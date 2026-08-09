"""v4f: re-place the left arm chain into the actual arm tube + rebuild its
weights (bones were fitted through the chest), and repaint the back-of-head
teal/blue texels to chestnut on her right side (Meshy smeared the rainbow
swath across the back; the authored look keeps rainbow only over her left)."""
import numpy as np, io as _io, json, struct, re
from PIL import Image
from scipy import ndimage

_src = open("audit_motions.py", encoding="utf-8").read().split("# ---------------- player.gd motion")[0]
_src = re.sub(r'GLB = "[^"]+"', 'GLB = "roshan_v4e_slim.glb"', _src)   # always build from clean v4e
exec(_src)

UV = acc_np(prim["attributes"]["TEXCOORD_0"]).astype(np.float64)
mat = gltf["materials"][0]
srci = gltf["textures"][mat["pbrMetallicRoughness"]["baseColorTexture"]["index"]]["source"]
bvi = gltf["bufferViews"][gltf["images"][srci]["bufferView"]]
tex = Image.open(_io.BytesIO(bin_data[bvi.get("byteOffset", 0):bvi.get("byteOffset", 0)+bvi["byteLength"]])).convert("RGB")
T = np.asarray(tex).copy()
th, tw = T.shape[:2]
u = np.clip((UV[:, 0] % 1.0)*(tw-1), 0, tw-1).astype(int)
v = np.clip((UV[:, 1] % 1.0)*(th-1), 0, th-1).astype(int)
C = T[v, u].astype(float)
r, g, b = C[:, 0], C[:, 1], C[:, 2]
skin = (r > 170) & (r > g) & (g > b) & (g > 110) & (g < 215) & (b > 90) & (b < 190) & \
       ((r-b) > 25) & ((r-b) < 95)

# ---------------- FIX 1: left arm chain + weights ----------------
tube = skin & (P0[:, 0] > 0.12) & (P0[:, 1] < 0.2) & (P0[:, 1] > -0.45)
A = P0[tube]
c0 = A.mean(0)
ev, evec = np.linalg.eigh(np.cov((A-c0).T))
ax = evec[:, -1]
t = (A-c0) @ ax
if A[t < np.percentile(t, 10)].mean(0)[1] < A[t > np.percentile(t, 90)].mean(0)[1]:
    ax = -ax
    t = -t
o = np.argsort(t)
As, ts = A[o], t[o]-t[o].min()
tmax = ts[-1]

def seg(f0, f1):
    m = (ts >= f0*tmax) & (ts <= f1*tmax)
    if m.sum() >= 5:
        return As[m].mean(0)
    i0, i1 = int(f0*(len(As)-1)), max(int(f1*(len(As)-1)), int(f0*(len(As)-1))+3)
    return As[i0:i1+1].mean(0)   # rank-based fallback for sparse bands

top = seg(0, 0.10)
wr = seg(0.78, 0.92)
tip = seg(0.95, 1.0)
# shoulder: extend the tube axis upward to the torso junction (the shoulder
# itself is sleeve-covered, so the skin tube starts mid-upper-arm)
up = (top - wr)
up = up/np.linalg.norm(up)
sh = top + up * max(0.0, (0.02 - top[1]) / max(up[1], 1e-6))
sh[0] = max(sh[0], 0.15)
# near-straight hanging arm: elbow by ratio (matches the R arm proportions)
el = sh + 0.54*(wr - sh) + np.array([0.0, 0.0, 0.018])   # elbow set back -> forearm bows forward (natural flexion slack)
print("new L chain: sh", sh.round(3), "el", el.round(3), "wr", wr.round(3))

def gmats_base():
    G = {}
    for i in order:
        L = np.eye(4)
        L[:3, :3] = quat_mat(rest_q[i])
        L[:3, 3] = rest_t[i]
        G[i] = (G[parent[i]] @ L) if i in parent else L
    return G

G0 = gmats_base()
data2 = bytearray(open(GLB, "rb").read())
clen2, _ = struct.unpack_from("<II", data2, 12)
g2 = json.loads(data2[20:20+clen2])
boff = 20+clen2+8
targets = {"armU": sh, "armF": el, "hand": wr}
newG = {}
for bn in ("armU", "armF", "hand"):
    ni = name2j[bn]
    pi = parent[ni]
    Gp = newG.get(pi, G0[pi])
    lt = np.linalg.inv(Gp) @ np.array([*targets[bn], 1.0])
    g2["nodes"][ni]["translation"] = [float(x) for x in lt[:3]]
    L = np.eye(4)
    L[:3, :3] = quat_mat(rest_q[ni])
    L[:3, 3] = lt[:3]
    newG[ni] = Gp @ L

sk2 = g2["skins"][0]
ai = g2["accessors"][sk2["inverseBindMatrices"]]
bv2 = g2["bufferViews"][ai["bufferView"]]
sti = boff+bv2.get("byteOffset", 0)+ai.get("byteOffset", 0)
rest_t2 = dict(rest_t)
for bn in ("armU", "armF", "hand"):
    rest_t2[name2j[bn]] = np.array(g2["nodes"][name2j[bn]]["translation"])
G1 = {}
for i in order:
    L = np.eye(4)
    L[:3, :3] = quat_mat(rest_q[i])
    L[:3, 3] = rest_t2[i]
    G1[i] = (G1[parent[i]] @ L) if i in parent else L

def subtree(ni):
    out = [ni]
    for c in g2["nodes"][ni].get("children", []):
        out += subtree(c)
    return out

for ni in subtree(name2j["armU"]):
    if ni in joints:
        k = joints.index(ni)
        data2[sti+k*64:sti+k*64+64] = np.linalg.inv(G1[ni]).T.astype(np.float32).reshape(-1).tobytes()

arm_ks = {bn: joints.index(name2j[bn]) for bn in ("armU", "armF", "hand")}
chest_k = joints.index(name2j["chest"])
spine_k = joints.index(name2j["spine1"])
segs = [(sh, el, "armU"), (el, wr, "armF"), (wr, tip, "hand")]

def capsule_d(p, a, bb):
    ab = bb-a
    t2 = np.clip(np.dot(p-a, ab)/max(np.dot(ab, ab), 1e-9), 0, 1)
    return np.linalg.norm(p-a-t2*ab)

J2 = J.copy()
W2 = W.copy().astype(np.float64)
larm_old = np.zeros(len(P0))
for c in range(4):
    larm_old += np.where(np.isin(J2[:, c], list(arm_ks.values())), W2[:, c], 0)
affected = np.where(larm_old > 0.02)[0]
print("re-weighting", len(affected), "left-arm-influenced verts")
for vi in affected:
    p = P0[vi]
    lateral_ok = p[0] > 0.10 and not (p[0] < 0.14 and abs(p[2]) < 0.10 and p[1] > -0.05)
    ds = sorted((capsule_d(p, a, bb), nm) for a, bb, nm in segs)
    dmin, nm_best = ds[0]
    strip = 0.0
    for c in range(4):
        if J2[vi, c] in arm_ks.values():
            strip += W2[vi, c]
            W2[vi, c] = 0.0
    if lateral_ok and dmin < 0.09:
        w_arm = strip * np.exp(-(dmin/0.06)**2)
    else:
        w_arm = 0.0
    w_anchor = strip - w_arm
    if w_arm > 0.01:
        c0i = int(np.argmin(W2[vi]))
        J2[vi, c0i] = arm_ks[nm_best]
        W2[vi, c0i] = w_arm
    if w_anchor > 0.005:
        tgt = chest_k if p[1] > -0.05 else spine_k
        placed = False
        for c in range(4):
            if J2[vi, c] == tgt:
                W2[vi, c] += w_anchor
                placed = True
                break
        if not placed:
            c0i = int(np.argmin(W2[vi]))
            J2[vi, c0i] = tgt
            W2[vi, c0i] += w_anchor
W2n = (W2/np.maximum(W2.sum(1, keepdims=True), 1e-9)).astype(np.float32)

def wacc_raw(idx, arr, dtype):
    a2 = g2["accessors"][idx]
    bvv = g2["bufferViews"][a2["bufferView"]]
    st = boff+bvv.get("byteOffset", 0)+a2.get("byteOffset", 0)
    fl = arr.astype(dtype).reshape(-1)
    data2[st:st+fl.nbytes] = fl.tobytes()

jacc = g2["accessors"][prim["attributes"]["JOINTS_0"]]
jdt = {5121: np.uint8, 5123: np.uint16}[jacc["componentType"]]
wacc_raw(prim["attributes"]["JOINTS_0"], J2, jdt)
wacc_raw(prim["attributes"]["WEIGHTS_0"], W2n, np.float32)

# ---------------- FIX 2: repaint back-of-head teal -> chestnut -------------
back_blue = (P0[:, 1] > 0.28) & (P0[:, 2] > -0.02) & (P0[:, 0] < 0.05)
teal = (C[:, 2] > C[:, 0]+10) | ((C[:, 1] > C[:, 0]+15) & (C[:, 1] > 90))
paint_verts = back_blue & teal
print("repainting texels from", int(paint_verts.sum()), "verts")
mask = np.zeros((th, tw), bool)
mask[v[paint_verts], u[paint_verts]] = True
mask = ndimage.binary_dilation(mask, iterations=7)
px = T.astype(np.float64)
mr, mg, mb = px[..., 0][mask], px[..., 1][mask], px[..., 2][mask]
mx2 = np.maximum(np.maximum(mr, mg), mb)
mn2 = np.minimum(np.minimum(mr, mg), mb)
val = mx2/255.0
sat2 = (mx2-mn2)/np.maximum(mx2, 1)
ss = np.clip(sat2*0.85+0.10, 0, 0.65)
f = (25/60.0)  # hue 25 deg inside sector 0
p_ = val*(1-ss)
t_ = val*(1-(1-f)*ss)
px[..., 0][mask] = val*255
px[..., 1][mask] = t_*255
px[..., 2][mask] = p_*255
T2 = px.astype(np.uint8)
buf = _io.BytesIO()
Image.fromarray(T2).save(buf, "JPEG", quality=88)
newjpg = buf.getvalue()

img_bv_idx = g2["images"][srci]["bufferView"]
new_bin = bytearray()
nbvs = []
for i2 in range(len(g2["bufferViews"])):
    bvd = g2["bufferViews"][i2]
    start = bvd.get("byteOffset", 0)
    chunk = newjpg if i2 == img_bv_idx else bytes(data2[boff+start:boff+start+bvd["byteLength"]])
    while len(new_bin) % 4:
        new_bin.append(0)
    nb = dict(bvd)
    nb["byteOffset"] = len(new_bin)
    nb["byteLength"] = len(chunk)
    nbvs.append(nb)
    new_bin += chunk
g2["bufferViews"] = nbvs
g2["buffers"] = [{"byteLength": len(new_bin)}]
js = json.dumps(g2, separators=(",", ":")).encode()
while len(js) % 4:
    js += b" "
while len(new_bin) % 4:
    new_bin.append(0)
out = struct.pack("<4sII", b"glTF", 2, 12+8+len(js)+8+len(new_bin))
out += struct.pack("<II", len(js), 0x4E4F534A)+js
out += struct.pack("<II", len(new_bin), 0x004E4942)+bytes(new_bin)
open("roshan_v4f_slim.glb", "wb").write(out)
print("v4f written")
