import unittest
import tempfile
from pathlib import Path

from tools.run_advisory_sensor import classify, output_inventory, stale_requirements


class AdvisorySensorTests(unittest.TestCase):
	def test_nonzero_or_explicit_failure_never_measured(self):
		for output, code in (("LAGOONSHOT|RESULT|FAIL", 0), ("BALANCE|RESULT|ALL OK", 1), ("SCRIPT ERROR", 0)):
			self.assertEqual(classify(output, code, "", [])[0], "FAILED")

	def test_caps_unsupported_and_empty_are_distinct(self):
		self.assertEqual(classify("", 124, "", [])[0], "CAPPED")
		self.assertEqual(classify("BALANCE|verdict=capped", 0, "BALANCE|", [])[0], "CAPPED")
		self.assertEqual(classify("BALANCE|NOT_MEASURED", 0, "BALANCE|", [])[0], "NOT_MEASURED")
		self.assertEqual(classify("engine booted", 0, "BALANCE|", [])[0], "EMPTY")

	def test_missing_capture_cannot_be_measured(self):
		self.assertEqual(classify("SHOT|RESULT|ALL OK", 0, "SHOT|", ["*.png"])[0], "NOT_MEASURED")
		self.assertEqual(classify("SHOT|RESULT|ALL OK", 0, "SHOT|", [])[0], "MEASURED")

	def test_partial_cap_overrides_success(self):
		self.assertEqual(classify("BALANCE|verdict=capped\nBALANCE|RESULT|ALL OK", 0, "BALANCE|", [])[0], "CAPPED")

	def test_generic_failure_row_cannot_hide_behind_success(self):
		self.assertEqual(classify("SHOT|FAIL|blank\nSHOT|RESULT|ALL OK", 0, "SHOT|", [])[0], "FAILED")

	def test_actual_legacy_failure_formats_never_measured(self):
		for output in (
			"DUSTBAL|result: 2 FAILED",
			"NORTHSHOT|frame|FAIL\nNORTHSHOT|DONE|folder",
			"DUSTSHOT|frame|OK|path=SAVE_ERROR\nDUSTSHOT|DONE|folder",
		):
			with self.subTest(output=output):
				self.assertEqual("FAILED", classify(output, 0, "", [])[0])

	def test_legacy_human_art_save_error_cannot_hide_behind_done(self):
		output = "ART_AUDIT|saved bathroom -> /tmp/legacy-shots ERR 13\nART_AUDIT|DONE"
		self.assertEqual("FAILED", classify(output, 0, "ART_AUDIT|DONE", [])[0])
		self.assertEqual("MEASURED", classify(
			"ART_AUDIT|saved bathroom -> /tmp/legacy-shots\nART_AUDIT|DONE",
			0, "ART_AUDIT|DONE", [])[0])
	def test_metric_prefix_and_truncated_verdict_do_not_complete_run(self):
		for output in ("BALANCE|ROSTER|acts=15", "BALANCE|canvas|act=nursery|time=45", "BALANCE|RESULT|", "BALANCE|RESULT|unknown"):
			with self.subTest(output=output):
				self.assertEqual("EMPTY", classify(output, 0, "BALANCE|", [])[0])

	def test_current_and_legacy_completion_markers(self):
		for output, expected in (
			("BALANCE|RESULT|PASS|measured=45", "BALANCE|RESULT|"),
			("CASTLESHOT|RESULT|PASS|written=13", "CASTLESHOT|RESULT|"),
			("DUSTBAL|result: ALL OK", "DUSTBAL|result:"),
			("ARTMANIFEST|done", "ARTMANIFEST|done"),
			("NORTHSHOT|DONE|folder", "NORTHSHOT|DONE|"),
			("DUSTSHOT|DONE|folder", "DUSTSHOT|DONE|"),
		):
			with self.subTest(output=output):
				self.assertEqual("MEASURED", classify(output, 0, expected, [])[0])

	def test_incomplete_capture_cannot_hide_behind_some_fresh_outputs(self):
		for output in ("DUSTSHOT|INCOMPLETE|interrupted\nDUSTSHOT|DONE|folder", "NORTHSHOT|RESULT|HEADLESS SKIP"):
			self.assertEqual("NOT_MEASURED", classify(output, 0, "", [])[0])

	def test_old_outputs_do_not_count_as_current_capture(self):
		with tempfile.TemporaryDirectory() as folder:
			path = Path(folder) / "capture.png"
			path.write_bytes(b"old capture")
			patterns = [str(Path(folder) / "*.png")]
			before = output_inventory(patterns)
			self.assertEqual(patterns, stale_requirements(patterns, before, output_inventory(patterns)))
			path.write_bytes(b"current capture")
			self.assertEqual([], stale_requirements(patterns, before, output_inventory(patterns)))


if __name__ == "__main__":
	unittest.main()
