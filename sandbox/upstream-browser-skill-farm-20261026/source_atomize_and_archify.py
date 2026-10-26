#!/usr/bin/env python3
"""REA/Archify methodology on authorized RON-SHO source: 9 source-backed atoms,
line-hash evidence graph and native Archify workflow candidate.
No REA CLI/Ghidra invoked; no production PolicyGate or binary analyzed.
"""
import ast
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd().resolve()
BASE = Path("sandbox/upstream-browser-skill-farm-20261026")
OUT = Path("evidence/source-graph")
OUT.mkdir(parents=True, exist_ok=True)
REVISION = subprocess.check_output(["git","rev-parse","HEAD"], text=True).strip()
assert re.fullmatch(r"[a-f0-9]{40}", REVISION)
URL = "https://github.com/phattrongtran15-pixel/ai-delivery-control-kit"
read_paths=[
    BASE/"mcp_actor_scale.mjs",
    BASE/"mcp_multiclient.mjs",
    BASE/"skill_memory.py",
    BASE/"browser_memory_uat.py",
    BASE/"capability_farm.py",
    Path(".github/workflows/ron-9-capability-sandbox.yml")
]

def sha(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
def first(path, needle):
    path = Path(path)
    f = (ROOT/path).resolve(strict=True)
    assert ROOT in f.parents and f.is_file(), "INVALID_CITED_PATH"
    lines = f.read_text(encoding="utf-8").splitlines()
    positions=[i+1 for i,line in enumerate(lines) if needle in line]
    if not positions:raise AssertionError("MISSING_SOURCE_ANCHOR:"+str(path)+":"+needle)
    n = positions[0]
    return {"path":path.as_posix(),"start":n,"end":n,"sha256":sha(lines[n-1])}

# Real code anchors; stages with absent implementation are explicitly not SOURCE_SUPPORTED.
specs=[
 ("monitor","Browser multi-actor monitoring", read_paths[0],
  "ledger.push({actor", "Every session produces a monitored verified row",
  "new actor event", "actor,phase,status,elapsed_ms", "ephemeral ledger", "MCP navigation",
  "valid HTTP actor session", "ron-mcp-actor-farm-6-12-24"),
 ("mcp","Isolated multi-client MCP", read_paths[0],
  "new StreamableHTTPClientTransport(transportURL)", "One independent protocol client per actor",
  "connect actor", "MCP transport client", "session membership", "Playwright MCP",
  "cookie A/B and post-fanout readback", "ron-mcp-actor-farm-6-12-24"),
 ("learn","Propose procedural skill", read_paths[2],
  "def propose(db,", "A verified observer may propose a candidate skill only",
  "new observed action", "candidate id and trace hash", "PROPOSED", "browser action evidence",
  "no credentials, allowed fixture/actor", "ron-procedural-skill-memory"),
 ("verify","Independent outcome verification", read_paths[2],
  "def verify(db,", "A separate verifier gates untrusted browser result",
  "candidate submitted", "outcome + verifier hash", "VERIFIED_STAGING or FAILED", "HTTP fixture receipt",
  "must not self-verify, positive safe count", "ron-procedural-skill-memory"),
 ("cache","Fingerprint-keyed action cache", read_paths[2],
  "CREATE TABLE IF NOT EXISTS action_cache", "Reuses action selector only on exact site and UI fingerprint",
  "pre-browser lookup", "cached selector", "cache hits, invalidation", "SQLite FTS5 skill lookup",
  "scope and fingerprint match", "ron-procedural-skill-memory"),
 ("search","Cross-process searchable memory", read_paths[2],
  "CREATE VIRTUAL TABLE IF NOT EXISTS skill_index", "FTS5 task index resolves staging-approved skill",
  "search by task", "approved skill metadata", "persistent SQLite within artifact", "search FTS5",
  "status and actor authorization", "ron-procedural-skill-memory"),
 ("automation","GitHub Actions automation", read_paths[5],
  "  scaled-real-mcp-actors:", "CI starts scoped browser and source tests and uploads receipts",
  "push to staging", "GH Actions steps/jobs", "GitHub Actions run/artifacts", "checkout/node/playwright",
  "no secrets, read-only GitHub checkout", "workflow GitHub run"),
 ("sharing","Artifact-based skill sharing", read_paths[5],
  "  independent-memory-consumer:", "A separate runner downloads and reads exported memory",
  "new consumer job", "SQLite artifact/skill hash", "cross-job continuity", "actions/download-artifact",
  "staging-only; no credential sharing", "ron-procedural-skill-memory"),
 ("tree","Capability lineage tree", read_paths[2],
  "growing-capability-tree.json", "Outputs versioned graph from recorded skill lifecycle events",
  "skill event", "nodes/edges/lineage", "versioned JSON export", "SQLite event register",
  "source is staging only", "growing-capability-tree.json")
]
atoms=[]; citations={}
for cap,name,path,needle,purpose,trigger,output,state,deps,guard,test in specs:
    ev=first(path,needle)
    citations[cap]=ev
    atoms.append({"capability_id":"ron.browser."+cap,"purpose":purpose,"trigger":trigger,
      "inputs":"authorized synthetic browser context + versioned state",
      "outputs":output,"state":state,"dependencies":deps,"guards":guard,
      "evidence":[ev],"verification":test,"status":"SOURCE_SUPPORTED",
      "reusability":"Staging candidate only","native_binary_disassembly":"NOT_APPLICABLE"})
# Independent structural inspection; no pretending that regex == decompilation.
python_ast={}
for path in read_paths:
    if path.suffix==".py":
        tree=ast.parse((ROOT/path).read_text(encoding="utf8"), filename=str(path))
        python_ast[str(path)]=[{"function":node.name,"line":node.lineno}
            for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))]
source_file_shas={}
for p in read_paths:
    source_file_shas[p.as_posix()]=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
lineage={
    "scope":"GitHub checked-out authorized source; no native target","source_revision":REVISION,
    "source_file_shas":source_file_shas,"python_ast_functions":python_ast,
    "REA_plugin_methodology":"G1 source scope; G2 source/AST provider; G3 REA CLI NOT RUN (requires real gated worker)",
    "Ghidra_12_1_4":"NOT_APPLICABLE for JS/Python text","REA_G5":"BLOCKED",
    "claims":"SOURCE_SUPPORTED only, not runtime accepted","atoms":atoms}
(OUT/"rea-source-capability-atoms.json").write_text(json.dumps(lineage,indent=2)+"\n",encoding="utf8")

nodes=[{"id":cap,"label":name,"status":"SOURCE_SUPPORTED","evidence":[citations[cap]]}
    for cap,name,*_ in specs]
links=[
 ("monitor","mcp","monitor uses actor-MCP sessions"),
 ("mcp","learn","MCP sessions can produce observations"),
 ("learn","verify","candidate independent readback"),
 ("verify","cache","verified skills qualify for cache"),
 ("verify","search","gate approved lookup"),
 ("search","cache","pre-action cache reuse"),
 ("cache","sharing","cached skill projection to separate agent"),
 ("sharing","tree","events update capability graph"),
 ("automation","mcp","workflow executes MCP test")
]
edges=[{"from":a,"to":b,"label":label,"status":"INFERRED","evidence":[]}
    for a,b,label in links]
graph={"schema_version":"1.0","subject":"RON-SHO 9 capability browser/skill staged architecture",
    "repo_revision":REVISION,"nodes":nodes,"edges":edges}
(OUT/"evidence-graph.json").write_text(json.dumps(graph,indent=2)+"\n",encoding="utf8")

# Native Archify v3.2 WORKFLOW candidate. Source references belong to committed revision.
loc=lambda cap:{"path":citations[cap]["path"],"line":citations[cap]["start"],
                "end_line":citations[cap]["end"]}
workflow={
 "schema_version":2,"diagram_type":"workflow",
 "meta":{"title":"RON-SHO Browser Intelligence | 24 MCP clients",
   "subtitle":"GitHub staging: source-backed flow, not production AIOS",
   "output":"evidence/source-graph/ron-browser-intelligence.html",
   "quality_profile":"standard",
   "repository":{"url":URL,"provider":"github","revision":REVISION}},
 "lanes":[
    {"id":"browser","label":"Browser sessions & monitor"},
    {"id":"control","label":"MCP and workflow control"},
    {"id":"policy","label":"Independent checks","variant":"exception"},
    {"id":"memory","label":"SkillStore candidate memory"}],
 "mainPath":["monitor","mcp","learn","verify","search","cache","sharing"],
 "nodes":[
    {"id":"monitor","lane":"browser","col":0,"type":"frontend","label":"Actor monitor",
      "sublabel":"6 / 12 / 24 MCP clients","sources":[loc("monitor")]},
    {"id":"mcp","lane":"control","col":1,"type":"backend","label":"Isolated MCP",
      "sublabel":"one context per client","sources":[loc("mcp")]},
    {"id":"learn","lane":"control","col":2,"type":"backend","label":"Propose skill",
      "sublabel":"browser trace","sources":[loc("learn")]},
    {"id":"verify","lane":"policy","col":2,"type":"security","label":"Verify outcome",
      "sublabel":"independent receipt","sources":[loc("verify")]},
    {"id":"search","lane":"memory","col":3,"type":"database","label":"FTS5 lookup",
      "sublabel":"approved + scoped","sources":[loc("search")]},
    {"id":"cache","lane":"memory","col":4,"type":"database","label":"Action cache",
      "sublabel":"fingerprint keyed","sources":[loc("cache")]},
    {"id":"sharing","lane":"control","col":5,"type":"messagebus","label":"Job handoff",
      "sublabel":"versioned artifact","sources":[loc("sharing")]},
    {"id":"automation","lane":"control","col":0,"type":"backend","label":"GitHub Actions",
      "sublabel":"ephemeral runner","sources":[loc("automation")]},
    {"id":"tree","lane":"memory","col":5,"type":"frontend","label":"Capability DAG",
      "sublabel":"staging lineage","sources":[loc("tree")]}],
 "edges":[
    {"from":"monitor","to":"mcp"},
    {"from":"mcp","to":"learn"},
    {"from":"learn","to":"verify","variant":"security"},
    {"from":"verify","to":"search","variant":"security"},
    {"from":"search","to":"cache"},
    {"from":"cache","to":"sharing"},
    {"from":"automation","to":"mcp","variant":"dashed"},
    {"from":"sharing","to":"tree","variant":"dashed"}],
 "cards":[
    {"dot":"cyan","title":"Physical UAT","items":["6, 12 and 24 real MCP clients with isolated cookies","Actor names represent test clients, not LLM workers"]},
    {"dot":"amber","title":"Authority boundary","items":["Staging skill approvals do not grant Ron/PolicyGate acceptance",
      "REA/Ghidra native runtime not invoked for Python/JS source"]}]
}
(OUT/"workflow-candidate.json").write_text(json.dumps(workflow,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("RON_REA_SOURCE_ATOMIZATION_"+str(len(atoms))+"_PASS")
print("RON_ARCHIFY_SOURCE_WORKFLOW_CANDIDATE_PASS")
