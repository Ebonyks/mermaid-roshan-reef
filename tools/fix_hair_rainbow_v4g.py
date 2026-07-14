"""v4g: authored rainbow hair. v4f wrongly chestnut-painted the swath chunk
(it lives at NEGATIVE x) and left Meshy's teal/orange noise inside it. Per the
back reference (Mermaid roshan art base / fhup27): most of the rear hair is
chestnut, with ONE clean rainbow swath (pink->orange->yellow->green->cyan
bands) sweeping from the crown parting down her left side. This build:
  FIX 1 (unchanged from v4f): left arm chain re-placed into the arm tube.
  FIX 2 (new): UV-space repaint — banded rainbow projected along the swath
  chunk's fitted centerline; her-right scalp teal -> chestnut; tail untouched.
"""
import numpy as np, io as _io, json, struct, re
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree

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

# ---------------- FIX 1: left arm chain + weights (verbatim v4f) ----------------
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
up = (top - wr)
up = up/np.linalg.norm(up)
sh = top + up * max(0.0, (0.02 - top[1]) / max(up[1], 1e-6))
sh[0] = max(sh[0], 0.15)
el = sh + 0.54*(wr - sh) + np.array([0.0, 0.0, 0.018])
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

# ---------------- FIX 2: authored rainbow swath + chestnut scalp ----------------
sat_v = (C.max(1)-C.min(1))/np.maximum(C.max(1), 1)
teal_v = ((b > r+10) | ((g > r+15) & (g > 90))) & (sat_v > 0.25)
hair_gate_v = (P0[:, 1] > 0.14)                      # above torso; tail/waist excluded
# seed from the coherent lobe only (x < -0.10): the teal SPECKLE smeared across
# the center back-of-head is Meshy noise and must go chestnut, not rainbow
swath_seed = teal_v & hair_gate_v & (P0[:, 0] < -0.10)
print("swath seed verts:", int(swath_seed.sum()))
# grow the seed over the whole geometric lobe (catches Meshy's orange noise inside it)
d3, _ = cKDTree(P0[swath_seed]).query(P0, workers=-1)
chunk_v = (d3 < 0.03) & hair_gate_v & (P0[:, 0] < 0.02) & ~skin
print("chunk verts after growth:", int(chunk_v.sum()))

# fitted centerline in back-projection (x,y): bands stack across the flow
pts2 = P0[chunk_v][:, :2]
c2 = pts2.mean(0)
ev2, evec2 = np.linalg.eigh(np.cov((pts2-c2).T))
main = evec2[:, -1]
if main[0] > 0:
    main = -main                       # s increases crown (x~0) -> tip (x<<0)
orth = np.array([-main[1], main[0]])
s_all = (pts2-c2) @ main
d_all = (pts2-c2) @ orth
# pink band faces the crown parting; anchor the +dr side there
anchor = np.array([0.0, 0.80])
if (anchor-c2) @ orth - np.polyval(np.polyfit(s_all, d_all, 2), (anchor-c2) @ main) < 0:
    orth = -orth
    d_all = -d_all
cf = np.polyfit(s_all, d_all, 2)       # curved centerline
dr = d_all - np.polyval(cf, s_all)
NB = 12
sbins = np.linspace(s_all.min(), s_all.max(), NB+1)

def bin_of(s):
    return np.clip(np.digitize(s, sbins)-1, 0, NB-1)

# quantile band coordinate per s-bin: every band gets even coverage across the
# lobe's local cross-section, whatever its silhouette does
sorted_dr = []
for i in range(NB):
    m = bin_of(s_all) == i
    sorted_dr.append(np.sort(dr[m]) if m.sum() >= 8 else np.sort(dr))

HUE_STOPS = np.array([-25.0, 20.0, 55.0, 115.0, 195.0])   # pink,orange,yellow,green,cyan

def swath_hue(px, py):
    pp = np.stack([px, py], 1)
    s = (pp-c2) @ main
    d = (pp-c2) @ orth - np.polyval(cf, s)
    bi = bin_of(s)
    tt = np.empty_like(d)
    for i in range(NB):
        m = bi == i
        if m.any():
            arr = sorted_dr[i]
            tt[m] = np.searchsorted(arr, d[m])/max(len(arr), 1)*2.0 - 1.0
    return np.interp((1.0-tt)*2.0, [0, 1, 2, 3, 4], HUE_STOPS) % 360.0

def hsv_rgb(h, s, vv):
    h6 = (h % 360.0)/60.0
    i = np.floor(h6).astype(int) % 6
    f = h6-np.floor(h6)
    p_ = vv*(1-s); q_ = vv*(1-f*s); t_ = vv*(1-(1-f)*s)
    return (np.choose(i, [vv, q_, p_, p_, t_, vv])*255,
            np.choose(i, [t_, vv, vv, q_, p_, p_])*255,
            np.choose(i, [p_, p_, t_, vv, vv, q_])*255)

# per-texel geometry: IDW position + chunk membership from nearest verts in UV space
kt = cKDTree(np.stack([u, v], 1).astype(float))
gy, gx = np.mgrid[0:th, 0:tw]
q = np.stack([gx.reshape(-1), gy.reshape(-1)], 1).astype(float)
dd, ii = kt.query(q, k=4, workers=-1)
iw = 1.0/(dd+1e-3)
iw /= iw.sum(1, keepdims=True)
p_tex = (P0[ii]*iw[..., None]).sum(1).reshape(th, tw, 3)
chunkness = (chunk_v[ii]*iw).sum(1).reshape(th, tw)
near = dd[:, 0].reshape(th, tw) < 12.0

Tf = T.astype(np.float64)
Rt, Gt, Bt = Tf[..., 0], Tf[..., 1], Tf[..., 2]
mx = Tf.max(2); mn = Tf.min(2)
sat_t = (mx-mn)/np.maximum(mx, 1)
val_t = mx/255.0
teal_t = ((Bt > Rt+10) | ((Gt > Rt+15) & (Gt > 90))) & (sat_t > 0.25)
skin_t = (Rt > 170) & (Rt > Gt) & (Gt > Bt) & (Gt > 110) & (Gt < 215) & (Bt > 90) & (Bt < 190) & \
         ((Rt-Bt) > 25) & ((Rt-Bt) < 95)
hair_t = near & (p_tex[..., 1] > 0.14) & ~skin_t
rainbow_m = hair_t & (chunkness > 0.45)            # the lobe is entirely swath
chest_m = hair_t & teal_t & ~rainbow_m             # ALL other head teal -> chestnut
rainbow_m = ndimage.binary_dilation(rainbow_m, iterations=2) & ~skin_t
chest_m = ndimage.binary_dilation(chest_m, iterations=2) & ~skin_t & ~rainbow_m
print(f"painting rainbow {int(rainbow_m.sum())} texels, chestnut {int(chest_m.sum())} texels")

# rainbow swath: banded hue, keep strand shading via original value channel
hue = swath_hue(p_tex[..., 0][rainbow_m], p_tex[..., 1][rainbow_m])
vv = 0.30 + 0.70*np.clip(val_t[rainbow_m], 0, 1)
rr, gg2, bb2 = hsv_rgb(hue, np.full_like(hue, 0.60), vv)
Tf[..., 0][rainbow_m] = rr
Tf[..., 1][rainbow_m] = gg2
Tf[..., 2][rainbow_m] = bb2
# her-right scalp: teal -> chestnut (v4f formula, structure-preserving)
valc = val_t[chest_m]
ssc = np.clip(sat_t[chest_m]*0.85+0.10, 0, 0.65)
fch = 25/60.0
Tf[..., 0][chest_m] = valc*255
Tf[..., 1][chest_m] = valc*(1-(1-fch)*ssc)*255
Tf[..., 2][chest_m] = valc*(1-ssc)*255
T2 = Tf.astype(np.uint8)
# self-check: no teal speckle should survive outside the swath
C2 = T2[v, u].astype(float)
left_teal = ((C2[:, 2] > C2[:, 0]+10) | ((C2[:, 1] > C2[:, 0]+15) & (C2[:, 1] > 90))) & \
            ((C2.max(1)-C2.min(1))/np.maximum(C2.max(1), 1) > 0.25) & hair_gate_v & ~chunk_v
print(f"teal verts remaining outside swath: {int(left_teal.sum())} "
      f"(was {int((teal_v & hair_gate_v & ~chunk_v).sum())})")
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
open("roshan_v4g_slim.glb", "wb").write(out)
print("v4g written")
