from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from tools import record_owner_decision as intake


class OwnerDecisionTests(unittest.TestCase):
	def setUp(self):
		self.temp = tempfile.TemporaryDirectory()
		self.addCleanup(self.temp.cleanup)
		self.root = Path(self.temp.name)
		(self.root / "note.md").write_text("Owner: yes", encoding="utf-8")
		(self.root / "check.py").write_text("assert True", encoding="utf-8")
		self.row = {"id": "ODR-TEST", "date": "2026-10-03", "subject": "A scope", "decision": "Keep the approved art", "source": "note.md", "question": "Q1", "authority": "recorded_owner", "cycle": None, "checks": []}
		self.data = {"schema": "owner_decisions/1", "decisions": [self.row]}

	def test_register_rejects_missing_or_escaped_evidence(self):
		for value in ("gone.md", "../note.md", ".secrets/key"):
			with self.subTest(value=value):
				data = copy.deepcopy(self.data)
				data["decisions"][0]["source"] = value
				self.assertTrue(intake.validate(self.root, data))

	def test_append_is_immutable_and_dates_are_explicit(self):
		answer = {**self.row, "id": "ODR-SECOND"}
		merged = intake.append(self.root, self.data, [answer], "2026-10-03", "2026-10-03")
		self.assertEqual(merged["decisions"][0], self.row)
		self.assertEqual(len(self.data["decisions"]), 1)
		self.assertEqual(merged["decisions"][1]["cycle"], "2026-10-03")
		with self.assertRaises(ValueError):
			intake.append(self.root, self.data, [answer], "2026-10-03", "2026-10-04")

	def test_defaults_never_count_as_answers(self):
		answer = {**self.row, "id": "ODR-DEFAULT", "authority": "operating_default"}
		with self.assertRaisesRegex(ValueError, "not owner answers"):
			intake.append(self.root, self.data, [answer], "2026-10-03", "2026-10-03")

	def test_no_duplicate_or_more_than_five_answers(self):
		with self.assertRaises(ValueError):
			intake.append(self.root, self.data, [self.row], "cycle-1", "2026-10-03")
		with self.assertRaises(ValueError):
			intake.append(self.root, self.data, [self.row] * 6, "cycle-1", "2026-10-03")

	def test_checkable_correction_needs_check(self):
		self.row["checkable"] = True
		self.assertTrue(intake.validate(self.root, self.data))
		self.row["checks"] = ["check.py"]
		self.assertFalse(intake.validate(self.root, self.data))

	def test_document_and_string_flag_cannot_masquerade_as_executable_check(self):
		self.row.update(checkable=True, checks=["note.md"])
		self.assertTrue(intake.validate(self.root, self.data))
		self.row.update(checkable="true", checks=["check.py"])
		self.assertTrue(intake.validate(self.root, self.data))

	def test_render_preserves_authority_and_escapes_table_cells(self):
		self.row["decision"] = "A | B\nC"
		text = intake.render(self.data)
		self.assertIn("A \\| B C", text)
		self.assertIn("recorded_owner", text)


class AppendOnlyTests(unittest.TestCase):
	def test_changed_removed_and_reordered_decisions_are_rejected(self):
		first = {"id": "ODR-A", "decision": "Keep it"}
		second = {"id": "ODR-B", "decision": "Add it"}
		before = {"decisions": [first, second]}
		self.assertEqual([], intake.append_only_issues(before, {"decisions": [first, second, {"id": "ODR-C"}]}))
		self.assertTrue(intake.append_only_issues(before, {"decisions": [first]}))
		self.assertTrue(intake.append_only_issues(before, {"decisions": [first, {**second, "decision": "Rewritten"}]}))
		self.assertTrue(intake.append_only_issues(before, {"decisions": [second, first]}))

	def test_live_register_only_appends_since_the_comparison_base(self):
		import json
		import subprocess
		from tools import audit_development
		root = Path(__file__).resolve().parents[2]
		try:
			base = audit_development.resolve_base(root, "auto")
		except (subprocess.CalledProcessError, OSError, ValueError, KeyError):
			self.skipTest("No comparison base in this checkout")
		before = intake.register_at(root, base)
		if before is None:
			self.skipTest("Register did not exist at the comparison base")
		after = json.loads((root / intake.REGISTER).read_text(encoding="utf-8"))
		self.assertEqual([], intake.append_only_issues(before, after))


if __name__ == "__main__":
	unittest.main()
