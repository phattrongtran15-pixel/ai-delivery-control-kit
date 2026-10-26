// Two REAL MCP HTTP clients against Playwright MCP browser tools.
// Isolated ephemeral GitHub runner, simulated agent identities.
import http from "node:http";
import fs from "node:fs";
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const evidenceDir="evidence";
fs.mkdirSync(evidenceDir,{recursive:true});
const originServer=http.createServer((req,res)=>{
  const u=new URL(req.url,"http://127.0.0.1");
  const actor=u.searchParams.get("actor");
  if(u.pathname==="/set"&&(actor==="A"||actor==="B")){
    res.writeHead(200,{"Content-Type":"text/html","Set-Cookie":"actor="+actor+"; Path=/; SameSite=Lax"});
    res.end("<html><title>MCP session "+actor+"</title><body>isolated-session-"+actor+"</body></html>");
  }else{res.writeHead(404);res.end("not found")}
});
await new Promise(resolve=>originServer.listen(0,"127.0.0.1",resolve));
const fixture="http://127.0.0.1:"+originServer.address().port;
const url=new URL("http://127.0.0.1:8931/mcp");
const clients=[];
async function connect(label){
  let last;
  for(let i=0;i<45;i++){
    const c=new Client({name:"ron-"+label,version:"0.0.1"},{capabilities:{}});
    const t=new StreamableHTTPClientTransport(url);
    try{await c.connect(t);clients.push(c);return c}
    catch(e){last=e;try{await t.close()}catch{};await new Promise(r=>setTimeout(r,1100))}
  }
  throw new Error("MCP_CONNECT_TIMEOUT:"+String(last));
}
try{
  const a=await connect("agent-A");
  const b=await connect("agent-B");
  const tools=await a.listTools();
  const available=tools.tools.map(x=>x.name);
  for(const n of ["browser_navigate","browser_evaluate"])assert(available.includes(n),"MCP_TOOL_MISSING:"+n);
  function validateResult(r,label){
    assert(!r.isError,"MCP_ERROR:"+label+":"+JSON.stringify(r).slice(0,800));
    return JSON.stringify(r.content);
  }
  validateResult(await a.callTool({name:"browser_navigate",arguments:{url:fixture+"/set?actor=A"}}),"navigate-A");
  validateResult(await b.callTool({name:"browser_navigate",arguments:{url:fixture+"/set?actor=B"}}),"navigate-B");
  const ra=validateResult(await a.callTool({name:"browser_evaluate",arguments:{function:"() => document.cookie"}}),"A-cookie");
  const rb=validateResult(await b.callTool({name:"browser_evaluate",arguments:{function:"() => document.cookie"}}),"B-cookie");
  assert(ra.includes("actor=A")&&!ra.includes("actor=B"),"CLIENT_A_STORAGE_CROSSED:"+ra);
  assert(rb.includes("actor=B")&&!rb.includes("actor=A"),"CLIENT_B_STORAGE_CROSSED:"+rb);
  const summary={result:"PASS",mcp_transport:"streamable-http",
    actual_mcp_client_connections:2,actual_browser_tools:["browser_navigate","browser_evaluate"],
    per_client_browser_context_isolated:true,client_a_cookie_only_A:true,client_b_cookie_only_B:true,
    sdk_version:"1.32.0",server_package:"@playwright/mcp@0.0.83",
    real_gpt_agent_or_remote_mcp_gateway:false};
  fs.writeFileSync(evidenceDir+"/mcp-multiclient.json",JSON.stringify(summary,null,2)+"\n");
  console.log("RON_REAL_MCP_TWO_CLIENT_SESSION_ISOLATION_PASS");
}catch(e){
  fs.writeFileSync(evidenceDir+"/mcp-multiclient-failure.json",JSON.stringify({result:"FAILED",message:String(e)},null,2));
  throw e;
}finally{
  await Promise.all(clients.map(c=>c.close().catch(()=>{})));
  await new Promise(resolve=>originServer.close(resolve));
}
