from __future__ import annotations

import math
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(path: str) -> str:
	return (ROOT / path).read_text(encoding="utf-8")


def _vector(source: str, name: str) -> tuple[float, float]:
	match = re.search(
		rf"{re.escape(name)}\.size\s*=\s*Vector2\(([-\d.]+),\s*([-\d.]+)\)",
		source,
	)
	if match is None:
		raise AssertionError(f"missing size for {name}")
	return float(match.group(1)), float(match.group(2))


def _style_size(source: str, name: str) -> int:
	match = re.search(
		rf"style_(?:label|button|picture_button)\({re.escape(name)},\s*(\d+)",
		source,
	)
	if match is None:
		raise AssertionError(f"missing style size for {name}")
	return int(match.group(1))


def _wrapped_lines(text: str, width: float, font_size: int) -> int:
	"""Conservative deterministic line count, independent of a font asset.

	0.70em is a deliberately wide average advance for this pre-font gate. A
	passing result therefore proves only this exact English/layout candidate;
	it is not glyph or device acceptance.
	"""
	capacity = max(1, int(width / (font_size * 0.70)))
	lines = 0
	for paragraph in text.split("\n"):
		words = paragraph.split()
		if not words:
			lines += 1
			continue
		current = 0
		for word in words:
			if current == 0:
				current = len(word)
			elif current + 1 + len(word) <= capacity:
				current += 1 + len(word)
			else:
				lines += 1
				current = len(word)
		lines += 1
	return lines


def _required_height(lines: int, font_size: int, outline: int) -> int:
	return lines * math.ceil(font_size * 1.25) + outline * 2


class TypeCLayoutTests(unittest.TestCase):
	def test_save_warning_is_child_safety_copy_and_fits_exact_english(self) -> None:
		source = _source("scripts/start_menu.gd")
		self.assertNotIn("adult_caption_adult_only_save_safety", source)
		self.assertIn('note.text = "Your saved adventure will be kept for a grown-up to restore."', source)
		self.assertIn("ROLE_STATUS", source)
		self.assertEqual(_style_size(source, "note"), 28)
		width, height = _vector(source, "note")
		text = "Your saved adventure will be kept for a grown-up to restore."
		lines = _wrapped_lines(text, width, 28)
		self.assertLessEqual(lines, 3)
		self.assertGreaterEqual(height, _required_height(lines, 28, 2))
		self.assertIn("note.max_lines_visible = 3", source)

	def test_wardrobe_locked_hint_has_reserved_picture_column(self) -> None:
		source = _source("scripts/wardrobe_ui.gd")
		self.assertIn("ROLE_CHILD_CONTROL, 28)", source)
		self.assertIn("b.alignment = HORIZONTAL_ALIGNMENT_RIGHT", source)
		self.assertIn("bt.alignment = HORIZONTAL_ALIGNMENT_RIGHT", source)
		width, height = _vector(source, "b")
		self.assertEqual((width, height), (480.0, 110.0))
		# Portrait 96px + 16px breathing room is not text-bearing width.
		available = width - 96.0 - 16.0
		current_labels = [
			"🔒 Fairy Mermaid",
			"✔ Roshan", "✔ Fairy Mermaid", "✔ Princess Huluu",
			"    Roshan", "    Fairy Mermaid", "    Princess Huluu",
		]
		for label in current_labels:
			with self.subTest(label=label):
				self.assertLessEqual(len(label) * 28 * 0.70, available)

	def test_craft_locked_choice_is_explicitly_deferred_not_claimed_fit(self) -> None:
		source = _source("scripts/craft_studio.gd")
		self.assertIn('button.text = ("▣  " + "◉".repeat(mini(price, 3)) + "\\n" + kind_name)', source)
		self.assertIn("style_button(button, \"locked\" if locked else \"secondary\", 24, 28)", source)
		self.assertIn("known sub-floor child surface", source)
		width, height = _vector(source, "button")
		current_locked = [
			"▣  ◉◉◉\n♧\nKITTY",
			"▣  ◉◉◉\n♢\nBIRDIE",
		]
		for locked in current_locked:
			with self.subTest(locked=locked):
				lines = _wrapped_lines(locked, width, 24)
				self.assertEqual(lines, 3)
				self.assertLessEqual(_required_height(lines, 24, 3), height)
		status = "▣  ◉◉◉\nExplore for more pearls"
		status_lines = _wrapped_lines(status, 175.0, 21)
		self.assertLessEqual(_required_height(status_lines, 21, 5), 150.0)
		self.assertLess(24, 28)  # the child-size repair remains explicitly open

	def test_other_fixed_box_enlargements_are_not_asserted_as_safe(self) -> None:
		companion = _source("scripts/companion.gd")
		self.assertIn('style_button(card, "selected" if id == m.companion_pick_id else "secondary", 24, 24)', companion)
		self.assertIn("style_label(nm, 26, StorybookUI.INK, 3)", companion)
		self.assertIn("style_label(atk, 24, StorybookUI.INK_SOFT, 2)", companion)
		main = _source("scripts/main.gd")
		self.assertIn("style_hud_label(hint, 24, StorybookUI.GOLD, 3)", main)
		wardrobe = _source("scripts/wardrobe_ui.gd")
		self.assertIn('font_size", 20 if earned else 15', wardrobe)
		self.assertIn("reserves only 72px", wardrobe)


if __name__ == "__main__":
	unittest.main()
