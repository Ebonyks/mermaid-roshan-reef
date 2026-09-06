#!/usr/bin/env python3
"""Fail-closed validator for the declared minigame art-review ledger.

The ledger records human/AI judgments and their evidence. This tool verifies
file hashes and internal declarations; it deliberately does not infer scores
from pixels. A matching ``candidate_revision`` is declarative: this tool does
not prove that the revision exists, that a source file had its recorded bytes
at that revision, or that a screenshot came from that build. Canonical
same-process runtime capture remains responsible for those provenance links.
Source records for UTF-8 ``.gd``/``.py`` files may opt into the ``utf8_lf``
canonical text hash to survive CRLF/LF checkout conversion; screenshots,
images, and every other evidence record always use exact bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import tempfile
import zlib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "audit/minigame_art_quality_2026-09-05/registry.json"
SCHEMA = "minigame-art-quality-v1"
DIMENSIONS = (
	"identity", "finish", "edges", "readability", "animation",
	"ownership", "consistency", "technical",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
REV_RE = re.compile(r"^[0-9a-f]{40}$")
RULE_RE = re.compile(r"^DL-[A-Z]+-[0-9]{2}$")


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_utf8_lf(path: Path) -> str:
	"""Hash strict UTF-8 source after canonicalizing only CRLF line endings."""
	text = path.read_bytes().decode("utf-8", errors="strict")
	return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def _png_info(path: Path) -> tuple[int, int] | None:
	"""Validate a small/ordinary 8-bit PNG and return its dimensions.

	This is deliberately a structural decode gate, not a visual/art-quality
	judgment.  It checks the signature, chunk CRCs, IHDR, and that IDAT zlib
	data contains the expected scanline bytes for a supported screenshot PNG.
	"""
	data = path.read_bytes()
	if not data.startswith(b"\x89PNG\r\n\x1a\n"):
		return None
	offset = 8
	width = height = None
	bit_depth = color_type = None
	idat = bytearray()
	seen_iend = False
	while offset + 12 <= len(data):
		length = struct.unpack(">I", data[offset:offset + 4])[0]
		end = offset + 12 + length
		if end > len(data):
			return None
		kind = data[offset + 4:offset + 8]
		payload = data[offset + 8:offset + 8 + length]
		crc_expected = struct.unpack(">I", data[offset + 8 + length:end])[0]
		if (zlib.crc32(kind + payload) & 0xffffffff) != crc_expected:
			return None
		if kind == b"IHDR":
			if length != 13 or width is not None:
				return None
			width, height, bit_depth, color_type, compression, filt, interlace = struct.unpack(
				">IIBBBBB", payload)
			if not width or not height or bit_depth != 8 or compression != 0 \
					or filt != 0 or interlace != 0 or color_type not in (2, 6):
				return None
		elif kind == b"IDAT":
			idat.extend(payload)
		elif kind == b"IEND":
			seen_iend = True
			break
		offset = end
	if width is None or height is None or not idat or not seen_iend:
		return None
	try:
		decoded = zlib.decompress(bytes(idat))
	except zlib.error:
		return None
	channels = 4 if color_type == 6 else 3
	row_bytes = width * channels
	if len(decoded) != height * (row_bytes + 1):
		return None
	for row in range(height):
		if decoded[row * (row_bytes + 1)] not in (0, 1, 2, 3, 4):
			return None
	return width, height


def _inside(root: Path, value: Any, label: str, errors: list[str]) -> Path | None:
	if not isinstance(value, str) or not value or Path(value).is_absolute():
		errors.append(f"{label}: path must be a non-empty repository-relative path")
		return None
	path = (root / value).resolve()
	try:
		path.relative_to(root.resolve())
	except ValueError:
		errors.append(f"{label}: path escapes repository: {value!r}")
		return None
	return path


def _file(
	root: Path, record: Any, label: str, errors: list[str],
	*, allow_source_normalization: bool = False,
) -> Path | None:
	if not isinstance(record, dict):
		errors.append(f"{label}: expected path/sha256 object")
		return None
	path = _inside(root, record.get("path"), label, errors)
	digest = record.get("sha256")
	if not isinstance(digest, str) or not SHA_RE.fullmatch(digest):
		errors.append(f"{label}: sha256 must be 64 lowercase hex characters")
		return path
	normalization = record.get("hash_normalization")
	if normalization is not None:
		if not allow_source_normalization:
			errors.append(f"{label}: hash_normalization is allowed only on asset source records")
			return path
		if normalization != "utf8_lf":
			errors.append(f"{label}: unknown hash_normalization {normalization!r}")
			return path
		if path is not None and path.suffix.lower() not in {".gd", ".py"}:
			errors.append(f"{label}: utf8_lf normalization is allowed only for .gd/.py source files")
			return path
	if path is None:
		return None
	if not path.is_file():
		errors.append(f"{label}: file does not exist: {record.get('path')}")
	else:
		try:
			actual = _sha256_utf8_lf(path) if normalization == "utf8_lf" else _sha256(path)
		except UnicodeDecodeError:
			errors.append(f"{label}: utf8_lf source must be valid UTF-8")
		else:
			if actual != digest:
				errors.append(f"{label}: file hash mismatch: {record.get('path')}")
	return path


def _review(
	root: Path, review: Any, label: str, revision: str, asset_states: set[str],
	errors: list[str], blockers: list[str], required: bool, role: str,
) -> None:
	if review is None:
		if required:
			blockers.append(f"{label}: candidate review missing")
		return
	if not isinstance(review, dict):
		errors.append(f"{label}: review must be an object or null")
		return
	dimensions = review.get("dimensions")
	na_reasons = review.get("na_reasons", {})
	if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
		errors.append(f"{label}: dimensions must contain exactly {', '.join(DIMENSIONS)}")
		return
	if not isinstance(na_reasons, dict):
		errors.append(f"{label}: na_reasons must be an object")
		na_reasons = {}
	values: list[float] = []
	static_object = review.get("object_classification") == "static_object"
	for name in DIMENSIONS:
		value = dimensions[name]
		if value is None:
			if not isinstance(na_reasons.get(name), str) or not na_reasons[name].strip():
				errors.append(f"{label}: null {name} requires a non-empty NA reason")
			elif required and (name != "animation" or not static_object \
					or role.lower() in {"actor", "action-required"}):
				blockers.append(f"{label}: candidate NA is allowed only for animation on an explicit static_object")
			continue
		if isinstance(value, bool) or not isinstance(value, (int, float)) \
				or not 1.0 <= float(value) <= 5.0:
			errors.append(f"{label}: {name} must be 1..5 or null")
		else:
			values.append(float(value))
	reviewer = review.get("reviewer")
	if not isinstance(reviewer, dict) or reviewer.get("kind") not in {"ai", "owner", "human"} \
			or not isinstance(reviewer.get("id"), str) or not reviewer.get("id", "").strip():
		errors.append(f"{label}: reviewer requires kind ai/owner/human and non-empty id")
	evidence = review.get("evidence")
	if not isinstance(evidence, list) or not evidence:
		errors.append(f"{label}: review requires at least one evidence item")
		evidence = []
	current_runtime_states: set[str] = set()
	current_state_hashes: dict[str, str] = {}
	for index, item in enumerate(evidence):
		evidence_label = f"{label}.evidence[{index}]"
		evidence_path = _file(root, item, evidence_label, errors)
		context = item.get("context") if isinstance(item, dict) else None
		if not isinstance(context, dict):
			errors.append(f"{evidence_label}: context object missing")
			continue
		state = context.get("state")
		current_context = context.get("runtime") is True and context.get("candidate_revision") == revision \
				and context.get("renderer") == "mobile" \
				and context.get("viewport") == [1280, 720] \
				and context.get("hud") is True and context.get("diagnostic") is not True
		if current_context and isinstance(state, str):
			if evidence_path is None:
				continue
			info = _png_info(evidence_path)
			if info != tuple(context["viewport"]):
				errors.append(f"{evidence_label}: current evidence must be a valid 8-bit PNG matching context.viewport")
				continue
			digest = _sha256(evidence_path)
			previous_state = current_state_hashes.get(digest)
			if previous_state is not None and previous_state != state:
				blockers.append(f"{evidence_label}: identical current PNG bytes cannot be relabeled for states {previous_state!r} and {state!r}")
				continue
			current_state_hashes[digest] = state
			current_runtime_states.add(state)
	if required and values and min(values) >= 4.5:
		missing_states = asset_states - current_runtime_states
		if missing_states:
			blockers.append(
				f"{label}: >=4.5 requires current candidate runtime Mobile/HUD "
				f"evidence for states {sorted(missing_states)}")
	if required and (not values or min(values) < 4.5):
		blockers.append(f"{label}: one or more applicable dimensions are below 4.5")
	declared = review.get("score")
	if values:
		mean = round(sum(values) / len(values), 2)
		if isinstance(declared, bool) or not isinstance(declared, (int, float)) \
				or abs(float(declared) - mean) > 0.005:
			errors.append(f"{label}: score must equal applicable-dimension mean {mean:.2f}")


def audit_data(data: Any, root: Path = ROOT) -> tuple[list[str], list[str]]:
	errors: list[str] = []
	blockers: list[str] = []
	if not isinstance(data, dict):
		return ["registry root must be an object"], []
	if data.get("schema") != SCHEMA:
		errors.append(f"schema must be {SCHEMA!r}")
	revision = data.get("candidate_revision")
	if not isinstance(revision, str) or not REV_RE.fullmatch(revision):
		errors.append("candidate_revision must be 40 lowercase hex characters")
		revision = ""
	scope = data.get("scope")
	if not isinstance(scope, dict):
		errors.append("scope must be an object")
		scope = {}
	games = scope.get("games")
	surfaces = scope.get("surfaces")
	if not isinstance(games, list) or not games or any(not isinstance(x, str) or not x for x in games):
		errors.append("scope.games must be a non-empty string list")
		games = []
	if not isinstance(surfaces, list) or not surfaces:
		errors.append("scope.surfaces must be a non-empty list")
		surfaces = []
	if scope.get("coverage_complete") is not True:
		blockers.append("scope.coverage_complete is not true")

	assets = data.get("assets")
	if not isinstance(assets, list) or not assets:
		errors.append("assets must be a non-empty list")
		assets = []
	asset_ids: list[str] = []
	for index, asset in enumerate(assets):
		label = f"assets[{index}]"
		if not isinstance(asset, dict):
			errors.append(f"{label}: expected object")
			continue
		asset_id = asset.get("id")
		if not isinstance(asset_id, str) or not asset_id:
			errors.append(f"{label}: id must be non-empty")
		else:
			asset_ids.append(asset_id)
		game = asset.get("game")
		if game not in games:
			errors.append(f"{label}: game is absent from scope.games")
		if not isinstance(asset.get("surface"), str) or not asset.get("surface"):
			errors.append(f"{label}: surface must be non-empty")
		if not isinstance(asset.get("role"), str) or not asset.get("role"):
			errors.append(f"{label}: role must be non-empty")
		states = asset.get("states")
		if not isinstance(states, list) or not states or any(not isinstance(x, str) or not x for x in states):
			errors.append(f"{label}: states must be a non-empty string list")
			state_set: set[str] = set()
		else:
			state_set = set(states)
		_file(root, asset.get("source"), f"{label}.source", errors,
			allow_source_normalization=True)
		reviews = asset.get("reviews")
		if not isinstance(reviews, dict):
			errors.append(f"{label}: reviews must be an object")
			reviews = {}
		_review(root, reviews.get("prior"), f"{label}.reviews.prior", revision,
			state_set, errors, blockers, False, str(asset.get("role", "")))
		_review(root, reviews.get("candidate"), f"{label}.reviews.candidate", revision,
			state_set, errors, blockers, True, str(asset.get("role", "")))
		defects = asset.get("defects")
		if not isinstance(defects, list):
			errors.append(f"{label}: defects must be a list")
			defects = []
		for defect_index, defect in enumerate(defects):
			prefix = f"{label}.defects[{defect_index}]"
			if not isinstance(defect, dict) or not RULE_RE.fullmatch(str(defect.get("rule_id", ""))):
				errors.append(f"{prefix}: valid DL-* rule_id required")
				continue
			if not isinstance(defect.get("blocking"), bool) or not isinstance(defect.get("resolved"), bool):
				errors.append(f"{prefix}: blocking and resolved must be booleans")
			elif defect["blocking"] and not defect["resolved"]:
				blockers.append(f"{prefix}: unresolved blocking defect")
		history = asset.get("replacement_history")
		if not isinstance(history, list):
			errors.append(f"{label}: replacement_history must be a list")
		else:
			for history_index, record in enumerate(history):
				prefix = f"{label}.replacement_history[{history_index}]"
				if not isinstance(record, dict) or not isinstance(record.get("method"), str) \
						or not record.get("method"):
					errors.append(f"{prefix}: method required")
					continue
				hashes = record.get("source_hashes")
				if not isinstance(hashes, list) or any(not isinstance(x, str) or not SHA_RE.fullmatch(x) for x in hashes):
					errors.append(f"{prefix}: source_hashes must be lowercase SHA-256 list")
				if not SHA_RE.fullmatch(str(record.get("output_sha256", ""))):
					errors.append(f"{prefix}: output_sha256 required")

	if len(asset_ids) != len(set(asset_ids)):
		errors.append("asset ids must be unique")
	declared_live: list[str] = []
	seen_surfaces: set[tuple[str, str]] = set()
	for index, surface in enumerate(surfaces):
		label = f"scope.surfaces[{index}]"
		if not isinstance(surface, dict):
			errors.append(f"{label}: expected object")
			continue
		key = (str(surface.get("game", "")), str(surface.get("id", "")))
		if not all(key) or key[0] not in games or key in seen_surfaces:
			errors.append(f"{label}: unique in-scope game/id required")
		seen_surfaces.add(key)
		live = surface.get("live_asset_ids")
		if not isinstance(live, list) or not live:
			errors.append(f"{label}: live_asset_ids must be non-empty")
		else:
			declared_live.extend(str(x) for x in live)
	if set(declared_live) != set(asset_ids) or len(declared_live) != len(set(declared_live)):
		errors.append("scope live_asset_ids must cover every asset exactly once")
	for asset in assets:
		if isinstance(asset, dict) and (asset.get("game"), asset.get("surface")) not in seen_surfaces:
			errors.append(f"asset {asset.get('id')!r} has no matching scope surface")

	approvals = data.get("approvals", {})
	if not isinstance(approvals, dict):
		errors.append("approvals must be an object")
	else:
		for kind in ("owner", "device", "child"):
			claim = approvals.get(kind, {"approved": False})
			if not isinstance(claim, dict) or not isinstance(claim.get("approved"), bool):
				errors.append(f"approvals.{kind}.approved must be boolean")
				continue
			if claim["approved"]:
				_file(root, claim.get("evidence"), f"approvals.{kind}.evidence", errors)
		if not errors:
			approval_set = all(approvals.get(kind, {}).get("approved") is True
				for kind in ("owner", "device", "child"))
			for asset in assets:
				review = asset.get("reviews", {}).get("candidate") if isinstance(asset, dict) else None
				if isinstance(review, dict) and review.get("score") == 5 and not approval_set:
					blockers.append(f"asset {asset.get('id')!r}: score 5 requires owner/device/child evidence")
	return errors, blockers


def audit_registry(path: Path, root: Path = ROOT) -> tuple[list[str], list[str]]:
	try:
		data = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		return [f"cannot read registry: {exc}"], []
	return audit_data(data, root)


def _stress() -> int:
	with tempfile.TemporaryDirectory() as temp:
		root = Path(temp)
		asset = root / "asset.png"
		evidence = root / "capture.png"
		asset.write_bytes(b"asset")
		width, height = 1280, 720
		ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
		idat = zlib.compress((b"\x00" + b"\x14\x28\x50" * width) * height)
		def chunk(kind: bytes, payload: bytes) -> bytes:
			return struct.pack(">I", len(payload)) + kind + payload \
				+ struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
		evidence.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) \
			+ chunk(b"IDAT", idat) + chunk(b"IEND", b""))
		digest = lambda path: _sha256(path)
		base = {
			"schema": SCHEMA, "candidate_revision": "a" * 40,
			"scope": {"games": ["g"], "coverage_complete": True,
				"surfaces": [{"game": "g", "id": "s", "live_asset_ids": ["a"]}]},
			"assets": [{"id": "a", "game": "g", "surface": "s", "role": "actor",
				"states": ["idle"], "source": {"path": "asset.png", "sha256": digest(asset)},
				"reviews": {"prior": None, "candidate": {"dimensions": dict.fromkeys(DIMENSIONS, 4.5),
					"na_reasons": {}, "score": 4.5, "reviewer": {"kind": "ai", "id": "stress"},
					"evidence": [{"path": "capture.png", "sha256": digest(evidence), "context": {
						"runtime": True, "candidate_revision": "a" * 40, "renderer": "mobile",
						"viewport": [1280, 720], "hud": True, "state": "idle"}}]}},
				"defects": [], "replacement_history": []}],
			"approvals": {"owner": {"approved": False}, "device": {"approved": False},
				"child": {"approved": False}},
		}
		if any(audit_data(base, root)):
			print("MINIGAME_ART|STRESS|FAIL|valid fixture rejected")
			return 1
		mutants = []
		for mutate in ("low", "blocker", "stale", "hash", "coverage", "owner"):
			copy = json.loads(json.dumps(base))
			if mutate == "low": copy["assets"][0]["reviews"]["candidate"]["dimensions"]["edges"] = 4
			if mutate == "blocker": copy["assets"][0]["defects"] = [{"rule_id": "DL-VIS-02", "blocking": True, "resolved": False}]
			if mutate == "stale": copy["assets"][0]["reviews"]["candidate"]["evidence"][0]["context"]["candidate_revision"] = "b" * 40
			if mutate == "hash": copy["assets"][0]["source"]["sha256"] = "0" * 64
			if mutate == "coverage": copy["scope"]["coverage_complete"] = False
			if mutate == "owner": copy["approvals"]["owner"] = {"approved": True}
			mutants.append((mutate, copy))
		for name, mutant in mutants:
			if not any(audit_data(mutant, root)):
				print(f"MINIGAME_ART|STRESS|FAIL|{name} mutant passed")
				return 1
	print(f"MINIGAME_ART|STRESS|PASS|{len(mutants)} mutants rejected")
	return 0


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT_REGISTRY)
	parser.add_argument("--check", action="store_true",
		help="fail unless every declared live asset reaches the 4.5 threshold")
	parser.add_argument("--validate-only", action="store_true",
		help="validate schema/evidence integrity; unresolved quality remains reported")
	parser.add_argument("--stress", action="store_true")
	args = parser.parse_args(argv)
	if args.stress:
		return _stress()
	errors, blockers = audit_registry(args.registry.resolve(), ROOT)
	for error in errors:
		print(f"MINIGAME_ART|INVALID|{error}")
	for blocker in blockers:
		print(f"MINIGAME_ART|BLOCKED|{blocker}")
	if errors:
		print("MINIGAME_ART|RESULT|INVALID")
		return 1
	status = "SATISFIED" if not blockers else "UNSATISFIED"
	print(f"MINIGAME_ART|RESULT|{status}")
	print("MINIGAME_ART|LIMIT|declared-registry consistency only; "
		"this is not master/game-wide provenance proof; use the canonical "
		"same-process capture gate")
	if args.validate_only:
		return 0
	return 0 if status == "SATISFIED" else 1


if __name__ == "__main__":
	sys.exit(main())
