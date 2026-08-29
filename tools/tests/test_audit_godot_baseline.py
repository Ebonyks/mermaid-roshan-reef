from __future__ import annotations

import copy
import unittest

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


if __name__ == "__main__":
	unittest.main()
