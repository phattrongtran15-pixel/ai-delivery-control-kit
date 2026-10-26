# RUNBOOK — Browser Intelligence five-gate operations
Human: [RUNBOOK_HUMAN.md](RUNBOOK_HUMAN.md) | AI: [RUNBOOK_AI.md](RUNBOOK_AI.md)
GitHub remains the code/test origin; Google Drive is a version-stamped, read-only-by-default operating documentation projection. The production memory source remains the existing AIOS SkillStore/PolicyGate, **not this package**.

**Use case:** qualify, replay, inspect, verify and hand over an already scoped staging version. Production deployment and login pooling are not granted.
**Start:** Re-run the verified [Five Gates Actions run 40358101487](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40358101487) via **Re-run all jobs**. To verify a newer source commit, a scoped push to the same staging branch triggers this workflow. Branch-only workflows generally cannot be dispatched manually from GitHub UI until also present on default branch; do not merge for this.
**Stop:** Cancel the GitHub run from GitHub Actions if needed; temporary runner/job/browser contexts end. This is not an always-on server.
**Rollback:** Revert/delete only candidate commits on sandbox branch after preserving receipt; do not change `main`, production hosts, Drive canonical resources, or AIOS.db.
**Restore:** Checkout immutable known-good `40ce3365...` in a fresh staging copy and re-run the 48-client test. Confirm matching source hash + outcome/role isolation. This is a **procedure**, not a restore test already performed.
**Drift response:** pause replay on origin/role/UI mismatch, revoke candidate in sandbox, verify known-good snapshot; owner approval before production rollback or data writes.
**Success condition:** CI verifier PASS may qualify G1–G4 **for its scope**; G5 remains HOLD until Ron acceptance, recovery UAT and successor ACK.

Do not use a browser session or skill to bypass host policy, rate limits, secrets or service terms.