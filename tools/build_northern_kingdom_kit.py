#!/usr/bin/env python3
"""Build the authored Mobile-friendly northern kingdom art kit.

The kit replaces the first-pass engine primitives with rounded, asymmetrical
storybook models in the project's pastel toy-diorama language. No protected
book, voice, friend, or character asset is read or modified.

Usage: blender --background --python tools/build_northern_kingdom_kit.py
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "northern"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_northern_kingdom_kit"
BLEND_OUT = SOURCE_OUT / "northern_kingdom_kit.blend"
ONLY_ASSET = ""
for argument in sys.argv[1:]:
	if argument.startswith("--only="):
		ONLY_ASSET = argument.split("=", 1)[1]
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"navy": (0.075, 0.085, 0.19, 1.0),
	"purple": (0.22, 0.18, 0.38, 1.0),
	"plum": (0.36, 0.20, 0.43, 1.0),
	"stone": (0.48, 0.53, 0.65, 1.0),
	"stone_light": (0.68, 0.72, 0.82, 1.0),
	"stone_dark": (0.31, 0.35, 0.49, 1.0),
	"mountain_lavender": (0.38, 0.38, 0.58, 1.0),
	"mountain_blue": (0.31, 0.43, 0.60, 1.0),
	"snow": (0.88, 0.95, 0.98, 1.0),
	"ice": (0.47, 0.82, 0.90, 1.0),
	"ice_deep": (0.34, 0.56, 0.80, 1.0),
	"pine_dark": (0.13, 0.34, 0.34, 1.0),
	"pine": (0.22, 0.52, 0.43, 1.0),
	"pine_light": (0.43, 0.72, 0.55, 1.0),
	"moss": (0.42, 0.50, 0.27, 1.0),
	"leaf_gold": (0.78, 0.55, 0.22, 1.0),
	"leaf_rose": (0.70, 0.32, 0.42, 1.0),
	"earth": (0.35, 0.25, 0.20, 1.0),
	"wood": (0.43, 0.25, 0.18, 1.0),
	"wood_light": (0.67, 0.43, 0.28, 1.0),
	"rope": (0.78, 0.65, 0.43, 1.0),
	"iron": (0.22, 0.24, 0.31, 1.0),
	"cream": (0.94, 0.91, 0.80, 1.0),
	"gold": (0.94, 0.70, 0.22, 1.0),
	"glass": (0.43, 0.78, 0.88, 1.0),
	"window_warm": (1.0, 0.72, 0.32, 1.0),
	"ember": (1.0, 0.34, 0.12, 1.0),
	"red": (0.74, 0.25, 0.25, 1.0),
	"amber": (0.88, 0.56, 0.20, 1.0),
	"aqua": (0.24, 0.60, 0.58, 1.0),
	"rose": (0.72, 0.34, 0.54, 1.0),
	"blue": (0.34, 0.49, 0.72, 1.0),
	"orange": (0.80, 0.42, 0.22, 1.0),
	"roof_blue": (0.20, 0.28, 0.43, 1.0),
	"roof_plum": (0.31, 0.20, 0.38, 1.0),
	"mushroom": (0.83, 0.28, 0.35, 1.0),
	"mushroom_tan": (0.74, 0.55, 0.36, 1.0),
	"wisp_a": (0.42, 0.88, 0.96, 1.0),
	"wisp_b": (0.76, 0.52, 0.94, 1.0),
}


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("MRN_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.88
	bsdf.inputs["Metallic"].default_value = 0.0
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


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
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0), radius: float = 0.16) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	# primitive_cube_add(size=1) starts at one Blender unit across, so the
	# requested dimensions are the scale itself (not the half extents).
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
		mat: bpy.types.Material, parent: bpy.types.Object, vertices: int = 10) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	bev = obj.modifiers.new("soft_profile", "BEVEL")
	bev.width, bev.segments = min(radius * 0.15, 0.16), 2
	apply_modifier(obj, bev)
	return obj


def cone(name: str, loc: tuple[float, float, float], bottom: float, top: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object, vertices: int = 10) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=bottom, radius2=top, depth=depth, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	bev = obj.modifiers.new("soft_profile", "BEVEL")
	bev.width, bev.segments = min(max(top, 0.2) * 0.12, 0.12), 2
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
		factor = 0.93 + rng.random() * 0.14
		vertex.co *= factor
	assign(obj, mat, parent)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def panel_xz(name: str, outline: list[tuple[float, float]], depth: float,
		loc: tuple[float, float, float], mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	verts = [(x, -depth * 0.5, z) for x, z in outline] + [(x, depth * 0.5, z) for x, z in outline]
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
	bev.width, bev.segments = min(depth * 0.28, 0.12), 2
	apply_modifier(obj, bev)
	return obj


def tube(name: str, points: list[tuple[float, float, float]], radius: float,
		mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions, curve.resolution_u = "3D", 2
	curve.bevel_depth, curve.bevel_resolution = radius, 2
	spline = curve.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, co in zip(spline.bezier_points, points):
		point.co = co
		point.handle_left_type = point.handle_right_type = "AUTO"
	obj = bpy.data.objects.new(name, curve)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	curve.materials.append(mat)
	return obj


def poly_tube(name: str, points: list[tuple[float, float, float]], radius: float,
		mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions, curve.resolution_u = "3D", 1
	curve.bevel_depth, curve.bevel_resolution = radius, 2
	spline = curve.splines.new("POLY")
	spline.points.add(len(points) - 1)
	for point, co in zip(spline.points, points):
		point.co = (*co, 1.0)
	obj = bpy.data.objects.new(name, curve)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	curve.materials.append(mat)
	return obj


def ring(name: str, loc: tuple[float, float, float], major: float, minor: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=12, minor_segments=6, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return obj


def ground_vignette(parent: bpy.types.Object, radius: float, seed: int,
		snowy: bool = False) -> None:
	"""A compact authored base keeps props planted instead of floating."""
	base_mat = MATS["snow"] if snowy else MATS["earth"]
	blob("ground_base", (0, 0, .16), (radius, radius * .78, .24), base_mat, parent, seed)
	rng = random.Random(seed)
	for index in range(5):
		angle = math.tau * float(index) / 5.0 + rng.uniform(-.28, .28)
		distance = radius * rng.uniform(.58, .88)
		rock_mat = MATS["stone_light"] if snowy else MATS["stone"]
		blob("base_rock_%d" % index,
			(math.cos(angle) * distance, math.sin(angle) * distance, .3),
			(.34 + rng.random() * .24, .28 + rng.random() * .2, .26 + rng.random() * .18),
			rock_mat, parent, seed + 20 + index)
	if not snowy:
		for index in range(6):
			angle = math.tau * float(index) / 6.0 + .23
			x, y = math.cos(angle) * radius * .68, math.sin(angle) * radius * .54
			leaf = rounded_box("leaf_litter_%d" % index, (x, y, .34),
				(.58, .22, .08), MATS["leaf_gold" if index % 2 else "leaf_rose"],
				parent, (0, 0, angle), .04)
			leaf.rotation_euler.z = angle


def crystal_cluster(parent: bpy.types.Object, base: tuple[float, float, float],
		scale: float, prefix: str) -> None:
	for index, (dx, dy, height) in enumerate(((0.0, 0.0, 1.0),
		(-.52, .08, .68), (.46, .14, .54))):
		crystal = cone("%s_%d" % (prefix, index),
			(base[0] + dx * scale, base[1] + dy * scale,
			base[2] + height * scale * .5), .34 * scale, .03 * scale,
			height * scale, MATS["ice" if index != 1 else "wisp_b"], parent, 6)
		crystal.rotation_euler.y = (-.18 + index * .14)


def crag_mesh(name: str, height: float, radius: float, seed: int,
		mat: bpy.types.Material, parent: bpy.types.Object, snow: bool = False) -> bpy.types.Object:
	rng = random.Random(seed)
	segments = 11
	rings = 5
	verts: list[tuple[float, float, float]] = []
	for ring in range(rings):
		z = height * float(ring) / float(rings - 1)
		t = float(ring) / float(rings - 1)
		base_radius = radius * (1.0 - t * 0.78)
		for segment in range(segments):
			angle = math.tau * float(segment) / float(segments) + ring * 0.17
			jitter = 0.78 + rng.random() * 0.38
			verts.append((math.cos(angle) * base_radius * jitter,
				math.sin(angle) * base_radius * jitter, z + rng.uniform(-0.18, 0.18)))
	faces: list[tuple[int, ...]] = []
	faces.append(tuple(range(segments - 1, -1, -1)))
	for ring in range(rings - 1):
		for segment in range(segments):
			next_segment = (segment + 1) % segments
			a = ring * segments + segment
			b = ring * segments + next_segment
			c = (ring + 1) * segments + next_segment
			d = (ring + 1) * segments + segment
			faces.append((a, b, c, d))
	faces.append(tuple((rings - 1) * segments + i for i in range(segments)))
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	assign(obj, mat, parent)
	if snow:
		for polygon in obj.data.polygons:
			polygon.use_smooth = True
	return obj


def pine_crown(name: str, loc: tuple[float, float, float], radius: float, height: float,
		mat: bpy.types.Material, parent: bpy.types.Object, phase: float) -> bpy.types.Object:
	segments = 12
	verts = [(0.0, 0.0, height)]
	for ring, (z, scale) in enumerate(((height * .72, .48), (height * .34, .82), (0.0, 1.0))):
		for i in range(segments):
			angle = math.tau * i / segments + phase + ring * .11
			jag = 1.0 if i % 2 == 0 else .74
			verts.append((math.cos(angle) * radius * scale * jag,
				math.sin(angle) * radius * scale * jag, z))
	faces = []
	for i in range(segments):
		faces.append((0, 1 + i, 1 + (i + 1) % segments))
	for ring in range(2):
		start_a = 1 + ring * segments
		start_b = start_a + segments
		for i in range(segments):
			faces.append((start_a + i, start_b + i, start_b + (i + 1) % segments,
				start_a + (i + 1) % segments))
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = loc
	assign(obj, mat, parent)
	bev = obj.modifiers.new("soft_needles", "BEVEL")
	bev.width, bev.segments = .06, 2
	apply_modifier(obj, bev)
	return obj


def build_peak(name: str, seed: int, lean: float) -> bpy.types.Object:
	r = root(name)
	ground_vignette(r, 6.5, seed + 200, True)
	main = crag_mesh("hero_crag", 13.0, 5.2, seed, MATS["mountain_blue"], r)
	main.rotation_euler.x = lean
	spur = crag_mesh("side_crag", 8.0, 3.2, seed + 13, MATS["mountain_lavender"], r)
	spur.location = (3.9 if lean < 0 else -3.8, .8, .15)
	spur.rotation_euler.y = -lean * 1.5
	back = crag_mesh("back_crag", 10.2, 3.45, seed + 19, MATS["purple"], r)
	back.location = (-3.2 if lean < 0 else 3.0, 2.4, .1)
	back.rotation_euler.y = lean * 1.2
	crag_mesh("snow_crown", 4.0, 2.25, seed + 27, MATS["snow"], r, True).location.z = 9.5
	crag_mesh("spur_snow", 2.5, 1.45, seed + 29, MATS["snow"], r, True).location = (
		3.9 if lean < 0 else -3.8, .8, 5.85)
	for index, (loc, scale) in enumerate((((-1.8, -.2, 8.9), (2.1, 1.0, .55)),
		((1.2, .4, 10.0), (1.8, 1.1, .48)), ((3.8, .9, 6.2), (1.5, .9, .42)))):
		blob("snow_shelf_%d" % index, loc, scale, MATS["snow"], r, seed + index)
	crystal_cluster(r, (-4.8 if lean < 0 else 4.6, -1.1, .35), .85, "peak_crystal")
	# Broad snow ledges split the vertical mass into child-readable tiers.
	for index, (x, y, z, sx) in enumerate(((-2.1, -2.8, 4.0, 1.75),
		(1.45, -3.5, 6.25, 1.35), (-.25, -3.0, 8.65, 1.05))):
		blob("front_snow_ledge_%d" % index, (x, y, z),
			(sx, .72, .28), MATS["snow"], r, seed + 80 + index)
	return r


def build_pass_arch() -> bpy.types.Object:
	r = root("northern_pass_arch")
	ground_vignette(r, 5.2, 401, True)
	for side in (-1.0, 1.0):
		for row in range(4):
			z = .85 + row * 1.65
			blob("arch_stone_%s_%d" % ("l" if side < 0 else "r", row),
				(side * (3.55 - row * .08), 0.0, z), (1.45, 1.15, 1.05),
				MATS["stone"] if row % 2 == 0 else MATS["stone_light"], r, 40 + row + int(side))
	for index in range(7):
		angle = math.pi - math.pi * index / 6.0
		x = math.cos(angle) * 3.45
		z = 6.55 + math.sin(angle) * 2.15
		blob("arch_crown_%d" % index, (x, 0.0, z), (1.28, 1.12, 1.0),
			MATS["stone_light"] if index % 2 else MATS["stone"], r, 70 + index)
	for index, x in enumerate((-4.0, -2.5, -.8, 1.3, 3.2)):
		blob("arch_snow_%d" % index, (x, .05, 8.45 - abs(x) * .12),
			(1.35, 1.0, .35), MATS["snow"], r, 90 + index)
	# A modeled six-arm snowflake reads from both sides without a flat Label3D.
	for arm in range(6):
		angle = math.tau * arm / 6.0
		bar = rounded_box("snowflake_arm_%d" % arm, (0, -.95, 5.25),
			(.22, .18, 2.9), MATS["ice"], r, (0.0, angle, 0.0), .06)
		bar.rotation_euler.y = angle
	blob("snowflake_heart", (0, -.95, 5.25), (.48, .22, .48), MATS["snow"], r, 3)
	for side in (-1.0, 1.0):
		crystal_cluster(r, (side * 4.55, -.35, .35), .92, "gate_crystal_%s" % side)
		for drip in range(3):
			x = side * (1.15 + float(drip) * 1.15)
			cone("ice_drip_%s_%d" % (side, drip), (x, -.2, 7.5 - float(drip % 2) * .45),
				.18, .01, .9 + float(drip % 2) * .35, MATS["ice"], r, 6).rotation_euler.x = math.pi
	return r


def build_pine(name: str, variant: int) -> bpy.types.Object:
	r = root(name)
	ground_vignette(r, 2.6 + variant * .12, 500 + variant, variant == 2)
	height = 8.6 + variant * .7
	cylinder("trunk", (0, 0, height * .34), .48 + variant * .05, height * .68,
		MATS["wood"], r, 9)
	colors = (MATS["pine_dark"], MATS["pine"], MATS["pine_light"])
	for tier in range(4):
		pine_crown("crown_%d" % tier, (0, 0, 2.35 + tier * 2.25),
			3.25 - tier * .57 + variant * .1, 4.25 - tier * .28,
			colors[(tier + variant) % len(colors)], r, variant * .31 + tier * .17)
		# Rounded branch-fan tips break the stacked-cone read.
		for side in (-1.0, 1.0):
			blob("branch_pad_%d_%s" % (tier, side),
				(side * (2.35 - tier * .38), -.25 + tier * .12,
				2.4 + tier * 2.25), (.78, .52, .3),
				colors[(tier + variant + 1) % len(colors)], r,
				560 + variant * 20 + tier * 2 + int(side > 0))
	for index, (x, y, z, sx) in enumerate(((-1.2, -.35, 5.2, 1.5),
		(1.05, .25, 7.0, 1.25), (-.4, .15, 8.8, .9))):
		blob("snow_pillow_%d" % index, (x, y, z + variant * .2),
			(sx, sx * .65, .34), MATS["snow"], r, variant * 10 + index)
	for index in range(3):
		angle = -.65 + index * .62 + variant * .2
		cone("pinecone_%d" % index, (math.cos(angle) * 1.15, -.65,
			1.0 + index * .18), .22, .08, .52, MATS["wood_light"], r, 8)
	return r


def build_mushrooms(name: str, tan: bool) -> bpy.types.Object:
	r = root(name)
	ground_vignette(r, 2.8, 620 if tan else 610, False)
	cap_mat = MATS["mushroom_tan"] if tan else MATS["mushroom"]
	spots = ((-1.35, .15, 1.25, .8), (0, -.25, 1.8, 1.05), (1.35, .2, 1.05, .65),
		(.65, .7, .72, .43))
	for index, (x, y, height, radius) in enumerate(spots):
		cylinder("stem_%d" % index, (x, y, height * .5), radius * .24,
			height, MATS["cream"], r, 9)
		cap = blob("cap_%d" % index, (x, y, height + radius * .22),
			(radius, radius * .82, radius * .42), cap_mat, r, 100 + index)
		cap.rotation_euler.z = (-.1 + index * .07)
		# A warm undershelf makes the caps sculptural instead of sphere halves.
		cone("gills_%d" % index, (x, y, height + radius * .06), radius * .72,
			radius * .24, radius * .24, MATS["cream"], r, 12)
		if not tan:
			for spot in range(3):
				angle = math.tau * spot / 3.0 + index
				blob("dot_%d_%d" % (index, spot),
					(x + math.cos(angle) * radius * .44, y + math.sin(angle) * radius * .38,
					height + radius * .52), (radius * .12, radius * .08, radius * .05),
					MATS["snow"], r, 140 + index * 3 + spot)
	for index, x in enumerate((-1.9, 1.8)):
		cone("fern_%d" % index, (x, .55, .62), .5, .08, 1.15,
			MATS["moss"], r, 7).rotation_euler.y = (-.35 if index == 0 else .32)
	return r


def build_house(name: str, body_key: str, roof_key: str, variant: int) -> bpy.types.Object:
	r = root(name)
	width = 8.2 + (variant % 3) * .55
	depth = 6.7 + (variant % 2) * .55
	body_h = 5.2 + (variant % 2) * .35
	rise = 3.9 + (variant % 3) * .28
	body_mat, roof_mat = MATS[body_key], MATS[roof_key]
	ground_vignette(r, width * .68, 700 + variant, False)
	rounded_box("painted_timber_body", (0, 0, body_h * .5), (width, depth, body_h),
		body_mat, r, radius=.32)
	# Uneven stone footing and dark sill anchor each cottage into the street.
	for index in range(7):
		x = -width * .43 + float(index) * width * .86 / 6.0
		blob("foundation_stone_%d" % index, (x, -depth * .54, .48),
			(width * .075, .48, .5 + (index % 2) * .12),
			MATS["stone_light" if index % 3 else "stone"], r, 730 + variant * 10 + index)
	gable_mat = MATS["cream"] if variant in (1, 3, 5) else body_mat
	panel_xz("front_gable", [(-width * .5, 0), (width * .5, 0), (0, rise)], .42,
		(0, -depth * .5 - .04, body_h), gable_mat, r)
	panel_xz("back_gable", [(-width * .5, 0), (width * .5, 0), (0, rise)], .42,
		(0, depth * .5 + .04, body_h), body_mat, r)
	slope = math.atan2(rise, width * .5)
	roof_len = math.sqrt((width * .5) ** 2 + rise ** 2) + .75
	for side in (-1.0, 1.0):
		rounded_box("roof_%s" % ("l" if side < 0 else "r"),
			(side * width * .245, 0, body_h + rise * .52),
			(roof_len, depth + 1.0, .52), roof_mat, r,
			(0.0, side * slope, 0.0), .16)
	# Three broad scalloped courses follow both roof slopes. They add depth to
	# the surface that is actually visible in the three-quarter game camera.
	for side in (-1.0, 1.0):
		for row in range(3):
			d = 1.0 + float(row) * 1.15
			x = side * (width * .12 + float(row) * width * .095)
			z = body_h + rise * (.84 - float(row) * .2)
			for index in range(5):
				y = -depth * .38 + float(index) * depth * .19
				tile = rounded_box("roof_tile_%s_%d_%d" % (side, row, index),
					(x, y, z), (d, depth * .16, .18), MATS[roof_key], r,
					(0, side * slope, 0), .07)
				tile.rotation_euler.y = side * slope
	# Snow is a single soft ridge instead of a second floating roof card. This
	# keeps the gable silhouette joined and readable on the Mobile renderer.
	tube("snowy_ridge", [(0, -depth * .52, body_h + rise + .08),
		(0, 0, body_h + rise + .16), (0, depth * .52, body_h + rise + .08)],
		.22, MATS["snow"], r)
	for y in (-depth * .35, depth * .28):
		blob("roof_snow_pillow_%.1f" % y, (-width * .18, y, body_h + rise * .63),
			(width * .13, .68, .18), MATS["snow"], r, 310 + variant * 2 + int(y > 0))
	for x in (-width * .45, width * .45):
		rounded_box("corner_board_%.1f" % x, (x, -depth * .515, body_h * .5),
			(.42, .26, body_h + .15), MATS["cream"], r, radius=.09)
	for z in (1.45, 3.75):
		rounded_box("front_beam_%.1f" % z, (0, -depth * .525, z),
			(width * .92, .24, .28), MATS["wood"], r, radius=.07)
	# Gable braces form a strong Nordic A-shape instead of a blank triangle.
	for side in (-1.0, 1.0):
		brace = rounded_box("gable_brace_%s" % side,
			(side * width * .22, -depth * .57, body_h + rise * .42),
			(.28, .22, rise * .86), MATS["wood"], r,
			(0, -side * slope, 0), .06)
		brace.rotation_euler.y = -side * slope
	# Oversized door and blue-glass windows remain readable at gameplay distance.
	door_x = -width * .22 if variant % 2 else width * .22
	panel_xz("carved_door", [(-1.0, 0), (1.0, 0), (1.0, 2.65), (0, 3.55), (-1.0, 2.65)],
		.34, (-width * .22 if variant % 2 else width * .22, -depth * .54, .05),
		MATS["wood_light"], r)
	poly_tube("door_arch", [(door_x - 1.25, -depth * .74, .15),
		(door_x - 1.25, -depth * .74, 2.6), (door_x, -depth * .74, 3.85),
		(door_x + 1.25, -depth * .74, 2.6), (door_x + 1.25, -depth * .74, .15)],
		.12, MATS["cream"], r)
	rounded_box("door_step", (door_x, -depth * .84, .18), (2.65, 1.0, .32),
		MATS["stone_light"], r, radius=.1)
	blob("door_knob", (door_x + .56,
		-depth * .75, 1.35), (.12, .12, .12), MATS["gold"], r, 790 + variant)
	for index, x in enumerate((-width * .27, width * .27)):
		if (variant % 2 == 0 and index == 1) or (variant % 2 == 1 and index == 0):
			continue
		rounded_box("window_%d" % index, (x, -depth * .545, 2.65),
			(1.9, .26, 1.9), MATS["window_warm"], r, radius=.22)
		rounded_box("window_cross_v_%d" % index, (x, -depth * .57, 2.65),
			(.14, .12, 1.82), MATS["cream"], r, radius=.04)
		rounded_box("window_cross_h_%d" % index, (x, -depth * .57, 2.65),
			(1.82, .12, .14), MATS["cream"], r, radius=.04)
		poly_tube("window_trim_%d" % index,
			[(x - 1.05, -depth * .72, 1.62), (x - 1.05, -depth * .72, 3.68),
			(x + 1.05, -depth * .72, 3.68), (x + 1.05, -depth * .72, 1.62)],
			.09, MATS["cream"], r)
	if variant % 2 == 0:
		rounded_box("chimney", (-width * .25, .7, body_h + rise * .66),
			(1.0, 1.0, 3.5), MATS["stone"], r, radius=.15)
		blob("chimney_snow", (-width * .25, .7, body_h + rise * .66 + 1.8),
			(.65, .65, .25), MATS["snow"], r, variant)
	else:
		# A tiny front dormer prevents the family from reading as palette swaps.
		rounded_box("dormer_face", (0, -depth * .52, body_h + rise * .48),
			(2.1, .7, 1.75), body_mat, r, radius=.2)
		panel_xz("dormer_gable", [(-1.2, 0), (1.2, 0), (0, 1.0)], .75,
			(0, -depth * .52, body_h + rise * .48 + .85), roof_mat, r)
		rounded_box("dormer_window", (0, -depth * .92, body_h + rise * .54),
			(1.05, .18, .9), MATS["glass"], r, radius=.12)
	# Variant-specific porch/side wing gives all six runtime roles a distinct profile.
	if variant in (2, 5):
		rounded_box("side_wing", (width * .56, .55, 1.65), (3.0, depth * .68, 3.3),
			body_mat, r, radius=.25)
		rounded_box("side_wing_roof", (width * .56, .55, 3.55),
			(3.5, depth * .78, .48), roof_mat, r, (0, .18, 0), .12)
	elif variant in (1, 4):
		for x in (-1.65, 1.65):
			cylinder("porch_post_%s" % x, (x, -depth * .72, 1.3), .14, 2.6,
				MATS["cream"], r, 8)
		rounded_box("porch_canopy", (0, -depth * .72, 2.75),
			(4.4, 2.0, .4), roof_mat, r, (math.radians(-8), 0, 0), .1)
	# Six unmistakable role motifs: inn sign, flower porch, bay lantern,
	# heart crest, snow balcony, or covered wood rack.
	if variant == 0:
		ring("inn_sign", (-width * .38, -depth * .78, 3.9), .58, .13,
			MATS["gold"], r, (math.pi * .5, 0, 0))
		cylinder("sign_bracket", (-width * .38, -depth * .58, 4.6), .08, 1.25,
			MATS["iron"], r, 8)
	elif variant == 1:
		for index, x in enumerate((-1.2, -.55, .2, .85)):
			blob("porch_flower_%d" % index, (x, -depth * .91, .75),
				(.25, .25, .3), MATS["rose" if index % 2 else "gold"], r, 820 + index)
	elif variant == 2:
		crystal_cluster(r, (-width * .42, -depth * .62, .45), .68, "house_crystal")
	elif variant == 3:
		panel_xz("heart_crest", [(-.55, .35), (0, 0), (.55, .35),
			(.45, .85), (0, 1.25), (-.45, .85)], .18,
			(0, -depth * .73, body_h + rise * .48), MATS["gold"], r)
	elif variant == 4:
		rounded_box("snow_balcony", (0, -depth * .84, body_h * .72),
			(3.8, 1.0, .3), MATS["wood_light"], r, radius=.08)
		for x in (-1.55, -.5, .5, 1.55):
			cylinder("baluster_%s" % x, (x, -depth * .98, body_h * .72 + .65),
				.08, 1.3, MATS["cream"], r, 7)
	else:
		for index in range(4):
			log = cylinder("wood_rack_log_%d" % index,
				(-width * .43 + float(index % 2) * .55, -depth * .64,
				.5 + float(index // 2) * .48), .22, 1.5, MATS["wood"], r, 8)
			log.rotation_euler.y = math.pi * .5
	return r


def build_dock() -> bpy.types.Object:
	r = root("northern_fjord_dock")
	for x in (-7.8, 7.8):
		for y in (-1.2, 1.2):
			blob("dock_footing_%.1f_%.1f" % (x, y), (x, y, -.45),
				(1.05, .9, .55), MATS["stone_light"], r, 850 + int(x + y))
	for index in range(14):
		x = -7.8 + index * 1.2
		plank = rounded_box("plank_%02d" % index, (x, 0, .45 + (index % 3 - 1) * .035),
			(1.05, 2.8, .38), MATS["wood_light"] if index % 3 else MATS["wood"], r, radius=.09)
		plank.rotation_euler.z = (index % 2 - .5) * .012
	for x in (-7.9, -2.7, 2.7, 7.9):
		for y in (-1.15, 1.15):
			cylinder("post_%.1f_%.1f" % (x, y), (x, y, .25), .24, 3.4, MATS["wood"], r, 9)
			ring("rope_knot_%.1f_%.1f" % (x, y), (x, y, 1.15), .32, .08,
				MATS["rope"], r, (math.pi * .5, 0, 0))
	for side in (-1.0, 1.0):
		for section, (x0, x1) in enumerate(((-7.9, -2.7), (-2.7, 2.7), (2.7, 7.9))):
			tube("rope_%s_%d" % ("l" if side < 0 else "r", section),
				[(x0, side * 1.15, 1.55), ((x0 + x1) * .5, side * 1.15, .92),
				(x1, side * 1.15, 1.55)], .075, MATS["cream"], r)
	# Child-readable carved prow marker.
	panel_xz("dock_fish_sign", [(-.75, 0), (.35, 0), (1.0, .55), (.35, 1.1), (-.75, 1.1),
		(-1.15, .55)], .22, (7.15, -1.45, 1.75), MATS["aqua"], r)
	for x in (-5.2, 0.0, 5.2):
		for side in (-1.0, 1.0):
			brace = rounded_box("dock_brace_%.1f_%s" % (x, side),
				(x, side * .78, -.15), (.28, .28, 2.0), MATS["wood"], r,
				(side * .55, 0, 0), .06)
			brace.rotation_euler.x = side * .55
	# A ladder and two iron bumpers make the dock tell a usable story.
	for y in (-.55, .55):
		cylinder("ladder_rail_%s" % y, (6.0, y, -.75), .09, 2.6,
			MATS["rope"], r, 8)
	for z in (-1.45, -.7, .05):
		rounded_box("ladder_rung_%s" % z, (6.0, 0, z), (.16, 1.25, .16),
			MATS["rope"], r, radius=.04)
	for x in (-4.0, 4.0):
		ring("dock_bumper_%s" % x, (x, -1.55, .1), .62, .16, MATS["iron"], r,
			(math.pi * .5, 0, 0))
	return r


def add_crenels(parent: bpy.types.Object, y: float, z: float, width: float, along_x: bool,
		prefix: str) -> None:
	count = max(3, int(width / 4.5))
	for index in range(count):
		offset = -width * .5 + (index + .5) * width / count
		loc = (offset, y, z) if along_x else (y, offset, z)
		size = (1.8, 1.1, 1.45) if along_x else (1.1, 1.8, 1.45)
		rounded_box(prefix + "_%02d" % index, loc, size, MATS["stone_light"], parent, radius=.14)


def build_castle() -> bpy.types.Object:
	r = root("northern_center_castle")
	blob("castle_snow_island", (0, 1, .25), (34.0, 31.0, .6), MATS["snow"], r, 900)
	rounded_box("courtyard_path", (0, -15.0, .75), (8.0, 24.0, .38),
		MATS["stone_light"], r, radius=.12)
	# Curtain wall with an open, unmistakable south gate.
	for name, loc, size in (("north_wall", (0, 27, 5.0), (58, 3.2, 10)),
		("west_wall", (-29, 0, 5.0), (3.2, 54, 10)),
		("east_wall", (29, 0, 5.0), (3.2, 54, 10)),
		("south_left", (-19, -27, 5.0), (20, 3.2, 10)),
		("south_right", (19, -27, 5.0), (20, 3.2, 10))):
		rounded_box(name, loc, size, MATS["stone"], r, radius=.45)
		rounded_box(name + "_navy_foot", (loc[0], loc[1], .75),
			(size[0] + .18, size[1] + .18, .65), MATS["navy"], r, radius=.18)
	add_crenels(r, -27, 10.65, 20, True, "south_left_merlon")
	add_crenels(r, -27, 10.65, 20, True, "south_right_merlon")
	add_crenels(r, 27, 10.65, 58, True, "north_merlon")
	add_crenels(r, -29, 10.65, 54, False, "west_merlon")
	add_crenels(r, 29, 10.65, 54, False, "east_merlon")
	for side in (-1.0, 1.0):
		for index in range(4):
			x = side * (8.0 + float(index) * 4.5)
			rounded_box("front_course_%s_%d" % (side, index), (x, -28.7, 4.0),
				(3.7, .22, .38), MATS["stone_light"], r, radius=.08)
		# Long hanging banners make the entrance readable at gameplay distance.
		panel_xz("gate_banner_%s" % side,
			[(-1.05, 0), (1.05, 0), (1.05, 4.5), (0, 3.85), (-1.05, 4.5)], .18,
			(side * 7.1, -28.75, 4.2), MATS["aqua" if side < 0 else "rose"], r)
		panel_xz("banner_star_%s" % side,
			[(0, 0), (.25, .55), (.8, .65), (.38, 1.0), (.5, 1.6),
				(0, 1.25), (-.5, 1.6), (-.38, 1.0), (-.8, .65), (-.25, .55)], .08,
			(side * 7.1, -28.98, 5.55), MATS["gold"], r)
	# Four asymmetrical profiled towers and steep Nordic roofs.
	for index, (x, y) in enumerate(((-29, -27), (29, -27), (-29, 27), (29, 27))):
		cylinder("tower_%d" % index, (x, y, 8.0), 5.5 + (index % 2) * .35,
			16.0 + (index % 2), MATS["stone_light"], r, 12)
		cylinder("tower_band_%d" % index, (x, y, 8.4), 5.75, .7, MATS["purple"], r, 12)
		cone("tower_roof_%d" % index, (x, y, 20.3 + (index % 2) * .5),
			7.2, .35, 9.0, MATS["roof_blue"] if index % 2 == 0 else MATS["roof_plum"], r, 12)
		blob("tower_snow_%d" % index, (x - 1.2, y - .4, 18.0),
			(4.8, 3.7, .45), MATS["snow"], r, 230 + index)
		cylinder("flag_pole_%d" % index, (x, y, 27.3), .12, 6.0, MATS["gold"], r, 8)
		flag = panel_xz("flag_%d" % index, [(0, 0), (2.7, -.45), (2.3, 1.4), (0, 1.4)],
			.12, (x, y, 28.8), MATS["rose"] if index % 2 else MATS["aqua"], r)
		flag.rotation_euler.z = math.radians(-7 if index % 2 else 8)
	# Keep: an actual open doorway and hollow shell, not a door painted on a box.
	for name, loc, size in (("keep_back", (0, 17.2, 10), (26, 1.6, 20)),
		("keep_left", (-12.2, 8, 10), (1.6, 18.0, 20)),
		("keep_right", (12.2, 8, 10), (1.6, 18.0, 20)),
		("keep_front_left", (-8.0, -1.2, 10), (8.5, 1.6, 20)),
		("keep_front_right", (8.0, -1.2, 10), (8.5, 1.6, 20)),
		("keep_door_lintel", (0, -1.2, 16.2), (7.5, 1.6, 7.6))):
		rounded_box(name, loc, size, MATS["stone_light"], r, radius=.5)
	rounded_box("keep_navy_base", (0, 8, 1.0), (26.5, 20.5, 1.1), MATS["navy"], r, radius=.2)
	for side in (-1.0, 1.0):
		rounded_box("keep_roof_%s" % side, (side * 6.2, 8, 21.1),
			(16.2, 22.0, .8), MATS["roof_blue"], r,
			(0, side * math.radians(34), 0), .18)
	tube("keep_snowy_ridge", [(0, -2.5, 26.25), (0, 8, 26.35), (0, 18.5, 26.25)],
		.32, MATS["snow"], r)
	for side in (-1.0, 1.0):
		cylinder("keep_bay_%s" % side, (side * 10.5, -2.0, 7.0), 3.4, 14.0,
			MATS["stone"], r, 10)
		cone("keep_bay_roof_%s" % side, (side * 10.5, -2.0, 16.0),
			4.5, .25, 5.8, MATS["roof_plum"], r, 10)
	# The great door is visibly open; paired leaves sit against the jambs.
	for side in (-1.0, 1.0):
		door = panel_xz("open_door_%s" % side,
			[(-1.4, 0), (1.4, 0), (1.4, 5.2), (0, 6.6), (-1.4, 5.2)], .36,
			(side * 4.0, -2.1, .05), MATS["wood_light"], r)
		door.rotation_euler.z = side * math.radians(7)
	for side in (-1.0, 1.0):
		tube("door_arch_%s" % side, [(side * 3.45, -2.52, .5),
			(side * 3.65, -2.52, 5.2), (side * 2.0, -2.52, 7.6),
			(0, -2.52, 8.55)], .25, MATS["gold"], r)
	for x in (-7.0, 7.0):
		for z in (6.0, 12.2):
			rounded_box("keep_window_%.1f_%.1f" % (x, z), (x, -2.35, z),
				(2.8, .3, 3.1), MATS["glass"], r, radius=.28)
			rounded_box("keep_window_trim_%.1f_%.1f" % (x, z), (x, -2.52, z),
				(3.25, .15, .3), MATS["cream"], r, radius=.07)
	# A modeled crown crest replaces the billboard glyph.
	panel_xz("crown_crest", [(-3, 0), (3, 0), (2.7, 2.1), (1.25, .8),
		(0, 3.2), (-1.25, .8), (-2.7, 2.1)], .55, (0, -2.65, 25.2), MATS["gold"], r)
	for x in (-2.7, 0, 2.7):
		blob("crown_jewel_%.1f" % x, (x, -2.98, 26.6 if x == 0 else 26.0),
			(.32, .2, .32), MATS["wisp_b" if x == 0 else "ice"], r, 290 + int(x))
	crystal_cluster(r, (-17.0, -20.5, .8), 1.4, "courtyard_crystal_l")
	crystal_cluster(r, (17.0, -20.5, .8), 1.2, "courtyard_crystal_r")
	return r


def build_wisp() -> bpy.types.Object:
	r = root("northern_wisp")
	# Two crossed, thick flame profiles keep a sculpted silhouette from all angles.
	outline = [(-.55, 0), (.55, 0), (.78, .9), (.32, 1.65), (.08, 2.55),
		(-.38, 1.72), (-.78, .92)]
	front = panel_xz("wisp_flame_a", outline, .32, (0, 0, 0), MATS["wisp_a"], r)
	side = panel_xz("wisp_flame_b", outline, .32, (0, 0, 0), MATS["wisp_b"], r)
	side.rotation_euler.z = math.pi * .5
	blob("wisp_heart", (0, 0, .82), (.42, .42, .58), MATS["snow"], r, 12)
	ring("wisp_orbit", (0, 0, .92), 1.15, .055, MATS["ice"], r,
		(math.pi * .5, 0, math.radians(18)))
	for index in range(5):
		angle = math.tau * index / 5.0
		blob("wisp_mote_%d" % index,
			(math.cos(angle) * 1.35, math.sin(angle) * 1.35, .9 + (index % 2) * .35),
			(.18, .18, .28), MATS["wisp_a"] if index % 2 == 0 else MATS["wisp_b"], r, index)
	panel_xz("wisp_star", [(0, 0), (.12, .3), (.42, .42), (.12, .54),
		(0, .86), (-.12, .54), (-.42, .42), (-.12, .3)], .12,
		(0, -.42, .72), MATS["gold"], r)
	return r


def build_spirit_stone() -> bpy.types.Object:
	r = root("northern_spirit_stone")
	# A compact base and strongly vertical silhouette keep this readable as a
	# standing ritual stone when the runtime camera is several metres away.
	ground_vignette(r, 1.8, 960, False)
	cylinder("menhir_lower_plinth", (0, 0, .34), 1.75, .62,
		MATS["stone_dark"], r, 10)
	cylinder("menhir_upper_plinth", (0, 0, .78), 1.42, .36,
		MATS["stone_light"], r, 10)
	stone = crag_mesh("carved_menhir", 7.2, 1.18, 961, MATS["stone"], r)
	stone.location.z = .92
	stone.scale = (.94, .72, 1.0)
	stone.rotation_euler.y = math.radians(3)
	panel_xz("menhir_shadow", [(-.55, 0), (.12, .18), (.48, 4.7),
		(0, 6.15), (-.5, 4.55)], .14, (0, -.88, 1.2), MATS["stone_dark"], r)
	# The oversized elemental crest is modeled geometry rather than a font or
	# billboard, so its identity remains crisp under the Mobile renderer.
	crest_z = 5.0
	for arm in range(8):
		angle = math.tau * float(arm) / 8.0
		bar = rounded_box("crest_arm_%d" % arm, (0, -1.02, crest_z),
			(.16, .12, 1.42), MATS["wisp_b" if arm % 2 else "ice"], r,
			(0, angle, 0), .045)
		bar.rotation_euler.y = angle
	blob("crest_heart", (0, -1.08, crest_z), (.46, .2, .46), MATS["snow"], r, 962)
	ring("crest_halo", (0, -.98, crest_z), 1.05, .1, MATS["gold"], r,
		(math.pi * .5, 0, 0))
	cone("menhir_crown", (0, 0, 8.48), .72, .05, 1.05,
		MATS["wisp_b"], r, 8)
	crystal_cluster(r, (1.45, -.2, .38), .72, "menhir_crystal")
	return r


def build_log_bridge() -> bpy.types.Object:
	r = root("northern_log_bridge")
	for index in range(10):
		x = -5.4 + float(index) * 1.2
		plank = rounded_box("bridge_plank_%02d" % index,
			(x, 0, .45 + (index % 3 - 1) * .04), (1.05, 5.6, .38),
			MATS["wood_light" if index % 3 else "wood"], r, radius=.09)
		plank.rotation_euler.z = (-.012 if index % 2 else .014)
	for x in (-5.55, -.5, 5.55):
		for side in (-1.0, 1.0):
			cylinder("bridge_post_%s_%s" % (x, side), (x, side * 2.5, 1.45),
				.24, 3.2, MATS["wood"], r, 9)
			ring("bridge_knot_%s_%s" % (x, side), (x, side * 2.5, 2.05),
				.31, .08, MATS["rope"], r, (math.pi * .5, 0, 0))
	for side in (-1.0, 1.0):
		for section, (x0, x1) in enumerate(((-5.55, -.5), (-.5, 5.55))):
			tube("bridge_rope_%s_%d" % (side, section),
				[(x0, side * 2.5, 2.3), ((x0 + x1) * .5, side * 2.5, 1.65),
				(x1, side * 2.5, 2.3)], .075, MATS["rope"], r)
	for side in (-1.0, 1.0):
		for x in (-5.6, 5.6):
			blob("bridge_bank_rock_%s_%s" % (side, x), (x, side * 2.15, .25),
				(.85, .72, .42), MATS["stone"], r, 980 + int(x + side))
	return r


def build_mill_house() -> bpy.types.Object:
	r = root("northern_mill_house")
	ground_vignette(r, 7.0, 1000, False)
	for index in range(8):
		x = -4.5 + float(index) * 1.28
		blob("mill_foundation_%d" % index, (x, -4.1, .48),
			(.72, .55, .52), MATS["stone_light" if index % 2 else "stone"], r, 1001 + index)
	rounded_box("mill_body", (0, 0, 3.5), (10.0, 8.0, 7.0),
		MATS["wood_light"], r, radius=.32)
	for x in (-4.45, 0, 4.45):
		rounded_box("mill_beam_%s" % x, (x, -4.15, 3.5), (.45, .32, 7.1),
			MATS["wood"], r, radius=.09)
	for z in (1.35, 4.6):
		rounded_box("mill_crossbeam_%s" % z, (0, -4.16, z), (9.2, .3, .34),
			MATS["wood"], r, radius=.08)
	panel_xz("mill_gable", [(-5.0, 0), (5.0, 0), (0, 4.2)], .45,
		(0, -4.02, 7.0), MATS["cream"], r)
	for side in (-1.0, 1.0):
		roof = rounded_box("mill_roof_%s" % side, (side * 2.55, 0, 9.15),
			(6.9, 9.2, .58), MATS["roof_plum"], r,
			(0, side * math.radians(39), 0), .14)
		roof.rotation_euler.y = side * math.radians(39)
		for row in range(3):
			for index in range(5):
				tile = rounded_box("mill_roof_tile_%s_%d_%d" % (side, row, index),
					(side * (1.0 + row * 1.0), -3.1 + index * 1.55,
					10.25 - row * 1.15), (1.15, 1.25, .18),
					MATS["roof_plum"], r, (0, side * math.radians(39), 0), .07)
				tile.rotation_euler.y = side * math.radians(39)
	tube("mill_snow_ridge", [(0, -4.2, 11.25), (0, 0, 11.4), (0, 4.2, 11.25)],
		.24, MATS["snow"], r)
	panel_xz("mill_door", [(-.9, 0), (.9, 0), (.9, 2.6), (0, 3.25), (-.9, 2.6)],
		.32, (2.4, -4.35, .05), MATS["wood"], r)
	poly_tube("mill_door_arch", [(1.25, -4.55, .15), (1.25, -4.55, 2.55),
		(2.4, -4.55, 3.65), (3.55, -4.55, 2.55), (3.55, -4.55, .15)],
		.12, MATS["cream"], r)
	for x in (-2.3, 0):
		rounded_box("mill_window_%s" % x, (x, -4.35, 3.8),
			(1.35, .24, 1.45), MATS["window_warm"], r, radius=.16)
		for vertical in (True, False):
			rounded_box("mill_window_cross_%s_%s" % (x, vertical),
				(x, -4.5, 3.8), (.12, .08, 1.35) if vertical else (1.25, .08, .12),
				MATS["cream"], r, radius=.03)
	for index in range(9):
		x = -5.2 + float(index) * 1.3
		rounded_box("mill_deck_%d" % index, (x, -5.7, .55),
			(1.1, 3.0, .38), MATS["wood_light" if index % 2 else "wood"], r, radius=.08)
	panel_xz("mill_saw_sign", [(-.8, 0), (.8, 0), (1.05, .45), (.8, .9),
		(-.8, .9), (-1.05, .45)], .18, (-4.1, -4.55, 5.8), MATS["gold"], r)
	for index in range(4):
		log = cylinder("mill_log_%d" % index, (-3.6 + (index % 2) * 1.1,
			3.5, .55 + (index // 2) * .72), .38, 3.5, MATS["wood"], r, 8)
		log.rotation_euler.y = math.pi * .5
	return r


def build_mill_wheel() -> bpy.types.Object:
	r = root("northern_mill_wheel")
	ring("wheel_outer", (0, 0, 0), 3.25, .28, MATS["wood"], r,
		(0, math.pi * .5, 0))
	ring("wheel_inner", (0, 0, 0), 2.35, .18, MATS["wood_light"], r,
		(0, math.pi * .5, 0))
	hub = cylinder("wheel_hub", (0, 0, 0), .62, 1.2, MATS["iron"], r, 10)
	hub.rotation_euler.y = math.pi * .5
	for index in range(8):
		angle = math.tau * float(index) / 8.0
		spoke = rounded_box("wheel_spoke_%d" % index, (0, 0, 0),
			(.32, .28, 5.8), MATS["wood_light"], r, (angle, 0, 0), .06)
		spoke.rotation_euler.x = angle
		paddle = rounded_box("wheel_paddle_%d" % index,
			(0, math.sin(angle) * 3.45, math.cos(angle) * 3.45),
			(.85, 1.2, .38), MATS["wood"], r, (angle, 0, 0), .07)
		paddle.rotation_euler.x = angle
	return r


def build_forge() -> bpy.types.Object:
	r = root("northern_forge")
	ground_vignette(r, 5.0, 1050, False)
	for x in (-3.6, 3.6):
		for y in (-3.2, 3.2):
			cylinder("forge_post_%s_%s" % (x, y), (x, y, 2.8), .28, 5.6,
				MATS["wood"], r, 9)
	for side in (-1.0, 1.0):
		roof = rounded_box("forge_roof_%s" % side, (side * 2.0, 0, 5.9),
			(5.3, 7.8, .5), MATS["roof_plum"], r,
			(0, side * math.radians(22), 0), .13)
		roof.rotation_euler.y = side * math.radians(22)
	tube("forge_snow_ridge", [(0, -3.4, 6.85), (0, 0, 6.95), (0, 3.4, 6.85)],
		.2, MATS["snow"], r)
	for y in (-2.4, 0, 2.4):
		for side in (-1.0, 1.0):
			roof_batten = rounded_box("forge_roof_batten_%s_%s" % (side, y),
				(side * 2.0, y, 6.12), (4.7, .18, .16), MATS["plum"], r,
				(0, side * math.radians(22), 0), .05)
			roof_batten.rotation_euler.y = side * math.radians(22)
	# Stone hearth with a dark arched mouth and three hot coals.
	for index in range(6):
		angle = math.tau * float(index) / 6.0
		blob("hearth_stone_%d" % index,
			(1.65 + math.cos(angle) * 1.25, -.7, .85 + math.sin(angle) * .78),
			(.72, .65, .62), MATS["stone_light" if index % 2 else "stone"], r, 1060 + index)
	panel_xz("hearth_mouth", [(-.85, 0), (.85, 0), (.75, 1.0), (0, 1.45), (-.75, 1.0)],
		.22, (1.65, -1.38, .18), MATS["navy"], r)
	for index, x in enumerate((1.15, 1.65, 2.15)):
		blob("ember_%d" % index, (x, -1.58, .62), (.22, .18, .16),
			MATS["ember" if index != 1 else "gold"], r, 1070 + index)
	# A recognisable horned anvil rather than a plain grey box.
	rounded_box("anvil_base", (-1.35, -.2, .58), (1.15, .85, 1.15),
		MATS["iron"], r, radius=.13)
	rounded_box("anvil_face", (-1.45, -.2, 1.38), (2.55, 1.0, .38),
		MATS["stone_dark"], r, radius=.1)
	cone("anvil_horn", (-3.0, -.2, 1.38), .48, .03, 1.55,
		MATS["iron"], r, 8).rotation_euler.y = math.pi * .5
	for index, x in enumerate((-3.0, -2.35, -1.7)):
		tool = rounded_box("hanging_tool_%d" % index, (x, 2.95, 3.25),
			(.12, .16, 2.0 - index * .2), MATS["iron"], r,
			(0, 0, -.12 + index * .11), .03)
		tool.rotation_euler.z = -.12 + index * .11
	cylinder("forge_chimney", (2.0, 1.5, 6.9), .72, 4.0,
		MATS["stone"], r, 9)
	blob("forge_chimney_snow", (2.0, 1.5, 9.0), (.72, .68, .2),
		MATS["snow"], r, 1085)
	panel_xz("forge_hammer_sign", [(-.16, 0), (.16, 0), (.16, 1.45),
		(.7, 1.45), (.7, 1.9), (-.7, 1.9), (-.7, 1.45), (-.16, 1.45)],
		.18, (-3.55, -3.55, 3.1), MATS["gold"], r)
	return r


def build_street_lantern() -> bpy.types.Object:
	r = root("northern_street_lantern")
	blob("lantern_foot", (0, 0, .24), (.72, .62, .32), MATS["stone"], r, 1100)
	cylinder("lantern_post", (0, 0, 2.6), .18, 5.0, MATS["wood"], r, 9)
	tube("lantern_hook", [(0, 0, 4.75), (.1, 0, 5.55), (.75, 0, 5.75),
		(1.05, 0, 5.35)], .11, MATS["iron"], r)
	for z in (4.75, 5.65):
		ring("lantern_frame_%s" % z, (1.05, 0, z), .48, .08,
			MATS["iron"], r, (math.pi * .5, 0, 0))
	for x in (.65, 1.45):
		rounded_box("lantern_cage_%s" % x, (x, 0, 5.2), (.09, .12, 1.0),
			MATS["iron"], r, radius=.03)
	blob("lantern_glow", (1.05, 0, 5.2), (.42, .32, .55), MATS["window_warm"], r, 1101)
	cone("lantern_cap", (1.05, 0, 5.88), .7, .08, .48, MATS["roof_plum"], r, 8)
	return r


def build_hall_centerpiece() -> bpy.types.Object:
	r = root("northern_hall_centerpiece")
	# Frozen fountain and six carved pillars form one coherent hero composition.
	for tier, (radius, height, z) in enumerate(((4.8, 1.0, .5), (3.2, .9, 1.45),
		(1.7, 2.6, 2.95))):
		cylinder("fountain_tier_%d" % tier, (0, 0, z), radius, height,
			MATS["snow" if tier == 0 else "ice"], r, 12)
	ring("fountain_rim", (0, 0, 1.0), 4.25, .28, MATS["ice_deep"], r)
	crystal_cluster(r, (0, 0, 4.1), 2.0, "fountain_crown")
	for index in range(6):
		angle = math.tau * float(index) / 6.0
		tube("frozen_jet_%d" % index,
			[(math.cos(angle) * 1.2, math.sin(angle) * 1.2, 4.0),
			(math.cos(angle) * 2.0, math.sin(angle) * 2.0, 5.8),
			(math.cos(angle) * 3.0, math.sin(angle) * 3.0, 3.7)],
			.18, MATS["ice"], r)
		px, py = math.cos(angle) * 14.5, math.sin(angle) * 10.8
		cylinder("hall_pillar_%d" % index, (px, py, 7.5), 1.45, 15.0,
			MATS["stone_light"], r, 10)
		cylinder("pillar_base_%d" % index, (px, py, .75), 2.05, 1.5,
			MATS["stone"], r, 10)
		cone("pillar_capital_%d" % index, (px, py, 14.75), 2.1, 1.48, 1.4,
			MATS["snow"], r, 10)
		cylinder("pillar_band_%d" % index, (px, py, 11.2), 1.62, .48,
			MATS["ice_deep"], r, 10)
		crystal_cluster(r, (px, py, 15.0), .75, "pillar_crown_%d" % index)
		next_angle = math.tau * float(index + 1) / 6.0
		nx, ny = math.cos(next_angle) * 14.5, math.sin(next_angle) * 10.8
		tube("hall_arch_%d" % index, [(px, py, 14.5),
			((px + nx) * .5, (py + ny) * .5, 17.8), (nx, ny, 14.5)],
			.2, MATS["ice_deep"], r)
	panel_xz("hall_star", [(0, 0), (.8, 1.5), (2.4, 1.8), (1.1, 2.8),
		(1.45, 4.5), (0, 3.5), (-1.45, 4.5), (-1.1, 2.8), (-2.4, 1.8),
		(-.8, 1.5)], .18, (0, -4.9, .4), MATS["gold"], r)
	return r


def build_bedroom_set() -> bpy.types.Object:
	r = root("northern_bedroom_set")
	# One authored cluster replaces the former box bed, cylinder rug and loose
	# generic furniture. Its footprint stays compact enough for all three bays.
	blob("braided_rug", (0, -.15, .12), (4.45, 4.95, .22), MATS["rose"], r, 1200)
	ring("rug_braid", (0, -.15, .28), 3.75, .22, MATS["gold"], r)
	blob("rug_snow_heart", (0, -.45, .32), (1.35, 1.7, .12), MATS["blue"], r, 1201)

	# Rounded timber/ice frame with crystal-capped corner posts.
	rounded_box("bed_frame", (0, 0, 1.15), (6.4, 7.2, 1.25),
		MATS["stone_light"], r, radius=.3)
	rounded_box("mattress", (0, -.1, 1.95), (5.6, 6.5, .72),
		MATS["cream"], r, radius=.34)
	for side in (-1.0, 1.0):
		for end in (-1.0, 1.0):
			x, y = side * 3.15, end * 3.45
			rounded_box("bed_post_%s_%s" % (side, end), (x, y, 2.15),
				(.58, .58, 4.3), MATS["mountain_blue"], r, radius=.16)
			cone("post_crystal_%s_%s" % (side, end), (x, y, 4.75),
				.62, .05, 1.25, MATS["ice"], r, 8)
		panel_xz("post_jewel_%s" % side,
			[(-.28, 0), (0, .38), (.28, 0), (0, -.38)], .12,
			(side * 3.15, -3.78, 2.4), MATS["gold"], r)

	# Tall arched headboard and lower footboard create the royal silhouette.
	panel_xz("crowned_headboard", [(-3.0, 0), (3.0, 0), (3.0, 4.1),
		(2.35, 5.25), (0, 6.35), (-2.35, 5.25), (-3.0, 4.1)],
		.55, (0, 3.3, .75), MATS["mountain_blue"], r)
	poly_tube("headboard_ice_trim", [(-2.75, 3.0, 4.1), (-2.15, 3.0, 5.65),
		(0, 3.0, 6.85), (2.15, 3.0, 5.65), (2.75, 3.0, 4.1)],
		.16, MATS["snow"], r)
	panel_xz("footboard", [(-3.0, 0), (3.0, 0), (3.0, 1.65),
		(0, 2.45), (-3.0, 1.65)], .48, (0, -3.48, .65),
		MATS["mountain_blue"], r)
	panel_xz("foot_crown", [(-.85, 0), (.85, 0), (.72, .8), (.32, .35),
		(0, 1.35), (-.32, .35), (-.72, .8)], .14,
		(0, -3.76, 1.15), MATS["gold"], r)

	# Broad quilt layers and pillows model softness without costly cloth sims.
	rounded_box("quilt_blue", (0, -.55, 2.43), (5.25, 4.85, .42),
		MATS["blue"], r, radius=.22)
	rounded_box("quilt_rose_fold", (0, .75, 2.68), (5.35, 1.35, .34),
		MATS["rose"], r, radius=.16)
	rounded_box("quilt_cream_fold", (0, 1.5, 2.82), (5.45, 1.0, .36),
		MATS["cream"], r, radius=.16)
	for index, x in enumerate((-1.45, 1.45)):
		pillow = rounded_box("pillow_%d" % index, (x, 2.0, 3.0),
			(2.35, 1.45, .68), MATS["wisp_b" if index == 0 else "rose"],
			r, (math.radians(-5), 0, math.radians(-4 if index == 0 else 4)), .3)
		pillow.rotation_euler.z = math.radians(-4 if index == 0 else 4)
		panel_xz("pillow_jewel_%d" % index,
			[(-.24, 0), (0, .32), (.24, 0), (0, -.32)], .1,
			(x, 1.22, 3.0), MATS["gold"], r)

	# Modeled snowflake on the headboard and quilt; no font or billboard.
	for prefix, y, z, scale in (("head", 2.98, 4.55, 1.0),
		("quilt", -3.0, 2.72, .72)):
		for arm in range(6):
			angle = math.tau * float(arm) / 6.0
			bar = rounded_box("%s_snow_arm_%d" % (prefix, arm), (0, y, z),
				(.12 * scale, .1, 1.35 * scale), MATS["snow"], r,
				(0, angle, 0), .035)
			bar.rotation_euler.y = angle
		blob("%s_snow_heart" % prefix, (0, y - .04, z),
			(.25 * scale, .14, .25 * scale), MATS["ice"], r, 1220 + int(scale * 10))

	# Warm lantern table and a compact shelf complete the lived-in vignette.
	rounded_box("bedside_table", (4.25, 1.75, 1.25), (2.0, 2.0, 2.5),
		MATS["wood_light"], r, radius=.22)
	rounded_box("table_runner", (4.25, .7, 2.55), (2.2, .85, .16),
		MATS["wisp_b"], r, radius=.06)
	cylinder("lantern_base", (4.25, 1.75, 2.9), .62, .3, MATS["gold"], r, 10)
	blob("lantern_glow", (4.25, 1.75, 3.55), (.62, .48, .82),
		MATS["window_warm"], r, 1230)
	cone("lantern_cap", (4.25, 1.75, 4.25), .72, .12, .5,
		MATS["gold"], r, 8)
	ring("lantern_handle", (4.25, 1.75, 4.65), .42, .08, MATS["gold"], r,
		(math.pi * .5, 0, 0))
	rounded_box("storybook_shelf", (-4.25, 1.1, 2.5), (2.15, 2.0, 5.0),
		MATS["mountain_blue"], r, radius=.24)
	for z in (1.45, 3.0, 4.55):
		rounded_box("shelf_%s" % z, (-4.25, -.02, z), (1.9, .28, .2),
			MATS["snow"], r, radius=.05)
	for index, (x, z, color) in enumerate(((-4.65, 1.95, "rose"),
		(-4.2, 2.0, "gold"), (-3.9, 3.55, "wisp_b"), (-4.45, 3.5, "aqua"))):
		rounded_box("storybook_%d" % index, (x, -.18, z), (.3, .22, .85),
			MATS[color], r, (0, 0, math.radians(-8 + index * 5)), .04)
	return r


ASSETS = {
	"northern_pass_arch": build_pass_arch(),
	"northern_peak_a": build_peak("northern_peak_a", 11, -.08),
	"northern_peak_b": build_peak("northern_peak_b", 37, .11),
	"northern_pine_a": build_pine("northern_pine_a", 0),
	"northern_pine_b": build_pine("northern_pine_b", 1),
	"northern_pine_c": build_pine("northern_pine_c", 2),
	"northern_mushrooms_red": build_mushrooms("northern_mushrooms_red", False),
	"northern_mushrooms_tan": build_mushrooms("northern_mushrooms_tan", True),
	"northern_house_red": build_house("northern_house_red", "red", "roof_blue", 0),
	"northern_house_amber": build_house("northern_house_amber", "amber", "roof_plum", 1),
	"northern_house_aqua": build_house("northern_house_aqua", "aqua", "roof_blue", 2),
	"northern_house_rose": build_house("northern_house_rose", "rose", "roof_plum", 3),
	"northern_house_blue": build_house("northern_house_blue", "blue", "roof_blue", 4),
	"northern_house_orange": build_house("northern_house_orange", "orange", "roof_plum", 5),
	"northern_fjord_dock": build_dock(),
	"northern_center_castle": build_castle(),
	"northern_wisp": build_wisp(),
	"northern_spirit_stone": build_spirit_stone(),
	"northern_log_bridge": build_log_bridge(),
	"northern_mill_house": build_mill_house(),
	"northern_mill_wheel": build_mill_wheel(),
	"northern_forge": build_forge(),
	"northern_street_lantern": build_street_lantern(),
	"northern_hall_centerpiece": build_hall_centerpiece(),
	"northern_bedroom_set": build_bedroom_set(),
}


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result += family(child)
	return result


def export_asset(name: str, obj: bpy.types.Object) -> int:
	# Keep the .blend fully editable, but collapse each runtime asset to one mesh
	# with material surfaces. This preserves the authored silhouette while
	# avoiding hundreds of tiny object submissions on Mali-G52.
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
	bpy.ops.export_scene.gltf(filepath=str(ASSET_OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False)
	bpy.data.objects.remove(merged, do_unlink=True)
	return runtime_triangles


def bounds(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	points = []
	for member in family(obj):
		if member.type == "MESH":
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	return (Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points))),
		Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points))))


def triangles(obj: bpy.types.Object) -> int:
	total = 0
	for member in family(obj):
		if member.type == "MESH":
			member.data.calc_loop_triangles()
			total += len(member.data.loop_triangles)
	return total


for asset_name, asset in ASSETS.items():
	if ONLY_ASSET != "" and asset_name != ONLY_ASSET:
		for member in family(asset):
			member.hide_render = True
		continue
	runtime_triangles = export_asset(asset_name, asset)
	lo, hi = bounds(asset)
	print("NORTH_KIT|%s|triangles=%d|bounds=%s..%s" % (asset_name, runtime_triangles,
		tuple(round(value, 2) for value in lo), tuple(round(value, 2) for value in hi)))
	for member in family(asset):
		member.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))

# Isolated Eevee QA renders catch inverted placement and weak silhouettes before
# the stricter in-game Mobile captures run.
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 780, 660, 100
scene.render.image_settings.file_format, scene.render.film_transparent = "PNG", True
scene.view_settings.look = "AgX - Medium High Contrast"
bpy.ops.object.camera_add(location=(12, -18, 10))
camera = bpy.context.active_object
camera.data.lens, scene.camera = 58, camera
for loc, energy, size, color in (((8, -10, 16), 1150, 8, (.85, .94, 1.0)),
	((-10, -4, 9), 780, 6, (.72, .82, 1.0)), ((4, 9, 12), 900, 6, (1.0, .76, .62))):
	bpy.ops.object.light_add(type="AREA", location=loc)
	light = bpy.context.active_object
	light.data.energy, light.data.shape, light.data.size, light.data.color = energy, "DISK", size, color
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(28), math.radians(-24), math.radians(-32)))
qa_sun = bpy.context.active_object
qa_sun.data.energy, qa_sun.data.color = 2.0, (0.86, 0.92, 1.0)
if scene.world is None:
	scene.world = bpy.data.worlds.new("Northern QA World")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.055, 0.075, 0.12, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .36

for asset_name, asset in ASSETS.items():
	if ONLY_ASSET != "" and asset_name != ONLY_ASSET:
		continue
	for member in family(asset):
		member.hide_render = False
	lo, hi = bounds(asset)
	center, size = (lo + hi) * .5, hi - lo
	distance = max(size.x, size.y, size.z) * 2.1
	if "house" in asset_name or "castle" in asset_name:
		camera.location = center + Vector((distance * .18, -distance * 1.42, distance * .52))
	else:
		camera.location = center + Vector((distance * .78, -distance * 1.32, distance * .64))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
	for member in family(asset):
		member.hide_render = True

print("NORTH_KIT|assets|%d" % (1 if ONLY_ASSET != "" else len(ASSETS)))
print("NORTH_KIT|blend|%s" % BLEND_OUT)
