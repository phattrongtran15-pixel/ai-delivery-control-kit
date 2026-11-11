# RON-SHO — Semantic Asset Intelligence V2
## Hồ sơ giới thiệu dự án (tiếng Việt)

**Mục tiêu:** Biến tài sản mã nguồn trong một repository GitHub thành hồ sơ có thể truy cứu: file chứa gì, đang thực hiện chức năng kỹ thuật nào, có bằng chứng liên quan đến requirement/test nào và chỗ nào chưa biết.

**Phạm vi đã thực hiện:** PoC trên repository ai-delivery-control-kit, nhánh sandbox/semantic-asset-canary-20261111. Không quét ổ C:, không đụng Core X production, không gọi API LLM trả phí, không merge vào main.

### 1. Mở tài liệu theo thứ tự
1. [SPEC_DU_AN_VI.md](./SPEC_DU_AN_VI.md) — mục tiêu, kiến trúc, luồng dữ liệu, contract, phương pháp kiểm chứng, giới hạn và roadmap.
2. [BAO_CAO_KIEM_THU_V2_VI.md](./BAO_CAO_KIEM_THU_V2_VI.md) — kết quả GitHub Actions đã quan sát và phân loại PASS / HOLD.
3. [KE_HOACH.md](./KE_HOACH.md) — kế hoạch 5 bước, checkpoint và rollback.
4. [HANDOFF_V2_VI.md](./HANDOFF_V2_VI.md) — bàn giao kỹ thuật, người sở hữu quyết định, bước tiếp theo.

### 2. Sơ đồ luồng
Mission fixture → Requirement manifest → Git-tracked files → AST / Source Reader → Asset Profiles + Import Edges → Requirement-to-Source-to-Test Trace → Verifier độc lập về mã đọc → GitHub Actions Artifact → Ron xem xét.

### 3. Những gì đã làm được
- Kiểm kê file văn bản có trong Git, giới hạn kích thước và số lượng.
- Ghi SHA-256, đường dẫn, commit, mô tả trích từ nguồn và vị trí dòng.
- Suy luận vai trò **kỹ thuật** ở mức quy tắc AST (không nhầm với lý do file được tạo).
- Truy vết mô hình từ Requirement trong fixture tới mô tả, symbol triển khai và lời gọi test.
- Verifier tách khỏi analyzer để đối chiếu lại hash, AST, cạnh và chống report giả.
- GitHub Actions chạy unit tests và sinh artifact đọc được.

### 4. Chưa làm được
- Chưa dùng mô hình ngôn ngữ (LLM), do đó chưa phải kiểm chứng AI hiểu ngữ nghĩa sâu hoặc business purpose.
- Chưa chứng minh ý định ban đầu của tác giả, quyền sở hữu, hay nguồn gốc phê duyệt.
- Chưa nối tới tất cả file/Core X/C4/Archify trên máy.
- Chưa chứng minh hoạt động runtime/production; không được tự ACCEPT.

### 5. Xem kết quả ở đâu?
- PR nháp: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/pull/3
- GitHub Actions: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions
- Nhánh: sandbox/semantic-asset-canary-20261111
- Trong Actions mở run **RON-SHO Semantic Asset V2 GitHub-Only**, kéo xuống **Artifacts**, tải gói semantic-asset-v2-evidence.
- Bên trong artifact, mở REPORT_V2.md (mặc định tiếng Việt), REPORT_V2_VI.md (bản sao tiếng Việt), ASSET_PROFILES_V2.json, VERIFICATION_V2.json; báo cáo kỹ thuật tiếng Anh nằm tại REPORT_V2_EN.md.

### 6. Quy tắc tin cậy
**Executed ≠ Verified ≠ Accepted.** SOURCE_DECLARED là lời mô tả có trong file, không phải mục đích lịch sử đã được chứng minh. UNKNOWN khác PASS. Ron giữ quyền quyết định nghiệm thu đầu ra.

### 7. Kiểm soát thay đổi
- Baseline main: 981c88592c78e908c1ce9c39dec93fa7718c4cd4
- Nguyên tắc: chỉ sửa nhánh sandbox và workflow canary, không sửa mã ứng dụng.
- Rollback: bỏ hoặc đưa nhánh sandbox về commit checkpoint theo thay đổi đã duyệt; không dùng force trên main.
