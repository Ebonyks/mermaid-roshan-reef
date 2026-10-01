#!/usr/bin/env python3
"""Append an explicitly selected cohort through the existing filler master.

Existing OGG bytes and historical provenance stay immutable. Local attempt
numbers are namespaced so a new batch cannot replace an older attempt record.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path

import audit_audio_quality as audit
import master_filler_voices as master

ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append(cohort: str, keys_file: Path, trials: Path, report_path: Path,
           selection_path: Path, archive: Path) -> None:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", cohort):
        raise ValueError("unsafe cohort ID")
    archive = archive.resolve()
    if ROOT / "assets_src" not in archive.parents or archive.exists():
        raise ValueError("archive must be a new directory below assets_src")
    keys = set(keys_file.read_text(encoding="utf-8").split())
    report = json.loads(report_path.read_text(encoding="utf-8"))
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    catalog = audit.authoritative_filler_lines(ROOT)
    if not keys or set(row["key"] for row in report) != keys:
        raise ValueError("selection report must cover exactly the requested cohort")
    for row in report:
        if row.get("status") != "SELECTED" or not isinstance(row.get("chosen"), dict):
            raise ValueError("cohort still needs retries: " + row["key"])
        if catalog[row["key"]] != (row["character"], row["expected"]):
            raise ValueError("cohort transcript does not match the authored catalog")
    out = ROOT / "assets/audio/voices/filler_v1"
    manifest_path = out / "FILLER_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if keys & {entry["key"] for entry in manifest["entries"]}:
        raise ValueError("append may not replace an existing filler entry")
    before = {path: master.sha256_file(path) for path in (ROOT / "assets/audio/voices").rglob("*")
              if path.is_file() and path.suffix.lower() in {".ogg", ".wav", ".mp3"}}
    trial_rows = json.loads((trials / "trial_manifest.json").read_text(encoding="utf-8"))
    if {row["key"] for row in trial_rows} != keys:
        raise ValueError("trial manifest includes keys outside the requested cohort")
    by_identity = {}
    local_candidates = {}
    for row in trial_rows:
        path = trials / Path(row["raw_path"]).name
        durable = master.candidate_row_with_hash(row, trials / "trial_manifest.json")
        identity = (int(row["attempt"]), row["key"], durable["raw_sha256"])
        by_identity[identity] = (durable, path)
        local_candidates[identity] = path
    evidence = master.selection_evidence(report, selection, local_candidates)
    with tempfile.TemporaryDirectory(prefix="append_filler_", dir=ROOT / "tmp") as temp:
        stage = Path(temp)
        rows = []
        for row in report:
            chosen = row["chosen"]
            identity = (int(chosen["attempt"]), row["key"], chosen["selected_raw_sha256"])
            source_meta, source = by_identity[identity]
            master.validate_selected_input(row, chosen, source_meta, source)
            if row["character"] not in {"roshan", "imp"}:
                raise ValueError("this cohort is limited to approved synthetic Roshan/imp presets")
            destination = stage / (row["key"] + ".ogg")
            metrics, command = master.master_source(source, destination)
            rows.append({
                "key": row["key"], "character": row["character"], "text": row["expected"],
                "status": "PROVISIONAL_SYNTHETIC_FILLER", "generation_cohort": cohort,
                "selected_attempt": chosen["attempt"], "seed": chosen["seed"],
                "mood": source_meta.get("mood"), "speaker_preset": source_meta["speaker"],
                "model": source_meta["model"], "model_revision": source_meta["model_revision"],
                "description_tokenizer_revision": source_meta["description_tokenizer_revision"],
                "description": source_meta["description"],
                "generation_text": " ".join(source_meta["generation_segments"]),
                "generation_segments": source_meta["generation_segments"],
                "segment_seeds": source_meta["segment_seeds"],
                "generation_prompt_capture_state": "CAPTURED_AT_GENERATION",
                "candidate_manifest_text": source_meta["text"],
                "candidate_manifest_generation_text": source_meta["generation_text"],
                "source_wav_sha256": master.sha256_file(source),
                "final_ogg_sha256": master.sha256_file(destination),
                "selection_metrics": {k: v for k, v in chosen.items() if k != "path"},
                "selected_input_provenance": {"validated": True, "attempt": chosen["attempt"],
                    "seed": chosen["seed"], "raw_sha256": master.sha256_file(source),
                    "candidate_path": (archive / source.name).relative_to(ROOT).as_posix(),
                    "candidate_manifest": (archive / "trial_manifest.json").relative_to(ROOT).as_posix()},
                "delivery_metrics": metrics, "ffmpeg_command": command,
            })
        # All takes and their unchanged generation run remain inspectable.
        archive.mkdir(parents=True)
        durable_rows = []
        for original, source in by_identity.values():
            shutil.copyfile(source, archive / source.name)
            original["raw_path"] = (archive / source.name).relative_to(ROOT).as_posix()
            durable_rows.append(original)
        write_json(archive / "trial_manifest.json", durable_rows)
        shutil.copyfile(trials / "run_provenance.json", archive / "run_provenance.json")
        shutil.copyfile(report_path, archive / "selection_report.json")
        shutil.copyfile(selection_path, archive / "selection_provenance.json")
        payload = json.loads((trials / "run_provenance.json").read_text(encoding="utf-8"))
        for attempt in sorted({int(row["attempt"]) for row in durable_rows}):
            run = payload.get("generation_runs", {}).get(str(attempt), payload)
            run_path = archive / f"run_provenance_attempt_{attempt}.json"
            write_json(run_path, run)
            candidates = [row for row in durable_rows if row["attempt"] == attempt]
            manifest["generation_run_provenance"][f"{cohort}_attempt_{attempt}"] = {
                "attempt": attempt, "capture_state": "CAPTURED_AT_GENERATION",
                "generator_sha256": run["generator_sha256"],
                "run_provenance_path": run_path.relative_to(ROOT).as_posix(),
                "run_provenance_sha256": master.sha256_file(run_path),
                "candidate_manifest_path": (archive / "trial_manifest.json").relative_to(ROOT).as_posix(),
                "candidate_manifest_sha256": master.sha256_file(archive / "trial_manifest.json"),
                "candidate_count": len(candidates), "candidate_rows": candidates,
                "candidate_rows_sha256": audit.canonical_json_sha256(candidates),
                "generation_run": run,
            }
        manifest["entries"].extend(rows)
        manifest["candidate_selection_evidence"].update(evidence)
        for key in keys:
            for candidate in manifest["candidate_selection_evidence"][key]["candidates"]:
                candidate["path"] = (archive / Path(candidate["path"]).name).relative_to(ROOT).as_posix()
        # Current pipeline identity changes only for the selector's new cohort option.
        selector_hash = master.normalized_text_sha256(ROOT / "tools/select_filler_voices.py")
        manifest["pipeline_script_sha256"]["tools/select_filler_voices.py"] = selector_hash
        manifest["pipeline_script_sha256"]["tools/make_parler_voice_trials.py"] = master.normalized_text_sha256(ROOT / "tools/make_parler_voice_trials.py")
        manifest["pipeline_script_sha256"]["tools/master_filler_voices.py"] = master.normalized_text_sha256(ROOT / "tools/master_filler_voices.py")
        manifest["selection_provenance"]["selector_sha256"] = selector_hash
        write_json(archive / "delivery_manifest.json", rows)
        # This is explicitly an append-time authority snapshot. Each native
        # candidate separately retains its actual generation segments.
        catalog_source = ROOT / "tools/opera_contest_voice_catalog.json"
        shutil.copyfile(catalog_source, archive / "catalog_at_append.json")
        write_json(archive / "CATALOG_PROVENANCE.json", {
            "capture_state": "AUTHORED_AUTHORITY_SNAPSHOT_AT_APPEND",
            "catalog_source": catalog_source.relative_to(ROOT).as_posix(),
            "catalog_snapshot": (archive / "catalog_at_append.json").relative_to(ROOT).as_posix(),
            "catalog_sha256": master.sha256_file(catalog_source),
            "append_tool_sha256": master.normalized_text_sha256(Path(__file__)),
            "keys": sorted(keys),
            "generation_text_authority": "Native candidate generation_segments in trial_manifest.json; no retrospective transcript substitution",
        })
        for path in stage.glob("*.ogg"):
            if (out / path.name).exists():
                raise ValueError("runtime destination appeared during mastering")
            shutil.copyfile(path, out / path.name)
        write_json(manifest_path, manifest)
    if any(master.sha256_file(path) != sha for path, sha in before.items()):
        raise ValueError("an existing voice changed during append")
    write_json(archive / "EXISTING_VOICES_UNCHANGED.json", {
        "status": "ALL_PREEXISTING_VOICE_BYTES_IDENTICAL",
        "files_count": len(before), "files": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": sha}
            for path, sha in sorted(before.items())],
        "scope": "Every OGG/WAV/MP3 already present before this cohort append",
    })
    with (ROOT / "ASSET_LICENSES.md").open("a", encoding="utf-8") as license_file:
        license_file.write(f"\n## Provisional voice cohort: {cohort} (2026-09-30)\n\n")
        license_file.write("| Asset | Source | License / URL | Modifications |\n|---|---|---|---|\n")
        for row in rows:
            license_file.write(f"| `assets/audio/voices/filler_v1/{row['key']}.ogg` | Synthetic Parler Mini v1.1 {row['speaker_preset']}; exact generation/ASR evidence in `{archive.relative_to(ROOT).as_posix()}` | Apache-2.0 model; https://huggingface.co/parler-tts/parler-tts-mini-v1.1 | 48 kHz mono Vorbis, mastered to -16 LUFS; provisional listening/device acceptance pending. |\n")
        for path in sorted(archive.glob("*.wav")):
            license_file.write(f"| `{path.relative_to(ROOT).as_posix()}` | Same synthetic contest cohort; immutable native candidate | Apache-2.0 model; https://huggingface.co/parler-tts/parler-tts-mini-v1.1 | None; source candidate preserved. |\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort", required=True)
    parser.add_argument("--keys-file", type=Path, required=True)
    parser.add_argument("--trials", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--selection-provenance", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    append(args.cohort, args.keys_file, args.trials, args.report,
           args.selection_provenance, args.archive)
    print("APPEND_FILLER|COMPLETE")
