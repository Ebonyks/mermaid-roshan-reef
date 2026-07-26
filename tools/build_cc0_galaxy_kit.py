#!/usr/bin/env python3
"""Build the original Butterfly World crystal-and-tray kit.

Reconstructs the accepted Codex 2D concept sheets in
`assets_src/concepts/cc0_ocean_replacements_2026-07-22/` as original,
texture-free, Mobile-safe geometry, replacing the last live CC0/CC-BY props in
the Butterfly World and the rainbow kart track (Regen IDs 04-08 of
`CC0_REPLACEMENT_WORKORDER_2026-07-22.md`):

    regen_04_06_crystal_family.png -> crystal1/2/3.glb   (galaxy.gd CRYSTALS)
    regen_07_crystal_castle.png    -> crystal_castle.glb (galaxy.gd CASTLE_GLB)
    regen_08_serving_tray.png      -> tray.glb           (galaxy.gd TRAY_GLB)

Every mesh is original project geometry with embedded matte pastel materials —
no reference sheet is baked in as a runtime texture, no transparency, no
display plinth or baked ground patch (each cluster exposes its own contact
geometry, per the placement-continuity rule).

Run with Blender 4.5+ or the pinned bpy wheel:
    blender --background --python tools/build_cc0_galaxy_kit.py
    python3 tools/build_cc0_galaxy_kit.py        # bpy wheel
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import bpy
from mathutils import Euler, Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "galaxy" / "gen2"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_cc0_galaxy_kit"
BLEND_OUT = SOURCE_OUT / "cc0_galaxy_kit.blend"
METRICS_OUT = QA_OUT / "cc0_galaxy_kit_metrics.csv"
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


# Palette sampled from the accepted concept sheets: opaque cel blocks, two or
# three values per family, aqua/lavender shadow planes, restrained gold.
PALETTE = {
	"aqua": (0.55, 0.86, 0.88, 1.0),
	"aqua_shade": (0.36, 0.72, 0.78, 1.0),
	"aqua_light": (0.75, 0.94, 0.94, 1.0),
	"rose": (0.95, 0.62, 0.78, 1.0),
	"rose_shade": (0.85, 0.45, 0.66, 1.0),
	"rose_light": (0.99, 0.79, 0.87, 1.0),
	"violet": (0.62, 0.53, 0.90, 1.0),
	"violet_shade": (0.48, 0.40, 0.78, 1.0),
	"violet_light": (0.79, 0.74, 0.96, 1.0),
	"pearl": (0.96, 0.94, 0.89, 1.0),
	"pearl_shade": (0.85, 0.83, 0.79, 1.0),
	"pearl_light": (1.0, 0.99, 0.95, 1.0),
	"coral": (0.93, 0.62, 0.60, 1.0),
	"coral_shade": (0.82, 0.47, 0.47, 1.0),
	"ice": (0.60, 0.86, 0.97, 1.0),
	"ice_shade": (0.45, 0.72, 0.92, 1.0),
	"ice_light": (0.86, 0.95, 1.0, 1.0),
	"plum": (0.26, 0.21, 0.36, 1.0),
	"gold": (0.83, 0.66, 0.30, 1.0),
	"lavender_band": (0.66, 0.60, 0.88, 1.0),
	"aqua_band": (0.52, 0.78, 0.86, 1.0),
}


def material(key: str) -> bpy.types.Material:
	color = PALETTE[key]
	mat = bpy.data.materials.new("CC0Gen2_" + key)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.86
	bsdf.inputs["Metallic"].default_value = 0.0
	return mat


MATS = {key: material(key) for key in PALETTE}


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	out = [obj]
	for child in obj.children:
		out.extend(family(child))
	return out


def build_mesh(name: str, verts: list[Vector], faces: list[tuple[list[int], str]],
		parent: bpy.types.Object, location: Vector = Vector((0.0, 0.0, 0.0))) -> bpy.types.Object:
	"""Create one flat-shaded mesh; every face names the palette key it uses."""
	slots: list[str] = []
	for _, key in faces:
		if key not in slots:
			slots.append(key)
	mesh = bpy.data.meshes.new(name)
	mesh.from_pydata([tuple(v) for v in verts], [], [face for face, _ in faces])
	mesh.validate()
	for key in slots:
		mesh.materials.append(MATS[key])
	for poly, (_, key) in zip(mesh.polygons, faces):
		poly.material_index = slots.index(key)
		poly.use_smooth = False
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = location
	obj.parent = parent
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 1) -> bpy.types.Object:
	mod = obj.modifiers.new("storybook_rounding", "BEVEL")
	mod.width = width
	mod.segments = segments
	mod.limit_method = "ANGLE"
	mod.angle_limit = math.radians(35.0)
	apply_modifier(obj, mod)
	return obj


def prim_cylinder(name: str, key: str, parent: bpy.types.Object, location: tuple[float, float, float],
		radius: float, depth: float, vertices: int = 16,
		scale: tuple[float, float, float] = (1.0, 1.0, 1.0),
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
		location=location, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.data.materials.append(MATS[key])
	for poly in obj.data.polygons:
		poly.use_smooth = False
	obj.parent = parent
	return obj


def prim_box(name: str, key: str, parent: bpy.types.Object, location: tuple[float, float, float],
		size: tuple[float, float, float], rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	obj.scale = (size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	obj.data.materials.append(MATS[key])
	for poly in obj.data.polygons:
		poly.use_smooth = False
	obj.parent = parent
	return obj


# ---------------------------------------------------------------------------
# Regen 04-06 — the crystal family
# ---------------------------------------------------------------------------
# One shard = a chunky six-sided prism with a pyramid tip, no transparency and
# no separate rock base: the shard bodies themselves are the contact geometry.

def shard(name: str, parent: bpy.types.Object, base: tuple[float, float, float],
		radius: float, body: float, tip: float, keys: tuple[str, str, str],
		tilt: tuple[float, float] = (0.0, 0.0), spin: float = 0.0) -> bpy.types.Object:
	body_key, shade_key, tip_key = keys
	sides = 6
	verts: list[Vector] = []
	for ring, (height, scale) in enumerate(((0.0, 1.0), (body, 0.88))):
		for i in range(sides):
			ang = spin + (i / sides) * math.tau
			verts.append(Vector((math.cos(ang) * radius * scale, math.sin(ang) * radius * scale, height)))
	apex = len(verts)
	verts.append(Vector((0.0, 0.0, body + tip)))

	faces: list[tuple[list[int], str]] = []
	faces.append(([i for i in range(sides - 1, -1, -1)], shade_key))       # closed base
	for i in range(sides):
		j = (i + 1) % sides
		# alternate the two body values so each shard reads as cel facets
		key = body_key if i % 2 == 0 else shade_key
		faces.append(([i, j, sides + j, sides + i], key))
	for i in range(sides):
		j = (i + 1) % sides
		faces.append(([sides + i, sides + j, apex], tip_key if i % 2 == 0 else body_key))

	obj = build_mesh(name, verts, faces, parent)
	obj.rotation_euler = Euler((math.radians(tilt[0]), math.radians(tilt[1]), 0.0), "XYZ")
	obj.location = Vector(base)
	bpy.context.view_layer.update()
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
	obj.select_set(False)
	return bevel(obj, radius * 0.16)


AQUA = ("aqua", "aqua_shade", "aqua_light")
ROSE = ("rose", "rose_shade", "rose_light")
VIOLET = ("violet", "violet_shade", "violet_light")


def build_crystal1() -> bpy.types.Object:
	"""Low three-point cluster: one dominant aqua spire, rose and violet flanks."""
	grp = root("crystal1")
	shard("c1_main", grp, (0.0, 0.0, 0.0), 0.23, 0.66, 0.52, AQUA, spin=0.12)
	shard("c1_left", grp, (-0.30, 0.05, 0.0), 0.145, 0.34, 0.32, ROSE, tilt=(4.0, -17.0), spin=0.5)
	shard("c1_right", grp, (0.29, -0.04, 0.0), 0.145, 0.30, 0.30, VIOLET, tilt=(-4.0, 16.0), spin=0.9)
	shard("c1_nub", grp, (-0.12, -0.22, 0.0), 0.09, 0.14, 0.19, AQUA, tilt=(12.0, -4.0), spin=0.3)
	return grp


def build_crystal2() -> bpy.types.Object:
	"""Tall asymmetric five-point cluster led by a rose spire."""
	grp = root("crystal2")
	shard("c2_main", grp, (0.02, 0.0, 0.0), 0.20, 0.86, 0.60, ROSE, tilt=(2.0, 4.0), spin=0.2)
	shard("c2_second", grp, (-0.26, 0.06, 0.0), 0.145, 0.52, 0.40, AQUA, tilt=(3.0, -10.0), spin=0.7)
	shard("c2_third", grp, (0.27, 0.02, 0.0), 0.14, 0.44, 0.36, VIOLET, tilt=(-2.0, 12.0), spin=1.1)
	shard("c2_small", grp, (-0.13, 0.24, 0.0), 0.10, 0.22, 0.24, AQUA, tilt=(-12.0, -5.0), spin=0.4)
	shard("c2_tiny", grp, (0.18, 0.22, 0.0), 0.085, 0.16, 0.20, VIOLET, tilt=(-13.0, 7.0), spin=0.9)
	return grp


def build_crystal3() -> bpy.types.Object:
	"""Broad radial cluster: one dominant centre point ringed by short shards."""
	grp = root("crystal3")
	shard("c3_main", grp, (0.0, 0.0, 0.0), 0.22, 0.64, 0.52, AQUA, spin=0.15)
	ring = [
		(0.0, ROSE, 0.145, 0.30, 0.30),
		(0.9, VIOLET, 0.125, 0.26, 0.26),
		(1.8, AQUA, 0.105, 0.20, 0.23),
		(2.7, ROSE, 0.12, 0.23, 0.25),
		(3.6, VIOLET, 0.145, 0.31, 0.30),
		(4.5, AQUA, 0.105, 0.19, 0.22),
		(5.4, ROSE, 0.115, 0.22, 0.24),
	]
	for idx, (ang, keys, radius, body, tip) in enumerate(ring):
		lean = 20.0 + (idx % 3) * 4.0
		px = math.cos(ang) * 0.40
		py = math.sin(ang) * 0.40
		obj = shard("c3_ray_%d" % idx, grp, (px, py, 0.0), radius, body, tip, keys, spin=ang)
		obj.rotation_euler = Euler((math.sin(ang) * math.radians(lean), -math.cos(ang) * math.radians(lean), 0.0), "XYZ")
		bpy.context.view_layer.objects.active = obj
		obj.select_set(True)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
		obj.select_set(False)
	return grp


# ---------------------------------------------------------------------------
# Regen 07 — the crystal castle landmark
# ---------------------------------------------------------------------------

def faceted_spire(name: str, parent: bpy.types.Object, location: tuple[float, float, float],
		radius: float, height: float, sides: int = 8) -> bpy.types.Object:
	"""Gem-cut spire: a short faceted collar under a tall faceted point."""
	collar = height * 0.24
	verts: list[Vector] = []
	for height_z, scale in ((0.0, 1.0), (collar, 0.86)):
		for i in range(sides):
			ang = (i / sides) * math.tau + math.pi / sides
			verts.append(Vector((math.cos(ang) * radius * scale, math.sin(ang) * radius * scale, height_z)))
	apex = len(verts)
	verts.append(Vector((0.0, 0.0, height)))

	facet = ("ice", "ice_shade", "violet_light", "ice_light")
	faces: list[tuple[list[int], str]] = [([i for i in range(sides - 1, -1, -1)], "ice_shade")]
	for i in range(sides):
		j = (i + 1) % sides
		faces.append(([i, j, sides + j, sides + i], facet[i % len(facet)]))
	for i in range(sides):
		j = (i + 1) % sides
		faces.append(([sides + i, sides + j, apex], facet[(i + 2) % len(facet)]))
	return build_mesh(name, verts, faces, parent, Vector(location))


def arch_band(name: str, key: str, parent: bpy.types.Object, centre: tuple[float, float, float],
		outer: float, inner: float, leg: float, thickness: float, segments: int = 10) -> bpy.types.Object:
	"""An extruded door frame: two straight legs closed by a semicircular head."""
	def outline(radius: float) -> list[tuple[float, float]]:
		pts = [(-radius, 0.0), (-radius, leg)]
		for i in range(segments + 1):
			ang = math.pi - (i / segments) * math.pi
			pts.append((math.cos(ang) * radius, leg + math.sin(ang) * radius))
		pts.append((radius, 0.0))
		return pts

	out_pts = outline(outer)
	in_pts = outline(inner)
	half = thickness * 0.5
	verts: list[Vector] = []
	for depth in (-half, half):
		for x, z in out_pts:
			verts.append(Vector((x, depth, z)))
		for x, z in in_pts:
			verts.append(Vector((x, depth, z)))
	count = len(out_pts)
	front_out, front_in = 0, count
	back_out, back_in = count * 2, count * 3

	faces: list[tuple[list[int], str]] = []
	for i in range(count - 1):
		faces.append(([front_out + i, front_out + i + 1, front_in + i + 1, front_in + i], key))
		faces.append(([back_in + i, back_in + i + 1, back_out + i + 1, back_out + i], key))
		faces.append(([back_out + i, back_out + i + 1, front_out + i + 1, front_out + i], key))
		faces.append(([front_in + i, front_in + i + 1, back_in + i + 1, back_in + i], key))
	for lo, hi in ((0, count - 1),):
		faces.append(([front_out + lo, front_in + lo, back_in + lo, back_out + lo], key))
		faces.append(([back_out + hi, back_in + hi, front_in + hi, front_out + hi], key))
	return build_mesh(name, verts, faces, parent, Vector(centre))


def castle_tower(grp: bpy.types.Object, tag: str, x: float, z: float, radius: float,
		wall: float, spire: float, window: bool) -> None:
	prim_cylinder("cc_%s_plinth" % tag, "pearl_shade", grp, (x, z, 0.07), radius + 0.10, 0.14, 20)
	prim_cylinder("cc_%s_wall" % tag, "pearl", grp, (x, z, 0.14 + wall * 0.5), radius, wall, 20)
	prim_cylinder("cc_%s_belt_lo" % tag, "coral", grp, (x, z, 0.20), radius + 0.03, 0.10, 20)
	prim_cylinder("cc_%s_belt_hi" % tag, "coral", grp, (x, z, 0.14 + wall - 0.07), radius + 0.03, 0.13, 20)
	prim_cylinder("cc_%s_cornice" % tag, "coral_shade", grp, (x, z, 0.14 + wall + 0.02), radius + 0.05, 0.06, 20)
	faceted_spire("cc_%s_spire" % tag, grp, (x, z, 0.14 + wall + 0.05), radius + 0.02, spire)
	if window:
		prim_box("cc_%s_window" % tag, "plum", grp, (x, z - radius * 0.97, 0.14 + wall * 0.52),
			(radius * 0.30, 0.06, wall * 0.34))
		prim_cylinder("cc_%s_window_arch" % tag, "plum", grp,
			(x, z - radius * 0.97, 0.14 + wall * 0.52 + wall * 0.17), radius * 0.15, 0.06, 10,
			rotation=(math.radians(90.0), 0.0, 0.0))


def build_crystal_castle() -> bpy.types.Object:
	"""Central keep, two shorter flanking towers, one readable arched door."""
	grp = root("crystal_castle")
	# continuous foundation that ties the three round footprints together
	prim_box("cc_base_link", "pearl_shade", grp, (0.0, 0.0, 0.06), (1.72, 0.72, 0.12))
	castle_tower(grp, "keep", 0.0, 0.0, 0.52, 0.92, 1.15, False)
	castle_tower(grp, "left", -0.86, 0.06, 0.30, 0.60, 0.74, True)
	castle_tower(grp, "right", 0.86, 0.06, 0.30, 0.60, 0.74, True)

	# the arched door: coral frame, recessed plum opening, small shell keystone
	door_z = -0.50
	arch_band("cc_door_frame", "coral", grp, (0.0, door_z - 0.02, 0.14), 0.32, 0.23, 0.34, 0.10)
	# the opening itself sits deeper, so the coral frame reads as a raised lip
	prim_box("cc_door_void", "plum", grp, (0.0, door_z + 0.05, 0.14 + 0.17), (0.46, 0.10, 0.34))
	prim_cylinder("cc_door_void_arch", "plum", grp, (0.0, door_z + 0.05, 0.14 + 0.34), 0.23, 0.10, 14,
		rotation=(math.radians(90.0), 0.0, 0.0))
	prim_cylinder("cc_door_step", "pearl_light", grp, (0.0, door_z - 0.05, 0.16), 0.30, 0.07, 16,
		scale=(1.0, 0.5, 1.0))
	# scalloped shell keystone: a flat three-lobe fan, not a cloud of spheres
	for i, ang in enumerate((-36.0, 0.0, 36.0)):
		prim_cylinder("cc_door_shell_%d" % i, "pearl_light", grp,
			(math.sin(math.radians(ang)) * 0.13, door_z - 0.05,
				0.14 + 0.70 + math.cos(math.radians(ang)) * 0.06),
			0.085, 0.05, 10, scale=(0.55, 1.0, 1.0), rotation=(math.radians(90.0), 0.0, math.radians(ang)))
	prim_cylinder("cc_door_shell_hub", "coral", grp, (0.0, door_z - 0.06, 0.14 + 0.665), 0.06, 0.055, 10,
		rotation=(math.radians(90.0), 0.0, 0.0))
	return grp


# ---------------------------------------------------------------------------
# Regen 08 — the pearl serving tray
# ---------------------------------------------------------------------------

def build_tray() -> bpy.types.Object:
	"""Oval cream tray, gold rim line, aqua/lavender skirt, two loop handles."""
	grp = root("tray")
	segments = 28
	# lathe profile (radius, height) from the accepted side view
	profile = [
		(0.000, 0.075),
		(0.780, 0.075),
		(0.850, 0.105),
		(0.910, 0.255),
		(1.000, 0.270),
		(1.010, 0.240),
		(1.000, 0.205),
		(0.995, 0.170),
		(0.985, 0.060),
		(0.930, 0.015),
		(0.000, 0.000),
	]
	verts: list[Vector] = []
	for radius, height in profile:
		if radius <= 0.0001:
			verts.append(Vector((0.0, 0.0, height)))
			continue
		for i in range(segments):
			ang = (i / segments) * math.tau
			verts.append(Vector((math.cos(ang) * radius, math.sin(ang) * radius * 0.62, height)))
	# index bookkeeping: rings are either a single centre vert or `segments` verts
	starts: list[int] = []
	cursor = 0
	for radius, _ in profile:
		starts.append(cursor)
		cursor += 1 if radius <= 0.0001 else segments

	faces: list[tuple[list[int], str]] = []
	bands = ["pearl_light", "pearl_light", "pearl", "pearl", "gold", "pearl",
		"aqua_band", "lavender_band", "lavender_band", "pearl_shade"]
	for band in range(len(profile) - 1):
		lo, hi = starts[band], starts[band + 1]
		lo_single = profile[band][0] <= 0.0001
		hi_single = profile[band + 1][0] <= 0.0001
		key = bands[band]
		for i in range(segments):
			j = (i + 1) % segments
			if lo_single:
				faces.append(([lo, hi + i, hi + j], key))
			elif hi_single:
				faces.append(([lo + i, lo + j, hi], key))
			else:
				faces.append(([lo + i, lo + j, hi + j, hi + i], key))
	body = build_mesh("tray_body", verts, faces, grp)
	body.select_set(False)

	# loop handles: a flattened ring at each end, half-buried in the rim
	for tag, sign in (("l", -1.0), ("r", 1.0)):
		bpy.ops.mesh.primitive_torus_add(major_radius=0.19, minor_radius=0.065,
			major_segments=14, minor_segments=6,
			location=(sign * 0.99, 0.0, 0.215))
		handle = bpy.context.object
		handle.name = "tray_handle_" + tag
		handle.scale = (1.05, 1.55, 0.40)
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		handle.data.materials.append(MATS["pearl_light"])
		for poly in handle.data.polygons:
			poly.use_smooth = False
		handle.parent = grp
	return grp


ASSETS = [
	("crystal1", build_crystal1(), "crystals"),
	("crystal2", build_crystal2(), "crystals"),
	("crystal3", build_crystal3(), "crystals"),
	("crystal_castle", build_crystal_castle(), "landmark"),
	("tray", build_tray(), "props"),
]


def metrics(obj: bpy.types.Object) -> tuple[int, int, int, Vector]:
	tris = 0
	slots = set()
	islands = 0
	lo = Vector((1e9, 1e9, 1e9))
	hi = Vector((-1e9, -1e9, -1e9))
	for member in family(obj):
		if member.type != "MESH":
			continue
		islands += 1
		mesh = member.data
		for poly in mesh.polygons:
			tris += max(1, len(poly.vertices) - 2)
		for mat in mesh.materials:
			slots.add(mat.name)
		for corner in member.bound_box:
			world = member.matrix_world @ Vector(corner)
			lo = Vector((min(lo.x, world.x), min(lo.y, world.y), min(lo.z, world.z)))
			hi = Vector((max(hi.x, world.x), max(hi.y, world.y), max(hi.z, world.z)))
	return tris, len(slots), islands, hi - lo


def export_asset(name: str, obj: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for member in family(obj):
		member.hide_render = False
		member.hide_viewport = False
		member.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.export_scene.gltf(filepath=str(ASSET_OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False)


rows = []
for asset_name, asset_obj, group in ASSETS:
	export_asset(asset_name, asset_obj)
	tris, slots, islands, dims = metrics(asset_obj)
	rows.append({"asset": asset_name, "group": group, "triangles": tris,
		"material_slots": slots, "mesh_islands": islands,
		"size_x": round(dims.x, 3), "size_y": round(dims.y, 3), "size_z": round(dims.z, 3)})

with METRICS_OUT.open("w", newline="", encoding="utf-8") as handle:
	writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
	writer.writeheader()
	writer.writerows(rows)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))

# ---------------------------------------------------------------------------
# QA: one isolated three-quarter render per asset plus a contact sheet, matching
# the high-key studio used by the other kit builders.
# ---------------------------------------------------------------------------
scene = bpy.context.scene
# Cycles on CPU: the headless bpy wheel has no GL context, so Workbench/EEVEE
# cannot open a display, while a small CPU path-trace renders anywhere.
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.view_settings.view_transform = "Standard"
scene.render.resolution_x = 680
scene.render.resolution_y = 560
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("QA")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.96, 0.94, 0.88, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
bpy.ops.object.light_add(type="SUN", location=(2.0, -3.0, 4.0))
key_light = bpy.context.object
key_light.data.energy = 1.05
key_light.rotation_euler = (math.radians(48.0), 0.0, math.radians(34.0))

bpy.ops.object.camera_add(location=(0.0, 0.0, 0.0))
camera = bpy.context.object
camera.data.type = "ORTHO"
scene.camera = camera


def frame(obj: bpy.types.Object) -> None:
	_, _, _, dims = metrics(obj)
	span = max(dims.x, dims.y, dims.z, 0.2)
	camera.data.ortho_scale = span * 1.9
	centre = Vector((0.0, 0.0, dims.z * 0.5))
	direction = Vector((1.0, -1.6, 0.75)).normalized()
	camera.location = centre + direction * span * 4.0
	camera.rotation_euler = (direction * -1.0).to_track_quat("-Z", "Y").to_euler()


all_objects = [member for _, asset_obj, _ in ASSETS for member in family(asset_obj)]
for asset_name, asset_obj, _ in ASSETS:
	for member in all_objects:
		member.hide_render = member not in family(asset_obj)
	frame(asset_obj)
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
for member in all_objects:
	member.hide_render = False

print("built %d assets into %s" % (len(ASSETS), ASSET_OUT))
