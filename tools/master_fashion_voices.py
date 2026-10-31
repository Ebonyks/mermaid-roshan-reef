"""Master the bounded Roshan Fashion Designer cohort with the established gates."""
from __future__ import annotations
import argparse
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--selection-provenance", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    args = parser.parse_args()
    tmp_root = (ROOT / "tmp").resolve()
    for path in (args.report, args.selection_provenance, args.candidates):
        if not path.resolve().is_relative_to(tmp_root):
            parser.error("all build inputs must stay under this checkout's tmp/")
    destination = ROOT / "assets/audio/fashion"
    if destination.exists():
        parser.error("fashion delivery exists; preserve it before an explicit remaster")
    spec = importlib.util.spec_from_file_location("fashion_master", ROOT / "tools/master_filler_voices.py")
    assert spec and spec.loader
    master = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(master)
    report = json.loads(args.report.read_text(encoding="utf-8"))
    if not report or any(r["status"] != "SELECTED" or r["character"] != "roshan"
                         or not r["key"].startswith("roshan_fashion_") for r in report):
        parser.error("only a complete selected Roshan fashion cohort can ship")
    selection = json.loads(args.selection_provenance.read_text(encoding="utf-8"))
    candidates, metadata, runs = {}, {}, {}
    for manifest in sorted(args.candidates.glob("attempt_*/*manifest.json")):
        rows = json.loads(manifest.read_text(encoding="utf-8"))
        run_path = manifest.with_name("run_provenance.json")
        if not run_path.is_file():
            parser.error("generation-time run provenance is required")
        captured = json.loads(run_path.read_text(encoding="utf-8"))
        verified = [master.candidate_row_with_hash(row, manifest) for row in rows]
        durable = [dict(row) for row in rows]
        for row, enriched in zip(rows, durable):
            raw = manifest.parent / Path(row["raw_path"]).name
            identity = (int(row["attempt"]), str(row["key"]), str(row["raw_sha256"]).lower())
            candidates[identity] = raw
            metadata[identity] = row
        for attempt in sorted({int(row["attempt"]) for row in rows}):
            captured_rows = [row for row in durable if int(row["attempt"]) == attempt]
            runs[f"attempt_{attempt}"] = captured | {
                "attempt": attempt, "capture_state": "CAPTURED_AT_GENERATION",
                "candidate_manifest_path": master.root_relative(manifest),
                "candidate_manifest_sha256": master.sha256_file(manifest),
                "candidate_count": len(captured_rows), "candidate_rows": captured_rows,
                "candidate_rows_sha256": master.canonical_json_sha256(captured_rows),
                "run_provenance_path": master.root_relative(run_path),
                "run_provenance_sha256": master.sha256_file(run_path),
            }
    evidence = master.selection_evidence(report, selection, candidates)
    protected = master.committed_protected_hashes()
    entries = []
    with tempfile.TemporaryDirectory(prefix="fashion_master_", dir=tmp_root) as work:
        stage = Path(work)
        for row in report:
            chosen = row["chosen"]
            identity = (int(chosen["attempt"]), row["key"], chosen["selected_raw_sha256"].lower())
            source, meta = candidates[identity], metadata[identity]
            master.validate_selected_input(row, chosen, meta, source)
            if master.sha256_file(source) != meta["raw_sha256"]:
                raise ValueError("selected raw hash drift")
            output = stage / (row["key"] + ".ogg")
            metrics, command = master.master_source(source, output)
            entries.append({
                "key": row["key"], "character": "roshan", "text": row["expected"],
                "status": "PROVISIONAL_SYNTHETIC_FILLER", "selected_attempt": chosen["attempt"],
                "seed": chosen["seed"], "mood": meta["mood"], "speaker_preset": meta["speaker"],
                "model": meta["model"], "model_revision": meta["model_revision"],
                "description_tokenizer_revision": meta["description_tokenizer_revision"],
                "description": meta["description"], "generation_text": meta["generation_text"],
                "generation_segments": meta["generation_segments"], "segment_seeds": meta["segment_seeds"],
                "generation_prompt_capture_state": "CAPTURED_AT_GENERATION",
                "candidate_manifest_text": meta["text"], "candidate_manifest_generation_text": meta["generation_text"],
                "selection_metrics": {k: v for k, v in chosen.items() if k != "path"},
                "selected_input_provenance": {"candidate_path": master.root_relative(source),
                    "candidate_manifest": master.root_relative(source.parent / "trial_manifest.json"),
                    "attempt": chosen["attempt"], "seed": chosen["seed"],
                    "raw_sha256": identity[2], "validated": True},
                "source_wav_sha256": identity[2], "final_ogg_sha256": master.sha256_file(output),
                "delivery_metrics": metrics, "ffmpeg_command": command,
            })
            print("FASHION_MASTER|" + row["key"] + "|PASS", flush=True)
        manifest = {"manifest_schema": 3, "status": "PROVISIONAL_SYNTHETIC_FILLER",
            "protected_recordings_modified": False, "faron_modified": False,
            "protected_recording_hashes": protected, "generation_run_provenance": runs,
            "generation_attempt_count": len(runs), "candidate_selection_evidence": evidence,
            "selection_provenance": selection, "selection_report": {
                "path": master.root_relative(args.report), "sha256": master.sha256_file(args.report)},
            "pipeline_hash_mode": "utf8_lf", "pipeline_script_sha256": {
                rel: master.normalized_text_sha256(ROOT / rel) for rel in [
                    "tools/make_parler_voice_trials.py", "tools/select_filler_voices.py",
                    "tools/master_filler_voices.py", "tools/master_fashion_voices.py"]},
            "codec_target": "48 kHz mono Ogg Vorbis 96 kbps, -16 LUFS +/-1, <= -1.5 dBTP",
            "human_review": "PENDING", "device_review": "PENDING", "entries": entries}
        (stage / "FASHION_VOICE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if master.committed_protected_hashes() != protected:
            raise ValueError("protected voice hash drift during mastering")
        shutil.copytree(stage, destination)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
