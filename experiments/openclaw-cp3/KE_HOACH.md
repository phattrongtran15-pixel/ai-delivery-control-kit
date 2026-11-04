# KE_HOACH — OpenClaw GitHub Sandbox CP3 (2026-11-04)

## Mission
Verify OpenClaw as a possible executor coordinator for RON-SHO without touching production, without model/API spending, and without claiming n8n E2E until credentials and mock transport are tested.

## Canonical checkpoint
- Upstream: https://github.com/openclaw/openclaw
- Pinned source commit: `062d5d85481fca84c57014e7c3a128fc4386ea79`
- Published npm version to install: `2026.10.10` (NOT assumed byte-identical to source commit)
- Test repo: `phattrongtran15-pixel/ai-delivery-control-kit` (public isolated sandbox)
- Base commit: `981c88592c78e908c1ce9c39dec93fa7718c4cd4`
- Branch: `sandbox/openclaw-cp3-20261104`
- Guard: no secrets, no production URLs, no real n8n, no model calls, no daemon install, no main edits.

## Checklist
- [x] CP1 (READ_ONLY): identify upstream repo, source SHA, version requirements, current GitHub permissions. Evidence: upstream README/package and GitHub connector.
- [x] CP2 (SANDBOX CHECKPOINT): isolated branch from known base commit. Rollback: delete only isolated branch after Ron accepts deletion; `main` remains untouched.
- [ ] CP3 (SANDBOX EXECUTION): GitHub Actions installs pinned npm package with lifecycle scripts disabled, fetches pinned source manifest, probes CLI/version/help/ACP/plugin/gateway status. Evidence: run ID, job logs, uploaded receipt. No model and no real n8n.
- [ ] CP4 (INDEPENDENT VERIFY): read GitHub jobs/logs/artifact and check pass/fail/unknown. Negative assertions: no secrets, no production mutation, no auto ACCEPT.
- [ ] CP5 (DECISION): classify REUSE/ADAPT/GAP and choose whether separate n8n mock E2E test is justified; Ron retains ACCEPT authority.

## Acceptance rule
A green install/smoke job establishes installation and help CLI only. It does NOT establish successful one-prompt n8n, MCP/ACP live routing, safe production access, or quota independence. UNKNOWN is not PASS.

## Rollback
Do not delete or modify source default branch. To revert sandbox work, first check isolated branch still points to expected test commit; then delete that branch only after authorized approval. No credentials created, no local host changes.
