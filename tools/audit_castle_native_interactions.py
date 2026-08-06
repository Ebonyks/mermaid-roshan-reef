#!/usr/bin/env python3
"""Deterministic source-ownership gate for Pearl Castle interactions.

An interaction passes only when its rest card is measurably the object painted
in its room, the shipped room surface has been healed underneath it, and the
runtime animation is a clean, padded sequence of authored object states.  The
gate does not accept prompt provenance, visual-review labels, or plausible new
props as substitutes for pixel ownership.

V4 manifest contract
--------------------
``assets/flats/castle/interactions_v4/castle_interactions_v4.json`` contains an
``assets`` list.  Every active V4 asset owns exactly one runtime instance and
uses ``pack: v4_native``.  Alongside the normal sheet/grid/timeline fields it
contains:

* ``source_rect``: ``[x, y, width, height]`` in 1024x576 room coordinates
  (3344x941 for the main hall); runtime placement is derived from this rect;
* ``rest_card_path``, ``healed_background_path``, and ``mask_path``;
* optional ``source_room_plate_path`` (otherwise ``room_<room>.png``);
* ``source_ownership`` with the four required true flags, the same
  ``source_rect``, and file hashes ``source_room_plate_sha256``,
  ``healed_background_sha256``, ``rest_card_sha256``; and
* ``animation_behavior`` with ``mode: authored_object_states``, an ``action``
  exactly matching ``semantic_action``, and
  ``generic_transform_fallback: false``.

The audit independently decodes every image and remeasures the evidence.  It
also rejects any runtime route that can still load ``pack: v3_addition``.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy.ndimage import label as component_label


ROOT = Path(__file__).resolve().parents[1]
V4_RELATIVE = Path(
    "assets/flats/castle/interactions_v4/castle_interactions_v4.json"
)
V2_RELATIVE = Path(
    "assets/flats/castle/interactions_v2/castle_interactions_v2.json"
)
FIXTURE_RUNTIME_RELATIVE = Path("scripts/arena/castle_fixture_rigs.gd")
ROOM_RUNTIME_RELATIVE = Path("scripts/arena/castle_rooms_25d.gd")
V4_TILE_RELATIVE = Path("assets/flats/castle/interactions_v4/background_tiles")

ALPHA_VISIBLE = 16
ALPHA_COMPARE = 48
MIN_PADDING = 6
MIN_FRAMES = 4
MAX_FRAMES = 12
KEY_RGB = (255, 0, 255)
SOURCE_TOLERANCE = 32
DUPLICATE_TOLERANCE = 4
HEALING_TOLERANCE = 4
SOURCE_MATCH_MIN = 0.84
REST_STATE_MATCH_MIN = 0.80
DUPLICATE_MATCH_MAX = 0.18
HEALED_CHANGE_MIN = 0.45
OUTSIDE_DIFF_TOLERANCE = 18
OUTSIDE_CHANGE_MAX = 0.005
ROOM_SIZE = defaultdict(lambda: (1024, 576), {"main_hall": (3344, 941)})


def add_error(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, label: str, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        add_error(errors, f"{label}: missing {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"{label}: cannot parse JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        add_error(errors, f"{label}: root must be an object")
        return {}
    return value


def repository_file(root: Path, value: Any, label: str,
                    errors: list[str]) -> Path | None:
    text = str(value or "").replace("\\", "/").removeprefix("res://")
    if not text:
        add_error(errors, f"{label}: missing path")
        return None
    path = (root / text).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        add_error(errors, f"{label}: path escapes repository: {text}")
        return None
    if not path.is_file():
        add_error(errors, f"{label}: missing file {text}")
        return None
    return path


def verify_file_hash(path: Path | None, expected: Any, label: str,
                     errors: list[str]) -> bool:
    if path is None:
        return False
    expected_text = str(expected or "")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_text):
        add_error(errors, f"{label}: missing lowercase file SHA-256")
        return False
    measured = sha256(path)
    if measured != expected_text:
        add_error(errors, f"{label}: stale file SHA-256; measured {measured}")
        return False
    return True


def image_rgba(path: Path | None, label: str,
               errors: list[str]) -> Image.Image | None:
    if path is None:
        return None
    try:
        image = Image.open(path)
        image.load()
    except (OSError, ValueError) as exc:
        add_error(errors, f"{label}: cannot decode image: {exc}")
        return None
    if image.mode != "RGBA":
        add_error(errors, f"{label}: must be stored as RGBA, found {image.mode}")
        image = image.convert("RGBA")
    return image


def image_surface(path: Path | None, label: str,
                  errors: list[str]) -> Image.Image | None:
    """Decode an opaque room surface; RGB storage is expected and valid."""
    if path is None:
        return None
    try:
        image = Image.open(path)
        image.load()
    except (OSError, ValueError) as exc:
        add_error(errors, f"{label}: cannot decode image: {exc}")
        return None
    if image.mode not in ("RGB", "RGBA"):
        add_error(errors, f"{label}: room surface must be RGB/RGBA, found {image.mode}")
    return image.convert("RGBA")


def image_mask(path: Path | None, label: str,
               errors: list[str]) -> Image.Image | None:
    if path is None:
        return None
    try:
        image = Image.open(path)
        image.load()
    except (OSError, ValueError) as exc:
        add_error(errors, f"{label}: cannot decode image: {exc}")
        return None
    if image.mode not in ("1", "L", "LA", "RGBA"):
        add_error(errors, f"{label}: mask must be binary/grayscale/alpha, found {image.mode}")
    if image.mode in ("LA", "RGBA") and image.getchannel("A").getbbox() is not None:
        return image.getchannel("A")
    return image.convert("L")


def numeric_list(value: Any, count: int) -> list[float] | None:
    if not isinstance(value, list) or len(value) != count:
        return None
    if any(isinstance(component, bool)
           or not isinstance(component, (int, float)) for component in value):
        return None
    return [float(component) for component in value]


def source_rect(value: Any, room: str) -> tuple[int, int, int, int] | None:
    components = numeric_list(value, 4)
    if components is None or any(component != int(component)
                                 for component in components):
        return None
    x, y, width, height = (int(component) for component in components)
    room_width, room_height = ROOM_SIZE[room]
    if (x < 0 or y < 0 or width <= 0 or height <= 0
            or x + width > room_width or y + height > room_height):
        return None
    return x, y, width, height


def runtime_text(root: Path, errors: list[str]) -> str:
    path = root / FIXTURE_RUNTIME_RELATIVE
    if not path.is_file():
        add_error(errors, "runtime: missing castle_fixture_rigs.gd")
        return ""
    return path.read_text(encoding="utf-8")


def literal_constant(text: str, name: str) -> str:
    # Supports both a one-line constant and the project's backslash-wrapped form.
    pattern = rf'const\s+{re.escape(name)}[^=]*:=\s*(?:\\\s*)?"res://([^"]+)"'
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else ""


def active_v3_additions(root: Path, fixture_text: str,
                        errors: list[str]) -> list[str]:
    """Return any obsolete V3 runtime route.

    V3 was physically retired.  Its missing manifest is therefore the expected
    healthy state and must never be opened as a prerequisite for this audit.
    Conversely, even a supposedly filtered runtime literal is rejected: a
    deleted delivery cannot be a valid runtime dependency.
    """
    del root, errors
    return sorted(set(re.findall(
        r'res://([^"\n]*interactions_v3[^"\n]*)', fixture_text
    )))


def scripted_interactions(root: Path, errors: list[str]) -> set[str]:
    path = root / ROOM_RUNTIME_RELATIVE
    if not path.is_file():
        add_error(errors, "runtime: missing castle_rooms_25d.gd")
        return set()
    text = path.read_text(encoding="utf-8")
    start = text.find("const INTERACTION_SPECS := {")
    end = text.find("const INTERACTION_GRIDS_3X3", start)
    if start < 0 or end < 0:
        add_error(errors, "runtime: cannot delimit INTERACTION_SPECS")
        return set()
    return set(re.findall(
        r'(?m)^\s*"([a-z0-9_]+:[a-z0-9_]+)"\s*:', text[start:end]
    ))


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").point(
        lambda value: 255 if value >= ALPHA_VISIBLE else 0
    ).getbbox()


def pixels(image: Image.Image) -> Iterable[Any]:
    getter = getattr(image, "get_flattened_data", None)
    return getter() if getter is not None else image.getdata()


def split_frames(sheet: Image.Image, asset: dict[str, Any], label: str,
                 errors: list[str]) -> list[Image.Image]:
    frame_count = asset.get("authored_frame_count", asset.get("frame_count"))
    if isinstance(frame_count, bool) or not isinstance(frame_count, int) \
            or not MIN_FRAMES <= frame_count <= MAX_FRAMES:
        add_error(errors, f"{label}: authored_frame_count must be 4..12")
        return []
    grid = numeric_list(asset.get("grid"), 2)
    if grid is None or any(component != int(component) for component in grid):
        add_error(errors, f"{label}: grid must contain two integers")
        return []
    columns, rows = (int(component) for component in grid)
    if columns <= 0 or rows <= 0 or columns * rows < frame_count:
        add_error(errors, f"{label}: grid cannot hold authored frames")
        return []
    if sheet.width % columns or sheet.height % rows:
        add_error(errors, f"{label}: sheet dimensions are not divisible by grid")
        return []
    cell_width, cell_height = sheet.width // columns, sheet.height // rows
    return [
        sheet.crop((
            (index % columns) * cell_width,
            (index // columns) * cell_height,
            (index % columns + 1) * cell_width,
            (index // columns + 1) * cell_height,
        ))
        for index in range(frame_count)
    ]


def audit_frame_alpha(frames: list[Image.Image], label: str,
                      errors: list[str], minimum_unique: int = MIN_FRAMES) -> None:
    unique: set[str] = set()
    for index, frame in enumerate(frames):
        bbox = alpha_bbox(frame)
        if bbox is None:
            add_error(errors, f"{label}: frame {index} has no visible object")
            continue
        left, top, right, bottom = bbox
        padding = min(left, top, frame.width - right, frame.height - bottom)
        if padding < MIN_PADDING:
            add_error(errors, f"{label}: frame {index} has {padding}px alpha "
                      f"padding; requires {MIN_PADDING}px")
        alpha = frame.getchannel("A")
        border = (
            list(pixels(alpha.crop((0, 0, frame.width, 1))))
            + list(pixels(alpha.crop((0, frame.height - 1, frame.width, frame.height))))
            + list(pixels(alpha.crop((0, 0, 1, frame.height))))
            + list(pixels(alpha.crop((frame.width - 1, 0, frame.width, frame.height))))
        )
        if any(border):
            add_error(errors, f"{label}: frame {index} has a nontransparent border")
        hidden_rgb = exact_key = near_key = 0
        visible_pixels = 0
        for red, green, blue, alpha_value in pixels(frame):
            if alpha_value == 0 and (red or green or blue):
                hidden_rgb += 1
            if alpha_value >= ALPHA_VISIBLE:
                visible_pixels += 1
                exact_key += (red, green, blue) == KEY_RGB
                near_key += red >= 220 and blue >= 220 and green <= 55
        if hidden_rgb:
            add_error(errors, f"{label}: frame {index} has {hidden_rgb} hidden "
                      "RGB pixels under zero alpha")
        near_key_limit = max(16, int(visible_pixels * 0.0002))
        if exact_key or near_key > near_key_limit:
            add_error(errors, f"{label}: frame {index} retains keyed pixels "
                      f"(exact={exact_key}, near={near_key}, "
                      f"near_limit={near_key_limit})")
        unique.add(hashlib.sha256(frame.tobytes()).hexdigest())
    if len(unique) < minimum_unique:
        add_error(errors, f"{label}: only {len(unique)} unique authored states")


def audit_seahorse_source_states(
        frames: list[Image.Image], asset: dict[str, Any], label: str,
        errors: list[str]) -> None:
    """Prove the damaged generated fountain body cannot return unnoticed."""
    if not frames:
        return
    rest = frames[0].convert("RGBA")
    rest_alpha = np.asarray(rest.getchannel("A"), dtype=np.uint8)
    rest_bbox = alpha_bbox(rest)
    layers = asset.get("water_layers", [])
    if rest_bbox is None or not isinstance(layers, list) or len(layers) != 1 \
            or not isinstance(layers[0], dict):
        add_error(errors, f"{label}: source-stream audit lacks one bounded water layer")
        return
    points = normalized_points(layers[0].get("points"))
    if points is None:
        add_error(errors, f"{label}: source-stream audit lacks normalized polygon")
        return
    left, top, right, bottom = rest_bbox
    width, height = right - left, bottom - top
    polygon = [
        (round(left + point[0] * width), round(top + point[1] * height))
        for point in points
    ]
    allowed = Image.new("L", rest.size, 0)
    ImageDraw.Draw(allowed).polygon(polygon, fill=255)
    allowed = allowed.filter(ImageFilter.GaussianBlur(0.65))
    allowed = ImageChops.multiply(allowed, rest.getchannel("A"))
    allowed_values = np.asarray(allowed, dtype=np.uint8) > 0
    rest_rgb = np.asarray(rest, dtype=np.uint8)[:, :, :3]
    unique: set[str] = set()
    changed_states = 0
    for index, frame in enumerate(frames):
        rgba = np.asarray(frame.convert("RGBA"), dtype=np.uint8)
        if not np.array_equal(rgba[:, :, 3], rest_alpha):
            add_error(errors, f"{label}: frame {index} changed the source alpha silhouette")
        rgb_changed = np.any(rgba[:, :, :3] != rest_rgb, axis=2)
        if np.any(rgb_changed & ~allowed_values):
            add_error(errors, f"{label}: frame {index} repainted the fountain body")
        changed_states += int(np.any(rgb_changed))
        unique.add(hashlib.sha256(frame.tobytes()).hexdigest())
    if changed_states != len(frames) - 1 or len(unique) != len(frames):
        add_error(errors, f"{label}: stream shimmer must provide eight distinct states")


def audit_fridge_pale_matte(
        frames: list[Image.Image], label: str, errors: list[str]) -> None:
    counts: list[int] = []
    component_counts: list[int] = []
    for frame in frames:
        visible = frame.getchannel("A").point(
            lambda value: 255 if value >= ALPHA_VISIBLE else 0)
        _components, component_count = component_label(
            np.asarray(visible, dtype=np.uint8) > 0)
        component_counts.append(int(component_count))
        eroded = visible.filter(ImageFilter.MinFilter(5))
        edge = ImageChops.subtract(visible, eroded)
        count = 0
        for rgba, edge_value in zip(pixels(frame), pixels(edge)):
            if not edge_value:
                continue
            red, green, blue, _alpha = rgba
            if min(red, green, blue) >= 232 \
                    and max(red, green, blue) - min(red, green, blue) <= 18:
                count += 1
        counts.append(count)
    if any(counts):
        add_error(errors, f"{label}: pale checker matte survives on frame edges: {counts}")
    if any(count != 1 for count in component_counts):
        add_error(errors, f"{label}: disconnected visible alpha components remain: "
                  f"{component_counts}")


def opaque_mask(image: Image.Image) -> Image.Image:
    return image.getchannel("A").point(
        lambda value: 255 if value >= ALPHA_COMPARE else 0
    )


def ownership_core_mask(image: Image.Image) -> Image.Image:
    return image.getchannel("A").point(
        lambda value: 255 if value >= 224 else 0
    )


def max_rgb_difference(first: Image.Image, second: Image.Image) -> Image.Image:
    channels = ImageChops.difference(
        first.convert("RGB"), second.convert("RGB")
    ).split()
    return ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]),
                              channels[2])


def match_ratio(first: Image.Image, second: Image.Image,
                mask: Image.Image, tolerance: int = SOURCE_TOLERANCE) -> float:
    matched = max_rgb_difference(first, second).point(
        lambda value: 255 if value <= tolerance else 0
    )
    matched = ImageChops.multiply(matched, mask)
    return matched.histogram()[255] / float(max(1, mask.histogram()[255]))


def change_ratio(first: Image.Image, second: Image.Image,
                 mask: Image.Image, tolerance: int = OUTSIDE_DIFF_TOLERANCE) -> float:
    changed = max_rgb_difference(first, second).point(
        lambda value: 255 if value > tolerance else 0
    )
    changed = ImageChops.multiply(changed, mask)
    return changed.histogram()[255] / float(max(1, mask.histogram()[255]))


def fitted_object(image: Image.Image, size: tuple[int, int]) -> Image.Image | None:
    bbox = alpha_bbox(image)
    if bbox is None:
        return None
    return image.crop(bbox).resize(size, Image.Resampling.LANCZOS)


def evidence_mask(mask_image: Image.Image, rest_object: Image.Image,
                  rect: tuple[int, int, int, int], room_image_size: tuple[int, int],
                  label: str, errors: list[str],
                  allow_alpha_only_trim: bool = False) -> Image.Image:
    x, y, width, height = rect
    if mask_image.size == room_image_size:
        result = mask_image.convert("L").crop((x, y, x + width, y + height))
    elif mask_image.size == (width, height):
        result = mask_image.convert("L")
    else:
        add_error(errors, f"{label}: mask must match source rect or full room; "
                  f"found {mask_image.size}")
        result = opaque_mask(rest_object)
    result = result.point(lambda value: 255 if value >= ALPHA_COMPARE else 0)
    # A supplied mask may be narrower than anti-aliased card edges, but it may
    # never claim pixels wholly outside the visible rest object.
    rest_mask = opaque_mask(rest_object)
    outside = ImageChops.subtract(result, rest_mask)
    if outside.getbbox() is not None and not allow_alpha_only_trim:
        add_error(errors, f"{label}: mask claims pixels outside the rest card")
    result = ImageChops.multiply(result, rest_mask)
    if result.getbbox() is None:
        add_error(errors, f"{label}: ownership mask is empty")
        return rest_mask
    return result


def default_source_plate(room: str) -> str:
    return f"assets/flats/castle/rooms/room_{room}.png"


def default_parent_background(room: str) -> str:
    return f"assets/flats/castle/rooms/room_{room}_background.png"


def runtime_uses_healed_background(root: Path, room: str, path: Path,
                                   errors: list[str], label: str,
                                   runtime_tile_rooms: set[str] | None = None) -> None:
    if runtime_tile_rooms is not None and room in runtime_tile_rooms:
        return
    relative = path.relative_to(root).as_posix()
    standard = f"assets/flats/castle/rooms/room_{room}_background.png"
    room_text = (root / ROOM_RUNTIME_RELATIVE).read_text(encoding="utf-8")
    if relative == standard:
        return
    if relative not in room_text:
        add_error(errors, f"{label}: healed background is not referenced by castle "
                  f"room runtime: {relative}")


def audit_hotspot(asset: dict[str, Any], rect: tuple[int, int, int, int],
                  label: str, errors: list[str]) -> None:
    width, height = rect[2], rect[3]
    size = numeric_list(asset.get("hotspot_size"), 2)
    offset = numeric_list(asset.get("hotspot_offset"), 2)
    if size is None or min(size) < 112.0:
        add_error(errors, f"{label}: hotspot_size must be at least 112x112 logical px")
        return
    if offset is None:
        add_error(errors, f"{label}: hotspot_offset must center the child touch target")
        return
    expected = ((width - size[0]) * 0.5, (height - size[1]) * 0.5)
    if any(abs(offset[index] - expected[index]) > 0.001 for index in range(2)):
        add_error(errors, f"{label}: hotspot is not centered on source_rect")


def normalized_points(value: Any) -> list[tuple[float, float]] | None:
    if not isinstance(value, list) or len(value) < 3:
        return None
    points: list[tuple[float, float]] = []
    for raw in value:
        point = numeric_list(raw, 2)
        if point is None or any(component < 0.0 or component > 1.0
                                for component in point):
            return None
        points.append((point[0], point[1]))
    return points


def point_inside_box(point: tuple[float, float], box: list[float]) -> bool:
    return (box[0] <= point[0] <= box[0] + box[2]
            and box[1] <= point[1] <= box[1] + box[3])


def audit_native_semantics(asset: dict[str, Any], label: str,
                           errors: list[str]) -> None:
    asset_id = str(asset.get("id", ""))
    action = str(asset.get("semantic_action", ""))
    exact_actions = {
        "kitchen_fridge": "unlatch_and_open_fridge_door",
        "craft_room_supply_cupboard_left":
            "pull_supply_bins_and_reveal_art_supplies",
        "mermaid_pool_flower_float":
            "bloom_flower_petals_and_make_ripples",
        "mermaid_pool_star_float":
            "flex_star_point_and_make_ripples",
    }
    if asset_id in exact_actions and action != exact_actions[asset_id]:
        add_error(errors, f"{label}: semantic_action does not name the delivered use")
    if asset_id in {"kitchen_stove_pot_lid", "bubble_bath_toilet_roll"}:
        add_error(errors, f"{label}: rejected ownership candidate entered delivery")
    review = asset.get("visual_review", {})
    if not isinstance(review, dict) \
            or review.get("status") != "accepted" \
            or review.get("identity_continuity") != "accepted" \
            or review.get("fixed_root_verified") is not True \
            or review.get("normalized_use_verified") is not True:
        add_error(errors, f"{label}: missing accepted identity/use visual review")
    metrics = asset.get("fixed_root_bbox_metrics", {})
    if not isinstance(metrics, dict) \
            or not isinstance(metrics.get("maximum_width_ratio_to_rest"), (int, float)) \
            or not isinstance(metrics.get("maximum_height_ratio_to_rest"), (int, float)) \
            or float(metrics.get("maximum_width_ratio_to_rest", 99.0)) > 1.75 \
            or float(metrics.get("maximum_height_ratio_to_rest", 99.0)) > 1.75:
        add_error(errors, f"{label}: fixed-root bbox continuity is missing or implausible")
    if asset_id == "playroom_tent_flaps_right":
        normalization = asset.get("normalization", {})
        if not isinstance(normalization, dict) \
                or normalization.get("method") != "source_owned_flap_fold_states" \
                or normalization.get("per_frame_warp") is not True \
                or normalization.get("per_frame_local_resample") is not True \
                or normalization.get("fixed_root_pivot") is not True:
            add_error(errors, f"{label}: seam-fold derivation metadata is inaccurate")
    if asset_id == "mermaid_pool_seahorse_fountain":
        normalization = asset.get("normalization", {})
        if not isinstance(normalization, dict) \
                or normalization.get("method") \
                != "source_owned_seahorse_stream_shimmer_states" \
                or normalization.get("source_owned_pixels_only") is not True \
                or normalization.get("exact_alpha_silhouette_all_frames") is not True \
                or normalization.get("body_rgb_unchanged_outside_stream_mask") \
                is not True \
                or "source_path" in normalization:
            add_error(errors, f"{label}: rejected generated fountain states remain")
    if asset_id == "kitchen_fridge":
        normalization = asset.get("normalization", {})
        matte_audit = normalization.get("pale_matte_edge_audit", {}) \
            if isinstance(normalization, dict) else {}
        edge_cleanup = normalization.get("generated_edge_cleanup", {}) \
            if isinstance(normalization, dict) else {}
        source_cleanup = asset.get("source_alpha_cleanup", {})
        override = asset.get("v4_override_of", {})
        if asset.get("runtime_interaction_key") != "kitchen:fridge" \
                or not isinstance(override, dict) \
                or override.get("pack") != "v2_base" \
                or override.get("asset_id") != "kitchen_fridge":
            add_error(errors, f"{label}: must override only the V2 kitchen fridge")
        if asset.get("anchor_mode") != "bottom_left" \
                or asset.get("grid") != [3, 3] \
                or asset.get("cell_size") != [320, 272] \
                or asset.get("sheet_dimensions") != [960, 816]:
            add_error(errors, f"{label}: exact rest/open-door atlas geometry drifted")
        if not isinstance(normalization, dict) \
                or normalization.get("method") \
                != "normalized_generated_fridge_states_fixed_base" \
                or normalization.get("matte_method") \
                != "edge_connected_neutral_components_in_two_source_rows" \
                or normalization.get("edge_rgb_decontamination") \
                != "nearest_eroded_foreground_core" \
                or normalization.get("per_frame_warp") is not False \
                or normalization.get("per_frame_scale") is not False:
            add_error(errors, f"{label}: fridge segmentation/fixed-base metadata missing")
        if not isinstance(matte_audit, dict) \
                or matte_audit.get("status") != "passed" \
                or matte_audit.get("visible_pale_matte_pixels_by_frame") != [0] * 8:
            add_error(errors, f"{label}: pale checker matte audit did not pass")
        if not isinstance(edge_cleanup, dict) \
                or edge_cleanup.get("method") \
                != "nearest_solid_object_core_rgb_on_translucent_generated_edges" \
                or edge_cleanup.get("visible_alpha_component_count_by_frame") \
                != [1] * 8:
            add_error(errors, f"{label}: generated edge/component cleanup is missing")
        if not isinstance(source_cleanup, dict) \
                or source_cleanup.get("method") != "fridge_only_source_pixels_v1" \
                or source_cleanup.get("rgb_repainted") is not False \
                or int(source_cleanup.get("removed_visible_pixels", 0)) <= 0:
            add_error(errors, f"{label}: source-card non-fridge alpha cleanup is missing")
    continuity = asset.get("ownership_continuity", [])
    if asset_id == "kitchen_fridge" \
            and "frame0_exact_source_derived_fridge_only_card" not in continuity:
        add_error(errors, f"{label}: exact teal fridge rest continuity is unproven")
    if asset_id == "mermaid_pool_flower_float" \
            and "exact_source_aqua_float_base_in_every_state" not in continuity:
        add_error(errors, f"{label}: native aqua support continuity is unproven")
    if asset_id == "mermaid_pool_star_float" \
            and "exact_source_cyan_rear_underside_in_every_state" not in continuity:
        add_error(errors, f"{label}: native cyan underside continuity is unproven")
    if asset_id == "mermaid_pool_seahorse_fountain" \
            and ("exact_source_fountain_body_in_every_state" not in continuity \
                 or "exact_source_alpha_silhouette_in_every_state" not in continuity \
                 or "generated_damaged_body_states_rejected_after_mobile_review" \
                 not in continuity):
        add_error(errors, f"{label}: source-owned fountain continuity is unproven")

    physics_expected = {
        "mermaid_pool_flower_float": "buoyant",
        "mermaid_pool_star_float": "buoyant",
    }
    mode = str(asset.get("physics_mode", "none"))
    expected_mode = physics_expected.get(asset_id, "none")
    if mode != expected_mode:
        add_error(errors, f"{label}: physics_mode must be {expected_mode}")
    behavior = asset.get("animation_behavior", {})
    if asset_id in physics_expected:
        if not isinstance(behavior, dict) \
                or behavior.get("secondary_physics") is not True \
                or not str(behavior.get("physics_role", "")):
            add_error(errors, f"{label}: bounded secondary solid physics metadata missing")
        if asset.get("secondary_root_physics") is not True \
                or asset.get("jolt_role") != "secondary_solid_body_garnish":
            add_error(errors, f"{label}: Jolt must be declared secondary solid garnish")
        angle = asset.get("physics_max_angle_radians")
        impulse = asset.get("physics_impulse_scale")
        if (isinstance(angle, bool) or not isinstance(angle, (int, float))
                or not 0.0 < float(angle) <= 0.12):
            add_error(errors, f"{label}: buoyant angle is missing or unbounded")
        if (isinstance(impulse, bool) or not isinstance(impulse, (int, float))
                or not 0.0 < float(impulse) <= 0.50):
            add_error(errors, f"{label}: buoyant impulse is missing or unbounded")
    elif isinstance(behavior, dict) and behavior.get("secondary_physics") is True:
        add_error(errors, f"{label}: dry/non-solid fixture cannot request Jolt garnish")

    fluid_assets = {
        "mermaid_pool_waterfall", "mermaid_pool_seahorse_fountain",
        "mermaid_pool_flower_float", "mermaid_pool_star_float",
    }
    layers = asset.get("water_layers", [])
    authored_count = int(asset.get("authored_frame_count", 0))
    if asset_id not in fluid_assets:
        if layers or asset.get("fluid_engine", "none") != "none":
            add_error(errors, f"{label}: unexpected fluid layer")
        return
    if asset.get("fluid_engine") != "fixture_water_shader" \
            or asset.get("water_mask_space") != "source_rect_normalized" \
            or asset.get("uses_jolt_for_fluid") is not False:
        add_error(errors, f"{label}: fluid must use bounded fixture water shader, not Jolt")
    if not isinstance(layers, list) or not layers:
        add_error(errors, f"{label}: missing bounded water layer")
        return
    for layer_index, layer in enumerate(layers):
        layer_label = f"{label}:water layer {layer_index}"
        if not isinstance(layer, dict):
            add_error(errors, f"{layer_label}: invalid layer")
            continue
        if layer.get("local_origin") != "source_rect":
            add_error(errors, f"{layer_label}: must use source_rect local origin")
        active = layer.get("active_frames")
        if (not isinstance(active, list) or not active
                or 0 in active
                or any(isinstance(index, bool) or not isinstance(index, int)
                       or index < 0 or index >= authored_count for index in active)):
            add_error(errors, f"{layer_label}: active_frames must be bounded non-rest states")
        shape = str(layer.get("shape", ""))
        if shape == "ellipse":
            center = numeric_list(layer.get("center"), 2)
            radius = numeric_list(layer.get("radius"), 2)
            if center is None or radius is None or any(value <= 0.0 for value in radius) \
                    or center[0] - radius[0] < 0.0 \
                    or center[1] - radius[1] < 0.0 \
                    or center[0] + radius[0] > 1.0 \
                    or center[1] + radius[1] > 1.0:
                add_error(errors, f"{layer_label}: ellipse escapes owned source_rect")
            if asset_id in {"mermaid_pool_flower_float", "mermaid_pool_star_float"}:
                if layer.get("role") != "ripple" \
                        or layer.get("contact_role") != "under_object_pool_contact" \
                        or float(layer.get("z_offset", 0.0)) >= 0.0:
                    add_error(errors, f"{layer_label}: float ripple is not under-object contact")
        else:
            points = normalized_points(layer.get("points"))
            if points is None:
                add_error(errors, f"{layer_label}: polygon escapes owned source_rect")
                continue
            for frame_points in layer.get("points_frames", []):
                if normalized_points(frame_points) is None:
                    add_error(errors, f"{layer_label}: animated polygon escapes source_rect")
                    break
            if asset_id in {"mermaid_pool_waterfall", "mermaid_pool_seahorse_fountain"}:
                outlet = numeric_list(layer.get("outlet_bounds_normalized"), 4)
                if outlet is None or outlet[2] <= 0.0 or outlet[3] <= 0.0 \
                        or any(value < 0.0 for value in outlet) \
                        or outlet[0] + outlet[2] > 1.0 \
                        or outlet[1] + outlet[3] > 1.0:
                    add_error(errors, f"{layer_label}: missing tight real-outlet bounds")
                elif not all(point_inside_box(point, outlet) for point in points[:2]):
                    add_error(errors, f"{layer_label}: flow does not begin at real outlet")
                if asset_id == "mermaid_pool_seahorse_fountain":
                    if layer.get("points_frames"):
                        add_error(errors, f"{layer_label}: fountain outlet may not drift")
                    alpha_base = layer.get("alpha_base")
                    turbulence = layer.get("turbulence")
                    if (isinstance(alpha_base, bool)
                            or not isinstance(alpha_base, (int, float))
                            or not 0.10 <= float(alpha_base) <= 0.25
                            or isinstance(turbulence, bool)
                            or not isinstance(turbulence, (int, float))
                            or not 0.05 <= float(turbulence) <= 0.30):
                        add_error(errors, f"{layer_label}: subtle stream shader tuning missing")


def audit_exact_rest_frame(frame: Image.Image, rest: Image.Image,
                           asset: dict[str, Any], label: str,
                           errors: list[str]) -> None:
    if asset.get("frame0_exact_rest_card") is not True:
        add_error(errors, f"{label}: frame0_exact_rest_card must be true")
        return
    origin = numeric_list(asset.get("rest_card_cell_origin"), 2)
    if origin is None or any(value != int(value) for value in origin):
        add_error(errors, f"{label}: rest_card_cell_origin must contain two integers")
        return
    x, y = int(origin[0]), int(origin[1])
    if x < 0 or y < 0 or x + rest.width > frame.width \
            or y + rest.height > frame.height:
        add_error(errors, f"{label}: exact rest card does not fit its atlas cell")
        return
    expected = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    expected.alpha_composite(rest, (x, y))
    if expected.tobytes() != frame.tobytes():
        add_error(errors, f"{label}: rest frame is not an exact unscaled rest-card paste")


def audit_asset(
        root: Path, asset: dict[str, Any],
        surface_masks: dict[tuple[Path, Path], Image.Image],
        surface_images: dict[tuple[Path, Path], tuple[Image.Image, Image.Image]],
        healed_overrides: dict[str, Path],
        errors: list[str],
        runtime_tile_rooms: set[str] | None = None) -> set[str]:
    asset_id = str(asset.get("id", ""))
    label = f"asset {asset_id or '<missing>'}"
    room = str(asset.get("room", ""))
    instances = asset.get("instances", [])
    keys: set[str] = set()
    if not asset_id or not room:
        add_error(errors, f"{label}: missing id/room")
        return keys
    if not isinstance(instances, list) or len(instances) != 1 \
            or not str(instances[0]):
        add_error(errors, f"{label}: V4 source ownership requires exactly one instance")
        return keys
    keys.add(f"{room}:{instances[0]}")
    if asset.get("pack") != "v4_native":
        add_error(errors, f"{label}: pack must be v4_native")
    if asset.get("render_mode") != "generated_full_object_states":
        add_error(errors, f"{label}: render_mode must be generated_full_object_states")
    if asset.get("primary_animation_is_overlay") is not False:
        add_error(errors, f"{label}: primary_animation_is_overlay must be false")

    action = str(asset.get("semantic_action", ""))
    behavior = asset.get("animation_behavior")
    if not isinstance(behavior, dict):
        add_error(errors, f"{label}: animation_behavior must be an object")
    else:
        if behavior.get("mode") != "authored_object_states":
            add_error(errors, f"{label}: animation_behavior.mode must be "
                      "authored_object_states")
        if not action or behavior.get("action") != action:
            add_error(errors, f"{label}: animation_behavior.action must exactly "
                      "match semantic_action")
        if behavior.get("generic_transform_fallback") is not False:
            add_error(errors, f"{label}: generic_transform_fallback must be false")

    ownership = asset.get("source_ownership")
    if not isinstance(ownership, dict):
        add_error(errors, f"{label}: source_ownership must be an object")
        return keys
    for flag in ("passed", "verified", "background_healed",
                 "duplicate_pixels_removed"):
        if ownership.get(flag) is not True:
            add_error(errors, f"{label}: source_ownership.{flag} must be true")
    rect = source_rect(asset.get("source_rect"), room)
    ownership_rect = source_rect(ownership.get("source_rect"), room)
    if rect is None or ownership_rect is None or rect != ownership_rect:
        add_error(errors, f"{label}: source_rect must be one valid identical room rect")
        return keys
    x, y, width, height = rect
    if asset.get("placement_position") not in (None, [x, y], [float(x), float(y)]):
        add_error(errors, f"{label}: placement_position may not diverge from source_rect")
    if asset.get("placement_size") not in (None, [width, height],
                                             [float(width), float(height)]):
        add_error(errors, f"{label}: placement_size may not diverge from source_rect")

    source_path = repository_file(
        root,
        asset.get("source_room_plate_path", default_source_plate(room)),
        f"{label}:source room plate",
        errors,
    )
    healed_path = repository_file(root, asset.get("healed_background_path"),
                                  f"{label}:healed background", errors)
    parent_path = repository_file(
        root,
        asset.get("parent_background_path", default_parent_background(room)),
        f"{label}:parent background",
        errors,
    )
    rest_path = repository_file(root, asset.get("rest_card_path"),
                                f"{label}:rest card", errors)
    mask_path = repository_file(root, asset.get("mask_path"),
                                f"{label}:ownership mask", errors)
    verify_file_hash(source_path, ownership.get("source_room_plate_sha256"),
                     f"{label}:source room plate", errors)
    verify_file_hash(healed_path, ownership.get("healed_background_sha256"),
                     f"{label}:healed background", errors)
    verify_file_hash(rest_path, ownership.get("rest_card_sha256"),
                     f"{label}:rest card", errors)
    verify_file_hash(mask_path, ownership.get("mask_sha256"),
                     f"{label}:ownership mask", errors)
    source_image = image_surface(source_path, f"{label}:source room plate", errors)
    healed_image = image_surface(healed_path, f"{label}:healed background", errors)
    parent_image = image_surface(parent_path, f"{label}:parent background", errors)
    rest_card = image_rgba(rest_path, f"{label}:rest card", errors)
    mask_image = image_mask(mask_path, f"{label}:ownership mask", errors)
    if any(value is None for value in (
            source_path, healed_path, parent_path, source_image, healed_image,
            parent_image,
            rest_card, mask_image)):
        return keys
    assert source_path is not None and healed_path is not None and parent_path is not None
    assert source_image is not None and healed_image is not None and parent_image is not None
    assert rest_card is not None and mask_image is not None
    if source_image.size != ROOM_SIZE[room]:
        add_error(errors, f"{label}: source plate size {source_image.size} does not "
                  f"match room coordinates {ROOM_SIZE[room]}")
    if source_image.size != healed_image.size:
        add_error(errors, f"{label}: source/healed surface dimensions differ")
        return keys
    if parent_image.size != healed_image.size:
        add_error(errors, f"{label}: parent/healed background dimensions differ")
        return keys
    # The 1024x576 healed plate is audit evidence only. Runtime routing is
    # independently and exhaustively verified against approved native tile
    # masters by audit_runtime_background_tiles().
    previous_override = healed_overrides.get(room)
    if previous_override is not None and previous_override != healed_path:
        add_error(errors, f"{label}: room has multiple healed runtime backgrounds")
    healed_overrides[room] = healed_path

    source_crop = source_image.crop((x, y, x + width, y + height))
    healed_crop = healed_image.crop((x, y, x + width, y + height))
    cleanup = asset.get("rest_card_pixel_cleanup", {})
    alpha_only_trim = isinstance(cleanup, dict) \
        and cleanup.get("method") \
        == "source_rgb_preserving_alpha_only_pool_contact_trim"
    registration = numeric_list(asset.get("rest_card_registration_bbox"), 4)
    if registration is not None \
            and all(value == int(value) for value in registration) \
            and int(registration[2] - registration[0]) == width \
            and int(registration[3] - registration[1]) == height:
        rest_object = rest_card.crop(tuple(int(value) for value in registration))
    else:
        rest_object = rest_card if rest_card.size == (width, height) else fitted_object(
            rest_card, (width, height)
        )
    if rest_object is None:
        add_error(errors, f"{label}: rest card has no visible object")
        return keys
    mask = evidence_mask(
        mask_image, rest_object, rect, source_image.size,
        label, errors, allow_alpha_only_trim=alpha_only_trim)
    source_match = match_ratio(rest_object, source_crop, mask)
    duplicate_match = match_ratio(
        rest_object, healed_crop, mask, DUPLICATE_TOLERANCE
    )
    healing_change = change_ratio(
        source_crop, healed_crop, mask, HEALING_TOLERANCE
    )
    if source_match < SOURCE_MATCH_MIN:
        add_error(errors, f"{label}: rest card is not the painted source object "
                  f"(match={source_match:.6f}, requires {SOURCE_MATCH_MIN})")
    if duplicate_match > DUPLICATE_MATCH_MAX:
        add_error(errors, f"{label}: duplicate rest-card pixels remain in healed "
                  f"background (match={duplicate_match:.6f}, max={DUPLICATE_MATCH_MAX})")
    if healing_change < HEALED_CHANGE_MIN:
        add_error(errors, f"{label}: source object was not healed out of the room "
                  f"(changed={healing_change:.6f}, requires {HEALED_CHANGE_MIN})")
    if alpha_only_trim:
        if cleanup.get("protected_source_modified") is not False \
                or cleanup.get("hidden_rgb_zeroed") is not True \
                or int(cleanup.get("removed_visible_pixels", 0)) <= 0 \
                or cleanup.get("registration_bbox_preserved") \
                != [int(value) for value in registration or []]:
            add_error(errors, f"{label}: pool-contact alpha trim evidence is incomplete")
        source_master_path = repository_file(
            root, asset.get("rest_card_source_path"),
            f"{label}:rest-card source master", errors)
        source_master = image_rgba(
            source_master_path, f"{label}:rest-card source master", errors)
        if source_master is not None and source_master.size == rest_card.size:
            retained = rest_card.getchannel("A").point(
                lambda value: 255 if value > 0 else 0)
            if match_ratio(
                    rest_card, source_master, retained, tolerance=0) < 1.0:
                add_error(errors, f"{label}: alpha trim repainted retained source RGB")

    # The room composite proves where the object came from.  The parent
    # background, not that layered composite, is the correct baseline for
    # proving that the healing pass changed only owned pixels.
    surface_key = (parent_path, healed_path)
    if surface_key not in surface_images:
        surface_images[surface_key] = (parent_image, healed_image)
        surface_masks[surface_key] = Image.new("L", parent_image.size, 0)
    full_mask = surface_masks[surface_key]
    existing = full_mask.crop((x, y, x + width, y + height))
    full_mask.paste(ImageChops.lighter(existing, mask), (x, y))

    pending = str(asset.get("delivery_status", "")).startswith(
        "ownership_ready_authored_states_pending")
    if pending and not asset.get("sheet"):
        return keys

    audit_hotspot(asset, rect, label, errors)
    audit_native_semantics(asset, label, errors)
    if asset_id == "kitchen_fridge":
        normalization = asset.get("normalization", {})
        source_master = repository_file(
            root,
            normalization.get("source_path") if isinstance(normalization, dict)
            else None,
            f"{label}:ImageGen source master",
            errors,
        )
        if source_master is not None:
            verify_file_hash(
                source_master,
                normalization.get("source_sha256"),
                f"{label}:ImageGen source master",
                errors,
            )
        cleanup = asset.get("source_alpha_cleanup", {})
        legacy_card_path = repository_file(
            root,
            cleanup.get("source_card_path") if isinstance(cleanup, dict) else None,
            f"{label}:legacy source card",
            errors,
        )
        if legacy_card_path is not None:
            verify_file_hash(
                legacy_card_path,
                cleanup.get("source_card_sha256"),
                f"{label}:legacy source card",
                errors,
            )
            legacy_card = image_rgba(
                legacy_card_path, f"{label}:legacy source card", errors)
            if legacy_card is not None and legacy_card.size == rest_card.size:
                retained = rest_card.getchannel("A").point(
                    lambda value: 255 if value >= ALPHA_VISIBLE else 0)
                if match_ratio(rest_card, legacy_card, retained, tolerance=0) < 1.0:
                    add_error(errors, f"{label}: retained source-card RGB was repainted")
                rest_values = np.asarray(rest_card.convert("RGBA"), dtype=np.uint8)
                red = rest_values[:, :, 0].astype(np.int16)
                green = rest_values[:, :, 1].astype(np.int16)
                blue = rest_values[:, :, 2].astype(np.int16)
                visible = rest_values[:, :, 3] >= ALPHA_VISIBLE
                purple_wall = visible & (red >= green + 8) & (blue >= green + 8)
                yy, xx = np.mgrid[0:rest_card.height, 0:rest_card.width]
                neighbor = visible & (xx >= 133) & (yy >= 164) & (yy <= 196)
                if np.any(purple_wall) or np.any(neighbor):
                    add_error(errors, f"{label}: non-fridge source alpha survives cleanup")

    sheet_path = repository_file(root, asset.get("sheet"), f"{label}:sheet", errors)
    if sheet_path is not None and asset.get("sheet_sha256") is not None:
        verify_file_hash(sheet_path, asset.get("sheet_sha256"), f"{label}:sheet", errors)
    sheet = image_rgba(sheet_path, f"{label}:sheet", errors)
    if sheet is None:
        return keys
    frames = split_frames(sheet, asset, label, errors)
    if not frames:
        return keys
    audit_frame_alpha(frames, label, errors)
    if asset_id == "kitchen_fridge":
        audit_fridge_pale_matte(frames, label, errors)
    elif asset_id == "mermaid_pool_seahorse_fountain":
        audit_seahorse_source_states(frames, asset, label, errors)
    timeline = asset.get("timeline_sequence")
    if (not isinstance(timeline, list)
            or not MIN_FRAMES <= len(timeline) <= MAX_FRAMES
            or any(isinstance(index, bool) or not isinstance(index, int)
                   or index < 0 or index >= len(frames) for index in timeline)):
        add_error(errors, f"{label}: timeline_sequence must have 4..12 valid indices")
    rest_index = asset.get("rest_frame", 0)
    if isinstance(rest_index, bool) or not isinstance(rest_index, int) \
            or not 0 <= rest_index < len(frames):
        add_error(errors, f"{label}: invalid rest_frame")
        return keys
    audit_exact_rest_frame(frames[rest_index], rest_card, asset, label, errors)
    card_object = fitted_object(rest_card, (width, height))
    state_object = fitted_object(frames[rest_index], (width, height))
    if card_object is not None and state_object is not None:
        state_mask = ImageChops.multiply(opaque_mask(card_object),
                                         opaque_mask(state_object))
        state_match = match_ratio(card_object, state_object, state_mask)
        if state_match < REST_STATE_MATCH_MIN:
            add_error(errors, f"{label}: animation rest state does not preserve the "
                      f"native rest card (match={state_match:.6f}, "
                      f"requires {REST_STATE_MATCH_MIN})")
    return keys


def audit_outside_owned_regions(
        surface_masks: dict[tuple[Path, Path], Image.Image],
        surface_images: dict[tuple[Path, Path], tuple[Image.Image, Image.Image]],
        errors: list[str]) -> None:
    for (source_path, healed_path), (source, healed) in surface_images.items():
        outside = ImageChops.invert(surface_masks[(source_path, healed_path)])
        changed = max_rgb_difference(source, healed).point(
            lambda value: 255 if value > OUTSIDE_DIFF_TOLERANCE else 0
        )
        changed = ImageChops.multiply(changed, outside)
        ratio = changed.histogram()[255] / float(max(1, outside.histogram()[255]))
        if ratio > OUTSIDE_CHANGE_MAX:
            add_error(errors, f"surface {source_path.name}->{healed_path.name}: "
                      f"{ratio:.6f} of pixels outside owned masks changed "
                      f"(max={OUTSIDE_CHANGE_MAX})")


def runtime_frame_union(
        root: Path, asset: dict[str, Any], label: str,
        errors: list[str]) -> Image.Image | None:
    sheet_path = repository_file(
        root, asset.get("sheet"), f"{label}:runtime-union sheet", errors)
    sheet = image_rgba(sheet_path, f"{label}:runtime-union sheet", errors)
    if sheet is None:
        return None
    frames = split_frames(sheet, asset, f"{label}:runtime-union", errors)
    if not frames:
        return None
    frame_width, frame_height = frames[0].size
    scale = float(asset.get("runtime_scale", 1.0))
    if scale <= 0.0:
        add_error(errors, f"{label}: invalid runtime scale")
        return None
    offset = numeric_list(asset.get("runtime_center_offset"), 2)
    rect = source_rect(asset.get("source_rect"), str(asset.get("room", "")))
    if offset is None or rect is None:
        add_error(errors, f"{label}: missing runtime frame registration")
        return None
    center_x = rect[0] + offset[0]
    center_y = rect[1] + offset[1]
    union = Image.new("L", ROOM_SIZE[str(asset.get("room", ""))], 0)
    for frame in frames:
        placed = frame.getchannel("A").transform(
            union.size,
            Image.Transform.AFFINE,
            (
                1.0 / scale,
                0.0,
                frame_width * 0.5 - center_x / scale,
                0.0,
                1.0 / scale,
                frame_height * 0.5 - center_y / scale,
            ),
            resample=Image.Resampling.BILINEAR,
        )
        union = ImageChops.lighter(union, placed)
    return union.point(lambda value: 255 if value >= 128 else 0)


def audit_runtime_background_tiles(
        root: Path, manifest: dict[str, Any], assets: list[dict[str, Any]],
        errors: list[str]) -> set[str]:
    """Verify native-resolution healing and the readiness-gated runtime route."""
    records = manifest.get("runtime_background_tiles", {})
    if not isinstance(records, dict):
        add_error(errors, "V4 manifest: runtime_background_tiles must be an object")
        return set()
    by_room: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for asset in assets:
        by_room[str(asset.get("room", ""))].append(asset)
    expected_rooms = set(by_room)
    if set(records) != expected_rooms:
        add_error(errors, "V4 manifest: runtime tile rooms must exactly match accepted "
                  f"asset rooms (expected={sorted(expected_rooms)}, "
                  f"found={sorted(records)})")

    fixture_text = runtime_text(root, errors)
    room_text_path = root / ROOM_RUNTIME_RELATIVE
    room_text = room_text_path.read_text(encoding="utf-8") \
        if room_text_path.is_file() else ""
    runtime_root = literal_constant(fixture_text, "NATIVE_V4_TILE_ROOT")
    if runtime_root.replace("\\", "/").rstrip("/") \
            != V4_TILE_RELATIVE.as_posix():
        add_error(errors, "runtime V4_BACKGROUND_TILE_ROOT does not route native healed tiles")
    if "runtime_background_tiles" not in fixture_text \
            or "room_background_tile_root" not in room_text:
        add_error(errors, "runtime V4 background route is not manifest-readiness gated")

    routed: set[str] = set()
    for room, record_value in sorted(records.items()):
        label = f"runtime background {room}"
        if not isinstance(record_value, dict):
            add_error(errors, f"{label}: invalid record")
            continue
        record = record_value
        if record.get("route") != "v4_native_high_resolution_healed_tiles" \
                or record.get("derived_from_low_resolution_audit_plate") is not False:
            add_error(errors, f"{label}: must heal approved native masters directly")
        grid = numeric_list(record.get("grid"), 2)
        tile_size = numeric_list(record.get("tile_dimensions"), 2)
        native_size = numeric_list(record.get("native_canvas_size"), 2)
        expected_grid = (4, 3) if room == "kitchen" else (4, 2)
        expected_tile = (1024, 768) if room == "kitchen" else (910, 1024)
        expected_native = (4096, 2304) if room == "kitchen" else (3640, 2048)
        if grid != list(map(float, expected_grid)) \
                or tile_size != list(map(float, expected_tile)) \
                or native_size != list(map(float, expected_native)):
            add_error(errors, f"{label}: native grid/dimensions drifted")
            continue
        columns, rows = expected_grid
        source_records = record.get("source_tiles", [])
        output_records = record.get("tiles", [])
        if not isinstance(source_records, list) or not isinstance(output_records, list) \
                or len(source_records) != columns * rows \
                or len(output_records) != columns * rows:
            add_error(errors, f"{label}: incomplete source/runtime tile set")
            continue
        source_canvas = Image.new("RGB", expected_native)
        output_canvas = Image.new("RGB", expected_native)
        records_valid = True
        for index, (source_record, output_record) in enumerate(zip(
                source_records, output_records)):
            row, column = divmod(index, columns)
            for kind, tile_record, canvas in (
                    ("source", source_record, source_canvas),
                    ("runtime", output_record, output_canvas)):
                if not isinstance(tile_record, dict):
                    add_error(errors, f"{label}: invalid {kind} tile record")
                    records_valid = False
                    continue
                path = repository_file(
                    root, tile_record.get("path"), f"{label}:{kind} tile", errors)
                if path is None:
                    records_valid = False
                    continue
                verify_file_hash(path, tile_record.get("sha256"),
                                 f"{label}:{kind} tile", errors)
                try:
                    stored = Image.open(path)
                    stored.load()
                except (OSError, ValueError) as exc:
                    add_error(errors, f"{label}: cannot decode {kind} tile: {exc}")
                    records_valid = False
                    continue
                if stored.size != expected_tile or max(stored.size) > 1024:
                    add_error(errors, f"{label}: {kind} tile exceeds native tile contract")
                    records_valid = False
                rgba = stored.convert("RGBA")
                if rgba.getchannel("A").getextrema() != (255, 255):
                    add_error(errors, f"{label}: {kind} tile is not opaque")
                    records_valid = False
                canvas.paste(rgba.convert("RGB"),
                             (column * expected_tile[0], row * expected_tile[1]))
        if not records_valid:
            continue

        union = Image.new("L", ROOM_SIZE[room], 0)
        visible_ownership_union = Image.new("L", ROOM_SIZE[room], 0)
        live_union = Image.new("L", ROOM_SIZE[room], 0)
        for asset in by_room.get(room, []):
            mask_path = repository_file(
                root, asset.get("mask_path"), f"{label}:ownership mask", errors)
            mask = image_mask(mask_path, f"{label}:ownership mask", errors)
            rect = source_rect(asset.get("source_rect"), room)
            if mask is None or rect is None:
                records_valid = False
                continue
            x, y, width, height = rect
            if mask.size == union.size:
                full = mask
            elif mask.size == (width, height):
                full = Image.new("L", union.size, 0)
                full.paste(mask, (x, y))
            else:
                add_error(errors, f"{label}: ownership mask size drifted")
                records_valid = False
                continue
            union = ImageChops.lighter(union, full.point(
                lambda value: 255 if value >= ALPHA_COMPARE else 0))
            visible_ownership_union = ImageChops.lighter(
                visible_ownership_union, full.point(
                    lambda value: 255 if value >= 128 else 0))
            frame_union = runtime_frame_union(root, asset, label, errors)
            if frame_union is None:
                records_valid = False
                continue
            live_union = ImageChops.lighter(live_union, frame_union)
        if not records_valid:
            continue
        live_union = live_union.point(
            lambda value: 255 if value >= 128 else 0)
        healing_union = union
        native_mask = healing_union.resize(
            expected_native, Image.Resampling.NEAREST)
        changed = max_rgb_difference(source_canvas, output_canvas).point(
            lambda value: 255 if value > 0 else 0)
        outside_changed = ImageChops.multiply(
            changed, ImageChops.invert(native_mask)).histogram()[255]
        inside_changed = ImageChops.multiply(changed, native_mask).histogram()[255]
        owned_pixels = native_mask.histogram()[255]
        ownership_pixels = union.histogram()[255]
        live_pixels = live_union.histogram()[255]
        healing_pixels = healing_union.histogram()[255]
        source_outside_live = ImageChops.multiply(
            union, ImageChops.invert(live_union)).histogram()[255]
        visible_outside_live = ImageChops.multiply(
            visible_ownership_union,
            ImageChops.invert(live_union)).histogram()[255]
        if outside_changed:
            add_error(errors, f"{label}: {outside_changed} pixels outside ownership changed")
        if inside_changed / float(max(1, owned_pixels)) < HEALED_CHANGE_MIN:
            add_error(errors, f"{label}: native object pixels were not locally healed")
        for field, measured in (
                ("owned_pixel_count_native", owned_pixels),
                ("changed_owned_pixels", inside_changed),
                ("changed_outside_pixels", outside_changed)):
            if record.get(field) != measured:
                add_error(errors, f"{label}: stale {field} metric")
        for field, measured in (
                ("ownership_mask_pixels_logical", ownership_pixels),
                ("live_frame_union_pixels_logical", live_pixels),
                ("healing_mask_pixels_logical", healing_pixels),
                ("ownership_pixels_clipped_outside_live_union",
                 0),
                ("source_ownership_pixels_outside_live_union",
                 source_outside_live),
                ("visible_ownership_pixels_outside_live_union",
                 visible_outside_live)):
            if record.get(field) != measured:
                add_error(errors, f"{label}: stale {field} metric")
        for field, mask in (
                ("ownership_mask_pixel_sha256", union),
                ("live_frame_union_pixel_sha256", live_union),
                ("healing_mask_pixel_sha256", healing_union)):
            measured = hashlib.sha256(mask.tobytes()).hexdigest()
            if record.get(field) != measured:
                add_error(errors, f"{label}: stale {field}")
        if record.get("live_alpha_scissor_threshold") != 128:
            add_error(errors, f"{label}: runtime healing is not alpha-scissor clipped")
        if record.get("full_source_ownership_healed") is not True:
            add_error(errors, f"{label}: full source ownership was not healed")
        routed.add(room)
    return routed


def room_mapping_block(text: str, constant: str, room: str) -> str:
    start = text.find(f"const {constant} := {{")
    if start < 0:
        return ""
    room_start = text.find(f'\n\t"{room}":', start)
    if room_start < 0:
        return ""
    current_line_end = text.find("\n", room_start + 1)
    if current_line_end < 0:
        return text[room_start:]
    next_room = re.search(r'(?m)^\t"[a-z0-9_]+":', text[current_line_end + 1:])
    if next_room is None:
        return text[room_start:]
    return text[room_start:current_line_end + 1 + next_room.start()]


def legacy_item_positions(root: Path, errors: list[str]) -> dict[str, tuple[int, int]]:
    text = (root / ROOM_RUNTIME_RELATIVE).read_text(encoding="utf-8")
    result: dict[str, tuple[int, int]] = {}
    for room in (
            "opera_hall", "kitchen", "library", "playroom", "craft_room",
            "mermaid_pool", "bubble_bath"):
        block = room_mapping_block(text, "ROOM_ITEMS", room)
        if not block:
            add_error(errors, f"legacy registry: cannot find ROOM_ITEMS.{room}")
            continue
        for match in re.finditer(
                r'\{"id":\s*"([a-z0-9_]+)".*?'
                r'"pos":\s*Vector2\(\s*(-?[0-9.]+)\s*,\s*(-?[0-9.]+)\s*\)',
                block, flags=re.DOTALL):
            key = f"{room}:{match.group(1)}"
            result[key] = (int(round(float(match.group(2)))),
                           int(round(float(match.group(3)))))
    return result


def room_layers(root: Path, room: str, errors: list[str]) -> list[tuple[Path, int, int]]:
    text = (root / ROOM_RUNTIME_RELATIVE).read_text(encoding="utf-8")
    block = room_mapping_block(text, "ROOM_LAYOUTS", room)
    if not block:
        add_error(errors, f"legacy room composite: cannot find ROOM_LAYOUTS.{room}")
        return []
    layers: list[tuple[Path, int, int]] = []
    for match in re.finditer(
            r'\{"tex":\s*"([^"]+)"\s*,\s*"pos":\s*Vector2\('
            r'\s*(-?[0-9.]+)\s*,\s*(-?[0-9.]+)\s*\)', block):
        path = root / "assets/flats/castle/rooms" / match.group(1)
        if not path.is_file():
            add_error(errors, f"legacy room composite: missing {path.relative_to(root)}")
            continue
        layers.append((path, int(round(float(match.group(2)))),
                       int(round(float(match.group(3))))))
    return layers


def compose_runtime_room(root: Path, room: str, background_path: Path,
                         errors: list[str]) -> Image.Image | None:
    background = image_surface(background_path, f"legacy {room}:background", errors)
    if background is None:
        return None
    canvas = background.copy()
    for path, x, y in room_layers(root, room, errors):
        try:
            layer = Image.open(path).convert("RGBA")
            layer.load()
        except (OSError, ValueError) as exc:
            add_error(errors, f"legacy {room}: cannot decode {path.name}: {exc}")
            continue
        canvas.alpha_composite(layer, dest=(x, y))
    return canvas


def legacy_asset_frames(root: Path, asset: dict[str, Any], label: str,
                        errors: list[str]) -> list[Image.Image]:
    sheet_path = repository_file(root, asset.get("sheet", asset.get("atlas")),
                                 f"{label}:sheet", errors)
    expected_hash = asset.get("sheet_sha256", asset.get("atlas_sha256"))
    if expected_hash is not None:
        verify_file_hash(sheet_path, expected_hash, f"{label}:sheet", errors)
    sheet = image_rgba(sheet_path, f"{label}:sheet", errors)
    if sheet is None:
        return []
    adapted = dict(asset)
    if "grid" not in adapted:
        adapted["grid"] = [asset.get("hframes"), asset.get("vframes")]
    if "authored_frame_count" not in adapted:
        adapted["authored_frame_count"] = asset.get("frame_count")
    frames = split_frames(sheet, adapted, label, errors)
    if frames:
        audit_frame_alpha(frames, label, errors)
        timeline = asset.get("timeline_sequence", list(range(len(frames))))
        if (not isinstance(timeline, list)
                or not MIN_FRAMES <= len(timeline) <= MAX_FRAMES
                or any(isinstance(index, bool) or not isinstance(index, int)
                       or index < 0 or index >= len(frames) for index in timeline)):
            add_error(errors, f"{label}: timeline must contain 4..12 valid states")
    return frames


def locate_source_card(source_room: Image.Image, source_card: Image.Image,
                       expected: tuple[int, int], radius: int = 24) -> tuple[int, int, float]:
    """Find the painted occurrence near runtime placement by pixel agreement."""
    width, height = source_card.size
    mask = ownership_core_mask(source_card)
    best = (expected[0], expected[1], -1.0)
    # Coarse scan followed by a one-pixel refinement keeps the gate fast while
    # allowing the small registration offsets recorded by the V2 normalizer.
    coarse: list[tuple[int, int, float]] = []
    for y in range(expected[1] - radius, expected[1] + radius + 1, 2):
        for x in range(expected[0] - radius, expected[0] + radius + 1, 2):
            if x < 0 or y < 0 or x + width > source_room.width \
                    or y + height > source_room.height:
                continue
            crop = source_room.crop((x, y, x + width, y + height))
            ratio = match_ratio(source_card, crop, mask, DUPLICATE_TOLERANCE)
            coarse.append((x, y, ratio))
            if ratio > best[2]:
                best = (x, y, ratio)
    for coarse_x, coarse_y, _ratio in sorted(
            coarse, key=lambda value: value[2], reverse=True)[:4]:
        for y in range(coarse_y - 2, coarse_y + 3):
            for x in range(coarse_x - 2, coarse_x + 3):
                if x < 0 or y < 0 or x + width > source_room.width \
                        or y + height > source_room.height:
                    continue
                crop = source_room.crop((x, y, x + width, y + height))
                ratio = match_ratio(source_card, crop, mask, DUPLICATE_TOLERANCE)
                if ratio > best[2]:
                    best = (x, y, ratio)
    return best


def audit_toilet_cavity_water(asset: dict[str, Any], label: str,
                              errors: list[str]) -> None:
    layers = asset.get("water_layers", [])
    if not isinstance(layers, list) or len(layers) != 1 \
            or not isinstance(layers[0], dict):
        add_error(errors, f"{label}: toilet requires one bowl-local vortex")
        return
    layer = layers[0]
    center = numeric_list(layer.get("center"), 2)
    radius = numeric_list(layer.get("radius"), 2)
    cavity = numeric_list(layer.get("cavity_bounds_normalized"), 4)
    if center is None or radius is None or cavity is None:
        add_error(errors, f"{label}: toilet bowl cavity geometry is incomplete")
        return
    ellipse = [
        center[0] - radius[0], center[1] - radius[1],
        center[0] + radius[0], center[1] + radius[1],
    ]
    cavity_right = cavity[0] + cavity[2]
    cavity_bottom = cavity[1] + cavity[3]
    if layer.get("role") != "vortex" \
            or layer.get("contact_role") != "inside_bowl_cavity" \
            or layer.get("active_frames") != [2, 3, 4] \
            or not 0.58 <= center[1] <= 0.65 \
            or radius[0] > 0.13 or radius[1] > 0.03 \
            or ellipse[0] < cavity[0] or ellipse[1] < cavity[1] \
            or ellipse[2] > cavity_right or ellipse[3] > cavity_bottom \
            or not 0.0 < float(layer.get("z_offset", 1.0)) <= 0.004:
        add_error(errors, f"{label}: vortex escapes the animated inner bowl cavity")


def audit_grandfathered_interactions(
        root: Path, v4_keys: set[str], healed_overrides: dict[str, Path],
        errors: list[str]) -> set[str]:
    """Prove equivalent ownership for the retained V2 and four pool cards."""
    v2 = load_json(root / V2_RELATIVE, "V2 base manifest", errors)
    v1 = load_json(
        root / "assets/flats/castle/interactions/castle_interactions.json",
        "legacy interaction manifest",
        errors,
    )
    v1_index = {
        str(value.get("id", "")): value
        for value in v1.get("assets", []) if isinstance(value, dict)
    }
    retained: dict[str, dict[str, Any]] = {}
    for value in v2.get("assets", []):
        if not isinstance(value, dict):
            continue
        if str(value.get("id", "")) in {"main_hall_sconce", "main_hall_tapestry"}:
            continue
        instances = value.get("instances", [])
        if isinstance(instances, list) and len(instances) == 1:
            retained[f"{value.get('room')}:{instances[0]}"] = value
    for value in v1.get("assets", []):
        if not isinstance(value, dict) or value.get("room") != "mermaid_pool":
            continue
        instances = value.get("instances", [])
        if isinstance(instances, list) and len(instances) == 1:
            key = f"mermaid_pool:{instances[0]}"
            retained.setdefault(key, value)

    positions = legacy_item_positions(root, errors)
    room_composites: dict[str, tuple[Path, Image.Image, Image.Image, Image.Image]] = {}
    room_masks: dict[str, Image.Image] = {}
    accepted: set[str] = set()
    for key, asset in sorted(retained.items()):
        if key in v4_keys:
            continue
        room, _item_id = key.split(":", 1)
        label = f"grandfathered {key}"
        position = positions.get(key)
        if position is None:
            add_error(errors, f"{label}: no deterministic ROOM_ITEMS position")
            continue
        legacy = v1_index.get(str(asset.get("id", "")), asset)
        room_card = root / (
            f"assets/flats/castle/rooms/room_{room}_item_{_item_id}.png"
        )
        uses_manifest_source = not room_card.is_file()
        source_path = repository_file(
            root,
            legacy.get("source") if uses_manifest_source
            else room_card.relative_to(root).as_posix(),
            f"{label}:source card",
            errors,
        )
        if uses_manifest_source and legacy.get("source_sha256") is not None:
            verify_file_hash(source_path, legacy.get("source_sha256"),
                             f"{label}:source card", errors)
        source_card = image_rgba(source_path, f"{label}:source card", errors)
        if source_card is None:
            continue
        if alpha_bbox(source_card) is None:
            add_error(errors, f"{label}: source card has no visible object")
            continue
        frames = legacy_asset_frames(root, asset, label, errors)
        if not frames:
            continue
        if asset.get("pack", "v2_base") == "v2_base":
            if asset.get("render_mode") != "generated_full_object_states" \
                    or asset.get("primary_animation_is_overlay") is not False:
                add_error(errors, f"{label}: V2 base is not a full-object state animation")
        if key == "bubble_bath:toilet":
            audit_toilet_cavity_water(asset, label, errors)

        if room not in room_composites:
            source_room_path = root / default_source_plate(room)
            background_path = healed_overrides.get(
                room, root / default_parent_background(room))
            source_room = image_surface(source_room_path,
                                        f"{label}:source room", errors)
            runtime_room = compose_runtime_room(root, room, background_path, errors)
            parent_background = image_surface(
                root / default_parent_background(room),
                f"{label}:parent background",
                errors,
            )
            if source_room is None or runtime_room is None or parent_background is None:
                continue
            room_composites[room] = (
                source_room_path, source_room, runtime_room, parent_background)
            room_masks[room] = Image.new("L", source_room.size, 0)
        _source_room_path, source_room, runtime_room, _parent = room_composites[room]
        width, height = source_card.size
        source_x, source_y, located_match = locate_source_card(
            source_room, source_card, position
        )
        if located_match < SOURCE_MATCH_MIN:
            add_error(errors, f"{label}: cannot locate source card near runtime "
                      f"placement (best exact-core match={located_match:.6f})")
            continue
        room_width, room_height = ROOM_SIZE[room]
        normalized_delta = max(
            abs(position[0] - source_x) / room_width,
            abs(position[1] - source_y) / room_height,
        )
        if normalized_delta > 0.018:
            add_error(errors, f"{label}: runtime placement moved from painted "
                      f"occurrence (normalized delta={normalized_delta:.6f})")
        card_mask = ownership_core_mask(source_card)
        source_crop = source_room.crop(
            (source_x, source_y, source_x + width, source_y + height)
        )
        runtime_crop = runtime_room.crop(
            (source_x, source_y, source_x + width, source_y + height)
        )
        source_match = match_ratio(source_card, source_crop, card_mask)
        duplicate_match = match_ratio(
            source_card, runtime_crop, card_mask, DUPLICATE_TOLERANCE
        )
        healing_change = change_ratio(
            source_crop, runtime_crop, card_mask, HEALING_TOLERANCE
        )
        if source_match < SOURCE_MATCH_MIN:
            add_error(errors, f"{label}: source card does not own painted room pixels "
                      f"(match={source_match:.6f})")
        if duplicate_match > DUPLICATE_MATCH_MAX:
            add_error(errors, f"{label}: duplicate source pixels remain in runtime room "
                      f"(match={duplicate_match:.6f})")
        if healing_change < HEALED_CHANGE_MIN:
            add_error(errors, f"{label}: runtime room is not healed under source card "
                      f"(changed={healing_change:.6f})")
        existing = room_masks[room].crop(
            (source_x, source_y, source_x + width, source_y + height)
        )
        room_masks[room].paste(
            ImageChops.lighter(existing, card_mask), (source_x, source_y)
        )
        accepted.add(key)

    # Obsolete hall atlases may remain in source manifests but must not be
    # instantiated. Runtime retirement and removal of HALL_ITEMS are both
    # required so an old cutout cannot silently return.
    fixture = runtime_text(root, errors)
    room_text = (root / ROOM_RUNTIME_RELATIVE).read_text(encoding="utf-8")
    retired_match = re.search(
        r'const\s+RETIRED_V2_ASSET_IDS[^=]*=\s*\[(.*?)\]',
        fixture,
        flags=re.DOTALL,
    )
    retired_block = retired_match.group(1) if retired_match else ""
    for asset_id in ("main_hall_sconce", "main_hall_tapestry"):
        if asset_id not in retired_block:
            add_error(errors, f"obsolete Hall asset is not retired: {asset_id}")
    if "const HALL_ITEMS" in room_text:
        add_error(errors, "obsolete Hall interaction cutouts remain in HALL_ITEMS")
    return accepted


def v4_assets(manifest: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    values = manifest.get("assets", [])
    if not isinstance(values, list):
        add_error(errors, "V4 manifest: assets must be a list")
        return []
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for value in values:
        if not isinstance(value, dict):
            add_error(errors, "V4 manifest: invalid asset record")
            continue
        asset_id = str(value.get("id", ""))
        if not asset_id or asset_id in ids:
            add_error(errors, f"V4 manifest: missing/duplicate asset id {asset_id!r}")
            continue
        ids.add(asset_id)
        result.append(value)
    return result


def audit_pool_static_alpha_ownership(
        root: Path, assets: list[dict[str, Any]], errors: list[str]) -> None:
    """Prove the Pool mid card carries no rendered copy of V4 source objects."""
    path = root / "assets/flats/castle/rooms/room_mermaid_pool_mid_pool.png"
    try:
        static = Image.open(path).convert("RGBA")
    except (OSError, ValueError) as exc:
        add_error(errors, f"Pool static ownership audit cannot decode mid card: {exc}")
        return
    canvas = Image.new("L", ROOM_SIZE["mermaid_pool"], 0)
    canvas.paste(static.getchannel("A").point(
        lambda value: 255 if value >= 128 else 0), (0, 218))
    for asset in assets:
        if str(asset.get("room", "")) != "mermaid_pool":
            continue
        label = f"Pool static ownership {asset.get('id', '<missing>')}"
        rect = source_rect(asset.get("source_rect"), "mermaid_pool")
        mask_path = repository_file(
            root, asset.get("mask_path"), f"{label}:mask", errors)
        mask = image_mask(mask_path, f"{label}:mask", errors)
        if rect is None or mask is None:
            continue
        x, y, width, height = rect
        full = Image.new("L", canvas.size, 0)
        full.paste(mask.point(
            lambda value: 255 if value >= 128 else 0), (x, y))
        overlap = ImageChops.multiply(canvas, full).histogram()[255]
        if overlap:
            add_error(errors, f"{label}: {overlap} rendered duplicate mid-card pixels")
    room_text = (root / ROOM_RUNTIME_RELATIVE).read_text(encoding="utf-8")
    flower_start = room_text.find('{"id": "flower_float"')
    flower_block = room_text[flower_start:flower_start + 700] \
        if flower_start >= 0 else ""
    if '"z": MIDGROUND_Z + 0.02' not in flower_block:
        add_error(errors, "Pool flower bloom is not deterministically above mid water")


def audit(root: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    fixture_text = runtime_text(root, errors)
    additions = active_v3_additions(root, fixture_text, errors)
    if additions:
        add_error(errors, "runtime still references forbidden pack:v3_addition assets: "
                  + ",".join(additions))

    runtime_v4 = literal_constant(fixture_text, "MANIFEST_PATH")
    expected_v4 = V4_RELATIVE.as_posix()
    if runtime_v4.replace("\\", "/") != expected_v4:
        add_error(errors, f"runtime MANIFEST_PATH must be res://{expected_v4}")
    if "_normalized_native_v4_entry" not in fixture_text \
            or 'ownership.get("source_rect"' not in fixture_text:
        add_error(errors, "runtime placement is not derived from source_ownership.source_rect")

    manifest = load_json(manifest_path, "V4 manifest", errors)
    if not manifest:
        return errors
    schema = manifest.get("schema_version")
    if schema not in (4, "4", "4.0"):
        add_error(errors, "V4 manifest: schema_version must identify V4")
    assets = v4_assets(manifest, errors)
    audit_pool_static_alpha_ownership(root, assets, errors)
    runtime_tile_rooms = audit_runtime_background_tiles(
        root, manifest, assets, errors)
    surface_masks: dict[tuple[Path, Path], Image.Image] = {}
    surface_images: dict[tuple[Path, Path], tuple[Image.Image, Image.Image]] = {}
    healed_overrides: dict[str, Path] = {}
    v4_keys: set[str] = set()
    for asset in assets:
        v4_keys.update(audit_asset(
            root, asset, surface_masks, surface_images, healed_overrides, errors,
            runtime_tile_rooms,
        ))
    audit_outside_owned_regions(surface_masks, surface_images, errors)

    grandfathered_keys = audit_grandfathered_interactions(
        root, v4_keys, healed_overrides, errors
    )

    # INTERACTION_SPECS is the deterministic registry of legacy animated room
    # items.  A key left there but absent from V4 is still an active interaction
    # without V4 ownership evidence, even if an older delivery manifest exists.
    legacy_keys = scripted_interactions(root, errors)
    missing = sorted(legacy_keys - v4_keys - grandfathered_keys)
    if missing:
        add_error(errors, "runtime interactions lack V4 painted-source ownership: "
                  + ",".join(missing))
    return errors


def print_result(errors: Iterable[str]) -> int:
    messages = list(errors)
    if messages:
        for message in messages:
            print(f"CASTLE_NATIVE|FAIL|{message}")
        print(f"CASTLE_NATIVE|RESULT=FAIL|checks_failed={len(messages)}")
        return 1
    print("CASTLE_NATIVE|RESULT=OK|painted_source_ownership=true|duplicates=0")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = args.manifest.resolve() if args.manifest else root / V4_RELATIVE
    return print_result(audit(root, manifest))


if __name__ == "__main__":
    sys.exit(main())
