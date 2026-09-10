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

    def test_authored_pullback_is_allowed(self):
        self.card["camera"] = dict(verb="smooth pullback", move_count=1)
        self.assertEqual(check_card(self.root, self.card, {"S1"}), [])

    def test_multiple_camera_moves_rejected(self):
        self.card["camera"] = dict(verb="pan then pullback", move_count=2)
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

    def test_camera_count_cannot_disguise_movement(self):
        self.card["camera"] = dict(verb="smooth pullback", move_count=0)
        self.assertTrue(check_card(self.root, self.card, {"S1"}))

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


class OriginalDirectionRegressionTests(unittest.TestCase):
    packet = Path(__file__).resolve().parents[2] / "assets_src/cinematics/day_one_grok_handoff_2_2026-09-09"

    def card(self, sid):
        import json
        return json.loads((self.packet / "shots" / sid / "SHOT_PACKET.json").read_text(encoding="utf-8"))

    def test_pool_reveal_keeps_authored_camera_and_cast(self):
        self.assertEqual(self.card("D1-C06-S04")["camera"], dict(verb="smooth pullback", move_count=1))
        self.assertEqual(self.card("D1-C06-S07")["exact_cast"], ["Rumi", "Roshan"])

    def test_plug_removal_ends_before_first_water(self):
        self.assertIn("no water yet", self.card("D1-C06-S01")["end_state"])
        self.assertIn("open dry nozzle", self.card("D1-C06-S02")["timeline"][0])

    def test_discovery_cannot_bind_unplugged_state(self):
        for sid in ["D1-C05-S01", "D1-C05-S05", "D1-C05-S06", "D1-C06-S01"]:
            paths = [b["path"] for b in self.card(sid)["bindings"]]
            self.assertNotIn("references/D1-C05/handoff_art/seahorse_sick.png", paths)

    def test_recap_conflict_cannot_be_silently_rewritten(self):
        card = self.card("D1-C12-S03")
        self.assertIsNone(card["exact_cast"])
        self.assertTrue(any("conflicts" in b for b in card["blocking_findings"]))
        self.assertIn("Baby Eagle", card["must_move"])

    def test_cleared_rescue_bunny_is_absent_at_next_boundary(self):
        self.assertEqual(self.card("D1-C08-S02")["cast_by_boundary"]["end_pin_bunnies"], 1)
        self.assertEqual(self.card("D1-C08-S04")["cast_by_boundary"], dict(start_pin_bunnies=1, end_pin_bunnies=0))


if __name__ == "__main__":
    unittest.main()
