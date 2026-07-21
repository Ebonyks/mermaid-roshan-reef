#!/usr/bin/env python3
"""Build the gen3 Sky Lagoon ancient-oak quality trial.

This is deliberately a one-tree gate.  The earlier procedural family failed
because separate tube branches and shallow canopy bowls read as construction
parts instead of a sculpt.  This pass fuses the complete wood graph into one
organic mesh, preserves the concept's large negative spaces, and layers small
leaf pads over full rounded crown masses.  The remaining seven trees should
only follow if this trial survives multi-angle review.

Usage: blender --background --python tools/build_sky_lagoon_tree_gen3_trial.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit" / "lagoon_tree_ancient_oak.glb"
BLEND = ROOT / "assets_src" / "blender" / "sky_lagoon_tree_gen3_trial.blend"
QA = ROOT / "assets_src" / "blender" / "qa_sky_lagoon_tree_gen3"
for folder in (OUT.parent, BLEND.parent, QA):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"bark": (0.47, 0.25, 0.17, 1.0),
	"bark_light": (0.70, 0.44, 0.29, 1.0),
	"bark_shadow": (0.31, 0.20, 0.30, 1.0),
	"ink": (0.09, 0.07, 0.18, 1.0),
	"mint": (0.28, 0.64, 0.47, 1.0),
	"seafoam": (0.45, 0.77, 0.59, 1.0),
	"teal": (0.12, 0.42, 0.40, 1.0),
	"aqua": (0.26, 0.58, 0.64, 1.0),
	"lavender": (0.59, 0.52, 0.78, 1.0),
	"stone": (0.65, 0.79, 0.79, 1.0),
	"stone_light": (0.78, 0.88, 0.84, 1.0),
	"birch": (0.77, 0.75, 0.86, 1.0),
	"coral": (0.88, 0.45, 0.52, 1.0),
	"rose": (0.79, 0.43, 0.66, 1.0),
	"butter": (0.94, 0.72, 0.31, 1.0),
	"snow": (0.88, 0.94, 0.97, 1.0),
	"cream": (0.94, 0.88, 0.73, 1.0),
}


def make_material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("SL_GEN3_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.92
	bsdf.inputs["Metallic"].default_value = 0.0
	bsdf.inputs["Specular IOR Level"].default_value = 0.18
	return mat


MATS = {name: make_material(name, color) for name, color in PALETTE.items()}


def new_root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def sample_polyline(points: list[Vector], radii: list[float], spacing: float) -> list[tuple[Vector, float]]:
	result: list[tuple[Vector, float]] = []
	for segment in range(len(points) - 1):
		start = points[segment]
		end = points[segment + 1]
		length = (end - start).length
		steps = max(2, int(math.ceil(length / spacing)))
		for step in range(steps):
			t = step / steps
			# smoothstep keeps fork junctions broad without pinching midway.
			s = t * t * (3.0 - 2.0 * t)
			result.append((start.lerp(end, t), radii[segment] * (1.0 - s) + radii[segment + 1] * s))
	result.append((points[-1], radii[-1]))
	return result


def add_meta_path(meta: bpy.types.MetaBall, points: list[tuple[float, float, float]],
		radii: list[float], spacing: float = 0.20) -> None:
	for point, radius in sample_polyline([Vector(p) for p in points], radii, spacing):
		element = meta.elements.new()
		element.co = point
		element.radius = radius
		element.stiffness = 2.0


def fused_wood(parent: bpy.types.Object) -> bpy.types.Object:
	"""One watertight wood sculpture: trunk, bough loops, and buttress roots."""
	meta = bpy.data.metaballs.new("ancient_oak_wood_volume")
	meta.resolution = 0.105
	meta.render_resolution = 0.075
	meta.threshold = 0.68

	# The front graph intentionally reconnects at the outer branches.  Those
	# reconnections create three child-readable windows rather than decorative
	# holes booleaned into a flat trunk.
	paths: list[tuple[list[tuple[float, float, float]], list[float]]] = [
		# central twisting spine
		([(0.00, 0.00, 0.15), (-0.18, 0.02, 1.45), (0.10, 0.02, 2.85),
		  (-0.28, 0.00, 4.10), (0.12, 0.00, 5.40), (0.55, 0.00, 6.25)],
		 [1.05, 0.96, 0.84, 0.70, 0.48, 0.22]),
		# left low sweep
		([(-0.08, 0.02, 1.15), (-1.20, 0.00, 1.75), (-2.20, 0.02, 2.65),
		  (-3.25, 0.00, 3.65), (-4.20, 0.00, 4.45)],
		 [0.72, 0.61, 0.47, 0.30, 0.13]),
		# left high arch returning into the crown support
		([(-0.10, 0.00, 2.80), (-1.18, 0.00, 3.62), (-1.95, 0.00, 4.75),
		  (-1.52, 0.00, 5.62), (-0.50, 0.00, 5.95)],
		 [0.62, 0.51, 0.35, 0.24, 0.13]),
		# left outer bridge closes a generous circular window
		([(-2.20, 0.00, 2.65), (-2.82, 0.00, 3.72), (-2.65, 0.00, 4.72),
		  (-1.95, 0.00, 4.75)],
		 [0.42, 0.32, 0.24, 0.18]),
		# right low sweep
		([(0.05, 0.02, 1.05), (1.08, 0.00, 1.55), (2.05, 0.00, 2.40),
		  (3.05, 0.00, 3.58), (4.22, 0.00, 4.48)],
		 [0.75, 0.62, 0.48, 0.31, 0.13]),
		# right high arch
		([(0.03, 0.00, 3.00), (1.10, 0.00, 3.85), (1.82, 0.00, 5.02),
		  (1.42, 0.00, 5.92), (0.55, 0.00, 6.25)],
		 [0.61, 0.50, 0.35, 0.23, 0.15]),
		# right outer bridge closes a second distinct window
		([(2.05, 0.00, 2.40), (2.72, 0.00, 3.45), (2.62, 0.00, 4.48),
		  (1.82, 0.00, 5.02)],
		 [0.42, 0.32, 0.24, 0.18]),
		# top crown beams
		([(-1.95, 0.00, 4.75), (-2.75, 0.05, 5.58), (-3.62, 0.12, 6.02)],
		 [0.31, 0.21, 0.10]),
		([(1.82, 0.00, 5.02), (2.72, -0.02, 5.62), (3.62, 0.08, 6.02)],
		 [0.31, 0.21, 0.10]),
		([(-0.50, 0.00, 5.95), (-1.10, 0.05, 6.68), (-1.85, 0.12, 7.12)],
		 [0.28, 0.18, 0.09]),
		([(0.55, 0.00, 6.25), (1.08, -0.04, 6.82), (1.82, 0.10, 7.12)],
		 [0.27, 0.18, 0.09]),
		# rear-depth limbs make oblique views a sculpture, not a facade
		([(-0.05, 0.18, 2.45), (-0.80, 0.82, 3.62), (-1.75, 1.02, 4.62)],
		 [0.48, 0.31, 0.10]),
		([(0.08, -0.16, 2.65), (0.88, -0.82, 3.85), (1.92, -1.02, 4.82)],
		 [0.46, 0.29, 0.10]),
		([(-0.12, -0.10, 4.00), (-0.72, -0.72, 5.15), (-1.42, -0.90, 5.92)],
		 [0.34, 0.22, 0.09]),
		([(0.18, 0.10, 4.25), (0.88, 0.72, 5.35), (1.55, 0.92, 6.05)],
		 [0.34, 0.22, 0.09]),
	]
	for points, radii in paths:
		add_meta_path(meta, points, radii)

	# Broad radial buttresses make the tree feel planted from every angle.
	for index in range(12):
		angle = math.tau * index / 12.0 + 0.12 * math.sin(index * 1.9)
		reach = 2.00 + 0.48 * (index % 3)
		add_meta_path(meta, [
			(0.0, 0.0, 0.36),
			(math.cos(angle) * reach * 0.40, math.sin(angle) * reach * 0.40, 0.20),
			(math.cos(angle) * reach, math.sin(angle) * reach, 0.05),
		], [0.70, 0.42, 0.08], 0.16)

	obj = bpy.data.objects.new("ancient_oak_fused_wood", meta)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	obj.name = "ancient_oak_fused_wood"
	obj.data.materials.append(MATS["bark"])
	obj.data.materials.append(MATS["bark_light"])
	obj.data.materials.append(MATS["bark_shadow"])
	# A tiny surface break avoids a balloon finish while keeping the silhouette
	# continuous and low-frequency enough for the Mobile renderer.
	texture = bpy.data.textures.new("ancient_oak_bark_surface", type="CLOUDS")
	texture.noise_scale = 0.42
	texture.noise_depth = 1
	displace = obj.modifiers.new("carved_surface", "DISPLACE")
	displace.texture = texture
	displace.strength = 0.055
	displace.texture_coords = "GLOBAL"
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=displace.name)
	decimate = obj.modifiers.new("mobile_sculpt", "DECIMATE")
	decimate.ratio = 0.32
	bpy.ops.object.modifier_apply(modifier=decimate.name)
	for polygon in obj.data.polygons:
		if polygon.normal.z < -0.32 or polygon.center.y > 0.66:
			polygon.material_index = 2
		elif polygon.normal.x > 0.72 and polygon.center.z > 0.75:
			polygon.material_index = 1
		else:
			polygon.material_index = 0
		polygon.use_smooth = True
	bpy.ops.object.select_all(action="DESELECT")
	return obj


def tube(name: str, points: list[tuple[float, float, float]], radius: float,
		material: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
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
	obj.data.materials.append(material)
	obj.parent = parent
	return obj


def loop_tube(name: str, points: list[tuple[float, float, float]], radius: float,
		material: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	curve_data = bpy.data.curves.new(name + "_curve", "CURVE")
	curve_data.dimensions = "3D"
	curve_data.bevel_depth = radius
	curve_data.bevel_resolution = 1
	spline = curve_data.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, coordinate in zip(spline.bezier_points, points):
		point.co = coordinate
		point.handle_left_type = "AUTO"
		point.handle_right_type = "AUTO"
	spline.use_cyclic_u = True
	obj = bpy.data.objects.new(name, curve_data)
	bpy.context.collection.objects.link(obj)
	obj.data.materials.append(material)
	obj.parent = parent
	return obj


def add_bark_drawing(parent: bpy.types.Object) -> None:
	"""Raised painterly strokes echo the approved gen2 ink without seam clutter."""
	# Surface-color facets on the fused wood now carry the bark rhythm.  Raised
	# line meshes were removed after oblique review exposed their hull outlines
	# as plank-like seams.
	strokes: list[tuple[list[tuple[float, float, float]], float, str]] = []
	for index, (points, radius, mat_name) in enumerate(strokes):
		tube("oak_painted_grain_%02d" % index, points, radius, MATS[mat_name], parent)

	# An asymmetric carved hollow avoids the mechanical portal shape rejected by
	# the first trial while keeping the landmark legible at child-scale distance.
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=(0.02, -0.94, 1.64))
	hollow = bpy.context.active_object
	hollow.name = "oak_hollow"
	hollow.scale = (0.34, 0.065, 0.47)
	hollow.rotation_euler.y = -0.16
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	hollow.data.materials.append(MATS["ink"])
	hollow.parent = parent
	rim_points = []
	for index in range(12):
		angle = math.tau * index / 12.0
		wobble = 1.0 + 0.08 * math.sin(index * 2.4 + 0.5)
		rim_points.append((0.02 + math.cos(angle) * 0.43 * wobble,
			-1.01, 1.64 + math.sin(angle) * 0.58 * wobble))
	loop_tube("oak_hollow_carved_rim", rim_points, 0.050, MATS["bark_light"], parent)


def fused_cloud(name: str, location: tuple[float, float, float],
		scale: tuple[float, float, float], seed: int, parent: bpy.types.Object,
		palette: tuple[str, str, str] = ("mint", "teal", "aqua")) -> bpy.types.Object:
	"""A full 3D scalloped crown, never a cut bowl or pile of spheres."""
	rng = random.Random(seed)
	meta = bpy.data.metaballs.new(name + "_volume")
	meta.resolution = 0.14
	meta.render_resolution = 0.10
	meta.threshold = 0.70
	lobes = [
		(0.00, 0.00, 0.00, 1.00), (-0.56, -0.02, -0.02, 0.76),
		(0.56, 0.02, 0.00, 0.76), (-0.30, 0.05, 0.42, 0.70),
		(0.32, -0.05, 0.43, 0.68), (-0.22, -0.03, -0.42, 0.66),
		(0.24, 0.04, -0.40, 0.64),
	]
	for x, y, z, radius in lobes:
		element = meta.elements.new()
		element.co = (x + rng.uniform(-0.04, 0.04), y + rng.uniform(-0.04, 0.04),
			z + rng.uniform(-0.04, 0.04))
		element.radius = radius * (1.0 + rng.uniform(-0.04, 0.04))
	obj = bpy.data.objects.new(name, meta)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.convert(target="MESH")
	obj = bpy.context.active_object
	obj.name = name
	for vertex in obj.data.vertices:
		vertex.co.x *= scale[0]
		vertex.co.y *= scale[1]
		vertex.co.z *= scale[2]
	obj.data.update()
	for mat_name in palette:
		obj.data.materials.append(MATS[mat_name])
	for polygon in obj.data.polygons:
		# Closely related facet colors retain volume without the dark horizontal
		# cutoff that made the rejected crowns look like bowls.
		if polygon.center.z < -0.30 and polygon.normal.z < 0.15:
			polygon.material_index = 1
		elif (polygon.index + seed) % 23 == 0:
			polygon.material_index = 2
		else:
			polygon.material_index = 0
		polygon.use_smooth = True
	decimate = obj.modifiers.new("cloud_mobile", "DECIMATE")
	decimate.ratio = 0.28
	bpy.ops.object.modifier_apply(modifier=decimate.name)
	obj.parent = parent
	bpy.ops.object.select_all(action="DESELECT")
	return obj


def leaf_pad(name: str, location: tuple[float, float, float], scale: tuple[float, float, float],
		material: bpy.types.Material, parent: bpy.types.Object, rotation: float = 0.0) -> bpy.types.Object:
	# A closed volumetric pad is required by the shared inverted-hull outline.
	# Thin extrusions cause their expanded backface to occlude the painted face.
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=location)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	obj.rotation_euler.y = rotation
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.data.materials.append(material)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	obj.parent = parent
	return obj


def layered_crown(parent: bpy.types.Object) -> None:
	cloud_specs = [
		(-4.28, 0.04, 4.52, 0.86, 0.64, 0.72),
		(-3.95, 0.02, 5.45, 1.15, 0.72, 0.86),
		(-3.42, 0.04, 4.92, 1.00, 0.70, 0.74),
		(-3.10, 0.02, 6.25, 1.35, 0.82, 0.98),
		(-2.00, 0.03, 6.92, 1.43, 0.90, 1.03),
		(-0.72, 0.00, 7.35, 1.52, 0.95, 1.07),
		(0.70, 0.00, 7.38, 1.50, 0.95, 1.06),
		(2.02, 0.02, 6.98, 1.42, 0.90, 1.00),
		(3.18, 0.02, 6.30, 1.32, 0.82, 0.95),
		(3.48, 0.04, 4.98, 0.98, 0.70, 0.74),
		(4.02, 0.02, 5.48, 1.12, 0.72, 0.84),
		(4.30, 0.04, 4.55, 0.84, 0.64, 0.70),
		(-2.62, 0.18, 5.38, 1.12, 0.82, 0.80),
		(-1.35, 0.22, 5.82, 1.22, 0.88, 0.88),
		(0.02, 0.28, 6.02, 1.30, 0.92, 0.90),
		(1.42, 0.20, 5.86, 1.20, 0.86, 0.86),
		(2.70, 0.18, 5.40, 1.08, 0.80, 0.78),
	]
	clouds: list[bpy.types.Object] = []
	for index, (x, y, z, sx, sy, sz) in enumerate(cloud_specs):
		palette = ("seafoam", "teal", "lavender") if index % 4 == 0 else ("mint", "teal", "aqua")
		clouds.append(fused_cloud("oak_crown_%02d" % index, (x, y, z), (sx, sy, sz),
			600 + index, parent, palette))

	# Small front pads provide the hand-layered leaf language seen in the old
	# gen2 oak without making every crown a clone of that source mesh.
	rng = random.Random(711)
	pad_index = 0
	for cloud_index, spec in enumerate(cloud_specs):
		x, _, z, sx, _, sz = spec
		for local_index in range(2):
			angle = math.tau * (local_index / 2.0) + rng.uniform(-0.40, 0.40)
			px = x + math.cos(angle) * sx * rng.uniform(0.34, 0.62)
			pz = z + math.sin(angle) * sz * rng.uniform(0.28, 0.58)
			width = rng.uniform(0.34, 0.52)
			height = width * rng.uniform(0.50, 0.68)
			pad_colors = ("seafoam", "aqua", "mint", "teal")
			mat = MATS[pad_colors[(pad_index + cloud_index) % len(pad_colors)]]
			leaf_pad("oak_leaf_pad_%03d" % pad_index, (px, -0.82, pz),
				(width, 0.20, height), mat, parent, rng.uniform(-0.35, 0.35))
			pad_index += 1



def base_stones(parent: bpy.types.Object) -> None:
	for index, (angle, radius, size) in enumerate(((0.22, 1.55, 0.34), (1.25, 1.58, 0.28),
		(2.25, 1.50, 0.31), (3.48, 1.72, 0.38), (4.55, 1.55, 0.29), (5.48, 1.64, 0.33))):
		bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0,
			location=(math.cos(angle) * radius, math.sin(angle) * radius, 0.18))
		obj = bpy.context.active_object
		obj.name = "oak_root_stone_%02d" % index
		obj.scale = (size * 1.25, size, size * 0.72)
		obj.rotation_euler.z = angle * 0.62
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		obj.data.materials.append(MATS["stone_light"] if index % 2 else MATS["stone"])
		obj.parent = parent


def descendants(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result.extend(descendants(child))
	return result


def export_asset(root: bpy.types.Object) -> int:
	bpy.ops.object.select_all(action="DESELECT")
	copies: list[bpy.types.Object] = []
	for source in descendants(root):
		if source.type not in {"MESH", "CURVE"}:
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
		if copy.type == "CURVE":
			bpy.ops.object.convert(target="MESH")
			copy.select_set(True)
	bpy.context.view_layer.objects.active = copies[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = "lagoon_tree_ancient_oak"
	merged.data.validate(clean_customdata=True)
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	bpy.ops.export_scene.gltf(filepath=str(OUT), export_format="GLB", export_yup=True,
		use_selection=True, export_apply=True, export_materials="EXPORT", export_animations=False,
		export_cameras=False, export_lights=False)
	bpy.data.objects.remove(merged, do_unlink=True)
	return triangles


def main() -> None:
	oak = new_root("lagoon_tree_ancient_oak")
	fused_wood(oak)
	add_bark_drawing(oak)
	layered_crown(oak)

	triangles = export_asset(oak)
	bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
	print("SKY_TREE_GEN3|lagoon_tree_ancient_oak|triangles=%d" % triangles)
	print("SKY_TREE_GEN3|glb|%s" % OUT)
	print("SKY_TREE_GEN3|blend|%s" % BLEND)


if __name__ == "__main__":
	main()
