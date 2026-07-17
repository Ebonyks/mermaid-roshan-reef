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
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "northern"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_northern_kingdom_kit"
BLEND_OUT = SOURCE_OUT / "northern_kingdom_kit.blend"
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"navy": (0.075, 0.085, 0.19, 1.0),
	"purple": (0.22, 0.18, 0.38, 1.0),
	"stone": (0.48, 0.53, 0.65, 1.0),
	"stone_light": (0.68, 0.72, 0.82, 1.0),
	"snow": (0.88, 0.95, 0.98, 1.0),
	"ice": (0.47, 0.82, 0.90, 1.0),
	"pine_dark": (0.13, 0.34, 0.34, 1.0),
	"pine": (0.22, 0.52, 0.43, 1.0),
	"pine_light": (0.43, 0.72, 0.55, 1.0),
	"wood": (0.43, 0.25, 0.18, 1.0),
	"wood_light": (0.67, 0.43, 0.28, 1.0),
	"cream": (0.94, 0.91, 0.80, 1.0),
	"gold": (0.94, 0.70, 0.22, 1.0),
	"glass": (0.43, 0.78, 0.88, 1.0),
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
	main = crag_mesh("hero_crag", 13.0, 5.2, seed, MATS["stone"], r)
	main.rotation_euler.x = lean
	spur = crag_mesh("side_crag", 8.0, 3.2, seed + 13, MATS["stone_light"], r)
	spur.location = (3.9 if lean < 0 else -3.8, .8, .15)
	spur.rotation_euler.y = -lean * 1.5
	crag_mesh("snow_crown", 4.0, 2.25, seed + 27, MATS["snow"], r, True).location.z = 9.5
	for index, (loc, scale) in enumerate((((-1.8, -.2, 8.9), (2.1, 1.0, .55)),
		((1.2, .4, 10.0), (1.8, 1.1, .48)), ((3.8, .9, 6.2), (1.5, .9, .42)))):
		blob("snow_shelf_%d" % index, loc, scale, MATS["snow"], r, seed + index)
	return r


def build_pass_arch() -> bpy.types.Object:
	r = root("northern_pass_arch")
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
	return r


def build_pine(name: str, variant: int) -> bpy.types.Object:
	r = root(name)
	height = 8.6 + variant * .7
	cylinder("trunk", (0, 0, height * .34), .48 + variant * .05, height * .68,
		MATS["wood"], r, 9)
	colors = (MATS["pine_dark"], MATS["pine"], MATS["pine_light"])
	for tier in range(3):
		pine_crown("crown_%d" % tier, (0, 0, 2.35 + tier * 2.25),
			3.15 - tier * .55 + variant * .1, 4.4 - tier * .25,
			colors[(tier + variant) % len(colors)], r, variant * .31 + tier * .17)
	for index, (x, y, z, sx) in enumerate(((-1.2, -.35, 5.2, 1.5),
		(1.05, .25, 7.0, 1.25), (-.4, .15, 8.8, .9))):
		blob("snow_pillow_%d" % index, (x, y, z + variant * .2),
			(sx, sx * .65, .34), MATS["snow"], r, variant * 10 + index)
	return r


def build_mushrooms(name: str, tan: bool) -> bpy.types.Object:
	r = root(name)
	cap_mat = MATS["mushroom_tan"] if tan else MATS["mushroom"]
	spots = ((-1.35, .15, 1.25, .8), (0, -.25, 1.8, 1.05), (1.35, .2, 1.05, .65),
		(.65, .7, .72, .43))
	for index, (x, y, height, radius) in enumerate(spots):
		cylinder("stem_%d" % index, (x, y, height * .5), radius * .24,
			height, MATS["cream"], r, 9)
		cap = blob("cap_%d" % index, (x, y, height + radius * .22),
			(radius, radius * .82, radius * .42), cap_mat, r, 100 + index)
		cap.rotation_euler.z = (-.1 + index * .07)
		if not tan:
			for spot in range(3):
				angle = math.tau * spot / 3.0 + index
				blob("dot_%d_%d" % (index, spot),
					(x + math.cos(angle) * radius * .44, y + math.sin(angle) * radius * .38,
					height + radius * .52), (radius * .12, radius * .08, radius * .05),
					MATS["snow"], r, 140 + index * 3 + spot)
	return r


def build_house(name: str, body_key: str, roof_key: str, variant: int) -> bpy.types.Object:
	r = root(name)
	width = 8.2 + (variant % 3) * .55
	depth = 6.7 + (variant % 2) * .55
	body_h = 5.2 + (variant % 2) * .35
	rise = 3.9 + (variant % 3) * .28
	body_mat, roof_mat = MATS[body_key], MATS[roof_key]
	rounded_box("painted_timber_body", (0, 0, body_h * .5), (width, depth, body_h),
		body_mat, r, radius=.32)
	panel_xz("front_gable", [(-width * .5, 0), (width * .5, 0), (0, rise)], .42,
		(0, -depth * .5 - .04, body_h), body_mat, r)
	panel_xz("back_gable", [(-width * .5, 0), (width * .5, 0), (0, rise)], .42,
		(0, depth * .5 + .04, body_h), body_mat, r)
	slope = math.atan2(rise, width * .5)
	roof_len = math.sqrt((width * .5) ** 2 + rise ** 2) + .75
	for side in (-1.0, 1.0):
		rounded_box("roof_%s" % ("l" if side < 0 else "r"),
			(side * width * .245, 0, body_h + rise * .52),
			(roof_len, depth + 1.0, .52), roof_mat, r,
			(0.0, side * slope, 0.0), .16)
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
	# Oversized door and blue-glass windows remain readable at gameplay distance.
	panel_xz("carved_door", [(-.8, 0), (.8, 0), (.8, 2.35), (0, 2.95), (-.8, 2.35)],
		.34, (-width * .22 if variant % 2 else width * .22, -depth * .54, .05),
		MATS["wood_light"], r)
	for index, x in enumerate((-width * .27, width * .27)):
		if (variant % 2 == 0 and index == 1) or (variant % 2 == 1 and index == 0):
			continue
		rounded_box("window_%d" % index, (x, -depth * .545, 2.65),
			(1.55, .26, 1.55), MATS["glass"], r, radius=.18)
		rounded_box("window_cross_v_%d" % index, (x, -depth * .57, 2.65),
			(.14, .12, 1.48), MATS["cream"], r, radius=.04)
		rounded_box("window_cross_h_%d" % index, (x, -depth * .57, 2.65),
			(1.48, .12, .14), MATS["cream"], r, radius=.04)
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
	return r


def build_dock() -> bpy.types.Object:
	r = root("northern_fjord_dock")
	for index in range(14):
		x = -7.8 + index * 1.2
		plank = rounded_box("plank_%02d" % index, (x, 0, .45 + (index % 3 - 1) * .035),
			(1.05, 2.8, .38), MATS["wood_light"] if index % 3 else MATS["wood"], r, radius=.09)
		plank.rotation_euler.z = (index % 2 - .5) * .012
	for x in (-7.9, -2.7, 2.7, 7.9):
		for y in (-1.15, 1.15):
			cylinder("post_%.1f_%.1f" % (x, y), (x, y, .25), .24, 3.4, MATS["wood"], r, 9)
	for side in (-1.0, 1.0):
		for section, (x0, x1) in enumerate(((-7.9, -2.7), (-2.7, 2.7), (2.7, 7.9))):
			tube("rope_%s_%d" % ("l" if side < 0 else "r", section),
				[(x0, side * 1.15, 1.55), ((x0 + x1) * .5, side * 1.15, .92),
				(x1, side * 1.15, 1.55)], .075, MATS["cream"], r)
	# Child-readable carved prow marker.
	panel_xz("dock_fish_sign", [(-.75, 0), (.35, 0), (1.0, .55), (.35, 1.1), (-.75, 1.1),
		(-1.15, .55)], .22, (7.15, -1.45, 1.75), MATS["aqua"], r)
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
	# Keep: stepped silhouette, gabled hall, bay towers, big readable doorway.
	rounded_box("keep_body", (0, 8, 10), (26, 20, 20), MATS["stone_light"], r, radius=.65)
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
	panel_xz("great_door", [(-3, 0), (3, 0), (3, 5.2), (0, 8.2), (-3, 5.2)],
		.45, (0, -2.25, .05), MATS["wood_light"], r)
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
	for index in range(5):
		angle = math.tau * index / 5.0
		blob("wisp_mote_%d" % index,
			(math.cos(angle) * 1.35, math.sin(angle) * 1.35, .9 + (index % 2) * .35),
			(.18, .18, .28), MATS["wisp_a"] if index % 2 == 0 else MATS["wisp_b"], r, index)
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

print("NORTH_KIT|assets|%d" % len(ASSETS))
print("NORTH_KIT|blend|%s" % BLEND_OUT)
