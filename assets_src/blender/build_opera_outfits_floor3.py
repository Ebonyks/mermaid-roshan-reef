#!/usr/bin/env python3
"""Opera job 3D batch 9 — Floor 3 outfit kits (painter, astronaut, racer,
pop star) completing all twelve careers, plus the pop star's pearl
StarMicrophone stand. Piece* contract on the set_costume bone anchors."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, SILVER)
import bpy, math

S.QA = os.path.join(ROOT, "assets_src/blender/qa_outfits_floor3")
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
BERET = mat("beret_blue", (0.35, 0.5, 0.8))
GLASSH = mat("helmet_glass", (0.8, 0.92, 1.0), alpha=0.35)
SUIT = mat("suit_silver", (0.78, 0.82, 0.9))
HELMET_R = mat("helmet_red", (0.9, 0.32, 0.3))
VISOR = mat("visor_blue", (0.45, 0.75, 0.95), emission=0.3)
STARGOLD = mat("star_gold", (1.0, 0.85, 0.35), emission=0.5)
MIC_PINK = mat("mic_pink", (0.9, 0.5, 0.85))

def painter_kit():
    kit = empty("OperaPainterOutfit")
    head = empty("PieceHead", kit)
    b = cyl("Beret", BERET, head, r=1.15, depth=0.4, loc=(0.25, 0, 2.45), verts=20)
    b.rotation_euler = (0, math.radians(-12), 0)
    sph("BeretPuff", PEARL, head, r=0.16, loc=(0.5, 0, 2.75), seg=8, rings=5)
    hand = empty("PieceHandR", kit)
    cyl("Brush", mat("brush_wood", (0.6, 0.42, 0.28)), hand, r=0.09, depth=1.1, loc=(0, 0, 0.2))
    cyl("Ferrule", BRASS, hand, r=0.11, depth=0.16, loc=(0, 0, 0.82))
    sph("Tip", CORAL, hand, r=0.2, loc=(0, 0, 1.0), scale=(1, 1, 1.4), seg=8, rings=5)
    hand_l = empty("PieceHandL", kit)
    p = cyl("Palette", CREAM, hand_l, r=0.75, depth=0.12, loc=(0, 0, 0.3), verts=20)
    p.scale = (1.0, 0.8, 1.0)
    for k, m in enumerate([PLUM, CORAL, TEAL]):
        sph("Dab%d" % k, m, hand_l, r=0.16,
            loc=(0.3 * math.cos(k * 2.1), 0.25 * math.sin(k * 2.1), 0.42), scale=(1, 1, 0.4), seg=8, rings=5)
    return kit

def astronaut_kit():
    kit = empty("OperaAstronautOutfit")
    head = empty("PieceHead", kit)
    torus("Collar", SUIT, head, R=0.95, r=0.22, loc=(0, 0, -0.55))
    sph("Helmet", GLASSH, head, r=1.3, loc=(0, 0, 1.2), seg=18, rings=12)
    torus("HelmetRim", BRASS, head, R=1.28, r=0.08, loc=(0, 0, 1.2), rot=(math.radians(12), 0, 0))
    chest = empty("PieceChest", kit)
    for sx in (-1, 1):
        cyl("Tank%d" % sx, SUIT, chest, r=0.35, depth=1.4, loc=(sx * 0.5, 0.85, -0.2))
        sph("TankCap%d" % sx, CORAL, chest, r=0.36, loc=(sx * 0.5, 0.85, 0.55), scale=(1, 1, 0.5), seg=10, rings=6)
    box("Strap", SUIT, chest, size=(1.5, 0.16, 0.3), loc=(0, 0.6, 0.2))
    return kit

def racer_kit():
    kit = empty("OperaRacerOutfit")
    head = empty("PieceHead", kit)
    sph("Helmet", HELMET_R, head, r=1.05, loc=(0, 0, 1.75), scale=(1, 1, 0.9))
    box("Visor", VISOR, head, size=(1.45, 0.35, 0.55), loc=(0, -1.0, 1.5))
    box("BrimStripe", CREAM, head, size=(0.3, 2.0, 0.14), loc=(0, 0, 2.65))
    hand = empty("PieceHandR", kit)
    w = empty("Wheel", hand, (0, 0, 0.35))
    w.rotation_euler = (math.radians(90), 0, 0)
    torus("WheelRim", mat("wheel_dark", (0.25, 0.25, 0.35)), w, R=0.62, r=0.12)
    for k in range(3):
        box("Spoke%d" % k, SILVER, w, size=(0.1, 1.1, 0.1), rot=(0, 0, k * math.tau / 6))
    sph("Hub", BRASS, w, r=0.16, seg=8, rings=5)
    return kit

def popstar_kit():
    kit = empty("OperaPopstarOutfit")
    head = empty("PieceHead", kit)
    for sx in (-1, 1):   # star glasses at eye level, pushed clear of the face
        st = empty("Star%d" % sx, head, (sx * 0.45, -1.15, 1.2))
        for k in range(5):
            a = k / 5.0 * math.tau + math.pi / 2
            sph("Pt", STARGOLD, st, r=0.14,
                loc=(math.cos(a) * 0.3, 0, math.sin(a) * 0.3), scale=(1, 0.5, 1), seg=8, rings=5)
        sph("StarC", STARGOLD, st, r=0.2, scale=(1, 0.5, 1), seg=8, rings=5)
    box("Bridge", STARGOLD, head, size=(0.5, 0.12, 0.12), loc=(0, -1.18, 1.2))
    hand = empty("PieceHandR", kit)
    cyl("MicHandle", SILVER, hand, r=0.11, depth=0.9, loc=(0, 0, 0.05))
    sph("MicBall", MIC_PINK, hand, r=0.4, loc=(0, 0, 0.7), seg=12, rings=8)
    torus("MicRing", BRASS, hand, R=0.4, r=0.05, loc=(0, 0, 0.6))
    return kit

def star_microphone():
    root = empty("OperaStarMicrophone")
    vis = empty("Visual", root)
    cyl("Base", PLUM, vis, r=1.3, depth=0.4, loc=(0, 0, 0.2), verts=20)
    torus("BaseTrim", BRASS, vis, R=1.28, r=0.07, loc=(0, 0, 0.4))
    cyl("Stand", SILVER, vis, r=0.12, depth=3.6, loc=(0, 0, 2.2))
    sph("MicBall", PEARL, vis, r=0.75, loc=(0, 0, 4.2), seg=14, rings=10)
    torus("MicRing", BRASS, vis, R=0.72, r=0.08, loc=(0, 0, 4.0), rot=(math.radians(20), 0, 0))
    st_a = empty("StateActive", vis)
    torus("GlowRing", STARGOLD, st_a, R=1.0, r=0.09, loc=(0, 0, 4.2))
    shell_clasp(vis, (0, -1.25, 0.35), s=1.1)
    return root

for name, builder, folder in [("painter", painter_kit, "painter"),
                              ("astronaut", astronaut_kit, "astronaut"),
                              ("racer", racer_kit, "racer"),
                              ("popstar", popstar_kit, "popstar")]:
    S.OUT = os.path.join(ROOT, "assets/opera/jobs/%s" % folder)
    os.makedirs(S.OUT, exist_ok=True)
    kit = builder()
    export_glb(kit, "opera_%s_outfit.glb" % folder)
    qa_render([kit], name + "_outfit")
    kit.location = (0, 25, 0)
S.OUT = os.path.join(ROOT, "assets/opera/jobs/popstar")
m = star_microphone()
export_glb(m, "opera_popstar_microphone.glb")
qa_render([m], "microphone")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_outfits_floor3_2026-07-22.blend"))
print("DONE")
