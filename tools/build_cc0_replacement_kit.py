#!/usr/bin/env python3
"""Build authored replacements for the remaining live CC0/CC-BY world assets.

Companion to CC0_REPLACEMENT_WORKORDER_2026-07-22.md. Every piece here
replaces a still-referenced Kenney/Tiny Treats/Quaternius/poly.pizza file,
following the same texture-free flat-material, storybook-toon language as
the pearl-castle and Northern Kingdom kits. No protected book, voice,
friend, or character asset is read or modified.

Usage: python3 tools/build_cc0_replacement_kit.py
  (bpy installed via `pip install bpy==4.4.0`; no Blender app needed)
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
GEN2_OUT = ROOT / "assets" / "props" / "gen2"
VEHICLE_OUT = ROOT / "assets" / "vehicles"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_cc0_replacement_kit"
BLEND_OUT = SOURCE_OUT / "cc0_replacement_kit.blend"
for folder in (GEN2_OUT, VEHICLE_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
	"ink": (0.10, 0.08, 0.22, 1.0),
	"midnight": (0.11, 0.18, 0.32, 1.0),
	"slate": (0.42, 0.47, 0.64, 1.0),
	"stone": (0.62, 0.60, 0.66, 1.0),
	"stone_light": (0.78, 0.76, 0.82, 1.0),
	"lavender": (0.66, 0.55, 0.76, 1.0),
	"pearl": (0.91, 0.88, 0.83, 1.0),
	"gold": (0.92, 0.66, 0.22, 1.0),
	"coral": (0.89, 0.43, 0.47, 1.0),
	"cherry": (0.85, 0.22, 0.30, 1.0),
	"peach": (0.96, 0.65, 0.48, 1.0),
	"yellow": (0.96, 0.80, 0.35, 1.0),
	"mint": (0.48, 0.77, 0.62, 1.0),
	"leaf": (0.35, 0.66, 0.50, 1.0),
	"leaf_dark": (0.22, 0.48, 0.36, 1.0),
	"aqua": (0.30, 0.72, 0.76, 1.0),
	"sky": (0.43, 0.64, 0.86, 1.0),
	"wood": (0.62, 0.42, 0.28, 1.0),
	"wood_light": (0.78, 0.58, 0.40, 1.0),
	"sail": (0.93, 0.90, 0.86, 1.0),
	"ghost": (0.72, 0.80, 0.88, 1.0),
	"crystal_pink": (0.86, 0.55, 0.86, 1.0),
	"crystal_blue": (0.52, 0.72, 0.96, 1.0),
	"crystal_mint": (0.55, 0.90, 0.80, 1.0),
	"chrome": (0.85, 0.87, 0.92, 1.0),
	"tire": (0.20, 0.20, 0.24, 1.0),
}


def make_material(name: str, color, roughness: float = 0.82,
		metallic: float = 0.0, emission: float = 0.0) -> bpy.types.Material:
	mat = bpy.data.materials.new("CC0KIT_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = roughness
	bsdf.inputs["Metallic"].default_value = metallic
	if emission > 0.0 and "Emission Color" in bsdf.inputs:
		bsdf.inputs["Emission Color"].default_value = color
		bsdf.inputs["Emission Strength"].default_value = emission
	return mat


MATS = {name: make_material(name, color) for name, color in PALETTE.items()}
MATS["gold"] = make_material("gold", PALETTE["gold"], 0.42, 0.2)
MATS["chrome"] = make_material("chrome", PALETTE["chrome"], 0.25, 0.55)
MATS["tire"] = make_material("tire", PALETTE["tire"], 0.95, 0.0)
for glow in ("crystal_pink", "crystal_blue", "crystal_mint", "aqua"):
	MATS[glow] = make_material(glow, PALETTE[glow], 0.35, 0.0, 0.35)
MATS["ghost"] = make_material("ghost", PALETTE["ghost"], 0.55, 0.0, 0.10)


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def assign(obj: bpy.types.Object, mat: bpy.types.Material,
		parent: bpy.types.Object) -> bpy.types.Object:
	obj.data.materials.append(mat)
	obj.parent = parent
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def rounded_box(name, loc, size, mat, parent, radius=0.14, rotation=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = size
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	bevel = obj.modifiers.new("storybook_rounding", "BEVEL")
	bevel.width = min(radius, min(size) * 0.2)
	bevel.segments = 2
	bevel.limit_method = "ANGLE"
	apply_modifier(obj, bevel)
	return obj


def cylinder(name, loc, radius, depth, mat, parent, vertices=14, rotation=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
		location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return obj


def cone(name, loc, radius1, radius2, depth, mat, parent, vertices=12, rotation=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2,
		depth=depth, location=loc, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return obj


def sphere(name, loc, radius, mat, parent, segments=12, rings=8, scale=(1.0, 1.0, 1.0)):
	bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius,
		location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	assign(obj, mat, parent)
	return obj


def torus(name, loc, major_radius, minor_radius, mat, parent, rotation=(0.0, 0.0, 0.0)):
	bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=major_radius,
		minor_radius=minor_radius, major_segments=16, minor_segments=8, rotation=rotation)
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return obj


def prism(name, loc, size, mat, parent, rotation=(0.0, 0.0, 0.0)):
	# low-poly gem facet: an octahedron squashed into a crystal spike
	bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=size[0], radius2=0.0,
		depth=size[2], location=(loc[0], loc[1], loc[2] + size[2] * 0.25), rotation=rotation)
	top = bpy.context.active_object
	bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=size[0], radius2=0.0,
		depth=size[2] * 0.4, location=(loc[0], loc[1], loc[2] - size[2] * 0.05),
		rotation=(rotation[0] + math.pi, rotation[1], rotation[2]))
	bottom = bpy.context.active_object
	bpy.ops.object.select_all(action="DESELECT")
	top.select_set(True)
	bottom.select_set(True)
	bpy.context.view_layer.objects.active = top
	bpy.ops.object.join()
	obj = bpy.context.active_object
	obj.name = name
	assign(obj, mat, parent)
	return obj


# ------------------------------------------------------------- vehicles

def build_gokart() -> bpy.types.Object:
	r = root("gokart_story")
	rounded_box("Kart_Body", (0.0, 0.0, 0.55), (2.6, 1.35, 0.6), MATS["cherry"], r, 0.18)
	rounded_box("Kart_Nose", (1.35, 0.0, 0.5), (0.7, 1.0, 0.42), MATS["yellow"], r, 0.16)
	rounded_box("Kart_Seat", (-0.35, 0.0, 0.95), (0.85, 0.95, 0.55), MATS["ink"], r, 0.14)
	torus("Kart_Wheel", (0.0, 0.0, 0.0), 0.01, 0.01, MATS["tire"], r)  # placeholder removed below
	bpy.data.objects.remove(bpy.data.objects["Kart_Wheel"], do_unlink=True)
	for sx, sy in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)):
		wx = 0.95 * sx
		wy = 0.85 * sy
		cylinder("Kart_Wheel_%d_%d" % (sx, sy), (wx, wy, 0.42), 0.42, 0.32, MATS["tire"], r,
			rotation=(math.pi / 2.0, 0.0, 0.0))
		cylinder("Kart_Hub_%d_%d" % (sx, sy), (wx, wy + 0.02 * sy, 0.42), 0.18, 0.10, MATS["chrome"], r,
			rotation=(math.pi / 2.0, 0.0, 0.0))
	torus("Kart_Wheel_Ring", (1.35, 0.0, 1.05), 0.32, 0.045, MATS["chrome"], r,
		rotation=(math.pi / 2.0, 0.0, 0.0))
	cylinder("Kart_Column", (1.15, 0.0, 0.85), 0.05, 0.35, MATS["chrome"], r,
		rotation=(0.0, math.radians(35.0), 0.0))
	rounded_box("Kart_Spoiler_Post_L", (-1.15, 0.55, 0.85), (0.06, 0.06, 0.55), MATS["ink"], r, 0.02)
	rounded_box("Kart_Spoiler_Post_R", (-1.15, -0.55, 0.85), (0.06, 0.06, 0.55), MATS["ink"], r, 0.02)
	rounded_box("Kart_Spoiler", (-1.15, 0.0, 1.15), (0.32, 1.35, 0.14), MATS["cherry"], r, 0.06)
	return r


def build_motorcycle() -> bpy.types.Object:
	r = root("motorcycle_story")
	rounded_box("Moto_Body", (0.0, 0.0, 0.62), (1.55, 0.42, 0.36), MATS["sky"], r, 0.14)
	rounded_box("Moto_Tank", (0.35, 0.0, 0.92), (0.55, 0.38, 0.34), MATS["sky"], r, 0.16)
	rounded_box("Moto_Seat", (-0.4, 0.0, 0.92), (0.7, 0.36, 0.16), MATS["ink"], r, 0.08)
	cylinder("Moto_Wheel_F", (1.1, 0.0, 0.5), 0.5, 0.28, MATS["tire"], r,
		rotation=(math.pi / 2.0, 0.0, 0.0))
	cylinder("Moto_Wheel_R", (-1.1, 0.0, 0.5), 0.5, 0.28, MATS["tire"], r,
		rotation=(math.pi / 2.0, 0.0, 0.0))
	for wx in (1.1, -1.1):
		cylinder("Moto_Hub_%d" % int(wx * 10), (wx, 0.0, 0.5), 0.16, 0.30, MATS["chrome"], r,
			rotation=(math.pi / 2.0, 0.0, 0.0))
	cylinder("Moto_Fork", (1.1, 0.0, 0.85), 0.05, 0.75, MATS["chrome"], r,
		rotation=(0.0, math.radians(-20.0), 0.0))
	rounded_box("Moto_Handlebar", (1.35, 0.0, 1.2), (0.06, 0.55, 0.06), MATS["chrome"], r, 0.03)
	sphere("Moto_Headlight", (1.5, 0.0, 0.95), 0.15, MATS["chrome"], r)
	rounded_box("Moto_Exhaust", (-0.5, 0.22, 0.42), (0.65, 0.12, 0.12), MATS["chrome"], r, 0.05)
	return r


# ------------------------------------------------------------- galaxy landmarks

def build_crystal(name: str, mat_key: str, height: float) -> bpy.types.Object:
	r = root(name)
	prism("%s_Spike" % name, (0.0, 0.0, height * 0.5), (height * 0.32, height * 0.32, height),
		MATS[mat_key], r)
	prism("%s_Spike_Small_A" % name, (height * 0.28, height * 0.1, height * 0.28),
		(height * 0.14, height * 0.14, height * 0.5), MATS[mat_key], r,
		rotation=(0.0, math.radians(12.0), math.radians(35.0)))
	prism("%s_Spike_Small_B" % name, (-height * 0.22, -height * 0.18, height * 0.22),
		(height * 0.11, height * 0.11, height * 0.4), MATS[mat_key], r,
		rotation=(0.0, math.radians(-8.0), math.radians(-50.0)))
	cylinder("%s_Base" % name, (0.0, 0.0, 0.05), height * 0.34, 0.1, MATS["stone"], r)
	return r


def build_crystal_castle() -> bpy.types.Object:
	r = root("crystal_castle")
	cylinder("Castle_Keep", (0.0, 0.0, 2.2), 2.4, 4.4, MATS["pearl"], r)
	cone("Castle_Roof", (0.0, 0.0, 5.0), 2.7, 0.0, 2.4, MATS["lavender"], r)
	for sx, sy in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)):
		tx, ty = 2.1 * sx, 2.1 * sy
		cylinder("Castle_Turret_%d_%d" % (sx, sy), (tx, ty, 2.6), 0.85, 5.2, MATS["pearl"], r)
		cone("Castle_Turret_Roof_%d_%d" % (sx, sy), (tx, ty, 5.4), 1.0, 0.0, 1.4, MATS["lavender"], r)
		prism("Castle_Turret_Crystal_%d_%d" % (sx, sy), (tx, ty, 6.4), (0.3, 0.3, 1.1),
			MATS["crystal_blue"], r)
	prism("Castle_Spire_Crystal", (0.0, 0.0, 6.5), (0.55, 0.55, 2.0), MATS["crystal_pink"], r)
	rounded_box("Castle_Gate", (2.35, 0.0, 0.9), (0.5, 1.1, 1.8), MATS["gold"], r, 0.1)
	return r


def build_galaxy_tray() -> bpy.types.Object:
	r = root("galaxy_tray")
	cylinder("Tray_Base", (0.0, 0.0, 0.08), 1.55, 0.16, MATS["pearl"], r)
	cylinder("Tray_Rim", (0.0, 0.0, 0.2), 1.55, 0.08, MATS["gold"], r, vertices=18)
	cylinder("Tray_Well", (0.0, 0.0, 0.06), 1.25, 0.12, MATS["lavender"], r)
	return r


# ------------------------------------------------------------- nature rocks

def build_cliff_rock(name: str, bumps: int, base_radius: float) -> bpy.types.Object:
	r = root(name)
	rounded_box("%s_Core" % name, (0.0, 0.0, base_radius * 0.55), (base_radius, base_radius * 0.85, base_radius * 0.55),
		MATS["stone"], r, base_radius * 0.28)
	import random
	rng = random.Random(hash(name) & 0xFFFF)
	for i in range(bumps):
		ang = rng.uniform(0.0, math.tau)
		dist = rng.uniform(base_radius * 0.35, base_radius * 0.75)
		bx = math.cos(ang) * dist
		by = math.sin(ang) * dist
		bz = rng.uniform(base_radius * 0.25, base_radius * 0.7)
		bs = rng.uniform(base_radius * 0.28, base_radius * 0.5)
		rounded_box("%s_Bump_%d" % (name, i), (bx, by, bz), (bs, bs * rng.uniform(0.8, 1.2), bs),
			MATS["stone_light"] if i % 2 == 0 else MATS["stone"], r, bs * 0.35,
			rotation=(0.0, 0.0, rng.uniform(0.0, math.tau)))
	return r


# ------------------------------------------------------------- ship props

def build_ship_wreck() -> bpy.types.Object:
	r = root("ship_wreck")
	rounded_box("Wreck_Hull", (0.0, 0.0, 0.9), (4.4, 1.5, 1.1), MATS["wood"], r, 0.3,
		rotation=(math.radians(8.0), 0.0, math.radians(4.0)))
	rounded_box("Wreck_Bow", (2.4, 0.0, 1.1), (1.0, 1.1, 0.9), MATS["wood_light"], r, 0.3,
		rotation=(0.0, math.radians(-18.0), 0.0))
	rounded_box("Wreck_Deck_Break", (-0.6, 0.0, 1.55), (1.6, 1.15, 0.28), MATS["wood_light"], r, 0.1)
	cylinder("Wreck_Mast_Stump", (-1.6, 0.2, 1.9), 0.15, 1.4, MATS["wood"], r,
		rotation=(math.radians(20.0), math.radians(10.0), 0.0))
	rounded_box("Wreck_Rib_A", (0.9, 0.7, 1.6), (0.1, 0.1, 1.0), MATS["wood"], r, 0.03,
		rotation=(math.radians(-25.0), 0.0, 0.0))
	rounded_box("Wreck_Rib_B", (0.5, -0.7, 1.55), (0.1, 0.1, 0.9), MATS["wood"], r, 0.03,
		rotation=(math.radians(25.0), 0.0, 0.0))
	return r


def build_ship_chest() -> bpy.types.Object:
	r = root("ship_chest")
	rounded_box("Chest_Body", (0.0, 0.0, 0.42), (1.0, 0.68, 0.55), MATS["wood"], r, 0.1)
	cylinder("Chest_Lid", (0.0, 0.0, 0.72), 0.5, 1.0, MATS["wood_light"], r, vertices=16,
		rotation=(0.0, math.radians(90.0), 0.0))
	rounded_box("Chest_Band_A", (0.0, 0.32, 0.42), (1.02, 0.06, 0.58), MATS["gold"], r, 0.03)
	rounded_box("Chest_Band_B", (0.0, -0.32, 0.42), (1.02, 0.06, 0.58), MATS["gold"], r, 0.03)
	rounded_box("Chest_Latch", (0.5, 0.0, 0.55), (0.08, 0.18, 0.2), MATS["gold"], r, 0.04)
	return r


def build_ship_barrel() -> bpy.types.Object:
	r = root("ship_barrel")
	cylinder("Barrel_Body", (0.0, 0.0, 0.5), 0.42, 1.0, MATS["wood"], r, vertices=14)
	bulge = cylinder("Barrel_Bulge", (0.0, 0.0, 0.5), 0.47, 0.6, MATS["wood"], r, vertices=14)
	for hz in (0.15, 0.5, 0.85):
		cylinder("Barrel_Band_%d" % int(hz * 100), (0.0, 0.0, hz), 0.44, 0.05, MATS["ink"], r, vertices=14)
	return r


def build_ship_ghost() -> bpy.types.Object:
	r = root("ship_ghost")
	rounded_box("Ghost_Hull", (0.0, 0.0, 0.6), (2.6, 0.9, 0.65), MATS["ghost"], r, 0.22)
	cylinder("Ghost_Mast", (0.0, 0.0, 2.3), 0.08, 3.4, MATS["ghost"], r)
	rounded_box("Ghost_Sail", (0.55, 0.0, 2.6), (0.06, 1.5, 1.9), MATS["sail"], r, 0.05,
		rotation=(0.0, 0.0, math.radians(6.0)))
	rounded_box("Ghost_Sail_Small", (-0.15, 0.0, 3.9), (0.05, 0.9, 1.0), MATS["sail"], r, 0.04)
	cone("Ghost_Bow", (1.5, 0.0, 0.65), 0.6, 0.05, 1.0, MATS["ghost"], r,
		rotation=(0.0, math.radians(90.0), 0.0))
	return r


# ------------------------------------------------------------- castle/park/furniture kit

def build_kit_tower_square() -> bpy.types.Object:
	r = root("kit_tower_square")
	rounded_box("Tower_Shaft", (0.0, 0.0, 2.6), (1.7, 1.7, 5.2), MATS["stone_light"], r, 0.14)
	cone("Tower_Roof", (0.0, 0.0, 5.9), 1.5, 0.0, 2.0, MATS["lavender"], r, vertices=4,
		rotation=(0.0, 0.0, math.radians(45.0)))
	for sx, sy in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)):
		rounded_box("Tower_Crenel_%d_%d" % (sx, sy), (sx * 0.75, sy * 0.75, 5.35), (0.28, 0.28, 0.4),
			MATS["stone"], r, 0.06)
	rounded_box("Tower_Door", (0.0, 0.87, 0.9), (0.5, 0.14, 1.5), MATS["wood"], r, 0.08)
	return r


def build_kit_flag() -> bpy.types.Object:
	r = root("kit_flag")
	cylinder("Flag_Pole", (0.0, 0.0, 1.0), 0.05, 2.0, MATS["wood"], r)
	rounded_box("Flag_Banner_A", (0.28, 0.0, 1.6), (0.5, 0.02, 0.4), MATS["coral"], r, 0.03,
		rotation=(0.0, 0.0, math.radians(-6.0)))
	rounded_box("Flag_Banner_B", (0.28, 0.0, 1.3), (0.42, 0.02, 0.32), MATS["gold"], r, 0.03,
		rotation=(0.0, 0.0, math.radians(4.0)))
	sphere("Flag_Finial", (0.0, 0.0, 2.05), 0.09, MATS["gold"], r)
	return r


def build_kit_wall() -> bpy.types.Object:
	r = root("kit_wall")
	rounded_box("Wall_Body", (0.0, 0.0, 1.6), (3.6, 0.6, 3.2), MATS["stone_light"], r, 0.12)
	for i in range(5):
		x = -1.5 + i * 0.75
		rounded_box("Wall_Crenel_%d" % i, (x, 0.0, 3.35), (0.3, 0.62, 0.35), MATS["stone"], r, 0.06)
	return r


def build_kit_bench() -> bpy.types.Object:
	r = root("kit_bench")
	rounded_box("Bench_Seat", (0.0, 0.0, 0.5), (1.6, 0.55, 0.1), MATS["wood"], r, 0.05)
	rounded_box("Bench_Back", (-0.65, 0.0, 0.85), (0.1, 0.55, 0.6), MATS["wood"], r, 0.05,
		rotation=(0.0, math.radians(-8.0), 0.0))
	for sx, sy in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)):
		rounded_box("Bench_Leg_%d_%d" % (sx, sy), (sx * 0.65, sy * 0.2, 0.25), (0.08, 0.08, 0.5),
			MATS["wood_light"], r, 0.02)
	return r


def build_kit_fountain() -> bpy.types.Object:
	r = root("kit_fountain")
	cylinder("Fountain_Basin", (0.0, 0.0, 0.35), 1.6, 0.7, MATS["stone_light"], r, vertices=18)
	cylinder("Fountain_Basin_Rim", (0.0, 0.0, 0.65), 1.6, 0.14, MATS["stone"], r, vertices=18)
	cylinder("Fountain_Pedestal", (0.0, 0.0, 1.1), 0.3, 0.8, MATS["stone"], r)
	cylinder("Fountain_Bowl", (0.0, 0.0, 1.6), 0.75, 0.28, MATS["stone_light"], r, vertices=16)
	cylinder("Fountain_Water", (0.0, 0.0, 1.68), 0.6, 0.06, MATS["aqua"], r, vertices=16)
	sphere("Fountain_Spout", (0.0, 0.0, 1.85), 0.14, MATS["aqua"], r)
	return r


def build_kit_hedge(name: str, length: float) -> bpy.types.Object:
	r = root(name)
	rounded_box("%s_Body" % name, (0.0, 0.0, 0.5), (length, 0.5, 0.9), MATS["leaf"], r, 0.22)
	import random
	rng = random.Random(hash(name) & 0xFFFF)
	bumps = max(3, int(length))
	for i in range(bumps):
		x = -length * 0.42 + (length * 0.84) * (i / max(bumps - 1, 1))
		sphere("%s_Bump_%d" % (name, i), (x, 0.0, 0.92), rng.uniform(0.22, 0.32),
			MATS["leaf_dark"] if i % 2 == 0 else MATS["leaf"], r, segments=8, rings=6)
	return r


def build_kit_bookcase() -> bpy.types.Object:
	r = root("kit_bookcase")
	rounded_box("Bookcase_Frame", (0.0, 0.0, 1.1), (0.35, 1.3, 2.2), MATS["wood"], r, 0.08)
	for i, hz in enumerate((0.35, 0.9, 1.45, 1.95)):
		rounded_box("Bookcase_Shelf_%d" % i, (0.02, 0.0, hz), (0.3, 1.22, 0.06), MATS["wood_light"], r, 0.02)
	colors = ("coral", "mint", "sky", "gold", "lavender")
	for i in range(6):
		by = -0.95 + i * 0.35
		bc = colors[i % len(colors)]
		rounded_box("Bookcase_Book_%d" % i, (0.05, by, 0.65), (0.24, 0.12, 0.4), MATS[bc], r, 0.03)
	return r


def build_kit_chair() -> bpy.types.Object:
	r = root("kit_chair")
	rounded_box("Chair_Seat", (0.0, 0.0, 0.45), (0.5, 0.5, 0.08), MATS["wood_light"], r, 0.05)
	rounded_box("Chair_Back", (-0.2, 0.0, 0.8), (0.08, 0.48, 0.6), MATS["wood_light"], r, 0.05,
		rotation=(0.0, math.radians(-6.0), 0.0))
	for sx, sy in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)):
		rounded_box("Chair_Leg_%d_%d" % (sx, sy), (sx * 0.19, sy * 0.19, 0.22), (0.06, 0.06, 0.44),
			MATS["wood"], r, 0.02)
	return r


def build_kit_table() -> bpy.types.Object:
	r = root("kit_table")
	rounded_box("Table_Top", (0.0, 0.0, 0.75), (1.4, 1.4, 0.12), MATS["wood_light"], r, 0.06)
	cylinder("Table_Pedestal", (0.0, 0.0, 0.37), 0.22, 0.74, MATS["wood"], r)
	cylinder("Table_Base", (0.0, 0.0, 0.06), 0.55, 0.1, MATS["wood"], r, vertices=16)
	return r


ASSETS = {
	# vehicles -> assets/vehicles/*_story.glb (primary; existing files stay as legacy_glb)
	"gokart_story": (build_gokart(), VEHICLE_OUT),
	"motorcycle_story": (build_motorcycle(), VEHICLE_OUT),
	# galaxy landmarks -> assets/props/gen2/
	"crystal1": (build_crystal("crystal1", "crystal_pink", 1.6), GEN2_OUT),
	"crystal2": (build_crystal("crystal2", "crystal_blue", 1.9), GEN2_OUT),
	"crystal3": (build_crystal("crystal3", "crystal_mint", 1.4), GEN2_OUT),
	"crystal_castle": (build_crystal_castle(), GEN2_OUT),
	"galaxy_tray": (build_galaxy_tray(), GEN2_OUT),
	# nature rocks -> assets/props/gen2/ (wired via NATURE_GEN2)
	"cliffrock_block": (build_cliff_rock("cliffrock_block", 5, 1.1), GEN2_OUT),
	"cliffrock_large": (build_cliff_rock("cliffrock_large", 7, 1.6), GEN2_OUT),
	"rock_boulder": (build_cliff_rock("rock_boulder", 4, 0.9), GEN2_OUT),
	# ship props -> assets/props/gen2/
	"ship_wreck": (build_ship_wreck(), GEN2_OUT),
	"ship_chest": (build_ship_chest(), GEN2_OUT),
	"ship_barrel": (build_ship_barrel(), GEN2_OUT),
	"ship_ghost": (build_ship_ghost(), GEN2_OUT),
	# castle/park/furniture kit -> assets/props/gen2/ (wired via KIT_GEN2)
	"kit_tower_square": (build_kit_tower_square(), GEN2_OUT),
	"kit_flag": (build_kit_flag(), GEN2_OUT),
	"kit_wall": (build_kit_wall(), GEN2_OUT),
	"kit_bench": (build_kit_bench(), GEN2_OUT),
	"kit_fountain": (build_kit_fountain(), GEN2_OUT),
	"kit_hedge": (build_kit_hedge("kit_hedge", 2.2), GEN2_OUT),
	"kit_hedge_long": (build_kit_hedge("kit_hedge_long", 4.4), GEN2_OUT),
	"kit_bookcase": (build_kit_bookcase(), GEN2_OUT),
	"kit_chair": (build_kit_chair(), GEN2_OUT),
	"kit_table": (build_kit_table(), GEN2_OUT),
}


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	result = [obj]
	for child in obj.children:
		result += family(child)
	return result


def bounds(obj: bpy.types.Object):
	points = []
	for member in family(obj):
		if member.type in {"MESH", "CURVE"}:
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	return (
		Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points))),
		Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points))),
	)


def export_asset(name: str, obj: bpy.types.Object, out_dir: Path) -> int:
	bpy.ops.object.select_all(action="DESELECT")
	export_meshes = []
	for member in family(obj):
		if member.type not in {"MESH", "CURVE"}:
			continue
		copy = member.copy()
		copy.data = member.data.copy()
		bpy.context.collection.objects.link(copy)
		copy.parent = None
		copy.matrix_world = member.matrix_world.copy()
		if copy.type == "CURVE":
			copy.select_set(True)
			bpy.context.view_layer.objects.active = copy
			bpy.ops.object.convert(target="MESH")
			copy = bpy.context.active_object
			copy.select_set(False)
		export_meshes.append(copy)
	bpy.ops.object.select_all(action="DESELECT")
	for mesh in export_meshes:
		mesh.select_set(True)
	bpy.context.view_layer.objects.active = export_meshes[0]
	if len(export_meshes) > 1:
		bpy.ops.object.join()
	merged = bpy.context.active_object
	merged.name = name
	merged.data.calc_loop_triangles()
	triangles = len(merged.data.loop_triangles)
	bpy.ops.export_scene.gltf(
		filepath=str(out_dir / (name + ".glb")),
		export_format="GLB",
		export_yup=True,
		use_selection=True,
		export_apply=True,
		export_materials="EXPORT",
		export_animations=False,
	)
	bpy.data.objects.remove(merged, do_unlink=True)
	return triangles


for asset_name, (asset_obj, out_dir) in ASSETS.items():
	triangle_count = export_asset(asset_name, asset_obj, out_dir)
	lo, hi = bounds(asset_obj)
	print("CC0KIT|%s|triangles=%d|bounds=%s..%s" % (
		asset_name, triangle_count,
		tuple(round(v, 2) for v in lo), tuple(round(v, 2) for v in hi)))
	if triangle_count > 6000:
		raise RuntimeError("%s exceeds the 6k triangle prop budget" % asset_name)
	for member in family(asset_obj):
		member.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 780
scene.render.resolution_y = 660
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = True
scene.view_settings.look = "AgX - Medium High Contrast"
bpy.ops.object.camera_add(location=(12.0, -18.0, 10.0))
camera = bpy.context.active_object
camera.data.lens = 58
scene.camera = camera
for location, energy, size, color in (
	((8.0, -10.0, 16.0), 1150.0, 8.0, (0.85, 0.94, 1.0)),
	((-10.0, -4.0, 9.0), 780.0, 6.0, (0.72, 0.82, 1.0)),
	((4.0, 9.0, 12.0), 900.0, 6.0, (1.0, 0.76, 0.62)),
):
	bpy.ops.object.light_add(type="AREA", location=location)
	light = bpy.context.active_object
	light.data.energy = energy
	light.data.shape = "DISK"
	light.data.size = size
	light.data.color = color
if scene.world is None:
	scene.world = bpy.data.worlds.new("CC0 Kit QA World")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.055, 0.10, 1.0)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.36

for asset_name, (asset_obj, out_dir) in ASSETS.items():
	for member in family(asset_obj):
		member.hide_render = False
	lo, hi = bounds(asset_obj)
	center = (lo + hi) * 0.5
	size = hi - lo
	distance = max(size.x, size.y, size.z, 0.5) * 1.9
	camera.location = center + Vector((distance * 0.72, -distance * 1.30, distance * 0.55))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
	for member in family(asset_obj):
		member.hide_render = True

print("CC0KIT|assets|%d" % len(ASSETS))
print("CC0KIT|blend|%s" % BLEND_OUT)
