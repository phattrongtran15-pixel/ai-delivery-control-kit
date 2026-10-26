# RUNBOOK HUMAN — anh thao tác trên GitHub và Drive
**Bản:** 2026-10-26 / staging. Không cần PowerShell/Windows. Hoạt động trên trình duyệt GitHub.

## A. Xem ngay bằng chứng đang có
1. Mở GitHub repo: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/tree/sandbox/upstream-browser-skill-farm-20261026
2. Mở [lượt kiểm thử Browser Intelligence](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40354279483). Chọn job `scaled-real-mcp-actors`, tìm `RON_REAL_MCP_ACTOR_FARM_PASS:48` và `RON_MCP_48_ACTOR_DASHBOARD_AND_PROVENANCE_VERIFIED`.
3. Ở mục **Artifacts**, tải `ron-mcp-actor-farm-6-12-24-48`; mở `actor-monitor-48.png`, `scale-receipt.json`.
4. Tải `ron-procedural-skill-memory`, xem `memory-actor-monitor-48.png`, `memory-48-actor-scale.json`.
5. Tải `ron-rea-archify-source-workflow`; mở HTML `ron-browser-intelligence.html` để xem luồng và `source-verify.json` kiểm tra các liên kết code.

## B. Chạy lại G1–G4 ở GitHub (không chạy production)
**Lưu ý quan trọng:** workflow hiện chỉ nằm trên nhánh staging. Theo quy tắc GitHub, nút **Run workflow** có thể chưa xuất hiện vì `workflow_dispatch` yêu cầu file workflow tồn tại trên nhánh mặc định. KHÔNG merge vào main chỉ để có nút.
1. Mở [GitHub run Five Gates 40358101487](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40358101487).
2. Nhấn **Re-run jobs → Re-run all jobs** (nếu tài khoản có quyền). Cách này lặp lại đúng commit đã kiểm chứng, KHÔNG chạy commit mới.
3. Kiểm tra hai job `build-dossier` và `independent-verify` đều SUCCESS; tải artifact `ron-five-gates-builder` (builder-receipt.json, negative-tests.json, likec4-validate.json) và `ron-browser-five-gates-receipt` (independent-verdict.json).
4. So sánh `source_sha` giữa builder và independent verifier. `G5=HOLD` là trạng thái đúng cho đến khi Ron nghiệm thu có quyền.
5. Để chạy **commit staging mới nhất**, phải có thay đổi đã phê duyệt trên nhánh staging; `push` vào đúng đường dẫn trong workflow sẽ tự kích hoạt CI mới.

GitHub CLI (đã xác thực, có quyền Actions):
```bash
gh run rerun 40358101487 --repo phattrongtran15-pixel/ai-delivery-control-kit
gh run list --repo phattrongtran15-pixel/ai-delivery-control-kit --workflow ron-browser-five-gates.yml --limit 5
gh run view <REAL_RUN_ID> --repo phattrongtran15-pixel/ai-delivery-control-kit --log
gh run download <REAL_RUN_ID> --repo phattrongtran15-pixel/ai-delivery-control-kit -n ron-browser-five-gates-receipt -D ./gates-evidence
```
Chỉ dùng `gh workflow run` sau khi workflow đã tồn tại trên default branch bằng một thay đổi được duyệt riêng. Không thay ID thật bằng số bịa đặt.

## C. Chạy lại bể browser 48 actor ở staging
Mở [run browser 40354279483](https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/40354279483) và chọn **Re-run jobs → Re-run all jobs** (hoặc `gh run rerun 40354279483 --repo phattrongtran15-pixel/ai-delivery-control-kit`); sau đó xem `scaled-real-mcp-actors` và `procedural-skill-memory`. Mỗi lượt dùng GitHub-hosted runner/quota; đây là 48 MCP client + 48 actor giả lập, KHÔNG 48 GPT model sống.

## D. Đọc bản đồng bộ Drive
Mở [thư mục Drive đồng bộ](https://drive.google.com/drive/folders/1hK3uifKYpbQqO1ekzmhFtQ1zP2a1exDf): `AI_OS_TEAM/02_PROJECTS/RON_SHO_5_GATE_PRODUCT_LIFECYCLE/BROWSER_INTELLIGENCE_9CAP_5_GATES_20261026`. Drive giữ bộ hồ sơ và runbook tương ứng với commit GitHub đã ghi trong MANIFEST; **không coi Drive là phiên bản live khi SHA lệch**.

## E. Nghiệm thu G5 hoặc từ chối
- Chỉ review G5 khi có Work ID/Asset ID thật từ registrar, binding PolicyGate, kiểm thử Local+Cloud AI dùng LLM thật, license/quota, restore UAT, successor ACK và evidence SHA khớp.
- Nếu thiếu bất kỳ điều kiện nào: ghi quyết định `HOLD / REWORK`, không tự cấp quyền.
- Không dán cookie/API key/token vào Issue, Artifact, Google Drive hay runbook.

## F. Khi job FAIL
Đọc đúng bước đỏ. `GATE_VALIDATION_FAILED` nghĩa là yêu cầu/hồ sơ chưa đúng; sửa trên sandbox rồi chạy lại. `UNKNOWN` không chuyển thành `PASS`. Trước rollback, xác minh không có dữ liệu production bị tác động (workflow được thiết kế không truy cập production).