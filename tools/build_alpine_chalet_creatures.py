#!/usr/bin/env python3
"""Build the three collectible Alpine chalet habitats in Blender 4.4.

Outputs:
  assets/props/alpine/alpine_fish_aquarium.glb
  assets/props/alpine/alpine_beetle_terrarium.glb
  assets/props/alpine/alpine_bird_cage.glb
  assets_src/blender/alpine_chalet_creatures.blend
  assets_src/blender/qa_alpine_chalet_creatures/*.png

The runtime GLBs deliberately keep a node named ``Collectible`` separate from
the node named ``Cage``. Godot can hide the rescued animal while leaving its
little habitat behind as an immediately readable collected-state marker.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_OUT = ROOT / "assets" / "props" / "alpine"
SOURCE_OUT = ROOT / "assets_src" / "blender"
QA_OUT = SOURCE_OUT / "qa_alpine_chalet_creatures"
BLEND_OUT = SOURCE_OUT / "alpine_chalet_creatures.blend"

RUNTIME_OUT.mkdir(parents=True, exist_ok=True)
SOURCE_OUT.mkdir(parents=True, exist_ok=True)
QA_OUT.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0


PALETTE = {
    "navy": (0.075, 0.07, 0.18, 1.0),
    "indigo": (0.25, 0.20, 0.45, 1.0),
    "aqua": (0.24, 0.78, 0.82, 1.0),
    "sky": (0.46, 0.75, 0.94, 1.0),
    "mint": (0.45, 0.84, 0.66, 1.0),
    "leaf": (0.24, 0.58, 0.38, 1.0),
    "lavender": (0.70, 0.56, 0.90, 1.0),
    "coral": (0.96, 0.38, 0.44, 1.0),
    "orange": (1.0, 0.60, 0.24, 1.0),
    "gold": (0.98, 0.76, 0.25, 1.0),
    "cream": (0.97, 0.92, 0.80, 1.0),
    "snow": (0.91, 0.97, 1.0, 1.0),
    "wood": (0.52, 0.31, 0.22, 1.0),
    "dark_wood": (0.30, 0.18, 0.16, 1.0),
    "soil": (0.42, 0.27, 0.22, 1.0),
    "black": (0.035, 0.04, 0.075, 1.0),
}


def material(
    name: str,
    color: tuple[float, float, float, float],
    *,
    roughness: float = 0.82,
    metallic: float = 0.0,
    alpha: float | None = None,
) -> bpy.types.Material:
    mat = bpy.data.materials.new("Alpine_" + name)
    rgba = color if alpha is None else (color[0], color[1], color[2], alpha)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if alpha is not None:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            mat.surface_render_method = "DITHERED"
        except (AttributeError, TypeError):
            pass
        mat.use_transparency_overlap = False
        mat.diffuse_color = rgba
    return mat


MATS = {name: material(name, value) for name, value in PALETTE.items()}
MATS["glass"] = material("glass", (0.46, 0.86, 1.0, 1.0), roughness=0.12, metallic=0.08, alpha=0.16)
MATS["water"] = material("water", (0.24, 0.78, 0.92, 1.0), roughness=0.2, alpha=0.20)
MATS["gold_metal"] = material("gold_metal", PALETTE["gold"], roughness=0.46, metallic=0.28)


def empty(name: str, parent: bpy.types.Object | None = None) -> bpy.types.Object:
    obj = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(obj)
    obj.parent = parent
    return obj


def assign(obj: bpy.types.Object, mat: bpy.types.Material) -> bpy.types.Object:
    obj.data.materials.append(mat)
    return obj


def smooth(obj: bpy.types.Object) -> bpy.types.Object:
    if obj.type == "MESH":
        for polygon in obj.data.polygons:
            polygon.use_smooth = True
    return obj


def apply_modifier(obj: bpy.types.Object, modifier: bpy.types.Modifier) -> None:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.select_set(False)


def bevel(obj: bpy.types.Object, width: float, segments: int = 2) -> bpy.types.Object:
    if width <= 0.0:
        return obj
    modifier = obj.modifiers.new("storybook_soft_edge", "BEVEL")
    modifier.width = width
    modifier.segments = segments
    modifier.limit_method = "ANGLE"
    apply_modifier(obj, modifier)
    return obj


def box(
    name: str,
    location: tuple[float, float, float],
    scale: tuple[float, float, float],
    mat: bpy.types.Material,
    parent: bpy.types.Object,
    bevel_width: float = 0.06,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.parent = parent
    assign(obj, mat)
    return bevel(obj, bevel_width, 2)


def sphere(
    name: str,
    location: tuple[float, float, float],
    scale: tuple[float, float, float],
    mat: bpy.types.Material,
    parent: bpy.types.Object,
    *,
    segments: int = 16,
    rings: int = 10,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.parent = parent
    assign(obj, mat)
    return smooth(obj)


def cylinder(
    name: str,
    location: tuple[float, float, float],
    radius: float,
    depth: float,
    mat: bpy.types.Material,
    parent: bpy.types.Object,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
    vertices: int = 12,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.parent = parent
    assign(obj, mat)
    return smooth(obj)


def cone(
    name: str,
    location: tuple[float, float, float],
    radius1: float,
    radius2: float,
    depth: float,
    mat: bpy.types.Material,
    parent: bpy.types.Object,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
    vertices: int = 12,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.parent = parent
    assign(obj, mat)
    return smooth(obj)


def torus(
    name: str,
    location: tuple[float, float, float],
    major_radius: float,
    minor_radius: float,
    mat: bpy.types.Material,
    parent: bpy.types.Object,
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        major_segments=16,
        minor_segments=6,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.parent = parent
    assign(obj, mat)
    return smooth(obj)


def cylinder_between(
    name: str,
    start: tuple[float, float, float] | Vector,
    end: tuple[float, float, float] | Vector,
    radius: float,
    mat: bpy.types.Material,
    parent: bpy.types.Object,
    vertices: int = 10,
) -> bpy.types.Object:
    p0 = Vector(start)
    p1 = Vector(end)
    direction = p1 - p0
    obj = cylinder(name, tuple((p0 + p1) * 0.5), radius, direction.length, mat, parent, vertices=vertices)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat("Z", "Y")
    return obj


def fin_mesh(
    name: str,
    points: list[tuple[float, float, float]],
    thickness: float,
    mat: bpy.types.Material,
    parent: bpy.types.Object,
) -> bpy.types.Object:
    half = thickness * 0.5
    verts = [(x, y - half, z) for x, y, z in points]
    verts.extend((x, y + half, z) for x, y, z in points)
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent = parent
    assign(obj, mat)
    return bevel(obj, 0.035, 2)


def habitat_root(name: str) -> tuple[bpy.types.Object, bpy.types.Object, bpy.types.Object]:
    root = empty(name)
    # Blender object names are global within a .blend. Keep descriptive source
    # names here, then assign the exact runtime role names while exporting each
    # selected habitat below.
    cage = empty(f"{name}Cage", root)
    cage["habitat_role"] = "cage"
    collectible = empty(f"{name}Collectible", root)
    collectible["habitat_role"] = "collectible"
    return root, cage, collectible


def build_fish_aquarium() -> bpy.types.Object:
    root, cage, collectible = habitat_root("AlpineFishAquarium")
    box("wooden_base", (0.0, 0.0, 0.24), (4.6, 2.8, 0.48), MATS["wood"], cage, 0.10)
    box("snow_trim", (0.0, 0.0, 0.51), (4.35, 2.56, 0.12), MATS["snow"], cage, 0.03)
    box("sand", (0.0, 0.0, 0.66), (4.08, 2.34, 0.18), MATS["cream"], cage, 0.04)

    for x in (-2.12, 2.12):
        for y in (-1.27, 1.27):
            cylinder("navy_corner_post", (x, y, 1.93), 0.075, 2.84, MATS["navy"], cage, vertices=8)
    for z in (0.58, 3.34):
        box("front_frame", (0.0, -1.27, z), (4.35, 0.10, 0.12), MATS["navy"], cage, 0.025)
        box("back_frame", (0.0, 1.27, z), (4.35, 0.10, 0.12), MATS["navy"], cage, 0.025)
        box("left_frame", (-2.12, 0.0, z), (0.10, 2.52, 0.12), MATS["navy"], cage, 0.025)
        box("right_frame", (2.12, 0.0, z), (0.10, 2.52, 0.12), MATS["navy"], cage, 0.025)

    box("front_glass", (0.0, -1.245, 1.96), (4.08, 0.035, 2.65), MATS["glass"], cage, 0.0)
    box("back_glass", (0.0, 1.245, 1.96), (4.08, 0.035, 2.65), MATS["glass"], cage, 0.0)
    box("left_glass", (-2.095, 0.0, 1.96), (0.035, 2.40, 2.65), MATS["glass"], cage, 0.0)
    box("right_glass", (2.095, 0.0, 1.96), (0.035, 2.40, 2.65), MATS["glass"], cage, 0.0)
    box("water_surface", (0.0, 0.0, 3.10), (4.02, 2.34, 0.035), MATS["water"], cage, 0.0)

    for index, x in enumerate((-1.55, 1.45)):
        stem = cylinder("water_plant_stem", (x, 0.72, 1.22), 0.07, 1.18 + index * 0.18, MATS["leaf"], cage, vertices=8)
        stem.rotation_euler.x = 0.12 if index == 0 else -0.10
        sphere("water_plant_leaf", (x - 0.18, 0.66, 1.58), (0.34, 0.10, 0.14), MATS["mint"], cage, segments=10, rings=6)
        sphere("water_plant_leaf", (x + 0.18, 0.71, 1.88), (0.31, 0.10, 0.13), MATS["mint"], cage, segments=10, rings=6)

    sphere("fish_body", (0.12, -0.03, 1.98), (1.18, 0.43, 0.68), MATS["orange"], collectible)
    sphere("fish_muzzle", (0.94, -0.03, 1.98), (0.42, 0.35, 0.43), MATS["gold"], collectible)
    fin_mesh("fish_tail", [(-0.88, 0.0, 2.0), (-1.72, 0.0, 2.72), (-1.72, 0.0, 1.30)], 0.20, MATS["coral"], collectible)
    fin_mesh("fish_top_fin", [(-0.10, 0.0, 2.48), (0.18, 0.0, 3.02), (0.58, 0.0, 2.45)], 0.14, MATS["coral"], collectible)
    fin_mesh("fish_side_fin", [(0.12, -0.34, 1.92), (-0.28, -0.78, 1.60), (0.62, -0.46, 1.70)], 0.10, MATS["coral"], collectible)
    for y in (-0.36, 0.36):
        sphere("fish_eye_white", (0.72, y, 2.18), (0.18, 0.08, 0.18), MATS["snow"], collectible, segments=12, rings=8)
        sphere("fish_eye", (0.78, y * 1.03, 2.19), (0.085, 0.045, 0.085), MATS["navy"], collectible, segments=10, rings=6)
    for x in (-0.36, 0.16):
        torus("fish_story_stripe", (x, -0.01, 1.98), 0.51, 0.075, MATS["cream"], collectible, rotation=(0.0, math.pi * 0.5, 0.0))

    for index, pos in enumerate(((1.35, -0.55, 2.45), (1.63, -0.45, 2.78), (1.42, -0.48, 3.02))):
        sphere(f"bubble_{index}", pos, (0.11, 0.07, 0.11), MATS["glass"], cage, segments=10, rings=6)
    return root


def build_beetle_terrarium() -> bpy.types.Object:
    root, cage, collectible = habitat_root("AlpineBeetleTerrarium")
    box("terrarium_base", (0.0, 0.0, 0.24), (4.3, 2.9, 0.48), MATS["wood"], cage, 0.10)
    box("terrarium_soil", (0.0, 0.0, 0.58), (4.0, 2.58, 0.26), MATS["soil"], cage, 0.05)
    for x in (-1.98, 1.98):
        for y in (-1.28, 1.28):
            cylinder("terrarium_post", (x, y, 1.92), 0.07, 2.75, MATS["dark_wood"], cage, vertices=8)
    for z in (0.58, 3.26):
        box("terrarium_front_rail", (0.0, -1.28, z), (4.08, 0.10, 0.12), MATS["dark_wood"], cage, 0.025)
        box("terrarium_back_rail", (0.0, 1.28, z), (4.08, 0.10, 0.12), MATS["dark_wood"], cage, 0.025)
        box("terrarium_left_rail", (-1.98, 0.0, z), (0.10, 2.48, 0.12), MATS["dark_wood"], cage, 0.025)
        box("terrarium_right_rail", (1.98, 0.0, z), (0.10, 2.48, 0.12), MATS["dark_wood"], cage, 0.025)
    box("terrarium_front_glass", (0.0, -1.255, 1.92), (3.82, 0.035, 2.54), MATS["glass"], cage, 0.0)
    box("terrarium_back_glass", (0.0, 1.255, 1.92), (3.82, 0.035, 2.54), MATS["glass"], cage, 0.0)
    box("terrarium_left_glass", (-1.955, 0.0, 1.92), (0.035, 2.38, 2.54), MATS["glass"], cage, 0.0)
    box("terrarium_right_glass", (1.955, 0.0, 1.92), (0.035, 2.38, 2.54), MATS["glass"], cage, 0.0)
    box("mesh_lid", (0.0, 0.0, 3.28), (4.04, 2.58, 0.10), MATS["navy"], cage, 0.02)
    for index in range(7):
        x = -1.55 + index * 0.52
        box("lid_slit", (x, -0.02, 3.35), (0.10, 2.30, 0.045), MATS["gold"], cage, 0.01)

    cylinder_between("storybook_branch", (-1.35, 0.48, 0.76), (1.30, -0.08, 1.23), 0.16, MATS["wood"], cage, 10)
    sphere("terrarium_leaf", (-1.12, 0.25, 1.05), (0.62, 0.18, 0.30), MATS["leaf"], cage, segments=12, rings=7)
    sphere("terrarium_leaf", (1.18, 0.12, 1.26), (0.55, 0.16, 0.28), MATS["mint"], cage, segments=12, rings=7)

    sphere("beetle_body", (0.0, -0.18, 1.78), (0.78, 0.46, 0.38), MATS["coral"], collectible, segments=16, rings=10)
    sphere("beetle_head", (0.72, -0.18, 1.78), (0.38, 0.36, 0.32), MATS["navy"], collectible, segments=14, rings=8)
    box("beetle_wing_split", (-0.08, -0.20, 2.12), (0.06, 0.75, 0.05), MATS["navy"], collectible, 0.015)
    for x in (-0.33, 0.30):
        for y in (-0.48, 0.12):
            sphere("beetle_spot", (x, y, 2.08), (0.12, 0.07, 0.055), MATS["navy"], collectible, segments=10, rings=6)
    for index, x in enumerate((-0.42, 0.04, 0.48)):
        for side in (-1.0, 1.0):
            start = (x, -0.18 + side * 0.30, 1.72)
            end = (x - 0.20 + index * 0.10, -0.18 + side * 0.88, 1.42 + (index % 2) * 0.08)
            cylinder_between("beetle_leg", start, end, 0.045, MATS["navy"], collectible, 7)
    for side in (-1.0, 1.0):
        cylinder_between("beetle_antenna", (0.92, -0.18 + side * 0.16, 1.91), (1.28, -0.18 + side * 0.42, 2.15), 0.032, MATS["navy"], collectible, 7)
        sphere("antenna_tip", (1.29, -0.18 + side * 0.43, 2.16), (0.07, 0.07, 0.07), MATS["gold"], collectible, segments=8, rings=5)
    for y in (-0.48, 0.12):
        sphere("beetle_eye", (0.91, y, 1.87), (0.075, 0.045, 0.075), MATS["snow"], collectible, segments=8, rings=5)
    return root


def build_bird_cage() -> bpy.types.Object:
    root, cage, collectible = habitat_root("AlpineBirdCage")
    cylinder("round_wooden_base", (0.0, 0.0, 0.24), 2.12, 0.48, MATS["wood"], cage, vertices=20)
    cylinder("snow_base_trim", (0.0, 0.0, 0.51), 1.96, 0.10, MATS["snow"], cage, vertices=20)
    for z, radius in ((0.56, 1.82), (2.80, 1.82), (3.62, 1.76)):
        torus("golden_cage_ring", (0.0, 0.0, z), radius, 0.075, MATS["gold_metal"], cage)
    for index in range(12):
        angle = float(index) / 12.0 * math.tau
        x = math.cos(angle) * 1.80
        y = math.sin(angle) * 1.80
        cylinder("golden_cage_bar", (x, y, 2.10), 0.045, 3.06, MATS["gold_metal"], cage, vertices=8)
        cylinder_between(
            "golden_dome_bar",
            (x, y, 3.60),
            (math.cos(angle) * 0.28, math.sin(angle) * 0.28, 4.55),
            0.045,
            MATS["gold_metal"],
            cage,
            8,
        )
    torus("dome_crown", (0.0, 0.0, 4.56), 0.28, 0.065, MATS["gold_metal"], cage)
    sphere("cage_top_knob", (0.0, 0.0, 4.86), (0.18, 0.18, 0.22), MATS["gold_metal"], cage, segments=12, rings=8)
    cylinder("cage_hanger", (0.0, 0.0, 5.16), 0.055, 0.48, MATS["navy"], cage, vertices=8)
    torus("cage_hanging_loop", (0.0, 0.0, 5.52), 0.32, 0.055, MATS["navy"], cage, rotation=(math.pi * 0.5, 0.0, 0.0))
    cylinder("wooden_perch", (0.0, 0.0, 1.32), 0.12, 3.0, MATS["dark_wood"], cage, rotation=(0.0, math.pi * 0.5, 0.0), vertices=10)

    sphere("bird_body", (0.0, -0.02, 2.08), (0.66, 0.50, 0.86), MATS["sky"], collectible, segments=16, rings=10)
    sphere("bird_belly", (0.0, -0.46, 2.04), (0.43, 0.16, 0.58), MATS["cream"], collectible, segments=14, rings=8)
    sphere("bird_head", (0.0, -0.12, 2.87), (0.56, 0.52, 0.55), MATS["lavender"], collectible, segments=16, rings=10)
    sphere("bird_left_wing", (-0.56, -0.02, 2.16), (0.28, 0.38, 0.62), MATS["indigo"], collectible, segments=14, rings=8)
    sphere("bird_right_wing", (0.56, -0.02, 2.16), (0.28, 0.38, 0.62), MATS["indigo"], collectible, segments=14, rings=8)
    cone("bird_beak", (0.0, -0.72, 2.82), 0.18, 0.02, 0.46, MATS["gold"], collectible, rotation=(math.pi * 0.5, 0.0, 0.0), vertices=10)
    for x in (-0.20, 0.20):
        sphere("bird_eye_white", (x, -0.57, 3.00), (0.13, 0.07, 0.14), MATS["snow"], collectible, segments=10, rings=6)
        sphere("bird_eye", (x, -0.625, 3.00), (0.065, 0.035, 0.075), MATS["navy"], collectible, segments=8, rings=5)
    for x in (-0.22, 0.22):
        cone("bird_tail", (x, 0.12, 1.35), 0.18, 0.055, 0.95, MATS["indigo"], collectible, rotation=(0.0, 0.0, 0.0), vertices=8)
        cylinder("bird_foot", (x, -0.02, 1.43), 0.055, 0.34, MATS["orange"], collectible, vertices=8)
    for index, x in enumerate((-0.28, 0.0, 0.28)):
        cone("bird_crest", (x, -0.04, 3.35 + (0.10 if index == 1 else 0.0)), 0.13, 0.025, 0.45, MATS["gold"], collectible, vertices=8)
    return root


ROOTS = {
    "fish": build_fish_aquarium(),
    "beetle": build_beetle_terrarium(),
    "bird": build_bird_cage(),
}


def descendants(root: bpy.types.Object) -> list[bpy.types.Object]:
    result = [root]
    for child in root.children:
        result.extend(descendants(child))
    return result


def export_root(root: bpy.types.Object, output_name: str) -> None:
    cage = next(
        child for child in root.children
        if child.get("habitat_role") == "cage"
    )
    collectible = next(
        child for child in root.children
        if child.get("habitat_role") == "collectible"
    )
    cage_source_name = cage.name
    collectible_source_name = collectible.name
    cage.name = "Cage"
    collectible.name = "Collectible"
    bpy.ops.object.select_all(action="DESELECT")
    for obj in descendants(root):
        obj.select_set(True)
    bpy.context.view_layer.objects.active = root
    output_path = RUNTIME_OUT / output_name
    bpy.ops.export_scene.gltf(
        filepath=str(output_path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
    )
    cage.name = cage_source_name
    collectible.name = collectible_source_name
    print("EXPORTED", output_path, output_path.stat().st_size, "bytes")


export_root(ROOTS["fish"], "alpine_fish_aquarium.glb")
export_root(ROOTS["beetle"], "alpine_beetle_terrarium.glb")
export_root(ROOTS["bird"], "alpine_bird_cage.glb")


scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 700
scene.render.resolution_y = 700
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = False
scene.render.use_freestyle = False
scene.view_settings.look = "AgX - Medium High Contrast"
if scene.world is None:
    scene.world = bpy.data.worlds.new("Alpine_QA_World")
scene.world.color = (0.16, 0.19, 0.30)

world = scene.world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.19, 0.23, 0.37, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.65

ground = box("QA_snow_floor", (0.0, 0.0, -0.22), (14.0, 14.0, 0.35), MATS["snow"], empty("QA_Set"), 0.04)

key_data = bpy.data.lights.new("QA_key", type="AREA")
key_data.energy = 900.0
key_data.shape = "DISK"
key_data.size = 6.0
key = bpy.data.objects.new("QA_key", key_data)
bpy.context.collection.objects.link(key)
key.location = (4.5, -5.5, 8.5)

fill_data = bpy.data.lights.new("QA_fill", type="AREA")
fill_data.energy = 520.0
fill_data.color = (0.58, 0.78, 1.0)
fill_data.size = 5.0
fill = bpy.data.objects.new("QA_fill", fill_data)
bpy.context.collection.objects.link(fill)
fill.location = (-5.0, -1.0, 5.0)

camera_data = bpy.data.cameras.new("QA_camera")
camera_data.type = "ORTHO"
camera = bpy.data.objects.new("QA_camera", camera_data)
bpy.context.collection.objects.link(camera)
scene.camera = camera


def world_bounds(root: bpy.types.Object) -> tuple[Vector, Vector]:
    points: list[Vector] = []
    for obj in descendants(root):
        if obj.type != "MESH":
            continue
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    mins = Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points)))
    maxs = Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points)))
    return mins, maxs


def render_root(key_name: str, root: bpy.types.Object) -> None:
    for other in ROOTS.values():
        for obj in descendants(other):
            obj.hide_render = other != root
    mins, maxs = world_bounds(root)
    center = (mins + maxs) * 0.5
    extent = maxs - mins
    camera.location = center + Vector((7.2, -9.4, 5.8))
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.ortho_scale = max(extent.x, extent.z) * 1.38
    scene.render.filepath = str(QA_OUT / f"alpine_{key_name}_habitat.png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", scene.render.filepath)


for key_name, root in ROOTS.items():
    render_root(key_name, root)

for root in ROOTS.values():
    for obj in descendants(root):
        obj.hide_render = False
ground.hide_render = False
ROOTS["fish"].location.x = -5.6
ROOTS["bird"].location.x = 5.6
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_OUT))
print("SAVED", BLEND_OUT)
