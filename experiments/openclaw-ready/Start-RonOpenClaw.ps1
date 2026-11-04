#requires -Version 5.1
[CmdletBinding()]
param([ValidateSet("Install","SelfTest","Status","Rollback")][string]$Mode="Install",[switch]$NoBrowser)
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$Profile="ronsho-sandbox"
$Root=Join-Path $env:USERPROFILE ".openclaw-ronsho-sandbox"
$Config=Join-Path $Root "openclaw.json"
$Owner=Join-Path $Root "RONSHO_OWNED.json"
$Evidence=Join-Path $Root "ronsho-evidence"
$Program=Join-Path $Root "ronsho-bootstrap"
$TaskScript=Join-Path $Program "Safe-Health.ps1"
$TaskReceipt=Join-Path $Evidence "latest-scheduled-health.json"
$TaskName="RONSHO_SAFE_HEALTH_30M"
$Stage="PREFLIGHT"
function Utc { return (Get-Date).ToUniversalTime().ToString("o") }
function Save([string]$name,[object]$o) {
  if(!(Test-Path $Evidence)){New-Item -ItemType Directory -Force -Path $Evidence|Out-Null}
  $o|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Evidence $name) -Encoding UTF8
}
function Cli([string[]]$parts) {
  $old=$ErrorActionPreference
  $ErrorActionPreference="Continue"
  try {$out=(& openclaw --profile $Profile @parts 2>&1|Out-String);$rc=$LASTEXITCODE}
  finally {$ErrorActionPreference=$old}
  return [pscustomobject]@{ok=($rc -eq 0);exit=$rc;output=[string]$out}
}
function Need([string[]]$parts) {
  $r=Cli $parts
  if(!$r.ok){throw ("OpenClaw command failed: "+($parts -join " ")+" EXIT="+$r.exit+" "+$r.output)}
  return $r
}
function Decode([string]$s){try{return $s|ConvertFrom-Json -ErrorAction Stop}catch{return $null}}
function Healthy {
  $r=Cli @("health","--json","--timeout","8000")
  $j=Decode $r.output
  if(!$r.ok -or $null -eq $j){return $false}
  if(($j.PSObject.Properties.Name -contains "status") -and $j.status -eq "starting"){return $false}
  return (($j.PSObject.Properties.Name -contains "ok" -and $j.ok -eq $true) -or ($j.PSObject.Properties.Name -contains "status" -and $j.status -in @("ok","ready","healthy")))
}
function Job {
  $raw=Need @("automations","list","--all","--json")
  $j=Decode $raw.output
  if($null -eq $j){throw "Unparseable automations JSON"}
  $items=@()
  if($j -is [array]){$items=@($j)}
  elseif($j.PSObject.Properties.Name -contains "jobs"){$items=@($j.jobs)}
  elseif($j.PSObject.Properties.Name -contains "items"){$items=@($j.items)}
  else{throw "Unknown automation list schema"}
  $match=@($items|Where-Object {$_.name -eq $TaskName})
  if($match.Count -gt 1){throw "Duplicate cron definitions - HOLD"}
  if($match.Count -eq 0){return $null}
  return $match[0]
}
if($Mode -eq "SelfTest"){
  $cfg=@{gateway=@{mode="local";bind="loopback";port=18847;auth=@{mode="token"}};tools=@{deny=@("exec","write","browser")}}
  $j=Decode ($cfg|ConvertTo-Json -Depth 9)
  if($j.gateway.bind -ne "loopback" -or $j.gateway.auth.mode -ne "token" -or -not ($j.tools.deny -contains "exec")){throw "SELFTEST_FAILED"}
  Write-Host "PASS SELFTEST: separated profile, loopback/token, no privileged agent tools"
  return
}
if($Mode -eq "Status"){
  if(!(Get-Command openclaw -ErrorAction SilentlyContinue)){Write-Host "HOLD CLI_NOT_INSTALLED";exit 2}
  $ok=Healthy
  $job=$null
  if($ok){try{$job=Job}catch{}}
  $data=$null
  if(Test-Path $TaskReceipt){$data=Decode (Get-Content -Raw $TaskReceipt)}
  $pass=($ok -and $null -ne $job -and $null -ne $data -and $data.kind -eq "RONSHO_SAFE_HEALTH")
  $res=@{utc=Utc;status=if($pass){"SAFE_AUTOMATION_READY"}else{"HOLD"};gatewayHealthy=$ok;jobPresent=($null -ne $job);receiptPresent=($null -ne $data)}
  Save "STATUS.json" $res
  $res|ConvertTo-Json -Compress|Write-Host
  if(!$pass){exit 3}
  return
}
if($Mode -eq "Rollback"){
  if(!(Test-Path $Owner)){throw "Not a RON-SHO owned profile, rollback refused"}
  if(Get-Command openclaw -ErrorAction SilentlyContinue){
    try{$job=Job;if($null -ne $job -and $job.id){$null=Need @("automations","remove",([string]$job.id))}}catch{Write-Warning $_.Exception.Message}
    $null=Cli @("gateway","stop")
    $null=Cli @("gateway","uninstall")
  }
  Save "ROLLBACK.json" @{utc=Utc;result="ROLLBACK_REQUESTED";filesRetained=$true;profile=$Profile}
  Write-Host "ROLLBACK_REQUESTED; run Status for independent verification."
  return
}
try{
  foreach($d in @($Root,$Program,$Evidence)){if(!(Test-Path $d)){New-Item -ItemType Directory -Force -Path $d|Out-Null}}
  $Stage="INSTALL_CLI"
  if(!(Get-Command openclaw -ErrorAction SilentlyContinue)){
    $inst=Join-Path $Program "official-install.ps1"
    Invoke-WebRequest -UseBasicParsing -Uri "https://openclaw.ai/install.ps1" -OutFile $inst
    Save "INSTALLER.json" @{url="https://openclaw.ai/install.ps1";sha256=(Get-FileHash $inst -Algorithm SHA256).Hash;unpinnedInstaller=$true;utc=Utc}
    $ps=Join-Path $env:WINDIR "System32\WindowsPowerShell\v1.0\powershell.exe"
    & $ps -NoProfile -ExecutionPolicy Bypass -File $inst -NoOnboard
    if($LASTEXITCODE -ne 0){throw "Official installer failed"}
    $env:PATH=[Environment]::GetEnvironmentVariable("Path","Machine")+";"+[Environment]::GetEnvironmentVariable("Path","User")
    if(!(Get-Command openclaw -ErrorAction SilentlyContinue)){throw "CLI missing after install"}
  }
  $version=Need @("--version")
  $Stage="CHECKPOINT_CONFIG"
  if((Test-Path $Config) -and !(Test-Path $Owner)){throw "Existing profile not owned by bootstrap - HOLD"}
  if(!(Test-Path $Config)){
    $bytes=New-Object byte[] 32
    $rng=[Security.Cryptography.RandomNumberGenerator]::Create()
    try{$rng.GetBytes($bytes)}finally{$rng.Dispose()}
    $token=[Convert]::ToBase64String($bytes)
    $cfg=[ordered]@{
      gateway=[ordered]@{mode="local";port=18847;bind="loopback";auth=@{mode="token";token=$token};controlUi=@{enabled=$true}}
      tools=@{deny=@("exec","process","read","write","edit","apply_patch","browser","message","cron","nodes","gateway")}
      agents=@{defaults=@{contextInjection="never"}}
    }
    $cfg|ConvertTo-Json -Depth 9|Set-Content -LiteralPath $Config -Encoding UTF8
    @{utc=Utc;profile=$Profile;initialConfigSha256=(Get-FileHash $Config -Algorithm SHA256).Hash}|ConvertTo-Json|Set-Content -LiteralPath $Owner -Encoding UTF8
  }
  $Stage="VALIDATE_CONFIG"
  $validation=Need @("config","validate","--json")
  $v=Decode $validation.output
  if($null -eq $v -or $v.valid -ne $true){throw "Configuration not independently valid"}
  $Stage="START_GATEWAY"
  $ready=Healthy
  if(!$ready){
    $null=Need @("gateway","install")
    $null=Cli @("gateway","start")
    for($i=0;$i -lt 15;$i++){Start-Sleep -Seconds 3;if(Healthy){$ready=$true;break}}
  }
  if(!$ready){throw "Gateway not healthy - no automation writes permitted"}
  $Stage="INSTALL_SAFE_COMMAND"
  if(!(Test-Path $TaskScript)){
    @'
#requires -Version 5.1
$ErrorActionPreference="Stop"
$root=Join-Path $env:USERPROFILE ".openclaw-ronsho-sandbox"
$dir=Join-Path $root "ronsho-evidence"
if(!(Test-Path $dir)){New-Item -ItemType Directory -Force -Path $dir|Out-Null}
@{kind="RONSHO_SAFE_HEALTH";utc=(Get-Date).ToUniversalTime().ToString("o");source="OPENCLAW_COMMAND_JOB";noModelCalls=$true;noN8nCalls=$true}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $dir "latest-scheduled-health.json") -Encoding UTF8
Write-Output "RONSHO_SAFE_HEALTH_OK"
'@ | Set-Content -LiteralPath $TaskScript -Encoding UTF8
  }
  $Stage="REGISTER_JOB"
  $job=Job
  if($null -eq $job){
    $argv=ConvertTo-Json -InputObject @("powershell.exe","-NoProfile","-NonInteractive","-ExecutionPolicy","Bypass","-File",$TaskScript) -Compress
    $null=Need @("automations","create","*/30 * * * *","--name",$TaskName,"--command-argv",$argv,"--command-cwd",$Root,"--no-deliver")
    $job=Job
  }
  if($null -eq $job -or !$job.id){throw "Scheduled job not readable after creation"}
  $Stage="RUN_JOB_AND_READBACK"
  $before=(Get-Date).ToUniversalTime().AddSeconds(-3)
  $null=Need @("automations","run",([string]$job.id),"--wait","--wait-timeout","2m")
  if(!(Test-Path $TaskReceipt)){throw "Job returned without file receipt"}
  $receipt=Decode (Get-Content -Raw $TaskReceipt)
  if($null -eq $receipt -or $receipt.kind -ne "RONSHO_SAFE_HEALTH" -or ([datetime]$receipt.utc).ToUniversalTime() -lt $before){throw "Invalid or stale effect receipt"}
  Save "BOOTSTRAP_RESULT.json" @{utc=Utc;status="SAFE_AUTOMATION_READY";gatewayReady=$true;modelAuthenticationVerified=$false;n8nProductionConnected=$false;automationId=$job.id;cliVersion=$version.output.Trim();profile=$Profile}
  Write-Host "SAFE_AUTOMATION_READY"
  Write-Host ("Evidence: "+(Join-Path $Evidence "BOOTSTRAP_RESULT.json"))
  Write-Host "Now login to an existing model provider once: openclaw --profile ronsho-sandbox onboard --classic"
  if(!$NoBrowser){try{$null=Cli @("dashboard")}catch{}}
}catch{
  try{Save "BOOTSTRAP_HOLD.json" @{utc=Utc;status="HOLD";stage=$Stage;reason=$_.Exception.Message;defaultProfileUntouched=$true}}catch{}
  Write-Host ("HOLD at "+$Stage+": "+$_.Exception.Message)
  exit 4
}
