# KE_HOACH — 5 Gates × 9 Core Capabilities
**Scope:** one GitHub sandbox project + a versioned Drive documentation projection. This is NOT another orchestrator.

| Gate | Minimum deliverable | Owner and evidence | Current result |
|---|---|---|---|
| G1 DEFINE | Mission, scope, owner, nine pass/fail oracles | Ron demand, `README.md` / `SPEC.md` | DOCUMENTED; canonical Work/Asset ID UNKNOWN |
| G2 DESIGN | OpenSpec R1–R9, LikeC4 node R1–R9, reuse, risk | `openspec/.../spec.md`, `likec4/...c4` | CANDIDATE; pending native CLI check |
| G3 BUILD | bounded GitHub staging build + source SHA + rollback | `40ce3365...`, test artifacts | STAGING BUILT (not production) |
| G4 VERIFY | independent same-revision checks, negative tests, hash/receipts | existing run `40354279483` + 5-gate verifier CI | historical run PASS; NEW G4 must be independently rechecked |
| G5 OPERATE | Ron acceptance + production runtime + restore + successor ACK | `RUNBOOK_HUMAN.md` / `RUNBOOK_AI.md` + signed human decision | HOLD / NOT ACCEPTED |

## Acceptance checklist
- Every one of **C1–C9** must pass on *real* authorized AI Local and Cloud actors, not synthetic labels.
- Every skill publication requires independently observed effect, version, risk classification and PolicyGate permit.
- MCP must isolate storage/accounts; no cross-agent credentials.
- Browser monitoring is observable; no loss of evidence after restart, on network split or after partial failure.
- Cache speedup measured against uncached baseline; invalidate on UI/role/origin mismatch.
- Capability tree uses accepted registry state, not fabricated or staging-only IDs.
- Recovery/rollback and successor runbook are actually exercised and read back.
- GitHub and Google Drive projections are versioned; Drive never invents real-time canonical truth.

## Next action
Obtain trusted canonical Work/Asset bindings and authorize one model-backed local-compatible + cloud-compatible end-to-end pilot (same repository/track), then bring new receipts to Ron.