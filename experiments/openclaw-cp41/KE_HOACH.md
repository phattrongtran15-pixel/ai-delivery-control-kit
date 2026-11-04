# KE_HOACH — OpenClaw CP4.1 GitHub SANDBOX_ONLY

## CP3 inherited checkpoint
- Branch: \`sandbox/openclaw-cp3-20261104\`
- HEAD before CP4.1: \`990c078e4aa888d18cbd812af8016ac19c4e3167\`
- Upstream code checkpoint: \`062d5d85481fca84c57014e7c3a128fc4386ea79\`
- Tested npm build: \`openclaw@2026.10.10\`; package/source byte parity still UNKNOWN
- CP3 CI run IDs: \`41788971022\`, \`41789468813\`, both SUCCESS.
- Rollback: restore sandbox branch to pre-CP4.1 checkpoint only under explicit approval; never force-update main.

## Scope and acceptance criteria
- Single Mission ingress into real \`openclaw agent exec\` with local fake OpenAI-compatible model (127.0.0.1), no paid provider.
- Fake HTTP n8n transport stages: readiness -> create -> validate -> test -> evidence.
- Deterministic positive and adversarial tests: success, recoverable timeout, duplicate execution, missing permission, false READY, exhausted timeout.
- Verify downstream effects, idempotent workflow identity, unique create/test, signed-by-hash simulated receipt; no real n8n, no external API, no secrets.
- \`gateway status\` return code alone is insufficient readiness evidence.
- Agent integration result must show model stub called, actual OpenClaw tool dispatch, and downstream fake effects; otherwise HOLD even if transport tests PASS.
- Protected mutation only sandbox files; no release/merge/production credentials; no auto ACCEPT.

## Checklist
- [x] 1. READ_ONLY: pin CP3 source/branch/CI evidence, examine official \`agent exec\` and custom provider contracts.
- [x] 2. CHECKPOINT: record branch HEAD SHA and rollback; create fake transport, provider and CI candidate only in sandbox branch.
- [ ] 3. EXECUTE: GitHub Actions job executes local fake cases and a real OpenClaw embedded agent turn.
- [ ] 4. INDEPENDENT READ-BACK: inspect run log, JSON receipts, artifact hashes, new branch/main SHA and failures.
- [ ] 5. DECISION: GO/HOLD with precise trust boundary, minimum fix, Ron ACCEPT reserved.

## Execution contract
The fake deterministic model is a controlled stub: it does not demonstrate actual AI reasoning, genuine MCP-to-n8n tool semantics, credentials, reliable scheduling, Kilo/ACP routing, or production readiness. Do not equate simulated test PASS with real n8n E2E.
