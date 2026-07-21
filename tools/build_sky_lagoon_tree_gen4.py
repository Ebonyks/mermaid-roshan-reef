#!/usr/bin/env python3
"""Build eight Sky Lagoon GEN4 trees from the approved sculpt language.

The four shipped GEN2 trees remain untouched.  This builder uses their dense,
faceted meshes as modeling stock, then performs large mesh-space silhouette
warps, multi-trunk assembly, and habitat-specific detailing.  The result keeps
the hand-cut planes and interior branch rhythm the owner preferred while each
new role receives a different botanical graph and proportion.

Usage: blender --background --python tools/build_sky_lagoon_tree_gen4.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Callable

import bmesh
import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit"
BLEND = ROOT / "assets_src" / "blender" / "sky_lagoon_tree_gen4.blend"
OUT.mkdir(parents=True, exist_ok=True)
BLEND.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0

GEN2 = {
	"round": ROOT / "assets" / "props" / "gen2" / "tree_pineroundf.glb",
	"oak": ROOT / "assets" / "props" / "gen2" / "tree_fall.glb",
	"airy": ROOT / "assets" / "props" / "gen2" / "tree_fall2.glb",
	"dome": ROOT / "assets" / "props" / "gen2" / "tree_fat.glb",
	"snow_pine": ROOT / "assets" / "northern" / "northern_pine_a.glb",
}

PALETTE = {
	"ink": (0.055, 0.035, 0.12, 1.0),
	"bark": (0.48, 0.27, 0.20, 1.0),
	"bark_light": (0.70, 0.43, 0.31, 1.0),
	"stone": (0.61, 0.75, 0.80, 1.0),
	"stone_light": (0.80, 0.88, 0.86, 1.0),
	"coral": (0.89, 0.43, 0.52, 1.0),
	"rose": (0.79, 0.44, 0.68, 1.0),
	"butter": (0.96, 0.73, 0.28, 1.0),
	"aqua": (0.33, 0.72, 0.72, 1.0),
	"lavender": (0.62, 0.55, 0.82, 1.0),
	"snow": (0.90, 0.95, 0.98, 1.0),
}


def material(name: str) -> bpy.types.Material:
	existing = bpy.data.materials.get("SL_GEN4_" + name)
	if existing is not None:
		return existing
	mat = bpy.data.materials.new("SL_GEN4_" + name)
	mat.diffuse_color = PALETTE[name]
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = PALETTE[name]
	bsdf.inputs["Roughness"].default_value = 0.94
	bsdf.inputs["Metallic"].default_value = 0.0
	bsdf.inputs["Specular IOR Level"].default_value = 0.16
	return mat


def new_root(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def import_mesh(source: Path, name: str, parent: bpy.types.Object) -> bpy.types.Object:
	before = set(bpy.context.scene.objects)
	bpy.ops.import_scene.gltf(filepath=str(source))
	created = [obj for obj in bpy.context.scene.objects if obj not in before]
	meshes = [obj for obj in created if obj.type == "MESH"]
	if len(meshes) != 1:
		raise RuntimeError("Expected one mesh in %s, found %d" % (source, len(meshes)))
	obj = meshes[0]
	world = obj.matrix_world.copy()
	obj.parent = None
	obj.data.transform(world)
	obj.matrix_world = Matrix.Identity(4)
	obj.name = name
	obj.data.name = name + "_mesh"
	obj.parent = parent
	for other in created:
		if other != obj:
			bpy.data.objects.remove(other, do_unlink=True)
	return obj


def normalized_coordinates(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	minimum = Vector((1.0e9, 1.0e9, 1.0e9))
	maximum = Vector((-1.0e9, -1.0e9, -1.0e9))
	for vertex in obj.data.vertices:
		for axis in range(3):
			minimum[axis] = min(minimum[axis], vertex.co[axis])
			maximum[axis] = max(maximum[axis], vertex.co[axis])
	return minimum, maximum


Warp = Callable[[float, float, float], tuple[float, float, float]]


def reshape(obj: bpy.types.Object, warp: Warp) -> None:
	minimum, maximum = normalized_coordinates(obj)
	center = (minimum + maximum) * 0.5
	span = maximum - minimum
	for vertex in obj.data.vertices:
		x = (vertex.co.x - center.x) / max(span.x * 0.5, 0.0001)
		y = (vertex.co.y - center.y) / max(span.y * 0.5, 0.0001)
		t = (vertex.co.z - minimum.z) / max(span.z, 0.0001)
		vertex.co = warp(x, y, t)
	obj.data.update()


def decimate(obj: bpy.types.Object, ratio: float) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	modifier = obj.modifiers.new("mobile_sculpt_preserve", "DECIMATE")
	modifier.ratio = ratio
	modifier.use_collapse_triangulate = True
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def ico(name: str, location: tuple[float, float, float], scale: tuple[float, float, float],
	mat_name: str, parent: bpy.types.Object, subdivisions: int = 1) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1.0, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.data.materials.append(material(mat_name))
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	obj.parent = parent
	return obj


def planted_stones(parent: bpy.types.Object, radius: float, count: int, seed: float = 0.0) -> None:
	for index in range(count):
		angle = math.tau * index / count + seed
		size = 0.22 + 0.07 * ((index * 5) % 3)
		ico("root_stone_%02d" % index,
			(math.cos(angle) * radius, math.sin(angle) * radius * 0.72, 0.12),
			(size * 1.35, size, size * 0.70),
			"stone_light" if index % 2 else "stone", parent)


def crop_below(obj: bpy.types.Object, normalized_height: float) -> None:
	minimum, maximum = normalized_coordinates(obj)
	cutoff = minimum.z + (maximum.z - minimum.z) * normalized_height
	mesh = bmesh.new()
	mesh.from_mesh(obj.data)
	bmesh.ops.delete(mesh, geom=[vertex for vertex in mesh.verts if vertex.co.z < cutoff],
		context="VERTS")
	mesh.to_mesh(obj.data)
	mesh.free()
	obj.data.update()


def branch_tube(name: str, points: list[tuple[float, float, float]], radius: float,
	parent: bpy.types.Object) -> bpy.types.Object:
	curve_data = bpy.data.curves.new(name + "_curve", "CURVE")
	curve_data.dimensions = "3D"
	curve_data.resolution_u = 2
	curve_data.bevel_depth = radius
	curve_data.bevel_resolution = 1
	curve_data.resolution_u = 2
	spline = curve_data.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, coordinate in zip(spline.bezier_points, points):
		point.co = coordinate
		point.handle_left_type = "AUTO"
		point.handle_right_type = "AUTO"
	obj = bpy.data.objects.new(name, curve_data)
	bpy.context.collection.objects.link(obj)
	obj.data.materials.append(material("bark"))
	obj.parent = parent
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	obj.name = name
	obj.parent = parent
	obj.select_set(False)
	return obj


def willow_crown_piece(parent: bpy.types.Object, name: str,
	center: tuple[float, float, float], half_width: float, half_depth: float,
	height: float, ratio: float) -> bpy.types.Object:
	obj = import_mesh(GEN2["round"], name, parent)
	crop_below(obj, 0.34)
	def warp(x: float, y: float, t: float) -> tuple[float, float, float]:
		return (center[0] + x * half_width, center[1] + y * half_depth,
			center[2] + t * height)
	reshape(obj, warp)
	decimate(obj, ratio)
	return obj


def ancient_oak() -> bpy.types.Object:
	root = new_root("lagoon_tree_ancient_oak")
	obj = import_mesh(GEN2["oak"], "ancient_oak_sculpt", root)
	def warp(x: float, y: float, t: float) -> tuple[float, float, float]:
		crown = max(0.0, min(1.0, (t - 0.24) / 0.64))
		width = 2.75 + 1.95 * crown
		depth = 1.45 + 0.75 * crown
		return (x * width + 0.22 * math.sin(t * math.pi * 2.0), y * depth, t * 8.7)
	reshape(obj, warp)
	# Radial stones reinforce the enormous exposed-root footprint without adding
	# a flat front-facing ornament that would fail oblique Mobile views.
	planted_stones(root, 2.10, 7, 0.18)
	return root


def dancing_birch() -> bpy.types.Object:
	root = new_root("lagoon_tree_dancing_birch")
	shared_material: bpy.types.Material | None = None
	for index, (base_x, height, lean, depth_shift) in enumerate((
		(-1.02, 8.15, -0.62, 0.12),
		(0.02, 8.85, 0.08, -0.12),
		(1.04, 7.72, 0.68, 0.10),
	)):
		obj = import_mesh(GEN2["dome"], "birch_sculpt_%02d" % index, root)
		if shared_material is None:
			shared_material = obj.data.materials[0]
		else:
			obj.data.materials[0] = shared_material
		def warp(x: float, y: float, t: float, bx: float = base_x,
				h: float = height, sway: float = lean, dy: float = depth_shift
				) -> tuple[float, float, float]:
			crown = max(0.0, min(1.0, (t - 0.38) / 0.18))
			z = (t / 0.42) * 4.75 if t < 0.42 else 4.75 + ((t - 0.42) / 0.58) * (h - 4.75)
			return (bx + x * (0.30 + 0.70 * crown) + sway * t * t
				+ 0.10 * math.sin(t * math.tau + bx),
				dy + y * (0.34 + 0.46 * crown), z)
		reshape(obj, warp)
		decimate(obj, 0.30)
	planted_stones(root, 1.34, 6, 0.42)
	return root


def umbrella_tree() -> bpy.types.Object:
	root = new_root("lagoon_tree_umbrella")
	obj = import_mesh(GEN2["oak"], "umbrella_sculpt", root)
	def warp(x: float, y: float, t: float) -> tuple[float, float, float]:
		crown = max(0.0, min(1.0, (t - 0.30) / 0.52))
		width = 2.00 + 2.35 * crown
		z = t * 6.25
		if t > 0.56:
			z = 3.50 + (t - 0.56) * 5.60
		return (x * width + 0.82 * t * t - 0.46, y * (1.05 + 0.38 * crown), z)
	reshape(obj, warp)
	planted_stones(root, 1.78, 6, -0.18)
	return root


def blossom_cloud() -> bpy.types.Object:
	root = new_root("lagoon_tree_blossom_cloud")
	obj = import_mesh(GEN2["airy"], "blossom_sculpt", root)
	def warp(x: float, y: float, t: float) -> tuple[float, float, float]:
		crown = max(0.0, min(1.0, (t - 0.26) / 0.66))
		return (x * (1.90 + 1.05 * crown) + 0.28 * math.sin(t * 7.0),
			y * (0.92 + 0.55 * crown), t * 8.15)
	reshape(obj, warp)
	planted_stones(root, 1.45, 5, 0.74)
	return root


def windswept_tree() -> bpy.types.Object:
	root = new_root("lagoon_tree_windswept")
	obj = import_mesh(GEN2["oak"], "windswept_sculpt", root)
	def warp(x: float, y: float, t: float) -> tuple[float, float, float]:
		crown = max(0.0, min(1.0, (t - 0.26) / 0.66))
		sweep = 4.20 * (t ** 1.55)
		return (-1.35 + x * (1.55 + 1.20 * crown) + sweep,
			y * (0.95 + 0.40 * crown), t * 6.85)
	reshape(obj, warp)
	planted_stones(root, 1.58, 6, 0.06)
	return root


def twinheart_tree() -> bpy.types.Object:
	root = new_root("lagoon_tree_twinheart")
	shared_material: bpy.types.Material | None = None
	for index, side in enumerate((-1.0, 1.0)):
		obj = import_mesh(GEN2["airy"], "heart_sculpt_%02d" % index, root)
		if shared_material is None:
			shared_material = obj.data.materials[0]
		else:
			obj.data.materials[0] = shared_material
		def warp(x: float, y: float, t: float, direction: float = side
				) -> tuple[float, float, float]:
			crown = max(0.0, min(1.0, (t - 0.28) / 0.58))
			cleft = direction * (0.16 + 1.28 * (t ** 1.65))
			return (cleft + x * (0.72 + 0.78 * crown),
				y * (0.62 + 0.42 * crown), t * 7.35)
		reshape(obj, warp)
		decimate(obj, 0.34)
	planted_stones(root, 1.54, 7, -0.52)
	return root


def weeping_willow() -> bpy.types.Object:
	root = new_root("lagoon_tree_weeping_willow")
	branch_tube("willow_trunk", [(0.0, 0.0, 0.05), (-0.28, 0.0, 1.75),
		(0.12, 0.0, 3.45), (-0.08, 0.0, 5.15)], 0.58, root)
	for index, (x, y, z) in enumerate(((-3.35, 0.05, 4.55), (-2.05, -0.15, 5.05),
		(-0.75, 0.15, 5.50), (0.75, -0.14, 5.48), (2.05, 0.15, 5.02),
		(3.35, -0.04, 4.52))):
		branch_tube("willow_bough_%02d" % index,
			[(0.0, 0.0, 3.25), (x * 0.46, y, 4.70), (x, y, z)],
			0.25 - 0.018 * abs(index - 2.5), root)
	# One broad high cap and six long, overlapping crown islands form a true
	# hanging curtain.  Each island keeps the approved GEN2 cut planes and UVs;
	# their unequal heights and depth offsets avoid a row of cloned pods.
	cap = willow_crown_piece(root, "willow_high_cap", (0.0, 0.0, 4.75),
		3.55, 1.55, 1.72, 0.18)
	shared_material: bpy.types.Material = cap.data.materials[0]
	for index, (x, y, base, width, drop) in enumerate((
		(-3.18, 0.02, 2.25, 0.86, 2.65), (-2.02, -0.18, 1.78, 1.02, 3.18),
		(-0.78, 0.16, 2.12, 1.06, 3.28), (0.68, -0.14, 2.02, 1.08, 3.34),
		(1.98, 0.18, 1.82, 1.00, 3.12), (3.16, -0.02, 2.28, 0.84, 2.58),
	)):
		curtain = willow_crown_piece(root, "willow_curtain_%02d" % index,
			(x, y, base), width, 0.72, drop, 0.13)
		curtain.data.materials[0] = shared_material
	planted_stones(root, 1.92, 7, 0.25)
	return root


def star(parent: bpy.types.Object, location: tuple[float, float, float], radius: float) -> None:
	outline = []
	for index in range(10):
		angle = math.pi * 0.5 + index * math.pi / 5.0
		r = radius if index % 2 == 0 else radius * 0.43
		outline.append((math.cos(angle) * r, -0.13, math.sin(angle) * r))
	verts = outline + [(x, 0.13, z) for x, _, z in outline]
	faces = [tuple(range(10)), tuple(reversed(range(10, 20)))]
	faces += [(i, (i + 1) % 10, 10 + (i + 1) % 10, 10 + i) for i in range(10)]
	mesh = bpy.data.meshes.new("celebration_star_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new("celebration_star", mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.data.materials.append(material("butter"))
	obj.parent = parent


def celebration_snow() -> bpy.types.Object:
	root = new_root("lagoon_tree_celebration_snow")
	obj = import_mesh(GEN2["snow_pine"], "celebration_pine_sculpt", root)
	def warp(x: float, y: float, t: float) -> tuple[float, float, float]:
		angle = 0.14 * math.sin(t * math.tau * 2.4)
		cosine = math.cos(angle)
		sine = math.sin(angle)
		px = x * 3.05
		py = y * 2.40
		return (px * cosine - py * sine, px * sine + py * cosine, t * 8.25)
	reshape(obj, warp)
	for index, (angle, z, radius, color) in enumerate((
		(0.10, 1.75, 2.46, "coral"), (2.20, 2.45, 2.18, "butter"),
		(4.20, 3.18, 1.92, "coral"), (1.25, 3.90, 1.65, "butter"),
		(3.35, 4.62, 1.40, "coral"), (5.35, 5.30, 1.16, "butter"),
		(2.15, 6.02, 0.88, "coral"), (4.50, 6.62, 0.62, "butter"),
	)):
		ico("pine_ornament_%02d" % index,
			(math.cos(angle) * radius, math.sin(angle) * radius * 0.74, z),
			(0.28, 0.28, 0.28), color, root, 2)
	star(root, (0.0, 0.0, 8.62), 0.66)
	return root


BUILDERS = {
	"lagoon_tree_ancient_oak": ancient_oak,
	"lagoon_tree_dancing_birch": dancing_birch,
	"lagoon_tree_umbrella": umbrella_tree,
	"lagoon_tree_blossom_cloud": blossom_cloud,
	"lagoon_tree_windswept": windswept_tree,
	"lagoon_tree_twinheart": twinheart_tree,
	"lagoon_tree_weeping_willow": weeping_willow,
	"lagoon_tree_celebration_snow": celebration_snow,
}


def descendants(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result.extend(descendants(child))
	return result


def export_asset(name: str, root: bpy.types.Object) -> int:
	bpy.ops.object.select_all(action="DESELECT")
	copies: list[bpy.types.Object] = []
	for source in descendants(root):
		if source.type != "MESH":
			continue
		copy = source.copy()
		copy.data = source.data.copy()
		bpy.context.collection.objects.link(copy)
		copy.parent = None
		copy.matrix_world = source.matrix_world.copy()
		copies.append(copy)
	for copy in copies:
		copy.select_set(True)
		bpy.context.view_layer.objects.active = copy
	bpy.context.view_layer.objects.active = copies[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged["role"] = name
	merged["style_gate"] = "sky_lagoon_tree_gen4"
	merged.data.validate(clean_customdata=True)
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	bpy.ops.export_scene.gltf(filepath=str(OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False, export_cameras=False, export_lights=False,
		export_extras=True)
	bpy.data.objects.remove(merged, do_unlink=True)
	return triangles


ASSETS = {name: builder() for name, builder in BUILDERS.items()}
for asset_name, asset in ASSETS.items():
	triangles = export_asset(asset_name, asset)
	print("SKY_TREE_GEN4|%s|triangles=%d" % (asset_name, triangles))

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
print("SKY_TREE_GEN4|assets|%d" % len(ASSETS))
print("SKY_TREE_GEN4|blend|%s" % BLEND)
