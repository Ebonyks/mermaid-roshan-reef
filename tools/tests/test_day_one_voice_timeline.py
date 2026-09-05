"""Deterministic regression tests for Day One editorial voice timelines."""

import importlib.util
import json
import copy
import tempfile
import unittest
from pathlib import Path
from unittest import mock


TOOL = Path(__file__).parents[1] / "build_day_one_voice_timeline.py"
SPEC = importlib.util.spec_from_file_location("day_one_voice_timeline", TOOL)
TIMELINE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(TIMELINE)


ROOT = Path(__file__).parents[2]
LEDGER_PATH = ROOT / "audit/cinematics/day_one_voice_timelines/day_one_source_ledger.json"
CUE_PATH = ROOT / "audit/cinematics/day_one_voice_timelines/d1_c00_c01_roshan_cues.json"


class DayOneVoiceTimelineTests(unittest.TestCase):
    def test_registered_reference_is_hash_bound_silent_and_unresolved(self):
        ledger = TIMELINE.load_json(LEDGER_PATH)
        source = ledger["sources"][0]
        self.assertEqual(source["source_sha256"], TIMELINE.SOURCE_SHA256)
        self.assertEqual(source["video_sha256"], TIMELINE.SOURCE_SHA256)
        self.assertEqual(source["audio_sha256"], TIMELINE.EMPTY_AUDIO_SHA256)
        self.assertEqual(source["audio_stream_count"], 0)
        self.assertEqual(source["visual_acceptance"], "unresolved")

    def test_sidecar_maps_visible_beats_and_omits_ambiguous_otter(self):
        ledger = TIMELINE.load_json(LEDGER_PATH)
        sidecar = TIMELINE.load_json(CUE_PATH)
        self.assertEqual(TIMELINE.validate_cues(ledger, sidecar), [])
        self.assertEqual(len(sidecar["cues"]), 19)
        keys = {cue["event_key"] for cue in sidecar["cues"]}
        self.assertNotIn("D1-C00-C01.S16.otter_reaction", keys)
        self.assertTrue(sidecar["editorial_notes"]["preserve_closed_door_semantics"])
        closed = next(cue for cue in sidecar["cues"] if cue["event_key"].endswith("plane_exit_closed"))
        opened = next(cue for cue in sidecar["cues"] if cue["event_key"].endswith("plane_exit_open"))
        self.assertEqual((closed["timing"]["start_s"], closed["timing"]["end_s"]), (37.5, 40.5))
        self.assertEqual((opened["timing"]["start_s"], opened["timing"]["end_s"]), (40.5, 43.5))

    def test_require_audio_blocks_pending_bindings(self):
        ledger = TIMELINE.load_json(LEDGER_PATH)
        sidecar = TIMELINE.load_json(CUE_PATH)
        errors = TIMELINE.validate_cues(ledger, sidecar, require_audio=True)
        self.assertEqual(len(errors), 19)
        self.assertTrue(all("audio binding is pending" in error for error in errors))

    def test_require_audio_verifies_mastered_paths_hashes_and_durations(self):
        ledger = TIMELINE.load_json(LEDGER_PATH)
        sidecar_path = ROOT / "audit/cinematics/day_one_voice_timelines/d1_c00_c01_roshan_mastered_cues.json"
        sidecar = TIMELINE.load_json(sidecar_path)
        self.assertEqual(TIMELINE.validate_cues(ledger, sidecar, require_audio=True), [])

        missing = copy.deepcopy(sidecar)
        missing["cues"][0]["audio"]["path"] = "assets/audio/voices/filler_v1/missing.ogg"
        errors = TIMELINE.validate_cues(ledger, missing, require_audio=True)
        self.assertTrue(any("audio.path does not exist" in error for error in errors))

        wrong_hash = copy.deepcopy(sidecar)
        wrong_hash["cues"][0]["audio"]["sha256"] = "0" * 64
        errors = TIMELINE.validate_cues(ledger, wrong_hash, require_audio=True)
        self.assertTrue(any("audio.sha256 does not match asset" in error for error in errors))

        too_short = copy.deepcopy(sidecar)
        cue = too_short["cues"][1]
        cue["timing"]["end_s"] = cue["timing"]["start_s"] + 1.0
        errors = TIMELINE.validate_cues(ledger, too_short, require_audio=True)
        self.assertTrue(any("audio duration" in error and "exceeds cue span" in error for error in errors))

    def test_time_stretch_and_mux_are_blocked(self):
        ledger = TIMELINE.load_json(LEDGER_PATH)
        sidecar = TIMELINE.load_json(CUE_PATH)
        sidecar["cues"][0]["timing"]["time_stretch"] = True
        sidecar["mix_plan"]["mux"] = True
        errors = TIMELINE.validate_cues(ledger, sidecar)
        self.assertTrue(any("time_stretch=false" in error for error in errors))
        self.assertTrue(any("mix_plan must forbid" in error for error in errors))

    def test_plan_is_deterministic_and_review_only(self):
        with tempfile.TemporaryDirectory() as temp:
            first = Path(temp) / "plan-a.json"
            second = Path(temp) / "plan-b.json"
            TIMELINE.build_plan(LEDGER_PATH, CUE_PATH, first)
            TIMELINE.build_plan(LEDGER_PATH, CUE_PATH, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            plan = json.loads(first.read_text(encoding="utf-8"))
            self.assertIsNone(plan["runtime_path"])
            self.assertIsNone(plan["muxed_video"])
            self.assertEqual(plan["delivery_acceptance"], "pending_human_and_device_review")

    def test_review_output_cannot_be_written_under_runtime_assets(self):
        with self.assertRaisesRegex(ValueError, "outside the runtime assets"):
            TIMELINE.save_json(Path("assets/review/plan.json"), {"schema": TIMELINE.SCHEMA})

    def test_inspect_source_rejects_audio_and_records_geometry(self):
        probe = {
            "streams": [{
                "codec_type": "video", "codec_name": "h264", "width": 1280,
                "height": 720, "avg_frame_rate": "24/1", "duration": "46.5",
                "nb_frames": "1116",
            }],
            "format": {"duration": "46.5"},
        }
        with tempfile.NamedTemporaryFile() as handle:
            path = Path(handle.name)
            with mock.patch.object(TIMELINE, "_probe", return_value=probe), mock.patch.object(
                TIMELINE, "file_sha256", return_value=TIMELINE.SOURCE_SHA256
            ):
                metadata = TIMELINE.inspect_source(path)
        self.assertEqual(metadata["width"], 1280)
        self.assertEqual(metadata["fps"], 24.0)
        self.assertEqual(metadata["audio_sha256"], TIMELINE.EMPTY_AUDIO_SHA256)
        with tempfile.NamedTemporaryFile() as handle:
            with mock.patch.object(TIMELINE, "_probe", return_value={"streams": [
                probe["streams"][0], {"codec_type": "audio"}
            ]}):
                with self.assertRaisesRegex(ValueError, "must be silent"):
                    TIMELINE.inspect_source(Path(handle.name))


if __name__ == "__main__":
    unittest.main()
