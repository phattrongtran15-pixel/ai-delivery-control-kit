"""Small immutable-deny-by-default policy for bounded localhost Browser Use canary.
NOT a general production security boundary; process/browser can still bypass this adapter.
"""
from dataclasses import dataclass

EXPECTED_LABEL = "Record approved result"
EXPECTED_ONCLICK = "fetch('/event/safe',{method:'POST'})"

@dataclass
class ActionGuard:
    origin: str
    approved_count: int = 0
    denied_count: int = 0

    def _deny(self, reason: str) -> tuple[bool, str]:
        self.denied_count += 1
        print(f"POLICY_DENY_BEFORE_CLICK: {reason}", flush=True)
        return False, reason

    def authorize(self, index, url, node) -> tuple[bool, str]:
        if not isinstance(index, int) or isinstance(index, bool) or index < 1:
            return self._deny("BAD_INDEX")
        if url != self.origin:
            return self._deny("UNTRUSTED_ORIGIN")
        if node is None:
            return self._deny("MISSING_NODE")
        if self.approved_count >= 1:
            return self._deny("SINGLE_CLICK_LEASE_USED")
        attrs = getattr(node, "attributes", None) or {}
        if getattr(node, "node_name", "").upper() != "BUTTON":
            return self._deny("WRONG_ELEMENT_TYPE")
        if attrs.get("id") != "safe":
            return self._deny("TARGET_NOT_ALLOWLISTED")
        if attrs.get("onclick") != EXPECTED_ONCLICK:
            return self._deny("HANDLER_MISMATCH")
        if getattr(node, "ax_name", None) != EXPECTED_LABEL:
            return self._deny("LABEL_MISMATCH")
        return True, "ALLOW"

    def reserve(self):
        if self.approved_count != 0:
            raise RuntimeError("LEASE_ALREADY_USED")
        self.approved_count += 1
        print("POLICY_ALLOW_PRE_CLICK: exact target and lease reserved", flush=True)
