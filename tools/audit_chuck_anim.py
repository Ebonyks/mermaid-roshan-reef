#!/usr/bin/env python3
"""
audit_chuck_anim.py — frame-by-frame audit of Chuck's animation clips against
tools/CHUCK_ANIMATION_SPEC.md.

Audits the EXPORTED GLB (what the game actually loads), not the .blend:
    blender --background --python tools/audit_chuck_anim.py -- \
        --glb assets/characters/chuck_poodle_rigged.glb --out <dir>

Outputs per clip:
  frames/<clip>_f###_side.png (+ _front for run)   every single frame
  audit_report.json                                per-criterion PASS/FAIL
  console lines:  AUDIT|<clip>|<ID>|PASS/FAIL|<measured>
Stitch strips afterwards with tools/stitch_strips.py (system python + PIL).
"""
import bpy, sys, os, math, json
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

GLB = os.path.abspath(arg("--glb", "assets/characters/chuck_poodle_rigged.glb"))
OUT = os.path.abspath(arg("--out", "tools/out/audit"))
FR_DIR = os.path.join(OUT, "frames")
os.makedirs(FR_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
scene = bpy.context.scene
scene.render.fps = 24

PAWS = ["foot_FL", "foot_FR", "foot_BL", "foot_BR"]
LOOPING = {"sit_idle", "sit_excited", "run", "wag"}

def wpos(bname, tail=False):
    pb = arm.pose.bones[bname]
    return arm.matrix_world @ (pb.tail if tail else pb.head)

# ---- rest-pose ground reference ----
arm.data.pose_position = "REST"
bpy.context.view_layer.update()
GROUND = min(wpos(p, tail=True).z for p in PAWS)
REST_HIPS_Z = wpos("hips").z
arm.data.pose_position = "POSE"
CONTACT = GROUND + 0.07

# ---- render setup ----
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "OBJECT"
for o in bpy.data.objects:
    if o.type == "MESH":
        o.color = (0.72, 0.72, 0.78, 1.0)
scene.render.resolution_x, scene.render.resolution_y = 300, 240
scene.render.use_stamp = True
scene.render.use_stamp_frame = True
scene.render.use_stamp_date = False
scene.render.use_stamp_time = False
scene.render.use_stamp_render_time = False
scene.render.use_stamp_filename = False
scene.render.use_stamp_camera = False
scene.render.use_stamp_scene = False
scene.render.stamp_font_size = 16
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
bpy.context.collection.objects.link(cam)
scene.camera = cam
# ground reference slab
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, GROUND - 0.06))
gr = bpy.context.active_object
gr.scale = (4, 4, 0.05)
gr.color = (0.5, 0.62, 0.5, 1.0)

def shoot(fname, az_deg):
    a = math.radians(az_deg)
    cam.location = Vector((math.sin(a) * 4.6, -math.cos(a) * 4.6, GROUND + 1.5))
    d = Vector((0, 0, GROUND + 0.8)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(FR_DIR, fname)
    bpy.ops.render.render(write_still=True)

def contact_windows(mask):
    """Contiguous True runs, circular. Returns list of (start, length)."""
    n = len(mask)
    if all(mask):
        return [(0, n)]
    runs, i = [], 0
    start = next(k for k in range(n) if not mask[k])
    idx = [(start + k) % n for k in range(n)]
    k = 0
    while k < n:
        if mask[idx[k]]:
            j = k
            while j < n and mask[idx[j]]:
                j += 1
            runs.append((idx[k], j - k))
            k = j
        else:
            k += 1
    return runs

def ang(q1, q2):
    return math.degrees((q1.rotation_difference(q2)).angle)

report = {}
for act in bpy.data.actions:
    name = act.name
    ad = arm.animation_data or arm.animation_data_create()
    ad.action = act
    f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
    nfr = f1 - f0 + 1
    data = {"paw": {p: [] for p in PAWS}, "rootz": [], "rootx": [], "hipsz": [],
            "nose": [], "tailtip": [], "pitch": [], "quats": [], "headang": []}
    for f in range(f0, f1 + 1):
        scene.frame_set(f)
        bpy.context.view_layer.update()
        for p in PAWS:
            data["paw"][p].append(wpos(p, tail=True))
        data["rootz"].append(wpos("root").z)
        data["rootx"].append(wpos("root").x)
        data["hipsz"].append(wpos("hips").z)
        data["nose"].append(wpos("head", tail=True))
        data["tailtip"].append(wpos("tail2", tail=True))
        hips, chest = wpos("hips"), wpos("chest")
        v = chest - hips
        data["pitch"].append(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))))
        data["quats"].append({pb.name: pb.matrix_basis.to_quaternion() for pb in arm.pose.bones})
        data["headang"].append(arm.pose.bones["head"].matrix_basis.to_quaternion())
        shoot(f"{name}_f{f - f0:03d}_side.png", 90)
        if name == "run":
            shoot(f"{name}_f{f - f0:03d}_front.png", 0)

    res = {}
    def check(cid, ok, measured):
        res[cid] = {"pass": bool(ok), "measured": measured}
        print(f"AUDIT|{name}|{cid}|{'PASS' if ok else 'FAIL'}|{measured}")

    # G1 pops
    maxpop = 0.0
    for i in range(1, nfr):
        for bn, q in data["quats"][i].items():
            maxpop = max(maxpop, ang(data["quats"][i - 1][bn], q))
    check("G1", maxpop < 30, f"max pop {maxpop:.1f}deg")
    # G2 loop closure
    if name in LOOPING:
        worst = max(ang(data["quats"][0][bn], data["quats"][-1][bn]) for bn in data["quats"][0])
        check("G2", worst < 4, f"loop gap {worst:.1f}deg")
    # G3 penetration
    dmin = min(v.z for p in PAWS for v in data["paw"][p]) - GROUND
    check("G3", dmin > -0.08, f"deepest {dmin:.3f}")
    # G4 lateral
    check("G4", max(abs(x) for x in data["rootx"]) < 0.05, f"|x| {max(abs(x) for x in data['rootx']):.3f}")

    zr = [z - min(data["rootz"]) for z in data["rootz"]]
    def drift(p):
        vs = data["paw"][p]
        return max((max(c[i] for c in vs) - min(c[i] for c in vs)) for i in range(3))
    def wag_cycles(vals):
        m = sum(vals) / len(vals)
        s = [v - m for v in vals]
        return sum(1 for i in range(1, len(s)) if s[i - 1] * s[i] < 0) / 2.0

    if name == "run":
        masks = {p: [v.z < CONTACT for v in data["paw"][p]] for p in PAWS}
        wins = {p: contact_windows(masks[p]) for p in PAWS}
        def midpt(p):
            w = max(wins[p], key=lambda r: r[1]) if wins[p] else None
            return None if w is None else (w[0] + w[1] / 2.0) % nfr
        def circoff(a, b):
            d = abs(a - b) % nfr
            return min(d, nfr - d)
        mF = [midpt("foot_FL"), midpt("foot_FR")]
        mB = [midpt("foot_BL"), midpt("foot_BR")]
        okR1 = None not in mF and circoff(*mF) <= 1.5
        okR2 = None not in mB and circoff(*mB) <= 1.5
        check("R1", okR1, f"front offset {None if None in mF else round(circoff(*mF),1)}f")
        check("R2", okR2, f"hind offset {None if None in mB else round(circoff(*mB),1)}f")
        if None not in mF and None not in mB:
            fh = circoff((mF[0] + mF[1]) / 2, (mB[0] + mB[1]) / 2) / nfr
            check("R3", 0.40 <= fh + 0.5 - abs(0.5 - fh) or 0.40 <= fh <= 0.60, f"front/hind {fh:.2f} cycle")
        else:
            check("R3", False, "missing contact")
        okR4 = all(len(wins[p]) == 1 and 3 <= wins[p][0][1] <= 9 for p in PAWS)
        check("R4", okR4, {p: wins[p] for p in PAWS})
        air = sum(1 for i in range(nfr) if not any(masks[p][i] for p in PAWS))
        check("R5", air >= 2, f"airborne {air}f")
        bob = max(zr) - min(zr)
        check("R6", 0.06 <= bob <= 0.20 and 1.5 >= wag_cycles(zr) / 1 >= 0.5, f"bob {bob:.3f}, {wag_cycles(zr):.1f} cyc")
        pr = max(data["pitch"]) - min(data["pitch"])
        check("R7", 8 <= pr <= 35, f"spine pitch range {pr:.1f}deg")

    if name in ("sit_idle", "sit_excited"):
        drop = REST_HIPS_Z - min(data["hipsz"])
        check("S1", drop >= 0.45, f"haunch drop {drop:.2f}")
        grounded = [p for p in PAWS if min(v.z for v in data["paw"][p]) < CONTACT + 0.1]
        wd = max(drift(p) for p in grounded if p != "foot_FR") if grounded else 9
        check("S2", wd < 0.06, f"paw drift {wd:.3f}")
        tr = max((max(c[i] for c in data["tailtip"]) - min(c[i] for c in data["tailtip"])) for i in range(3))
        check("S3", tr >= 0.10, f"tail travel {tr:.2f}")
        ha = max(ang(data["headang"][0], q) for q in data["headang"])
        check("S4", ha <= 12, f"head range {ha:.1f}deg")
        if name == "sit_excited":
            fr = data["paw"]["foot_FR"]
            frz = max(v.z for v in fr) - min(v.z for v in fr)
            check("E1", frz >= 0.06, f"FR paw range {frz:.3f}")
            hop = max(zr) - min(zr)
            check("E2", 0.02 <= hop <= 0.08, f"hop {hop:.3f}")
            tx = [v.x for v in data["tailtip"]]
            check("E3", wag_cycles(tx) >= 2, f"wag cycles {wag_cycles(tx):.1f}")

    if name == "pickup":
        nz = [v.z - GROUND for v in data["nose"]]
        lo = min(nz); lof = nz.index(lo)
        check("P1", lo <= 0.55, f"nose min {lo:.2f}")
        endok = ang(data["headang"][0], data["headang"][-1]) <= 15
        check("P2", 6 <= lof <= 14 and endok, f"dip@f{lof}, end gap {ang(data['headang'][0], data['headang'][-1]):.0f}deg")
        bd = max(drift(p) for p in ("foot_BL", "foot_BR"))
        check("P3", bd < 0.08, f"hind drift {bd:.3f}")

    if name == "wag":
        grounded = [p for p in PAWS if min(v.z for v in data["paw"][p]) < CONTACT + 0.1]
        wd = max(drift(p) for p in grounded) if len(grounded) >= 3 else 9
        check("W1", len(grounded) >= 3 and wd < 0.06, f"{len(grounded)} grounded, drift {wd:.3f}")
        tx = [v.x for v in data["tailtip"]]
        amp = max(tx) - min(tx)
        check("W2", amp >= 0.25, f"tail sweep {amp:.2f}")
        check("W3", wag_cycles(tx) >= 3, f"cycles {wag_cycles(tx):.1f}")
        hy = []
        for q in data["quats"]:
            e = q["hips"].to_euler()
            hy.append(math.degrees(e.z))
        yr = max(hy) - min(hy)
        check("W4", 4 <= yr <= 15, f"hip yaw range {yr:.1f}deg")

    report[name] = res

with open(os.path.join(OUT, "audit_report.json"), "w") as fh:
    json.dump(report, fh, indent=1, default=str)
fails = sum(1 for c in report.values() for r in c.values() if not r["pass"])
print(f"AUDIT_SUMMARY|clips={len(report)}|fails={fails}")
