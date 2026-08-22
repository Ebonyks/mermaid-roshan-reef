from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools import check_grade_headroom as gate


class GradeHeadroomConsoleTests(unittest.TestCase):
	def test_true_2d_castle_uses_pixel_identity_profile(self) -> None:
		with (
			patch.object(gate, "parse_profiles", return_value=({}, {
				"warm_pastel": {
					"full_exposure": 0.92,
					"white_point": 1.62,
					"brightness": 1.0,
					"contrast": 1.0,
					"saturation": 1.0,
				},
			})),
			patch.object(gate, "parse_castle_room", return_value=None),
		):
			table = gate.build_profile_table()
		self.assertIsNone(table["castle_room"])

	def test_gate_output_is_safe_on_windows_cp1252_console(self) -> None:
		buffer = io.BytesIO()
		console = io.TextIOWrapper(buffer, encoding="cp1252")
		profile = (1.0,) * 9
		with (
			patch.object(gate, "ZONES", {
				"test_zone": ("test_profile", ["fake.png"], 1.0, 1.0),
			}),
			patch.object(gate, "REPORT_ONLY", set()),
			patch.object(gate, "build_profile_table", return_value={
				"test_profile": profile,
			}),
			patch.object(Path, "glob", return_value=[Path("fake.png")]),
			patch.object(gate, "measure", return_value=(0.0, 0.1, 0.0, 0.1)),
			redirect_stdout(console),
		):
			self.assertEqual(gate.main([]), 0)
		console.flush()
		self.assertIn(b"clip% in->out", buffer.getvalue())


if __name__ == "__main__":
	unittest.main()
