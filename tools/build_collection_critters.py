#!/usr/bin/env python3
"""Build the Critter Book's project-authored, Mobile-safe 3D assets.

Every species is modeled from rounded low-poly primitives and receives an
embedded matte storybook palette.  No external textures or copyrighted source
meshes are used.  The editable source .blend and an overview render are kept
beside the generator for future art passes.

Usage:
  blender --background --python tools/build_collection_critters.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "collectibles"
SOURCE = ROOT / "assets_src" / "blender"
BLEND_OUT = SOURCE / "collection_critters.blend"
QA_OUT = SOURCE / "qa_collection_critters.png"

OUT.mkdir(parents=True, exist_ok=True)
SOURCE.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"navy": (0.08, 0.07, 0.20, 1.0),
	"indigo": (0.22, 0.18, 0.44, 1.0),
	"aqua": (0.25, 0.78, 0.86, 1.0),
	"sky": (0.43, 0.76, 0.96, 1.0),
	"mint": (0.48, 0.88, 0.70, 1.0),
	"seafoam": (0.72, 0.94, 0.84, 1.0),
	"lavender": (0.71, 0.58, 0.91, 1.0),
	"violet": (0.48, 0.33, 0.72, 1.0),
	"coral": (0.97, 0.43, 0.48, 1.0),
	"rose": (0.95, 0.58, 0.75, 1.0),
	"apricot": (0.99, 0.70, 0.40, 1.0),
	"gold": (0.98, 0.82, 0.30, 1.0),
	"cream": (0.98, 0.94, 0.82, 1.0),
	"snow": (0.88, 0.96, 1.0, 1.0),
	"white": (1.0, 1.0, 1.0, 1.0),
	"brown": (0.48, 0.27, 0.20, 1.0),
	"black": (0.025, 0.02, 0.06, 1.0),
}


def material(name: str, rgba: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("Critter_" + name)
	mat.diffuse_color = rgba
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = rgba
	bsdf.inputs["Roughness"].default_value = 0.88
	bsdf.inputs["Metallic"].default_value = 0.0
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def finish(obj: bpy.types.Object, parent: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
	obj.parent = parent
	if obj.type == "MESH":
		obj.data.materials.append(mat)
		for poly in obj.data.polygons:
			poly.use_smooth = True
	return obj


def sphere(
	name: str,
	loc: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	segments: int = 12,
	rings: int = 8,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=1.0, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(obj, parent, mat)


def ico(
	name: str,
	loc: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	subdivisions: int = 2,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1.0, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(obj, parent, mat)


def cone(
	name: str,
	loc: tuple[float, float, float],
	radius: float,
	depth: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	vertices: int = 10,
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0.0, depth=depth, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	return finish(obj, parent, mat)


def cylinder_between(
	name: str,
	a: tuple[float, float, float],
	b: tuple[float, float, float],
	radius: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	vertices: int = 8,
) -> bpy.types.Object:
	from mathutils import Vector

	va = Vector(a)
	vb = Vector(b)
	d = vb - va
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=d.length, location=(va + vb) * 0.5)
	obj = bpy.context.active_object
	obj.name = name
	obj.rotation_mode = "QUATERNION"
	obj.rotation_quaternion = d.to_track_quat("Z", "Y")
	return finish(obj, parent, mat)


def torus(
	name: str,
	loc: tuple[float, float, float],
	major: float,
	minor: float,
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=16, minor_segments=6, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	return finish(obj, parent, mat)


def eye(parent: bpy.types.Object, x: float, y: float, z: float, side: int = 1, scale: float = 1.0) -> None:
	sphere("eye_white", (x, y * side, z), (0.18 * scale, 0.11 * scale, 0.18 * scale), MATS["white"], parent, 8, 6)
	sphere("eye_pupil", (x + 0.08 * scale, y * side + 0.08 * side * scale, z), (0.095 * scale,) * 3, MATS["navy"], parent, 8, 6)


def wing(
	name: str,
	loc: tuple[float, float, float],
	scale: tuple[float, float, float],
	mat: bpy.types.Material,
	parent: bpy.types.Object,
	rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
	obj = ico(name, loc, scale, mat, parent, 2)
	obj.rotation_euler = rotation
	return obj


def fish_model(name: str, colors: tuple[str, str, str], style: str = "fish") -> bpy.types.Object:
	r = root(name)
	primary, accent, pale = (MATS[c] for c in colors)
	if style == "seahorse":
		sphere("head", (0.42, 0.0, 1.0), (0.55, 0.42, 0.52), primary, r)
		cone("snout", (1.05, 0.0, 0.95), 0.16, 0.9, accent, r, (0.0, math.pi / 2.0, 0.0), 8)
		for i in range(5):
			t = float(i) / 4.0
			sphere("tail_%d" % i, (-0.05 - t * 0.55, 0.0, 0.55 - t * 0.85), (0.38 - t * 0.20, 0.28 - t * 0.12, 0.42 - t * 0.18), primary, r, 10, 7)
		torus("curled_tail", (-0.58, 0.0, -0.45), 0.31, 0.10, accent, r, (math.pi / 2.0, 0.0, 0.0))
		wing("fin", (-0.12, -0.30, 0.52), (0.35, 0.07, 0.42), pale, r, (0.25, 0.0, -0.25))
		eye(r, 0.64, 0.35, 1.12, 1, 0.8)
		eye(r, 0.64, 0.35, 1.12, -1, 0.8)
	else:
		body_scale = (1.55, 0.56, 0.86) if style != "minnow" else (1.72, 0.40, 0.56)
		sphere("body", (0.0, 0.0, 0.0), body_scale, primary, r)
		sphere("muzzle", (1.18, 0.0, -0.05), (0.48, 0.47, 0.56), pale, r, 10, 7)
		wing("tail_top", (-1.63, 0.0, 0.42), (0.70, 0.15, 0.55), accent, r, (0.0, -0.32, 0.0))
		wing("tail_bottom", (-1.63, 0.0, -0.42), (0.70, 0.15, 0.55), accent, r, (0.0, 0.32, 0.0))
		wing("fin_top", (-0.30, 0.0, 0.78), (0.65, 0.10, 0.50), accent, r, (0.0, 0.15, 0.0))
		wing("fin_l", (0.20, 0.50, -0.10), (0.62, 0.10, 0.30), accent, r, (0.25, 0.0, -0.35))
		wing("fin_r", (0.20, -0.50, -0.10), (0.62, 0.10, 0.30), accent, r, (-0.25, 0.0, 0.35))
		if style == "angel":
			wing("banner_top", (-0.15, 0.0, 0.98), (0.92, 0.10, 0.95), pale, r)
			wing("banner_bottom", (-0.15, 0.0, -0.78), (0.85, 0.10, 0.70), pale, r)
		for x in (-0.45, 0.18):
			torus("stripe", (x, 0.0, 0.0), 0.62 if style != "minnow" else 0.44, 0.09, accent, r, (0.0, math.pi / 2.0, 0.0))
		eye(r, 1.12, 0.45, 0.24, 1)
		eye(r, 1.12, 0.45, 0.24, -1)
	return r


def insect_model(name: str, colors: tuple[str, str, str], style: str) -> bpy.types.Object:
	r = root(name)
	primary, accent, pale = (MATS[c] for c in colors)
	if style in ("beetle", "ladybug"):
		sphere("body", (0.0, 0.0, 0.30), (0.92, 0.68, 0.43), primary, r)
		sphere("head", (0.82, 0.0, 0.30), (0.42, 0.42, 0.35), MATS["navy"], r)
		cylinder_between("wing_seam", (-0.55, 0.0, 0.66), (0.52, 0.0, 0.67), 0.035, MATS["navy"], r, 6)
		if style == "ladybug":
			for x, y in ((-0.35, 0.35), (0.15, 0.37), (-0.35, -0.35), (0.15, -0.37)):
				sphere("spot", (x, y, 0.64), (0.13, 0.08, 0.08), MATS["navy"], r, 8, 5)
		for i, x in enumerate((-0.45, 0.0, 0.45)):
			for side in (-1, 1):
				cylinder_between("leg_%d_%d" % (i, side), (x, 0.45 * side, 0.25), (x - 0.20, 1.00 * side, 0.02), 0.045, accent, r, 6)
	else:
		sphere("thorax", (0.15, 0.0, 0.25), (0.45, 0.36, 0.38), primary, r)
		sphere("head", (0.68, 0.0, 0.30), (0.34, 0.32, 0.32), MATS["navy"], r)
		if style == "dragonfly":
			for i in range(5):
				sphere("abdomen_%d" % i, (-0.20 - float(i) * 0.35, 0.0, 0.24), (0.28 - float(i) * 0.025, 0.19, 0.19), accent if i % 2 else primary, r, 8, 6)
			for side in (-1, 1):
				wing("wing_%s_front" % ("l" if side > 0 else "r"), (0.12, 0.72 * side, 0.35), (0.72, 0.48, 0.06), pale, r, (0.0, 0.20 * side, 0.30 * side))
				wing("wing_%s_back" % ("l" if side > 0 else "r"), (-0.35, 0.62 * side, 0.32), (0.62, 0.42, 0.06), pale, r, (0.0, -0.15 * side, -0.25 * side))
		elif style == "bee":
			sphere("abdomen", (-0.45, 0.0, 0.25), (0.72, 0.42, 0.42), primary, r)
			for x in (-0.62, -0.30):
				torus("stripe", (x, 0.0, 0.25), 0.41, 0.07, MATS["navy"], r, (0.0, math.pi / 2.0, 0.0))
			for side in (-1, 1):
				wing("wing_%s" % ("l" if side > 0 else "r"), (0.0, 0.48 * side, 0.58), (0.63, 0.38, 0.07), pale, r, (0.15 * side, 0.0, 0.35 * side))
		else:
			cylinder_between("abdomen", (0.0, 0.0, 0.28), (-0.85, 0.0, 0.20), 0.18, accent, r, 8)
			for side in (-1, 1):
				wing("wing_%s_front" % ("l" if side > 0 else "r"), (0.05, 0.62 * side, 0.42), (0.68, 0.62, 0.08), primary, r, (0.0, 0.18 * side, 0.35 * side))
				wing("wing_%s_back" % ("l" if side > 0 else "r"), (-0.45, 0.48 * side, 0.36), (0.52, 0.48, 0.07), pale, r, (0.0, -0.18 * side, -0.25 * side))
	for side in (-1, 1):
		cylinder_between("antenna_%d" % side, (0.82, 0.18 * side, 0.48), (1.20, 0.48 * side, 0.85), 0.035, MATS["navy"], r, 6)
	return r


def bird_model(name: str, colors: tuple[str, str, str], style: str) -> bpy.types.Object:
	r = root(name)
	primary, accent, pale = (MATS[c] for c in colors)
	body_scale = (0.80, 0.68, 1.02) if style == "owl" else (0.95, 0.62, 0.82)
	sphere("body", (0.0, 0.0, 0.70), body_scale, primary, r)
	sphere("belly", (0.42, 0.0, 0.62), (0.63, 0.50, 0.68), pale, r)
	head_scale = (0.68, 0.68, 0.68) if style == "owl" else (0.58, 0.55, 0.58)
	sphere("head", (0.52, 0.0, 1.55), head_scale, primary, r)
	beak_len = 1.15 if style in ("hummingbird", "kingfisher") else 0.55
	cone("beak", (0.98 + beak_len * 0.42, 0.0, 1.50), 0.18 if style != "puffin" else 0.28, beak_len, accent, r, (0.0, math.pi / 2.0, 0.0), 8)
	for side in (-1, 1):
		wing("wing_%s" % ("l" if side > 0 else "r"), (-0.05, 0.62 * side, 0.82), (0.82, 0.22, 0.68), accent, r, (0.0, 0.15 * side, 0.18 * side))
		eye(r, 0.76, 0.48, 1.72, side, 0.82 if style != "owl" else 1.18)
		cylinder_between("leg_%d" % side, (0.12, 0.26 * side, 0.12), (0.12, 0.28 * side, -0.35), 0.055, MATS["brown"], r, 7)
	wing("tail", (-0.88, 0.0, 0.55), (0.72, 0.38, 0.28), accent, r, (0.0, -0.35, 0.0))
	if style == "owl":
		for side in (-1, 1):
			cone("ear_%d" % side, (0.40, 0.36 * side, 2.13), 0.18, 0.48, accent, r, (0.0, 0.0, -0.20 * side), 6)
	if style == "puffin":
		sphere("face_patch", (0.83, 0.0, 1.58), (0.40, 0.48, 0.42), MATS["white"], r)
	return r


SPECIES = [
	("coral_clownfish", "fish", ("coral", "cream", "white"), "fish"),
	("pearl_seahorse", "fish", ("lavender", "rose", "cream"), "seahorse"),
	("rainbow_angelfish", "fish", ("aqua", "gold", "lavender"), "angel"),
	("sky_koi", "fish", ("white", "coral", "cream"), "fish"),
	("cloud_minnow", "fish", ("sky", "snow", "white"), "minnow"),
	("frostfin", "fish", ("snow", "violet", "aqua"), "angel"),
	("coral_ladybug", "insect", ("coral", "navy", "cream"), "ladybug"),
	("blue_dragonfly", "insect", ("aqua", "violet", "seafoam"), "dragonfly"),
	("moon_moth", "insect", ("lavender", "gold", "seafoam"), "moth"),
	("honeybee", "insect", ("gold", "navy", "cream"), "bee"),
	("snow_beetle", "insect", ("snow", "aqua", "lavender"), "beetle"),
	("crystal_butterfly", "insect", ("sky", "violet", "rose"), "moth"),
	("lagoon_bluebird", "bird", ("sky", "indigo", "cream"), "songbird"),
	("ruby_hummingbird", "bird", ("mint", "coral", "cream"), "hummingbird"),
	("river_kingfisher", "bird", ("aqua", "apricot", "cream"), "kingfisher"),
	("cloud_puffin", "bird", ("navy", "coral", "white"), "puffin"),
	("snowy_owl", "bird", ("snow", "lavender", "white"), "owl"),
	("aurora_tern", "bird", ("white", "aqua", "seafoam"), "songbird"),
]


def select_tree(obj: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	for child in obj.children_recursive:
		child.select_set(True)
	bpy.context.view_layer.objects.active = obj


def export(root_obj: bpy.types.Object, filename: str) -> None:
	select_tree(root_obj)
	bpy.ops.export_scene.gltf(
		filepath=str(OUT / filename),
		export_format="GLB",
		use_selection=True,
		export_yup=True,
		export_apply=True,
		export_materials="EXPORT",
		export_animations=False,
		export_cameras=False,
		export_lights=False,
	)


roots: list[bpy.types.Object] = []
for species_name, category, colors, style in SPECIES:
	if category == "fish":
		model = fish_model(species_name, colors, style)
	elif category == "insect":
		model = insect_model(species_name, colors, style)
	else:
		model = bird_model(species_name, colors, style)
	export(model, species_name + ".glb")
	roots.append(model)


# A toy-sized catch net used for the no-fail sweep celebration.
net = root("storybook_catch_net")
cylinder_between("handle", (0.0, 0.0, -1.8), (0.0, 0.0, 1.1), 0.11, MATS["apricot"], net, 10)
torus("hoop", (0.0, 0.0, 1.85), 0.82, 0.09, MATS["violet"], net, (math.pi / 2.0, 0.0, 0.0))
for i in range(-3, 4):
	x = float(i) * 0.20
	h = math.sqrt(max(0.0, 0.70 * 0.70 - x * x))
	cylinder_between("net_v_%d" % i, (x, 0.0, 1.85 - h), (x, 0.0, 1.85 + h), 0.018, MATS["seafoam"], net, 5)
	cylinder_between("net_h_%d" % i, (-h, 0.0, 1.85 + x), (h, 0.0, 1.85 + x), 0.018, MATS["seafoam"], net, 5)
export(net, "catch_net.glb")


# Arrange all editable source models into a tidy overview sheet after export.
for i, model in enumerate(roots):
	model.location = ((i % 6) * 4.8 - 12.0, (i // 6) * 4.6 - 4.6, 0.0)
	if SPECIES[i][1] == "insect":
		model.scale = (1.35,) * 3
net.hide_render = True
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))


# One lightweight QA render makes missing parts or broken skins obvious.
bpy.ops.object.camera_add(location=(0.0, -30.0, 20.0), rotation=(math.radians(60.0), 0.0, 0.0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera
camera.data.type = "ORTHO"
camera.data.ortho_scale = 34.0
bpy.ops.object.light_add(type="AREA", location=(-8.0, -12.0, 22.0))
key = bpy.context.active_object
key.data.energy = 1700.0
key.data.shape = "DISK"
key.data.size = 15.0
bpy.ops.object.light_add(type="AREA", location=(12.0, 2.0, 15.0))
fill = bpy.context.active_object
fill.data.energy = 1000.0
fill.data.size = 12.0
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1200
scene.render.resolution_y = 700
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = True
scene.render.filepath = str(QA_OUT)
scene.view_settings.look = "AgX - Medium High Contrast"
bpy.ops.render.render(write_still=True)

print("COLLECTION_ASSETS|species=%d|out=%s" % (len(SPECIES), OUT))
