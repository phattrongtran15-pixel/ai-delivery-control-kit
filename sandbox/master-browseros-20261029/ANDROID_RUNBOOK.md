# MASTER BROWSEROS — ANDROID / PHONE RUNBOOK
Status as of 2026-10-29: Windows host software VERIFIED; Android connection/pairing NOT VERIFIED.

## Two different mobile capabilities
A. **Ask AI to operate BrowserOS** from Android ChatGPT: Open ChatGPT using the same account, connect/use private RON-SHO Master BrowserOS plugin and RON-SHO MCP Cloud (if available on that client). The Master plugin is a skill, not itself a native MCP connection. Existing RON Cloud bridge can execute bounded commands on Windows. This can start/check jobs but does not show a live GUI inside ChatGPT by itself.
B. **Actually WATCH / SEE / STOP the actor in GUI on phone:** use authorized Android remote desktop into Windows phatt to view the native BrowserOS neo Cockpit. Do NOT publicly expose 127.0.0.1:9210/mcp.

## Windows evidence, not Android acceptance
- RustDesk 1.5.0 installed, service RUNNING.
- Chrome Remote Desktop Host 157.0.8103.7 installed, chromoting service RUNNING.
- Tailscale 1.104.2 installed, service RUNNING.
This does not mean phone is paired, remote access provisioned or permission is granted.

## Recommended GUI workflow using existing Chrome Remote Desktop
1. On Windows under phatt, open https://remotedesktop.google.com/access and check **this laptop's existing access configuration**. Do not generate or share an unattended-access PIN in ChatGPT.
2. If not paired, Ron personally enrolls authorized Google account and sets PIN/security according to Google's page. Chrome Remote Desktop Host is installed, so avoid reinstalling without need.
3. On Android, install/open official Chrome Remote Desktop app from Google Play and sign into the matching authorized Google account.
4. Select registered laptop from Remote Access, enter PIN locally on phone, confirm native Windows desktop appears.
5. Open BrowserOS neo on Windows and select Cockpit, Watch actual actor, Stop matching session, Audit/Replay. Confirm the phone display shows the same page.
6. Disconnect remote session, lock Android and Windows, revoke old access if device lost.
7. Record UAT screenshot and receipt without secrets. Stop on unexpected security prompts; no router port-forward.

## Alternative RustDesk
RustDesk client also installed on Windows; official Android client supports Mouse/Touch mode. Pair only with Ron's explicit approval and locally enter device ID/password. Use secure pairing and approved relay; do not publish ID/password in logs or chat.

## Do not assume
- No evidence of native BrowserOS Android app or of direct localhost MCP from Android.
- Do not provide raw remote desktop credentials, browser profile or secrets to an AI skill.
- No remote interactive UAT PASS before phone screenshot + actual user test.

Sources:
Google Android Remote Desktop: https://support.google.com/chrome/answer/1649523?co=GENIE.Platform%3DAndroid&hl=en
RustDesk Android official: https://rustdesk.com/docs/en/client/android/
