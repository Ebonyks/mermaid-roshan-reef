#!/usr/bin/env python3
"""Fail-closed tests for MA-VIS-007 background/card pixel ownership."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from tools import build_interactive_background_ownership as ownership


class InteractiveBackgroundOwnershipTests(unittest.TestCase):
	def test_every_promoted_source_is_complete_and_opaque(self) -> None:
		manifest = json.loads(ownership.AUDIT.read_text(encoding="utf-8"))
		records = manifest["castle"] + manifest["opera"]
		self.assertEqual(len(records), 9)
		for record in records:
			path = ownership.ROOT / record["source"]
			with Image.open(path) as image:
				self.assertEqual(
					image.convert("RGBA").getchannel("A").getextrema(),
					(255, 255), record["source"])
			self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
				record["source_sha256"])

	def test_active_generators_do_not_call_legacy_local_clean_plate(self) -> None:
		v4 = (ownership.ROOT / "tools/build_castle_native_interactions_v4.py") \
			.read_text(encoding="utf-8")
		layers = (ownership.ROOT / "tools/build_castle_room_layers.py") \
			.read_text(encoding="utf-8")
		self.assertNotIn("= _clean_plate(", v4)
		self.assertNotIn("= _clean_plate(", layers)

	def test_runtime_tiles_are_exact_master_crops(self) -> None:
		planned, fable, v4, audit = ownership.build_expected()
		ownership.bind_hashes(planned, fable, v4, audit)
		self.assertEqual(ownership.check_outputs(planned, audit), [])

	def test_manifest_hashes_bind_committed_png_bytes(self) -> None:
		image = Image.new("RGB", (97, 61), (12, 34, 56))
		with tempfile.TemporaryDirectory(dir=ownership.ROOT / "audit") as directory:
			path = Path(directory) / "compressed_differently.png"
			image.save(path, "PNG", compress_level=1)
			committed = hashlib.sha256(path.read_bytes()).hexdigest()
			reencoded = hashlib.sha256(ownership.png_bytes(image)).hexdigest()
			self.assertNotEqual(committed, reencoded)
			hashes = ownership.committed_output_hashes({path: image})
			self.assertEqual(hashes[ownership.relative(path)], committed)

	def test_partial_tent_override_is_retired_for_complete_v2_object(self) -> None:
		v4 = json.loads((ownership.ROOT /
			"assets/flats/castle/interactions_v4/castle_interactions_v4.json")
			.read_text(encoding="utf-8"))
		self.assertNotIn("playroom_tent_flaps_right",
			{asset["id"] for asset in v4["assets"]})
		v2 = json.loads((ownership.ROOT /
			"assets/flats/castle/interactions_v2/castle_interactions_v2.json")
			.read_text(encoding="utf-8"))
		full_tent = next(asset for asset in v2["assets"]
			if asset["id"] == "playroom_play_tent")
		self.assertEqual(full_tent["instances"], ["play_tent"])
		self.assertEqual(full_tent["render_mode"],
			"generated_full_object_states")
		self.assertEqual(full_tent["authored_frame_count"], 8)

	def test_craft_cupboard_rest_frame_is_complete_closed_state(self) -> None:
		v4 = json.loads((ownership.ROOT /
			"assets/flats/castle/interactions_v4/castle_interactions_v4.json")
			.read_text(encoding="utf-8"))
		asset = next(asset for asset in v4["assets"]
			if asset["id"] == "craft_room_supply_cupboard_left")
		columns, rows = asset["grid"]
		with Image.open(ownership.ROOT / asset["sheet"]) as sheet:
			cell_width = sheet.width // columns
			cell_height = sheet.height // rows
			frame_zero = sheet.crop((0, 0, cell_width, cell_height))
			frame_seven = sheet.crop((3 * cell_width, cell_height,
				4 * cell_width, 2 * cell_height))
			self.assertEqual(frame_zero.tobytes(), frame_seven.tobytes())


if __name__ == "__main__":
	unittest.main()
