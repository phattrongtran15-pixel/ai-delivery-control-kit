/**
 * 6/12/24 actual protocol-level Playwright MCP clients in isolated browser sessions.
 * Logical actor identities are synthetic; no LLM model or real GPT account used.
 * Executes in a GitHub Actions hosted runner, never touches production credentials.
 */
import http from "node:http";
import fs from "node:fs";
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const OUT="evidence/actor-farm";fs.mkdirSync(OUT,{recursive:true});
const transportURL=new URL("http://localhost:8931/mcp");
const allStages=[6,12,24,48];
const sessions=new Set();const ledger=[];
const fixture=http.createServer((req,res)=>{
  const u=new URL(req.url,"http://127.0.0.1");
  if(u.pathname==="/actor"){
    const actor=u.searchParams.get("id")||"";
    if(!/^A[0-9]{2}$/.test(actor)){res.writeHead(400);return res.end("bad actor")}
    res.writeHead(200,{"Content-Type":"text/html; charset=utf-8",
      "Set-Cookie":"actor="+actor+"; Path=/; SameSite=Lax"});
    return res.end("<!doctype html><title>RON-SHO "+actor+"</title><h1>"+actor+
      "</h1><p class='signed'>Session attached to "+actor+"</p>"+
      "<button id='safe'>Authorized synthetic action</button>");
  }
  if(u.pathname==="/dashboard"){
    const rows=ledger.filter(x=>x.phase===48).map((x,i)=>
      "<tr><td>"+String(i+1)+"</td><td>"+x.actor+"</td><td>"+x.phase+
      "</td><td>"+x.status+"</td><td>"+x.elapsed_ms+" ms</td></tr>").join("");
    res.writeHead(200,{"Content-Type":"text/html; charset=utf-8"});
    return res.end("<!doctype html><style>body{font:18px Arial;background:#f4f7fa;color:#1b324b;padding:28px}"+
      "table{width:100%;border-collapse:collapse;background:white}td,th{padding:8px;border-bottom:1px solid #e0e5eb;text-align:left}"+
      "h1{font-size:28px}small{color:#576575}</style><h1>RON-SHO Browser Farm — 48 MCP actors</h1>"+
      "<small>Real independent MCP client connections; synthetic actor identities, no LLM calls</small>"+
      "<table><tr><th>No.</th><th>Actor</th><th>Batch</th><th>Verified</th><th>Latency</th></tr>"+
      rows+"</table>");
  }
  res.writeHead(404);res.end("not found");
});
await new Promise(resolve=>fixture.listen(0,"127.0.0.1",resolve));
const origin="http://127.0.0.1:"+fixture.address().port;
let stageName="preflight";
function safeBody(result,name){
  assert(!result.isError,"MCP_TOOL_ERROR:"+name+":"+JSON.stringify(result).slice(0,1200));
  return JSON.stringify(result.content);
}
async function clientConnect(actor){
  let error;
  for(let attempt=0;attempt<9;attempt++){
    const c=new Client({name:"ron-actor-"+actor,version:"0.1.0"},{capabilities:{}});
    const t=new StreamableHTTPClientTransport(transportURL);
    try{await c.connect(t);sessions.add(c);return c}
    catch(e){error=e;try{await t.close()}catch{};await new Promise(r=>setTimeout(r,500+150*attempt))}
  }
  throw new Error("ACTOR_CONNECT_FAILED:"+actor+":"+String(error));
}
async function mapLimit(items,max,fn){
  let i=0;const results=new Array(items.length);
  await Promise.all(Array.from({length:Math.min(max,items.length)},async()=>{
    while(i<items.length){const n=i++;results[n]=await fn(items[n],n);}
  }));
  return results;
}
function pct(values,p){
  const x=[...values].sort((a,b)=>a-b);
  return Math.round(x[Math.max(0,Math.ceil(x.length*p)-1)]*10)/10;
}
const summary={version:"mcp-actor-farm-v1",run:process.env.GITHUB_RUN_ID||"UNKNOWN",
  real_mcp_client_sessions:true,real_model_agents:false,credentials_used:false,
  browser_service:"@playwright/mcp@0.0.83",groups:[],status:"UNKNOWN"};
try{
  for(const n of allStages){
    stageName="batch-"+n;
    const actors=Array.from({length:n},(_,i)=>"A"+String(i+1).padStart(2,"0"));
    const created=[];
    const start=Date.now();const latencies=[];
    try{
      // Start and test real protocol sessions in cohorts up to 48, bounded connection launch rather than 24 simultaneous handshakes.
      await mapLimit(actors,6,async actor=>{
        const client=await clientConnect(actor);
        created.push([actor,client]);
      });
      const tools=await created[0][1].listTools();
      for(const name of ["browser_navigate","browser_evaluate"]){
        assert(tools.tools.some(t=>t.name===name),"MISSING_MCP_TOOL:"+name);
      }
      // Real, distinct clients: navigate all first, verify ALL second.
      const verification=await mapLimit(created,6,async([actor,c])=>{
        const t=Date.now();
        safeBody(await c.callTool({name:"browser_navigate",
          arguments:{url:origin+"/actor?id="+actor}}),"navigate "+actor);
        return {actor,client:c,latency_ms:Date.now()-t};
      });
      await mapLimit(verification,6,async ({actor,client,latency_ms})=>{
        const actual=safeBody(await client.callTool({name:"browser_evaluate",
          arguments:{function:"() => ({cookie:document.cookie, title:document.title})"}}),
          "evaluate "+actor);
        assert(actual.includes("actor="+actor), "WRONG_SESSION_OR_COOKIE:"+actor+":"+actual.slice(0,250));
        for(const other of actors){
          if(other!==actor) assert(!actual.includes("actor="+other),
            "CROSS_ACTOR_COOKIE_LEAK:"+actor+"/"+other);
        }
        latencies.push(latency_ms);
        ledger.push({actor,phase:n,status:"PASS",elapsed_ms:latency_ms});
      });
      // Verify that previous client A01 was not overwritten after all other clients navigated.
      const [first,cf]=created[0];
      const final=safeBody(await cf.callTool({name:"browser_evaluate",
        arguments:{function:"() => document.cookie"}}),"recheck "+first);
      assert(final.includes("actor="+first),"SESSION_REUSE_BLEED:"+first);
      summary.groups.push({contexts:n,independent_mcp_connections:n,success:n,
        elapsed_ms:Date.now()-start,p50_navigation_ms:pct(latencies,.5),
        p95_navigation_ms:pct(latencies,.95),cookie_bleed:0});
      console.log("RON_REAL_MCP_ACTOR_FARM_PASS:"+n,JSON.stringify(summary.groups.at(-1)));
      if(n===48){
        try{
          safeBody(await cf.callTool({name:"browser_navigate",
            arguments:{url:origin+"/dashboard"}}),"dashboard");
          const shot=await cf.callTool({name:"browser_take_screenshot",
            arguments:{type:"png"}});
          const img=shot.content?.find(c=>c.type==="image" && c.data);
          if(img){fs.writeFileSync(OUT+"/actor-monitor-48.png",Buffer.from(img.data,"base64"));
            summary.monitor_screenshot="actor-monitor-48.png";}
          else{summary.monitor_screenshot="NOT_AVAILABLE";summary.monitor_screenshot_error="MCP returned no image";}
        }catch(e){summary.monitor_screenshot_error=String(e);}
        // Even without screenshot, preserve the source of the live dashboard actually served to browser.
        fs.writeFileSync(OUT+"/actor-ledger-48.json",JSON.stringify(ledger,null,2));
      }
    }finally{
      await mapLimit(created,6,async ([actor,c])=>{await c.close().catch(()=>{});sessions.delete(c)});
    }
  }
  summary.status="PASS";
}catch(e){
  summary.status="FAIL";summary.failed_stage=stageName;summary.reason=String(e);
  console.error("RON_ACTOR_FARM_FAIL",String(e));
  process.exitCode=1;
}finally{
  fs.writeFileSync(OUT+"/scale-receipt.json",JSON.stringify(summary,null,2)+"\n");
  await Promise.all([...sessions].map(c=>c.close().catch(()=>{})));
  await new Promise(resolve=>fixture.close(resolve));
}
