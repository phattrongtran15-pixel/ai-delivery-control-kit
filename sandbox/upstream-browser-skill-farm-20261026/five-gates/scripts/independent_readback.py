#!/usr/bin/env python3
"""Independent GitHub job/implementation. Same-SHA and byte readback, G5 fail closed."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
def independent(root,receipt):
    r=json.loads(Path(receipt).read_text());errs=[]
    sha=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    if sha!=r.get("source_sha"):errs.append("REVISION_MISMATCH")
    for name,expected in r.get("hashes",{}).items():
        p=(root/name).resolve()
        if root.resolve() not in p.parents or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            errs.append("SOURCE_BYTES_MISMATCH:"+name)
    if len(r.get("hashes",{}))!=11:errs.append("INCOMPLETE_MANIFEST")
    s=json.loads((root/"gate_state.json").read_text())
    if any([s.get("accepted") is not False,s.get("work_id") is not None,s.get("asset_ref") is not None,
        s.get("canonical_registry_bound") is not False,s.get("policygate_bound") is not False,
        s.get("gates",{}).get("G5",{}).get("state")!="HOLD_OWNER_ACCEPTANCE"]):
        errs.append("G5_MUST_HOLD")
    spec=(root/"openspec/specs/browser-intelligence/spec.md").read_text()
    graph=(root/"likec4/browser-intelligence.c4").read_text()
    for i in range(1,10):
        if spec.count("### Requirement: R"+str(i)+" ")!=1:errs.append("REQUIREMENT_MISSING:"+str(i))
        if len(re.findall(r"\bC"+str(i)+r":",graph))!=1:errs.append("MODEL_COMPONENT_MISSING:"+str(i))
    if r.get("status")!="PASS_CANDIDATE":errs.append("BUILDER_FAILED")
    return {"status":"G4_DOSSIER_INTEGRITY_PASS" if not errs else "BLOCKED","errors":errs,"source_sha":sha,
        "builder_sha":r.get("source_sha"),"independent_job":True,
        "scope":"documentation integrity only, not 9 real model actors",
        "ron_accepted":False,"G5":"HOLD_OWNER_ACCEPTANCE"}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True)
    p.add_argument("--builder-receipt",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args()
    result=independent(a.root,a.builder_receipt)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result));sys.exit(0 if not result["errors"] else 2)
