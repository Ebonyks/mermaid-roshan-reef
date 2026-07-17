#!/usr/bin/env python3
"""Build the game-wide pass-35 authored art families in Blender 4.4.

Run with:
  blender --background --python tools/build_art_pass35.py

Protected book, family, friend, character, and child-toy art is never read or
modified by this generator.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "blender"
QA_DIR = SOURCE_DIR / "qa_art_pass35"
BLEND_PATH = SOURCE_DIR / "art_pass35.blend"

for folder in (
	ROOT / "assets" / "art35" / "landmarks",
	ROOT / "assets" / "art35" / "reef",
	ROOT / "assets" / "art35" / "kart",
	ROOT / "assets" / "art35" / "northern",
	ROOT / "assets" / "art35" / "castle",
	ROOT / "assets" / "art35" / "arena",
	ROOT / "assets" / "art35" / "galaxy",
	ROOT / "assets" / "dungeon",
	ROOT / "assets" / "props" / "gen2",
	SOURCE_DIR,
	QA_DIR,
):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"ink": (0.10, 0.07, 0.22, 1.0),
	"pearl": (0.96, 0.92, 0.82, 1.0),
	"cloud": (0.93, 0.93, 0.98, 1.0),
	"cloud_shadow": (0.58, 0.67, 0.84, 1.0),
	"aqua": (0.27, 0.77, 0.78, 1.0),
	"aqua_light": (0.54, 0.91, 0.84, 1.0),
	"coral": (0.94, 0.38, 0.46, 1.0),
	"coral_light": (1.0, 0.64, 0.60, 1.0),
	"lavender": (0.66, 0.49, 0.84, 1.0),
	"violet": (0.38, 0.25, 0.60, 1.0),
	"gold": (0.96, 0.72, 0.22, 1.0),
	"leaf": (0.25, 0.62, 0.47, 1.0),
	"leaf_light": (0.50, 0.83, 0.56, 1.0),
	"stone": (0.42, 0.48, 0.64, 1.0),
	"stone_light": (0.63, 0.67, 0.80, 1.0),
	"stone_dark": (0.29, 0.31, 0.47, 1.0),
	"wood": (0.52, 0.28, 0.25, 1.0),
	"wood_light": (0.72, 0.43, 0.35, 1.0),
	"ice": (0.62, 0.85, 0.92, 1.0),
	"snow": (0.88, 0.91, 0.95, 1.0),
}


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("MR35_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.88
	bsdf.inputs["Metallic"].default_value = 0.0
	bsdf.inputs["Specular IOR Level"].default_value = 0.18
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root_object(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.data.materials.append(mat)
	return obj


def smooth(obj: bpy.types.Object) -> bpy.types.Object:
	if obj.type == "MESH":
		for polygon in obj.data.polygons:
			polygon.use_smooth = True
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
	modifier = obj.modifiers.new("storybook_rounding", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	apply_modifier(obj, modifier)
	return smooth(obj)


def cube(name, location, size, mat, parent, rotation=(0.0, 0.0, 0.0), radius=0.12):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = tuple(value * 0.5 for value in size)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(radius, min(size) * 0.18), 2)


def sphere(name, location, scale, mat, parent, segments=16, rings=10):
	bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def ico(name, location, scale, mat, parent, subdivisions=2, rotation=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def cylinder(name, location, radius, depth, mat, parent, rotation=(0.0, 0.0, 0.0), vertices=16):
	bpy.ops.mesh.primitive_cylinder_add(
		vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(radius * 0.1, depth * 0.08), 2)


def cone(name, location, radius1, radius2, depth, mat, parent, rotation=(0.0, 0.0, 0.0), vertices=16):
	bpy.ops.mesh.primitive_cone_add(
		vertices=vertices,
		radius1=radius1,
		radius2=radius2,
		depth=depth,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def torus(name, location, major, minor, mat, parent, rotation=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(
		major_radius=major,
		minor_radius=minor,
		major_segments=24,
		minor_segments=8,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def curve_tube(name, points, radius, mat, parent):
	curve = bpy.data.curves.new(name + "Curve", "CURVE")
	curve.dimensions = "3D"
	curve.resolution_u = 2
	curve.bevel_depth = radius
	curve.bevel_resolution = 2
	curve.resolution_u = 3
	spline = curve.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, coordinate in zip(spline.bezier_points, points):
		point.co = coordinate
		point.handle_left_type = "AUTO"
		point.handle_right_type = "AUTO"
	obj = bpy.data.objects.new(name, curve)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	assign(obj, mat)
	return obj


def prism_polygon(name, points, depth, mat, parent, location=(0.0, 0.0, 0.0)):
	count = len(points)
	verts = [(0.0, 0.0, -depth * 0.5), (0.0, 0.0, depth * 0.5)]
	verts += [(x, y, -depth * 0.5) for x, y in points]
	verts += [(x, y, depth * 0.5) for x, y in points]
	faces = []
	for index in range(count):
		next_index = (index + 1) % count
		faces.append((0, 2 + next_index, 2 + index))
		faces.append((1, 2 + count + index, 2 + count + next_index))
		faces.append((2 + index, 2 + next_index, 2 + count + next_index, 2 + count + index))
	mesh = bpy.data.meshes.new(name + "Mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, depth * 0.16, 2)


def star_points(radius=1.0, inner=0.48):
	return [
		(
			math.cos(-math.pi * 0.5 + index * math.pi / 5.0) * (radius if index % 2 == 0 else radius * inner),
			math.sin(-math.pi * 0.5 + index * math.pi / 5.0) * (radius if index % 2 == 0 else radius * inner),
		)
		for index in range(10)
	]


def blade(name, location, height, width, bend, mat, parent):
	levels = 5
	front = []
	for index in range(levels):
		t = index / float(levels - 1)
		center_x = bend * t * t
		half = width * (1.0 - t * 0.84) * 0.5
		front.append((center_x - half, 0.0, height * t))
		front.append((center_x + half, 0.0, height * t))
	verts = [(x, -0.025, z) for x, _y, z in front] + [(x, 0.025, z) for x, _y, z in front]
	faces = []
	for side in range(2):
		offset = side * len(front)
		for index in range(levels - 1):
			a = offset + index * 2
			quad = (a, a + 1, a + 3, a + 2)
			faces.append(quad if side else tuple(reversed(quad)))
	for index in range(levels - 1):
		for edge in (0, 1):
			a = index * 2 + edge
			b = (index + 1) * 2 + edge
			faces.append((a, b, b + len(front), a + len(front)))
	mesh = bpy.data.meshes.new(name + "Mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


ASSETS: dict[str, tuple[bpy.types.Object, Path]] = {}


def register(name: str, root: bpy.types.Object, relative_path: str) -> None:
	ASSETS[name] = (root, ROOT / relative_path)


def build_cloud(variant: int) -> bpy.types.Object:
	root = root_object(f"Cloud_{variant}")
	profiles = (
		((-1.05, 0.18, 0.0, 0.68), (-0.45, 0.48, 0.05, 0.82), (0.28, 0.58, 0.0, 0.95), (0.95, 0.24, 0.02, 0.72)),
		((-1.10, 0.10, 0.0, 0.62), (-0.55, 0.52, 0.02, 0.92), (0.18, 0.42, 0.0, 0.78), (0.82, 0.40, 0.04, 0.86), (1.25, 0.05, 0.0, 0.56)),
		((-1.15, 0.16, 0.0, 0.65), (-0.62, 0.36, 0.04, 0.80), (0.0, 0.68, 0.0, 1.0), (0.70, 0.34, 0.02, 0.78), (1.16, 0.10, 0.0, 0.58)),
	)[variant]
	for index, (x, z, y, radius) in enumerate(profiles):
		sphere(f"CloudLobe_{index}", (x, y, z), (radius, radius * 0.76, radius * 0.78), MATS["cloud"], root)
	for index, x in enumerate((-0.72, 0.0, 0.72)):
		sphere(f"SoftUnderside_{index}", (x, 0.03, -0.15), (0.76, 0.60, 0.30), MATS["cloud_shadow"], root)
	return root


def build_star(name: str, accent: str, crown: bool, chamber: bool) -> bpy.types.Object:
	root = root_object(name)
	points = star_points(1.0, 0.47 if not chamber else 0.55)
	vertical_prism("InkOutline", [(x * 1.10, y * 1.10) for x, y in points], 0.30, MATS["ink"], root, (0.0, 0.0, 0.0))
	vertical_prism("PaintedFace", points, 0.36, MATS[accent], root, (0.0, -0.08, 0.0))
	vertical_prism("PearlInset", [(x * 0.54, y * 0.54) for x, y in points], 0.22, MATS["pearl"], root, (0.0, -0.28, 0.0))
	for index, mat_name in enumerate(("aqua", "coral", "lavender", "gold", "aqua_light")):
		angle = -math.pi * 0.5 + index * math.tau / 5.0
		sphere(f"Pearl_{index}", (math.cos(angle) * 0.70, -0.34, math.sin(angle) * 0.70), (0.08, 0.08, 0.08), MATS[mat_name], root, 12, 8)
	if crown:
		crown_points = [(-0.62, 0.0), (-0.52, 0.58), (-0.18, 0.28), (0.0, 0.74), (0.18, 0.28), (0.52, 0.58), (0.62, 0.0)]
		vertical_prism("CrownInk", [(x * 0.60, y * 0.60 + 1.0) for x, y in crown_points], 0.34, MATS["ink"], root, (0.0, 0.0, 0.0))
		vertical_prism("CrownGold", [(x * 0.50, y * 0.50 + 1.02) for x, y in crown_points], 0.38, MATS["gold"], root, (0.0, -0.08, 0.0))
	if chamber:
		torus("OrbitRing", (0.0, 0.0, 0.0), 1.42, 0.035, MATS["aqua"], root, (math.pi * 0.5, 0.2, 0.0))
		sphere("MoonPearl", (1.34, 0.18, 0.18), (0.15, 0.15, 0.15), MATS["pearl"], root)
	return root


def build_butterfly_gate() -> bpy.types.Object:
	root = root_object("ButterflyGatePass35")
	torus("PortalFrame", (0.0, 0.0, 0.0), 0.82, 0.10, MATS["pearl"], root, (math.pi * 0.5, 0.0, 0.0))
	upper = [(0.05, -0.05), (0.20, 0.70), (0.74, 1.18), (1.40, 1.02), (1.62, 0.42), (1.26, -0.18), (0.55, -0.40)]
	lower = [(0.08, 0.04), (0.62, -0.08), (1.26, -0.38), (1.38, -0.92), (0.92, -1.28), (0.32, -1.04)]
	for side in (-1.0, 1.0):
		for label, source, mat_name, inset_name, y_offset in (
			("Upper", upper, "lavender" if side < 0 else "coral", "aqua", 0.18),
			("Lower", lower, "aqua" if side < 0 else "gold", "coral_light", -0.18),
		):
			points = [(x * side, y + y_offset) for x, y in source]
			wing = vertical_prism(f"{label}_{'L' if side < 0 else 'R'}_Ink", [(x * 1.06, y * 1.06) for x, y in points], 0.18, MATS["ink"], root, (0.0, 0.0, 0.0))
			wing["gate_wing"] = True
			vertical_prism(f"{label}_{'L' if side < 0 else 'R'}", points, 0.22, MATS[mat_name], root, (0.0, -0.08, 0.0))
			inset = [(x * 0.68, y * 0.68 + (0.16 if label == "Upper" else -0.10)) for x, y in points]
			vertical_prism(f"{label}Inset_{'L' if side < 0 else 'R'}", inset, 0.14, MATS[inset_name], root, (0.0, -0.23, 0.0))
	cylinder("Body", (0.0, 0.0, 0.28), 0.20, 1.22, MATS["ink"], root)
	sphere("Thorax", (0.0, 0.36, 0.28), (0.28, 0.28, 0.32), MATS["violet"], root)
	sphere("Head", (0.0, 0.82, 0.28), (0.24, 0.24, 0.24), MATS["aqua"], root)
	for side in (-1.0, 1.0):
		curve_tube(f"Antenna_{side}", [(0.08 * side, 0.95, 0.30), (0.28 * side, 1.30, 0.30), (0.45 * side, 1.38, 0.30)], 0.025, MATS["ink"], root)
	return root


def build_coral(index: int) -> bpy.types.Object:
	root = root_object(f"CoralPass35_{index}")
	ico("RootStone", (0.0, 0.0, 0.18), (0.72, 0.58, 0.30), MATS["stone_dark"], root, 2)
	colors = ("coral", "aqua", "lavender", "coral_light", "gold", "aqua_light", "violet")
	mat = MATS[colors[index % len(colors)]]
	if index == 5:
		# Fan coral: a single marine fan, not flowers mixed with coral.
		for branch in range(7):
			x = (branch - 3) * 0.18
			curve_tube(f"FanBranch_{branch}", [(0.0, 0.0, 0.28), (x * 0.55, 0.0, 0.95), (x, 0.0, 1.65 - abs(x) * 0.22)], 0.055, mat, root)
		for level in range(4):
			z = 0.70 + level * 0.28
			width = 0.55 + level * 0.18
			curve_tube(f"FanCross_{level}", [(-width, 0.0, z), (0.0, 0.0, z + 0.08), (width, 0.0, z)], 0.035, mat, root)
	else:
		count = 4 + index % 3
		for branch in range(count):
			angle = (branch / count) * math.tau + index * 0.31
			radius = 0.22 + (branch % 2) * 0.18
			height = 1.10 + 0.22 * ((branch + index) % 3)
			x = math.cos(angle) * radius
			y = math.sin(angle) * radius
			curve_tube(f"Branch_{branch}", [(0.0, 0.0, 0.24), (x * 0.65, y * 0.65, height * 0.62), (x, y, height)], 0.09 + 0.015 * (branch % 2), mat, root)
			sphere(f"RoundedTip_{branch}", (x, y, height), (0.13, 0.13, 0.16), MATS["pearl"] if index == 4 else mat, root, 12, 8)
	return root


def build_rock(index: int, large: bool = False) -> bpy.types.Object:
	root = root_object(f"ReefRockPass35_{index}{'_Large' if large else ''}")
	scale = 1.55 if large else 1.0
	profiles = (
		((0.0, 0.0, 0.48, 1.00, 0.78, 0.58), (-0.58, 0.12, 0.28, 0.52, 0.48, 0.34)),
		((0.0, 0.0, 0.60, 0.84, 0.72, 0.72), (0.54, -0.15, 0.27, 0.46, 0.52, 0.30)),
		((0.0, 0.0, 0.42, 1.18, 0.68, 0.52), (-0.44, -0.12, 0.30, 0.56, 0.44, 0.38)),
		((0.0, 0.0, 0.65, 0.72, 0.84, 0.76), (0.50, 0.14, 0.33, 0.52, 0.45, 0.40)),
		((0.0, 0.0, 0.48, 1.05, 0.90, 0.58), (0.0, -0.42, 0.24, 0.64, 0.44, 0.30)),
		((0.0, 0.0, 0.54, 0.92, 0.74, 0.64), (-0.52, 0.22, 0.30, 0.46, 0.52, 0.35)),
	)[index % 6]
	for piece, values in enumerate(profiles):
		x, y, z, sx, sy, sz = values
		ico(f"RoundedRock_{piece}", (x * scale, y * scale, z * scale), (sx * scale, sy * scale, sz * scale), MATS["stone"] if piece == 0 else MATS["stone_dark"], root, 2, (0.12 * piece, 0.18 * index, 0.08 * index))
	# Broad painted facet instead of noisy realistic texture.
	ico("AquaFacet", (0.18 * scale, -0.58 * scale, 0.58 * scale), (0.34 * scale, 0.06 * scale, 0.20 * scale), MATS["stone_light"], root, 1)
	return root


def build_plant(name: str, kelp: bool, variant: int) -> bpy.types.Object:
	root = root_object(name)
	ico("RootPebble", (0.0, 0.0, 0.10), (0.42, 0.34, 0.18), MATS["stone_dark"], root, 1)
	count = 5 if kelp else 7
	for index in range(count):
		angle = (index / count) * math.tau + variant * 0.42
		radius = 0.18 + 0.08 * (index % 2)
		height = (2.6 + 0.38 * (index % 3)) if kelp else (1.15 + 0.18 * (index % 4))
		width = (0.34 + 0.05 * (index % 2)) if kelp else (0.16 + 0.03 * (index % 3))
		blade_obj = blade(
			f"{'KelpRibbon' if kelp else 'GrassBlade'}_{index}",
			(math.cos(angle) * radius, math.sin(angle) * radius, 0.10),
			height,
			width,
			(0.34 if index % 2 == 0 else -0.28) + variant * 0.08,
			MATS["leaf"] if index % 3 else MATS["leaf_light"],
			root,
		)
		blade_obj.rotation_euler.z = angle
	return root


def build_kart_plinth() -> bpy.types.Object:
	root = root_object("KartShowcasePlinth")
	cylinder("Base", (0.0, 0.0, 0.18), 1.35, 0.36, MATS["violet"], root, vertices=24)
	cylinder("Inset", (0.0, 0.0, 0.38), 1.08, 0.10, MATS["aqua"], root, vertices=24)
	for index in range(8):
		angle = index * math.tau / 8.0
		sphere("Pearl_%d" % index, (math.cos(angle) * 1.12, math.sin(angle) * 1.12, 0.46), (0.07, 0.07, 0.07), MATS["pearl"], root, 10, 6)
	return root


def build_finish_arch() -> bpy.types.Object:
	root = root_object("KartFinishArch")
	for side in (-1.0, 1.0):
		cylinder(f"Post_{side}", (side * 2.6, 0.0, 1.65), 0.22, 3.3, MATS["ink"], root)
		for level in range(4):
			cube(f"PostBand_{side}_{level}", (side * 2.6, -0.02, 0.55 + level * 0.75), (0.54, 0.42, 0.24), MATS["pearl"] if level % 2 == 0 else MATS["lavender"], root, radius=0.08)
	cube("Banner", (0.0, 0.0, 3.35), (5.7, 0.34, 0.82), MATS["pearl"], root, radius=0.16)
	for index in range(8):
		cube(f"Check_{index}", (-2.15 + index * 0.62, -0.20, 3.35), (0.52, 0.08, 0.52), MATS["violet"] if index % 2 else MATS["aqua"], root, radius=0.04)
	return root


def build_barrier() -> bpy.types.Object:
	root = root_object("KartSoftBarrier")
	for index in range(4):
		x = -1.05 + index * 0.70
		sphere(f"Cushion_{index}", (x, 0.0, 0.35), (0.42, 0.52, 0.35), MATS["coral"] if index % 2 else MATS["aqua"], root, 12, 8)
	cube("Foot", (0.0, 0.0, 0.08), (3.2, 0.78, 0.16), MATS["ink"], root, radius=0.06)
	return root


def build_northern_castle() -> bpy.types.Object:
	root = root_object("NorthernToyCastle")
	cube("Hall", (0.0, 0.0, 1.35), (5.8, 2.8, 2.7), MATS["stone_light"], root, radius=0.20)
	for side in (-1.0, 1.0):
		cylinder(f"Tower_{side}", (side * 3.0, 0.0, 1.70), 1.05, 3.4, MATS["stone"], root, vertices=16)
		cone(f"SnowRoof_{side}", (side * 3.0, 0.0, 4.05), 1.45, 0.12, 1.70, MATS["snow"], root, vertices=16)
		cone(f"Roof_{side}", (side * 3.0, 0.0, 3.88), 1.28, 0.10, 1.58, MATS["violet"], root, vertices=16)
		for level in range(3):
			cube(f"Window_{side}_{level}", (side * 3.0, -1.01, 1.10 + level * 0.78), (0.42, 0.08, 0.52), MATS["aqua"], root, radius=0.10)
	# Deep framed doorway and roof resolve the open-box silhouette in the old build.
	torus("DoorFrame", (0.0, -1.43, 1.15), 0.82, 0.14, MATS["ink"], root, (math.pi * 0.5, 0.0, 0.0))
	cube("Door", (0.0, -1.46, 0.86), (1.36, 0.10, 1.72), MATS["wood"], root, radius=0.18)
	cone("HallRoof", (0.0, 0.0, 3.72), 3.55, 0.16, 1.62, MATS["violet"], root, vertices=4, rotation=(0.0, 0.0, math.pi * 0.25))
	for index in range(5):
		cube(f"SnowCap_{index}", (-2.2 + index * 1.1, 0.0, 3.10), (0.92, 3.05, 0.20), MATS["snow"], root, radius=0.08)
	return root


def gable_roof(name: str, location, width: float, depth: float, wall_z: float, ridge_z: float, mat, parent) -> bpy.types.Object:
	verts = [
		(-width * 0.5, -depth * 0.5, wall_z), (width * 0.5, -depth * 0.5, wall_z),
		(-width * 0.5, depth * 0.5, wall_z), (width * 0.5, depth * 0.5, wall_z),
		(0.0, -depth * 0.5, ridge_z), (0.0, depth * 0.5, ridge_z),
	]
	faces = [(0, 1, 4), (2, 5, 3), (0, 4, 5, 2), (1, 3, 5, 4), (0, 2, 3, 1)]
	mesh = bpy.data.meshes.new(name + "Mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.parent = parent
	assign(obj, mat)
	return obj


def build_northern_house(variant: int) -> bpy.types.Object:
	root = root_object(f"NorthernHousePass35_{variant}")
	body_mats = (MATS["coral"], MATS["aqua"], MATS["lavender"])
	roof_mats = (MATS["violet"], MATS["stone_dark"], MATS["ink"])
	cube("HouseBody", (0.0, 0.0, 1.65), (4.8, 4.0, 3.3), body_mats[variant], root, radius=0.18)
	# One closed gable replaces the two floating roof cards.
	gable_roof("GableRoof", (0.0, 0.0, 0.0), 5.6, 4.7, 3.22, 5.05, roof_mats[variant], root)
	gable_roof("SnowCap", (0.0, 0.0, 0.10), 5.75, 4.82, 3.43, 5.18, MATS["snow"], root)
	cube("FrontDoor", (0.0, -2.03, 1.16), (1.12, 0.16, 2.18), MATS["wood"], root, radius=0.12)
	for side in (-1.0, 1.0):
		cube(f"FrontWindow_{side}", (side * 1.48, -2.04, 2.15), (0.82, 0.14, 0.86), MATS["aqua_light"], root, radius=0.10)
		cube(f"CornerTrim_{side}", (side * 2.30, -2.06, 1.70), (0.18, 0.13, 3.1), MATS["pearl"], root, radius=0.04)
	cube("DoorStep", (0.0, -2.38, 0.16), (1.72, 0.72, 0.30), MATS["stone"], root, radius=0.08)
	cube("Chimney", (1.55, 0.70, 4.65), (0.52, 0.62, 1.82), MATS["stone_dark"], root, radius=0.08)
	cube("ChimneySnow", (1.55, 0.70, 5.58), (0.68, 0.78, 0.18), MATS["snow"], root, radius=0.06)
	return root


def build_northern_mountain() -> bpy.types.Object:
	root = root_object("NorthernMountainPass35")
	# Interlocking faceted masses read as one mountain without the old volcano cone.
	ico("PeakCore", (0.0, 0.0, 2.75), (2.55, 2.15, 2.75), MATS["stone"], root, 2)
	ico("PeakLeft", (-1.55, 0.10, 1.78), (1.65, 1.52, 1.82), MATS["stone_dark"], root, 2, (0.1, 0.3, 0.0))
	ico("PeakRight", (1.50, -0.08, 1.55), (1.48, 1.40, 1.58), MATS["stone_light"], root, 2, (-0.1, -0.2, 0.0))
	# Separate snow facets sit on the upper masses rather than forming a white ring.
	ico("SnowCore", (0.0, -0.03, 4.20), (1.55, 1.34, 1.20), MATS["snow"], root, 2)
	ico("SnowLeft", (-1.48, 0.02, 2.63), (0.82, 0.76, 0.62), MATS["snow"], root, 1)
	return root


def build_northern_gate() -> bpy.types.Object:
	root = root_object("NorthernPassGate35")
	for side in (-1.0, 1.0):
		cube(f"StonePost_{side}", (side * 2.30, 0.0, 2.30), (1.30, 1.45, 4.60), MATS["stone"], root, radius=0.22)
		ico(f"PostSnow_{side}", (side * 2.30, 0.0, 4.75), (0.90, 0.82, 0.42), MATS["snow"], root, 1)
	cube("Lintel", (0.0, 0.0, 4.75), (5.9, 1.48, 1.18), MATS["stone_light"], root, radius=0.20)
	vertical_prism("SnowflakeInk", star_points(0.72, 0.35), 0.16, MATS["ink"], root, (0.0, -0.84, 4.80))
	vertical_prism("Snowflake", star_points(0.62, 0.35), 0.18, MATS["ice"], root, (0.0, -0.94, 4.82))
	return root


def build_kettle() -> bpy.types.Object:
	root = root_object("KitchenKettlePass35")
	sphere("Body", (0.0, 0.0, 0.60), (0.66, 0.58, 0.62), MATS["aqua"], root)
	cone("Spout", (-0.74, 0.0, 0.76), 0.24, 0.11, 0.82, MATS["aqua_light"], root, (0.0, math.pi * 0.5, 0.0))
	torus("Handle", (0.0, 0.0, 0.92), 0.58, 0.07, MATS["ink"], root, (math.pi * 0.5, 0.0, 0.0))
	cylinder("Lid", (0.0, 0.0, 1.19), 0.31, 0.10, MATS["gold"], root)
	sphere("Knob", (0.0, 0.0, 1.30), (0.10, 0.10, 0.10), MATS["coral"], root, 12, 8)
	return root


def build_teapot() -> bpy.types.Object:
	root = root_object("KitchenTeapotPass35")
	sphere("Body", (0.0, 0.0, 0.56), (0.72, 0.64, 0.58), MATS["coral_light"], root)
	cone("Spout", (-0.82, 0.0, 0.72), 0.30, 0.10, 0.96, MATS["coral"], root, (0.0, math.pi * 0.5, 0.0))
	torus("Handle", (0.58, 0.0, 0.72), 0.48, 0.08, MATS["ink"], root, (math.pi * 0.5, 0.0, 0.0))
	cylinder("Lid", (0.0, 0.0, 1.10), 0.34, 0.10, MATS["lavender"], root)
	sphere("Knob", (0.0, 0.0, 1.22), (0.11, 0.11, 0.11), MATS["gold"], root, 12, 8)
	return root


def build_pan_set() -> bpy.types.Object:
	root = root_object("KitchenPanSetPass35")
	for index, offset in enumerate((-0.48, 0.48)):
		cylinder(f"Pan_{index}", (offset, 0.0, 0.12), 0.42 + index * 0.06, 0.16, MATS["violet"] if index else MATS["aqua"], root)
		cube(f"Handle_{index}", (offset + (0.70 if index else -0.70), 0.0, 0.18), (0.82, 0.18, 0.16), MATS["ink"], root, radius=0.07)
	return root


def build_soup_pot() -> bpy.types.Object:
	root = root_object("KitchenSoupPotPass35")
	cylinder("PotBody", (0.0, 0.0, 0.48), 0.74, 0.88, MATS["coral"], root, vertices=20)
	torus("PotRim", (0.0, 0.0, 0.94), 0.69, 0.07, MATS["gold"], root)
	cylinder("Soup", (0.0, 0.0, 0.94), 0.64, 0.06, MATS["leaf_light"], root, vertices=20)
	for side in (-1.0, 1.0):
		torus(f"Handle_{side}", (side * 0.76, 0.0, 0.62), 0.24, 0.06, MATS["ink"], root, (math.pi * 0.5, 0.0, 0.0))
	return root


def build_table_set() -> bpy.types.Object:
	root = root_object("KitchenTableSetPass35")
	cylinder("TableTop", (0.0, 0.0, 1.28), 1.34, 0.22, MATS["wood_light"], root, vertices=24)
	cylinder("TableStem", (0.0, 0.0, 0.66), 0.24, 1.20, MATS["wood"], root)
	cylinder("TableFoot", (0.0, 0.0, 0.12), 0.72, 0.20, MATS["wood"], root, vertices=20)
	for index in range(3):
		angle = index * math.tau / 3.0
		x, y = math.cos(angle) * 2.05, math.sin(angle) * 2.05
		cylinder(f"StoolSeat_{index}", (x, y, 0.75), 0.50, 0.20, MATS["lavender"] if index % 2 else MATS["aqua"], root, vertices=20)
		cylinder(f"StoolStem_{index}", (x, y, 0.38), 0.14, 0.70, MATS["wood"], root)
	return root


def build_music_rail() -> bpy.types.Object:
	root = root_object("CastleMusicRailPass35")
	for side in (-1.0, 1.0):
		cube(f"Rail_{side}", (side * 4.1, 0.0, 0.50), (0.82, 32.0, 1.0), MATS["wood"], root, radius=0.18)
	for y in (-14.0, -7.0, 0.0, 7.0, 14.0):
		cube(f"Brace_{y}", (0.0, y, 0.30), (8.8, 0.62, 0.55), MATS["ink"], root, radius=0.14)
	return root


def build_music_bar(index: int) -> bpy.types.Object:
	root = root_object(f"CastleMusicBarPass35_{index}")
	colors = ("coral", "coral_light", "gold", "leaf_light", "aqua", "lavender", "violet")
	width = 8.4 - index * 0.55
	cube("InkKey", (0.0, 0.0, 0.52), (width + 0.22, 2.92, 1.05), MATS["ink"], root, radius=0.28)
	cube("PaintedKey", (0.0, -0.04, 0.66), (width, 2.70, 0.88), MATS[colors[index]], root, radius=0.24)
	for side in (-1.0, 1.0):
		x = side * (width * 0.5 - 0.48)
		cylinder(f"PearlPin_{side}", (x, -0.04, 1.12), 0.16, 0.10, MATS["pearl"], root, vertices=12)
	return root


def build_song_star() -> bpy.types.Object:
	root = root_object("CastleSongStarPass35")
	cylinder("PedestalFoot", (0.0, 0.0, 0.18), 1.42, 0.36, MATS["violet"], root, vertices=24)
	cylinder("PedestalStem", (0.0, 0.0, 1.20), 0.34, 1.90, MATS["gold"], root, vertices=16)
	vertical_prism("StarInk", [(x * 1.48, y * 1.48) for x, y in star_points()], 0.30, MATS["ink"], root, (0.0, -0.02, 3.10))
	vertical_prism("StarFace", [(x * 1.30, y * 1.30) for x, y in star_points()], 0.36, MATS["gold"], root, (0.0, -0.10, 3.12))
	for side in (-1.0, 1.0):
		curve_tube(f"MusicCurl_{side}", [(side * 0.25, 0.0, 2.60), (side * 1.20, 0.0, 3.15), (side * 1.55, 0.0, 3.95)], 0.065, MATS["aqua"], root)
	return root


def build_music_wall_panel() -> bpy.types.Object:
	root = root_object("CastleMusicWallPanelPass35")
	cube("FrameInk", (0.0, 0.0, 4.0), (12.4, 0.72, 8.2), MATS["ink"], root, radius=0.28)
	cube("Panel", (0.0, -0.20, 4.0), (11.8, 0.38, 7.6), MATS["violet"], root, radius=0.22)
	for line in range(5):
		z = 2.20 + float(line) * 0.90
		cube(f"Staff_{line}", (0.0, -0.48, z), (10.5, 0.14, 0.12), MATS["aqua_light"], root, radius=0.04)
	notes = [(-4.0, 2.65, "coral"), (-2.0, 4.45, "gold"), (0.0, 3.55, "aqua"), (2.1, 5.35, "coral_light"), (4.1, 4.00, "leaf_light")]
	for index, (x, z, mat_name) in enumerate(notes):
		sphere(f"NoteHead_{index}", (x, -0.62, z), (0.48, 0.22, 0.38), MATS[mat_name], root, 12, 8)
		cube(f"NoteStem_{index}", (x + 0.40, -0.58, z + 0.72), (0.12, 0.16, 1.55), MATS[mat_name], root, radius=0.04)
	return root


def build_royal_bed(accent: str = "aqua") -> bpy.types.Object:
	root = root_object(f"RoyalBedPass35_{accent}")
	cube("BedFrame", (0.0, 0.0, 0.90), (7.0, 12.0, 1.35), MATS["wood"], root, radius=0.28)
	cube("Mattress", (0.0, 0.0, 1.78), (6.35, 11.3, 1.10), MATS["pearl"], root, radius=0.34)
	cube("Blanket", (0.0, 1.45, 2.43), (6.48, 6.75, 0.46), MATS[accent], root, radius=0.22)
	cube("Pillow", (0.0, -4.15, 2.55), (5.25, 2.20, 0.70), MATS["cloud"], root, radius=0.34)
	cube("HeadboardInk", (0.0, -5.78, 3.30), (7.35, 0.72, 6.10), MATS["ink"], root, radius=0.28)
	for side in (-1.0, 1.0):
		cylinder(f"HeadPost_{side}", (side * 3.18, -5.78, 3.65), 0.30, 6.70, MATS["wood_light"], root, vertices=16)
		sphere(f"PostPearl_{side}", (side * 3.18, -5.78, 7.05), (0.45, 0.45, 0.45), MATS["gold"], root, 12, 8)
	curve_tube("HeadboardCrown", [(-2.8, -5.84, 5.35), (-1.35, -5.84, 6.55), (0.0, -5.84, 6.05), (1.35, -5.84, 6.55), (2.8, -5.84, 5.35)], 0.24, MATS["gold"], root)
	return root


def build_nightstand() -> bpy.types.Object:
	root = root_object("RoyalNightstandPass35")
	cube("CabinetInk", (0.0, 0.0, 1.55), (2.65, 2.65, 3.10), MATS["ink"], root, radius=0.24)
	cube("Cabinet", (0.0, -0.04, 1.62), (2.34, 2.34, 2.82), MATS["wood_light"], root, radius=0.20)
	sphere("DrawerPull", (0.0, -1.22, 1.80), (0.15, 0.12, 0.15), MATS["gold"], root, 10, 6)
	cylinder("LampStem", (0.0, 0.0, 3.80), 0.16, 1.65, MATS["gold"], root, vertices=12)
	cone("LampShadeInk", (0.0, 0.0, 4.85), 0.92, 0.45, 1.42, MATS["ink"], root, vertices=20)
	cone("LampShade", (0.0, -0.02, 4.90), 0.78, 0.37, 1.22, MATS["coral_light"], root, vertices=20)
	return root


def build_bookcase() -> bpy.types.Object:
	root = root_object("RoyalBookcasePass35")
	cube("CabinetInk", (0.0, 0.0, 5.0), (8.8, 1.70, 10.2), MATS["ink"], root, radius=0.24)
	cube("CabinetBack", (0.0, 0.06, 5.0), (8.35, 1.25, 9.75), MATS["wood"], root, radius=0.18)
	book_mats = (MATS["coral"], MATS["aqua"], MATS["gold"], MATS["leaf_light"], MATS["lavender"], MATS["coral_light"])
	for row in range(3):
		z = 1.45 + row * 3.05
		cube(f"Shelf_{row}", (0.0, -0.82, z - 0.55), (8.25, 1.38, 0.28), MATS["gold"], root, radius=0.08)
		for index in range(8):
			width = 0.56 + 0.12 * ((index + row) % 3)
			height = 1.62 + 0.18 * ((index * 2 + row) % 4)
			x = -3.45 + index * 0.98
			cube(f"Book_{row}_{index}", (x, -0.92, z + height * 0.5), (width, 0.68, height), book_mats[(index + row * 2) % len(book_mats)], root, rotation=(0.0, 0.0, 0.04 * ((index % 3) - 1)), radius=0.08)
	cube("CrownRail", (0.0, -0.12, 9.85), (9.0, 1.82, 0.55), MATS["wood_light"], root, radius=0.14)
	return root


def build_winter_tree(variant: int) -> bpy.types.Object:
	root = root_object(f"WinterTreePass35_{variant}")
	cylinder("Trunk", (0.0, 0.0, 2.0), 0.62, 4.0, MATS["wood"], root, vertices=14)
	for level in range(4):
		z = 3.0 + level * 1.65
		radius = 3.15 - level * 0.55 + variant * 0.10
		ico(f"NeedleCrown_{level}", (0.0, 0.0, z), (radius, radius * 0.88, 1.62), MATS["leaf"] if level % 2 == 0 else MATS["leaf_light"], root, 2)
		ico(f"SnowCap_{level}", (-0.18, -0.05, z + 0.88), (radius * 0.82, radius * 0.72, 0.46), MATS["snow"], root, 2)
	return root


def build_lily_cluster() -> bpy.types.Object:
	root = root_object("FairyLilyClusterPass35")
	for index, (x, y, radius) in enumerate(((-1.35, 0.2, 1.30), (0.45, -0.45, 1.55), (1.55, 0.75, 0.92))):
		cylinder(f"Pad_{index}", (x, y, 0.12), radius, 0.22, MATS["leaf" if index % 2 else "leaf_light"], root, vertices=20)
		prism_polygon(f"PadInset_{index}", star_points(radius * 0.42, 0.78), 0.10, MATS["aqua_light"], root, (x, y, 0.28))
	if True:
		for petal in range(6):
			angle = petal * math.tau / 6.0
			sphere(f"Petal_{petal}", (0.45 + math.cos(angle) * 0.48, -0.45 + math.sin(angle) * 0.48, 0.58), (0.38, 0.22, 0.14), MATS["coral_light"], root, 12, 8)
		sphere("FlowerHeart", (0.45, -0.45, 0.62), (0.24, 0.24, 0.18), MATS["gold"], root, 12, 8)
	return root


def build_fairy_ring() -> bpy.types.Object:
	root = root_object("FairyFlowerGatePass35")
	torus("InkArch", (0.0, 0.0, 3.40), 3.55, 0.34, MATS["ink"], root, (math.pi * 0.5, 0.0, 0.0))
	torus("PaintedArch", (0.0, -0.08, 3.40), 3.52, 0.23, MATS["aqua"], root, (math.pi * 0.5, 0.0, 0.0))
	for index in range(7):
		angle = math.pi * 0.16 + index * math.pi * 0.68 / 6.0
		x = math.cos(angle) * 3.55
		z = 3.40 + math.sin(angle) * 3.55
		for petal in range(5):
			pa = petal * math.tau / 5.0
			sphere(f"Flower_{index}_{petal}", (x + math.cos(pa) * 0.34, -0.18, z + math.sin(pa) * 0.34), (0.26, 0.16, 0.18), MATS["coral_light"] if index % 2 else MATS["lavender"], root, 10, 6)
		sphere(f"FlowerHeart_{index}", (x, -0.25, z), (0.19, 0.12, 0.19), MATS["gold"], root, 10, 6)
	return root


def build_shadow_beetle() -> bpy.types.Object:
	root = root_object("FairyShadowBeetlePass35")
	ico("Abdomen", (0.0, 0.0, 0.70), (1.15, 0.78, 0.72), MATS["violet"], root, 2)
	sphere("Thorax", (0.0, -0.78, 0.72), (0.72, 0.62, 0.58), MATS["ink"], root, 14, 8)
	sphere("Head", (0.0, -1.34, 0.72), (0.48, 0.42, 0.42), MATS["stone_dark"], root, 14, 8)
	for side in (-1.0, 1.0):
		for pair in range(3):
			y = -0.65 + pair * 0.65
			curve_tube(f"Leg_{side}_{pair}", [(side * 0.42, y, 0.65), (side * 1.05, y - 0.12, 0.35), (side * 1.42, y + 0.18, 0.12)], 0.10, MATS["ink"], root)
		curve_tube(f"Antenna_{side}", [(side * 0.18, -1.62, 0.88), (side * 0.50, -1.98, 1.05), (side * 0.78, -2.08, 1.28)], 0.06, MATS["ink"], root)
	for index in (-1, 1):
		sphere(f"GlowSpot_{index}", (index * 0.42, -0.15, 1.24), (0.18, 0.12, 0.12), MATS["coral"], root, 10, 6)
	return root


def build_wish_fountain() -> bpy.types.Object:
	root = root_object("GalaxyWishFountainPass35")
	cylinder("Foot", (0.0, 0.0, 0.25), 3.0, 0.50, MATS["violet"], root, vertices=24)
	torus("BasinInk", (0.0, 0.0, 1.20), 2.32, 0.42, MATS["ink"], root)
	torus("BasinPearl", (0.0, 0.0, 1.28), 2.28, 0.27, MATS["pearl"], root)
	cylinder("Water", (0.0, 0.0, 1.18), 2.15, 0.16, MATS["aqua"], root, vertices=24)
	for index in range(7):
		angle = -math.pi * 0.5 + index * math.pi / 6.0
		vertical_prism(f"ShellRib_{index}", [(-0.16, 0.0), (0.0, 2.2), (0.16, 0.0)], 0.22, MATS["coral_light"] if index % 2 else MATS["lavender"], root, (math.cos(angle) * 0.75, -0.35, 1.55 + math.sin(angle) * 0.10))
	sphere("FountainPearl", (0.0, -0.46, 3.62), (0.52, 0.34, 0.52), MATS["pearl"], root, 16, 10)
	return root


def build_galaxy_star_bell(index: int) -> bpy.types.Object:
	root = root_object(f"GalaxyStarBellPass35_{index}")
	accent = ("coral", "aqua", "leaf_light")[index]
	vertical_prism("StarInk", [(x * 1.42, y * 1.42) for x, y in star_points()], 0.30, MATS["ink"], root, (0.0, 0.0, 2.20))
	vertical_prism("StarFace", [(x * 1.24, y * 1.24) for x, y in star_points()], 0.36, MATS[accent], root, (0.0, -0.08, 2.22))
	curve_tube("Hanger", [(0.0, 0.0, 3.35), (0.0, 0.0, 4.25)], 0.10, MATS["gold"], root)
	sphere("Clapper", (0.0, 0.0, 0.55), (0.34, 0.34, 0.34), MATS["gold"], root, 12, 8)
	return root


def build_ice_gate() -> bpy.types.Object:
	root = root_object("GalaxyIceGatePass35")
	cylinder("FootInk", (0.0, 0.0, 0.34), 3.75, 0.68, MATS["ink"], root, vertices=24)
	cylinder("Foot", (0.0, -0.04, 0.48), 3.42, 0.56, MATS["violet"], root, vertices=24)
	for side in (-1.0, 1.0):
		cube(f"FrostPostInk_{side}", (side * 2.65, 0.0, 3.05), (1.28, 1.28, 5.70), MATS["ink"], root, radius=0.30)
		cube(f"FrostPost_{side}", (side * 2.65, -0.10, 3.08), (0.96, 0.94, 5.38), MATS["ice"], root, radius=0.24)
		for berry in range(3):
			z = 1.40 + float(berry) * 1.48
			sphere(f"PostBerry_{side}_{berry}", (side * 2.65, -0.62, z), (0.34, 0.22, 0.34), MATS[("aqua", "lavender", "coral")[berry]], root, 12, 8)
	arch_points = [(-2.65, 0.0, 5.65), (-2.00, 0.0, 7.15), (-1.00, 0.0, 8.05), (0.0, 0.0, 8.35), (1.00, 0.0, 8.05), (2.00, 0.0, 7.15), (2.65, 0.0, 5.65)]
	curve_tube("FrostArchInk", arch_points, 0.62, MATS["ink"], root)
	curve_tube("FrostArch", [(x, -0.10, z) for x, _y, z in arch_points], 0.40, MATS["aqua_light"], root)
	vertical_prism("SnowflakeInk", [(x * 1.42, y * 1.42) for x, y in star_points(1.0, 0.34)], 0.24, MATS["ink"], root, (0.0, -0.64, 6.75))
	vertical_prism("Snowflake", [(x * 1.22, y * 1.22) for x, y in star_points(1.0, 0.34)], 0.30, MATS["pearl"], root, (0.0, -0.78, 6.75))
	return root


def build_shell_throne() -> bpy.types.Object:
	root = root_object("GalaxyShellThronePass35")
	cube("SeatInk", (0.0, 0.0, 1.15), (5.6, 4.5, 2.10), MATS["ink"], root, radius=0.52)
	cube("Seat", (0.0, -0.10, 1.28), (5.15, 4.05, 1.78), MATS["pearl"], root, radius=0.46)
	for index in range(7):
		angle = -0.92 + index * 1.84 / 6.0
		x = math.sin(angle) * 3.75
		z = 3.30 + math.cos(angle) * 3.15
		sphere(f"ShellLobe_{index}", (x, 1.35, z), (1.05, 0.70, 2.05), MATS["lavender"] if index % 2 else MATS["aqua_light"], root, 16, 10)
	vertical_prism("CrownStar", star_points(0.85, 0.48), 0.30, MATS["gold"], root, (0.0, 0.58, 6.75))
	return root


def vertical_prism(name, points, depth, mat, parent, location, rotation=(math.pi * 0.5, 0.0, 0.0)):
	obj = prism_polygon(name, points, depth, mat, parent, location)
	obj.rotation_euler = rotation
	return obj


def build_clownfish() -> bpy.types.Object:
	"""A readable fish silhouette with a real caudal peduncle and complete fins."""
	root = root_object("ClownfishPass35")
	sphere("Body", (0.0, 0.0, 1.10), (0.70, 1.52, 0.82), MATS["coral"], root, 20, 12)
	sphere("Muzzle", (0.0, -1.30, 1.12), (0.60, 0.52, 0.68), MATS["coral_light"], root, 16, 10)
	sphere("TailPeduncle", (0.0, 1.42, 1.08), (0.34, 0.50, 0.38), MATS["coral"], root, 14, 8)
	for y, radius in ((-0.86, 0.69), (0.08, 0.72), (1.00, 0.48)):
		torus(f"PearlBand_{y}", (0.0, y, 1.10), radius, 0.10, MATS["pearl"], root, (math.pi * 0.5, 0.0, 0.0))
	vertical_prism("TailInk", [(-0.12, 0.0), (-0.95, 0.90), (-0.72, 0.02), (-0.98, -0.88), (0.12, -0.12)], 0.28, MATS["ink"], root, (0.0, 1.82, 1.08))
	vertical_prism("Tail", [(-0.08, 0.0), (-0.78, 0.72), (-0.58, 0.02), (-0.80, -0.70), (0.08, -0.10)], 0.34, MATS["gold"], root, (0.0, 1.80, 1.08))
	vertical_prism("DorsalFin", [(-0.72, 0.0), (0.05, 0.78), (0.82, 0.0)], 0.18, MATS["gold"], root, (0.0, 0.05, 1.78), (0.0, math.pi * 0.5, 0.0))
	vertical_prism("AnalFin", [(-0.54, 0.0), (0.10, -0.55), (0.66, 0.0)], 0.16, MATS["gold"], root, (0.0, 0.44, 0.42), (0.0, math.pi * 0.5, 0.0))
	for side in (-1.0, 1.0):
		fin = vertical_prism(f"Pectoral_{side}", [(-0.32, 0.0), (0.28, 0.50), (0.48, -0.20)], 0.13, MATS["aqua"], root, (side * 0.64, -0.48, 0.92), (0.0, math.pi * 0.5, side * 0.36))
		fin.scale *= 0.78
		sphere(f"Eye_{side}", (side * 0.48, -1.57, 1.34), (0.11, 0.09, 0.13), MATS["ink"], root, 12, 8)
	curve_tube("Mouth", [(-0.20, -1.78, 1.00), (0.0, -1.83, 0.96), (0.20, -1.78, 1.00)], 0.035, MATS["ink"], root)
	return root


def build_octopus() -> bpy.types.Object:
	"""Eight independent arms, a mantle, siphon, and paired camera-facing eyes."""
	root = root_object("OctopusPass35")
	sphere("Mantle", (0.0, 0.10, 2.28), (1.04, 0.92, 1.38), MATS["lavender"], root, 20, 12)
	sphere("Head", (0.0, -0.08, 1.30), (1.10, 0.95, 0.82), MATS["coral_light"], root, 18, 10)
	for side in (-1.0, 1.0):
		sphere(f"EyeWhite_{side}", (side * 0.50, -0.83, 1.48), (0.25, 0.14, 0.29), MATS["pearl"], root, 14, 8)
		sphere(f"Pupil_{side}", (side * 0.50, -0.96, 1.46), (0.10, 0.07, 0.13), MATS["ink"], root, 12, 8)
	cone("Siphon", (0.76, -0.35, 1.02), 0.22, 0.12, 0.62, MATS["coral"], root, (0.25, 0.65, 0.0), 12)
	for arm in range(8):
		angle = arm * math.tau / 8.0
		direction = Vector((math.cos(angle), math.sin(angle), 0.0))
		start = direction * 0.58 + Vector((0.0, 0.0, 0.92))
		middle = direction * (1.38 + 0.14 * (arm % 2)) + Vector((0.0, 0.0, 0.42 + 0.10 * (arm % 3)))
		curl = Vector((-direction.y, direction.x, 0.0)) * (0.42 if arm % 2 else -0.42)
		end = direction * (2.05 + 0.12 * (arm % 3)) + curl + Vector((0.0, 0.0, 0.14))
		curve_tube(f"Arm_{arm + 1}", [start, middle, end], 0.18 - arm % 2 * 0.02, MATS["coral"] if arm % 2 else MATS["lavender"], root)
		for sucker in range(2):
			p = middle.lerp(end, 0.35 + sucker * 0.34)
			sphere(f"Sucker_{arm + 1}_{sucker}", tuple(p + Vector((0.0, 0.0, 0.10))), (0.075, 0.075, 0.045), MATS["pearl"], root, 10, 6)
	return root


def build_jellyfish() -> bpy.types.Object:
	"""A bell, scalloped margin, four oral arms, and eight fine tentacles."""
	root = root_object("JellyfishPass35")
	sphere("Bell", (0.0, 0.0, 2.55), (1.46, 1.30, 0.88), MATS["aqua"], root, 20, 12)
	torus("BellMargin", (0.0, 0.0, 2.10), 1.12, 0.15, MATS["pearl"], root)
	for lobe in range(8):
		angle = lobe * math.tau / 8.0
		sphere(f"MarginLobe_{lobe}", (math.cos(angle) * 1.05, math.sin(angle) * 1.05, 2.04), (0.28, 0.28, 0.18), MATS["lavender"] if lobe % 2 else MATS["coral_light"], root, 12, 8)
	for arm in range(4):
		angle = arm * math.tau / 4.0 + math.pi * 0.25
		x, y = math.cos(angle) * 0.40, math.sin(angle) * 0.40
		curve_tube(f"OralArm_{arm + 1}", [(x, y, 2.08), (x * 1.20, y * 1.20, 1.15), (x * 0.72, y * 0.72, 0.28)], 0.17, MATS["coral_light"] if arm % 2 else MATS["lavender"], root)
	for tentacle in range(8):
		angle = tentacle * math.tau / 8.0
		x, y = math.cos(angle) * 0.92, math.sin(angle) * 0.92
		wave = Vector((-math.sin(angle), math.cos(angle), 0.0)) * (0.20 if tentacle % 2 else -0.20)
		curve_tube(f"Tentacle_{tentacle + 1}", [(x, y, 2.03), tuple(Vector((x * 1.02, y * 1.02, 1.10)) + wave), (x * 0.88, y * 0.88, 0.05)], 0.055, MATS["aqua_light"], root)
	return root


def build_shrimp() -> bpy.types.Object:
	"""Future-safe shrimp with segmented abdomen, tail fan, antennae and ten legs."""
	root = root_object("ShrimpPass35")
	sphere("Carapace", (0.0, -1.02, 0.92), (0.58, 0.78, 0.56), MATS["coral_light"], root, 16, 10)
	for segment in range(6):
		y = -0.38 + segment * 0.43
		z = 0.92 + math.sin(segment / 5.0 * math.pi) * 0.30
		scale = 0.52 - segment * 0.045
		sphere(f"Abdomen_{segment + 1}", (0.0, y, z), (scale, 0.34, scale * 0.82), MATS["coral"] if segment % 2 else MATS["coral_light"], root, 14, 8)
	for side in (-1.0, 1.0):
		sphere(f"EyeStalk_{side}", (side * 0.38, -1.56, 1.25), (0.12, 0.12, 0.12), MATS["ink"], root, 10, 6)
		curve_tube(f"Antenna_{side}", [(side * 0.32, -1.56, 1.28), (side * 0.72, -2.25, 1.52), (side * 1.18, -3.25, 1.18)], 0.035, MATS["coral"], root)
		for leg in range(5):
			y = -0.82 + leg * 0.36
			curve_tube(f"WalkingLeg_{side}_{leg + 1}", [(side * 0.30, y, 0.73), (side * 0.72, y - 0.08, 0.36), (side * 0.92, y + 0.10, 0.08)], 0.045, MATS["coral"], root)
	vertical_prism("TailFanCenter", [(-0.18, 0.0), (0.0, 0.72), (0.18, 0.0)], 0.18, MATS["gold"], root, (0.0, 2.35, 0.88))
	for side in (-1.0, 1.0):
		fan = vertical_prism(f"TailFan_{side}", [(0.0, 0.0), (side * 0.88, 0.56), (side * 0.54, -0.34)], 0.16, MATS["coral_light"], root, (0.0, 2.30, 0.88))
		fan.rotation_euler.y = side * 0.10
	return root


def build_meadow_bush(variant: int) -> bpy.types.Object:
	root = root_object(f"MeadowBushPass35_{variant}")
	accents = ("coral", "gold", "lavender", "aqua")
	cube("Root", (0.0, 0.0, 0.30), (0.62, 0.62, 0.60), MATS["wood"], root, radius=0.14)
	profiles = ((-0.92, 0.05, 0.88), (-0.38, -0.18, 1.18), (0.28, 0.10, 1.26), (0.86, -0.06, 0.92), (0.0, 0.38, 0.88))
	for index, (x, y, z) in enumerate(profiles):
		ico(f"LeafMass_{index}", (x, y, z), (0.80, 0.66, 0.72), MATS["leaf_light"] if index % 2 else MATS["leaf"], root, 2)
	for flower in range(5):
		angle = flower * math.tau / 5.0 + variant * 0.32
		x, y = math.cos(angle) * 0.82, math.sin(angle) * 0.44 - 0.42
		for petal in range(5):
			pa = petal * math.tau / 5.0
			sphere(f"Flower_{flower}_Petal_{petal}", (x + math.cos(pa) * 0.18, y, 1.46 + math.sin(pa) * 0.18), (0.15, 0.08, 0.20), MATS[accents[variant]], root, 10, 6)
		sphere(f"Flower_{flower}_Center", (x, y - 0.06, 1.46), (0.10, 0.08, 0.10), MATS["pearl"], root, 10, 6)
	return root


def build_winter_shore_cluster(variant: int) -> bpy.types.Object:
	root = root_object(f"WinterShoreClusterPass35_{variant}")
	for index in range(3 + variant):
		x = (index - (2 + variant) * 0.5) * 1.20
		scale = 0.70 + 0.18 * ((index + variant) % 3)
		ico(f"Stone_{index}", (x, 0.0, scale * 0.48), (scale, scale * 0.72, scale * 0.68), MATS["stone"], root, 2)
		sphere(f"SnowCap_{index}", (x - 0.08, -0.04, scale * 0.92), (scale * 0.82, scale * 0.58, scale * 0.25), MATS["snow"], root, 14, 8)
	for reed in range(4):
		x = -1.65 + reed * 1.10
		curve_tube(f"WinterReed_{reed}", [(x, 0.25, 0.0), (x + 0.12, 0.22, 0.85), (x + 0.26, 0.18, 1.55 + 0.18 * (reed % 2))], 0.045, MATS["aqua"], root)
	return root


def build_treasure_chest() -> bpy.types.Object:
	root = root_object("TreasureChestPass35")
	cube("ChestInk", (0.0, 0.0, 1.12), (5.20, 3.70, 2.24), MATS["ink"], root, radius=0.36)
	cube("ChestBody", (0.0, -0.05, 1.18), (4.78, 3.28, 1.88), MATS["wood_light"], root, radius=0.28)
	# The lid stays visibly attached to the body. Two rounded boxes read more
	# reliably at phone size than the former oversized floating ellipsoid.
	cube("LidInk", (0.0, 0.0, 2.64), (5.30, 3.82, 1.42), MATS["ink"], root, radius=0.52)
	cube("Lid", (0.0, -0.06, 2.66), (4.88, 3.40, 1.10), MATS["wood"], root, radius=0.46)
	for band_x in (-1.55, 0.0, 1.55):
		cube(f"GoldBand_{band_x}", (band_x, -1.78, 1.85), (0.30, 0.18, 3.10), MATS["gold"], root, radius=0.06)
	cube("LockInk", (0.0, -1.94, 1.72), (0.94, 0.24, 1.18), MATS["ink"], root, radius=0.14)
	cube("Lock", (0.0, -2.08, 1.74), (0.64, 0.18, 0.88), MATS["gold"], root, radius=0.12)
	for pearl, x in enumerate((-1.25, -0.62, 0.62, 1.25)):
		sphere(f"TreasurePearl_{pearl}", (x, -1.90, 0.54), (0.20, 0.14, 0.20), MATS["pearl"], root, 12, 8)
	return root


def build_treasure_cluster(variant: int) -> bpy.types.Object:
	root = root_object(f"TreasureClusterPass35_{variant}")
	colors = ("aqua", "lavender", "coral")
	for index in range(4 + variant):
		angle = index * math.tau / (4 + variant)
		radius = 0.58 + 0.22 * (index % 2)
		height = 1.55 + 0.45 * ((index + variant) % 3)
		crystal = cone(f"Crystal_{index}", (math.cos(angle) * radius, math.sin(angle) * radius, height * 0.5), 0.48, 0.02, height, MATS[colors[(index + variant) % 3]], root, vertices=6)
		crystal.rotation_euler = (0.18 * math.sin(angle), 0.20 * math.cos(angle), -angle * 0.10)
	torus("PearlNest", (0.0, 0.0, 0.18), 1.18, 0.16, MATS["pearl"], root)
	for pearl in range(3):
		angle = pearl * math.tau / 3.0 + variant
		sphere(f"Gem_{pearl}", (math.cos(angle) * 1.30, math.sin(angle) * 1.30, 0.30), (0.25, 0.25, 0.25), MATS[colors[(pearl + variant) % 3]], root, 12, 8)
	return root


def build_pepper_projectile() -> bpy.types.Object:
	"""A broad, curved chili silhouette that remains readable while moving."""
	root = root_object("PepperProjectilePass35")
	# Use colored overlapping lobes instead of an enclosing ink shell. At the
	# projectile's gameplay scale the shell hid the red body and read as an
	# eggplant; this hooked taper reads immediately as a hot pepper.
	ico("PepperShoulder", (-0.05, -0.62, 0.0), (0.68, 0.62, 0.54), MATS["coral"], root, 2, rotation=(0.08, 0.0, -0.08))
	ico("PepperBody", (0.02, -0.02, -0.02), (0.61, 0.70, 0.49), MATS["coral"], root, 2, rotation=(0.12, 0.0, -0.14))
	ico("PepperTaper", (0.18, 0.58, -0.08), (0.46, 0.56, 0.38), MATS["coral_light"], root, 2, rotation=(0.18, 0.0, -0.28))
	ico("PepperHook", (0.45, 1.00, -0.14), (0.27, 0.43, 0.25), MATS["coral_light"], root, 1, rotation=(0.28, 0.0, -0.52))
	curve_tube("StemInk", [(-0.05, -1.08, 0.08), (0.02, -1.42, 0.22), (0.30, -1.66, 0.30)], 0.16, MATS["ink"], root)
	curve_tube("Stem", [(-0.05, -1.08, 0.08), (0.02, -1.42, 0.22), (0.30, -1.66, 0.30)], 0.095, MATS["leaf_light"], root)
	for index, x in enumerate((-0.34, 0.0, 0.34)):
		cone(f"PepperCalyx_{index}", (x, -1.02, 0.08), 0.24, 0.03, 0.55, MATS["leaf"], root, rotation=(math.pi * 0.5, 0.0, x * 0.35), vertices=7)
	return root


def build_ice_berry_projectile() -> bpy.types.Object:
	"""A faceted berry with a leafy crown, paired with the fire projectile."""
	root = root_object("IceBerryProjectilePass35")
	ico("BerryBody", (0.0, -0.05, 0.0), (0.80, 0.80, 0.80), MATS["aqua"], root, 2)
	for index in range(6):
		angle = float(index) * math.tau / 6.0
		ico(f"FrostFacet_{index}", (math.cos(angle) * 0.55, math.sin(angle) * 0.55 - 0.05, 0.31), (0.15, 0.15, 0.10), MATS["ice"], root, 1)
	for index in range(4):
		angle = float(index) * math.tau / 4.0
		leaf = cone(f"BerryLeaf_{index}", (math.cos(angle) * 0.24, math.sin(angle) * 0.24, 0.91), 0.24, 0.02, 0.72, MATS["leaf_light"], root, rotation=(0.0, 0.62, angle), vertices=7)
		leaf.scale.z = 0.55
		bpy.context.view_layer.objects.active = leaf
		leaf.select_set(True)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		leaf.select_set(False)
	cylinder("BerryStem", (0.0, 0.0, 1.08), 0.10, 0.30, MATS["leaf"], root, vertices=8)
	return root


def build_shop_interior() -> bpy.types.Object:
	"""Open-fronted shop shell with broad, non-repeating storybook panels."""
	root = root_object("PearlShopInteriorPass35")
	floor_mats = ("aqua_light", "pearl", "coral_light", "lavender", "leaf_light", "pearl")
	for index, mat_name in enumerate(floor_mats):
		y = -10.0 + float(index) * 4.6
		cube(f"FloorInk_{index}", (0.0, y, -0.05), (32.4, 4.45, 0.46), MATS["ink"], root, radius=0.18)
		cube(f"FloorPanel_{index}", (0.0, y, 0.18), (31.8, 4.18, 0.28), MATS[mat_name], root, radius=0.16)
	wall_mats = ("coral_light", "aqua_light", "pearl", "lavender", "leaf_light")
	for index, mat_name in enumerate(wall_mats):
		x = -12.8 + float(index) * 6.4
		cube(f"WallInk_{index}", (x, 13.0, 9.2), (6.2, 1.05, 17.8), MATS["ink"], root, radius=0.30)
		cube(f"WallPanel_{index}", (x, 12.55, 9.2), (5.72, 0.36, 17.25), MATS[mat_name], root, radius=0.24)
	for side in (-1.0, 1.0):
		cube(f"SidePostInk_{side}", (side * 16.0, 12.4, 9.3), (1.25, 1.65, 18.6), MATS["ink"], root, radius=0.24)
		cube(f"SidePost_{side}", (side * 16.0, 12.0, 9.3), (0.86, 0.90, 18.0), MATS["violet"], root, radius=0.18)
	# Scalloped canopy and central pearl-shell emblem create one readable focal wall.
	for index in range(7):
		x = -12.0 + float(index) * 4.0
		sphere(f"CanopyScallop_{index}", (x, 12.10, 17.7), (2.28, 0.62, 1.72), MATS[("aqua", "coral", "gold")[index % 3]], root, 16, 8)
	torus("ShellEmblemInk", (0.0, 11.84, 11.2), 2.65, 0.34, MATS["ink"], root, (math.pi * 0.5, 0.0, 0.0))
	for ray in range(7):
		angle = math.pi * (0.12 + 0.76 * float(ray) / 6.0)
		sphere(
			f"ShellRay_{ray}",
			(math.cos(angle) * 2.1, 11.30, 10.8 + math.sin(angle) * 2.0),
			(0.62, 0.24, 1.28),
			MATS["pearl"] if ray % 2 else MATS["aqua_light"],
			root,
			14,
			8,
		)
	# Rounded counter is part of the same authored set so wares retain their gameplay positions.
	cube("CounterInk", (0.0, 5.0, 1.35), (13.2, 4.9, 2.9), MATS["ink"], root, radius=0.48)
	cube("CounterBody", (0.0, 4.88, 1.42), (12.55, 4.35, 2.48), MATS["leaf"], root, radius=0.40)
	cube("CounterTop", (0.0, 4.72, 2.82), (13.05, 4.65, 0.42), MATS["gold"], root, radius=0.18)
	for x in (-4.5, 0.0, 4.5):
		torus(f"CounterPearlRing_{x}", (x, 2.62, 1.45), 0.58, 0.14, MATS["pearl"], root, (math.pi * 0.5, 0.0, 0.0))
		sphere(f"CounterPearl_{x}", (x, 2.42, 1.45), (0.28, 0.16, 0.28), MATS["coral_light"], root, 12, 8)
	return root


def build_slide_snowbank(variant: int) -> bpy.types.Object:
	root = root_object(f"SlideSnowbankPass35_{variant}")
	for index in range(5 + variant):
		x = -3.8 + float(index) * 1.55
		y = 0.42 * math.sin(float(index) * 1.7 + variant)
		scale = 0.82 + 0.18 * ((index + variant) % 3)
		ico(f"SnowMass_{index}", (x, y, 0.42 * scale), (1.32 * scale, 0.86 * scale, 0.62 * scale), MATS["snow"], root, 2)
	for index in range(3):
		x = -2.7 + float(index) * 2.8
		crystal = cone(f"IceMarker_{index}", (x, -0.10, 1.02), 0.42, 0.04, 1.85 + 0.25 * (index % 2), MATS["ice"] if index % 2 else MATS["aqua"], root, vertices=6)
		crystal.rotation_euler = (0.12 * (index - 1), 0.0, 0.12 * (1 - index))
	return root


def build_slide_finish_arch() -> bpy.types.Object:
	root = root_object("SlideFinishArchPass35")
	for side in (-1.0, 1.0):
		cube(f"PostInk_{side}", (side * 5.0, 0.0, 3.4), (1.15, 1.35, 6.8), MATS["ink"], root, radius=0.24)
		cube(f"Post_{side}", (side * 5.0, -0.06, 3.4), (0.82, 1.02, 6.45), MATS["ice"], root, radius=0.18)
	curve_tube("ArchInk", [(-5.0, 0.0, 6.4), (-2.7, 0.0, 8.6), (0.0, 0.0, 9.1), (2.7, 0.0, 8.6), (5.0, 0.0, 6.4)], 0.42, MATS["ink"], root)
	curve_tube("Arch", [(-5.0, -0.12, 6.4), (-2.7, -0.12, 8.6), (0.0, -0.12, 9.1), (2.7, -0.12, 8.6), (5.0, -0.12, 6.4)], 0.28, MATS["aqua_light"], root)
	vertical_prism("FinishStar", star_points(1.25, 0.48), 0.34, MATS["gold"], root, (0.0, -0.58, 8.2))
	return root


def build_fairy_bank(variant: int) -> bpy.types.Object:
	root = root_object(f"FairyPondBankPass35_{variant}")
	for index in range(4):
		x = -2.8 + float(index) * 1.85
		ico(f"BankStone_{index}", (x, 0.0, 0.38), (1.10, 0.82, 0.58), MATS["stone_dark"] if index % 2 else MATS["stone"], root, 2)
	for index in range(7):
		x = -3.25 + float(index) * 1.08
		height = 1.65 + 0.34 * ((index + variant) % 3)
		blade(f"BankLeaf_{index}", (x, 0.10 + 0.18 * (index % 2), 0.45), height, 0.58, (-0.30 + 0.10 * index), MATS["leaf_light"] if index % 2 else MATS["aqua"], root)
	for flower in range(3):
		x = -2.15 + flower * 2.15
		for petal in range(5):
			pa = petal * math.tau / 5.0
			sphere(f"BankFlower_{flower}_{petal}", (x + math.cos(pa) * 0.34, -0.28, 2.15 + math.sin(pa) * 0.34), (0.28, 0.13, 0.38), MATS[("coral_light", "lavender", "gold")[flower]], root, 12, 7)
		sphere(f"BankFlowerCenter_{flower}", (x, -0.40, 2.15), (0.20, 0.12, 0.20), MATS["pearl"], root, 10, 6)
	return root


def build_shadow_jellyfish() -> bpy.types.Object:
	root = root_object("FairyShadowJellyfishPass35")
	# A true bell, four oral arms and eight tentacles preserve the same anatomy
	# standard as the reef jellyfish while allowing a darker gameplay palette.
	sphere("Bell", (0.0, 0.0, 2.65), (2.15, 2.15, 1.48), MATS["violet"], root, 24, 12)
	torus("BellRim", (0.0, 0.0, 2.12), 1.84, 0.18, MATS["lavender"], root)
	for index in range(4):
		angle = index * math.tau / 4.0 + math.pi * 0.25
		curve_tube(
			f"OralArm_{index}",
			[(math.cos(angle) * 0.72, math.sin(angle) * 0.72, 2.15), (math.cos(angle) * 0.90, math.sin(angle) * 0.90, 0.55), (math.cos(angle + 0.35) * 1.20, math.sin(angle + 0.35) * 1.20, -0.35)],
			0.20,
			MATS["coral"],
			root,
		)
	for index in range(8):
		angle = index * math.tau / 8.0
		curve_tube(
			f"Tentacle_{index}",
			[(math.cos(angle) * 1.55, math.sin(angle) * 1.55, 2.05), (math.cos(angle + 0.18) * 1.72, math.sin(angle + 0.18) * 1.72, 0.50), (math.cos(angle - 0.22) * 1.52, math.sin(angle - 0.22) * 1.52, -1.30)],
			0.075,
			MATS["lavender"],
			root,
		)
	return root


def build_shadow_eel() -> bpy.types.Object:
	root = root_object("FairyShadowEelPass35")
	for index in range(11):
		t = float(index) / 10.0
		x = -5.2 + 10.4 * t
		y = math.sin(t * math.tau) * 0.72
		radius = 0.95 * (1.0 - 0.70 * t) + 0.12
		sphere(f"Body_{index}", (x, y, 1.15), (0.82, radius, radius), MATS["violet"], root, 14, 8)
	# Paired pectoral fins and a continuous tail fin keep the silhouette fish-like.
	for side in (-1.0, 1.0):
		fin = cone(f"PectoralFin_{side}", (-2.65, side * 1.05, 1.05), 0.72, 0.05, 1.70, MATS["lavender"], root, (math.pi * 0.5, 0.0, 0.0), 6)
		fin.rotation_euler.y = side * 0.40
	vertical_prism("TailFin", [(0.0, 1.3), (1.2, 0.0), (0.0, -1.3), (-0.5, 0.0)], 0.24, MATS["coral"], root, (5.45, 0.0, 1.15))
	for side in (-1.0, 1.0):
		sphere(f"Eye_{side}", (-4.74, side * 0.68, 1.55), (0.25, 0.16, 0.25), MATS["pearl"], root, 10, 6)
		sphere(f"Pupil_{side}", (-4.90, side * 0.81, 1.56), (0.11, 0.08, 0.11), MATS["ink"], root, 10, 6)
	return root


def build_treasure_dais() -> bpy.types.Object:
	root = root_object("TreasureDaisPass35")
	cylinder("DaisInk", (0.0, 0.0, 0.38), 4.45, 0.76, MATS["ink"], root, vertices=24)
	cylinder("Dais", (0.0, 0.0, 0.62), 4.05, 0.62, MATS["violet"], root, vertices=24)
	torus("PearlBorder", (0.0, 0.0, 0.95), 3.55, 0.22, MATS["gold"], root)
	for index in range(8):
		angle = index * math.tau / 8.0
		sphere(f"BorderPearl_{index}", (math.cos(angle) * 3.55, math.sin(angle) * 3.55, 1.00), (0.28, 0.28, 0.28), MATS["pearl"], root, 12, 8)
	return root


def build_dungeon_gate() -> bpy.types.Object:
	root = root_object("DungeonGatePass35")
	for side in (-1.0, 1.0):
		cube(f"PillarInk_{side}", (side * 3.20, 0.0, 3.20), (1.48, 1.30, 6.40), MATS["ink"], root, radius=0.26)
		cube(f"Pillar_{side}", (side * 3.20, -0.10, 3.20), (1.10, 0.96, 6.04), MATS["lavender"], root, radius=0.20)
		for pearl in range(5):
			z = 1.15 + float(pearl) * 1.05
			sphere(f"RoomPearl_{'L' if side < 0 else 'R'}_{pearl + 1}", (side * 3.20, 0.72, z), (0.31, 0.20, 0.31), MATS[("gold", "aqua", "coral", "lavender", "pearl")[pearl]], root, 12, 8)
	cube("LintelInk", (0.0, 0.0, 6.55), (7.70, 1.35, 1.45), MATS["ink"], root, radius=0.28)
	cube("Lintel", (0.0, -0.10, 6.56), (7.28, 1.00, 1.08), MATS["violet"], root, radius=0.22)
	vertical_prism("GateStarInk", [(x * 1.12, y * 1.12) for x, y in star_points(0.90, 0.46)], 0.30, MATS["ink"], root, (0.0, 0.68, 6.55))
	vertical_prism("GateStar", star_points(0.78, 0.46), 0.34, MATS["gold"], root, (0.0, 0.82, 6.55))
	return root


def build_star_observatory() -> bpy.types.Object:
	root = root_object("StarObservatoryPass35")
	cylinder("PedestalInk", (0.0, 0.0, 0.58), 2.38, 1.16, MATS["ink"], root, vertices=24)
	cylinder("Pedestal", (0.0, -0.05, 0.68), 2.08, 0.96, MATS["violet"], root, vertices=24)
	star = build_star("ObservatoryStarInner", "lavender", False, True)
	star.parent = root
	star.location = (0.0, 0.0, 4.15)
	star.scale = (2.20, 2.20, 2.20)
	for orbit, tilt in ((3.25, 0.25), (3.78, -0.34), (4.28, 0.56)):
		torus(f"Orbit_{orbit}", (0.0, 0.0, 4.15), orbit, 0.075, MATS["aqua_light"], root, (math.pi * 0.5 + tilt, 0.18 * orbit, 0.0))
	for planet, (angle, radius, mat_name) in enumerate(((0.30, 3.25, "coral"), (2.25, 3.78, "gold"), (4.45, 4.28, "aqua"))):
		sphere(f"Planet_{planet}", (math.cos(angle) * radius, math.sin(angle) * 0.65, 4.15 + math.sin(angle) * radius * 0.36), (0.32, 0.32, 0.32), MATS[mat_name], root, 12, 8)
	return root


for variant in range(3):
	register(f"cloud_{variant}", build_cloud(variant), f"assets/art35/landmarks/cloud_{variant}.glb")

register("dream_star", build_star("DreamStarPass35", "gold", False, False), "assets/art35/landmarks/dream_star.glb")
register("crown_star", build_star("CrownStarPass35", "gold", True, False), "assets/art35/landmarks/crown_star.glb")
register("chamber_star", build_star("ChamberStarPass35", "lavender", False, True), "assets/art35/landmarks/chamber_star.glb")
register("butterfly_gate", build_butterfly_gate(), "assets/art35/landmarks/butterfly_gate.glb")
register("star_observatory", build_star_observatory(), "assets/art35/landmarks/star_observatory.glb")
register("dungeon_gate", build_dungeon_gate(), "assets/art35/castle/dungeon_gate.glb")

coral_names = ("coral", "coral1", "coral2", "coral3", "coral4", "coral5", "coral6")
for index, name in enumerate(coral_names):
	register(name, build_coral(index), f"assets/props/gen2/{name}.glb")

rock_names = ("rock", "rock1", "rock2", "rock3", "rock4", "rock5")
for index, name in enumerate(rock_names):
	register(name, build_rock(index), f"assets/props/gen2/{name}.glb")
register("rock_largea", build_rock(2, True), "assets/props/gen2/rock_largea.glb")
register("clownfish", build_clownfish(), "assets/props/gen2/clownfish.glb")
register("octopus", build_octopus(), "assets/props/gen2/octopus.glb")
register("jellyfish", build_jellyfish(), "assets/props/gen2/jellyfish.glb")
register("shrimp", build_shrimp(), "assets/props/gen2/shrimp.glb")

register("seagrass_0", build_plant("SeagrassPass35_0", False, 0), "assets/art35/reef/seagrass_0.glb")
register("seagrass_1", build_plant("SeagrassPass35_1", False, 1), "assets/art35/reef/seagrass_1.glb")
register("kelp_0", build_plant("KelpPass35_0", True, 0), "assets/art35/reef/kelp_0.glb")
register("kelp_1", build_plant("KelpPass35_1", True, 1), "assets/art35/reef/kelp_1.glb")

register("kart_showcase_plinth", build_kart_plinth(), "assets/art35/kart/showcase_plinth.glb")
register("kart_finish_arch", build_finish_arch(), "assets/art35/kart/finish_arch.glb")
register("kart_barrier", build_barrier(), "assets/art35/kart/soft_barrier.glb")
register("northern_castle", build_northern_castle(), "assets/art35/northern/northern_castle.glb")
for variant in range(3):
	register(f"northern_house_{variant}", build_northern_house(variant), f"assets/art35/northern/northern_house_{variant}.glb")
register("northern_mountain", build_northern_mountain(), "assets/art35/northern/northern_mountain.glb")
register("northern_gate", build_northern_gate(), "assets/art35/northern/northern_gate.glb")
register("kitchen_kettle", build_kettle(), "assets/art35/castle/kitchen_kettle.glb")
register("kitchen_teapot", build_teapot(), "assets/art35/castle/kitchen_teapot.glb")
register("kitchen_pan_set", build_pan_set(), "assets/art35/castle/kitchen_pan_set.glb")
register("kitchen_soup_pot", build_soup_pot(), "assets/art35/castle/kitchen_soup_pot.glb")
register("kitchen_table_set", build_table_set(), "assets/art35/castle/kitchen_table_set.glb")
register("music_rail", build_music_rail(), "assets/art35/castle/music_rail.glb")
for index in range(7):
	register(f"music_bar_{index}", build_music_bar(index), f"assets/art35/castle/music_bar_{index}.glb")
register("music_song_star", build_song_star(), "assets/art35/castle/music_song_star.glb")
register("music_wall_panel", build_music_wall_panel(), "assets/art35/castle/music_wall_panel.glb")
register("royal_bed", build_royal_bed("aqua"), "assets/art35/castle/royal_bed.glb")
register("royal_nightstand", build_nightstand(), "assets/art35/castle/royal_nightstand.glb")
register("royal_bookcase", build_bookcase(), "assets/art35/castle/royal_bookcase.glb")
dream_accents = ("coral", "aqua", "lavender", "leaf_light", "coral_light")
for index, accent in enumerate(dream_accents):
	register(f"dream_bed_{index}", build_royal_bed(accent), f"assets/art35/castle/dream_bed_{index}.glb")
for variant in range(3):
	register(f"winter_tree_{variant}", build_winter_tree(variant), f"assets/art35/arena/winter_tree_{variant}.glb")
for variant in range(2):
	register(f"winter_shore_{variant}", build_winter_shore_cluster(variant), f"assets/art35/arena/winter_shore_{variant}.glb")
for variant in range(4):
	register(f"meadow_bush_{variant}", build_meadow_bush(variant), f"assets/art35/arena/meadow_bush_{variant}.glb")
register("treasure_chest", build_treasure_chest(), "assets/art35/arena/treasure_chest.glb")
for variant in range(3):
	register(f"treasure_cluster_{variant}", build_treasure_cluster(variant), f"assets/art35/arena/treasure_cluster_{variant}.glb")
register("treasure_dais", build_treasure_dais(), "assets/art35/arena/treasure_dais.glb")
register("pepper_projectile", build_pepper_projectile(), "assets/dungeon/pepper_projectile.glb")
register("ice_berry_projectile", build_ice_berry_projectile(), "assets/dungeon/ice_berry_projectile.glb")
register("shop_interior", build_shop_interior(), "assets/art35/arena/shop_interior.glb")
for variant in range(2):
	register(f"slide_snowbank_{variant}", build_slide_snowbank(variant), f"assets/art35/arena/slide_snowbank_{variant}.glb")
register("slide_finish_arch", build_slide_finish_arch(), "assets/art35/arena/slide_finish_arch.glb")
register("fairy_lily_cluster", build_lily_cluster(), "assets/art35/arena/fairy_lily_cluster.glb")
register("fairy_flower_gate", build_fairy_ring(), "assets/art35/arena/fairy_flower_gate.glb")
register("fairy_shadow_beetle", build_shadow_beetle(), "assets/art35/arena/fairy_shadow_beetle.glb")
for variant in range(2):
	register(f"fairy_bank_{variant}", build_fairy_bank(variant), f"assets/art35/arena/fairy_bank_{variant}.glb")
register("fairy_shadow_jellyfish", build_shadow_jellyfish(), "assets/art35/arena/fairy_shadow_jellyfish.glb")
register("fairy_shadow_eel", build_shadow_eel(), "assets/art35/arena/fairy_shadow_eel.glb")
register("galaxy_wish_fountain", build_wish_fountain(), "assets/art35/galaxy/wish_fountain.glb")
for index in range(3):
	register(f"galaxy_star_bell_{index}", build_galaxy_star_bell(index), f"assets/art35/galaxy/star_bell_{index}.glb")
register("galaxy_ice_gate", build_ice_gate(), "assets/art35/galaxy/ice_gate.glb")
register("galaxy_shell_throne", build_shell_throne(), "assets/art35/galaxy/shell_throne.glb")


def descendants(root: bpy.types.Object):
	return [root] + list(root.children_recursive)


def select_root(root: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for obj in descendants(root):
		obj.hide_viewport = False
		obj.hide_render = False
		obj.select_set(True)
	bpy.context.view_layer.objects.active = root


def export_root(name: str, root: bpy.types.Object, path: Path) -> None:
	select_root(root)
	path.parent.mkdir(parents=True, exist_ok=True)
	bpy.ops.export_scene.gltf(
		filepath=str(path),
		export_format="GLB",
		use_selection=True,
		export_materials="EXPORT",
		export_animations=False,
		export_yup=True,
	)
	print(f"ART35_EXPORT|{name}|{path}", flush=True)


def join_static_meshes(root: bpy.types.Object) -> None:
	meshes = [obj for obj in descendants(root) if obj.type == "MESH"]
	if len(meshes) < 2:
		return
	bpy.ops.object.select_all(action="DESELECT")
	for obj in meshes:
		obj.select_set(True)
	bpy.context.view_layer.objects.active = meshes[0]
	bpy.ops.object.join()
	joined = bpy.context.active_object
	joined.name = root.name + "Mesh"
	joined.parent = root


for asset_name, (asset_root, _asset_path) in ASSETS.items():
	if asset_name.startswith("seagrass_") or asset_name.startswith("kelp_"):
		join_static_meshes(asset_root)


for asset_name, (asset_root, asset_path) in ASSETS.items():
	export_root(asset_name, asset_root, asset_path)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))


def mesh_bounds(root: bpy.types.Object) -> tuple[Vector, float]:
	points = []
	for obj in descendants(root):
		if obj.type == "MESH":
			points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
	if not points:
		return Vector((0.0, 0.0, 0.0)), 2.0
	minimum = Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points)))
	maximum = Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points)))
	return (minimum + maximum) * 0.5, max((maximum - minimum).length, 1.0)


scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "rim.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "BOTH"
scene.render.resolution_x = 720
scene.render.resolution_y = 620
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = True

bpy.ops.object.camera_add()
camera = bpy.context.active_object
scene.camera = camera

for asset_name, (asset_root, _asset_path) in ASSETS.items():
	for other_root, _other_path in ASSETS.values():
		for obj in descendants(other_root):
			obj.hide_render = other_root != asset_root
	center, diameter = mesh_bounds(asset_root)
	camera.location = center + Vector((diameter * 0.62, -diameter * 0.88, diameter * 0.52))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	camera.data.type = "ORTHO"
	camera.data.ortho_scale = diameter * 0.68
	scene.render.filepath = str(QA_DIR / f"{asset_name}.png")
	bpy.ops.render.render(write_still=True)
	print(f"ART35_RENDER|{asset_name}|{scene.render.filepath}", flush=True)

print(f"ART35_DONE|assets={len(ASSETS)}", flush=True)
