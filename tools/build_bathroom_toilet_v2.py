#!/usr/bin/env python3
"""Build the image-directed Royal Bathroom toilet as a polished static GLB.

The conventional silhouette follows the older toilet art while the palette,
trim, terrazzo, and exact front/side proportions follow the approved generated
turnaround. Blender +X is the bowl/front direction, Blender -X is the cistern;
Godot therefore needs no runtime yaw. Blender X/Y/Z maps to Godot X/-Z/Y.

Usage:
  blender --background --python tools/build_bathroom_toilet_v2.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_OUT = ROOT / "assets" / "castle" / "bathroom_toilet.glb"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_bathroom_props"
BLEND_OUT = SOURCE_OUT / "bathroom_toilet_v2.blend"

SOURCE_OUT.mkdir(parents=True, exist_ok=True)
QA_OUT.mkdir(parents=True, exist_ok=True)
RUNTIME_OUT.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


def make_material(
	name: str,
	color: tuple[float, float, float, float],
	roughness: float,
	metallic: float = 0.0,
) -> bpy.types.Material:
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = roughness
	bsdf.inputs["Metallic"].default_value = metallic
	return mat


MATS = {
	"porcelain": make_material("MR_Toilet_WarmPearlPorcelain", (0.94, 0.86, 0.72, 1.0), 0.48),
	"porcelain_light": make_material("MR_Toilet_PearlHighlight", (1.0, 0.94, 0.83, 1.0), 0.42),
	"porcelain_shadow": make_material("MR_Toilet_LavenderShadow", (0.74, 0.66, 0.73, 1.0), 0.63),
	"seat": make_material("MR_Toilet_RosyLavenderSeat", (0.72, 0.46, 0.75, 1.0), 0.46),
	"seat_light": make_material("MR_Toilet_SeatInset", (0.84, 0.64, 0.84, 1.0), 0.52),
	"water": make_material("MR_Toilet_AquaWater", (0.22, 0.70, 0.74, 1.0), 0.22),
	"water_light": make_material("MR_Toilet_WaterRipple", (0.55, 0.91, 0.88, 1.0), 0.18),
	"gold": make_material("MR_Toilet_SoftGold", (0.93, 0.58, 0.15, 1.0), 0.32, 0.52),
	"fleck_aqua": make_material("MR_Toilet_TerrazzoAqua", (0.45, 0.78, 0.76, 1.0), 0.74),
	"fleck_lavender": make_material("MR_Toilet_TerrazzoLavender", (0.69, 0.53, 0.78, 1.0), 0.74),
	"fleck_peach": make_material("MR_Toilet_TerrazzoPeach", (0.91, 0.62, 0.48, 1.0), 0.74),
}


def root_object(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.data.materials.append(mat)
	return obj


def mesh_object(
	name: str,
	vertices: list[tuple[float, float, float]],
	faces: list[tuple[int, ...]],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	smooth: bool = True,
) -> bpy.types.Object:
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(vertices, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	assign(obj, mat)
	if smooth:
		for polygon in mesh.polygons:
			polygon.use_smooth = True
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
	modifier = obj.modifiers.new("hand_softened_edges", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	modifier.harden_normals = True
	apply_modifier(obj, modifier)
	return obj


def cube(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return obj


def rounded_box(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	radius: float,
	segments: int = 3,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	obj = cube(name, location, size, mat, parent, rotation)
	return bevel(obj, min(radius, min(size) * 0.24), segments)


def sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 12,
	rings: int = 8,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(
		segments=segments,
		ring_count=rings,
		radius=1.0,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def cylinder(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	vertices: int = 16,
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
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(radius * 0.10, depth * 0.10), 2)


def ellipse_loft(
	name: str,
	rings: list[tuple[float, float, float, float]],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 36,
	cap_bottom: bool = True,
	cap_top: bool = False,
	inward: bool = False,
) -> bpy.types.Object:
	"""Loft horizontal ellipse rings: (center_x, radius_x, radius_y, z)."""
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	for center_x, radius_x, radius_y, z in rings:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			vertices.append((center_x + math.cos(a) * radius_x, math.sin(a) * radius_y, z))
	for ring_index in range(len(rings) - 1):
		base = ring_index * segments
		next_base = (ring_index + 1) * segments
		for index in range(segments):
			next_index = (index + 1) % segments
			face = (base + index, base + next_index, next_base + next_index, next_base + index)
			faces.append(tuple(reversed(face)) if inward else face)
	if cap_bottom:
		center = len(vertices)
		vertices.append((rings[0][0], 0.0, rings[0][3]))
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((center, next_index, index))
	if cap_top:
		base = (len(rings) - 1) * segments
		center = len(vertices)
		vertices.append((rings[-1][0], 0.0, rings[-1][3]))
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((center, base + index, base + next_index))
	return mesh_object(name, vertices, faces, mat, parent)


def ellipse_annular_prism(
	name: str,
	center: tuple[float, float],
	outer: tuple[float, float],
	inner: tuple[float, float],
	z_bottom: float,
	z_top: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 36,
) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	for z in (z_bottom, z_top):
		for radii in (outer, inner):
			for index in range(segments):
				a = float(index) * math.tau / float(segments)
				vertices.append((center[0] + math.cos(a) * radii[0], center[1] + math.sin(a) * radii[1], z))
	for index in range(segments):
		n = (index + 1) % segments
		ob, ib = index, segments + index
		ot, it = segments * 2 + index, segments * 3 + index
		obn, ibn = n, segments + n
		otn, itn = segments * 2 + n, segments * 3 + n
		faces.extend([
			(ob, obn, otn, ot),
			(ibn, ib, it, itn),
			(ot, otn, itn, it),
			(obn, ob, ib, ibn),
		])
	return bevel(mesh_object(name, vertices, faces, mat, parent), 0.055, 2)


def elliptical_torus(
	name: str,
	center: tuple[float, float, float],
	center_radii: tuple[float, float],
	tube_xy: float,
	tube_z: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 36,
	cross_segments: int = 10,
) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	rx, ry = center_radii
	for index in range(segments):
		theta = float(index) * math.tau / float(segments)
		cx = center[0] + math.cos(theta) * rx
		cy = center[1] + math.sin(theta) * ry
		normal = Vector((math.cos(theta) / rx, math.sin(theta) / ry, 0.0)).normalized()
		for cross in range(cross_segments):
			phi = float(cross) * math.tau / float(cross_segments)
			horizontal = math.cos(phi) * tube_xy
			vertices.append((
				cx + normal.x * horizontal,
				cy + normal.y * horizontal,
				center[2] + math.sin(phi) * tube_z,
			))
	for index in range(segments):
		next_index = (index + 1) % segments
		for cross in range(cross_segments):
			next_cross = (cross + 1) % cross_segments
			a = index * cross_segments + cross
			b = next_index * cross_segments + cross
			c = next_index * cross_segments + next_cross
			d = index * cross_segments + next_cross
			faces.append((a, b, c, d))
	return mesh_object(name, vertices, faces, mat, parent)


def superellipse_point(angle: float, radius_x: float, radius_y: float, exponent: float) -> tuple[float, float]:
	c = math.cos(angle)
	s = math.sin(angle)
	power = 2.0 / exponent
	return (
		radius_x * math.copysign(abs(c) ** power, c),
		radius_y * math.copysign(abs(s) ** power, s),
	)


def rounded_rect_loft(
	name: str,
	rings: list[tuple[float, float, float, float, float]],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 32,
	exponent: float = 4.0,
) -> bpy.types.Object:
	"""Rounded rectangular horizontal rings: (cx, rx, ry, z, exponent_scale)."""
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	for cx, rx, ry, z, exp_scale in rings:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			x, y = superellipse_point(a, rx, ry, exponent * exp_scale)
			vertices.append((cx + x, y, z))
	for ring_index in range(len(rings) - 1):
		base = ring_index * segments
		next_base = (ring_index + 1) * segments
		for index in range(segments):
			n = (index + 1) % segments
			faces.append((base + index, base + n, next_base + n, next_base + index))
	bottom_center = len(vertices)
	vertices.append((rings[0][0], 0.0, rings[0][3]))
	top_center = len(vertices)
	vertices.append((rings[-1][0], 0.0, rings[-1][3]))
	last = (len(rings) - 1) * segments
	for index in range(segments):
		n = (index + 1) % segments
		faces.append((bottom_center, n, index))
		faces.append((top_center, last + index, last + n))
	return mesh_object(name, vertices, faces, mat, parent)


def solid_oval_lid(
	name: str,
	hinge: tuple[float, float, float],
	radius_y: float,
	radius_z: float,
	local_center_z: float,
	thickness: float,
	lean_degrees: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 36,
	exponent: float = 2.35,
) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	lean = math.radians(lean_degrees)
	cos_a = math.cos(lean)
	sin_a = math.sin(lean)

	def transform(local_x: float, local_y: float, local_z: float) -> tuple[float, float, float]:
		return (
			hinge[0] + cos_a * local_x + sin_a * local_z,
			hinge[1] + local_y,
			hinge[2] - sin_a * local_x + cos_a * local_z,
		)

	for local_x in (-thickness * 0.5, thickness * 0.5):
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			y, z = superellipse_point(a, radius_y, radius_z, exponent)
			vertices.append(transform(local_x, y, local_center_z + z))
	front_center = len(vertices)
	vertices.append(transform(-thickness * 0.5, 0.0, local_center_z))
	back_center = len(vertices)
	vertices.append(transform(thickness * 0.5, 0.0, local_center_z))
	for index in range(segments):
		n = (index + 1) % segments
		faces.append((index, n, segments + n, segments + index))
		faces.append((front_center, n, index))
		faces.append((back_center, segments + index, segments + n))
	obj = mesh_object(name, vertices, faces, mat, parent, smooth=False)
	# Thin decorative insets need a proportionally smaller bevel; a fixed 0.07
	# bevel on the 0.045-deep inset overlaps itself and exports sliver triangles.
	return bevel(obj, min(0.07, thickness * 0.28), 3)


def tube_curve(
	name: str,
	points: list[tuple[float, float, float]],
	radius: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	curve_data = bpy.data.curves.new(name + "_curve", "CURVE")
	curve_data.dimensions = "3D"
	curve_data.resolution_u = 3
	curve_data.bevel_depth = radius
	curve_data.bevel_resolution = 2
	curve_data.use_fill_caps = True
	curve_data.resolution_u = 3
	spline = curve_data.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, position in zip(spline.bezier_points, points):
		point.co = position
		point.handle_left_type = "AUTO"
		point.handle_right_type = "AUTO"
	curve = bpy.data.objects.new(name, curve_data)
	bpy.context.collection.objects.link(curve)
	curve.parent = parent
	curve.data.materials.append(mat)
	bpy.ops.object.select_all(action="DESELECT")
	curve.select_set(True)
	bpy.context.view_layer.objects.active = curve
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def shell_badge(parent: bpy.types.Object) -> list[bpy.types.Object]:
	parts: list[bpy.types.Object] = []
	# Five small flattened lobes fan across the visible tank side (-Y).
	center = Vector((-1.02, -1.465, 3.56))
	for index, degrees in enumerate((-44.0, -22.0, 0.0, 22.0, 44.0)):
		a = math.radians(degrees)
		offset = Vector((math.sin(a) * 0.15, 0.0, math.cos(a) * 0.11))
		parts.append(sphere(
			f"ToiletSeat_ShellBadgeLobe_{index}",
			tuple(center + offset),
			(0.105, 0.045, 0.30),
			MATS["seat_light"],
			parent,
			10,
			6,
			(0.0, a, 0.0),
		))
	parts.append(sphere(
		"ToiletSeat_ShellBadgeFoot",
		(-1.02, -1.48, 3.31),
		(0.27, 0.055, 0.13),
		MATS["seat"],
		parent,
		10,
		6,
	))
	return parts


def add_terrazzo(parent: bpy.types.Object) -> list[bpy.types.Object]:
	parts: list[bpy.types.Object] = []
	colors = (MATS["fleck_aqua"], MATS["fleck_lavender"], MATS["fleck_peach"])
	# Modeled flecks are deliberately sparse and low relief. They export as
	# ordinary geometry/materials, so the finish has no procedural dependency.
	tank_side = [
		(-1.36, 3.10, 0.085), (-0.82, 3.18, 0.070), (-1.18, 3.88, 0.080),
		(-0.62, 4.25, 0.065), (-1.48, 4.36, 0.060), (-0.72, 3.54, 0.055),
	]
	for index, (x, z, size) in enumerate(tank_side):
		parts.append(rounded_box(
			f"ToiletTerrazzo_Side_{index}",
			(x, -1.454, z),
			(size * 1.25, 0.025, size * 1.25),
			colors[index % len(colors)],
			parent,
			0.008,
			1,
			(0.0, math.radians(45.0), 0.0),
		))
	tank_front = [
		(-0.60, 3.22, 0.060), (0.54, 3.56, 0.070), (-0.46, 4.42, 0.055),
	]
	for index, (y, z, size) in enumerate(tank_front):
		parts.append(rounded_box(
			f"ToiletTerrazzo_Front_{index}",
			(-0.244, y, z),
			(0.025, size * 1.30, size * 1.30),
			colors[(index + 1) % len(colors)],
			parent,
			0.008,
			1,
			(math.radians(45.0), 0.0, 0.0),
		))
	return parts


def join_material_group(
	root: bpy.types.Object,
	mat: bpy.types.Material,
	name: str,
) -> bpy.types.Object:
	objects = [
		obj for obj in root.children
		if obj.type == "MESH" and len(obj.data.materials) > 0 and obj.data.materials[0] == mat
	]
	if not objects:
		raise ValueError(f"No meshes use material {mat.name} for role {name}")
	if len(objects) == 1:
		joined = objects[0]
		joined.name = name
		joined.data.materials.clear()
		joined.data.materials.append(mat)
		for polygon in joined.data.polygons:
			polygon.material_index = 0
		return joined
	bpy.ops.object.select_all(action="DESELECT")
	for obj in objects:
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


def bake_mesh_transforms(root: bpy.types.Object) -> None:
	# Joining rotated terrazzo diamonds without first baking their transforms can
	# distort the consolidated bounds. Baking is lossless because the root is an
	# identity transform at the exact authored floor origin.
	for obj in list(root.children):
		if obj.type != "MESH":
			continue
		bpy.ops.object.select_all(action="DESELECT")
		obj.select_set(True)
		bpy.context.view_layer.objects.active = obj
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		obj.select_set(False)


def consolidate_runtime_nodes(root: bpy.types.Object) -> None:
	# Each distinct finish remains independently editable, while exact-same
	# material pieces collapse into a single draw-compatible role node.
	bake_mesh_transforms(root)
	groups = [
		(MATS["porcelain"], "ToiletPorcelain_Main"),
		(MATS["porcelain_light"], "ToiletPorcelain_Trim"),
		(MATS["porcelain_shadow"], "ToiletPorcelain_Inner"),
		(MATS["seat"], "ToiletSeat_Main"),
		(MATS["seat_light"], "ToiletSeat_Detail"),
		(MATS["water"], "ToiletWater_Main"),
		(MATS["water_light"], "ToiletWater_Ripple"),
		(MATS["gold"], "ToiletMetal_Main"),
		(MATS["fleck_aqua"], "ToiletTerrazzo_Aqua"),
		(MATS["fleck_lavender"], "ToiletTerrazzo_Lavender"),
		(MATS["fleck_peach"], "ToiletTerrazzo_Peach"),
	]
	for mat, name in groups:
		join_material_group(root, mat, name)
	for obj in root.children:
		if obj.type != "MESH":
			continue
		bm = bmesh.new()
		bm.from_mesh(obj.data)
		bmesh.ops.dissolve_degenerate(bm, dist=1.0e-8, edges=list(bm.edges))
		bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
		bm.to_mesh(obj.data)
		bm.free()
		obj.data.update()
	remaining = [obj.name for obj in root.children if obj.type == "MESH" and obj.name not in {name for _, name in groups}]
	if remaining:
		raise RuntimeError(f"Unconsolidated toilet meshes: {remaining}")


def build_toilet() -> bpy.types.Object:
	root = root_object("BathroomToilet")

	# Thin rosy-lavender floor trim, then a pearl transition collar. The body
	# begins at the exact z=0 floor plane and never depends on a runtime scale.
	ellipse_loft(
		"ToiletSeat_BaseTrim",
		[(-0.42, 1.24, 1.08, 0.00), (-0.42, 1.28, 1.12, 0.10), (-0.42, 1.20, 1.05, 0.22)],
		MATS["seat"], root, 36, True, True,
	)
	ellipse_loft(
		"ToiletPorcelain_BaseCollar",
		[(-0.42, 1.18, 1.03, 0.18), (-0.40, 1.12, 1.00, 0.34)],
		MATS["porcelain_light"], root, 36, True, True,
	)

	# The continuously shifting ring centres create the conventional flowing
	# side silhouette: narrow pedestal, rear S bend, and a full rounded bowl.
	ellipse_loft(
		"ToiletPorcelain_SculptedPedestalBowl",
		[
			(-0.40, 1.10, 0.99, 0.22),
			(-0.32, 1.02, 0.93, 0.48),
			(-0.16, 0.84, 0.80, 0.82),
			(0.02, 0.78, 0.76, 1.18),
			(0.24, 0.88, 0.86, 1.50),
			(0.45, 1.08, 1.02, 1.82),
			(0.62, 1.31, 1.22, 2.12),
			(0.73, 1.49, 1.39, 2.40),
			(0.75, 1.58, 1.45, 2.64),
		],
		MATS["porcelain"], root, 36, True, False,
	)

	# The ring-centre shifts above form the readable S-profile directly in the
	# pedestal silhouette. No separate hose-like trap applique is added.

	# Thick ceramic rim + nested inner wall + water form a genuinely open bowl.
	ellipse_annular_prism(
		"ToiletPorcelain_ThickBowlRim",
		(0.75, 0.0), (1.58, 1.45), (1.15, 0.96), 2.61, 2.82,
		MATS["porcelain_light"], root, 36,
	)
	ellipse_loft(
		"ToiletPorcelain_TrueInnerBowl",
		[
			(0.75, 1.15, 0.96, 2.70),
			(0.80, 0.98, 0.78, 2.40),
			(0.82, 0.83, 0.65, 2.36),
			(0.82, 0.72, 0.57, 2.28),
		],
		MATS["porcelain_shadow"], root, 36, False, False, True,
	)
	ellipse_loft(
		"ToiletWater_DeepAqua",
		[(0.82, 0.70, 0.55, 2.295), (0.82, 0.70, 0.55, 2.32)],
		MATS["water"], root, 32, True, True,
	)
	elliptical_torus(
		"ToiletWater_Ripple",
		(0.82, 0.0, 2.335), (0.47, 0.34), 0.028, 0.018,
		MATS["water_light"], root, 28, 6,
	)

	# A toroidal cross-section gives the separate seat a soft manufactured edge
	# and preserves the opening at steep gameplay camera angles.
	elliptical_torus(
		"ToiletSeat_ThickRing",
		(0.75, 0.0, 2.93), (1.34, 1.195), 0.24, 0.13,
		MATS["seat"], root, 40, 10,
	)

	# Rounded, gently tapered cistern. A separate band and cap reproduce the
	# generated turnaround's layered toy-like finish.
	rounded_rect_loft(
		"ToiletPorcelain_RoundedCistern",
		[
			(-1.06, 0.68, 1.31, 2.62, 0.92),
			(-1.06, 0.72, 1.38, 2.78, 0.96),
			(-1.07, 0.77, 1.43, 4.49, 1.00),
			(-1.07, 0.79, 1.45, 4.68, 0.96),
		],
		MATS["porcelain"], root, 32, 4.2,
	)
	rounded_rect_loft(
		"ToiletSeat_CisternBand",
		[
			(-1.07, 0.79, 1.48, 4.58, 0.96),
			(-1.07, 0.80, 1.49, 4.72, 0.96),
		],
		MATS["seat"], root, 32, 4.2,
	)
	rounded_rect_loft(
		"ToiletPorcelain_TerrazzoTankCap",
		[
			(-1.07, 0.78, 1.48, 4.70, 0.96),
			(-1.07, 0.80, 1.50, 4.84, 0.92),
			(-1.07, 0.78, 1.47, 5.00, 0.90),
		],
		MATS["porcelain_light"], root, 32, 4.2,
	)

	# Thick raised lid leans back toward the cistern. Its inset is a second solid
	# layer, not a one-sided decal, so Mobile backface culling cannot erase it.
	hinge = (-0.10, 0.0, 2.89)
	solid_oval_lid(
		"ToiletSeat_RaisedLid",
		hinge, 1.24, 1.02, 1.03, 0.18, -8.0,
		MATS["seat"], root, 40, 2.35,
	)
	solid_oval_lid(
		"ToiletSeat_RaisedLidInset",
		(0.015, 0.0, 2.94), 1.08, 0.87, 1.00, 0.045, -8.0,
		MATS["seat_light"], root, 36, 2.35,
	)

	# Twin hinges and a familiar side flush lever keep the object instantly
	# readable as a real toilet even at the small child-facing camera scale.
	for index, y in enumerate((-0.72, 0.72)):
		cylinder(
			f"ToiletMetal_Hinge_{index}", (-0.08, y, 2.91), 0.14, 0.34,
			MATS["gold"], root, (math.pi * 0.5, 0.0, 0.0), 16,
		)
	cylinder(
		"ToiletMetal_FlushMount", (-1.22, -1.48, 4.08), 0.17, 0.15,
		MATS["gold"], root, (math.pi * 0.5, 0.0, 0.0), 18,
	)
	tube_curve(
		"ToiletMetal_FlushLever",
		[(-1.22, -1.50, 4.08), (-0.98, -1.50, 4.08), (-0.69, -1.50, 4.00)],
		0.095, MATS["gold"], root,
	)
	sphere(
		"ToiletMetal_FlushHandle", (-0.58, -1.50, 3.97), (0.22, 0.13, 0.14),
		MATS["gold"], root, 12, 7,
	)

	shell_badge(root)
	add_terrazzo(root)
	consolidate_runtime_nodes(root)
	return root


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
	items = [root]
	for child in root.children:
		items.extend(descendants(child))
	return items


def triangle_count(root: bpy.types.Object) -> int:
	total = 0
	for obj in descendants(root):
		if obj.type != "MESH":
			continue
		obj.data.calc_loop_triangles()
		total += len(obj.data.loop_triangles)
	return total


def degenerate_triangle_count(root: bpy.types.Object) -> int:
	total = 0
	for obj in descendants(root):
		if obj.type != "MESH":
			continue
		obj.data.calc_loop_triangles()
		for triangle in obj.data.loop_triangles:
			a = obj.data.vertices[triangle.vertices[0]].co
			b = obj.data.vertices[triangle.vertices[1]].co
			c = obj.data.vertices[triangle.vertices[2]].co
			if (b - a).cross(c - a).length_squared <= 1.0e-12:
				total += 1
	return total


def bounds_for(root: bpy.types.Object) -> tuple[Vector, Vector]:
	mins = Vector((1e9, 1e9, 1e9))
	maxs = Vector((-1e9, -1e9, -1e9))
	for obj in descendants(root):
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


def export_root(root: bpy.types.Object) -> None:
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
	print("EXPORTED", RUNTIME_OUT)


def audit_exported_glb(path: Path) -> tuple[int, int, int, list[tuple[str, str]]]:
	before = set(bpy.data.objects)
	bpy.ops.import_scene.gltf(filepath=str(path))
	imported = [obj for obj in bpy.data.objects if obj not in before]
	mesh_nodes = 0
	triangles = 0
	degenerates = 0
	for obj in imported:
		if obj.type != "MESH":
			continue
		mesh_nodes += 1
		obj.data.calc_loop_triangles()
		triangles += len(obj.data.loop_triangles)
		for triangle in obj.data.loop_triangles:
			a = obj.data.vertices[triangle.vertices[0]].co
			b = obj.data.vertices[triangle.vertices[1]].co
			c = obj.data.vertices[triangle.vertices[2]].co
			if (b - a).cross(c - a).length_squared <= 1.0e-12:
				degenerates += 1
	forbidden = [(obj.name, obj.type) for obj in imported if obj.type in {"ARMATURE", "LIGHT", "CAMERA"}]
	for obj in imported:
		bpy.data.objects.remove(obj, do_unlink=True)
	return triangles, mesh_nodes, degenerates, forbidden


def look_at(obj: bpy.types.Object, target: Vector) -> None:
	obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def render_qa(root: bpy.types.Object) -> None:
	scene = bpy.context.scene
	scene.render.engine = "BLENDER_EEVEE_NEXT"
	scene.render.resolution_x = 900
	scene.render.resolution_y = 900
	scene.render.resolution_percentage = 100
	scene.render.image_settings.file_format = "PNG"
	scene.render.film_transparent = False
	if scene.world is None:
		scene.world = bpy.data.worlds.new("QA_World")
	scene.world.color = (0.055, 0.045, 0.075)

	world = scene.world
	world.use_nodes = True
	background = world.node_tree.nodes.get("Background")
	background.inputs["Color"].default_value = (0.025, 0.035, 0.060, 1.0)
	background.inputs["Strength"].default_value = 0.32

	# Neutral floor catches a soft shadow and makes the exact floor origin clear.
	ground_mat = make_material("QA_Backdrop", (0.12, 0.15, 0.20, 1.0), 0.82)
	ground = rounded_box("qa_ground", (0.0, 0.0, -0.10), (11.0, 11.0, 0.20), ground_mat, root_object("QAOnly"), 0.08, 2)

	def area(name: str, location: tuple[float, float, float], energy: float, color: tuple[float, float, float], size: float) -> None:
		data = bpy.data.lights.new(name, "AREA")
		data.energy = energy
		data.color = color
		data.shape = "DISK"
		data.size = size
		lamp = bpy.data.objects.new(name, data)
		bpy.context.collection.objects.link(lamp)
		lamp.location = location
		look_at(lamp, Vector((0.1, 0.0, 2.2)))

	area("qa_key", (6.0, -7.0, 8.5), 1150.0, (1.0, 0.84, 0.68), 4.5)
	area("qa_fill", (1.0, 6.0, 6.0), 900.0, (0.56, 0.72, 1.0), 5.0)
	area("qa_rim", (-6.0, -2.0, 7.0), 1000.0, (0.80, 0.58, 1.0), 3.5)

	camera_data = bpy.data.cameras.new("qa_camera")
	camera_data.type = "ORTHO"
	camera_data.ortho_scale = 6.35
	camera = bpy.data.objects.new("qa_camera", camera_data)
	bpy.context.collection.objects.link(camera)
	camera.location = (8.4, -10.2, 8.8)
	look_at(camera, Vector((0.15, 0.0, 2.45)))
	scene.camera = camera

	scene.render.filepath = str(QA_OUT / "bathroom_toilet.png")
	bpy.ops.render.render(write_still=True)
	print("RENDERED", scene.render.filepath)


toilet = build_toilet()
export_root(toilet)
mins, maxs = bounds_for(toilet)
triangles = triangle_count(toilet)
mesh_nodes = sum(1 for obj in descendants(toilet) if obj.type == "MESH")
glb_triangles, glb_mesh_nodes, glb_degenerates, glb_forbidden = audit_exported_glb(RUNTIME_OUT)
print(
	"AUDIT bathroom_toilet_v2 triangles", triangles,
	"bounds", tuple(round(v, 4) for v in mins), tuple(round(v, 4) for v in maxs),
	"size", tuple(round(v, 4) for v in (maxs - mins)),
	"mesh_nodes", mesh_nodes,
)
print(
	"GLB_AUDIT triangles", glb_triangles,
	"mesh_nodes", glb_mesh_nodes,
	"degenerate_triangles", glb_degenerates,
	"forbidden", glb_forbidden,
)
if triangles > 10000:
	raise RuntimeError(f"Toilet triangle budget exceeded: {triangles} > 10000")
if mins.z < -0.001 or maxs.z > 5.05:
	raise RuntimeError(f"Toilet floor/height bounds invalid: z={mins.z:.4f}..{maxs.z:.4f}")
if glb_degenerates != 0:
	raise RuntimeError(f"Exported toilet contains {glb_degenerates} degenerate triangles")
if mesh_nodes > 16:
	raise RuntimeError(f"Toilet mesh node budget exceeded: {mesh_nodes} > 16")
if glb_mesh_nodes != mesh_nodes or glb_triangles != triangles:
	raise RuntimeError("Exported toilet mesh/triangle audit does not match authored source")
if glb_forbidden:
	raise RuntimeError(f"Exported toilet has forbidden nodes: {glb_forbidden}")

render_qa(toilet)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
print("SAVED", BLEND_OUT)
