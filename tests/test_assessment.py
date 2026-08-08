import unittest

from ai_delivery_control import assess_gateway_need


def base_payload():
    return {
        "project_id": "TEST-01",
        "stage": "pre_value",
        "active_agents": 1,
        "independent_teams": 1,
        "shared_policy_surfaces": 1,
        "accepted_value_events": 0,
        "protected_actions": True,
        "multi_tenant": False,
        "regulated_or_high_sensitivity_data": False,
        "confirmed_enterprise_requirement": False,
        "verified_inline_control_incident": False,
    }


class AssessmentTests(unittest.TestCase):
    def test_pre_value_prefers_inline_controls(self):
        result = assess_gateway_need(base_payload())
        self.assertEqual(result["decision"], "INLINE_CONTROLS_FIRST")
        self.assertIn("NO_ACCEPTED_VALUE_EVIDENCE", result["evidence_gaps"])

    def test_protected_actions_keep_owner_approval(self):
        result = assess_gateway_need(base_payload())
        self.assertIn("RON_APPROVAL_FOR_PROTECTED_ACTIONS", result["required_controls"])

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

    def test_scale_can_create_gateway_candidate(self):
        payload = base_payload()
        payload.update(
            stage="scaling",
            active_agents=12,
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
