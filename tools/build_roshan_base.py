#!/usr/bin/env python3
"""
build_roshan_base.py — automate "author the base" without auto-rigging.

THE INSIGHT
-----------
Don't auto-rig the AI mesh (web auto-riggers are humanoid-only and produce their
OWN skeleton with the wrong bone names — see CHARACTER_CUSTOMIZATION.md §9).
Instead REUSE Roshan's proven 26-bone rig + procedural swim, and just move the
skin weights onto the new geometry. Then bolt on cosmetic sockets and a fan of
independent hair strands.

PIPELINE (run in Blender):
    1. import rig source (existing roshan.glb)  -> the proven armature + weights
    2. import the new mesh (from Tripo / Hunyuan3D, sculpted from the sprite)
    3. align + transfer skin weights old-mesh -> new-mesh (kept on the SAME armature)
    4. add cosmetic SOCKET bones                (headTop, backL/R, earL/R, tailTip, handHold)
    5. add a fan of HAIR STRAND chains          (default 12, each 3 segs) for physics hair
    6. export glb + remind to validate

What stays manual: fidelity/likeness cleanup on the AI mesh, and weight-paint
touch-ups around the tail/face. Everything else here is automated.

USAGE (needs a real Blender; none in the headless web session):
    blender --background --python tools/build_roshan_base.py -- \
        --rig assets/characters/roshan.glb \
        --mesh /path/to/ai_generated_roshan.glb \
        --hair 12 --out /tmp/roshan_new.glb
"""
import sys, os
from math import cos, sin, pi

SOCKET_BONES = [
    # name,     parent,   local offset from parent head (Blender Z-up, metres)
    ("headTop", "head",   (0.00, 0.00, 0.18)),
    ("backL",   "chest",  (0.10, -0.04, 0.10)),
    ("backR",   "chest",  (-0.10, -0.04, 0.10)),
    ("earL",    "head",   (0.09, 0.00, 0.04)),
    ("earR",    "head",   (-0.09, 0.00, 0.04)),
    ("tailTip", "tail8",  (0.00, -0.10, 0.00)),
    ("handHold","hand",   (0.04, 0.00, 0.00)),
]

# Hair strand naming contract (the runtime scripts/hair.gd discovers these):
#   hair_<SS>_<J>   SS = strand 00..N-1,  J = segment 0..segs-1
HAIR_PREFIX = "hair_"


def parse_args(argv):
    a = {"rig": "assets/characters/roshan.glb", "mesh": "", "hair": "12",
         "segs": "3", "out": "/tmp/roshan_new.glb",
         "weights": "auto",   # auto = Blender automatic weights (best for a different AI mesh);
                              # transfer = copy weights from the old mesh (best if shapes match)
         "hairgeo": "1"}      # 1 = generate procedural rainbow hair cards (no sculpting)
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        i = 0
        while i < len(rest):
            k = rest[i].lstrip("-")
            if k in a and i + 1 < len(rest):
                a[k] = rest[i + 1]; i += 2
            else:
                i += 1
    return a


def hair_layout(n, segs):
    """Return [(bonename, parent, head_xyz), ...] for a fan of n strands off 'head'.
    Strands fan across the back of the scalp and hang down in `segs` segments."""
    out = []
    for s in range(n):
        # spread across a 200-degree arc around the back of the head
        ang = (-100.0 + 200.0 * (s / max(1, n - 1))) * pi / 180.0
        rx = 0.085 * sin(ang)
        ry = -0.02 - 0.06 * cos(ang)     # back strands sit further back
        parent = "head"
        for j in range(segs):
            name = "%s%02d_%d" % (HAIR_PREFIX, s, j)
            if j == 0:
                head = (rx, ry, 0.10)                 # scalp anchor
            else:
                head = (rx * 0.4, ry - 0.02, -0.10 * j)  # hang downward/back
            out.append((name, parent, head))
            parent = name
    return out


def generate_hair_cards(bpy, Vector, arm, n, segs, width=0.045):
    """Build the rainbow hair AS GEOMETRY (no sculpting): one tapered ribbon 'card'
    per strand, following its hair_<SS>_<J> bone chain, weighted to that chain, with
    the strand index baked into vertex-colour RED for hair_rainbow.gdshader."""
    me = bpy.data.meshes.new("roshan_hair")
    obj = bpy.data.objects.new("roshan_hair", me)
    bpy.context.collection.objects.link(obj)
    bones = arm.data.bones
    verts, faces, vbone, vidx = [], [], [], []
    for s in range(n):
        chain = ["hair_%02d_%d" % (s, j) for j in range(segs)]
        pts, bnames = [], []
        for bn in chain:
            if bn in bones:
                pts.append(arm.matrix_world @ bones[bn].head_local); bnames.append(bn)
        if chain[-1] in bones:
            pts.append(arm.matrix_world @ bones[chain[-1]].tail_local); bnames.append(chain[-1])
        if len(pts) < 2:
            continue
        base = len(verts)
        for k, p in enumerate(pts):
            d = (pts[k + 1] - p) if k < len(pts) - 1 else (p - pts[k - 1])
            d.normalize()
            side = d.cross(Vector((0, 0, 1)))
            side = side.normalized() if side.length > 1e-4 else Vector((1, 0, 0))
            w = width * (1.0 - 0.6 * k / (len(pts) - 1))   # taper to the tip
            verts.append(p + side * w); verts.append(p - side * w)
            bn = bnames[min(k, len(bnames) - 1)]
            vbone += [bn, bn]; vidx += [s, s]
        for k in range(len(pts) - 1):
            a0, a1 = base + k * 2, base + k * 2 + 1
            b0, b1 = base + (k + 1) * 2, base + (k + 1) * 2 + 1
            faces.append((a0, a1, b1, b0))
    me.from_pydata(verts, [], faces); me.update()
    for bn in set(vbone):
        obj.vertex_groups.new(name=bn)
    for vi, bn in enumerate(vbone):
        obj.vertex_groups[bn].add([vi], 1.0, "REPLACE")
    col = me.color_attributes.new(name="Color", type="FLOAT_COLOR", domain="POINT")
    for vi, si in enumerate(vidx):
        col.data[vi].color = (si / max(1, n - 1), 0.0, 0.0, 1.0)
    obj.parent = arm
    obj.modifiers.new("Armature", "ARMATURE").object = arm
    return len(verts)


def main():
    args = parse_args(sys.argv)
    n_hair = int(args["hair"]); segs = int(args["segs"])
    print(f"[i] sockets: {[s[0] for s in SOCKET_BONES]}")
    print(f"[i] hair: {n_hair} strands x {segs} segs = {n_hair*segs} bones "
          f"(named {HAIR_PREFIX}00_0 .. {HAIR_PREFIX}{n_hair-1:02d}_{segs-1})")

    try:
        import bpy
        from mathutils import Vector
    except ImportError:
        print(__doc__)
        print("\n[!] Run inside Blender:")
        print("    blender --background --python tools/build_roshan_base.py -- "
              "--mesh <ai_mesh.glb> --hair %d --out %s" % (n_hair, args["out"]))
        print("[i] No Blender in the Claude Code web session; run where Blender exists.")
        print("[i] Geometry source first: Tripo (clean quads) or self-hosted Hunyuan3D.")
        sys.exit(1)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(args["rig"]))
    arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
    old_mesh = next((o for o in bpy.data.objects if o.type == "MESH"), None)
    if arm is None or old_mesh is None:
        print("[!] rig source must contain an armature + mesh"); sys.exit(2)

    # 2. import the new AI mesh (optional — if omitted, we just extend the rig)
    new_mesh = None
    if args["mesh"] and os.path.exists(args["mesh"]):
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.abspath(args["mesh"]))
        added = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        new_mesh = added[0] if added else None

    # 3. bind the new mesh to the EXISTING 26-bone rig. Done BEFORE socket/hair
    #    bones are added, so the body only weights to the real deform bones.
    if new_mesh is not None:
        if args["weights"] == "auto":
            print("[i] binding new mesh with AUTOMATIC weights (best for a fresh AI mesh)")
            bpy.ops.object.select_all(action="DESELECT")
            new_mesh.select_set(True); arm.select_set(True)
            bpy.context.view_layer.objects.active = arm
            bpy.ops.object.parent_set(type="ARMATURE_AUTO")
            print("[ok] auto-weighted. Test-pose tail1..tail8 / fins; touch up only if pinching.")
        else:
            print("[i] transferring skin weights old -> new mesh (shapes should match)")
            for vg in old_mesh.vertex_groups:
                if vg.name not in new_mesh.vertex_groups:
                    new_mesh.vertex_groups.new(name=vg.name)
            dt = new_mesh.modifiers.new("WeightTransfer", "DATA_TRANSFER")
            dt.object = old_mesh
            dt.use_vert_data = True
            dt.data_types_verts = {"VGROUP_WEIGHTS"}
            dt.vert_mapping = "POLYINTERP_NEAREST"
            bpy.context.view_layer.objects.active = new_mesh
            bpy.ops.object.datalayout_transfer(modifier=dt.name)
            bpy.ops.object.modifier_apply(modifier=dt.name)
            new_mesh.modifiers.new("Armature", "ARMATURE").object = arm
            print("[ok] weights transferred (review tail/face by hand)")
        old_mesh.hide_set(True); old_mesh.name = "roshan_OLD_reference"

    # 4 + 5. add socket + hair bones to the armature
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.data.edit_bones

    def add_bone(name, parent, head_off):
        if name in eb:
            return
        b = eb.new(name)
        p = eb.get(parent)
        base = p.head if p else Vector((0, 0, 0))
        b.head = base + Vector(head_off)
        b.tail = b.head + Vector((0, 0, -0.06))
        if p:
            b.parent = p
        b.use_connect = False

    for name, parent, off in SOCKET_BONES:
        add_bone(name, parent, off)
    for name, parent, head in hair_layout(n_hair, segs):
        add_bone(name, parent, head)

    bpy.ops.object.mode_set(mode="OBJECT")

    # 6. generate the rainbow hair as geometry (no sculpting needed)
    if args["hairgeo"] == "1":
        try:
            nv = generate_hair_cards(bpy, Vector, arm, n_hair, segs)
            print("[ok] generated procedural rainbow hair: %d strands, %d verts" % (n_hair, nv))
        except Exception as e:
            print("[!] hair-card generation needs a tweak: %s" % e)

    out = os.path.abspath(args["out"])
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB")
    print(f"[ok] wrote {out}")
    print("[i] validate:  python3 tools/glb_check.py %s" % out)
    print("[i] then weight the hair geometry to the %s** chains and store a per-strand"
          " index in vertex-colour R (0..1) for the rainbow shader (see hair.gd)." % HAIR_PREFIX)


if __name__ == "__main__":
    main()
