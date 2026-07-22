#!/usr/bin/env python3
"""Opera job 3D batch 4 — Candy Maker mechanic props.

The gazebo press machine (coral dome, shell+pearl finial, gold columns,
pearl-studded base) with a PressBlock node the existing stamp tween drives,
plus SEVEN candies with different outer silhouettes per the accepted cards:
scallop round, shell, wrapped bonbon, drop, flower, button, bow."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, CORAL_L)
import bpy, math

S.OUT = os.path.join(ROOT, "assets/opera/jobs/candymaker")
S.QA = os.path.join(ROOT, "assets_src/blender/qa_candymaker")
os.makedirs(S.OUT, exist_ok=True)
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
TEAL_L = mat("teal_l2", (0.55, 0.82, 0.8))
PLUM_L = mat("plum_l2", (0.68, 0.5, 0.78))
CANDY_CORAL = mat("candy_coral", (0.93, 0.45, 0.42))

def press():
    root = empty("OperaCandyPress")
    vis = empty("Visual", root)
    # pearl-studded pedestal base + stamping table
    cyl("Base", CORAL, vis, r=4.4, depth=0.9, loc=(0, 0, 0.45), verts=28)
    torus("BaseTrim", BRASS, vis, R=4.35, r=0.12, loc=(0, 0, 0.9))
    for k in range(8):
        a = k / 8.0 * math.tau
        sph("BasePearl%d" % k, PEARL, vis, r=0.28,
            loc=(math.cos(a) * 4.1, math.sin(a) * 4.1, 0.5), seg=10, rings=6)
    cyl("Table", CREAM, vis, r=2.1, depth=0.6, loc=(0, 0, 1.2), verts=24)
    torus("TableTrim", BRASS, vis, R=2.05, r=0.08, loc=(0, 0, 1.5))
    # four gold columns + valance + coral dome with shell finial
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl("Col", BRASS, vis, r=0.28, depth=5.6, loc=(sx * 2.9, sy * 2.9, 3.7))
    cyl("Valance", TEAL, vis, r=3.9, depth=0.55, loc=(0, 0, 6.4), verts=28)
    for k in range(10):
        a = k / 10.0 * math.tau
        sph("Scallop%d" % k, CORAL_L, vis, r=0.42,
            loc=(math.cos(a) * 3.75, math.sin(a) * 3.75, 6.1), scale=(1, 1, 0.6), seg=10, rings=6)
    sph("Dome", CORAL, vis, r=3.8, loc=(0, 0, 6.7), scale=(1, 1, 0.55))
    shell_clasp(vis, (0, -3.0, 7.6), s=1.6)
    sph("Finial", PEARL, vis, r=0.42, loc=(0, 0, 8.9))
    # side crank per the cards (decorative; the act's PRESS button is the verb)
    crank = empty("Crank", vis, (3.6, 0, 4.6))
    cyl("CrankArm", BRASS, crank, r=0.14, depth=1.6, loc=(0.55, 0, 0.55), rot=(0, math.radians(50), 0))
    sph("CrankBall", CANDY_CORAL, crank, r=0.45, loc=(1.15, 0, 1.1))
    # the descending stamp: a DIRECT child so the act's tween drives it
    blockp = empty("PressBlock", root, (0, 0, 5.3))
    cyl("Shaft", BRASS, blockp, r=0.4, depth=1.8, loc=(0, 0, 0.9))
    cyl("Plate", CANDY_CORAL, blockp, r=1.8, depth=0.7, loc=(0, 0, -0.35), verts=24)
    torus("PlateTrim", BRASS, blockp, R=1.75, r=0.08, loc=(0, 0, -0.7))
    empty("TouchTarget", root, (0, 0, 2.4))
    empty("FXAnchor", root, (0, 0, 2.6))
    return root

def candy(i):
    root = empty("OperaCandy%d" % i)
    vis = empty("Visual", root)
    if i == 0:      # coral scalloped round
        sph("Body", CANDY_CORAL, vis, r=1.25, scale=(1, 1, 0.75))
        for k in range(8):
            a = k / 8.0 * math.tau
            sph("Sc%d" % k, CANDY_CORAL, vis, r=0.4,
                loc=(math.cos(a) * 1.15, math.sin(a) * 1.15, 0), seg=10, rings=6)
    elif i == 1:    # teal shell
        for k in range(5):
            a = math.radians(-44 + k * 22)
            sph("Rib%d" % k, TEAL_L, vis, r=0.5,
                loc=(math.sin(a) * 0.85, 0, 0.35 + math.cos(a) * 0.75),
                scale=(0.75, 0.55, 1.5), seg=10, rings=6)
        sph("Hinge", TEAL_L, vis, r=0.45, loc=(0, 0, -0.7), scale=(1, 0.6, 0.8))
    elif i == 2:    # plum wrapped bonbon
        sph("Body", PLUM_L, vis, r=1.05)
        for sx in (-1, 1):
            c = obj_cone(vis, sx)
    elif i == 3:    # cream drop with a soft point
        sph("Body", CREAM, vis, r=1.1, scale=(1, 1, 1.15))
        sph("Tip", CREAM, vis, r=0.45, loc=(0, 0, 1.15), scale=(1, 1, 1.4), seg=10, rings=6)
    elif i == 4:    # coral flower cluster
        sph("Core", CANDY_CORAL, vis, r=0.7)
        for k in range(6):
            a = k / 6.0 * math.tau
            sph("Petal%d" % k, CANDY_CORAL, vis, r=0.62,
                loc=(math.cos(a) * 0.95, math.sin(a) * 0.95, 0), seg=10, rings=6)
    elif i == 5:    # teal button
        sph("Body", TEAL_L, vis, r=1.25, scale=(1, 1, 0.6))
        torus("Ring", TEAL, vis, R=0.75, r=0.14, loc=(0, 0, 0.55))
    else:           # plum bow
        for sx in (-1, 1):
            sph("Loop%d" % sx, PLUM_L, vis, r=0.75, loc=(sx * 0.8, 0, 0.1),
                scale=(1.15, 0.7, 0.8), seg=10, rings=6)
        sph("Knot", PLUM_L, vis, r=0.42)
        for sx in (-1, 1):
            box("Tail%d" % sx, PLUM_L, vis, size=(0.5, 0.35, 1.0),
                loc=(sx * 0.45, 0, -0.85), rot=(0, sx * 0.4, 0))
    return root

def obj_cone(vis, sx):
    import bpy as _b
    _b.ops.mesh.primitive_cone_add(radius1=0.55, radius2=0.15, depth=0.9,
                                   vertices=12, location=(sx * 1.35, 0, 0),
                                   rotation=(0, sx * math.pi / 2, 0))
    o = _b.context.active_object
    o.name = "Wrap%d" % sx
    o.data.materials.append(PLUM_L)
    o.parent = vis
    for p in o.data.polygons:
        p.use_smooth = True
    return o

pr = press()
export_glb(pr, "opera_candymaker_press.glb")
qa_render([pr], "press")
built = []
for i in range(7):
    c = candy(i)
    c.location = ((i - 3) * 3.2, 10, 1.2)
    export_glb(c, "opera_candymaker_candy_%d.glb" % i)
    built.append(c)
qa_render(built, "candies")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_candymaker_2026-07-22.blend"))
print("DONE")
