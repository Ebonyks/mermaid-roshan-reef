#!/usr/bin/env python3
"""Safely remove the explicitly retired, catalog-only Day One voice rows.

This command is intentionally allow-listed.  It refuses to run when a target
cue has an unexpected runtime/cinematic reference or when any target row is
missing/duplicated in a linked artifact.  Use ``--check`` for a read-only
audit (the default), and ``--apply`` to update the source catalog, generated
runtime catalog, cohort proof/manifest, and license table.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TARGET_IDS = (
    "day1_art_customization",
    "day1_art_material_blue_paint",
    "day1_art_material_brushes",
    "day1_art_material_cups",
    "day1_art_material_pink_paint",
    "day1_art_scrub_left",
    "day1_art_scrub_right",
)
TARGET_KEYS = {f"roshan_{cue_id}" for cue_id in TARGET_IDS}
CATALOG = ROOT / "audit" / "DAY_ONE_CONTEXTUAL_VOICE_COVERAGE_2026-09-01.json"
RUNTIME = ROOT / "scripts" / "day_one_contextual_voice_catalog.gd"
MANIFEST = ROOT / "assets" / "audio" / "voices" / "filler_v1" / "FILLER_MANIFEST.json"
PROVENANCE = ROOT / "assets" / "audio" / "voices" / "filler_v1" / "DAY_ONE_CONTEXTUAL_COHORT_PROVENANCE.json"
LICENSES = ROOT / "ASSET_LICENSES.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any, *, sort_keys: bool = True) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
                               sort_keys=sort_keys) + "\n",
                    encoding="utf-8", newline="\n")


def occurrences(value: Any, target_ids: set[str]) -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []

    def visit(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                if key in target_ids or key in {f"roshan_{x}" for x in target_ids}:
                    found.append((f"{path}.{key}", child))
                visit(child, f"{path}.{key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                if isinstance(child, dict) and (
                    child.get("cue_id") in target_ids
                    or child.get("contextual_cue_id") in target_ids
                    or child.get("key") in TARGET_KEYS
                ):
                    found.append((f"{path}[{index}]", child))
                visit(child, f"{path}[{index}]")
        elif isinstance(node, str) and node in target_ids:
            found.append((path, node))

    visit(value, "$")
    return found


def runtime_renderer(catalog: dict[str, Any]) -> str:
    module_path = ROOT / "tools" / "audit_day_one_contextual_voices.py"
    spec = importlib.util.spec_from_file_location("day_one_contextual_audit", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load contextual catalog renderer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.runtime_catalog_source(catalog)


def check_target_references() -> None:
    allowed = {
        CATALOG.relative_to(ROOT).as_posix(),
        RUNTIME.relative_to(ROOT).as_posix(),
        MANIFEST.relative_to(ROOT).as_posix(),
        PROVENANCE.relative_to(ROOT).as_posix(),
        LICENSES.relative_to(ROOT).as_posix(),
    }
    hits: list[str] = []
    for base in (ROOT / "scripts", ROOT / "scenes", ROOT / "audit" / "cinematics"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".gd", ".json", ".tscn", ".tres", ".md", ".txt"}:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in allowed:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for cue_id in TARGET_IDS:
                if re.search(rf"(?<![A-Za-z0-9_]){re.escape(cue_id)}(?![A-Za-z0-9_])", text):
                    hits.append(f"{rel}: {cue_id}")
    if hits:
        raise ValueError("unexpected runtime/cinematic references:\n" + "\n".join(hits))


def remove_rows(document: dict[str, Any], field: str) -> None:
    rows = document.get(field)
    if not isinstance(rows, list):
        raise ValueError(f"{field} must be a list")
    if field == "cue_ids":
        counts = {cue_id: rows.count(cue_id) for cue_id in TARGET_IDS}
        if counts != {cue_id: 1 for cue_id in TARGET_IDS}:
            raise ValueError(f"unexpected target cue_ids counts: {counts}")
        document[field] = [row for row in rows if row not in TARGET_IDS]
        return
    matches = [row for row in rows if isinstance(row, dict) and (
        row.get("cue_id") in TARGET_IDS
        or row.get("contextual_cue_id") in TARGET_IDS
        or row.get("key") in TARGET_KEYS
    )]
    counts = {cue_id: sum(
        row.get("cue_id") == cue_id
        or row.get("contextual_cue_id") == cue_id
        or row.get("key") == f"roshan_{cue_id}"
        for row in matches
    ) for cue_id in TARGET_IDS}
    if counts != {cue_id: 1 for cue_id in TARGET_IDS}:
        raise ValueError(f"unexpected target {field} counts: {counts}")
    document[field] = [row for row in rows if row not in matches]


def update_hash_fields(value: Any, catalog_hash: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"catalog_sha256", "contextual_catalog_sha256", "contextual_cohort_catalog_sha256"}:
                value[key] = catalog_hash
            else:
                update_hash_fields(child, catalog_hash)
    elif isinstance(value, list):
        for child in value:
            update_hash_fields(child, catalog_hash)


def apply() -> None:
    check_target_references()
    catalog = load(CATALOG)
    runtime_before = RUNTIME.read_text(encoding="utf-8")
    if runtime_before != runtime_renderer(catalog):
        raise ValueError("runtime catalog was already out of parity; refusing prune")
    remove_rows(catalog, "rows")
    dump(CATALOG, catalog, sort_keys=False)
    catalog_hash = sha256(CATALOG)
    RUNTIME.write_text(runtime_renderer(catalog), encoding="utf-8", newline="\n")

    provenance = load(PROVENANCE)
    remove_rows(provenance, "cue_ids")
    remove_rows(provenance, "entries")
    update_hash_fields(provenance, catalog_hash)
    dump(PROVENANCE, provenance)
    provenance_hash = sha256(PROVENANCE)

    manifest = load(MANIFEST)
    remove_rows(manifest, "entries")
    update_hash_fields(manifest, catalog_hash)
    manifest["contextual_cohort_provenance_sha256"] = provenance_hash
    dump(MANIFEST, manifest)

    license_text = LICENSES.read_text(encoding="utf-8")
    for cue_id in TARGET_IDS:
        needle = f"| assets/audio/voices/filler_v1/roshan_{cue_id}.ogg |"
        matching = [line for line in license_text.splitlines() if needle in line]
        if len(matching) != 1:
            raise ValueError(f"expected one license row for {cue_id}, found {len(matching)}")
        license_text = "\n".join(line for line in license_text.splitlines() if needle not in line) + "\n"
    license_text = license_text.replace("aeda6a42ad3792580074c773441eb660936f8e099c79ba405f3228ee1e109323", catalog_hash)
    LICENSES.write_text(license_text, encoding="utf-8", newline="\n")
    print(f"PRUNE|applied|catalog_rows={len(catalog['rows'])}|manifest_entries={len(manifest['entries'])}|catalog_sha256={catalog_hash}|provenance_sha256={provenance_hash}")


def check() -> None:
    check_target_references()
    for path in (CATALOG, RUNTIME, MANIFEST, PROVENANCE, LICENSES):
        if not path.is_file():
            raise ValueError(f"missing linked artifact: {path.relative_to(ROOT)}")
    catalog = load(CATALOG)
    manifest = load(MANIFEST)
    provenance = load(PROVENANCE)
    licenses = LICENSES.read_text(encoding="utf-8")
    for cue_id in TARGET_IDS:
        if occurrences(catalog, {cue_id}):
            raise ValueError(f"retired cue remains in catalog: {cue_id}")
        if occurrences(manifest, {cue_id}):
            raise ValueError(f"retired cue remains in manifest: {cue_id}")
        if occurrences(provenance, {cue_id}):
            raise ValueError(f"retired cue remains in provenance: {cue_id}")
        exact_token = re.compile(
            rf"(?<![A-Za-z0-9_]){re.escape(cue_id)}(?![A-Za-z0-9_])")
        if exact_token.search(RUNTIME.read_text(encoding="utf-8")) \
                or exact_token.search(licenses):
            raise ValueError(f"retired cue remains in generated text: {cue_id}")
        audio = ROOT / "assets" / "audio" / "voices" / "filler_v1" / f"roshan_{cue_id}.ogg"
        if audio.exists() or audio.with_suffix(".ogg.import").exists():
            raise ValueError(f"retired runtime asset remains: {audio.relative_to(ROOT)}")
    if RUNTIME.read_text(encoding="utf-8") != runtime_renderer(catalog):
        raise ValueError("runtime catalog is out of parity")
    catalog_hash = sha256(CATALOG)
    if provenance.get("catalog_sha256") != catalog_hash:
        raise ValueError("provenance catalog hash is stale")
    if manifest.get("contextual_cohort_catalog_sha256") != catalog_hash:
        raise ValueError("manifest catalog hash is stale")
    captions = [str(row.get("caption", "")) for row in catalog.get("rows", [])]
    if len(captions) != len(set(captions)):
        raise ValueError("catalog still contains duplicate captions")
    print(f"PRUNE|check|retired={len(TARGET_IDS)}|catalog_rows={len(catalog.get('rows', []))}|catalog_sha256={catalog_hash}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        apply() if args.apply else check()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PRUNE|FAIL|{exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
