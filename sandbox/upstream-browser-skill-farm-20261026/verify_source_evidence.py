#!/usr/bin/env python3
"""Check source citation integrity of a workflow graph; no runtime claims (stdlib)."""
import argparse
import hashlib
import json
from pathlib import Path

ALLOWED = {"SOURCE_SUPPORTED", "INFERRED", "UNKNOWN"}


def validate(repo: Path, graph: dict) -> dict:
    errors = []
    root = repo.resolve(strict=True)
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if graph.get("schema_version") != "1.0" or not str(graph.get("subject", "")).strip():
        errors.append("Invalid schema version or subject")
    if not isinstance(nodes, list) or not nodes:
        errors.append("Graph must have nodes")
        nodes = []
    if not isinstance(edges, list):
        errors.append("Graph edges must be a list")
        edges = []

    ids = set()

    def check(item: object, where: str):
        if not isinstance(item, dict):
            errors.append(f"{where}: expected object")
            return
        status = item.get("status")
        evidence = item.get("evidence")
        if status not in ALLOWED:
            errors.append(f"{where}: invalid status")
        if not isinstance(evidence, list):
            errors.append(f"{where}: evidence must be list")
            return
        if status == "SOURCE_SUPPORTED" and not evidence:
            errors.append(f"{where}: missing mandatory source evidence")
        for j, ev in enumerate(evidence):
            tag = f"{where}.evidence[{j}]"
            if not isinstance(ev, dict):
                errors.append(f"{tag}: invalid object")
                continue
            p = ev.get("path")
            a, b, digest = ev.get("start"), ev.get("end"), ev.get("sha256")
            if not isinstance(p, str) or not p or Path(p).is_absolute() or "\\" in p:
                errors.append(f"{tag}: path not repository-relative")
                continue
            f = (root / p).resolve()
            if f == root or root not in f.parents:
                errors.append(f"{tag}: path escapes repo")
                continue
            if not f.is_file():
                errors.append(f"{tag}: missing file")
                continue
            if type(a) is not int or type(b) is not int or not (1 <= a <= b):
                errors.append(f"{tag}: bad line range")
                continue
            if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                errors.append(f"{tag}: invalid digest")
                continue
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
            except (UnicodeError, OSError):
                errors.append(f"{tag}: invalid utf8/read failure")
                continue
            if b > len(lines):
                errors.append(f"{tag}: lines out of range")
                continue
            actual = hashlib.sha256("\n".join(lines[a-1:b]).encode("utf-8")).hexdigest()
            if digest != actual:
                errors.append(f"{tag}: hash mismatch")

    for i, node in enumerate(nodes):
        check(node, f"nodes[{i}]")
        if not isinstance(node, dict):
            continue
        key = node.get("id")
        if not isinstance(key, str) or not key.strip() or key in ids:
            errors.append(f"nodes[{i}]: invalid/duplicate id")
        else:
            ids.add(key)
    for i, edge in enumerate(edges):
        check(edge, f"edges[{i}]")
        if isinstance(edge, dict) and (edge.get("from") not in ids or edge.get("to") not in ids):
            errors.append(f"edges[{i}]: dangling endpoint")
    return {"status": "PASS" if not errors else "FAIL", "checks": len(nodes) + len(edges), "errors": errors,
            "scope": "source-citation-integrity-only; not runtime or semantic verification"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--graph", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    args = p.parse_args()
    try:
        graph = json.loads(args.graph.read_text(encoding="utf-8"))
        if not isinstance(graph, dict):
            raise ValueError("graph must be object")
        result = validate(args.repo_root, graph)
    except (OSError, ValueError) as err:
        result = {"status": "FAIL", "checks": 0, "errors": [str(err)]}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()
