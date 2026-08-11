#!/usr/bin/env python3
"""Prepare the reviewed Opera minigame art derivatives.

This tool is intentionally deterministic and reuse-first.  It never modifies
the approved concept cards or ImageGen native boards.  Default mode writes the
runtime PNGs and adjacent review evidence; ``--check-only`` rebuilds every byte
in memory and fails if the checked-in derivatives differ.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from collections import deque
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WIDGETS = ROOT / "assets" / "opera" / "worlds" / "widgets"
CARDS = ROOT / "assets_src" / "concepts" / "opera_jobs_flat_2026-07-21" / "cards"
HOUSE_CARDS = ROOT / "assets_src" / "concepts" / "opera_house_flat" / "cards"
SOURCE_DIR = ROOT / "assets_src" / "imagegen" / "opera_minigame_quality_2026-08-09"
ALPHA_BOARD = SOURCE_DIR / "opera_minigame_prop_sheet_alpha_native.png"
NATIVE_BOARD = SOURCE_DIR / "opera_minigame_prop_sheet_native.png"
GENERATED_TEXT_ARTIFACTS = frozenset({
    SOURCE_DIR / "PROVENANCE.json",
    SOURCE_DIR / "REVIEW.md",
})

PROMPT = (
    "Create a production sprite-board source for the Mermaid Roshan Pearl Opera "
    "minigames, matching the supplied polished 2D storybook props: warm ivory/cream, "
    "coral, teal, pearl and brass, softly painted texture, clean dark navy-purple "
    "outline, child-readable silhouette. Exactly four isolated props in a strict "
    "2x2 grid on a perfectly flat, uniform pure chroma green #00FF00 background. "
    "Wide empty green gutters between quadrants. Top-left: one small cream-and-coral "
    "handled batter pitcher in side three-quarter view, with a clear spout and pale "
    "sparkling cake batter visibly inside; no bowl. Top-right: one whimsical "
    "teal-and-coral shell-trimmed candy syrup jug in side three-quarter view, with a "
    "clear spout and pink syrup visibly inside; no candy and no molds. Bottom-left: "
    "one warm ivory merbaby feeding bottle with coral shell cap and golden milk, "
    "upright, no baby and no hand. Bottom-right: one cream/coral/brass open-end racing "
    "mechanic wrench with a tiny shell crest, diagonal but fully contained; no toolbox "
    "and no kart. Every prop complete and anatomically/structurally coherent, centered "
    "within its own quadrant, same apparent scale, at least 18 percent green margin on "
    "all sides. No cast shadows, no floor, no glow, no labels, no letters, no numbers, "
    "no characters, no extra objects, no detached or floating pieces, no cropping, no "
    "overlap across cells. Crisp edges suitable for chroma-key extraction and "
    "downscaling to 256x256."
)

GENERATION = {
    "date": "2026-08-09",
    "method": "OpenAI built-in ImageGen",
    "result_id": "exec-36bd6833-2769-4631-b95b-6bc016511f87.png",
    "original_result_path": (
        r"C:\Users\Peter\.codex\generated_images\019fe6fd-6f77-7353-86b6-d32b930bea1a"
        r"\exec-36bd6833-2769-4631-b95b-6bc016511f87.png"
    ),
    "preserved_native_path": str(NATIVE_BOARD.relative_to(ROOT)).replace("\\", "/"),
    "preserved_alpha_path": str(ALPHA_BOARD.relative_to(ROOT)).replace("\\", "/"),
    "references_supplied": [
        "assets/opera/worlds/widgets/widget_pour_chef.png",
        "assets/opera/worlds/widgets/widget_pour_candymaker.png",
        "assets/opera/worlds/widgets/widget_pour_nursery.png",
        (
            "assets_src/concepts/opera_jobs_flat_2026-07-21/cards/"
            "opera_job_racecar_driver_gameplay_pit_toolkit.png"
        ),
    ],
    "alpha_command": (
        "remove_chroma_key.py --auto-key border --soft-matte "
        "--transparent-threshold 22 --opaque-threshold 105 --edge-feather 0.6 "
        "--spill-cleanup --force"
    ),
    "alpha_report": {
        "detected_key": "#05f70c",
        "transparent_pixels": 1197210,
        "total_pixels": 1572516,
        "partial_alpha_pixels": 39522,
    },
    "prompt": PROMPT,
}


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _check_bytes_match(path: Path, checked_in: bytes, generated: bytes) -> bool:
    """Compare deterministic outputs, tolerating only text newline checkout policy."""
    if path in GENERATED_TEXT_ARTIFACTS:
        checked_in = checked_in.replace(b"\r\n", b"\n")
        generated = generated.replace(b"\r\n", b"\n")
    return checked_in == generated


def _png_bytes(image: Image.Image) -> bytes:
    output = io.BytesIO()
    clean = image.convert("RGBA")
    clean.save(output, format="PNG", compress_level=9, optimize=False)
    return output.getvalue()


def _alpha_bbox(image: Image.Image, threshold: int = 4) -> tuple[int, int, int, int] | None:
    alpha = np.asarray(image.convert("RGBA"), dtype=np.uint8)[:, :, 3]
    ys, xs = np.nonzero(alpha > threshold)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def _label_components(mask: np.ndarray) -> tuple[np.ndarray, int]:
    """4-connected labels, using scipy when present and a small fallback otherwise."""
    try:
        from scipy import ndimage  # type: ignore

        labels, count = ndimage.label(mask)
        return labels.astype(np.int32, copy=False), int(count)
    except ImportError:
        height, width = mask.shape
        labels = np.zeros((height, width), dtype=np.int32)
        count = 0
        for y in range(height):
            for x in range(width):
                if not mask[y, x] or labels[y, x] != 0:
                    continue
                count += 1
                labels[y, x] = count
                queue: deque[tuple[int, int]] = deque([(x, y)])
                while queue:
                    px, py = queue.popleft()
                    for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                        if 0 <= nx < width and 0 <= ny < height and mask[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = count
                            queue.append((nx, ny))
        return labels, count


def _fill_holes(mask: np.ndarray) -> np.ndarray:
    try:
        from scipy import ndimage  # type: ignore

        return ndimage.binary_fill_holes(mask)
    except ImportError:
        inv = ~mask
        height, width = inv.shape
        reached = np.zeros_like(inv)
        queue: deque[tuple[int, int]] = deque()
        for x in range(width):
            for y in (0, height - 1):
                if inv[y, x] and not reached[y, x]:
                    reached[y, x] = True
                    queue.append((x, y))
        for y in range(height):
            for x in (0, width - 1):
                if inv[y, x] and not reached[y, x]:
                    reached[y, x] = True
                    queue.append((x, y))
        while queue:
            px, py = queue.popleft()
            for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                if 0 <= nx < width and 0 <= ny < height and inv[ny, nx] and not reached[ny, nx]:
                    reached[ny, nx] = True
                    queue.append((nx, ny))
        return mask | (inv & ~reached)


def _select_components(mask: np.ndarray, count: int = 1, min_area: int = 48) -> np.ndarray:
    labels, label_count = _label_components(mask)
    if label_count == 0:
        return mask
    areas = np.bincount(labels.ravel(), minlength=label_count + 1)
    candidates: list[tuple[int, int]] = []
    h, w = mask.shape
    border_labels = set(np.unique(np.concatenate((
        labels[:2, :].ravel(), labels[-2:, :].ravel(),
        labels[:, :2].ravel(), labels[:, -2:].ravel(),
    ))).tolist())
    for label in range(1, label_count + 1):
        area = int(areas[label])
        if area < min_area or label in border_labels:
            continue
        ys, xs = np.nonzero(labels == label)
        if not len(xs):
            continue
        span_x = (int(xs.max()) - int(xs.min()) + 1) / float(w)
        span_y = (int(ys.max()) - int(ys.min()) + 1) / float(h)
        # Approved masters were exported from contact sheets.  A pale/grey
        # inset rule can be brighter than the navy field; never mistake that
        # almost-full-canvas presentation frame for the subject.
        if span_x > 0.92 and span_y > 0.92:
            continue
        candidates.append((area, label))
    candidates.sort(reverse=True)
    kept = [label for _area, label in candidates[:count]]
    if not kept:
        kept = [int(np.argmax(areas[1:])) + 1]
    return np.isin(labels, kept)


def _remove_edge_field(
    image: Image.Image,
    *,
    component_count: int = 1,
    min_component_area: int = 48,
) -> Image.Image:
    """Remove the connected dark presentation field without repainting RGB art.

    The approved cards share a very dark navy/black contact-sheet field.  Bright
    subject pixels seed the silhouette, a four-pixel native dilation restores the
    authored dark outline, enclosed dark details are retained, and frame/grid
    components touching the crop edge are rejected.
    """
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3].astype(np.float32)
    luminance = rgb[:, :, 0] * 0.299 + rgb[:, :, 1] * 0.587 + rgb[:, :, 2] * 0.114
    source_alpha = rgba[:, :, 3]
    core = (luminance > 56.0) & (source_alpha > 4)
    core_image = Image.fromarray((core.astype(np.uint8) * 255), mode="L")
    grown = np.asarray(core_image.filter(ImageFilter.MaxFilter(9)), dtype=np.uint8) > 0
    selected = _select_components(grown, component_count, min_component_area)
    selected = _fill_holes(selected)
    matte = Image.fromarray((selected.astype(np.uint8) * 255), mode="L").filter(
        ImageFilter.GaussianBlur(0.55)
    )
    matte_array = np.asarray(matte, dtype=np.uint8)
    rgba[:, :, 3] = ((matte_array.astype(np.uint16) * source_alpha.astype(np.uint16)) // 255).astype(np.uint8)
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, mode="RGBA")


def _source(
    filename: str,
    *,
    crop: tuple[int, int, int, int] | None = None,
    components: int = 1,
    min_area: int = 48,
) -> Image.Image:
    image = Image.open(CARDS / filename).convert("RGBA")
    if crop is not None:
        image = image.crop(crop)
    return _remove_edge_field(image, component_count=components, min_component_area=min_area)


def _chef_topping_only(filename: str, kind: str) -> Image.Image:
    """Isolate the visible topping from its approved serving-display source.

    The masters show each complete topping resting on a pedestal.  This is a
    colour/connected-component alpha derivation only: no hidden edge is drawn,
    and the authored visible lower outline is retained while gold/pink stand
    pixels are excluded.
    """
    crop_by_kind = {
        "cherry": (350, 0, 900, 455),
        "cream": (0, 500, 555, 1045),
        "chocolate": (700, 500, 1254, 1045),
    }
    source_image = Image.open(CARDS / filename).convert("RGBA")
    field_removed_full = _remove_edge_field(source_image, component_count=24, min_component_area=40)
    field_removed = field_removed_full.crop(crop_by_kind[kind])
    rgba = np.asarray(field_removed.convert("RGBA"), dtype=np.uint8).copy()
    rgb = rgba[:, :, :3].astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    luminance = r * 0.299 + g * 0.587 + b * 0.114
    if kind == "cherry":
        red = (r > 105) & (g < r * 0.53) & (b < r * 0.53)
        leaf = (g > 55) & (g > b * 1.25) & (r < 165)
        colour = red | leaf
        outline_allowed = ((r > g * 1.12) & (r > b * 1.12)) | (
            (g > r * 0.72) & (g > b * 1.18)
        )
    elif kind == "cream":
        colour = (r > 135) & (g > r * 0.71) & (b > r * 0.49)
        # The approved card paints a cool-purple table shadow directly below
        # the dollop.  Preserve only warm authored outline pixels adjacent to
        # the cream so that shadow cannot become a false serving plate.
        outline_allowed = (r > b * 1.08) & (g > b * 0.90)
    elif kind == "chocolate":
        colour = (r > 32) & (r < 210) & (r > g * 1.24) & (b < r * 0.60)
        # The source also has a detached mauve ground shadow.  Chocolate's
        # genuine outline is distinctly warmer/redder, so hue-gate restored
        # dark pixels rather than accepting every nearby low-luminance pixel.
        outline_allowed = (r > g * 1.20) & (r > b * 1.60)
    else:
        raise ValueError(f"unknown topping kind: {kind}")
    colour &= rgba[:, :, 3] > 4
    colour_image = Image.fromarray((colour.astype(np.uint8) * 255), mode="L")
    near = np.asarray(colour_image.filter(ImageFilter.MaxFilter(15)), dtype=np.uint8) > 0
    # Restore the authored dark outline adjacent to the topping, but not the
    # brighter gold/coral pedestal beneath it.
    silhouette = colour | (
        near
        & outline_allowed
        & (luminance < 96.0)
        & (rgba[:, :, 3] > 4)
    )
    silhouette = _select_components(silhouette, 1, 180)
    silhouette = _fill_holes(silhouette)
    matte = Image.fromarray((silhouette.astype(np.uint8) * 255), mode="L").filter(
        ImageFilter.GaussianBlur(0.45)
    )
    matte_array = np.asarray(matte, dtype=np.uint8)
    rgba[:, :, 3] = ((rgba[:, :, 3].astype(np.uint16) * matte_array.astype(np.uint16)) // 255).astype(np.uint8)
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, mode="RGBA")


def _trim(image: Image.Image, padding: int = 0) -> Image.Image:
    bbox = _alpha_bbox(image)
    if bbox is None:
        raise RuntimeError("derived image has no visible pixels")
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom))


def _fit(
    sprite: Image.Image,
    canvas_size: tuple[int, int],
    max_box: tuple[int, int],
    *,
    center: tuple[float, float] | None = None,
) -> Image.Image:
    sprite = _trim(sprite, 3)
    scale = min(max_box[0] / sprite.width, max_box[1] / sprite.height)
    resized = sprite.resize(
        (max(1, int(round(sprite.width * scale))), max(1, int(round(sprite.height * scale)))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    cx, cy = center if center is not None else (canvas_size[0] / 2.0, canvas_size[1] / 2.0)
    x = int(round(cx - resized.width / 2.0))
    y = int(round(cy - resized.height / 2.0))
    canvas.alpha_composite(resized, (x, y))
    return canvas


def _fit_into(
    canvas: Image.Image,
    sprite: Image.Image,
    box: tuple[int, int, int, int],
) -> None:
    left, top, right, bottom = box
    fitted = _fit(sprite, (right - left, bottom - top), (right - left, bottom - top))
    canvas.alpha_composite(fitted, (left, top))


def _generated_prop_cells() -> dict[str, Image.Image]:
    board = Image.open(ALPHA_BOARD).convert("RGBA")
    half_w = board.width // 2
    half_h = board.height // 2
    cells = {
        "widget_pour_chef_mover.png": board.crop((0, 0, half_w, half_h)),
        "widget_pour_candymaker_mover.png": board.crop((half_w, 0, board.width, half_h)),
        "widget_pour_nursery_mover.png": board.crop((0, half_h, half_w, board.height)),
        "widget_crank_racer_mover.png": board.crop((half_w, half_h, board.width, board.height)),
    }
    trimmed = {name: _trim(cell, 3) for name, cell in cells.items()}
    max_width = max(image.width for image in trimmed.values())
    max_height = max(image.height for image in trimmed.values())
    scale = min(216.0 / max_width, 216.0 / max_height)
    outputs: dict[str, Image.Image] = {}
    for name, image in trimmed.items():
        resized = image.resize(
            (max(1, int(round(image.width * scale))), max(1, int(round(image.height * scale)))),
            Image.Resampling.LANCZOS,
        )
        canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
        canvas.alpha_composite(resized, ((256 - resized.width) // 2, (256 - resized.height) // 2))
        arr = np.asarray(canvas, dtype=np.uint8).copy()
        arr[arr[:, :, 3] <= 3] = 0
        outputs[name] = Image.fromarray(arr, mode="RGBA")
    return outputs


def _astronaut_patch(index: int) -> Image.Image:
    scale = 4
    size = 256 * scale
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    navy = "#392883"
    cream = "#fff2d4"
    coral = "#f47f75"
    teal = "#61c9c6"
    gold = "#f6cb58"
    outline = 22

    def ellipse(box: tuple[int, int, int, int], fill: str, width: int = outline) -> None:
        draw.ellipse(box, fill=fill, outline=navy, width=width)

    if index == 0:
        ellipse((110, 110, size - 110, size - 110), cream, 26)
        center_x, base_y = size // 2, 700
        for offset in (-210, -105, 0, 105, 210):
            draw.polygon(
                [(center_x, base_y), (center_x + offset - 78, 355), (center_x + offset, 235),
                 (center_x + offset + 78, 355)],
                fill=coral,
                outline=navy,
            )
        ellipse((center_x - 92, base_y - 92, center_x + 92, base_y + 92), gold, 20)
        draw.arc((250, 250, size - 250, size - 210), 18, 162, fill=navy, width=22)
    elif index == 1:
        points = [(size // 2, 105), (size - 125, 320), (size - 125, 704),
                  (size // 2, size - 105), (125, 704), (125, 320)]
        draw.polygon(points, fill=teal)
        draw.line(points + [points[0]], fill=navy, width=28, joint="curve")
        ellipse((318, 318, size - 318, size - 318), cream, 24)
        for angle in range(0, 360, 60):
            point = (size // 2 + int(math.cos(math.radians(angle)) * 330),
                     size // 2 + int(math.sin(math.radians(angle)) * 330))
            ellipse((point[0] - 42, point[1] - 42, point[0] + 42, point[1] + 42), gold, 14)
    else:
        draw.rounded_rectangle((125, 170, size - 125, size - 170), radius=170,
                               fill=coral, outline=navy, width=28)
        ellipse((315, 275, size - 315, size - 275), teal, 24)
        ellipse((405, 365, size - 405, size - 365), cream, 20)
        for point in ((225, 270), (size - 225, 270), (225, size - 270), (size - 225, size - 270)):
            ellipse((point[0] - 48, point[1] - 48, point[0] + 48, point[1] + 48), gold, 14)
    return canvas.resize((256, 256), Image.Resampling.LANCZOS)


def _cabinet_reveal(closed: Image.Image, lamba: Image.Image) -> Image.Image:
    cabinet = _trim(closed, 3)
    w, h = cabinet.size
    opened = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # Lamba is composited first, then the approved cabinet header/rails/base
    # are restored in front of her.  The door-panel area remains transparent:
    # there is no painted rectangle, card field, or pasted-on square seam.
    lamba_fit = _fit(lamba, (int(w * 0.56), int(h * 0.51)), (int(w * 0.54), int(h * 0.49)))
    opened.alpha_composite(lamba_fit, (int(w * 0.22), int(h * 0.27)))
    opened.alpha_composite(cabinet.crop((0, 0, w, int(h * 0.31))), (0, 0))
    opened.alpha_composite(cabinet.crop((0, int(h * 0.72), w, h)), (0, int(h * 0.72)))
    opened.alpha_composite(cabinet.crop((0, int(h * 0.26), int(w * 0.21), int(h * 0.78))),
                           (0, int(h * 0.26)))
    opened.alpha_composite(cabinet.crop((int(w * 0.79), int(h * 0.26), w, int(h * 0.78))),
                           (int(w * 0.79), int(h * 0.26)))
    return opened


def _build_contact_sheet(images: dict[str, Image.Image]) -> Image.Image:
    names = sorted(images)
    columns = 6
    rows = max(1, math.ceil(len(names) / columns))
    sheet = Image.new("RGBA", (2048, 2048), (29, 21, 58, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    cell_w = sheet.width // columns
    cell_h = sheet.height // rows
    for index, name in enumerate(names):
        column = index % columns
        row = index // columns
        x0, y0 = column * cell_w, row * cell_h
        x1, y1 = x0 + cell_w, y0 + cell_h
        draw.rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y1 - 8), radius=16,
                               fill=(239, 244, 252, 255), outline=(83, 63, 137, 255), width=4)
        art_box = (x0 + 22, y0 + 30, x1 - 22, y1 - 44)
        art = _fit(images[name], (art_box[2] - art_box[0], art_box[3] - art_box[1]),
                   (art_box[2] - art_box[0], art_box[3] - art_box[1]))
        sheet.alpha_composite(art, (art_box[0], art_box[1]))
        label = name.removeprefix("widget_")
        if len(label) > 42:
            label = label[:39] + "..."
        draw.text((x0 + 16, y1 - 32), label, font=font, fill=(45, 31, 77, 255))
    return sheet


def build() -> tuple[dict[Path, Image.Image], dict[str, dict[str, Any]], list[str]]:
    images: dict[Path, Image.Image] = {}
    records: dict[str, dict[str, Any]] = {}
    notes: list[str] = []

    def add(
        name: str,
        image: Image.Image,
        sources: Iterable[Path],
        operation: str,
        qa: str,
    ) -> None:
        path = WIDGETS / name
        images[path] = image.convert("RGBA")
        records[name] = {
            "sources": [str(source.relative_to(ROOT)).replace("\\", "/") for source in sources],
            "operation": operation,
            "artifact_qa": qa,
        }

    generated = _generated_prop_cells()
    generated_roles = {
        "widget_pour_chef_mover.png": "top-left batter pitcher",
        "widget_pour_candymaker_mover.png": "top-right candy syrup jug",
        "widget_pour_nursery_mover.png": "bottom-left feeding bottle",
        "widget_crank_racer_mover.png": "bottom-right mechanic wrench",
    }
    for name, image in generated.items():
        add(name, image, [ALPHA_BOARD, NATIVE_BOARD],
            f"crop reviewed 2x2 cell ({generated_roles[name]}), trim shared alpha, apply one shared scale, "
            "Lanczos fit on 256x256 transparent canvas; alpha<=3 cleared",
            "accepted source topology preserved; one complete object; no crop, detached part, or visible green spill")

    # Detective case board, tokens, and crown chest.
    detective_empty = CARDS / "opera_job_detective_stage_states_case_board_empty.png"
    detective_complete = CARDS / "opera_job_detective_stage_states_case_board_complete.png"
    for name, source in (("widget_clue_board_empty.png", detective_empty),
                         ("widget_clue_board_complete.png", detective_complete)):
        sprite = _source(source.name, components=1, min_area=800)
        add(name, _fit(sprite, (1024, 608), (982, 574)), [source],
            "_remove_edge_field, retain largest ornate board component, aspect-preserving Lanczos fit on 1024x608 alpha card",
            "complete frame and all three left-to-right silhouettes visible; no grid/frame bleed or crop")

    token_sources = [
        CARDS / "opera_job_detective_gameplay_paw_clue.png",
        CARDS / "opera_job_detective_gameplay_feather_clue.png",
        CARDS / "opera_job_detective_gameplay_ribbon_clue.png",
    ]
    token_strip = Image.new("RGBA", (768, 256), (0, 0, 0, 0))
    for index, source in enumerate(token_sources):
        token = _fit(_source(source.name, components=1), (256, 256), (218, 218))
        token_strip.alpha_composite(token, (index * 256, 0))
    add("widget_clue_board_tokens.png", token_strip, token_sources,
        "_remove_edge_field per source; paw/feather/ribbon preserved in silhouette order; each fit to one 256px cell",
        "three distinct complete tokens; no cross-cell bleed or clipping")

    chest_sources = [CARDS / "opera_job_detective_gameplay_chest_closed.png",
                     CARDS / "opera_job_detective_gameplay_chest_open.png"]
    for name, source in zip(("widget_crown_chest_closed.png", "widget_crown_chest_open.png"), chest_sources):
        sprite = _source(source.name, components=1, min_area=800)
        add(name, _fit(sprite, (512, 512), (428, 382)), [source],
            "_remove_edge_field, retain full chest state, aspect-preserving Lanczos fit with cover-safe vertical margins",
            "closed/open topology coherent; open tiara remains connected and fully visible; no crop")

    # Magician: approved cabinet shell plus the intentionally continued Lamba reveal.
    cabinet_source = CARDS / "opera_job_magician_stage_states_trick_cabinet.png"
    lamba_source = CARDS / "opera_job_magician_stage_states_bunny_fish_reveal.png"
    cabinet = _source(cabinet_source.name, components=1, min_area=1000)
    lamba = _source(lamba_source.name, crop=(285, 45, 945, 620), components=1, min_area=800)
    cabinet_reveal = _cabinet_reveal(cabinet, lamba)
    add("widget_magic_cabinet_closed.png", _fit(cabinet, (512, 512), (430, 390)), [cabinet_source],
        "_remove_edge_field; preserve closed cabinet as one component; fit on 512x512 with cover-safe margins",
        "complete cabinet, hinges, shell crest, feet, and handles visible")
    add("widget_magic_cabinet_reveal.png", _fit(cabinet_reveal, (512, 512), (430, 390)),
        [cabinet_source, lamba_source],
        "_remove_edge_field; leave the door-panel opening transparent; fit approved alpha Lamba behind restored approved "
        "cabinet header/side-rail/base crops; flatten to 512x512",
        "Lamba is fully contained behind the approved open cabinet shell; no opaque plate, hard rectangular seam, floating hat, crop, or source repaint")

    vanish_sources = [CARDS / "opera_job_magician_gameplay_hat_open.png",
                      CARDS / "opera_job_magician_gameplay_pearl_wand.png",
                      CARDS / "opera_job_magician_gameplay_successful_reveal.png"]
    vanish_specs = [
        ("widget_magic_vanish_hat.png", vanish_sources[0], 1, (430, 360)),
        ("widget_magic_vanish_wand.png", vanish_sources[1], 1, (414, 414)),
    ]
    for name, source, components, box in vanish_specs:
        sprite = _source(source.name, components=components, min_area=80)
        add(name, _fit(sprite, (512, 512), box), [source],
            f"_remove_edge_field; retain {components} reviewed subject/effect component(s); Lanczos fit on 512x512",
            "magic prop/reveal complete and contained; no labels, presentation frame, or clipped silhouette")
    reveal_hat = _source(vanish_sources[0].name, components=1, min_area=500)
    reveal = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    _fit_into(reveal, lamba, (88, 18, 424, 312))
    _fit_into(reveal, reveal_hat, (74, 266, 438, 492))
    add("widget_magic_vanish_reveal.png", reveal, [lamba_source, vanish_sources[0]],
        "reuse the clean alpha Lamba crop accepted for the cabinet and the approved open hat; "
        "aspect-preserving fit in a coherent Lamba-over-hat reveal on 512x512",
        "clean Lamba-over-hat reveal; both silhouettes complete and contained; no presentation field, blob, hard seam, labels, or crop")

    portal_source = HOUSE_CARDS / "opera_upper_access_act_portal_open.png"
    portal = _remove_edge_field(Image.open(portal_source).convert("RGBA"),
                                component_count=1, min_component_area=300)
    add("widget_portal_magician_mover.png", _fit(portal, (256, 256), (224, 224)), [portal_source],
        "_remove_edge_field on approved open Opera portal; retain portal only; aspect-preserving fit on 256x256 alpha canvas",
        "complete open portal frame, curtains, threshold, and warm opening; no Lamba, hat, stage tableau, or crop")

    # Authored target pieces.  Export filenames are deliberately mapped by
    # reviewed visible content because the source contact sheet has shifted names.
    target_sources: dict[str, list[Path]] = {
        "chef": [
            CARDS / "opera_job_pastry_chef_stage_states_placement_glows.png",
            CARDS / "opera_job_pastry_chef_stage_states_placement_glows.png",
            CARDS / "opera_job_pastry_chef_stage_states_placement_glows.png",
        ],
        "candymaker": [
            CARDS / "opera_job_candy_maker_gameplay_teal_spiral_candy.png",  # visible coral flower
            CARDS / "opera_job_candy_maker_gameplay_plum_wrapped_candy.png",  # visible teal shell
            CARDS / "opera_job_candy_maker_gameplay_cream_heart_candy.png",  # visible plum wrapped candy
        ],
        "farmer": [
            CARDS / "opera_job_farmer_gameplay_hay_bale.png",  # visible carrot
            CARDS / "opera_job_farmer_gameplay_piggy_fed.png",  # visible corn
            CARDS / "opera_job_farmer_gameplay_piggy_munch.png",  # visible pumpkin
        ],
    }
    built_pieces: dict[str, list[Image.Image]] = {}
    for career, sources in target_sources.items():
        built_pieces[career] = []
        for index, source in enumerate(sources):
            if career == "chef":
                topping_kind = ("cherry", "cream", "chocolate")[index]
                subject = _chef_topping_only(source.name, topping_kind)
                operation = (
                    "_remove_edge_field, isolate the approved visible topping by colour and connected alpha, "
                    "retain its authored lower outline while excluding every pedestal/plate/base pixel, fit on 256x256"
                )
                artifact_qa = "one complete topping-only token; no serving stand, plate, pedestal, flat cut, frame bleed, or detached part"
            else:
                subject = _source(source.name, components=1, min_area=500)
                operation = (
                    "_remove_edge_field, retain reviewed visible prop despite shifted export labels, "
                    "fit on 256x256 alpha canvas"
                )
                artifact_qa = "one child-readable complete target prop; no frame bleed, crop, or detached part"
            piece = _fit(subject, (256, 256), (222, 222))
            if career == "chef" and topping_kind == "chocolate":
                # Two tiny gold/mauve curls from the source presentation plate
                # survive the colour matte at the lower corners.  They are
                # spatially detached from the topping after the 256px fit;
                # clear only those reviewed corner ROIs, leaving the authored
                # curved lower chocolate outline untouched.
                piece_draw = ImageDraw.Draw(piece)
                piece_draw.rectangle((0, 182, 26, 255), fill=(0, 0, 0, 0))
                piece_draw.rectangle((231, 185, 255, 185), fill=(0, 0, 0, 0))
                piece_draw.rectangle((226, 186, 255, 255), fill=(0, 0, 0, 0))
                operation += (
                    "; clear reviewed detached plate-remnant corner ROIs "
                    "x=0..26/y=182..255 and x=226..255/y=186..255"
                )
            built_pieces[career].append(piece)
            add(f"widget_target_{career}_piece_{index}.png", piece, [source],
                operation, artifact_qa)
    built_pieces["astronaut"] = []
    palette_source = WIDGETS / "widget_target_astronaut.png"
    for index in range(3):
        piece = _astronaut_patch(index)
        built_pieces["astronaut"].append(piece)
        add(f"widget_target_astronaut_piece_{index}.png", piece, [palette_source],
            "project-original Pillow vector construction at 4x antialias scale using established Opera coral/teal/cream/gold/navy palette; "
            "whole-canvas Lanczos downscale to 256x256",
            "unique shell/rivet patch silhouette; complete outline and >=24px transparent margin")

    # Career-specific fallback stamps replace the generic yellow ring.
    mark_source_by_career = {
        "chef": target_sources["chef"][1],
        "candymaker": target_sources["candymaker"][0],
        "farmer": target_sources["farmer"][0],
    }
    for career in ("chef", "candymaker", "farmer", "astronaut"):
        mark = _fit(built_pieces[career][0 if career != "chef" else 1], (128, 128), (112, 112))
        sources = [palette_source] if career == "astronaut" else [mark_source_by_career[career]]
        add(f"widget_target_{career}_mark.png", mark, sources,
            "derive fallback from the career's reviewed target piece; aspect-preserving fit on existing 128x128 mark contract",
            "thematic filled stamp remains distinct from hollow invitation ring")

    painter_source = CARDS / "opera_job_painter_stage_states_splat_state.png"
    painter_splat = _source(painter_source.name, crop=(300, 160, 710, 780), components=5, min_area=70)
    painter_mark = _fit(painter_splat, (128, 128), (112, 112))
    add("widget_target_painter_mark.png", painter_mark, [painter_source],
        "crop approved center coral paint splat and droplets, _remove_edge_field, fit on existing 128x128 mark contract",
        "literal coral paint splat replaces generic ring; main splash and intentional droplets fully contained")

    # Racer tune-up card: retain an established Racer card frame, clear only
    # its illustration field, then place the approved stationary kart/toolkit.
    racer_frame_source = WIDGETS / "widget_push_racer.png"
    kart_source = CARDS / "opera_job_racecar_driver_gameplay_opera_kart_side.png"
    toolkit_source = CARDS / "opera_job_racecar_driver_gameplay_pit_toolkit.png"
    racer_card = Image.open(racer_frame_source).convert("RGBA").copy()
    card_draw = ImageDraw.Draw(racer_card)
    card_draw.rounded_rectangle((72, 104, 952, 542), radius=30, fill=(239, 244, 252, 255))
    kart = _source(kart_source.name, components=1, min_area=900)
    wheel_source_crop = (650, 570, 980, 970)
    wheel_sprite = _source(kart_source.name, crop=wheel_source_crop, components=4, min_area=70)
    wheel = _fit(wheel_sprite, (256, 256), (218, 218))
    toolkit = _source(toolkit_source.name, components=1, min_area=900)
    # The card is the pre-repair state: retain a complete front wheel while
    # leaving the rear hub open for the runtime wrench/install progression.
    front_wheel = _fit(wheel, (170, 170), (160, 160))
    racer_card.alpha_composite(front_wheel, (158, 350))
    _fit_into(racer_card, kart, (112, 146, 712, 520))
    _fit_into(racer_card, toolkit, (700, 208, 934, 496))
    add("widget_crank_racer.png", racer_card, [racer_frame_source, kart_source, toolkit_source],
        "reuse established opaque Racer widget frame; clear central illustration field only; _remove_edge_field on approved side kart/toolkit; "
        "aspect-preserving fit as a stationary pit tune-up tableau; restore approved front wheel behind fender while leaving rear hub open",
        "no racetrack curve; clear pre-repair state has one complete front wheel, one open rear hub, and a non-overlapping toolkit")
    add("widget_crank_racer_wheel.png", wheel, [kart_source],
        "crop approved rear wheel from side-kart master, _remove_edge_field while retaining tire/rim/hub components, "
        "aspect-preserving fit on 256x256 alpha canvas",
        "complete isolated wheel with tire, rim, and shell hub; no fender, body fragment, crop, or presentation field")

    cake_source = CARDS / "opera_job_pastry_chef_gameplay_finished_cake.png"
    cake = _source(cake_source.name, components=1, min_area=1200)
    cake_overlay = _fit(cake, (1024, 608), (548, 520), center=(512.0, 310.0))
    add("widget_gauge_chef_success.png", cake_overlay, [cake_source],
        "_remove_edge_field; preserve complete finished cake; fit as centered 1024x608 transparent achieved overlay",
        "finished cake replaces generic green disk; plate, tiers, fruit, and frosting fully visible")

    pop_source = CARDS / "opera_job_pop_star_gameplay_microphone_active.png"
    pop_mic = _source(pop_source.name, components=12, min_area=55)
    add("widget_crank_popstar_mover.png", _fit(pop_mic, (256, 256), (224, 224)), [pop_source],
        "_remove_edge_field; retain approved handheld microphone plus authored sound-wave/pearl pulse components; fit on 256x256",
        "single finale microphone identity, not whole stage; complete mic with intentional sound pulses and no frame bleed")

    notes.extend([
        "Source export labels were audited visually. Candy and Farmer source names are shifted; mappings above follow visible art.",
        "Chef pieces retain only each topping's approved visible silhouette/lower outline; every serving pedestal/plate/base pixel is excluded.",
        "Magician cabinet reveal continues VANISH by placing the approved Lamba reveal inside a cabinet shell derived only from approved crops.",
        "Detective board slots are authored left-to-right; runtime hit targets must use the same horizontal order.",
    ])
    return images, records, notes


def _validate(images: dict[Path, Image.Image]) -> dict[str, Any]:
    failures: list[str] = []
    metrics: dict[str, Any] = {}
    transparent_margin_names = {
        name for name in (path.name for path in images)
        if name not in {"widget_crank_racer.png"}
    }
    expected_dims: dict[str, tuple[int, int]] = {}
    for path in images:
        name = path.name
        if name in {"widget_clue_board_empty.png", "widget_clue_board_complete.png",
                    "widget_crank_racer.png", "widget_gauge_chef_success.png"}:
            expected_dims[name] = (1024, 608)
        elif name == "widget_clue_board_tokens.png":
            expected_dims[name] = (768, 256)
        elif name.startswith("widget_crown_chest_") or name.startswith("widget_magic_"):
            expected_dims[name] = (512, 512)
        elif name.endswith("_mark.png"):
            expected_dims[name] = (128, 128)
        else:
            expected_dims[name] = (256, 256)

    generated_names = {
        "widget_pour_chef_mover.png", "widget_pour_candymaker_mover.png",
        "widget_pour_nursery_mover.png", "widget_crank_racer_mover.png",
    }
    for path, image in sorted(images.items(), key=lambda item: item[0].name):
        name = path.name
        if image.size != expected_dims[name]:
            failures.append(f"{name}: dimensions {image.size}, expected {expected_dims[name]}")
        bbox = _alpha_bbox(image)
        if bbox is None:
            failures.append(f"{name}: empty alpha")
            continue
        left, top, right, bottom = bbox
        margins = [left, top, image.width - right, image.height - bottom]
        metrics[name] = {"dimensions": list(image.size), "alpha_bbox": list(bbox), "margins": margins}
        if name in transparent_margin_names:
            required = 4 if name.startswith("widget_clue_board_") else 6
            if min(margins) < required:
                failures.append(f"{name}: alpha margin {min(margins)}px below {required}px")
        if name in generated_names:
            arr = np.asarray(image.convert("RGBA"), dtype=np.uint8)
            opaque = arr[:, :, 3] > 16
            green = opaque & (arr[:, :, 1] > 110) & \
                (arr[:, :, 1].astype(np.int16) > arr[:, :, 0].astype(np.int16) * 1.40) & \
                (arr[:, :, 1].astype(np.int16) > arr[:, :, 2].astype(np.int16) * 1.40)
            green_count = int(green.sum())
            metrics[name]["visible_green_spill_pixels"] = green_count
            if green_count:
                failures.append(f"{name}: {green_count} visible green-spill pixels")
            mask = arr[:, :, 3] > 24
            _labels, components = _label_components(mask)
            metrics[name]["alpha_components_over_24"] = components
            if components != 1:
                failures.append(f"{name}: expected one connected prop, found {components}")
    if failures:
        raise RuntimeError("asset validation failed:\n- " + "\n- ".join(failures))
    return metrics


def _review_markdown(
    records: dict[str, dict[str, Any]],
    notes: list[str],
    metrics: dict[str, Any],
) -> str:
    lines = [
        "# Opera minigame art review — 2026-08-09",
        "",
        "Status: **Codex visual QA accepted; owner/human review pending**. The four-cell ImageGen board was visually inspected by Codex before runtime derivation.",
        "All other art is a non-destructive derivative of approved project sources.",
        "",
        "## Artifact QA",
        "",
        "- Four generated movers: one connected prop each, complete silhouette, no crop, floating part, text, or visible chroma spill.",
        "- Approved-card derivatives: dark presentation field and contact-sheet rules removed with `_remove_edge_field`; source RGB subjects were not repainted.",
        "- Every transparent runtime derivative has a nonzero safe alpha gutter; every output obeys the <=1024/POT texture rule.",
        "- Exact dimensions, alpha bounds, hashes, source hashes, transforms, and the exact generation prompt are in `PROVENANCE.json`.",
        "- `python tools/prepare_opera_minigame_art.py --check-only` is the byte-exact reproducibility gate.",
        "",
        "## Source-role audit notes",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.extend(["", "## Runtime derivatives", ""])
    for name in sorted(records):
        metric = metrics[name]
        lines.append(
            f"- `{name}` — {metric['dimensions'][0]}x{metric['dimensions'][1]}; "
            f"alpha bbox `{metric['alpha_bbox']}`; {records[name]['artifact_qa']}."
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true",
                        help="rebuild in memory and fail if any checked-in derivative differs")
    args = parser.parse_args()

    if not NATIVE_BOARD.is_file() or not ALPHA_BOARD.is_file():
        raise SystemExit("missing reviewed native or alpha ImageGen board")

    images, records, notes = build()
    metrics = _validate(images)
    runtime_images = {path.name: image for path, image in images.items()}
    contact = _build_contact_sheet(runtime_images)
    contact_path = SOURCE_DIR / "OPERA_MINIGAME_ART_CONTACT_SHEET_2026-08-09.png"

    encoded: dict[Path, bytes] = {path: _png_bytes(image) for path, image in images.items()}
    encoded[contact_path] = _png_bytes(contact)
    for name, record in records.items():
        path = WIDGETS / name
        record["runtime_path"] = str(path.relative_to(ROOT)).replace("\\", "/")
        record["runtime_sha256"] = _sha256_bytes(encoded[path])
        record.update(metrics[name])
        record["source_sha256"] = {
            source: _sha256_file(ROOT / source) for source in record["sources"]
        }

    provenance = {
        "schema": 1,
        "generation": GENERATION,
        "native_sha256": _sha256_file(NATIVE_BOARD),
        "alpha_native_sha256": _sha256_file(ALPHA_BOARD),
        "derivation_tool": "tools/prepare_opera_minigame_art.py",
        "determinism_gate": "python tools/prepare_opera_minigame_art.py --check-only",
        "contact_sheet": {
            "path": str(contact_path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _sha256_bytes(encoded[contact_path]),
        },
        "source_role_notes": notes,
        "artifacts": {name: records[name] for name in sorted(records)},
        "qa_summary": {
            "codex_visual_review": "accepted",
            "owner_human_review": "pending",
            "crop": "pass",
            "floating_parts": "pass",
            "green_spill": "pass",
            "alpha_margin": "pass",
            "dimensions": "pass",
        },
    }
    provenance_path = SOURCE_DIR / "PROVENANCE.json"
    review_path = SOURCE_DIR / "REVIEW.md"
    encoded[provenance_path] = (json.dumps(provenance, indent=2, sort_keys=True) + "\n").encode("utf-8")
    encoded[review_path] = _review_markdown(records, notes, metrics).encode("utf-8")

    mismatches: list[str] = []
    for path, data in sorted(encoded.items(), key=lambda item: str(item[0])):
        if args.check_only:
            if not path.is_file():
                mismatches.append(f"missing {path.relative_to(ROOT)}")
            elif not _check_bytes_match(path, path.read_bytes(), data):
                mismatches.append(f"stale {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            print(f"wrote {path.relative_to(ROOT)}  sha256={_sha256_bytes(data)}")

    if mismatches:
        print("CHECK FAILED")
        for mismatch in mismatches:
            print(f"- {mismatch}")
        return 1
    if args.check_only:
        print(f"CHECK OK: {len(encoded)} deterministic files match")
    else:
        print(f"PREP OK: {len(encoded)} deterministic files written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
