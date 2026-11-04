# RON-SHO OpenClaw STRONG + Automation — Runbook v0.1

## Mission
Deliver a one-command Windows sandbox bootstrap plus a practical, evidence-gated path to actual one-Mission automation without manual verification chores for Ron. Technical integration is NOT ACCEPTED until each integration is independently verified.

## Capability map — REUSE before BUILD
| Goal | Native OpenClaw component | Scope now | Preconditions |
|---|---|---|---|
| One request → multi-tool agent | `openclaw agent exec`, Gateway | Synthetic 7/7 PASS CP4.1 | model auth and tool scope for real work |
| Timed operations | `openclaw automations` (`cron` alias) | Windows safe fixed-command candidate | Gateway running and role operator.admin |
| Strong deterministic pipeline | Official `@openclaw/lobster` | RESEARCHED, not installed | enable plugin deliberately, explicit approval, host-trust surface |
| Kilo / OpenCode delegation | ACP agents `kilocode`, `opencode` | RESEARCHED, not routed | installed CLI, live model auth, ACP lease/policy/identity |
| n8n authoring | n8n MCP with tool allowlist | Synthetic fake n8n 7/7 PASS | disposable real n8n, correct permissions, reconcile orphan workflows |
| Evidence & health | `health --json`, automation run history | wrapper tests fail-closed | runtime read-back and source/receipt hashes |

## Run now — first safe automation (no model needed)
From native Windows PowerShell, use the pinned `Start-RonOpenClaw.ps1` at the source commit documented in the GitHub branch. It installs OpenClaw if absent using the official HTTPS installer, creates a dedicated `ronsho-sandbox` profile on port 18847, creates a scheduled **read-only** PowerShell health receipt job every 30 minutes, force-runs it once, and independently checks for a recent receipt. Output is `SAFE_AUTOMATION_READY` or `HOLD [stage]`.

Native cron command jobs execute in the Gateway process and do not inherit model-facing `tools.exec` approvals. The bootstrap therefore uses only exact argv with one fixed file and never accepts a prompt-supplied shell command.

Runtime files:
- `%USERPROFILE%\.openclaw-ronsho-sandbox\openclaw.json` — scoped auth token, DO NOT SHARE.
- `%USERPROFILE%\.openclaw-ronsho-sandbox\ronsho-evidence\BOOTSTRAP_RESULT.json`
- `%USERPROFILE%\.openclaw-ronsho-sandbox\ronsho-evidence\BOOTSTRAP_HOLD.json` if failed.
- Dashboard `http://127.0.0.1:18847` (local browser only).

The first bootstrap **does not** configure model credentials, privileged agent tools, n8n, mobile channels or production permissions.

## One-time provider login — human action
```powershell
openclaw --profile ronsho-sandbox onboard --classic
openclaw --profile ronsho-sandbox dashboard
```
Use the official masked login/browser flow only. Never paste API tokens, login cookies, OAuth secrets or n8n credentials into ChatGPT. Provider/quota is independent from the OpenClaw app; no promised free model usage.

## Strong mission prompt — preview mode (safe to paste into dashboard after model login)
```text
MISSION: Design a single n8n workflow to check overdue orders every day at 08:00 Asia/Ho_Chi_Minh, read a MOCK Google Sheets dataset, classify late orders, draft (do not send) email alerts, and write a simulated report.
CONSTRAINTS: Sandbox only. No production n8n, no real Gmail/Sheets credentials, no activation or outbound messages. Inspect available capabilities before proposing tool calls. If n8n MCP, Kilo ACP or permissions are unavailable, report HOLD and produce an executable plan instead of claiming execution.
OUTPUT: mission, steps, actor/tool ownership, draft workflow JSON, node mapping, test cases, timestamps, source/line refs, independent evidence receipts and UNKNOWN/HOLD gaps. Executed != Verified != Accepted. Ron decides final approval.
```
Under the initial tool-deny profile this is a **design/preview** task only. Real n8n create/update/test requires an approved adapter, identity, credentials and disposable sandbox.

## Actual one-Mission execution path (future proof gates)
1. Onboard model and check `openclaw --profile ronsho-sandbox models status` with documented provider and quota, no secrets exported.
2. Verify Kilo ACP adapter routing `kilocode` in an isolated workdir; no global shell rights.
3. Connect a disposable n8n instance/MCP with only create/validate/test scopes, keep activate/send disabled.
4. Reconcile timed-out create by idempotency key before retrying; keep a durable Work ID, step receipts and independent verifier.
5. Promote to real automations only after Ron accepts both safety and E2E evidence.

## Inspect without manual guessing
```powershell
openclaw --profile ronsho-sandbox health --json
openclaw --profile ronsho-sandbox automations list --all --json
openclaw --profile ronsho-sandbox security audit --json
openclaw --profile ronsho-sandbox tasks list
```
The bootstrap auto-collects its own readiness receipt; the above commands are optional independent investigations.

## Rollback
The bootstrap provides `-Mode Rollback`: guard owner marker, remove only its managed automation, stop/uninstall only its named Gateway service. All files and receipts are retained for read-back. Do not use `--force` to overwrite unrelated production state.

## Evidence baseline
- OpenClaw CP4.1 synthetic actual `agent exec` tool dispatch: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41796803853 — PASS 7/7 mock cases.
- Windows PowerShell self-test: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41800153952 — PASS.
- First Windows native smoke: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41800334382 — HOLD due to PowerShell `Cli` alias. Fixed source in sandbox commit `f9cf1b019c3157d085d1374d88358d369517f9c7`, native retest underway.
- Local Ron Windows runtime: UNKNOWN (Desktop Commander offline and RON-SHO MCP Cloud unreachable as of this session).

## Documentation sources (verified 2026-11-04)
- https://docs.openclaw.ai/cli/cron
- https://docs.openclaw.ai/tools/lobster
- https://docs.openclaw.ai/tools/acp-agents/quickstart
- https://docs.openclaw.ai/platforms/windows
- https://docs.openclaw.ai/cli/health
