#!/usr/bin/env python3
"""Build the Ember Fortress enrichment kit from the approved 2D boards.

Stage 2/3 of the art construction pathway for the forty individual cards in
`assets_src/concepts/ember_fortress_claude_2026-07-22/expansion_40/`, whose
export contract is `CLAUDE_EXPANSION_40_MANIFEST.csv` and whose review is
`EMBER_FORTRESS_EXPANSION_40_AUDIT_2026-07-22.md`.

This is the ADDITIVE half of `CLAUDE_EMBER_FORTRESS_BLENDER_HANDOFF_2026-07-22`:
forty new enrichment roles in four families (architecture, terrain,
interactive, ambient/guidance). It does not touch the 39 shipped core exports,
whose provenance is a separate owner decision recorded in
`ART_CONSTRUCTION_PATHWAY_AUDIT_2026-07-25.md` §3.3.

Contracts honoured here, from the manifest and the handoff:
  * per-row triangle budget, checked and printed;
  * named state/part children where a row asks for them (a lever handle, a
    pressure-plate centre, a brazier flame, moth children, beacon lens) - the
    runtime addresses them by name, so those rows export a small node tree
    instead of one merged mesh;
  * no OmniLight, no transparency, no baked smoke, no refraction, no collision
    on ambient flora - all of those are explicit "do not" items;
  * IP-safe generic volcanic fantasy only.

Usage:  blender --background --python tools/build_ember_expansion_kit.py
        python3 tools/build_ember_expansion_kit.py     (pip `bpy` module)
        ... --only=ember_ash_fern
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "ember_fortress"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_ember_expansion_kit"
BLEND_OUT = SOURCE_OUT / "ember_expansion_kit.blend"
MANIFEST = (ROOT / "assets_src" / "concepts" / "ember_fortress_claude_2026-07-22"
	/ "expansion_40" / "CLAUDE_EXPANSION_40_MANIFEST.csv")

ONLY_ASSET = ""
for argument in sys.argv[1:]:
	if argument.startswith("--only="):
		ONLY_ASSET = argument.split("=", 1)[1]
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0

# Sampled off the four expansion contact sheets.
PALETTE = {
	"basalt": (0.208, 0.180, 0.267, 1.0),
	"basalt_light": (0.310, 0.271, 0.384, 1.0),
	"basalt_dark": (0.129, 0.110, 0.176, 1.0),
	"mortar": (0.435, 0.396, 0.494, 1.0),
	"lava": (1.0, 0.404, 0.114, 1.0),
	"lava_hot": (1.0, 0.678, 0.286, 1.0),
	"lava_deep": (0.827, 0.208, 0.055, 1.0),
	"ash": (0.478, 0.435, 0.522, 1.0),
	"ash_light": (0.612, 0.573, 0.647, 1.0),
	"fern": (0.596, 0.529, 0.808, 1.0),
	"fern_teal": (0.404, 0.706, 0.706, 1.0),
	"moss": (0.286, 0.706, 0.596, 1.0),
	"moss_tip": (0.941, 0.435, 0.404, 1.0),
	"cap": (0.396, 0.286, 0.463, 1.0),
	"gill": (1.0, 0.522, 0.220, 1.0),
	"wing": (1.0, 0.561, 0.259, 1.0),
	"smoke": (0.396, 0.349, 0.494, 1.0),
	"crystal": (0.718, 0.620, 0.945, 1.0),
	"iron": (0.271, 0.271, 0.333, 1.0),
	"band_pink": (0.949, 0.451, 0.671, 1.0),
	"band_aqua": (0.400, 0.804, 0.851, 1.0),
	"band_gold": (0.980, 0.792, 0.361, 1.0),
}


def material(name, color):
	mat = bpy.data.materials.new("EMX_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.92
	bsdf.inputs["Metallic"].default_value = 0.0
	if name.startswith("lava") or name in ("gill", "wing", "crystal"):
		bsdf.inputs["Emission Color"].default_value = color
		bsdf.inputs["Emission Strength"].default_value = 0.55
	return mat


MATS = {name: material(name, color) for name, color in PALETTE.items()}


def root(name, parent=None):
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	if parent is not None:
		obj.parent = parent
	return obj


def _finish(obj, mat, parent, bevel, segments=1):
	obj.data.materials.append(MATS[mat])
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


def box(name, loc, size, mat, parent, rot=(0.0, 0.0, 0.0), bevel=0.05):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return _finish(obj, mat, parent, min(bevel, min(size) * 0.3))


def cyl(name, loc, radius, depth, mat, parent, verts=8, rot=(0.0, 0.0, 0.0), bevel=0.04):
	bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth,
		location=loc, rotation=rot)
	obj = bpy.context.active_object
	obj.name = name
	return _finish(obj, mat, parent, min(bevel, radius * 0.3))


def cone(name, loc, r1, r2, depth, mat, parent, verts=8, rot=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth,
		location=loc, rotation=rot)
	obj = bpy.context.active_object
	obj.name = name
	return _finish(obj, mat, parent, 0.0)


def ball(name, loc, scale, mat, parent, subdiv=1):
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdiv, radius=1.0, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	for polygon in obj.data.polygons:
		polygon.use_smooth = True
	return _finish(obj, mat, parent, 0.0)


def blocks(name, parent, span, z, count, size, mat="basalt", alt="basalt_light", axis="x"):
	"""A course of chunky masonry blocks — the boards' core architectural read."""
	for i in range(count):
		t = (i + 0.5) / count - 0.5
		loc = (span * t, 0.0, z) if axis == "x" else (0.0, span * t, z)
		_finish_mat = mat if i % 2 == 0 else alt
		box(f"{name}{i}", loc, size, _finish_mat, parent, bevel=0.05)


def vein(name, parent, loc, size, rot=(0.0, 0.0, 0.0)):
	"""A glowing lava seam set into the stone."""
	return box(name, loc, size, "lava", parent, rot=rot, bevel=0.02)


# ---------------------------------------------------------------------------
# architecture (10)
# ---------------------------------------------------------------------------

def obsidian_bridge(n):
	g = root(n)
	box(n + "_deck", (0, 0, -0.15), (8.0, 2.6, 0.32), "basalt", g)
	for side in (-1.0, 1.0):
		box(f"{n}_curb{side}", (0, side * 1.15, 0.12), (8.0, 0.34, 0.34), "basalt_light", g)
		vein(f"{n}_vein{side}", g, (0, side * 1.15, 0.3), (7.2, 0.14, 0.06))
	for i in range(5):
		box(f"{n}_plank{i}", (-3.2 + i * 1.6, 0, 0.03), (1.3, 2.3, 0.1), "basalt_dark", g)
	for end in (-3.9, 3.9):
		box(f"{n}_post{end}", (end, 0, 0.35), (0.55, 2.8, 0.9), "basalt_light", g)
	return g


def basalt_archway(n):
	g = root(n)
	for side in (-1.0, 1.0):
		for i in range(4):
			box(f"{n}_leg{side}{i}", (side * 1.9, 0, 0.5 + i * 0.95), (0.95, 0.9, 0.95),
				"basalt" if i % 2 == 0 else "basalt_light", g)
		vein(f"{n}_legvein{side}", g, (side * 2.35, 0, 2.4), (0.08, 0.2, 1.6))
	for i in range(5):
		a = math.pi * (0.12 + 0.76 * i / 4.0)
		box(f"{n}_key{i}", (math.cos(a) * 2.0, 0.0, 4.3 + math.sin(a) * 1.7),
			(0.95, 0.9, 0.85), "basalt" if i % 2 else "basalt_light", g, rot=(0, -a + math.pi / 2, 0))
	return g


def lava_aqueduct(n):
	g = root(n)
	box(n + "_trough", (0, 0, 2.6), (10.0, 1.5, 0.9), "basalt", g)
	box(n + "_channel", (0, 0, 3.05), (9.4, 0.85, 0.3), "lava", g, bevel=0.03)
	for i in range(4):
		x = -3.6 + i * 2.4
		box(f"{n}_pier{i}", (x, 0, 1.05), (0.95, 1.2, 2.1), "basalt_light", g)
		box(f"{n}_foot{i}", (x, 0, 0.15), (1.35, 1.5, 0.3), "basalt_dark", g)
	return g


def ember_balcony(n):
	g = root(n)
	box(n + "_floor", (0, -0.6, 0.15), (5.0, 2.6, 0.3), "basalt", g)
	for i in range(6):
		a = math.pi * (0.1 + 0.8 * i / 5.0)
		box(f"{n}_rail{i}", (math.cos(a) * 2.4, -0.6 + math.sin(a) * 1.15, 0.75),
			(0.42, 0.42, 1.0), "basalt_light", g, rot=(0, 0, a))
	box(n + "_cap", (0, -1.7, 1.3), (4.6, 0.3, 0.22), "basalt_light", g)
	for side in (-1.0, 1.0):
		box(f"{n}_bracket{side}", (side * 1.8, 0.55, -0.35), (0.7, 1.1, 0.9), "basalt_dark", g)
	vein(n + "_vein", g, (0, -1.72, 0.7), (3.4, 0.06, 0.12))
	return g


def gatehouse_buttress(n):
	g = root(n)
	box(n + "_base", (0, 0.5, 0.4), (2.4, 2.2, 0.8), "basalt_dark", g)
	box(n + "_body", (0, 0.15, 2.0), (1.7, 1.4, 2.6), "basalt", g)
	box(n + "_slope", (0, -0.5, 3.0), (1.5, 0.9, 1.6), "basalt_light", g, rot=(0.5, 0, 0))
	vein(n + "_vein", g, (0, -0.75, 1.9), (0.5, 0.06, 1.6))
	return g


def stair_module(n):
	g = root(n)
	for i in range(5):
		box(f"{n}_step{i}", (0, -2.4 + i * 1.2, 0.22 + i * 0.44), (3.2, 1.2, 0.44),
			"basalt" if i % 2 == 0 else "basalt_light", g)
	for side in (-1.0, 1.0):
		box(f"{n}_rail{side}", (side * 1.75, 0, 1.4), (0.4, 6.0, 0.5), "basalt_dark", g,
			rot=(math.atan2(2.2, 6.0), 0, 0))
		vein(f"{n}_vein{side}", g, (side * 1.75, 0, 1.75), (0.08, 5.4, 0.1),
			rot=(math.atan2(2.2, 6.0), 0, 0))
	return g


def parapet_corner(n):
	g = root(n)
	for axis, sign in (("x", 1.0), ("y", 1.0)):
		for i in range(4):
			t = 0.5 + i * 1.0
			loc = (t, 0.0, 0.9) if axis == "x" else (0.0, t, 0.9)
			box(f"{n}_{axis}{i}", loc, (1.0, 1.0, 1.8),
				"basalt" if i % 2 == 0 else "basalt_light", g)
	box(n + "_corner", (0, 0, 0.9), (1.2, 1.2, 1.9), "basalt_dark", g)
	for axis in ("x", "y"):
		for i in range(2):
			t = 1.2 + i * 1.8
			loc = (t, 0.0, 2.1) if axis == "x" else (0.0, t, 2.1)
			box(f"{n}_merlon_{axis}{i}", loc, (0.7, 0.9, 0.6), "basalt_light", g)
	vein(n + "_vein_x", g, (2.4, -0.48, 0.9), (0.16, 0.06, 0.9))
	vein(n + "_vein_y", g, (-0.48, 2.4, 0.9), (0.06, 0.16, 0.9))
	return g


def ash_chimney(n):
	g = root(n)
	for i in range(5):
		r = 1.35 - i * 0.16
		cyl(f"{n}_drum{i}", (0, 0, 0.65 + i * 1.3), r, 1.3,
			"basalt" if i % 2 == 0 else "basalt_light", g, verts=10)
	cyl(n + "_lip", (0, 0, 6.9), 1.0, 0.5, "basalt_dark", g, verts=10)
	cyl(n + "_mouth", (0, 0, 7.1), 0.62, 0.2, "lava", g, verts=10)
	for i in range(3):
		vein(f"{n}_vein{i}", g, (math.cos(i * 2.1) * 1.16, math.sin(i * 2.1) * 1.16, 2.4 + i * 1.2),
			(0.14, 0.14, 1.0))
	return g


def plaza_brazier(n):
	g = root(n)
	cyl(n + "_foot", (0, 0, 0.18), 0.85, 0.36, "basalt_dark", g, verts=10)
	cyl(n + "_stem", (0, 0, 0.85), 0.42, 1.05, "basalt", g, verts=8)
	cyl(n + "_bowl", (0, 0, 1.55), 0.95, 0.5, "basalt_light", g, verts=10)
	for i in range(6):   # the card's petal crown
		a = math.tau * i / 6.0
		box(f"{n}_petal{i}", (math.cos(a) * 0.85, math.sin(a) * 0.85, 1.95),
			(0.36, 0.2, 0.85), "basalt", g, rot=(0.35 * math.sin(a), -0.35 * math.cos(a), a))
	flame = root(n + "_Flame", g)   # separate flame child per the manifest
	cone(n + "_flame_body", (0, 0, 2.15), 0.5, 0.0, 1.0, "lava", flame, verts=8)
	cone(n + "_flame_core", (0, 0, 2.05), 0.28, 0.0, 0.7, "lava_hot", flame, verts=6)
	return g


def lavafall_cliff(n):
	g = root(n)
	box(n + "_face", (0, 0.4, 3.5), (3.4, 1.0, 7.0), "basalt", g)
	for i in range(4):
		box(f"{n}_ledge{i}", (-1.1 + i * 0.75, 0.0, 1.0 + i * 1.6), (1.5, 0.7, 0.5),
			"basalt_light", g)
	fall = root(n + "_Lava", g)   # separate contained lava child
	box(n + "_fall", (0, -0.15, 3.6), (0.95, 0.3, 6.4), "lava", fall, bevel=0.06)
	box(n + "_pool", (0, -0.5, 0.18), (2.0, 1.1, 0.36), "lava_deep", fall, bevel=0.06)
	return g


# ---------------------------------------------------------------------------
# terrain (11)
# ---------------------------------------------------------------------------

def magma_pool(n):
	g = root(n)
	for i in range(9):
		a = math.tau * i / 9.0
		box(f"{n}_rim{i}", (math.cos(a) * 2.2, math.sin(a) * 2.2, 0.28),
			(1.1, 0.8, 0.56), "basalt" if i % 2 == 0 else "basalt_light", g, rot=(0, 0, a))
	molten = root(n + "_Molten", g)
	cyl(n + "_molten", (0, 0, 0.2), 1.85, 0.24, "lava", molten, verts=12)
	cyl(n + "_core", (0, 0, 0.3), 1.0, 0.12, "lava_hot", molten, verts=10)
	return g


def basalt_columns(n):
	g = root(n)
	spec = [(0.0, 0.0, 4.5, 0.62), (1.05, 0.2, 3.2, 0.5), (-0.9, 0.55, 3.8, 0.55),
		(0.35, -1.05, 2.5, 0.45), (-0.7, -0.85, 2.0, 0.4)]
	for i, (x, y, h, r) in enumerate(spec):
		cyl(f"{n}_col{i}", (x, y, h * 0.5), r, h, "basalt" if i % 2 == 0 else "basalt_light",
			g, verts=6)
		cyl(f"{n}_cap{i}", (x, y, h - 0.06), r * 1.06, 0.16, "basalt_dark", g, verts=6)
	vein(n + "_vein", g, (0.0, -0.42, 1.6), (0.1, 0.08, 2.2))
	return g


def ash_dune(n):
	g = root(n)
	ball(n + "_body", (0, 0, 0.35), (1.75, 1.05, 0.62), "ash", g)
	ball(n + "_crest", (0.55, 0.1, 0.55), (0.9, 0.6, 0.4), "ash_light", g)
	ball(n + "_toe", (-0.85, -0.2, 0.2), (0.7, 0.5, 0.25), "ash", g)
	return g


def vent_cluster(n):
	g = root(n)
	for i, (x, y, h, r) in enumerate([(0.0, 0.0, 1.5, 0.62), (0.95, 0.35, 1.0, 0.46),
			(-0.7, 0.6, 0.75, 0.38)]):
		cone(f"{n}_cone{i}", (x, y, h * 0.5), r * 1.5, r * 0.72, h, "basalt", g, verts=8)
		cyl(f"{n}_mouth{i}", (x, y, h - 0.04), r * 0.55, 0.12, "lava", g, verts=8)
	return g


def obsidian_shards(n):
	g = root(n)
	cyl(n + "_plate", (0, 0, 0.1), 2.0, 0.2, "basalt_dark", g, verts=10)
	for i in range(6):
		a = math.tau * i / 6.0 + 0.3
		d = 0.55 + (i % 3) * 0.42
		h = 0.85 + (i % 4) * 0.3
		cone(f"{n}_shard{i}", (math.cos(a) * d, math.sin(a) * d, 0.2 + h * 0.5),
			0.34, 0.1, h, "basalt_light" if i % 2 else "basalt", g, verts=5,
			rot=(0.16 * math.sin(a), -0.16 * math.cos(a), 0.0))
	return g


def cooled_flow(n):
	g = root(n)
	for i in range(6):
		t = i / 5.0
		x = -3.4 + t * 6.8
		y = math.sin(t * math.pi * 1.3) * 0.75
		box(f"{n}_slab{i}", (x, y, 0.14), (1.5, 1.5, 0.28),
			"basalt" if i % 2 == 0 else "basalt_dark", g, bevel=0.07)
		if i % 2 == 0:
			vein(f"{n}_seam{i}", g, (x, y, 0.29), (1.2, 0.12, 0.05))
	return g


def cave_mouth(n):
	g = root(n)
	for i in range(6):
		a = math.pi * (0.08 + 0.84 * i / 5.0)
		box(f"{n}_jamb{i}", (math.cos(a) * 2.4, 0.0, 0.4 + math.sin(a) * 4.6),
			(1.2, 1.4, 1.2), "basalt" if i % 2 == 0 else "basalt_light", g,
			rot=(0, -a + math.pi / 2, 0))
	depth = root(n + "_Depth", g)   # separate opaque warm depth field
	box(n + "_depth", (0, 0.75, 2.4), (3.4, 0.3, 4.2), "lava_deep", depth, bevel=0.1)
	box(n + "_sill", (0, 0, 0.16), (4.4, 1.8, 0.32), "basalt_dark", g)
	return g


def meteor_crater(n):
	g = root(n)
	for i in range(10):
		a = math.tau * i / 10.0
		box(f"{n}_rim{i}", (math.cos(a) * 2.7, math.sin(a) * 2.7, 0.3),
			(1.3, 0.9, 0.6), "basalt" if i % 2 == 0 else "ash", g, rot=(0, 0, a))
	cyl(n + "_floor", (0, 0, 0.08), 2.3, 0.16, "basalt_dark", g, verts=12)
	ball(n + "_stone", (0.35, -0.2, 0.35), (0.65, 0.6, 0.45), "basalt_light", g)
	vein(n + "_seam", g, (0, 0, 0.17), (2.6, 0.16, 0.05))
	return g


def cinder_island(n):
	g = root(n)
	cyl(n + "_top", (0, 0, 0.3), 3.0, 0.6, "basalt", g, verts=12)
	cone(n + "_keel", (0, 0, -1.15), 2.6, 0.5, 2.3, "basalt_dark", g, verts=10)
	for i in range(5):
		a = math.tau * i / 5.0
		box(f"{n}_shelf{i}", (math.cos(a) * 2.5, math.sin(a) * 2.5, 0.62),
			(1.1, 0.8, 0.34), "basalt_light", g, rot=(0, 0, a))
	vein(n + "_seam", g, (0, 0, -0.35), (3.2, 0.2, 0.08))
	return g


def chain_anchor(n):
	g = root(n)
	box(n + "_socket", (0, 0, 0.4), (1.7, 1.7, 0.8), "basalt", g)
	box(n + "_collar", (0, 0, 0.95), (1.1, 1.1, 0.4), "basalt_light", g)
	cyl(n + "_pin", (0, 0, 1.35), 0.26, 0.6, "iron", g, verts=8)
	bpy.ops.mesh.primitive_torus_add(location=(0, 0, 2.05), major_radius=0.55,
		minor_radius=0.16, major_segments=12, minor_segments=6,
		rotation=(math.pi * 0.5, 0, 0))
	link = bpy.context.active_object
	link.name = n + "_link"
	for polygon in link.data.polygons:
		polygon.use_smooth = True
	_finish(link, "iron", g, 0.0)
	return g


def crust_slab(n):
	g = root(n)
	cyl(n + "_slab", (0, 0, 0.16), 1.4, 0.32, "basalt", g, verts=9)
	cyl(n + "_top", (0, 0, 0.33), 1.28, 0.06, "basalt_dark", g, verts=9)
	for i in range(3):
		a = math.tau * i / 3.0 + 0.4
		vein(f"{n}_crack{i}", g, (math.cos(a) * 0.5, math.sin(a) * 0.5, 0.35),
			(1.1, 0.09, 0.04), rot=(0, 0, a))
	return g


# ---------------------------------------------------------------------------
# interactive (10)
# ---------------------------------------------------------------------------

def forge_anvil(n):
	g = root(n)
	box(n + "_base", (0, 0, 0.18), (1.0, 0.75, 0.36), "basalt_dark", g)
	box(n + "_waist", (0, 0, 0.5), (0.55, 0.45, 0.32), "basalt", g)
	box(n + "_top", (0, 0, 0.78), (1.6, 0.62, 0.26), "basalt_light", g)
	cone(n + "_horn", (0.95, 0, 0.78), 0.24, 0.05, 0.5, "basalt_light", g, verts=6,
		rot=(0, math.pi * 0.5, 0))
	vein(n + "_vein", g, (0, -0.32, 0.5), (0.4, 0.05, 0.2))
	return g


def coal_cart(n):
	g = root(n)
	box(n + "_tub", (0, 0, 0.62), (2.0, 1.1, 0.72), "iron", g)
	box(n + "_load", (0, 0, 1.0), (1.7, 0.85, 0.24), "basalt_dark", g)
	vein(n + "_glow", g, (0, 0, 1.11), (1.4, 0.6, 0.05))
	wheels = root(n + "_Wheels", g)
	for side in (-1.0, 1.0):
		for x in (-0.65, 0.65):
			cyl(f"{n}_wheel{side}{x}", (x, side * 0.62, 0.26), 0.26, 0.14, "basalt_light",
				wheels, verts=8, rot=(math.pi * 0.5, 0, 0))
	handle = root(n + "_Handle", g)
	box(n + "_handle_bar", (-1.25, 0, 1.05), (0.16, 0.9, 0.14), "iron", handle)
	box(n + "_handle_arm", (-1.05, 0, 0.85), (0.6, 0.12, 0.12), "iron", handle)
	return g


def ember_urn(n):
	g = root(n)
	cyl(n + "_foot", (0, 0, 0.12), 0.38, 0.24, "basalt_dark", g, verts=10)
	cyl(n + "_belly", (0, 0, 0.66), 0.58, 0.9, "basalt", g, verts=10)
	cyl(n + "_neck", (0, 0, 1.24), 0.4, 0.3, "basalt_light", g, verts=10)
	cyl(n + "_mouth", (0, 0, 1.4), 0.34, 0.1, "lava", g, verts=10)
	for side in (-1.0, 1.0):
		box(f"{n}_handle{side}", (side * 0.62, 0, 0.86), (0.16, 0.16, 0.5), "basalt_light", g)
	return g


def volcanic_drum(n):
	g = root(n)
	cyl(n + "_shell", (0, 0, 0.42), 0.9, 0.84, "basalt", g, verts=12)
	cyl(n + "_head", (0, 0, 0.87), 0.92, 0.1, "ash_light", g, verts=12)
	cyl(n + "_hoop", (0, 0, 0.8), 0.96, 0.12, "basalt_light", g, verts=12)
	mallets = root(n + "_Mallets", g)
	for i, side in enumerate((-1.0, 1.0)):
		cyl(f"{n}_stick{i}", (side * 0.75, 0.55, 1.05), 0.06, 0.7, "iron", mallets, verts=6,
			rot=(0.5, 0, 0))
		ball(f"{n}_head{i}", (side * 0.75, 0.38, 1.32), (0.16, 0.16, 0.16), "lava", mallets)
	return g


def ember_bell(n):
	g = root(n)
	for side in (-1.0, 1.0):
		box(f"{n}_post{side}", (side * 0.68, 0, 0.85), (0.25, 0.25, 1.7), "basalt", g)
	box(n + "_yoke", (0, 0, 1.78), (1.75, 0.24, 0.2), "basalt_light", g)
	bell = root(n + "_Bell", g)
	cone(n + "_bell_body", (0, 0, 1.15), 0.62, 0.26, 0.9, "iron", bell, verts=12)
	cyl(n + "_bell_lip", (0, 0, 0.72), 0.66, 0.14, "basalt_light", bell, verts=12)
	striker = root(n + "_Striker", g)
	cyl(n + "_striker_rod", (0.95, 0, 1.0), 0.06, 0.8, "iron", striker, verts=6)
	ball(n + "_striker_head", (0.95, 0, 0.62), (0.15, 0.15, 0.15), "lava", striker)
	return g


def magma_lever(n):
	g = root(n)
	box(n + "_base", (0, 0, 0.2), (0.9, 0.7, 0.4), "basalt", g)
	box(n + "_column", (0, 0, 0.68), (0.42, 0.42, 0.6), "basalt_light", g)
	window = root(n + "_Window", g)   # state window child
	box(n + "_window", (0, -0.24, 0.7), (0.28, 0.06, 0.34), "lava", window, bevel=0.02)
	handle = root(n + "_Handle", g)
	cyl(n + "_handle_rod", (0, 0.12, 1.1), 0.07, 0.72, "iron", handle, verts=6, rot=(0.45, 0, 0))
	ball(n + "_handle_grip", (0, 0.42, 1.38), (0.16, 0.16, 0.16), "lava_hot", handle)
	return g


def pressure_plate(n):
	g = root(n)
	for i in range(8):
		a = math.tau * i / 8.0
		box(f"{n}_frame{i}", (math.cos(a) * 1.1, math.sin(a) * 1.1, 0.1),
			(0.7, 0.42, 0.2), "basalt", g, rot=(0, 0, a))
	centre = root(n + "_Center", g)   # raised/pressed centre child
	cyl(n + "_pad", (0, 0, 0.16), 0.85, 0.24, "basalt_light", centre, verts=12)
	cyl(n + "_glow", (0, 0, 0.29), 0.6, 0.06, "lava", centre, verts=12)
	return g


def flame_wheel(n):
	g = root(n)
	box(n + "_post", (0, 0, 0.75), (0.3, 0.3, 1.5), "basalt", g)
	cyl(n + "_axle", (0, 0, 1.5), 0.16, 0.5, "iron", g, verts=8, rot=(math.pi * 0.5, 0, 0))
	wheel = root(n + "_Wheel", g)
	cyl(n + "_hub", (0, 0, 1.5), 0.34, 0.3, "basalt_light", wheel, verts=10,
		rot=(math.pi * 0.5, 0, 0))
	flames = root(n + "_Flames", g)
	for i in range(6):
		a = math.tau * i / 6.0
		px, pz = math.cos(a) * 1.05, 1.5 + math.sin(a) * 1.05
		box(f"{n}_paddle{i}", (px, 0, pz), (0.9, 0.2, 0.42), "basalt", wheel, rot=(0, -a, 0))
		cone(f"{n}_flame{i}", (px * 1.32, 0, pz * 1.0 + 0.0), 0.2, 0.0, 0.55, "lava",
			flames, verts=5, rot=(0, -a + math.pi * 0.5, 0))
	return g


def heat_shield(n):
	g = root(n)
	box(n + "_face", (0, 0, 0.95), (1.15, 0.18, 1.6), "basalt", g)
	box(n + "_boss", (0, -0.14, 1.0), (0.55, 0.14, 0.55), "basalt_light", g)
	for i in range(3):
		vein(f"{n}_band{i}", g, (0, -0.12, 0.45 + i * 0.5), (0.95, 0.06, 0.09))
	handles = root(n + "_Handles", g)
	for z in (0.7, 1.25):
		box(f"{n}_grip{z}", (0, 0.2, z), (0.5, 0.14, 0.12), "iron", handles)
	return g


def ember_bloom(n):
	g = root(n)
	cyl(n + "_stalk", (0, 0, 0.3), 0.12, 0.6, "basalt", g, verts=6)
	petals = root(n + "_Petals", g)
	for i in range(5):
		a = math.tau * i / 5.0
		box(f"{n}_petal{i}", (math.cos(a) * 0.34, math.sin(a) * 0.34, 0.85),
			(0.3, 0.16, 0.6), "cap", petals,
			rot=(0.5 * math.sin(a), -0.5 * math.cos(a), a))
	centre = root(n + "_Center", g)
	ball(n + "_core", (0, 0, 0.98), (0.2, 0.2, 0.2), "lava_hot", centre)
	return g


# ---------------------------------------------------------------------------
# ambient + guidance (9)
# ---------------------------------------------------------------------------

def ash_fern(n):
	g = root(n)
	ball(n + "_crown", (0, 0, 0.16), (0.28, 0.28, 0.16), "basalt", g)
	for i in range(6):
		a = math.tau * i / 6.0
		lean = 0.85
		box(f"{n}_frond{i}", (math.cos(a) * 0.42, math.sin(a) * 0.42, 0.6),
			(0.2, 0.5, 0.9), "fern" if i % 2 == 0 else "fern_teal", g,
			rot=(lean * math.sin(a), -lean * math.cos(a), a), bevel=0.06)
	return g


def glow_moss(n):
	g = root(n)
	cyl(n + "_bed", (0, 0, 0.06), 1.0, 0.12, "basalt_dark", g, verts=10)
	spec = [(0.0, 0.0, 0.5), (0.42, 0.2, 0.38), (-0.35, 0.34, 0.34), (0.2, -0.42, 0.3),
		(-0.45, -0.25, 0.28), (0.55, -0.15, 0.24)]
	for i, (x, y, r) in enumerate(spec):
		ball(f"{n}_lobe{i}", (x, y, 0.14 + r * 0.4), (r, r, r * 0.62), "moss", g)
	for i in range(4):
		a = math.tau * i / 4.0 + 0.6
		cone(f"{n}_tip{i}", (math.cos(a) * 0.5, math.sin(a) * 0.5, 0.34), 0.06, 0.0, 0.26,
			"moss_tip", g, verts=5)
	return g


def cinder_fungus(n):
	g = root(n)
	for i, (x, y, h, r) in enumerate([(0.0, 0.0, 1.05, 0.42), (0.42, 0.2, 0.72, 0.3),
			(-0.36, 0.28, 0.55, 0.26)]):
		cyl(f"{n}_stem{i}", (x, y, h * 0.5), r * 0.32, h, "basalt", g, verts=6)
		cone(f"{n}_cap{i}", (x, y, h + 0.1), r, r * 0.3, 0.34, "cap", g, verts=8)
		cyl(f"{n}_gill{i}", (x, y, h - 0.11), r * 0.92, 0.09, "gill", g, verts=8)
	return g


def moth_cluster(n):
	g = root(n)
	ball(n + "_perch", (0, 0, 0.1), (0.34, 0.28, 0.12), "basalt", g)
	for i, (x, y, z, s) in enumerate([(0.0, 0.0, 0.35, 1.0), (0.3, 0.16, 0.22, 0.8),
			(-0.26, 0.2, 0.18, 0.72)]):
		moth = root(f"{n}_Moth{i}", g)
		ball(f"{n}_body{i}", (x, y, z), (0.07 * s, 0.13 * s, 0.07 * s), "basalt_dark", moth)
		for side in (-1.0, 1.0):
			box(f"{n}_wing{i}{side}", (x + side * 0.16 * s, y, z + 0.03 * s),
				(0.3 * s, 0.22 * s, 0.04 * s), "wing", moth,
				rot=(0.0, side * 0.4, side * 0.25), bevel=0.02)
	return g


def smoke_cluster(n):
	g = root(n)
	spec = [(0.0, 0.0, 0.5, 0.55), (0.3, 0.1, 1.0, 0.45), (-0.25, 0.18, 1.35, 0.4),
		(0.18, -0.2, 1.7, 0.32), (-0.1, 0.05, 1.95, 0.24)]
	for i, (x, y, z, r) in enumerate(spec):
		ball(f"{n}_lobe{i}", (x, y, z), (r, r, r * 0.85), "smoke", g)
	ball(n + "_root", (0, 0, 0.12), (0.35, 0.3, 0.14), "basalt_dark", g)
	return g


def lava_bubbles(n):
	g = root(n)
	cyl(n + "_rim", (0, 0, 0.12), 0.85, 0.24, "basalt", g, verts=10)
	cyl(n + "_pool", (0, 0, 0.22), 0.68, 0.1, "lava", g, verts=10)
	for i, (x, y, r) in enumerate([(0.0, 0.0, 0.34), (0.42, 0.12, 0.24), (-0.3, 0.3, 0.2)]):
		bub = root(f"{n}_Bubble{i}", g)
		cyl(f"{n}_neck{i}", (x, y, 0.35), r * 0.4, 0.3, "lava_deep", bub, verts=6)
		ball(f"{n}_dome{i}", (x, y, 0.55 + r * 0.6), (r, r, r), "lava_hot", bub)
	return g


def shimmer_totem(n):
	g = root(n)
	cyl(n + "_foot", (0, 0, 0.2), 0.62, 0.4, "basalt_dark", g, verts=8)
	bands = ["band_gold", "band_pink", "band_aqua", "band_gold"]
	for i in range(4):
		cyl(f"{n}_ring{i}", (0, 0, 0.5 + i * 0.5), 0.5, 0.18, "basalt", g, verts=8, bevel=0.0)
		cyl(f"{n}_wave{i}", (0, 0, 0.72 + i * 0.5), 0.42, 0.3, bands[i], g, verts=8, bevel=0.0)
	cyl(n + "_crown", (0, 0, 2.45), 0.55, 0.25, "basalt_light", g, verts=8)
	return g


def spark_trail(n):
	g = root(n)
	for i in range(6):
		t = i / 5.0
		x = -0.7 + t * 1.4
		y = math.sin(t * math.pi) * 0.28
		box(f"{n}_ribbon{i}", (x, y, 0.05), (0.3, 0.2, 0.1), "basalt_dark", g, bevel=0.03)
	sparks = root(n + "_Sparks", g)
	for i in range(5):
		t = (i + 0.5) / 5.0
		x = -0.65 + t * 1.3
		y = math.sin(t * math.pi) * 0.26
		cone(f"{n}_spark{i}", (x, y, 0.24), 0.08, 0.0, 0.28, "lava_hot", sparks, verts=5)
	return g


def comet_beacon(n):
	g = root(n)
	for i in range(3):
		a = math.tau * i / 3.0
		box(f"{n}_leg{i}", (math.cos(a) * 0.45, math.sin(a) * 0.45, 0.5),
			(0.28, 0.28, 1.0), "iron", g, rot=(0.16 * math.sin(a), -0.16 * math.cos(a), a))
	cyl(n + "_body", (0, 0, 1.25), 0.5, 0.7, "iron", g, verts=10)
	vein(n + "_body_vein", g, (0, -0.5, 1.25), (0.5, 0.06, 0.3))
	halo = root(n + "_Halo", g)   # addressable halo
	bpy.ops.mesh.primitive_torus_add(location=(0, 0, 2.5), major_radius=0.8,
		minor_radius=0.1, major_segments=16, minor_segments=6,
		rotation=(math.pi * 0.5, 0, 0))
	ring = bpy.context.active_object
	ring.name = n + "_halo_ring"
	for polygon in ring.data.polygons:
		polygon.use_smooth = True
	_finish(ring, "lava_hot", halo, 0.0)
	lens = root(n + "_Lens", g)   # addressable lens
	cone(n + "_lens_lower", (0, 0, 2.25), 0.3, 0.0, 0.6, "crystal", lens, verts=6,
		rot=(math.pi, 0, 0))
	cone(n + "_lens_upper", (0, 0, 2.75), 0.3, 0.0, 0.7, "crystal", lens, verts=6)
	return g


# export name -> (builder, keeps a node tree instead of one merged mesh)
ASSETS = {
	"ember_obsidian_bridge": (obsidian_bridge, False),
	"ember_basalt_archway": (basalt_archway, False),
	"ember_lava_aqueduct": (lava_aqueduct, False),
	"ember_balcony": (ember_balcony, False),
	"ember_gatehouse_buttress": (gatehouse_buttress, False),
	"ember_stair_module": (stair_module, False),
	"ember_parapet_corner": (parapet_corner, False),
	"ember_ash_chimney": (ash_chimney, False),
	"ember_plaza_brazier": (plaza_brazier, True),
	"ember_lavafall_cliff": (lavafall_cliff, True),
	"ember_magma_pool": (magma_pool, True),
	"ember_basalt_columns": (basalt_columns, False),
	"ember_ash_dune": (ash_dune, False),
	"ember_vent_cluster": (vent_cluster, False),
	"ember_obsidian_shards": (obsidian_shards, False),
	"ember_cooled_flow": (cooled_flow, False),
	"ember_cave_mouth": (cave_mouth, True),
	"ember_meteor_crater": (meteor_crater, False),
	"ember_cinder_island": (cinder_island, False),
	"ember_chain_anchor": (chain_anchor, False),
	"ember_forge_anvil": (forge_anvil, False),
	"ember_coal_cart": (coal_cart, True),
	"ember_urn": (ember_urn, False),
	"ember_drum": (volcanic_drum, True),
	"ember_bell": (ember_bell, True),
	"ember_magma_lever": (magma_lever, True),
	"ember_pressure_plate": (pressure_plate, True),
	"ember_flame_wheel": (flame_wheel, True),
	"ember_heat_shield": (heat_shield, True),
	"ember_bloom": (ember_bloom, True),
	"ember_ash_fern": (ash_fern, False),
	"ember_glow_moss": (glow_moss, False),
	"ember_cinder_fungus": (cinder_fungus, False),
	"ember_moth_cluster": (moth_cluster, True),
	"ember_smoke_cluster": (smoke_cluster, False),
	"ember_spark_trail": (spark_trail, True),
	"ember_lava_bubbles": (lava_bubbles, True),
	"ember_shimmer_totem": (shimmer_totem, False),
	"ember_crust_slab": (crust_slab, False),
	"ember_comet_beacon": (comet_beacon, True),
}


def family(obj):
	out = [obj]
	for child in obj.children:
		out += family(child)
	return out


def _merge(objects, name):
	bpy.ops.object.select_all(action="DESELECT")
	copies = []
	for member in objects:
		copy = member.copy()
		copy.data = member.data.copy()
		bpy.context.collection.objects.link(copy)
		copy.parent = None
		copy.matrix_world = member.matrix_world.copy()
		copies.append(copy)
	if not copies:
		return None
	for copy in copies:
		copy.select_set(True)
	bpy.context.view_layer.objects.active = copies[0]
	bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	return merged


def export_asset(name, obj, keep_tree):
	"""One merged mesh by default; a shallow named tree when the manifest asks
	for addressable state children (DungeonArt.find_part reads those names)."""
	temps = []
	if keep_tree:
		groups = {}
		for member in family(obj):
			if member.type != "MESH":
				continue
			owner = member.parent
			key = owner.name if owner is not None and owner.type == "EMPTY" and owner is not obj else name + "_Body"
			groups.setdefault(key, []).append(member)
		holder = bpy.data.objects.new(name, None)
		bpy.context.collection.objects.link(holder)
		temps.append(holder)
		for key, members in groups.items():
			merged = _merge(members, key)
			if merged is None:
				continue
			merged.parent = holder
			temps.append(merged)
		export_root = holder
	else:
		merged = _merge([m for m in family(obj) if m.type == "MESH"], name)
		if merged is None:
			return (0, 0, 0)
		temps.append(merged)
		export_root = merged
	bpy.ops.object.select_all(action="DESELECT")
	tris = 0
	mats = set()
	for temp in temps:
		temp.select_set(True)
		if temp.type == "MESH":
			temp.data.calc_loop_triangles()
			tris += len(temp.data.loop_triangles)
			for slot in temp.data.materials:
				if slot is not None:
					mats.add(slot.name)
	bpy.context.view_layer.objects.active = export_root
	bpy.ops.export_scene.gltf(filepath=str(ASSET_OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT",
		export_animations=False)
	children = max(len(temps) - 1, 0) if keep_tree else 0
	for temp in temps:
		bpy.data.objects.remove(temp, do_unlink=True)
	return (tris, len(mats), children)


def bounds(obj):
	points = []
	for member in family(obj):
		if member.type == "MESH":
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	if not points:
		return (Vector(), Vector())
	return (Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points))),
		Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points))))


def setup_render():
	scene = bpy.context.scene
	scene.render.engine = "CYCLES"
	scene.cycles.device = "CPU"
	scene.cycles.samples = 20
	scene.cycles.use_denoising = False
	scene.render.resolution_x = 512
	scene.render.resolution_y = 512
	scene.world = bpy.data.worlds.new("EMX_world")
	scene.world.use_nodes = True
	bg = scene.world.node_tree.nodes["Background"]
	# A bright cream sheet at full strength washes dark basalt to grey (the
	# first QA pass did exactly that). Keep a light card for silhouette
	# reading, but dim it and add a warm rim so the plum stone and the hot
	# veins read at their authored values.
	bg.inputs[0].default_value = (0.62, 0.60, 0.66, 1.0)
	bg.inputs[1].default_value = 0.32
	key = bpy.data.lights.new("EMX_key", "SUN")
	key.energy = 2.6
	key_obj = bpy.data.objects.new("EMX_key", key)
	key_obj.rotation_euler = (math.radians(54.0), 0.0, math.radians(40.0))
	bpy.context.collection.objects.link(key_obj)
	rim = bpy.data.lights.new("EMX_rim", "SUN")
	rim.energy = 1.5
	rim.color = (1.0, 0.62, 0.32)
	rim_obj = bpy.data.objects.new("EMX_rim", rim)
	rim_obj.rotation_euler = (math.radians(72.0), 0.0, math.radians(-128.0))
	bpy.context.collection.objects.link(rim_obj)
	cam_data = bpy.data.cameras.new("EMX_cam")
	cam_data.type = "ORTHO"
	cam = bpy.data.objects.new("EMX_cam", cam_data)
	bpy.context.collection.objects.link(cam)
	scene.camera = cam
	return cam


def render_qa(cam, name, obj):
	low, high = bounds(obj)
	centre = (low + high) * 0.5
	size = max((high - low).x, (high - low).y, (high - low).z, 0.6)
	cam.data.ortho_scale = size * 1.4
	for label, angle in (("front", 0.0), ("three_quarter", math.radians(48.0))):
		distance = size * 3.0
		cam.location = (centre.x + math.sin(angle) * distance,
			centre.y - math.cos(angle) * distance, centre.z + size * 0.4)
		direction = centre - Vector(cam.location)
		cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
		bpy.context.scene.render.filepath = str(QA_OUT / f"{name}_{label}.png")
		bpy.ops.render.render(write_still=True)


def main():
	budgets = {}
	contracts = {}
	with open(MANIFEST, newline="", encoding="utf-8") as handle:
		for row in csv.DictReader(handle):
			stem = row["export_name"].replace(".glb", "")
			budgets[stem] = int(row["triangle_budget_max"])
			contracts[stem] = row
	report = []
	built = []
	over = []
	for name, (builder, keep_tree) in ASSETS.items():
		if ONLY_ASSET and name != ONLY_ASSET:
			continue
		obj = builder(name)
		tris, mats, children = export_asset(name, obj, keep_tree)
		low, high = bounds(obj)
		budget = budgets.get(name, 0)
		if budget and tris > budget:
			over.append((name, tris, budget))
		report.append((name, tris, budget, mats, children, high - low))
		built.append((name, obj))
	bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
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
	except Exception as exc:
		print("EMBER_EXPANSION | QA_RENDER_SKIPPED |", exc)
	print("\nEMBER_EXPANSION | asset | triangles | budget | materials | state_children | size")
	total = 0
	for name, tris, budget, mats, children, size in report:
		total += tris
		flag = "OVER" if budget and tris > budget else "ok"
		print(f"EMBER_EXPANSION | {name} | {tris} | {budget} | {mats} | {children} | "
			f"{size.x:.2f},{size.y:.2f},{size.z:.2f} | {flag}")
	print(f"EMBER_EXPANSION | TOTAL | {len(report)} assets | {total} triangles | "
		f"over_budget={len(over)}")
	for name, tris, budget in over:
		print(f"EMBER_EXPANSION | OVER_BUDGET | {name} | {tris} > {budget}")


main()
