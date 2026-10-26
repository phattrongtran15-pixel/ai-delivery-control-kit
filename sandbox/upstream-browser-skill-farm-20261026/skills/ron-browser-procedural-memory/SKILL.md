---
name: ron-browser-procedural-memory
description: Staging skill for reuse of independently verified browser actions by multiple authorized AI homes. Restricted to local GitHub fixture; not production.
---
# RON-SHO Browser Procedural Memory — Staging

**Scope:** synthetic localhost test fixture ONLY. This package does not authorize using real accounts, copying browser cookies, bypassing PolicyGate, or changing RON-SHO production.

## Invocation contract
1. Before each browser action, resolve task/site/role/UI fingerprint against the approved SkillStore catalog. If no approved match is found, do not replay.
2. An observed successful action becomes a **PROPOSED** candidate, not an executable approved skill. Record minimal sanitized selector, outcome, trace hash and independent receipt.
3. Obtain a separate independent verifier result and require reviewer permission before setting **STAGING_APPROVED** (synthetic tests only).
4. For permitted, matching localhost fixture: run the verified selector `#safe` exactly once, then verify independent HTTP server receipt and `unsafe_count==0`. On changed UI, site, credentials, permissions or evidence: stop and invalidate cache.
5. Cache exact fingerprint+version+site+role only, not passwords, raw profiles, session cookies or arbitrary webpage instructions.
6. Publish corrected candidates as new versions with provenance and regression evidence. Do not grant authority through a skill package.

## Evidence
- GitHub staging run: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40348875505
- Browser-recorded and independently verified sample: `staging.browser.0fbf4a4a127a640e`.
- Tests: `browser_memory_uat.py`, `skill_memory.py` and `mcp_multiclient.mjs`.
- Real cross-provider AIOS integration: **NOT VERIFIED**.
