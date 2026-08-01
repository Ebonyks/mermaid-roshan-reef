#!/usr/bin/env python3
"""Build Kitchen v3 by replacing only the defective two-spout kettle."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from skimage.restoration import inpaint


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
	ROOT / "assets_src" / "castle" / "room_regenerations"
	/ "room_kitchen_fullframe_v2_1672x941.png")
KETTLE = (
	ROOT / "assets_src" / "castle" / "room_regenerations"
	/ "room_kitchen_kettle_single_spout.png")
OUTPUT = (
	ROOT / "assets_src" / "castle" / "room_regenerations"
	/ "room_kitchen_fullframe_v3_1672x941.png")

# Native 1672x941 source coordinates. The old kettle is removed as one object
# before compositing, so neither its second spout nor its old handle can peek
# around the replacement silhouette.
INPAINT_CROP = (622, 336, 770, 462)
KETTLE_TARGET_BOX = (642, 353, 752, 448)


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def main() -> None:
	frame = Image.open(SOURCE).convert("RGB")
	if frame.size != (1672, 941):
		raise ValueError(f"{SOURCE} is {frame.size}, expected (1672, 941)")

	left, top, right, bottom = INPAINT_CROP
	patch = np.asarray(
		frame.crop(INPAINT_CROP), dtype=np.float32) / 255.0
	mask_image = Image.new("L", frame.size, 0)
	draw = ImageDraw.Draw(mask_image)
	draw.ellipse((638, 378, 748, 457), fill=255)
	draw.ellipse((648, 343, 730, 414), fill=255)
	draw.polygon((
		(631, 369), (651, 356), (675, 368), (678, 399),
		(652, 411), (633, 397),
	), fill=255)
	draw.polygon((
		(728, 378), (745, 372), (762, 379), (758, 397),
		(741, 411), (727, 403),
	), fill=255)
	mask = np.asarray(
		mask_image.crop(INPAINT_CROP), dtype=np.uint8) > 0
	repaired = inpaint.inpaint_biharmonic(
		patch, mask, channel_axis=-1)
	frame.paste(
		Image.fromarray(
			np.clip(repaired * 255.0, 0, 255).astype(np.uint8), mode="RGB"),
		(left, top))

	kettle = Image.open(KETTLE).convert("RGBA")
	alpha = np.asarray(kettle, dtype=np.uint8)[:, :, 3]
	y_values, x_values = np.nonzero(alpha)
	if x_values.size == 0:
		raise RuntimeError("single-spout kettle has an empty alpha channel")
	kettle = kettle.crop((
		int(x_values.min()), int(y_values.min()),
		int(x_values.max()) + 1, int(y_values.max()) + 1))
	target_width = KETTLE_TARGET_BOX[2] - KETTLE_TARGET_BOX[0]
	target_height = KETTLE_TARGET_BOX[3] - KETTLE_TARGET_BOX[1]
	kettle = kettle.resize(
		(target_width, target_height), Image.Resampling.LANCZOS)
	frame = frame.convert("RGBA")
	frame.alpha_composite(
		kettle, (KETTLE_TARGET_BOX[0], KETTLE_TARGET_BOX[1]))
	frame.convert("RGB").save(OUTPUT, optimize=True)
	print(
		f"OK: {OUTPUT.relative_to(ROOT).as_posix()} "
		f"sha256={sha256(OUTPUT)}")


if __name__ == "__main__":
	main()
