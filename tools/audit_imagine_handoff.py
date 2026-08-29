#!/usr/bin/env python3
"""Fail-closed structural audit for external Grok Imagine shot packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_NAME = "IMAGINE_HANDOFF.json"
SHOT_SCHEMA = "imagine-shot-packet-v1"
HANDOFF_SCHEMA = "imagine-handoff-v1"
ALLOWED_REFERENCE_ROLES = {
	"approved_clean_first_frame",
	"subject_identity",
	"object_or_material_identity",
	"lighting_or_grade",
}
FORBIDDEN_PIXEL_PATH_TOKENS = (
	"storyboard",
	"shot_board",
	"runtime_boundary",
	"runtime_anchor",
	"audit_montage",
)
FORBIDDEN_PROMPT_TOKENS = (
	"sha256",
	"license_provenance",
	"archive_complete",
	"delivery_accepted",
	"dl-cin-",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _sha256(path: Path) -> str:
	hash_value = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			hash_value.update(block)
	return hash_value.hexdigest()


def _load_json(path: Path, errors: list[str]) -> dict[str, Any]:
	try:
		value = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		errors.append(f"cannot read JSON {path}: {exc}")
		return {}
	if not isinstance(value, dict):
		errors.append(f"JSON root must be an object: {path}")
		return {}
	return value


def _resolve_inside(packet_dir: Path, relative: str, errors: list[str]) -> Path:
	path = (packet_dir / relative).resolve()
	try:
		path.relative_to(packet_dir.resolve())
	except ValueError:
		errors.append(f"path escapes packet: {relative}")
	return path


def _check_file_hash(
	packet_dir: Path,
	relative: Any,
	declared_hash: Any,
	errors: list[str],
	label: str,
) -> Path | None:
	if not isinstance(relative, str) or not relative:
		errors.append(f"{label} path is missing")
		return None
	path = _resolve_inside(packet_dir, relative, errors)
	if not path.is_file():
		errors.append(f"{label} file is missing: {relative}")
		return None
	if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(declared_hash):
		errors.append(f"{label} SHA-256 is invalid: {relative}")
	elif _sha256(path) != declared_hash:
		errors.append(f"{label} SHA-256 mismatch: {relative}")
	return path


def audit_shot(packet_dir: Path, card_path: Path) -> list[str]:
	errors: list[str] = []
	card = _load_json(card_path, errors)
	if card.get("schema") != SHOT_SCHEMA:
		errors.append(f"{card_path}: schema must be {SHOT_SCHEMA}")
	shot_id = card.get("shot_id")
	if not isinstance(shot_id, str) or not shot_id:
		errors.append(f"{card_path}: shot_id is missing")
	if card.get("mode") != "image_to_video":
		errors.append(f"{card_path}: mode must be image_to_video")
	if card.get("output_disposition") != "motion_reference_only":
		errors.append(f"{card_path}: output_disposition must be motion_reference_only")
	duration = card.get("duration_seconds")
	if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not 2 <= duration <= 8:
		errors.append(f"{card_path}: duration_seconds must be from 2 through 8")
	if card.get("aspect_ratio") != "16:9" or card.get("delivery_size") != [1280, 720]:
		errors.append(f"{card_path}: aspect_ratio/delivery_size must be 16:9 and 1280x720")

	refs = card.get("bound_references")
	if not isinstance(refs, list) or not 2 <= len(refs) <= 4:
		errors.append(f"{card_path}: bound_references must contain 2 through 4 images")
		refs = []
	for index, ref in enumerate(refs, start=1):
		if not isinstance(ref, dict):
			errors.append(f"{card_path}: reference {index} must be an object")
			continue
		expected_id = f"IMAGE_{index}"
		if ref.get("id") != expected_id:
			errors.append(f"{card_path}: reference {index} id must be {expected_id}")
		role = ref.get("role")
		if role not in ALLOWED_REFERENCE_ROLES:
			errors.append(f"{card_path}: {expected_id} has invalid role {role!r}")
		relative = ref.get("path")
		if isinstance(relative, str) and any(token in relative.lower() for token in FORBIDDEN_PIXEL_PATH_TOKENS):
			errors.append(f"{card_path}: forbidden bound pixel reference {relative}")
		path = _check_file_hash(packet_dir, relative, ref.get("sha256"), errors, expected_id)
		if path is not None and path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
			errors.append(f"{card_path}: {expected_id} must be a raster image")
		if ref.get("hud_present") is not False:
			errors.append(f"{card_path}: {expected_id} must declare hud_present false")
		if ref.get("human_decision") != "accepted":
			errors.append(f"{card_path}: {expected_id} must be human accepted")
	if refs and refs[0].get("role") != "approved_clean_first_frame":
		errors.append(f"{card_path}: IMAGE_1 must be the approved clean first frame")

	for item in card.get("non_pixel_references", []):
		if not isinstance(item, dict) or item.get("used_as_pixel_reference") is not False:
			errors.append(f"{card_path}: non-pixel references must declare used_as_pixel_reference false")

	camera = card.get("camera")
	if not isinstance(camera, dict) or camera.get("move_count") not in (0, 1) or not camera.get("verb"):
		errors.append(f"{card_path}: camera requires one verb and move_count 0 or 1")
	for field in ("must_move", "must_not_move", "end_state", "negative_constraints"):
		value = card.get(field)
		if not isinstance(value, (str, list)) or not value:
			errors.append(f"{card_path}: {field} is required")

	prompt_path = _check_file_hash(
		packet_dir,
		card.get("prompt_path"),
		card.get("prompt_sha256"),
		errors,
		"prompt",
	)
	if prompt_path is not None:
		prompt = prompt_path.read_text(encoding="utf-8")
		prompt_lower = prompt.lower()
		if "sound:" not in prompt_lower:
			errors.append(f"{card_path}: prompt must contain Sound:")
		if "end:" not in prompt_lower:
			errors.append(f"{card_path}: prompt must contain end:")
		for token in FORBIDDEN_PROMPT_TOKENS:
			if token in prompt_lower:
				errors.append(f"{card_path}: archive metadata token leaked into prompt: {token}")
	return errors


def audit_handoff(packet_dir: Path, require_ready: bool = False) -> list[str]:
	errors: list[str] = []
	manifest_path = packet_dir / HANDOFF_NAME
	manifest = _load_json(manifest_path, errors)
	if manifest.get("schema") != HANDOFF_SCHEMA:
		errors.append(f"{manifest_path}: schema must be {HANDOFF_SCHEMA}")
	if manifest.get("archive_status") not in {"complete", "incomplete"}:
		errors.append(f"{manifest_path}: archive_status must be complete or incomplete")
	if manifest.get("archive_status") == "complete":
		remote = manifest.get("archive_remote")
		if not isinstance(remote, dict):
			errors.append(f"{manifest_path}: complete archive requires archive_remote verification")
		else:
			commit = remote.get("commit")
			if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
				errors.append(f"{manifest_path}: archive_remote commit must be a full Git SHA")
			for field in ("tree", "manifest"):
				url = remote.get(field)
				if not isinstance(url, str) or "github" not in url or not isinstance(commit, str) or commit not in url:
					errors.append(f"{manifest_path}: archive_remote {field} must use the immutable commit")
			if not remote.get("verified_via") or not remote.get("verified_at"):
				errors.append(f"{manifest_path}: archive_remote verification evidence is incomplete")
	generation_status = manifest.get("generation_status")
	if generation_status not in {"blocked", "ready"}:
		errors.append(f"{manifest_path}: generation_status must be blocked or ready")
	if manifest.get("delivery_status") not in {"not_accepted", "accepted"}:
		errors.append(f"{manifest_path}: delivery_status must be not_accepted or accepted")
	findings = manifest.get("blocking_findings")
	shot_paths = manifest.get("shot_packets")
	if not isinstance(shot_paths, list):
		errors.append(f"{manifest_path}: shot_packets must be a list")
		shot_paths = []
	if generation_status == "blocked":
		if not isinstance(findings, list) or not findings:
			errors.append(f"{manifest_path}: blocked handoff requires blocking_findings")
		if require_ready:
			errors.append(f"{manifest_path}: GENERATION_READY is required but status is blocked")
	elif generation_status == "ready":
		if findings not in ([], None):
			errors.append(f"{manifest_path}: ready handoff cannot retain blocking_findings")
		if not shot_paths:
			errors.append(f"{manifest_path}: ready handoff requires shot packets")

	seen_shots: set[str] = set()
	for relative in shot_paths:
		if not isinstance(relative, str):
			errors.append(f"{manifest_path}: shot packet path must be text")
			continue
		card_path = _resolve_inside(packet_dir, relative, errors)
		if not card_path.is_file():
			errors.append(f"{manifest_path}: shot packet is missing: {relative}")
			continue
		card = _load_json(card_path, errors)
		shot_id = card.get("shot_id")
		if shot_id in seen_shots:
			errors.append(f"{manifest_path}: duplicate shot_id {shot_id}")
		elif isinstance(shot_id, str):
			seen_shots.add(shot_id)
		errors.extend(audit_shot(packet_dir, card_path))
	return errors


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument("packet", nargs="*", type=Path)
	parser.add_argument("--all", action="store_true", dest="audit_all")
	parser.add_argument("--require-ready", action="store_true")
	return parser.parse_args()


def main() -> int:
	args = _parse_args()
	packets = [path.resolve() for path in args.packet]
	if args.audit_all:
		packets.extend(path.parent for path in sorted((ROOT / "assets_src" / "cinematics").glob(f"**/{HANDOFF_NAME}")))
	packets = list(dict.fromkeys(packets))
	if not packets:
		print("IMAGINE|RESULT|FAIL|no handoff packets selected")
		return 1
	failed = False
	for packet in packets:
		errors = audit_handoff(packet, args.require_ready)
		status = "FAIL" if errors else "PASS"
		print(f"IMAGINE|PACKET|{packet}|{status}")
		for error in errors:
			print(f"IMAGINE|ERROR|{error}")
		failed = failed or bool(errors)
	print(f"IMAGINE|RESULT|{'FAIL' if failed else 'ALL OK'}")
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())
