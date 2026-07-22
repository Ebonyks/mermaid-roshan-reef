#!/usr/bin/env python3
"""Build the texture-free Ember Fortress overworld and dungeon art kit.

Run with Blender 4.5+ or the pinned bpy wheel. The output is deterministic:
runtime GLBs, the editable .blend source, isolated QA renders, three contact
sheets, and a machine-readable metrics CSV. All geometry is original project
work and uses only embedded flat materials.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "ember_fortress"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_ember_fortress_kit"
BLEND_OUT = SOURCE_OUT / "ember_fortress_kit.blend"
METRICS_OUT = QA_OUT / "ember_fortress_kit_metrics.csv"
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
random.seed(74021)

PALETTE = {
	"ink": (0.035, 0.045, 0.095, 1.0),
	"outline": (0.10, 0.075, 0.18, 1.0),
	"basalt": (0.20, 0.16, 0.29, 1.0),
	"basalt_mid": (0.30, 0.23, 0.40, 1.0),
	"basalt_light": (0.43, 0.34, 0.52, 1.0),
	"ash": (0.55, 0.47, 0.59, 1.0),
	"cream": (0.96, 0.88, 0.70, 1.0),
	"ember": (1.0, 0.35, 0.10, 1.0),
	"gold": (1.0, 0.69, 0.20, 1.0),
	"hot": (0.95, 0.45, 0.12, 1.0),
	"coral": (0.98, 0.39, 0.32, 1.0),
	"lavender": (0.55, 0.39, 0.76, 1.0),
	"aqua": (0.25, 0.75, 0.78, 1.0),
	"mint": (0.42, 0.78, 0.56, 1.0),
	"ice": (0.43, 0.84, 0.96, 1.0),
	"berry": (0.49, 0.34, 0.78, 1.0),
	"pepper": (0.95, 0.22, 0.13, 1.0),
	"shell": (0.43, 0.18, 0.24, 1.0),
}


def material(name: str, color: tuple[float, float, float, float], emission: float = 0.0) -> bpy.types.Material:
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.78
	if emission > 0.0:
		bsdf.inputs["Emission Color"].default_value = color
		bsdf.inputs["Emission Strength"].default_value = emission
	return mat


MATS = {key: material("Ember_%s" % key.title(), value,
	0.48 if key == "hot" else 0.28 if key in ("ember", "gold", "ice") else 0.0)
	for key, value in PALETTE.items()}


def root(name: str) -> bpy.types.Object:
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def assign(obj: bpy.types.Object, mat: bpy.types.Material, parent: bpy.types.Object) -> bpy.types.Object:
	obj.data.materials.append(mat)
	obj.parent = parent
	return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.modifier_apply(modifier=modifier.name)
	obj.select_set(False)


def rounded_box(name: str, loc: tuple[float, float, float], size: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object, bevel: float = 0.14) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cube_add(location=loc)
	obj = bpy.context.object
	obj.name = name
	obj.scale = (size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	if bevel > 0.0:
		mod = obj.modifiers.new("storybook_rounding", "BEVEL")
		mod.width = bevel
		mod.segments = 2
		apply_modifier(obj, mod)
	return assign(obj, mat, parent)


def sphere(name: str, loc: tuple[float, float, float], scale: tuple[float, float, float],
		mat: bpy.types.Material, parent: bpy.types.Object, subdivisions: int = 2) -> bpy.types.Object:
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1.0, location=loc)
	obj = bpy.context.object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return assign(obj, mat, parent)


def cylinder(name: str, loc: tuple[float, float, float], radius: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object, vertices: int = 10,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	return assign(obj, mat, parent)


def cone(name: str, loc: tuple[float, float, float], bottom: float, top: float, depth: float,
		mat: bpy.types.Material, parent: bpy.types.Object, vertices: int = 9,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=bottom, radius2=top, depth=depth,
		location=loc, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	return assign(obj, mat, parent)


def torus(name: str, loc: tuple[float, float, float], major: float, minor: float,
		mat: bpy.types.Material, parent: bpy.types.Object,
		rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=16,
		minor_segments=6, location=loc, rotation=rotation)
	obj = bpy.context.object
	obj.name = name
	return assign(obj, mat, parent)


def panel(name: str, outline: list[tuple[float, float]], depth: float, mat: bpy.types.Material,
		parent: bpy.types.Object, loc: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
	# Polygon lies in XZ with thickness along Y.
	verts = [(x, -depth * 0.5, z) for x, z in outline] + [(x, depth * 0.5, z) for x, z in outline]
	n = len(outline)
	faces = [tuple(range(n)), tuple(range(n, n * 2))]
	for i in range(n):
		j = (i + 1) % n
		faces.append((i, j, n + j, n + i))
	mesh = bpy.data.meshes.new(name + "Mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = loc
	return assign(obj, mat, parent)


def descendants(obj: bpy.types.Object) -> list[bpy.types.Object]:
	return [candidate for candidate in bpy.context.scene.objects if candidate == obj or candidate.parent in descendants_shallow(obj)]


def descendants_shallow(obj: bpy.types.Object) -> set[bpy.types.Object]:
	result = {obj}
	pending = [obj]
	while pending:
		parent = pending.pop()
		for child in parent.children:
			if child not in result:
				result.add(child)
				pending.append(child)
	return result


def family(obj: bpy.types.Object) -> list[bpy.types.Object]:
	return list(descendants_shallow(obj))


def add_crenels(parent: bpy.types.Object, radius: float, y: float, count: int = 8) -> None:
	for i in range(count):
		a = math.tau * i / count
		rounded_box("Crenel_%02d" % i, (math.sin(a) * radius, math.cos(a) * radius, y),
			(1.05, 0.92, 1.1), MATS["basalt_light"], parent, 0.18)


def build_planet() -> bpy.types.Object:
	p = root("EmberPlanet")
	segments, rings, radius = 72, 36, 40.0
	verts: list[tuple[float, float, float]] = []
	for j in range(rings + 1):
		lat = -math.pi * 0.5 + math.pi * j / rings
		for i in range(segments):
			lon = math.tau * i / segments
			noise = 0.28 * math.sin(lon * 5.0 + lat * 3.0) + 0.16 * math.sin(lon * 11.0 - lat * 7.0)
			r = radius + noise
			verts.append((r * math.cos(lat) * math.sin(lon), r * math.cos(lat) * math.cos(lon), r * math.sin(lat)))
	faces: list[tuple[int, int, int, int]] = []
	for j in range(rings):
		for i in range(segments):
			n = (i + 1) % segments
			faces.append((j * segments + i, j * segments + n, (j + 1) * segments + n, (j + 1) * segments + i))
	mesh = bpy.data.meshes.new("EmberPlanetMesh")
	mesh.from_pydata(verts, [], faces)
	mesh.materials.append(MATS["basalt"])
	mesh.materials.append(MATS["basalt_mid"])
	mesh.materials.append(MATS["ember"])
	mesh.materials.append(MATS["hot"])
	for poly in mesh.polygons:
		c = poly.center.normalized()
		lon = math.atan2(c.x, c.y)
		lat = math.asin(max(-1.0, min(1.0, c.z)))
		channel = abs(math.sin(lon * 2.5 + math.sin(lat * 4.0) * 1.25))
		# Keep the polar portal/citadel caps quiet. Longitude ribbons collapse
		# into visual pinwheels at a pole and compete with child-readable goals.
		if abs(lat) > 1.37:
			poly.material_index = 1 if (poly.index % 7 == 0) else 0
		elif channel < 0.12:
			poly.material_index = 3
		elif channel < 0.22:
			poly.material_index = 2
		else:
			poly.material_index = 1 if (poly.index % 7 == 0) else 0
	obj = bpy.data.objects.new("Surface", mesh)
	bpy.context.collection.objects.link(obj)
	obj.parent = p
	# Deliberate, shallow polar dais: visual grounding without changing analytic collision.
	for i, rr in enumerate((10.0, 7.5, 5.2)):
		cylinder("CitadelDais_%d" % i, (0, 0, 39.2 + i * 0.28), rr, 0.55,
			MATS["basalt_light"] if i == 1 else MATS["basalt_mid"], p, 16)
	# A quiet landing pad masks the inevitable triangle fan at the opposite
	# pole and gives the rainbow home portal a deliberate, readable plaza.
	cylinder("HomePortalDaisOuter", (0, 0, -40.15), 7.4, 0.82, MATS["basalt_mid"], p, 20)
	cylinder("HomePortalDaisInner", (0, 0, -40.62), 5.7, 0.24, MATS["basalt_light"], p, 20)
	return p


def build_tower(name: str, variant: int) -> bpy.types.Object:
	p = root(name)
	height = (6.2, 7.1, 6.7, 7.8)[variant]
	cylinder("TowerBody", (0, 0, height * 0.5), 1.75 + 0.08 * variant, height,
		MATS["basalt"], p, 10)
	cylinder("UpperBand", (0, 0, height - 0.8), 2.0, 0.55, MATS["basalt_light"], p, 10)
	add_crenels(p, 1.72, height + 0.18, 8)
	for side in (-1, 1):
		panel("WarmWindow", [(-0.34, 0), (0.34, 0), (0.34, 0.85), (0, 1.22), (-0.34, 0.85)],
			0.08, MATS["gold"], p, (side * 1.76, 0, height * 0.56))
		p.children[-1].rotation_euler[2] = math.radians(90)
	for i in range(3):
		a = (i * 2.1 + variant * 0.7)
		cone("BasaltShoulder", (math.sin(a) * 1.7, math.cos(a) * 1.7, 0.7), 1.2, 0.35,
			2.0 + 0.25 * i, MATS["basalt_mid"], p, 7)
	return p


def build_rampart() -> bpy.types.Object:
	p = root("EmberRampart")
	rounded_box("Wall", (0, 0, 2.4), (8.0, 1.7, 4.8), MATS["basalt"], p, 0.28)
	for x in (-3.2, -1.05, 1.05, 3.2):
		rounded_box("Crenel", (x, 0, 5.15), (1.25, 1.9, 1.35), MATS["basalt_light"], p, 0.2)
	for x in (-2.7, 0, 2.7):
		panel("EmberRecess", [(-0.42, 0), (0.42, 0), (0.42, 1.0), (0, 1.5), (-0.42, 1.0)],
			0.08, MATS["ember"], p, (x, -0.9, 1.45))
	return p


def build_flag() -> bpy.types.Object:
	p = root("EmberFlag")
	cylinder("Pole", (0, 0, 2.9), 0.12, 5.8, MATS["gold"], p, 8)
	panel("Banner", [(0, 0), (2.5, -0.18), (2.1, 1.0), (2.65, 2.1), (0, 2.35)],
		0.16, MATS["coral"], p, (0, 0, 3.1))
	panel("FlameMark", [(0, 0), (0.45, 0.35), (0.25, 0.9), (0.75, 1.55), (-0.1, 1.28), (-0.42, 0.62)],
		0.19, MATS["hot"], p, (1.0, -0.01, 3.5))
	return p


def build_gate(name: str = "EmberGreatGate", compact: bool = False) -> bpy.types.Object:
	p = root(name)
	w, h = ((7.2, 7.4) if not compact else (6.2, 6.4))
	for s in (-1, 1):
		rounded_box("GatePillar", (s * w * 0.47, 0, h * 0.44), (1.5, 2.0, h * 0.88), MATS["basalt"], p, 0.28)
		cone("CrownCap", (s * w * 0.47, 0, h + 0.15), 1.25, 0.3, 1.8, MATS["basalt_light"], p, 8)
	rounded_box("Lintel", (0, 0, h * 0.89), (w, 2.1, 1.25), MATS["basalt_mid"], p, 0.34)
	if compact:
		panel("Door", [(-2.2, 0), (2.2, 0), (2.2, 4.0), (0, 6.0), (-2.2, 4.0)],
			0.45, MATS["outline"], p, (0, 0, 0.15))
	for i in range(5):
		x = (i - 2) * 1.18
		panel("LanternSigil_%d" % i, [(-0.28, 0), (0.28, 0), (0.42, 0.48), (0, 1.1), (-0.42, 0.48)],
			0.16, MATS["gold"], p, (x, -1.08, h * (0.64 if compact else 0.81)))
	return p


def build_flame(name: str, layers: int = 3) -> bpy.types.Object:
	p = root(name)
	for i in range(layers):
		scale = 1.0 - i * 0.22
		cone("FlameLayer_%d" % i, (0.12 * i, 0, 0.75 + i * 0.12), 0.72 * scale, 0.02,
			1.8 * scale, (MATS["ember"], MATS["gold"], MATS["hot"])[i], p, 8,
			(0, math.radians(-8 + i * 8), 0))
	return p


def build_gate_veil() -> bpy.types.Object:
	p = root("EmberGateVeil")
	for i in range(5):
		f = build_flame("VeilFlame_%d" % i, 2)
		f.parent = p
		f.location = ((i - 2) * 0.95, 0, 0)
		f.scale = (0.9, 0.65, 2.4 - abs(i - 2) * 0.18)
	return p


def build_lantern(name: str = "EmberLantern") -> bpy.types.Object:
	p = root(name)
	cylinder("Foot", (0, 0, 0.25), 1.15, 0.5, MATS["basalt_light"], p, 10)
	cylinder("Stem", (0, 0, 1.3), 0.5, 1.8, MATS["basalt"], p, 10)
	cylinder("Bowl", (0, 0, 2.25), 1.25, 0.65, MATS["shell"], p, 10)
	for i in range(5):
		a = math.tau * i / 5
		cone("Petal_%d" % i, (math.sin(a) * 0.85, math.cos(a) * 0.85, 2.65), 0.42, 0.08,
			1.15, MATS["gold"], p, 7, (math.sin(a) * 0.24, -math.cos(a) * 0.24, 0))
	glow = build_flame("Glow", 3)
	glow.parent = p
	glow.location = (0, 0, 2.75)
	glow.scale = (0.82, 0.82, 0.82)
	return p


def build_beacon() -> bpy.types.Object:
	p = root("EmberBeacon")
	for i, scale in enumerate((1.0, 0.78, 0.58)):
		d = sphere("BeaconDiamond_%d" % i, (0, 0, i * 2.7), (1.15 * scale, 0.65 * scale, 1.7 * scale),
			MATS["ember"] if i < 2 else MATS["hot"], p, 1)
		d.rotation_euler[1] = math.radians(45)
	return p


def build_geyser() -> bpy.types.Object:
	p = root("EmberGeyser")
	for i in range(10):
		a = math.tau * i / 10
		r = 1.9 + 0.18 * math.sin(i * 2.3)
		cone("BasaltLip_%02d" % i, (math.sin(a) * r, math.cos(a) * r, 0.45), 0.72, 0.36,
			1.1 + 0.25 * (i % 3), MATS["basalt_mid"] if i % 2 else MATS["basalt"], p, 7)
	cylinder("WarmPool", (0, 0, 0.18), 1.5, 0.24, MATS["ember"], p, 12)
	flame = build_flame("FriendlyGeyserFlame", 3)
	flame.parent = p
	flame.location = (0, 0, 0.35)
	flame.scale = (1.3, 1.3, 1.6)
	return p


def build_crag(name: str, variant: int) -> bpy.types.Object:
	p = root(name)
	count = 4 + variant
	for i in range(count):
		a = i * 2.1 + variant * 0.5
		r = 0.45 + 0.34 * (i % 2)
		h = 2.5 + ((i * 7 + variant * 3) % 5) * 0.48
		cone("Crag_%02d" % i, (math.sin(a) * r, math.cos(a) * r, h * 0.5),
			1.0 - i * 0.06, 0.12, h, MATS["basalt_mid"] if i % 3 else MATS["basalt"], p, 7,
			(math.sin(a) * 0.08, -math.cos(a) * 0.08, 0))
	return p


def build_crystal(name: str, variant: int) -> bpy.types.Object:
	p = root(name)
	for i in range(3 + variant):
		a = i * 2.0 + variant
		h = 1.8 + 0.5 * ((i + variant) % 3)
		cone("Crystal_%02d" % i, (math.sin(a) * 0.55, math.cos(a) * 0.55, h * 0.5),
			0.52, 0.0, h, MATS["coral"] if i % 2 else MATS["ember"], p, 6,
			(math.sin(a) * 0.12, -math.cos(a) * 0.12, 0))
	return p


def build_moon() -> bpy.types.Object:
	p = root("EmberAshMoon")
	moon = sphere("AshBody", (0, 0, 0), (4.6, 4.25, 4.9), MATS["ash"], p, 3)
	for i, loc in enumerate(((2.5, -2.8, 1.4), (-1.8, -3.6, -1.3), (0.2, -4.2, 2.7))):
		torus("Crater_%d" % i, loc, 0.72 + i * 0.13, 0.18, MATS["basalt_mid"], p,
			(math.radians(90), 0, 0))
	# Graphic fissure: three warm bars, deliberately sparse at gameplay distance.
	for i in range(3):
		bar = rounded_box("Fissure_%d" % i, (-1.0 + i * 0.75, -4.12, -1.2 + i * 1.0),
			(0.16, 0.12, 2.0), MATS["ember"], p, 0.05)
		bar.rotation_euler[1] = math.radians(-18 + i * 14)
	return p


def build_home_ring() -> bpy.types.Object:
	p = root("EmberHomeRing")
	colors = (MATS["coral"], MATS["gold"], MATS["mint"], MATS["aqua"], MATS["lavender"])
	for i in range(15):
		a = math.tau * i / 15
		segment = rounded_box("RainbowSegment_%02d" % i, (math.sin(a) * 3.0, 0, math.cos(a) * 3.0),
			(1.25, 0.65, 0.72), colors[(i // 3) % len(colors)], p, 0.18)
		segment.rotation_euler[1] = a
	for s in (-1, 1):
		panel("ShellFin", [(0, 0), (1.1, 0.4), (1.5, 1.3), (0.6, 1.0)], 0.28, MATS["cream"], p,
			(s * 3.45, 0, -0.7))
		p.children[-1].scale.x = s
	return p


def build_turtle(name: str, statue: bool = False, boss: bool = False) -> bpy.types.Object:
	p = root(name)
	body_mat = MATS["basalt_light"] if statue else MATS["coral"]
	shell_mat = MATS["basalt"] if statue else MATS["shell"]
	sphere("Body", (0, 0, 1.7), (1.8, 1.35, 1.2), body_mat, p, 2)
	sphere("Shell", (0, 0.45, 2.15), (2.15, 1.15, 1.65), shell_mat, p, 2)
	sphere("Head", (0, -1.65, 2.25), (1.05, 0.9, 0.9), body_mat, p, 2)
	for sx in (-1, 1):
		for sy in (-1, 1):
			cone("Foot", (sx * 1.45, sy * 0.8, 0.65), 0.48, 0.28, 1.3, body_mat, p, 7,
				(0, sx * 0.35, 0))
	if not statue:
		for sx in (-1, 1):
			sphere("Eye", (sx * 0.34, -2.38, 2.5), (0.18, 0.12, 0.23), MATS["cream"], p, 1)
			sphere("Pupil", (sx * 0.34, -2.49, 2.5), (0.08, 0.05, 0.10), MATS["ink"], p, 1)
		# Rounded lantern-frill communicates an Ember monarch without borrowed spikes.
		for i in range(5):
			a = -0.8 + i * 0.4
			cone("LanternFrill", (math.sin(a) * 0.9, 0.15, 3.45), 0.34, 0.06,
				1.15 + (0.3 if i == 2 else 0), MATS["gold"], p, 7,
				(0, math.sin(a) * 0.18, -a * 0.12))
	for ring_i, z in enumerate((1.75, 2.25, 2.72)):
		torus("ShellBand_%d" % ring_i, (0, 0.95, z), 0.92 + ring_i * 0.18, 0.12,
			MATS["ember"] if not statue else MATS["ash"], p, (math.radians(90), 0, 0))
	if boss:
		p.scale = (1.18, 1.18, 1.18)
	return p


def build_arena() -> bpy.types.Object:
	p = root("EmberArena")
	cylinder("Surface", (0, 0, -0.25), 27.0, 0.5, MATS["basalt_mid"], p, 16)
	for i in range(16):
		a = math.tau * i / 16
		wall = rounded_box("Trim", (math.sin(a) * 26.2, math.cos(a) * 26.2, 1.5),
			(10.1, 1.35, 3.0), MATS["basalt"], p, 0.34)
		wall.rotation_euler[2] = -a
		if i % 2 == 0:
			cone("WallLantern", (math.sin(a) * 25.2, math.cos(a) * 25.2, 3.7), 0.62, 0.08,
				1.6, MATS["gold"], p, 7)
	for i in range(8):
		a = math.tau * i / 8
		ray = rounded_box("FloorRay", (0, 7.2, 0.05), (1.15, 12.0, 0.08), MATS["ember"], p, 0.04)
		ray.rotation_euler[2] = a
	return p


def build_imp() -> bpy.types.Object:
	p = root("EmberImp")
	sphere("AshBody", (0, 0, 1.0), (0.88, 0.72, 0.95), MATS["basalt_light"], p, 2)
	for sx in (-1, 1):
		cone("Ear", (sx * 0.75, 0, 1.55), 0.38, 0.0, 0.95, MATS["coral"], p, 6,
			(0, sx * math.radians(64), 0))
		sphere("Eye", (sx * 0.3, -0.67, 1.2), (0.15, 0.08, 0.18), MATS["hot"], p, 1)
		sphere("Foot", (sx * 0.45, -0.05, 0.16), (0.43, 0.64, 0.25), MATS["outline"], p, 1)
	flame = build_flame("Tuft", 2)
	flame.parent = p
	flame.location = (0, 0, 1.72)
	flame.scale = (0.55, 0.55, 0.65)
	return p


def build_basket() -> bpy.types.Object:
	p = root("EmberBasket")
	cone("Basket", (0, 0, 0.85), 1.5, 1.18, 1.7, MATS["gold"], p, 10)
	torus("Rim", (0, 0, 1.72), 1.25, 0.16, MATS["cream"], p)
	for i in range(5):
		a = math.tau * i / 5
		pep = sphere("Pepper", (math.sin(a) * 0.65, math.cos(a) * 0.65, 1.78 + 0.12 * (i % 2)),
			(0.34, 0.34, 0.72), MATS["pepper"], p, 1)
		pep.rotation_euler[1] = math.sin(a) * 0.4
		cone("Stem", (math.sin(a) * 0.65, math.cos(a) * 0.65, 2.2), 0.11, 0.04, 0.35, MATS["mint"], p, 6)
	return p


def build_projectile(name: str, fire: bool) -> bpy.types.Object:
	p = root(name)
	if fire:
		body = sphere("PepperBody", (0, 0, 0), (0.55, 0.55, 0.9), MATS["pepper"], p, 1)
		body.rotation_euler[1] = math.radians(22)
		cone("PepperStem", (0, 0, 0.72), 0.16, 0.05, 0.38, MATS["mint"], p, 6)
	else:
		sphere("Berry", (0, 0, 0), (0.72, 0.72, 0.72), MATS["ice"], p, 2)
		for i in range(6):
			a = math.tau * i / 6
			cone("IceCrown", (math.sin(a) * 0.38, math.cos(a) * 0.38, 0.62), 0.16, 0.0, 0.42, MATS["cream"], p, 5)
	return p


def build_pedestal() -> bpy.types.Object:
	p = root("EmberPedestal")
	cylinder("Foot", (0, 0, 0.3), 1.8, 0.6, MATS["basalt"], p, 10)
	cone("Column", (0, 0, 1.4), 1.2, 0.72, 1.8, MATS["basalt_mid"], p, 10)
	cylinder("Trim", (0, 0, 2.4), 1.55, 0.4, MATS["gold"], p, 10)
	for i in range(5):
		a = math.tau * i / 5
		cone("EmberPetal", (math.sin(a) * 0.92, math.cos(a) * 0.92, 2.72), 0.35, 0.07, 0.7,
			MATS["ember"], p, 6)
	return p


def build_stone() -> bpy.types.Object:
	p = root("EmberSteppingStone")
	sphere("Stone", (0, 0, 0), (2.4, 1.9, 0.58), MATS["basalt_light"], p, 2)
	panel("Footprint", [(-0.4, 0), (0.2, -0.2), (0.55, 0.3), (0.15, 1.1), (-0.5, 0.75)], 0.08,
		MATS["gold"], p, (0, -1.92, 0.2))
	return p


def build_pictograms() -> bpy.types.Object:
	p = root("EmberPictograms")
	def icon(icon_name: str, points: list[tuple[float, float]], mat: bpy.types.Material, x: float) -> None:
		child = root(icon_name)
		child.parent = p
		panel(icon_name + "Shape", points, 0.18, mat, child)
	icons = [
		("Diamond", [(0, 1.1), (0.8, 0), (0, -1.1), (-0.8, 0)], MATS["aqua"]),
		("Orb", [(-0.8, -0.8), (0.8, -0.8), (1.0, 0), (0.8, 0.8), (-0.8, 0.8), (-1.0, 0)], MATS["gold"]),
		("Triangle", [(0, 1.1), (1.0, -0.9), (-1.0, -0.9)], MATS["lavender"]),
		("Ice", [(0, 1.15), (0.26, 0.26), (1.1, 0), (0.26, -0.26), (0, -1.15), (-0.26, -0.26), (-1.1, 0), (-0.26, 0.26)], MATS["ice"]),
		("Flame", [(0, 1.2), (0.7, 0.3), (0.45, -0.9), (0, -1.15), (-0.65, -0.4), (-0.35, 0.2)], MATS["ember"]),
		("Left", [(0, 0), (0.9, 0.9), (0.9, 0.35), (1.6, 0.35), (1.6, -0.35), (0.9, -0.35), (0.9, -0.9)], MATS["aqua"]),
		("Right", [(1.6, 0), (0.7, 0.9), (0.7, 0.35), (0, 0.35), (0, -0.35), (0.7, -0.35), (0.7, -0.9)], MATS["coral"]),
		("Pepper", [(0, 1.1), (0.5, 0.5), (0.72, -0.5), (0, -1.1), (-0.72, -0.5), (-0.5, 0.5)], MATS["pepper"]),
		("Moon", [(0.55, 1), (-0.2, 0.7), (-0.65, 0), (-0.2, -0.7), (0.55, -1), (0.15, -0.45), (0.05, 0.4)], MATS["cream"]),
		("Star", [(0, 1.15), (0.3, 0.35), (1.1, 0.3), (0.45, -0.2), (0.7, -1.0), (0, -0.5), (-0.7, -1.0), (-0.45, -0.2), (-1.1, 0.3), (-0.3, 0.35)], MATS["gold"]),
		("Question", [(-0.55, 0.7), (0, 1.0), (0.6, 0.7), (0.4, 0), (0, -0.2), (0, -0.55), (-0.35, -0.55), (-0.35, 0.05), (0.2, 0.35), (0.05, 0.58), (-0.25, 0.45)], MATS["lavender"]),
	]
	for i, (icon_name, points, mat) in enumerate(icons):
		icon(icon_name, points, mat, (i % 4) * 3.2)
	return p


def build_marker(name: str, kind: str) -> bpy.types.Object:
	p = root(name)
	if kind == "disc":
		cylinder("Plaque", (0, 0, 0), 2.6, 0.36, MATS["outline"], p, 12)
		for i in range(5):
			a = math.tau * i / 5
			sphere("Notch", (math.sin(a) * 2.0, math.cos(a) * 2.0, 0.25), (0.22, 0.22, 0.18), MATS["gold"], p, 1)
	elif kind == "beak":
		cone("DirectionBeak", (0, 0, 0), 0.62, 0.0, 2.4, MATS["gold"], p, 8, (math.radians(90), 0, 0))
	elif kind == "complete":
		for i in range(6):
			a = math.tau * i / 6
			cone("Ray", (math.sin(a) * 0.7, 0, math.cos(a) * 0.7), 0.22, 0.0, 1.0, MATS["hot"], p, 6,
				(0, a, 0))
	else:
		sphere("Pearl", (0, 0, 0), (1.5, 1.5, 1.5), MATS["cream"], p, 3)
		torus("PearlHalo", (0, 0, 0), 1.75, 0.13, MATS["gold"], p, (math.radians(90), 0, 0))
	return p


ASSETS: list[tuple[str, bpy.types.Object, str]] = []


def register(name: str, obj: bpy.types.Object, group: str) -> None:
	ASSETS.append((name, obj, group))


register("ember_planet", build_planet(), "world")
for v in range(4):
	register("ember_tower_%s" % chr(ord("a") + v), build_tower("EmberTower%s" % chr(ord("A") + v), v), "world")
register("ember_rampart", build_rampart(), "world")
register("ember_flag", build_flag(), "world")
register("ember_great_gate", build_gate(), "world")
register("ember_gate_veil", build_gate_veil(), "world")
register("ember_sentry", build_turtle("EmberSentry", statue=True), "world")
register("ember_king", build_turtle("EmberKing", boss=True), "world")
register("ember_lantern", build_lantern(), "props")
register("ember_flame", build_flame("EmberFlame"), "props")
register("ember_beacon", build_beacon(), "props")
register("ember_geyser", build_geyser(), "props")
for v in range(3):
	register("ember_crag_%s" % chr(ord("a") + v), build_crag("EmberCrag%s" % chr(ord("A") + v), v), "props")
	register("ember_crystal_%s" % chr(ord("a") + v), build_crystal("EmberCrystal%s" % chr(ord("A") + v), v), "props")
register("ember_ash_moon", build_moon(), "props")
register("ember_home_ring", build_home_ring(), "props")
register("ember_arena", build_arena(), "dungeon")
register("ember_door", build_gate("EmberDungeonDoor", compact=True), "dungeon")
register("ember_imp", build_imp(), "dungeon")
register("ember_boss", build_turtle("EmberDungeonBoss", boss=True), "dungeon")
register("ember_basket", build_basket(), "dungeon")
register("ember_fire_projectile", build_projectile("EmberFireProjectile", True), "dungeon")
register("ember_ice_projectile", build_projectile("EmberIceProjectile", False), "dungeon")
register("ember_pedestal", build_pedestal(), "dungeon")
register("ember_dungeon_lantern", build_lantern("EmberDungeonLantern"), "dungeon")
register("ember_statue", build_turtle("EmberDungeonStatue", statue=True), "dungeon")
register("ember_stepping_stone", build_stone(), "dungeon")
register("ember_pictograms", build_pictograms(), "dungeon")
register("ember_clue_plaque", build_marker("EmberCluePlaque", "disc"), "dungeon")
register("ember_direction_beak", build_marker("EmberDirectionBeak", "beak"), "dungeon")
register("ember_completion_spark", build_marker("EmberCompletionSpark", "complete"), "dungeon")
register("ember_pearl_target", build_marker("EmberPearlTarget", "pearl"), "dungeon")


def bounds(obj: bpy.types.Object) -> tuple[Vector, Vector]:
	points: list[Vector] = []
	for member in family(obj):
		if member.type == "MESH":
			points.extend(member.matrix_world @ Vector(corner) for corner in member.bound_box)
	minimum = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
	maximum = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
	return minimum, maximum


def metrics(obj: bpy.types.Object) -> tuple[int, int, int, Vector]:
	triangles = materials = islands = 0
	for member in family(obj):
		if member.type != "MESH":
			continue
		mesh = member.data
		mesh.calc_loop_triangles()
		triangles += len(mesh.loop_triangles)
		materials += len(mesh.materials)
		islands += 1
	bmin, bmax = bounds(obj)
	return triangles, materials, islands, bmax - bmin


def export_asset(name: str, obj: bpy.types.Object) -> None:
	bpy.ops.object.select_all(action="DESELECT")
	for member in family(obj):
		member.hide_render = False
		member.hide_viewport = False
		member.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.export_scene.gltf(filepath=str(ASSET_OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT", export_animations=False)


metric_rows = []
for asset_name, asset, group in ASSETS:
	export_asset(asset_name, asset)
	tris, material_slots, mesh_islands, dims = metrics(asset)
	metric_rows.append({"asset": asset_name, "group": group, "triangles": tris,
		"material_slots": material_slots, "mesh_islands": mesh_islands,
		"size_x": round(dims.x, 3), "size_y": round(dims.y, 3), "size_z": round(dims.z, 3)})

with METRICS_OUT.open("w", newline="", encoding="utf-8") as handle:
	writer = csv.DictWriter(handle, fieldnames=list(metric_rows[0].keys()))
	writer.writeheader()
	writer.writerows(metric_rows)

bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
legacy_backup = BLEND_OUT.with_suffix(".blend1")
if legacy_backup.exists():
	legacy_backup.unlink()

# Isolated Eevee QA. Every render uses the same high-key studio and frames the
# measured object, so silhouette and scale problems are comparable.
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.render.resolution_x = 680
scene.render.resolution_y = 560
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
if scene.world is None:
	scene.world = bpy.data.worlds.new("EmberQAWorld")
scene.world.color = (0.055, 0.065, 0.12)

bpy.ops.object.light_add(type="AREA", location=(6, -8, 10))
key = bpy.context.object
key.data.energy = 1100
key.data.shape = "DISK"
key.data.size = 8
bpy.ops.object.light_add(type="AREA", location=(-7, 4, 6))
fill = bpy.context.object
fill.data.energy = 850
fill.data.color = (0.62, 0.72, 1.0)
fill.data.size = 10
bpy.ops.object.camera_add()
camera = bpy.context.object
scene.camera = camera


def frame_object(obj: bpy.types.Object) -> None:
	bmin, bmax = bounds(obj)
	center = (bmin + bmax) * 0.5
	span = max((bmax - bmin).length, 1.0)
	camera.location = center + Vector((span * 0.72, -span * 1.05, span * 0.58))
	direction = center - camera.location
	camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
	camera.data.type = "ORTHO"
	camera.data.ortho_scale = max(bmax.x - bmin.x, bmax.z - bmin.z, bmax.y - bmin.y) * 1.38


for asset_name, asset, _group in ASSETS:
	for _n, other, _g in ASSETS:
		for member in family(other):
			member.hide_render = other != asset
	for member in family(asset):
		member.hide_render = False
	frame_object(asset)
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)


def contact_sheet(group: str) -> None:
	chosen = [(name, obj) for name, obj, item_group in ASSETS if item_group == group]
	originals = []
	cols = 5
	cell = 8.8
	for index, (name, obj) in enumerate(chosen):
		originals.append((obj, obj.location.copy(), obj.scale.copy()))
		bmin, bmax = bounds(obj)
		dims = bmax - bmin
		scale = 5.2 / max(dims.x, dims.y, dims.z, 0.001)
		obj.scale *= scale
		obj.location = ((index % cols - (cols - 1) * 0.5) * cell, 0,
			-(index // cols) * cell)
		bpy.context.view_layer.update()
		for member in family(obj):
			member.hide_render = False
	rows = math.ceil(len(chosen) / cols)
	camera.location = (0, -64, -((rows - 1) * cell) * 0.5 + 1.0)
	camera.rotation_euler = (math.radians(90), 0, 0)
	camera.data.ortho_scale = max(cols * cell, rows * cell) * 1.05
	bpy.context.view_layer.update()
	scene.render.resolution_x = 1280
	scene.render.resolution_y = max(640, int(1280 * rows / cols))
	scene.render.filepath = str(QA_OUT / ("contact_" + group + ".png"))
	bpy.ops.render.render(write_still=True)
	for obj, loc, scale in originals:
		obj.location, obj.scale = loc, scale
		for member in family(obj):
			member.hide_render = True


for group_name in ("world", "props", "dungeon"):
	contact_sheet(group_name)

print("EMBER_KIT_OK", len(ASSETS), "assets", METRICS_OUT)
