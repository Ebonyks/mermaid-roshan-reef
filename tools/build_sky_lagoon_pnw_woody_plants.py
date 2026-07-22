#!/usr/bin/env python3
"""Build the Seattle/PNW woody-plant family for Sky Lagoon (GEN2).

GEN2 rebuilds every species to the accepted flat-prototype grammar
(`SKY_LAGOON_PNW_FLAT_PROTOTYPE_AUDIT_2026-07-21.md`): each plant is a
single readable silhouette made of two to five primary volumes — stacked
scalloped skirt tiers for conifers, big rounded crown clouds for
broadleaves — with one or two oversized botanical ornaments (samaras,
catkins, acorns, tassels, plumes, berries) and a compact planted base.
No branch scaffolds, no leaf-level geometry, no dark-on-top shading.

The runtime roster is the full 24-card set: twelve trees plus six shrub
species in two structurally distinct A/B variants each.  Trailing
blackberry replaces the superseded evergreen huckleberry.

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

STYLE_GATE = "sky_lagoon_pnw_woody_gen2"

# Lightened, card-matched palette: crowns keep clear value steps
# (highlight top, mid body, aqua-lavender shadow underside).
PALETTE = {
    "bark_dark": (0.22, 0.12, 0.16, 1.0),
    "bark": (0.38, 0.22, 0.15, 1.0),
    "bark_light": (0.58, 0.38, 0.25, 1.0),
    "alder_bark": (0.76, 0.74, 0.66, 1.0),
    "madrone": (0.78, 0.32, 0.24, 1.0),
    "madrone_light": (0.94, 0.60, 0.40, 1.0),
    "moss": (0.44, 0.66, 0.38, 1.0),
    "jade_dark": (0.12, 0.33, 0.30, 1.0),
    "jade": (0.22, 0.50, 0.40, 1.0),
    "mint": (0.40, 0.70, 0.50, 1.0),
    "mint_hi": (0.56, 0.84, 0.60, 1.0),
    "sage": (0.48, 0.72, 0.50, 1.0),
    "sage_hi": (0.64, 0.84, 0.60, 1.0),
    "teal": (0.25, 0.55, 0.52, 1.0),
    "teal_deep": (0.15, 0.40, 0.42, 1.0),
    "teal_hi": (0.42, 0.72, 0.64, 1.0),
    "aqua_shadow": (0.26, 0.40, 0.56, 1.0),
    "lavender": (0.56, 0.44, 0.72, 1.0),
    "coral": (0.90, 0.36, 0.40, 1.0),
    "salmon": (0.98, 0.52, 0.34, 1.0),
    "magenta": (0.84, 0.26, 0.52, 1.0),
    "berry": (0.22, 0.16, 0.38, 1.0),
    "berry_blue": (0.34, 0.40, 0.68, 1.0),
    "butter": (0.96, 0.72, 0.26, 1.0),
    "olive_gold": (0.72, 0.64, 0.26, 1.0),
    "cream": (0.98, 0.90, 0.68, 1.0),
    "white": (0.94, 0.95, 0.90, 1.0),
    "stone": (0.48, 0.60, 0.64, 1.0),
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
    root["style_gate"] = STYLE_GATE
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


def cloud(name: str, center: tuple[float, float, float],
          scale: tuple[float, float, float], colors: tuple[str, str, str],
          parent: bpy.types.Object, seed: float, rings: int = 5,
          segments: int = 10, rotation: float = 0.0,
          lobe_amp: float = 0.16, lobe_count: float = 3.0) -> bpy.types.Object:
    """One big rounded crown mass with visible soft lobes.

    colors are (top highlight, mid body, underside shadow).
    """
    vertices: list[tuple[float, float, float]] = []
    for ring in range(rings):
        fraction = ring / max(rings - 1, 1)
        latitude = math.pi * fraction
        radial = max(0.22, math.sin(latitude) ** 0.82)
        vertical = math.cos(latitude)
        for segment in range(segments):
            angle = math.tau * segment / segments
            lobes = 1.0 + lobe_amp * math.sin(angle * lobe_count + seed) \
                * math.sin(latitude)
            local_x = math.cos(angle) * scale[0] * radial * lobes
            local_y = math.sin(angle) * scale[1] * radial * \
                (1.0 + lobe_amp * 0.5 * math.cos(angle * (lobe_count + 1.0) - seed))
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
            # Highlight only crowns the top ring; the mid body color
            # dominates so masses keep a clear value identity.
            indices.append(0 if ring == 0 else (2 if ring >= rings - 2 else 1))
    faces.append(tuple(reversed(range(segments))))
    indices.append(0)
    last = (rings - 1) * segments
    faces.append(tuple(last + segment for segment in range(segments)))
    indices.append(2)
    return mesh_object(name, vertices, faces, colors, parent, indices)


def skirt_tier(name: str, z: float, radius: float, height: float,
               droop: float, parent: bpy.types.Object, seed: float,
               colors: tuple[str, str, str] = ("sage_hi", "sage", "jade"),
               lobes: int = 7, segments: int = 14,
               offset: tuple[float, float] = (0.0, 0.0),
               squash: float = 1.0) -> bpy.types.Object:
    """One large scalloped conifer skirt: dome top, lobed drooping rim,
    closed shadow underside.  This is the card language for every conifer —
    a handful of these stacked make the whole crown."""
    ring_spec = (
        (0.16, height, 0),          # inner dome highlight
        (0.56, height * 0.55, 1),   # dome shoulder
        (0.88, height * 0.14, 1),   # outer slope
        (1.00, -droop, 1),          # scalloped rim
        (0.66, -droop * 0.62, 2),   # underside return
        (0.16, -droop * 0.24, 2),   # underside center
    )
    vertices: list[tuple[float, float, float]] = []
    for fraction, dz, _band in ring_spec:
        for segment in range(segments):
            angle = math.tau * segment / segments
            scallop = 1.0 + 0.11 * (fraction ** 2.0) * \
                math.sin(angle * lobes + seed)
            r = radius * fraction * scallop
            drop = dz - (0.14 * droop * (fraction ** 2.0) *
                         (0.5 + 0.5 * math.cos(angle * lobes + seed)))
            vertices.append((offset[0] + math.cos(angle) * r,
                             offset[1] + math.sin(angle) * r * squash,
                             z + drop))
    faces: list[tuple[int, ...]] = []
    indices: list[int] = []
    bands = [band for _f, _dz, band in ring_spec]
    for ring in range(len(ring_spec) - 1):
        for segment in range(segments):
            nxt = (segment + 1) % segments
            faces.append((ring * segments + segment, ring * segments + nxt,
                          (ring + 1) * segments + nxt,
                          (ring + 1) * segments + segment))
            indices.append(bands[ring])
    faces.append(tuple(reversed(range(segments))))
    indices.append(0)
    last = (len(ring_spec) - 1) * segments
    faces.append(tuple(last + segment for segment in range(segments)))
    indices.append(2)
    return mesh_object(name, vertices, faces, colors, parent, indices)


def berry(name: str, position: tuple[float, float, float], radius: float,
          parent: bpy.types.Object, color: str) -> None:
    cloud(name, position, (radius, radius, radius), (color, color, color),
          parent, sum(position), rings=3, segments=7, lobe_amp=0.0)


def bell(name: str, position: tuple[float, float, float], radius: float,
         parent: bpy.types.Object, color: str = "cream") -> None:
    cloud(name, position, (radius * 0.72, radius * 0.72, radius),
          (color, color, color), parent, sum(position), rings=3, segments=7,
          lobe_amp=0.0)


def flower(name: str, position: tuple[float, float, float], radius: float,
           parent: bpy.types.Object, petal: str, center_color: str = "butter",
           petals: int = 5, yaw: float = 0.0) -> None:
    for index in range(petals):
        angle = yaw + math.tau * index / petals
        cloud(name + "_petal_%02d" % index,
              (position[0] + math.cos(angle) * radius * 0.70,
               position[1] + math.sin(angle) * radius * 0.70,
               position[2]),
              (radius * 0.60, radius * 0.60, radius * 0.30),
              (petal, petal, petal), parent, index * 1.3, rings=3,
              segments=7, lobe_amp=0.0)
    berry(name + "_center", (position[0], position[1], position[2] + radius * 0.24),
          radius * 0.38, parent, center_color)


def catkin(name: str, top: tuple[float, float, float], length: float,
           parent: bpy.types.Object, color: str, beads: int = 4,
           bead_radius: float = 0.10, stem_color: str = "bark") -> None:
    """Oversized hanging catkin/seed string — a single readable ornament."""
    tube(name + "_stem", [(top[0], top[1], top[2] + 0.10, 0.022),
                          (top[0], top[1], top[2] - length * 0.2, 0.016)],
         parent, stem_color, 5)
    for index in range(beads):
        fraction = (index + 1) / beads
        berry(name + "_bead_%02d" % index,
              (top[0] + 0.03 * math.sin(index * 2.1),
               top[1] + 0.03 * math.cos(index * 1.7),
               top[2] - fraction * length),
              bead_radius * (1.0 - 0.16 * fraction), parent, color)


def samara(name: str, top: tuple[float, float, float],
           parent: bpy.types.Object, yaw: float, size: float = 0.5) -> None:
    """Bigleaf-maple paired double samara: olive-gold seed bases and two
    long warm-tan wings forming a clear V.  Never a leaf badge."""
    tube(name + "_stem", [(top[0], top[1], top[2] + 0.16, 0.02),
                          (top[0], top[1], top[2], 0.015)], parent, "bark", 5)
    for side in (-1.0, 1.0):
        wing_yaw = yaw + side * 0.52
        tip = (top[0] + math.sin(wing_yaw) * size,
               top[1] + math.cos(wing_yaw) * size,
               top[2] - size * 0.85)
        mid = (top[0] + math.sin(wing_yaw) * size * 0.5,
               top[1] + math.cos(wing_yaw) * size * 0.5,
               top[2] - size * 0.38)
        cloud(name + "_wing_%d" % side,
              ((top[0] + tip[0]) * 0.5, (top[1] + tip[1]) * 0.5,
               (top[2] + tip[2]) * 0.5),
              (size * 0.16 + abs(mid[0] - top[0]) * 0.4,
               size * 0.16 + abs(mid[1] - top[1]) * 0.4, size * 0.5),
              ("bark_light", "bark_light", "bark_light"), parent,
              side * 2.0, rings=3, segments=7, lobe_amp=0.0)
        berry(name + "_seed_%d" % side,
              (top[0] + math.sin(wing_yaw) * size * 0.16,
               top[1] + math.cos(wing_yaw) * size * 0.16,
               top[2] - size * 0.12), size * 0.15, parent, "olive_gold")


def acorn(name: str, position: tuple[float, float, float], scale: float,
          parent: bpy.types.Object) -> None:
    tube(name + "_stem", [(position[0], position[1], position[2] + scale * 2.2, 0.02),
                          (position[0], position[1], position[2] + scale * 0.8, 0.015)],
         parent, "bark", 5)
    berry(name + "_nut", position, scale, parent, "butter")
    cloud(name + "_cap", (position[0], position[1], position[2] + scale * 0.62),
          (scale * 0.92, scale * 0.92, scale * 0.5),
          ("bark", "bark", "bark"), parent, 1.0, rings=3, segments=7,
          lobe_amp=0.0)


def tassel(name: str, top: tuple[float, float, float], length: float,
           parent: bpy.types.Object, color: str = "coral",
           beads: int = 5) -> None:
    tube(name + "_stem", [(top[0], top[1], top[2] + 0.08, 0.02),
                          (top[0], top[1], top[2] - length * 0.15, 0.014)],
         parent, "bark", 5)
    for index in range(beads):
        fraction = (index + 1) / beads
        berry(name + "_bead_%02d" % index,
              (top[0] + 0.05 * math.sin(index * 2.4),
               top[1] + 0.04 * math.cos(index * 1.9),
               top[2] - fraction * length),
              0.11 * (1.0 + 0.22 * fraction), parent, color)


def plume(name: str, base: tuple[float, float, float], yaw: float,
          length: float, rise: float, parent: bpy.types.Object,
          color: str = "cream") -> None:
    """One chunky blossom plume: overlapping pods along a soft arc."""
    for index in range(4):
        fraction = 0.16 + index * 0.24
        droop = rise * (1.0 - (fraction - 0.5) ** 2 * 2.4)
        size = 0.15 + 0.035 * index
        cloud(name + "_pod_%02d" % index,
              (base[0] + math.sin(yaw) * length * fraction,
               base[1] + math.cos(yaw) * length * fraction,
               base[2] + droop),
              (size, size, size * 1.25),
              (color, color, color), parent, index * 1.6, rings=3,
              segments=7, lobe_amp=0.0)


def raceme(name: str, base: tuple[float, float, float], height: float,
           parent: bpy.types.Object, color: str = "butter",
           lean: float = 0.0) -> None:
    top = (base[0] + math.sin(lean) * height * 0.4, base[1],
           base[2] + height)
    tube(name + "_stalk", [(base[0], base[1], base[2], 0.03),
                           (top[0], top[1], top[2], 0.018)], parent, "bark", 5)
    for index in range(5):
        fraction = 0.35 + index * 0.16
        berry(name + "_bead_%02d" % index,
              (base[0] + (top[0] - base[0]) * fraction,
               base[1] + (top[1] - base[1]) * fraction,
               base[2] + (top[2] - base[2]) * fraction),
              0.10 * (1.0 - 0.1 * index) + 0.02, parent, color)


def berry_cluster(name: str, center: tuple[float, float, float],
                  parent: bpy.types.Object, color: str = "berry",
                  count: int = 4, radius: float = 0.10) -> None:
    for index in range(count):
        angle = index * math.tau / count + center[2]
        berry(name + "_%02d" % index,
              (center[0] + math.cos(angle) * radius * 0.9,
               center[1] + math.sin(angle) * radius * 0.9,
               center[2] + (0.06 if index % 2 else -0.05)),
              radius, parent, color)


def spear_leaf(name: str, base: tuple[float, float, float], yaw: float,
               length: float, width: float, parent: bpy.types.Object,
               color: str, pitch: float = 0.22) -> None:
    """One oversized pointed Oregon-grape leaf: a single elongated volume
    anchored at the crown so it can never read as a floating slab."""
    for step, (fraction, width_scale) in enumerate(((0.26, 1.0), (0.56, 0.74),
                                                    (0.84, 0.42))):
        center = (base[0] + math.sin(yaw) * length * fraction * math.cos(pitch),
                  base[1] + math.cos(yaw) * length * fraction * math.cos(pitch),
                  base[2] + length * fraction * math.sin(pitch))
        cloud(name + "_seg_%02d" % step, center,
              (length * 0.15 + width * 0.30 * width_scale,
               length * 0.15 + width * 0.30 * width_scale,
               width * 0.44 * width_scale),
              (color, color, color), parent, yaw + step, rings=3,
              segments=7, lobe_amp=0.0)


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


def ground_details(parent: bpy.types.Object, radius: float,
                   mossy: bool = False, tuft_color: str = "moss") -> None:
    # Stones stay a single material and tufts reuse an existing crown slot
    # where needed, keeping every asset within the 8-material Mobile gate.
    for index in range(4):
        angle = 0.45 + index * math.tau / 4.0
        size = 0.14 + 0.04 * (index % 3)
        cloud("ground_stone_%02d" % index,
              (math.cos(angle) * radius, math.sin(angle) * radius * 0.72, 0.09),
              (size * 1.35, size, size * 0.58), ("stone",) * 3,
              parent, index + radius, rings=3, segments=7, lobe_amp=0.0)
    for index in range(3):
        angle = 1.35 + index * math.tau / 3.0
        cloud("ground_tuft_%02d" % index,
              (math.cos(angle) * radius * 0.86,
               math.sin(angle) * radius * 0.62, 0.10),
              (0.16, 0.16, 0.20), (tuft_color,) * 3, parent,
              index * 2.2, rings=3, segments=7, lobe_amp=0.0)


def bark_dashes(parent: bpy.types.Object, prefix: str, trunk_x: float,
                trunk_y: float, radius: float, heights: tuple[float, ...],
                seed: float = 0.0) -> None:
    """Short dark horizontal dashes for pale birch-like alder bark."""
    for index, z in enumerate(heights):
        angle = seed + index * 2.4
        cloud(prefix + "_dash_%02d" % index,
              (trunk_x + math.cos(angle) * radius * 0.92,
               trunk_y + math.sin(angle) * radius * 0.55, z),
              (radius * 0.42, radius * 0.16, 0.09),
              ("bark_dark", "bark_dark", "bark_dark"), parent,
              index * 1.1, rings=3, segments=7, lobe_amp=0.0)


# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------


def douglas_fir() -> bpy.types.Object:
    root = new_root("lagoon_tree_douglas_fir", "Coastal Douglas-fir",
                    "Pseudotsuga menziesii", "dry-moist meadow forest")
    tube("fir_trunk", [(0, 0, 0.02, 0.66), (0.05, -0.03, 2.2, 0.50),
                       (-0.05, 0.02, 5.0, 0.30), (0.0, 0.0, 9.6, 0.05)],
         root, "bark", 9)
    root_flare(root, 1.9, 8, "bark_light", 0.18)
    # Seven stacked scalloped skirts, pale mint over sage over jade.
    tiers = ((1.65, 3.30, 1.05, 0.62), (2.55, 2.95, 0.95, 0.58),
             (3.50, 2.55, 0.90, 0.52), (4.45, 2.15, 0.85, 0.48),
             (5.40, 1.75, 0.80, 0.44), (6.35, 1.35, 0.75, 0.38),
             (7.30, 0.98, 0.72, 0.32))
    for index, (z, radius, height, droop) in enumerate(tiers):
        skirt_tier("fir_skirt_%02d" % index, z, radius, height, droop, root,
                   index * 1.7, ("sage_hi", "sage", "jade"), lobes=7)
    cloud("fir_tip", (0.0, 0.0, 8.55), (0.62, 0.62, 1.05),
          ("sage_hi", "sage", "jade"), root, 4.2, lobe_amp=0.10)
    # A few oversized hanging cones tucked under the skirt rims are the cue.
    for index, (tier_z, tier_radius) in enumerate(((2.55, 2.95), (4.45, 2.15),
                                                   (6.35, 1.35))):
        angle = 0.6 + index * 2.1
        catkin("fir_cone_%02d" % index,
               (math.cos(angle) * tier_radius * 0.72,
                math.sin(angle) * tier_radius * 0.72, tier_z - 0.72),
               0.62, root, "bark_light", beads=3, bead_radius=0.20)
    ground_details(root, 1.55, True)
    return root


def western_redcedar() -> bpy.types.Object:
    root = new_root("lagoon_tree_western_redcedar", "Western redcedar",
                    "Thuja plicata", "moist-wet forest edge")
    # Broad fluted base narrowing fast; wide drooping curtain skirts.
    tube("cedar_trunk", [(0, 0, 0.02, 0.95), (-0.06, 0.02, 1.9, 0.62),
                         (0.05, 0.0, 4.6, 0.34), (-0.08, 0.04, 9.0, 0.06)],
         root, "bark", 10)
    root_flare(root, 2.6, 10, "bark_light", 0.05)
    tiers = ((1.55, 3.75, 0.95, 1.05), (2.70, 3.35, 0.90, 0.98),
             (3.85, 2.90, 0.85, 0.90), (5.00, 2.45, 0.82, 0.82),
             (6.15, 1.95, 0.78, 0.72), (7.25, 1.45, 0.74, 0.60))
    for index, (z, radius, height, droop) in enumerate(tiers):
        skirt_tier("cedar_curtain_%02d" % index, z, radius, height, droop,
                   root, 0.9 + index * 1.4, ("teal_hi", "teal", "jade_dark"),
                   lobes=8)
    # Bent leader tip.
    cloud("cedar_tip", (0.30, 0.06, 8.35), (0.55, 0.55, 0.92),
          ("teal_hi", "teal", "jade_dark"), root, 2.8, lobe_amp=0.10)
    tube("cedar_tip_bend", [(0.0, 0.0, 7.7, 0.10), (0.22, 0.05, 8.15, 0.06),
                            (0.52, 0.10, 8.42, 0.03)], root, "bark", 6)
    ground_details(root, 2.05, True)
    return root


def western_hemlock() -> bpy.types.Object:
    root = new_root("lagoon_tree_western_hemlock", "Western hemlock",
                    "Tsuga heterophylla", "cool moist part-shade forest")
    tube("hemlock_trunk", [(0, 0, 0.02, 0.52), (0.04, 0.0, 3.4, 0.32),
                           (-0.05, 0.02, 7.0, 0.14), (0.05, 0.02, 8.9, 0.05)],
         root, "bark_dark", 8)
    root_flare(root, 1.6, 7, "bark", 0.28)
    # Narrow feathered tiers with deeper rim droop.
    tiers = ((1.85, 2.45, 0.72, 0.72), (2.90, 2.15, 0.68, 0.68),
             (3.95, 1.85, 0.66, 0.62), (5.00, 1.55, 0.62, 0.56),
             (6.05, 1.25, 0.58, 0.50), (7.05, 0.95, 0.55, 0.42))
    for index, (z, radius, height, droop) in enumerate(tiers):
        skirt_tier("hemlock_feather_%02d" % index, z, radius, height, droop,
                   root, 2.2 + index * 1.9, ("mint_hi", "mint", "aqua_shadow"),
                   lobes=9)
    # Unmistakably bowed drooping leader; foliage wraps the bowed tube so
    # nothing reads as a detached saucer.
    cloud("hemlock_top", (0.0, 0.0, 8.15), (0.72, 0.72, 0.62),
          ("mint_hi", "mint", "aqua_shadow"), root, 2.9, lobe_amp=0.12)
    tube("hemlock_leader", [(0.0, 0.0, 8.3, 0.09), (0.16, 0.02, 9.05, 0.055),
                            (0.62, 0.06, 9.42, 0.03),
                            (1.02, 0.10, 9.18, 0.018)], root, "bark_dark", 6)
    cloud("hemlock_leader_pad", (0.50, 0.05, 9.18), (0.52, 0.40, 0.34),
          ("mint_hi", "mint", "aqua_shadow"), root, 3.7, lobe_amp=0.12,
          rotation=0.45)
    cloud("hemlock_leader_tip", (0.98, 0.10, 9.06), (0.32, 0.26, 0.24),
          ("mint_hi", "mint", "aqua_shadow"), root, 5.1, lobe_amp=0.0,
          rings=3, segments=7)
    ground_details(root, 1.35, True)
    return root


def sitka_spruce() -> bpy.types.Object:
    root = new_root("lagoon_tree_sitka_spruce", "Sitka spruce",
                    "Picea sitchensis", "wet coastal forest")
    tube("spruce_trunk", [(0, 0, 0.02, 0.72), (-0.04, 0.03, 2.4, 0.50),
                          (0.04, -0.02, 5.4, 0.26), (0, 0, 8.6, 0.05)],
         root, "bark_dark", 9)
    root_flare(root, 2.1, 8, "bark", 0.36)
    # Dense broad blue-teal cone: bumpier, closer-packed skirts.
    tiers = ((1.35, 3.60, 0.92, 0.55), (2.20, 3.30, 0.88, 0.52),
             (3.05, 2.95, 0.85, 0.50), (3.90, 2.60, 0.82, 0.46),
             (4.75, 2.20, 0.78, 0.42), (5.60, 1.80, 0.74, 0.38),
             (6.45, 1.40, 0.70, 0.34), (7.30, 1.02, 0.66, 0.28))
    for index, (z, radius, height, droop) in enumerate(tiers):
        skirt_tier("spruce_skirt_%02d" % index, z, radius, height, droop,
                   root, 1.3 + index * 2.3, ("teal_hi", "teal_deep", "aqua_shadow"),
                   lobes=10)
    cloud("spruce_tip", (0.0, 0.0, 8.30), (0.55, 0.55, 0.95),
          ("teal_hi", "teal_deep", "aqua_shadow"), root, 6.4, lobe_amp=0.12)
    ground_details(root, 1.65, False)
    return root


def shore_pine() -> bpy.types.Object:
    root = new_root("lagoon_tree_shore_pine", "Shore pine",
                    "Pinus contorta var. contorta",
                    "dry windy shore and bog edge")
    # Crooked wind-pruned S trunk with three offset umbrella pads.
    tube("shore_pine_trunk",
         [(0, 0, 0.02, 0.58), (-0.65, 0.12, 1.7, 0.44),
          (-0.10, -0.10, 3.3, 0.32), (-0.90, 0.06, 4.9, 0.20),
          (-0.45, 0.0, 6.1, 0.09)], root, "bark", 9)
    tube("shore_pine_limb", [(-0.35, -0.02, 3.4, 0.20),
                             (1.15, -0.30, 4.05, 0.13),
                             (2.15, -0.42, 4.30, 0.05)], root, "bark_dark", 7)
    root_flare(root, 1.9, 7, "bark_light", 0.12)
    pads = (((2.10, -0.40, 4.70), (1.70, 1.20, 0.46), 3.1),
            ((-1.20, 0.15, 5.50), (2.05, 1.45, 0.52), 1.2),
            ((-0.30, -0.05, 6.50), (1.45, 1.05, 0.46), 5.3))
    for index, (center, scale, seed) in enumerate(pads):
        cloud("shore_pine_pad_%02d" % index, center, scale,
              ("sage_hi", "jade", "jade_dark"), root, seed, lobe_amp=0.20,
              lobe_count=4.0)
    for index in range(2):
        catkin("shore_pine_cone_%02d" % index,
               (1.45 - 2.75 * index, -0.35 + 0.30 * index, 4.52 + 0.80 * index),
               0.42, root, "bark_light", beads=2, bead_radius=0.19)
    ground_details(root, 1.55, False)
    return root


def pacific_yew() -> bpy.types.Object:
    root = new_root("lagoon_tree_pacific_yew", "Pacific yew",
                    "Taxus brevifolia", "shaded moist understory")
    # Twisted twin-stem understory tree with deep-jade rounded masses.
    tube("yew_stem_a", [(-0.42, 0.05, 0.02, 0.36), (-0.66, 0.14, 1.6, 0.26),
                        (-0.28, 0.0, 3.6, 0.12), (-0.45, -0.08, 4.6, 0.05)],
         root, "bark", 7)
    tube("yew_stem_b", [(0.30, -0.08, 0.02, 0.40), (0.56, -0.18, 1.9, 0.26),
                        (0.12, -0.02, 4.0, 0.11), (0.42, 0.14, 4.9, 0.05)],
         root, "bark_dark", 7)
    root_flare(root, 1.55, 8, "bark", 0.4)
    masses = (((-1.30, 0.15, 2.55), (1.25, 0.95, 0.80), 0.6),
              ((1.35, -0.20, 2.85), (1.30, 0.95, 0.85), 2.9),
              ((-0.55, -0.60, 3.85), (1.15, 0.90, 0.78), 4.4),
              ((0.60, 0.55, 4.25), (1.10, 0.88, 0.76), 1.8),
              ((-0.05, 0.05, 5.00), (1.00, 0.82, 0.72), 6.0))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("yew_mass_%02d" % index, center, scale,
              ("jade", "jade_dark", "aqua_shadow"), root, seed,
              lobe_amp=0.17, lobe_count=4.0)
    # Coral arils sprinkled on the shaded masses are the species cue.
    for index in range(6):
        angle = index * 2.35
        berry("yew_aril_%02d" % index,
              (math.cos(angle) * (1.05 + 0.16 * (index % 3)),
               math.sin(angle) * (0.82 + 0.12 * (index % 2)),
               2.75 + 0.52 * index * 0.45), 0.19, root, "coral")
    ground_details(root, 1.30, True)
    return root


def bigleaf_maple() -> bpy.types.Object:
    root = new_root("lagoon_tree_bigleaf_maple", "Bigleaf maple",
                    "Acer macrophyllum", "moist meadow and forest edge")
    tube("maple_trunk", [(0, 0, 0.02, 0.92), (-0.15, 0.05, 1.9, 0.74),
                         (0.05, -0.05, 3.1, 0.55)], root, "bark", 10)
    tube("maple_fork_a", [(0.0, 0.0, 2.7, 0.52), (-1.55, 0.30, 4.2, 0.30),
                          (-2.45, 0.55, 5.1, 0.12)], root, "bark", 8)
    tube("maple_fork_b", [(0.02, 0.0, 2.8, 0.50), (1.60, -0.28, 4.3, 0.30),
                          (2.50, -0.55, 5.2, 0.12)], root, "bark", 8)
    root_flare(root, 2.5, 9, "bark_light", 0.15)
    # One broad cloud crown built from six big lobes.
    lobes = (((-2.45, 0.45, 5.55), (1.80, 1.45, 1.15), 0.7),
             ((-0.95, -0.85, 6.15), (1.85, 1.50, 1.20), 2.4),
             ((-0.85, 1.05, 6.20), (1.75, 1.42, 1.15), 4.0),
             ((0.95, 0.85, 6.15), (1.85, 1.50, 1.20), 5.6),
             ((1.05, -0.95, 6.05), (1.78, 1.45, 1.16), 1.5),
             ((0.05, 0.05, 7.05), (1.95, 1.60, 1.10), 3.2))
    for index, (center, scale, seed) in enumerate(lobes):
        cloud("maple_crown_%02d" % index, center, scale,
              ("mint_hi", "mint", "jade"), root, seed, lobe_amp=0.15,
              lobe_count=3.0)
    # Two clean paired double samaras tucked beneath the outer crown.
    samara("maple_samara_a", (-2.85, 0.55, 4.80), root, 0.8, 0.85)
    samara("maple_samara_b", (2.90, -0.60, 4.90), root, 4.0, 0.85)
    for index in range(4):
        cloud("maple_moss_%02d" % index,
              (-0.25 + 0.14 * index, -0.5, 0.9 + index * 0.6),
              (0.26, 0.12, 0.42), ("moss", "moss", "moss"), root,
              index + 0.4, rings=3, segments=7, lobe_amp=0.0)
    ground_details(root, 1.95, True)
    return root


def red_alder() -> bpy.types.Object:
    root = new_root("lagoon_tree_red_alder", "Red alder", "Alnus rubra",
                    "moist-wet meadow edge")
    # Pale paired trunks with dark dashes; airy separated crown lobes.
    tube("alder_trunk_a", [(-0.45, 0.05, 0.02, 0.40), (-0.60, 0.02, 3.4, 0.28),
                           (-0.40, 0.0, 6.4, 0.12), (-0.52, 0.05, 7.6, 0.05)],
         root, "alder_bark", 8)
    tube("alder_trunk_b", [(0.42, -0.06, 0.02, 0.36), (0.62, -0.02, 3.2, 0.25),
                           (0.45, 0.02, 6.0, 0.11), (0.62, 0.02, 7.2, 0.05)],
         root, "alder_bark", 8)
    bark_dashes(root, "alder_a", -0.55, 0.02, 0.34, (1.1, 1.9, 2.8, 3.7), 0.4)
    bark_dashes(root, "alder_b", 0.55, -0.02, 0.30, (1.4, 2.3, 3.3), 2.1)
    root_flare(root, 1.5, 7, "alder_bark", 0.22)
    lobes = (((-1.35, 0.25, 5.35), (1.15, 0.95, 1.00), 0.5),
             ((1.30, -0.20, 5.05), (1.10, 0.92, 0.95), 2.2),
             ((-0.60, -0.55, 6.55), (1.20, 0.98, 1.05), 3.9),
             ((0.75, 0.60, 6.35), (1.12, 0.94, 1.00), 5.4),
             ((-0.52, 0.30, 7.65), (1.00, 0.85, 0.92), 1.1),
             ((0.60, -0.15, 7.45), (0.95, 0.82, 0.88), 4.7))
    for index, (center, scale, seed) in enumerate(lobes):
        cloud("alder_crown_%02d" % index, center, scale,
              ("sage_hi", "sage", "jade"), root, seed, lobe_amp=0.14,
              lobe_count=3.0)
    # Golden catkin strings hang between the lobes.
    catkin("alder_catkin_a", (-1.75, 0.30, 4.75), 1.00, root, "butter",
           beads=4, bead_radius=0.15, stem_color="bark_dark")
    catkin("alder_catkin_b", (0.35, -0.55, 5.85), 0.95, root, "butter",
           beads=4, bead_radius=0.14, stem_color="bark_dark")
    catkin("alder_catkin_c", (1.75, 0.30, 4.55), 0.90, root, "butter",
           beads=4, bead_radius=0.14, stem_color="bark_dark")
    ground_details(root, 1.25, True)
    return root


def black_cottonwood() -> bpy.types.Object:
    root = new_root("lagoon_tree_black_cottonwood", "Black cottonwood",
                    "Populus trichocarpa", "wet riverbank and floodplain")
    tube("cottonwood_trunk", [(0, 0, 0.02, 0.62), (-0.04, 0, 3.6, 0.40),
                              (0.05, 0.02, 7.2, 0.16), (0, 0, 8.7, 0.05)],
         root, "bark_dark", 9)
    root_flare(root, 1.75, 8, "bark", 0.31)
    # Tall narrow stacked crown — five lobes rising in a flame.
    lobes = (((-0.55, 0.10, 4.15), (1.30, 1.05, 1.05), 0.8),
             ((0.60, -0.12, 4.75), (1.25, 1.00, 1.05), 2.5),
             ((-0.42, -0.15, 5.85), (1.15, 0.95, 1.05), 4.1),
             ((0.42, 0.18, 6.85), (1.05, 0.88, 1.00), 5.7),
             ((0.0, 0.0, 7.95), (0.88, 0.75, 0.95), 1.4))
    for index, (center, scale, seed) in enumerate(lobes):
        cloud("cottonwood_crown_%02d" % index, center, scale,
              ("mint_hi", "mint", "jade"), root, seed, lobe_amp=0.13,
              lobe_count=3.0)
    # Three restrained coral catkin/seed ornaments at the crown edges.
    catkin("cottonwood_catkin_a", (-1.55, 0.15, 4.35), 0.95, root, "salmon",
           beads=4, bead_radius=0.15)
    catkin("cottonwood_catkin_b", (1.50, -0.10, 5.35), 0.90, root, "salmon",
           beads=4, bead_radius=0.14)
    catkin("cottonwood_catkin_c", (-1.05, -0.15, 6.70), 0.85, root, "salmon",
           beads=4, bead_radius=0.14)
    ground_details(root, 1.40, True)
    return root


def pacific_madrone() -> bpy.types.Object:
    root = new_root("lagoon_tree_pacific_madrone", "Pacific madrone",
                    "Arbutus menziesii", "dry sunny bluff and forest edge")
    # Sinuous peeling coral trunk is the hero feature.
    tube("madrone_trunk",
         [(0, 0, 0.02, 0.72), (-0.45, 0.14, 1.5, 0.55),
          (0.30, -0.20, 3.0, 0.42), (-0.20, 0.10, 4.3, 0.30),
          (0.15, -0.05, 5.2, 0.18)], root, "madrone", 9)
    tube("madrone_limb_a", [(-0.10, 0.05, 3.9, 0.22), (-1.35, 0.40, 4.9, 0.13),
                            (-2.05, 0.65, 5.6, 0.06)], root, "madrone", 7)
    tube("madrone_limb_b", [(0.10, -0.05, 4.3, 0.20), (1.30, -0.40, 5.3, 0.12),
                            (1.95, -0.68, 5.9, 0.06)], root, "madrone", 7)
    root_flare(root, 2.1, 8, "madrone", 0.03)
    # Pale peeling ribbons wind up the trunk.
    for index in range(5):
        angle = index * 1.9
        cloud("madrone_peel_%02d" % index,
              (math.cos(angle) * 0.42 - 0.05, math.sin(angle) * 0.32,
               0.8 + index * 0.85),
              (0.20, 0.10, 0.55), ("madrone_light",) * 3, root,
              index + 0.7, rings=3, segments=7, lobe_amp=0.0)
    masses = (((-1.95, 0.60, 6.10), (1.35, 1.05, 0.85), 0.9),
              ((0.05, -0.20, 6.55), (1.55, 1.20, 0.95), 2.6),
              ((1.90, -0.62, 6.35), (1.30, 1.02, 0.85), 4.3),
              ((0.02, 0.75, 6.05), (1.25, 1.00, 0.82), 5.9))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("madrone_crown_%02d" % index, center, scale,
              ("jade", "jade_dark", "aqua_shadow"), root, seed,
              lobe_amp=0.15, lobe_count=4.0)
    berry_cluster("madrone_berries_a", (-1.75, 0.60, 5.45), root, "coral", 4, 0.16)
    berry_cluster("madrone_berries_b", (1.80, -0.60, 5.70), root, "coral", 4, 0.16)
    ground_details(root, 1.70, False)
    return root


def garry_oak() -> bpy.types.Object:
    root = new_root("lagoon_tree_garry_oak", "Garry oak",
                    "Quercus garryana", "dry sunny meadow and woodland")
    # Powerful low fork with a very broad open crown.
    tube("oak_trunk", [(0, 0, 0.02, 0.98), (-0.15, 0.06, 1.6, 0.82),
                       (0.08, -0.02, 2.5, 0.66)], root, "bark_dark", 10)
    tube("oak_fork_a", [(0.0, 0.0, 2.1, 0.60), (-1.90, 0.30, 3.3, 0.36),
                        (-3.30, 0.55, 4.1, 0.14)], root, "bark_dark", 8)
    tube("oak_fork_b", [(0.0, 0.0, 2.2, 0.58), (1.95, -0.28, 3.4, 0.36),
                        (3.40, -0.55, 4.2, 0.14)], root, "bark_dark", 8)
    tube("oak_fork_c", [(0.0, 0.0, 2.4, 0.45), (-0.35, -1.30, 3.8, 0.26),
                        (-0.75, -2.25, 4.6, 0.11)], root, "bark_dark", 7)
    root_flare(root, 2.7, 10, "bark", 0.20)
    lobes = (((-3.15, 0.50, 4.75), (1.70, 1.30, 0.95), 0.6),
             ((-1.05, -1.75, 5.05), (1.65, 1.30, 0.95), 2.3),
             ((-0.95, 1.15, 5.35), (1.72, 1.35, 1.00), 3.9),
             ((1.10, -0.85, 5.35), (1.75, 1.38, 1.00), 5.5),
             ((3.25, -0.50, 4.70), (1.68, 1.28, 0.94), 1.2),
             ((0.10, 0.15, 5.95), (1.60, 1.30, 0.92), 4.6))
    for index, (center, scale, seed) in enumerate(lobes):
        cloud("oak_crown_%02d" % index, center, scale,
              ("sage_hi", "jade", "jade_dark"), root, seed, lobe_amp=0.16,
              lobe_count=3.0)
    # Four sparse golden acorns under separate crown lobes.
    acorn("oak_acorn_a", (-3.05, 0.45, 3.90), 0.30, root)
    acorn("oak_acorn_b", (-0.85, -1.85, 4.20), 0.30, root)
    acorn("oak_acorn_c", (1.35, -0.90, 4.40), 0.30, root)
    acorn("oak_acorn_d", (3.15, -0.45, 3.95), 0.30, root)
    ground_details(root, 2.10, True)
    return root


def pacific_dogwood() -> bpy.types.Object:
    root = new_root("lagoon_tree_pacific_dogwood", "Pacific dogwood",
                    "Cornus nuttallii", "part-shade moist forest edge")
    tube("dogwood_trunk", [(0, 0, 0.02, 0.42), (0.10, -0.04, 1.8, 0.30),
                           (-0.05, 0.0, 3.4, 0.12)], root, "bark", 8)
    tube("dogwood_limb_a", [(0.02, 0.0, 2.0, 0.16), (-1.15, 0.25, 2.55, 0.09),
                            (-1.85, 0.40, 2.75, 0.04)], root, "bark", 6)
    tube("dogwood_limb_b", [(0.04, 0.0, 2.5, 0.14), (1.10, -0.22, 3.05, 0.08),
                            (1.75, -0.40, 3.25, 0.04)], root, "bark", 6)
    root_flare(root, 1.4, 7, "bark", 0.10)
    # Horizontal layered crown: three flattened wide masses.
    layers = (((-1.15, 0.20, 2.95), (1.60, 1.20, 0.50), 0.8),
              ((1.10, -0.20, 3.45), (1.55, 1.15, 0.48), 2.5),
              ((0.0, 0.05, 4.05), (1.30, 1.00, 0.46), 4.2))
    for index, (center, scale, seed) in enumerate(layers):
        cloud("dogwood_layer_%02d" % index, center, scale,
              ("mint_hi", "mint", "jade"), root, seed, lobe_amp=0.15,
              lobe_count=4.0)
    # Oversized four-bract white flowers sit proud of the layers.
    flower("dogwood_flower_a", (-1.45, 0.35, 3.60), 0.72, root, "white",
           "butter", petals=4, yaw=0.3)
    flower("dogwood_flower_b", (1.40, -0.35, 4.10), 0.72, root, "white",
           "butter", petals=4, yaw=1.1)
    flower("dogwood_flower_c", (0.10, 0.30, 4.70), 0.66, root, "white",
           "butter", petals=4, yaw=0.7)
    berry_cluster("dogwood_fruit", (-0.45, -0.85, 3.30), root, "coral", 3, 0.13)
    ground_details(root, 1.20, False, tuft_color="mint")
    return root


# ---------------------------------------------------------------------------
# Shrubs — six species, two structurally distinct variants each
# ---------------------------------------------------------------------------


def salal_a() -> bpy.types.Object:
    root = new_root("lagoon_shrub_salal_a", "Salal (broad mound)",
                    "Gaultheria shallon",
                    "dry-moist part-shade evergreen understory")
    # Low wide three-lobe deep-jade mound.
    masses = (((-0.75, 0.10, 0.55), (0.95, 0.72, 0.55), 0.7),
              ((0.72, -0.08, 0.58), (0.98, 0.74, 0.58), 2.4),
              ((0.0, 0.15, 0.92), (0.88, 0.68, 0.55), 4.1))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("salal_a_mound_%02d" % index, center, scale,
              ("jade", "jade_dark", "aqua_shadow"), root, seed,
              lobe_amp=0.18, lobe_count=4.0)
    # Cream bell cluster concentrated left on the mound, berries low right.
    for index in range(3):
        bell("salal_a_bell_%02d" % index,
             (-0.85 + 0.24 * index, 0.15 - 0.10 * index, 1.10 - 0.08 * index),
             0.17, root)
    berry_cluster("salal_a_berries", (0.72, -0.30, 0.68), root, "berry", 3, 0.12)
    ground_details(root, 0.85, True)
    return root


def salal_b() -> bpy.types.Object:
    root = new_root("lagoon_shrub_salal_b", "Salal (terraced mound)",
                    "Gaultheria shallon",
                    "dry-moist part-shade evergreen understory")
    # Compact upright terraced hill: four staggered blocks rising back-left.
    masses = (((0.45, -0.30, 0.42), (0.80, 0.62, 0.42), 0.9),
              ((-0.10, -0.05, 0.78), (0.82, 0.66, 0.48), 2.6),
              ((-0.48, 0.22, 1.18), (0.72, 0.58, 0.46), 4.3),
              ((-0.72, 0.42, 1.58), (0.58, 0.48, 0.42), 6.0))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("salal_b_step_%02d" % index, center, scale,
              ("jade", "jade_dark", "aqua_shadow"), root, seed,
              lobe_amp=0.18, lobe_count=4.0)
    for index in range(3):
        bell("salal_b_bell_%02d" % index,
             (-0.30 + 0.20 * index, 0.30 - 0.08 * index, 1.62 - 0.20 * index),
             0.16, root)
    berry_cluster("salal_b_berries", (0.40, -0.35, 0.55), root, "berry", 3, 0.11)
    ground_details(root, 0.80, True)
    return root


def oregon_grape_a() -> bpy.types.Object:
    root = new_root("lagoon_shrub_oregon_grape_a", "Low Oregon grape (starburst)",
                    "Mahonia nervosa", "dry-moist shaded evergreen understory")
    # Central crown mound with a radial starburst of four oversized
    # pointed teal leaves growing out of it.
    cloud("grape_a_crown", (0.0, 0.0, 0.35), (0.60, 0.60, 0.42),
          ("teal_hi", "teal", "teal_deep"), root, 1.4, lobe_amp=0.14,
          lobe_count=4.0)
    for index in range(4):
        yaw = 0.45 + index * math.tau / 4.0
        spear_leaf("grape_a_leaf_%02d" % index, (0.0, 0.0, 0.30), yaw,
                   1.30, 0.66, root, "teal", pitch=0.16)
    # Three upright gold racemes and a few lavender-blue berries.
    raceme("grape_a_spike_a", (-0.15, 0.10, 0.55), 1.00, root)
    raceme("grape_a_spike_b", (0.18, -0.05, 0.58), 0.88, root, lean=0.3)
    raceme("grape_a_spike_c", (0.0, 0.22, 0.52), 0.76, root, lean=-0.25)
    berry_cluster("grape_a_berries", (0.45, 0.35, 0.55), root, "berry_blue", 3, 0.12)
    ground_details(root, 0.80, False)
    return root


def oregon_grape_b() -> bpy.types.Object:
    root = new_root("lagoon_shrub_oregon_grape_b", "Low Oregon grape (spear-fan)",
                    "Mahonia nervosa", "dry-moist shaded evergreen understory")
    # Vertical asymmetric spear-fan: a solid leaning spine of three crown
    # steps with paired upswept leaves, narrow triangular profile.
    spine = (((0.10, 0.0, 0.35), (0.62, 0.52, 0.42), 0.9),
             ((-0.12, 0.05, 0.85), (0.55, 0.46, 0.40), 2.6),
             ((-0.34, 0.10, 1.38), (0.46, 0.40, 0.38), 4.3))
    for index, (center, scale, seed) in enumerate(spine):
        cloud("grape_b_spine_%02d" % index, center, scale,
              ("teal_hi", "teal", "teal_deep"), root, seed, lobe_amp=0.14,
              lobe_count=4.0)
    tiers = ((0.42, 1.00, 0.30), (0.90, 0.85, 0.46), (1.45, 0.70, 0.62))
    for index, (z, length, pitch) in enumerate(tiers):
        for side_index, yaw in enumerate((-0.62, 0.55)):
            spear_leaf("grape_b_tier_%02d_%02d" % (index, side_index),
                       (-0.12 * index, 0.0, z), yaw - 0.12 * index,
                       length, 0.52, root, "teal", pitch=pitch)
    raceme("grape_b_spike_a", (-0.42, 0.10, 1.60), 0.70, root, lean=-0.3)
    raceme("grape_b_spike_b", (0.25, -0.10, 1.05), 0.58, root, lean=0.25)
    berry_cluster("grape_b_berries", (0.40, 0.22, 0.45), root, "berry_blue", 3, 0.11)
    ground_details(root, 0.72, False)
    return root


def currant_a() -> bpy.types.Object:
    root = new_root("lagoon_shrub_red_flowering_currant_a",
                    "Red-flowering currant (rounded)",
                    "Ribes sanguineum", "dry-moist sunny forest edge")
    tube("currant_a_trunk", [(0.0, 0.0, 0.02, 0.16), (-0.06, 0.02, 0.55, 0.11)],
         root, "bark", 6)
    tube("currant_a_fork_a", [(-0.04, 0.0, 0.45, 0.10), (-0.55, 0.10, 1.05, 0.05)],
         root, "bark", 5)
    tube("currant_a_fork_b", [(0.04, 0.0, 0.50, 0.10), (0.55, -0.10, 1.10, 0.05)],
         root, "bark", 5)
    # Upright rounded three-mass shrub.
    masses = (((-0.62, 0.12, 1.45), (0.75, 0.60, 0.55), 0.8),
              ((0.62, -0.10, 1.50), (0.78, 0.62, 0.58), 2.5),
              ((0.0, 0.05, 1.95), (0.72, 0.58, 0.55), 4.2))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("currant_a_mass_%02d" % index, center, scale,
              ("mint", "jade", "jade_dark"), root, seed, lobe_amp=0.16,
              lobe_count=4.0)
    # Five oversized hanging coral tassels.
    for index, (x, y, z) in enumerate(((-1.05, 0.20, 1.35), (-0.45, -0.30, 1.75),
                                       (0.10, 0.30, 2.10), (0.60, -0.25, 1.85),
                                       (1.05, 0.15, 1.40))):
        tassel("currant_a_tassel_%02d" % index, (x, y, z), 0.62, root)
    ground_details(root, 0.70, False)
    return root


def currant_b() -> bpy.types.Object:
    root = new_root("lagoon_shrub_red_flowering_currant_b",
                    "Red-flowering currant (candelabra)",
                    "Ribes sanguineum", "dry-moist sunny forest edge")
    # Narrow upright candelabra: three stems, three separated clusters.
    stems = (((-0.35, 0.08, 1.15), 0.5), ((0.05, -0.05, 1.75), 1.9),
             ((0.42, 0.10, 1.40), 3.6))
    for index, ((x, y, z), seed) in enumerate(stems):
        tube("currant_b_stem_%02d" % index,
             [(x * 0.2, y * 0.2, 0.05, 0.10), (x * 0.7, y * 0.7, z * 0.55, 0.06),
              (x, y, z - 0.25, 0.035)], root, "bark", 5)
        cloud("currant_b_cluster_%02d" % index, (x, y, z),
              (0.55 + 0.06 * index, 0.46 + 0.05 * index, 0.44),
              ("mint", "jade", "jade_dark"), root, seed, lobe_amp=0.16,
              lobe_count=4.0)
    # Four large rose-coral tassels close to the vertical masses.
    tassel("currant_b_tassel_a", (-0.62, 0.15, 1.05), 0.75, root)
    tassel("currant_b_tassel_b", (-0.10, -0.28, 1.62), 0.80, root)
    tassel("currant_b_tassel_c", (0.30, 0.28, 1.30), 0.72, root)
    tassel("currant_b_tassel_d", (0.68, -0.05, 1.05), 0.70, root)
    ground_details(root, 0.62, False)
    return root


def oceanspray_a() -> bpy.types.Object:
    root = new_root("lagoon_shrub_oceanspray_a", "Oceanspray (fountain)",
                    "Holodiscus discolor", "dry-moist sunny or shaded slope")
    # Compact fountain of three pale-jade masses.
    masses = (((-0.55, 0.10, 0.80), (0.72, 0.58, 0.62), 0.9),
              ((0.55, -0.08, 0.85), (0.74, 0.60, 0.65), 2.6),
              ((0.0, 0.05, 1.35), (0.68, 0.56, 0.62), 4.3))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("oceanspray_a_mass_%02d" % index, center, scale,
              ("sage_hi", "sage", "jade"), root, seed, lobe_amp=0.15,
              lobe_count=4.0)
    # Five broad cream blossom plumes arcing outward all around the crown.
    for index in range(5):
        yaw = 0.3 + index * math.tau / 5.0
        plume("oceanspray_a_plume_%02d" % index,
              (math.sin(yaw) * 0.30, math.cos(yaw) * 0.26, 1.28), yaw,
              0.80, 0.28, root)
    ground_details(root, 0.72, False)
    return root


def oceanspray_b() -> bpy.types.Object:
    root = new_root("lagoon_shrub_oceanspray_b", "Oceanspray (tiered wedge)",
                    "Holodiscus discolor", "dry-moist sunny or shaded slope")
    # Broad solid tiered wedge ascending to one side.
    masses = (((0.62, -0.05, 0.48), (0.92, 0.70, 0.45), 0.8),
              ((0.0, 0.05, 0.92), (0.85, 0.66, 0.50), 2.5),
              ((-0.58, 0.12, 1.42), (0.72, 0.58, 0.48), 4.2))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("oceanspray_b_tier_%02d" % index, center, scale,
              ("sage_hi", "sage", "jade"), root, seed, lobe_amp=0.15,
              lobe_count=4.0)
    # Four chunky plumes pointing upward at staggered heights.
    for index, (x, y, z, yaw) in enumerate(((0.85, 0.05, 0.72, 0.5),
                                            (0.30, -0.15, 1.15, 0.2),
                                            (-0.25, 0.15, 1.60, -0.2),
                                            (-0.72, 0.05, 1.88, -0.5))):
        for pod in range(3):
            cloud("oceanspray_b_plume_%02d_%02d" % (index, pod),
                  (x + math.sin(yaw) * 0.09 * pod, y + 0.04 * pod,
                   z + 0.15 * pod),
                  (0.16 + 0.03 * pod, 0.16 + 0.03 * pod, 0.17 + 0.03 * pod),
                  ("cream", "cream", "cream"), root, pod * 1.6, rings=3,
                  segments=7, lobe_amp=0.0)
    ground_details(root, 0.75, False)
    return root


def salmonberry_a() -> bpy.types.Object:
    root = new_root("lagoon_shrub_salmonberry_a", "Salmonberry (broad mound)",
                    "Rubus spectabilis", "moist-wet bank and thicket")
    # Broad low three-cloud mint mound.
    masses = (((-0.75, 0.10, 0.60), (0.92, 0.70, 0.58), 0.9),
              ((0.72, -0.10, 0.62), (0.95, 0.72, 0.60), 2.6),
              ((0.0, 0.12, 1.02), (0.85, 0.66, 0.58), 4.3))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("salmonberry_a_mound_%02d" % index, center, scale,
              ("mint_hi", "mint", "jade"), root, seed, lobe_amp=0.17,
              lobe_count=4.0)
    # Three oversized magenta flowers, four salmon berry clusters.
    flower("salmonberry_a_flower_a", (-0.85, 0.30, 1.30), 0.42, root,
           "magenta", "butter", 5, 0.4)
    flower("salmonberry_a_flower_b", (0.15, 0.35, 1.62), 0.42, root,
           "magenta", "butter", 5, 1.2)
    flower("salmonberry_a_flower_c", (0.85, -0.10, 1.28), 0.38, root,
           "magenta", "butter", 5, 2.0)
    for index, (x, y, z) in enumerate(((-0.45, -0.55, 0.85), (0.35, -0.60, 0.80),
                                       (-0.05, 0.60, 0.95), (1.05, 0.25, 0.70))):
        berry_cluster("salmonberry_a_fruit_%02d" % index, (x, y, z), root,
                      "salmon", 4, 0.13)
    ground_details(root, 0.82, False)
    return root


def salmonberry_b() -> bpy.types.Object:
    root = new_root("lagoon_shrub_salmonberry_b", "Salmonberry (clustered tower)",
                    "Rubus spectabilis", "moist-wet bank and thicket")
    # Tall asymmetric clustered tower stepping diagonally.
    masses = (((0.15, -0.05, 0.65), (0.95, 0.75, 0.65), 0.9),
              ((-0.35, 0.15, 1.45), (0.72, 0.58, 0.52), 2.6),
              ((-0.72, 0.30, 2.05), (0.55, 0.46, 0.44), 4.3))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("salmonberry_b_step_%02d" % index, center, scale,
              ("mint_hi", "mint", "jade"), root, seed, lobe_amp=0.17,
              lobe_count=4.0)
    flower("salmonberry_b_flower_a", (0.60, 0.30, 1.20), 0.42, root,
           "magenta", "butter", 5, 0.6)
    flower("salmonberry_b_flower_b", (-0.80, 0.45, 2.45), 0.38, root,
           "magenta", "butter", 5, 1.5)
    for index, (x, y, z) in enumerate(((0.65, -0.40, 0.90), (-0.10, 0.55, 1.75),
                                       (-0.62, -0.20, 1.40))):
        berry_cluster("salmonberry_b_fruit_%02d" % index, (x, y, z), root,
                      "salmon", 4, 0.13)
    ground_details(root, 0.72, False)
    return root


def trailing_blackberry_a() -> bpy.types.Object:
    root = new_root("lagoon_shrub_trailing_blackberry_a",
                    "Trailing blackberry (creeping crescent)",
                    "Rubus ursinus", "dry-moist open ground and woodland edge")
    # Low creeping crescent: two thick curved canes arcing over the pads.
    tube("blackberry_a_cane_a",
         [(-1.15, 0.15, 0.12, 0.10), (-0.45, -0.10, 0.78, 0.08),
          (0.45, 0.10, 0.72, 0.07), (1.15, -0.05, 0.20, 0.05)],
         root, "bark", 6)
    tube("blackberry_a_cane_b",
         [(-0.95, -0.25, 0.10, 0.08), (-0.15, -0.40, 0.62, 0.07),
          (0.70, -0.30, 0.55, 0.06), (1.25, -0.35, 0.12, 0.04)],
         root, "bark", 6)
    pads = (((-0.85, 0.05, 0.32), (0.62, 0.50, 0.34), 0.9),
            ((0.05, -0.12, 0.38), (0.66, 0.52, 0.36), 2.6),
            ((0.90, -0.05, 0.30), (0.60, 0.48, 0.33), 4.3))
    for index, (center, scale, seed) in enumerate(pads):
        cloud("blackberry_a_pad_%02d" % index, center, scale,
              ("jade", "jade_dark", "aqua_shadow"), root, seed,
              lobe_amp=0.19, lobe_count=4.0)
    # Two oversized white flowers and four dark berry clusters.
    flower("blackberry_a_flower_a", (-0.55, 0.28, 0.72), 0.36, root,
           "white", "butter", 5, 0.5)
    flower("blackberry_a_flower_b", (0.55, 0.18, 0.76), 0.36, root,
           "white", "butter", 5, 1.4)
    for index, (x, y, z) in enumerate(((-1.05, -0.20, 0.38), (-0.25, -0.42, 0.50),
                                       (0.40, -0.38, 0.48), (1.10, -0.25, 0.32))):
        berry_cluster("blackberry_a_fruit_%02d" % index, (x, y, z), root,
                      "berry", 5, 0.11)
    ground_details(root, 0.85, True, tuft_color="jade")
    return root


def trailing_blackberry_b() -> bpy.types.Object:
    root = new_root("lagoon_shrub_trailing_blackberry_b",
                    "Trailing blackberry (cane arch)",
                    "Rubus ursinus", "dry-moist open ground and woodland edge")
    # Compact arching bramble with a clear tunnel-like negative space.
    tube("blackberry_b_arch",
         [(-0.85, 0.0, 0.10, 0.07), (-0.55, 0.05, 0.72, 0.06),
          (0.0, 0.02, 0.98, 0.055), (0.55, -0.05, 0.70, 0.05),
          (0.85, 0.0, 0.10, 0.04)], root, "bark", 6)
    masses = (((-0.95, -0.05, 0.35), (0.55, 0.46, 0.38), 0.9),
              ((0.95, 0.05, 0.32), (0.52, 0.44, 0.36), 2.6),
              ((0.0, 0.02, 1.15), (0.48, 0.40, 0.32), 4.3))
    for index, (center, scale, seed) in enumerate(masses):
        cloud("blackberry_b_mass_%02d" % index, center, scale,
              ("jade", "jade_dark", "aqua_shadow"), root, seed,
              lobe_amp=0.19, lobe_count=4.0)
    flower("blackberry_b_flower", (0.10, 0.18, 1.50), 0.36, root,
           "cream", "butter", 5, 0.8)
    for index, (x, y, z) in enumerate(((-1.15, 0.12, 0.62), (-0.48, 0.12, 1.02),
                                       (0.48, -0.12, 0.98), (1.10, 0.12, 0.58),
                                       (0.78, 0.18, 0.32))):
        berry_cluster("blackberry_b_fruit_%02d" % index, (x, y, z), root,
                      "berry", 5, 0.11)
    ground_details(root, 0.78, True, tuft_color="jade")
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
    "lagoon_shrub_salal_a": salal_a,
    "lagoon_shrub_salal_b": salal_b,
    "lagoon_shrub_oregon_grape_a": oregon_grape_a,
    "lagoon_shrub_oregon_grape_b": oregon_grape_b,
    "lagoon_shrub_red_flowering_currant_a": currant_a,
    "lagoon_shrub_red_flowering_currant_b": currant_b,
    "lagoon_shrub_oceanspray_a": oceanspray_a,
    "lagoon_shrub_oceanspray_b": oceanspray_b,
    "lagoon_shrub_salmonberry_a": salmonberry_a,
    "lagoon_shrub_salmonberry_b": salmonberry_b,
    "lagoon_shrub_trailing_blackberry_a": trailing_blackberry_a,
    "lagoon_shrub_trailing_blackberry_b": trailing_blackberry_b,
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
