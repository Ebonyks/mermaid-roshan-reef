#!/usr/bin/env python3
"""Focused tests for deterministic Castle depth-card refinement."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image


TOOL = Path(__file__).with_name("refine_castle_depth_cards.py")
SPEC = importlib.util.spec_from_file_location("castle_depth_refiner", TOOL)
assert SPEC is not None and SPEC.loader is not None
REFINE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REFINE
SPEC.loader.exec_module(REFINE)


class CastleDepthRefinerTests(unittest.TestCase):
	def setUp(self) -> None:
		self.temporary = tempfile.TemporaryDirectory()
		self.root = Path(self.temporary.name)
		self.saved_paths = (
			REFINE.ROOT, REFINE.ROOM_DIR, REFINE.SOURCE_ROOT,
			REFINE.SOURCE_ALPHA_ROOT,
		)
		REFINE.ROOT = self.root
		REFINE.ROOM_DIR = self.root / "assets/flats/castle/rooms"
		REFINE.SOURCE_ROOT = self.root / "assets_src/castle/depth_cards"
		REFINE.SOURCE_ALPHA_ROOT = REFINE.SOURCE_ROOT / "source_alpha"
		REFINE.ROOM_DIR.mkdir(parents=True)
		REFINE.SOURCE_ALPHA_ROOT.mkdir(parents=True)

	def tearDown(self) -> None:
		(
			REFINE.ROOT, REFINE.ROOM_DIR, REFINE.SOURCE_ROOT,
			REFINE.SOURCE_ALPHA_ROOT,
		) = self.saved_paths
		self.temporary.cleanup()

	def _fixture(self, method: str = "reviewed") -> object:
		room = np.zeros((8, 10, 3), dtype=np.uint8)
		room[:, :] = (24, 96, 180)
		Image.fromarray(room, "RGB").save(REFINE.ROOM_DIR / "room_test.png")
		card = np.zeros((4, 6, 4), dtype=np.uint8)
		card[:, :, :3] = (24, 96, 180)
		card[:, :, 3] = 255
		Image.fromarray(card, "RGBA").save(
			REFINE.ROOM_DIR / "room_test_front_left.png")
		Image.fromarray(card[:, :, 3], "L").save(
			REFINE.SOURCE_ALPHA_ROOT / "room_test_front_left_alpha.png")
		return REFINE.CardSpec(
			"test", "front_left", (2, 2),
			(REFINE.rounded_rectangle((1, 1, 4, 3), 0),), method)

	def test_shape_rasterizer_supports_all_declared_shape_types(self) -> None:
		mask = np.asarray(REFINE.rasterize_shapes((12, 10), (
			REFINE.polygon((1, 1), (3, 1), (2, 3)),
			REFINE.ellipse((5, 1, 8, 4)),
			REFINE.rounded_rectangle((8, 5, 11, 9), 1),
		)))
		self.assertEqual(255, int(mask[2, 2]))
		self.assertEqual(255, int(mask[2, 6]))
		self.assertEqual(255, int(mask[7, 9]))
		self.assertEqual(0, int(mask[0, 0]))

	def test_refinement_keeps_exact_room_rgb_and_zeros_hidden_rgb(self) -> None:
		output, _source = REFINE.refined_card(self._fixture())
		rgba = np.asarray(output)
		visible = rgba[:, :, 3] > 0
		self.assertTrue(np.all(rgba[visible, :3] == (24, 96, 180)))
		self.assertTrue(np.all(rgba[~visible, :3] == 0))

	def test_alpha_scissor_core_never_escapes_hard_keep_shape(self) -> None:
		spec = self._fixture()
		output, _source = REFINE.refined_card(spec)
		alpha = np.asarray(output.getchannel("A"))
		hard_keep = np.asarray(REFINE.rasterize_shapes(output.size, spec.keep_shapes))
		self.assertFalse(np.any(
			(alpha >= REFINE.ALPHA_SCISSOR_THRESHOLD) & (hard_keep == 0)))
		self.assertTrue(np.any(
			(alpha > 0) & (alpha < REFINE.ALPHA_SCISSOR_THRESHOLD)))

	def test_png_encoding_is_deterministic(self) -> None:
		output, _source = REFINE.refined_card(self._fixture())
		self.assertEqual(REFINE.png_bytes(output), REFINE.png_bytes(output))


if __name__ == "__main__":
	unittest.main()
