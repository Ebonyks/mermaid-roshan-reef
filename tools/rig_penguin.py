#!/usr/bin/env python3
"""
rig_penguin.py — Blender bootstrap: skeleton + basic clips for the GEN2
penguin (same pipeline family as build_npc_rig.py / roshan_v2_retarget.py).

The Meshy penguin is a static statue (0 skins / 0 animations). The slide
chase, the cheer squad and the portal NPC all need real motion, so this
script rigs it in place:

  root -> body -> head
               -> flipperL / flipperR
               -> tailB

Weights are region-based with smooth blend bands (the penguin is a blob —
bone-heat weighting is unnecessary AND it fails silently on Meshy meshes,
see the Roshan V2 retarget notes). Four looping clips are keyframed:

  idle    2.6s  breathing bob, slow head tilt, tiny flipper drift
  waddle  0.7s  body roll, alternating flippers, counter head-tilt
  sprint  0.45s waddle at 1.4x amplitude + forward lean
  cheer   1.0s  both flippers pumping overhead, head up, hop

Frame conventions (Blender, after glTF import): head -Y, up +Z, width X.
Flipper flap = local-X rotation (bone points outward along +/-X).

USAGE:
    blender -b --python tools/rig_penguin.py -- assets/props/gen2/penguin.glb
"""
import bpy
import sys
import math
import numpy as np

FPS = 24

BONES = {
    #  name       parent      head                 tail
    "root":     (None,       (0.0, 0.10, -0.50), (0.0, 0.10, -0.20)),
    "body":     ("root",     (0.0, 0.30, -0.28), (0.0, -0.10, 0.12)),
    "head":     ("body",     (0.0, -0.42, 0.10), (0.0, -0.80, 0.26)),
    "flipperL": ("body",     (0.42, 0.02, 0.02), (0.72, 0.06, -0.10)),
    "flipperR": ("body",     (-0.42, 0.02, 0.02), (-0.72, 0.06, -0.10)),
    "tailB":    ("body",     (0.0, 0.60, -0.08), (0.0, 0.92, -0.02)),
}


def smooth(a, lo, hi):
    return np.clip((a - lo) / max(hi - lo, 1e-6), 0.0, 1.0)


def build_weights(vco):
    """region weights per vertex: dict bone -> (n,) array, normalized."""
    x, y = vco[:, 0], vco[:, 1]
    w = {}
    w["head"] = smooth(-y, 0.32, 0.46)
    w["flipperL"] = smooth(x, 0.34, 0.48)
    w["flipperR"] = smooth(-x, 0.34, 0.48)
    w["tailB"] = smooth(y, 0.50, 0.64)
    others = w["head"] + w["flipperL"] + w["flipperR"] + w["tailB"]
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


def make_action(arm, name, length_s, keys_fn):
    action = bpy.data.actions.new(name)
    arm.animation_data_create()
    arm.animation_data.action = action
    frames = int(length_s * FPS)
    keys_fn(arm.pose.bones, frames)
    action.frame_range  # touch to finalize
    # push to NLA (muted) so the ACTIONS exporter picks every clip up
    track = arm.animation_data.nla_tracks.new()
    track.name = name
    strip = track.strips.new(name, 1, action)
    strip.mute = True
    return action


def idle_keys(pb, frames):
    for i in range(5):
        f = 1 + i * (frames // 4)
        t = i / 4.0 * math.tau
        key(pb["head"], f, rot=(math.sin(t) * 0.08, math.sin(t * 0.5) * 0.05, 0))
        key(pb["flipperL"], f, rot=(math.sin(t) * 0.10, 0, 0))
        key(pb["flipperR"], f, rot=(-math.sin(t) * 0.10, 0, 0))
        key(pb["body"], f, rot=(0, math.sin(t) * 0.03, 0))
        key(pb["root"], f, loc=(0, 0, 0.012 * math.sin(t)))


def waddle_keys(pb, frames, amp=1.0, lean=0.0):
    for i in range(5):
        f = 1 + i * (frames // 4)
        t = i / 4.0 * math.tau
        s = math.sin(t)
        key(pb["body"], f, rot=(lean, s * 0.18 * amp, 0))
        key(pb["flipperL"], f, rot=(s * 0.5 * amp, 0, 0))
        key(pb["flipperR"], f, rot=(s * 0.5 * amp, 0, 0))
        key(pb["head"], f, rot=(-s * 0.08 * amp, 0, 0))
        key(pb["tailB"], f, rot=(0, -s * 0.2 * amp, 0))
        key(pb["root"], f, loc=(0, 0, 0.03 * amp * abs(math.sin(t * 2.0))))


def cheer_keys(pb, frames):
    for i in range(5):
        f = 1 + i * (frames // 4)
        t = i / 4.0 * math.tau
        pump = 0.55 + 0.35 * math.sin(t)
        key(pb["flipperL"], f, rot=(-pump, 0, 0))
        key(pb["flipperR"], f, rot=(pump, 0, 0))
        key(pb["head"], f, rot=(-0.18, 0, 0))
        key(pb["root"], f, loc=(0, 0, 0.05 * abs(math.sin(t))))
        key(pb["body"], f, rot=(-0.06, 0, 0))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    glb = argv[0]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    assert meshes, "no meshes in glb"

    # ---- armature ----
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

    # ---- skin ----
    for o in meshes:
        n = len(o.data.vertices)
        vco = np.empty(n * 3)
        o.data.vertices.foreach_get("co", vco)
        # account for object transform (Meshy meshes are usually identity)
        mw = np.array(o.matrix_world)
        co4 = np.concatenate([vco.reshape(n, 3), np.ones((n, 1))], axis=1)
        wco = (co4 @ mw.T)[:, :3]
        weights = build_weights(wco)
        for bone, warr in weights.items():
            vg = o.vertex_groups.new(name=bone)
            for vi in range(n):
                if warr[vi] > 0.003:
                    vg.add([vi], float(warr[vi]), "REPLACE")
        mod = o.modifiers.new("Armature", "ARMATURE")
        mod.object = arm
        o.parent = arm

    # ---- clips ----
    make_action(arm, "idle", 2.6, idle_keys)
    make_action(arm, "waddle", 0.7, lambda pb, fr: waddle_keys(pb, fr, 1.0, 0.0))
    make_action(arm, "sprint", 0.45, lambda pb, fr: waddle_keys(pb, fr, 1.4, 0.16))
    make_action(arm, "cheer", 1.0, cheer_keys)

    bpy.ops.export_scene.gltf(
        filepath=glb, export_format="GLB", export_yup=True,
        export_animations=True, export_animation_mode="ACTIONS")
    print("RIGGED:", glb)


main()
