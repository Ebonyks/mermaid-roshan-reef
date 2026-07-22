#!/usr/bin/env python3
"""Shared helpers for the opera job 3D batches (materials, primitives,
join/flatten, GLB export, QA renders). Import from per-job build scripts."""
import bpy, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = None  # set by the job script
QA = None   # set by the job script

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------- shared toy material library (flat, rough, no textures) ----
MATS = {}
def srgb(c):
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)

def mat(name, rgb, emission=0.0, alpha=1.0):
    rgb = srgb(rgb)
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new("Opera_" + name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if emission > 0:
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        m.blend_method = 'BLEND'
    MATS[name] = m
    return m

CREAM   = mat("cream",   (0.93, 0.87, 0.78))
CORAL   = mat("coral",   (0.86, 0.42, 0.38))
CORAL_L = mat("coral_l", (0.93, 0.60, 0.55))
PLUM    = mat("plum",    (0.55, 0.36, 0.66))
VANILLA = mat("vanilla", (0.94, 0.80, 0.52))
BRASS   = mat("brass",   (0.83, 0.64, 0.30))
PEARL   = mat("pearl",   (0.96, 0.93, 0.95), emission=0.15)
DOILY   = mat("doily",   (0.93, 0.70, 0.73))
BATTER  = mat("batter",  (0.90, 0.55, 0.50))
CREAMY  = mat("creamy",  (0.95, 0.90, 0.78))
SILVER  = mat("silver",  (0.80, 0.82, 0.86))
NAVYGL  = mat("navy_glass", (0.13, 0.12, 0.25))
GLOW    = mat("oven_glow", (1.0, 0.62, 0.25), emission=2.0)
INNER   = mat("bowl_inner", (0.80, 0.72, 0.62))

def obj(mesh_op, name, material, parent, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), **kw):
    mesh_op(**kw)
    o = bpy.context.active_object
    o.name = name
    o.location = loc
    o.rotation_euler = rot
    o.scale = scale
    if material:
        o.data.materials.append(material)
    o.parent = parent
    for p in o.data.polygons:
        p.use_smooth = True
    return o

def empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    e.parent = parent
    bpy.context.scene.collection.objects.link(e)
    return e

def cyl(name, m, parent, r=1, depth=1, loc=(0,0,0), rot=(0,0,0), scale=(1,1,1), verts=24):
    return obj(bpy.ops.mesh.primitive_cylinder_add, name, m, parent,
               loc, rot, scale, radius=r, depth=depth, vertices=verts)

def sph(name, m, parent, r=1, loc=(0,0,0), scale=(1,1,1), seg=14, rings=8):
    return obj(bpy.ops.mesh.primitive_uv_sphere_add, name, m, parent,
               loc, (0,0,0), scale, radius=r, segments=seg, ring_count=rings)

def box(name, m, parent, size=(1,1,1), loc=(0,0,0), rot=(0,0,0)):
    o = obj(bpy.ops.mesh.primitive_cube_add, name, m, parent, loc, rot, (1,1,1), size=1)
    o.scale = (size[0]/2, size[1]/2, size[2]/2)
    return o

def torus(name, m, parent, R=1, r=0.2, loc=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
    return obj(bpy.ops.mesh.primitive_torus_add, name, m, parent, loc, rot, scale,
               major_radius=R, minor_radius=r, major_segments=20, minor_segments=8)

def shell_clasp(parent, loc, s=1.0):
    """Gold scallop shell + pearl, the family signature front detail."""
    base = empty("ShellClasp", parent, loc)
    for i in range(5):
        a = math.radians(-40 + i * 20)
        sph("ShellRib%d" % i, BRASS, base, r=0.16 * s,
            loc=(math.sin(a) * 0.22 * s, 0.02, 0.16 * s + math.cos(a) * 0.16 * s),
            scale=(0.8, 0.45, 1.5), seg=10, rings=6)
    sph("Pearl", PEARL, base, r=0.11 * s, loc=(0, -0.06 * s, 0.02))
    return base

def whisk(parent, loc, rot=(0, 0, 0)):
    w = empty("Whisk", parent, loc)
    w.rotation_euler = rot
    cyl("Handle", CORAL, w, r=0.10, depth=0.95, loc=(0, 0, 1.45))
    sph("HandleCap", BRASS, w, r=0.13, loc=(0, 0, 1.95))
    cyl("Ferrule", BRASS, w, r=0.12, depth=0.18, loc=(0, 0, 0.96))
    for i in range(3):
        a = i / 3.0 * math.pi
        torus("Loop%d" % i, SILVER, w, R=0.46, r=0.035,
              loc=(0, 0, 0.45), rot=(math.pi / 2, 0, a), scale=(1, 1.5, 1))
    return w

def join_group(parent):
    """Join every mesh descendant of `parent` that is not under a nested
    State*/Door* pivot into ONE multi-material mesh — node count and draw
    calls drop to one per group, which the act's mobile node budget needs."""
    def gather(o, out):
        for c in list(o.children):
            base = c.name.split(".")[0]
            if c.type == 'EMPTY' and (base.startswith("State") or base.startswith("Door")):
                continue
            if c.type == 'MESH':
                out.append(c)
            gather(c, out)
    meshes = []
    gather(parent, meshes)
    if len(meshes) < 2:
        return
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    # freeze each part's world transform into the joined mesh
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.parent = parent
    joined.name = parent.name.split(".")[0] + "Mesh"

def flatten_for_export(root):
    """Collapse static groups so each GLB is a handful of nodes."""
    for c in list(root.children):
        base = c.name.split(".")[0]
        if base == "Visual":
            join_group(c)                       # static shell of the visual
            for s in list(c.children):
                sbase = s.name.split(".")[0]
                if sbase.startswith("State"):
                    for d in list(s.children):
                        if d.type == 'EMPTY' and d.name.split(".")[0].startswith("Door"):
                            join_group(d)       # hinged door: one mesh under its pivot
                    join_group(s)               # rest of the state joins to one mesh

def export_glb(root, fname):
    flatten_for_export(root)
    bpy.ops.object.select_all(action='DESELECT')
    def walk(o):
        o.select_set(True)
        for c in o.children:
            walk(c)
    walk(root)
    bpy.context.view_layer.objects.active = root
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, fname),
                              use_selection=True, export_format='GLB',
                              export_yup=True, export_apply=True)
    tris = 0
    def count(o):
        nonlocal tris
        if o.type == 'MESH':
            tris += sum(len(p.vertices) - 2 for p in o.data.polygons)
        for c in o.children:
            count(c)
    count(root)
    print("EXPORT %-44s %6d tris" % (fname, tris))
    return tris

def qa_render(roots, tag):
    """0/45/135-degree turntable QA against the neutral navy card."""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    world = bpy.data.worlds.new("Navy") if scene.world is None else scene.world
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.09, 0.075, 0.18, 1)
    bg.inputs[1].default_value = 1.0
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", 'SUN'))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    scene.collection.objects.link(sun)
    cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    scene.collection.objects.link(cam)
    scene.camera = cam
    def set_tree(o, hide):
        o.hide_render = hide
        for c in o.children:
            set_tree(c, hide)
    all_roots = [o for o in bpy.data.objects if o.type == 'EMPTY' and o.parent is None]
    hidden = [r for r in all_roots if r not in roots]
    for r in hidden:
        set_tree(r, True)
    import mathutils
    cx = sum(r.location.x for r in roots) / len(roots)
    cy = sum(r.location.y for r in roots) / len(roots)
    top = 0.0
    def top_of(o):
        nonlocal top
        if o.type == 'MESH':
            for v in o.bound_box:
                wz = (o.matrix_world @ mathutils.Vector(v)).z
                top = max(top, wz)
        for c in o.children:
            top_of(c)
    bpy.context.view_layer.update()
    for r in roots:
        top_of(r)
    dist = 8.0 + 3.0 * len(roots) + top * 1.4
    aim_z = max(1.5, top * 0.45)
    for angle in (0, 45, 135):
        a = math.radians(angle)
        cam.location = (cx + math.sin(a) * dist, cy - math.cos(a) * dist, dist * 0.5)
        direction = mathutils.Vector((cx, cy, aim_z)) - cam.location
        cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = os.path.join(QA, "%s_%03d.png" % (tag, angle))
        bpy.ops.render.render(write_still=True)
    for r in hidden:
        set_tree(r, False)
    bpy.data.objects.remove(sun)
    bpy.data.objects.remove(cam)

