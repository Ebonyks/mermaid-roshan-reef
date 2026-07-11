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
    # split at the wing cloud's own median: Meshy centres the WHOLE model, so
    # the coiled tail biases x=0 away from the line between the wings
    xs = sorted(x for _, x in wing_all)
    mid_x = xs[len(xs) // 2]
    wingL = [i for i, x in wing_all if x > mid_x]
    wingR = [i for i, x in wing_all if x <= mid_x]
    print(f"[i] wing verts: L={len(wingL)} R={len(wingR)} (thresh {thresh:.3f})")
    assert len(wingL) > 50 and len(wingR) > 50, "wing detection found too little geometry"
    import mathutils as _mu
    wl_c = sum(( (body.matrix_world @ body.data.vertices[i].co) for i in wingL), _mu.Vector()) / len(wingL)
    wr_c = sum(( (body.matrix_world @ body.data.vertices[i].co) for i in wingR), _mu.Vector()) / len(wingR)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    chest = arm.data.edit_bones.get("chest")
    inv_arm = arm.matrix_world.inverted()
    for bname, cen in (("wingL", wl_c), ("wingR", wr_c)):
        eb = arm.data.edit_bones.new(bname)
        root = _mu.Vector((0.0, cen.y, cen.z)) * 0.35 + _mu.Vector((cen.x * 0.1, cen.y * 0.65, cen.z * 0.65))
        eb.head = inv_arm @ _mu.Vector((cen.x * 0.15, cen.y, cen.z))
        eb.tail = inv_arm @ cen
        eb.parent = chest
    bpy.ops.object.mode_set(mode="OBJECT")
    for bname, verts in (("wingL", wingL), ("wingR", wingR)):
        vg = body.vertex_groups.new(name=bname)
        # rigid wings: exclusive ownership so the flap cannot fight body weights
        for g in body.vertex_groups:
            if g.name != bname:
                g.remove(verts)
        vg.add(verts, 1.0, "REPLACE")
    print("[ok] wingL/wingR bones added (parent: chest), wing verts exclusively weighted")

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
    # ---- calibrate the flap axis: which bone-local rotation sweeps the wing
    # forward/back (world Y)? That axis goes into player.gd.
    import mathutils as _mu
    wing_ids = [v.index for v in body.data.vertices
                if body.vertex_groups["wingL"].index in [g.group for g in v.groups]]
    def wing_cen():
        dgx = bpy.context.evaluated_depsgraph_get()
        evx = body.evaluated_get(dgx)
        return sum(((evx.matrix_world @ evx.data.vertices[i].co) for i in wing_ids), _mu.Vector()) / len(wing_ids)
    base_c = wing_cen()
    best = None
    for axis in ("X", "Y", "Z"):
        pb = arm.pose.bones["wingL"]
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = _mu.Quaternion(_mu.Vector((1 if axis=="X" else 0, 1 if axis=="Y" else 0, 1 if axis=="Z" else 0)), 0.6)
        d = wing_cen() - base_c
        pb.rotation_quaternion = _mu.Quaternion()
        print(f"[i] flap axis {axis}: wing centroid moved dx={d.x:.3f} dy={d.y:.3f} dz={d.z:.3f}")
        score = abs(d.y)
        if best is None or score > best[1]:
            best = (axis, score)
    print(f"[ok] FLAP AXIS: local {best[0]} (world-Y sweep {best[1]:.3f}) — use this in player.gd")
    pb = arm.pose.bones["wingL"]
    pb.rotation_quaternion = _mu.Quaternion(_mu.Vector((1 if best[0]=="X" else 0, 1 if best[0]=="Y" else 0, 1 if best[0]=="Z" else 0)), 0.7)
    arm.pose.bones["wingR"].rotation_mode = "QUATERNION"
    arm.pose.bones["wingR"].rotation_quaternion = _mu.Quaternion(_mu.Vector((1 if best[0]=="X" else 0, 1 if best[0]=="Y" else 0, 1 if best[0]=="Z" else 0)), -0.7)
    sc.render.filepath = os.path.join(preview, "flap.png")
    bpy.ops.render.render(write_still=True)
    # re-export WITH the wing bones baked into the rig
    bpy.ops.object.mode_set(mode="POSE")
    for pbx in arm.pose.bones:
        pbx.rotation_quaternion = _mu.Quaternion()
        pbx.rotation_euler = (0, 0, 0)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, out_glb),
                              export_format="GLB", export_yup=True)
    print("[ok] re-exported with wing bones:", out_glb)

print("[ok] previews in", preview)
