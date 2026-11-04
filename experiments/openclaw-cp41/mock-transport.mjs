import http from "node:http";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import {spawn} from "node:child_process";
import {fileURLToPath} from "node:url";
const __filename = fileURLToPath(import.meta.url);
const hash = (x) => crypto.createHash("sha256").update(JSON.stringify(x)).digest("hex");
const delay = (ms) => new Promise((resolve) => setTimeout(resolve,ms));
const evidenceRoot = path.resolve(process.env.CP41_EVIDENCE_DIR || "evidence/cp41");
fs.mkdirSync(evidenceRoot,{recursive:true});
function save(name,data){fs.writeFileSync(path.join(evidenceRoot,name),JSON.stringify(data,null,2)+"\n");}
function cleanEnv(){return {PATH:process.env.PATH, HOME:process.env.CP41_SAFE_HOME || os.tmpdir(),TMPDIR:process.env.RUNNER_TEMP || os.tmpdir(),XDG_CONFIG_HOME:process.env.CP41_SAFE_HOME || os.tmpdir(),LANG:"C.UTF-8",CI:"true",OPENCLAW_DISABLE_UPDATE_CHECK:"1",OPENCLAW_DISABLE_TELEMETRY:"1"};}
async function call(base,pathname,body,{timeoutMs=800,permission="sandbox-operator"}={}){
 const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),timeoutMs);
 try{
   const res=await fetch(base+pathname,{method:body===undefined?"GET":"POST",headers:{"content-type":"application/json","x-sandbox-permission":permission},body:body===undefined?undefined:JSON.stringify(body),signal:controller.signal});
   const data=await res.json();
   if(!res.ok)throw Object.assign(new Error(data.error||"HTTP_ERROR"),{code:res.status});
   return data;
 }finally{clearTimeout(timer);}
}
async function runWorkflow(base,scenario,workId){
 const logs=[];
 try{
  const ready=await call(base,"/mock-n8n/health?scenario="+scenario,undefined);
  logs.push({step:"health",status:ready.state});
  if(ready.ready!==true||ready.state!=="ready")throw new Error("FALSE_READY_BLOCKED");
  let created;let retries=0;
  for(let a=0;a<2;a++){
   try{
    created=await call(base,"/mock-n8n/create",{scenario,workId,idempotencyKey:workId},{timeoutMs:60,permission:scenario==="missing_permission"?"":"sandbox-operator"});
    break;
   }catch(e){
    logs.push({step:"create_attempt",attempt:a+1,error:String(e.message)});
    if(e.name==="AbortError"&&a===0){retries++;continue;}
    throw e;
   }
  }
  if(!created)throw new Error("CREATE_UNCERTAIN");
  logs.push({step:"create",workflowId:created.workflowId,reused:created.reused});
  const validated=await call(base,"/mock-n8n/validate",{scenario,workId,workflowId:created.workflowId});
  if(validated.valid!==true)throw new Error("VALIDATION_FAILED");
  logs.push({step:"validate",valid:true});
  const tested=await call(base,"/mock-n8n/test",{scenario,workId,workflowId:created.workflowId});
  if(tested.result!=="PASS_MOCK")throw new Error("TEST_FAILED");
  logs.push({step:"test",result:tested.result});
  const received=await call(base,"/mock-n8n/evidence",{scenario,workId,workflowId:created.workflowId});
  if(received.kind!=="SIMULATED_EVIDENCE" || received.receiptSha!==hash(received.payload))throw new Error("EVIDENCE_INVALID");
  logs.push({step:"evidence",receiptSha:received.receiptSha});
  return {ok:true,scenario,workId,retries,logs,receiptSha:received.receiptSha};
 }catch(e){return {ok:false,scenario,workId,error:String(e.message),logs};}
}
if(process.argv[2]==="--client"){
 const [scenario,workId,base]=process.argv.slice(3);
 if(!scenario||!workId||!base.startsWith("http://127.0.0.1:"))process.exit(30);
 const r=await runWorkflow(base,scenario,workId);console.log(JSON.stringify(r));process.exit(r.ok?0:21);
}
function stateFor(m,scenario,workId){
 const key=scenario+":"+workId;let s=m.get(key);
 if(!s){s={scenario,workId,createRequests:0,uniqueCreates:0,validations:0,tests:0,evidence:0,workflowId:null};m.set(key,s);}
 return s;
}
function reply(res,status,data,delayMs=0){
 const send=()=>{if(!res.writableEnded&&!res.destroyed){res.writeHead(status,{"content-type":"application/json"});res.end(JSON.stringify(data));}};
 if(delayMs)setTimeout(send,delayMs);else send();
}
function chooseExecTool(tools){
 return (tools||[]).find(t=>{let name=t.function?.name||t.name;return name==="exec"||name==="functions.exec"||name==="shell";});
}
function streamCompletion(res,model,choice){
 res.writeHead(200,{"content-type":"text/event-stream","cache-control":"no-cache","connection":"keep-alive"});
 const id="chatcmpl-cp41";
 const payload={id,object:"chat.completion.chunk",created:1793790000,model,choices:[{index:0,delta:choice.delta,finish_reason:null}]};
 res.write("data: "+JSON.stringify(payload)+"\n\n");
 res.write("data: "+JSON.stringify({...payload,choices:[{index:0,delta:{},finish_reason:choice.finish}]})+"\n\n");
 res.end("data: [DONE]\n\n");
}
async function startServer(){
 const states=new Map(); const modelCalls=[]; const audit=[];
 const server=http.createServer(async(req,res)=>{
  const url=new URL(req.url,"http://127.0.0.1");
  if(url.pathname==="/mock-n8n/health"){
   const scenario=url.searchParams.get("scenario");
   return reply(res,200,scenario==="false_ready"?{ready:false,state:"stopped"}:{ready:true,state:"ready"});
  }
  let body={};
  try{let input="";for await (const chunk of req)input+=chunk; if(input)body=JSON.parse(input);}
  catch{return reply(res,400,{error:"BAD_JSON"});}
  if(url.pathname==="/v1/chat/completions"){
   const tools=body.tools||[];
   const names=tools.map(t=>t.function?.name||t.name);
   const done=(body.messages||[]).some(m=>m.role==="tool"||m.role==="function");
   const rec={stream:body.stream===true,model:body.model,toolNames:names,done};
   modelCalls.push(rec);
   let name="";let args={};
   if(!done){
     const tool=chooseExecTool(tools);
     if(tool){
       name=tool.function?.name||tool.name;
       const props=tool.function?.parameters?.properties||tool.parameters?.properties||{};
       const cmd=process.execPath+" "+JSON.stringify(__filename)+" --client success WORK-CP41-AGENT http://127.0.0.1:"+server.address().port;
       if("command" in props)args.command=cmd;
       else if("cmd" in props)args.cmd=cmd;
       else if("script" in props)args.script=cmd;
       else args.command=cmd;
       rec.selectedTool=name;rec.args=args;
     }else rec.selectedTool="NO_EXEC_TOOL";
   }
   let choice;
   if(done)choice={delta:{role:"assistant",content:"CP41_MOCK_AGENT_COMPLETED"},finish:"stop"};
   else if(name)choice={delta:{role:"assistant",tool_calls:[{index:0,id:"call_cp41_one",type:"function",function:{name,arguments:JSON.stringify(args)}}]},finish:"tool_calls"};
   else choice={delta:{role:"assistant",content:"CP41_NO_EXEC_TOOL"},finish:"stop"};
   if(body.stream===true)return streamCompletion(res,body.model||"deterministic",choice);
   if(name&&!done)return reply(res,200,{id:"chatcmpl-cp41",object:"chat.completion",created:1793790000,model:body.model,choices:[{index:0,message:{role:"assistant",content:null,tool_calls:[{id:"call_cp41_one",type:"function",function:{name,arguments:JSON.stringify(args)}}]},finish_reason:"tool_calls"}]});
   return reply(res,200,{id:"chatcmpl-cp41",object:"chat.completion",created:1793790000,model:body.model,choices:[{index:0,message:{role:"assistant",content:done?"CP41_MOCK_AGENT_COMPLETED":"CP41_NO_EXEC_TOOL"},finish_reason:"stop"}]});
  }
  const m=url.pathname.match(/^\/mock-n8n\/(create|validate|test|evidence)$/);
  if(!m)return reply(res,404,{error:"ROUTE_NOT_FOUND"});
  if(body.workId===undefined || body.scenario===undefined)return reply(res,400,{error:"INVALID_WORK"});
  const s=stateFor(states,body.scenario,body.workId);const step=m[1];
  audit.push({scenario:body.scenario,workId:body.workId,step});
  if(req.headers["x-sandbox-permission"]!=="sandbox-operator")return reply(res,403,{error:"PERMISSION_DENIED"});
  if(step==="create"){
   if(body.idempotencyKey!==body.workId)return reply(res,409,{error:"IDEMPOTENCY_MISMATCH"});
   s.createRequests++;
   const reused=!!s.workflowId;
   if(!reused){s.uniqueCreates++;s.workflowId="wf-"+hash({scenario:body.scenario,workId:body.workId}).slice(0,12);}
   const wait=body.scenario==="timeout_exhausted"||body.scenario==="timeout_recovered"&&s.createRequests===1?250:0;
   return reply(res,200,{workflowId:s.workflowId,reused},wait);
  }
  if(body.workflowId!==s.workflowId||!s.workflowId)return reply(res,409,{error:"STAGE_ORDER_VIOLATION"});
  if(step==="validate"){s.validations=1;return reply(res,200,{valid:true});}
  if(step==="test"){
   if(s.validations!==1)return reply(res,409,{error:"NOT_VALIDATED"});
   s.tests=1;return reply(res,200,{result:"PASS_MOCK"});
  }
  if(step==="evidence"){
   if(s.tests!==1)return reply(res,409,{error:"NOT_TESTED"});
   s.evidence=1;
   const payload={scenario:s.scenario,workId:s.workId,workflowId:s.workflowId,validations:s.validations,tests:s.tests,simulation:true};
   return reply(res,200,{kind:"SIMULATED_EVIDENCE",payload,receiptSha:hash(payload)});
  }
 });
 await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));
 return {server,states,modelCalls,audit,base:"http://127.0.0.1:"+server.address().port};
}
async function spawnCaptured(executable,args,options={}){
 return await new Promise(resolve=>{
  const child=spawn(executable,args,{cwd:options.cwd||process.cwd(),env:options.env||cleanEnv(),stdio:["ignore","pipe","pipe"]});
  let stdout="",stderr="";let ended=false;
  child.stdout.on("data",x=>{stdout+=x.toString().slice(0,100000);});
  child.stderr.on("data",x=>{stderr+=x.toString().slice(0,100000);});
  const t=setTimeout(()=>{child.kill("SIGTERM");setTimeout(()=>child.kill("SIGKILL"),1500).unref();},options.timeoutMs||105000);
  child.on("error",err=>{if(ended)return;ended=true;clearTimeout(t);resolve({code:-1,error:String(err),stdout,stderr});});
  child.on("exit",(code,signal)=>{if(ended)return;ended=true;clearTimeout(t);resolve({code,signal,stdout,stderr});});
 });
}
async function main(){
 const {server,states,modelCalls,audit,base}=await startServer();
 const checks=[]; let agentRun=null;
 try{
  for(const [scenario,wid,expectOK] of [
   ["success","WORK-CP41-SUCCESS",true],
   ["timeout_recovered","WORK-CP41-TIMEOUT",true],
   ["duplicate","WORK-CP41-DUP",true],
   ["missing_permission","WORK-CP41-DENY",false],
   ["false_ready","WORK-CP41-FALSE",false],
   ["timeout_exhausted","WORK-CP41-EXHAUST",false]]){
   const first=await runWorkflow(base,scenario,wid);
   const second=scenario==="duplicate"?await runWorkflow(base,scenario,wid):null;
   const s=states.get(scenario+":"+wid);
   const extra=first.ok===expectOK && (!second||second.ok) &&
       (s?.uniqueCreates||0)<2 &&
       (scenario==="missing_permission"||scenario==="false_ready"?(s?.uniqueCreates||0)===0:true) &&
       (scenario==="timeout_exhausted"?(s?.tests||0)===0:true) &&
       (scenario==="timeout_recovered"?first.retries===1:true);
   checks.push({case:scenario,pass:extra,first,second,state:s||null});
  }
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"cp41-openclaw-"));
  const config={
   agents:{defaults:{model:{primary:"ronmock/deterministic"},contextInjection:"never"}},
   models:{providers:{ronmock:{baseUrl:base+"/v1",api:"openai-completions",auth:"api-key",apiKey:"cp41-fake-local-only",models:[{id:"deterministic",name:"CP41 Fake Deterministic Model",reasoning:false,input:["text"],contextWindow:16384,maxTokens:512,cost:{input:0,output:0,cacheRead:0,cacheWrite:0}}]}}},
   tools:{profile:"coding"}
  };
  const configPath=path.join(tmp,"config.json");
  fs.writeFileSync(configPath,JSON.stringify(config));
  const cli=process.env.CP41_OPENCLAW_CLI;
  const env={...cleanEnv(),CP41_SAFE_HOME:tmp,HOME:tmp,XDG_CONFIG_HOME:path.join(tmp,"config"),CP41_EVIDENCE_DIR:evidenceRoot};
  const mission="CP41 SANDBOX MISSION: use your shell exec tool exactly once to run the local fake n8n transport client. Create -> validate -> test -> evidence for WORK-CP41-AGENT. Do not reach real n8n, external model APIs, or write outside sandbox.";
  agentRun=await spawnCaptured(process.execPath,[cli,"agent","exec",mission,"--config",configPath,"--cwd",process.cwd(),"--code-mode","direct","--json"],{env,timeoutMs:125000});
  let parsed=null;try{parsed=JSON.parse(agentRun.stdout);}catch{}
  const agentState=states.get("success:WORK-CP41-AGENT");
  checks.push({case:"openclaw_agent_exec_real",pass:agentRun.code===0 && modelCalls.length>=2 && !!agentState && agentState.uniqueCreates===1 && agentState.validations===1 && agentState.tests===1 && agentState.evidence===1,modelCalls:modelCalls.length,agentExit:agentRun.code,agentEnvelope:parsed?{ok:parsed.ok,status:parsed.status,toolSummary:parsed.toolSummary,final:parsed.final}:null,agentState:agentState||null});
  save("agent-stdout.json",{exit:agentRun.code,stdout:agentRun.stdout.slice(0,40000)});
  save("agent-stderr.json",{exit:agentRun.code,stderr:agentRun.stderr.slice(-30000)});
  save("mock-model-requests.json",modelCalls);
  save("fake-n8n-audit.json",audit);
  const receipt={schema:"RONSHO_CP41_V1",fakeModel:true,fakeN8n:true,noProviderApiCalls:true,noProduction:true,source:"openclaw@2026.10.10 via GitHub Action",checks,passed:checks.filter(x=>x.pass).length,total:checks.length,decision:checks.every(x=>x.pass)?"GO_SANDBOX_MOCK_ONLY":"HOLD_INTEGRATION"};
  save("CP41_TEST_RECEIPT.json",receipt);
  for(const c of checks)console.log((c.pass?"PASS":"FAIL")+" "+c.case);
  console.log("CP41_RESULT="+receipt.passed+"/"+receipt.total+" "+receipt.decision);
  if(!checks.every(x=>x.pass))process.exitCode=1;
 }finally{server.close();}
}
await main();
