#!/usr/bin/env python3
"""Reject Castle depth cards that hide actors behind painted background pixels."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ROOM_ROOT = ROOT / "assets" / "flats" / "castle" / "rooms"
MANIFEST = ROOT / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"
CONTACT = ROOT / "audit" / "castle_sprite3d" / "castle_card_alpha_contact.png"
THUMBNAIL_SIZE = (250, 170)
CELL_SIZE = (280, 210)


def checkerboard(size: tuple[int, int]) -> Image.Image:
	width, height = size
	y_grid, x_grid = np.indices((height, width))
	cells = ((x_grid // 12 + y_grid // 12) % 2)[:, :, None]
	rgba = np.empty((height, width, 4), dtype=np.uint8)
	rgba[:, :, :3] = np.where(cells == 0, 205, 245)
	rgba[:, :, 3] = 255
	return Image.fromarray(rgba, mode="RGBA")


def main() -> None:
	manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
	records: list[dict[str, object]] = []
	failures: list[str] = []
	for room_id, room in manifest["rooms"].items():
		source_path = ROOM_ROOT / f"room_{room_id}.png"
		background_path = ROOM_ROOT / f"room_{room_id}_background.png"
		if not source_path.exists() or not background_path.exists():
			continue
		source = np.asarray(
			Image.open(source_path).convert("RGB"), dtype=np.int16)
		background = np.asarray(
			Image.open(background_path).convert("RGB"), dtype=np.int16)
		for card in room.get("cards", []):
			card_id = str(card["id"])
			card_path = ROOM_ROOT / f"room_{room_id}_{card_id}.png"
			image = Image.open(card_path).convert("RGBA")
			alpha = np.asarray(image, dtype=np.uint8)[:, :, 3]
			left, top, right, bottom = (
				int(value) for value in card["crop"])
			difference = np.max(np.abs(
				source[top:bottom, left:right]
				- background[top:bottom, left:right]), axis=2)
			depth_opaque = alpha >= 128
			invisible_depth = depth_opaque & (difference <= 6)
			opaque_pixels = int(np.count_nonzero(depth_opaque))
			invisible_pixels = int(np.count_nonzero(invisible_depth))
			invisible_ratio = (
				invisible_pixels / opaque_pixels if opaque_pixels else 1.0)
			coverage = opaque_pixels / alpha.size
			if opaque_pixels == 0:
				# Fully claimed overlap cards are harmless: they write no depth.
				continue
			if not bool(card.get("alpha_outline_refined", False)):
				failures.append(
					f"{room_id}:{card_id} lacks outline refinement evidence")
			if invisible_ratio > 0.35:
				failures.append(
					f"{room_id}:{card_id} invisible-depth ratio "
					f"{invisible_ratio:.4f} > 0.3500")
			if coverage >= 0.995:
				failures.append(
					f"{room_id}:{card_id} remains a rectangular depth card")
			preview = Image.alpha_composite(
				checkerboard(image.size), image)
			preview.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
			records.append({
				"name": f"{room_id}:{card_id}",
				"preview": preview,
				"coverage": coverage,
				"invisible_ratio": invisible_ratio,
			})

	columns = 4
	rows = math.ceil(len(records) / columns)
	contact = Image.new(
		"RGB", (columns * CELL_SIZE[0], rows * CELL_SIZE[1]), "white")
	draw = ImageDraw.Draw(contact)
	for index, record in enumerate(records):
		x = (index % columns) * CELL_SIZE[0]
		y = (index // columns) * CELL_SIZE[1]
		draw.text((x + 6, y + 5), str(record["name"]), fill="black")
		draw.text(
			(x + 6, y + 23),
			"opaque %.3f  invisible %.4f" % (
				float(record["coverage"]),
				float(record["invisible_ratio"])),
			fill="black")
		contact.paste(record["preview"], (x + 6, y + 40))
	CONTACT.parent.mkdir(parents=True, exist_ok=True)
	contact.save(CONTACT, optimize=True)

	print(json.dumps({
		"cards": len(records),
		"invisible_depth_failures": len(failures),
		"contact": CONTACT.relative_to(ROOT).as_posix(),
	}, indent=2))
	if failures:
		for failure in failures:
			print("FAIL:", failure)
		raise SystemExit(1)


if __name__ == "__main__":
	main()
