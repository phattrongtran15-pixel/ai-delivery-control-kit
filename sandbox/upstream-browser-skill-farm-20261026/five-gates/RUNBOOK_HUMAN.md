# RUNBOOK HUMAN — anh thao tác trên GitHub và Drive
**Bản:** 2026-10-26 / staging. Không cần PowerShell/Windows. Hoạt động trên trình duyệt GitHub.

## A. Xem ngay bằng chứng đang có
1. Mở GitHub repo: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/tree/sandbox/upstream-browser-skill-farm-20261026
2. Mở [lượt kiểm thử Browser Intelligence](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40354279483). Chọn job `scaled-real-mcp-actors`, tìm `RON_REAL_MCP_ACTOR_FARM_PASS:48` và `RON_MCP_48_ACTOR_DASHBOARD_AND_PROVENANCE_VERIFIED`.
3. Ở mục **Artifacts**, tải `ron-mcp-actor-farm-6-12-24-48`; mở `actor-monitor-48.png`, `scale-receipt.json`.
4. Tải `ron-procedural-skill-memory`, xem `memory-actor-monitor-48.png`, `memory-48-actor-scale.json`.
5. Tải `ron-rea-archify-source-workflow`; mở HTML `ron-browser-intelligence.html` để xem luồng và `source-verify.json` kiểm tra các liên kết code.

## B. Chạy G1–G4 ở GitHub (không chạy production)
1. Mở tab **Actions** tại https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions
2. Chọn `RON Browser Five Gates — dossier verifier` → **Run workflow**.
3. Branch: `sandbox/upstream-browser-skill-farm-20261026`; chọn `verify_only`. Chỉ chạy định dạng/scope/nguồn/evidence hợp lệ, không gọi LLM trả phí.
4. Mở lượt run vừa tạo. Kiểm tra job `build-dossier` và job `independent-verify`; cần **cả hai SUCCESS**.
5. Tải artifact `ron-browser-five-gates-receipt`; đối chiếu `source_sha`, `gate_verdict.json`, `negative_tests.json`.
6. Nếu `G5=HOLD`, đó là trạng thái đúng khi chưa có Work/Asset ID và Ron ký nghiệm thu. **Không nhấn merge vào main và không sửa gate_state.json để giả tạo ACCEPTED**.

Tùy chọn bằng GitHub CLI (đã xác thực; phải có quyền `workflow_dispatch`):
```bash
gh workflow run ron-browser-five-gates.yml --repo phattrongtran15-pixel/ai-delivery-control-kit --ref 'sandbox/upstream-browser-skill-farm-20261026' -f mode=verify_only
gh run list --repo phattrongtran15-pixel/ai-delivery-control-kit --workflow ron-browser-five-gates.yml --limit 5
gh run view <REAL_RUN_ID> --repo phattrongtran15-pixel/ai-delivery-control-kit --log
gh run download <REAL_RUN_ID> --repo phattrongtran15-pixel/ai-delivery-control-kit -n ron-browser-five-gates-receipt -D ./gates-evidence
```
Chỉ thay `<REAL_RUN_ID>` bằng ID thật từ GitHub; không lấy ID ví dụ làm bằng chứng.

## C. Chạy lại bể browser 48 actor ở staging
Chọn `RON 9-capability GitHub-only staging` → **Run workflow** trên cùng branch, sau đó xem `scaled-real-mcp-actors` và `procedural-skill-memory`. Mỗi lượt dùng GitHub-hosted runner/quota; đây là 48 MCP client + 48 actor giả lập, KHÔNG 48 GPT model sống.

## D. Đọc bản đồng bộ Drive
Vào `AI_OS_TEAM/02_PROJECTS/RON_SHO_5_GATE_PRODUCT_LIFECYCLE/BROWSER_INTELLIGENCE_9CAP_5_GATES_20261026`. Drive giữ bộ hồ sơ và runbook tương ứng với commit GitHub đã ghi trong MANIFEST; **không coi Drive là phiên bản live khi SHA lệch**.

## E. Nghiệm thu G5 hoặc từ chối
- Chỉ review G5 khi có Work ID/Asset ID thật từ registrar, binding PolicyGate, kiểm thử Local+Cloud AI dùng LLM thật, license/quota, restore UAT, successor ACK và evidence SHA khớp.
- Nếu thiếu bất kỳ điều kiện nào: ghi quyết định `HOLD / REWORK`, không tự cấp quyền.
- Không dán cookie/API key/token vào Issue, Artifact, Google Drive hay runbook.

## F. Khi job FAIL
Đọc đúng bước đỏ. `GATE_VALIDATION_FAILED` nghĩa là yêu cầu/hồ sơ chưa đúng; sửa trên sandbox rồi chạy lại. `UNKNOWN` không chuyển thành `PASS`. Trước rollback, xác minh không có dữ liệu production bị tác động (workflow được thiết kế không truy cập production).