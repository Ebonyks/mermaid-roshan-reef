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

    def test_all_seed_evidence_exists_and_is_structurally_valid(self):
        # Live evidence files change often; drift is a study re-review item, never a build failure.
        self.assertEqual([], roadmap.validate_strengths(ROOT, self.document, check_hashes=False))
        self.assertGreaterEqual(len(self.document["strengths"]), 15)
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
        sweep = roadmap.render_sweep(rows, "2026-10-03")
        owner = roadmap.render_sweep(rows, "2026-10-03", "owner")
        device = roadmap.render_sweep(rows, "2026-10-03", "device")
        self.assertIn("no session is scheduled", owner.lower())
        self.assertIn("not a booking", device)
        self.assertIn("Lifecycle remains", sweep)
        self.assertIn("lifecycle remains unchanged", owner)
        self.assertIn("../../findings/ACTIVE_FINDINGS_2026-08-13.md", owner)
        self.assertNotEqual(sweep.split("\n", 1)[1], device.split("\n", 1)[1])
        self.assertNotIn("441adf35", owner + device)
        # Verify navigation from the actual cycle document location.
        self.assertTrue((ROOT / "audit/cycles/2026-10-03" / "../../findings/ACTIVE_FINDINGS_2026-08-13.md").resolve().is_file())

    def test_every_roadmap_item_resolves_a_recipe_and_no_fake_scores(self):
        study = {"cycle_date": "2026-10-03", "head": "a" * 40,
                 "handoffs": [{"handoff": "test-packet", "status": "NOT_STARTED"}],
                 "sensors": {"capture": {"status": "FAIL", "reason": "No output"}},
                 "surfaces": [{"name": "Day One", "source": "scripts/day_one_director.gd"}, {"name": "Grand Puff"}]}
        output = roadmap.build_outputs(ROOT, study)
        for lane in ("## Repair", "## Verify", "## Decide", "## Waiting", "## Parked", "## Grow", "## Strengthen"):
            self.assertIn(lane, output["ROADMAP.md"])
        lane = None
        for line in output["ROADMAP.md"].splitlines():
            if line.startswith("## "):
                lane = line[3:].split(" ", 1)[0]
            elif line.startswith("| ") and not line.startswith("| Item") and not line.startswith("|---"):
                if lane in {"Decide", "Waiting", "Parked"}:
                    self.assertIn(roadmap.LANE_REASONS[lane], line)
                else:
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


class LoopRepairTests(unittest.TestCase):
    """Repairs from the 2026-10-03 review of the loop implementation."""

    def record(self, lifecycle="CONFIRMED_OPEN", severity="P2", title="A defect the child can meet", impact="Presentation"):
        return {"title": title, "lifecycle": f"`{lifecycle}`", "severity": severity, "child_impact": impact,
                "owner_decision": "None", "history": "2026-09-01: opened.", "closure": "Owner evidence missing.",
                "acceptance": "Owner review.", "reproduction": "Play."}

    def test_changed_evidence_is_reported_not_fatal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.md"
            source.write_text("Original evidence\n", encoding="utf-8")
            document = {"strengths": [{"id": "S-90", "tier": "candidate", "acceptance_scope": "fixture", "reuse": "fixture",
                                       "evidence": [{"path": "source.md", "sha256": roadmap.sha256(source)}]}]}
            source.write_text("Edited evidence\n", encoding="utf-8")
            self.assertEqual([], roadmap.validate_strengths(root, document, check_hashes=False))
            self.assertTrue(roadmap.validate_strengths(root, document))
            stale = roadmap.stale_strength_evidence(root, document)
            self.assertEqual(["S-90"], [row["id"] for row in stale])

    def test_lanes_follow_lifecycle_and_severity_ranks_before_wording(self):
        records = {
            "MA-TEST-001": self.record(severity="P2", impact="Lost progress may trap the child."),
            "MA-TEST-002": self.record(severity="P1"),
            "MA-TEST-003": self.record(lifecycle="FIXED_PENDING_VERIFICATION"),
            "MA-TEST-004": self.record(lifecycle="BLOCKED_EXTERNAL"),
            "MA-TEST-005": self.record(lifecycle="OWNER_DECISION_REQUIRED"),
            "MA-TEST-006": self.record(lifecycle="DEFERRED_WITH_REASON"),
            "MA-DOC-901": self.record(),
            "MA-TEST-007": self.record(lifecycle="REPORTED_UNCONFIRMED"),
            "MA-TEST-008": self.record(lifecycle="IN_PROGRESS"),
        }
        ordered = roadmap.make_repair_items(records, dt.date(2026, 10, 3))
        items = {item["id"]: item for item in ordered}
        self.assertEqual("Verify", items["MA-TEST-003"]["lane"])
        self.assertEqual("Waiting", items["MA-TEST-004"]["lane"])
        self.assertEqual("Decide", items["MA-TEST-005"]["lane"])
        self.assertEqual("Parked", items["MA-TEST-006"]["lane"])
        self.assertEqual("Strengthen", items["MA-DOC-901"]["lane"])
        for identifier in ("MA-TEST-004", "MA-TEST-005", "MA-TEST-006"):
            self.assertNotIn("recipe", items[identifier])
            self.assertTrue(items[identifier]["reason"])
        self.assertTrue(items["MA-TEST-002"]["prompt"].startswith("Fix MA-TEST-002"))
        self.assertTrue(items["MA-TEST-003"]["prompt"].startswith("Check the fix for MA-TEST-003"))
        self.assertTrue(items["MA-TEST-007"]["prompt"].startswith("Confirm or dismiss"))
        self.assertTrue(items["MA-TEST-008"]["prompt"].startswith("Finish"))
        self.assertTrue(items["MA-TEST-005"]["prompt"].startswith("Decide"))
        repair = [item["id"] for item in ordered if item["lane"] == "Repair"]
        self.assertEqual("MA-TEST-002", repair[0])

    def test_recorded_owner_priority_leads_its_lane(self):
        records = {"MA-DOC-901": self.record(severity="P2"), "MA-DOC-902": self.record(severity="P1")}
        priorities = {"MA-DOC-901": {"decision": "ODR-TEST", "reason": "owner priority ODR-TEST (2026-09-30)"}}
        items = roadmap.make_repair_items(records, dt.date(2026, 10, 3), priorities=priorities)
        self.assertEqual(["MA-DOC-901", "MA-DOC-902"], [item["id"] for item in items])
        self.assertIn("owner priority", items[0]["owner_reason"])

    def test_owner_report_outranks_age_but_not_priority(self):
        records = {"MA-TEST-010": {**self.record(severity="P1"), "history": "2026-10-03: reopened on owner report."},
                   "MA-TEST-011": {**self.record(severity="P1"), "history": "2026-08-01: opened."},
                   "MA-TEST-012": {**self.record(severity="P2"), "history": "2026-08-01: opened."}}
        priorities = {"MA-TEST-010": {"rank": 1, "reason": "owner report ODR-X (2026-10-03)"},
                      "MA-TEST-012": {"rank": 0, "reason": "owner priority ODR-Y (2026-09-30)"}}
        ordered = [item["id"] for item in roadmap.make_repair_items(records, dt.date(2026, 10, 3), priorities=priorities)]
        self.assertEqual(["MA-TEST-012", "MA-TEST-010", "MA-TEST-011"], ordered)

    def test_live_register_priority_reaches_the_roadmap(self):
        priorities = roadmap.owner_priorities(ROOT)
        self.assertIn("MA-DOC-006", priorities)
        output = roadmap.build_outputs(ROOT, {"cycle_date": "2026-10-03", "ci": {"status": "MEASURED", "advisory_steps": []}})["ROADMAP.md"]
        strengthen = output.split("## Strengthen", 1)[1]
        first_row = next(line for line in strengthen.splitlines() if line.startswith("| ") and not line.startswith(("| Item", "|---")))
        self.assertTrue(first_row.startswith("| MA-DOC-006"))

    def test_roadmap_prompts_route_to_their_recipe(self):
        from tools import plan_prompt
        catalogue = plan_prompt.load_catalogue(ROOT)
        by_recipe = {item["recipe"]["id"]: item["id"] for item in catalogue["intents"]}
        study = {"cycle_date": "2026-10-03", "handoffs": [{"handoff": "test-packet", "status": "NOT_STARTED"}],
                 "ci": {"status": "MEASURED", "advisory_steps": [{"name": "Capture fixture", "status": "FAILED", "reason": "renderer fallback"}]},
                 "sensors": {"debt": {"status": "MEASURED", "summary": {"status": "UNSATISFIED"}}}}
        records = roadmap.split_records((ROOT / roadmap.FINDINGS).read_text(encoding="utf-8"))
        items = roadmap.make_repair_items(records, dt.date(2026, 10, 3))
        rows = [item for item in items if item.get("recipe")]
        rows += roadmap.strengthen_items(study, [], [], 1) + roadmap.grow_items(catalogue)
        for item in rows:
            with self.subTest(prompt=item["prompt"]):
                self.assertEqual(by_recipe[item["recipe"]], plan_prompt.infer_intent(item["prompt"], catalogue)["id"])

    def test_unmeasured_ci_and_retired_steps(self):
        unmeasured = roadmap.strengthen_items({"ci": {"status": "UNAVAILABLE", "reason": "offline"}}, [], [], 0)
        self.assertEqual("CI-UNMEASURED", unmeasured[0]["id"])
        steps = [{"name": "Retired capture", "status": "NOT_MEASURED", "retired": True},
                 {"name": "Broken capture", "status": "FAILED", "reason": "renderer fallback"}]
        rows = roadmap.strengthen_items({"ci": {"status": "MEASURED", "advisory_steps": steps}}, [], [], 0)
        ids = [row["id"] for row in rows]
        self.assertIn("ADVISORY-Broken capture", ids)
        self.assertNotIn("ADVISORY-Retired capture", ids)

    def test_grow_lane_comes_from_the_catalogue(self):
        from tools import plan_prompt
        rows = roadmap.grow_items(plan_prompt.load_catalogue(ROOT))
        self.assertEqual(["GROW-ADD-JOB", "GROW-ROOM-ACTIVITY", "GROW-COMPANION", "GROW-EVENT"], [row["id"] for row in rows])
        self.assertIn("ODR-LOOP-Q8", rows[0]["source"])

    def test_short_title_is_sayable(self):
        title = "Castle interaction progress the child can see accumulates only in the unpersisted `m.g` scratch dictionary and is lost on app kill."
        handle = roadmap.short_title(title)
        self.assertLessEqual(len(handle), 91)
        self.assertNotIn("`", handle)
        self.assertEqual("2026-10-03", roadmap.cycle_date("2026-10-03b").isoformat())


class RaiseLaneTests(unittest.TestCase):
    """The gold-star scorecard feeds a Raise lane: broken catalogue, stale scores, the reference, the weakest."""

    gold = {"status": "STALE", "errors": [], "stale": ["fetch"],
            "reference": {"game": "day_one_pool", "name": "Mermaid Pool cleanup", "rating": 3, "gaps": ["C3", "C12"]},
            "weakest": [{"id": "reef", "name": "Reef", "rating": 1, "points": 2}, {"id": "kart", "name": "Kart", "rating": 1, "points": 11}]}

    def test_order_and_every_prompt_routes_to_the_gold_star_recipe(self):
        from tools import plan_prompt
        catalogue = plan_prompt.load_catalogue(ROOT)
        rows = roadmap.raise_items({"gold_star": self.gold})
        self.assertEqual(["GOLD-STAR-STALE-fetch", "GOLD-STAR-REFERENCE", "GOLD-STAR-RAISE-reef", "GOLD-STAR-RAISE-kart"],
                         [row["id"] for row in rows])
        for row in rows:
            self.assertEqual("REC-GOLD-STAR", row["recipe"])
            self.assertEqual("INT-GOLD-STAR", plan_prompt.infer_intent(row["prompt"], catalogue)["id"], row["prompt"])
        broken = roadmap.raise_items({"gold_star": {"status": "ERROR", "errors": ["games.json: bad"]}})
        self.assertEqual("GOLD-STAR-CHECK", broken[0]["id"])

    def test_lane_renders_only_when_the_scorecard_exists(self):
        study = {"cycle": "2026-10-03", "head": "a" * 40, "ci": {"status": "MEASURED", "advisory_steps": []}, "sensors": {}}
        without = roadmap.build_outputs(ROOT, {**study, "gold_star": {"status": "ABSENT"}})["ROADMAP.md"]
        self.assertNotIn("## Raise", without)
        with_lane = roadmap.build_outputs(ROOT, {**study, "gold_star": self.gold})["ROADMAP.md"]
        self.assertIn("## Raise — 4", with_lane)
        self.assertIn("Bring Mermaid Pool cleanup up to the gold star", with_lane)


if __name__ == "__main__":
    unittest.main()
