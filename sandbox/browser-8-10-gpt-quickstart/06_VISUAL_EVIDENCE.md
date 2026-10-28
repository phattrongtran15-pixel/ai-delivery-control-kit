# VISUAL EVIDENCE REGISTER — KHÔNG DÙNG ẢNH GIẢ LÀM BẰNG CHỨNG

## V1: Windows Folder B
Status: NOT CAPTURED. Required future image: screenshot File Explorer showing File A, excluding private paths outside sandbox. Source: user's Windows machine. Capture method: approved interactive session or Ron screenshot.

## V2: Black launcher window
Status: NOT CAPTURED. Required future image: real menu after File A double-click, before typing N. Source: Windows screenshot with timestamp and code hash.

## V3: Browser N=2
Status: NOT CAPTURED. Required future image: Chrome tab strip with 1 START_HERE + 2 ChatGPT tabs, URL bar visible, private chat content redacted.

## V4: START_HERE
Status: LOCAL HTML SOURCE VERIFIED, SCREENSHOT NOT CAPTURED. Source: `START_HERE.html`. Do not label source-derived illustration as a real screenshot.

## V5: External repository documentation
Status: NOT RETRIEVED. No unverified community screenshot is included. When using upstream BrowserOS images, cite the exact README/image URL, version and license; never claim they depict the local Chrome launcher.

## Why no screenshots?
On 2026-10-28, `desktop_screen_capture(include_base64=false)` returned `INTERACTIVE_SESSION_UNAVAILABLE` (WinError 10061, connection refused). Thus a real desktop capture could not be obtained. The honest evidence is terminal dry-run and process inspection, not screenshots.

## Screenshot acceptance contract
Image filename, source URL/path, timestamp, capture tool, target host, test input, expected/observed tabs, redaction statement, SHA-256, independent verifier. Never include cookie, OTP, private chats or login tokens.
