#!/usr/bin/env python3
"""Build six Mobile-friendly Blender props for the reef's weak districts.

Usage: blender --background --python tools/build_reef_region_kit.py
"""

from pathlib import Path
import math

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
ASSET_OUT = ROOT / "assets" / "reef_regions"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_reef_region_kit"
for folder in (ASSET_OUT, SOURCE_OUT, QA_OUT):
	folder.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0

COLORS = {
	"navy": (0.09, 0.10, 0.23, 1), "kelp0": (0.16, 0.34, 0.31, 1),
	"kelp1": (0.28, 0.58, 0.43, 1), "kelp2": (0.52, 0.78, 0.57, 1),
	"lamp": (0.78, 0.82, 0.49, 1), "moon": (0.45, 0.40, 0.58, 1),
	"shell": (0.79, 0.67, 0.82, 1), "shell2": (0.92, 0.83, 0.88, 1),
	"pearl": (0.88, 0.93, 0.94, 1), "ice0": (0.35, 0.52, 0.65, 1),
	"ice1": (0.56, 0.76, 0.84, 1), "ice2": (0.78, 0.91, 0.94, 1),
}


def make_mat(name, color):
	mat = bpy.data.materials.new("MR_region_" + name)
	mat.diffuse_color = color
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	bsdf.inputs["Base Color"].default_value = color
	bsdf.inputs["Roughness"].default_value = 0.88
	return mat


MAT = {name: make_mat(name, color) for name, color in COLORS.items()}


def root(name):
	obj = bpy.data.objects.new(name, None)
	bpy.context.collection.objects.link(obj)
	return obj


def finish(obj, mat, parent, smooth=True):
	obj.data.materials.append(mat)
	obj.parent = parent
	if smooth:
		for poly in obj.data.polygons:
			poly.use_smooth = True
	return obj


def ico(name, loc, scale, mat, parent, subdivisions=2):
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=loc)
	obj = bpy.context.active_object
	obj.name = name
	obj.scale = scale
	bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
	return finish(obj, mat, parent)


def cylinder(name, loc, radius, depth, mat, parent, vertices=10):
	bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
	obj = finish(bpy.context.active_object, mat, parent)
	obj.name = name
	bev = obj.modifiers.new("soft_edges", "BEVEL")
	bev.width, bev.segments = min(radius * 0.18, 0.12), 2
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=bev.name)
	return obj


def tube(name, points, radius, mat, parent):
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions, curve.resolution_u = "3D", 2
	curve.bevel_depth, curve.bevel_resolution = radius, 2
	spline = curve.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, co in zip(spline.bezier_points, points):
		point.co = co
		point.handle_left_type = point.handle_right_type = "AUTO"
	obj = bpy.data.objects.new(name, curve)
	bpy.context.collection.objects.link(obj)
	obj.parent = parent
	curve.materials.append(mat)
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.object.convert(target="MESH")
	obj.select_set(False)
	return obj


def panel(name, outline, depth, mat, parent):
	verts = [(x, -depth / 2, z) for x, z in outline] + [(x, depth / 2, z) for x, z in outline]
	n = len(outline)
	faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, n * 2))]
	faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	finish(obj, mat, parent, False)
	bev = obj.modifiers.new("rounded_panel", "BEVEL")
	bev.width, bev.segments = min(depth * 0.32, 0.12), 2
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=bev.name)
	return obj


def crystal(name, loc, radius, height, mat, parent, tilt=(0, 0, 0)):
	bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=radius, radius2=radius * .72,
		depth=height * .72, location=(loc[0], loc[1], loc[2] + height * .36), rotation=tilt)
	body = finish(bpy.context.active_object, mat, parent, False)
	body.name = name + "_shaft"
	bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=radius * .72, radius2=0,
		depth=height * .28, location=(loc[0], loc[1], loc[2] + height * .86), rotation=tilt)
	tip = finish(bpy.context.active_object, MAT["ice2"], parent, False)
	tip.name = name + "_tip"


def fan_shell(name, loc, scale, parent, mirror=1):
	angles = [math.radians(v) for v in (-72, -48, -24, 0, 24, 48, 72)]
	outline = [(0, 0)] + [(math.sin(a) * scale, math.cos(a) * scale) for a in angles]
	body = panel(name + "_body", outline, scale * .16, MAT["shell"], parent)
	body.location, body.scale.x = loc, mirror
	for i, angle in enumerate(angles):
		end = (loc[0] + math.sin(angle) * scale * mirror, loc[1] - scale * .1,
			loc[2] + math.cos(angle) * scale)
		tube(name + "_rib_%d" % i, [loc, end], scale * .035, MAT["shell2"], parent)


def kelp_arch():
	r = root("kelp_cathedral_arch")
	for side in (-1, 1):
		tube("kelp_pillar", [(side * 3, 0, .2), (side * 3.5, .25, 3.8),
			(side * 2.8, -.15, 7.3), (side * .3, 0, 9.8)], .48, MAT["kelp0"], r)
		ico("root_stone", (side * 3, 0, .45), (1.2, .9, .55), MAT["navy"], r)
		for z, offset in ((2.1, 1), (4.5, -1), (6.8, .8)):
			leaf = ico("kelp_paddle", (side * (3.2 + offset * .45), 0, z),
				(.85, .18, 1.35), MAT["kelp2"], r, 1)
			leaf.rotation_euler.y = side * .35
	tube("crown_braid", [(-.4, 0, 9.7), (0, .45, 10.35), (.4, 0, 9.7)], .34, MAT["kelp1"], r)
	return r


def kelp_lanterns():
	r = root("kelp_lantern_cluster")
	for i, (x, y, h, lean) in enumerate(((-1.5, .2, 4.3, -.5), (0, -.2, 6.1, .25), (1.55, .15, 4.9, .55))):
		tube("stem_%d" % i, [(x * .55, y, 0), (x, y, h * .55), (x + lean, y, h)], .2, MAT["kelp0"], r)
		ico("pod_%d" % i, (x + lean, y, h + .3), (.72, .55, .95), MAT["lamp"], r)
		cylinder("cap_%d" % i, (x + lean, y, h + 1.1), .34, .24, MAT["kelp2"], r, 8)
	ico("lantern_base", (0, 0, .35), (2.4, 1.15, .55), MAT["kelp1"], r)
	return r


def moon_arch():
	r = root("moon_shell_arch")
	fan_shell("left_shell", (-2.15, 0, .2), 3.35, r, -1)
	fan_shell("right_shell", (2.15, 0, .2), 3.35, r, 1)
	tube("moon_crescent", [(-2, 0, 3), (-1.5, 0, 5.6), (0, 0, 6.8),
		(1.5, 0, 5.6), (2, 0, 3)], .35, MAT["moon"], r)
	for x in (-2.25, 2.25):
		ico("arch_foot", (x, 0, .25), (.85, .75, .42), MAT["moon"], r, 1)
	return r


def moon_totem():
	r = root("moon_pearl_totem")
	ico("totem_base", (0, 0, .35), (2.2, 1.35, .58), MAT["moon"], r)
	for side in (-1, 1):
		petal = panel("shell_petal", [(0, 0), (side * .4, .7), (side * 1.9, 2.7),
			(side * 1.6, 3.8), (side * .55, 2.8)], .42, MAT["shell"], r)
		petal.location.z = .25
	for i, (x, y, z, s) in enumerate(((0, 0, 1.45, .9), (-.65, .05, 2.75, .66), (.58, -.02, 3.75, .52))):
		ico("pearl_%d" % i, (x, y, z), (s, s, s), MAT["pearl"], r)
	return r


def ice_crystals():
	r = root("ice_crystal_cluster")
	ico("crystal_shelf", (0, 0, .3), (2.8, 1.8, .55), MAT["ice0"], r)
	crystal("hero", (0, 0, .5), 1.15, 7.6, MAT["ice1"], r)
	crystal("left", (-1.8, .2, .45), .85, 5.2, MAT["ice0"], r, (0, -.24, -.15))
	crystal("right", (1.7, -.1, .45), .78, 4.4, MAT["ice1"], r, (0, .28, .18))
	crystal("front", (.8, -1, .4), .54, 3.1, MAT["ice2"], r, (.1, .15, .08))
	return r


def ice_fan():
	r = root("ice_current_fan")
	ico("current_base", (0, 0, .32), (2.8, 1.35, .55), MAT["ice0"], r)
	shapes = (
		([(-.45, 0), (-1, 1.2), (-1.45, 3.6), (-.4, 5.7), (.25, 3.4), (.35, 1)], -1.35, MAT["ice1"]),
		([(-.4, 0), (-.9, 1.4), (-.7, 4.4), (.45, 7), (.65, 4), (.35, 1)], 0, MAT["ice2"]),
		([(-.35, 0), (-.55, 1.3), (-.15, 3.6), (1.35, 5.4), (1, 2.9), (.35, .9)], 1.25, MAT["ice1"]),
	)
	for i, (shape, x, mat) in enumerate(shapes):
		fin = panel("frozen_current_%d" % i, shape, .5, mat, r)
		fin.location.x, fin.rotation_euler.z = x, (i - 1) * .12
	return r


BUILDERS = {
	"kelp_cathedral_arch": kelp_arch, "kelp_lantern_cluster": kelp_lanterns,
	"moon_shell_arch": moon_arch, "moon_pearl_totem": moon_totem,
	"ice_crystal_cluster": ice_crystals, "ice_current_fan": ice_fan,
}


def family(obj):
	result = [obj]
	for child in obj.children:
		result += family(child)
	return result


def export(name, obj):
	bpy.ops.object.select_all(action="DESELECT")
	for member in family(obj):
		member.select_set(True)
	bpy.context.view_layer.objects.active = obj
	bpy.ops.export_scene.gltf(filepath=str(ASSET_OUT / (name + ".glb")), export_format="GLB",
		export_yup=True, use_selection=True, export_apply=True, export_materials="EXPORT")
	bpy.ops.object.select_all(action="DESELECT")


def bounds(obj):
	points = []
	for member in family(obj):
		if member.type == "MESH":
			points += [member.matrix_world @ Vector(corner) for corner in member.bound_box]
	return (Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points))),
		Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points))))


roots = {}
for asset_name, builder in BUILDERS.items():
	asset = builder()
	roots[asset_name] = asset
	export(asset_name, asset)
	for member in family(asset):
		member.hide_render = True

bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_OUT / "reef_region_kit.blend"))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 760, 620, 100
scene.render.image_settings.file_format, scene.render.film_transparent = "PNG", True
scene.view_settings.look = "AgX - Medium High Contrast"
bpy.ops.object.camera_add(location=(12, -18, 10))
camera = bpy.context.active_object
camera.data.lens, scene.camera = 58, camera
for loc, energy, size, color in (((7, -9, 14), 1100, 7, (.85, .95, 1)),
	((-9, -4, 8), 850, 6, (.75, .82, 1)), ((3, 8, 10), 950, 5, (1, .72, .64))):
	bpy.ops.object.light_add(type="AREA", location=loc)
	light = bpy.context.active_object
	light.data.energy, light.data.shape, light.data.size, light.data.color = energy, "DISK", size, color

for asset_name, asset in roots.items():
	for member in family(asset):
		member.hide_render = False
	lo, hi = bounds(asset)
	center, size = (lo + hi) * .5, hi - lo
	distance = max(size.x, size.y, size.z) * 2.15
	camera.location = center + Vector((distance * .82, -distance * 1.35, distance * .62))
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(QA_OUT / (asset_name + ".png"))
	bpy.ops.render.render(write_still=True)
	for member in family(asset):
		member.hide_render = True

print("REEF_REGION_KIT|assets|%d" % len(roots))
print("REEF_REGION_KIT|blend|%s" % (SOURCE_OUT / "reef_region_kit.blend"))
