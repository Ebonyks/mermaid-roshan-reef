#!/usr/bin/env python3
"""Build the image-approved Royal Bathroom vanity as a detailed static GLB.

The model is authored from the generated concept and turnaround in
assets_src/blender/references.  Every visible finish is an embedded bespoke
material or a small geometric accent: no kitchen/castle texture is reused and
no Blender-only procedural shader is required by the exported asset.

Usage:
  blender --background --python tools/build_bathroom_sink_v2.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_OUT = ROOT / "assets" / "castle" / "bathroom_sink.glb"
SOURCE_OUT = ROOT / "assets_src" / "blender" / "bathroom_sink_v2.blend"
QA_DIR = ROOT / "assets_src" / "blender" / "qa_bathroom_props"
QA_OUT = QA_DIR / "bathroom_sink.png"

QA_DIR.mkdir(parents=True, exist_ok=True)
RUNTIME_OUT.parent.mkdir(parents=True, exist_ok=True)
SOURCE_OUT.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


def _set_socket(bsdf: bpy.types.Node, name: str, value: object) -> None:
	if name in bsdf.inputs:
		bsdf.inputs[name].default_value = value


def material(
	name: str,
	color: tuple[float, float, float, float],
	*,
	metallic: float = 0.0,
	roughness: float = 0.48,
	coat: float = 0.12,
) -> bpy.types.Material:
	"""Create a glTF-safe Principled material with no procedural dependency."""
	mat = bpy.data.materials.new("MR_Sink_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	mat.use_backface_culling = False
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	_set_socket(bsdf, "Base Color", color)
	_set_socket(bsdf, "Metallic", metallic)
	_set_socket(bsdf, "Roughness", roughness)
	_set_socket(bsdf, "Coat Weight", coat)
	_set_socket(bsdf, "Coat Roughness", 0.28)
	return mat


MATS = {
	"wood": material("WoodHoney", (0.72, 0.34, 0.105, 1.0), roughness=0.52, coat=0.18),
	"wood_light": material("WoodAmberHighlight", (0.82, 0.43, 0.13, 1.0), roughness=0.45, coat=0.22),
	"wood_dark": material("WoodCaramelShadow", (0.48, 0.205, 0.065, 1.0), roughness=0.58),
	"wood_inset": material("WoodInsetPanel", (0.80, 0.405, 0.135, 1.0), roughness=0.50, coat=0.18),
	"cream": material("TerrazzoCream", (0.96, 0.855, 0.69, 1.0), roughness=0.56, coat=0.16),
	"chip_peach": material("TerrazzoChipPeach", (0.95, 0.63, 0.47, 1.0), roughness=0.63),
	"chip_lav": material("TerrazzoChipLavender", (0.69, 0.54, 0.83, 1.0), roughness=0.63),
	"chip_aqua": material("TerrazzoChipAqua", (0.50, 0.78, 0.76, 1.0), roughness=0.63),
	"basin": material("BasinAquaCeramic", (0.31, 0.72, 0.72, 1.0), roughness=0.34, coat=0.35),
	"basin_light": material("BasinWaterGlow", (0.53, 0.88, 0.87, 1.0), roughness=0.27, coat=0.38),
	"gold": material("WarmGold", (0.96, 0.58, 0.105, 1.0), metallic=0.55, roughness=0.24, coat=0.30),
	"gold_light": material("GoldHighlight", (1.0, 0.78, 0.25, 1.0), metallic=0.38, roughness=0.22, coat=0.32),
	"lavender": material("ShellLavender", (0.68, 0.46, 0.82, 1.0), roughness=0.38, coat=0.26),
	"lavender_light": material("ShellRibHighlight", (0.87, 0.70, 0.95, 1.0), roughness=0.32, coat=0.28),
	"mirror": material("MirrorAqua", (0.30, 0.77, 0.79, 1.0), metallic=0.05, roughness=0.20, coat=0.42),
	"mirror_highlight": material("MirrorPearlHighlight", (0.74, 0.98, 0.96, 1.0), roughness=0.20, coat=0.42),
	"drain_dark": material("DrainRecess", (0.20, 0.15, 0.16, 1.0), metallic=0.20, roughness=0.38),
	"nozzle": material("PearlAerator", (0.82, 0.94, 0.92, 1.0), metallic=0.05, roughness=0.25, coat=0.30),
}

# The bowl is topologically open and its normals face into the basin.  Cull its
# exterior backfaces so the aqua shell cannot peek through the cabinet/counter
# join at a grazing angle; the recessed interior and top-facing water remain.
MATS["basin"].use_backface_culling = True
MATS["basin_light"].use_backface_culling = True


root = bpy.data.objects.new("BathroomSink", None)
bpy.context.collection.objects.link(root)


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.data.materials.append(mat)
	return obj


def activate(obj: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	activate(obj)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def smooth_angle(obj: bpy.types.Object) -> bpy.types.Object:
	if obj.type != "MESH":
		return obj
	activate(obj)
	try:
		bpy.ops.object.shade_smooth_by_angle()
	except (AttributeError, RuntimeError):
		for polygon in obj.data.polygons:
			polygon.use_smooth = True
	obj.select_set(False)
	return obj


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
	modifier = obj.modifiers.new("soft_storybook_edges", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	modifier.harden_normals = True
	modifier.use_clamp_overlap = True
	apply_modifier(obj, modifier)
	return smooth_angle(obj)


def rounded_box(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	radius: float = 0.10,
	segments: int = 2,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = root
	assign(obj, mat)
	bevel(obj, min(radius, min(size) * 0.22), segments)
	collection.append(obj)
	return obj


def cylinder(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	vertices: int = 24,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	bevel_width: float = 0.02,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(
		vertices=vertices,
		radius=radius,
		depth=depth,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = root
	assign(obj, mat)
	if bevel_width > 0.0:
		bevel(obj, min(bevel_width, radius * 0.20, depth * 0.20), 1)
	else:
		smooth_angle(obj)
	collection.append(obj)
	return obj


def uv_sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	segments: int = 16,
	rings: int = 8,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(
		segments=segments,
		ring_count=rings,
		radius=1.0,
		location=location,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = root
	assign(obj, mat)
	smooth_angle(obj)
	collection.append(obj)
	return obj


def mesh_object(
	name: str,
	vertices: list[tuple[float, float, float]],
	faces: list[tuple[int, ...]],
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	smooth: bool = True,
) -> bpy.types.Object:
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(vertices, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.parent = root
	assign(obj, mat)
	if smooth:
		smooth_angle(obj)
	collection.append(obj)
	return obj


def curve_tube(
	name: str,
	points: list[tuple[float, float, float]],
	radius: float,
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	bevel_resolution: int = 2,
	path_resolution: int = 3,
	cyclic: bool = False,
	polyline: bool = False,
) -> bpy.types.Object:
	curve_data = bpy.data.curves.new(name + "_curve", "CURVE")
	curve_data.dimensions = "3D"
	curve_data.resolution_u = path_resolution
	curve_data.bevel_depth = radius
	curve_data.bevel_resolution = bevel_resolution
	curve_data.resolution_v = 0
	curve_data.use_fill_caps = not cyclic
	if polyline:
		spline = curve_data.splines.new("POLY")
		spline.points.add(len(points) - 1)
		for point, position in zip(spline.points, points):
			point.co = (*position, 1.0)
		spline.use_cyclic_u = cyclic
	else:
		spline = curve_data.splines.new("BEZIER")
		spline.bezier_points.add(len(points) - 1)
		for point, position in zip(spline.bezier_points, points):
			point.co = position
			point.handle_left_type = "AUTO"
			point.handle_right_type = "AUTO"
		spline.use_cyclic_u = cyclic
	obj = bpy.data.objects.new(name, curve_data)
	bpy.context.collection.objects.link(obj)
	obj.parent = root
	curve_data.materials.append(mat)
	activate(obj)
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	obj.name = name
	smooth_angle(obj)
	collection.append(obj)
	return obj


def rounded_rect_points(half_w: float, half_h: float, radius: float, corner_steps: int = 4) -> list[tuple[float, float]]:
	points: list[tuple[float, float]] = []
	centers_angles = (
		((half_w - radius, -half_h + radius), -math.pi * 0.5, 0.0),
		((half_w - radius, half_h - radius), 0.0, math.pi * 0.5),
		((-half_w + radius, half_h - radius), math.pi * 0.5, math.pi),
		((-half_w + radius, -half_h + radius), math.pi, math.pi * 1.5),
	)
	for (cx, cy), start, end in centers_angles:
		for index in range(corner_steps + 1):
			t = float(index) / float(corner_steps)
			a = start + (end - start) * t
			points.append((cx + math.cos(a) * radius, cy + math.sin(a) * radius))
	return points


def rounded_rect_moulding(
	name: str,
	center: tuple[float, float, float],
	half_w: float,
	half_h: float,
	radius: float,
	tube_radius: float,
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	axis: str = "XZ",
) -> bpy.types.Object:
	points_2d = rounded_rect_points(half_w, half_h, radius, 3)
	if axis == "XZ":
		points = [(center[0] + u, center[1], center[2] + v) for u, v in points_2d]
	else:
		points = [(center[0], center[1] + u, center[2] + v) for u, v in points_2d]
	return curve_tube(
		name,
		points,
		tube_radius,
		mat,
		collection,
		bevel_resolution=0,
		path_resolution=1,
		cyclic=True,
		polyline=True,
	)


def countertop_ring(name: str, collection: list[bpy.types.Object]) -> bpy.types.Object:
	segments = 48
	outer_profiles = (
		(2.11, 1.14, 3.11),
		(2.17, 1.20, 3.17),
		(2.17, 1.20, 3.49),
		(2.12, 1.15, 3.56),
	)
	inner_profiles = (
		(1.36, 0.67, 3.11),
		(1.43, 0.73, 3.18),
		(1.43, 0.73, 3.49),
		(1.37, 0.68, 3.56),
	)
	vertices: list[tuple[float, float, float]] = []
	for rx, ry, z in outer_profiles:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			c = math.cos(a)
			s = math.sin(a)
			x = math.copysign(abs(c) ** 0.54, c) * rx
			y = math.copysign(abs(s) ** 0.54, s) * ry
			scallop = 1.0 + 0.032 * math.cos(a * 10.0)
			vertices.append((x * scallop, y * scallop - 0.02, z))
	outer_count = len(outer_profiles)
	for rx, ry, z in inner_profiles:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			vertices.append((math.cos(a) * rx, math.sin(a) * ry - 0.16, z))
	faces: list[tuple[int, ...]] = []
	for ring_index in range(outer_count - 1):
		base = ring_index * segments
		next_base = (ring_index + 1) * segments
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((base + index, base + next_index, next_base + next_index, next_base + index))
	inner_offset = outer_count * segments
	for ring_index in range(len(inner_profiles) - 1):
		base = inner_offset + ring_index * segments
		next_base = inner_offset + (ring_index + 1) * segments
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((base + next_index, base + index, next_base + index, next_base + next_index))
	outer_bottom = 0
	outer_top = (outer_count - 1) * segments
	inner_bottom = inner_offset
	inner_top = inner_offset + (len(inner_profiles) - 1) * segments
	for index in range(segments):
		next_index = (index + 1) % segments
		faces.append((outer_top + index, outer_top + next_index, inner_top + next_index, inner_top + index))
		faces.append((outer_bottom + next_index, outer_bottom + index, inner_bottom + index, inner_bottom + next_index))
	return mesh_object(name, vertices, faces, MATS["cream"], collection)


def basin_bowl(name: str, collection: list[bpy.types.Object]) -> bpy.types.Object:
	segments = 40
	profiles = (
		(1.39, 0.70, 3.52),
		(1.34, 0.66, 3.39),
		(1.22, 0.59, 3.15),
		(0.98, 0.47, 2.91),
		(0.62, 0.29, 2.73),
		(0.34, 0.16, 2.66),
	)
	vertices: list[tuple[float, float, float]] = []
	for rx, ry, z in profiles:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			vertices.append((math.cos(a) * rx, math.sin(a) * ry - 0.16, z))
	faces: list[tuple[int, ...]] = []
	for ring_index in range(len(profiles) - 1):
		base = ring_index * segments
		next_base = (ring_index + 1) * segments
		for index in range(segments):
			next_index = (index + 1) % segments
			# Reverse the usual vessel exterior winding: this surface is the
			# visible inside of the recessed bowl and deliberately culls outside.
			faces.append((base + index, base + next_index, next_base + next_index, next_base + index))
	center_index = len(vertices)
	vertices.append((0.0, -0.16, 2.66))
	last_ring = (len(profiles) - 1) * segments
	for index in range(segments):
		next_index = (index + 1) % segments
		faces.append((last_ring + index, last_ring + next_index, center_index))
	return mesh_object(name, vertices, faces, MATS["basin"], collection)


def flat_ellipse(
	name: str,
	center: tuple[float, float, float],
	radii: tuple[float, float],
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	segments: int = 40,
) -> bpy.types.Object:
	vertices = [center]
	for index in range(segments):
		a = float(index) * math.tau / float(segments)
		vertices.append((center[0] + math.cos(a) * radii[0], center[1] + math.sin(a) * radii[1], center[2]))
	faces = [(0, index + 1, ((index + 1) % segments) + 1) for index in range(segments)]
	return mesh_object(name, vertices, faces, mat, collection, smooth=False)


def terrazzo_chip(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	seed: int,
) -> bpy.types.Object:
	rng = random.Random(seed)
	segments = 6
	vertices = [location]
	for index in range(segments):
		a = float(index) * math.tau / float(segments)
		r = radius * rng.uniform(0.72, 1.18)
		vertices.append((location[0] + math.cos(a) * r, location[1] + math.sin(a) * r * 0.72, location[2]))
	faces = [(0, index + 1, ((index + 1) % segments) + 1) for index in range(segments)]
	return mesh_object(name, vertices, faces, mat, collection, smooth=False)


def arch_outline(radius: float, bottom: float, center_z: float, arc_steps: int = 24) -> list[tuple[float, float]]:
	points: list[tuple[float, float]] = [(-radius, bottom), (radius, bottom), (radius, center_z)]
	for index in range(1, arc_steps + 1):
		a = float(index) * math.pi / float(arc_steps)
		points.append((math.cos(a) * radius, center_z + math.sin(a) * radius))
	return points


def arch_ring(
	name: str,
	outer: tuple[float, float, float],
	inner: tuple[float, float, float],
	y_center: float,
	depth: float,
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
	*,
	bevel_width: float = 0.035,
) -> bpy.types.Object:
	outer_points = arch_outline(*outer)
	inner_points = arch_outline(*inner)
	if len(outer_points) != len(inner_points):
		raise ValueError("Arch loops must match")
	n = len(outer_points)
	front_y = y_center - depth * 0.5
	back_y = y_center + depth * 0.5
	vertices: list[tuple[float, float, float]] = []
	for y in (front_y, back_y):
		for x, z in outer_points:
			vertices.append((x, y, z))
		for x, z in inner_points:
			vertices.append((x, y, z))
	faces: list[tuple[int, ...]] = []
	of = 0
	inf = n
	ob = n * 2
	inb = n * 3
	for index in range(n):
		next_index = (index + 1) % n
		faces.extend((
			(of + index, inf + index, inf + next_index, of + next_index),
			(ob + next_index, inb + next_index, inb + index, ob + index),
			(of + next_index, ob + next_index, ob + index, of + index),
			(inf + index, inb + index, inb + next_index, inf + next_index),
		))
	obj = mesh_object(name, vertices, faces, mat, collection)
	if bevel_width > 0.0:
		bevel(obj, bevel_width, 1)
	return obj


def arch_solid(
	name: str,
	profile: tuple[float, float, float],
	y: float,
	mat: bpy.types.Material,
	collection: list[bpy.types.Object],
) -> bpy.types.Object:
	outline = arch_outline(*profile)
	center_x = 0.0
	center_z = (profile[1] + profile[2]) * 0.5
	vertices: list[tuple[float, float, float]] = [(center_x, y, center_z)]
	vertices.extend((x, y, z) for x, z in outline)
	faces: list[tuple[int, ...]] = []
	for index in range(len(outline)):
		next_index = (index + 1) % len(outline)
		faces.append((0, index + 1, next_index + 1))
	return mesh_object(name, vertices, faces, mat, collection, smooth=False)


def shell_fan(
	name: str,
	center: tuple[float, float, float],
	scale: tuple[float, float, float],
	body_mat: bpy.types.Material,
	rib_mat: bpy.types.Material,
	body_collection: list[bpy.types.Object],
	rib_collection: list[bpy.types.Object],
	*,
	ribs: int = 7,
) -> None:
	"""Create an extruded scallop shell plus seven genuinely separate ribs."""
	arc_steps = 28
	outline_2d: list[tuple[float, float]] = [(-0.55, -0.42), (0.55, -0.42)]
	for index in range(arc_steps + 1):
		a = float(index) * math.pi / float(arc_steps)
		radial = 0.92 + 0.065 * math.cos(float(ribs) * a)
		outline_2d.append((math.cos(a) * 0.58 * radial, -0.22 + math.sin(a) * 0.92 * radial))
	front_y = center[1] - scale[1] * 0.5
	back_y = center[1] + scale[1] * 0.5
	vertices: list[tuple[float, float, float]] = []
	for y in (front_y, back_y):
		for x, z in outline_2d:
			vertices.append((center[0] + x * scale[0], y, center[2] + z * scale[2]))
	n = len(outline_2d)
	faces: list[tuple[int, ...]] = []
	front_center = len(vertices)
	vertices.append((center[0], front_y, center[2] - 0.02 * scale[2]))
	back_center = len(vertices)
	vertices.append((center[0], back_y, center[2] - 0.02 * scale[2]))
	for index in range(n):
		next_index = (index + 1) % n
		faces.append((front_center, index, next_index))
		faces.append((back_center, n + next_index, n + index))
		faces.append((index, n + index, n + next_index, next_index))
	mesh_object(name + "_Shell", vertices, faces, body_mat, body_collection)
	base = (center[0], front_y - 0.012, center[2] - 0.34 * scale[2])
	for rib_index in range(ribs):
		a = math.radians(24.0 + (132.0 * float(rib_index) / float(ribs - 1)))
		end = (
			center[0] + math.cos(a) * scale[0] * 0.50,
			front_y - 0.025,
			center[2] - scale[2] * 0.18 + math.sin(a) * scale[2] * 0.78,
		)
		mid = (
			base[0] * 0.44 + end[0] * 0.56,
			front_y - 0.045,
			base[2] * 0.44 + end[2] * 0.56 + scale[2] * 0.035,
		)
		curve_tube(
			f"{name}_Rib{rib_index + 1}",
			[base, mid, end],
			max(0.012, scale[0] * 0.032),
			rib_mat,
			rib_collection,
			bevel_resolution=0,
			path_resolution=2,
		)


def join_group(name: str, objects: list[bpy.types.Object], mat: bpy.types.Material) -> bpy.types.Object:
	if not objects:
		raise ValueError(f"No objects for {name}")
	if len(objects) == 1:
		joined = objects[0]
		joined.name = name
		joined.parent = root
		joined.data.materials.clear()
		joined.data.materials.append(mat)
		for polygon in joined.data.polygons:
			polygon.material_index = 0
		return joined
	bpy.ops.object.select_all(action="DESELECT")
	for obj in objects:
		obj.hide_set(False)
		obj.select_set(True)
	bpy.context.view_layer.objects.active = objects[0]
	bpy.ops.object.join()
	joined = bpy.context.active_object
	joined.name = name
	joined.parent = root
	joined.data.materials.clear()
	joined.data.materials.append(mat)
	for polygon in joined.data.polygons:
		polygon.material_index = 0
	joined.select_set(False)
	return joined


# Components are grouped by both role prefix and bespoke exported material.
body_wood: list[bpy.types.Object] = []
body_light: list[bpy.types.Object] = []
body_dark: list[bpy.types.Object] = []
body_inset: list[bpy.types.Object] = []
top_cream: list[bpy.types.Object] = []
chips_peach: list[bpy.types.Object] = []
chips_lav: list[bpy.types.Object] = []
chips_aqua: list[bpy.types.Object] = []
basin_aqua: list[bpy.types.Object] = []
basin_light: list[bpy.types.Object] = []
metal_gold: list[bpy.types.Object] = []
metal_gold_light: list[bpy.types.Object] = []
metal_lav: list[bpy.types.Object] = []
metal_lav_light: list[bpy.types.Object] = []
metal_dark: list[bpy.types.Object] = []
metal_nozzle: list[bpy.types.Object] = []
mirror_lav: list[bpy.types.Object] = []
mirror_lav_light: list[bpy.types.Object] = []
mirror_gold: list[bpy.types.Object] = []
mirror_glass: list[bpy.types.Object] = []
mirror_highlight: list[bpy.types.Object] = []


# Rounded cabinet shell, open beneath the bowl so the recess has real volume.
rounded_box("carcass_back", (0.0, 0.93, 1.79), (3.72, 0.18, 2.66), MATS["wood"], body_wood, radius=0.08, segments=2)
rounded_box("carcass_bottom", (0.0, 0.0, 0.58), (3.72, 1.88, 0.20), MATS["wood_dark"], body_dark, radius=0.07, segments=2)
for x in (-1.87, 1.87):
	rounded_box(f"carcass_side_{x}", (x, 0.0, 1.79), (0.22, 1.92, 2.66), MATS["wood"], body_wood, radius=0.07, segments=2)
	rounded_box(f"front_corner_post_{x}", (x, -0.97, 1.79), (0.28, 0.25, 2.67), MATS["wood_light"], body_light, radius=0.11, segments=3)
rounded_box("front_lower_rail", (0.0, -0.98, 0.70), (3.66, 0.22, 0.30), MATS["wood_dark"], body_dark, radius=0.08, segments=2)
rounded_box("front_upper_rail", (0.0, -0.98, 2.93), (3.66, 0.22, 0.40), MATS["wood_light"], body_light, radius=0.09, segments=2)
rounded_box("center_stile", (0.0, -1.00, 1.73), (0.12, 0.20, 2.15), MATS["wood_dark"], body_dark, radius=0.045, segments=2)

# Crowned plinth and four bun feet keep the toy-furniture silhouette grounded.
rounded_box("base_shadow", (0.0, 0.0, 0.29), (4.20, 2.18, 0.34), MATS["wood_dark"], body_dark, radius=0.15, segments=3)
rounded_box("base_plinth", (0.0, -0.01, 0.40), (4.28, 2.26, 0.35), MATS["wood"], body_wood, radius=0.15, segments=3)
rounded_box("base_gold_moulding", (0.0, -0.02, 0.56), (4.08, 2.12, 0.12), MATS["wood_light"], body_light, radius=0.055, segments=2)
for x in (-1.70, 1.70):
	for y in (-0.85, 0.85):
		uv_sphere(f"bun_foot_{x}_{y}", (x, y, 0.22), (0.30, 0.30, 0.22), MATS["wood"], body_wood, segments=12, rings=6)

# Layered, genuinely inset front doors and side panels.
for index, x in enumerate((-0.91, 0.91)):
	rounded_box(f"door_slab_{index}", (x, -1.105, 1.72), (1.58, 0.16, 1.92), MATS["wood"], body_wood, radius=0.14, segments=2)
	rounded_box(f"door_inset_{index}", (x, -1.205, 1.72), (1.28, 0.055, 1.58), MATS["wood_inset"], body_inset, radius=0.17, segments=2)
	rounded_rect_moulding(
		f"door_moulding_{index}", (x, -1.246, 1.72), 0.68, 0.83, 0.16, 0.040,
		MATS["wood_light"], body_light,
	)
	pull_x = -0.35 if index == 0 else 0.35
	cylinder(f"door_pull_base_{index}", (pull_x, -1.29, 1.58), 0.15, 0.11, MATS["gold"], metal_gold,
		vertices=24, rotation=(math.pi * 0.5, 0.0, 0.0), bevel_width=0.018)
	shell_fan(
		f"door_pull_{index}", (pull_x, -1.275, 1.72), (0.48, 0.14, 0.48),
		MATS["gold"], MATS["gold_light"], metal_gold, metal_gold_light,
		ribs=5,
	)

for side, x in (("left", -2.01), ("right", 2.01)):
	rounded_box(f"side_inset_{side}", (x, 0.02, 1.70), (0.07, 1.36, 1.76), MATS["wood_inset"], body_inset, radius=0.04, segments=2)
	rounded_rect_moulding(
		f"side_moulding_{side}", (x + (-0.045 if x < 0.0 else 0.045), 0.02, 1.70),
		0.58, 0.79, 0.14, 0.035, MATS["wood_light"], body_light, axis="YZ",
	)

# Scalloped terrazzo counter with a topological oval opening, not a painted hole.
countertop_ring("scalloped_countertop", top_cream)
chip_positions = (
	(-1.73, -0.78), (-1.28, -0.94), (-0.79, -0.98), (0.76, -0.98), (1.27, -0.92), (1.73, -0.74),
	(-1.86, -0.20), (1.86, -0.22), (-1.82, 0.40), (1.83, 0.42),
	(-1.63, 0.83), (-1.15, 0.96), (-0.58, 0.94), (0.58, 0.94), (1.17, 0.96), (1.64, 0.82),
)
chip_groups = ((MATS["chip_peach"], chips_peach), (MATS["chip_lav"], chips_lav), (MATS["chip_aqua"], chips_aqua))
for index, (x, y) in enumerate(chip_positions):
	mat, group = chip_groups[index % len(chip_groups)]
	terrazzo_chip(f"counter_chip_{index}", (x, y, 3.565), 0.075 + 0.012 * float(index % 3), mat, group, index + 21)

# Smooth six-ring ceramic bowl, low water glint, and a detailed perforated drain.
basin_bowl("deep_oval_basin", basin_aqua)
flat_ellipse("basin_water_glint", (0.0, -0.16, 2.705), (0.47, 0.225), MATS["basin_light"], basin_light, segments=40)
cylinder("drain_plate", (0.0, -0.16, 2.722), 0.18, 0.035, MATS["gold"], metal_gold, vertices=32, bevel_width=0.012)
for index, (dx, dy) in enumerate(((0.0, 0.0), (-0.075, 0.0), (0.075, 0.0), (0.0, -0.075), (0.0, 0.075))):
	cylinder(f"drain_hole_{index}", (dx, -0.16 + dy, 2.744), 0.024, 0.010, MATS["drain_dark"], metal_dark,
		vertices=12, bevel_width=0.0)

# High gooseneck faucet with a separate pearl aerator.
rounded_box("faucet_square_base", (0.0, 0.62, 3.65), (0.43, 0.43, 0.18), MATS["gold"], metal_gold, radius=0.055, segments=2)
cylinder("faucet_collar", (0.0, 0.62, 3.82), 0.17, 0.22, MATS["gold_light"], metal_gold_light, vertices=28, bevel_width=0.018)
curve_tube(
	"gooseneck_faucet",
	[(0.0, 0.62, 3.85), (0.0, 0.62, 4.38), (0.0, 0.45, 4.73), (0.0, -0.04, 4.72), (0.0, -0.29, 4.33)],
	0.115,
	MATS["gold"],
	metal_gold,
	bevel_resolution=3,
	path_resolution=4,
)
cylinder("aerator_gold_collar", (0.0, -0.29, 4.30), 0.13, 0.13, MATS["gold_light"], metal_gold_light, vertices=28, bevel_width=0.014)
cylinder("pearl_aerator", (0.0, -0.29, 4.20), 0.105, 0.13, MATS["nozzle"], metal_nozzle, vertices=24, bevel_width=0.012)

for index, x in enumerate((-0.82, 0.82)):
	cylinder(f"tap_base_{index}", (x, 0.63, 3.67), 0.19, 0.17, MATS["gold"], metal_gold, vertices=28, bevel_width=0.018)
	shell_fan(
		f"tap_shell_{index}", (x, 0.60, 3.94), (0.68, 0.20, 0.69),
		MATS["lavender"], MATS["lavender_light"], metal_lav, metal_lav_light,
	)

# Nested, extruded arch mirror with lavender frame, gold inner trim, and crest.
arch_ring(
	"mirror_outer_frame", (1.70, 3.52, 5.15), (1.47, 3.76, 5.15),
	0.91, 0.25, MATS["lavender"], mirror_lav, bevel_width=0.045,
)
arch_ring(
	"mirror_gold_inner_trim", (1.485, 3.74, 5.15), (1.365, 3.85, 5.15),
	0.755, 0.13, MATS["gold"], mirror_gold, bevel_width=0.0,
)
arch_solid("mirror_aqua_glass", (1.33, 3.87, 5.15), 0.79, MATS["mirror"], mirror_glass)
rounded_box("mirror_left_foot", (-1.57, 0.91, 3.65), (0.32, 0.30, 0.30), MATS["lavender_light"], mirror_lav_light, radius=0.07, segments=2)
rounded_box("mirror_right_foot", (1.57, 0.91, 3.65), (0.32, 0.30, 0.30), MATS["lavender_light"], mirror_lav_light, radius=0.07, segments=2)
rounded_box("mirror_bottom_rail", (0.0, 0.91, 3.69), (3.28, 0.30, 0.24), MATS["lavender"], mirror_lav, radius=0.07, segments=2)
shell_fan(
	"mirror_crest", (0.0, 0.75, 6.56), (1.10, 0.24, 0.66),
	MATS["lavender"], MATS["lavender_light"], mirror_lav, mirror_lav_light,
)

# Two restrained geometric gleams keep the mirror readable without transparency.
rounded_box("mirror_gleam_wide", (-0.48, 0.735, 5.22), (0.13, 0.035, 1.48), MATS["mirror_highlight"], mirror_highlight,
	radius=0.025, segments=1, rotation=(0.0, math.radians(-24.0), 0.0))
rounded_box("mirror_gleam_small", (0.05, 0.732, 5.65), (0.07, 0.035, 0.72), MATS["mirror_highlight"], mirror_highlight,
	radius=0.020, segments=1, rotation=(0.0, math.radians(-24.0), 0.0))


# Consolidate matching material islands so the detailed prop remains mobile-safe.
joined_objects = (
	join_group("VanityBody_WoodHoney", body_wood, MATS["wood"]),
	join_group("VanityBody_WoodAmber", body_light, MATS["wood_light"]),
	join_group("VanityBody_WoodShadow", body_dark, MATS["wood_dark"]),
	join_group("VanityBody_InsetPanels", body_inset, MATS["wood_inset"]),
	join_group("VanityTop_CreamTerrazzo", top_cream, MATS["cream"]),
	join_group("VanityTop_ChipsPeach", chips_peach, MATS["chip_peach"]),
	join_group("VanityTop_ChipsLavender", chips_lav, MATS["chip_lav"]),
	join_group("VanityTop_ChipsAqua", chips_aqua, MATS["chip_aqua"]),
	join_group("VanityBasin_AquaCeramic", basin_aqua, MATS["basin"]),
	join_group("VanityBasin_WaterGlow", basin_light, MATS["basin_light"]),
	join_group("VanityMetal_WarmGold", metal_gold, MATS["gold"]),
	join_group("VanityMetal_GoldHighlights", metal_gold_light, MATS["gold_light"]),
	join_group("VanityMetal_LavenderHandles", metal_lav, MATS["lavender"]),
	join_group("VanityMetal_HandleRibs", metal_lav_light, MATS["lavender_light"]),
	join_group("VanityMetal_DrainRecesses", metal_dark, MATS["drain_dark"]),
	join_group("VanityMetal_PearlAerator", metal_nozzle, MATS["nozzle"]),
	join_group("VanityMirror_LavenderFrame", mirror_lav, MATS["lavender"]),
	join_group("VanityMirror_FrameHighlights", mirror_lav_light, MATS["lavender_light"]),
	join_group("VanityMirror_GoldTrim", mirror_gold, MATS["gold"]),
	join_group("VanityMirror_AquaGlass", mirror_glass, MATS["mirror"]),
	join_group("VanityMirror_PearlGleam", mirror_highlight, MATS["mirror_highlight"]),
)


def descendants(node: bpy.types.Object) -> list[bpy.types.Object]:
	items = [node]
	for child in node.children:
		items.extend(descendants(child))
	return items


def triangle_count(node: bpy.types.Object) -> int:
	total = 0
	for obj in descendants(node):
		if obj.type == "MESH":
			obj.data.calc_loop_triangles()
			total += len(obj.data.loop_triangles)
	return total


def bounds_for(node: bpy.types.Object) -> tuple[Vector, Vector]:
	mins = Vector((1e9, 1e9, 1e9))
	maxs = Vector((-1e9, -1e9, -1e9))
	for obj in descendants(node):
		if obj.type != "MESH":
			continue
		for corner in obj.bound_box:
			point = obj.matrix_world @ Vector(corner)
			mins.x = min(mins.x, point.x)
			mins.y = min(mins.y, point.y)
			mins.z = min(mins.z, point.z)
			maxs.x = max(maxs.x, point.x)
			maxs.y = max(maxs.y, point.y)
			maxs.z = max(maxs.z, point.z)
	return mins, maxs


def export_glb() -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for obj in descendants(root):
		obj.hide_set(False)
		obj.hide_render = False
		obj.select_set(True)
	bpy.context.view_layer.objects.active = root
	bpy.ops.export_scene.gltf(
		filepath=str(RUNTIME_OUT),
		export_format="GLB",
		use_selection=True,
		export_materials="EXPORT",
		export_animations=False,
		export_yup=True,
	)
	bpy.ops.object.select_all(action="DESELECT")


tris = triangle_count(root)
mins, maxs = bounds_for(root)
for audit_obj in root.children:
	if audit_obj.type == "MESH":
		audit_obj.data.calc_loop_triangles()
		print("SINK_V2|MESH", audit_obj.name, len(audit_obj.data.loop_triangles))
if tris > 10000:
	raise RuntimeError(f"Sink exceeds 10k triangle target: {tris}")
if abs(mins.z) > 0.001:
	raise RuntimeError(f"Sink must sit at z=0, got {mins.z}")
export_glb()
print("SINK_V2|EXPORTED", RUNTIME_OUT)
print("SINK_V2|AUDIT|triangles", tris, "bounds_min", tuple(round(v, 4) for v in mins), "bounds_max", tuple(round(v, 4) for v in maxs))


# Polished Eevee concept render; camera/lights/floor are not part of GLB selection.
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 900
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.render.filepath = str(QA_OUT)
scene.render.image_settings.color_mode = "RGBA"
scene.render.image_settings.color_depth = "8"

if scene.world is None:
	scene.world = bpy.data.worlds.new("QA_World")
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get("Background")
background.inputs["Color"].default_value = (0.94, 0.89, 0.84, 1.0)
background.inputs["Strength"].default_value = 0.55

try:
	scene.view_settings.look = "AgX - Medium High Contrast"
except TypeError:
	pass

floor_mat = material("QAFloor", (0.89, 0.82, 0.75, 1.0), roughness=0.84, coat=0.0)
bpy.ops.mesh.primitive_plane_add(size=80.0, location=(0.0, 0.0, -0.015))
floor = bpy.context.active_object
floor.name = "QA_Ground"
assign(floor, floor_mat)

camera_data = bpy.data.cameras.new("QA_Camera")
camera_data.type = "ORTHO"
camera_data.ortho_scale = 8.15
camera = bpy.data.objects.new("QA_Camera", camera_data)
bpy.context.collection.objects.link(camera)
target = Vector((0.0, 0.0, 3.38))
camera.location = Vector((7.8, -10.6, 10.15))
camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
scene.camera = camera


def area_light(name: str, location: tuple[float, float, float], energy: float, size: float, color: tuple[float, float, float]) -> None:
	data = bpy.data.lights.new(name, "AREA")
	data.energy = energy
	data.shape = "DISK"
	data.size = size
	data.color = color
	obj = bpy.data.objects.new(name, data)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


area_light("QA_Key", (-4.5, -6.5, 10.0), 980.0, 5.0, (1.0, 0.78, 0.65))
area_light("QA_Fill", (5.5, -4.0, 6.2), 680.0, 4.0, (0.65, 0.86, 1.0))
area_light("QA_Rim", (3.0, 4.5, 9.0), 840.0, 3.5, (0.78, 0.67, 1.0))

bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_OUT))
bpy.ops.render.render(write_still=True)
print("SINK_V2|SAVED", SOURCE_OUT)
print("SINK_V2|RENDERED", QA_OUT)
