#!/usr/bin/env python3
"""Build the first Blender-native replacements for score-2 world art.

The generated models deliberately avoid book characters and child-owned toys.
They use simple Mobile-friendly geometry and embedded matte palette materials.

Usage:
  blender --background --python tools/build_low_score_batch_01.py
"""

from __future__ import annotations

import math
import os
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
PROP_OUT = ROOT / "assets" / "props" / "gen2"
VEHICLE_OUT = ROOT / "assets" / "vehicles"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_low_score_batch_01"
BLEND_OUT = SOURCE_OUT / "low_score_batch_01.blend"

for folder in (PROP_OUT, VEHICLE_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"navy": (0.10, 0.09, 0.24, 1.0),
	"indigo": (0.20, 0.18, 0.42, 1.0),
	"aqua": (0.28, 0.78, 0.82, 1.0),
	"mint": (0.43, 0.86, 0.67, 1.0),
	"seafoam": (0.67, 0.91, 0.78, 1.0),
	"lavender": (0.69, 0.56, 0.88, 1.0),
	"violet": (0.43, 0.30, 0.68, 1.0),
	"coral": (0.96, 0.43, 0.48, 1.0),
	"rose": (0.93, 0.56, 0.72, 1.0),
	"apricot": (0.98, 0.69, 0.42, 1.0),
	"gold": (0.98, 0.78, 0.32, 1.0),
	"cream": (0.97, 0.92, 0.80, 1.0),
	"window": (0.28, 0.66, 0.75, 1.0),
}


def make_material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.82
	bsdf.inputs["Metallic"].default_value = 0.0
	return mat


MATS = {name: make_material("MR_" + name, color) for name, color in PALETTE.items()}


def root_object(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def smooth(obj: bpy.types.Object) -> bpy.types.Object:
	if obj.type == "MESH":
		for poly in obj.data.polygons:
			poly.use_smooth = True
	return obj


def assign(obj: bpy.types.Object, material: bpy.types.Material) -> bpy.types.Object:
	if obj.type == "MESH":
		obj.data.materials.append(material)
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
	modifier = obj.modifiers.new("soft_edges", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	apply_modifier(obj, modifier)
	return smooth(obj)


def decimate(obj: bpy.types.Object, ratio: float) -> bpy.types.Object:
	modifier = obj.modifiers.new("mobile_decimate", "DECIMATE")
	modifier.ratio = ratio
	modifier.use_collapse_triangulate = True
	apply_modifier(obj, modifier)
	return smooth(obj)


def uv_sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	material: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 20,
	rings: int = 12,
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
	obj.parent = parent
	assign(obj, material)
	return smooth(obj)


def ico_sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	material: bpy.types.Material,
	parent: bpy.types.Object,
	subdivisions: int = 2,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1.0, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, material)
	return smooth(obj)


def rounded_box(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	material: bpy.types.Material,
	parent: bpy.types.Object,
	radius: float = 0.18,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = tuple(v * 0.5 for v in size)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, material)
	return bevel(obj, min(radius, min(size) * 0.22), 3)


def cone_between(
	name: str,
	start: Vector,
	end: Vector,
	radius_start: float,
	radius_end: float,
	material: bpy.types.Material,
	parent: bpy.types.Object,
	vertices: int = 12,
) -> bpy.types.Object:
	direction = end - start
	length = direction.length
	midpoint = (start + end) * 0.5
	bpy.ops.mesh.primitive_cone_add(
		vertices=vertices,
		radius1=radius_start,
		radius2=radius_end,
		depth=length,
		location=midpoint,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.rotation_mode = "QUATERNION"
	obj.rotation_quaternion = Vector((0.0, 0.0, 1.0)).rotation_difference(direction.normalized())
	obj.parent = parent
	assign(obj, material)
	return smooth(obj)


def cylinder(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	material: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	vertices: int = 20,
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
	assign(obj, material)
	return bevel(obj, min(radius * 0.15, depth * 0.12), 2)


def polygon_prism(
	name: str,
	points: list[tuple[float, float]],
	z: float,
	material: bpy.types.Material,
	parent: bpy.types.Object,
	thickness: float = 0.07,
	bevel_width: float = 0.05,
) -> bpy.types.Object:
	verts = [(x, y, z) for x, y in points]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], [list(range(len(verts)))])
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	assign(obj, material)
	solid = obj.modifiers.new("wing_thickness", "SOLIDIFY")
	solid.thickness = thickness
	solid.offset = 0.0
	apply_modifier(obj, solid)
	return bevel(obj, bevel_width, 2)


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
	items = [root]
	for child in root.children:
		items.extend(descendants(child))
	return items


def join_meshes(root: bpy.types.Object, name: str) -> bpy.types.Object:
	meshes = [obj for obj in descendants(root) if obj.type == "MESH"]
	return join_objects(meshes, root, name)


def join_direct_meshes(parent: bpy.types.Object, name: str) -> bpy.types.Object:
	meshes = [obj for obj in parent.children if obj.type == "MESH"]
	return join_objects(meshes, parent, name)


def join_objects(meshes: list[bpy.types.Object], parent: bpy.types.Object, name: str) -> bpy.types.Object:
	bpy.ops.object.select_all(action="DESELECT")
	for obj in meshes:
		obj.select_set(True)
	bpy.context.view_layer.objects.active = meshes[0]
	bpy.ops.object.join()
	joined = bpy.context.active_object
	joined.name = name
	joined.parent = parent
	joined.select_set(False)
	return joined


def build_anemone() -> bpy.types.Object:
	root = root_object("anemone_story")
	uv_sphere("base", (0.0, 0.0, 0.34), (1.05, 1.05, 0.36), MATS["aqua"], root)
	uv_sphere("inner_crown", (0.0, 0.0, 0.58), (0.72, 0.72, 0.30), MATS["mint"], root)
	colors = [MATS["coral"], MATS["lavender"], MATS["seafoam"], MATS["rose"]]
	for index in range(10):
		a = index / 10.0 * math.tau
		out = Vector((math.cos(a), math.sin(a), 0.0))
		tangent = Vector((-math.sin(a), math.cos(a), 0.0))
		phase = -0.10 if index % 2 else 0.12
		points = [
			Vector((0.0, 0.0, 0.55)) + out * 0.30,
			Vector((0.0, 0.0, 0.90)) + out * 0.55 + tangent * phase,
			Vector((0.0, 0.0, 1.42)) + out * 0.82 - tangent * phase,
			Vector((0.0, 0.0, 1.68 + 0.10 * (index % 3))) + out * 1.05,
		]
		for segment in range(3):
			cone_between(
				f"tentacle_{index:02d}_{segment}",
				points[segment],
				points[segment + 1],
				0.18 - segment * 0.04,
				0.14 - segment * 0.045,
				colors[index % len(colors)] if segment < 2 else MATS["cream"],
				root,
		)
	joined = join_meshes(root, "anemone_story_mesh")
	decimate(joined, 0.48)
	return root


def build_urchin() -> bpy.types.Object:
	root = root_object("urchin_story")
	center = Vector((0.0, 0.0, 0.88))
	ico_sphere("core", tuple(center), (0.92, 0.92, 0.78), MATS["violet"], root, subdivisions=3)
	ico_sphere("core_band", (0.0, 0.0, 0.95), (0.74, 0.74, 0.64), MATS["aqua"], root, subdivisions=2)
	spine_mats = [MATS["coral"], MATS["rose"], MATS["seafoam"], MATS["lavender"]]
	golden = math.pi * (3.0 - math.sqrt(5.0))
	for index in range(28):
		z = -0.10 + 1.10 * (index / 27.0)
		r = math.sqrt(max(0.0, 1.0 - min(z, 1.0) ** 2))
		a = index * golden
		direction = Vector((math.cos(a) * r, math.sin(a) * r, z)).normalized()
		start = center + direction * 0.72
		end = center + direction * (1.38 + 0.12 * (index % 3))
		if end.z < 0.08:
			end.z = 0.08
		cone_between(
			f"spine_{index:02d}",
			start,
			end,
			0.13,
			0.025,
			spine_mats[index % len(spine_mats)],
			root,
			vertices=10,
		)
	joined = join_meshes(root, "urchin_story_mesh")
	decimate(joined, 0.58)
	return root


def mirrored(points: list[tuple[float, float]], sign: float) -> list[tuple[float, float]]:
	return [(x * sign, y) for x, y in points]


def build_butterfly() -> bpy.types.Object:
	root = root_object("butterfly_story")
	uv_sphere("body", (0.0, 0.0, 0.0), (0.20, 0.72, 0.20), MATS["navy"], root, segments=16, rings=10)
	uv_sphere("head", (0.0, -0.72, 0.02), (0.27, 0.27, 0.25), MATS["indigo"], root, segments=16, rings=10)
	uv_sphere("tail_mark", (0.0, 0.46, 0.03), (0.14, 0.23, 0.15), MATS["gold"], root, segments=12, rings=8)
	wing_pivots = []
	for sign, side in ((1.0, "L"), (-1.0, "R")):
		pivot = bpy.data.objects.new("wing_" + side, None)
		pivot.location = (0.10 * sign, -0.03, 0.0)
		bpy.context.collection.objects.link(pivot)
		pivot.parent = root
		wing_pivots.append((pivot, side))
		fore = [(0.0, -0.08), (0.55, -0.84), (1.42, -0.96), (1.92, -0.45), (1.74, 0.18), (0.72, 0.40)]
		hind = [(0.0, 0.03), (0.58, 0.22), (1.47, 0.38), (1.55, 1.05), (0.92, 1.32), (0.24, 0.58)]
		polygon_prism("forewing_" + side, mirrored(fore, sign), 0.0, MATS["aqua"], pivot, 0.075, 0.055)
		polygon_prism("hindwing_" + side, mirrored(hind, sign), -0.01, MATS["lavender"], pivot, 0.075, 0.055)
		fore_mark = [(0.22, -0.12), (0.62, -0.60), (1.22, -0.66), (1.48, -0.38), (1.24, -0.04), (0.66, 0.16)]
		hind_mark = [(0.20, 0.16), (0.64, 0.34), (1.14, 0.48), (1.12, 0.86), (0.76, 0.98), (0.34, 0.50)]
		polygon_prism("fore_mark_" + side, mirrored(fore_mark, sign), 0.065, MATS["coral"], pivot, 0.025, 0.025)
		polygon_prism("hind_mark_" + side, mirrored(hind_mark, sign), 0.055, MATS["gold"], pivot, 0.025, 0.025)
		pivot.rotation_mode = "XYZ"
		for frame, degrees in ((1, 12.0), (7, -42.0), (13, 12.0)):
			pivot.rotation_euler[1] = math.radians(degrees * sign)
			pivot.keyframe_insert(data_path="rotation_euler", frame=frame, index=1)
	for sign, side in ((1.0, "L"), (-1.0, "R")):
		p0 = Vector((0.09 * sign, -0.88, 0.08))
		p1 = Vector((0.20 * sign, -1.13, 0.12))
		p2 = Vector((0.40 * sign, -1.30, 0.16))
		cone_between("antenna_base_" + side, p0, p1, 0.025, 0.018, MATS["navy"], root, vertices=8)
		cone_between("antenna_tip_" + side, p1, p2, 0.018, 0.010, MATS["navy"], root, vertices=8)
	join_direct_meshes(root, "butterfly_body_mesh")
	for pivot, side in wing_pivots:
		join_direct_meshes(pivot, "wing_" + side + "_mesh")
	bpy.context.scene.frame_start = 1
	bpy.context.scene.frame_end = 13
	bpy.context.scene.render.fps = 24
	return root


def build_giant_fish() -> bpy.types.Object:
	root = root_object("giant_fish_story")
	# A distant blue whale: broad body, paired pectoral fins, one dorsal fin,
	# and horizontal tail flukes. Front points toward Blender -Y so Godot sees +Z.
	uv_sphere("body", (0.0, 0.0, 1.72), (1.62, 4.15, 1.48), MATS["aqua"], root, segments=24, rings=14)
	uv_sphere("back_patch", (0.0, 0.30, 2.30), (1.64, 3.90, 1.03), MATS["indigo"], root, segments=24, rings=14)
	uv_sphere("belly_patch", (0.0, -0.38, 1.20), (1.55, 3.76, 0.82), MATS["seafoam"], root, segments=24, rings=14)
	for sign, side in ((1.0, "L"), (-1.0, "R")):
		# Pectoral fins are paired and sweep backward from the lower shoulder.
		fin_points = [
			(1.10 * sign, -1.25),
			(1.70 * sign, -0.72),
			(2.58 * sign, 1.18),
			(1.66 * sign, 0.74),
		]
		polygon_prism("pectoral_" + side, fin_points, 0.96, MATS["violet"], root, 0.16, 0.09)
		uv_sphere(
			"eye_white_" + side,
			(1.12 * sign, -2.80, 2.02),
			(0.13, 0.25, 0.25),
			MATS["cream"],
			root,
			segments=12,
			rings=8,
		)
		uv_sphere(
			"eye_" + side,
			(1.23 * sign, -2.88, 2.02),
			(0.08, 0.13, 0.14),
			MATS["navy"],
			root,
			segments=10,
			rings=6,
		)
	# The dorsal fin is a thin vertical triangular prism on the rear back.
	dorsal = polygon_prism(
		"dorsal_fin",
		[(0.0, -0.72), (-0.86, 0.0), (0.0, 0.98)],
		0.0,
		MATS["indigo"],
		root,
		0.16,
		0.08,
	)
	dorsal.rotation_euler[1] = math.pi * 0.5
	dorsal.location = (0.0, 1.18, 3.03)
	# A single animated pivot keeps both horizontal flukes anatomically linked.
	tail = bpy.data.objects.new("tail_pivot", None)
	tail.location = (0.0, 3.55, 1.77)
	bpy.context.collection.objects.link(tail)
	tail.parent = root
	cone_between("tail_stock", Vector((0.0, -0.15, 0.0)), Vector((0.0, 1.30, 0.0)), 0.62, 0.30, MATS["indigo"], tail, vertices=16)
	for sign, side in ((1.0, "L"), (-1.0, "R")):
		fluke = [
			(0.0, 1.08),
			(0.68 * sign, 1.02),
			(2.10 * sign, 1.54),
			(2.42 * sign, 2.15),
			(1.38 * sign, 2.34),
			(0.26 * sign, 1.88),
		]
		polygon_prism("fluke_" + side, fluke, 0.0, MATS["indigo"], tail, 0.18, 0.10)
	tail.rotation_mode = "XYZ"
	for frame, degrees in ((1, 10.0), (9, -10.0), (17, 10.0)):
		tail.rotation_euler[2] = math.radians(degrees)
		tail.keyframe_insert(data_path="rotation_euler", frame=frame, index=2)
	join_direct_meshes(root, "giant_fish_body_mesh")
	join_direct_meshes(tail, "giant_fish_tail_mesh")
	bpy.context.scene.frame_start = 1
	bpy.context.scene.frame_end = 17
	bpy.context.scene.render.fps = 24
	return root


def build_monstertruck() -> bpy.types.Object:
	root = root_object("monstertruck_story")
	# Front points toward Blender -Y, which becomes Godot +Z like the legacy truck.
	rounded_box("chassis", (0.0, 0.0, 1.15), (3.35, 5.10, 0.72), MATS["indigo"], root, 0.24)
	rounded_box("lower_body", (0.0, -0.15, 1.72), (3.10, 4.45, 0.90), MATS["aqua"], root, 0.28)
	rounded_box("hood", (0.0, -1.52, 2.25), (2.90, 1.60, 0.78), MATS["coral"], root, 0.24)
	rounded_box("cab", (0.0, 0.55, 2.64), (2.72, 2.16, 1.65), MATS["cream"], root, 0.30)
	rounded_box("roof", (0.0, 0.60, 3.55), (2.92, 2.30, 0.30), MATS["lavender"], root, 0.14)
	rounded_box("windshield", (0.0, -0.55, 2.88), (2.35, 0.14, 0.82), MATS["window"], root, 0.08)
	for sign in (-1.0, 1.0):
		rounded_box(f"side_window_{sign:+.0f}", (1.40 * sign, 0.50, 2.86), (0.12, 1.44, 0.76), MATS["window"], root, 0.055)
		rounded_box(f"door_panel_{sign:+.0f}", (1.47 * sign, 0.58, 2.03), (0.10, 1.72, 0.72), MATS["rose"], root, 0.045)
	for axle_y in (-1.72, 1.62):
		for sign in (-1.0, 1.0):
			cylinder(
				f"tire_{axle_y:+.0f}_{sign:+.0f}",
				(1.78 * sign, axle_y, 1.12),
				1.06,
				0.62,
				MATS["navy"],
				root,
				rotation=(0.0, math.pi * 0.5, 0.0),
				vertices=24,
			)
			cylinder(
				f"hub_{axle_y:+.0f}_{sign:+.0f}",
				(2.10 * sign, axle_y, 1.12),
				0.48,
				0.14,
				MATS["gold"],
				root,
				rotation=(0.0, math.pi * 0.5, 0.0),
				vertices=20,
			)
	rounded_box("front_bumper", (0.0, -2.70, 1.30), (3.25, 0.34, 0.42), MATS["cream"], root, 0.12)
	rounded_box("rear_bumper", (0.0, 2.63, 1.30), (3.05, 0.30, 0.38), MATS["cream"], root, 0.10)
	for sign in (-1.0, 1.0):
		uv_sphere(f"headlight_{sign:+.0f}", (0.78 * sign, -2.35, 2.30), (0.28, 0.12, 0.24), MATS["gold"], root, segments=14, rings=8)
	for stripe_y, material in ((-0.95, MATS["gold"]), (-0.35, MATS["lavender"]), (0.25, MATS["mint"])):
		rounded_box("side_band", (0.0, stripe_y, 1.82), (3.18, 0.22, 0.26), material, root, 0.08)
	join_meshes(root, "monstertruck_story_mesh")
	return root


ASSETS = {
	"anemone_story": (build_anemone(), PROP_OUT / "anemone_story.glb"),
	"urchin_story": (build_urchin(), PROP_OUT / "urchin_story.glb"),
	"butterfly_story": (build_butterfly(), PROP_OUT / "butterfly_story.glb"),
	"giant_fish_story": (build_giant_fish(), PROP_OUT / "giant_fish_story.glb"),
	"monstertruck_story": (build_monstertruck(), VEHICLE_OUT / "monstertruck_story.glb"),
}


def export_root(root: bpy.types.Object, path: Path) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for obj in descendants(root):
		obj.hide_set(False)
		obj.hide_render = False
		obj.select_set(True)
	bpy.context.view_layer.objects.active = root
	bpy.ops.export_scene.gltf(
		filepath=str(path),
		export_format="GLB",
		use_selection=True,
		export_materials="EXPORT",
		export_animations=True,
		export_frame_range=True,
		export_image_format="AUTO",
	)
	bpy.ops.object.select_all(action="DESELECT")
	print("EXPORTED", path)


for asset_root, output in ASSETS.values():
	export_root(asset_root, output)


scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "paint.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "WORLD"
scene.display.shading.show_object_outline = True
scene.render.resolution_x = 900
scene.render.resolution_y = 700
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = True

camera_data = bpy.data.cameras.new("qa_camera")
camera_data.type = "ORTHO"
camera = bpy.data.objects.new("qa_camera", camera_data)
bpy.context.collection.objects.link(camera)
scene.camera = camera


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


def render_root(name: str, root: bpy.types.Object) -> None:
	for other_root, _ in ASSETS.values():
		for obj in descendants(other_root):
			obj.hide_render = other_root != root
	scene.frame_set(1)
	mins, maxs = bounds_for(root)
	center = (mins + maxs) * 0.5
	span = max(maxs.x - mins.x, maxs.y - mins.y, maxs.z - mins.z)
	view = Vector((1.25, -1.55, 0.95)).normalized()
	camera.location = center + view * max(span * 3.0, 8.0)
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	camera.data.ortho_scale = span * 1.48
	scene.render.filepath = str(QA_OUT / f"{name}.png")
	bpy.ops.render.render(write_still=True)
	print("RENDERED", scene.render.filepath)


for asset_name, (asset_root, _) in ASSETS.items():
	render_root(asset_name, asset_root)

for root, _ in ASSETS.values():
	for obj in descendants(root):
		obj.hide_render = False

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
print("SAVED", BLEND_OUT)
