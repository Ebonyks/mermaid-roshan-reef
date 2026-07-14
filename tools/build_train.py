#!/usr/bin/env python3
"""
build_train.py — Blender bootstrap for the Sky Lagoon courtyard train.

Companion to build_chuck_rig.py: the same measured-primitive, wireframe-QA
workflow, applied to the castle train instead of a scanned quadruped. The
consist (engine, tender, open-sided passenger coach, open-top gondola,
caboose with back balcony) is assembled here from the SAME dimensions the
game builds at runtime in scripts/arena/courtyard_train.gd, then rendered
from the canonical QA angles (side/front/top + three-quarter, solid and
wireframe-overlay) so any proportion change can be eyeballed before it
ships. Keep the two files' numbers in sync — this script is the authoring
reference and preview rig; the game constructs its own copy procedurally
(zero new assets) and only ever needs this when the proportions change.

Conventions (match the game):
  * +Y up, -Y forward in Blender — round-trips to Godot +Z, the game's
    facing convention (same as Chuck's nose).
  * Origin of every car = railhead centre at the bogie midpoint.
  * Units 1:1 with game units (Roshan is ~7 units tall).

USAGE
    blender --background --python tools/build_train.py -- \
        --blend tools/out/train.blend --renders tools/out/train_qa \
        [--glb tools/out/train_preview.glb]
"""
import bpy, sys, os, math

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

BLEND_OUT = os.path.abspath(arg("--blend", "tools/out/train.blend"))
RENDER_DIR = os.path.abspath(arg("--renders", "tools/out/train_qa"))
GLB_OUT = arg("--glb", "")
os.makedirs(os.path.dirname(BLEND_OUT), exist_ok=True)
os.makedirs(RENDER_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

# pastel toy palette (matches _train_mat colours in courtyard_train.gd)
TEAL = (0.35, 0.75, 0.78, 1.0)
NAVY = (0.22, 0.22, 0.40, 1.0)
GOLD = (0.95, 0.80, 0.40, 1.0)
LAV = (0.72, 0.65, 0.92, 1.0)
CREAM = (0.97, 0.93, 0.86, 1.0)
BUTTER = (0.98, 0.85, 0.45, 1.0)
CORAL = (0.95, 0.55, 0.55, 1.0)
ROOFP = (0.60, 0.55, 0.80, 1.0)
WHEEL = (0.24, 0.24, 0.42, 1.0)

def _obj(o, name, col, parent):
    o.name = name
    o.color = col
    if parent is not None:
        o.parent = parent
    return o

def box(name, pos, size, col, parent=None):
    # game space (x, y_up, z_fwd) -> Blender (x, -z_fwd, y_up)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(pos[0], -pos[2], pos[1]))
    o = bpy.context.active_object
    o.scale = (size[0], size[2], size[1])
    return _obj(o, name, col, parent)

def cyl(name, pos, r_top, r_bot, h, col, axis="Y", parent=None):
    # axis: "Y" = upright (Blender Z), "Z" = along travel, "X" = axle
    rot = {"Y": (0, 0, 0), "Z": (math.pi / 2, 0, 0), "X": (0, math.pi / 2, 0)}[axis]
    bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=r_bot, radius2=r_top, depth=h,
                                    location=(pos[0], -pos[2], pos[1]), rotation=rot)
    return _obj(bpy.context.active_object, name, col, parent)

def sph(name, pos, r, col, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=14, ring_count=8,
                                         location=(pos[0], -pos[2], pos[1]))
    return _obj(bpy.context.active_object, name, col, parent)

def car_root(name, z_world):
    e = bpy.data.objects.new(name, None)
    e.location = (0, -z_world, 0)
    bpy.context.collection.objects.link(e)
    return e

def chassis_and_wheels(root, length, col, axz, r):
    box("chassis", (0, 2.0, 0), (4.4, 0.7, length), col, root)
    for z in axz:
        for sx in (-1.0, 1.0):
            cyl("wheel", (sx * 2.4, r + 0.3, z), r, r, 0.5, WHEEL, "X", root)
            sph("pin", (sx * 2.7, r + 0.3 + r * 0.55, z), 0.22, GOLD, root)

# ---------------- the consist (dims mirror courtyard_train.gd) ----------------
eng = car_root("engine", 0.0)
chassis_and_wheels(eng, 9.0, NAVY, (-1.9, 0.2, 2.3), 1.3)
cyl("boiler", (0, 3.8, 1.4), 1.9, 1.9, 5.2, TEAL, "Z", eng)
cyl("smokebox", (0, 3.8, 4.2), 2.05, 2.05, 0.6, NAVY, "Z", eng)
sph("headlamp", (0, 3.8, 4.6), 0.55, GOLD, eng)
for bz in (0.0, 2.6):
    cyl("band", (0, 3.8, bz), 1.98, 1.98, 0.3, GOLD, "Z", eng)
cyl("funnel", (0, 6.4, 3.2), 1.0, 0.55, 1.7, NAVY, "Y", eng)
sph("dome", (0, 5.9, 0.8), 0.8, GOLD, eng)
box("cab", (0, 4.6, -2.9), (4.4, 3.8, 2.8), TEAL, eng)
box("cab_roof", (0, 6.75, -2.9), (5.0, 0.5, 3.4), NAVY, eng)
cow = cyl("cowcatcher", (0, 1.3, 5.1), 0.2, 2.1, 1.9, NAVY, "Z", eng)
cow.scale = (1.0, 1.0, 0.55)
for sx in (-1.0, 1.0):
    box("rod", (sx * 2.75, 2.3, 0.9), (0.22, 0.3, 5.2), GOLD, eng)

ten = car_root("tender", 9.5)
chassis_and_wheels(ten, 6.4, (0.30, 0.55, 0.60, 1.0), (-1.8, 1.8), 0.9)
box("tub", (0, 3.4, 0), (4.4, 2.2, 6.0), TEAL, ten)
for k in range(5):
    sph("coal", (k % 3 * 0.9 - 0.9, 4.7, k % 2 * 1.4 - 0.7), 0.75, (0.16, 0.15, 0.2, 1.0), ten)

coach = car_root("coach", 18.0)
chassis_and_wheels(coach, 8.8, LAV, (-2.6, 2.6), 0.9)
box("floor", (0, 2.5, 0), (4.6, 0.4, 8.4), CREAM, coach)
for sz in (-4.2, 4.2):
    box("endwall", (0, 5.6, sz), (4.6, 6.2, 0.4), LAV, coach)
for sx in (-1.0, 1.0):
    box("sidewall", (sx * 2.2, 3.4, 0), (0.35, 1.5, 8.4), LAV, coach)
    for pz in (-4.2, 0.0, 4.2):
        box("post", (sx * 2.2, 6.2, pz), (0.4, 5.0, 0.4), CREAM, coach)
box("roof", (0, 8.95, 0), (5.6, 0.5, 9.4), CORAL, coach)
box("bench", (0, 3.15, -1.2), (3.2, 0.55, 1.7), CORAL, coach)       # Roshan's seat
box("backrest", (0, 3.9, -1.95), (3.2, 1.5, 0.35), CORAL, coach)

gon = car_root("gondola", 27.3)
chassis_and_wheels(gon, 8.0, BUTTER, (-2.4, 2.4), 0.9)
box("floor", (0, 2.5, 0), (4.6, 0.4, 7.6), BUTTER, gon)
for sx in (-1.0, 1.0):
    box("wall", (sx * 2.25, 3.3, 0), (0.35, 1.4, 7.6), BUTTER, gon)
for sz in (-3.8, 3.8):
    box("wall", (0, 3.3, sz), (4.6, 1.4, 0.35), BUTTER, gon)
box("cushion", (0, 2.9, 0), (2.8, 0.6, 2.8), (0.95, 0.62, 0.78, 1.0), gon)

cab = car_root("caboose", 36.2)
chassis_and_wheels(cab, 8.0, CORAL, (-2.4, 2.4), 0.9)
box("deck", (0, 2.5, 0), (4.6, 0.4, 7.6), CREAM, cab)
box("house", (0, 4.2, 0.9), (4.2, 3.4, 4.8), CORAL, cab)
box("roof", (0, 6.15, 0.9), (5.0, 0.5, 5.6), ROOFP, cab)
box("cupola", (0, 6.9, 0.9), (2.2, 1.2, 1.9), CORAL, cab)
box("cupola_roof", (0, 7.7, 0.9), (2.8, 0.4, 2.5), ROOFP, cab)
for sx in (-1.0, 1.0):
    box("rail", (sx * 2.15, 3.2, -2.7), (0.3, 1.1, 2.2), CREAM, cab)
box("rail", (0, 3.2, -3.75), (4.6, 1.1, 0.3), CREAM, cab)

# a straight reference track slice under the consist (ballast + rails + ties)
box("ballast", (0, -0.45, -20.0), (5.4, 0.6, 52.0), (0.78, 0.68, 0.52, 1.0))
for sx in (-1.0, 1.0):
    box("railbar", (sx * 1.55, 0.15, -20.0), (0.34, 0.3, 52.0), (0.30, 0.28, 0.50, 1.0))
for k in range(13):
    box("tie", (0, -0.18, 4.0 - k * 4.0), (4.6, 0.2, 1.1), (0.50, 0.36, 0.22, 1.0))

# ---------------- QA renders (chuck-style workbench shots) ----------------
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "OBJECT"
scene.display.shading.show_object_outline = True   # the 'wireframe' read
scene.render.resolution_x, scene.render.resolution_y = 1200, 700
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
bpy.context.collection.objects.link(cam)
scene.camera = cam
CTR = (0, 20.0, 3.5)   # Blender coords: consist spans y 0..40 (game z 0..-40)

def shoot(fname, az_deg, el=0.35, r=58.0):
    from mathutils import Vector
    a = math.radians(az_deg)
    cam.location = Vector((math.sin(a) * r, CTR[1] - math.cos(a) * r, CTR[2] + el * r))
    d = Vector(CTR) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(RENDER_DIR, fname)
    bpy.ops.render.render(write_still=True)

shoot("train_side.png", 90)
shoot("train_front.png", 0, el=0.18, r=30.0)
shoot("train_top.png", 0, el=3.2)
shoot("train_three_quarter.png", 135, el=0.5)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print("SAVED", BLEND_OUT)
if GLB_OUT:
    bpy.ops.export_scene.gltf(filepath=os.path.abspath(GLB_OUT))
    print("EXPORTED", GLB_OUT)
