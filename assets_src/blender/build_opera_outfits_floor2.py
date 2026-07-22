#!/usr/bin/env python3
"""Opera outfit kits, Floor 2 — doctor, farmer, boxer, magician.

Piece* contract for player.set_costume bone anchors. Head pieces span
+2.2..+3.6 over the eye-level head joint; face-adjacent pieces push
Blender -Y (her front); hand pieces sit around the hand joint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, SILVER)
import bpy, math

S.QA = os.path.join(ROOT, "assets_src/blender/qa_outfits_floor2")
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
STRAW = mat("straw", (0.9, 0.78, 0.48))
CARROT = mat("carrot", (0.95, 0.5, 0.2))
LEAF = mat("leaf", (0.45, 0.75, 0.4))
GLOVE = mat("glove_red", (0.85, 0.28, 0.32))
BELT_GOLD = mat("belt_gold", (1.0, 0.85, 0.4), emission=0.4)
PLUM_HAT = mat("plum_hat", (0.36, 0.24, 0.55))
SCOPE = mat("scope_navy", (0.35, 0.4, 0.55))

def doctor_kit():
    kit = empty("OperaDoctorOutfit")
    head = empty("PieceHead", kit)
    torus("MirrorBand", CREAM, head, R=0.95, r=0.12, loc=(0, 0, 1.75), scale=(1, 1, 0.6))
    cyl("Mirror", BRASS, head, r=0.34, depth=0.1, loc=(0, -0.95, 1.95), rot=(math.radians(75), 0, 0))
    sph("MirrorGem", PEARL, head, r=0.14, loc=(0, -1.0, 1.98), seg=8, rings=5)
    chest = empty("PieceChest", kit)
    t = torus("ScopeLoop", SCOPE, chest, R=0.72, r=0.09, loc=(0, -0.5, 0.7),
              rot=(math.radians(80), 0, 0))
    cyl("ScopeStem", SCOPE, chest, r=0.08, depth=0.7, loc=(0, -0.8, 0.15), rot=(math.radians(15), 0, 0))
    cyl("ChestPad", CREAM, chest, r=0.32, depth=0.14, loc=(0, -0.9, -0.2), rot=(math.radians(80), 0, 0))
    hand = empty("PieceHandR", kit)
    torus("Roll", CREAM, hand, R=0.4, r=0.2, loc=(0, 0, 0.35), rot=(math.radians(90), 0, 0))
    return kit

def farmer_kit():
    kit = empty("OperaFarmerOutfit")
    head = empty("PieceHead", kit)
    cyl("Brim", STRAW, head, r=1.55, depth=0.18, loc=(0, 0, 2.3), verts=24)
    cyl("Crown", STRAW, head, r=0.9, depth=0.7, loc=(0, 0, 2.7), verts=20)
    sph("CrownTop", STRAW, head, r=0.9, loc=(0, 0, 3.05), scale=(1, 1, 0.35))
    torus("HatBand", CORAL, head, R=0.92, r=0.09, loc=(0, 0, 2.5))
    hand = empty("PieceHandR", kit)
    c = bpy.ops.mesh.primitive_cone_add(radius1=0.38, radius2=0.05, depth=1.1,
                                        vertices=12, location=(0, 0, 0.15))
    o = bpy.context.active_object
    o.name = "Carrot"
    o.data.materials.append(CARROT)
    o.parent = hand
    for p in o.data.polygons:
        p.use_smooth = True
    for k in range(3):
        sph("Leaf%d" % k, LEAF, hand, r=0.16,
            loc=(0.12 * math.sin(k * 2.1), 0.12 * math.cos(k * 2.1), 0.85),
            scale=(0.6, 0.6, 1.6), seg=8, rings=5)
    return kit

def boxer_kit():
    kit = empty("OperaBoxerOutfit")
    for pname, side in [("PieceHandR", -1), ("PieceHandL", 1)]:
        hand = empty(pname, kit)
        sph("Glove", GLOVE, hand, r=0.62, scale=(0.95, 1.0, 1.05))
        sph("GloveThumb", GLOVE, hand, r=0.28, loc=(side * -0.45, -0.25, -0.1), seg=10, rings=6)
        torus("Cuff", CREAM, hand, R=0.42, r=0.14, loc=(0, 0.35, -0.45),
              rot=(math.radians(75), 0, 0))
    waist = empty("PieceWaist", kit)
    torus("BeltStrap", GLOVE, waist, R=0.95, r=0.22, loc=(0, 0, -0.1), scale=(1, 1, 0.7))
    sph("BeltPlate", BELT_GOLD, waist, r=0.5, loc=(0, -0.85, -0.1), scale=(1, 0.35, 0.85), seg=12, rings=8)
    shell_clasp(waist, (0, -1.0, 0.12), s=0.8)
    return kit

def magician_kit():
    kit = empty("OperaMagicianOutfit")
    head = empty("PieceHead", kit)
    cyl("Brim", PLUM_HAT, head, r=1.3, depth=0.18, loc=(0, 0, 2.3), verts=24)
    cyl("Crown", PLUM_HAT, head, r=0.85, depth=1.35, loc=(0, 0, 3.05), verts=20)
    torus("HatBand", TEAL, head, R=0.87, r=0.1, loc=(0, 0, 2.6))
    sph("BandPearl", PEARL, head, r=0.13, loc=(0, -0.88, 2.6), seg=8, rings=5)
    chest = empty("PieceChest", kit)
    for sx in (-1, 1):
        sph("TieLoop%d" % sx, TEAL, chest, r=0.3, loc=(sx * 0.35, -0.85, 0.7),
            scale=(1.1, 0.5, 0.6), seg=10, rings=6)
    sph("TieKnot", PEARL, chest, r=0.14, loc=(0, -0.9, 0.7), seg=8, rings=5)
    hand = empty("PieceHandR", kit)
    cyl("Wand", CREAM, hand, r=0.07, depth=1.15, loc=(0, 0, 0.3))
    cyl("WandTip", PLUM_HAT, hand, r=0.075, depth=0.3, loc=(0, 0, 0.75))
    sph("WandStar", PEARL, hand, r=0.16, loc=(0, 0, 0.95), seg=8, rings=5)
    return kit

for name, builder, folder in [("doctor", doctor_kit, "doctor"),
                              ("farmer", farmer_kit, "farmer"),
                              ("boxer", boxer_kit, "boxer"),
                              ("magician", magician_kit, "magician")]:
    S.OUT = os.path.join(ROOT, "assets/opera/jobs/%s" % folder)
    os.makedirs(S.OUT, exist_ok=True)
    kit = builder()
    export_glb(kit, "opera_%s_outfit.glb" % folder)
    qa_render([kit], name + "_outfit")
    kit.location = (0, 25, 0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_outfits_floor2_2026-07-22.blend"))
print("DONE")
