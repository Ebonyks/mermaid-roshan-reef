#!/usr/bin/env python3
"""Opera job 3D batch 1 — Pastry Chef mechanic-critical props.

Interprets the accepted flat cards in
assets_src/concepts/opera_jobs_flat_2026-07-21/ (vanilla/coral/plum layer,
bowl empty/stirring/calm, whisk, oven closed/open) into original chunky toy
3D per CLAUDE_OPERA_JOB_3D_CONTINUATION_2026-07-21.md: flat shared materials,
rounded primitives, registered state nodes, real hinge pivots, mobile budgets.

Run with the pip `bpy` module (Blender 5.x):  python3 build_opera_pastry_chef.py
Outputs GLBs to assets/opera/jobs/pastry_chef/, saves the .blend source, and
renders 0/45/135-degree QA views per family to assets_src/blender/qa_pastry_chef/.
"""
import bpy, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "assets/opera/jobs/pastry_chef")
QA = os.path.join(ROOT, "assets_src/blender/qa_pastry_chef")
os.makedirs(OUT, exist_ok=True)
os.makedirs(QA, exist_ok=True)

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

def doily_pedestal(parent):
    """Scalloped pink doily base with gold shell clasp — shared by all layers."""
    ped = empty("Doily", parent)
    cyl("DoilyTop", DOILY, ped, r=1.55, depth=0.22, loc=(0, 0, 0.11))
    for i in range(12):
        a = i / 12.0 * math.tau
        sph("Scallop%d" % i, DOILY, ped, r=0.34,
            loc=(math.cos(a) * 1.52, math.sin(a) * 1.52, 0.10), scale=(1, 1, 0.5), seg=10, rings=6)
    torus("DoilyRim", BRASS, ped, R=1.56, r=0.045, loc=(0, 0, 0.22))
    shell_clasp(ped, (0, -1.62, 0.12))
    return ped

def cake_layer(kind, m):
    """One chunky cake layer on its doily pedestal. Pivot at doily floor centre."""
    root = empty("OperaChef%s" % kind)
    vis = empty("Visual", root)
    doily_pedestal(vis)
    cyl("Cake", m, vis, r=1.18, depth=0.62, loc=(0, 0, 0.55))
    sph("CakeTop", m, vis, r=1.18, loc=(0, 0, 0.85), scale=(1, 1, 0.22))
    empty("TouchTarget", root, (0, 0, 0.6))
    empty("FXAnchor", root, (0, 0, 1.2))
    empty("PointerAnchor", root, (0, 0, 2.2))
    return root

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

def bowl():
    """The goal bowl: StateIdle (empty+whisk), StateActive (batter swirl),
    StateComplete (calm cream). All states registered to one shell."""
    root = empty("OperaChefBowl")
    vis = empty("Visual", root)
    body = empty("Shell", vis)
    obj(bpy.ops.mesh.primitive_cone_add, "BowlBody", CREAM, body,
        (0, 0, 1.15), (0, 0, 0), (1, 1, 1),
        radius1=1.35, radius2=2.15, depth=1.7, vertices=28)
    cyl("BowlFoot", CREAM, body, r=0.95, depth=0.35, loc=(0, 0, 0.18))
    torus("FootRim", BRASS, body, R=0.98, r=0.05, loc=(0, 0, 0.04))
    obj(bpy.ops.mesh.primitive_cone_add, "BowlBand", CORAL_L, body,
        (0, 0, 0.78), (0, 0, 0), (1, 1, 1),
        radius1=1.52, radius2=1.98, depth=0.62, vertices=28)
    torus("BowlRim", BRASS, body, R=2.13, r=0.08, loc=(0, 0, 2.0))
    cyl("InnerFloor", INNER, body, r=1.82, depth=0.06, loc=(0, 0, 1.30))
    shell_clasp(body, (0, -1.95, 1.0), s=1.5)
    st_i = empty("StateIdle", vis)
    cyl("EmptyFloor", INNER, st_i, r=1.80, depth=0.04, loc=(0, 0, 1.33))
    whisk(st_i, (0.9, 0, 1.55), rot=(0, math.radians(28), 0))
    st_a = empty("StateActive", vis)
    cyl("BatterTop", BATTER, st_a, r=1.95, depth=0.10, loc=(0, 0, 1.78))
    for i in range(3):
        torus("Swirl%d" % i, CREAMY, st_a, R=0.45 + i * 0.5, r=0.05,
              loc=(0, 0, 1.86), rot=(0, 0, i * 0.9), scale=(1, 0.8, 1))
    whisk(st_a, (0.55, 0.3, 1.9), rot=(0, math.radians(10), 0.4))
    st_c = empty("StateComplete", vis)
    sph("CreamDome", CREAMY, st_c, r=1.80, loc=(0, 0, 1.80), scale=(1, 1, 0.42))
    sph("CreamPeak", CREAMY, st_c, r=0.55, loc=(0, 0, 2.45), scale=(1, 1, 0.8))
    empty("TouchTarget", root, (0, 0, 1.6))
    empty("FXAnchor", root, (0, 0, 2.6))
    empty("PointerAnchor", root, (0, 0, 4.0))
    empty("AudioAnchor", root, (0, 0, 1.6))
    return root

def oven():
    """Scenic arched oven. Door hinged at its real bottom axis:
    StateIdle = closed, StateActive = open with warm glow + tray."""
    root = empty("OperaChefOven")
    vis = empty("Visual", root)
    body = empty("Shell", vis)
    box("Body", CREAM, body, size=(4.8, 3.0, 4.6), loc=(0, 0, 2.3))
    # flat arched pediment, not a drum: squashed half-cylinder crown
    ped = cyl("Pediment", CORAL_L, body, r=1.7, depth=2.9,
              loc=(0, 0, 4.6), rot=(math.pi / 2, 0, 0), verts=32)
    ped.scale = (1.0, 0.5, 1.0)   # local Y after the X-rotation is world Z: flatten the arch
    shell_clasp(body, (0, -1.5, 5.15), s=1.5)
    for sx in (-2.05, 2.05):
        cyl("Column", CORAL, body, r=0.42, depth=4.4, loc=(sx, -1.45, 2.2))
        sph("ColumnCap", BRASS, body, r=0.5, loc=(sx, -1.45, 4.5), scale=(1, 1, 0.5))
        cyl("ColumnBase", BRASS, body, r=0.5, depth=0.25, loc=(sx, -1.45, 0.12))
    st_i = empty("StateIdle", vis)
    door_c = empty("DoorClosedHinge", st_i, (0, -1.55, 0.7))   # real bottom hinge
    box("DoorFrame", BRASS, door_c, size=(2.7, 0.18, 3.0), loc=(0, 0, 1.5))
    box("DoorGlass", NAVYGL, door_c, size=(2.0, 0.2, 2.3), loc=(0, 0, 1.55))
    st_a = empty("StateActive", vis)
    box("CavityGlow", GLOW, st_a, size=(2.1, 0.3, 2.2), loc=(0, -1.42, 2.0))
    door_o = empty("DoorOpenHinge", st_a, (0, -1.55, 0.7))
    door_o.rotation_euler = (math.radians(-96), 0, 0)
    box("DoorFrameO", BRASS, door_o, size=(2.7, 0.18, 3.0), loc=(0, 0, 1.5))
    box("DoorGlassO", NAVYGL, door_o, size=(2.0, 0.2, 2.3), loc=(0, 0, 1.55))
    box("Tray", BRASS, st_a, size=(1.9, 1.3, 0.14), loc=(0, -2.3, 1.05))
    empty("FXAnchor", root, (0, -1.5, 2.2))
    return root

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

# ---------------- build the family --------------------------------------
total = 0
layers = [("LayerVanilla", VANILLA, "opera_pastry_chef_layer_vanilla.glb"),
          ("LayerCoral", CORAL, "opera_pastry_chef_layer_coral.glb"),
          ("LayerPlum", PLUM, "opera_pastry_chef_layer_plum.glb")]
built = []
for i, (kind, m, fname) in enumerate(layers):
    r = cake_layer(kind, m)
    r.location = ((i - 1) * 4.5, 0, 0)
    total += export_glb(r, fname)
    built.append(r)
b = bowl()
b.location = (0, 7.5, 0)
total += export_glb(b, "opera_pastry_chef_bowl.glb")
built.append(b)
ov = oven()
ov.location = (0, 15, 0)
total += export_glb(ov, "opera_pastry_chef_oven.glb")
built.append(ov)
print("TOTAL tris:", total)

qa_render(built[:3], "layers")
def solo_state(bowl_root, keep):
    for c in bowl_root.children:
        if c.name.split(".")[0] == "Visual":
            for s in c.children:
                base = s.name.split(".")[0]
                if base.startswith("State"):
                    hide = base != keep
                    def st(o, h):
                        o.hide_render = h
                        for cc in o.children:
                            st(cc, h)
                    st(s, hide)
for state in ("StateIdle", "StateActive", "StateComplete"):
    solo_state(b, state)
    qa_render([b], "bowl_" + state.lower())
solo_state(b, "StateIdle")
def oven_state(keep):
    solo_state(ov, keep)
oven_state("StateIdle")
qa_render([ov], "oven_closed")
oven_state("StateActive")
qa_render([ov], "oven_open")
oven_state("StateIdle")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets_src/blender/opera_pastry_chef_2026-07-22.blend"))
print("DONE")
