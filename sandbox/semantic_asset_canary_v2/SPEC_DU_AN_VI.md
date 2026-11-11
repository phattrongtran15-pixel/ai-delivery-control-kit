# ĐẶC TẢ DỰ ÁN — RON-SHO SEMANTIC ASSET INTELLIGENCE V2
**Loại:** Software Requirement & Architecture Specification  
**Ngôn ngữ:** Tiếng Việt  
**Trạng thái:** SOURCE-ONLY IMPLEMENTED / BUSINESS SEMANTICS NOT VERIFIED  
**Phạm vi:** GitHub Actions sandbox, repository phattrongtran15-pixel/ai-delivery-control-kit  
**Owner quyết định:** Ron (Human Sovereign)  
**Ngày lập:** 11/11/2026

## I. Vấn đề và Mission
Các hệ thống RON-SHO có nhiều tài sản file, module, schema và tài liệu. Chỉ kiểm kê đường dẫn/metadata không trả lời được: nội dung file là gì, chức năng thực tế nào được triển khai, file phục vụ yêu cầu nào, có test nào kiểm tra và thay đổi một file ảnh hưởng tới đâu.

**Mission dài hạn:** Từ một file bất kỳ có thể đi ngược lên Requirement → Mission/Blueprint và đi xuôi xuống các file, test, evidence liên quan; phân biệt rõ suy luận với sự thật đã kiểm chứng.

**Mission PoC V2 được giới hạn:** Thử quy trình trên **một repository GitHub**, dùng GitHub Actions; xuất hồ sơ file, vai trò kỹ thuật suy ra từ AST, mô tả do nguồn khai báo, các cạnh import và bảng truy vết requirement-code-test. Không hứa hiểu mục đích kinh doanh bằng LLM khi chưa hề gọi model.

## II. Người dùng và câu hỏi cần trả lời
- Ron: File này để làm gì? Ai/cái gì phụ thuộc? Có nguồn bằng chứng không? Có nên giữ/xóa/sửa không?
- Architect: Module/Function nào hiện diện trong source? Phần nào trùng hoặc thiếu so với blueprint?
- Verifier: Claim nào có hash/dòng code/contract/test? Claim nào chỉ là mô tả hoặc suy luận?

## III. Ranh giới sản phẩm
**IN SCOPE V2**
- Git-tracked text files (.py/.md/.json/.toml/.yaml/.yml); tối đa 160 file, mỗi file tối đa 250 KB.
- Đọc AST Python không thực thi mã; trích docstring, function/class, import, test_* calls.
- Đọc Markdown/JSON/TOML/YAML có giới hạn, trích mô tả được khai báo.
- Ghi SHA-256, commit Git, dòng chứa mô tả và last-file-commit.
- Liên kết fixture requirement ID tới anchor tài liệu, symbol nguồn và lời gọi test.
- Verifier là script riêng: kiểm lại source, hash, gate, test call; 3 ca tampering.
- Artifact trên Actions. Không ghi DB, không cập nhật application source.

**OUT OF SCOPE**
- Deep semantic understanding bằng LLM, business-purpose verified, quyết định ý định nguyên thủy của tác giả.
- Chạy production, đọc laptop, scan tài sản chưa đưa lên Git.
- Bản đồ C4 thực tế, phát hiện call graph xuyên ngôn ngữ, dynamic trace.
- Kết luận bảo mật/giấy phép, tự động merge hoặc auto ACCEPT.
- Sinh source ứng dụng từ bản vẽ (giai đoạn khác, chưa phải V2).

## IV. Cấu trúc thành phần
| Thành phần | Vai trò | Đầu vào | Đầu ra |
|---|---|---|---|
| requirements.json | Fixture yêu cầu có cấu trúc | 4 requirement mẫu | Mission ID + document/source/test contract |
| analyzer.py | Reader + AST graph + suy luận kỹ thuật giới hạn | Git tree, file, manifest | ASSET_PROFILES_V2.json, REPORT_V2.md gốc |
| independent_verify.py | Đọc ngược bằng logic khác; chặn claim giả | JSON, manifest, source thực | VERIFICATION_V2.json |
| generate_report_vi.py | Trình bày báo cáo kết quả bằng tiếng Việt | JSON profile + verification | REPORT_V2.md, REPORT_V2_VI.md, REPORT_V2_EN.md |
| semantic_asset_v2.yml | CI điều phối, upload artifact | Push nhánh sandbox | Logs + artifact |
| SPEC/REPORT/HANDOFF (VI) | Hợp đồng và bàn giao đọc được | Bằng chứng từng run | Hồ sơ dự án |

Luồng: Checkout source → compile/check → unit tests → analyzer → independent verifier → generator tiếng Việt → upload artifact. Tất cả hoạt động trên runner GitHub.

## V. Data contract và trạng thái
**Asset profile**
- path: đường dẫn tương đối, không phải định danh nhiệm vụ.
- commit, sha256, bytes, latest_file_commit: provenance kỹ thuật của file tại phiên kiểm tra.
- description, claim_line, claim_basis: câu mô tả và vị trí được đọc từ nguồn.
- claim_state: SOURCE_DECLARED hoặc UNKNOWN.
- technical_role, technical_role_state: vai trò kỹ thuật suy ra theo quy tắc hoặc UNKNOWN.
- original_creator_intent: UNKNOWN nếu không có hồ sơ chứng minh độc lập.
- human_accepted: false cho đến khi Ron thật sự nghiệm thu.
- python.symbols/imports/test_calls: dữ liệu AST, không phải dynamic coverage.

**Trace record**
- requirement_id, statement, mission_id.
- document_evidence: path + line + anchor.
- source_evidence: path + symbol + line + SHA-256.
- test_evidence: path + test name + source-call line khi tìm thấy.
- gates: FOUND/MISSING cho ba liên kết.
- state: STATIC_TRACE_PRESENT hoặc HOLD_INCOMPLETE_TRACE.
- accepted: false; runtime_verified không được suy từ static trace.

**Phân biệt epistemic**
- SOURCE_DECLARED = văn bản được ghi trong file, chưa kiểm chứng đúng/sai.
- INFERENCE = phân loại dựa vào tên symbol/AST, không thể coi là tác giả xác nhận.
- STATIC_TRACE_PRESENT = tìm thấy ba mắt xích tĩnh, không chứng minh test thật sự đúng mọi nhánh.
- PASS_SOURCE_ONLY = verifier xác nhận tính nhất quán nguồn/evidence trong scope.
- UNKNOWN/HOLD = thiếu bằng chứng, không được mặc định xanh.
- ACCEPTED = chỉ Ron có quyền xác nhận với evidence đủ điều kiện.

## VI. Điều kiện nghiệm thu
| Gate | Expected | Điều kiện loại |
|---|---|---|
| G0 Authority | Chạy trên nhánh sandbox có baseline SHA, main bất biến | Thay main/production |
| G1 Census | File thực trong Git, hash thật, loại symlink/binary/quá cỡ | Đếm file chưa đọc thành analyzed |
| G2 Source meaning | Mô tả có path/line, chức năng kỹ thuật phân loại là inference | Gọi mô tả là verified original purpose |
| G3 Trace | Requirement có doc/source/test với line và SHA hoặc HOLD | Thiếu mắt xích mà vẫn PASS |
| G4 Independent source check | Verifier riêng đối chiếu lại dữ liệu | Dùng chính claim analyzer làm proof |
| G5 Adversarial | Sửa hash, nâng giả trace, giả acceptance đều bị reject | Một ca giả vẫn được PASS |
| G6 Delivery | Workflow SUCCESS + artifact + báo cáo tiếng Việt | Không có artifact/file thực |

**Ghi chú:** Verifier độc lập về implementation path, nhưng cùng runner GitHub; chưa phải kiểm toán bởi bên thứ ba.

## VII. Fixture 4 yêu cầu
1. REQ-01: mô tả/đánh giá nhu cầu Gateway; kỳ vọng trace tới assessment.py và test_assessment.py.
2. REQ-02: kiểm tra Work Package và protected action; trace tới work_package.py và test_work_package.py.
3. REQ-03: lối vào CLI; mục đích đặt một test path cố ý chưa tồn tại để buộc HOLD.
4. REQ-04: chứng minh original author intent có chữ ký; symbol không tồn tại để buộc HOLD.
Hai yêu cầu 03–04 được tạo để kiểm soát false positive; không phải lỗi mà AI tự ý sửa ở V2.

## VIII. An ninh, giới hạn, tác động
- GitHub token workflow: contents:read; checkout không giữ credentials sau bước checkout.
- Chỉ đẩy file vào nhánh sandbox; runner sinh artifact riêng, không commit kết quả vào repo.
- Không gọi mạng ngoài thông qua model API; checkout/setup-python/upload-artifact vẫn là GitHub Actions do GitHub cung cấp.
- Không chạy mã từ file bị phân tích; unit tests hiện hữu của repository được chạy riêng trong scope thử nghiệm.
- Khả năng có prompt injection trong tài liệu: treat as data, không chạy instruction trong nội dung file.
- Giới hạn tài nguyên bằng số file, kích thước và timeout 8 phút.

## IX. Known gaps & roadmap hợp lý
- G1 — Hồ sơ purpose nâng cao: cần provenance từ commit/PR/issue/Work; không lấy docstring là bằng chứng ý định.
- G2 — LLM semantic canary: chỉ chạy khi có model/provider được phép và bộ ground truth do Ron xác nhận; đo false positives.
- G3 — File impact graph: link import, call, schema, API, test, deployment theo loại source.
- G4 — C4/Archify: nối graph đã kiểm chứng với blueprint trên canonical RON-SHO; không lập hệ thống sự thật thứ hai.
- G5 — Golden Work thật: evidence runtime và Human ACCEPT; không thuộc V2.

## X. Baseline và rollback
- Checkpoint main: 981c88592c78e908c1ce9c39dec93fa7718c4cd4.
- Checkpoint trước V2 của sandbox: f252688dc692ce668a060c9b78144d99c69ca082.
- V2 code commit ban đầu: bc7972955861bd197d8b3aa7278093ea30253722.
- Những cập nhật tiếng Việt chỉ trên sandbox; rollback bằng cách loại nhánh hoặc đưa sandbox về checkpoint sau khi kiểm tra lease.
- Không có quyền suy ra rằng GitHub Actions PASS = sản phẩm RON-SHO hoàn thành.

## XI. Nguồn evidence
- PR nháp: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/pull/3
- Run nguồn đầu tiên: https://github.com/phattrongtran15-pixel/ai-delivery-control-kit/actions/runs/42994419698
- File nguồn: sandbox/semantic_asset_canary_v2/analyzer.py và independent_verify.py.
- Test hiện có: tests/test_assessment.py, tests/test_work_package.py.
- Dữ liệu: sandbox/semantic_asset_canary_v2/requirements.json.
