#!/usr/bin/env python3
"""Fail closed on first-frame location topology records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
	try:
		value = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		errors.append(f"cannot read {path}: {exc}")
		return {}
	if not isinstance(value, dict):
		errors.append(f"JSON root must be an object: {path}")
		return {}
	return value


def checked_file(packet: Path, relative: Any, declared: Any, label: str, errors: list[str]) -> Path | None:
	if not isinstance(relative, str) or not relative:
		errors.append(f"{label}: path missing")
		return None
	path = (packet / relative).resolve()
	try:
		path.relative_to(packet.resolve())
	except ValueError:
		errors.append(f"{label}: path escapes packet: {relative}")
		return None
	if not path.is_file():
		errors.append(f"{label}: file missing: {relative}")
		return None
	if not isinstance(declared, str) or not SHA256_RE.fullmatch(declared):
		errors.append(f"{label}: invalid SHA-256")
	elif sha256(path) != declared:
		errors.append(f"{label}: SHA-256 mismatch: {relative}")
	return path


def nonempty_strings(value: Any, minimum: int = 1) -> bool:
	return isinstance(value, list) and len(value) >= minimum and all(isinstance(item, str) and item.strip() for item in value)


def audit_packet(packet: Path) -> tuple[list[str], list[str]]:
	errors: list[str] = []
	blockers: list[str] = []
	frames = sorted((packet / "first_frames").glob("S*_FIRST_FRAME.png"))
	lock_path = packet / "LOCATION_GEOMETRY_LOCK.json"
	if not frames and not lock_path.is_file():
		return errors, blockers
	if frames and not lock_path.is_file():
		errors.append("first-frame candidates exist without LOCATION_GEOMETRY_LOCK.json")
		return errors, blockers
	lock = load_json(lock_path, errors)
	if lock.get("schema") != "location-geometry-lock-v1":
		errors.append("geometry lock schema must be location-geometry-lock-v1")
	sources = lock.get("source_authorities")
	if not isinstance(sources, list) or not sources:
		errors.append("source_authorities must be non-empty")
		sources = []
	source_ids: set[str] = set()
	for index, source in enumerate(sources):
		if not isinstance(source, dict):
			errors.append(f"source_authorities[{index}] must be an object")
			continue
		source_id = source.get("source_id")
		if not isinstance(source_id, str) or not source_id:
			errors.append(f"source_authorities[{index}] source_id missing")
		else:
			source_ids.add(source_id)
		checked_file(packet, source.get("path"), source.get("sha256"), f"source {source_id}", errors)
		if not nonempty_strings(source.get("ordered_landmarks_left_to_right"), 2):
			errors.append(f"source {source_id}: ordered landmarks missing")
		counts = source.get("counts")
		if not isinstance(counts, dict) or not counts:
			errors.append(f"source {source_id}: fixture counts missing")
	if not nonempty_strings(lock.get("global_invariants"), 3):
		errors.append("at least three global topology invariants are required")
	reviews = lock.get("candidate_reviews")
	if not isinstance(reviews, list):
		errors.append("candidate_reviews must be a list")
		reviews = []
	reviewed_paths: set[Path] = set()
	for index, review in enumerate(reviews):
		if not isinstance(review, dict):
			errors.append(f"candidate_reviews[{index}] must be an object")
			continue
		path = checked_file(packet, review.get("path"), review.get("sha256"), f"candidate {index}", errors)
		if path is not None:
			reviewed_paths.add(path)
		for source_id in review.get("authority_source_ids", []):
			if source_id not in source_ids and not str(source_id).startswith(("pearl_castle_", "sky_lagoon_")):
				errors.append(f"candidate {index}: unknown authority source {source_id}")
		human = review.get("human_decision")
		if human not in {"pending", "accepted", "rejected"}:
			errors.append(f"candidate {index}: invalid human_decision")
		eligible = review.get("eligible_as_image_1")
		if eligible is True and (human != "accepted" or review.get("sol_topology_decision") != "pass"):
			errors.append(f"candidate {index}: IMAGE_1 eligibility claimed without Sol and human acceptance")
		if human != "accepted":
			blockers.append(f"{review.get('shot_id', index)} human geometry decision is {human}")
	for frame in frames:
		if frame.resolve() not in reviewed_paths:
			errors.append(f"unreviewed first-frame candidate: {frame.relative_to(packet)}")
	return errors, blockers


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("packet", nargs="*", type=Path)
	parser.add_argument("--all", action="store_true", dest="audit_all")
	parser.add_argument("--require-approved", action="store_true")
	args = parser.parse_args()
	packets = [path.resolve() for path in args.packet]
	if args.audit_all:
		packets.extend(path.parent for path in sorted((ROOT / "assets_src" / "cinematics").glob("**/IMAGINE_HANDOFF.json")))
	packets = list(dict.fromkeys(packets))
	if not packets:
		print("GEOMETRY|RESULT|FAIL|no packets selected")
		return 1
	failed = False
	for packet in packets:
		errors, blockers = audit_packet(packet)
		if args.require_approved and blockers:
			errors.extend(blockers)
		status = "FAIL" if errors else ("BLOCKED" if blockers else "PASS")
		print(f"GEOMETRY|PACKET|{packet}|{status}")
		for error in errors:
			print(f"GEOMETRY|ERROR|{packet}|{error}")
		for blocker in blockers:
			print(f"GEOMETRY|BLOCKER|{packet}|{blocker}")
		failed = failed or bool(errors)
	print(f"GEOMETRY|RESULT|{'FAIL' if failed else 'ALL OK'}")
	return 1 if failed else 0


if __name__ == "__main__":
	sys.exit(main())

