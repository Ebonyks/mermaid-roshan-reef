"""Build the Fable 5 constructed-model kit from the approved E1 reference
sheets (gen2/generated/*) to the measurements in
gen2/generated/MEASURED_INTERFACE_SHEET_2026-07-19.md.

Outputs (assets/fable_kit/):
  coral_bare_0.glb      r003 bare branching coral   — single mesh, origin at burial point
  kelp_vol_0.glb        r004 volumetric tall kelp   — single mesh, origin at burial point
  loco_body.glb         r021A locomotive body shell — origin at railhead, +Z = travel
  track_straight.glb    r021B straight segment, L 5.013 — single mesh, +Z = travel
  track_curve.glb       r021C quarter curve, r 12   — single mesh, origin at entry end
  station_platform.glb  r021D low platform          — origin at ground center
  station_shelter.glb   r021E open shelter          — origin at platform-deck level

Blender is Z-up here; the glTF exporter (+Y up) maps a Godot point
(gx, gy, gz) to Blender (gx, -gz, gy). helpers take GODOT coords.

Run: blender --background --python tools/build_fable_kit.py
Headless gotchas honoured: no transform_apply / no object.join — meshes are
fused via evaluated-depsgraph bmesh appends only.
"""
import math
import os
import random

import bpy
import bmesh
from mathutils import Matrix, Vector

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "fable_kit")
RNG = random.Random(5)

# ---------------------------------------------------------------- palette
COLS = {
    "coral_pink":   (0.94, 0.56, 0.58),
    "coral_tip":    (0.97, 0.90, 0.82),
    "coral_base":   (0.70, 0.62, 0.88),
    "kelp_green":   (0.53, 0.70, 0.52),
    "kelp_purple":  (0.60, 0.50, 0.74),
    "kelp_stem":    (0.22, 0.44, 0.52),
    "teal":         (0.35, 0.75, 0.78),
    "navy":         (0.22, 0.22, 0.40),
    "gold":         (0.95, 0.80, 0.40),
    "window":       (1.00, 0.92, 0.65),
    "coupler_red":  (0.93, 0.45, 0.45),
    "rail_navy":    (0.30, 0.28, 0.50),
    "tie_lav":      (0.66, 0.58, 0.82),
    "deck_teal":    (0.45, 0.78, 0.76),
    "cream":        (0.93, 0.89, 0.80),
    "skirt_lav":    (0.66, 0.60, 0.84),
    "post_aqua":    (0.62, 0.85, 0.88),
    "roof_purple":  (0.48, 0.44, 0.72),
}
_mats = {}


def mat(name, emission=0.0):
    key = (name, emission)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(f"{name}_e{emission}" if emission else name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    col = COLS[name] + (1.0,)
    bsdf.inputs["Base Color"].default_value = col
    bsdf.inputs["Roughness"].default_value = 0.85
    if emission > 0.0:
        bsdf.inputs["Emission Color"].default_value = col
        bsdf.inputs["Emission Strength"].default_value = emission
    _mats[key] = m
    return m


def g2b(gx, gy, gz):
    """Godot (x, y, z-forward) -> Blender Z-up vector."""
    return Vector((gx, -gz, gy))


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear()


def new_obj(name, mesh):
    ob = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(ob)
    return ob


def prim_box(name, center_g, size_g, material, bevel=0.05):
    """Axis-aligned box, Godot center/size."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me)
    bm.free()
    ob = new_obj(name, me)
    sx, sy, sz = size_g[0], size_g[2], size_g[1]   # godot size -> blender xyz
    me.transform(Matrix.Diagonal((sx, sy, sz, 1.0)))
    me.transform(Matrix.Translation(g2b(*center_g)))
    me.materials.append(material)
    if bevel > 0.0:
        b = ob.modifiers.new("bev", "BEVEL")
        b.width = min(bevel, 0.45 * min(sx, sy, sz))
        b.segments = 2
        b.limit_method = "ANGLE"
    return ob


def prim_cyl(name, center_g, r_top, r_bot, height, material, axis="Y",
             verts=20, scale_g=None):
    """Cylinder along a GODOT axis ('Y' vertical or 'Z' travel)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts,
                          radius1=r_bot, radius2=r_top, depth=height)
    bm.to_mesh(me)
    bm.free()
    ob = new_obj(name, me)
    if axis == "Z":                      # godot z = blender -Y
        me.transform(Matrix.Rotation(math.radians(90.0), 4, "X"))
    if scale_g is not None:
        me.transform(Matrix.Diagonal((scale_g[0], scale_g[2], scale_g[1], 1.0)))
    me.transform(Matrix.Translation(g2b(*center_g)))
    me.materials.append(material)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def prim_sphere(name, center_g, r, material):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=r)
    bm.to_mesh(me)
    bm.free()
    ob = new_obj(name, me)
    me.transform(Matrix.Translation(g2b(*center_g)))
    me.materials.append(material)
    for p in me.polygons:
        p.use_smooth = True
    return ob


def fuse_and_export(objs, out_name, single_mesh):
    """Evaluate every object (modifiers applied), optionally fuse to ONE mesh,
    then export GLB."""
    dg = bpy.context.evaluated_depsgraph_get()
    if single_mesh:
        fused = bpy.data.meshes.new(out_name)
        bm = bmesh.new()
        mat_slots = []
        for ob in objs:
            ev = ob.evaluated_get(dg)
            me = bpy.data.meshes.new_from_object(ev, depsgraph=dg)
            me.transform(ob.matrix_world)
            base = len(mat_slots)
            for m in (me.materials if me.materials else [None]):
                mat_slots.append(m)
            for p in me.polygons:
                p.material_index += base
            tmp = bmesh.new()
            tmp.from_mesh(me)
            tmp.to_mesh(me)
            tmp.free()
            bm.from_mesh(me)
            bpy.data.meshes.remove(me)
        bm.to_mesh(fused)
        bm.free()
        # dedupe material slots
        remap, final = {}, []
        for i, m in enumerate(mat_slots):
            if m in final:
                remap[i] = final.index(m)
            else:
                remap[i] = len(final)
                final.append(m)
        for m in final:
            fused.materials.append(m)
        for p in fused.polygons:
            p.material_index = remap.get(p.material_index, 0)
        for ob in list(objs):
            bpy.data.objects.remove(ob)
        new_obj(out_name, fused)
    path = os.path.join(OUT_DIR, out_name + ".glb")
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB",
                              export_apply=True, export_yup=True)
    print(f"EXPORTED {path}")


# ================================================================ r003 coral
def build_coral():
    reset_scene()
    branches = []          # (p0, p1, r0, r1) godot coords

    def grow(p, d, length, r, depth):
        tip = (p[0] + d[0] * length, p[1] + d[1] * length, p[2] + d[2] * length)
        r_tip = max(0.055, r * (0.62 if depth > 0 else 0.5))
        branches.append((p, tip, r, r_tip))
        if depth == 0:
            return [tip]
        tips = []
        n = 2 if depth > 1 else RNG.choice([1, 2])
        for k in range(n):
            ang = RNG.uniform(0.35, 0.75) * (1 if k == 0 else -1)
            yaw = RNG.uniform(0.6, 2.4) * RNG.choice([1.0, -1.0])
            ca, sa = math.cos(ang), math.sin(ang)
            nd = (d[0] * ca + sa * math.cos(yaw),
                  d[1] * ca + abs(sa) * 0.55,
                  d[2] * ca + sa * math.sin(yaw))
            ln = math.sqrt(sum(c * c for c in nd))
            nd = tuple(c / ln for c in nd)
            tips += grow(tip, nd, length * RNG.uniform(0.55, 0.75), r_tip, depth - 1)
        return tips

    # fused trunk (buried foot -0.15), one high fork + one low lateral arm
    branches.append(((0, -0.15, 0), (0, 0.55, 0), 0.26, 0.21))
    tips = []
    tips += grow((0, 0.55, 0), (0.30, 0.92, 0.18), 1.05, 0.21, 3)     # high fork
    tips += grow((0, 0.55, 0), (-0.68, 0.60, -0.34), 0.86, 0.19, 2)   # low lateral
    tips += grow((0, 0.45, 0), (0.10, 0.78, -0.60), 0.72, 0.15, 1)    # rear arm
    tips += grow((0, 0.50, 0), (-0.18, 0.85, 0.50), 0.64, 0.13, 1)    # front sprig

    me = bpy.data.meshes.new("coral_skel")
    verts, edges, radii = [], [], []
    for p0, p1, r0, r1 in branches:
        i = len(verts)
        verts += [g2b(*p0), g2b(*p1)]
        radii += [r0, r1]
        edges.append((i, i + 1))
    me.from_pydata(verts, edges, [])
    ob = new_obj("coral", me)
    # weld duplicate vertices so the skin fuses at forks
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.02)
    bm.to_mesh(me)
    bm.free()
    skin = ob.modifiers.new("skin", "SKIN")
    skin.use_smooth_shade = False       # faceted low-poly planes per the sheet
    sub = ob.modifiers.new("sub", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 1
    # per-vertex skin radii: nearest original endpoint's radius
    sv = me.skin_vertices[0].data
    for i, v in enumerate(me.vertices):
        best, br = 1e9, 0.2
        for (p0, p1, r0, r1) in branches:
            for p, r in ((p0, r0), (p1, r1)):
                d = (v.co - g2b(*p)).length
                if d < best:
                    best, br = d, r
        sv[i].radius = (br, br)
    # materials by height band + tip proximity, applied after evaluation
    dg = bpy.context.evaluated_depsgraph_get()
    ev = bpy.data.meshes.new_from_object(ob.evaluated_get(dg), depsgraph=dg)
    for p in ev.polygons:
        p.use_smooth = False
    ev.materials.append(mat("coral_pink"))
    ev.materials.append(mat("coral_tip"))
    ev.materials.append(mat("coral_base"))
    tip_pts = [g2b(*t) for t in tips]
    for p in ev.polygons:
        c = p.center
        if any((c - t).length < 0.16 for t in tip_pts):
            p.material_index = 1
        elif c.z < 0.28:
            p.material_index = 2
    bpy.data.objects.remove(ob)
    new_obj("coral_final", ev)
    fuse_and_export([bpy.data.objects["coral_final"]], "coral_bare_0",
                    single_mesh=True)


# ================================================================ r004 kelp
def build_kelp():
    reset_scene()
    objs = []
    # narrow buried root -> visible thin stems (open lower third) -> ribbon
    # blades with S-sway forming a broad irregular canopy, per the v2 sheet.
    blades = [
        # (yaw deg, radial, blade_z0, height, width, sway_amp, purple_back)
        (0,    0.18, 1.05, 3.45, 0.24, 0.34, True),
        (55,   0.34, 0.95, 3.05, 0.22, 0.30, False),
        (130,  0.30, 0.85, 2.65, 0.21, 0.28, True),
        (200,  0.38, 0.80, 2.30, 0.19, 0.26, False),
        (275,  0.30, 0.72, 1.90, 0.17, 0.24, True),
        (330,  0.42, 0.65, 1.50, 0.15, 0.20, False),
    ]
    for bi, (yaw, rad, z0, h, w, amp, purple) in enumerate(blades):
        rot = Matrix.Rotation(math.radians(yaw), 4, "Z")
        # stem: thin tapered strut from the buried root to the blade foot
        foot = rot @ Vector((rad, 0.0, z0))
        stem = prim_cyl(f"stem{bi}", (0, 0, 0), 0.028, 0.05, 1.0,
                        mat("kelp_stem"), verts=8)
        sm = stem.data
        d = foot - Vector((rad * 0.25 * math.cos(math.radians(yaw)),
                           rad * 0.25 * math.sin(math.radians(yaw)), -0.1))
        sm.transform(Matrix.Translation(Vector((0, 0, 0.5))))   # base at origin
        sm.transform(Matrix.Diagonal((1.0, 1.0, d.length, 1.0)))
        sm.transform(d.to_track_quat("Z", "Y").to_matrix().to_4x4())
        sm.transform(Matrix.Translation(
            Vector((rad * 0.25 * math.cos(math.radians(yaw)),
                    rad * 0.25 * math.sin(math.radians(yaw)), -0.1))))
        objs.append(stem)
        # ribbon blade
        segs = 22
        me = bpy.data.meshes.new(f"blade{bi}")
        verts, faces = [], []
        phase = RNG.uniform(0, math.tau)
        lean = RNG.uniform(0.10, 0.30) * RNG.choice([1.0, -1.0])
        spread = 0.42 + 0.18 * (bi % 3)     # canopy fans OUTWARD radially
        for i in range(segs + 1):
            t = i / segs
            z = z0 + t * (h - z0)
            sway = amp * math.sin(t * 3.4 + phase) * (0.25 + 0.75 * t) \
                + lean * t * t
            wt = w * (0.16 + 1.9 * t * (1.0 - t) ** 0.6)
            if i == segs:
                wt = 0.012
            twist = 1.1 * math.sin(t * 2.6 + phase) + bi * 0.9
            dx, dy = math.cos(twist) * wt, math.sin(twist) * wt
            rr = rad + spread * t * t       # outward drift with height
            verts.append(Vector((rr - dx, -dy + sway, z)))
            verts.append(Vector((rr + dx, dy + sway, z)))
        for i in range(segs):
            a = i * 2
            faces.append((a, a + 1, a + 3, a + 2))
        me.from_pydata(verts, [], faces)
        me.materials.append(mat("kelp_green"))
        me.materials.append(mat("kelp_purple"))
        for p in me.polygons:
            p.use_smooth = True
        ob = new_obj(f"blade{bi}", me)
        sol = ob.modifiers.new("sol", "SOLIDIFY")
        sol.thickness = 0.05
        sol.offset = 0.0
        if purple:
            sol.material_offset = 1
        me.transform(rot)
        objs.append(ob)
    fuse_and_export(objs, "kelp_vol_0", single_mesh=True)


# ============================================================ r021A loco body
def build_loco():
    reset_scene()
    teal, navy, gold = mat("teal"), mat("navy"), mat("gold")
    o = []
    # boiler + smokebox + headlamp
    o.append(prim_cyl("boiler", (0, 3.8, 1.4), 1.9, 1.9, 5.2, teal, axis="Z"))
    o.append(prim_cyl("smokebox", (0, 3.8, 4.2), 2.05, 2.05, 0.6, navy, axis="Z"))
    o.append(prim_sphere("headlamp", (0, 3.8, 4.6), 0.55, mat("window", 2.0)))
    for i, bz in enumerate((0.0, 2.6)):
        o.append(prim_cyl(f"band{i}", (0, 3.8, bz), 1.98, 1.98, 0.3, gold, axis="Z"))
    # funnel (navy, gold lip) + steam dome
    o.append(prim_cyl("funnel", (0, 6.4, 3.2), 1.0, 0.55, 1.7, navy))
    o.append(prim_cyl("funnel_lip", (0, 7.2, 3.2), 1.05, 0.98, 0.28, gold))
    o.append(prim_sphere("dome", (0, 5.9, 0.8), 0.8, gold))
    o.append(prim_cyl("dome_collar", (0, 5.55, 0.8), 0.62, 0.72, 0.5, gold))
    # cab, rounded navy roof, warm windows
    o.append(prim_box("cab", (0, 4.6, -2.9), (4.4, 3.8, 2.8), teal, bevel=0.10))
    o.append(prim_box("cab_roof", (0, 6.75, -2.9), (5.0, 0.5, 3.4), navy, bevel=0.16))
    for i, sx in enumerate((-1.0, 1.0)):
        o.append(prim_box(f"win{i}", (sx * 2.25, 5.1, -2.9), (0.14, 1.5, 1.5),
                          mat("window", 1.2), bevel=0.03))
        o.append(prim_box(f"trim{i}", (sx * 2.28, 5.1, -2.9), (0.06, 1.9, 1.9),
                          mat("cream"), bevel=0.02))
    # cowcatcher: flattened cone + rib fins (child-readable per sheet)
    o.append(prim_cyl("cow", (0, 1.3, 5.1), 0.2, 2.1, 1.9, navy, axis="Z",
                      scale_g=(1.0, 0.55, 1.0)))
    for i in range(5):
        fx = -1.4 + i * 0.7
        o.append(prim_box(f"fin{i}", (fx, 1.05, 5.35), (0.16, 1.15, 0.9),
                          navy, bevel=0.03))
    # couplers, coral-red (sheet identity, front + rear)
    o.append(prim_box("coup_f", (0, 1.5, 6.05), (0.7, 0.5, 0.5),
                      mat("coupler_red"), bevel=0.05))
    o.append(prim_box("coup_r", (0, 1.5, -4.45), (0.7, 0.5, 0.5),
                      mat("coupler_red"), bevel=0.05))
    fuse_and_export(o, "loco_body", single_mesh=False)


# ============================================================ track builders
SEG_L = 5.013          # ring circumference / 240
RAIL_X = 1.55
RAIL_W = 0.34
RAIL_TOP = 0.30
RAIL_SKIRT = 0.6
TIE = (4.6, 0.2, 1.1)  # w, h, d — tie top at -0.18


def _track_parts(length, n_ties):
    parts = []
    for i, sx in enumerate((-RAIL_X, RAIL_X)):
        # railhead at +0.30, skirt drop 0.6 below it (matches _ring_ribbon)
        parts.append(prim_box(f"rail{i}", (sx, 0.0, 0.0),
                              (RAIL_W, RAIL_SKIRT, length),
                              mat("rail_navy"), bevel=0.05))
    step = length / n_ties
    for i in range(n_ties):
        z = -length * 0.5 + step * (i + 0.5)
        parts.append(prim_box(f"tie{i}", (0, -0.28, z), TIE,
                              mat("tie_lav"), bevel=0.04))
        for j, sx in enumerate((-RAIL_X, RAIL_X)):
            parts.append(prim_box(f"plate{i}_{j}", (sx, RAIL_TOP + 0.03, z),
                                  (0.5, 0.07, 0.34), mat("gold"), bevel=0.02))
    return parts


def build_track_straight():
    reset_scene()
    fuse_and_export(_track_parts(SEG_L, 4), "track_straight", single_mesh=True)


def build_track_curve():
    reset_scene()
    r = 12.0
    arc = r * math.pi * 0.5
    parts = _track_parts(arc, 10)
    # subdivide along length so the bend is smooth, then bend 90 deg about Z.
    dg = bpy.context.evaluated_depsgraph_get()
    fused = bpy.data.meshes.new("curve_src")
    bm = bmesh.new()
    slots, spans = [], []
    for ob in parts:
        ev = bpy.data.meshes.new_from_object(ob.evaluated_get(dg), depsgraph=dg)
        ev.transform(ob.matrix_world)
        base = len(slots)
        for m in (ev.materials if ev.materials else [None]):
            slots.append(m)
        for p in ev.polygons:
            p.material_index += base
        bm.from_mesh(ev)
        bpy.data.meshes.remove(ev)
        bpy.data.objects.remove(ob)
    bmesh.ops.subdivide_edges(
        bm, edges=[e for e in bm.edges
                   if abs(e.verts[0].co.y - e.verts[1].co.y) > 0.5],
        cuts=18, use_grid_fill=True)
    # bend: map y (along track, -arc/2..arc/2) to angle about a center at x=-r
    for v in bm.verts:
        ang = v.co.y / r
        rad = r + v.co.x
        v.co = Vector((rad * math.cos(ang) - r, rad * math.sin(ang), v.co.z))
    # shift origin to the entry end (y = -arc/2 end was bent to angle -arc/2r)
    a0 = -arc * 0.5 / r
    entry = Vector((r * math.cos(a0) - r, r * math.sin(a0), 0.0))
    ent_rot = Matrix.Rotation(-a0, 4, "Z")
    bm.transform(Matrix.Translation(-entry))
    bm.transform(ent_rot)
    bm.to_mesh(fused)
    bm.free()
    remap, final = {}, []
    for i, m in enumerate(slots):
        if m in final:
            remap[i] = final.index(m)
        else:
            remap[i] = len(final)
            final.append(m)
    for m in final:
        fused.materials.append(m)
    for p in fused.polygons:
        p.material_index = remap.get(p.material_index, 0)
    new_obj("track_curve", fused)
    fuse_and_export([bpy.data.objects["track_curve"]], "track_curve",
                    single_mesh=False)


# ========================================================== r021D platform
def build_platform():
    reset_scene()
    L, W, H = 12.0, 5.2, 1.1
    o = []
    o.append(prim_box("skirt", (0, H * 0.42, 0), (W - 0.3, H * 0.84, L - 0.3),
                      mat("skirt_lav"), bevel=0.08))
    o.append(prim_box("deck", (0, H - 0.09, 0), (W, 0.18, L),
                      mat("deck_teal"), bevel=0.06))
    # cream rim border
    for i, sx in enumerate((-1.0, 1.0)):
        o.append(prim_box(f"rimx{i}", (sx * (W * 0.5 - 0.22), H + 0.03, 0),
                          (0.44, 0.26, L), mat("cream"), bevel=0.06))
    for i, sz in enumerate((-1.0, 1.0)):
        o.append(prim_box(f"rimz{i}", (0, H + 0.03, sz * (L * 0.5 - 0.22)),
                          (W - 0.88, 0.26, 0.44), mat("cream"), bevel=0.06))
    for i, (sx, sz) in enumerate(((-1, -1), (-1, 1), (1, -1), (1, 1))):
        o.append(prim_box(f"cap{i}", (sx * (W * 0.5 - 0.3), H + 0.06,
                                      sz * (L * 0.5 - 0.3)),
                          (0.62, 0.34, 0.62), mat("gold"), bevel=0.10))
    # boarding steps on +X side (placed away from the rails at runtime)
    for i in range(2):
        o.append(prim_box(f"step{i}", (W * 0.5 + 0.35 + i * 0.0, 0.28 + i * 0.38,
                                       -2.2), (0.75, 0.24, 2.2),
                          mat("cream") if i else mat("deck_teal"), bevel=0.05))
    o.append(prim_box("tag", (0, H + 0.08, 0.0), (0.8, 0.12, 0.4),
                      mat("coupler_red"), bevel=0.03))
    fuse_and_export(o, "station_platform", single_mesh=False)


# ========================================================== r021E shelter
def build_shelter():
    reset_scene()
    o = []
    px, pz, ph = 1.8, 1.2, 5.2       # post rect half-extents, post height
    for i, (sx, sz) in enumerate(((-1, -1), (-1, 1), (1, -1), (1, 1))):
        o.append(prim_cyl(f"post{i}", (sx * px, ph * 0.5, sz * pz),
                          0.14, 0.17, ph, mat("post_aqua"), verts=10))
        o.append(prim_box(f"foot{i}", (sx * px, 0.14, sz * pz),
                          (0.55, 0.28, 0.55), mat("cream"), bevel=0.05))
        o.append(prim_box(f"cap{i}", (sx * px, ph - 0.06, sz * pz),
                          (0.4, 0.22, 0.4), mat("cream"), bevel=0.04))
    # low rear rail (sheet: optional, keeps three sides open)
    o.append(prim_box("rear_rail", (-px, 1.15, 0), (0.16, 0.16, pz * 2),
                      mat("post_aqua"), bevel=0.03))
    # gently arched roof: wide flat cylinder wedge, purple, cream eaves
    o.append(prim_cyl("roof", (0, ph + 0.42, 0), 3.4, 3.4, 4.6,
                      mat("roof_purple"), axis="Z", verts=28,
                      scale_g=(0.68, 0.26, 1.0)))
    for i, sx in enumerate((-1.0, 1.0)):
        o.append(prim_box(f"eave{i}", (sx * 2.25, ph + 0.30, 0),
                          (0.34, 0.3, 4.7), mat("cream"), bevel=0.08))
    o.append(prim_box("finial", (0, ph + 1.42, 0), (0.5, 0.42, 0.5),
                      mat("gold"), bevel=0.12))
    fuse_and_export(o, "station_shelter", single_mesh=False)


# ---------------------------------------------------------------- main
os.makedirs(OUT_DIR, exist_ok=True)
build_coral()
build_kelp()
build_loco()
build_track_straight()
build_track_curve()
build_platform()
build_shelter()
print("ALL KIT PIECES BUILT")
