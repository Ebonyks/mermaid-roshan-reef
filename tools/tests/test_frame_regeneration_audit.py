"""Regression tests for full-frame cinematic regeneration evidence."""
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


TOOL = Path(__file__).parents[1] / "audit_cinematic.py"
SPEC = importlib.util.spec_from_file_location("audit_cinematic_frame_regeneration", TOOL)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path):
    return {"path": path.name, "sha256": sha256(path)}


def make_rgb(path, subject_left, background, subject=(245, 240, 255)):
    image = Image.new("RGB", (32, 18), background)
    draw = ImageDraw.Draw(image)
    draw.rectangle((subject_left, 6, subject_left + 5, 11), fill=subject)
    image.save(path)


def make_mask(path, subject_left, subject_top=6):
    image = Image.new("L", (32, 18), 0)
    ImageDraw.Draw(image).rectangle(
        (subject_left, subject_top, subject_left + 5, subject_top + 5),
        fill=255,
    )
    image.save(path)


def review(value=4.9):
    return {key: value for key in AUDIT.FRAME_REGENERATION_SCORES}


class FrameRegenerationAuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.previous = self.root / "previous.png"
        self.candidate = self.root / "candidate.png"
        self.following = self.root / "following.png"
        self.guide = self.root / "guide.png"
        self.candidate_mask = self.root / "candidate_mask.png"
        self.guide_mask = self.root / "guide_mask.png"
        self.prompt = self.root / "prompt.txt"
        self.previous_candidate = self.root / "previous_candidate.png"
        self.previous_guide = self.root / "previous_guide.png"
        self.previous_candidate_mask = self.root / "previous_candidate_mask.png"
        self.previous_guide_mask = self.root / "previous_guide_mask.png"
        make_rgb(self.previous, 8, (30, 90, 150))
        make_rgb(self.candidate, 10, (30, 90, 150))
        make_rgb(self.following, 12, (30, 90, 150))
        make_rgb(self.guide, 10, (255, 0, 255), subject=(0, 255, 0))
        make_mask(self.candidate_mask, 10)
        make_mask(self.guide_mask, 10)
        make_rgb(self.previous_candidate, 8, (30, 90, 150))
        make_rgb(self.previous_guide, 8, (255, 0, 255), subject=(0, 255, 0))
        make_mask(self.previous_candidate_mask, 8)
        make_mask(self.previous_guide_mask, 8)
        self.prompt.write_text("Generate the complete next frame.\n", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def manifest(self):
        return {
            "schema": "cinematic-frame-regeneration-v1",
            "frame_index_origin": 0,
            "frames": [{
                "frame": 1,
                "candidate": artifact(self.candidate),
                "previous_reference": artifact(self.previous),
                "next_reference": artifact(self.following),
                "prompt": artifact(self.prompt),
                "prompt_sha256": sha256(self.prompt),
                "attempt": 1,
                "generation_method": "full_frame_image_generation",
                "delivery_techniques": [],
                "temporal_derivation": "none",
                "action_state": "motion",
                "human_review": review(),
                "generation_references": [{
                    **artifact(self.previous),
                    "role": "accepted_neighbor",
                    "used_as_delivery_pixels": False,
                }],
                "position_guide": {
                    **artifact(self.guide),
                    "role": "position_only",
                    "used_as_delivery_pixels": False,
                },
                "subjects": [{
                    "id": "plane",
                    "candidate_mask": artifact(self.candidate_mask),
                    "position_guide_mask": artifact(self.guide_mask),
                    "max_center_error": 0.02,
                }],
            }],
        }

    def validate(self, manifest):
        return AUDIT.validate_frame_regeneration_manifest(
            manifest,
            frame_count=3,
            manifest_dir=self.root,
        )

    def motion_manifest(self):
        candidate = self.manifest()
        current = candidate["frames"][0]
        current["subjects"][0].update({
            "required_direction": "right",
            "position_axis": "x",
            "max_position_error": 0.2,
            "max_step_error": 0.01,
            "max_cross_axis_step": 0.01,
            "max_bbox_height_step": 0.01,
        })
        previous = {
            **current,
            "frame": 0,
            "candidate": artifact(self.previous_candidate),
            "next_reference": artifact(self.candidate),
            "position_guide": {
                **artifact(self.previous_guide),
                "role": "position_only",
                "used_as_delivery_pixels": False,
            },
            "subjects": [{
                **current["subjects"][0],
                "candidate_mask": artifact(self.previous_candidate_mask),
                "position_guide_mask": artifact(self.previous_guide_mask),
            }],
        }
        previous.pop("previous_reference")
        candidate["frames"].insert(0, previous)
        return candidate

    def test_accepts_complete_full_frame_regeneration(self):
        errors, reports = self.validate(self.manifest())
        self.assertEqual(errors, [])
        self.assertEqual(reports[0]["subjects"][0]["position_error"], 0.0)

    def test_accepts_generation_without_optional_position_guide(self):
        candidate = self.manifest()
        candidate["frames"][0].pop("position_guide")
        candidate["frames"][0]["subjects"][0].pop("position_guide_mask")
        errors, reports = self.validate(candidate)
        self.assertEqual(errors, [])
        self.assertIsNone(reports[0]["subjects"][0]["position_error"])

    def test_accepts_uniform_full_canvas_normalization(self):
        make_rgb(self.following, 12, (30, 90, 150))
        with Image.open(self.following).convert("RGB") as image:
            image.resize((33, 18)).save(self.following)
        candidate = self.manifest()
        candidate["canvas_policy"] = "uniform_full_canvas_normalization"
        candidate["delivery_size"] = [1280, 720]
        candidate["maximum_native_aspect_error"] = 0.04
        errors, reports = self.validate(candidate)
        self.assertEqual(errors, [])
        self.assertEqual(
            reports[0]["canvas_policy"],
            "uniform_full_canvas_normalization",
        )

    def test_rejects_native_canvas_mismatch_without_normalization_policy(self):
        with Image.open(self.following).convert("RGB") as image:
            image.resize((33, 18)).save(self.following)
        candidate = self.manifest()
        errors, _ = self.validate(candidate)
        self.assertTrue(any("does not match candidate size" in error for error in errors))

    def test_accepts_right_edge_position_anchor(self):
        candidate = self.manifest()
        candidate["frames"][0]["subjects"][0]["position_anchor"] = "bbox_right"
        errors, reports = self.validate(candidate)
        self.assertEqual(errors, [])
        self.assertEqual(reports[0]["subjects"][0]["candidate_position"][0], 0.5)

    def test_accepts_leading_edge_position_anchor(self):
        candidate = self.manifest()
        candidate["frames"][0]["subjects"][0][
            "position_anchor"
        ] = "leading_edge_right"
        errors, reports = self.validate(candidate)
        self.assertEqual(errors, [])
        self.assertEqual(reports[0]["subjects"][0]["candidate_position"], (0.5, 0.5))

    def test_rejects_tween_delivery_technique(self):
        candidate = self.manifest()
        candidate["frames"][0]["delivery_techniques"] = ["tween"]
        errors, _ = self.validate(candidate)
        self.assertTrue(any("forbidden delivery technique 'tween'" in error for error in errors))

    def test_rejects_position_guide_pixels_in_delivery(self):
        candidate = self.manifest()
        candidate["frames"][0]["position_guide"]["used_as_delivery_pixels"] = True
        errors, _ = self.validate(candidate)
        self.assertTrue(any("used_as_delivery_pixels must be false" in error for error in errors))

    def test_rejects_subject_position_drift(self):
        make_mask(self.candidate_mask, 18)
        candidate = self.manifest()
        errors, reports = self.validate(candidate)
        self.assertTrue(any("position error" in error for error in errors))
        self.assertGreater(reports[0]["subjects"][0]["position_error"], 0.02)

    def test_accepts_matching_signed_motion_step(self):
        errors, reports = self.validate(self.motion_manifest())
        self.assertEqual(errors, [])
        subject = reports[1]["subjects"][0]
        self.assertEqual(subject["step_from_previous"], 0.0625)
        self.assertEqual(subject["expected_step_from_previous"], 0.0625)
        self.assertEqual(subject["step_error"], 0.0)

    def test_rejects_wrong_motion_step_magnitude(self):
        make_mask(self.candidate_mask, 11)
        candidate = self.motion_manifest()
        errors, reports = self.validate(candidate)
        self.assertTrue(any("step error" in error for error in errors))
        self.assertGreater(reports[1]["subjects"][0]["step_error"], 0.01)

    def test_rejects_wrong_motion_direction(self):
        make_mask(self.previous_candidate_mask, 12)
        candidate = self.motion_manifest()
        errors, _ = self.validate(candidate)
        self.assertTrue(any("violating required_direction 'right'" in error for error in errors))

    def test_rejects_cross_axis_jitter(self):
        make_mask(self.candidate_mask, 10, subject_top=8)
        candidate = self.motion_manifest()
        errors, reports = self.validate(candidate)
        self.assertTrue(any("cross-axis step" in error for error in errors))
        self.assertGreater(
            reports[1]["subjects"][0]["cross_axis_step_from_previous"],
            0.01,
        )

    def test_x_position_axis_ignores_mask_height_change(self):
        make_mask(self.candidate_mask, 10, subject_top=8)
        candidate = self.manifest()
        candidate["frames"][0]["subjects"][0]["position_axis"] = "x"
        errors, reports = self.validate(candidate)
        self.assertEqual(errors, [])
        self.assertEqual(reports[0]["subjects"][0]["position_error"], 0.0)

    def test_rejects_subject_bbox_height_drift(self):
        image = Image.new("L", (32, 18), 0)
        ImageDraw.Draw(image).rectangle((10, 5, 15, 12), fill=255)
        image.save(self.candidate_mask)
        candidate = self.motion_manifest()
        errors, reports = self.validate(candidate)
        self.assertTrue(any("bbox-height step" in error for error in errors))
        self.assertGreater(
            reports[1]["subjects"][0]["bbox_height_step_from_previous"],
            0.01,
        )

    def test_rejects_material_position_guide_pixel_reuse(self):
        with Image.open(self.candidate).convert("RGB") as image:
            image.putpixel((0, 0), (31, 90, 150))
            image.save(self.guide)
        candidate = self.manifest()
        errors, _ = self.validate(candidate)
        self.assertTrue(any("exact guide-pixel ratio" in error for error in errors))

    def test_rejects_unreviewed_identity(self):
        candidate = self.manifest()
        candidate["frames"][0]["human_review"]["identity"] = 4.89
        errors, _ = self.validate(candidate)
        self.assertTrue(any("identity=4.89 is below 4.9" in error for error in errors))

    def test_rejects_candidate_hash_mismatch(self):
        candidate = self.manifest()
        candidate["frames"][0]["candidate"]["sha256"] = "0" * 64
        errors, _ = self.validate(candidate)
        self.assertTrue(any("candidate: sha256 mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
