# RON-SHO — Actual 9-capability acceptance readback
**Date:** 26 October 2026 | **Source:** GitHub Actions + GitHub repository readback | **Authority:** staging only.
**Direct answer:** **NOT FULL 9/9.** A successful CI run is not full production capability acceptance.

## Source-of-truth evidence
- **Latest successful integration run** [40349665708](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40349665708) — six jobs SUCCESS, source download SKIPPED intentionally to reduce repeated bandwidth; five evidence artifacts. Commit `16267315ce211a188cbb13a0244ae6c363a33518`.
- **11 upstream source downloads** [40342982007](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40342982007) — 11 pinned repo snapshots archived (4 full, 7 sparse/root only); this is **NOT 11 production deployments**.
- **Existing baseline M4** [40019468606](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40019468606) — deterministic browser replay and independent HTTP verifier.
- **Current branch** [sandbox/upstream-browser-skill-farm-20261026](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/tree/sandbox/upstream-browser-skill-farm-20261026). No other implementation branches, no merge to main.

## Nine fixed criteria — staged proof vs full product gap

| # | Non-negotiable capability | Real tested GitHub evidence | Actual status | Required to claim FULL |
|---|---|---|---|---|
| 1 | Browser nhìn thấy/giám sát nhiều AI | Actual browser-rendered monitor screenshot from 3 simulated role-labelled actor contexts; 3/6/10/15 real Chromium context tests | PARTIAL | Run real BrowserOS/monitor with live independent AI agent sessions and observable work/trace |
| 2 | MCP nhiều phiên cô lập | Two real independent Streamable HTTP MCP clients called Playwright MCP navigate/evaluate, cookie A/B isolation pass | STAGING VERIFIED | Connect different real AIOS clients through a governed remote MCP gateway with account isolation |
| 3 | AI học và phát triển kỹ năng | Browser A recorded a successful safe action; proposed a skill, independent fixture verified, staging gate approved | PARTIAL | Actual autonomous skill synthesis/expansion, regression quality and Ron/PolicyGate acceptance |
| 4 | Ghi thao tác, replay, verify | M4 real browser deterministic replay 3/3 plus independent HTTP evidence; browser action trace stored | STAGING VERIFIED (limited) | Rich event/screenshot recording and OpenAdapt replay integration on real sites |
| 5 | Cache thao tác để chạy nhanh | Version/UI fingerprint keyed SQLite action cache, cold resolution vs hit recorded and used to drive action | PARTIAL | Stagehand or equivalent runtime cache with measured p50/p95 speedup and UI-drift fallback |
| 6 | Bộ nhớ tìm kiếm xuyên agent | SQLite FTS5 pre-action discovery across separate Python subprocesses and separate GitHub jobs; integrity and authorization negative tests | STAGING VERIFIED (limited) | Persistent governed Mem0/semantic memory with concurrent real Local/Cloud agents |
| 7 | Automation | GitHub push-triggered Actions pipeline, independent tests and artifact handoff | STAGING VERIFIED (GitHub) | Real n8n workflows or authorized end-to-end event scheduling, retries, idempotency |
| 8 | Share memory | Vercel Skills CLI installed same staging skill to Codex and Kilo test homes (2 copies, hash receipt); artifacts consumed in new job | STAGING VERIFIED (limited) | RonSkillStore canonical projection and actual Local/Cloud actor read/write under PolicyGate |
| 9 | Cây phát triển năng lực | Versioned Mermaid tree, runtime-generated lineage + JSON DAG artifacts | PARTIAL | Live interactive xyflow-backed graph, skill ancestry/metrics and approved registry synchronization |

**Strict final acceptance:** **0/9 FULL** across live RON-SHO AIOS. The staging proofs improve implementation readiness but do not certify production.

## New PASS evidence markers
- `RON_REAL_MCP_TWO_CLIENT_SESSION_ISOLATION_PASS`
- `RON_MEMORY_FTS5_MULTI_ACTOR_PREACTION_PASS`
- `RON_RECORDED_VERIFIED_SKILL_CACHE_HIT_PASS`
- `RON_LIVE_BROWSER_ACTOR_MONITOR_PASS`
- `RON_FTS5_CROSS_JOB_CONSUMER_PASS:staging.browser.0fbf4a4a127a640e`
- `RON_MULTI_AGENT_SKILL_COPY_COUNT=2`
- `RON_VERCEL_SKILLS_TWO_AGENT_INSTALL_PASS`
- `M4_DETERMINISTIC_REPLAY_3_OF_3_PASS`

## Exact staging assets
- [Skill contract](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/blob/sandbox/upstream-browser-skill-farm-20261026/sandbox/upstream-browser-skill-farm-20261026/skills/ron-browser-procedural-memory/CONTRACT.json)
- [Agent Skills SKILL.md](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/blob/sandbox/upstream-browser-skill-farm-20261026/sandbox/upstream-browser-skill-farm-20261026/skills/ron-browser-procedural-memory/SKILL.md)
- [Procedure memory implementation](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/blob/sandbox/upstream-browser-skill-farm-20261026/sandbox/upstream-browser-skill-farm-20261026/skill_memory.py)
- [Actual browser memory UAT](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/blob/sandbox/upstream-browser-skill-farm-20261026/sandbox/upstream-browser-skill-farm-20261026/browser_memory_uat.py)
- [Actual Playwright MCP 2-client UAT](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/blob/sandbox/upstream-browser-skill-farm-20261026/sandbox/upstream-browser-skill-farm-20261026/mcp_multiclient.mjs)
- [9-class capability tree](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/blob/sandbox/upstream-browser-skill-farm-20261026/sandbox/upstream-browser-skill-farm-20261026/CAPABILITY_TREE.md)

## Safety and infrastructure
- GitHub Actions hosted runner is ephemeral: no persistent always-on browser, no actual GPT login pool.
- No Windows or Google Drive accessed/modified during this implementation stage. No canonical RonSkillStore, AIOS.db, protected production config, real tokens, or external account cookies touched.
- Test-only reviewer state is NOT an actual Ron/PolicyGate decision.
- GitHub Actions may have plan quotas; no paid LLM APIs were called.
- Preserve existing SkillStore. Never introduce a second canonical database from a staging SQLite file.
- Upstream license review required for BrowserOS (AGPL), Browserless (SSPL) and n8n (fair-code).

## CURRENT SYSTEM STATE
- Work ID: UNKNOWN. Branch checkpoint: `16267315ce211a188cbb13a0244ae6c363a33518`.
- Source snapshots: 11; integrated CI artifacts latest: 5.
- GitHub CI state: VERIFIED SUCCESS, scoped to staging.
- Product complete: BLOCKED; not 9/9 accepted.
- One next action: integrate the actual OpenAdapt recorder and Stagehand cached replay against the same guarded GitHub fixture, with independent before/after evidence and failure drift test; keep same branch and no production mutation.
