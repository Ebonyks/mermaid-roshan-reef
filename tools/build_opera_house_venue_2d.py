"""Build the true-2D Pearl Opera House venue from its accepted scene key.

The July 21 master is immutable review art.  This tool makes a lossless-path,
deterministic runtime derivative: one 3640x2048 reconstruction split into the
project's established 2x4 grid of <=1024px textures.  It never changes the
accepted source image and never invents or composites new scene content.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
	ROOT
	/ "assets_src"
	/ "concepts"
	/ "opera_house_flat"
	/ "opera_house_master_scene_key_2026-07-21.png"
)
OUTPUT_ROOT = ROOT / "assets" / "flats" / "castle" / "opera_house_venue_2d"
TILE_ROOT = OUTPUT_ROOT / "background_tiles"
FALLBACK = OUTPUT_ROOT / "room_opera_house_venue.png"
MANIFEST = OUTPUT_ROOT / "opera_house_venue_2d_manifest.json"

MASTER_SIZE = (3640, 2048)
TILE_SIZE = (910, 1024)
ROWS = 2
COLUMNS = 4


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def main() -> None:
	if not SOURCE.is_file():
		raise FileNotFoundError(SOURCE)
	OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
	TILE_ROOT.mkdir(parents=True, exist_ok=True)

	with Image.open(SOURCE) as source_image:
		source = source_image.convert("RGB")
		# Keep an exact-size fallback for atomic room transitions and headless
		# loading.  The tiled route below is the shipping background.
		source.save(FALLBACK, format="PNG", optimize=True)
		master = source.resize(MASTER_SIZE, Image.Resampling.LANCZOS)

	tile_records: list[dict[str, object]] = []
	for row in range(ROWS):
		for column in range(COLUMNS):
			left = column * TILE_SIZE[0]
			top = row * TILE_SIZE[1]
			tile = master.crop((
				left,
				top,
				left + TILE_SIZE[0],
				top + TILE_SIZE[1],
			))
			path = TILE_ROOT / (
				f"room_opera_house_venue_background_r{row}_c{column}.png"
			)
			tile.save(path, format="PNG", optimize=True)
			tile_records.append({
				"path": path.relative_to(ROOT).as_posix(),
				"row": row,
				"column": column,
				"size": list(TILE_SIZE),
				"source_rect": [left, top, TILE_SIZE[0], TILE_SIZE[1]],
				"sha256": _sha256(path),
			})

	payload = {
		"role": "runtime_true_2d_opera_house_venue",
		"historical_layout_commit": "90d19190",
		"accepted_source": SOURCE.relative_to(ROOT).as_posix(),
		"accepted_source_sha256": _sha256(SOURCE),
		"accepted_source_size": [1024, 576],
		"derivation": "whole-frame Lanczos normalization, then exact non-overlapping crops",
		"master_size": list(MASTER_SIZE),
		"grid": {"rows": ROWS, "columns": COLUMNS},
		"fallback": {
			"path": FALLBACK.relative_to(ROOT).as_posix(),
			"size": [1024, 576],
			"sha256": _sha256(FALLBACK),
		},
		"tiles": tile_records,
	}
	MANIFEST.write_text(
		json.dumps(payload, indent=2) + "\n",
		encoding="utf-8",
	)
	print(f"built {len(tile_records)} Opera House venue tiles")


if __name__ == "__main__":
	main()
