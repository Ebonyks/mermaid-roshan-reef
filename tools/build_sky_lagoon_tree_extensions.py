#!/usr/bin/env python3
"""Build the seven gen3 Sky Lagoon trees that join the approved ancient oak.

The original four shipped GEN2 roles remain untouched.  These seven use the
same renderer-safe fused-sculpt method as build_sky_lagoon_tree_gen3_trial.py,
but each has a different botanical graph and crown language; they are not
scaled or recolored copies.

Usage: blender --background --python tools/build_sky_lagoon_tree_extensions.py
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit"
BLEND = ROOT / "assets_src" / "blender" / "sky_lagoon_tree_extensions.blend"
OUT.mkdir(parents=True, exist_ok=True)
BLEND.parent.mkdir(parents=True, exist_ok=True)

# The trial module owns the audited palette and low-level sculpt primitives.
trial_path = ROOT / "tools" / "build_sky_lagoon_tree_gen3_trial.py"
spec = importlib.util.spec_from_file_location("sky_tree_gen3", trial_path)
assert spec is not None and spec.loader is not None
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


PathSpec = tuple[list[tuple[float, float, float]], list[float]]


def fused_wood(name: str, paths: list[PathSpec], parent: bpy.types.Object,
		root_count: int, root_reach: float, root_radius: float,
		pale: bool = False, seed: int = 0) -> bpy.types.Object:
	meta = bpy.data.metaballs.new(name + "_wood_volume")
	meta.resolution = 0.115
	meta.render_resolution = 0.085
	meta.threshold = 0.68
	for points, radii in paths:
		g.add_meta_path(meta, points, radii, 0.19)
	for index in range(root_count):
		angle = math.tau * index / root_count + 0.13 * math.sin(seed + index * 1.7)
		reach = root_reach * (0.82 + 0.16 * ((index + seed) % 3))
		g.add_meta_path(meta, [
			(0.0, 0.0, 0.28),
			(math.cos(angle) * reach * 0.42, math.sin(angle) * reach * 0.42, 0.15),
			(math.cos(angle) * reach, math.sin(angle) * reach, 0.04),
		], [root_radius, root_radius * 0.54, 0.065], 0.15)

	obj = bpy.data.objects.new(name + "_fused_wood", meta)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	obj.name = name + "_fused_wood"
	mat_names = ("birch", "lavender", "ink") if pale else ("bark", "bark_light", "bark_shadow")
	for mat_name in mat_names:
		obj.data.materials.append(g.MATS[mat_name])
	texture = bpy.data.textures.new(name + "_surface", type="CLOUDS")
	texture.noise_scale = 0.40
	texture.noise_depth = 1
	displace = obj.modifiers.new("hand_carved_surface", "DISPLACE")
	displace.texture = texture
	displace.strength = 0.040
	displace.texture_coords = "GLOBAL"
	bpy.ops.object.modifier_apply(modifier=displace.name)
	decimate = obj.modifiers.new("mobile_sculpt", "DECIMATE")
	decimate.ratio = 0.34
	bpy.ops.object.modifier_apply(modifier=decimate.name)
	for polygon in obj.data.polygons:
		if polygon.normal.z < -0.35 or polygon.center.y > 0.62:
			polygon.material_index = 2
		elif (polygon.index + seed) % 19 == 0:
			polygon.material_index = 1
		else:
			polygon.material_index = 0
		polygon.use_smooth = True
	bpy.ops.object.select_all(action="DESELECT")
	return obj


def cloud(name: str, location: tuple[float, float, float], scale: tuple[float, float, float],
		palette: tuple[str, str, str], seed: int, parent: bpy.types.Object,
		droop: bool = False) -> bpy.types.Object:
	obj = g.fused_cloud(name, location, scale, seed, parent, palette)
	if droop:
		minimum = min(vertex.co.z for vertex in obj.data.vertices)
		for vertex in obj.data.vertices:
			if vertex.co.z < 0.0:
				factor = max(0.28, 1.0 - abs(vertex.co.z / minimum) * 0.62)
				vertex.co.x *= factor
				vertex.co.y *= 0.72 + factor * 0.28
		obj.data.update()
	return obj


def leaf(name: str, location: tuple[float, float, float], size: tuple[float, float, float],
		color: str, parent: bpy.types.Object, rotation: float = 0.0) -> bpy.types.Object:
	return g.leaf_pad(name, location, size, g.MATS[color], parent, rotation)


def berry(name: str, location: tuple[float, float, float], radius: float,
		color: str, parent: bpy.types.Object) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.data.materials.append(g.MATS[color])
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	obj.parent = parent
	return obj


def dancing_birch() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_dancing_birch")
	paths: list[PathSpec] = [
		([(-0.52, 0.05, 0.10), (-0.72, 0.02, 2.25), (-0.48, 0.00, 4.60), (-0.82, 0.05, 7.20)],
		 [0.34, 0.28, 0.17, 0.045]),
		([(0.00, -0.04, 0.10), (0.16, -0.02, 2.50), (-0.05, 0.00, 5.05), (0.28, -0.04, 7.72)],
		 [0.40, 0.31, 0.19, 0.045]),
		([(0.55, 0.06, 0.10), (0.42, 0.04, 2.10), (0.72, 0.00, 4.22), (1.08, 0.08, 6.65)],
		 [0.31, 0.25, 0.15, 0.040]),
	]
	for index, (start, end) in enumerate((
		((-0.62, 0.0, 2.65), (-1.45, 0.04, 4.15)),
		((-0.52, 0.0, 4.05), (-1.52, 0.02, 5.62)),
		((0.06, 0.0, 3.20), (0.95, -0.04, 4.72)),
		((0.02, 0.0, 5.00), (0.92, 0.03, 6.28)),
		((0.52, 0.0, 2.72), (1.58, 0.05, 3.92)),
		((0.70, 0.0, 4.12), (1.70, -0.02, 5.32)),
	)):
		mid = Vector(start).lerp(Vector(end), 0.52) + Vector((0.0, 0.0, 0.18))
		paths.append(([start, tuple(mid), end], [0.15, 0.09, 0.032]))
	fused_wood("dancing_birch", paths, root, 7, 1.38, 0.24, True, 17)
	leaves = [
		(-1.52, -0.10, 5.62, 0.72, 0.42, "coral"), (-0.82, 0.08, 7.22, 0.72, 0.44, "butter"),
		(0.25, -0.08, 7.74, 0.78, 0.46, "mint"), (1.08, 0.10, 6.66, 0.76, 0.44, "lavender"),
		(1.70, -0.05, 5.30, 0.68, 0.40, "rose"), (-1.48, 0.14, 4.12, 0.60, 0.36, "butter"),
		(1.58, 0.10, 3.92, 0.58, 0.35, "coral"), (-0.10, -0.18, 6.38, 0.58, 0.34, "aqua"),
		(-0.72, 0.18, 6.42, 0.54, 0.34, "rose"), (0.86, 0.18, 5.58, 0.54, 0.34, "butter"),
		(-1.05, -0.08, 5.02, 0.48, 0.31, "lavender"), (1.18, -0.12, 4.52, 0.48, 0.31, "mint"),
	]
	for index, (x, y, z, sx, sz, color) in enumerate(leaves):
		leaf("birch_leaf_%02d" % index, (x, y, z), (sx, 0.30, sz), color, root, 0.16 * index)
	return root


def umbrella_tree() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_umbrella")
	paths: list[PathSpec] = [
		([(-1.25, 0.0, 0.10), (-1.02, 0.02, 1.52), (-0.42, 0.00, 2.78),
		  (0.48, 0.00, 3.78), (0.82, 0.00, 4.62)], [0.64, 0.57, 0.48, 0.34, 0.18]),
	]
	for index, (x, z) in enumerate(((-3.60, 4.72), (-2.05, 5.02), (-0.45, 5.18),
		(1.15, 5.12), (2.72, 4.92), (3.85, 4.58))):
		paths.append(([(0.25, 0.0, 3.65), (x * 0.46, 0.02, 4.35), (x, 0.0, z)],
			[0.30 - index * 0.018, 0.16, 0.045]))
	fused_wood("umbrella_tree", paths, root, 8, 1.85, 0.39, False, 29)
	for index, (x, z, sx) in enumerate(((-3.55, 4.90, 1.20), (-2.05, 5.20, 1.45),
		(-0.48, 5.34, 1.52), (1.08, 5.28, 1.48), (2.64, 5.08, 1.35), (3.82, 4.78, 1.10))):
		cloud("umbrella_crown_%02d" % index, (x, 0.0, z), (sx, 0.78, 0.50),
			("seafoam", "teal", "lavender"), 120 + index, root)
	for index, x in enumerate((-3.18, -1.85, -0.42, 1.02, 2.42, 3.45)):
		leaf("umbrella_leaf_%02d" % index, (x, -0.80, 5.02 + 0.12 * math.sin(index)),
			(0.48, 0.20, 0.25), "aqua" if index % 2 else "mint", root, 0.12 * index)
	return root


def blossom_cloud() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_blossom_cloud")
	paths: list[PathSpec] = [
		([(0.0, 0.0, 0.10), (0.08, 0.0, 1.80), (-0.12, 0.0, 3.32)], [0.56, 0.46, 0.28]),
		([(-0.05, 0.0, 2.42), (-0.92, 0.0, 3.48), (-1.95, 0.04, 4.72)], [0.32, 0.18, 0.035]),
		([(0.02, 0.0, 2.64), (0.78, 0.0, 3.78), (1.82, -0.04, 5.08)], [0.31, 0.17, 0.035]),
		([(-0.12, 0.0, 3.05), (-0.55, 0.02, 4.52), (-0.48, 0.02, 6.10)], [0.26, 0.13, 0.030]),
		([(0.08, 0.0, 3.10), (0.66, -0.02, 4.62), (1.08, -0.02, 6.32)], [0.24, 0.12, 0.030]),
		([(0.44, 0.0, 4.02), (1.82, 0.02, 4.36), (2.68, 0.02, 5.02)], [0.18, 0.10, 0.028]),
		([(-0.55, 0.15, 3.75), (-1.20, 0.72, 4.60), (-1.68, 0.90, 5.30)], [0.16, 0.09, 0.028]),
	]
	fused_wood("blossom_cloud", paths, root, 7, 1.48, 0.31, False, 41)
	clouds = [(-2.08, 4.82, 0.78), (-1.42, 5.42, 0.65), (-0.72, 6.16, 0.70),
		(0.12, 6.54, 0.72), (0.98, 6.34, 0.74), (1.68, 5.62, 0.72),
		(2.58, 5.08, 0.64), (-0.42, 4.92, 0.58), (0.58, 5.08, 0.62), (1.92, 4.62, 0.56)]
	palettes = (("coral", "rose", "lavender"), ("rose", "lavender", "seafoam"),
		("coral", "rose", "butter"))
	for index, (x, z, size) in enumerate(clouds):
		cloud("blossom_crown_%02d" % index, (x, 0.02 * (index % 3), z),
			(size, 0.52, size * 0.70), palettes[index % len(palettes)], 220 + index, root)
	for index, (x, z, color) in enumerate(((-1.72, 5.10, "butter"), (-0.18, 5.78, "cream"),
		(0.72, 6.10, "butter"), (1.52, 5.22, "cream"), (2.18, 4.84, "butter"),
		(-0.82, 4.76, "cream"))):
		berry("blossom_center_%02d" % index, (x, -0.76, z), 0.28, color, root)
	return root


def windswept_tree() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_windswept")
	paths: list[PathSpec] = [
		([(-1.48, 0.0, 0.10), (-1.20, 0.0, 1.48), (-0.48, 0.0, 2.78),
		  (0.58, 0.0, 3.68), (1.68, 0.0, 4.16)], [0.64, 0.57, 0.46, 0.32, 0.14]),
	]
	for index, (start, end) in enumerate((((-0.62, 0.0, 2.62), (2.35, 0.0, 3.22)),
		((-0.15, 0.0, 3.08), (3.18, 0.0, 3.72)), ((0.52, 0.0, 3.58), (4.02, 0.0, 4.22)),
		((1.28, 0.0, 3.96), (4.72, 0.0, 4.72)))):
		mid = Vector(start).lerp(Vector(end), 0.52) + Vector((0.0, 0.02, 0.20))
		paths.append(([start, tuple(mid), end], [0.25 - 0.03 * index, 0.13, 0.032]))
	fused_wood("windswept_tree", paths, root, 7, 1.72, 0.39, False, 53)
	for index, (x, z, sx, color) in enumerate(((1.22, 3.22, 1.10, "mint"),
		(2.32, 3.42, 1.22, "lavender"), (3.42, 3.76, 1.26, "aqua"),
		(4.46, 4.30, 1.10, "seafoam"), (1.58, 4.22, 0.96, "teal"),
		(2.82, 4.52, 1.12, "mint"), (4.00, 4.78, 0.92, "lavender"))):
		cloud("wind_crown_%02d" % index, (x, 0.0, z), (sx, 0.55, 0.42),
			(color, "teal", "lavender"), 280 + index, root)
	return root


def twinheart_tree() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_twinheart")
	left = [(-0.38, 0.0, 0.10), (-0.92, 0.0, 1.65), (-1.32, 0.0, 3.22),
		(-1.08, 0.0, 4.72), (-0.30, 0.0, 5.62), (0.0, 0.0, 4.82)]
	right = [(0.38, 0.0, 0.10), (0.92, 0.0, 1.65), (1.32, 0.0, 3.22),
		(1.08, 0.0, 4.72), (0.30, 0.0, 5.62), (0.0, 0.0, 4.82)]
	paths: list[PathSpec] = [
		(left, [0.50, 0.44, 0.34, 0.24, 0.13, 0.042]),
		(right, [0.50, 0.44, 0.34, 0.24, 0.13, 0.042]),
		([(-0.98, 0.0, 2.34), (-1.92, 0.0, 3.50), (-2.52, 0.0, 4.62)], [0.29, 0.15, 0.034]),
		([(0.98, 0.0, 2.34), (1.92, 0.0, 3.50), (2.52, 0.0, 4.62)], [0.29, 0.15, 0.034]),
		([(-0.78, 0.25, 3.00), (-1.42, 0.78, 4.10), (-1.82, 0.92, 5.02)], [0.19, 0.11, 0.030]),
		([(0.78, -0.25, 3.00), (1.42, -0.78, 4.10), (1.82, -0.92, 5.02)], [0.19, 0.11, 0.030]),
	]
	fused_wood("twinheart_tree", paths, root, 8, 1.78, 0.37, False, 67)
	for index, (x, z, size) in enumerate(((-2.46, 4.82, 0.86), (-1.78, 5.56, 1.00),
		(-0.78, 6.04, 0.92), (0.78, 6.04, 0.92), (1.78, 5.56, 1.00),
		(2.46, 4.82, 0.86), (-1.22, 4.36, 0.72), (1.22, 4.36, 0.72))):
		cloud("heart_crown_%02d" % index, (x, 0.0, z), (size, 0.70, size * 0.76),
			("mint", "teal", "coral"), 320 + index, root)
	for index, (x, z, color) in enumerate(((-2.22, 4.65, "coral"), (-1.34, 5.52, "butter"),
		(0.92, 5.78, "rose"), (2.08, 4.95, "coral"), (1.42, 4.22, "butter"))):
		berry("heart_fruit_%02d" % index, (x, -0.82, z), 0.32, color, root)
	return root


def weeping_willow() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_weeping_willow")
	paths: list[PathSpec] = [
		([(0.0, 0.0, 0.10), (-0.18, 0.0, 1.72), (0.12, 0.0, 3.42), (-0.12, 0.0, 5.08)],
		 [0.68, 0.61, 0.50, 0.31]),
	]
	for index, (x, z) in enumerate(((-2.35, 5.18), (-1.18, 5.82), (0.0, 6.08),
		(1.22, 5.78), (2.38, 5.10))):
		paths.append(([(-0.04, 0.0, 3.72), (x * 0.52, 0.0, 5.02), (x, 0.0, z)],
			[0.29, 0.17, 0.045]))
	fused_wood("weeping_willow", paths, root, 9, 2.02, 0.43, False, 73)
	for index, (x, y, z, sx, sz) in enumerate(((-2.35, 0.0, 4.08, 0.82, 1.58),
		(-1.28, -0.08, 4.48, 0.94, 1.88), (0.0, 0.0, 4.62, 1.00, 2.02),
		(1.30, 0.08, 4.44, 0.94, 1.86), (2.38, 0.0, 4.02, 0.80, 1.54),
		(-1.76, 0.52, 4.15, 0.72, 1.50), (0.72, 0.56, 4.24, 0.72, 1.52),
		(1.82, 0.46, 3.92, 0.66, 1.38))):
		cloud("willow_curtain_%02d" % index, (x, y, z), (sx, 0.64, sz),
			("mint", "teal", "lavender"), 390 + index, root, True)
	# High crown caps keep the top lush while the long tapered masses establish
	# the unmistakable willow silhouette.
	for index, (x, z, sx) in enumerate(((-1.72, 5.72, 1.05), (-0.58, 6.22, 1.16),
		(0.66, 6.20, 1.14), (1.78, 5.68, 1.02))):
		cloud("willow_cap_%02d" % index, (x, 0.02, z), (sx, 0.72, 0.72),
			("seafoam", "teal", "aqua"), 420 + index, root)
	return root


def pine_tier(parent: bpy.types.Object, z: float, radius: float, height: float,
		color: str, seed: int) -> bpy.types.Object:
	sides = 16
	verts = [(0.0, 0.0, z + height)]
	for index in range(sides):
		angle = math.tau * index / sides
		uneven = 1.0 + 0.07 * math.sin(index * 2.6 + seed)
		verts.append((math.cos(angle) * radius * uneven,
			math.sin(angle) * radius * 0.76 * uneven, z - 0.18 - 0.08 * (index % 2)))
	faces = [(0, 1 + index, 1 + (index + 1) % sides) for index in range(sides)]
	faces.append(tuple(reversed(range(1, sides + 1))))
	mesh = bpy.data.meshes.new("celebration_pine_tier_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new("celebration_pine_tier", mesh)
	bpy.context.collection.objects.link(obj)
	for mat_name in (color, "teal", "lavender"):
		obj.data.materials.append(g.MATS[mat_name])
	for polygon in mesh.polygons:
		polygon.material_index = 2 if (polygon.index + seed) % 7 == 0 else (1 if polygon.index % 4 == 0 else 0)
	obj.parent = parent
	return obj


def star(parent: bpy.types.Object, location: tuple[float, float, float], radius: float) -> bpy.types.Object:
	outline = []
	for index in range(10):
		angle = math.pi * 0.5 + index * math.pi / 5.0
		r = radius if index % 2 == 0 else radius * 0.43
		outline.append((math.cos(angle) * r, -0.13, math.sin(angle) * r))
	verts = outline + [(x, 0.13, z) for x, _, z in outline]
	faces = [tuple(range(10)), tuple(reversed(range(10, 20)))]
	faces += [(i, (i + 1) % 10, 10 + (i + 1) % 10, 10 + i) for i in range(10)]
	mesh = bpy.data.meshes.new("celebration_star_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new("celebration_star", mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.data.materials.append(g.MATS["butter"])
	obj.parent = parent
	return obj


def celebration_pine() -> bpy.types.Object:
	root = g.new_root("lagoon_tree_celebration_snow")
	paths: list[PathSpec] = [
		([(0.0, 0.0, 0.10), (0.03, 0.0, 7.25)], [0.46, 0.16]),
	]
	fused_wood("celebration_pine", paths, root, 8, 1.35, 0.29, False, 89)
	for index in range(7):
		z = 1.05 + index * 0.86
		radius = 2.30 - index * 0.27
		pine_tier(root, z, radius, 0.76, "mint" if index % 2 == 0 else "lavender", 440 + index)
		for side in range(3):
			angle = math.tau * side / 3.0 + index * 0.31
			leaf("pine_snow_%02d_%02d" % (index, side),
				(math.cos(angle) * radius * 0.70, math.sin(angle) * radius * 0.53, z + 0.06),
				(0.38 - index * 0.015, 0.24, 0.20), "snow", root, angle)
	for index, (angle, z, radius, color) in enumerate(((0.2, 2.0, 1.88, "coral"),
		(2.5, 2.74, 1.62, "butter"), (4.3, 3.48, 1.40, "rose"),
		(1.1, 4.22, 1.18, "aqua"), (3.1, 4.96, 0.94, "coral"),
		(5.3, 5.68, 0.72, "butter"))):
		berry("pine_ornament_%02d" % index,
			(math.cos(angle) * radius, math.sin(angle) * radius * 0.76, z), 0.34, color, root)
	star(root, (0.0, 0.0, 7.68), 0.64)
	return root


BUILDERS = {
	"lagoon_tree_dancing_birch": dancing_birch,
	"lagoon_tree_umbrella": umbrella_tree,
	"lagoon_tree_blossom_cloud": blossom_cloud,
	"lagoon_tree_windswept": windswept_tree,
	"lagoon_tree_twinheart": twinheart_tree,
	"lagoon_tree_weeping_willow": weeping_willow,
	"lagoon_tree_celebration_snow": celebration_pine,
}


def descendants(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result.extend(descendants(child))
	return result


def export_asset(name: str, root: bpy.types.Object) -> int:
	bpy.ops.object.select_all(action="DESELECT")
	copies: list[bpy.types.Object] = []
	for source in descendants(root):
		if source.type not in {"MESH", "CURVE"}:
			continue
		copy = source.copy()
		copy.data = source.data.copy()
		bpy.context.collection.objects.link(copy)
		copy.parent = None
		copy.matrix_world = source.matrix_world.copy()
		copies.append(copy)
	for copy in copies:
		copy.select_set(True)
		bpy.context.view_layer.objects.active = copy
		if copy.type == "CURVE":
			bpy.ops.object.convert(target="MESH")
			copy.select_set(True)
	bpy.context.view_layer.objects.active = copies[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged.data.validate(clean_customdata=True)
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	bpy.ops.export_scene.gltf(filepath=str(OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False, export_cameras=False, export_lights=False)
	bpy.data.objects.remove(merged, do_unlink=True)
	return triangles


ASSETS = {name: builder() for name, builder in BUILDERS.items()}
for asset_name, asset in ASSETS.items():
	triangles = export_asset(asset_name, asset)
	print("SKY_TREE_GEN3|%s|triangles=%d" % (asset_name, triangles))

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
print("SKY_TREE_GEN3|assets|%d" % len(ASSETS))
print("SKY_TREE_GEN3|blend|%s" % BLEND)
