#!/usr/bin/env python3
"""Audit footage-aware Grok handoffs without changing the handoff packet.

This is deliberately separate from ``audit_imagine_handoff.py``.  The older
audit proves that a packet is structurally well-formed; this audit also checks
the evidence chain that makes a continuity handoff believable: optional
footage-analysis records, local clip hashes and metadata, accepted endpoint
candidates, and one V2 card for every planned shot.

Blocked packets are useful drafts.  They therefore report readiness blockers
but return success when their existing structure is sound.  A ready claim, or
``--require-ready``, is fail-closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
HANDOFF_NAME = "IMAGINE_HANDOFF.json"
SHOT_SCHEMA_V2 = "imagine-shot-packet-v2"
HANDOFF_SCHEMA_V2 = "imagine-handoff-v2"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
IMMUTABLE_GITHUB_RE = re.compile(
	r"https://(?:raw\.githubusercontent\.com|github\.com)/.+/[0-9a-f]{40}/"
)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
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
	"contact_sheet",
	"montage",
	"runtime_boundary",
	"runtime_anchor",
)


@dataclass
class AuditReport:
	"""Results for one packet.

	``errors`` are structural or contradictory-claim failures.  ``blockers``
	are truthful reasons a blocked draft cannot yet claim generation readiness.
	"""

	packet: Path
	errors: list[str] = field(default_factory=list)
	blockers: list[str] = field(default_factory=list)
	notes: list[str] = field(default_factory=list)

	@property
	def passed(self) -> bool:
		return not self.errors


def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def _load_json(path: Path, report: AuditReport) -> dict[str, Any]:
	try:
		value = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		report.errors.append(f"cannot read JSON {path}: {exc}")
		return {}
	if not isinstance(value, dict):
		report.errors.append(f"JSON root must be an object: {path}")
		return {}
	return value


def _resolve_inside(packet: Path, relative: Any, report: AuditReport, label: str) -> Path | None:
	if not isinstance(relative, str) or not relative.strip():
		report.errors.append(f"{label} path is missing")
		return None
	path = (packet / relative).resolve()
	try:
		path.relative_to(packet.resolve())
	except ValueError:
		report.errors.append(f"{label} path escapes packet: {relative}")
		return None
	return path


def _checked_file(
	packet: Path,
	relative: Any,
	declared_hash: Any,
	report: AuditReport,
	label: str,
	allow_missing_hash: bool = False,
) -> Path | None:
	path = _resolve_inside(packet, relative, report, label)
	if path is None:
		return None
	if not path.is_file():
		report.errors.append(f"{label} file is missing: {relative}")
		return None
	if not isinstance(declared_hash, str) or not SHA256_RE.fullmatch(declared_hash):
		if not allow_missing_hash:
			report.errors.append(f"{label} SHA-256 is invalid: {relative}")
	elif _sha256(path) != declared_hash:
		report.errors.append(f"{label} SHA-256 mismatch: {relative}")
	return path


def _nonempty_strings(value: Any, minimum: int = 1) -> bool:
	return (
		isinstance(value, list)
		and len(value) >= minimum
		and all(isinstance(item, str) and item.strip() for item in value)
	)


def _number(value: Any) -> bool:
	return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _record_values(value: Any, packet: Path, report: AuditReport, label: str) -> list[dict[str, Any]]:
	"""Normalize an inline record, list, or JSON path into record objects."""
	if value is None:
		return []
	if isinstance(value, str):
		path = _resolve_inside(packet, value, report, label)
		if path is None or not path.is_file():
			if path is not None:
				report.errors.append(f"{label} file is missing: {value}")
			return []
		loaded = _load_json(path, report)
		return _record_values(loaded, packet, report, label)
	if isinstance(value, list):
		result: list[dict[str, Any]] = []
		for index, item in enumerate(value):
			if isinstance(item, str):
				result.extend(_record_values(item, packet, report, f"{label}[{index}]") )
			elif isinstance(item, dict):
				result.append(item)
			else:
				report.errors.append(f"{label}[{index}] must be an object or JSON path")
		return result
	if isinstance(value, dict):
		for key in ("records", "analyses", "footage_records", "clips"):
			if key in value and isinstance(value[key], list) and key != "clips":
				return _record_values(value[key], packet, report, f"{label}.{key}")
		return [value]
	report.errors.append(f"{label} must be an object, list, or JSON path")
	return []


def _analysis_records(packet: Path, handoff: dict[str, Any], report: AuditReport) -> list[dict[str, Any]]:
	"""Read inline or conventional footage-analysis records, if supplied."""
	if "footage_analysis" in handoff:
		return _record_values(handoff.get("footage_analysis"), packet, report, "footage_analysis")
	for relative in (
		"FOOTAGE_ANALYSIS.json",
		"analysis/FOOTAGE_ANALYSIS.json",
		"footage/ANALYSIS.json",
		"footage_analysis.json",
	):
		path = packet / relative
		if path.is_file():
			return _record_values(relative, packet, report, "footage_analysis")
	return []


def _endpoint_records(packet: Path, handoff: dict[str, Any], report: AuditReport) -> list[dict[str, Any]]:
	"""Read endpoint candidates kept in a separate sidecar, when present."""
	value = handoff.get("endpoint_candidates", handoff.get("accepted_endpoints"))
	if value is not None:
		return _record_values(value, packet, report, "endpoint_candidates")
	for relative in (
		"ENDPOINT_CANDIDATES.json",
		"analysis/ENDPOINT_CANDIDATES.json",
		"endpoints.json",
	):
		if (packet / relative).is_file():
			return _record_values(relative, packet, report, "endpoint_candidates")
	return []


def _clip_items(record: dict[str, Any]) -> list[dict[str, Any]]:
	clips = record.get("clips")
	if isinstance(record.get("clip"), dict):
		clips = [record["clip"]]
	if clips is None and any(key in record for key in ("clip_id", "clip_path", "clip", "video_path")):
		clips = [record]
	if not isinstance(clips, list):
		return []
	return [item for item in clips if isinstance(item, dict)]


def _clip_path(item: dict[str, Any]) -> Any:
	return item.get("path", item.get("clip_path", item.get("relative_path", item.get("video_path", item.get("file")))))


def _clip_hash(item: dict[str, Any]) -> Any:
	return item.get("sha256", item.get("clip_sha256", item.get("hash")))


def _audit_footage(
	packet: Path,
	handoff: dict[str, Any],
	report: AuditReport,
	force_required: bool,
) -> tuple[set[str], set[str]]:
	records = _analysis_records(packet, handoff, report)
	required = force_required or handoff.get("footage_analysis_required") is True
	if not records:
		if required:
			report.blockers.append("required footage-analysis record is missing")
		else:
			report.notes.append("no footage-analysis record supplied (optional for a blocked draft)")
		return set(), set()

	clip_ids: set[str] = set()
	accepted_endpoint_hashes: set[str] = set()
	for record_index, record in enumerate(records):
		clips = _clip_items(record)
		if not clips:
			report.errors.append(f"footage_analysis[{record_index}] has no clip records")
		for clip_index, clip in enumerate(clips):
			label = f"footage_analysis[{record_index}].clips[{clip_index}]"
			clip_id = clip.get("clip_id", clip.get("id"))
			if not isinstance(clip_id, str) or not clip_id.strip():
				report.errors.append(f"{label} clip_id is required")
			else:
				clip_ids.add(clip_id)
			path = _checked_file(packet, _clip_path(clip), _clip_hash(clip), report, label)
			if path is not None and path.suffix.lower() not in VIDEO_EXTENSIONS:
				report.errors.append(f"{label} must point to a video clip: {path.name}")
			metadata = clip.get("metadata") if isinstance(clip.get("metadata"), dict) else {}
			resolution = clip.get("resolution", metadata.get("resolution"))
			width = clip.get("width", metadata.get("width"))
			height = clip.get("height", metadata.get("height"))
			if isinstance(resolution, list) and len(resolution) == 2:
				width, height = resolution
			if not _number(width) or not _number(height):
				report.errors.append(f"{label} requires positive width and height metadata")
			duration = clip.get("duration_seconds", clip.get("duration", metadata.get("duration_seconds", metadata.get("duration"))))
			fps = clip.get("fps", clip.get("frame_rate", metadata.get("fps", metadata.get("frame_rate"))))
			if not _number(duration):
				report.errors.append(f"{label} requires positive duration_seconds metadata")
			if not _number(fps):
				report.errors.append(f"{label} requires positive fps metadata")
			for endpoint in clip.get("endpoint_candidates", []):
				if isinstance(endpoint, dict):
					accepted_endpoint_hashes.update(_audit_endpoint(endpoint, packet, report, label))

		for endpoint in record.get("endpoint_candidates", record.get("endpoints", [])):
			if isinstance(endpoint, dict):
				accepted_endpoint_hashes.update(_audit_endpoint(endpoint, packet, report, f"footage_analysis[{record_index}]"))

	# A top-level manifest may keep endpoint candidates beside footage_analysis.
	for endpoint_record in _endpoint_records(packet, handoff, report):
		endpoints = endpoint_record.get("endpoint_candidates", endpoint_record.get("endpoints"))
		if isinstance(endpoints, list):
			for endpoint in endpoints:
				if isinstance(endpoint, dict):
					accepted_endpoint_hashes.update(_audit_endpoint(endpoint, packet, report, "endpoint_candidates"))
		elif any(key in endpoint_record for key in ("path", "frame_path", "sha256")):
			accepted_endpoint_hashes.update(_audit_endpoint(endpoint_record, packet, report, "endpoint_candidates"))
	return clip_ids, accepted_endpoint_hashes


def _audit_endpoint(
	endpoint: dict[str, Any],
	packet: Path,
	report: AuditReport,
	label: str,
) -> set[str]:
	path = _checked_file(packet, endpoint.get("path", endpoint.get("frame_path")), endpoint.get("sha256"), report, f"{label} endpoint")
	if path is not None and path.suffix.lower() not in IMAGE_EXTENSIONS:
		report.errors.append(f"{label} endpoint must be a raster image")
	decision = endpoint.get("human_decision", endpoint.get("decision"))
	if decision not in {"accepted", "rejected", "pending"}:
		report.errors.append(f"{label} endpoint human_decision must be accepted, rejected, or pending")
	shot_id = endpoint.get("shot_id")
	if not isinstance(shot_id, str) or not shot_id.strip():
		report.errors.append(f"{label} endpoint shot_id is required")
	if decision == "accepted" and isinstance(endpoint.get("sha256"), str) and SHA256_RE.fullmatch(endpoint["sha256"]):
		return {endpoint["sha256"]}
	return set()


def _planned_shot_ids(
	handoff: dict[str, Any],
	packet: Path,
	shot_paths: Any = None,
	report: AuditReport | None = None,
) -> list[str]:
	planned = handoff.get("planned_shots")
	if isinstance(planned, list) and planned:
		result = []
		for item in planned:
			if isinstance(item, str):
				result.append(item)
			elif isinstance(item, dict) and isinstance(item.get("shot_id"), str):
				result.append(item["shot_id"])
		if result:
			return result
	story = handoff.get("story_contract")
	beats = story.get("ordered_beats") if isinstance(story, dict) else None
	if isinstance(beats, list):
		beat_ids = [item["beat_id"] for item in beats if isinstance(item, dict) and isinstance(item.get("beat_id"), str)]
		# Some valid cards use generic beat IDs (B01) while their shot IDs are
		# S01.  When cards are already present, use their declared shot IDs as
		# the planned-shot set and let beat coverage remain a card-level check.
		if beat_ids and not all(re.search(r"(?:^|-)S\d+$", item) for item in beat_ids) and isinstance(shot_paths, list):
			card_ids: list[str] = []
			for relative in shot_paths:
				if not isinstance(relative, str):
					continue
				path = (packet / relative).resolve()
				try:
					path.relative_to(packet.resolve())
				except ValueError:
					continue
				if path.is_file():
					try:
						value = json.loads(path.read_text(encoding="utf-8"))
					except (OSError, json.JSONDecodeError):
						continue
					if isinstance(value, dict) and isinstance(value.get("shot_id"), str):
						card_ids.append(value["shot_id"])
			if card_ids:
				return card_ids
		return beat_ids
	return []


def _prompt_and_card(
	packet: Path,
	card: dict[str, Any],
	card_path: Path,
	handoff: dict[str, Any],
	expected_position: int,
	expected_previous: str | None,
	accepted_endpoint_hashes: set[str],
	report: AuditReport,
) -> tuple[bool, str | None, str | None]:
	label = str(card_path)
	valid = True
	def fail(message: str) -> None:
		nonlocal valid
		valid = False
		report.errors.append(f"{label}: {message}")

	if card.get("schema") != SHOT_SCHEMA_V2:
		fail("schema must be imagine-shot-packet-v2")
	expected_movie_id = handoff.get("movie_id", handoff.get("handoff_id"))
	if expected_movie_id is not None and card.get("movie_id") != expected_movie_id:
		fail("movie_id does not match handoff")
	if card.get("sequence_position") != expected_position:
		fail(f"sequence_position must be {expected_position}")
	if card.get("mode") != "image_to_video" or card.get("output_disposition") != "motion_reference_only":
		fail("mode/output_disposition must be image_to_video/motion_reference_only")
	duration = card.get("duration_seconds")
	if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not 2 <= duration <= 8:
		fail("duration_seconds must be from 2 through 8")
	if card.get("aspect_ratio") != "16:9" or card.get("delivery_size") != [1280, 720]:
		fail("aspect_ratio/delivery_size must be 16:9 and 1280x720")
	if not _nonempty_strings(card.get("beat_ids")):
		fail("beat_ids must list at least one story beat")

	refs = card.get("bound_references")
	if not isinstance(refs, list) or not 2 <= len(refs) <= 4:
		fail("bound_references must contain 2 through 4 images")
		refs = []
	ref_hashes: list[str] = []
	for index, ref in enumerate(refs):
		rlabel = f"{label} IMAGE_{index + 1}"
		if not isinstance(ref, dict):
			fail(f"reference {index + 1} must be an object")
			continue
		expected_id = f"IMAGE_{index + 1}"
		if ref.get("id") != expected_id:
			fail(f"reference {index + 1} id must be {expected_id}")
		if ref.get("role") not in ALLOWED_REFERENCE_ROLES:
			fail(f"{expected_id} has an invalid role")
		path_value = ref.get("path")
		if isinstance(path_value, str) and any(token in path_value.lower() for token in FORBIDDEN_PIXEL_PATH_TOKENS):
			fail(f"{expected_id} uses a forbidden narrative pixel path")
		path = _checked_file(packet, path_value, ref.get("sha256"), report, rlabel)
		if path is not None and path.suffix.lower() not in IMAGE_EXTENSIONS:
			fail(f"{expected_id} must be a raster image")
		if ref.get("hud_present") is not False:
			fail(f"{expected_id} must declare hud_present false")
		if ref.get("human_decision") != "accepted":
			fail(f"{expected_id} must be human accepted")
		if not isinstance(ref.get("authority_domain"), str) or not ref["authority_domain"].strip():
			fail(f"{expected_id} must declare authority_domain")
		if not isinstance(ref.get("remote_url"), str) or not IMMUTABLE_GITHUB_RE.search(ref["remote_url"]):
			fail(f"{expected_id} requires an immutable GitHub URL")
		ref_hashes.append(ref.get("sha256", ""))
	if refs and (refs[0].get("role") != "approved_clean_first_frame" if isinstance(refs[0], dict) else True):
		fail("IMAGE_1 must be the approved clean first frame")
	if refs and isinstance(refs[0], dict) and refs[0].get("source_kind") not in {"approved_master", "accepted_previous_end"}:
		fail("IMAGE_1 source_kind must be approved_master or accepted_previous_end")

	continuity = card.get("continuity")
	if not isinstance(continuity, dict):
		fail("continuity contract is required")
		continuity = {}
	kind = continuity.get("kind")
	if kind not in {"new_setup", "authored_cut", "continuous_action", "intentional_hold"}:
		fail("continuity kind is invalid")
	if continuity.get("previous_shot_id") != expected_previous:
		fail(f"previous_shot_id must be {expected_previous!r}")
	if not _nonempty_strings(continuity.get("inherited_state")):
		fail("continuity inherited_state is required")
	if not _nonempty_strings(continuity.get("allowed_changes")):
		fail("continuity allowed_changes is required")
	first_hash = ref_hashes[0] if ref_hashes else ""
	if kind == "continuous_action":
		if refs and refs[0].get("source_kind") != "accepted_previous_end":
			fail("continuous_action must use accepted_previous_end as IMAGE_1")
		if continuity.get("previous_end_sha256") != first_hash:
			fail("previous_end_sha256 must equal IMAGE_1")
		if first_hash not in accepted_endpoint_hashes:
			report.blockers.append(f"{card.get('shot_id')}: IMAGE_1 accepted_previous_end has no accepted endpoint candidate record")
	else:
		if refs and refs[0].get("source_kind") != "approved_master":
			fail("new setup/cut/hold must use approved_master as IMAGE_1")

	for field_name in ("must_move", "must_not_move", "end_state", "negative_constraints"):
		value = card.get(field_name)
		if not ((isinstance(value, str) and value.strip()) or _nonempty_strings(value)):
			fail(f"{field_name} is required")
	camera = card.get("camera")
	if not isinstance(camera, dict) or not isinstance(camera.get("verb"), str) or camera.get("move_count") not in (0, 1):
		fail("camera requires a verb and move_count 0 or 1")
	causal = card.get("causal_chain")
	if not isinstance(causal, dict) or any(not isinstance(causal.get(key), str) or not causal[key].strip() for key in ("trigger", "visible_change", "end_confirmation")):
		fail("causal_chain requires trigger, visible_change, and end_confirmation")

	prompt_path = _checked_file(packet, card.get("prompt_path"), card.get("prompt_sha256"), report, "prompt")
	prompt = ""
	if prompt_path is not None:
		prompt = prompt_path.read_text(encoding="utf-8")
		if "sound:" not in prompt.casefold():
			fail("prompt must contain Sound:")
		if "end:" not in prompt.casefold():
			fail("prompt must contain end:")
		if any(token in prompt.casefold() for token in ("sha256", "license_provenance", "archive_complete", "delivery_accepted")):
			fail("prompt contains archive metadata")
	end_state = card.get("end_state")
	if isinstance(end_state, str) and end_state.casefold() not in prompt.casefold():
		fail("exact end_state must appear in prompt")

	# V2 character locks are required when the handoff has character authorities.
	authorities = {item.get("character_id"): item for item in handoff.get("character_authorities", []) if isinstance(item, dict)}
	exact_cast = card.get("exact_cast")
	locks = card.get("character_locks")
	if authorities:
		if not isinstance(exact_cast, list) or not all(isinstance(item, str) for item in exact_cast):
			fail("exact_cast is required")
		if not isinstance(locks, list):
			fail("character_locks is required")
			locks = []
		locked = {item.get("character_id") for item in locks if isinstance(item, dict)}
		if set(exact_cast or []) != locked:
			fail("exact_cast and character_locks must name the same characters")
		ref_by_id = {item.get("id"): item for item in refs if isinstance(item, dict)}
		for character_id in exact_cast or []:
			lock = next((item for item in locks if isinstance(item, dict) and item.get("character_id") == character_id), None)
			if lock is None:
				continue
			authority = authorities.get(character_id)
			identity_ref = ref_by_id.get(lock.get("reference_id"))
			if not isinstance(identity_ref, dict) or identity_ref.get("role") != "subject_identity":
				fail(f"{character_id} lock must point to subject_identity")
			elif authority is not None and identity_ref.get("sha256") != authority.get("sha256"):
				fail(f"{character_id} bound identity hash differs from authority")
			for field_name, minimum in (("identity_invariants", 3), ("anatomy_invariants", 1), ("forbidden_changes", 2), ("required_prompt_phrases", 2)):
				if not _nonempty_strings(lock.get(field_name), minimum):
					fail(f"{character_id} {field_name} requires at least {minimum} entries")
			for field_name in ("screen_role", "start_state", "end_state"):
				if not isinstance(lock.get(field_name), str) or not lock[field_name].strip():
					fail(f"{character_id} {field_name} is required")
			for phrase in lock.get("required_prompt_phrases", []):
				if phrase.casefold() not in prompt.casefold():
					fail(f"{character_id} prompt phrase is missing: {phrase}")
	location = card.get("location_lock")
	if not isinstance(location, dict) or location.get("reference_id") != "IMAGE_1":
		fail("location_lock must reference IMAGE_1")
	elif not _nonempty_strings(location.get("immutable_features"), 2) or not _nonempty_strings(location.get("forbidden_geometry")):
		fail("location_lock requires immutable_features and forbidden_geometry")
	if not isinstance(card.get("shot_id"), str) or not card["shot_id"].strip():
		fail("shot_id is required")
	return valid, card.get("shot_id"), first_hash


def _archive_claim_check(handoff: dict[str, Any], report: AuditReport) -> None:
	if handoff.get("archive_status") != "complete":
		report.blockers.append("archive_status is not complete")
		return
	remote = handoff.get("archive_remote")
	if not isinstance(remote, dict):
		report.errors.append("ready archive requires archive_remote verification")
		return
	commit = remote.get("commit")
	if not isinstance(commit, str) or not GIT_SHA_RE.fullmatch(commit):
		report.errors.append("archive_remote commit must be a full Git SHA")
		return
	for key in ("tree", "manifest"):
		url = remote.get(key)
		if not isinstance(url, str) or "github" not in url or commit not in url:
			report.errors.append(f"archive_remote {key} must use the immutable commit")
	if not remote.get("verified_via") or not remote.get("verified_at"):
		report.errors.append("archive_remote verification evidence is incomplete")


def audit_packet(
	packet: Path,
	require_ready: bool = False,
	require_footage_analysis: bool = False,
) -> AuditReport:
	"""Audit one packet; blocked drafts produce blockers, not failures."""
	packet = packet.resolve()
	report = AuditReport(packet)
	handoff_path = packet / HANDOFF_NAME
	handoff = _load_json(handoff_path, report)
	if handoff.get("schema") != HANDOFF_SCHEMA_V2:
		report.errors.append(f"{handoff_path}: schema must be imagine-handoff-v2")
	status = handoff.get("generation_status")
	if status not in {"blocked", "ready"}:
		report.errors.append(f"{handoff_path}: generation_status must be blocked or ready")
	if handoff.get("delivery_status") not in {"not_accepted", "accepted"}:
		report.errors.append(f"{handoff_path}: delivery_status must be not_accepted or accepted")
	shot_paths = handoff.get("shot_packets")
	planned = _planned_shot_ids(handoff, packet, shot_paths, report)
	if not planned:
		report.errors.append(f"{handoff_path}: no planned shots found in story_contract or planned_shots")

	_, accepted_endpoint_hashes = _audit_footage(packet, handoff, report, require_footage_analysis)
	if not isinstance(shot_paths, list):
		report.errors.append(f"{handoff_path}: shot_packets must be a list")
		shot_paths = []
	if not shot_paths:
		report.blockers.append(f"no V2 shot cards supplied for planned shots: {', '.join(planned) or 'none'}")

	seen: set[str] = set()
	card_hashes: dict[str, str] = {}
	for relative in shot_paths:
		card_path = _resolve_inside(packet, relative, report, "shot packet")
		if card_path is None or not card_path.is_file():
			if card_path is not None:
				report.blockers.append(f"shot card is missing: {relative}")
			continue
		card = _load_json(card_path, report)
		shot_id = card.get("shot_id")
		position = planned.index(shot_id) if shot_id in planned else len(seen)
		previous = planned[position - 1] if position > 0 and position < len(planned) else None
		valid, parsed_id, first_hash = _prompt_and_card(packet, card, card_path, handoff, position, previous, accepted_endpoint_hashes, report)
		if parsed_id in seen:
			report.errors.append(f"duplicate shot_id: {parsed_id}")
		if isinstance(parsed_id, str):
			seen.add(parsed_id)
			if first_hash:
				card_hashes[parsed_id] = first_hash
		if not valid and status == "blocked":
			report.notes.append(f"blocked draft contains an invalid card: {parsed_id}")

	missing = [shot_id for shot_id in planned if shot_id not in seen]
	if missing:
		report.blockers.append(f"planned shots missing V2 cards: {', '.join(missing)}")
	if status == "ready":
		if handoff.get("blocking_findings") not in (None, []):
			report.errors.append("ready handoff cannot retain blocking_findings")
		_archive_claim_check(handoff, report)
		if missing:
			report.errors.append(f"generation-ready claim leaves planned shots uncovered: {', '.join(missing)}")
		if report.blockers:
			report.errors.extend(f"generation-ready claim is contradicted: {blocker}" for blocker in report.blockers)
	if require_ready:
		if status != "ready":
			report.errors.append(f"GENERATION_READY is required but status is {status!r}")
		_archive_claim_check(handoff, report)
		if report.blockers:
			report.errors.extend(f"--require-ready blocker: {blocker}" for blocker in report.blockers)
	return report


def audit_handoff(packet: Path, require_ready: bool = False, require_footage_analysis: bool = False) -> list[str]:
	"""Compatibility helper returning only fatal errors."""
	return audit_packet(packet, require_ready, require_footage_analysis).errors


def _discover_packets() -> list[Path]:
	packets: set[Path] = set()
	for path in (ROOT / "assets_src" / "cinematics").rglob(HANDOFF_NAME):
		try:
			value = json.loads(path.read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError):
			# Malformed V2 candidates must still reach the normal audit path.
			packets.add(path.parent.resolve())
			continue
		if isinstance(value, dict) and value.get("schema") == HANDOFF_SCHEMA_V2:
			packets.add(path.parent.resolve())
	return sorted(packets)


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("packet", nargs="*", type=Path, help="packet directories")
	parser.add_argument("--all", action="store_true", help="audit all imagine-handoff-v2 packets under assets_src/cinematics")
	parser.add_argument("--require-ready", action="store_true", help="fail unless every packet truthfully claims readiness")
	parser.add_argument("--require-footage-analysis", action="store_true", help="make footage analysis mandatory")
	return parser.parse_args()


def main() -> int:
	args = _parse_args()
	packets = [path.resolve() for path in args.packet]
	if args.all:
		packets.extend(_discover_packets())
	packets = list(dict.fromkeys(packets))
	if not packets:
		print("CONTINUITY|RESULT|FAIL|no handoff packets selected")
		return 1
	fatal = False
	for packet in packets:
		report = audit_packet(packet, args.require_ready, args.require_footage_analysis)
		if report.errors:
			state = "FAIL"
			fatal = True
		elif report.blockers:
			state = "BLOCKED"
		else:
			state = "PASS"
		print(f"CONTINUITY|PACKET|{packet}|{state}")
		for blocker in report.blockers:
			print(f"CONTINUITY|BLOCKER|{packet}|{blocker}")
		for note in report.notes:
			print(f"CONTINUITY|NOTE|{packet}|{note}")
		for error in report.errors:
			print(f"CONTINUITY|ERROR|{error}")
	print(f"CONTINUITY|RESULT|{'FAIL' if fatal else 'ALL OK'}")
	return 1 if fatal else 0


if __name__ == "__main__":
	sys.exit(main())
