#!/usr/bin/env python3
"""Build the Pearl Opera House architecture kit from the approved flat cards.

Stage 2/3 of the art construction pathway for
`assets_src/concepts/opera_house_flat/` — the twelve `opera_architecture_*`
cards accepted in `audit/opera_house_flat_prototype_ledger_2026-07-21.csv`,
staged by `CLAUDE_OPERA_HOUSE_3D_CONTINUATION_2026-07-21.md`. The board is the
visual source of truth: cream stone, gold trim, theatre-rose velvet, pearl
accents, shell motif.

Scale follows the live lobby in `scripts/opera_house.gd`: 78 units wide,
storeys 13 apart, ceiling at 46.6. Every asset's origin sits at the base
centre so `_lobby_prop(name, pos)` places it directly on the floor.

Mobile rules: texture-free, embedded matte materials, low segment counts,
no lights, no animation.

Usage:  blender --background --python tools/build_opera_house_kit.py
        python3 tools/build_opera_house_kit.py        (pip `bpy` module)
        ... --only=opera_column
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "opera" / "house"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_opera_house_kit"
BLEND_OUT = SOURCE_OUT / "opera_house_kit.blend"

ONLY_ASSET = ""
for argument in sys.argv[1:]:
	if argument.startswith("--only="):
		ONLY_ASSET = argument.split("=", 1)[1]
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0

# Sampled off opera_house_architecture_kit_2026-07-21.png / the master scene key.
PALETTE = {
	"stone": (0.937, 0.882, 0.796, 1.0),        # warm ivory masonry
	"stone_shadow": (0.831, 0.749, 0.647, 1.0),
	"stone_deep": (0.706, 0.612, 0.518, 1.0),
	"gold": (0.855, 0.667, 0.278, 1.0),
	"gold_deep": (0.671, 0.478, 0.180, 1.0),
	"velvet": (0.706, 0.267, 0.325, 1.0),        # theatre rose
	"velvet_deep": (0.522, 0.157, 0.235, 1.0),
	"peach": (0.914, 0.635, 0.514, 1.0),
	"pearl": (0.976, 0.949, 0.918, 1.0),
	"terrazzo": (0.855, 0.443, 0.427, 1.0),
	"terrazzo_mint": (0.678, 0.808, 0.741, 1.0),
	"terrazzo_cream": (0.945, 0.902, 0.831, 1.0),
	"glass": (0.678, 0.855, 0.902, 1.0),
	"veil": (0.984, 0.878, 0.639, 1.0),          # warm walk-in glow
	"ink": (0.145, 0.157, 0.286, 1.0),           # navy/purple outline accent
	"dark": (0.212, 0.176, 0.298, 1.0),
}


def material(name: str, color: tuple[float, float, float, float]) -> bpy.types.Material:
	mat = bpy.data.materials.new("OPH_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.86
	bsdf.inputs["Metallic"].default_value = 0.28 if "gold" in name else 0.0
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def _finish(obj, mat, parent, bevel: float, segments: int = 2):
	obj.data.materials.append(mat)
	obj.parent = parent
	if bevel > 0.0:
		bev = obj.modifiers.new("toy_rounding", "BEVEL")
		bev.width = bevel
		bev.segments = segments
		bev.limit_method = "ANGLE"
		bpy.context.view_layer.objects.active = obj
		obj.select_set(True)
		bpy.ops.object.modifier_apply(modifier=bev.name)
		obj.select_set(False)
	return obj


def box(name, loc, size, mat, parent, rot=(0.0, 0.0, 0.0), bevel=0.09):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return _finish(obj, MATS[mat], parent, min(bevel, min(size) * 0.28))


def cyl(name, loc, radius, depth, mat, parent, verts=12, rot=(0.0, 0.0, 0.0), bevel=0.06):
	bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
		location=loc, rotation=rot)
	obj = bpy.context.active_object
	obj.name = name
	return _finish(obj, MATS[mat], parent, min(bevel, radius * 0.3))


def cone(name, loc, r1, r2, depth, mat, parent, verts=12, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth,
		location=loc, rotation=rot)
	obj = bpy.context.active_object
	obj.name = name
	return _finish(obj, MATS[mat], parent, 0.05)


def ball(name, loc, scale, mat, parent, subdiv=2):
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdiv, radius=1.0, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return _finish(obj, MATS[mat], parent, 0.0)


def torus(name, loc, major, minor, mat, parent, major_seg=16, minor_seg=6, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(location=loc, rotation=rot, major_radius=major,
		minor_radius=minor, major_segments=major_seg, minor_segments=minor_seg)
	obj = bpy.context.active_object
	obj.name = name
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return _finish(obj, MATS[mat], parent, 0.0)


def arc_band(name, parent, mat, radius, thickness, depth, z0, span=math.pi,
		start=0.0, segments=14, height_scale=1.0):
	"""A ring segment standing in the XZ plane — arch heads, cornices, fascias."""
	verts, faces = [], []
	inner = radius - thickness * 0.5
	outer = radius + thickness * 0.5
	for i in range(segments + 1):
		a = start + span * (i / segments)
		cx, cz = math.cos(a), math.sin(a) * height_scale
		verts += [
			(inner * cx, -depth * 0.5, z0 + inner * cz),
			(outer * cx, -depth * 0.5, z0 + outer * cz),
			(inner * cx, depth * 0.5, z0 + inner * cz),
			(outer * cx, depth * 0.5, z0 + outer * cz),
		]
	for i in range(segments):
		a, b = i * 4, (i + 1) * 4
		faces += [
			(a + 0, a + 1, b + 1, b + 0),   # inner->outer front
			(a + 2, b + 2, b + 3, a + 3),   # back
			(a + 0, b + 0, b + 2, a + 2),   # inner wall
			(a + 1, a + 3, b + 3, b + 1),   # outer wall
		]
	faces += [(0, 2, 3, 1)]
	last = segments * 4
	faces += [(last + 0, last + 1, last + 3, last + 2)]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	return _finish(obj, MATS[mat], parent, 0.05)


def shell(name, parent, loc, size, mat="pearl", ribs=5, yaw=0.0):
	"""The house motif: a fan of pearl ribs over a rounded boss."""
	node = root(name)
	node.parent = parent
	node.location = loc
	node.rotation_euler = (0.0, 0.0, yaw)
	ball(name + "_boss", (0.0, 0.0, -size * 0.18), (size * 0.42, size * 0.2, size * 0.3), mat, node)
	for i in range(ribs):
		a = math.pi * (0.16 + 0.68 * (i / max(ribs - 1, 1)))
		rx, rz = math.cos(a) * size * 0.62, math.sin(a) * size * 0.62
		rib = ball(f"{name}_rib{i}", (rx, 0.0, rz), (size * 0.17, size * 0.13, size * 0.34), mat, node)
		rib.rotation_euler = (0.0, -a + math.pi * 0.5, 0.0)
	return node


def pearl_garland(name, parent, radius, z0, count=13, size=0.34, span=math.pi, start=0.0, sag=0.0):
	node = root(name)
	node.parent = parent
	for i in range(count):
		t = i / (count - 1)
		a = start + span * t
		drop = math.sin(t * math.pi) * sag
		ball(f"{name}_p{i}", (math.cos(a) * radius, 0.0, z0 + math.sin(a) * radius - drop),
			(size, size * 0.8, size), "pearl", node)
	return node


# ---------------------------------------------------------------------------
# the twelve architecture cards
# ---------------------------------------------------------------------------

def build_column(name):
	"""opera_architecture_column_and_pilaster — the free-standing storey column."""
	node = root(name)
	cyl(name + "_plinth", (0, 0, 0.45), 2.05, 0.9, "stone_shadow", node, verts=16)
	cyl(name + "_base_ring", (0, 0, 1.15), 1.85, 0.5, "gold", node, verts=16)
	shaft = cyl(name + "_shaft", (0, 0, 6.9), 1.55, 10.9, "stone", node, verts=16)
	shaft.name = name + "_shaft"
	for i in range(8):   # broad reeds standing PROUD of the shaft: an inset
		a = math.tau * i / 8.0   # strip co-planar with the drum z-fights on Mali
		box(f"{name}_reed{i}", (math.cos(a) * 1.66, math.sin(a) * 1.66, 6.9),
			(0.42, 0.42, 10.2), "stone_shadow", node, rot=(0, 0, a), bevel=0.16)
	cyl(name + "_neck", (0, 0, 12.5), 1.72, 0.42, "gold", node, verts=16)
	cyl(name + "_capital", (0, 0, 12.95), 2.1, 0.7, "stone", node, verts=16)
	shell(name + "_motif", node, (0.0, -2.0, 12.9), 1.5)
	box(name + "_abacus", (0, 0, 13.45), (4.5, 4.5, 0.42), "stone_shadow", node)
	return node


def build_pilaster(name):
	"""The flat wall-facing half of the same card."""
	node = root(name)
	box(name + "_plinth", (0, 0, 0.42), (2.6, 1.5, 0.84), "stone_shadow", node)
	box(name + "_base", (0, 0, 1.05), (2.3, 1.3, 0.5), "gold", node)
	box(name + "_shaft", (0, 0, 7.0), (1.9, 1.05, 11.4), "stone", node)
	for offset in (-0.55, 0.0, 0.55):
		box(f"{name}_reed{offset}", (offset, -0.62, 7.0), (0.3, 0.3, 10.6), "stone_shadow", node, bevel=0.1)
	box(name + "_neck", (0, 0, 12.85), (2.2, 1.2, 0.36), "gold", node)
	box(name + "_capital", (0, 0, 13.2), (2.7, 1.45, 0.62), "stone", node)
	shell(name + "_motif", node, (0.0, -0.75, 13.15), 1.1)
	return node


def build_cove_cornice(name):
	"""opera_architecture_cove_cornice — a 6-unit wall trim module."""
	node = root(name)
	box(name + "_bed", (0, 0, 0.22), (6.0, 1.0, 0.44), "stone", node)
	arc_band(name + "_cove", node, "stone", 1.05, 0.42, 6.0, 0.62,
		span=math.pi * 0.5, start=math.pi * 1.5, segments=8)
	box(name + "_fillet", (0, -0.32, 1.02), (6.0, 0.34, 0.3), "gold", node, bevel=0.07)
	box(name + "_crown", (0, 0, 1.42), (6.0, 1.25, 0.5), "stone_shadow", node)
	box(name + "_panel", (0, -0.56, 0.7), (4.6, 0.16, 0.62), "peach", node, bevel=0.06)
	return node


def build_balcony_fascia(name):
	"""opera_architecture_curved_balcony_fascia — the bowed mezzanine front."""
	node = root(name)
	arc_band(name + "_face", node, "velvet", 7.2, 1.0, 3.0, 1.6,
		span=math.pi * 0.62, start=math.pi * 0.19, segments=12)
	arc_band(name + "_rail", node, "gold", 7.35, 0.5, 0.7, 3.2,
		span=math.pi * 0.62, start=math.pi * 0.19, segments=12)
	arc_band(name + "_skirt", node, "stone", 7.3, 0.7, 0.85, 0.28,
		span=math.pi * 0.62, start=math.pi * 0.19, segments=12)
	arc_band(name + "_band", node, "stone_shadow", 7.3, 0.4, 0.5, 1.05,
		span=math.pi * 0.62, start=math.pi * 0.19, segments=12)
	shell(name + "_motif", node, (0.0, -7.6, 1.9), 1.6)
	return node


def build_shell_balustrade(name):
	"""opera_architecture_shell_balustrade — one 6-unit gold run."""
	node = root(name)
	box(name + "_plinth", (0, 0, 0.2), (6.0, 0.9, 0.4), "stone", node)
	for i in range(5):
		x = -2.2 + i * 1.1
		cyl(f"{name}_baluster{i}", (x, 0, 1.4), 0.24, 2.0, "gold", node, verts=10)
		ball(f"{name}_bead{i}", (x, 0, 1.62), (0.36, 0.36, 0.3), "gold", node)
	for x in (-2.85, 2.85):
		box(f"{name}_post{x}", (x, 0, 1.45), (0.62, 0.62, 2.1), "gold", node, bevel=0.1)
		ball(f"{name}_finial{x}", (x, 0, 2.62), (0.4, 0.4, 0.42), "gold", node)
	box(name + "_rail", (0, 0, 2.62), (6.0, 0.7, 0.44), "gold", node, bevel=0.14)
	box(name + "_rail_top", (0, 0, 2.92), (6.0, 0.86, 0.22), "gold_deep", node, bevel=0.08)
	return node


def build_split_stair(name):
	"""opera_architecture_split_stair — one storey-height flight, velvet runner."""
	node = root(name)
	steps = 9
	rise = 13.0 / steps
	run = 1.35
	for i in range(steps):
		z = rise * (i + 0.5)
		y = -run * (steps - 1) * 0.5 + run * i
		box(f"{name}_tread{i}", (0, y, z - rise * 0.5), (7.6, run, rise), "stone", node, bevel=0.07)
		box(f"{name}_runner{i}", (0, y - 0.02, z - rise * 0.02), (4.4, run * 0.98, rise * 0.14),
			"velvet", node, bevel=0.04)
	for side in (-1.0, 1.0):
		box(f"{name}_stringer{side}", (side * 4.05, 0.0, 6.5),
			(0.7, run * steps * 1.02, 13.4), "stone_shadow", node, bevel=0.12)
		for i in range(4):
			t = i / 3.0
			y = -run * (steps - 1) * 0.5 + run * (steps - 1) * t
			cyl(f"{name}_newel{side}{i}", (side * 4.05, y, rise * (steps * t) + 1.5), 0.26, 3.0,
				"gold", node, verts=10)
		rail = box(f"{name}_rail{side}", (side * 4.05, 0.0, 8.6),
			(0.44, run * steps * 1.04, 0.44), "gold", node, bevel=0.14)
		rail.rotation_euler = (math.atan2(13.0, run * steps), 0.0, 0.0)
	return node


def build_grand_arch(name):
	"""opera_architecture_grand_arch — the pearl-garlanded proscenium head."""
	node = root(name)
	for side in (-1.0, 1.0):
		box(f"{name}_pier{side}", (side * 5.4, 0, 5.0), (2.2, 2.0, 10.0), "stone", node)
		box(f"{name}_pier_base{side}", (side * 5.4, 0, 0.5), (2.8, 2.4, 1.0), "stone_shadow", node)
		box(f"{name}_pier_cap{side}", (side * 5.4, 0, 10.3), (2.7, 2.3, 0.7), "gold", node)
		cyl(f"{name}_colonnette{side}", (side * 4.1, -1.0, 5.4), 0.55, 9.4, "gold", node, verts=10)
	arc_band(name + "_head", node, "stone", 5.4, 2.1, 2.0, 10.6, segments=16)
	arc_band(name + "_head_trim", node, "gold", 6.6, 0.5, 2.3, 10.6, segments=16)
	arc_band(name + "_soffit", node, "velvet_deep", 4.2, 0.5, 1.6, 10.6, segments=16)
	# the garland is a FRONT-FACE swag: on the arch radius and proud of the
	# stone, or the soffit swallows it (first render caught exactly that)
	garland = pearl_garland(name + "_garland", node, 5.3, 10.6, count=17, size=0.42)
	garland.location = (0.0, -1.15, 0.0)
	shell(name + "_crest", node, (0.0, -1.1, 16.6), 2.4)
	box(name + "_threshold", (0, 0, 0.14), (8.6, 2.4, 0.28), "velvet", node, bevel=0.06)
	return node


def _portal_frame(name, node):
	for side in (-1.0, 1.0):
		box(f"{name}_jamb{side}", (side * 3.0, 0, 4.6), (1.1, 1.2, 9.2), "stone", node)
		box(f"{name}_jamb_base{side}", (side * 3.0, 0, 0.4), (1.5, 1.5, 0.8), "stone_shadow", node)
		box(f"{name}_jamb_trim{side}", (side * 2.45, -0.6, 4.8), (0.3, 0.5, 8.8), "gold", node, bevel=0.07)
	arc_band(name + "_head", node, "stone", 3.0, 1.1, 1.2, 9.2, segments=12)
	arc_band(name + "_head_trim", node, "gold", 3.6, 0.32, 1.4, 9.2, segments=12)
	torus(name + "_crest_ring", (0.0, -0.55, 12.9), 0.95, 0.24, "gold", node,
		major_seg=16, minor_seg=6, rot=(math.pi * 0.5, 0.0, 0.0))
	return node


def build_portal_closed(name):
	"""opera_architecture_portal_closed — locked career door, curtains drawn."""
	node = root(name)
	_portal_frame(name, node)
	cyl(name + "_crest_plate", (0.0, -0.62, 12.9), 0.74, 0.22, "stone_shadow", node,
		verts=16, rot=(math.pi * 0.5, 0.0, 0.0))
	for side in (-1.0, 1.0):
		for i in range(4):
			x = side * (0.35 + i * 0.72)
			box(f"{name}_drape{side}{i}", (x, 0.35, 5.2), (0.66, 0.5, 10.0),
				"velvet" if i % 2 == 0 else "velvet_deep", node, bevel=0.16)
		box(f"{name}_tieback{side}", (side * 1.5, 0.1, 4.2), (2.0, 0.7, 0.6), "gold", node, bevel=0.16)
		ball(f"{name}_tassel{side}", (side * 1.5, -0.15, 3.6), (0.34, 0.34, 0.6), "gold", node)
	box(name + "_valance", (0, 0.3, 9.6), (5.4, 0.62, 1.0), "velvet_deep", node, bevel=0.2)
	return node


def build_portal_open(name):
	"""opera_architecture_portal_open — active door, warm walk-in veil."""
	node = root(name)
	_portal_frame(name, node)
	shell(name + "_crest", node, (0.0, -0.62, 12.9), 0.9)
	box(name + "_veil", (0, 0.45, 5.0), (4.6, 0.14, 9.4), "veil", node, bevel=0.05)
	for i in range(7):   # soft pleats read as light, not as a wall
		box(f"{name}_pleat{i}", (-1.9 + i * 0.64, 0.3, 5.0), (0.4, 0.22, 9.2), "peach", node, bevel=0.08)
	for side in (-1.0, 1.0):
		for i in range(2):
			x = side * (2.2 + i * 0.6)
			box(f"{name}_swag{side}{i}", (x, 0.3, 5.6), (0.6, 0.5, 8.4), "velvet", node, bevel=0.18)
		box(f"{name}_tieback{side}", (side * 2.4, 0.0, 4.6), (1.5, 0.66, 0.55), "gold", node, bevel=0.16)
	box(name + "_valance", (0, 0.25, 9.6), (5.4, 0.6, 1.0), "velvet", node, bevel=0.2)
	return node


def _medallion(name, lit):
	"""opera_architecture_medallion_states — the centre-stage boss inlay."""
	node = root(name)
	cyl(name + "_disc", (0, 0, 0.12), 2.6, 0.24, "velvet_deep" if not lit else "velvet", node, verts=24)
	cyl(name + "_rim", (0, 0, 0.2), 2.75, 0.28, "gold" if lit else "gold_deep", node, verts=24)
	cyl(name + "_field", (0, 0, 0.26), 2.0, 0.2, "velvet_deep" if not lit else "peach", node, verts=24)
	for i in range(4):
		a = math.tau * i / 4.0 + math.pi * 0.25
		ball(f"{name}_stud{i}", (math.cos(a) * 2.25, math.sin(a) * 2.25, 0.34),
			(0.34, 0.34, 0.22), "pearl" if lit else "stone_deep", node)
	crest = shell(name + "_crest", node, (0.0, 0.0, 0.36), 1.5 if lit else 1.25,
		"pearl" if lit else "stone_deep")
	crest.rotation_euler = (math.pi * 0.5, 0.0, 0.0)
	if lit:
		cyl(name + "_glow", (0, 0, 0.9), 1.55, 1.2, "veil", node, verts=20)
	return node


def build_medallion_dark(name):
	return _medallion(name, False)


def build_medallion_lit(name):
	return _medallion(name, True)


def build_bubble_lift(name):
	"""opera_architecture_bubble_lift — glass column, brass base, landing ring."""
	node = root(name)
	cyl(name + "_pad", (0, 0, 0.2), 3.2, 0.4, "stone", node, verts=20)
	cyl(name + "_pad_trim", (0, 0, 0.44), 3.35, 0.24, "gold", node, verts=20)
	cyl(name + "_carpet", (0, 0, 0.6), 2.5, 0.14, "velvet", node, verts=20)
	for i in range(6):
		a = math.tau * i / 6.0
		cyl(f"{name}_post{i}", (math.cos(a) * 2.7, math.sin(a) * 2.7, 1.5), 0.2, 2.4,
			"gold", node, verts=8)
		ball(f"{name}_knob{i}", (math.cos(a) * 2.7, math.sin(a) * 2.7, 2.8), (0.3, 0.3, 0.3), "gold", node)
	cyl(name + "_tube", (0, 0, 7.0), 2.15, 11.6, "glass", node, verts=20)
	for z in (1.6, 12.6):
		torus(name + "_ring%d" % int(z), (0, 0, z), 2.2, 0.22, "gold", node, major_seg=20, minor_seg=6)
	for i, (bx, bz, br) in enumerate([(0.6, 4.0, 0.5), (-0.8, 6.4, 0.36), (0.3, 8.9, 0.44), (-0.4, 10.6, 0.3)]):
		ball(f"{name}_bubble{i}", (bx, 0.0, bz), (br, br, br), "pearl", node)
	cyl(name + "_cap", (0, 0, 13.1), 2.5, 0.7, "stone", node, verts=20)
	cyl(name + "_cap_trim", (0, 0, 13.5), 2.65, 0.3, "gold", node, verts=20)
	return node


def build_terrazzo_tile(name):
	"""opera_architecture_terrazzo_floor_tile — a 6-unit swirl floor module."""
	node = root(name)
	box(name + "_slab", (0, 0, 0.1), (6.0, 6.0, 0.2), "terrazzo", node, bevel=0.05)
	for i in range(7):   # the painted ribbon reads as two broad bands, not noise
		t = i / 6.0
		y = -2.4 + t * 4.8
		x = math.sin(t * math.pi * 1.4) * 1.5
		box(f"{name}_cream{i}", (x, y, 0.21), (2.1, 0.95, 0.06), "terrazzo_cream", node, bevel=0.03)
		box(f"{name}_mint{i}", (x + 1.5, y, 0.21), (1.1, 0.9, 0.05), "terrazzo_mint", node, bevel=0.03)
	return node


def build_carpet_runner(name):
	"""opera_architecture_carpet_runner_pair — the straight run."""
	node = root(name)
	box(name + "_pile", (0, 0, 0.09), (5.2, 6.0, 0.18), "velvet", node, bevel=0.04)
	for x in (-2.45, 2.45):
		box(f"{name}_edge{x}", (x, 0, 0.13), (0.42, 6.0, 0.2), "gold", node, bevel=0.05)
	box(name + "_field", (0, 0, 0.2), (3.9, 5.7, 0.05), "velvet_deep", node, bevel=0.03)
	return node


def build_carpet_turn(name):
	"""The quarter-turn half of the same card."""
	node = root(name)
	arc_band(name + "_pile", node, "velvet", 3.6, 5.2, 0.18, 0.0,
		span=math.pi * 0.5, start=0.0, segments=10)
	arc_band(name + "_inner_edge", node, "gold", 1.15, 0.42, 0.22, 0.0,
		span=math.pi * 0.5, start=0.0, segments=10)
	arc_band(name + "_outer_edge", node, "gold", 6.05, 0.42, 0.22, 0.0,
		span=math.pi * 0.5, start=0.0, segments=10)
	node.rotation_euler = (math.pi * 0.5, 0.0, 0.0)
	return node


ASSETS = {
	# export name                 builder                  concept card
	"opera_column": (build_column, "opera_architecture_column_and_pilaster"),
	"opera_pilaster": (build_pilaster, "opera_architecture_column_and_pilaster"),
	"opera_cove_cornice": (build_cove_cornice, "opera_architecture_cove_cornice"),
	"opera_balcony_fascia": (build_balcony_fascia, "opera_architecture_curved_balcony_fascia"),
	"opera_shell_balustrade": (build_shell_balustrade, "opera_architecture_shell_balustrade"),
	"opera_split_stair": (build_split_stair, "opera_architecture_split_stair"),
	"opera_grand_arch": (build_grand_arch, "opera_architecture_grand_arch"),
	"opera_portal_closed": (build_portal_closed, "opera_architecture_portal_closed"),
	"opera_portal_open": (build_portal_open, "opera_architecture_portal_open"),
	"opera_medallion_dark": (build_medallion_dark, "opera_architecture_medallion_states"),
	"opera_medallion_lit": (build_medallion_lit, "opera_architecture_medallion_states"),
	"opera_bubble_lift": (build_bubble_lift, "opera_architecture_bubble_lift"),
	"opera_terrazzo_tile": (build_terrazzo_tile, "opera_architecture_terrazzo_floor_tile"),
	"opera_carpet_runner": (build_carpet_runner, "opera_architecture_carpet_runner_pair"),
	"opera_carpet_turn": (build_carpet_turn, "opera_architecture_carpet_runner_pair"),
}


def family(obj):
	out = [obj]
	for child in obj.children:
		out += family(child)
	return out


def export_asset(name: str, obj: bpy.types.Object) -> tuple[int, int]:
	"""Collapse the family to one mesh (Mali-G52 submission budget) and export."""
	bpy.ops.object.select_all(action="DESELECT")
	copies = []
	for member in family(obj):
		if member.type != "MESH":
			continue
		copy = member.copy()
		copy.data = member.data.copy()
		bpy.context.collection.objects.link(copy)
		copy.parent = None
		copy.matrix_world = member.matrix_world.copy()
		copies.append(copy)
	if not copies:
		return (0, 0)
	bpy.ops.object.select_all(action="DESELECT")
	for copy in copies:
		copy.select_set(True)
	bpy.context.view_layer.objects.active = copies[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged.data.calc_loop_triangles()
	tris = len(merged.data.loop_triangles)
	mats = len(merged.data.materials)
	bpy.ops.export_scene.gltf(filepath=str(ASSET_OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False)
	bpy.data.objects.remove(merged, do_unlink=True)
	return (tris, mats)


def bounds(obj) -> tuple[Vector, Vector]:
	points = []
	for member in family(obj):
		if member.type == "MESH":
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	if not points:
		return (Vector(), Vector())
	return (Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points))),
		Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points))))


def setup_render():
	"""Cycles on CPU: this container has no GPU/EGL, so Workbench and EEVEE
	cannot open a context. Cycles renders headless on CPU and is deterministic,
	which is what an isolated QA sheet needs."""
	scene = bpy.context.scene
	scene.render.engine = "CYCLES"
	scene.cycles.device = "CPU"
	scene.cycles.samples = 24
	scene.cycles.use_denoising = False
	scene.render.resolution_x = 512
	scene.render.resolution_y = 512
	scene.render.film_transparent = False
	scene.world = bpy.data.worlds.new("OPH_world")
	scene.world.use_nodes = True
	bg = scene.world.node_tree.nodes["Background"]
	bg.inputs[0].default_value = (0.06, 0.07, 0.15, 1.0)
	bg.inputs[1].default_value = 1.1
	key = bpy.data.lights.new("OPH_key", "SUN")
	key.energy = 3.2
	key_obj = bpy.data.objects.new("OPH_key", key)
	key_obj.rotation_euler = (math.radians(52.0), 0.0, math.radians(38.0))
	bpy.context.collection.objects.link(key_obj)
	fill = bpy.data.lights.new("OPH_fill", "SUN")
	fill.energy = 1.1
	fill_obj = bpy.data.objects.new("OPH_fill", fill)
	fill_obj.rotation_euler = (math.radians(66.0), 0.0, math.radians(-124.0))
	bpy.context.collection.objects.link(fill_obj)
	cam_data = bpy.data.cameras.new("OPH_cam")
	cam_data.type = "ORTHO"
	cam = bpy.data.objects.new("OPH_cam", cam_data)
	bpy.context.collection.objects.link(cam)
	scene.camera = cam
	return cam


def render_qa(cam, name, obj):
	low, high = bounds(obj)
	centre = (low + high) * 0.5
	size = max((high - low).x, (high - low).y, (high - low).z, 1.0)
	cam.data.ortho_scale = size * 1.4
	for label, angle in (("front", 0.0), ("three_quarter", math.radians(45.0))):
		distance = size * 3.0
		cam.location = (centre.x + math.sin(angle) * distance,
			centre.y - math.cos(angle) * distance, centre.z + size * 0.34)
		direction = centre - Vector(cam.location)
		cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
		bpy.context.scene.render.filepath = str(QA_OUT / f"{name}_{label}.png")
		bpy.ops.render.render(write_still=True)


def main():
	report = []
	built = []
	# stage 3 first: every GLB exports before any renderer is touched, so a
	# headless box with no GL context still produces the runtime kit
	for name, (builder, card) in ASSETS.items():
		if ONLY_ASSET and name != ONLY_ASSET:
			continue
		obj = builder(name)
		tris, mats = export_asset(name, obj)
		low, high = bounds(obj)
		report.append((name, card, tris, mats, high - low))
		built.append((name, obj))
	bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
	# stage 4: isolated QA renders, one family visible at a time
	for _, obj in built:
		for member in family(obj):
			member.hide_render = True
	try:
		cam = setup_render()
		for name, obj in built:
			for member in family(obj):
				member.hide_render = False
			render_qa(cam, name, obj)
			for member in family(obj):
				member.hide_render = True
	except Exception as exc:   # no GL/EGL context: keep the kit, skip the sheet
		print("OPERA_HOUSE_KIT | QA_RENDER_SKIPPED |", exc)
	print("\nOPERA_HOUSE_KIT | asset | card | triangles | materials | size(x,y,z)")
	total = 0
	for name, card, tris, mats, size in report:
		total += tris
		print(f"OPERA_HOUSE_KIT | {name} | {card} | {tris} | {mats} | "
			f"{size.x:.2f},{size.y:.2f},{size.z:.2f}")
	print(f"OPERA_HOUSE_KIT | TOTAL | {len(report)} assets | {total} triangles")


main()
