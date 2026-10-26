"""Fail-closed OpenSpec change → skill-version genealogy validator. No registry writes."""
def validate(changes, lineage, browseros, store):
    errors=[]
    if changes.get("canonical_change_registry") is not False or lineage.get("canonical_store") is not False:
        errors.append("NOT_STAGING")
    cset=set();requirements={f"R{x}" for x in range(1,10)}
    for c in changes.get("changes",[]):
        if c.get("change_id") in cset or not c.get("change_id"):errors.append("DUPLICATE_CHANGE")
        cset.add(c.get("change_id"))
        if c.get("spec_requirement") not in requirements:errors.append("REQUIREMENT_MISSING")
        if c.get("production_authority") is not False:errors.append("UNAUTHORIZED_CHANGE_APPROVAL")
    if not cset:errors.append("NO_CHANGES")
    seen_skills=set()
    for skill in lineage.get("skills",[]):
        identity=skill.get("skill_ref")
        if not identity or identity in seen_skills:errors.append("DUPLICATE_SKILL_ID")
        seen_skills.add(identity)
        versions={v.get("version"):v for v in skill.get("versions",[])}
        if len(versions)!=len(skill.get("versions",[])):errors.append("DUPLICATE_SKILL_VERSION")
        for v in skill.get("versions",[]):
            if v.get("change_id") not in cset:errors.append("UNLINKED_OPEN_SPEC_CHANGE")
            if v.get("accepted_by_ron") is not False:errors.append("UNAUTHORIZED_ACCEPTANCE")
            if v.get("parent_version") is not None and v.get("parent_version") not in versions:
                errors.append("MISSING_VERSION_PARENT")
            if v.get("status")=="PROPOSED_UNVERIFIED" and v.get("verifier_run") is not None:
                errors.append("UNVERIFIED_HAS_RECEIPT")
            if v.get("status")=="STAGING_VERIFIED" and not (v.get("verifier_run") and v.get("source")):
                errors.append("VERIFIER_EVIDENCE_MISSING")
        for vid in versions:
            visited=set();step=vid
            while step is not None:
                if step in visited:errors.append("ANCESTRY_CYCLE");break
                visited.add(step)
                node=versions.get(step)
                if not node:break
                step=node.get("parent_version")
    for src in (browseros,store):
        if src.get("mode")!="DISCONNECTED" or src.get("runtime_status")!="BLOCKED_NOT_CONNECTED":
            errors.append("UNATTESTED_ONLINE_CLAIM")
        if src.get("live_runtime_attestation") is not False:errors.append("ATTESTATION_INVALID")
    if store.get("can_write") is not False or store.get("can_publish") is not False or store.get("policygate_connected") is not False:
        errors.append("UNAUTHORIZED_STORE_WRITE")
    return {"status":"PASS_STAGING" if not errors else "BLOCKED","errors":sorted(set(errors)),
            "change_count":len(cset),"skill_count":len(seen_skills)}
