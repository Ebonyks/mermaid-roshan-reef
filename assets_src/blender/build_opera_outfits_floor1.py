#!/usr/bin/env python3
"""Opera outfit kits, Floor 1 — ballerina, detective, candy maker.

Card-faithful reversible kits mounted by player.set_costume onto the bone
anchors (Piece* contract). Authored around the anchor origin: head pieces
span +2.2..+3.5 (crown over the eye-level head joint), waist pieces sit at
the spine1 anchor, hand pieces around the hand joint. Blender -Y = her front."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, CORAL_L, SILVER)
import bpy, math

S.QA = os.path.join(ROOT, "assets_src/blender/qa_outfits_floor1")
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
TEAL_L = mat("teal_l3", (0.55, 0.82, 0.8))
BROWNH = mat("brown_hat", (0.55, 0.4, 0.28))
PINKC = mat("pink_candy", (0.95, 0.55, 0.62))
WHITEC = mat("white_candy", (0.96, 0.93, 0.9))

def pearl_tiara(parent, tint):
    t = empty("Tiara", parent, (0, 0, 2.3))
    for k in range(7):
        a = math.radians(-54 + k * 18)
        h = 0.35 + 0.4 * math.cos(a * 1.6)
        sph("TP%d" % k, PEARL, t, r=0.14 + (0.08 if k == 3 else 0),
            loc=(math.sin(a) * 0.8, -0.35, h), seg=10, rings=6)
    torus("TBase", BRASS, t, R=0.82, r=0.07, loc=(0, 0, 0.05), scale=(1, 1, 0.6))
    for k in range(5):
        a = math.radians(-40 + k * 20)
        sph("Shell%d" % k, tint, t, r=0.14, loc=(math.sin(a) * 0.4, -0.72, 0.28 + math.cos(a) * 0.2),
            scale=(0.8, 0.45, 1.4), seg=10, rings=6)
    return t

def ballerina_kit():
    kit = empty("OperaBallerinaOutfit")
    head = empty("PieceHead", kit)
    pearl_tiara(head, CORAL_L)
    chest = empty("PieceChest", kit)
    shell_clasp(chest, (0, -0.95, 0.35), s=1.4)
    waist = empty("PieceWaist", kit)
    for ring, (rr, zz, m, n) in enumerate([(1.5, 0.1, CORAL_L, 10), (1.15, -0.15, CREAM, 8)]):
        for k in range(n):
            a = k / n * math.tau
            sph("Petal%d_%d" % (ring, k), m, waist, r=0.55,
                loc=(math.cos(a) * rr, math.sin(a) * rr, zz),
                scale=(1.0, 1.0, 0.38), seg=10, rings=6)
    torus("Band", BRASS, waist, R=0.95, r=0.08, loc=(0, 0, 0.3))
    for sx in (-1, 1):
        sph("BowLoop%d" % sx, TEAL, waist, r=0.42, loc=(sx * 0.45, 1.35, 0.05),
            scale=(1.1, 0.6, 0.6), seg=10, rings=6)
    sph("BowKnot", PEARL, waist, r=0.18, loc=(0, 1.4, 0.08))
    hand = empty("PieceHandR", kit)
    cyl("WandStick", BRASS, hand, r=0.07, depth=1.1, loc=(0, 0, 0.3))
    for k in range(4):
        sph("Ribbon%d" % k, TEAL_L, hand, r=0.22,
            loc=(0.35 * math.sin(k * 1.9), -0.15 * k, 0.95 + k * 0.32),
            scale=(1.6, 0.5, 0.5), seg=10, rings=6)
    return kit

def detective_kit():
    kit = empty("OperaDetectiveOutfit")
    head = empty("PieceHead", kit)
    cyl("Brim", BROWNH, head, r=1.35, depth=0.2, loc=(0, 0, 2.3))
    sph("Crown", BROWNH, head, r=0.95, loc=(0, 0, 2.55), scale=(1, 1.15, 0.75))
    box("Band", CORAL, head, size=(2.0, 2.0, 0.22), loc=(0, 0, 2.45))
    for sy in (-1, 1):
        sph("Flap", BROWNH, head, r=0.42, loc=(0, sy * 0.95, 2.75), scale=(1, 0.6, 0.9), seg=10, rings=6)
    hand = empty("PieceHandR", kit)
    torus("Lens", BRASS, hand, R=0.5, r=0.1, loc=(0, 0, 0.55))
    cyl("Glass", mat("lens_glass", (0.55, 0.62, 0.75), alpha=0.5), hand,
        r=0.42, depth=0.06, loc=(0, 0, 0.55), rot=(math.pi / 2, 0, 0))
    cyl("MagHandle", CORAL, hand, r=0.11, depth=0.8, loc=(0, 0, -0.25))
    sph("HandleTip", BRASS, hand, r=0.15, loc=(0, 0, -0.68), seg=10, rings=6)
    return kit

def candymaker_kit():
    kit = empty("OperaCandymakerOutfit")
    head = empty("PieceHead", kit)
    for k, m in enumerate([PINKC, WHITEC, PINKC, WHITEC]):
        cyl("Stripe%d" % k, m, head, r=0.95 - k * 0.16, depth=0.42,
            loc=(0, 0, 2.35 + k * 0.4))
    sph("HatTip", PEARL, head, r=0.28, loc=(0, 0, 4.05), seg=10, rings=6)
    hand = empty("PieceHandR", kit)
    cyl("LolliStick", WHITEC, hand, r=0.08, depth=1.2, loc=(0, 0, 0.1))
    cyl("LolliDisc", PINKC, hand, r=0.62, depth=0.2, loc=(0, 0, 0.95), rot=(math.pi / 2, 0, 0))
    torus("LolliSwirl", WHITEC, hand, R=0.34, r=0.07, loc=(0, 0, 0.95), rot=(math.pi / 2, 0, 0))
    return kit

for name, builder, folder in [("ballerina", ballerina_kit, "ballerina"),
                              ("detective", detective_kit, "detective"),
                              ("candymaker", candymaker_kit, "candymaker")]:
    S.OUT = os.path.join(ROOT, "assets/opera/jobs/%s" % folder)
    os.makedirs(S.OUT, exist_ok=True)
    kit = builder()
    kit.location = (0, 0, 0)
    export_glb(kit, "opera_%s_outfit.glb" % folder)
    qa_render([kit], name + "_outfit")
    kit.location = (0, 20, 0)   # park it out of the next render
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_outfits_floor1_2026-07-22.blend"))
print("DONE")
