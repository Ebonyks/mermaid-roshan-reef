import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "audit_audio_quality", ROOT / "tools" / "audit_audio_quality.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AudioQualityPolicyTests(unittest.TestCase):
    def test_protected_inventory_is_explicit(self):
        self.assertEqual(len(MODULE.PROTECTED), 6)
        self.assertNotIn("assets/audio/voice_yay.mp3", MODULE.PROTECTED)
        self.assertIn("assets/audio/voices/chuck_whimper.ogg", MODULE.PROTECTED)
        self.assertIn("assets/audio/voices/daddy1.ogg", MODULE.PROTECTED)

    def test_legacy_low_music_is_not_upgraded_by_metadata(self):
        meta = {"decode_ok": True, "duration_seconds": 8.0}
        for path in MODULE.LEGACY_LOW_MUSIC:
            self.assertEqual(
                MODULE.grade(path, meta, -8.0),
                ("D", 2, "P2", "LISTEN_REPLACE_CANDIDATE"),
            )

    def test_provisional_yay_has_no_fabricated_human_grade(self):
        meta = {"decode_ok": True, "duration_seconds": 1.0}
        self.assertEqual(
            MODULE.grade("assets/audio/voices/filler_v1/yay.ogg", meta, -6.0),
            ("A", "", "P1", "REVIEW_PROVISIONAL_FILLER"),
        )

    def test_clipping_precedes_other_dispositions(self):
        meta = {"decode_ok": True, "duration_seconds": 1.0}
        self.assertEqual(
            MODULE.grade("assets/audio/ui_tap.ogg", meta, 0.1),
            ("F", 1, "P1", "REPLACE_CLIPPING"),
        )

    def test_new_exact_racer_voices_are_review_gated(self):
        meta = {"decode_ok": True, "duration_seconds": 2.0}
        for path in MODULE.NEW_EXACT_VOICES:
            self.assertEqual(
                MODULE.grade(path, meta, -2.0),
                ("A", 4, "P1", "REVIEW_NEW_EXACT_VOICE"),
            )

    def test_faron_is_protected_by_speaker_and_filler_is_not(self):
        self.assertEqual(
            MODULE.protected_kind("assets/audio/voices/faron_op_nursery_bedtime.ogg"),
            "protected_faron",
        )
        self.assertIsNone(
            MODULE.protected_kind("assets/audio/voices/filler_v1/faron_fake.ogg"))

    def test_filler_manifest_absence_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            state = MODULE.validate_filler_manifest(Path(directory))
        self.assertFalse(state["present"])
        self.assertFalse(state["blocking"])

    def test_filler_manifest_validates_set_hash_and_delivery_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            audio = filler / "roshan_win.ogg"
            audio.write_bytes(b"fixture ogg")
            payload = {
                "entries": [{
                    "key": "roshan_win",
                    "character": "roshan", "text": "Yay! I did it!",
                    "status": "PROVISIONAL_SYNTHETIC_FILLER",
                    "selected_attempt": 1, "generation_text": "Yay! I did it!",
                    "generation_segments": ["Yay! I did it!"],
                    "segment_seeds": [1], "source_wav_sha256": "1" * 64,
                    "speaker_preset": "Laura", "description": "fixture",
                    "selection_metrics": {
                        "semantic_gate_schema": 3,
                        "semantic_gate_expected_words": ["yay", "i", "did", "it"],
                        "semantic_gate_transcript_words": ["yay", "i", "did", "it"],
                    },
                    "final_ogg_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
                    "delivery_metrics": {
                        "codec": "vorbis", "sample_rate_hz": 48000,
                        "channels": 1, "bit_rate_bps": 96000,
                        "integrated_lufs": -16.0, "true_peak_dbtp": -2.0,
                        "duration_s": 1.0, "decoded_clipped_samples": 0,
                        "dc_offset": 0.0,
                    },
                }],
                "generation_run_provenance": {"attempt_1": {"attempt": 1}},
            }
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps(payload), encoding="utf-8")
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            try:
                state = MODULE.validate_filler_manifest(root, {
                    "roshan_win": ("roshan", "Yay! I did it!"),
                })
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
        self.assertTrue(state["present"])
        self.assertFalse(state["blocking"], state["issues"])

    def test_filler_manifest_rejects_unlisted_ogg_and_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            listed = filler / "roshan_win.ogg"
            listed.write_bytes(b"fixture ogg")
            (filler / "unlisted.ogg").write_bytes(b"extra")
            payload = {"entries": [{
                "key": "roshan_win", "final_ogg_sha256": "0" * 64,
                "delivery_metrics": {
                    "codec": "vorbis", "sample_rate_hz": 48000,
                    "channels": 1, "bit_rate_bps": 96000,
                    "integrated_lufs": -16.0, "true_peak_dbtp": -2.0,
                },
            }]}
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps(payload), encoding="utf-8")
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            try:
                state = MODULE.validate_filler_manifest(root, {
                    "roshan_win": ("roshan", "Yay! I did it!"),
                })
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
        self.assertTrue(state["blocking"])
        self.assertTrue(any("unlisted filler OGG" in issue for issue in state["issues"]))
        self.assertTrue(any("hash mismatch" in issue for issue in state["issues"]))

    def test_filler_manifest_rejects_incomplete_authoritative_cohort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps({"entries": [], "generation_run_provenance": {}}),
                encoding="utf-8",
            )
            state = MODULE.validate_filler_manifest(root, {
                "roshan_talk": ("roshan", "This is so much fun!"),
                "yay": ("roshan", "Yay!"),
            })
        self.assertTrue(state["blocking"])
        self.assertTrue(any(
            "authoritative filler key missing" in issue for issue in state["issues"]))

    def test_filler_rows_are_distinct_and_mark_legacy_shadowing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            voice_dir = root / "assets/audio/voices"
            filler = voice_dir / "filler_v1"
            filler.mkdir(parents=True)
            (voice_dir / "roshan_win.ogg").write_bytes(b"legacy")
            (filler / "roshan_win.ogg").write_bytes(b"filler")
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            try:
                rows = MODULE.build_rows(root, {
                    "present": True, "blocking": False,
                    "expected_names": {"roshan_win.ogg"},
                })
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
        by_path = {row["path"]: row for row in rows}
        self.assertEqual(by_path["assets/audio/voices/filler_v1/roshan_win.ogg"]["cohort"], "filler_v1")
        self.assertEqual(by_path["assets/audio/voices/roshan_win.ogg"]["cohort"], "legacy_voice")
        self.assertEqual(
            by_path["assets/audio/voices/roshan_win.ogg"]["shadowed_by_filler_path"],
            "assets/audio/voices/filler_v1/roshan_win.ogg",
        )


if __name__ == "__main__":
    unittest.main()
