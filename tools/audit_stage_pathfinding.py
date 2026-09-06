#!/usr/bin/env python3
"""Fail-closed coverage check for the stage pathfinding inventory.

This checks catalog coverage and provenance only. It deliberately does not
turn existing gameplay probe results into geometry evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "audit/stage_pathfinding/stage_inventory.json"
CASTLE = ROOT / "scripts/arena/castle_rooms_25d.gd"
OPERA = ROOT / "scripts/opera_house.gd"
STATUSES = {"UNVERIFIED", "PARTIAL", "DEBT", "SATISFIED", "ACCEPTED", "COMPLETE"}


def _career_slug(career: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", career.lower()).strip("_")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def expected_catalogs() -> tuple[set[str], set[str]]:
    castle_text = _read(CASTLE)
    rooms_block = castle_text.split("const ROOMS", 1)[1].split("const ROOM_PARENTS", 1)[0]
    rooms = set(re.findall(r'"id"\s*:\s*"([a-z0-9_]+)"', rooms_block))
    opera_text = _read(OPERA)
    live_match = re.search(r"LIVE_ACT_INDICES[^=]*=\s*\[([^\]]+)\]", opera_text)
    if not live_match:
        raise ValueError("LIVE_ACT_INDICES catalog missing")
    live = {int(x) for x in re.findall(r"\d+", live_match.group(1))}
    acts_block = opera_text.split("const ACTS", 1)[1].split("var m:", 1)[0]
    acts: dict[int, str] = {}
    for match in re.finditer(r'"save_bit"\s*:\s*(\d+),\s*"name"\s*:\s*"[^"]+",\s*"career"\s*:\s*"([^"]+)"', acts_block):
        acts[int(match.group(1))] = match.group(2)
    missing = sorted(live - set(acts))
    if missing:
        raise ValueError(f"LIVE_ACT_INDICES missing ACTS entries: {missing}")
    return rooms, {f"opera.act.{bit:02d}.{_career_slug(acts[bit])}" for bit in live}


def _path_tokens(value: str) -> list[str]:
    tokens: list[str] = []
    for raw in value.split(";"):
        raw = raw.strip()
        match = re.search(r"((?:assets|scripts)/[^\s;]+)", raw)
        if match:
            token = match.group(1).rstrip(".,)")
            tokens.append(token)
    return tokens


def _exists(token: str) -> bool:
    path = ROOT / token
    if "*" in token or "?" in token:
        return any(ROOT.glob(token))
    return path.exists()


MATRIX_ROWS = ("tap_arrival", "drag_arrival", "near_tap_once", "cancel_stale", "oob_recovery", "door_arrival", "exact_return", "no_passive_awards")


def _check_matrix(entry: dict, errors: list[str]) -> None:
    ident = str(entry.get("id", "<unknown>"))
    matrix = entry.get("evidence_matrix")
    claimed = entry.get("status") in {"SATISFIED", "ACCEPTED", "COMPLETE"}
    if matrix is None and not claimed:
        return
    if not isinstance(matrix, dict):
        errors.append(f"{ident}: evidence_matrix must be an object of hash-bound rows")
        return
    revision = str(entry.get("source_revision", ""))
    if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        errors.append(f"{ident}: evidence matrix requires a full source_revision commit hash")
    elif subprocess.run(["git", "cat-file", "-e", revision + "^{commit}"],
                        cwd=ROOT, capture_output=True, check=False).returncode:
        errors.append(f"{ident}: source_revision commit does not resolve")
    for row_name in MATRIX_ROWS:
        row = matrix.get(row_name)
        if not isinstance(row, dict) or row.get("result") != "PASS":
            errors.append(f"{ident}: evidence row {row_name} is not PASS")
            continue
        evidence = str(row.get("evidence_path", ""))
        evidence_path = (ROOT / evidence.removeprefix("res://")).resolve()
        try:
            evidence_path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{ident}: evidence row {row_name} escapes repository")
            continue
        digest = str(row.get("sha256", ""))
        if not evidence or not evidence_path.is_file():
            errors.append(f"{ident}: evidence row {row_name} path missing")
        elif not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            errors.append(f"{ident}: evidence row {row_name} hash missing/invalid")
        elif hashlib.sha256(evidence_path.read_bytes()).hexdigest().lower() != digest.lower():
            errors.append(f"{ident}: evidence row {row_name} hash mismatch")
    for review_name in ("human_geometry_review", "target_device_review"):
        review = entry.get(review_name)
        if not isinstance(review, dict) or review.get("result") != "PASS":
            if claimed:
                errors.append(f"{ident}: accepted status requires {review_name}=PASS")
            continue
        review_path = (ROOT / str(review.get("evidence_path", "")).removeprefix("res://")).resolve()
        digest = str(review.get("sha256", ""))
        try:
            review_path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{ident}: {review_name} escapes repository")
            continue
        if not review_path.is_file() or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            errors.append(f"{ident}: {review_name} lacks valid evidence hash/path")
        elif hashlib.sha256(review_path.read_bytes()).hexdigest().lower() != digest.lower():
            errors.append(f"{ident}: {review_name} hash mismatch")


def audit(inventory_path: Path = INVENTORY) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    data = json.loads(_read(inventory_path))
    if not isinstance(data, dict) or data.get("schema") != "stage-pathfinding-inventory-v1":
        return ["unsupported inventory schema"], {}
    entries = data.get("entries")
    if not isinstance(entries, list):
        return ["entries must be an array"], {}
    by_id: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            errors.append("entry missing string id")
            continue
        ident = entry["id"]
        if ident in by_id:
            errors.append(f"duplicate inventory id: {ident}")
        by_id[ident] = entry
        if ident.startswith("opera.act.") and entry.get("surface_class") != "avatar_locomotion":
            errors.append(f"{ident}: live Opera room must cover avatar locomotion and its activity seam")
        if entry.get("surface_class") not in {"avatar_locomotion", "fixed_minigame", "spatial_3d_debt"}:
            errors.append(f"{ident}: invalid surface_class")
        if entry.get("status") not in STATUSES:
            errors.append(f"{ident}: unknown status {entry.get('status')!r}")
        if entry.get("status") in {"SATISFIED", "ACCEPTED", "COMPLETE"}:
            if entry.get("gaps"):
                errors.append(f"{ident}: accepted status with unresolved gaps")
        _check_matrix(entry, errors)
        paths = _path_tokens(str(entry.get("approved_art", "")))
        if not paths:
            runtime = str(entry.get("runtime_state", ""))
            inferred = re.search(r"(?:games|scripts)/[a-z0-9_/]+\.gd", runtime)
            if inferred:
                paths = [inferred.group(0) if inferred.group(0).startswith("scripts/") else "scripts/" + inferred.group(0)]
        if not paths and entry.get("id", "").startswith("debt."):
            debt_paths = {
                "debt.kart": "scripts/kart.gd", "debt.galaxy": "scripts/galaxy.gd",
                "debt.combat.ice": "scripts/combat_arena.gd", "debt.combat.fire": "scripts/combat_arena.gd",
                "debt.stuffie_battle": "scripts/stuffie_battle.gd", "debt.dungeon.00_09": "scripts/dungeon_level.gd",
                "debt.ember.fortress": "scripts/ember_fortress.gd", "debt.ember.dungeon": "scripts/dungeon_level.gd",
            }
            if entry["id"] in debt_paths:
                paths = [debt_paths[entry["id"]]]
        if not paths:
            errors.append(f"{ident}: approved_art has no repository path token")
        for token in paths:
            if not _exists(token):
                errors.append(f"{ident}: source path missing: {token}")

    castle_rooms, opera_prefixes = expected_catalogs()
    for room in sorted(castle_rooms):
        ident = f"level2.castle.{room}"
        if ident not in by_id:
            errors.append(f"missing Castle room variant: {ident}")
    for expected in sorted(opera_prefixes):
        if expected not in by_id:
            errors.append(f"missing live Opera act variant: {expected}")
    counts = {"entries": len(entries), "castle_rooms": len(castle_rooms), "opera_acts": len(opera_prefixes)}
    return errors, counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--check", action="store_true", help="coverage/provenance check; geometry remains advisory")
    parser.add_argument("--strict", action="store_true", help="also fail while any geometry remains unverified")
    args = parser.parse_args(argv)
    errors, counts = audit(args.inventory)
    data = json.loads(_read(args.inventory))
    unresolved = sum(1 for e in data.get("entries", []) if e.get("status") not in {"SATISFIED", "ACCEPTED", "COMPLETE"})
    print(f"STAGEPATH|ENTRIES={counts.get('entries', 0)}|CASTLE={counts.get('castle_rooms', 0)}|OPERA={counts.get('opera_acts', 0)}|OPEN={unresolved}")
    for error in errors:
        print(f"STAGEPATH|FAIL|{error}")
    if args.strict and unresolved:
        print("STAGEPATH|FAIL|strict geometry gate remains open")
    if errors or (args.strict and unresolved):
        print("STAGEPATH|RESULT|FAIL")
        return 1
    print("STAGEPATH|RESULT|COVERAGE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
