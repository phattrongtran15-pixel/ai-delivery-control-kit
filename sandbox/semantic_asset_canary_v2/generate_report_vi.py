#!/usr/bin/env python3
"""Sinh báo cáo tiếng Việt từ artifact đã được verifier độc lập về mã nguồn xác minh.

Tác vụ trình bày, không chạy mô hình ngôn ngữ; không tự suy diễn mục đích tác giả.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Artifact không phải JSON object")
    return data


def clean(value) -> str:
    return " ".join(str(value).split()).replace("|", "/")[:300]


def generate(folder: Path, repo_docs: Path) -> None:
    raw = folder / "ASSET_PROFILES_V2.json"
    verified = folder / "VERIFICATION_V2.json"
    previous = folder / "REPORT_V2.md"
    if not all(path.is_file() for path in (raw, verified, previous)):
        raise FileNotFoundError("Thiếu artifact analyzer/verifier")
    data = read_json(raw)
    audit = read_json(verified)
    if audit.get("status") != "PASS_SOURCE_ONLY" or audit.get("errors") != []:
        raise ValueError("Verifier chưa đạt PASS_SOURCE_ONLY")
    profiles = data.get("profiles", [])
    traces = data.get("requirement_traces", [])
    edges = data.get("static_import_edges", [])
    if len(profiles) != audit.get("verified_profiles"):
        raise ValueError("Số profile không khớp verifier")
    if len(traces) != audit.get("verified_requirements"):
        raise ValueError("Số requirement không khớp verifier")
    if len(edges) != audit.get("verified_static_edges"):
        raise ValueError("Số cạnh không khớp verifier")
    if data.get("human_accepted") is not False or data.get("llm_invoked") is not False:
        raise ValueError("Không được báo cáo đã nghiệm thu hoặc đã sử dụng LLM")
    states = data.get("claim_states", {})
    if sum(states.values()) != len(profiles):
        raise ValueError("Tổng trạng thái file không khớp")

    header = [
        "# RON-SHO — BÁO CÁO KIỂM THỬ FILE INTELLIGENCE V2 (TIẾNG VIỆT)",
        "",
        "**Loại bằng chứng:** GitHub Actions, kiểm thử nguồn tĩnh; chưa kiểm thử AI hiểu ngữ nghĩa sâu.",
        "",
        "## 1. Kết quả tổng quan",
        "- **Commit đang được kiểm tra:** " + clean(data.get("repo_commit", "UNKNOWN")),
        "- **Mission fixture:** " + clean(data.get("mission_id", "UNKNOWN")),
        "- **Số file đã đọc:** " + str(len(profiles)),
        "- **Có mô tả khai báo trong nguồn:** " + str(states.get("SOURCE_DECLARED", 0)),
        "- **File chưa rõ mô tả:** " + str(states.get("UNKNOWN", 0)),
        "- **Cạnh import Python tĩnh:** " + str(len(edges)),
        "- **Requirement fixture:** " + str(len(traces)),
        "- **Verifier:** " + clean(audit["status"]),
        "- **Ca giả mạo đã bị bác bỏ:** " + clean(audit.get("negative_checks", {})),
        "- **LLM phân tích:** KHÔNG; phân tích theo AST và quy tắc có giới hạn.",
        "- **Mục đích lịch sử của tác giả:** UNKNOWN.",
        "- **Trạng thái runtime Core X:** NOT_TESTED.",
        "- **Quyền nghiệm thu:** Ron; không tự ACCEPT.",
        "",
        "## 2. Truy vết Requirement → Tài liệu → File → Test",
        "",
        "| Yêu cầu | File/source symbol | Bằng chứng test | Trạng thái |",
        "|---|---|---|---|",
    ]
    for trace in traces:
        src = trace.get("source_evidence", {})
        test = trace.get("test_evidence") or {}
        header.append(
            "| " + clean(trace.get("requirement_id", "UNKNOWN")) +
            " | " + clean(src.get("path", "?")) + ":" + clean(src.get("symbol", "?")) +
            " | " + clean(test.get("test", "THIẾU")) +
            " | " + clean(trace.get("state", "UNKNOWN")) + " |"
        )
    header.extend([
        "",
        "**Diễn giải:** STATIC_TRACE_PRESENT chỉ nghĩa là đã tìm thấy liên kết tĩnh giữa tài liệu, symbol và lời gọi test; không tự chứng minh test đúng hoặc hành vi production. HOLD_INCOMPLETE_TRACE = thiếu ít nhất một mắt xích.",
        "",
        "## 3. Hồ sơ file và bằng chứng nguồn",
        "",
        "| File | Phân loại mô tả | Mô tả tìm thấy | Dòng |",
        "|---|---|---|---|",
    ])
    for item in profiles:
        header.append(
            "| " + clean(item.get("path", "?")) +
            " | " + clean(item.get("claim_state", "UNKNOWN")) +
            " | " + clean(item.get("description", "UNKNOWN")) +
            " | " + clean(item.get("claim_line") if item.get("claim_line") is not None else "—") + " |"
        )
    header.extend([
        "",
        "## 4. Đối chiếu độc lập và kiểm thử chống kết luận giả",
        "- **Phương pháp:** " + clean(audit.get("independent_method", "UNKNOWN")),
        "- **Profile đọc lại:** " + str(audit.get("verified_profiles", "UNKNOWN")),
        "- **Requirement đọc lại:** " + str(audit.get("verified_requirements", "UNKNOWN")),
        "- **Cạnh tĩnh đọc lại:** " + str(audit.get("verified_static_edges", "UNKNOWN")),
        "- **Tampered SHA:** " + clean(audit.get("negative_checks", {}).get("tampered_sha", "UNKNOWN")),
        "- **Fake PASS trace:** " + clean(audit.get("negative_checks", {}).get("fake_static_trace", "UNKNOWN")),
        "- **Fake Human ACCEPT:** " + clean(audit.get("negative_checks", {}).get("fake_acceptance", "UNKNOWN")),
        "",
        "## 5. Giới hạn và điều kiện nghiệm thu",
        "1. SOURCE_DECLARED = văn bản khai báo trong file; không phải mục đích tác giả đã được chứng thực.",
        "2. INFERENCE kỹ thuật = suy luận theo AST/đường dẫn; không phải business-purpose verified.",
        "3. Trích xuất import và test-call không chứng minh rằng nhánh mã đó đã chạy trên production.",
        "4. Không kết luận Core X có kết nối thật với các file trong repo này.",
        "5. Báo cáo nguồn PASS không tự đồng nghĩa Ron đã ACCEPT semantic Mission.",
        "",
        "## 6. Điều hướng",
        "- SPEC dự án: SPEC_DU_AN_VI.md (cùng artifact).",
        "- Báo cáo đối chiếu theo run trước: BAO_CAO_KIEM_THU_V2_VI.md (cùng artifact).",
        "- Hồ sơ JSON: ASSET_PROFILES_V2.json.",
        "- Kết quả verifier: VERIFICATION_V2.json.",
        "",
        "**KẾT LUẬN:** PASS_SOURCE_ONLY; ORIGINAL_PURPOSE_UNKNOWN; LLM_NOT_TESTED; CORE_X_NOT_TESTED.",
        "",
    ])
    content = "\n".join(header)
    shutil.copyfile(previous, folder / "REPORT_V2_EN.md")
    previous.write_text(content, encoding="utf-8")
    (folder / "REPORT_V2_VI.md").write_text(content, encoding="utf-8")
    for filename in ("SPEC_DU_AN_VI.md", "BAO_CAO_KIEM_THU_V2_VI.md", "README_VI.md", "HANDOFF_V2_VI.md", "KE_HOACH.md"):
        source = repo_docs / filename
        if not source.is_file():
            raise FileNotFoundError(str(source))
        shutil.copyfile(source, folder / filename)
    assert "TIẾNG VIỆT" in previous.read_text(encoding="utf-8")
    print("VI_REPORT_GENERATED=" + str(previous))
    print("VI_REPORT_ASSET_ROWS=" + str(len(profiles)))
    print("SPEC_INCLUDED=" + str((folder / "SPEC_DU_AN_VI.md").is_file()))
    print("VI_REPORT_STATUS=SOURCE_ONLY_NOT_ACCEPTED")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-dir", default="out/semantic-asset-v2")
    ap.add_argument("--docs-dir", default="sandbox/semantic_asset_canary_v2")
    args = ap.parse_args()
    generate(Path(args.artifact_dir), Path(args.docs_dir))
