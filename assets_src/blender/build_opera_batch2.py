#!/usr/bin/env python3
"""Opera job 3D batch 2 — Ballerina dance tiles + Pastry Chef outfit kit.

Tiles pair color AND icon (coral shell / teal wave / plum ribbon / cream
pearl) per the accepted ballerina gameplay cards; the chef outfit kit is the
first card-faithful reversible costume (toque -> PieceHead, whisk ->
PieceHandR) that player.set_costume mounts on the existing bone anchors."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, whisk, ROOT,
                          CREAM, CORAL, PLUM, BRASS, PEARL, SILVER, CORAL_L)
import bpy, math

S.OUT = os.path.join(ROOT, "assets/opera/jobs/ballerina")
S.QA = os.path.join(ROOT, "assets_src/blender/qa_batch2")
os.makedirs(S.OUT, exist_ok=True)
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
TEAL_L = mat("teal_l", (0.55, 0.85, 0.86))
PLUM_L = mat("plum_l", (0.75, 0.58, 0.85))
GLOWY = mat("tile_glow", (1.0, 0.92, 0.6), emission=1.4)

def tile(idx, base_m, icon):
    root = empty("OperaBallerinaTile%d" % idx)
    vis = empty("Visual", root)
    cyl("Disc", base_m, vis, r=3.0, depth=0.6, loc=(0, 0, 0.3), verts=28)
    torus("Rim", BRASS, vis, R=2.95, r=0.09, loc=(0, 0, 0.6))
    ic = empty("Icon", vis, (0, 0, 0.66))
    if icon == "shell":
        for i in range(5):
            a = math.radians(-44 + i * 22)
            sph("Rib%d" % i, CREAM, ic, r=0.42,
                loc=(math.sin(a) * 0.7, 0.5 + math.cos(a) * 0.55, 0.06),
                scale=(0.7, 1.6, 0.25), seg=10, rings=6)
        sph("Hinge", CREAM, ic, r=0.34, loc=(0, -0.25, 0.06), scale=(1, 0.8, 0.3))
    elif icon == "wave":
        for i in range(3):
            torus("Arc%d" % i, CREAM, ic, R=0.55, r=0.11,
                  loc=(-1.0 + i * 1.0, 0.15 * (1 if i % 2 == 0 else -1), 0.06),
                  scale=(1, 1, 0.3))
    elif icon == "ribbon":
        for sx in (-1, 1):
            sph("Bow%d" % sx, CREAM, ic, r=0.55, loc=(sx * 0.62, 0.15, 0.06),
                scale=(1.15, 0.7, 0.28), seg=12, rings=8)
        sph("Knot", CREAM, ic, r=0.26, loc=(0, 0.15, 0.09), scale=(1, 1, 0.4))
        for sx in (-1, 1):
            box("Tail%d" % sx, CREAM, ic, size=(0.32, 0.75, 0.1),
                loc=(sx * 0.35, -0.62, 0.05), rot=(0, 0, sx * 0.5))
    else:  # pearl
        sph("Pearl", PEARL, ic, r=0.62, loc=(0, 0.05, 0.2), scale=(1, 1, 0.55))
        torus("Seat", BRASS, ic, R=0.66, r=0.07, loc=(0, 0.05, 0.05))
    st_a = empty("StateActive", vis)
    torus("GlowRing", GLOWY, st_a, R=2.6, r=0.12, loc=(0, 0, 0.68))
    empty("TouchTarget", root, (0, 0, 0.6))
    empty("FXAnchor", root, (0, 0, 1.4))
    return root

built = []
specs = [(0, CORAL, "shell"), (1, TEAL, "wave"), (2, PLUM_L, "ribbon"), (3, CREAM, "pearl")]
for idx, m, icon in specs:
    r = tile(idx, m, icon)
    r.location = ((idx - 1.5) * 7.0, 0, 0)
    export_glb(r, "opera_ballerina_tile_%d.glb" % idx)
    built.append(r)
qa_render(built, "ballerina_tiles")

# ---------------- Pastry Chef outfit kit (toque + whisk) --------------------
# Pieces are authored around the ANCHOR origin (player bone anchors): the
# toque spans anchor +2.2..+3.6 (head joint = eye level, crown +2.2), the
# whisk hangs around the hand joint. Names are the set_costume contract.
S.OUT = os.path.join(ROOT, "assets/opera/jobs/pastry_chef")
kit = empty("OperaPastryChefOutfit")
head_p = empty("PieceHead", kit)
cyl("ToqueBand", CREAM, head_p, r=0.9, depth=0.55, loc=(0, 0, 2.5))
torus("ToqueTrim", CORAL_L, head_p, R=0.9, r=0.07, loc=(0, 0, 2.28))
sph("ToquePuff", CREAM, head_p, r=1.0, loc=(0, 0, 3.05), scale=(1, 1, 0.85))
sph("PuffLobeL", CREAM, head_p, r=0.5, loc=(-0.62, 0, 2.95))
sph("PuffLobeR", CREAM, head_p, r=0.5, loc=(0.62, 0, 2.95))
hand_p = empty("PieceHandR", kit)
whisk(hand_p, (0, 0, -0.9), rot=(0, 0, 0))
export_glb(kit, "opera_pastry_chef_outfit.glb")
qa_render([kit], "chef_outfit")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_batch2_2026-07-22.blend"))
print("DONE")
