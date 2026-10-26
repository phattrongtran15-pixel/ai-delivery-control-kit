#!/usr/bin/env python3
"""At least ten fail-closed negative tests; each mutation happens in /tmp copy."""
import json,shutil,sys,tempfile
from pathlib import Path
from validate_dossier import validate
def cases(root):
    assert validate(root)["status"]=="PASS_CANDIDATE",validate(root)
    checks=[]
    def run(label,mutate,expected):
        with tempfile.TemporaryDirectory() as temp:
            d=Path(temp)/"d";shutil.copytree(root,d);mutate(d)
            result=validate(d)
            assert result["status"]=="BLOCKED" and any(expected in e for e in result["errors"]),(label,result)
            checks.append({"case":label,"status":"REJECTED_AS_EXPECTED"})
    def state(d,fn):
        p=d/"gate_state.json";j=json.loads(p.read_text());fn(j);p.write_text(json.dumps(j))
    run("FAKE_G5",lambda d:state(d,lambda s:s.update(accepted=True)),"FALSE_ACCEPTANCE")
    run("FAKE_POLICYGATE",lambda d:state(d,lambda s:s.update(policygate_bound=True)),"FALSE_ACCEPTANCE")
    run("FAKE_WORK_ID",lambda d:state(d,lambda s:s.update(work_id="FAKE")),"UNVERIFIED_ID")
    run("FAKE_ASSET_ID",lambda d:state(d,lambda s:s.update(asset_ref="FAKE")),"UNVERIFIED_ID")
    run("SKIP_G3",lambda d:state(d,lambda s:s["gates"].pop("G3")),"FIVE_GATES_MISMATCH")
    run("AUTO_ADVANCE",lambda d:state(d,lambda s:s["gates"]["G5"].update(state="ACCEPTED")),"GATE_TRANSITION_UNAUTHORIZED")
    run("BAD_SHA",lambda d:state(d,lambda s:s.update(source_evidence_commit="0")),"BAD_SOURCE_SHA")
    run("MISSING_SPEC",lambda d:(d/"openspec/specs/browser-intelligence/spec.md").unlink(),"FILE_INVALID")
    run("MISSING_C9",lambda d:(d/"likec4/browser-intelligence.c4").write_text((d/"likec4/browser-intelligence.c4").read_text().replace("C9: Capability Growth Tree","Tree")),"LIKEC4_NOT_NINE")
    run("DUPLICATE_R9",lambda d:(d/"openspec/specs/browser-intelligence/spec.md").write_text((d/"openspec/specs/browser-intelligence/spec.md").read_text()+"\n### Requirement: R9 Duplicate\nSHALL\n#### Scenario: Duplicate\n"),"REQUIREMENTS_NOT_NINE")
    run("NO_AI_RUNBOOK",lambda d:(d/"RUNBOOK_AI.md").unlink(),"FILE_INVALID")
    run("NO_ROLLBACK",lambda d:(d/"RUNBOOK.md").write_text((d/"RUNBOOK.md").read_text().replace("Rollback","Recovery").replace("rollback","recovery")),"ROLLBACK_MISSING")
    return {"negative_cases":len(checks),"results":checks,"status":"PASS"}
if __name__=="__main__":
    root=Path(sys.argv[1]);out=Path(sys.argv[2]);result=cases(root)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("RON_FIVE_GATES_FAIL_CLOSED_12_OF_12_PASS")
