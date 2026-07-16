#!/usr/bin/env python3
"""Build the imagegen-guided royal kitchen props as exact-size static GLBs.

The generated stove, sink, and counter are lightweight storybook meshes for
the Mobile renderer.  Blender X/Y/Z maps to Godot X/-Z/Y, so every appliance
faces Blender -Y and arrives facing the kitchen interior (+Z in Godot).

Usage:
  blender --background --python tools/build_kitchen_props.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_OUT = ROOT / "assets" / "castle"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_kitchen_props"
BLEND_OUT = SOURCE_OUT / "kitchen_props.blend"

for folder in (RUNTIME_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"wood": (0.77, 0.43, 0.20, 1.0),
	"counter": (0.96, 0.90, 0.79, 1.0),
	"cream": (0.96, 0.91, 0.80, 1.0),
	"pearl_blue": (0.56, 0.75, 0.86, 1.0),
	"aqua": (0.37, 0.78, 0.76, 1.0),
	"water": (0.31, 0.78, 0.83, 1.0),
	"lavender": (0.66, 0.57, 0.84, 1.0),
	"gold": (0.94, 0.65, 0.19, 1.0),
	"glass": (0.16, 0.13, 0.31, 1.0),
	"burner": (0.14, 0.12, 0.25, 1.0),
	"hot": (1.0, 0.30, 0.12, 1.0),
	"warm": (1.0, 0.62, 0.18, 1.0),
}


def material(name: str, color: tuple[float, float, float, float], metallic: float = 0.0) -> bpy.types.Material:
	mat = bpy.data.materials.new("MR_Kitchen_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.50 if metallic > 0.0 else 0.82
	bsdf.inputs["Metallic"].default_value = metallic
	return mat


MATS = {
	"wood": material("Wood", PALETTE["wood"]),
	"counter": material("Counter", PALETTE["counter"]),
	"cream": material("Cream", PALETTE["cream"]),
	"pearl_blue": material("PearlBlue", PALETTE["pearl_blue"]),
	"aqua": material("Aqua", PALETTE["aqua"]),
	"water": material("Water", PALETTE["water"]),
	"lavender": material("Lavender", PALETTE["lavender"]),
	"gold": material("Gold", PALETTE["gold"], 0.35),
	"glass": material("Glass", PALETTE["glass"]),
	"burner": material("Burner", PALETTE["burner"], 0.12),
	"hot": material("BurnerHot", PALETTE["hot"]),
	"warm": material("BurnerWarm", PALETTE["warm"]),
}


def root_object(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.data.materials.append(mat)
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def soften(obj: bpy.types.Object) -> bpy.types.Object:
	if obj.type == "MESH":
		for polygon in obj.data.polygons:
			polygon.use_smooth = True
	return obj


def bevel(obj: bpy.types.Object, width: float, segments: int = 1) -> bpy.types.Object:
	modifier = obj.modifiers.new("storybook_rounding", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	modifier.harden_normals = True
	apply_modifier(obj, modifier)
	return soften(obj)


def cube(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
	obj = bpy.context.active_object
	obj.name = name
	# primitive_cube_add(size=1) already creates a one-unit-wide cube.
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	return assign(obj, mat)


def rounded_box(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	radius: float = 0.12,
) -> bpy.types.Object:
	obj = cube(name, location, size, mat, parent)
	return bevel(obj, min(radius, min(size) * 0.22), 1)


def rounded_box_with_hole(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	hole_center: tuple[float, float],
	hole_size: tuple[float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	obj = cube(name, location, size, mat, parent)
	cutter = cube(
		name + "_cutter",
		(hole_center[0], hole_center[1], location[2]),
		(hole_size[0], hole_size[1], size[2] * 3.0),
		mat,
		parent,
	)
	modifier = obj.modifiers.new("real_sink_cutout", "BOOLEAN")
	modifier.operation = "DIFFERENCE"
	modifier.solver = "EXACT"
	modifier.object = cutter
	apply_modifier(obj, modifier)
	bpy.data.objects.remove(cutter, do_unlink=True)
	return bevel(obj, 0.11, 1)


def cylinder(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	vertices: int = 12,
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
	return bevel(obj, min(radius * 0.12, depth * 0.10), 1)


def torus(
	name: str,
	location: tuple[float, float, float],
	major_radius: float,
	minor_radius: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(
		major_radius=major_radius,
		minor_radius=minor_radius,
		major_segments=10,
		minor_segments=4,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return soften(obj)


def sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=1.0, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return soften(obj)


def tube_curve(
	name: str,
	points: list[tuple[float, float, float]],
	radius: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	curve_data = bpy.data.curves.new(name + "_curve", "CURVE")
	curve_data.dimensions = "3D"
	curve_data.resolution_u = 1
	curve_data.bevel_depth = radius
	curve_data.bevel_resolution = 0
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
	return soften(bpy.context.active_object)


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
	items = [root]
	for child in root.children:
		items.extend(descendants(child))
	return items


def join_role(
	root: bpy.types.Object,
	name: str,
	objects: list[bpy.types.Object],
	mat: bpy.types.Material,
) -> bpy.types.Object:
	if not objects:
		raise ValueError(f"No meshes supplied for {name}")
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


def u_handle(
	name: str,
	center: tuple[float, float, float],
	width: float,
	height: float,
	horizontal: bool,
	parent: bpy.types.Object,
) -> list[bpy.types.Object]:
	x, y, z = center
	parts: list[bpy.types.Object] = []
	if horizontal:
		parts.append(rounded_box(name + "_bar", (x, y - 0.13, z), (width, 0.15, 0.15), MATS["gold"], parent, 0.065))
		for sign in (-1.0, 1.0):
			parts.append(rounded_box(name + "_mount", (x + sign * width * 0.5, y - 0.02, z), (0.17, 0.26, 0.17), MATS["gold"], parent, 0.065))
	else:
		parts.append(rounded_box(name + "_bar", (x, y - 0.13, z), (0.15, 0.15, height), MATS["gold"], parent, 0.065))
		for sign in (-1.0, 1.0):
			parts.append(rounded_box(name + "_mount", (x, y - 0.02, z + sign * height * 0.5), (0.17, 0.26, 0.17), MATS["gold"], parent, 0.065))
	return parts


def build_counter() -> bpy.types.Object:
	root = root_object("KitchenCounter")
	wood: list[bpy.types.Object] = []
	metal: list[bpy.types.Object] = []

	wood.append(rounded_box("cabinet_body", (0.0, 0.0, 1.68), (9.8, 2.5, 3.05), MATS["wood"], root, 0.24))
	wood.append(rounded_box("toe_kick", (0.0, -0.02, 0.22), (10.0, 2.68, 0.42), MATS["wood"], root, 0.16))
	# Raised geometry makes the panel borders readable without extra textures.
	for index, x in enumerate((-3.18, 0.0, 3.18)):
		wood.append(rounded_box(f"door_{index}", (x, -1.31, 1.24), (2.84, 0.15, 1.52), MATS["wood"], root, 0.12))
		metal.extend(u_handle(f"door_handle_{index}", (x + 0.90, -1.40, 1.24), 0.0, 0.62, False, root))
	for index, x in enumerate((-2.43, 2.43)):
		wood.append(rounded_box(f"drawer_{index}", (x, -1.32, 2.61), (4.52, 0.16, 0.66), MATS["wood"], root, 0.11))
		metal.extend(u_handle(f"drawer_handle_{index}", (x, -1.41, 2.61), 0.94, 0.0, True, root))

	top = rounded_box_with_hole(
		"countertop_with_sink_cutout",
		(0.0, 0.0, 3.40),
		(10.4, 3.0, 0.50),
		(1.60, -0.15),
		(2.34, 1.70),
		MATS["counter"],
		root,
	)
	join_role(root, "CounterWood", wood, MATS["wood"])
	join_role(root, "CounterTop", [top], MATS["counter"])
	join_role(root, "CounterMetal", metal, MATS["gold"])
	return root


def build_sink() -> bpy.types.Object:
	root = root_object("KitchenSink")
	porcelain: list[bpy.types.Object] = []
	basin: list[bpy.types.Object] = []
	metal: list[bpy.types.Object] = []
	water: list[bpy.types.Object] = []

	# Four rim bars frame a genuinely recessed bowl that fits the counter cutout.
	porcelain.append(rounded_box("rim_front", (0.0, -0.98, 0.08), (2.80, 0.30, 0.24), MATS["cream"], root, 0.11))
	porcelain.append(rounded_box("rim_back", (0.0, 0.98, 0.08), (2.80, 0.30, 0.24), MATS["cream"], root, 0.11))
	porcelain.append(rounded_box("rim_left", (-1.25, 0.0, 0.08), (0.30, 1.72, 0.24), MATS["cream"], root, 0.11))
	porcelain.append(rounded_box("rim_right", (1.25, 0.0, 0.08), (0.30, 1.72, 0.24), MATS["cream"], root, 0.11))
	basin.append(rounded_box("bowl_bottom", (0.0, 0.0, -0.51), (2.18, 1.46, 0.16), MATS["aqua"], root, 0.07))
	basin.append(rounded_box("bowl_front", (0.0, -0.75, -0.25), (2.18, 0.14, 0.52), MATS["aqua"], root, 0.055))
	basin.append(rounded_box("bowl_back", (0.0, 0.75, -0.25), (2.18, 0.14, 0.52), MATS["aqua"], root, 0.055))
	basin.append(rounded_box("bowl_left", (-1.02, 0.0, -0.25), (0.14, 1.38, 0.52), MATS["aqua"], root, 0.055))
	basin.append(rounded_box("bowl_right", (1.02, 0.0, -0.25), (0.14, 1.38, 0.52), MATS["aqua"], root, 0.055))
	water.append(rounded_box("water_surface", (0.0, -0.02, -0.38), (1.92, 1.20, 0.055), MATS["water"], root, 0.025))

	metal.append(tube_curve("arched_faucet", [(0.0, 0.90, 0.16), (0.0, 0.90, 1.16), (0.0, 0.60, 1.63), (0.0, 0.05, 1.63), (0.0, -0.10, 1.28)], 0.105, MATS["gold"], root))
	metal.append(cylinder("faucet_base", (0.0, 0.90, 0.16), 0.22, 0.22, MATS["gold"], root, vertices=12))
	metal.append(cylinder("faucet_nozzle", (0.0, -0.10, 1.21), 0.135, 0.26, MATS["gold"], root, vertices=12))
	for index, x in enumerate((-0.82, 0.82)):
		metal.append(cylinder(f"handle_base_{index}", (x, 0.91, 0.18), 0.18, 0.18, MATS["gold"], root, vertices=12))
		porcelain.append(sphere(f"shell_handle_{index}", (x, 0.91, 0.43), (0.31, 0.17, 0.33), MATS["cream"], root))
		for ridge in (-0.10, 0.0, 0.10):
			porcelain.append(rounded_box(f"shell_ridge_{index}", (x + ridge, 0.73, 0.43), (0.055, 0.045, 0.42), MATS["cream"], root, 0.02))
	metal.append(torus("drain", (0.0, -0.02, -0.34), 0.16, 0.045, MATS["gold"], root))

	join_role(root, "SinkPorcelain", porcelain, MATS["cream"])
	join_role(root, "SinkBasin", basin, MATS["aqua"])
	join_role(root, "SinkMetal", metal, MATS["gold"])
	join_role(root, "SinkWater", water, MATS["water"])
	return root


def build_stove() -> bpy.types.Object:
	root = root_object("KitchenStove")
	body: list[bpy.types.Object] = []
	cream: list[bpy.types.Object] = []
	trim: list[bpy.types.Object] = []
	metal: list[bpy.types.Object] = []
	glass: list[bpy.types.Object] = []
	dark: list[bpy.types.Object] = []
	hot: list[bpy.types.Object] = []
	warm: list[bpy.types.Object] = []

	for x in (-1.45, 1.45):
		for y in (-1.05, 1.05):
			body.append(rounded_box("short_foot", (x, y, 0.14), (0.48, 0.48, 0.28), MATS["pearl_blue"], root, 0.10))
	body.append(rounded_box("enamel_body", (0.0, 0.0, 1.88), (3.62, 2.82, 3.48), MATS["pearl_blue"], root, 0.27))
	cream.append(rounded_box("cream_control_panel", (0.0, -1.43, 3.10), (3.18, 0.16, 0.62), MATS["cream"], root, 0.10))
	cream.append(rounded_box("oven_door", (0.0, -1.44, 1.50), (3.06, 0.18, 2.06), MATS["cream"], root, 0.18))
	trim.append(rounded_box("cooktop", (0.0, 0.0, 3.82), (3.80, 3.00, 0.32), MATS["lavender"], root, 0.14))
	trim.append(rounded_box("bottom_trim", (0.0, -1.44, 0.44), (3.52, 0.16, 0.28), MATS["lavender"], root, 0.08))
	glass.append(rounded_box("oven_window", (0.0, -1.56, 1.54), (2.48, 0.10, 1.28), MATS["glass"], root, 0.16))
	metal.extend(u_handle("oven_handle", (0.0, -1.62, 2.54), 2.30, 0.0, True, root))
	for index, x in enumerate((-0.92, 0.0, 0.92)):
		metal.append(cylinder(f"control_knob_{index}", (x, -1.57, 3.10), 0.25, 0.24, MATS["gold"], root, rotation=(math.pi * 0.5, 0.0, 0.0), vertices=12))
		metal.append(rounded_box(f"knob_grip_{index}", (x, -1.72, 3.10), (0.13, 0.10, 0.34), MATS["gold"], root, 0.04))

	# Two active rings line up with the existing soup pot and kitchen staging.
	for name, x, y, role in (
		("hot", -0.80, 0.00, hot),
		("warm", 0.90, 0.00, warm),
		("dark_left", -0.82, 0.78, dark),
		("dark_right", 0.88, 0.78, dark),
	):
		role.append(torus("burner_ring_" + name, (x, y, 4.02), 0.43, 0.085, MATS["hot"] if role is hot else MATS["warm"] if role is warm else MATS["burner"], root))
		dark.append(cylinder("burner_plate_" + name, (x, y, 3.99), 0.37, 0.10, MATS["burner"], root, vertices=12))

	join_role(root, "StoveBody", body, MATS["pearl_blue"])
	join_role(root, "StoveCream", cream, MATS["cream"])
	join_role(root, "StoveTrim", trim, MATS["lavender"])
	join_role(root, "StoveMetal", metal, MATS["gold"])
	join_role(root, "StoveGlass", glass, MATS["glass"])
	join_role(root, "StoveBurnerHot", hot, MATS["hot"])
	join_role(root, "StoveBurnerWarm", warm, MATS["warm"])
	join_role(root, "StoveBurnerDark", dark, MATS["burner"])
	return root


ASSETS = {
	"kitchen_counter": (build_counter(), RUNTIME_OUT / "kitchen_counter.glb"),
	"kitchen_sink": (build_sink(), RUNTIME_OUT / "kitchen_sink.glb"),
	"kitchen_stove": (build_stove(), RUNTIME_OUT / "kitchen_stove.glb"),
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
		export_animations=False,
		export_yup=True,
	)
	bpy.ops.object.select_all(action="DESELECT")
	print("EXPORTED", path)


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


def triangle_count(root: bpy.types.Object) -> int:
	total = 0
	for obj in descendants(root):
		if obj.type != "MESH":
			continue
		obj.data.calc_loop_triangles()
		total += len(obj.data.loop_triangles)
	return total


for asset_name, (asset_root, output) in ASSETS.items():
	export_root(asset_root, output)
	mins, maxs = bounds_for(asset_root)
	print("AUDIT", asset_name, "triangles", triangle_count(asset_root), "bounds", tuple(round(v, 3) for v in mins), tuple(round(v, 3) for v in maxs))


scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "paint.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "WORLD"
scene.display.shading.show_object_outline = True
scene.display.shading.object_outline_color = (0.10, 0.08, 0.22)
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


def render_root(name: str, root: bpy.types.Object) -> None:
	for other_root, _ in ASSETS.values():
		for obj in descendants(other_root):
			obj.hide_render = other_root != root
	mins, maxs = bounds_for(root)
	center = (mins + maxs) * 0.5
	span = max(maxs.x - mins.x, maxs.y - mins.y, maxs.z - mins.z)
	view = Vector((1.25, -1.55, 0.92)).normalized()
	camera.location = center + view * max(span * 3.0, 8.0)
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	camera.data.ortho_scale = span * 1.62
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
