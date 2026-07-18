#!/usr/bin/env python3
"""Build the authored pearl-castle architecture and furnishing kit.

The kit replaces visible engine primitives in the Grand Hall while preserving
the existing navigation, collision, protected book art, and light budget.
Every runtime prop is exported as one mesh with flat material surfaces for the
Mobile renderer.

Usage: blender --background --python tools/build_pearl_castle_kit.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "castle" / "pearl_kit"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_pearl_castle_kit"
BLEND_OUT = SOURCE_OUT / "pearl_castle_kit.blend"
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"ink": (0.10, 0.08, 0.22, 1.0),
	"plum": (0.31, 0.22, 0.43, 1.0),
	"lavender": (0.66, 0.55, 0.76, 1.0),
	"pearl_shadow": (0.72, 0.70, 0.79, 1.0),
	"pearl": (0.91, 0.88, 0.83, 1.0),
	"pearl_light": (1.0, 0.95, 0.84, 1.0),
	"gold": (0.92, 0.66, 0.22, 1.0),
	"coral": (0.89, 0.43, 0.47, 1.0),
	"peach": (0.96, 0.65, 0.48, 1.0),
	"yellow": (0.96, 0.80, 0.35, 1.0),
	"mint": (0.48, 0.77, 0.62, 1.0),
	"aqua": (0.30, 0.72, 0.76, 1.0),
	"sky": (0.43, 0.64, 0.86, 1.0),
	"rose": (0.80, 0.51, 0.68, 1.0),
	"leaf_dark": (0.19, 0.46, 0.40, 1.0),
	"leaf": (0.35, 0.66, 0.50, 1.0),
	"water": (0.24, 0.70, 0.78, 1.0),
}


def make_material(name: str, color: tuple[float, float, float, float],
		roughness: float = 0.82, metallic: float = 0.0,
		emission: float = 0.0) -> bpy.types.Material:
	mat = bpy.data.materials.new("MRC_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = roughness
	bsdf.inputs["Metallic"].default_value = metallic
	if emission > 0.0 and "Emission Color" in bsdf.inputs:
		bsdf.inputs["Emission Color"].default_value = color
		bsdf.inputs["Emission Strength"].default_value = emission
	return mat


MATS = {name: make_material(name, color) for name, color in PALETTE.items()}
MATS["gold"] = make_material("gold", PALETTE["gold"], 0.46, 0.18)
for glow_name in ("coral", "yellow", "mint", "aqua", "sky", "rose", "water"):
	MATS[glow_name] = make_material(glow_name, PALETTE[glow_name], 0.72, 0.0, 0.06)


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def assign(obj: bpy.types.Object, mat: bpy.types.Material,
		parent: bpy.types.Object) -> bpy.types.Object:
	obj.data.materials.append(mat)
	obj.parent = parent
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def rounded_box(name: str, loc: tuple[float, float, float],
		size: tuple[float, float, float], mat: bpy.types.Material,
		parent: bpy.types.Object, radius: float = 0.16,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	bevel = obj.modifiers.new("storybook_rounding", "BEVEL")
	bevel.width = min(radius, min(size) * 0.18)
	bevel.segments = 2
	bevel.limit_method = "ANGLE"
	apply_modifier(obj, bevel)
	return obj


def cylinder(name: str, loc: tuple[float, float, float], radius: float,
		depth: float, mat: bpy.types.Material, parent: bpy.types.Object,
		vertices: int = 16,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius,
		depth=depth, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	bevel = obj.modifiers.new("soft_profile", "BEVEL")
	bevel.width = min(radius * 0.12, depth * 0.08, 0.16)
	bevel.segments = 2
	apply_modifier(obj, bevel)
	return obj


def cone(name: str, loc: tuple[float, float, float], bottom: float, top: float,
		depth: float, mat: bpy.types.Material, parent: bpy.types.Object,
		vertices: int = 16) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=bottom,
		radius2=top, depth=depth, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	bevel = obj.modifiers.new("soft_profile", "BEVEL")
	bevel.width = min(max(top, 0.2) * 0.12, 0.13)
	bevel.segments = 2
	apply_modifier(obj, bevel)
	return obj


def ellipsoid(name: str, loc: tuple[float, float, float],
		scale: tuple[float, float, float], mat: bpy.types.Material,
		parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0,
		location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def torus(name: str, loc: tuple[float, float, float], major: float, minor: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
		major_segments: int = 24) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
		major_segments=major_segments, minor_segments=6, location=loc,
		rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def tube(name: str, points: list[tuple[float, float, float]], radius: float,
		mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions = "3D"
	curve.resolution_u = 2
	curve.bevel_depth = radius
	curve.bevel_resolution = 2
	curve.use_fill_caps = True
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


def arc_tube(name: str, center: tuple[float, float, float], radius: float,
		tube_radius: float, mat: bpy.types.Material, parent: bpy.types.Object,
		start: float = 0.0, end: float = math.pi, steps: int = 13) -> bpy.types.Object:
	points = []
	for index in range(steps):
		a = start + (end - start) * float(index) / float(steps - 1)
		points.append((center[0] + math.cos(a) * radius, center[1],
			center[2] + math.sin(a) * radius))
	return tube(name, points, tube_radius, mat, parent)


def panel_xz(name: str, outline: list[tuple[float, float]], depth: float,
		loc: tuple[float, float, float], mat: bpy.types.Material,
		parent: bpy.types.Object, bevel_width: float = 0.08) -> bpy.types.Object:
	vertices = [(x, -depth * 0.5, z) for x, z in outline]
	vertices += [(x, depth * 0.5, z) for x, z in outline]
	count = len(outline)
	faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, count * 2))]
	faces += [(i, (i + 1) % count, count + (i + 1) % count, count + i)
		for i in range(count)]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(vertices, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = loc
	assign(obj, mat, parent)
	bevel = obj.modifiers.new("rounded_profile", "BEVEL")
	bevel.width = bevel_width
	bevel.segments = 2
	apply_modifier(obj, bevel)
	return obj


def shell_fan(name: str, loc: tuple[float, float, float], size: float,
		parent: bpy.types.Object, face_rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
		lobe_mat: bpy.types.Material | None = None,
		shadow_mat: bpy.types.Material | None = None) -> bpy.types.Object:
	fan = root(name)
	fan.parent = parent
	fan.location = loc
	fan.rotation_euler = face_rotation
	lobe_material = lobe_mat or MATS["pearl_light"]
	shadow_material = shadow_mat or MATS["lavender"]
	for index, degrees in enumerate((-48.0, -24.0, 0.0, 24.0, 48.0)):
		a = math.radians(degrees)
		ellipsoid(
			name + "_Lobe_%d" % index,
			(math.sin(a) * size * 0.23, -size * 0.025, math.cos(a) * size * 0.18),
			(size * 0.21, size * 0.095, size * 0.48),
			lobe_material, fan, (0.0, a, 0.0),
		)
	ellipsoid(name + "_Foot", (0.0, 0.0, -size * 0.25),
		(size * 0.46, size * 0.16, size * 0.20), shadow_material, fan)
	ellipsoid(name + "_Pearl", (0.0, -size * 0.11, size * 0.10),
		(size * 0.13, size * 0.13, size * 0.13), MATS["pearl"], fan)
	return fan


def sector_prism(name: str, inner: float, outer: float, start: float, end: float,
		z_bottom: float, z_top: float, mat: bpy.types.Material,
		parent: bpy.types.Object, steps: int = 8) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	for z in (z_bottom, z_top):
		for radius in (inner, outer):
			for index in range(steps):
				a = start + (end - start) * float(index) / float(steps - 1)
				vertices.append((math.cos(a) * radius, math.sin(a) * radius, z))
	faces: list[tuple[int, ...]] = []
	stride = steps * 2
	for index in range(steps - 1):
		i0, i1 = index, index + 1
		o0, o1 = steps + index, steps + index + 1
		faces.extend([
			(i0, o0, o1, i1),
			(stride + i1, stride + o1, stride + o0, stride + i0),
			(i0, i1, stride + i1, stride + i0),
			(o1, o0, stride + o0, stride + o1),
		])
	faces.extend([
		(0, steps, stride + steps, stride),
		(steps - 1, stride - 1, stride * 2 - 1, stride + steps - 1),
	])
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(vertices, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	assign(obj, mat, parent)
	return obj


def build_column() -> bpy.types.Object:
	r = root("pearl_column")
	cylinder("Column_InkFoot", (0.0, 0.0, 0.45), 2.75, 0.9, MATS["ink"], r, 20)
	cylinder("Column_GoldBase", (0.0, 0.0, 1.05), 2.55, 1.0, MATS["gold"], r, 20)
	cylinder("Column_PearlBase", (0.0, 0.0, 1.75), 2.15, 0.8, MATS["pearl_light"], r, 20)
	cone("Column_Shaft", (0.0, 0.0, 17.0), 1.65, 1.42, 29.8, MATS["pearl"], r, 20)
	for index in range(8):
		a = math.tau * float(index) / 8.0
		cylinder("Column_Flute_%d" % index,
			(math.cos(a) * 1.48, math.sin(a) * 1.48, 17.0),
			0.18, 28.2, MATS["pearl_light"] if index % 2 == 0 else MATS["pearl_shadow"], r, 8)
	cylinder("Column_Neck", (0.0, 0.0, 32.0), 1.85, 0.8, MATS["gold"], r, 20)
	cylinder("Column_Capital", (0.0, 0.0, 33.15), 2.65, 1.5, MATS["pearl_light"], r, 20)
	for yaw in (0.0, math.pi * 0.5, math.pi, math.pi * 1.5):
		shell_fan("Column_Shell",
			(math.sin(yaw) * 2.48, -math.cos(yaw) * 2.48, 32.85), 1.35, r,
			(0.0, 0.0, yaw), MATS["pearl_light"], MATS["lavender"])
	cylinder("Column_Crown", (0.0, 0.0, 33.85), 2.90, 0.3, MATS["gold"], r, 20)
	return r


def build_balustrade() -> bpy.types.Object:
	r = root("pearl_balustrade")
	rounded_box("Balustrade_InkFoot", (0.0, 0.0, 0.20), (9.0, 0.82, 0.40), MATS["ink"], r, 0.18)
	rounded_box("Balustrade_PearlFoot", (0.0, 0.0, 0.48), (9.0, 0.72, 0.32), MATS["pearl"], r, 0.14)
	rounded_box("Balustrade_GoldRail", (0.0, 0.0, 3.02), (9.0, 0.80, 0.50), MATS["gold"], r, 0.20)
	for index, x in enumerate((-4.1, -2.65, -1.32, 0.0, 1.32, 2.65, 4.1)):
		cone("Balustrade_Stem_%d" % index, (x, 0.0, 1.60), 0.42, 0.29, 2.15,
			MATS["pearl"] if index % 2 == 0 else MATS["pearl_shadow"], r, 12)
		shell_fan("Balustrade_Shell_%d" % index, (x, -0.37, 2.20), 0.56, r,
			lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_shell_arch() -> bpy.types.Object:
	r = root("pearl_shell_arch")
	for x in (-4.65, 4.65):
		rounded_box("Arch_InkPost", (x, 0.0, 4.65), (1.55, 1.28, 9.3), MATS["ink"], r, 0.26)
		rounded_box("Arch_PearlPost", (x, -0.03, 4.65), (1.18, 1.38, 9.3), MATS["pearl"], r, 0.23)
		cylinder("Arch_GoldFoot", (x, 0.0, 0.55), 1.18, 1.1, MATS["gold"], r, 16)
	arc_tube("Arch_InkCurve", (0.0, 0.0, 9.2), 4.65, 0.92, MATS["ink"], r)
	arc_tube("Arch_PearlCurve", (0.0, -0.03, 9.2), 4.65, 0.68, MATS["pearl_light"], r)
	arc_tube("Arch_GoldInlay", (0.0, -0.73, 9.2), 4.65, 0.13, MATS["gold"], r)
	shell_fan("Arch_KeystoneShell", (0.0, -0.72, 14.05), 1.65, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_rainbow_window() -> bpy.types.Object:
	r = root("pearl_rainbow_window")
	outline = [(-6.25, 0.0), (-6.25, 5.8)]
	for index in range(13):
		a = math.pi - math.pi * float(index) / 12.0
		outline.append((math.cos(a) * 6.25, 5.8 + math.sin(a) * 6.25))
	outline.extend([(6.25, 0.0)])
	panel_xz("Window_InkGlass", outline, 0.34, (0.0, 0.0, 0.0), MATS["ink"], r, 0.12)
	colors = ("coral", "peach", "yellow", "mint", "aqua", "sky", "rose")
	for index, color in enumerate(colors):
		radius = 5.45 - float(index) * 0.64
		arc_tube("Window_Rainbow_%s" % color, (0.0, -0.24, 5.72), radius,
			0.35, MATS[color], r, 0.04, math.pi - 0.04, 17)
	for x in (-5.75, 5.75):
		rounded_box("Window_PearlJamb", (x, -0.22, 2.9), (0.72, 0.60, 5.8), MATS["pearl_light"], r, 0.15)
	rounded_box("Window_GoldSill", (0.0, -0.22, 0.30), (12.4, 0.72, 0.60), MATS["gold"], r, 0.18)
	arc_tube("Window_PearlFrame", (0.0, -0.22, 5.8), 6.05, 0.48, MATS["pearl_light"], r, steps=17)
	shell_fan("Window_CenterShell", (0.0, -0.64, 2.0), 2.1, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_sconce() -> bpy.types.Object:
	r = root("pearl_shell_sconce")
	ellipsoid("Sconce_InkPlaque", (0.0, 0.10, 0.0), (1.38, 0.24, 1.58), MATS["ink"], r)
	shell_fan("Sconce_Shell", (0.0, -0.20, 0.02), 1.58, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	for side in (-1.0, 1.0):
		tube("Sconce_GoldCradle", [(side * 0.62, -0.42, -0.18),
			(side * 0.50, -0.92, 0.22), (side * 0.24, -1.18, 0.42)],
			0.09, MATS["gold"], r)
	ellipsoid("Sconce_GoldCup", (0.0, -1.05, 0.20), (0.48, 0.28, 0.18), MATS["gold"], r)
	ellipsoid("Sconce_PearlLight", (0.0, -1.22, 0.44), (0.28, 0.28, 0.32), MATS["yellow"], r)
	return r


def build_chandelier() -> bpy.types.Object:
	r = root("pearl_shell_chandelier")
	tube("Chandelier_Chain", [(0.0, 0.0, 2.4), (0.0, 0.0, 0.6)], 0.10, MATS["gold"], r)
	torus("Chandelier_InkRing", (0.0, 0.0, -0.15), 3.05, 0.24, MATS["ink"], r, major_segments=28)
	torus("Chandelier_GoldRing", (0.0, 0.0, -0.08), 2.95, 0.15, MATS["gold"], r, major_segments=28)
	for index in range(6):
		a = math.tau * float(index) / 6.0
		x, y = math.cos(a) * 2.90, math.sin(a) * 2.90
		tube("Chandelier_Arm_%d" % index, [(0.0, 0.0, 0.55), (x * 0.70, y * 0.70, 0.18),
			(x, y, -0.08)], 0.09, MATS["gold"], r)
		shell_fan("Chandelier_Shell_%d" % index, (x, y, -0.35), 0.78, r,
			(0.0, 0.0, a + math.pi * 0.5), MATS["pearl_light"], MATS["lavender"])
		ellipsoid("Chandelier_Pearl_%d" % index, (x, y, -0.82), (0.30, 0.30, 0.38), MATS["yellow"], r)
	ellipsoid("Chandelier_CenterPearl", (0.0, 0.0, -0.85), (0.62, 0.62, 0.78), MATS["aqua"], r)
	return r


def build_floor_medallion() -> bpy.types.Object:
	r = root("pearl_floor_medallion")
	cylinder("Medallion_Ink", (0.0, 0.0, 0.06), 5.2, 0.12, MATS["ink"], r, 32)
	cylinder("Medallion_Pearl", (0.0, 0.0, 0.14), 4.85, 0.16, MATS["pearl"], r, 32)
	colors = ("coral", "peach", "yellow", "mint", "aqua", "sky", "rose")
	span = math.tau / float(len(colors))
	for index, color in enumerate(colors):
		start = float(index) * span + 0.035
		sector_prism("Medallion_Ray_%s" % color, 1.45, 4.45, start,
			start + span - 0.07, 0.22, 0.31, MATS[color], r)
	torus("Medallion_GoldRing", (0.0, 0.0, 0.34), 4.65, 0.11, MATS["gold"], r, major_segments=32)
	shell_fan("Medallion_Shell", (0.0, 0.0, 0.47), 1.55, r,
		(math.pi * 0.5, 0.0, 0.0), MATS["pearl_light"], MATS["lavender"])
	return r


def build_throne_canopy() -> bpy.types.Object:
	r = root("pearl_throne_canopy")
	for x in (-6.6, 6.6):
		rounded_box("Canopy_InkPier", (x, 0.0, 7.0), (1.55, 1.65, 14.0), MATS["ink"], r, 0.26)
		rounded_box("Canopy_PearlPier", (x, -0.10, 7.0), (1.10, 1.72, 13.6), MATS["pearl"], r, 0.23)
		cylinder("Canopy_GoldFoot", (x, 0.0, 0.65), 1.25, 1.3, MATS["gold"], r, 18)
	arc_tube("Canopy_InkHood", (0.0, 0.0, 13.2), 6.6, 0.95, MATS["ink"], r, steps=17)
	arc_tube("Canopy_PearlHood", (0.0, -0.08, 13.2), 6.6, 0.67, MATS["pearl_light"], r, steps=17)
	arc_tube("Canopy_GoldInlay", (0.0, -0.76, 13.2), 5.42, 0.18,
		MATS["gold"], r, 0.20, math.pi - 0.20, 15)
	shell_fan("Canopy_CrownShell", (0.0, -0.78, 19.55), 2.15, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_throne() -> bpy.types.Object:
	"""A shell-backed throne whose rails never cross the seated character."""
	r = root("pearl_shell_throne")
	outer = [(-4.35, 1.75), (-4.35, 6.70), (-3.78, 8.65), (-2.35, 10.25),
		(0.0, 11.25), (2.35, 10.25), (3.78, 8.65), (4.35, 6.70), (4.35, 1.75)]
	inner = [(-3.82, 2.05), (-3.82, 6.55), (-3.28, 8.18), (-2.00, 9.55),
		(0.0, 10.38), (2.00, 9.55), (3.28, 8.18), (3.82, 6.55), (3.82, 2.05)]
	panel_xz("Throne_InkBack", outer, 0.72, (0.0, 1.34, 0.0), MATS["ink"], r, 0.18)
	panel_xz("Throne_PearlBack", inner, 0.78, (0.0, 1.00, 0.0), MATS["plum"], r, 0.16)
	for index, x in enumerate((-3.0, -1.5, 0.0, 1.5, 3.0)):
		tube("Throne_ShellRib_%d" % index,
			[(0.0, 0.54, 2.55), (x * 0.52, 0.52, 6.20), (x, 0.50, 9.10 - abs(x) * 0.18)],
			0.13, MATS["gold"] if index % 2 == 0 else MATS["pearl_light"], r)
	rounded_box("Throne_InkPlinth", (0.0, -0.35, 0.42), (8.5, 4.25, 0.84), MATS["ink"], r, 0.26)
	rounded_box("Throne_GoldPlinth", (0.0, -0.42, 0.90), (7.9, 3.85, 0.48), MATS["gold"], r, 0.22)
	rounded_box("Throne_PearlSeat", (0.0, -0.62, 1.78), (6.45, 3.35, 1.28), MATS["pearl"], r, 0.36)
	rounded_box("Throne_RoseCushion", (0.0, -0.78, 2.48), (5.85, 2.92, 0.50), MATS["rose"], r, 0.28)
	for x in (-3.18, 3.18):
		rounded_box("Throne_Arm", (x, -0.72, 3.18), (0.72, 2.72, 2.20), MATS["pearl_light"], r, 0.28)
		shell_fan("Throne_ArmShell", (x, -2.00, 4.22), 1.18, r,
			lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	shell_fan("Throne_CrestShell", (0.0, 0.45, 10.05), 2.25, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_planter() -> bpy.types.Object:
	r = root("pearl_shell_planter")
	cylinder("Planter_InkFoot", (0.0, 0.0, 0.28), 1.75, 0.55, MATS["ink"], r, 18)
	cone("Planter_PearlBowl", (0.0, 0.0, 1.45), 1.55, 2.05, 2.35, MATS["pearl"], r, 18)
	torus("Planter_GoldRim", (0.0, 0.0, 2.62), 1.88, 0.16, MATS["gold"], r, major_segments=22)
	for yaw in (0.0, math.pi * 0.5, math.pi, math.pi * 1.5):
		shell_fan("Planter_Shell",
			(math.sin(yaw) * 1.76, -math.cos(yaw) * 1.76, 1.48), 0.82, r,
			(0.0, 0.0, yaw), MATS["pearl_light"], MATS["lavender"])
	for index in range(7):
		a = math.tau * float(index) / 7.0
		ellipsoid("Planter_Leaf_%d" % index,
			(math.cos(a) * 0.70, math.sin(a) * 0.70, 3.55 + float(index % 2) * 0.34),
			(0.34, 0.18, 1.45), MATS["leaf"] if index % 2 == 0 else MATS["leaf_dark"], r,
			(0.0, math.sin(a) * 0.38, -math.cos(a) * 0.38))
	return r


def build_bench() -> bpy.types.Object:
	r = root("pearl_shell_bench")
	rounded_box("Bench_InkSeat", (0.0, 0.0, 2.1), (8.0, 2.6, 0.62), MATS["ink"], r, 0.24)
	rounded_box("Bench_RoseCushion", (0.0, -0.05, 2.46), (7.5, 2.35, 0.52), MATS["rose"], r, 0.26)
	for x in (-3.25, 3.25):
		cylinder("Bench_GoldLeg", (x, 0.0, 1.05), 0.42, 2.1, MATS["gold"], r, 14)
		shell_fan("Bench_SideShell", (x, -1.22, 3.30), 1.15, r,
			lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	rounded_box("Bench_PearlBack", (0.0, 1.05, 4.55), (7.3, 0.55, 3.7), MATS["pearl"], r, 0.32)
	for index, color in enumerate(("coral", "yellow", "mint", "aqua", "rose")):
		arc_tube("Bench_Rainbow_%s" % color, (0.0, 0.72, 3.55),
			2.85 - float(index) * 0.42, 0.14, MATS[color], r, 0.15, math.pi - 0.15, 11)
	return r


def build_cloud_settee() -> bpy.types.Object:
	"""Purpose-built lounge seating with a cloud silhouette and explicit seat."""
	r = root("pearl_cloud_settee")
	for x in (-3.55, 3.55):
		cylinder("CloudSettee_GoldFoot", (x, 0.22, 0.62), 0.38, 1.24, MATS["gold"], r, 14)
	rounded_box("CloudSettee_InkBase", (0.0, 0.0, 1.30), (9.0, 3.45, 1.15), MATS["ink"], r, 0.40)
	rounded_box("CloudSettee_AquaSeat", (0.0, -0.20, 2.02), (8.35, 3.02, 0.62), MATS["aqua"], r, 0.34)
	cloud_lobes = [(-3.35, 3.95, 1.55), (-1.75, 4.55, 1.90), (0.0, 4.90, 2.12),
		(1.75, 4.55, 1.90), (3.35, 3.95, 1.55)]
	for index, (x, z, scale) in enumerate(cloud_lobes):
		ellipsoid("CloudSettee_Shadow_%d" % index, (x, 1.12, z - 0.30),
			(scale * 0.96, 0.56, scale * 0.84), MATS["lavender"], r)
		ellipsoid("CloudSettee_Lobe_%d" % index, (x, 0.78, z),
			(scale, 0.58, scale * 0.88), MATS["pearl_light"], r)
	for x in (-4.05, 4.05):
		ellipsoid("CloudSettee_Arm", (x, -0.28, 2.85), (0.95, 1.36, 1.18), MATS["pearl"], r)
		shell_fan("CloudSettee_ArmShell", (x, -1.48, 3.02), 0.86, r,
			lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	for index, color in enumerate(("coral", "yellow", "mint", "aqua", "rose")):
		arc_tube("CloudSettee_Rainbow_%s" % color, (0.0, -0.86, 3.90),
			2.62 - float(index) * 0.43, 0.12, MATS[color], r, 0.18, math.pi - 0.18, 11)
	return r


def build_cloud_pouf() -> bpy.types.Object:
	r = root("pearl_cloud_pouf")
	for index, (x, y) in enumerate(((-1.25, -0.42), (-0.62, 0.54), (0.55, 0.58), (1.28, -0.35), (0.0, -0.76))):
		ellipsoid("CloudPouf_Lobe_%d" % index, (x, y, 1.18),
			(1.18, 0.92, 0.86), MATS["pearl_light"] if index % 2 == 0 else MATS["pearl"], r)
	cylinder("CloudPouf_InkFoot", (0.0, 0.0, 0.30), 1.82, 0.60, MATS["ink"], r, 18)
	cylinder("CloudPouf_GoldBand", (0.0, 0.0, 0.62), 1.68, 0.30, MATS["gold"], r, 18)
	ellipsoid("CloudPouf_RoseCushion", (0.0, -0.10, 1.62), (1.52, 1.18, 0.48), MATS["rose"], r)
	shell_fan("CloudPouf_Shell", (0.0, -1.08, 1.20), 0.82, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_fountain() -> bpy.types.Object:
	r = root("pearl_shell_fountain")
	cylinder("Fountain_InkBase", (0.0, 0.0, 0.32), 2.85, 0.64, MATS["ink"], r, 24)
	cylinder("Fountain_GoldBase", (0.0, 0.0, 0.72), 2.55, 0.42, MATS["gold"], r, 24)
	cone("Fountain_PearlStem", (0.0, 0.0, 2.15), 1.30, 0.80, 2.65, MATS["pearl"], r, 18)
	cylinder("Fountain_Basin", (0.0, 0.0, 3.35), 2.85, 0.55, MATS["pearl_light"], r, 24)
	cylinder("Fountain_Water", (0.0, 0.0, 3.68), 2.45, 0.11, MATS["water"], r, 24)
	shell_fan("Fountain_BackShell", (0.0, 0.55, 5.35), 2.45, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	ellipsoid("Fountain_Pearl", (0.0, -0.40, 4.25), (0.52, 0.52, 0.52), MATS["pearl_light"], r)
	tube("Fountain_WaterArc", [(0.0, -0.28, 4.45), (0.0, -0.62, 4.12),
		(0.0, -0.55, 3.78)], 0.09, MATS["water"], r)
	return r


def build_rainbow_gate() -> bpy.types.Object:
	r = root("pearl_rainbow_gate")
	for x in (-4.25, 4.25):
		rounded_box("Gate_PearlPost", (x, 0.0, 3.8), (1.05, 1.15, 7.6), MATS["pearl"], r, 0.22)
		cylinder("Gate_GoldFoot", (x, 0.0, 0.52), 1.05, 1.04, MATS["gold"], r, 16)
	arc_tube("Gate_InkFrame", (0.0, 0.0, 7.55), 4.25, 0.76, MATS["ink"], r, steps=15)
	for index, color in enumerate(("coral", "yellow", "mint", "aqua", "rose")):
		arc_tube("Gate_Rainbow_%s" % color, (0.0, -0.18, 7.55),
			4.15 - float(index) * 0.46, 0.20, MATS[color], r, 0.06, math.pi - 0.06, 15)
	arc_tube("Gate_PearlFrame", (0.0, -0.12, 7.55), 4.25, 0.46, MATS["pearl_light"], r, steps=15)
	shell_fan("Gate_KeystoneShell", (0.0, -0.62, 12.15), 1.45, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_banner(name: str, alternate: bool) -> bpy.types.Object:
	r = root(name)
	back_mat = MATS["aqua"] if alternate else MATS["plum"]
	edge_mat = MATS["pearl_light"] if alternate else MATS["gold"]
	outline = [(-3.0, 0.8), (-2.45, 0.0), (-1.65, 0.62), (-0.82, 0.0),
		(0.0, 0.65), (0.82, 0.0), (1.65, 0.62), (2.45, 0.0), (3.0, 0.8),
		(3.0, 12.0), (-3.0, 12.0)]
	panel_xz("Banner_Cloth", outline, 0.24, (0.0, 0.0, 0.0), back_mat, r, 0.10)
	cylinder("Banner_GoldRod", (0.0, 0.0, 12.35), 0.20, 7.2, MATS["gold"], r, 14,
		(0.0, math.pi * 0.5, 0.0))
	for x in (-3.25, 3.25):
		ellipsoid("Banner_RodPearl", (x, 0.0, 12.35), (0.36, 0.36, 0.36), MATS["pearl_light"], r)
	shell_fan("Banner_Crest", (0.0, -0.34, 8.55), 1.55, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	for index, (color, height) in enumerate((("mint", 4.70), ("sky", 3.72), ("rose", 2.76))):
		tube("Banner_Wave_%d" % index,
			[(-2.25, -0.27, height), (-1.10, -0.38, height + 0.42),
				(0.0, -0.38, height), (1.10, -0.38, height - 0.42),
				(2.25, -0.27, height)],
			0.13, MATS[color] if alternate else edge_mat, r)
	return r


def build_stair_rail() -> bpy.types.Object:
	r = root("pearl_stair_rail")
	bottom_points = [(0.0, 0.0, 0.62), (0.0, 15.0, 12.62)]
	top_points = [(0.0, 0.0, 2.65), (0.0, 15.0, 14.65)]
	tube("StairRail_InkBase", bottom_points, 0.27, MATS["ink"], r)
	tube("StairRail_GoldTop", top_points, 0.30, MATS["gold"], r)
	for index in range(6):
		y = float(index) * 3.0
		z = 0.62 + y * 0.8
		cylinder("StairRail_PearlPost_%d" % index, (0.0, y, z + 1.05),
			0.28, 2.1, MATS["pearl"] if index % 2 == 0 else MATS["pearl_shadow"], r, 12)
		shell_fan("StairRail_Shell_%d" % index, (0.0, y - 0.24, z + 1.55), 0.55, r,
			lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	for y in (0.0, 15.0):
		z = 0.62 + y * 0.8
		cylinder("StairRail_Newel", (0.0, y, z + 1.28), 0.55, 2.55, MATS["pearl_light"], r, 16)
		ellipsoid("StairRail_NewelPearl", (0.0, y, z + 2.72), (0.52, 0.52, 0.52), MATS["gold"], r)
	return r


ASSETS = {
	"pearl_column": build_column(),
	"pearl_balustrade": build_balustrade(),
	"pearl_shell_arch": build_shell_arch(),
	"pearl_rainbow_window": build_rainbow_window(),
	"pearl_shell_sconce": build_sconce(),
	"pearl_shell_chandelier": build_chandelier(),
	"pearl_floor_medallion": build_floor_medallion(),
	"pearl_throne_canopy": build_throne_canopy(),
	"pearl_shell_throne": build_throne(),
	"pearl_shell_planter": build_planter(),
	"pearl_shell_bench": build_bench(),
	"pearl_cloud_settee": build_cloud_settee(),
	"pearl_cloud_pouf": build_cloud_pouf(),
	"pearl_shell_fountain": build_fountain(),
	"pearl_rainbow_gate": build_rainbow_gate(),
	"pearl_shell_banner_a": build_banner("pearl_shell_banner_a", False),
	"pearl_shell_banner_b": build_banner("pearl_shell_banner_b", True),
	"pearl_stair_rail": build_stair_rail(),
}


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result += family(child)
	return result


def bounds(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	points: list[Vector] = []
	for member in family(obj):
		if member.type in {"MESH", "CURVE"}:
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	return (
		Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points))),
		Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points))),
	)


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
			copy.select_set(True)
			bpy.context.view_layer.objects.active = copy
			bpy.ops.object.convert(target="MESH")
			copy = bpy.context.active_object
			copy.select_set(False)
		export_meshes.append(copy)
	bpy.ops.object.select_all(action="DESELECT")
	for mesh in export_meshes:
		mesh.select_set(True)
	bpy.context.view_layer.objects.active = export_meshes[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	bpy.ops.export_scene.gltf(
		filepath=str(ASSET_OUT / (name + ".glb")),
		export_format="GLB",
		export_yup=True,
		use_selection=True,
		export_apply=True,
		export_materials="EXPORT",
		export_animations=False,
	)
	bpy.data.objects.remove(merged, do_unlink=True)
	return triangles


for asset_name, asset in ASSETS.items():
	triangle_count = export_asset(asset_name, asset)
	lo, hi = bounds(asset)
	print("PEARL_CASTLE|%s|triangles=%d|bounds=%s..%s" % (
		asset_name, triangle_count,
		tuple(round(value, 2) for value in lo),
		tuple(round(value, 2) for value in hi),
	))
	if triangle_count > 10000:
		raise RuntimeError("%s exceeds the 10k triangle prop budget" % asset_name)
	for member in family(asset):
		member.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))


scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 780
scene.render.resolution_y = 660
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = True
scene.view_settings.look = "AgX - Medium High Contrast"
bpy.ops.object.camera_add(location=(12.0, -18.0, 10.0))
camera = bpy.context.active_object
camera.data.lens = 58
scene.camera = camera
for location, energy, size, color in (
	((8.0, -10.0, 16.0), 1150.0, 8.0, (0.85, 0.94, 1.0)),
	((-10.0, -4.0, 9.0), 780.0, 6.0, (0.72, 0.82, 1.0)),
	((4.0, 9.0, 12.0), 900.0, 6.0, (1.0, 0.76, 0.62)),
):
	bpy.ops.object.light_add(type="AREA", location=location)
	light = bpy.context.active_object
	light.data.energy = energy
	light.data.shape = "DISK"
	light.data.size = size
	light.data.color = color
if scene.world is None:
	scene.world = bpy.data.worlds.new("Pearl Castle QA World")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.055, 0.10, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.36

for asset_name, asset in ASSETS.items():
	for member in family(asset):
		member.hide_render = False
	lo, hi = bounds(asset)
	center = (lo + hi) * 0.5
	size = hi - lo
	distance = max(size.x, size.y, size.z) * 1.85
	if "medallion" in asset_name or "chandelier" in asset_name:
		camera.location = center + Vector((distance * 0.72, -distance * 1.12, distance * 0.95))
	else:
		camera.location = center + Vector((distance * 0.72, -distance * 1.30, distance * 0.52))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
	for member in family(asset):
		member.hide_render = True

print("PEARL_CASTLE|assets|%d" % len(ASSETS))
print("PEARL_CASTLE|blend|%s" % BLEND_OUT)
