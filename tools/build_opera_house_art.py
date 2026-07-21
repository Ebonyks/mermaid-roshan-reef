#!/usr/bin/env python3
"""Build the Pearl Opera House authored art set (Codex designs, first pass).

Run with either:
  blender --background --python tools/build_opera_house_art.py
  python3 tools/build_opera_house_art.py          (pip bpy module)

Generates smooth, beveled toy-theatre GLBs under assets/art35/opera/ that the
lobby and the grand-finale stage load with primitive fallbacks. All original
work; flat toon-friendly materials; no textures (POT rule trivially satisfied).
Protected book, family, friend and character art is never read or modified.
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "art35" / "opera"
OUT.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "gold": (1.0, 0.72, 0.28, 1.0),
    "velvet": (0.55, 0.10, 0.16, 1.0),
    "velvet_dark": (0.42, 0.07, 0.12, 1.0),
    "plum": (0.30, 0.20, 0.38, 1.0),
    "cream": (0.96, 0.92, 0.84, 1.0),
    "night": (0.10, 0.09, 0.22, 1.0),
    "skin": (0.92, 0.90, 1.0, 1.0),
    "glass": (0.65, 0.90, 1.0, 1.0),
    "brass": (0.80, 0.62, 0.30, 1.0),
}
_mats = {}


def mat(name):
    if name not in _mats:
        m = bpy.data.materials.new("opera_" + name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = PALETTE[name]
        bsdf.inputs["Roughness"].default_value = 0.65
        _mats[name] = m
    return _mats[name]


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear()


def finish(obj, name, bevel=0.02):
    obj.name = name
    if bevel > 0:
        b = obj.modifiers.new("bevel", "BEVEL")
        b.width = bevel
        b.segments = 2
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    for mod in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return obj


def cube(size, loc, m, name="part", bevel=0.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat(m))
    return finish(o, name, bevel)


def cyl(r, depth, loc, m, name="part", verts=24, bevel=0.02, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, vertices=verts)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=depth, location=loc, vertices=verts)
    o = bpy.context.active_object
    o.data.materials.append(mat(m))
    return finish(o, name, bevel)


def sphere(r, loc, m, name="part", seg=20):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=max(8, seg // 2))
    o = bpy.context.active_object
    o.data.materials.append(mat(m))
    return finish(o, name, bevel=0)


def torus(r_maj, r_min, loc, m, name="part", rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r_maj, minor_radius=r_min, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.data.materials.append(mat(m))
    return finish(o, name, bevel=0)


def export(fname):
    bpy.ops.object.select_all(action="SELECT")
    path = str(OUT / fname)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True)
    print("wrote", fname, f"{(OUT / fname).stat().st_size // 1024}kb")


def build_arch():
    """Grand proscenium: fluted columns, arched beam, star keystone."""
    reset()
    for sx in (-1, 1):
        cyl(0.55, 8.0, (sx * 6.0, 0, 4.0), "cream", "column", bevel=0)
        cyl(0.75, 0.5, (sx * 6.0, 0, 0.25), "gold", "base")
        cyl(0.75, 0.5, (sx * 6.0, 0, 7.85), "gold", "cap")
        torus(0.62, 0.09, (sx * 6.0, 0, 2.6), "gold", "ring", rot=(0, 0, 0))
    # arched beam: ring segment approximated with rotated blocks
    for i in range(9):
        a = math.pi * (i / 8.0)
        x = math.cos(a) * 6.0
        z = 8.0 + math.sin(a) * 2.4
        b = cube((1.7, 0.9, 1.0), (x, 0, z), "velvet", "arch_stone")
        b.rotation_euler = (0, a - math.pi / 2, 0)
    cube((13.4, 0.8, 0.9), (0, 0, 8.15), "gold", "lintel")
    s = sphere(0.65, (0, 0, 10.9), "gold", "star_keystone", seg=8)
    s.scale = (1.0, 0.4, 1.0)
    export("opera_arch.glb")


def build_curtain():
    """Swagged side curtain: sine-fold shells + gathered tieback + valance."""
    reset()
    for i in range(6):
        x = -1.5 + i * 0.6
        r = 0.42 + 0.1 * math.sin(i * 2.1)
        c = cyl(r, 7.6, (x, 0, 3.8), "velvet" if i % 2 == 0 else "velvet_dark", "fold", verts=14, bevel=0)
        c.scale = (1.0, 0.55, 1.0)
    torus(0.9, 0.22, (0, 0, 2.2), "gold", "tieback", rot=(math.pi / 2, 0, 0))
    v = cube((4.2, 1.0, 1.3), (0, 0, 7.9), "velvet_dark", "valance")
    v.rotation_euler = (0.12, 0, 0)
    export("opera_curtain.glb")


def build_door():
    """Career marquee door: gold frame, recessed panel, curtain folds."""
    reset()
    cube((5.6, 0.5, 9.4), (0, 0.25, 4.7), "plum", "recess")
    for sx in (-1, 1):
        cyl(0.42, 9.8, (sx * 2.7, 0, 4.9), "gold", "pillar", verts=16, bevel=0)
        sphere(0.5, (sx * 2.7, 0, 10.0), "gold", "finial", seg=10)
    cube((6.4, 0.8, 0.9), (0, 0, 9.85), "gold", "lintel")
    for i in range(5):
        x = -1.8 + i * 0.9
        c = cyl(0.36, 8.2, (x, -0.15, 4.1), "velvet" if i % 2 == 0 else "velvet_dark", "curtain_fold", verts=12, bevel=0)
        c.scale = (1.0, 0.5, 1.0)
    export("opera_door.glb")


def build_medallion():
    """Centre-stage medallion: inlaid disc, star relief, halo ring."""
    reset()
    cyl(3.4, 0.35, (0, 0, 0.18), "plum", "disc", verts=36, bevel=0.04)
    torus(3.3, 0.18, (0, 0, 0.4), "gold", "halo")
    for i in range(5):
        a = i * math.tau / 5 - math.pi / 2
        arm = cube((0.5, 1.9, 0.16), (math.cos(a) * 1.0, math.sin(a) * 1.0, 0.44), "gold", "star_arm", bevel=0)
        arm.rotation_euler = (0, 0, a + math.pi / 2)
    sphere(0.5, (0, 0, 0.5), "gold", "star_heart", seg=10)
    export("opera_medallion.glb")


def build_chandelier():
    """Crystal chandelier: gold ring, six arms, glass drops, glow bulb."""
    reset()
    torus(1.9, 0.14, (0, 0, 0), "gold", "ring")
    sphere(0.75, (0, 0, -0.2), "cream", "bulb", seg=14)
    for i in range(6):
        a = i * math.tau / 6
        x, y = math.cos(a) * 1.9, math.sin(a) * 1.9
        cyl(0.06, 1.2, (x * 0.55, y * 0.55, 0.45), "gold", "arm", verts=8, bevel=0)
        d = sphere(0.22, (x, y, -0.55), "glass", "drop", seg=8)
        d.scale = (1.0, 1.0, 1.6)
    cyl(0.07, 2.2, (0, 0, 1.3), "gold", "chain", verts=8, bevel=0)
    export("opera_chandelier.glb")


def build_bench():
    """Tufted audience bench with turned gold feet."""
    reset()
    seat = cube((9.6, 2.6, 1.0), (0, 0, 1.35), "velvet", "seat", bevel=0.12)
    seat.scale = (1.0, 1.0, 1.0)
    cube((9.6, 0.7, 1.9), (0, 1.15, 2.4), "velvet_dark", "back", bevel=0.1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(0.22, 0.9, (sx * 4.2, sy * 0.9, 0.45), "gold", "foot", verts=10, bevel=0)
    for i in range(4):
        sphere(0.14, (-3.3 + i * 2.2, -0.05, 1.9), "gold", "tuft", seg=8)
    export("opera_bench.glb")


def build_railing():
    """Mezzanine railing segment (6 units wide): balusters + gold rail."""
    reset()
    cube((6.0, 0.35, 0.3), (0, 0, 3.0), "gold", "rail", bevel=0.05)
    cube((6.0, 0.3, 0.25), (0, 0, 0.15), "plum", "shoe", bevel=0.04)
    for i in range(5):
        x = -2.4 + i * 1.2
        c = cyl(0.16, 2.6, (x, 0, 1.55), "cream", "baluster", verts=10, bevel=0)
        sphere(0.2, (x, 0, 1.55), "cream", "belly", seg=8)
    export("opera_railing.glb")


def build_lift():
    """Bubble lift: glass column, brass base + top rings."""
    reset()
    g = cyl(2.6, 26.0, (0, 0, 13.0), "glass", "glass_column", verts=20, bevel=0)
    gm = g.data.materials[0]
    bsdf = gm.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Alpha"].default_value = 0.25
    gm.blend_method = "BLEND"
    torus(2.7, 0.3, (0, 0, 0.3), "brass", "base_ring")
    torus(2.7, 0.3, (0, 0, 25.7), "brass", "top_ring")
    cyl(3.1, 0.5, (0, 0, 0.1), "plum", "pad", verts=24)
    export("opera_lift.glb")


def build_maestro():
    """The Midnight Maestro: swirled gown, head, collar, gold baton."""
    reset()
    gown = cyl(2.9, 6.2, (0, 0, 3.1), "night", "gown", verts=28, r2=0.4, bevel=0)
    gown.scale = (1.0, 0.85, 1.0)
    torus(1.15, 0.3, (0, 0, 5.9), "plum", "collar", rot=(0, 0, 0))
    sphere(1.05, (0, 0.45, 6.6), "skin", "head", seg=18)
    for sx in (-1, 1):
        sphere(0.2, (sx * 0.4, 1.35, 6.8), "night", "eye", seg=8)
    b = cyl(0.09, 2.6, (2.0, 0.6, 5.6), "gold", "baton", verts=8, bevel=0)
    b.rotation_euler = (0, math.radians(-38), 0)
    sphere(0.42, (0, 1.4, 4.6), "gold", "brooch", seg=10)
    export("opera_maestro.glb")


def build_stage_apron():
    """Grand stage apron: curved gold-trimmed footlight edge."""
    reset()
    cube((26.0, 2.2, 1.1), (0, 0, 0.55), "velvet_dark", "apron")
    cube((26.0, 2.3, 0.25), (0, 0, 1.2), "gold", "trim", bevel=0.04)
    for i in range(7):
        x = -10.8 + i * 3.6
        sphere(0.3, (x, -1.15, 1.05), "cream", "footlight", seg=10)
    export("opera_stage_apron.glb")


if __name__ == "__main__":
    build_arch()
    build_curtain()
    build_door()
    build_medallion()
    build_chandelier()
    build_bench()
    build_railing()
    build_lift()
    build_maestro()
    build_stage_apron()
    print("opera art set complete")
