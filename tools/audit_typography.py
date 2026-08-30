#!/usr/bin/env python3
"""Fail-closed static evidence for the project's typography contract.

Godot's engine, system, and theme fallback are never treated as a font
authority. Missing authority/device evidence is OPEN; regressions and false
VERIFIED claims are machine failures.
"""

from __future__ import annotations

import argparse
import datetime as _datetime
import hashlib
import json
import re
import struct
import subprocess
import zlib
import zipfile
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
    "hover_pressed_color",
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

SFNT_FLAVORS = {b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"}
REQUIRED_DEVICE_STATES = {
    "default", "longest", "wrapped", "locked", "selected", "missing-glyph",
}
HEX40_RE = re.compile(r"[0-9a-fA-F]{40}")
HEX64_RE = re.compile(r"[0-9a-fA-F]{64}")

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
        # Godot import descriptors and other sidecars are not font bytes.  A
        # sidecar named `face.ttf.import` must never make a missing/invalid
        # runtime font look like an asset in the evidence inventory.
        if name.endswith(".import") or name.endswith(".uid"):
            continue
        if name.endswith(FONT_SUFFIXES):
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
        duplicated = sorted(field for field in ROLE_FIELDS
                            if len(re.findall(rf'"{re.escape(field)}"\s*:', block)) != 1)
        if duplicated:
            errors.append(f"role {role} fields must be single-owned: {', '.join(duplicated)}")
        size_match = re.search(r'"font_size"\s*:\s*(\d+)', block)
        if not size_match:
            errors.append(f"role {role} has no numeric font_size")
        elif int(size_match.group(1)) < int(expected.get("min_px", 1)):
            errors.append(
                f"role {role} font_size {size_match.group(1)} below "
                f"minimum {expected.get('min_px')}"
            )
    for marker in ('token["font_authority"]', 'token["fallback_authority"]',
                   'token["line_spacing"]', 'token["hover_pressed_color"]'):
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


def _sfnt_search_fields(table_count: int) -> tuple[int, int, int]:
    """Return the OpenType header searchRange/entrySelector/rangeShift."""
    power = 1 << (table_count.bit_length() - 1)
    search_range = 16 * power
    entry_selector = power.bit_length() - 1
    range_shift = table_count * 16 - search_range
    return search_range, entry_selector, range_shift


def _table_checksum(payload: bytes, tag: bytes = b"") -> int:
    """Compute an OpenType table checksum, treating head.adjustment as zero."""
    data = bytearray(payload)
    if tag == b"head" and len(data) >= 12:
        data[8:12] = b"\0\0\0\0"
    data.extend(b"\0" * ((4 - len(data) % 4) % 4))
    return sum(struct.unpack(f">{len(data) // 4}I", data)) & 0xFFFFFFFF


def _sfnt_bytes(data: bytes) -> bytes | None:
    """Return an uncompressed SFNT byte stream after validating WOFF tables."""
    if len(data) < 4:
        return None
    if data[:4] != b"wOFF":
        return data if data[:4] in SFNT_FLAVORS else None
    if len(data) < 44:
        return None
    try:
        (_signature, flavor, length, tables, reserved, total_size, _major, _minor,
         meta_offset, meta_length, meta_orig_length, priv_offset, priv_length) = struct.unpack(
            ">4s4sIHHIHHIIIII", data[:44])
    except struct.error:
        return None
    if (length != len(data) or reserved != 0 or tables == 0 or tables > 4096
            or flavor not in SFNT_FLAVORS or total_size < 12 + tables * 16):
        return None
    directory_end = 44 + tables * 20
    if directory_end > len(data):
        return None
    # Optional WOFF metadata/private blocks are bounded and cannot overlap the
    # table payload. Metadata is zlib-compressed by the WOFF format.
    blocks: list[tuple[int, int]] = []
    for offset, block_length in ((meta_offset, meta_length), (priv_offset, priv_length)):
        if (offset == 0) != (block_length == 0) or offset + block_length > len(data):
            return None
        if block_length:
            blocks.append((offset, offset + block_length))
    if meta_length:
        try:
            if len(zlib.decompress(data[meta_offset:meta_offset + meta_length])) != meta_orig_length:
                return None
        except zlib.error:
            return None
    records: list[tuple[bytes, int, int, int, int]] = []
    spans: list[tuple[int, int]] = []
    for index in range(tables):
        start = 44 + index * 20
        try:
            tag, offset, comp_len, orig_len, checksum = struct.unpack(
                ">4sIIII", data[start:start + 20])
        except struct.error:
            return None
        if (not orig_len or not comp_len or offset < directory_end
                or offset % 4 or offset + comp_len > len(data)
                or comp_len > orig_len or tag in {record[0] for record in records}):
            return None
        span = (offset, offset + comp_len)
        if any(span[0] < end and start < span[1] for start, end in blocks):
            return None
        spans.append(span)
        records.append((tag, offset, comp_len, orig_len, checksum))
    if records != sorted(records, key=lambda record: record[0]):
        return None
    ordered = sorted(spans)
    if any(end > next_start for (_start, end), (next_start, _end) in zip(ordered, ordered[1:])):
        return None
    sfnt = bytearray(struct.pack(">4sHHHH", flavor, tables, *_sfnt_search_fields(tables)))
    sfnt.extend(b"\0" * (tables * 16))
    payloads: list[tuple[bytes, int, int, int, bytes]] = []
    for tag, offset, comp_len, orig_len, checksum in records:
        compressed = data[offset:offset + comp_len]
        try:
            payload = compressed if comp_len == orig_len else zlib.decompress(compressed)
        except zlib.error:
            return None
        if len(payload) != orig_len or _table_checksum(payload, tag) != checksum:
            return None
        cursor = (len(sfnt) + 3) & ~3
        sfnt.extend(b"\0" * (cursor - len(sfnt)))
        table_offset = cursor
        sfnt.extend(payload)
        sfnt.extend(b"\0" * ((4 - len(payload) % 4) % 4))
        payloads.append((tag, table_offset, orig_len, checksum, payload))
    if len(sfnt) != total_size:
        return None
    for index, (tag, table_offset, orig_len, checksum, _payload) in enumerate(payloads):
        record_at = 12 + index * 16
        sfnt[record_at:record_at + 16] = struct.pack(
            ">4sIII", tag, checksum, table_offset, orig_len)
    return bytes(sfnt)


def _sfnt_structurally_valid(data: bytes) -> bool:
    if len(data) < 12 or data[:4] not in SFNT_FLAVORS:
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
    if (search_range, entry_selector, range_shift) != _sfnt_search_fields(tables):
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
        if (tag in records or not re.fullmatch(rb"[ -~]{4}", tag)
                or length == 0 or offset < directory_end or offset % 4
                or offset + length > len(data)):
            return False
        if _table_checksum(data[offset:offset + length], tag) != _checksum:
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
    if head[12:16] != b"_\x0f<\xf5":
        return False
    if struct.unpack(">H", head[18:20])[0] < 16 or struct.unpack(">H", head[18:20])[0] > 16384:
        return False
    # head.indexToLocFormat is a signed 16-bit field, but the OpenType
    # contract permits only the short (0) and long (1) offset encodings.
    # Negative values are not a valid third encoding and must not make a
    # pseudo-font look structurally complete.
    if struct.unpack(">h", head[50:52])[0] not in {0, 1}:
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
        if offset < 4 or offset + 2 > len(cmap):
            return False
        fmt = struct.unpack(">H", cmap[offset:offset + 2])[0]
        if fmt in {0, 4, 6}:
            if offset + 4 > len(cmap):
                return False
            length = struct.unpack(">H", cmap[offset + 2:offset + 4])[0]
            minimum = {0: 262, 4: 16, 6: 10}[fmt]
            if length < minimum:
                return False
            if fmt == 4:
                if offset + 8 > len(cmap):
                    return False
                segments = struct.unpack(">H", cmap[offset + 6:offset + 8])[0] // 2
                if segments == 0 or 16 + segments * 8 > length:
                    return False
            elif fmt == 6:
                if offset + 10 > len(cmap):
                    return False
                count = struct.unpack(">H", cmap[offset + 8:offset + 10])[0]
                if 10 + count * 2 > length:
                    return False
        elif fmt in {12, 13}:
            if offset + 16 > len(cmap):
                return False
            length = struct.unpack(">I", cmap[offset + 4:offset + 8])[0]
            groups = struct.unpack(">I", cmap[offset + 12:offset + 16])[0]
            if length < 16 or 16 + groups * 12 > length:
                return False
        elif fmt == 14:
            if offset + 10 > len(cmap):
                return False
            length = struct.unpack(">I", cmap[offset + 2:offset + 6])[0]
            selectors = struct.unpack(">I", cmap[offset + 6:offset + 10])[0]
            if length < 10 or 10 + selectors * 11 > length:
                return False
        else:
            continue
        if offset + length > len(cmap):
            return False
        usable_cmap = True
    # The name directory must at least contain a bounded format-0 record
    # array and string storage; this catches directory-shaped pseudo-fonts.
    name = data[records[b"name"][0]:records[b"name"][0] + records[b"name"][1]]
    name_format, name_count, name_offset = struct.unpack(">HHH", name[:6])
    if name_format not in {0, 1} or name_count == 0 or 6 + name_count * 12 > len(name):
        return False
    name_records_end = 6 + name_count * 12
    if name_format == 1:
        if name_records_end + 2 > len(name):
            return False
        lang_tag_count = struct.unpack(">H", name[name_records_end:name_records_end + 2])[0]
        name_records_end += 2 + lang_tag_count * 4
    if name_offset < name_records_end or name_offset > len(name):
        return False
    for index in range(name_count):
        record_at = 6 + index * 12
        _platform, _encoding, _language, _name_id, string_length, string_offset = struct.unpack(
            ">HHHHHH", name[record_at:record_at + 12])
        if string_offset + string_length > len(name) - name_offset:
            return False
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


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
REQUIRED_ASPECTS = {"base", "wide"}
_PNG_COLOR_CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
_PNG_ALLOWED_BIT_DEPTHS = {
    0: {1, 2, 4, 8, 16},
    2: {8, 16},
    3: {1, 2, 4, 8},
    4: {8, 16},
    6: {8, 16},
}
_APK_SIG_BLOCK_MAGIC = b"APK Sig Block 42"
_DEX_MAGICS = {b"dex\n035\0", b"dex\n037\0", b"dex\n038\0",
               b"dex\n039\0", b"dex\n040\0", b"dex\n041\0"}


def _png_dimensions(path: Path) -> tuple[int, int] | None:
    """Validate a complete, non-interlaced PNG and return its dimensions.

    The audit consumes screenshots as evidence, so checking only their chunk
    framing is insufficient: a CRC-correct IDAT can still contain truncated,
    trailing, or otherwise invalid zlib data.  Decode the concatenated IDAT
    stream and account for every scanline byte, including the per-row filter.
    """
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if not data.startswith(PNG_SIGNATURE):
        return None
    cursor = len(PNG_SIGNATURE)
    dimensions: tuple[int, int] | None = None
    ihdr: tuple[int, int, int, int, int, int, int] | None = None
    idat_payload = bytearray()
    saw_idat = False
    saw_iend = False
    while cursor < len(data):
        if cursor + 12 > len(data):
            return None
        length = struct.unpack(">I", data[cursor:cursor + 4])[0]
        end = cursor + 12 + length
        if end < cursor or end > len(data):
            return None
        chunk_type = data[cursor + 4:cursor + 8]
        if len(chunk_type) != 4 or not all(
                (65 <= byte <= 90) or (97 <= byte <= 122)
                for byte in chunk_type):
            return None
        chunk = data[cursor + 8:cursor + 8 + length]
        actual_crc = struct.unpack(">I", data[cursor + 8 + length:end])[0]
        if zlib.crc32(chunk_type + chunk) & 0xFFFFFFFF != actual_crc:
            return None
        if dimensions is None and chunk_type != b"IHDR":
            return None
        if chunk_type == b"IHDR":
            if dimensions is not None or length != 13:
                return None
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", chunk)
            if (width == 0 or height == 0
                    or color_type not in _PNG_COLOR_CHANNELS
                    or bit_depth not in _PNG_ALLOWED_BIT_DEPTHS[color_type]
                    or compression != 0 or filtering != 0 or interlace != 0):
                return None
            dimensions = (width, height)
            ihdr = (width, height, bit_depth, color_type, compression,
                    filtering, interlace)
        elif chunk_type == b"IDAT":
            if saw_iend:
                return None
            saw_idat = True
            idat_payload.extend(chunk)
        elif chunk_type == b"IEND":
            if length != 0 or saw_iend or not saw_idat or end != len(data):
                return None
            saw_iend = True
            cursor = end
            break
        cursor = end
    if dimensions is None or not saw_idat or not saw_iend or cursor != len(data):
        return None
    if ihdr is None:
        return None
    width, height, bit_depth, color_type, _compression, _filtering, _interlace = ihdr
    bits_per_pixel = _PNG_COLOR_CHANNELS[color_type] * bit_depth
    row_bytes = (width * bits_per_pixel + 7) // 8
    expected_scanline_bytes = height * (row_bytes + 1)
    try:
        decompressor = zlib.decompressobj()
        scanlines = decompressor.decompress(bytes(idat_payload))
        scanlines += decompressor.flush()
    except zlib.error:
        return None
    if (not decompressor.eof or decompressor.unused_data
            or decompressor.unconsumed_tail
            or len(scanlines) != expected_scanline_bytes):
        return None
    if any(scanlines[offset * (row_bytes + 1)] > 4 for offset in range(height)):
        return None
    return dimensions


def _git_head(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"], cwd=root,
            check=True, capture_output=True, text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    head = result.stdout.strip().lower()
    return head if HEX40_RE.fullmatch(head) else None


def _binary_xml_valid(data: bytes) -> bool:
    """Check Android's binary-XML file/chunk framing without XML decoding."""
    if len(data) < 8:
        return False
    chunk_type, header_size, declared_size = struct.unpack_from("<HHI", data)
    if chunk_type != 0x0003 or header_size != 8 or declared_size != len(data):
        return False
    cursor = header_size
    while cursor < len(data):
        if len(data) - cursor < 8:
            return False
        _chunk_type, chunk_header_size, chunk_size = struct.unpack_from(
            "<HHI", data, cursor)
        if (chunk_header_size < 8 or chunk_size < chunk_header_size
                or cursor + chunk_size > len(data)):
            return False
        cursor += chunk_size
    return cursor == len(data)


def _dex_valid(data: bytes) -> bool:
    """Validate the fixed DEX header integrity fields and declared size."""
    if len(data) < 112 or data[:8] not in _DEX_MAGICS:
        return False
    file_size, header_size, endian_tag = struct.unpack_from("<III", data, 32)
    if file_size != len(data) or header_size != 112 or endian_tag != 0x12345678:
        return False
    signature = data[12:32]
    if signature != hashlib.sha1(data[32:]).digest():
        return False
    return struct.unpack_from("<I", data, 8)[0] == (zlib.adler32(data[12:]) & 0xFFFFFFFF)


def _resources_table_valid(data: bytes) -> bool:
    """Validate the resources.arsc table chunk's type, header, and size."""
    if len(data) < 12:
        return False
    chunk_type, header_size, declared_size = struct.unpack_from("<HHI", data)
    return (chunk_type == 0x0002 and header_size == 12
            and declared_size == len(data) and declared_size >= header_size)


def _zip_path_safe(name: str) -> bool:
    if not name or "\0" in name or name.startswith(("/", "\\")):
        return False
    if re.match(r"^[A-Za-z]:([/\\]|$)", name):
        return False
    parts = re.split(r"[/\\]", name)
    return all(part not in {"", ".", ".."} for part in parts)


def _apk_signing_block_valid(data: bytes, central_offset: int) -> bool:
    """Recognize a well-framed APK v2/v3 signing block before the central dir."""
    if central_offset < 24:
        return False
    footer = data[central_offset - 24:central_offset]
    if len(footer) != 24:
        return False
    size2 = struct.unpack_from("<Q", footer)[0]
    if footer[8:] != _APK_SIG_BLOCK_MAGIC:
        return False
    block_start = central_offset - size2 - 8
    if block_start < 0 or block_start + 8 > central_offset - 24:
        return False
    size1 = struct.unpack_from("<Q", data, block_start)[0]
    if size1 != size2:
        return False
    cursor = block_start + 8
    pair_end = central_offset - 24
    found_signer = False
    while cursor < pair_end:
        if pair_end - cursor < 12:
            return False
        pair_size = struct.unpack_from("<Q", data, cursor)[0]
        pair_end_item = cursor + 8 + pair_size
        if pair_size < 4 or pair_end_item > pair_end:
            return False
        pair_id = struct.unpack_from("<I", data, cursor + 8)[0]
        if pair_id in {0x7109871A, 0xF05368C0} and pair_size > 4:
            found_signer = True
        cursor = pair_end_item
    return cursor == pair_end and found_signer


def _apk_zip_valid(path: Path) -> tuple[bool, str, set[str], bytes | None]:
    """Validate ZIP integrity, path safety, and return names/raw bytes."""
    try:
        raw = path.read_bytes()
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            names: set[str] = set()
            folded_names: set[str] = set()
            for info in infos:
                name = info.filename
                folded = name.casefold()
                if (not _zip_path_safe(name) or folded in folded_names
                        or info.flag_bits & 0x1):
                    return False, "APK ZIP contains duplicate, unsafe, or encrypted paths", set(), None
                folded_names.add(folded)
                names.add(name)
                archive.read(info)
            if archive.testzip() is not None:
                return False, "APK ZIP has a corrupt member", set(), None
            # zipfile tolerates arbitrary trailing bytes.  APK evidence must
            # bind to the exact archive, including the central-directory end.
            eocd_offset = raw.rfind(b"PK\x05\x06")
            if eocd_offset < 0 or eocd_offset + 22 > len(raw):
                return False, "APK ZIP has no valid end-of-central-directory", set(), None
            fields = struct.unpack_from("<4s4H2LH", raw, eocd_offset)
            comment_length = fields[-1]
            if eocd_offset + 22 + comment_length != len(raw):
                return False, "APK ZIP has trailing or truncated bytes", set(), None
            central_size, central_offset = fields[5], fields[6]
            if (central_offset != archive.start_dir
                    or central_offset + central_size != eocd_offset):
                return False, "APK ZIP central-directory bounds are invalid", set(), None
            return True, "", names, raw
    except (OSError, RuntimeError, zipfile.BadZipFile, ValueError):
        return False, "APK is not a valid ZIP/APK", set(), None


def _apk_artifact(root: Path, path_value: Any, expected: Any) -> tuple[bool, str]:
    if not isinstance(path_value, str) or not path_value.strip():
        return False, "APK path is missing"
    digest = str(expected).lower() if isinstance(expected, str) else ""
    if not HEX64_RE.fullmatch(digest):
        return False, "APK SHA-256 is missing or invalid"
    relative = path_value.removeprefix("res://")
    if (not relative or "\0" in relative or relative.startswith(("/", "\\"))
            or re.match(r"^[A-Za-z]:([/\\]|$)", relative)
            or any(part in {"", ".", ".."} for part in re.split(r"[/\\]", relative))):
        return False, "APK path is unsafe"
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False, "APK escapes repository"
    if not path.is_file() or path.stat().st_size == 0:
        return False, f"APK missing or empty: {relative}"
    if _sha256(path) != digest:
        return False, f"APK hash mismatch: {relative}"
    ok, reason, names, raw = _apk_zip_valid(path)
    if not ok:
        return False, reason
    if raw is None:
        return False, "APK ZIP bytes are unavailable"
    try:
        with zipfile.ZipFile(path) as archive:
            manifest = archive.read("AndroidManifest.xml")
            dex = archive.read("classes.dex")
            resources = archive.read("resources.arsc")
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile):
        return False, "APK ZIP is missing a required Android artifact"
    if not _binary_xml_valid(manifest):
        return False, "APK AndroidManifest.xml is not valid binary XML"
    if not _dex_valid(dex):
        return False, "APK classes.dex header or integrity is invalid"
    if not _resources_table_valid(resources):
        return False, "APK resources.arsc table header or size is invalid"
    signature_pair = (
        "META-INF/MANIFEST.MF" in names
        and any(name.upper().startswith("META-INF/") and name.upper().endswith(".SF")
                and len(name) > len("META-INF/.SF") for name in names)
        and any(name.upper().startswith("META-INF/") and name.upper().endswith(
            (".RSA", ".DSA", ".EC")) and len(name) > len("META-INF/.RSA") for name in names)
    )
    try:
        with zipfile.ZipFile(path) as archive:
            signature_payloads = [archive.read(name) for name in names
                                  if name.upper().startswith("META-INF/")]
    except (KeyError, OSError, RuntimeError, zipfile.BadZipFile):
        return False, "APK signature evidence cannot be read"
    signature_pair = signature_pair and all(signature_payloads)
    # The central offset is recovered from the validated EOCD above.
    eocd_offset = raw.rfind(b"PK\x05\x06")
    central_offset = struct.unpack_from("<L", raw, eocd_offset + 16)[0]
    if not signature_pair and not _apk_signing_block_valid(raw, central_offset):
        return False, "APK has no valid signature evidence"
    return True, ""


def _apk_verification_record(root: Path, value: Any, apk_path: str,
                             apk_sha256: str) -> tuple[bool, str]:
    record, reason = _artifact_json(root, value, "APK verification")
    if record is None:
        return False, reason
    bound_hash = str(_first_value(record, ("apk_sha256", "sha256", "apk_hash"))).lower()
    bound_path = _first_value(record, ("apk_path", "path", "artifact"))
    tool = _first_value(record, ("tool", "verification_tool"))
    tool_version = _first_value(record, ("tool_version", "toolVersion", "version"))
    command = record.get("command")
    result = str(_first_value(record, ("result", "status", "outcome"))).upper()
    package_id = _first_value(record, ("package_id", "package", "application_id"))
    package_version = _first_value(record, (
        "package_version", "version_name", "app_version", "versionName"))
    expected_path = apk_path.removeprefix("res://")
    actual_path = (str(bound_path).removeprefix("res://")
                   if isinstance(bound_path, str) else "")
    if (bound_hash != apk_sha256.lower()
            or actual_path != expected_path
            or not isinstance(tool, str) or not tool.strip()
            or not isinstance(tool_version, str) or not tool_version.strip()
            or not isinstance(command, str) or not command.strip()
            or result != "PASS"
            or not isinstance(package_id, str) or not package_id.strip()
            or not isinstance(package_version, str) or not package_version.strip()):
        return False, "APK verification record must bind APK path/SHA and declare tool/version, PASS command, package id/version"
    return True, ""


def _device_artifact(root: Path, value: Any, selected_hash: str) -> tuple[bool, str]:
    payload, reason = _artifact_json(root, value, "device evidence")
    if payload is None:
        return False, reason
    commit = _first_value(payload, ("commit", "git_commit", "source_commit"))
    apk_path = payload.get("apk_path")
    apk_sha256 = payload.get("apk_sha256")
    font_hash = str(_first_value(payload, (
        "font_sha256", "selected_font_sha256", "font_hash"))).lower()
    devices = _first_value(payload, ("devices", "device"))
    states = _first_value(payload, ("states", "tested_states", "state"))
    # A flat state map cannot prove both required aspect owners on both
    # devices.  The acceptance artifact therefore uses one explicit row per
    # device/state/aspect tuple.
    results = _first_value(payload, ("device_matrix", "matrix"))
    date_value = _first_value(payload, ("date", "review_date", "tested_date"))
    reviewer = payload.get("reviewer")
    actual_head = _git_head(root)
    if (not isinstance(commit, str) or not HEX40_RE.fullmatch(commit.strip())
            or actual_head is None or commit.strip().lower() != actual_head
            or not isinstance(apk_path, str) or not isinstance(apk_sha256, str)
            or not HEX64_RE.fullmatch(font_hash) or font_hash != selected_hash
            or not isinstance(date_value, str) or not _valid_iso_date(date_value)
            or not isinstance(reviewer, str) or not reviewer.strip()):
        return False, "device evidence requires actual HEAD, APK path/hash, font hash, ISO date, and reviewer"
    apk_ok, apk_reason = _apk_artifact(root, apk_path, apk_sha256)
    if not apk_ok:
        return False, apk_reason
    verification = _first_value(payload, (
        "apk_verification", "apk_verification_record", "verification_record",
        "apk_verification_evidence"))
    verification_ok, verification_reason = _apk_verification_record(
        root, verification, apk_path, apk_sha256) if verification is not None else (
            False, "APK verification record is missing")
    if not verification_ok:
        return False, verification_reason

    device_names: list[str] = []
    if isinstance(devices, str):
        device_names = [part.strip().lower() for part in re.split(r"[;,\n]", devices) if part.strip()]
    elif isinstance(devices, list):
        for item in devices:
            if isinstance(item, str) and item.strip():
                device_names.append(item.strip().lower())
            elif isinstance(item, dict):
                name = _first_value(item, ("name", "device", "model"))
                category = _first_value(item, ("category", "class", "tier", "age"))
                parts = [part.strip().lower() for part in (name, category)
                         if isinstance(part, str) and part.strip()]
                if parts:
                    # Keep a model and its age/category in one record so an
                    # `older_phone` category is tied to a named device.
                    device_names.append(" ".join(parts))
    has_m11 = any("lenovo tab m11" in name for name in device_names)
    has_older = any(
        "older" in name and ("phone" in name or "android" in name)
        and len(set(re.findall(r"[a-z0-9]+", name)) - {
            "older", "android", "phone", "the", "a", "an", "device"
        }) >= 1 for name in device_names)
    if not has_m11 or not has_older:
        return False, "device evidence must include Lenovo Tab M11 and an older-phone entry"

    def canonical_state(value: Any) -> str:
        return re.sub(r"[\s_]+", "-", str(value).strip().lower())

    if isinstance(states, str):
        state_values = [part for part in re.split(r"[;,\n]", states) if part.strip()]
    elif isinstance(states, list):
        state_values = states
    else:
        state_values = []
    state_set = {canonical_state(item) for item in state_values if isinstance(item, str)}
    if len(state_values) != len(REQUIRED_DEVICE_STATES) or state_set != REQUIRED_DEVICE_STATES:
        return False, "device evidence must list exactly the required DL-TYPE-12 states"

    def result_rows(value: Any) -> list[tuple[str, Any]]:
        if isinstance(value, list):
            return [(canonical_state(item.get("state", "")), item)
                    for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            return [(canonical_state(key), item if isinstance(item, dict)
                     else {"result": item}) for key, item in value.items()]
        return []

    rows = result_rows(results)
    if not isinstance(results, list):
        return False, "device evidence requires an explicit per-device/state/aspect matrix"

    aspect_dimensions = payload.get("aspect_dimensions", payload.get("aspects"))
    if not isinstance(aspect_dimensions, dict) or set(aspect_dimensions) != REQUIRED_ASPECTS:
        return False, "device evidence must declare base and wide aspect dimensions"
    parsed_aspects: dict[str, tuple[int, int]] = {}
    for aspect in REQUIRED_ASPECTS:
        dimensions = aspect_dimensions.get(aspect)
        if (not isinstance(dimensions, list) or len(dimensions) != 2
                or any(not isinstance(value, int) or value <= 0 for value in dimensions)):
            return False, f"device evidence {aspect} aspect dimensions are invalid"
        parsed_aspects[aspect] = (dimensions[0], dimensions[1])
    if parsed_aspects["base"] != (1280, 720):
        return False, "device evidence base aspect must be 1280x720"

    expected_rows = len(REQUIRED_DEVICE_STATES) * 2 * 2
    if len(rows) != expected_rows:
        return False, "device evidence matrix must cover every state on both devices and aspects"
    seen_tuples: set[tuple[str, str, str]] = set()
    for _state, item in rows:
        if not isinstance(item, dict):
            return False, "device evidence matrix rows must be structured objects"
        device_name = item.get("device", item.get("device_name"))
        aspect = str(item.get("aspect", item.get("aspect_id", ""))).strip().lower()
        state = canonical_state(item.get("state", ""))
        if not isinstance(device_name, str) or not device_name.strip():
            return False, "device evidence matrix row is missing a device name"
        if aspect not in REQUIRED_ASPECTS or state not in REQUIRED_DEVICE_STATES:
            return False, "device evidence matrix row has an invalid state or aspect"
        key = (device_name.strip().lower(), state, aspect)
        if key in seen_tuples:
            return False, "device evidence matrix contains duplicate device/state/aspect rows"
        seen_tuples.add(key)
    if len({state for _state, state_item in rows
            for state in [canonical_state(state_item.get("state", ""))]}) != len(REQUIRED_DEVICE_STATES):
        return False, "device evidence matrix is missing a required DL-TYPE-12 state"
    if {aspect for _state, state_item in rows
            for aspect in [str(state_item.get("aspect", state_item.get("aspect_id", ""))).lower()]} != REQUIRED_ASPECTS:
        return False, "device evidence matrix is missing a required aspect"
    for name in ("lenovo tab m11",):
        if not any(key[0] == name or name in key[0] for key in seen_tuples):
            return False, "device evidence matrix is missing Lenovo Tab M11 rows"
    if not any("older" in key[0] and ("phone" in key[0] or "android" in key[0])
               for key in seen_tuples):
        return False, "device evidence matrix is missing older-phone rows"
    matrix_devices = {key[0] for key in seen_tuples}
    if len(matrix_devices) != 2:
        return False, "device evidence matrix must contain exactly two named devices"
    declared_devices = set(device_names)
    if not all(any(declared == name or declared in name or name in declared
                   for declared in declared_devices) for name in matrix_devices):
        return False, "device evidence matrix device names are not declared devices"
    for device_name in matrix_devices:
        owned = {(state, aspect) for name, state, aspect in seen_tuples
                 if name == device_name}
        if owned != {(state, aspect) for state in REQUIRED_DEVICE_STATES
                     for aspect in REQUIRED_ASPECTS}:
            return False, f"device evidence matrix is incomplete for {device_name}"

    def external_artifact_ref(role: str, state: str) -> Any:
        containers = (
            payload.get(f"{role}s"), payload.get(f"{role}_references"),
            payload.get(f"{role}_refs"), payload.get(f"{role}shots"),
        )
        for container in containers:
            if isinstance(container, dict):
                candidate = container.get(state)
                if candidate is not None:
                    return candidate
            elif isinstance(container, list):
                for candidate in container:
                    if isinstance(candidate, dict) and canonical_state(
                            candidate.get("state", "")) == state:
                        return candidate
        return None

    def artifact_ref(item: dict[str, Any], role: str, state: str) -> dict[str, Any] | None:
        candidate = item.get(role)
        if candidate is None:
            candidate = item.get(f"{role}_ref")
        if candidate is None:
            candidate = external_artifact_ref(role, state)
        if isinstance(candidate, dict):
            path = candidate.get("path", candidate.get("ref", candidate.get("reference")))
            digest = candidate.get("sha256", candidate.get("hash"))
            dimensions = candidate.get("dimensions")
        else:
            path = candidate if isinstance(candidate, str) else None
            digest = item.get(f"{role}_sha256", item.get(f"{role}_hash"))
            dimensions = item.get(f"{role}_dimensions")
        if not isinstance(path, str) or not path.strip() or not isinstance(digest, str):
            return None
        return {"path": path, "sha256": digest, "dimensions": dimensions}

    used_paths: set[str] = set()
    used_content_hashes: set[str] = set()
    for state, item in rows:
        if not isinstance(item, dict):
            return False, f"device evidence {state} result is not structured"
        result = item.get("result", item.get("status", item.get("outcome")))
        if str(result).strip().upper() != "PASS":
            return False, f"device evidence {state} result is not explicitly PASS"
        aspect = str(item.get("aspect", item.get("aspect_id", ""))).strip().lower()
        expected_dimensions = parsed_aspects[aspect]
        for role in ("screen", "capture"):
            reference = artifact_ref(item, role, state)
            if reference is None:
                return False, f"device evidence {state} is missing a hashed {role} reference"
            ok, ref_reason = _artifact(root, reference)
            if not ok:
                return False, f"device evidence {state} {role}: {ref_reason}"
            relative = str(reference["path"]).removeprefix("res://")
            if relative in used_paths:
                return False, f"device evidence {state} reuses a {role} capture path"
            used_paths.add(relative)
            content_hash = str(reference["sha256"]).lower()
            if content_hash in used_content_hashes:
                return False, f"device evidence {state} reuses capture content SHA-256"
            used_content_hashes.add(content_hash)
            declared_dimensions = reference.get("dimensions")
            if (not isinstance(declared_dimensions, list)
                    or len(declared_dimensions) != 2
                    or tuple(declared_dimensions) != expected_dimensions):
                return False, f"device evidence {state} {role} dimensions do not own {aspect} aspect"
            actual_dimensions = _png_dimensions((root / relative).resolve())
            if actual_dimensions != expected_dimensions:
                return False, f"device evidence {state} {role} is not a valid PNG with declared dimensions"
    return True, ""


def _valid_iso_date(value: str) -> bool:
    try:
        return _datetime.date.fromisoformat(value.strip()).isoformat() == value.strip()
    except (TypeError, ValueError):
        return False


def _license_rows(text: str) -> list[dict[str, str]]:
    """Parse the canonical markdown ledger, rather than matching free text."""
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None and {cell.lower() for cell in cells} >= {"path", "source", "license"}:
            header = [cell.lower() for cell in cells]
            continue
        if header is None or not cells or all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        if len(cells) < len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def _license_path_matches(cell: str, asset: str) -> bool:
    # Match a complete path token, including grouped rows, while rejecting
    # look-alike substrings such as `face.ttf.backup`.
    pattern = rf"(?<![A-Za-z0-9_./*-]){re.escape(asset)}(?![A-Za-z0-9_./*-])"
    return bool(re.search(pattern, cell)) or cell.strip() == asset


def _recognized_license(value: str) -> bool:
    normalized = re.sub(r"\s+", " ", value.strip()).lower()
    # Keep this deliberately exact.  Substring checks accepted adversarial
    # values such as `NOT MIT LICENSE` and silently converted unknown/TBD
    # provenance into a green authority claim.
    return normalized in {
        "mit", "mit license", "apache-2.0", "apache 2.0", "apache license 2.0",
        "bsd-2-clause", "bsd-3-clause", "isc", "ofl-1.1", "sil ofl 1.1",
        "cc0-1.0", "cc0", "cc-by-4.0", "cc-by-sa-4.0", "unlicense",
        "public domain", "public-domain", "gpl-3.0", "gpl-3.0-only",
        "lgpl-3.0", "lgpl-3.0-only", "mpl-2.0", "zlib", "epl-2.0",
    }


def _license_row_for_asset(root: Path, asset: str) -> bool:
    license_path = root / "ASSET_LICENSES.md"
    if not license_path.is_file():
        return False
    try:
        rows = _license_rows(license_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return False
    for row in rows:
        source = row.get("source", "").strip()
        license_name = row.get("license", "").strip()
        url = row.get("url", row.get("source_url", "")).strip()
        modifications = row.get(
            "modifications", row.get("modification", row.get("provenance", ""))
        ).strip()
        provider_identifier = row.get(
            "provider", row.get("provider_id", row.get("source_id", ""))
        ).strip()
        source_lower = source.lower()
        source_valid = bool(source) and source_lower not in {
            "-", "—", "unknown", "tbd", "todo", "pending", "n/a",
        } and not re.match(r"^(?:unknown|tbd|todo|pending)(?:\b|\s)", source_lower)
        url_valid = bool(re.fullmatch(r"https?://[^\s|]+", url, re.IGNORECASE)) \
            or bool(re.fullmatch(r"https?://[^\s|]+", source, re.IGNORECASE))
        provider_valid = bool(re.search(
            r"(?:provider|source[_ -]?id|font[_ -]?id)\s*[:=][^\s|]+",
            source, re.IGNORECASE))
        provider_valid = provider_valid or (
            bool(provider_identifier)
            and provider_identifier.lower() not in {
                "-", "—", "unknown", "tbd", "todo", "pending", "n/a"
            }
        )
        modification_valid = bool(modifications) and modifications.lower() not in {
            "-", "—", "unknown", "tbd", "todo", "pending", "n/a",
        }
        if (_license_path_matches(row.get("path", ""), asset)
                and source_valid and (url_valid or provider_valid)
                and modification_valid and _recognized_license(license_name)):
            return True
    return False


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
    # `license_row` in the manifest is descriptive metadata only. Authority
    # comes from a parsed ledger row whose path, source and recognized license
    # fields all bind to the selected runtime asset.
    license_ok = bool(binding_asset and _license_row_for_asset(root, binding_asset))

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
