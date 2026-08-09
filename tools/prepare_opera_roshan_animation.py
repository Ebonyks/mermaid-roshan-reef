#!/usr/bin/env python3
"""Normalize a generated Opera Roshan sheet into sixteen clip-safe cells.

The image generator is asked for a 4x4 chroma-key sheet, but its figures can
drift a few pixels across the mathematical cell boundaries.  Sampling that
sheet with a plain AtlasTexture would recreate the exact head/tail clipping
this asset family is meant to fix.  This tool assigns connected artwork to a
cell by its centroid, preserves the complete component matte, applies one
shared scale to every frame, and packs the results into a 1024x1024 RGBA
runtime sheet with measured padding.

The chroma-key removal remains a separate, provenance-preserving step.  Pass
the native alpha result from the installed imagegen helper to --input-alpha.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


COLS = 4
ROWS = 4
CELL = 256
FRAME_COUNT = COLS * ROWS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-alpha", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--alpha-threshold", type=int, default=64)
    parser.add_argument("--min-component-area", type=int, default=1800)
    parser.add_argument("--cell-padding", type=int, default=16)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0 < args.alpha_threshold < 255:
        raise SystemExit("--alpha-threshold must be between 1 and 254")
    if not 4 <= args.cell_padding <= 48:
        raise SystemExit("--cell-padding must be between 4 and 48")

    source = Image.open(args.input_alpha).convert("RGBA")
    pixels = np.asarray(source)
    alpha = pixels[:, :, 3]
    labels, count = ndimage.label(
        alpha > args.alpha_threshold,
        structure=np.ones((3, 3), dtype=np.uint8),
    )

    components: list[dict[str, object]] = []
    for label_id in range(1, count + 1):
        positions = np.argwhere(labels == label_id)
        if positions.shape[0] < args.min_component_area:
            continue
        y0, x0 = positions.min(axis=0)
        y1, x1 = positions.max(axis=0) + 1
        cy, cx = positions.mean(axis=0)
        components.append(
            {
                "label": label_id,
                "area": int(positions.shape[0]),
                "bbox": [int(x0), int(y0), int(x1), int(y1)],
                "centroid": [float(cx), float(cy)],
            }
        )

    groups: dict[tuple[int, int], list[dict[str, object]]] = {}
    for component in components:
        cx, cy = component["centroid"]
        row = min(int(cy / (source.height / ROWS)), ROWS - 1)
        col = min(int(cx / (source.width / COLS)), COLS - 1)
        groups.setdefault((row, col), []).append(component)

    occupied = sorted(groups)
    expected = [(row, col) for row in range(ROWS) for col in range(COLS)]
    if occupied != expected:
        raise SystemExit(
            f"expected one occupied subject group in every 4x4 cell; got {occupied}"
        )

    frames: list[dict[str, object]] = []
    for row, col in expected:
        group = groups[(row, col)]
        label_ids = [int(component["label"]) for component in group]
        primary = np.isin(labels, label_ids)
        support = ndimage.binary_dilation(
            primary,
            structure=np.ones((3, 3), dtype=np.uint8),
            iterations=3,
        )
        support &= alpha > 0
        positions = np.argwhere(support)
        if positions.size == 0:
            raise SystemExit(f"cell {(row, col)} has no supported alpha pixels")
        y0, x0 = positions.min(axis=0)
        y1, x1 = positions.max(axis=0) + 1
        x0 = max(0, int(x0) - 4)
        y0 = max(0, int(y0) - 4)
        x1 = min(source.width, int(x1) + 4)
        y1 = min(source.height, int(y1) + 4)
        crop_pixels = pixels[y0:y1, x0:x1].copy()
        crop_support = support[y0:y1, x0:x1]
        crop_pixels[~crop_support] = 0
        frames.append(
            {
                "row": row,
                "col": col,
                "source_components": group,
                "source_bbox": [x0, y0, x1, y1],
                "image": Image.fromarray(crop_pixels, "RGBA"),
            }
        )

    usable = CELL - args.cell_padding * 2
    max_width = max(frame["image"].width for frame in frames)
    max_height = max(frame["image"].height for frame in frames)
    shared_scale = min(usable / max_width, usable / max_height)
    if shared_scale <= 0.0:
        raise SystemExit("computed a non-positive frame scale")

    sheet = Image.new("RGBA", (COLS * CELL, ROWS * CELL), (0, 0, 0, 0))
    report_frames: list[dict[str, object]] = []
    for frame in frames:
        crop: Image.Image = frame.pop("image")
        width = max(1, int(round(crop.width * shared_scale)))
        height = max(1, int(round(crop.height * shared_scale)))
        resized = crop.resize((width, height), Image.Resampling.LANCZOS)
        row = int(frame["row"])
        col = int(frame["col"])
        x = col * CELL + (CELL - width) // 2
        y = row * CELL + CELL - args.cell_padding - height
        sheet.alpha_composite(resized, (x, y))
        report_frames.append(
            {
                **frame,
                "runtime_rect": [x, y, x + width, y + height],
                "runtime_size": [width, height],
            }
        )

    # Transparent texels still take part in GPU filtering.  Clear their RGB
    # so no chroma tint can fringe around the illustrated outline.
    packed = np.array(sheet)
    packed[packed[:, :, 3] == 0, :3] = 0
    sheet = Image.fromarray(packed, "RGBA")

    cell_audits: list[dict[str, object]] = []
    for row, col in expected:
        cell = sheet.getchannel("A").crop(
            (col * CELL, row * CELL, (col + 1) * CELL, (row + 1) * CELL)
        )
        bbox = cell.getbbox()
        if bbox is None:
            raise SystemExit(f"runtime cell {(row, col)} is empty")
        left, top, right, bottom = bbox
        safe = (
            left >= args.cell_padding - 2
            and top >= args.cell_padding - 2
            and right <= CELL - args.cell_padding + 2
            and bottom <= CELL - args.cell_padding + 2
        )
        cell_audits.append(
            {"row": row, "col": col, "alpha_bbox": list(bbox), "safe": safe}
        )
    if not all(item["safe"] for item in cell_audits):
        raise SystemExit(f"one or more packed frames violate padding: {cell_audits}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, optimize=True)
    report = {
        "pass": True,
        "method": (
            "8-connected alpha components grouped by 4x4 centroid; 3px matte "
            "support; one shared whole-figure scale; bottom-aligned 256px cells"
        ),
        "input": str(args.input_alpha),
        "input_sha256": sha256(args.input_alpha),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "source_size": list(source.size),
        "runtime_size": list(sheet.size),
        "shared_scale": shared_scale,
        "cell_padding": args.cell_padding,
        "component_count": len(components),
        "frames": report_frames,
        "cell_audits": cell_audits,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"packed {FRAME_COUNT} clip-safe frames -> {args.output} "
        f"(shared scale {shared_scale:.4f})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
