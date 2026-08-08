"""Work Package contract validation."""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = {
    "work_package_id",
    "objective",
    "owner",
    "owner_hours_required",
    "inputs",
    "output",
    "acceptance",
    "evidence",
    "next_action",
    "protected_actions",
}


def validate_work_package(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS.difference(data))
    if missing:
        errors.append("MISSING_FIELDS: " + ", ".join(missing))

    owner_hours = data.get("owner_hours_required")
    if isinstance(owner_hours, bool) or not isinstance(owner_hours, (int, float)):
        errors.append("OWNER_HOURS_REQUIRED_MUST_BE_NUMBER")
    elif owner_hours < 0:
        errors.append("OWNER_HOURS_REQUIRED_MUST_BE_NON_NEGATIVE")

    protected = data.get("protected_actions")
    if not isinstance(protected, list):
        errors.append("PROTECTED_ACTIONS_MUST_BE_LIST")
    elif protected and not str(data.get("ron_approval_reference", "")).strip():
        errors.append("RON_APPROVAL_REFERENCE_REQUIRED")

    for field in ("work_package_id", "objective", "owner", "output", "acceptance", "next_action"):
        if field in data and not str(data[field]).strip():
            errors.append(f"{field.upper()}_MUST_NOT_BE_EMPTY")

    for field in ("inputs", "evidence"):
        if field in data and not isinstance(data[field], list):
            errors.append(f"{field.upper()}_MUST_BE_LIST")

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_version": "FINITE-WORK-PACKAGE-VALIDATION-v1",
        "work_package_id": data.get("work_package_id", "UNKNOWN"),
        "status": status,
        "errors": errors,
        "owner_hours_required": owner_hours if isinstance(owner_hours, (int, float)) and not isinstance(owner_hours, bool) else None,
    }
