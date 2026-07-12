#!/usr/bin/env python3
"""
rig_animate_aquatic.py — batch rig + animate the gen2 Meshy ocean creatures
and export game-ready GLBs for reef2.

Unlike Chuck (proxy bind), sea creatures get a PROCEDURAL rig: a spine chain
along the body axis with weights computed directly from vertex position
(smooth hat functions along the axis, optional side-limb masks). This is
immune to the Meshy disconnected-shell problem and needs no landmarks.

Conventions (verified by probe 2026-07-11):
  * nose faces Blender -Y  ->  glTF/Godot +Z (same as the Riley pack)
  * models baked to absolute nose-to-tail LENGTH so existing per-creature
    scale multipliers in main.gd keep working
  * swimmers: bbox center at origin; bottom dwellers: belly at z=0
  * one looping clip per creature named Swim (movers) or Idle (bottom dwellers)

USAGE
    blender --background --python tools/rig_animate_aquatic.py -- \
        [--only shark,whale] [--renders <dir>] [--outdir assets/aquatic2]
"""
import bpy, sys, os, math
import numpy as np
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

REEF2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN2 = os.path.join(os.path.dirname(REEF2), "reef2_playground_audit", "gen2", "meshy")
OUTDIR = os.path.abspath(arg("--outdir", os.path.join(REEF2, "assets", "aquatic2")))
RENDERS = os.path.abspath(arg("--renders", os.path.join(REEF2, "tools", "out", "aquatic_qa")))
ONLY = [s for s in arg("--only", "").split(",") if s]
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(RENDERS, exist_ok=True)
FPS = 24

# style: lateral (fish tail sways sideways) | vertical (fluke pumps up/down)
#        flap (side wing bones) | pulse (breathing + tentacle sway) | scuttle
# rot: extra bakes applied after import, as (axis, degrees) tuples
CONFIG = {
    "clownfish":  dict(src="aquatic_clownfish_mv", riley="ClownFish", style="lateral", bones=5, length=1.5, amp=26, period=24),
    "hammerhead": dict(src="aquatic_hammerhead_mv2", riley="Hammerhead", style="lateral", bones=6, length=3.2, amp=20, period=32,
                       rot=[("Z", 180)]),
    "shark":      dict(src="aquatic_shark_mv2", riley="Shark", style="lateral", bones=6, length=3.5, amp=20, period=32),
    "dolphin":    dict(src="aquatic_dolphin_mv", riley="Dolphin", style="vertical", bones=6, length=3.1, amp=11, period=28),
    "whale":      dict(src="aquatic_whale_mv2", riley="Whale", style="vertical", bones=6, length=3.1, amp=9, period=40),
    "penguin":    dict(src="aquatic_penguin_mv2", riley="Penguin", style="vertical", bones=5, length=1.8, amp=10, period=28),
    "turtle":     dict(src="aquatic_turtle_mv", riley="Turtle", style="flap", bones=3, length=2.8, amp=22, period=40,
                       wing_front=0.75, chain_start=0.60),
    "stingray":   dict(src="aquatic_stingray_mv2", riley="StingRay", style="flap", bones=4, length=2.5, amp=30, period=48,
                       rot=[("X", -90), ("Z", 180)], wing_front=1.0, chain_start=0.62),
    "squid":      dict(src="aquatic_squid_mv2", riley="Squid", style="pulse", bones=5, length=2.5, amp=14, period=36,
                       rot=[("Z", 180)]),
    "octopus":    dict(src="aquatic_octopus_mv2", riley="Octopus", style="pulse", bones=4, length=2.5, amp=10, period=44,
                       bottom=True, clip="Idle"),
    "crab":       dict(src="aquatic_crab_mv2", riley="Crab", style="scuttle", bones=1, length=1.75, amp=16, period=36,
                       bottom=True, clip="Idle"),
    "lobster":    dict(src="aquatic_lobster_mv2", riley="Lobster", style="scuttle", bones=2, length=1.75, amp=14, period=36,
                       bottom=True, clip="Idle"),
}

def process(name, cfg):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(GEN2, cfg["src"], "static.glb"))
    mesh_obj = next(o for o in bpy.data.objects if o.type == "MESH")
    mesh_obj.name = name
    wm = mesh_obj.matrix_world.copy()
    mesh_obj.parent = None
    mesh_obj.matrix_world = Matrix.Identity(4)
    mesh_obj.data.transform(wm)   # transform_apply no-ops headless; bake directly
    mesh_obj.data.update()
    for o in list(bpy.data.objects):
        if o.type == "EMPTY":
            bpy.data.objects.remove(o)

    def bake(mat):
        mesh_obj.data.transform(mat)
        mesh_obj.data.update()

    for axis, deg in cfg.get("rot", []):
        bake(Matrix.Rotation(math.radians(deg), 4, axis))

    # scale to target length (nose-to-tail along Y) and recenter
    vs = [v.co.copy() for v in mesh_obj.data.vertices]
    ys = sorted(v.y for v in vs)
    s = cfg["length"] / (ys[-1] - ys[0])
    bake(Matrix.Diagonal((s, s, s, 1.0)))
    vs = [v.co.copy() for v in mesh_obj.data.vertices]
    xs = sorted(v.x for v in vs); ys = sorted(v.y for v in vs); zs = sorted(v.z for v in vs)
    zoff = zs[0] if cfg.get("bottom") else (zs[0] + zs[-1]) / 2
    bake(Matrix.Translation((-(xs[0] + xs[-1]) / 2, -(ys[0] + ys[-1]) / 2, -zoff)))
    vs = [v.co.copy() for v in mesh_obj.data.vertices]
    ys = sorted(v.y for v in vs); zs = sorted(v.z for v in vs)
    y0, y1 = ys[0], ys[-1]
    zmid = (zs[0] + zs[-1]) / 2
    halfw = max(abs(v.x) for v in vs)
    print(f"{name}: len={y1 - y0:.2f} halfw={halfw:.2f} z[{zs[0]:.2f},{zs[-1]:.2f}] verts={len(vs)}")

    # ---------------- armature: root + spine chain (+ side bones) ----------------
    N = cfg["bones"]
    arm = bpy.data.armatures.new(name + "_rig")
    arm_obj = bpy.data.objects.new(name + "_rig", arm)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.edit_bones
    rootb = eb.new("root")
    rootb.head, rootb.tail = Vector((0, y0 - 0.05, zmid)), Vector((0, y0 - 0.05 + 0.1, zmid))
    # chain nose -> tail: seg boundaries; head 35% of length is the root's segment
    # so faces don't wobble: chain starts after the head segment.
    chain_start = y0 + cfg.get("chain_start", 0.35) * (y1 - y0)
    bounds = [chain_start + (y1 - chain_start) * i / N for i in range(N + 1)]
    prev = rootb
    chain = []
    for i in range(N):
        b = eb.new(f"spine{i}")
        b.head = Vector((0, bounds[i], zmid))
        b.tail = Vector((0, bounds[i + 1], zmid))
        b.parent = prev
        b.use_connect = False
        prev = b
        chain.append(f"spine{i}")
    side = []
    if cfg["style"] == "flap":
        for tag, sgn in [("wingL", 1), ("wingR", -1)]:
            b = eb.new(tag)
            b.head = Vector((sgn * 0.15 * halfw, y0 + 0.35 * (y1 - y0), zmid))
            b.tail = Vector((sgn * 0.9 * halfw, y0 + 0.35 * (y1 - y0), zmid))
            b.parent = rootb
            side.append(tag)
    if cfg["style"] == "scuttle":
        for tag, sgn in [("clawL", 1), ("clawR", -1)]:
            b = eb.new(tag)
            b.head = Vector((sgn * 0.25 * halfw, y0 + 0.30 * (y1 - y0), zmid))
            b.tail = Vector((sgn * 0.85 * halfw, y0 + 0.05 * (y1 - y0), zmid))
            b.parent = rootb
            side.append(tag)
    bpy.ops.object.mode_set(mode="OBJECT")

    # ---------------- procedural weights ----------------
    me = mesh_obj.data
    nv = len(me.vertices)
    co = np.array([v.co[:] for v in me.vertices], dtype=np.float64)
    names_all = ["root"] + chain + side
    W = np.zeros((nv, len(names_all)), dtype=np.float64)
    ci = {nm: k for k, nm in enumerate(names_all)}
    # chain hat weights along y: control points = root(=head zone) + bone centers
    centers = [chain_start - 0.5 * (chain_start - y0)] + \
              [(bounds[i] + bounds[i + 1]) / 2 for i in range(N)]
    ctrl_cols = [ci["root"]] + [ci[c] for c in chain]
    yv = co[:, 1]
    for vi in range(nv):
        y = yv[vi]
        if y <= centers[0]:
            W[vi, ctrl_cols[0]] = 1.0
            continue
        if y >= centers[-1]:
            W[vi, ctrl_cols[-1]] = 1.0
            continue
        for k in range(len(centers) - 1):
            if centers[k] <= y <= centers[k + 1]:
                t = (y - centers[k]) / (centers[k + 1] - centers[k])
                t = t * t * (3 - 2 * t)   # smoothstep blend between adjacent bones
                W[vi, ctrl_cols[k]] = 1.0 - t
                W[vi, ctrl_cols[k + 1]] = t
                break
    # side-limb masks override the chain smoothly
    if side:
        xv = co[:, 0]
        if cfg["style"] == "flap":
            # wings: beyond 30% halfwidth, front portion of the body
            yfrac = (yv - y0) / (y1 - y0)
            front = cfg.get("wing_front", 1.0)
            m = np.clip((np.abs(xv) / halfw - 0.30) / 0.25, 0, 1)
            m = np.where(yfrac < front, m, m * np.clip((1.0 - yfrac) / max(1e-5, 1.0 - front), 0, 1))
        else:
            # claws: front third, outer half
            yfrac = (yv - y0) / (y1 - y0)
            m = np.clip((np.abs(xv) / halfw - 0.35) / 0.2, 0, 1) * np.clip((0.45 - yfrac) / 0.2, 0, 1)
            m = np.clip(m, 0, 1)
        m = m * m * (3 - 2 * m)
        for tag, sgn in [(side[0], 1), (side[1], -1)]:
            mm = m * (np.sign(xv) == sgn)
            W[:, ci[tag]] = mm
        blend = np.clip(W[:, [ci[side[0]], ci[side[1]]]].sum(axis=1), 0, 1)
        for cname in ["root"] + chain:
            W[:, ci[cname]] *= (1.0 - blend)
    W /= np.maximum(W.sum(axis=1, keepdims=True), 1e-8)
    for vg in list(mesh_obj.vertex_groups):
        mesh_obj.vertex_groups.remove(vg)
    vgs = [mesh_obj.vertex_groups.new(name=nm) for nm in names_all]
    for vi in range(nv):
        for k in np.nonzero(W[vi] > 1e-4)[0]:
            vgs[k].add([vi], float(W[vi, k]), "REPLACE")
    mesh_obj.parent = arm_obj
    mod = mesh_obj.modifiers.new("Armature", "ARMATURE")
    mod.object = arm_obj

    # ---------------- animation ----------------
    clip = cfg.get("clip", "Swim")
    period = cfg["period"]
    amp = math.radians(cfg["amp"])
    act = bpy.data.actions.new(clip)
    arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = "XYZ"
    nkeys = 8
    for k in range(nkeys + 1):
        f = 1 + k * period / nkeys
        t = k / nkeys * 2 * math.pi
        style = cfg["style"]
        for i, bn in enumerate(chain):
            pb = arm_obj.pose.bones[bn]
            ramp = ((i + 1) / N) ** 1.4
            phase = t - i * 0.9
            if style == "lateral":
                pb.rotation_euler = (0, 0, amp * ramp * math.sin(phase))
            elif style == "vertical":
                pb.rotation_euler = (amp * ramp * math.sin(phase), 0, 0)
            elif style == "flap":
                pb.rotation_euler = (0.3 * amp * ramp * math.sin(phase), 0, 0)
            elif style == "pulse":
                sway = amp * ramp * math.sin(phase)
                pb.rotation_euler = (0.6 * sway, 0, 0.5 * amp * ramp * math.sin(phase * 0.7 + 1.0))
            else:  # scuttle: chain is just the body rear
                pb.rotation_euler = (0, 0, 0.3 * amp * math.sin(t))
            pb.keyframe_insert("rotation_euler", frame=f)
        for tag in side:
            pb = arm_obj.pose.bones[tag]
            if cfg["style"] == "flap":
                # both wings beat together: world flap direction flips with the
                # bone's outward direction, so mirror the sign for the R wing
                sgn = 1 if tag.endswith("L") else -1
                pb.rotation_euler = (sgn * amp * math.sin(t), 0, 0)
            else:
                sgn = 1 if tag.endswith("L") else -1
                pb.rotation_euler = (0, 0, sgn * amp * 0.7 * math.sin(t + (0 if sgn > 0 else 1.1)))
            pb.keyframe_insert("rotation_euler", frame=f)
        rootpb = arm_obj.pose.bones["root"]
        if cfg["style"] == "pulse":
            sc = 1.0 + 0.05 * math.sin(t)
            rootpb.scale = (sc, sc, 1.0 / sc)
            rootpb.keyframe_insert("scale", frame=f)
        if cfg.get("bottom"):
            rootpb.location = (0, 0, 0.03 * cfg["length"] * (0.5 + 0.5 * math.sin(t)))
            rootpb.keyframe_insert("location", frame=f)
    tr = arm_obj.animation_data.nla_tracks.new()
    tr.name = clip
    tr.strips.new(clip, 1, act)
    arm_obj.animation_data.action = None

    # ---------------- QA renders ----------------
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "TEXTURE"
    scene.render.resolution_x, scene.render.resolution_y = 480, 380
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    L = cfg["length"]
    def shoot(tag, loc):
        cam.location = Vector(loc)
        d = Vector((0, 0, 0 if not cfg.get("bottom") else 0.25 * L)) - cam.location
        cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        scene.render.filepath = os.path.join(RENDERS, f"{name}_{tag}.png")
        bpy.ops.render.render(write_still=True)
    tr.mute = False
    strip = tr.strips[0]
    strip.action_frame_start = 1
    for f, tag in [(1, "f01"), (int(period * 0.25), "f25"), (int(period * 0.5), "f50"), (int(period * 0.75), "f75")]:
        scene.frame_set(max(1, f))
        bpy.context.view_layer.update()
        shoot(f"side_{tag}", (2.0 * L, 0, 0.5 * L))
        shoot(f"top_{tag}", (0, -0.01 * L, 2.2 * L))

    # ---------------- export ----------------
    out = os.path.join(OUTDIR, cfg["riley"] + ".glb")
    bpy.ops.object.select_all(action="DESELECT")
    mesh_obj.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.export_scene.gltf(
        filepath=out, export_format="GLB", use_selection=True,
        export_animation_mode="NLA_TRACKS", export_anim_single_armature=False,
        export_skins=True, export_yup=True, export_apply=False,
    )
    print(f"EXPORTED {out} {os.path.getsize(out)} bytes")

for name, cfg in CONFIG.items():
    if ONLY and name not in ONLY:
        continue
    process(name, cfg)
print("ALL DONE")
