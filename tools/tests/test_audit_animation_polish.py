from __future__ import annotations

import unittest

from tools import audit_animation_polish as audit


def _juice_text() -> str:
	return (audit.REPO / audit.JUICE).read_text(encoding="utf-8")


class AnimationPolishAuditTests(unittest.TestCase):
	def test_committed_vocabulary_and_exemplars_are_green(self) -> None:
		self.assertEqual(audit.validate_vocabulary(_juice_text()), [])
		self.assertEqual(audit.validate_exemplars(audit.REPO), [])

	def test_missing_constant_is_rejected(self) -> None:
		text = _juice_text().replace("const MIN_PULSE_PERIOD := ", "const RENAMED := ")
		self.assertTrue(any("MIN_PULSE_PERIOD" in error
			for error in audit.validate_vocabulary(text)))

	def test_lost_tree_guard_is_rejected(self) -> None:
		text = _juice_text().replace("is_inside_tree()", "true", 1000)
		self.assertTrue(any("is_inside_tree" in error
			for error in audit.validate_vocabulary(text)))

	def test_lost_rest_scale_discipline_is_rejected(self) -> None:
		text = _juice_text().replace("juice_rest_scale", "some_other_meta")
		self.assertTrue(any("rest-scale" in error
			for error in audit.validate_vocabulary(text)))

	def test_too_fast_pulse_default_is_rejected(self) -> None:
		text = _juice_text().replace("half: float = 0.18", "half: float = 0.05")
		self.assertTrue(any("MIN_PULSE_PERIOD" in error
			for error in audit.validate_vocabulary(text)))

	def test_overlong_default_duration_is_rejected(self) -> None:
		text = _juice_text().replace("dur: float = 0.30", "dur: float = 3.0")
		self.assertTrue(any("outside [MIN_DUR, MAX_DUR]" in error
			for error in audit.validate_vocabulary(text)))

	def test_unwired_exemplar_is_rejected(self) -> None:
		broken = list(audit.EXEMPLARS) + [
			("scripts/medal_system.gd", "Juice.never_wired(", "synthetic")]
		original = audit.EXEMPLARS
		audit.EXEMPLARS = tuple(broken)
		try:
			self.assertTrue(any("exemplar unwired" in error
				for error in audit.validate_exemplars(audit.REPO)))
		finally:
			audit.EXEMPLARS = original


if __name__ == "__main__":
	unittest.main()
