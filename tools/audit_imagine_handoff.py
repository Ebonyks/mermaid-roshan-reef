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
SHOT_SCHEMA_V1 = "imagine-shot-packet-v1"
SHOT_SCHEMA_V2 = "imagine-shot-packet-v2"
HANDOFF_SCHEMA_V1 = "imagine-handoff-v1"
HANDOFF_SCHEMA_V2 = "imagine-handoff-v2"
ALLOWED_REFERENCE_ROLES = {
	"approved_clean_first_frame",
	"subject_identity",
	"relationship_scale_contact",
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
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
IMMUTABLE_GITHUB_RE = re.compile(r"https://(?:raw\.githubusercontent\.com|github\.com)/.+/[0-9a-f]{40}/")


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


def _nonempty_string_list(value: Any, minimum: int = 1) -> bool:
	return (
		isinstance(value, list)
		and len(value) >= minimum
		and all(isinstance(item, str) and item.strip() for item in value)
	)


def _audit_v2_shot_contract(
	card: dict[str, Any],
	card_path: Path,
	refs: list[dict[str, Any]],
	prompt: str,
	handoff: dict[str, Any],
	errors: list[str],
) -> None:
	reference_by_id = {ref.get("id"): ref for ref in refs if isinstance(ref, dict)}
	exact_cast = card.get("exact_cast")
	if not isinstance(exact_cast, list) or not all(isinstance(item, str) and item for item in exact_cast):
		errors.append(f"{card_path}: exact_cast must be a list of stable character IDs")
		exact_cast = []
	if len(exact_cast) != len(set(exact_cast)):
		errors.append(f"{card_path}: exact_cast contains duplicate character IDs")

	authority_items = handoff.get("character_authorities", [])
	if not isinstance(authority_items, list):
		authority_items = []
	authorities = {
		item.get("character_id"): item
		for item in authority_items
		if isinstance(item, dict) and isinstance(item.get("character_id"), str)
	}
	locks = card.get("character_locks")
	if not isinstance(locks, list):
		errors.append(f"{card_path}: character_locks must be a list")
		locks = []
	locked_ids: list[str] = []
	for lock in locks:
		if not isinstance(lock, dict):
			errors.append(f"{card_path}: each character lock must be an object")
			continue
		character_id = lock.get("character_id")
		if not isinstance(character_id, str) or not character_id:
			errors.append(f"{card_path}: character lock is missing character_id")
			continue
		locked_ids.append(character_id)
		authority = authorities.get(character_id)
		if authority is None:
			errors.append(f"{card_path}: {character_id} is absent from handoff character_authorities")
		reference_id = lock.get("reference_id")
		ref = reference_by_id.get(reference_id)
		if not isinstance(ref, dict) or ref.get("role") != "subject_identity":
			errors.append(f"{card_path}: {character_id} lock must point to a subject_identity reference")
		elif authority is not None and ref.get("sha256") != authority.get("sha256"):
			errors.append(f"{card_path}: {character_id} bound identity hash differs from the handoff authority")
		for field, minimum in (("identity_invariants", 3), ("anatomy_invariants", 1), ("forbidden_changes", 2)):
			if not _nonempty_string_list(lock.get(field), minimum):
				errors.append(f"{card_path}: {character_id} {field} requires at least {minimum} explicit entries")
		for field in ("screen_role", "start_state", "end_state"):
			if not isinstance(lock.get(field), str) or not lock.get(field):
				errors.append(f"{card_path}: {character_id} {field} is required")
		phrases = lock.get("required_prompt_phrases")
		if not _nonempty_string_list(phrases, 2):
			errors.append(f"{card_path}: {character_id} requires at least two prompt lock phrases")
		else:
			for phrase in phrases:
				if phrase.casefold() not in prompt.casefold():
					errors.append(f"{card_path}: character lock phrase is missing from prompt: {phrase}")
	if set(exact_cast) != set(locked_ids):
		errors.append(f"{card_path}: exact_cast and character_locks must name the same characters")

	location = card.get("location_lock")
	if not isinstance(location, dict):
		errors.append(f"{card_path}: location_lock is required")
	else:
		if location.get("reference_id") != "IMAGE_1":
			errors.append(f"{card_path}: location_lock reference_id must be IMAGE_1")
		for field, minimum in (("immutable_features", 2), ("forbidden_geometry", 1)):
			if not _nonempty_string_list(location.get(field), minimum):
				errors.append(f"{card_path}: location_lock {field} requires at least {minimum} entries")
		phrases = location.get("required_prompt_phrases")
		if not _nonempty_string_list(phrases):
			errors.append(f"{card_path}: location_lock requires a prompt lock phrase")
		else:
			for phrase in phrases:
				if phrase.casefold() not in prompt.casefold():
					errors.append(f"{card_path}: location lock phrase is missing from prompt: {phrase}")

	causal = card.get("causal_chain")
	if not isinstance(causal, dict) or any(not isinstance(causal.get(field), str) or not causal.get(field) for field in ("trigger", "visible_change", "end_confirmation")):
		errors.append(f"{card_path}: causal_chain requires trigger, visible_change, and end_confirmation")

	continuity = card.get("continuity")
	if not isinstance(continuity, dict):
		errors.append(f"{card_path}: continuity contract is required")
	else:
		kind = continuity.get("kind")
		if kind not in {"new_setup", "authored_cut", "continuous_action", "intentional_hold"}:
			errors.append(f"{card_path}: continuity kind is invalid")
		for field in ("inherited_state", "allowed_changes"):
			if not _nonempty_string_list(continuity.get(field)):
				errors.append(f"{card_path}: continuity {field} must be explicit")
		first_ref = refs[0] if refs and isinstance(refs[0], dict) else {}
		source_kind = first_ref.get("source_kind")
		if kind == "continuous_action":
			if source_kind != "accepted_previous_end":
				errors.append(f"{card_path}: continuous_action must use an accepted_previous_end as IMAGE_1")
			if continuity.get("previous_end_sha256") != first_ref.get("sha256"):
				errors.append(f"{card_path}: previous_end_sha256 must equal IMAGE_1")
		elif source_kind != "approved_master":
			errors.append(f"{card_path}: a new setup/cut/hold must use an approved_master as IMAGE_1")

	for field in ("sequence_position",):
		if not isinstance(card.get(field), int) or isinstance(card.get(field), bool) or card.get(field) < 0:
			errors.append(f"{card_path}: {field} must be a non-negative integer")
	if not _nonempty_string_list(card.get("beat_ids")):
		errors.append(f"{card_path}: beat_ids must name at least one story-contract beat")

	end_state = card.get("end_state")
	if isinstance(end_state, str) and end_state.casefold() not in prompt.casefold():
		errors.append(f"{card_path}: exact end_state must appear in the prompt")


def audit_shot(
	packet_dir: Path,
	card_path: Path,
	handoff: dict[str, Any] | None = None,
) -> list[str]:
	errors: list[str] = []
	card = _load_json(card_path, errors)
	schema = card.get("schema")
	if schema not in {SHOT_SCHEMA_V1, SHOT_SCHEMA_V2}:
		errors.append(f"{card_path}: schema must be {SHOT_SCHEMA_V1} or {SHOT_SCHEMA_V2}")
	is_v2 = schema == SHOT_SCHEMA_V2
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
		if is_v2:
			if not isinstance(ref.get("authority_domain"), str) or not ref.get("authority_domain"):
				errors.append(f"{card_path}: {expected_id} must declare one authority_domain")
			remote_url = ref.get("remote_url")
			if not isinstance(remote_url, str) or not IMMUTABLE_GITHUB_RE.search(remote_url):
				errors.append(f"{card_path}: {expected_id} requires an immutable GitHub URL")
			else:
				commit = (handoff or {}).get("archive_remote", {}).get("commit")
				if isinstance(commit, str) and commit not in remote_url:
					errors.append(f"{card_path}: {expected_id} remote URL must use the archive content commit")
	if refs and (not isinstance(refs[0], dict) or refs[0].get("role") != "approved_clean_first_frame"):
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
	prompt = ""
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
	if is_v2:
		_audit_v2_shot_contract(card, card_path, refs, prompt, handoff or {}, errors)
	return errors


def audit_handoff(packet_dir: Path, require_ready: bool = False) -> list[str]:
	errors: list[str] = []
	manifest_path = packet_dir / HANDOFF_NAME
	manifest = _load_json(manifest_path, errors)
	schema = manifest.get("schema")
	if schema not in {HANDOFF_SCHEMA_V1, HANDOFF_SCHEMA_V2}:
		errors.append(f"{manifest_path}: schema must be {HANDOFF_SCHEMA_V1} or {HANDOFF_SCHEMA_V2}")
	is_v2 = schema == HANDOFF_SCHEMA_V2
	if manifest.get("archive_status") not in {"complete", "incomplete"}:
		errors.append(f"{manifest_path}: archive_status must be complete or incomplete")
	if manifest.get("archive_status") == "complete":
		remote = manifest.get("archive_remote")
		if not isinstance(remote, dict):
			errors.append(f"{manifest_path}: complete archive requires archive_remote verification")
		else:
			commit = remote.get("commit")
			if not isinstance(commit, str) or not GIT_SHA_RE.fullmatch(commit):
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
	shot_cards: list[dict[str, Any]] = []
	for relative in shot_paths:
		if not isinstance(relative, str):
			errors.append(f"{manifest_path}: shot packet path must be text")
			continue
		card_path = _resolve_inside(packet_dir, relative, errors)
		if not card_path.is_file():
			errors.append(f"{manifest_path}: shot packet is missing: {relative}")
			continue
		card = _load_json(card_path, errors)
		shot_cards.append(card)
		if is_v2 and card.get("schema") != SHOT_SCHEMA_V2:
			errors.append(f"{manifest_path}: V2 handoff requires V2 shot packet: {relative}")
		shot_id = card.get("shot_id")
		if shot_id in seen_shots:
			errors.append(f"{manifest_path}: duplicate shot_id {shot_id}")
		elif isinstance(shot_id, str):
			seen_shots.add(shot_id)
		errors.extend(audit_shot(packet_dir, card_path, manifest))

	if is_v2:
		story = manifest.get("story_contract")
		if not isinstance(story, dict):
			errors.append(f"{manifest_path}: story_contract is required")
			story = {}
		for field in ("one_sentence_promise", "final_state"):
			if not isinstance(story.get(field), str) or not story.get(field):
				errors.append(f"{manifest_path}: story_contract {field} is required")
		beats = story.get("ordered_beats")
		if not isinstance(beats, list) or not beats or not all(isinstance(item, dict) and item.get("beat_id") and item.get("trigger") and item.get("visible_result") for item in beats):
			errors.append(f"{manifest_path}: story_contract requires ordered beats with trigger and visible_result")
			beats = []
		beat_ids = [item.get("beat_id") for item in beats]
		if len(beat_ids) != len(set(beat_ids)):
			errors.append(f"{manifest_path}: story beat IDs must be unique")
		if not _nonempty_string_list(story.get("forbidden_events"), 2):
			errors.append(f"{manifest_path}: story_contract requires at least two forbidden events")

		characters = manifest.get("character_authorities")
		if not isinstance(characters, list):
			errors.append(f"{manifest_path}: character_authorities must be a list")
			characters = []
		character_ids: list[str] = []
		for character in characters:
			if not isinstance(character, dict):
				errors.append(f"{manifest_path}: each character authority must be an object")
				continue
			character_id = character.get("character_id")
			if not isinstance(character_id, str) or not character_id:
				errors.append(f"{manifest_path}: character authority is missing character_id")
				continue
			character_ids.append(character_id)
			if character.get("status") not in {"approved", "approved_private_canon"}:
				errors.append(f"{manifest_path}: {character_id} is not approved character authority")
			_check_file_hash(packet_dir, character.get("path"), character.get("sha256"), errors, f"character {character_id}")
			for field, minimum in (("immutable_traits", 3), ("anatomy_traits", 1), ("forbidden_drift", 2)):
				if not _nonempty_string_list(character.get(field), minimum):
					errors.append(f"{manifest_path}: {character_id} {field} requires at least {minimum} entries")
		if len(character_ids) != len(set(character_ids)):
			errors.append(f"{manifest_path}: character authority IDs must be unique")

		location = manifest.get("location_authority")
		if not isinstance(location, dict):
			errors.append(f"{manifest_path}: location_authority is required")
		else:
			_check_file_hash(packet_dir, location.get("path"), location.get("sha256"), errors, "location authority")
			for field, minimum in (("immutable_features", 3), ("forbidden_geometry", 1)):
				if not _nonempty_string_list(location.get(field), minimum):
					errors.append(f"{manifest_path}: location_authority {field} requires at least {minimum} entries")

		positions = [card.get("sequence_position") for card in shot_cards]
		if positions != list(range(len(shot_cards))):
			errors.append(f"{manifest_path}: shot packets must be ordered with contiguous sequence_position values")
		used_beats: set[str] = set()
		for card in shot_cards:
			card_beats = card.get("beat_ids", [])
			if isinstance(card_beats, list):
				used_beats.update(beat for beat in card_beats if isinstance(beat, str))
		unknown_beats = used_beats - set(beat_ids)
		if unknown_beats:
			errors.append(f"{manifest_path}: shots reference unknown story beats: {sorted(unknown_beats)}")
		missing_beats = set(beat_ids) - used_beats
		if generation_status == "ready" and missing_beats:
			errors.append(f"{manifest_path}: ready handoff leaves story beats uncovered: {sorted(missing_beats)}")
		for index, card in enumerate(shot_cards):
			continuity = card.get("continuity", {})
			previous_id = continuity.get("previous_shot_id") if isinstance(continuity, dict) else None
			expected_previous = shot_cards[index - 1].get("shot_id") if index else None
			if previous_id != expected_previous:
				errors.append(f"{manifest_path}: {card.get('shot_id')} previous_shot_id must be {expected_previous!r}")
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
