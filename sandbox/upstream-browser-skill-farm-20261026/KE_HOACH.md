# KE_HOACH — GitHub-only upstream browser + skills deployment
Date: 2026-10-26 | Mode: SANDBOX | Target: GitHub Actions on `phattrongtran15-pixel/ai-delivery-control-kit`.
Mission: Reuse high-star upstreams; download pinned source into GitHub hosted runner, run repeatable browser + skill interoperability smoke tests, publish evidence artifacts. **No Windows, C:, G:, Google Drive, production browser or real GPT accounts.**

## 5 checkpoints
- [x] CP1: Inspect existing successful Browser Use M4 evidence (run 40019468606), upstream stars, pin upstream commits.
- [x] CP2: Create an isolated branch `sandbox/upstream-browser-skill-farm-20261026`; checkpoint = immutable parent `2d8dc2b3e47edbd39bb4fde76fcdb18d0df308a0`.
- [ ] CP3: Commit lock manifest, tests and dedicated GitHub Actions workflow, read back exact files.
- [ ] CP4: Let push-trigger run; retrieve run/job logs and artifacts; classify each tested capability as VERIFIED, FAILED, BLOCKED, UNKNOWN. No fake production claims.
- [ ] CP5: Ron reviews result; promote **only after approved gates**. Keep original branch untouched.

## No branching / safety
- One implementation track; no other repos created, no forks, no core replacement.
- Source snapshots: pinned Git commit, GitHub Actions temporary runner plus downloadable artifacts; never auto-run unreviewed upstream postinstall scripts except isolated CLI smoke.
- Action permission `contents: read`; no secrets or paid APIs; local HTTP fixture only; no internet credentials; no real ChatGPT sessions.
- CI passing != production deployment. Simulator skill handoff != real cross-vendor AIOS hook.
- Browserless license is SSPL; AGPL/SSPL/commercial implications must be reviewed before shipping.
- Rollback: delete staging branch or revert its commits; no production state has changed.

One Next Action: verify CI run result after workflow push and inspect the evidence artifact before further action.
