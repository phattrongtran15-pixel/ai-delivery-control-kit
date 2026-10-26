#!/usr/bin/env python3
"""Build one self-contained, zero-network RON-SHO Control Console from verified
GitHub dossier and source files. This is a review-only dashboard, not live AIOS.
"""
import html,json,re,argparse,hashlib,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
DOSSIER=HERE.parent/"five-gates"
OUT=HERE/"dist"
REPO="phattrongtran15-pixel/ai-delivery-control-kit"
BRANCH="sandbox/upstream-browser-skill-farm-20261026"
RUN=40354279483
LABELS=[
"Browser giám sát nhiều AI","MCP đa phiên cô lập","AI học và phát triển kỹ năng",
"Record · Replay · Verify","Cache thao tác","Bộ nhớ tìm kiếm xuyên agent",
"Automation","Shared Memory","Cây phát triển năng lực"]
STATES=[
"STAGING_PARTIAL","STAGING_VERIFIED","STAGING_PARTIAL","STAGING_VERIFIED_LIMITED",
"STAGING_PARTIAL","STAGING_VERIFIED_LIMITED","STAGING_VERIFIED_LIMITED",
"STAGING_VERIFIED_LIMITED","STAGING_PARTIAL"]
PROOFS=[
"48 actor synthetic, browser dashboard PNG","48 independent MCP HTTP clients, cookie isolation",
"Proposed skill + independent fixture verifier; no autonomous model",
"M4 replay 3/3; 48 guarded browser replays, server receipt",
"48 warm cache hits; no real Stagehand speedup benchmark",
"FTS5 search in independent subprocesses and GitHub jobs",
"GitHub Actions repeatable CI; no running n8n service",
"Artifact handoff + two test agent homes; no live Local↔Cloud",
"Archify HTML source graph + versioned lineage; no live AIOS registry"]
UPSTREAM=["BrowserOS (candidate)","Playwright MCP (tested)","OpenAdapt (source only)",
"Browser Use / fixture (tested)","Stagehand (source only)","FTS5 test adapter (tested), Mem0 source only",
"GitHub Actions (tested), n8n source only","Skills CLI (tested), real RonSkillStore not bound",
"Archify / LikeC4 (tested diagrams), OpenSpec requirements"]
def read(rel):return (DOSSIER/rel).read_text(encoding="utf8")
def get_data():
    # Read-only integration projection. BrowserOS and RonSkillStore default fail closed.
    changes=json.loads((HERE/"lineage/openspec_changes.json").read_text(encoding="utf8"))
    skill_lineage=json.loads((HERE/"lineage/skill_versions.json").read_text(encoding="utf8"))
    browseros=json.loads((HERE/"adapters/browseros.json").read_text(encoding="utf8"))
    skillstore=json.loads((HERE/"adapters/ronskillstore.json").read_text(encoding="utf8"))
    assert changes["canonical_change_registry"] is False
    assert skill_lineage["canonical_store"] is False
    for source in (browseros,skillstore):
        assert source["mode"]=="DISCONNECTED" and source["runtime_status"]=="BLOCKED_NOT_CONNECTED"
    ids={c["change_id"] for c in changes["changes"]}
    assert len(ids)==len(changes["changes"])
    for skill in skill_lineage["skills"]:
        versions={v["version"]:v for v in skill["versions"]}
        assert len(versions)==len(skill["versions"]),"DUPLICATE_SKILL_VERSION"
        for version in skill["versions"]:
            assert version["change_id"] in ids,"OPEN_SPEC_CHANGE_REQUIRED"
            assert version["parent_version"] != version["version"],"SELF_PARENT_DENIED"
            assert version["parent_version"] is None or version["parent_version"] in versions,"UNKNOWN_PARENT"
            assert not version["accepted_by_ron"],"UNAUTHORIZED_ACCEPTANCE"
            if version["status"]=="PROPOSED_UNVERIFIED":
                assert version["verifier_run"] is None,"UNVERIFIED_RUN_INVALID"
    from lineage_validation import validate as validate_genealogy
    qualified=validate_genealogy(changes,skill_lineage,browseros,skillstore)
    assert qualified["status"]=="PASS_STAGING",qualified
    gate=json.loads(read("gate_state.json"))
    spec=read("openspec/specs/browser-intelligence/spec.md")
    tests=re.findall(r"^### Requirement: R([1-9]) ([^\n]+)",spec,re.M)
    assert [int(x[0]) for x in tests]==list(range(1,10)), "9 OPENSPEC REQUIREMENTS REQUIRED"
    model=read("likec4/browser-intelligence.c4")
    assert all("C"+str(i)+":" in model for i in range(1,10))
    sha=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    evidence_url="https://github.com/"+REPO+"/actions/runs/"+str(RUN)
    values=[{"id":"C"+str(i),"requirement":"R"+str(i),"title":LABELS[i-1],
             "state":STATES[i-1],"scenario":tests[i-1][1],"evidence":PROOFS[i-1],
             "component":UPSTREAM[i-1],"source_url":evidence_url,
             "accepted":False,
             "lineage":{"parent":"C"+str(i-1) if i>1 else None,"kind":"DESIGN_RELATION_ONLY",
                         "version":"candidate-0.1.0"}} for i in range(1,10)]
    return {"product":"RON-SHO Control Console","commit":sha,"environment":"GITHUB_STAGING",
       "source_run":RUN,"verified_current_run":False,"synthetic_browser_clients":48,
       "real_model_agents":0,"live_sessions":None,"production_accepted":False,
       "gate5":"HOLD","drive_folder":"https://drive.google.com/drive/folders/1hK3uifKYpbQqO1ekzmhFtQ1zP2a1exDf",
       "github_actions":"https://github.com/"+REPO+"/actions",
       "archify_artifact":evidence_url+"/artifacts/12664337823",
       "actors_receipt":evidence_url+"/artifacts/12664957943",
       "memory_receipt":evidence_url+"/artifacts/12664583708",
       "code_folder":"https://github.com/"+REPO+"/tree/"+BRANCH+"/sandbox/upstream-browser-skill-farm-20261026",
       "requirements":values,"gate_states":{k:v["state"] for k,v in gate["gates"].items()},
       "canonical_work_id":gate["work_id"],"canonical_asset_id":gate["asset_ref"],
       "design_edges":[["C1","C2"],["C2","C3"],["C3","C4"],["C4","C5"],["C5","C6"],
                       ["C6","C8"],["C7","C2"],["C8","C9"]],
       "openspec_history":changes["changes"],"skill_genealogy":skill_lineage["skills"],
       "browseros_adapter":browseros,"ronskillstore_adapter":skillstore}
def render(data):
    raw=json.dumps(data,ensure_ascii=False).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    page=r'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RON-SHO | Unified Control Console</title>
<style>
:root{--base:#07101b;--panel:#111e2c;--edge:#263b4c;--txt:#e5edf5;--muted:#91aabd;--aqua:#50d5c5;--gold:#f1b96a}
*{box-sizing:border-box}body{margin:0;background:var(--base);color:var(--txt);font:15px/1.5 system-ui,-apple-system,Arial}
.shell{display:flex;min-height:100vh}.side{width:235px;background:#0b1724;border-right:1px solid var(--edge);padding:25px 18px}
.brand{font-weight:850;font-size:20px;letter-spacing:.02em}.kicker{font-size:11px;letter-spacing:.13em;color:var(--aqua);text-transform:uppercase}
.sidebar-caption{font-size:12px;color:var(--muted);margin:8px 0 28px}
.nav{background:none;border:0;color:var(--muted);cursor:pointer;text-align:left;width:100%;border-radius:10px;padding:12px 14px;margin-bottom:5px;font:inherit}
.nav:hover,.nav.selected{background:#1a3041;color:#eafffd}.nav.selected{border-left:3px solid var(--aqua)}
.main{flex:1;min-width:0;padding:30px;max-width:1500px;margin:auto}
h1{font-size:27px;margin:4px 0 7px}h2{font-size:17px;margin:0 0 17px}.subtitle{color:var(--muted)}
.warning{border:1px solid #765c36;background:#302719;padding:11px 15px;border-radius:10px;color:#ffdb9e;margin:22px 0}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px}.card{background:var(--panel);border:1px solid var(--edge);border-radius:13px;padding:18px}.metric{font-size:31px;font-weight:750;margin:5px 0}.hint,.foot{color:var(--muted);font-size:12px}
.grid2{display:grid;grid-template-columns:1.15fr .85fr;gap:14px;margin-top:15px}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:11px 9px;border-bottom:1px solid var(--edge);font-size:13px}th{color:var(--muted);font-weight:600}.status{font-size:11px;color:#f2cd95}.pass{color:#83ebd4}
button,a{touch-action:manipulation}a{color:#86decf;text-decoration:none}a:hover{text-decoration:underline}
.pill{display:inline-block;padding:4px 9px;border-radius:20px;background:#253c4e;color:#d9eeed;font-size:12px}
.section{display:none}.section.active{display:block}.nodegrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.node{cursor:pointer;text-align:left;color:var(--txt);width:100%}
.node:hover,.node.active{border-color:var(--aqua)}.node .num{color:var(--aqua);font-size:12px}
.details{margin-top:15px}.edge{text-align:center;color:var(--muted)}.specs{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.7 ui-monospace,SFMono-Regular,monospace;background:#0c1b29;padding:16px;border-radius:10px}
footer{margin-top:38px;font-size:11px;color:var(--muted);border-top:1px solid var(--edge);padding-top:15px}
@media(max-width:860px){.side{width:74px;padding:20px 10px}.brand{font-size:12px}.sidebar-caption,.nav-word{display:none}.main{padding:16px}.grid2{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}.nodegrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.nodegrid{grid-template-columns:1fr}.metrics{grid-template-columns:1fr 1fr}.card{padding:13px}}
</style></head>
<body><div class="shell"><aside class="side">
<div class="kicker">Single Control Surface</div><div class="brand">RON-SHO</div><div class="sidebar-caption">Browser Intelligence · Staging</div>
<button class="nav selected" data-view="overview"><span class="nav-word">01 · Tổng quan</span><span class="mobile-ico">▦</span></button>
<button class="nav" data-view="sessions"><span class="nav-word">02 · Browser & AI</span><span class="mobile-ico">◎</span></button>
<button class="nav" data-view="lineage"><span class="nav-word">03 · Phả hệ năng lực</span><span class="mobile-ico">◇</span></button>
<button class="nav" data-view="governance"><span class="nav-word">04 · OpenSpec & 5 Gates</span><span class="mobile-ico">◈</span></button>
<button class="nav" data-view="evidence"><span class="nav-word">05 · Evidence & Runbook</span><span class="mobile-ico">▤</span></button>
</aside><main class="main">
<header><div class="kicker">RON-SHO Unified Control Console · Evidence-backed preview</div>
<h1 id="page-title">Trung tâm điều hành</h1><div class="subtitle">Một bề mặt quan sát BrowserOS · OpenSpec · Archify/LikeC4 · RonSkillStore · 5 Gates</div></header>
<div class="warning" role="status">BẢN GITHUB STAGING — không kết nối BrowserOS runtime, không có AI online thật. 48 là MCP clients + actor thử nghiệm từ lượt CI lịch sử, không phải 48 mô hình AI.</div>
<section class="section active" id="overview"><div class="metrics">
<div class="card"><div class="hint">MCP client kiểm thử</div><div class="metric" id="countMcp">48 / 48</div><span class="pass">Historical CI PASS</span></div>
<div class="card"><div class="hint">AI model online xác nhận</div><div class="metric">0</div><span class="hint">Chưa nối live runtime</span></div>
<div class="card"><div class="hint">Năng lực OpenSpec</div><div class="metric" id="countCaps">9 / 9</div><span class="hint">Yêu cầu đã mô hình hóa</span></div>
<div class="card"><div class="hint">Gate vận hành</div><div class="metric" style="color:#f1b96a">HOLD</div><span class="hint">Chờ Ron nghiệm thu G5</span></div>
</div><div class="grid2">
<div class="card"><h2>9 lớp năng lực bắt buộc</h2><table><thead><tr><th>ID</th><th>Năng lực</th><th>Evidence</th></tr></thead><tbody id="summary-table"></tbody></table></div>
<div class="card"><h2>Chuỗi vận hành chung</h2><div class="specs">AI Actor → MCP Session → Browser Monitor
             ↓
      Record / Replay
             ↓
      Independent Verify
             ↓
OpenSpec Skill Candidate
             ↓
RonSkillStore + PolicyGate
             ↓
Skill Memory / Cache / AI reuse
             ↓
Capability Lineage → 5 Gates</div><p class="hint">Đây là luồng dự kiến được ánh xạ từ OpenSpec; không đồng nghĩa với dịch vụ đã triển khai.</p></div>
</div></section>
<section class="section" id="sessions"><div class="card"><h2>BrowserOS adapter — trạng thái</h2>
<p><span class="pill" id="browseros-status">NOT CONNECTED</span> BrowserOS chưa được đưa vào runtime điều hành. Không có live session stream hay cookie.</p>
<p class="hint" id="browseros-contract"></p>
<p><b>RonSkillStore:</b> <span class="pill" id="skillstore-status">NOT CONNECTED</span>. Không có quyền publish hoặc gọi PolicyGate từ dashboard.</p>
<p class="hint" id="skillstore-contract"></p>
<p><b>MCP UAT:</b> 48 client riêng biệt, kiểm tra cookie isolation; test thuộc GitHub hosted-runner và đã kết thúc.</p>
<p><a id="sessionsLink" target="_blank" rel="noopener noreferrer">Xem receipt 48 phiên và ảnh dashboard →</a></p>
<div class="specs">LIVE_AGENTS = 0 confirmed
LIVE_BROWSER_SESSIONS = UNKNOWN
HISTORICAL_MCP_CLIENTS = 48
CREDENTIALS_VISIBLE = NEVER</div>
</div></section>
<section class="section" id="lineage"><div class="card"><h2>Cây phả hệ — OpenSpec → Skill Version → Verify → 5 Gates</h2>
<p class="hint">Chọn từng nút để xem requirement, nguồn tích hợp, test và trạng thái. Các cạnh thiết kế KHÔNG được đánh đồng với quan hệ kế thừa/version phả hệ đã xác minh.</p>
<div class="nodegrid" id="node-list"></div><div class="details card" id="cap-detail" aria-live="polite">Chọn một năng lực.</div>
<div class="card" style="margin-top:14px"><h2>Phả hệ phiên bản từ OpenSpec (có source)</h2>
<p class="hint">Các version ví dụ được gắn run lịch sử. Không thay thế canonical RonSkillStore hoặc xác nhận một AI thật đã tự học.</p>
<div id="genealogy-list" aria-label="Skill version lineage"></div></div></div></section>
<section class="section" id="governance"><div class="grid2">
<div class="card"><h2>Universal 5 Gates</h2><table id="gate-table"></table><p class="hint">G4 PASS hiện chỉ xác minh dossier cùng SHA; không chứng nhận 9 chức năng production.</p></div>
<div class="card"><h2>OpenSpec as lineage ledger</h2><p>Yêu cầu R1–R9 đã liên kết C1–C9. Mỗi cải tiến phải có version, cha/con, source commit, scenario và receipt trước khi đưa vào SkillStore.</p><div class="specs">OBSERVED → CANDIDATE → VERIFIED_STAGING
          ↓ Ron/PolicyGate
ACCEPTED (NOT YET)
          ↓
SKILL VERSION / CAPABILITY TREE</div>
<p><a id="specLink" target="_blank" rel="noopener noreferrer">Xem OpenSpec trên GitHub →</a></p>
</div></div></section>
<section class="section" id="evidence"><div class="card"><h2>Nguồn bằng chứng và vận hành</h2>
<p><a id="evidenceLink" target="_blank" rel="noopener noreferrer">Run kiểm thử Browser UAT →</a></p>
<p><a id="archifyLink" target="_blank" rel="noopener noreferrer">Archify HTML & Source Graph artifact →</a></p>
<p><a id="memoryLink" target="_blank" rel="noopener noreferrer">FTS5 / Replay / Shared Memory artifact →</a></p>
<p><a id="driveLink" target="_blank" rel="noopener noreferrer">Google Drive — Hồ sơ 5 Gates và 2 runbook →</a></p>
<p><a id="actionsLink" target="_blank" rel="noopener noreferrer">GitHub Actions — Xác minh lại dossier →</a></p>
<p class="hint">Các artifact GitHub có thời hạn lưu trữ; trạng thái stale hoặc hết hạn phải hiện UNKNOWN, không được hiển thị như dữ liệu thời gian thực.</p></div></section>
<footer id="revision-footer"></footer></main></div>
<script id="snapshot" type="application/json">__SNAPSHOT__</script><script>
"use strict";
const d=JSON.parse(document.querySelector("#snapshot").textContent);
const el=id=>document.getElementById(id);
function make(tag,txt,cls){const e=document.createElement(tag);if(txt!==undefined)e.textContent=txt;if(cls)e.className=cls;return e}
function link(id,url){const a=el(id);a.href=url}
const pageTitles={overview:"Trung tâm điều hành",sessions:"Browser & AI",lineage:"Phả hệ năng lực",governance:"OpenSpec & 5 Gates",evidence:"Evidence & Runbook"};
document.querySelectorAll(".nav").forEach(b=>b.addEventListener("click",()=>{
  document.querySelectorAll(".nav").forEach(n=>n.classList.remove("selected"));
  document.querySelectorAll(".section").forEach(s=>s.classList.remove("active"));
  b.classList.add("selected");const name=b.dataset.view;el(name).classList.add("active");
  el("page-title").textContent=pageTitles[name];
}));
const summary=el("summary-table");
d.requirements.forEach(r=>{
  const row=make("tr");row.append(make("td",r.id),make("td",r.title));
  row.append(make("td",r.state.includes("PARTIAL")?"Một phần":"Đã kiểm thử",r.state.includes("PARTIAL")?"status":"pass"));
  summary.append(row);
});
const cards=el("node-list"),details=el("cap-detail");
function selectCap(r){
  document.querySelectorAll(".node").forEach(n=>n.classList.toggle("active",n.dataset.cap===r.id));
  details.replaceChildren();
  const h=make("h2",r.id+" · "+r.title);details.append(h);
  [["OpenSpec",r.requirement+" — "+r.scenario],["Triển khai",r.component],
    ["Evidence",r.evidence],["Trạng thái",r.state],["Version",r.lineage.version],
    ["Quan hệ",r.lineage.kind+"; parent "+(r.lineage.parent??"none")],
    ["Ron ACCEPTED","NO"]].forEach(([k,v])=>{const p=make("p");p.append(make("strong",k+": "),document.createTextNode(v));details.append(p)});
  const a=make("a","Mở bằng chứng GitHub →");a.href=r.source_url;a.target="_blank";a.rel="noopener noreferrer";details.append(a);
}
d.requirements.forEach(r=>{const button=make("button",undefined,"node card");button.dataset.cap=r.id;
  button.append(make("div",r.id+" · "+r.requirement,"num"),make("b",r.title),make("p",r.state,"hint"));
  button.addEventListener("click",()=>selectCap(r));cards.append(button);});
selectCap(d.requirements[0]);
// Skill ancestry is built from versioned OpenSpec change records, never from design edges.
const changes=new Map(d.openspec_history.map(c=>[c.change_id,c]));
for(const skill of d.skill_genealogy){
  const box=make("div",undefined,"card");box.style.marginTop="10px";
  box.append(make("b",skill.skill_ref));
  for(const ver of skill.versions){
    const change=changes.get(ver.change_id);
    if(!change)throw Error("missing change");
    const row=make("div",undefined,"card");row.style.marginTop="8px";
    row.append(make("div",ver.version+" · "+ver.status,ver.status.includes("UNVERIFIED")?"status":"pass"));
    row.append(make("p","OpenSpec: "+change.change_id+" · "+change.spec_requirement+" · "+change.title,"hint"));
    row.append(make("p","Parent: "+(ver.parent_version??"ROOT")+" | Verifier: "+(ver.verifier_run??"NOT VERIFIED")+" | "+ver.gate,"hint"));
    row.append(make("p","Ron accepted: "+String(ver.accepted_by_ron).toUpperCase(),"hint"));
    if(ver.source){
      const link=make("a","Verifier evidence →");
      link.href=ver.source;link.target="_blank";link.rel="noopener noreferrer";
      row.append(link);
    }
    box.append(row);
  }
  el("genealogy-list").append(box);
}
el("browseros-status").textContent=d.browseros_adapter.mode;
el("skillstore-status").textContent=d.ronskillstore_adapter.mode;
el("browseros-contract").textContent="BrowserOS: "+d.browseros_adapter.runtime_status+" · Host: "+d.browseros_adapter.host;
el("skillstore-contract").textContent="RonSkillStore: "+d.ronskillstore_adapter.runtime_status+" · Canonical registry endpoint: UNKNOWN";
for(const [name,state] of Object.entries(d.gate_states)){
  const row=make("tr");row.append(make("td",name),make("td",state,state.includes("HOLD")?"status":""));
  el("gate-table").append(row);
}
link("sessionsLink",d.actors_receipt);link("evidenceLink","https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/"+d.source_run);
link("archifyLink",d.archify_artifact);link("memoryLink",d.memory_receipt);link("driveLink",d.drive_folder);link("actionsLink",d.github_actions);
link("specLink",d.code_folder+"/five-gates/openspec/specs/browser-intelligence/spec.md");
el("revision-footer").textContent="Snapshot from GitHub commit "+d.commit+" · NOT LIVE · G5 HOLD · AIOS production authority NOT granted";
</script></body></html>'''
    return page.replace("__SNAPSHOT__",raw)
def main():
    data=get_data();OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"snapshot.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf8")
    page=render(data)
    assert "__SNAPSHOT__" not in page
    (OUT/"index.html").write_text(page,encoding="utf8")
    print("RON_UNIFIED_CONSOLE_SNAPSHOT_BUILT",data["commit"],len(data["requirements"]))
if __name__=="__main__":main()
