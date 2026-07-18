#!/usr/bin/env python3
"""Render every isolated regeneration GLB for visual review."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector
from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "full_texture_regen_2026-07-18"
MANIFEST = PACK / "model_manifest.json"
OUT_DIR = ROOT / "audit" / "full_regen_2026-07-18" / "renders" / "models"
METRICS = ROOT / "audit" / "full_regen_2026-07-18" / "model_render_metrics.csv"
RESOLUTION = 320
BACKGROUND = (0.79, 0.90, 0.91, 1.0)


def clear_scene() -> None:
	bpy.ops.object.select_all(action="SELECT")
	bpy.ops.object.delete(use_global=False)
	for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
		for datablock in list(datablocks):
			if datablock.users == 0:
				datablocks.remove(datablock)


def mesh_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, float, float]:
	corners: list[Vector] = []
	for obj in objects:
		if obj.type not in {"MESH", "CURVE"}:
			continue
		corners.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
	if not corners:
		raise RuntimeError("Imported asset contains no renderable bounds")
	minimum = Vector((min(point.x for point in corners), min(point.y for point in corners), min(point.z for point in corners)))
	maximum = Vector((max(point.x for point in corners), max(point.y for point in corners), max(point.z for point in corners)))
	center = (minimum + maximum) * 0.5
	radius = max((point - center).length for point in corners)
	return center, max(radius, 0.25), minimum.z


def point_camera(camera: bpy.types.Object, target: Vector) -> None:
	camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()


def add_camera(center: Vector, radius: float, role_id: str) -> bpy.types.Object:
	data = bpy.data.cameras.new("ReviewCamera")
	camera = bpy.data.objects.new("ReviewCamera", data)
	bpy.context.collection.objects.link(camera)
	front_facing = any(token in role_id for token in ("BUTTERFLY", "STAR"))
	flat_overhead = "FLOOR" in role_id
	if front_facing:
		view = Vector((0.05, -1.0, 0.12))
	elif flat_overhead:
		view = Vector((0.1, -0.12, 1.0))
	else:
		view = Vector((1.25, -1.6, 1.05))
	view.normalize()
	camera.location = center + view * radius * 4.2
	data.type = "ORTHO"
	data.ortho_scale = radius * (2.45 if flat_overhead or front_facing else 2.8)
	data.lens = 50
	point_camera(camera, center)
	bpy.context.scene.camera = camera
	return camera


def add_lighting(center: Vector, radius: float) -> None:
	sun_data = bpy.data.lights.new("ReviewSun", type="SUN")
	sun_data.energy = 2.2
	sun_data.angle = math.radians(28.0)
	sun = bpy.data.objects.new("ReviewSun", sun_data)
	sun.rotation_euler = (math.radians(32.0), math.radians(-18.0), math.radians(-38.0))
	bpy.context.collection.objects.link(sun)

	key_data = bpy.data.lights.new("Key", type="AREA")
	key_data.energy = max(900.0, radius * radius * 180.0)
	key_data.shape = "DISK"
	key_data.size = max(4.0, radius * 2.5)
	key = bpy.data.objects.new("Key", key_data)
	key.location = center + Vector((-radius * 1.5, -radius * 2.0, radius * 3.0))
	bpy.context.collection.objects.link(key)
	point_camera(key, center)

	fill_data = bpy.data.lights.new("Fill", type="AREA")
	fill_data.energy = max(500.0, radius * radius * 90.0)
	fill_data.size = max(3.0, radius * 2.0)
	fill = bpy.data.objects.new("Fill", fill_data)
	fill.location = center + Vector((radius * 2.0, radius * 0.5, radius * 1.5))
	bpy.context.collection.objects.link(fill)
	point_camera(fill, center)


def add_ground(center: Vector, radius: float, floor_z: float) -> None:
	bpy.ops.mesh.primitive_plane_add(size=max(20.0, radius * 12.0), location=(center.x, center.y, floor_z - radius * 0.025))
	plane = bpy.context.object
	plane.name = "ReviewGround"
	material = bpy.data.materials.new("ReviewGroundMat")
	material.diffuse_color = (0.68, 0.84, 0.84, 1.0)
	material.use_nodes = True
	principled = material.node_tree.nodes.get("Principled BSDF")
	principled.inputs["Base Color"].default_value = material.diffuse_color
	principled.inputs["Roughness"].default_value = 1.0
	plane.data.materials.append(material)


def configure_scene(path: Path) -> None:
	scene = bpy.context.scene
	scene.render.engine = "BLENDER_EEVEE"
	scene.render.resolution_x = RESOLUTION
	scene.render.resolution_y = RESOLUTION
	scene.render.resolution_percentage = 100
	scene.render.image_settings.file_format = "PNG"
	scene.render.image_settings.color_mode = "RGB"
	scene.render.film_transparent = False
	scene.render.filepath = str(path)
	scene.render.use_file_extension = True
	scene.render.image_settings.color_depth = "8"
	scene.render.resolution_percentage = 100
	scene.world.use_nodes = True
	background = scene.world.node_tree.nodes.get("Background")
	background.inputs["Color"].default_value = BACKGROUND
	background.inputs["Strength"].default_value = 0.8
	scene.render.film_transparent = False
	scene.render.engine = "BLENDER_EEVEE"
	scene.render.image_settings.compression = 35
	scene.view_settings.look = "AgX - Medium High Contrast"


def render_entry(entry: dict[str, object]) -> dict[str, str]:
	clear_scene()
	asset_path = ROOT / str(entry["path"])
	output_path = OUT_DIR / f"{entry['name']}.png"
	bpy.ops.import_scene.gltf(filepath=str(asset_path))
	imported = [obj for obj in bpy.context.scene.objects if obj.type in {"MESH", "CURVE"}]
	center, radius, floor_z = mesh_bounds(imported)
	add_ground(center, radius, floor_z)
	add_camera(center, radius, str(entry["role_id"]).upper())
	add_lighting(center, radius)
	configure_scene(output_path)
	bpy.ops.render.render(write_still=True)
	with Image.open(output_path) as image:
		variance = sum(ImageStat.Stat(image.convert("RGB")).var) / 3.0
		brightness = sum(ImageStat.Stat(image.convert("L")).mean)
	return {
		"name": str(entry["name"]),
		"role_id": str(entry["role_id"]),
		"path": output_path.relative_to(ROOT).as_posix(),
		"variance": f"{variance:.2f}",
		"brightness": f"{brightness:.2f}",
		"status": "pass" if variance >= 20.0 and 20.0 <= brightness <= 245.0 else "reject",
	}


def main() -> None:
	OUT_DIR.mkdir(parents=True, exist_ok=True)
	manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
	entries = manifest["assets"]
	rows: list[dict[str, str]] = []
	for index, entry in enumerate(entries, start=1):
		row = render_entry(entry)
		rows.append(row)
		print(f"RENDER {index:03d}/{len(entries):03d} {row['name']} {row['status']}", flush=True)
	with METRICS.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
		writer.writeheader()
		writer.writerows(rows)
	print(json.dumps({"render_count": len(rows), "reject_count": sum(row["status"] == "reject" for row in rows)}, indent=2))


if __name__ == "__main__":
	main()
