#!/usr/bin/env python3
"""Build the true-2D Evie and Lamb-a' animation atlases for Seek.

The generated sources use flat chroma fields.  Chroma removal is deliberately
border-connected: green/magenta costume pixels enclosed by the character
silhouette remain opaque.  Each action row is normalized as one coordinate
system so authored hop/gesture motion survives atlas packing.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets_src" / "imagegen" / "seek_animated_2026-08-09"
RUNTIME_DIR = ROOT / "assets" / "minigames" / "seek"
MANIFEST_PATH = SOURCE_DIR / "build_manifest.json"
PROMPT_PATH = SOURCE_DIR / "PROMPTS.md"
GRID_COLUMNS = 4
GRID_ROWS = 2
CELL_SIZE = 256
CELL_PADDING = 10
DESPILL_RADIUS = 8


@dataclass(frozen=True)
class ActorSpec:
    actor: str
    source_name: str
    expected_sha256: str
    declared_key: tuple[int, int, int]
    output_name: str


ACTORS = (
    ActorSpec(
        actor="lamma",
        source_name="lamma_atlas_chroma.png",
        expected_sha256="7f38bb41209073f38aaec2cd4a99ed609154da71b02a383e89bfa58548a051fa",
        declared_key=(255, 0, 255),
        output_name="lamma_animation.png",
    ),
    ActorSpec(
        actor="evie",
        source_name="evie_atlas_chroma.png",
        expected_sha256="2b1cd2703388f14525603146545d7b9299e53d68e0d0ead449b3a5d85fe40597",
        declared_key=(0, 255, 0),
        output_name="evie_animation.png",
    ),
)


def _sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _png_bytes(image: Image.Image) -> bytes:
    stream = BytesIO()
    image.save(stream, format="PNG", optimize=True, compress_level=9)
    return stream.getvalue()


def _split_edges(length: int, parts: int) -> list[int]:
    return [round(index * length / parts) for index in range(parts + 1)]


def _sample_border_key(image: Image.Image) -> tuple[int, int, int]:
    rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    border = np.concatenate((
        rgb[0, :, :],
        rgb[-1, :, :],
        rgb[1:-1, 0, :],
        rgb[1:-1, -1, :],
    ))
    median = np.median(border, axis=0)
    return tuple(int(round(value)) for value in median)


def _remove_border_chroma(
    image: Image.Image,
    declared_key: tuple[int, int, int],
    *,
    transparent_distance: float = 12.0,
    opaque_distance: float = 190.0,
) -> tuple[Image.Image, dict[str, Any]]:
    """Remove only key-colored pixels connected to the image border."""

    sampled_key = _sample_border_key(image)
    declared_delta = max(
        abs(sampled_key[channel] - declared_key[channel])
        for channel in range(3)
    )
    if declared_delta > 32:
        raise ValueError(
            f"sampled chroma {sampled_key} is not close to declared {declared_key}"
        )

    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    key = np.asarray(sampled_key, dtype=np.float32)
    distance = np.linalg.norm(rgb - key, axis=2)
    eligible = distance < opaque_distance
    height, width = eligible.shape
    connected = np.zeros((height, width), dtype=np.bool_)
    queue: deque[int] = deque()

    def seed(x_pos: int, y_pos: int) -> None:
        if eligible[y_pos, x_pos] and not connected[y_pos, x_pos]:
            connected[y_pos, x_pos] = True
            queue.append(y_pos * width + x_pos)

    for x_pos in range(width):
        seed(x_pos, 0)
        seed(x_pos, height - 1)
    for y_pos in range(1, height - 1):
        seed(0, y_pos)
        seed(width - 1, y_pos)

    while queue:
        packed = queue.popleft()
        y_pos, x_pos = divmod(packed, width)
        if x_pos > 0 and eligible[y_pos, x_pos - 1] \
                and not connected[y_pos, x_pos - 1]:
            connected[y_pos, x_pos - 1] = True
            queue.append(packed - 1)
        if x_pos + 1 < width and eligible[y_pos, x_pos + 1] \
                and not connected[y_pos, x_pos + 1]:
            connected[y_pos, x_pos + 1] = True
            queue.append(packed + 1)
        if y_pos > 0 and eligible[y_pos - 1, x_pos] \
                and not connected[y_pos - 1, x_pos]:
            connected[y_pos - 1, x_pos] = True
            queue.append(packed - width)
        if y_pos + 1 < height and eligible[y_pos + 1, x_pos] \
                and not connected[y_pos + 1, x_pos]:
            connected[y_pos + 1, x_pos] = True
            queue.append(packed + width)

    alpha = np.full((height, width), 255.0, dtype=np.float32)
    ramp = np.clip(
        (distance - transparent_distance)
        / (opaque_distance - transparent_distance),
        0.0,
        1.0,
    )
    alpha[connected] = ramp[connected] * 255.0

    # Recover foreground color from the chroma blend on antialiased edges.
    output_rgb = rgb.copy()
    partial = connected & (alpha > 0.0) & (alpha < 255.0)
    partial_alpha = alpha[partial, None] / 255.0
    output_rgb[partial] = np.clip(
        (rgb[partial] - (1.0 - partial_alpha) * key) / partial_alpha,
        0.0,
        255.0,
    )
    output_rgb[alpha <= 0.0] = 0.0
    rgba = np.dstack((
        output_rgb.astype(np.uint8),
        np.rint(alpha).astype(np.uint8),
    ))
    result = Image.fromarray(rgba, mode="RGBA")
    return result, {
        "sampled_key": list(sampled_key),
        "declared_key": list(declared_key),
        "border_connected_pixels": int(np.count_nonzero(connected)),
        "transparent_pixels": int(np.count_nonzero(alpha <= 0.0)),
        "partial_pixels": int(np.count_nonzero((alpha > 0.0) & (alpha < 255.0))),
    }


def _alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    box = image.getchannel("A").getbbox()
    if box is None:
        raise ValueError("animation cell has no visible subject")
    return box


def _despill_transparent_edges(
    image: Image.Image,
    declared_key: tuple[int, int, int],
    *,
    radius: int = DESPILL_RADIUS,
) -> tuple[Image.Image, dict[str, int]]:
    """Remove residual key hue only in the transparent-edge neighborhood.

    Image-generation antialiasing can leave fully opaque key-colored pixels
    just inside the matte, and atlas resampling can make that fringe visible.
    Limiting decontamination to a narrow shell preserves enclosed costume art.
    """

    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    alpha = rgba[:, :, 3]
    reachable = alpha == 0
    for _step in range(radius):
        padded = np.pad(reachable, 1, mode="constant", constant_values=False)
        reachable = (
            padded[1:-1, 1:-1]
            | padded[:-2, 1:-1]
            | padded[2:, 1:-1]
            | padded[1:-1, :-2]
            | padded[1:-1, 2:]
            | padded[:-2, :-2]
            | padded[:-2, 2:]
            | padded[2:, :-2]
            | padded[2:, 2:]
        )
    shell = reachable & (alpha > 0)
    rgb = rgba[:, :, :3].astype(np.int16)

    if declared_key[1] > declared_key[0] and declared_key[1] > declared_key[2]:
        spill = np.maximum(
            0,
            rgb[:, :, 1] - np.maximum(rgb[:, :, 0], rgb[:, :, 2]),
        )
        affected = shell & (spill > 0)
        rgb[:, :, 1][affected] -= spill[affected]
    elif declared_key[0] > declared_key[1] and declared_key[2] > declared_key[1]:
        spill = np.maximum(
            0,
            np.minimum(
                rgb[:, :, 0] - rgb[:, :, 1],
                rgb[:, :, 2] - rgb[:, :, 1],
            ),
        )
        affected = shell & (spill > 0)
        rgb[:, :, 0][affected] -= spill[affected]
        rgb[:, :, 2][affected] -= spill[affected]
    else:
        raise ValueError(f"unsupported chroma key for edge despill: {declared_key}")

    rgba[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, mode="RGBA"), {
        "radius": radius,
        "pixels": int(np.count_nonzero(affected)),
        "maximum_removed_channel_value": int(spill[affected].max())
        if np.any(affected) else 0,
    }


def _keep_primary_component(image: Image.Image) -> tuple[Image.Image, int]:
    """Discard neighboring-cell fragments and isolated generated specks."""

    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    visible = rgba[:, :, 3] > 0
    height, width = visible.shape
    visited = np.zeros((height, width), dtype=np.bool_)
    components: list[list[int]] = []

    for y_seed in range(height):
        for x_seed in range(width):
            if not visible[y_seed, x_seed] or visited[y_seed, x_seed]:
                continue
            component: list[int] = []
            queue: deque[int] = deque([y_seed * width + x_seed])
            visited[y_seed, x_seed] = True
            while queue:
                packed = queue.popleft()
                component.append(packed)
                y_pos, x_pos = divmod(packed, width)
                for y_next in range(max(0, y_pos - 1), min(height, y_pos + 2)):
                    for x_next in range(max(0, x_pos - 1), min(width, x_pos + 2)):
                        if visible[y_next, x_next] and not visited[y_next, x_next]:
                            visited[y_next, x_next] = True
                            queue.append(y_next * width + x_next)
            components.append(component)

    if not components:
        raise ValueError("animation cell has no visible component")
    primary = max(components, key=len)
    keep = np.zeros(height * width, dtype=np.bool_)
    keep[np.asarray(primary, dtype=np.int64)] = True
    keep = keep.reshape((height, width))
    removed = int(np.count_nonzero(visible & ~keep))
    rgba[~keep] = 0
    return Image.fromarray(rgba, mode="RGBA"), removed


def _pack_atlas(
    source: Image.Image,
) -> tuple[Image.Image, dict[str, Any]]:
    x_edges = _split_edges(source.width, GRID_COLUMNS)
    y_edges = _split_edges(source.height, GRID_ROWS)
    rows: list[list[Image.Image]] = []
    row_unions: list[tuple[int, int, int, int]] = []
    source_boxes: list[list[int]] = []
    removed_fragment_pixels: list[int] = []

    for row in range(GRID_ROWS):
        cells: list[Image.Image] = []
        boxes: list[tuple[int, int, int, int]] = []
        for column in range(GRID_COLUMNS):
            cell = source.crop((
                x_edges[column],
                y_edges[row],
                x_edges[column + 1],
                y_edges[row + 1],
            ))
            cell, removed = _keep_primary_component(cell)
            box = _alpha_bbox(cell)
            cells.append(cell)
            boxes.append(box)
            source_boxes.append(list(box))
            removed_fragment_pixels.append(removed)
        union = (
            min(box[0] for box in boxes),
            min(box[1] for box in boxes),
            max(box[2] for box in boxes),
            max(box[3] for box in boxes),
        )
        rows.append(cells)
        row_unions.append(union)

    maximum_width = max(box[2] - box[0] for box in row_unions)
    maximum_height = max(box[3] - box[1] for box in row_unions)
    available = CELL_SIZE - CELL_PADDING * 2
    scale = min(available / maximum_width, available / maximum_height)
    atlas = Image.new(
        "RGBA",
        (CELL_SIZE * GRID_COLUMNS, CELL_SIZE * GRID_ROWS),
        (0, 0, 0, 0),
    )
    runtime_boxes: list[list[int]] = []

    for row, cells in enumerate(rows):
        union = row_unions[row]
        union_width = union[2] - union[0]
        union_height = union[3] - union[1]
        resized_size = (
            max(1, round(union_width * scale)),
            max(1, round(union_height * scale)),
        )
        offset = (
            (CELL_SIZE - resized_size[0]) // 2,
            CELL_SIZE - CELL_PADDING - resized_size[1],
        )
        for column, cell in enumerate(cells):
            normalized = cell.crop(union).resize(
                resized_size,
                Image.Resampling.LANCZOS,
            )
            destination = (
                column * CELL_SIZE + offset[0],
                row * CELL_SIZE + offset[1],
            )
            atlas.alpha_composite(normalized, destination)
            runtime_box = _alpha_bbox(atlas.crop((
                column * CELL_SIZE,
                row * CELL_SIZE,
                (column + 1) * CELL_SIZE,
                (row + 1) * CELL_SIZE,
            )))
            runtime_boxes.append(list(runtime_box))

    for box in runtime_boxes:
        if box[0] <= 0 or box[1] <= 0 or box[2] >= CELL_SIZE \
                or box[3] >= CELL_SIZE:
            raise ValueError(f"runtime frame touches its cell edge: {box}")

    return atlas, {
        "grid": [GRID_COLUMNS, GRID_ROWS],
        "cell_size": [CELL_SIZE, CELL_SIZE],
        "source_cell_boxes": source_boxes,
        "removed_fragment_pixels": removed_fragment_pixels,
        "source_row_unions": [list(box) for box in row_unions],
        "runtime_cell_boxes": runtime_boxes,
        "scale": round(scale, 8),
    }


def _build_actor(spec: ActorSpec) -> tuple[Image.Image, dict[str, Any]]:
    source_path = SOURCE_DIR / spec.source_name
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    source_hash = _sha256_file(source_path)
    if source_hash != spec.expected_sha256:
        raise ValueError(
            f"{source_path}: expected {spec.expected_sha256}, got {source_hash}"
        )
    with Image.open(source_path) as opened:
        source_size = list(opened.size)
        keyed, chroma_metrics = _remove_border_chroma(
            opened,
            spec.declared_key,
        )
    atlas, atlas_metrics = _pack_atlas(keyed)
    atlas, despill_metrics = _despill_transparent_edges(
        atlas,
        spec.declared_key,
    )
    atlas_metrics["edge_despill"] = despill_metrics
    return atlas, {
        "source": source_path.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash,
        "source_dimensions": source_size,
        "chroma": chroma_metrics,
        "atlas": atlas_metrics,
    }


def build() -> tuple[dict[Path, bytes], dict[str, Any]]:
    outputs: dict[Path, bytes] = {}
    actors: dict[str, Any] = {}
    for spec in ACTORS:
        atlas, metrics = _build_actor(spec)
        output_path = RUNTIME_DIR / spec.output_name
        output_bytes = _png_bytes(atlas)
        outputs[output_path] = output_bytes
        metrics["output"] = output_path.relative_to(ROOT).as_posix()
        metrics["output_sha256"] = _sha256_bytes(output_bytes)
        metrics["output_dimensions"] = list(atlas.size)
        actors[spec.actor] = metrics
        if spec.actor == "evie":
            portrait = atlas.crop((0, 0, CELL_SIZE, CELL_SIZE))
            portrait_path = RUNTIME_DIR / "evie_portrait.png"
            portrait_bytes = _png_bytes(portrait)
            outputs[portrait_path] = portrait_bytes
            actors[spec.actor]["portrait"] = {
                "output": portrait_path.relative_to(ROOT).as_posix(),
                "output_sha256": _sha256_bytes(portrait_bytes),
                "output_dimensions": list(portrait.size),
            }

    manifest = {
        "schema_version": 1,
        "purpose": "true_canvas_seek_animated_actors",
        "grid": [GRID_COLUMNS, GRID_ROWS],
        "cell_size": [CELL_SIZE, CELL_SIZE],
        "frame_rows": {
            "evie": ["idle_hover", "point_giggle_cheer"],
            "lamma": ["idle_breathe", "peek_hop_celebrate"],
        },
        "prompt_record": PROMPT_PATH.relative_to(ROOT).as_posix(),
        "prompt_record_sha256": _sha256_file(PROMPT_PATH),
        "actors": actors,
    }
    return outputs, manifest


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_outputs(outputs: dict[Path, bytes], manifest: dict[str, Any]) -> None:
    for path, payload in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        print(f"SEEK_ANIM|WRITE|{path.relative_to(ROOT).as_posix()}")
    MANIFEST_PATH.write_bytes(_manifest_bytes(manifest))
    print(f"SEEK_ANIM|WRITE|{MANIFEST_PATH.relative_to(ROOT).as_posix()}")


def check_outputs(outputs: dict[Path, bytes], manifest: dict[str, Any]) -> bool:
    failures: list[str] = []
    for path, expected in outputs.items():
        if not path.is_file():
            failures.append(f"missing {path.relative_to(ROOT).as_posix()}")
        elif path.read_bytes() != expected:
            failures.append(f"drift {path.relative_to(ROOT).as_posix()}")
    expected_manifest = _manifest_bytes(manifest)
    if not MANIFEST_PATH.is_file():
        failures.append(f"missing {MANIFEST_PATH.relative_to(ROOT).as_posix()}")
    elif MANIFEST_PATH.read_bytes() != expected_manifest:
        failures.append(f"drift {MANIFEST_PATH.relative_to(ROOT).as_posix()}")
    for failure in failures:
        print(f"SEEK_ANIM|FAIL|{failure}")
    if failures:
        return False
    print(f"SEEK_ANIM|PASS|outputs={len(outputs)}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, manifest = build()
    if args.write:
        write_outputs(outputs, manifest)
    elif not check_outputs(outputs, manifest):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
