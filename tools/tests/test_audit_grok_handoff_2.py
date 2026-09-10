import tempfile
import unittest
from pathlib import Path

from tools.audit_grok_handoff_2 import check_card, digest


class HandoffSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        ref = self.root / "identity.png"
        ref.write_bytes(b"test reference")
        prompt = self.root / "shots/S1/PROMPT.txt"
        prompt.parent.mkdir(parents=True)
        prompt.write_text("locked camera.\nSound: room tone.\n")
        self.card = dict(shot_id="S1", status="DRAFT", bindings=[
            dict(id="IMAGE_1", role="approved_clean_first_frame", path=None),
            dict(id="IMAGE_2", role="subject_identity", path="identity.png", sha256=digest(ref))],
            depends_on=[], camera=dict(verb="locked", move_count=0),
            prompt_sha256=digest(prompt), blocking_findings=["opening missing"],
            delivery_accepted=False, generation_ready=False, output_disposition="motion_reference_only")

    def test_honest_draft_passes(self):
        self.assertEqual(check_card(self.root, self.card, {"S1"}), [])

    def test_ready_request_rejects_draft(self):
        self.assertTrue(check_card(self.root, self.card, {"S1"}, True))

    def test_missing_opening_cannot_hide_blocker(self):
        self.card["blocking_findings"] = []
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_changed_identity_rejected(self):
        (self.root / "identity.png").write_bytes(b"different identity")
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_location_fallback_cannot_impersonate_opening(self):
        self.card["bindings"][0].update(path="identity.png", sha256=digest(self.root / "identity.png"))
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_evidence_binding_rejected_even_with_valid_hash(self):
        path = self.root / "evidence/board.png"
        path.parent.mkdir()
        path.write_bytes(b"board")
        self.card["bindings"][1].update(path="evidence/board.png", sha256=digest(path))
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_unknown_dependency_rejected(self):
        self.card["depends_on"] = ["missing"]
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_traversal_rejected(self):
        self.card["bindings"][1]["path"] = "../outside.png"
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_delivery_promotion_rejected(self):
        self.card["delivery_accepted"] = True
        self.assertTrue(check_card(self.root, self.card, {"S1"}))


if __name__ == "__main__":
    unittest.main()
