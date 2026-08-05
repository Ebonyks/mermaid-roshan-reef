#!/usr/bin/env python3
"""Regression tests for live-alpha Castle background repair policy."""

from __future__ import annotations

import unittest

from PIL import Image, ImageDraw

from tools import repair_castle_room_native_backgrounds as repair


class CastleRoomNativeBackgroundRepairTests(unittest.TestCase):
	def test_review_font_pixels_are_repeatable_without_os_font_lookup(self) -> None:
		def render() -> bytes:
			image = Image.new("L", (180, 40), 0)
			ImageDraw.Draw(image).text(
				(2, 2), "POOL APPROVED", fill=255,
				font=repair._font(18, bold=True))
			return image.tobytes()

		self.assertEqual(render(), render())
		self.assertGreater(sum(render()), 0)

	def test_retired_pool_water_card_is_not_a_background_heal_mask(self) -> None:
		self.assertFalse(repair._static_card_is_active(
			"mermaid_pool", "mid_pool"))
		self.assertTrue(repair._static_card_is_active(
			"mermaid_pool", "front_left"))
		self.assertTrue(repair._static_card_is_active(
			"bubble_bath", "front_right"))


if __name__ == "__main__":
	unittest.main()
