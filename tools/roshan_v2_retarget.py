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
      gen2/meshy/roshan_v2/static.glb assets/characters/roshan_v2.glb /tmp/preview
"""
import math
import os
import sys

import bpy
import mathutils

argv = sys.argv[sys.argv.index("--") + 1:]
new_mesh_glb, out_glb, preview = argv[0], argv[1], argv[2]
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
for ob in old_meshes:
    bpy.data.objects.remove(ob, do_unlink=True)

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

# ---- 3. bind: automatic weights against the KEPT armature
bpy.ops.object.select_all(action="DESELECT")
for ob in new_meshes:
    ob.select_set(True)
bpy.context.view_layer.objects.active = arm
arm.select_set(True)
bpy.ops.object.parent_set(type="ARMATURE_AUTO")
print("[ok] bound", len(new_meshes), "mesh object(s) to", arm.name)

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
sc.render.filepath = os.path.join(preview, "bent.png")
bpy.ops.render.render(write_still=True)
print("[ok] previews in", preview)
