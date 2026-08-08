import unittest

from ai_delivery_control import validate_work_package


def valid_package():
    return {
        "work_package_id": "WP-01",
        "objective": "Create one verified output",
        "owner": "Codex",
        "owner_hours_required": 0.25,
        "inputs": ["input"],
        "output": "artifact",
        "acceptance": "test passes",
        "evidence": ["test receipt"],
        "next_action": "review evidence",
        "protected_actions": [],
    }


class WorkPackageTests(unittest.TestCase):
    def test_valid_package_passes(self):
        self.assertEqual(validate_work_package(valid_package())["status"], "PASS")

    def test_owner_hours_is_required(self):
        payload = valid_package()
        payload.pop("owner_hours_required")
        result = validate_work_package(payload)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("OWNER_HOURS" in error for error in result["errors"]))

    def test_protected_action_requires_approval_reference(self):
        payload = valid_package()
        payload["protected_actions"] = ["PUBLICATION"]
        result = validate_work_package(payload)
        self.assertIn("RON_APPROVAL_REFERENCE_REQUIRED", result["errors"])


if __name__ == "__main__":
    unittest.main()
