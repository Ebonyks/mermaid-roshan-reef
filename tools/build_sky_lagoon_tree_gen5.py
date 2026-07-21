#!/usr/bin/env python3
"""Build the eight Sky Lagoon GEN5 tree extensions.

GEN5 deliberately stops warping whole GEN2 tree meshes.  The rejected GEN4
runtime captures showed that approach could preserve surface detail while still
collapsing silhouettes into crowns, spikes, or edge-on cards.  This builder
instead authors a different botanical graph for every role: tapered trunks,
visible branch forks, root flares, and volumetric faceted canopy masses.  The
four approved GEN2 trees remain byte-for-byte untouched and ship beside these
extensions.

Usage: blender --background --python tools/build_sky_lagoon_tree_gen5.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit"
BLEND = ROOT / "assets_src" / "blender" / "sky_lagoon_tree_gen5.blend"
OUT.mkdir(parents=True, exist_ok=True)
BLEND.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0

SCULPT_SOURCES = {
	"round": ROOT / "assets" / "props" / "gen2" / "tree_pineroundf.glb",
	"fall": ROOT / "assets" / "props" / "gen2" / "tree_fall.glb",
	"fat": ROOT / "assets" / "props" / "gen2" / "tree_fat.glb",
	"snow_pine": ROOT / "assets" / "northern" / "northern_pine_a.glb",
}
SCULPT_MATERIALS: dict[str, bpy.types.Material] = {}

PALETTE = {
	"ink": (0.055, 0.035, 0.12, 1.0),
	"bark": (0.40, 0.20, 0.16, 1.0),
	"bark_light": (0.69, 0.43, 0.30, 1.0),
	"birch": (0.88, 0.88, 0.79, 1.0),
	"mint": (0.45, 0.82, 0.70, 1.0),
	"mint_hi": (0.66, 0.92, 0.79, 1.0),
	"mint_shadow": (0.31, 0.58, 0.62, 1.0),
	"aqua": (0.34, 0.73, 0.76, 1.0),
	"aqua_hi": (0.57, 0.90, 0.87, 1.0),
	"aqua_shadow": (0.33, 0.43, 0.69, 1.0),
	"coral": (0.91, 0.43, 0.48, 1.0),
	"coral_hi": (1.00, 0.66, 0.62, 1.0),
	"coral_shadow": (0.60, 0.30, 0.55, 1.0),
	"rose": (0.82, 0.48, 0.72, 1.0),
	"rose_hi": (0.96, 0.68, 0.82, 1.0),
	"rose_shadow": (0.52, 0.38, 0.70, 1.0),
	"butter": (0.96, 0.72, 0.29, 1.0),
	"butter_hi": (1.00, 0.86, 0.54, 1.0),
	"butter_shadow": (0.75, 0.43, 0.34, 1.0),
	"snow": (0.91, 0.96, 0.98, 1.0),
	"snow_shadow": (0.68, 0.79, 0.92, 1.0),
	"stone": (0.55, 0.68, 0.75, 1.0),
	"stone_hi": (0.78, 0.86, 0.85, 1.0),
}


def material(name: str) -> bpy.types.Material:
	full_name = "SL_GEN5_" + name
	existing = bpy.data.materials.get(full_name)
	if existing is not None:
		return existing
	mat = bpy.data.materials.new(full_name)
	mat.diffuse_color = PALETTE[name]
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = PALETTE[name]
	bsdf.inputs["Roughness"].default_value = 0.96
	bsdf.inputs["Metallic"].default_value = 0.0
	bsdf.inputs["Specular IOR Level"].default_value = 0.12
	return mat


def new_root(name: str) -> bpy.types.Object:
	root = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(root)
	return root


def import_sculpt(source_key: str, name: str, parent: bpy.types.Object) -> bpy.types.Object:
	before = set(bpy.context.scene.objects)
	bpy.ops.import_scene.gltf(filepath=str(SCULPT_SOURCES[source_key]))
	created = [obj for obj in bpy.context.scene.objects if obj not in before]
	meshes = [obj for obj in created if obj.type == "MESH"]
	if len(meshes) != 1:
		raise RuntimeError("Expected one mesh in %s, found %d" %
			(SCULPT_SOURCES[source_key], len(meshes)))
	obj = meshes[0]
	world = obj.matrix_world.copy()
	obj.parent = None
	obj.data.transform(world)
	obj.matrix_world = Matrix.Identity(4)
	obj.name = name
	obj.data.name = name + "_mesh"
	obj.parent = parent
	if source_key in SCULPT_MATERIALS:
		obj.data.materials[0] = SCULPT_MATERIALS[source_key]
	else:
		SCULPT_MATERIALS[source_key] = obj.data.materials[0]
	for other in created:
		if other != obj:
			bpy.data.objects.remove(other, do_unlink=True)
	return obj


def object_bounds(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	minimum = Vector((1.0e9, 1.0e9, 1.0e9))
	maximum = Vector((-1.0e9, -1.0e9, -1.0e9))
	for vertex in obj.data.vertices:
		for axis in range(3):
			minimum[axis] = min(minimum[axis], vertex.co[axis])
			maximum[axis] = max(maximum[axis], vertex.co[axis])
	return minimum, maximum


def crop_sculpt_below(obj: bpy.types.Object, normalized_height: float) -> None:
	minimum, maximum = object_bounds(obj)
	cutoff = minimum.z + (maximum.z - minimum.z) * normalized_height
	mesh = bmesh.new()
	mesh.from_mesh(obj.data)
	bmesh.ops.delete(mesh, geom=[vertex for vertex in mesh.verts if vertex.co.z < cutoff],
		context="VERTS")
	mesh.to_mesh(obj.data)
	mesh.free()
	obj.data.update()


def decimate_sculpt(obj: bpy.types.Object, ratio: float) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	modifier = obj.modifiers.new("mobile_sculpt_preserve", "DECIMATE")
	modifier.ratio = ratio
	modifier.use_collapse_triangulate = True
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def sculpt_canopy(source_key: str, name: str, center: tuple[float, float, float],
		half_scale: tuple[float, float, float], parent: bpy.types.Object,
		crop: float = 0.34, ratio: float = 0.10, rotation: float = 0.0,
		drift: float = 0.0) -> bpy.types.Object:
	"""Place a rich GEN2 crown fragment on a new authored branch graph."""
	obj = import_sculpt(source_key, name, parent)
	crop_sculpt_below(obj, crop)
	minimum, maximum = object_bounds(obj)
	midpoint = (minimum + maximum) * 0.5
	span = maximum - minimum
	cosine = math.cos(rotation)
	sine = math.sin(rotation)
	for vertex in obj.data.vertices:
		x = (vertex.co.x - midpoint.x) / max(span.x * 0.5, 0.0001)
		y = (vertex.co.y - midpoint.y) / max(span.y * 0.5, 0.0001)
		z = (vertex.co.z - midpoint.z) / max(span.z * 0.5, 0.0001)
		local_x = x * half_scale[0] + drift * (z + 1.0) * 0.5
		local_y = y * half_scale[1]
		vertex.co = (center[0] + local_x * cosine - local_y * sine,
			center[1] + local_x * sine + local_y * cosine,
			center[2] + z * half_scale[2])
	obj.data.update()
	decimate_sculpt(obj, ratio)
	return obj


def sculpt_full(source_key: str, name: str, center: tuple[float, float, float],
		half_scale: tuple[float, float, float], parent: bpy.types.Object,
		ratio: float = 0.34, rotation: float = 0.0) -> bpy.types.Object:
	obj = import_sculpt(source_key, name, parent)
	minimum, maximum = object_bounds(obj)
	midpoint = (minimum + maximum) * 0.5
	span = maximum - minimum
	cosine = math.cos(rotation)
	sine = math.sin(rotation)
	for vertex in obj.data.vertices:
		x = (vertex.co.x - midpoint.x) / max(span.x * 0.5, 0.0001)
		y = (vertex.co.y - midpoint.y) / max(span.y * 0.5, 0.0001)
		z = (vertex.co.z - minimum.z) / max(span.z, 0.0001)
		local_x = x * half_scale[0]
		local_y = y * half_scale[1]
		vertex.co = (center[0] + local_x * cosine - local_y * sine,
			center[1] + local_x * sine + local_y * cosine,
			center[2] + z * half_scale[2] * 2.0)
	obj.data.update()
	decimate_sculpt(obj, ratio)
	return obj


def mesh_object(name: str, vertices: list[tuple[float, float, float]],
		faces: list[tuple[int, ...]], materials: tuple[str, ...],
		parent: bpy.types.Object, material_indices: list[int] | None = None
		) -> bpy.types.Object:
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(vertices, [], faces)
	mesh.validate(clean_customdata=True)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	for mat_name in materials:
		mesh.materials.append(material(mat_name))
	if material_indices is not None:
		for polygon, index in zip(mesh.polygons, material_indices):
			polygon.material_index = index
	return obj


def tapered_branch(name: str, points: list[tuple[float, float, float, float]],
		parent: bpy.types.Object, mat_name: str = "bark", sides: int = 8
		) -> bpy.types.Object:
	"""Create a faceted tube whose final coordinate in each point is radius."""
	centers = [Vector(point[:3]) for point in points]
	vertices: list[tuple[float, float, float]] = []
	previous_u: Vector | None = None
	for index, (center, point) in enumerate(zip(centers, points)):
		if index == 0:
			tangent = centers[1] - center
		elif index == len(centers) - 1:
			tangent = center - centers[index - 1]
		else:
			tangent = centers[index + 1] - centers[index - 1]
		tangent.normalize()
		reference = Vector((0.0, 0.0, 1.0))
		if abs(tangent.dot(reference)) > 0.88:
			reference = Vector((1.0, 0.0, 0.0))
		u = tangent.cross(reference).normalized()
		if previous_u is not None and u.dot(previous_u) < 0.0:
			u.negate()
		previous_u = u.copy()
		v = tangent.cross(u).normalized()
		for side in range(sides):
			angle = math.tau * side / sides
			position = center + point[3] * (math.cos(angle) * u + math.sin(angle) * v)
			vertices.append(tuple(position))
	faces: list[tuple[int, ...]] = []
	for ring in range(len(points) - 1):
		for side in range(sides):
			next_side = (side + 1) % sides
			faces.append((ring * sides + side, ring * sides + next_side,
				(ring + 1) * sides + next_side, (ring + 1) * sides + side))
	faces.append(tuple(reversed(range(sides))))
	last = (len(points) - 1) * sides
	faces.append(tuple(last + side for side in range(sides)))
	return mesh_object(name, vertices, faces, (mat_name,), parent)


def canopy_blob(name: str, center: tuple[float, float, float],
		scale: tuple[float, float, float], colors: tuple[str, str, str],
		parent: bpy.types.Object, seed: float, rotation: float = 0.0,
		rings: int = 6, segments: int = 12) -> bpy.types.Object:
	"""Create one irregular, fully volumetric hand-faceted canopy mass."""
	vertices: list[tuple[float, float, float]] = []
	for ring in range(rings):
		fraction = ring / max(rings - 1, 1)
		latitude = math.pi * fraction
		# Broad terminal rings plus polygon caps make a hand-cut crown instead of
		# the pointy UV-sphere poles that failed the first GEN5 turntable.
		radial = max(0.30, math.sin(latitude) ** 0.78)
		vertical = math.cos(latitude)
		for segment in range(segments):
			angle = math.tau * segment / segments
			lobes = (1.0 + 0.16 * math.sin(angle * 3.0 + seed)
				+ 0.085 * math.cos(angle * 5.0 - seed * 1.7)
				+ 0.055 * math.sin(ring * 2.4 + segment * 1.3 + seed))
			x = radial * math.cos(angle) * scale[0] * lobes
			y = radial * math.sin(angle) * scale[1] * (1.0 + 0.05 * math.sin(angle * 4.0 + seed))
			z = vertical * scale[2]
			# A small ring-dependent drift prevents manufactured symmetry.
			x += 0.10 * scale[0] * math.sin(latitude * 2.0 + seed)
			y += 0.07 * scale[1] * math.cos(latitude * 2.5 - seed)
			cosine = math.cos(rotation)
			sine = math.sin(rotation)
			vertices.append((center[0] + x * cosine - y * sine,
				center[1] + x * sine + y * cosine, center[2] + z))
	faces: list[tuple[int, ...]] = []
	indices: list[int] = []
	for ring in range(rings - 1):
		for segment in range(segments):
			next_segment = (segment + 1) % segments
			faces.append((ring * segments + segment, ring * segments + next_segment,
				(ring + 1) * segments + next_segment, (ring + 1) * segments + segment))
			fraction = (ring + 0.5) / max(rings - 1, 1)
			indices.append(0 if fraction < 0.45 else (1 if fraction < 0.74 else 2))
	faces.append(tuple(reversed(range(segments))))
	indices.append(0)
	last_ring = (rings - 1) * segments
	faces.append(tuple(last_ring + segment for segment in range(segments)))
	indices.append(2)
	return mesh_object(name, vertices, faces, colors, parent, indices)


def root_flare(parent: bpy.types.Object, center: tuple[float, float, float],
		radius: float, count: int, mat_name: str = "bark_light", seed: float = 0.0) -> None:
	for index in range(count):
		angle = math.tau * index / count + seed
		length = radius * (0.78 + 0.18 * math.sin(index * 2.2 + seed))
		start = (center[0], center[1], center[2] + 0.24, 0.34)
		middle = (center[0] + math.cos(angle) * length * 0.44,
			center[1] + math.sin(angle) * length * 0.34, center[2] + 0.10, 0.24)
		end = (center[0] + math.cos(angle) * length,
			center[1] + math.sin(angle) * length * 0.72, center[2] + 0.04, 0.07)
		tapered_branch("root_%02d" % index, [start, middle, end], parent, mat_name, 7)


def stone(name: str, position: tuple[float, float, float],
		scale: tuple[float, float, float], parent: bpy.types.Object, seed: float) -> None:
	canopy_blob(name, position, scale, ("stone", "stone", "stone"),
		parent, seed, rotation=seed, rings=3, segments=7)


def grounding_stones(parent: bpy.types.Object, radius: float, count: int, seed: float) -> None:
	for index in range(count):
		angle = math.tau * index / count + seed
		size = 0.20 + 0.05 * ((index * 5) % 3)
		stone("ground_stone_%02d" % index,
			(math.cos(angle) * radius, math.sin(angle) * radius * 0.64, 0.10),
			(size * 1.35, size, size * 0.60), parent, seed + index)


def ancient_oak() -> bpy.types.Object:
	root = new_root("lagoon_tree_ancient_oak")
	tapered_branch("oak_trunk", [(0.0, 0.0, 0.02, 0.92), (-0.25, 0.08, 1.70, 0.82),
		(0.02, 0.02, 3.18, 0.68), (-0.08, 0.0, 4.20, 0.52)], root, "bark_light", 10)
	for index, points in enumerate((
		[(-0.05, 0.02, 2.55, 0.62), (-1.35, 0.20, 3.85, 0.43), (-2.55, 0.34, 5.10, 0.20)],
		[(0.02, 0.02, 2.85, 0.58), (1.38, -0.20, 4.05, 0.42), (2.75, -0.34, 5.18, 0.19)],
		[(-0.02, 0.0, 3.35, 0.48), (-0.78, -0.18, 4.72, 0.32), (-0.55, -0.34, 5.82, 0.15)],
		[(0.02, 0.0, 3.42, 0.46), (0.72, 0.22, 4.78, 0.31), (0.48, 0.40, 5.90, 0.14)],
	)):
		tapered_branch("oak_branch_%02d" % index, points, root, "bark", 8)
	for index, (position, scale, seed) in enumerate((
		((-3.05, 0.36, 5.72), (1.95, 1.30, 1.02), 0.4),
		((-1.72, -0.40, 6.38), (2.02, 1.42, 1.14), 1.3),
		((0.02, 0.25, 6.78), (2.10, 1.48, 1.20), 2.2),
		((1.72, -0.34, 6.40), (2.00, 1.40, 1.12), 3.1),
		((3.10, 0.32, 5.76), (1.88, 1.28, 1.02), 4.0),
		((-0.95, 0.72, 5.76), (1.68, 1.22, 1.02), 5.1),
		((1.02, -0.78, 5.72), (1.66, 1.20, 1.00), 6.0),
	)):
		sculpt_canopy("round", "oak_crown_%02d" % index, position, scale,
			root, crop=0.33, ratio=0.105, rotation=seed * 0.17)
	root_flare(root, (0.0, 0.0, 0.0), 2.55, 8, "bark_light", 0.17)
	grounding_stones(root, 2.72, 7, 0.28)
	return root


def birch_band(parent: bpy.types.Object, x: float, y: float, z: float,
		radius: float, lean: float, index: int) -> None:
	tapered_branch("birch_band_%02d" % index,
		[(x, y, z - 0.055, radius), (x + lean * 0.015, y, z + 0.055, radius)],
		parent, "ink", 8)


def dancing_birch() -> bpy.types.Object:
	root = new_root("lagoon_tree_dancing_birch")
	trunks = (
		(-1.10, -0.06, -0.58, 7.10),
		(0.00, 0.18, 0.10, 7.85),
		(1.08, -0.12, 0.62, 6.90),
	)
	for index, (base_x, base_y, lean, height) in enumerate(trunks):
		path = [(base_x, base_y, 0.02, 0.34),
			(base_x + lean * 0.18, base_y, 2.35, 0.30),
			(base_x + lean * 0.52, base_y + 0.08 * (-1) ** index, 4.65, 0.23),
			(base_x + lean, base_y, height - 1.0, 0.11)]
		tapered_branch("birch_trunk_%02d" % index, path, root, "birch", 8)
		for band_index, z in enumerate((1.15, 2.05, 3.02, 3.92)):
			x = base_x + lean * (z / height) ** 1.3
			birch_band(root, x, base_y, z, 0.355 - z * 0.025, lean,
				index * 10 + band_index)
		fork_x = base_x + lean * 0.62
		fork_z = height - 2.20
		for fork_index, direction in enumerate((-1.0, 1.0)):
			tapered_branch("birch_fork_%02d_%02d" % (index, fork_index),
				[(fork_x, base_y, fork_z, 0.18),
					(fork_x + direction * 0.62, base_y + direction * 0.18,
						height - 0.72, 0.07)], root, "birch", 7)
		sculpt_canopy("fat", "birch_crown_%02d_a" % index,
			(base_x + lean + (-0.30 if index == 0 else 0.0), base_y, height),
			(1.20, 0.95, 1.15), root, crop=0.31, ratio=0.12,
			rotation=0.16 * index)
		sculpt_canopy("fat", "birch_crown_%02d_b" % index,
			(base_x + lean + (0.72 if index != 2 else -0.68), base_y + 0.18, height - 0.48),
			(0.95, 0.80, 0.88), root, crop=0.34, ratio=0.10,
			rotation=-0.18 * (index + 1))
	root_flare(root, (0.0, 0.0, 0.0), 1.95, 7, "birch", 0.40)
	grounding_stones(root, 2.05, 6, 0.68)
	return root


def umbrella_tree() -> bpy.types.Object:
	root = new_root("lagoon_tree_umbrella")
	tapered_branch("umbrella_trunk", [(-0.30, 0.0, 0.02, 0.62), (-0.52, 0.04, 1.70, 0.54),
		(-0.18, 0.0, 3.18, 0.40), (0.20, 0.04, 4.38, 0.24)], root, "bark_light", 9)
	for index, points in enumerate((
		[(-0.22, 0.0, 2.92, 0.38), (-1.45, 0.18, 4.00, 0.24), (-2.20, 0.18, 4.70, 0.10)],
		[(-0.05, 0.0, 3.25, 0.34), (1.20, -0.20, 4.28, 0.22), (2.05, -0.18, 4.90, 0.09)],
		[(0.10, 0.02, 3.68, 0.30), (0.65, 0.28, 4.78, 0.16), (0.35, 0.42, 5.45, 0.07)],
	)):
		tapered_branch("umbrella_branch_%02d" % index, points, root, "bark", 8)
	for index, (position, scale, seed) in enumerate((
		((-2.05, 0.18, 5.05), (2.12, 1.32, 0.70), 0.7),
		((0.05, 0.28, 5.60), (2.55, 1.55, 0.78), 2.1),
		((2.18, -0.22, 5.18), (2.04, 1.30, 0.68), 3.8),
	)):
		sculpt_canopy("round", "umbrella_crown_%02d" % index, position, scale,
			root, crop=0.36, ratio=0.115, rotation=0.12 * index,
			drift=0.12 * (-1) ** index)
	root_flare(root, (-0.30, 0.0, 0.0), 1.90, 7, "bark_light", -0.16)
	grounding_stones(root, 2.02, 6, 0.12)
	return root


def blossom_cloud() -> bpy.types.Object:
	root = new_root("lagoon_tree_blossom_cloud")
	tapered_branch("blossom_trunk", [(0.0, 0.0, 0.02, 0.70), (0.24, 0.08, 1.55, 0.62),
		(-0.18, 0.0, 3.05, 0.49), (0.10, -0.04, 4.10, 0.36)], root, "bark_light", 9)
	tips = [
		(-2.65, 0.26, 5.25), (-1.70, -0.48, 6.30), (-0.48, 0.42, 7.05),
		(0.78, -0.46, 6.72), (1.86, 0.52, 6.12), (2.82, -0.18, 5.22),
		(0.20, 0.72, 5.62),
	]
	for index, tip in enumerate(tips):
		start_x = -0.06 if tip[0] < 0.0 else 0.08
		start_z = 3.18 + min(abs(tip[0]) * 0.12, 0.50)
		middle = (tip[0] * 0.54, tip[1] * 0.40, (start_z + tip[2]) * 0.52, 0.24)
		tapered_branch("blossom_branch_%02d" % index,
			[(start_x, 0.0, start_z, 0.36), middle, (tip[0], tip[1], tip[2] - 0.30, 0.08)],
			root, "bark", 7)
	for index, tip in enumerate(tips):
		scale = (1.12 + 0.14 * (index % 2), 0.94 + 0.08 * (index % 3),
			0.92 + 0.12 * ((index + 1) % 2))
		sculpt_canopy("fall", "blossom_cluster_%02d" % index, tip, scale,
			root, crop=0.42, ratio=0.070, rotation=index * 0.31)
	root_flare(root, (0.0, 0.0, 0.0), 2.15, 7, "bark_light", 0.52)
	grounding_stones(root, 2.28, 6, 0.22)
	return root


def windswept_tree() -> bpy.types.Object:
	root = new_root("lagoon_tree_windswept")
	tapered_branch("windswept_trunk", [(0.0, 0.0, 0.02, 0.74), (-0.52, 0.08, 1.30, 0.66),
		(-1.15, 0.02, 2.62, 0.54), (-1.32, -0.08, 3.92, 0.40),
		(-0.72, 0.0, 4.90, 0.24)], root, "bark_light", 9)
	for index, points in enumerate((
		[(-1.15, 0.0, 3.10, 0.46), (0.30, 0.32, 4.05, 0.30), (2.05, 0.38, 4.72, 0.11)],
		[(-1.12, -0.04, 3.65, 0.42), (0.65, -0.36, 4.80, 0.27), (3.12, -0.44, 5.32, 0.10)],
		[(-0.78, 0.0, 4.38, 0.34), (1.10, 0.12, 5.35, 0.22), (4.02, 0.18, 5.72, 0.08)],
	)):
		tapered_branch("windswept_branch_%02d" % index, points, root, "bark", 8)
	for index, (position, scale, seed) in enumerate((
		((0.10, 0.32, 4.72), (1.85, 1.12, 0.78), 0.8),
		((1.88, -0.38, 5.32), (2.22, 1.20, 0.82), 2.2),
		((3.92, 0.20, 5.76), (2.05, 1.14, 0.74), 3.6),
		((5.28, -0.18, 5.48), (1.52, 1.02, 0.66), 5.0),
	)):
		sculpt_canopy("round", "windswept_crown_%02d" % index, position, scale,
			root, crop=0.37, ratio=0.105, rotation=0.04, drift=0.42)
	root_flare(root, (0.0, 0.0, 0.0), 2.30, 7, "bark_light", 2.62)
	for index, (position, scale) in enumerate((
		((-1.55, 0.22, 0.24), (0.65, 0.48, 0.34)),
		((-0.78, -0.46, 0.19), (0.48, 0.36, 0.28)),
		((0.92, 0.40, 0.18), (0.44, 0.34, 0.26)),
	)):
		stone("cliff_stone_%02d" % index, position, scale, root, 1.4 + index)
	return root


def twinheart_tree() -> bpy.types.Object:
	root = new_root("lagoon_tree_twinheart")
	left = [(-0.34, 0.05, 0.02, 0.46), (-0.78, 0.10, 1.45, 0.39),
		(0.28, 0.02, 2.85, 0.31), (-0.74, 0.08, 4.22, 0.18),
		(-1.28, 0.16, 5.12, 0.08)]
	right = [(0.34, -0.05, 0.02, 0.46), (0.76, -0.10, 1.45, 0.39),
		(-0.26, -0.02, 2.85, 0.31), (0.72, -0.08, 4.22, 0.18),
		(1.28, -0.16, 5.12, 0.08)]
	tapered_branch("heart_trunk_left", left, root, "bark_light", 9)
	tapered_branch("heart_trunk_right", right, root, "bark", 9)
	for side, x in ((-1.0, -1.65), (1.0, 1.65)):
		for fork_index, direction in enumerate((-1.0, 1.0)):
			tapered_branch("heart_fork_%s_%02d" % ("l" if side < 0 else "r", fork_index),
				[(side * 0.66, 0.0, 4.05, 0.20),
					(x + direction * 0.58, direction * 0.22, 5.50, 0.08)],
				root, "bark" if side > 0 else "bark_light", 7)
	for index, (position, scale, seed) in enumerate((
		((-2.18, 0.20, 6.05), (1.20, 1.00, 1.16), 0.8),
		((-1.10, -0.16, 6.12), (1.18, 1.00, 1.18), 1.7),
		((-1.64, 0.04, 5.32), (1.05, 0.92, 1.12), 2.5),
		((1.10, 0.16, 6.12), (1.18, 1.00, 1.18), 3.4),
		((2.18, -0.20, 6.05), (1.20, 1.00, 1.16), 4.3),
		((1.64, -0.04, 5.32), (1.05, 0.92, 1.12), 5.2),
	)):
		sculpt_canopy("fall", "heart_crown_%02d" % index, position, scale,
			root, crop=0.43, ratio=0.075, rotation=0.18 * (-1) ** index)
	root_flare(root, (0.0, 0.0, 0.0), 1.95, 7, "bark_light", -0.36)
	grounding_stones(root, 2.08, 6, 0.34)
	return root


def weeping_willow() -> bpy.types.Object:
	root = new_root("lagoon_tree_weeping_willow")
	tapered_branch("willow_trunk", [(0.0, 0.0, 0.02, 0.78), (-0.42, 0.06, 1.55, 0.68),
		(0.18, 0.0, 3.12, 0.54), (-0.10, -0.04, 4.58, 0.36),
		(0.26, 0.0, 5.55, 0.20)], root, "bark_light", 10)
	for index, (x, y, z) in enumerate((
		(-3.25, 0.18, 5.45), (-2.08, -0.50, 6.08), (-0.82, 0.56, 6.48),
		(0.82, -0.54, 6.52), (2.12, 0.50, 6.02), (3.28, -0.16, 5.42),
	)):
		tapered_branch("willow_bough_%02d" % index,
			[(0.0, 0.0, 3.58, 0.39), (x * 0.46, y * 0.45, 5.15, 0.24),
				(x, y, z, 0.08)], root, "bark", 7)
	for index, (position, scale, seed) in enumerate((
		((-2.65, 0.20, 6.05), (1.65, 1.22, 0.88), 0.7),
		((-1.12, -0.42, 6.64), (1.75, 1.28, 0.94), 1.8),
		((0.58, 0.36, 6.78), (1.82, 1.32, 0.96), 2.9),
		((2.28, -0.24, 6.12), (1.70, 1.24, 0.90), 4.0),
	)):
		sculpt_canopy("round", "willow_cap_%02d" % index, position, scale,
			root, crop=0.36, ratio=0.095, rotation=seed * 0.12)
	curtains = (
		(-3.30, 0.42, 4.45, 1.45, 0.72, 2.10),
		(-2.15, -0.62, 4.05, 1.30, 0.70, 2.35),
		(-0.85, 0.72, 4.35, 1.18, 0.68, 2.55),
		(0.52, -0.76, 4.15, 1.24, 0.70, 2.65),
		(1.82, 0.66, 4.05, 1.28, 0.72, 2.38),
		(3.12, -0.38, 4.42, 1.38, 0.72, 2.08),
	)
	for index, (x, y, z, width, depth, height) in enumerate(curtains):
		sculpt_canopy("round", "willow_curtain_%02d" % index, (x, y, z),
			(width * 0.62, depth, height * 0.58), root, crop=0.31,
			ratio=0.075, rotation=0.16 * (-1) ** index,
			drift=0.10 * (-1) ** index)
	root_flare(root, (0.0, 0.0, 0.0), 2.35, 8, "bark_light", 0.26)
	grounding_stones(root, 2.48, 7, 0.18)
	return root


def conifer_tier(name: str, center_z: float, radius_x: float, radius_y: float,
		height: float, colors: tuple[str, str, str], parent: bpy.types.Object,
		seed: float, segments: int = 12) -> bpy.types.Object:
	levels = ((0.44, 0.12), (0.14, 0.58), (-0.20, 1.00), (-0.46, 0.58))
	vertices: list[tuple[float, float, float]] = []
	for level, (z_fraction, radial) in enumerate(levels):
		for segment in range(segments):
			angle = math.tau * segment / segments
			scallop = 1.0 + 0.09 * math.sin(segment * 3.0 + seed) + 0.04 * ((segment + level) % 2)
			vertices.append((math.cos(angle) * radius_x * radial * scallop,
				math.sin(angle) * radius_y * radial * scallop,
				center_z + z_fraction * height))
	faces: list[tuple[int, ...]] = []
	indices: list[int] = []
	for level in range(len(levels) - 1):
		for segment in range(segments):
			next_segment = (segment + 1) % segments
			faces.append((level * segments + segment, level * segments + next_segment,
				(level + 1) * segments + next_segment, (level + 1) * segments + segment))
			indices.append(0 if level == 0 else (1 if level == 1 else 2))
	faces.append(tuple(reversed(range((len(levels) - 1) * segments, len(levels) * segments))))
	indices.append(2)
	return mesh_object(name, vertices, faces, colors, parent, indices)


def ornament(parent: bpy.types.Object, name: str, position: tuple[float, float, float],
		color: str, size: float = 0.25) -> None:
	canopy_blob(name, position, (size, size, size), (color, color, color),
		parent, position[0] + position[2], rings=3, segments=8)


def star(parent: bpy.types.Object, location: tuple[float, float, float], radius: float) -> None:
	outline: list[tuple[float, float, float]] = []
	for index in range(10):
		angle = math.pi * 0.5 + index * math.pi / 5.0
		r = radius if index % 2 == 0 else radius * 0.43
		outline.append((location[0] + math.cos(angle) * r, location[1] - 0.13,
			location[2] + math.sin(angle) * r))
	vertices = outline + [(x, location[1] + 0.13, z) for x, _, z in outline]
	faces: list[tuple[int, ...]] = [tuple(range(10)), tuple(reversed(range(10, 20)))]
	faces += [(index, (index + 1) % 10, 10 + (index + 1) % 10, 10 + index)
		for index in range(10)]
	mesh_object("celebration_star", vertices, faces, ("butter",), parent)


def celebration_snow() -> bpy.types.Object:
	root = new_root("lagoon_tree_celebration_snow")
	sculpt_full("snow_pine", "celebration_pine_sculpt", (0.0, 0.0, 0.0),
		(3.05, 2.40, 4.00), root, ratio=0.34, rotation=0.05)
	# Large, surface-positioned ornaments remain readable from the gameplay
	# camera instead of disappearing inside the dense approved pine sculpt.
	for index, (position, color) in enumerate((
		((-1.82, -1.76, 1.72), "coral"), ((1.72, -1.70, 2.06), "butter"),
		((-1.46, -1.53, 2.92), "butter"), ((1.30, -1.38, 3.42), "coral"),
		((-1.02, -1.20, 4.22), "coral"), ((0.90, -1.02, 4.72), "butter"),
		((-0.64, -0.82, 5.52), "butter"), ((0.50, -0.70, 6.08), "coral"),
		((0.02, -0.48, 6.72), "butter"),
	)):
		ornament(root, "pine_ornament_%02d" % index, position, color, 0.34)
	star(root, (0.0, 0.0, 8.50), 0.64)
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


def export_asset(name: str, root: bpy.types.Object) -> tuple[int, int]:
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
	merged["style_gate"] = "sky_lagoon_tree_gen5"
	old_materials = list(merged.data.materials)
	unique_materials: list[bpy.types.Material] = []
	material_remap: dict[int, int] = {}
	for old_index, old_material in enumerate(old_materials):
		try:
			new_index = unique_materials.index(old_material)
		except ValueError:
			new_index = len(unique_materials)
			unique_materials.append(old_material)
		material_remap[old_index] = new_index
	new_polygon_materials = [material_remap[polygon.material_index]
		for polygon in merged.data.polygons]
	merged.data.materials.clear()
	for unique_material in unique_materials:
		merged.data.materials.append(unique_material)
	for polygon, new_material_index in zip(merged.data.polygons, new_polygon_materials):
		polygon.material_index = new_material_index
	merged.data.validate(clean_customdata=True)
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	material_count = len(merged.data.materials)
	bpy.ops.export_scene.gltf(filepath=str(OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False, export_cameras=False, export_lights=False,
		export_extras=True)
	bpy.data.objects.remove(merged, do_unlink=True)
	return triangles, material_count


ASSETS = {name: builder() for name, builder in BUILDERS.items()}
for asset_name, asset in ASSETS.items():
	triangle_count, asset_material_count = export_asset(asset_name, asset)
	print("SKY_TREE_GEN5|%s|triangles=%d|materials=%d" %
		(asset_name, triangle_count, asset_material_count))

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
print("SKY_TREE_GEN5|assets|%d" % len(ASSETS))
print("SKY_TREE_GEN5|blend|%s" % BLEND)
