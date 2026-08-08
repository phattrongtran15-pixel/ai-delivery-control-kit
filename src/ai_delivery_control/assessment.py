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
    peak_concurrent_agents = _non_negative_int(data, "peak_concurrent_agents")
    independent_teams = _non_negative_int(data, "independent_teams")
    shared_policy_surfaces = _non_negative_int(data, "shared_policy_surfaces")
    accepted_value_events = _non_negative_int(data, "accepted_value_events")

    protected_actions = _boolean(data, "protected_actions")
    multi_tenant = _boolean(data, "multi_tenant")
    regulated_data = _boolean(data, "regulated_or_high_sensitivity_data")
    enterprise_requirement = _boolean(data, "confirmed_enterprise_requirement")
    inline_incident = _boolean(data, "verified_inline_control_incident")
    concurrency_incident = _boolean(data, "verified_concurrency_contention")
    reusable_gateway_assets = _boolean(data, "reusable_gateway_assets")
    identity_required = _boolean(data, "machine_or_agent_identity_required")
    designated_folder_required = _boolean(data, "designated_folder_enforcement_required")
    inter_agent_exchange = _boolean(data, "inter_agent_data_exchange")
    untrusted_inbox_content = _boolean(data, "untrusted_inbox_content")
    downstream_binding_verified = _boolean(data, "downstream_execution_binding_verified")
    business_demand_verified = _boolean(data, "business_demand_verified")
    gateway_budget_approved = _boolean(data, "gateway_resource_budget_approved")

    signals: list[str] = []
    score = 0

    if active_agents >= 50:
        score += 2
        signals.append("FIFTY_OR_MORE_ACTIVE_AGENTS")
    if peak_concurrent_agents >= 2:
        score += 2
        signals.append("CONCURRENT_AGENT_EXECUTION")
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
    if concurrency_incident:
        score += 4
        signals.append("VERIFIED_CONCURRENCY_CONTENTION")

    evidence_gaps: list[str] = []
    if accepted_value_events == 0:
        evidence_gaps.append("NO_ACCEPTED_VALUE_EVIDENCE")
    if active_agents <= 1 and peak_concurrent_agents <= 1:
        evidence_gaps.append("SINGLE_AGENT_NO_CONCURRENCY_EVIDENCE")
    if not signals:
        evidence_gaps.append("NO_CENTRALIZATION_SIGNAL")

    if enterprise_requirement or inline_incident or concurrency_incident:
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

    activation_blockers: list[str] = []
    if decision == "INLINE_CONTROLS_FIRST":
        activation_state = "HOLD_NO_CURRENT_NEED"
    else:
        if not downstream_binding_verified:
            activation_blockers.append("DOWNSTREAM_EXECUTION_BINDING_NOT_VERIFIED")
        if not business_demand_verified:
            activation_blockers.append("BUSINESS_DEMAND_NOT_VERIFIED")
        if not gateway_budget_approved:
            activation_blockers.append("GATEWAY_RESOURCE_BUDGET_NOT_APPROVED")
        activation_state = "READY_FOR_BOUNDED_PILOT" if not activation_blockers else "HOLD_ACTIVATION_BLOCKERS"

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
    if identity_required:
        required_controls.extend(["AUTHENTICATED_AGENT_IDENTITY", "CALLER_IDENTITY_NOT_SELF_ASSERTED"])
    if designated_folder_required:
        required_controls.extend(["DESIGNATED_PATH_BOUNDARY", "PATH_NORMALIZATION", "DEFAULT_DENY_OUTSIDE_ALLOWED_ROOTS"])
    if inter_agent_exchange:
        required_controls.extend(["MESSAGE_PROVENANCE", "INBOX_SCHEMA_VALIDATION", "IDEMPOTENCY_KEY"])
    if untrusted_inbox_content:
        required_controls.extend(
            ["PROMPT_INJECTION_DEFENSE", "DATA_INSTRUCTION_SEPARATION", "UNTRUSTED_CONTENT_QUARANTINE"]
        )

    if reusable_gateway_assets:
        asset_disposition = "FROZEN_REUSABLE_ASSET"
        asset_reuse_actions = [
            "INVENTORY_COMMAND_CONTRACTS",
            "EXTRACT_COMMANDS_FROM_GATEWAY_RUNTIME",
            "TEST_COMMANDS_INDEPENDENTLY",
            "DO_NOT_AUTO_ACTIVATE_GATEWAY",
        ]
    else:
        asset_disposition = "NO_REUSABLE_GATEWAY_ASSET_REPORTED"
        asset_reuse_actions = []

    return {
        "schema_version": "AI-DELIVERY-CONTROL-ASSESSMENT-v1.1",
        "project_id": project_id,
        "stage": stage,
        "decision": decision,
        "reason": reason,
        "signal_score": score,
        "signals": signals,
        "required_controls": sorted(set(required_controls)),
        "evidence_gaps": evidence_gaps,
        "activation_state": activation_state,
        "activation_blockers": activation_blockers,
        "asset_disposition": asset_disposition,
        "asset_reuse_actions": asset_reuse_actions,
        "claim_boundary": "DECISION_AID_NOT_SECURITY_CERTIFICATION",
    }
