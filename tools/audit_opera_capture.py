#!/usr/bin/env python3
"""Fail-closed validator for the two-aspect Opera route capture bundle.

The Godot harness writes one manifest beneath each required aspect directory.
This validator independently owns the expected state matrix, source closure,
file set, hashes, dimensions, and semantic state contracts.  These artifacts
are machine-review evidence only; they do not represent device, child, owner,
or visual acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

try:
	import audit_godot_baseline as godot_baseline
except ModuleNotFoundError:  # imported as tools.audit_opera_capture in tests
	from tools import audit_godot_baseline as godot_baseline


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = godot_baseline.BASELINE_PATH
SCHEMA = "reef.opera.route_capture.v1"
MANIFEST_NAME = "opera_capture_manifest.json"
ROUTE_ENTRY_METHOD = "guarded_castle_career_route_launch"
ASPECTS: dict[str, tuple[int, int]] = {
    "1280x720": (1280, 720),
    "1600x720": (1600, 720),
}

NON_HALL_ROUTES: tuple[tuple[str, tuple[int, ...]], ...] = (
    ("kitchen", (0, 3)),
    ("library", (1,)),
    ("craft_room", (10,)),
    ("playroom", (5, 7)),
    ("bubble_bath", (15,)),
    ("mermaid_pool", (11,)),
    ("dining_room", (6,)),
    ("movie_lounge", (12,)),
)
VENUE_FLOORS: tuple[tuple[int, int, str], ...] = (
    (0, 2, "ballerina"),
    (1, 8, "magician"),
    (2, 13, "popstar"),
)
CAREERS: tuple[tuple[int, str, str, str], ...] = (
    (0, "chef", "pastry_chef", "kitchen"),
    (1, "detective", "detective", "library"),
    (2, "ballerina", "ballerina", "opera_hall"),
    (3, "candymaker", "candy_maker", "kitchen"),
    (5, "doctor", "stuffie_surgeon", "playroom"),
    (6, "farmer", "farmer", "dining_room"),
    (7, "boxer", "boxer", "playroom"),
    (8, "magician", "magician", "opera_hall"),
    (10, "painter", "painter", "craft_room"),
    (11, "astronaut", "astronaut_engineer", "mermaid_pool"),
    (12, "racer", "racecar_driver", "movie_lounge"),
    (13, "popstar", "pop_star", "opera_hall"),
    (15, "nursery", "nursery_nurse", "bubble_bath"),
)

# Capture freshness covers every project script, scene/resource descriptor,
# source pixel, and shader that can transitively affect these rendered frames.
# Keep these rules byte-for-byte equivalent to scripts/probe_opera_art.gd.
SOURCE_FIXED_FILES: tuple[str, ...] = (
    "project.godot",
    "tools/audit_opera_capture.py",
)
SOURCE_TREE_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("assets", (
        ".bmp", ".dds", ".exr", ".gdshader", ".hdr", ".import", ".jpeg",
        ".jpg", ".json", ".ktx", ".mp3", ".ogg", ".png", ".svg", ".tga",
        ".uid", ".wav", ".webp",
    )),
    ("scenes", (".res", ".tres", ".tscn", ".uid")),
    ("scripts", (".gd", ".uid")),
    ("shaders", (".gdshader", ".uid")),
)

MANIFEST_KEYS = frozenset({
    "schema", "run_nonce", "source_revision", "aspect_id", "viewport",
    "capture_method", "rendering_method", "engine", "source_signature",
    "expected_state_ids", "states", "global_failures", "summary", "result",
})
ENGINE_KEYS = frozenset({
    "major", "minor", "patch", "status", "build", "version_string",
})


def capture_engine_evidence(path: Path = BASELINE_PATH) -> dict[str, Any]:
    """Return the parsed baseline and its canonical capture identity."""
    baseline = godot_baseline.load_baseline(path)
    return {
        "baseline": baseline,
        "canonical": godot_baseline.canonical_engine_contract(baseline),
    }


STATE_ROW_KEYS = frozenset({
    "id", "sequence", "kind", "expected_state", "actual_state",
    "state_signature", "input", "status", "failures", "image",
})
IMAGE_KEYS = frozenset({"file", "width", "height", "bytes", "sha256"})


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def canonical_signature(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True,
    ).encode("utf-8")
    return sha256_bytes(encoded)


def strict_equal(actual: Any, expected: Any) -> bool:
    """Recursively compare JSON-shaped values without Python's bool/int aliasing."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            strict_equal(actual[key], expected[key]) for key in expected
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            strict_equal(actual_value, expected_value)
            for actual_value, expected_value in zip(actual, expected)
        )
    return actual == expected


def _mask_non_newlines(value: str) -> str:
    return "".join("\n" if character == "\n" else " " for character in value)


def _gdscript_lexical_views(source: str) -> tuple[str, str]:
    """Return comment-free and executable-only, position-preserving views."""
    comment_free: list[str] = []
    executable: list[str] = []
    index = 0
    while index < len(source):
        character = source[index]
        if character == "#":
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            segment = source[index:end]
            masked = _mask_non_newlines(segment)
            comment_free.append(masked)
            executable.append(masked)
            index = end
            continue
        if character in ("'", '"'):
            delimiter = character * 3 \
                if source.startswith(character * 3, index) else character
            end = index + len(delimiter)
            while end < len(source):
                if source[end] == "\\":
                    end = min(len(source), end + 2)
                    continue
                if source.startswith(delimiter, end):
                    end += len(delimiter)
                    break
                end += 1
            segment = source[index:end]
            comment_free.append(segment)
            executable.append(_mask_non_newlines(segment))
            index = end
            continue
        comment_free.append(character)
        executable.append(character)
        index += 1
    return "".join(comment_free), "".join(executable)


def _has_emit_signal(executable: str) -> bool:
    return re.search(r"\bemit_signal\s*\(", executable) is not None


def collect_source_paths(
    source_root: Path,
) -> tuple[list[str], list[str], list[dict[str, Any]]]:
    paths = set(SOURCE_FIXED_FILES)
    missing: list[str] = []
    tree_rules: list[dict[str, Any]] = []
    for relative_root, suffixes in SOURCE_TREE_RULES:
        tree_rules.append({"root": relative_root, "suffixes": list(suffixes)})
        tree_root = source_root / relative_root
        if not tree_root.is_dir():
            missing.append(f"{relative_root}/")
            continue
        for path in tree_root.rglob("*"):
            if path.is_file() and any(
                path.name.lower().endswith(suffix) for suffix in suffixes
            ):
                paths.add(path.relative_to(source_root).as_posix())
    return sorted(paths), sorted(missing), tree_rules


def compute_source_signature(source_root: Path) -> dict[str, Any]:
    source_paths, missing, tree_rules = collect_source_paths(source_root)
    files: dict[str, str] = {}
    for relative in source_paths:
        path = source_root / relative
        if not path.is_file():
            missing.append(relative)
            continue
        files[relative] = sha256_file(path)
    missing.sort()
    entries = [f"{relative}:{files.get(relative, '')}" for relative in source_paths]
    return {
        "algorithm": "sha256_opera_capture_source_closure_v2",
        "tree_rules": tree_rules,
        "paths": source_paths,
        "files": files,
        "missing": missing,
        "sha256": sha256_bytes("\n".join(entries).encode("utf-8")),
    }


def probe_contract_errors(source_root: Path) -> list[str]:
    path = source_root / "scripts/probe_opera_art.gd"
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"probe_source: {exc}"]
    comment_free, executable = _gdscript_lexical_views(source)
    required = (
        "await _wait_career_ready(index, room_id)",
        "await _wait_capture_frame_post_draw()",
        "button.is_visible_in_tree()",
        "Vector2i(1280, 720)",
        "Vector2i(1600, 720)",
    )
    errors = [
        f"probe_contract: missing {token}"
        for token in required if token not in executable
    ]
    if re.search(
        r"\broutes\s*\.\s*_launch\s*\(\s*room_id\s*,\s*index\s*\)",
        executable,
    ) is None:
        errors.append("probe_contract: missing routes._launch(room_id, index)")
    if re.search(r"\.\s*pressed\s*\.\s*emit\s*\(", executable):
        errors.append("probe_contract: direct pressed.emit route is forbidden")
    if _has_emit_signal(executable):
        errors.append("probe_contract: emit_signal routes are forbidden")
    direct_main_route = re.search(
        r"\bmain\s*\.\s*_start_opera_from_room\s*\(", executable,
    ) is not None
    reflected_main_route = re.search(
        r"\bmain\s*\.\s*callv?\s*\(\s*(?:&\s*)?"
        r"[\"']_start_opera_from_room[\"']",
        comment_free,
    ) is not None or re.search(
        r"\bCallable\s*\(\s*main\s*,\s*(?:&\s*)?"
        r"[\"']_start_opera_from_room[\"']",
        comment_free,
    ) is not None
    if direct_main_route or reflected_main_route:
        errors.append("probe_contract: direct main route bypass is forbidden")
    if re.search(
        r"\bawait\s+RenderingServer\s*\.\s*frame_post_draw\b", executable,
    ):
        errors.append("probe_contract: unbounded frame_post_draw await is forbidden")
    return errors


def _route_expected(room_id: str, acts: tuple[int, ...]) -> dict[str, Any]:
    return {
        "game": "level2",
        "phase": "hall",
        "room_id": room_id,
        "stage_id": f"castle.room.{room_id}",
        "route_visible": True,
        "act_indices": list(acts),
        "castle_layer": 14,
        "living_layer": 15,
        "pause_layer": 16,
        "opera_active": False,
        "venue_open": False,
        "start_menu_visible": False,
    }


def _venue_expected(floor: int, act_index: int) -> dict[str, Any]:
    return {
        "game": "level2",
        "phase": "hall",
        "room_id": "opera_hall",
        "stage_id": "castle.room.opera_hall",
        "venue_open": True,
        "accepting_input": True,
        "floor_index": floor,
        "floor_act_index": act_index,
        "guide_act_index": act_index,
        "enabled_act_indices": [act_index],
        "castle_layer": 14,
        "living_layer": 15,
        "pause_layer": 16,
        "opera_active": False,
        "start_menu_visible": False,
    }


def _career_expected(
    act_index: int, career_id: str, room_id: str,
) -> dict[str, Any]:
    return {
        "game": "opera",
        "act_index": act_index,
        "career_id": career_id,
        "room_id": room_id,
        "return_room": room_id,
        "stage_id": f"opera.act.{act_index:02d}",
        "act_state": "play",
        "career_world_present": True,
        "career_world_visible": True,
        "career_world_layer": 10,
        "living_layer": 11,
        "hud_layer": 12,
        "pause_layer": 13,
        "castle_layer_visible": False,
        "player_visible": False,
        "entry_method": ROUTE_ENTRY_METHOD,
        "start_menu_visible": False,
    }


def expected_states() -> list[dict[str, Any]]:
    states: list[dict[str, Any]] = []
    for room_id, acts in NON_HALL_ROUTES:
        states.append({
            "id": f"castle_career_routes_{room_id}",
            "kind": "castle_route",
            "expected_state": _route_expected(room_id, acts),
        })
    for floor, act_index, career_id in VENUE_FLOORS:
        states.append({
            "id": f"opera_venue_floor_{floor + 1:02d}_{career_id}",
            "kind": "opera_venue_floor",
            "expected_state": _venue_expected(floor, act_index),
        })
    for act_index, career_id, slug, room_id in CAREERS:
        states.append({
            "id": f"opera_act_{act_index + 1:02d}_{slug}_from_{room_id}",
            "kind": "career_entry",
            "expected_state": _career_expected(act_index, career_id, room_id),
        })
    for sequence, state in enumerate(states):
        state["sequence"] = sequence
    assert len(states) == 24
    return states


def _add(errors: list[str], code: str, detail: str) -> None:
    errors.append(f"{code}: {detail}")


def _load_json(
    path: Path, errors: list[str], aspect: str,
) -> dict[str, Any] | None:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key!r}")
            value[key] = item
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        _add(errors, "manifest_read", f"{aspect}: {exc}")
        return None
    if not isinstance(value, dict):
        _add(errors, "manifest_type", f"{aspect}: root must be an object")
        return None
    return value


def _check_image(
    path: Path,
    row: dict[str, Any],
    dimensions: tuple[int, int],
    errors: list[str],
    aspect: str,
    state_id: str,
) -> str:
    image_meta = row.get("image")
    if type(image_meta) is not dict:
        _add(errors, "image_metadata", f"{aspect}/{state_id}: missing object")
        return ""
    if set(image_meta) != IMAGE_KEYS:
        _add(errors, "image_metadata", (
            f"{aspect}/{state_id}: keys must be {sorted(IMAGE_KEYS)}"
        ))
    expected_file = f"{state_id}.png"
    if not strict_equal(image_meta.get("file"), expected_file):
        _add(errors, "image_name", f"{aspect}/{state_id}: expected {expected_file}")
    if not strict_equal(image_meta.get("width"), dimensions[0]) \
            or not strict_equal(image_meta.get("height"), dimensions[1]):
        _add(errors, "image_dimensions", f"{aspect}/{state_id}: manifest mismatch")
    if not path.is_file():
        _add(errors, "image_missing", f"{aspect}/{expected_file}")
        return ""
    actual_bytes = path.stat().st_size
    actual_hash = sha256_file(path)
    if not strict_equal(image_meta.get("bytes"), actual_bytes):
        _add(errors, "image_bytes", f"{aspect}/{state_id}: byte count drift")
    if not strict_equal(image_meta.get("sha256"), actual_hash):
        _add(errors, "image_hash", f"{aspect}/{state_id}: SHA-256 drift")
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG":
                _add(errors, "image_format", f"{aspect}/{state_id}: not PNG")
            if image.size != dimensions:
                _add(errors, "image_dimensions", (
                    f"{aspect}/{state_id}: decoded {image.size}, expected {dimensions}"
                ))
            sample = image.convert("RGBA").resize((32, 18))
            pixels = sample.load()
            visible_colours = [
                (pixel[0], pixel[1], pixel[2])
                for y in range(sample.height)
                for x in range(sample.width)
                if (pixel := pixels[x, y])[3] >= 8
            ]
            if len(visible_colours) < 6:
                _add(errors, "image_transparent", (
                    f"{aspect}/{state_id}: insufficient visible coverage"
                ))
            elif len(set(visible_colours)) < 2:
                _add(errors, "image_blank", f"{aspect}/{state_id}: no visual variation")
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        _add(errors, "image_decode", f"{aspect}/{state_id}: {exc}")
    return actual_hash


def _check_career_entry(
    value: Any,
    expected_state: dict[str, Any],
    errors: list[str],
    aspect: str,
    state_id: str,
) -> None:
    prefix = f"{aspect}/{state_id}"
    exact_keys = {"method", "room_id", "act_index", "control_path"}
    if not isinstance(value, dict):
        _add(errors, "input_evidence", f"{prefix}: missing object")
        return
    if set(value) != exact_keys:
        _add(errors, "input_evidence", f"{prefix}: keys must be {sorted(exact_keys)}")
    if value.get("method") != ROUTE_ENTRY_METHOD:
        _add(errors, "input_evidence", f"{prefix}: wrong guarded-route method")
    if not strict_equal(value.get("room_id"), expected_state.get("return_room")):
        _add(errors, "input_evidence", f"{prefix}: wrong route room")
    if not strict_equal(value.get("act_index"), expected_state.get("act_index")):
        _add(errors, "input_evidence", f"{prefix}: wrong route act")
    control_path = value.get("control_path")
    if not isinstance(control_path, str) or not control_path.startswith("/root/"):
        _add(errors, "input_evidence", f"{prefix}: invalid control path")


def _validate_aspect(
    capture_root: Path,
    source_signature: dict[str, Any],
    aspect: str,
    dimensions: tuple[int, int],
    engine_evidence: dict[str, Any],
) -> tuple[list[str], str]:
    errors: list[str] = []
    aspect_dir = capture_root / aspect
    if not aspect_dir.is_dir():
        _add(errors, "aspect_missing", aspect)
        return errors, ""
    manifest_path = aspect_dir / MANIFEST_NAME
    manifest = _load_json(manifest_path, errors, aspect)
    if manifest is None:
        return errors, ""
    if set(manifest) != MANIFEST_KEYS:
        _add(errors, "manifest_keys", (
            f"{aspect}: keys must be {sorted(MANIFEST_KEYS)}"
        ))

    expected = expected_states()
    expected_ids = [state["id"] for state in expected]
    expected_files = {MANIFEST_NAME, *(f"{state_id}.png" for state_id in expected_ids)}
    actual_files = {path.name for path in aspect_dir.iterdir() if path.is_file()}
    actual_dirs = sorted(path.name for path in aspect_dir.iterdir() if path.is_dir())
    if actual_dirs:
        _add(errors, "aspect_extra_directory", f"{aspect}: {actual_dirs}")
    missing_files = sorted(expected_files - actual_files)
    extra_files = sorted(actual_files - expected_files)
    if missing_files:
        _add(errors, "file_set_missing", f"{aspect}: {missing_files}")
    if extra_files:
        _add(errors, "file_set_extra", f"{aspect}: {extra_files}")

    if not strict_equal(manifest.get("schema"), SCHEMA):
        _add(errors, "schema", f"{aspect}: {manifest.get('schema')!r}")
    if not strict_equal(manifest.get("aspect_id"), aspect):
        _add(errors, "aspect_id", f"{aspect}: {manifest.get('aspect_id')!r}")
    wanted_viewport = {"width": dimensions[0], "height": dimensions[1]}
    if not strict_equal(manifest.get("viewport"), wanted_viewport):
        _add(errors, "viewport", f"{aspect}: wrong viewport contract")
    if not strict_equal(manifest.get("capture_method"), "same_process_viewport"):
        _add(errors, "capture_method", f"{aspect}: not same-process")
    if not strict_equal(manifest.get("rendering_method"), "mobile"):
        _add(errors, "renderer", f"{aspect}: {manifest.get('rendering_method')!r}")
    engine = manifest.get("engine")
    version_string = engine.get("version_string") \
        if type(engine) is dict else None
    wanted_engine = engine_evidence["canonical"]
    exact_engine = strict_equal(engine, wanted_engine) \
        and set(engine) == ENGINE_KEYS
    if not exact_engine:
        _add(errors, "engine", (
            f"{aspect}: exact official Godot {wanted_engine['version_string']} required"
        ))
    if not strict_equal(manifest.get("source_signature"), source_signature):
        _add(errors, "source_signature", f"{aspect}: source closure drift")
    if not strict_equal(manifest.get("expected_state_ids"), expected_ids):
        _add(errors, "expected_state_ids", f"{aspect}: matrix drift")
    run_nonce = manifest.get("run_nonce")
    if type(run_nonce) is not str or not run_nonce.strip():
        _add(errors, "run_nonce", f"{aspect}: missing")
        run_nonce = ""
    source_revision = manifest.get("source_revision")
    if type(source_revision) is not str or not source_revision.strip():
        _add(errors, "source_revision", f"{aspect}: missing")

    rows = manifest.get("states")
    if type(rows) is not list:
        _add(errors, "states", f"{aspect}: states must be an array")
        rows = []
    row_ids = [row.get("id") if type(row) is dict else None for row in rows]
    if len(rows) != len(expected):
        _add(errors, "state_count", f"{aspect}: {len(rows)} != {len(expected)}")
    has_duplicate = any(
        any(strict_equal(row_id, previous) for previous in row_ids[:index])
        for index, row_id in enumerate(row_ids)
    )
    if has_duplicate:
        _add(errors, "state_duplicate", f"{aspect}: duplicate state ID")
    if not strict_equal(row_ids, expected_ids):
        _add(errors, "state_order", f"{aspect}: state IDs/order drift")

    image_hash_states: dict[str, list[str]] = {}
    for index, expected_row in enumerate(expected):
        if index >= len(rows) or type(rows[index]) is not dict:
            continue
        row = rows[index]
        state_id = expected_row["id"]
        if set(row) != STATE_ROW_KEYS:
            _add(errors, "state_keys", (
                f"{aspect}/{state_id}: keys must be {sorted(STATE_ROW_KEYS)}"
            ))
        if not strict_equal(row.get("id"), state_id):
            _add(errors, "state_id", f"{aspect}/{state_id}: wrong ID")
        if not strict_equal(row.get("sequence"), index):
            _add(errors, "state_sequence", f"{aspect}/{state_id}: wrong sequence")
        if not strict_equal(row.get("kind"), expected_row["kind"]):
            _add(errors, "state_kind", f"{aspect}/{state_id}: wrong kind")
        if not strict_equal(row.get("expected_state"), expected_row["expected_state"]):
            _add(errors, "expected_state", f"{aspect}/{state_id}: contract drift")
        actual_state = row.get("actual_state")
        if type(actual_state) is not dict:
            _add(errors, "actual_state", f"{aspect}/{state_id}: missing object")
            actual_state = {}
        if not strict_equal(actual_state, expected_row["expected_state"]):
            _add(errors, "actual_state", f"{aspect}/{state_id}: contract drift")
        if not strict_equal(
            row.get("state_signature"), canonical_signature(actual_state),
        ):
            _add(errors, "state_signature", f"{aspect}/{state_id}: drift")
        if not strict_equal(row.get("status"), "PASS"):
            _add(errors, "state_status", f"{aspect}/{state_id}: not PASS")
        if not strict_equal(row.get("failures"), []):
            _add(errors, "state_failures", f"{aspect}/{state_id}: not empty")
        if expected_row["kind"] == "career_entry":
            _check_career_entry(
                row.get("input"), expected_row["expected_state"], errors,
                aspect, state_id,
            )
        elif not strict_equal(row.get("input"), {}):
            _add(errors, "input_evidence", f"{aspect}/{state_id}: must be empty")
        image_hash = _check_image(
            aspect_dir / f"{state_id}.png", row, dimensions, errors, aspect, state_id,
        )
        if image_hash:
            image_hash_states.setdefault(image_hash, []).append(state_id)

    for image_hash, state_ids in image_hash_states.items():
        if len(state_ids) > 1:
            _add(errors, "image_duplicate", (
                f"{aspect}: SHA-256 {image_hash} reused by {state_ids}"
            ))

    summary = manifest.get("summary")
    wanted_summary = {
        "expected": 24,
        "rows": 24,
        "written": 24,
        "passed": 24,
        "failed": 0,
    }
    if not strict_equal(summary, wanted_summary):
        _add(errors, "summary", f"{aspect}: {summary!r}")
    if not strict_equal(manifest.get("global_failures"), []):
        _add(errors, "global_failures", f"{aspect}: not empty")
    if not strict_equal(manifest.get("result"), "PASS"):
        _add(errors, "result", f"{aspect}: {manifest.get('result')!r}")
    return errors, str(run_nonce)


def validate_capture_root(
    capture_root: Path,
    source_root: Path = ROOT,
    baseline_path: Path = BASELINE_PATH,
) -> list[str]:
    errors: list[str] = []
    if not capture_root.is_dir():
        return [f"capture_root: missing directory {capture_root}"]
    try:
        engine_evidence = capture_engine_evidence(baseline_path)
    except godot_baseline.BaselineError as error:
        return [f"baseline: {error}"]
    root_entries = {path.name for path in capture_root.iterdir()}
    expected_entries = set(ASPECTS)
    missing = sorted(expected_entries - root_entries)
    extra = sorted(root_entries - expected_entries)
    if missing:
        _add(errors, "root_missing", str(missing))
    if extra:
        _add(errors, "root_extra", str(extra))

    source_signature = compute_source_signature(source_root)
    if source_signature["missing"]:
        _add(errors, "source_missing", str(source_signature["missing"]))
    errors.extend(probe_contract_errors(source_root))
    nonces: list[str] = []
    for aspect, dimensions in ASPECTS.items():
        aspect_errors, nonce = _validate_aspect(
            capture_root, source_signature, aspect, dimensions, engine_evidence,
        )
        errors.extend(aspect_errors)
        if nonce:
            nonces.append(nonce)
    if len(nonces) == len(ASPECTS) and len(set(nonces)) != 1:
        _add(errors, "stale_mixed_run", "aspect manifests have different run_nonce values")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_root", type=Path)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_capture_root(args.capture_root.resolve(), args.source_root.resolve())
    if errors:
        for error in errors:
            print(f"OPERA_CAPTURE_AUDIT|FAIL|{error}")
        print(f"OPERA_CAPTURE_AUDIT|RESULT|FAIL|count={len(errors)}")
        return 1
    print("OPERA_CAPTURE_AUDIT|RESULT|PASS|aspects=2|states=48")
    return 0


if __name__ == "__main__":
    sys.exit(main())
