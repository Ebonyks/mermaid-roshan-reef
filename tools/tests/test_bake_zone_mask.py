#!/usr/bin/env python3
"""Regression coverage for Baby Eagle's three coherent paint regions."""

from pathlib import Path
import unittest

import numpy as np
from PIL import Image

from tools import bake_zone_mask


ROOT = Path(__file__).resolve().parents[2]


class BabyEagleZoneMaskTests(unittest.TestCase):
	def test_shipped_birdie_atlas_exposes_anatomical_signals(self) -> None:
		base_path = ROOT / "assets" / "props" / "gen2" / "craft_birdie_base_color.jpg"
		mask_path = ROOT / "assets" / "props" / "gen2" / "craft_birdie_mask.png"
		with Image.open(base_path) as source:
			base = np.asarray(source.convert("RGB"))
		self.assertEqual(base.shape, (1024, 1024, 3))
		with Image.open(mask_path) as source:
			mask = np.asarray(source.convert("RGB"))
		self.assertEqual(mask.shape, (1024, 1024, 3))
		self.assertTrue(np.all((mask > 0).sum(axis=2) <= 1))
		self.assertTrue(np.all(mask.sum(axis=(0, 1)) > 25000))

	def test_birdie_classifier_keeps_regions_anatomical_and_one_hot(self) -> None:
		points = np.zeros((3, 3, 3), dtype=np.float64)
		points[..., 0] = 0.24
		points[..., 1] = 0.70
		points[..., 2] = 0.0
		wing = np.zeros((3, 3), dtype=np.float64)
		feet = np.zeros((3, 3), dtype=np.float64)
		filled = np.ones((3, 3), dtype=bool)
		albedo = np.full((3, 3, 3), 0.55, dtype=np.float64)

		# Strong rig ownership is a wing even on neutral albedo.
		wing[0, 0] = 0.70
		# Authored pink may extend a feather edge, but only near a wing.
		wing[0, 1] = 0.25
		albedo[0, 1] = (0.90, 0.25, 0.55)
		# The same pink texel away from a wing cannot spill onto the torso.
		albedo[0, 2] = (0.90, 0.25, 0.55)

		# Detail is one centered, front-facing breast shield.
		points[1, 0] = (0.0, 0.405, 0.10)
		# Beak and articulated foot ownership remain fixed (black mask).
		points[1, 1] = (0.0, 0.70, 0.22)
		feet[1, 2] = 0.80
		# The crest belongs to the accent region.
		points[2, 0] = (0.0, 0.95, 0.0)

		labels = bake_zone_mask.classify_birdie(points, wing, feet, filled, albedo)
		self.assertTrue(labels[0, 0, 1])
		self.assertTrue(labels[0, 1, 1])
		self.assertTrue(labels[0, 2, 0])
		self.assertTrue(labels[1, 0, 2])
		self.assertFalse(labels[1, 1].any())
		self.assertFalse(labels[1, 2].any())
		self.assertTrue(labels[2, 0, 1])
		self.assertTrue(np.all(labels.sum(axis=2) <= 1))

	def test_shipped_mask_is_categorical_and_has_three_visible_regions(self) -> None:
		path = ROOT / "assets" / "props" / "gen2" / "craft_birdie_mask.png"
		with Image.open(path) as source:
			mask = np.asarray(source.convert("RGB"))
		self.assertEqual(mask.shape, (1024, 1024, 3))
		self.assertTrue(np.all(np.isin(mask, (0, 255))))
		self.assertTrue(np.all((mask > 0).sum(axis=2) <= 1))
		zone_pixels = (mask > 0).sum(axis=(0, 1))
		self.assertTrue(np.all(zone_pixels > 25000), zone_pixels)


if __name__ == "__main__":
	unittest.main()
