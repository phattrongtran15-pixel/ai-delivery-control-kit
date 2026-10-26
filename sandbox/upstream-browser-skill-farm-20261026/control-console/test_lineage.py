"""Twelve fail-closed regressions on disposable in-memory copies of adapters/lineage."""
import copy,json,sys
from pathlib import Path
from lineage_validation import validate
root=Path(__file__).parent
src=[json.loads((root/p).read_text()) for p in
     ("lineage/openspec_changes.json","lineage/skill_versions.json","adapters/browseros.json","adapters/ronskillstore.json")]
assert validate(*src)["status"]=="PASS_STAGING"
out=[]
def case(name,idx,mutate,expected):
    test=copy.deepcopy(src);mutate(test[idx])
    x=validate(*test)
    assert x["status"]=="BLOCKED" and expected in x["errors"],(name,x)
    out.append({"case":name,"result":"REJECTED_AS_EXPECTED"})
case("FAKE_BROWSEROS_ONLINE",2,lambda d:d.update(mode="CONNECTED"),"UNATTESTED_ONLINE_CLAIM")
case("FAKE_SKILLSTORE_ONLINE",3,lambda d:d.update(mode="CONNECTED"),"UNATTESTED_ONLINE_CLAIM")
case("MISSING_ATTESTATION",2,lambda d:d.update(live_runtime_attestation=True),"ATTESTATION_INVALID")
case("FORCE_PUBLISH",3,lambda d:d.update(can_publish=True),"UNAUTHORIZED_STORE_WRITE")
case("FORCE_WRITE",3,lambda d:d.update(can_write=True),"UNAUTHORIZED_STORE_WRITE")
case("FAKE_POLICYGATE",3,lambda d:d.update(policygate_connected=True),"UNAUTHORIZED_STORE_WRITE")
case("FAKE_ACCEPTED",1,lambda d:d["skills"][0]["versions"][0].update(accepted_by_ron=True),"UNAUTHORIZED_ACCEPTANCE")
case("BROKEN_PARENT",1,lambda d:d["skills"][0]["versions"][1].update(parent_version="does-not-exist"),"MISSING_VERSION_PARENT")
case("CYCLE",1,lambda d:d["skills"][0]["versions"][0].update(parent_version="0.1.1-candidate"),"ANCESTRY_CYCLE")
case("UNKNOWN_REQUIREMENT",0,lambda d:d["changes"][0].update(spec_requirement="R99"),"REQUIREMENT_MISSING")
case("NO_CHANGE_LINK",1,lambda d:d["skills"][0]["versions"][1].update(change_id="nonexistent"),"UNLINKED_OPEN_SPEC_CHANGE")
case("FAKE_RECEIPT",1,lambda d:d["skills"][0]["versions"][1].update(verifier_run=123),"UNVERIFIED_HAS_RECEIPT")
print("RON_CONSOLE_LINEAGE_NEGATIVE_12_OF_12_PASS",json.dumps(out))
