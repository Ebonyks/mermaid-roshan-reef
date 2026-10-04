"""The gold star must rate from evidence, fail closed, and never raise a score by itself."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools import gold_star

ROOT = Path(__file__).resolve().parents[2]

DESIGN = """# Design language
`DL-AGE-01` — non-reader.
`DL-AGE-02` — one finger.
`DL-QA-10` — satisfaction.
`DL-QA-06` — owner review.
"""
FINDINGS = """# Findings

## MA-OPERA-001

| Field | Value |
|---|---|
| title | Chef pours backwards |
| severity | P1 |
| lifecycle | `CONFIRMED_OPEN` |

## MA-OPERA-005

| Field | Value |
|---|---|
| title | Ballerina lacks acceptance |
| severity | P2 |
| lifecycle | `FIXED_PENDING_VERIFICATION` |
"""
GAME_A = """extends Node2D

func _ready() -> void:
\tpass

# Pour from the spout.
func pour() -> void:
\tvar side := -1
# a column-0 comment inside the body stays with it
\tprint(side)

static func helper(value: int) -> int:
\treturn value

var trailing := 1
"""
ALL_TWO = {key: {"score": 2, "note": f"{key} evidence"} for key in gold_star.ASSESSED}


def game(identifier: str, source: str, scores: dict | None = None, **extra) -> dict:
    entry = {"id": identifier, "name": identifier.title(), "family": "minigame", "state": "live",
             "route": "Castle door", "sources": [source], "probes": ["probe_x"], "findings": [],
             "scores": copy.deepcopy(scores or ALL_TWO), "acceptance": {"device": None, "child": None, "owner": None},
             "evidence": [{"path": source}]}
    entry.update(extra)
    return entry


class FixtureRepo:
    def __init__(self, directory: Path):
        self.root = directory
        files = {
            "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md": DESIGN,
            "audit/findings/ACTIVE_FINDINGS_2026-08-13.md": FINDINGS,
            "scripts/ci.sh": "for p in probe_x probe_y; do\n\techo $p\ndone\n",
            "scripts/probe_x.gd": "extends SceneTree\n",
            "scripts/probe_untrusted.gd": "extends SceneTree\n",
            "scripts/games/alpha.gd": GAME_A,
            "scripts/games/beta.gd": "extends Node2D\n\nfunc tap() -> void:\n\tpass\n",
            "scripts/games/helper.gd": "extends RefCounted\n",
            "design/reference/owner_decisions.json": json.dumps({"schema": "owner_decisions/1", "decisions": [
                {"id": "ODR-CHEF", "decision": "No.", "applies_to": ["MA-OPERA-001"]}]}),
            "tools/game_2d_migration_manifest.json": json.dumps({"production_3d_files": {"scripts/games/beta.gd": {"Vector3": 4, "Node3D": 1}}}),
        }
        for relative, text in files.items():
            path = directory / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.catalogue = {"schema": "game_catalogue/1", "status": "SUPPORTING_CURRENT", "author": "Claude",
                          "assessed": "2026-10-03", "assessed_head": "a" * 40,
                          "games": [game("alpha", "scripts/games/alpha.gd"),
                                    game("beta", "scripts/games/beta.gd",
                                         {**ALL_TWO, "C2": {"score": 0, "note": "3D"}, "C7": {"score": 0, "note": "drawn"}})]}
        self.catalogue["games"][0]["evidence"] = [{"path": "scripts/games/alpha.gd", "func": "pour"}]
        criteria = [{"id": key, "title": f"Criterion {key}", "rules": ["DL-AGE-01"], "meets": "meets"} for key in gold_star.CRITERIA]
        self.rubric = {"schema": "gold_star/1", "criteria": criteria, "rating_rule": "deterministic",
                       "reference": {"game": "alpha", "why": "strongest", "status": "CANDIDATE_REFERENCE"},
                       "patterns": [{"id": "GS-01", "criterion": "C7", "title": "Painted props", "copy": "Use the painted prop",
                                     "anchors": [{"path": "scripts/games/alpha.gd", "func": "pour"}]}],
                       "coverage": {"globs": ["scripts/games/*.gd"],
                                    "not_games": [{"path": "scripts/games/helper.gd", "reason": "shared helper"}]}}
        gold_star.bind_anchors(directory, self.catalogue["games"][0]["evidence"])
        gold_star.bind_anchors(directory, self.catalogue["games"][1]["evidence"])
        gold_star.bind_anchors(directory, self.rubric["patterns"][0]["anchors"])
        self.save()

    def save(self) -> None:
        gold_star.write_json(self.root / gold_star.CATALOGUE, self.catalogue)
        gold_star.write_json(self.root / gold_star.RUBRIC, self.rubric)


class FuncTextTests(unittest.TestCase):
    def test_function_runs_to_the_next_top_level_declaration(self):
        body = gold_star.func_text(GAME_A, "pour")
        self.assertTrue(body.startswith("func pour() -> void:"))
        self.assertIn("column-0 comment", body)
        self.assertIn("print(side)", body)
        self.assertNotIn("helper", body)

    def test_static_function_and_missing_function(self):
        self.assertIn("return value", gold_star.func_text(GAME_A, "helper"))
        self.assertIsNone(gold_star.func_text(GAME_A, "absent"))

    def test_crlf_and_lf_hash_the_same(self):
        self.assertEqual(gold_star.func_text(GAME_A, "pour"), gold_star.func_text(GAME_A.replace("\n", "\r\n"), "pour"))

    def test_one_entry_of_a_shared_table_binds_alone(self):
        table = ('const PHASES := {\n\t"chef": [\n\t\t{"name": "POUR", "voice": "Tip [it] in!"},\n\t],\n'
                 '\t"candy": [\n\t\t{"name": "SYRUP", "voice": "Pour \\"slowly\\" {now}"},\n\t],\n}\nconst NEXT := 1\n')
        block = gold_star.declaration_text(table, "PHASES", "const")
        self.assertTrue(block.endswith("}\n"))
        self.assertNotIn("NEXT", block)
        chef = gold_star.entry_text(block, "chef")
        self.assertTrue(chef.startswith('"chef": [') and chef.endswith("]"))
        self.assertNotIn("SYRUP", chef)
        self.assertIn('{now}"}', gold_star.entry_text(block, "candy"))
        self.assertIsNone(gold_star.entry_text(block, "absent"))
        edited = table.replace("SYRUP", "SUGAR")
        anchor = {"const": "PHASES", "key": "chef"}
        self.assertEqual(gold_star.anchor_text(table, anchor), gold_star.anchor_text(edited, anchor))
        self.assertNotEqual(gold_star.anchor_text(table, {"const": "PHASES", "key": "candy"}),
                            gold_star.anchor_text(edited, {"const": "PHASES", "key": "candy"}))


class RatingTests(unittest.TestCase):
    def scores(self, **changes) -> dict:
        values = {key: 2 for key in gold_star.CRITERIA}
        values.update(changes)
        return values

    def test_gold_needs_every_criterion_including_acceptance(self):
        self.assertEqual(5, gold_star.derive_rating(self.scores())[0])
        self.assertEqual(4, gold_star.derive_rating(self.scores(C12=0))[0])

    def test_unreachable_is_absent(self):
        self.assertEqual(1, gold_star.derive_rating(self.scores(C1=0, C12=0))[0])

    def test_two_failures_are_major_repair_and_one_is_workable(self):
        self.assertEqual(2, gold_star.derive_rating(self.scores(C2=0, C7=0, C12=0))[0])
        self.assertEqual(3, gold_star.derive_rating(self.scores(C7=0, C12=0))[0])

    def test_open_p0_blocker_caps_at_major_repair(self):
        self.assertEqual(2, gold_star.derive_rating(self.scores(C11=0, C12=0), p0_open=True)[0])
        self.assertEqual(2, gold_star.derive_rating(self.scores(), p0_open=True)[0])
        self.assertEqual(1, gold_star.derive_rating(self.scores(C1=0), p0_open=True)[0])

    def test_open_p1_defect_or_many_partials_cap_at_workable(self):
        self.assertEqual(3, gold_star.derive_rating(self.scores(C11=0, C12=0))[0])
        self.assertEqual(3, gold_star.derive_rating(self.scores(C3=1, C4=1, C10=1, C12=0))[0])
        self.assertEqual(4, gold_star.derive_rating(self.scores(C3=1, C10=1, C11=1, C12=0))[0])


class ComputedCriteriaTests(unittest.TestCase):
    findings = {"MA-1": {"severity": "P1", "lifecycle": "CONFIRMED_OPEN"},
                "MA-2": {"severity": "P2", "lifecycle": "CONFIRMED_OPEN"},
                "MA-3": {"severity": "P1", "lifecycle": "FIXED_PENDING_VERIFICATION"},
                "MA-4": {"severity": "P1", "lifecycle": "OWNER_DECISION_REQUIRED"},
                "MA-5": {"severity": "P0", "lifecycle": "VERIFIED_FIXED"}}

    def test_c11_counts_defects_not_pending_verification(self):
        self.assertEqual(0, gold_star.compute_c11({"findings": ["MA-1"]}, self.findings)[0])
        self.assertEqual(1, gold_star.compute_c11({"findings": ["MA-2"]}, self.findings)[0])
        self.assertEqual(2, gold_star.compute_c11({"findings": ["MA-3", "MA-5"]}, self.findings)[0])
        self.assertEqual(1, gold_star.compute_c11({"findings": ["MA-4"]}, self.findings)[0])

    def test_c12_needs_all_three_lanes_and_a_refusal_wins(self):
        accepted = {"result": "accepted", "evidence": "x.md"}
        refused = {"result": "not_accepted", "evidence": "ODR-CHEF"}
        none = {"findings": ["MA-3"], "acceptance": {}}
        score, note = gold_star.compute_c12(none, self.findings)
        self.assertEqual(0, score)
        self.assertIn("MA-3", note)
        self.assertEqual(1, gold_star.compute_c12({"acceptance": {"owner": accepted}}, self.findings)[0])
        everything = {"acceptance": {lane: accepted for lane in gold_star.ACCEPTANCE_LANES}}
        self.assertEqual(2, gold_star.compute_c12(everything, self.findings)[0])
        everything["acceptance"]["owner"] = refused
        self.assertEqual(0, gold_star.compute_c12(everything, self.findings)[0])


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.repo = FixtureRepo(Path(self.directory.name))
        self.root = self.repo.root

    def tearDown(self):
        self.directory.cleanup()

    def load(self) -> tuple[dict, dict]:
        return gold_star.read_json(self.root, gold_star.CATALOGUE), gold_star.read_json(self.root, gold_star.RUBRIC)

    def test_clean_fixture_validates_and_ranks(self):
        catalogue, rubric = self.load()
        self.assertEqual([], gold_star.validate(self.root, catalogue, rubric))
        rows = gold_star.evaluate(self.root, catalogue, rubric)
        order = gold_star.ranked(rows)
        self.assertEqual(["alpha", "beta"], [row["id"] for row in order])
        beta = next(row for row in rows if row["id"] == "beta")
        self.assertEqual((2, 5), (beta["rating"], beta["debt_3d"]))

    def test_new_game_file_must_be_catalogued(self):
        (self.root / "scripts/games/gamma.gd").write_text("extends Node2D\n", encoding="utf-8")
        catalogue, rubric = self.load()
        errors = gold_star.validate(self.root, catalogue, rubric)
        self.assertTrue(any("scripts/games/gamma.gd" in error and "not in the catalogue" in error for error in errors))

    def test_unknown_ids_and_hand_set_computed_scores_fail(self):
        self.repo.catalogue["games"][0]["findings"] = ["MA-NOPE-001"]
        self.repo.catalogue["games"][0]["probes"] = ["probe_missing"]
        self.repo.catalogue["games"][0]["scores"]["C12"] = {"score": 2, "note": "self-accepted"}
        self.repo.rubric["criteria"][0]["rules"] = ["DL-NOPE-01"]
        self.repo.save()
        errors = gold_star.validate(self.root, *self.load())
        for expected in ("MA-NOPE-001", "probe_missing", "cannot be assessed by hand", "DL-NOPE-01"):
            self.assertTrue(any(expected in error for error in errors), expected)

    def test_acceptance_needs_real_evidence(self):
        self.repo.catalogue["games"][0]["acceptance"]["owner"] = {"result": "accepted", "evidence": "ODR-MISSING"}
        self.repo.catalogue["games"][0]["acceptance"]["child"] = {"result": "accepted", "evidence": "missing/session.md"}
        self.repo.save()
        errors = gold_star.validate(self.root, *self.load())
        self.assertTrue(any("unknown owner decision" in error for error in errors))
        self.assertTrue(any("missing/session.md" in error for error in errors))

    def test_changed_function_marks_assessment_and_pattern_stale(self):
        path = self.root / "scripts/games/alpha.gd"
        path.write_text(GAME_A.replace("var side := -1", "var side := 1"), encoding="utf-8")
        catalogue, rubric = self.load()
        alpha = next(row for row in gold_star.evaluate(self.root, catalogue, rubric) if row["id"] == "alpha")
        self.assertEqual(["scripts/games/alpha.gd::pour"], alpha["stale_evidence"])
        self.assertEqual(["GS-01 scripts/games/alpha.gd::pour"], gold_star.stale_patterns(self.root, rubric))
        # Editing another function leaves the bound one current.
        path.write_text(GAME_A.replace("return value", "return value + 0"), encoding="utf-8")
        alpha = next(row for row in gold_star.evaluate(self.root, *self.load()) if row["id"] == "alpha")
        self.assertEqual([], alpha["stale_evidence"])

    def test_rebind_records_new_hashes_and_head(self):
        path = self.root / "scripts/games/alpha.gd"
        path.write_text(GAME_A.replace("var side := -1", "var side := 1"), encoding="utf-8")
        catalogue, rubric = self.load()
        updated = gold_star.rebind(self.root, catalogue, "alpha", "b" * 40)
        self.assertEqual("b" * 40, updated["games"][0]["assessed_head"])
        rows = gold_star.evaluate(self.root, updated, rubric)
        self.assertEqual([], next(row for row in rows if row["id"] == "alpha")["stale_evidence"])
        with self.assertRaises(gold_star.GoldStarError):
            gold_star.rebind(self.root, updated, "nope", "c" * 40)

    def test_compare_names_the_gap_and_the_reference_pattern(self):
        catalogue, rubric = self.load()
        result = gold_star.compare(gold_star.evaluate(self.root, catalogue, rubric), rubric, "beta")
        self.assertEqual(["C2", "C7", "C12"], [gap["criterion"] for gap in result["gaps"]])
        c7 = next(gap for gap in result["gaps"] if gap["criterion"] == "C7")
        self.assertEqual("GS-01", c7["patterns"][0]["id"])
        self.assertEqual("Bring Beta up to the gold star", result["prompt"])
        self.assertIn("Copy GS-01", gold_star.render_compare(result))

    def test_page_is_deterministic_and_check_reports_staleness(self):
        catalogue, rubric = self.load()
        rows = gold_star.evaluate(self.root, catalogue, rubric)
        self.assertEqual(gold_star.render_page(self.root, catalogue, rubric, rows),
                         gold_star.render_page(self.root, catalogue, rubric, rows))
        self.assertEqual(0, gold_star.main(["--root", str(self.root), "--render"]))
        self.assertEqual(0, gold_star.main(["--root", str(self.root), "--check", "--strict"]))
        self.repo.catalogue["games"][1]["scores"]["C7"] = {"score": 1, "note": "partly repainted"}
        self.repo.save()
        self.assertEqual(0, gold_star.main(["--root", str(self.root), "--check"]))
        self.assertEqual(1, gold_star.main(["--root", str(self.root), "--check", "--strict"]))

    def test_summary_never_raises_on_a_damaged_catalogue(self):
        (self.root / gold_star.CATALOGUE).write_text("{not json", encoding="utf-8")
        self.assertEqual("ERROR", gold_star.summary(self.root)["status"])


class LiveCatalogueTests(unittest.TestCase):
    def test_repository_catalogue_and_rubric_validate(self):
        catalogue = gold_star.read_json(ROOT, gold_star.CATALOGUE)
        rubric = gold_star.read_json(ROOT, gold_star.RUBRIC)
        self.assertEqual([], gold_star.validate(ROOT, catalogue, rubric))
        rows = gold_star.evaluate(ROOT, catalogue, rubric)
        # No game can claim a gold star without recorded device, child and owner acceptance.
        for row in rows:
            if row["rating"] == 5:
                self.assertEqual(2, row["scores"]["C12"], row["id"])
        reference = rubric["reference"]["game"]
        self.assertIn(reference, {row["id"] for row in gold_star.ranked(rows)})


if __name__ == "__main__":
    unittest.main()
