from __future__ import annotations

import json
import hashlib
import os
import struct
import tempfile
import unittest
import zlib
import subprocess
import shutil
import stat
import zipfile
from pathlib import Path
from unittest.mock import patch

from tools.audit_typography import (
    _apk_artifact, _apk_verification_record, _binary_xml_valid, _discover_apk_parser,
    _discover_apk_verifier, _parse_aapt_output, _parse_apkanalyzer_manifest,
    _png_dimensions, _run_parser, _run_verifier,
    _sfnt_bytes, _sfnt_structurally_valid, audit, inventory_font_assets,
    scan_live_glyphs,
)


ROLE_SOURCE = '''
const ROLE_DISPLAY := &"display"
const ROLE_TITLE := &"title"
const ROLE_CHILD_CONTROL := &"child_control"
const ROLE_BODY := &"body"
const ROLE_ADULT_CAPTION := &"adult_caption"
const ROLE_STATUS := &"status"
const ROLE_NUMERIC := &"numeric_progress"
const ROLE_DECORATIVE_GLYPH := &"decorative_glyph"
const TYPOGRAPHY_ROLES: Dictionary = {
\tROLE_DISPLAY: {"font_size": 56, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 1},
\tROLE_TITLE: {"font_size": 44, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 2},
\tROLE_CHILD_CONTROL: {"font_size": 30, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 2},
\tROLE_BODY: {"font_size": 30, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 3},
\tROLE_ADULT_CAPTION: {"font_size": 22, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 3},
\tROLE_STATUS: {"font_size": 30, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 2},
\tROLE_NUMERIC: {"font_size": 34, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 1},
\tROLE_DECORATIVE_GLYPH: {"font_size": 30, "font_color": 1, "outline_color": 1,
\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,
\t\t"disabled_color": 1, "wrap_mode": 0, "max_lines": 1},
}
func typography_role(role: StringName) -> Dictionary:
\tvar token: Dictionary = {}
\ttoken["font_authority"] = "engine"
\ttoken["fallback_authority"] = "fallback"
\ttoken["line_spacing"] = 0
\treturn token
'''

# Keep the synthetic role source aligned with the production role contract;
# this replacement updates every role without depending on host font files.
ROLE_SOURCE = ROLE_SOURCE.replace(
    '\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,',
    '\t\t"outline_size": 1, "focus_color": 1, "pressed_color": 1,\n'
    '\t\t"hover_pressed_color": 1,')
ROLE_SOURCE = ROLE_SOURCE.replace(
    '\ttoken["line_spacing"] = 0',
    '\ttoken["line_spacing"] = 0\n\ttoken["hover_pressed_color"] = 1')


def _minimal_sfnt(index_to_loc_format: int = 0) -> bytes:
    """Build a tiny deterministic SFNT without relying on an OS font."""
    tables = {
        "cmap": struct.pack(">HHHHI", 0, 1, 3, 1, 12),
        "glyf": b"\0\0\0\0",
        "head": bytearray(54),
        "hhea": bytearray(36),
        "hmtx": struct.pack(">HH", 1000, 0),
        "maxp": struct.pack(">IH", 0x00010000, 1),
        "name": struct.pack(">HHH", 0, 1, 18) + struct.pack(">HHHHHH", 3, 1, 0, 1, 4, 0) + b"Test",
    }
    tables["head"][0:4] = struct.pack(">I", 0x00010000)
    tables["head"][12:16] = struct.pack(">I", 0x5F0F3CF5)
    tables["head"][18:20] = struct.pack(">H", 1024)
    tables["head"][50:52] = struct.pack(">h", index_to_loc_format)
    tables["hhea"][0:4] = struct.pack(">I", 0x00010000)
    tables["hhea"][34:36] = struct.pack(">H", 1)
    # cmap format 6 has a 12-byte subtable for one glyph; the header above
    # intentionally points at the subtable start and is followed by it.
    tables["cmap"] += struct.pack(">HHHHH", 6, 12, 0, 0x2605, 1) + struct.pack(">H", 1)
    records = sorted(tables.items())
    header = struct.pack(">4sHHHH", b"\x00\x01\x00\x00", len(records),
                         16 * (1 << (len(records).bit_length() - 1)),
                         len(records).bit_length() - 1,
                         len(records) * 16 - 16 * (1 << (len(records).bit_length() - 1)))
    directory = bytearray(header + b"\0" * (16 * len(records)))
    payload = bytearray()
    for index, (tag, data) in enumerate(records):
        while (len(directory) + len(payload)) % 4:
            payload.append(0)
        offset = len(directory) + len(payload)
        payload.extend(data)
        checksum_data = bytearray(data)
        if tag == "head":
            checksum_data[8:12] = b"\0\0\0\0"
        checksum_data.extend(b"\0" * ((4 - len(checksum_data) % 4) % 4))
        checksum = sum(struct.unpack(f">{len(checksum_data) // 4}I", checksum_data)) & 0xFFFFFFFF
        directory[12 + index * 16:28 + index * 16] = struct.pack(
            ">4sIII", tag.encode("ascii"), checksum, offset, len(data))
    payload.extend(b"\0" * ((4 - len(payload) % 4) % 4))
    return bytes(directory + payload)


def _minimal_png(dimensions: tuple[int, int], rgb: tuple[int, int, int],
                 seed: int = 0) -> bytes:
    width, height = dimensions
    # Keep every row valid while making each generated screenshot's pixel
    # payload distinct.  Repeating one compressed image under unique paths is
    # not useful device evidence and should be caught by the audit.
    rows = []
    for row_index in range(height):
        first = tuple((component + seed + row_index) % 256 for component in rgb)
        rows.append(bytes((0,)) + bytes(first) + bytes(rgb) * (width - 1))
    raw = b"".join(rows)

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def _minimal_woff(sfnt: bytes) -> bytes:
    count = struct.unpack(">H", sfnt[4:6])[0]
    entries = []
    blobs = bytearray()
    cursor = 44 + count * 20
    for index in range(count):
        tag, checksum, offset, length = struct.unpack(">4sIII", sfnt[12 + index * 16:28 + index * 16])
        data = sfnt[offset:offset + length]
        cursor = (cursor + 3) & ~3
        blobs.extend(b"\0" * (cursor - (44 + count * 20 + len(blobs))))
        compressed = zlib.compress(data) if tag == b"name" else data
        comp = compressed if len(compressed) < len(data) else data
        entries.append((tag, cursor, len(comp), length, checksum, comp))
        blobs.extend(comp)
        cursor += len(comp)
    total = 44 + count * 20 + len(blobs)
    header = struct.pack(">4s4sIHHIHHIIIII", b"wOFF", sfnt[:4], total, count, 0,
                         len(sfnt), 1, 0, 0, 0, 0, 0, 0)
    directory = b"".join(struct.pack(">4sIIII", *entry[:5]) for entry in entries)
    return header + directory + bytes(blobs)


def _minimal_binary_manifest() -> bytes:
    """Build a tiny valid binary Android manifest without Android SDK tools."""
    strings = ["manifest", "package", "com.example.fixture", "application", "name", "Fixture"]
    string_bytes = []
    offsets = []
    for value in strings:
        offsets.append(sum(len(item) for item in string_bytes))
        encoded = value.encode("utf-16le")
        string_bytes.append(struct.pack("<H", len(value)) + encoded + b"\0\0")
    string_pool_header_size = 28
    strings_start = string_pool_header_size + 4 * len(strings)
    string_pool_size = strings_start + sum(len(item) for item in string_bytes)
    string_pool = struct.pack(
        "<HHI5I", 0x0001, string_pool_header_size, string_pool_size,
        len(strings), 0, 0, strings_start, 0,
    ) + b"".join(struct.pack("<I", offset) for offset in offsets) + b"".join(string_bytes)

    def start_element(name_index: int, attribute_name: int, value_index: int) -> bytes:
        node = struct.pack(
            "<IIIIHHHHHH", 1, 0xFFFFFFFF, 0xFFFFFFFF, name_index,
            20, 20, 1, 0, 0, 0,
        )
        attribute = struct.pack(
            "<IIIHBBI", 0xFFFFFFFF, attribute_name, value_index,
            8, 0, 0x03, value_index,
        )
        return struct.pack("<HHI", 0x0102, 16, 8 + len(node) + len(attribute)) + node + attribute

    elements = (
        start_element(0, 1, 2),
        start_element(3, 4, 5),
    )
    payload = string_pool + b"".join(elements)
    return struct.pack("<HHI", 0x0003, 8, 8 + len(payload)) + payload


def _minimal_dex() -> bytes:
    data = bytearray(112)
    data[:8] = b"dex\n035\0"
    struct.pack_into("<III", data, 32, len(data), 112, 0x12345678)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into("<I", data, 8, zlib.adler32(data[12:]) & 0xFFFFFFFF)
    return bytes(data)


def _minimal_apk() -> bytes:
    """Build a deterministic APK-shaped ZIP accepted by structural checks."""
    entries = {
        "AndroidManifest.xml": _minimal_binary_manifest(),
        "classes.dex": _minimal_dex(),
        "resources.arsc": struct.pack("<HHI", 0x0002, 12, 12) + b"\0" * 4,
        "META-INF/MANIFEST.MF": b"Manifest-Version: 1.0\n",
        "META-INF/CERT.SF": b"Signature-Version: 1.0\n",
        # Structurally valid PKCS#7-shaped evidence; cryptographic execution is mocked.
        "META-INF/CERT.RSA": b"\x30\x06\x06\x01\x00\xa0\x01\x00",
    }
    with tempfile.SpooledTemporaryFile() as output:
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, payload in entries.items():
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, payload)
        output.seek(0)
        return output.read()


def manifest(glyphs: list[str], baseline: dict[str, int] | None = None) -> dict:
    return {
        "schema_version": 1,
        "role_source": "scripts/storybook_ui.gd",
        "font_authority": {
            "coverage_status": "UNRESOLVED",
            "device_evidence_status": "MISSING",
            "font_hashes": [],
        },
        "roles": {
            "display": {"min_px": 1}, "title": {"min_px": 1},
            "child_control": {"min_px": 28}, "body": {"min_px": 28},
            "adult_caption": {"min_px": 22}, "status": {"min_px": 28},
            "numeric_progress": {"min_px": 28}, "decorative_glyph": {"min_px": 1},
        },
        "adult_caption_exception": {
            "role": "adult_caption", "min_px": 22, "wrapped": True,
            "high_contrast": True, "voice_picture_redundant": True,
            "device_verified": False, "evidence_status": "MISSING",
        },
        "label3d_baseline": {"total": sum((baseline or {}).values()), "files": baseline or {}},
        "glyph_classes": {"decorative": [], "redundant": [], "critical": glyphs},
    }


class TypographyAuditTests(unittest.TestCase):
    def write_tree(self, source: str, extra: dict[str, str] | None = None) -> tuple[Path, Path]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "scripts").mkdir()
        (root / "scripts/storybook_ui.gd").write_text(ROLE_SOURCE, encoding="utf-8")
        (root / "scripts/main.gd").write_text(source, encoding="utf-8")
        for path, text in (extra or {}).items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"],
                       cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"],
                       cwd=root, check=True)
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
        manifest_path = root / "manifest.json"
        return root, manifest_path

    def test_live_scanner_ignores_comments_and_reports_literal_reference(self) -> None:
        root, manifest_path = self.write_tree('var label = "★" # ☃ comment\n')
        manifest_path.write_text(json.dumps(manifest(["U+2605"])), encoding="utf-8")
        self.assertEqual(set(scan_live_glyphs(root)), {"U+2605"})
        self.assertEqual(scan_live_glyphs(root)["U+2605"][0].line, 1)

    def test_live_scanner_decodes_godot_unicode_escape(self) -> None:
        root, _ = self.write_tree('var label = "\\u2606"\n')
        self.assertEqual(set(scan_live_glyphs(root)), {"U+2606"})

    def test_live_scanner_handles_single_triple_and_raw_literals(self) -> None:
        root, _ = self.write_tree(
            "var single = '★'\n"
            "var multiline = '''\n☆\n'''\n"
            'var raw = r"\\u2603 ☃"\n'
        )
        self.assertEqual(set(scan_live_glyphs(root)), {"U+2605", "U+2606", "U+2603"})

    def test_portable_sfnt_and_woff_fixtures_pass_structural_checks(self) -> None:
        for index_to_loc_format in (0, 1):
            sfnt = _minimal_sfnt(index_to_loc_format)
            self.assertTrue(_sfnt_structurally_valid(sfnt))
            woff = _minimal_woff(sfnt)
            self.assertEqual(_sfnt_bytes(woff), sfnt)

    def test_invalid_index_to_loc_format_is_rejected(self) -> None:
        sfnt = bytearray(_minimal_sfnt())
        sfnt[50:52] = struct.pack(">h", -1)
        self.assertFalse(_sfnt_structurally_valid(bytes(sfnt)))
        sfnt[50:52] = struct.pack(">h", 2)
        self.assertFalse(_sfnt_structurally_valid(bytes(sfnt)))

    def test_sfnt_search_fields_and_table_checksum_are_enforced(self) -> None:
        sfnt = bytearray(_minimal_sfnt())
        sfnt[10:12] = struct.pack(">H", 0)  # entrySelector must be log2(power)
        self.assertFalse(_sfnt_structurally_valid(bytes(sfnt)))
        sfnt = bytearray(_minimal_sfnt())
        sfnt[124] ^= 1  # first byte of cmap, covered by its directory checksum
        self.assertFalse(_sfnt_structurally_valid(bytes(sfnt)))

    def test_font_import_sidecars_are_not_binary_assets(self) -> None:
        root, _manifest_path = self.write_tree('var label = "★"\n', {
            "assets/fonts/face.ttf.import": "metadata",
            "assets/fonts/face.ttf.uid": "uid",
            "assets/fonts/face.ttf": _minimal_sfnt().decode("latin1"),
        })
        self.assertEqual(inventory_font_assets(root), ["assets/fonts/face.ttf"])

    def _write_verified_fixture(self, *, deterministic: bool = False) -> tuple[Path, Path, dict]:
        real_apk: Path | None = None
        if not deterministic:
            real_apk_value = os.environ.get("TYPOGRAPHY_TEST_REAL_APK", "").strip()
            if not real_apk_value:
                self.skipTest(
                    "real APK positive fixture skipped: set TYPOGRAPHY_TEST_REAL_APK "
                    "to a genuine signed, parser-readable APK")
            real_apk = Path(real_apk_value).expanduser()
            if not real_apk.is_file():
                self.skipTest(f"real APK positive fixture is missing: {real_apk}")
        root, manifest_path = self.write_tree(
            'var label = "★"\nbutton.add_theme_font_override("font", load("res://assets/fonts/face.ttf"))\n')
        font = _minimal_sfnt()
        font_path = root / "assets/fonts/face.ttf"
        font_path.parent.mkdir(parents=True)
        font_path.write_bytes(font)
        font_hash = hashlib.sha256(font).hexdigest()
        dimensions = {"base": (1280, 720), "wide": (1600, 720)}
        states = ["default", "longest", "wrapped", "locked", "selected", "missing-glyph"]
        device_names = ["Lenovo Tab M11", "Samsung Galaxy A10 (older Android phone)"]
        matrix = []
        image_index = 0
        for device_index, device_name in enumerate(device_names):
            for state_index, state in enumerate(states):
                for aspect in ("base", "wide"):
                    rows = f"{device_index}_{state_index}_{aspect}"
                    screen_path = f"captures/{rows}_screen.png"
                    capture_path = f"captures/{rows}_capture.png"
                    (root / screen_path).parent.mkdir(parents=True, exist_ok=True)
                    size = dimensions[aspect]
                    screen_bytes = _minimal_png(size, (20, 40, 80), image_index)
                    image_index += 1
                    capture_bytes = _minimal_png(size, (20, 40, 80), image_index)
                    image_index += 1
                    (root / screen_path).write_bytes(screen_bytes)
                    (root / capture_path).write_bytes(capture_bytes)
                    screen = {"path": screen_path, "sha256": hashlib.sha256(screen_bytes).hexdigest(),
                              "dimensions": list(dimensions[aspect])}
                    capture = {"path": capture_path, "sha256": hashlib.sha256(capture_bytes).hexdigest(),
                               "dimensions": list(dimensions[aspect])}
                    matrix.append({"device": device_name, "state": state,
                                   "aspect": aspect, "result": "PASS",
                                   "screen": screen, "capture": capture})
        coverage = {"font_sha256": font_hash, "observed_codepoints": ["U+2605"],
                    "positive_results": {"U+2605": "PASS"}}
        negative = {"font_sha256": font_hash, "codepoint": "U+10FFFF",
                    "purpose": "deliberate missing-glyph negative", "covered": False}
        for name, contents in (("coverage.json", coverage), ("negative.json", negative)):
            (root / name).write_text(json.dumps(contents), encoding="utf-8")
        apk_path = root / "build" / "typography-fixture.apk"
        apk_path.parent.mkdir(parents=True, exist_ok=True)
        if deterministic:
            apk_path.write_bytes(_minimal_apk())
            verifier_name, tool_version, verifier_output = "apksigner", "fixture-verifier 1", b"fixture verifier output"
            parser_name, parser_version, parser_output = "aapt2", "fixture-parser 1", b"fixture parser output"
            parsed = {
                "package_id": "com.example.fixture", "version_code": "7",
                "version_name": "1.2", "manifest_identity": "manifest",
                "application_identity": "Fixture",
            }
            verifier_path = root / "fixture-apksigner"
            parser_path = root / "fixture-aapt2"
            verifier_path.write_bytes(b"deterministic verifier executable")
            parser_path.write_bytes(b"deterministic parser executable")
            try:
                verifier_path.chmod(verifier_path.stat().st_mode | stat.S_IXUSR)
                parser_path.chmod(parser_path.stat().st_mode | stat.S_IXUSR)
            except OSError:
                pass
            patchers = (
                patch("tools.audit_typography._discover_apk_verifier",
                      return_value=(verifier_name, verifier_path)),
                patch("tools.audit_typography._discover_apk_parser",
                      return_value=(parser_name, parser_path)),
                patch("tools.audit_typography._run_verifier",
                      return_value=(True, tool_version, "", verifier_output)),
                patch("tools.audit_typography._run_parser",
                      return_value=(True, parser_version, "", parser_output, parsed, "")),
            )
            for patcher in patchers:
                patcher.start()
                self.addCleanup(patcher.stop)
        else:
            assert real_apk is not None
            apk_path.write_bytes(real_apk.read_bytes())
            verifier = _discover_apk_verifier()
            parser = _discover_apk_parser()
            if verifier is None or parser is None:
                self.skipTest("real APK positive fixture skipped: approved signer and Android parser are required")
            apk_ok, apk_reason = _apk_artifact(root, "build/typography-fixture.apk",
                                               hashlib.sha256(apk_path.read_bytes()).hexdigest())
            if not apk_ok:
                self.skipTest(f"real APK positive fixture is not parseable: {apk_reason}")
            verifier_name, verifier_path = verifier
            verified, tool_version, reason, verifier_output = _run_verifier(
                verifier_name, verifier_path, apk_path)
            if not verified:
                self.skipTest(f"approved APK verifier cannot verify fixture: {reason}")
            parser_name, parser_path = parser
            parsed_ok, parser_version, _parser_text, parser_output, parsed, parser_reason = _run_parser(
                parser_name, parser_path, apk_path)
            if not parsed_ok:
                self.skipTest(f"approved Android parser cannot parse fixture: {parser_reason}")
        output_path = root / "apk-verification-output.txt"
        output_path.write_bytes(verifier_output)
        parser_output_path = root / "apk-parser-output.txt"
        parser_output_path.write_bytes(parser_output)
        apk_hash = hashlib.sha256(apk_path.read_bytes()).hexdigest()
        verification = {
            "apk_path": "build/typography-fixture.apk", "apk_sha256": apk_hash,
            "tool": verifier_name, "tool_version": tool_version,
            "executable_path": str(verifier_path),
            "executable_sha256": hashlib.sha256(verifier_path.read_bytes()).hexdigest(),
            "output_sha256": hashlib.sha256(verifier_output).hexdigest(),
            "output_artifact": {"path": "apk-verification-output.txt",
                                "sha256": hashlib.sha256(verifier_output).hexdigest()},
            "result": "PASS", "package_id": parsed["package_id"],
            "package_version": parsed["version_name"], "version_code": parsed["version_code"],
            "android_parser": {
                "tool": parser_name, "tool_version": parser_version,
                "executable_path": str(parser_path),
                "executable_sha256": hashlib.sha256(parser_path.read_bytes()).hexdigest(),
                "output_sha256": hashlib.sha256(parser_output).hexdigest(),
                "output_artifact": {"path": "apk-parser-output.txt",
                                     "sha256": hashlib.sha256(parser_output).hexdigest()},
                "package_id": parsed["package_id"], "version_code": parsed["version_code"],
                "version_name": parsed["version_name"],
                "manifest_identity": parsed["manifest_identity"],
                "application_identity": parsed["application_identity"],
            },
        }
        verification_path = root / "apk-verification.json"
        verification_path.write_text(json.dumps(verification), encoding="utf-8")
        device = {"commit": subprocess.run(
                      ["git", "rev-parse", "HEAD"], cwd=root, check=True,
                      capture_output=True, text=True).stdout.strip(),
                   "apk_path": "build/typography-fixture.apk",
                   "apk_sha256": apk_hash,
                  "font_sha256": font_hash,
                  "date": "2026-08-30", "reviewer": "Typography QA",
                  "devices": device_names, "states": states,
                  "aspect_dimensions": {key: list(value) for key, value in dimensions.items()},
                   "device_matrix": matrix,
                   "apk_verification": {
                       "path": "apk-verification.json",
                       "sha256": hashlib.sha256(verification_path.read_bytes()).hexdigest(),
                   }}
        (root / "device.json").write_text(json.dumps(device), encoding="utf-8")
        data = manifest(["U+2605"])
        authority = data["font_authority"]
        authority.update({
            "primary": "PASS", "fallback": "PASS", "provenance_status": "PASS",
            "coverage_status": "PASS", "device_evidence_status": "PASS",
            "font_hashes": [{"path": "assets/fonts/face.ttf", "sha256": font_hash}],
            "binding": {"status": "PASS", "asset": "assets/fonts/face.ttf"},
            "coverage": {"status": "PASS", "positive": {"path": "coverage.json", "sha256": hashlib.sha256(json.dumps(coverage).encode()).hexdigest()},
                          "negative": {"path": "negative.json", "sha256": hashlib.sha256(json.dumps(negative).encode()).hexdigest()}},
            "device_evidence": {"status": "PASS", "artifact": {"path": "device.json", "sha256": hashlib.sha256(json.dumps(device).encode()).hexdigest()}},
            "license_row": "forged manifest echo that must not grant authority",
        })
        (root / "ASSET_LICENSES.md").write_text(
            "| Path | Source | License | URL | Modifications |\n"
            "|---|---|---|---|---|\n"
            "| assets/fonts/face.ttf | Project-owned deterministic font fixture | Apache-2.0 | https://example.invalid/font | none |\n",
            encoding="utf-8")
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        return root, manifest_path, data

    def test_end_to_end_verified_fixture_is_os_font_independent(self) -> None:
        root, manifest_path, _data = self._write_verified_fixture()
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["font"]["license_ok"])
        self.assertTrue(report["font"]["device_ok"])

    def test_framed_but_empty_manifest_is_not_android_manifest(self) -> None:
        self.assertFalse(_binary_xml_valid(struct.pack("<HHI", 0x0003, 8, 8)))

    def test_android_parser_output_requires_identity_values(self) -> None:
        self.assertEqual(
            _parse_apkanalyzer_manifest(
                '<manifest xmlns:android="http://schemas.android.com/apk/res/android" '
                'package="com.example.fixture" android:versionCode="7" '
                'android:versionName="1.2"><application android:label="Fixture"/></manifest>'
            ),
            {"package_id": "com.example.fixture", "version_code": "7",
             "version_name": "1.2", "manifest_identity": "manifest",
             "application_identity": "Fixture"},
        )
        self.assertIsNone(_parse_apkanalyzer_manifest("<manifest/>"))
        self.assertEqual(
            _parse_aapt_output(
                "package: name='com.example.fixture' versionCode='7' versionName='1.2'\n"
                "application-label:'Fixture'\n",
                "E: manifest (line=2)\n  E: application (line=3)\n"
                "    A: android:label(0x01010001)=\"Fixture\"\n",
            )["package_id"], "com.example.fixture")

    def test_sdk_root_discovers_android_parsers_when_not_on_path(self) -> None:
        """SDK-root discovery covers all parser names independently of PATH."""
        with tempfile.TemporaryDirectory() as temporary:
            sdk_root = Path(temporary)
            suffix = ".exe" if os.name == "nt" else ""
            parser_locations = (
                ("apkanalyzer", Path("cmdline-tools") / "16.0" / "bin"),
                ("aapt2", Path("build-tools") / "35.0.0"),
                ("aapt", Path("build-tools") / "35.0.0"),
            )
            with patch.dict(os.environ, {"ANDROID_HOME": str(sdk_root),
                                         "ANDROID_SDK_ROOT": ""}, clear=False), \
                    patch("tools.audit_typography.shutil.which", return_value=None):
                for name, relative_directory in parser_locations:
                    target = sdk_root / relative_directory / f"{name}{suffix}"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(f"deterministic {name}".encode("ascii"))
                    try:
                        target.chmod(target.stat().st_mode | stat.S_IXUSR)
                    except OSError:
                        pass
                    self.assertEqual(_discover_apk_parser(), (name, target.resolve()))
                    target.unlink()

    def test_signed_zip_fake_cannot_grant_android_device_authority(self) -> None:
        """Signature-shaped ZIP evidence is still not an Android APK."""
        root, _manifest_path = self.write_tree('var label = "★"\n')
        apk_path = root / "signed.zip"
        with zipfile.ZipFile(apk_path, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, payload in {
                "payload.txt": b"not an Android package",
                "META-INF/MANIFEST.MF": b"Manifest-Version: 1.0\n",
                "META-INF/CERT.SF": b"Signature-Version: 1.0\n",
                "META-INF/CERT.RSA": b"\x30\x06\x06\x01\x00\xa0\x01\x00",
            }.items():
                archive.writestr(name, payload)
        ok, reason = _apk_artifact(
            root, "signed.zip", hashlib.sha256(apk_path.read_bytes()).hexdigest())
        self.assertFalse(ok)
        self.assertIn("required Android artifact", reason)

    def test_fabricated_verifier_and_command_cannot_grant_device_authority(self) -> None:
        root, manifest_path, data = self._write_verified_fixture(deterministic=True)
        record_path = root / "apk-verification.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["tool"] = "fixture-apk-verifier"
        record["command"] = "echo PASS"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        device_path = root / "device.json"
        device = json.loads(device_path.read_text(encoding="utf-8"))
        device["apk_verification"]["sha256"] = hashlib.sha256(record_path.read_bytes()).hexdigest()
        device_path.write_text(json.dumps(device), encoding="utf-8")
        data["font_authority"]["device_evidence"]["artifact"]["sha256"] = hashlib.sha256(
            device_path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("allowlisted tool" in error for error in report["machine_errors"]))

    def test_malformed_cert_rsa_is_not_signature_evidence(self) -> None:
        root, _manifest_path, _data = self._write_verified_fixture(deterministic=True)
        apk_path = root / "build" / "typography-fixture.apk"
        with zipfile.ZipFile(apk_path) as source:
            entries = {info.filename: source.read(info) for info in source.infolist()}
        cert_name = next(name for name in entries if name.upper().endswith(".RSA"))
        entries[cert_name] = b"deterministic fixture signature evidence"
        with zipfile.ZipFile(apk_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, payload in entries.items():
                archive.writestr(name, payload)
        digest = hashlib.sha256(apk_path.read_bytes()).hexdigest()
        ok, reason = _apk_artifact(root, "build/typography-fixture.apk", digest)
        self.assertFalse(ok)
        self.assertIn("malformed", reason)

    def test_png_crc_correct_invalid_zlib_payload_is_rejected(self) -> None:
        root, _manifest_path = self.write_tree('var label = "★"\n')

        def chunk(kind: bytes, payload: bytes) -> bytes:
            return (struct.pack(">I", len(payload)) + kind + payload
                    + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

        ihdr = struct.pack(">IIBBBBB", 2, 1, 8, 2, 0, 0, 0)
        malformed = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                     + chunk(b"IDAT", b"not-a-zlib-stream")
                     + chunk(b"IEND", b""))
        path = root / "bad.png"
        path.write_bytes(malformed)
        self.assertIsNone(_png_dimensions(path))

    def test_png_rejects_crc_correct_trailing_zlib_payload(self) -> None:
        root, _manifest_path = self.write_tree('var label = "★"\n')

        def chunk(kind: bytes, payload: bytes) -> bytes:
            return (struct.pack(">I", len(payload)) + kind + payload
                    + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

        ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
        stream = zlib.compress(b"\0\x01\x02\x03") + b"trailing"
        malformed = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                     + chunk(b"IDAT", stream) + chunk(b"IEND", b""))
        path = root / "bad-trailing.png"
        path.write_bytes(malformed)
        self.assertIsNone(_png_dimensions(path))

    def test_device_matrix_rejects_duplicate_content_with_distinct_paths(self) -> None:
        root, manifest_path, data = self._write_verified_fixture(deterministic=True)
        device_path = root / "device.json"
        device = json.loads(device_path.read_text(encoding="utf-8"))
        first = device["device_matrix"][0]["screen"]
        duplicate = device["device_matrix"][1]["screen"]
        source = root / first["path"]
        target = root / duplicate["path"]
        target.write_bytes(source.read_bytes())
        duplicate["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        device_path.write_text(json.dumps(device), encoding="utf-8")
        data["font_authority"]["device_evidence"]["artifact"]["sha256"] = hashlib.sha256(
            device_path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("capture content SHA-256" in error
                            for error in report["machine_errors"]))

    def test_device_evidence_requires_sha_bound_apk_verification_record(self) -> None:
        root, manifest_path, data = self._write_verified_fixture(deterministic=True)
        device_path = root / "device.json"
        device = json.loads(device_path.read_text(encoding="utf-8"))
        record_path = root / "apk-verification.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["result"] = "FAIL"
        record_path.write_text(json.dumps(record), encoding="utf-8")
        device["apk_verification"]["sha256"] = hashlib.sha256(
            record_path.read_bytes()).hexdigest()
        device_path.write_text(json.dumps(device), encoding="utf-8")
        data["font_authority"]["device_evidence"]["artifact"]["sha256"] = hashlib.sha256(
            device_path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("verification record" in error
                            for error in report["machine_errors"]))

    def test_plain_text_manifest_zip_is_not_an_apk(self) -> None:
        root, _manifest_path = self.write_tree('var label = "★"\n')
        path = root / "fake.apk"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("AndroidManifest.xml", b"<manifest package='fake'/>")
        ok, reason = _apk_artifact(root, "fake.apk",
                                   hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertFalse(ok)
        self.assertIn("required Android artifact", reason)

    def test_bad_dex_resources_and_signature_are_rejected(self) -> None:
        root, _manifest_path, _data = self._write_verified_fixture(deterministic=True)
        path = root / "build" / "typography-fixture.apk"

        original_entries = None
        def entries() -> dict[str, bytes]:
            with zipfile.ZipFile(path) as archive:
                return {info.filename: archive.read(info)
                        for info in archive.infolist()}

        original_entries = entries()

        def check(modified: dict[str, bytes]) -> str:
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, payload in modified.items():
                    archive.writestr(name, payload)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            return _apk_artifact(root, "build/typography-fixture.apk", digest)[1]

        bad_dex = dict(original_entries)
        bad_dex["classes.dex"] = b"dex\n035\0" + b"broken"
        self.assertIn("classes.dex", check(bad_dex))
        bad_resources = dict(original_entries)
        bad_resources["resources.arsc"] = b"\x02\0\x0c\0\x0b\0\0\0" + b"x"
        self.assertIn("resources.arsc", check(bad_resources))
        no_signature = dict(original_entries)
        for name in list(no_signature):
            if name.upper().startswith("META-INF/") and name.upper().endswith((".RSA", ".SF")):
                del no_signature[name]
        self.assertIn("signature", check(no_signature))

    def test_device_and_license_evidence_reject_forged_strings(self) -> None:
        root, manifest_path, data = self._write_verified_fixture(deterministic=True)
        device = json.loads((root / "device.json").read_text(encoding="utf-8"))
        device["commit"] = "latest"
        (root / "device.json").write_text(json.dumps(device), encoding="utf-8")
        data["font_authority"]["device_evidence"]["artifact"]["sha256"] = hashlib.sha256(
            json.dumps(device).encode()).hexdigest()
        (root / "ASSET_LICENSES.md").write_text(
            "| Path | Source | License | URL | Modifications |\n|---|---|---|---|---|\n"
            "| assets/fonts/not-face.ttf | unrelated source | Apache-2.0 | https://example.invalid | none |\n",
            encoding="utf-8")
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["font"]["license_ok"])
        self.assertTrue(any("actual HEAD" in error for error in report["machine_errors"]))

    def test_license_values_and_source_are_exact_and_provenanced(self) -> None:
        for license_value, source in (("NOT MIT LICENSE", "Project font"),
                                      ("MIT", "TBD source")):
            root, manifest_path, data = self._write_verified_fixture(deterministic=True)
            (root / "ASSET_LICENSES.md").write_text(
                "| Path | Source | License | URL | Modifications |\n"
                "|---|---|---|---|---|\n"
                f"| assets/fonts/face.ttf | {source} | {license_value} | "
                "https://example.invalid/font | none |\n",
                encoding="utf-8")
            manifest_path.write_text(json.dumps(data), encoding="utf-8")
            report = audit(root, manifest_path)
            self.assertFalse(report["font"]["license_ok"])
            self.assertTrue(any("provenance" in error.lower()
                                for error in report["machine_errors"]))

    def test_empty_or_fake_font_is_not_evidence(self) -> None:
        root, manifest_path = self.write_tree(
            'var label = "★"\n',
            {"assets/fonts/fake.ttf": "not a font"},
        )
        manifest_path.write_text(json.dumps(manifest(["U+2605"])), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("not a recognized font" in e for e in report["machine_errors"]))

    def test_sfnt_magic_only_pseudo_font_is_not_evidence(self) -> None:
        root, manifest_path = self.write_tree('var label = "★"\n', {
            "assets/fonts/pseudo.ttf": "\x00\x01\x00\x00" + "x" * 256,
        })
        manifest_path.write_text(json.dumps(manifest(["U+2605"])), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("not a recognized font" in e for e in report["machine_errors"]))

    def test_binding_must_match_an_observed_runtime_asset(self) -> None:
        root, manifest_path = self.write_tree(
            'var label = "★"\nbutton.add_theme_font_override("font", load("res://assets/fonts/other.ttf"))\n',
            {"assets/fonts/selected.ttf": "not a font", "assets/fonts/other.ttf": "not a font"},
        )
        data = manifest(["U+2605"])
        data["font_authority"]["binding"] = {
            "status": "PASS", "asset": "assets/fonts/selected.ttf",
        }
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertTrue(any("not a recognized font" in e for e in report["machine_errors"]))
        self.assertFalse(report["font"]["binding_ok"])

    def test_unhashed_artifact_cannot_support_verified_evidence(self) -> None:
        root, manifest_path = self.write_tree('var label = "★"\n', {
            "evidence.json": "{}",
        })
        data = manifest(["U+2605"])
        data["font_authority"].update({
            "coverage_status": "VERIFIED",
            "coverage": {"status": "VERIFIED", "positive": {"path": "evidence.json"}, "negative": None},
        })
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertTrue(any("sha256 is missing or invalid" in e for e in report["machine_errors"]))

    def test_malformed_sfnt_directory_is_not_evidence(self) -> None:
        # A plausible header with a table directory that points outside the
        # file must not be accepted as a font parser shortcut.
        malformed = b"\x00\x01\x00\x00" + b"\x00\x01\x00\x10\x00\x01\x00\x00" + b"head" + b"\x00" * 12
        root, manifest_path = self.write_tree('var label = "★"\n', {
            "assets/fonts/malformed.ttf": malformed.decode("latin1"),
        })
        manifest_path.write_text(json.dumps(manifest(["U+2605"])), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("not a recognized font" in e for e in report["machine_errors"]))

    def test_unresolved_status_with_populated_paths_never_becomes_pass(self) -> None:
        evidence = "{}"
        digest = hashlib.sha256(evidence.encode()).hexdigest()
        root, manifest_path = self.write_tree('var label = "★"\n', {
            "coverage.json": evidence,
            "negative.json": evidence,
            "device.json": evidence,
        })
        data = manifest(["U+2605"])
        data["font_authority"].update({
            "coverage": {
                "status": "UNRESOLVED",
                "positive": {"path": "coverage.json", "sha256": digest},
                "negative": {"path": "negative.json", "sha256": digest},
            },
            "device_evidence": {
                "status": "MISSING",
                "artifact": {"path": "device.json", "sha256": digest},
            },
        })
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertNotEqual(report["status"], "PASS")

    def test_verified_status_without_binding_hash_license_or_artifacts_fails(self) -> None:
        root, manifest_path = self.write_tree('var label = "★"\n')
        data = manifest(["U+2605"])
        data["font_authority"].update({
            "coverage_status": "VERIFIED",
            "device_evidence_status": "VERIFIED",
            "provenance_status": "VERIFIED",
            "binding": {"status": "VERIFIED", "asset": "assets/fonts/missing.ttf"},
        })
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("VERIFIED" in e for e in report["machine_errors"]))

    def test_manifest_baseline_inflation_cannot_hide_new_label3d(self) -> None:
        root, manifest_path = self.write_tree(
            'var label = "★"\nLabel3D.new()\n',
            {"scripts/new_family.gd": "Label3D.new()\n"},
        )
        data = manifest(["U+2605"], {"scripts/main.gd": 999})
        data["label3d_baseline"]["total"] = 9999
        data["label3d_baseline"]["files"]["scripts/new_family.gd"] = 999
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertEqual(report["label3d"]["baseline_total"], 45)
        self.assertTrue(any("sealed baseline" in e for e in report["machine_errors"]))

    def test_new_codepoint_is_a_machine_failure(self) -> None:
        root, manifest_path = self.write_tree('var label = "★ ☃"\n')
        manifest_path.write_text(json.dumps(manifest(["U+2605"])), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertIn("U+2603", report["glyphs"]["unclassified"])
        self.assertTrue(any("unclassified live code points" in error for error in report["machine_errors"]))

    def test_removed_dodge_button_has_no_stale_lightning_evidence(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest_path = root / "audit/typography_manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        report = audit(root, manifest_path)
        source = (root / "scripts/games/dust_boss.gd").read_text(encoding="utf-8")

        self.assertNotIn("U+26A1", data["glyph_evidence"])
        self.assertNotIn("U+26A1", data["glyph_classes"]["redundant"])
        self.assertNotIn("U+26A1", data["glyph_classes"]["critical"])
        self.assertNotIn("⚡", source)
        self.assertNotIn("DustBossDodgeButton", source)
        self.assertNotIn("db_dodge_button", source)
        self.assertNotIn("U+26A1", report["glyphs"]["observed_codepoints"])

    def test_label3d_new_file_is_a_machine_failure(self) -> None:
        root, manifest_path = self.write_tree(
            'var label = "★"\nLabel3D.new()\n',
            {"scripts/new_family.gd": "Label3D.new()\n"},
        )
        manifest_path.write_text(
            json.dumps(manifest(["U+2605"], {"scripts/main.gd": 1})),
            encoding="utf-8",
        )
        report = audit(root, manifest_path)
        self.assertEqual(report["label3d"]["current_total"], 2)
        self.assertIn("scripts/new_family.gd", report["label3d"]["growth"])
        self.assertTrue(any("Label3D ratchet" in error for error in report["machine_errors"]))

    def test_incomplete_role_or_caption_contract_is_a_machine_failure(self) -> None:
        root, manifest_path = self.write_tree('var label = "★"\n')
        broken = ROLE_SOURCE.replace('"disabled_color": 1, "wrap_mode": 0, "max_lines": 1', '"wrap_mode": 0, "max_lines": 1', 1)
        (root / "scripts/storybook_ui.gd").write_text(broken, encoding="utf-8")
        data = manifest(["U+2605"])
        del data["adult_caption_exception"]["wrapped"]
        manifest_path.write_text(json.dumps(data), encoding="utf-8")
        report = audit(root, manifest_path)
        self.assertTrue(any("missing fields" in error for error in report["machine_errors"]))
        self.assertIn("adult-caption exception metadata is incomplete", report["machine_errors"])

    def test_current_repository_is_open_only_for_external_evidence(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = audit(root, root / "audit/typography_manifest.json")
        self.assertEqual(report["label3d"]["current_total"], 45)
        self.assertEqual(report["label3d"]["production_file_count"], 13)
        self.assertEqual(report["glyphs"]["unclassified"], [])
        self.assertEqual(report["font"]["coverage_status"], "UNRESOLVED")
        self.assertEqual(report["font"]["device_evidence_status"], "MISSING")
        self.assertEqual(report["machine_errors"], [])
        self.assertEqual(report["status"], "OPEN")


if __name__ == "__main__":
    unittest.main()
