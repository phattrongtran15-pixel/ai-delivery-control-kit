# SPEC — Browser Launcher v1.1

## Goal
User chooses **N = 1..10**. Chrome opens **N ChatGPT tabs + one START_HERE guide tab**, using a dedicated RON-SHO Chrome profile. Input 0 cancels. Invalid or out-of-range input fails without browser launch.

## Requirements
- B01: File A in Folder B starts launcher by double-click.
- B02: Any integer 1..10 accepted; 0 cancels; letters, fractions, negative and >10 rejected.
- B03: Use installed Chrome; no new BrowserOS install.
- B04: Separate `CHROME_PROFILE_RON_SHO` profile, but all N tabs **share this profile**.
- B05: START_HERE is a local guide; user signs in directly in ChatGPT.
- B06: No automated messages, MCP agents, credentials extraction, AIOS mutation, scheduler or public web service.
- B07: Two runbooks, handbook, 08:30 walkthrough, evidence and visual provenance.
- B08: UAT requires observed correct tabs, human login and successful chats. Script success alone is not UAT.

## Tests
Dry-run N=1 → 2 URLs, N=2 → 3 URLs, N=8 → 9 URLs, N=10 → 11 URLs, N=11 → exit 11. These were executed on local Windows. Visual tab count remains UNKNOWN because interactive screen capture was unavailable.

## NOT in scope
1..10 **ChatGPT browser tabs** are not 1..10 independent GPT accounts or autonomous AI agents. BrowserOS, MCP, 5 Gates and SkillStore integration are future phases.
