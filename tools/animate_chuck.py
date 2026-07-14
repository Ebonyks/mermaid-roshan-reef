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

LEG_BONES = tuple(f"{seg}_{tag}" for seg in ("legU", "legL", "foot")
                  for tag in ("FL", "FR", "BL", "BR"))

def keypose(action_pose, frame, extra=None, contact=(), clearance=None, floor_feet=(),
            nose_max=None, clamp_prev=None, clamp_deg=16.0, clear_paws=None):
    """Apply pose, then solve constraints, then keyframe everything.
    contact:    paws that must touch the ground this frame (root drops to the
                lowest, then each remaining paw's leg is bent down to reach).
    clearance:  minimum height of ALL paws above ground (flight frames).
    floor_feet: paws that must not be BELOW ground (raised to it if sunk).
    clamp_prev: previous frame's solved pose — leg joints are limited to
                clamp_deg of travel from it (damps solver frame-to-frame
                oscillation, which read as popping joints)."""
    p = _merge(action_pose, extra)
    _apply(p)
    _solve_constraints(contact, clearance, floor_feet, nose_max, clear_paws)
    if clamp_prev is not None:
        lim = math.radians(clamp_deg)
        changed = False
        for bn in LEG_BONES:
            cur = arm_obj.pose.bones[bn].rotation_euler.x
            prv = math.radians(clamp_prev[bn][0])
            if cur - prv > lim:
                arm_obj.pose.bones[bn].rotation_euler.x = prv + lim
                changed = True
            elif prv - cur > lim:
                arm_obj.pose.bones[bn].rotation_euler.x = prv - lim
                changed = True
        if changed:
            bpy.context.view_layer.update()
    for pb in arm_obj.pose.bones:
        pb.keyframe_insert("rotation_euler", frame=frame)
        if pb.name == "root":
            pb.keyframe_insert("location", frame=frame)

def _solve_constraints(contact=(), clearance=None, floor_feet=(), nose_max=None, clear_paws=None):
    if contact:
        # SYMMETRIC solve: root moves by the pair MEAN, then every contact paw
        # bends BOTH ways onto the target. (One-way bending made a sunken paw
        # hoist the whole root instead - phantom bob peaks, deep paws.)
        dz = (GROUND + 0.03) - sum(_pawz(c) for c in contact) / len(contact)
        arm_obj.pose.bones["root"].location.z += dz
        bpy.context.view_layer.update()
        for c in contact:
            if abs(_pawz(c) - (GROUND + 0.04)) > 0.025:
                _bend_leg_to(c, GROUND + 0.04)
    if clearance is not None:
        # fix low paws by curling THAT leg, never by hoisting the root;
        # clear_paws restricts which legs must lift (e.g. the airborne pair
        # during the other pair's plant)
        for c in (clear_paws if clear_paws is not None else PAWS):
            if _pawz(c) < GROUND + clearance:
                _bend_leg_to(c, GROUND + clearance + 0.04, tol=0.03)
    for c in floor_feet:
        if _pawz(c) < GROUND - 0.02:
            _bend_leg_to(c, GROUND + 0.01)
    if nose_max is not None:
        # measured sign convention (bow_probe): POSITIVE neck/head x lowers
        # the nose on this rig; negative orbits it upward
        for _ in range(20):   # capped assist: the BASE pose must do the work
            nz = (arm_obj.matrix_world @ arm_obj.pose.bones["head"].tail).z
            if nz <= GROUND + nose_max:
                break
            arm_obj.pose.bones["neck"].rotation_euler.x += math.radians(2.5)
            arm_obj.pose.bones["head"].rotation_euler.x += math.radians(2.0)
            bpy.context.view_layer.update()

def lerp_pose(a, b, t):
    """Cosine-eased blend of two pose dicts (all bones + root_dz)."""
    t = 0.5 - 0.5 * math.cos(t * math.pi)
    out = {}
    for k in set(a) | set(b):
        va, vb = a.get(k, (0, 0, 0)), b.get(k, (0, 0, 0))
        if k == "root_dz":
            va = a.get(k, 0.0); vb = b.get(k, 0.0)
            out[k] = va + (vb - va) * t
        else:
            out[k] = tuple(x + (y - x) * t for x, y in zip(va, vb))
    return out

def bake_clip(anchors, schedule, nframes, loop, clamp_deg=22.0):
    """Key EVERY frame: cosine-interpolate between anchor poses, then apply
    that frame's contact/clearance constraints. Sparse keys leave interpolated
    frames unconstrained (dips, phantom contacts); per-frame baking doesn't.
    anchors:  sorted [(frame, posedict), ...] spanning 1..nframes+1
    schedule: {frame: constraint-kwargs for keypose}"""
    prev_solved = None
    for f in range(1, nframes + 1):
        prev = max((af, ap) for af, ap in anchors if af <= f)
        nxt = min((af, ap) for af, ap in anchors if af >= f)
        t = 0.0 if nxt[0] == prev[0] else (f - prev[0]) / (nxt[0] - prev[0])
        keypose(lerp_pose(prev[1], nxt[1], t), f, clamp_prev=prev_solved, clamp_deg=clamp_deg,
                **schedule.get(f, {}))
        prev_solved = snapshot_pose()
        if f == 1 and loop:
            first = prev_solved
    if loop:
        keypose(first, nframes + 1)

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
    # Flush the one-time animation re-evaluation that assigning an action
    # triggers: with stashed NLA strips present it stomps the next manually
    # set pose (verified in Blender 5.1). Eat it now, before posing.
    bpy.context.view_layer.update()
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
        5:  {"root_dz": 0.10, "hips": (-8, 0, 0), "spine": (6, 0, 0), "chest": (4, 0, 0),
             "neck": (-6, 0, 0), "head": (2, 0, 0), "tail1": (40, 0, 0), "tail2": (22, 0, 0),
             "legU_BL": (48, 0, 0), "legL_BL": (-34, 0, 0), "foot_BL": (22, 0, 0),
             "legU_BR": (48, 0, 0), "legL_BR": (-34, 0, 0), "foot_BR": (22, 0, 0),
             "legU_FL": (-34, 0, 0), "legL_FL": (20, 0, 0), "foot_FL": (6, 0, 0),
             "legU_FR": (-34, 0, 0), "legL_FR": (20, 0, 0), "foot_FR": (6, 0, 0)},
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
        11: {"root_dz": 0.03, "hips": (6, 0, 0), "spine": (-8, 0, 0), "chest": (-2, 0, 0),
             "neck": (2, 0, 0), "head": (-4, 0, 0), "tail1": (24, 0, 0), "tail2": (14, 0, 0),
             "legU_BL": (-20, 0, 0), "legL_BL": (18, 0, 0), "foot_BL": (-8, 0, 0),
             "legU_BR": (-20, 0, 0), "legL_BR": (18, 0, 0), "foot_BR": (-8, 0, 0),
             "legU_FL": (28, 0, 0), "legL_FL": (26, 0, 0), "foot_FL": (10, 0, 0),
             "legU_FR": (16, 0, 0), "legL_FR": (16, 0, 0), "foot_FR": (8, 0, 0)},
        13: {"root_dz": 0.03, "hips": (2, 0, 0), "spine": (-6, 0, 0), "chest": (0, 0, 0),
             "neck": (-4, 0, 0), "head": (0, 0, 0), "tail1": (28, 0, 0), "tail2": (16, 0, 0),
             "legU_BL": (-8, 0, 0), "legL_BL": (10, 0, 0), "foot_BL": (-4, 0, 0),
             "legU_BR": (-8, 0, 0), "legL_BR": (10, 0, 0), "foot_BR": (-4, 0, 0),
             "legU_FL": (-6, 0, 0), "legL_FL": (20, 0, 0), "foot_FL": (8, 0, 0),
             "legU_FR": (-6, 0, 0), "legL_FR": (20, 0, 0), "foot_FR": (8, 0, 0)},
        15: {"root_dz": 0.03, "hips": (0, 0, 0), "spine": (-5, 0, 0), "chest": (1, 0, 0),
             "neck": (-6, 0, 0), "head": (2, 0, 0), "tail1": (26, 0, 0), "tail2": (14, 0, 0),
             "legU_BL": (4, 0, 0), "legL_BL": (-2, 0, 0), "foot_BL": (0, 0, 0),
             "legU_BR": (4, 0, 0), "legL_BR": (-2, 0, 0), "foot_BR": (0, 0, 0),
             "legU_FL": (-32, 0, 0), "legL_FL": (26, 0, 0), "foot_FL": (10, 0, 0),
             "legU_FR": (-32, 0, 0), "legL_FR": (26, 0, 0), "foot_FR": (10, 0, 0)},
    }
    # per-frame constraint schedule (baked at every frame — see bake_clip):
    # hind plant f1-4, flight f5-7, front plant f8-11, gather f12-16.
    # Clearances stay ABOVE the 0.07 contact threshold except the approach
    # frames (7, 16) which ease toward the next plant.
    # each plant also LIFTS the opposite pair — without it all four paws sat
    # on the floor through the front plant (audit v15 strips)
    HC = {"contact": ("foot_BL", "foot_BR"), "clearance": 0.18, "clear_paws": ("foot_FL", "foot_FR")}
    FC = {"contact": ("foot_FL", "foot_FR"), "clearance": 0.18, "clear_paws": ("foot_BL", "foot_BR")}
    schedule = {1: HC, 2: HC, 3: HC, 4: HC,
                5: {"clearance": 0.15}, 6: {"clearance": 0.15}, 7: {"clearance": 0.10},
                8: FC, 9: FC, 10: FC, 11: FC,
                12: {"clearance": 0.16}, 13: {"clearance": 0.16}, 14: {"clearance": 0.12},
                15: {"clearance": 0.10}, 16: {"clearance": 0.09}}
    anchors = sorted(T.items()) + [(17, T[1])]
    bake_clip(anchors, schedule, 16, loop=True, clamp_deg=26.0)
    return act

def build_pickup():
    act = new_action("pickup")
    # play-bow that PIVOTS around the hips: front end dives (chest low, elbows
    # folded), rear stays tall with hind legs counter-rotated against the hips
    # so the rear paws never leave their spots. Bending the neck alone can
    # never reach the ball - the neck JOINT has to come down.
    # Bow designed from bow_probe.py measurements: spine/chest/root lower the
    # nose with ZERO hind-paw movement (hips rotation slid the rear paws 0.4
    # and is banned here). Neck/head signs are POSITIVE-down on this rig.
    # root stays UP (root drops sank the hind paws, and re-grounding them
    # frame by frame random-walked the rear 0.3); depth comes from spine/chest
    # pivot + front legs sliding forward LOW (no fold-plunge through floor)
    BOW = {"root_dz": 0.0, "hips": (0, 0, 0), "spine": (22, 0, 0), "chest": (16, 0, 0),
           "neck": (50, 0, 0), "head": (26, 0, 0),
           "legU_FL": (-30, 0, 0), "legL_FL": (12, 0, 0), "foot_FL": (6, 0, 0),
           "legU_FR": (-30, 0, 0), "legL_FR": (12, 0, 0), "foot_FR": (6, 0, 0),
           "tail1": (38, 0, 0), "tail2": (20, 0, 0)}
    start = solved_base("stand", STAND, contact=GROUND_PAWS)
    # pre-solve the bow ONCE (per-key greedy solves each land differently and
    # made the hind paws wander between keys), then bake every frame between
    # the same two solved endpoints
    # BOW deltas go ON TOP of the solved stand: the stand calibration bends
    # each leg to the (uneven) scan ground, and the bow must inherit those
    # hind angles exactly or the rear legs animate between bent and straight
    _apply(_merge(start, BOW))
    _solve_constraints(floor_feet=("foot_FR",), nose_max=0.95)
    _bend_leg_to("foot_FL", GROUND + 0.10, tol=0.02)   # margin for importer tail synthesis
    nz = (arm_obj.matrix_world @ arm_obj.pose.bones["head"].tail).z
    print(f"PICKUP nose after solve: {nz - GROUND:.2f} above ground")
    bow = snapshot_pose()
    # crouch waypoint keeps the folding front paws ON the floor mid-path —
    # a straight joint-space lerp plunges them through it
    CROUCH = dict(start)
    for k, v in {"root_dz": -0.02, "spine": (10, 0, 0), "chest": (8, 0, 0),
                 "neck": (22, 0, 0), "head": (12, 0, 0),
                 "legU_FL": (-15, 0, 0), "legL_FL": (6, 0, 0), "foot_FL": (2, 0, 0),
                 "legU_FR": (-15, 0, 0), "legL_FR": (6, 0, 0), "foot_FR": (2, 0, 0)}.items():
        if k == "root_dz":
            CROUCH[k] = CROUCH.get(k, 0.0) + v
        else:
            b = CROUCH.get(k, (0, 0, 0))
            CROUCH[k] = (b[0] + v[0], b[1] + v[1], b[2] + v[2])
    anchors = [(1, start), (5, CROUCH), (9, bow), (13, bow), (16, CROUCH), (20, start)]
    # hind paws never dip (root stays up), so only the front pair needs floor
    # guarding — solving the hind each frame was the drift source
    schedule = {f: {"floor_feet": ("foot_FL", "foot_FR")} for f in range(2, 20)}
    bake_clip(anchors, schedule, 20, loop=False)
    for tag in ("legU_BL", "legL_BL", "foot_BL"):
        print(f"PICKDBG {tag} start={start.get(tag)} bow={bow.get(tag)}")
    for f in (1, 5, 9, 13, 17, 20):
        bpy.context.scene.frame_set(f)
        bpy.context.view_layer.update()
        pw = arm_obj.matrix_world @ arm_obj.pose.bones["foot_BL"].tail
        print(f"PICKDBG f{f} BLpaw=({pw.x:+.3f},{pw.y:+.3f},{pw.z:+.3f})")
    return act

def build_wag():
    act = new_action("wag")
    # tail + butt wiggle; chest counter-yaws the hips so front paws stay put
    base = solved_base("stand", STAND, contact=GROUND_PAWS)
    for f, side in [(1, 1), (5, -1), (9, 1), (13, -1), (17, 1), (21, -1), (25, 1), (29, -1), (33, 1)]:
        keypose(base, f, {"tail1": (40, 0, 30 * side), "tail2": (20, 0, 40 * side),
                          "hips": (0, 0, 2.5 * side), "spine": (0, 0, -2.5 * side),
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
    # LINEAR interpolation: kills Bezier overshoot (mid-segment paw dips and
    # amplified joint deltas); reads crisp at this toy scale
    for layer in act.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"
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
