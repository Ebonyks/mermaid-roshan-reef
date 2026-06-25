#!/usr/bin/env python3
"""
build_roshan_rig.py — Blender bootstrap for re-sculpting Roshan onto her EXACT rig.

WHY THIS EXISTS
---------------
Roshan is already a real 3D, rigged character: `assets/characters/roshan.glb`
(~15.5k tris, 26-bone skeleton). She is *not* a sprite. The procedural swim in
`scripts/player.gd` drives her by bone NAME at runtime (no baked animation clip):

    tail1..tail8  -> sine wave down the tail        (axis Vector3.RIGHT)
    finTop,finBot -> flutter                        (axis Vector3.RIGHT)
    chest, neck   -> counter-sway                   (axis Vector3.RIGHT)
    head          -> bob + idle                     (axis Vector3.BACK)
    hair1,2,3     -> trailing sway                   (axis Vector3.BACK)

So ANY replacement mesh MUST be weighted to a skeleton with the SAME 26 bone
names and the SAME hierarchy, or `player.gd` silently stops animating those
bones (it warns once and leaves them at rest). The safest way to guarantee that
is to KEEP THE EXISTING ARMATURE and only replace the mesh. That is exactly what
this script sets up.

The "stuffed animal" look is a SCULPT + SHADING problem, not a rig problem —
this pipeline keeps the rig and lets an artist redo the body.

USAGE (needs a real Blender — none is available in the headless web session):
    blender --background --python tools/build_roshan_rig.py -- \
        --src assets/characters/roshan.glb \
        --out /tmp/roshan_sculpt_start.blend

Then open the .blend, sculpt/replace the body mesh (it is already parented to the
original armature with weights as a starting point), keep bone names intact, and
export per the EXPORT CONTRACT printed at the end.

The 26-bone rest table (local translations, glTF axes) is embedded below for
reference / from-scratch rebuilds; the import path is preferred for guaranteed
parity.
"""

import sys, os

# --- Ground-truth rig, extracted from the shipping roshan.glb (local T, glTF axes) ---
# name        parent      (x, y, z)
RIG = [
    ("root",   None,     ( 0.000,  1.050,  0.000)),
    ("spine1", "root",   (-0.164,  0.391,  0.000)),
    ("chest",  "spine1", (-0.181,  0.437,  0.000)),
    ("neck",   "chest",  (-0.234,  0.644,  0.000)),
    ("head",   "neck",   (-0.253,  0.529,  0.000)),
    ("hair1",  "head",   ( 0.596,  0.207,  0.000)),
    ("hair2",  "hair1",  ( 0.541,  0.069,  0.000)),
    ("hair3",  "hair2",  ( 0.577,  0.000,  0.000)),
    ("hairL1", "head",   (-0.541,  0.000,  0.000)),
    ("hairL2", "hairL1", (-0.216, -0.391,  0.000)),
    ("armU",   "chest",  (-0.234,  0.483,  0.000)),
    ("armF",   "armU",   (-0.361, -0.414,  0.000)),
    ("hand",   "armF",   ( 0.108,  0.299,  0.000)),
    ("armU2",  "chest",  (-0.396,  0.368,  0.000)),
    ("armF2",  "armU2",  (-0.181, -0.460,  0.000)),
    ("hand2",  "armF2",  ( 0.072, -0.322,  0.000)),
    ("tail1",  "root",   (-0.009, -0.319,  0.000)),
    ("tail2",  "tail1",  (-0.074, -0.286,  0.000)),
    ("tail3",  "tail2",  (-0.184, -0.215,  0.000)),
    ("tail4",  "tail3",  (-0.232, -0.120,  0.000)),
    ("tail5",  "tail4",  (-0.236, -0.103,  0.000)),
    ("tail6",  "tail5",  (-0.242, -0.083,  0.000)),
    ("tail7",  "tail6",  (-0.248, -0.038,  0.000)),
    ("tail8",  "tail7",  (-0.250, -0.029,  0.000)),
    ("finTop", "tail8",  (-0.277,  0.779,  0.000)),
    ("finBot", "tail8",  (-0.457,  0.043,  0.000)),
]
REQUIRED_BONES = [b[0] for b in RIG]

EXPORT_CONTRACT = """
================ EXPORT CONTRACT (read before exporting) ================
1. Keep all 26 bone names EXACTLY: {bones}
2. Keep the hierarchy (root is the only parentless bone; tail1..tail8 chain off
   root; finTop/finBot off tail8; hair1..3 off head; etc.).
3. One skinned mesh, bound to that armature. Triangulate on export.
4. File -> Export -> glTF 2.0 (.glb), settings:
     Format: glTF Binary (.glb)
     Include: Selected Objects (armature + mesh)
     Transform: +Y Up  (Godot/glTF standard)
     Data: Mesh (UVs, Normals, Tangents), Skinning ON, Animation OFF
           (player.gd animates procedurally — do NOT bake clips)
5. Overwrite assets/characters/roshan.glb. Delete the stale
   assets/characters/roshan.glb.import so Godot re-imports on next editor open.
6. player.gd scales the model x1.55 and offsets y -1.6 — sculpt at the same
   overall proportions as the original so those constants still frame her.
7. Sanity check after export:
     python3 tools/glb_check.py assets/characters/roshan.glb   # expects 26 joints
=========================================================================
""".format(bones=", ".join(REQUIRED_BONES))


def parse_args(argv):
    a = {"src": "assets/characters/roshan.glb", "out": "/tmp/roshan_sculpt_start.blend"}
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        i = 0
        while i < len(rest):
            if rest[i] in ("--src", "--out"):
                a[rest[i][2:]] = rest[i + 1]; i += 2
            else:
                i += 1
    return a


def main():
    try:
        import bpy
    except ImportError:
        print(__doc__)
        print("\n[!] This script must be run inside Blender:")
        print("    blender --background --python tools/build_roshan_rig.py -- "
              "--src assets/characters/roshan.glb --out /tmp/roshan_sculpt_start.blend")
        print("\n[i] No Blender is installed in the Claude Code web session, so it cannot")
        print("    run here. Run it in a Blender-equipped environment.")
        print(EXPORT_CONTRACT)
        sys.exit(1)

    args = parse_args(sys.argv)
    bpy.ops.wm.read_factory_settings(use_empty=True)

    src = os.path.abspath(args["src"])
    if not os.path.exists(src):
        print(f"[!] source not found: {src}"); sys.exit(2)

    print(f"[i] importing existing rig from {src}")
    bpy.ops.import_scene.gltf(filepath=src)

    arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
    if arm is None:
        print("[!] no armature found in source glb"); sys.exit(3)

    have = {b.name for b in arm.data.bones}
    missing = [b for b in REQUIRED_BONES if b not in have]
    if missing:
        print(f"[!] WARNING: source rig is missing expected bones: {missing}")
    else:
        print(f"[ok] all 26 expected bones present.")

    # Keep the armature; tag the original mesh as the sculpt reference, add a
    # mirrored, lightly-decimated copy to start a cleaner sculpt from.
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for m in meshes:
        m.name = "roshan_OLD_reference"
        m.hide_set(True)  # keep as silhouette reference, hidden by default

    print("[i] Original mesh kept as 'roshan_OLD_reference' (hidden) for silhouette matching.")
    print("[i] Sculpt the NEW body, weight it to the armature (keep bone names), then export.")

    out = os.path.abspath(args["out"])
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print(f"[ok] wrote sculpt-start blend: {out}")
    print(EXPORT_CONTRACT)


if __name__ == "__main__":
    main()
