#!/usr/bin/env python3
"""Build Blender-importable GLB reliefs from Fairy Pond illustrated masters.

The Fairy Pond camera is overhead, so an upright billboard would disappear and
a stock vertical flower reads poorly.  Each generated illustration becomes a
shallow XZ-plane relief with a clipped illustrated face, a matching back, and
dark-indigo boundary walls.  The result is a real mesh item with stable scale,
phone-readable silhouette, and no runtime alpha-card rectangle.

The GLBs use only core glTF 2.0 and can be opened or further edited in Blender.
No third-party Python package is required.
"""

from __future__ import annotations

import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / "assets_src" / "fairy_v2" / "runtime_textures"
OUTPUT = ROOT / "assets" / "fairy" / "models"
INK = [0.035, 0.052, 0.102, 1.0]


@dataclass(frozen=True)
class BuildSpec:
	texture: str
	output: str
	grid: int
	thickness: float
	role: str


SPECS = [
	BuildSpec("bug_jewel.png", "bug_jewel.glb", 48, 0.10, "shadow_bug_jewel"),
	BuildSpec("bug_moth.png", "bug_moth.glb", 48, 0.08, "shadow_bug_moth"),
	BuildSpec("bug_firefly.png", "bug_firefly.glb", 48, 0.10, "shadow_bug_firefly"),
	BuildSpec("boss_leaf.png", "boss_leaf.glb", 48, 0.08, "fairy_flower_leaf_shield"),
	BuildSpec("boss_seed.png", "boss_seed.glb", 72, 0.12, "fairy_flower_seed"),
	BuildSpec("boss_sprout.png", "boss_sprout.glb", 72, 0.10, "fairy_flower_sprout"),
	BuildSpec("boss_bud.png", "boss_bud.glb", 72, 0.12, "fairy_flower_bud"),
	BuildSpec("boss_opening.png", "boss_opening.glb", 72, 0.10, "fairy_flower_opening"),
	BuildSpec("boss_bloom.png", "boss_bloom.glb", 72, 0.10, "fairy_flower_bloom"),
]


def _pack_floats(values: list[tuple[float, ...]]) -> bytes:
	flat = [component for value in values for component in value]
	return struct.pack("<" + "f" * len(flat), *flat)


def _pack_uints(values: list[int]) -> bytes:
	return struct.pack("<" + "I" * len(values), *values)


class GlbBuilder:
	def __init__(self) -> None:
		self.binary = bytearray()
		self.buffer_views: list[dict] = []
		self.accessors: list[dict] = []

	def add_view(self, data: bytes, target: int | None = None) -> int:
		while len(self.binary) % 4:
			self.binary.append(0)
		offset = len(self.binary)
		self.binary.extend(data)
		view: dict = {"buffer": 0, "byteOffset": offset, "byteLength": len(data)}
		if target is not None:
			view["target"] = target
		self.buffer_views.append(view)
		return len(self.buffer_views) - 1

	def add_accessor(
		self,
		view: int,
		component_type: int,
		count: int,
		kind: str,
		minimum: list[float] | None = None,
		maximum: list[float] | None = None,
	) -> int:
		accessor: dict = {
			"bufferView": view,
			"byteOffset": 0,
			"componentType": component_type,
			"count": count,
			"type": kind,
		}
		if minimum is not None:
			accessor["min"] = minimum
		if maximum is not None:
			accessor["max"] = maximum
		self.accessors.append(accessor)
		return len(self.accessors) - 1


def _position_bounds(values: list[tuple[float, float, float]]) -> tuple[list[float], list[float]]:
	return (
		[min(value[axis] for value in values) for axis in range(3)],
		[max(value[axis] for value in values) for axis in range(3)],
	)


def _build_geometry(image: Image.Image, grid: int, thickness: float) -> dict[str, list]:
	alpha = image.getchannel("A")
	width, height = image.size
	keep: set[tuple[int, int]] = set()
	for row in range(grid):
		for column in range(grid):
			x = min(width - 1, int((column + 0.5) / grid * width))
			y = min(height - 1, int((row + 0.5) / grid * height))
			if alpha.getpixel((x, y)) > 12:
				keep.add((column, row))

	front_pos: list[tuple[float, float, float]] = []
	front_nrm: list[tuple[float, float, float]] = []
	front_uv: list[tuple[float, float]] = []
	front_idx: list[int] = []
	front_vertices: dict[tuple[int, int], int] = {}
	back_vertices: dict[tuple[int, int], int] = {}

	def vertex(column: int, row: int, front: bool) -> int:
		cache = front_vertices if front else back_vertices
		key = (column, row)
		if key in cache:
			return cache[key]
		u = column / grid
		v = row / grid
		x = u - 0.5
		z = 0.5 - v
		index = len(front_pos)
		front_pos.append((x, thickness * 0.5 if front else -thickness * 0.5, z))
		front_nrm.append((0.0, 1.0 if front else -1.0, 0.0))
		front_uv.append((u, v))
		cache[key] = index
		return index

	for column, row in sorted(keep, key=lambda item: (item[1], item[0])):
		a = vertex(column, row, True)
		b = vertex(column + 1, row, True)
		c = vertex(column + 1, row + 1, True)
		d = vertex(column, row + 1, True)
		front_idx.extend((a, b, c, a, c, d))
		ab = vertex(column, row, False)
		bb = vertex(column + 1, row, False)
		cb = vertex(column + 1, row + 1, False)
		db = vertex(column, row + 1, False)
		front_idx.extend((ab, cb, bb, ab, db, cb))

	side_pos: list[tuple[float, float, float]] = []
	side_nrm: list[tuple[float, float, float]] = []
	side_idx: list[int] = []

	def side_quad(points: tuple[tuple[float, float], tuple[float, float]], normal: tuple[float, float, float]) -> None:
		start = len(side_pos)
		for plane_y, point in (
			(thickness * 0.5, points[0]),
			(thickness * 0.5, points[1]),
			(-thickness * 0.5, points[1]),
			(-thickness * 0.5, points[0]),
		):
			side_pos.append((point[0], plane_y, point[1]))
			side_nrm.append(normal)
		side_idx.extend((start, start + 1, start + 2, start, start + 2, start + 3))

	for column, row in keep:
		x0 = column / grid - 0.5
		x1 = (column + 1) / grid - 0.5
		z0 = 0.5 - row / grid
		z1 = 0.5 - (row + 1) / grid
		if (column, row - 1) not in keep:
			side_quad(((x0, z0), (x1, z0)), (0.0, 0.0, 1.0))
		if (column + 1, row) not in keep:
			side_quad(((x1, z0), (x1, z1)), (1.0, 0.0, 0.0))
		if (column, row + 1) not in keep:
			side_quad(((x1, z1), (x0, z1)), (0.0, 0.0, -1.0))
		if (column - 1, row) not in keep:
			side_quad(((x0, z1), (x0, z0)), (-1.0, 0.0, 0.0))

	return {
		"front_pos": front_pos,
		"front_nrm": front_nrm,
		"front_uv": front_uv,
		"front_idx": front_idx,
		"side_pos": side_pos,
		"side_nrm": side_nrm,
		"side_idx": side_idx,
		"cells": [len(keep)],
	}


def build(spec: BuildSpec) -> None:
	texture_path = TEXTURES / spec.texture
	output_path = OUTPUT / spec.output
	image = Image.open(texture_path).convert("RGBA")
	geometry = _build_geometry(image, spec.grid, spec.thickness)
	builder = GlbBuilder()

	front_pos = geometry["front_pos"]
	front_min, front_max = _position_bounds(front_pos)
	front_pos_view = builder.add_view(_pack_floats(front_pos), 34962)
	front_nrm_view = builder.add_view(_pack_floats(geometry["front_nrm"]), 34962)
	front_uv_view = builder.add_view(_pack_floats(geometry["front_uv"]), 34962)
	front_idx_view = builder.add_view(_pack_uints(geometry["front_idx"]), 34963)
	front_pos_acc = builder.add_accessor(front_pos_view, 5126, len(front_pos), "VEC3", front_min, front_max)
	front_nrm_acc = builder.add_accessor(front_nrm_view, 5126, len(front_pos), "VEC3")
	front_uv_acc = builder.add_accessor(front_uv_view, 5126, len(front_pos), "VEC2")
	front_idx_acc = builder.add_accessor(front_idx_view, 5125, len(geometry["front_idx"]), "SCALAR")

	side_pos = geometry["side_pos"]
	side_min, side_max = _position_bounds(side_pos)
	side_pos_view = builder.add_view(_pack_floats(side_pos), 34962)
	side_nrm_view = builder.add_view(_pack_floats(geometry["side_nrm"]), 34962)
	side_idx_view = builder.add_view(_pack_uints(geometry["side_idx"]), 34963)
	side_pos_acc = builder.add_accessor(side_pos_view, 5126, len(side_pos), "VEC3", side_min, side_max)
	side_nrm_acc = builder.add_accessor(side_nrm_view, 5126, len(side_pos), "VEC3")
	side_idx_acc = builder.add_accessor(side_idx_view, 5125, len(geometry["side_idx"]), "SCALAR")

	texture_view = builder.add_view(texture_path.read_bytes())
	name = Path(spec.output).stem
	document = {
		"asset": {"version": "2.0", "generator": "Mermaid Roshan Fairy Relief Builder"},
		"extensionsUsed": ["KHR_materials_unlit"],
		"scene": 0,
		"scenes": [{"name": name, "nodes": [0]}],
		"nodes": [{"name": name, "mesh": 0, "extras": {"role": spec.role, "camera_contract": "overhead"}}],
		"meshes": [{
			"name": name + "_relief",
			"primitives": [
				{
					"attributes": {"POSITION": front_pos_acc, "NORMAL": front_nrm_acc, "TEXCOORD_0": front_uv_acc},
					"indices": front_idx_acc,
					"material": 0,
				},
				{
					"attributes": {"POSITION": side_pos_acc, "NORMAL": side_nrm_acc},
					"indices": side_idx_acc,
					"material": 1,
				},
			],
		}],
		"materials": [
			{
				"name": name + "_illustration",
				"pbrMetallicRoughness": {
					"baseColorTexture": {"index": 0},
					"metallicFactor": 0.0,
					"roughnessFactor": 0.92,
				},
				"alphaMode": "MASK",
				"alphaCutoff": 0.05,
				"doubleSided": False,
				"extensions": {"KHR_materials_unlit": {}},
			},
			{
				"name": name + "_ink_edge",
				"pbrMetallicRoughness": {"baseColorFactor": INK, "metallicFactor": 0.0, "roughnessFactor": 0.96},
				"doubleSided": True,
				"extensions": {"KHR_materials_unlit": {}},
			},
		],
		"textures": [{"source": 0, "sampler": 0}],
		"samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
		"images": [{"name": spec.texture, "bufferView": texture_view, "mimeType": "image/png"}],
		"buffers": [{"byteLength": len(builder.binary)}],
		"bufferViews": builder.buffer_views,
		"accessors": builder.accessors,
	}

	json_data = json.dumps(document, separators=(",", ":")).encode("utf-8")
	json_data += b" " * ((4 - len(json_data) % 4) % 4)
	while len(builder.binary) % 4:
		builder.binary.append(0)
	bin_data = bytes(builder.binary)
	total_length = 12 + 8 + len(json_data) + 8 + len(bin_data)
	glb = bytearray(struct.pack("<4sII", b"glTF", 2, total_length))
	glb.extend(struct.pack("<I4s", len(json_data), b"JSON"))
	glb.extend(json_data)
	glb.extend(struct.pack("<I4s", len(bin_data), b"BIN\x00"))
	glb.extend(bin_data)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_bytes(glb)
	triangles = (len(geometry["front_idx"]) + len(geometry["side_idx"])) // 3
	print(f"wrote {output_path.relative_to(ROOT)}: cells={geometry['cells'][0]} triangles={triangles}")


def main() -> None:
	for spec in SPECS:
		build(spec)


if __name__ == "__main__":
	main()
