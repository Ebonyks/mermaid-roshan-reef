"""Planning data must fail closed on fabricated acceptance and stale evidence."""
from __future__ import annotations

import copy
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

from tools import build_study_roadmap as roadmap

ROOT = Path(__file__).resolve().parents[2]


class StrengthsTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ROOT / "design/reference/strengths.json").read_text(encoding="utf-8"))

    def test_all_seed_evidence_exists_and_is_hash_bound(self):
        self.assertEqual([], roadmap.validate_strengths(ROOT, self.document))
        self.assertEqual(15, len(self.document["strengths"]))
        self.assertIn("unmerged", next(item for item in self.document["strengths"] if item["id"] == "S-15")["acceptance_scope"])

    def test_missing_and_changed_evidence_rejected(self):
        missing = copy.deepcopy(self.document)
        missing["strengths"][0]["evidence"][0]["path"] = "missing-strength-source.md"
        self.assertTrue(any("missing evidence" in error for error in roadmap.validate_strengths(ROOT, missing)))
        changed = copy.deepcopy(self.document)
        changed["strengths"][0]["evidence"][0]["sha256"] = "0" * 64
        self.assertTrue(any("re-review" in error for error in roadmap.validate_strengths(ROOT, changed)))

    def test_machine_evidence_cannot_promote_candidate(self):
        forged = copy.deepcopy(self.document)
        item = next(item for item in forged["strengths"] if item["tier"] == "candidate")
        item["tier"] = "accepted"
        item["accepted_evidence"] = {"kind": "probe_source", "path": item["evidence"][0]["path"]}
        self.assertTrue(any("owner/child" in error for error in roadmap.validate_strengths(ROOT, forged)))

    def test_declared_text_hash_is_cross_platform_but_content_changes_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "source.md"
            path.write_bytes(b"Owner scope\r\nSame content\r\n")
            digest = roadmap.sha256(path, "git_canonical_lf")
            document = {"strengths": [{"id": "S-99", "strength": "Test source", "tier": "candidate", "acceptance_scope": "source only", "reuse": "reference",
                "evidence": [{"kind": "file", "path": "source.md", "sha256": digest, "hash_mode": "git_canonical_lf"}]}]}
            self.assertEqual([], roadmap.validate_strengths(root, document))
            path.write_bytes(b"Owner scope\nSame content\n")
            self.assertEqual(digest, roadmap.sha256(path, "git_canonical_lf"))
            self.assertEqual([], roadmap.validate_strengths(root, document))
            path.write_bytes(b"Owner scope\nChanged content\n")
            self.assertTrue(any("re-review" in error for error in roadmap.validate_strengths(root, document)))
            self.assertIn("hash mode `git_canonical_lf`", roadmap.render_strengths(document))

    def test_raw_and_unspecified_hash_modes_retain_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "source.md"
            path.write_bytes(b"Line\r\n")
            raw = roadmap.sha256(path)
            self.assertEqual(raw, roadmap.sha256(path, "raw"))
            document = {"strengths": [{"id": "S-99", "tier": "candidate", "acceptance_scope": "source only", "reuse": "reference",
                "evidence": [{"path": "source.md", "sha256": raw}]}]}
            self.assertEqual([], roadmap.validate_strengths(root, document))
            path.write_bytes(b"Line\n")
            self.assertNotEqual(raw, roadmap.sha256(path))
            self.assertTrue(roadmap.validate_strengths(root, document))
            image = root / "reference.png"
            image.write_bytes(b"binary\r\npixels")
            self.assertNotEqual(roadmap.sha256(image), roadmap.sha256(path))
            with self.assertRaisesRegex(ValueError, "text-source"):
                roadmap.sha256(image, "git_canonical_lf")


class RoadmapTests(unittest.TestCase):
    def record(self, impact="Presentation", owner="None", history="2026-10-01: opened.", lifecycle="CONFIRMED_OPEN"):
        return {"title": "Test", "lifecycle": f"`{lifecycle}`", "severity": "P2", "child_impact": impact,
                "owner_decision": owner, "history": history, "closure": "Device and owner evidence missing.",
                "acceptance": "Exact phone run and owner review.", "reproduction": "Play exact build."}

    def test_order_uses_impact_owner_dependencies_and_age(self):
        records = {
            "MA-TEST-001": self.record("Lost progress may trap the child.", "Owner decision", "2026-08-01: opened."),
            "MA-TEST-002": self.record("Lost progress may trap the child.", "Owner decision", "2026-10-01: opened."),
            "MA-TEST-003": self.record("Confusing touch", "None", "2026-01-01: opened."),
            "MA-TEST-004": self.record(lifecycle="VERIFIED_FIXED"),
        }
        today = dt.date(2026, 10, 3)
        ordinary = roadmap.make_repair_items(records, today)
        self.assertEqual(["MA-TEST-001", "MA-TEST-002", "MA-TEST-003"], [row["id"] for row in ordinary])
        dependent = roadmap.make_repair_items(records, today, {"MA-TEST-001": {"depends_on": ["MA-TEST-003"]}})
        ids = [row["id"] for row in dependent]
        self.assertLess(ids.index("MA-TEST-003"), ids.index("MA-TEST-001"))
        self.assertEqual("No directed dependency supplied; relationships are context, not an inferred blocker.", ordinary[0]["dependency_reason"])

    def test_cycle_keeps_unresolved_dependency_visible(self):
        records = {"MA-TEST-001": self.record(), "MA-TEST-002": self.record()}
        result = roadmap.make_repair_items(records, dt.date(2026, 10, 3), {
            "MA-TEST-001": {"depends_on": ["MA-TEST-002"]}, "MA-TEST-002": {"depends_on": ["MA-TEST-001"]}})
        self.assertEqual(2, len(result))
        self.assertTrue(all("Dependency cycle" in row["dependency_reason"] for row in result))

    def test_sweep_keeps_every_pending_finding_and_exact_closure_text(self):
        text = (ROOT / roadmap.FINDINGS).read_text(encoding="utf-8")
        records = roadmap.split_records(text)
        before = copy.deepcopy(records)
        rows = roadmap.verification_sweep(records, dt.date(2026, 10, 3))
        expected = {key for key, fields in records.items() if roadmap.bare(fields.get("lifecycle", "")) == "FIXED_PENDING_VERIFICATION"}
        self.assertEqual(expected, {row["id"] for row in rows})
        for row in rows:
            self.assertEqual(records[row["id"]]["closure"], row["missing_evidence"])
        self.assertEqual(before, records)
        owner = roadmap.render_sweep(rows, "2026-10-03", "owner")
        device = roadmap.render_sweep(rows, "2026-10-03", "device")
        self.assertIn("no session is scheduled", owner)
        self.assertIn("not a booking", device)
        self.assertIn("Lifecycle remains", owner)
        self.assertIn("../../findings/ACTIVE_FINDINGS_2026-08-13.md", owner)
        # Verify navigation from the actual cycle document location.
        self.assertTrue((ROOT / "audit/cycles/2026-10-03" / "../../findings/ACTIVE_FINDINGS_2026-08-13.md").resolve().is_file())

    def test_every_roadmap_item_resolves_a_recipe_and_no_fake_scores(self):
        study = {"cycle_date": "2026-10-03", "head": "a" * 40,
                 "handoffs": [{"handoff": "test-packet", "status": "NOT_STARTED"}],
                 "sensors": {"capture": {"status": "FAIL", "reason": "No output"}},
                 "surfaces": [{"name": "Day One", "source": "scripts/day_one_director.gd"}, {"name": "Grand Puff"}]}
        output = roadmap.build_outputs(ROOT, study)
        for lane in ("## Repair", "## Grow", "## Strengthen"):
            self.assertIn(lane, output["ROADMAP.md"])
        for line in output["ROADMAP.md"].splitlines():
            if line.startswith("| MA-") or line.startswith("| GROW-") or line.startswith("| SENSOR-") or line.startswith("| test-packet"):
                self.assertIn("`REC-", line)
        self.assertIn("Scores are **not assessed**", output["CURRENT_SURFACES.md"])
        self.assertIn("Day One", output["CURRENT_SURFACES.md"])
        self.assertIn("Grand Puff", output["CURRENT_SURFACES.md"])
        self.assertIn("PENDING", output["OWNER_REVIEW.md"])

    def test_measured_collection_is_not_mislabelled_as_sensor_failure(self):
        output = roadmap.build_outputs(ROOT, {"cycle_date": "2026-10-03", "sensors": {
            "measured": {"status": "MEASURED", "summary": {"status": "NO_FINDINGS_RECORDED"}},
            "debt": {"status": "MEASURED", "summary": {"status": "UNSATISFIED"}},
        }, "ci": {"advisory_steps": [{"name": "Empty capture", "status": "NOT_MEASURED"}]}})
        self.assertNotIn("SENSOR-measured:", output["ROADMAP.md"])
        self.assertIn("SENSOR-debt:", output["ROADMAP.md"])
        self.assertIn("ADVISORY-Empty capture:", output["ROADMAP.md"])

    def test_generated_history_retains_declarations_and_unknown_dates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "design/audit_impacts"
            folder.mkdir(parents=True)
            first = {"id": "first", "scope": "Original", "baseline": "a" * 40, "validation": [{"result": "PENDING"}]}
            (folder / "task-20260901.json").write_text(json.dumps(first), encoding="utf-8")
            (folder / "undated.json").write_text(json.dumps({"id": "later", "scope": "Undated"}), encoding="utf-8")
            rows = roadmap.impact_history(root)
            self.assertEqual("2026-09-01", rows[0]["date"])
            self.assertEqual("filename; not asserted completion date", rows[0]["date_source"])
            self.assertEqual("PENDING", rows[0]["results"])
            self.assertIsNone(rows[1]["date"])
            self.assertEqual(first, json.loads((folder / "task-20260901.json").read_text(encoding="utf-8")))

    def test_history_display_labels_only_real_bare_families(self):
        original = "Apply DL-VIS, DL-AUTH and DL-NOSUCH; retain DL-VIS-01 and DL-VIS-*."
        display = roadmap.format_scope_families(original, {"VIS", "AUTH"})
        self.assertEqual("Apply DL-VIS-*, DL-AUTH-* and DL-NOSUCH; retain DL-VIS-01 and DL-VIS-*.", display)
        self.assertEqual("Apply DL-VIS, DL-AUTH and DL-NOSUCH; retain DL-VIS-01 and DL-VIS-*.", original)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "design/audit_impacts"
            folder.mkdir(parents=True)
            source = folder / "historical.json"
            source.write_text(json.dumps({"scope": original}), encoding="utf-8")
            before = source.read_bytes()
            row = roadmap.impact_history(root)[0]
            self.assertEqual(original, row["scope"])
            self.assertEqual(before, source.read_bytes())


if __name__ == "__main__":
    unittest.main()
