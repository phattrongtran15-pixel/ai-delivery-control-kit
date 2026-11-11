# KẾ HOẠCH — RON-SHO SEMANTIC ASSET INTELLIGENCE V2 (GITHUB ONLY)

## I. Mission
Ron yêu cầu thực hiện một lượt trọn gói trên GitHub: kiểm kê file → đọc mô tả nội dung → suy luận vai trò kỹ thuật → nối Requirement/Source/Test → kiểm chứng độc lập theo evidence → bàn giao SPEC và REPORT bằng tiếng Việt.

## II. Phạm vi ủy quyền
- **Repo:** phattrongtran15-pixel/ai-delivery-control-kit.
- **Nhánh sandbox:** sandbox/semantic-asset-canary-20261111.
- **Main SHA checkpoint:** 981c88592c78e908c1ce9c39dec93fa7718c4cd4.
- **Sandbox trước V2:** f252688dc692ce668a060c9b78144d99c69ca082.
- **Checkpoint trước bổ sung tài liệu tiếng Việt:** 1a19aa215acb257384c28ba746b04ffb1a5a6bbf.
- **Allowed:** Chỉ sửa source canary, workflow và tài liệu trong nhánh sandbox. Không sửa code production, không merge, không tạo phí model.
- **Rollback:** Hoàn nguyên thay đổi tài liệu/workflow về sandbox checkpoint trên; chỉ dùng cập nhật ref có expected SHA khi có quyền và yêu cầu rollback riêng. Main giữ nguyên.

## III. 5 bước hành động trong một ủy quyền
1. [x] Kiểm tra GitHub repository, source, tests, existing Actions và giữ checkpoint.
2. [x] Triển khai V2 analyzer, independent verifier, fixture requirements trên nhánh sandbox; có negative test.
3. [x] Chạy GitHub Actions V2: 16 unit tests PASS, 32 files, 21 SOURCE_DECLARED, 11 UNKNOWN, 7 static imports, trace 2 PASS tĩnh / 2 HOLD, 3/3 fake evidence REJECTED.
4. [x] Soạn bộ hồ sơ VI: README, SPEC dự án, báo cáo kiểm thử, HANDOFF; thêm generator báo cáo VI trong Actions.
5. [x] Đã chạy GitHub Actions có generator tiếng Việt, tải và mở artifact, đối chiếu REPORT_V2.md/SPEC/README/HANDOFF, xác nhận CI PASS; sau bổ sung KE_HOACH.md vào artifact phải đọc ngược run cuối.

## IV. Điều kiện nghiệm thu
- GitHub Actions cuối phải SUCCESS và artifact chứa REPORT_V2.md tiếng Việt, REPORT_V2_VI.md, REPORT_V2_EN.md, SPEC_DU_AN_VI.md, BAO_CAO_KIEM_THU_V2_VI.md, README_VI.md, HANDOFF_V2_VI.md, ASSET_PROFILES_V2.json, VERIFICATION_V2.json.
- Không sửa main, không merge PR #3.
- SOURCE_ONLY_PASS không được suy ra ý định tác giả hay LLM semantic verified.
- Requirement không có đủ evidence vẫn HOLD; UNKNOWN không được suy thành PASS.

## V. Bằng chứng gốc
- PR nháp: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/pull/3
- Run V2 xác minh trước bước bổ sung tài liệu: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/42994419698
- V2 kết quả gốc: 32 file, 21 SOURCE_DECLARED, 11 UNKNOWN, 7 import; 2 STATIC_TRACE_PRESENT, 2 HOLD_INCOMPLETE_TRACE.
- Các kết quả này là snapshot đã được kiểm chứng tại run nêu trên; workflow sau thay đổi phải kiểm tra bằng run riêng.

## VI. Kết luận
- **Executed:** đã có baseline PASS cho canary mã nguồn.
- **Verified:** chỉ trên source-only.
- **Accepted:** Anh ủy quyền full execution; semantic business outcome vẫn chưa được xác minh độc lập.
- **Bước cuối:** read-back artifact tiếng Việt, giữ PR draft để review.

## VII. Bằng chứng hồ sơ tiếng Việt
- Run kiểm tra tiếng Việt: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/42996277058 (SUCCESS).
- Artifact ID: 13844256092, SHA256: 8385d88a948afb5c97660990a56b9739af28ea4818ebb70286d009a8d1432887.
- Đã mở ZIP kiểm chứng có REPORT_V2.md tiếng Việt, REPORT_V2_VI.md, SPEC_DU_AN_VI.md, BAO_CAO_KIEM_THU_V2_VI.md, README_VI.md, HANDOFF_V2_VI.md và 2 JSON evidence.
- Bản cuối bổ sung KE_HOACH.md vào artifact để hồ sơ tải xuống đầy đủ.
