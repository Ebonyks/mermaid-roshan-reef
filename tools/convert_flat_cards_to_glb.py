#!/usr/bin/env python3
"""Convert flat card art (PNG) into storybook-cutout GLBs with Blender.

Scans the un-integrated flat batches, builds an alpha-clipped textured card
with a slight cutout extrusion for each image, resizes any NPOT texture to
fit the 1024/POT rule, and exports to assets/art35/cards/<batch>/<name>.glb.
Protected art (book, voices, friends, characters) is never touched.
Run: python3 tools/convert_flat_cards_to_glb.py  (pip bpy or blender -b -P)
"""
from __future__ import annotations
from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]
BATCHES = {
    "style3": ROOT / "assets_src" / "style_review_score3",
    "batch04": ROOT / "assets_src" / "style_review_batch_04" / "final",
    "chroma": ROOT / "assets_src" / "imagegen" / "pass35_2026-07-16" / "chroma",
    "gen2": ROOT / "assets" / "props" / "gen2",
    "mg": ROOT / "assets" / "mg",
}
OUT = ROOT / "assets" / "art35" / "cards"
SKIP = ("contact_sheet", "qa_", "screenshot")


def pot_fit(n: int) -> int:
    p = 1
    while p * 2 <= min(n, 1024):
        p *= 2
    return p


def convert(src: Path, dst: Path) -> bool:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        img = bpy.data.images.load(str(src))
    except Exception:
        return False
    w, h = img.size
    if w == 0 or h == 0:
        return False
    if (w & (w - 1)) or (h & (h - 1)) or w > 1024 or h > 1024:
        img.scale(pot_fit(w), pot_fit(h))
    aspect = h / w
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    card = bpy.context.active_object
    card.name = src.stem
    card.scale = (1.0, aspect, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode="OBJECT")
    solid = card.modifiers.new("cutout", "SOLIDIFY")
    solid.thickness = 0.05
    bpy.ops.object.modifier_apply(modifier="cutout")
    m = bpy.data.materials.new("card_" + src.stem)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    m.node_tree.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    m.blend_method = "CLIP"
    card.data.materials.append(m)
    dst.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=str(dst), export_format="GLB",
                              use_selection=True, export_yup=True)
    return True


def main() -> None:
    done = failed = 0
    for tag, folder in BATCHES.items():
        if not folder.exists():
            continue
        for src in sorted(folder.glob("*.png")):
            if any(s in src.name.lower() for s in SKIP):
                continue
            if convert(src, OUT / tag / (src.stem + ".glb")):
                done += 1
            else:
                failed += 1
    print(f"converted {done} cards, {failed} failed")


if __name__ == "__main__":
    main()
