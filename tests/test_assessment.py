import unittest

from ai_delivery_control import assess_gateway_need


def base_payload():
    return {
        "project_id": "TEST-01",
        "stage": "pre_value",
        "active_agents": 1,
        "peak_concurrent_agents": 1,
        "independent_teams": 1,
        "shared_policy_surfaces": 1,
        "accepted_value_events": 0,
        "protected_actions": True,
        "multi_tenant": False,
        "regulated_or_high_sensitivity_data": False,
        "confirmed_enterprise_requirement": False,
        "verified_inline_control_incident": False,
        "verified_concurrency_contention": False,
        "reusable_gateway_assets": True,
        "machine_or_agent_identity_required": True,
        "designated_folder_enforcement_required": True,
        "inter_agent_data_exchange": False,
        "untrusted_inbox_content": False,
    }


class AssessmentTests(unittest.TestCase):
    def test_pre_value_prefers_inline_controls(self):
        result = assess_gateway_need(base_payload())
        self.assertEqual(result["decision"], "INLINE_CONTROLS_FIRST")
        self.assertIn("NO_ACCEPTED_VALUE_EVIDENCE", result["evidence_gaps"])

    def test_protected_actions_keep_owner_approval(self):
        result = assess_gateway_need(base_payload())
        self.assertIn("RON_APPROVAL_FOR_PROTECTED_ACTIONS", result["required_controls"])

    def test_single_agent_does_not_justify_gateway(self):
        result = assess_gateway_need(base_payload())
        self.assertEqual(result["decision"], "INLINE_CONTROLS_FIRST")
        self.assertIn("SINGLE_AGENT_NO_CONCURRENCY_EVIDENCE", result["evidence_gaps"])

    def test_reusable_commands_are_preserved_without_gateway_activation(self):
        result = assess_gateway_need(base_payload())
        self.assertEqual(result["asset_disposition"], "FROZEN_REUSABLE_ASSET")
        self.assertIn("EXTRACT_COMMANDS_FROM_GATEWAY_RUNTIME", result["asset_reuse_actions"])

    def test_identity_and_folder_controls_survive_without_gateway(self):
        result = assess_gateway_need(base_payload())
        self.assertIn("AUTHENTICATED_AGENT_IDENTITY", result["required_controls"])
        self.assertIn("DESIGNATED_PATH_BOUNDARY", result["required_controls"])

    def test_inter_agent_inbox_adds_provenance_and_injection_controls(self):
        payload = base_payload()
        payload.update(inter_agent_data_exchange=True, untrusted_inbox_content=True)
        result = assess_gateway_need(payload)
        self.assertIn("MESSAGE_PROVENANCE", result["required_controls"])
        self.assertIn("PROMPT_INJECTION_DEFENSE", result["required_controls"])
        self.assertEqual(result["decision"], "INLINE_CONTROLS_FIRST")

    def test_fifty_agents_is_scale_signal_not_automatic_approval(self):
        payload = base_payload()
        payload["active_agents"] = 50
        result = assess_gateway_need(payload)
        self.assertIn("FIFTY_OR_MORE_ACTIVE_AGENTS", result["signals"])
        self.assertNotEqual(result["decision"], "GATEWAY_JUSTIFIED")

    def test_confirmed_enterprise_requirement_justifies_gateway(self):
        payload = base_payload()
        payload["confirmed_enterprise_requirement"] = True
        result = assess_gateway_need(payload)
        self.assertEqual(result["decision"], "GATEWAY_JUSTIFIED")

    def test_verified_inline_incident_justifies_gateway(self):
        payload = base_payload()
        payload["verified_inline_control_incident"] = True
        result = assess_gateway_need(payload)
        self.assertEqual(result["decision"], "GATEWAY_JUSTIFIED")

    def test_verified_concurrency_contention_justifies_gateway(self):
        payload = base_payload()
        payload.update(active_agents=3, peak_concurrent_agents=3, verified_concurrency_contention=True)
        result = assess_gateway_need(payload)
        self.assertEqual(result["decision"], "GATEWAY_JUSTIFIED")
        self.assertIn("VERIFIED_CONCURRENCY_CONTENTION", result["signals"])

    def test_scale_can_create_gateway_candidate(self):
        payload = base_payload()
        payload.update(
            stage="scaling",
            active_agents=12,
            peak_concurrent_agents=6,
            independent_teams=3,
            shared_policy_surfaces=4,
            multi_tenant=True,
            accepted_value_events=4,
        )
        result = assess_gateway_need(payload)
        self.assertEqual(result["decision"], "CENTRAL_GATEWAY_CANDIDATE")

    def test_invalid_stage_fails_closed(self):
        payload = base_payload()
        payload["stage"] = "unknown"
        with self.assertRaises(ValueError):
            assess_gateway_need(payload)


if __name__ == "__main__":
    unittest.main()
