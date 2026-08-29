#!/usr/bin/env python3
"""Generate and gate exact per-frame review evidence for Castle V4 objects.

This repository-facing layer deliberately keeps review generation separate from
approval.  ``generate`` writes deterministic contact sheets and a candidate
JSON below ignored ``audit/``.  ``check`` regenerates that candidate and accepts
it only when a separately authored ledger names the exact candidate and frame
hashes.  There is intentionally no command that promotes candidate hashes into
the approval ledger.

Primary coverage is always the authored atlas frame after the runtime's 0.5
alpha scissor.  Water shaders, particles, and other secondary effects are never
allowed to conceal exposed healing or satisfy object coverage.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass, replace
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Mapping, Sequence

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont


TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import audit_castle_static_depth_cards as static_cards_audit  # noqa: E402
import castle_interaction_frame_qa as frame_qa  # noqa: E402


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
V4_MANIFEST_RELATIVE = Path(
    "assets/flats/castle/interactions_v4/castle_interactions_v4.json")
RUNTIME_LAYOUT_RELATIVE = Path("scripts/arena/castle_rooms_25d.gd")
DEFAULT_OUTPUT_RELATIVE = Path("audit/castle_interaction_frame_review_v4")
DEFAULT_APPROVAL_RELATIVE = Path(
    "assets_src/castle/interactions_v4/"
    "castle_interaction_frame_approval_ledger.json")
CANDIDATE_FILENAME = "castle_interaction_frame_candidate_v4.json"

CANDIDATE_SCHEMA = "castle_interaction_frame_candidate_v2"
APPROVAL_SCHEMA = "castle_interaction_frame_approval_v2"
EXPECTED_V4_ASSET_COUNT = 12
LOGICAL_ROOM_SIZE = (1024, 576)
STATIC_ALPHA_THRESHOLD = 128
MINIMUM_ABSOLUTE_Z_DELTA = 0.01

LAYER_CONSTANTS = {
    "mid": "MIDGROUND_Z",
    "front": "FOREGROUND_Z",
}


class ReviewInputError(RuntimeError):
    """Raised when repository evidence cannot be reproduced exactly."""


@dataclass(frozen=True)
class StaticCard:
    """One active ROOM_LAYOUTS mid/front card placed in logical room space."""

    room: str
    card_id: str
    layer: str
    path: str
    position: tuple[float, float]
    z: float
    rgba: Image.Image
    alpha_mask: Image.Image
    file_sha256: str
    alpha_pixel_sha256: str

    def evidence(self) -> dict[str, Any]:
        return {
            "room": self.room,
            "card_id": self.card_id,
            "layer": self.layer,
            "path": self.path,
            "position": [self.position[0], self.position[1]],
            "z": self.z,
            "file_sha256": self.file_sha256,
            "alpha_pixel_sha256": self.alpha_pixel_sha256,
            "alpha_threshold": STATIC_ALPHA_THRESHOLD,
        }


@dataclass(frozen=True)
class RepositoryReviewBuild:
    """In-memory candidate plus deterministic files and blocking findings."""

    candidate: dict[str, Any]
    contact_sheets: dict[str, bytes]
    blocking_findings: tuple[str, ...]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def semantic_json_sha256(value: Any) -> str:
    """Hash parsed JSON semantics, independent of checkout line endings."""
    return sha256_bytes(canonical_json_bytes(value))


def normalized_text_sha256(text: str) -> str:
    """Hash UTF-8 text after normalizing CRLF/CR to repository LF."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(normalized.encode("utf-8"))


def candidate_payload_sha256(candidate: Mapping[str, Any]) -> str:
    """Hash candidate content without its self-referential digest field."""
    payload = deepcopy(dict(candidate))
    payload.pop("candidate_payload_sha256", None)
    return sha256_bytes(canonical_json_bytes(payload))


def seal_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    sealed = deepcopy(dict(candidate))
    sealed.pop("candidate_payload_sha256", None)
    sealed["candidate_payload_sha256"] = candidate_payload_sha256(sealed)
    return sealed


def _repository_file(root: Path, value: object, label: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ReviewInputError(f"{label} must be a repository-relative POSIX path")
    relative = Path(value)
    if relative.is_absolute():
        raise ReviewInputError(f"{label} must be repository-relative")
    root_resolved = root.resolve()
    path = (root_resolved / relative).resolve()
    try:
        path.relative_to(root_resolved)
    except ValueError as exc:
        raise ReviewInputError(f"{label} escapes the repository: {value}") from exc
    if not path.is_file():
        raise ReviewInputError(f"{label} is missing: {value}")
    return path


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _verify_hash(path: Path, expected: object, label: str) -> str:
    measured = sha256_file(path)
    if not isinstance(expected, str) or measured != expected:
        raise ReviewInputError(
            f"{label} hash mismatch: expected={expected!r}, measured={measured}")
    return measured


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReviewInputError(f"cannot load {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReviewInputError(f"{label} must contain a JSON object")
    return value


def _numeric_pair(value: object, label: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise ReviewInputError(f"{label} must contain exactly two numbers")
    try:
        result = (float(value[0]), float(value[1]))
    except (TypeError, ValueError) as exc:
        raise ReviewInputError(f"{label} must contain exactly two numbers") from exc
    if not all(math.isfinite(item) for item in result):
        raise ReviewInputError(f"{label} contains a non-finite number")
    return result


def _integer_pair(value: object, label: str) -> tuple[int, int]:
    pair = _numeric_pair(value, label)
    result = (int(pair[0]), int(pair[1]))
    if pair != (float(result[0]), float(result[1])) or min(result) <= 0:
        raise ReviewInputError(f"{label} must contain two positive integers")
    return result


def _source_rect(asset: Mapping[str, Any]) -> tuple[int, int, int, int]:
    ownership = asset.get("source_ownership")
    if not isinstance(ownership, dict):
        raise ReviewInputError(f"{asset.get('id')}: missing source_ownership")
    value = ownership.get("source_rect", asset.get("source_rect"))
    if not isinstance(value, list) or len(value) != 4:
        raise ReviewInputError(f"{asset.get('id')}: invalid source_rect")
    try:
        floats = tuple(float(item) for item in value)
    except (TypeError, ValueError) as exc:
        raise ReviewInputError(f"{asset.get('id')}: invalid source_rect") from exc
    integers = tuple(int(item) for item in floats)
    if floats != tuple(float(item) for item in integers):
        raise ReviewInputError(f"{asset.get('id')}: source_rect must be integral")
    x, y, width, height = integers
    if x < 0 or y < 0 or width <= 0 or height <= 0 \
            or x + width > LOGICAL_ROOM_SIZE[0] \
            or y + height > LOGICAL_ROOM_SIZE[1]:
        raise ReviewInputError(f"{asset.get('id')}: source_rect leaves the room")
    return x, y, width, height


def _image_alpha(image: Image.Image) -> Image.Image:
    if image.mode in {"RGBA", "LA"}:
        return image.getchannel("A")
    return image.convert("L")


def expand_ownership_mask(
        mask: Image.Image,
        source_rect: Sequence[int],
        room_size: tuple[int, int] = LOGICAL_ROOM_SIZE,
        ) -> Image.Image:
    """Place either a crop-local or room-sized ownership mask in room space."""
    if len(source_rect) != 4:
        raise ReviewInputError("ownership source_rect must contain four values")
    x, y, width, height = (int(value) for value in source_rect)
    alpha = _image_alpha(mask)
    if alpha.size == room_size:
        return alpha.copy()
    if alpha.size != (width, height):
        raise ReviewInputError(
            f"ownership mask size {alpha.size} does not match {(width, height)}")
    placed = Image.new("L", room_size, 0)
    placed.paste(alpha, (x, y))
    return placed


def place_static_card_alpha(
        image: Image.Image,
        position: Sequence[float],
        room_size: tuple[int, int] = LOGICAL_ROOM_SIZE,
        alpha_threshold: int = STATIC_ALPHA_THRESHOLD,
        ) -> Image.Image:
    """Place an active ROOM_LAYOUTS card under its runtime top-left transform."""
    if len(position) != 2:
        raise ReviewInputError("static-card position must have two coordinates")
    x, y = float(position[0]), float(position[1])
    placed = _image_alpha(image).transform(
        room_size,
        Image.Transform.AFFINE,
        (1.0, 0.0, -x, 0.0, 1.0, -y),
        resample=Image.Resampling.BILINEAR,
    )
    return frame_qa.binary_mask(placed, alpha_threshold)


def place_static_card_rgba(
        image: Image.Image,
        position: Sequence[float],
        room_size: tuple[int, int] = LOGICAL_ROOM_SIZE,
        alpha_threshold: int = STATIC_ALPHA_THRESHOLD,
        ) -> tuple[Image.Image, Image.Image]:
    """Place and alpha-scissor a ROOM_LAYOUTS card in logical room space."""
    if len(position) != 2:
        raise ReviewInputError("static-card position must have two coordinates")
    x, y = float(position[0]), float(position[1])
    rgba = image.convert("RGBA").transform(
        room_size,
        Image.Transform.AFFINE,
        (1.0, 0.0, -x, 0.0, 1.0, -y),
        resample=Image.Resampling.BILINEAR,
    )
    alpha = frame_qa.binary_mask(rgba.getchannel("A"), alpha_threshold)
    values = np.asarray(rgba, dtype=np.uint8).copy()
    values[np.asarray(alpha, dtype=np.uint8) == 0] = 0
    return Image.fromarray(values, mode="RGBA"), alpha


def _runtime_constants(runtime_text: str) -> dict[str, float]:
    constants: dict[str, float] = {}
    for name, value in re.findall(
            r"(?m)^const\s+([A-Z][A-Z0-9_]*)\s*:=\s*"
            r"(-?(?:\d+(?:\.\d*)?|\.\d+))\s*$",
            runtime_text):
        constants[name] = float(value)
    required = {"MIDGROUND_Z", "FOREGROUND_Z"}
    missing = sorted(required - set(constants))
    if missing:
        raise ReviewInputError(f"runtime lacks numeric constants: {missing}")
    return constants


def _room_mapping_block(text: str, constant: str, room: str) -> str:
    start = text.find(f"const {constant} := {{")
    if start < 0:
        return ""
    room_start = text.find(f'\n\t"{room}":', start)
    if room_start < 0:
        return ""
    line_end = text.find("\n", room_start + 1)
    if line_end < 0:
        return text[room_start:]
    match = re.search(
        r'(?m)^\t"[a-z0-9_]+":', text[line_end + 1:])
    if match is None:
        return text[room_start:]
    return text[room_start:line_end + 1 + match.start()]


def _evaluate_depth(expression: str, constants: Mapping[str, float]) -> float:
    match = re.fullmatch(
        r"\s*([A-Z][A-Z0-9_]*|-?(?:\d+(?:\.\d*)?|\.\d+))"
        r"(?:\s*([+-])\s*((?:\d+(?:\.\d*)?|\.\d+)))?\s*",
        expression,
    )
    if match is None:
        raise ReviewInputError(f"unsupported runtime z expression: {expression!r}")
    base_token = match.group(1)
    if re.fullmatch(r"[A-Z][A-Z0-9_]*", base_token):
        if base_token not in constants:
            raise ReviewInputError(f"unknown runtime z constant: {base_token}")
        value = float(constants[base_token])
    else:
        value = float(base_token)
    if match.group(2):
        offset = float(match.group(3))
        value += offset if match.group(2) == "+" else -offset
    if not math.isfinite(value):
        raise ReviewInputError(f"non-finite runtime z expression: {expression!r}")
    return value


def runtime_asset_depths(
        runtime_text: str,
        fixture_text: str,
        assets: Sequence[Mapping[str, Any]],
        ) -> dict[str, tuple[float, str]]:
    """Reproduce legacy-item preservation and native-item default z routing."""
    constants = _runtime_constants(runtime_text)
    default_match = re.search(
        r'"z"\s*:\s*float\(entry\.get\("z",\s*'
        r'(-?(?:\d+(?:\.\d*)?|\.\d+))\s*\)\)',
        fixture_text,
    )
    if default_match is None:
        raise ReviewInputError("cannot locate native V4 runtime z default")
    native_default = float(default_match.group(1))
    result: dict[str, tuple[float, str]] = {}
    room_blocks: dict[str, str] = {}
    for asset in assets:
        asset_id = str(asset.get("id", ""))
        room = str(asset.get("room", ""))
        instances = asset.get("instances")
        if not asset_id or not room or not isinstance(instances, list) \
                or len(instances) != 1 or not isinstance(instances[0], str):
            raise ReviewInputError(f"{asset_id or '<asset>'}: invalid runtime instance")
        instance = instances[0]
        block = room_blocks.setdefault(
            room, _room_mapping_block(runtime_text, "ROOM_ITEMS", room))
        matches = list(re.finditer(
            r'\{"id":\s*"([a-z0-9_]+)"', block))
        item_expression: str | None = None
        for index, match in enumerate(matches):
            if match.group(1) != instance:
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) \
                else len(block)
            record = block[match.start():end]
            z_match = re.search(r'"z"\s*:\s*([^,\n}]+)', record)
            if z_match is None:
                raise ReviewInputError(f"ROOM_ITEMS.{room}:{instance} lacks z")
            item_expression = z_match.group(1).strip()
            break
        if item_expression is not None:
            result[asset_id] = (
                _evaluate_depth(item_expression, constants),
                f"ROOM_ITEMS.{room}:{instance}",
            )
            continue
        if "z" in asset:
            try:
                asset_z = float(asset["z"])
            except (TypeError, ValueError) as exc:
                raise ReviewInputError(f"{asset_id}: invalid manifest z") from exc
            if not math.isfinite(asset_z):
                raise ReviewInputError(f"{asset_id}: invalid manifest z")
            result[asset_id] = (asset_z, "V4 manifest asset.z")
        else:
            result[asset_id] = (native_default, "CastleFixtureRigs native default")
    return result


def reconstruct_logical_underlay(
        root: Path,
        room: str,
        route: Mapping[str, Any],
        ) -> tuple[Image.Image, dict[str, Any]]:
    """Rebuild the exact readiness-gated V4 tile set into logical room space."""
    grid = _integer_pair(route.get("grid"), f"{room}: route grid")
    tile_size = _integer_pair(
        route.get("tile_dimensions"), f"{room}: tile dimensions")
    native_size = _integer_pair(
        route.get("native_canvas_size"), f"{room}: native canvas")
    logical_size = _integer_pair(
        route.get("logical_canvas_size"), f"{room}: logical canvas")
    if logical_size != LOGICAL_ROOM_SIZE:
        raise ReviewInputError(
            f"{room}: logical canvas is {logical_size}, expected {LOGICAL_ROOM_SIZE}")
    columns, rows = grid
    if native_size != (columns * tile_size[0], rows * tile_size[1]):
        raise ReviewInputError(f"{room}: native route dimensions are inconsistent")
    if logical_size[0] % columns or logical_size[1] % rows:
        raise ReviewInputError(f"{room}: logical canvas is not divisible by route grid")
    logical_cell = (logical_size[0] // columns, logical_size[1] // rows)
    tiles = route.get("tiles")
    if not isinstance(tiles, list) or len(tiles) != columns * rows:
        raise ReviewInputError(f"{room}: runtime V4 tile set is incomplete")

    logical = Image.new("RGB", logical_size)
    evidence: list[dict[str, Any]] = []
    for index, record_value in enumerate(tiles):
        if not isinstance(record_value, dict):
            raise ReviewInputError(f"{room}: invalid runtime tile record {index}")
        path = _repository_file(
            root, record_value.get("path"), f"{room}: runtime tile {index}")
        measured_hash = _verify_hash(
            path, record_value.get("sha256"), f"{room}: runtime tile {index}")
        try:
            image = Image.open(path).convert("RGBA")
            image.load()
        except (OSError, ValueError) as exc:
            raise ReviewInputError(f"{room}: cannot decode runtime tile {path}") from exc
        if image.size != tile_size:
            raise ReviewInputError(
                f"{room}: runtime tile {path.name} has size {image.size}")
        if image.getchannel("A").getextrema() != (255, 255):
            raise ReviewInputError(f"{room}: runtime tile {path.name} is not opaque")
        row, column = divmod(index, columns)
        resized = image.convert("RGB").resize(
            logical_cell, Image.Resampling.LANCZOS)
        logical.paste(
            resized, (column * logical_cell[0], row * logical_cell[1]))
        evidence.append({
            "row": row,
            "column": column,
            "path": _relative(root, path),
            "file_sha256": measured_hash,
            "dimensions": [image.width, image.height],
        })
    return logical.convert("RGBA"), {
        "room": room,
        "route": str(route.get("route", "")),
        "grid": [columns, rows],
        "native_canvas_size": list(native_size),
        "logical_canvas_size": list(logical_size),
        "logical_cell_size": list(logical_cell),
        "reconstruction": "per_tile_lanczos_to_runtime_logical_cells",
        "logical_pixel_sha256": frame_qa.raw_pixel_sha256(logical),
        "tiles": evidence,
    }


def load_static_cards(
        root: Path,
        runtime_text: str,
        rooms: set[str],
        ) -> list[StaticCard]:
    """Load every active V4-room mid/front card directly from ROOM_LAYOUTS."""
    constants = _runtime_constants(runtime_text)
    try:
        records, _ = static_cards_audit.parse_runtime_cards(runtime_text)
    except static_cards_audit.AuditInputError as exc:
        raise ReviewInputError(f"cannot parse active ROOM_LAYOUTS: {exc}") from exc
    cards: list[StaticCard] = []
    for record in records:
        room = str(record["room"])
        if room not in rooms:
            continue
        layer = str(record["layer"])
        if layer not in LAYER_CONSTANTS:
            raise ReviewInputError(f"unexpected ROOM_LAYOUTS layer: {layer}")
        path = _repository_file(root, record["path"], f"{room}:{layer} card")
        try:
            image = Image.open(path).convert("RGBA")
            image.load()
        except (OSError, ValueError) as exc:
            raise ReviewInputError(f"cannot decode static card: {path}") from exc
        position = (
            float(record["position"][0]), float(record["position"][1]))
        placed_rgba, alpha = place_static_card_rgba(image, position)
        cards.append(StaticCard(
            room=room,
            card_id=str(record["id"]),
            layer=layer,
            path=_relative(root, path),
            position=position,
            z=float(constants[LAYER_CONSTANTS[layer]]),
            rgba=placed_rgba,
            alpha_mask=alpha,
            file_sha256=sha256_file(path),
            alpha_pixel_sha256=frame_qa.raw_pixel_sha256(alpha),
        ))
    return sorted(cards, key=lambda card: (
        card.room, card.layer, card.path, card.position))


def compose_depth_aware_frame(
        _approved_room: Image.Image,
        runtime_underlay: Image.Image,
        _ownership_mask: Image.Image,
        placed_frame: frame_qa.PlacedFrame,
        static_cards: Sequence[StaticCard],
        asset_z: float,
        ) -> Image.Image:
    """Reapply active static cards on the correct side of the target object.

    The complete generated room background owns every noninteractive pixel.
    Starting from the historical approved room and clearing only a legacy
    ownership mask can resurrect baked copies outside that mask, so the review
    compositor starts from the exact readiness-gated runtime background.  Real
    static cards are then composited behind or in front according to z.
    Coplanar cards are drawn in front only to keep the candidate deterministic;
    their zero delta is an unconditional gate failure.
    """
    base = runtime_underlay.convert("RGBA")
    ordered = sorted(static_cards, key=lambda card: (
        card.z, card.layer, card.path))
    for card in ordered:
        base.paste(runtime_underlay, (0, 0), card.alpha_mask)
    for card in ordered:
        if card.z < asset_z:
            base.alpha_composite(card.rgba)
    base.alpha_composite(placed_frame.rgba)
    for card in ordered:
        if card.z >= asset_z:
            base.alpha_composite(card.rgba)
    return base


def replace_result_composite(
        result: frame_qa.FrameQAResult,
        composite: Image.Image,
        ) -> frame_qa.FrameQAResult:
    """Bind the QA record to the repository's depth-aware review composite."""
    if composite.size != result.composite.size:
        raise ValueError("replacement composite has a different room size")
    composite_hash = frame_qa.raw_pixel_sha256(
        composite.convert("RGB").crop(result.record.review_crop))
    return replace(
        result,
        record=replace(
            result.record, composite_pixel_sha256=composite_hash),
        composite=composite,
    )


def measure_frame_occlusions(
        primary_alpha_mask: Image.Image,
        static_cards: Sequence[StaticCard],
        asset_z: float,
        ) -> tuple[list[dict[str, Any]], list[Image.Image]]:
    """Intersect primary alpha only with active static-card alpha at 128."""
    primary = frame_qa.binary_mask(
        primary_alpha_mask, frame_qa.DEFAULT_ALPHA_SCISSOR_THRESHOLD)
    relations: list[dict[str, Any]] = []
    masks: list[Image.Image] = []
    for card in static_cards:
        if card.alpha_mask.size != primary.size:
            raise ReviewInputError(
                f"static card {card.path} has a different logical canvas")
        overlap = ImageChops.multiply(primary, card.alpha_mask)
        pixels = int(np.count_nonzero(np.asarray(overlap, dtype=np.uint8)))
        if not pixels:
            continue
        signed_delta = round(float(asset_z) - float(card.z), 6)
        relations.append({
            "card_id": card.card_id,
            "card_path": card.path,
            "layer": card.layer,
            "card_z": card.z,
            "asset_z": float(asset_z),
            "signed_z_delta": signed_delta,
            "relation": (
                "asset_in_front_of_card" if signed_delta > 0.0
                else "card_in_front_of_asset" if signed_delta < 0.0
                else "coplanar_forbidden"
            ),
            "overlap_pixels": pixels,
            "overlap_pixel_sha256": frame_qa.raw_pixel_sha256(overlap),
        })
        masks.append(overlap)
    paired = sorted(zip(relations, masks), key=lambda item: (
        item[0]["layer"], item[0]["card_path"]))
    return [item[0] for item in paired], [item[1] for item in paired]


def nonwaivable_frame_issues(
        asset_id: str,
        result: frame_qa.FrameQAResult,
        occlusions: Sequence[Mapping[str, Any]],
        ) -> list[str]:
    """Return source-duplicate and coplanar/static-depth hard failures."""
    problems: list[str] = []
    record = result.record
    large_components = [
        component for component in record.duplicate_components
        if component.pixels >= record.duplicate_component_min_pixels
    ]
    if large_components:
        problems.append(
            f"{asset_id} frame {record.frame_index}: exposed source duplicate "
            f"has {large_components[0].pixels} connected pixels")
    for relation in occlusions:
        delta = float(relation["signed_z_delta"])
        if abs(delta) + 1.0e-12 < MINIMUM_ABSOLUTE_Z_DELTA:
            problems.append(
                f"{asset_id} frame {record.frame_index}: static-card overlap "
                f"with {relation['card_path']} has signed z delta {delta:.6f}; "
                f"minimum absolute delta is {MINIMUM_ABSOLUTE_Z_DELTA:.6f}")
    return problems


def _tint_mask(
        image: Image.Image,
        mask: Image.Image,
        color: tuple[int, int, int],
        opacity: int = 120,
        ) -> Image.Image:
    base = image.convert("RGBA")
    alpha_values = np.asarray(mask.convert("L"), dtype=np.uint16)
    tinted_alpha = Image.fromarray(
        ((alpha_values * opacity) // 255).astype(np.uint8), mode="L")
    overlay = Image.new("RGBA", base.size, (*color, 0))
    overlay.putalpha(tinted_alpha)
    return Image.alpha_composite(base, overlay)


def _fit_review_image(
        image: Image.Image,
        maximum: tuple[int, int] = (320, 238),
        ) -> Image.Image:
    scale = min(maximum[0] / image.width, maximum[1] / image.height)
    if scale >= 1.0:
        scale = float(max(1, min(3, int(math.floor(scale)))))
        resampling = Image.Resampling.NEAREST
    else:
        resampling = Image.Resampling.LANCZOS
    size = (
        max(1, int(round(image.width * scale))),
        max(1, int(round(image.height * scale))),
    )
    return image.resize(size, resampling)


def render_contact_sheet(
        asset_record: Mapping[str, Any],
        results: Sequence[frame_qa.FrameQAResult],
        occlusion_masks_by_frame: Sequence[Sequence[Image.Image]],
        *,
        show_diagnostics: bool = True,
        ) -> Image.Image:
    """Render a deterministic labeled review sheet for every authored frame.

    The diagnostic sheet colors measured masks for forensic inspection.  The
    companion plain sheet deliberately shows the exact depth-aware composite
    without those colors so a reviewer can judge the artwork itself.
    """
    if len(results) != len(occlusion_masks_by_frame):
        raise ValueError("occlusion-mask groups must match result count")
    columns = 4
    rows = int(math.ceil(len(results) / columns))
    tile_size = (352, 310)
    header_height = 54
    sheet = Image.new(
        "RGBA", (columns * tile_size[0], header_height + rows * tile_size[1]),
        (24, 22, 38, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    asset_id = str(asset_record["id"])
    room = str(asset_record["room"])
    draw.text(
        (10, 7), f"{asset_id} | room={room} | z={asset_record['asset_z']:.3f}",
        fill=(255, 255, 255, 255), font=font)
    subtitle = (
        "red=exposed heal | magenta=outside ownership | "
        "yellow=source duplicate | cyan=static overlap"
        if show_diagnostics else
        "plain depth-aware runtime composite | no diagnostic tint"
    )
    draw.text((10, 27), subtitle, fill=(205, 210, 232, 255), font=font)
    for index, result in enumerate(results):
        row, column = divmod(index, columns)
        origin = (
            column * tile_size[0], header_height + row * tile_size[1])
        draw.rectangle((
            origin[0] + 3, origin[1] + 3,
            origin[0] + tile_size[0] - 4,
            origin[1] + tile_size[1] - 4,
        ), outline=(94, 89, 126, 255), width=1)
        crop = result.record.review_crop
        review = result.composite.crop(crop)
        occlusion_union = Image.new("L", result.composite.size, 0)
        for mask in occlusion_masks_by_frame[index]:
            occlusion_union = ImageChops.lighter(occlusion_union, mask)
        if show_diagnostics:
            review = _tint_mask(
                review, result.exposed_heal_mask.crop(crop), (255, 45, 45))
            review = _tint_mask(
                review, result.outside_ownership_mask.crop(crop),
                (255, 36, 210))
            review = _tint_mask(
                review, result.duplicate_exposed_mask.crop(crop),
                (255, 220, 35))
            review = _tint_mask(
                review, occlusion_union.crop(crop), (30, 220, 255))
        fitted = _fit_review_image(review)
        image_x = origin[0] + (tile_size[0] - fitted.width) // 2
        image_y = origin[1] + 48 + (238 - fitted.height) // 2
        sheet.alpha_composite(fitted, (image_x, image_y))
        qa_record = result.record
        occlusion_pixels = sum(int(np.count_nonzero(
            np.asarray(mask, dtype=np.uint8)))
            for mask in occlusion_masks_by_frame[index])
        draw.text(
            (origin[0] + 9, origin[1] + 10),
            f"frame {qa_record.frame_index} | primary "
            f"{qa_record.primary_visible_pixels}",
            fill=(255, 255, 255, 255), font=font)
        draw.text(
            (origin[0] + 9, origin[1] + 27),
            f"heal {qa_record.exposed_heal_pixels} | outside "
            f"{qa_record.outside_ownership_pixels} | dup "
            f"{qa_record.duplicate_exposed_pixels} | static {occlusion_pixels}",
            fill=(226, 226, 236, 255), font=font)
    return sheet


def png_bytes(image: Image.Image) -> bytes:
    stream = BytesIO()
    image.save(stream, format="PNG", optimize=False, compress_level=9)
    return stream.getvalue()


def contact_sheet_evidence(filename: str, image: Image.Image) -> dict[str, Any]:
    """Bind review-visible pixels, never platform-specific PNG compression."""
    return {
        "file": filename,
        "pixel_sha256": frame_qa.raw_pixel_sha256(image),
        "dimensions": list(image.size),
    }


def _frame_approval_payload(
        qa_record: Mapping[str, Any],
        occlusions: Sequence[Mapping[str, Any]],
        ) -> dict[str, Any]:
    return {
        "qa": deepcopy(dict(qa_record)),
        "static_occlusions": [deepcopy(dict(value)) for value in occlusions],
        "primary_coverage_includes_secondary_effects": False,
    }


def _flatten_occlusion_relations(
        frames: Sequence[Mapping[str, Any]],
        ) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for frame in frames:
        frame_index = int(frame["frame_index"])
        for relation_value in frame.get("static_occlusions", []):
            relation = {"frame_index": frame_index, **dict(relation_value)}
            result.append(relation)
    return sorted(result, key=lambda value: (
        int(value["frame_index"]), str(value["layer"]),
        str(value["card_path"])))


def build_repository_candidate(
        root: Path = REPOSITORY_ROOT,
        manifest_relative: Path = V4_MANIFEST_RELATIVE,
        runtime_relative: Path = RUNTIME_LAYOUT_RELATIVE,
        ) -> RepositoryReviewBuild:
    """Load all 12 V4 assets and produce exact per-frame review evidence."""
    root = root.resolve()
    manifest_path = _repository_file(
        root, manifest_relative.as_posix(), "V4 manifest")
    runtime_path = _repository_file(
        root, runtime_relative.as_posix(), "castle room runtime")
    fixture_path = _repository_file(
        root, "scripts/arena/castle_fixture_rigs.gd", "fixture runtime")
    manifest = _load_json(manifest_path, "V4 manifest")
    if manifest.get("schema_version") != 4:
        raise ReviewInputError("V4 manifest schema_version must be 4")
    assets_value = manifest.get("assets")
    if not isinstance(assets_value, list):
        raise ReviewInputError("V4 manifest assets must be a list")
    assets = [value for value in assets_value if isinstance(value, dict)]
    if len(assets) != len(assets_value):
        raise ReviewInputError("V4 manifest contains a non-object asset")
    if len(assets) != EXPECTED_V4_ASSET_COUNT:
        raise ReviewInputError(
            f"V4 asset count is {len(assets)}; expected {EXPECTED_V4_ASSET_COUNT}")
    asset_ids = [str(asset.get("id", "")) for asset in assets]
    if any(not value for value in asset_ids) or len(set(asset_ids)) != len(asset_ids):
        raise ReviewInputError("V4 asset ids are missing or duplicated")
    assets = sorted(assets, key=lambda asset: (
        str(asset.get("room", "")), str(asset.get("id", ""))))
    rooms = {str(asset.get("room", "")) for asset in assets}
    if "" in rooms:
        raise ReviewInputError("V4 asset room is missing")

    runtime_text = runtime_path.read_text(encoding="utf-8")
    fixture_text = fixture_path.read_text(encoding="utf-8")
    asset_depths = runtime_asset_depths(runtime_text, fixture_text, assets)
    static_cards = load_static_cards(root, runtime_text, rooms)
    cards_by_room: dict[str, list[StaticCard]] = {
        room: [card for card in static_cards if card.room == room]
        for room in rooms
    }

    routes = manifest.get("runtime_background_tiles")
    room_records = manifest.get("rooms")
    if not isinstance(routes, dict) or set(routes) != rooms:
        raise ReviewInputError(
            "runtime_background_tiles must exactly cover the 12 assets' rooms")
    if not isinstance(room_records, dict) or not rooms.issubset(room_records):
        raise ReviewInputError("V4 manifest room records are incomplete")

    approved_rooms: dict[str, Image.Image] = {}
    runtime_underlays: dict[str, Image.Image] = {}
    room_evidence: dict[str, dict[str, Any]] = {}
    for room in sorted(rooms):
        room_record = room_records[room]
        if not isinstance(room_record, dict):
            raise ReviewInputError(f"{room}: invalid manifest room record")
        approved_path = _repository_file(
            root, room_record.get("source_room_plate"),
            f"{room}: approved logical room")
        approved_hash = _verify_hash(
            approved_path, room_record.get("source_room_plate_sha256"),
            f"{room}: approved logical room")
        try:
            approved = Image.open(approved_path).convert("RGBA")
            approved.load()
        except (OSError, ValueError) as exc:
            raise ReviewInputError(
                f"{room}: cannot decode approved logical room") from exc
        if approved.size != LOGICAL_ROOM_SIZE:
            raise ReviewInputError(
                f"{room}: approved logical room size is {approved.size}")
        route = routes[room]
        if not isinstance(route, dict):
            raise ReviewInputError(f"{room}: invalid V4 runtime route")
        underlay, underlay_evidence = reconstruct_logical_underlay(
            root, room, route)
        approved_rooms[room] = approved
        runtime_underlays[room] = underlay
        room_evidence[room] = {
            "approved_logical_room": {
                "path": _relative(root, approved_path),
                "file_sha256": approved_hash,
                "pixel_sha256": frame_qa.raw_pixel_sha256(approved),
                "dimensions": list(approved.size),
            },
            "runtime_v4_underlay": underlay_evidence,
        }

    contact_sheets: dict[str, bytes] = {}
    candidate_assets: list[dict[str, Any]] = []
    blocking_findings: list[str] = []
    frame_total = 0
    for asset in assets:
        asset_id = str(asset["id"])
        room = str(asset["room"])
        if asset.get("pack") != "v4_native":
            raise ReviewInputError(f"{asset_id}: pack must be v4_native")
        rect = _source_rect(asset)
        ownership = asset["source_ownership"]
        approved_path_expected = asset.get("source_room_plate_path")
        approved_path_actual = room_evidence[room]["approved_logical_room"]["path"]
        if approved_path_expected != approved_path_actual:
            raise ReviewInputError(
                f"{asset_id}: source_room_plate_path disagrees with room record")
        if ownership.get("source_room_plate_sha256") != \
                room_evidence[room]["approved_logical_room"]["file_sha256"]:
            raise ReviewInputError(f"{asset_id}: approved room hash is stale")

        mask_path = _repository_file(
            root, asset.get("mask_path"), f"{asset_id}: ownership mask")
        mask_hash = _verify_hash(
            mask_path, ownership.get("mask_sha256"),
            f"{asset_id}: ownership mask")
        try:
            mask_image = Image.open(mask_path)
            mask_image.load()
        except (OSError, ValueError) as exc:
            raise ReviewInputError(
                f"{asset_id}: cannot decode ownership mask") from exc
        ownership_full = expand_ownership_mask(mask_image, rect)

        sheet_path = _repository_file(
            root, asset.get("sheet"), f"{asset_id}: authored sheet")
        sheet_hash = _verify_hash(
            sheet_path, asset.get("sheet_sha256"),
            f"{asset_id}: authored sheet")
        try:
            sheet = Image.open(sheet_path).convert("RGBA")
            sheet.load()
        except (OSError, ValueError) as exc:
            raise ReviewInputError(
                f"{asset_id}: cannot decode authored sheet") from exc
        grid = _integer_pair(asset.get("grid"), f"{asset_id}: grid")
        frame_count = int(asset.get(
            "authored_frame_count", asset.get("frame_count", 0)))
        if frame_count < 4 or frame_count > 12:
            raise ReviewInputError(f"{asset_id}: authored frame count is invalid")
        center_offset = _numeric_pair(
            asset.get("runtime_center_offset"),
            f"{asset_id}: runtime_center_offset")
        try:
            runtime_scale = float(asset.get("runtime_scale", 1.0))
        except (TypeError, ValueError) as exc:
            raise ReviewInputError(f"{asset_id}: runtime scale is invalid") from exc
        placed_frames = frame_qa.place_atlas_frames(
            sheet,
            grid,
            frame_count,
            LOGICAL_ROOM_SIZE,
            rect,
            center_offset,
            runtime_scale,
            frame_qa.DEFAULT_ALPHA_SCISSOR_THRESHOLD,
        )
        # Keep the historical approved room only as a contamination reference
        # for exact duplicate-pixel detection.  The depth-aware compositor
        # below renders from the generated full-frame runtime background and
        # therefore cannot resurrect the reference plate's retired objects.
        results = frame_qa.compute_asset_frame_qa(
            approved_rooms[room],
            runtime_underlays[room],
            ownership_full,
            placed_frames,
            healing_mask=frame_qa.binary_mask(
                ownership_full, frame_qa.DEFAULT_OWNERSHIP_THRESHOLD),
        )
        asset_z, asset_z_source = asset_depths[asset_id]
        results = [
            replace_result_composite(
                result,
                compose_depth_aware_frame(
                    approved_rooms[room],
                    runtime_underlays[room],
                    ownership_full,
                    placed_frames[index],
                    cards_by_room[room],
                    asset_z,
                ),
            )
            for index, result in enumerate(results)
        ]
        frame_records: list[dict[str, Any]] = []
        occlusion_masks_by_frame: list[list[Image.Image]] = []
        asset_findings: list[str] = []
        for result in results:
            occlusions, occlusion_masks = measure_frame_occlusions(
                result.primary_alpha_mask, cards_by_room[room], asset_z)
            qa_dict = result.record.to_dict()
            approval_payload = _frame_approval_payload(qa_dict, occlusions)
            frame_record = {
                "frame_index": result.record.frame_index,
                "qa": qa_dict,
                "static_occlusions": occlusions,
                "primary_coverage_includes_secondary_effects": False,
                "frame_review_sha256": sha256_bytes(
                    canonical_json_bytes(approval_payload)),
            }
            frame_records.append(frame_record)
            occlusion_masks_by_frame.append(occlusion_masks)
            asset_findings.extend(nonwaivable_frame_issues(
                asset_id, result, occlusions))
        frame_total += len(frame_records)
        blocking_findings.extend(asset_findings)
        asset_record: dict[str, Any] = {
            "id": asset_id,
            "room": room,
            "runtime_instance": asset["instances"][0],
            "source_rect": list(rect),
            "runtime_center_offset": list(center_offset),
            "runtime_scale": runtime_scale,
            "asset_z": asset_z,
            "asset_z_source": asset_z_source,
            "sheet": {
                "path": _relative(root, sheet_path),
                "file_sha256": sheet_hash,
                "pixel_sha256": frame_qa.raw_pixel_sha256(sheet),
                "dimensions": list(sheet.size),
                "grid": list(grid),
            },
            "ownership_mask": {
                "path": _relative(root, mask_path),
                "file_sha256": mask_hash,
                "room_pixel_sha256": frame_qa.raw_pixel_sha256(
                    ownership_full),
                "ownership_threshold": frame_qa.DEFAULT_OWNERSHIP_THRESHOLD,
            },
            "primary_coverage_policy": (
                "authored_atlas_frame_alpha_scissor_128_only"),
            "secondary_effect_policy": (
                "water_and_effect_overlays_never_satisfy_primary_coverage"),
            "secondary_water_layer_count": len(asset.get("water_layers", [])),
            "frames": frame_records,
            "required_occlusion_relation": _flatten_occlusion_relations(
                frame_records),
            "blocking_findings": sorted(asset_findings),
        }
        contact = render_contact_sheet(
            asset_record, results, occlusion_masks_by_frame)
        filename = f"{asset_id}_frames.png"
        contact_data = png_bytes(contact)
        contact_sheets[filename] = contact_data
        asset_record["contact_sheet"] = contact_sheet_evidence(
            filename, contact)
        plain_contact = render_contact_sheet(
            asset_record, results, occlusion_masks_by_frame,
            show_diagnostics=False)
        plain_filename = f"{asset_id}_plain_frames.png"
        plain_contact_data = png_bytes(plain_contact)
        contact_sheets[plain_filename] = plain_contact_data
        asset_record["plain_contact_sheet"] = contact_sheet_evidence(
            plain_filename, plain_contact)
        candidate_assets.append(asset_record)

    candidate = seal_candidate({
        "schema_version": CANDIDATE_SCHEMA,
        "asset_count": len(candidate_assets),
        "authored_frame_count": frame_total,
        "policy": {
            "runtime_alpha_scissor_threshold": (
                frame_qa.DEFAULT_ALPHA_SCISSOR_THRESHOLD),
            "ownership_alpha_threshold": frame_qa.DEFAULT_OWNERSHIP_THRESHOLD,
            "static_card_alpha_threshold": STATIC_ALPHA_THRESHOLD,
            "minimum_absolute_static_occlusion_z_delta": (
                MINIMUM_ABSOLUTE_Z_DELTA),
            "secondary_effects_count_as_primary_coverage": False,
            "candidate_hashes_are_not_approvals": True,
        },
        "inputs": {
            "v4_manifest": {
                "path": _relative(root, manifest_path),
                "semantic_sha256": semantic_json_sha256(manifest),
                "hash_kind": "canonical_json_utf8",
            },
            "runtime_layout": {
                "path": _relative(root, runtime_path),
                "semantic_sha256": normalized_text_sha256(runtime_text),
                "hash_kind": "utf8_lf_normalized_text",
            },
            "fixture_runtime": {
                "path": _relative(root, fixture_path),
                "semantic_sha256": normalized_text_sha256(fixture_text),
                "hash_kind": "utf8_lf_normalized_text",
            },
            "rooms": room_evidence,
            "active_static_cards": [
                card.evidence() for card in static_cards],
        },
        "assets": candidate_assets,
        "blocking_findings": sorted(blocking_findings),
    })
    return RepositoryReviewBuild(
        candidate=candidate,
        contact_sheets=contact_sheets,
        blocking_findings=tuple(sorted(blocking_findings)),
    )


def validate_approval_ledger(
        build: RepositoryReviewBuild,
        ledger: Mapping[str, Any] | None,
        ) -> list[str]:
    """Validate exact reviewed hashes and explicit per-asset occlusion records."""
    candidate = build.candidate
    problems = list(build.blocking_findings)
    measured_candidate_hash = candidate_payload_sha256(candidate)
    if candidate.get("candidate_payload_sha256") != measured_candidate_hash:
        problems.append("candidate payload hash is internally stale")
    if ledger is None:
        problems.append(
            "missing approval ledger: candidate hashes remain unreviewed and "
            "cannot pass the blocking gate")
        return sorted(set(problems))
    if ledger.get("schema_version") != APPROVAL_SCHEMA:
        problems.append(f"approval ledger schema_version must be {APPROVAL_SCHEMA}")
    if ledger.get("candidate_payload_sha256") != measured_candidate_hash:
        problems.append("approval ledger candidate_payload_sha256 is missing or stale")
    manifest_hash = candidate["inputs"]["v4_manifest"]["semantic_sha256"]
    if ledger.get("manifest_semantic_sha256") != manifest_hash:
        problems.append(
            "approval ledger manifest_semantic_sha256 is missing or stale")
    reviewer = ledger.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip():
        problems.append("approval ledger reviewer must be a non-empty string")

    approvals = ledger.get("assets")
    if not isinstance(approvals, dict):
        problems.append("approval ledger assets must be an object")
        return sorted(set(problems))
    expected_ids = {str(asset["id"]) for asset in candidate["assets"]}
    if set(approvals) != expected_ids:
        problems.append(
            "approval ledger asset ids differ from candidate: "
            f"expected={sorted(expected_ids)}, found={sorted(approvals)}")
    for asset in candidate["assets"]:
        asset_id = str(asset["id"])
        approval = approvals.get(asset_id)
        if not isinstance(approval, dict):
            problems.append(f"{asset_id}: missing per-asset approval record")
            continue
        expected_frames = {
            str(frame["frame_index"]): frame["frame_review_sha256"]
            for frame in asset["frames"]
        }
        approved_frames = approval.get("frame_review_sha256")
        if approved_frames != expected_frames:
            problems.append(f"{asset_id}: exact per-frame review hashes are stale")
        expected_relations = asset["required_occlusion_relation"]
        approved_relations = approval.get("occlusion_relation")
        if approved_relations != expected_relations:
            problems.append(
                f"{asset_id}: occlusion_relation must exactly enumerate every "
                "active static-card overlap")
    return sorted(set(problems))


def write_review_outputs(
        root: Path,
        output_dir: Path,
        build: RepositoryReviewBuild,
        ) -> Path:
    """Write candidate evidence only below the ignored repository audit root."""
    root = root.resolve()
    resolved = output_dir.resolve() if output_dir.is_absolute() \
        else (root / output_dir).resolve()
    audit_root = (root / "audit").resolve()
    try:
        resolved.relative_to(audit_root)
    except ValueError as exc:
        raise ReviewInputError(
            f"review output must stay below ignored {audit_root}") from exc
    resolved.mkdir(parents=True, exist_ok=True)
    for filename, data in sorted(build.contact_sheets.items()):
        (resolved / filename).write_bytes(data)
    candidate_path = resolved / CANDIDATE_FILENAME
    candidate_path.write_text(
        json.dumps(build.candidate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return candidate_path


def _resolve_repository_argument(root: Path, value: Path) -> Path:
    path = value.resolve() if value.is_absolute() else (root / value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ReviewInputError(f"path escapes repository: {value}") from exc
    return path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser(
        "generate", help="write unapproved candidate JSON and contact sheets")
    generate.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_RELATIVE)
    check = subparsers.add_parser(
        "check", help="regenerate candidate and enforce reviewed approvals")
    check.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_RELATIVE)
    check.add_argument(
        "--approval-ledger", type=Path, default=DEFAULT_APPROVAL_RELATIVE)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        build = build_repository_candidate(root)
        candidate_path = write_review_outputs(root, args.output_dir, build)
        relative_candidate = _relative(root, candidate_path)
        print(
            "CASTLE_INTERACTION_FRAME_REVIEW|CANDIDATE|"
            f"path={relative_candidate}|sha256="
            f"{build.candidate['candidate_payload_sha256']}")
        if args.command == "generate":
            for finding in build.blocking_findings:
                print(f"CASTLE_INTERACTION_FRAME_REVIEW|FINDING|{finding}")
            print(
                "CASTLE_INTERACTION_FRAME_REVIEW|RESULT=CANDIDATE|"
                f"assets={build.candidate['asset_count']}|"
                f"frames={build.candidate['authored_frame_count']}|"
                f"blocking_findings={len(build.blocking_findings)}|"
                "approved=false")
            return 0

        ledger_path = _resolve_repository_argument(root, args.approval_ledger)
        ledger = _load_json(ledger_path, "approval ledger") \
            if ledger_path.is_file() else None
        problems = validate_approval_ledger(build, ledger)
        if problems:
            for problem in problems:
                print(f"CASTLE_INTERACTION_FRAME_REVIEW|FAIL|{problem}")
            print(
                "CASTLE_INTERACTION_FRAME_REVIEW|RESULT=FAIL|"
                f"issues={len(problems)}")
            return 1
        print(
            "CASTLE_INTERACTION_FRAME_REVIEW|RESULT=OK|"
            f"assets={build.candidate['asset_count']}|"
            f"frames={build.candidate['authored_frame_count']}|"
            f"reviewer={ledger['reviewer']}")
        return 0
    except (ReviewInputError, OSError, ValueError, TypeError) as exc:
        print(f"CASTLE_INTERACTION_FRAME_REVIEW|FAIL|{exc}")
        print("CASTLE_INTERACTION_FRAME_REVIEW|RESULT=FAIL|issues=1")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
