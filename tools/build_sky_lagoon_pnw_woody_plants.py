#!/usr/bin/env python3
"""Build the Seattle/PNW woody-plant family for Sky Lagoon.

The runtime family is intentionally botanical rather than template-driven:
every tree has its own branch graph and every shrub has a signature leaf,
flower, fruit, or spray system.  The concept art is reference only; these
meshes are deterministic Blender-authored geometry suitable for the Mobile
renderer.

Usage: blender --background --python tools/build_sky_lagoon_pnw_woody_plants.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sky_lagoon" / "lagoon_kit"
BLEND = ROOT / "assets_src" / "blender" / "sky_lagoon_pnw_woody_plants.blend"
OUT.mkdir(parents=True, exist_ok=True)
BLEND.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0

PALETTE = {
    "ink": (0.055, 0.035, 0.12, 1.0),
    "bark_dark": (0.19, 0.10, 0.16, 1.0),
    "bark": (0.40, 0.22, 0.18, 1.0),
    "bark_light": (0.66, 0.43, 0.31, 1.0),
    "alder_bark": (0.72, 0.72, 0.64, 1.0),
    "madrone": (0.86, 0.37, 0.28, 1.0),
    "madrone_light": (0.98, 0.65, 0.44, 1.0),
    "moss": (0.50, 0.73, 0.44, 1.0),
    "jade_dark": (0.13, 0.34, 0.35, 1.0),
    "jade": (0.25, 0.55, 0.45, 1.0),
    "mint": (0.46, 0.79, 0.62, 1.0),
    "mint_hi": (0.67, 0.90, 0.70, 1.0),
    "aqua_shadow": (0.27, 0.42, 0.63, 1.0),
    "lavender": (0.57, 0.43, 0.72, 1.0),
    "coral": (0.91, 0.36, 0.47, 1.0),
    "salmon": (1.00, 0.56, 0.40, 1.0),
    "berry": (0.19, 0.16, 0.39, 1.0),
    "berry_blue": (0.27, 0.38, 0.66, 1.0),
    "butter": (0.98, 0.76, 0.30, 1.0),
    "cream": (1.00, 0.91, 0.68, 1.0),
    "white": (0.94, 0.97, 0.94, 1.0),
    "stone": (0.45, 0.60, 0.66, 1.0),
}


def material(name: str) -> bpy.types.Material:
    full_name = "SL_PNW_" + name
    existing = bpy.data.materials.get(full_name)
    if existing is not None:
        return existing
    mat = bpy.data.materials.new(full_name)
    mat.diffuse_color = PALETTE[name]
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = PALETTE[name]
    bsdf.inputs["Roughness"].default_value = 0.94
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.14
    return mat


def new_root(name: str, common: str, latin: str, habitat: str) -> bpy.types.Object:
    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root["role"] = name
    root["species_common"] = common
    root["species_latin"] = latin
    root["habitat"] = habitat
    root["style_gate"] = "sky_lagoon_pnw_woody_gen1"
    return root


def mesh_object(name: str, vertices: list[tuple[float, float, float]],
                faces: list[tuple[int, ...]], materials: tuple[str, ...],
                parent: bpy.types.Object,
                material_indices: list[int] | None = None) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.validate(clean_customdata=True)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.parent = parent
    for mat_name in materials:
        mesh.materials.append(material(mat_name))
    if material_indices is not None:
        for polygon, index in zip(mesh.polygons, material_indices):
            polygon.material_index = index
    return obj


def tube(name: str, points: list[tuple[float, float, float, float]],
         parent: bpy.types.Object, mat_name: str = "bark", sides: int = 7
         ) -> bpy.types.Object:
    centers = [Vector(point[:3]) for point in points]
    vertices: list[tuple[float, float, float]] = []
    previous_u: Vector | None = None
    for index, (center, point) in enumerate(zip(centers, points)):
        if index == 0:
            tangent = centers[1] - center
        elif index == len(centers) - 1:
            tangent = center - centers[index - 1]
        else:
            tangent = centers[index + 1] - centers[index - 1]
        tangent.normalize()
        reference = Vector((0.0, 0.0, 1.0))
        if abs(tangent.dot(reference)) > 0.86:
            reference = Vector((1.0, 0.0, 0.0))
        u = tangent.cross(reference).normalized()
        if previous_u is not None and u.dot(previous_u) < 0.0:
            u.negate()
        previous_u = u.copy()
        v = tangent.cross(u).normalized()
        for side in range(sides):
            angle = math.tau * side / sides
            position = center + point[3] * (math.cos(angle) * u + math.sin(angle) * v)
            vertices.append(tuple(position))
    faces: list[tuple[int, ...]] = []
    for ring in range(len(points) - 1):
        for side in range(sides):
            next_side = (side + 1) % sides
            faces.append((ring * sides + side, ring * sides + next_side,
                          (ring + 1) * sides + next_side,
                          (ring + 1) * sides + side))
    faces.append(tuple(reversed(range(sides))))
    last = (len(points) - 1) * sides
    faces.append(tuple(last + side for side in range(sides)))
    return mesh_object(name, vertices, faces, (mat_name,), parent)


def blob(name: str, center: tuple[float, float, float],
         scale: tuple[float, float, float], colors: tuple[str, str, str],
         parent: bpy.types.Object, seed: float, rings: int = 5,
         segments: int = 9, rotation: float = 0.0) -> bpy.types.Object:
    vertices: list[tuple[float, float, float]] = []
    for ring in range(rings):
        fraction = ring / max(rings - 1, 1)
        latitude = math.pi * fraction
        radial = max(0.24, math.sin(latitude) ** 0.78)
        vertical = math.cos(latitude)
        for segment in range(segments):
            angle = math.tau * segment / segments
            lobes = 1.0 + 0.12 * math.sin(angle * 3.0 + seed)
            local_x = math.cos(angle) * scale[0] * radial * lobes
            local_y = math.sin(angle) * scale[1] * radial * \
                (1.0 + 0.06 * math.cos(angle * 4.0 - seed))
            vertices.append((
                center[0] + local_x * math.cos(rotation) - local_y * math.sin(rotation),
                center[1] + local_x * math.sin(rotation) + local_y * math.cos(rotation),
                center[2] + vertical * scale[2]))
    faces: list[tuple[int, ...]] = []
    indices: list[int] = []
    for ring in range(rings - 1):
        for segment in range(segments):
            nxt = (segment + 1) % segments
            faces.append((ring * segments + segment, ring * segments + nxt,
                          (ring + 1) * segments + nxt,
                          (ring + 1) * segments + segment))
            indices.append(0 if ring < 2 else (1 if ring == 2 else 2))
    faces.append(tuple(reversed(range(segments))))
    indices.append(0)
    last = (rings - 1) * segments
    faces.append(tuple(last + segment for segment in range(segments)))
    indices.append(2)
    return mesh_object(name, vertices, faces, colors, parent, indices)


LEAF_SHAPES = {
    "oval": [(-0.00, -0.50), (-0.42, -0.24), (-0.48, 0.08),
             (-0.28, 0.37), (0.00, 0.50), (0.28, 0.37),
             (0.48, 0.08), (0.42, -0.24)],
    "round": [(0.00, -0.48), (-0.42, -0.31), (-0.50, 0.02),
              (-0.36, 0.35), (0.00, 0.50), (0.36, 0.35),
              (0.50, 0.02), (0.42, -0.31)],
    "triangle": [(0.00, -0.48), (-0.46, -0.12), (-0.32, 0.20),
                 (0.00, 0.50), (0.32, 0.20), (0.46, -0.12)],
    "lobed": [(0.00, -0.50), (-0.20, -0.35), (-0.43, -0.32),
              (-0.29, -0.12), (-0.50, 0.03), (-0.27, 0.12),
              (-0.38, 0.36), (0.00, 0.50), (0.38, 0.36),
              (0.27, 0.12), (0.50, 0.03), (0.29, -0.12),
              (0.43, -0.32), (0.20, -0.35)],
    "palmate": [(0.00, -0.46), (-0.11, -0.18), (-0.42, -0.28),
                (-0.24, -0.02), (-0.50, 0.14), (-0.19, 0.18),
                (-0.25, 0.50), (0.00, 0.27), (0.25, 0.50),
                (0.19, 0.18), (0.50, 0.14), (0.24, -0.02),
                (0.42, -0.28), (0.11, -0.18)],
    "spiny": [(0.00, -0.50), (-0.16, -0.25), (-0.47, -0.25),
              (-0.24, -0.05), (-0.48, 0.12), (-0.19, 0.16),
              (0.00, 0.50), (0.19, 0.16), (0.48, 0.12),
              (0.24, -0.05), (0.47, -0.25), (0.16, -0.25)],
    "needle": [(0.00, -0.50), (-0.14, -0.12), (-0.08, 0.30),
               (0.00, 0.50), (0.08, 0.30), (0.14, -0.12)],
}


def leaf(name: str, center: tuple[float, float, float], length: float,
         width: float, parent: bpy.types.Object, color: str, shape: str,
         yaw: float, pitch: float = 0.18, roll: float = 0.0,
         thickness: float = 0.025) -> bpy.types.Object:
    outline = LEAF_SHAPES[shape]
    direction = Vector((math.sin(yaw) * math.cos(pitch),
                        math.cos(yaw) * math.cos(pitch), math.sin(pitch)))
    across = Vector((math.cos(yaw), -math.sin(yaw), 0.0))
    normal = direction.cross(across).normalized()
    across = (across * math.cos(roll) + normal * math.sin(roll)).normalized()
    normal = direction.cross(across).normalized()
    origin = Vector(center)
    vertices: list[tuple[float, float, float]] = []
    for side in (-1.0, 1.0):
        for x, y in outline:
            point = origin + across * (x * width) + direction * (y * length)
            point += normal * (side * thickness + (0.04 * length * (1.0 - abs(y) * 2.0)))
            vertices.append(tuple(point))
    count = len(outline)
    faces: list[tuple[int, ...]] = [tuple(range(count)),
                                    tuple(reversed(range(count, count * 2)))]
    for index in range(count):
        nxt = (index + 1) % count
        faces.append((index, nxt, count + nxt, count + index))
    return mesh_object(name, vertices, faces, (color,), parent)


def berry(name: str, position: tuple[float, float, float], radius: float,
          parent: bpy.types.Object, color: str) -> None:
    blob(name, position, (radius, radius, radius), (color, color, color),
         parent, sum(position), rings=3, segments=7)


def flower(name: str, position: tuple[float, float, float], radius: float,
           parent: bpy.types.Object, petal: str, center_color: str = "butter",
           petals: int = 5, yaw: float = 0.0) -> None:
    for index in range(petals):
        angle = yaw + math.tau * index / petals
        offset = (position[0] + math.cos(angle) * radius * 0.58,
                  position[1] + math.sin(angle) * radius * 0.58,
                  position[2] + 0.02)
        leaf(name + "_petal_%02d" % index, offset, radius * 1.15,
             radius * 0.62, parent, petal, "oval", angle - math.pi * 0.5,
             pitch=0.08, roll=angle, thickness=0.018)
    berry(name + "_center", position, radius * 0.26, parent, center_color)


def root_flare(parent: bpy.types.Object, radius: float, count: int,
               mat_name: str = "bark_light", seed: float = 0.0) -> None:
    for index in range(count):
        angle = math.tau * index / count + seed
        length = radius * (0.82 + 0.14 * math.sin(index * 2.3 + seed))
        tube("root_%02d" % index,
             [(0.0, 0.0, 0.28, radius * 0.13),
              (math.cos(angle) * length * 0.46,
               math.sin(angle) * length * 0.40, 0.12, radius * 0.09),
              (math.cos(angle) * length,
               math.sin(angle) * length * 0.76, 0.035, radius * 0.025)],
             parent, mat_name, 6)


def ground_details(parent: bpy.types.Object, radius: float, mossy: bool = False) -> None:
    for index in range(5):
        angle = 0.45 + index * math.tau / 5.0
        size = 0.14 + 0.035 * (index % 3)
        blob("ground_stone_%02d" % index,
             (math.cos(angle) * radius, math.sin(angle) * radius * 0.72, 0.09),
             (size * 1.35, size, size * 0.58),
             (("moss" if mossy and index % 2 == 0 else "stone"),) * 3,
             parent, index + radius, rings=3, segments=7)


def conifer_pad(name: str, center: tuple[float, float, float],
                length: float, width: float, height: float,
                parent: bpy.types.Object, seed: float,
                colors: tuple[str, str, str] = ("jade_dark", "jade", "mint"),
                yaw: float = 0.0) -> None:
    blob(name, center, (width, length, height), colors, parent, seed,
         rings=3, segments=7, rotation=-yaw)


def cone(name: str, position: tuple[float, float, float], scale: float,
         parent: bpy.types.Object, mat_name: str = "bark_light") -> None:
    blob(name, position, (scale * 0.52, scale * 0.52, scale),
         (mat_name, mat_name, mat_name), parent, sum(position), rings=4, segments=7)


def douglas_fir() -> bpy.types.Object:
    root = new_root("lagoon_tree_douglas_fir", "Coastal Douglas-fir",
                    "Pseudotsuga menziesii", "dry-moist meadow forest")
    tube("furrowed_trunk", [(0, 0, 0.02, 0.72), (0.08, -0.04, 3.3, 0.55),
                             (-0.10, 0.02, 7.1, 0.27), (0.02, 0, 10.4, 0.06)],
         root, "bark_dark", 10)
    root_flare(root, 2.25, 9, "bark", 0.18)
    for tier in range(8):
        z = 2.6 + tier * 0.91
        radius = 3.55 - tier * 0.36
        for branch_index in range(4):
            angle = tier * 0.43 + branch_index * math.tau / 4.0
            start = Vector((0.02 * math.sin(tier), 0, z))
            mid = start + Vector((math.cos(angle) * radius * 0.52,
                                  math.sin(angle) * radius * 0.52, -0.08))
            end = start + Vector((math.cos(angle) * radius,
                                  math.sin(angle) * radius, -0.30 - 0.04 * tier))
            tube("fir_branch_%02d_%02d" % (tier, branch_index),
                 [(*start, 0.17 - tier * 0.010), (*mid, 0.105), (*end, 0.035)],
                 root, "bark", 6)
            for pad_index, fraction in enumerate((0.46, 0.72, 0.94)):
                point = start.lerp(end, fraction)
                conifer_pad("fir_pad_%02d_%02d_%02d" % (tier, branch_index, pad_index),
                            tuple(point + Vector((0, 0, 0.10))), 0.56, 0.58,
                            0.27, root, tier * 1.9 + branch_index + pad_index,
                            yaw=angle)
    # Signature dead lower limb and hanging cones make this more than a generic pine.
    tube("fir_dead_limb", [(0, 0, 2.2, 0.16), (-1.10, -0.30, 2.22, 0.08),
                            (-1.70, -0.45, 2.08, 0.025)], root, "bark_light", 6)
    for index in range(6):
        angle = 0.4 + index * 1.03
        cone("fir_cone_%02d" % index,
             (math.cos(angle) * (1.15 + 0.12 * index),
              math.sin(angle) * (1.15 + 0.12 * index), 4.9 + 0.55 * (index % 3)),
             0.24, root)
    ground_details(root, 1.70, True)
    return root


def western_redcedar() -> bpy.types.Object:
    root = new_root("lagoon_tree_western_redcedar", "Western redcedar",
                    "Thuja plicata", "moist-wet forest edge")
    tube("cedar_fluted_trunk", [(0, 0, 0.02, 0.88), (-0.08, 0.02, 3.5, 0.62),
                                 (0.08, 0.0, 7.3, 0.28), (-0.10, 0.05, 9.3, 0.10),
                                 (-0.38, 0.08, 9.85, 0.035)], root, "bark", 10)
    root_flare(root, 3.0, 10, "bark_light", 0.05)
    # Broad, layered skirts built from hanging scale-spray fans.
    for tier in range(8):
        z = 2.0 + tier * 0.92
        radius = 4.15 - tier * 0.43
        fans = 6 if tier < 5 else 4
        for fan_index in range(fans):
            angle = tier * 0.34 + fan_index * math.tau / fans
            origin = Vector((0, 0, z))
            shoulder = origin + Vector((math.cos(angle) * radius * 0.60,
                                        math.sin(angle) * radius * 0.60, -0.05))
            tip = origin + Vector((math.cos(angle) * radius,
                                   math.sin(angle) * radius, -0.72))
            tube("cedar_bough_%02d_%02d" % (tier, fan_index),
                 [(*origin, 0.16), (*shoulder, 0.08), (*tip, 0.025)], root, "bark_dark", 6)
            for drop in range(3):
                fraction = 0.45 + drop * 0.22
                point = shoulder.lerp(tip, fraction)
                conifer_pad("cedar_scale_fan_%02d_%02d_%02d" % (tier, fan_index, drop),
                            (point.x, point.y, point.z - 0.24 - drop * 0.08),
                            0.30 + drop * 0.12, 0.64 - drop * 0.07,
                            0.48 + drop * 0.05, root,
                            tier * 2.1 + fan_index + drop,
                            ("jade_dark", "jade", "mint"), yaw=angle)
    ground_details(root, 2.20, True)
    return root


def western_hemlock() -> bpy.types.Object:
    root = new_root("lagoon_tree_western_hemlock", "Western hemlock",
                    "Tsuga heterophylla", "cool moist part-shade forest")
    tube("hemlock_trunk", [(0, 0, 0.02, 0.57), (0.05, 0, 4.8, 0.34),
                            (-0.08, 0.02, 8.4, 0.13), (0.12, 0.02, 9.45, 0.07),
                            (0.58, 0.04, 9.92, 0.025), (0.73, 0.06, 9.48, 0.015)],
         root, "bark_dark", 8)
    root_flare(root, 1.75, 7, "bark", 0.28)
    for tier in range(8):
        z = 2.4 + tier * 0.84
        radius = 3.10 - tier * 0.30
        for branch_index in range(3):
            angle = tier * 0.69 + branch_index * math.tau / 3.0
            end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                          z - 0.52))
            tube("hemlock_branch_%02d_%02d" % (tier, branch_index),
                 [(0, 0, z, 0.13), (end.x * 0.65, end.y * 0.65, z - 0.06, 0.065),
                  (*end, 0.024), (end.x * 1.03, end.y * 1.03, end.z - 0.38, 0.012)],
                 root, "bark", 6)
            for pad_index, fraction in enumerate((0.45, 0.72, 0.96)):
                point = Vector((0, 0, z)).lerp(end, fraction)
                conifer_pad("hemlock_feather_%02d_%02d_%02d" %
                            (tier, branch_index, pad_index), tuple(point),
                            0.48, 0.48, 0.20, root,
                            tier + branch_index * 1.7 + pad_index,
                            ("aqua_shadow", "jade_dark", "jade"), yaw=angle)
    ground_details(root, 1.45, True)
    return root


def sitka_spruce() -> bpy.types.Object:
    root = new_root("lagoon_tree_sitka_spruce", "Sitka spruce",
                    "Picea sitchensis", "wet coastal forest")
    tube("spruce_trunk", [(0, 0, 0.02, 0.70), (-0.04, 0.03, 4.0, 0.45),
                           (0.04, -0.02, 7.6, 0.20), (0, 0, 9.25, 0.035)],
         root, "bark_dark", 9)
    root_flare(root, 2.25, 8, "bark", 0.36)
    for tier in range(9):
        z = 1.75 + tier * 0.78
        radius = 4.25 - tier * 0.39
        count = 5 if tier < 6 else 4
        for branch_index in range(count):
            angle = tier * 0.39 + branch_index * math.tau / count
            end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                          z + 0.12))
            tube("spruce_stiff_branch_%02d_%02d" % (tier, branch_index),
                 [(0, 0, z, 0.16), (end.x * 0.54, end.y * 0.54, z + 0.02, 0.09),
                  (*end, 0.025)], root, "bark", 6)
            for pad_index, fraction in enumerate((0.42, 0.68, 0.91)):
                point = Vector((0, 0, z)).lerp(end, fraction)
                # Short radial star pads make Sitka read prickly and stiff.
                conifer_pad("spruce_spike_pad_%02d_%02d_%02d" %
                            (tier, branch_index, pad_index), tuple(point),
                            0.38, 0.56, 0.32, root,
                            tier * 1.3 + branch_index + pad_index,
                            ("jade_dark", "aqua_shadow", "mint"), yaw=angle)
                if pad_index == 2:
                    direction = angle + (0.7 if branch_index % 2 else -0.7)
                    leaf("spruce_side_spike_%02d_%02d" % (tier, branch_index),
                         (point.x, point.y, point.z + 0.06), 0.72, 0.24,
                         root, "jade", "needle", direction, pitch=0.20)
    ground_details(root, 1.70, False)
    return root


def shore_pine() -> bpy.types.Object:
    root = new_root("lagoon_tree_shore_pine", "Shore pine",
                    "Pinus contorta var. contorta", "dry windy shore and bog edge")
    tube("shore_pine_crooked_trunk",
         [(0, 0, 0.02, 0.62), (-0.55, 0.15, 1.65, 0.52),
          (-0.18, -0.12, 3.15, 0.39), (-0.82, 0.08, 4.80, 0.27),
          (-0.35, 0.0, 6.65, 0.10)], root, "bark", 9)
    root_flare(root, 2.10, 7, "bark_light", 0.12)
    branch_specs = (
        ((-0.30, 0.0, 2.45, 0.30), (1.35, -0.25, 3.15, 0.20), (3.20, -0.35, 3.42, 0.06)),
        ((-0.55, 0.08, 3.55, 0.28), (-2.05, 0.55, 4.20, 0.17), (-3.25, 0.90, 4.18, 0.05)),
        ((-0.68, 0.04, 4.45, 0.24), (0.72, 0.75, 5.25, 0.15), (2.35, 1.10, 5.42, 0.045)),
        ((-0.50, 0.0, 5.30, 0.19), (-1.60, -0.65, 6.00, 0.11), (-2.20, -1.00, 6.08, 0.035)),
        ((-0.42, 0.0, 5.90, 0.17), (0.60, -0.30, 6.56, 0.09), (1.45, -0.45, 6.72, 0.025)),
    )
    for index, points in enumerate(branch_specs):
        tube("shore_pine_branch_%02d" % index, list(points), root, "bark_dark", 7)
        for tuft_index, point in enumerate(points[1:]):
            for needle_index in range(5):
                angle = index * 1.17 + tuft_index * 0.8 + needle_index * math.tau / 5.0
                leaf("shore_pine_needle_%02d_%02d_%02d" %
                     (index, tuft_index, needle_index), point[:3], 0.72, 0.19,
                     root, "jade_dark" if needle_index % 2 else "jade", "needle",
                     angle, pitch=0.16 + 0.18 * (needle_index % 2))
        cone("shore_pine_cone_%02d" % index,
             (points[-1][0] * 0.92, points[-1][1] * 0.92, points[-1][2] - 0.22),
             0.23, root)
    # Open, wind-pruned needle clouds stay confined to branch terminals.
    foliage_masses(root, "shore_pine_terminal_cloud", (
        ((3.00, -0.32, 3.48), (0.82, 0.58, 0.38), -0.08),
        ((-3.05, 0.84, 4.26), (0.86, 0.60, 0.40), 0.24),
        ((2.18, 1.02, 5.50), (0.80, 0.56, 0.38), 0.36),
        ((-2.06, -0.94, 6.15), (0.74, 0.54, 0.36), -0.40),
        ((1.32, -0.42, 6.78), (0.70, 0.50, 0.34), -0.12),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 1.65, False)
    return root


def pacific_yew() -> bpy.types.Object:
    root = new_root("lagoon_tree_pacific_yew", "Pacific yew",
                    "Taxus brevifolia", "shaded moist understory")
    trunks = (
        [(-0.50, 0.05, 0.02, 0.38), (-0.75, 0.12, 2.1, 0.27), (-0.35, 0.0, 5.15, 0.08)],
        [(0.28, -0.08, 0.02, 0.44), (0.58, -0.18, 2.5, 0.28), (0.10, -0.05, 5.60, 0.07)],
        [(0.78, 0.22, 0.02, 0.31), (0.98, 0.42, 1.85, 0.20), (1.34, 0.55, 4.45, 0.06)],
    )
    for index, points in enumerate(trunks):
        tube("yew_twisted_stem_%02d" % index, points, root,
             "bark_dark" if index % 2 else "bark", 7)
    root_flare(root, 1.75, 8, "bark", 0.4)
    for tier in range(5):
        z = 1.6 + tier * 0.78
        for spray_index in range(5):
            angle = tier * 0.55 + spray_index * math.tau / 5.0
            radius = 2.55 - tier * 0.20 + 0.18 * (spray_index % 2)
            start = Vector((0.18 * math.sin(tier), 0.1 * math.cos(tier), z))
            end = start + Vector((math.cos(angle) * radius,
                                  math.sin(angle) * radius, 0.18 - 0.12 * (spray_index % 2)))
            tube("yew_branch_%02d_%02d" % (tier, spray_index),
                 [(*start, 0.10), (*end, 0.025)], root, "bark_dark", 6)
            for leaf_index in range(4):
                point = start.lerp(end, 0.38 + leaf_index * 0.18)
                leaf("yew_flat_leaf_%02d_%02d_%02d" %
                     (tier, spray_index, leaf_index), tuple(point), 0.52, 0.25,
                     root, "jade_dark" if leaf_index % 2 else "jade", "needle",
                     angle + (-0.30 if leaf_index % 2 else 0.30), pitch=0.08)
    for index in range(9):
        angle = index * 2.13
        berry("yew_aril_%02d" % index,
              (math.cos(angle) * (1.0 + 0.11 * index),
               math.sin(angle) * (0.75 + 0.08 * index), 2.0 + 0.36 * (index % 5)),
              0.12, root, "coral")
    foliage_masses(root, "yew_flat_spray_mass", (
        ((-1.65, 0.12, 1.82), (1.10, 0.62, 0.34), -0.05),
        ((1.72, -0.10, 2.08), (1.12, 0.64, 0.34), 0.05),
        ((-1.30, -0.52, 2.92), (1.08, 0.66, 0.36), 0.20),
        ((1.42, 0.50, 3.18), (1.10, 0.66, 0.36), -0.20),
        ((-0.82, 0.20, 4.20), (0.98, 0.62, 0.34), -0.08),
        ((0.85, -0.18, 4.60), (0.94, 0.60, 0.32), 0.08),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 1.42, True)
    return root


def branch_leaf_run(parent: bpy.types.Object, prefix: str,
                    points: list[tuple[float, float, float, float]],
                    leaf_shape: str, leaf_color: str, leaf_length: float,
                    leaf_width: float, count: int, seed: float,
                    bark_color: str = "bark", alternate_color: str | None = None,
                    pitch: float = 0.28) -> None:
    tube(prefix + "_wood", points, parent, bark_color, 7)
    start = Vector(points[0][:3])
    end = Vector(points[-1][:3])
    branch_angle = math.atan2(end.x - start.x, end.y - start.y)
    for index in range(count):
        fraction = 0.32 + 0.64 * index / max(count - 1, 1)
        point = start.lerp(end, fraction)
        side = -1.0 if index % 2 else 1.0
        color = alternate_color if alternate_color is not None and index % 3 == 0 else leaf_color
        leaf(prefix + "_leaf_%02d" % index,
             (point.x + math.cos(branch_angle) * side * 0.12,
              point.y - math.sin(branch_angle) * side * 0.12,
              point.z + 0.12 * ((index % 3) - 1)),
             leaf_length * (0.90 + 0.08 * ((index + 1) % 3)), leaf_width,
             parent, color, leaf_shape,
             branch_angle + side * (0.70 + 0.08 * math.sin(seed + index)),
             pitch=pitch + 0.10 * (index % 2), roll=0.18 * side)


def foliage_masses(parent: bpy.types.Object, prefix: str,
                   specs: tuple[tuple[tuple[float, float, float],
                                      tuple[float, float, float], float], ...],
                   colors: tuple[str, str, str]) -> None:
    """Add a hand-arranged crown; each species supplies a different graph."""
    for index, (position, scale, rotation) in enumerate(specs):
        blob(prefix + "_%02d" % index, position, scale, colors, parent,
             index * 1.71 + rotation, rings=5, segments=10, rotation=rotation)


def bigleaf_maple() -> bpy.types.Object:
    root = new_root("lagoon_tree_bigleaf_maple", "Bigleaf maple",
                    "Acer macrophyllum", "moist meadow and forest edge")
    tube("maple_trunk", [(0, 0, 0.02, 0.95), (-0.15, 0.05, 2.0, 0.82),
                          (0.08, -0.05, 3.2, 0.64)], root, "bark", 10)
    root_flare(root, 2.65, 9, "bark_light", 0.15)
    branches = (
        [(0, 0, 2.55, 0.68), (-1.75, 0.30, 4.15, 0.43), (-3.55, 0.75, 5.50, 0.14)],
        [(0.02, 0, 2.72, 0.66), (1.82, -0.25, 4.25, 0.42), (3.70, -0.62, 5.42, 0.14)],
        [(0.0, 0.0, 3.02, 0.56), (-0.70, -1.25, 4.62, 0.34), (-1.55, -2.25, 6.08, 0.11)],
        [(0.04, 0.02, 3.04, 0.54), (0.82, 1.22, 4.72, 0.33), (1.72, 2.20, 6.00, 0.11)],
        [(0.02, 0.0, 3.15, 0.48), (0.10, 0.05, 5.15, 0.27), (0.35, 0.10, 7.05, 0.08)],
    )
    for index, points in enumerate(branches):
        branch_leaf_run(root, "maple_branch_%02d" % index, points, "palmate",
                        "mint", 1.15, 1.15, 6, index * 1.7,
                        alternate_color="mint_hi", pitch=0.34)
    # Oversized leaf rosettes at every terminal are the species' gameplay cue.
    for branch_index, points in enumerate(branches):
        end = points[-1]
        for index in range(4):
            angle = branch_index * 1.13 + index * math.tau / 4.0
            leaf("maple_terminal_%02d_%02d" % (branch_index, index), end[:3],
                 1.35, 1.35, root, "mint_hi" if index == 0 else "mint",
                 "palmate", angle, pitch=0.42, roll=0.18 * index)
    foliage_masses(root, "maple_umbrella_mass", (
        ((-3.25, 0.52, 5.66), (1.55, 1.05, 0.82), -0.20),
        ((-1.62, -1.62, 6.10), (1.48, 1.08, 0.86), 0.42),
        ((-1.15, 0.62, 6.72), (1.62, 1.16, 0.92), -0.18),
        ((0.22, 0.02, 7.05), (1.54, 1.12, 0.88), 0.10),
        ((1.32, -0.62, 6.66), (1.62, 1.15, 0.90), 0.20),
        ((1.72, 1.62, 6.06), (1.46, 1.06, 0.84), -0.42),
        ((3.35, -0.48, 5.58), (1.52, 1.02, 0.80), 0.24),
    ), ("jade", "mint", "mint_hi"))
    for index, (x, z) in enumerate((
            (-3.72, 5.72), (-2.72, 6.22), (-1.70, 6.86), (-0.60, 7.50),
            (0.55, 7.46), (1.62, 6.86), (2.75, 6.18), (3.74, 5.66))):
        for side in (-1, 1):
            leaf("maple_signature_%02d_%d" % (index, side),
                 (x, side * (0.92 + 0.08 * (index % 2)), z), 1.08, 1.06,
                 root, "mint_hi" if index % 3 == 0 else "mint", "palmate",
                 0.35 * index + (math.pi if side > 0 else 0.0),
                 pitch=0.38, roll=side * 0.22)
    for index in range(5):
        blob("maple_moss_%02d" % index,
             (-0.28 + 0.13 * index, -0.55, 1.1 + index * 0.55),
             (0.26, 0.12, 0.42), ("moss", "moss", "moss"), root,
             index + 0.4, rings=3, segments=7)
    ground_details(root, 2.05, True)
    return root


def red_alder() -> bpy.types.Object:
    root = new_root("lagoon_tree_red_alder", "Red alder", "Alnus rubra",
                    "moist-wet meadow edge")
    tube("alder_pale_trunk", [(0, 0, 0.02, 0.56), (0.08, -0.04, 4.2, 0.39),
                               (-0.08, 0.03, 7.5, 0.16), (0.04, 0.0, 8.55, 0.045)],
         root, "alder_bark", 9)
    root_flare(root, 1.62, 7, "alder_bark", 0.22)
    branches: list[list[tuple[float, float, float, float]]] = []
    for tier in range(6):
        z = 3.0 + tier * 0.75
        radius = 2.70 - tier * 0.22
        for branch_index in range(3):
            angle = tier * 0.56 + branch_index * math.tau / 3.0
            end = (math.cos(angle) * radius, math.sin(angle) * radius,
                   z + 0.85 + 0.10 * (branch_index % 2), 0.035)
            points = [(0, 0, z, 0.14),
                      (math.cos(angle) * radius * 0.52,
                       math.sin(angle) * radius * 0.52, z + 0.34, 0.08), end]
            branches.append(points)
            branch_leaf_run(root, "alder_branch_%02d_%02d" % (tier, branch_index),
                            points, "round", "mint", 0.78, 0.68, 4,
                            tier + branch_index, bark_color="alder_bark",
                            alternate_color="mint_hi", pitch=0.30)
            # Dangling catkin plus woody cone at selected terminals.
            if (tier + branch_index) % 2 == 0:
                catkin = Vector(end[:3]) + Vector((0.10, -0.06, -0.42))
                tube("alder_catkin_%02d_%02d" % (tier, branch_index),
                     [(catkin.x, catkin.y, catkin.z + 0.30, 0.07),
                      (catkin.x + 0.05, catkin.y, catkin.z - 0.18, 0.04)],
                     root, "butter", 6)
                cone("alder_cone_%02d_%02d" % (tier, branch_index),
                     (end[0] - 0.12, end[1], end[2] - 0.18), 0.14, root, "bark_dark")
    foliage_masses(root, "alder_airy_crown", (
        ((-1.20, 0.42, 4.60), (1.02, 0.82, 0.92), -0.18),
        ((1.24, -0.38, 4.78), (1.00, 0.80, 0.96), 0.20),
        ((-1.42, -0.42, 5.72), (1.12, 0.84, 1.00), 0.28),
        ((1.38, 0.48, 5.88), (1.08, 0.82, 1.02), -0.22),
        ((-0.92, 0.34, 6.88), (1.06, 0.82, 1.00), -0.12),
        ((0.95, -0.26, 7.18), (1.00, 0.78, 0.98), 0.16),
        ((0.02, 0.10, 8.05), (0.82, 0.68, 0.84), 0.04),
    ), ("mint", "mint_hi", "jade"))
    for index, (x, z) in enumerate((
            (-1.62, 4.52), (1.58, 4.72), (-1.70, 5.74), (1.68, 5.94),
            (-1.18, 6.96), (1.15, 7.24), (-0.48, 8.10), (0.48, 8.18))):
        leaf("alder_signature_%02d" % index, (x, -0.78, z), 0.74, 0.65,
             root, "mint_hi" if index % 2 else "mint", "round",
             0.42 * index, pitch=0.30)
    ground_details(root, 1.30, True)
    return root


def black_cottonwood() -> bpy.types.Object:
    root = new_root("lagoon_tree_black_cottonwood", "Black cottonwood",
                    "Populus trichocarpa", "wet riverbank and floodplain")
    tube("cottonwood_column_trunk", [(0, 0, 0.02, 0.65), (-0.05, 0, 4.6, 0.43),
                                      (0.06, 0.02, 8.2, 0.18), (0, 0, 9.6, 0.05)],
         root, "bark_dark", 9)
    root_flare(root, 1.90, 8, "bark", 0.31)
    for tier in range(7):
        z = 2.7 + tier * 0.86
        radius = 2.35 - tier * 0.17
        for branch_index in range(3):
            angle = tier * 0.74 + branch_index * math.tau / 3.0
            end = (math.cos(angle) * radius, math.sin(angle) * radius,
                   z + 1.55, 0.035)
            points = [(0, 0, z, 0.14),
                      (math.cos(angle) * radius * 0.52,
                       math.sin(angle) * radius * 0.52, z + 0.75, 0.08), end]
            branch_leaf_run(root, "cottonwood_rising_%02d_%02d" % (tier, branch_index),
                            points, "triangle", "mint", 0.86, 0.70, 4,
                            tier * 1.2 + branch_index, alternate_color="mint_hi",
                            pitch=0.42)
    foliage_masses(root, "cottonwood_flame_crown", (
        ((-0.92, 0.12, 3.92), (0.92, 0.76, 1.18), -0.12),
        ((0.95, -0.18, 4.42), (0.90, 0.72, 1.24), 0.18),
        ((-0.72, -0.32, 5.42), (0.88, 0.70, 1.28), 0.24),
        ((0.78, 0.28, 5.98), (0.86, 0.70, 1.30), -0.18),
        ((-0.58, 0.16, 6.90), (0.82, 0.68, 1.24), -0.08),
        ((0.52, -0.12, 7.54), (0.78, 0.64, 1.16), 0.14),
        ((0.02, 0.08, 8.62), (0.64, 0.56, 0.98), 0.02),
    ), ("jade", "mint", "mint_hi"))
    for index, (x, z) in enumerate((
            (-1.12, 3.74), (1.12, 4.30), (-1.05, 5.02), (1.02, 5.72),
            (-0.92, 6.34), (0.88, 6.96), (-0.68, 7.62), (0.62, 8.25),
            (-0.24, 8.92), (0.28, 9.08))):
        leaf("cottonwood_signature_%02d" % index,
             (x, -0.66 - 0.05 * (index % 2), z), 0.78, 0.62,
             root, "mint_hi" if index % 3 == 0 else "mint", "triangle",
             0.48 * index, pitch=0.38)
    ground_details(root, 1.48, True)
    return root


def pacific_madrone() -> bpy.types.Object:
    root = new_root("lagoon_tree_pacific_madrone", "Pacific madrone",
                    "Arbutus menziesii", "dry sunny bluff and forest edge")
    tube("madrone_sculptural_trunk",
         [(0, 0, 0.02, 0.82), (-0.38, 0.12, 1.70, 0.70),
          (0.18, -0.18, 3.10, 0.54), (-0.12, 0.04, 4.05, 0.40)],
         root, "madrone", 10)
    root_flare(root, 2.40, 8, "madrone", 0.03)
    # Pale peeling facets wind visibly around the coral trunk.
    for index in range(6):
        angle = index * 1.65
        blob("madrone_peel_%02d" % index,
             (math.cos(angle) * 0.48, math.sin(angle) * 0.35, 0.75 + index * 0.58),
             (0.22, 0.10, 0.48), ("madrone_light",) * 3, root,
             index + 0.7, rings=3, segments=7)
    branches = (
        [(-0.05, 0.02, 3.38, 0.44), (-1.48, 0.40, 4.65, 0.28), (-2.75, 0.70, 5.62, 0.09)],
        [(0.06, 0.00, 3.48, 0.42), (1.50, -0.36, 4.72, 0.27), (2.82, -0.72, 5.72, 0.09)],
        [(0.00, 0.02, 3.76, 0.35), (-0.52, -1.00, 5.00, 0.22), (-0.68, -1.78, 6.32, 0.07)],
        [(0.00, 0.02, 3.82, 0.34), (0.70, 0.98, 5.10, 0.21), (0.98, 1.72, 6.38, 0.07)],
    )
    for index, points in enumerate(branches):
        branch_leaf_run(root, "madrone_branch_%02d" % index, points, "oval",
                        "jade_dark", 0.84, 0.52, 6, index * 1.6,
                        bark_color="madrone", alternate_color="jade", pitch=0.30)
        end = Vector(points[-1][:3])
        for berry_index in range(4):
            angle = index + berry_index * math.tau / 4.0
            berry("madrone_berry_%02d_%02d" % (index, berry_index),
                  (end.x + math.cos(angle) * 0.28,
                   end.y + math.sin(angle) * 0.28, end.z - 0.22),
                  0.12, root, "coral")
    foliage_masses(root, "madrone_glossy_crown", (
        ((-2.55, 0.62, 5.72), (1.22, 0.94, 0.78), -0.28),
        ((-0.72, -1.55, 6.18), (1.25, 0.92, 0.80), 0.46),
        ((-0.52, 0.45, 6.55), (1.34, 1.00, 0.84), -0.12),
        ((1.00, 1.48, 6.28), (1.24, 0.90, 0.80), -0.44),
        ((2.62, -0.58, 5.82), (1.22, 0.94, 0.78), 0.26),
    ), ("jade_dark", "jade", "mint"))
    for index, (x, z) in enumerate((
            (-3.02, 5.62), (-2.06, 6.18), (-1.00, 6.64), (0.05, 6.92),
            (1.12, 6.56), (2.10, 6.20), (3.02, 5.72))):
        for side in (-1, 1):
            leaf("madrone_signature_%02d_%d" % (index, side),
                 (x, side * 0.82, z), 0.78, 0.48, root,
                 "jade" if index % 2 else "jade_dark", "oval",
                 0.50 * index + (math.pi if side > 0 else 0.0), pitch=0.30)
    ground_details(root, 1.85, False)
    return root


def garry_oak() -> bpy.types.Object:
    root = new_root("lagoon_tree_garry_oak", "Garry oak",
                    "Quercus garryana", "dry sunny meadow and woodland")
    tube("oak_heavy_trunk", [(0, 0, 0.02, 1.02), (-0.18, 0.08, 1.85, 0.88),
                              (0.10, -0.04, 2.90, 0.70)], root, "bark_dark", 10)
    root_flare(root, 3.0, 10, "bark", 0.20)
    branches = (
        [(0, 0, 2.18, 0.75), (-1.85, 0.30, 3.25, 0.52), (-3.85, 0.58, 4.20, 0.17)],
        [(0, 0, 2.34, 0.72), (1.92, -0.25, 3.30, 0.50), (4.05, -0.58, 4.18, 0.17)],
        [(-0.05, 0, 2.62, 0.62), (-1.18, -1.25, 3.92, 0.39), (-2.12, -2.12, 5.18, 0.13)],
        [(0.04, 0, 2.68, 0.60), (1.32, 1.18, 3.96, 0.38), (2.30, 2.10, 5.08, 0.13)],
        [(0, 0, 2.78, 0.54), (-0.12, 0.08, 4.38, 0.32), (0.18, 0.12, 6.10, 0.10)],
    )
    for index, points in enumerate(branches):
        branch_leaf_run(root, "oak_branch_%02d" % index, points, "lobed",
                        "jade", 0.82, 0.70, 7, index * 1.3,
                        bark_color="bark_dark", alternate_color="mint", pitch=0.30)
        end = Vector(points[-1][:3])
        for acorn_index in range(2):
            berry("oak_acorn_%02d_%02d" % (index, acorn_index),
                  (end.x + (acorn_index - 0.5) * 0.34, end.y, end.z - 0.38),
                  0.14, root, "butter")
            tube("oak_acorn_stem_%02d_%02d" % (index, acorn_index),
                 [(end.x + (acorn_index - 0.5) * 0.34, end.y, end.z - 0.08, 0.025),
                  (end.x + (acorn_index - 0.5) * 0.34, end.y, end.z - 0.28, 0.018)],
                 root, "bark", 5)
    foliage_masses(root, "oak_open_crown_mass", (
        ((-3.62, 0.50, 4.34), (1.38, 0.98, 0.80), -0.22),
        ((-2.00, -1.52, 5.12), (1.42, 1.05, 0.86), 0.38),
        ((-1.15, 0.58, 5.76), (1.46, 1.08, 0.88), -0.16),
        ((0.22, 0.02, 6.10), (1.38, 1.04, 0.88), 0.08),
        ((1.28, -0.52, 5.72), (1.42, 1.08, 0.88), 0.20),
        ((2.18, 1.48, 5.02), (1.40, 1.02, 0.84), -0.38),
        ((3.78, -0.52, 4.30), (1.36, 0.98, 0.80), 0.22),
    ), ("jade_dark", "jade", "mint"))
    for index, (x, z) in enumerate((
            (-4.12, 4.34), (-3.04, 4.94), (-1.92, 5.56), (-0.72, 6.22),
            (0.52, 6.28), (1.76, 5.58), (2.98, 4.96), (4.12, 4.36))):
        for side in (-1, 1):
            leaf("oak_signature_%02d_%d" % (index, side),
                 (x, side * 0.86, z), 0.82, 0.72, root,
                 "mint" if index % 3 == 0 else "jade", "lobed",
                 0.42 * index + (math.pi if side > 0 else 0.0), pitch=0.32)
    ground_details(root, 2.25, True)
    return root


def pacific_dogwood() -> bpy.types.Object:
    root = new_root("lagoon_tree_pacific_dogwood", "Pacific dogwood",
                    "Cornus nuttallii", "part-shade moist forest edge")
    tube("dogwood_trunk", [(0, 0, 0.02, 0.48), (0.12, -0.04, 2.4, 0.35),
                            (-0.04, 0.0, 4.65, 0.10)], root, "bark", 8)
    root_flare(root, 1.55, 7, "bark", 0.10)
    # Horizontal tiers are the species' architectural cue.
    tier_ends: list[Vector] = []
    for tier in range(4):
        z = 2.0 + tier * 0.74
        radius = 2.85 - tier * 0.32
        for branch_index in range(4):
            angle = tier * 0.34 + branch_index * math.tau / 4.0
            end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                          z + 0.22))
            points = [(0, 0, z, 0.13),
                      (end.x * 0.55, end.y * 0.55, z + 0.08, 0.07), (*end, 0.025)]
            branch_leaf_run(root, "dogwood_tier_%02d_%02d" % (tier, branch_index),
                            points, "oval", "jade", 0.68, 0.46, 4,
                            tier + branch_index, alternate_color="mint", pitch=0.24)
            tier_ends.append(end)
    for index, end in enumerate(tier_ends):
        if index % 2 == 0:
            flower("dogwood_bract_%02d" % index, tuple(end + Vector((0, 0, 0.18))),
                   0.42, root, "white", "butter", petals=4, yaw=index * 0.37)
        else:
            berry("dogwood_fruit_%02d" % index,
                  tuple(end + Vector((0, 0, -0.12))), 0.13, root, "coral")
    foliage_masses(root, "dogwood_layered_mass", (
        ((-2.30, 0.12, 2.32), (1.08, 0.78, 0.44), -0.05),
        ((2.30, -0.12, 2.34), (1.08, 0.78, 0.44), 0.05),
        ((-0.18, -2.05, 3.08), (1.00, 0.76, 0.42), math.pi * 0.5),
        ((0.18, 2.05, 3.10), (1.00, 0.76, 0.42), math.pi * 0.5),
        ((-1.58, 0.10, 3.82), (0.96, 0.72, 0.40), -0.04),
        ((1.58, -0.10, 3.84), (0.96, 0.72, 0.40), 0.04),
        ((-0.12, -1.12, 4.46), (0.84, 0.66, 0.38), math.pi * 0.5),
        ((0.12, 1.12, 4.48), (0.84, 0.66, 0.38), math.pi * 0.5),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 1.28, False)
    return root


def salal() -> bpy.types.Object:
    root = new_root("lagoon_shrub_salal", "Salal", "Gaultheria shallon",
                    "dry-moist part-shade evergreen understory")
    for stem_index in range(7):
        angle = stem_index * math.tau / 7.0 + 0.2
        radius = 1.15 + 0.12 * (stem_index % 3)
        end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                      1.10 + 0.16 * (stem_index % 2)))
        points = [(0, 0, 0.08, 0.11), (end.x * 0.56, end.y * 0.56, 0.58, 0.065),
                  (*end, 0.025)]
        branch_leaf_run(root, "salal_arch_%02d" % stem_index, points, "oval",
                        "jade_dark", 0.58, 0.40, 5, stem_index,
                        alternate_color="jade", pitch=0.30)
        if stem_index % 2 == 0:
            for fruit_index in range(3):
                berry("salal_berry_%02d_%02d" % (stem_index, fruit_index),
                      (end.x + 0.08 * fruit_index, end.y - 0.06 * fruit_index,
                       end.z - 0.15 - fruit_index * 0.15), 0.095, root, "berry")
        else:
            for flower_index in range(2):
                cone("salal_bell_%02d_%02d" % (stem_index, flower_index),
                     (end.x + 0.06 * flower_index, end.y,
                     end.z - 0.16 - flower_index * 0.18), 0.10, root, "white")
    foliage_masses(root, "salal_arching_mass", (
        ((-0.72, 0.28, 0.72), (0.78, 0.58, 0.34), -0.18),
        ((0.70, -0.26, 0.76), (0.80, 0.60, 0.36), 0.18),
        ((-0.12, -0.68, 0.88), (0.72, 0.56, 0.36), 0.35),
        ((0.16, 0.70, 0.92), (0.74, 0.56, 0.36), -0.35),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 0.86, True)
    return root


def low_oregon_grape() -> bpy.types.Object:
    root = new_root("lagoon_shrub_oregon_grape", "Low Oregon grape",
                    "Mahonia nervosa", "dry-moist shaded evergreen understory")
    # Compound leaves radiate like low green feathers from the woody crown.
    for fan_index in range(10):
        angle = fan_index * math.tau / 10.0
        end = Vector((math.cos(angle) * 1.32, math.sin(angle) * 1.32,
                      0.58 + 0.16 * (fan_index % 3)))
        tube("oregon_grape_rachis_%02d" % fan_index,
             [(0, 0, 0.18, 0.065), (*end, 0.025)], root, "bark", 5)
        for leaflet_index in range(4):
            fraction = 0.38 + leaflet_index * 0.16
            point = Vector((0, 0, 0.18)).lerp(end, fraction)
            for side in (-1, 1):
                leaf("oregon_grape_leaf_%02d_%02d_%d" %
                     (fan_index, leaflet_index, side), tuple(point), 0.44, 0.30,
                     root, "jade_dark" if leaflet_index % 2 else "jade", "spiny",
                     angle + side * 0.80, pitch=0.20, roll=side * 0.18)
    for raceme_index in range(3):
        angle = raceme_index * math.tau / 3.0 + 0.4
        x, y = math.cos(angle) * 0.28, math.sin(angle) * 0.28
        tube("oregon_grape_raceme_%02d" % raceme_index,
             [(x, y, 0.30, 0.045), (x, y, 1.32, 0.018)], root, "bark", 5)
        for berry_index in range(5):
            z = 0.82 + berry_index * 0.13
            berry("oregon_grape_gold_%02d_%02d" % (raceme_index, berry_index),
                  (x + math.cos(berry_index * 2.2) * 0.13,
                   y + math.sin(berry_index * 2.2) * 0.13, z), 0.085, root, "butter")
        for fruit_index in range(3):
            berry("oregon_grape_blue_%02d_%02d" % (raceme_index, fruit_index),
                  (x - 0.15 + fruit_index * 0.14, y + 0.10, 0.56 - fruit_index * 0.07),
                  0.10, root, "berry_blue")
    foliage_masses(root, "oregon_grape_low_mass", (
        ((-0.46, 0.18, 0.50), (0.72, 0.58, 0.28), -0.18),
        ((0.48, -0.16, 0.52), (0.72, 0.58, 0.28), 0.18),
        ((0.02, 0.32, 0.66), (0.68, 0.54, 0.26), -0.05),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 0.86, False)
    return root


def red_flowering_currant() -> bpy.types.Object:
    root = new_root("lagoon_shrub_red_flowering_currant", "Red-flowering currant",
                    "Ribes sanguineum", "dry-moist sunny forest edge")
    for stem_index in range(7):
        angle = stem_index * math.tau / 7.0
        end = Vector((math.cos(angle) * (0.72 + 0.13 * (stem_index % 2)),
                      math.sin(angle) * (0.72 + 0.13 * (stem_index % 2)),
                      2.05 + 0.18 * (stem_index % 3)))
        points = [(0, 0, 0.05, 0.105), (end.x * 0.42, end.y * 0.42, 0.95, 0.065),
                  (*end, 0.025)]
        branch_leaf_run(root, "currant_stem_%02d" % stem_index, points, "palmate",
                        "jade", 0.54, 0.48, 4, stem_index,
                        alternate_color="mint", pitch=0.32)
        # Saturated hanging flower chains stay readable from the game camera.
        for chain_index in range(2):
            cx = end.x + (chain_index - 0.5) * 0.25
            cy = end.y
            tube("currant_chain_%02d_%02d" % (stem_index, chain_index),
                 [(cx, cy, end.z - 0.05, 0.022), (cx, cy, end.z - 0.80, 0.012)],
                 root, "bark", 5)
            for bloom_index in range(4):
                berry("currant_bloom_%02d_%02d_%02d" %
                      (stem_index, chain_index, bloom_index),
                      (cx + 0.07 * (-1 if bloom_index % 2 else 1), cy,
                      end.z - 0.18 - bloom_index * 0.18), 0.11, root, "coral")
    foliage_masses(root, "currant_airborne_mass", (
        ((-0.58, 0.24, 0.92), (0.68, 0.58, 0.46), -0.15),
        ((0.62, -0.22, 1.04), (0.70, 0.58, 0.48), 0.18),
        ((-0.52, -0.34, 1.56), (0.66, 0.56, 0.48), 0.24),
        ((0.48, 0.34, 1.68), (0.66, 0.56, 0.48), -0.24),
        ((0.02, 0.02, 2.08), (0.62, 0.52, 0.44), 0.04),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 0.72, False)
    return root


def oceanspray() -> bpy.types.Object:
    root = new_root("lagoon_shrub_oceanspray", "Oceanspray",
                    "Holodiscus discolor", "dry-moist sunny or shaded slope")
    for stem_index in range(9):
        angle = stem_index * math.tau / 9.0 + 0.1
        radius = 1.05 + 0.12 * (stem_index % 3)
        end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                      2.15 + 0.15 * (stem_index % 2)))
        points = [(0, 0, 0.05, 0.10), (end.x * 0.38, end.y * 0.38, 1.10, 0.06),
                  (*end, 0.022)]
        branch_leaf_run(root, "oceanspray_fountain_%02d" % stem_index,
                        points, "oval", "jade", 0.45, 0.28, 4, stem_index,
                        alternate_color="mint", pitch=0.26)
        # Cream plumes arc outward from each fountain cane.
        plume_tip = end + Vector((math.cos(angle) * 0.62,
                                  math.sin(angle) * 0.62, -0.36))
        tube("oceanspray_plume_stem_%02d" % stem_index,
             [(*end, 0.025), (*plume_tip, 0.010)], root, "bark_light", 5)
        for bloom_index in range(6):
            fraction = bloom_index / 5.0
            point = end.lerp(plume_tip, fraction)
            for side in (-1, 1):
                berry("oceanspray_bloom_%02d_%02d_%d" %
                      (stem_index, bloom_index, side),
                      (point.x + side * 0.09, point.y, point.z + 0.05 * side),
                      0.075, root, "cream")
    foliage_masses(root, "oceanspray_fountain_mass", (
        ((-0.66, 0.22, 0.86), (0.70, 0.58, 0.40), -0.15),
        ((0.68, -0.18, 0.92), (0.72, 0.58, 0.42), 0.17),
        ((-0.56, -0.34, 1.46), (0.66, 0.56, 0.40), 0.25),
        ((0.54, 0.34, 1.54), (0.66, 0.56, 0.40), -0.25),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 0.76, False)
    return root


def salmonberry() -> bpy.types.Object:
    root = new_root("lagoon_shrub_salmonberry", "Salmonberry",
                    "Rubus spectabilis", "moist-wet bank and thicket")
    cane_ends: list[Vector] = []
    for cane_index in range(7):
        angle = cane_index * math.tau / 7.0 + 0.26
        radius = 1.25 + 0.13 * (cane_index % 2)
        end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                      1.12 + 0.15 * (cane_index % 3)))
        points = [(0, 0, 0.05, 0.09),
                  (math.cos(angle) * radius * 0.52,
                   math.sin(angle) * radius * 0.52, 1.62, 0.055), (*end, 0.022)]
        branch_leaf_run(root, "salmonberry_cane_%02d" % cane_index,
                        points, "palmate", "jade", 0.55, 0.50, 4, cane_index,
                        alternate_color="mint", pitch=0.32)
        cane_ends.append(end)
    for index, end in enumerate(cane_ends):
        flower("salmonberry_flower_%02d" % index,
               tuple(end + Vector((0, 0, 0.18))), 0.25, root,
               "coral", "butter", 5, index * 0.7)
        # Four-lobed berry clusters read as raspberry fruit without textures.
        for lobe in range(4):
            angle = lobe * math.tau / 4.0
            berry("salmonberry_fruit_%02d_%02d" % (index, lobe),
                  (end.x + math.cos(angle) * 0.09,
                   end.y + math.sin(angle) * 0.09, end.z - 0.24),
                  0.105, root, "salmon")
    foliage_masses(root, "salmonberry_thicket_mass", (
        ((-0.72, 0.25, 0.72), (0.80, 0.64, 0.38), -0.16),
        ((0.74, -0.22, 0.76), (0.82, 0.64, 0.40), 0.18),
        ((-0.30, -0.62, 1.16), (0.74, 0.60, 0.40), 0.30),
        ((0.32, 0.64, 1.20), (0.74, 0.60, 0.40), -0.30),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 0.82, False)
    return root


def evergreen_huckleberry() -> bpy.types.Object:
    root = new_root("lagoon_shrub_evergreen_huckleberry", "Evergreen huckleberry",
                    "Vaccinium ovatum", "dry-moist part-shade evergreen understory")
    for stem_index in range(11):
        angle = stem_index * 2.399
        radius = 0.48 + 0.035 * stem_index
        end = Vector((math.cos(angle) * radius, math.sin(angle) * radius,
                      1.65 + 0.10 * (stem_index % 4)))
        points = [(0, 0, 0.05, 0.075), (end.x * 0.55, end.y * 0.55, 0.92, 0.042),
                  (*end, 0.018)]
        branch_leaf_run(root, "huckleberry_stem_%02d" % stem_index,
                        points, "oval", "jade_dark", 0.36, 0.20, 5,
                        stem_index, alternate_color="jade", pitch=0.30)
        for fruit_index in range(2):
            berry("huckleberry_fruit_%02d_%02d" % (stem_index, fruit_index),
                  (end.x + (fruit_index - 0.5) * 0.17, end.y,
                   end.z - 0.16 - fruit_index * 0.15),
                  0.09, root, "berry_blue")
        if stem_index % 3 == 0:
            cone("huckleberry_bell_%02d" % stem_index,
                 (end.x - 0.13, end.y, end.z - 0.10), 0.085, root, "white")
    foliage_masses(root, "huckleberry_dense_mass", (
        ((-0.34, 0.16, 0.62), (0.62, 0.54, 0.48), -0.12),
        ((0.36, -0.14, 0.72), (0.64, 0.54, 0.50), 0.12),
        ((-0.30, -0.18, 1.16), (0.60, 0.52, 0.50), 0.18),
        ((0.32, 0.20, 1.30), (0.60, 0.52, 0.50), -0.18),
        ((0.00, 0.00, 1.70), (0.56, 0.48, 0.46), 0.02),
    ), ("jade_dark", "jade", "mint"))
    ground_details(root, 0.70, True)
    return root


BUILDERS = {
    "lagoon_tree_douglas_fir": douglas_fir,
    "lagoon_tree_western_redcedar": western_redcedar,
    "lagoon_tree_western_hemlock": western_hemlock,
    "lagoon_tree_sitka_spruce": sitka_spruce,
    "lagoon_tree_shore_pine": shore_pine,
    "lagoon_tree_pacific_yew": pacific_yew,
    "lagoon_tree_bigleaf_maple": bigleaf_maple,
    "lagoon_tree_red_alder": red_alder,
    "lagoon_tree_black_cottonwood": black_cottonwood,
    "lagoon_tree_pacific_madrone": pacific_madrone,
    "lagoon_tree_garry_oak": garry_oak,
    "lagoon_tree_pacific_dogwood": pacific_dogwood,
    "lagoon_shrub_salal": salal,
    "lagoon_shrub_oregon_grape": low_oregon_grape,
    "lagoon_shrub_red_flowering_currant": red_flowering_currant,
    "lagoon_shrub_oceanspray": oceanspray,
    "lagoon_shrub_salmonberry": salmonberry,
    "lagoon_shrub_evergreen_huckleberry": evergreen_huckleberry,
}


def descendants(obj: bpy.types.Object) -> list[bpy.types.Object]:
    result = [obj]
    for child in obj.children:
        result.extend(descendants(child))
    return result


def export_asset(name: str, root: bpy.types.Object) -> tuple[int, int, Vector]:
    bpy.ops.object.select_all(action="DESELECT")
    copies: list[bpy.types.Object] = []
    for source in descendants(root):
        if source.type != "MESH":
            continue
        copy = source.copy()
        copy.data = source.data.copy()
        bpy.context.collection.objects.link(copy)
        copy.parent = None
        copy.matrix_world = source.matrix_world.copy()
        copies.append(copy)
    if not copies:
        raise RuntimeError("No mesh descendants for " + name)
    for copy in copies:
        copy.select_set(True)
    bpy.context.view_layer.objects.active = copies[0]
    bpy.ops.object.join()
    merged = bpy.context.active_object
    merged.name = name
    for key in ("role", "species_common", "species_latin", "habitat", "style_gate"):
        merged[key] = root[key]
    old_materials = list(merged.data.materials)
    unique_materials: list[bpy.types.Material] = []
    remap: dict[int, int] = {}
    for old_index, old_material in enumerate(old_materials):
        if old_material not in unique_materials:
            unique_materials.append(old_material)
        remap[old_index] = unique_materials.index(old_material)
    polygon_materials = [remap[polygon.material_index] for polygon in merged.data.polygons]
    merged.data.materials.clear()
    for unique_material in unique_materials:
        merged.data.materials.append(unique_material)
    for polygon, new_index in zip(merged.data.polygons, polygon_materials):
        polygon.material_index = new_index
    merged.data.validate(clean_customdata=True)
    merged.data.calc_loop_triangles()
    triangles = len(merged.data.loop_triangles)
    material_count = len(merged.data.materials)
    minimum = Vector((1.0e9, 1.0e9, 1.0e9))
    maximum = Vector((-1.0e9, -1.0e9, -1.0e9))
    for vertex in merged.data.vertices:
        for axis in range(3):
            minimum[axis] = min(minimum[axis], vertex.co[axis])
            maximum[axis] = max(maximum[axis], vertex.co[axis])
    size = maximum - minimum
    bpy.ops.export_scene.gltf(filepath=str(OUT / (name + ".glb")), export_format="GLB",
                              export_yup=True, use_selection=True, export_apply=True,
                              export_materials="EXPORT", export_animations=False,
                              export_cameras=False, export_lights=False,
                              export_extras=True)
    bpy.data.objects.remove(merged, do_unlink=True)
    return triangles, material_count, size


ASSETS = {name: builder() for name, builder in BUILDERS.items()}
for asset_name, asset in ASSETS.items():
    triangle_count, asset_material_count, dimensions = export_asset(asset_name, asset)
    print("SKY_PNW_WOODY|%s|triangles=%d|materials=%d|size=%.3fx%.3fx%.3f" %
          (asset_name, triangle_count, asset_material_count,
           dimensions.x, dimensions.y, dimensions.z))

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
print("SKY_PNW_WOODY|assets|%d" % len(ASSETS))
print("SKY_PNW_WOODY|blend|%s" % BLEND)
