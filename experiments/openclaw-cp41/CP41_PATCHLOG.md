# CP4.1 sandbox repair #1 — API provider config schema

- Input HEAD: `d5588ae3296b3963a4527c90df77cce44cdc778f`.
- GitHub Run: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41795831614
- First run: 6/7 transport cases PASS. Real OpenClaw agent fails config before invoking model.
- Evidence: `agent-stderr.json`: `models.providers.ronmock.auth: Invalid input (allowed: "api-key", "aws-sdk", "oauth", "token")`.
- Source docs claim `auth: "none"` support at upstream HEAD, but npm `2026.10.10` schema does not accept it; version parity UNKNOWN.
- Minimal fix: use published package's supported `auth: "api-key"` and static placeholder `apiKey: "cp41-fake-local-only"` on loopback-only fake model; it is NOT a credential, no external provider calls.
- Prior actual n8n tool integration: NOT TESTED. Retry no more than two repairs total in this CP4.1.
- Rollback: restore exact prior blob `f8c1805292231ad8b53422fb9d8fa6b3eb37f3bc` on branch after authorization. Main untouched.
