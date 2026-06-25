#!/usr/bin/env python3
"""
build_npc_rig.py — Blender bootstrap for the NPC 3D conversion.

WHY THIS EXISTS
---------------
Every friend/NPC (Gabby, Wacky, Chuck, Huluu, Evie, Harper, Fiona, Faron,
Daddy, Kareem, ...) is currently a flat 2D billboard `.png` in
assets/characters/friends/. Converting them to 3D means: one low-poly humanoid
mesh per character, on a SHARED standard rig, with a simple looping idle so they
read as alive in dialogue pop-ins.

Unlike Roshan (a mermaid driven by a bespoke 26-bone procedural animator), NPCs
are land kids with legs and only need a light idle. We give them ONE shared
18-bone humanoid rig so a single idle animation (and one integration code path)
covers the whole cast. Build the rig once, reuse for every character.

STANDARD NPC RIG (18 bones)
    root
      hips
        spine -> chest -> neck -> head
        chest -> armUL -> armFL -> handL      (left arm)
        chest -> armUR -> armFR -> handR      (right arm)
      hips -> legUL -> legLL -> footL          (left leg)
      hips -> legUR -> legLR -> footR          (right leg)

Bone names are the contract — keep them identical across all NPCs so the same
idle clip and the same loader retarget to every character (see CHARACTER_PIPELINE.md).

USAGE (needs a real Blender; none in the headless web session):
    blender --background --python tools/build_npc_rig.py -- --out /tmp/npc_rig.blend

Produces a .blend containing just the armature (+ a rough body proxy) to sculpt
each NPC onto. For animation, author ONE 'idle' clip on this rig and reuse it.
"""
import sys, os
from math import sqrt

# name, parent, head (x,y,z) in Blender Z-up metres (approx kid proportions, ~1.0 tall)
BONES = [
    ("root",  None,    (0.00, 0.00, 0.00)),
    ("hips",  "root",  (0.00, 0.00, 0.50)),
    ("spine", "hips",  (0.00, 0.00, 0.60)),
    ("chest", "spine", (0.00, 0.00, 0.72)),
    ("neck",  "chest", (0.00, 0.00, 0.86)),
    ("head",  "neck",  (0.00, 0.00, 0.92)),
    ("armUL", "chest", (0.10, 0.00, 0.82)),
    ("armFL", "armUL", (0.22, 0.00, 0.74)),
    ("handL", "armFL", (0.30, 0.00, 0.62)),
    ("armUR", "chest", (-0.10, 0.00, 0.82)),
    ("armFR", "armUR", (-0.22, 0.00, 0.74)),
    ("handR", "armFR", (-0.30, 0.00, 0.62)),
    ("legUL", "hips",  (0.06, 0.00, 0.48)),
    ("legLL", "legUL", (0.07, 0.00, 0.26)),
    ("footL", "legLL", (0.07, 0.08, 0.04)),
    ("legUR", "hips",  (-0.06, 0.00, 0.48)),
    ("legLR", "legUR", (-0.07, 0.00, 0.26)),
    ("footR", "legLR", (-0.07, 0.08, 0.04)),
]
HEAD = {n: h for n, p, h in BONES}
CHILDREN = {}
for n, p, h in BONES:
    CHILDREN.setdefault(p, []).append(n)

EXPORT_CONTRACT = """
================ NPC EXPORT CONTRACT ================
1. Keep the 18 bone names exactly (root,hips,spine,chest,neck,head,
   armUL/armFL/handL, armUR/armFR/handR, legUL/legLL/footL, legUR/legLR/footR).
2. One skinned mesh per character, bound to this rig.
3. Author ONE looping 'idle' clip on the shared rig; reuse across all NPCs.
4. Export glTF Binary (.glb), +Y Up, Skinning ON, Animation ON (the single idle).
5. Save each as assets/characters/friends/<tex>.glb where <tex> matches the
   FRIEND_DEFS / sprite name (gabby, wacky_chuck, huluu, pearl_friend, ...).
   The model-aware loader (see CHARACTER_PIPELINE.md §4) picks the .glb up
   automatically and falls back to the .png until the model exists.
6. Validate:  python3 tools/glb_check.py assets/characters/friends/gabby.glb
=====================================================
"""


def tail_for(name):
    kids = CHILDREN.get(name, [])
    if kids:
        return HEAD[kids[0]]
    # leaf: extend a little along its direction from parent
    parent = next(p for n, p, h in BONES if n == name)
    ph = HEAD[parent] if parent else (0, 0, 0)
    h = HEAD[name]
    d = tuple(h[i] - ph[i] for i in range(3))
    ln = sqrt(sum(c * c for c in d)) or 1.0
    return tuple(h[i] + d[i] / ln * 0.08 for i in range(3))


def main():
    try:
        import bpy
        from mathutils import Vector
    except ImportError:
        print(__doc__)
        print("\n[!] Run inside Blender:")
        print("    blender --background --python tools/build_npc_rig.py -- --out /tmp/npc_rig.blend")
        print("[i] No Blender in the Claude Code web session; run it where Blender exists.")
        print(EXPORT_CONTRACT)
        sys.exit(1)

    out = "/tmp/npc_rig.blend"
    if "--" in sys.argv:
        rest = sys.argv[sys.argv.index("--") + 1:]
        if "--out" in rest:
            out = rest[rest.index("--out") + 1]

    bpy.ops.wm.read_factory_settings(use_empty=True)
    arm_data = bpy.data.armatures.new("npc_rig")
    arm = bpy.data.objects.new("npc_rig", arm_data)
    bpy.context.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")

    eb = arm_data.edit_bones
    made = {}
    for name, parent, head in BONES:
        b = eb.new(name)
        b.head = Vector(head)
        b.tail = Vector(tail_for(name))
        if parent:
            b.parent = made[parent]
            b.use_connect = False
        made[name] = b

    bpy.ops.object.mode_set(mode="OBJECT")
    out = os.path.abspath(out)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print(f"[ok] wrote NPC rig blend: {out}  ({len(BONES)} bones)")
    print(EXPORT_CONTRACT)


if __name__ == "__main__":
    main()
