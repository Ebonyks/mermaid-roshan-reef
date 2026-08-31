from __future__ import annotations

import copy
import json
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

	def test_canonical_engine_contract_is_derived_from_json(self) -> None:
		data = copy.deepcopy(audit.load_baseline())
		canonical = audit.canonical_engine_contract(data)
		self.assertEqual(canonical["version_string"], "4.7.2-stable (official)")
		data["version"] = "4.7.3"
		data["release"] = "4.7.3-stable"
		for entry in data["downloads"].values():
			entry["filename"] = entry["filename"].replace("4.7.2-stable", "4.7.3-stable")
		mutated = audit.canonical_engine_contract(data)
		self.assertNotEqual(canonical, mutated)
		self.assertEqual(mutated["version_string"], "4.7.3-stable (official)")

	def test_malformed_baseline_fails_closed(self) -> None:
		with tempfile.TemporaryDirectory() as raw_path:
			path = Path(raw_path) / "godot_baseline.json"
			path.write_text("{not-json", encoding="utf-8")
			with self.assertRaises(audit.BaselineError):
				audit.load_baseline(path)
			path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
			with self.assertRaises(audit.BaselineError):
				audit.load_baseline(path)


if __name__ == "__main__":
	unittest.main()
