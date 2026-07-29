#!/usr/bin/env python3
"""Prepare and assemble native-detail Pearl Castle Main Hall masters.

The built-in image generator returns 1672x940 review images. This tool never
upscales those images. Instead, it:

1. prepares four overlapping reference crops per screen;
2. accepts four separately regenerated native-detail quadrant images;
3. extracts a smaller 1152x648 native crop from each generated image;
4. feather-composites those crops into a new 2048x1153 master; and
5. records seam, ratio, source, crop, and structure evidence.

The 2048x1153 master is then eligible for the repository's ordinary lossless
2x2 runtime slicing. Acceptance still depends on the visual and structural
audit; dimensions alone are not sufficient.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit" / "castle_sprite3d"
ITERATIONS = AUDIT / "room_led_iterations"
CONCEPT_SIZE = (1672, 940)
REFERENCE_CROP_SIZE = (941, 529)
PATCH_SIZE = (1152, 648)
MASTER_SIZE = (2048, 1153)
PATCH_POSITIONS = {
    "tl": (0, 0),
    "tr": (896, 0),
    "bl": (0, 505),
    "br": (896, 505),
}
REFERENCE_RECTS = {
    "tl": (0, 0, 941, 529),
    "tr": (731, 0, 1672, 529),
    "bl": (0, 411, 941, 940),
    "br": (731, 411, 1672, 940),
}
CONTEXT_RECTS = {
    "tl": (0, 0, 1367, 769),
    "tr": (305, 0, 1672, 769),
    "bl": (0, 171, 1367, 940),
    "br": (305, 171, 1672, 940),
}
CONTEXT_TARGET_RECTS = REFERENCE_RECTS
REPAIR_CONTEXT_RECTS = {
    "top": (188, 0, 1860, 941),
    "bottom": (188, 212, 1860, 1153),
}
REPAIR_BAND_RECT = (640, 0, 1408, 1153)
REPAIR_GENERATED_CROPS = {
    "top": (452, 0, 1220, 648),
    "bottom": (452, 293, 1220, 941),
}
LOWER_RIGHT_CONTEXT_RECT = (376, 212, 2048, 1153)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    filename = "segoeuib.ttf" if bold else "segoeui.ttf"
    candidate = Path("C:/Windows/Fonts") / filename
    if candidate.exists():
        return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def prepare(screen: str, concept: Path, pass_dir: Path) -> None:
    concept = concept.resolve()
    pass_dir = pass_dir.resolve()
    with Image.open(concept) as source_image:
        source = source_image.convert("RGB")
    if source.size != CONCEPT_SIZE:
        raise ValueError(f"Expected {CONCEPT_SIZE}, got {source.size}: {concept}")
    reference_dir = pass_dir / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for quadrant, rect in REFERENCE_RECTS.items():
        crop = source.crop(rect)
        path = reference_dir / f"screen_{screen}_{quadrant}_reference.png"
        crop.save(path, optimize=True)
        records.append(
            {
                "quadrant": quadrant,
                "path": path.relative_to(ROOT).as_posix(),
                "dimensions": list(crop.size),
                "source_rect": list(rect),
                "sha256": sha256(path),
            }
        )
    manifest = {
        "schema": "castle-room-led-native-reference-v1",
        "screen": screen,
        "concept": concept.relative_to(ROOT).as_posix(),
        "concept_dimensions": list(source.size),
        "concept_sha256": sha256(concept),
        "reference_crop_dimensions": list(REFERENCE_CROP_SIZE),
        "references": records,
        "note": "Reference crops are generator inputs only; they are never enlarged or used at runtime.",
    }
    (pass_dir / f"screen_{screen}_reference_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def prepare_context(screen: str, concept: Path, pass_dir: Path) -> None:
    concept = concept.resolve()
    pass_dir = pass_dir.resolve()
    with Image.open(concept) as source_image:
        source = source_image.convert("RGB")
    if source.size != CONCEPT_SIZE:
        raise ValueError(f"Expected {CONCEPT_SIZE}, got {source.size}: {concept}")
    reference_dir = pass_dir / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for quadrant, rect in CONTEXT_RECTS.items():
        crop = source.crop(rect)
        path = reference_dir / f"screen_{screen}_{quadrant}_context.png"
        crop.save(path, optimize=True)
        target = CONTEXT_TARGET_RECTS[quadrant]
        relative_target = (
            target[0] - rect[0],
            target[1] - rect[1],
            target[2] - rect[0],
            target[3] - rect[1],
        )
        records.append(
            {
                "quadrant": quadrant,
                "path": path.relative_to(ROOT).as_posix(),
                "dimensions": list(crop.size),
                "source_rect": list(rect),
                "target_source_rect": list(target),
                "target_rect_within_context": list(relative_target),
                "sha256": sha256(path),
            }
        )
    manifest = {
        "schema": "castle-room-led-native-context-v1",
        "screen": screen,
        "concept": concept.relative_to(ROOT).as_posix(),
        "concept_dimensions": list(source.size),
        "concept_sha256": sha256(concept),
        "context_dimensions": [1367, 769],
        "contexts": records,
        "note": (
            "Context crops are generator inputs only. Each regenerated image is "
            "cropped without scaling back to its mapped 1152x648 native target."
        ),
    }
    (pass_dir / f"screen_{screen}_context_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def prepare_repair(screen: str, master: Path, pass_dir: Path) -> None:
    master = master.resolve()
    pass_dir = pass_dir.resolve()
    with Image.open(master) as source_image:
        source = source_image.convert("RGB")
    if source.size != MASTER_SIZE:
        raise ValueError(f"Expected {MASTER_SIZE}, got {source.size}: {master}")
    reference_dir = pass_dir / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for section, rect in REPAIR_CONTEXT_RECTS.items():
        context = source.crop(rect)
        path = reference_dir / f"screen_{screen}_{section}_seam_repair_context.png"
        context.save(path, optimize=True)
        records.append(
            {
                "section": section,
                "path": path.relative_to(ROOT).as_posix(),
                "dimensions": list(context.size),
                "master_rect": list(rect),
                "generated_native_crop": list(REPAIR_GENERATED_CROPS[section]),
                "sha256": sha256(path),
            }
        )
    manifest = {
        "schema": "castle-room-led-seam-repair-context-v1",
        "screen": screen,
        "rejected_master": {
            "path": master.relative_to(ROOT).as_posix(),
            "dimensions": list(source.size),
            "sha256": sha256(master),
        },
        "contexts": records,
        "repair_band_master_rect": list(REPAIR_BAND_RECT),
        "note": (
            "Generator contexts and output have identical 1672x941 dimensions. "
            "The repair band is extracted and inserted without scaling."
        ),
    }
    (pass_dir / f"screen_{screen}_seam_repair_context_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def prepare_lower_right(screen: str, master: Path, pass_dir: Path) -> None:
    master = master.resolve()
    pass_dir = pass_dir.resolve()
    with Image.open(master) as source_image:
        source = source_image.convert("RGB")
    if source.size != MASTER_SIZE:
        raise ValueError(f"Expected {MASTER_SIZE}, got {source.size}: {master}")
    context = source.crop(LOWER_RIGHT_CONTEXT_RECT)
    reference_dir = pass_dir / "references"
    reference_dir.mkdir(parents=True, exist_ok=True)
    path = reference_dir / f"screen_{screen}_lower_right_repair_context.png"
    context.save(path, optimize=True)
    manifest = {
        "schema": "castle-room-led-lower-right-context-v1",
        "screen": screen,
        "source_master": {
            "path": master.relative_to(ROOT).as_posix(),
            "dimensions": list(source.size),
            "sha256": sha256(master),
        },
        "context": {
            "path": path.relative_to(ROOT).as_posix(),
            "dimensions": list(context.size),
            "master_rect": list(LOWER_RIGHT_CONTEXT_RECT),
            "sha256": sha256(path),
        },
        "note": "The native generator output is aligned to the master bottom-right without scaling.",
    }
    (pass_dir / f"screen_{screen}_lower_right_context_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def mapped_context_crop(
    image: Image.Image, quadrant: str, size: tuple[int, int]
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    width, height = size
    if image.width < width or image.height < height:
        raise ValueError(f"Generated image {image.size} is smaller than crop {size}")
    context = CONTEXT_RECTS[quadrant]
    target = CONTEXT_TARGET_RECTS[quadrant]
    context_width = context[2] - context[0]
    context_height = context[3] - context[1]
    target_left = target[0] - context[0]
    target_top = target[1] - context[1]
    left = round(target_left * image.width / context_width)
    top = round(target_top * image.height / context_height)
    left = min(max(left, 0), image.width - width)
    top = min(max(top, 0), image.height - height)
    rect = (left, top, left + width, top + height)
    return image.crop(rect), rect


def minimum_vertical_seam(cost: np.ndarray) -> np.ndarray:
    height, width = cost.shape
    cumulative = cost.astype(np.float64).copy()
    backtrack = np.zeros((height, width), dtype=np.int8)
    for y in range(1, height):
        previous = cumulative[y - 1]
        padded = np.pad(previous, (1, 1), mode="edge")
        choices = np.stack(
            (padded[0:width], padded[1 : width + 1], padded[2 : width + 2]),
            axis=0,
        )
        selected = np.argmin(choices, axis=0)
        cumulative[y] += choices[selected, np.arange(width)]
        backtrack[y] = selected.astype(np.int8) - 1
    seam = np.zeros(height, dtype=np.int32)
    seam[-1] = int(np.argmin(cumulative[-1]))
    for y in range(height - 1, 0, -1):
        seam[y - 1] = int(
            np.clip(seam[y] + backtrack[y, seam[y]], 0, width - 1)
        )
    return seam


def stitch_horizontal(
    left: Image.Image, right: Image.Image
) -> tuple[Image.Image, np.ndarray, float]:
    overlap = PATCH_SIZE[0] * 2 - MASTER_SIZE[0]
    left_array = np.asarray(left.convert("RGB"), dtype=np.uint8)
    right_array = np.asarray(right.convert("RGB"), dtype=np.uint8)
    left_overlap = left_array[:, -overlap:].astype(np.float32)
    right_overlap = right_array[:, :overlap].astype(np.float32)
    cost = np.abs(left_overlap - right_overlap).mean(axis=2)
    edge_penalty = np.abs(
        np.gradient(left_overlap.mean(axis=2), axis=1)
        - np.gradient(right_overlap.mean(axis=2), axis=1)
    )
    cost += edge_penalty * 0.35
    seam = minimum_vertical_seam(cost)
    output = np.empty((PATCH_SIZE[1], MASTER_SIZE[0], 3), dtype=np.uint8)
    output[:, : PATCH_SIZE[0]] = left_array
    output[:, PATCH_SIZE[0] :] = right_array[:, overlap:]
    overlap_start = PATCH_POSITIONS["tr"][0]
    for y, seam_x in enumerate(seam):
        split = overlap_start + int(seam_x)
        output[y, split : overlap_start + overlap] = right_array[
            y, int(seam_x) : overlap
        ]
    chosen_error = float(cost[np.arange(cost.shape[0]), seam].mean())
    return Image.fromarray(output, mode="RGB"), seam, chosen_error


def stitch_vertical(
    top: Image.Image, bottom: Image.Image
) -> tuple[Image.Image, np.ndarray, float]:
    overlap = PATCH_SIZE[1] * 2 - MASTER_SIZE[1]
    top_array = np.asarray(top.convert("RGB"), dtype=np.uint8)
    bottom_array = np.asarray(bottom.convert("RGB"), dtype=np.uint8)
    top_overlap = top_array[-overlap:, :].astype(np.float32)
    bottom_overlap = bottom_array[:overlap, :].astype(np.float32)
    cost = np.abs(top_overlap - bottom_overlap).mean(axis=2)
    edge_penalty = np.abs(
        np.gradient(top_overlap.mean(axis=2), axis=0)
        - np.gradient(bottom_overlap.mean(axis=2), axis=0)
    )
    cost += edge_penalty * 0.35
    seam = minimum_vertical_seam(cost.T)
    output = np.empty((MASTER_SIZE[1], top.width, 3), dtype=np.uint8)
    output[: PATCH_SIZE[1], :] = top_array
    output[PATCH_SIZE[1] :, :] = bottom_array[overlap:, :]
    overlap_start = PATCH_POSITIONS["bl"][1]
    for x, seam_y in enumerate(seam):
        split = overlap_start + int(seam_y)
        output[split : overlap_start + overlap, x] = bottom_array[
            int(seam_y) : overlap, x
        ]
    chosen_error = float(cost[seam, np.arange(cost.shape[1])].mean())
    return Image.fromarray(output, mode="RGB"), seam, chosen_error


def apply_repair(
    screen: str,
    base_master_path: Path,
    generated_top_path: Path,
    generated_bottom_path: Path,
    pass_dir: Path,
    output_master_path: Path,
) -> None:
    base_master_path = base_master_path.resolve()
    generated_top_path = generated_top_path.resolve()
    generated_bottom_path = generated_bottom_path.resolve()
    pass_dir = pass_dir.resolve()
    output_master_path = output_master_path.resolve()
    with Image.open(base_master_path) as image:
        base = image.convert("RGB")
    with Image.open(generated_top_path) as image:
        generated_top = image.convert("RGB")
    with Image.open(generated_bottom_path) as image:
        generated_bottom = image.convert("RGB")
    if base.size != MASTER_SIZE:
        raise ValueError(f"Expected base {MASTER_SIZE}, got {base.size}")
    valid_widths = (1671, 1672)
    if (
        generated_top.width not in valid_widths
        or generated_bottom.width not in valid_widths
        or generated_top.height != 941
        or generated_bottom.height != 941
    ):
        raise ValueError(
            "Seam repair generations must be native 1671/1672x941 outputs"
        )
    repair_width = min(generated_top.width, generated_bottom.width)
    band_x_left = 0
    band_x_right = repair_width
    top_band = generated_top.crop((band_x_left, 0, band_x_right, 941))
    bottom_band = generated_bottom.crop((band_x_left, 0, band_x_right, 941))
    top_array = np.asarray(top_band, dtype=np.uint8)
    bottom_array = np.asarray(bottom_band, dtype=np.uint8)
    # Both repair contexts map 1:1 to the master. Their shared master range is
    # y=212..941. Restrict the join to empty foreground floor (y=850..941) so
    # a rejected lower generation can never replace accepted architecture.
    join_top = 850
    join_bottom = 941
    bottom_context_y = REPAIR_CONTEXT_RECTS["bottom"][1]
    top_overlap = top_array[join_top:join_bottom].astype(np.float32)
    bottom_overlap = bottom_array[
        join_top - bottom_context_y : join_bottom - bottom_context_y
    ].astype(np.float32)
    row_cost = np.abs(top_overlap - bottom_overlap).mean(axis=2)
    row_seam_local = minimum_vertical_seam(row_cost.T)
    row_seam = row_seam_local + join_top
    band_array = np.empty(
        (MASTER_SIZE[1], repair_width, 3),
        dtype=np.uint8,
    )
    for x, master_y in enumerate(row_seam):
        split = int(master_y)
        band_array[:split, x] = top_array[:split, x]
        band_array[split:, x] = bottom_array[
            split - bottom_context_y :, x
        ]
    row_error = float(
        row_cost[row_seam_local, np.arange(row_cost.shape[1])].mean()
    )
    band = Image.fromarray(band_array, mode="RGB")
    base_array = np.asarray(base, dtype=np.uint8).copy()
    band_left = REPAIR_CONTEXT_RECTS["top"][0]
    band_right = band_left + repair_width
    side_overlap = 64
    left_original = base_array[:, band_left : band_left + side_overlap].astype(
        np.float32
    )
    left_repair = band_array[:, :side_overlap].astype(np.float32)
    left_cost = np.abs(left_original - left_repair).mean(axis=2)
    left_split = int(np.argmin(left_cost.mean(axis=0)))
    right_repair = band_array[:, -side_overlap:].astype(np.float32)
    right_original = base_array[:, band_right - side_overlap : band_right].astype(
        np.float32
    )
    right_cost = np.abs(right_repair - right_original).mean(axis=2)
    right_split = int(np.argmin(right_cost.mean(axis=0)))
    output = base_array
    for y in range(MASTER_SIZE[1]):
        left_local = left_split
        right_local = band.width - side_overlap + right_split
        output[
            y,
            band_left + left_local : band_left + right_local,
        ] = band_array[y, left_local:right_local]
    result = Image.fromarray(output, mode="RGB")
    output_master_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_master_path, optimize=True)
    band_path = pass_dir / f"screen_{screen}_native_repair_band.png"
    band.save(band_path, optimize=True)
    manifest = {
        "schema": "castle-room-led-seam-repair-v1",
        "screen": screen,
        "base_master": {
            "path": base_master_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(base_master_path),
        },
        "generated": {
            "top_path": str(generated_top_path),
            "top_sha256": sha256(generated_top_path),
            "bottom_path": str(generated_bottom_path),
            "bottom_sha256": sha256(generated_bottom_path),
            "scaled": False,
        },
        "repair_band": {
            "path": band_path.relative_to(ROOT).as_posix(),
            "dimensions": list(band.size),
            "sha256": sha256(band_path),
            "master_rect": [band_left, 0, band_right, MASTER_SIZE[1]],
            "row_seam_min": int(row_seam.min()),
            "row_seam_max": int(row_seam.max()),
            "row_seam_mean_cost": round(row_error, 4),
        },
        "side_seams": {
            "overlap_pixels": side_overlap,
            "left_split": left_split,
            "right_split": right_split,
            "path": "straight native-pixel seam selected by minimum mean error",
        },
        "output_master": {
            "path": output_master_path.relative_to(ROOT).as_posix(),
            "dimensions": list(result.size),
            "sha256": sha256(output_master_path),
            "native_long_edge_pass": max(result.size) >= 2048,
            "assembled_without_scaling": True,
        },
    }
    (pass_dir / f"screen_{screen}_seam_repair_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def apply_lower_right(
    screen: str,
    base_master_path: Path,
    generated_path: Path,
    pass_dir: Path,
    output_master_path: Path,
) -> None:
    base_master_path = base_master_path.resolve()
    generated_path = generated_path.resolve()
    pass_dir = pass_dir.resolve()
    output_master_path = output_master_path.resolve()
    with Image.open(base_master_path) as image:
        base = image.convert("RGB")
    with Image.open(generated_path) as image:
        generated = image.convert("RGB")
    if base.size != MASTER_SIZE:
        raise ValueError(f"Expected base {MASTER_SIZE}, got {base.size}")
    if generated.width not in (1671, 1672) or generated.height != 941:
        raise ValueError(f"Expected native 1671/1672x941, got {generated.size}")
    base_array = np.asarray(base, dtype=np.uint8).copy()
    patch_array = np.asarray(generated, dtype=np.uint8)
    left = MASTER_SIZE[0] - generated.width
    top = MASTER_SIZE[1] - generated.height
    overlap = 64
    left_cost = np.abs(
        base_array[top:, left : left + overlap].astype(np.float32)
        - patch_array[:, :overlap].astype(np.float32)
    ).mean(axis=2)
    left_split = int(np.argmin(left_cost.mean(axis=0)))
    top_cost = np.abs(
        base_array[top : top + overlap, left:].astype(np.float32)
        - patch_array[:overlap].astype(np.float32)
    ).mean(axis=2)
    top_split = int(np.argmin(top_cost.mean(axis=1)))
    output = base_array
    output[
        top + top_split :,
        left + left_split :,
    ] = patch_array[top_split:, left_split:]
    result = Image.fromarray(output, mode="RGB")
    output_master_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_master_path, optimize=True)
    manifest = {
        "schema": "castle-room-led-lower-right-repair-v1",
        "screen": screen,
        "base_master": {
            "path": base_master_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(base_master_path),
        },
        "generated": {
            "path": str(generated_path),
            "dimensions": list(generated.size),
            "sha256": sha256(generated_path),
            "scaled": False,
        },
        "placement": {
            "left": left,
            "top": top,
            "left_overlap_split": left_split,
            "top_overlap_split": top_split,
            "path": "straight native-pixel seams selected by minimum mean error",
        },
        "output_master": {
            "path": output_master_path.relative_to(ROOT).as_posix(),
            "dimensions": list(result.size),
            "sha256": sha256(output_master_path),
            "native_long_edge_pass": max(result.size) >= 2048,
            "assembled_without_scaling": True,
        },
    }
    (pass_dir / f"screen_{screen}_lower_right_repair_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def boundary_error(master: Image.Image, axis: str, coordinate: int) -> float:
    array = np.asarray(master.convert("RGB"), dtype=np.float32)
    if axis == "vertical":
        left = array[:, coordinate - 1]
        right = array[:, coordinate]
    else:
        left = array[coordinate - 1]
        right = array[coordinate]
    return float(np.abs(left - right).mean())


def structure_metrics(concept: Image.Image, master: Image.Image) -> dict[str, float]:
    normalized = master.resize(concept.size, Image.Resampling.LANCZOS)
    source = np.asarray(concept.convert("RGB"), dtype=np.float32)
    candidate = np.asarray(normalized.convert("RGB"), dtype=np.float32)
    difference = np.abs(source - candidate)
    source_edges = np.asarray(
        concept.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32
    )
    candidate_edges = np.asarray(
        normalized.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32
    )
    return {
        "normalized_rgb_mean_abs_error": round(float(difference.mean()), 4),
        "normalized_edge_mean_abs_error": round(
            float(np.abs(source_edges - candidate_edges).mean()), 4
        ),
    }


def audit_board(
    screen: str,
    concept: Image.Image,
    master: Image.Image,
    patches: dict[str, Image.Image],
    output: Path,
) -> None:
    canvas = Image.new("RGB", (2048, 1620), "#f5f2ff")
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (28, 18),
        f"Pearl Castle Screen {screen.upper()} — native master audit",
        font=font(34, True),
        fill="#302a68",
    )
    draw.text(
        (28, 65),
        "Top: 1672x940 concept reference | Middle: 2048x1153 native-detail master | Bottom: four generated patches",
        font=font(20),
        fill="#655b8e",
    )
    concept_preview = concept.resize((960, 540), Image.Resampling.LANCZOS)
    master_preview = master.resize((960, 540), Image.Resampling.LANCZOS)
    canvas.paste(concept_preview, (28, 104))
    canvas.paste(master_preview, (1060, 104))
    draw.rectangle((28, 104, 988, 644), outline="#59468a", width=4)
    draw.rectangle((1060, 104, 2020, 644), outline="#2e9b92", width=4)
    draw.text((40, 114), "CONCEPT / BELOW 2K", font=font(20, True), fill="#8e4055")
    draw.text((1072, 114), "MASTER / 2048x1153", font=font(20, True), fill="#237d75")
    positions = {"tl": (28, 700), "tr": (538, 700), "bl": (1048, 700), "br": (1558, 700)}
    for quadrant, patch in patches.items():
        preview = patch.resize((462, 260), Image.Resampling.LANCZOS)
        x, y = positions[quadrant]
        canvas.paste(preview, (x, y))
        draw.rectangle((x, y, x + 462, y + 260), outline="#d5a733", width=3)
        draw.text((x + 8, y + 8), quadrant.upper(), font=font(20, True), fill="#302a68")
    full = master.resize((1992, 1121), Image.Resampling.LANCZOS)
    full = full.crop((0, 620, 1992, 1121))
    canvas.paste(full, (28, 1048))
    draw.text((40, 1058), "LOWER-LANE / SEAM REVIEW", font=font(20, True), fill="#302a68")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def assemble(
    screen: str,
    concept_path: Path,
    generated: dict[str, Path],
    pass_dir: Path,
    output_master: Path,
) -> None:
    concept_path = concept_path.resolve()
    pass_dir = pass_dir.resolve()
    output_master = output_master.resolve()
    generated = {
        quadrant: path.resolve() for quadrant, path in generated.items()
    }
    patches: dict[str, Image.Image] = {}
    patch_records: list[dict[str, object]] = []
    patch_dir = pass_dir / "native_patches"
    patch_dir.mkdir(parents=True, exist_ok=True)
    for quadrant, generated_path in generated.items():
        with Image.open(generated_path) as generated_image:
            generated_rgb = generated_image.convert("RGB")
        patch, generator_crop_rect = mapped_context_crop(
            generated_rgb, quadrant, PATCH_SIZE
        )
        patch_path = patch_dir / f"screen_{screen}_{quadrant}_native_patch.png"
        patch.save(patch_path, optimize=True)
        patches[quadrant] = patch
        patch_records.append(
            {
                "quadrant": quadrant,
                "generator_path": str(generated_path),
                "generator_dimensions": list(generated_rgb.size),
                "generator_sha256": sha256(generated_path),
                "native_crop_dimensions": list(patch.size),
                "generator_crop_rect": list(generator_crop_rect),
                "native_crop_path": patch_path.relative_to(ROOT).as_posix(),
                "native_crop_sha256": sha256(patch_path),
                "master_position": list(PATCH_POSITIONS[quadrant]),
                "scaled": False,
            }
        )

    top, top_seam, top_error = stitch_horizontal(patches["tl"], patches["tr"])
    bottom, bottom_seam, bottom_error = stitch_horizontal(
        patches["bl"], patches["br"]
    )
    master, row_seam, row_error = stitch_vertical(top, bottom)
    output_master.parent.mkdir(parents=True, exist_ok=True)
    master.save(output_master, optimize=True)

    with Image.open(concept_path) as concept_image:
        concept = concept_image.convert("RGB")
    normalized_master = master.resize(concept.size, Image.Resampling.LANCZOS)
    difference = ImageChops.difference(concept, normalized_master)
    difference_path = pass_dir / f"screen_{screen}_concept_difference.png"
    difference.save(difference_path, optimize=True)
    board_path = pass_dir / f"screen_{screen}_native_master_audit.png"
    audit_board(screen, concept, master, patches, board_path)
    manifest = {
        "schema": "castle-room-led-native-master-v1",
        "screen": screen,
        "concept": {
            "path": concept_path.relative_to(ROOT).as_posix(),
            "dimensions": list(concept.size),
            "sha256": sha256(concept_path),
            "runtime_accepted": False,
        },
        "master": {
            "path": output_master.relative_to(ROOT).as_posix(),
            "dimensions": list(master.size),
            "aspect_ratio": round(master.width / master.height, 9),
            "approved_ratio_target": round(1672 / 941, 9),
            "ratio_delta": round(abs(master.width / master.height - 1672 / 941), 9),
            "native_long_edge": max(master.size),
            "native_long_edge_pass": max(master.size) >= 2048,
            "sha256": sha256(output_master),
            "assembled_without_scaling": True,
        },
        "patches": patch_records,
        "overlaps": {
            "horizontal_pixels": PATCH_SIZE[0] * 2 - MASTER_SIZE[0],
            "vertical_pixels": PATCH_SIZE[1] * 2 - MASTER_SIZE[1],
            "blend": (
                "minimum-error native-pixel seam; no interpolation or scaling; "
                "final runtime tiles are lossless non-overlapping crops"
            ),
            "top_row_seam": {
                "min_x": int(top_seam.min()),
                "max_x": int(top_seam.max()),
                "mean_cost": round(top_error, 4),
            },
            "bottom_row_seam": {
                "min_x": int(bottom_seam.min()),
                "max_x": int(bottom_seam.max()),
                "mean_cost": round(bottom_error, 4),
            },
            "row_join_seam": {
                "min_y": int(row_seam.min()),
                "max_y": int(row_seam.max()),
                "mean_cost": round(row_error, 4),
            },
        },
        "seams": {
            "vertical_x_896_mae": round(boundary_error(master, "vertical", 896), 4),
            "vertical_x_1152_mae": round(boundary_error(master, "vertical", 1152), 4),
            "horizontal_y_505_mae": round(boundary_error(master, "horizontal", 505), 4),
            "horizontal_y_648_mae": round(boundary_error(master, "horizontal", 648), 4),
        },
        "difference": {
            "path": difference_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(difference_path),
        },
        "audit_board": {
            "path": board_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(board_path),
        },
    }
    (pass_dir / f"screen_{screen}_native_master_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--screen", choices=("a", "b"), required=True)
    prepare_parser.add_argument("--concept", type=Path, required=True)
    prepare_parser.add_argument("--pass-dir", type=Path, required=True)
    context_parser = subparsers.add_parser("prepare-context")
    context_parser.add_argument("--screen", choices=("a", "b"), required=True)
    context_parser.add_argument("--concept", type=Path, required=True)
    context_parser.add_argument("--pass-dir", type=Path, required=True)
    repair_context_parser = subparsers.add_parser("prepare-repair")
    repair_context_parser.add_argument("--screen", choices=("a", "b"), required=True)
    repair_context_parser.add_argument("--master", type=Path, required=True)
    repair_context_parser.add_argument("--pass-dir", type=Path, required=True)
    repair_parser = subparsers.add_parser("apply-repair")
    repair_parser.add_argument("--screen", choices=("a", "b"), required=True)
    repair_parser.add_argument("--base-master", type=Path, required=True)
    repair_parser.add_argument("--top", type=Path, required=True)
    repair_parser.add_argument("--bottom", type=Path, required=True)
    repair_parser.add_argument("--pass-dir", type=Path, required=True)
    repair_parser.add_argument("--output-master", type=Path, required=True)
    lower_right_context_parser = subparsers.add_parser("prepare-lower-right")
    lower_right_context_parser.add_argument(
        "--screen", choices=("a", "b"), required=True
    )
    lower_right_context_parser.add_argument("--master", type=Path, required=True)
    lower_right_context_parser.add_argument("--pass-dir", type=Path, required=True)
    lower_right_parser = subparsers.add_parser("apply-lower-right")
    lower_right_parser.add_argument("--screen", choices=("a", "b"), required=True)
    lower_right_parser.add_argument("--base-master", type=Path, required=True)
    lower_right_parser.add_argument("--generated", type=Path, required=True)
    lower_right_parser.add_argument("--pass-dir", type=Path, required=True)
    lower_right_parser.add_argument("--output-master", type=Path, required=True)
    assemble_parser = subparsers.add_parser("assemble")
    assemble_parser.add_argument("--screen", choices=("a", "b"), required=True)
    assemble_parser.add_argument("--concept", type=Path, required=True)
    assemble_parser.add_argument("--tl", type=Path, required=True)
    assemble_parser.add_argument("--tr", type=Path, required=True)
    assemble_parser.add_argument("--bl", type=Path, required=True)
    assemble_parser.add_argument("--br", type=Path, required=True)
    assemble_parser.add_argument("--pass-dir", type=Path, required=True)
    assemble_parser.add_argument("--output-master", type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.command == "prepare":
        prepare(arguments.screen, arguments.concept, arguments.pass_dir)
    elif arguments.command == "prepare-context":
        prepare_context(arguments.screen, arguments.concept, arguments.pass_dir)
    elif arguments.command == "prepare-repair":
        prepare_repair(arguments.screen, arguments.master, arguments.pass_dir)
    elif arguments.command == "apply-repair":
        apply_repair(
            arguments.screen,
            arguments.base_master,
            arguments.top,
            arguments.bottom,
            arguments.pass_dir,
            arguments.output_master,
        )
    elif arguments.command == "prepare-lower-right":
        prepare_lower_right(arguments.screen, arguments.master, arguments.pass_dir)
    elif arguments.command == "apply-lower-right":
        apply_lower_right(
            arguments.screen,
            arguments.base_master,
            arguments.generated,
            arguments.pass_dir,
            arguments.output_master,
        )
    else:
        generated = {
            "tl": arguments.tl,
            "tr": arguments.tr,
            "bl": arguments.bl,
            "br": arguments.br,
        }
        assemble(
            arguments.screen,
            arguments.concept,
            generated,
            arguments.pass_dir,
            arguments.output_master,
        )


if __name__ == "__main__":
    # Imported late so prepare mode has minimal dependencies and the analyzer
    # reports accidental use clearly.
    from PIL import ImageFilter

    main()
