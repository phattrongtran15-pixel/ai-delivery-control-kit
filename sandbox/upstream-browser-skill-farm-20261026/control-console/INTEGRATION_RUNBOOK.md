# RON-SHO Unified Console — thực thi chuỗi OpenSpec → Skill → Verify → Gates → Lineage

**Kết nối thật hiện tại:** OpenSpec change history → candidate skill versions → verifier reference → candidate 5-Gate status → cây tương tác chạy trực tiếp trong console staging. BrowserOS/RonSkillStore: adapter discovery **chưa có endpoint/identity được kiểm chứng**, do đó công tắc hiển thị DISCONNECTED, không ngầm coi đã tích hợp. Không ghi vào canonical DB.

## Cho anh (human)
1. Mở GitHub Actions `RON Unified Control Console — staging UAT` trên nhánh staging, lấy artifact `ron-unified-control-console-preview`, mở `index.html`.
2. Trong **Phả hệ năng lực** chọn C3, mở phiên bản skill và dòng OpenSpec change `os-browser-procedural-memory-001`; bấm liên kết evidence để xem verifier run. Phiên bản `0.1.1-candidate` phải hiển thị *PROPOSED_UNVERIFIED* và không được nâng gate.
3. Trong **Browser & AI**, kiểm tra BrowserOS adapter phải ghi DISCONNECTED; không nhập token/cookie vào bản HTML offline.
4. Trong **SkillStore**, kiểm tra RonSkillStore adapter DISCONNECTED. Xác minh 5 Gates G5 HOLD; không merge production để thử nghiệm.
5. Để có kết nối BrowserOS thật: cần endpoint MCP/HTTP có cấu trúc dữ liệu, chứng thực read-only, phân tách tenant/session và host đang chạy; thử test độc lập bằng readback trước khi giao diện hiển thị ONLINE.
6. Để có kết nối RonSkillStore thật: cần địa chỉ read-only export/API hiện hành và actor authorization từ registry/PolicyGate; không tạo database thứ hai. Khi hai nguồn đã xác minh, thay JSON adapter bằng projection chuẩn, không đặt secret trong GitHub.

## Cho AI
- Đọc nguồn OpenSpec và skill_versions, kiểm tra `change_id`, version, parent_version, verifier URL/run, gate và `accepted_by_ron`.
- Không tạo cycle, không chấp nhận duplicate version hay self-parent; reject `PROPOSED_UNVERIFIED` như một skill executable.
- Xem adapter `mode`; nếu != CONNECTED_VERIFIED thì `live_status=UNKNOWN`, `integration=BLOCKED`, cấm giả định actor online.
- Lấy run hiện hành từ GitHub; chỉ gọi G4 verified khi independent receipt cùng SHA; G5 chỉ Ron có quyền.
- Trả handoff: Work/Asset ID thực hoặc UNKNOWN, git SHA, 9 tiêu chí, source references, owner decision, rollback, đúng một next action.

## Tài sản tích hợp
- `lineage/openspec_changes.json`: đề xuất thay đổi OpenSpec (không phải canonical change log).
- `lineage/skill_versions.json`: graph phiên bản skill ví dụ, nguồn run có thật.
- `adapters/browseros.json` và `adapters/ronskillstore.json`: adapter read-only fail closed.
- Console snapshot chỉ đọc; không có backend luôn online trên GitHub Actions.

## Actual upstream reconnaissance (2026-10-27)
- The real Smart SkillStore control kit exists in [RON-AIOS Draft PR #28](https://github.com/phattrongtran15-pixel/RON-AIOS/pull/28); `tooling/smart-skillstore/skillstore_ctl.py` opens existing `AIOS.db` with `mode=ro` / `query_only=ON`. `apply` remains blocked. **It is NOT a deployed HTTP service**.
- Existing canonical `skill_registry`, `policy_registry`, `capability_registry` are held in AIOS.db and must stay sole truth. Do not upload AIOS.db into GitHub or replicate it into the Console.
- BrowserOS upstream documents a local AI-centric browser and MCP connections. The Console has **no verified authenticated BrowserOS endpoint, session feed, or local agent identity**. Upstream README alone does not prove live integration.
- Integration should be delivered as signed / authenticated **read-only projections** from a trusted running RON-SHO gateway, with TTL and source/actor/tenant evidence. Browser session capture must never export real login cookies. Ron / PolicyGate acceptance is required before enabling writes.
