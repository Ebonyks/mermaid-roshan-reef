#!/usr/bin/env python3
"""Extract source-owned castle objects and heal their painted footprints.

This is a deterministic ownership pass, not an art generator. Every resting
card keeps the exact RGB pixels from an approved 1024x576 room plate and adds
only an antialiased alpha mask. The existing clean room background is used as
the parent plate so previously separated objects stay separated; all newly
claimed V4 footprints are healed together in one production pass.

Outputs are versioned under ``interactions_v4``. Approved room composites,
existing cards, and existing clean backgrounds are read-only inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy.ndimage import label
from skimage.filters import sobel
from skimage.segmentation import watershed


CANVAS = (1024, 576)
MASK_SUPERSAMPLE = 4
GENERATION_DATE = "2026-08-04"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repository_text_sha256(path: Path) -> str:
    """Hash text as it is stored in Git, independent of checkout EOLs."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _scaled_points(points: list[list[int]]) -> list[tuple[int, int]]:
    return [
        (int(point[0]) * MASK_SUPERSAMPLE,
         int(point[1]) * MASK_SUPERSAMPLE)
        for point in points
    ]


def _scaled_box(box: list[int]) -> tuple[int, int, int, int]:
    return tuple(int(value) * MASK_SUPERSAMPLE for value in box)


def _shape_layer(shape: dict[str, Any]) -> Image.Image:
    size = (CANVAS[0] * MASK_SUPERSAMPLE,
            CANVAS[1] * MASK_SUPERSAMPLE)
    layer = Image.new("L", size, 0)
    draw = ImageDraw.Draw(layer)
    shape_type = str(shape["type"])
    if shape_type == "polygon":
        draw.polygon(_scaled_points(shape["points"]), fill=255)
    elif shape_type == "ellipse":
        draw.ellipse(_scaled_box(shape["box"]), fill=255)
    elif shape_type == "rounded_rectangle":
        draw.rounded_rectangle(
            _scaled_box(shape["box"]),
            radius=int(shape.get("radius", 0)) * MASK_SUPERSAMPLE,
            fill=255,
        )
    elif shape_type == "line":
        draw.line(
            _scaled_points(shape["points"]),
            fill=255,
            width=max(1, int(shape.get("width", 1)) * MASK_SUPERSAMPLE),
            joint="curve",
        )
    else:
        raise ValueError(f"Unsupported mask shape: {shape_type}")
    return layer


def _shape_mask(shapes: list[dict[str, Any]]) -> Image.Image:
    size = (CANVAS[0] * MASK_SUPERSAMPLE,
            CANVAS[1] * MASK_SUPERSAMPLE)
    mask = Image.new("L", size, 0)
    for shape in shapes:
        layer = _shape_layer(shape)
        if shape.get("op", "add") == "subtract":
            mask = ImageChops.subtract(mask, layer)
        else:
            mask = ImageChops.lighter(mask, layer)
    return mask.resize(CANVAS, Image.Resampling.LANCZOS)


def _clean_plate(image: Image.Image, owned_mask: Image.Image) -> Image.Image:
    """Fill the opaque ownership core from unowned same-plate scanlines.

    This is the established room-layer fill algorithm, reproduced locally so
    V4 remains standalone and cannot mutate or invoke the legacy layer build.
    The caller supplies the exact binary ownership core to change.
    """
    from scipy.ndimage import distance_transform_edt

    mask_array = np.asarray(owned_mask, dtype=np.uint8) >= 250
    source = np.asarray(image.convert("RGB"), dtype=np.float32)
    height, width = mask_array.shape
    if not np.any(mask_array):
        return image.convert("RGB").copy()

    indices = distance_transform_edt(
        mask_array, return_distances=False, return_indices=True)
    nearest = source[indices[0], indices[1]]
    horizontal = nearest.copy()
    vertical = nearest.copy()
    horizontal_valid = np.zeros(mask_array.shape, dtype=bool)
    vertical_valid = np.zeros(mask_array.shape, dtype=bool)
    x_positions = np.arange(width)
    y_positions = np.arange(height)
    for y_pos in range(height):
        known_x = np.flatnonzero(~mask_array[y_pos])
        if known_x.size == 0:
            continue
        horizontal_valid[y_pos, :] = True
        for channel in range(3):
            horizontal[y_pos, :, channel] = np.interp(
                x_positions, known_x, source[y_pos, known_x, channel])
    for x_pos in range(width):
        known_y = np.flatnonzero(~mask_array[:, x_pos])
        if known_y.size == 0:
            continue
        vertical_valid[:, x_pos] = True
        for channel in range(3):
            vertical[:, x_pos, channel] = np.interp(
                y_positions, known_y, source[known_y, x_pos, channel])

    filled = source.copy()
    both = mask_array & horizontal_valid & vertical_valid
    horizontal_only = mask_array & horizontal_valid & ~vertical_valid
    vertical_only = mask_array & vertical_valid & ~horizontal_valid
    neither = mask_array & ~horizontal_valid & ~vertical_valid
    filled[both] = horizontal[both] * 0.72 + vertical[both] * 0.28
    filled[horizontal_only] = horizontal[horizontal_only]
    filled[vertical_only] = vertical[vertical_only]
    filled[neither] = nearest[neither]
    filled = np.clip(filled, 0, 255).astype(np.uint8)
    smoothed = np.asarray(
        Image.fromarray(filled, "RGB").filter(ImageFilter.GaussianBlur(2.5)),
        dtype=np.uint8,
    )
    filled[mask_array] = smoothed[mask_array]
    return Image.fromarray(filled, "RGB")


def _existing_ownership(
    room_id: str,
    room_dir: Path,
    room_record: dict[str, Any],
) -> tuple[Image.Image, list[dict[str, Any]]]:
    ownership = Image.new("L", CANVAS, 0)
    existing_cards: list[dict[str, Any]] = []
    for record in room_record["cards"]:
        card_path = room_dir / f"room_{room_id}_{record['id']}.png"
        if not card_path.exists():
            raise FileNotFoundError(card_path)
        card = Image.open(card_path).convert("RGBA")
        crop = [int(value) for value in record["crop"]]
        expected_size = (crop[2] - crop[0], crop[3] - crop[1])
        if card.size != expected_size:
            raise ValueError(
                f"Existing card size mismatch: {card_path}: "
                f"{card.size} != {expected_size}")
        alpha = card.getchannel("A")
        full_alpha = Image.new("L", CANVAS, 0)
        full_alpha.paste(alpha, (crop[0], crop[1]))
        ownership = ImageChops.lighter(ownership, full_alpha)
        existing_cards.append({
            "record": record,
            "path": card_path,
            "image": card,
            "crop": crop,
            "full_alpha": full_alpha,
        })
    return ownership, existing_cards


def _refine_mask(
    source: Image.Image,
    provisional_background: Image.Image,
    raw_mask: Image.Image,
    crop: list[int],
    forbidden: Image.Image,
) -> Image.Image:
    """Settle a routing mask onto the painted outline without filling holes."""
    left, top, right, bottom = crop
    raw_crop = np.asarray(raw_mask.crop(tuple(crop)), dtype=np.float32) / 255.0
    raw_core = raw_crop >= 0.16
    if not np.any(raw_core):
        return Image.new("L", CANVAS, 0)

    source_crop = np.asarray(
        source.crop(tuple(crop)), dtype=np.float32) / 255.0
    clean_crop = np.asarray(
        provisional_background.crop(tuple(crop)), dtype=np.float32) / 255.0
    difference = np.max(np.abs(source_crop - clean_crop), axis=2) * 255.0
    edge = np.max(np.stack([
        sobel(source_crop[:, :, channel]) for channel in range(3)
    ]), axis=0)

    markers = np.zeros(raw_core.shape, dtype=np.uint8)
    markers[~raw_core] = 1
    markers[raw_core & (difference <= 7.0)] = 1
    strong_foreground = raw_core & (difference >= 32.0)
    markers[strong_foreground] = 2
    if not np.any(strong_foreground):
        raise RuntimeError(f"No foreground seed in crop {crop}")

    segmented = (watershed(edge, markers) == 2) & raw_core
    components, component_count = label(segmented)
    # Detached sub-12px islands are illustration noise/background flecks, not
    # usable child-readable fixture parts. Keeping them creates the exact
    # "brick chip on a transparent card" failure this V4 pass is removing.
    minimum_component = max(12, int(np.count_nonzero(raw_core) * 0.0015))
    kept = np.zeros(segmented.shape, dtype=bool)
    for component_id in range(1, component_count + 1):
        component = components == component_id
        if (np.count_nonzero(component) >= minimum_component
                and np.any(component & strong_foreground)):
            kept |= component

    local_alpha = Image.fromarray(
        kept.astype(np.uint8) * 255, mode="L").filter(
            ImageFilter.GaussianBlur(0.45))
    local_alpha = ImageChops.multiply(
        local_alpha, raw_mask.crop(tuple(crop)))
    full_alpha = Image.new("L", CANVAS, 0)
    full_alpha.paste(local_alpha, (left, top))

    # Reapply hard availability after antialiasing. No alpha, including a soft
    # fringe, may be owned by both an old card and a new card.
    unavailable = forbidden.point(lambda value: 255 if value > 0 else 0)
    full_alpha = ImageChops.multiply(
        full_alpha, ImageChops.invert(unavailable))
    return full_alpha


def _source_rect(crop: list[int]) -> list[int]:
    return [crop[0], crop[1], crop[2] - crop[0], crop[3] - crop[1]]


def _visible_global_crop(mask: Image.Image) -> list[int]:
    bbox = mask.point(lambda value: 255 if value >= 16 else 0).getbbox()
    if bbox is None:
        raise RuntimeError("Ownership mask has no visible alpha")
    return [int(value) for value in bbox]


def _exact_alpha_card(
    source: Image.Image,
    crop: list[int],
    full_alpha: Image.Image,
) -> tuple[Image.Image, Image.Image]:
    """Return a tight exact-RGB card and RGBA alpha-evidence image."""
    local_alpha = full_alpha.crop(tuple(crop))
    source_crop = source.crop(tuple(crop)).convert("RGB")
    source_array = np.asarray(source_crop, dtype=np.uint8)
    alpha_array = np.asarray(local_alpha, dtype=np.uint8)
    rgba_array = np.zeros((source_crop.height, source_crop.width, 4), dtype=np.uint8)
    rgba_array[:, :, :3] = source_array
    rgba_array[:, :, 3] = alpha_array
    rgba_array[alpha_array == 0, :3] = 0
    card = Image.fromarray(rgba_array, "RGBA")

    mask_array = np.zeros_like(rgba_array)
    mask_array[alpha_array > 0, :3] = 255
    mask_array[:, :, 3] = alpha_array
    mask = Image.fromarray(mask_array, "RGBA")
    visible = alpha_array > 0
    card_rgb = np.asarray(card, dtype=np.uint8)[:, :, :3]
    if np.any(card_rgb[visible] != source_array[visible]):
        raise RuntimeError("Visible resting-card RGB diverged from source")
    return card, mask


def _fridge_only_source_card(
        source_card: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    """Discard legacy non-fridge alpha while preserving every retained RGB pixel."""
    rgba = np.asarray(source_card.convert("RGBA"), dtype=np.uint8).copy()
    red = rgba[:, :, 0].astype(np.int16)
    green = rgba[:, :, 1].astype(np.int16)
    blue = rgba[:, :, 2].astype(np.int16)
    alpha = rgba[:, :, 3]
    visible = alpha >= 16
    # Purple wall fragments at the upper-left/left outline are not fridge
    # pixels.  Peach/gold hardware is retained because its blue channel stays
    # below green; teal shell pixels are retained because green dominates.
    purple_wall = (red >= green + 8) & (blue >= green + 8)
    yy, xx = np.mgrid[0:source_card.height, 0:source_card.width]
    # This narrow protrusion between the two gold hinges belongs to the
    # neighboring lower cabinet in the approved room composite.
    neighboring_cabinet = (xx >= 133) & (yy >= 164) & (yy <= 196)
    keep = visible & ~purple_wall & ~neighboring_cabinet
    components, component_count = label(keep)
    component_sizes = np.bincount(components.ravel())
    kept = np.zeros(keep.shape, dtype=bool)
    for component_id in range(1, component_count + 1):
        if int(component_sizes[component_id]) >= 8:
            kept |= components == component_id
    if not np.any(kept):
        raise RuntimeError("fridge alpha cleanup removed the source object")
    rgba[:, :, 3] = np.where(kept, alpha, 0).astype(np.uint8)
    rgba[~kept, :3] = 0
    cleaned = Image.fromarray(rgba, "RGBA")
    retained_rgb = np.asarray(cleaned, dtype=np.uint8)[:, :, :3]
    source_rgb = np.asarray(source_card.convert("RGBA"), dtype=np.uint8)[:, :, :3]
    if np.any(retained_rgb[kept] != source_rgb[kept]):
        raise RuntimeError("fridge alpha cleanup changed retained source RGB")
    return cleaned, {
        "method": "fridge_only_source_pixels_v1",
        "rgb_repainted": False,
        "minimum_retained_alpha": 16,
        "purple_wall_rule": "red>=green+8 and blue>=green+8",
        "neighboring_cabinet_exclusion_xyxy": [133, 164, 140, 197],
        "minimum_retained_component_pixels": 8,
        "removed_visible_pixels": int(np.count_nonzero(visible & ~kept)),
        "retained_visible_pixels": int(np.count_nonzero(kept)),
    }


def _checkerboard(size: tuple[int, int], cell: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, (238, 232, 246, 255))
    draw = ImageDraw.Draw(image)
    for y_pos in range(0, size[1], cell):
        for x_pos in range(0, size[0], cell):
            if (x_pos // cell + y_pos // cell) % 2:
                draw.rectangle(
                    (x_pos, y_pos, x_pos + cell - 1, y_pos + cell - 1),
                    fill=(211, 202, 226, 255),
                )
    return image


def _annotated_thumbnail(
    image: Image.Image,
    boxes: list[tuple[str, list[int]]],
    label_text: str,
) -> Image.Image:
    thumb = image.convert("RGB").resize((512, 288), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(thumb)
    for item_id, crop in boxes:
        scaled = [
            int(crop[0] * 0.5), int(crop[1] * 0.5),
            int(crop[2] * 0.5), int(crop[3] * 0.5),
        ]
        draw.rectangle(tuple(scaled), outline=(255, 45, 104), width=2)
        draw.text((scaled[0] + 2, max(1, scaled[1] - 11)), item_id,
                  fill=(255, 255, 255), stroke_width=2,
                  stroke_fill=(76, 31, 88))
    draw.rectangle((0, 0, 511, 19), fill=(37, 28, 61))
    draw.text((7, 4), label_text, fill=(255, 255, 255))
    return thumb


def _save_room_audit(
    path: Path,
    source: Image.Image,
    parent_background: Image.Image,
    healed_background: Image.Image,
    reconstruction: Image.Image,
    boxes: list[tuple[str, list[int]]],
) -> None:
    sheet = Image.new("RGB", (1024, 576), (35, 28, 55))
    panels = [
        _annotated_thumbnail(source, boxes, "SOURCE + NATIVE OWNERSHIP"),
        _annotated_thumbnail(parent_background, boxes, "PARENT CLEAN PLATE"),
        _annotated_thumbnail(healed_background, boxes, "V4 HEALED PLATE"),
        _annotated_thumbnail(reconstruction, boxes, "RESTING RECONSTRUCTION"),
    ]
    sheet.paste(panels[0], (0, 0))
    sheet.paste(panels[1], (512, 0))
    sheet.paste(panels[2], (0, 288))
    sheet.paste(panels[3], (512, 288))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, optimize=True)


def _save_card_contact_sheet(
    path: Path,
    entries: list[dict[str, Any]],
    root: Path,
    white_background: bool = False,
) -> None:
    columns = 4
    cell_size = (240, 180)
    rows = (len(entries) + columns - 1) // columns
    sheet = Image.new(
        "RGBA", (columns * cell_size[0], rows * cell_size[1]),
        (35, 28, 55, 255))
    for index, entry in enumerate(entries):
        card = Image.open(root / entry["rest_card_path"]).convert("RGBA")
        available = (cell_size[0] - 20, cell_size[1] - 42)
        scale = min(available[0] / card.width, available[1] / card.height, 1.0)
        size = (max(1, int(card.width * scale)),
                max(1, int(card.height * scale)))
        card = card.resize(size, Image.Resampling.LANCZOS)
        cell = (Image.new("RGBA", cell_size, (255, 255, 255, 255))
                if white_background else _checkerboard(cell_size))
        x_pos = (cell_size[0] - card.width) // 2
        y_pos = 28 + (available[1] - card.height) // 2
        cell.alpha_composite(card, (x_pos, y_pos))
        draw = ImageDraw.Draw(cell)
        draw.rectangle((0, 0, cell_size[0] - 1, 25), fill=(76, 49, 99, 255))
        label_text = f"{entry['asset_id']}  ({entry['source_rect'][2]}x{entry['source_rect'][3]})"
        draw.text((6, 7), label_text, fill=(255, 255, 255, 255))
        column = index % columns
        row = index // columns
        sheet.alpha_composite(cell, (column * cell_size[0], row * cell_size[1]))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(path, optimize=True)


def _build_instance(
    room_id: str,
    item_id: str,
    semantic_action: str,
    crop: list[int],
    rest_card_path: Path,
    mask_path: Path,
    source_path: Path,
    healed_background_path: Path,
    root: Path,
    reused_existing_card: bool = False,
) -> dict[str, Any]:
    source_rect = _source_rect(crop)
    instance: dict[str, Any] = {
        "id": item_id,
        "asset_id": f"{room_id}_{item_id}",
        "semantic_action": semantic_action,
        "pack": "v4_native",
        "source_rect": source_rect,
        "rest_card_path": _relative(rest_card_path, root),
        "mask_path": _relative(mask_path, root),
        "healed_background_path": _relative(healed_background_path, root),
        "animation_behavior": {
            "mode": "authored_object_states",
            "action": semantic_action,
            "generic_transform_fallback": False,
        },
        "authored_frames": {
            "status": "pending_generation",
            "sheet_path": None,
            "state_count": 0,
        },
        "source_ownership": {
            "passed": True,
            "verified": True,
            "background_healed": True,
            "duplicate_pixels_removed": True,
            "source_rect": source_rect,
            "source_room_plate_sha256": _sha256(source_path),
            "healed_background_sha256": _sha256(healed_background_path),
            "rest_card_sha256": _sha256(rest_card_path),
        },
    }
    if reused_existing_card:
        instance["reuse_existing_card"] = True
    return instance


def _runtime_asset_record(room_id: str, instance: dict[str, Any]) -> dict[str, Any]:
    """Promote ownership evidence into the fail-closed runtime schema.

    Authored sheets are deliberately null until the animation pass supplies
    four to twelve reviewed full-object states. Runtime validation rejects
    these preparation records rather than falling back to generic movement.
    """
    source_rect = list(instance["source_rect"])
    record = {
        "id": instance["asset_id"],
        "room": room_id,
        "name": str(instance["id"]).replace("_", " ").title(),
        "instances": [instance["id"]],
        "pack": "v4_native",
        "semantic_action": instance["semantic_action"],
        "render_mode": "generated_full_object_states",
        "primary_animation_is_overlay": False,
        "source_rect": source_rect,
        "placement_position": source_rect[:2],
        "placement_size": source_rect[2:],
        "rest_card_path": instance["rest_card_path"],
        "mask_path": instance["mask_path"],
        "healed_background_path": instance["healed_background_path"],
        "source_room_plate_path": (
            f"assets/flats/castle/rooms/room_{room_id}.png"),
        "source_ownership": instance["source_ownership"],
        "animation_behavior": instance["animation_behavior"],
        "physics_mode": "none",
        "sheet": None,
        "sheet_sha256": None,
        "grid": [4, 2],
        "authored_frame_count": 0,
        "frame_count": 0,
        "rest_frame": 0,
        "timeline_sequence": [],
        "timeline_frame_count": 0,
        "delivery_status": "ownership_ready_authored_states_pending",
    }
    if "source_alpha_cleanup" in instance:
        record["source_alpha_cleanup"] = instance["source_alpha_cleanup"]
    return record


def build(root: Path, spec_path: Path) -> dict[str, Any]:
    room_dir = root / "assets" / "flats" / "castle" / "rooms"
    output_root = root / "assets" / "flats" / "castle" / "interactions_v4"
    card_dir = output_root / "rest_cards"
    background_dir = output_root / "backgrounds"
    source_root = root / "assets_src" / "castle" / "interactions_v4"
    mask_dir = source_root / "masks"
    audit_dir = root / "audit" / "castle_native_interactions_v4"
    layer_manifest_path = root / "FABLE_CASTLE_DEPTH_MANIFEST_2026-07-26.json"

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if tuple(spec["canvas"]) != CANVAS:
        raise ValueError(f"V4 spec canvas must be {CANVAS}")
    layer_manifest = json.loads(layer_manifest_path.read_text(encoding="utf-8"))

    card_dir.mkdir(parents=True, exist_ok=True)
    background_dir.mkdir(parents=True, exist_ok=True)
    mask_dir.mkdir(parents=True, exist_ok=True)
    audit_dir.mkdir(parents=True, exist_ok=True)
    # Remove only files this deterministic extraction pass owns. This prevents
    # a rejected candidate from lingering as an apparently active V4 asset.
    for directory, pattern in (
            (card_dir, "*_rest.png"),
            (background_dir, "room_*_background.png"),
            (mask_dir, "*_mask.png")):
        for stale_path in directory.glob(pattern):
            stale_path.unlink()

    manifest: dict[str, Any] = {
        "schema_version": 4,
        "generated_on": GENERATION_DATE,
        "generator": _relative(Path(__file__).resolve(), root),
        "generator_sha256": _repository_text_sha256(Path(__file__).resolve()),
        "spec": _relative(spec_path, root),
        "spec_sha256": _repository_text_sha256(spec_path),
        "source_layer_manifest": _relative(layer_manifest_path, root),
        "source_layer_manifest_sha256": _repository_text_sha256(
            layer_manifest_path),
        "contract": {
            "resting_rgb_source": "exact approved room-composite pixels",
            "card_rgb_repainted": False,
            "parent_backgrounds_modified": False,
            "new_background_healing_passes": 1,
            "card_overlap_pixels_allowed": 0,
            "authored_animation_states_required_before_runtime": True,
            "generic_transform_fallback": False,
        },
        "assets": [],
        "rooms": {},
        "excluded": spec.get("excluded", []),
    }
    all_instances: list[dict[str, Any]] = []

    for room_id, candidates in spec["candidates"].items():
        source_path = room_dir / f"room_{room_id}.png"
        parent_background_path = room_dir / f"room_{room_id}_background.png"
        source = Image.open(source_path).convert("RGB")
        parent_background = Image.open(parent_background_path).convert("RGB")
        if source.size != CANVAS or parent_background.size != CANVAS:
            raise ValueError(f"Unexpected {room_id} room dimensions")

        layer_room = layer_manifest["rooms"][room_id]
        existing_ownership, existing_cards = _existing_ownership(
            room_id, room_dir, layer_room)
        claimed = existing_ownership.copy()
        raw_masks: list[Image.Image] = []
        for candidate in candidates:
            raw = _shape_mask(candidate["shapes"])
            unavailable = claimed.point(lambda value: 255 if value > 0 else 0)
            raw = ImageChops.multiply(raw, ImageChops.invert(unavailable))
            raw_masks.append(raw)
            claimed = ImageChops.lighter(claimed, raw)

        raw_union = Image.new("L", CANVAS, 0)
        for raw in raw_masks:
            raw_union = ImageChops.lighter(raw_union, raw)
        # MA-VIS-007: segmentation compares against the complete authoritative
        # clean frame; it must never synthesize a temporary blur-filled plate.
        provisional_background = parent_background.copy()

        refined_masks: list[Image.Image] = []
        refined_claimed = existing_ownership.copy()
        new_union = Image.new("L", CANVAS, 0)
        card_builds: list[dict[str, Any]] = []
        for candidate, raw in zip(candidates, raw_masks):
            crop = [int(value) for value in candidate["crop"]]
            refined = _refine_mask(
                source, provisional_background, raw, crop, refined_claimed)
            alpha_array = np.asarray(refined, dtype=np.uint8)
            alpha_pixels = int(np.count_nonzero(alpha_array > 0))
            opaque_pixels = int(np.count_nonzero(alpha_array >= 128))
            if opaque_pixels < 64:
                raise RuntimeError(
                    f"{room_id}:{candidate['id']} mask too small: "
                    f"{opaque_pixels} opaque pixels")
            refined_masks.append(refined)
            refined_claimed = ImageChops.lighter(refined_claimed, refined)
            new_union = ImageChops.lighter(new_union, refined)

            asset_id = f"{room_id}_{candidate['id']}"
            card_path = card_dir / f"{asset_id}_rest.png"
            mask_path = mask_dir / f"{asset_id}_mask.png"
            source_crop = _visible_global_crop(refined)
            card, mask_evidence = _exact_alpha_card(
                source, source_crop, refined)
            card.save(card_path, optimize=True)
            mask_evidence.save(mask_path, optimize=True)
            card_builds.append({
                "candidate": candidate,
                "routing_crop": crop,
                "crop": source_crop,
                "card_path": card_path,
                "mask_path": mask_path,
                "alpha_pixels": alpha_pixels,
                "opaque_pixels": opaque_pixels,
            })

        reused = spec.get("reused_existing", {}).get(room_id, [])
        existing_by_id = {
            str(card["record"]["id"]).removeprefix("item_"): card
            for card in existing_cards
            if str(card["record"]["id"]).startswith("item_")
        }
        for reused_spec in reused:
            cleanup_method = str(reused_spec.get("alpha_cleanup", ""))
            if not cleanup_method:
                continue
            item_id = str(reused_spec["id"])
            existing = existing_by_id.get(item_id)
            if existing is None:
                raise KeyError(f"Missing cleanup card {room_id}:{item_id}")
            if cleanup_method != "fridge_only_source_pixels_v1" \
                    or room_id != "kitchen" or item_id != "fridge":
                raise ValueError(
                    f"Unsupported source alpha cleanup {room_id}:{item_id}: "
                    f"{cleanup_method}")
            original_path = existing["path"]
            cleaned_card, cleanup = _fridge_only_source_card(existing["image"])
            cleaned_path = card_dir / f"{room_id}_{item_id}_rest.png"
            cleaned_card.save(cleaned_path, optimize=True)
            full_alpha = Image.new("L", CANVAS, 0)
            full_alpha.paste(
                cleaned_card.getchannel("A"),
                (existing["crop"][0], existing["crop"][1]),
            )
            existing.update({
                "image": cleaned_card,
                "full_alpha": full_alpha,
                "path": cleaned_path,
                "alpha_cleanup": cleanup,
                "alpha_cleanup_source_path": original_path,
                "alpha_cleanup_source_sha256": _sha256(original_path),
            })
        repair_union = Image.new("L", CANVAS, 0)
        for reused_spec in reused:
            if not bool(reused_spec.get("repair_healing", False)):
                continue
            repair_id = str(reused_spec["id"])
            existing = existing_by_id.get(repair_id)
            if existing is None:
                raise KeyError(f"Missing repair card {room_id}:{repair_id}")
            repair_union = ImageChops.lighter(
                repair_union, existing["full_alpha"])

        # This is the sole production healing pass for all new room ownership.
        # The ownership audit measures alpha >= 48, so harden that same verified
        # core before filling. Leaving the antialiased core unchanged would keep
        # duplicate source pixels under a moving/generated object state.
        healing_union = new_union.point(
            lambda value: 255 if value >= 48 else 0)
        healing_union = ImageChops.lighter(
            healing_union,
            repair_union.point(lambda value: 255 if value >= 48 else 0),
        )
        # Background pixels are owned by the complete generated frame.  New
        # cards may not locally repaint, interpolate, or blur that frame.
        healed_background = parent_background.copy()
        healed_background_path = background_dir / f"room_{room_id}_background.png"
        healed_background.save(healed_background_path, optimize=True)

        occupancy = np.zeros((CANVAS[1], CANVAS[0]), dtype=np.uint8)
        for alpha in refined_masks:
            occupancy += (np.asarray(alpha, dtype=np.uint8) > 0).astype(np.uint8)
        existing_array = np.asarray(existing_ownership, dtype=np.uint8) > 0
        new_array = np.asarray(new_union, dtype=np.uint8) > 0
        new_card_overlap = int(np.count_nonzero(occupancy > 1))
        existing_card_overlap = int(np.count_nonzero(existing_array & new_array))
        if new_card_overlap or existing_card_overlap:
            raise RuntimeError(
                f"Ownership overlap in {room_id}: new={new_card_overlap}, "
                f"existing={existing_card_overlap}")

        parent_array = np.asarray(parent_background, dtype=np.uint8)
        healed_array = np.asarray(healed_background, dtype=np.uint8)
        changed = np.any(parent_array != healed_array, axis=2)
        owned_core = np.asarray(healing_union, dtype=np.uint8) >= 250
        changed_outside = int(np.count_nonzero(changed & ~owned_core))
        if changed_outside:
            raise RuntimeError(
                f"Healing escaped new ownership in {room_id}: "
                f"{changed_outside} pixels")

        instances: list[dict[str, Any]] = []
        for build_record in card_builds:
            candidate = build_record["candidate"]
            instance = _build_instance(
                room_id,
                str(candidate["id"]),
                str(candidate["semantic_action"]),
                build_record["crop"],
                build_record["card_path"],
                build_record["mask_path"],
                source_path,
                healed_background_path,
                root,
            )
            instance["alpha_pixels"] = build_record["alpha_pixels"]
            instance["depth_opaque_pixels"] = build_record["opaque_pixels"]
            instance["routing_crop"] = build_record["routing_crop"]
            instance["source_ownership"]["mask_sha256"] = _sha256(
                build_record["mask_path"])
            instances.append(instance)

        for reused_spec in reused:
            item_id = str(reused_spec["id"])
            existing = existing_by_id.get(item_id)
            if existing is None:
                raise KeyError(f"Missing reusable card {room_id}:{item_id}")
            original_crop = existing["crop"]
            visible_bbox = existing["image"].getchannel("A").point(
                lambda value: 255 if value >= 16 else 0).getbbox()
            if visible_bbox is None:
                raise RuntimeError(f"Reusable card has no alpha: {room_id}:{item_id}")
            crop = [
                original_crop[0] + int(visible_bbox[0]),
                original_crop[1] + int(visible_bbox[1]),
                original_crop[0] + int(visible_bbox[2]),
                original_crop[1] + int(visible_bbox[3]),
            ]
            mask_path = mask_dir / f"{room_id}_{item_id}_existing_mask.png"
            local_alpha = existing["image"].getchannel("A").crop(visible_bbox)
            alpha_array = np.asarray(local_alpha, dtype=np.uint8)
            mask_array = np.zeros(
                (local_alpha.height, local_alpha.width, 4), dtype=np.uint8)
            mask_array[alpha_array > 0, :3] = 255
            mask_array[:, :, 3] = alpha_array
            Image.fromarray(mask_array, "RGBA").save(mask_path, optimize=True)
            instance = _build_instance(
                room_id,
                item_id,
                str(reused_spec["semantic_action"]),
                crop,
                existing["path"],
                mask_path,
                source_path,
                healed_background_path,
                root,
                reused_existing_card=True,
            )
            instance["source_ownership"].update({
                "mask_sha256": _sha256(mask_path),
                "prior_ownership_manifest": _relative(
                    layer_manifest_path, root),
                "prior_ownership_verified": True,
                "production_rehealed": bool(
                    reused_spec.get("repair_healing", False)),
            })
            if "alpha_cleanup" in existing:
                instance["source_alpha_cleanup"] = existing["alpha_cleanup"]
                instance["source_alpha_cleanup"].update({
                    "source_card_path": _relative(
                        existing["alpha_cleanup_source_path"], root),
                    "source_card_sha256": existing[
                        "alpha_cleanup_source_sha256"],
                    "cleaned_card_path": _relative(existing["path"], root),
                    "cleaned_card_sha256": _sha256(existing["path"]),
                })
            instance["routing_crop"] = original_crop
            instances.append(instance)

        reconstruction = healed_background.convert("RGBA")
        for existing in existing_cards:
            crop = existing["crop"]
            reconstruction.alpha_composite(
                existing["image"], (crop[0], crop[1]))
        for build_record in card_builds:
            crop = build_record["crop"]
            card = Image.open(build_record["card_path"]).convert("RGBA")
            reconstruction.alpha_composite(card, (crop[0], crop[1]))
        source_array = np.asarray(source, dtype=np.int16)
        reconstruction_array = np.asarray(
            reconstruction.convert("RGB"), dtype=np.int16)
        reconstruction_mae = float(np.abs(
            source_array - reconstruction_array).mean())

        room_audit_path = audit_dir / f"room_{room_id}_ownership_audit.png"
        boxes = [(str(candidate["id"]), [int(v) for v in candidate["crop"]])
                 for candidate in candidates]
        _save_room_audit(
            room_audit_path,
            source,
            parent_background,
            healed_background,
            reconstruction,
            boxes,
        )
        room_record: dict[str, Any] = {
            "source_room_plate": _relative(source_path, root),
            "source_room_plate_sha256": _sha256(source_path),
            "parent_background": _relative(parent_background_path, root),
            "parent_background_sha256": _sha256(parent_background_path),
            "healed_background": _relative(healed_background_path, root),
            "healed_background_sha256": _sha256(healed_background_path),
            "production_healing_passes": 1,
            "instances": instances,
            "physical_item_count": len(instances),
            "new_card_overlap_pixels": new_card_overlap,
            "existing_card_overlap_pixels": existing_card_overlap,
            "healing_changed_pixels": int(np.count_nonzero(changed)),
            "healing_changed_pixels_outside_owned_core": changed_outside,
            "resting_reconstruction_mean_abs_error": round(
                reconstruction_mae, 6),
            "visual_audit": {
                "path": _relative(room_audit_path, root),
                "sha256": _sha256(room_audit_path),
                "status": "generated_for_visual_review",
            },
        }
        manifest["rooms"][room_id] = room_record
        manifest["assets"].extend(
            _runtime_asset_record(room_id, instance)
            for instance in instances
        )
        all_instances.extend(instances)

    card_contact_path = audit_dir / "native_rest_cards_contact_sheet.png"
    _save_card_contact_sheet(card_contact_path, all_instances, root)
    white_contact_path = audit_dir / "native_rest_cards_white_contact_sheet.png"
    _save_card_contact_sheet(
        white_contact_path, all_instances, root, white_background=True)
    manifest["visual_review_evidence"] = {
        "path": _relative(card_contact_path, root),
        "sha256": _sha256(card_contact_path),
        "dimensions": list(Image.open(card_contact_path).size),
        "white_background_path": _relative(white_contact_path, root),
        "white_background_sha256": _sha256(white_contact_path),
        "status": "generated_for_visual_review",
    }
    manifest["summary"] = {
        "rooms_with_new_ownership": sum(
            1 for items in spec["candidates"].values() if items),
        "new_native_cards": sum(len(items) for items in spec["candidates"].values()),
        "reused_source_owned_cards": sum(
            len(items) for items in spec.get("reused_existing", {}).values()),
        "runtime_ready_authored_animation_sheets": 0,
    }
    manifest_path = output_root / "castle_interactions_v4.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    default_root = Path(__file__).resolve().parents[1]
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument(
        "--spec",
        type=Path,
        default=Path(__file__).with_name(
            "castle_native_interactions_v4_spec.json"),
    )
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    spec_path = arguments.spec.resolve()
    manifest = build(root, spec_path)
    print(json.dumps(manifest["summary"], indent=2))


if __name__ == "__main__":
    main()
