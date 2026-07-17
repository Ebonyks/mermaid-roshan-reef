#!/usr/bin/env python3
"""Build seven Mobile-friendly Blender props for the reef's weak districts.

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
	"wreck0": (0.28, 0.31, 0.42, 1), "wreck1": (0.43, 0.42, 0.54, 1),
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


def tapered_tube(name, points, radii, mat, parent):
	"""A soft branch whose thickness changes along its path."""
	curve = bpy.data.curves.new(name + "_curve", "CURVE")
	curve.dimensions, curve.resolution_u = "3D", 3
	curve.bevel_depth, curve.bevel_resolution = 1.0, 2
	spline = curve.splines.new("BEZIER")
	spline.bezier_points.add(len(points) - 1)
	for point, co, radius in zip(spline.bezier_points, points, radii):
		point.co = co
		point.radius = radius
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


def ribbon_3d(name, points, widths, thickness, mat, parent):
	"""A tapered, slightly twisting blade; useful for kelp and current fins."""
	verts = []
	for index, (co, width) in enumerate(zip(points, widths)):
		center = Vector(co)
		if index == 0:
			tangent = Vector(points[1]) - center
		elif index == len(points) - 1:
			tangent = center - Vector(points[index - 1])
		else:
			tangent = Vector(points[index + 1]) - Vector(points[index - 1])
		tangent.normalize()
		side = Vector((tangent.z, 0, -tangent.x))
		if side.length < .01:
			side = Vector((1, 0, 0))
		side.normalize()
		# A tiny depth drift prevents the blade from reading as a cardboard sign.
		depth_shift = Vector((0, math.sin(index * 1.7) * thickness * .35, 0))
		for depth in (-thickness * .5, thickness * .5):
			verts.append(tuple(center - side * width + depth_shift + Vector((0, depth, 0))))
			verts.append(tuple(center + side * width + depth_shift + Vector((0, depth, 0))))
	faces = []
	for index in range(len(points) - 1):
		a = index * 4
		b = a + 4
		faces += [(a, b, b + 1, a + 1), (a + 2, a + 3, b + 3, b + 2),
			(a, a + 2, b + 2, b), (a + 1, b + 1, b + 3, a + 3)]
	faces += [(0, 1, 3, 2), (len(verts) - 4, len(verts) - 2, len(verts) - 1, len(verts) - 3)]
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	finish(obj, mat, parent, True)
	# Two lightweight subdivision passes turn the sparse authored path into a
	# flowing silhouette. These props are instanced only a handful of times.
	subd = obj.modifiers.new("flowing_surface", "SUBSURF")
	subd.subdivision_type = "CATMULL_CLARK"
	subd.levels = subd.render_levels = 2
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=subd.name)
	bev = obj.modifiers.new("soft_blade_edges", "BEVEL")
	bev.width, bev.segments = min(thickness * .45, .12), 2
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=bev.name)
	return obj


def organic_sweep(name, points, radii, mat, parent, seed=0):
	"""An irregular continuous mass swept along a path, with no primitive seams."""
	segments = 9
	verts = []
	for index, (co, radius) in enumerate(zip(points, radii)):
		center = Vector(co)
		if index == 0:
			tangent = Vector(points[1]) - center
		elif index == len(points) - 1:
			tangent = center - Vector(points[index - 1])
		else:
			tangent = Vector(points[index + 1]) - Vector(points[index - 1])
		tangent.normalize()
		depth_axis = Vector((0, 1, 0))
		side_axis = depth_axis.cross(tangent)
		if side_axis.length < .01:
			side_axis = Vector((1, 0, 0))
		side_axis.normalize()
		depth_axis = tangent.cross(side_axis).normalized()
		rx, ry = radius if isinstance(radius, tuple) else (radius, radius * .78)
		for side in range(segments):
			a = math.tau * side / segments + seed * .07
			wobble = 1.0 + math.sin(side * 2.17 + index * 1.31 + seed) * .08
			vertex = center + side_axis * math.cos(a) * rx * wobble
			vertex += depth_axis * math.sin(a) * ry * (2.0 - wobble)
			verts.append(tuple(vertex))
	faces = []
	for ring in range(len(points) - 1):
		for side in range(segments):
			next_side = (side + 1) % segments
			faces.append((ring * segments + side, ring * segments + next_side,
				(ring + 1) * segments + next_side, (ring + 1) * segments + side))
	faces.append(tuple(range(segments - 1, -1, -1)))
	last = (len(points) - 1) * segments
	faces.append(tuple(last + side for side in range(segments)))
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	finish(obj, mat, parent, True)
	# Preserve the authored asymmetry while rounding the sparse path rings into
	# water-worn massing instead of a chain of geometric elbows.
	subd = obj.modifiers.new("water_worn_mass", "SUBSURF")
	subd.subdivision_type = "CATMULL_CLARK"
	subd.levels = subd.render_levels = 1
	bpy.context.view_layer.objects.active = obj
	bpy.ops.object.modifier_apply(modifier=subd.name)
	return obj


def blob(name, loc, scale, mat, parent, seed=0):
	obj = ico(name, loc, scale, mat, parent, 2)
	# Break the perfect primitive without adding texture cost. Distortion is
	# deterministic so regenerated assets remain byte-shape stable in Blender.
	for index, vertex in enumerate(obj.data.vertices):
		co = vertex.co
		wave = math.sin(co.x * 2.7 + seed) * math.cos(co.y * 3.1 - seed * .4)
		wave += math.sin(co.z * 2.3 + index * .17) * .55
		vertex.co *= 1.0 + wave * .045
	obj.data.update()
	return obj


def kelp_leaf(name, loc, length, width, bend, mat, parent, rotation=(0, 0, 0)):
	centers = []
	widths = []
	for i in range(8):
		t = i / 7.0
		centers.append((bend * math.sin(t * math.pi) * (.35 + t), t * length))
		widths.append(width * (math.sin(math.pi * t) ** .65) * (.72 + .28 * t))
	left = [(cx - w, z) for (cx, z), w in zip(centers, widths)]
	right = [(cx + w, z) for (cx, z), w in reversed(list(zip(centers, widths)))]
	leaf = panel(name, left + right, max(.11, width * .16), mat, parent)
	leaf.location = loc
	leaf.rotation_euler = rotation
	return leaf


def ice_shard(name, loc, height, radius, lean, mat, parent, seed=0):
	segments = 7
	rings = 7
	verts = []
	profile = (.72, .96, 1.0, .88, .68, .42, .12)
	for ring in range(rings):
		t = ring / (rings - 1)
		cx = lean[0] * t * t
		cy = lean[1] * t * t
		for side in range(segments):
			a = math.tau * side / segments + seed * .13
			uneven = 1.0 + math.sin(side * 2.1 + ring * .8 + seed) * .08
			r = radius * profile[ring] * uneven
			verts.append((cx + math.cos(a) * r, cy + math.sin(a) * r, t * height))
	faces = []
	for ring in range(rings - 1):
		for side in range(segments):
			next_side = (side + 1) % segments
			a = ring * segments + side
			b = ring * segments + next_side
			c = (ring + 1) * segments + next_side
			d = (ring + 1) * segments + side
			faces.append((a, b, c, d))
	faces.append(tuple(range(segments - 1, -1, -1)))
	faces.append(tuple((rings - 1) * segments + side for side in range(segments)))
	mesh = bpy.data.meshes.new(name + "_mesh")
	mesh.from_pydata(verts, [], faces)
	mesh.update()
	obj = bpy.data.objects.new(name, mesh)
	bpy.context.collection.objects.link(obj)
	obj.location = loc
	finish(obj, mat, parent, True)
	bev = obj.modifiers.new("water_worn_edges", "BEVEL")
	bev.width, bev.segments = min(radius * .2, .16), 3
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
	# Two unrelated old kelp plants overlap into a swim-through. Their tapered
	# trunks and trailing blades keep the silhouette botanical, not architectural.
	tapered_tube("old_kelp_left", [(-3.3, .1, 0), (-3.7, .25, 3.1), (-3.0, 0, 6.2),
		(-1.4, .2, 8.6), (.7, .7, 9.5), (2.2, 1.0, 8.9)],
		[.72, .68, .56, .42, .24, .06], MAT["kelp0"], r)
	tapered_tube("old_kelp_right", [(2.75, -.55, 0), (3.25, -.4, 2.9), (2.85, -.2, 5.6),
		(1.9, .2, 7.4), (.55, .65, 8.45)], [.58, .55, .44, .29, .05], MAT["kelp1"], r)
	tapered_tube("broken_side_stalk", [(-2.7, -.6, .2), (-1.9, -.8, 2.6), (-.2, -.7, 4.3),
		(1.25, -.55, 4.65)], [.34, .29, .17, .035], MAT["kelp1"], r)
	blades = (
		([(-3.45, .15, 1.5), (-4.7, .05, 2.4), (-5.45, .2, 4.0), (-5.0, .6, 5.7)], [.08, .62, .82, .03]),
		([(-3.2, 0, 4.5), (-4.3, -.1, 5.5), (-4.7, -.25, 7.2), (-3.8, -.1, 8.5)], [.06, .72, .9, .03]),
		([(-1.45, .25, 8.5), (-1.8, .6, 10.0), (-.9, .9, 11.1), (.3, 1.1, 10.6)], [.05, .7, .58, .02]),
		([(2.95, -.35, 2.1), (4.1, -.2, 3.1), (4.55, .05, 4.8), (3.9, .25, 6.0)], [.05, .65, .78, .025]),
		([(2.55, -.15, 5.2), (3.4, .15, 6.4), (3.3, .5, 8.0), (2.55, .8, 9.0)], [.04, .64, .7, .02]),
		([(.8, .7, 9.45), (1.4, 1.0, 10.4), (2.55, 1.1, 10.65), (3.25, .8, 9.9)], [.03, .55, .44, .02]),
	)
	for index, (points, widths) in enumerate(blades):
		ribbon_3d("kelp_blade_%d" % index, points, widths, .18, MAT["kelp2"], r)
	for index, (start, end, radius) in enumerate((
		((-3.35, .1, .25), (-5.2, -.4, .08), .24), ((-3.35, .1, .25), (-4.5, .9, .1), .2),
		((-3.2, .05, .25), (-1.7, 1.15, .08), .18), ((2.75, -.5, .2), (4.2, -.9, .08), .18),
		((2.75, -.5, .2), (1.35, -1.3, .08), .15))):
		tapered_tube("root_finger_%d" % index, [start, ((start[0] + end[0]) * .5,
			(start[1] + end[1]) * .5, .18), end], [radius, radius * .55, .02], MAT["navy"], r)
	blob("left_holdfast", (-3.35, .1, .28), (1.15, .85, .48), MAT["navy"], r, 2)
	blob("right_holdfast", (2.75, -.5, .25), (.9, .72, .42), MAT["kelp0"], r, 7)
	return r


def wreck_shoulders():
	r = root("wreck_ravine_shoulders")
	# A low cluster of overlapping water-worn boulders with unequal crests. It
	# provides destination-scale structure without becoming another arch/icon.
	blob("ridge_foot", (0, 0, .45), (4.8, 1.55, .72), MAT["wreck0"], r, 23)
	mounds = (
		((-3.35, .05, 1.05), (1.55, 1.18, 1.35), MAT["wreck1"], 27),
		((-1.55, -.1, 1.55), (2.05, 1.35, 2.05), MAT["wreck0"], 31),
		((.75, .15, 1.7), (1.75, 1.42, 2.35), MAT["wreck1"], 36),
		((2.75, -.05, 1.05), (1.65, 1.2, 1.45), MAT["wreck0"], 41),
	)
	for index, (loc, scale, mat, seed) in enumerate(mounds):
		blob("ridge_mound_%d" % index, loc, scale, mat, r, seed)
	for index, (x, y, z, sx, sz) in enumerate(((-4.05, -.35, .55, .72, .48),
		(-.2, -.65, .65, .9, .55), (3.85, -.25, .58, .68, .46))):
		blob("ridge_lobe_%d" % index, (x, y, z), (sx, sx * .72, sz), MAT["wreck1"], r, index + 47)
	return r


def kelp_lanterns():
	r = root("kelp_lantern_cluster")
	# Lantern pods hang beneath branching kelp arms; none sit on top like flowers.
	stems = (
		([(-2.0, .1, .15), (-2.5, .2, 2.7), (-1.8, .15, 5.2), (-.2, .1, 6.3)], [.34, .3, .2, .04]),
		([(.3, -.45, .1), (.9, -.55, 2.5), (.5, -.4, 4.8), (1.8, -.2, 5.65)], [.38, .32, .19, .04]),
		([(1.75, .55, .1), (2.25, .65, 2.2), (1.55, .7, 3.9), (.7, .65, 4.35)], [.28, .23, .14, .035]),
	)
	for index, (points, radii) in enumerate(stems):
		tapered_tube("lantern_kelp_%d" % index, points, radii, MAT["kelp0" if index < 2 else "kelp1"], r)
	for index, (anchor, size) in enumerate((((-.25, .1, 6.25), .82), ((1.8, -.2, 5.6), .65),
		((.7, .65, 4.3), .52), ((-1.75, .15, 5.15), .46))):
		tapered_tube("pod_cord_%d" % index, [anchor, (anchor[0] + .08, anchor[1], anchor[2] - .55)],
			[.08, .045], MAT["kelp2"], r)
		center = (anchor[0] + .08, anchor[1], anchor[2] - .95)
		organic_sweep("bell_pod_%d" % index,
			[(center[0], center[1], center[2] + .42), center, (center[0], center[1], center[2] - .34)],
			[(size * .28, size * .22), (size, size * .72), (size * .68, size * .55)], MAT["lamp"], r, index + 3)
		for fringe in range(3):
			offset = (fringe - 1) * size * .42
			tapered_tube("pod_fringe_%d_%d" % (index, fringe),
				[(center[0] + offset, center[1], center[2] - .3),
				(center[0] + offset * 1.15, center[1] + .06, center[2] - .75)],
				[.055, .015], MAT["kelp2"], r)
	for index, (points, widths) in enumerate((
		([(-2.15, .1, 1.1), (-3.25, .1, 2.1), (-3.5, .25, 3.5), (-3.0, .4, 4.3)], [.04, .58, .72, .02]),
		([(1.85, .55, .8), (3.0, .5, 1.8), (3.25, .35, 3.1), (2.8, .15, 4.0)], [.04, .55, .68, .02]))):
		ribbon_3d("lantern_leaf_%d" % index, points, widths, .16, MAT["kelp2"], r)
	blob("lantern_holdfast", (0, 0, .25), (2.5, 1.25, .46), MAT["kelp1"], r, 11)
	return r


def moon_arch():
	r = root("moon_shell_arch")
	# One continuous eroded shell-rock mass makes the opening. Broken shelves
	# and lopsided lobes replace the previous repeated concentric hoops.
	organic_sweep("weathered_shell_mass", [(-3.15, .1, .25), (-3.55, .2, 2.3), (-2.8, .05, 4.55),
		(-1.25, -.15, 6.15), (.7, -.25, 6.5), (2.15, -.05, 5.2), (2.7, .15, 3.0),
		(2.65, .25, .3)], [(1.3, .95), (1.35, 1.0), (1.05, .82), (.82, .7),
		(.68, .62), (.82, .72), (1.08, .86), (1.2, .9)], MAT["moon"], r, 5)
	organic_sweep("broken_shell_spur", [(-3.25, .25, 1.1), (-4.45, .45, 2.0), (-4.9, .5, 3.4)],
		[(.72, .6), (.52, .43), (.12, .1)], MAT["shell"], r, 9)
	for index, (points, widths) in enumerate((
		([(-3.25, -.65, 2.0), (-2.35, -.8, 3.1), (-1.15, -.82, 3.55)], [.12, .6, .04]),
		([(1.9, -.65, 4.55), (2.8, -.7, 4.25), (3.55, -.6, 3.3)], [.1, .5, .03]),
		([(-.9, -.75, 6.05), (-.2, -.85, 6.85), (.65, -.8, 6.45)], [.08, .42, .03]))):
		ribbon_3d("shell_shelf_%d" % index, points, widths, .32, MAT["shell2"], r)
	for index, (x, y, z, sx, sz) in enumerate(((-3.45, .1, .55, 1.25, .75), (2.7, .15, .5, 1.15, .7),
		(-3.15, -.05, 3.5, .55, .8), (2.25, -.1, 4.4, .45, .65))):
		blob("shell_lobe_%d" % index, (x, y, z), (sx, sx * .72, sz), MAT["shell2"], r, index + 14)
	return r


def moon_totem():
	r = root("moon_pearl_totem")
	# A single open clam nest: broad rounded shells cradle the pearls without
	# any vertical stack, spikes, or repeated freestanding panels.
	blob("lower_shell_bowl", (0, 0, .35), (2.7, 1.65, .62), MAT["moon"], r, 5)
	back = blob("back_shell", (0, .75, 1.75), (2.45, .42, 1.95), MAT["shell"], r, 8)
	back.rotation_euler.x = math.radians(-10)
	for index, x in enumerate((-1.45, -.75, 0, .8, 1.5)):
		tapered_tube("shell_growth_ridge_%d" % index,
			[(x * .35, .3, .55), (x * .72, .32, 1.45), (x, .34, 2.85)],
			[.14, .11, .02], MAT["shell2"], r)
	blob("left_lip", (-1.75, -.25, .7), (.85, .62, .42), MAT["shell2"], r, 17)
	blob("right_lip", (1.55, -.2, .62), (1.0, .68, .4), MAT["shell2"], r, 21)
	blob("hero_pearl", (-.25, -.3, 1.25), (1.02, .98, 1.02), MAT["pearl"], r, 1)
	blob("small_pearl", (1.05, -.15, .82), (.4, .38, .41), MAT["pearl"], r, 9)
	return r


def ice_crystals():
	r = root("ice_crystal_cluster")
	# Rounded brinicle hummocks and undercut shelves replace gemstone spikes.
	blob("sea_glass_shelf", (0, 0, .32), (3.25, 1.9, .6), MAT["ice0"], r, 4)
	organic_sweep("tall_brine_column", [(-.55, .1, .35), (-.85, .12, 1.7), (-.45, .05, 3.2),
		(-.75, 0, 4.65), (-.25, -.05, 5.75)], [(1.35, 1.0), (1.48, 1.05),
		(1.12, .9), (1.25, .92), (.62, .5)], MAT["ice1"], r, 3)
	blob("tall_round_cap", (-.25, -.05, 5.72), (.7, .56, .62), MAT["ice2"], r, 7)
	organic_sweep("left_brine_column", [(-2.15, .2, .35), (-2.35, .25, 1.4), (-2.0, .2, 2.65),
		(-2.2, .15, 3.65)], [(1.05, .8), (1.18, .86), (.9, .7), (.45, .38)], MAT["ice0"], r, 10)
	blob("left_round_cap", (-2.2, .15, 3.62), (.52, .43, .45), MAT["ice2"], r, 12)
	organic_sweep("right_brine_column", [(1.65, -.2, .3), (1.95, -.18, 1.3), (1.65, -.1, 2.35),
		(2.0, 0, 3.0)], [(1.0, .76), (1.12, .82), (.8, .64), (.4, .34)], MAT["ice1"], r, 16)
	blob("right_round_cap", (2.0, 0, 2.98), (.48, .4, .42), MAT["ice2"], r, 18)
	ribbon_3d("undercut_ice_shelf", [(-2.55, -.65, 1.45), (-1.15, -.8, 1.8),
		(.55, -.82, 1.65), (2.2, -.65, 1.15)], [.08, .62, .55, .03], .34, MAT["ice2"], r)
	return r


def ice_fan():
	r = root("ice_current_fan")
	blob("current_shelf", (0, 0, .3), (3.0, 1.5, .5), MAT["ice0"], r, 6)
	# Three broad, incomplete sheets sweep in one direction like a frozen
	# current. Their unequal crests avoid both hoops and a radial fan symbol.
	sheets = (
		([(-2.65, .15, .4), (-2.65, .1, 2.0), (-1.75, .05, 3.8), (-.2, 0, 4.9),
			(1.55, -.05, 5.0), (2.75, -.1, 4.25)], [.08, .7, .9, .72, .45, .02], .42, MAT["ice1"]),
		([(-1.75, -.75, .35), (-1.25, -.75, 1.65), (-.1, -.72, 2.8), (1.35, -.68, 3.15),
			(2.45, -.62, 2.65)], [.06, .58, .72, .46, .02], .32, MAT["ice2"]),
		([(-.65, .8, .3), (-.2, .82, 1.25), (.75, .8, 2.0), (1.9, .72, 2.15),
			(2.65, .62, 1.7)], [.05, .42, .54, .32, .02], .26, MAT["ice1"]),
	)
	for index, (points, widths, thickness, mat) in enumerate(sheets):
		ribbon_3d("frozen_current_sheet_%d" % index, points, widths, thickness, mat, r)
	for index, (x, y, z, sx, sz) in enumerate(((-2.55, .1, .85, .55, .72), (-.15, 0, 4.7, .5, .4),
		(1.5, -.05, 4.85, .38, .32), (2.35, -.62, 2.55, .3, .28))):
		blob("current_foam_%d" % index, (x, y, z), (sx, sx * .7, sz), MAT["ice2"], r, index + 30)
	return r


BUILDERS = {
	"wreck_ravine_shoulders": wreck_shoulders,
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
