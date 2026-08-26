#!/usr/bin/env python3
"""Blocking contract for the shipped true-Canvas Sky Lagoon stage."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKDROP_ROOT = "assets/flats/sky_lagoon/main"
BACKDROP_COLUMNS = 6
BACKDROP_ROWS = 2
TILE_SIZE = (1024, 1024)
BACKDROP_TILES = tuple(
	BACKDROP_ROOT + f"/flat_sky_lagoon_main_panorama_v5_tile_r{row}_c{column}.png"
	for row in range(BACKDROP_ROWS)
	for column in range(BACKDROP_COLUMNS)
)
RUNTIME_CARDS = (
	"assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_tall_v1.png",
	"assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_slender_v1.png",
	"assets/sprites/sky_lagoon/sky_lagoon_cloud_single_v1.png",
	"assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png",
	"assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png",
	"assets/sprites/sky_lagoon/sky_lagoon_slide_v3_compact.png",
	"assets/sprites/sky_lagoon/sky_lagoon_seesaw_v5_fitted.png",
	"assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png",
	"assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png",
	"assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png",
	"assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png",
	"assets/sprites/sky_lagoon/animals/otter_idle_atlas.png",
	"assets/sprites/sky_lagoon/animals/otter_startle_atlas.png",
	"assets/sprites/sky_lagoon/animals/frog_idle_atlas.png",
	"assets/sprites/sky_lagoon/animals/frog_startle_atlas.png",
	"assets/sprites/sky_lagoon/animals/hare_idle_atlas.png",
	"assets/sprites/sky_lagoon/animals/hare_startle_atlas.png",
	"assets/sprites/sky_lagoon/animals/squirrel_idle_atlas.png",
	"assets/sprites/sky_lagoon/animals/squirrel_startle_atlas.png",
	"assets/sprites/sky_lagoon/animals/raccoon_idle_atlas.png",
	"assets/sprites/sky_lagoon/animals/raccoon_startle_atlas.png",
)
RUNTIME_SOURCE = "scripts/arena/sky_lagoon_promenade.gd"
SOURCE_REQUIREMENTS = (
	"const MASTER_SIZE := Vector2(6144.0, 2048.0)",
	"const BACKDROP_COLUMNS := 6",
	"const BACKDROP_ROWS := 2",
	"flat_sky_lagoon_main_panorama_v5_tile_r%d_c%d.png",
	"SkyLagoonBackdrop_r%d_c%d",
	"func _build_backdrop() -> void:",
	"func _build_castle_screen() -> void:",
	"Sprite2D.new()",
)
FORBIDDEN_SPATIAL_MARKERS = (".glb", "Node3D", "Sprite3D", "Camera3D", "Vector3")


def png_size(path: Path) -> tuple[int, int]:
	data = path.read_bytes()
	if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
		raise ValueError("not a valid PNG")
	width = int.from_bytes(data[16:20], "big")
	height = int.from_bytes(data[20:24], "big")
	if width <= 0 or height <= 0:
		raise ValueError(f"invalid dimensions {width}x{height}")
	return width, height


def audit_card(relative: str, expected_size: tuple[int, int] | None = None) -> tuple[int, int, str]:
	path = ROOT / relative
	width, height = png_size(path)
	digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
	if expected_size is not None and (width, height) != expected_size:
		raise ValueError(f"expected {expected_size[0]}x{expected_size[1]}, got {width}x{height}")
	return width, height, digest


def audit_source() -> None:
	path = ROOT / RUNTIME_SOURCE
	source = path.read_text(encoding="utf-8")
	for requirement in SOURCE_REQUIREMENTS:
		if requirement not in source:
			raise ValueError(f"missing Canvas runtime contract: {requirement}")
	for marker in FORBIDDEN_SPATIAL_MARKERS:
		if marker in source:
			raise ValueError(f"retired spatial runtime marker remains: {marker}")


def main() -> None:
	failures: list[str] = []
	digests: set[str] = set()
	for relative in BACKDROP_TILES:
		path = ROOT / relative
		try:
			width, height, digest = audit_card(relative, TILE_SIZE)
			digests.add(digest)
			print(f"SKYCANVAS|TILE|OK|{relative}|size={width}x{height}|sha={digest}")
		except (OSError, ValueError) as error:
			failures.append(f"{relative}: {error}")
			print(f"SKYCANVAS|TILE|FAIL|{relative}|{error}")
	for relative in RUNTIME_CARDS:
		try:
			width, height, _digest = audit_card(relative)
			print(f"SKYCANVAS|CARD|OK|{relative}|size={width}x{height}")
		except (OSError, ValueError) as error:
			failures.append(f"{relative}: {error}")
			print(f"SKYCANVAS|CARD|FAIL|{relative}|{error}")
	try:
		audit_source()
		print(f"SKYCANVAS|SOURCE|OK|{RUNTIME_SOURCE}|medium=Canvas2D")
	except (OSError, ValueError) as error:
		failures.append(f"{RUNTIME_SOURCE}: {error}")
		print(f"SKYCANVAS|SOURCE|FAIL|{RUNTIME_SOURCE}|{error}")
	if len(digests) < BACKDROP_COLUMNS:
		failures.append(f"backdrop grid has only {len(digests)} distinct tile hashes")
	if failures:
		raise SystemExit(1)
	print(f"SKYCANVAS|RESULT|OK|tiles={len(BACKDROP_TILES)}|cards={len(RUNTIME_CARDS)}|"
		f"distinct_tiles={len(digests)}")


if __name__ == "__main__":
	main()
