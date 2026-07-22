#!/usr/bin/env python3
"""Opera job 3D batch 3 — Detective mechanic props.

Six search boxes with DIFFERENT silhouettes (jewel box, quilted box, round
hatbox, steamer trunk, ribbon box, crate) each with a separately-tweenable
Lid node, plus the tiara chest with StateIdle/StateActive/StateComplete
(locked -> ready glow -> open with the pearl tiara risen)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, CORAL_L)
import bpy, math

S.OUT = os.path.join(ROOT, "assets/opera/jobs/detective")
S.QA = os.path.join(ROOT, "assets_src/blender/qa_detective")
os.makedirs(S.OUT, exist_ok=True)
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
TEAL_D = mat("teal_d", (0.24, 0.48, 0.5))
PLUM_D = mat("plum_d", (0.45, 0.3, 0.55))
WOODY = mat("woody", (0.72, 0.5, 0.36))
READY = mat("chest_ready", (1.0, 0.88, 0.45), emission=1.6)

def base_feet(parent, hw, hd):
    for sx in (-1, 1):
        for sy in (-1, 1):
            sph("Foot", BRASS, parent, r=0.22, loc=(sx * hw, sy * hd, 0.12),
                scale=(1, 1, 0.7), seg=10, rings=6)

def search_box(i):
    """Body under Visual; Lid is a DIRECT child of root so opera_act's
    open tween (position up + z-tilt) drives it exactly like the primitive."""
    root = empty("OperaDetectiveBox%d" % i)
    vis = empty("Visual", root)
    lid = empty("Lid", root)
    if i == 0:      # coral square jewel box, gold corners
        box("Body", CORAL, vis, size=(2.5, 2.5, 1.8), loc=(0, 0, 1.05))
        base_feet(vis, 1.0, 1.0)
        for sx in (-1.2, 1.2):
            box("Corner", BRASS, vis, size=(0.22, 2.55, 0.5), loc=(sx, 0, 0.42))
        shell_clasp(vis, (0, -1.3, 1.1), s=1.3)
        box("LidTop", CORAL_L, lid, size=(2.7, 2.7, 0.55), loc=(0, 0, 2.2))
        torus("LidTrim", BRASS, lid, R=1.35, r=0.06, loc=(0, 0, 1.95), scale=(1, 1, 0.4))
    elif i == 1:    # teal quilted box, scalloped skirt
        box("Body", TEAL, vis, size=(2.4, 2.4, 1.7), loc=(0, 0, 1.0))
        for k in range(8):
            a = k / 8.0 * math.tau
            sph("Scal", TEAL_D, vis, r=0.35, loc=(math.cos(a) * 1.15, math.sin(a) * 1.15, 0.22),
                scale=(1, 1, 0.5), seg=10, rings=6)
        shell_clasp(vis, (0, -1.25, 1.15), s=1.2)
        box("LidTop", TEAL_D, lid, size=(2.6, 2.6, 0.5), loc=(0, 0, 2.05))
        sph("LidPearl", PEARL, lid, r=0.2, loc=(0, 0, 2.35))
    elif i == 2:    # plum round hatbox
        cyl("Body", PLUM, vis, r=1.5, depth=1.6, loc=(0, 0, 0.95))
        base_feet(vis, 0.95, 0.95)
        shell_clasp(vis, (0, -1.55, 0.95), s=1.2)
        cyl("LidTop", PLUM_D, lid, r=1.62, depth=0.45, loc=(0, 0, 1.95))
        sph("LidDome", PLUM_D, lid, r=1.55, loc=(0, 0, 2.1), scale=(1, 1, 0.28))
    elif i == 3:    # cream steamer trunk, coral straps
        box("Body", CREAM, vis, size=(3.1, 2.1, 1.7), loc=(0, 0, 1.0))
        for sx in (-0.9, 0.9):
            box("Strap", CORAL, vis, size=(0.35, 2.2, 1.8), loc=(sx, 0, 1.0))
        shell_clasp(vis, (0, -1.1, 1.15), s=1.2)
        lidm = cyl("LidTop", CREAM, lid, r=1.05, depth=3.1,
                   loc=(0, 0, 1.9), rot=(0, math.pi / 2, 0), verts=20)
        lidm.scale = (0.55, 1.0, 1.0)
        for sx in (-0.9, 0.9):
            b = cyl("LidStrap", CORAL, lid, r=1.12, depth=0.36,
                    loc=(sx, 0, 1.9), rot=(0, math.pi / 2, 0), verts=20)
            b.scale = (0.55, 1.0, 1.0)
    elif i == 4:    # coral round ribbon box with teal band + bow
        cyl("Body", CORAL, vis, r=1.45, depth=1.5, loc=(0, 0, 0.9))
        cyl("Band", TEAL, vis, r=1.47, depth=0.45, loc=(0, 0, 0.65))
        shell_clasp(vis, (0, -1.5, 0.7), s=1.1)
        cyl("LidTop", CORAL, lid, r=1.55, depth=0.4, loc=(0, 0, 1.8))
        for sx in (-1, 1):
            sph("Bow", TEAL, lid, r=0.45, loc=(sx * 0.5, -1.2, 1.9),
                scale=(1.1, 0.5, 0.6), seg=10, rings=6)
        sph("Knot", PEARL, lid, r=0.18, loc=(0, -1.25, 1.92))
    else:           # red/teal crate with X planks
        box("Body", TEAL_D, vis, size=(2.4, 2.4, 2.2), loc=(0, 0, 1.25))
        for sgn in (-1, 1):
            box("Cross", CORAL, vis, size=(0.32, 0.34, 3.0),
                loc=(0, -1.22, 1.25), rot=(0, sgn * 0.7, 0))
        for e in (-1, 1):
            box("Edge", CORAL, vis, size=(2.6, 2.6, 0.3), loc=(0, 0, 1.25 + e * 1.05))
        shell_clasp(vis, (0, -1.35, 1.25), s=1.1)
        box("LidTop", CORAL, lid, size=(2.6, 2.6, 0.35), loc=(0, 0, 2.5))
    empty("TouchTarget", root, (0, 0, 1.2))
    empty("FXAnchor", root, (0, 0, 2.8))
    return root

def tiara(parent, loc):
    t = empty("Tiara", parent, loc)
    for k in range(7):
        a = math.radians(-54 + k * 18)
        h = 0.55 + 0.35 * math.cos(a * 1.6)
        sph("TiaraPearl%d" % k, PEARL, t, r=0.16 + (0.08 if k == 3 else 0),
            loc=(math.sin(a) * 1.05, 0, h), seg=10, rings=6)
    torus("TiaraBase", BRASS, t, R=1.05, r=0.09, loc=(0, 0, 0.1), scale=(1, 0.55, 1))
    shell_clasp(t, (0, -0.18, 0.28), s=0.9)
    return t

def chest():
    root = empty("OperaDetectiveChest")
    vis = empty("Visual", root)
    body = empty("Shell", vis)
    box("Body", TEAL, body, size=(3.6, 2.4, 1.9), loc=(0, 0, 1.1))
    for sx in (-1.3, 1.3):
        box("Strap", BRASS, body, size=(0.3, 2.5, 2.0), loc=(sx, 0, 1.1))
    base_feet(body, 1.5, 1.0)
    shell_clasp(body, (0, -1.25, 1.2), s=1.5)
    st_i = empty("StateIdle", vis)
    lid_c = empty("LidClosedHinge", st_i, (0, 1.2, 2.05))    # real rear hinge
    lidm = cyl("LidC", TEAL_D, lid_c, r=1.2, depth=3.6,
               loc=(0, -1.2, 0), rot=(0, math.pi / 2, 0), verts=20)
    lidm.scale = (0.55, 1, 1)
    for sx in (-1.3, 1.3):
        b = cyl("LidStrapC", BRASS, lid_c, r=1.26, depth=0.32,
                loc=(sx, -1.2, 0), rot=(0, math.pi / 2, 0), verts=20)
        b.scale = (0.55, 1, 1)
    st_a = empty("StateActive", vis)
    torus("ReadyGlow", READY, st_a, R=2.1, r=0.1, loc=(0, 0, 0.25))
    sph("Keyhole", READY, st_a, r=0.22, loc=(0, -1.28, 1.2))
    st_c = empty("StateComplete", vis)
    lid_o = empty("LidOpenHinge", st_c, (0, 1.2, 2.05))
    lid_o.rotation_euler = (math.radians(105), 0, 0)
    lidm2 = cyl("LidO", TEAL_D, lid_o, r=1.2, depth=3.6,
                loc=(0, -1.2, 0), rot=(0, math.pi / 2, 0), verts=20)
    lidm2.scale = (0.55, 1, 1)
    tiara(st_c, (0, 0, 2.8))
    sph("GlowBed", READY, st_c, r=1.5, loc=(0, 0, 2.0), scale=(1, 0.7, 0.25))
    empty("TouchTarget", root, (0, 0, 1.4))
    empty("FXAnchor", root, (0, 0, 3.2))
    empty("PointerAnchor", root, (0, 0, 4.6))
    return root

built = []
for i in range(6):
    r = search_box(i)
    r.location = ((i - 2.5) * 4.6, 0, 0)
    export_glb(r, "opera_detective_box_%d.glb" % i)
    built.append(r)
qa_render(built, "detective_boxes")
ch = chest()
ch.location = (0, 10, 0)
export_glb(ch, "opera_detective_chest.glb")
for st in ("StateIdle", "StateActive", "StateComplete"):
    for c in ch.children:
        if c.name.split(".")[0] == "Visual":
            for s in c.children:
                base = s.name.split(".")[0]
                if base.startswith("State"):
                    def hide(o, h):
                        o.hide_render = h
                        for cc in o.children:
                            hide(cc, h)
                    hide(s, base != st and not (st == "StateComplete" and base == "StateActive"))
    qa_render([ch], "chest_" + st.lower())
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_detective_2026-07-22.blend"))
print("DONE")
