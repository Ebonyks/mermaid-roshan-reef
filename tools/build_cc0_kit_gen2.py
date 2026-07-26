#!/usr/bin/env python3
"""Build the original replacements for the last live CC0 kit pieces.

Reconstructs two accepted Codex 2D concept sheets in
`assets_src/concepts/cc0_ocean_replacements_2026-07-22/` as original,
texture-free, Mobile-safe geometry (Regen IDs 29-35 of
`CC0_REPLACEMENT_WORKORDER_2026-07-22.md`):

    regen_29_32_park_and_rooted_hedges.png -> park_bench.glb, park_fountain.glb
    regen_33_35_pearl_furniture.png        -> pearl_bookcase/chair/table.glb

Only the pieces with a verified live `_kit()` call site are modelled. The two
hedge rows on the park sheet have no live call site in the current tree
(`grep '_kit("park/hedge'` is empty; the Sky Lagoon dresses its hedges from its
own authored kit), so they stay concept-only rather than shipping dead art.

Output lands in `assets/props/gen2/`, the shadow folder that `main.gd`'s
`KIT_GEN2` dict checks before the legacy `assets/kits/**` path.

Run with Blender 4.5+ or the pinned bpy wheel:
    blender --background --python tools/build_cc0_kit_gen2.py
    python3 tools/build_cc0_kit_gen2.py        # bpy wheel
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "props" / "gen2"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_cc0_kit_gen2"
BLEND_OUT = SOURCE_OUT / "cc0_kit_gen2.blend"
METRICS_OUT = QA_OUT / "cc0_kit_gen2_metrics.csv"
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


# Palette sampled from the two accepted sheets.
PALETTE = {
	"wood": (0.88, 0.68, 0.38, 1.0),
	"wood_shade": (0.74, 0.53, 0.27, 1.0),
	"wood_light": (0.95, 0.80, 0.53, 1.0),
	"cream": (0.97, 0.93, 0.83, 1.0),
	"cream_shade": (0.88, 0.83, 0.72, 1.0),
	"cream_light": (1.0, 0.98, 0.92, 1.0),
	"stone": (0.93, 0.91, 0.85, 1.0),
	"stone_shade": (0.78, 0.75, 0.68, 1.0),
	"aqua": (0.55, 0.80, 0.84, 1.0),
	"aqua_shade": (0.40, 0.68, 0.74, 1.0),
	"lavender": (0.72, 0.66, 0.88, 1.0),
	"coral": (0.95, 0.52, 0.42, 1.0),
	"berry": (0.62, 0.45, 0.80, 1.0),
	"book_rose": (0.93, 0.55, 0.60, 1.0),
	"book_teal": (0.38, 0.66, 0.68, 1.0),
}


def material(key: str) -> bpy.types.Material:
	color = PALETTE[key]
	mat = bpy.data.materials.new("KitGen2_" + key)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.88
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


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def finish(obj: bpy.types.Object, key: str, parent: bpy.types.Object,
		bevel_width: float = 0.0) -> bpy.types.Object:
	if bevel_width > 0.0:
		mod = obj.modifiers.new("storybook_rounding", "BEVEL")
		mod.width = bevel_width
		mod.segments = 2
		mod.limit_method = "ANGLE"
		mod.angle_limit = math.radians(40.0)
		apply_modifier(obj, mod)
	obj.data.materials.append(MATS[key])
	for poly in obj.data.polygons:
		poly.use_smooth = False
	obj.parent = parent
	return obj


def box(name: str, key: str, parent: bpy.types.Object, location: tuple[float, float, float],
		size: tuple[float, float, float], rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
		bevel_width: float = 0.02) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	obj.scale = (size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(obj, key, parent, bevel_width)


def cylinder(name: str, key: str, parent: bpy.types.Object, location: tuple[float, float, float],
		radius: float, depth: float, vertices: int = 12,
		scale: tuple[float, float, float] = (1.0, 1.0, 1.0),
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
		bevel_width: float = 0.0) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
		location=location, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(obj, key, parent, bevel_width)


def blob(name: str, key: str, parent: bpy.types.Object, location: tuple[float, float, float],
		scale: tuple[float, float, float], rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
		subdivisions: int = 2) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1.0,
		location=location, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(obj, key, parent)


def shell_fan(name: str, parent: bpy.types.Object, hinge: tuple[float, float, float],
		radius: float, lobes: int = 5, key: str = "cream",
		thickness: float = 0.10, spread: float = 46.0) -> None:
	"""The scallop motif the sheets repeat: a fan of rounded lobes on a hinge.

	Stands in the XZ plane (thickness along Y), so it reads as a shell back or
	a fountain spout rather than a disc lying on the floor.
	"""
	for i in range(lobes):
		frac = (i / (lobes - 1)) * 2.0 - 1.0 if lobes > 1 else 0.0
		ang = math.radians(spread) * frac
		length = radius * (1.0 - 0.22 * abs(frac))
		cx = hinge[0] + math.sin(ang) * length * 0.52
		cz = hinge[2] + math.cos(ang) * length * 0.52
		lobe = blob("%s_%d" % (name, i), key, parent, (cx, hinge[1], cz),
			(radius * 0.30, thickness * 0.5, length * 0.52))
		lobe.rotation_euler = (0.0, ang, 0.0)
		bpy.context.view_layer.objects.active = lobe
		lobe.select_set(True)
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
		lobe.select_set(False)
	blob(name + "_hinge", key, parent, hinge, (radius * 0.42, thickness * 0.54, radius * 0.22))


def banded_leg(name: str, parent: bpy.types.Object, x: float, y: float, radius: float,
		height: float, key: str = "cream") -> None:
	"""Every furniture leg on the sheet ends in a lavender then aqua cuff."""
	cylinder(name, key, parent, (x, y, height * 0.5 + 0.10), radius, height, 10)
	cylinder(name + "_band", "lavender", parent, (x, y, 0.10 + height * 0.10), radius * 1.04, height * 0.20, 10)
	cylinder(name + "_foot", "aqua", parent, (x, y, 0.05), radius * 1.06, 0.10, 10)


# ---------------------------------------------------------------------------
# Regen 29 — the park bench (aqua cast-iron ends, warm plank seat and back)
# ---------------------------------------------------------------------------

def build_park_bench() -> bpy.types.Object:
	grp = root("park_bench")
	for tag, sx in (("l", -0.86), ("r", 0.86)):
		frame = "bench_%s" % tag
		box(frame + "_front_leg", "aqua", grp, (sx, -0.19, 0.22), (0.10, 0.12, 0.44), bevel_width=0.03)
		box(frame + "_rear_leg", "aqua", grp, (sx, 0.17, 0.20), (0.10, 0.12, 0.40), bevel_width=0.03)
		box(frame + "_foot", "aqua", grp, (sx, -0.01, 0.04), (0.11, 0.56, 0.08), bevel_width=0.03)
		box(frame + "_apron", "aqua", grp, (sx, 0.0, 0.40), (0.09, 0.52, 0.10), bevel_width=0.03)
		# the scrolled arm and the back upright that the planks bolt onto
		box(frame + "_post", "aqua", grp, (sx, 0.20, 0.70), (0.09, 0.11, 0.62),
			rotation=(math.radians(-9.0), 0.0, 0.0), bevel_width=0.03)
		cylinder(frame + "_scroll", "aqua", grp, (sx, -0.20, 0.50), 0.10, 0.09, 12,
			rotation=(0.0, math.radians(90.0), 0.0))
		cylinder(frame + "_scroll_eye", "cream", grp, (sx * 1.03, -0.20, 0.50), 0.035, 0.10, 8,
			rotation=(0.0, math.radians(90.0), 0.0))
		for i, bz in enumerate((0.18, 0.30)):
			cylinder("%s_bolt_%d" % (frame, i), "cream", grp, (sx * 1.02, 0.0, bz), 0.03, 0.09, 8,
				rotation=(0.0, math.radians(90.0), 0.0))
	for i, py in enumerate((-0.20, -0.02, 0.16)):
		box("bench_seat_%d" % i, "wood" if i % 2 == 0 else "wood_shade", grp,
			(0.0, py, 0.47), (1.86, 0.16, 0.07), bevel_width=0.02)
	for i, (pz, py) in enumerate(((0.66, 0.229), (0.84, 0.200), (1.02, 0.172))):
		box("bench_back_%d" % i, "wood" if i % 2 == 0 else "wood_shade", grp,
			(0.0, py, pz), (1.86, 0.07, 0.14), rotation=(math.radians(-9.0), 0.0, 0.0),
			bevel_width=0.02)
	return grp


# ---------------------------------------------------------------------------
# Regen 30 — the scallop-shell park fountain
# ---------------------------------------------------------------------------

def build_park_fountain() -> bpy.types.Object:
	grp = root("park_fountain")
	# basin: a banded stone ring on four rounded feet, open at the top
	segments = 22
	profile = [
		(0.62, 0.18),   # inner floor edge
		(0.66, 0.16),
		(0.80, 0.16),
		(0.86, 0.56),   # inner wall
		(1.00, 0.58),   # rim
		(1.02, 0.42),
		(0.98, 0.24),
		(0.90, 0.13),
		(0.00, 0.13),   # underside
	]
	bands = ["stone_shade", "stone_shade", "stone", "stone_shade", "stone", "stone", "stone_shade", "stone_shade"]
	verts: list[Vector] = []
	starts: list[int] = []
	cursor = 0
	for radius, height in profile:
		starts.append(cursor)
		if radius <= 0.0001:
			verts.append(Vector((0.0, 0.0, height)))
			cursor += 1
			continue
		for i in range(segments):
			ang = (i / segments) * math.tau
			verts.append(Vector((math.cos(ang) * radius, math.sin(ang) * radius, height)))
		cursor += segments
	faces: list[tuple[list[int], str]] = []
	for band in range(len(profile) - 1):
		lo, hi = starts[band], starts[band + 1]
		hi_single = profile[band + 1][0] <= 0.0001
		for i in range(segments):
			j = (i + 1) % segments
			if hi_single:
				faces.append(([lo + i, lo + j, hi], bands[band]))
			else:
				faces.append(([lo + i, lo + j, hi + j, hi + i], bands[band]))
	slots: list[str] = []
	for _, key in faces:
		if key not in slots:
			slots.append(key)
	mesh = bpy.data.meshes.new("fountain_basin")
	mesh.from_pydata([tuple(v) for v in verts], [], [face for face, _ in faces])
	mesh.validate()
	for key in slots:
		mesh.materials.append(MATS[key])
	for poly, (_, key) in zip(mesh.polygons, faces):
		poly.material_index = slots.index(key)
		poly.use_smooth = False
	basin = bpy.data.objects.new("fountain_basin", mesh)
	bpy.context.collection.objects.link(basin)
	basin.parent = grp
	# floor inside the ring, and the four little stone feet from the side view
	cylinder("fountain_floor", "stone_shade", grp, (0.0, 0.0, 0.17), 0.66, 0.06, segments)
	for i in range(4):
		ang = math.pi * 0.25 + i * math.pi * 0.5
		blob("fountain_foot_%d" % i, "stone", grp,
			(math.cos(ang) * 0.72, math.sin(ang) * 0.72, 0.06), (0.14, 0.14, 0.07))
	# the standing scallop centrepiece
	cylinder("fountain_shell_base", "stone", grp, (0.0, 0.06, 0.26), 0.26, 0.22, 12, scale=(1.0, 0.7, 1.0))
	shell_fan("fountain_shell", grp, (0.0, 0.06, 0.40), 0.92, 5, "stone", 0.20, 52.0)
	return grp


# ---------------------------------------------------------------------------
# Regen 33-35 — the pearl castle furniture family
# ---------------------------------------------------------------------------

def build_pearl_bookcase() -> bpy.types.Object:
	grp = root("pearl_bookcase")
	box("case_back", "cream", grp, (0.0, 0.19, 0.66), (1.32, 0.08, 0.96), bevel_width=0.03)
	box("case_floor", "cream_shade", grp, (0.0, 0.0, 0.22), (1.32, 0.44, 0.10), bevel_width=0.03)
	for tag, sx in (("l", -0.66), ("r", 0.66)):
		box("case_post_" + tag, "wood", grp, (sx, 0.0, 0.70), (0.14, 0.44, 1.02), bevel_width=0.05)
		blob("case_finial_" + tag, "cream_light", grp, (sx, 0.0, 1.25), (0.15, 0.15, 0.15))
		banded_leg("case_leg_" + tag + "_f", grp, sx, -0.15, 0.10, 0.16, "cream")
		banded_leg("case_leg_" + tag + "_b", grp, sx, 0.15, 0.10, 0.16, "cream")
	for i, sz in enumerate((0.62, 1.02)):
		box("case_shelf_%d" % i, "wood_light", grp, (0.0, -0.01, sz), (1.24, 0.42, 0.07), bevel_width=0.02)
	box("case_rail_lo", "wood", grp, (0.0, -0.21, 0.66), (1.24, 0.06, 0.09), bevel_width=0.02)
	box("case_rail_hi", "wood", grp, (0.0, -0.21, 1.06), (1.24, 0.06, 0.09), bevel_width=0.02)
	# scalloped crest board with the coral shell medallion
	box("case_crest", "cream", grp, (0.0, 0.10, 1.28), (1.10, 0.14, 0.16), bevel_width=0.05)
	blob("case_crest_arc", "cream", grp, (0.0, 0.10, 1.34), (0.42, 0.07, 0.12))
	shell_fan("case_crest_shell", grp, (0.0, 0.02, 1.33), 0.22, 4, "coral", 0.09, 40.0)
	# a few books so the shelf reads as a bookcase from across the hall
	for i, (bx, key, height) in enumerate(((-0.42, "book_rose", 0.30), (-0.30, "berry", 0.26),
			(-0.19, "book_teal", 0.29), (-0.08, "coral", 0.24))):
		box("case_book_%d" % i, key, grp, (bx, 0.02, 0.66 + height * 0.5 + 0.035),
			(0.09, 0.26, height), bevel_width=0.015)
	return grp


def build_pearl_chair() -> bpy.types.Object:
	grp = root("pearl_chair")
	box("chair_seat", "cream_light", grp, (0.0, 0.0, 0.52), (0.62, 0.58, 0.13), bevel_width=0.05)
	box("chair_rim", "wood", grp, (0.0, 0.0, 0.43), (0.66, 0.62, 0.09), bevel_width=0.04)
	for tag, (sx, sy) in (("fl", (-0.24, -0.22)), ("fr", (0.24, -0.22)),
			("bl", (-0.24, 0.22)), ("br", (0.24, 0.22))):
		banded_leg("chair_leg_" + tag, grp, sx, sy, 0.075, 0.30, "cream")
	# scallop-shell back with the coral medallion at the hinge
	box("chair_back_rail", "wood", grp, (0.0, 0.26, 0.62), (0.56, 0.09, 0.10), bevel_width=0.03)
	shell_fan("chair_back", grp, (0.0, 0.28, 0.66), 0.56, 5, "cream_light", 0.12, 44.0)
	blob("chair_medallion", "coral", grp, (0.0, 0.21, 0.72), (0.09, 0.05, 0.09))
	return grp


def build_pearl_table() -> bpy.types.Object:
	grp = root("pearl_table")
	box("table_top", "wood_light", grp, (0.0, 0.0, 0.62), (1.16, 0.86, 0.08), bevel_width=0.05)
	box("table_apron", "cream", grp, (0.0, 0.0, 0.54), (1.10, 0.80, 0.12), bevel_width=0.04)
	box("table_band", "lavender", grp, (0.0, 0.40, 0.54), (0.34, 0.04, 0.11), bevel_width=0.02)
	shell_fan("table_shell", grp, (0.0, -0.42, 0.50), 0.19, 4, "coral", 0.07, 40.0)
	for tag, (sx, sy) in (("fl", (-0.46, -0.32)), ("fr", (0.46, -0.32)),
			("bl", (-0.46, 0.32)), ("br", (0.46, 0.32))):
		banded_leg("table_leg_" + tag, grp, sx, sy, 0.095, 0.38, "cream")
	return grp


ASSETS = [
	("park_bench", build_park_bench(), "park"),
	("park_fountain", build_park_fountain(), "park"),
	("pearl_bookcase", build_pearl_bookcase(), "furniture"),
	("pearl_chair", build_pearl_chair(), "furniture"),
	("pearl_table", build_pearl_table(), "furniture"),
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
		for poly in member.data.polygons:
			tris += max(1, len(poly.vertices) - 2)
		for mat in member.data.materials:
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
# QA renders (Cycles on CPU — the headless bpy wheel has no GL context).
# ---------------------------------------------------------------------------
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.view_settings.view_transform = "Standard"
scene.render.resolution_x = 680
scene.render.resolution_y = 560
scene.render.image_settings.file_format = "PNG"
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

all_objects = [member for _, asset_obj, _ in ASSETS for member in family(asset_obj)]
for asset_name, asset_obj, _ in ASSETS:
	for member in all_objects:
		member.hide_render = member not in family(asset_obj)
	_, _, _, dims = metrics(asset_obj)
	span = max(dims.x, dims.y, dims.z, 0.2)
	camera.data.ortho_scale = span * 1.7
	centre = Vector((0.0, 0.0, dims.z * 0.5))
	direction = Vector((1.0, -1.6, 0.75)).normalized()
	camera.location = centre + direction * span * 4.0
	camera.rotation_euler = (direction * -1.0).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
for member in all_objects:
	member.hide_render = False

print("built %d assets into %s" % (len(ASSETS), ASSET_OUT))
