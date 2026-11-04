# CP4.1 Windows READY bootstrap fix #2

- **Prior failing run:** https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/41801311159.
- **Evidence:** OpenClaw installed on Windows and Gateway healthy; CLI create refused `--command-argv` because PowerShell 5.1 native argument quoting removed JSON string quotes.
- **Fix:** Node subprocess (shell:false) with explicit argument vector and retained JSON argument file; preserve JSON payload byte-accurately, only for fixed, allowlisted local health script.
- **CI fix:** Remove continue-on-error, independently require BOOTSTRAP_RESULT status SAFE_AUTOMATION_READY, scheduled effect file, Status = 0.
- **Checkpoint:** 776c8115a97e76fa1a8fb7304174ed14f52a17d1; original source blob b36d5ceee42c486b477031a49c9eb9b32d4b7992; original workflow blob 0e705858a1894cc10a72f593f641ae364ea6522f. Rollback = restore these two blobs in sandbox branch only.
- **Main:** Unchanged. No model API or n8n production, no operator credential exported.
