"""Motion-cage audit for roshan_v4: simulate every motion the game plays
(swim at 3 speeds + all 7 verbs, incl. the idle-swim underneath and the verb
blend window) exactly as player.gd computes them, then judge each against
numeric acceptance criteria. Frame math mirrors _rot_bone/_apply_verb:
absolute pose = rest * delta; verb slerp happens in delta space (slerp is
left-invariant). glTF frame: +y up, -z her front, +x her left.
"""
import json, struct, io, sys
import numpy as np
from PIL import Image, ImageFilter

GLB = "roshan_v4_slim.glb"
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

prim = gltf["meshes"][0]["primitives"][0]
P0 = acc_np(prim["attributes"]["POSITION"]).astype(np.float64)
J = acc_np(prim["attributes"]["JOINTS_0"]).astype(int)
W = acc_np(prim["attributes"]["WEIGHTS_0"]).astype(np.float64)
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
   "armU":{"axis":RIGHT,"keys":[[0,-0.2],[0.4,2.2],[1.7,2.2],[2.2,-0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.4,2.8],[1.7,2.8],[2.2,-0.2]]},
   "head":{"axis":RIGHT,"keys":[[0,0],[0.5,0.2],[1.7,0.2],[2.2,0]]},
   "chest":{"axis":RIGHT,"keys":[[0,0],[0.5,-0.12],[1.7,-0.12],[2.2,0]]}}},
 "clap": {"len":2.0,"tracks":{
   "armU":{"axis":RIGHT,"keys":[[0,-0.2],[0.35,2.4],[1.7,2.4],[2.0,-0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.35,2.9],[1.7,2.9],[2.0,-0.2]]},
   "armF":{"axis":(1,0,-1),"keys":[[0,0],[0.5,-1.2],[0.65,-0.3],[0.8,-1.2],[0.95,-0.3],[1.1,-1.2],[1.25,-0.3],[1.4,-1.2],[1.7,0]]},
   "armF2":{"axis":(1,0,1),"keys":[[0,0],[0.5,0.6],[0.65,0.05],[0.8,0.6],[0.95,0.05],[1.1,0.6],[1.25,0.05],[1.4,0.6],[1.7,0]]}}},
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
   "armU":{"axis":RIGHT,"keys":[[0,-0.2],[0.3,0.9],[1.2,0.9],[1.5,-0.2]]},
   "armU2":{"axis":RIGHT,"keys":[[0,-0.2],[0.3,1.9],[1.2,1.9],[1.5,-0.2]]}}},
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
    d["armF"] = model_axis_delta("armF", RIGHT, np.sin(ap-0.5)*arm_amp*0.7)
    d["armU2"] = model_axis_delta("armU2", RIGHT, np.sin(ap-0.35)*arm_amp)
    d["armF2"] = model_axis_delta("armF2", RIGHT, np.sin(ap-0.85)*arm_amp*0.7)
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
check("clap hands near (anat. limit 0.30)", dist[i] < 0.33, f"min dist {dist[i]:.2f} at t={rows[i][0]:.2f}")
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

# ---------------- report ----------------
fails = 0
print(f"{'CHECK':44s} {'VERDICT':8s} DETAIL")
for name, ok, detail in results:
    if not ok: fails += 1
    print(f"{name:44s} {'PASS' if ok else 'FAIL':8s} {detail}")
print(f"\n{len(results)-fails}/{len(results)} passed")
sys.exit(1 if fails else 0)
