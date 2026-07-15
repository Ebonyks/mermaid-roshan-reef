#!/usr/bin/env python3
"""Build and render the low-score picture-game replacement family.

The source scene contains reusable 3D models. Runtime output is transparent
orthographic PNG art because the picture games consume touch-sized TextureRects.
Protected book art, characters, watering can, carrot, friendship flower, and
child-owned toys are deliberately outside this build.

Usage:
  blender --background --python tools/build_low_score_batch_02.py
"""

from __future__ import annotations

import math
import shutil
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_OUT = ROOT / "assets" / "mg"
SOURCE_OUT = ROOT / "assets_src" / "blender"
BLEND_OUT = SOURCE_OUT / "low_score_batch_02.blend"

RUNTIME_OUT.mkdir(parents=True, exist_ok=True)
SOURCE_OUT.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"navy": (0.09, 0.08, 0.22, 1.0),
	"indigo": (0.22, 0.18, 0.43, 1.0),
	"aqua": (0.30, 0.76, 0.79, 1.0),
	"blue": (0.35, 0.58, 0.88, 1.0),
	"mint": (0.42, 0.82, 0.60, 1.0),
	"leaf": (0.24, 0.60, 0.42, 1.0),
	"lime": (0.61, 0.82, 0.34, 1.0),
	"lavender": (0.68, 0.55, 0.86, 1.0),
	"violet": (0.46, 0.30, 0.68, 1.0),
	"coral": (0.94, 0.42, 0.48, 1.0),
	"rose": (0.91, 0.55, 0.70, 1.0),
	"apricot": (0.97, 0.66, 0.38, 1.0),
	"gold": (0.97, 0.76, 0.29, 1.0),
	"cream": (0.96, 0.91, 0.79, 1.0),
	"wood": (0.48, 0.27, 0.27, 1.0),
	"coal": (0.19, 0.16, 0.29, 1.0),
	"soil": (0.48, 0.30, 0.25, 1.0),
}


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("MR2_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.86
	bsdf.inputs["Metallic"].default_value = 0.0
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root_object(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.data.materials.append(mat)
	return obj


def smooth(obj: bpy.types.Object) -> bpy.types.Object:
	if obj.type == "MESH":
		for polygon in obj.data.polygons:
			polygon.use_smooth = True
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


def sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	segments: int = 20,
	rings: int = 12,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.rotation_euler = rotation
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def ico(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	subdivisions: int = 2,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.rotation_euler = rotation
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def cylinder(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	vertices: int = 18,
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
	return bevel(obj, min(radius * 0.12, depth * 0.06), 2)


def cone(
	name: str,
	location: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	vertices: int = 24,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(
		vertices=vertices,
		radius1=radius,
		radius2=0.05,
		depth=depth,
		location=location,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, 0.06, 2)


def torus(
	name: str,
	location: tuple[float, float, float],
	major_radius: float,
	minor_radius: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (math.pi * 0.5, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(
		major_radius=major_radius,
		minor_radius=minor_radius,
		major_segments=16,
		minor_segments=8,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def star_prism(
	name: str,
	location: tuple[float, float, float],
	outer: float,
	inner: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	points: int = 5,
) -> bpy.types.Object:
	outline = []
	for index in range(points * 2):
		angle = math.pi * 0.5 + index * math.pi / points
		radius = outer if index % 2 == 0 else inner
		outline.append((math.cos(angle) * radius, math.sin(angle) * radius))
	verts = []
	for y in (-depth * 0.5, depth * 0.5):
		verts.extend([(x, y, z) for x, z in outline])
	count = len(outline)
	faces = [list(reversed(range(count))), list(range(count, count * 2))]
	for index in range(count):
		next_index = (index + 1) % count
		faces.append([index, next_index, count + next_index, count + index])
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(depth * 0.25, outer * 0.08), 3)


def leaf(
	name: str,
	location: tuple[float, float, float],
	length: float,
	width: float,
	angle: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	return sphere(
		name,
		location,
		(width, 0.10, length),
		mat,
		parent,
		rotation=(0.0, angle, 0.0),
		segments=16,
		rings=8,
	)


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
	items = [root]
	for child in root.children:
		items.extend(descendants(child))
	return items


def build_coal() -> bpy.types.Object:
	root = root_object("mg_coal")
	ico("coal_main", (0.0, 0.0, 0.7), (0.80, 0.38, 0.60), MATS["coal"], root, rotation=(0.1, 0.2, -0.2), subdivisions=2)
	ico("coal_side", (-0.42, 0.0, 0.54), (0.46, 0.31, 0.40), MATS["indigo"], root, rotation=(-0.2, 0.1, 0.3), subdivisions=1)
	ico("coal_highlight", (0.24, -0.28, 0.90), (0.22, 0.08, 0.15), MATS["violet"], root, subdivisions=1)
	return root


def build_seed() -> bpy.types.Object:
	root = root_object("mg_seed")
	sphere("seed", (0.0, 0.0, 0.65), (0.62, 0.25, 0.82), MATS["soil"], root, rotation=(0.0, 0.45, -0.22), segments=18, rings=10)
	sphere("seed_mark", (-0.17, -0.23, 0.85), (0.13, 0.05, 0.25), MATS["apricot"], root, rotation=(0.0, 0.35, -0.22), segments=12, rings=8)
	return root


def build_sprout() -> bpy.types.Object:
	root = root_object("mg_sprout")
	cylinder("stem", (0.0, 0.0, 0.92), 0.10, 1.55, MATS["leaf"], root, vertices=14)
	leaf("leaf_L", (-0.36, 0.0, 1.25), 0.42, 0.25, -0.85, MATS["mint"], root)
	leaf("leaf_R", (0.36, 0.0, 1.52), 0.42, 0.25, 0.85, MATS["lime"], root)
	sphere("soil", (0.0, 0.05, 0.15), (0.62, 0.24, 0.20), MATS["soil"], root, segments=16, rings=8)
	return root


def build_flower(name: str, petal_mat: bpy.types.Material, center_mat: bpy.types.Material, petal_count: int, petal_scale: float) -> bpy.types.Object:
	root = root_object(name)
	cylinder("stem", (0.0, 0.0, 1.35), 0.10, 2.35, MATS["leaf"], root, vertices=14)
	leaf("leaf_L", (-0.33, 0.0, 1.15), 0.46, 0.24, -0.85, MATS["mint"], root)
	leaf("leaf_R", (0.34, 0.02, 1.55), 0.42, 0.22, 0.90, MATS["lime"], root)
	center_z = 2.55
	for index in range(petal_count):
		angle = index / petal_count * math.tau
		x = math.cos(angle) * 0.56 * petal_scale
		z = center_z + math.sin(angle) * 0.56 * petal_scale
		sphere(
			f"petal_{index:02d}",
			(x, 0.02, z),
			(0.25 * petal_scale, 0.10, 0.48 * petal_scale),
			petal_mat,
			root,
			rotation=(0.0, -angle + math.pi * 0.5, 0.0),
			segments=14,
			rings=8,
		)
	sphere("flower_center", (0.0, -0.13, center_z), (0.38, 0.16, 0.38), center_mat, root, segments=16, rings=10)
	return root


def build_bush(name: str, flowering: bool) -> bpy.types.Object:
	root = root_object(name)
	clusters = [
		(-0.72, 0.0, 0.74, 0.72),
		(0.00, 0.04, 0.95, 0.88),
		(0.72, 0.0, 0.74, 0.70),
		(-0.38, -0.06, 1.38, 0.66),
		(0.38, -0.04, 1.42, 0.68),
	]
	colors = [MATS["leaf"], MATS["mint"], MATS["lime"]]
	for index, (x, y, z, radius) in enumerate(clusters):
		ico(f"bush_{index}", (x, y, z), (radius, radius * 0.64, radius), colors[index % len(colors)], root, subdivisions=2)
	if flowering:
		for index, (x, z) in enumerate(((-0.62, 1.22), (0.04, 1.63), (0.70, 1.05), (0.46, 0.55))):
			sphere(f"blossom_{index}", (x, -0.52, z), (0.18, 0.09, 0.18), [MATS["coral"], MATS["gold"], MATS["lavender"]][index % 3], root, segments=12, rings=8)
	return root


def build_tree() -> bpy.types.Object:
	root = root_object("mg_tree")
	cylinder("trunk", (0.0, 0.06, 1.25), 0.32, 2.5, MATS["wood"], root, vertices=16)
	for index, (x, z, radius) in enumerate(((-0.92, 2.62, 0.92), (0.0, 2.88, 1.10), (0.92, 2.60, 0.90), (-0.52, 3.45, 0.86), (0.48, 3.50, 0.86), (0.0, 4.05, 0.76))):
		ico(f"crown_{index}", (x, 0.0, z), (radius, radius * 0.70, radius), [MATS["leaf"], MATS["mint"], MATS["lime"]][index % 3], root, subdivisions=2)
	return root


def build_pine(name: str, snowy: bool) -> bpy.types.Object:
	root = root_object(name)
	cylinder("trunk", (0.0, 0.08, 0.80), 0.28, 1.6, MATS["wood"], root, vertices=16)
	tiers = [(1.48, 1.50, 1.82), (2.48, 1.24, 1.70), (3.35, 0.96, 1.54), (4.05, 0.65, 1.28)]
	for index, (z, radius, depth) in enumerate(tiers):
		cone(f"pine_{index}", (0.0, 0.0, z), radius, depth, [MATS["leaf"], MATS["aqua"]][index % 2], root)
		if snowy:
			sphere(f"snow_{index}", (0.0, -0.06, z - depth * 0.28), (radius * 0.86, 0.16, 0.18), MATS["cream"], root, segments=18, rings=8)
	return root


def build_sun() -> bpy.types.Object:
	root = root_object("mg_sun")
	sphere("sun_disc", (0.0, 0.0, 0.0), (1.18, 0.24, 1.18), MATS["gold"], root, segments=24, rings=14)
	for index in range(10):
		angle = index / 10.0 * math.tau
		x = math.cos(angle) * 1.72
		z = math.sin(angle) * 1.72
		sphere(
			f"ray_{index}",
			(x, 0.02, z),
			(0.22, 0.12, 0.48),
			MATS["apricot"] if index % 2 else MATS["gold"],
			root,
			rotation=(0.0, -angle + math.pi * 0.5, 0.0),
			segments=14,
			rings=8,
		)
	return root


def build_star() -> bpy.types.Object:
	root = root_object("mg_star")
	star_prism("reward_star", (0.0, 0.0, 0.0), 1.45, 0.68, 0.34, MATS["gold"], root)
	star_prism("star_inset", (0.0, -0.20, 0.03), 0.88, 0.42, 0.10, MATS["cream"], root)
	return root


def ornament_cap(root: bpy.types.Object, z: float) -> None:
	cylinder("cap", (0.0, 0.0, z), 0.22, 0.28, MATS["gold"], root, vertices=14)
	torus("loop", (0.0, 0.0, z + 0.28), 0.19, 0.055, MATS["gold"], root)


def build_ornament_round(name: str, body: bpy.types.Material, accent: bpy.types.Material) -> bpy.types.Object:
	root = root_object(name)
	sphere("body", (0.0, 0.0, 0.0), (0.82, 0.34, 0.92), body, root, segments=20, rings=12)
	sphere("accent", (0.0, -0.32, -0.08), (0.54, 0.08, 0.17), accent, root, segments=16, rings=8)
	ornament_cap(root, 1.02)
	return root


def build_ornament_finial() -> bpy.types.Object:
	root = root_object("mg_ornament_finial")
	sphere("upper", (0.0, 0.0, 0.45), (0.62, 0.30, 0.70), MATS["rose"], root, segments=18, rings=10)
	cone("drop", (0.0, 0.0, -0.55), 0.55, 1.45, MATS["coral"], root, vertices=20)
	ornament_cap(root, 1.20)
	return root


def build_ornament_star() -> bpy.types.Object:
	root = root_object("mg_ornament_star")
	star_prism("body", (0.0, 0.0, 0.0), 1.05, 0.48, 0.28, MATS["gold"], root)
	ornament_cap(root, 1.08)
	return root


def build_ornament_drop() -> bpy.types.Object:
	root = root_object("mg_ornament_drop")
	sphere("drop", (0.0, 0.0, -0.05), (0.66, 0.30, 0.90), MATS["lavender"], root, segments=20, rings=12)
	cone("tip", (0.0, 0.0, -0.92), 0.34, 0.72, MATS["violet"], root, vertices=18)
	sphere("band", (0.0, -0.29, 0.08), (0.55, 0.08, 0.15), MATS["mint"], root, segments=16, rings=8)
	ornament_cap(root, 1.02)
	return root


ASSETS: dict[str, tuple[bpy.types.Object, list[str]]] = {
	"coal": (build_coal(), ["coal.png"]),
	"seed": (build_seed(), ["seed.png"]),
	"sprout": (build_sprout(), ["sprout.png", "k_sprout.png"]),
	"flower_coral": (build_flower("mg_flower_coral", MATS["coral"], MATS["gold"], 6, 1.00), ["flower.png"]),
	"flower_lavender": (build_flower("mg_flower_lavender", MATS["lavender"], MATS["cream"], 7, 0.95), ["flower2.png"]),
	"flower_blue": (build_flower("mg_flower_blue", MATS["blue"], MATS["gold"], 5, 1.05), ["flower3.png"]),
	"flower_white": (build_flower("mg_flower_white", MATS["cream"], MATS["coral"], 8, 0.88), ["flower4.png"]),
	"flower_rose": (build_flower("mg_flower_rose", MATS["rose"], MATS["violet"], 6, 0.98), ["k_flower1.png"]),
	"flower_yellow": (build_flower("mg_flower_yellow", MATS["gold"], MATS["coral"], 9, 0.86), ["k_flower2.png"]),
	"bush": (build_bush("mg_bush", False), ["k_bush.png"]),
	"bush_flowering": (build_bush("mg_bush_flowering", True), ["k_bush2.png"]),
	"tree": (build_tree(), ["tree.png"]),
	"pine": (build_pine("mg_pine", False), ["k_pine.png"]),
	"xmas_tree": (build_pine("mg_xmas_tree_empty", True), ["xtree.png", "k_xmastree.png"]),
	"sun": (build_sun(), ["sun.png"]),
	"star": (build_star(), ["star.png"]),
	"ornament_round": (build_ornament_round("mg_ornament_round", MATS["lavender"], MATS["rose"]), ["orn1.png"]),
	"ornament_finial": (build_ornament_finial(), ["orn2.png"]),
	"ornament_pearl": (build_ornament_round("mg_ornament_pearl", MATS["blue"], MATS["cream"]), ["orn3.png"]),
	"ornament_star": (build_ornament_star(), ["orn4.png"]),
	"ornament_drop": (build_ornament_drop(), ["orn5.png"]),
}


scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = True
scene.render.use_freestyle = True
scene.render.line_thickness = 1.3
scene.view_settings.look = "AgX - Medium High Contrast"

line_set = scene.view_layers[0].freestyle_settings.linesets[0]
line_style = line_set.linestyle
if line_style is None:
	line_style = bpy.data.linestyles.new("storybook_navy_line")
	line_set.linestyle = line_style
line_style.color = PALETTE["navy"][:3]
line_style.thickness = 1.7

world = bpy.data.worlds.new("storybook_world")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.62, 0.76, 0.80, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55
scene.world = world

key_data = bpy.data.lights.new("key", "AREA")
key_data.energy = 820
key_data.shape = "DISK"
key_data.size = 6.0
key = bpy.data.objects.new("key", key_data)
key.location = (-4.5, -6.0, 8.0)
bpy.context.collection.objects.link(key)

fill_data = bpy.data.lights.new("fill", "AREA")
fill_data.energy = 480
fill_data.size = 5.0
fill = bpy.data.objects.new("fill", fill_data)
fill.location = (5.0, -3.5, 4.5)
bpy.context.collection.objects.link(fill)

camera_data = bpy.data.cameras.new("icon_camera")
camera_data.type = "ORTHO"
camera = bpy.data.objects.new("icon_camera", camera_data)
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


def render_icon(root: bpy.types.Object, output_name: str) -> None:
	for other_root, _ in ASSETS.values():
		for obj in descendants(other_root):
			obj.hide_render = other_root != root
	mins, maxs = bounds_for(root)
	center = (mins + maxs) * 0.5
	width = maxs.x - mins.x
	height = maxs.z - mins.z
	camera.location = Vector((center.x, mins.y - 14.0, center.z))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	camera.data.ortho_scale = max(width, height) * 1.32
	scene.render.filepath = str(RUNTIME_OUT / output_name)
	bpy.ops.render.render(write_still=True)
	print("RENDERED", scene.render.filepath)


for _, (asset_root, output_names) in ASSETS.items():
	render_icon(asset_root, output_names[0])
	for output_name in output_names[1:]:
		shutil.copyfile(RUNTIME_OUT / output_names[0], RUNTIME_OUT / output_name)
		print("COPIED", RUNTIME_OUT / output_name)

for asset_root, _ in ASSETS.values():
	for obj in descendants(asset_root):
		obj.hide_render = False

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
print("SAVED", BLEND_OUT)
