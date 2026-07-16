"""Motion-cage audit for roshan_v4: simulate every motion the game plays
(swim at 3 speeds + all 7 verbs + all paired-arm playground toy ranges,
including the idle-swim underneath and the verb blend window) exactly as
player.gd computes them, then judge each against numeric acceptance criteria.
Frame math mirrors _rot_bone/_apply_verb:
absolute pose = rest * delta; verb slerp happens in delta space (slerp is
left-invariant). glTF frame: +y up, -z her front, +x her left.
"""
import json, struct, io, sys
import numpy as np
from PIL import Image, ImageFilter

GLB = "assets/characters/roshan_v4.glb"
if "--glb" in sys.argv:
    GLB = sys.argv[sys.argv.index("--glb") + 1]
FPS = 60.0

# ---------------- GLB / skinning core ----------------
data = open(GLB, "rb").read()
clen, _ = struct.unpack_from("<II", data, 12)
gltf = json.loads(data[20:20+clen])
off = 20 + clen
blen, _ = struct.unpack_from("<II", data, off)
bin_data = data[off+8:off+8+blen]

def acc_np(idx):
    acc = gltf["accessors"][idx]
    bv = gltf["bufferViews"][acc["bufferView"]]
    start = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
    dt = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}[acc["componentType"]]
    n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}[acc["type"]]
    a = np.frombuffer(bin_data, dtype=dt, count=acc["count"]*n, offset=start)
    return a.reshape(acc["count"], n) if n > 1 else a

def quat_mat(q):
    x, y, z, w = q
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
        [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
        [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])

def aa_quat(axis, ang):
    axis = np.asarray(axis, float); axis = axis/np.linalg.norm(axis)
    s = np.sin(ang/2)
    return np.array([axis[0]*s, axis[1]*s, axis[2]*s, np.cos(ang/2)])

def qmul(a, b):
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return np.array([aw*bx+ax*bw+ay*bz-az*by, aw*by-ax*bz+ay*bw+az*bx,
                     aw*bz+ax*by-ay*bx+az*bw, aw*bw-ax*bx-ay*by-az*bz])

def qslerp(a, b, t):
    d = float(np.dot(a, b))
    if d < 0: b = -b; d = -d
    if d > 0.9995:
        r = a + t*(b-a); return r/np.linalg.norm(r)
    th = np.arccos(np.clip(d, -1, 1))
    return (np.sin((1-t)*th)*a + np.sin(t*th)*b)/np.sin(th)

nodes = gltf["nodes"]
skin = gltf["skins"][0]
joints = skin["joints"]
jname = {j: nodes[j].get("name") for j in joints}
name2j = {v: k for k, v in jname.items()}
ibm = acc_np(skin["inverseBindMatrices"]).reshape(-1, 4, 4).transpose(0, 2, 1)
parent = {}
for i, n in enumerate(nodes):
    for c in n.get("children", []):
        parent[c] = i
order = []
def topo(i):
    order.append(i)
    for c in nodes[i].get("children", []):
        topo(c)
for r in [i for i in range(len(nodes)) if i not in parent]:
    topo(r)
rest_q = {i: np.array(nodes[i].get("rotation", [0, 0, 0, 1]), float) for i in range(len(nodes))}
rest_t = {i: np.array(nodes[i].get("translation", [0, 0, 0]), float) for i in range(len(nodes))}

def joint_mats(deltas):  # deltas: bone-name -> delta quat (post-rest, local)
    G = {}
    for i in order:
        q = rest_q[i]
        nm = jname.get(i)
        if nm in deltas:
            q = qmul(q, deltas[nm])
        L = np.eye(4); L[:3, :3] = quat_mat(q); L[:3, 3] = rest_t[i]
        G[i] = (G[parent[i]] @ L) if i in parent else L
    return np.stack([G[j] @ ibm[k] for k, j in enumerate(joints)])

prims = gltf["meshes"][0]["primitives"]
prim = prims[0]
P_parts = [acc_np(p["attributes"]["POSITION"]).astype(np.float64) for p in prims]
primitive_offsets = np.cumsum([0] + [len(values) for values in P_parts[:-1]])
P0 = np.concatenate(P_parts, axis=0)
J = np.concatenate([
    acc_np(p["attributes"]["JOINTS_0"]).astype(int) for p in prims
], axis=0)
W = np.concatenate([
    acc_np(p["attributes"]["WEIGHTS_0"]).astype(np.float64) for p in prims
], axis=0)
W = W/np.maximum(W.sum(1, keepdims=True), 1e-9)

def probe_set(bone, wmin=0.12):
    k = joints.index(name2j[bone])
    sel = np.zeros(len(J), bool)
    for c in range(4):
        sel |= (J[:, c] == k) & (W[:, c] > wmin)
    return np.where(sel)[0]

PROBES = {b: probe_set(b) for b in
          ["hand", "hand2", "armF", "armF2", "head", "chest", "tail8", "finTop"]}
Ph = np.concatenate([P0, np.ones((len(P0), 1))], 1)

def probe_pos(deltas):
    M = joint_mats(deltas)
    out = {}
    for b, vi in PROBES.items():
        acc = np.zeros(3)
        pts = Ph[vi]
        Jv, Wv = J[vi], W[vi]
        S = np.zeros((len(vi), 3))
        for c in range(4):
            S += Wv[:, c][:, None] * np.einsum("nij,nj->ni", M[Jv[:, c]], pts)[:, :3]
        out[b] = S.mean(0)
    return out

def model_axis_delta(bone, axis, ang):
    rq = rest_q[name2j[bone]]
    Rr = quat_mat(rq)
    return aa_quat(Rr.T @ np.asarray(axis, float), ang)

# ---------------- player.gd motion definitions ----------------
RIGHT, UP, BACK, FWD = (1,0,0), (0,1,0), (0,0,1), (0,0,-1)
VERBS = {
 "wave": {"len":2.6,"tracks":{
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.5,2.8],[2.1,2.8],[2.6,-0.2]]},
   "armF2":{"axis":RIGHT,"keys":[[0,0],[0.6,0.55],[0.9,-0.45],[1.2,0.55],[1.5,-0.45],[1.8,0.55],[2.2,0]]},
   "head":{"axis":BACK,"keys":[[0,0],[0.7,0.16],[2.0,0.16],[2.6,0]]}}},
 "cheer": {"len":2.2,"tracks":{
   "armU":{"axis":RIGHT,"keys":[[0,-0.2],[0.4,2.45],[1.7,2.45],[2.2,-0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.4,2.502],[1.7,2.502],[2.2,-0.2]]},
   "armF":{"axis":BACK,"keys":[[0,0],[0.4,1.15],[1.7,1.15],[2.2,0]]},
   "armF2":{"axis":RIGHT,"keys":[[0,0],[0.4,0.76],[1.7,0.76],[2.2,0]]},
   "head":{"axis":RIGHT,"keys":[[0,0],[0.5,0.08],[1.7,0.08],[2.2,0]]},
   "chest":{"axis":RIGHT,"keys":[[0,0],[0.5,-0.08],[1.7,-0.08],[2.2,0]]}}},
 "clap": {"len":2.0,"tracks":{
   "armU":{"axis":RIGHT,"keys":[[0,-0.2],[0.35,1.8857],[1.7,1.8857],[2.0,-0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.35,2.2294],[1.7,2.2294],[2.0,-0.2]]},
   "armF":{"axis":BACK,"keys":[[0,0],[0.5,1.812],[0.65,1.6198],[0.8,1.812],[0.95,1.6198],[1.1,1.812],[1.25,1.6198],[1.4,1.812],[1.7,0]]},
   "armF2":{"axis":(1,0,1),"keys":[[0,0],[0.5,-0.405],[0.65,0.2239],[0.8,-0.405],[0.95,0.2239],[1.1,-0.405],[1.25,0.2239],[1.4,-0.405],[1.7,0]]}}},
 "twirl": {"len":1.9,"tracks":{
   "armU":{"axis":FWD,"keys":[[0,0],[0.4,-1.2],[1.5,-1.2],[1.9,0]]},
   "armU2":{"axis":FWD,"keys":[[0,0],[0.4,1.2],[1.5,1.2],[1.9,0]]},
   "hair1":{"axis":BACK,"keys":[[0,0],[0.9,0.3],[1.9,0]]}}},
 "look": {"len":3.4,"tracks":{
   "neck":{"axis":UP,"keys":[[0,0],[0.7,0.5],[1.4,0.5],[2.1,-0.5],[2.8,-0.5],[3.4,0]]},
   "head":{"axis":UP,"keys":[[0,0],[0.7,0.55],[1.4,0.55],[2.1,-0.55],[2.8,-0.55],[3.4,0]]}}},
 "giggle": {"len":1.5,"tracks":{
   "chest":{"axis":RIGHT,"keys":[[0,0],[0.2,-0.14],[0.4,0.02],[0.6,-0.14],[0.8,0.02],[1.0,-0.14],[1.5,0]]},
   "head":{"axis":BACK,"keys":[[0,0],[0.25,0.18],[0.55,-0.18],[0.85,0.18],[1.15,-0.18],[1.5,0]]},
   "armU":{"axis":RIGHT,"keys":[[0,-0.2],[0.3,1.74],[1.2,1.74],[1.5,-0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.3,2.22],[1.2,2.22],[1.5,-0.2]]}}},
 "sleep": {"len":6.0,"tracks":{
   "head":{"axis":RIGHT,"keys":[[0,0],[1.2,-0.5],[5.0,-0.5],[6.0,0]]},
   "neck":{"axis":RIGHT,"keys":[[0,0],[1.2,-0.32],[5.0,-0.32],[6.0,0]]},
   "chest":{"axis":RIGHT,"keys":[[0,0],[1.2,-0.26],[5.0,-0.26],[6.0,0]]},
   "armU":{"axis":RIGHT,"keys":[[0,0.2],[1.2,0.7],[5.0,0.7],[6.0,0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,0.2],[1.2,0.7],[5.0,0.7],[6.0,0.2]]},
   **{f"tail{k}":{"axis":RIGHT,"keys":[[0,0],[1.4,v],[5.0,v],[6.0,0]]}
      for k, v in [(3,-0.22),(4,-0.3),(5,-0.38),(6,-0.46),(7,-0.52),(8,-0.58)]}}},
}

def smoothstep(a, b, x):
    t = np.clip((x-a)/max(b-a, 1e-9), 0, 1)
    return t*t*(3-2*t)

def sample_keys(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for i in range(1, len(keys)):
        if t <= keys[i][0]:
            a, b = keys[i-1], keys[i]
            f = (t-a[0])/max(b[0]-a[0], 1e-3)
            return a[1] + (b[1]-a[1])*smoothstep(0, 1, f)
    return keys[-1][1]

def swim_deltas(phase, speed):
    amp = 0.10 + min(speed*0.03, 0.26)
    d = {}
    for i in range(8):
        ph = phase - i*0.45
        grow = 0.12 + 0.88*((i/7.0)**1.5)
        d[f"tail{i+1}"] = model_axis_delta(f"tail{i+1}", RIGHT, np.sin(ph)*amp*grow)
    fin = phase - 3.6
    d["finTop"] = model_axis_delta("finTop", RIGHT, np.sin(fin-0.25)*amp*0.9)
    d["finBot"] = model_axis_delta("finBot", RIGHT, np.sin(fin-0.55)*amp*0.9)
    d["spine1"] = model_axis_delta("spine1", RIGHT, -np.sin(phase)*amp*0.16)
    d["chest"] = model_axis_delta("chest", RIGHT, -np.sin(phase-0.4)*amp*0.12)
    d["neck"] = model_axis_delta("neck", RIGHT, np.sin(phase-0.7)*amp*0.06)
    d["head"] = model_axis_delta("head", BACK, np.sin(phase*0.5+0.6)*0.02)
    arm_amp = 0.06 + min(speed*0.02, 0.20)
    ap = phase*0.5
    d["armU"] = model_axis_delta("armU", RIGHT, np.sin(ap)*arm_amp)
    d["armF"] = model_axis_delta("armF", RIGHT, (np.sin(ap-0.5)+1.0)*0.5*arm_amp)
    d["armU2"] = model_axis_delta("armU2", RIGHT, np.sin(ap-0.35)*arm_amp)
    d["armF2"] = model_axis_delta("armF2", RIGHT, (np.sin(ap-0.85)+1.0)*0.5*arm_amp)
    return d

def verb_frame(vname, t, swim_d):
    spec = VERBS[vname]
    vlen = spec["len"]
    w = smoothstep(0, 0.25, t)*(1 - smoothstep(vlen-0.3, vlen, t))
    d = dict(swim_d)
    for bone, tr in spec["tracks"].items():
        if bone not in name2j: continue
        ang = sample_keys(tr["keys"], t)
        target = model_axis_delta(bone, tr["axis"], ang)
        base = swim_d.get(bone, np.array([0., 0., 0., 1.]))
        d[bone] = qslerp(base, target, w)
    return d

def track(vname, speed=0.0):
    spec = VERBS[vname]
    T = spec["len"]
    rows = []
    phase = 0.0
    for f in range(int(T*FPS)+1):
        t = f/FPS
        phase += (2.2 + speed*0.9)/FPS
        d = verb_frame(vname, t, swim_deltas(phase, speed))
        rows.append((t, probe_pos(d)))
    return rows

def swim_track(speed, seconds=3.0):
    rows = []
    phase = 0.0
    for f in range(int(seconds*FPS)):
        phase += (2.2 + speed*0.9)/FPS
        rows.append((f/FPS, probe_pos(swim_deltas(phase, speed))))
    return rows

# ---------------- criteria ----------------
REST = probe_pos({})
results = []

def check(name, cond, detail):
    results.append((name, bool(cond), detail))

# swim at 3 speeds
for speed in (0.0, 12.0, 25.0):
    rows = swim_track(speed)
    hL = np.array([r[1]["hand"] for r in rows]); hR = np.array([r[1]["hand2"] for r in rows])
    t8 = np.array([r[1]["tail8"] for r in rows])
    ampL = hL[:, 2].max()-hL[:, 2].min(); ampR = hR[:, 2].max()-hR[:, 2].min()
    check(f"swim@{speed:g} both arms move", ampL > 0.01 and ampR > 0.01,
          f"z-sweep L={ampL:.3f} R={ampR:.3f}")
    check(f"swim@{speed:g} arms stay below shoulders", hL[:, 1].max() < 0.25 and hR[:, 1].max() < 0.25,
          f"peak y L={hL[:,1].max():.2f} R={hR[:,1].max():.2f}")
    check(f"swim@{speed:g} amps comparable", 0.4 < (ampL/max(ampR, 1e-6)) < 2.5,
          f"ratio {ampL/max(ampR,1e-6):.2f}")
    check(f"swim@{speed:g} tail waves", (t8[:, 2].max()-t8[:, 2].min()) > 0.05,
          f"tail8 z-sweep {(t8[:,2].max()-t8[:,2].min()):.3f}")

# cheer: both hands high+forward, symmetric
rows = track("cheer")
hL = np.array([r[1]["hand"] for r in rows]); hR = np.array([r[1]["hand2"] for r in rows])
iL, iR = hL[:, 1].argmax(), hR[:, 1].argmax()
check("cheer both hands rise", hL[iL, 1] > 0.25 and hR[iR, 1] > 0.25,
      f"peak y L={hL[iL,1]:.2f} R={hR[iR,1]:.2f} (rest {REST['hand'][1]:.2f}/{REST['hand2'][1]:.2f})")
check("cheer hands forward not buried", hL[iL, 2] < 0.05 and hR[iR, 2] < 0.05,
      f"peak z L={hL[iL,2]:.2f} R={hR[iR,2]:.2f}")
check("cheer symmetric", abs(hL[iL, 1]-hR[iR, 1]) < 0.12, f"dy={abs(hL[iL,1]-hR[iR,1]):.2f}")
check("cheer returns to rest", np.linalg.norm(hL[-1]-REST["hand"]) < 0.15 and
      np.linalg.norm(hR[-1]-REST["hand2"]) < 0.15,
      f"end drift L={np.linalg.norm(hL[-1]-REST['hand']):.2f} R={np.linalg.norm(hR[-1]-REST['hand2']):.2f}")

# wave: right hand high, left ~static
rows = track("wave")
hL = np.array([r[1]["hand"] for r in rows]); hR = np.array([r[1]["hand2"] for r in rows])
iR = hR[:, 1].argmax()
check("wave hand raised", hR[iR, 1] > 0.3, f"peak y={hR[iR,1]:.2f}")
check("wave hand forward", hR[iR, 2] < 0.05, f"peak z={hR[iR,2]:.2f}")
wavg = hR[int(0.6*FPS):int(2.2*FPS), 0]
check("wave forearm waggles", (wavg.max()-wavg.min()) > 0.06, f"x-sweep {(wavg.max()-wavg.min()):.3f}")
check("wave other arm quiet", (hL[:, 1].max()-hL[:, 1].min()) < 0.15,
      f"L y-sweep {(hL[:,1].max()-hL[:,1].min()):.3f}")

# clap: hands converge in front at chest height
rows = track("clap")
hL = np.array([r[1]["hand"] for r in rows]); hR = np.array([r[1]["hand2"] for r in rows])
dist = np.linalg.norm(hL-hR, axis=1)
i = dist.argmin()
check("clap hands make contact", dist[i] < 0.15, f"min centroid dist {dist[i]:.3f} at t={rows[i][0]:.2f}")
check("clap in front", hL[i, 2] < 0.0 and hR[i, 2] < 0.0, f"z L={hL[i,2]:.2f} R={hR[i,2]:.2f}")
check("clap at chest height", -0.1 < hL[i, 1] < 0.48, f"y={hL[i,1]:.2f}")
mid = dist[int(0.5*FPS):int(1.5*FPS)]
check("clap rhythm (repeats)", (mid.max()-mid.min()) > 0.08, f"gap swing {(mid.max()-mid.min()):.3f}")

# twirl: arms flare laterally
rows = track("twirl")
hL = np.array([r[1]["hand"] for r in rows]); hR = np.array([r[1]["hand2"] for r in rows])
check("twirl arms flare out", (hL[:, 0].max()-REST["hand"][0]) > 0.1 and
      (REST["hand2"][0]-hR[:, 0].min()) > 0.1,
      f"dxL={(hL[:,0].max()-REST['hand'][0]):.2f} dxR={(REST['hand2'][0]-hR[:,0].min()):.2f}")

# giggle: hands toward mouth (up+forward), moderate
rows = track("giggle")
hL = np.array([r[1]["hand"] for r in rows]); hR = np.array([r[1]["hand2"] for r in rows])
iL, iR = hL[:, 1].argmax(), hR[:, 1].argmax()
check("giggle hands lift", hL[iL, 1] > 0.0 and hR[iR, 1] > 0.0,
      f"peak y L={hL[iL,1]:.2f} R={hR[iR,1]:.2f}")
check("giggle hands forward", hL[iL, 2] < 0.1 and hR[iR, 2] < 0.1,
      f"z L={hL[iL,2]:.2f} R={hR[iR,2]:.2f}")
check("giggle below cheer height", hL[iL, 1] < 0.35, f"y={hL[iL,1]:.2f}")

# look: head yaws both ways, arms still
rows = track("look")
hd = np.array([r[1]["head"] for r in rows])
hL = np.array([r[1]["hand"] for r in rows])
check("look head sweeps", (hd[:, 0].max()-hd[:, 0].min()) > 0.08,
      f"head x-sweep {(hd[:,0].max()-hd[:,0].min()):.3f}")
check("look arms quiet", (hL[:, 1].max()-hL[:, 1].min()) < 0.12,
      f"L y-sweep {(hL[:,1].max()-hL[:,1].min()):.3f}")

# sleep: slump forward, arms fold forward, tail curls forward
rows = track("sleep")
hd = np.array([r[1]["head"] for r in rows]); hL = np.array([r[1]["hand"] for r in rows])
hR = np.array([r[1]["hand2"] for r in rows]); t8 = np.array([r[1]["tail8"] for r in rows])
mid = int(3.0*FPS)
check("sleep head slumps forward", hd[mid, 2] < REST["head"][2]-0.02,
      f"head z {REST['head'][2]:.2f}->{hd[mid,2]:.2f}")
check("sleep arms fold forward", hL[mid, 2] < REST["hand"][2]+0.02 and hR[mid, 2] < REST["hand2"][2]+0.02,
      f"hand z L {REST['hand'][2]:.2f}->{hL[mid,2]:.2f} R {REST['hand2'][2]:.2f}->{hR[mid,2]:.2f}")
check("sleep tail curls", abs(t8[mid, 2]-REST["tail8"][2]) > 0.1,
      f"tail8 z {REST['tail8'][2]:.2f}->{t8[mid,2]:.2f}")

# ---------------- elbow anatomy + hyperextension ----------------
def gmats(deltas={}):
    G = {}
    for i in order:
        q = rest_q[i]
        nm = jname.get(i)
        if nm in deltas:
            q = qmul(q, deltas[nm])
        L = np.eye(4); L[:3,:3] = quat_mat(q); L[:3,3] = rest_t[i]
        G[i] = (G[parent[i]] @ L) if i in parent else L
    return G

# Playground paired-arm fit from player.gd _mirror_arm(). Independent upper/
# forearm maps cannot reconcile the two intentionally different shoulder
# frames after the localized resculpt. The symmetric modes below are actual
# simultaneous controls. The dig range is also included as a transfer probe:
# runtime alternates the two scoops, so those mapped controls are not applied
# to both arms at once. Actual alternating dig poses are audited separately.
def toy_mirror_arm(upper, forearm):
    return np.array([
        upper*0.96 + forearm*0.22 + 0.35,
        upper*0.31 + forearm*0.82 + 0.45,
    ])

toy_samples = [("swing", 1.10, 0.55), ("seat", 0.65, 0.50)]
toy_samples += [("climb", 0.35 + 1.15*p, 0.25 + 0.30*p)
                for p in np.linspace(0.0, 1.0, 13)]
toy_samples += [("ride", 1.50 - 0.80*d, 0.35)
                for d in np.linspace(0.0, 1.0, 11)]
toy_samples += [("land", -0.20 + 1.70*n, 0.35*n)
                for n in np.linspace(0.0, 1.0, 18)]
toy_samples += [("dig_transfer", 0.55 - 0.45*s, 0.30 + 0.35*s)
                for s in np.linspace(0.0, 1.0, 11)]
toy_errors = []
toy_yz_errors = []
toy_residuals = []
toy_arm2_interiors = []
dig_primary_points = []
dig_secondary_points = []
for _toy_name, upper, forearm in toy_samples:
    upper2, forearm2 = toy_mirror_arm(upper, forearm)
    deltas = {
        "armU": model_axis_delta("armU", RIGHT, upper),
        "armF": model_axis_delta("armF", RIGHT, forearm),
        "armU2": model_axis_delta("armU2", RIGHT, upper2),
        "armF2": model_axis_delta("armF2", RIGHT, forearm2),
    }
    posed = probe_pos(deltas)
    globals_ = gmats(deltas)
    shoulder = globals_[name2j["armU"]][:3, 3]
    shoulder2 = globals_[name2j["armU2"]][:3, 3]
    target = posed["hand"] - shoulder
    target[0] *= -1.0
    residual = (posed["hand2"] - shoulder2) - target
    toy_errors.append(float(np.linalg.norm(residual)))
    toy_yz_errors.append(float(np.linalg.norm(residual[1:])))
    toy_residuals.append(residual)
    if _toy_name == "dig_transfer":
        dig_primary_points.append(posed["hand"] - shoulder)
        dig_secondary_points.append(posed["hand2"] - shoulder2)
    elbow2 = globals_[name2j["armF2"]][:3, 3]
    wrist2 = globals_[name2j["hand2"]][:3, 3]
    upper_vector = (shoulder2-elbow2)/np.linalg.norm(shoulder2-elbow2)
    forearm_vector = (wrist2-elbow2)/np.linalg.norm(wrist2-elbow2)
    toy_arm2_interiors.append(float(np.degrees(np.arccos(
        np.clip(np.dot(upper_vector, forearm_vector), -1.0, 1.0)
    ))))

toy_error_rms = float(np.sqrt(np.mean(np.square(toy_errors))))
toy_error_max = max(toy_errors)
toy_yz_rms = float(np.sqrt(np.mean(np.square(toy_yz_errors))))
toy_yz_max = max(toy_yz_errors)
toy_residuals = np.asarray(toy_residuals)
toy_y_abs_max = float(np.abs(toy_residuals[:, 1]).max())
toy_z_abs_max = float(np.abs(toy_residuals[:, 2]).max())
dig_primary_sweep = float(np.linalg.norm(dig_primary_points[-1]-dig_primary_points[0]))
dig_secondary_sweep = float(np.linalg.norm(dig_secondary_points[-1]-dig_secondary_points[0]))
dig_sweep_ratio = dig_secondary_sweep/max(dig_primary_sweep, 1e-9)
check("toy mirror mapping stays paired", toy_error_rms < 0.045 and toy_error_max < 0.060 and
      toy_yz_rms < 0.020 and toy_yz_max < 0.040 and
      toy_y_abs_max < 0.040 and toy_z_abs_max < 0.040,
      f"55 mapped control states: xyz RMS={toy_error_rms:.3f} max={toy_error_max:.3f}, "
      f"yz RMS={toy_yz_rms:.3f} max={toy_yz_max:.3f}, "
      f"|dy|/|dz| max={toy_y_abs_max:.3f}/{toy_z_abs_max:.3f}")
runtime_dig_primary = []
runtime_dig_secondary = []
for scoop in np.linspace(0.0, 1.0, 11):
    idle2 = toy_mirror_arm(0.55, 0.30)
    left_active = probe_pos({
        "armU": model_axis_delta("armU", RIGHT, 0.55 - 0.45*scoop),
        "armF": model_axis_delta("armF", RIGHT, 0.30 + 0.35*scoop),
        "armU2": model_axis_delta("armU2", RIGHT, idle2[0]),
        "armF2": model_axis_delta("armF2", RIGHT, idle2[1]),
    })
    active2 = toy_mirror_arm(0.55 - 0.45*scoop, 0.30 + 0.35*scoop)
    right_active = probe_pos({
        "armU": model_axis_delta("armU", RIGHT, 0.55),
        "armF": model_axis_delta("armF", RIGHT, 0.30),
        "armU2": model_axis_delta("armU2", RIGHT, active2[0]),
        "armF2": model_axis_delta("armF2", RIGHT, active2[1]),
    })
    runtime_dig_primary.append(left_active["hand"])
    runtime_dig_secondary.append(right_active["hand2"])
runtime_dig_primary_sweep = float(np.linalg.norm(
    runtime_dig_primary[-1] - runtime_dig_primary[0]))
runtime_dig_secondary_sweep = float(np.linalg.norm(
    runtime_dig_secondary[-1] - runtime_dig_secondary[0]))
runtime_dig_sweep_ratio = runtime_dig_secondary_sweep/max(runtime_dig_primary_sweep, 1e-9)
check("runtime alternating dig sweeps stay comparable",
      0.80 <= runtime_dig_sweep_ratio <= 1.25 and
      abs(runtime_dig_sweep_ratio-dig_sweep_ratio) < 1e-6,
      f"secondary/primary endpoint sweep={runtime_dig_sweep_ratio:.3f}")
check("toy secondary elbow stays natural", min(toy_arm2_interiors) > 100.0 and
      max(toy_arm2_interiors) < 175.0,
      f"interior={min(toy_arm2_interiors):.0f}..{max(toy_arm2_interiors):.0f} deg")

ARMS = {"L": ("armU","armF","hand"), "R": ("armU2","armF2","hand2")}
G0e = gmats()
elbow_ref = {}
for side, (sh, el, wr) in ARMS.items():
    Sh, El, Wr = (G0e[name2j[b]][:3,3] for b in (sh, el, wr))
    upper = np.linalg.norm(El-Sh); fore = np.linalg.norm(Wr-El)
    check(f"elbow {side} proportions", 0.55 < fore/max(upper,1e-9) < 1.15,
          f"fore/upper={fore/max(upper,1e-9):.2f}")
    ks = [joints.index(name2j[b]) for b in (sh, el)]
    sel = np.zeros(len(J), bool)
    for c in range(4):
        for k in ks:
            sel |= (J[:,c]==k) & (W[:,c]>0.25)
    near = P0[sel][np.linalg.norm(P0[sel]-El, axis=1) < 0.09]
    off = np.linalg.norm(near.mean(0)-El) if len(near) > 10 else 99
    check(f"elbow {side} centered in arm mesh", off < 0.04, f"offset={off:.3f} (radius~0.045)")
    v1 = (Sh-El)/np.linalg.norm(Sh-El); v2 = (Wr-El)/np.linalg.norm(Wr-El)
    interior = np.degrees(np.arccos(np.clip(np.dot(v1,v2),-1,1)))
    check(f"elbow {side} rest bend natural", 140 <= interior <= 178, f"interior={interior:.0f} deg")
    check(f"shoulder {side} lateral (not in chest)", abs(Sh[0]) >= 0.11, f"|x|={abs(Sh[0]):.2f}")
    ext0 = (El-Sh)/np.linalg.norm(El-Sh)
    fr0 = np.array([0,0,-1.0]) - np.dot([0,0,-1.0], ext0)*ext0
    elbow_ref[side] = (fr0/np.linalg.norm(fr0), ext0, G0e[name2j[sh]][:3,:3])

def elbow_stats(deltas):
    G = gmats(deltas)
    o = {}
    for side, (sh, el, wr) in ARMS.items():
        Sh, El, Wr = (G[name2j[b]][:3,3] for b in (sh, el, wr))
        v2 = (Wr-El)/np.linalg.norm(Wr-El)
        fr0, ext0, R0 = elbow_ref[side]
        Rc = G[name2j[sh]][:3,:3] @ R0.T
        ang = np.degrees(np.arctan2(np.dot(v2, Rc@fr0), np.dot(v2, Rc@ext0)))
        v1 = (Sh-El)/np.linalg.norm(Sh-El)
        interior = np.degrees(np.arccos(np.clip(np.dot(v1,v2),-1,1)))
        o[side] = (ang, interior)
    return o

worst = {"L": 0.0, "R": 0.0}
worst_source = {"L": "rest", "R": "rest"}
minfold = {"L": 180.0, "R": 180.0}
def scan_hyper(label, gen):
    for frame_index, d in enumerate(gen):
        st = elbow_stats(d)
        for s2 in ("L","R"):
            ang, inter = st[s2]
            if ang < worst[s2]:
                worst[s2] = ang
                worst_source[s2] = f"{label}@{frame_index / FPS:.2f}s"
            minfold[s2] = min(minfold[s2], inter)
for speed in (0.0, 25.0):
    def sg(spd=speed):
        ph = 0.0
        for f in range(180):
            ph += (2.2+spd*0.9)/FPS
            yield swim_deltas(ph, spd)
    scan_hyper(f"swim@{speed:g}", sg())
for vn in VERBS:
    vlen = VERBS[vn]["len"]
    def vg(v=vn, L=vlen):
        ph = 0.0
        for f in range(int(L*FPS)):
            ph += 2.2/FPS
            yield verb_frame(v, f/FPS, swim_deltas(ph, 0.0))
    scan_hyper(vn, vg())
check("elbow L never hyperextends", worst["L"] > -6.0,
      f"worst={worst['L']:.1f} deg at {worst_source['L']}")
check("elbow L never over-folds", minfold["L"] > 25, f"min interior={minfold['L']:.0f} deg")
check("elbow R never hyperextends", worst["R"] > -6.0,
      f"worst={worst['R']:.1f} deg at {worst_source['R']}")
check("elbow R never over-folds", minfold["R"] > 25, f"min interior={minfold['R']:.0f} deg")

# ---------------- skinning stress: streaks, shirt/skin capture, rear hair hue ----
import io as _io
from PIL import Image as _Im
UVs = np.concatenate([
    acc_np(p["attributes"]["TEXCOORD_0"]).astype(np.float64) for p in prims
], axis=0)
_mat = gltf["materials"][0]
_src = gltf["textures"][_mat["pbrMetallicRoughness"]["baseColorTexture"]["index"]]["source"]
_bv = gltf["bufferViews"][gltf["images"][_src]["bufferView"]]
_tex = _Im.open(_io.BytesIO(bin_data[_bv.get("byteOffset",0):_bv.get("byteOffset",0)+_bv["byteLength"]])).convert("RGB")
_T = np.asarray(_tex); _th,_tw = _T.shape[:2]
_u = np.clip((UVs[:,0]%1.0)*(_tw-1),0,_tw-1).astype(int)
_v = np.clip((UVs[:,1]%1.0)*(_th-1),0,_th-1).astype(int)
CT = _T[_v,_u].astype(float)
_r,_g,_b = CT[:,0],CT[:,1],CT[:,2]
_mx=CT.max(1); _mn=CT.min(1); _sat=(_mx-_mn)/np.maximum(_mx,1)
_skin = (_r>170)&(_r>_g)&(_g>_b)&(_g>110)&(_g<215)&(_b>90)&(_b<190)&((_r-_b)>25)&((_r-_b)<95)
_pink = (_r>190)&(_b>170)&(_g>140)&(_g<_r)&(_sat<0.35)&~_skin
strand_ks = [k for k,j in enumerate(joints) if jname[j].startswith("hair_")]
_sw = np.zeros(len(P0))
_head_w = np.zeros(len(P0))
_head_k = joints.index(name2j["head"])
for c in range(4):
    _sw += np.where(np.isin(J[:,c], strand_ks), W[:,c], 0)
    _head_w += np.where(J[:,c] == _head_k, W[:,c], 0)
# Head-dominant scalp vertices legitimately combine head and strand motion;
# exclude them from the garment/skin capture test even if their painted pixels
# happen to meet the broad pink or skin color heuristic.
_bad_shirt = np.flatnonzero((_sw > 0.3) & (_head_w < 0.5) & _pink)
_bad_skin = np.flatnonzero((_sw > 0.3) & (_head_w < 0.5) & _skin)
check("no shirt verts strand-driven", len(_bad_shirt) == 0,
      f"{len(_bad_shirt)} pink-top verts >30% strand weight: {_bad_shirt.tolist()}")
check("no skin verts strand-driven", len(_bad_skin) == 0,
      f"{len(_bad_skin)} skin verts >30% strand weight: {_bad_skin.tolist()}")

def full_skin_pose(deltas):
    M = joint_mats(deltas)
    S = np.zeros((len(P0),3))
    for c in range(4):
        S += W[:,c][:,None]*np.einsum("nij,nj->ni", M[J[:,c]], Ph)[:,:3]
    return S

# Worst-case: every strand at HairSim MAX_ANGLE (0.35 rad after damping),
# both axes, on top of sprint swim + the exact player.gd cheer peak.
HMAX = 0.35
stress = swim_deltas(1.3, 25.0)
for k in strand_ks:
    nm = jname[joints[k]]
    q = qmul(model_axis_delta(nm, RIGHT, HMAX), model_axis_delta(nm, BACK, HMAX))
    stress[nm] = q
stress["armU"] = model_axis_delta("armU", RIGHT, 2.45)
stress["armU2"] = model_axis_delta("armU2", RIGHT, 2.502)
stress["armF"] = model_axis_delta("armF", BACK, 1.15)
stress["armF2"] = model_axis_delta("armF2", RIGHT, 0.76)
stress["head"] = model_axis_delta("head", RIGHT, 0.08)
stress["chest"] = model_axis_delta("chest", RIGHT, -0.08)
S1 = full_skin_pose(stress)
disp = np.linalg.norm(S1-P0, axis=1)
check("stress max displacement bounded", float(disp.max()) < 1.1,
      f"max vert displacement {disp.max():.2f} (hair tips ~0.6 legit)")
IDX = np.concatenate([
    acc_np(p["indices"]).astype(np.int64).reshape(-1,3) + primitive_offsets[index]
    for index, p in enumerate(prims)
], axis=0)
e = np.unique(np.sort(np.concatenate([IDX[:,[0,1]], IDX[:,[1,2]], IDX[:,[0,2]]]),1), axis=0)
sel_e = e[np.random.RandomState(7).choice(len(e), 30000, replace=False)]
l0 = np.linalg.norm(P0[sel_e[:,0]]-P0[sel_e[:,1]], axis=1)
l1 = np.linalg.norm(S1[sel_e[:,0]]-S1[sel_e[:,1]], axis=1)
ok_e = l0 > 1e-4
ratio = (l1[ok_e]/l0[ok_e])
opening = l1[ok_e] - l0[ok_e]
open_edges = sel_e[ok_e]
worst_opening_index = int(np.argmax(opening))
worst_opening_edge = open_edges[worst_opening_index]
def dominant_bone(vertex):
    slot = int(np.argmax(W[vertex]))
    return jname[joints[int(J[vertex, slot])]]
hair_edge = (_sw[open_edges[:,0]] > 0.3) | (_sw[open_edges[:,1]] > 0.3)
arm_indices = [joints.index(name2j[name]) for name in
               ("armU", "armF", "hand", "armU2", "armF2", "hand2")]
arm_weight = np.zeros(len(P0))
for c in range(4):
    arm_weight += np.where(np.isin(J[:,c], arm_indices), W[:,c], 0)
arm_edge = (arm_weight[open_edges[:,0]] > 0.3) | (arm_weight[open_edges[:,1]] > 0.3)
def region_opening(mask):
    values = opening[mask]
    if len(values) == 0:
        return (0.0, 0.0)
    return (float(np.percentile(values, 99.9)), float(values.max()))
hair_opening = region_opening(hair_edge)
arm_opening = region_opening(arm_edge)
body_opening = region_opening(~hair_edge & ~arm_edge)
check("stress no visible tearing", float(np.percentile(opening, 99.9)) < 0.05 and float(opening.max()) < 0.12,
      f"edge opening 99.9pct {np.percentile(opening,99.9):.3f} max {opening.max():.3f}; "
      f"hair {hair_opening[0]:.3f}/{hair_opening[1]:.3f}, "
      f"arm {arm_opening[0]:.3f}/{arm_opening[1]:.3f}, "
      f"body {body_opening[0]:.3f}/{body_opening[1]:.3f}; "
      f"worst {worst_opening_edge[0]}-{worst_opening_edge[1]} "
      f"({dominant_bone(worst_opening_edge[0])}/{dominant_bone(worst_opening_edge[1])})")
# rear hair hue balance: blue fraction of rear-facing hair pixels, rest vs stress
def rear_blue(S):
    m = (S[:,2] > 0.05) & (S[:,1] > 0.1)     # back hemisphere, above waist
    cc = CT[m]
    blue = (cc[:,2] > cc[:,0]+20) & (cc[:,2] > 110)
    brownish = (cc[:,0] > cc[:,2]+20)
    return blue.sum()/max(blue.sum()+brownish.sum(),1)
rb0, rb1 = rear_blue(P0), rear_blue(S1)
check("rear hair keeps brown/rainbow mix", rb1 < 0.62 and rb1 < rb0*1.6 + 0.05,
      f"rear blue fraction rest={rb0:.2f} stress={rb1:.2f}")

# authored rainbow design (v4g): her-right rear scalp is pure chestnut, and the
# swath lobe carries all rainbow band families (warm / green / cyan) at rest
def _hue_deg(cc):
    mxh = cc.max(1); mnh = cc.min(1); dh = np.maximum(mxh-mnh, 1e-6)
    r_, g_, b_ = cc[:, 0], cc[:, 1], cc[:, 2]
    h = np.where(mxh == r_, ((g_-b_)/dh) % 6,
                 np.where(mxh == g_, (b_-r_)/dh+2, (r_-g_)/dh+4))
    return h*60
_scalpR = (P0[:, 0] > 0.10) & (P0[:, 1] > 0.35) & (P0[:, 2] > 0.05)
_ccR = CT[_scalpR]
_tealR = ((_ccR[:, 2] > _ccR[:, 0]+10) | ((_ccR[:, 1] > _ccR[:, 0]+15) & (_ccR[:, 1] > 90)))
check("rear-right scalp chestnut (no teal)", float(_tealR.mean()) < 0.10,
      f"teal fraction {_tealR.mean():.3f} over {len(_ccR)} verts")
_swath = (P0[:, 0] < -0.08) & (P0[:, 1] > 0.20) & (P0[:, 1] < 0.75)
_csw = CT[_swath]
_hsw = _hue_deg(_csw)
_satsw = (_csw.max(1)-_csw.min(1))/np.maximum(_csw.max(1), 1)
_col = _satsw > 0.30
_fw = float((((_hsw < 75) | (_hsw > 300)) & _col).mean())
_fg = float((((_hsw >= 85) & (_hsw < 160)) & _col).mean())
_fc = float((((_hsw >= 160) & (_hsw < 255)) & _col).mean())
check("swath shows full rainbow banding", _fw > 0.10 and _fg > 0.05 and _fc > 0.05,
      f"warm {_fw:.2f} green {_fg:.2f} cyan {_fc:.2f} of {len(_csw)} swath verts")

# ---------------- report ----------------
fails = 0
print(f"{'CHECK':44s} {'VERDICT':8s} DETAIL")
for name, ok, detail in results:
    if not ok: fails += 1
    print(f"{name:44s} {'PASS' if ok else 'FAIL':8s} {detail}")
print(f"\n{len(results)-fails}/{len(results)} passed")
sys.exit(1 if fails else 0)
