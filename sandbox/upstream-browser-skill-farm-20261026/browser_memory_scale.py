"""Scale one independently verified, test-approved skill to 12/24/48 distinct
actor identities via cross-PROCESS SQLite FTS5 retrieval and real isolated browser
contexts. NOT 48 model-backed AI agents; not connected to production SkillStore.
"""
import asyncio
import json
import statistics
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from pathlib import Path

from playwright.async_api import async_playwright
from browser_memory_uat import (
    Fixture, RECEIPT, LOCK, subprocess_lookup, independent_readback
)
from skill_memory import connect, export, sha

OUT=Path("evidence")
OUT.mkdir(exist_ok=True)
DB=(OUT/"stage-memory.sqlite3").resolve()
assert DB.is_file(),"SKILL_MEMORY_SEED_MISSING"
db=connect(DB)
seed=db.execute("SELECT * FROM skills WHERE status='STAGING_APPROVED' LIMIT 1").fetchone()
assert seed and seed["evidence_hash"] and seed["fingerprint"],"SEED_NOT_VERIFIED"

def p95(values):
    ordered=sorted(values)
    return round(ordered[max(0, __import__("math").ceil(len(ordered)*0.95)-1)],1)

async def main():
    server=ThreadingHTTPServer(("127.0.0.1",0),Fixture)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin="http://127.0.0.1:"+str(server.server_port)+"/"
    results=[]
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            try:
                for n in (12,24,48):
                    started=time.perf_counter()
                    with LOCK:
                        RECEIPT["safe_count"]=0
                        RECEIPT["unsafe_count"]=0
                        RECEIPT["actors"]=[]
                    limiter=asyncio.Semaphore(8)
                    timings=[]
                    outputs=[]
                    async def actor_run(i):
                        ident="actor-"+str(i).zfill(2)
                        async with limiter:
                            c=await browser.new_context()
                            try:
                                await c.add_cookies([{"name":"actor","value":ident,"url":origin}])
                                page=await c.new_page()
                                await page.goto(origin,wait_until="load",timeout=35000)
                                assert await page.evaluate("document.cookie")=="actor="+ident
                                button_html=await page.locator("#safe").evaluate("(el)=>el.outerHTML")
                                observed_fingerprint=sha({"target_html":button_html,"site":"127.0.0.1"})
                                assert observed_fingerprint==seed["fingerprint"],"UI_FINGERPRINT_CHANGED"
                                begin=time.perf_counter()
                                rec=await asyncio.to_thread(subprocess_lookup,DB,seed["task"],observed_fingerprint,ident)
                                assert rec and rec["skill_id"]==seed["id"],"SKILL_NOT_DISTRIBUTED"
                                assert rec["cache_hit"],"EXPECTED_ALREADY_WARM_CACHE_HIT"
                                assert not await asyncio.to_thread(subprocess_lookup,DB,seed["task"],
                                    "tampered-ui",ident),"UI_DRIFT_NOT_BLOCKED"
                                await page.locator(rec["selector"]).click(timeout=15000)
                                await page.wait_for_function("window.__done === true",timeout=15000)
                                assert await page.evaluate("document.cookie")=="actor="+ident,"CROSS_ACTOR_COOKIE"
                                timings.append((time.perf_counter()-begin)*1000)
                                outputs.append(ident)
                            finally:
                                await c.close()
                    await asyncio.wait_for(asyncio.gather(*(actor_run(i) for i in range(1,n+1))),timeout=190)
                    receipt=independent_readback(origin)
                    assert receipt["safe_count"]==n and receipt["unsafe_count"]==0,receipt
                    assert len(set(outputs))==n,"DUPLICATE_ACTOR"
                    duration=round((time.perf_counter()-started),3)
                    item={"actor_count":n,"successful_actor_browser_runs":n,
                          "unique_actor_ids":n,"independent_python_subprocess_retrieval":True,
                          "browser_context_isolated":True,"all_cache_hits":True,
                          "independent_http_receipt":{"safe_count":n,"unsafe_count":0},
                          "elapsed_seconds":duration,"p95_lookup_and_click_ms":p95(timings),
                          "real_LLM_agents":False,"status":"PASS"}
                    results.append(item)
                    print("RON_SHARED_SKILL_MEMORY_ACTORS_PASS:"+str(n)+" "+json.dumps(item,sort_keys=True),flush=True)
                    if n==48:
                        with LOCK:
                            RECEIPT["actors"]=list(outputs)
                        page=await browser.new_page(viewport={"width":1280,"height":1400})
                        try:
                            await page.goto(origin+"dashboard",wait_until="load")
                            assert await page.locator("tr").count()==49,"MONITOR_48_ACTOR_ROWS_MISMATCH"
                            await page.screenshot(path=str(OUT/"memory-actor-monitor-48.png"),full_page=True)
                            print("RON_MEMORY_MONITOR_48_ACTORS_PASS",flush=True)
                        finally:
                            await page.close()
            finally:
                await browser.close()
    finally:
        server.shutdown()
        server.server_close()
    stats=export(db,OUT)
    assert stats["cache_hits"]>=48,"CACHE_READBACK_MISSING"
    record={"status":"PASS","scale":results,"memory_stats":stats,
            "real_cloud_local_actor_connections":False,
            "persistent_across_jobs_via_GitHub_artifact":True,
            "policygate_production":False,"skillsource":"staging browser observed + independent readback"}
    (OUT/"memory-48-actor-scale.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print("RON_ALL_48_ACTORS_SKILL_REUSE_VERIFIED_STAGING",flush=True)

if __name__=="__main__":
    asyncio.run(main())
