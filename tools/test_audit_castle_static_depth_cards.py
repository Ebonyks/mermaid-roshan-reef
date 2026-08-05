#!/usr/bin/env python3
"""Focused tests for the Castle static depth-card blocking audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image


TOOL = Path(__file__).with_name("audit_castle_static_depth_cards.py")
SPEC = importlib.util.spec_from_file_location("castle_static_depth_audit", TOOL)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def sha256(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


class StaticDepthCardAuditTests(unittest.TestCase):
	def setUp(self) -> None:
		self.temporary = tempfile.TemporaryDirectory()
		self.root = Path(self.temporary.name)
		(self.root / "scripts/arena").mkdir(parents=True)
		(self.root / "assets/flats/castle/rooms").mkdir(parents=True)
		(self.root / "assets_src/castle/depth_cards").mkdir(parents=True)
		self.card_path = (
			self.root / "assets/flats/castle/rooms/room_kitchen_front_left.png")
		self._write_card()
		self._write_layout()
		self._write_manifest()

	def tearDown(self) -> None:
		self.temporary.cleanup()

	def _write_card(
			self, hidden_rgb: bool = False, outside_shape: bool = False) -> None:
		pixels = np.zeros((6, 8, 4), dtype=np.uint8)
		pixels[1:5, 1:5] = (40, 100, 180, 255)
		if outside_shape:
			pixels[5, 7] = (90, 80, 70, 255)
		if hidden_rgb:
			pixels[0, 0, :3] = (7, 8, 9)
		Image.fromarray(pixels, mode="RGBA").save(self.card_path)

	def _write_layout(
			self, position: tuple[float, float] = (0.0, 354.0),
			pool_mid: bool = False, extra_reference: bool = False) -> None:
		mid = (
			'[{"tex": "room_mermaid_pool_mid_pool.png", '
			'"pos": Vector2(0.0, 218.0)}]'
			if pool_mid else "[]")
		trailer = (
			'\nconst BAD_RUNTIME_REFERENCE := "room_mermaid_pool_mid_pool.png"\n'
			if extra_reference else "")
		text = f'''extends RefCounted
const ROOM_LAYOUTS := {{
	"kitchen": {{
		"walk": Rect2(0, 0, 1, 1),
		"mid": [],
		"front": [
			{{"tex": "room_kitchen_front_left.png",
			 "pos": Vector2({position[0]}, {position[1]})}},
		],
	}},
	"mermaid_pool": {{
		"mid": {mid},
		"front": [],
	}},
}}
{trailer}'''
		(self.root / AUDIT.EXPECTED_LAYOUT).write_text(text, encoding="utf-8")

	def _card_record(self) -> dict[str, object]:
		data = self.card_path.read_bytes()
		pixels = np.asarray(Image.open(self.card_path).convert("RGBA"), dtype=np.uint8)
		alpha = pixels[:, :, 3]
		core = (alpha >= 128).astype(np.uint8) * 255
		metrics = {
			"alpha_pixels": int(np.count_nonzero(alpha)),
			"core_pixels": int(np.count_nonzero(core)),
			"hidden_rgb_pixels": int(np.count_nonzero(
				(alpha == 0) & np.any(pixels[:, :, :3] != 0, axis=2))),
		}
		return {
			"room": "kitchen",
			"id": "front_left",
			"role": "foreground",
			"path": "assets/flats/castle/rooms/room_kitchen_front_left.png",
			"position": [0.0, 354.0],
			"source_sha256": sha256(data),
			"output_sha256": sha256(data),
			"alpha_sha256": sha256(alpha.tobytes()),
			"core_mask_sha256": sha256(core.tobytes()),
			"before": dict(metrics),
			"after": dict(metrics),
			"keep_shapes": [{
				"type": "polygon",
				"points": [[1, 1], [4, 1], [4, 4], [1, 4]],
			}],
			"method": "test fixture alpha cleanup",
		}

	def _write_manifest(
			self, mutate: object | None = None,
			include_retired: bool = True) -> None:
		record = self._card_record()
		if callable(mutate):
			mutate(record)
		manifest = {
			"schema_version": 1,
			"alpha_scissor_threshold": 128,
			"runtime_layout_path": AUDIT.EXPECTED_LAYOUT,
			"cards": [record],
			"retired_cards": ([{
				"room": "mermaid_pool",
				"id": "mid_pool",
				"role": "midground",
				"path": AUDIT.POOL_MID_PATH,
				"reason": "retired to prevent a coplanar water sheet",
			}] if include_retired else []),
		}
		path = self.root / AUDIT.DEFAULT_MANIFEST
		path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

	def _audit(self) -> tuple[dict[str, object], list[str]]:
		return AUDIT.audit_repository(self.root)

	def test_clean_declared_card_passes_without_writes(self) -> None:
		before = {
			path.relative_to(self.root).as_posix(): path.read_bytes()
			for path in self.root.rglob("*") if path.is_file()
		}
		summary, errors = self._audit()
		after = {
			path.relative_to(self.root).as_posix(): path.read_bytes()
			for path in self.root.rglob("*") if path.is_file()
		}
		self.assertEqual([], errors)
		self.assertEqual(1, summary["verified_cards"])
		self.assertEqual(before, after)

	def test_rejects_rgb_hidden_under_zero_alpha(self) -> None:
		self._write_card(hidden_rgb=True)
		self._write_manifest()
		_, errors = self._audit()
		self.assertTrue(any("RGB pixels under alpha==0" in error for error in errors))

	def test_rejects_core_alpha_outside_approved_shapes(self) -> None:
		self._write_card(outside_shape=True)
		self._write_manifest()
		_, errors = self._audit()
		self.assertTrue(any("outside keep_shapes" in error for error in errors))

	def test_rejects_runtime_position_not_in_provenance(self) -> None:
		self._write_layout(position=(1.0, 354.0))
		_, errors = self._audit()
		self.assertTrue(any(
			"active runtime card lacks matching provenance" in error
			for error in errors))
		self.assertTrue(any(
			"provenance card is not active" in error for error in errors))

	def test_rejects_active_pool_mid_and_runtime_reference(self) -> None:
		self._write_layout(pool_mid=True)
		_, errors = self._audit()
		self.assertIn("ROOM_LAYOUTS.mermaid_pool.mid must be empty", errors)
		self.assertTrue(any(
			"remains referenced" in error for error in errors))

	def test_rejects_pool_mid_reference_outside_layout_entry(self) -> None:
		self._write_layout(extra_reference=True)
		_, errors = self._audit()
		self.assertTrue(any(
			"remains referenced" in error for error in errors))

	def test_does_not_treat_a_comment_as_a_runtime_reference(self) -> None:
		layout = self.root / AUDIT.EXPECTED_LAYOUT
		layout.write_text(
			layout.read_text(encoding="utf-8")
			+ "\n# retired room_mermaid_pool_mid_pool.png is intentionally absent\n",
			encoding="utf-8")
		_, errors = self._audit()
		self.assertFalse(any("remains referenced" in error for error in errors))

	def test_rejects_decoded_hash_drift(self) -> None:
		def mutate(record: dict[str, object]) -> None:
			record["alpha_sha256"] = "0" * 64
			record["core_mask_sha256"] = "1" * 64
		self._write_manifest(mutate)
		_, errors = self._audit()
		self.assertTrue(any("alpha_sha256 does not match" in error for error in errors))
		self.assertTrue(any("core_mask_sha256 does not match" in error for error in errors))

	def test_rejects_missing_retired_pool_record(self) -> None:
		self._write_manifest(include_retired=False)
		_, errors = self._audit()
		self.assertIn(
			"retired_cards must contain exactly one mermaid_pool:mid_pool record",
			errors)


if __name__ == "__main__":
	unittest.main()
