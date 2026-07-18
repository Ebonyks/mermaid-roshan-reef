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
	cylinder("CloudPouf_InkFoot", (0.0, 0.0, 0.30), 1.82, 0.60, MATS["ink"], r, 18)
	cylinder("CloudPouf_GoldBand", (0.0, 0.0, 0.62), 1.68, 0.30, MATS["gold"], r, 18)
	for index, (x, y, sx) in enumerate(((-1.12, 0.02, 1.04), (-0.58, 0.48, 0.92),
		(0.58, 0.48, 0.92), (1.12, 0.02, 1.04), (0.0, -0.38, 1.12))):
		ellipsoid("CloudPouf_Lobe_%d" % index, (x, y, 0.92),
			(sx, 0.72, 0.52), MATS["pearl_light"] if index % 2 == 0 else MATS["pearl"], r)
	ellipsoid("CloudPouf_RoseCushion", (0.0, -0.08, 1.52), (1.48, 1.12, 0.38), MATS["rose"], r)
	torus("CloudPouf_CushionPiping", (0.0, -0.08, 1.48), 1.23, 0.08, MATS["gold"], r,
		(math.pi * 0.5, 0.0, 0.0), 20)
	shell_fan("CloudPouf_Shell", (0.0, -1.04, 0.98), 0.72, r,
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


def build_ocean_portal() -> bpy.types.Object:
	"""An opaque graphic-water curtain that gives the return gate a destination."""
	r = root("pearl_ocean_portal")
	outer = [(-3.62, 0.25), (-3.62, 6.95)]
	for index in range(13):
		a = math.pi - math.pi * float(index) / 12.0
		outer.append((math.cos(a) * 3.62, 6.95 + math.sin(a) * 3.62))
	outer.append((3.62, 0.25))
	inner = [(-3.25, 0.52), (-3.25, 6.80)]
	for index in range(13):
		a = math.pi - math.pi * float(index) / 12.0
		inner.append((math.cos(a) * 3.25, 6.80 + math.sin(a) * 3.25))
	inner.append((3.25, 0.52))
	panel_xz("OceanPortal_Ink", outer, 0.26, (0.0, 0.0, 0.0), MATS["ink"], r, 0.10)
	panel_xz("OceanPortal_Water", inner, 0.30, (0.0, -0.18, 0.0), MATS["water"], r, 0.08)
	for wave_index, (z, color, phase) in enumerate(((2.2, "aqua", 0.0),
		(3.35, "mint", 0.65), (4.55, "sky", 1.25), (5.75, "pearl_light", 0.35))):
		points = []
		for point_index in range(9):
			x = -3.0 + float(point_index) * 0.75
			points.append((x, -0.39, z + math.sin(float(point_index) * 0.9 + phase) * 0.24))
		tube("OceanPortal_Wave_%d" % wave_index, points, 0.12, MATS[color], r)
	for index, (x, z, scale) in enumerate(((-1.9, 7.1, 0.28), (1.7, 6.4, 0.38),
		(-0.8, 8.2, 0.22), (2.2, 8.8, 0.20))):
		ellipsoid("OceanPortal_Bubble_%d" % index, (x, -0.42, z),
			(scale, scale, scale), MATS["pearl_light"], r)
	shell_fan("OceanPortal_FloorShell", (0.0, -0.43, 1.12), 1.25, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_shell_window() -> bpy.types.Object:
	r = root("pearl_shell_window")
	outer = [(-3.05, 0.0), (-3.05, 4.15)]
	for index in range(11):
		a = math.pi - math.pi * float(index) / 10.0
		outer.append((math.cos(a) * 3.05, 4.15 + math.sin(a) * 3.05))
	outer.append((3.05, 0.0))
	panel_xz("ShellWindow_InkGlass", outer, 0.32, (0.0, 0.0, 0.0), MATS["ink"], r, 0.10)
	inner = [(-2.48, 0.52), (-2.48, 4.06)]
	for index in range(11):
		a = math.pi - math.pi * float(index) / 10.0
		inner.append((math.cos(a) * 2.48, 4.06 + math.sin(a) * 2.48))
	inner.append((2.48, 0.52))
	panel_xz("ShellWindow_AquaGlass", inner, 0.36, (0.0, -0.18, 0.0), MATS["sky"], r, 0.08)
	for x in (-2.82, 2.82):
		rounded_box("ShellWindow_Jamb", (x, -0.22, 2.10), (0.56, 0.58, 4.20), MATS["pearl"], r, 0.14)
	rounded_box("ShellWindow_Sill", (0.0, -0.22, 0.28), (6.10, 0.64, 0.56), MATS["gold"], r, 0.16)
	arc_tube("ShellWindow_Frame", (0.0, -0.22, 4.15), 2.82, 0.38,
		MATS["pearl_light"], r, steps=15)
	tube("ShellWindow_Mullion", [(0.0, -0.42, 0.55), (0.0, -0.42, 6.45)],
		0.10, MATS["gold"], r)
	shell_fan("ShellWindow_Crest", (0.0, -0.52, 6.92), 1.05, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_story_cushion() -> bpy.types.Object:
	r = root("pearl_story_cushion")
	cylinder("StoryCushion_InkBase", (0.0, 0.0, 0.28), 2.35, 0.56, MATS["ink"], r, 20)
	cylinder("StoryCushion_GoldBase", (0.0, 0.0, 0.58), 2.18, 0.30, MATS["gold"], r, 20)
	ellipsoid("StoryCushion_LavenderSeat", (0.0, -0.12, 1.02), (2.02, 1.78, 0.58), MATS["lavender"], r)
	for side in (-1.0, 1.0):
		ellipsoid("StoryCushion_PearlArm", (side * 1.72, 0.05, 1.50),
			(0.65, 1.22, 0.92), MATS["pearl"], r)
	shell_fan("StoryCushion_BackShell", (0.0, 1.35, 2.42), 1.72, r,
		(0.0, 0.0, math.pi), MATS["pearl_light"], MATS["lavender"])
	return r


def build_toy_block_stack() -> bpy.types.Object:
	r = root("pearl_toy_block_stack")
	blocks = [
		(-1.60, 0.10, 1.10, 2.15, "coral", -8.0),
		(0.62, 0.00, 0.95, 1.85, "aqua", 6.0),
		(1.92, 0.20, 0.72, 1.38, "yellow", -4.0),
		(-0.78, 0.10, 3.00, 1.65, "mint", 4.0),
		(0.95, 0.10, 2.70, 1.42, "rose", -7.0),
	]
	for index, (x, y, z, size, color, angle) in enumerate(blocks):
		rounded_box("ToyBlock_Ink_%d" % index, (x, y, z),
			(size + 0.18, size + 0.18, size + 0.18), MATS["ink"], r, 0.24,
			(0.0, 0.0, math.radians(angle)))
		rounded_box("ToyBlock_Color_%d" % index, (x, y - 0.08, z + 0.05),
			(size, size, size), MATS[color], r, 0.26,
			(0.0, 0.0, math.radians(angle)))
		ellipsoid("ToyBlock_Pearl_%d" % index, (x, y - size * 0.52, z + 0.05),
			(size * 0.16, size * 0.10, size * 0.16), MATS["pearl_light"], r)
	return r


def build_chest(name: str, secret: bool = False) -> bpy.types.Object:
	r = root(name)
	width = 7.2 if secret else 5.6
	depth = 4.5 if secret else 3.8
	body_height = 3.55 if secret else 2.85
	body_mat = MATS["plum"] if secret else MATS["aqua"]
	rounded_box("Chest_InkBase", (0.0, 0.0, 0.34), (width + 0.30, depth + 0.30, 0.68), MATS["ink"], r, 0.24)
	rounded_box("Chest_Body", (0.0, 0.0, 0.58 + body_height * 0.5),
		(width, depth, body_height), body_mat, r, 0.38)
	rounded_box("Chest_LidInk", (0.0, 0.0, body_height + 0.92),
		(width + 0.40, depth + 0.40, 1.20), MATS["ink"], r, 0.42)
	rounded_box("Chest_LidPearl", (0.0, -0.05, body_height + 1.02),
		(width + 0.12, depth + 0.15, 0.92), MATS["pearl"], r, 0.38)
	for x in (-width * 0.32, width * 0.32):
		rounded_box("Chest_GoldBand", (x, -depth * 0.515, 2.05),
			(0.32, 0.18, body_height + 2.0), MATS["gold"], r, 0.08)
	shell_fan("Chest_ShellLock", (0.0, -depth * 0.57, body_height * 0.72),
		1.10 if secret else 0.82, r, lobe_mat=MATS["pearl_light"], shadow_mat=MATS["gold"])
	if secret:
		for index, color in enumerate(("coral", "yellow", "mint", "aqua", "rose")):
			ellipsoid("Chest_RainbowPearl_%d" % index,
				((-2.0 + float(index)) * 0.72, -depth * 0.535, body_height + 1.05),
				(0.20, 0.13, 0.20), MATS[color], r)
	return r


def build_shell_hopscotch() -> bpy.types.Object:
	r = root("pearl_shell_hopscotch")
	pad_data = [
		(0.0, 0.0, "coral"), (-1.18, 2.35, "yellow"), (1.18, 2.35, "mint"),
		(0.0, 4.70, "aqua"), (-1.18, 7.05, "sky"), (1.18, 7.05, "rose"),
		(0.0, 9.40, "pearl_light"),
	]
	for index, (x, y, color) in enumerate(pad_data):
		cylinder("Hopscotch_Ink_%d" % index, (x, y, 0.10), 1.08, 0.20, MATS["ink"], r, 18)
		cylinder("Hopscotch_Pad_%d" % index, (x, y, 0.23), 0.92, 0.18, MATS[color], r, 18)
		for lobe_index, angle in enumerate((-0.58, -0.29, 0.0, 0.29, 0.58)):
			ellipsoid("Hopscotch_Lobe_%d_%d" % (index, lobe_index),
				(x + math.sin(angle) * 0.55, y - 0.05, 0.38 + math.cos(angle) * 0.13),
				(0.25, 0.42, 0.18), MATS["pearl_light"], r, (0.0, angle, 0.0))
	return r


def build_canopy_bed() -> bpy.types.Object:
	r = root("pearl_canopy_bed")
	rounded_box("Bed_InkPlinth", (0.0, 0.0, 0.46), (7.4, 12.2, 0.92), MATS["ink"], r, 0.30)
	rounded_box("Bed_PearlFrame", (0.0, 0.0, 1.08), (7.0, 11.8, 0.72), MATS["pearl"], r, 0.28)
	rounded_box("Bed_Mattress", (0.0, -0.15, 1.78), (6.55, 10.9, 0.82), MATS["pearl_light"], r, 0.34)
	rounded_box("Bed_Quilt", (0.0, -1.28, 2.25), (6.12, 7.65, 0.30), MATS["rose"], r, 0.18)
	for index, color in enumerate(("coral", "yellow", "mint", "aqua", "sky")):
		rounded_box("Bed_RainbowStripe_%d" % index,
			(-2.16 + float(index) * 1.08, -3.95, 2.43), (0.78, 1.55, 0.15), MATS[color], r, 0.08)
	for x in (-1.78, 1.78):
		ellipsoid("Bed_Pillow", (x, 4.05, 2.48), (1.55, 1.10, 0.40), MATS["lavender"], r)
	for x in (-3.38, 3.38):
		for y in (-5.55, 5.55):
			cylinder("Bed_Post", (x, y, 4.72), 0.28, 8.65, MATS["pearl"], r, 14)
			cylinder("Bed_PostGold", (x, y, 0.70), 0.46, 0.70, MATS["gold"], r, 14)
			ellipsoid("Bed_PostPearl", (x, y, 9.15), (0.42, 0.42, 0.48), MATS["gold"], r)
	arc_tube("Bed_HeadCanopy", (0.0, 5.55, 8.02), 3.38, 0.26, MATS["gold"], r, steps=15)
	arc_tube("Bed_FootCanopy", (0.0, -5.55, 8.02), 3.38, 0.26, MATS["gold"], r, steps=15)
	shell_fan("Bed_HeadShell", (0.0, 5.35, 5.25), 2.25, r,
		(0.0, 0.0, math.pi), MATS["pearl_light"], MATS["lavender"])
	return r


def build_bedside_table() -> bpy.types.Object:
	r = root("pearl_bedside_table")
	cylinder("Bedside_InkFoot", (0.0, 0.0, 0.28), 1.30, 0.56, MATS["ink"], r, 18)
	cone("Bedside_PearlBody", (0.0, 0.0, 1.52), 1.18, 0.92, 2.40, MATS["pearl"], r, 18)
	cylinder("Bedside_GoldTop", (0.0, 0.0, 2.82), 1.38, 0.34, MATS["gold"], r, 18)
	shell_fan("Bedside_DrawerShell", (0.0, -0.98, 1.48), 0.72, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	cylinder("Bedside_LampStem", (0.0, 0.0, 3.62), 0.13, 1.35, MATS["gold"], r, 10)
	cone("Bedside_LampShade", (0.0, 0.0, 4.45), 0.82, 0.38, 1.15, MATS["pearl_light"], r, 18)
	ellipsoid("Bedside_LampPearl", (0.0, 0.0, 4.30), (0.30, 0.30, 0.34), MATS["yellow"], r)
	return r


def build_wardrobe() -> bpy.types.Object:
	r = root("pearl_shell_wardrobe")
	rounded_box("Wardrobe_InkBody", (0.0, 0.0, 6.6), (7.1, 2.25, 13.2), MATS["ink"], r, 0.34)
	rounded_box("Wardrobe_PearlBody", (0.0, -0.08, 6.55), (6.65, 2.12, 12.75), MATS["pearl"], r, 0.32)
	rounded_box("Wardrobe_Mirror", (0.0, -1.14, 6.75), (4.35, 0.18, 8.15), MATS["sky"], r, 0.18)
	for x in (-2.42, 2.42):
		rounded_box("Wardrobe_GoldFrame", (x, -1.24, 6.75), (0.34, 0.22, 8.82), MATS["gold"], r, 0.09)
	rounded_box("Wardrobe_GoldSill", (0.0, -1.24, 2.26), (5.18, 0.22, 0.34), MATS["gold"], r, 0.09)
	shell_fan("Wardrobe_Crest", (0.0, -1.27, 11.72), 1.62, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	for index, color in enumerate(("coral", "yellow", "mint", "aqua", "rose")):
		ellipsoid("Wardrobe_Swatch_%d" % index, (-2.72 + float(index) * 1.36, -1.30, 1.18),
			(0.30, 0.18, 0.30), MATS[color], r)
	return r


def build_music_rail() -> bpy.types.Object:
	r = root("pearl_music_rail")
	for x in (-3.0, 3.0):
		rounded_box("MusicRail_Ink", (x, 0.0, 0.34), (0.82, 31.0, 0.68), MATS["ink"], r, 0.22)
		rounded_box("MusicRail_Gold", (x, 0.0, 0.72), (0.50, 30.4, 0.30), MATS["gold"], r, 0.14)
	for y in (-15.0, 15.0):
		rounded_box("MusicRail_End", (0.0, y, 0.54), (7.1, 0.78, 0.72), MATS["pearl"], r, 0.22)
		shell_fan("MusicRail_EndShell", (0.0, y - 0.42 * (1.0 if y > 0.0 else -1.0), 1.05), 1.10, r,
			(0.0, 0.0, 0.0 if y < 0.0 else math.pi), MATS["pearl_light"], MATS["lavender"])
	return r


def build_music_bar(index: int) -> bpy.types.Object:
	r = root("pearl_music_bar_%d" % index)
	colors = ("coral", "peach", "yellow", "mint", "aqua", "sky", "rose")
	width = 7.25 - float(index) * 0.22
	rounded_box("MusicBar_Ink", (0.0, 0.0, 0.18), (width + 0.28, 2.72, 0.72), MATS["ink"], r, 0.22)
	rounded_box("MusicBar_Key", (0.0, -0.04, 0.48), (width, 2.48, 0.70), MATS[colors[index]], r, 0.28)
	for x in (-width * 0.36, width * 0.36):
		ellipsoid("MusicBar_PearlPin", (x, -0.72, 0.92), (0.24, 0.24, 0.18), MATS["pearl_light"], r)
	ellipsoid("MusicBar_Resonator", (0.0, 0.42, -0.18), (1.25, 0.66, 0.42), MATS["gold"], r)
	return r


def build_storage_barrel() -> bpy.types.Object:
	r = root("pearl_storage_barrel")
	cylinder("Barrel_Ink", (0.0, 0.0, 1.70), 1.72, 3.40, MATS["ink"], r, 18)
	cone("Barrel_Plum", (0.0, 0.0, 1.70), 1.42, 1.58, 3.10, MATS["plum"], r, 18)
	for z in (0.34, 1.70, 3.06):
		torus("Barrel_GoldHoop", (0.0, 0.0, z), 1.52, 0.12, MATS["gold"], r, major_segments=20)
	for x in (-0.54, 0.0, 0.54):
		tube("Barrel_PearlStave", [(x, -1.52, 0.42), (x * 1.08, -1.58, 2.98)],
			0.07, MATS["pearl_shadow"], r)
	shell_fan("Barrel_ShellMark", (0.0, -1.58, 1.72), 0.72, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_storage_crate() -> bpy.types.Object:
	r = root("pearl_storage_crate")
	rounded_box("Crate_Ink", (0.0, 0.0, 1.55), (3.55, 3.35, 3.10), MATS["ink"], r, 0.28)
	rounded_box("Crate_Pearl", (0.0, -0.04, 1.58), (3.18, 3.02, 2.78), MATS["pearl_shadow"], r, 0.24)
	for x in (-1.42, 1.42):
		rounded_box("Crate_GoldEdge", (x, -1.57, 1.55), (0.28, 0.22, 2.95), MATS["gold"], r, 0.08)
	for angle in (-0.60, 0.60):
		rounded_box("Crate_Brace", (0.0, -1.60, 1.56), (0.28, 0.20, 3.58), MATS["plum"], r, 0.07,
			(angle, 0.0, 0.0))
	shell_fan("Crate_ShellMark", (0.0, -1.72, 1.52), 0.62, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_shell_lantern() -> bpy.types.Object:
	r = root("pearl_shell_lantern")
	ellipsoid("Lantern_InkPlaque", (0.0, 0.10, 0.0), (1.02, 0.24, 1.18), MATS["ink"], r)
	shell_fan("Lantern_Shell", (0.0, -0.20, 0.0), 1.08, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	tube("Lantern_GoldArm", [(0.0, -0.35, -0.20), (0.0, -0.85, -0.62),
		(0.0, -1.02, -1.12)], 0.10, MATS["gold"], r)
	rounded_box("Lantern_InkFrame", (0.0, -1.03, -1.72), (0.92, 0.74, 1.28), MATS["ink"], r, 0.20)
	ellipsoid("Lantern_PearlGlow", (0.0, -1.08, -1.72), (0.34, 0.28, 0.48), MATS["yellow"], r)
	return r


def build_pantry_shelf() -> bpy.types.Object:
	r = root("pearl_pantry_shelf")
	for x in (-5.15, 5.15):
		rounded_box("PantryShelf_Post", (x, 0.0, 4.0), (0.46, 1.55, 8.0), MATS["pearl"], r, 0.14)
	for z in (0.42, 3.15, 5.85, 8.15):
		rounded_box("PantryShelf_Board", (0.0, 0.0, z), (10.8, 1.82, 0.42), MATS["plum"], r, 0.14)
	for row, z in enumerate((1.22, 3.94, 6.66)):
		for index, color in enumerate(("coral", "yellow", "mint", "sky")):
			x = -3.72 + float(index) * 2.48
			cylinder("PantryJar_%d_%d" % (row, index), (x, -0.18, z), 0.50, 1.18,
				MATS[color], r, 14)
			cylinder("PantryJarLid_%d_%d" % (row, index), (x, -0.18, z + 0.68), 0.54, 0.20,
				MATS["gold"], r, 14)
	shell_fan("PantryShelf_Crest", (0.0, -0.92, 8.20), 1.25, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_craft_easel() -> bpy.types.Object:
	r = root("pearl_craft_easel")
	for x in (-2.55, 2.55):
		tube("CraftEasel_Leg", [(x * 0.72, 0.25, 0.0), (x, 0.0, 8.40)], 0.20, MATS["gold"], r)
	tube("CraftEasel_BackLeg", [(0.0, 1.75, 0.0), (0.0, 0.35, 7.70)], 0.22, MATS["plum"], r)
	rounded_box("CraftEasel_InkFrame", (0.0, -0.22, 5.15), (6.25, 0.50, 5.90), MATS["ink"], r, 0.22)
	rounded_box("CraftEasel_Canvas", (0.0, -0.52, 5.15), (5.65, 0.22, 5.30), MATS["pearl_light"], r, 0.16)
	rounded_box("CraftEasel_Tray", (0.0, -0.52, 2.20), (6.55, 1.10, 0.42), MATS["gold"], r, 0.15)
	shell_fan("CraftEasel_Crest", (0.0, -0.66, 8.25), 1.05, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_paint_rack() -> bpy.types.Object:
	r = root("pearl_paint_rack")
	rounded_box("PaintRack_InkBase", (0.0, 0.0, 0.28), (12.4, 2.35, 0.56), MATS["ink"], r, 0.20)
	rounded_box("PaintRack_PearlShelf", (0.0, 0.0, 0.62), (12.0, 2.10, 0.42), MATS["pearl"], r, 0.18)
	for index, color in enumerate(("coral", "peach", "yellow", "mint", "aqua", "sky", "rose")):
		x = -4.92 + float(index) * 1.64
		cone("PaintPot_%d" % index, (x, 0.0, 1.58), 0.66, 0.54, 1.55, MATS["pearl_shadow"], r, 14)
		cylinder("PaintColor_%d" % index, (x, 0.0, 2.37), 0.50, 0.16, MATS[color], r, 14)
	return r


def build_craft_table() -> bpy.types.Object:
	r = root("pearl_craft_table")
	for x in (-2.65, 2.65):
		for y in (-1.65, 1.65):
			cylinder("CraftTable_Leg", (x, y, 1.42), 0.22, 2.84, MATS["gold"], r, 12)
	rounded_box("CraftTable_InkTop", (0.0, 0.0, 3.02), (6.65, 4.55, 0.62), MATS["ink"], r, 0.26)
	rounded_box("CraftTable_PearlTop", (0.0, -0.04, 3.40), (6.30, 4.20, 0.42), MATS["pearl"], r, 0.22)
	rounded_box("CraftTable_Paper", (-0.85, -0.20, 3.68), (3.10, 2.85, 0.10), MATS["pearl_light"], r, 0.05,
		(0.0, 0.0, -0.08))
	for index, color in enumerate(("coral", "yellow", "aqua", "rose")):
		rounded_box("CraftTable_Crayon_%d" % index,
			(1.25 + float(index) * 0.40, 0.55 - float(index % 2) * 0.50, 3.78),
			(0.22, 1.20, 0.20), MATS[color], r, 0.06, (0.0, 0.0, -0.18 + float(index) * 0.10))
	shell_fan("CraftTable_Shell", (0.0, -2.22, 2.28), 0.82, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_bath_duck() -> bpy.types.Object:
	r = root("pearl_bath_duck")
	ellipsoid("BathDuck_Body", (-0.18, 0.0, 0.62), (1.08, 0.72, 0.70), MATS["yellow"], r)
	ellipsoid("BathDuck_Head", (0.66, -0.02, 1.18), (0.56, 0.52, 0.58), MATS["yellow"], r)
	ellipsoid("BathDuck_UpperBill", (1.22, -0.02, 1.16), (0.48, 0.34, 0.15), MATS["peach"], r)
	ellipsoid("BathDuck_LowerBill", (1.18, -0.02, 1.03), (0.40, 0.30, 0.10), MATS["coral"], r)
	for side in (-1.0, 1.0):
		ellipsoid("BathDuck_Eye", (0.86, side * 0.42, 1.36), (0.10, 0.07, 0.12), MATS["ink"], r)
	ellipsoid("BathDuck_Wing", (-0.28, -0.60, 0.74), (0.62, 0.16, 0.38), MATS["pearl_light"], r)
	return r


def build_towel_stack() -> bpy.types.Object:
	r = root("pearl_towel_stack")
	rounded_box("TowelStack_InkShelf", (0.0, 0.0, 0.28), (3.55, 2.75, 0.56), MATS["ink"], r, 0.22)
	for index, color in enumerate(("sky", "rose", "pearl_light")):
		rounded_box("TowelStack_Towel_%d" % index, (0.0, 0.0, 0.72 + float(index) * 0.68),
			(3.10 - float(index) * 0.18, 2.35, 0.56), MATS[color], r, 0.20)
	shell_fan("TowelStack_Shell", (0.0, -1.34, 1.40), 0.62, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_tiara() -> bpy.types.Object:
	r = root("pearl_keepsake_tiara")
	arc_tube("Tiara_GoldBand", (0.0, 0.0, 0.0), 1.55, 0.14, MATS["gold"], r,
		0.18, math.pi - 0.18, 15)
	for index, x in enumerate((-1.02, -0.52, 0.0, 0.52, 1.02)):
		height = 1.15 if index == 2 else 0.78 if index in (1, 3) else 0.52
		cone("Tiara_Point_%d" % index, (x, 0.0, 0.55 + height * 0.5), 0.28, 0.06,
			height, MATS["gold"], r, 10)
		ellipsoid("Tiara_Pearl_%d" % index, (x, -0.10, 0.62 + height),
			(0.18, 0.18, 0.20), MATS[("coral", "yellow", "aqua", "mint", "rose")[index]], r)
	return r


def build_cradle() -> bpy.types.Object:
	r = root("pearl_keepsake_cradle")
	for y in (-1.70, 1.70):
		arc_tube("Cradle_Rocker", (0.0, y, 0.12), 1.85, 0.16, MATS["gold"], r,
			0.20, math.pi - 0.20, 13)
	rounded_box("Cradle_InkBowl", (0.0, 0.0, 1.15), (4.15, 3.15, 1.55), MATS["ink"], r, 0.40)
	rounded_box("Cradle_PearlBowl", (0.0, -0.04, 1.28), (3.80, 2.82, 1.28), MATS["pearl"], r, 0.38)
	ellipsoid("Cradle_RoseBlanket", (0.0, -0.18, 1.82), (1.55, 1.12, 0.42), MATS["rose"], r)
	for y in (-1.48, 1.48):
		shell_fan("Cradle_EndShell", (0.0, y, 1.62), 0.82, r,
			(0.0, 0.0, 0.0 if y < 0.0 else math.pi), MATS["pearl_light"], MATS["lavender"])
	return r


def build_pet_basket() -> bpy.types.Object:
	r = root("pearl_pet_basket")
	torus("PetBasket_InkRim", (0.0, 0.0, 1.00), 2.25, 0.30, MATS["ink"], r, major_segments=24)
	cone("PetBasket_PearlBowl", (0.0, 0.0, 0.62), 1.82, 2.25, 1.15, MATS["pearl_shadow"], r, 22)
	ellipsoid("PetBasket_RoseCushion", (0.0, 0.0, 1.05), (1.90, 1.90, 0.42), MATS["rose"], r)
	for index in range(8):
		a = math.tau * float(index) / 8.0
		tube("PetBasket_GoldWeave_%d" % index,
			[(math.cos(a) * 1.72, math.sin(a) * 1.72, 0.14),
			(math.cos(a) * 2.05, math.sin(a) * 2.05, 1.05)], 0.08, MATS["gold"], r)
	shell_fan("PetBasket_Shell", (0.0, -2.04, 0.76), 0.72, r,
		lobe_mat=MATS["pearl_light"], shadow_mat=MATS["lavender"])
	return r


def build_music_box() -> bpy.types.Object:
	r = root("pearl_keepsake_music_box")
	rounded_box("MusicBox_Ink", (0.0, 0.0, 0.72), (3.2, 2.45, 1.44), MATS["ink"], r, 0.28)
	rounded_box("MusicBox_Pearl", (0.0, -0.05, 0.82), (2.88, 2.12, 1.18), MATS["pearl"], r, 0.26)
	shell_fan("MusicBox_OpenShell", (0.0, 0.98, 2.10), 1.10, r,
		(0.0, 0.0, math.pi), MATS["pearl_light"], MATS["lavender"])
	for index, color in enumerate(("coral", "yellow", "mint", "aqua", "rose")):
		cylinder("MusicBox_Chime_%d" % index,
			(-1.02 + float(index) * 0.51, -0.56, 1.72 + float(index % 2) * 0.22),
			0.09, 1.25, MATS[color], r, 8)
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
	"pearl_ocean_portal": build_ocean_portal(),
	"pearl_shell_window": build_shell_window(),
	"pearl_story_cushion": build_story_cushion(),
	"pearl_toy_block_stack": build_toy_block_stack(),
	"pearl_toy_chest": build_chest("pearl_toy_chest"),
	"pearl_secret_chest": build_chest("pearl_secret_chest", True),
	"pearl_shell_hopscotch": build_shell_hopscotch(),
	"pearl_canopy_bed": build_canopy_bed(),
	"pearl_bedside_table": build_bedside_table(),
	"pearl_shell_wardrobe": build_wardrobe(),
	"pearl_music_rail": build_music_rail(),
	"pearl_music_bar_0": build_music_bar(0),
	"pearl_music_bar_1": build_music_bar(1),
	"pearl_music_bar_2": build_music_bar(2),
	"pearl_music_bar_3": build_music_bar(3),
	"pearl_music_bar_4": build_music_bar(4),
	"pearl_music_bar_5": build_music_bar(5),
	"pearl_music_bar_6": build_music_bar(6),
	"pearl_storage_barrel": build_storage_barrel(),
	"pearl_storage_crate": build_storage_crate(),
	"pearl_shell_lantern": build_shell_lantern(),
	"pearl_pantry_shelf": build_pantry_shelf(),
	"pearl_craft_easel": build_craft_easel(),
	"pearl_paint_rack": build_paint_rack(),
	"pearl_craft_table": build_craft_table(),
	"pearl_bath_duck": build_bath_duck(),
	"pearl_towel_stack": build_towel_stack(),
	"pearl_keepsake_tiara": build_tiara(),
	"pearl_keepsake_cradle": build_cradle(),
	"pearl_pet_basket": build_pet_basket(),
	"pearl_keepsake_music_box": build_music_box(),
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
