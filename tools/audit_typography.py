#!/usr/bin/env python3
"""Fail-closed static evidence for the project's typography contract.

Godot's engine, system, and theme fallback are never treated as a font
authority. Missing authority/device evidence is OPEN; regressions and false
VERIFIED claims are machine failures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import zlib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MANIFEST = "audit/typography_manifest.json"
PRODUCTION_ROOT = "scripts"
LABEL3D_RE = re.compile(r"\bLabel3D\s*\.\s*new\s*\(")
ROLE_CONSTS = {
    "display": "ROLE_DISPLAY",
    "title": "ROLE_TITLE",
    "child_control": "ROLE_CHILD_CONTROL",
    "body": "ROLE_BODY",
    "adult_caption": "ROLE_ADULT_CAPTION",
    "status": "ROLE_STATUS",
    "numeric_progress": "ROLE_NUMERIC",
    "decorative_glyph": "ROLE_DECORATIVE_GLYPH",
}
ROLE_FIELDS = {
    "font_size",
    "font_color",
    "outline_color",
    "outline_size",
    "focus_color",
    "pressed_color",
    "disabled_color",
    "wrap_mode",
    "max_lines",
}
DECLARATION_RE = re.compile(
    r"(?:add_theme_font_override\s*\(\s*[\"']font[\"']|"
    r"(?:default_font|font_override)\s*[:=])"
)
FONT_SUFFIXES = (".ttf", ".otf", ".woff", ".woff2", ".font", ".fontdata")
FONT_PATH_RE = re.compile(
    r"(?:res://)?((?:assets/)?[^\"'\s,)]+(?:\.ttf|\.otf|\.woff2?|\.fontdata?|\.font))",
    re.IGNORECASE,
)

# The editable manifest may describe this baseline for humans, but cannot
# raise the ceiling used by the gate.
SEALED_LABEL3D_BASELINE: dict[str, int] = {
    "scripts/arena/sky_lagoon.gd": 7,
    "scripts/combat_arena.gd": 1,
    "scripts/combat_tutorial.gd": 1,
    "scripts/companion.gd": 13,
    "scripts/collection_system.gd": 2,
    "scripts/dungeon_puzzle_room.gd": 1,
    "scripts/galaxy.gd": 2,
    "scripts/games/dust_boss.gd": 1,
    "scripts/games/shop.gd": 4,
    "scripts/kart.gd": 4,
    "scripts/main.gd": 7,
    "scripts/reef_districts.gd": 1,
    "scripts/stuffie_battle.gd": 1,
}
SEALED_LABEL3D_TOTAL = sum(SEALED_LABEL3D_BASELINE.values())


@dataclass(frozen=True)
class GlyphRef:
    path: str
    line: int
    column: int

    def as_text(self) -> str:
        return f"{self.path}:{self.line}:{self.column}"


def _is_probe(path: Path) -> bool:
    return path.name.startswith("probe") or path.name.startswith("probe_")


def production_scripts(root: Path) -> list[Path]:
    return sorted(
        p for p in (root / PRODUCTION_ROOT).rglob("*.gd") if not _is_probe(p)
    )


def _scan_strings(source: str) -> list[tuple[int, int, str, bool]]:
    """Scan valid single/double/triple/raw GDScript literals conservatively."""
    found: list[tuple[int, int, str, bool]] = []
    i = 0
    line = 1
    column = 1

    def advance(text: str) -> None:
        nonlocal line, column
        if "\n" in text:
            line += text.count("\n")
            column = len(text) - text.rfind("\n")
        else:
            column += len(text)

    while i < len(source):
        char = source[i]
        if char == "#":
            end = source.find("\n", i)
            end = len(source) if end < 0 else end
            advance(source[i:end])
            i = end
            continue
        if char not in "'\"":
            advance(char)
            i += 1
            continue
        start_line, start_column = line, column
        triple = source.startswith(char * 3, i)
        delimiter = char * (3 if triple else 1)
        raw = i > 0 and source[i - 1] in "rR"
        advance(delimiter)
        i += len(delimiter)
        parts: list[str] = []
        while i < len(source):
            if source.startswith(delimiter, i):
                advance(delimiter)
                i += len(delimiter)
                break
            current = source[i]
            if current == "\\" and not raw:
                if i + 1 < len(source) and source[i + 1] in "uU":
                    width = 4 if source[i + 1] == "u" else 8
                    digits = source[i + 2:i + 2 + width]
                    if len(digits) == width and re.fullmatch(r"[0-9A-Fa-f]+", digits):
                        parts.append(chr(int(digits, 16)))
                        escaped = source[i:i + 2 + width]
                        advance(escaped)
                        i += len(escaped)
                        continue
                if i + 1 < len(source):
                    parts.append(source[i + 1])
                    escaped = source[i:i + 2]
                    advance(escaped)
                    i += 2
                    continue
            parts.append(current)
            advance(current)
            i += 1
        found.append((start_line, start_column, "".join(parts), raw))
    return found


def scan_live_glyphs(root: Path) -> dict[str, list[GlyphRef]]:
    refs: dict[str, list[GlyphRef]] = defaultdict(list)
    for path in production_scripts(root):
        relative = path.relative_to(root).as_posix()
        for line, column, content, _raw in _scan_strings(path.read_text(encoding="utf-8")):
            for char in content:
                if ord(char) > 127:
                    refs[f"U+{ord(char):04X}"].append(GlyphRef(relative, line, column))
    return dict(sorted(refs.items()))


def _code_without_comments(source: str) -> str:
    """Blank comments while preserving string content for declaration scans."""
    chars = list(source)
    in_string = False
    delimiter = ""
    raw = False
    i = 0
    while i < len(chars):
        if not in_string and chars[i] == "#":
            end = source.find("\n", i)
            end = len(chars) if end < 0 else end
            for j in range(i, end):
                chars[j] = " "
            i = end
            continue
        if not in_string and chars[i] in "'\"":
            delimiter = chars[i] * (3 if source.startswith(chars[i] * 3, i) else 1)
            raw = i > 0 and chars[i - 1] in "rR"
            in_string = True
            i += len(delimiter)
            continue
        if in_string and source.startswith(delimiter, i):
            i += len(delimiter)
            in_string = False
            continue
        if in_string and chars[i] == "\\" and not raw:
            i += 2
            continue
        i += 1
    return "".join(chars)


def _tracked_files(root: Path) -> Iterable[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, check=True,
            capture_output=True, text=False,
        )
        for raw in result.stdout.split(b"\0"):
            if raw:
                yield root / raw.decode("utf-8")
    except (OSError, subprocess.CalledProcessError):
        yield from (p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)


def inventory_font_assets(root: Path) -> list[str]:
    paths = []
    asset_root = root / "assets"
    candidates = asset_root.rglob("*") if asset_root.exists() else []
    for path in candidates:
        if not path.is_file():
            continue
        name = path.name.lower()
        if any(name.endswith(suffix) or name.endswith(suffix + ".import") for suffix in FONT_SUFFIXES):
            paths.append(path.relative_to(root).as_posix())
    return sorted(paths)


def inventory_font_declarations(root: Path) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    candidates = list(production_scripts(root)) + [root / "project.godot"]
    for path in _tracked_files(root):
        if path.suffix.lower() in {".tscn", ".tres"}:
            candidates.append(path)
    candidates = sorted(set(candidates))
    for path in candidates:
        if not path.exists():
            continue
        relative = path.relative_to(root).as_posix()
        source = _code_without_comments(path.read_text(encoding="utf-8"))
        ext_resource_paths = {
            match.group(1): match.group(2).removeprefix("res://").replace("\\", "/")
            for match in re.finditer(
                r'\[ext_resource\s+path="([^"]+)"[^\]]*id="([^"]+)"', source)
        }
        for line_no, raw_line in enumerate(source.splitlines(), 1):
            line = raw_line
            for match in DECLARATION_RE.finditer(line):
                linked = sorted({
                    found.group(1).replace("\\", "/")
                    for found in FONT_PATH_RE.finditer(line)
                })
                # TSCN/TRES declarations commonly bind an ExtResource on a
                # different line. Resolve the referenced resource ID exactly;
                # never treat an unrelated font resource in the same scene as
                # the selected runtime binding.
                if not linked and path.suffix.lower() in {".tscn", ".tres"}:
                    linked = sorted({
                        ext_resource_paths[resource_id]
                        for resource_id in re.findall(
                            r'ExtResource\(\s*["\']([^"\']+)["\']\s*\)', line)
                        if resource_id in ext_resource_paths
                    })
                hits.append({"path": relative, "line": line_no,
                             "token": match.group(0), "assets": linked})
    return hits


def label3d_counts(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in production_scripts(root):
        count = len(LABEL3D_RE.findall(path.read_text(encoding="utf-8")))
        if count:
            counts[path.relative_to(root).as_posix()] = count
    return dict(sorted(counts.items()))


def _role_block(source: str, constant: str) -> str | None:
    start = source.find(constant + ": {")
    if start < 0:
        return None
    # Each role entry ends on the line before the next ROLE_* entry.  Looking
    # only for a standalone `},` is insufficient because the closing brace is
    # commonly followed by a comma on the same line as the final field.
    next_role = re.search(r"\n\s*ROLE_[A-Z_]+\s*:\s*\{", source[start + 1 :])
    end = start + 1 + next_role.start() if next_role else source.find("\n}", start)
    return source[start:end if end >= 0 else len(source)]


def validate_roles(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_path = root / str(manifest.get("role_source", "scripts/storybook_ui.gd"))
    if not source_path.exists():
        return [f"role source missing: {source_path.relative_to(root).as_posix()}"]
    source = source_path.read_text(encoding="utf-8")
    roles = manifest.get("roles", {})
    for role, expected in roles.items():
        constant = ROLE_CONSTS.get(role)
        block = _role_block(source, constant) if constant else None
        if block is None:
            errors.append(f"missing typography role: {role}")
            continue
        missing = sorted(field for field in ROLE_FIELDS if field not in block)
        if missing:
            errors.append(f"role {role} missing fields: {', '.join(missing)}")
        size_match = re.search(r'"font_size"\s*:\s*(\d+)', block)
        if not size_match:
            errors.append(f"role {role} has no numeric font_size")
        elif int(size_match.group(1)) < int(expected.get("min_px", 1)):
            errors.append(
                f"role {role} font_size {size_match.group(1)} below "
                f"minimum {expected.get('min_px')}"
            )
    for marker in ('token["font_authority"]', 'token["fallback_authority"]', 'token["line_spacing"]'):
        if marker not in source:
            errors.append(f"shared typography authority missing: {marker}")
    return errors


def validate_caption_exception(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    item = manifest.get("adult_caption_exception")
    required = {"role", "min_px", "wrapped", "high_contrast", "voice_picture_redundant", "device_verified", "evidence_status"}
    if not isinstance(item, dict) or not required.issubset(item):
        return ["adult-caption exception metadata is incomplete"]
    if item["role"] != "adult_caption":
        errors.append("adult-caption exception role is not adult_caption")
    if int(item["min_px"]) < 22:
        errors.append("adult-caption minimum is below 22px")
    for key in ("wrapped", "high_contrast", "voice_picture_redundant", "device_verified"):
        if not isinstance(item[key], bool):
            errors.append(f"adult-caption metadata {key} must be boolean")
    if item["evidence_status"] not in {"MISSING", "PROVISIONAL", "VERIFIED"}:
        errors.append("adult-caption evidence_status is invalid")
    return errors


def _sfnt_bytes(data: bytes) -> bytes | None:
    """Return an uncompressed SFNT byte stream after structural validation."""
    if len(data) < 4:
        return None
    if data[:4] != b"wOFF":
        return data if data[:4] in {b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"} else None
    if len(data) < 44:
        return None
    try:
        signature, flavor, length, tables, reserved, total_size, _major, _minor,
        meta_offset, meta_length, _meta_orig, priv_offset, priv_length = struct.unpack(
            ">4s4sIHHIHHIIIII", data[:44])
    except struct.error:
        return None
    if (length != len(data) or reserved != 0 or tables == 0 or tables > 4096
            or total_size < 12 + tables * 16):
        return None
    if flavor not in {b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"}:
        return None
    directory_end = 44 + tables * 20
    if directory_end > len(data):
        return None
    records: list[tuple[bytes, int, int, int]] = []
    spans: list[tuple[int, int]] = []
    for index in range(tables):
        start = 44 + index * 20
        try:
            tag, offset, comp_len, orig_len, _checksum = struct.unpack(
                ">4sIIII", data[start:start + 20])
        except struct.error:
            return None
        if not orig_len or not comp_len or offset < directory_end \
                or offset + comp_len > len(data) or comp_len > orig_len:
            return None
        spans.append((offset, offset + comp_len))
        records.append((tag, offset, comp_len, orig_len))
    if len({record[0] for record in records}) != tables:
        return None
    ordered = sorted(spans)
    if any(end > next_start for (_start, end), (next_start, _end) in zip(ordered, ordered[1:])):
        return None
    sfnt = bytearray(struct.pack(">4sHHHH", flavor, tables, 0, 0, 0)
                     + b"\0" * (tables * 16))
    # The searchRange/entrySelector/rangeShift fields are not semantically
    # relevant to the parser; use deterministic values for the rebuilt stream.
    search_range = 16 * (2 ** (tables.bit_length() - 1))
    sfnt[6:12] = struct.pack(">HHH", search_range, tables.bit_length() - 1,
                             tables * 16 - search_range)
    cursor = len(sfnt)
    payloads: list[tuple[bytes, int, int, int, bytes]] = []
    for tag, offset, comp_len, orig_len in records:
        payload = data[offset:offset + comp_len]
        if comp_len != orig_len:
            try:
                payload = zlib.decompress(payload)
            except zlib.error:
                return None
        if len(payload) != orig_len:
            return None
        cursor = (cursor + 3) & ~3
        if len(sfnt) < cursor:
            sfnt.extend(b"\0" * (cursor - len(sfnt)))
        table_offset = cursor
        sfnt.extend(payload)
        cursor += len(payload)
        payloads.append((tag, table_offset, len(payload), orig_len, payload))
    for index, (tag, table_offset, comp_len, orig_len, payload) in enumerate(payloads):
        record_at = 12 + index * 16
        sfnt[record_at:record_at + 16] = struct.pack(
            ">4sIII", tag, 0, table_offset, orig_len)
    return bytes(sfnt)


def _sfnt_structurally_valid(data: bytes) -> bool:
    if len(data) < 12 or data[:4] not in {b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"}:
        return False
    try:
        _version, tables, search_range, entry_selector, range_shift = struct.unpack(
            ">4sHHHH", data[:12])
    except struct.error:
        return False
    if tables == 0 or tables > 4096 or 12 + tables * 16 > len(data):
        return False
    # Malformed search fields are a common pseudo-font trick. They are cheap
    # to validate and make the directory itself falsifiable.
    expected_search = 16 * (2 ** (tables.bit_length() - 1))
    if (search_range, entry_selector, range_shift) != (
            expected_search, expected_search.bit_length() - 1,
            tables * 16 - expected_search):
        return False
    records: dict[bytes, tuple[int, int]] = {}
    spans: list[tuple[int, int]] = []
    for index in range(tables):
        start = 12 + index * 16
        try:
            tag, _checksum, offset, length = struct.unpack(">4sIII", data[start:start + 16])
        except struct.error:
            return False
        directory_end = 12 + tables * 16
        if tag in records or length == 0 or offset < directory_end \
                or offset + length > len(data):
            return False
        records[tag] = (offset, length)
        spans.append((offset, offset + length))
    ordered = sorted(spans)
    if any(end > next_start for (_start, end), (next_start, _end) in zip(ordered, ordered[1:])):
        return False
    required = {b"head", b"hhea", b"maxp", b"name", b"cmap", b"hmtx"}
    if not required.issubset(records) or not ({b"glyf", b"CFF ", b"CFF2"} & records.keys()):
        return False
    if records[b"head"][1] < 54 or records[b"hhea"][1] < 36 \
            or records[b"maxp"][1] < 6 or records[b"name"][1] < 6 \
            or records[b"cmap"][1] < 4 or records[b"hmtx"][1] < 4:
        return False
    head = data[records[b"head"][0]:records[b"head"][0] + records[b"head"][1]]
    maxp = data[records[b"maxp"][0]:records[b"maxp"][0] + records[b"maxp"][1]]
    hhea = data[records[b"hhea"][0]:records[b"hhea"][0] + records[b"hhea"][1]]
    if struct.unpack(">H", head[18:20])[0] < 16 or struct.unpack(">H", head[18:20])[0] > 16384:
        return False
    glyphs = struct.unpack(">H", maxp[4:6])[0]
    metrics = struct.unpack(">H", hhea[34:36])[0]
    if glyphs == 0 or metrics == 0 or metrics > glyphs or records[b"hmtx"][1] < metrics * 4:
        return False
    cmap = data[records[b"cmap"][0]:records[b"cmap"][0] + records[b"cmap"][1]]
    version, cmap_count = struct.unpack(">HH", cmap[:4])
    if version != 0 or cmap_count == 0 or 4 + cmap_count * 8 > len(cmap):
        return False
    usable_cmap = False
    for index in range(cmap_count):
        platform, encoding, offset = struct.unpack(">HHI", cmap[4 + index * 8:12 + index * 8])
        del platform, encoding
        if offset + 2 > len(cmap):
            return False
        fmt = struct.unpack(">H", cmap[offset:offset + 2])[0]
        if fmt in {0, 4, 6}:
            if offset + 4 > len(cmap):
                return False
            length = struct.unpack(">H", cmap[offset + 2:offset + 4])[0]
        elif fmt in {12, 13, 14}:
            if offset + 8 > len(cmap):
                return False
            length = struct.unpack(">I", cmap[offset + 4:offset + 8])[0]
        else:
            continue
        if length < 4 or offset + length > len(cmap):
            return False
        usable_cmap = True
    return usable_cmap


def _font_file_valid(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if data[:4] == b"wOF2":
        # WOFF2 requires a Brotli decoder, which is intentionally not an
        # implicit dependency of this audit. Reject it rather than accepting
        # a magic-only pseudo-font.
        return False
    sfnt = _sfnt_bytes(data)
    return sfnt is not None and _sfnt_structurally_valid(sfnt)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact(root: Path, value: Any) -> tuple[bool, str]:
    if not isinstance(value, dict):
        return False, "artifact must be a structured path/sha256 object"
    path_value = value.get("path")
    expected = str(value.get("sha256", "")).lower()
    if not isinstance(path_value, str) or not path_value.strip():
        return False, "missing artifact path"
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        return False, f"artifact sha256 is missing or invalid: {path_value}"
    path_value = path_value.removeprefix("res://")
    path = (root / path_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False, "artifact escapes repository"
    if not path.is_file() or path.stat().st_size == 0:
        return False, f"artifact missing or empty: {path_value}"
    if _sha256(path) != expected:
        return False, f"artifact hash mismatch: {path_value}"
    return True, ""


def _artifact_json(root: Path, value: Any, label: str) -> tuple[dict[str, Any] | None, str]:
    ok, reason = _artifact(root, value)
    if not ok:
        return None, f"{label}: {reason}"
    path_value = str(value["path"]).removeprefix("res://")
    try:
        parsed = json.loads((root / path_value).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, f"{label}: artifact is not valid JSON ({exc})"
    if not isinstance(parsed, dict):
        return None, f"{label}: artifact root must be an object"
    return parsed, ""


def _first_value(mapping: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        if name in mapping:
            return mapping[name]
    return None


def _codepoint_set(value: Any) -> set[str]:
    values = list(value.keys()) if isinstance(value, dict) else value
    if not isinstance(values, (list, tuple, set)):
        return set()
    result: set[str] = set()
    for item in values:
        text = str(item.get("codepoint", item.get("code_point", ""))
                     if isinstance(item, dict) else item).upper()
        if re.fullmatch(r"U\+[0-9A-F]{4,6}", text):
            result.add(text)
    return result


def _positive_result_set(value: Any) -> set[str]:
    """Extract code points with an explicitly positive coverage result."""
    result: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            cp = str(key).upper()
            if re.fullmatch(r"U\+[0-9A-F]{4,6}", cp):
                positive = item is True or str(item).upper() in {
                    "PASS", "VERIFIED", "COVERED", "PRESENT", "TRUE"
                } or (isinstance(item, dict) and (
                    item.get("covered") is True
                    or str(item.get("status", "")).upper() in {
                        "PASS", "VERIFIED", "COVERED", "PRESENT"
                    }))
                if positive:
                    result.add(cp)
    elif isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            cp = str(item.get("codepoint", item.get("code_point", ""))).upper()
            positive = item.get("covered") is True or str(item.get("status", "")).upper() in {
                "PASS", "VERIFIED", "COVERED", "PRESENT"
            }
            if re.fullmatch(r"U\+[0-9A-F]{4,6}", cp) and positive:
                result.add(cp)
    return result


def _coverage_artifact(root: Path, value: Any, selected_hash: str,
                       observed: set[str], label: str,
                       negative: bool = False) -> tuple[bool, str]:
    payload, reason = _artifact_json(root, value, label)
    if payload is None:
        return False, reason
    artifact_hash = str(_first_value(payload, (
        "font_sha256", "selected_font_sha256", "font_hash"))).lower()
    if artifact_hash != selected_hash:
        return False, f"{label}: selected font hash is missing or does not match the bound font"
    if negative:
        codepoint = str(_first_value(payload, ("codepoint", "code_point"))).upper()
        status = str(_first_value(payload, ("status", "result", "coverage"))).upper()
        if (not re.fullmatch(r"U\+[0-9A-F]{4,6}", codepoint)
                or codepoint in observed
                or not (payload.get("covered") is False
                        or status in {"MISSING", "ABSENT", "NOT_FOUND", "UNSUPPORTED", "FALSE"})
                or "missing" not in str(payload.get("purpose", "")).lower()
                    and "negative" not in str(payload.get("purpose", "")).lower()):
            return False, f"{label}: no deliberate missing-glyph negative result"
        return True, ""
    listed = _codepoint_set(_first_value(payload, (
        "observed_codepoints", "live_codepoints", "codepoints")))
    positive = _positive_result_set(_first_value(payload, (
        "positive_results", "coverage_results", "results", "covered")))
    missing = sorted(observed - listed)
    if missing:
        return False, f"{label}: missing observed live code points: {', '.join(missing)}"
    if observed - positive:
        return False, f"{label}: no positive coverage result for: {', '.join(sorted(observed - positive))}"
    return True, ""


def _device_artifact(root: Path, value: Any, selected_hash: str) -> tuple[bool, str]:
    payload, reason = _artifact_json(root, value, "device evidence")
    if payload is None:
        return False, reason
    commit = _first_value(payload, ("commit", "git_commit", "source_commit"))
    apk = _first_value(payload, ("apk", "apk_sha256", "apk_hash"))
    font_hash = str(_first_value(payload, (
        "font_sha256", "selected_font_sha256", "font_hash"))).lower()
    devices = _first_value(payload, ("devices", "device"))
    states = _first_value(payload, ("states", "tested_states", "state"))
    results = _first_value(payload, ("results", "outcomes", "checks"))
    if (not isinstance(commit, str) or not commit.strip()
            or not apk or font_hash != selected_hash
            or not isinstance(devices, (list, str)) or not devices
            or not isinstance(states, (list, str)) or not states
            or not isinstance(results, (dict, list)) or not results):
        return False, "device evidence must identify commit, APK, font hash, devices, states, and results"
    return True, ""


def _font_evidence(root: Path, manifest: dict[str, Any],
                   assets: list[str],
                   declarations: list[dict[str, Any]],
                   observed: set[str]) -> tuple[dict[str, Any], list[str], bool]:
    authority = manifest.get("font_authority", {})
    errors: list[str] = []
    invalid_assets = [path for path in assets if not _font_file_valid(root / path)]
    if invalid_assets:
        errors.append("font asset is empty or not a recognized font: " + ", ".join(invalid_assets))

    hashes = authority.get("font_hashes", [])
    hash_map: dict[str, str] = {}
    if not isinstance(hashes, list):
        errors.append("font_hashes must be a list")
    seen_hash_paths: set[str] = set()
    for item in hashes if isinstance(hashes, list) else []:
        if not isinstance(item, dict) or not item.get("path") or not item.get("sha256"):
            errors.append("font hash entry is missing path or hash")
            continue
        path = str(item["path"]).removeprefix("res://")
        value = str(item["sha256"]).lower()
        if path in seen_hash_paths:
            errors.append(f"font hash entry is duplicated: {path}")
        seen_hash_paths.add(path)
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            errors.append(f"font hash is invalid for {path}")
        elif path not in assets or not (root / path).is_file() or _sha256(root / path) != value:
            errors.append(f"font hash does not match file bytes: {path}")
        hash_map[path] = value
    for asset in assets:
        if asset not in hash_map:
            errors.append(f"font asset has no SHA-256 evidence: {asset}")
    for path in hash_map:
        if path not in assets:
            errors.append(f"font hash names an untracked or missing asset: {path}")

    binding = authority.get("binding", {})
    binding_asset = binding.get("asset") if isinstance(binding, dict) else None
    binding_asset = binding_asset.removeprefix("res://") if isinstance(binding_asset, str) else binding_asset
    observed_bindings = {
        asset.removeprefix("res://")
        for declaration in declarations
        for asset in declaration.get("assets", [])
        if isinstance(asset, str)
    }
    binding_ok = (bool(declarations) and isinstance(binding_asset, str)
                  and binding_asset in assets and binding_asset in observed_bindings)
    license_row = authority.get("license_row")
    if not license_row and isinstance(authority.get("license"), dict):
        license_row = authority["license"].get("row")
    license_path = root / "ASSET_LICENSES.md"
    license_text = license_path.read_text(encoding="utf-8") if license_path.exists() else ""
    license_ok = bool(binding_asset and license_row and binding_asset in license_text
                     and str(license_row).strip() in license_text)

    coverage = authority.get("coverage", {})
    positive = coverage.get("positive") if isinstance(coverage, dict) else authority.get("coverage_evidence")
    negative = coverage.get("negative") if isinstance(coverage, dict) else manifest.get("coverage_negative")
    selected_hash = hash_map.get(binding_asset, "") if isinstance(binding_asset, str) else ""
    positive_ok, positive_reason = _coverage_artifact(
        root, positive, selected_hash, observed, "coverage positive") if positive is not None else (
            False, "coverage positive evidence is missing")
    negative_ok, negative_reason = _coverage_artifact(
        root, negative, selected_hash, observed, "coverage negative", True) if negative is not None else (
            False, "coverage negative evidence is missing")
    coverage_ok = positive_ok and negative_ok
    device = authority.get("device_evidence", {})
    device_value = device.get("artifact") if isinstance(device, dict) else device
    device_ok, device_reason = _device_artifact(
        root, device_value, selected_hash) if device_value is not None else (
            False, "device evidence is missing")
    # A supplied artifact is an assertion, even when its enclosing status is
    # UNRESOLVED/MISSING. Surface malformed paths/hashes instead of allowing
    # them to hide behind an OPEN status.
    if positive is not None and positive_reason:
        errors.append(positive_reason)
    if negative is not None and negative_reason:
        errors.append(negative_reason)
    if device_value is not None and device_reason:
        errors.append(device_reason)

    valid_statuses = {"MISSING", "UNRESOLVED", "PLANNED", "PROVISIONAL", "OPEN", "VERIFIED", "PASS"}
    status_fields = [
        ("font primary", authority.get("primary", "UNRESOLVED")),
        ("font fallback", authority.get("fallback", "MISSING")),
        ("font binding", binding.get("status", "MISSING") if isinstance(binding, dict) else "MISSING"),
        ("font coverage", authority.get("coverage_status", "UNRESOLVED")),
        ("font device", authority.get("device_evidence_status", "MISSING")),
        ("font provenance", authority.get("provenance_status", "MISSING")),
    ]
    if isinstance(coverage, dict):
        status_fields.append(("coverage artifact", coverage.get("status", "UNRESOLVED")))
    if isinstance(device, dict):
        status_fields.append(("device artifact", device.get("status", "MISSING")))
    for label, value in status_fields:
        if str(value).upper() not in valid_statuses:
            errors.append(f"{label} status is invalid: {value}")

    false_claims: list[str] = []
    coverage_claims = [authority.get("coverage_status", "")]
    if isinstance(coverage, dict):
        coverage_claims.append(coverage.get("status", ""))
    if any(str(claim).upper() in {"VERIFIED", "PASS"} for claim in coverage_claims) and not coverage_ok:
        false_claims.append("coverage status VERIFIED/PASS lacks structured positive and negative artifacts")
    device_claims = [authority.get("device_evidence_status", "")]
    if isinstance(device, dict):
        device_claims.append(device.get("status", ""))
    if any(str(claim).upper() in {"VERIFIED", "PASS"} for claim in device_claims) and not device_ok:
        false_claims.append("device status VERIFIED/PASS lacks complete structured evidence")
    if str(authority.get("provenance_status", "")).upper() in {"VERIFIED", "PASS"} and not license_ok:
        false_claims.append("provenance status VERIFIED/PASS lacks a real license row")
    if isinstance(binding, dict) and str(binding.get("status", "")).upper() in {"VERIFIED", "PASS"} and not binding_ok:
        false_claims.append("font binding status VERIFIED/PASS lacks an exact observed binding")
    errors.extend(false_claims)
    evidence = {
        "assets": assets, "invalid_assets": invalid_assets, "bindings": declarations,
        "declarations": declarations,
        "authority": authority, "font_hashes": authority.get("font_hashes", []),
        "hashes": hash_map, "binding_asset": binding_asset, "binding_ok": binding_ok,
        "license_ok": license_ok, "coverage_ok": coverage_ok,
        "coverage_positive": positive, "coverage_negative": negative,
        "coverage_positive_reason": positive_reason, "coverage_negative_reason": negative_reason,
        "device_ok": device_ok, "device_artifact": device_value,
        "device_reason": device_reason, "selected_font_hash": selected_hash,
        "coverage_status": str(authority.get("coverage_status", "UNRESOLVED")),
        "device_evidence_status": str(authority.get("device_evidence_status", "MISSING")),
        "false_claims": false_claims,
    }
    complete = bool(assets and not invalid_assets and binding_ok and hash_map
                    and license_ok and coverage_ok and device_ok
                    and all(str(value).upper() in {"VERIFIED", "PASS"}
                            for _label, value in status_fields)
                    and not errors)
    return evidence, errors, complete


def audit(root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    glyphs = scan_live_glyphs(root)
    allow = manifest.get("glyph_classes", {})
    allowed = set(allow.get("decorative", [])) | set(allow.get("redundant", [])) | set(allow.get("critical", []))
    observed = set(glyphs)
    unclassified = sorted(observed - allowed)
    stale = sorted(allowed - observed)
    duplicate_classes = sorted(
        cp for cp in set(allow.get("decorative", [])) | set(allow.get("redundant", [])) | set(allow.get("critical", []))
        if sum(cp in allow.get(kind, []) for kind in ("decorative", "redundant", "critical")) != 1
    )
    current_labels = label3d_counts(root)
    label_growth = {
        path: {"baseline": SEALED_LABEL3D_BASELINE.get(path, 0), "current": count}
        for path, count in current_labels.items()
        if path not in SEALED_LABEL3D_BASELINE or count > SEALED_LABEL3D_BASELINE[path]
    }
    current_total = sum(current_labels.values())
    declared_baseline = manifest.get("label3d_baseline", {})
    declared_files = declared_baseline.get("files", {}) if isinstance(declared_baseline, dict) else {}
    baseline_inflation = (
        int(declared_baseline.get("total", 0)) > SEALED_LABEL3D_TOTAL
        or any(int(value) > SEALED_LABEL3D_BASELINE.get(path, 0)
               for path, value in declared_files.items())
    )
    role_errors = validate_roles(root, manifest)
    caption_errors = validate_caption_exception(manifest)
    font_assets = inventory_font_assets(root)
    declarations = inventory_font_declarations(root)
    font, font_errors, font_complete = _font_evidence(
        root, manifest, font_assets, declarations, observed)
    machine_errors: list[str] = []
    if unclassified:
        machine_errors.append("unclassified live code points: " + ", ".join(unclassified))
    if stale:
        machine_errors.append("stale glyph allowlist entries: " + ", ".join(stale))
    if duplicate_classes:
        machine_errors.append("glyph allowlist has duplicate classifications: " + ", ".join(duplicate_classes))
    if label_growth or current_total > SEALED_LABEL3D_TOTAL or baseline_inflation:
        machine_errors.append("Label3D ratchet exceeded sealed baseline")
    machine_errors.extend(role_errors)
    machine_errors.extend(caption_errors)
    machine_errors.extend(font_errors)
    return {
        "schema_version": int(manifest.get("schema_version", 1)),
        "status": "FAIL" if machine_errors else ("PASS" if font_complete else "OPEN"),
        "machine_errors": sorted(set(machine_errors)),
        "font": font,
        "glyphs": {
            "observed_codepoints": sorted(observed),
            "counts": {cp: len(glyphs[cp]) for cp in sorted(glyphs)},
            "classification_counts": {
                kind: sum(1 for cp in observed if cp in allow.get(kind, []))
                for kind in ("decorative", "redundant", "critical")
            },
            "unresolved_critical_codepoints": sorted(
                cp for cp in observed if cp in allow.get("critical", [])
            ) if not font.get("coverage_ok") else [],
            "references": {
                cp: [ref.as_text() for ref in glyphs[cp]] for cp in sorted(glyphs)
            },
            "unclassified": unclassified,
            "stale_allowlist_entries": stale,
        },
        "label3d": {
            "baseline_total": SEALED_LABEL3D_TOTAL,
            "current_total": current_total,
            "delta": current_total - SEALED_LABEL3D_TOTAL,
            "baseline_files": SEALED_LABEL3D_BASELINE,
            "current_files": current_labels,
            "growth": label_growth,
            "production_file_count": len(current_labels),
        },
        "roles": {
            "required": sorted(manifest.get("roles", {})),
            "errors": sorted(role_errors),
            "adult_caption_exception": manifest.get("adult_caption_exception", {}),
            "caption_errors": sorted(caption_errors),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--check", action="store_true",
                        help="fail only on regressions or false evidence")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    manifest_path = (args.manifest or (root / DEFAULT_MANIFEST)).resolve()
    report = audit(root, manifest_path)
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(f"TYPOGRAPHY_AUDIT status={report['status']}")
        print(f"FONT assets={len(report['font']['assets'])} bindings={len(report['font']['bindings'])} coverage={report['font']['coverage_status']} device={report['font']['device_evidence_status']}")
        print(f"GLYPHS observed={len(report['glyphs']['observed_codepoints'])} unclassified={len(report['glyphs']['unclassified'])} critical={report['glyphs']['classification_counts']['critical']} critical_unresolved={len(report['glyphs']['unresolved_critical_codepoints'])}")
        print(f"LABEL3D current={report['label3d']['current_total']} baseline={report['label3d']['baseline_total']} files={report['label3d']['production_file_count']} delta={report['label3d']['delta']}")
        for path, count in report["label3d"]["current_files"].items():
            print(f"LABEL3D_FILE {count:2d} {path}")
        for error in report["machine_errors"]:
            print(f"FAIL {error}")
        if report["status"] == "OPEN":
            print("OPEN font authority, coverage, and/or device evidence remains unresolved")
    return 1 if args.check and report["machine_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
