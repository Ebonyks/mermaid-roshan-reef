#!/usr/bin/env python3
"""Render exact transparent references for Dirty Castle skin generation.

Run with Blender 4.4+:

    blender --background --python tools/render_dirty_castle_references.py

The output is deliberately derived from the shipped GLBs, not concept art.
Every dirty full-object skin is composited over one of these renders so its
geometry, proportions, material blocks, shell motifs, and view remain fixed.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
	ROOT
	/ "assets_src"
	/ "concepts"
	/ "dirty_castle_cleanup_2026-07-22"
	/ "scene_references"
	/ "objects"
)

JOBS: tuple[tuple[str, str], ...] = (
	("assets/castle/pearl_kit/pearl_shell_chandelier.glb", "pearl_shell_chandelier"),
	("assets/castle/pearl_kit/pearl_shell_banner_a.glb", "pearl_shell_banner_a"),
	("assets/castle/pearl_kit/pearl_shell_throne.glb", "pearl_shell_throne"),
	("assets/castle/pearl_kit/pearl_pantry_shelf.glb", "pearl_pantry_shelf"),
	("assets/castle/pearl_kit/pearl_craft_table.glb", "pearl_craft_table"),
	("assets/castle/pearl_kit/pearl_toy_chest.glb", "pearl_toy_chest"),
	("assets/castle/pearl_kit/pearl_rainbow_stacker.glb", "pearl_rainbow_stacker"),
	("assets/castle/pearl_kit/pearl_shell_drum.glb", "pearl_shell_drum"),
	("assets/castle/pearl_kit/pearl_toy_block_stack.glb", "pearl_toy_block_stack"),
	("assets/castle/pearl_kit/pearl_toy_sailboat.glb", "pearl_toy_sailboat"),
	("assets/castle/pearl_kit/pearl_shell_hopscotch.glb", "pearl_shell_hopscotch"),
	("assets/art35/castle/royal_bookcase.glb", "royal_bookcase"),
	("assets/castle/pearl_kit/pearl_library_table.glb", "pearl_library_table"),
	("assets/castle/pearl_kit/pearl_story_cushion.glb", "pearl_story_cushion"),
	("assets/castle/kitchen_counter.glb", "kitchen_counter"),
	("assets/castle/kitchen_sink.glb", "kitchen_sink"),
	("assets/castle/kitchen_stove.glb", "kitchen_stove"),
	("assets/art35/castle/kitchen_kettle.glb", "kitchen_kettle"),
	("assets/art35/castle/kitchen_pan_set.glb", "kitchen_pan_set"),
	("assets/art35/castle/kitchen_teapot.glb", "kitchen_teapot"),
	("assets/castle/bathroom_bathtub.glb", "bathroom_bathtub"),
	("assets/castle/bathroom_sink.glb", "bathroom_sink"),
	("assets/castle/bathroom_toilet.glb", "bathroom_toilet"),
	("assets/castle/pearl_kit/pearl_towel_stack.glb", "pearl_towel_stack"),
	("assets/castle/pearl_kit/pearl_bath_duck.glb", "pearl_bath_duck"),
	("assets/castle/pearl_kit/pearl_storage_barrel.glb", "pearl_storage_barrel"),
	("assets/castle/pearl_kit/pearl_storage_crate.glb", "pearl_storage_crate"),
	("assets/castle/pearl_kit/pearl_storage_cart.glb", "pearl_storage_cart"),
	("assets/castle/pearl_kit/pearl_cloud_pouf.glb", "pearl_cloud_pouf"),
	("assets/castle/pearl_kit/pearl_cloud_settee.glb", "pearl_cloud_settee"),
)


def _bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
	minimum = Vector((1.0e9, 1.0e9, 1.0e9))
	maximum = Vector((-1.0e9, -1.0e9, -1.0e9))
	for obj in objects:
		if obj.type != "MESH":
			continue
		for corner in obj.bound_box:
			point = obj.matrix_world @ Vector(corner)
			for axis in range(3):
				minimum[axis] = min(minimum[axis], point[axis])
				maximum[axis] = max(maximum[axis], point[axis])
	return minimum, maximum


def _configure_scene() -> bpy.types.Object:
	bpy.ops.wm.read_factory_settings(use_empty=True)
	scene = bpy.context.scene
	scene.render.engine = "BLENDER_WORKBENCH"
	scene.render.resolution_x = 1024
	scene.render.resolution_y = 1024
	scene.render.resolution_percentage = 100
	scene.render.image_settings.file_format = "PNG"
	scene.render.image_settings.color_mode = "RGBA"
	scene.render.film_transparent = True
	scene.display.shading.light = "STUDIO"
	scene.display.shading.studio_light = "paint.sl"
	scene.display.shading.color_type = "MATERIAL"
	scene.display.shading.show_shadows = True
	scene.display.shading.show_cavity = True
	scene.display.shading.cavity_type = "WORLD"
	scene.display.shading.show_object_outline = True
	scene.display.shading.object_outline_color = (0.10, 0.06, 0.22)
	scene.view_settings.view_transform = "Standard"
	scene.view_settings.look = "Medium High Contrast"

	camera_data = bpy.data.cameras.new("dirty_castle_reference_camera")
	camera_data.type = "ORTHO"
	camera = bpy.data.objects.new("dirty_castle_reference_camera", camera_data)
	scene.collection.objects.link(camera)
	scene.camera = camera
	return camera


def _render_reference(
	camera: bpy.types.Object,
	resource_path: str,
	stem: str,
) -> None:
	glb = ROOT / resource_path
	if not glb.is_file():
		raise FileNotFoundError(glb)
	before = set(bpy.data.objects)
	bpy.ops.import_scene.gltf(filepath=str(glb))
	imported = [obj for obj in bpy.data.objects if obj not in before]
	meshes = [obj for obj in imported if obj.type == "MESH"]
	if not meshes:
		raise RuntimeError(f"No meshes imported from {glb}")

	minimum, maximum = _bounds(meshes)
	center = (minimum + maximum) * 0.5
	size = maximum - minimum
	span = max(size.x, size.y, size.z)
	view = Vector((0.78, -1.36, 0.72)).normalized()
	camera.location = center + view * max(span * 3.0, 8.0)
	camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
	camera.data.ortho_scale = span * 1.58

	OUTPUT.mkdir(parents=True, exist_ok=True)
	target = OUTPUT / f"{stem}.png"
	bpy.context.scene.render.filepath = str(target)
	bpy.ops.render.render(write_still=True)
	print(
		"DIRTY_CASTLE_REFERENCE|%s|source=%s|bounds=%s..%s"
		% (
			stem,
			resource_path,
			tuple(round(value, 4) for value in minimum),
			tuple(round(value, 4) for value in maximum),
		),
		flush=True,
	)

	for obj in imported:
		bpy.data.objects.remove(obj, do_unlink=True)


def main() -> None:
	camera = _configure_scene()
	for resource_path, stem in JOBS:
		_render_reference(camera, resource_path, stem)
	print(f"DIRTY_CASTLE_REFERENCE|RESULT=OK|count={len(JOBS)}", flush=True)


if __name__ == "__main__":
	main()
