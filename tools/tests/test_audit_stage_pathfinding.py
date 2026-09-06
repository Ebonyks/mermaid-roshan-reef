import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools import audit_stage_pathfinding as audit


class StagePathfindingAuditTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(audit.INVENTORY.read_text(encoding="utf-8"))

    def run_data(self, data):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "inventory.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return audit.audit(path)[0]

    def test_current_inventory_has_catalog_coverage(self):
        errors, counts = audit.audit()
        self.assertEqual(errors, [])
        self.assertGreaterEqual(counts["castle_rooms"], 13)
        self.assertEqual(counts["opera_acts"], 15)

    def test_missing_doctor_fails(self):
        data = json.loads(json.dumps(self.data))
        data["entries"] = [e for e in data["entries"] if e["id"] != "opera.act.05.stuffie_surgeon"]
        errors = self.run_data(data)
        self.assertTrue(any("opera.act.05.stuffie_surgeon" in e for e in errors))

    def test_wrong_career_suffix_fails(self):
        data = json.loads(json.dumps(self.data))
        for entry in data["entries"]:
            if entry["id"] == "opera.act.00.pastry_chef":
                entry["id"] = "opera.act.00.wrong_career"
        errors = self.run_data(data)
        self.assertTrue(any("opera.act.00.pastry_chef" in e for e in errors))

    def test_live_catalog_parse_requires_every_live_bit(self):
        rooms, acts = audit.expected_catalogs()
        self.assertEqual(len(rooms), 13)
        self.assertEqual(len(acts), 15)
        self.assertIn("opera.act.05.stuffie_surgeon", acts)

    def test_all_debt_strict_fails(self):
        data = json.loads(json.dumps(self.data))
        for entry in data["entries"]:
            entry["status"] = "DEBT"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "inventory.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            errors, _ = audit.audit(path)
            self.assertEqual(errors, [])
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = audit.main(["--inventory", str(path), "--strict"])
            self.assertEqual(result, 1)
            self.assertIn("strict geometry gate remains open", output.getvalue())

    def test_missing_castle_room_fails(self):
        data = json.loads(json.dumps(self.data))
        data["entries"] = [e for e in data["entries"] if e["id"] != "level2.castle.royal_bedroom"]
        errors = self.run_data(data)
        self.assertTrue(any("royal_bedroom" in e for e in errors))

    def test_nonexistent_source_fails(self):
        data = json.loads(json.dumps(self.data))
        data["entries"][0]["approved_art"] = "assets/does_not_exist.png"
        errors = self.run_data(data)
        self.assertTrue(any("source path missing" in e for e in errors))

    def test_false_accepted_status_fails(self):
        data = json.loads(json.dumps(self.data))
        data["entries"][0]["status"] = "ACCEPTED"
        errors = self.run_data(data)
        self.assertTrue(any("accepted status" in e for e in errors))

    def test_forged_complete_matrix_without_files_fails(self):
        data = json.loads(json.dumps(self.data))
        data["entries"][0]["status"] = "ACCEPTED"
        data["entries"][0]["evidence_matrix"] = "complete"
        errors = self.run_data(data)
        self.assertTrue(any("must be an object" in e for e in errors))

    def test_failed_matrix_row_fails(self):
        data = json.loads(json.dumps(self.data))
        data["entries"][0]["evidence_matrix"] = {"tap_arrival": {"result": "FAIL"}}
        errors = self.run_data(data)
        self.assertTrue(any("tap_arrival is not PASS" in e for e in errors))

    def test_matrix_hash_mismatch_fails(self):
        data = json.loads(json.dumps(self.data))
        rows = {name: {"result": "PASS", "evidence_path": "AGENTS.md", "sha256": "0" * 64} for name in audit.MATRIX_ROWS}
        data["entries"][0]["source_revision"] = "test-revision"
        data["entries"][0]["evidence_matrix"] = rows
        errors = self.run_data(data)
        self.assertTrue(any("hash mismatch" in e for e in errors))

    def test_stale_version_is_visible_but_not_a_coverage_pass(self):
        data = json.loads(json.dumps(self.data))
        data["schema"] = "stage-pathfinding-inventory-v0"
        self.assertTrue(any("unsupported inventory schema" in e for e in self.run_data(data)))

    def test_live_opera_board_label_cannot_erase_room_locomotion(self):
        data = json.loads(json.dumps(self.data))
        row = next(e for e in data["entries"] if e["id"] == "opera.act.05.stuffie_surgeon")
        row["surface_class"] = "fixed_minigame"
        self.assertTrue(any("live Opera room" in e for e in self.run_data(data)))


if __name__ == "__main__":
    unittest.main()
