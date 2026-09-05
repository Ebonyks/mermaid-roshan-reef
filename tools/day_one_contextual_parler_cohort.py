#!/usr/bin/env python3
"""Bounded, append-only Parler cohort flow for frozen Day One voice rows.

Planning and generation are deliberately separate from delivery.  The plan
and raw candidates live below ``tmp/``.  The ``master`` command is the only
operation that may add runtime OGGs, and it requires a complete selection
report whose keys/transcripts exactly match the catalog's
``PENDING_GENERATION`` rows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import importlib.util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT
DEFAULT_CATALOG = ROOT / "audit" / "DAY_ONE_CONTEXTUAL_VOICE_COVERAGE_2026-09-01.json"
DEFAULT_TRIALS = ROOT / "tmp" / "day_one_contextual_parler_trials"
DEFAULT_SELECTED = ROOT / "tmp" / "day_one_contextual_parler_selected"
DEFAULT_REPORT = ROOT / "tmp" / "day_one_contextual_parler_selection_report.json"
DEFAULT_PROVENANCE = ROOT / "tmp" / "day_one_contextual_parler_selection_provenance.json"
RUNTIME_DIR = ROOT / "assets" / "audio" / "voices" / "filler_v1"
TMP_DIR = ROOT / "tmp"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,96}$")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_text_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(text.encode("utf-8"))


def canonical_sha(value: object) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":")).encode("utf-8"))


def resolve_inside(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    root = parent.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"path must be below {root}: {path}")
    return resolved


def portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def load_pending(catalog_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = json.loads(catalog_path.read_text(encoding="utf-8"))
    if document.get("speaker") != "roshan" or document.get("allow_generic") is not False:
        raise ValueError("catalog is not the fail-closed Roshan contextual catalog")
    rows = [dict(row) for row in document.get("rows", [])
            if row.get("status") == "PENDING_GENERATION"]
    if not rows:
        raise ValueError("catalog contains no PENDING_GENERATION rows")
    seen: set[str] = set()
    for row in rows:
        cue_id = str(row.get("cue_id", ""))
        caption = str(row.get("caption", ""))
        route = str(row.get("route", ""))
        if not ID_RE.fullmatch(cue_id):
            raise ValueError(f"invalid contextual cue_id: {cue_id!r}")
        if cue_id in seen:
            raise ValueError(f"duplicate contextual cue_id: {cue_id}")
        if not caption.strip() or not route.strip():
            raise ValueError(f"contextual row is missing caption/route: {cue_id}")
        if cue_id.startswith("faron") or "faron" in route.lower():
            raise ValueError(f"Faron row is forbidden in contextual cohort: {cue_id}")
        seen.add(cue_id)
    return document, rows


def row_identity(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "cue_id": str(row["cue_id"]),
        "caption": str(row["caption"]),
        "route": str(row["route"]),
        "moment": str(row.get("moment", "")),
        "policy": str(row.get("policy", "")),
        "audio_path": str(row.get("audio_path", "")),
    }


def make_plan(catalog_path: Path, trials: Path, takes: int) -> dict[str, Any]:
    document, rows = load_pending(catalog_path)
    resolve_inside(trials, TMP_DIR)
    if takes < 1 or takes > 8:
        raise ValueError("takes must be between 1 and 8")
    return {
        "schema": 1,
        "status": "PLANNED_NO_MODEL_RUN",
        "catalog_path": portable_path(catalog_path),
        "catalog_sha256": sha256_file(catalog_path),
        "catalog_schema_version": document.get("schema_version"),
        "speaker": "roshan",
        "model": "parler-tts/parler-tts-mini-v1.1",
        "takes_per_cue": takes,
        "candidate_root": portable_path(trials),
        "rows": [row_identity(row) | {
            "candidate_files": [
                f"{row['cue_id']}__attempt_{index}.wav"
                for index in range(1, takes + 1)
            ],
        } for row in rows],
        "scope": {
            "pending_status_only": True,
            "allow_generic": False,
            "faron_allowed": False,
            "runtime_writes": False,
        },
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def run_generation(catalog: Path, trials: Path, takes: int, attempt: int,
                   register_profile: str) -> int:
    resolve_inside(trials, TMP_DIR)
    command = [
        sys.executable, str(ROOT / "tools" / "make_parler_voice_trials.py"),
        "--contextual-catalog", str(catalog), "--takes-per-key", str(takes),
        "--attempt", str(attempt), "--roshan-register-profile", register_profile,
        "--out", str(trials),
    ]
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def load_report(report_path: Path, rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(report, list):
        raise ValueError("selection report must be a list")
    expected = {str(row["cue_id"]): str(row["caption"]) for row in rows}
    by_key: dict[str, dict[str, Any]] = {}
    for item in report:
        if not isinstance(item, dict):
            raise ValueError("selection report contains a non-object row")
        key = str(item.get("key", ""))
        if key in by_key or key not in expected:
            raise ValueError(f"selection report key is outside pending cohort: {key}")
        if str(item.get("expected", "")) != expected[key]:
            raise ValueError(f"caption mismatch for selected cue: {key}")
        if item.get("status") != "SELECTED" or not isinstance(item.get("chosen"), dict):
            raise ValueError(f"selection is incomplete for {key}")
        by_key[key] = item
    if set(by_key) != set(expected):
        missing = sorted(set(expected) - set(by_key))
        raise ValueError("selection report does not cover pending cohort: " + ", ".join(missing))
    return by_key


def snapshot_files(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def append_license_rows(license_path: Path, rows: list[dict[str, Any]],
                        catalog_sha: str) -> None:
    existing = license_path.read_text(encoding="utf-8")
    marker = f"<!-- day-one-contextual-cohort:{catalog_sha} -->"
    if marker in existing:
        raise ValueError("contextual cohort license row already exists")
    lines = ["", marker]
    for row in rows:
        audio_path = str(row["audio_path"])
        lines.append(
            f"| {audio_path} | Parler-TTS Mini v1.1 synthetic contextual voice; "
            f"project-authored line `{row['cue_id']}` | Apache-2.0 model/code; "
            f"synthesized provisional output | "
            f"https://huggingface.co/parler-tts/parler-tts-mini-v1.1 "
            f"(catalog SHA-256 `{catalog_sha}`) | Append-only selected cohort; "
            f"48 kHz mono Ogg Vorbis 96 kbps; -16 LUFS; protected Faron/family "
            f"recordings unchanged |"
        )
    license_path.write_text(existing.rstrip() + "\n" + "\n".join(lines) + "\n",
                            encoding="utf-8")


def master_append(catalog_path: Path, report_path: Path, trials: Path,
                  out: Path, provenance_path: Path, license_path: Path) -> dict[str, Any]:
    document, rows = load_pending(catalog_path)
    if out.resolve() != RUNTIME_DIR.resolve():
        raise ValueError("append-only delivery target must be assets/audio/voices/filler_v1")
    resolve_inside(trials, TMP_DIR)
    report_by_key = load_report(report_path, rows)
    if not out.is_dir():
        raise ValueError("existing filler_v1 directory and manifest are required")
    manifest_path = out / "FILLER_MANIFEST.json"
    if not manifest_path.is_file() or not license_path.is_file():
        raise ValueError("existing runtime manifest and ASSET_LICENSES.md are required")
    existing_manifest_bytes = manifest_path.read_bytes()
    existing_manifest = json.loads(existing_manifest_bytes.decode("utf-8"))
    existing_entries = list(existing_manifest.get("entries", []))
    existing_keys = {str(item.get("key")) for item in existing_entries}
    if existing_keys.intersection(report_by_key):
        raise ValueError("append-only cohort would overwrite existing manifest keys")
    protected_before = snapshot_files(ROOT / "assets" / "audio" / "voices")
    # Keep the normal command independent of PYTHONPATH and import the mature
    # mastering implementation only for an explicit delivery operation.
    master_spec = importlib.util.spec_from_file_location(
        "day_one_master_filler_voices", REPO_ROOT / "tools" / "master_filler_voices.py"
    )
    if master_spec is None or master_spec.loader is None:
        raise ValueError("could not load tools/master_filler_voices.py")
    master_module = importlib.util.module_from_spec(master_spec)
    master_spec.loader.exec_module(master_module)
    master_source = master_module.master_source

    trial_rows: dict[tuple[str, int, str], dict[str, Any]] = {}
    manifest_paths = sorted(trials.glob("attempt_*/*manifest.json"))
    contextual_manifest = trials / "trial_manifest.json"
    if contextual_manifest.is_file():
        manifest_paths.append(contextual_manifest)
    for manifest in manifest_paths:
        for item in json.loads(manifest.read_text(encoding="utf-8")):
            raw = Path(str(item.get("raw_path", "")))
            if not raw.is_absolute():
                raw = manifest.parent / raw
            raw = raw.resolve()
            resolve_inside(raw, TMP_DIR)
            trial_rows[(str(item.get("key")), int(item.get("attempt", -1)),
                       str(item.get("raw_sha256", "")).lower())] = item | {"_raw": raw}
    with tempfile.TemporaryDirectory(prefix="day_one_contextual_master_", dir=TMP_DIR) as stage_name:
        stage = Path(stage_name)
        new_entries: list[dict[str, Any]] = []
        for row in rows:
            key = str(row["cue_id"])
            asset_key = Path(str(row["audio_path"])).stem
            chosen = report_by_key[key]["chosen"]
            attempt = int(chosen.get("attempt", -1))
            chosen_sha = str(chosen.get("selected_raw_sha256") or chosen.get("source_sha256") or "").lower()
            source_record = trial_rows.get((key, attempt, chosen_sha))
            if source_record is None:
                raise ValueError(f"selected candidate provenance missing for {key}")
            source = Path(source_record["_raw"])
            if sha256_file(source) != chosen_sha:
                raise ValueError(f"selected candidate hash mismatch for {key}")
            destination = stage / f"{asset_key}.ogg"
            metrics, command = master_source(source, destination)
            new_entries.append({
                "key": asset_key, "contextual_cue_id": key,
                "character": "roshan", "text": row["caption"],
                "status": "PROVISIONAL_SYNTHETIC_CONTEXTUAL",
                "selected_attempt": attempt, "seed": chosen.get("seed"),
                "mood": source_record.get("mood"),
                "speaker_preset": source_record.get("speaker"),
                "description": source_record.get("description"),
                "roshan_register_profile": source_record.get("roshan_register_profile"),
                "model": source_record.get("model"),
                "model_revision": source_record.get("model_revision"),
                "description_tokenizer_revision": source_record.get("description_tokenizer_revision"),
                "generation_text": source_record.get("generation_text"),
                "generation_segments": source_record.get("generation_segments"),
                "segment_seeds": source_record.get("segment_seeds"),
                "source_wav_sha256": chosen_sha,
                "final_ogg_sha256": sha256_file(destination),
                "selection_report_sha256": sha256_file(report_path),
                "selection_metrics": chosen,
                "delivery_metrics": metrics, "ffmpeg_command": command,
                "contextual_catalog_sha256": sha256_file(catalog_path),
                "policy": row.get("policy"), "route": row.get("route"),
            })
        staged_names = {path.name for path in stage.glob("*.ogg")}
        expected_names = {Path(str(row["audio_path"])).name for row in rows}
        if staged_names != expected_names:
            raise ValueError("staged OGG set does not match pending cohort")
        merged = dict(existing_manifest)
        merged["entries"] = existing_entries + new_entries
        merged["contextual_append_only"] = True
        merged["contextual_cohort_catalog_sha256"] = sha256_file(catalog_path)
        merged["contextual_cohort_selection_report_sha256"] = sha256_file(report_path)
        staged_manifest = stage / "FILLER_MANIFEST.json"
        write_json(staged_manifest, merged)
        staged_provenance = stage / provenance_path.name
        write_json(staged_provenance, {
            "schema": 1, "status": "APPENDED_AFTER_SELECTION",
            "catalog": portable_path(catalog_path),
            "catalog_sha256": sha256_file(catalog_path),
            "selection_report": portable_path(report_path),
            "selection_report_sha256": sha256_file(report_path),
            "cue_ids": [str(row["cue_id"]) for row in rows],
            "entries": new_entries,
            "protected_voice_tree_before": protected_before,
        })
        # All validation is complete; this is the first point at which runtime
        # bytes, manifest provenance, and license evidence are changed.
        for path in sorted(stage.glob("*.ogg")):
            destination = out / path.name
            if destination.exists():
                raise ValueError(f"runtime destination appeared during delivery: {destination}")
            shutil.copyfile(path, destination)
        os.replace(staged_manifest, manifest_path)
        provenance_path.parent.mkdir(parents=True, exist_ok=True)
        os.replace(staged_provenance, provenance_path)
    append_license_rows(license_path, rows, sha256_file(catalog_path))
    protected_after = snapshot_files(ROOT / "assets" / "audio" / "voices")
    if any(protected_before.get(key) != value for key, value in protected_after.items()
           if not key.startswith("filler_v1/")):
        raise ValueError("protected/family voice tree changed during append")
    return {"status": "APPENDED_AFTER_SELECTION", "cue_ids": [str(row["cue_id"]) for row in rows]}


def enrich_provenance(manifest_path: Path, provenance_path: Path,
                      trials: Path) -> dict[str, Any]:
    """Complete embedded contextual generation evidence without changing audio."""
    resolve_inside(trials, TMP_DIR)
    trial_manifest = trials / "trial_manifest.json"
    if not trial_manifest.is_file():
        raise ValueError("contextual trial_manifest.json is required")
    trial_rows = json.loads(trial_manifest.read_text(encoding="utf-8"))
    if not isinstance(trial_rows, list):
        raise ValueError("contextual trial manifest must be a list")
    by_selection: dict[tuple[str, int, str], dict[str, Any]] = {}
    for item in trial_rows:
        if not isinstance(item, dict):
            continue
        by_selection[(str(item.get("key")), int(item.get("attempt", -1)),
                      str(item.get("raw_sha256", "")).lower())] = item
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])
    enriched: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("contextual_cue_id"):
            continue
        cue_id = str(entry["contextual_cue_id"])
        selection = (cue_id, int(entry.get("selected_attempt", -1)),
                     str(entry.get("source_wav_sha256", "")).lower())
        source = by_selection.get(selection)
        if source is None:
            raise ValueError(f"contextual generation evidence missing for {cue_id}")
        entry["description"] = source.get("description")
        entry["roshan_register_profile"] = source.get("roshan_register_profile")
        if not entry["description"]:
            raise ValueError(f"contextual generation description missing for {cue_id}")
        audio_path = RUNTIME_DIR / f"{entry['key']}.ogg"
        if not audio_path.is_file() or sha256_file(audio_path) != entry.get("final_ogg_sha256"):
            raise ValueError(f"contextual runtime audio hash mismatch for {cue_id}")
        enriched.append(entry)
    if len(enriched) != len(provenance.get("cue_ids", [])):
        raise ValueError("contextual provenance cue count mismatch")
    provenance["entries"] = enriched
    provenance["trial_manifest_sha256"] = sha256_file(trial_manifest)
    provenance["generator_sha256"] = normalized_text_sha256(
        ROOT / "tools" / "make_parler_voice_trials.py")
    provenance["selector_sha256"] = normalized_text_sha256(
        ROOT / "tools" / "select_filler_voices.py")
    provenance["cohort_tool_sha256"] = normalized_text_sha256(Path(__file__))
    staged_provenance = provenance_path.with_suffix(".json.tmp")
    write_json(staged_provenance, provenance)
    manifest["contextual_cohort_provenance_path"] = portable_path(provenance_path)
    manifest["contextual_cohort_provenance_sha256"] = sha256_file(staged_provenance)
    pipeline = manifest.get("pipeline_script_sha256")
    if isinstance(pipeline, dict):
        for rel in ("tools/make_parler_voice_trials.py", "tools/select_filler_voices.py"):
            pipeline[rel] = normalized_text_sha256(ROOT / rel)
    selection = manifest.get("selection_provenance")
    if isinstance(selection, dict):
        selection["selector_sha256"] = normalized_text_sha256(
            ROOT / "tools" / "select_filler_voices.py")
    staged_manifest = manifest_path.with_suffix(".json.tmp")
    write_json(staged_manifest, manifest)
    os.replace(staged_provenance, provenance_path)
    os.replace(staged_manifest, manifest_path)
    return {"status": "CONTEXTUAL_PROVENANCE_ENRICHED", "cue_count": len(enriched)}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    plan.add_argument("--trials", type=Path, default=DEFAULT_TRIALS)
    plan.add_argument("--takes-per-cue", type=int, default=3)
    plan.add_argument("--output", type=Path)
    generate = sub.add_parser("generate")
    generate.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    generate.add_argument("--trials", type=Path, default=DEFAULT_TRIALS)
    generate.add_argument("--takes-per-cue", type=int, default=3)
    generate.add_argument("--attempt", type=int, default=1)
    generate.add_argument("--roshan-register-profile", default="baseline")
    master = sub.add_parser("master")
    master.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    master.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    master.add_argument("--trials", type=Path, default=DEFAULT_TRIALS)
    master.add_argument("--out", type=Path, default=RUNTIME_DIR)
    master.add_argument("--provenance", type=Path,
                        default=RUNTIME_DIR / "DAY_ONE_CONTEXTUAL_COHORT_PROVENANCE.json")
    master.add_argument("--licenses", type=Path, default=ROOT / "ASSET_LICENSES.md")
    enrich = sub.add_parser("enrich")
    enrich.add_argument("--manifest", type=Path, default=RUNTIME_DIR / "FILLER_MANIFEST.json")
    enrich.add_argument("--provenance", type=Path,
                        default=RUNTIME_DIR / "DAY_ONE_CONTEXTUAL_COHORT_PROVENANCE.json")
    enrich.add_argument("--trials", type=Path, default=DEFAULT_TRIALS)
    args = parser.parse_args()
    try:
        if args.command == "plan":
            output = args.output or args.trials / "day_one_contextual_plan.json"
            write_json(output, make_plan(args.catalog, args.trials, args.takes_per_cue))
            print(f"DAY_ONE_CONTEXTUAL|PLAN|{output}")
            return 0
        if args.command == "generate":
            # Generation is explicit and still writes only below tmp/.
            return run_generation(args.catalog, args.trials, args.takes_per_cue,
                                  args.attempt, args.roshan_register_profile)
        if args.command == "enrich":
            result = enrich_provenance(args.manifest, args.provenance, args.trials)
            print(f"DAY_ONE_CONTEXTUAL|{result['status']}|{result['cue_count']} cues")
            return 0
        result = master_append(args.catalog, args.report, args.trials, args.out,
                               args.provenance, args.licenses)
        print(f"DAY_ONE_CONTEXTUAL|{result['status']}|{len(result['cue_ids'])} cues")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
