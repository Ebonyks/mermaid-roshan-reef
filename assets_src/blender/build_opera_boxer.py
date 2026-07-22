#!/usr/bin/env python3
"""Opera job 3D batch 7 — Boxer ring dressing.

The live ring footprint (deck, posts, ropes) is gameplay-authoritative and
stays primitive; this kit dresses it in place at the SAME coordinates:
padded corner caps, the shell bell, three round-progress lamps
(StateLamp0..2), and the championship-belt pedestal outside the fight path
with a raised-belt StateComplete. Godot (x, y, z) -> Blender (x, -z, y)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, shell_clasp, ROOT, CREAM, CORAL, BRASS, PEARL)
import bpy, math

S.OUT = os.path.join(ROOT, "assets/opera/jobs/boxer")
S.QA = os.path.join(ROOT, "assets_src/blender/qa_boxer")
os.makedirs(S.OUT, exist_ok=True)
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
PADRED = mat("pad_red", (0.85, 0.3, 0.4))
LAMP_OFF = mat("lamp_off", (0.4, 0.32, 0.5))
LAMP_ON = mat("lamp_on", (1.0, 0.85, 0.4), emission=1.8)
BELT_RED = mat("belt_red", (0.8, 0.28, 0.32))
GOLD_GLOW = mat("gold_glow", (1.0, 0.88, 0.45), emission=1.2)

def dressing():
    root = empty("OperaBoxerDressing")
    vis = empty("Visual", root)
    # padded caps + collars on the four posts (Godot x±11, z -11/7)
    for gx in (-11.0, 11.0):
        for gz in (-11.0, 7.0):
            bx, by = gx, -gz
            sph("PostCap", PADRED, vis, r=0.85, loc=(bx, by, 5.2), scale=(1, 1, 0.75), seg=12, rings=8)
            sph("CapPearl", PEARL, vis, r=0.22, loc=(bx, by, 5.85), seg=8, rings=5)
            cyl("PostPad", TEAL, vis, r=0.62, depth=1.6, loc=(bx, by, 1.6))
    # shell bell on the front-left post (Godot -11, 5.2, 7 -> Blender -11, -7)
    bell = empty("ShellBell", vis, (-11, -7, 5.2))
    sph("BellDome", BRASS, bell, r=0.85, scale=(1, 1, 0.8))
    shell_clasp(bell, (0, -0.75, 0.15), s=1.1)
    sph("Clapper", PEARL, bell, r=0.2, loc=(0, 0, -0.7), seg=8, rings=5)
    # three round-progress lamps over the front rope line
    for k in range(3):
        lx = (k - 1) * 2.2
        cyl("LampPost%d" % k, BRASS, vis, r=0.12, depth=1.0, loc=(lx, -12.2, 4.0))
        sph("LampOff%d" % k, LAMP_OFF, vis, r=0.55, loc=(lx, -12.2, 4.8), seg=10, rings=6)
        st = empty("StateLamp%d" % k, vis)
        sph("LampOn%d" % k, LAMP_ON, st, r=0.58, loc=(lx, -12.2, 4.8), seg=10, rings=6)
    # championship-belt pedestal outside the fight path (Godot 15.5, 0, 7)
    ped = empty("BeltPedestal", vis, (15.5, -7, 0))
    cyl("Ped", CREAM, ped, r=1.5, depth=1.0, loc=(0, 0, 0.5))
    torus("PedTrim", BRASS, ped, R=1.45, r=0.08, loc=(0, 0, 1.0))
    st_i = empty("StateIdle", vis)
    belt_i = empty("BeltRest", st_i, (15.5, -7, 1.4))
    torus("BeltStrapI", BELT_RED, belt_i, R=0.95, r=0.28, scale=(1, 1, 0.6))
    sph("BeltPlateI", GOLD_GLOW, belt_i, r=0.55, loc=(0, -0.9, 0), scale=(1, 0.4, 1), seg=12, rings=8)
    st_c = empty("StateComplete", vis)
    belt_c = empty("BeltRaised", st_c, (15.5, -7, 4.2))
    torus("BeltStrapC", BELT_RED, belt_c, R=0.95, r=0.28, scale=(1, 1, 0.6))
    sph("BeltPlateC", GOLD_GLOW, belt_c, r=0.55, loc=(0, -0.9, 0), scale=(1, 0.4, 1), seg=12, rings=8)
    torus("WinHalo", GOLD_GLOW, st_c, R=1.7, r=0.09, loc=(15.5, -7, 4.2))
    return root

d = dressing()
export_glb(d, "opera_boxer_dressing.glb")
qa_render([d], "boxer_dressing")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_boxer_2026-07-22.blend"))
print("DONE")
