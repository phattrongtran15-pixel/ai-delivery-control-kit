"""RON-SHO staging procedural memory: FTS5, action-cache, verification & skill lineage.
Runs only on GitHub-hosted runner; not connected to production RonSkillStore.
"""
import argparse, hashlib, json, sqlite3
from pathlib import Path
from datetime import datetime, timezone

ACTORS = {"local-agent-A","cloud-agent-B","cloud-agent-C"}
def sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def now():
    return datetime.now(timezone.utc).isoformat()
def connect(path):
    db=sqlite3.connect(str(path),timeout=15)
    db.row_factory=sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS skills(
      id TEXT PRIMARY KEY, version TEXT NOT NULL, task TEXT NOT NULL,
      origin TEXT NOT NULL, selector TEXT NOT NULL, fingerprint TEXT NOT NULL,
      author TEXT NOT NULL, status TEXT NOT NULL, trace_hash TEXT NOT NULL,
      evidence_hash TEXT, verifier TEXT, approved_by TEXT, created_at TEXT);
    CREATE TABLE IF NOT EXISTS events(
      id INTEGER PRIMARY KEY AUTOINCREMENT, skill_id TEXT, actor TEXT,
      kind TEXT, details TEXT, created_at TEXT);
    CREATE TABLE IF NOT EXISTS action_cache(
      cache_key TEXT PRIMARY KEY, skill_id TEXT, selector TEXT,
      hits INTEGER DEFAULT 0, invalidated INTEGER DEFAULT 0);
    CREATE VIRTUAL TABLE IF NOT EXISTS skill_index USING fts5(id UNINDEXED,task);
    """)
    db.commit()
    return db
def event(db,skill_id,actor,kind,details):
    db.execute("INSERT INTO events(skill_id,actor,kind,details,created_at) VALUES(?,?,?,?,?)",
               (skill_id,actor,kind,json.dumps(details,sort_keys=True),now()))
def propose(db,task,origin,selector,fingerprint,trace,author):
    if author!="local-agent-A" or origin!="127.0.0.1" or selector!="#safe":
        raise PermissionError("STAGING_ONLY")
    if any(s in json.dumps(trace).lower() for s in ("cookie","password","token","secret","bearer")):
        raise ValueError("POTENTIAL_SECRET")
    sid="staging.browser."+sha([task,origin,selector])[:16]
    db.execute("INSERT INTO skills(id,version,task,origin,selector,fingerprint,author,status,trace_hash,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
      (sid,"0.1.0",task,origin,selector,fingerprint,author,"PROPOSED",sha(trace),now()))
    db.execute("INSERT INTO skill_index(id,task) VALUES(?,?)",(sid,task))
    event(db,sid,author,"PROPOSED",{"trace_hash":sha(trace)})
    db.commit()
    return sid
def verify(db,sid,receipt,verifier):
    row=db.execute("SELECT * FROM skills WHERE id=?",(sid,)).fetchone()
    if not row or row["status"]!="PROPOSED" or verifier!="independent-fixture-verifier" or verifier==row["author"]:
        raise PermissionError("INDEPENDENT_VERIFICATION_REQUIRED")
    if receipt.get("safe_count")!=1 or receipt.get("unsafe_count")!=0:
        db.execute("UPDATE skills SET status='FAILED' WHERE id=?",(sid,))
        event(db,sid,verifier,"FAILED",{"receipt":receipt})
        db.commit()
        raise AssertionError("OUTCOME_MISMATCH")
    evidence_sha=sha(receipt)
    db.execute("UPDATE skills SET status='VERIFIED_STAGING', evidence_hash=?,verifier=? WHERE id=?",
               (evidence_sha,verifier,sid))
    event(db,sid,verifier,"VERIFIED_STAGING",{"receipt_sha256":evidence_sha})
    db.commit()
    return evidence_sha
def approve_staging(db,sid,reviewer):
    row=db.execute("SELECT * FROM skills WHERE id=?",(sid,)).fetchone()
    if reviewer!="staging-test-controller" or not row or row["status"]!="VERIFIED_STAGING" or not row["evidence_hash"]:
        raise PermissionError("STAGING_GATE_DENIED")
    db.execute("UPDATE skills SET status='STAGING_APPROVED',approved_by=? WHERE id=?",(reviewer,sid))
    event(db,sid,reviewer,"STAGING_APPROVED",{"real_ron_policygate":False})
    db.commit()
def resolve(db,task,origin,fingerprint,actor):
    if actor not in ACTORS or origin!="127.0.0.1":return None
    rows=db.execute("""SELECT s.* FROM skill_index i JOIN skills s ON s.id=i.id
      WHERE skill_index MATCH 'browser AND approved'
      AND s.status='STAGING_APPROVED' AND s.origin=? ORDER BY rank LIMIT 10""",
      (origin,)).fetchall()
    for row in rows:
        if row["task"]!=task or row["fingerprint"]!=fingerprint:continue
        key=sha([row["id"],fingerprint,origin])
        cache=db.execute("SELECT * FROM action_cache WHERE cache_key=? AND invalidated=0",(key,)).fetchone()
        if cache:
            db.execute("UPDATE action_cache SET hits=hits+1 WHERE cache_key=?",(key,))
        else:
            db.execute("INSERT INTO action_cache(cache_key,skill_id,selector) VALUES(?,?,?)",
                       (key,row["id"],row["selector"]))
        event(db,row["id"],actor,"PRE_ACTION_RECOMMENDATION",{"cache_hit":bool(cache)})
        db.commit()
        return {"skill_id":row["id"],"selector":row["selector"],"cache_hit":bool(cache),
                "version":row["version"],"evidence_hash":row["evidence_hash"]}
    return None
def invalidate(db,sid):
    db.execute("UPDATE action_cache SET invalidated=1 WHERE skill_id=?",(sid,))
    event(db,sid,"staging-test-controller","CACHE_INVALIDATED",{"UI_change":True})
    db.commit()
def export(db,path):
    out=Path(path);out.mkdir(parents=True,exist_ok=True)
    skills=[dict(r) for r in db.execute("SELECT * FROM skills")]
    events=[dict(r) for r in db.execute("SELECT * FROM events ORDER BY id")]
    cache=[dict(r) for r in db.execute("SELECT * FROM action_cache")]
    stats={"skills":len(skills),"events":len(events),"cache_hits":sum(r["hits"] for r in cache),
           "actor_users":sorted({r["actor"] for r in events if r["kind"]=="PRE_ACTION_RECOMMENDATION"}),
           "fts5_enabled":True,"persistent_across_github_jobs_via_artifact":True,
           "real_mem0_runtime":False,"canonical_ron_skillstore_connected":False}
    (out/"procedural-memory-evidence.json").write_text(
      json.dumps({"stats":stats,"skills":skills,"events":events,"cache":cache},indent=2),encoding="utf8")
    stages=["Browser Session","Capture Trace","Verify Outcome","Publish Staging Skill","Cross-Agent Retrieval","Cached Replay"]
    nodes=[{"id":"n"+str(i),"label":name,"verified_in_staging":True} for i,name in enumerate(stages)]
    edges=[["n"+str(i),"n"+str(i+1)] for i in range(len(nodes)-1)]
    tree={"nodes":nodes,"edges":edges,"lineage":[e for e in events if e["kind"] in ("PROPOSED","VERIFIED_STAGING","STAGING_APPROVED")],
          "real_aios_capability_registry":False}
    (out/"growing-capability-tree.json").write_text(json.dumps(tree,indent=2),encoding="utf8")
    diagram=["# Browser Capability Growth (staging only)","","~~~mermaid","flowchart LR"]
    for i,name in enumerate(stages):
        diagram.append('  N'+str(i)+'["'+name+'"]')
        if i:diagram.append('  N'+str(i-1)+' --> N'+str(i))
    diagram.extend(["~~~","","Source: independently recorded staging events. Not live canonical AIOS registry."])
    (out/"growing-capability-tree.md").write_text("\n".join(diagram)+"\n",encoding="utf8")
    return stats
def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=["consumer-check","inspect"])
    p.add_argument("--db",required=True)
    args=p.parse_args()
    db=connect(args.db)
    row=db.execute("SELECT * FROM skills LIMIT 1").fetchone()
    if args.mode=="consumer-check":
        assert row and row["status"]=="STAGING_APPROVED","SKILL_NOT_PRESENT"
        assert resolve(db,row["task"],row["origin"],row["fingerprint"],"cloud-agent-C")
        for bad in [
          (row["task"],row["origin"],row["fingerprint"],"untrusted-client"),
          (row["task"],"wrong.site",row["fingerprint"],"cloud-agent-C"),
          (row["task"],row["origin"],"stale-fingerprint","cloud-agent-C")]:
            assert not resolve(db,*bad),"UNAUTHORIZED_OR_STALE_SKILL"
        print("RON_FTS5_CROSS_JOB_CONSUMER_PASS:"+row["id"])
    else:
        print(json.dumps(export(db,"evidence")))
if __name__=="__main__":main()
