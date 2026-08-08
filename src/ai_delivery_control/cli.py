"""Command-line interface for AI Delivery Control Kit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from .assessment import assess_gateway_need
from .work_package import validate_work_package


def _load_json(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input JSON must be an object")
    return payload


def _write_result(result: dict[str, Any], output: str | None) -> None:
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def _run(handler: Callable[[dict[str, Any]], dict[str, Any]], input_path: str, output: str | None) -> int:
    try:
        result = handler(_load_json(input_path))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 2
    _write_result(result, output)
    return 1 if result.get("status") == "FAIL" else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-delivery-control")
    sub = parser.add_subparsers(dest="command", required=True)

    assess = sub.add_parser("assess", help="Assess whether a centralized Gateway is justified")
    assess.add_argument("input", help="Project assessment JSON")
    assess.add_argument("--output", help="Optional output JSON path")

    validate = sub.add_parser("validate-work-package", help="Validate a finite Work Package JSON")
    validate.add_argument("input", help="Work Package JSON")
    validate.add_argument("--output", help="Optional output JSON path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "assess":
        return _run(assess_gateway_need, args.input, args.output)
    return _run(validate_work_package, args.input, args.output)
