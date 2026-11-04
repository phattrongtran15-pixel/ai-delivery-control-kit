# OpenClaw Windows alias fix — checkpoint

- Failed run: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41800334382
- Evidence: npm install `openclaw@2026.10.10` on Windows PASS but bootstrap failed INSTALL_CLI because built-in PowerShell alias `cli` maps to `Clear-Item` and overrides the custom `Cli` function.
- Minimal repair: rename all 7 function references to `Invoke-OC`, no changes to policy.
- Checkpoint: `54a6ecbfb53aa7cb27ffc83dbd46cf0783c458dc`, original blob `b679c96680254138adc0256452e9d1d16637b1eb`.
- Rollback: restore original file blob only within the sandbox branch, never main.
- Local deployment: NOT EXECUTED; no user Windows evidence yet.
