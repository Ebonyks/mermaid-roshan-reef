from __future__ import annotations

import json
import hashlib
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from tools.audit_typography import (
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


def _minimal_sfnt() -> bytes:
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
    tables["head"][50:52] = struct.pack(">h", 0)
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
        sfnt = _minimal_sfnt()
        self.assertTrue(_sfnt_structurally_valid(sfnt))
        woff = _minimal_woff(sfnt)
        self.assertEqual(_sfnt_bytes(woff), sfnt)

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

    def _write_verified_fixture(self) -> tuple[Path, Path, dict]:
        root, manifest_path = self.write_tree(
            'var label = "★"\nbutton.add_theme_font_override("font", load("res://assets/fonts/face.ttf"))\n')
        font = _minimal_sfnt()
        font_path = root / "assets/fonts/face.ttf"
        font_path.parent.mkdir(parents=True)
        font_path.write_bytes(font)
        font_hash = hashlib.sha256(font).hexdigest()
        for name, contents in (("screen.png", b"screen"), ("capture.png", b"capture")):
            (root / name).write_bytes(contents)
        screen = {"path": "screen.png", "sha256": hashlib.sha256(b"screen").hexdigest()}
        capture = {"path": "capture.png", "sha256": hashlib.sha256(b"capture").hexdigest()}
        coverage = {"font_sha256": font_hash, "observed_codepoints": ["U+2605"],
                    "positive_results": {"U+2605": "PASS"}}
        negative = {"font_sha256": font_hash, "codepoint": "U+10FFFF",
                    "purpose": "deliberate missing-glyph negative", "covered": False}
        for name, contents in (("coverage.json", coverage), ("negative.json", negative)):
            (root / name).write_text(json.dumps(contents), encoding="utf-8")
        states = ["default", "longest", "wrapped", "locked", "selected", "missing-glyph"]
        results = {state: {"result": "PASS", "screen": screen, "capture": capture} for state in states}
        device = {"commit": "a" * 40, "apk_sha256": "b" * 64, "font_sha256": font_hash,
                  "date": "2026-08-30", "reviewer": "Typography QA",
                  "devices": ["Lenovo Tab M11", "older Android phone"],
                  "states": states, "results": results}
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

    def test_device_and_license_evidence_reject_forged_strings(self) -> None:
        root, manifest_path, data = self._write_verified_fixture()
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
        self.assertTrue(any("exact commit" in error for error in report["machine_errors"]))

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
