#!/usr/bin/env python3
"""
animate_chuck.py — author Chuck's animation clips on the rig from
build_chuck_rig.py and export the game-ready GLB.

CLIPS (all in-place; main.gd moves/rotates the root node)
    sit_idle     48f loop  sitting, slow tail sweep + head tilt
    sit_excited  32f loop  sitting, fast wag, front-paw bounce (ball in air)
    run          16f loop  gallop cycle (fetch + return)
    pickup       20f once  head dips to the ball
    wag          32f loop  standing tail wag (win celebration)

USAGE
    blender --background --python tools/animate_chuck.py -- \
        --blend tools/out/chuck_rig.blend --out assets/characters/chuck_poodle_rigged.glb \
        --renders <dir> [--preview sit_idle]

--preview <clip> renders 4 frames of one clip and skips export (pose tuning).
"""
import bpy, sys, os, math
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

BLEND = os.path.abspath(arg("--blend", "tools/out/chuck_rig.blend"))
OUT = os.path.abspath(arg("--out", "assets/characters/chuck_poodle_rigged.glb"))
RENDER_DIR = os.path.abspath(arg("--renders", "tools/out"))
PREVIEW = arg("--preview", "")
os.makedirs(RENDER_DIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=BLEND)
arm_obj = bpy.data.objects["chuck_rig"]
mesh_obj = bpy.data.objects["chuck_body"]
FPS = 24
scene = bpy.context.scene
scene.render.fps = FPS

# ---------------- restore full-res texture maps ----------------
# The slim GLB kept only base color; wire the original normal + metallic-
# roughness maps (extracted to tools/out/textures) back into the material so
# the glTF exporter emits them. Node layouts follow what the exporter expects.
TEXDIR = os.path.join(os.path.dirname(BLEND), "textures")
mat = mesh_obj.data.materials[0]
nt = mat.node_tree
bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
if os.path.exists(os.path.join(TEXDIR, "normal.jpg")):
    nimg = nt.nodes.new("ShaderNodeTexImage")
    nimg.image = bpy.data.images.load(os.path.join(TEXDIR, "normal.jpg"))
    nimg.image.colorspace_settings.name = "Non-Color"
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(nimg.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    mrimg = nt.nodes.new("ShaderNodeTexImage")
    mrimg.image = bpy.data.images.load(os.path.join(TEXDIR, "metallic_roughness.jpg"))
    mrimg.image.colorspace_settings.name = "Non-Color"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(mrimg.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"])
    print("TEXTURES restored: normal + metallic_roughness")

# ---------------- pose vocabulary ----------------
# Each pose: bone -> (rx, ry, rz) degrees, plus optional "root_dz" drop in
# Blender units (dog is ~1.9 tall). Signs found by render iteration:
#   hips -X tips the pelvis under / chest up (sit direction)
#   legU +X swings the leg back, -X forward (front legs; hind mirrored by chain)
SIT_BASE = {
    "root_dz": -0.62,
    "hips": (-26, 0, 0), "spine": (-8, 0, 0), "chest": (4, 0, 0),
    "neck": (12, 0, 0), "head": (6, 0, 0),
    "tail1": (45, 0, 0), "tail2": (25, 0, 0),
    "legU_BL": (42, 0, 0), "legL_BL": (-60, 0, 0), "foot_BL": (30, 0, 0),
    "legU_BR": (42, 0, 0), "legL_BR": (-60, 0, 0), "foot_BR": (30, 0, 0),
    "legU_FL": (28, 0, 0), "legL_FL": (4, 0, 0),
    "legU_FR": (34, 0, 0), "legL_FR": (4, 0, 0),
}
STAND = {"root_dz": 0.0}

def keypose(action_pose, frame, extra=None):
    """Apply base pose + per-frame overrides, keyframe every bone + root drop."""
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
def build_sit_idle():
    act = new_action("sit_idle")
    for f, ph in [(1, 0.0), (13, 0.5), (25, 1.0), (37, 0.5), (48, 0.0)]:
        wag = math.sin(ph * math.pi) * 18
        keypose(SIT_BASE, f, {"tail2": (0, 0, wag), "tail1": (0, 0, wag * 0.5),
                              "head": (0, 0, ph * 8 - 4), "neck": (ph * 3, 0, 0)})
    return act

def build_sit_excited():
    act = new_action("sit_excited")
    for f in range(1, 33, 4):
        ph = (f - 1) / 4
        wag = (28 if ph % 2 < 1 else -28)
        hop = 0.035 if ph % 2 < 1 else 0.0
        paw = -30 if ph % 2 < 1 else -10
        keypose(SIT_BASE, f, {"tail2": (0, 0, wag), "tail1": (0, 0, wag * 0.6),
                              "root_dz": hop, "legU_FR": (paw, 0, 0),
                              "head": (-6, 0, 0), "neck": (4, 0, 0)})
    return act

def build_run():
    act = new_action("run")
    # bounding gallop: front and hind pairs out of phase, left/right staggered
    # a beat for a rotary feel, spine flexes with the stride, big air on the hop
    for i, f in enumerate([1, 5, 9, 13, 16]):
        ph = (i % 4) / 4.0
        s = math.sin(ph * 2 * math.pi)
        c = math.cos(ph * 2 * math.pi)
        s2 = math.sin((ph - 0.09) * 2 * math.pi)   # right side trails slightly
        c2 = math.cos((ph - 0.09) * 2 * math.pi)
        keypose(STAND, f, {
            "root_dz": 0.09 * abs(s) - 0.02,
            "hips": (9 * s, 0, 0), "spine": (-12 * s, 0, 0), "chest": (8 * s, 0, 0),
            "neck": (10 * s - 5, 0, 0), "head": (-8 * s, 0, 0),
            "tail1": (28 + 14 * s, 0, 0), "tail2": (18 + 8 * s, 0, 0),
            "legU_FL": (-52 * s - 8, 0, 0), "legL_FL": (42 * s + 6, 0, 0), "foot_FL": (16 * s, 0, 0),
            "legU_FR": (-52 * s2 - 8, 0, 0), "legL_FR": (42 * s2 + 6, 0, 0), "foot_FR": (16 * s2, 0, 0),
            "legU_BL": (46 * c + 8, 0, 0), "legL_BL": (-36 * c - 6, 0, 0), "foot_BL": (18 * c, 0, 0),
            "legU_BR": (46 * c2 + 8, 0, 0), "legL_BR": (-36 * c2 - 6, 0, 0), "foot_BR": (18 * c2, 0, 0),
        })
    return act

def build_pickup():
    act = new_action("pickup")
    keypose(STAND, 1)
    keypose(STAND, 8, {"root_dz": -0.06, "hips": (10, 0, 0), "spine": (14, 0, 0),
                       "chest": (16, 0, 0), "neck": (-38, 0, 0), "head": (-30, 0, 0),
                       "legU_FL": (14, 0, 0), "legU_FR": (14, 0, 0),
                       "tail1": (30, 0, 0)})
    keypose(STAND, 12, {"root_dz": -0.06, "hips": (10, 0, 0), "spine": (14, 0, 0),
                        "chest": (16, 0, 0), "neck": (-38, 0, 0), "head": (-30, 0, 0),
                        "legU_FL": (14, 0, 0), "legU_FR": (14, 0, 0),
                        "tail1": (30, 0, 0)})
    keypose(STAND, 20, {"tail1": (35, 0, 0), "tail2": (15, 0, 0), "neck": (6, 0, 0)})
    return act

def build_wag():
    act = new_action("wag")
    for f, side in [(1, 1), (9, -1), (17, 1), (25, -1), (32, 1)]:
        keypose(STAND, f, {"tail1": (40, 0, 22 * side), "tail2": (20, 0, 30 * side),
                           "hips": (0, 0, 4 * side), "head": (0, 0, -6 * side),
                           "neck": (10, 0, 0)})
    return act

BUILDERS = {"sit_idle": (build_sit_idle, 48), "sit_excited": (build_sit_excited, 32),
            "run": (build_run, 16), "pickup": (build_pickup, 20), "wag": (build_wag, 32)}

# ---------------- QA renders ----------------
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "OBJECT"
mesh_obj.color = (0.7, 0.7, 0.75, 1.0)
scene.render.resolution_x, scene.render.resolution_y = 700, 560
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
bpy.context.collection.objects.link(cam)
scene.camera = cam
# ground reference at rest-pose paw height so floor contact is judgeable
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.98))
ground = bpy.context.active_object
ground.scale = (4, 4, 0.02)
ground.color = (0.45, 0.55, 0.45, 1.0)

def shoot(fname, az_deg, el=0.5):
    a = math.radians(az_deg)
    r = 5.2
    cam.location = Vector((math.sin(a) * r, -math.cos(a) * r, el * 2.2))
    d = Vector((0, 0, -0.15)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(RENDER_DIR, fname)
    bpy.ops.render.render(write_still=True)

def qa(clip, frames):
    for f in frames:
        scene.frame_set(f)
        bpy.context.view_layer.update()
        shoot(f"anim_{clip}_f{f:02d}_side.png", 90)
        shoot(f"anim_{clip}_f{f:02d}_3q.png", 40)

if PREVIEW == "sit_tune":
    # grid-search the sit pose: 3 hips angles x 3 root drops, one render each
    act = new_action("sit_tune")
    f = 1
    variants = []
    for hip in (-18, -26, -34):
        for dz in (-0.55, -0.75, -0.95):
            p = dict(SIT_BASE)
            p["root_dz"] = dz
            p["hips"] = (hip, 0, 0)
            p["neck"] = (12, 0, 0)
            p["head"] = (6, 0, 0)
            fold = -hip + 16
            p["legU_BL"] = p["legU_BR"] = (fold, 0, 0)
            p["legL_BL"] = p["legL_BR"] = (-60, 0, 0)
            p["foot_BL"] = p["foot_BR"] = (30, 0, 0)
            p["legU_FL"] = (-hip + 2, 0, 0)
            p["legU_FR"] = (-hip + 8, 0, 0)
            p["legL_FL"] = p["legL_FR"] = (4, 0, 0)
            keypose(p, f)
            variants.append((f, hip, dz))
            f += 1
    for fr, hip, dz in variants:
        scene.frame_set(fr)
        bpy.context.view_layer.update()
        shoot(f"tune_sit_h{-hip}_d{int(-dz*100)}.png", 90)
    print("PREVIEW done: sit_tune")
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

# QA one representative frame per clip
for name, length in acts:
    tr = arm_obj.animation_data.nla_tracks[name]
    tr.mute = False
scene.frame_set(1)

# ---------------- export ----------------
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
