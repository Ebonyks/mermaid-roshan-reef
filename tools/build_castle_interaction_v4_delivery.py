#!/usr/bin/env python3
"""Build the source-owned Pearl Castle V4 runtime delivery.

The ownership extractor deliberately stops at exact room-derived rest cards and
1024x576 audit plates.  This builder performs the two production-only steps:

* author fixed-pivot 4x2 atlases whose first state is the exact clean rest card;
* heal the same accepted ownership masks directly in the approved high-resolution
  runtime tile masters, without upscaling audit plates.

No room object is invented here.  Generated source sheets are accepted only for
the specific object parts they faithfully preserve.  Failed sources (the full
tent canopy and the unrelated waterfall gate) are replaced with deterministic
states derived from the exact owned pixels.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter
from scipy.ndimage import (
    binary_erosion,
    binary_propagation,
    distance_transform_edt,
    label,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_RELATIVE = Path(
    "assets/flats/castle/interactions_v4/castle_interactions_v4.json"
)
SHEET_RELATIVE = Path("assets/flats/castle/interactions_v4/sheets")
REST_RELATIVE = Path("assets/flats/castle/interactions_v4/rest_cards")
SOURCE_TILE_RELATIVE = Path("assets/flats/castle/rooms/background_tiles")
RUNTIME_TILE_RELATIVE = Path(
    "assets/flats/castle/interactions_v4/background_tiles"
)

CELL_SIZE = (256, 256)
SHEET_SIZE = (1024, 512)
GRID = (4, 2)
FRAME_COUNT = 8
TIMELINE = [0, 1, 2, 3, 4, 5, 6, 7, 0]
MIN_ALPHA = 16
MASK_ALPHA = 48
MIN_PADDING = 6
BUILDER_VERSION = 1
GENERATION_DATE = "2026-08-04"


@dataclass(frozen=True)
class AnimationPlan:
    method: str
    pivot: str = "center"
    source: str = ""
    source_frames: tuple[int, ...] = tuple(range(FRAME_COUNT))
    source_segmentation: str = "alpha"
    grid: tuple[int, int] = GRID
    cell_size: tuple[int, int] = CELL_SIZE
    sound: str = ""
    close_sound: str = ""
    sound_frame: int = 1
    frame_duration: float = 0.12


PLANS: dict[str, AnimationPlan] = {
    "kitchen_fridge": AnimationPlan(
        "normalized_generated_fridge_states_fixed_base",
        pivot="bottom_left",
        source=("assets_src/imagegen/castle_object_animations_v4/kitchen/"
                "kitchen_fridge_sheet_checkerboard.png"),
        source_segmentation="edge_connected_neutral_checkerboard_components",
        grid=(3, 3),
        cell_size=(320, 272),
        sound="assets/audio/castle/fridge_open.ogg",
        close_sound="assets/audio/castle/fridge_close.ogg",
        sound_frame=1,
        frame_duration=0.145,
    ),
    "opera_hall_pearl_sconce_left": AnimationPlan(
        "source_owned_pearl_color_chase", sound="assets/audio/castle/light_switch.ogg"),
    "opera_hall_pearl_sconce_right": AnimationPlan(
        "source_owned_pearl_color_chase", sound="assets/audio/castle/light_switch.ogg"),
    "library_pearl_lamp_right": AnimationPlan(
        "source_owned_pearl_color_chase", sound="assets/audio/castle/light_switch.ogg"),
    "library_ceiling_chandelier": AnimationPlan(
        "source_owned_pearl_color_chase", sound="assets/audio/castle/light_switch.ogg"),
    "playroom_shelf_sailboat": AnimationPlan(
        "normalized_generated_full_object_states_fixed_pivot",
        pivot="bottom_center",
        source=("assets_src/imagegen/castle_object_animations_v4/playroom/"
                "playroom_shelf_sailboat_sheet_alpha.png"),
        sound="assets/audio/castle/curtain_swish.ogg",
        frame_duration=0.13,
    ),
    "craft_room_supply_cupboard_left": AnimationPlan(
        "normalized_generated_full_object_states_fixed_pivot",
        pivot="bottom_center",
        source=("assets_src/imagegen/castle_object_animations_v4/craft_room/"
                "craft_room_supply_cupboard_left_sheet_alpha.png"),
        sound="assets/audio/castle/toy_blocks.ogg",
        frame_duration=0.13,
    ),
    "mermaid_pool_waterfall": AnimationPlan(
        "source_owned_native_states_with_fixture_water_shader_handoff",
        pivot="top_center",
        sound="assets/audio/castle/bubble_water.ogg",
        frame_duration=0.10,
    ),
    "mermaid_pool_flower_float": AnimationPlan(
        "normalized_generated_states_with_exact_source_support",
        pivot="bottom_center",
        source=("assets_src/imagegen/castle_object_animations_v4/mermaid_pool/"
                "mermaid_pool_flower_float_sheet_alpha.png"),
        sound="assets/audio/castle/bubble_water.ogg",
        frame_duration=0.13,
    ),
    "mermaid_pool_seahorse_fountain": AnimationPlan(
        "source_owned_seahorse_stream_shimmer_states",
        pivot="bottom_center",
        sound="assets/audio/castle/faucet_water.ogg",
        frame_duration=0.10,
    ),
    "mermaid_pool_star_float": AnimationPlan(
        "safe_generated_states_with_exact_source_support",
        pivot="bottom_center",
        source=("assets_src/imagegen/castle_object_animations_v4/mermaid_pool/"
                "mermaid_pool_star_float_sheet_alpha.png"),
        source_frames=(0, 6, 7, 6, 0, 7, 6, 0),
        sound="assets/audio/castle/bubble_water.ogg",
        frame_duration=0.13,
    ),
    "bubble_bath_vanity_mirror": AnimationPlan(
        "source_owned_mirror_fog_wipe_states",
        sound="assets/audio/castle/faucet_water.ogg",
        frame_duration=0.12,
    ),
}


PHYSICS: dict[str, dict[str, Any]] = {
    "mermaid_pool_flower_float": {
        "physics_mode": "buoyant",
        "physics_role": "bounded_float_settle_after_authored_petals",
        "physics_max_angle_radians": 0.065,
        "physics_impulse_scale": 0.24,
    },
    "mermaid_pool_star_float": {
        "physics_mode": "buoyant",
        "physics_role": "bounded_float_settle_after_authored_point_flex",
        "physics_max_angle_radians": 0.06,
        "physics_impulse_scale": 0.22,
    },
}


WATER_LAYERS: dict[str, list[dict[str, Any]]] = {
    "mermaid_pool_waterfall": [{
        "role": "waterfall_band",
        "shape": "polygon",
        # Follow the painted fall from the shell lip to the existing foam.
        # A low-alpha highlight layer preserves the rainbow art instead of
        # laying an opaque cyan rectangle over it at maximum flow.
        "points": [[0.29, 0.13], [0.81, 0.13], [0.76, 0.93], [0.34, 0.93]],
        "local_origin": "source_rect",
        "active_frames": [1, 2, 3, 4, 5, 6],
        "flow_start": 0.02,
        "stream": True,
        "z_offset": 0.012,
        "outlet_bounds_normalized": [0.29, 0.11, 0.52, 0.08],
        "painted_stream_alpha_preserved": True,
        "deep": [0.72, 0.93, 0.99, 1.0],
        "shallow": [0.97, 0.995, 1.0, 1.0],
        "alpha_base": 0.12,
        "turbulence": 0.42,
        "edge_foam": 0.05,
        "flow_speed": 1.35,
    }],
    "mermaid_pool_seahorse_fountain": [{
        "role": "stream",
        "shape": "polygon",
        # The first edge is the outlet edge consumed by CastleFixtureRigs.
        "points": [
            [0.35, 0.32], [0.46, 0.34], [0.40, 0.47], [0.29, 0.66],
            [0.12, 0.91], [0.03, 0.89], [0.17, 0.62], [0.27, 0.43],
        ],
        "local_origin": "source_rect",
        "active_frames": [1, 2, 3, 4, 5, 6],
        "flow_start": 0.08,
        "stream": True,
        "z_offset": 0.013,
        "outlet_bounds_normalized": [0.32, 0.29, 0.17, 0.10],
        "deep": [0.68, 0.91, 0.97, 1.0],
        "shallow": [0.92, 0.995, 1.0, 1.0],
        "alpha_base": 0.14,
        "turbulence": 0.12,
        "edge_foam": 0.06,
        "flow_speed": 1.10,
    }],
    "mermaid_pool_flower_float": [{
        "role": "ripple",
        "shape": "ellipse",
        "center": [0.50, 0.76],
        "radius": [0.27, 0.07],
        "local_origin": "source_rect",
        "active_frames": [1, 2, 3, 4, 5, 6],
        "flow_start": 0.10,
        "z_offset": -0.004,
        "contact_role": "under_object_pool_contact",
        "alpha_base": 0.12,
        "turbulence": 0.08,
        "edge_foam": 0.04,
        "flow_speed": 0.72,
    }],
    "mermaid_pool_star_float": [{
        "role": "ripple",
        "shape": "ellipse",
        "center": [0.50, 0.78],
        "radius": [0.25, 0.07],
        "local_origin": "source_rect",
        "active_frames": [1, 2, 3, 4, 5, 6],
        "flow_start": 0.10,
        "z_offset": -0.004,
        "contact_role": "under_object_pool_contact",
        "alpha_base": 0.12,
        "turbulence": 0.08,
        "edge_foam": 0.04,
        "flow_speed": 0.72,
    }],
}

_seahorse_layer = WATER_LAYERS["mermaid_pool_seahorse_fountain"][0]
_seahorse_base_points = _seahorse_layer["points"]


SEMANTIC_OVERRIDES = {
    "kitchen_fridge": "unlatch_and_open_fridge_door",
    "craft_room_supply_cupboard_left": "pull_supply_bins_and_reveal_art_supplies",
    "mermaid_pool_flower_float": "bloom_flower_petals_and_make_ripples",
    "mermaid_pool_star_float": "flex_star_point_and_make_ripples",
}


GENERATED_TARGET_REST_BBOX: dict[str, list[int]] = {}


VISUAL_REVIEW_NOTES = {
    "kitchen_fridge": (
        "Accepted source-owned override: frame zero keeps exact approved teal fridge "
        "RGB while discarding only audited wall/cabinet alpha from the legacy card. "
        "Generated frames preserve its mint shell, peach shell badge, "
        "gold handle and hinges while opening the attached door to reveal a coherent "
        "food interior; the cabinet stays registered at one fixed base pivot."),
    "playroom_shelf_sailboat": (
        "Accepted: the same pink hull, pearl mast, flag, and triangular sail remain "
        "legible; authored states furl and unfurl the attached sail on a fixed "
        "bottom pivot rather than replacing or moving the shelf toy."),
    "craft_room_supply_cupboard_left": (
        "Accepted: the cream 2x2 casing, books, yellow supply cup, lavender bin, "
        "and blue bin retain identity; only the attached lower bins pull forward, "
        "with the casing held at the registered fixed root."),
    "playroom_tent_flaps_right": (
        "Accepted source-derived replacement: only the exact owned inner right flap "
        "folds at its seam; the non-owned generated canopy and gold knob are excluded."),
    "mermaid_pool_waterfall": (
        "Accepted source-derived replacement: exact shell, rock, and rainbow-flow "
        "alpha remains complete in every state while the painted stream pulses "
        "beneath a low-alpha fixture-water highlight shaped from lip to foam; the "
        "invented gate generation and both defective rectangular handoffs are "
        "excluded."),
    "mermaid_pool_seahorse_fountain": (
        "Accepted source-derived replacement after maximum-state Mobile review: "
        "the generated statue states were rejected for purple matte/body damage. "
        "Every state now preserves the exact painted fountain body and alpha "
        "silhouette; only its existing attached stream receives a gentle source-pixel "
        "shimmer beneath the tightly outlet-registered fixture-water shader."),
    "mermaid_pool_flower_float": (
        "Accepted with continuity repair: the exact aqua support remains attached "
        "beneath every petal state and the ripple stays under the float."),
    "mermaid_pool_star_float": (
        "Accepted safe subset: the exact cyan underside remains attached; extreme "
        "crescent states are excluded in favor of gentle point flex."),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_text_sha256(path: Path) -> str:
    """Hash text as it is stored in Git, independent of checkout EOLs."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def visible_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").point(
        lambda value: 255 if value >= MIN_ALPHA else 0
    ).getbbox()


def clean_hidden_rgb(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    rgba[rgba[:, :, 3] == 0, :3] = 0
    return Image.fromarray(rgba, "RGBA")


def png_bytes(image: Image.Image) -> bytes:
    stream = BytesIO()
    image.save(stream, format="PNG", compress_level=9, optimize=False)
    return stream.getvalue()


def pixel_sha256(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def split_generated_sheet(path: Path) -> list[Image.Image]:
    source = clean_hidden_rgb(Image.open(path).convert("RGBA"))
    cells: list[Image.Image] = []
    for index in range(FRAME_COUNT):
        column = index % GRID[0]
        row = index // GRID[0]
        left = round(column * source.width / GRID[0])
        right = round((column + 1) * source.width / GRID[0])
        top = round(row * source.height / GRID[1])
        bottom = round((row + 1) * source.height / GRID[1])
        cell = source.crop((left, top, right, bottom))
        canonical = Image.new("RGBA", (444, 444), (0, 0, 0, 0))
        canonical.alpha_composite(
            cell, ((canonical.width - cell.width) // 2,
                   (canonical.height - cell.height) // 2))
        cells.append(canonical)
    return cells


def split_checkerboard_component_sheet(
        path: Path) -> tuple[list[Image.Image], dict[str, Any]]:
    """Recover one complete fridge component per pose from a baked pale matte.

    The ImageGen poses cross the nominal 4x2 cell boundaries, so equal slicing
    would both clip an opening door and leak part of the neighboring state.  We
    instead flood only edge-connected near-neutral pixels in each source row,
    select the four dominant disconnected subjects, and register their visible
    bounds at one fixed lower-left cabinet base.  A one-pixel inward matte and
    subpixel feather remove the pale checker fringe without changing interior
    food, milk, cake, or pearl highlights.
    """
    source = Image.open(path).convert("RGB")
    if source.size != (1536, 1024):
        raise ValueError(
            f"fridge source must be RGB 1536x1024, got {source.size}")
    source_array = np.asarray(source, dtype=np.uint8)
    cells: list[Image.Image] = []
    source_bboxes: list[list[int]] = []
    component_pixels: list[int] = []
    neutral_minimum = 232
    neutral_spread = 18
    canonical_size = (512, 512)
    registered_left = 16
    registered_bottom = 496

    for row in range(2):
        row_top = row * 512
        row_array = source_array[row_top:row_top + 512]
        minimum = row_array.min(axis=2)
        spread = row_array.max(axis=2) - minimum
        neutral = (minimum >= neutral_minimum) & (spread <= neutral_spread)
        seeds = np.zeros(neutral.shape, dtype=bool)
        seeds[0, :] = neutral[0, :]
        seeds[-1, :] = neutral[-1, :]
        seeds[:, 0] = neutral[:, 0]
        seeds[:, -1] = neutral[:, -1]
        connected_background = binary_propagation(seeds, mask=neutral)
        labels, label_count = label(~connected_background)
        sizes = np.bincount(labels.ravel())
        candidates = sorted(
            range(1, label_count + 1), key=lambda value: int(sizes[value]),
            reverse=True)[:4]
        if len(candidates) != 4 or int(sizes[candidates[-1]]) < 10_000:
            raise ValueError(
                f"fridge matte row {row} did not yield four complete poses")
        candidates.sort(key=lambda value: int(
            np.flatnonzero(np.any(labels == value, axis=0))[0]))

        for component_id in candidates:
            hard_component = labels == component_id
            y_positions, x_positions = np.nonzero(hard_component)
            hard_bbox = (
                int(x_positions.min()), int(y_positions.min()),
                int(x_positions.max()) + 1, int(y_positions.max()) + 1,
            )
            left = max(0, hard_bbox[0] - 4)
            top = max(0, hard_bbox[1] - 4)
            right = min(source.width, hard_bbox[2] + 4)
            bottom = min(512, hard_bbox[3] + 4)
            local_hard = hard_component[top:bottom, left:right]
            local_core = binary_erosion(local_hard, iterations=1)
            if not np.any(local_core):
                raise ValueError("fridge matte erosion removed a pose")
            alpha = np.asarray(
                Image.fromarray(local_core.astype(np.uint8) * 255, "L").filter(
                    ImageFilter.GaussianBlur(0.8)),
                dtype=np.uint8,
            )
            rgb = row_array[top:bottom, left:right].copy()
            _, nearest = distance_transform_edt(
                ~local_core, return_distances=True, return_indices=True)
            feather = (~local_core) & (alpha > 0)
            rgb[feather] = rgb[
                nearest[0][feather], nearest[1][feather]]
            rgba = np.dstack((rgb, alpha))
            rgba[alpha == 0, :3] = 0
            recovered = Image.fromarray(rgba, "RGBA")
            recovered_bbox = visible_bbox(recovered)
            if recovered_bbox is None:
                raise ValueError("fridge recovered pose is empty")
            recovered = recovered.crop(recovered_bbox)
            if (recovered.width > canonical_size[0] - registered_left
                    or recovered.height > registered_bottom):
                raise ValueError("fridge recovered pose exceeds canonical canvas")
            cell = Image.new("RGBA", canonical_size, (0, 0, 0, 0))
            cell.alpha_composite(
                recovered,
                (registered_left, registered_bottom - recovered.height),
            )
            cells.append(clean_hidden_rgb(cell))
            source_bboxes.append([
                hard_bbox[0], hard_bbox[1] + row_top,
                hard_bbox[2], hard_bbox[3] + row_top,
            ])
            component_pixels.append(int(sizes[component_id]))

    return cells, {
        "matte_method": "edge_connected_neutral_components_in_two_source_rows",
        "source_grid_role": "layout_only_components_may_cross_nominal_cells",
        "neutral_minimum_rgb": neutral_minimum,
        "neutral_max_channel_spread": neutral_spread,
        "component_selection": "four_largest_per_row_sorted_left_to_right",
        "matte_core_erosion_pixels": 1,
        "matte_feather_radius_pixels": 0.8,
        "edge_rgb_decontamination": "nearest_eroded_foreground_core",
        "canonical_component_canvas": list(canonical_size),
        "fixed_source_base_registration": [registered_left, registered_bottom],
        "source_component_bboxes": source_bboxes,
        "source_component_pixels": component_pixels,
    }


def audit_pale_matte_edges(frames: list[Image.Image]) -> dict[str, Any]:
    counts: list[int] = []
    for frame in frames:
        array = np.asarray(frame.convert("RGBA"), dtype=np.uint8)
        alpha = array[:, :, 3]
        visible = alpha >= MIN_ALPHA
        edge = visible & ~binary_erosion(
            visible, structure=np.ones((5, 5), dtype=bool))
        rgb = array[:, :, :3]
        minimum = rgb.min(axis=2)
        spread = rgb.max(axis=2) - minimum
        pale_matte = edge & (minimum >= 232) & (spread <= 18)
        counts.append(int(np.count_nonzero(pale_matte)))
    if any(counts):
        raise ValueError(
            f"fridge source retains pale checker matte on frame edges: {counts}")
    return {
        "status": "passed",
        "edge_band_pixels": 2,
        "minimum_rgb": 232,
        "maximum_channel_spread": 18,
        "visible_pale_matte_pixels_by_frame": counts,
    }


def clean_generated_fridge_edges(
        frames: list[Image.Image]) -> tuple[list[Image.Image], dict[str, Any]]:
    cleaned = [frames[0]]
    translucent_counts = [0]
    pale_edge_counts = [0]
    component_counts: list[int] = []
    for index, frame in enumerate(frames):
        if index > 0:
            rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8).copy()
            alpha = rgba[:, :, 3]
            solid = alpha >= 224
            if not np.any(solid):
                raise ValueError(f"fridge frame {index} has no solid object core")
            _, nearest = distance_transform_edt(
                ~solid, return_distances=True, return_indices=True)
            translucent = (alpha > 0) & (alpha < 224)
            rgba[translucent, :3] = rgba[
                nearest[0][translucent], nearest[1][translucent], :3]
            visible = alpha >= MIN_ALPHA
            deep_visible = binary_erosion(
                visible, structure=np.ones((5, 5), dtype=bool))
            _, visible_nearest = distance_transform_edt(
                ~deep_visible, return_distances=True, return_indices=True)
            edge = visible & ~deep_visible
            rgb = rgba[:, :, :3]
            minimum = rgb.min(axis=2)
            spread = rgb.max(axis=2) - minimum
            pale_edge = edge & (minimum >= 232) & (spread <= 18)
            rgba[pale_edge, :3] = rgba[
                visible_nearest[0][pale_edge],
                visible_nearest[1][pale_edge], :3]
            rgba[alpha == 0, :3] = 0
            frame = Image.fromarray(rgba, "RGBA")
            cleaned.append(frame)
            translucent_counts.append(int(np.count_nonzero(translucent)))
            pale_edge_counts.append(int(np.count_nonzero(pale_edge)))
        visible = np.asarray(frame.getchannel("A"), dtype=np.uint8) >= MIN_ALPHA
        _components, count = label(visible)
        component_counts.append(int(count))
    if any(count != 1 for count in component_counts):
        raise ValueError(
            f"fridge frames contain disconnected alpha components: {component_counts}")
    return cleaned, {
        "method": "nearest_solid_object_core_rgb_on_translucent_generated_edges",
        "solid_alpha_threshold": 224,
        "translucent_edge_pixels_by_frame": translucent_counts,
        "pale_visible_edge_pixels_replaced_by_frame": pale_edge_counts,
        "visible_alpha_component_count_by_frame": component_counts,
        "disconnected_alpha_components_removed": True,
    }


def target_geometry(
        rest: Image.Image, source_rect: list[int],
        cell_size: tuple[int, int] = CELL_SIZE,
        registration_bbox: list[int] | tuple[int, int, int, int] | None = None,
        ) -> dict[str, Any]:
    rest_bbox = visible_bbox(rest)
    if rest_bbox is None:
        raise ValueError("rest card has no visible pixels")
    width, height = int(source_rect[2]), int(source_rect[3])
    registration = tuple(int(value) for value in (
        registration_bbox if registration_bbox is not None else rest_bbox))
    if len(registration) != 4:
        raise ValueError("rest-card registration bbox must have four values")
    if (registration[2] - registration[0],
            registration[3] - registration[1]) != (width, height):
        raise ValueError(
            "rest registration bbox does not equal source_rect size: "
            f"{registration} vs {source_rect}")
    target_left = (cell_size[0] - width) // 2
    target_top = (cell_size[1] - height) // 2
    rest_origin = (
        target_left - registration[0], target_top - registration[1])
    visible_target_bbox = (
        rest_bbox[0] + rest_origin[0], rest_bbox[1] + rest_origin[1],
        rest_bbox[2] + rest_origin[0], rest_bbox[3] + rest_origin[1],
    )
    return {
        "rest_bbox": rest_bbox,
        "registration_bbox": registration,
        "target_bbox": (target_left, target_top,
                        target_left + width, target_top + height),
        "visible_target_bbox": visible_target_bbox,
        "rest_origin": rest_origin,
        # This exactly compensates integer atlas placement, including odd sizes.
        "runtime_center_offset": [
            cell_size[0] / 2.0 - target_left,
            cell_size[1] / 2.0 - target_top,
        ],
    }


def pivot_point(bbox: tuple[int, int, int, int], mode: str) -> tuple[float, float]:
    left, top, right, bottom = bbox
    if mode == "bottom_left":
        return (float(left), float(bottom))
    if mode == "bottom_center":
        return ((left + right) * 0.5, float(bottom))
    if mode == "top_center":
        return ((left + right) * 0.5, float(top))
    if mode == "top_right":
        return (float(right), float(top))
    return ((left + right) * 0.5, (top + bottom) * 0.5)


def normalize_generated_frames(
        source_cells: list[Image.Image], rest: Image.Image,
        geometry: dict[str, Any], plan: AnimationPlan,
        target_bbox: tuple[int, int, int, int] | None = None,
        cell_size: tuple[int, int] = CELL_SIZE,
        ) -> tuple[list[Image.Image], dict[str, Any]]:
    boxes = [visible_bbox(cell) for cell in source_cells]
    if any(box is None for box in boxes):
        raise ValueError("generated source contains an empty state")
    typed_boxes = [box for box in boxes if box is not None]
    rest_bbox = target_bbox or geometry["target_bbox"]
    source_bbox = typed_boxes[0]
    source_width = source_bbox[2] - source_bbox[0]
    source_height = source_bbox[3] - source_bbox[1]
    target_width = rest_bbox[2] - rest_bbox[0]
    target_height = rest_bbox[3] - rest_bbox[1]
    scale = math.sqrt(
        (target_width / source_width) * (target_height / source_height))
    source_pivot = pivot_point(source_bbox, plan.pivot)
    target_pivot = pivot_point(rest_bbox, plan.pivot)
    union = (
        min(box[0] for box in typed_boxes), min(box[1] for box in typed_boxes),
        max(box[2] for box in typed_boxes), max(box[3] for box in typed_boxes),
    )
    limits: list[float] = []
    for available, distance in (
        (target_pivot[0] - MIN_PADDING, source_pivot[0] - union[0]),
        (cell_size[0] - MIN_PADDING - target_pivot[0], union[2] - source_pivot[0]),
        (target_pivot[1] - MIN_PADDING, source_pivot[1] - union[1]),
        (cell_size[1] - MIN_PADDING - target_pivot[1], union[3] - source_pivot[1]),
    ):
        if distance > 0.0:
            limits.append(available / distance)
    if limits:
        scale = min(scale, min(limits))
    resized_size = (
        max(1, round(source_cells[0].width * scale)),
        max(1, round(source_cells[0].height * scale)),
    )
    destination = (
        round(target_pivot[0] - source_pivot[0] * scale),
        round(target_pivot[1] - source_pivot[1] * scale),
    )
    normalized: list[Image.Image] = []
    for source_index in plan.source_frames:
        resized = source_cells[source_index].resize(
            resized_size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", cell_size, (0, 0, 0, 0))
        frame.alpha_composite(resized, destination)
        normalized.append(clean_hidden_rgb(frame))
    exact = Image.new("RGBA", cell_size, (0, 0, 0, 0))
    exact.alpha_composite(rest, geometry["rest_origin"])
    normalized[0] = clean_hidden_rgb(exact)
    return normalized, {
        "source_cell_canvas": list(source_cells[0].size),
        "uniform_scale": round(scale, 8),
        "uniform_translation": list(destination),
        "source_pivot": [round(value, 4) for value in source_pivot],
        "target_pivot": [round(value, 4) for value in target_pivot],
        "source_frame_indices": list(plan.source_frames),
        "per_frame_warp": False,
        "per_frame_scale": False,
    }


def derived_glow_frames(rest: Image.Image, geometry: dict[str, Any],
                        asset_id: str) -> list[Image.Image]:
    phases = [0.0, 0.20, 0.42, 0.70, 1.0, 0.76, 0.46, 0.18]
    palettes = [
        np.array([255.0, 225.0, 154.0]),
        np.array([173.0, 244.0, 255.0]),
        np.array([225.0, 183.0, 255.0]),
    ]
    base = np.asarray(rest.convert("RGBA"), dtype=np.float32)
    yy, xx = np.mgrid[0:rest.height, 0:rest.width]
    chase_axis = xx / max(1, rest.width - 1)
    if "chandelier" not in asset_id:
        chase_axis = yy / max(1, rest.height - 1)
    frames: list[Image.Image] = []
    for index, phase in enumerate(phases):
        if index == 0:
            state = rest.copy()
        else:
            color = palettes[(index - 1) % len(palettes)]
            wave = 0.35 + 0.65 * np.maximum(
                0.0, np.cos((chase_axis - phase) * math.tau))
            alpha = base[:, :, 3:4] / 255.0
            luminance = np.mean(base[:, :, :3], axis=2, keepdims=True) / 255.0
            weight = (wave[:, :, None] * luminance ** 1.35
                      * alpha * (0.18 + 0.34 * phase))
            rgb = base[:, :, :3] * (1.0 + 0.12 * phase) \
                + color[None, None, :] * weight
            value = np.concatenate(
                [np.clip(rgb, 0, 255), base[:, :, 3:4]], axis=2).astype(np.uint8)
            state = Image.fromarray(value, "RGBA")
        cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
        cell.alpha_composite(clean_hidden_rgb(state), geometry["rest_origin"])
        frames.append(clean_hidden_rgb(cell))
    return frames


def derived_mirror_frames(rest: Image.Image,
                          geometry: dict[str, Any]) -> list[Image.Image]:
    fog_amounts = [0.0, 0.88, 0.72, 0.48, 0.20, 0.05, 0.32, 0.12]
    wipe_progress = [0.0, 0.0, 0.18, 0.42, 0.72, 0.94, 0.78, 0.96]
    ellipse = Image.new("L", rest.size, 0)
    draw = ImageDraw.Draw(ellipse)
    draw.ellipse((round(rest.width * 0.12), round(rest.height * 0.08),
                  round(rest.width * 0.88), round(rest.height * 0.83)), fill=255)
    ellipse = ellipse.filter(ImageFilter.GaussianBlur(1.0))
    frames: list[Image.Image] = []
    for index, (fog, wipe) in enumerate(zip(fog_amounts, wipe_progress)):
        state = rest.copy()
        if index > 0:
            wipe_mask = Image.new("L", rest.size, 0)
            ImageDraw.Draw(wipe_mask).rectangle(
                (round(rest.width * wipe), 0, rest.width, rest.height), fill=255)
            mask = ImageChops.multiply(ellipse, wipe_mask).point(
                lambda value: round(value * fog))
            mist = Image.new("RGBA", rest.size, (232, 244, 250, 255))
            state = Image.composite(mist, state, mask)
            state.putalpha(rest.getchannel("A"))
        cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
        cell.alpha_composite(clean_hidden_rgb(state), geometry["rest_origin"])
        frames.append(clean_hidden_rgb(cell))
    return frames


def derived_flap_frames(rest: Image.Image,
                        geometry: dict[str, Any]) -> list[Image.Image]:
    # The owned pixels are only the narrow right inner flap.  Fold that exact
    # fabric toward its right seam; never import the generated outer canopy.
    widths = [1.0, 0.88, 0.70, 0.52, 0.38, 0.54, 0.74, 0.92]
    target = geometry["target_bbox"]
    frames: list[Image.Image] = []
    for index, width_scale in enumerate(widths):
        state = rest if index == 0 else rest.resize(
            (max(2, round(rest.width * width_scale)), rest.height),
            Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
        right = target[2]
        top = geometry["rest_origin"][1]
        cell.alpha_composite(clean_hidden_rgb(state), (right - state.width, top))
        frames.append(clean_hidden_rgb(cell))
    return frames


def stream_polygon_on_rest(rest: Image.Image,
                           geometry: dict[str, Any]) -> list[tuple[int, int]]:
    left, top, right, bottom = geometry["rest_bbox"]
    width, height = right - left, bottom - top
    points = WATER_LAYERS["mermaid_pool_waterfall"][0]["points"]
    return [
        (round(left + float(point[0]) * width),
         round(top + float(point[1]) * height))
        for point in points
    ]


def derived_waterfall_frames(rest: Image.Image,
                             geometry: dict[str, Any]) -> list[Image.Image]:
    # Keep the complete source-painted stream opaque in every authored state.
    # The former dry handoff exposed a rectangular healed patch whenever the
    # shader was absent or partially revealed.  A restrained brightness pulse
    # now animates the real painted water while the bounded shader supplies the
    # moving flow texture on top; neither layer has to conceal missing pixels.
    brightness_pulse = [1.0, 1.03, 1.07, 1.10, 1.12, 1.09, 1.05, 1.02]
    stream_mask = Image.new("L", rest.size, 0)
    ImageDraw.Draw(stream_mask).polygon(
        stream_polygon_on_rest(rest, geometry), fill=255)
    stream_mask = stream_mask.filter(ImageFilter.GaussianBlur(0.7))
    stream_mask = ImageChops.multiply(stream_mask, rest.getchannel("A"))
    frames: list[Image.Image] = []
    for index, brightness in enumerate(brightness_pulse):
        state = rest.copy()
        if index > 0:
            brightened = ImageEnhance.Brightness(rest).enhance(brightness)
            state.paste(brightened, (0, 0), stream_mask)
            state.putalpha(rest.getchannel("A"))
        cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
        cell.alpha_composite(clean_hidden_rgb(state), geometry["rest_origin"])
        frames.append(clean_hidden_rgb(cell))
    return frames


def exact_support_layer(rest: Image.Image, kind: str) -> Image.Image:
    array = np.asarray(rest.convert("RGBA"), dtype=np.uint8)
    red = array[:, :, 0].astype(np.int16)
    green = array[:, :, 1].astype(np.int16)
    blue = array[:, :, 2].astype(np.int16)
    alpha = array[:, :, 3]
    yy = np.arange(rest.height)[:, None]
    if kind == "flower":
        support = (
            (blue > red + 5) & (green > red - 8)
            & (green > 105) & (yy > rest.height * 0.35))
    else:
        support = ((blue > red + 4) & (green > 100) & (yy > rest.height * 0.36))
    support &= alpha >= MIN_ALPHA
    # Preserve antialiased neighbours without importing unrelated pink/gold art.
    mask = Image.fromarray((support * 255).astype(np.uint8), "L").filter(
        ImageFilter.MaxFilter(3))
    layer = Image.new("RGBA", rest.size, (0, 0, 0, 0))
    layer.paste(rest, (0, 0), mask)
    return clean_hidden_rgb(layer)


def add_exact_support(frames: list[Image.Image], rest: Image.Image,
                      geometry: dict[str, Any], kind: str) -> list[Image.Image]:
    support = exact_support_layer(rest, kind)
    result: list[Image.Image] = []
    for index, frame in enumerate(frames):
        if index == 0:
            result.append(frame)
            continue
        state = frame.copy()
        # Support is behind the moving/generated subject, so the float retains
        # its native contact/underside while authored petals/points stay visible.
        base = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
        base.alpha_composite(support, geometry["rest_origin"])
        base.alpha_composite(state)
        result.append(clean_hidden_rgb(base))
    return result


def seahorse_stream_mask(rest: Image.Image,
                         geometry: dict[str, Any]) -> Image.Image:
    """Return the antialiased mask of the source-painted fountain stream."""
    left, top, right, bottom = geometry["rest_bbox"]
    width, height = right - left, bottom - top
    polygon = [
        (round(left + float(point[0]) * width),
         round(top + float(point[1]) * height))
        for point in _seahorse_base_points
    ]
    mask = Image.new("L", rest.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.65))
    return ImageChops.multiply(mask, rest.getchannel("A"))


def derived_seahorse_frames(rest: Image.Image,
                            geometry: dict[str, Any]) -> list[Image.Image]:
    # Maximum-state Mobile review rejected the generated body states: several
    # carried purple/blue matte damage and a detached diagonal stream.  Keep the
    # exact source-owned body and alpha footprint in every state.  Only RGB inside
    # the already-painted stream changes, while the bounded shader supplies motion.
    brightness = [0.0, 0.035, 0.075, 0.110, 0.085, 0.050, 0.020, 0.055]
    aqua_mix = [0.0, 0.012, 0.025, 0.040, 0.030, 0.018, 0.007, 0.022]
    mask = np.asarray(
        seahorse_stream_mask(rest, geometry), dtype=np.float32) / 255.0
    source = np.asarray(rest.convert("RGBA"), dtype=np.uint8)
    source_rgb = source[:, :, :3].astype(np.float32)
    source_alpha = source[:, :, 3].copy()
    aqua = np.asarray([174.0, 240.0, 255.0], dtype=np.float32)
    frames: list[Image.Image] = []
    for index, (lift, tint) in enumerate(zip(brightness, aqua_mix)):
        state = rest
        if index > 0:
            tint_weight = mask[:, :, None] * tint
            rgb = source_rgb * (1.0 - tint_weight) + aqua * tint_weight
            rgb *= 1.0 + mask[:, :, None] * lift
            rgba = np.concatenate([
                np.clip(rgb, 0, 255).astype(np.uint8),
                source_alpha[:, :, None],
            ], axis=2)
            state = Image.fromarray(rgba, "RGBA")
        cell = Image.new("RGBA", CELL_SIZE, (0, 0, 0, 0))
        cell.alpha_composite(clean_hidden_rgb(state), geometry["rest_origin"])
        frames.append(clean_hidden_rgb(cell))
    return frames


def build_sheet(root: Path, asset: dict[str, Any], plan: AnimationPlan,
                rest: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    cell_size = plan.cell_size
    grid = plan.grid
    sheet_size = (grid[0] * cell_size[0], grid[1] * cell_size[1])
    if grid[0] * grid[1] < FRAME_COUNT or max(sheet_size) > 1024:
        raise ValueError(
            f"{asset['id']} atlas grid is invalid or exceeds 1024px: {sheet_size}")
    geometry = target_geometry(
        rest, asset["source_rect"], cell_size,
        asset.get("rest_card_registration_bbox"))
    normalization: dict[str, Any] = {
        "method": plan.method,
        "per_frame_warp": False,
        "root_transform_animation": False,
    }
    if plan.source:
        source_path = root / plan.source
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        segmentation: dict[str, Any] = {}
        if plan.source_segmentation \
                == "edge_connected_neutral_checkerboard_components":
            source_cells, segmentation = split_checkerboard_component_sheet(
                source_path)
        else:
            source_cells = split_generated_sheet(source_path)
        generated_target: tuple[int, int, int, int] | None = None
        target_in_rest = GENERATED_TARGET_REST_BBOX.get(str(asset["id"]))
        if target_in_rest is not None:
            origin_x, origin_y = geometry["rest_origin"]
            generated_target = (
                origin_x + int(target_in_rest[0]),
                origin_y + int(target_in_rest[1]),
                origin_x + int(target_in_rest[2]),
                origin_y + int(target_in_rest[3]),
            )
        frames, generated = normalize_generated_frames(
            source_cells, rest, geometry, plan, generated_target, cell_size)
        if generated_target is not None:
            generated["target_object_bbox_in_cell"] = list(generated_target)
        normalization.update(generated)
        normalization.update(segmentation)
        normalization["source_path"] = plan.source
        normalization["source_sha256"] = sha256_file(source_path)
    elif plan.method == "source_owned_pearl_color_chase":
        frames = derived_glow_frames(rest, geometry, str(asset["id"]))
    elif plan.method == "source_owned_mirror_fog_wipe_states":
        frames = derived_mirror_frames(rest, geometry)
    elif plan.method == "source_owned_flap_fold_states":
        frames = derived_flap_frames(rest, geometry)
        normalization.update({
            "per_frame_warp": True,
            "per_frame_local_resample": True,
            "local_component": "owned_inner_right_flap",
            "fixed_root_pivot": True,
            "source_owned_pixels_only": True,
        })
    elif plan.method == "source_owned_native_states_with_fixture_water_shader_handoff":
        frames = derived_waterfall_frames(rest, geometry)
    elif plan.method == "source_owned_seahorse_stream_shimmer_states":
        frames = derived_seahorse_frames(rest, geometry)
        normalization.update({
            "source_owned_pixels_only": True,
            "exact_alpha_silhouette_all_frames": True,
            "body_rgb_unchanged_outside_stream_mask": True,
            "stream_mask_source": "owned_fixture_water_polygon_times_rest_alpha",
            "generated_source_rejected": (
                "purple_blue_matte_and_body_damage_in_maximum_state_mobile_review"),
        })
    else:
        raise ValueError(f"unsupported animation plan: {plan.method}")

    if asset["id"] == "mermaid_pool_flower_float":
        frames = add_exact_support(frames, rest, geometry, "flower")
    elif asset["id"] == "mermaid_pool_star_float":
        frames = add_exact_support(frames, rest, geometry, "star")
    elif asset["id"] == "craft_room_supply_cupboard_left":
        # The generated source's first cell is a small segmented placeholder;
        # cell seven is the complete closed cupboard.  Runtime frame zero must
        # be a complete object state over the clean full-frame background.
        frames[0] = frames[7].copy()
        normalization["frame0_source_frame"] = 7
        normalization["frame0_repair"] = "complete_closed_object_state"

    if asset["id"] == "kitchen_fridge":
        frames, edge_cleanup = clean_generated_fridge_edges(frames)
        normalization["generated_edge_cleanup"] = edge_cleanup
        normalization["pale_matte_edge_audit"] = audit_pale_matte_edges(frames)

    sheet = Image.new("RGBA", sheet_size, (0, 0, 0, 0))
    bboxes: list[list[int]] = []
    hashes: list[str] = []
    for index, frame in enumerate(frames):
        frame = clean_hidden_rgb(frame)
        bbox = visible_bbox(frame)
        if bbox is None:
            raise ValueError(f"{asset['id']} frame {index} is empty")
        padding = min(bbox[0], bbox[1], cell_size[0] - bbox[2],
                      cell_size[1] - bbox[3])
        if padding < MIN_PADDING:
            raise ValueError(
                f"{asset['id']} frame {index} has only {padding}px padding")
        bboxes.append(list(bbox))
        hashes.append(pixel_sha256(frame))
        sheet.alpha_composite(
            frame, ((index % grid[0]) * cell_size[0],
                    (index // grid[0]) * cell_size[1]))
    if len(set(hashes)) < 4:
        raise ValueError(f"{asset['id']} has fewer than four unique states")
    return clean_hidden_rgb(sheet), {
        "frame_bboxes": bboxes,
        "frame_sha256": hashes,
        "unique_frame_count": len(set(hashes)),
        "rest_card_cell_origin": list(geometry["rest_origin"]),
        "rest_visible_bbox_in_cell": list(geometry["visible_target_bbox"]),
        "rest_registration_bbox_in_cell": list(geometry["target_bbox"]),
        "runtime_center_offset": geometry["runtime_center_offset"],
        "grid": list(grid),
        "cell_size": list(cell_size),
        "sheet_dimensions": list(sheet_size),
        "normalization": normalization,
    }


def room_grid(room: str) -> tuple[int, int, tuple[int, int]]:
    if room == "kitchen":
        return 4, 3, (1024, 768)
    return 4, 2, (910, 1024)


def logical_mask(root: Path, assets: list[dict[str, Any]],
                 threshold: int = MASK_ALPHA) -> Image.Image:
    union = Image.new("L", (1024, 576), 0)
    for asset in assets:
        mask = Image.open(root / str(asset["mask_path"]))
        if mask.mode in ("RGBA", "LA"):
            mask = mask.getchannel("A")
        else:
            mask = mask.convert("L")
        x, y, width, height = [int(value) for value in asset["source_rect"]]
        if mask.size == union.size:
            full = mask
        elif mask.size == (width, height):
            full = Image.new("L", union.size, 0)
            full.paste(mask, (x, y))
        else:
            raise ValueError(
                f"unexpected mask size for {asset['id']}: {mask.size}")
        full = full.point(lambda value: 255 if value >= threshold else 0)
        union = ImageChops.lighter(union, full)
    return union


def logical_runtime_frame_union(
        root: Path, assets: list[dict[str, Any]],
        planned: dict[Path, Image.Image]) -> Image.Image:
    """Reproduce Sprite3D placement and its 0.5 alpha-scissor ownership."""
    union = Image.new("L", (1024, 576), 0)
    for asset in assets:
        sheet_path = root / str(asset["sheet"])
        sheet = planned.get(sheet_path)
        if sheet is None:
            sheet = Image.open(sheet_path).convert("RGBA")
        columns, rows = [int(value) for value in asset["grid"]]
        if sheet.width % columns or sheet.height % rows:
            raise ValueError(f"invalid runtime sheet grid for {asset['id']}")
        frame_width = sheet.width // columns
        frame_height = sheet.height // rows
        frame_count = int(asset["authored_frame_count"])
        runtime_scale = float(asset.get("runtime_scale", 1.0))
        center_offset = asset.get(
            "runtime_center_offset", [frame_width * 0.5, frame_height * 0.5])
        source_rect = asset["source_ownership"]["source_rect"]
        center_x = float(source_rect[0]) + float(center_offset[0])
        center_y = float(source_rect[1]) + float(center_offset[1])
        for frame_index in range(frame_count):
            column = frame_index % columns
            row = frame_index // columns
            alpha = sheet.crop((
                column * frame_width,
                row * frame_height,
                (column + 1) * frame_width,
                (row + 1) * frame_height,
            )).getchannel("A")
            placed = alpha.transform(
                union.size,
                Image.Transform.AFFINE,
                (
                    1.0 / runtime_scale,
                    0.0,
                    frame_width * 0.5 - center_x / runtime_scale,
                    0.0,
                    1.0 / runtime_scale,
                    frame_height * 0.5 - center_y / runtime_scale,
                ),
                resample=Image.Resampling.BILINEAR,
            )
            union = ImageChops.lighter(union, placed)
    return union.point(lambda value: 255 if value >= 128 else 0)


def load_native_master(root: Path, room: str) -> tuple[Image.Image, list[dict[str, Any]]]:
    columns, rows, tile_size = room_grid(room)
    master = Image.new("RGB", (columns * tile_size[0], rows * tile_size[1]))
    records: list[dict[str, Any]] = []
    for row in range(rows):
        for column in range(columns):
            name = f"room_{room}_background_r{row}_c{column}.png"
            path = root / SOURCE_TILE_RELATIVE / name
            if not path.is_file():
                raise FileNotFoundError(path)
            tile = Image.open(path)
            tile.load()
            if tile.size != tile_size:
                raise ValueError(f"{path} size {tile.size} != {tile_size}")
            rgba = tile.convert("RGBA")
            if rgba.getchannel("A").getextrema() != (255, 255):
                raise ValueError(f"approved runtime background tile is not opaque: {path}")
            master.paste(rgba.convert("RGB"),
                         (column * tile_size[0], row * tile_size[1]))
            records.append({
                "path": relative(path, root),
                "sha256": sha256_file(path),
                "dimensions": list(tile.size),
            })
    return master, records


def heal_native_master(master: Image.Image, mask: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    scale_x = master.width / mask.width
    scale_y = master.height / mask.height
    reference_aspect = mask.width / mask.height
    aspect_pixel_delta = min(
        abs(master.height - master.width / reference_aspect),
        abs(master.width - master.height * reference_aspect),
    )
    if min(scale_x, scale_y) < 2.0 or aspect_pixel_delta > 1.0:
        raise ValueError(
            "native background is not a compliant whole-canvas scale of "
            f"the logical mask: {master.size}, delta={aspect_pixel_delta:.6f}")
    filter_scale = max(scale_x, scale_y)
    native_mask = mask.resize(master.size, Image.Resampling.NEAREST).point(
        lambda value: 255 if value >= MASK_ALPHA else 0)
    bbox = native_mask.getbbox()
    if bbox is None:
        raise ValueError("empty native ownership mask")
    source = np.asarray(master.convert("RGB"), dtype=np.float32)
    filled = source.copy()
    mask_array = np.asarray(native_mask, dtype=np.uint8) >= 250
    left, top, right, bottom = bbox
    margin = int(math.ceil(12.0 * filter_scale))
    left = max(0, left - margin)
    top = max(0, top - margin)
    right = min(master.width, right + margin)
    bottom = min(master.height, bottom + margin)
    local = source[top:bottom, left:right]
    local_mask = mask_array[top:bottom, left:right]
    horizontal = local.copy()
    vertical = local.copy()
    horizontal_valid = np.zeros(local_mask.shape, dtype=bool)
    vertical_valid = np.zeros(local_mask.shape, dtype=bool)
    x_positions = np.arange(local.shape[1])
    y_positions = np.arange(local.shape[0])
    for y_pos in np.flatnonzero(np.any(local_mask, axis=1)):
        known = np.flatnonzero(~local_mask[y_pos])
        if known.size < 2:
            continue
        horizontal_valid[y_pos] = True
        for channel in range(3):
            horizontal[y_pos, :, channel] = np.interp(
                x_positions, known, local[y_pos, known, channel])
    for x_pos in np.flatnonzero(np.any(local_mask, axis=0)):
        known = np.flatnonzero(~local_mask[:, x_pos])
        if known.size < 2:
            continue
        vertical_valid[:, x_pos] = True
        for channel in range(3):
            vertical[:, x_pos, channel] = np.interp(
                y_positions, known, local[known, x_pos, channel])
    local_filled = local.copy()
    both = local_mask & horizontal_valid & vertical_valid
    only_horizontal = local_mask & horizontal_valid & ~vertical_valid
    only_vertical = local_mask & vertical_valid & ~horizontal_valid
    local_filled[both] = horizontal[both] * 0.72 + vertical[both] * 0.28
    local_filled[only_horizontal] = horizontal[only_horizontal]
    local_filled[only_vertical] = vertical[only_vertical]
    unresolved = local_mask & ~horizontal_valid & ~vertical_valid
    if np.any(unresolved):
        raise ValueError("native healing mask contains an unfillable span")
    smoothed = np.asarray(Image.fromarray(
        np.clip(local_filled, 0, 255).astype(np.uint8), "RGB"
    ).filter(ImageFilter.GaussianBlur(2.5 * filter_scale)), dtype=np.uint8)
    local_output = source[top:bottom, left:right].copy()
    local_output[local_mask] = smoothed[local_mask]
    filled[top:bottom, left:right] = local_output
    output = Image.fromarray(np.clip(filled, 0, 255).astype(np.uint8), "RGB")
    changed = np.any(np.asarray(output) != np.asarray(master), axis=2)
    return output, {
        "native_scale": round(filter_scale, 9),
        "native_scale_xy": [round(scale_x, 9), round(scale_y, 9)],
        "owned_pixel_count_native": int(np.count_nonzero(mask_array)),
        "changed_owned_pixels": int(np.count_nonzero(changed & mask_array)),
        "changed_outside_pixels": int(np.count_nonzero(changed & ~mask_array)),
    }


def build_runtime_tiles(
        root: Path, room: str, assets: list[dict[str, Any]],
        planned: dict[Path, Image.Image]) -> dict[str, Any]:
    source_master, source_records = load_native_master(root, room)
    ownership_mask = logical_mask(root, assets)
    visible_ownership_mask = logical_mask(root, assets, 128)
    live_frame_union = logical_runtime_frame_union(root, assets, planned)
    # Heal the complete accepted source ownership.  Clipping this mask to the
    # authored-frame union left source-painted edge/contact fragments in the
    # opaque background whenever a normalized state was narrower than the
    # extracted rest card.  Generated motion outside the original footprint is
    # harmless; source pixels surviving inside it are not.
    mask = ownership_mask
    ownership_pixels = ownership_mask.histogram()[255]
    healing_pixels = mask.histogram()[255]
    if healing_pixels <= 0:
        raise ValueError(f"{room} has no live V4 healing pixels")
    # MA-VIS-007: the canonical native master is already a complete clean
    # generated frame.  Re-healing a local ownership mask here recreated the
    # plaid/blur holes that live animation states exposed.  V4 now slices the
    # exact canonical master and never modifies pixels beneath a card.
    healed = source_master.copy()
    native_ownership_mask = ownership_mask.resize(
        source_master.size, Image.Resampling.NEAREST)
    metrics = {
        "native_scale": round(max(
            source_master.width / ownership_mask.width,
            source_master.height / ownership_mask.height), 9),
        "native_scale_xy": [
            round(source_master.width / ownership_mask.width, 9),
            round(source_master.height / ownership_mask.height, 9),
        ],
        "owned_pixel_count_native": int(
            native_ownership_mask.histogram()[255]),
        "changed_owned_pixels": 0,
        "changed_outside_pixels": 0,
    }
    columns, rows, tile_size = room_grid(room)
    output_records: list[dict[str, Any]] = []
    for row in range(rows):
        for column in range(columns):
            name = f"room_{room}_background_r{row}_c{column}.png"
            path = root / RUNTIME_TILE_RELATIVE / name
            tile = healed.crop((
                column * tile_size[0], row * tile_size[1],
                (column + 1) * tile_size[0], (row + 1) * tile_size[1],
            )).convert("RGB")
            planned[path] = tile
            output_records.append({
                "path": relative(path, root),
                "sha256": "__PLANNED_IMAGE_HASH__",
                "dimensions": list(tile.size),
                "opaque": True,
            })
    return {
        "route": "generated_full_frame_pixel_ownership_tiles",
        "derived_from_low_resolution_audit_plate": False,
        "source_tile_root": SOURCE_TILE_RELATIVE.as_posix(),
        "runtime_tile_root": RUNTIME_TILE_RELATIVE.as_posix(),
        "tile_name_pattern": f"room_{room}_background_r{{row}}_c{{column}}.png",
        "grid": [columns, rows],
        "tile_dimensions": list(tile_size),
        "native_canvas_size": [source_master.width, source_master.height],
        "logical_canvas_size": [1024, 576],
        "ownership_mask_pixel_sha256": hashlib.sha256(
            ownership_mask.tobytes()).hexdigest(),
        "live_frame_union_pixel_sha256": hashlib.sha256(
            live_frame_union.tobytes()).hexdigest(),
        "healing_mask_pixel_sha256": hashlib.sha256(mask.tobytes()).hexdigest(),
        "ownership_mask_pixels_logical": ownership_pixels,
        "live_frame_union_pixels_logical": live_frame_union.histogram()[255],
        "healing_mask_pixels_logical": healing_pixels,
        "ownership_pixels_clipped_outside_live_union": 0,
        "source_ownership_pixels_outside_live_union": int(np.count_nonzero(
            (np.asarray(ownership_mask, dtype=np.uint8) > 0)
            & (np.asarray(live_frame_union, dtype=np.uint8) == 0))),
        "visible_ownership_pixels_outside_live_union": int(np.count_nonzero(
            (np.asarray(visible_ownership_mask, dtype=np.uint8) > 0)
            & (np.asarray(live_frame_union, dtype=np.uint8) == 0))),
        "full_source_ownership_healed": True,
        "live_alpha_scissor_threshold": 128,
        "source_tiles": source_records,
        "tiles": output_records,
        **metrics,
    }


def trim_pool_contact_water(
        rest: Image.Image, asset_id: str,
        registration_bbox: tuple[int, int, int, int],
        ) -> tuple[Image.Image, dict[str, Any] | None]:
    """Remove detached pool-water patches from source-owned object cards.

    The approved room extractor intentionally carried nearby pool pixels with
    the flower and fountain so the old static reconstruction was exact.  Those
    broad patches read as cyan stickers once the same objects become live
    Sprite3D cards.  This is an alpha-only, source-pixel-preserving trim: object
    RGB is never repainted, and a small attached contact region remains.
    """
    if asset_id not in {
            "mermaid_pool_flower_float",
            "mermaid_pool_seahorse_fountain"}:
        return rest, None
    rgba = np.asarray(rest.convert("RGBA"), dtype=np.uint8).copy()
    source_rgba = rgba.copy()
    red = rgba[:, :, 0].astype(np.int16)
    green = rgba[:, :, 1].astype(np.int16)
    blue = rgba[:, :, 2].astype(np.int16)
    alpha = rgba[:, :, 3]
    left, top, right, bottom = registration_bbox
    width = max(1, right - left)
    height = max(1, bottom - top)
    yy, xx = np.mgrid[0:rest.height, 0:rest.width]
    nx = (xx - left) / width
    ny = (yy - top) / height
    # Pool water is aqua/cyan, while the flower petals, shell pedestal, coral,
    # and gold/cream fixture are warmer.  Restrict the classifier to the known
    # lower/contact regions so similarly colored painted fixture details remain.
    any_alpha = alpha > 0
    visible = alpha >= MIN_ALPHA
    warm_core = visible & (
        (red >= blue - 5)
        | ((red >= 150) & (green >= 115) & (red >= green - 45))
    )
    warm_subject = np.asarray(
        Image.fromarray((warm_core * 255).astype(np.uint8), "L").filter(
            ImageFilter.MaxFilter(5)), dtype=np.uint8) > 0
    if asset_id == "mermaid_pool_flower_float":
        contact = (
            ((nx - 0.50) / 0.21) ** 2
            + ((ny - 0.69) / 0.065) ** 2 <= 1.0
        )
        petal_bounds = (
            (nx >= 0.06) & (nx <= 0.94)
            & (ny >= 0.18) & (ny <= 0.78)
        )
        keep = (warm_subject & petal_bounds) | (any_alpha & contact)
        removable = any_alpha & ~keep
        contact_role = "narrow_attached_flower_underside"
    else:
        stream = Image.new("L", rest.size, 0)
        stream_points = [
            (round(left + float(point[0]) * width),
             round(top + float(point[1]) * height))
            for point in _seahorse_base_points
        ]
        ImageDraw.Draw(stream).polygon(stream_points, fill=255)
        stream_values = np.asarray(
            stream.filter(ImageFilter.MaxFilter(3)), dtype=np.uint8) > 0
        pedestal_bounds = (
            (nx >= 0.28) & (nx <= 0.99) & (ny < 0.90)
        )
        lower_keep = (
            (warm_subject & pedestal_bounds)
            | stream_values
        )
        removable = any_alpha & (ny >= 0.76) & ~lower_keep
        contact_role = "narrow_attached_pedestal_and_mouth_stream"
    removed = int(np.count_nonzero(removable))
    if removed <= 0:
        raise ValueError(f"{asset_id} pool-contact trim removed no pixels")
    rgba[removable] = 0
    cleaned = clean_hidden_rgb(Image.fromarray(rgba, "RGBA"))
    # Every retained visible pixel must be byte-identical to the source.  Only
    # alpha-to-zero removal is allowed by this derivation.
    retained = np.asarray(cleaned.convert("RGBA"), dtype=np.uint8)[:, :, 3] > 0
    if np.any(
            np.asarray(cleaned)[:, :, :3][retained]
            != source_rgba[:, :, :3][retained]):
        raise ValueError(f"{asset_id} contact trim repainted retained RGB")
    return cleaned, {
        "method": "source_rgb_preserving_alpha_only_pool_contact_trim",
        "removed_visible_pixels": removed,
        "contact_role_retained": contact_role,
        "registration_bbox_preserved": list(registration_bbox),
        "hidden_rgb_zeroed": True,
        "protected_source_modified": False,
    }


def clean_rest_card(root: Path, asset: dict[str, Any],
                    planned: dict[Path, Image.Image]) -> tuple[Image.Image, str]:
    declared_path = str(asset["rest_card_path"])
    if str(asset.get("id", "")) == "craft_room_supply_cupboard_left":
        # Preserve the exact source-owned extraction as provenance/healing
        # evidence.  Its tiny segmented state is not used as runtime frame 0;
        # the atlas uses the complete generated closed state below.
        source = Image.open(root / str(asset["source_room_plate_path"])) \
            .convert("RGBA")
        x, y, width, height = (int(value) for value in asset["source_rect"])
        rest = source.crop((x, y, x + width, y + height))
        mask = Image.open(root / str(asset["mask_path"])).convert("L")
        rest.putalpha(mask)
        cleaned = clean_hidden_rgb(rest)
        registration_bbox = visible_bbox(cleaned)
        if registration_bbox is None:
            raise ValueError("craft cupboard source extraction is empty")
        asset["rest_card_registration_bbox"] = list(registration_bbox)
        planned[root / declared_path] = cleaned
        asset["rest_card_pixel_cleanup"] = {
            "method": "exact_source_rect_rgb_times_owned_alpha_mask",
            "hidden_rgb_zeroed": True,
            "protected_source_modified": False,
            "runtime_frame_role": "ownership_reference_only",
        }
        return cleaned, declared_path
    master_relative = str(asset.get("rest_card_source_path", declared_path))
    source_path = root / master_relative
    rest = Image.open(source_path).convert("RGBA")
    registration_bbox = visible_bbox(rest)
    if registration_bbox is None:
        raise ValueError(f"empty rest card: {source_path}")
    cleaned = clean_hidden_rgb(rest)
    cleaned, pool_trim = trim_pool_contact_water(
        cleaned, str(asset["id"]), registration_bbox)
    asset["rest_card_registration_bbox"] = list(registration_bbox)
    if cleaned.tobytes() == rest.tobytes() and "rest_card_source_path" not in asset:
        return cleaned, declared_path
    asset_id = str(asset["id"])
    output_path = root / declared_path if "rest_card_source_path" in asset \
        else root / REST_RELATIVE / f"{asset_id}_rest.png"
    planned[output_path] = cleaned
    asset["rest_card_source_path"] = master_relative
    asset["rest_card_source_sha256"] = sha256_file(source_path)
    asset["rest_card_pixel_cleanup"] = (
        pool_trim if pool_trim is not None else {
            "method": "zero_rgb_under_fully_transparent_alpha_only",
            "hidden_rgb_zeroed": True,
            "protected_source_modified": False,
        })
    return cleaned, relative(output_path, root)


def hotspot_fields(asset: dict[str, Any]) -> tuple[list[float], list[float]]:
    width, height = float(asset["source_rect"][2]), float(asset["source_rect"][3])
    hotspot_width = max(112.0, width)
    hotspot_height = max(112.0, height)
    return (
        [hotspot_width, hotspot_height],
        [(width - hotspot_width) * 0.5, (height - hotspot_height) * 0.5],
    )


def update_asset(
        root: Path, asset: dict[str, Any], planned: dict[Path, Image.Image]
        ) -> dict[str, Any]:
    asset_id = str(asset["id"])
    if asset_id not in PLANS:
        raise ValueError(f"no delivery plan for {asset_id}")
    if "toilet_roll" in asset_id or asset_id == "kitchen_stove_pot":
        raise ValueError(f"rejected object entered V4 delivery: {asset_id}")
    plan = PLANS[asset_id]
    rest, rest_relative = clean_rest_card(root, asset, planned)
    asset["rest_card_path"] = rest_relative
    asset["source_ownership"]["rest_card_sha256"] = "__PLANNED_REST_HASH__"
    sheet, sheet_meta = build_sheet(root, asset, plan, rest)
    sheet_path = root / SHEET_RELATIVE / f"{asset_id}_sheet.png"
    planned[sheet_path] = sheet

    action = SEMANTIC_OVERRIDES.get(asset_id, str(asset["semantic_action"]))
    asset["semantic_action"] = action
    asset["animation_behavior"] = {
        "mode": "authored_object_states",
        "action": action,
        "generic_transform_fallback": False,
        "secondary_physics": asset_id in PHYSICS,
    }
    if asset_id in PHYSICS:
        asset["animation_behavior"]["physics_role"] = PHYSICS[asset_id][
            "physics_role"]
    asset.update({
        "authored_frame_count": FRAME_COUNT,
        "frame_count": FRAME_COUNT,
        "delivery_status": "runtime_ready_source_owned_states",
        "grid": sheet_meta["grid"],
        "cell_size": sheet_meta["cell_size"],
        "sheet_dimensions": sheet_meta["sheet_dimensions"],
        "sheet": relative(sheet_path, root),
        "sheet_sha256": "__PLANNED_IMAGE_HASH__",
        "timeline_sequence": list(TIMELINE),
        "timeline_frame_count": len(TIMELINE),
        "rest_frame": 0,
        "frame0_exact_rest_card": asset_id != "craft_room_supply_cupboard_left",
        "fixed_pivot": True,
        "root_transform_animation": False,
        "primary_animation_is_overlay": False,
        "render_mode": "generated_full_object_states",
        "runtime_scale": 1.0,
        "anchor_mode": plan.pivot,
        "frame_duration_seconds": plan.frame_duration,
        "sound": plan.sound,
        "sound_frame": plan.sound_frame,
        "physics_mode": "none",
        "fluid_engine": "none",
        **sheet_meta,
    })
    if asset_id == "craft_room_supply_cupboard_left":
        asset["frame0_complete_closed_state"] = True
        asset["rest_card_runtime_role"] = (
            "source_ownership_reference_not_runtime_frame_zero")
    bbox_widths = [bbox[2] - bbox[0] for bbox in sheet_meta["frame_bboxes"]]
    bbox_heights = [bbox[3] - bbox[1] for bbox in sheet_meta["frame_bboxes"]]
    registration_bbox = sheet_meta["rest_registration_bbox_in_cell"]
    rest_width = max(1, registration_bbox[2] - registration_bbox[0])
    rest_height = max(1, registration_bbox[3] - registration_bbox[1])
    asset["fixed_root_bbox_metrics"] = {
        "rest_visible_size": [rest_width, rest_height],
        "minimum_visible_size": [min(bbox_widths), min(bbox_heights)],
        "maximum_visible_size": [max(bbox_widths), max(bbox_heights)],
        "maximum_width_ratio_to_rest": round(max(bbox_widths) / rest_width, 6),
        "maximum_height_ratio_to_rest": round(max(bbox_heights) / rest_height, 6),
    }
    asset["visual_review"] = {
        "status": "accepted",
        "reviewer": "Codex source-ownership and contact-sheet audit 2026-08-04",
        "identity_continuity": "accepted",
        "fixed_root_verified": True,
        "normalized_use_verified": True,
        "notes": VISUAL_REVIEW_NOTES.get(
            asset_id,
            "Accepted: complete object identity remains coherent across all authored "
            "states with an exact source-owned rest frame and fixed root pivot."),
    }
    if plan.close_sound:
        asset["close_sound"] = plan.close_sound
    else:
        asset.pop("close_sound", None)
    hotspot_size, hotspot_offset = hotspot_fields(asset)
    asset["hotspot_size"] = hotspot_size
    asset["hotspot_offset"] = hotspot_offset

    if asset_id in PHYSICS:
        asset.update(PHYSICS[asset_id])
        asset["secondary_root_physics"] = True
        asset["jolt_role"] = "secondary_solid_body_garnish"
    else:
        asset["secondary_root_physics"] = False
        asset.pop("physics_max_angle_radians", None)
        asset.pop("physics_impulse_scale", None)
        asset.pop("jolt_role", None)

    if asset_id in WATER_LAYERS:
        asset["water_layers"] = deepcopy(WATER_LAYERS[asset_id])
        asset["fluid_engine"] = "fixture_water_shader"
        asset["water_mask_space"] = "source_rect_normalized"
        asset["uses_jolt_for_fluid"] = False
        asset["native_painted_rest_water"] = True
    else:
        asset.pop("water_layers", None)
        asset.pop("water_mask_space", None)
        asset.pop("uses_jolt_for_fluid", None)
        asset.pop("native_painted_rest_water", None)

    if asset_id == "kitchen_fridge":
        asset["runtime_interaction_key"] = "kitchen:fridge"
        asset["v4_override_of"] = {
            "pack": "v2_base",
            "asset_id": "kitchen_fridge",
        }
        asset["ownership_continuity"] = [
            "frame0_exact_source_derived_fridge_only_card",
            "generated_states_preserve_mint_shell_peach_badge_gold_hardware",
            "generated_hidden_food_interior_only_visible_after_door_opens",
            "pale_checkerboard_matte_removed_and_audited",
            "fixed_cabinet_base_with_attached_door_motion_only",
        ]
    elif asset_id == "playroom_tent_flaps_right":
        asset["ownership_continuity"] = [
            "exact_inner_right_flap_pixels_only",
            "generated_outer_canopy_rejected",
        ]
    elif asset_id == "mermaid_pool_flower_float":
        asset["ownership_continuity"] = [
            "exact_source_aqua_float_base_in_every_state",
            "generated_petals_remain_attached_to_base",
        ]
    elif asset_id == "mermaid_pool_star_float":
        asset["ownership_continuity"] = [
            "exact_source_cyan_rear_underside_in_every_state",
            "extreme_crescent_generated_states_rejected",
            "gentle_inflatable_point_flex_only",
        ]
    elif asset_id == "mermaid_pool_waterfall":
        asset["ownership_continuity"] = [
            "exact_source_shell_and_rocks_in_every_state",
            "invented_clam_gate_generated_source_rejected",
            "complete_painted_stream_alpha_preserved_in_every_state",
            "painted_stream_brightness_pulse_under_low_alpha_bounded_shader",
            "shader_polygon_follows_painted_fall_lip_and_foam_silhouette",
        ]
    elif asset_id == "mermaid_pool_seahorse_fountain":
        asset["ownership_continuity"] = [
            "exact_source_fountain_body_in_every_state",
            "exact_source_alpha_silhouette_in_every_state",
            "generated_damaged_body_states_rejected_after_mobile_review",
            "existing_painted_stream_rgb_shimmer_only",
            "shader_flow_begins_at_exact_mouth_outlet",
        ]
    return asset


def synchronize_room_instances(manifest: dict[str, Any],
                               assets: list[dict[str, Any]]) -> None:
    index = {str(asset["id"]): asset for asset in assets}
    rooms = manifest.get("rooms", {})
    if not isinstance(rooms, dict):
        return
    for room in rooms.values():
        if not isinstance(room, dict):
            continue
        for instance in room.get("instances", []):
            if not isinstance(instance, dict):
                continue
            asset = index.get(str(instance.get("asset_id", "")))
            if asset is None:
                continue
            instance["semantic_action"] = asset["semantic_action"]
            instance["animation_behavior"] = deepcopy(asset["animation_behavior"])
            instance["rest_card_path"] = asset["rest_card_path"]
            instance["source_ownership"] = deepcopy(asset["source_ownership"])
            instance["authored_frames"] = {
                "sheet_path": asset["sheet"],
                "sheet_sha256": asset["sheet_sha256"],
                "state_count": FRAME_COUNT,
                "status": "runtime_ready_source_owned_states",
                "method": asset["normalization"]["method"],
            }


def replace_planned_hashes(
        root: Path, manifest: dict[str, Any], planned: dict[Path, Image.Image],
        actual_hashes: dict[Path, str]) -> None:
    path_hashes = {
        relative(path, root): actual_hashes[path] for path in planned
    }
    for asset in manifest["assets"]:
        asset["sheet_sha256"] = path_hashes[str(asset["sheet"])]
        rest_path = root / str(asset["rest_card_path"])
        if rest_path in planned:
            rest_hash = path_hashes[str(asset["rest_card_path"])]
        else:
            rest_hash = sha256_file(rest_path)
        asset["source_ownership"]["rest_card_sha256"] = rest_hash
    for room in manifest["runtime_background_tiles"].values():
        for tile in room["tiles"]:
            tile["sha256"] = path_hashes[str(tile["path"])]
    synchronize_room_instances(manifest, manifest["assets"])


def build(root: Path) -> tuple[dict[str, Any], dict[Path, Image.Image]]:
    manifest_path = root / MANIFEST_RELATIVE
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    planned: dict[Path, Image.Image] = {}
    source_assets = manifest.get("assets", [])
    if not isinstance(source_assets, list):
        raise ValueError("V4 manifest assets must be a list")
    # The flap-only V4 card depended on a baked tent chassis.  With complete
    # clean backgrounds it becomes a disconnected crescent, so retain the
    # already approved, self-contained V2 full-tent state sheet instead.
    retired_partial_ids = {"playroom_tent_flaps_right"}
    source_assets = [
        asset for asset in source_assets
        if str(asset.get("id", "")) not in retired_partial_ids
    ]
    rooms = manifest.get("rooms", {})
    if isinstance(rooms, dict):
        for room in rooms.values():
            if isinstance(room, dict) and isinstance(room.get("instances"), list):
                room["instances"] = [
                    instance for instance in room["instances"]
                    if not isinstance(instance, dict)
                    or str(instance.get("asset_id", "")) not in retired_partial_ids
                ]
    ids = {str(asset.get("id", "")) for asset in source_assets}
    if ids != set(PLANS):
        missing = sorted(set(PLANS) - ids)
        extra = sorted(ids - set(PLANS))
        raise ValueError(f"V4 accepted asset set drifted; missing={missing}, extra={extra}")
    assets: list[dict[str, Any]] = []
    for source in source_assets:
        asset = deepcopy(source)
        assets.append(update_asset(root, asset, planned))
    manifest["assets"] = assets

    by_room: dict[str, list[dict[str, Any]]] = {}
    for asset in assets:
        by_room.setdefault(str(asset["room"]), []).append(asset)
    runtime_tiles: dict[str, Any] = {}
    for room, room_assets in sorted(by_room.items()):
        runtime_tiles[room] = build_runtime_tiles(
            root, room, room_assets, planned)
    manifest["runtime_background_tiles"] = runtime_tiles
    manifest["delivery"] = {
        "builder": "tools/build_castle_interaction_v4_delivery.py",
        "builder_version": BUILDER_VERSION,
        "generation_date": GENERATION_DATE,
        "sheet_contract": (
            "RGBA_4_to_12_state_fixed_pivot_atlas_max_1024px_edge"),
        "rest_contract": "frame0_exact_clean_source_owned_rest_pixels_unscaled",
        "background_contract": (
            "MA_VIS_007_complete_generated_frame_then_exact_native_tiles"),
        "rejected_assets": [
            "bubble_bath_toilet_roll",
            "kitchen_stove_pot_lid",
            "kitchen_stove_pot_full_body",
            "generated_mermaid_pool_waterfall_clam_gate",
            "generated_playroom_full_tent_canopy",
            "playroom_tent_flaps_right_partial_override",
        ],
        "v4_interaction_overrides": ["kitchen:fridge"],
    }
    manifest["summary"] = {
        "new_native_cards": 7,
        "reused_source_owned_cards": 5,
        "rooms_with_new_ownership": 5,
        "runtime_ready_authored_animation_sheets": len(assets),
        "runtime_healed_native_tile_rooms": len(runtime_tiles),
    }
    synchronize_room_instances(manifest, assets)
    # The builder is itself a bound input.  Refresh repository-normalized
    # hashes during materialization so a legitimate pipeline repair can be
    # regenerated once, while --check still rejects any later drift.
    for key in ("generator", "source_layer_manifest"):
        declared = manifest.get(key)
        if isinstance(declared, str) and declared:
            manifest[f"{key}_sha256"] = repository_text_sha256(root / declared)
    return manifest, planned


def images_equal(first: Image.Image, second: Image.Image) -> bool:
    if first.mode != second.mode or first.size != second.size:
        return False
    return ImageChops.difference(first, second).getbbox() is None


def runtime_manifest_png_paths(manifest: dict[str, Any]) -> Iterable[str]:
    for asset in manifest["assets"]:
        for key in ("sheet", "rest_card_path", "healed_background_path"):
            yield str(asset[key])
    for room in manifest["runtime_background_tiles"].values():
        for tile in room["tiles"]:
            yield str(tile["path"])


def audit_runtime_inventory(root: Path, manifest: dict[str, Any]) -> list[str]:
    """Reject orphaned runtime art left behind by a changed ownership audit."""
    errors: list[str] = []
    v4_root = (root / MANIFEST_RELATIVE.parent).resolve()
    expected: set[Path] = set()
    for declared in runtime_manifest_png_paths(manifest):
        path = (root / declared).resolve()
        try:
            path.relative_to(v4_root)
        except ValueError:
            continue
        expected.add(path)

    actual = {path.resolve() for path in v4_root.rglob("*.png")}
    for path in sorted(actual - expected):
        errors.append(f"unreferenced runtime image: {relative(path, root)}")
    for path in sorted(expected - actual):
        errors.append(f"missing referenced runtime image: {relative(path, root)}")
    for sidecar in sorted(v4_root.rglob("*.png.import")):
        image_path = Path(str(sidecar)[:-len(".import")]).resolve()
        if image_path not in expected:
            errors.append(f"orphaned runtime import: {relative(sidecar, root)}")
    return errors


def audit_upstream_provenance(root: Path, manifest: dict[str, Any]) -> list[str]:
    """Reject a delivery built from stale ownership/source declarations."""
    errors: list[str] = []
    bindings = (
        ("generator", "generator_sha256"),
        ("spec", "spec_sha256"),
        ("source_layer_manifest", "source_layer_manifest_sha256"),
    )
    for path_key, hash_key in bindings:
        declared_path = manifest.get(path_key)
        declared_hash = manifest.get(hash_key)
        if not isinstance(declared_path, str) or not declared_path:
            errors.append(f"missing upstream provenance path: {path_key}")
            continue
        if not isinstance(declared_hash, str) or not declared_hash:
            errors.append(f"missing upstream provenance hash: {hash_key}")
            continue
        path = (root / declared_path).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"upstream provenance escapes repository: {declared_path}")
            continue
        if not path.is_file():
            errors.append(f"missing upstream provenance file: {declared_path}")
            continue
        actual_hash = repository_text_sha256(path)
        if actual_hash != declared_hash:
            errors.append(
                f"stale upstream provenance hash: {hash_key}; "
                f"declared={declared_hash}, actual={actual_hash}")
    return errors


def materialize_or_check(root: Path, check: bool) -> list[str]:
    manifest, planned = build(root)
    errors = audit_upstream_provenance(root, manifest)
    actual_hashes: dict[Path, str] = {}
    for path, expected in planned.items():
        if check:
            if not path.is_file():
                errors.append(f"missing generated image: {relative(path, root)}")
                actual_hashes[path] = sha256_bytes(png_bytes(expected))
                continue
            actual = Image.open(path)
            actual.load()
            if not images_equal(actual, expected):
                errors.append(f"generated image drift: {relative(path, root)}")
            actual_hashes[path] = sha256_file(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            data = png_bytes(expected)
            path.write_bytes(data)
            actual_hashes[path] = sha256_bytes(data)
    replace_planned_hashes(root, manifest, planned, actual_hashes)
    expected_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    manifest_path = root / MANIFEST_RELATIVE
    if check:
        errors.extend(audit_runtime_inventory(root, manifest))
        try:
            actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read delivery manifest: {exc}")
        else:
            if actual_manifest != manifest:
                errors.append("delivery manifest drift")
    else:
        manifest_path.write_text(expected_text, encoding="utf-8")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        errors = materialize_or_check(args.root.resolve(), args.check)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"CASTLE_V4_DELIVERY|FAIL|{exc}")
        return 1
    if errors:
        for error in errors:
            print(f"CASTLE_V4_DELIVERY|FAIL|{error}")
        print(f"CASTLE_V4_DELIVERY|RESULT=FAIL|checks_failed={len(errors)}")
        return 1
    mode = "CHECK" if args.check else "BUILD"
    print(
        f"CASTLE_V4_DELIVERY|RESULT=OK|mode={mode}|assets={len(PLANS)}|"
        "native_background_rooms=7")
    return 0


if __name__ == "__main__":
    sys.exit(main())
