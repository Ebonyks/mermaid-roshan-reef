from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import audit_opera_capture as audit  # noqa: E402


class OperaCaptureAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name)
        self.source_root = self.root / "source"
        self.capture_root = self.root / "captures"
        self.source_root.mkdir()
        self.capture_root.mkdir()
        fixture_sources = [
            *audit.SOURCE_FIXED_FILES,
            "scenes/main.tscn",
            "scripts/probe_opera_art.gd",
            "scripts/transitive_capture_dependency.gd",
            "scripts/transitive_capture_dependency.gd.uid",
            "assets/opera/worlds/backdrops/world_chef.png",
            "assets/opera/worlds/backdrops/world_chef.png.import",
            "assets/flats/castle/interactions_v4/castle_interactions_v4.json",
            "shaders/castle_fixture_bloom.gdshader",
        ]
        for index, relative in enumerate(fixture_sources):
            path = self.source_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            source = f"fixture source {index}: {relative}\n"
            if relative == "scripts/probe_opera_art.gd":
                source += (
                    "routes._launch(room_id, index)\n"
                    "await _wait_career_ready(index, room_id)\n"
                    "await _wait_capture_frame_post_draw()\n"
                    "button.is_visible_in_tree()\n"
                    "Vector2i(1280, 720)\n"
                    "Vector2i(1600, 720)\n"
                )
            if path.suffix.lower() == ".png":
                path.write_bytes(source.encode("utf-8"))
            else:
                path.write_text(source, encoding="utf-8")
        self.capture_dependency = (
            self.source_root / "scripts/transitive_capture_dependency.gd"
        )
        self.capture_asset = (
            self.source_root / "assets/opera/worlds/backdrops/world_chef.png"
        )
        self._write_valid_bundle()

    def tearDown(self) -> None:
        self._temp.cleanup()

    @staticmethod
    def _png_bytes(
        dimensions: tuple[int, int],
        accent: tuple[int, int, int],
        marker: int,
    ) -> bytes:
        image = Image.new("RGB", dimensions, (18, 30, 70))
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (dimensions[0] // 4, dimensions[1] // 4,
             dimensions[0] * 3 // 4, dimensions[1] * 3 // 4),
            fill=accent,
        )
        marker_x = 12 + marker * 37
        marker_y = 12 + marker * 19
        draw.rectangle(
            (marker_x, marker_y, marker_x + 24, marker_y + 24),
            fill=((marker * 47 + 31) % 255, (marker * 83 + 61) % 255, 220),
        )
        stream = io.BytesIO()
        image.save(stream, format="PNG", compress_level=1)
        return stream.getvalue()

    def _write_valid_bundle(self) -> None:
        source_signature = audit.compute_source_signature(self.source_root)
        expected = audit.expected_states()
        expected_ids = [state["id"] for state in expected]
        for aspect_index, (aspect, dimensions) in enumerate(audit.ASPECTS.items()):
            aspect_dir = self.capture_root / aspect
            aspect_dir.mkdir()
            states: list[dict] = []
            for state_index, state in enumerate(expected):
                state_id = state["id"]
                png = self._png_bytes(
                    dimensions,
                    (218 - aspect_index * 20, 120, 190),
                    state_index,
                )
                png_hash = audit.sha256_bytes(png)
                (aspect_dir / f"{state_id}.png").write_bytes(png)
                actual_state = copy.deepcopy(state["expected_state"])
                input_evidence: dict = {}
                if state["kind"] == "career_entry":
                    input_evidence = {
                        "method": audit.ROUTE_ENTRY_METHOD,
                        "room_id": actual_state["return_room"],
                        "act_index": actual_state["act_index"],
                        "control_path": f"/root/ReefMain/CareerRoutes/{state_id}",
                    }
                states.append({
                    "id": state_id,
                    "sequence": state["sequence"],
                    "kind": state["kind"],
                    "expected_state": copy.deepcopy(state["expected_state"]),
                    "actual_state": actual_state,
                    "state_signature": audit.canonical_signature(actual_state),
                    "input": input_evidence,
                    "status": "PASS",
                    "failures": [],
                    "image": {
                        "file": f"{state_id}.png",
                        "width": dimensions[0],
                        "height": dimensions[1],
                        "bytes": len(png),
                        "sha256": png_hash,
                    },
                })
            manifest = {
                "schema": audit.SCHEMA,
                "run_nonce": "fixture-shared-run",
                "source_revision": "fixture",
                "aspect_id": aspect,
                "viewport": {"width": dimensions[0], "height": dimensions[1]},
                "capture_method": "same_process_viewport",
                "rendering_method": "mobile",
                "engine": copy.deepcopy(
                    audit.capture_engine_evidence()["canonical"]
                ),
                "source_signature": source_signature,
                "expected_state_ids": expected_ids,
                "states": states,
                "global_failures": [],
                "summary": {
                    "expected": 24,
                    "rows": 24,
                    "written": 24,
                    "passed": 24,
                    "failed": 0,
                },
                "result": "PASS",
            }
            self._write_manifest(aspect, manifest)

    def _manifest(self, aspect: str = "1280x720") -> dict:
        return json.loads(
            (self.capture_root / aspect / audit.MANIFEST_NAME).read_text(
                encoding="utf-8",
            )
        )

    def _write_manifest(self, aspect: str, manifest: dict) -> None:
        (self.capture_root / aspect / audit.MANIFEST_NAME).write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _codes(self) -> set[str]:
        return {
            error.split(":", 1)[0]
            for error in audit.validate_capture_root(
                self.capture_root, self.source_root,
            )
        }

    def test_valid_two_aspect_bundle_passes(self) -> None:
        self.assertEqual(
            audit.validate_capture_root(self.capture_root, self.source_root),
            [],
        )

    def test_canonical_state_signature_matches_frozen_known_answer(self) -> None:
        state = {
            "act_index": 2,
            "career_world_present": True,
            "entry_method": "guarded_castle_career_route_launch",
            "layers": [10, 11, 12, 13],
            "room_id": "opera_hall",
            "stage_id": "opera.act.02",
        }
        self.assertEqual(
            audit.canonical_signature(state),
            "8c492168bd271b360981d5fcfbccb550bb6820e54faedf94749eb28b0d1c2ce5",
        )

    def test_stale_source_signature_fails_closed(self) -> None:
        (self.source_root / "scripts/main.gd").write_text(
            "changed after capture\n", encoding="utf-8",
        )
        self.assertIn("source_signature", self._codes())

    def test_transitive_script_signature_fails_closed(self) -> None:
        self.capture_dependency.write_text(
            "changed transitive capture dependency\n", encoding="utf-8",
        )
        self.assertIn("source_signature", self._codes())

    def test_uid_sidecar_signature_fails_closed(self) -> None:
        (self.source_root / "scripts/transitive_capture_dependency.gd.uid").write_text(
            "changed uid sidecar\n", encoding="utf-8",
        )
        self.assertIn("source_signature", self._codes())

    def test_pixel_asset_signature_fails_closed(self) -> None:
        self.capture_asset.write_bytes(b"changed capture pixel asset\n")
        self.assertIn("source_signature", self._codes())

    def test_mixed_run_nonce_is_stale(self) -> None:
        manifest = self._manifest("1600x720")
        manifest["run_nonce"] = "different-run"
        self._write_manifest("1600x720", manifest)
        self.assertIn("stale_mixed_run", self._codes())

    def test_missing_png_fails_closed(self) -> None:
        state_id = audit.expected_states()[0]["id"]
        (self.capture_root / "1280x720" / f"{state_id}.png").unlink()
        codes = self._codes()
        self.assertIn("file_set_missing", codes)
        self.assertIn("image_missing", codes)

    def test_extra_output_fails_closed(self) -> None:
        (self.capture_root / "1280x720" / "old_stale.png").write_bytes(b"old")
        self.assertIn("file_set_extra", self._codes())

    def test_duplicate_state_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["states"].append(copy.deepcopy(manifest["states"][0]))
        self._write_manifest("1280x720", manifest)
        self.assertIn("state_duplicate", self._codes())

    def test_corrupt_png_fails_even_when_manifest_hash_is_refreshed(self) -> None:
        manifest = self._manifest()
        row = manifest["states"][0]
        path = self.capture_root / "1280x720" / row["image"]["file"]
        corrupt = b"not a decodable PNG"
        path.write_bytes(corrupt)
        row["image"]["bytes"] = len(corrupt)
        row["image"]["sha256"] = audit.sha256_bytes(corrupt)
        self._write_manifest("1280x720", manifest)
        self.assertIn("image_decode", self._codes())

    def test_fully_transparent_png_with_hidden_rgb_fails_closed(self) -> None:
        manifest = self._manifest()
        row = manifest["states"][0]
        path = self.capture_root / "1280x720" / row["image"]["file"]
        image = Image.new("RGBA", audit.ASPECTS["1280x720"], (200, 10, 30, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 639, 719), fill=(10, 220, 180, 0))
        stream = io.BytesIO()
        image.save(stream, format="PNG", compress_level=1)
        hidden_rgb_png = stream.getvalue()
        path.write_bytes(hidden_rgb_png)
        row["image"]["bytes"] = len(hidden_rgb_png)
        row["image"]["sha256"] = audit.sha256_bytes(hidden_rgb_png)
        self._write_manifest("1280x720", manifest)
        self.assertIn("image_transparent", self._codes())

    def test_duplicate_png_fails_with_refreshed_metadata(self) -> None:
        manifest = self._manifest()
        source_row = manifest["states"][0]
        duplicate_row = manifest["states"][1]
        aspect_dir = self.capture_root / "1280x720"
        duplicate = (aspect_dir / source_row["image"]["file"]).read_bytes()
        (aspect_dir / duplicate_row["image"]["file"]).write_bytes(duplicate)
        duplicate_row["image"]["bytes"] = len(duplicate)
        duplicate_row["image"]["sha256"] = audit.sha256_bytes(duplicate)
        self._write_manifest("1280x720", manifest)
        self.assertIn("image_duplicate", self._codes())

    def test_wrong_aspect_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["aspect_id"] = "1600x720"
        self._write_manifest("1280x720", manifest)
        self.assertIn("aspect_id", self._codes())

    def test_wrong_viewport_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["viewport"]["width"] = 1279
        self._write_manifest("1280x720", manifest)
        self.assertIn("viewport", self._codes())

    def test_wrong_renderer_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["rendering_method"] = "gl_compatibility"
        self._write_manifest("1280x720", manifest)
        self.assertIn("renderer", self._codes())

    def test_wrong_semantic_state_fails_with_fresh_state_hash(self) -> None:
        manifest = self._manifest()
        row = manifest["states"][0]
        row["actual_state"]["stage_id"] = "castle.room.wrong"
        row["state_signature"] = audit.canonical_signature(row["actual_state"])
        self._write_manifest("1280x720", manifest)
        self.assertIn("actual_state", self._codes())

    def test_bool_cannot_substitute_for_integer_state_value(self) -> None:
        manifest = self._manifest()
        row = next(
            state for state in manifest["states"]
            if state["actual_state"].get("floor_index") == 1
        )
        row["actual_state"]["floor_index"] = True
        row["state_signature"] = audit.canonical_signature(row["actual_state"])
        self._write_manifest("1280x720", manifest)
        self.assertIn("actual_state", self._codes())

    def test_extra_actual_state_key_fails_with_fresh_state_hash(self) -> None:
        manifest = self._manifest()
        row = manifest["states"][0]
        row["actual_state"]["forged_extra"] = "not allowed"
        row["state_signature"] = audit.canonical_signature(row["actual_state"])
        self._write_manifest("1280x720", manifest)
        self.assertIn("actual_state", self._codes())

    def test_nonempty_state_failures_fail_closed(self) -> None:
        manifest = self._manifest()
        manifest["states"][0]["failures"] = ["semantic readiness timed out"]
        self._write_manifest("1280x720", manifest)
        self.assertIn("state_failures", self._codes())

    def test_missing_career_touch_evidence_fails_closed(self) -> None:
        manifest = self._manifest()
        career_row = next(
            row for row in manifest["states"] if row["kind"] == "career_entry"
        )
        career_row["input"] = {}
        self._write_manifest("1280x720", manifest)
        self.assertIn("input_evidence", self._codes())

    def test_wrong_career_route_evidence_fails_closed(self) -> None:
        manifest = self._manifest()
        career_row = next(
            row for row in manifest["states"] if row["kind"] == "career_entry"
        )
        career_row["input"]["room_id"] = "wrong_room"
        self._write_manifest("1280x720", manifest)
        self.assertIn("input_evidence", self._codes())

    def test_png_hash_drift_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["states"][0]["image"]["sha256"] = "0" * 64
        self._write_manifest("1280x720", manifest)
        self.assertIn("image_hash", self._codes())

    def test_empty_manifest_with_missing_pngs_fails_closed(self) -> None:
        aspect_dir = self.capture_root / "1280x720"
        for path in aspect_dir.glob("*.png"):
            path.unlink()
        (aspect_dir / audit.MANIFEST_NAME).write_text("{}\n", encoding="utf-8")
        codes = self._codes()
        self.assertIn("file_set_missing", codes)
        self.assertIn("schema", codes)
        self.assertIn("state_count", codes)

    def test_direct_signal_route_is_forbidden(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        path.write_text(
            path.read_text(encoding="utf-8") + "button.pressed.emit()\n",
            encoding="utf-8",
        )
        errors = audit.validate_capture_root(self.capture_root, self.source_root)
        self.assertTrue(any(
            error == "probe_contract: direct pressed.emit route is forbidden"
            for error in errors
        ))

    def test_required_token_comment_and_dead_string_spoof_fails(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        source = path.read_text(encoding="utf-8").replace(
            "button.is_visible_in_tree()\n", "",
        )
        source += (
            "# button.is_visible_in_tree()\n"
            'var dead_required = "button.is_visible_in_tree()"\n'
        )
        path.write_text(source, encoding="utf-8")
        self.assertIn(
            "probe_contract: missing button.is_visible_in_tree()",
            audit.probe_contract_errors(self.source_root),
        )

    def test_direct_route_tokens_in_comments_and_strings_are_ignored(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        source = path.read_text(encoding="utf-8") + (
            "# button.pressed.emit()\n"
            '# button.emit_signal("pressed")\n'
            'var dead_route = "button.pressed.emit()"\n'
            'var other_dead_route = "button.emit_signal(\\"pressed\\")"\n'
        )
        path.write_text(source, encoding="utf-8")
        errors = audit.probe_contract_errors(self.source_root)
        self.assertNotIn(
            "probe_contract: direct pressed.emit route is forbidden", errors,
        )
        self.assertNotIn(
            "probe_contract: emit_signal routes are forbidden", errors,
        )

    def test_all_emit_signal_routes_are_forbidden(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        original = path.read_text(encoding="utf-8")
        routes = (
            'button.emit_signal("pressed")',
            'button.emit_signal(&"pressed")',
            'button.emit_signal(StringName("pressed"))',
            'button.emit_signal("anything_else")',
        )
        for route in routes:
            with self.subTest(route=route):
                path.write_text(original + route + "\n", encoding="utf-8")
                self.assertIn(
                    "probe_contract: emit_signal routes are forbidden",
                    audit.probe_contract_errors(self.source_root),
                )

    def test_identifier_prefixed_route_cannot_spoof_required_launch(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        source = path.read_text(encoding="utf-8").replace(
            "routes._launch(room_id, index)",
            "fake_routes._launch(room_id, index)",
        )
        path.write_text(source, encoding="utf-8")
        self.assertIn(
            "probe_contract: missing routes._launch(room_id, index)",
            audit.probe_contract_errors(self.source_root),
        )

    def test_whitespace_and_reflection_main_bypasses_are_forbidden(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        original = path.read_text(encoding="utf-8")
        bypasses = (
            "main . _start_opera_from_room(room_id, index)",
            'main.call("_start_opera_from_room", room_id, index)',
            'main.callv("_start_opera_from_room", [room_id, index])',
            'Callable(main, "_start_opera_from_room").call(room_id, index)',
        )
        for bypass in bypasses:
            with self.subTest(bypass=bypass):
                path.write_text(original + bypass + "\n", encoding="utf-8")
                self.assertIn(
                    "probe_contract: direct main route bypass is forbidden",
                    audit.probe_contract_errors(self.source_root),
                )

    def test_duplicate_manifest_key_fails_closed(self) -> None:
        path = self.capture_root / "1280x720" / audit.MANIFEST_NAME
        raw = path.read_text(encoding="utf-8")
        path.write_text(raw.replace("{", '{\n  "schema": "spoof",', 1), encoding="utf-8")
        self.assertIn("manifest_read", self._codes())

    def test_unapproved_engine_version_string_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["engine"]["version_string"] = "4.7.1.stable.official.fixture"
        self._write_manifest("1280x720", manifest)
        self.assertIn("engine", self._codes())

    def test_changed_json_baseline_changes_capture_engine_evidence(self) -> None:
        baseline = copy.deepcopy(audit.capture_engine_evidence()["baseline"])
        with tempfile.TemporaryDirectory() as raw_path:
            path = Path(raw_path) / "godot_baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            original = audit.capture_engine_evidence(path)
            baseline["version"] = "4.7.3"
            baseline["release"] = "4.7.3-stable"
            for entry in baseline["downloads"].values():
                entry["filename"] = entry["filename"].replace(
                    "4.7.2-stable", "4.7.3-stable",
                )
            path.write_text(json.dumps(baseline), encoding="utf-8")
            changed = audit.capture_engine_evidence(path)
            self.assertEqual(changed["baseline"], baseline)
            self.assertNotEqual(
                original["canonical"], changed["canonical"],
            )
            self.assertEqual(
                changed["canonical"]["version_string"],
                "4.7.3-stable (official)",
            )

    def test_malformed_or_mismatched_capture_baseline_fails_closed(self) -> None:
        baseline = copy.deepcopy(audit.capture_engine_evidence()["baseline"])
        with tempfile.TemporaryDirectory() as raw_path:
            path = Path(raw_path) / "godot_baseline.json"
            path.write_text("{not-json", encoding="utf-8")
            with self.assertRaises(audit.godot_baseline.BaselineError):
                audit.capture_engine_evidence(path)
            baseline["release"] = "4.7.1-stable"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            with self.assertRaises(audit.godot_baseline.BaselineError):
                audit.capture_engine_evidence(path)

    def test_ancestor_hidden_route_is_forbidden(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "button.is_visible_in_tree()", "button.visible",
            ),
            encoding="utf-8",
        )
        errors = audit.validate_capture_root(self.capture_root, self.source_root)
        self.assertTrue(any(
            error == "probe_contract: missing button.is_visible_in_tree()"
            for error in errors
        ))

    def test_unbounded_frame_draw_await_is_forbidden(self) -> None:
        path = self.source_root / "scripts/probe_opera_art.gd"
        path.write_text(
            path.read_text(encoding="utf-8")
            + "await RenderingServer.frame_post_draw\n",
            encoding="utf-8",
        )
        errors = audit.validate_capture_root(self.capture_root, self.source_root)
        self.assertTrue(any(
            error == (
                "probe_contract: unbounded frame_post_draw await is forbidden"
            )
            for error in errors
        ))


if __name__ == "__main__":
    unittest.main()
