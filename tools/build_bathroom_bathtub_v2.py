#!/usr/bin/env python3
"""Build the imagegen-guided Royal Bubble Bath as a polished static GLB.

The fixture is authored at the same exact runtime scale/orientation as the
original placeholder: Blender X/Y/Z maps to Godot X/-Z/Y, canonical front is
Blender -Y, and the feet touch Z=0.  Everything visible in the GLB is real
mesh geometry with embedded bespoke materials; no procedural material nodes,
external textures, armatures, lights, animation, or collision objects are
exported.

Usage:
  blender --background --python tools/build_bathroom_bathtub_v2.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
GLB_OUT = ROOT / "assets" / "castle" / "bathroom_bathtub.glb"
SOURCE_OUT = ROOT / "assets_src" / "blender" / "bathroom_bathtub_v2.blend"
QA_DIR = ROOT / "assets_src" / "blender" / "qa_bathroom_props"
QA_OUT = QA_DIR / "bathroom_bathtub.png"

GLB_OUT.parent.mkdir(parents=True, exist_ok=True)
SOURCE_OUT.parent.mkdir(parents=True, exist_ok=True)
QA_DIR.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


def make_material(
	name: str,
	color: tuple[float, float, float, float],
	roughness: float,
	metallic: float = 0.0,
	coat: float = 0.0,
	transmission: float = 0.0,
) -> bpy.types.Material:
	"""Create a simple GLTF-safe Principled material with no external inputs."""
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = roughness
	bsdf.inputs["Metallic"].default_value = metallic
	if "Coat Weight" in bsdf.inputs:
		bsdf.inputs["Coat Weight"].default_value = coat
	if "Coat Roughness" in bsdf.inputs:
		bsdf.inputs["Coat Roughness"].default_value = max(0.08, roughness * 0.45)
	if "Transmission Weight" in bsdf.inputs:
		bsdf.inputs["Transmission Weight"].default_value = transmission
	return mat


MATS = {
	"porcelain": make_material("MR_Bathtub_CreamPorcelain", (0.93, 0.84, 0.70, 1.0), 0.34, coat=0.28),
	"interior": make_material("MR_Bathtub_SeafoamInset", (0.37, 0.73, 0.70, 1.0), 0.38, coat=0.18),
	"accent": make_material("MR_Bathtub_LavenderShell", (0.56, 0.39, 0.78, 1.0), 0.31, coat=0.30),
	"accent_light": make_material("MR_Bathtub_LavenderHighlight", (0.74, 0.62, 0.91, 1.0), 0.28, coat=0.32),
	"gold": make_material("MR_Bathtub_WarmGold", (0.83, 0.46, 0.09, 1.0), 0.22, metallic=0.55, coat=0.25),
	"gold_dark": make_material("MR_Bathtub_NozzleInset", (0.20, 0.11, 0.08, 1.0), 0.48, metallic=0.10),
	"water": make_material("MR_Bathtub_AquaWater", (0.18, 0.69, 0.76, 1.0), 0.18, metallic=0.03, coat=0.45),
	"water_light": make_material("MR_Bathtub_WaterHighlight", (0.52, 0.91, 0.91, 1.0), 0.20, coat=0.38),
	"foam": make_material("MR_Bathtub_PearlFoam", (0.96, 0.98, 0.97, 1.0), 0.20, coat=0.42),
	"chip_rose": make_material("MR_Bathtub_TerrazzoRose", (0.88, 0.53, 0.58, 1.0), 0.52),
	"chip_aqua": make_material("MR_Bathtub_TerrazzoAqua", (0.32, 0.66, 0.67, 1.0), 0.52),
	"chip_lilac": make_material("MR_Bathtub_TerrazzoLilac", (0.60, 0.45, 0.78, 1.0), 0.50),
}


def root_object(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


ROOT_OBJ = root_object("BathroomBathtub")


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.data.materials.append(mat)
	return obj


def make_mesh(
	name: str,
	vertices: list[tuple[float, float, float]],
	faces: list[tuple[int, ...]],
	mat: bpy.types.Material,
	parent: bpy.types.Object = ROOT_OBJ,
	smooth: bool = True,
) -> bpy.types.Object:
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(vertices, [], faces)
	mesh.validate(verbose=False)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	assign(obj, mat)
	if smooth:
		for polygon in mesh.polygons:
			polygon.use_smooth = True
	return obj


def select_only(obj: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	select_only(obj)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
	modifier = obj.modifiers.new("hand_softened_edges", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	modifier.harden_normals = True
	apply_modifier(obj, modifier)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def transform_apply(obj: bpy.types.Object) -> bpy.types.Object:
	select_only(obj)
	bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
	obj.select_set(False)
	return obj


def rounded_box(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	radius: float,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	parent: bpy.types.Object = ROOT_OBJ,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	obj.parent = parent
	assign(obj, mat)
	transform_apply(obj)
	return bevel(obj, min(radius, min(size) * 0.22), 2)


def chip_prism(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	rotation_degrees: float,
	mat: bpy.types.Material,
) -> bpy.types.Object:
	"""Make one tiny chamfered terrazzo lozenge with a twelve-triangle budget."""
	hx = size[0] * 0.5
	hy = size[1] * 0.5
	hz = size[2] * 0.5
	a = math.radians(rotation_degrees)
	c = math.cos(a)
	s = math.sin(a)
	outline = [(-hx, 0.0), (0.0, -hy), (hx, 0.0), (0.0, hy)]
	vertices: list[tuple[float, float, float]] = []
	for z in (-hz, hz):
		for x, y in outline:
			vertices.append((
				location[0] + x * c - y * s,
				location[1] + x * s + y * c,
				location[2] + z,
			))
	faces: list[tuple[int, ...]] = [
		(3, 2, 1, 0),
		(4, 5, 6, 7),
		(0, 1, 5, 4),
		(1, 2, 6, 5),
		(2, 3, 7, 6),
		(3, 0, 4, 7),
	]
	return make_mesh(name, vertices, faces, mat, smooth=False)


def cylinder(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	vertices: int = 20,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	parent: bpy.types.Object = ROOT_OBJ,
	bevel_width: float = 0.035,
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
	if bevel_width > 0.0:
		bevel(obj, min(bevel_width, radius * 0.18, depth * 0.18), 1)
	return obj


def ellipsoid(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	segments: int = 12,
	rings: int = 6,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	parent: bpy.types.Object = ROOT_OBJ,
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
	obj.parent = parent
	assign(obj, mat)
	transform_apply(obj)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return obj


def curve_tube(
	name: str,
	points: list[tuple[float, float, float]],
	radius: float,
	mat: bpy.types.Material,
	resolution: int = 4,
	bevel_resolution: int = 2,
	parent: bpy.types.Object = ROOT_OBJ,
) -> bpy.types.Object:
	curve_data = bpy.data.curves.new(name + "_curve", "CURVE")
	curve_data.dimensions = "3D"
	curve_data.resolution_u = resolution
	curve_data.bevel_depth = radius
	curve_data.bevel_resolution = bevel_resolution
	curve_data.resolution_v = 0
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
	select_only(curve)
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	obj.name = name
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	obj.select_set(False)
	return obj


def superellipse_point(rx: float, ry: float, angle: float, exponent: float = 3.35) -> tuple[float, float]:
	c = math.cos(angle)
	s = math.sin(angle)
	power = 2.0 / exponent
	x = rx * math.copysign(abs(c) ** power, c)
	y = ry * math.copysign(abs(s) ** power, s)
	return x, y


def profiled_superellipse(
	name: str,
	rings: list[tuple[float, float, float]],
	mat: bpy.types.Material,
	segments: int = 40,
	close_bottom: bool = False,
	close_profile: bool = False,
) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	for rx, ry, z in rings:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			x, y = superellipse_point(rx, ry, a)
			vertices.append((x, y, z))
	span = len(rings) if close_profile else len(rings) - 1
	for ring_index in range(span):
		next_ring = (ring_index + 1) % len(rings)
		base = ring_index * segments
		next_base = next_ring * segments
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((base + index, base + next_index, next_base + next_index, next_base + index))
	if close_bottom:
		center = len(vertices)
		vertices.append((0.0, 0.0, rings[0][2]))
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((center, next_index, index))
	return make_mesh(name, vertices, faces, mat, smooth=True)


def superellipse_slab(
	name: str,
	rx: float,
	ry: float,
	z_bottom: float,
	z_top: float,
	mat: bpy.types.Material,
	segments: int = 40,
) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	for z in (z_bottom, z_top):
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			x, y = superellipse_point(rx, ry, a)
			vertices.append((x, y, z))
	for index in range(segments):
		next_index = (index + 1) % segments
		faces.append((index, next_index, segments + next_index, segments + index))
	faces.append(tuple(range(segments - 1, -1, -1)))
	faces.append(tuple(range(segments, segments * 2)))
	return make_mesh(name, vertices, faces, mat, smooth=True)


def ornate_loop(width: float, height: float, inset: float = 0.0) -> list[tuple[float, float]]:
	hw = width * 0.5 - inset
	hh = height * 0.5 - inset
	clip = max(0.08, min(hw, hh) * 0.22)
	return [
		(-hw + clip, -hh),
		(hw - clip, -hh),
		(hw, -hh + clip),
		(hw, hh - clip),
		(hw - clip, hh),
		(-hw + clip, hh),
		(-hw, hh - clip),
		(-hw, -hh + clip),
	]


def plane_vertex(axis: str, u: float, depth: float, v: float) -> tuple[float, float, float]:
	if axis == "y":
		return (u, depth, v)
	return (depth, u, v)


def plaque_ring(
	name: str,
	center: tuple[float, float, float],
	width: float,
	height: float,
	frame: float,
	depth: float,
	mat: bpy.types.Material,
	axis: str = "y",
) -> bpy.types.Object:
	outer = ornate_loop(width, height)
	inner = ornate_loop(width, height, frame)
	d0 = center[1] - depth * 0.5 if axis == "y" else center[0] - depth * 0.5
	d1 = center[1] + depth * 0.5 if axis == "y" else center[0] + depth * 0.5
	cu = center[0] if axis == "y" else center[1]
	cz = center[2]
	vertices: list[tuple[float, float, float]] = []
	for d in (d0, d1):
		for loop in (outer, inner):
			for u, v in loop:
				vertices.append(plane_vertex(axis, cu + u, d, cz + v))
	n = len(outer)
	faces: list[tuple[int, ...]] = []
	for index in range(n):
		next_index = (index + 1) % n
		ob = index
		ib = n + index
		of = n * 2 + index
		inf = n * 3 + index
		faces.extend([
			(of, n * 2 + next_index, n * 3 + next_index, inf),
			(ob, of, n * 2 + next_index, next_index),
			(ib, n + next_index, n * 3 + next_index, inf),
		])
	return bevel(make_mesh(name, vertices, faces, mat, smooth=False), min(0.045, frame * 0.20), 1)


def plaque_fill(
	name: str,
	center: tuple[float, float, float],
	width: float,
	height: float,
	depth: float,
	mat: bpy.types.Material,
	axis: str = "y",
) -> bpy.types.Object:
	loop = ornate_loop(width, height)
	d0 = center[1] - depth * 0.5 if axis == "y" else center[0] - depth * 0.5
	d1 = center[1] + depth * 0.5 if axis == "y" else center[0] + depth * 0.5
	cu = center[0] if axis == "y" else center[1]
	cz = center[2]
	vertices = [plane_vertex(axis, cu + u, d, cz + v) for d in (d0, d1) for u, v in loop]
	n = len(loop)
	faces: list[tuple[int, ...]] = [tuple(range(n - 1, -1, -1)), tuple(range(n, n * 2))]
	for index in range(n):
		next_index = (index + 1) % n
		faces.append((index, next_index, n + next_index, n + index))
	# This fill sits behind two raised molding layers, so a bevel contributes no
	# readable silhouette. More importantly, beveling a 0.05-0.065-deep plaque
	# created collapsed export faces when the bevel approached half its depth.
	return make_mesh(name, vertices, faces, mat, smooth=False)


def teardrop_lobe(
	name: str,
	center: tuple[float, float, float],
	angle: float,
	length: float,
	width: float,
	depth: float,
	mat: bpy.types.Material,
	axis: str = "y",
	outward: float = -1.0,
	length_segments: int = 5,
	cross_segments: int = 5,
) -> bpy.types.Object:
	"""Create one rounded, tapered shell rib as a true closed volume."""
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	du = math.sin(angle)
	dv = math.cos(angle)
	pu = math.cos(angle)
	pv = -math.sin(angle)
	for ring in range(length_segments + 1):
		t = float(ring) / float(length_segments)
		center_u = du * length * t
		center_v = dv * length * t
		profile = max(0.035, math.sin(math.pi * (0.05 + t * 0.90)) ** 0.72)
		for side in range(cross_segments):
			a = float(side) * math.tau / float(cross_segments)
			plane_offset = math.cos(a) * width * profile
			depth_offset = math.sin(a) * depth * profile
			u = center_u + pu * plane_offset
			v = center_v + pv * plane_offset
			if axis == "y":
				vertices.append((center[0] + u, center[1] + outward * depth_offset, center[2] + v))
			else:
				vertices.append((center[0] + outward * depth_offset, center[1] + u, center[2] + v))
	for ring in range(length_segments):
		base = ring * cross_segments
		next_base = (ring + 1) * cross_segments
		for side in range(cross_segments):
			next_side = (side + 1) % cross_segments
			faces.append((base + side, base + next_side, next_base + next_side, next_base + side))
	faces.append(tuple(range(cross_segments - 1, -1, -1)))
	last = length_segments * cross_segments
	faces.append(tuple(last + i for i in range(cross_segments)))
	return make_mesh(name, vertices, faces, mat, smooth=True)


def scallop_shell(
	name: str,
	center: tuple[float, float, float],
	width: float,
	height: float,
	depth: float,
	mat: bpy.types.Material,
	ribs: int = 7,
	axis: str = "y",
	outward: float = -1.0,
) -> list[bpy.types.Object]:
	parts: list[bpy.types.Object] = []
	# Fit the fan to the requested silhouette instead of letting the outer ribs
	# flare into flower petals.  The slight overlap creates deep molded grooves.
	spread = min(math.radians(38.0), math.atan2(width * 0.46, max(height, 0.001)))
	for index in range(ribs):
		t = float(index) / float(ribs - 1) if ribs > 1 else 0.5
		angle = -spread + t * spread * 2.0
		length = height * (0.91 + 0.09 * math.cos(angle))
		parts.append(teardrop_lobe(
			f"{name}_rib_{index + 1:02d}",
			center,
			angle,
			length,
			width / float(ribs) * 1.22,
			depth,
			mat,
			axis,
			outward,
		))
	return parts


def oriented_matrix(location: tuple[float, float, float], local_z: Vector) -> Matrix:
	rotation = local_z.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
	return Matrix.Translation(Vector(location)) @ rotation


def apply_matrix(obj: bpy.types.Object, matrix: Matrix) -> bpy.types.Object:
	obj.matrix_world = matrix @ obj.matrix_world
	select_only(obj)
	bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
	obj.parent = ROOT_OBJ
	obj.select_set(False)
	return obj


def ellipse_cylinder_local(
	name: str,
	rx: float,
	ry: float,
	z_bottom: float,
	z_top: float,
	mat: bpy.types.Material,
	segments: int = 32,
) -> bpy.types.Object:
	vertices: list[tuple[float, float, float]] = []
	faces: list[tuple[int, ...]] = []
	for z in (z_bottom, z_top):
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			vertices.append((math.cos(a) * rx, math.sin(a) * ry, z))
	for index in range(segments):
		next_index = (index + 1) % segments
		faces.append((index, next_index, segments + next_index, segments + index))
	faces.extend([tuple(range(segments - 1, -1, -1)), tuple(range(segments, segments * 2))])
	return make_mesh(name, vertices, faces, mat, smooth=True)


def shower_dome(
	location: tuple[float, float, float],
	face_direction: Vector,
) -> list[bpy.types.Object]:
	"""Build a scalloped dome, gold face, nine raised ribs, and real nozzle insets."""
	parts: list[bpy.types.Object] = []
	segments = 36
	radial_rings = (0.26, 0.54, 0.78, 1.0)
	vertices: list[tuple[float, float, float]] = [(0.0, 0.0, 0.46)]
	for r in radial_rings:
		for index in range(segments):
			a = float(index) * math.tau / float(segments)
			rib = 0.045 * (math.cos(a * 9.0) ** 2) * r
			scallop = 1.0 + 0.035 * math.cos(a * 9.0) * (r ** 2)
			x = math.cos(a) * 0.82 * r * scallop
			y = math.sin(a) * 0.59 * r * scallop
			z = 0.46 * (1.0 - r ** 1.45) + rib
			vertices.append((x, y, z))
	faces: list[tuple[int, ...]] = []
	for index in range(segments):
		next_index = (index + 1) % segments
		faces.append((0, 1 + index, 1 + next_index))
	for ring in range(len(radial_rings) - 1):
		base = 1 + ring * segments
		next_base = base + segments
		for index in range(segments):
			next_index = (index + 1) % segments
			faces.append((base + index, next_base + index, next_base + next_index, base + next_index))
	dome = make_mesh("TubAccent_ShowerShellDome", vertices, faces, MATS["accent"], smooth=True)
	local_z = -face_direction.normalized()
	matrix = oriented_matrix(location, local_z)
	apply_matrix(dome, matrix)
	parts.append(dome)

	face = ellipse_cylinder_local("TubMetal_ShowerFace", 0.82, 0.59, -0.085, 0.0, MATS["gold"], 36)
	apply_matrix(face, matrix)
	parts.append(face)

	# Raised ribs make the generated shell silhouette survive the mobile camera.
	for index in range(9):
		a = float(index) * math.tau / 9.0
		points: list[tuple[float, float, float]] = []
		for r in (0.05, 0.32, 0.62, 0.91):
			x = math.cos(a) * 0.82 * r
			y = math.sin(a) * 0.59 * r
			z = 0.46 * (1.0 - r ** 1.45) + 0.055
			points.append((x, y, z))
		rib = curve_tube(f"TubAccent_ShowerRib_{index + 1:02d}", points, 0.025, MATS["accent_light"], 2, 0)
		apply_matrix(rib, matrix)
		parts.append(rib)

	# Dark inset cylinders are actual geometry, not a procedural dot texture.
	hole_positions = [
		(0.0, 0.0),
		(-0.22, 0.0), (0.22, 0.0),
		(-0.42, 0.0), (0.42, 0.0),
		(-0.12, -0.21), (0.12, -0.21),
		(-0.12, 0.21), (0.12, 0.21),
		(-0.39, -0.20), (0.39, -0.20),
		(-0.39, 0.20), (0.39, 0.20),
	]
	for index, (x, y) in enumerate(hole_positions):
		hole = cylinder(
			f"ShowerNozzleInset_{index + 1:02d}",
			(x, y, -0.105),
			0.045,
			0.025,
			MATS["gold_dark"],
			vertices=10,
			bevel_width=0.0,
		)
		apply_matrix(hole, matrix)
		parts.append(hole)
	return parts


def join_role(name: str, objects: list[bpy.types.Object], mat: bpy.types.Material) -> bpy.types.Object:
	if not objects:
		raise ValueError(f"No geometry supplied for role {name}")
	bpy.ops.object.select_all(action="DESELECT")
	for obj in objects:
		obj.select_set(True)
	bpy.context.view_layer.objects.active = objects[0]
	bpy.ops.object.join()
	joined = bpy.context.active_object
	joined.name = name
	joined.parent = ROOT_OBJ
	joined.data.materials.clear()
	joined.data.materials.append(mat)
	for polygon in joined.data.polygons:
		polygon.material_index = 0
	joined.select_set(False)
	return joined


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
	items = [root]
	for child in root.children:
		items.extend(descendants(child))
	return items


# ---------------------------------------------------------------------------
# Sculpted tub body: a rounded-rectangle shell, substantial rim, true cavity.
# ---------------------------------------------------------------------------

porcelain_parts: list[bpy.types.Object] = []
interior_parts: list[bpy.types.Object] = []
accent_parts: list[bpy.types.Object] = []
metal_parts: list[bpy.types.Object] = []
water_parts: list[bpy.types.Object] = []
foam_parts: list[bpy.types.Object] = []

porcelain_parts.append(profiled_superellipse(
	"outer_tapered_shell",
	[
		(3.03, 1.67, 0.54),
		(3.11, 1.78, 0.72),
		(3.24, 1.92, 1.18),
		(3.42, 2.08, 2.28),
		(3.53, 2.16, 2.64),
	],
	MATS["porcelain"],
	40,
	close_bottom=True,
))

porcelain_parts.append(profiled_superellipse(
	"thick_rounded_rim",
	[
		(3.51, 2.15, 2.60),
		(3.69, 2.37, 2.72),
		(3.75, 2.48, 2.91),
		(3.68, 2.41, 3.10),
		(3.51, 2.24, 3.22),
		(3.04, 1.74, 3.20),
		(2.90, 1.61, 3.04),
		(2.91, 1.62, 2.78),
	],
	MATS["porcelain"],
	40,
	close_profile=True,
))

interior_parts.append(profiled_superellipse(
	"deep_hollow_basin",
	[
		(2.91, 1.62, 2.82),
		(2.78, 1.49, 2.48),
		(2.49, 1.26, 1.62),
		(2.18, 1.02, 1.18),
	],
	MATS["interior"],
	40,
	close_bottom=True,
))

water_parts.append(superellipse_slab("bath_water_surface", 2.68, 1.38, 2.65, 2.72, MATS["water"], 40))


# Layered front and side molding, with genuine inset panels.
accent_parts.append(plaque_ring("front_outer_molding", (0.0, -2.205, 1.50), 5.18, 1.50, 0.22, 0.13, MATS["accent"]))
metal_parts.append(plaque_ring("front_gold_inlay", (0.0, -2.285, 1.50), 4.73, 1.13, 0.105, 0.075, MATS["gold"]))
interior_parts.append(plaque_fill("front_seafoam_inset", (0.0, -2.335, 1.50), 4.45, 0.86, 0.065, MATS["interior"]))

for side, x in (("left", -3.49), ("right", 3.49)):
	outward = -1.0 if x < 0.0 else 1.0
	accent_parts.append(plaque_ring(f"{side}_outer_molding", (x, 0.0, 1.48), 1.66, 1.18, 0.18, 0.12, MATS["accent"], "x"))
	metal_parts.append(plaque_ring(f"{side}_gold_inlay", (x + outward * 0.075, 0.0, 1.48), 1.30, 0.84, 0.085, 0.07, MATS["gold"], "x"))
	interior_parts.append(plaque_fill(f"{side}_seafoam_inset", (x + outward * 0.12, 0.0, 1.48), 1.08, 0.63, 0.05, MATS["interior"], "x"))

# A nine-rib medallion and two rivets complete the front panel hierarchy.
accent_parts.extend(scallop_shell("front_shell_medallion", (0.0, -2.39, 0.89), 1.18, 1.19, 0.14, MATS["accent_light"], 9))
metal_parts.append(cylinder("front_shell_pedestal", (0.0, -2.36, 0.90), 0.25, 0.18, MATS["gold"], 20, (math.pi * 0.5, 0.0, 0.0)))
for x in (-1.72, 1.72):
	metal_parts.append(ellipsoid(f"front_gold_rivet_{x:+.2f}", (x, -2.41, 1.50), (0.11, 0.07, 0.11), MATS["gold"], 12, 6))


# Four modeled paw feet: ankle, broad pad, three distinct toes, and collar.
for x in (-2.82, 2.82):
	for y in (-1.52, 1.52):
		front_sign = -1.0 if y < 0.0 else 1.0
		label = f"{('L' if x < 0.0 else 'R')}{('F' if y < 0.0 else 'B')}"
		metal_parts.append(ellipsoid(f"paw_{label}_ankle", (x, y, 0.42), (0.29, 0.33, 0.40), MATS["gold"], 10, 5))
		metal_parts.append(ellipsoid(f"paw_{label}_pad", (x, y + front_sign * 0.16, 0.22), (0.39, 0.49, 0.22), MATS["gold"], 10, 5))
		for toe_index, x_offset in enumerate((-0.22, 0.0, 0.22)):
			metal_parts.append(ellipsoid(
				f"paw_{label}_toe_{toe_index + 1}",
				(x + x_offset, y + front_sign * 0.43, 0.13),
				(0.18, 0.23, 0.13),
				MATS["gold"],
				8,
				4,
			))
		accent_parts.append(cylinder(f"paw_{label}_lavender_collar", (x, y, 0.65), 0.39, 0.17, MATS["accent"], 18))


# Smooth gold faucet and tall riser, each with molded mounting collars.
metal_parts.append(curve_tube(
	"bath_faucet_spout",
	[(0.0, 1.82, 3.05), (0.0, 1.82, 3.70), (0.0, 1.48, 3.92), (0.0, 1.05, 3.68), (0.0, 0.94, 3.42)],
	0.13,
	MATS["gold"],
	5,
	1,
))
metal_parts.append(cylinder("faucet_mount", (0.0, 1.82, 3.16), 0.27, 0.24, MATS["gold"], 24))
metal_parts.append(cylinder("faucet_nozzle", (0.0, 0.92, 3.37), 0.15, 0.24, MATS["gold"], 20, (math.pi * 0.5, 0.0, 0.0)))

metal_parts.append(curve_tube(
	"shower_riser",
	[(2.22, 1.87, 3.06), (2.22, 1.87, 5.85), (2.15, 1.86, 6.49), (1.57, 1.59, 6.86), (0.72, 0.92, 6.48)],
	0.14,
	MATS["gold"],
	5,
	1,
))
metal_parts.append(cylinder("riser_mount", (2.22, 1.87, 3.15), 0.28, 0.25, MATS["gold"], 24))
metal_parts.append(cylinder("riser_neck_collar", (0.67, 0.88, 6.42), 0.24, 0.22, MATS["gold"], 20, (math.radians(27.0), 0.0, 0.0)))

# Real seven-rib shell tap handles, oriented toward the room.
for index, x in enumerate((-1.30, 1.22)):
	metal_parts.append(cylinder(f"tap_{index + 1}_mount", (x, 1.83, 3.16), 0.23, 0.20, MATS["gold"], 20))
	accent_parts.extend(scallop_shell(
		f"tap_{index + 1}_shell",
		(x, 1.76, 3.22),
		0.76,
		0.72,
		0.08,
		MATS["accent_light"],
		7,
		"y",
		-1.0,
	))

shower_parts = shower_dome((0.55, 0.73, 6.05), Vector((0.0, -0.48, -0.877)))
shower_rib_parts: list[bpy.types.Object] = []
shower_nozzle_parts: list[bpy.types.Object] = []
for shower_part in shower_parts:
	if shower_part.name.startswith("TubAccent_ShowerShellDome"):
		accent_parts.append(shower_part)
	elif shower_part.name.startswith("TubMetal_ShowerFace"):
		metal_parts.append(shower_part)
	elif shower_part.name.startswith("TubAccent_ShowerRib"):
		shower_rib_parts.append(shower_part)
	elif shower_part.name.startswith("ShowerNozzleInset"):
		shower_nozzle_parts.append(shower_part)
	else:
		raise RuntimeError(f"Unclassified shower mesh: {shower_part.name}")


# Sparse, shallow terrazzo chips are genuine geometry on the top rim.
chip_groups: dict[str, list[bpy.types.Object]] = {"chip_rose": [], "chip_aqua": [], "chip_lilac": []}
chip_specs = [
	(-2.75, -1.91, 18.0), (-2.10, -1.97, -12.0), (-1.42, -2.01, 32.0), (-0.72, -2.04, -18.0),
	(0.08, -2.05, 25.0), (0.84, -2.03, -28.0), (1.58, -1.99, 15.0), (2.34, -1.94, -20.0),
	(-2.55, 1.94, -24.0), (-1.78, 2.00, 14.0), (-0.78, 2.04, -8.0), (0.72, 2.04, 18.0),
	(1.58, 1.99, -22.0), (2.48, 1.92, 10.0),
	(-3.38, -1.05, 22.0), (-3.47, 0.12, -16.0), (-3.35, 1.08, 30.0),
	(3.38, -1.00, -20.0), (3.47, 0.02, 17.0), (3.34, 1.04, -28.0),
]
chip_keys = ("chip_rose", "chip_aqua", "chip_lilac")
for index, (x, y, degrees) in enumerate(chip_specs):
	key = chip_keys[index % len(chip_keys)]
	size = (0.17, 0.11, 0.035) if index % 2 == 0 else (0.12, 0.16, 0.032)
	chip_groups[key].append(chip_prism(
		f"terrazzo_{key}_{index + 1:02d}",
		(x, y, 3.235),
		size,
		degrees,
		MATS[key],
	))


# Graphic water highlights and pearl bubbles echo the generated concept.
for index, (x, y, sx, sy) in enumerate((
	(-1.62, -0.42, 0.48, 0.25),
	(0.05, 0.34, 0.62, 0.31),
	(1.58, -0.18, 0.43, 0.22),
)):
	bpy.ops.mesh.primitive_torus_add(
		major_radius=sx,
		minor_radius=0.025,
		major_segments=16,
		minor_segments=4,
		location=(x, y, 2.745),
	)
	ripple = bpy.context.active_object
	ripple.name = f"TubWater_Ripple_{index + 1}"
	ripple.scale.y = sy / sx
	ripple.parent = ROOT_OBJ
	assign(ripple, MATS["water_light"])
	transform_apply(ripple)
	water_parts.append(ripple)

bubble_specs = [
	(-1.62, -0.40, 0.29), (-1.33, -0.25, 0.12), (-1.90, -0.17, 0.10),
	(0.12, 0.30, 0.18), (-0.20, 0.18, 0.10),
	(1.52, -0.13, 0.34), (1.88, 0.03, 0.13), (1.25, 0.16, 0.11),
]
for index, (x, y, radius) in enumerate(bubble_specs):
	foam_parts.append(ellipsoid(
		f"foam_bubble_{index + 1:02d}",
		(x, y, 2.71 + radius * 0.52),
		(radius, radius, radius * 0.72),
		MATS["foam"],
		10,
		5,
	))


# Join only same-role geometry. Standalone detail materials remain separate so
# terrazzo chips, water highlights, and nozzle perforations survive runtime.
join_role("TubPorcelain", porcelain_parts, MATS["porcelain"])
join_role("TubInterior", interior_parts, MATS["interior"])
join_role("TubAccent", accent_parts, MATS["accent"])
join_role("TubMetal", metal_parts, MATS["gold"])
join_role("TubWater", water_parts, MATS["water"])
join_role("TubFoam", foam_parts, MATS["foam"])
join_role("TubAccentHighlights", shower_rib_parts, MATS["accent_light"])
join_role("ShowerNozzleInsets", shower_nozzle_parts, MATS["gold_dark"])
for key, objects in chip_groups.items():
	join_role("Terrazzo" + key.removeprefix("chip_").title(), objects, MATS[key])


def triangle_count(root: bpy.types.Object) -> int:
	total = 0
	for obj in descendants(root):
		if obj.type == "MESH":
			obj.data.calc_loop_triangles()
			total += len(obj.data.loop_triangles)
	return total


def zero_area_triangle_count(root: bpy.types.Object, epsilon: float = 1e-10) -> int:
	count = 0
	for obj in descendants(root):
		if obj.type != "MESH":
			continue
		obj.data.calc_loop_triangles()
		for triangle in obj.data.loop_triangles:
			a = obj.data.vertices[triangle.vertices[0]].co
			b = obj.data.vertices[triangle.vertices[1]].co
			c = obj.data.vertices[triangle.vertices[2]].co
			if (b - a).cross(c - a).length_squared <= epsilon:
				count += 1
	return count


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


tris = triangle_count(ROOT_OBJ)
mesh_nodes = sum(1 for obj in descendants(ROOT_OBJ) if obj.type == "MESH")
zero_area = zero_area_triangle_count(ROOT_OBJ)
mins, maxs = bounds_for(ROOT_OBJ)
print("AUDIT bathroom_bathtub_v2 triangles", tris, "mesh_nodes", mesh_nodes, "zero_area", zero_area, "bounds", tuple(round(v, 3) for v in mins), tuple(round(v, 3) for v in maxs))
for audit_obj in ROOT_OBJ.children:
	if audit_obj.type == "MESH":
		audit_obj.data.calc_loop_triangles()
		print("AUDIT_ROLE", audit_obj.name, len(audit_obj.data.loop_triangles))
		audit_min_z = min((audit_obj.matrix_world @ Vector(corner)).z for corner in audit_obj.bound_box)
		if audit_min_z < -0.001:
			print("AUDIT_FLOOR", audit_obj.name, round(audit_min_z, 4))
if tris > 10000:
	raise RuntimeError(f"Bathtub exceeds 10k mobile triangle budget: {tris}")
if mesh_nodes > 16:
	raise RuntimeError(f"Bathtub exceeds 16-node draw-call budget: {mesh_nodes}")
if zero_area != 0:
	raise RuntimeError(f"Bathtub contains zero-area triangles: {zero_area}")
if abs(mins.z) > 0.025:
	raise RuntimeError(f"Bathtub feet must touch floor Z=0, got {mins.z}")


def export_glb() -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for obj in descendants(ROOT_OBJ):
		obj.hide_set(False)
		obj.hide_render = False
		obj.select_set(True)
	bpy.context.view_layer.objects.active = ROOT_OBJ
	bpy.ops.export_scene.gltf(
		filepath=str(GLB_OUT),
		export_format="GLB",
		use_selection=True,
		export_materials="EXPORT",
		export_animations=False,
		export_yup=True,
		export_apply=True,
	)
	bpy.ops.object.select_all(action="DESELECT")
	print("EXPORTED", GLB_OUT)


export_glb()


# ---------------------------------------------------------------------------
# Polished Eevee QA render. Lights/camera/backdrop are added only after export.
# ---------------------------------------------------------------------------

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1024
scene.render.resolution_y = 820
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.render.filepath = str(QA_OUT)
scene.render.use_file_extension = True

if scene.world is None:
	scene.world = bpy.data.worlds.new("QA_World")
scene.world.use_nodes = True
world_bg = scene.world.node_tree.nodes.get("Background")
world_bg.inputs["Color"].default_value = (0.045, 0.028, 0.065, 1.0)
world_bg.inputs["Strength"].default_value = 0.28

scene.view_settings.look = "AgX - Medium High Contrast"

floor_mat = make_material("QA_WarmBackdrop", (0.31, 0.20, 0.34, 1.0), 0.72)
bpy.ops.mesh.primitive_plane_add(size=30.0, location=(0.0, 0.0, -0.025))
floor = bpy.context.active_object
floor.name = "QA_BackdropFloor"
assign(floor, floor_mat)

# A broad back panel gives the asset a deliberate studio-card presentation.
bpy.ops.mesh.primitive_plane_add(size=26.0, location=(0.0, 4.8, 5.2), rotation=(math.pi * 0.5, 0.0, 0.0))
backdrop = bpy.context.active_object
backdrop.name = "QA_BackdropWall"
assign(backdrop, floor_mat)


def area_light(
	name: str,
	location: tuple[float, float, float],
	energy: float,
	color: tuple[float, float, float],
	size: float,
	target: tuple[float, float, float],
) -> bpy.types.Object:
	data = bpy.data.lights.new(name, "AREA")
	data.energy = energy
	data.color = color
	data.shape = "DISK"
	data.size = size
	obj = bpy.data.objects.new(name, data)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
	return obj


area_light("QA_Key", (-5.5, -7.5, 11.5), 1250.0, (1.0, 0.73, 0.54), 5.0, (0.0, 0.0, 2.8))
area_light("QA_Fill", (7.5, -3.0, 7.0), 900.0, (0.48, 0.72, 1.0), 4.0, (0.0, 0.0, 2.8))
area_light("QA_Rim", (-1.0, 5.0, 10.5), 1350.0, (0.72, 0.48, 1.0), 3.5, (0.0, 0.0, 3.4))
area_light("QA_FrontSoft", (0.0, -8.0, 4.0), 500.0, (1.0, 0.90, 0.77), 5.5, (0.0, 0.0, 2.5))

camera_data = bpy.data.cameras.new("QA_Camera")
camera_data.type = "ORTHO"
camera_data.ortho_scale = 9.15
camera = bpy.data.objects.new("QA_Camera", camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (9.6, -13.2, 8.0)
camera.rotation_euler = (Vector((0.0, 0.0, 3.40)) - camera.location).to_track_quat("-Z", "Y").to_euler()
scene.camera = camera

bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_OUT))
print("SAVED", SOURCE_OUT)
bpy.ops.render.render(write_still=True)
print("RENDERED", QA_OUT)
