"""Authored musical form must survive rendering without rotated notes or roots."""
from copy import deepcopy
import math
from pathlib import Path
import unittest
from unittest.mock import patch

from tools import build_area_music as music

ROOT = Path(__file__).resolve().parents[2]


class AuthoredAreaMusicTests(unittest.TestCase):
    def setUp(self):
        self.catalog, self.cues = music._load_catalog(ROOT)
        self.cue = deepcopy(next(c for c in self.cues if c["id"] == "castle_opera_hall"))

    def test_hook_returns_then_resolves_with_space(self):
        bars = self.cue["authored_melody"]["bars"]
        self.assertEqual([n[0] for n in bars[0]], self.catalog["roshan_motif"]["scale_degrees"])
        self.assertEqual(bars[0], bars[2])
        self.assertNotEqual(bars[:4], bars[4:])
        self.assertEqual(bars[-1], [[0, 4], [None, 2]])
        self.assertEqual([music._developed_root(self.cue, b, 8)[0] for b in range(8)],
                         self.cue["progression"])
        self.assertEqual(self.cue["progression"][-2:], [4, 0])

    def test_renderer_preserves_timing_rests_and_centered_lead(self):
        clock = music._cue_clock(self.cue)
        with patch.object(music, "_add_note") as add:
            music._arrange_melody(None, self.cue, self.catalog, clock[1], clock[2], clock[3])
        calls = add.call_args_list
        expected = []
        for bar, events in enumerate(self.cue["authored_melody"]["bars"]):
            cursor = float(bar * 6)
            for degree, duration in events:
                if degree is not None:
                    expected.append((degree, cursor, duration * .92))
                cursor += duration
        self.assertEqual(len(calls), len(expected) + 1)  # Only the final bell is additional.
        for call, (degree, start, duration) in zip(calls, expected):
            self.assertEqual(call.args[3:6], (degree, start, duration))
            self.assertEqual(call.args[7], 0.0)
        self.assertEqual(calls[-1].args[4], 42.0)

    def test_rejects_missing_bars_and_wrong_harmonic_form(self):
        for key in ("bars", "bar_gains"):
            cue = deepcopy(self.cue)
            cue["authored_melody"][key].pop()
            with self.subTest(key=key), self.assertRaises(ValueError):
                music._validate_cue(cue)
        self.cue["progression"][-1] = 4
        with self.assertRaises(ValueError):
            music._validate_cue(self.cue)

    def test_rejects_overfull_underfull_and_nonfinite_events(self):
        for value in (0, -1, .5, 2, math.nan, math.inf, True, "1"):
            cue = deepcopy(self.cue)
            cue["authored_melody"]["bars"][0][0][1] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                music._validate_cue(cue)

    def test_rejects_invalid_pitch_dynamics_and_register(self):
        for degree in (True, "C", 1.5, 100):
            cue = deepcopy(self.cue)
            cue["authored_melody"]["bars"][0][0][0] = degree
            with self.subTest(degree=degree), self.assertRaises(ValueError):
                music._validate_cue(cue)
        for gain in (0, -1, math.nan, math.inf, 2, True):
            cue = deepcopy(self.cue)
            cue["authored_melody"]["bar_gains"][0] = gain
            with self.subTest(gain=gain), self.assertRaises(ValueError):
                music._validate_cue(cue)
        self.cue["authored_melody"]["octave"] = 3
        with self.assertRaises(ValueError):
            music._validate_cue(self.cue)

    def test_rejects_explicit_null_instead_of_crashing_during_render(self):
        self.cue["authored_melody"] = None
        with self.assertRaises(ValueError):
            music._validate_cue(self.cue)

    def test_only_commissioned_cue_opts_into_authored_form(self):
        self.assertEqual([c["id"] for c in self.cues if "authored_melody" in c],
                         ["castle_opera_hall"])


if __name__ == "__main__":
    unittest.main()
