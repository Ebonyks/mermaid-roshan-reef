#!/usr/bin/env python3
"""Record dimensions, hashes, content drift, and seam evidence for the HD grid."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v2_3x1.png"
MASTER = ROOT / "assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png"
TILES = ROOT / "assets/flats/sky_lagoon/main"
REPORT = ROOT / "audit/sky_lagoon_hd_grid.json"
SEAMS = ROOT / "audit/sky_lagoon_hd_seam_capture.jpg"


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def mean_difference(left: Image.Image, right: Image.Image) -> float:
	stats = ImageStat.Stat(ImageChops.difference(left, right))
	return sum(stats.mean) / (len(stats.mean) * 255.0)


def main() -> None:
	old = Image.open(OLD).convert("RGB")
	master = Image.open(MASTER).convert("RGB")
	downsampled = master.resize(old.size, Image.Resampling.LANCZOS)
	content_delta = mean_difference(old, downsampled)

	seam_entries: list[dict[str, float | int | str | bool]] = []
	for x in range(1024, master.width, 1024):
		seam_jump = mean_difference(
			master.crop((x - 1, 0, x, master.height)),
			master.crop((x, 0, x + 1, master.height)),
		)
		near_jump = max(
			1e-9,
			(
				mean_difference(
					master.crop((x - 2, 0, x - 1, master.height)),
					master.crop((x - 1, 0, x, master.height)),
				)
				+ mean_difference(
					master.crop((x, 0, x + 1, master.height)),
					master.crop((x + 1, 0, x + 2, master.height)),
				)
			)
			* 0.5,
		)
		ratio = seam_jump / near_jump
		seam_entries.append(
			{"axis": "vertical", "pixel": x, "jump": seam_jump,
			 "near_jump": near_jump, "ratio": ratio, "pass": ratio <= 2.0}
		)
	for y in range(1024, master.height, 1024):
		seam_jump = mean_difference(
			master.crop((0, y - 1, master.width, y)),
			master.crop((0, y, master.width, y + 1)),
		)
		near_jump = max(
			1e-9,
			(
				mean_difference(
					master.crop((0, y - 2, master.width, y - 1)),
					master.crop((0, y - 1, master.width, y)),
				)
				+ mean_difference(
					master.crop((0, y, master.width, y + 1)),
					master.crop((0, y + 1, master.width, y + 2)),
				)
			)
			* 0.5,
		)
		ratio = seam_jump / near_jump
		seam_entries.append(
			{"axis": "horizontal", "pixel": y, "jump": seam_jump,
			 "near_jump": near_jump, "ratio": ratio, "pass": ratio <= 2.0}
		)

	tile_entries = []
	for row in range(2):
		for column in range(6):
			path = (
				TILES
				/ f"flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{column}.png"
			)
			with Image.open(path) as tile:
				size = tile.size
			tile_entries.append(
				{
					"row": row,
					"column": column,
					"rect": [column * 1024, row * 1024, 1024, 1024],
					"size": list(size),
					"sha256": sha256(path),
				}
			)

	vertical_strips = [
		master.crop((x - 48, 0, x + 48, master.height)).resize(
			(96, 320), Image.Resampling.LANCZOS
		)
		for x in range(1024, master.width, 1024)
	]
	horizontal = master.crop((0, 1024 - 48, master.width, 1024 + 48)).resize(
		(720, 96), Image.Resampling.LANCZOS
	)
	capture = Image.new("RGB", (720, 448), "white")
	for index, strip in enumerate(vertical_strips):
		capture.paste(strip, (index * 144 + 24, 16))
	capture.paste(horizontal, (0, 344))
	draw = ImageDraw.Draw(capture)
	draw.text((8, 424), "vertical joins (top) and horizontal join (bottom)", fill=(20, 40, 55))
	SEAMS.parent.mkdir(parents=True, exist_ok=True)
	capture.save(SEAMS, quality=94, subsampling=0)

	report = {
		"source": {
			"path": OLD.relative_to(ROOT).as_posix(),
			"size": list(old.size),
			"ratio": old.width / old.height,
			"sha256": sha256(OLD),
		},
		"master": {
			"path": MASTER.relative_to(ROOT).as_posix(),
			"size": list(master.size),
			"ratio": master.width / master.height,
			"ratio_delta": abs(master.width / master.height - old.width / old.height),
			"sha256": sha256(MASTER),
			"downsampled_mean_absolute_delta": content_delta,
		},
		"grid": {"columns": 6, "rows": 2, "tile_size": [1024, 1024]},
		"tiles": tile_entries,
		"seams": seam_entries,
		"all_seams_pass": all(bool(item["pass"]) for item in seam_entries),
		"seam_capture": SEAMS.relative_to(ROOT).as_posix(),
	}
	REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
	print(f"HD_GRID seams={'PASS' if report['all_seams_pass'] else 'FAIL'}")
	print(f"HD_GRID content_delta={content_delta:.4f}")
	print(REPORT)


if __name__ == "__main__":
	main()
