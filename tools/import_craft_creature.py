"""Craft-creature import pass (headless Blender).

Web-UI Meshy generations ship ~300k faces (no polycount option, unlike the
API pipeline's 8k target) plus 2K textures. This pass: decimates to the
mobile budget, downscales textures to <=1024, strips normal/metallic maps
(the sway shader only reads albedo), and re-exports for assets/props/gen2/.

Usage:
  blender --background --python tools/import_craft_creature.py -- <in.glb> <out.glb> [faces=9000]
"""
import bpy
import os
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
target_faces = 9000
for a in argv[2:]:
    if a.startswith("faces="):
        target_faces = int(a.split("=")[1])

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(src))

# ---- decimate every mesh to the shared budget ----
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
total = sum(len(o.data.polygons) for o in meshes)
if total > target_faces:
    ratio = target_faces / total
    dg = bpy.context.evaluated_depsgraph_get()
    for o in meshes:
        mod = o.modifiers.new("dec", "DECIMATE")
        mod.ratio = ratio
        dg = bpy.context.evaluated_depsgraph_get()
        newmesh = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        o.modifiers.remove(o.modifiers["dec"])
        old = o.data
        o.data = newmesh
        bpy.data.meshes.remove(old)
    print(f"DECIMATED {total} -> {sum(len(o.data.polygons) for o in meshes)} faces")

# ---- shrink textures, drop non-albedo maps (same policy as shrink_glb.py) ----
for img in list(bpy.data.images):
    if img.size[0] == 0:
        continue
    if max(img.size) > 1024:
        img.scale(min(img.size[0], 1024), min(img.size[1], 1024))

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        continue
    for sock_name in ("Normal", "Metallic", "Roughness"):
        sock = bsdf.inputs.get(sock_name)
        if sock is not None:
            for lk in list(sock.links):
                nt.links.remove(lk)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.9
    # a stripped black emissive map otherwise renders the model pure white
    em = bsdf.inputs.get("Emission Color")
    if em is not None:
        for lk in list(em.links):
            nt.links.remove(lk)
        em.default_value = (0, 0, 0, 1)
    es = bsdf.inputs.get("Emission Strength")
    if es is not None:
        es.default_value = 0.0

bpy.ops.export_scene.gltf(filepath=os.path.abspath(dst), export_format="GLB", export_yup=True)
print("EXPORTED", dst, os.path.getsize(os.path.abspath(dst)), "bytes")
