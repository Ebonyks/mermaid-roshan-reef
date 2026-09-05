import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "audit_day_one_contextual_voices", ROOT / "tools" / "audit_day_one_contextual_voices.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DayOneContextualVoiceAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = MODULE.load_catalog(ROOT)

    def test_current_catalog_is_green_during_implementation(self) -> None:
        self.assertEqual(MODULE.validate_catalog(self.catalog, ROOT, mode="implementation"), [])

    def test_delivery_mode_fails_closed_on_pending_rows(self) -> None:
        mutated = copy.deepcopy(self.catalog)
        mutated["rows"][0]["status"] = "PENDING_GENERATION"
        issues = MODULE.validate_catalog(mutated, ROOT, mode="delivery")
        self.assertTrue(any("pending generation in delivery mode" in issue for issue in issues))

    def test_duplicate_exact_asset_requires_declared_shared_reuse(self) -> None:
        mutated = copy.deepcopy(self.catalog)
        rows = mutated["rows"]
        self.assertEqual(len({row["audio_path"] for row in rows}), len(rows))
        rows[1]["audio_path"] = rows[0]["audio_path"]
        issues = MODULE.validate_catalog(mutated, ROOT, mode="implementation")
        self.assertTrue(any("duplicate exact asset requires shared_asset_reuse" in issue for issue in issues))

    def test_generic_governed_asset_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.catalog)
        mutated["rows"][0]["audio_path"] = "assets/audio/voices/filler_v1/yay.ogg"
        issues = MODULE.validate_catalog(mutated, ROOT, mode="implementation")
        self.assertTrue(any("generic governed cue rejected" in issue for issue in issues))

    def test_ready_missing_asset_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.catalog)
        mutated["rows"][0]["status"] = "READY"
        mutated["rows"][0]["audio_path"] = "assets/audio/voices/filler_v1/does_not_exist.ogg"
        issues = MODULE.validate_catalog(mutated, ROOT, mode="implementation")
        self.assertTrue(any("READY asset missing" in issue for issue in issues))

    def test_ready_caption_file_semantic_mismatch_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.catalog)
        ready_row = mutated["rows"][0]
        ready_row["status"] = "READY"
        ready_row["audio_path"] = "assets/audio/voices/filler_v1/roshan_intro1.ogg"
        ready_row["caption"] = "Wow! A princess in the sky!"
        ready_row["caption"] = "This sentence describes a different moment."
        issues = MODULE.validate_catalog(mutated, ROOT, mode="implementation")
        self.assertTrue(any("READY caption/transcript mismatch" in issue for issue in issues))

    def test_runtime_catalog_parity_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime.gd"
            runtime.write_text(MODULE.runtime_catalog_source(self.catalog), encoding="utf-8")
            catalog = copy.deepcopy(self.catalog)
            catalog["runtime_catalog_path"] = "runtime.gd"
            self.assertEqual(MODULE.validate_runtime_catalog_parity(catalog, root), [])
            runtime.write_text(runtime.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
            issues = MODULE.validate_runtime_catalog_parity(catalog, root)
            self.assertTrue(any("runtime catalog parity drift" in issue for issue in issues))

    def test_generic_runtime_override_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "scripts" / "audio_director.gd").write_text(
                "say_day_one_context(\"cue\", \"caption\", \"bathroom\", \"s1\", 0, true)\n",
                encoding="utf-8")
            found = MODULE.find_generic_governed_calls(root)
            self.assertEqual(len(found), 1)

    def test_catalog_rows_have_stable_unique_ids_and_required_kitchen_rows(self) -> None:
        rows = self.catalog["rows"]
        ids = [row["cue_id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(rows), 114)
        self.assertEqual(len({row["audio_path"] for row in rows}), len(rows))
        self.assertTrue({
            "day1_fridge_open", "day1_fridge_close",
            "day1_recipe_pearl_select", "day1_recipe_pearl_ready",
            "day1_recipe_carrot_select", "day1_recipe_carrot_ready",
        }.issubset(ids))
        pool_captions = {row["cue_id"]: row["caption"] for row in rows if row["cue_id"].startswith("day1_pool_waterfall_lane_")}
        self.assertEqual(pool_captions["day1_pool_waterfall_lane_left"], "The left waterfall lane is clear!")
        self.assertEqual(pool_captions["day1_pool_waterfall_lane_center"], "The middle waterfall lane is clear!")
        self.assertEqual(pool_captions["day1_pool_waterfall_lane_right"], "The right waterfall lane is clear!")
        self.assertTrue({"arrival", "bathroom", "kitchen", "pool", "stuffie", "art", "boss", "finale"}.issubset(
            {row["route"] for row in rows}))

    def test_governed_callsites_have_exact_catalog_rows(self) -> None:
        self.assertEqual(MODULE.validate_governed_callsites(self.catalog, ROOT), [])

    def test_governed_callsite_caption_mismatch_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.catalog)
        row = next(row for row in mutated["rows"] if row["cue_id"] == "day1_boss_defeated")
        row["caption"] = "A different boss moment."
        issues = MODULE.validate_governed_callsites(mutated, ROOT)
        self.assertTrue(any("governed callsite caption mismatch: day1_boss_defeated" in issue for issue in issues))

    def test_day_one_live_routes_use_exact_contextual_seams(self) -> None:
        main = (ROOT / "scripts" / "main.gd").read_text(encoding="utf-8")
        castle = (ROOT / "scripts" / "arena" / "castle_rooms_25d.gd").read_text(encoding="utf-8")
        opera = (ROOT / "scripts" / "opera_act.gd").read_text(encoding="utf-8")
        self.assertIn('say_day_one_context("day1_arrival_castle"', main)
        self.assertIn('say_day_one_context("day1_finale_day_two"', main)
        self.assertIn('_say_day_one_context("day1_fridge_menu"', castle)
        self.assertIn('config["reward_policy"] = "chapter2_story"', castle)
        self.assertIn('_say_day_one_context("day1_pool_rumi_reply"', castle)
        self.assertIn('_say_day_one_context("day1_stuffie_rescue_start"', castle)
        self.assertIn('m.show_msg("", win_line, "")', opera)

    def test_day_one_live_routes_do_not_restore_known_generic_paths(self) -> None:
        castle = (ROOT / "scripts" / "arena" / "castle_rooms_25d.gd").read_text(encoding="utf-8")
        self.assertNotIn('m.show_msg("Roshan", "Hi Roshan!", "day_one_rumi_hi"', castle)
        self.assertNotIn('"Bump both dust bunnies away first! I know you can do it!",\n\t\t\t\t\t"talk")', castle)


if __name__ == "__main__":
    unittest.main()
