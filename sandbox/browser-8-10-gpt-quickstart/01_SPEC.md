# SPEC - RON-SHO Browser 8-10 GPT
Version 1.0 staging. Owner: Ron. Scope: Chrome local sandbox.

## Product
A single launcher opens one START_HERE help tab plus eight or ten https://chatgpt.com/ tabs in a dedicated Chrome profile. It never logs in, extracts credentials, sends messages, or automates ChatGPT. Eight tabs are NOT eight autonomous agents or independently isolated MCP sessions.

## Acceptance criteria
B01: Double-click FILE_A_START_BROWSER.cmd in Folder B.
B02: Choose 1 for 8 GPT tabs, 2 for 10, 0 to cancel. Invalid choice must fail.
B03: Google Chrome executable exists, missing Chrome produces a clear error.
B04: First browser tab is START_HERE.html with step-by-step directions.
B05: Option 1 opens 1 guide + 8 GPT links; option 2 opens 1 guide + 10 GPT links.
B06: Browser profile is CHROME_PROFILE_RON_SHO inside sandbox; do not expose or upload it.
B07: Login and ChatGPT account verification are human-only.
B08: No passwords, cookies, 2FA data or tokens are read or copied by our scripts.
B09: Human and AI runbooks contain exact paths, prompts, expected screen text, failure recovery.
B10: No production AIOS service/database, Windows Scheduled Task or firewall change.

## Proof required
Source and Chrome detected = SOURCE_VERIFIED. Successful launch command = EXECUTED. Actual tab count = UI_VERIFIED. Successful manual login and two separate conversations = HUMAN_UAT_PASS. Do not infer latter states from the former.

## Future scope, not part of this product
BrowserOS Neo, automatic multi-agent operation, independent MCP sessions, shared memory, SkillStore, Phả hệ, Gate acceptance.

## Safety
All ChatGPT tabs in this phase share the same isolated RON-SHO Chrome profile and account login. It is isolated from the user's regular Chrome profile, NOT isolated from other tabs inside the RON-SHO window. Respect ChatGPT account limits and terms; do not bypass CAPTCHA or authentication.
