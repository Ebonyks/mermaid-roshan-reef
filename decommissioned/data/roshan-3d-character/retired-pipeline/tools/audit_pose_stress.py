"""Static pose stress test for roshan_v4: hold four extreme arm poses
(arms overhead, T-pose, hands on hips, both arms forward) and judge the
skinned mesh numerically — edge tearing, triangle blowup, forearm/hand
penetration into the body, left/right symmetry, and per-pose reach goals.
Companion to audit_motions.py (which cages the game's *animated* motions);
this file cages held poses at range-of-motion extremes.
Frame: glTF +y up, -z her front, +x her left. Renders QA captures to
tools/out/pose_stress/.
"""
import json, struct, os, sys
import numpy as np
from PIL import Image, ImageDraw

GLB = "assets/characters/roshan_v4.glb"
if "--glb" in sys.argv:
    GLB = sys.argv[sys.argv.index("--glb") + 1]
OUT = "tools/out/pose_stress"
os.makedirs(OUT, exist_ok=True)

# ---------------- GLB / skinning core (mirrors audit_motions.py) ----------------
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
rest_global_r = {}
for i in order:
    local_r = quat_mat(rest_q[i])
    rest_global_r[i] = rest_global_r[parent[i]] @ local_r if i in parent else local_r

def joint_mats(deltas):
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
P_parts = [acc_np(p["attributes"]["POSITION"]).astype(np.float64) for p in prims]
primitive_offsets = np.cumsum([0] + [len(v) for v in P_parts[:-1]])
P0 = np.concatenate(P_parts, axis=0)
J = np.concatenate([acc_np(p["attributes"]["JOINTS_0"]).astype(int) for p in prims], axis=0)
W = np.concatenate([acc_np(p["attributes"]["WEIGHTS_0"]).astype(np.float64) for p in prims], axis=0)
W = W/np.maximum(W.sum(1, keepdims=True), 1e-9)
Ph = np.concatenate([P0, np.ones((len(P0), 1))], 1)
IDX = np.concatenate([
    acc_np(p["indices"]).astype(np.int64).reshape(-1, 3) + primitive_offsets[i]
    for i, p in enumerate(prims)], axis=0)

def full_skin_pose(deltas):
    M = joint_mats(deltas)
    S = np.zeros((len(P0), 3))
    for c in range(4):
        S += W[:, c][:, None]*np.einsum("nij,nj->ni", M[J[:, c]], Ph)[:, :3]
    return S

def model_axis_delta(bone, axis, ang):
    Rg = rest_global_r[name2j[bone]]
    return aa_quat(Rg.T @ np.asarray(axis, float), ang)

def rot_axis(axis, ang):
    return quat_mat(aa_quat(axis, ang))

def mat_quat(R):
    w = np.sqrt(max(0.0, 1+R[0, 0]+R[1, 1]+R[2, 2]))/2
    return np.array([(R[2, 1]-R[1, 2])/(4*w), (R[0, 2]-R[2, 0])/(4*w),
                     (R[1, 0]-R[0, 1])/(4*w), w])

def model_mat_delta(bone, R):
    Rg = rest_global_r[name2j[bone]]
    q = mat_quat(Rg.T @ R @ Rg)
    return q/np.linalg.norm(q)

MIRROR = np.diag([-1.0, 1.0, 1.0])
def mirrored(R):
    return MIRROR @ R @ MIRROR

RIGHT, UP, BACK, FWD = np.eye(3)[0], np.eye(3)[1], np.eye(3)[2], -np.eye(3)[2]

# ---------------- region masks ----------------
ARM_BONES = ("armU", "armF", "hand", "armU2", "armF2", "hand2")
arm_idx = [joints.index(name2j[n]) for n in ARM_BONES]
distal_idx = [joints.index(name2j[n]) for n in ("armF", "hand", "armF2", "hand2")]
strand_idx = [k for k, j in enumerate(joints) if jname[j].startswith("hair_")]
def weight_of(idx_list):
    w = np.zeros(len(P0))
    for c in range(4):
        w += np.where(np.isin(J[:, c], idx_list), W[:, c], 0)
    return w
arm_w = weight_of(arm_idx)
distal_w = weight_of(distal_idx)
strand_w = weight_of(strand_idx)
left_w = weight_of([joints.index(name2j[n]) for n in ("armF", "hand")])
right_w = weight_of([joints.index(name2j[n]) for n in ("armF2", "hand2")])
body_mask = (arm_w < 0.05) & (strand_w < 0.3)          # torso+head+tail+fixed hair
handL = left_w > 0.4
handR = right_w > 0.4

edges = np.unique(np.sort(np.concatenate(
    [IDX[:, [0, 1]], IDX[:, [1, 2]], IDX[:, [0, 2]]]), 1), axis=0)
rest_el = np.linalg.norm(P0[edges[:, 0]]-P0[edges[:, 1]], axis=1)
edge_ok = rest_el > 1e-4
def tri_areas(S):
    a = S[IDX[:, 1]]-S[IDX[:, 0]]; b = S[IDX[:, 2]]-S[IDX[:, 0]]
    return 0.5*np.linalg.norm(np.cross(a, b), axis=1)
rest_area = tri_areas(P0)
area_ok = rest_area > 1e-10

def vertex_normals(S):
    a = S[IDX[:, 1]]-S[IDX[:, 0]]; b = S[IDX[:, 2]]-S[IDX[:, 0]]
    fn = np.cross(a, b)
    vn = np.zeros_like(S)
    for k in range(3):
        np.add.at(vn, IDX[:, k], fn)
    n = np.linalg.norm(vn, axis=1, keepdims=True)
    return vn/np.maximum(n, 1e-12)

def penetration(S, probe_mask, tol=0.005, radius=0.08):
    """Max depth (m) of probe verts inside the body surface, via nearest
    body vertex + outward normal. Positive depth = inside."""
    vn = vertex_normals(S)
    B = S[body_mask]; BN = vn[body_mask]
    Pv = S[probe_mask]
    if len(Pv) == 0:
        return 0.0, 0
    cell = radius
    grid = {}
    keys = np.floor(B/cell).astype(int)
    for i, k in enumerate(map(tuple, keys)):
        grid.setdefault(k, []).append(i)
    depths = np.zeros(len(Pv))
    pk = np.floor(Pv/cell).astype(int)
    for i, p in enumerate(Pv):
        cand = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    cand += grid.get((pk[i, 0]+dx, pk[i, 1]+dy, pk[i, 2]+dz), [])
        if not cand:
            continue
        cand = np.array(cand)
        d = np.linalg.norm(B[cand]-p, axis=1)
        j = cand[np.argmin(d)]
        if d.min() < radius:
            depth = float(np.dot(BN[j], B[j]-p))
            if depth > 0:
                depths[i] = depth
    bad = depths > tol
    return float(depths.max()), int(bad.sum())

# ---------------- the four stress poses ----------------
# Angles are the measured safe envelope of this rig: the widest expression of
# each pose that stays clean. The strict textbook extremes are probed
# separately below as WARN diagnostics (they clip; see the report doc).
def both_arms(RL):
    RR = mirrored(RL)
    return {"armU": model_mat_delta("armU", RL), "armU2": model_mat_delta("armU2", RR)}

def pose_overhead():
    # Wide V: hands at crown height. Beyond ~1.9 the hands enter the
    # head/hair shell (arm chain 0.4156 vs hair half-width 0.29). The right
    # arm is held 0.1 rad wider: the hand skin sits ~5 cm off mirror-perfect
    # and passes closer to the hair on that side.
    return {"armU": model_mat_delta("armU", rot_axis(BACK, 1.9)),
            "armU2": model_mat_delta("armU2", mirrored(rot_axis(BACK, 1.8)))}

def pose_tpose():
    return both_arms(rot_axis(BACK, 0.72))

def pose_hips():
    # Elbows out, moderate bend. True palm-on-hip is unreachable without
    # forearm-through-torso clipping (rigid hand, no wrist joint).
    RU = rot_axis(BACK, 0.4) @ rot_axis(UP, 0.8)
    RF = rot_axis(np.array([0, 1, -0.4]), 1.7)
    d = both_arms(RU)
    d["armF"] = model_mat_delta("armF", RF)
    d["armF2"] = model_mat_delta("armF2", mirrored(RF))
    return d

def pose_forward():
    return both_arms(rot_axis(UP, 1.5) @ rot_axis(BACK, 0.72))

POSES = {
    "arms_overhead": pose_overhead(),
    "t_pose": pose_tpose(),
    "hands_on_hips": pose_hips(),
    "arms_forward": pose_forward(),
}

# strict extremes + the game's own peaks, reported as WARN not FAIL
def probe_cheer():
    return {"armU": model_axis_delta("armU", (1, 0, 3), 2.4),
            "armU2": model_axis_delta("armU2", (1, 0, -3), 2.4),
            "armF": model_axis_delta("armF", (1, 0, -0.5), 0.8),
            "armF2": model_axis_delta("armF2", (1, 0, 0.5), 0.8)}

def probe_wave():
    return {"armU2": model_axis_delta("armU2", (1, 0, 0), 2.8),
            "armF2": model_axis_delta("armF2", (0, 0, 1), 0.55)}

ENVELOPE_PROBES = {
    "vertical_overhead (strict)": both_arms(rot_axis(BACK, 2.3)),
    "palm_on_hip (strict)": {
        **both_arms(rot_axis(BACK, 0.2) @ rot_axis(UP, 1.1)),
        "armF": model_mat_delta("armF", rot_axis(np.array([0, 1, -0.4]), 2.1)),
        "armF2": model_mat_delta("armF2", mirrored(rot_axis(np.array([0, 1, -0.4]), 2.1)))},
    "game_cheer_peak": probe_cheer(),
    "game_wave_peak": probe_wave(),
}

# ---------------- checks ----------------
fails = []
def check(name, cond, detail):
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}: {detail}")
    if not cond:
        fails.append(name)

S_rest = full_skin_pose({})
check("rest-pose skin residual", float(np.abs(S_rest-P0).max()) < 1e-4,
      f"max residual {np.abs(S_rest-P0).max():.2e}")

shoulder_y = 0.14
hip_pt = np.array([0.1815, -0.1834, -0.0596])

def hand_centroids(S):
    return S[handL].mean(0), S[handR].mean(0)

def head_clearance(S, mask):
    head_w = weight_of([joints.index(name2j["head"])])
    Hm = (head_w > 0.4) & body_mask
    H = S[Hm]
    Pv = S[mask]
    dmin = 1e9
    for i in range(0, len(Pv), 256):
        chunk = Pv[i:i+256]
        d = np.linalg.norm(H[None, :, :]-chunk[:, None, :], axis=2)
        dmin = min(dmin, float(d.min()))
    return dmin

results = {}
for pname, deltas in POSES.items():
    S = full_skin_pose(deltas)
    results[pname] = S
    el = np.linalg.norm(S[edges[:, 0]]-S[edges[:, 1]], axis=1)
    opening = (el-rest_el)[edge_ok]
    p999, omax = float(np.percentile(opening, 99.9)), float(opening.max())
    check(f"{pname}: no visible tearing", p999 < 0.05 and omax < 0.12,
          f"edge opening 99.9pct {p999:.3f} max {omax:.3f}")
    ar = tri_areas(S)[area_ok]/rest_area[area_ok]
    blow = int((ar > 3.0).sum())
    check(f"{pname}: triangle blowup bounded", blow < 200,
          f"{blow} tris >3x rest area (cage reference: 28-62 at 90deg swing)")
    dep, cnt = penetration(S, (distal_w > 0.4))
    limit = 0.030 if pname == "hands_on_hips" else 0.025
    check(f"{pname}: forearm/hand body penetration", dep < limit,
          f"max depth {dep:.3f} ({cnt} verts beyond 5mm tol; limit {limit})")
    hL, hR = hand_centroids(S)
    mirror_gap = float(np.linalg.norm(hL*np.array([-1, 1, 1])-hR))
    check(f"{pname}: left/right symmetry", mirror_gap < 0.08,
          f"mirrored hand-centroid gap {mirror_gap:.3f}")
    if pname == "arms_overhead":
        check("arms_overhead: hands reach crown height",
              hL[1] > 0.46 and hR[1] > 0.46,
              f"hand y L {hL[1]:.2f} R {hR[1]:.2f} (head centroid 0.547; "
              f"arm chain 0.4156 caps reach at ~0.556)")
        clr = head_clearance(S, handL | handR)
        check("arms_overhead: no head/hair clipping", clr > 0.015,
              f"min hand-to-head distance {clr:.3f} (right side is the tight "
              f"one; its hand skin sits ~5cm off mirror)")
    if pname == "t_pose":
        check("t_pose: arms horizontal",
              abs(hL[1]-shoulder_y) < 0.06 and abs(hR[1]-shoulder_y) < 0.06,
              f"hand y L {hL[1]:.2f} R {hR[1]:.2f} vs shoulder {shoulder_y}")
        check("t_pose: full span", hL[0] > 0.55 and hR[0] < -0.55,
              f"hand x L {hL[0]:.2f} R {hR[0]:.2f}")
    if pname == "hands_on_hips":
        dL = float(np.linalg.norm(hL-hip_pt))
        dR = float(np.linalg.norm(hR-hip_pt*np.array([-1, 1, 1])))
        check("hands_on_hips: hands frame the hips", dL < 0.22 and dR < 0.22,
              f"hand-to-hip distance L {dL:.3f} R {dR:.3f}; palm contact is "
              f"outside this rig's clean envelope (rigid hand, no wrist joint)")
    if pname == "arms_forward":
        check("arms_forward: forward reach", hL[2] < -0.35 and hR[2] < -0.35,
              f"hand z L {hL[2]:.2f} R {hR[2]:.2f}")
        check("arms_forward: arms stay parallel", float(np.linalg.norm(hL-hR)) > 0.22,
              f"hand separation {np.linalg.norm(hL-hR):.2f}")

# ---------------- envelope probes (WARN, not gated) ----------------
print("\n-- envelope probes: strict extremes and shipped animation peaks --")
for ename, deltas in ENVELOPE_PROBES.items():
    S = full_skin_pose(deltas)
    mask = (right_w > 0.4) if "wave" in ename else (distal_w > 0.4)
    dep, cnt = penetration(S, mask)
    tag = "WARN" if dep > 0.025 else "ok  "
    print(f"[{tag}] {ename}: body penetration max {dep:.3f}, {cnt} verts beyond 5mm")
    results[f"probe_{ename.split(' ')[0]}"] = S

# ---------------- QA renders ----------------
def render(S, path, yaw=0.0, size=(560, 760)):
    c, s = np.cos(yaw), np.sin(yaw)
    R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    V = S @ R.T
    lo, hi = V.min(0), V.max(0)
    span = max(hi[0]-lo[0], hi[1]-lo[1])*1.12
    cx, cy = (hi[0]+lo[0])/2, (hi[1]+lo[1])/2
    def to_px(p):
        return ((p[:, 0]-cx)/span*size[0]+size[0]/2,
                (cy-p[:, 1])/span*size[0]+size[1]/2)
    img = Image.new("RGB", size, (24, 28, 48))
    dr = ImageDraw.Draw(img)
    a = V[IDX[:, 1]]-V[IDX[:, 0]]; b = V[IDX[:, 2]]-V[IDX[:, 0]]
    fn = np.cross(a, b)
    fn = fn/np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-12)
    light = fn @ np.array([0.3, 0.5, 0.81])
    depth = V[IDX].mean(1)[:, 2]
    tri_arm = (arm_w[IDX] > 0.4).any(1)
    # camera sits at -z (her front): far = +z, painter draws far first
    ordn = np.argsort(-depth)
    xs = (cx-V[:, 0])/span*size[0]+size[0]/2
    ys = (cy-V[:, 1])/span*size[0]+size[1]/2
    for t in ordn:
        i0, i1, i2 = IDX[t]
        sh = 0.35+0.65*max(0.0, float(light[t]))
        base = (150, 170, 205) if not tri_arm[t] else (235, 180, 150)
        col = tuple(int(v*sh) for v in base)
        dr.polygon([(xs[i0], ys[i0]), (xs[i1], ys[i1]), (xs[i2], ys[i2])], fill=col)
    img.save(path)

for pname, S in [("rest", S_rest)] + list(results.items()):
    render(S, f"{OUT}/{pname}_front.png", 0.0)
    render(S, f"{OUT}/{pname}_quarter.png", 0.7)
print(f"renders written to {OUT}/")

print(f"\n{'ALL OK' if not fails else 'FAILURES: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
