"""Convert reviewed, normalized Unity sprite placements to a Godot 4 Canvas scene."""

import argparse
import json
import math
from pathlib import Path, PurePosixPath


def number(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("Coordinates and scales must be finite numbers")
    return value


def pair(value):
    x, y = value
    return number(x), number(y)


def texture_path(value):
    if not isinstance(value, str) or not value.startswith("res://assets/"):
        raise ValueError("Use a reviewed project-local texture under res://assets/")
    relative = PurePosixPath(value.removeprefix("res://"))
    if ".." in relative.parts or "\\" in value or relative.suffix.lower() != ".png":
        raise ValueError("Use a canonical project-local PNG path")
    return value


def canvas_scene(source):
    if not isinstance(source, dict) or source.get("schema_version") != 1:
        raise ValueError("Expected placement schema 1")
    pixels = number(source["master_pixels_per_unit"])
    origin_x, origin_y = pair(source["master_origin"])
    if pixels <= 0:
        raise ValueError("master_pixels_per_unit must be positive")
    plane = source["plane"]
    if plane not in ("xy_up", "xz_forward"):
        raise ValueError("Select xy_up or xz_forward")
    vertical_axis = 1 if plane == "xy_up" else 2
    resources = {}
    nodes = []
    names = set()
    for sprite in source["sprites"]:
        name = sprite["name"]
        if not isinstance(name, str) or not name.isidentifier() or name in names:
            raise ValueError("Sprite names must be unique identifiers")
        names.add(name)
        texture = texture_path(sprite["texture"])
        resource = resources.setdefault(texture, f"Tex{len(resources) + 1}")
        x, y, z = map(number, sprite["position"])
        vertical = (x, y, z)[vertical_axis]
        x_scale, y_scale = pair(sprite.get("scale", [1, 1]))
        width, height = pair(sprite["texture_size"])
        pivot_x, pivot_y = pair(sprite.get("pivot", [0.5, 0.5]))
        ppu = number(sprite["sprite_pixels_per_unit"])
        depth = sprite["canvas_z"]
        if min(width, height, ppu, x_scale, y_scale) <= 0:
            raise ValueError("Sprite dimensions, PPU and scales must be positive")
        if not (0 <= pivot_x <= 1 and 0 <= pivot_y <= 1):
            raise ValueError("Unity normalized pivots must be in [0, 1]")
        if type(depth) is not int or not -4096 <= depth <= 4096:
            raise ValueError("canvas_z must be an explicit Godot z index")
        rotation = number(sprite.get("rotation_degrees", 0))
        nodes.extend([
            "",
            f'[node name={json.dumps(name)} type="Sprite2D" parent="."]',
            f"position = Vector2({origin_x + x * pixels:g}, {origin_y - vertical * pixels:g})",
            f"scale = Vector2({x_scale * pixels / ppu:g}, {y_scale * pixels / ppu:g})",
            f"offset = Vector2({(0.5 - pivot_x) * width:g}, {(pivot_y - 0.5) * height:g})",
            f"rotation = {-math.radians(rotation):.9g}",
            f"z_index = {depth}",
            f'texture = ExtResource("{resource}")',
        ])
    header = [f"[gd_scene load_steps={len(resources) + 1} format=3]", ""]
    header.extend(f'[ext_resource type="Texture2D" path={json.dumps(path)} id="{key}"]'
                  for path, key in resources.items())
    return "\n".join(header + ["", '[node name="ReviewedUnityPlacement" type="Node2D"]'] + nodes) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("placements", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        scene = canvas_scene(json.loads(args.placements.read_text(encoding="utf-8")))
        with args.output.open("x", encoding="utf-8", newline="\n") as out:
            out.write(scene)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f"unity_2d_layout_bridge: {error}\n")


if __name__ == "__main__":
    main()
