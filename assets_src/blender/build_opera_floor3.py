#!/usr/bin/env python3
"""Opera job 3D batch 8 — Floor 3 mechanic props (painter + astronaut).

Painter: three paint pots in the LOCKED cue palette (coral / cream / plum,
matching order indices 0/1/2 so the live [2,0,1,2] sequence reads
plum-coral-cream-plum) and the gallery easel whose frame leaves the canvas
plane free for the runtime stripe reveals. Astronaut: bubble tank, star
rocket (window zone left open for the live rocket_window), valve wheel kit
that rides the existing spin tween. Blender -Y = stage front."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, SILVER)
import bpy, math

TEAL = mat("teal", (0.31, 0.62, 0.63))
GLASS = mat("tank_glass", (0.55, 0.85, 0.95), alpha=0.55)
BUBBLE = mat("bubble", (0.75, 0.95, 1.0), emission=0.4, alpha=0.6)
ROCKET_C = mat("rocket_cream", (0.92, 0.9, 0.94))
NOSE_C = mat("nose_coral", (0.95, 0.5, 0.45))
WOODE = mat("easel_wood", (0.72, 0.55, 0.4))
POT_COLS = [mat("paint_coral", (0.86, 0.42, 0.38)),
            mat("paint_cream", (0.93, 0.87, 0.78)),
            mat("paint_plum", (0.55, 0.36, 0.66))]

def pot(i):
    root = empty("OperaPainterPot%d" % i)
    vis = empty("Visual", root)
    obj_c = bpy.ops.mesh.primitive_cone_add(radius1=1.0, radius2=1.3, depth=1.5,
                                            vertices=20, location=(0, 0, 0.75))
    o = bpy.context.active_object
    o.name = "PotBody"
    o.data.materials.append(CREAM)
    o.parent = vis
    for p in o.data.polygons:
        p.use_smooth = True
    torus("PotRim", BRASS, vis, R=1.3, r=0.09, loc=(0, 0, 1.5))
    sph("Paint", POT_COLS[i], vis, r=1.18, loc=(0, 0, 1.5), scale=(1, 1, 0.35))
    sph("PaintBlob", POT_COLS[i], vis, r=0.35, loc=(0.75, -0.7, 1.35), scale=(1, 1, 0.5), seg=10, rings=6)
    shell_clasp(vis, (0, -1.2, 0.7), s=1.0)
    return root

def easel():
    root = empty("OperaPainterEasel")
    vis = empty("Visual", root)
    for sx in (-1, 1):
        leg = box("Leg%d" % sx, WOODE, vis, size=(0.35, 0.35, 6.4), loc=(sx * 2.6, 0.5, 3.0))
        leg.rotation_euler = (math.radians(-6), sx * math.radians(-6), 0)
    box("LegBack", WOODE, vis, size=(0.35, 0.35, 6.0), loc=(0, 1.6, 2.9), rot=(math.radians(14), 0, 0))
    box("Tray", WOODE, vis, size=(6.2, 0.7, 0.35), loc=(0, -0.25, 1.1))
    box("TopBar", WOODE, vis, size=(5.6, 0.4, 0.4), loc=(0, 0.1, 5.4))
    # blank canvas board: the runtime stripe reveals draw in FRONT of this
    box("Canvas", mat("canvas_blank", (0.96, 0.94, 0.9)), vis, size=(6.0, 0.25, 4.4), loc=(0, 0.05, 3.2))
    box("Frame", BRASS, vis, size=(6.5, 0.2, 0.3), loc=(0, 0.05, 5.35))
    shell_clasp(vis, (0, -0.4, 5.55), s=1.2)
    return root

def tank():
    root = empty("OperaAstronautTank")
    vis = empty("Visual", root)
    cyl("Glass", GLASS, vis, r=2.2, depth=4.4, loc=(0, 0, 2.2), verts=24)
    for k in range(4):
        sph("Bub%d" % k, BUBBLE, vis, r=0.3 + 0.1 * (k % 2),
            loc=(math.cos(k * 1.7) * 1.1, math.sin(k * 1.7) * 1.1, 1.0 + k * 0.9), seg=10, rings=6)
    torus("BandLo", SILVER, vis, R=2.22, r=0.14, loc=(0, 0, 0.4))
    torus("BandHi", SILVER, vis, R=2.22, r=0.14, loc=(0, 0, 4.1))
    sph("Dome", GLASS, vis, r=2.2, loc=(0, 0, 4.4), scale=(1, 1, 0.55))
    sph("DomeBubble", BUBBLE, vis, r=1.1, loc=(0, 0, 5.0), seg=12, rings=8)
    cyl("Gauge", CREAM, vis, r=0.45, depth=0.2, loc=(0, -2.25, 3.0), rot=(math.radians(90), 0, 0))
    torus("GaugeRim", BRASS, vis, R=0.45, r=0.07, loc=(0, -2.3, 3.0), rot=(math.radians(90), 0, 0))
    return root

def rocket():
    root = empty("OperaAstronautRocket")
    vis = empty("Visual", root)
    cyl("Body", ROCKET_C, vis, r=1.8, depth=6.0, loc=(0, 0, 3.0), verts=24)
    obj_c = bpy.ops.mesh.primitive_cone_add(radius1=1.85, radius2=0.12, depth=2.6,
                                            vertices=20, location=(0, 0, 7.3))
    o = bpy.context.active_object
    o.name = "Nose"
    o.data.materials.append(NOSE_C)
    o.parent = vis
    for p in o.data.polygons:
        p.use_smooth = True
    torus("NoseRing", BRASS, vis, R=1.82, r=0.1, loc=(0, 0, 6.05))
    torus("BaseRing", BRASS, vis, R=1.82, r=0.1, loc=(0, 0, 0.25))
    # window PORT ring only — the live rocket_window sphere sits inside it
    torus("PortRim", BRASS, vis, R=0.95, r=0.14, loc=(0, -1.55, 3.6), rot=(math.radians(80), 0, 0))
    for k in range(3):
        a = k / 3.0 * math.tau + 0.5
        fin = box("Fin%d" % k, NOSE_C, vis, size=(0.3, 1.6, 2.2),
                  loc=(math.cos(a) * 1.9, math.sin(a) * 1.9, 0.9))
        fin.rotation_euler = (0, 0, a + math.pi / 2)
    return root

def valve():
    root = empty("OperaAstronautValve")
    vis = empty("Visual", root)
    cyl("Ped", SILVER, vis, r=0.9, depth=1.6, loc=(0, 0, 0.8))
    wheel = empty("Wheel", vis, (0, 0, 2.0))
    torus("WheelRim", NOSE_C, wheel, R=1.1, r=0.18)
    for k in range(4):
        a = k / 4.0 * math.tau
        box("Spoke%d" % k, SILVER, wheel, size=(0.16, 2.1, 0.16),
            loc=(0, 0, 0), rot=(0, 0, a))
    sph("Hub", BRASS, wheel, r=0.32, seg=10, rings=6)
    return root

S.QA = os.path.join(ROOT, "assets_src/blender/qa_floor3")
os.makedirs(S.QA, exist_ok=True)
S.OUT = os.path.join(ROOT, "assets/opera/jobs/painter")
os.makedirs(S.OUT, exist_ok=True)
built = []
for i in range(3):
    p = pot(i)
    p.location = ((i - 1) * 4.0, 0, 0)
    export_glb(p, "opera_painter_pot_%d.glb" % i)
    built.append(p)
e = easel()
e.location = (0, 8, 0)
export_glb(e, "opera_painter_easel.glb")
built.append(e)
qa_render(built, "painter_family")
for b in built:
    b.location = (0, 40, 0)

S.OUT = os.path.join(ROOT, "assets/opera/jobs/astronaut")
os.makedirs(S.OUT, exist_ok=True)
built2 = []
for builder, fname in [(tank, "opera_astronaut_tank.glb"),
                       (rocket, "opera_astronaut_rocket.glb"),
                       (valve, "opera_astronaut_valve.glb")]:
    r = builder()
    r.location = (len(built2) * 8.0, 0, 0)
    export_glb(r, fname)
    built2.append(r)
qa_render(built2, "astronaut_family")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_floor3_2026-07-22.blend"))
print("DONE")
