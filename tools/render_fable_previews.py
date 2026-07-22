"""Render 2-view preview sheets of every fable_kit GLB for visual QA.

Usage: blender --background --python tools/render_fable_previews.py -- <out_dir>
"""
import math
import os
import sys

import bpy
from mathutils import Vector

OUT = sys.argv[sys.argv.index("--") + 1]
KIT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "fable_kit")
os.makedirs(OUT, exist_ok=True)

for fname in sorted(os.listdir(KIT)):
    if not fname.endswith(".glb"):
        continue
    stem = fname[:-4]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(KIT, fname))
    # bounds
    lo = Vector((1e9,) * 3)
    hi = Vector((-1e9,) * 3)
    for ob in bpy.data.objects:
        if ob.type != "MESH":
            continue
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], w[i]) for i in range(3)))
            hi = Vector((max(hi[i], w[i]) for i in range(3)))
    ctr = (lo + hi) * 0.5
    diag = (hi - lo).length

    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.5
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    bpy.context.collection.objects.link(sun)
    world = bpy.data.worlds.new("w")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.82, 0.90, 0.94, 1.0)
    bg.inputs[1].default_value = 1.0
    bpy.context.scene.world = world

    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 24
    sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x = 640
    sc.render.resolution_y = 640
    sc.render.film_transparent = False

    for tag, ang in (("front", math.radians(-90)), ("three_q", math.radians(-38))):
        d = diag * 1.35
        cam.location = ctr + Vector((math.cos(ang) * d, math.sin(ang) * d,
                                     diag * 0.42))
        look = ctr - cam.location
        cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(OUT, f"{stem}_{tag}.png")
        bpy.ops.render.render(write_still=True)
        print(f"RENDERED {stem}_{tag}")
print("PREVIEWS DONE")
