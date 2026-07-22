#!/usr/bin/env python3
"""Render fixed 0/45/135-degree toon QA views for one GLB."""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


glb = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
out_dir = Path(sys.argv[sys.argv.index("--") + 2]).resolve()
stem = sys.argv[sys.argv.index("--") + 3]
out_dir.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
minimum = Vector((1e9, 1e9, 1e9))
maximum = Vector((-1e9, -1e9, -1e9))
for obj in meshes:
	for corner in obj.bound_box:
		point = obj.matrix_world @ Vector(corner)
		for axis in range(3):
			minimum[axis] = min(minimum[axis], point[axis])
			maximum[axis] = max(maximum[axis], point[axis])
center = (minimum + maximum) * 0.5
size = maximum - minimum
max_dimension = max(size)
radius = max(size.x, size.z)
height = size.y

ink = bpy.data.materials.new("turntable_ink")
ink.use_nodes = True
nodes = ink.node_tree.nodes
for node in list(nodes):
	nodes.remove(node)
emission = nodes.new("ShaderNodeEmission")
emission.inputs[0].default_value = (0.02, 0.01, 0.06, 1.0)
transparent = nodes.new("ShaderNodeBsdfTransparent")
geometry = nodes.new("ShaderNodeNewGeometry")
mix = nodes.new("ShaderNodeMixShader")
ink.node_tree.links.new(geometry.outputs["Backfacing"], mix.inputs[0])
ink.node_tree.links.new(transparent.outputs[0], mix.inputs[1])
ink.node_tree.links.new(emission.outputs[0], mix.inputs[2])
output = nodes.new("ShaderNodeOutputMaterial")
ink.node_tree.links.new(mix.outputs[0], output.inputs[0])

for obj in meshes:
	for material in [item for item in obj.data.materials if item and item.use_nodes]:
		material_nodes = material.node_tree.nodes
		bsdf = material_nodes.get("Principled BSDF")
		material_output = next((node for node in material_nodes if node.type == "OUTPUT_MATERIAL"), None)
		if material_output is None:
			continue
		toon = material_nodes.new("ShaderNodeBsdfToon")
		toon.component = "DIFFUSE"
		toon.inputs["Size"].default_value = 0.8
		toon.inputs["Smooth"].default_value = 0.02
		if bsdf:
			base_color = bsdf.inputs["Base Color"]
			toon.inputs["Color"].default_value = base_color.default_value
			if base_color.is_linked:
				material.node_tree.links.new(base_color.links[0].from_socket,
					toon.inputs["Color"])
		material.node_tree.links.new(toon.outputs[0], material_output.inputs["Surface"])
	obj.data.materials.append(ink)
	outline = obj.modifiers.new("turntable_outline", "SOLIDIFY")
	outline.thickness = 0.012 * max_dimension
	outline.offset = 1.0
	outline.material_offset = len(obj.data.materials) - 1
	outline.use_rim = False

camera_data = bpy.data.cameras.new("turntable_camera")
camera = bpy.data.objects.new("turntable_camera", camera_data)
bpy.context.scene.collection.objects.link(camera)
bpy.context.scene.camera = camera
for energy, rotation_z in ((4.5, 30), (2.2, 210)):
	light_data = bpy.data.lights.new("turntable_sun", "SUN")
	light_data.energy = energy
	light = bpy.data.objects.new("turntable_sun", light_data)
	bpy.context.scene.collection.objects.link(light)
	light.rotation_euler = (math.radians(55), 0.0, math.radians(rotation_z))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 560
scene.render.resolution_y = 820
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.world = bpy.data.worlds.new("turntable_world")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.10, 0.32, 0.45, 1.0)

for angle in (0, 45, 135):
	radians = math.radians(angle)
	distance = max(height, radius) * 2.2
	camera.location = center + Vector((math.sin(radians) * distance,
		-math.cos(radians) * distance, height * 0.12))
	camera.rotation_euler = (center - camera.location).normalized().to_track_quat("-Z", "Y").to_euler()
	scene.render.filepath = str(out_dir / (stem + "_%03d.png" % angle))
	bpy.ops.render.render(write_still=True)
	print("TURNTABLE|%s|%03d" % (stem, angle))
