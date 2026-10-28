# RUNBOOK AI v1.1 — STEP-BY-STEP, FAIL-CLOSED

## Source of truth
Folder B: `C:\Users\phatt\AI_OS_TEAM\98_SANDBOX\RON_SHO_BROWSER_8_10_GPT`.
Read `00_README.md`, `01_SPEC.md`, `02_HANDBOOK.md`, `03_RUNBOOK_HUMAN.md`, `05_KICH_BAN_0830.md`, `06_VISUAL_EVIDENCE.md`, `LAUNCH_BROWSER.ps1`, and test receipt before any operation.

## Step 1: READ_ONLY preflight
Confirm File A, PowerShell script, START_HERE and installed Chrome; record source SHA and timestamp. Never inspect/export the Chrome profile.

## Step 2: Validate input
Check 0 cancels; 1..10 allowed; other input rejected. Use `powershell -NoProfile -ExecutionPolicy Bypass -File LAUNCH_BROWSER.ps1 -DryRunCount N` for N=1,2,8,10 and 11 (negative). Dry-run does not launch Chrome. For 1/2/8/10 assert total URLs=2/3/9/11 and GPT_URLS=N.

## Step 3: Launch with explicit user intent
Run File A, user enters N. No automated login, prompts or account switching. Do not imply N AI agents exist.

## Step 4: Independent readback
Check actual browser tab count from authorized UI session; Chrome process count is **not tab count**. If `INTERACTIVE_SESSION_UNAVAILABLE`, mark UI verification UNKNOWN, not PASS. Never invent screenshots.

## Step 5: Human UAT
Ron logs in directly; creates two distinct conversations when N>=2. Human reports PASS/FAIL. One tab may be tested with N=1.

## Step 6: Evidence and provenance
Every screenshot must have source, capture method, timestamp, observed tab count, redaction and SHA. External repo images must have exact source URL/license and be labeled `REFERENCE_ONLY`; conceptual mockups labeled `MOCKUP_NOT_TESTED`. Current local capture returned `INTERACTIVE_SESSION_UNAVAILABLE`.

## Step 7: Handoff
Return VERIFIED / EXECUTED / UNKNOWN / BLOCKED, source hash, N chosen, real tab count or UNKNOWN, login or UNKNOWN, independent verifier, exactly one next action. Never mutate AIOS.db, PolicyGate, services or canonical SkillStore.
