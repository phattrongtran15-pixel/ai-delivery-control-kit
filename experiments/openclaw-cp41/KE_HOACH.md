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
- [x] 3. EXECUTE: GitHub Actions job executes local fake cases and a real OpenClaw embedded agent turn.
- [x] 4. INDEPENDENT READ-BACK: inspect run log, JSON receipts, artifact hashes, new branch/main SHA and failures.
- [x] 5. DECISION: GO/HOLD with precise trust boundary, minimum fix, Ron ACCEPT reserved.

## Execution contract
The fake deterministic model is a controlled stub: it does not demonstrate actual AI reasoning, genuine MCP-to-n8n tool semantics, credentials, reliable scheduling, Kilo/ACP routing, or production readiness. Do not equate simulated test PASS with real n8n E2E.

## Evidence closure — CP4.1 SANDBOX only
- Initial code commit: \`d5588ae3296b3963a4527c90df77cce44cdc778f\`; first CI \`41795831614\` = FAIL / 6 of 7 transport cases passed, OpenClaw config rejected custom provider \`auth:none\`.
- Minimal schema repair: \`691b307b8a0436ecc79378f09665abee0e219cbe\`; second CI \`41796052832\` = SUCCESS / 7 of 7.
- Oracle enhancement: \`e5b1e01efe92d250d9fcfc95a6ef288a99444618\`; final test CI \`41796446758\` = SUCCESS / 7 of 7. Distinct tests counted as inbound requests vs effective simulated execution.
- Artifact: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41796446758/artifacts/13304844990
- Artifact ZIP SHA256 (read independently after download): \`dd90f54243fcd04828a4eaba9297b31a374cbe9234e2aa99f7f77780e195d17f\`.
- Real OpenClaw embedded runtime used a loopback-only synthetic model: 2 model requests, 1 \`exec\` tool call, 0 tool failures, 1 simulated workflow created/validated/tested/evidenced.
- Negative canaries: timeout recovered with 2 create requests / 1 unique workflow; duplicate 2 create + 2 test requests / 1 effective test; permission denied / 0 creates; false READY / 0 creates; exhausted timeout / 0 validation or tests.
- IMPORTANT recovery gap: exhausted timeout produced 1 workflow effect on mock server with no acknowledged workflowId; MUST reconcile by idempotency key and verify state before a real-system retry or ACCEPT. \`UNKNOWN != PASS\`.
- Source/runtime parity: installed npm build \`7dc3350\` vs pinned GitHub HEAD \`062d5d8...\` — not established identical. \`auth:none\` docs/version drift is evidence of this.
- Decision: \`GO_SANDBOX_MOCK_ONLY\`; \`HOLD_REAL_N8N_MCP\`, \`HOLD_KILO_ACP\`, \`HOLD_PRODUCTION\`, \`WAITING_RON_ACCEPT\`.
- Independent main read-back at evidence closure: \`981c88592c78e908c1ce9c39dec93fa7718c4cd4\` unchanged.
