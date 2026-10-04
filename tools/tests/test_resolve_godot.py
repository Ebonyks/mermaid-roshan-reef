import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from tools import resolve_godot as resolver


class GodotResolutionTests(unittest.TestCase):
	def setUp(self):
		self.data = resolver.baseline.load_baseline()

	def test_old_path_build_is_skipped(self):
		with patch.object(resolver, "candidates", return_value=["old", "approved"]), patch.object(resolver.baseline, "validate_executable", side_effect=[["4.7.1 mismatch"], []]):
			self.assertEqual(resolver.resolve(Path("."), self.data, None, {}), "approved")

	def test_explicit_mismatch_fails_without_fallback(self):
		with patch.object(resolver.baseline, "validate_executable", return_value=["wrong build"]), patch.object(resolver, "candidates") as options:
			with self.assertRaisesRegex(ValueError, "Explicit GODOT"):
				resolver.resolve(Path("."), self.data, "old", {})
			options.assert_not_called()

	def test_no_matching_build_fails(self):
		with patch.object(resolver, "candidates", return_value=[]):
			with self.assertRaisesRegex(ValueError, "No official"):
				resolver.resolve(Path("."), self.data, None, {})

	def test_explicit_relative_path_is_bound_to_selected_root(self):
		with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as caller:
			root = Path(directory)
			expected = str((root / "editor/approved.exe").resolve())
			previous = Path.cwd()
			try:
				os.chdir(caller)
				with patch.object(resolver.baseline, "validate_executable", return_value=[]) as validate:
					self.assertEqual(expected, resolver.resolve(root, self.data, "./editor/approved.exe", {}))
					validate.assert_called_once_with(expected, self.data)
			finally:
				os.chdir(previous)

	def test_development_baseline_rejected(self):
		data = {**self.data, "status": "dev7"}
		with self.assertRaises(ValueError):
			resolver.resolve(Path("."), data, None, {})


if __name__ == "__main__":
	unittest.main()
