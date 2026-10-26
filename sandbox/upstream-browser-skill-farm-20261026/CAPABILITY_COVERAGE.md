# RON-SHO — 9 immutable capability criteria (GitHub-only staging)
Checkpoint: 2026-10-26. **Do not fork scope into adjacent architecture.**
Success means verified integrated capability, not merely cloning a GitHub repository.

| # | Core user criterion | Primary high-star upstream | Test currently planned in GitHub | Not yet claimed |
|---|---|---|---|---|
| 1 | Browser thấy/giám sát nhiều AI | browseros-ai/BrowserOS (14,104★) | pin & source snapshot; browser dashboard PNG produced from sandbox fixture | Running BrowserOS's actual GUI with multiple real LLM agents |
| 2 | MCP đa phiên cô lập | microsoft/playwright-mcp (38,653★), browser-use/browser-use (119,187★) | CLI install/help; 3/6/10/15 real isolated Chromium contexts on localhost | MCP protocol multi-agent live cross-provider UAT |
| 3 | AI học/phát triển skill mới | OpenAdaptAI/OpenAdapt (1,826★) | source snapshot; simulated new candidate lifecycle | Autonomous skill synthesis and acceptance |
| 4 | Ghi thao tác, replay, verify | browser-use/browser-use, OpenAdapt | reuse prior M4 deterministic browser replay, ActionGuard, independent HTTP receipt | Full visual recording + OpenAdapt executable replay |
| 5 | Cache thao tác chạy nhanh | browserbase/stagehand (25,826★) | source snapshot, contract research | Stagehand cache performance benchmark |
| 6 | Bộ nhớ tìm kiếm xuyên agent | mem0ai/mem0 (67,841★) | pinned full source download | Running persistent vector memory with semantic retrieval |
| 7 | Automation | n8n-io/n8n (208,641★) | snapshot + GitHub Actions automated tests as separate functional proof | Real n8n server workflow configured |
| 8 | Shared memory Local ↔ Cloud | vercel-labs/skills (36,637★), iflytek/skillhub (5,299★), Mem0 | producer job skill artifact -> distinct consumer job; hash+role/permission guards | Real cross-model pre-browser-action hook or canonical RonSkillStore write |
| 9 | Cây phát triển năng lực | xyflow/xyflow (38,787★) | source snapshot + structured capability DAG evidence | Interactive xyflow UI linked to live canonical registry |

Crosscut: Browserless (13,863★) browser pool candidate, source snapshot only. License check mandatory: Browserless SSPL, BrowserOS AGPL, n8n fair-code. No silently asserted FOSS rights.

## Source download policy
- **4 FULL Git checkouts on ephemeral GitHub-hosted runners:** browser-use, playwright-mcp, vercel-labs/skills, mem0. Source archived as GitHub Actions artifact.
- **7 ROOT-ONLY pinned sparse Git checkouts:** BrowserOS, OpenAdapt, Stagehand, n8n, xyflow, SkillHub, browserless. Root-only artifacts are *not* full repositories.
- Pinned commit from GitHub on 2026-10-26. Upstream stars snapshot only, not a performance ranking.
- Committing source snapshots into canonical RON-AIOS is not authorized and not attempted.

## Outcome labels
SOURCE_DOWNLOADED != INSTALLED != EXECUTED != VERIFIED != ACCEPTED.
A capability remains UNKNOWN or BLOCKED if its real upstream runtime, service, or cross-agent integration has not passed independent UAT.
