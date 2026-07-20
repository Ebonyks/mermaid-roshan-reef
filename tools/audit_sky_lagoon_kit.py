#!/usr/bin/env python3
"""Structural gate for the generated Sky Lagoon core-glTF kit."""

from __future__ import annotations

import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
	"assets/sky_lagoon/lagoon_kit/lagoon_baby_rosette.glb": "grounded_baby_plant",
	"assets/sky_lagoon/lagoon_kit/lagoon_meadow_shrub.glb": "developed_meadow_shrub",
	"assets/sky_lagoon/lagoon_kit/lagoon_flower_cluster_coral.glb": "grounded_flowering_cluster",
	"assets/sky_lagoon/lagoon_kit/lagoon_flower_cluster_lavender.glb": "grounded_flowering_cluster",
	"assets/sky_lagoon/lagoon_kit/lagoon_mushroom_cluster.glb": "grounded_mushroom_family",
	"assets/sky_lagoon/lagoon_kit/lagoon_pond_reeds.glb": "rooted_reed_bed",
	"assets/sky_lagoon/lagoon_kit/lagoon_river_stones.glb": "riverbank_stone_cluster",
	"assets/sky_lagoon/lagoon_kit/lagoon_story_lantern.glb": "storybook_path_lantern",
	"assets/sky_lagoon/lagoon_kit/lagoon_memory_frame.glb": "protected_memory_display_surround",
	"assets/sky_lagoon/lagoon_kit/lagoon_rainbow_race_arch.glb": "rainbow_race_gateway",
	"assets/sky_lagoon/lagoon_kit/lagoon_train_station.glb": "courtyard_train_station",
	"assets/sky_lagoon/lagoon_kit/lagoon_snowbank.glb": "alpine_snow_edge_cluster",
	"assets/art35/landmarks/cloud_0.glb": "soft_toon_cloud_family",
	"assets/art35/landmarks/cloud_1.glb": "soft_toon_cloud_family",
	"assets/art35/landmarks/cloud_2.glb": "soft_toon_cloud_family",
}


def glb_json(path: Path) -> dict:
	data = path.read_bytes()
	magic, version, total_length = struct.unpack_from("<4sII", data, 0)
	if magic != b"glTF" or version != 2 or total_length != len(data):
		raise ValueError("invalid glTF 2.0 header")
	json_length, json_type = struct.unpack_from("<I4s", data, 12)
	if json_type != b"JSON":
		raise ValueError("missing JSON chunk")
	return json.loads(data[20:20 + json_length].decode("utf-8"))


def audit(path: Path, expected_role: str) -> tuple[int, int]:
	document = glb_json(path)
	if document.get("images") or document.get("textures"):
		raise ValueError("unexpected texture memory")
	nodes = document.get("nodes", [])
	if len(nodes) != 1:
		raise ValueError(f"expected one authored root, got {len(nodes)}")
	extras = nodes[0].get("extras", {})
	if extras.get("role") != expected_role:
		raise ValueError(f"role {extras.get('role')!r} != {expected_role!r}")
	if extras.get("style_gate") != "no_single_ground_leaf":
		raise ValueError("missing style-gate metadata")
	triangles = 0
	for mesh in document.get("meshes", []):
		for primitive in mesh.get("primitives", []):
			accessor_index = primitive["indices"]
			triangles += int(document["accessors"][accessor_index]["count"]) // 3
	materials = len(document.get("materials", []))
	if triangles <= 0 or triangles > 3000:
		raise ValueError(f"triangle count outside Mobile budget: {triangles}")
	if materials <= 0 or materials > 12:
		raise ValueError(f"material count outside kit budget: {materials}")
	return triangles, materials


def main() -> None:
	failures: list[str] = []
	for relative, role in EXPECTED.items():
		path = ROOT / relative
		try:
			triangles, materials = audit(path, role)
			print(f"SKYKIT|OK|{relative}|tris={triangles}|materials={materials}|role={role}")
		except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
			failures.append(f"{relative}: {error}")
			print(f"SKYKIT|FAIL|{relative}|{error}")
	if failures:
		raise SystemExit(1)
	print(f"SKYKIT|RESULT|OK|assets={len(EXPECTED)}")


if __name__ == "__main__":
	main()
