#!/usr/bin/env python3
"""Build the unified authored Sky Lagoon Mobile art kit.

The generated concept sheet is shape/palette reference only. Runtime assets are
deterministically reconstructed here as editable Blender geometry and exported
as one batched GLB mesh per family.

Usage: blender --background --python tools/build_sky_lagoon_quality_kit.py
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_sky_lagoon_quality_kit"
BLEND_OUT = SOURCE_OUT / "sky_lagoon_quality_kit.blend"
ONLY_ASSET = ""
for argument in sys.argv[1:]:
	if argument.startswith("--only="):
		ONLY_ASSET = argument.split("=", 1)[1]
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"navy": (0.065, 0.075, 0.18, 1.0),
	"plum": (0.24, 0.16, 0.34, 1.0),
	"lavender": (0.55, 0.47, 0.72, 1.0),
	"lavender_light": (0.76, 0.70, 0.86, 1.0),
	"pearl": (0.88, 0.85, 0.78, 1.0),
	"cream": (0.96, 0.91, 0.79, 1.0),
	"gold": (0.91, 0.65, 0.25, 1.0),
	"teal": (0.23, 0.61, 0.62, 1.0),
	"aqua": (0.39, 0.78, 0.78, 1.0),
	"coral": (0.88, 0.43, 0.45, 1.0),
	"rose": (0.80, 0.46, 0.66, 1.0),
	"butter": (0.94, 0.76, 0.34, 1.0),
	"wood": (0.42, 0.25, 0.20, 1.0),
	"wood_light": (0.66, 0.43, 0.30, 1.0),
	"leaf": (0.30, 0.57, 0.36, 1.0),
	"leaf_light": (0.53, 0.70, 0.39, 1.0),
	"pine": (0.16, 0.43, 0.39, 1.0),
	"pine_light": (0.31, 0.60, 0.50, 1.0),
	"water": (0.30, 0.68, 0.76, 1.0),
	"snow": (0.90, 0.95, 0.97, 1.0),
	"rock": (0.46, 0.46, 0.61, 1.0),
	"rock_light": (0.64, 0.62, 0.76, 1.0),
	"warm": (1.0, 0.72, 0.32, 1.0),
	"coal": (0.12, 0.11, 0.16, 1.0),
}


def material(name: str, color: tuple[float, float, float, float], emission: float = 0.0) -> bpy.types.Material:
	mat = bpy.data.materials.new("SLQ_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.88
	bsdf.inputs["Metallic"].default_value = 0.0
	if emission > 0.0:
		bsdf.inputs["Emission Color"].default_value = color
		bsdf.inputs["Emission Strength"].default_value = emission
	return mat


MATS = {name: material(name, color, 1.1 if name == "warm" else 0.0)
	for name, color in PALETTE.items()}


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def assign(obj: bpy.types.Object, mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	obj.data.materials.append(mat)
	obj.parent = parent
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def rounded_box(name: str, loc: tuple[float, float, float], size: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0), radius: float = 0.14) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	bev = obj.modifiers.new("storybook_rounding", "BEVEL")
	bev.width = min(radius, min(size) * 0.18)
	bev.segments = 2
	bev.limit_method = "ANGLE"
	apply_modifier(obj, bev)
	return obj


def cylinder(name: str, loc: tuple[float, float, float], radius: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object, vertices: int = 12,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
		location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	bev = obj.modifiers.new("soft_profile", "BEVEL")
	bev.width, bev.segments = min(radius * 0.14, 0.16), 2
	apply_modifier(obj, bev)
	return obj


def cone(name: str, loc: tuple[float, float, float], bottom: float, top: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object, vertices: int = 12,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=bottom, radius2=top, depth=depth,
		location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	bev = obj.modifiers.new("soft_profile", "BEVEL")
	bev.width, bev.segments = min(max(top, 0.2) * 0.12, 0.13), 2
	apply_modifier(obj, bev)
	return obj


def blob(name: str, loc: tuple[float, float, float], scale: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object, seed: int = 0) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	rng = random.Random(seed)
	for vertex in obj.data.vertices:
		vertex.co *= 0.93 + rng.random() * 0.14
	assign(obj, mat, parent)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def tube(name: str, points: list[tuple[float, float, float]], radius: float,
		mat: bpy.types.Material, parent: bpy.types.Object, cyclic: bool = False) -> bpy.types.Object:
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions, curve.resolution_u = "3D", 2
	curve.bevel_depth, curve.bevel_resolution = radius, 2
	spline = curve.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, co in zip(spline.bezier_points, points):
		point.co = co
		point.handle_left_type = point.handle_right_type = "AUTO"
	spline.use_cyclic_u = cyclic
	obj = bpy.data.objects.new(name, curve)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	curve.materials.append(mat)
	return obj


def panel_xz(name: str, outline: list[tuple[float, float]], depth: float,
		loc: tuple[float, float, float], mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	verts = [(x, -depth * .5, z) for x, z in outline] + [(x, depth * .5, z) for x, z in outline]
	count = len(outline)
	faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, count * 2))]
	faces += [(i, (i + 1) % count, count + (i + 1) % count, count + i) for i in range(count)]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = loc
	assign(obj, mat, parent)
	bev = obj.modifiers.new("rounded_profile", "BEVEL")
	bev.width, bev.segments = min(depth * .26, .12), 2
	apply_modifier(obj, bev)
	return obj


def ring(name: str, loc: tuple[float, float, float], major: float, minor: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=16, minor_segments=6, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return obj


def arch_tube(name: str, center: tuple[float, float, float], radius: float, thickness: float,
		mat: bpy.types.Material, parent: bpy.types.Object, start: float = 0.0, end: float = math.pi,
		segments: int = 12) -> bpy.types.Object:
	cx, cy, cz = center
	points = [(cx + math.cos(start + (end - start) * i / segments) * radius, cy,
		cz + math.sin(start + (end - start) * i / segments) * radius)
		for i in range(segments + 1)]
	return tube(name, points, thickness, mat, parent)


def leaf(name: str, loc: tuple[float, float, float], size: float, mat: bpy.types.Material,
		parent: bpy.types.Object, angle: float = 0.0) -> bpy.types.Object:
	outline = [(0, size), (.48 * size, .25 * size), (.36 * size, -.52 * size),
		(0, -.78 * size), (-.36 * size, -.52 * size), (-.48 * size, .25 * size)]
	obj = panel_xz(name, outline, .12 * size, loc, mat, parent)
	obj.rotation_euler.y = angle
	return obj


def flower(parent: bpy.types.Object, loc: tuple[float, float, float], petal: bpy.types.Material,
		scale: float, seed: int) -> None:
	x, y, z = loc
	cylinder("flower_stem", (x, y, z * .5), .09 * scale, z, MATS["leaf"], parent, 8)
	for index in range(6):
		a = math.tau * index / 6.0
		blob("flower_petal", (x + math.cos(a) * .38 * scale, y + math.sin(a) * .38 * scale, z),
			(.32 * scale, .22 * scale, .18 * scale), petal, parent, seed + index)
	blob("flower_center", (x, y, z + .02), (.23 * scale, .23 * scale, .16 * scale), MATS["butter"], parent, seed + 20)


def blossom(parent: bpy.types.Object, loc: tuple[float, float, float], petal: bpy.types.Material,
		scale: float, seed: int) -> None:
	"""Modeled tree blossom with no ground-reaching stem."""
	x, y, z = loc
	for index in range(5):
		a = math.tau * index / 5.0
		blob("tree_blossom_petal", (x + math.cos(a) * .28 * scale,
			y + math.sin(a) * .28 * scale, z), (.24 * scale, .18 * scale, .13 * scale),
			petal, parent, seed + index)
	blob("tree_blossom_center", (x, y - .03, z + .01),
		(.15 * scale, .15 * scale, .12 * scale), MATS["butter"], parent, seed + 8)


def foliage_rosette(parent: bpy.types.Object, loc: tuple[float, float, float], scale: float,
		primary: bpy.types.Material, secondary: bpy.types.Material, seed: int) -> None:
	"""Broad modeled leaf-scale motif for premium low-poly crown surfaces."""
	x, y, z = loc
	for index in range(7):
		a = math.tau * index / 7.0 + (seed % 5) * .09
		blob("crown_leaf_scale", (x + math.cos(a) * .36 * scale,
			y - .10 - .04 * (index % 2), z + math.sin(a) * .27 * scale),
			(.34 * scale, .20 * scale, .24 * scale),
			primary if index % 3 else secondary, parent, seed + index)
	blob("crown_leaf_heart", (x, y - .13, z), (.40 * scale, .22 * scale, .30 * scale),
		secondary, parent, seed + 9)


def shell_crest(parent: bpy.types.Object, loc: tuple[float, float, float], scale: float,
		mat: bpy.types.Material | None = None) -> None:
	x, y, z = loc
	used = mat or MATS["gold"]
	for index in range(7):
		a = math.radians(-66 + index * 22)
		p = panel_xz("shell_rib", [(0, 0), (-.22 * scale, .75 * scale),
			(0, 1.05 * scale), (.22 * scale, .75 * scale)], .18 * scale,
			(x + math.sin(a) * .42 * scale, y, z + math.cos(a) * .18 * scale), used, parent)
		p.rotation_euler.y = a
	blob("shell_hinge", (x, y, z), (.55 * scale, .35 * scale, .26 * scale), MATS["plum"], parent, 91)


def grounded(parent: bpy.types.Object, radius: float, snowy: bool = False, seed: int = 0) -> None:
	base = MATS["snow"] if snowy else MATS["pearl"]
	blob("grounded_base", (0, 0, .14), (radius, radius * .72, .20), base, parent, seed)
	# A complete planted asset always carries a readable transition into its
	# habitat. Alternating stones avoid the former blank white poker-chip base.
	stone_count = 8 if radius >= 1.7 else 6
	for index in range(stone_count):
		a = math.tau * index / stone_count + seed * .17
		r = radius * (.78 + .05 * (index % 2))
		s = .22 + .07 * ((seed + index) % 3)
		blob("base_stone", (math.cos(a) * r, math.sin(a) * r * .72, .25),
			(s * 1.25, s, s * .72), MATS["rock_light"] if index % 2 else MATS["rock"],
			parent, seed * 19 + index)
	if not snowy and radius >= 1.4:
		for index in range(3):
			a = -1.05 + index * 1.10 + seed * .04
			leaf("base_leaf_litter", (math.cos(a) * radius * .58,
				math.sin(a) * radius * .48, .48), .48 + .08 * (index % 2),
				MATS["pine_light"] if index % 2 else MATS["leaf"], parent, a)


def build_rosette() -> bpy.types.Object:
	p = root("lagoon_baby_rosette")
	grounded(p, 1.25, False, 1)
	for index in range(10):
		a = math.tau * index / 10.0
		obj = leaf("rosette_leaf", (math.cos(a) * .52, math.sin(a) * .52, .42),
			.72 if index % 2 else .92, MATS["teal"] if index % 2 else MATS["leaf_light"], p, a)
		obj.rotation_euler.x = math.radians(20)
	blob("pearl_bud", (0, 0, .82), (.28, .28, .34), MATS["aqua"], p, 17)
	return p


def build_shrub() -> bpy.types.Object:
	p = root("lagoon_meadow_shrub")
	grounded(p, 1.35, False, 2)
	for index, (x, y, s) in enumerate(((-.45, 0, .9), (.35, .12, 1.1), (0, -.35, .75), (.58, -.24, .68))):
		cylinder("shrub_branch", (x * .55, y * .55, .82 * s), .11, 1.6 * s, MATS["wood"], p, 8)
		blob("shrub_crown", (x, y, 1.55 * s), (.72 * s, .62 * s, .48 * s),
			MATS["leaf_light"] if index % 2 else MATS["leaf"], p, 20 + index)
	flower(p, (-.26, -.42, 1.95), MATS["coral"], .55, 60)
	return p


def build_flowers(name: str, coral: bool) -> bpy.types.Object:
	p = root(name)
	grounded(p, 1.45, False, 3 if coral else 4)
	petals = [MATS["coral"], MATS["rose"], MATS["butter"]] if coral else [MATS["lavender"], MATS["aqua"], MATS["rose"]]
	for index, (x, y, h) in enumerate(((-.75, .05, 1.35), (-.25, -.25, 1.75), (.35, .08, 1.45), (.72, -.20, 1.95), (.05, .38, 1.20))):
		flower(p, (x, y, h), petals[index % len(petals)], .68 + .08 * (index % 2), 80 + index * 8)
	return p


def build_mushrooms() -> bpy.types.Object:
	p = root("lagoon_mushroom_cluster")
	grounded(p, 1.5, False, 5)
	for index, (x, y, h, r) in enumerate(((-.65, 0, 1.3, .62), (.08, -.15, 1.9, .82), (.72, .05, 1.05, .55), (.35, .45, .75, .42))):
		cylinder("mushroom_stem", (x, y, h * .5 + .2), r * .30, h, MATS["cream"], p, 10)
		cone("mushroom_cap", (x, y, h + .28), r, r * .18, .52, MATS["coral"] if index != 1 else MATS["lavender"], p, 12)
		for spot in range(3):
			a = math.tau * spot / 3.0 + index
			blob("cap_spot", (x + math.cos(a) * r * .42, y + math.sin(a) * r * .42, h + .48),
				(.09, .09, .055), MATS["cream"], p, 110 + index * 4 + spot)
	return p


def build_reeds() -> bpy.types.Object:
	p = root("lagoon_pond_reeds")
	blob("water_base", (0, 0, .08), (1.55, 1.05, .11), MATS["water"], p, 8)
	for index in range(9):
		x = -1.0 + (index % 5) * .48
		y = -.35 + (index // 5) * .65
		h = 1.7 + (index % 3) * .38
		cylinder("reed_stem", (x, y, h * .5), .055, h, MATS["leaf"], p, 7)
		if index % 2 == 0:
			cone("cattail", (x, y, h + .28), .13, .10, .58, MATS["wood"], p, 8)
		leaf("reed_leaf", (x + .18, y, .72), .60, MATS["pine_light"], p, -.35)
	return p


def build_stones() -> bpy.types.Object:
	p = root("lagoon_river_stones")
	blob("water_edge", (0, .18, .08), (2.15, 1.15, .13), MATS["water"], p, 12)
	for index, (x, y, s) in enumerate(((-1.25, 0, .75), (-.45, -.12, 1.0), (.52, .15, .68), (1.18, -.08, .48), (.15, .50, .42))):
		blob("river_stone", (x, y, .34 * s), (.72 * s, .55 * s, .42 * s),
			MATS["rock_light"] if index % 2 else MATS["rock"], p, 150 + index)
	if True:
		shell_crest(p, (-.45, -.48, .52), .34, MATS["pearl"])
	return p


def build_broadleaf(name: str, variant: int, coral: bool = False) -> bpy.types.Object:
	p = root(name)
	grounded(p, 2.15 + variant * .08, False, 210 + variant)
	lean = (-.22, .18, .32)[variant % 3]
	tube("tree_trunk", [(0, 0, .2), (lean * .35, .03, 1.8),
		(lean, -.08 + variant * .05, 3.7), (lean * .72, 0, 5.0)],
		.46, MATS["wood_light"], p)
	for side in (-1.0, 1.0):
		tube("tree_bough", [(lean * .42, 0, 2.5), (side * (1.15 + .12 * variant), .10, 3.5),
			(side * (1.65 + .16 * variant), .04, 4.35)], .25, MATS["wood"], p)
	canopy_mats = ([MATS["coral"], MATS["rose"]] if coral else
		[MATS["leaf_light"], MATS["leaf"]])
	centers = [(-1.45, .05, 4.6, 1.45), (0, -.05, 5.35, 1.65),
		(1.45, .10, 4.7, 1.35), ((-.45 + variant * .45), .25, 4.2, 1.10)]
	if variant == 1:
		centers += [(2.0, -.10, 5.3, .92)]
	elif variant == 2:
		centers += [(-2.0, -.15, 5.0, .86), (.72, -.12, 5.95, .80)]
	for index, (x, y, z, s) in enumerate(centers):
		blob("tree_crown", (x + lean, y, z), (s, s * .85, s * .70),
			canopy_mats[index % 2], p, 230 + variant * 20 + index)
	for index in range(5 if coral else 3):
		a = math.tau * index / (5 if coral else 3) + variant * .4
		flower(p, (math.cos(a) * 1.45 + lean, math.sin(a) * .55,
			4.7 + .45 * (index % 2)), MATS["cream"] if coral else MATS["rose"], .34, 270 + index)
	return p


def build_willow(name: str, variant: int) -> bpy.types.Object:
	p = root(name)
	blob("shore_base", (0, 0, .10), (2.25, 1.55, .14), MATS["water"], p, 300 + variant)
	lean = -.48 if variant == 0 else .52
	tube("willow_trunk", [(0, 0, .2), (lean * .4, 0, 1.8), (lean, .05, 3.5),
		(lean * 1.25, 0, 4.65)], .48, MATS["wood_light"], p)
	for index in range(5):
		a = math.radians(-105 + index * 52 + variant * 11)
		x = lean + math.cos(a) * 1.55
		y = math.sin(a) * .58
		tube("willow_bough", [(lean * .8, 0, 3.7), (x * .75, y, 4.35), (x, y, 4.65)],
			.20, MATS["wood"], p)
		for drop in range(4):
			dx = x + (drop - 1.5) * .28
			dz = 4.8 - drop * .42 - .12 * (index % 2)
			leaf("willow_leaf", (dx, y, dz), .64, MATS["aqua"] if drop % 2 else MATS["teal"], p, .08 * drop)
	return p


def build_pine(name: str, variant: int, snowy: bool = False, decorated: bool = False) -> bpy.types.Object:
	p = root(name)
	grounded(p, 2.0, snowy, 340 + variant)
	lean = (-.18, .12, .28, 0.0)[variant % 4]
	tube("pine_trunk", [(0, 0, .2), (lean * .45, 0, 2.8), (lean, 0, 5.8)], .34,
		MATS["wood_light"], p)
	for tier in range(5):
		z = 1.45 + tier * 1.08
		radius = 2.0 - tier * .28 + (.12 if variant % 2 else 0)
		for side in range(8):
			a = math.tau * side / 8.0 + tier * .21 + variant * .13
			x = lean * (z / 5.8) + math.cos(a) * radius * .62
			y = math.sin(a) * radius * .48
			leaf("pine_branch", (x, y, z), radius * .72,
				MATS["pine_light"] if (tier + side + variant) % 3 == 0 else MATS["pine"], p, a)
			if snowy and side % 2 == tier % 2:
				blob("snow_pad", (x, y - .03, z + .27),
					(radius * .34, radius * .22, .13), MATS["snow"], p, 370 + tier * 10 + side)
	if decorated:
		for index in range(12):
			a = math.tau * index / 12.0
			z = 1.8 + (index % 4) * 1.05
			r = 1.55 - (index % 4) * .25
			blob("tree_ornament", (math.cos(a) * r + lean * z / 5.8, math.sin(a) * r * .55, z),
				(.18, .18, .18), [MATS["gold"], MATS["coral"], MATS["aqua"], MATS["lavender"]][index % 4], p, 410 + index)
		panel_xz("tree_star", [(0, .68), (.16, .21), (.65, .21), (.26, -.08),
			(.40, -.62), (0, -.30), (-.40, -.62), (-.26, -.08), (-.65, .21), (-.16, .21)],
			.20, (lean, 0, 6.45), MATS["gold"], p)
	return p


# Every lagoon tree below has a different trunk graph and crown profile.  The
# older broadleaf/pine helpers remain useful for historical rebuilds, but the
# shipped twelve-tree roster deliberately does not count recolours as variants.
def build_ancient_oak() -> bpy.types.Object:
	p = root("lagoon_tree_meadow_a")
	grounded(p, 2.55, False, 500)
	for index, end in enumerate(((-2.05, -.35, .24), (-1.25, .65, .20),
		(1.15, .70, .20), (2.15, -.30, .22))):
		tube("oak_radial_root", [(0, 0, .20), end], .24 - index * .018, MATS["wood"], p)
	tube("oak_hollow_trunk", [(0, 0, .18), (-.12, 0, 2.25), (-.42, .02, 4.05)],
		.68, MATS["wood_light"], p)
	for side, z in ((-1.0, 3.05), (1.0, 3.25), (-1.0, 4.05), (1.0, 4.20)):
		tube("oak_heavy_bough", [(-.18, 0, z - .45), (side * 1.30, .04, z),
			(side * 2.35, -.02, z + .35)], .30, MATS["wood"], p)
	ring("oak_hollow", (-.06, -.64, 1.95), .39, .12, MATS["plum"], p,
		(math.pi * .5, 0, 0))
	for index, (x, z, sx, sz) in enumerate(((-2.30, 4.55, 1.45, .82), (-.90, 5.20, 1.55, .95),
		(.75, 5.28, 1.60, .98), (2.15, 4.65, 1.35, .78), (.15, 4.35, 1.85, .74))):
		blob("oak_crown", (x, .03 * (index % 2), z), (sx, 1.03, sz),
			MATS["leaf_light"] if index % 2 else MATS["leaf"], p, 510 + index)
	for index, (x, y, z, s) in enumerate(((-3.0, -.15, 4.55, .56), (-2.05, -.55, 5.25, .62),
		(-.95, -.72, 5.78, .58), (.35, -.70, 5.95, .62), (1.55, -.55, 5.42, .57),
		(2.90, -.12, 4.65, .52), (1.65, .56, 4.28, .50), (-1.45, .58, 4.18, .52))):
		blob("oak_leaf_cluster", (x, y, z), (s, s * .72, s * .58),
			MATS["leaf_light"] if index % 3 == 0 else MATS["leaf"], p, 518 + index)
	for index, loc in enumerate(((-2.25, -.92, 4.72), (.20, -.98, 5.72), (2.10, -.88, 4.82))):
		blossom(p, loc, MATS["cream"], .56, 540 + index * 8)
	for index, loc in enumerate(((-2.55, -1.02, 4.45), (-1.35, -1.08, 5.20),
		(-.15, -1.12, 5.58), (1.10, -1.06, 5.20), (2.35, -.98, 4.52),
		(-.55, -.98, 4.48), (1.00, -.96, 4.42))):
		foliage_rosette(p, loc, .72, MATS["leaf"], MATS["leaf_light"], 560 + index * 12)
	return p


def build_dancing_birch() -> bpy.types.Object:
	p = root("lagoon_tree_meadow_b")
	grounded(p, 1.62, False, 520)
	tube("birch_main", [(0, 0, .18), (.18, 0, 2.10), (-.28, .02, 4.15),
		(.12, 0, 6.50)], .30, MATS["cream"], p)
	for side, top in ((-1.0, 6.25), (1.0, 6.78)):
		tube("birch_fork", [(-.10, 0, 3.65), (side * .72, .02, 5.15),
			(side * 1.10, 0, top)], .18, MATS["wood_light"], p)
	for index, (x, z, tilt) in enumerate(((.08, 1.15, -8), (.11, 1.82, 9), (-.12, 2.55, -5),
		(-.20, 3.42, 8), (-.12, 4.28, -10), (.05, 5.08, 6))):
		rounded_box("birch_bark_mark", (x, -.31, z), (.42, .10, .11), MATS["plum"], p,
			rotation=(0, math.radians(tilt), 0), radius=.035)
	for side, z in ((-1.0, 2.75), (1.0, 3.35), (-1.0, 4.35), (1.0, 4.85)):
		tube("birch_dancing_bough", [(-.12, 0, z), (side * .52, .03, z + .55),
			(side * 1.18, 0, z + .82)], .11, MATS["wood_light"], p)
		blob("birch_bough_leaves", (side * 1.23, 0, z + .88), (.52, .42, .66),
			MATS["leaf_light"], p, 548 + int(z * 10))
	for index, (x, z, sx, sz) in enumerate(((-1.08, 6.25, .78, 1.10), (-.22, 6.92, .82, 1.28),
		(.82, 6.52, .86, 1.18), (.10, 5.55, .72, .95))):
		blob("birch_oval_crown", (x, 0, z), (sx, .66, sz),
			MATS["leaf_light"] if index % 2 else MATS["leaf"], p, 530 + index)
	for index, loc in enumerate(((-1.15, -.68, 6.02), (-.58, -.72, 6.78),
		(.05, -.74, 7.22), (.72, -.70, 6.52), (.16, -.66, 5.62))):
		foliage_rosette(p, loc, .58, MATS["leaf_light"], MATS["leaf"], 590 + index * 12)
	return p


def build_umbrella_acacia() -> bpy.types.Object:
	p = root("lagoon_tree_meadow_c")
	blob("acacia_shore_base", (0, 0, .10), (3.05, 1.55, .15), MATS["water"], p, 540)
	tube("acacia_swept_trunk", [(-1.35, 0, .18), (-.85, 0, 1.65), (.10, 0, 3.05),
		(1.20, 0, 3.70)], .42, MATS["wood_light"], p)
	for end_x in (-2.25, -.70, 1.85, 2.80):
		tube("acacia_lateral", [(0, 0, 2.85), (end_x * .48, .02, 3.52),
			(end_x, 0, 3.88)], .21, MATS["wood"], p)
	for index, (x, z, sx) in enumerate(((-2.10, 4.05, 1.35), (-.55, 4.35, 1.55),
		(1.10, 4.28, 1.60), (2.45, 4.08, 1.20))):
		blob("acacia_flat_crown", (x, 0, z), (sx, .88, .46),
			MATS["leaf"] if index % 2 else MATS["leaf_light"], p, 550 + index)
	for index, (x, y, z, sx) in enumerate(((-2.85, -.25, 3.88, .62), (-1.62, -.58, 4.38, .76),
		(-.15, -.62, 4.56, .82), (1.38, -.58, 4.47, .78), (2.90, -.24, 3.92, .58),
		(-.85, .55, 4.18, .68), (1.75, .52, 4.12, .64))):
		blob("acacia_leaf_pad", (x, y, z), (sx, sx * .68, .28),
			MATS["leaf_light"] if index % 2 else MATS["leaf"], p, 556 + index)
	for index, loc in enumerate(((-2.55, -.82, 4.02), (-1.42, -.90, 4.42),
		(-.20, -.94, 4.58), (1.05, -.92, 4.50), (2.28, -.84, 4.05))):
		foliage_rosette(p, loc, .62, MATS["leaf_light"], MATS["leaf"], 610 + index * 12)
	return p


def build_airy_cherry() -> bpy.types.Object:
	p = root("lagoon_tree_coral_a")
	grounded(p, 2.05, False, 560)
	tube("cherry_trunk", [(0, 0, .18), (.05, 0, 2.10), (.28, 0, 3.65)], .36,
		MATS["wood_light"], p)
	for index, (side, z, end_x, end_z) in enumerate(((-1, 2.25, -1.75, 4.65),
		(1, 2.45, 1.65, 5.05), (-1, 3.15, -.65, 5.70), (1, 3.25, 2.35, 4.55))):
		tube("cherry_fine_fork", [(.12, 0, z), (side * .55, .02, z + .82),
			(end_x, 0, end_z)], .14 + .025 * (index % 2), MATS["wood"], p)
	for index, (x, z, s) in enumerate(((-1.75, 4.78, .82), (-.72, 5.58, .72),
		(.30, 6.00, .88), (1.32, 5.25, .78), (2.28, 4.68, .68), (.38, 4.48, .64))):
		blob("cherry_blossom_cloud", (x, 0, z), (s, s * .72, s * .58),
			MATS["coral"] if index % 2 else MATS["rose"], p, 570 + index)
	for index, loc in enumerate(((-2.10, -.70, 4.72), (-1.28, -.78, 5.48),
		(-.25, -.82, 5.95), (.82, -.80, 5.42), (1.82, -.74, 4.96), (2.48, -.52, 4.55),
		(.25, .62, 4.62), (-.92, .55, 4.92))):
		blossom(p, loc, MATS["cream"] if index % 3 == 0 else MATS["coral"],
			.55, 590 + index * 8)
	for index, loc in enumerate(((-1.78, -.78, 4.90), (-.88, -.84, 5.55),
		(.15, -.88, 5.92), (1.10, -.84, 5.22), (2.05, -.76, 4.72), (.35, -.80, 4.52))):
		foliage_rosette(p, loc, .55, MATS["coral"], MATS["rose"], 680 + index * 12)
	return p


def build_windswept_rose() -> bpy.types.Object:
	p = root("lagoon_tree_coral_b")
	grounded(p, 2.35, False, 580)
	tube("rose_swept_trunk", [(-1.35, 0, .18), (-1.02, 0, 1.45), (-.20, 0, 2.65),
		(1.25, 0, 3.42)], .40, MATS["wood_light"], p)
	for index, (x, z) in enumerate(((.45, 3.12), (1.62, 3.55), (2.72, 3.95), (3.45, 4.35))):
		tube("rose_flag_branch", [(-.05 + index * .28, 0, 2.52 + index * .18),
			(x, .02, z), (x + .62, 0, z + .15)], .16, MATS["wood"], p)
	for index, (x, z, sx) in enumerate(((.15, 3.35, .70), (1.25, 3.72, .92),
		(2.35, 4.08, 1.02), (3.42, 4.38, .78))):
		blob("rose_windswept_crown", (x, 0, z), (sx, .70, .56),
			MATS["rose"] if index % 2 else MATS["coral"], p, 590 + index)
		for bud in range(3):
			blossom(p, (x + (bud - 1) * sx * .42, -.62,
				z + .20 * (bud % 2)), MATS["cream"] if bud == 1 else MATS["rose"],
				.46, 600 + index * 32 + bud * 8)
	for index, loc in enumerate(((.25, -.86, 3.38), (1.18, -.90, 3.72),
		(2.20, -.88, 4.02), (3.20, -.78, 4.32))):
		foliage_rosette(p, loc, .56, MATS["rose"], MATS["coral"], 740 + index * 12)
	return p


def build_heart_orchard() -> bpy.types.Object:
	p = root("lagoon_tree_coral_c")
	grounded(p, 2.05, False, 620)
	for side in (-1.0, 1.0):
		tube("heart_twin_trunk", [(side * .40, 0, .18), (side * .58, 0, 2.25),
			(side * 1.05, 0, 4.20)], .34, MATS["wood_light"], p)
		tube("heart_inward_branch", [(side * .52, 0, 2.75), (side * .18, 0, 3.62),
			(0, 0, 4.22)], .18, MATS["wood"], p)
	blob("heart_left_crown", (-1.08, 0, 4.78), (1.45, 1.05, 1.55), MATS["coral"], p, 630)
	blob("heart_right_crown", (1.08, 0, 4.78), (1.45, 1.05, 1.55), MATS["rose"], p, 631)
	blob("heart_lower_point", (0, 0, 4.05), (1.18, .92, 1.15), MATS["coral"], p, 632)
	for index, (x, y, z, s) in enumerate(((-1.75, -.45, 5.25, .52), (-.78, -.70, 5.85, .58),
		(.78, -.70, 5.85, .58), (1.75, -.45, 5.25, .52), (-1.42, .52, 4.42, .48),
		(1.42, .52, 4.42, .48), (0, -.74, 3.78, .50))):
		blob("heart_blossom_cluster", (x, y, z), (s, s * .76, s * .62),
			MATS["rose"] if index % 2 else MATS["coral"], p, 635 + index)
	for index, loc in enumerate(((-1.10, -.98, 5.22), (1.08, -.98, 5.22), (0, -.94, 4.05))):
		blossom(p, loc, MATS["cream"], .55, 650 + index * 8)
	for index, loc in enumerate(((-1.65, -.98, 5.22), (-.92, -1.04, 5.72),
		(-.30, -1.06, 5.08), (.30, -1.06, 5.08), (.92, -1.04, 5.72),
		(1.65, -.98, 5.22), (-1.05, -.98, 4.42), (1.05, -.98, 4.42),
		(0, -1.02, 3.90))):
		foliage_rosette(p, loc, .54, MATS["coral"], MATS["rose"], 780 + index * 12)
	return p


def build_domed_willow() -> bpy.types.Object:
	p = root("lagoon_tree_willow_a")
	blob("willow_pool", (0, 0, .10), (2.75, 2.00, .15), MATS["water"], p, 640)
	tube("willow_dome_trunk", [(0, 0, .18), (-.12, 0, 2.10), (.25, 0, 4.25)],
		.46, MATS["wood_light"], p)
	for index in range(7):
		a = math.tau * index / 7.0
		x, y = math.cos(a) * 2.15, math.sin(a) * 1.20
		tube("willow_dome_bough", [(.10, 0, 3.15), (x * .58, y * .55, 4.65),
			(x, y, 4.42)], .18, MATS["wood"], p)
		for drop in range(4):
			leaf("willow_curtain", (x + (drop - 1.5) * .16, y, 4.12 - drop * .52),
				.78, MATS["aqua"] if drop % 2 else MATS["teal"], p, a)
			blob("willow_leaf_knot", (x + (drop - 1.5) * .16, y - .24,
				4.15 - drop * .52), (.26, .18, .36),
				MATS["teal"] if drop % 2 else MATS["aqua"], p, 650 + index * 5 + drop)
	for index in range(6):
		a = math.tau * index / 6.0
		blob("willow_lily_pad", (math.cos(a) * 1.72, math.sin(a) * 1.05, .26),
			(.38, .28, .06), MATS["leaf_light"], p, 690 + index)
	for index, loc in enumerate(((-1.95, -.95, 3.72), (-1.25, -1.00, 4.42),
		(-.38, -1.02, 4.62), (.48, -1.02, 4.58), (1.30, -1.0, 4.30),
		(2.02, -.92, 3.62), (-.80, -.96, 3.42), (.92, -.96, 3.35))):
		foliage_rosette(p, loc, .54, MATS["teal"], MATS["aqua"], 850 + index * 12)
	return p


def build_crescent_willow() -> bpy.types.Object:
	p = root("lagoon_tree_willow_b")
	blob("crescent_pool", (.55, 0, .10), (3.25, 1.55, .15), MATS["water"], p, 660)
	tube("crescent_trunk", [(-1.70, 0, .18), (-1.45, 0, 1.75), (-.72, 0, 3.35),
		(.55, 0, 4.35), (2.25, 0, 4.10), (3.20, 0, 3.35)], .40, MATS["wood_light"], p)
	for index, (x, z, length) in enumerate(((-.45, 4.18, 1.45), (.85, 4.55, 1.95),
		(2.10, 4.16, 1.65), (3.12, 3.45, 1.15))):
		tube("crescent_drop_bough", [(x, 0, z), (x + .22, 0, z - length)],
			.12, MATS["wood"], p)
		for drop in range(3):
			leaf("crescent_ribbon", (x + .16 * drop, 0, z - .35 - drop * length * .30),
				.72, MATS["teal"] if index % 2 else MATS["aqua"], p, .10)
			blob("crescent_leaf_knot", (x + .16 * drop, -.20,
				z - .35 - drop * length * .30), (.24, .16, .34),
				MATS["aqua"] if index % 2 else MATS["teal"], p, 705 + index * 4 + drop)
	for index in range(5):
		a = -.45 + index * .52
		blob("crescent_lily_pad", (.40 + math.cos(a) * 1.95, math.sin(a) * .82, .27),
			(.40, .28, .06), MATS["leaf_light"], p, 725 + index)
	for index, loc in enumerate(((-.45, -.80, 4.15), (.55, -.84, 4.48),
		(1.48, -.82, 4.32), (2.30, -.76, 3.92), (3.00, -.68, 3.28),
		(.90, -.78, 3.52))):
		foliage_rosette(p, loc, .50, MATS["aqua"], MATS["teal"], 950 + index * 12)
	return p


def build_lagoon_cypress() -> bpy.types.Object:
	p = root("lagoon_tree_evergreen")
	grounded(p, 1.55, False, 680)
	tube("cypress_trunk", [(0, 0, .18), (-.08, 0, 3.20), (.18, 0, 6.75)], .28,
		MATS["wood_light"], p)
	for tier, (z, width, offset) in enumerate(((1.45, 1.15, -.12), (2.28, 1.45, .18),
		(3.18, 1.08, -.22), (4.08, 1.30, .12), (5.02, .86, -.08), (5.82, .62, .10))):
		for side in (-1.0, 1.0):
			tube("cypress_pagoda_arm", [(offset, 0, z), (offset + side * width * .68, 0, z - .08),
				(offset + side * width, 0, z + .10)], .11, MATS["wood"], p)
			leaf("cypress_layer", (offset + side * width * .72, 0, z + .10), width * .78,
				MATS["pine_light"] if tier % 2 else MATS["pine"], p, side * .08)
		blob("cypress_center_mass", (offset, .05, z + .18),
			(width * .52, .48, .42), MATS["pine"] if tier % 2 else MATS["pine_light"],
			p, 740 + tier)
	cone("cypress_spire", (.18, 0, 6.55), .52, .04, 1.55, MATS["pine_light"], p, 9)
	for index, loc in enumerate(((-.62, -.56, 1.62), (.60, -.56, 2.32),
		(-.55, -.55, 3.22), (.52, -.55, 4.12), (-.36, -.52, 5.05), (.28, -.50, 5.78))):
		foliage_rosette(p, loc, .43, MATS["pine"], MATS["pine_light"], 1030 + index * 12)
	return p


def build_alpine_spruce() -> bpy.types.Object:
	p = root("lagoon_tree_alpine_a")
	grounded(p, 2.45, True, 700)
	tube("spruce_stout_trunk", [(0, 0, .18), (0, 0, 6.45)], .42, MATS["wood_light"], p)
	for tier in range(6):
		z = 1.25 + tier * .92
		width = 2.35 - tier * .31
		for side in range(8):
			a = math.tau * side / 8.0 + tier * .13
			x, y = math.cos(a) * width * .62, math.sin(a) * width * .44
			leaf("spruce_dense_skirt", (x, y, z), width * .82, MATS["pine"], p, a)
			if side % 2 == tier % 2:
				blob("spruce_snow_shelf", (x, y - .03, z + .30),
					(width * .38, width * .25, .15), MATS["snow"], p, 710 + tier * 8 + side)
	cone("spruce_snow_cap", (0, 0, 6.36), .65, .04, 1.45, MATS["snow"], p, 9)
	for index, loc in enumerate(((-1.62, -.88, 1.42), (-.55, -.94, 2.02),
		(.72, -.94, 2.55), (1.48, -.86, 3.02), (-1.12, -.86, 3.48),
		(.58, -.82, 4.02), (-.58, -.76, 4.82), (.22, -.68, 5.58))):
		foliage_rosette(p, loc, .48, MATS["pine"], MATS["pine_light"], 1120 + index * 12)
	return p


def build_crooked_fir() -> bpy.types.Object:
	p = root("lagoon_tree_alpine_b")
	grounded(p, 1.82, True, 770)
	tube("fir_crooked_trunk", [(0, 0, .18), (.15, 0, 1.65), (-.30, 0, 3.35),
		(.32, 0, 5.10), (.62, 0, 7.10)], .28, MATS["wood_light"], p)
	for tier, (z, side, width) in enumerate(((1.72, -1, 1.45), (2.58, 1, 1.75),
		(3.48, -1, 1.25), (4.38, 1, 1.45), (5.38, -1, .98), (6.18, 1, .72))):
		base_x = (-.30 if z < 4.2 else .38)
		tube("fir_sparse_arm", [(base_x, 0, z), (base_x + side * width, 0, z + .08)],
			.13, MATS["wood"], p)
		for twig in range(3):
			x = base_x + side * width * (.35 + twig * .28)
			leaf("fir_sparse_needles", (x, 0, z + .12), .68 - twig * .08,
				MATS["pine_light"] if tier % 2 else MATS["pine"], p, side * .12)
		blob("fir_uneven_snow", (base_x + side * width * .70, -.02, z + .34),
			(width * .34, .33, .13), MATS["snow"], p, 780 + tier)
		# Short counter-boughs keep the silhouette botanical while preserving the
		# deliberately crooked, wind-pruned profile.
		var_side = -side
		tube("fir_counter_arm", [(base_x, .06, z + .22),
			(base_x + var_side * width * .48, .06, z + .34)], .09, MATS["wood"], p)
		leaf("fir_counter_needles", (base_x + var_side * width * .38, .06, z + .42),
			.50, MATS["pine_light"], p, var_side * .12)
	for index, loc in enumerate(((-1.10, -.58, 1.92), (.92, -.58, 2.72),
		(-.82, -.58, 3.62), (1.05, -.58, 4.48), (-.52, -.56, 5.42),
		(.62, -.54, 6.18))):
		foliage_rosette(p, loc, .42, MATS["pine"], MATS["pine_light"], 1230 + index * 12)
	return p


def build_spiral_celebration_pine() -> bpy.types.Object:
	p = root("lagoon_tree_alpine_decorated")
	grounded(p, 2.05, True, 800)
	tube("celebration_trunk", [(0, 0, .18), (.08, 0, 6.55)], .30, MATS["wood_light"], p)
	spiral_points: list[tuple[float, float, float]] = []
	for index in range(37):
		t = index / 36.0
		a = math.tau * 3.15 * t
		radius = 1.78 * (1.0 - t * .76)
		spiral_points.append((math.cos(a) * radius, math.sin(a) * radius * .62, 1.20 + t * 5.10))
	tube("celebration_helical_bough", spiral_points, .20, MATS["pine"], p)
	for index in range(15):
		t = index / 14.0
		a = math.tau * 3.15 * t
		radius = 1.78 * (1.0 - t * .76)
		x, y, z = math.cos(a) * radius, math.sin(a) * radius * .62, 1.20 + t * 5.10
		leaf("celebration_spiral_needles", (x, y, z), .82 - t * .24,
			MATS["pine_light"] if index % 2 else MATS["pine"], p, a)
		if index % 2 == 0:
			blob("celebration_ornament", (x, y - .18, z - .22), (.18, .18, .18),
				[MATS["gold"], MATS["coral"], MATS["aqua"], MATS["lavender"]][index % 4], p, 820 + index)
	panel_xz("celebration_star", [(0, .68), (.16, .21), (.65, .21), (.26, -.08),
		(.40, -.62), (0, -.30), (-.40, -.62), (-.26, -.08), (-.65, .21), (-.16, .21)],
		.20, (.08, 0, 7.02), MATS["gold"], p)
	for index, (x, y, mat) in enumerate(((-1.05, -.45, MATS["lavender"]),
		(.85, -.38, MATS["aqua"]), (1.35, .30, MATS["coral"]))):
		rounded_box("celebration_gift", (x, y, .36), (.62, .62, .62), mat, p, radius=.09)
		rounded_box("celebration_ribbon", (x, y - .33, .36), (.13, .04, .68), MATS["gold"], p, radius=.02)
	for index, loc in enumerate(((-1.18, -.64, 1.72), (.82, -.66, 2.35),
		(-.68, -.64, 3.02), (.62, -.62, 3.72), (-.48, -.58, 4.45),
		(.38, -.54, 5.18), (-.24, -.48, 5.82))):
		foliage_rosette(p, loc, .42, MATS["pine"], MATS["pine_light"], 1320 + index * 12)
	return p


def build_cloud(name: str, variant: int) -> bpy.types.Object:
	p = root(name)
	for index, (x, y, z, s) in enumerate(((-1.25, 0, .05, 1.15), (-.25, .08, .35, 1.5),
		(.85, -.03, .18, 1.25), (1.65, .04, -.02, .76))):
		blob("cloud_puff", (x + variant * .08 * index, y, z),
			(s, s * .68, s * .58), MATS["snow"] if index % 2 else MATS["pearl"], p, 450 + variant * 8 + index)
	return p


def build_memory_frame() -> bpy.types.Object:
	p = root("lagoon_memory_frame")
	rounded_box("frame_back", (0, .10, 3.5), (5.2, .42, 7.0), MATS["plum"], p, radius=.22)
	for x in (-2.65, 2.65):
		rounded_box("frame_pillar", (x, -.05, 3.5), (.46, .60, 7.2), MATS["lavender_light"], p, radius=.16)
		rounded_box("gold_inlay", (x * .93, -.37, 3.5), (.12, .12, 6.4), MATS["gold"], p, radius=.04)
	rounded_box("frame_top", (0, -.05, 7.1), (5.9, .68, .62), MATS["pearl"], p, radius=.18)
	rounded_box("frame_base", (0, -.05, .22), (6.0, 1.05, .44), MATS["lavender"], p, radius=.20)
	arch_tube("frame_arch", (0, -.43, 5.7), 2.3, .20, MATS["gold"], p, 0, math.pi)
	shell_crest(p, (0, -.48, 7.38), .72, MATS["gold"])
	for side in (-1, 1):
		for band, mat in enumerate((MATS["coral"], MATS["butter"], MATS["aqua"])):
			arch_tube("rainbow_corner", (side * 1.65, -.45, .35), .40 + band * .16, .10, mat, p, 0, math.pi)
	return p


def build_lantern() -> bpy.types.Object:
	p = root("lagoon_story_lantern")
	grounded(p, .72, False, 13)
	cone("lantern_pedestal", (0, 0, .7), .62, .38, 1.25, MATS["plum"], p, 10)
	rounded_box("gold_band", (0, 0, 1.38), (.88, .88, .20), MATS["gold"], p, radius=.06)
	cylinder("lantern_post", (0, 0, 2.9), .22, 3.0, MATS["navy"], p, 10)
	for side in (-1, 1):
		tube("lantern_hook", [(0, 0, 4.15), (side * .65, 0, 4.75), (side * 1.05, 0, 4.35)],
			.12, MATS["gold"], p)
		cone("lantern_cap", (side * 1.05, 0, 4.28), .54, .14, .42, MATS["lavender"], p, 10)
		blob("lantern_core", (side * 1.05, 0, 3.88), (.42, .34, .52), MATS["warm"], p, 480 + int(side))
		ring("lantern_cage", (side * 1.05, 0, 3.88), .48, .07, MATS["navy"], p, (math.pi * .5, 0, 0))
	shell_crest(p, (0, -.04, 4.55), .56, MATS["pearl"])
	return p


def build_rainbow_arch() -> bpy.types.Object:
	p = root("lagoon_rainbow_race_arch")
	for side in (-1, 1):
		blob("cloud_foot", (side * 3.2, 0, .5), (1.25, .78, .62), MATS["pearl"], p, 500 + int(side))
	for band, mat in enumerate((MATS["coral"], MATS["butter"], MATS["leaf_light"], MATS["aqua"], MATS["lavender"])):
		arch_tube("rainbow_band", (0, 0, .8), 3.45 - band * .35, .20, mat, p, 0, math.pi)
	return p


def build_butterfly_gate() -> bpy.types.Object:
	p = root("lagoon_butterfly_world_gate")
	grounded(p, 4.0, False, 14)
	for side in (-1.0, 1.0):
		rounded_box("gate_pier", (side * 2.85, 0, 2.8), (.62, 1.0, 5.6), MATS["plum"], p, radius=.24)
		wing = panel_xz("butterfly_wing", [(0, 0), (side * 2.6, .7), (side * 3.2, 3.1),
			(side * 1.9, 4.4), (side * .55, 3.55)], .40, (side * .35, .10, 3.4),
			MATS["coral"] if side < 0 else MATS["aqua"], p)
		wing.rotation_euler.y = side * .06
		panel_xz("wing_inset", [(0, 0), (side * 1.85, .7), (side * 2.25, 2.65),
			(side * 1.25, 3.35), (side * .40, 2.75)], .46, (side * .35, .08, 3.45),
			MATS["rose"] if side < 0 else MATS["teal"], p)
		for z in (.75, 1.55):
			blob("gate_flower", (side * 3.05, -.12, z), (.48, .38, .30),
				MATS["coral"] if z < 1 else MATS["lavender_light"], p, 530 + int(z * 10) + int(side))
	arch_tube("gate_inner", (0, -.14, 2.1), 2.7, .34, MATS["gold"], p, 0, math.pi)
	arch_tube("gate_outer", (0, .04, 2.1), 3.15, .30, MATS["navy"], p, 0, math.pi)
	blob("butterfly_body", (0, -.12, 6.0), (.48, .42, .58), MATS["plum"], p, 540)
	for side in (-1, 1):
		tube("antenna", [(side * .12, -.12, 6.35), (side * .45, -.12, 6.85),
			(side * .72, -.12, 6.72)], .07, MATS["gold"], p)
	return p


def build_bench() -> bpy.types.Object:
	p = root("lagoon_park_bench")
	for x in (-2.2, 2.2):
		cone("bench_foot", (x, 0, .32), .40, .28, .60, MATS["lavender"], p, 10)
		rounded_box("bench_arm", (x, 0, 1.45), (.28, .75, 2.4), MATS["gold"], p, radius=.10)
	for index in range(3):
		rounded_box("bench_seat", (0, -.28 + index * .28, 1.18), (4.6, .22, .34), MATS["teal"], p, radius=.12)
	for index in range(3):
		rounded_box("bench_back", (0, .25, 2.0 + index * .42), (4.6, .22, .30), MATS["teal"], p, radius=.12)
	shell_crest(p, (0, .12, 2.95), .48, MATS["pearl"])
	return p


def build_hedge() -> bpy.types.Object:
	p = root("lagoon_park_hedge")
	blob("hedge_base", (0, 0, .15), (3.6, 1.0, .18), MATS["pearl"], p, 560)
	for index in range(7):
		x = -2.7 + index * .9
		blob("hedge_crown", (x, 0, .95 + .12 * (index % 2)), (.82, .72, .72),
			MATS["leaf"] if index % 2 else MATS["leaf_light"], p, 570 + index)
		if index % 2 == 0:
			flower(p, (x, -.56, 1.48), MATS["rose"] if index % 4 else MATS["cream"], .30, 580 + index)
	return p


def build_fountain() -> bpy.types.Object:
	p = root("lagoon_park_fountain")
	cylinder("fountain_pool", (0, 0, .42), 3.35, .78, MATS["lavender_light"], p, 20)
	cylinder("fountain_water", (0, 0, .84), 2.85, .18, MATS["water"], p, 20)
	cone("fountain_pedestal", (0, 0, 1.65), 1.25, .78, 1.55, MATS["pearl"], p, 14)
	cylinder("fountain_bowl", (0, 0, 2.55), 1.75, .34, MATS["lavender_light"], p, 18)
	cylinder("fountain_water_top", (0, 0, 2.75), 1.42, .12, MATS["water"], p, 18)
	cone("fountain_column", (0, 0, 3.45), .48, .28, 1.40, MATS["pearl"], p, 12)
	shell_crest(p, (0, -.04, 4.18), .85, MATS["gold"])
	for side in (-1, 1):
		tube("water_arc", [(0, 0, 3.55), (side * 1.35, 0, 3.15), (side * 2.0, 0, 1.15)],
			.07, MATS["aqua"], p)
	return p


def build_gatehouse() -> bpy.types.Object:
	p = root("lagoon_entry_gatehouse")
	for side in (-1, 1):
		x = side * 5.0
		cone("gate_tower_base", (x, 0, 2.6), 2.25, 2.0, 5.2, MATS["lavender_light"], p, 14)
		cylinder("tower_belt", (x, 0, 4.0), 2.18, .48, MATS["gold"], p, 14)
		cone("tower_roof", (x, 0, 6.25), 2.65, .22, 3.9, MATS["lavender"], p, 14)
		blob("roof_finial", (x, 0, 8.3), (.30, .30, .42), MATS["gold"], p, 600 + int(side))
		rounded_box("gate_window", (x, -2.05, 3.0), (1.0, .22, 1.75), MATS["aqua"], p, radius=.22)
	arch_tube("welcome_arch", (0, 0, 4.15), 4.65, .48, MATS["plum"], p, 0, math.pi)
	arch_tube("welcome_inlay", (0, -.14, 4.15), 4.05, .20, MATS["gold"], p, 0, math.pi)
	shell_crest(p, (0, -.12, 8.05), .92, MATS["pearl"])
	return p


def build_slide() -> bpy.types.Object:
	p = root("lagoon_play_slide")
	for side in (-1, 1):
		rounded_box("slide_post", (side * 1.05, 1.8, 2.8), (.28, .28, 5.6), MATS["navy"], p, radius=.10)
		for step in range(6):
			rounded_box("ladder_step", (side * .78, 1.65 - step * .30, .55 + step * .62),
				(.25, 1.4, .16), MATS["gold"], p, radius=.06)
	# A broad curved chute reads from gameplay distance.
	for index in range(9):
		t = index / 8.0
		y = .85 - t * 5.2
		z = 5.0 * (1.0 - t) ** 1.45 + .28
		rounded_box("slide_chute", (0, y, z), (2.4, .82, .28),
			MATS["aqua"] if index % 2 else MATS["lavender_light"], p,
			rotation=(math.radians(20 + t * 28), 0, 0), radius=.14)
	for side in (-1, 1):
		tube("slide_rail", [(side * 1.2, 1.4, 5.2), (side * 1.2, -1.4, 3.8),
			(side * 1.2, -4.3, .75)], .12, MATS["gold"], p)
	shell_crest(p, (0, 1.55, 5.55), .52, MATS["coral"])
	return p


def build_swing() -> bpy.types.Object:
	p = root("lagoon_play_swing")
	for side in (-1, 1):
		for y in (-1.75, 1.75):
			tube("swing_leg", [(side * 2.7, y, .15), (side * 1.8, y, 5.6)], .22,
				MATS["teal"] if y < 0 else MATS["lavender"], p)
	rounded_box("swing_beam", (0, 0, 5.7), (6.3, .48, .48), MATS["gold"], p, radius=.16)
	for seat_x in (-1.2, 1.2):
		for side in (-.55, .55):
			tube("swing_chain", [(seat_x + side, 0, 5.45), (seat_x + side, 0, 1.85)], .06, MATS["gold"], p)
		rounded_box("swing_seat", (seat_x, 0, 1.65), (1.35, 1.0, .22),
			MATS["coral"] if seat_x < 0 else MATS["aqua"], p, radius=.12)
	return p


def build_seesaw() -> bpy.types.Object:
	p = root("lagoon_play_seesaw")
	grounded(p, 1.45, False, 22)
	cone("seesaw_pivot", (0, 0, 1.05), 1.0, .45, 1.8, MATS["lavender"], p, 12)
	rounded_box("seesaw_beam", (0, 0, 2.0), (7.0, .72, .38), MATS["teal"], p,
		rotation=(0, math.radians(-7), 0), radius=.16)
	for side in (-1, 1):
		rounded_box("seesaw_seat", (side * 2.75, 0, 2.0 - side * .34), (1.4, 1.25, .22),
			MATS["coral"] if side < 0 else MATS["butter"], p, radius=.12)
		tube("seesaw_handle", [(side * 2.35, -.5, 2.2 - side * .34),
			(side * 2.35, -.5, 3.05 - side * .34), (side * 2.85, -.5, 3.05 - side * .34)],
			.09, MATS["gold"], p)
	return p


def build_merry() -> bpy.types.Object:
	p = root("lagoon_play_merry")
	cylinder("merry_base", (0, 0, .35), 3.2, .62, MATS["lavender"], p, 20)
	cylinder("merry_deck", (0, 0, .72), 2.75, .24, MATS["butter"], p, 20)
	cylinder("merry_pole", (0, 0, 1.9), .22, 2.5, MATS["plum"], p, 10)
	ring("merry_rail", (0, 0, 2.15), 2.15, .13, MATS["gold"], p)
	for index in range(8):
		a = math.tau * index / 8.0
		tube("merry_spoke", [(0, 0, 2.15), (math.cos(a) * 2.15, math.sin(a) * 2.15, 2.15)],
			.09, MATS["gold"], p)
	shell_crest(p, (0, 0, 3.35), .42, MATS["pearl"])
	return p


def build_sandbox() -> bpy.types.Object:
	p = root("lagoon_play_sandbox")
	for index in range(12):
		a = math.tau * index / 12.0
		mat = [MATS["coral"], MATS["butter"], MATS["aqua"], MATS["lavender"]][index % 4]
		rounded_box("sandbox_segment", (math.cos(a) * 2.65, math.sin(a) * 2.65, .42),
			(1.45, .78, .72), mat, p, rotation=(0, 0, a), radius=.18)
	cylinder("sandbox_sand", (0, 0, .28), 2.55, .30, MATS["cream"], p, 20)
	for index in range(7):
		a = math.tau * index / 7.0
		blob("sandbox_ball", (math.cos(a) * 1.35, math.sin(a) * 1.1, .72), (.45, .45, .45),
			[MATS["coral"], MATS["aqua"], MATS["lavender"], MATS["butter"]][index % 4], p, 640 + index)
	return p


def build_spring_horse() -> bpy.types.Object:
	p = root("lagoon_play_spring_horse")
	grounded(p, 1.35, False, 24)
	for turn in range(6):
		a = turn * math.pi * .72
		tube("spring", [(math.cos(a) * .22, math.sin(a) * .22, .45 + turn * .28),
			(math.cos(a + .7) * .22, math.sin(a + .7) * .22, .72 + turn * .28)],
			.09, MATS["navy"], p)
	blob("horse_body", (0, 0, 2.85), (1.65, .58, .92), MATS["coral"], p, 660)
	blob("horse_head", (.95, 0, 3.75), (.70, .52, .82), MATS["coral"], p, 661)
	for side in (-1, 1):
		leaf("horse_ear", (1.02 + side * .24, 0, 4.45), .36, MATS["lavender"], p, side * .20)
		cylinder("horse_leg", (side * .72, 0, 2.15), .16, 1.05, MATS["plum"], p, 8)
	tube("horse_tail", [(-1.25, 0, 3.05), (-1.95, 0, 3.35), (-1.75, 0, 2.55)], .16, MATS["aqua"], p)
	rounded_box("horse_seat", (-.25, 0, 3.72), (1.15, 1.0, .22), MATS["butter"], p, radius=.12)
	return p


def build_station() -> bpy.types.Object:
	p = root("lagoon_train_station")
	rounded_box("station_platform", (0, 0, .30), (12.0, 4.6, .60), MATS["lavender_light"], p, radius=.20)
	for x in (-5.1, 5.1):
		cone("station_foot", (x, 0, .75), .45, .32, .90, MATS["plum"], p, 10)
		cylinder("station_post", (x, 0, 3.55), .24, 5.3, MATS["navy"], p, 10)
		blob("station_finial", (x, 0, 6.42), (.30, .30, .36), MATS["gold"], p, 700 + int(x))
	for x in (-2.6, 0, 2.6):
		cylinder("station_support", (x, .9, 3.5), .16, 5.1, MATS["teal"], p, 10)
	# Scalloped canopy: alternating broad roof pads create a shell rhythm.
	for index in range(9):
		x = -5.0 + index * 1.25
		mat = MATS["pearl"] if index % 2 else MATS["lavender_light"]
		rounded_box("station_canopy", (x, 0, 6.1 - abs(index - 4) * .08),
			(1.42, 5.2, .42), mat, p, rotation=(0, math.radians((index - 4) * 2.0), 0), radius=.18)
	for bx in (-2.6, 2.6):
		rounded_box("station_bench", (bx, .75, 1.45), (3.6, 1.1, .30), MATS["wood_light"], p, radius=.12)
		rounded_box("station_back", (bx, 1.20, 2.25), (3.6, .24, 1.35), MATS["teal"], p, radius=.12)
	shell_crest(p, (0, -2.62, 6.7), .76, MATS["gold"])
	return p


def build_track_tie() -> bpy.types.Object:
	p = root("lagoon_track_tie")
	rounded_box("wood_sleeper", (0, 0, .14), (4.8, 1.0, .28), MATS["wood_light"], p, radius=.12)
	for x in (-1.55, 1.55):
		rounded_box("rail_chair", (x, 0, .40), (.62, .72, .26), MATS["lavender"], p, radius=.10)
		for y in (-.25, .25):
			blob("gold_spike", (x, y, .62), (.10, .10, .14), MATS["gold"], p, 720 + int((x + y) * 10))
	return p


def build_engine() -> bpy.types.Object:
	p = root("lagoon_train_engine")
	rounded_box("engine_frame", (0, 0, 1.85), (4.6, 9.2, .72), MATS["navy"], p, radius=.16)
	cylinder("engine_boiler", (0, -1.0, 4.05), 1.75, 5.3, MATS["teal"], p, 16,
		rotation=(math.pi * .5, 0, 0))
	for y in (-2.8, -1.0, .8):
		ring("boiler_band", (0, y, 4.05), 1.78, .13, MATS["gold"], p, (math.pi * .5, 0, 0))
	cylinder("smokebox", (0, -3.85, 4.05), 1.88, .52, MATS["plum"], p, 16,
		rotation=(math.pi * .5, 0, 0))
	blob("headlamp", (0, -4.22, 4.35), (.48, .28, .48), MATS["warm"], p, 730)
	cone("funnel", (0, -2.55, 6.35), 1.10, .62, 2.2, MATS["navy"], p, 14)
	blob("steam_dome", (0, .25, 5.85), (.72, .72, .82), MATS["gold"], p, 731)
	rounded_box("engine_cab", (0, 2.75, 4.45), (4.5, 3.2, 5.0), MATS["teal"], p, radius=.24)
	for x in (-2.3, 2.3):
		rounded_box("cab_window", (x, 2.7, 4.85), (.22, 1.45, 1.72), MATS["warm"], p, radius=.18)
	rounded_box("cab_roof", (0, 2.75, 7.10), (5.25, 3.85, .48), MATS["lavender"], p, radius=.22)
	for index in range(5):
		x = -2.3 + index * 1.15
		tube("cowcatcher", [(x, -4.35, 1.8), (x * 1.28, -5.25, .75)], .11, MATS["gold"], p)
	rounded_box("cowcatcher_bar", (0, -5.28, .74), (5.8, .30, .28), MATS["plum"], p, radius=.10)
	shell_crest(p, (0, -4.35, 5.25), .56, MATS["pearl"])
	return p


def build_tender() -> bpy.types.Object:
	p = root("lagoon_train_tender")
	rounded_box("tender_frame", (0, 0, 1.85), (4.6, 6.5, .72), MATS["navy"], p, radius=.16)
	rounded_box("tender_box", (0, 0, 3.45), (4.35, 6.1, 2.7), MATS["lavender"], p, radius=.24)
	for side in (-1, 1):
		rounded_box("tender_gold_rail", (side * 2.22, 0, 4.55), (.14, 6.0, .20), MATS["gold"], p, radius=.05)
	for index in range(9):
		x = -1.4 + (index % 3) * 1.4
		y = -1.8 + (index // 3) * 1.8
		blob("tender_coal", (x, y, 4.95), (.55, .55, .42), MATS["coal"], p, 750 + index)
	shell_crest(p, (0, -3.12, 3.65), .48, MATS["gold"])
	return p


def build_coach() -> bpy.types.Object:
	p = root("lagoon_train_coach")
	rounded_box("coach_frame", (0, 0, 1.85), (4.7, 8.9, .72), MATS["navy"], p, radius=.16)
	rounded_box("coach_floor", (0, 0, 2.4), (4.6, 8.5, .32), MATS["cream"], p, radius=.14)
	for x in (-2.15, 2.15):
		for y in (-3.8, 0, 3.8):
			cylinder("coach_post", (x, y, 5.15), .18, 5.2, MATS["teal"], p, 10)
		rounded_box("coach_low_wall", (x, 0, 3.35), (.30, 8.2, 1.55), MATS["lavender"], p, radius=.12)
	for y in (-4.1, 4.1):
		rounded_box("coach_end", (0, y, 4.75), (4.5, .34, 4.7), MATS["teal"], p, radius=.18)
		rounded_box("coach_window", (0, y - math.copysign(.19, y), 5.25), (2.2, .12, 1.65), MATS["warm"], p, radius=.20)
	for side in (-1, 1):
		rounded_box("coach_bench", (side * 1.25, 0, 3.05), (1.25, 6.4, .30), MATS["wood_light"], p, radius=.12)
	for index in range(9):
		x = -2.45 + index * .61
		rounded_box("coach_roof_course", (x, 0, 8.0 - abs(index - 4) * .06),
			(.72, 9.3, .42), MATS["lavender"] if index % 2 else MATS["lavender_light"], p, radius=.16)
	shell_crest(p, (0, -4.45, 8.35), .50, MATS["gold"])
	return p


def build_gondola() -> bpy.types.Object:
	p = root("lagoon_train_gondola")
	rounded_box("gondola_frame", (0, 0, 1.85), (4.7, 8.1, .72), MATS["navy"], p, radius=.16)
	rounded_box("gondola_floor", (0, 0, 2.45), (4.45, 7.7, .38), MATS["cream"], p, radius=.14)
	for x in (-2.15, 2.15):
		rounded_box("gondola_side", (x, 0, 3.5), (.32, 7.7, 2.0), MATS["aqua"], p, radius=.14)
		for y in (-2.6, 0, 2.6):
			rounded_box("gondola_gold", (x * 1.01, y, 3.6), (.12, .22, 1.7), MATS["gold"], p, radius=.05)
	for y in (-3.8, 3.8):
		rounded_box("gondola_end", (0, y, 3.5), (4.5, .32, 2.0), MATS["teal"], p, radius=.14)
	rounded_box("gondola_cushion", (0, 0, 2.95), (2.8, 3.0, .55), MATS["rose"], p, radius=.22)
	shell_crest(p, (0, -3.95, 4.18), .42, MATS["pearl"])
	return p


def build_caboose() -> bpy.types.Object:
	p = root("lagoon_train_caboose")
	rounded_box("caboose_frame", (0, 0, 1.85), (4.7, 8.1, .72), MATS["navy"], p, radius=.16)
	rounded_box("caboose_house", (0, .65, 4.35), (4.35, 5.4, 4.8), MATS["coral"], p, radius=.24)
	for x in (-2.18, 2.18):
		rounded_box("caboose_window", (x, .65, 4.65), (.14, 1.5, 1.55), MATS["warm"], p, radius=.18)
	rounded_box("caboose_roof", (0, .65, 6.95), (5.2, 6.2, .52), MATS["lavender"], p, radius=.22)
	rounded_box("cupola", (0, .65, 7.55), (2.2, 2.4, 1.15), MATS["teal"], p, radius=.18)
	rounded_box("cupola_roof", (0, .65, 8.3), (2.75, 2.9, .36), MATS["gold"], p, radius=.16)
	for x in (-2.05, 2.05):
		for y in (-3.65, -2.65):
			cylinder("balcony_post", (x, y, 3.35), .13, 2.0, MATS["gold"], p, 8)
		tube("balcony_rail", [(x, -4.0, 3.9), (x, -2.2, 3.9)], .10, MATS["gold"], p)
	rounded_box("balcony_end", (0, -4.0, 3.9), (4.2, .18, .20), MATS["gold"], p, radius=.07)
	shell_crest(p, (0, -2.12, 7.15), .46, MATS["pearl"])
	return p


def build_bridge() -> bpy.types.Object:
	p = root("lagoon_castle_bridge")
	# Sixty-unit sleeve covers the retained analytic bridge collision.
	for index in range(20):
		y = -28.5 + index * 3.0
		z = .18 + .55 * math.sin(math.pi * index / 19.0)
		rounded_box("bridge_paver", (0, y, z), (13.6, 2.9, .55),
			MATS["lavender_light"] if index % 2 else MATS["pearl"], p, radius=.18)
	for side in (-1, 1):
		for index in range(8):
			y = -28.0 + index * 8.0
			z = .85 + .55 * math.sin(math.pi * index / 7.0)
			cylinder("bridge_post", (side * 7.0, y, z + 1.65), .32, 3.3, MATS["plum"], p, 10)
			blob("bridge_pearl", (side * 7.0, y, z + 3.5), (.42, .42, .42), MATS["pearl"], p, 790 + index + int(side))
		points = []
		for index in range(15):
			y = -28.0 + index * 4.0
			z = 2.35 + .75 * math.sin(math.pi * index / 14.0)
			points.append((side * 7.0, y, z))
		tube("bridge_rail", points, .18, MATS["gold"], p)
	for y in (-28.5, 28.5):
		shell_crest(p, (0, y - math.copysign(1.55, y), 1.25), .72, MATS["gold"])
	return p


def build_castle() -> bpy.types.Object:
	p = root("lagoon_pearl_castle")
	front_y, back_y = -14.4, 30.0
	# A complete outer shell wraps the older procedural structure. The central
	# upper opening is intentionally empty: Godot mounts the protected Mermaid
	# Roshan stained glass at its original byte-identical runtime position.
	rounded_box("castle_foundation", (0, 7.0, 2.1), (70.0, 47.0, 4.2), MATS["lavender"], p, radius=.35)
	for x in (-24.0, 24.0):
		rounded_box("front_wing", (x, front_y, 24.0), (22.0, 3.0, 43.0), MATS["pearl"], p, radius=.36)
	# Lintel between the entrance and the protected glass opening.
	rounded_box("front_mid_lintel", (0, front_y, 27.0), (24.0, 3.0, 4.0), MATS["lavender_light"], p, radius=.28)
	# Upper crown deliberately leaves a 22x28 central window aperture.
	for x in (-19.0, 19.0):
		rounded_box("glass_side_pier", (x, front_y - .2, 43.0), (14.0, 3.2, 32.0), MATS["pearl"], p, radius=.32)
	rounded_box("glass_top", (0, front_y - .2, 59.0), (24.0, 3.2, 4.0), MATS["pearl"], p, radius=.30)
	rounded_box("castle_back", (0, back_y, 28.0), (70.0, 3.0, 52.0), MATS["lavender_light"], p, radius=.36)
	for x in (-34.0, 34.0):
		rounded_box("castle_side", (x, 7.5, 28.0), (3.0, 45.0, 52.0), MATS["lavender_light"], p, radius=.36)
	# Four strongly authored towers and roofs establish the silhouette.
	for index, (x, y) in enumerate(((-32, -8), (32, -8), (-32, 24), (32, 24))):
		cone("castle_tower", (x, y, 26.5), 7.2, 6.5, 49.0, MATS["lavender_light"], p, 16)
		cylinder("tower_gold_belt", (x, y, 43.5), 7.1, 1.25, MATS["gold"], p, 16)
		cone("tower_roof", (x, y, 57.0), 8.3, .35, 25.5, MATS["lavender"], p, 16)
		cylinder("tower_roof_gold_rim", (x, y, 44.7), 8.0, .62, MATS["gold"], p, 16)
		blob("tower_finial", (x, y, 70.2), (.62, .62, .86), MATS["gold"], p, 820 + index)
		if y < 0:
			rounded_box("tower_window", (x, front_y - 1.7, 31.0), (3.4, .32, 7.5), MATS["aqua"], p, radius=.34)
			arch_tube("tower_window_hood", (x, front_y - 1.95, 34.0), 2.0, .28, MATS["gold"], p, 0, math.pi)
	# Central crown repeats the shell language without competing with the glass.
	rounded_box("crown_keep", (0, 8.0, 67.0), (24.0, 24.0, 17.0), MATS["pearl"], p, radius=.34)
	cone("crown_roof", (0, 8.0, 82.0), 14.5, .35, 14.0, MATS["lavender"], p, 14)
	cylinder("crown_roof_gold_rim", (0, 8.0, 75.1), 14.0, .72, MATS["gold"], p, 14)
	blob("crown_pearl", (0, 8.0, 89.5), (1.0, 1.0, 1.25), MATS["gold"], p, 830)
	rounded_box("crown_window", (0, front_y - 1.85, 69.0), (5.8, .42, 8.2), MATS["aqua"], p, radius=.48)
	arch_tube("crown_window_hood", (0, front_y - 2.10, 71.4), 3.5, .38, MATS["gold"], p, 0, math.pi)
	# Deep gold-and-plum lancet surround for the protected stained glass.
	for x in (-12.2, 12.2):
		rounded_box("stained_glass_jamb", (x, front_y - 2.05, 42.0), (1.35, 1.6, 27.5), MATS["gold"], p, radius=.20)
		obj = rounded_box("stained_glass_hood", (x * .50, front_y - 2.05, 58.0),
			(1.35, 1.6, 16.2), MATS["gold"], p, radius=.20)
		obj.rotation_euler.y = math.radians(52.0 if x > 0 else -52.0)
	arch_tube("stained_glass_plum_arch", (0, front_y - 2.15, 47.0), 12.0, .62, MATS["plum"], p, 0, math.pi)
	shell_crest(p, (0, front_y - 2.35, 62.5), 1.65, MATS["gold"])
	# Child-readable entrance remains physically aligned with the retained door.
	for x in (-9.6, 9.6):
		rounded_box("door_pier", (x, front_y - 1.8, 12.0), (2.5, 2.0, 24.0), MATS["lavender"], p, radius=.28)
	arch_tube("door_arch", (0, front_y - 1.95, 18.0), 9.4, 1.15, MATS["lavender"], p, 0, math.pi)
	arch_tube("door_gold_inlay", (0, front_y - 2.20, 18.0), 7.9, .30, MATS["gold"], p, 0, math.pi)
	# Broad buttresses, pearl caps and restrained coral/aqua banners.
	for x in (-23.5, 23.5):
		cone("front_buttress", (x, front_y - 2.1, 11.5), 4.2, 2.4, 22.0, MATS["lavender"], p, 12)
		blob("buttress_pearl", (x, front_y - 2.1, 23.0), (.72, .72, .72), MATS["pearl"], p, 850 + int(x))
		rounded_box("castle_banner", (x, front_y - 2.55, 34.0), (4.2, .28, 10.0),
			MATS["coral"] if x < 0 else MATS["teal"], p, radius=.16)
		shell_crest(p, (x, front_y - 2.78, 38.2), .50, MATS["gold"])
	# Broad modeled façade courses and pearl capitals keep the architecture rich
	# at Mobile distance without relying on texture noise.
	for z in (7.0, 22.5, 49.0):
		for x in (-23.5, 23.5):
			rounded_box("facade_belt", (x, front_y - 1.72, z), (22.5, .70, .92),
				MATS["lavender"] if z != 22.5 else MATS["gold"], p, radius=.18)
	for x in (-14.0, 14.0):
		cone("glass_capital", (x, front_y - 2.0, 26.5), 1.35, .85, 2.4, MATS["pearl"], p, 12)
		blob("glass_cap_pearl", (x, front_y - 2.0, 28.0), (.68, .68, .68), MATS["pearl"], p, 860 + int(x))
	for step in range(4):
		rounded_box("castle_entry_step", (0, front_y - 3.4 - step * .95, .35 + step * .30),
			(18.0 - step * 1.8, 2.4, .60), MATS["lavender_light"] if step % 2 else MATS["pearl"], p, radius=.20)
	for x in range(-28, 29, 7):
		blob("battlement_pearl", (float(x), front_y - .4, 53.6), (.58, .58, .62),
			MATS["pearl"], p, 870 + x)
	return p


def build_snowbank() -> bpy.types.Object:
	p = root("lagoon_snowbank")
	for index, (x, y, s) in enumerate(((-1.15, 0, 1.0), (-.25, .08, 1.25), (.75, -.05, .92), (1.45, .10, .60))):
		blob("snowbank", (x, y, .32 * s), (.92 * s, .72 * s, .44 * s),
			MATS["snow"] if index % 2 else MATS["pearl"], p, 880 + index)
	return p


def build_chalet(name: str, variant: int) -> bpy.types.Object:
	p = root(name)
	# Open-front wrapper preserves the existing walk-in room and cutaway system.
	rounded_box("chalet_back", (0, 5.7, 4.2), (15.4, 1.0, 8.4), MATS["cream"], p, radius=.24)
	for x in (-7.2, 7.2):
		rounded_box("chalet_side", (x, 0, 4.2), (1.0, 11.5, 8.4), MATS["cream"], p, radius=.24)
	for x in (-5.4, 5.4):
		rounded_box("chalet_front", (x, -5.6, 4.2), (4.4, 1.0, 8.4), MATS["cream"], p, radius=.24)
	# Timber frame and generous snow roof.
	for x in (-6.6, 0, 6.6):
		rounded_box("chalet_beam", (x, -6.18, 4.5), (.48, .48, 8.2), MATS["wood"], p, radius=.10)
	rounded_box("chalet_crossbeam", (0, -6.18, 7.65), (14.2, .48, .48), MATS["wood"], p, radius=.10)
	for course in range(7):
		x = -7.6 + course * 2.55
		z = 9.1 + (3 - abs(course - 3)) * 1.3
		rounded_box("roof_course", (x, 0, z), (2.8, 14.6, .72),
			[MATS["teal"], MATS["lavender"], MATS["coral"]][variant], p,
			rotation=(0, math.radians((course - 3) * 9.0), 0), radius=.20)
		blob("roof_snow", (x, -.15, z + .52), (1.55, 6.8, .34), MATS["snow"], p, 900 + variant * 10 + course)
	for x in (-4.5, 4.5):
		rounded_box("warm_window", (x, -6.32, 4.85), (2.5, .20, 2.7), MATS["warm"], p, radius=.28)
		arch_tube("window_hood", (x, -6.48, 5.65), 1.35, .18, MATS["gold"], p, 0, math.pi)
	rounded_box("chalet_step", (0, -6.4, .42), (6.0, 2.0, .72), MATS["lavender_light"], p, radius=.18)
	shell_crest(p, (0, -6.42, 8.4), .62, MATS["gold"])
	return p


def build_cave() -> bpy.types.Object:
	p = root("lagoon_alpine_cave")
	grounded(p, 10.5, True, 33)
	# Layered rock blobs form a deep, irregular arch rather than a black box.
	for index, (x, y, z, sx, sz) in enumerate(((-8.5, 0, 4.0, 4.2, 4.8), (-6.0, .5, 9.0, 4.4, 5.2),
		(-2.7, .8, 13.0, 4.2, 4.8), (1.0, .5, 14.8, 4.8, 5.0), (5.2, .3, 12.2, 4.4, 5.2),
		(8.2, 0, 7.0, 4.0, 5.0), (9.0, .2, 3.0, 3.8, 4.2))):
		blob("cave_rock", (x, y, z), (sx, 4.2, sz),
			MATS["rock_light"] if index % 2 else MATS["rock"], p, 930 + index)
	# Snow cap shelves and a plum recess around the preserved portal/star.
	for index, (x, z, sx) in enumerate(((-7.0, 8.5, 3.4), (-2.5, 14.7, 3.1), (2.0, 16.8, 3.5), (6.2, 12.8, 3.0))):
		blob("cave_snow", (x, -.45, z), (sx, 3.2, .55), MATS["snow"], p, 950 + index)
	arch_tube("cave_recess", (0, -4.1, 5.0), 5.7, .75, MATS["plum"], p, 0, math.pi)
	for side in (-1, 1):
		blob("cave_crystal", (side * 6.6, -4.0, 2.0), (.7, .7, 2.0),
			MATS["aqua"] if side < 0 else MATS["lavender_light"], p, 960 + int(side))
	return p


def build_gifts() -> bpy.types.Object:
	p = root("lagoon_alpine_gifts")
	for index, (x, y, s, mat) in enumerate(((-1.2, 0, 1.0, MATS["coral"]), (.2, .1, .82, MATS["teal"]), (1.2, -.05, .72, MATS["lavender"]))):
		rounded_box("gift_box", (x, y, .55 * s), (1.15 * s, 1.15 * s, 1.1 * s), mat, p, radius=.15)
		rounded_box("gift_ribbon", (x, y, .58 * s), (.20 * s, 1.23 * s, 1.18 * s), MATS["gold"], p, radius=.05)
		blob("gift_bow", (x - .20 * s, y, 1.22 * s), (.30 * s, .18 * s, .18 * s), MATS["gold"], p, 980 + index)
		blob("gift_bow", (x + .20 * s, y, 1.22 * s), (.30 * s, .18 * s, .18 * s), MATS["gold"], p, 990 + index)
	return p


def build_snowman() -> bpy.types.Object:
	p = root("lagoon_alpine_snowman")
	grounded(p, 1.55, True, 44)
	blob("snowman_body", (0, 0, 1.25), (1.1, .9, 1.25), MATS["snow"], p, 1000)
	blob("snowman_head", (0, 0, 3.05), (.78, .68, .78), MATS["pearl"], p, 1001)
	cone("carrot", (0, -.72, 3.08), .20, .02, .72, MATS["coral"], p, 8, (math.pi * .5, 0, 0))
	cylinder("hat", (0, 0, 4.0), .85, .24, MATS["plum"], p, 12)
	cylinder("hat_top", (0, 0, 4.45), .55, .90, MATS["navy"], p, 12)
	tube("scarf", [(-.70, 0, 2.55), (0, -.75, 2.50), (.70, 0, 2.55)], .18, MATS["coral"], p)
	return p


def build_cairn() -> bpy.types.Object:
	p = root("lagoon_alpine_cairn")
	grounded(p, 1.05, True, 45)
	for index in range(4):
		blob("cairn_stone", (0, 0, .55 + index * .72),
			(1.0 - index * .17, .72 - index * .09, .42),
			MATS["rock_light"] if index % 2 else MATS["rock"], p, 1020 + index)
	panel_xz("cairn_glow", [(0, .78), (.18, .20), (.72, 0), (.18, -.20), (0, -.78),
		(-.18, -.20), (-.72, 0), (-.18, .20)], .18, (0, -.48, 3.7), MATS["warm"], p)
	return p


BUILDERS = {
	"lagoon_baby_rosette": build_rosette,
	"lagoon_meadow_shrub": build_shrub,
	"lagoon_flower_cluster_coral": lambda: build_flowers("lagoon_flower_cluster_coral", True),
	"lagoon_flower_cluster_lavender": lambda: build_flowers("lagoon_flower_cluster_lavender", False),
	"lagoon_mushroom_cluster": build_mushrooms,
	"lagoon_pond_reeds": build_reeds,
	"lagoon_river_stones": build_stones,
	"lagoon_story_lantern": build_lantern,
	"lagoon_memory_frame": build_memory_frame,
	"lagoon_rainbow_race_arch": build_rainbow_arch,
	"lagoon_butterfly_world_gate": build_butterfly_gate,
	"lagoon_train_station": build_station,
	"lagoon_snowbank": build_snowbank,
	"lagoon_park_bench": build_bench,
	"lagoon_park_hedge": build_hedge,
	"lagoon_park_fountain": build_fountain,
	"lagoon_entry_gatehouse": build_gatehouse,
	"lagoon_play_slide": build_slide,
	"lagoon_play_swing": build_swing,
	"lagoon_play_seesaw": build_seesaw,
	"lagoon_play_merry": build_merry,
	"lagoon_play_sandbox": build_sandbox,
	"lagoon_play_spring_horse": build_spring_horse,
	"lagoon_track_tie": build_track_tie,
	"lagoon_train_engine": build_engine,
	"lagoon_train_tender": build_tender,
	"lagoon_train_coach": build_coach,
	"lagoon_train_gondola": build_gondola,
	"lagoon_train_caboose": build_caboose,
	"lagoon_castle_bridge": build_bridge,
	"lagoon_pearl_castle": build_castle,
	"lagoon_alpine_chalet_a": lambda: build_chalet("lagoon_alpine_chalet_a", 0),
	"lagoon_alpine_chalet_b": lambda: build_chalet("lagoon_alpine_chalet_b", 1),
	"lagoon_alpine_chalet_c": lambda: build_chalet("lagoon_alpine_chalet_c", 2),
	"lagoon_alpine_cave": build_cave,
	"lagoon_alpine_gifts": build_gifts,
	"lagoon_alpine_snowman": build_snowman,
	"lagoon_alpine_cairn": build_cairn,
	"lagoon_cloud_0": lambda: build_cloud("lagoon_cloud_0", 0),
	"lagoon_cloud_1": lambda: build_cloud("lagoon_cloud_1", 1),
	"lagoon_cloud_2": lambda: build_cloud("lagoon_cloud_2", 2),
}

ASSETS = {name: builder() for name, builder in BUILDERS.items()
	if ONLY_ASSET == "" or ONLY_ASSET == name}


SPECIAL_OUT = {
	"lagoon_cloud_0": ROOT / "assets" / "art35" / "landmarks" / "cloud_0.glb",
	"lagoon_cloud_1": ROOT / "assets" / "art35" / "landmarks" / "cloud_1.glb",
	"lagoon_cloud_2": ROOT / "assets" / "art35" / "landmarks" / "cloud_2.glb",
}


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result += family(child)
	return result


def export_asset(name: str, obj: bpy.types.Object) -> int:
	bpy.ops.object.select_all(action="DESELECT")
	export_meshes: list[bpy.types.Object] = []
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
		export_meshes.append(copy)
	bpy.ops.object.select_all(action="DESELECT")
	for mesh in export_meshes:
		mesh.select_set(True)
	bpy.context.view_layer.objects.active = export_meshes[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged.data.calc_loop_triangles()
	runtime_triangles = len(merged.data.loop_triangles)
	output = SPECIAL_OUT.get(name, ASSET_OUT / (name + ".glb"))
	output.parent.mkdir(parents=True, exist_ok=True)
	bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", export_yup=True,
		use_selection=True, export_apply=True, export_materials="EXPORT", export_animations=False)
	bpy.data.objects.remove(merged, do_unlink=True)
	return runtime_triangles


def bounds(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	points = []
	for member in family(obj):
		if member.type == "MESH":
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	return (Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points))),
		Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points))))


for asset_name, asset in ASSETS.items():
	if ONLY_ASSET != "" and asset_name != ONLY_ASSET:
		for member in family(asset):
			member.hide_render = True
		continue
	runtime_triangles = export_asset(asset_name, asset)
	lo, hi = bounds(asset)
	print("SKYQ_KIT|%s|triangles=%d|bounds=%s..%s" % (asset_name, runtime_triangles,
		tuple(round(value, 2) for value in lo), tuple(round(value, 2) for value in hi)))
	for member in family(asset):
		member.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))

# Isolated Eevee renders are the first 4.5 review gate.
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 720, 620, 100
scene.eevee.taa_render_samples = 16
scene.render.image_settings.file_format, scene.render.film_transparent = "PNG", True
scene.view_settings.look = "AgX - Medium High Contrast"
bpy.ops.object.camera_add(location=(12, -18, 10))
camera = bpy.context.active_object
camera.data.lens, scene.camera = 58, camera
for loc, energy, size, color in (((8, -10, 16), 1100, 8, (.90, .95, 1.0)),
	((-10, -4, 9), 720, 6, (.74, .84, 1.0)), ((4, 9, 12), 820, 6, (1.0, .79, .65))):
	bpy.ops.object.light_add(type="AREA", location=loc)
	light = bpy.context.active_object
	light.data.energy, light.data.shape, light.data.size, light.data.color = energy, "DISK", size, color
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(28), math.radians(-24), math.radians(-32)))
qa_sun = bpy.context.active_object
qa_sun.data.energy, qa_sun.data.color = 1.7, (0.88, 0.93, 1.0)
scene.world = bpy.data.worlds.new("Sky Lagoon QA World")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.035, 0.05, 0.12, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .38

for asset_name, asset in ASSETS.items():
	if ONLY_ASSET != "" and asset_name != ONLY_ASSET:
		continue
	for member in family(asset):
		member.hide_render = False
	lo, hi = bounds(asset)
	center, size = (lo + hi) * .5, hi - lo
	distance = max(size.x, size.y, size.z) * 2.0
	if "castle" in asset_name or "bridge" in asset_name or "station" in asset_name:
		camera.location = center + Vector((distance * .42, -distance * 1.20, distance * .48))
	elif "train" in asset_name:
		camera.location = center + Vector((distance * .72, -distance * 1.05, distance * .48))
	else:
		camera.location = center + Vector((distance * .76, -distance * 1.28, distance * .62))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
	for member in family(asset):
		member.hide_render = True

print("SKYQ_KIT|assets|%d" % (1 if ONLY_ASSET != "" else len(ASSETS)))
print("SKYQ_KIT|blend|%s" % BLEND_OUT)
