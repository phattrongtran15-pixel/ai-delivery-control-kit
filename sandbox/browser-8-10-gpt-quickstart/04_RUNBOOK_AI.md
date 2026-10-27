# RUNBOOK AI - CONTRACT FOR SUCCESSOR AGENT

Product: RON-SHO Browser Tab Launcher, phase 1.
Work ID: UNKNOWN. Asset ID: UNKNOWN. Owner: Ron. G5 production: NOT ACCEPTED.
Host: Windows, C:\Users\phatt\AI_OS_TEAM.
Root: 98_SANDBOX/RON_SHO_BROWSER_8_10_GPT.
Entrypoint: FILE_A_START_BROWSER.cmd.
Logic: LAUNCH_BROWSER.ps1.
Browser: existing Google Chrome, dedicated CHROME_PROFILE_RON_SHO.
Expected: 1 START_HERE tab + 8 or 10 chatgpt.com tabs.

## Required read order
01_SPEC.md, 02_HANDBOOK.md, 03_RUNBOOK_HUMAN.md, 05_KICH_BAN_0830.md, both scripts, EVIDENCE receipt.

## Execution contract
1. Verify Chrome path, file presence and source hashes READ_ONLY.
2. Review PowerShell and CMD: no extraction of profile, no automatic login or chat send, no copying credentials.
3. Verify 8 → 9 URLs (1 help + 8 ChatGPT); 10 → 11 URLs, 0 cancels, invalid choice fails.
4. Run syntax/static check. If launching Chrome within an authorized session, observe the actual tab count by UI, NOT merely command exit.
5. Ron signs in himself. Never use AI to extract passwords/cookies or circumvent CAPTCHA/rate limits.
6. User manually tests GPT 01 and GPT 02, then reports actual result.
7. Save evidence as script hash, timestamp, test command and tab count. Do not save profile/cookies/private chats.
8. Fail closed when access or real UI confirmation is missing. REPORT STATUS as VERIFIED, REPORTED, UNKNOWN, BLOCKED.

## Prohibited
Do not create real AIOS Work IDs or Gate approvals in a JSON file. Do not edit production AIOS.db, install services, alter Windows Scheduled Tasks, configure remote debugging/CDP, expose local profile to GitHub/Drive or host browser over public network. No 8-10 autonomous GPT claim from 8-10 tabs.

## Handoff fields
Source SHA, host, root folder, launched option, script test results, actual Chrome tabs observed, user-login confirmation, GPT 01/02 chat check, blockers, rollback, exactly ONE next action.

## Recovery
Close ONLY dedicated browser window. Retain Chrome profile unless Ron authorizes deletion. All code files reside under the staging root, so changes must be checkpointed and diffed before altering them.
