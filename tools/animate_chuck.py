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
    "root_dz": -0.50,
    "hips": (-26, 0, 0), "spine": (-8, 0, 0), "chest": (4, 0, 0),
    "neck": (12, 0, 0), "head": (6, 0, 0),
    "tail1": (45, 0, 0), "tail2": (25, 0, 0),
    "legU_BL": (40, 0, 0), "legL_BL": (-44, 0, 0), "foot_BL": (38, 0, 0),
    "legU_BR": (40, 0, 0), "legL_BR": (-44, 0, 0), "foot_BR": (38, 0, 0),
    "legU_FL": (28, 0, 0), "legL_FL": (4, 0, 0),
    "legU_FR": (34, 0, 0), "legL_FR": (4, 0, 0),
}
STAND = {"root_dz": 0.0}

# ---- contact solver ------------------------------------------------------
# The scan's legs have UNEQUAL rest geometry (front-right paw is curled in
# the air), so identical rotation tables put paws at different heights —
# hand-tuned tables can never give clean ground contact. Poses stay artistic;
# CONTACT is solved numerically per frame: drop/raise the root, then greedily
# bend each contact leg until its paw tail touches the ground plane.
PAWS = ("foot_FL", "foot_FR", "foot_BL", "foot_BR")

def _merge(action_pose, extra):
    p = dict(action_pose)
    if extra:
        for k, v in extra.items():
            if k == "root_dz":
                p["root_dz"] = p.get("root_dz", 0.0) + v
            else:
                b = p.get(k, (0, 0, 0))
                p[k] = (b[0] + v[0], b[1] + v[1], b[2] + v[2])
    return p

def _apply(p):
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = "XYZ"
        rot = p.get(pb.name, (0, 0, 0))
        pb.rotation_euler = tuple(math.radians(a) for a in rot)
        if pb.name == "root":
            pb.location = (0, 0, p.get("root_dz", 0.0))
    bpy.context.view_layer.update()

def _pawz(paw):
    pb = arm_obj.pose.bones[paw]
    return (arm_obj.matrix_world @ pb.tail).z

# ground = lowest paw in REST pose
arm_obj.data.pose_position = "REST"
bpy.context.view_layer.update()
GROUND = min(_pawz(p) for p in PAWS)
arm_obj.data.pose_position = "POSE"
bpy.context.view_layer.update()

def _bend_leg_to(paw, target_z, tol=0.02, iters=40):
    """Greedy per-leg bend: nudge shin then thigh, keeping whichever direction
    moves the paw toward target height."""
    chain = [paw.replace("foot_", "legL_"), paw.replace("foot_", "legU_"), paw]
    for _ in range(iters):
        err = _pawz(paw) - target_z
        if abs(err) <= tol:
            return True
        best = None
        for bn in chain:
            pb = arm_obj.pose.bones[bn]
            for step in (math.radians(3), math.radians(-3)):
                pb.rotation_euler.x += step
                bpy.context.view_layer.update()
                e = abs(_pawz(paw) - target_z)
                if best is None or e < best[0]:
                    best = (e, bn, step)
                pb.rotation_euler.x -= step
                bpy.context.view_layer.update()
        arm_obj.pose.bones[best[1]].rotation_euler.x += best[2]
        bpy.context.view_layer.update()
    return abs(_pawz(paw) - target_z) <= tol * 2

def keypose(action_pose, frame, extra=None, contact=(), clearance=None, floor_feet=(), nose_max=None):
    """Apply pose, then solve constraints, then keyframe everything.
    contact:    paws that must touch the ground this frame (root drops to the
                lowest, then each remaining paw's leg is bent down to reach).
    clearance:  minimum height of ALL paws above ground (flight frames).
    floor_feet: paws that must not be BELOW ground (raised to it if sunk)."""
    p = _merge(action_pose, extra)
    _apply(p)
    if contact:
        dz = GROUND - min(_pawz(c) for c in contact)
        arm_obj.pose.bones["root"].location.z += dz
        bpy.context.view_layer.update()
        for c in contact:
            if _pawz(c) > GROUND + 0.03:
                _bend_leg_to(c, GROUND + 0.005)
    if clearance is not None:
        # fix low paws by curling THAT leg, never by hoisting the root
        for c in PAWS:
            if _pawz(c) < GROUND + clearance:
                _bend_leg_to(c, GROUND + clearance + 0.04, tol=0.03)
    for c in floor_feet:
        if _pawz(c) < GROUND - 0.02:
            _bend_leg_to(c, GROUND + 0.01)
    if nose_max is not None:
        for _ in range(36):
            nz = (arm_obj.matrix_world @ arm_obj.pose.bones["head"].tail).z
            if nz <= GROUND + nose_max:
                break
            arm_obj.pose.bones["neck"].rotation_euler.x -= math.radians(2.5)
            arm_obj.pose.bones["head"].rotation_euler.x -= math.radians(2.0)
            bpy.context.view_layer.update()
    # key TWICE: Blender 5 slotted actions stomp the manually-set pose while
    # creating the slot on the very first insert of a fresh action, zeroing
    # that frame. Re-applying and re-keying overwrites with correct values.
    solved = snapshot_pose()
    for _pass in range(2):
        _apply(solved)
        for pb in arm_obj.pose.bones:
            pb.keyframe_insert("rotation_euler", frame=frame)
            if pb.name == "root":
                pb.keyframe_insert("location", frame=frame)

def snapshot_pose():
    """Read back the solved pose as a dict (so every key of a static clip
    reuses identical solved values -> perfect loop closure)."""
    p = {}
    for pb in arm_obj.pose.bones:
        e = pb.rotation_euler
        p[pb.name] = (math.degrees(e.x), math.degrees(e.y), math.degrees(e.z))
    p["root_dz"] = arm_obj.pose.bones["root"].location.z
    return p

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
# Solved static bases (computed once, reused for every key of a clip so
# looping clips close perfectly)
_solved = {}
def solved_base(name, pose, **solve_kw):
    if name not in _solved:
        _apply(pose)
        if solve_kw.get("contact"):
            dz = GROUND - min(_pawz(c) for c in solve_kw["contact"])
            arm_obj.pose.bones["root"].location.z += dz
            bpy.context.view_layer.update()
            for c in solve_kw["contact"]:
                if _pawz(c) > GROUND + 0.03:
                    _bend_leg_to(c, GROUND + 0.005)
        for c in solve_kw.get("floor_feet", ()):
            if _pawz(c) < GROUND - 0.02:
                _bend_leg_to(c, GROUND + 0.01)
        _solved[name] = snapshot_pose()
    return _solved[name]

GROUND_PAWS = ("foot_FL", "foot_BL", "foot_BR")   # FR is his raised signature paw

def build_sit_idle():
    act = new_action("sit_idle")
    base = solved_base("sit", SIT_BASE, floor_feet=PAWS)
    # slow symmetric tail sweep (+/-26) with a gentle head tilt; f49 == f1
    for f, sway in [(1, 0), (13, 26), (25, 0), (37, -26), (49, 0)]:
        keypose(base, f, {"tail2": (0, 0, sway * 1.2), "tail1": (0, 0, sway * 0.6),
                          "head": (0, 0, sway * 0.25), "neck": (abs(sway) * 0.1, 0, 0)})
    return act

def build_sit_excited():
    act = new_action("sit_excited")
    base = solved_base("sit", SIT_BASE, floor_feet=PAWS)
    for f in range(1, 34, 4):   # f33 repeats f1's phase: seamless loop
        ph = (f - 1) / 4
        wag = (28 if ph % 2 < 1 else -28)
        hop = 0.035 if ph % 2 < 1 else 0.0
        paw = -30 if ph % 2 < 1 else -10
        keypose(base, f, {"tail2": (0, 0, wag), "tail1": (0, 0, wag * 0.6),
                          "root_dz": hop, "legU_FR": (paw, 0, 0),
                          "head": (-6, 0, 0), "neck": (4, 0, 0)})
    return act

def build_run():
    act = new_action("run")
    # BOUND cycle, 16f, designed contact-first (audit spec R1-R7):
    #   f1-4   hind pair planted (legs near rest extension, body low) - push
    #   f5-6   extended flight (body high, spine long, front reaching)
    #   f7-10  front pair planted (front vertical under chest, body low)
    #   f11-14 gathered flight (body LOW but legs curled clear of ground)
    #   f15-16 hind extending down for next plant
    # Ground contact = leg near rest extension AND root_dz near 0.
    # One bob cycle per stride (peak at f5); paws clear ground in the gather
    # via leg curl, not body lift.
    T = {
        1:  {"root_dz": 0.02, "hips": (-2, 0, 0), "spine": (-4, 0, 0), "chest": (2, 0, 0),
             "neck": (-8, 0, 0), "head": (4, 0, 0), "tail1": (26, 0, 0), "tail2": (14, 0, 0),
             "legU_BL": (6, 0, 0), "legL_BL": (-4, 0, 0), "foot_BL": (2, 0, 0),
             "legU_BR": (6, 0, 0), "legL_BR": (-4, 0, 0), "foot_BR": (2, 0, 0),
             "legU_FL": (-46, 0, 0), "legL_FL": (30, 0, 0), "foot_FL": (12, 0, 0),
             "legU_FR": (-46, 0, 0), "legL_FR": (30, 0, 0), "foot_FR": (12, 0, 0)},
        3:  {"root_dz": 0.05, "hips": (-6, 0, 0), "spine": (2, 0, 0), "chest": (4, 0, 0),
             "neck": (-10, 0, 0), "head": (6, 0, 0), "tail1": (34, 0, 0), "tail2": (18, 0, 0),
             "legU_BL": (24, 0, 0), "legL_BL": (-12, 0, 0), "foot_BL": (16, 0, 0),
             "legU_BR": (24, 0, 0), "legL_BR": (-12, 0, 0), "foot_BR": (16, 0, 0),
             "legU_FL": (-40, 0, 0), "legL_FL": (24, 0, 0), "foot_FL": (10, 0, 0),
             "legU_FR": (-40, 0, 0), "legL_FR": (24, 0, 0), "foot_FR": (10, 0, 0)},
        5:  {"root_dz": 0.15, "hips": (-8, 0, 0), "spine": (6, 0, 0), "chest": (4, 0, 0),
             "neck": (-6, 0, 0), "head": (2, 0, 0), "tail1": (40, 0, 0), "tail2": (22, 0, 0),
             "legU_BL": (42, 0, 0), "legL_BL": (-26, 0, 0), "foot_BL": (20, 0, 0),
             "legU_BR": (42, 0, 0), "legL_BR": (-26, 0, 0), "foot_BR": (20, 0, 0),
             "legU_FL": (-34, 0, 0), "legL_FL": (14, 0, 0), "foot_FL": (6, 0, 0),
             "legU_FR": (-34, 0, 0), "legL_FR": (14, 0, 0), "foot_FR": (6, 0, 0)},
        7:  {"root_dz": 0.03, "hips": (8, 0, 0), "spine": (-10, 0, 0), "chest": (-4, 0, 0),
             "neck": (6, 0, 0), "head": (-8, 0, 0), "tail1": (22, 0, 0), "tail2": (12, 0, 0),
             "legU_BL": (-18, 0, 0), "legL_BL": (10, 0, 0), "foot_BL": (-6, 0, 0),
             "legU_BR": (-18, 0, 0), "legL_BR": (10, 0, 0), "foot_BR": (-6, 0, 0),
             "legU_FL": (-4, 0, 0), "legL_FL": (2, 0, 0), "foot_FL": (-2, 0, 0),
             "legU_FR": (-4, 0, 0), "legL_FR": (2, 0, 0), "foot_FR": (-2, 0, 0)},
        9:  {"root_dz": 0.02, "hips": (10, 0, 0), "spine": (-14, 0, 0), "chest": (-4, 0, 0),
             "neck": (8, 0, 0), "head": (-8, 0, 0), "tail1": (18, 0, 0), "tail2": (10, 0, 0),
             "legU_BL": (-30, 0, 0), "legL_BL": (16, 0, 0), "foot_BL": (-8, 0, 0),
             "legU_BR": (-30, 0, 0), "legL_BR": (16, 0, 0), "foot_BR": (-8, 0, 0),
             "legU_FL": (12, 0, 0), "legL_FL": (6, 0, 0), "foot_FL": (4, 0, 0),
             "legU_FR": (12, 0, 0), "legL_FR": (6, 0, 0), "foot_FR": (4, 0, 0)},
        11: {"root_dz": 0.07, "hips": (6, 0, 0), "spine": (-8, 0, 0), "chest": (-2, 0, 0),
             "neck": (2, 0, 0), "head": (-4, 0, 0), "tail1": (24, 0, 0), "tail2": (14, 0, 0),
             "legU_BL": (-22, 0, 0), "legL_BL": (26, 0, 0), "foot_BL": (-10, 0, 0),
             "legU_BR": (-22, 0, 0), "legL_BR": (26, 0, 0), "foot_BR": (-10, 0, 0),
             "legU_FL": (28, 0, 0), "legL_FL": (22, 0, 0), "foot_FL": (10, 0, 0),
             "legU_FR": (28, 0, 0), "legL_FR": (22, 0, 0), "foot_FR": (10, 0, 0)},
        13: {"root_dz": 0.06, "hips": (2, 0, 0), "spine": (-6, 0, 0), "chest": (0, 0, 0),
             "neck": (-4, 0, 0), "head": (0, 0, 0), "tail1": (28, 0, 0), "tail2": (16, 0, 0),
             "legU_BL": (-10, 0, 0), "legL_BL": (14, 0, 0), "foot_BL": (-4, 0, 0),
             "legU_BR": (-10, 0, 0), "legL_BR": (14, 0, 0), "foot_BR": (-4, 0, 0),
             "legU_FL": (-16, 0, 0), "legL_FL": (18, 0, 0), "foot_FL": (8, 0, 0),
             "legU_FR": (-16, 0, 0), "legL_FR": (18, 0, 0), "foot_FR": (8, 0, 0)},
        15: {"root_dz": 0.03, "hips": (0, 0, 0), "spine": (-5, 0, 0), "chest": (1, 0, 0),
             "neck": (-6, 0, 0), "head": (2, 0, 0), "tail1": (26, 0, 0), "tail2": (14, 0, 0),
             "legU_BL": (4, 0, 0), "legL_BL": (-2, 0, 0), "foot_BL": (0, 0, 0),
             "legU_BR": (4, 0, 0), "legL_BR": (-2, 0, 0), "foot_BR": (0, 0, 0),
             "legU_FL": (-32, 0, 0), "legL_FL": (26, 0, 0), "foot_FL": (10, 0, 0),
             "legU_FR": (-32, 0, 0), "legL_FR": (26, 0, 0), "foot_FR": (10, 0, 0)},
    }
    CONSTRAINTS = {
        1: {"contact": ("foot_BL", "foot_BR")},
        3: {"contact": ("foot_BL", "foot_BR")},
        5: {"clearance": 0.10},
        7: {"contact": ("foot_FL", "foot_FR")},
        9: {"contact": ("foot_FL", "foot_FR")},
        11: {"clearance": 0.07},
        13: {"clearance": 0.05},
        15: {"clearance": 0.02},
    }
    f1_solved = None
    for f, pose in T.items():
        keypose(STAND, f, pose, **CONSTRAINTS[f])
        if f == 1:
            f1_solved = snapshot_pose()
    keypose(f1_solved, 17)   # seamless loop: f17 == solved f1, cycle length 16
    return act

def build_pickup():
    act = new_action("pickup")
    # deep play-bow: nose solved down to ball height, grounded paws solved
    # onto the floor at both ends so nothing drifts
    BOW = {"root_dz": -0.20, "hips": (8, 0, 0), "spine": (14, 0, 0), "chest": (14, 0, 0),
           "neck": (-46, 0, 0), "head": (-38, 0, 0),
           "legU_FL": (-10, 0, 0), "legL_FL": (20, 0, 0), "foot_FL": (-8, 0, 0),
           "legU_FR": (-10, 0, 0), "legL_FR": (20, 0, 0), "foot_FR": (-8, 0, 0),
           "legU_BL": (-8, 0, 0), "legL_BL": (2, 0, 0), "foot_BL": (2, 0, 0),
           "legU_BR": (-8, 0, 0), "legL_BR": (2, 0, 0), "foot_BR": (2, 0, 0),
           "tail1": (32, 0, 0), "tail2": (16, 0, 0)}
    start = solved_base("stand", STAND, contact=GROUND_PAWS)
    keypose(start, 1)
    keypose(STAND, 8, BOW, contact=("foot_FL", "foot_BL", "foot_BR"),
            floor_feet=("foot_FR",), nose_max=0.50)
    bow_solved = snapshot_pose()
    keypose(bow_solved, 12)
    keypose(start, 20)
    return act

def build_wag():
    act = new_action("wag")
    # tail + butt wiggle; chest counter-yaws the hips so front paws stay put
    base = solved_base("stand", STAND, contact=GROUND_PAWS)
    for f, side in [(1, 1), (5, -1), (9, 1), (13, -1), (17, 1), (21, -1), (25, 1), (29, -1), (33, 1)]:
        keypose(base, f, {"tail1": (40, 0, 30 * side), "tail2": (20, 0, 40 * side),
                          "hips": (0, 0, 2.5 * side), "chest": (0, 0, -2.5 * side),
                          "head": (0, 0, -6 * side), "neck": (10, 0, 0)})
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
# keying diagnostics: every action's fcurve count, range, and tail2-z samples
for act in bpy.data.actions:
    for layer in act.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                fcs = list(bag.fcurves)
                tz = next((fc for fc in fcs if "tail2" in fc.data_path and fc.array_index == 2), None)
                samp = [round(math.degrees(k.co[1]), 1) for k in tz.keyframe_points] if tz else "NONE"
                print(f"DIAG|{act.name}|slot={bag.slot_handle}|fcurves={len(fcs)}|range={tuple(act.frame_range)}|tail2z={samp}")

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
