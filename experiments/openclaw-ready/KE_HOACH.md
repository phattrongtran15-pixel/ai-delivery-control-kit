# KE_HOACH.md — OpenClaw Strong Automation quickstart

## Mission
Ron can run a single PowerShell command on Windows. Bootstrap itself checks CLI, dedicated loopback Gateway, fixed command automation and independent file receipt. Ron need not manually test. One-time provider login is still required for genuine AI reasoning.

## Baseline
- Repo: phattrongtran15-pixel/ai-delivery-control-kit
- Branch: sandbox/openclaw-cp3-20261104
- Previous CP4.1 checkpoint SHA: 6c27a90cfb06431d140167814ebf7fa175f6ae43
- Profile: ronsho-sandbox, port 18847, localhost-only, separate from default and RON-SHO production.
- Only the fake/non-model scheduled health check is auto-enabled. Kilo ACP, n8n, Lobster and unrestricted tools remain disabled/not configured.

## Checklist
- [x] CP1 Research: official Windows, cron, health, ACP, Lobster, config validation.
- [x] CP2 Checkpoint and source: isolated profile PowerShell setup with owner marker, local receipt, rollback mode, and GitHub CI.
- [ ] CP3 GitHub CI Windows parser + offline self-test + static guards, independent read-back.
- [ ] CP4 Ron's one paste: auto-install OpenClaw if missing, setup isolated Gateway and safe scheduled task, run it once and verify fresh receipt. Without live host access Windows runtime is UNKNOWN.
- [ ] CP5 Human Acceptance: Ron may login to provider once; independently verify model, ACP Kilo and n8n before production promotion. No auto ACCEPT.

## Security
Official installer downloaded over HTTPS and SHA logged (not pinned); user must trust official source. Script never requests or embeds third-party API keys, never exposes Gateway beyond localhost, generates unique token, denies model-visible privileged tools, and uses exact argv for one local scheduled health receipt. Native command automations execute at Gateway privileges and DO NOT inherit agent exec approvals, so enabling any arbitrary command would be unsafe.

## Rollback
Run script with -Mode Rollback. It checks RONSHO_OWNED.json, removes only the named cron job and stops/uninstalls only the named profile service; keeps runtime files/evidence, never touches main/default profiles.

## Evidence
GitHub Actions self-test is a parser/contract check, not proof of Windows installation. Local status SAFE_AUTOMATION_READY only after successful Gateway health plus run-now command job and fresh file effect. AI model/n8n/ACP state remains UNKNOWN.
