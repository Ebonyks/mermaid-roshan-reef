#!/usr/bin/env python3
"""Build the isolated full-regeneration 3D candidate pack.

Run with the worktree-local bpy runtime:
  tmp/bpy_env/Scripts/python.exe tools/build_full_texture_regen.py

The script never writes to active runtime asset paths. It creates a versioned
candidate pack and an editable Blender source under assets_src.
"""

from __future__ import annotations

import csv
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "full_texture_regen_2026-07-18"
MODEL_OUT = PACK / "models"
SOURCE_OUT = ROOT / "assets_src" / "blender" / "full_texture_regen_2026-07-18"
BLEND_OUT = SOURCE_OUT / "full_texture_regen.blend"
MANIFEST_OUT = SOURCE_OUT / "model_manifest.json"
TARGET_LEDGER = ROOT / "audit" / "full_regen_2026-07-18" / "target_ledger.csv"
for folder in (PACK, MODEL_OUT, SOURCE_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"ink": (0.075, 0.085, 0.19, 1.0),
	"indigo": (0.14, 0.10, 0.29, 1.0),
	"slate": (0.42, 0.48, 0.64, 1.0),
	"slate_light": (0.64, 0.69, 0.81, 1.0),
	"cream": (0.96, 0.92, 0.82, 1.0),
	"foam": (0.89, 0.96, 0.97, 1.0),
	"aqua": (0.27, 0.77, 0.78, 1.0),
	"aqua_light": (0.55, 0.90, 0.85, 1.0),
	"ocean": (0.25, 0.53, 0.69, 1.0),
	"lavender": (0.66, 0.49, 0.84, 1.0),
	"violet": (0.38, 0.25, 0.60, 1.0),
	"coral": (1.0, 0.64, 0.60, 1.0),
	"rose": (0.91, 0.55, 0.72, 1.0),
	"gold": (0.96, 0.72, 0.22, 1.0),
	"mint": (0.50, 0.83, 0.56, 1.0),
	"leaf": (0.25, 0.62, 0.47, 1.0),
	"leaf_dark": (0.13, 0.38, 0.34, 1.0),
	"wood": (0.52, 0.28, 0.25, 1.0),
	"wood_light": (0.72, 0.43, 0.35, 1.0),
	"ice": (0.62, 0.85, 0.92, 1.0),
	"snow": (0.88, 0.93, 0.97, 1.0),
	"red": (0.76, 0.25, 0.31, 1.0),
	"orange": (0.92, 0.48, 0.22, 1.0),
	"yellow": (0.98, 0.79, 0.28, 1.0),
	"blue": (0.34, 0.55, 0.82, 1.0),
}


def srgb_channel(value: float) -> float:
	return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def material(name: str, color: tuple[float, float, float, float], roughness: float = 0.84) -> bpy.types.Material:
	linear = tuple(srgb_channel(channel) for channel in color[:3]) + (color[3],)
	mat = bpy.data.materials.new("MR_FULL_" + name)
	mat.diffuse_color = linear
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = linear
	bsdf.inputs["Roughness"].default_value = roughness
	bsdf.inputs["Metallic"].default_value = 0.0
	if "Specular IOR Level" in bsdf.inputs:
		bsdf.inputs["Specular IOR Level"].default_value = 0.18
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root_object(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def assign(obj: bpy.types.Object, mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	obj.data.materials.append(mat)
	obj.parent = parent
	return obj


def smooth(obj: bpy.types.Object) -> bpy.types.Object:
	if obj.type == "MESH":
		for polygon in obj.data.polygons:
			polygon.use_smooth = True
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
	modifier = obj.modifiers.new("storybook_rounding", "BEVEL")
	modifier.width = max(0.005, width)
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	apply_modifier(obj, modifier)
	return smooth(obj)


def rounded_box(name: str, location: tuple[float, float, float], size: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0), radius: float = 0.12) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	return bevel(obj, min(radius, min(size) * 0.16), 2)


def sphere(name: str, location: tuple[float, float, float], scale: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object, segments: int = 16, rings: int = 10) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	return smooth(obj)


def ico(name: str, location: tuple[float, float, float], scale: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object, seed: int = 0, subdivisions: int = 2) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	if seed:
		rng = random.Random(seed)
		for vertex in obj.data.vertices:
			vertex.co *= 0.9 + rng.random() * 0.2
	assign(obj, mat, parent)
	return smooth(obj)


def cylinder(name: str, location: tuple[float, float, float], radius: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0), vertices: int = 14) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return bevel(obj, min(radius * 0.12, depth * 0.06), 2)


def cone(name: str, location: tuple[float, float, float], radius1: float, radius2: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0), vertices: int = 14) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2,
		depth=depth, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return smooth(obj)


def torus(name: str, location: tuple[float, float, float], major: float, minor: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=24,
		minor_segments=8, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return smooth(obj)


def tube(name: str, points: list[tuple[float, float, float]], radius: float,
		mat: bpy.types.Material, parent: bpy.types.Object, resolution: int = 1) -> bpy.types.Object:
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions = "3D"
	curve.resolution_u = resolution
	curve.bevel_depth = radius
	curve.bevel_resolution = 2
	spline = curve.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, co in zip(spline.bezier_points, points):
		point.co = co
		point.handle_left_type = "AUTO"
		point.handle_right_type = "AUTO"
	obj = bpy.data.objects.new(name, curve)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	curve.materials.append(mat)
	return obj


def panel_xz(name: str, outline: list[tuple[float, float]], depth: float,
		location: tuple[float, float, float], mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	verts = [(x, -depth * 0.5, z) for x, z in outline] + [(x, depth * 0.5, z) for x, z in outline]
	count = len(outline)
	faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, count * 2))]
	faces += [(i, (i + 1) % count, count + (i + 1) % count, count + i) for i in range(count)]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.rotation_euler = rotation
	assign(obj, mat, parent)
	return bevel(obj, min(depth * 0.25, 0.08), 2)


def star_panel(name: str, points: int, outer: float, inner: float, depth: float,
		location: tuple[float, float, float], mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: float = 0.0) -> bpy.types.Object:
	outline: list[tuple[float, float]] = []
	for index in range(points * 2):
		angle = rotation + math.tau * index / (points * 2) + math.pi * 0.5
		radius = outer if index % 2 == 0 else inner
		outline.append((math.cos(angle) * radius, math.sin(angle) * radius))
	return panel_xz(name, outline, depth, location, mat, parent)


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result += family(child)
	return result


def bounds(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	points: list[Vector] = []
	for member in family(obj):
		if member.type == "MESH":
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
		elif member.type == "CURVE":
			for spline in member.data.splines:
				if spline.type == "BEZIER":
					points += [member.matrix_world @ point.co for point in spline.bezier_points]
				else:
					points += [member.matrix_world @ Vector(point.co[:3]) for point in spline.points]
	if not points:
		return Vector((0, 0, 0)), Vector((0, 0, 0))
	return (
		Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points))),
		Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points))),
	)


def component_names(obj: bpy.types.Object) -> list[str]:
	return sorted(member.name for member in family(obj) if member is not obj)


def build_coral(name: str, variant: int = 0, low: bool = False) -> bpy.types.Object:
	r = root_object(name)
	rng = random.Random(1100 + variant)
	ico("coral_base", (0, 0, 0.22), (1.35, 1.0, 0.42), MATS["slate"], r, 50 + variant)
	family = variant % 6
	main = [MATS["coral"], MATS["rose"], MATS["aqua"], MATS["lavender"]][variant % 4]
	accent = [MATS["gold"], MATS["aqua"], MATS["lavender"], MATS["coral"]][variant % 4]
	if family == 0:
		for index in range(4):
			angle = -0.75 + index * 0.5
			x = (index - 1.5) * 0.42
			height = 1.9 + index % 2 * 0.55
			mid = (x, math.sin(angle) * 0.25, height * 0.58)
			top = (x + math.sin(angle) * 0.35, math.cos(angle) * 0.3, height)
			tube(f"antler_trunk_{index}", [(x * 0.55, 0, 0.32), mid, top], 0.18, main, r)
			for fork in (-1, 1):
				end = (top[0] + fork * 0.42, top[1] + fork * 0.12, top[2] + 0.48)
				tube(f"antler_fork_{index}_{fork}", [mid, top, end], 0.11, main, r)
				sphere(f"antler_tip_{index}_{fork}", end, (0.13, 0.13, 0.12), accent, r, 10, 6)
	elif family == 1:
		tube("fan_stem", [(0, 0, 0.3), (0, 0, 1.2)], 0.22, main, r)
		for branch in range(7):
			x = (branch - 3) * 0.38
			height = 1.65 + (3 - abs(branch - 3)) * 0.28
			tube(f"fan_branch_{branch}", [(0, 0, 0.8), (x * 0.55, 0, 1.35), (x, 0, height)], 0.085, main, r)
			if branch < 6:
				tube(f"fan_lattice_{branch}", [(x, 0, height - 0.25), (x + 0.38, 0, height + 0.05)], 0.055, accent, r)
	elif family == 2:
		ico("brain_mound", (0, 0, 0.85), (1.25, 1.0, 0.78), main, r, 1120 + variant, subdivisions=3)
		for groove in range(5):
			z = 0.48 + groove * 0.22
			tube(f"brain_groove_{groove}", [(-0.92, -0.76, z), (-0.48, -0.96, z + 0.14),
				(-0.05, -1.02, z - 0.04), (0.4, -0.94, z + 0.12), (0.88, -0.74, z)],
				0.045, MATS["indigo"], r)
	elif family == 3:
		cylinder("table_stem", (0, 0, 0.85), 0.28, 1.35, main, r, vertices=12)
		for level, (z, radius) in enumerate(((1.25, 1.25), (1.75, 0.92), (2.18, 0.62))):
			ico(f"table_plate_{level}", (0.12 * level, 0, z), (radius, radius * 0.82, 0.18),
				main if level != 1 else accent, r, 1140 + variant * 3 + level, subdivisions=2)
			for scallop in range(7):
				angle = math.tau * scallop / 7 + level * 0.2
				sphere(f"plate_scallop_{level}_{scallop}", (math.cos(angle) * radius, math.sin(angle) * radius * 0.82, z),
					(0.16, 0.14, 0.1), accent, r, 10, 6)
	elif family == 4:
		for whip in range(7):
			x = (whip - 3) * 0.28
			height = rng.uniform(1.8, 3.0)
			tube(f"sea_whip_{whip}", [(x, 0, 0.3), (x + math.sin(whip) * 0.28, 0.1, height * 0.55),
				(x + math.cos(whip) * 0.38, -0.05, height)], 0.09, main if whip % 2 else accent, r)
	else:
		for finger in range(6):
			angle = math.tau * finger / 6
			radius = 0.25 + (finger % 3) * 0.2
			x, y = math.cos(angle) * radius, math.sin(angle) * radius
			height = 1.25 + (finger % 4) * 0.38
			cone(f"finger_{finger}", (x, y, 0.3 + height * 0.5), 0.22, 0.12, height,
				main if finger % 2 else accent, r, vertices=12)
			sphere(f"finger_tip_{finger}", (x, y, 0.3 + height), (0.13, 0.13, 0.12),
				main if finger % 2 else accent, r, 10, 6)
	if low:
		r.scale = (0.78, 0.78, 0.78)
	return r


def build_vegetation(name: str, kind: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	rng = random.Random(2200 + variant)
	if kind == "kelp":
		for index in range(7):
			x = (index - 3) * 0.34 + rng.uniform(-0.12, 0.12)
			height = rng.uniform(2.0, 3.7)
			outline = [(-0.15, 0), (0.18, 0.05), (0.08, height * 0.32), (0.24, height * 0.58),
				(0.04, height), (-0.18, height * 0.72), (-0.08, height * 0.38)]
			y = rng.uniform(-0.4, 0.4)
			panel_xz(f"kelp_blade_{index}", outline, 0.11, (x, y, 0),
				MATS["leaf"] if index % 2 else MATS["leaf_dark"], r,
				rotation=(0, 0, rng.uniform(-0.14, 0.14)))
			tube(f"kelp_midrib_{index}", [(x, y - 0.08, 0.08), (x + 0.04, y - 0.08, height * 0.52),
				(x, y - 0.08, height * 0.92)], 0.025, MATS["mint"], r)
	elif kind == "seagrass":
		for index in range(11):
			angle = math.tau * index / 11 + rng.uniform(-0.2, 0.2)
			radius = rng.uniform(0.2, 1.1)
			height = rng.uniform(0.8, 1.8)
			x, y = math.cos(angle) * radius, math.sin(angle) * radius
			outline = [(-0.07, 0), (0.07, 0), (0.11, height * 0.52), (0, height), (-0.08, height * 0.55)]
			panel_xz(f"grass_blade_{index}", outline, 0.055, (x, y, 0),
				MATS["mint"] if index % 3 == 0 else MATS["leaf"], r,
				rotation=(0, 0, rng.uniform(-0.18, 0.18)))
	elif kind == "palm":
		for segment in range(5):
			cylinder(f"trunk_{segment}", (0.08 * segment, 0, 0.45 + segment * 0.8),
				0.27 - segment * 0.02, 0.9, MATS["wood_light"], r, rotation=(0, 0.08, 0))
		for index in range(7):
			angle = math.tau * index / 7
			points = [(0.4, 0), (1.6, 0.2), (2.4, 0), (1.5, -0.22)]
			leaf = panel_xz(f"palm_leaf_{index}", points, 0.1,
				(0.38, 0, 4.2), MATS["leaf"] if index % 2 else MATS["mint"], r)
			leaf.rotation_euler = (math.radians(68), 0, angle)
	else:
		raise ValueError(kind)
	return r


def build_rock_family(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	rng = random.Random(3300 + variant)
	for index in range(4 + variant % 2):
		angle = math.tau * index / (4 + variant % 2)
		radius = 0.45 + index * 0.16
		x, y = math.cos(angle) * radius, math.sin(angle) * radius
		scale = rng.uniform(0.65, 1.25)
		ico(f"rock_{index}", (x, y, scale * 0.48), (scale, scale * 0.78, scale * 0.66),
			MATS["slate"] if index % 2 else MATS["slate_light"], r, 3300 + variant * 20 + index)
	for index in range(3):
		tube(f"aqua_vein_{index}", [(-0.6 + index * 0.4, -0.7, 0.55),
			(-0.45 + index * 0.45, 0.0, 0.75), (-0.25 + index * 0.5, 0.55, 0.5)],
			0.035, MATS["aqua"], r)
	return r


def build_cloud(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	rng = random.Random(4400 + variant)
	length = 4.1 + variant * 0.45
	shadow = MATS["slate_light"] if variant % 2 == 0 else MATS["lavender"]
	rounded_box("cloud_outline_shelf", (0, 0.14, 0.27), (length + 0.18, 1.38, 0.25),
		MATS["indigo"], r, radius=0.34)
	rounded_box("cloud_shadow_shelf", (0, 0.12, 0.43), (length, 1.25, 0.42), shadow, r, radius=0.36)
	rounded_box("cloud_body_shelf", (0, -0.02, 0.7), (length * 0.93, 1.45, 0.62), MATS["foam"], r, radius=0.48)
	lobes = 5 + variant % 2
	for index in range(lobes):
		x = (index - (lobes - 1) * 0.5) * length / (lobes + 0.8) + rng.uniform(-0.12, 0.12)
		center_bias = 1.0 - abs(index - (lobes - 1) * 0.5) / max(1.0, lobes * 0.5)
		z = 0.92 + center_bias * 0.75 + rng.uniform(-0.05, 0.16)
		sphere(f"cloud_lobe_{index}", (x, -0.08, z),
			(0.72 + center_bias * 0.35, 0.74, 0.58 + center_bias * 0.4), MATS["foam"], r, 16, 10)
	for curl in (-1, 1):
		tube(f"wind_curl_outline_{curl}", [(curl * length * 0.28, -0.84, 0.5),
			(curl * length * 0.42, -0.84, 0.32), (curl * length * 0.52, -0.84, 0.48)],
			0.075, MATS["indigo"], r)
		tube(f"wind_curl_{curl}", [(curl * length * 0.28, -0.86, 0.5),
			(curl * length * 0.42, -0.86, 0.34), (curl * length * 0.52, -0.86, 0.48)],
			0.038, shadow, r)
	return r


def build_fish(name: str, variant: int = 0, clown: bool = False) -> bpy.types.Object:
	r = root_object(name)
	body_mat = MATS["orange"] if clown else [MATS["aqua"], MATS["rose"], MATS["lavender"]][variant % 3]
	sphere("fish_body", (0, 0, 0), (1.7, 0.55, 0.9), body_mat, r, 20, 12)
	panel_xz("tail_upper", [(-0.1, 0), (-1.0, 0.95), (-0.82, 0), (-1.0, -0.1)], 0.18,
		(-1.55, 0, 0.15), MATS["coral"] if not clown else MATS["cream"], r)
	panel_xz("tail_lower", [(-0.1, 0.1), (-1.0, 0), (-0.82, -0.95), (-0.05, -0.25)], 0.18,
		(-1.55, 0, -0.1), MATS["coral"] if not clown else MATS["cream"], r)
	panel_xz("dorsal_fin", [(-0.75, 0), (0.0, 0.85), (0.65, 0)], 0.16,
		(-0.05, 0, 0.72), MATS["gold"], r)
	for side in (-1, 1):
		fin = panel_xz(f"pectoral_fin_{side}", [(-0.4, 0), (0.55, 0.5), (0.45, -0.35)], 0.12,
			(0.25, side * 0.5, -0.05), MATS["gold"], r)
		fin.rotation_euler.x = side * math.radians(72)
	for side in (-1, 1):
		sphere(f"eye_{side}", (1.35, side * 0.42, 0.22), (0.14, 0.08, 0.14), MATS["ink"], r, 12, 8)
	if clown:
		for x in (-0.65, 0.35):
			torus(f"clown_band_{x}", (x, 0, 0), 0.63, 0.11, MATS["cream"], r, rotation=(math.pi * 0.5, 0, 0))
	return r


def build_octopus(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	main = MATS["lavender"] if variant % 2 == 0 else MATS["coral"]
	sphere("octopus_mantle", (0, 0, 1.45), (0.95, 0.85, 1.2), main, r, 20, 12)
	sphere("octopus_head", (0, 0, 0.72), (1.0, 0.88, 0.62), main, r, 18, 10)
	for side in (-1, 1):
		sphere(f"eye_{side}", (0.58, side * 0.68, 0.9), (0.18, 0.1, 0.22), MATS["cream"], r, 12, 8)
		sphere(f"pupil_{side}", (0.69, side * 0.77, 0.9), (0.08, 0.05, 0.11), MATS["ink"], r, 10, 6)
	for index in range(8):
		angle = math.tau * index / 8
		x, y = math.cos(angle) * 0.55, math.sin(angle) * 0.55
		tube(f"arm_{index}", [(x, y, 0.5), (math.cos(angle) * 1.15, math.sin(angle) * 1.15, 0.05),
			(math.cos(angle + 0.35 * (-1 if index % 2 else 1)) * 1.95,
			 math.sin(angle + 0.35 * (-1 if index % 2 else 1)) * 1.95, 0.18)],
			0.17, main, r)
	return r


def build_shrimp(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	main = MATS["coral"] if variant % 2 == 0 else MATS["rose"]
	for index in range(7):
		x = -0.85 + index * 0.3
		z = 0.25 + math.sin(index / 6 * math.pi) * 0.55
		sphere(f"abdomen_segment_{index}", (x, 0, z), (0.32, 0.38, 0.3), main, r, 14, 8)
	sphere("carapace", (1.15, 0, 0.58), (0.72, 0.55, 0.48), MATS["orange"], r, 18, 10)
	for side in (-1, 1):
		sphere(f"eye_{side}", (1.62, side * 0.35, 0.82), (0.12, 0.09, 0.12), MATS["ink"], r, 10, 6)
		tube(f"antenna_{side}_a", [(1.55, side * 0.28, 0.75), (2.1, side * 0.55, 1.15),
			(3.05, side * 0.9, 1.25)], 0.035, MATS["cream"], r)
		tube(f"antenna_{side}_b", [(1.52, side * 0.2, 0.68), (2.0, side * 0.4, 0.65),
			(2.75, side * 0.7, 0.45)], 0.028, MATS["cream"], r)
		for index in range(5):
			x = -0.4 + index * 0.38
			tube(f"leg_{side}_{index}", [(x, side * 0.25, 0.2), (x + 0.15, side * 0.65, -0.1),
				(x + 0.35, side * 0.9, -0.05)], 0.04, main, r)
	for side in (-1, 1):
		panel_xz(f"tail_fan_{side}", [(-0.2, 0), (-0.95, side * 0.68), (-0.9, 0), (-0.25, -side * 0.15)],
			0.12, (-1.05, 0, 0.25), MATS["rose"], r)
	return r


def build_jellyfish(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	main = [MATS["aqua"], MATS["lavender"], MATS["rose"]][variant % 3]
	sphere("bell", (0, 0, 1.5), (1.25, 1.25, 0.82), main, r, 24, 12)
	torus("bell_rim", (0, 0, 1.14), 1.08, 0.12, MATS["cream"], r)
	for index in range(4):
		angle = math.tau * index / 4
		tube(f"oral_arm_{index}", [(math.cos(angle) * 0.4, math.sin(angle) * 0.4, 1.1),
			(math.cos(angle + 0.4) * 0.65, math.sin(angle + 0.4) * 0.65, 0.35),
			(math.cos(angle - 0.2) * 0.52, math.sin(angle - 0.2) * 0.52, -0.55)],
			0.1, MATS["cream"], r)
	for index in range(8):
		angle = math.tau * index / 8
		tube(f"tentacle_{index}", [(math.cos(angle) * 0.9, math.sin(angle) * 0.9, 1.05),
			(math.cos(angle + 0.25) * 1.05, math.sin(angle + 0.25) * 1.05, 0.15),
			(math.cos(angle - 0.2) * 0.85, math.sin(angle - 0.2) * 0.85, -1.0)],
			0.035, main, r)
	return r


def build_butterfly(name: str, variant: int = 0, gate: bool = False) -> bpy.types.Object:
	r = root_object(name)
	scale = 1.65 if gate else 1.0
	wing_colors = [MATS["coral"], MATS["aqua"], MATS["lavender"], MATS["gold"]]
	body = MATS["ink"]
	cone("body", (-0.3 * scale, 0, 0), 0.07 * scale, 0.14 * scale, 1.4 * scale, body, r,
		rotation=(0, math.pi * 0.5, 0), vertices=14)
	sphere("thorax", (0.2 * scale, 0, 0), (0.3 * scale, 0.25 * scale, 0.3 * scale), body, r, 12, 8)
	sphere("head", (0.82 * scale, 0, 0), (0.22 * scale, 0.2 * scale, 0.22 * scale), body, r, 12, 8)
	for side in (-1, 1):
		front_outline = [(0.05 * scale, side * 0.16 * scale), (0.22 * scale, side * 0.68 * scale),
			(0.42 * scale, side * 1.24 * scale), (0.78 * scale, side * 1.58 * scale),
			(1.18 * scale, side * 1.66 * scale), (1.5 * scale, side * 1.42 * scale),
			(1.65 * scale, side * 1.02 * scale), (1.55 * scale, side * 0.62 * scale),
			(1.15 * scale, side * 0.34 * scale), (0.52 * scale, side * 0.18 * scale)]
		rear_outline = [(-0.18 * scale, side * 0.14 * scale), (-0.3 * scale, side * 0.58 * scale),
			(-0.48 * scale, side * 1.02 * scale), (-0.82 * scale, side * 1.34 * scale),
			(-1.2 * scale, side * 1.42 * scale), (-1.5 * scale, side * 1.2 * scale),
			(-1.62 * scale, side * 0.82 * scale), (-1.46 * scale, side * 0.48 * scale),
			(-1.08 * scale, side * 0.24 * scale), (-0.62 * scale, side * 0.15 * scale)]
		front = panel_xz(f"front_wing_{'left' if side > 0 else 'right'}", front_outline, 0.09 * scale,
			(0, 0, 0), wing_colors[variant % 4], r)
		rear = panel_xz(f"rear_wing_{'left' if side > 0 else 'right'}", rear_outline, 0.09 * scale,
			(0, 0.03, 0), wing_colors[(variant + 2) % 4], r)
		front_inset = [(x * 0.66, z * 0.66) for x, z in front_outline]
		rear_inset = [(x * 0.62, z * 0.62) for x, z in rear_outline]
		panel_xz(f"front_wing_motif_{'left' if side > 0 else 'right'}", front_inset, 0.045 * scale,
			(0, -0.075, 0), wing_colors[(variant + 1) % 4], r)
		panel_xz(f"rear_wing_motif_{'left' if side > 0 else 'right'}", rear_inset, 0.045 * scale,
			(0, -0.08, 0), MATS["cream"], r)
		for spot in range(3):
			spot_x = (0.45 + spot * 0.34) * scale
			spot_z = side * (0.45 + spot * 0.3) * scale
			sphere(f"wing_spot_{side}_{spot}", (spot_x, -0.08, spot_z),
				(0.12 * scale, 0.025 * scale, 0.12 * scale), MATS["cream"], r, 10, 6)
		tube(f"antenna_{side}", [(0.82 * scale, 0, side * 0.08 * scale),
			(1.15 * scale, 0, side * 0.32 * scale), (1.48 * scale, 0, side * 0.52 * scale)], 0.035 * scale, body, r)
		for leg in range(3):
			x = (0.25 - leg * 0.35) * scale
			tube(f"leg_{side}_{leg}", [(x, 0, side * 0.12 * scale),
				(x - 0.18 * scale, 0, side * (0.42 + leg * 0.08) * scale),
				(x - 0.05 * scale, 0, side * (0.62 + leg * 0.12) * scale)], 0.025 * scale, body, r)
	if gate:
		torus("gate_opening", (0, 0.18, 0), 1.9 * scale, 0.16 * scale,
			MATS["indigo"], r, rotation=(math.pi * 0.5, 0, 0))
		torus("gate_inlay", (0, 0.16, 0), 1.72 * scale, 0.055 * scale,
			MATS["aqua"], r, rotation=(math.pi * 0.5, 0, 0))
		for side in (-1, 1):
			ico(f"gate_foot_{side}", (side * 1.55 * scale, 0, -1.65 * scale),
				(0.62 * scale, 0.48 * scale, 0.32 * scale), MATS["slate"], r, 4700 + side + variant * 4)
	return r


def build_star(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	points = (5, 6, 8)[variant % 3]
	colors = [MATS["gold"], MATS["lavender"], MATS["aqua"]]
	star_panel("star_outline", points, 1.82, 0.74, 0.3, (0, 0.08, 0), MATS["indigo"], r,
		rotation=math.pi * 0.5)
	star_panel("star_body", points, 1.62, 0.66, 0.34, (0, -0.08, 0), colors[variant % 3], r,
		rotation=math.pi * 0.5)
	star_panel("star_inset", points, 0.88, 0.36, 0.38, (0, -0.26, 0), MATS["cream"], r,
		rotation=math.pi * 0.5)
	if variant == 0:
		for side in (-1, 1):
			tube(f"dream_ribbon_{side}", [(-1.0, 0.18, side * 0.35), (-1.85, 0.18, side * 0.65),
				(-2.35, 0.18, side * 0.42)], 0.11, MATS["aqua"] if side > 0 else MATS["coral"], r)
	elif variant == 1:
		rounded_box("crown_band", (0, 0.14, -1.18), (2.2, 0.28, 0.28), MATS["gold"], r, radius=0.1)
		for index in range(3):
			sphere(f"crown_jewel_{index}", ((index - 1) * 0.58, -0.25, -1.18),
				(0.16, 0.08, 0.16), [MATS["coral"], MATS["aqua"], MATS["rose"]][index], r, 10, 6)
	else:
		for radius, color in ((2.08, MATS["indigo"]), (2.32, MATS["gold"])):
			torus(f"chamber_halo_{radius}", (0, 0.18, 0), radius, 0.065, color, r,
				rotation=(math.pi * 0.5, 0, 0))
	return r


def build_shell_portal(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	torus("portal_opening", (0, 0, 2.3), 2.2, 0.28, MATS["indigo"], r, rotation=(math.pi * 0.5, 0, 0))
	for index in range(9):
		angle = math.pi * index / 8
		x = math.cos(angle) * 2.25
		z = 2.3 + math.sin(angle) * 2.25
		tube(f"shell_rib_{index}", [(0, 0.15, 2.15), (x * 0.72, 0.05, z * 0.82), (x, 0, z)],
			0.12, MATS["coral"] if (index + variant) % 2 else MATS["cream"], r)
	for side in (-1, 1):
		ico(f"portal_base_{side}", (side * 2.1, 0, 0.45), (0.9, 0.7, 0.65), MATS["slate"], r,
			5100 + variant * 10 + side)
	return r


def build_castle(name: str, variant: int = 0, compact: bool = False) -> bpy.types.Object:
	r = root_object(name)
	width = 3.2 if compact else 5.0
	rounded_box("castle_keep", (0, 0, 2.0), (width, 2.6, 3.8), MATS["cream"], r, radius=0.28)
	for index, x in enumerate((-width * 0.58, width * 0.58)):
		cylinder(f"tower_{index}", (x, 0, 2.35), 1.05, 4.7, MATS["slate_light"], r, vertices=16)
		cone(f"tower_roof_{index}", (x, 0, 5.15), 1.4, 0.12, 1.8,
			MATS["lavender"] if (index + variant) % 2 else MATS["ocean"], r, vertices=16)
		for slit in range(2):
			rounded_box(f"tower_window_{index}_{slit}", (x, -1.04, 1.9 + slit * 1.2),
				(0.24, 0.08, 0.62), MATS["aqua"], r, radius=0.05)
	rounded_box("castle_door", (0, -1.34, 1.15), (1.2, 0.12, 2.1), MATS["wood"], r, radius=0.28)
	torus("door_shell_trim", (0, -1.43, 1.8), 0.72, 0.12, MATS["gold"], r, rotation=(math.pi * 0.5, 0, 0))
	for index in range(5):
		x = -width * 0.38 + index * width * 0.19
		cone(f"roof_finial_{index}", (x, 0, 4.35), 0.16, 0.0, 0.72, MATS["gold"], r, vertices=10)
	return r


def build_train_piece(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	kind = ("engine", "tender", "coach", "gondola", "caboose", "station")[variant % 6]
	if kind == "station":
		rounded_box("station_platform", (0, 0, 0.25), (5.4, 2.2, 0.45), MATS["slate"], r, radius=0.16)
		rounded_box("station_house", (0.5, 0.35, 1.8), (3.6, 1.5, 2.8), MATS["cream"], r, radius=0.2)
		panel_xz("station_roof", [(-2.4, 0), (0, 1.35), (2.4, 0)], 2.0,
			(0.5, 0.35, 3.15), MATS["lavender"], r)
		for index in range(3):
			rounded_box(f"station_window_{index}", (-0.7 + index * 1.0, -0.43, 1.9),
				(0.55, 0.08, 0.8), MATS["aqua"], r, radius=0.08)
		return r
	length = 3.5 if kind == "engine" else 3.0
	rounded_box(f"{kind}_body", (0, 0, 1.15), (length, 1.55, 1.45),
		[MATS["coral"], MATS["aqua"], MATS["lavender"]][variant % 3], r, radius=0.22)
	if kind == "engine":
		cylinder("engine_boiler", (-0.35, 0, 1.65), 0.65, 2.1, MATS["ocean"], r,
			rotation=(0, math.pi * 0.5, 0), vertices=16)
		cone("engine_stack", (0.2, 0, 2.65), 0.36, 0.22, 1.0, MATS["ink"], r, vertices=12)
	elif kind == "gondola":
		for side in (-1, 1):
			rounded_box(f"gondola_rail_{side}", (0, side * 0.72, 1.85), (2.9, 0.12, 0.18), MATS["gold"], r)
	else:
		for index in range(3):
			rounded_box(f"window_{index}", (-0.85 + index * 0.85, -0.79, 1.42), (0.5, 0.08, 0.55), MATS["cream"], r)
	for side in (-1, 1):
		for index in (-1, 1):
			torus(f"wheel_{side}_{index}", (index * length * 0.28, side * 0.83, 0.48), 0.38, 0.12,
				MATS["ink"], r, rotation=(math.pi * 0.5, 0, 0))
	return r


def build_snow_terrain(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	rng = random.Random(5500 + variant)
	for index in range(4):
		angle = math.tau * index / 4 + variant * 0.25
		radius = 0.45 + index * 0.38
		x, y = math.cos(angle) * radius, math.sin(angle) * radius
		scale = rng.uniform(0.75, 1.25)
		height = scale * (1.55 + (2 if index == 0 else 0) * 0.45)
		ico(f"crag_{index}", (x, y, height * 0.5), (scale * 0.68, scale * 0.62, height), MATS["slate"], r,
			5500 + variant * 10 + index)
		ico(f"snow_cap_{index}", (x, y, height * 0.86), (scale * 0.57, scale * 0.52, height * 0.22),
			MATS["snow"], r, 5600 + variant * 10 + index)
	ico("snow_foot", (0, 0, 0.15), (2.2, 1.85, 0.32), MATS["ice"], r, 5700 + variant)
	return r


def build_architecture(name: str, kind: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	if kind == "reef_hub":
		ico("hub_island", (0, 0, 0), (6.0, 5.2, 0.75), MATS["slate"], r, 6000)
		portal = build_shell_portal(name + "_portal", variant)
		portal.parent = r
		portal.location = (0, 2.0, 0.4)
		for index in range(5):
			angle = math.tau * index / 5
			tube(f"friend_marker_{index}", [(math.cos(angle) * 3.8, math.sin(angle) * 3.8, 0.35),
				(math.cos(angle) * 4.0, math.sin(angle) * 4.0, 1.6)], 0.18,
				[MATS["coral"], MATS["aqua"], MATS["lavender"], MATS["gold"], MATS["mint"]][index], r)
	elif kind == "sky_world":
		ico("floating_island", (0, 0, 0), (7.0, 5.5, 1.2), MATS["slate_light"], r, 6010)
		ico("snow_field", (0, 0, 0.75), (6.6, 5.1, 0.55), MATS["snow"], r, 6011)
		castle = build_castle(name + "_castle", variant, compact=True)
		castle.parent = r
		castle.location = (0, 0.8, 1.0)
		for index in range(4):
			cloud = build_cloud(name + f"_cloud_{index}", index)
			cloud.parent = r
			cloud.location = (-7 + index * 4.5, 4.0 - index, 2.0 + index * 0.5)
	elif kind == "rainbow_route":
		for index, color in enumerate(("coral", "orange", "gold", "mint", "aqua", "lavender")):
			offset = (index - 2.5) * 0.22
			tube(f"rainbow_lane_{index}", [(-5, offset, 0), (-2.5, offset, 1.2), (0, offset, 1.8),
				(2.5, offset, 1.2), (5, offset, 0)], 0.11, MATS[color], r)
		torus("destination_arch", (5.1, 0, 1.5), 1.5, 0.16, MATS["indigo"], r,
			rotation=(math.pi * 0.5, 0, 0))
	elif kind == "painting_display":
		for index in range(3):
			x = (index - 1) * 2.8
			rounded_box(f"frame_outer_{index}", (x, 0, 1.8), (2.3, 0.28, 3.0), MATS["gold"], r, radius=0.18)
			rounded_box(f"protected_art_window_{index}", (x, -0.18, 1.8), (1.82, 0.12, 2.48), MATS["ink"], r, radius=0.12)
			star_panel(f"frame_crest_{index}", 5, 0.35, 0.16, 0.12, (x, -0.2, 3.45), MATS["aqua"], r)
	elif kind == "hall":
		rounded_box("hall_floor", (0, 0, 0), (7.0, 5.0, 0.3), MATS["slate_light"], r, radius=0.12)
		for side in (-1, 1):
			for index in range(3):
				x = -4.2 + index * 4.2
				cylinder(f"hall_column_{side}_{index}", (x, side * 3.6, 2.2), 0.38, 4.2, MATS["cream"], r, vertices=16)
				torus(f"column_capital_{side}_{index}", (x, side * 3.6, 4.15), 0.58, 0.1, MATS["gold"], r)
		for side in (-1, 1):
			tube(f"ceiling_arch_{side}", [(side * 5.8, -3.4, 4.0), (side * 6.1, 0, 6.3),
				(side * 5.8, 3.4, 4.0)], 0.24, MATS["lavender"], r)
	elif kind == "wall_modules":
		for index in range(3):
			x = (index - 1) * 3.8
			rounded_box(f"wall_panel_{index}", (x, 0, 1.7), (3.2, 0.45, 3.4),
				MATS["cream"] if index != 1 else MATS["slate_light"], r, radius=0.2)
			torus(f"wall_arch_{index}", (x, -0.28, 2.0), 1.05, 0.16, MATS["gold"], r,
				rotation=(math.pi * 0.5, 0, 0))
			rounded_box(f"baseboard_{index}", (x, -0.28, 0.32), (3.3, 0.18, 0.34), MATS["lavender"], r)
	elif kind == "stairs":
		for flight in range(2):
			xoff = (flight - 0.5) * 4.5
			for step in range(8):
				rounded_box(f"step_{flight}_{step}", (xoff, step * 0.42 - 1.5, 0.2 + step * 0.25),
					(2.8, 0.48, 0.28), MATS["slate_light"], r, radius=0.08)
			for side in (-1, 1):
				tube(f"stair_rail_{flight}_{side}", [(xoff + side * 1.35, -1.7, 0.7),
					(xoff + side * 1.35, 1.6, 2.8)], 0.1, MATS["gold"], r)
	elif kind == "columns":
		for index in range(3):
			x = (index - 1) * 2.4
			cylinder(f"fluted_column_{index}", (x, 0, 2.1), 0.52, 3.7, MATS["cream"], r, vertices=18)
			torus(f"capital_ring_{index}", (x, 0, 3.9), 0.72, 0.12, MATS["gold"], r)
			torus(f"base_ring_{index}", (x, 0, 0.25), 0.68, 0.12, MATS["lavender"], r)
			for flute in range(8):
				angle = math.tau * flute / 8
				tube(f"flute_{index}_{flute}", [(x + math.cos(angle) * 0.48, math.sin(angle) * 0.48, 0.45),
					(x + math.cos(angle) * 0.48, math.sin(angle) * 0.48, 3.75)], 0.035, MATS["slate_light"], r)
	elif kind == "doors":
		for index in range(3):
			x = (index - 1) * 3.0
			rounded_box(f"door_{index}", (x, 0, 1.55), (2.1, 0.38, 3.1),
				[MATS["wood"], MATS["ocean"], MATS["lavender"]][index], r, radius=0.45)
			torus(f"door_frame_{index}", (x, -0.25, 2.1), 1.32, 0.16, MATS["gold"], r,
				rotation=(math.pi * 0.5, 0, 0))
			sphere(f"door_knob_{index}", (x + 0.65, -0.26, 1.45), (0.14, 0.1, 0.14), MATS["aqua"], r, 10, 6)
	elif kind == "throne_room":
		rounded_box("dais", (0, 0.5, 0.35), (5.5, 3.2, 0.6), MATS["slate_light"], r, radius=0.18)
		for side in (-1, 1):
			cylinder(f"canopy_column_{side}", (side * 2.2, 1.4, 2.8), 0.34, 4.8, MATS["cream"], r)
		tube("canopy_arch", [(-2.2, 1.4, 5.0), (0, 1.4, 6.2), (2.2, 1.4, 5.0)], 0.22, MATS["gold"], r)
		for index in range(5):
			star_panel(f"canopy_star_{index}", 5, 0.34, 0.15, 0.1, ((index - 2) * 0.7, 1.1, 5.15),
				MATS["aqua"] if index % 2 else MATS["rose"], r)
	elif kind == "butterfly_world":
		ico("garden_planet", (0, 0, 0), (5.8, 5.8, 5.8), MATS["aqua_light"], r, 6020, subdivisions=3)
		torus("garden_equator", (0, 0, 0), 5.88, 0.14, MATS["indigo"], r)
		torus("garden_path", (0, 0, 0), 5.62, 0.08, MATS["gold"], r)
		for index in range(7):
			angle = math.tau * index / 7
			ico(f"garden_patch_{index}", (math.cos(angle) * 4.8, math.sin(angle) * 4.8, 2.0 - index * 0.2),
				(1.6, 1.0, 0.35), [MATS["mint"], MATS["coral"], MATS["lavender"]][index % 3], r, 6030 + index)
			star_panel(f"garden_blossom_{index}", 5, 0.38, 0.17, 0.08,
				(math.cos(angle) * 4.95, math.sin(angle) * 4.95, 2.45 - index * 0.2),
				[MATS["gold"], MATS["coral"], MATS["aqua"]][index % 3], r, rotation=angle)
	elif kind == "gate_transition":
		for side in (-1, 1):
			gate = build_butterfly(name + f"_gate_{side}", variant + (0 if side < 0 else 1), gate=True)
			gate.parent = r
			gate.location = (side * 5.5, 0, 2.7)
		tube("transition_path_left", [(-4.0, 0, 0), (0, 0, 0.2), (4.0, 0, 0)], 0.25, MATS["aqua"], r)
	elif kind == "dungeon_arena":
		for ring in range(3):
			torus(f"arena_ring_{ring}", (0, 0, ring * 0.08), 3.0 + ring * 1.3, 0.24,
				[MATS["slate"], MATS["lavender"], MATS["aqua"]][ring], r)
		for index in range(12):
			angle = math.tau * index / 12
			ico(f"wall_shell_{index}", (math.cos(angle) * 6.1, math.sin(angle) * 6.1, 1.3),
				(1.1, 0.65, 1.6), MATS["slate_light"] if index % 2 else MATS["cream"], r, 6100 + index)
	elif kind == "dungeon_walls":
		for index in range(5):
			x = (index - 2) * 2.0
			ico(f"scallop_wall_{index}", (x, 0, 1.4), (1.25, 0.7, 1.55),
				MATS["slate"] if index % 2 else MATS["slate_light"], r, 6200 + index)
			cone(f"coral_buttress_{index}", (x, -0.65, 2.4), 0.42, 0.12, 2.4,
				MATS["aqua"] if index % 2 else MATS["coral"], r)
	elif kind == "puzzle_room":
		rounded_box("puzzle_floor", (0, 0, 0), (7, 5, 0.35), MATS["slate"], r, radius=0.12)
		for index in range(6):
			angle = math.tau * index / 6
			cylinder(f"puzzle_pad_{index}", (math.cos(angle) * 3.2, math.sin(angle) * 2.1, 0.35),
				0.72, 0.48, [MATS["aqua"], MATS["lavender"], MATS["coral"]][index % 3], r)
			star_panel(f"pad_symbol_{index}", 5 + index % 2, 0.42, 0.2, 0.08,
				(math.cos(angle) * 3.2, math.sin(angle) * 2.1 - 0.28, 0.72), MATS["cream"], r)
	elif kind == "kart_world":
		torus("track_outer", (0, 0, 0.1), 6.5, 0.8, MATS["slate"], r)
		torus("track_inner_mark", (0, 0, 0.35), 5.9, 0.08, MATS["aqua"], r)
		for side in (-1, 1):
			rounded_box(f"grandstand_{side}", (side * 7.8, 0, 2.0), (2.4, 6.5, 3.0),
				MATS["cream"], r, radius=0.25)
			for row in range(3):
				rounded_box(f"stand_seat_{side}_{row}", (side * 6.9, 0, 1.0 + row * 0.75),
					(0.35, 5.7 - row * 0.4, 0.28), [MATS["coral"], MATS["aqua"], MATS["lavender"]][row], r)
		rounded_box("pit_garage", (0, -8.1, 1.4), (7.0, 2.3, 2.5), MATS["slate_light"], r, radius=0.28)
	elif kind == "alpine_interior":
		rounded_box("room_floor", (0, 0, 0), (6.2, 5.0, 0.3), MATS["wood_light"], r, radius=0.12)
		rounded_box("hearth", (-2.0, 1.8, 1.2), (2.2, 1.1, 2.2), MATS["slate"], r, radius=0.24)
		rounded_box("bed_frame", (1.5, 1.3, 0.7), (3.0, 2.0, 0.55), MATS["wood"], r, radius=0.16)
		rounded_box("bed_blanket", (1.5, 1.15, 1.0), (2.7, 1.75, 0.28), MATS["lavender"], r, radius=0.18)
		for index in range(3):
			cylinder(f"stool_{index}", (-1.2 + index * 1.2, -1.5, 0.6), 0.48, 0.45, MATS["coral"], r)
	else:
		raise ValueError(kind)
	return r


def build_prop(name: str, kind: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	if kind == "throne":
		rounded_box("throne_seat", (0, 0, 1.0), (2.1, 1.7, 0.45), MATS["lavender"], r, radius=0.22)
		rounded_box("throne_back", (0, 0.55, 2.7), (2.4, 0.45, 3.5), MATS["cream"], r, radius=0.45)
		for side in (-1, 1):
			tube(f"throne_arm_{side}", [(side * 0.95, -0.5, 1.1), (side * 1.2, 0.1, 1.65),
				(side * 1.1, 0.6, 1.65)], 0.18, MATS["gold"], r)
		star_panel("throne_crest", 5, 0.7, 0.3, 0.14, (0, 0.25, 4.35), MATS["gold"], r)
	elif kind == "bed":
		rounded_box("bed_base", (0, 0, 0.55), (3.8, 2.4, 0.55), MATS["wood"], r, radius=0.2)
		rounded_box("mattress", (0, -0.05, 0.98), (3.55, 2.2, 0.35), MATS["cream"], r, radius=0.22)
		rounded_box("blanket", (-0.45, 0, 1.22), (2.4, 2.15, 0.22), MATS["lavender"], r, radius=0.18)
		rounded_box("headboard", (1.65, 0, 2.0), (0.35, 2.5, 2.4), MATS["coral"], r, radius=0.45)
		for side in (-1, 1):
			sphere(f"pillow_{side}", (0.95, side * 0.58, 1.35), (0.55, 0.45, 0.22), MATS["aqua_light"], r, 14, 8)
	elif kind == "kitchen_room":
		rounded_box("counter_run", (0, 1.5, 1.0), (5.5, 1.2, 1.8), MATS["aqua_light"], r, radius=0.18)
		rounded_box("counter_top", (0, 0.88, 1.92), (5.8, 1.5, 0.18), MATS["cream"], r, radius=0.08)
		for index in range(4):
			rounded_box(f"cabinet_door_{index}", (-2.0 + index * 1.3, 0.84, 1.05),
				(1.0, 0.08, 1.15), MATS["lavender"] if index % 2 else MATS["coral"], r, radius=0.1)
		for index in range(3):
			torus(f"hanging_pan_{index}", (-1.6 + index * 1.6, 1.0, 3.1), 0.42 + index * 0.08, 0.09,
				MATS["slate"], r, rotation=(math.pi * 0.5, 0, 0))
	elif kind == "stove":
		rounded_box("stove_body", (0, 0, 1.0), (2.2, 1.7, 2.0), MATS["cream"], r, radius=0.25)
		for x in (-0.55, 0.55):
			for y in (-0.42, 0.42):
				torus(f"burner_{x}_{y}", (x, y, 2.02), 0.32, 0.06, MATS["ink"], r)
		rounded_box("oven_window", (0, -0.88, 0.9), (1.45, 0.1, 0.85), MATS["ocean"], r, radius=0.14)
		for index in range(4):
			sphere(f"knob_{index}", (-0.72 + index * 0.48, -0.93, 1.65), (0.12, 0.06, 0.12), MATS["coral"], r, 10, 6)
	elif kind == "kettle" or kind == "teapot":
		body_mat = MATS["aqua"] if kind == "kettle" else MATS["lavender"]
		sphere("pot_body", (0, 0, 0.9), (1.0, 0.82, 0.82), body_mat, r, 20, 12)
		cone("spout", (1.05, 0, 1.15), 0.3, 0.14, 1.45, body_mat, r,
			rotation=(0, math.radians(62), 0), vertices=14)
		torus("handle", (-0.2, 0, 1.25), 1.0, 0.12, MATS["wood"], r, rotation=(math.pi * 0.5, 0, 0))
		cylinder("lid", (0, 0, 1.7), 0.55, 0.16, MATS["cream"], r)
		sphere("lid_knob", (0, 0, 1.92), (0.16, 0.16, 0.16), MATS["gold"], r, 10, 6)
	elif kind == "pans":
		for index in range(3):
			x = (index - 1) * 1.2
			torus(f"pan_rim_{index}", (x, 0, 0.35), 0.62 - index * 0.08, 0.1, MATS["slate"], r)
			cylinder(f"pan_base_{index}", (x, 0, 0.25), 0.55 - index * 0.08, 0.16, MATS["ink"], r)
			tube(f"pan_handle_{index}", [(x + 0.45, 0, 0.35), (x + 1.25, 0, 0.5)], 0.09, MATS["wood"], r)
	elif kind == "table":
		cylinder("table_top", (0, 0, 1.45), 1.85, 0.3, MATS["wood_light"], r, vertices=18)
		cylinder("table_pedestal", (0, 0, 0.75), 0.35, 1.35, MATS["wood"], r)
		for index in range(4):
			angle = math.tau * index / 4
			x, y = math.cos(angle) * 2.65, math.sin(angle) * 2.65
			cylinder(f"stool_seat_{index}", (x, y, 0.85), 0.62, 0.25,
				[MATS["coral"], MATS["aqua"], MATS["lavender"], MATS["gold"]][index], r)
			cylinder(f"stool_leg_{index}", (x, y, 0.4), 0.14, 0.8, MATS["wood"], r)
	elif kind == "pepper":
		for lobe in range(3):
			angle = math.tau * lobe / 3
			sphere(f"pepper_lobe_{lobe}", (math.cos(angle) * 0.17, math.sin(angle) * 0.17, 0),
				(0.38, 0.34, 0.72), MATS["red"], r, 16, 10)
		cone("pepper_tip", (0, 0, -0.72), 0.28, 0.025, 0.62, MATS["red"], r, vertices=12)
		star_panel("pepper_calyx", 5, 0.38, 0.12, 0.09, (0, 0, 0.66), MATS["leaf_dark"], r)
		tube("pepper_stem", [(0, 0, 0.65), (0.05, 0, 0.95), (0.2, 0, 1.08)], 0.07, MATS["leaf"], r)
	elif kind == "basket":
		cone("basket_body", (0, 0, 0.75), 1.25, 0.92, 1.5, MATS["wood_light"], r, vertices=18)
		for ring in range(5):
			torus(f"weave_ring_{ring}", (0, 0, 0.2 + ring * 0.3), 1.0 + ring * 0.04, 0.055, MATS["wood"], r)
		tube("basket_handle", [(-0.85, 0, 1.0), (-0.7, 0, 2.3), (0, 0, 2.8),
			(0.7, 0, 2.3), (0.85, 0, 1.0)], 0.11, MATS["wood"], r)
		for index in range(5):
			pepper = build_prop(name + f"_pepper_{index}", "pepper", index)
			pepper.parent = r
			pepper.location = ((index - 2) * 0.35, 0, 1.45 + (index % 2) * 0.2)
			pepper.scale = (0.5, 0.5, 0.5)
	elif kind == "puzzle_door":
		rounded_box("door_leaf", (0, 0, 1.8), (2.8, 0.45, 3.6), MATS["slate_light"], r, radius=0.55)
		torus("shell_frame", (0, -0.3, 2.2), 1.75, 0.2, MATS["gold"], r,
			rotation=(math.pi * 0.5, 0, 0))
		star_panel("star_lock", 5, 0.62, 0.28, 0.16, (0, -0.38, 1.8), MATS["aqua"], r)
	elif kind == "crystal_pad":
		cylinder("pad_base", (0, 0, 0.3), 1.25, 0.6, MATS["slate"], r, vertices=16)
		torus("pearl_rim", (0, 0, 0.62), 1.0, 0.12, MATS["cream"], r)
		ico("pad_crystal", (0, 0, 1.25), (0.48, 0.48, 0.85),
			[MATS["aqua"], MATS["lavender"], MATS["coral"]][variant % 3], r, 7000 + variant)
	elif kind == "crystal":
		ico("crystal_core", (0, 0, 0.8), (0.58, 0.52, 1.0),
			[MATS["aqua"], MATS["lavender"], MATS["rose"]][variant % 3], r, 7010 + variant)
		for index in range(4):
			angle = math.tau * index / 4
			cone(f"crystal_shard_{index}", (math.cos(angle) * 0.45, math.sin(angle) * 0.45, 0.35),
				0.22, 0.0, 0.75, MATS["cream"], r, rotation=(0.2, 0.2, angle), vertices=8)
	elif kind == "torch":
		cylinder("torch_stem", (0, 0, 1.1), 0.18, 2.2, MATS["wood"], r)
		cone("torch_cup", (0, 0, 2.18), 0.48, 0.28, 0.5, MATS["indigo"], r, vertices=12)
		torus("torch_rim", (0, 0, 2.42), 0.43, 0.08, MATS["gold"], r)
		for index in range(3):
			angle = math.tau * index / 3
			panel_xz(f"outer_flame_{index}", [(-0.34, 0), (-0.08, 0.68), (0.05, 1.42),
				(0.34, 0.42), (0.28, 0)], 0.12, (0, 0, 2.36), MATS["coral"], r,
				rotation=(0, 0, angle))
		panel_xz("inner_flame", [(-0.2, 0), (0, 0.92), (0.22, 0)], 0.16,
			(0, -0.08, 2.42), MATS["gold"], r)
		panel_xz("flame_core", [(-0.1, 0), (0, 0.52), (0.11, 0)], 0.17,
			(0, -0.18, 2.48), MATS["cream"], r)
	elif kind == "selection_pad":
		cylinder("pad", (0, 0, 0.25), 1.5, 0.5,
			[MATS["coral"], MATS["aqua"], MATS["lavender"]][variant % 3], r, vertices=20)
		torus("pad_rim", (0, 0, 0.5), 1.25, 0.12, MATS["cream"], r)
		star_panel("pad_icon", 5, 0.62, 0.28, 0.08, (0, -0.1, 0.62), MATS["ink"], r)
	elif kind == "barrier":
		for index in range(4):
			x = (index - 1.5) * 1.25
			rounded_box(f"barrier_segment_{index}", (x, 0, 0.65), (1.1, 0.55, 1.05),
				MATS["cream"] if index % 2 else MATS["coral"], r, radius=0.24)
			torus(f"barrier_shell_{index}", (x, -0.34, 0.72), 0.42, 0.07, MATS["aqua"], r,
				rotation=(math.pi * 0.5, 0, 0))
	elif kind == "gokart" or kind == "monster_truck":
		truck = kind == "monster_truck"
		rounded_box("vehicle_body", (0, 0, 0.95 if truck else 0.65),
			(3.4 if truck else 2.8, 1.75, 0.75), MATS["coral"] if truck else MATS["aqua"], r, radius=0.3)
		rounded_box("vehicle_cabin", (-0.25, 0, 1.55 if truck else 1.05),
			(1.55, 1.45, 1.0 if truck else 0.55), MATS["cream"], r, radius=0.28)
		wheel_radius = 0.72 if truck else 0.48
		for x in (-1.05, 1.05):
			for side in (-1, 1):
				torus(f"wheel_{x}_{side}", (x, side * 0.94, 0.45), wheel_radius, 0.2,
					MATS["ink"], r, rotation=(math.pi * 0.5, 0, 0))
				torus(f"hub_{x}_{side}", (x, side * 1.05, 0.45), wheel_radius * 0.35, 0.08,
					MATS["gold"], r, rotation=(math.pi * 0.5, 0, 0))
		if truck:
			tube("truck_rollbar", [(-0.8, -0.7, 1.5), (-0.55, -0.7, 2.5),
				(0.55, -0.7, 2.5), (0.8, -0.7, 1.5)], 0.1, MATS["indigo"], r)
	else:
		raise ValueError(kind)
	return r


def build_imp(name: str, variant: int = 0) -> bpy.types.Object:
	r = root_object(name)
	main = MATS["violet"] if variant % 2 == 0 else MATS["ocean"]
	sphere("imp_body", (0, 0, 0.9), (0.7, 0.55, 0.8), main, r, 16, 10)
	sphere("imp_head", (0.1, 0, 1.8), (0.65, 0.55, 0.58), main, r, 16, 10)
	for side in (-1, 1):
		panel_xz(f"fin_{side}", [(0, 0), (0.95, 0.5), (0.7, -0.55)], 0.1,
			(-0.25, side * 0.5, 1.1), MATS["aqua"], r)
		tube(f"arm_{side}", [(0, side * 0.4, 1.15), (0.55, side * 0.85, 0.85)], 0.11, main, r)
		tube(f"leg_{side}", [(-0.2, side * 0.3, 0.35), (-0.5, side * 0.6, -0.25)], 0.13, main, r)
		cone(f"horn_{side}", (0.0, side * 0.35, 2.35), 0.12, 0.0, 0.55, MATS["coral"], r,
			rotation=(side * 0.3, 0, 0), vertices=10)
		sphere(f"eye_{side}", (0.58, side * 0.34, 1.93), (0.1, 0.06, 0.12), MATS["cream"], r, 10, 6)
	return r


def build_dragon_turtle(name: str) -> bpy.types.Object:
	r = root_object(name)
	ico("shell", (0, 0, 1.0), (1.75, 1.45, 0.9), MATS["slate"], r, 8001, subdivisions=3)
	for ring in range(3):
		torus(f"shell_ring_{ring}", (0, 0, 1.0 + ring * 0.15), 1.0 + ring * 0.25, 0.1,
			[MATS["aqua"], MATS["lavender"], MATS["gold"]][ring], r)
	sphere("dragon_head", (2.0, 0, 1.1), (0.78, 0.62, 0.62), MATS["mint"], r, 18, 10)
	for side in (-1, 1):
		sphere(f"eye_{side}", (2.58, side * 0.38, 1.28), (0.12, 0.08, 0.12), MATS["ink"], r, 10, 6)
		for index, x in enumerate((-0.9, 0.9)):
			panel_xz(f"flipper_{side}_{index}", [(0, 0), (1.0, 0.42), (1.25, -0.45), (0.2, -0.55)], 0.16,
				(x, side * 1.15, 0.55), MATS["mint"], r,
				rotation=(side * math.radians(55), 0, 0))
	tube("tail", [(-1.4, 0, 0.9), (-2.0, 0, 0.65), (-2.65, 0, 0.85)], 0.22, MATS["mint"], r)
	for index in range(5):
		cone(f"shell_spine_{index}", (-0.9 + index * 0.45, 0, 2.0), 0.18, 0.0, 0.65,
			MATS["coral"], r, vertices=10)
	return r


def build_northern(name: str, variant: int) -> bpy.types.Object:
	kinds = ["castle", "dock"] + ["house"] * 6 + ["arch"] + ["peak"] * 2 + ["pine"] * 3 + ["mushroom"] * 2 + ["wisp"]
	kind = kinds[variant]
	if kind == "castle":
		r = root_object(name)
		castle = build_castle(name + "_ice_castle", 5, compact=False)
		castle.parent = r
		ico("castle_snow_island", (0, 0, -0.25), (5.6, 3.8, 0.65), MATS["ice"], r, 8180)
		for side in (-1, 1):
			tube(f"castle_winter_banner_{side}", [(side * 2.7, -1.45, 3.6), (side * 2.7, -1.45, 5.5)],
				0.08, MATS["indigo"], r)
			star_panel(f"castle_banner_star_{side}", 6, 0.42, 0.18, 0.08,
				(side * 2.7, -1.52, 4.7), MATS["ice"], r)
		return r
	r = root_object(name)
	if kind == "dock":
		for index in range(8):
			rounded_box(f"dock_plank_{index}", ((index - 3.5) * 0.72, 0, 0.5 + (index % 2) * 0.04),
				(0.62, 2.2, 0.22), MATS["wood_light"] if index % 2 else MATS["wood"], r, radius=0.08)
		for side in (-1, 1):
			for x in (-2.7, 0, 2.7):
				cylinder(f"dock_post_{side}_{x}", (x, side * 1.15, 1.05), 0.11, 1.35, MATS["wood"], r, vertices=10)
				sphere(f"dock_post_snow_{side}_{x}", (x, side * 1.15, 1.78), (0.2, 0.2, 0.12), MATS["snow"], r, 10, 6)
			tube(f"dock_rope_{side}_a", [(-2.7, side * 1.15, 1.4), (0, side * 1.15, 0.95),
				(2.7, side * 1.15, 1.4)], 0.06, MATS["cream"], r)
	elif kind == "house":
		index = variant - 2
		body_mat = [MATS["red"], MATS["orange"], MATS["aqua"], MATS["rose"], MATS["blue"], MATS["gold"]][index]
		widths = (3.2, 2.6, 4.2, 3.5, 3.8, 3.0)
		heights = (2.7, 3.5, 2.35, 2.75, 2.55, 2.9)
		width = widths[index]
		height = heights[index]
		depth = 2.65 + (index % 2) * 0.35
		if index == 5:
			cylinder("house_body", (0, 0, height * 0.5), width * 0.48, height, body_mat, r, vertices=16)
			cone("house_roof", (0, 0, height + 0.72), width * 0.68, 0.18, 1.6, MATS["ice"], r, vertices=16)
			cone("roof_snow", (0, 0, height + 0.86), width * 0.56, 0.1, 0.72, MATS["snow"], r, vertices=16)
		else:
			rounded_box("house_body", (0, 0, height * 0.5), (width, depth, height), body_mat, r, radius=0.32)
			roof_height = 1.55 + (index == 1) * 0.35
			panel_xz("house_roof", [(-width * 0.62, 0), (0, roof_height), (width * 0.62, 0)], depth + 0.42,
				(0, 0, height), MATS["indigo"] if index % 2 else MATS["ocean"], r)
			angle = math.atan2(roof_height, width * 0.62)
			for side in (-1, 1):
				rounded_box(f"roof_snow_{side}", (side * width * 0.28, 0, height + roof_height * 0.52),
					(width * 0.72, depth + 0.5, 0.16), MATS["snow"], r,
					rotation=(0, side * angle, 0), radius=0.08)
		rounded_box("house_door", (0, -depth * 0.51, 0.95), (0.86, 0.16, 1.75), MATS["wood"], r, radius=0.22)
		torus("door_trim", (0, -depth * 0.55, 1.35), 0.56, 0.08, MATS["cream"], r,
			rotation=(math.pi * 0.5, 0, 0))
		window_count = 3 if index in (2, 4) else 2
		for window in range(window_count):
			x = (window - (window_count - 1) * 0.5) * min(1.25, width / 3.0)
			if abs(x) < 0.3:
				continue
			rounded_box(f"window_trim_{window}", (x, -depth * 0.52, height * 0.6),
				(0.72, 0.14, 0.82), MATS["cream"], r, radius=0.12)
			rounded_box(f"window_glass_{window}", (x, -depth * 0.56, height * 0.6),
				(0.48, 0.08, 0.58), MATS["ice"], r, radius=0.08)
		if index in (0, 2, 4):
			rounded_box("chimney", (-width * 0.28, 0.2, height + 0.95), (0.45, 0.55, 1.5), MATS["wood"], r, radius=0.1)
			sphere("chimney_snow", (-width * 0.28, 0.2, height + 1.72), (0.34, 0.42, 0.14), MATS["snow"], r, 10, 6)
		if index == 3:
			rounded_box("market_awning", (0, -depth * 0.7, 1.9), (width * 0.78, 0.9, 0.18), MATS["gold"], r,
				rotation=(math.radians(12), 0, 0), radius=0.08)
	elif kind == "arch":
		for side in (-1, 1):
			ico(f"arch_pillar_{side}", (side * 1.8, 0, 1.6), (0.75, 0.7, 1.8), MATS["slate"], r, 8200 + side)
		tube("arch_curve", [(-1.8, 0, 3.1), (0, 0, 4.45), (1.8, 0, 3.1)], 0.38, MATS["slate_light"], r)
		star_panel("snowflake_crest", 6, 0.6, 0.22, 0.12, (0, -0.3, 3.75), MATS["ice"], r)
	elif kind == "peak":
		peak_index = variant - 9
		for crag in range(3):
			x = (crag - 1) * 0.9
			height = (3.6 if crag == 1 else 2.2 + crag * 0.25) + peak_index * 0.35
			ico(f"peak_crag_{crag}", (x, crag * 0.2, height * 0.5),
				(0.78 + crag * 0.08, 0.7, height), MATS["slate"], r, 8250 + variant * 4 + crag)
			ico(f"peak_snow_{crag}", (x, crag * 0.2, height * 0.84),
				(0.62, 0.56, height * 0.23), MATS["snow"], r, 8270 + variant * 4 + crag)
		ico("peak_foot", (0, 0, 0.12), (2.0, 1.5, 0.28), MATS["ice"], r, 8290 + variant)
	elif kind == "pine":
		index = variant - 11
		cylinder("pine_trunk", (0, 0, 1.9), 0.28, 3.8, MATS["wood"], r)
		for tier in range(4):
			cone(f"pine_tier_{tier}", (0, 0, 1.4 + tier * 1.0), 1.7 - tier * 0.25, 0.08, 1.6,
				MATS["leaf_dark"] if (tier + index) % 2 else MATS["leaf"], r, vertices=12)
			sphere(f"snow_tier_{tier}", (0, 0, 1.9 + tier * 1.0),
				(1.25 - tier * 0.18, 1.25 - tier * 0.18, 0.16), MATS["snow"], r, 12, 7)
	elif kind == "mushroom":
		for index in range(4):
			x = (index - 1.5) * 0.75
			y = (index % 2 - 0.5) * 0.38
			height = 0.72 + index % 3 * 0.22
			cylinder(f"stem_{index}", (x, y, height * 0.5), 0.14 + index * 0.015, height,
				MATS["cream"], r, rotation=(0, (index - 1.5) * 0.06, 0), vertices=12)
			cap_mat = MATS["rose"] if variant == 14 else MATS["gold"]
			cone(f"cap_{index}", (x, y, height + 0.16), 0.5 + index * 0.04, 0.12, 0.34, cap_mat, r, vertices=16)
			sphere(f"cap_snow_{index}", (x - 0.08, y, height + 0.38),
				(0.34 + index * 0.03, 0.3, 0.1), MATS["snow"], r, 12, 7)
	elif kind == "wisp":
		outer = [(-0.66, 0), (0.46, 0), (0.75, 0.72), (0.34, 1.25), (0.08, 2.65),
			(-0.22, 1.72), (-0.66, 1.15), (-0.8, 0.56)]
		panel_xz("wisp_outer", outer, 0.24, (0, 0, 0), MATS["indigo"], r)
		panel_xz("wisp_middle", [(-0.43, 0.12), (0.35, 0.12), (0.48, 0.72), (0.1, 2.05),
			(-0.18, 1.25), (-0.5, 0.68)], 0.26, (0, -0.08, 0.1), MATS["aqua"], r)
		panel_xz("wisp_inner", [(-0.22, 0.18), (0.2, 0.18), (0.28, 0.62), (0.0, 1.35), (-0.3, 0.58)],
			0.28, (0, -0.16, 0.26), MATS["lavender"], r)
		sphere("wisp_heart", (0, -0.24, 0.66), (0.25, 0.09, 0.34), MATS["cream"], r, 12, 8)
	return r


def build_symbol(name: str, variant: int) -> bpy.types.Object:
	r = root_object(name)
	points = 3 + variant % 6
	star_panel("symbol_face", points, 0.9, 0.45, 0.22, (0, 0, 0),
		[MATS["aqua"], MATS["coral"], MATS["lavender"], MATS["gold"]][variant % 4], r,
		rotation=variant * 0.11)
	torus("symbol_rim", (0, 0.12, 0), 1.15, 0.1, MATS["cream"], r, rotation=(math.pi * 0.5, 0, 0))
	for index in range(1 + variant % 3):
		sphere(f"symbol_pearl_{index}", ((index - (variant % 3) * 0.5) * 0.35, -0.18, 0),
			(0.12, 0.06, 0.12), MATS["ink"], r, 10, 6)
	return r


@dataclass(frozen=True)
class AssetSpec:
	name: str
	role_id: str
	kind: str
	variant: int = 0


SPECS: list[AssetSpec] = []


def add(role_id: str, kind: str, count: int = 1) -> None:
	for variant in range(count):
		suffix = f"_{variant + 1:02d}" if count > 1 else ""
		SPECS.append(AssetSpec(f"{role_id.lower()}_{kind}{suffix}", role_id, kind, variant))


add("R001_reef_hub_overall", "reef_hub")
add("R002_reef_portal_presentation", "shell_portal")
add("R003_reef_coral_mass_placement", "coral", 6)
add("R004_reef_kelp_cards", "kelp", 3)
add("R005_reef_seagrass_cards", "seagrass", 3)
add("R006_reef_rock_family", "rock", 4)
add("R009_reef_coral_flower_hybrid", "coral", 2)
add("R010_reef_clownfish_model", "clownfish")
add("R011_reef_octopus_model", "octopus")
add("R012_reef_shrimp_role", "shrimp")
add("R013_reef_jellyfish_role", "jellyfish")
add("R014_sky_lagoon_world_composition", "sky_world")
add("R015_sky_lagoon_main_castle", "sky_castle")
add("R016_sky_lagoon_castle_towers", "castle_tower", 3)
add("R017_sky_lagoon_cloud_family", "cloud", 3)
add("R018_sky_lagoon_rainbow_route", "rainbow_route")
add("R019_sky_lagoon_snow_terrain", "snow", 3)
add("R020_sky_lagoon_painting_displays", "painting_display")
add("R021_sky_lagoon_train_presentation", "train", 6)
add("R022_sky_lagoon_palm_repetition", "palm", 3)
add("R023_castle_castle_hall_overall", "hall")
add("R024_castle_wall_modules", "wall_modules")
add("R025_castle_stairs", "stairs")
add("R026_castle_columns", "columns")
add("R027_castle_doors", "doors")
add("R028_castle_throne_room_presentation", "throne_room")
add("R029_castle_throne_model", "throne")
add("R030_castle_bed_model", "bed")
add("R031_castle_kitchen_room", "kitchen_room")
add("R035_castle_kitchen_stove", "stove")
add("R036_castle_kitchen_kettle", "kettle")
add("R037_castle_kitchen_pans", "pans")
add("R038_castle_kitchen_teapot", "teapot")
add("R039_castle_kitchen_table_and_stools", "table")
add("R040_stars_dream_star", "star", 1)
add("R041_stars_crown_star", "star", 1)
add("R042_stars_star_chamber_focal", "star", 1)
add("R043_butterfly_world_world_overall", "butterfly_world")
add("R045_butterfly_world_home_gate", "butterfly_gate")
add("R046_butterfly_world_inter_world_gate", "butterfly_gate")
add("R047_butterfly_world_gate_transition_composition", "gate_transition")
add("R048_butterfly_world_butterfly_environment_family", "butterfly", 4)
add("R049_dungeon_combat_arena_overall", "dungeon_arena")
add("R051_dungeon_arena_walls", "dungeon_walls")
add("R052_dungeon_standard_enemies", "imp", 2)
add("R053_dungeon_boss", "dragon_turtle")
add("R054_dungeon_pepper_projectile", "pepper")
add("R055_dungeon_basket", "basket")
add("R056_dungeon_puzzle_room_overall", "puzzle_room")
add("R057_dungeon_puzzle_door", "puzzle_door")
add("R058_dungeon_crystal_pads", "crystal_pad", 3)
add("R059_dungeon_puzzle_crystals", "crystal", 3)
add("R060_dungeon_torch_family", "torch", 2)
add("R061_dungeon_shell_props", "shell", 3)
add("R062_dungeon_puzzle_symbols", "symbol", 11)
add("R063_kart_kart_world_overall", "kart_world")
add("R064_kart_vehicle_selection_pads", "selection_pad", 3)
add("R065_kart_track_barriers", "barrier", 3)
add("R068_kart_coral_dressing", "kart_coral", 3)
add("R069_kart_gokart_source", "gokart")
add("R070_kart_monster_truck_source", "monster_truck")
add("R085_development_alpine_interiors", "alpine_interior")
add("R086_development_northern_kingdom_additions", "northern", 17)
add("R087_development_undersea_additions", "undersea", 5)


def build(spec: AssetSpec) -> bpy.types.Object:
	kind = spec.kind
	if kind in {"coral", "kart_coral"}:
		return build_coral(spec.name, spec.variant, low=kind == "kart_coral")
	if kind in {"kelp", "seagrass", "palm"}:
		return build_vegetation(spec.name, kind, spec.variant)
	if kind == "rock":
		return build_rock_family(spec.name, spec.variant)
	if kind == "cloud":
		return build_cloud(spec.name, spec.variant)
	if kind == "clownfish":
		return build_fish(spec.name, spec.variant, clown=True)
	if kind == "octopus":
		return build_octopus(spec.name, spec.variant)
	if kind == "shrimp":
		return build_shrimp(spec.name, spec.variant)
	if kind == "jellyfish":
		return build_jellyfish(spec.name, spec.variant)
	if kind == "butterfly":
		return build_butterfly(spec.name, spec.variant, gate=False)
	if kind == "butterfly_gate":
		gate_variant = 1 if "inter_world" in spec.role_id else spec.variant
		return build_butterfly(spec.name, gate_variant, gate=True)
	if kind == "star":
		variant = {"R040_stars_dream_star": 0, "R041_stars_crown_star": 1,
			"R042_stars_star_chamber_focal": 2}[spec.role_id]
		return build_star(spec.name, variant)
	if kind == "shell_portal":
		return build_shell_portal(spec.name, spec.variant)
	if kind == "sky_castle":
		return build_castle(spec.name, spec.variant, compact=False)
	if kind == "castle_tower":
		return build_castle(spec.name, spec.variant, compact=True)
	if kind == "train":
		return build_train_piece(spec.name, spec.variant)
	if kind == "snow":
		return build_snow_terrain(spec.name, spec.variant)
	if kind in {"reef_hub", "sky_world", "rainbow_route", "painting_display", "hall", "wall_modules",
		"stairs", "columns", "doors", "throne_room", "butterfly_world", "gate_transition",
		"dungeon_arena", "dungeon_walls", "puzzle_room", "kart_world", "alpine_interior"}:
		return build_architecture(spec.name, kind, spec.variant)
	if kind in {"throne", "bed", "kitchen_room", "stove", "kettle", "pans", "teapot", "table",
		"pepper", "basket", "puzzle_door", "crystal_pad", "crystal", "torch", "selection_pad",
		"barrier", "gokart", "monster_truck"}:
		return build_prop(spec.name, kind, spec.variant)
	if kind == "imp":
		return build_imp(spec.name, spec.variant)
	if kind == "dragon_turtle":
		return build_dragon_turtle(spec.name)
	if kind == "northern":
		return build_northern(spec.name, spec.variant)
	if kind == "symbol":
		return build_symbol(spec.name, spec.variant)
	if kind == "shell":
		r = root_object(spec.name)
		for index in range(3):
			torus(f"shell_ridge_{index}", (0, 0, index * 0.18), 1.0 - index * 0.2, 0.13,
				[MATS["cream"], MATS["coral"], MATS["aqua"]][(index + spec.variant) % 3], r)
		cone("shell_spire", (0, 0, 0.8), 0.5, 0.08, 1.5, MATS["lavender"], r, vertices=14)
		return r
	if kind == "undersea":
		if spec.variant == 0:
			return build_coral(spec.name, 9)
		if spec.variant == 1:
			return build_vegetation(spec.name, "kelp", 6)
		if spec.variant == 2:
			return build_jellyfish(spec.name, 5)
		if spec.variant == 3:
			return build_fish(spec.name, 4, clown=False)
		r = root_object(spec.name)
		ico("urchin_body", (0, 0, 0.55), (0.72, 0.72, 0.72), MATS["violet"], r, 9000)
		for index in range(18):
			angle = math.tau * index / 18
			tilt = -0.7 + (index % 6) * 0.28
			start = (math.cos(angle) * 0.5, math.sin(angle) * 0.5, 0.55 + math.sin(tilt) * 0.4)
			end = (math.cos(angle) * 1.3, math.sin(angle) * 1.3, 0.55 + math.sin(tilt) * 1.0)
			tube(f"urchin_spine_{index}", [start, end], 0.045, MATS["lavender"], r)
		return r
	raise ValueError(kind)


def export_asset(spec: AssetSpec, obj: bpy.types.Object) -> dict[str, object]:
	lo, hi = bounds(obj)
	components = component_names(obj)
	bpy.ops.object.select_all(action="DESELECT")
	copies: list[bpy.types.Object] = []
	for member in family(obj):
		if member.type not in {"MESH", "CURVE"}:
			continue
		copy = member.copy()
		copy.data = member.data.copy()
		bpy.context.collection.objects.link(copy)
		copy.parent = None
		copy.matrix_world = member.matrix_world.copy()
		if copy.type == "CURVE":
			bpy.ops.object.select_all(action="DESELECT")
			copy.select_set(True)
			bpy.context.view_layer.objects.active = copy
			bpy.ops.object.convert(target="MESH")
			copy = bpy.context.active_object
		copies.append(copy)
	bpy.ops.object.select_all(action="DESELECT")
	for copy in copies:
		copy.select_set(True)
	bpy.context.view_layer.objects.active = copies[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = spec.name
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	vertices = len(merged.data.vertices)
	materials = len(merged.data.materials)
	path = MODEL_OUT / f"{spec.name}.glb"
	bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB", export_yup=True,
		use_selection=True, export_apply=True, export_materials="EXPORT", export_animations=False)
	bpy.data.objects.remove(merged, do_unlink=True)
	return {
		"name": spec.name,
		"role_id": spec.role_id,
		"kind": spec.kind,
		"variant": spec.variant,
		"path": path.relative_to(ROOT).as_posix(),
		"vertices": vertices,
		"triangles": triangles,
		"materials": materials,
		"bounds_min": [round(value, 4) for value in lo],
		"bounds_max": [round(value, 4) for value in hi],
		"components": components,
	}


with TARGET_LEDGER.open(newline="", encoding="utf-8") as handle:
	target_rows = list(csv.DictReader(handle))

expected_roles = {
	row["role_id"] for row in target_rows
	if row["disposition"].startswith("regenerate_") and row["target_kind"] in {"modeled_3d", "composition_kit"}
}
planned_roles = {spec.role_id for spec in SPECS}
missing_roles = sorted(expected_roles - planned_roles)
unexpected_roles = sorted(planned_roles - expected_roles)
if missing_roles or unexpected_roles:
	raise RuntimeError(f"Role plan mismatch; missing={missing_roles}, unexpected={unexpected_roles}")

manifest_assets: list[dict[str, object]] = []
roots: list[bpy.types.Object] = []
for spec in SPECS:
	asset = build(spec)
	roots.append(asset)
	entry = export_asset(spec, asset)
	manifest_assets.append(entry)
	print(f"FULL_REGEN|{spec.name}|tri={entry['triangles']}|mat={entry['materials']}")

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))

role_counts: dict[str, int] = {}
for entry in manifest_assets:
	role_id = str(entry["role_id"])
	role_counts[role_id] = role_counts.get(role_id, 0) + 1

manifest = {
	"pack": PACK.relative_to(ROOT).as_posix(),
	"generator": "tools/build_full_texture_regen.py",
	"blender_version": bpy.app.version_string,
	"asset_count": len(manifest_assets),
	"covered_role_count": len(role_counts),
	"role_asset_counts": dict(sorted(role_counts.items())),
	"assets": manifest_assets,
}
MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
(PACK / "model_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(f"FULL_REGEN|assets|{len(manifest_assets)}")
print(f"FULL_REGEN|roles|{len(role_counts)}")
print(f"FULL_REGEN|blend|{BLEND_OUT}")
