#!/usr/bin/env python3
"""Bake coherent craft-creature paint zones into a UV mask.

The RGB channels are body, accent, and detail. Black texels keep the baked
albedo (eyes, beak, feet, and other fixed features).

Baby Eagle must be classified from the character itself, not from broad
world-space boxes. The rig already tells us which vertices belong to each
wing, and its embedded albedo carries the authored pink feather boundaries.
Those signals produce whole anatomical cutouts; geometry is used only for
the deliberate belly patch and fixed beak/feet.

Usage:
  python tools/bake_zone_mask.py <rigged.glb> <kitty|birdie> <out_mask.png>
      [--preview-dir <directory>]
"""

from __future__ import annotations

import argparse
import json
import struct
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image


SIZE = 1024
PREVIEW_SIZE = 512
CHANNEL_NAMES = ("body", "accent", "detail")
COMPONENT_DTYPES = {
	5121: np.uint8,
	5123: np.uint16,
	5125: np.uint32,
	5126: np.float32,
}
COMPONENT_COUNTS = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


@dataclass
class MeshData:
	gltf: dict
	buffer: bytes
	positions: np.ndarray
	uvs: np.ndarray
	triangles: np.ndarray
	joint_names: list[str]
	joints: np.ndarray | None
	weights: np.ndarray | None
	albedo: np.ndarray | None


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("glb", type=Path)
	parser.add_argument("kind", choices=("kitty", "birdie"))
	parser.add_argument("output", type=Path)
	parser.add_argument("--preview-dir", type=Path)
	return parser.parse_args()


def _accessor(gltf: dict, buffer: bytes, index: int) -> np.ndarray:
	accessor = gltf["accessors"][index]
	view = gltf["bufferViews"][accessor["bufferView"]]
	offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
	dtype = COMPONENT_DTYPES[accessor["componentType"]]
	components = COMPONENT_COUNTS[accessor["type"]]
	array = np.frombuffer(
		buffer,
		dtype=dtype,
		count=accessor["count"] * components,
		offset=offset,
	)
	return array.reshape(accessor["count"], components)


def _embedded_albedo(gltf: dict, buffer: bytes, primitive: dict) -> np.ndarray | None:
	material_index = primitive.get("material")
	if material_index is None:
		return None
	material = gltf.get("materials", [])[material_index]
	texture_info = material.get("pbrMetallicRoughness", {}).get("baseColorTexture")
	if texture_info is None:
		return None
	texture = gltf.get("textures", [])[texture_info["index"]]
	image_info = gltf.get("images", [])[texture["source"]]
	view_index = image_info.get("bufferView")
	if view_index is None:
		return None
	view = gltf["bufferViews"][view_index]
	offset = view.get("byteOffset", 0)
	payload = buffer[offset:offset + view["byteLength"]]
	with Image.open(BytesIO(payload)) as source:
		image = source.convert("RGB")
		if image.size != (SIZE, SIZE):
			image = image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
		return np.asarray(image, dtype=np.float64) / 255.0


def load_mesh(path: Path) -> MeshData:
	data = path.read_bytes()
	if data[:4] != b"glTF":
		raise ValueError(f"not a binary glTF: {path}")
	json_length = struct.unpack("<I", data[12:16])[0]
	gltf = json.loads(data[20:20 + json_length])
	buffer_offset = 20 + json_length + 8
	buffer = data[buffer_offset:]
	mesh = gltf["meshes"][0]
	if len(mesh["primitives"]) != 1:
		raise ValueError("paint-mask baker requires one mesh primitive")
	primitive = mesh["primitives"][0]
	attributes = primitive["attributes"]
	positions = _accessor(gltf, buffer, attributes["POSITION"]).astype(np.float64)
	uvs = _accessor(gltf, buffer, attributes["TEXCOORD_0"]).astype(np.float64)
	triangles = _accessor(gltf, buffer, primitive["indices"]).astype(np.int64).reshape(-1, 3)

	joints = None
	weights = None
	joint_names: list[str] = []
	if "JOINTS_0" in attributes and "WEIGHTS_0" in attributes:
		joints = _accessor(gltf, buffer, attributes["JOINTS_0"]).astype(np.int64)
		weights = _accessor(gltf, buffer, attributes["WEIGHTS_0"]).astype(np.float64)
		skin_index = next(
			(node["skin"] for node in gltf.get("nodes", []) if "skin" in node),
			None,
		)
		if skin_index is not None:
			skin = gltf["skins"][skin_index]
			joint_names = [gltf["nodes"][node_index].get("name", "") for node_index in skin["joints"]]

	return MeshData(
		gltf=gltf,
		buffer=buffer,
		positions=positions,
		uvs=uvs,
		triangles=triangles,
		joint_names=joint_names,
		joints=joints,
		weights=weights,
		albedo=_embedded_albedo(gltf, buffer, primitive),
	)


def normalize_positions(positions: np.ndarray) -> np.ndarray:
	"""Return x/y/z in character-height units with y in the 0..1 range."""
	y_min = positions[:, 1].min()
	height = positions[:, 1].max() - y_min
	if height <= 0.0:
		raise ValueError("mesh has zero height")
	normalized = positions.copy()
	normalized[:, 1] = (positions[:, 1] - y_min) / height
	normalized[:, 0] = positions[:, 0] / height
	normalized[:, 2] = positions[:, 2] / height
	return normalized


def joint_weight(mesh: MeshData, wanted: set[str]) -> np.ndarray:
	"""Sum each vertex's skin weights for the requested named joints."""
	result = np.zeros(len(mesh.positions), dtype=np.float64)
	if mesh.joints is None or mesh.weights is None or not mesh.joint_names:
		return result
	for slot in range(mesh.joints.shape[1]):
		indices = mesh.joints[:, slot]
		matches = np.fromiter(
			(mesh.joint_names[index] in wanted for index in indices),
			dtype=bool,
			count=len(indices),
		)
		result += mesh.weights[:, slot] * matches
	return result


def rasterize_attributes(
	uvs: np.ndarray,
	triangles: np.ndarray,
	vertex_attributes: np.ndarray,
	canvas_size: int = SIZE,
) -> tuple[np.ndarray, np.ndarray]:
	"""Interpolate vertex attributes into UV space and return values + coverage."""
	uv_pixels = uvs.copy()
	uv_pixels[:, 0] = np.clip(uv_pixels[:, 0] % 1.0, 0.0, 1.0) * (canvas_size - 1)
	uv_pixels[:, 1] = np.clip(uv_pixels[:, 1] % 1.0, 0.0, 1.0) * (canvas_size - 1)
	attributes = np.asarray(vertex_attributes, dtype=np.float64)
	if attributes.ndim == 1:
		attributes = attributes[:, None]
	result = np.zeros((canvas_size, canvas_size, attributes.shape[1]), dtype=np.float64)
	count = np.zeros((canvas_size, canvas_size, 1), dtype=np.float64)

	for triangle in triangles:
		a, b, c = uv_pixels[triangle[0]], uv_pixels[triangle[1]], uv_pixels[triangle[2]]
		x0 = int(max(0, np.floor(min(a[0], b[0], c[0]))))
		x1 = int(min(canvas_size - 1, np.ceil(max(a[0], b[0], c[0]))))
		y0 = int(max(0, np.floor(min(a[1], b[1], c[1]))))
		y1 = int(min(canvas_size - 1, np.ceil(max(a[1], b[1], c[1]))))
		if x1 <= x0 or y1 <= y0 or (x1 - x0) * (y1 - y0) > 40000:
			continue
		xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
		determinant = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
		if abs(determinant) < 1e-9:
			continue
		lambda0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / determinant
		lambda1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / determinant
		lambda2 = 1.0 - lambda0 - lambda1
		inside = (lambda0 >= -0.02) & (lambda1 >= -0.02) & (lambda2 >= -0.02)
		if not inside.any():
			continue
		values = (
			lambda0[..., None] * attributes[triangle[0]]
			+ lambda1[..., None] * attributes[triangle[1]]
			+ lambda2[..., None] * attributes[triangle[2]]
		)
		yy, xx = np.nonzero(inside)
		result[ys[yy, xx], xs[yy, xx]] += values[yy, xx]
		count[ys[yy, xx], xs[yy, xx]] += 1.0

	filled = count[..., 0] > 0.0
	result[filled] /= count[filled]
	return result, filled


def authored_color_regions(albedo: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
	"""Find the embedded pink and yellow paint without reacting to JPEG noise."""
	red, green, blue = albedo[..., 0], albedo[..., 1], albedo[..., 2]
	maximum = albedo.max(axis=2)
	minimum = albedo.min(axis=2)
	chroma = maximum - minimum
	saturation = chroma / np.maximum(maximum, 1e-6)
	# Pink paint has red and blue energy while yellow paint has red and green.
	# Channel relations are more stable than hue around low-saturation feather
	# edges and deliberately ignore gray shading in the neutralized base map.
	pink = (
		(saturation >= 0.14)
		& (red >= green + 0.055)
		& (blue >= green + 0.015)
	)
	yellow = (
		(saturation >= 0.14)
		& (red >= blue + 0.07)
		& (green >= blue + 0.035)
		& ~pink
	)
	return pink, yellow


def classify_kitty(points: np.ndarray, filled: np.ndarray) -> np.ndarray:
	x, y, z = points[..., 0], points[..., 1], points[..., 2]
	muzzle = (z > 0.17) & (y > 0.30) & (y < 0.62) & (np.abs(x) < 0.14)
	chest = (z > 0.05) & (y <= 0.36) & (y > -0.02) & (np.abs(x) < 0.19)
	ears = (y > 0.72) & (np.abs(x) > 0.10) & (z < 0.30)
	tail = z < -0.42
	detail = (muzzle | chest) & filled
	accent = (ears | tail) & ~detail & filled
	horn = (y > 0.74) & (np.abs(x) < 0.14) & (z > 0.0) & (z < 0.55)
	paintable = filled & ~horn
	body = paintable & ~accent & ~detail
	return np.stack((body, accent, detail), axis=2)


def classify_birdie(
	points: np.ndarray,
	wing_weights: np.ndarray,
	foot_weights: np.ndarray,
	filled: np.ndarray,
	albedo: np.ndarray,
) -> np.ndarray:
	"""Build one-hot Baby Eagle zones from anatomical and authored signals."""
	x, y, z = points[..., 0], points[..., 1], points[..., 2]
	pink, _yellow = authored_color_regions(albedo)

	# The wing bones provide a closed anatomical region. Authored pink expands
	# the cutout only along that region's feather edge; it can never create the
	# old stray patches on the tail, legs, or torso.
	wing_candidate = wing_weights >= 0.46
	wing_edge = (wing_weights >= 0.20) & pink
	crest = (y >= 0.925) & (np.abs(x) <= 0.13) & (z > -0.08)
	accent = (wing_candidate | wing_edge | crest) & filled

	# A single centered breast shield reads as one deliberate feather panel.
	# The former axis-aligned box cut shoulders and side feathers at random.
	belly_ellipse = (
		((x / 0.155) ** 2 + ((y - 0.405) / 0.185) ** 2 <= 1.0)
		& (z >= 0.075)
	)
	detail = belly_ellipse & ~accent & filled

	# Rig ownership keeps both articulated legs and feet fixed. The corrected
	# beak threshold is inside the actual z extent (the old z > 0.30 condition
	# could never match this mesh, whose normalized maximum is about 0.276).
	fixed_feet = (foot_weights >= 0.56) | (y < 0.115)
	fixed_beak = (z >= 0.185) & (y >= 0.61) & (np.abs(x) <= 0.155)
	paintable = filled & ~fixed_feet & ~fixed_beak
	accent &= paintable
	detail &= paintable
	body = paintable & ~accent & ~detail
	return np.stack((body, accent, detail), axis=2)


def grow_gutters(labels: np.ndarray, filled: np.ndarray, iterations: int = 2) -> np.ndarray:
	"""Copy one-hot labels into UV gutters without blending neighboring zones."""
	result = labels.copy()
	known = filled.copy()
	for _ in range(iterations):
		updated = result.copy()
		new_known = known.copy()
		for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
			neighbor_known = np.roll(known, (dy, dx), axis=(0, 1))
			target = ~new_known & neighbor_known
			updated[target] = np.roll(result, (dy, dx), axis=(0, 1))[target]
			new_known[target] = True
		result = updated
		known = new_known
	return result


def build_mask(mesh: MeshData, kind: str) -> tuple[np.ndarray, np.ndarray]:
	normalized = normalize_positions(mesh.positions)
	wing = joint_weight(mesh, {"wingL", "wingL2", "wingR", "wingR2"})
	feet = joint_weight(mesh, {"legL", "footL", "legR", "footR"})
	vertex_attributes = np.column_stack((normalized, wing, feet))
	uv_attributes, filled = rasterize_attributes(mesh.uvs, mesh.triangles, vertex_attributes)
	if kind == "kitty":
		labels = classify_kitty(uv_attributes[..., :3], filled)
	else:
		if mesh.albedo is None:
			raise ValueError("birdie mask requires the rig's embedded base-color texture")
		if not mesh.joint_names:
			raise ValueError("birdie mask requires named rig joints")
		labels = classify_birdie(
			uv_attributes[..., :3],
			uv_attributes[..., 3],
			uv_attributes[..., 4],
			filled,
			mesh.albedo,
		)
	labels = grow_gutters(labels, filled)
	return labels, filled


def save_preview(mask: np.ndarray, path: Path) -> None:
	"""Save a readable UV proof using Baby Eagle's canonical palette roles."""
	colors = np.array(
		[
			[67, 188, 205],
			[242, 82, 151],
			[255, 214, 72],
		],
		dtype=np.uint8,
	)
	rgb = np.asarray(mask, dtype=np.uint8) @ colors
	alpha = (mask.any(axis=2).astype(np.uint8) * 255)[..., None]
	preview = np.concatenate((rgb, alpha), axis=2)
	path.parent.mkdir(parents=True, exist_ok=True)
	Image.fromarray(preview, "RGBA").resize(
		(PREVIEW_SIZE, PREVIEW_SIZE),
		Image.Resampling.NEAREST,
	).save(path)


def render_zone_view(mesh: MeshData, mask: np.ndarray, view: str, path: Path) -> None:
	"""Render an orthographic zone proof without requiring Blender or Godot."""
	positions = normalize_positions(mesh.positions)
	if view == "front":
		horizontal, vertical, depth = positions[:, 0], positions[:, 1], positions[:, 2]
	elif view == "side":
		horizontal, vertical, depth = -positions[:, 2], positions[:, 1], positions[:, 0]
	elif view == "back":
		horizontal, vertical, depth = -positions[:, 0], positions[:, 1], -positions[:, 2]
	else:
		raise ValueError(f"unknown preview view: {view}")

	margin = 36.0
	scale = PREVIEW_SIZE - margin * 2.0
	projected = np.column_stack(
		(
			PREVIEW_SIZE * 0.5 + horizontal * scale,
			margin + (1.0 - vertical) * scale,
		)
	)
	uv_pixels = mesh.uvs.copy()
	uv_pixels[:, 0] = np.clip(uv_pixels[:, 0] % 1.0, 0.0, 1.0) * (SIZE - 1)
	uv_pixels[:, 1] = np.clip(uv_pixels[:, 1] % 1.0, 0.0, 1.0) * (SIZE - 1)
	zone_colors = np.array(
		[[67, 188, 205], [242, 82, 151], [255, 214, 72]],
		dtype=np.uint8,
	)
	canvas = np.zeros((PREVIEW_SIZE, PREVIEW_SIZE, 4), dtype=np.uint8)
	z_buffer = np.full((PREVIEW_SIZE, PREVIEW_SIZE), -np.inf)

	for triangle in mesh.triangles:
		a, b, c = projected[triangle[0]], projected[triangle[1]], projected[triangle[2]]
		x0 = int(max(0, np.floor(min(a[0], b[0], c[0]))))
		x1 = int(min(PREVIEW_SIZE - 1, np.ceil(max(a[0], b[0], c[0]))))
		y0 = int(max(0, np.floor(min(a[1], b[1], c[1]))))
		y1 = int(min(PREVIEW_SIZE - 1, np.ceil(max(a[1], b[1], c[1]))))
		if x1 < x0 or y1 < y0:
			continue
		determinant = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
		if abs(determinant) < 1e-9:
			continue
		xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
		lambda0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / determinant
		lambda1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / determinant
		lambda2 = 1.0 - lambda0 - lambda1
		inside = (lambda0 >= -0.001) & (lambda1 >= -0.001) & (lambda2 >= -0.001)
		if not inside.any():
			continue
		triangle_depth = (
			lambda0 * depth[triangle[0]]
			+ lambda1 * depth[triangle[1]]
			+ lambda2 * depth[triangle[2]]
		)
		uv = (
			lambda0[..., None] * uv_pixels[triangle[0]]
			+ lambda1[..., None] * uv_pixels[triangle[1]]
			+ lambda2[..., None] * uv_pixels[triangle[2]]
		)
		uv_x = np.clip(np.rint(uv[..., 0]).astype(int), 0, SIZE - 1)
		uv_y = np.clip(np.rint(uv[..., 1]).astype(int), 0, SIZE - 1)
		zones = mask[uv_y, uv_x]
		yy, xx = np.nonzero(inside)
		py, px = ys[yy, xx], xs[yy, xx]
		nearer = triangle_depth[yy, xx] > z_buffer[py, px]
		if not nearer.any():
			continue
		py, px = py[nearer], px[nearer]
		zone_values = zones[yy, xx][nearer]
		active = zone_values.any(axis=1)
		canvas[py, px, :3] = zone_values.astype(np.uint8) @ zone_colors
		canvas[py, px, 3] = active.astype(np.uint8) * 255
		z_buffer[py, px] = triangle_depth[yy, xx][nearer]

	path.parent.mkdir(parents=True, exist_ok=True)
	Image.fromarray(canvas, "RGBA").save(path)


def validate_mask(labels: np.ndarray, kind: str) -> None:
	active_count = labels.sum(axis=2)
	if np.any(active_count > 1):
		raise ValueError(f"{kind}: overlapping paint zones are not allowed")
	for index, name in enumerate(CHANNEL_NAMES):
		pixels = int(labels[..., index].sum())
		if pixels == 0:
			raise ValueError(f"{kind}: empty {name} zone")


def main() -> int:
	args = parse_args()
	mesh = load_mesh(args.glb)
	normalized = normalize_positions(mesh.positions)
	print(
		"verts %d tris %d bbox x[%.3f %.3f] y[%.3f %.3f] z[%.3f %.3f]"
		% (
			len(mesh.positions),
			len(mesh.triangles),
			normalized[:, 0].min(),
			normalized[:, 0].max(),
			normalized[:, 1].min(),
			normalized[:, 1].max(),
			normalized[:, 2].min(),
			normalized[:, 2].max(),
		)
	)
	labels, filled = build_mask(mesh, args.kind)
	validate_mask(labels, args.kind)
	mask = labels.astype(np.uint8) * 255
	args.output.parent.mkdir(parents=True, exist_ok=True)
	Image.fromarray(mask, "RGB").save(args.output)
	coverage = float(filled.mean()) * 100.0
	zone_pixels = labels.sum(axis=(0, 1)).astype(int)
	print(f"MASK {args.kind}: {coverage:.1f}% UV coverage -> {args.output}")
	print(
		"zone pixels "
		+ " ".join(f"{name}={zone_pixels[index]}" for index, name in enumerate(CHANNEL_NAMES))
	)
	if args.preview_dir is not None:
		preview_path = args.preview_dir / f"{args.kind}_zones_uv.png"
		save_preview(labels, preview_path)
		print(f"PREVIEW {preview_path}")
		for view in ("front", "side", "back"):
			view_path = args.preview_dir / f"{args.kind}_zones_{view}.png"
			render_zone_view(mesh, labels, view, view_path)
			print(f"PREVIEW {view_path}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
