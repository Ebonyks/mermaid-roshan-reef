#!/usr/bin/env python3
"""Build the authored Sky Lagoon art kit as core glTF 2.0 GLBs.

The builder intentionally uses no 3D package dependency. Every output can be
opened in Blender, but can also be regenerated in CI or a clean checkout with
ordinary Python. The geometry is faceted, matte, and sized for the Mobile
renderer. Optional Pillow QA renders provide a deterministic three-quarter
silhouette check without pretending to be the final Godot acceptance render.
"""

from __future__ import annotations

import json
import math
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
KIT_OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit"
CLOUD_OUT = ROOT / "assets" / "art35" / "landmarks"
QA_OUT = ROOT / "assets_src" / "sky_lagoon" / "qa_kit"


Vec3 = tuple[float, float, float]
Color = tuple[float, float, float, float]


PALETTE: dict[str, Color] = {
	"ink": (0.10, 0.08, 0.22, 1.0),
	# Lagoon lighting is intentionally high-key. These source values are one
	# band deeper than the final desired pastels so Mobile does not bleach every
	# plant, gate, and shell into the terrain.
	"leaf": (0.12, 0.43, 0.23, 1.0),
	"leaf_light": (0.27, 0.64, 0.34, 1.0),
	"mint": (0.27, 0.65, 0.49, 1.0),
	"aqua": (0.16, 0.55, 0.61, 1.0),
	"aqua_light": (0.43, 0.74, 0.72, 1.0),
	"lavender": (0.50, 0.38, 0.75, 1.0),
	"lavender_shadow": (0.32, 0.28, 0.58, 1.0),
	"coral": (0.81, 0.29, 0.38, 1.0),
	"coral_light": (0.91, 0.48, 0.48, 1.0),
	"gold": (0.82, 0.55, 0.12, 1.0),
	"butter": (0.88, 0.68, 0.18, 1.0),
	"pearl": (0.84, 0.80, 0.69, 1.0),
	"cloud": (0.98, 1.0, 1.0, 1.0),
	"cloud_warm": (1.0, 0.985, 0.955, 1.0),
	"cloud_shadow": (0.77, 0.84, 0.94, 1.0),
	"wood": (0.49, 0.31, 0.23, 1.0),
	"wood_light": (0.70, 0.48, 0.32, 1.0),
	"stone": (0.41, 0.51, 0.59, 1.0),
	"stone_light": (0.58, 0.69, 0.70, 1.0),
	"snow": (0.82, 0.91, 0.95, 1.0),
	"soil": (0.40, 0.29, 0.28, 1.0),
	"red": (0.72, 0.16, 0.25, 1.0),
	"orange": (0.85, 0.36, 0.12, 1.0),
	"yellow": (0.88, 0.64, 0.12, 1.0),
	"green": (0.18, 0.57, 0.28, 1.0),
	"blue": (0.20, 0.42, 0.75, 1.0),
	"violet": (0.45, 0.28, 0.68, 1.0),
}


def add(a: Vec3, b: Vec3) -> Vec3:
	return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec3, b: Vec3) -> Vec3:
	return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def mul(a: Vec3, value: float) -> Vec3:
	return (a[0] * value, a[1] * value, a[2] * value)


def dot(a: Vec3, b: Vec3) -> float:
	return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec3, b: Vec3) -> Vec3:
	return (
		a[1] * b[2] - a[2] * b[1],
		a[2] * b[0] - a[0] * b[2],
		a[0] * b[1] - a[1] * b[0],
	)


def length(a: Vec3) -> float:
	return math.sqrt(dot(a, a))


def norm(a: Vec3) -> Vec3:
	value = length(a)
	return mul(a, 1.0 / value) if value > 1.0e-8 else (0.0, 1.0, 0.0)


def lerp(a: Vec3, b: Vec3, t: float) -> Vec3:
	return add(a, mul(sub(b, a), t))


@dataclass
class Surface:
	material: str
	positions: list[Vec3] = field(default_factory=list)
	normals: list[Vec3] = field(default_factory=list)
	indices: list[int] = field(default_factory=list)

	def tri(self, a: Vec3, b: Vec3, c: Vec3, normal: Vec3 | None = None) -> None:
		n = norm(cross(sub(b, a), sub(c, a))) if normal is None else norm(normal)
		base = len(self.positions)
		self.positions.extend((a, b, c))
		self.normals.extend((n, n, n))
		self.indices.extend((base, base + 1, base + 2))

	def quad(self, a: Vec3, b: Vec3, c: Vec3, d: Vec3, normal: Vec3 | None = None) -> None:
		self.tri(a, b, c, normal)
		self.tri(a, c, d, normal)

	def smooth_tri(self, points: tuple[Vec3, Vec3, Vec3], normals: tuple[Vec3, Vec3, Vec3]) -> None:
		base = len(self.positions)
		self.positions.extend(points)
		self.normals.extend(norm(value) for value in normals)
		self.indices.extend((base, base + 1, base + 2))


@dataclass
class Asset:
	name: str
	role: str
	surfaces: dict[str, Surface] = field(default_factory=dict)

	def surface(self, material: str) -> Surface:
		if material not in self.surfaces:
			self.surfaces[material] = Surface(material)
		return self.surfaces[material]

	def triangle_count(self) -> int:
		return sum(len(surface.indices) // 3 for surface in self.surfaces.values())


def box(asset: Asset, center: Vec3, size: Vec3, material: str) -> None:
	x, y, z = (size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)
	pts = [
		add(center, (-x, -y, -z)), add(center, (x, -y, -z)),
		add(center, (x, y, -z)), add(center, (-x, y, -z)),
		add(center, (-x, -y, z)), add(center, (x, -y, z)),
		add(center, (x, y, z)), add(center, (-x, y, z)),
	]
	s = asset.surface(material)
	for a, b, c, d, n in (
		(4, 5, 6, 7, (0, 0, 1)), (1, 0, 3, 2, (0, 0, -1)),
		(0, 4, 7, 3, (-1, 0, 0)), (5, 1, 2, 6, (1, 0, 0)),
		(3, 7, 6, 2, (0, 1, 0)), (0, 1, 5, 4, (0, -1, 0)),
	):
		s.quad(pts[a], pts[b], pts[c], pts[d], n)


def cylinder(
	asset: Asset,
	p0: Vec3,
	p1: Vec3,
	r0: float,
	r1: float,
	material: str,
	segments: int = 8,
) -> None:
	direction = norm(sub(p1, p0))
	reference = (0.0, 1.0, 0.0) if abs(direction[1]) < 0.88 else (1.0, 0.0, 0.0)
	u = norm(cross(direction, reference))
	v = norm(cross(direction, u))
	s = asset.surface(material)
	for index in range(segments):
		a0 = index / segments * math.tau
		a1 = (index + 1) / segments * math.tau
		r0a = add(mul(u, math.cos(a0) * r0), mul(v, math.sin(a0) * r0))
		r0b = add(mul(u, math.cos(a1) * r0), mul(v, math.sin(a1) * r0))
		r1a = add(mul(u, math.cos(a0) * r1), mul(v, math.sin(a0) * r1))
		r1b = add(mul(u, math.cos(a1) * r1), mul(v, math.sin(a1) * r1))
		s.quad(add(p0, r0a), add(p0, r0b), add(p1, r1b), add(p1, r1a))
		s.tri(p0, add(p0, r0b), add(p0, r0a), mul(direction, -1.0))
		s.tri(p1, add(p1, r1a), add(p1, r1b), direction)


def ellipsoid(
	asset: Asset,
	center: Vec3,
	axis_x: Vec3,
	axis_y: Vec3,
	axis_z: Vec3,
	material: str,
	segments: int = 10,
	rings: int = 6,
	smooth: bool = True,
) -> None:
	s = asset.surface(material)
	axis_lengths = (max(length(axis_x), 1.0e-5), max(length(axis_y), 1.0e-5), max(length(axis_z), 1.0e-5))
	def point_normal(latitude: float, longitude: float) -> tuple[Vec3, Vec3]:
		cl = math.cos(latitude)
		local = (cl * math.cos(longitude), math.sin(latitude), cl * math.sin(longitude))
		point = add(center, add(mul(axis_x, local[0]), add(mul(axis_y, local[1]), mul(axis_z, local[2]))))
		normal = norm(add(mul(axis_x, local[0] / (axis_lengths[0] * axis_lengths[0])), add(
			mul(axis_y, local[1] / (axis_lengths[1] * axis_lengths[1])),
			mul(axis_z, local[2] / (axis_lengths[2] * axis_lengths[2])))))
		return point, normal
	for ring in range(rings):
		lat0 = -math.pi * 0.5 + math.pi * ring / rings
		lat1 = -math.pi * 0.5 + math.pi * (ring + 1) / rings
		for segment in range(segments):
			lon0 = math.tau * segment / segments
			lon1 = math.tau * (segment + 1) / segments
			a, na = point_normal(lat0, lon0)
			b, nb = point_normal(lat0, lon1)
			c, nc = point_normal(lat1, lon1)
			d, nd = point_normal(lat1, lon0)
			if ring > 0:
				if smooth:
					s.smooth_tri((a, c, b), (na, nc, nb))
				else:
					s.tri(a, c, b)
			if ring < rings - 1:
				if smooth:
					s.smooth_tri((a, d, c), (na, nd, nc))
				else:
					s.tri(a, d, c)


def sphere(asset: Asset, center: Vec3, scale: Vec3, material: str, segments: int = 10,
	rings: int = 6, smooth: bool = True) -> None:
	ellipsoid(asset, center, (scale[0], 0, 0), (0, scale[1], 0), (0, 0, scale[2]), material, segments, rings, smooth)


def leaf(
	asset: Asset,
	base: Vec3,
	tip: Vec3,
	width: float,
	thickness: float,
	material: str,
	roll: float = 0.0,
) -> None:
	direction = norm(sub(tip, base))
	if abs(direction[1]) > 0.82:
		side = (math.cos(roll), 0.0, math.sin(roll))
	else:
		side = norm(cross((0.0, 1.0, 0.0), direction))
		c = math.cos(roll)
		s = math.sin(roll)
		side = add(mul(side, c), mul(norm(cross(direction, side)), s))
	normal_axis = norm(cross(direction, side))
	center = lerp(base, tip, 0.52)
	ellipsoid(asset, center, mul(side, width), mul(normal_axis, thickness), mul(sub(tip, base), 0.52), material, 8, 5)
	cylinder(asset, base, lerp(base, tip, 0.76), max(0.018, thickness * 0.34), max(0.010, thickness * 0.18), "leaf_light", 6)


def flower(asset: Asset, center: Vec3, radius: float, material: str, facing: Vec3 = (0, 1, 0)) -> None:
	# A readable five-petal crown with no face-like center.
	up = norm(facing)
	reference = (1.0, 0.0, 0.0) if abs(up[0]) < 0.8 else (0.0, 0.0, 1.0)
	u = norm(cross(up, reference))
	v = norm(cross(up, u))
	for index in range(5):
		angle = index / 5.0 * math.tau
		d = add(mul(u, math.cos(angle)), mul(v, math.sin(angle)))
		petal_center = add(center, mul(d, radius * 0.60))
		ellipsoid(asset, petal_center, mul(d, radius * 0.58), mul(up, radius * 0.15), mul(norm(cross(up, d)), radius * 0.34), material, 8, 4)
	sphere(asset, center, (radius * 0.30, radius * 0.24, radius * 0.30), "gold", 8, 4)


def shell_fan(asset: Asset, center: Vec3, scale: float, facing: float = 1.0) -> None:
	hub = add(center, (0.0, 0.0, 0.04 * facing))
	sphere(asset, hub, (0.50 * scale, 0.28 * scale, 0.18 * scale), "gold", 8, 4)
	for index in range(7):
		t = index / 6.0
		angle = math.radians(-68.0 + 136.0 * t)
		tip = add(center, (math.sin(angle) * 1.22 * scale, math.cos(angle) * 0.92 * scale + 0.20 * scale, 0.0))
		cylinder(asset, hub, tip, 0.055 * scale, 0.035 * scale, "pearl", 6)
		sphere(asset, tip, (0.27 * scale, 0.18 * scale, 0.12 * scale), "aqua_light" if index % 2 else "coral_light", 7, 4)


def arch_band(asset: Asset, radius: float, width: float, depth: float, material: str, segments: int = 24) -> None:
	s = asset.surface(material)
	inner = radius - width * 0.5
	outer = radius + width * 0.5
	for index in range(segments):
		a0 = math.pi * index / segments
		a1 = math.pi * (index + 1) / segments
		def p(r: float, angle: float, z: float) -> Vec3:
			return (math.cos(angle) * r, math.sin(angle) * r, z)
		o0f, o1f = p(outer, a0, depth * 0.5), p(outer, a1, depth * 0.5)
		i0f, i1f = p(inner, a0, depth * 0.5), p(inner, a1, depth * 0.5)
		o0b, o1b = p(outer, a0, -depth * 0.5), p(outer, a1, -depth * 0.5)
		i0b, i1b = p(inner, a0, -depth * 0.5), p(inner, a1, -depth * 0.5)
		s.quad(i0f, o0f, o1f, i1f, (0, 0, 1))
		s.quad(o0b, i0b, i1b, o1b, (0, 0, -1))
		s.quad(o0f, o0b, o1b, o1f)
		s.quad(i0b, i0f, i1f, i1b)


def ellipse_band(asset: Asset, center: tuple[float, float], radius_x: float,
	radius_y: float, width: float, depth: float, material: str,
	tilt: float = 0.0, segments: int = 32) -> None:
	"""Build a closed oval rim in the XY plane for a readable open wing."""
	s = asset.surface(material)
	inner_x = radius_x - width
	inner_y = radius_y - width
	cos_tilt = math.cos(tilt)
	sin_tilt = math.sin(tilt)
	def p(rx: float, ry: float, angle: float, z: float) -> Vec3:
		local_x = math.cos(angle) * rx
		local_y = math.sin(angle) * ry
		return (
			center[0] + local_x * cos_tilt - local_y * sin_tilt,
			center[1] + local_x * sin_tilt + local_y * cos_tilt,
			z,
		)
	for index in range(segments):
		a0 = math.tau * index / segments
		a1 = math.tau * (index + 1) / segments
		o0f, o1f = p(radius_x, radius_y, a0, depth * 0.5), p(radius_x, radius_y, a1, depth * 0.5)
		i0f, i1f = p(inner_x, inner_y, a0, depth * 0.5), p(inner_x, inner_y, a1, depth * 0.5)
		o0b, o1b = p(radius_x, radius_y, a0, -depth * 0.5), p(radius_x, radius_y, a1, -depth * 0.5)
		i0b, i1b = p(inner_x, inner_y, a0, -depth * 0.5), p(inner_x, inner_y, a1, -depth * 0.5)
		s.quad(i0f, o0f, o1f, i1f, (0, 0, 1))
		s.quad(o0b, i0b, i1b, o1b, (0, 0, -1))
		s.quad(o0f, o0b, o1b, o1f)
		s.quad(i0b, i0f, i1f, i1b)


def barrel_canopy(asset: Asset, center: Vec3, width: float, length_value: float,
	rise: float, thickness: float, segments: int = 12) -> None:
	"""Build a shallow segmented shell canopy along the Z axis."""
	for index in range(segments):
		t0 = -1.0 + 2.0 * index / segments
		t1 = -1.0 + 2.0 * (index + 1) / segments
		a0 = t0 * math.pi * 0.5
		a1 = t1 * math.pi * 0.5
		x0 = center[0] + math.sin(a0) * width * 0.5
		x1 = center[0] + math.sin(a1) * width * 0.5
		y0 = center[1] + math.cos(a0) * rise
		y1 = center[1] + math.cos(a1) * rise
		front = center[2] + length_value * 0.5
		back = center[2] - length_value * 0.5
		material = "coral_light" if index % 3 else "pearl"
		s = asset.surface(material)
		top_a = (x0, y0, front)
		top_b = (x1, y1, front)
		top_c = (x1, y1, back)
		top_d = (x0, y0, back)
		under_a = (x0, y0 - thickness, front)
		under_b = (x1, y1 - thickness, front)
		under_c = (x1, y1 - thickness, back)
		under_d = (x0, y0 - thickness, back)
		s.quad(top_a, top_b, top_c, top_d)
		s.quad(under_d, under_c, under_b, under_a)
		s.quad(under_a, under_b, top_b, top_a)
		s.quad(top_d, top_c, under_c, under_d)
	# Gold ribs make the shell segmentation readable at train speed.
	for rib_index in range(0, segments + 1, 2):
		t = -1.0 + 2.0 * rib_index / segments
		angle = t * math.pi * 0.5
		x = center[0] + math.sin(angle) * width * 0.5
		y = center[1] + math.cos(angle) * rise + 0.035
		cylinder(asset, (x, y, center[2] - length_value * 0.5),
			(x, y, center[2] + length_value * 0.5), 0.055, 0.055, "gold", 6)


def baby_rosette() -> Asset:
	a = Asset("lagoon_baby_rosette", "grounded_baby_plant")
	sphere(a, (0, 0.12, 0), (0.42, 0.18, 0.42), "soil", 9, 4)
	sphere(a, (0, 0.38, 0), (0.30, 0.32, 0.30), "leaf", 9, 5)
	for index in range(8):
		angle = index / 8.0 * math.tau
		base = (math.cos(angle) * 0.16, 0.28, math.sin(angle) * 0.16)
		length_value = 1.08 if index % 2 == 0 else 0.82
		tip = (math.cos(angle) * length_value, 0.58 + 0.16 * (index % 2), math.sin(angle) * length_value)
		leaf(a, base, tip, 0.28 if index % 2 == 0 else 0.22, 0.075, "leaf_light" if index % 3 == 0 else "leaf", angle)
	# New center growth makes it unambiguously a whole young plant.
	leaf(a, (0, 0.40, 0), (-0.18, 1.15, 0.08), 0.16, 0.06, "mint", 0.4)
	leaf(a, (0, 0.40, 0), (0.22, 0.98, -0.04), 0.14, 0.05, "leaf_light", -0.5)
	return a


def meadow_shrub() -> Asset:
	a = Asset("lagoon_meadow_shrub", "developed_meadow_shrub")
	sphere(a, (0, 0.12, 0), (0.72, 0.20, 0.62), "soil", 9, 4)
	trunk_top = (0.0, 1.85, 0.0)
	cylinder(a, (0, 0.12, 0), trunk_top, 0.18, 0.10, "wood", 8)
	branches = [(-0.90, 2.38, 0.12), (0.82, 2.68, -0.18), (-0.52, 3.02, -0.36), (0.38, 3.28, 0.22)]
	for index, tip in enumerate(branches):
		start = (0.0, 1.15 + index * 0.18, 0.0)
		cylinder(a, start, tip, 0.10, 0.055, "wood_light", 7)
		for offset in (-0.18, 0.18):
			cluster = add(tip, (offset, -0.08 + abs(offset) * 0.3, 0.13 * (-1 if index % 2 else 1)))
			sphere(a, cluster, (0.46, 0.34, 0.32), "leaf_light" if index % 2 else "leaf", 9, 5)
	# Sparse blossoms preserve the branching habit.
	flower(a, add(branches[1], (0.08, 0.22, 0.02)), 0.28, "coral_light")
	flower(a, add(branches[3], (-0.06, 0.23, 0.00)), 0.24, "lavender")
	return a


def flower_cluster(name: str, petal_material: str) -> Asset:
	a = Asset(name, "grounded_flowering_cluster")
	sphere(a, (0, 0.10, 0), (0.58, 0.16, 0.48), "soil", 9, 4)
	stems = [(-0.55, 1.85, 0.12), (-0.18, 2.35, -0.16), (0.22, 2.08, 0.14), (0.58, 1.65, -0.08), (0.02, 1.55, 0.38)]
	for index, tip in enumerate(stems):
		base = (tip[0] * 0.25, 0.16, tip[2] * 0.25)
		cylinder(a, base, tip, 0.055, 0.025, "leaf", 7)
		leaf(a, lerp(base, tip, 0.40), add(lerp(base, tip, 0.40), ((-1 if index % 2 else 1) * 0.42, 0.24, 0.08)), 0.16, 0.045, "leaf_light", index * 0.5)
		flower(a, tip, 0.34 if index == 1 else 0.29, petal_material)
	return a


def mushroom_cluster() -> Asset:
	a = Asset("lagoon_mushroom_cluster", "grounded_mushroom_family")
	sphere(a, (0, 0.10, 0), (0.72, 0.16, 0.60), "soil", 9, 4)
	rows = [(-0.48, 0.78, 0.08, 0.38), (0.02, 1.28, -0.10, 0.55), (0.56, 0.68, 0.16, 0.33), (0.30, 0.92, 0.52, 0.40)]
	for index, (x, height_value, z, radius) in enumerate(rows):
		cylinder(a, (x, 0.14, z), (x, height_value, z), radius * 0.24, radius * 0.18, "pearl", 8)
		sphere(a, (x, height_value + radius * 0.10, z), (radius, radius * 0.30, radius * 0.85), "red" if index % 2 == 0 else "coral_light", 10, 5)
		for spot_index in range(3):
			angle = spot_index / 3.0 * math.tau + index
			sphere(a, (x + math.cos(angle) * radius * 0.42, height_value + radius * 0.32, z + math.sin(angle) * radius * 0.34), (radius * 0.075,) * 3, "pearl", 7, 4)
	return a


def pond_reeds() -> Asset:
	a = Asset("lagoon_pond_reeds", "rooted_reed_bed")
	sphere(a, (0, 0.08, 0), (0.78, 0.16, 0.64), "soil", 9, 4)
	for index in range(9):
		angle = index / 9.0 * math.tau
		radius = 0.18 + 0.26 * (index % 3) / 2.0
		x, z = math.cos(angle) * radius, math.sin(angle) * radius
		height_value = 2.2 + 0.25 * (index % 4)
		cylinder(a, (x, 0.12, z), (x + 0.05 * math.sin(index), height_value, z), 0.045, 0.025, "leaf", 7)
		leaf(a, (x, 0.18, z), (x + math.cos(angle) * 0.72, 1.55 + 0.10 * (index % 2), z + math.sin(angle) * 0.72), 0.13, 0.035, "leaf_light", angle)
		leaf(a, (x, 0.18, z), (x - math.sin(angle) * 0.58, 1.25, z + math.cos(angle) * 0.58), 0.11, 0.035, "mint", -angle)
		if index % 2 == 0:
			cylinder(a, (x, height_value - 0.42, z), (x, height_value + 0.18, z), 0.10, 0.085, "wood", 8)
	return a


def river_stones() -> Asset:
	a = Asset("lagoon_river_stones", "riverbank_stone_cluster")
	rows = [(-1.05, 0.42, -0.15, 0.76), (-0.35, 0.58, 0.12, 0.92), (0.45, 0.38, -0.22, 0.64), (1.02, 0.52, 0.18, 0.78), (0.18, 0.78, 0.24, 0.66)]
	for index, (x, y, z, scale_value) in enumerate(rows):
		sphere(a, (x, y, z), (scale_value, y, scale_value * 0.72), "stone_light" if index % 2 else "stone", 8, 4)
	return a


def story_lantern() -> Asset:
	a = Asset("lagoon_story_lantern", "storybook_path_lantern")
	sphere(a, (0, 0.16, 0), (0.66, 0.18, 0.66), "stone", 9, 4)
	cylinder(a, (0, 0.16, 0), (0, 5.45, 0), 0.24, 0.16, "wood", 9)
	cylinder(a, (0, 4.85, 0), (0.78, 5.55, 0), 0.16, 0.11, "gold", 8)
	sphere(a, (0.98, 5.58, 0), (0.52, 0.62, 0.52), "pearl", 10, 6)
	cylinder(a, (0.98, 6.13, 0), (0.98, 6.38, 0), 0.24, 0.12, "gold", 8)
	shell_fan(a, (0.0, 5.42, 0.0), 0.65)
	return a


def memory_frame() -> Asset:
	a = Asset("lagoon_memory_frame", "protected_memory_display_surround")
	# Opening is 8.4 x 11.4 around the protected image plane.
	box(a, (-4.75, 0.0, 0.0), (0.75, 13.2, 0.85), "aqua")
	box(a, (4.75, 0.0, 0.0), (0.75, 13.2, 0.85), "aqua")
	box(a, (0.0, 6.20, 0.0), (10.2, 0.82, 0.85), "gold")
	box(a, (0.0, -6.20, 0.0), (10.2, 0.82, 0.85), "gold")
	box(a, (-3.5, -7.05, -0.10), (2.2, 0.55, 2.8), "stone")
	box(a, (3.5, -7.05, -0.10), (2.2, 0.55, 2.8), "stone")
	shell_fan(a, (0.0, 6.45, 0.08), 1.55)
	for side in (-1.0, 1.0):
		cylinder(a, (side * 4.75, -5.8, 0.42), (side * 4.75, 5.8, 0.42), 0.12, 0.12, "pearl", 7)
	return a


def rainbow_race_arch() -> Asset:
	a = Asset("lagoon_rainbow_race_arch", "rainbow_race_gateway")
	colors = ("red", "orange", "yellow", "green", "blue", "violet")
	for index, material in enumerate(colors):
		arch_band(a, 6.65 - index * 0.52, 0.44, 0.64, material, 28)
	for side in (-1.0, 1.0):
		base_x = side * 6.65
		sphere(a, (base_x, 0.34, 0.0), (1.10, 0.42, 1.05), "cloud", 10, 5)
		shell_fan(a, (base_x, 0.42, 0.34), 0.66, 1.0)
	return a


def butterfly_world_gate() -> Asset:
	a = Asset("lagoon_butterfly_world_gate", "four_wing_swim_through_gateway")
	# Four open oval rims preserve the book's butterfly anatomy while leaving a
	# generous central swim-through opening. No opaque wing panel blocks the view.
	for center, rx, ry, tilt, material in (
		((-8.0, 3.5), 4.5, 5.4, -0.16, "lavender_shadow"),
		((8.0, 3.5), 4.5, 5.4, 0.16, "coral"),
		((-6.7, -3.2), 3.3, 3.7, 0.20, "aqua"),
		((6.7, -3.2), 3.3, 3.7, -0.20, "leaf"),
	):
		ellipse_band(a, center, rx, ry, 0.52, 0.82, material, tilt)
	# Four visible roots tie the open rims to one thorax. They stop short of the
	# ground-level passage and read as wing veins rather than extra portal rings.
	for target in ((-3.65, 5.0, 0.0), (3.65, 5.0, 0.0),
		(-3.45, -0.2, 0.0), (3.45, -0.2, 0.0)):
		cylinder(a, (0.0, 5.1, 0.0), target, 0.16, 0.10, "gold", 7)
		sphere(a, target, (0.26, 0.26, 0.20), "gold", 8, 4)
	# Body and antennae remain above the player opening, with a countable head,
	# thorax, abdomen, and two antennae instead of a face-like ornament.
	cylinder(a, (0.0, 4.4, 0.0), (0.0, 8.7, 0.0), 0.58, 0.42, "ink", 10)
	sphere(a, (0.0, 9.35, 0.0), (0.70, 0.70, 0.62), "gold", 10, 6)
	cylinder(a, (-0.25, 9.75, 0.0), (-1.55, 11.25, 0.0), 0.10, 0.055, "ink", 7)
	cylinder(a, (0.25, 9.75, 0.0), (1.55, 11.25, 0.0), 0.10, 0.055, "ink", 7)
	sphere(a, (-1.62, 11.32, 0.0), (0.20, 0.20, 0.18), "gold", 8, 4)
	sphere(a, (1.62, 11.32, 0.0), (0.20, 0.20, 0.18), "gold", 8, 4)
	return a


def train_station() -> Asset:
	a = Asset("lagoon_train_station", "courtyard_train_station")
	box(a, (0, 0.22, 0), (5.8, 0.44, 12.0), "stone_light")
	box(a, (0, 0.47, 5.35), (5.8, 0.16, 0.70), "gold")
	box(a, (0, 0.48, -5.35), (5.8, 0.16, 0.70), "aqua")
	for z in (-4.7, 4.7):
		cylinder(a, (1.75, 0.42, z), (1.75, 5.4, z), 0.22, 0.16, "wood", 8)
		cylinder(a, (-1.75, 0.42, z), (-1.75, 5.4, z), 0.22, 0.16, "wood", 8)
		for x in (-1.75, 1.75):
			sphere(a, (x, 5.38, z), (0.34, 0.22, 0.34), "gold", 8, 4)
	barrel_canopy(a, (0, 5.35, 0), 6.2, 11.7, 1.42, 0.22, 12)
	# Broad shell crest and pearl stop marker are readable from the moving train.
	shell_fan(a, (0, 5.82, 5.93), 1.28)
	cylinder(a, (-2.0, 0.45, 0.0), (-2.0, 3.1, 0.0), 0.14, 0.10, "gold", 8)
	sphere(a, (-2.0, 3.55, 0.0), (0.52, 0.52, 0.28), "aqua_light", 9, 5)
	return a


def snowbank() -> Asset:
	a = Asset("lagoon_snowbank", "alpine_snow_edge_cluster")
	for index, row in enumerate(((-1.9, 0.42, 0.15, 1.35), (-0.7, 0.68, -0.12, 1.65), (0.75, 0.48, 0.18, 1.25), (1.75, 0.35, -0.05, 0.95))):
		x, y, z, radius = row
		sphere(a, (x, y, z), (radius, y, radius * 0.74), "snow", 9, 5)
		if index in (1, 3):
			sphere(a, (x - 0.15, y * 0.58, z + 0.16), (radius * 0.55, y * 0.34, radius * 0.45), "stone", 8, 4)
	return a


def cloud_variant(index: int) -> Asset:
	a = Asset(f"lagoon_cloud_{index}", "soft_toon_cloud_family")
	profiles = (
		[(-1.24, 0.48, 0.08, 0.72, 0.54), (-0.55, 0.78, -0.04, 0.88, 0.72), (0.24, 0.94, 0.02, 1.02, 0.86), (1.02, 0.52, -0.05, 0.72, 0.56)],
		[(-1.34, 0.42, 0.02, 0.66, 0.48), (-0.67, 0.72, -0.06, 0.84, 0.68), (0.08, 1.02, 0.05, 1.00, 0.92), (0.84, 0.76, -0.02, 0.86, 0.70), (1.42, 0.38, 0.04, 0.58, 0.44)],
		[(-1.36, 0.38, 0.03, 0.64, 0.44), (-0.76, 0.76, -0.04, 0.88, 0.72), (0.02, 0.72, 0.04, 0.94, 0.68), (0.72, 1.04, -0.03, 0.92, 0.92), (1.38, 0.42, 0.03, 0.64, 0.48)],
	)[index]
	# One broad cool shadow shelf replaces the rejected row of dark discs.
	sphere(a, (0.0, 0.12, 0.02), (1.72, 0.12, 0.60), "cloud_shadow", 14, 6, True)
	sphere(a, (0.0, 0.30, 0.0), (1.70, 0.30, 0.68), "cloud_warm", 14, 6, True)
	for lobe_index, (x, y, z, sx, sy) in enumerate(profiles):
		sphere(a, (x, y, z), (sx, sy, 0.56 + 0.04 * (lobe_index % 2)), "cloud" if lobe_index % 2 else "cloud_warm", 14, 7, True)
	return a


ASSETS: list[tuple[Asset, Path]] = [
	(baby_rosette(), KIT_OUT / "lagoon_baby_rosette.glb"),
	(flower_cluster("lagoon_flower_cluster_coral", "coral_light"), KIT_OUT / "lagoon_flower_cluster_coral.glb"),
	(flower_cluster("lagoon_flower_cluster_lavender", "lavender"), KIT_OUT / "lagoon_flower_cluster_lavender.glb"),
	(mushroom_cluster(), KIT_OUT / "lagoon_mushroom_cluster.glb"),
	(pond_reeds(), KIT_OUT / "lagoon_pond_reeds.glb"),
	(river_stones(), KIT_OUT / "lagoon_river_stones.glb"),
	(story_lantern(), KIT_OUT / "lagoon_story_lantern.glb"),
	(memory_frame(), KIT_OUT / "lagoon_memory_frame.glb"),
	(rainbow_race_arch(), KIT_OUT / "lagoon_rainbow_race_arch.glb"),
	(butterfly_world_gate(), KIT_OUT / "lagoon_butterfly_world_gate.glb"),
	(train_station(), KIT_OUT / "lagoon_train_station.glb"),
	(snowbank(), KIT_OUT / "lagoon_snowbank.glb"),
	(cloud_variant(0), CLOUD_OUT / "cloud_0.glb"),
	(cloud_variant(1), CLOUD_OUT / "cloud_1.glb"),
	(cloud_variant(2), CLOUD_OUT / "cloud_2.glb"),
]


def pack_floats(values: list[Vec3]) -> bytes:
	flat = [component for value in values for component in value]
	return struct.pack("<" + "f" * len(flat), *flat)


def pack_uints(values: list[int]) -> bytes:
	return struct.pack("<" + "I" * len(values), *values)


class GlbBuffer:
	def __init__(self) -> None:
		self.binary = bytearray()
		self.views: list[dict] = []
		self.accessors: list[dict] = []

	def view(self, data: bytes, target: int) -> int:
		while len(self.binary) % 4:
			self.binary.append(0)
		offset = len(self.binary)
		self.binary.extend(data)
		self.views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(data), "target": target})
		return len(self.views) - 1

	def accessor(self, view: int, component: int, count: int, kind: str, values: list[Vec3] | None = None) -> int:
		entry: dict = {"bufferView": view, "byteOffset": 0, "componentType": component, "count": count, "type": kind}
		if values:
			entry["min"] = [min(value[axis] for value in values) for axis in range(3)]
			entry["max"] = [max(value[axis] for value in values) for axis in range(3)]
		self.accessors.append(entry)
		return len(self.accessors) - 1


def write_glb(asset: Asset, output: Path) -> None:
	buffer = GlbBuffer()
	materials = list(asset.surfaces)
	primitives: list[dict] = []
	for material_index, material in enumerate(materials):
		surface = asset.surfaces[material]
		position_view = buffer.view(pack_floats(surface.positions), 34962)
		normal_view = buffer.view(pack_floats(surface.normals), 34962)
		index_view = buffer.view(pack_uints(surface.indices), 34963)
		position_accessor = buffer.accessor(position_view, 5126, len(surface.positions), "VEC3", surface.positions)
		normal_accessor = buffer.accessor(normal_view, 5126, len(surface.normals), "VEC3")
		index_accessor = buffer.accessor(index_view, 5125, len(surface.indices), "SCALAR")
		primitives.append({"attributes": {"POSITION": position_accessor, "NORMAL": normal_accessor}, "indices": index_accessor, "material": material_index})
	document = {
		"asset": {"version": "2.0", "generator": "Mermaid Roshan Sky Lagoon Kit Builder"},
		"scene": 0,
		"scenes": [{"name": asset.name, "nodes": [0]}],
		"nodes": [{"name": asset.name, "mesh": 0, "extras": {"role": asset.role, "style_gate": "no_single_ground_leaf"}}],
		"meshes": [{"name": asset.name + "_mesh", "primitives": primitives}],
		"materials": [{
			"name": material,
			"pbrMetallicRoughness": {"baseColorFactor": list(PALETTE[material]), "metallicFactor": 0.0, "roughnessFactor": 0.88},
			"doubleSided": False,
		} for material in materials],
		"buffers": [{"byteLength": len(buffer.binary)}],
		"bufferViews": buffer.views,
		"accessors": buffer.accessors,
	}
	json_data = json.dumps(document, separators=(",", ":")).encode("utf-8")
	json_data += b" " * ((4 - len(json_data) % 4) % 4)
	while len(buffer.binary) % 4:
		buffer.binary.append(0)
	bin_data = bytes(buffer.binary)
	total = 12 + 8 + len(json_data) + 8 + len(bin_data)
	glb = bytearray(struct.pack("<4sII", b"glTF", 2, total))
	glb.extend(struct.pack("<I4s", len(json_data), b"JSON"))
	glb.extend(json_data)
	glb.extend(struct.pack("<I4s", len(bin_data), b"BIN\x00"))
	glb.extend(bin_data)
	output.parent.mkdir(parents=True, exist_ok=True)
	output.write_bytes(glb)


def render_qa(asset: Asset, output: Path) -> None:
	try:
		from PIL import Image, ImageDraw
	except ImportError:
		return
	width = height = 760
	yaw = math.radians(-34.0)
	pitch = math.radians(20.0)
	def transform(point: Vec3) -> Vec3:
		x = math.cos(yaw) * point[0] + math.sin(yaw) * point[2]
		z = -math.sin(yaw) * point[0] + math.cos(yaw) * point[2]
		y = math.cos(pitch) * point[1] - math.sin(pitch) * z
		depth = math.sin(pitch) * point[1] + math.cos(pitch) * z
		return (x, y, depth)
	all_points = [transform(point) for surface in asset.surfaces.values() for point in surface.positions]
	min_x, max_x = min(p[0] for p in all_points), max(p[0] for p in all_points)
	min_y, max_y = min(p[1] for p in all_points), max(p[1] for p in all_points)
	scale = min((width - 90) / max(0.1, max_x - min_x), (height - 90) / max(0.1, max_y - min_y))
	off_x = width * 0.5 - (min_x + max_x) * 0.5 * scale
	off_y = height * 0.5 + (min_y + max_y) * 0.5 * scale
	triangles: list[tuple[float, list[tuple[float, float]], str, float]] = []
	light = norm((-0.35, 0.75, 0.55))
	for material, surface in asset.surfaces.items():
		for index in range(0, len(surface.indices), 3):
			ids = surface.indices[index:index + 3]
			world = [surface.positions[value] for value in ids]
			view = [transform(value) for value in world]
			face_normal = norm(cross(sub(world[1], world[0]), sub(world[2], world[0])))
			brightness = 0.72 + 0.28 * max(0.0, dot(face_normal, light))
			triangles.append((sum(value[2] for value in view) / 3.0, [(value[0] * scale + off_x, off_y - value[1] * scale) for value in view], material, brightness))
	image = Image.new("RGB", (width, height), (225, 232, 235))
	draw = ImageDraw.Draw(image)
	for _, points, material, brightness in sorted(triangles, key=lambda row: row[0]):
		color = PALETTE[material]
		fill = tuple(max(0, min(255, round(channel * brightness * 255))) for channel in color[:3])
		draw.polygon(points, fill=fill)
	output.parent.mkdir(parents=True, exist_ok=True)
	image.save(output)


def main() -> None:
	for asset, output in ASSETS:
		write_glb(asset, output)
		render_qa(asset, QA_OUT / (output.stem + ".png"))
		print(f"wrote {output.relative_to(ROOT)}: {asset.triangle_count()} triangles, {len(asset.surfaces)} materials")


if __name__ == "__main__":
	main()
