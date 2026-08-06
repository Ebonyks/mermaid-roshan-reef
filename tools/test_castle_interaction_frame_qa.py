#!/usr/bin/env python3
"""Focused mutation tests for per-frame castle composite QA primitives."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import castle_interaction_frame_qa as qa  # noqa: E402


def rgba(size: tuple[int, int], color: tuple[int, int, int, int]) -> Image.Image:
	return Image.new("RGBA", size, color)


def mask_from_array(values: np.ndarray) -> Image.Image:
	return Image.fromarray(values.astype(np.uint8) * 255, mode="L")


def placed_from_room_rgba(image: Image.Image) -> qa.PlacedFrame:
	alpha = qa.binary_mask(image.getchannel("A"))
	values = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
	values[np.asarray(alpha, dtype=np.uint8) == 0] = 0
	return qa.PlacedFrame(Image.fromarray(values, "RGBA"), alpha)


class CastleInteractionFrameQATests(unittest.TestCase):
	def test_runtime_transform_places_cell_origin_at_source_rect(self) -> None:
		frame = rgba((4, 4), (90, 160, 220, 255))
		placed = qa.place_frame_rgba(
			frame, (16, 12), [5, 3, 4, 4], [2, 2])
		self.assertEqual(placed.alpha_mask.getbbox(), (5, 3, 9, 7))

	def test_ownership_threshold_matches_delivery_mask(self) -> None:
		ownership = Image.new("L", (2, 1), 0)
		ownership.putpixel((0, 0), 48)
		ownership.putpixel((1, 0), 47)
		frame = placed_from_room_rgba(rgba((2, 1), (90, 160, 220, 255)))
		healing = qa.asset_healing_mask(ownership, [frame])
		self.assertEqual(np.asarray(healing, dtype=np.uint8).ravel().tolist(),
		                 [255, 0])

	def test_union_coverage_cannot_hide_per_frame_exposure(self) -> None:
		size = (8, 4)
		ownership = Image.new("L", size, 255)
		left = np.zeros((4, 8, 4), dtype=np.uint8)
		left[:, :4] = (80, 170, 220, 255)
		right = np.zeros((4, 8, 4), dtype=np.uint8)
		right[:, 4:] = (80, 170, 220, 255)
		frames = [
			placed_from_room_rgba(Image.fromarray(left, "RGBA")),
			placed_from_room_rgba(Image.fromarray(right, "RGBA")),
		]
		healing = qa.asset_healing_mask(ownership, frames)
		self.assertEqual(np.count_nonzero(np.asarray(healing)), 32)
		results = qa.compute_asset_frame_qa(
			rgba(size, (230, 180, 150, 255)),
			rgba(size, (30, 70, 110, 255)),
			ownership,
			frames,
			review_margin=0,
		)
		self.assertEqual([result.record.exposed_heal_pixels for result in results],
		                 [16, 16])
		self.assertIn("missing composite approval",
		              " ".join(qa.blocking_issues(results[0].record, None)))

	def test_one_pixel_alpha_hole_invalidates_exposure_signature(self) -> None:
		size = (5, 5)
		ownership = Image.new("L", size, 255)
		base_frame = rgba(size, (80, 170, 220, 255))
		baseline = qa.compute_asset_frame_qa(
			rgba(size, (220, 170, 150, 255)),
			rgba(size, (20, 50, 90, 255)),
			ownership,
			[placed_from_room_rgba(base_frame)],
			review_margin=0,
		)[0]
		approval = baseline.record.to_dict()

		damaged = np.asarray(base_frame, dtype=np.uint8).copy()
		damaged[2, 2, 3] = 0
		mutation = qa.compute_asset_frame_qa(
			rgba(size, (220, 170, 150, 255)),
			rgba(size, (20, 50, 90, 255)),
			ownership,
			[placed_from_room_rgba(Image.fromarray(damaged, "RGBA"))],
			healing_mask=ownership,
			review_margin=0,
		)[0]
		self.assertEqual(mutation.record.exposed_heal_pixels, 1)
		problems = qa.compare_record_to_approval(mutation.record, approval)
		self.assertTrue(any("exposed_heal_pixel_sha256" in value
		                    for value in problems))

	def test_rgb_damage_with_same_alpha_invalidates_composite_signature(self) -> None:
		size = (5, 5)
		ownership = Image.new("L", size, 255)
		clean = rgba(size, (80, 170, 220, 255))
		approved = rgba(size, (220, 170, 150, 255))
		underlay = rgba(size, (20, 50, 90, 255))
		baseline = qa.compute_asset_frame_qa(
			approved, underlay, ownership,
			[placed_from_room_rgba(clean)], review_margin=0)[0]
		damaged = np.asarray(clean, dtype=np.uint8).copy()
		damaged[2, 2, :3] = (145, 55, 210)
		mutation = qa.compute_asset_frame_qa(
			approved, underlay, ownership,
			[placed_from_room_rgba(Image.fromarray(damaged, "RGBA"))],
			review_margin=0)[0]
		self.assertEqual(
			baseline.record.primary_alpha_pixel_sha256,
			mutation.record.primary_alpha_pixel_sha256,
		)
		self.assertNotEqual(
			baseline.record.composite_pixel_sha256,
			mutation.record.composite_pixel_sha256,
		)
		self.assertIn(
			"frame 0: stale composite_pixel_sha256",
			qa.compare_record_to_approval(
				mutation.record, baseline.record.to_dict()),
		)

	def test_underlay_smear_invalidates_composite_signature(self) -> None:
		size = (6, 4)
		ownership = Image.new("L", size, 255)
		frame_values = np.zeros((4, 6, 4), dtype=np.uint8)
		frame_values[:, :3] = (80, 170, 220, 255)
		frame = placed_from_room_rgba(Image.fromarray(frame_values, "RGBA"))
		approved = rgba(size, (220, 170, 150, 255))
		clean_underlay = rgba(size, (20, 90, 130, 255))
		baseline = qa.compute_asset_frame_qa(
			approved, clean_underlay, ownership, [frame], review_margin=0)[0]
		smear = np.asarray(clean_underlay, dtype=np.uint8).copy()
		smear[:, 3:, :3] = (95, 45, 155)
		mutation = qa.compute_asset_frame_qa(
			approved, Image.fromarray(smear, "RGBA"), ownership, [frame],
			review_margin=0)[0]
		self.assertEqual(
			baseline.record.exposed_heal_pixel_sha256,
			mutation.record.exposed_heal_pixel_sha256,
		)
		self.assertNotEqual(
			baseline.record.composite_pixel_sha256,
			mutation.record.composite_pixel_sha256,
		)

	def test_exposed_source_duplicate_component_is_nonwaivable(self) -> None:
		size = (6, 4)
		ownership = Image.new("L", size, 255)
		approved = rgba(size, (220, 170, 150, 255))
		underlay_values = np.zeros((4, 6, 4), dtype=np.uint8)
		underlay_values[:, :3] = (20, 90, 130, 255)
		underlay_values[:, 3:] = (220, 170, 150, 255)
		frame_values = np.zeros((4, 6, 4), dtype=np.uint8)
		frame_values[:, :3] = (80, 170, 220, 255)
		result = qa.compute_asset_frame_qa(
			approved,
			Image.fromarray(underlay_values, "RGBA"),
			ownership,
			[placed_from_room_rgba(Image.fromarray(frame_values, "RGBA"))],
			review_margin=0,
		)[0]
		self.assertEqual(result.record.duplicate_exposed_pixels, 12)
		self.assertEqual(result.record.duplicate_components[0].pixels, 12)
		problems = qa.blocking_issues(
			result.record, result.record.to_dict())
		self.assertTrue(any("exposed source duplicate" in value
		                    for value in problems))

	def test_tolerance_only_background_match_is_diagnostic_not_blocking(
			self) -> None:
		size = (6, 4)
		ownership = Image.new("L", size, 255)
		approved = rgba(size, (220, 170, 150, 255))
		underlay_values = np.zeros((4, 6, 4), dtype=np.uint8)
		underlay_values[:, :3] = (20, 90, 130, 255)
		# The uncovered half is similar enough for the historical +/-4 match,
		# but every decoded pixel changed and therefore is not retained source.
		underlay_values[:, 3:] = (217, 168, 147, 255)
		frame_values = np.zeros((4, 6, 4), dtype=np.uint8)
		frame_values[:, :3] = (80, 170, 220, 255)
		result = qa.compute_asset_frame_qa(
			approved,
			Image.fromarray(underlay_values, "RGBA"),
			ownership,
			[placed_from_room_rgba(Image.fromarray(frame_values, "RGBA"))],
			review_margin=0,
		)[0]
		self.assertEqual(result.record.blocking_duplicate_match_tolerance, 0)
		self.assertEqual(result.record.tolerance_only_match_radius, 4)
		self.assertEqual(result.record.duplicate_exposed_pixels, 0)
		self.assertEqual(result.record.duplicate_components, ())
		self.assertEqual(result.record.tolerance_only_duplicate_pixels, 12)
		self.assertEqual(
			result.record.tolerance_only_components[0].pixels, 12)
		self.assertEqual(
			qa.blocking_issues(result.record, result.record.to_dict()), [])

	def test_exact_approved_reveal_is_allowed(self) -> None:
		size = (6, 4)
		ownership = Image.new("L", size, 255)
		frame_values = np.zeros((4, 6, 4), dtype=np.uint8)
		frame_values[:, :3] = (80, 170, 220, 255)
		result = qa.compute_asset_frame_qa(
			rgba(size, (220, 170, 150, 255)),
			rgba(size, (20, 90, 130, 255)),
			ownership,
			[placed_from_room_rgba(Image.fromarray(frame_values, "RGBA"))],
			healing_mask=ownership,
			review_margin=0,
		)[0]
		self.assertEqual(result.record.exposed_heal_pixels, 12)
		approval = json.loads(json.dumps(result.record.to_dict()))
		self.assertEqual(qa.blocking_issues(result.record, approval), [])

	def test_runtime_center_offset_shift_invalidates_approval(self) -> None:
		room_size = (10, 8)
		frame = rgba((4, 4), (80, 170, 220, 255))
		ownership_values = np.zeros((8, 10), dtype=bool)
		ownership_values[2:6, 2:6] = True
		ownership = mask_from_array(ownership_values)
		approved = rgba(room_size, (220, 170, 150, 255))
		underlay = rgba(room_size, (20, 90, 130, 255))
		baseline = qa.compute_asset_frame_qa(
			approved, underlay, ownership,
			[qa.place_frame_rgba(frame, room_size, [2, 2, 4, 4], [2, 2])],
			review_margin=1,
		)[0]
		shifted = qa.compute_asset_frame_qa(
			approved, underlay, ownership,
			[qa.place_frame_rgba(frame, room_size, [2, 2, 4, 4], [3, 2])],
			review_margin=1,
		)[0]
		problems = qa.compare_record_to_approval(
			shifted.record, baseline.record.to_dict())
		self.assertTrue(any("primary_alpha_pixel_sha256" in value
		                    for value in problems))

	def test_secondary_water_overlay_cannot_count_as_primary_coverage(self) -> None:
		size = (6, 4)
		ownership = Image.new("L", size, 255)
		frame_values = np.zeros((4, 6, 4), dtype=np.uint8)
		frame_values[:, :3] = (80, 170, 220, 255)
		frame = placed_from_room_rgba(Image.fromarray(frame_values, "RGBA"))
		water_values = np.zeros((4, 6, 4), dtype=np.uint8)
		water_values[:, 3:] = (90, 220, 250, 255)
		water = Image.fromarray(water_values, "RGBA")
		approved = rgba(size, (220, 170, 150, 255))
		underlay = rgba(size, (20, 90, 130, 255))
		without_water = qa.compute_asset_frame_qa(
			approved, underlay, ownership, [frame], healing_mask=ownership,
			review_margin=0)[0]
		with_water = qa.compute_asset_frame_qa(
			approved, underlay, ownership, [frame], healing_mask=ownership,
			review_margin=0,
			secondary_overlays_by_frame=[(water,)])[0]
		self.assertEqual(without_water.record.exposed_heal_pixels, 12)
		self.assertEqual(with_water.record.exposed_heal_pixels, 12)
		self.assertEqual(
			without_water.record.exposed_heal_pixel_sha256,
			with_water.record.exposed_heal_pixel_sha256,
		)
		self.assertNotEqual(
			without_water.record.composite_pixel_sha256,
			with_water.record.composite_pixel_sha256,
		)


if __name__ == "__main__":
	unittest.main()
