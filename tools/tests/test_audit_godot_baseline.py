from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from tools import audit_godot_baseline as audit


class GodotBaselineAuditTests(unittest.TestCase):
	def test_committed_baseline_and_pins_are_consistent(self) -> None:
		data = audit.load_baseline()
		self.assertEqual(audit.validate_metadata(data), [])
		self.assertEqual(audit.validate_file_pins(audit.REPO, data), [])

	def test_mismatched_release_is_rejected(self) -> None:
		data = copy.deepcopy(audit.load_baseline())
		data["release"] = "4.7.1-stable"
		self.assertTrue(any("does not match" in error
			for error in audit.validate_metadata(data)))

	def test_non_stable_baseline_is_rejected(self) -> None:
		data = copy.deepcopy(audit.load_baseline())
		data["status"] = "dev4"
		self.assertTrue(any("must be stable" in error
			for error in audit.validate_metadata(data)))

	def test_capture_contract_drift_is_rejected(self) -> None:
		data = audit.load_baseline()
		with tempfile.TemporaryDirectory() as temp:
			root = Path(temp)
			for relative, pins in audit.required_pins(data).items():
				path = root / relative
				path.parent.mkdir(parents=True, exist_ok=True)
				path.write_text("\n".join(pins), encoding="utf-8")
			self.assertEqual([], audit.validate_file_pins(root, data))
			capture = root / "scripts/probe_opera_art.gd"
			capture.write_text(capture.read_text(encoding="utf-8").replace(
				'int(engine["patch"]) == int(parts[2])', 'int(engine["patch"]) == 1'), encoding="utf-8")
			self.assertTrue(any("scripts/probe_opera_art.gd" in error for error in audit.validate_file_pins(root, data)))
			validator = root / "tools/audit_opera_capture.py"
			validator.write_text(validator.read_text(encoding="utf-8").replace(
				"wanted_engine = expected_engine(source_root)", "wanted_engine = stale_engine"), encoding="utf-8")
			self.assertTrue(any("tools/audit_opera_capture.py" in error for error in audit.validate_file_pins(root, data)))


if __name__ == "__main__":
	unittest.main()
