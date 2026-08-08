# Changelog

## 0.2.1 — 2026-08-09

- Separated Gateway necessity from activation readiness.
- Added downstream end-to-end binding, verified demand, and approved resource budget as activation gates.
- Added a fail-closed `HOLD_ACTIVATION_BLOCKERS` state.

## 0.2.0 — 2026-08-09

- Updated GitHub Actions runtime dependencies to current major releases.
- Added explicit single-agent and peak-concurrency signals.
- Added verified concurrency-contention as a direct Gateway trigger.
- Added frozen command-asset disposition and recovery actions.
- Documented how to preserve commands without activating the Gateway runtime.
- Added agent identity, designated-folder, inter-agent inbox, and prompt-injection control placement.
- Added an explicit 50+ AI scale-review signal without treating agent count as automatic Gateway approval.

## 0.1.0 — 2026-08-09

- Added deterministic Gateway-necessity assessment.
- Added Work Package validation with `OWNER_HOURS_REQUIRED`.
- Added sanitized recovery case study, claim ledger, and demand contract.
- Added tests and CI.
