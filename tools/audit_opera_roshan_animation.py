#!/usr/bin/env python3
"""Blocking structural audit for the shipping Opera Roshan animation atlases.

The pack report proves that the native alpha sheet was sliced without losing
pixels.  This gate independently reopens every production PNG, checks the
report hashes and cell geometry, and requires the frame-by-frame human review
ledger that catches semantic defects such as legs, missing tails, or floating
props that pixel bounds alone cannot understand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src" / "imagegen" / "opera_roshan_animation_2026-08-09"
RUNTIME = ROOT / "assets" / "opera" / "worlds" / "actors" / "animation"
REVIEW = SOURCE / "OPERA_ROSHAN_ANIMATION_REVIEW_2026-08-09.json"
CAREERS = (
    "astronaut",
    "ballerina",
    "boxer",
    "candymaker",
    "chef",
    "detective",
    "doctor",
    "farmer",
    "magician",
    "nursery",
    "painter",
    "popstar",
    "racer",
)
ROWS = ("idle", "travel", "work", "cheer")
CELL = 256
MIN_MARGIN = 14


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {path.relative_to(ROOT)}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
    return {}


def audit_career(career: str, review: dict, errors: list[str]) -> None:
    prefix = f"roshan_{career}_sheet_a"
    native = SOURCE / f"{prefix}_native.png"
    alpha_native = SOURCE / f"{prefix}_alpha_native.png"
    runtime = RUNTIME / f"{prefix}.png"
    report_path = SOURCE / f"{prefix}_pack_report.json"
    for path in (native, alpha_native, runtime, report_path):
        if not path.is_file():
            errors.append(f"{career}: missing {path.relative_to(ROOT)}")
    if any(not path.is_file() for path in (native, alpha_native, runtime, report_path)):
        return

    report = load_json(report_path, errors)
    if not report:
        return
    if report.get("pass") is not True:
        errors.append(f"{career}: pack report is not passing")
    if report.get("runtime_size") != [1024, 1024]:
        errors.append(f"{career}: pack report runtime size is not 1024x1024")
    if int(report.get("component_count", -1)) != 16:
        errors.append(f"{career}: expected exactly one connected subject group per frame")
    if len(report.get("frames", [])) != 16:
        errors.append(f"{career}: pack report does not contain sixteen frames")
    if len(report.get("cell_audits", [])) != 16 or not all(
        bool(item.get("safe", False)) for item in report.get("cell_audits", [])
    ):
        errors.append(f"{career}: pack report cell safety is incomplete")

    alpha_hash = sha256(alpha_native)
    runtime_hash = sha256(runtime)
    if report.get("input_sha256") != alpha_hash:
        errors.append(f"{career}: alpha-native hash differs from pack report")
    if report.get("output_sha256") != runtime_hash:
        errors.append(f"{career}: runtime hash differs from pack report")

    try:
        with Image.open(native) as image:
            if image.size != (1254, 1254):
                errors.append(f"{career}: generated native must remain 1254x1254")
        with Image.open(alpha_native) as image:
            if image.size != (1254, 1254) or image.mode != "RGBA":
                errors.append(f"{career}: alpha native must be 1254x1254 RGBA")
        with Image.open(runtime) as image:
            packed = image.convert("RGBA")
            if image.size != (1024, 1024):
                errors.append(f"{career}: runtime atlas must be 1024x1024")
            for row, row_name in enumerate(ROWS):
                frame_hashes: set[str] = set()
                for col in range(4):
                    cell = packed.crop(
                        (col * CELL, row * CELL, (col + 1) * CELL, (row + 1) * CELL)
                    )
                    bbox = cell.getchannel("A").getbbox()
                    if bbox is None:
                        errors.append(f"{career}: {row_name} frame {col + 1} is empty")
                        continue
                    left, top, right, bottom = bbox
                    margin = min(left, top, CELL - right, CELL - bottom)
                    if margin < MIN_MARGIN:
                        errors.append(
                            f"{career}: {row_name} frame {col + 1} margin is {margin}px"
                        )
                    frame_hashes.add(hashlib.sha256(cell.tobytes()).hexdigest())
                if len(frame_hashes) != 4:
                    errors.append(f"{career}: {row_name} row contains a duplicate/held frame")
    except OSError as exc:
        errors.append(f"{career}: cannot decode an atlas: {exc}")

    entry = (review.get("careers", {}) or {}).get(career, {})
    if entry.get("decision") != "accepted":
        errors.append(f"{career}: human review decision is not accepted")
    checks = entry.get("human_review", {}) or {}
    for check in ("identity", "costume", "one_mermaid_tail", "no_human_legs", "props_attached", "no_artifacts"):
        if checks.get(check) is not True:
            errors.append(f"{career}: missing human review check '{check}'")
    if entry.get("native_sha256") != sha256(native):
        errors.append(f"{career}: reviewed native hash is stale")
    if entry.get("runtime_sha256") != runtime_hash:
        errors.append(f"{career}: reviewed runtime hash is stale")
    if len(entry.get("rows", [])) != 4:
        errors.append(f"{career}: human review does not cover all four semantic rows")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    review = load_json(REVIEW, errors)
    if review.get("schema") != 1:
        errors.append("review ledger schema must be 1")
    if sorted((review.get("careers", {}) or {}).keys()) != list(CAREERS):
        errors.append("review ledger must contain exactly the thirteen shipping careers")
    for career in CAREERS:
        audit_career(career, review, errors)
    if errors:
        for error in errors:
            print(f"OPERA_ROSHAN_ART|FAIL|{error}")
        print(f"OPERA_ROSHAN_ART|result: {len(errors)} FAIL")
        return 1
    if not args.quiet:
        print("OPERA_ROSHAN_ART|result: ALL OK (13 careers, 208 reviewed frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
