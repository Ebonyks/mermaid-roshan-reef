from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
MAKE_VOICES = ROOT / "tools" / "make_voices.py"
FARON_MISS = ("faron", "Whoopsie! The pillow caught the baby. Try again!")


def lines_dict(source: str) -> ast.Dict:
	tree = ast.parse(source)
	assignments = [
		node
		for node in tree.body
		if isinstance(node, ast.Assign)
		and any(isinstance(target, ast.Name) and target.id == "LINES" for target in node.targets)
	]
	if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Dict):
		raise AssertionError("make_voices.py must define exactly one literal LINES dictionary")
	return assignments[0].value


def duplicate_literal_keys(dictionary: ast.Dict) -> list[str]:
	keys = [
		key.value
		for key in dictionary.keys
		if isinstance(key, ast.Constant) and isinstance(key.value, str)
	]
	return sorted(key for key, count in Counter(keys).items() if count > 1)


class VoiceLineManifestTests(unittest.TestCase):
	def test_lines_has_no_duplicate_literal_keys(self) -> None:
		dictionary = lines_dict(MAKE_VOICES.read_text(encoding="utf-8"))
		self.assertEqual(duplicate_literal_keys(dictionary), [])

	def test_duplicate_literal_key_guard_detects_shadowing(self) -> None:
		dictionary = lines_dict('LINES = {"same": 1, "same": 2, "other": 3}')
		self.assertEqual(duplicate_literal_keys(dictionary), ["same"])

	def test_faron_miss_is_the_single_pillow_safe_transcript(self) -> None:
		dictionary = lines_dict(MAKE_VOICES.read_text(encoding="utf-8"))
		matches = [
			ast.literal_eval(value)
			for key, value in zip(dictionary.keys, dictionary.values)
			if isinstance(key, ast.Constant) and key.value == "faron_miss"
		]
		self.assertEqual(matches, [FARON_MISS])


if __name__ == "__main__":
	unittest.main()
