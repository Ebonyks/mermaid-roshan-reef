#!/usr/bin/env python3
"""
animate_kitty.py — author the craft kitty's animation clips on the quadruped rig
from build_chuck_rig.py (run on the kitty), and export the game GLB.

Same 20-bone quadruped contract as Chuck. The kitty scan rests in a stubby,
slightly-tucked pose, so unlike Chuck we first define a STAND base that plants
all four paws flat, then author the gaits from it.

CLIPS (all in-place; the behaviour FSM in sky_lagoon.gd moves/rotates the node)
    idle   64f loop  standing breath + slow tail sway + head look
    walk   28f loop  4-beat amble, diagonal pairs, paws plant
    run    16f loop  bounding scamper (Chuck's gallop phasing, cat-scaled)
    happy  40f loop  nuzzle: head rubs side to side, tail-up, little bounce

USAGE
    blender --background --python tools/animate_kitty.py -- \
        --blend tools/out/kitty_rig.blend --out assets/props/gen2/craft_kitty_rigged.glb \
        --renders tools/out/kitty_anim [--preview run|idle|walk|happy|stand_tune]
"""
import bpy, sys, os, math
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

BLEND = os.path.abspath(arg("--blend", "tools/out/kitty_rig.blend"))
OUT = os.path.abspath(arg("--out", "assets/props/gen2/craft_kitty_rigged.glb"))
RENDER_DIR = os.path.abspath(arg("--renders", "tools/out/kitty_anim"))
PREVIEW = arg("--preview", "")
os.makedirs(RENDER_DIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=BLEND)
arm_obj = bpy.data.objects["chuck_rig"]   # build_chuck_rig names them chuck_*
mesh_obj = bpy.data.objects["chuck_body"]
FPS = 24
scene = bpy.context.scene
scene.render.fps = FPS

# ---------------- pose vocabulary ----------------
# Sign conventions (Chuck): legU +X swings leg back, -X forward; hind mirrored by
# the chain. foot +X curls the toe down. STAND extends the tucked hind legs so
# every paw sits flat on the floor (feet-flat is the whole point of this pass).
STAND = {
    "root_dz": -0.10,
    "hips": (-4, 0, 0), "spine": (0, 0, 0), "chest": (2, 0, 0),
    "neck": (6, 0, 0), "head": (2, 0, 0),
    "tail1": (18, 0, 0), "tail2": (10, 0, 0),
    "legU_BL": (10, 0, 0), "legL_BL": (-18, 0, 0), "foot_BL": (12, 0, 0),
    "legU_BR": (10, 0, 0), "legL_BR": (-18, 0, 0), "foot_BR": (12, 0, 0),
    "legU_FL": (2, 0, 0), "legL_FL": (0, 0, 0), "foot_FL": (-4, 0, 0),
    "legU_FR": (2, 0, 0), "legL_FR": (0, 0, 0), "foot_FR": (-4, 0, 0),
}

def keypose(action_pose, frame, extra=None):
    p = dict(action_pose)
    if extra:
        for k, v in extra.items():
            if k == "root_dz":
                p["root_dz"] = p.get("root_dz", 0.0) + v
            else:
                b = p.get(k, (0, 0, 0))
                p[k] = (b[0] + v[0], b[1] + v[1], b[2] + v[2])
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = "XYZ"
        rot = p.get(pb.name, (0, 0, 0))
        pb.rotation_euler = tuple(math.radians(a) for a in rot)
        pb.keyframe_insert("rotation_euler", frame=frame)
        if pb.name == "root":
            pb.location = (0, 0, p.get("root_dz", 0.0))
            pb.keyframe_insert("location", frame=frame)

def new_action(name):
    act = bpy.data.actions.new(name)
    arm_obj.animation_data_create()
    arm_obj.animation_data.action = act
    return act

def stash(act):
    tr = arm_obj.animation_data.nla_tracks.new()
    tr.name = act.name
    tr.strips.new(act.name, 1, act)
    arm_obj.animation_data.action = None

# ---------------- clips ----------------
def build_idle():
    act = new_action("idle")
    for f, ph in [(1, 0.0), (16, 0.5), (32, 1.0), (48, 0.5), (64, 0.0)]:
        br = math.sin(ph * math.pi)
        sway = math.sin(ph * 2 * math.pi)
        keypose(STAND, f, {
            "chest": (2 * br, 0, 0), "spine": (1.5 * br, 0, 0),
            "tail1": (0, 0, 6 * sway), "tail2": (0, 0, 9 * sway),
            "head": (0, 0, 6 * sway), "neck": (1.5 * br, 0, 0),
        })
    return act

def build_walk():
    act = new_action("walk")
    # 4-beat amble: diagonal pairs alternate, low lift, paws plant each cycle
    for i, f in enumerate([1, 8, 15, 22, 28]):
        ph = (i % 4) / 4.0
        s = math.sin(ph * 2 * math.pi)
        keypose(STAND, f, {
            "root_dz": 0.03 * abs(s),
            "hips": (3 * s, 0, 0), "spine": (-3 * s, 0, 0),
            "tail1": (0, 0, 8 * s), "head": (0, 0, -4 * s),
            "legU_FL": (-18 * s, 0, 0), "legL_FL": (14 * max(s, 0.0), 0, 0), "foot_FL": (8 * s, 0, 0),
            "legU_FR": (18 * s, 0, 0), "legL_FR": (14 * max(-s, 0.0), 0, 0), "foot_FR": (-8 * s, 0, 0),
            "legU_BL": (14 * s, 0, 0), "legL_BL": (-12 * max(s, 0.0), 0, 0), "foot_BL": (8 * s, 0, 0),
            "legU_BR": (-14 * s, 0, 0), "legL_BR": (-12 * max(-s, 0.0), 0, 0), "foot_BR": (-8 * s, 0, 0),
        })
    return act

def build_run():
    act = new_action("run")
    # bounding scamper: front & hind pairs out of phase, spine flexes, small air
    for i, f in enumerate([1, 5, 9, 13, 16]):
        ph = (i % 4) / 4.0
        s = math.sin(ph * 2 * math.pi)
        c = math.cos(ph * 2 * math.pi)
        s2 = math.sin((ph - 0.08) * 2 * math.pi)
        c2 = math.cos((ph - 0.08) * 2 * math.pi)
        keypose(STAND, f, {
            "root_dz": 0.11 * abs(s) - 0.02,
            "hips": (8 * s, 0, 0), "spine": (-11 * s, 0, 0), "chest": (7 * s, 0, 0),
            "neck": (9 * s - 4, 0, 0), "head": (-7 * s, 0, 0),
            "tail1": (6 + 7 * s, 0, 0), "tail2": (4 + 5 * s, 0, 0),
            "legU_FL": (-40 * s - 5, 0, 0), "legL_FL": (32 * s + 5, 0, 0), "foot_FL": (13 * s, 0, 0),
            "legU_FR": (-40 * s2 - 5, 0, 0), "legL_FR": (32 * s2 + 5, 0, 0), "foot_FR": (13 * s2, 0, 0),
            "legU_BL": (36 * c + 5, 0, 0), "legL_BL": (-28 * c - 5, 0, 0), "foot_BL": (14 * c, 0, 0),
            "legU_BR": (36 * c2 + 5, 0, 0), "legL_BR": (-28 * c2 - 5, 0, 0), "foot_BR": (14 * c2, 0, 0),
        })
    return act

# curled nap: belly to the ground, head tucked toward the tail, tail wrapped
# around the body, all four legs folded under. Slow breathing loop.
# ball curl: the spine bends SIDEWAYS (z-yaw chain) so the nose sweeps
# around toward the wrapped tail like a real cat circle — pitching the head
# down instead just buries the horn in the chest (first attempt).
SLEEP = {
    "root_dz": -0.30,
    "hips": (-12, 0, 6), "spine": (-8, 0, 10), "chest": (-4, 0, 10),
    "neck": (-16, 0, 22), "head": (-20, 0, 28),
    "tail1": (8, 0, 32), "tail2": (4, 0, 40),
    "legU_BL": (44, 0, 0), "legL_BL": (-58, 0, 0), "foot_BL": (28, 0, 0),
    "legU_BR": (44, 0, 0), "legL_BR": (-58, 0, 0), "foot_BR": (28, 0, 0),
    "legU_FL": (42, 0, 0), "legL_FL": (-55, 0, 0), "foot_FL": (28, 0, 0),
    "legU_FR": (42, 0, 0), "legL_FR": (-55, 0, 0), "foot_FR": (28, 0, 0),
}

def build_sleep():
    act = new_action("sleep")
    for f, ph in [(1, 0.0), (18, 0.5), (36, 1.0), (54, 0.5), (72, 0.0)]:
        br = math.sin(ph * math.pi)
        keypose(SLEEP, f, {
            "chest": (2.5 * br, 0, 0), "spine": (2.0 * br, 0, 0),
            "root_dz": 0.012 * br,
            "tail2": (0, 0, 3 * math.sin(ph * math.pi)),
        })
    return act

def build_happy():
    act = new_action("happy")
    # nuzzle: cheek rubs side to side, chest low, tail up and curling, tiny bounce
    for i, f in enumerate([1, 10, 20, 30, 40]):
        ph = i / 4.0
        r = math.sin(ph * 2 * math.pi)
        keypose(STAND, f, {
            "root_dz": 0.03 * abs(math.sin(ph * 4 * math.pi)),
            "chest": (6, 0, 0), "spine": (4, 0, 0),
            "neck": (-8, 0, 12 * r), "head": (-6, 0, 18 * r),
            "tail1": (-12, 0, 7 * r), "tail2": (-8, 0, 10 * r),
        })
    return act

BUILDERS = {"idle": (build_idle, 64), "walk": (build_walk, 28),
            "run": (build_run, 16), "happy": (build_happy, 40),
            "sleep": (build_sleep, 72)}

# ---------------- QA renders ----------------
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "TEXTURE"
scene.render.resolution_x, scene.render.resolution_y = 640, 520
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
bpy.context.collection.objects.link(cam)
scene.camera = cam
# ground plane at the rest-pose paw floor so foot contact is judgeable
allv = [mesh_obj.matrix_world @ v.co for v in mesh_obj.data.vertices]
zmin = min(v.z for v in allv)
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, zmin))
ground = bpy.context.active_object
ground.color = (0.5, 0.6, 0.5, 1.0)

def shoot(fname, az_deg, el=0.42):
    a = math.radians(az_deg)
    r = 5.6
    cam.location = Vector((math.sin(a) * r, -math.cos(a) * r, zmin + el * 4.0))
    d = Vector((0, 0, zmin + 0.9)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(RENDER_DIR, fname)
    bpy.ops.render.render(write_still=True)

def qa(clip, frames):
    for f in frames:
        scene.frame_set(f)
        bpy.context.view_layer.update()
        shoot("anim_%s_f%02d_side.png" % (clip, f), 90)
        shoot("anim_%s_f%02d_3q.png" % (clip, f), 40)

if PREVIEW == "stand_tune":
    # grid: hind-leg extension x root drop -> find the flat-footed stand
    f = 1
    variants = []
    for ext in (4, 10, 16):
        for dz in (-0.02, -0.10, -0.18):
            p = dict(STAND)
            p["root_dz"] = dz
            p["legU_BL"] = p["legU_BR"] = (ext, 0, 0)
            p["legL_BL"] = p["legL_BR"] = (-(ext + 8), 0, 0)
            p["foot_BL"] = p["foot_BR"] = (ext + 2, 0, 0)
            keypose(p, f)
            variants.append((f, ext, dz))
            f += 1
    for fr, ext, dz in variants:
        scene.frame_set(fr)
        bpy.context.view_layer.update()
        shoot("tune_stand_e%02d_d%02d.png" % (ext, int(-dz * 100)), 90)
    print("PREVIEW done: stand_tune")
    raise SystemExit(0)

if PREVIEW == "audit":
    # deformation report IN-SESSION (bpy 5.x re-imported actions are inert):
    # max edge stretch vs rest pose per clip; >2x reads as crumpled/nightmare
    import numpy as np
    def snapshot():
        bpy.context.view_layer.update()
        dg = bpy.context.evaluated_depsgraph_get()
        ev = mesh_obj.evaluated_get(dg)
        me = ev.to_mesh()
        n = len(me.vertices)
        co = np.empty(n * 3)
        me.vertices.foreach_get("co", co)
        co = co.reshape(n, 3)
        ed = np.empty(len(me.edges) * 2, dtype=np.int64)
        me.edges.foreach_get("vertices", ed)
        ed = ed.reshape(-1, 2)
        ev.to_mesh_clear()
        return co, ed
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
        pb.location = (0, 0, 0)
    rest_co, edges = snapshot()
    rest_len = np.linalg.norm(rest_co[edges[:, 0]] - rest_co[edges[:, 1]], axis=1)
    ok = True
    for name, (build, length) in BUILDERS.items():
        act = build()
        worst = 0.0
        wabs = 0.0
        wf = 1
        macro = rest_len >= 0.01   # micro-edges (<1% body) smear invisibly;
        for f in range(1, length + 1, max(1, length // 8)):
            scene.frame_set(f)
            co, _ = snapshot()
            ln = np.linalg.norm(co[edges[:, 0]] - co[edges[:, 1]], axis=1)
            ratio = float(np.max((ln / np.maximum(rest_len, 1e-5))[macro]))
            wabs = max(wabs, float(np.max(ln - rest_len)))
            if ratio > worst:
                worst = ratio
                wf = f
        verdict = "OK" if worst <= 2.2 and wabs <= 0.15 else "DISTORTED"
        if verdict != "OK":
            ok = False
        print("AUDIT %s: macro stretch %.2fx at f%d, max elongation %.3f  %s" % (name, worst, wf, wabs, verdict))
        arm_obj.animation_data.action = None
    print("AUDIT_RESULT:", "PASS" if ok else "FAIL")
    raise SystemExit(0)

if PREVIEW:
    build, length = BUILDERS[PREVIEW]
    build()
    qa(PREVIEW, [1, length // 3, 2 * length // 3, length])
    print("PREVIEW done:", PREVIEW)
    raise SystemExit(0)

acts = []
for name, (build, length) in BUILDERS.items():
    act = build()
    stash(act)
    acts.append((name, length))
    print("built:", name, length, "frames")
for name, length in acts:
    arm_obj.animation_data.nla_tracks[name].mute = False
scene.frame_set(1)

bpy.ops.object.select_all(action="DESELECT")
mesh_obj.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.export_scene.gltf(
    filepath=OUT, export_format="GLB", use_selection=True,
    export_animation_mode="NLA_TRACKS", export_anim_single_armature=False,
    export_skins=True, export_yup=True, export_apply=False,
)
print("EXPORTED", OUT, os.path.getsize(OUT), "bytes")
