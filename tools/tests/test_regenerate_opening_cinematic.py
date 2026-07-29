"""Structural tests for the deterministic opening-cinematic regeneration."""
import importlib.util
import sys
import unittest
from pathlib import Path


TOOL = Path(__file__).parents[1] / "regenerate_opening_cinematic.py"
SPEC = importlib.util.spec_from_file_location("regenerate_opening_cinematic", TOOL)
REGEN = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = REGEN
SPEC.loader.exec_module(REGEN)


class OpeningCinematicRegenerationTests(unittest.TestCase):
    def test_timeline_has_approved_duration(self):
        self.assertEqual(
            sum(shot.duration_frames for shot in REGEN.SHOTS),
            REGEN.OUTPUT_FRAME_COUNT,
        )
        self.assertEqual(REGEN.OUTPUT_FRAME_COUNT / REGEN.FPS, 42.5)

    def test_prohibited_groups_are_not_reused(self):
        used = {
            group
            for shot in REGEN.SHOTS
            for group in shot.source_groups
        }
        self.assertNotIn(10, used)
        self.assertNotIn(29, used)

    def test_final_two_shots_use_locked_handhold_frame(self):
        self.assertEqual(REGEN.source_indices(REGEN.SHOTS[-2], "adaptive"), [260])
        self.assertEqual(REGEN.source_indices(REGEN.SHOTS[-1], "adaptive"), [260])

    def test_frame_distribution_is_exact(self):
        self.assertEqual(REGEN.distribute(10, 3), [4, 3, 3])
        self.assertEqual(sum(REGEN.distribute(66, 5)), 66)
        weighted = REGEN.distribute_quiet_motion_quiet(24, 5)
        self.assertEqual(sum(weighted), 24)
        self.assertGreater(weighted[0], weighted[2])
        self.assertGreater(weighted[-1], weighted[2])


if __name__ == "__main__":
    unittest.main()
