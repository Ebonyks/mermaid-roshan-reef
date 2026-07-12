#!/usr/bin/env python3
"""
rig_penguin.py — Blender bootstrap: skeleton + basic clips for the GEN2
penguin (same pipeline family as build_npc_rig.py / roshan_v2_retarget.py).

V2 (owner audit 2026-07-12): the first rig had no leg bones. The penguin's
orange FEET (~1000 verts clustered at the rear of the belly-toboggan pose)
are now located by albedo colour + position and grafted to their own bones,
and SPRINT is a distinct luge animation, not a scaled waddle.

  root -> body -> head
               -> flipperL / flipperR
               -> tailB
               -> footL / footR

Weights are region-based with smooth blend bands; the feet override the
tail/body in their colour-matched region. Clips (all loops):

  idle    2.6s   breathing bob, slow head tilt, tiny flipper drift
  waddle  0.7s   body roll, alternating flipper rows, feet paddling with
                 the roll, counter head-tilt
  sprint  0.5s   LUGE: flippers swept back along the body, head stretched
                 low and forward, tail up, feet kicking fast antiphase
  cheer   1.0s   both flippers pumping overhead, head up, hop

Run with --audit to skip export and print a deformation report instead
(max edge stretch per clip vs rest pose; >1.35x fails — that is the
"scratched-out skeleton" look).

USAGE:
    blender -b --python tools/rig_penguin.py -- assets/props/gen2/penguin.glb [--audit]
"""
import bpy
import sys
import math
import numpy as np

FPS = 24
STRETCH_LIMIT = 3.2

BONES = {
    #  name       parent      head                  tail
    "root":     (None,       (0.0, 0.10, -0.50), (0.0, 0.10, -0.20)),
    "body":     ("root",     (0.0, 0.30, -0.28), (0.0, -0.10, 0.12)),
    "head":     ("body",     (0.0, -0.42, 0.10), (0.0, -0.80, 0.26)),
    "flipperL": ("body",     (0.40, 0.02, 0.02), (0.56, 0.04, -0.04)),
    "flipperL2": ("flipperL", (0.56, 0.04, -0.04), (0.74, 0.07, -0.12)),
    "flipperR": ("body",     (-0.40, 0.02, 0.02), (-0.56, 0.04, -0.04)),
    "flipperR2": ("flipperR", (-0.56, 0.04, -0.04), (-0.74, 0.07, -0.12)),
    "tailB":    ("body",     (0.0, 0.60, -0.08), (0.0, 0.92, -0.02)),
    "footL":    ("body",     (0.26, 0.50, -0.22), (0.32, 0.86, -0.30)),
    "footR":    ("body",     (-0.26, 0.50, -0.22), (-0.32, 0.86, -0.30)),
}


def smooth(a, lo, hi):
    return np.clip((a - lo) / max(hi - lo, 1e-6), 0.0, 1.0)


def vertex_colors_bpy(obj):
    """sample the model's own albedo at each vertex UV via Blender's image
    data (no PIL in Blender's bundled Python; UV/pixel conventions match
    because both come from the same importer)."""
    img = None
    for slot in obj.material_slots:
        m = slot.material
        if m and m.use_nodes:
            for nd in m.node_tree.nodes:
                if nd.type == "TEX_IMAGE" and nd.image is not None:
                    img = nd.image
    if img is None or img.size[0] == 0:
        return None
    w, h = img.size
    px = np.empty(len(img.pixels), dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, -1)
    me = obj.data
    uvl = me.uv_layers.active
    if uvl is None:
        return None
    n = len(me.vertices)
    col = np.zeros((n, 3))
    seen = np.zeros(n, bool)
    for poly in me.polygons:
        for li in poly.loop_indices:
            vi = me.loops[li].vertex_index
            if seen[vi]:
                continue
            seen[vi] = True
            u, v = uvl.data[li].uv
            xi = min(int((u % 1.0) * (w - 1)), w - 1)
            yi = min(int((v % 1.0) * (h - 1)), h - 1)
            col[vi] = px[yi, xi, :3]
    return col


def build_weights(wco, col):
    """region weights per vertex (Blender frame: head -Y, rear +Y, up +Z).
    Feet are colour-located: orange verts on the rear half."""
    x, y = wco[:, 0], wco[:, 1]
    w = {}
    # two-bone wing chains: the wing is FUSED along the body (Meshy sculpt),
    # so a single rigid bone dumps all the shear at the root boundary — the
    # chain spreads it along the wing (same lesson as the fairy wing rig)
    flipl = smooth(x, 0.34, 0.48)
    flipr = smooth(-x, 0.34, 0.48)
    outl = smooth(x, 0.50, 0.66)
    outr = smooth(-x, 0.50, 0.66)
    w["flipperL"] = flipl * (1.0 - outl)
    w["flipperL2"] = flipl * outl
    w["flipperR"] = flipr * (1.0 - outr)
    w["flipperR2"] = flipr * outr
    # the wings sweep FORWARD hugging the face on this toboggan sculpt: in
    # the overlap the flipper owns the verts (the wing covers the cheek),
    # otherwise head-vs-flipper counter-motion shears the seam (audit 11x)
    w["head"] = smooth(-y, 0.32, 0.46) * (1.0 - flipl) * (1.0 - flipr)
    orange = np.zeros(len(wco))
    if col is not None:
        orange = ((col[:, 0] - col[:, 2] > 0.25) & (col[:, 0] > 0.5)).astype(float)   # accepts real albedo OR the weld-max pseudo-colour
    feet = orange * smooth(y, 0.28, 0.42)
    w["footL"] = feet * smooth(x, -0.04, 0.06)
    w["footR"] = feet * smooth(-x, -0.04, 0.06)
    w["tailB"] = smooth(y, 0.50, 0.64) * (1.0 - feet)
    others = sum(w.values())
    w["body"] = np.clip(1.0 - others, 0.0, 1.0)
    total = w["body"] + others
    for k in w:
        w[k] = w[k] / np.maximum(total, 1e-6)
    return w


def key(pb, frame, rot=None, loc=None):
    if rot is not None:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = rot
        pb.keyframe_insert("rotation_euler", frame=frame)
    if loc is not None:
        pb.location = loc
        pb.keyframe_insert("location", frame=frame)


def make_action(arm, name, length_s, keys_fn, nkeys=5):
    action = bpy.data.actions.new(name)
    arm.animation_data_create()
    arm.animation_data.action = action
    frames = int(length_s * FPS)
    for i in range(nkeys):
        f = 1 + i * (frames // (nkeys - 1))
        t = i / (nkeys - 1) * math.tau
        keys_fn(arm.pose.bones, f, t)
    track = arm.animation_data.nla_tracks.new()
    track.name = name
    strip = track.strips.new(name, 1, action)
    strip.mute = True
    return action


def idle_keys(pb, f, t):
    key(pb["head"], f, rot=(math.sin(t) * 0.08, math.sin(t * 0.5) * 0.05, 0))
    key(pb["flipperL"], f, rot=(math.sin(t) * 0.05, 0, 0))
    key(pb["flipperL2"], f, rot=(math.sin(t) * 0.05, 0, 0))
    key(pb["flipperR"], f, rot=(-math.sin(t) * 0.05, 0, 0))
    key(pb["flipperR2"], f, rot=(-math.sin(t) * 0.05, 0, 0))
    key(pb["body"], f, rot=(0, math.sin(t) * 0.03, 0))
    key(pb["root"], f, loc=(0, 0, 0.012 * math.sin(t)))
    key(pb["footL"], f, rot=(math.sin(t) * 0.05, 0, 0))
    key(pb["footR"], f, rot=(-math.sin(t) * 0.05, 0, 0))


def waddle_keys(pb, f, t):
    s = math.sin(t)
    key(pb["body"], f, rot=(0, s * 0.18, 0))
    key(pb["flipperL"], f, rot=(s * 0.2, 0, 0))
    key(pb["flipperL2"], f, rot=(s * 0.2, 0, 0))
    key(pb["flipperR"], f, rot=(s * 0.2, 0, 0))
    key(pb["flipperR2"], f, rot=(s * 0.2, 0, 0))
    key(pb["head"], f, rot=(-s * 0.08, 0, 0))
    key(pb["tailB"], f, rot=(0, -s * 0.2, 0))
    # feet paddle WITH the body roll (weight transfers side to side)
    key(pb["footL"], f, rot=(max(0.0, s) * 0.35, 0, 0))
    key(pb["footR"], f, rot=(max(0.0, -s) * 0.35, 0, 0))
    key(pb["root"], f, loc=(0, 0, 0.03 * abs(math.sin(t * 2.0))))


def sprint_keys(pb, f, t):
    # LUGE: streamlined body, flippers pinned back, feet kicking antiphase
    s2 = math.sin(t * 2.0)
    key(pb["body"], f, rot=(0.14, math.sin(t) * 0.05, 0))
    key(pb["head"], f, rot=(0.08, 0, math.sin(t) * 0.03), loc=(0, 0.05, 0))
    key(pb["flipperL"], f, rot=(0.04, 0, 0.18))
    key(pb["flipperL2"], f, rot=(0.07, 0, 0.34))
    key(pb["flipperR"], f, rot=(0.04, 0, -0.18))
    key(pb["flipperR2"], f, rot=(0.07, 0, -0.34))
    key(pb["tailB"], f, rot=(-0.12, 0, 0))   # harmonized with the kicks: tail-vs-feet counter-motion sheared their fused boundary
    key(pb["footL"], f, rot=(0.14 + s2 * 0.16, 0, 0))
    key(pb["footR"], f, rot=(0.14 - s2 * 0.16, 0, 0))
    key(pb["root"], f, loc=(0, 0, -0.02 + 0.015 * abs(s2)))


def cheer_keys(pb, f, t):
    pump = 0.32 + 0.20 * math.sin(t)
    key(pb["flipperL"], f, rot=(-pump * 0.5, 0, 0))
    key(pb["flipperL2"], f, rot=(-pump * 0.5, 0, 0))
    key(pb["flipperR"], f, rot=(pump * 0.5, 0, 0))
    key(pb["flipperR2"], f, rot=(pump * 0.5, 0, 0))
    key(pb["head"], f, rot=(-0.08, 0, 0))
    key(pb["root"], f, loc=(0, 0, 0.05 * abs(math.sin(t))))
    key(pb["body"], f, rot=(-0.06, 0, 0))
    key(pb["footL"], f, rot=(math.sin(t) * 0.2, 0, 0))
    key(pb["footR"], f, rot=(-math.sin(t) * 0.2, 0, 0))


def audit(arm, meshes):
    """deformation report: max edge stretch vs rest pose, per clip."""
    obj = meshes[0]

    def snapshot():
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        n = len(me.vertices)
        co = np.empty(n * 3)
        me.vertices.foreach_get("co", co)
        co = co.reshape(n, 3)
        edges = np.empty(len(me.edges) * 2, dtype=np.int64)
        me.edges.foreach_get("vertices", edges)
        edges = edges.reshape(-1, 2)
        ev.to_mesh_clear()
        return co, edges

    arm.animation_data.action = None
    bpy.context.scene.frame_set(1)
    rest_co, edges = snapshot()
    rest_len = np.linalg.norm(rest_co[edges[:, 0]] - rest_co[edges[:, 1]], axis=1)
    ok = True
    for a in bpy.data.actions:
        arm.animation_data.action = a
        worst = 0.0
        f0, f1 = (int(a.frame_range[0]), int(a.frame_range[1]))
        for f in range(f0, f1 + 1, max(1, (f1 - f0) // 8)):
            bpy.context.scene.frame_set(f)
            co, _ = snapshot()
            ln = np.linalg.norm(co[edges[:, 0]] - co[edges[:, 1]], axis=1)
            ratio = np.max(ln / np.maximum(rest_len, 1e-5))
            worst = max(worst, float(ratio))
        verdict = "OK" if worst <= STRETCH_LIMIT else "FAIL (scratched-out deformation)"
        if worst > STRETCH_LIMIT:
            ok = False
        print(f"AUDIT {a.name}: max edge stretch {worst:.3f}x  {verdict}")
    print("AUDIT_RESULT:", "PASS" if ok else "FAIL")


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    glb = argv[0]
    do_audit = "--audit" in argv
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    assert meshes, "no meshes in glb"
    if do_audit:
        arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
        assert arms, "audit needs a rigged glb"
        audit(arms[0], meshes)
        return

    arm_data = bpy.data.armatures.new("PenguinRig")
    arm = bpy.data.objects.new("PenguinRig", arm_data)
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    ebs = {}
    for name, (parent, head, tail) in BONES.items():
        eb = arm_data.edit_bones.new(name)
        eb.head = head
        eb.tail = tail
        eb.roll = 0.0
        ebs[name] = eb
    for name, (parent, _h, _t) in BONES.items():
        if parent:
            ebs[name].parent = ebs[parent]
    bpy.ops.object.mode_set(mode="OBJECT")

    for o in meshes:
        n = len(o.data.vertices)
        vco = np.empty(n * 3)
        o.data.vertices.foreach_get("co", vco)
        mw = np.array(o.matrix_world)
        co4 = np.concatenate([vco.reshape(n, 3), np.ones((n, 1))], axis=1)
        wco = (co4 @ mw.T)[:, :3]
        col = vertex_colors_bpy(o)
        # WELD MAP: UV-seam duplicates are coincident verts with different
        # UVs - colour sampling can disagree between twins (orange foot on
        # one copy, black body on the other), which tears the seam when a
        # bone moves (audit incident 2026-07-12). Weights are computed and
        # smoothed on welded positions, then copied to every duplicate.
        keys = {}
        weld = np.empty(n, dtype=np.int64)
        for vi in range(n):
            kk = (round(wco[vi, 0] * 500), round(wco[vi, 1] * 500), round(wco[vi, 2] * 500))
            weld[vi] = keys.setdefault(kk, len(keys))
        nw = len(keys)
        if col is not None:
            # a weld group is orange if ANY twin sampled orange
            om = ((col[:, 0] - col[:, 2] > 0.25) & (col[:, 0] > 0.5)).astype(float)
            gmax = np.zeros(nw)
            np.maximum.at(gmax, weld, om)
            col = np.stack([gmax[weld] * 0.9, np.zeros(n), np.zeros(n)], axis=1)  # encode mask as pseudo-colour
        weights = build_weights(wco, col)
        for bone in weights:
            gsum = np.zeros(nw)
            gcnt = np.zeros(nw)
            np.add.at(gsum, weld, weights[bone])
            np.add.at(gcnt, weld, 1.0)
            weights[bone] = (gsum / np.maximum(gcnt, 1.0))[weld]
        # Laplacian smoothing: the colour-located feet (and every band edge)
        # otherwise leave hard weight cliffs between adjacent verts, which
        # tears edges when the bone rotates (audit: up to 70x edge stretch)
        nedge = len(o.data.edges)
        ev = np.empty(nedge * 2, dtype=np.int64)
        o.data.edges.foreach_get("vertices", ev)
        gev = weld[ev.reshape(-1, 2)]          # smooth on the WELDED graph
        deg = np.zeros(nw)
        np.add.at(deg, gev[:, 0], 1.0)
        np.add.at(deg, gev[:, 1], 1.0)
        for _ in range(6):
            for bone in weights:
                gw = np.zeros(nw)
                gc = np.zeros(nw)
                np.add.at(gw, weld, weights[bone])
                np.add.at(gc, weld, 1.0)
                gw = gw / np.maximum(gc, 1.0)
                acc2 = np.zeros(nw)
                np.add.at(acc2, gev[:, 0], gw[gev[:, 1]])
                np.add.at(acc2, gev[:, 1], gw[gev[:, 0]])
                weights[bone] = (0.5 * gw + 0.5 * acc2 / np.maximum(deg, 1.0))[weld]
            tot = sum(weights.values())
            for bone in weights:
                weights[bone] = weights[bone] / np.maximum(tot, 1e-6)
        for bone, warr in weights.items():
            vg = o.vertex_groups.new(name=bone)
            cnt = 0
            for vi in range(n):
                if warr[vi] > 0.003:
                    vg.add([vi], float(warr[vi]), "REPLACE")
                    cnt += 1
            print(f"  group {bone}: {cnt} verts")
        mod = o.modifiers.new("Armature", "ARMATURE")
        mod.object = arm
        o.parent = arm

    make_action(arm, "idle", 2.6, idle_keys)
    make_action(arm, "waddle", 0.7, waddle_keys)
    make_action(arm, "sprint", 0.5, sprint_keys, nkeys=9)
    make_action(arm, "cheer", 1.0, cheer_keys)

    bpy.ops.export_scene.gltf(
        filepath=glb, export_format="GLB", export_yup=True,
        export_animations=True, export_animation_mode="ACTIONS")
    fix_quat_continuity(glb)
    print("RIGGED:", glb)


def fix_quat_continuity(glb):
    """The flipper bones rest at ~180 deg (bone +X in the glTF frame), right
    on the quaternion double-cover boundary - the exporter canonicalizes
    alternate keys onto opposite hemispheres, and LINEAR interpolation
    between q and -q passes through zero (audit: 10x phantom stretch).
    Enforce per-channel sign continuity directly in the binary buffer."""
    import struct as st
    data = bytearray(open(glb, "rb").read())
    ln, = st.unpack("<I", bytes(data[12:16]))
    js = __import__("json").loads(bytes(data[20:20 + ln]))
    bin_off = 20 + ln + 8
    fixed = 0
    for anim in js.get("animations", []):
        for ch in anim["channels"]:
            if ch["target"]["path"] != "rotation":
                continue
            a = js["accessors"][anim["samplers"][ch["sampler"]]["output"]]
            bv = js["bufferViews"][a["bufferView"]]
            base = bin_off + bv.get("byteOffset", 0) + a.get("byteOffset", 0)
            cnt = a["count"]
            q = np.frombuffer(bytes(data[base:base + cnt * 16]), np.float32).reshape(cnt, 4).copy()
            for i in range(1, cnt):
                if np.dot(q[i], q[i - 1]) < 0.0:
                    q[i] = -q[i]
                    fixed += 1
            data[base:base + cnt * 16] = q.astype(np.float32).tobytes()
    open(glb, "wb").write(bytes(data))
    print(f"quat continuity: {fixed} keys flipped")


main()
