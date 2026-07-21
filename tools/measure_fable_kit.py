"""R-GOV1 export measurement for assets/fable_kit: triangles, materials,
mesh objects, loose islands, dimensions — parsed from the GLB files themselves.

Usage: blender --background --python tools/measure_fable_kit.py
"""
import os

import bpy
import bmesh
from mathutils import Vector

KIT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "fable_kit")

for fname in sorted(os.listdir(KIT)):
    if not fname.endswith(".glb"):
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(KIT, fname))
    tris = 0
    mats = set()
    n_mesh = 0
    islands = 0
    lo = Vector((1e9,) * 3)
    hi = Vector((-1e9,) * 3)
    for ob in bpy.data.objects:
        if ob.type != "MESH":
            continue
        n_mesh += 1
        me = ob.data
        tris += sum(len(p.vertices) - 2 for p in me.polygons)
        for m in me.materials:
            if m:
                mats.add(m.name.split(".")[0])
        bm = bmesh.new()
        bm.from_mesh(me)
        seen = set()
        for v in bm.verts:
            if v.index in seen:
                continue
            islands += 1
            stack = [v]
            while stack:
                cur = stack.pop()
                if cur.index in seen:
                    continue
                seen.add(cur.index)
                for e in cur.link_edges:
                    stack.append(e.other_vert(cur))
        bm.free()
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], w[i]) for i in range(3)))
            hi = Vector((max(hi[i], w[i]) for i in range(3)))
    size = hi - lo
    print(f"MEASURE|{fname}|tris={tris}|meshes={n_mesh}|islands={islands}"
          f"|mats={len(mats)}:{sorted(mats)}"
          f"|size=({size.x:.2f},{size.y:.2f},{size.z:.2f})")
