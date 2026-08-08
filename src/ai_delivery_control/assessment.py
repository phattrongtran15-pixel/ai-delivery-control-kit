"""Deterministic Gateway-necessity assessment.

The model intentionally uses observable signals instead of a maturity
percentage. It is a planning aid, not a security certification.
"""

from __future__ import annotations

from typing import Any


VALID_STAGES = {"pre_value", "early_value", "scaling", "enterprise"}


def _non_negative_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key, 0)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{key} must be a non-negative integer")
    return value


def _boolean(data: dict[str, Any], key: str) -> bool:
    value = data.get(key, False)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a boolean")
    return value


def assess_gateway_need(data: dict[str, Any]) -> dict[str, Any]:
    """Return an evidence-aware control recommendation.

    A verified incident or confirmed external requirement can justify a
    Gateway at any stage. Otherwise, centralization is recommended only when
    multiple shared-policy signals exist. Accepted value is treated as a
    sequencing signal, never as permission to weaken protected-action gates.
    """

    project_id = str(data.get("project_id", "")).strip()
    if not project_id:
        raise ValueError("project_id is required")

    stage = str(data.get("stage", "")).strip()
    if stage not in VALID_STAGES:
        raise ValueError(f"stage must be one of {sorted(VALID_STAGES)}")

    active_agents = _non_negative_int(data, "active_agents")
    independent_teams = _non_negative_int(data, "independent_teams")
    shared_policy_surfaces = _non_negative_int(data, "shared_policy_surfaces")
    accepted_value_events = _non_negative_int(data, "accepted_value_events")

    protected_actions = _boolean(data, "protected_actions")
    multi_tenant = _boolean(data, "multi_tenant")
    regulated_data = _boolean(data, "regulated_or_high_sensitivity_data")
    enterprise_requirement = _boolean(data, "confirmed_enterprise_requirement")
    inline_incident = _boolean(data, "verified_inline_control_incident")

    signals: list[str] = []
    score = 0

    if active_agents >= 10:
        score += 2
        signals.append("TEN_OR_MORE_ACTIVE_AGENTS")
    if independent_teams >= 2:
        score += 2
        signals.append("MULTIPLE_INDEPENDENT_TEAMS")
    if shared_policy_surfaces >= 3:
        score += 2
        signals.append("THREE_OR_MORE_SHARED_POLICY_SURFACES")
    if multi_tenant:
        score += 3
        signals.append("MULTI_TENANT_BOUNDARY")
    if regulated_data:
        score += 2
        signals.append("REGULATED_OR_HIGH_SENSITIVITY_DATA")
    if accepted_value_events >= 3:
        score += 1
        signals.append("REPEATED_ACCEPTED_VALUE")
    if enterprise_requirement:
        score += 4
        signals.append("CONFIRMED_ENTERPRISE_REQUIREMENT")
    if inline_incident:
        score += 4
        signals.append("VERIFIED_INLINE_CONTROL_INCIDENT")

    evidence_gaps: list[str] = []
    if accepted_value_events == 0:
        evidence_gaps.append("NO_ACCEPTED_VALUE_EVIDENCE")
    if not signals:
        evidence_gaps.append("NO_CENTRALIZATION_SIGNAL")

    if enterprise_requirement or inline_incident:
        decision = "GATEWAY_JUSTIFIED"
        reason = "A direct, verified trigger exists. Scope the Gateway to that trigger."
    elif score >= 7 and accepted_value_events >= 1:
        decision = "CENTRAL_GATEWAY_CANDIDATE"
        reason = "Scale and shared-policy signals justify a bounded Gateway pilot."
    elif score >= 4:
        decision = "CENTRAL_POLICY_CANDIDATE"
        reason = "Central policy evaluation may reduce duplicated controls; a network chokepoint is not yet proven necessary."
    else:
        decision = "INLINE_CONTROLS_FIRST"
        reason = "Current signals support scoped capabilities, inline checks, evidence, and human approval before centralization."

    required_controls = [
        "SCOPED_CAPABILITIES",
        "EVIDENCE_LOG",
        "VERIFICATION_BEFORE_DONE",
        "RESTORE_PATH",
    ]
    if protected_actions:
        required_controls.append("RON_APPROVAL_FOR_PROTECTED_ACTIONS")
    if regulated_data:
        required_controls.extend(["DATA_CLASSIFICATION", "LEAST_PRIVILEGE"])

    return {
        "schema_version": "AI-DELIVERY-CONTROL-ASSESSMENT-v1",
        "project_id": project_id,
        "stage": stage,
        "decision": decision,
        "reason": reason,
        "signal_score": score,
        "signals": signals,
        "required_controls": sorted(set(required_controls)),
        "evidence_gaps": evidence_gaps,
        "claim_boundary": "DECISION_AID_NOT_SECURITY_CERTIFICATION",
    }
