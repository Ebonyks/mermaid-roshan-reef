#!/usr/bin/env python3
"""Blocking provenance and delivery audit for the Opera Arborist art packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "assets_src/imagegen/opera_arborist_2026-08-09"
PROVENANCE = PACKET / "PROVENANCE.json"
REVIEW = PACKET / "REVIEW.json"
PROMPTS = PACKET / "PROMPTS.md"
DERIVATION_REPORT = PACKET / "DERIVATION_REPORT.json"
LICENSES = ROOT / "ASSET_LICENSES.md"

EXPECTED_GENERATED = 10
EXPECTED_SOURCE_DERIVATIVES = 16
EXPECTED_RUNTIME = 28
STRICT_TREE_KEY_DISTANCE = 96.0

TREE_ALPHA_PAIRS = (
    (PACKET / "tree_states_native.png", PACKET / "tree_states_alpha_connected.png"),
    (
        PACKET / "tree_intermediate_native.png",
        PACKET / "tree_intermediate_alpha_connected.png",
    ),
)
TREE_RUNTIME = (
    "tree_needs_care.png",
    "tree_checked.png",
    "tree_pruned.png",
    "tree_watered.png",
    "tree_treated.png",
    "tree_bloom.png",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_sha256(path: Path) -> str:
    """Hash repository text with Git-checkout-stable LF normalization."""

    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {relative(path)}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {relative(path)}: {exc}")
    return {}


def pixels(image: Image.Image):
    """Return flat pixel data without Pillow 13's deprecated getdata warning."""

    flattened = getattr(image, "get_flattened_data", None)
    return flattened() if flattened is not None else image.getdata()


def audit_image_record(
    path_text: str,
    expected_hash: object,
    expected_dimensions: object,
    errors: list[str],
) -> None:
    path = ROOT / path_text
    if not path.is_file():
        errors.append(f"missing {path_text}")
        return
    actual_hash = sha256(path)
    if actual_hash != expected_hash:
        errors.append(f"hash drift: {path_text}")
    try:
        with Image.open(path) as image:
            if list(image.size) != expected_dimensions:
                errors.append(
                    f"dimension drift: {path_text} is {image.size}, "
                    f"expected {expected_dimensions}"
                )
    except OSError as exc:
        errors.append(f"cannot decode {path_text}: {exc}")


def audit_manifest(provenance: dict, errors: list[str]) -> set[str]:
    if provenance.get("schema") != 1:
        errors.append("provenance schema must be 1")
    if provenance.get("generator") != "built-in OpenAI ImageGen":
        errors.append("generator identity is missing or changed")
    prompt_record = provenance.get("prompt_record", {}) or {}
    if prompt_record.get("verbatim") is not False:
        errors.append("compacted prompt record must not claim to be verbatim")
    if prompt_record.get("invented_verbatim_claim") is not False:
        errors.append("prompt provenance must explicitly reject an invented exact claim")
    if provenance.get("protected_originals_modified") is not False:
        errors.append("protected-original modification declaration must be false")
    if provenance.get("protected_originals_used_as_delivery_pixels") is not False:
        errors.append("protected originals must not be declared as delivery pixels")
    if provenance.get("external_assets") != []:
        errors.append("Arborist packet unexpectedly declares external assets")

    generated = provenance.get("generated_sources", {}) or {}
    derivatives = provenance.get("source_derivatives", {}) or {}
    runtime = provenance.get("runtime_outputs", {}) or {}
    if len(generated) != EXPECTED_GENERATED:
        errors.append(
            f"expected {EXPECTED_GENERATED} generated sources, found {len(generated)}"
        )
    if len(derivatives) != EXPECTED_SOURCE_DERIVATIVES:
        errors.append(
            f"expected {EXPECTED_SOURCE_DERIVATIVES} source derivatives, "
            f"found {len(derivatives)}"
        )
    if len(runtime) != EXPECTED_RUNTIME:
        errors.append(f"expected {EXPECTED_RUNTIME} runtime PNGs, found {len(runtime)}")

    generation_ids: set[str] = set()
    for path_text, record_value in generated.items():
        record = record_value or {}
        generation_id = str(record.get("generation_id", ""))
        if not generation_id.startswith("exec-"):
            errors.append(f"missing ImageGen result ID: {path_text}")
        if generation_id in generation_ids:
            errors.append(f"duplicate ImageGen result ID: {generation_id}")
        generation_ids.add(generation_id)
        if record.get("result_filename") != f"{generation_id}.png":
            errors.append(f"result filename does not match generation ID: {path_text}")
        audit_image_record(
            path_text, record.get("sha256"), record.get("dimensions"), errors
        )

    for group_name, group in (("source derivative", derivatives), ("runtime", runtime)):
        for path_text, record_value in group.items():
            if not isinstance(record_value, list) or len(record_value) != 3:
                errors.append(f"malformed {group_name} record: {path_text}")
                continue
            audit_image_record(path_text, record_value[0], record_value[1], errors)

    all_pngs = set(generated) | set(derivatives) | set(runtime)
    if len(all_pngs) != EXPECTED_GENERATED + EXPECTED_SOURCE_DERIVATIVES + EXPECTED_RUNTIME:
        errors.append("manifest PNG paths overlap unexpectedly")
    return all_pngs


def audit_reports(provenance: dict, errors: list[str]) -> None:
    reports = provenance.get("reports", {}) or {}
    for path_text, expected_hash in reports.items():
        path = ROOT / path_text
        if not path.is_file():
            errors.append(f"missing report {path_text}")
        elif text_sha256(path) != expected_hash:
            errors.append(f"report hash drift: {path_text}")

    tools = provenance.get("build_tools", {}) or {}
    for path_text, expected_hash in tools.items():
        path = ROOT / path_text
        if not path.is_file():
            errors.append(f"missing build tool {path_text}")
        elif text_sha256(path) != expected_hash:
            errors.append(f"build-tool hash drift: {path_text}")

    report = load_json(DERIVATION_REPORT, errors)
    if report.get("pass") is not True:
        errors.append("DERIVATION_REPORT.json is not passing")
    manifest_records: dict[str, list] = {}
    manifest_records.update(provenance.get("source_derivatives", {}) or {})
    manifest_records.update(provenance.get("runtime_outputs", {}) or {})
    for output in report.get("outputs", []):
        path_text = str(output.get("path", ""))
        record = manifest_records.get(path_text)
        if record is None:
            errors.append(f"derivation output absent from provenance: {path_text}")
            continue
        if output.get("sha256") != record[0]:
            errors.append(f"derivation/provenance hash mismatch: {path_text}")
        if output.get("dimensions") != record[1]:
            errors.append(f"derivation/provenance dimensions mismatch: {path_text}")


def audit_tile_reconstruction(errors: list[str]) -> None:
    for kind in ("world", "stage"):
        master_path = PACKET / f"{kind}_arborist_master_2048.png"
        try:
            with Image.open(master_path) as image:
                master = image.convert("RGBA")
            joined = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
            for row in range(2):
                for col in range(2):
                    tile_path = (
                        ROOT
                        / "assets/opera/worlds/backdrops"
                        / f"{kind}_arborist_c{col}r{row}.png"
                    )
                    with Image.open(tile_path) as image:
                        tile = image.convert("RGBA")
                    joined.paste(tile, (col * 1024, row * 1024))
            if ImageChops.difference(master, joined).getbbox() is not None:
                errors.append(f"{kind} 2x2 tiles do not exactly reconstruct the master")
        except (FileNotFoundError, OSError) as exc:
            errors.append(f"cannot reconstruct {kind} tiles: {exc}")


def sampled_key(image: Image.Image) -> tuple[float, float, float]:
    rgb = image.convert("RGB")
    width, height = rgb.size
    span = max(8, min(width, height) // 40)
    samples: list[tuple[int, int, int]] = []
    for box in (
        (0, 0, span, span),
        (width - span, 0, width, span),
        (0, height - span, span, height),
        (width - span, height - span, width, height),
    ):
        samples.extend(pixels(rgb.crop(box)))
    return tuple(statistics.median(channel) for channel in zip(*samples))


def audit_tree_key_cleanup(errors: list[str]) -> None:
    for source_path, alpha_path in TREE_ALPHA_PAIRS:
        try:
            with Image.open(source_path) as image:
                source = image.convert("RGB")
            with Image.open(alpha_path) as image:
                alpha = image.convert("RGBA")
            if source.size != alpha.size:
                errors.append(f"tree matte size mismatch: {relative(alpha_path)}")
                continue
            key = sampled_key(source)
            residual = 0
            for rgb, rgba in zip(pixels(source), pixels(alpha)):
                if max(abs(float(rgb[i]) - key[i]) for i in range(3)) \
                        <= STRICT_TREE_KEY_DISTANCE and rgba[3] != 0:
                    residual += 1
                    if residual >= 4:
                        break
            if residual:
                errors.append(
                    f"{relative(alpha_path)} retains {residual}+ opaque strict-key pixels"
                )
        except (FileNotFoundError, OSError) as exc:
            errors.append(f"cannot audit strict tree key: {exc}")

    runtime_root = ROOT / "assets/opera/worlds/arborist"
    tree_hashes: set[str] = set()
    for name in TREE_RUNTIME:
        path = runtime_root / name
        if path.is_file():
            tree_hashes.add(sha256(path))
        try:
            with Image.open(path) as image:
                rgba = image.convert("RGBA")
            bbox = rgba.getchannel("A").getbbox()
            if bbox is None:
                errors.append(f"empty tree state: {relative(path)}")
            elif min(bbox[0], bbox[1], 768 - bbox[2], 768 - bbox[3]) < 4:
                errors.append(f"tree state lacks a safe transparent margin: {relative(path)}")
        except (FileNotFoundError, OSError) as exc:
            errors.append(f"cannot inspect tree state {relative(path)}: {exc}")
    if len(tree_hashes) != len(TREE_RUNTIME):
        errors.append("all six semantic tree states must have distinct PNG hashes")


def audit_review(review: dict, errors: list[str]) -> None:
    if review.get("schema") != 1:
        errors.append("review schema must be 1")
    if review.get("overall_decision") != "accepted_with_release_gates":
        errors.append("review must retain its open release gates")
    release_text = json.dumps(review.get("release_gates", []))
    for cue_id in (
        "op_arborist_inspect",
        "op_arborist_prune",
        "op_arborist_roots",
        "op_arborist_wrap",
        "op_arborist_bloom",
    ):
        if cue_id not in release_text:
            errors.append(f"pending protected-audio gate omits {cue_id}")
    backgrounds = (review.get("backgrounds", {}) or {}).get("human_review", {}) or {}
    for check in (
        "hero_tree_absent_from_clean_bed",
        "no_substitute_tree_in_clean_bed",
        "composition_continuity",
        "quiet_play_band",
        "no_required_text",
        "storybook_style",
    ):
        if backgrounds.get(check) is not True:
            errors.append(f"background review missing '{check}'")
    for section in ("hero_tree", "roshan", "helper_imp", "props"):
        checks = (review.get(section, {}) or {}).get("human_review", {}) or {}
        if not checks or not all(value is True for value in checks.values()):
            errors.append(f"{section} human review is incomplete")
    matte = review.get("matte_review", {}) or {}
    if matte.get("enclosed_tree_key_islands_removed") is not True:
        errors.append("tree enclosed-key cleanup is not human-reviewed")
    if matte.get("guide_pixels_used") is not False:
        errors.append("guide pixels must not be used")
    if matte.get("repaint_or_subject_warp") is not False:
        errors.append("review unexpectedly declares repaint or subject warp")
    if review.get("owner_visual_score_5_of_5") is not False:
        errors.append("technical review must not grant owner-only 5-of-5")
    if review.get("owner_review_pending") is not True:
        errors.append("owner on-device review must remain visibly pending")


def audit_licenses(all_pngs: set[str], errors: list[str]) -> None:
    try:
        text = LICENSES.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError) as exc:
        errors.append(f"cannot read ASSET_LICENSES.md: {exc}")
        return
    for path_text in sorted(all_pngs):
        if f"`{path_text}`" not in text:
            errors.append(f"missing ASSET_LICENSES.md entry: {path_text}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    for path in (PROMPTS, REVIEW, PROVENANCE, DERIVATION_REPORT, LICENSES):
        if not path.is_file():
            errors.append(f"missing {relative(path)}")
    provenance = load_json(PROVENANCE, errors)
    review = load_json(REVIEW, errors)
    all_pngs = audit_manifest(provenance, errors) if provenance else set()
    if provenance:
        audit_reports(provenance, errors)
    audit_tile_reconstruction(errors)
    audit_tree_key_cleanup(errors)
    if review:
        audit_review(review, errors)
    if all_pngs:
        audit_licenses(all_pngs, errors)

    if errors:
        for error in errors:
            print(f"OPERA_ARBORIST_ART|FAIL|{error}")
        print(f"OPERA_ARBORIST_ART|result: {len(errors)} FAIL")
        return 1
    if not args.quiet:
        print(
            "OPERA_ARBORIST_ART|result: ALL OK "
            f"({len(all_pngs)} licensed PNGs, six distinct tree states)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
