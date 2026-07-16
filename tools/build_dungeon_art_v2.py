#!/usr/bin/env python3
"""Build the authored Mobile-friendly dungeon art kit.

Usage:
  blender --background --python tools/build_dungeon_art_v2.py

The kit replaces runtime engine primitives with editable project-authored
geometry. It does not use or modify protected book, family, or toy art.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "dungeon"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_dungeon_art_v2"
BLEND_OUT = SOURCE_OUT / "dungeon_art_v2.blend"

for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"surface": (0.25, 0.30, 0.50, 1.0),
	"trim": (0.43, 0.78, 0.82, 1.0),
	"dark": (0.09, 0.07, 0.20, 1.0),
	"navy": (0.10, 0.09, 0.24, 1.0),
	"lavender": (0.66, 0.52, 0.86, 1.0),
	"violet": (0.39, 0.24, 0.58, 1.0),
	"aqua": (0.29, 0.78, 0.82, 1.0),
	"ice": (0.66, 0.91, 0.96, 1.0),
	"coral": (0.94, 0.39, 0.43, 1.0),
	"apricot": (0.97, 0.63, 0.35, 1.0),
	"gold": (0.96, 0.75, 0.25, 1.0),
	"cream": (0.96, 0.91, 0.78, 1.0),
	"leaf": (0.28, 0.62, 0.40, 1.0),
	"shell": (0.38, 0.64, 0.43, 1.0),
	"wood": (0.48, 0.25, 0.18, 1.0),
	"flame": (1.0, 0.31, 0.08, 1.0),
}


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("MRD_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.84
	bsdf.inputs["Metallic"].default_value = 0.0
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root_object(name: str, parent: bpy.types.Object | None = None) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	root.parent = parent
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
	modifier = obj.modifiers.new("storybook_rounding", "BEVEL")
	modifier.width = width
	modifier.segments = segments
	modifier.limit_method = "ANGLE"
	apply_modifier(obj, modifier)
	return smooth(obj)


def cube(
	name: str,
	location: tuple[float, float, float],
	size: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	radius: float = 0.18,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = tuple(value * 0.5 for value in size)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(radius, min(size) * 0.2), 3)


def sphere(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 20,
	rings: int = 12,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def ico(
	name: str,
	location: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	subdivisions: int = 2,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
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
	vertices: int = 20,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(
		vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(radius * 0.11, depth * 0.12), 2)


def cone(
	name: str,
	location: tuple[float, float, float],
	radius1: float,
	radius2: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	vertices: int = 14,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(
		vertices=vertices,
		radius1=radius1,
		radius2=radius2,
		depth=depth,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def torus(
	name: str,
	location: tuple[float, float, float],
	major: float,
	minor: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(
		major_radius=major,
		minor_radius=minor,
		major_segments=20,
		minor_segments=8,
		location=location,
		rotation=rotation,
	)
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	assign(obj, mat)
	return smooth(obj)


def prism(
	name: str,
	points: list[tuple[float, float]],
	depth: float,
	location: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
) -> bpy.types.Object:
	verts = [(x, y, -depth * 0.5) for x, y in points] + [(x, y, depth * 0.5) for x, y in points]
	n = len(points)
	faces = [list(range(n)), list(range(n, n * 2))[::-1]]
	for i in range(n):
		j = (i + 1) % n
		faces.append([i, j, n + j, n + i])
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.parent = parent
	assign(obj, mat)
	return bevel(obj, min(depth * 0.2, 0.08), 2)


def star_points(outer: float, inner: float, count: int = 5) -> list[tuple[float, float]]:
	points: list[tuple[float, float]] = []
	for i in range(count * 2):
		radius = outer if i % 2 == 0 else inner
		a = math.pi * 0.5 + float(i) * math.pi / float(count)
		points.append((math.cos(a) * radius, math.sin(a) * radius))
	return points


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
	items = [root]
	for child in root.children:
		items.extend(descendants(child))
	return items


def merge_direct_meshes(parent: bpy.types.Object) -> None:
	"""Collapse meshes by visual role without removing semantic empty nodes."""
	groups: dict[str, list[bpy.types.Object]] = {}
	for child in list(parent.children):
		if child.type != "MESH":
			continue
		if child.name.startswith("Tint_"):
			key = "Tint_Surface"
		elif child.name.startswith("Trim_"):
			key = "Trim_Detail"
		else:
			# Blender keeps material slots when joining, so fixed-color details can
			# share one node without losing their palette separation.
			key = "Fixed_Detail"
		groups.setdefault(key, []).append(child)
	for name, objects in groups.items():
		if len(objects) == 1:
			objects[0].name = name
			continue
		bpy.ops.object.select_all(action="DESELECT")
		for obj in objects:
			obj.select_set(True)
		bpy.context.view_layer.objects.active = objects[0]
		bpy.ops.object.join()
		joined = bpy.context.active_object
		joined.name = name
		joined.parent = parent


def optimize_asset(root: bpy.types.Object) -> None:
	# Work from leaves upward so special groups such as Head and Shell remain
	# addressable by gameplay while their internal meshes are batched.
	for child in list(root.children):
		if child.type == "EMPTY":
			optimize_asset(child)
	merge_direct_meshes(root)


def build_arena() -> bpy.types.Object:
	root = root_object("DungeonArena")
	cylinder("Tint_Floor", (0, 0, -0.45), 27.0, 0.9, MATS["surface"], root, vertices=32)
	cylinder("Floor_Inlay", (0, 0, 0.04), 21.5, 0.16, MATS["dark"], root, vertices=32)
	# Raised rings and shell mosaics give the broad play surface an authored
	# storybook read from the fixed three-quarter gameplay camera.
	torus("Floor_Gold_Ring", (0, 0, 0.2), 20.8, 0.22, MATS["gold"], root)
	torus("Floor_Aqua_Ring", (0, 0, 0.22), 6.2, 0.16, MATS["aqua"], root)
	cylinder("Floor_Medallion", (0, 0, 0.22), 2.2, 0.18, MATS["lavender"], root, vertices=16)
	for i in range(8):
		a = float(i) * math.tau / 8.0
		x, y = math.sin(a) * 4.25, math.cos(a) * 4.25
		petal = ico(
			f"Floor_Shell_Petal_{i}", (x, y, 0.31), (1.05, 2.1, 0.18),
			MATS["coral" if i % 2 == 0 else "aqua"], root, 2,
		)
		petal.rotation_euler[2] = -a
	for i in range(8):
		a = float(i) * math.tau / 8.0
		# Preserve the entrance and exit openings used by both room types.
		if i not in (0, 4):
			# A row of irregular shell-stones replaces the old straight box wall.
			center = Vector((math.sin(a) * 25.7, math.cos(a) * 25.7, 0.0))
			tangent = Vector((math.cos(a), -math.sin(a), 0.0))
			for stone_i in range(-3, 4):
				stone_pos = center + tangent * float(stone_i) * 2.45
				stone = ico(
					f"Tint_WallStone_{i}_{stone_i}",
					(stone_pos.x, stone_pos.y, 1.15 + 0.12 * abs(stone_i % 2)),
					(1.7, 1.2, 1.35 + 0.16 * abs(stone_i % 2)), MATS["surface"], root, 2,
				)
				stone.rotation_euler[2] = -a + float(stone_i) * 0.14
			for side in (-1.0, 1.0):
				world = center + tangent * side * 7.75
				ico(
					f"Buttress_Base_{i}_{side}", (world.x, world.y, 0.85),
					(1.35, 1.2, 0.9), MATS["navy"], root, 2,
				)
				# Three rounded sea-glass branches make a readable coral silhouette
				# without relying on stock cone spikes.
				for branch_i, offset in enumerate((-0.7, 0.0, 0.7)):
					branch_pos = world + tangent * offset
					height = 2.7 + float(branch_i % 2) * 1.0
					cylinder(
						f"Trim_ButtressStem_{i}_{side}_{branch_i}",
						(branch_pos.x, branch_pos.y, 1.1 + height * 0.5),
						0.38 + 0.08 * float(branch_i == 1), height, MATS["trim"], root, vertices=12,
					)
					ico(
						f"Buttress_Pearl_{i}_{side}_{branch_i}",
						(branch_pos.x, branch_pos.y, 1.15 + height),
						(0.62, 0.62, 0.62), MATS["gold" if branch_i == 1 else "ice"], root, 2,
					)
		for ray_i, radius in enumerate((9.0, 14.5, 19.5)):
			x, y = math.sin(a) * radius, math.cos(a) * radius
			diamond = prism(
				f"Floor_Diamond_{i}_{ray_i}", [(-0.75, 0), (0, 1.35), (0.75, 0), (0, -1.35)],
				0.15, (x, y, 0.28), MATS["gold" if ray_i == 1 else "lavender"], root,
			)
			diamond.rotation_euler[2] = -a
	for i in range(8):
		a = (float(i) + 0.5) * math.tau / 8.0
		x, y = math.sin(a) * 23.4, math.cos(a) * 23.4
		ico(f"Rune_Pearl_{i}", (x, y, 1.0), (0.6, 0.6, 0.6), MATS["gold"], root, 2)
	return root


def build_door() -> bpy.types.Object:
	root = root_object("DungeonDoor")
	cube("DoorPanel", (0, 0.2, 4.7), (8.2, 0.8, 9.4), MATS["dark"], root, radius=0.55)
	for side in (-1.0, 1.0):
		cylinder(f"Tint_Column_{side}", (side * 5.2, 0, 4.0), 1.25, 8.0, MATS["surface"], root, vertices=16)
		cone(f"Trim_Cap_{side}", (side * 5.2, 0, 8.8), 1.7, 0.35, 2.5, MATS["trim"], root)
	# A solid shell crown keeps the fan ribs connected at gameplay distance.
	sphere("Tint_Shell_Crown", (0, 0.22, 9.0), (5.7, 0.78, 2.6), MATS["surface"], root)
	cube("Trim_Lintel", (0, -0.48, 8.45), (8.8, 0.55, 1.25), MATS["trim"], root, radius=0.35)
	for i in range(7):
		a = math.radians(-66.0 + float(i) * 22.0)
		x = math.sin(a) * 5.4
		z = 8.1 + math.cos(a) * 3.1
		cube(f"Trim_Shell_Rib_{i}", (x, -0.62, z), (0.55, 0.42, 4.3), MATS["trim"], root, rotation=(0, -a, 0), radius=0.16)
	star = prism("Gold_Door_Star", star_points(1.45, 0.66), 0.35, (0, -0.75, 5.3), MATS["gold"], root)
	star.rotation_euler[0] = math.pi * 0.5
	for z in (1.8, 3.4, 7.2):
		cube(f"Door_Gold_Band_{z}", (0, -0.48, z), (6.2, 0.24, 0.32), MATS["gold"], root, radius=0.1)
	return root


def build_imp() -> bpy.types.Object:
	root = root_object("MischiefImp")
	sphere("Body", (0, 0, 1.65), (1.35, 0.95, 1.7), MATS["violet"], root)
	sphere("Hood", (0, 0, 3.0), (1.3, 0.92, 1.15), MATS["lavender"], root)
	# Broad fins read as a sea creature instead of the old cone-eared sphere.
	left_fin = [(0, 0.8), (-2.0, 1.65), (-1.35, -0.45), (0, -0.15)]
	prism("Left_Fin", left_fin, 0.24, (-0.95, 0.1, 1.8), MATS["aqua"], root)
	right_fin = [(-x, y) for x, y in left_fin]
	prism("Right_Fin", right_fin, 0.24, (0.95, 0.1, 1.8), MATS["aqua"], root)
	for side in (-1.0, 1.0):
		sphere(f"Eye_White_{side}", (side * 0.46, -0.86, 3.18), (0.31, 0.16, 0.36), MATS["cream"], root)
		sphere(f"Eye_{side}", (side * 0.46, -1.03, 3.18), (0.13, 0.09, 0.16), MATS["navy"], root)
		cone(f"Foot_{side}", (side * 0.48, -0.1, 0.25), 0.42, 0.12, 0.9, MATS["coral"], root, rotation=(0, math.radians(side * 20), 0))
	prism("Tail_Fin", [(-0.9, 0), (0, 1.3), (0.9, 0), (0, -0.4)], 0.22, (0, 0.75, 0.75), MATS["coral"], root)
	return root


def build_boss() -> bpy.types.Object:
	root = root_object("DragonTurtle")
	body = root_object("Body", root)
	shell = root_object("Shell", root)
	head = root_object("Head", root)
	sphere("Belly", (0, 0, 2.1), (3.5, 2.8, 1.65), MATS["leaf"], body)
	sphere("Shell_Dome", (0, 0.35, 3.25), (4.2, 3.35, 1.8), MATS["shell"], shell)
	# The shell is the boss for half of the encounter. Its pattern must remain
	# legible while the head is hidden and the model is spinning.
	outer_ring = torus("Shell_Outer_Ridge", (0, 0.35, 5.02), 3.05, 0.2, MATS["navy"], shell)
	outer_ring.scale.y = 0.78
	inner_ring = torus("Shell_Inner_Ridge", (0, 0.35, 5.18), 1.62, 0.16, MATS["gold"], shell)
	inner_ring.scale.y = 0.78
	center_star = prism("Shell_Crown_Star", star_points(1.28, 0.58), 0.34, (0, 0.35, 5.32), MATS["gold"], shell)
	for ring, count, radius in ((0, 6, 2.25), (1, 8, 3.15)):
		for i in range(count):
			a = float(i) * math.tau / float(count)
			ico(
				f"Shell_Scute_{ring}_{i}",
				(math.sin(a) * radius, math.cos(a) * radius * 0.72 + 0.35, 5.18 - ring * 0.12),
				(0.68 if ring == 0 else 0.5, 0.56 if ring == 0 else 0.42, 0.22),
				MATS["coral" if ring == 0 else "aqua"], shell, 1,
			)
	for i in range(6):
		a = float(i) * math.tau / 6.0
		x, y = math.sin(a) * 1.95, math.cos(a) * 1.48 + 0.35
		ridge = cube(
			f"Shell_Radial_Ridge_{i}", (x, y, 5.12), (0.18, 2.25, 0.16),
			MATS["cream"], shell, rotation=(0, 0, -a), radius=0.06,
		)
		ridge.scale.y = 0.72
	for side in (-1.0, 1.0):
		for front in (-1.0, 1.0):
			fin = [(-1.4, 0.2), (-0.2, 1.0), (1.7, 0.35), (0.4, -0.65)]
			obj = prism(f"Flipper_{side}_{front}", fin, 0.42, (side * 3.3, front * 1.85, 1.45), MATS["leaf"], body)
			obj.rotation_euler[2] = math.radians(35.0 * side * front)
	prism("Tail", [(-0.8, 0), (0, 2.3), (0.8, 0), (0, -0.5)], 0.48, (0, 3.2, 1.7), MATS["leaf"], body)
	sphere("Head_Form", (0, -4.05, 2.8), (2.1, 1.9, 1.65), MATS["leaf"], head)
	sphere("Muzzle", (0, -5.55, 2.35), (1.42, 0.8, 0.76), MATS["cream"], head)
	for side in (-1.0, 1.0):
		sphere(f"Boss_Eye_White_{side}", (side * 0.74, -5.55, 3.35), (0.46, 0.25, 0.54), MATS["cream"], head)
		sphere(f"Boss_Eye_{side}", (side * 0.74, -5.79, 3.35), (0.18, 0.11, 0.23), MATS["navy"], head)
		cone(f"Dragon_Horn_{side}", (side * 1.2, -3.75, 4.05), 0.38, 0.05, 1.6, MATS["gold"], head, rotation=(0, math.radians(side * 25), math.radians(side * 20)))
		cone(f"Ivory_Claw_{side}", (side * 3.9, -2.1, 1.0), 0.44, 0.04, 1.45, MATS["cream"], body, rotation=(math.radians(70), 0, math.radians(side * 18)))
	return root


def build_basket() -> bpy.types.Object:
	root = root_object("PepperBasket")
	for z, radius in ((0.35, 1.65), (0.85, 1.9), (1.35, 2.1)):
		torus(f"Weave_Ring_{z}", (0, 0, z), radius, 0.14, MATS["wood"], root)
	for i in range(10):
		a = float(i) * math.tau / 10.0
		x, y = math.sin(a) * 1.75, math.cos(a) * 1.75
		cube(f"Weave_Rib_{i}", (x, y, 0.8), (0.22, 0.22, 1.55), MATS["wood"], root, radius=0.08)
	torus("Basket_Handle", (0, 0, 1.6), 2.25, 0.16, MATS["gold"], root, rotation=(math.pi * 0.5, 0, 0))
	for i in range(5):
		x = -1.0 + float(i) * 0.5
		pepper = sphere(f"Pepper_{i}", (x, 0, 1.65 + float(i % 2) * 0.28), (0.36, 0.42, 0.72), MATS["coral"], root)
		pepper.rotation_euler[1] = math.radians(-18 + i * 9)
		cone(f"Pepper_Stem_{i}", (x, 0, 2.36 + float(i % 2) * 0.28), 0.12, 0.04, 0.38, MATS["leaf"], root)
	return root


def build_pedestal() -> bpy.types.Object:
	root = root_object("CrystalPedestal")
	cylinder("Tint_Pedestal_Base", (0, 0, 0.35), 3.4, 0.7, MATS["surface"], root, vertices=16)
	cylinder("Trim_Pedestal_Rim", (0, 0, 0.78), 2.85, 0.3, MATS["trim"], root, vertices=16)
	for i in range(8):
		a = float(i) * math.tau / 8.0
		x, y = math.sin(a) * 2.45, math.cos(a) * 2.45
		ico(f"Pearl_{i}", (x, y, 1.0), (0.27, 0.27, 0.27), MATS["gold"], root, 1)
	return root


def build_lantern() -> bpy.types.Object:
	root = root_object("PepperLantern")
	stem = root
	cylinder("Stem_Shaft", (0, 0, 2.2), 0.32, 4.4, MATS["wood"], stem, vertices=12)
	for i in range(3):
		a = math.radians(-35.0 + i * 35.0)
		fin = [(-0.2, 0), (-1.2, 0.8), (-0.9, -0.5), (0.1, -0.3)]
		leaf = prism(f"Stem_Leaf_{i}", fin, 0.18, (0, 0, 1.2 + i * 1.0), MATS["leaf"], stem)
		leaf.rotation_euler[1] = a
	sphere("Lantern_Glass", (0, 0, 5.1), (0.95, 0.78, 1.35), MATS["coral"], root)
	cone("Lantern_Cap", (0, 0, 6.35), 1.0, 0.18, 0.8, MATS["gold"], root)
	glow = root_object("Glow", root)
	sphere("Flame_Outer", (0, -0.82, 5.1), (0.48, 0.24, 0.72), MATS["flame"], glow)
	sphere("Flame_Inner", (0, -1.02, 5.0), (0.23, 0.12, 0.4), MATS["gold"], glow)
	return root


def build_turtle_statue() -> bpy.types.Object:
	root = root_object("TurtleStatue")
	sphere("Statue_Shell", (0, 0, 2.2), (2.55, 1.85, 1.35), MATS["shell"], root)
	for i in range(6):
		a = float(i) * math.tau / 6.0
		ico(f"Statue_Scute_{i}", (math.sin(a) * 1.45, math.cos(a) * 0.95, 3.0), (0.5, 0.38, 0.24), MATS["trim"], root, 1)
	sphere("Statue_Head", (0, -2.0, 2.0), (1.05, 1.2, 0.92), MATS["leaf"], root)
	cone("Golden_Nose", (0, -3.35, 2.0), 0.42, 0.08, 1.5, MATS["gold"], root, rotation=(math.pi * 0.5, 0, 0))
	for side in (-1.0, 1.0):
		prism(f"Statue_Flipper_{side}", [(-0.7, 0), (0, 0.7), (1.1, 0.2), (0, -0.4)], 0.3, (side * 2.1, -0.45, 1.25), MATS["leaf"], root)
	return root


def build_stepping_stone() -> bpy.types.Object:
	root = root_object("SteppingStone")
	ico("Tint_Stone", (0, 0, 0.25), (2.7, 2.1, 0.65), MATS["surface"], root, 2)
	for i in range(5):
		a = float(i) * math.tau / 5.0
		x, y = math.sin(a) * 1.45, math.cos(a) * 1.05
		ico(f"Trim_Inlay_{i}", (x, y, 0.82), (0.24, 0.24, 0.12), MATS["trim"], root, 1)
	return root


def build_pictograms() -> bpy.types.Object:
	root = root_object("DungeonPictograms")
	roles: dict[str, bpy.types.Object] = {}
	for name in ("Diamond", "Orb", "Triangle", "Ice", "Flame", "Moon", "Star", "Question", "Left", "Right", "Pepper"):
		roles[name] = root_object(name, root)
	ico("Diamond_Mesh", (0, 0, 0), (1.0, 0.42, 1.35), MATS["aqua"], roles["Diamond"], 1)
	sphere("Orb_Mesh", (0, 0, 0), (1.1, 0.48, 1.1), MATS["coral"], roles["Orb"], 16, 10)
	prism("Triangle_Mesh", [(-1.2, -0.9), (1.2, -0.9), (0, 1.25)], 0.55, (0, 0, 0), MATS["lavender"], roles["Triangle"])
	for i in range(3):
		cube(f"Ice_Branch_{i}", (0, 0, 0), (0.28, 0.48, 2.8), MATS["ice"], roles["Ice"], rotation=(0, math.radians(i * 60), 0), radius=0.1)
	sphere("Flame_Outer_Shape", (0, 0, 0), (0.9, 0.42, 1.35), MATS["flame"], roles["Flame"])
	cone("Flame_Tip", (0, 0, 1.0), 0.72, 0.04, 1.3, MATS["gold"], roles["Flame"])
	moon_points: list[tuple[float, float]] = []
	for i in range(9):
		a = math.radians(90 + i * 22.5)
		moon_points.append((math.cos(a) * 1.3, math.sin(a) * 1.3))
	for i in range(8, -1, -1):
		a = math.radians(90 + i * 22.5)
		moon_points.append((0.55 + math.cos(a) * 0.82, math.sin(a) * 0.82))
	prism("Moon_Mesh", moon_points, 0.45, (0, 0, 0), MATS["gold"], roles["Moon"])
	prism("Star_Mesh", star_points(1.35, 0.62), 0.45, (0, 0, 0), MATS["gold"], roles["Star"])
	torus("Question_Curl", (0, 0, 0.45), 0.72, 0.22, MATS["lavender"], roles["Question"], rotation=(math.pi * 0.5, 0, 0))
	sphere("Question_Dot", (0, 0, -1.0), (0.26, 0.2, 0.26), MATS["lavender"], roles["Question"])
	arrow = [(-1.2, 0), (0.1, 1.0), (0.1, 0.38), (1.2, 0.38), (1.2, -0.38), (0.1, -0.38), (0.1, -1.0)]
	left = prism("Left_Arrow", arrow, 0.45, (0, 0, 0), MATS["aqua"], roles["Left"])
	left.rotation_euler[1] = math.pi
	prism("Right_Arrow", arrow, 0.45, (0, 0, 0), MATS["coral"], roles["Right"])
	sphere("Pepper_Body", (0, 0, -0.15), (0.68, 0.42, 1.1), MATS["coral"], roles["Pepper"])
	cone("Pepper_Stem", (0, 0, 0.95), 0.22, 0.04, 0.55, MATS["leaf"], roles["Pepper"])
	return root


ASSETS = {
	"dungeon_arena": build_arena(),
	"dungeon_door": build_door(),
	"mischief_imp": build_imp(),
	"dragon_turtle": build_boss(),
	"pepper_basket": build_basket(),
	"crystal_pedestal": build_pedestal(),
	"pepper_lantern": build_lantern(),
	"turtle_statue": build_turtle_statue(),
	"stepping_stone": build_stepping_stone(),
	"dungeon_pictograms": build_pictograms(),
}

for asset_root in ASSETS.values():
	optimize_asset(asset_root)


def select_root(root: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for obj in descendants(root):
		obj.hide_viewport = False
		obj.hide_render = False
		obj.select_set(True)
	bpy.context.view_layer.objects.active = root


def export_root(name: str, root: bpy.types.Object) -> None:
	select_root(root)
	path = ASSET_OUT / f"{name}.glb"
	bpy.ops.export_scene.gltf(
		filepath=str(path),
		export_format="GLB",
		use_selection=True,
		export_materials="EXPORT",
		export_animations=False,
		export_yup=True,
	)
	print("EXPORTED", path)


for asset_name, asset_root in ASSETS.items():
	export_root(asset_name, asset_root)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))


scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "rim.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "BOTH"
scene.render.resolution_x = 900
scene.render.resolution_y = 700
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = True

bpy.ops.object.camera_add()
camera = bpy.context.active_object
scene.camera = camera


def mesh_bounds(root: bpy.types.Object) -> tuple[Vector, float]:
	points: list[Vector] = []
	for obj in descendants(root):
		if obj.type != "MESH":
			continue
		for corner in obj.bound_box:
			points.append(obj.matrix_world @ Vector(corner))
	if not points:
		return Vector((0, 0, 0)), 5.0
	low = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
	high = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
	return (low + high) * 0.5, max((high - low).length, 2.0)


def render_root(name: str, root: bpy.types.Object) -> None:
	for other in ASSETS.values():
		for obj in descendants(other):
			obj.hide_render = other != root
	center, diameter = mesh_bounds(root)
	camera.location = center + Vector((diameter * 0.75, -diameter * 0.95, diameter * 0.62))
	direction = center - camera.location
	camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
	camera.data.type = "ORTHO"
	camera.data.ortho_scale = diameter * 0.72
	scene.render.filepath = str(QA_OUT / f"{name}.png")
	bpy.ops.render.render(write_still=True)
	print("RENDERED", scene.render.filepath)


for asset_name, asset_root in ASSETS.items():
	render_root(asset_name, asset_root)

print("DUNGEON_ART_V2_DONE")
