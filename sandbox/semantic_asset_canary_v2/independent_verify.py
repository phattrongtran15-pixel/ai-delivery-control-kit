#!/usr/bin/env python3
"""Independent read-back of source, test, and evidence, without analyzer imports."""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import subprocess
from pathlib import Path


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def tracked_paths(root):
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    return {x.decode("utf-8", "replace") for x in raw.split(b"\0") if x}


def verify(payload, manifest, root):
    """Return explicit findings for each independently re-evaluated assertion."""
    issues = []
    tracked = tracked_paths(root)
    head = git(root, "rev-parse", "HEAD")
    if payload.get("repo_commit") != head:
        issues.append("COMMIT_MISMATCH")
    if payload.get("mission_id") != manifest.get("mission_id"):
        issues.append("MISSION_MISMATCH")
    if payload.get("human_accepted") is not False or payload.get("llm_invoked") is not False:
        issues.append("FALSE_ACCEPTANCE_OR_MODEL_CLAIM")
    source_index = {}
    for profile in payload["profiles"]:
        rel = profile["path"]
        if rel not in tracked or rel.startswith("/") or ".." in Path(rel).parts:
            issues.append("OUT_OF_SCOPE_FILE:" + rel)
            continue
        file = root / rel
        if file.is_symlink() or not file.is_file():
            issues.append("NONREGULAR_FILE:" + rel)
            continue
        content = file.read_bytes()
        sha = hashlib.sha256(content).hexdigest()
        if sha != profile["sha256"]:
            issues.append("HASH_MISMATCH:" + rel)
        if profile["commit"] != head:
            issues.append("PROFILE_COMMIT_MISMATCH:" + rel)
        if profile.get("original_creator_intent") != "UNKNOWN" or profile.get("human_accepted") is not False:
            issues.append("UNSUPPORTED_INTENT_OR_ACCEPTANCE:" + rel)
        text = content.decode("utf-8", "replace")
        lines = text.splitlines()
        line_no = profile.get("claim_line")
        if profile["claim_state"] == "SOURCE_DECLARED":
            if not isinstance(line_no, int) or not 1 <= line_no <= len(lines):
                issues.append("MISSING_SOURCE_LINE:" + rel)
        elif profile["claim_state"] != "UNKNOWN":
            issues.append("ILLEGAL_CLAIM_STATE:" + rel)
        source_index[rel] = (text, profile)

    manifest_index = {x["id"]: x for x in manifest["requirements"]}
    traces = payload["requirement_traces"]
    if {t["requirement_id"] for t in traces} != set(manifest_index):
        issues.append("REQUIREMENT_SET_MISMATCH")
    for trace in traces:
        rid = trace["requirement_id"]
        if rid not in manifest_index:
            issues.append("UNKNOWN_REQ:" + rid)
            continue
        expected = manifest_index[rid]
        doc = expected["evidence_document"]
        src = expected["implementation"]
        if trace["source_evidence"]["path"] != src["path"]:
            issues.append("SOURCE_PATH_MISMATCH:" + rid)
        if trace["source_evidence"]["symbol"] != src["symbol"]:
            issues.append("SOURCE_SYMBOL_MISMATCH:" + rid)
        target = root / src["path"]
        symbol_line = None
        if src["path"] in tracked and target.is_file():
            try:
                tree = ast.parse(target.read_text(encoding="utf-8"))
                symbol_line = next((x.lineno for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and x.name == src["symbol"]), None)
            except SyntaxError:
                pass
        if trace["source_evidence"]["line"] != symbol_line:
            issues.append("SYMBOL_LINE_MISMATCH:" + rid)
        if symbol_line:
            actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            if trace["source_evidence"]["sha256"] != actual_hash:
                issues.append("TRACE_FILE_HASH_MISMATCH:" + rid)

        doc_line = None
        if doc["path"] in tracked:
            for i, line in enumerate((root / doc["path"]).read_text(encoding="utf-8").splitlines(), 1):
                if doc["contains"].casefold() in line.casefold():
                    doc_line = i
                    break
        if trace["document_evidence"]["path"] != doc["path"] or trace["document_evidence"]["line"] != doc_line:
            issues.append("DOCUMENT_ANCHOR_MISMATCH:" + rid)

        test = expected.get("test")
        test_match = None
        if test and test["path"] in tracked:
            try:
                tree = ast.parse((root / test["path"]).read_text(encoding="utf-8"))
                for item in ast.walk(tree):
                    if isinstance(item, ast.FunctionDef) and item.name == test["test"]:
                        calls = [n.lineno for n in ast.walk(item)
                                 if isinstance(n, ast.Call)
                                 and ((isinstance(n.func, ast.Name) and n.func.id == src["symbol"])
                                      or (isinstance(n.func, ast.Attribute) and n.func.attr == src["symbol"]))]
                        if calls:
                            test_match = (item.lineno, calls[0])
                            break
            except SyntaxError:
                pass
        result_test = trace.get("test_evidence")
        if test_match:
            if not result_test or result_test.get("test_path") != test["path"] or result_test.get("test") != test["test"] or result_test.get("call_line") != test_match[1]:
                issues.append("TEST_CALL_MISMATCH:" + rid)
        elif result_test is not None:
            issues.append("FABRICATED_TEST_LINK:" + rid)
        expected_gates = {"document_anchor": "FOUND" if doc_line else "MISSING",
                          "source_symbol": "FOUND" if symbol_line else "MISSING",
                          "test_call": "FOUND" if test_match else "MISSING"}
        if trace["gates"] != expected_gates:
            issues.append("GATE_MISMATCH:" + rid)
        expected_state = "STATIC_TRACE_PRESENT" if all(v == "FOUND" for v in expected_gates.values()) else "HOLD_INCOMPLETE_TRACE"
        if trace["state"] != expected_state:
            issues.append("FALSE_TRACE_PASS:" + rid)
        if trace.get("accepted") is not False:
            issues.append("AUTO_ACCEPT_NOT_ALLOWED:" + rid)

    for edge in payload["static_import_edges"]:
        origin = edge["from"]
        target = edge["to"]
        line = edge["line"]
        if origin not in source_index or target not in tracked:
            issues.append("UNSUPPORTED_EDGE_PATH")
            continue
        code = source_index[origin][0].splitlines()
        if not isinstance(line, int) or line < 1 or line > len(code) or not code[line-1].lstrip().startswith(("import ", "from ")):
            issues.append("EDGE_LINE_NOT_IMPORT:" + origin)
        if edge.get("runtime_verified") is not False:
            issues.append("UNSUPPORTED_RUNTIME_CLAIM")
    return issues


def run(root, manifest_path, artifact_dir):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    path = artifact_dir / "ASSET_PROFILES_V2.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    problems = verify(report, manifest, root)
    assert not problems, "Independent verification failed: " + repr(problems)
    # Adversarial checks must FAIL on tampered evidence.
    tampered = copy.deepcopy(report)
    tampered["profiles"][0]["sha256"] = "0" * 64
    assert any("HASH_MISMATCH" in s for s in verify(tampered, manifest, root))
    tampered_trace = copy.deepcopy(report)
    missing = next(x for x in tampered_trace["requirement_traces"] if x["state"] == "HOLD_INCOMPLETE_TRACE")
    missing["state"] = "STATIC_TRACE_PRESENT"
    assert any("FALSE_TRACE_PASS" in s for s in verify(tampered_trace, manifest, root))
    tampered_acceptance = copy.deepcopy(report)
    tampered_acceptance["human_accepted"] = True
    assert "FALSE_ACCEPTANCE_OR_MODEL_CLAIM" in verify(tampered_acceptance, manifest, root)
    audit = {
        "status": "PASS_SOURCE_ONLY",
        "independent_method": "SEPARATE_READER_AST_HASH_RECHECK",
        "verified_profiles": len(report["profiles"]),
        "verified_requirements": len(report["requirement_traces"]),
        "verified_static_edges": len(report["static_import_edges"]),
        "negative_checks": {"tampered_sha": "REJECTED",
                            "fake_static_trace": "REJECTED", "fake_acceptance": "REJECTED"},
        "original_intent": "UNKNOWN",
        "llm_semantic_understanding": "NOT_TESTED",
        "deployed_runtime": "NOT_TESTED",
        "human_acceptance": "NOT_ACCEPTED",
        "errors": []
    }
    (artifact_dir / "VERIFICATION_V2.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print("INDEPENDENT_SOURCE_RECHECK=PASS")
    print("ADVERSARIAL_NEGATIVES=3/3 REJECTED")
    print("V2_VERIFICATION=" + json.dumps({k: v for k, v in audit.items() if k in ("status", "verified_profiles", "verified_requirements", "verified_static_edges")}))
    print("V2_NOT_AUTO_ACCEPTED")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="sandbox/semantic_asset_canary_v2/requirements.json")
    ap.add_argument("--artifact-dir", default="out/semantic-asset-v2")
    args = ap.parse_args()
    run(Path.cwd(), Path(args.manifest), Path(args.artifact_dir))
