#!/usr/bin/env python3
"""
bake_nano_wrap.py — Blender batch: dress CC0 pack GLBs in the nano-banana
painted sheets, offline (same tool family as build_npc_rig.py — the Blender
side of the character/asset conversion pipeline).

WHY THIS EXISTS
---------------
The runtime _toon_tile() wrap re-skins meshes the GDScript can reach, but the
Butterfly World garden, the fetch tray, the castle throne/bed etc. are pack
GLBs whose flat Kenney/Quaternius palette look is baked into the asset. This
tool rewrites the asset itself:

1. Box-project fresh UVs per face (dominant-normal-axis projection via bmesh —
   deterministic, no operator context needed headless).
2. Classify every material by its original colour (flat baseColorFactor, or a
   palette-texture sample at the faces' original UV centroid) and pick the
   matching nano-banana sheet: wood / cliff / grass / fabric / marble.
3. Multiply the ORIGINAL part colour into an embedded 512px copy of the sheet,
   so a gold trim stays gold and a red cushion stays red — export-safe (no
   reliance on glTF factor/mix-node conventions).
4. Re-export the GLB in place.

USAGE (in-repo Blender):
    blender -b --python tools/bake_nano_wrap.py -- <repo_root> <glb> [<glb>...]

Per-model overrides live in OVERRIDES below (e.g. the bed's white mattress
must read fabric, not marble).
"""
import bpy
import bmesh
import sys
import os
import colorsys
import numpy as np

SHEET_DIR = "assets/terrain"
SHEETS = {k: f"up_{k}_col.jpg" for k in ["wood", "cliff", "grass", "fabric", "marble", "sand", "snow"]}
TILES = 2.6          # sheet repeats across the model's largest dimension
BAKE_RES = 512
# per-model: force a tint for palette-lost imports (all-default-grey materials)
FORCE_TINT = {"trop_bigleaf": (0.42, 0.72, 0.45)}
# per-model: force a default sheet for materials that are NOT wood-hued
OVERRIDES = {"bed": "fabric", "tray": "wood", "trop_bigleaf": "grass"}   # bigleaf: palette lost on import (all mats default grey)

_sheet_px = {}       # sheet key -> HxWx4 float array


def load_sheet(root, key):
    if key not in _sheet_px:
        img = bpy.data.images.load(os.path.join(root, SHEET_DIR, SHEETS[key]))
        img.scale(BAKE_RES, BAKE_RES)
        px = np.empty(len(img.pixels), dtype=np.float32)
        img.pixels.foreach_get(px)
        _sheet_px[key] = px.reshape(BAKE_RES, BAKE_RES, 4)
        bpy.data.images.remove(img)
    return _sheet_px[key]


def classify(rgb, override_default):
    h, s, v = colorsys.rgb_to_hsv(*rgb[:3])
    hd = h * 360.0
    if s < 0.14:
        base = "marble" if v > 0.72 else "cliff"
    elif 10.0 <= hd < 52.0 and not (hd < 18.0 and s > 0.72 and v > 0.55):
        base = "wood"       # browns reach down to ~10deg; vivid reds stay fabric
    elif 52.0 <= hd < 75.0:
        base = "marble"       # golds: sheet is pale, the tint bake keeps the gold
    elif 75.0 <= hd < 175.0:
        base = "grass"
    elif 175.0 <= hd < 262.0:
        base = "cliff"
    else:
        base = "fabric"       # reds / pinks / purples
    if override_default and base != "wood":
        return override_default
    return base


def mat_base_color(mat, sample_uv):
    """original colour: palette-texture sample at the faces' uv centroid,
    else the Principled base colour factor."""
    if not mat.use_nodes:
        return tuple(mat.diffuse_color)[:3]
    principled, img = None, None
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            principled = n
        if n.type == "TEX_IMAGE" and n.image is not None:
            img = n.image
    if img is not None and sample_uv is not None:
        w, hgt = img.size
        if w > 0 and hgt > 0:
            px = np.empty(len(img.pixels), dtype=np.float32)
            img.pixels.foreach_get(px)
            px = px.reshape(hgt, w, 4)
            x = int(sample_uv[0] % 1.0 * (w - 1))
            y = int(sample_uv[1] % 1.0 * (hgt - 1))
            return tuple(px[y, x, :3])
    if principled is not None:
        return tuple(principled.inputs["Base Color"].default_value)[:3]
    return tuple(mat.diffuse_color)[:3]


def box_uv(obj, cube_size):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    layer = bm.loops.layers.uv.get("NanoUV") or bm.loops.layers.uv.new("NanoUV")
    inv = 1.0 / max(cube_size, 1e-6)
    for f in bm.faces:
        n = f.normal
        ax = 0 if abs(n.x) >= abs(n.y) and abs(n.x) >= abs(n.z) else (1 if abs(n.y) >= abs(n.z) else 2)
        for lp in f.loops:
            co = obj.matrix_world @ lp.vert.co
            if ax == 0:
                lp[layer].uv = (co.y * inv, co.z * inv)
            elif ax == 1:
                lp[layer].uv = (co.x * inv, co.z * inv)
            else:
                lp[layer].uv = (co.x * inv, co.y * inv)
    bm.to_mesh(me)
    bm.free()
    # make it the active render UV map
    me.uv_layers["NanoUV"].active_render = True


def orig_uv_centroid(obj, mat_index):
    me = obj.data
    if not me.uv_layers or me.uv_layers.get("NanoUV") is me.uv_layers.active:
        pass
    src = me.uv_layers[0] if me.uv_layers else None
    if src is None:
        return None
    acc, cnt = np.zeros(2), 0
    for poly in me.polygons:
        if poly.material_index != mat_index:
            continue
        for li in poly.loop_indices:
            acc += np.array(src.data[li].uv)
            cnt += 1
        if cnt > 60:
            break
    return None if cnt == 0 else tuple(acc / cnt)


def lift(c):
    return tuple(min(1.0, ci * 0.6 + 0.55) for ci in c)


def rebuild_material(mat, sheet_key, tint, root, tag):
    px = load_sheet(root, sheet_key).copy()
    t = np.array(list(lift(tint)) + [1.0], dtype=np.float32)
    px *= t
    img = bpy.data.images.new(f"nano_{sheet_key}_{tag}", BAKE_RES, BAKE_RES, alpha=False)
    img.pixels.foreach_set(px.ravel())
    img.pack()
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.9
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    uvn = nt.nodes.new("ShaderNodeUVMap")
    uvn.uv_map = "NanoUV"
    nt.links.new(uvn.outputs["UV"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def process(root, glb):
    name = os.path.splitext(os.path.basename(glb))[0]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes:
        print("SKIP (no meshes):", glb)
        return
    dim = max(max(o.dimensions) for o in meshes)
    override_default = OVERRIDES.get(name, "")
    done = set()
    for o in meshes:
        # colour sampling must read the ORIGINAL uvs, so sample before box_uv
        samples = {}
        for i, slot in enumerate(o.material_slots):
            if slot.material is not None:
                samples[i] = orig_uv_centroid(o, i)
        box_uv(o, dim / TILES)
        for i, slot in enumerate(o.material_slots):
            mat = slot.material
            if mat is None or mat.name in done:
                continue
            done.add(mat.name)
            col = FORCE_TINT.get(name, mat_base_color(mat, samples.get(i)))
            key = classify(col, override_default)
            rebuild_material(mat, key, col, root, f"{name}_{len(done)}")
            print(f"  {name}/{mat.name}: rgb={tuple(round(c,2) for c in col)} -> {key}")
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", export_yup=True)
    print("BAKED:", glb)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    root = argv[0]
    for glb in argv[1:]:
        process(root, glb)
    print("NANO_WRAP_DONE")


main()
