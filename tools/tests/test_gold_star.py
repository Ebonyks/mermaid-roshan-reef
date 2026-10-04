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

    def test_engine_class_names_in_notes_fail_before_the_2d_gate(self):
        self.repo.catalogue["games"][1]["scores"]["C2"]["note"] = "A Node3D root and a Camera3D."
        self.repo.save()
        errors = gold_star.validate(self.root, *self.load())
        self.assertTrue(any(gold_star.CATALOGUE in error and "Node3D x1" in error and "Camera3D x1" in error
                            for error in errors), errors)
        self.repo.catalogue["games"][1]["scores"]["C2"]["note"] = "A 3D root node and a 3D camera."
        self.repo.save()
        self.assertEqual([], gold_star.validate(self.root, *self.load()))

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


CLEAN_STATE = {
    "gpu": {"mean": 1.6, "p50": 2, "p95": 3, "max": 4, "share_ge4": 0.02},
    "gpu_translucent": {"mean": 0.1, "p50": 0, "p95": 1, "max": 2},
    "gpu_peak": 5, "duplicates": [], "broad_overlays": [], "code_drawing": [], "code_drawing_hidden": [],
    "wasted_layers": [], "roshan_covered_share": 0.02,
}
CLEAN_EFFECTS = {"transient": [{"name": "Ring", "seconds": 0.3, "screen_share": 0.002, "over_roshan_share": 0.0}],
                 "lingering_translucent": []}


class OverdrawTests(unittest.TestCase):
    """Overdraw is measured, never assumed: unmeasured, stale or code-drawn screens cannot reach 4/5."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.repo = FixtureRepo(Path(self.directory.name))
        self.root = self.repo.root
        (self.root / "scripts/games/wash.gd").write_text("extends Node2D\nfunc _draw() -> void:\n\tdraw_rect(Rect2(), Color())\n",
                                                         encoding="utf-8")
        self.repo.rubric["coverage"]["not_games"].append({"path": "scripts/games/wash.gd", "reason": "shared layer"})
        self.repo.rubric["core"] = list(gold_star.DEFAULT_CORE)
        self.repo.rubric["overdraw"] = {
            "states_not_budgeted": ["entry_transition"],
            "budgets": {"mean_layers": 2.5, "share_ge4": 0.10, "max_layers": 8, "peak_layers": 32, "translucent_p50": 0,
                        "effect_seconds": 1.0, "effect_over_roshan": 0.25},
            "checks": [{"id": check, "title": f"Check {check}", "means": "means", "method": "method"}
                       for check in gold_star.OD_CHECKS],
            "code_drawing": [{"path": "scripts/games/wash.gd", "role": "wash", "allowed": False,
                              "draws": "A full-screen wash.", "reason": "Muddies the art."}],
        }
        gold_star.bind_anchors(self.root, self.repo.rubric["overdraw"]["code_drawing"])
        self.repo.catalogue["games"][0]["overdraw_review"] = {
            "OD1": {"result": "pass", "evidence": "No painted copy under any live object."},
            "OD2": {"result": "pass", "evidence": "No look-alike beside the action."}}
        self.repo.save()

    def tearDown(self):
        self.directory.cleanup()

    def measure(self, state: dict | None = None, effects: dict | None = None, extra_states: dict | None = None) -> None:
        states = {"play": copy.deepcopy(state or CLEAN_STATE)}
        states.update(extra_states or {})
        inputs = {"scripts/games/alpha.gd": gold_star.anchor_hash(self.root, {"path": "scripts/games/alpha.gd"})}
        gold_star.write_json(self.root / gold_star.OVERDRAW, {
            "schema": "overdraw_measurements/1", "head": "a" * 40,
            "games": {"alpha": {"inputs": inputs, "states": states,
                                "effects": {"act": copy.deepcopy(effects or CLEAN_EFFECTS)}}}})

    def alpha(self) -> dict:
        catalogue, rubric = gold_star.read_json(self.root, gold_star.CATALOGUE), gold_star.read_json(self.root, gold_star.RUBRIC)
        self.assertEqual([], gold_star.validate(self.root, catalogue, rubric))
        return next(row for row in gold_star.evaluate(self.root, catalogue, rubric) if row["id"] == "alpha")

    def test_unmeasured_game_caps_c7_and_cannot_be_strong(self):
        row = self.alpha()
        # The look-alike review (OD2) needs no measurement; every machine check does.
        self.assertEqual("pass", row["overdraw"]["OD2"]["result"])
        self.assertEqual({"not_measured"}, {entry["result"] for check, entry in row["overdraw"].items() if check != "OD2"})
        self.assertEqual((1, 3), (row["scores"]["C7"], row["rating"]))
        self.assertIn("overdraw checks not all passed", row["rating_reason"])

    def test_a_clean_reviewed_measurement_passes_and_allows_four(self):
        self.measure(extra_states={"entry_transition": dict(CLEAN_STATE, gpu={"mean": 6.4, "share_ge4": 0.97, "max": 10})})
        row = self.alpha()
        self.assertEqual({"pass"}, {entry["result"] for entry in row["overdraw"].values()}, row["overdraw"])
        self.assertEqual((2, 4), (row["scores"]["C7"], row["rating"]))

    def test_each_kind_of_overdraw_is_named(self):
        state = copy.deepcopy(CLEAN_STATE)
        state["duplicates"] = [{"image": "basket.png", "names": ["Basket", "RescueBasket"], "overlap": 1.0}]
        state["code_drawing"] = ["scripts/games/wash.gd"]
        state["gpu_translucent"]["p50"] = 1
        state["gpu"].update({"mean": 3.4, "share_ge4": 0.3})
        state["wasted_layers"] = [{"name": "LetterboxFill", "screen_share": 1.0, "hidden_share": 0.98}]
        slow = {"transient": [{"name": "Puff", "seconds": 1.5, "screen_share": 0.01, "over_roshan_share": 0.6}],
                "lingering_translucent": [{"name": "Glow", "screen_share": 0.05, "translucent_share": 0.9}]}
        self.measure(state, slow)
        results = self.alpha()["overdraw"]
        self.assertIn("Basket and RescueBasket", results["OD1"]["detail"])
        self.assertIn("A full-screen wash", results["OD3"]["detail"])
        self.assertIn("Puff", results["OD4"]["detail"])
        self.assertIn("Glow", results["OD4"]["detail"])
        self.assertIn("half the screen", results["OD5"]["detail"])
        self.assertIn("LetterboxFill", results["OD6"]["detail"])
        self.assertEqual({"fail"}, {results[check]["result"] for check in ("OD1", "OD3", "OD4", "OD5", "OD6")})

    def test_unclassified_drawing_is_not_measured_and_a_peak_fails(self):
        state = copy.deepcopy(CLEAN_STATE)
        state["code_drawing"] = ["scripts/games/beta.gd"]
        state["gpu_peak"] = 255
        self.measure(state)
        results = self.alpha()["overdraw"]
        self.assertEqual("not_measured", results["OD3"]["result"])
        self.assertIn("beta.gd", results["OD3"]["detail"])
        self.assertIn("peak 255", results["OD6"]["detail"])

    def test_changed_game_file_makes_the_measurement_stale(self):
        self.measure()
        (self.root / "scripts/games/alpha.gd").write_text(GAME_A + "\n# edited\n", encoding="utf-8")
        results = self.alpha()["overdraw"]
        self.assertEqual({"not_measured"}, {entry["result"] for check, entry in results.items() if check != "OD2"})
        self.assertIn("stale", results["OD5"]["detail"])

    def test_classification_must_stay_current_and_only_child_marks_may_be_allowed(self):
        self.repo.rubric["overdraw"]["code_drawing"][0]["allowed"] = True
        self.repo.save()
        errors = gold_star.validate(self.root, *self.load())
        self.assertTrue(any("only the child's own marks" in error for error in errors), errors)
        (self.root / "scripts/games/wash.gd").write_text("extends Node2D\n", encoding="utf-8")
        self.assertEqual(["scripts/games/wash.gd"], gold_star.stale_drawing(self.root, gold_star.read_json(self.root, gold_star.RUBRIC)))

    def test_core_criteria_must_be_met_for_four(self):
        scores = {**{key: 2 for key in gold_star.ASSESSED}, "C11": 2, "C12": 0}
        self.assertEqual(4, gold_star.derive_rating(scores, core=gold_star.DEFAULT_CORE)[0])
        scores["C5"] = 1
        rating, reason = gold_star.derive_rating(scores, core=gold_star.DEFAULT_CORE)
        self.assertEqual(3, rating)
        self.assertIn("core C5", reason)

    def test_the_guide_ends_with_an_ordered_list(self):
        catalogue, rubric = self.load()
        result = gold_star.compare(gold_star.evaluate(self.root, catalogue, rubric), rubric, "alpha")
        text = gold_star.render_compare(result).rstrip().splitlines()
        self.assertIn("## To reach 4/5", text)
        self.assertTrue(text[-1].split(".")[0].isdigit(), text[-1])
        self.assertTrue(any("Measure overdraw" in step for step in result["to_four"]), result["to_four"])

    def load(self) -> tuple[dict, dict]:
        return gold_star.read_json(self.root, gold_star.CATALOGUE), gold_star.read_json(self.root, gold_star.RUBRIC)


class MeasureOverdrawTests(unittest.TestCase):
    def test_log_lines_become_compact_states_and_effects(self):
        from tools import measure_overdraw
        state = {"game": "alpha", "state": "play", "gpu_layers": {"mean": 2.0}, "gpu_translucent_layers": {"p50": 0},
                 "gpu_peak_layers": 6, "duplicates": [], "broad_overlays": [], "full_width_alpha_layers": [],
                 "custom_draw": {"items": [{"script": "res://scripts/a.gd", "shapes": True},
                                           {"script": "res://scripts/b.gd", "shapes": True}]},
                 "listing": [{"kind": "custom", "script": "b.gd", "cells": 100, "hidden": 100, "name": "B"},
                             {"kind": "vector", "name": "Fill", "cells": 9216, "hidden": 9000},
                             {"kind": "custom", "script": "a.gd", "cells": 0, "hidden": 0, "name": "A"}],
                 "roshan": {"covered_share": 0.1}, "items": 3}
        effects = {"game": "alpha", "state": "act", "transient": [
            {"name": "GuideHand", "last": 1.5}, {"name": "Ring", "last": 0.3, "max_screen_share": 0.01, "over_roshan_share": 0.0}],
            "persistent": [{"name": "Glow", "max_screen_share": 0.05, "translucent_share": 0.8, "image": "res://glow.png"}]}
        log = "noise\nOVERDRAW|STATE|" + json.dumps(state) + "\nOVERDRAW|EFFECTS|" + json.dumps(effects) + "\nOVERDRAW|DONE|{}\n"
        parsed = measure_overdraw.parse_log(log)
        compact = measure_overdraw.compact_state(parsed["states"][0])
        self.assertEqual(["scripts/a.gd"], compact["code_drawing"])
        self.assertEqual(["scripts/b.gd"], compact["code_drawing_hidden"])
        self.assertEqual(["Fill"], [layer["name"] for layer in compact["wasted_layers"]])
        self.assertEqual(6, compact["gpu_peak"])
        summary = measure_overdraw.compact_effects(parsed["effects"][0])
        self.assertEqual(["Ring"], [item["name"] for item in summary["transient"]])
        self.assertEqual(["Glow"], [item["name"] for item in summary["lingering_translucent"]])

    def test_engine_class_names_are_withheld_from_design_json(self):
        from tools import measure_overdraw
        self.assertNotIn("Node", measure_overdraw.safe("A " + "Node" + "3D root"))
        self.assertEqual("Basket", measure_overdraw.safe("Basket"))


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
