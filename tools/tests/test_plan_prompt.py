"""Cold-start coverage: one-line prompts expand from repository facts, for any job."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

from tools import plan_prompt
from tools.build_study_roadmap import sha256

ROOT = Path(__file__).resolve().parents[2]
# Words that belong to one stored job; a plan for another job must not contain them.
BAKERY_WORDS = ("bakery", "baker", "knead", "loaf", "flour", "oven", "dough")


class PromptTests(unittest.TestCase):
    def test_catalogue_has_all_seed_intents_and_actual_recipe_sources(self):
        catalogue = plan_prompt.load_catalogue(ROOT)
        self.assertEqual([], plan_prompt.validate_catalogue(ROOT, catalogue))
        seed = json.loads((ROOT / "docs/handoffs/codex_self_improvement_loop_2026-10-03/data/prompt_intents_seed.json").read_text(encoding="utf-8"))
        seed_ids = {item["id"] for item in seed["intents"]}
        live = {item["id"]: item for item in catalogue["intents"]}
        # The catalogue grows from lessons and owner requests; the seed may never shrink out of it.
        self.assertLessEqual(seed_ids, set(live))
        self.assertGreaterEqual(len(live), 15)
        for identifier in set(live) - seed_ids:
            self.assertTrue(live[identifier].get("revision_history"), identifier)
            self.assertTrue((ROOT / live[identifier]["recipe"]["path"]).is_file(), identifier)

    def test_recipes_are_rendered_from_the_catalogue(self):
        catalogue = plan_prompt.load_catalogue(ROOT)
        self.assertEqual([], plan_prompt.recipe_drift(ROOT, catalogue))
        for intent in catalogue["intents"]:
            text = (ROOT / intent["recipe"]["path"]).read_text(encoding="utf-8")
            self.assertNotIn("Existing session authorization takes precedence", text)
            self.assertIn("Codex builds code and every image", text)

    def test_job_plans_are_generic_and_complete(self):
        for prompt, name in (("add a bakery job", "bakery"), ("add a pizza job", "pizza"),
                             ("new job: vet", "vet"), ("plan a gardener career", "gardener")):
            with self.subTest(prompt=prompt):
                plan = plan_prompt.build_plan(ROOT, prompt)
                self.assertEqual("INT-ADD-JOB", plan["intent"])
                self.assertEqual("PLAN_ONLY", plan["status"])
                card = plan["job_card"]
                self.assertEqual(name, card["job"])
                self.assertEqual("TO_DESIGN", card["status"])
                self.assertNotIn("beats_designed", card)
                self.assertEqual(plan_prompt.JOB_BEAT_FIELDS, card["beat_fields"])
                text = json.dumps(plan)
                for topic in ("opera_house.gd", "opera_competition.gd", "opera_hotspot_catalog.gd", "castle_career_routes.gd",
                              "stage_inventory.json", "living_world_catalog.gd", "audio_director.gd", "audit_opera_roshan_animation",
                              "EXPECTED_IDS", "REQUIRED_AREA_MUSIC", "passive", "tombstone", "dev", "Parler", "roshan_base.png"):
                    self.assertIn(topic, text)
                self.assertIn("preserve", text.lower())
                self.assertTrue(all(item.get("default") and item.get("trigger") for item in plan["owner_touchpoints"]))
                self.assertTrue(all(item["default"].startswith("wait") for item in plan["owner_touchpoints"]))

    def test_unseen_jobs_carry_no_stored_answer(self):
        for prompt in ("add a pizza job", "new job: vet", "add a florist job"):
            with self.subTest(prompt=prompt):
                text = json.dumps(plan_prompt.build_plan(ROOT, prompt)).lower()
                for word in BAKERY_WORDS:
                    self.assertIsNone(re.search(rf"{word}", text), word)

    def test_imp_contest_matches_the_rule(self):
        card = plan_prompt.build_plan(ROOT, "add a vet job")["job_card"]
        self.assertIn("at most 2 s", card["imp"])
        self.assertIn("awaits owner confirmation", card["imp"])
        self.assertIn("no idle win", card["imp"])

    def test_allocation_is_derived_live(self):
        allocation = plan_prompt.build_plan(ROOT, "add a vet job")["save_allocation"]
        self.assertGreater(len(allocation["namespace_clamp_lines"]), 0)
        self.assertIn(str(allocation["next_bit"]), allocation["caveat"])
        self.assertIn(str(allocation["proposed_namespace_bound"]), allocation["caveat"])

    def test_allocates_live_mask_retired_bits_and_all_clamps(self):
        # A named fixture of the historic layout; the live game may add careers later.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            rows = [('{"save_bit": %d, "retired": true},' % index) if index in (4, 9, 14) else ('{"save_bit": %d, "name": "x"},' % index)
                    for index in range(18)]
            (root / "scripts/opera_house.gd").write_text("\n".join(rows), encoding="utf-8")
            (root / "scripts/save_state.gd").write_text(
                'const OPERA_ACTIVE_STAR_MASK := 0x3BDEF\nconst OPERA_ACTIVE_ACT_COUNT := 15\n'
                + '\n'.join('opera_stars = clampi(opera_stars, 0, 262143)' for _ in range(4)), encoding="utf-8")
            allocation = plan_prompt.save_inventory(root)
            self.assertEqual(18, allocation["next_bit"])
            self.assertEqual("0x3bdef", allocation["current_active_mask"])
            self.assertEqual("0x7bdef", allocation["proposed_active_mask"])
            self.assertEqual(524287, allocation["proposed_namespace_bound"])
            self.assertEqual(4, len(allocation["namespace_clamp_lines"]))
            self.assertEqual([4, 9, 14], allocation["retired_bits"])
            for phrase in ("retain every existing save key", "implementation head", "both shared normaliser clamp sites",
                           "external merge through the shared normaliser", "bit 18", "(4, 9, 14)"):
                self.assertIn(phrase, allocation["caveat"])
            # One more career moves every derived number; nothing stays at the old baseline.
            (root / "scripts/opera_house.gd").write_text("\n".join(rows + ['{"save_bit": 18, "name": "y"},']), encoding="utf-8")
            (root / "scripts/save_state.gd").write_text(
                'const OPERA_ACTIVE_STAR_MASK := 0x7BDEF\nconst OPERA_ACTIVE_ACT_COUNT := 16\n'
                + '\n'.join('opera_stars = clampi(opera_stars, 0, 524287)' for _ in range(4)), encoding="utf-8")
            later = plan_prompt.save_inventory(root)
            self.assertEqual(19, later["next_bit"])
            self.assertIn("bit 19", later["caveat"])
            self.assertNotIn("262143", later["caveat"])
            # A clamp written as an expression must stop the plan, not yield an empty list.
            (root / "scripts/save_state.gd").write_text(
                'const OPERA_ACTIVE_STAR_MASK := 0x7BDEF\nconst OPERA_ACTIVE_ACT_COUNT := 16\nopera_stars = clampi(opera_stars, 0, (1 << 19) - 1)\n',
                encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "clamp"):
                plan_prompt.save_inventory(root)

    def test_unknown_and_ambiguous_prompt_fail_closed_with_candidates(self):
        catalogue = plan_prompt.load_catalogue(ROOT)
        with self.assertRaises(plan_prompt.IntentError) as unknown:
            plan_prompt.infer_intent("teach Roshan to juggle", catalogue)
        self.assertEqual(3, len(unknown.exception.candidates))
        with self.assertRaises(plan_prompt.IntentError) as ambiguous:
            plan_prompt.infer_intent("study and publish the handoff", catalogue)
        self.assertEqual({"INT-STUDY", "INT-PUBLISH-HANDOFF"}, {row["intent"] for row in ambiguous.exception.candidates})
        plan = plan_prompt.build_plan(ROOT, "study and publish the handoff", "INT-PUBLISH-HANDOFF")
        self.assertEqual("REC-PUBLISH-HANDOFF", plan["recipe"]["id"])

    def test_natural_prompts_route(self):
        catalogue = plan_prompt.load_catalogue(ROOT)
        for prompt, expected in (("what should we build next", "INT-STUDY"), ("study the game", "INT-STUDY"),
                                 ("Fix MA-DOC-006: No current step-by-step script exists for building a new job game", "INT-REPAIR"),
                                 ("Finish MA-DOC-009: The improvement loop does not turn", "INT-REPAIR"),
                                 ("Check the fix for MA-VIS-002: Sky Lagoon", "INT-REPAIR"),
                                 ("delete the old backpack art", "INT-RETIRE"), ("ship it", "INT-RELEASE")):
            with self.subTest(prompt=prompt):
                self.assertEqual(expected, plan_prompt.infer_intent(prompt, catalogue)["id"])

    def test_cli_lists_candidates_instead_of_failing_silently(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = plan_prompt.main(["teach Roshan to juggle"])
        self.assertEqual(2, code)
        self.assertIn("PROMPT|NEEDS_INTENT", output.getvalue())
        self.assertIn("say it like", output.getvalue())

    def test_missing_recipe_and_reference_rejected(self):
        catalogue = copy.deepcopy(plan_prompt.load_catalogue(ROOT))
        catalogue["intents"][0]["recipe"]["path"] = "missing-recipe.md"
        catalogue["intents"][0]["read_first"].append("missing-source.md")
        errors = plan_prompt.validate_catalogue(ROOT, catalogue)
        self.assertTrue(any("missing recipe" in error for error in errors))
        self.assertTrue(any("missing reference" in error for error in errors))

    def test_touchpoints_must_be_questions_with_defaults(self):
        catalogue = copy.deepcopy(plan_prompt.load_catalogue(ROOT))
        catalogue["intents"][1]["owner_touchpoints"][0]["question"] = "New permanent career approval"
        self.assertTrue(any("question" in error for error in plan_prompt.validate_catalogue(ROOT, catalogue)))

    def test_strengths_are_bound_accepted_first_without_promoting_candidates(self):
        plan = plan_prompt.build_plan(ROOT, "add a bakery job")
        tiers = [item["tier"] for item in plan["strengths"]]
        self.assertEqual("accepted", tiers[0])
        self.assertIn("candidate", tiers)
        self.assertIn("grants none", plan["acceptance"])

    def test_changed_strength_source_is_flagged_not_fatal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "design/reference").mkdir(parents=True)
            source = root / "owner_note.md"
            source.write_bytes(b"Owner approves this exact constraint.\r\n")
            (root / "recipe.md").write_text("Source-bound study recipe", encoding="utf-8")
            intent = {
                "id": "INT-STUDY", "says": ["study the game"], "match_patterns": ["study"],
                "recipe": {"id": "REC-STUDY", "path": "recipe.md"}, "read_first": ["owner_note.md"],
                "defaults": "Read sources", "strengths": ["S-99"], "expand": ["Study source evidence"],
                "variety_rules": ["Inspect current sources"], "owner_touchpoints": [],
                "gates": ["Check source evidence"], "write_backs": ["Record findings"],
            }
            strength = {"id": "S-99", "strength": "Owner constraint", "tier": "accepted",
                "acceptance_scope": "Exact fixture owner constraint only", "reuse": "Keep the constraint",
                "evidence": [{"kind": "owner_note", "path": "owner_note.md", "hash_mode": "git_canonical_lf",
                              "sha256": sha256(source, "git_canonical_lf")}],
                "accepted_evidence": {"kind": "owner_note", "path": "owner_note.md"}}
            (root / plan_prompt.CATALOGUE).write_text(json.dumps({"intents": [intent]}), encoding="utf-8")
            (root / plan_prompt.STRENGTHS).write_text(json.dumps({"strengths": [strength]}), encoding="utf-8")
            plan = plan_prompt.build_plan(root, "study the game")
            self.assertEqual("accepted", plan["strengths"][0]["tier"])
            self.assertNotIn("evidence_changed", plan["strengths"][0])
            source.write_bytes(b"Different source; the previous scope no longer applies.\n")
            changed = plan_prompt.build_plan(root, "study the game")["strengths"][0]
            self.assertTrue(changed["evidence_changed"])
            self.assertIn("re-review", changed["scope"])


if __name__ == "__main__":
    unittest.main()
