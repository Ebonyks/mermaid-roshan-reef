#!/usr/bin/env python3
"""
survey_aquatic.py — orientation/size survey of the gen2 Meshy ocean-creature
scans vs the Riley pack models they will replace.

For each model: import, flatten transforms, print bbox dims, render side /
front / top views. Output feeds the per-creature config in build_swimmer_rig.py.

USAGE
    blender --background --python tools/survey_aquatic.py -- --out <render_dir>
"""
import bpy, sys, os, math
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default

OUT = os.path.abspath(arg("--out", "tools/out/aquatic_survey"))
os.makedirs(OUT, exist_ok=True)

REEF2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN2 = os.path.join(os.path.dirname(REEF2), "reef2_playground_audit", "gen2", "meshy")

MODELS = [
    ("clownfish", os.path.join(GEN2, "aquatic_clownfish_mv", "static.glb")),
    ("crab", os.path.join(GEN2, "aquatic_crab_mv2", "static.glb")),
    ("dolphin", os.path.join(GEN2, "aquatic_dolphin_mv", "static.glb")),
    ("hammerhead", os.path.join(GEN2, "aquatic_hammerhead_mv2", "static.glb")),
    ("lobster", os.path.join(GEN2, "aquatic_lobster_mv2", "static.glb")),
    ("octopus", os.path.join(GEN2, "aquatic_octopus_mv2", "static.glb")),
    ("penguin", os.path.join(GEN2, "aquatic_penguin_mv2", "static.glb")),
    ("shark", os.path.join(GEN2, "aquatic_shark_mv2", "static.glb")),
    ("squid", os.path.join(GEN2, "aquatic_squid_mv2", "static.glb")),
    ("stingray", os.path.join(GEN2, "aquatic_stingray_mv2", "static.glb")),
    ("turtle", os.path.join(GEN2, "aquatic_turtle_mv", "static.glb")),
    ("whale", os.path.join(GEN2, "aquatic_whale_mv2", "static.glb")),
    # Riley references (orientation + size the game is tuned for)
    ("REF_Shark", os.path.join(REEF2, "assets", "aquatic", "Shark.glb")),
    ("REF_Dolphin", os.path.join(REEF2, "assets", "aquatic", "Dolphin.glb")),
    ("REF_Turtle", os.path.join(REEF2, "assets", "aquatic", "Turtle.glb")),
    ("REF_StingRay", os.path.join(REEF2, "assets", "aquatic", "StingRay.glb")),
    ("REF_Crab", os.path.join(REEF2, "assets", "aquatic", "Crab.glb")),
    ("REF_ClownFish", os.path.join(REEF2, "assets", "aquatic", "ClownFish.glb")),
]

for name, path in MODELS:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    # flatten: bake world transforms into vertices (transform_apply no-ops headless)
    for mo in meshes:
        wm = mo.matrix_world.copy()
        mo.parent = None
        mo.matrix_world = Matrix.Identity(4)
        mo.data.transform(wm)
        mo.data.update()
    allv = [mo.matrix_world @ v.co for mo in meshes for v in mo.data.vertices]
    xs = sorted(v.x for v in allv); ys = sorted(v.y for v in allv); zs = sorted(v.z for v in allv)
    dims = (xs[-1] - xs[0], ys[-1] - ys[0], zs[-1] - zs[0])
    ctr = Vector(((xs[0] + xs[-1]) / 2, (ys[0] + ys[-1]) / 2, (zs[0] + zs[-1]) / 2))
    print(f"SURVEY {name}: dims X={dims[0]:.3f} Y={dims[1]:.3f} Z={dims[2]:.3f} "
          f"nmesh={len(meshes)} verts={sum(len(m.data.vertices) for m in meshes)}")
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "TEXTURE"
    scene.render.resolution_x, scene.render.resolution_y = 480, 400
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    bpy.context.collection.objects.link(cam)
    scene.camera = cam
    R = 2.2 * max(dims)
    def shoot(tag, loc):
        cam.location = ctr + Vector(loc)
        d = ctr - cam.location
        cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        scene.render.filepath = os.path.join(OUT, f"{name}_{tag}.png")
        bpy.ops.render.render(write_still=True)
    shoot("front", (0, -R, 0.25 * R))   # camera on -Y looking +Y
    shoot("side", (R, 0, 0.25 * R))     # camera on +X looking -X
    shoot("top", (0, -0.01 * R, R))
print("SURVEY DONE")
