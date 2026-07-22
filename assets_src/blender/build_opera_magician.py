#!/usr/bin/env python3
"""Opera job 3D batch 6 — Magician mechanic props.

Continuity rules from the handoff: the three hats share ONE silhouette and
scale, differing only by clear band color (coral / teal / cream) so tracking
stays fair; the bunny-fish is always a pink FISH (fins + tail) with long
rabbit ears — never a rabbit body. Blender -Y = stage front."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, ROOT, CREAM, CORAL, PLUM, BRASS, PEARL)
import bpy, math

S.OUT = os.path.join(ROOT, "assets/opera/jobs/magician")
S.QA = os.path.join(ROOT, "assets_src/blender/qa_magician")
os.makedirs(S.OUT, exist_ok=True)
os.makedirs(S.QA, exist_ok=True)

TEAL = mat("teal", (0.31, 0.62, 0.63))
PLUM_HAT = mat("plum_hat", (0.36, 0.24, 0.55))
PINK = mat("bunny_pink", (0.97, 0.62, 0.72))
PINK_L = mat("bunny_pink_l", (1.0, 0.78, 0.85))
INK = mat("face_ink", (0.12, 0.1, 0.22))

def hat(i, band_m):
    root = empty("OperaMagicianHat%d" % i)
    vis = empty("Visual", root)
    cyl("Base", PLUM_HAT, vis, r=2.3, depth=0.4, loc=(0, 0, -0.2), verts=24)
    torus("BaseTrim", BRASS, vis, R=2.28, r=0.06, loc=(0, 0, 0.0))
    cyl("Brim", PLUM_HAT, vis, r=2.05, depth=0.28, loc=(0, 0, 0.45), verts=24)
    crown = cyl("Crown", PLUM_HAT, vis, r=1.45, depth=2.5, loc=(0, 0, 1.85), verts=24)
    cyl("Band", band_m, vis, r=1.5, depth=0.55, loc=(0, 0, 0.95), verts=24)
    sph("CrownTop", PLUM_HAT, vis, r=1.45, loc=(0, 0, 3.1), scale=(1, 1, 0.2))
    sph("BandPearl", PEARL, vis, r=0.18, loc=(0, -1.5, 0.95), seg=8, rings=5)
    empty("TouchTarget", root, (0, 0, 1.5))
    empty("FXAnchor", root, (0, 0, 3.6))
    return root

def bunnyfish():
    root = empty("OperaBunnyFish")
    vis = empty("Visual", root)
    sph("Body", PINK, vis, r=0.85, scale=(0.95, 1.15, 0.95))       # fish body
    tail = empty("TailFin", vis, (0, 1.05, 0))
    for sx in (-1, 1):
        sph("TailLobe%d" % sx, PINK_L, tail, r=0.42,
            loc=(sx * 0.22, 0.3, 0.1), scale=(0.4, 1.1, 0.9), seg=10, rings=6)
    for sx in (-1, 1):
        sph("SideFin%d" % sx, PINK_L, vis, r=0.32,
            loc=(sx * 0.8, 0.15, -0.1), scale=(0.5, 1.0, 0.7), seg=10, rings=6)
    for sx in (-1, 1):                                              # LONG rabbit ears
        ear = sph("Ear%d" % sx, PINK, vis, r=0.3,
                  loc=(sx * 0.35, 0.05, 1.45), scale=(0.65, 0.5, 2.0), seg=10, rings=6)
        ear.rotation_euler = (0, sx * 0.12, 0)
        sph("EarInner%d" % sx, PINK_L, vis, r=0.18,
            loc=(sx * 0.35, -0.06, 1.45), scale=(0.55, 0.4, 1.6), seg=8, rings=5)
    for sx in (-1, 1):
        sph("Eye%d" % sx, INK, vis, r=0.13, loc=(sx * 0.32, -0.75, 0.25), seg=8, rings=5)
    sph("Snout", PINK_L, vis, r=0.24, loc=(0, -0.82, -0.05), scale=(1, 0.6, 0.8), seg=8, rings=5)
    empty("FXAnchor", root, (0, 0, 2.6))
    return root

built = []
for i, band in enumerate([CORAL, TEAL, CREAM]):
    h = hat(i, band)
    h.location = ((i - 1) * 6.0, 0, 0)
    export_glb(h, "opera_magician_hat_%d.glb" % i)
    built.append(h)
b = bunnyfish()
b.location = (0, 7, 1.0)
export_glb(b, "opera_magician_bunnyfish.glb")
built.append(b)
qa_render(built, "magician_family")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_magician_2026-07-22.blend"))
print("DONE")
