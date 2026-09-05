"""Fail-closed audit for Day One's exact Roshan contextual voice slate.

The catalog is intentionally independent of generation tooling.  A row is a
promise that a gameplay moment has its own semantic cue, not permission to
fall back to ``talk``, ``win`` or ``yay``.  During implementation missing rows
are explicit ``PENDING_GENERATION``; delivery mode rejects those rows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_REL = Path("audit/DAY_ONE_CONTEXTUAL_VOICE_COVERAGE_2026-09-01.json")
DEFAULT_RUNTIME_CATALOG_REL = Path("scripts/day_one_contextual_voice_catalog.gd")
GENERIC_TOKENS = {
    "talk",
    "win",
    "yay",
    "roshan",
    "voice_yay",
}
REQUIRED_ROUTES = {"arrival", "bathroom", "kitchen", "pool", "stuffie", "art", "boss", "finale"}
VALID_STATUSES = {"READY", "PENDING_GENERATION"}
VALID_POLICIES = {"once_per_session", "once_per_room_visit", "repeat_variant"}

# These are the runtime files whose exact Roshan calls are governed by the
# catalog.  Keeping the list explicit makes omissions reviewable and prevents
# a newly-added room from silently falling back to a generic voice.
GOVERNED_CALLSITE_FILES = (
    Path("scripts/arena/castle_rooms_25d.gd"),
    Path("scripts/day_one_art_studio.gd"),
    Path("scripts/games/day_one_bathroom_cleanup.gd"),
    Path("scripts/games/day_one_bathroom_cleaning.gd"),
    Path("scripts/games/day_one_pool_cleanup.gd"),
    Path("scripts/games/dust_boss.gd"),
)

# Dynamic families cannot be recovered from a literal call expression (the
# key/caption is selected from a gameplay state).  Their rows and source
# anchors are therefore enumerated here and audited as a set.
DYNAMIC_CALLSITE_FAMILIES: tuple[dict[str, Any], ...] = (
    {
        "family_id": "castle_room_entry",
        "source": Path("scripts/arena/castle_rooms_25d.gd"),
        "anchors": ("_room_entry_context_key", "_room_entry_context_caption"),
        "rows": {
            "day1_bathroom_enter": "Bubbles on my nose! Hee hee!",
            "day1_fridge_menu": "What shall we cook in the royal kitchen?",
            "day1_stuffie_enter": "A playroom! I want to see every toy!",
            "day1_art_enter": "Paint and sparkles! Let's make castle art!",
            "day1_pool_enter": "The pool is wiggly-blue! Splash time!",
        },
    },
    {
        "family_id": "castle_recipe",
        "source": Path("scripts/arena/castle_rooms_25d.gd"),
        "anchors": ("day1_recipe_pearl_select", "day1_recipe_carrot_select"),
        "rows": {
            "day1_recipe_pearl_select": "Pearl Cake! Let us make it!",
            "day1_recipe_carrot_select": "Carrot Cake! Let us make it!",
            "day1_recipe_pearl_ready": "Our Pearl Cake is ready!",
            "day1_recipe_carrot_ready": "Our Carrot Cake is ready!",
        },
    },
    {
        "family_id": "castle_stuffie_pins",
        "source": Path("scripts/arena/castle_rooms_25d.gd"),
        "anchors": ("pin_key", "day1_stuffie_pin_left_loose", "day1_stuffie_pin_right_loose"),
        "rows": {
            "day1_stuffie_pin_left_loose": "The left pin is loose!",
            "day1_stuffie_pin_right_loose": "The right pin is loose!",
        },
    },
    {
        "family_id": "art_materials",
        "source": Path("scripts/day_one_art_studio.gd"),
        "anchors": ("_material_context_key", "_material_context_caption"),
        "rows": {
            "day1_art_material_brushes_found": "I found the brushes!",
            "day1_art_material_pink_paint_found": "Pink paint! My favorite!",
            "day1_art_material_blue_paint_found": "Blue paint is ready!",
            "day1_art_material_cups_found": "I found the little paint cups!",
            "day1_art_material_brushes_hint": "Tap the loose brushes!",
            "day1_art_material_pink_paint_hint": "Tap the pink paint!",
            "day1_art_material_blue_paint_hint": "Tap the blue paint!",
            "day1_art_material_cups_hint": "Tap the paint cups!",
        },
    },
    {
        "family_id": "art_grime",
        "source": Path("scripts/day_one_art_studio.gd"),
        "anchors": ("_grime_context_key", "_grime_context_caption"),
        "rows": {
            "day1_art_scrub_left_clean": "Scrub this painty counter!",
            "day1_art_scrub_desk_clean": "The desk needs a good scrub!",
            "day1_art_scrub_right_clean": "One more counter to sparkle!",
            "day1_art_scrub_left_hint": "Now scrub the left counter grime!",
            "day1_art_scrub_desk_hint": "Now scrub the desk counter grime!",
            "day1_art_scrub_right_hint": "Now scrub the right counter grime!",
        },
    },
    {
        "family_id": "pool_skimmer",
        "source": Path("scripts/games/day_one_pool_cleanup.gd"),
        "anchors": ("SKIMMER_PICKUP_CAPTIONS", "SKIMMER_CUE_IDS"),
        "rows": {
            "day1_pool_skimmer_01": "One leaf scooped!",
            "day1_pool_skimmer_02": "Another leaf is gone!",
            "day1_pool_skimmer_03": "The water looks clearer!",
            "day1_pool_skimmer_04": "Scoop, scoop!",
            "day1_pool_skimmer_05": "Almost sparkling!",
            "day1_pool_skimmer_06": "The last leaf is out!",
        },
    },
    {
        "family_id": "pool_waterfall",
        "source": Path("scripts/games/day_one_pool_cleanup.gd"),
        "anchors": ("WATERFALL_LANE_CAPTIONS", "WATERFALL_CUE_IDS"),
        "rows": {
            "day1_pool_waterfall_lane_left": "The left waterfall lane is clear!",
            "day1_pool_waterfall_lane_center": "The middle waterfall lane is clear!",
            "day1_pool_waterfall_lane_right": "The right waterfall lane is clear!",
        },
    },
    {
        "family_id": "boss_reminders",
        "source": Path("scripts/games/dust_boss.gd"),
        "anchors": ("day1_boss_reminder_almost", "day1_boss_reminder_closer", "day1_boss_reminder_mercy"),
        "rows": {
            "day1_boss_reminder_almost": "So close! Wait for the next FLASH and tap FAST — three times!",
            "day1_boss_reminder_closer": "He is coming closer now — wait for the BIG GOLD STAR!",
            "day1_boss_reminder_mercy": "Grand Puff slowed down! Take your time — wait for the BIG GOLD STAR!",
        },
    },
)

VIDEO_CUES: dict[str, dict[str, Any]] = {
    "d1_c00_s01_roshan_flight": {"caption": "We're flying through the clouds!", "video_id": "D1-C00"},
    "d1_c00_s02_roshan_view": {"caption": "Daddy, what can you see?", "video_id": "D1-C00"},
    "d1_c00_s03_roshan_discovery": {"caption": "Look, Daddy! The lagoon is sparkling!", "video_id": "D1-C00"},
    "d1_c00_s04_roshan_handhold": {"caption": "Daddy, hold my hand!", "video_id": "D1-C00"},
    "d1_c00_s05_roshan_lagoon_reveal": {"caption": "Wow! Look at the Sky Lagoon!", "video_id": "D1-C00"},
    "d1_c00_s06_roshan_prepare_land": {"caption": "We're ready to land!", "video_id": "D1-C00"},
    "d1_c01_s01_roshan_landed": {"caption": "We landed!", "video_id": "D1-C01"},
    "d1_c01_s02_roshan_handhold": {"caption": "I'm ready, Daddy!", "video_id": "D1-C01"},
    "d1_c01_s03_roshan_walk_castle": {"caption": "Let's walk to the castle!", "video_id": "D1-C01"},
    "d1_c01_s04_roshan_castle_doors": {"caption": "The castle doors are so big!", "video_id": "D1-C01"},
}


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _issue(issues: list[str], message: str) -> None:
    issues.append(message)


def normalize_transcript(value: str) -> str:
    """Normalize only Unicode/case/whitespace/punctuation, never wording."""
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("\u2018", "'").replace("\u2019", "'")
    value = value.casefold()
    value = "".join(" " if unicodedata.category(char).startswith("P") else char
                    for char in value)
    return " ".join(value.split())


def _manifest_text_by_key(root: Path, catalog: dict[str, Any], issues: list[str]) -> dict[str, str]:
    manifest_rel = catalog.get("protected_hash_manifest")
    if not isinstance(manifest_rel, str):
        return {}
    path = root / manifest_rel
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    entries = payload.get("entries")
    if not isinstance(entries, list):
        _issue(issues, "filler manifest has no entries for semantic validation")
        return {}
    result: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key = entry.get("key")
        text = entry.get("text", entry.get("transcript"))
        if isinstance(key, str) and isinstance(text, str):
            result[key] = text
    return result


def load_catalog(root: Path = ROOT) -> dict[str, Any]:
    path = root / CATALOG_REL
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("contextual catalog must be an object")
    return payload


def runtime_catalog_source(catalog: dict[str, Any]) -> str:
    """Render the JSON rows into the export-safe deterministic GDScript source."""
    rows = catalog.get("rows", [])
    lines = [
        "class_name DayOneContextualVoiceCatalog",
        "extends RefCounted",
        "## Generated from the ignored audit catalog; do not hand-edit.",
        "## Runtime authority must remain export-safe under scripts/.",
        "",
        "const SCHEMA_VERSION: int = 1",
        "",
        "const ROWS: Array[Dictionary] = [",
    ]
    for row in rows:
        # Stable key order and compact JSON make regeneration byte-for-byte reproducible.
        encoded = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        # GDScript accepts JSON-style literals for strings/bools/null, and JSON
        # escaping is also valid GDScript escaping for the string values.
        lines.append("\t" + encoded + ",")
    lines.extend([
        "]",
        "",
        "static func rows() -> Array[Dictionary]:",
        "\treturn ROWS.duplicate(true)",
        "",
        "func catalog() -> Dictionary:",
        "\treturn {",
        '\t\t"schema": "day_one_contextual_voice_coverage",',
        '\t\t"schema_version": SCHEMA_VERSION,',
        '\t\t"scope": "day_one",',
        '\t\t"speaker": "roshan",',
        '\t\t"allow_generic": false,',
        f'\t\t"status": {json.dumps(str(catalog.get("status", "IMPLEMENTATION_PENDING")))},',
        '\t\t"rows": rows(),',
        "\t}",
        "",
        "static func row(cue_id: String) -> Dictionary:",
        "\tfor candidate: Dictionary in ROWS:",
        "\t\tif String(candidate.get(\"cue_id\", \"\")) == cue_id:",
        "\t\t\treturn candidate",
        "\treturn {}",
        "",
    ])
    # JSON and GDScript share the same object/array/string/bool syntax here.
    return "\n".join(lines)


def runtime_catalog_path(root: Path, catalog: dict[str, Any]) -> Path:
    rel = catalog.get("runtime_catalog_path", str(DEFAULT_RUNTIME_CATALOG_REL))
    if not isinstance(rel, str) or not rel:
        rel = str(DEFAULT_RUNTIME_CATALOG_REL)
    return root / rel


def validate_runtime_catalog_parity(
    catalog: dict[str, Any], root: Path = ROOT
) -> list[str]:
    expected = runtime_catalog_source(catalog)
    path = runtime_catalog_path(root, catalog)
    if not path.is_file():
        return [f"runtime catalog missing: {path.relative_to(root)}"]
    try:
        actual = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"runtime catalog unreadable: {exc}"]
    if actual != expected:
        return [f"runtime catalog parity drift: {path.relative_to(root)}"]
    return []


def _validate_protected_hashes(root: Path, catalog: dict[str, Any], issues: list[str]) -> None:
    manifest_rel = catalog.get("protected_hash_manifest")
    if not isinstance(manifest_rel, str) or not manifest_rel:
        _issue(issues, "protected_hash_manifest is required")
        return
    manifest_path = root / manifest_rel
    if not manifest_path.is_file():
        _issue(issues, f"protected hash manifest missing: {manifest_rel}")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _issue(issues, f"protected hash manifest unreadable: {exc}")
        return
    hashes = manifest.get("protected_recording_hashes")
    if not isinstance(hashes, dict) or not hashes:
        _issue(issues, "protected hash manifest has no protected_recording_hashes")
        return
    for rel, expected in sorted(hashes.items()):
        path = root / str(rel)
        if not path.is_file():
            _issue(issues, f"protected recording missing: {rel}")
        elif file_sha256(path) != expected:
            _issue(issues, f"protected recording hash drift: {rel}")


def validate_catalog(
    catalog: dict[str, Any],
    root: Path = ROOT,
    *,
    mode: str = "implementation",
) -> list[str]:
    """Return all catalog violations; an empty list is a pass."""
    issues: list[str] = []
    if catalog.get("schema") != "day_one_contextual_voice_coverage":
        _issue(issues, "wrong contextual catalog schema")
    if catalog.get("schema_version") != 1:
        _issue(issues, "unsupported contextual catalog schema_version")
    if catalog.get("scope") != "day_one" or catalog.get("speaker") != "roshan":
        _issue(issues, "catalog scope must be day_one/roshan")
    if catalog.get("allow_generic") is not False:
        _issue(issues, "governed Day One catalog must set allow_generic=false")
    if mode not in {"implementation", "delivery"}:
        _issue(issues, f"unknown mode: {mode}")
    rows = catalog.get("rows")
    if not isinstance(rows, list) or not rows:
        _issue(issues, "catalog rows must be a non-empty list")
        _validate_protected_hashes(root, catalog, issues)
        return issues

    cue_ids: set[str] = set()
    paths: dict[str, list[dict[str, Any]]] = {}
    routes: set[str] = set()
    manifest_text = _manifest_text_by_key(root, catalog, issues)
    for index, row in enumerate(rows):
        prefix = f"row {index}"
        if not isinstance(row, dict):
            _issue(issues, f"{prefix} is not an object")
            continue
        cue_id = row.get("cue_id")
        if not isinstance(cue_id, str) or not re.fullmatch(r"[a-z0-9_]+", cue_id):
            _issue(issues, f"{prefix} has invalid cue_id")
        elif cue_id in cue_ids:
            _issue(issues, f"duplicate cue_id: {cue_id}")
        else:
            cue_ids.add(cue_id)
        route = row.get("route")
        if route not in REQUIRED_ROUTES:
            _issue(issues, f"{prefix} has unsupported route: {route!r}")
        elif isinstance(route, str):
            routes.add(route)
        for required in ("moment", "caption", "audio_path", "status", "policy", "video_reuse"):
            if required not in row:
                _issue(issues, f"{prefix} missing {required}")
        status = row.get("status")
        if status not in VALID_STATUSES:
            _issue(issues, f"{prefix} has invalid status: {status!r}")
        elif mode == "delivery" and status == "PENDING_GENERATION":
            _issue(issues, f"pending generation in delivery mode: {cue_id}")
        policy = row.get("policy")
        if policy not in VALID_POLICIES:
            _issue(issues, f"{prefix} has invalid replay policy: {policy!r}")
        audio_path = row.get("audio_path")
        if not isinstance(audio_path, str) or not audio_path.startswith("assets/audio/voices/filler_v1/"):
            _issue(issues, f"{prefix} audio_path must be an exact filler_v1 asset")
            audio_path = ""
        if audio_path:
            paths.setdefault(audio_path, []).append(row)
            if Path(audio_path).suffix.lower() != ".ogg":
                _issue(issues, f"{prefix} audio_path is not OGG: {audio_path}")
            basename = Path(audio_path).stem.lower()
            if basename in GENERIC_TOKENS or any(
                token in cue_id.lower() for token in ("_talk", "_win", "_yay")
            ):
                _issue(issues, f"generic governed cue rejected: {cue_id} -> {audio_path}")
            exists = (root / audio_path).is_file()
            if status == "READY" and not exists:
                _issue(issues, f"READY asset missing: {audio_path}")
            if status == "READY":
                asset_key = Path(audio_path).stem
                expected = manifest_text.get(asset_key)
                if expected is None:
                    _issue(issues, f"READY asset missing manifest transcript: {asset_key}")
                elif normalize_transcript(str(row.get("caption", ""))) != normalize_transcript(expected):
                    _issue(issues, f"READY caption/transcript mismatch: {cue_id} -> {asset_key}")
            if status == "PENDING_GENERATION" and mode == "delivery" and not exists:
                _issue(issues, f"PENDING asset missing in delivery mode: {audio_path}")
        video_reuse = row.get("video_reuse")
        if not isinstance(video_reuse, dict) or video_reuse.get("eligible") is not True:
            _issue(issues, f"{prefix} must declare gameplay/video reuse eligibility")
        elif not isinstance(video_reuse.get("video_ids"), list) or not video_reuse["video_ids"]:
            _issue(issues, f"{prefix} video_reuse.video_ids must be non-empty")

    missing_routes = REQUIRED_ROUTES - routes
    if missing_routes:
        _issue(issues, "catalog missing routes: " + ", ".join(sorted(missing_routes)))

    for audio_path, reused_rows in paths.items():
        if len(reused_rows) < 2:
            continue
        declarations = [row.get("shared_asset_reuse") for row in reused_rows]
        if any(not isinstance(value, dict) for value in declarations):
            ids = ", ".join(str(row.get("cue_id")) for row in reused_rows)
            _issue(issues, f"duplicate exact asset requires shared_asset_reuse: {audio_path} ({ids})")
            continue
        reuse_ids = {str(value.get("reuse_id", "")) for value in declarations}
        reasons = {str(value.get("reason", "")) for value in declarations}
        if "" in reuse_ids or "" in reasons or len(reuse_ids) != 1 or len(reasons) != 1:
            _issue(issues, f"inconsistent shared_asset_reuse declaration: {audio_path}")

    _validate_protected_hashes(root, catalog, issues)
    return issues


def _decode_gd_string(value: str) -> str:
    return value.replace(r'\"', '"').replace(r"\'", "'").replace(r"\n", "\n")


def extract_literal_callsite_captions(root: Path = ROOT) -> dict[str, set[str]]:
    """Extract literal governed calls from all P1 gameplay callsites."""
    result: dict[str, set[str]] = {}
    call_re = re.compile(
        r"(?:_say_day_one_context|_say_context|say_day_one_context)\s*"
        r"\(\s*\"([a-z0-9_]+)\"\s*,\s*\"((?:\\.|[^\"])*)\""
    )
    for rel in GOVERNED_CALLSITE_FILES:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in call_re.finditer(text):
            result.setdefault(match.group(1), set()).add(_decode_gd_string(match.group(2)))
    return result


def _dynamic_rows() -> dict[str, tuple[str, Path, tuple[str, ...]]]:
    result: dict[str, tuple[str, Path, tuple[str, ...]]] = {}
    for family in DYNAMIC_CALLSITE_FAMILIES:
        source = family["source"]
        anchors = tuple(str(anchor) for anchor in family["anchors"])
        for cue_id, caption in family["rows"].items():
            result[str(cue_id)] = (str(caption), source, anchors)
    return result


def validate_governed_callsites(catalog: dict[str, Any], root: Path = ROOT) -> list[str]:
    """Require every governed call/family to have one exact catalog caption."""
    issues: list[str] = []
    rows = {
        str(row.get("cue_id")): row for row in catalog.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("cue_id"), str)
    }
    for cue_id, captions in extract_literal_callsite_captions(root).items():
        row = rows.get(cue_id)
        if row is None:
            _issue(issues, f"governed callsite cue missing from catalog: {cue_id}")
            continue
        if len(captions) != 1:
            _issue(issues, f"governed callsite has conflicting captions: {cue_id}")
            continue
        expected = next(iter(captions))
        if normalize_transcript(str(row.get("caption", ""))) != normalize_transcript(expected):
            _issue(issues, f"governed callsite caption mismatch: {cue_id}")

    for family in DYNAMIC_CALLSITE_FAMILIES:
        rel = family["source"]
        path = root / rel
        if not path.is_file():
            _issue(issues, f"dynamic governed source missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for anchor in family["anchors"]:
            if str(anchor) not in text:
                _issue(issues, f"dynamic family anchor missing: {family['family_id']}:{anchor}")
        for cue_id, expected in family["rows"].items():
            row = rows.get(str(cue_id))
            if row is None:
                _issue(issues, f"dynamic governed cue missing from catalog: {cue_id}")
            elif normalize_transcript(str(row.get("caption", ""))) != normalize_transcript(str(expected)):
                _issue(issues, f"dynamic governed caption mismatch: {cue_id}")
            # Hint keys are deliberately composed from the selected target
            # (`*_found`/`*_clean` -> `*_hint`) and therefore do not appear as
            # literal IDs in the source.  The family anchors plus the exact
            # generated caption template are the static authority for them.
            generated_key = str(cue_id).endswith("_hint")
            if str(cue_id) not in text and not generated_key:
                _issue(issues, f"dynamic governed cue missing from source: {cue_id}")

    for cue_id, metadata in VIDEO_CUES.items():
        row = rows.get(cue_id)
        if row is None:
            _issue(issues, f"video cue missing from catalog: {cue_id}")
        elif normalize_transcript(str(row.get("caption", ""))) != normalize_transcript(str(metadata["caption"])):
            _issue(issues, f"video cue caption mismatch: {cue_id}")
    return issues


def _route_for_cue(cue_id: str, existing: dict[str, Any] | None = None) -> str:
    if existing and existing.get("route") in REQUIRED_ROUTES:
        return str(existing["route"])
    for prefix, route in (
        ("day1_bathroom_", "bathroom"), ("day1_pool_", "pool"),
        ("day1_stuffie_", "stuffie"), ("day1_art_", "art"),
        ("day1_boss_", "boss"), ("day1_recipe_", "kitchen"),
        ("day1_fridge_", "kitchen"), ("d1_c00_", "arrival"),
        ("d1_c01_", "arrival"),
    ):
        if cue_id.startswith(prefix):
            return route
    return "finale" if "finale" in cue_id else "arrival"


def frozen_catalog(catalog: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    """Return the implementation slate with one unique cue-named asset path."""
    existing_rows = {
        str(row.get("cue_id")): dict(row)
        for row in catalog.get("rows", [])
        if isinstance(row, dict) and isinstance(row.get("cue_id"), str)
    }
    required: dict[str, tuple[str, str, dict[str, Any]]] = {}
    for cue_id, captions in extract_literal_callsite_captions(root).items():
        if len(captions) == 1:
            required[cue_id] = (next(iter(captions)), _route_for_cue(cue_id, existing_rows.get(cue_id)), {})
    for cue_id, (caption, _source, _anchors) in _dynamic_rows().items():
        required[cue_id] = (caption, _route_for_cue(cue_id, existing_rows.get(cue_id)), {})
    for cue_id, metadata in VIDEO_CUES.items():
        required[cue_id] = (str(metadata["caption"]), _route_for_cue(cue_id), {
            "video_reuse": {"eligible": True, "video_ids": [metadata["video_id"]], "gameplay_reuse": True},
        })

    merged: dict[str, dict[str, Any]] = {}
    for cue_id, old in existing_rows.items():
        row = dict(old)
        row["audio_path"] = f"assets/audio/voices/filler_v1/roshan_{cue_id}.ogg"
        row["status"] = "PENDING_GENERATION"
        row.pop("shared_asset_reuse", None)
        merged[cue_id] = row
    for cue_id, (caption, route, metadata) in required.items():
        row = merged.setdefault(cue_id, {
            "cue_id": cue_id,
            "moment": cue_id.replace("_", " "),
            "policy": "once_per_session",
            "video_reuse": {"eligible": True, "video_ids": ["day1_gameplay"]},
        })
        row["cue_id"] = cue_id
        row["route"] = route
        row["caption"] = caption
        row["audio_path"] = f"assets/audio/voices/filler_v1/roshan_{cue_id}.ogg"
        row["status"] = "PENDING_GENERATION"
        row.pop("shared_asset_reuse", None)
        row.update(metadata)
    for cue_id, row in merged.items():
        row.setdefault("route", _route_for_cue(cue_id, row))
        row.setdefault("moment", cue_id.replace("_", " "))
        row.setdefault("caption", cue_id.replace("_", " "))
        row.setdefault("policy", "once_per_session")
        row.setdefault("video_reuse", {"eligible": True, "video_ids": ["day1_gameplay"]})
    result = dict(catalog)
    result["status"] = "IMPLEMENTATION_PENDING"
    result["rows"] = [merged[cue_id] for cue_id in sorted(merged)]
    return result


def ready_catalog(catalog: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    """Mark a fully mastered, manifest-backed cohort ready for dev audition."""
    result = json.loads(json.dumps(catalog, ensure_ascii=False))
    result["status"] = "DEV_AUDITION_READY"
    for row in result.get("rows", []):
        row["status"] = "READY"
    issues = validate_catalog(result, root, mode="delivery")
    if issues:
        raise ValueError("cannot mark catalog ready: " + "; ".join(issues))
    return result


def find_generic_governed_calls(root: Path = ROOT) -> list[str]:
    """Find explicit attempts to re-enable generic playback in governed calls."""
    issues: list[str] = []
    call_re = re.compile(r"say_day_one_context\s*\((.*?)\)", re.DOTALL)
    for rel in (Path("scripts/audio_director.gd"), Path("scripts/main.gd"), *GOVERNED_CALLSITE_FILES):
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in call_re.finditer(text):
            args = " ".join(match.group(1).split())
            if re.search(r"(?:allow_generic\s*[:=]\s*|,\s*)true\s*$", args):
                issues.append(f"generic governed call enabled in {rel}: {args[:120]}")
    return issues


def audit(root: Path = ROOT, *, mode: str = "implementation") -> list[str]:
    try:
        catalog = load_catalog(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"cannot load contextual catalog: {exc}"]
    issues = validate_catalog(catalog, root, mode=mode)
    issues.extend(validate_runtime_catalog_parity(catalog, root))
    issues.extend(validate_governed_callsites(catalog, root))
    issues.extend(find_generic_governed_calls(root))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("implementation", "delivery"), default="implementation")
    parser.add_argument("--check", action="store_true", help="check JSON/runtime catalog parity")
    parser.add_argument("--generate", action="store_true", help="write deterministic runtime GDScript catalog")
    parser.add_argument("--freeze", action="store_true", help="expand and normalize the implementation catalog from governed callsites")
    parser.add_argument("--mark-ready", action="store_true", help="mark every manifest-backed mastered row ready for dev audition")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    catalog = load_catalog(root)
    if args.mark_ready:
        ready = ready_catalog(catalog, root)
        path = root / CATALOG_REL
        path.write_text(json.dumps(ready, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"DAY_ONE_CONTEXTUAL_VOICE_AUDIT|READY|rows={len(ready['rows'])}")
        return 0
    if args.freeze:
        frozen = frozen_catalog(catalog, root)
        path = root / CATALOG_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(frozen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"DAY_ONE_CONTEXTUAL_VOICE_AUDIT|FROZEN|rows={len(frozen['rows'])}")
        return 0
    if args.generate:
        path = runtime_catalog_path(root, catalog)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(runtime_catalog_source(catalog), encoding="utf-8", newline="\n")
        print(f"DAY_ONE_CONTEXTUAL_VOICE_AUDIT|GENERATED|path={path.relative_to(root)}")
        return 0
    if args.check:
        issues = validate_runtime_catalog_parity(catalog, root)
        label = "PASS" if not issues else "FAIL"
        print(f"DAY_ONE_CONTEXTUAL_VOICE_AUDIT|RUNTIME_PARITY_{label}")
        for issue in issues:
            print(f"FAIL|{issue}")
        return 0 if not issues else 1
    issues = audit(root, mode=args.mode)
    label = "PASS" if not issues else "FAIL"
    print(f"DAY_ONE_CONTEXTUAL_VOICE_AUDIT|{label}|mode={args.mode}|rows={len(load_catalog(args.root.resolve()).get('rows', [])) if not issues else '?'}")
    for issue in issues:
        print(f"FAIL|{issue}")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
