"""GEN2 prop import pass (headless Blender).

Meshy GLBs ship with huge embedded textures (4-9 MB per prop - an APK
killer). This pass: downscales textures to <=1024, strips normal/metallic
maps (the toon look doesn't use them), optionally lifts shadow-baked dark
regions (Meshy bakes the sprite's unseen back side dark), optionally
posterizes the albedo to a few flat pastel fills (the Wind Waker look:
Meshy paints soft gradients and baked shading; the storybook wants flat
color fields), and re-exports to assets/props/gen2/<name>.glb.

Usage:
  blender --background --python tools/shrink_glb.py -- <in.glb> <out.glb> [lift] [posterize[=N]]
"""
import bpy
import os
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
lift = "lift" in argv[2:]
posterize = 0
for a in argv[2:]:
    if a == "posterize":
        posterize = 8
    elif a.startswith("posterize="):
        posterize = int(a.split("=")[1])

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(src))

swap = {}
for img in list(bpy.data.images):
    if img.size[0] == 0:
        continue
    if max(img.size) > 1024:
        img.scale(min(img.size[0], 1024), min(img.size[1], 1024))
    if lift:
        # lift baked-dark shadow regions: strong gamma on dark pixels,
        # near-identity on bright ones, so the lit side keeps its colors.
        # Edited pixels on a PACKED image don't survive export, so bake
        # them into a fresh image datablock and swap it into the nodes.
        px = list(img.pixels)
        for i in range(0, len(px), 4):
            v = max(px[i], px[i + 1], px[i + 2])
            t = max(0.0, min(1.0, (0.6 - v) / 0.6))   # 1 in shadow, 0 in light
            g = 1.0 - 0.5 * t                          # gamma 1.0 -> 0.5
            for c in range(3):
                px[i + c] = px[i + c] ** g
        fresh = bpy.data.images.new(img.name + "_lift", img.size[0], img.size[1])
        fresh.pixels = px
        fresh.pack()
        swap[img.name] = fresh
    if posterize:
        # k-means the albedo down to a handful of flat fills. The GEN2 art is
        # already the family palette, so the fills keep their exact colors —
        # no pastel re-drift (that double-lifts and washes it out). Cluster
        # assignment runs on a 3x3-blurred copy so JPEG grain can't speckle
        # pixels across fill boundaries. New datablocks default to PNG so
        # flat fills export crisp instead of JPEG-ringed.
        import numpy as np
        base = swap.get(img.name, img)
        w, hgt = base.size[0], base.size[1]
        arr = np.array(base.pixels, dtype=np.float32).reshape(hgt, w, 4)
        rgb = arr[:, :, :3]
        soft = rgb.copy()
        for ax in (0, 1):
            soft = (np.roll(soft, 1, axis=ax) + soft + np.roll(soft, -1, axis=ax)) / 3.0
        flatpx = soft.reshape(-1, 3)
        rng = np.random.default_rng(7)
        sample = flatpx[rng.choice(len(flatpx), min(40000, len(flatpx)), replace=False)]
        cents = sample[rng.choice(len(sample), posterize, replace=False)]
        for _ in range(12):
            d = ((sample[:, None, :] - cents[None, :, :]) ** 2).sum(axis=2)
            lab = d.argmin(axis=1)
            for k in range(posterize):
                pick = sample[lab == k]
                if len(pick):
                    cents[k] = pick.mean(axis=0)
        d = ((flatpx[:, None, :] - cents[None, :, :]) ** 2).sum(axis=2)
        arr[:, :, :3] = cents[d.argmin(axis=1)].reshape(hgt, w, 3)
        flat = bpy.data.images.new(img.name + "_flat", w, hgt)
        flat.pixels = arr.reshape(-1).tolist()
        flat.pack()
        swap[img.name] = flat
if swap:
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        for n in mat.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image and n.image.name in swap:
                n.image = swap[n.image.name]

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        continue
    bsdf.inputs["Roughness"].default_value = 1.0
    bsdf.inputs["Metallic"].default_value = 0.0
    # drop normal-map links (toon look, and saves a texture per prop)
    for link in list(mat.node_tree.links):
        if link.to_socket.name == "Normal":
            mat.node_tree.links.remove(link)

os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
# posterized flat fills must stay PNG (JPEG rings hard edges); AUTO keeps the
# fresh PNG datablocks as PNG, and flat-color PNGs compress smaller anyway
fmt = "AUTO" if posterize else "JPEG"
bpy.ops.export_scene.gltf(filepath=os.path.abspath(dst), export_format="GLB",
                          export_image_format=fmt, export_jpeg_quality=85)
print("SHRUNK", src, "->", dst)
