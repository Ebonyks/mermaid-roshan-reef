"""Print world-space bounding boxes of every mesh object in the given GLBs.

Usage: blender --background --python tools/probe_glb_bounds.py -- file1.glb file2.glb ...
"""
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]

for path in argv:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.gltf(filepath=path)
    except Exception as exc:  # noqa: BLE001
        print(f"=== {path}: IMPORT FAILED: {exc}")
        continue
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    n_mesh = 0
    for ob in bpy.data.objects:
        if ob.type != "MESH":
            continue
        n_mesh += 1
        for corner in ob.bound_box:
            w = ob.matrix_world @ Vector(corner)
            lo = Vector((min(lo[i], w[i]) for i in range(3)))
            hi = Vector((max(hi[i], w[i]) for i in range(3)))
    size = hi - lo
    print(f"=== {path}: meshes={n_mesh} "
          f"min=({lo.x:.2f},{lo.y:.2f},{lo.z:.2f}) "
          f"max=({hi.x:.2f},{hi.y:.2f},{hi.z:.2f}) "
          f"size=({size.x:.2f},{size.y:.2f},{size.z:.2f})")
