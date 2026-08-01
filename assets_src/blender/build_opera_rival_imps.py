"""Build the twelve Pearl Opera House career-rival imp variants.

The base Mischief Imp is project-owned art.  These variants keep that mesh
unchanged and add a very small, mobile-friendly set of plain toy costume
pieces.  The imp family intentionally uses no shell, pearl, ocean-emblem,
badge, or medallion motif; profession reads through silhouette and tools.
Every output is a new GLB; the protected source and the existing dungeon GLB
are never modified.

Run from the repository root:
    blender --background --factory-startup \
        --python assets_src/blender/build_opera_rival_imps.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector


REPO = Path(bpy.path.abspath("//")).resolve()
if not (REPO / "project.godot").exists():
    REPO = Path.cwd().resolve()

BASE_IMP = REPO / "assets" / "dungeon" / "mischief_imp.glb"
OUT_DIR = REPO / "assets" / "opera" / "rivals"
QA_DIR = REPO / "assets_src" / "blender" / "qa_opera_rivals"

CAREERS = (
    "chef",
    "detective",
    "ballerina",
    "candymaker",
    "doctor",
    "farmer",
    "boxer",
    "magician",
    "painter",
    "astronaut",
    "racer",
    "popstar",
)

PLUM = (0.30, 0.20, 0.42, 1.0)
DEEP_PLUM = (0.18, 0.10, 0.30, 1.0)
CORAL = (0.94, 0.33, 0.38, 1.0)
ROSE = (0.96, 0.52, 0.66, 1.0)
TEAL = (0.28, 0.72, 0.72, 1.0)
SKY = (0.48, 0.80, 0.96, 1.0)
GOLD = (1.0, 0.76, 0.24, 1.0)
CREAM = (0.98, 0.94, 0.84, 1.0)
WHITE = (0.98, 0.98, 1.0, 1.0)
BROWN = (0.48, 0.28, 0.16, 1.0)
GREEN = (0.36, 0.72, 0.34, 1.0)
BLUE = (0.26, 0.46, 0.88, 1.0)
SILVER = (0.72, 0.78, 0.88, 1.0)
BLACK = (0.06, 0.05, 0.10, 1.0)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.cameras,
        bpy.data.lights,
    ):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def material(name: str, rgba: tuple[float, float, float, float], glow: float = 0.0) -> bpy.types.Material:
    mat = bpy.data.materials.get(name)
    if mat is not None:
        return mat
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = rgba
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = 0.74
    if rgba[3] < 1.0:
        bsdf.inputs["Alpha"].default_value = rgba[3]
        bsdf.inputs["Transmission Weight"].default_value = 0.08
        mat.surface_render_method = "DITHERED"
    if glow > 0.0:
        bsdf.inputs["Emission Color"].default_value = rgba
        bsdf.inputs["Emission Strength"].default_value = glow
    return mat


def finish_object(obj: bpy.types.Object, name: str, mat: bpy.types.Material, root: bpy.types.Object) -> bpy.types.Object:
    obj.name = name
    obj.data.materials.append(mat)
    obj.parent = root
    return obj


def sphere(
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    mat: bpy.types.Material,
    root: bpy.types.Object,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=loc)
    obj = bpy.context.object
    obj.scale = scale
    return finish_object(obj, name, mat, root)


def cube(
    name: str,
    loc: tuple[float, float, float],
    scale: tuple[float, float, float],
    mat: bpy.types.Material,
    root: bpy.types.Object,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.object
    obj.scale = scale
    return finish_object(obj, name, mat, root)


def cylinder(
    name: str,
    loc: tuple[float, float, float],
    radius: float,
    depth: float,
    mat: bpy.types.Material,
    root: bpy.types.Object,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
    vertices: int = 16,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    return finish_object(bpy.context.object, name, mat, root)


def cone(
    name: str,
    loc: tuple[float, float, float],
    r1: float,
    r2: float,
    depth: float,
    mat: bpy.types.Material,
    root: bpy.types.Object,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(
        vertices=16,
        radius1=r1,
        radius2=r2,
        depth=depth,
        location=loc,
        rotation=rot,
    )
    return finish_object(bpy.context.object, name, mat, root)


def torus(
    name: str,
    loc: tuple[float, float, float],
    major: float,
    minor: float,
    mat: bpy.types.Material,
    root: bpy.types.Object,
    rot: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=16,
        minor_segments=6,
        location=loc,
        rotation=rot,
    )
    return finish_object(bpy.context.object, name, mat, root)


def add_hat(root: bpy.types.Object, crown: tuple[float, float, float, float], tall: bool = False) -> None:
    brim = material("RivalHatBrim", crown)
    cylinder("RivalHatBrim", (0.0, 0.0, 4.10), 1.48 if tall else 1.34, 0.18, brim, root)
    cylinder("RivalHatCrown", (0.0, 0.0, 4.75 if tall else 4.45), 0.86, 1.35 if tall else 0.72, brim, root)


def add_hand_prop(
    root: bpy.types.Object,
    name: str,
    x: float,
    col: tuple[float, float, float, float] | bpy.types.Material,
    long: bool = True,
) -> None:
    mat = col if isinstance(col, bpy.types.Material) else material(name, col)
    if long:
        cylinder(name, (x, -0.65, 1.75), 0.12, 1.75, mat, root, (math.pi / 2.0, 0.0, 0.0), 10)
    else:
        sphere(name, (x, -0.68, 1.75), (0.42, 0.26, 0.42), mat, root)


def dress(root: bpy.types.Object, career: str) -> None:
    cream = material("RivalCream", CREAM)
    white = material("RivalWhite", WHITE)
    gold = material("RivalGold", GOLD, 0.08)
    coral = material("RivalCoral", CORAL)
    rose = material("RivalRose", ROSE)
    teal = material("RivalTeal", TEAL)
    sky = material("RivalSky", SKY)
    plum = material("RivalPlum", PLUM)
    deep_plum = material("RivalDeepPlum", DEEP_PLUM)
    brown = material("RivalBrown", BROWN)
    green = material("RivalGreen", GREEN)
    blue = material("RivalBlue", BLUE)
    silver = material("RivalSilver", SILVER)
    black = material("RivalBlack", BLACK)

    if career == "chef":
        cylinder("ChefToqueBand", (0.0, 0.0, 4.15), 1.12, 0.42, cream, root)
        for i, x in enumerate((-0.72, 0.0, 0.72)):
            sphere(f"ChefToquePuff{i}", (x, 0.0, 4.78), (0.72, 0.58, 0.68), white, root)
        cube("ChefNeckerchief", (0.0, -1.55, 2.48), (0.42, 0.18, 0.42), coral, root, (0.0, math.pi / 4.0, 0.0))
        add_hand_prop(root, "ChefWhisk", 3.05, silver)
    elif career == "detective":
        cylinder("DetectiveHatBrim", (0.0, 0.0, 4.08), 1.45, 0.20, brown, root)
        sphere("DetectiveHatCrown", (0.0, 0.0, 4.48), (1.05, 0.78, 0.52), brown, root)
        cylinder("DetectiveHatBand", (0.0, 0.0, 4.36), 1.08, 0.16, gold, root)
        torus("DetectiveLens", (3.0, -0.72, 1.95), 0.48, 0.10, gold, root, (math.pi / 2.0, 0.0, 0.0))
        cylinder("DetectiveLensHandle", (3.0, -0.48, 1.20), 0.10, 1.15, brown, root, (0.0, 0.0, 0.0), 10)
    elif career == "ballerina":
        torus("BallerinaTutu", (0.0, 0.0, 1.55), 1.44, 0.36, rose, root)
        sphere("BallerinaBowL", (-0.42, -0.10, 4.25), (0.48, 0.18, 0.34), rose, root)
        sphere("BallerinaBowR", (0.42, -0.10, 4.25), (0.48, 0.18, 0.34), rose, root)
        sphere("BallerinaBowKnot", (0.0, -0.18, 4.25), (0.24, 0.20, 0.24), gold, root)
    elif career == "candymaker":
        for i, z in enumerate((4.12, 4.62, 5.12)):
            cylinder(f"CandyHatTier{i}", (0.0, 0.0, z), 1.12 - float(i) * 0.18, 0.44, rose if i % 2 == 0 else cream, root)
        cylinder("CandyStick", (3.0, -0.55, 1.30), 0.10, 1.7, cream, root)
        sphere("CandyLollipop", (3.0, -0.55, 2.25), (0.62, 0.25, 0.62), coral, root)
    elif career == "doctor":
        torus("DoctorMirror", (0.0, -0.58, 4.25), 0.62, 0.13, silver, root, (math.pi / 2.0, 0.0, 0.0))
        sphere("DoctorMirrorLamp", (0.0, -0.72, 4.25), (0.18, 0.12, 0.18), gold, root)
        torus("DoctorScope", (0.0, -1.40, 2.30), 0.74, 0.10, blue, root, (math.pi / 2.0, 0.0, 0.0))
        sphere("DoctorScopeBell", (0.0, -1.55, 1.65), (0.24, 0.12, 0.24), silver, root)
    elif career == "farmer":
        cylinder("FarmerHatBrim", (0.0, 0.0, 4.10), 1.62, 0.18, gold, root)
        cylinder("FarmerHatCrown", (0.0, 0.0, 4.53), 0.92, 0.68, gold, root)
        cylinder("FarmerHatBand", (0.0, 0.0, 4.31), 0.96, 0.15, green, root)
        cone("FarmerCarrot", (3.0, -0.62, 1.55), 0.36, 0.04, 1.30, coral, root)
        sphere("FarmerCarrotTop", (3.0, -0.62, 2.25), (0.36, 0.22, 0.36), green, root)
    elif career == "boxer":
        sphere("BoxerGloveL", (-3.05, -0.55, 1.78), (0.72, 0.55, 0.68), teal, root)
        sphere("BoxerGloveR", (3.05, -0.55, 1.78), (0.72, 0.55, 0.68), teal, root)
        cylinder("BoxerHeadguard", (0.0, 0.0, 4.02), 1.16, 0.52, coral, root)
        cube("BoxerBelt", (0.0, -1.42, 1.10), (1.18, 0.16, 0.24), gold, root)
    elif career == "magician":
        add_hat(root, DEEP_PLUM, True)
        cylinder("MagicianHatBand", (0.0, 0.0, 4.35), 0.91, 0.18, gold, root)
        add_hand_prop(root, "MagicianWand", 3.05, WHITE)
        sphere("MagicianWandTip", (3.05, -1.48, 1.75), (0.28, 0.18, 0.28), gold, root)
        cone("MagicianCape", (0.0, 1.15, 1.90), 1.65, 0.72, 2.85, plum, root, (0.0, 0.0, math.pi))
    elif career == "painter":
        sphere("PainterBeret", (0.20, 0.0, 4.27), (1.20, 0.82, 0.32), blue, root)
        sphere("PainterBeretButton", (0.20, 0.0, 4.58), (0.16, 0.16, 0.18), gold, root)
        add_hand_prop(root, "PainterBrush", 3.02, brown)
        cone("PainterBrushTip", (3.02, -1.58, 1.75), 0.24, 0.04, 0.58, rose, root, (math.pi / 2.0, 0.0, 0.0))
        sphere("PainterPalette", (-3.0, -0.62, 1.70), (0.72, 0.22, 0.56), cream, root)
    elif career == "astronaut":
        helmet = sphere("AstronautHelmet", (0.0, 0.0, 3.55), (1.48, 1.28, 1.48), material("RivalGlass", (0.65, 0.88, 1.0, 0.32)), root)
        helmet.data.materials.clear()
        helmet.data.materials.append(material("RivalGlass", (0.65, 0.88, 1.0, 0.32)))
        torus("AstronautCollar", (0.0, 0.0, 2.65), 1.25, 0.22, silver, root)
        cylinder("AstronautTankL", (-0.55, 1.10, 1.85), 0.35, 1.75, silver, root)
        cylinder("AstronautTankR", (0.55, 1.10, 1.85), 0.35, 1.75, silver, root)
        sphere("AstronautStatusLight", (0.0, -1.55, 1.75), (0.36, 0.16, 0.36), gold, root)
    elif career == "racer":
        sphere("RacerHelmet", (0.0, 0.0, 3.75), (1.28, 1.12, 1.15), coral, root)
        cube("RacerVisor", (0.0, -1.16, 3.68), (0.82, 0.16, 0.30), sky, root)
        torus("RacerWheel", (3.0, -0.62, 1.70), 0.58, 0.14, black, root, (math.pi / 2.0, 0.0, 0.0))
        sphere("RacerHelmetStar", (0.0, -1.12, 4.35), (0.25, 0.12, 0.25), gold, root)
    elif career == "popstar":
        sphere("PopGlassesL", (-0.55, -1.22, 3.48), (0.48, 0.14, 0.36), gold, root)
        sphere("PopGlassesR", (0.55, -1.22, 3.48), (0.48, 0.14, 0.36), gold, root)
        cube("PopGlassesBridge", (0.0, -1.23, 3.48), (0.18, 0.10, 0.08), gold, root)
        cylinder("PopMicHandle", (3.0, -0.58, 1.35), 0.13, 1.25, silver, root)
        sphere("PopMicHead", (3.0, -0.58, 2.10), (0.38, 0.28, 0.38), rose, root)
        torus("PopCollar", (0.0, -0.05, 2.45), 1.05, 0.14, teal, root)


def import_base() -> bpy.types.Object:
    bpy.ops.import_scene.gltf(filepath=str(BASE_IMP))
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    base = max(meshes, key=lambda obj: len(obj.data.vertices))
    for obj in list(bpy.context.scene.objects):
        if obj is base:
            continue
        bpy.data.objects.remove(obj, do_unlink=True)
    base.name = "RivalImpBody"
    root = bpy.data.objects.new("OperaRival", None)
    bpy.context.scene.collection.objects.link(root)
    base.parent = root
    return root


def select_hierarchy(root: bpy.types.Object) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    root.select_set(True)
    for obj in root.children_recursive:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = root


def export_glb(root: bpy.types.Object, career: str) -> None:
    select_hierarchy(root)
    out = OUT_DIR / f"opera_rival_{career}.glb"
    bpy.ops.export_scene.gltf(
        filepath=str(out),
        export_format="GLB",
        use_selection=True,
        export_cameras=False,
        export_lights=False,
        export_apply=True,
    )


def aim(obj: bpy.types.Object, point: tuple[float, float, float]) -> None:
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def render_qa(career: str, transparent: bool = False) -> None:
    world = bpy.context.scene.world
    world.color = (0.04, 0.025, 0.08)
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.07, 0.04, 0.12, 1.0)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55

    bpy.ops.object.light_add(type="AREA", location=(4.5, -5.0, 7.5))
    key = bpy.context.object
    key.data.energy = 850.0
    key.data.shape = "DISK"
    key.data.size = 5.0
    aim(key, (0.0, 0.0, 2.3))
    bpy.ops.object.light_add(type="AREA", location=(-4.0, -1.0, 4.0))
    fill = bpy.context.object
    fill.data.energy = 500.0
    fill.data.color = (0.45, 0.78, 1.0)
    fill.data.size = 4.0
    aim(fill, (0.0, 0.0, 2.1))

    if not transparent:
        bpy.ops.mesh.primitive_plane_add(size=22.0, location=(0.0, 0.0, -0.58))
        plane = bpy.context.object
        plane.data.materials.append(material("QAFloor", (0.20, 0.13, 0.30, 1.0)))

    bpy.ops.object.camera_add(location=(8.4, -10.5, 6.8))
    cam = bpy.context.object
    cam.data.lens = 58.0
    aim(cam, (0.0, 0.0, 2.25))
    bpy.context.scene.camera = cam

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = transparent
    scene.render.filepath = str(
        OUT_DIR / "opera_rival_racer_portrait.png"
        if transparent
        else QA_DIR / f"opera_rival_{career}_qa.png"
    )
    bpy.ops.render.render(write_still=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    for career in CAREERS:
        clear_scene()
        root = import_base()
        dress(root, career)
        export_glb(root, career)
        render_qa(career)
        if career == "racer":
            clear_scene()
            root = import_base()
            dress(root, career)
            render_qa(career, transparent=True)
        print(f"BUILT opera rival: {career}")


if __name__ == "__main__":
    main()
