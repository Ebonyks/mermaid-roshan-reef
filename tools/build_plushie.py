#!/usr/bin/env python3
"""build_huluu.py — give Princess Huluu the 'mermaid Roshan treatment'.

Builds a double-sided PLUSHIE mesh by extruding her illustration's silhouette
(art textured on both sides, puffed with a solidify pass), rigged with the SAME
bone names as Roshan's proven rig (spine1/chest/neck/head, hair1-3, tail1..8)
so player.gd's procedural swim drives her with zero new animation code.

    blender --background --python tools/build_huluu.py
"""
import bpy, os, sys
from mathutils import Vector

def _arg(flag, default):
    argv = sys.argv
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        if flag in rest and rest.index(flag) + 1 < len(rest):
            return rest[rest.index(flag) + 1]
    return default

SRC = os.path.abspath(_arg("--src", "assets/characters/friends/huluu.png"))
OUT = os.path.abspath(_arg("--out", "assets/characters/huluu.glb"))
# GRID 96 gave visible stair-steps on thin details (fairy wings read as
# pixel-art blocks in-game); 192 halves the step size twice over. COV is the
# alpha coverage needed to keep a cell — looser than the old 0.70 so slim
# wing/fin strips survive; the CLIP alpha still trims edges to the art.
GRID = int(_arg("--grid", "192"))
COV = float(_arg("--cov", "0.55"))
THICK = 0.16              # plushie puff (metres, model is ~1.8 tall pre-scale)

bpy.ops.wm.read_factory_settings(use_empty=True)
img = bpy.data.images.load(SRC)
iw, ih = img.size
aspect = iw / ih
H = 1.8                   # model height in metres
W = H * aspect
px = list(img.pixels)     # RGBA flat

def alpha_at(u, v):
    x = min(iw - 1, max(0, int(u * iw)))
    y = min(ih - 1, max(0, int(v * ih)))
    return px[(y * iw + x) * 4 + 3]

# ---- silhouette grid mesh (XZ plane, Z-up; v=0 is image bottom) ----
verts, faces, uvs = [], [], []
vid = {}
def vert(i, j):
    key = (i, j)
    if key not in vid:
        u, v = i / GRID, j / GRID
        vid[key] = len(verts)
        verts.append((u * W - W / 2, 0.0, v * H))
    return vid[key]

for j in range(GRID):
    for i in range(GRID):
        # keep the cell if the art has decent alpha coverage at its centre
        u, v = (i + 0.5) / GRID, (j + 0.5) / GRID
        cov = sum(alpha_at(u + du, v + dv) for du in (-0.4 / GRID, 0.4 / GRID) for dv in (-0.4 / GRID, 0.4 / GRID)) / 4.0
        if cov < COV:
            continue
        faces.append((vert(i, j), vert(i + 1, j), vert(i + 1, j + 1), vert(i, j + 1)))

me = bpy.data.meshes.new("huluu")
me.from_pydata(verts, [], faces)
me.update()
obj = bpy.data.objects.new("huluu", me)
bpy.context.collection.objects.link(obj)

# UVs = planar map straight from vertex position
uvl = me.uv_layers.new(name="UVMap")
for poly in me.polygons:
    for li in poly.loop_indices:
        vco = me.vertices[me.loops[li].vertex_index].co
        uvl.data[li].uv = ((vco.x + W / 2) / W, vco.z / H)

# puff it: solidify + smooth = stuffed-toy volume, art on BOTH sides
sol = obj.modifiers.new("Solidify", "SOLIDIFY")
sol.thickness = THICK
sol.offset = 0.0
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_apply(modifier="Solidify")
for p in me.polygons:
    p.use_smooth = True

# fabric material, texture on both faces
mat = bpy.data.materials.new("huluu_mat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
tex.image = img
mat.node_tree.links.new(bsdf.inputs["Base Color"], tex.outputs["Color"])
mat.node_tree.links.new(bsdf.inputs["Alpha"], tex.outputs["Alpha"])
mat.blend_method = "CLIP"
bsdf.inputs["Roughness"].default_value = 0.85
mat.use_backface_culling = False
obj.data.materials.append(mat)
# rim faces (the solidify walls) get a solid FABRIC SEAM material — their UVs
# would otherwise smear the dark outline texels into comb-teeth streaks
mat2 = bpy.data.materials.new("huluu_seam")
mat2.use_nodes = True
b2 = mat2.node_tree.nodes["Principled BSDF"]
b2.inputs["Base Color"].default_value = (0.94, 0.62, 0.72, 1.0)   # warm plush pink
b2.inputs["Roughness"].default_value = 0.95
obj.data.materials.append(mat2)
for p in me.polygons:
    if abs(p.normal.y) < 0.5:
        p.material_index = 1

# ---- armature: Roshan-compatible bone names ----
arm_data = bpy.data.armatures.new("huluu_rig")
arm = bpy.data.objects.new("huluu_rig", arm_data)
bpy.context.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm_data.edit_bones

def bone(name, head, tail, parent=None):
    b = eb.new(name)
    b.head = Vector(head)
    b.tail = Vector(tail)
    if parent:
        b.parent = eb[parent]
    return b

# torso up the top half, tail chain down the bottom half (image bottom = tail tip)
bone("root",   (0, 0, 0.95), (0, 0, 1.05))
bone("spine1", (0, 0, 0.95), (0, 0, 1.15), "root")
bone("chest",  (0, 0, 1.15), (0, 0, 1.35), "spine1")
bone("neck",   (0, 0, 1.35), (0, 0, 1.45), "chest")
bone("head",   (0, 0, 1.45), (0, 0, 1.75), "neck")
for k in range(3):
    bone("hair%d" % (k + 1), (0.10 + 0.05 * k, 0, 1.62 - 0.1 * k), (0.16 + 0.05 * k, 0, 1.5 - 0.12 * k), "head")
prev = "root"
for k in range(8):
    z0 = 0.95 - 0.115 * k
    bone("tail%d" % (k + 1), (0, 0, z0), (0, 0, z0 - 0.115), prev)
    prev = "tail%d" % (k + 1)
bpy.ops.object.mode_set(mode="OBJECT")

# bind with automatic weights
bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB")
print("[ok] wrote", OUT)
