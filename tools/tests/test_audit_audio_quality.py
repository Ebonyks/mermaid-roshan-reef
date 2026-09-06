import importlib.util
import hashlib
import gzip
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "audit_audio_quality", ROOT / "tools" / "audit_audio_quality.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AudioQualityPolicyTests(unittest.TestCase):
    def test_source_hash_is_stable_across_checkout_line_endings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tool.py"
            path.write_bytes(b"print('one')\r\nprint('two')\r\n")
            crlf_hash = MODULE.normalized_text_sha256(path)
            path.write_bytes(b"print('one')\nprint('two')\n")
            self.assertEqual(MODULE.normalized_text_sha256(path), crlf_hash)

    def test_embedded_generation_rows_support_clean_clone_without_tmp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool = root / "tools" / "generator.py"
            tool.parent.mkdir(parents=True)
            tool.write_text("print('voice')\n", encoding="utf-8")
            candidate_rows = [{"attempt": 3, "key": "roshan_win", "seed": 7}]
            run = {
                "attempt": 3,
                "capture_state": "CAPTURED_AT_GENERATION",
                "generator_sha256": "1" * 64,
                "run_provenance_path": "tmp/attempt_3/run_provenance.json",
                "run_provenance_sha256": "2" * 64,
                "candidate_manifest_path": "tmp/attempt_3/trial_manifest.json",
                "candidate_manifest_sha256": "3" * 64,
                "candidate_count": 1,
                "candidate_rows": candidate_rows,
                "candidate_rows_sha256": MODULE.canonical_json_sha256(candidate_rows),
            }
            manifest = {
                "pipeline_hash_mode": "utf8_lf",
                "pipeline_script_sha256": {
                    "tools/generator.py": MODULE.normalized_text_sha256(tool),
                },
            }
            issues = []
            MODULE.validate_generation_evidence(
                root, manifest, [], {"attempt_3": run}, issues)
            self.assertEqual(issues, [])

            run["candidate_rows"][0]["seed"] = 8
            issues = []
            MODULE.validate_generation_evidence(
                root, manifest, [], {"attempt_3": run}, issues)
            self.assertTrue(any(
                "embedded candidate rows hash mismatch" in issue
                for issue in issues))

    def test_everyone_component_rejects_semantic_pitch_and_silence_outliers(self):
        component = {
            "character": "evie",
            "text": "Hooray!",
            "generation_text": "We did it! Yay!",
            "selection_evidence": {"selection": {
                "f0_median_hz": 65.0,
                "duration_s": 11.9815,
                "active_duration_s": 0.68,
                "voiced_frame_fraction": 0.0976,
                "semantic_gate_expected_words": ["hooray"],
                "semantic_gate_transcript_words": ["whee", "did", "it", "yay"],
            }},
        }
        issues = MODULE.group_component_issues(component)
        self.assertTrue(any("F0 out of range" in issue for issue in issues))
        self.assertTrue(any("active-speech bounds failed" in issue for issue in issues))
        self.assertTrue(any("semantic identity mismatch" in issue for issue in issues))

    def test_protected_inventory_is_explicit(self):
        self.assertEqual(len(MODULE.PROTECTED), 6)
        self.assertNotIn("assets/audio/voice_yay.mp3", MODULE.PROTECTED)
        self.assertIn("assets/audio/voices/chuck_whimper.ogg", MODULE.PROTECTED)
        self.assertIn("assets/audio/voices/daddy1.ogg", MODULE.PROTECTED)

    def test_legacy_low_music_is_not_upgraded_by_metadata(self):
        meta = {"decode_ok": True, "duration_seconds": 8.0}
        for path in MODULE.LEGACY_LOW_MUSIC:
            self.assertEqual(
                MODULE.grade(path, meta, -8.0),
                ("D", 2, "P2", "LISTEN_REPLACE_CANDIDATE"),
            )

    def test_provisional_yay_has_no_fabricated_human_grade(self):
        meta = {"decode_ok": True, "duration_seconds": 1.0}
        self.assertEqual(
            MODULE.grade("assets/audio/voices/filler_v1/yay.ogg", meta, -6.0),
            ("A", "", "P1", "REVIEW_PROVISIONAL_FILLER"),
        )

    def test_teacher_lessons_are_voice_assets(self):
        self.assertEqual(
            MODULE.category("assets/audio/teacher/teacher_pattern.ogg"),
            "voice",
        )

    def _teacher_fixture(self, root):
        tools = root / "tools"
        tools.mkdir(parents=True)
        tools.joinpath("make_voices.py").write_text(
            "LINES = {'teacher_pattern': ('roshan', 'Find the pattern.'), "
            "'legacy_key': ('roshan', 'Legacy.')}\n",
            encoding="utf-8",
        )
        audio = root / "assets/audio/teacher/teacher_pattern.ogg"
        audio.parent.mkdir(parents=True)
        audio.write_bytes(b"teacher fixture")
        source = tools.joinpath("make_voices.py").read_bytes()
        snapshot = root / MODULE.TEACHER_SOURCE_SNAPSHOT_REL
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(gzip.compress(source, mtime=0))
        manifest = {
            "schema_version": 1,
            "generator": {
                "script": "tools/make_voices.py",
                "script_sha256": hashlib.sha256(source).hexdigest(),
                "speaker_config": {
                    "character": "roshan", "voice": "af_heart",
                    "pitch_factor": 1.24, "speed": 1.02,
                },
            },
            "source_provenance": dict(MODULE.TEACHER_SOURCE_PROVENANCE),
            "delivery": {
                "directory": "assets/audio/teacher", "sample_rate_hz": 48000,
                "channels": 1, "codec": "vorbis", "target_lufs": -16.0,
                "true_peak_limit_dbtp": -1.5, "files_count": 17,
            },
            "entries": [{
                "key": "teacher_pattern", "speaker": "roshan",
                "text": "Find the pattern.",
                "kokoro_voice": "af_heart", "pitch_factor": 1.24, "speed": 1.02,
                "source_line_table": "tools/make_voices.py:LINES",
                "source_text_sha256": hashlib.sha256(b"Find the pattern.").hexdigest(),
                "output_path": "assets/audio/teacher/teacher_pattern.ogg",
                "output_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
                "output_bytes": len(audio.read_bytes()),
            }],
        }
        manifest_path = root / MODULE.TEACHER_MANIFEST_REL
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return audio, manifest_path

    def test_teacher_manifest_separates_keys_from_filler_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._teacher_fixture(root)
            state = MODULE.validate_teacher_manifest(root)
            self.assertFalse(any(
                "teacher_pattern.ogg" in issue and "media decode" not in issue
                for issue in state["issues"]))
            authority = MODULE.authoritative_filler_lines(
                root, set(state["declared_keys"]))
            self.assertNotIn("teacher_pattern", authority)

    def test_teacher_manifest_blocks_missing_and_mismatched_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            audio, manifest_path = self._teacher_fixture(root)
            audio.unlink()
            state = MODULE.validate_teacher_manifest(root)
            self.assertTrue(any("missing OGG" in issue for issue in state["issues"]))
            audio.write_bytes(b"changed teacher fixture")
            state = MODULE.validate_teacher_manifest(root)
            self.assertTrue(any("hash mismatch" in issue for issue in state["issues"]))

    def test_teacher_manifest_blocks_schema_text_and_speaker_mutations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _audio, manifest_path = self._teacher_fixture(root)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["schema_version"] = 2
            manifest["generator"]["speaker_config"]["voice"] = "wrong"
            manifest["entries"][0]["source_text_sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            issues = MODULE.validate_teacher_manifest(root)["issues"]
            self.assertTrue(any("schema_version" in issue for issue in issues))
            self.assertTrue(any("speaker_config" in issue for issue in issues))
            self.assertTrue(any("source_text_sha256" in issue for issue in issues))

    def test_teacher_manifest_blocks_weight_and_identity_provenance_mutations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _audio, manifest_path = self._teacher_fixture(root)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["source_provenance"]["model_sha256"] = "0" * 64
            manifest["source_provenance"]["voices_sha256"] = "1" * 64
            manifest["source_provenance"]["voice_identity"] = "unverified"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            issues = MODULE.validate_teacher_manifest(root)["issues"]
            self.assertTrue(any("model_sha256" in issue for issue in issues))
            self.assertTrue(any("voices_sha256" in issue for issue in issues))
            self.assertTrue(any("voice_identity" in issue for issue in issues))

    def test_teacher_manifest_blocks_clipping_and_peak_even_when_claimed_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._teacher_fixture(root)
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            old_signal = MODULE.decoded_signal
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 0.0, -0.5)
            MODULE.decoded_signal = lambda _path: {
                "decode_ok": True, "duration_s": 1.0,
                "decoded_peak_linear": 1.0, "decoded_clipped_samples": 3,
                "decoded_rms_dbfs": -16.0,
            }
            try:
                issues = MODULE.validate_teacher_manifest(root)["issues"]
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
                MODULE.decoded_signal = old_signal
            self.assertTrue(any("has decoded clipped samples: 3" in issue for issue in issues))
            self.assertTrue(any("true peak exceeds" in issue for issue in issues))

    def test_teacher_manifest_rejects_nested_and_noncohort_ogg(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._teacher_fixture(root)
            nested = root / "assets/audio/teacher/nested/legacy.ogg"
            nested.parent.mkdir(parents=True)
            nested.write_bytes(b"nested")
            issues = MODULE.validate_teacher_manifest(root)["issues"]
            self.assertTrue(any("nested/legacy.ogg" in issue for issue in issues))
            authority = MODULE.authoritative_filler_lines(root, {"legacy_key"})
            self.assertIn("teacher_pattern", authority)
            self.assertIn("legacy_key", authority)

    def test_clipping_precedes_other_dispositions(self):
        meta = {"decode_ok": True, "duration_seconds": 1.0}
        self.assertEqual(
            MODULE.grade("assets/audio/ui_tap.ogg", meta, 0.1),
            ("F", 1, "P1", "REPLACE_CLIPPING"),
        )

    def test_new_exact_racer_voices_are_review_gated(self):
        meta = {"decode_ok": True, "duration_seconds": 2.0}
        for path in MODULE.NEW_EXACT_VOICES:
            self.assertEqual(
                MODULE.grade(path, meta, -2.0),
                ("A", 4, "P1", "REVIEW_NEW_EXACT_VOICE"),
            )

    def test_faron_is_protected_by_speaker_and_filler_is_not(self):
        self.assertEqual(
            MODULE.protected_kind("assets/audio/voices/faron_op_nursery_bedtime.ogg"),
            "protected_faron",
        )
        self.assertIsNone(
            MODULE.protected_kind("assets/audio/voices/filler_v1/faron_fake.ogg"))

    def test_filler_manifest_absence_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            state = MODULE.validate_filler_manifest(Path(directory))
        self.assertFalse(state["present"])
        self.assertFalse(state["blocking"])

    def test_filler_manifest_validates_set_hash_and_delivery_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            audio = filler / "roshan_win.ogg"
            audio.write_bytes(b"fixture ogg")
            payload = {
                "entries": [{
                    "key": "roshan_win",
                    "character": "roshan", "text": "Yay! I did it!",
                    "status": "PROVISIONAL_SYNTHETIC_FILLER",
                    "selected_attempt": 1, "generation_text": "Yay! I did it!",
                    "generation_segments": ["Yay! I did it!"],
                    "segment_seeds": [1], "source_wav_sha256": "1" * 64,
                    "speaker_preset": "Laura", "description": "fixture",
                    "selection_metrics": {
                        "semantic_gate_schema": 3,
                        "semantic_gate_expected_words": ["yay", "i", "did", "it"],
                        "semantic_gate_transcript_words": ["yay", "i", "did", "it"],
                        "attempt": 1, "seed": 1,
                        "source_sha256": "1" * 64,
                        "selected_raw_sha256": "1" * 64,
                    },
                    "final_ogg_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
                    "delivery_metrics": {
                        "codec": "vorbis", "sample_rate_hz": 48000,
                        "channels": 1, "bit_rate_bps": 96000,
                        "integrated_lufs": -16.0, "true_peak_dbtp": -2.0,
                        "duration_s": 1.0, "decoded_clipped_samples": 0,
                        "decoded_peak_linear": 0.2, "dc_offset": 0.0,
                    },
                    "seed": 1,
                    "ffmpeg_command": [
                        "ffmpeg", "-serial_offset",
                        str(MODULE._expected_ogg_serial("roshan_win")),
                    ],
                }],
                "generation_run_provenance": {"attempt_1": {"attempt": 1}},
            }
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps(payload), encoding="utf-8")
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            old_signal, old_serials = MODULE.decoded_signal, MODULE.ogg_serials
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            MODULE.decoded_signal = lambda _path: {
                "decode_ok": True, "duration_s": 1.0,
                "decoded_peak_linear": 0.2, "decoded_clipped_samples": 0,
                "dc_offset": 0.0,
            }
            MODULE.ogg_serials = lambda _path: ({MODULE._expected_ogg_serial("roshan_win")}, None)
            try:
                state = MODULE.validate_filler_manifest(root, {
                    "roshan_win": ("roshan", "Yay! I did it!"),
                })
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
                MODULE.decoded_signal, MODULE.ogg_serials = old_signal, old_serials
        self.assertTrue(state["present"])
        self.assertFalse(state["blocking"], state["issues"])

    def test_filler_manifest_rejects_unlisted_ogg_and_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            listed = filler / "roshan_win.ogg"
            listed.write_bytes(b"fixture ogg")
            (filler / "unlisted.ogg").write_bytes(b"extra")
            payload = {"entries": [{
                "key": "roshan_win", "final_ogg_sha256": "0" * 64,
                "delivery_metrics": {
                    "codec": "vorbis", "sample_rate_hz": 48000,
                    "channels": 1, "bit_rate_bps": 96000,
                    "integrated_lufs": -16.0, "true_peak_dbtp": -2.0,
                },
            }]}
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps(payload), encoding="utf-8")
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            try:
                state = MODULE.validate_filler_manifest(root, {
                    "roshan_win": ("roshan", "Yay! I did it!"),
                })
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
        self.assertTrue(state["blocking"])
        self.assertTrue(any("unlisted filler OGG" in issue for issue in state["issues"]))
        self.assertTrue(any("hash mismatch" in issue for issue in state["issues"]))

    def test_manifest_only_fake_ogg_cannot_pass_media_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            fake = filler / "roshan_win.ogg"
            fake.write_bytes(b"not an ogg page")
            payload = {"entries": [{
                "key": "roshan_win", "character": "roshan",
                "text": "Yay! I did it!", "status": "PROVISIONAL_SYNTHETIC_FILLER",
                "selected_attempt": 1, "seed": 1,
                "generation_text": "Yay! I did it!", "generation_segments": ["Yay! I did it!"],
                "segment_seeds": [1], "source_wav_sha256": "1" * 64,
                "speaker_preset": "Laura", "description": "fixture",
                "selection_metrics": {
                    "semantic_gate_schema": 3,
                    "semantic_gate_expected_words": ["yay", "i", "did", "it"],
                    "semantic_gate_transcript_words": ["yay", "i", "did", "it"],
                    "attempt": 1, "seed": 1,
                    "source_sha256": "1" * 64, "selected_raw_sha256": "1" * 64,
                },
                "final_ogg_sha256": hashlib.sha256(fake.read_bytes()).hexdigest(),
                "delivery_metrics": {
                    "codec": "vorbis", "sample_rate_hz": 48000, "channels": 1,
                    "bit_rate_bps": 96000, "integrated_lufs": -16.0,
                    "true_peak_dbtp": -2.0, "duration_s": 1.0,
                    "decoded_clipped_samples": 0, "decoded_peak_linear": 0.2,
                    "dc_offset": 0.0,
                },
                "ffmpeg_command": [
                    "ffmpeg", "-serial_offset",
                    str(MODULE._expected_ogg_serial("roshan_win")),
                ],
            }], "generation_run_provenance": {"attempt_1": {"attempt": 1}}}
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps(payload), encoding="utf-8")
            old_probe, old_loudness, old_signal = MODULE.probe, MODULE.loudness, MODULE.decoded_signal
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            MODULE.decoded_signal = lambda _path: {
                "decode_ok": True, "duration_s": 1.0,
                "decoded_peak_linear": 0.2, "decoded_clipped_samples": 0,
                "dc_offset": 0.0,
            }
            try:
                state = MODULE.validate_filler_manifest(root, {
                    "roshan_win": ("roshan", "Yay! I did it!"),
                })
            finally:
                MODULE.probe, MODULE.loudness, MODULE.decoded_signal = old_probe, old_loudness, old_signal
        self.assertTrue(state["blocking"])
        self.assertTrue(any("Ogg parse failed" in issue for issue in state["issues"]))

    def test_selected_source_provenance_mismatch_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            audio = filler / "roshan_win.ogg"
            audio.write_bytes(b"fixture ogg")
            payload = {"entries": [{
                "key": "roshan_win", "character": "roshan", "text": "Yay! I did it!",
                "status": "PROVISIONAL_SYNTHETIC_FILLER", "selected_attempt": 2, "seed": 9,
                "generation_text": "Yay! I did it!", "generation_segments": ["Yay! I did it!"],
                "segment_seeds": [9], "source_wav_sha256": "1" * 64,
                "speaker_preset": "Laura", "description": "fixture",
                "selection_metrics": {
                    "semantic_gate_schema": 3,
                    "semantic_gate_expected_words": ["yay", "i", "did", "it"],
                    "semantic_gate_transcript_words": ["yay", "i", "did", "it"],
                    "attempt": 1, "seed": 8,
                    "source_sha256": "2" * 64, "selected_raw_sha256": "2" * 64,
                },
                "final_ogg_sha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
                "delivery_metrics": {
                    "codec": "vorbis", "sample_rate_hz": 48000, "channels": 1,
                    "bit_rate_bps": 96000, "integrated_lufs": -16.0,
                    "true_peak_dbtp": -2.0, "duration_s": 1.0,
                    "decoded_clipped_samples": 0, "decoded_peak_linear": 0.2,
                    "dc_offset": 0.0,
                },
                "ffmpeg_command": [
                    "ffmpeg", "-serial_offset",
                    str(MODULE._expected_ogg_serial("roshan_win")),
                ],
            }], "generation_run_provenance": {"attempt_2": {"attempt": 2}}}
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps(payload), encoding="utf-8")
            old_probe, old_loudness, old_signal, old_serials = (
                MODULE.probe, MODULE.loudness, MODULE.decoded_signal, MODULE.ogg_serials)
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            MODULE.decoded_signal = lambda _path: {
                "decode_ok": True, "duration_s": 1.0,
                "decoded_peak_linear": 0.2, "decoded_clipped_samples": 0,
                "dc_offset": 0.0,
            }
            MODULE.ogg_serials = lambda _path: ({MODULE._expected_ogg_serial("roshan_win")}, None)
            try:
                state = MODULE.validate_filler_manifest(root, {
                    "roshan_win": ("roshan", "Yay! I did it!"),
                })
            finally:
                MODULE.probe, MODULE.loudness, MODULE.decoded_signal, MODULE.ogg_serials = (
                    old_probe, old_loudness, old_signal, old_serials)
        self.assertTrue(state["blocking"])
        self.assertTrue(any("source_wav_sha256" in issue for issue in state["issues"]))
        self.assertTrue(any("selected attempt" in issue for issue in state["issues"]))

    def test_filler_manifest_rejects_incomplete_authoritative_cohort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            filler = root / "assets/audio/voices/filler_v1"
            filler.mkdir(parents=True)
            (filler / "FILLER_MANIFEST.json").write_text(
                json.dumps({"entries": [], "generation_run_provenance": {}}),
                encoding="utf-8",
            )
            state = MODULE.validate_filler_manifest(root, {
                "roshan_talk": ("roshan", "This is so much fun!"),
                "yay": ("roshan", "Yay!"),
            })
        self.assertTrue(state["blocking"])
        self.assertTrue(any(
            "authoritative filler key missing" in issue for issue in state["issues"]))

    def test_daddy_filler_allowlist_is_contextual_and_bounded(self):
        self.assertTrue({
            "daddy_hide_seek_start", "daddy_hide_seek_found", "daddy_hide_seek_visit",
        }.issubset(MODULE.ALLOWED_DADDY_FILLERS))
        self.assertNotIn("daddy_talk", MODULE.ALLOWED_DADDY_FILLERS)
        self.assertNotIn("daddy_win", MODULE.ALLOWED_DADDY_FILLERS)

    def test_filler_rows_are_distinct_and_mark_legacy_shadowing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            voice_dir = root / "assets/audio/voices"
            filler = voice_dir / "filler_v1"
            filler.mkdir(parents=True)
            (voice_dir / "roshan_win.ogg").write_bytes(b"legacy")
            (filler / "roshan_win.ogg").write_bytes(b"filler")
            old_probe, old_loudness = MODULE.probe, MODULE.loudness
            MODULE.probe = lambda _path: {
                "decode_ok": True, "codec": "vorbis", "sample_rate_hz": 48000,
                "channels": 1, "bitrate_kbps": 96.0, "duration_seconds": 1.0,
            }
            MODULE.loudness = lambda _path: (-16.0, 1.0, -2.0)
            try:
                rows = MODULE.build_rows(root, {
                    "present": True, "blocking": False,
                    "expected_names": {"roshan_win.ogg"},
                })
            finally:
                MODULE.probe, MODULE.loudness = old_probe, old_loudness
        by_path = {row["path"]: row for row in rows}
        self.assertEqual(by_path["assets/audio/voices/filler_v1/roshan_win.ogg"]["cohort"], "filler_v1")
        self.assertEqual(by_path["assets/audio/voices/roshan_win.ogg"]["cohort"], "legacy_voice")
        self.assertEqual(
            by_path["assets/audio/voices/roshan_win.ogg"]["shadowed_by_filler_path"],
            "assets/audio/voices/filler_v1/roshan_win.ogg",
        )


if __name__ == "__main__":
    unittest.main()
