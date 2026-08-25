import importlib.util
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
        self.assertIn("assets/audio/voice_yay.mp3", MODULE.PROTECTED)
        self.assertIn("assets/audio/voices/daddy1.ogg", MODULE.PROTECTED)

    def test_legacy_low_music_is_not_upgraded_by_metadata(self):
        meta = {"decode_ok": True, "duration_seconds": 8.0}
        for path in MODULE.LEGACY_LOW_MUSIC:
            self.assertEqual(
                MODULE.grade(path, meta, -8.0),
                ("D", 2, "P2", "LISTEN_REPLACE_CANDIDATE"),
            )

    def test_objective_fallback_remains_a_p1(self):
        meta = {"decode_ok": True, "duration_seconds": 1.0}
        self.assertEqual(
            MODULE.grade("assets/audio/voice_yay.mp3", meta, -6.0),
            ("C", 1, "P1", "KEEP_PROTECTED_RESTRICT_FALLBACK"),
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


if __name__ == "__main__":
    unittest.main()
