from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "day_one_contextual_parler_cohort.py"


def load_module():
    spec = importlib.util.spec_from_file_location("day_one_contextual_parler_cohort", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cohort = load_module()


class ContextualCohortTests(unittest.TestCase):
    def make_catalog(self, directory: Path) -> Path:
        path = directory / "catalog.json"
        path.write_text(json.dumps({
            "schema_version": 1, "speaker": "roshan", "allow_generic": False,
            "rows": [{
                "cue_id": "day1_test_cue", "route": "pool",
                "moment": "Test visible action", "caption": "The pool is shiny!",
                "audio_path": "assets/audio/voices/filler_v1/day1_test_cue.ogg",
                "status": "PENDING_GENERATION", "policy": "once_per_session",
            }],
        }), encoding="utf-8")
        return path

    def test_scope_rejects_faron_and_non_tmp_candidates(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            catalog = self.make_catalog(directory)
            with mock.patch.object(cohort, "TMP_DIR", directory / "tmp"):
                plan = cohort.make_plan(catalog, directory / "tmp" / "candidates", 3)
            self.assertEqual(plan["status"], "PLANNED_NO_MODEL_RUN")
            self.assertFalse(plan["scope"]["runtime_writes"])
            with self.assertRaises(ValueError):
                cohort.resolve_inside(directory / "runtime", directory / "tmp")
            bad = json.loads(catalog.read_text(encoding="utf-8"))
            bad["rows"][0]["cue_id"] = "faron_test"
            bad_path = directory / "bad.json"
            bad_path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(ValueError):
                cohort.load_pending(bad_path)

    def test_plan_preserves_one_cue_one_caption_identity(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            catalog = self.make_catalog(directory)
            with mock.patch.object(cohort, "TMP_DIR", directory / "tmp"):
                plan = cohort.make_plan(catalog, directory / "tmp" / "candidates", 2)
            row = plan["rows"][0]
            self.assertEqual(row["cue_id"], "day1_test_cue")
            self.assertEqual(row["caption"], "The pool is shiny!")
            self.assertEqual(row["candidate_files"], [
                "day1_test_cue__attempt_1.wav", "day1_test_cue__attempt_2.wav",
            ])

    def test_report_rejects_caption_drift_and_extra_keys(self):
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            catalog = self.make_catalog(directory)
            _document, rows = cohort.load_pending(catalog)
            report = directory / "report.json"
            report.write_text(json.dumps([{
                "key": "day1_test_cue", "expected": "A different line",
                "status": "SELECTED", "chosen": {"attempt": 1},
            }]), encoding="utf-8")
            with self.assertRaises(ValueError):
                cohort.load_report(report, rows)

    def test_license_append_is_idempotence_guarded(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "ASSET_LICENSES.md"
            path.write_text("# Licenses\n", encoding="utf-8")
            digest = "a" * 64
            rows = [{
                "cue_id": "day1_test_cue",
                "audio_path": "assets/audio/voices/filler_v1/roshan_day1_test_cue.ogg",
            }]
            cohort.append_license_rows(path, rows, digest)
            text = path.read_text(encoding="utf-8")
            self.assertIn("day1_test_cue", text)
            with self.assertRaises(ValueError):
                cohort.append_license_rows(path, rows, digest)

    def test_append_master_preserves_existing_entries_and_audio_format(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            runtime = root / "assets" / "audio" / "voices" / "filler_v1"
            runtime.mkdir(parents=True)
            (root / "assets" / "audio" / "voices").joinpath("faron1.ogg").write_bytes(b"FARON")
            existing = {"key": "legacy", "text": "Keep me"}
            manifest_path = runtime / "FILLER_MANIFEST.json"
            manifest_path.write_text(json.dumps({"manifest_schema": 3, "entries": [existing]}), encoding="utf-8")
            licenses = root / "ASSET_LICENSES.md"
            licenses.write_text("# Licenses\n", encoding="utf-8")
            catalog = self.make_catalog(root)
            trials = root / "tmp" / "trials" / "attempt_1"
            trials.mkdir(parents=True)
            source = trials / "day1_test_cue.wav"
            sample_rate = 24000
            samples = []
            noise_state = 17
            for i in range(sample_rate * 2):
                noise_state = (1664525 * noise_state + 1013904223) & 0xFFFFFFFF
                noise = ((noise_state / 0xFFFFFFFF) * 2.0 - 1.0) * 900.0
                tone = 7000.0 * math.sin(2 * math.pi * 220 * i / sample_rate)
                overtone = 1800.0 * math.sin(2 * math.pi * 733 * i / sample_rate)
                samples.append(int(tone + overtone + noise))
            with wave.open(str(source), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(int(value).to_bytes(2, "little", signed=True) for value in samples))
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            trial_manifest = [{
                "key": "day1_test_cue", "character": "roshan", "text": "The pool is shiny!",
                "generation_text": "The pool is shiny!", "generation_segments": ["The pool is shiny!"],
                "segment_seeds": [1], "mood": "celebrate", "speaker": "Joy",
                "model": "parler-tts/parler-tts-mini-v1.1", "model_revision": "test",
                "description_tokenizer_revision": "test", "attempt": 1, "seed": 1,
                "raw_path": str(source), "raw_sha256": source_hash,
            }]
            (trials / "trial_manifest.json").write_text(json.dumps(trial_manifest), encoding="utf-8")
            report = root / "tmp" / "report.json"
            report.write_text(json.dumps([{
                "key": "day1_test_cue", "expected": "The pool is shiny!", "status": "SELECTED",
                "chosen": {"attempt": 1, "seed": 1, "selected_raw_sha256": source_hash},
            }]), encoding="utf-8")
            provenance = root / "tmp" / "provenance.json"
            with mock.patch.object(cohort, "ROOT", root), \
                    mock.patch.object(cohort, "RUNTIME_DIR", runtime), \
                    mock.patch.object(cohort, "TMP_DIR", root / "tmp"):
                result = cohort.master_append(catalog, report, root / "tmp" / "trials",
                                              runtime, provenance, licenses)
            self.assertEqual(result["status"], "APPENDED_AFTER_SELECTION")
            merged = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(merged["entries"][0], existing)
            new_entry = merged["entries"][1]
            self.assertEqual(new_entry["key"], "day1_test_cue")
            self.assertEqual(new_entry["delivery_metrics"]["codec"], "vorbis")
            self.assertEqual(new_entry["delivery_metrics"]["sample_rate_hz"], 48000)
            self.assertEqual(new_entry["delivery_metrics"]["channels"], 1)
            self.assertGreaterEqual(new_entry["delivery_metrics"]["bit_rate_bps"], 64000)
            self.assertTrue((runtime / "day1_test_cue.ogg").is_file())
            self.assertTrue(provenance.is_file())
            self.assertIn("day1_test_cue", licenses.read_text(encoding="utf-8"))
            self.assertEqual((root / "assets" / "audio" / "voices" / "faron1.ogg").read_bytes(), b"FARON")


if __name__ == "__main__":
    unittest.main()
