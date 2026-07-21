#!/usr/bin/env python3
"""Structural gate for the generated Sky Lagoon core-glTF kit."""

from __future__ import annotations

import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
	"assets/sky_lagoon/lagoon_kit/lagoon_baby_rosette.glb": "grounded_baby_plant",
	"assets/sky_lagoon/lagoon_kit/lagoon_flower_cluster_coral.glb": "grounded_flowering_cluster",
	"assets/sky_lagoon/lagoon_kit/lagoon_flower_cluster_lavender.glb": "grounded_flowering_cluster",
	"assets/sky_lagoon/lagoon_kit/lagoon_mushroom_cluster.glb": "grounded_mushroom_family",
	"assets/sky_lagoon/lagoon_kit/lagoon_pond_reeds.glb": "rooted_reed_bed",
	"assets/sky_lagoon/lagoon_kit/lagoon_river_stones.glb": "riverbank_stone_cluster",
	"assets/sky_lagoon/lagoon_kit/lagoon_story_lantern.glb": "storybook_path_lantern",
	"assets/sky_lagoon/lagoon_kit/lagoon_memory_frame.glb": "protected_memory_display_surround",
	"assets/sky_lagoon/lagoon_kit/lagoon_rainbow_race_arch.glb": "rainbow_race_gateway",
	"assets/sky_lagoon/lagoon_kit/lagoon_butterfly_world_gate.glb": "four_wing_swim_through_gateway",
	"assets/sky_lagoon/lagoon_kit/lagoon_train_station.glb": "courtyard_train_station",
	"assets/sky_lagoon/lagoon_kit/lagoon_snowbank.glb": "alpine_snow_edge_cluster",
	"assets/art35/landmarks/cloud_0.glb": "soft_toon_cloud_family",
	"assets/art35/landmarks/cloud_1.glb": "soft_toon_cloud_family",
	"assets/art35/landmarks/cloud_2.glb": "soft_toon_cloud_family",
}
WOODY_EXPECTED = {
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_douglas_fir.glb": "lagoon_tree_douglas_fir",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_western_redcedar.glb": "lagoon_tree_western_redcedar",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_western_hemlock.glb": "lagoon_tree_western_hemlock",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_sitka_spruce.glb": "lagoon_tree_sitka_spruce",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_shore_pine.glb": "lagoon_tree_shore_pine",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_pacific_yew.glb": "lagoon_tree_pacific_yew",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_bigleaf_maple.glb": "lagoon_tree_bigleaf_maple",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_red_alder.glb": "lagoon_tree_red_alder",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_black_cottonwood.glb": "lagoon_tree_black_cottonwood",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_pacific_madrone.glb": "lagoon_tree_pacific_madrone",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_garry_oak.glb": "lagoon_tree_garry_oak",
	"assets/sky_lagoon/lagoon_kit/lagoon_tree_pacific_dogwood.glb": "lagoon_tree_pacific_dogwood",
	"assets/sky_lagoon/lagoon_kit/lagoon_shrub_salal.glb": "lagoon_shrub_salal",
	"assets/sky_lagoon/lagoon_kit/lagoon_shrub_oregon_grape.glb": "lagoon_shrub_oregon_grape",
	"assets/sky_lagoon/lagoon_kit/lagoon_shrub_red_flowering_currant.glb": "lagoon_shrub_red_flowering_currant",
	"assets/sky_lagoon/lagoon_kit/lagoon_shrub_oceanspray.glb": "lagoon_shrub_oceanspray",
	"assets/sky_lagoon/lagoon_kit/lagoon_shrub_salmonberry.glb": "lagoon_shrub_salmonberry",
	"assets/sky_lagoon/lagoon_kit/lagoon_shrub_evergreen_huckleberry.glb": "lagoon_shrub_evergreen_huckleberry",
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


def audit_woody(path: Path, expected_role: str) -> tuple[int, int, str, float]:
	document = glb_json(path)
	nodes = document.get("nodes", [])
	if len(nodes) != 1:
		raise ValueError(f"expected one authored woody-plant root, got {len(nodes)}")
	extras = nodes[0].get("extras", {})
	if extras.get("role") != expected_role:
		raise ValueError(f"role {extras.get('role')!r} != {expected_role!r}")
	if extras.get("style_gate") != "sky_lagoon_pnw_woody_gen1":
		raise ValueError("missing PNW woody-plant style-gate metadata")
	for metadata_key in ("species_common", "species_latin", "habitat"):
		if not extras.get(metadata_key):
			raise ValueError(f"missing {metadata_key} metadata")
	triangles = 0
	minimum_y = 1.0e9
	maximum_y = -1.0e9
	for mesh in document.get("meshes", []):
		for primitive in mesh.get("primitives", []):
			accessor_index = primitive["indices"]
			triangles += int(document["accessors"][accessor_index]["count"]) // 3
			position_accessor = document["accessors"][primitive["attributes"]["POSITION"]]
			minimum_y = min(minimum_y, float(position_accessor["min"][1]))
			maximum_y = max(maximum_y, float(position_accessor["max"][1]))
	materials = len(document.get("materials", []))
	maximum_triangles = 7500 if expected_role.startswith("lagoon_tree_") else 6500
	if triangles < 1500 or triangles > maximum_triangles:
		raise ValueError(f"woody-plant triangle count outside Mobile budget: {triangles}")
	if materials <= 0 or materials > 8:
		raise ValueError(f"woody-plant material count outside Mobile budget: {materials}")
	images = document.get("images", [])
	textures = document.get("textures", [])
	if len(images) > 1 or len(textures) > 1:
		raise ValueError(f"woody-plant texture count outside budget: {len(images)} images/{len(textures)} textures")
	image_gate = "none"
	if images:
		image = images[0]
		if image.get("mimeType") != "image/png" or "bufferView" not in image:
			raise ValueError("tree texture must be one embedded PNG")
		data = path.read_bytes()
		json_length = struct.unpack_from("<I", data, 12)[0]
		bin_header = 20 + json_length
		bin_length, bin_type = struct.unpack_from("<I4s", data, bin_header)
		if bin_type != b"BIN\x00":
			raise ValueError("tree GLB is missing its binary chunk")
		binary = data[bin_header + 8:bin_header + 8 + bin_length]
		view = document["bufferViews"][int(image["bufferView"])]
		offset = int(view.get("byteOffset", 0))
		blob = binary[offset:offset + int(view["byteLength"])]
		if blob[:8] != b"\x89PNG\r\n\x1a\n" or len(blob) < 24:
			raise ValueError("tree texture is not a valid PNG")
		width, height = struct.unpack_from(">II", blob, 16)
		if max(width, height) > 1024:
			raise ValueError(f"tree texture exceeds 1024px: {width}x{height}")
		image_gate = f"{width}x{height}"
	return triangles, materials, image_gate, maximum_y - minimum_y


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
	for relative, role in WOODY_EXPECTED.items():
		path = ROOT / relative
		try:
			triangles, materials, image_gate, height = audit_woody(path, role)
			print(f"SKYWOODY|OK|{relative}|tris={triangles}|materials={materials}|"
				f"texture={image_gate}|height={height:.3f}|role={role}")
		except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, struct.error) as error:
			failures.append(f"{relative}: {error}")
			print(f"SKYWOODY|FAIL|{relative}|{error}")
	if failures:
		raise SystemExit(1)
	print(f"SKYKIT|RESULT|OK|assets={len(EXPECTED)}|woody={len(WOODY_EXPECTED)}")


if __name__ == "__main__":
	main()
