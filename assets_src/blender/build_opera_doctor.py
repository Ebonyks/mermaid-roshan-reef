#!/usr/bin/env python3
"""Opera job 3D batch 5 — Doctor mechanic props.

SPECIES LOCK (handoff continuity rule): the patient is always ONE coral
five-armed starfish plush — never any other animal. Body radius and arm
layout match the primitive exactly so the runtime boo-boo/heart/band
attachment points still land on its surface. Face states: StateIdle
(worried) -> StateComplete (happy + blush). Blender -Y = stage front."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opera_shared as S
from opera_shared import (mat, empty, cyl, sph, box, torus, export_glb,
                          qa_render, ROOT, CREAM, BRASS, PEARL, CORAL_L)
import bpy, math

S.OUT = os.path.join(ROOT, "assets/opera/jobs/doctor")
S.QA = os.path.join(ROOT, "assets_src/blender/qa_doctor")
os.makedirs(S.OUT, exist_ok=True)
os.makedirs(S.QA, exist_ok=True)

STAR = mat("starfish", (0.95, 0.55, 0.45))       # coral plush
STAR_L = mat("starfish_l", (0.98, 0.68, 0.58))
INK = mat("face_ink", (0.12, 0.1, 0.22))
BLUSH = mat("blush", (0.98, 0.45, 0.5))
TEALP = mat("teal_ped", (0.75, 0.85, 0.9))
SCOPE = mat("scope_navy", (0.35, 0.4, 0.55))
THERMO_W = mat("thermo_white", (0.96, 0.97, 1.0))

def pedestal(parent):
    cyl("Ped", TEALP, parent, r=1.2, depth=0.4, loc=(0, 0, 0.2))
    torus("PedTrim", BRASS, parent, R=1.15, r=0.06, loc=(0, 0, 0.4))

def patient():
    root = empty("OperaDoctorPatient")
    vis = empty("Visual", root)
    body = empty("Shell", vis)
    sph("Body", STAR, body, r=1.6, scale=(1, 1, 0.85))
    for i in range(5):
        a = i * math.tau / 5.0 + 0.3
        # act XZ plane -> Blender X,-Y (front = -Y)
        arm = sph("Arm%d" % i, STAR_L, body, r=0.62,
                  loc=(math.cos(a) * 1.7, -math.sin(a) * 1.7, 0.2),
                  scale=(1.25, 1.25, 0.75), seg=12, rings=8)
        arm.rotation_euler = (0, 0, a)
    for i in range(3):
        sph("Dot%d" % i, STAR_L, body, r=0.18,
            loc=(math.cos(i * 2.1) * 0.7, 0.6, 1.15 + 0.1 * math.sin(i)), seg=8, rings=5)
    st_i = empty("StateIdle", vis)     # worried: button eyes, brows, small frown
    for sx in (-1, 1):
        sph("EyeW%d" % sx, INK, st_i, r=0.2, loc=(sx * 0.45, -1.15, 0.8), seg=8, rings=5)
        b = box("Brow%d" % sx, INK, st_i, size=(0.4, 0.08, 0.1),
                loc=(sx * 0.48, -1.2, 1.12), rot=(0, 0, -sx * 0.45))
    t = torus("Frown", INK, st_i, R=0.28, r=0.05, loc=(0, -1.3, 0.32),
              rot=(math.radians(80), 0, 0), scale=(1, 0.5, 1))
    st_c = empty("StateComplete", vis)  # happy: closed arc eyes, smile, blush
    for sx in (-1, 1):
        torus("EyeH%d" % sx, INK, st_c, R=0.2, r=0.05, loc=(sx * 0.45, -1.15, 0.85),
              rot=(math.radians(80), 0, 0), scale=(1, 0.5, 1))
        sph("Blush%d" % sx, BLUSH, st_c, r=0.17, loc=(sx * 0.8, -1.05, 0.55),
            scale=(1, 0.5, 0.7), seg=8, rings=5)
    torus("Smile", INK, st_c, R=0.34, r=0.06, loc=(0, -1.28, 0.4),
          rot=(math.radians(100), 0, 0), scale=(1, 0.6, 1))
    empty("FXAnchor", root, (0, 0, 2.2))
    return root

def stethoscope():
    root = empty("OperaDoctorScope")
    vis = empty("Visual", root)
    pedestal(vis)
    tube = empty("Tube", vis, (0, 0, 0.4))
    t = torus("TubeArc", SCOPE, tube, R=0.75, r=0.09, loc=(0, 0, 1.3),
              rot=(math.radians(90), 0, 0))
    for sx in (-1, 1):
        cyl("Ear%d" % sx, BRASS, tube, r=0.09, depth=0.5,
            loc=(sx * 0.72, 0, 1.85), rot=(0, sx * 0.35, 0))
        sph("EarTip%d" % sx, BRASS, tube, r=0.13, loc=(sx * 0.86, 0, 2.1), seg=8, rings=5)
    cyl("Stem", SCOPE, tube, r=0.09, depth=0.9, loc=(0, -0.2, 0.45), rot=(math.radians(20), 0, 0))
    cyl("ChestPad", THERMO_W, tube, r=0.42, depth=0.18, loc=(0, -0.45, 0.1))
    torus("PadRim", BRASS, tube, R=0.42, r=0.06, loc=(0, -0.45, 0.12))
    return root

def thermometer():
    root = empty("OperaDoctorThermo")
    vis = empty("Visual", root)
    pedestal(vis)
    stem = empty("Stem", vis, (0, 0, 0.4))
    stem.rotation_euler = (0, math.radians(-18), 0)
    cyl("Body", THERMO_W, stem, r=0.16, depth=2.2, loc=(0, 0, 1.3))
    sph("Bulb", STAR, stem, r=0.36, loc=(0, 0, 0.15))
    for k in range(3):
        box("Tick%d" % k, SCOPE, stem, size=(0.22, 0.06, 0.06),
            loc=(0.12, -0.13, 0.9 + k * 0.45))
    return root

def bandage():
    root = empty("OperaDoctorBandage")
    vis = empty("Visual", root)
    pedestal(vis)
    r = torus("Roll", CREAM, vis, R=0.62, r=0.3, loc=(0, 0, 1.1),
              rot=(math.radians(90), 0, 0))
    box("Tail", CREAM, vis, size=(0.55, 0.1, 1.0), loc=(0.62, -0.2, 0.6),
        rot=(math.radians(15), 0, 0))
    sph("PearlPin", PEARL, vis, r=0.14, loc=(0, -0.62, 1.1), seg=8, rings=5)
    return root

built = []
for builder, fname, tag in [(patient, "opera_doctor_patient.glb", "patient"),
                            (stethoscope, "opera_doctor_scope.glb", "scope"),
                            (thermometer, "opera_doctor_thermo.glb", "thermo"),
                            (bandage, "opera_doctor_bandage.glb", "bandage")]:
    r = builder()
    r.location = (len(built) * 6.0, 0, 0)
    export_glb(r, fname)
    built.append(r)
qa_render(built, "doctor_family")
# patient face states solo renders
p = built[0]
for st in ("StateIdle", "StateComplete"):
    for c in p.children:
        if c.name.split(".")[0] == "Visual":
            for s in c.children:
                base = s.name.split(".")[0]
                if base.startswith("State"):
                    def hide(o, h):
                        o.hide_render = h
                        for cc in o.children:
                            hide(cc, h)
                    hide(s, base != st)
    qa_render([p], "patient_" + st.lower())
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_doctor_2026-07-22.blend"))
print("DONE")
