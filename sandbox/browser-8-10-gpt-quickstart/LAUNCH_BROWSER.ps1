param([int]$DryRunCount = 0)
$ErrorActionPreference = "Stop"
if ($DryRunCount -lt 0 -or $DryRunCount -gt 10) { Write-Host "[ERROR] DryRunCount must be 0..10"; exit 11 }
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$chrome = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "$env:LocalAppData\Google\Chrome\Application\chrome.exe",
  "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if (-not $chrome) { Write-Host "[ERROR] Khong tim thay Chrome"; exit 10 }
Write-Host ""
Write-Host "[RON-SHO] STEP 1/3 - CHON SO TAB GPT" -ForegroundColor Cyan
Write-Host "Nhap so GPT tu 1 den 10 (VD: 1, 2, 8, 10)"
Write-Host "Nhap 0 de huy"
$choice = if ($DryRunCount -gt 0) { [string]$DryRunCount } else { Read-Host "Anh muon mo bao nhieu tab GPT? (0-10)" }
if ($choice -eq "0") { Write-Host "[STOP] Da huy"; exit 0 }
$count = 0
if (-not [int]::TryParse($choice,[ref]$count) -or $count -lt 1 -or $count -gt 10) { Write-Host "[ERROR] Chi nhap so nguyen tu 1 den 10, hoac 0 de huy"; exit 11 }
$profile = Join-Path $base "CHROME_PROFILE_RON_SHO"
$startPage = Join-Path $base "START_HERE.html"
if (-not (Test-Path -LiteralPath $startPage)) { Write-Host "[ERROR] Thieu START_HERE.html"; exit 12 }
if (-not (Test-Path -LiteralPath $profile)) { New-Item $profile -ItemType Directory -Force | Out-Null }
$url = [System.Uri]::new($startPage).AbsoluteUri
$urls = @($url) + @(1..$count | ForEach-Object { "https://chatgpt.com/" })
if ($DryRunCount -gt 0) {
  Write-Host "[DRY_RUN] REQUESTED_GPT_TABS=$count TOTAL_TABS=$($urls.Count)"
  Write-Host "[DRY_RUN] HELP=$($urls[0])"
  Write-Host "[DRY_RUN] GPT_URLS=$((@($urls | Where-Object { $_ -eq 'https://chatgpt.com/' })).Count)"
  Write-Host "[DRY_RUN] BROWSER_NOT_LAUNCHED"
  exit 0
}
Write-Host "[RON-SHO] STEP 2/3 - MO $count GPT TABS + 1 START TAB" -ForegroundColor Cyan
Write-Host "Chrome: $chrome"
Write-Host "Profile: $profile"
Write-Host "KHONG tu dong login / gui prompt / copy cookie."
$argList = @("--user-data-dir=$profile","--no-first-run","--new-window") + $urls
try { Start-Process -FilePath $chrome -ArgumentList $argList -ErrorAction Stop | Out-Null }
catch { Write-Host "[ERROR] Khong mo duoc Chrome: $_"; exit 13 }
Write-Host "[RON-SHO] STEP 3/3" -ForegroundColor Green
Write-Host "1. Chrome co 1 tab huong dan va $count tab GPT."
Write-Host "2. Neu co 'Log in' thi anh DANG NHAP TRUC TIEP."
Write-Host "3. Thu nhan tin thu cong GPT 01 va GPT 02."
Write-Host "4. Khong co 8/10 AI agent tu dong. Day la nhieu tab."
exit 0
