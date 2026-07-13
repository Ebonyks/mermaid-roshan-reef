#!/usr/bin/env python3
"""
rig_birdie.py — the craft birdie's OWN skeleton + clips (penguin-pipeline
family: region weights on a weld map, Laplacian smoothing, stretch audit,
quaternion-continuity fix).

Unlike the toboggan penguin, the birdie STANDS: it gets real two-bone legs
(thigh + foot) so walk/run are leg-driven steps with planted feet, plus
two-bone wing chains (the fused-wing shear lesson) and a head on top.

  root -> body -> head
               -> wingL / wingL2,  wingR / wingR2
               -> tailB
               -> legL -> footL,   legR -> footR

Blender frame (matches the mesh): face -Y, up +Z, wings +-X.
The sculpt rests mid-step (left leg forward, right heel up), so every clip
starts from BASE, a stand correction that plants both feet flat.

Clips (loop; names match the sky_lagoon behaviour FSM):
  idle   2.6s  breath bob, head tilt, wing settle, tail sway — feet planted
  walk   0.9s  alternating leg steps, body roll, counter head-bob
  run    0.55s bigger faster steps, wings flare, forward lean, bounce
  happy  1.2s  nuzzle: head rubs side to side, wings flutter, tail wag, hop

USAGE:
    blender -b --python tools/rig_birdie.py -- <in.glb> <out.glb> [--audit]
    (--audit on a rigged glb prints max edge stretch per clip)
"""
import bpy
import sys
import os
import math
import numpy as np

FPS = 24
STRETCH_LIMIT = 3.2

BONES = {
    #  name      parent     head                  tail
    "root":    (None,      (0.0, 0.10, -0.95), (0.0, 0.10, -0.70)),
    "body":    ("root",    (0.0, 0.02, -0.42), (0.0, -0.02, 0.20)),
    "head":    ("body",    (0.0, -0.02, 0.32), (0.0, -0.22, 0.78)),
    "wingL":   ("body",    (0.28, 0.02, 0.05), (0.46, 0.02, -0.06)),
    "wingL2":  ("wingL",   (0.46, 0.02, -0.06), (0.62, 0.02, -0.20)),
    "wingR":   ("body",    (-0.28, 0.02, 0.05), (-0.46, 0.02, -0.06)),
    "wingR2":  ("wingR",   (-0.46, 0.02, -0.06), (-0.62, 0.02, -0.20)),
    "tailB":   ("body",    (0.0, 0.34, -0.12), (0.0, 0.54, -0.28)),
    "legL":    ("body",    (0.30, -0.02, -0.40), (0.34, -0.05, -0.68)),
    "footL":   ("legL",    (0.34, -0.05, -0.68), (0.37, -0.33, -0.90)),
    "legR":    ("body",    (-0.30, -0.02, -0.40), (-0.34, -0.05, -0.68)),
    "footR":   ("legR",    (-0.34, -0.05, -0.68), (-0.37, -0.33, -0.90)),
}


def smooth(a, lo, hi):
    return np.clip((a - lo) / max(hi - lo, 1e-6), 0.0, 1.0)


def build_weights(wco):
    """standing-bird regions (face -Y, up +Z): wings = outer-x band on the
    UPPER body; legs = below the hip line split by x sign; feet = the bottom
    of each leg; head = the top; tail = rear puff. body = the rest."""
    x, y, z = wco[:, 0], wco[:, 1], wco[:, 2]
    w = {}
    upper = smooth(z, -0.36, -0.16)          # 0 in the leg zone, 1 on the torso
    wingl = smooth(x, 0.28, 0.42) * upper
    wingr = smooth(-x, 0.28, 0.42) * upper
    outl = smooth(x, 0.44, 0.58)
    outr = smooth(-x, 0.44, 0.58)
    w["wingL"] = wingl * (1.0 - outl)
    w["wingL2"] = wingl * outl
    w["wingR"] = wingr * (1.0 - outr)
    w["wingR2"] = wingr * outr
    w["head"] = smooth(z, 0.30, 0.48) * (1.0 - wingl) * (1.0 - wingr)
    leg = smooth(-z, 0.36, 0.50)             # fades in below the hips
    foot = smooth(-z, 0.60, 0.72)            # the ankle band inside the leg
    sidel = smooth(x, 0.02, 0.16)
    sider = smooth(-x, 0.02, 0.16)
    w["legL"] = leg * sidel * (1.0 - foot)
    w["footL"] = leg * sidel * foot
    w["legR"] = leg * sider * (1.0 - foot)
    w["footR"] = leg * sider * foot
    w["tailB"] = smooth(y, 0.30, 0.44) * upper * (1.0 - wingl) * (1.0 - wingr) * (1.0 - w["head"])
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


# stand correction: the sculpt rests mid-step — square both legs under the
# body and flatten both feet so the idle stands planted (tuned by render)
BASE = {
    "legL": (0.18, 0.0, 0.0), "footL": (-0.16, 0.0, 0.0),
    "legR": (-0.06, 0.0, 0.0), "footR": (0.10, 0.0, 0.0),
}


def kb(pb, f, name, rot=(0.0, 0.0, 0.0), loc=None):
    b = BASE.get(name, (0.0, 0.0, 0.0))
    key(pb[name], f, rot=(b[0] + rot[0], b[1] + rot[1], b[2] + rot[2]), loc=loc)


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
    strip.mute = False
    arm.animation_data.action = None
    return action


def idle_keys(pb, f, t):
    kb(pb, f, "head", rot=(math.sin(t) * 0.06, 0, math.sin(t * 0.5) * 0.05))
    kb(pb, f, "wingL", rot=(math.sin(t) * 0.05, 0, 0))
    kb(pb, f, "wingL2", rot=(math.sin(t) * 0.05, 0, 0))
    kb(pb, f, "wingR", rot=(-math.sin(t) * 0.05, 0, 0))
    kb(pb, f, "wingR2", rot=(-math.sin(t) * 0.05, 0, 0))
    kb(pb, f, "tailB", rot=(0, 0, math.sin(t) * 0.10))
    kb(pb, f, "body", rot=(math.sin(t) * 0.02, 0, 0))
    key(pb["root"], f, loc=(0, 0, 0.010 * math.sin(t)))
    kb(pb, f, "legL")
    kb(pb, f, "footL")
    kb(pb, f, "legR")
    kb(pb, f, "footR")


def walk_keys(pb, f, t):
    s = math.sin(t)
    # legs alternate: thigh swings fore/aft, foot lifts on the swing leg and
    # counter-flattens on the planted leg
    kb(pb, f, "legL", rot=(s * 0.45, 0, 0))
    kb(pb, f, "footL", rot=(-max(s, 0.0) * 0.35 + max(-s, 0.0) * 0.10, 0, 0))
    kb(pb, f, "legR", rot=(-s * 0.45, 0, 0))
    kb(pb, f, "footR", rot=(-max(-s, 0.0) * 0.35 + max(s, 0.0) * 0.10, 0, 0))
    kb(pb, f, "body", rot=(0.04, s * 0.10, 0))
    kb(pb, f, "head", rot=(-s * 0.05, 0, -s * 0.04))
    kb(pb, f, "wingL", rot=(s * 0.12, 0, 0))
    kb(pb, f, "wingR", rot=(s * 0.12, 0, 0))
    kb(pb, f, "tailB", rot=(0, 0, -s * 0.14))
    key(pb["root"], f, loc=(0, 0, 0.020 * abs(math.sin(t))))


def run_keys(pb, f, t):
    s = math.sin(t)
    kb(pb, f, "legL", rot=(s * 0.75, 0, 0))
    kb(pb, f, "footL", rot=(-max(s, 0.0) * 0.5 + max(-s, 0.0) * 0.12, 0, 0))
    kb(pb, f, "legR", rot=(-s * 0.75, 0, 0))
    kb(pb, f, "footR", rot=(-max(-s, 0.0) * 0.5 + max(s, 0.0) * 0.12, 0, 0))
    kb(pb, f, "body", rot=(0.12, s * 0.06, 0))
    kb(pb, f, "head", rot=(-0.06 - s * 0.04, 0, 0))
    # wings flare out and beat with the stride
    kb(pb, f, "wingL", rot=(0.10 + s * 0.22, 0, 0.10))
    kb(pb, f, "wingL2", rot=(s * 0.18, 0, 0.14))
    kb(pb, f, "wingR", rot=(0.10 - s * 0.22, 0, -0.10))
    kb(pb, f, "wingR2", rot=(-s * 0.18, 0, -0.14))
    kb(pb, f, "tailB", rot=(-0.10, 0, s * 0.10))
    key(pb["root"], f, loc=(0, 0, -0.01 + 0.035 * abs(s)))


def happy_keys(pb, f, t):
    r = math.sin(t)
    kb(pb, f, "head", rot=(-0.10, 0.20 * r, 0.16 * r))
    kb(pb, f, "body", rot=(0.06, 0.05 * r, 0))
    kb(pb, f, "wingL", rot=(0.15 + 0.20 * abs(math.sin(t * 2)), 0, 0.08))
    kb(pb, f, "wingL2", rot=(0.15 * math.sin(t * 2), 0, 0.10))
    kb(pb, f, "wingR", rot=(0.15 + 0.20 * abs(math.cos(t * 2)), 0, -0.08))
    kb(pb, f, "wingR2", rot=(-0.15 * math.sin(t * 2), 0, -0.10))
    kb(pb, f, "tailB", rot=(0, 0, 0.28 * r))
    key(pb["root"], f, loc=(0, 0, 0.030 * abs(math.sin(t))))
    kb(pb, f, "legL")
    kb(pb, f, "footL")
    kb(pb, f, "legR")
    kb(pb, f, "footR")


def sleep_keys(pb, f, t):
    # roosting nap: crouched onto the ground, head tucked back toward a wing,
    # wings hugged in, legs folded under. Slow breath on the body.
    br = math.sin(t)
    kb(pb, f, "body", rot=(0.40 + 0.03 * br, 0, 0))
    kb(pb, f, "head", rot=(0.95, 0.50, 0.35))
    kb(pb, f, "wingL", rot=(0.34 + 0.02 * br, 0, 0.18))
    kb(pb, f, "wingL2", rot=(0.24, 0, 0.20))
    kb(pb, f, "wingR", rot=(0.34 + 0.02 * br, 0, -0.18))
    kb(pb, f, "wingR2", rot=(0.24, 0, -0.20))
    kb(pb, f, "tailB", rot=(0.10, 0, 0))
    kb(pb, f, "legL", rot=(-0.95, 0, 0))
    kb(pb, f, "footL", rot=(0.60, 0, 0))
    kb(pb, f, "legR", rot=(-0.95, 0, 0))
    kb(pb, f, "footR", rot=(0.60, 0, 0))
    key(pb["root"], f, loc=(0, 0, -0.48 + 0.012 * br))


def audit(arm, meshes):
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
    for tr in arm.animation_data.nla_tracks:
        tr.mute = True
    bpy.context.scene.frame_set(1)
    rest_co, edges = snapshot()
    rest_len = np.linalg.norm(rest_co[edges[:, 0]] - rest_co[edges[:, 1]], axis=1)
    ok = True
    for a in bpy.data.actions:
        arm.animation_data.action = a
        # Blender 5.x slotted actions: without the slot the action is inert
        # and the audit silently measures the rest pose (1.000x everywhere)
        if hasattr(arm.animation_data, "action_slot") and len(a.slots) > 0:
            arm.animation_data.action_slot = a.slots[0]
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
    out = argv[1] if len(argv) > 1 and not argv[1].startswith("--") else glb
    do_audit = "--audit" in argv
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    meshes = [o for o in bpy.data.objects if o.type == "MESH" and len(o.data.vertices) > 500]
    assert meshes, "no meshes in glb"   # >500 filters Meshy's stray env icosphere
    if do_audit:
        arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
        assert arms, "audit needs a rigged glb"
        audit(arms[0], meshes)
        return

    arm_data = bpy.data.armatures.new("BirdieRig")
    arm = bpy.data.objects.new("BirdieRig", arm_data)
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
        # weld map: coincident UV-seam twins share weights (penguin lesson)
        keys = {}
        weld = np.empty(n, dtype=np.int64)
        for vi in range(n):
            kk = (round(wco[vi, 0] * 500), round(wco[vi, 1] * 500), round(wco[vi, 2] * 500))
            weld[vi] = keys.setdefault(kk, len(keys))
        nw = len(keys)
        weights = build_weights(wco)
        for bone in weights:
            gsum = np.zeros(nw)
            gcnt = np.zeros(nw)
            np.add.at(gsum, weld, weights[bone])
            np.add.at(gcnt, weld, 1.0)
            weights[bone] = (gsum / np.maximum(gcnt, 1.0))[weld]
        # Laplacian smoothing on the welded graph (kills band-edge cliffs)
        nedge = len(o.data.edges)
        ev = np.empty(nedge * 2, dtype=np.int64)
        o.data.edges.foreach_get("vertices", ev)
        gev = weld[ev.reshape(-1, 2)]
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
    make_action(arm, "walk", 0.9, walk_keys)
    make_action(arm, "run", 0.55, run_keys, nkeys=9)
    make_action(arm, "happy", 1.2, happy_keys)
    make_action(arm, "sleep", 3.0, sleep_keys)

    if "--preview" in argv:
        # render frames of each clip IN this session (actions live here for
        # sure; re-imported GLBs animate in Godot, not reliably in bpy 5.x)
        from mathutils import Vector
        scene = bpy.context.scene
        scene.render.engine = "BLENDER_WORKBENCH"
        scene.display.shading.light = "STUDIO"
        scene.display.shading.color_type = "TEXTURE"
        scene.render.resolution_x, scene.render.resolution_y = 560, 480
        cam = bpy.data.objects.new("cam", bpy.data.cameras.new("c"))
        bpy.context.collection.objects.link(cam)
        scene.camera = cam
        allv = [meshes[0].matrix_world @ v.co for v in meshes[0].data.vertices]
        zmin = min(v.z for v in allv)
        bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, zmin))
        rd = os.path.abspath("tools/out/birdie_anim")
        os.makedirs(rd, exist_ok=True)
        for tr in arm.animation_data.nla_tracks:
            tr.mute = True
        for tr in arm.animation_data.nla_tracks:
            tr.mute = False
            frames = int(tr.strips[0].action_frame_end)
            for i in range(4):
                f = 1 + i * max(1, frames // 4)
                scene.frame_set(f)
                bpy.context.view_layer.update()
                a = math.radians(78)
                r = 5.4
                cam.location = Vector((math.sin(a) * r, -math.cos(a) * r, zmin + 1.7))
                d = Vector((0, 0, zmin + 0.85)) - cam.location
                cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
                scene.render.filepath = os.path.join(rd, "prev_%s_f%02d.png" % (tr.name, f))
                bpy.ops.render.render(write_still=True)
            tr.mute = True
        for tr in arm.animation_data.nla_tracks:
            tr.mute = False
        print("PREVIEWS:", rd)

    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(
        filepath=out, export_format="GLB", use_selection=True, export_yup=True,
        export_animations=True, export_animation_mode="NLA_TRACKS",
        export_anim_single_armature=False, export_skins=True, export_apply=False)
    fix_quat_continuity(out)
    print("RIGGED:", out)


def fix_quat_continuity(glb):
    """wing bones rest near the quaternion double-cover boundary — enforce
    per-channel sign continuity in the binary (penguin audit lesson)."""
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
