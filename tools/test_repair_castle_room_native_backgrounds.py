#!/usr/bin/env python3
"""Regression tests for live-alpha Castle background repair policy."""

from __future__ import annotations

import io
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

from tools import repair_castle_room_native_backgrounds as repair


class CastleRoomNativeBackgroundRepairTests(unittest.TestCase):
	def test_pixel_identical_existing_png_encoding_is_preserved(self) -> None:
		image = Image.new("RGB", (8, 6), (24, 96, 180))
		metadata = PngInfo()
		metadata.add_text("test-encoding", "intentionally different")
		stream = io.BytesIO()
		image.save(stream, format="PNG", compress_level=0, pnginfo=metadata)
		existing_bytes = stream.getvalue()
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "same-pixels-different-encoding.png"
			path.write_bytes(existing_bytes)
			self.assertEqual(
				repair._png_bytes_preserving_pixels(path, image),
				existing_bytes)

	def test_pixel_change_never_preserves_existing_png_encoding(self) -> None:
		existing = Image.new("RGB", (8, 6), (24, 96, 180))
		changed = existing.copy()
		changed.putpixel((3, 2), (25, 96, 180))
		with tempfile.TemporaryDirectory() as directory:
			path = Path(directory) / "changed-pixel.png"
			path.write_bytes(repair._png_bytes(existing))
			output = repair._png_bytes_preserving_pixels(path, changed)
			with Image.open(io.BytesIO(output)) as rebuilt:
				self.assertEqual(rebuilt.convert("RGB").tobytes(), changed.tobytes())
			self.assertNotEqual(output, path.read_bytes())

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
