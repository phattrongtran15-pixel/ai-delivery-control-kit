# SPEC — Browser Intelligence 9-Capability Gate Contract
**Kind:** PRODUCT candidate, **Work ID:** UNKNOWN, **authority:** candidate-only.
**Acceptance oracle:** physical independent readback for every row, same commit under G4. Source-only, schema-only or CI green does not meet G5.

## Behavior and traceability
| ID | User-mandated capability | OpenSpec requirement | LikeC4 component | Staging evidence / test | FULL acceptance missing |
|---|---|---|---|---|---|
| C1 | Monitor many AI | R1 Browser monitoring | monitor | `mcp_actor_scale.mjs` dashboard + PNG (48 rows) | Real LLM actors / BrowserOS deployment |
| C2 | Isolated MCP sessions | R2 Isolated MCP sessions | mcp | `mcp_actor_scale.mjs`, 48/48 A/B-cookie isolation | Cross-host authenticated gateway |
| C3 | Skill learning | R3 Learn verified procedures | learning | `browser_memory_uat.py` proposal lifecycle | Autonomous synthesis+independent qualification |
| C4 | Capture/replay/verify | R4 Recorded replay | recorder | M4 3/3 + real browser fixture HTTP receipt | Complete event/video recorder on real sites |
| C5 | Fast action cache | R5 Safe action cache | cache | `browser_memory_scale.py` 48/48 cache hits | Stagehand baseline speedup, UI drift regression |
| C6 | Cross-agent search | R6 Searchable memory | memory | `skill_memory.py` SQLite FTS5 cross-process/job | Durable online authorized semantics |
| C7 | Automation | R7 Durable automation | automation | `ron-9-capability-sandbox.yml` CI PASS | Persistent workflow retries and idempotence |
| C8 | Shared Local/Cloud memory | R8 Cross-platform sharing | sharing | Artifact handoff+Vercel Skills Codex/Kilo test homes | Real Local/Cloud adapter and canonical registry |
| C9 | Capability evolution tree | R9 Capability lineage | tree | Archify workflow HTML + 9 cited atoms, source-hash test | Live graph + approved registry versioning |

Canonical machine-readable capability IDs are **candidate labels** C1–C9, NOT registered AIOS IDs. Real IDs must come from the registry; never invent one.
Source references: `openspec/specs/browser-intelligence/spec.md`, `likec4/browser-intelligence.c4`. Diagram is proposed composition, not evidence of production runtime.

## Architecture / safety
Actor adapters (MCP/API with per-host attestation) → before-browser-action recommendation/PolicyGate → browser session broker → sanitized action trace → independent outcome verifier → proposed skill → authorized registry publication → versioned Local/Cloud projection → capability graph.

**Privilege boundary:** no cross-account cookie sharing; no secret/PII in learned skills. Prompt-injection text from websites remains untrusted. Learning/recording is opt-in under host policy. No side effect from recommendation without authorized actor.
**State lifecycle:** OBSERVED → PROPOSED → VERIFIED_STAGING → STAGING_APPROVED (sandbox-only). Canonical state remains UNKNOWN. Later `RON_ACCEPTED` requires trusted PolicyGate and human approval, not editable JSON.

## Gates
- **G1:** mission, owner and user acceptance oracle written; canonical asset/Work IDs not resolved → registration remains BLOCKED.
- **G2:** nine OpenSpec requirements and a LikeC4 model linked to C1–C9; repository/model validation in staging needed.
- **G3:** GitHub sandbox code commit and rollback SHA identified, no production mutation.
- **G4:** independent GitHub job verifies exactly the same commit with negative tests; historical 48-client receipt is evidence only for that historical SHA.
- **G5:** HOLD until Ron reviews full live actor UAT, validates rollback and successor ACK.

**Change policy:** REUSE → ADAPT → CONFIGURE → BUILD; respect licenses, GitHub Actions quotas, only scoped staging activity.