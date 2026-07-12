#!/usr/bin/env python3
"""
build_chuck_rig.py — Blender bootstrap for Chuck's quadruped rig.

Companion to build_npc_rig.py (the 18-bone humanoid NPC contract). Chuck is the
one four-legged cast member, so he gets his own 20-bone quadruped contract.
The mesh is the Meshy scan `chuck_poodle_slim.glb` (72k tris, unrigged).

Scan quirks this script handles (verified by render on 2026-07-11):
  * The dog is baked ~35 deg diagonal in glTF space — PCA on the vertex cloud
    finds the body axis and the mesh is rotated so the nose faces Blender -Y
    (which round-trips to glTF/Godot +Z, the game's facing convention).
  * The scan pose has the front-RIGHT paw raised and curled, so leg landmarks
    come from per-side leg blob clustering, not a 4-way ground-slice split.

STANDARD QUADRUPED RIG (20 bones)
    root                                (ground, origin)
      hips                              (rear spine base)
        spine -> chest -> neck -> head
        tail1 -> tail2
        legU_BL -> legL_BL -> foot_BL   (hind left)
        legU_BR -> legL_BR -> foot_BR   (hind right)
      chest -> legU_FL -> legL_FL -> foot_FL   (front left)
      chest -> legU_FR -> legL_FR -> foot_FR   (front right)

USAGE
    blender --background --python tools/build_chuck_rig.py -- \
        --glb assets/characters/chuck_poodle_slim.glb \
        --blend tools/out/chuck_rig.blend --renders <dir>

Renders landmark markers + rest/test poses to <dir> for visual QA.
Export to game GLB happens in animate_chuck.py after clips are authored.
"""
import bpy, sys, os, math
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

GLB = os.path.abspath(arg("--glb", "assets/characters/chuck_poodle_slim.glb"))
BLEND_OUT = os.path.abspath(arg("--blend", "tools/out/chuck_rig.blend"))
RENDER_DIR = os.path.abspath(arg("--renders", "tools/out"))
os.makedirs(os.path.dirname(BLEND_OUT), exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)

# ---------------- import ----------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
mesh_obj = next(o for o in bpy.data.objects if o.type == "MESH")
mesh_obj.name = "chuck_body"
# flatten any importer hierarchy so vertex coords == world coords.
# NOTE: bpy.ops.object.transform_apply silently no-ops in --background here
# (stale depsgraph world matrix), so all baking uses mesh.data.transform().
wm = mesh_obj.matrix_world.copy()
mesh_obj.parent = None
mesh_obj.matrix_world = Matrix.Identity(4)
mesh_obj.data.transform(wm)
mesh_obj.data.update()
for o in list(bpy.data.objects):
    if o.type == "EMPTY":
        bpy.data.objects.remove(o)
bpy.ops.object.select_all(action="DESELECT")
mesh_obj.select_set(True)
bpy.context.view_layer.objects.active = mesh_obj

def bake(mat):
    mesh_obj.data.transform(mat)
    mesh_obj.data.update()

# ---------------- align: yaw search so the nose faces -Y ----------------
# PCA fails on this scan (body nearly as wide as long + raised paw skews it).
# Instead: find the yaw whose YZ-plane mirror symmetry is best (dogs are
# bilaterally symmetric), then point the topknot end (tallest slice) at -Y.
vs = [v.co.copy() for v in mesh_obj.data.vertices]
n = len(vs)
cx = sum(v.x for v in vs) / n; cy = sum(v.y for v in vs) / n
pts = [(v.x - cx, v.y - cy, v.z) for v in vs]
VOX = 0.06
def sym_score(a):
    ca, sa = math.cos(a), math.sin(a)
    occ = set()
    for x, y, z in pts:
        occ.add((round((x * ca - y * sa) / VOX), round((x * sa + y * ca) / VOX), round(z / VOX)))
    return sum(1 for (i, jj, k) in occ if (-i, jj, k) in occ) / len(occ)
best = max((sym_score(math.radians(a)), a) for a in range(0, 180, 4))
fine = max((sym_score(math.radians(a * 0.5)), a * 0.5)
           for a in range(2 * (int(best[1]) - 4), 2 * (int(best[1]) + 4)))
yaw = math.radians(fine[1])
print(f"SYMMETRY yaw={fine[1]:.1f}deg score={fine[0]:.3f}")
bake(Matrix.Translation((-cx, -cy, 0)))
bake(Matrix.Rotation(yaw, 4, "Z"))
vs = [v.co.copy() for v in mesh_obj.data.vertices]
def q(sv, f): return sv[min(len(sv) - 1, int(f * len(sv)))]
# nose side: the topknot is the tallest feature; its y-centroid marks the front
zs_ = sorted(v.z for v in vs)
ztop = zs_[-1] - 0.15 * (zs_[-1] - zs_[0])
top_slice = [v for v in vs if v.z > ztop]
y_head = sum(v.y for v in top_slice) / len(top_slice)
if y_head > 0:  # topknot on +Y, flip so nose faces -Y
    bake(Matrix.Rotation(math.pi, 4, "Z"))
    vs = [v.co.copy() for v in mesh_obj.data.vertices]
    print("FLIP 180 (topknot was at +Y)")
# center x on the spine band, drop paws to z-ground reference
xs_ = sorted(v.x for v in vs); ys_ = sorted(v.y for v in vs); zs_ = sorted(v.z for v in vs)
zmin, zmax = zs_[0], zs_[-1]; H = zmax - zmin
ymin, ymax = ys_[0], ys_[-1]; L = ymax - ymin
spine_band = sorted(v.x for v in vs if v.z > zmin + 0.55 * H and v.z < zmin + 0.8 * H)
bake(Matrix.Translation((-q(spine_band, 0.5), 0, 0)))
vs = [v.co.copy() for v in mesh_obj.data.vertices]
xs_ = sorted(v.x for v in vs); ys_ = sorted(v.y for v in vs)
print(f"ALIGNED verts={n} H={H:.3f} L={L:.3f} yaw_fix={math.degrees(yaw):.1f}deg "
      f"x[{xs_[0]:.2f},{xs_[-1]:.2f}] y[{ymin:.2f},{ymax:.2f}] z[{zmin:.2f},{zmax:.2f}]")

# ---------------- orientation renders (before landmarks, so we see failures) ----------------
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "OBJECT"
mesh_obj.color = (0.7, 0.7, 0.75, 1.0)
scene.render.resolution_x, scene.render.resolution_y = 900, 700
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
bpy.context.collection.objects.link(cam)
scene.camera = cam

def shoot(fname, az_deg, el_frac=0.75):
    a = math.radians(az_deg)
    r = 2.4 * max(H, L)
    cam.location = Vector((math.sin(a) * r, -math.cos(a) * r, zmin + el_frac * H))
    d = Vector((0, 0, zmin + 0.45 * H)) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(RENDER_DIR, fname)
    bpy.ops.render.render(write_still=True)

shoot("aligned_side.png", 90)
shoot("aligned_front.png", 0)
shoot("aligned_top.png", 0, el_frac=2.6)

# ---------------- landmarks ----------------
landmarks = {}

def blob(tag, pts):
    c = sum(pts, Vector()) / len(pts)
    landmarks[tag] = c
    print(f"  {tag}: ({c.x:.3f},{c.y:.3f},{c.z:.3f}) n={len(pts)}")
    return c

# hind paws: rear 40%, bottom 18%, split by x sign
rear_low = [v for v in vs if v.y > ymin + 0.6 * L and v.z < zmin + 0.18 * H]
paw_BL = blob("paw_BL", [v for v in rear_low if v.x > 0])
paw_BR = blob("paw_BR", [v for v in rear_low if v.x < 0])
# front leg blobs: front 45% of length, below spine height, split by x sign
front_leg = [v for v in vs if v.y < ymin + 0.45 * L and v.z < zmin + 0.5 * H]
fl_pts = [v for v in front_leg if v.x > 0]
fr_pts = [v for v in front_leg if v.x < 0]
def leg_ends(tag, pts):
    zz = sorted(v.z for v in pts)
    lo_cut, hi_cut = q(zz, 0.15), q(zz, 0.85)
    foot = blob(f"paw_{tag}", [v for v in pts if v.z <= lo_cut])
    top = blob(f"shoulder_{tag}", [v for v in pts if v.z >= hi_cut])
    return foot, top
paw_FL, shoulder_FL = leg_ends("FL", fl_pts)
paw_FR, shoulder_FR = leg_ends("FR", fr_pts)
raised = "FR" if paw_FR.z - zmin > paw_FL.z - zmin else "FL"
print(f"  raised front paw: {raised} (FL z={paw_FL.z - zmin:.2f} FR z={paw_FR.z - zmin:.2f})")
# head: front 25%, upper half; tail pom: rear 10%, above spine
head_c = blob("head", [v for v in vs if v.y < ymin + 0.25 * L and v.z > zmin + 0.5 * H])
tail_c = blob("tail", [v for v in vs if v.y > ymax - 0.10 * L and v.z > zmin + 0.4 * H])

spine_z = zmin + 0.60 * H
belly_z = zmin + 0.42 * H
hips_y = q(ys_, 0.82) - 0.05 * L
chest_y = q(ys_, 0.18) + 0.06 * L

def leg_chain(tag, pawv, top_z, knee_frac=0.5, knee_push=0.0):
    """Chain from body socket down to the paw; knee_push bows the knee (+y back)."""
    sock = Vector((pawv.x * 0.9, pawv.y, top_z))
    knee = sock.lerp(Vector((pawv.x, pawv.y, pawv.z + 0.06 * H)), knee_frac) + Vector((0, knee_push, 0))
    return [(f"legU_{tag}", sock), (f"legL_{tag}", knee),
            (f"foot_{tag}", Vector((pawv.x, pawv.y, pawv.z + 0.02 * H))),
            (f"foot_{tag}_TIP", pawv + Vector((0, -0.05 * L, -0.01)))]

mid = lambda a, b: (a + b) * 0.5
neck_head = Vector((0, chest_y - 0.03 * L, spine_z + 0.06 * H))
CHAINS = {
    "spine_chain": [("hips", Vector((0, hips_y, spine_z))),
                    ("spine", Vector((0, (hips_y + chest_y) / 2, spine_z + 0.03 * H))),
                    ("chest", Vector((0, chest_y, spine_z + 0.02 * H))),
                    ("neck", neck_head),
                    ("head", mid(neck_head, head_c)),
                    ("head_TIP", Vector((head_c.x * 0.3, head_c.y - 0.10 * L, head_c.z + 0.08 * H)))],
    "tail_chain": [("tail1", Vector((0, hips_y + 0.03 * L, spine_z + 0.05 * H))),
                   ("tail2", mid(Vector((0, hips_y + 0.03 * L, spine_z + 0.05 * H)), tail_c)),
                   ("tail2_TIP", tail_c + Vector((0, 0.04 * L, 0.05 * H)))],
    "leg_BL": leg_chain("BL", paw_BL, belly_z, knee_push=0.04 * L),
    "leg_BR": leg_chain("BR", paw_BR, belly_z, knee_push=0.04 * L),
    "leg_FL": leg_chain("FL", paw_FL, min(shoulder_FL.z, belly_z + 0.06 * H)),
    "leg_FR": leg_chain("FR", paw_FR, min(shoulder_FR.z, belly_z + 0.06 * H)),
}
PARENT = {"hips": "root", "tail1": "hips", "legU_BL": "hips", "legU_BR": "hips",
          "legU_FL": "chest", "legU_FR": "chest"}

# ---------------- debug markers render ----------------
marker_objs = []
def marker(pos, size, col):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=pos, segments=8, ring_count=6)
    m = bpy.context.active_object
    mat = bpy.data.materials.new("mk"); mat.diffuse_color = col
    m.data.materials.append(mat)
    marker_objs.append(m)
for c in landmarks.values():
    marker(c, 0.035, (1, 0, 0, 1))
for chain in CHAINS.values():
    for name, pos in chain:
        marker(pos, 0.025, (0, 1, 0, 1))

shoot("markers_side.png", 90)
shoot("markers_front.png", 0)
shoot("markers_top.png", 0, el_frac=2.6)
for m in marker_objs:
    bpy.data.objects.remove(m)

# ---------------- build armature ----------------
arm = bpy.data.armatures.new("chuck_rig")
arm_obj = bpy.data.objects.new("chuck_rig", arm)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.edit_bones
rootb = eb.new("root")
rootb.head, rootb.tail = Vector((0, 0, 0)), Vector((0, 0.15 * L, 0))
for chain in CHAINS.values():
    prev = None
    for name, headpos in chain:
        if name.endswith("_TIP"):
            prev.tail = headpos
            continue
        b = eb.new(name)
        b.head = headpos
        b.tail = headpos + Vector((0, -0.05, 0.05))
        if prev is not None:
            prev.tail = headpos
            b.parent = prev
            b.use_connect = True
        prev = b
for name, pname in PARENT.items():
    eb[name].parent = eb[pname]
bpy.ops.object.mode_set(mode="OBJECT")
print("BONES:", len(arm.bones))

# ---------------- bind via watertight proxy ----------------
# The scan is 70 disconnected shells — bone-heat directly on it gives adjacent
# shells different dominant bones and poses tear the dog apart. Instead:
# voxel-remesh a watertight proxy, auto-weight THAT, then transfer weights to
# the scan mesh by nearest-proxy-vertex sampling (smooth in space, ignores
# scan connectivity). Finally cap at 4 influences and renormalize for glTF.
import numpy as np
from mathutils import kdtree

proxy = mesh_obj.copy()
proxy.data = mesh_obj.data.copy()
proxy.name = "chuck_proxy"
bpy.context.collection.objects.link(proxy)
rm = proxy.modifiers.new("remesh", "REMESH")
rm.mode = "VOXEL"
rm.voxel_size = 0.045
dg = bpy.context.evaluated_depsgraph_get()
proxy_eval = proxy.evaluated_get(dg)
proxy_mesh = bpy.data.meshes.new_from_object(proxy_eval)
proxy.modifiers.remove(proxy.modifiers["remesh"])
old = proxy.data
proxy.data = proxy_mesh
bpy.data.meshes.remove(old)
print(f"PROXY: {len(proxy_mesh.vertices)} verts (voxel remesh)")

bpy.ops.object.select_all(action="DESELECT")
proxy.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type="ARMATURE_AUTO")
print("BIND: proxy automatic weights OK")

bone_names = [b.name for b in arm.bones]
pgi = {vg.index: vg.name for vg in proxy.vertex_groups}
pnv = len(proxy.data.vertices)
PW = np.zeros((pnv, len(bone_names)), dtype=np.float32)
col = {nm: k for k, nm in enumerate(bone_names)}
for v in proxy.data.vertices:
    for g in v.groups:
        nm = pgi.get(g.group)
        if nm in col:
            PW[v.index, col[nm]] = g.weight

kd = kdtree.KDTree(pnv)
for i, v in enumerate(proxy.data.vertices):
    kd.insert(v.co, i)
kd.balance()
me = mesh_obj.data
nv = len(me.vertices)
W = np.zeros((nv, len(bone_names)), dtype=np.float32)
for i, v in enumerate(me.vertices):
    hits = kd.find_n(v.co, 3)   # inverse-distance blend of 3 nearest
    tot = 0.0
    for _, pj, dist in hits:
        wgt = 1.0 / max(dist, 1e-5)
        W[i] += wgt * PW[pj]
        tot += wgt
    W[i] /= tot
# top-4 influences, renormalize
order = np.argsort(-W, axis=1)
mask = np.zeros_like(W, dtype=bool)
np.put_along_axis(mask, order[:, :4], True, axis=1)
W = np.where(mask, W, 0.0)
W /= np.maximum(W.sum(axis=1, keepdims=True), 1e-8)
for vg in list(mesh_obj.vertex_groups):
    mesh_obj.vertex_groups.remove(vg)
vgs = [mesh_obj.vertex_groups.new(name=nm) for nm in bone_names]
for i in range(nv):
    for k in np.nonzero(W[i])[0]:
        vgs[k].add([i], float(W[i, k]), "REPLACE")
mesh_obj.parent = arm_obj
mod = mesh_obj.modifiers.new("Armature", "ARMATURE")
mod.object = arm_obj
bpy.data.objects.remove(proxy)
print("WEIGHTS transferred from proxy: 3-NN inverse-distance, top-4, renormalized")

# ---------------- verification renders ----------------
def pose(rots):
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
    for bone, (rx, ry, rz) in rots.items():
        arm_obj.pose.bones[bone].rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
    bpy.context.view_layer.update()

pose({})
shoot("rig_rest_side.png", 90)
shoot("rig_rest_front.png", 0)
pose({"legU_FL": (45, 0, 0), "legL_FL": (-50, 0, 0),
      "legU_BR": (-40, 0, 0), "legL_BR": (45, 0, 0),
      "neck": (-20, 0, 0), "head": (-15, 0, 25), "tail1": (30, 0, 0)})
shoot("rig_test_bend.png", 90)
pose({"hips": (-28, 0, 0), "spine": (-14, 0, 0), "chest": (-8, 0, 0),
      "neck": (22, 0, 0), "head": (14, 0, 0),
      "legU_FL": (-30, 0, 0), "legU_FR": (-30, 0, 0),
      "tail1": (35, 0, 0), "tail2": (20, 0, 0)})
shoot("rig_test_sit.png", 70, el_frac=0.9)
shoot("rig_test_sit_side.png", 90, el_frac=0.7)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print("SAVED", BLEND_OUT)
