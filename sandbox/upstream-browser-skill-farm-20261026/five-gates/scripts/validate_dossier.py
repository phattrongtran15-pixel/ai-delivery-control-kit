#!/usr/bin/env python3
"""Read-only RON-SHO candidate dossier validator. NEVER advances canonical gates."""
import argparse,hashlib,json,os,re,subprocess,sys
from pathlib import Path
LIVING=["README.md","SPEC.md","KE_HOACH.md","EVIDENCE.md","RUNBOOK.md","CHANGELOG.md"]
OTHER=["RUNBOOK_HUMAN.md","RUNBOOK_AI.md","gate_state.json","openspec/specs/browser-intelligence/spec.md","likec4/browser-intelligence.c4"]
EXPECTED={"G1":"DOCUMENTED_CANDIDATE","G2":"DESIGNED_CANDIDATE","G3":"BUILT_STAGING","G4":"VERIFY_INDEPENDENT_CURRENT_SHA_PENDING","G5":"HOLD_OWNER_ACCEPTANCE"}
def validate(root):
    errors=[]; hashes={}
    for rel in LIVING+OTHER:
        try:
            p=(root/rel).resolve(strict=True)
            if root.resolve() not in p.parents or not p.is_file():raise ValueError("ESCAPED_ROOT")
            data=p.read_bytes();data.decode("utf-8")
            if len(data)<20:raise ValueError("EMPTY_FILE")
            hashes[rel]=hashlib.sha256(data).hexdigest()
        except (OSError,ValueError,UnicodeError) as e:errors.append("FILE_INVALID:"+rel+":"+str(e))
    if len(hashes)!=11:return {"status":"BLOCKED","errors":errors,"hashes":hashes}
    def read(name):return (root/name).read_text(encoding="utf8")
    try:s=json.loads(read("gate_state.json"))
    except json.JSONDecodeError:
        return {"status":"BLOCKED","errors":["INVALID_JSON"],"hashes":hashes}
    if s.get("asset_type")!="PRODUCT" or s.get("owner")!="Ron":errors.append("OWNER_OR_TYPE")
    if s.get("asset_ref") is not None or s.get("work_id") is not None:errors.append("UNVERIFIED_ID")
    if s.get("authority")!="STAGING_DOCUMENTATION_ONLY":errors.append("AUTHORITY_ESCALATION")
    for field in ("accepted","canonical_registry_bound","policygate_bound","successor_ack","production_runtime_verified"):
        if s.get(field) is not False:errors.append("FALSE_ACCEPTANCE:"+field)
    g=s.get("gates",{})
    if set(g)!=set(EXPECTED):errors.append("FIVE_GATES_MISMATCH")
    for key,value in EXPECTED.items():
        if g.get(key,{}).get("state")!=value:errors.append("GATE_TRANSITION_UNAUTHORIZED:"+key)
    if not re.fullmatch("[0-9a-f]{40}",s.get("source_evidence_commit","")):errors.append("BAD_SOURCE_SHA")
    if s.get("historical_run_id")!=40354279483:errors.append("UNSUPPORTED_HISTORICAL_RUN")
    spec=read("openspec/specs/browser-intelligence/spec.md")
    nums=[int(x) for x in re.findall(r"^### Requirement: R([0-9]+)\b",spec,re.M)]
    if sorted(nums)!=list(range(1,10)):errors.append("REQUIREMENTS_NOT_NINE_UNIQUE")
    if len(re.findall(r"^#### Scenario:",spec,re.M))!=9:errors.append("MISSING_SCENARIO")
    if any("SHALL" not in part.split("#### Scenario:")[0] for part in re.split(r"(?=^### Requirement: R\d+\b)",spec,flags=re.M)[1:]):
        errors.append("MISSING_SHALL")
    c4=read("likec4/browser-intelligence.c4")
    elems=[int(x) for x in re.findall(r"\bC([1-9]):",c4)]
    if sorted(elems)!=list(range(1,10)):errors.append("LIKEC4_NOT_NINE_UNIQUE")
    for section in ("specification {","model {","views {","view index {"):
        if section not in c4:errors.append("LIKEC4_MISSING_SECTION")
    trace=read("SPEC.md")
    ids=[int(x) for x in re.findall(r"^\|\s*C([1-9])\s*\|",trace,re.M)]
    if sorted(ids)!=list(range(1,10)):errors.append("TRACE_NOT_NINE_UNIQUE")
    if any("R"+str(n)+" " not in trace for n in range(1,10)):errors.append("OPENSPEC_MAPPING_MISSING")
    if "rollback" not in read("RUNBOOK.md").lower() or "rollback" not in read("KE_HOACH.md").lower():
        errors.append("ROLLBACK_MISSING")
    if "gh workflow run" not in read("RUNBOOK_HUMAN.md"):errors.append("HUMAN_RUNBOOK_NOT_EXECUTABLE")
    if "validate_dossier.py" not in read("RUNBOOK_AI.md"):errors.append("AI_RUNBOOK_NOT_EXECUTABLE")
    return {"status":"PASS_CANDIDATE" if not errors else "BLOCKED","errors":errors,"hashes":hashes,
      "gate_verdict":{"G1":"DOCUMENTED_UNREGISTERED","G2":"DESIGNED_CANDIDATE","G3":"BUILT_STAGING","G4":"PENDING_INDEPENDENT_JOB","G5":"HOLD"},
      "ron_accepted":False,"scope":"candidate file integrity only; NOT production gate API"}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);p.add_argument("--report",type=Path,required=True);a=p.parse_args()
    result=validate(a.root)
    try:rev=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    except Exception:rev="UNKNOWN"
    result.update(source_sha=rev,run_id=os.environ.get("GITHUB_RUN_ID","LOCAL"))
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="hashes"}))
    sys.exit(0 if result["status"]=="PASS_CANDIDATE" else 2)
