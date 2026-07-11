#!/usr/bin/env python3
"""ROSHAN V2 stage R2-B — put the Meshy body on her EXISTING skeleton.

Keeps the 26-bone armature from assets/characters/roshan.glb (player.gd
drives those bone names procedurally every frame), throws away the old
plushie mesh, aligns the new Meshy sculpt to the armature's bounds, and
binds it with automatic weights. The result is a drop-in GLB: same
skeleton, new body.

Also bakes a quick smoke test: rotates tail4 and armU and renders both the
rest pose and the bent pose to PNG, so weight quality can be eyeballed
without opening Blender.

Usage:
  blender -b -noaudio --python tools/roshan_v2_retarget.py -- \
      gen2/meshy/roshan_v2/static.glb assets/characters/roshan_v2.glb /tmp/preview [wings]

With "wings": vertices far from the (wingless) source body are detected as
wing geometry, split L/R, weighted 100% to NEW wingL/wingR bones parented to
chest, and a calibration pass reports which local rotation axis produces the
flap sweep (that axis goes into player.gd's procedural flutter).
"""
import math
import os
import sys

import bpy
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
new_mesh_glb, out_glb, preview = argv[0], argv[1], argv[2]
want_wings = len(argv) > 3 and argv[3] == "wings"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---- 1. old character: keep armature, remember mesh bounds, drop the mesh
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/characters/roshan.glb"))
arm = next((o for o in bpy.context.scene.objects if o.type == "ARMATURE"), None)
assert arm is not None, "no armature in roshan.glb"
old_meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]


def world_bounds(objs):
    mins = [1e9] * 3
    maxs = [-1e9] * 3
    for ob in objs:
        for c in ob.bound_box:
            w = ob.matrix_world @ mathutils.Vector(c)
            for i in range(3):
                mins[i] = min(mins[i], w[i])
                maxs[i] = max(maxs[i], w[i])
    return mathutils.Vector(mins), mathutils.Vector(maxs)


omin, omax = world_bounds(old_meshes)

# ---- 2. new sculpt in, aligned to the old body's height and floor
before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, new_mesh_glb))
new_meshes = [o for o in bpy.context.scene.objects
              if o.type == "MESH" and o not in before]
assert new_meshes, "no mesh in the Meshy glb"
nmin, nmax = world_bounds(new_meshes)
scale = (omax.z - omin.z) / max(nmax.z - nmin.z, 1e-6)   # match HEIGHT
for ob in new_meshes:
    ob.scale = ob.scale * scale
bpy.context.view_layer.update()
nmin, nmax = world_bounds(new_meshes)
# centre horizontally on the old body, feet/tail tip on the old floor line
delta = mathutils.Vector((
    (omin.x + omax.x) * 0.5 - (nmin.x + nmax.x) * 0.5,
    (omin.y + omax.y) * 0.5 - (nmin.y + nmax.y) * 0.5,
    omin.z - nmin.z,
))
for ob in new_meshes:
    ob.location += delta
bpy.context.view_layer.update()

# ---- 3. bind by WEIGHT TRANSFER from the old body (same armature, same
# proportions - bone-heat auto weights fail silently on Meshy meshes)
bpy.ops.object.select_all(action="DESELECT")
for ob in new_meshes:
    ob.select_set(True)
bpy.context.view_layer.objects.active = new_meshes[0]
if len(new_meshes) > 1:
    bpy.ops.object.join()
body = bpy.context.view_layer.objects.active
new_meshes = [body]
src = max(old_meshes, key=lambda o: len(o.vertex_groups))
print("[i] weight source:", src.name, "with", len(src.vertex_groups), "groups")
for vg in src.vertex_groups:
    if vg.name not in body.vertex_groups:
        body.vertex_groups.new(name=vg.name)
bpy.ops.object.select_all(action="DESELECT")
src.select_set(True)
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.data_transfer(use_reverse_transfer=True,
                             data_type="VGROUP_WEIGHTS",
                             vert_mapping="POLYINTERP_NEAREST",
                             layers_select_src="NAME",
                             layers_select_dst="ALL")
body.parent = arm
mod = body.modifiers.new("Armature", "ARMATURE")
mod.object = arm
print("[ok] weight-transferred", len(body.vertex_groups), "groups onto the V2 body")

if want_wings:
    # ---- wings: geometry with NO counterpart on the wingless source body.
    # Distance-to-source classifies them; far verts split L/R by x sign.
    from mathutils.bvhtree import BVHTree
    dg0 = bpy.context.evaluated_depsgraph_get()
    bvh = BVHTree.FromObject(src, dg0)
    src_inv = src.matrix_world.inverted()
    h = (omax.z - omin.z)
    thresh = h * 0.055
    wing_all = []
    z_floor = omin.z + h * 0.55   # wings live on the UPPER body: keeps the
    # coiled fairy tail (far from the straight source tail) out of the wings
    for v in body.data.vertices:
        w = body.matrix_world @ v.co
        if w.z < z_floor:
            continue
        loc = src_inv @ w
        hit = bvh.find_nearest(loc)
        if hit[0] is not None and (hit[0] - loc).length > thresh:
            wing_all.append((v.index, w.x))
    # 2-means on x separates the wings even when the model is off-centre or
    # the wings hold unequal vertex counts (median split skewed the pivots)
    xs = [x for _, x in wing_all]
    cl, cr = max(xs), min(xs)
    for _ in range(12):
        left = [x for x in xs if abs(x - cl) <= abs(x - cr)]
        right = [x for x in xs if abs(x - cl) > abs(x - cr)]
        if left:
            cl = sum(left) / len(left)
        if right:
            cr = sum(right) / len(right)
    wingL = [i for i, x in wing_all if abs(x - cl) <= abs(x - cr)]
    wingR = [i for i, x in wing_all if abs(x - cl) > abs(x - cr)]
    print(f"[i] wing verts: L={len(wingL)} R={len(wingR)} (thresh {thresh:.3f})")
    assert len(wingL) > 50 and len(wingR) > 50, "wing detection found too little geometry"
    import mathutils as _mu
    wl_c = sum(( (body.matrix_world @ body.data.vertices[i].co) for i in wingL), _mu.Vector()) / len(wingL)
    wr_c = sum(( (body.matrix_world @ body.data.vertices[i].co) for i in wingR), _mu.Vector()) / len(wingR)
    # hinge each wing where it MEETS the body (its vert nearest the chest),
    # tip at its farthest vert - an anatomical pivot, so the same flap angle
    # sweeps the whole wing instead of pivoting around empty space
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    chest = arm.data.edit_bones.get("chest")
    chest_w = arm.matrix_world @ chest.head
    inv_arm = arm.matrix_world.inverted()
    for bname, verts, sign in (("wingL", wingL, 1.0), ("wingR", wingR, -1.0)):
        pts = [body.matrix_world @ body.data.vertices[i].co for i in verts]
        hinge = min(pts, key=lambda pt: (pt - chest_w).length)
        eb = arm.data.edit_bones.new(bname)
        eb.head = inv_arm @ hinge
        # canonical HORIZONTAL outward bone (same shape both sides, roll 0):
        # per-wing local axes then relate by pure mirror, so one calibrated
        # recipe drives both wings believably
        eb.tail = inv_arm @ (hinge + _mu.Vector((sign * h * 0.28, 0.0, 0.0)))
        eb.roll = 0.0
        eb.parent = chest
    bpy.ops.object.mode_set(mode="OBJECT")
    # SOFT wing ownership: hard boundaries tore the membrane where detected
    # outer-wing verts met body-weighted inner-wing verts (playtest: wings
    # ripped into slabs). Seed weight 1 on detected verts, then diffuse the
    # weight outward across mesh edges so the wing root BENDS instead.
    adj = {}
    for e in body.data.edges:
        a, b2 = e.vertices
        adj.setdefault(a, []).append(b2)
        adj.setdefault(b2, []).append(a)
    for bname, verts in (("wingL", wingL), ("wingR", wingR)):
        wmap = {i: 1.0 for i in verts}
        for _ in range(3):
            frontier = {}
            for i, wv in list(wmap.items()):
                for nb in adj.get(i, []):
                    cand = wv * 0.55
                    if cand > wmap.get(nb, 0.0) and cand > frontier.get(nb, 0.0):
                        frontier[nb] = cand
            wmap.update(frontier)
        vg = body.vertex_groups.new(name=bname)
        for i, wv in wmap.items():
            # scale existing body weights down so wing + body still sum to 1
            for g in body.data.vertices[i].groups:
                g.weight = g.weight * (1.0 - wv)
            vg.add([i], wv, "REPLACE")
    print(f"[ok] wingL/wingR soft-weighted ({len(wingL)}/{len(wingR)} seeds + 3-ring falloff)")

for ob in old_meshes:
    bpy.data.objects.remove(ob, do_unlink=True)

# ---- 4. export the drop-in glb
os.makedirs(os.path.dirname(os.path.join(ROOT, out_glb)), exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, out_glb),
                          export_format="GLB", export_yup=True)
print("[ok] exported", out_glb)

# ---- 5. smoke renders: rest pose + a bent pose (tail + arm)
world = bpy.data.worlds.new("w")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
bpy.context.scene.world = world
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 2.5
sun.rotation_euler = (math.radians(55), 0, math.radians(35))
bpy.context.scene.collection.objects.link(sun)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam
sc = bpy.context.scene
sc.render.resolution_x = 512
sc.render.resolution_y = 512
nmin, nmax = world_bounds(new_meshes)
c = (nmin + nmax) * 0.5
size = max(nmax - nmin)
cam.location = (c.x + size * 1.9, c.y - size * 1.9, c.z + size * 0.35)
cam.rotation_euler = (c - mathutils.Vector(cam.location)).to_track_quat("-Z", "Y").to_euler()

os.makedirs(preview, exist_ok=True)
sc.render.filepath = os.path.join(preview, "rest.png")
bpy.ops.render.render(write_still=True)

bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for bone_name, rot in (("tail4", 35), ("tail6", 30), ("armU", 40), ("head", -15)):
    pb = arm.pose.bones.get(bone_name)
    if pb is None:
        print("[!] missing bone:", bone_name)
        continue
    pb.rotation_mode = "XYZ"
    pb.rotation_euler.x = math.radians(rot)
bpy.ops.object.mode_set(mode="OBJECT")
# numeric deform check: the tail tip must MOVE when the tail bends
dg = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(dg)
tip_before = min((ev.matrix_world @ v.co).z for v in ev.data.vertices)
sc.render.filepath = os.path.join(preview, "bent.png")
bpy.ops.render.render(write_still=True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="POSE")
for pb in arm.pose.bones:
    pb.rotation_euler = (0, 0, 0)
    pb.rotation_quaternion = (1, 0, 0, 0)
bpy.ops.object.mode_set(mode="OBJECT")
dg = bpy.context.evaluated_depsgraph_get()
ev = body.evaluated_get(dg)
tip_after = min((ev.matrix_world @ v.co).z for v in ev.data.vertices)
moved = abs(tip_before - tip_after)
print(f"[{'ok' if moved > 0.02 else '!'}] deform check: tail tip moved {moved:.3f}")

if want_wings:
    # ---- calibrate PER WING: which local axis+sign sweeps THAT wing toward
    # world +Y (forward)? The recipe below is copied verbatim into player.gd.
    import mathutils as _mu
    def cluster_cen(gname):
        gi = body.vertex_groups[gname].index
        ids = [v.index for v in body.data.vertices if gi in [g.group for g in v.groups]]
        dgx = bpy.context.evaluated_depsgraph_get()
        evx = body.evaluated_get(dgx)
        return sum(((evx.matrix_world @ evx.data.vertices[i].co) for i in ids), _mu.Vector()) / len(ids), ids
    recipe = {}
    for bname in ("wingL", "wingR"):
        base_c, _ids = cluster_cen(bname)
        best = None
        for axis, vec in (("X", (1, 0, 0)), ("Y", (0, 1, 0)), ("Z", (0, 0, 1))):
            for sgn in (1.0, -1.0):
                pb = arm.pose.bones[bname]
                pb.rotation_mode = "QUATERNION"
                pb.rotation_quaternion = _mu.Quaternion(_mu.Vector(vec), 0.5 * sgn)
                c2, _ = cluster_cen(bname)
                pb.rotation_quaternion = _mu.Quaternion()
                d = c2 - base_c
                if best is None or d.y > best[0]:
                    best = (d.y, axis, sgn, d)
        recipe[bname] = best
        print(f"[ok] {bname} RECIPE: local {best[1]} sign {best[2]:+.0f} (dy {best[0]:.3f}, dz {best[3].z:.3f})")
    # flap preview: both wings swept BACK using the recipe
    for bname in ("wingL", "wingR"):
        _, axis, sgn, _ = recipe[bname]
        vec = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}[axis]
        arm.pose.bones[bname].rotation_quaternion = _mu.Quaternion(_mu.Vector(vec), -0.45 * sgn)
    sc.render.filepath = os.path.join(preview, "flap.png")
    bpy.ops.render.render(write_still=True)
    for bname in ("wingL", "wingR"):
        arm.pose.bones[bname].rotation_quaternion = _mu.Quaternion()
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, out_glb),
                              export_format="GLB", export_yup=True)
    print("[ok] re-exported with wing bones:", out_glb)

print("[ok] previews in", preview)
