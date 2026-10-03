"""Cold-start coverage: the one-line bakery commission expands from repo facts."""
from __future__ import annotations

import copy
import json
import struct
import tempfile
import unittest
from pathlib import Path

from tools import plan_prompt
from tools.build_study_roadmap import sha256

ROOT = Path(__file__).resolve().parents[2]


class PromptTests(unittest.TestCase):
    def test_catalogue_has_all_seed_intents_and_actual_recipe_sources(self):
        catalogue = plan_prompt.load_catalogue(ROOT)
        self.assertEqual([], plan_prompt.validate_catalogue(ROOT, catalogue))
        seed = json.loads((ROOT / "docs/handoffs/codex_self_improvement_loop_2026-10-03/data/prompt_intents_seed.json").read_text(encoding="utf-8"))
        self.assertEqual({item["id"] for item in seed["intents"]}, {item["id"] for item in catalogue["intents"]})
        self.assertEqual(15, len(catalogue["intents"]))

    def test_bakery_plan_is_complete_without_chat_or_private_memory(self):
        plan = plan_prompt.build_plan(ROOT, "add a bakery job")
        self.assertEqual("INT-ADD-JOB", plan["intent"])
        self.assertEqual("PLAN_ONLY", plan["status"])
        self.assertEqual(2, len(plan["owner_touchpoints"]))
        self.assertIn("permanent job", plan["owner_touchpoints"][0]["question"])
        self.assertIn("costume", plan["owner_touchpoints"][1]["question"])
        card = plan["job_card"]
        self.assertEqual(["pour", "knead", "shape", "bake", "retrieve", "serve"], [beat["verb"] for beat in card["beats"]])
        self.assertEqual(len(card["beats"]), len({beat["verb"] for beat in card["beats"]}))
        for beat in card["beats"]:
            for key in ("visible_change", "voice_key", "line", "pointer", "contact", "child_action", "requires", "result_state"):
                self.assertTrue(beat[key])
        text = json.dumps(plan)
        for topic in ("opera_house.gd", "opera_competition.gd", "opera_hotspot_catalog.gd", "castle_career_routes.gd", "stage_inventory.json", "living_world_catalog.gd", "audio_director.gd", "audit_opera_roshan_animation", "EXPECTED_IDS", "REQUIRED_AREA_MUSIC", "passive", "tombstone", "retaining", "dev"):
            if topic == "retaining":
                self.assertIn("preserve", text.lower())
            else:
                self.assertIn(topic, text)
        self.assertTrue(all(item.get("default") and item.get("trigger") for item in plan["owner_touchpoints"]))

    def test_bakery_baking_and_retrieval_are_intentional_ordered_steps(self):
        card = plan_prompt.build_plan(ROOT, "add a bakery job")["job_card"]
        beats = card["beats"]
        for previous, current in zip(beats, beats[1:]):
            self.assertEqual(previous["result_state"], current["requires"])
        bake, retrieve, serve = beats[3:]
        self.assertEqual("shaped_raw_loaf", bake["requires"])
        self.assertEqual("baked_loaf_in_oven", bake["result_state"])
        self.assertIn("idle input pauses", bake["child_action"])
        self.assertIn("no automatic retrieval", retrieve["child_action"])
        self.assertIn("mitted hand", retrieve["contact"])
        self.assertEqual("retrieved_baked_loaf", serve["requires"])
        self.assertIn("Idle input cannot finish baking", card["state_rules"])
        self.assertIn("demonstration never grants completion", card["state_rules"])
        self.assertIn("cancels unfinished action", card["state_rules"])
        mapping = card["phase_mapping"]
        self.assertEqual(len(beats), mapping["phase_count"])
        self.assertEqual(5, mapping["finale_start"])
        finale = mapping["phases"][mapping["finale_start"]]
        self.assertEqual("Bow", finale["act"])
        self.assertEqual("serve", finale["verb"])
        self.assertTrue(all(phase["act"] != "Bow" for phase in mapping["phases"][:mapping["finale_start"]]))
        self.assertLess(mapping["finale_start"], mapping["phase_count"])
        self.assertIn("zero-based first contest phase", mapping["finale_source"])
        self.assertEqual(list(range(len(beats))), [phase["index"] for phase in mapping["phases"]])
        self.assertEqual([beat["verb"] for beat in beats], [phase["verb"] for phase in mapping["phases"]])
        self.assertIn("not four inherited phases", mapping["caveat"])
        self.assertIn("5/5 only after owner acceptance", card["quality_gate"])
        self.assertIn("pending", card["quality_gate"])

    def test_bakery_background_inventory_preserves_native_readiness_gap(self):
        inventory = plan_prompt.build_plan(ROOT, "add a bakery job")["job_card"]["background_readiness"]
        self.assertEqual("NATIVE_COVERAGE_GAP", inventory["status"])
        self.assertEqual([[1672, 941], [1672, 941]], [row["dimensions"] for row in inventory["native_sources"]])
        self.assertEqual([4096, 2304], inventory["kitchen_delivery_master"]["dimensions"])
        self.assertTrue(all(row["hash_matches_record"] for row in inventory["native_sources"]))
        self.assertTrue(inventory["kitchen_delivery_master"]["hash_matches_record"])
        self.assertIn("Lanczos", inventory["recorded_delivery_transform"])
        self.assertIn("do not prove native authored coverage or runtime readiness", inventory["acceptance"])
        self.assertIn("DL-LAY-07", inventory["acceptance"])
        self.assertIn("No new art", inventory["acceptance"])
        self.assertTrue(all((ROOT / path).is_file() for path in inventory["references"]))

    def test_bakery_background_inventory_flags_changed_source_provenance(self):
        inventory = plan_prompt.bakery_background_inventory(ROOT)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            measured = inventory["native_sources"] + [inventory["kitchen_delivery_master"]]
            hashes = {}
            for row in measured:
                source = root / row["path"]
                source.parent.mkdir(parents=True, exist_ok=True)
                # Metadata-only PNG fixtures; they make no image-quality claim.
                source.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR"
                                   + struct.pack(">II", *row["dimensions"]))
                hashes[row["path"]] = sha256(source)
            kitchen, chef, delivery = measured
            kitchen_manifest, chef_manifest = inventory["references"][:2]
            for relative, document in [
                (kitchen_manifest, {"castle": [{"room": "kitchen", "source": kitchen["path"],
                    "source_sha256": hashes[kitchen["path"]], "native_master": delivery["path"],
                    "native_master_sha256": hashes[delivery["path"]], "normalization": "whole-canvas Lanczos"}]}),
                (chef_manifest, {"accepted": [{"path": chef["path"], "sha256": hashes[chef["path"]]}]}),
            ]:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(document), encoding="utf-8")
            self.assertEqual("NATIVE_COVERAGE_GAP", plan_prompt.bakery_background_inventory(root)["status"])
            source = root / chef["path"]
            source.write_bytes(source.read_bytes() + b"changed source content")
            changed = plan_prompt.bakery_background_inventory(root)
            self.assertEqual("SOURCE_PROVENANCE_GAP", changed["status"])
            self.assertFalse(changed["native_sources"][1]["hash_matches_record"])

    def test_bakery_allocates_live_mask_and_all_four_clamps(self):
        # This named baseline fixture demonstrates the historic clamp trap
        # without preventing the live game from adding a later career.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            (root / "scripts/opera_house.gd").write_text('\n'.join(
                f'{{"save_bit": {index}}},' for index in range(18)), encoding="utf-8")
            (root / "scripts/save_state.gd").write_text(
                'const OPERA_ACTIVE_STAR_MASK := 0x3BDEF\nconst OPERA_ACTIVE_ACT_COUNT := 15\n'
                + '\n'.join('opera_stars = clampi(opera_stars, 0, 262143)' for _ in range(4)), encoding="utf-8")
            allocation = plan_prompt.save_inventory(root)
        self.assertEqual(18, allocation["next_bit"])
        self.assertEqual("0x3bdef", allocation["current_active_mask"])
        self.assertEqual("0x7bdef", allocation["proposed_active_mask"])
        self.assertEqual(524287, allocation["proposed_namespace_bound"])
        self.assertEqual(4, len(allocation["namespace_clamp_lines"]))
        self.assertIn("retain every existing save key", allocation["caveat"])
        self.assertIn("implementation head", allocation["caveat"])
        self.assertIn("both shared normaliser clamp sites", allocation["caveat"])
        self.assertIn("external merge through the shared normaliser", allocation["caveat"])

    def test_unknown_and_ambiguous_prompt_fail_closed(self):
        catalogue = plan_prompt.load_catalogue(ROOT)
        with self.assertRaises(ValueError):
            plan_prompt.infer_intent("something unspecified", catalogue)
        with self.assertRaises(ValueError):
            plan_prompt.infer_intent("study and publish the handoff", catalogue)
        plan = plan_prompt.build_plan(ROOT, "study and publish the handoff", "INT-PUBLISH-HANDOFF")
        self.assertEqual("REC-PUBLISH-HANDOFF", plan["recipe"]["id"])

    def test_missing_recipe_and_reference_rejected(self):
        catalogue = copy.deepcopy(plan_prompt.load_catalogue(ROOT))
        catalogue["intents"][0]["recipe"]["path"] = "missing-recipe.md"
        catalogue["intents"][0]["read_first"].append("missing-source.md")
        errors = plan_prompt.validate_catalogue(ROOT, catalogue)
        self.assertTrue(any("missing recipe" in error for error in errors))
        self.assertTrue(any("missing reference" in error for error in errors))

    def test_strengths_are_bound_accepted_first_without_promoting_candidates(self):
        plan = plan_prompt.build_plan(ROOT, "add a bakery job")
        tiers = [item["tier"] for item in plan["strengths"]]
        self.assertEqual("accepted", tiers[0])
        self.assertIn("candidate", tiers)
        self.assertIn("grants none", plan["acceptance"])

    def test_direct_planner_rejects_changed_strength_source_before_binding(self):
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
            source.write_bytes(b"Different source; the previous scope no longer applies.\n")
            with self.assertRaisesRegex(ValueError, "Strength evidence invalid:.*re-review"):
                plan_prompt.build_plan(root, "study the game")


if __name__ == "__main__":
    unittest.main()
