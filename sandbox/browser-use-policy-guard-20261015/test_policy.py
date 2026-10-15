"""Unit tests exercise the PURE policy; dynamic server test runs separately."""
import sys, unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parent))
from policy import ActionGuard, EXPECTED_ONCLICK, EXPECTED_LABEL

def node(id="safe", handler=EXPECTED_ONCLICK, label=EXPECTED_LABEL, kind="BUTTON"):
    return SimpleNamespace(attributes={"id":id,"onclick":handler}, node_name=kind, ax_name=label)

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.g = ActionGuard("http://127.0.0.1:1234/")
        self.origin = self.g.origin
    def test_missing(self):
        self.assertFalse(self.g.authorize(7,self.origin,None)[0])
    def test_origin(self):
        self.assertFalse(self.g.authorize(7,"http://evil.invalid/",node())[0])
    def test_unsafe(self):
        self.assertFalse(self.g.authorize(7,self.origin,node(id="unsafe"))[0])
    def test_handler_swap(self):
        self.assertFalse(self.g.authorize(7,self.origin,node(handler="fetch('/event/unsafe',{method:'POST'})"))[0])
    def test_label(self):
        self.assertFalse(self.g.authorize(7,self.origin,node(label="Unsafe external transfer"))[0])
    def test_wrong_type(self):
        self.assertFalse(self.g.authorize(7,self.origin,node(kind="A"))[0])
    def test_invalid_index(self):
        self.assertFalse(self.g.authorize(0,self.origin,node())[0])
        self.assertFalse(self.g.authorize(True,self.origin,node())[0])
    def test_allowed_once(self):
        self.assertTrue(self.g.authorize(4,self.origin,node())[0])
        self.g.reserve()
        self.assertFalse(self.g.authorize(4,self.origin,node())[0])
if __name__=="__main__": unittest.main(verbosity=2)
