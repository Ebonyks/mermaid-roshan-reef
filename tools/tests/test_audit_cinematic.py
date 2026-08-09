"""Regression tests for the cinematic quality-gate manifest validator."""
import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock


TOOL = Path(__file__).parents[1] / "audit_cinematic.py"
SPEC = importlib.util.spec_from_file_location("audit_cinematic", TOOL)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


def scores(value):
    return {key: value for key in AUDIT.REQUIRED_SCORES}


def manifest():
    return {
        "scenes": [{
            "id": "cabin", "background_id": "cabin_layout", "start_frame": 1, "end_frame": 2,
            "characters": ["child"],
            "tracks": [{"id": "child_head", "character_id": "child", "max_step": 0.5,
                        "samples": [{"frame": 1, "x": 0.1, "y": 0.2}, {"frame": 2, "x": 0.2, "y": 0.2}]}],
            "contacts": [],
            "review": scores(4.9),
        }],
        "character_passports": {"child": {"reference_image": "child_turnaround.png", "landmarks": ["eyes"],
                                           "global_review": scores(4.95)}},
    }


def probed_video_info(
    width=1280,
    height=720,
    sample_aspect_ratio="1:1",
    display_aspect_ratio="16:9",
    rotation=None,
):
    stream = {
        "avg_frame_rate": "24/1",
        "r_frame_rate": "24/1",
        "nb_frames": "48",
        "nb_read_frames": "48",
        "duration": "2.0",
        "width": width,
        "height": height,
        "sample_aspect_ratio": sample_aspect_ratio,
        "display_aspect_ratio": display_aspect_ratio,
    }
    if rotation is not None:
        stream["side_data_list"] = [{"rotation": rotation}]
    payload = json.dumps({"streams": [stream], "format": {"duration": "2.0"}})
    with mock.patch.object(AUDIT, "command", return_value="ffprobe"), mock.patch.object(
        AUDIT, "run", return_value=payload
    ):
        return AUDIT.video_info(Path("candidate.ogv"))


class CinematicAuditTests(unittest.TestCase):
    def test_accepts_required_landscape_video_delivery(self):
        info = probed_video_info()
        self.assertEqual(AUDIT.validate_video_delivery(info), [])
        self.assertEqual(info["coded_size"], (1280, 720))
        self.assertEqual(info["display_size"], (1280.0, 720.0))

    def test_rejects_portrait_video_delivery(self):
        info = probed_video_info(
            width=720,
            height=1280,
            display_aspect_ratio="9:16",
        )
        errors = AUDIT.validate_video_delivery(info)
        self.assertTrue(any("coded size 720x1280" in error for error in errors))
        self.assertTrue(any("orientation is not landscape" in error for error in errors))

    def test_rejects_rotated_portrait_coding_even_if_display_is_landscape(self):
        info = probed_video_info(
            width=720,
            height=1280,
            display_aspect_ratio="9:16",
            rotation=90,
        )
        self.assertEqual(info["display_size"], (1280.0, 720.0))
        errors = AUDIT.validate_video_delivery(info)
        self.assertTrue(any("coded size 720x1280" in error for error in errors))
        self.assertTrue(any("rotation metadata is 90" in error for error in errors))

    def test_rejects_non_square_sample_aspect_ratio(self):
        info = probed_video_info(
            width=960,
            height=720,
            sample_aspect_ratio="4:3",
            display_aspect_ratio="16:9",
        )
        self.assertEqual(info["display_size"], (1280.0, 720.0))
        errors = AUDIT.validate_video_delivery(info)
        self.assertTrue(any("sample aspect ratio" in error for error in errors))

    def test_accepts_complete_high_quality_manifest(self):
        self.assertEqual(AUDIT.validate_manifest(manifest(), 2), [])

    def test_rejects_scene_below_congruency_floor(self):
        candidate = manifest()
        candidate["scenes"][0]["review"]["motion"] = 4.84
        self.assertTrue(any("below 4.85" in error for error in AUDIT.validate_manifest(candidate, 2)))

    def test_rejects_character_morph_risk_below_identity_floor(self):
        candidate = manifest()
        candidate["character_passports"]["child"]["global_review"]["identity"] = 4.89
        self.assertTrue(any("below 4.9" in error for error in AUDIT.validate_manifest(candidate, 2)))

    def test_accepts_complete_animatic_at_explicit_lower_floors(self):
        candidate = manifest()
        candidate["scenes"][0]["review"] = scores(AUDIT.ANIMATIC_SCENE_FLOOR)
        candidate["character_passports"]["child"]["global_review"] = scores(
            AUDIT.ANIMATIC_IDENTITY_FLOOR
        )
        self.assertEqual(
            AUDIT.validate_manifest(
                candidate,
                2,
                scene_floor=AUDIT.ANIMATIC_SCENE_FLOOR,
                identity_floor=AUDIT.ANIMATIC_IDENTITY_FLOOR,
            ),
            [],
        )

    def test_strict_defaults_remain_unchanged(self):
        candidate = manifest()
        candidate["scenes"][0]["review"]["motion"] = AUDIT.ANIMATIC_SCENE_FLOOR
        errors = AUDIT.validate_manifest(candidate, 2)
        self.assertTrue(any("below 4.85" in error for error in errors))

    def test_rejects_untracked_character(self):
        candidate = manifest()
        candidate["scenes"][0]["tracks"] = []
        self.assertTrue(any("no tracked landmark" in error for error in AUDIT.validate_manifest(candidate, 2)))

    def test_accepts_explicit_zero_indexed_manifest(self):
        candidate = manifest()
        candidate["frame_index_origin"] = 0
        scene = candidate["scenes"][0]
        scene["start_frame"] = 0
        scene["end_frame"] = 1
        scene["tracks"][0]["samples"] = [
            {"frame": 0, "x": 0.1, "y": 0.2},
            {"frame": 1, "x": 0.2, "y": 0.2},
        ]
        self.assertEqual(AUDIT.validate_manifest(candidate, 2), [])

    def test_rejects_duplicate_track_samples(self):
        candidate = manifest()
        candidate["scenes"][0]["tracks"][0]["samples"].append(
            {"frame": 2, "x": 0.2, "y": 0.2}
        )
        self.assertTrue(any(
            "duplicate frame 2" in error for error in AUDIT.validate_manifest(candidate, 2)
        ))

    def test_parse_rate_handles_ogv_unknown_rate(self):
        self.assertEqual(AUDIT.parse_rate("0/0"), 0.0)
        self.assertEqual(AUDIT.parse_rate("24/1"), 24.0)


if __name__ == "__main__":
    unittest.main()
