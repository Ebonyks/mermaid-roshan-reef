"""Failure-first checks for the reusable authoring engine; no art acceptance."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw
from tools import sprite_pipeline as engine


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet = self.root / "assets_src/test"
        self.packet.mkdir(parents=True)
        image = Image.new("RGBA", (80, 80))
        ImageDraw.Draw(image).ellipse((16, 16, 64, 64), fill="pink")
        image.save(self.packet / "source.png")
        source = {"path": "assets_src/test/source.png", "sha256": engine.sha(self.packet / "source.png"),
                  "role": "identity", "license": "Synthetic test geometry", "acceptance_scope": "APPROVED_SOURCE", "pixel_input_allowed": True}
        frames = [{"index": i, "path": source["path"], "sha256": source["sha256"]} for i in range(3)]
        engine.write_json(self.packet / "frames.json", frames)
        self.joints = {"frames": [{"index": i, "sha256": source["sha256"], "flags": {"hand_open": True},
                                   "points": {"wrist": [20, 20], "tip": [30, 20]}} for i in range(3)]}
        engine.write_json(self.packet / "joints.json", self.joints)
        self.review = {"frames": [{"index": i, "sha256": source["sha256"], "reviewer": "synthetic test", "reviewer_kind": "human", "date": "2026-10-07",
                                   "checks": {axis: "PASS" for axis in engine.REVIEW_AXES}} for i in range(3)],
                       "full_speed": {"status": "PASS", "frame_hashes": [source["sha256"]] * 3, "reviewer": "synthetic test", "reviewer_kind": "human", "date": "2026-10-07"}}
        engine.write_json(self.packet / "review.json", self.review)
        engine.write_json(self.packet / "attempts.json", {"campaign_id": "shared", "limits": {"imagegen_calls_max": 2, "wall_minutes_max": 20, "cleanup_minutes_max": 10}, "attempts": []})
        geometry = {"landmarks": {"crown": [30, 30], "eye": [40, 40], "waist": [50, 50]}, "head_box": [20, 20, 60, 60],
                    "segments": {"hand": {"points": ["wrist", "tip"], "length_px": 10, "tolerance_pct": 5, "required_when": "hand_open"}}}
        action = {"count": 3, "fps": 24, "verb": "wave", "sources": ["home"], "phases": [{"name": "wave", "from": 0, "to": 2, "description": "greet and settle"}],
                  "limits": {"figure_scale_pp_pct": 1, "head_scale_pp_pct": 2, "border_px": 1}, "boundaries": [{"index": 0, "source_id": "home"}, {"index": 2, "source_id": "home"}],
                  "context_frames": 1, "motion_locks": ["whole figure", "constant size"], "key_canvas": [80, 80], "backend": {"route": "local"},
                  "key_gaps": [{"id": "raise", "index": 1, "description": "one complete raising pose", "source_ids": ["home"]},
                               {"id": "lower", "index": 1, "description": "one complete lowering pose", "source_ids": ["home"]}]}
        job = {"character_id": "test", "outfit_id": "pink", "action_id": "wave", "frames_manifest": "assets_src/test/frames.json",
               "native_canvas": [80, 80], "mapping": {"scale": 1, "offset": [0, 0]}, "joints": "assets_src/test/joints.json", "review": "assets_src/test/review.json",
               "campaign_id": "shared", "attempt_ledger": "assets_src/test/attempts.json"}
        self.catalog = {"schema": engine.SCHEMA, "sources": {"home": source}, "characters": {"test": {"sources": ["home"], "geometry": geometry, "identity_locks": ["test face"]}},
                        "outfits": {"pink": {"character_id": "test", "sources": ["home"], "description": "pink", "locks": ["same pink"]},
                                    "blue": {"character_id": "test", "sources": ["home"], "description": "blue", "locks": ["same blue"]}},
                        "actions": {"wave": action}, "jobs": {"pink_wave": job, "blue_wave": {**job, "outfit_id": "blue"}}}
        self.catalog_path = self.packet / "catalog.json"
        self.save_catalog()

    def save_catalog(self):
        engine.write_json(self.catalog_path, self.catalog)

    def job(self, name="pink_wave"):
        return engine.load_job(self.root, self.catalog_path, name)

    def report(self, job=None):
        with patch.object(engine, "geometry", return_value=({"single_layer": engine.check("PASS", 1)}, [])):
            return engine.inspect(self.root, job or self.job())

    def test_timeline_distributes_rounding_and_generalizes(self):
        self.assertEqual(sum(engine.frame_clock(41, 24)), 1708)
        self.assertEqual(sum(engine.frame_clock(7, 30)), 233)
        self.assertEqual(len(engine.frame_clock(19, 12)), 19)

    def test_unannotated_joints_never_pass(self):
        self.joints["frames"].pop()
        engine.write_json(self.packet / "joints.json", self.joints)
        report = self.report()
        self.assertFalse(report["candidate_ready"])
        self.assertEqual(report["checks"]["proportions"]["status"], "PENDING")

    def test_joint_flags_must_be_explicit(self):
        self.joints["frames"][1]["flags"] = {}
        engine.write_json(self.packet / "joints.json", self.joints)
        self.assertEqual(self.report()["checks"]["proportions"]["status"], "PENDING")

    def test_out_of_contract_joint_fails(self):
        self.joints["frames"][1]["points"]["tip"] = [40, 20]
        engine.write_json(self.packet / "joints.json", self.joints)
        self.assertEqual(self.report()["checks"]["proportions"]["status"], "FAIL")

    def test_stale_review_rejected(self):
        self.review["frames"][1]["sha256"] = "0" * 64
        engine.write_json(self.packet / "review.json", self.review)
        with self.assertRaisesRegex(ValueError, "stale"):
            self.report()

    def test_static_review_does_not_accept_motion(self):
        del self.review["full_speed"]
        engine.write_json(self.packet / "review.json", self.review)
        self.assertEqual(self.report()["checks"]["full_speed_review"]["status"], "PENDING")

    def test_model_observations_cannot_fill_human_acceptance(self):
        for row in self.review["frames"]:
            row["reviewer_kind"] = "model_observation"
        self.review["full_speed"]["reviewer_kind"] = "model_observation"
        engine.write_json(self.packet / "review.json", self.review)
        report = self.report()
        self.assertEqual(report["checks"]["human_frame_review"]["status"], "PENDING")
        self.assertEqual(report["checks"]["full_speed_review"]["status"], "PENDING")
        self.assertFalse(report["candidate_ready"])

    def test_guide_cannot_become_generation_pixels(self):
        self.catalog["sources"]["home"]["role"] = "position_only"
        self.save_catalog()
        job = self.job()
        with self.assertRaisesRegex(ValueError, "generation pixels"):
            engine.repair_requests(self.root, job, self.report(job))

    def test_outfit_aliases_rebind_references_without_action_fork(self):
        blue_path = self.packet / "blue.png"
        image = Image.open(self.packet / "source.png").convert("RGBA")
        ImageDraw.Draw(image).ellipse((16, 16, 64, 64), fill="blue")
        image.save(blue_path)
        blue = {**self.catalog["sources"]["home"], "path": "assets_src/test/blue.png", "sha256": engine.sha(blue_path)}
        self.catalog["sources"]["blue_home"] = blue
        self.catalog["outfits"]["pink"]["source_aliases"] = {"rest": "home"}
        self.catalog["outfits"]["blue"]["source_aliases"] = {"rest": "blue_home"}
        self.catalog["outfits"]["blue"]["sources"] = ["blue_home"]
        action = self.catalog["actions"]["wave"]
        action["sources"] = ["@rest"]
        for boundary in action["boundaries"]:
            boundary["source_id"] = "@rest"
        for gap in action["key_gaps"]:
            gap["source_ids"] = ["@rest"]
        engine.write_json(self.packet / "blue_frames.json", [{"index": i, "path": blue["path"], "sha256": blue["sha256"]} for i in range(3)])
        self.catalog["jobs"]["blue_wave"].update(frames_manifest="assets_src/test/blue_frames.json", review=None, joints=None)
        self.save_catalog()
        pink, blue_job = self.job(), self.job("blue_wave")
        pink_plan = engine.repair_requests(self.root, pink, self.report(pink))
        blue_report = self.report(blue_job)
        blue_plan = engine.repair_requests(self.root, blue_job, blue_report)
        self.assertEqual(pink["action"], blue_job["action"])
        self.assertEqual(blue_report["checks"]["endpoints"]["status"], "PASS")
        self.assertEqual(pink_plan["requests"][0]["bindings"][0]["source_id"], "home")
        self.assertEqual(blue_plan["requests"][0]["bindings"][0]["source_id"], "blue_home")
        self.assertEqual(blue_plan["requests"][0]["bindings"][0]["sha256"], blue["sha256"])

    def test_changed_source_rejected(self):
        with (self.packet / "source.png").open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(ValueError, "changed pinned"):
            self.job()

    def test_declared_metadata_line_endings_are_portable(self):
        import hashlib
        path = self.packet / "receipt.json"
        canonical = b'{"provider": "test"}\n'
        path.write_bytes(canonical.replace(b"\n", b"\r\n"))
        entry = {"path": "assets_src/test/receipt.json", "sha256": hashlib.sha256(canonical).hexdigest(), "hash_normalization": "git_text_lf"}
        self.assertEqual(engine.pinned(self.root, entry), path)
        path.write_bytes(canonical)
        self.assertEqual(engine.pinned(self.root, entry), path)
        path.write_bytes(canonical + b"changed")
        with self.assertRaisesRegex(ValueError, "changed pinned"):
            engine.pinned(self.root, entry)

    def test_duplicate_frame_inventory_rejected(self):
        frames = engine.read_json(self.packet / "frames.json")
        frames[1]["index"] = 0
        engine.write_json(self.packet / "frames.json", frames)
        with self.assertRaisesRegex(ValueError, "every index"):
            self.job()

    def test_outfit_change_reuses_engine_and_budget(self):
        pink = self.job()
        plan = engine.repair_requests(self.root, pink, self.report(pink))
        engine.reserve_key(pink, plan, "raise")
        blue = self.job("blue_wave")
        other = engine.repair_requests(self.root, blue, self.report(blue))
        self.assertEqual(other["calls_used"], 1)
        self.assertIn("Outfit: blue", other["requests"][1]["prompt"])
        self.assertEqual(other["requests"][1]["state"], "READY_TO_REQUEST_KEY")
        engine.reserve_key(blue, other, "lower")
        with self.assertRaisesRegex(ValueError, "call cap"):
            engine.reserve_key(pink, plan, "raise")

    def test_reservation_keeps_failed_call_in_budget(self):
        job = self.job()
        plan = engine.repair_requests(self.root, job, self.report(job))
        engine.reserve_key(job, plan, "raise")
        request = plan["requests"][0]
        receipt = {"provider": "synthetic", "request_id": "test-1", "provider_revision": "test", "elapsed_seconds": 2, "cleanup_minutes": 0,
                   "usage": {"calls": 1}, "disposition": "FAILED", "prompt_sha256": request["prompt_sha256"], "binding_hashes": [b["sha256"] for b in request["bindings"]]}
        result = engine.record_key(self.root, job, plan, "raise", None, receipt, self.packet / "failed")
        self.assertEqual(result["disposition"], "FAILED")
        self.assertEqual(len(engine.read_json(job["ledger_path"])["attempts"]), 1)

    def test_unreserved_output_cannot_hide_a_call(self):
        job = self.job()
        plan = engine.repair_requests(self.root, job, self.report(job))
        request = plan["requests"][0]
        receipt = {"provider": "synthetic", "request_id": "test", "provider_revision": "test", "elapsed_seconds": 2, "cleanup_minutes": 0,
                   "usage": {"calls": 1}, "disposition": "CANDIDATE", "prompt_sha256": request["prompt_sha256"], "binding_hashes": [b["sha256"] for b in request["bindings"]]}
        with self.assertRaisesRegex(ValueError, "Reserve"):
            engine.record_key(self.root, job, plan, "raise", self.packet / "source.png", receipt, self.packet / "candidate")

    def test_report_revision_cannot_be_reused(self):
        job = self.job()
        report = self.report(job)
        report["catalog_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "different revision"):
            engine.repair_requests(self.root, job, report)

    def test_paths_cannot_touch_runtime_or_private_directories(self):
        for path in ("../outside", ".secrets/key.txt", ".git/config", "assets/book/test.png", "."):
            with self.subTest(path=path), self.assertRaises(ValueError):
                engine.inside(self.root, path, output=True)

    def test_contiguous_defects_share_context(self):
        spans = engine.group_spans([{"index": i, "category": "hand"} for i in (5, 6, 7, 24, 25)], 41, 2)
        self.assertEqual([(r["from"], r["to"], r["context_from"], r["context_to"]) for r in spans], [(5, 7, 3, 9), (24, 25, 22, 27)])

    def test_missing_geometry_dependency_is_pending(self):
        with patch.object(engine, "geometry", return_value=({"geometry": engine.check("PENDING", "missing cv2")}, [])):
            self.assertFalse(engine.inspect(self.root, self.job())["candidate_ready"])

    def test_flattened_layers_cannot_hide_missing_derivation(self):
        self.assertEqual(self.report()["checks"]["whole_frame_provenance"]["status"], "PENDING")

    def test_complete_authoring_evidence_can_pass_without_granting_delivery(self):
        job = self.job()
        provenance = {"frames": [{"index": row["index"], "sha256": row["sha256"], "method": "approved_whole_frame_reuse", "pixel_assembly": "NONE",
                                  "parents": [self.catalog["sources"]["home"]], "edits": "Synthetic complete-shape source unchanged"} for row in job["frames"]]}
        path = self.packet / "derivation.json"
        engine.write_json(path, provenance)
        job["derivation"] = {"path": path.relative_to(self.root).as_posix(), "sha256": engine.sha(path)}
        with patch.object(engine, "alpha_islands", return_value=engine.check("PASS", "synthetic single component")):
            report = self.report(job)
        self.assertTrue(report["candidate_ready"])
        self.assertFalse(report["claims"]["DELIVERY_ACCEPTED"])
        self.assertEqual(report["claims"]["device_child_owner"], "PENDING")

    def test_pasted_limbs_fail_even_when_master_has_one_layer(self):
        job = self.job()
        provenance = {"frames": [{"index": row["index"], "sha256": row["sha256"], "method": "cutout_arm_composite", "pixel_assembly": "PASTED_PARTS",
                                  "parents": [self.catalog["sources"]["home"]], "edits": "Flattened separately warped arm over frozen body"} for row in job["frames"]]}
        path = self.packet / "derivation.json"
        engine.write_json(path, provenance)
        job["derivation"] = {"path": path.relative_to(self.root).as_posix(), "sha256": engine.sha(path)}
        self.assertEqual(self.report(job)["checks"]["whole_frame_provenance"]["status"], "FAIL")

    def test_normalization_refuses_nonuniform_character_stretch(self):
        job = self.job()
        job["action"]["delivery_cell"] = [80, 60]
        with self.assertRaisesRegex(ValueError, "stretch"):
            engine.normalize_key(self.root, job, self.packet / "source.png", self.packet / "normalized", "not-run")
        self.assertFalse((self.packet / "normalized").exists())

    def test_detached_alpha_fleck_is_measured_without_cleanup(self):
        try:
            import cv2
        except ImportError:
            self.skipTest("OpenCV is optional; actual component checks run in installed Python3.10")
        path = self.packet / "fleck.png"
        image = Image.open(self.packet / "source.png").convert("RGBA")
        ImageDraw.Draw(image).rectangle((2, 2, 6, 6), fill="white")
        image.save(path)
        before = engine.sha(path)
        result = engine.alpha_islands(path, 4)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(engine.sha(path), before)


if __name__ == "__main__":
    unittest.main()
