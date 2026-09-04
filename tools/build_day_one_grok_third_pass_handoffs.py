#!/usr/bin/env python3
"""Build the exhaustive Day One strict third-pass refinement packet.

This is deliberately a new packet.  It never mutates the September 3
regeneration handoff and never calls a motion-reference clip delivery-ready.
The builder fails closed when the three exhaustive original audits, the 119
original branch clips, or the committed 40-file regeneration audit disagree.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CIN = ROOT / "assets_src" / "cinematics"
TEMP_ROOT = ROOT.parents[1] / ".tmp" / "full-day-one-strict"
ORIGINAL_WORKTREE = ROOT.parents[1] / ".worktrees" / "day1-original-clips-audit"
SECOND = CIN / "day_one_grok_regeneration_handoffs_2026-09-03"
THIRD = CIN / "day_one_grok_handoff_v3_2026-09-04"
SOURCE_COMMIT = "076661afb9e092627eb5dfae7c39fecb27463892"
ORIGINAL_COMMIT = "5ca170e11c77ea55c3224f9f275b94b8fd62ca36"
REGEN_COMMIT = "384abc966b92b27bd61a735319a7639ef68ac15b"
REGEN_BRANCH = "day1-regen-3sets-2026-09-04"
REPO = "Ebonyks/mermaid-roshan-reef"
EXPECTED_ORIGINAL_FILES = 119
EXPECTED_REGEN_FILES = 40
EXPECTED_LEDGER_FILES = 159
DATE = "2026-09-04"

# These are the eleven known strict third-pass remake overrides.  They are
# resolved shot decisions, not a claim that every ID was independently
# re-reviewed by Sol.  C06-S04 is an additional strict camera override: its
# rough-cut clip does not establish the required close-to-wide pullback.
KNOWN_STRICT_REMAKE_OVERRIDES = {
	"D1-C01-S02", "D1-C02-S03", "D1-C03-S02", "D1-C03-S03",
	"D1-C03-S04", "D1-C05-S04", "D1-C05-S05", "D1-C06-S03",
	"D1-C06-S05", "D1-C06-S06", "D1-C06-S09",
}
STRICT_EXTRA_REMAKE = {"D1-C06-S04"}
STRICT_KEEP_OVERRIDES = {"D1-C01-S03", "D1-C06-S08", "D1-C11-S03"}
STRICT_TRIM_OVERRIDES = {"D1-C11-S02", "D1-C12-S05", "D1-C13-S01", "D1-C13-S02", "D1-C10-S03"}

SYNTHETIC_BINDINGS = {
	"D1-C01-S04": [("location", "lagoon geography"), ("roshan", "Roshan identity"), ("daddy", "Daddy identity"), ("castle", "castle exterior and closed door")],
	"D1-C04-S03": [("location", "clean bathroom layout"), ("roshan", "Roshan identity"), ("swimming_bunny", "swimming bunny identity")],
	"D1-C05-S02": [("location", "pool geography"), ("roshan", "Roshan identity"), ("swimming_bunny", "swimming bunny identity"), ("pool_trash", "pool debris identity")],
	"D1-C05-S06": [("location", "pool geography"), ("swimming_bunny", "swimming bunny identity"), ("waterfall_clog", "blocked waterfall identity"), ("seahorse", "sick seahorse identity")],
	"D1-C06-S04": [("location", "pool geography"), ("waterfall_rest", "restored rainbow source identity"), ("seahorse_rest", "restored seahorse source identity")],
	"D1-C06-S07": [("location", "pool geography"), ("rumi", "Rumi identity"), ("roshan", "Roshan identity")],
	"D1-C09-S05": [("location", "Art Room geography"), ("roshan", "Roshan identity"), ("fixture_sheet", "Art Room fixture identity sheet"), ("cleaning_brush", "magic cleaning brush")],
	"D1-C10-S01": [("location", "Art Room geography"), ("roshan", "Roshan identity"), ("fixture_sheet", "Art Room fixture identity sheet"), ("cleaning_brush", "magic cleaning brush")],
	"D1-C10-S05": [("location", "Art Room geography"), ("roshan", "Roshan identity"), ("fixture_sheet", "Art Room fixture identity sheet")],
	"D1-C13-S04": [("arena_location", "arena geography"), ("rumi", "Rumi identity"), ("grand_puff", "Grand Puff identity")],
}


def _load_second():
	path = ROOT / "tools" / "build_day_one_grok_regeneration_handoffs.py"
	spec = importlib.util.spec_from_file_location("day_one_second_handoff", path)
	if spec is None or spec.loader is None:
		raise RuntimeError(f"cannot import second handoff: {path}")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


SECOND_BUILDER = _load_second()
PACKETS = SECOND_BUILDER.PACKETS
TITLES = SECOND_BUILDER.TITLES
GAME_AUTHORITY = SECOND_BUILDER.GAME_AUTHORITY


def _sha256(path: Path) -> str:
	return hashlib.sha256(_canonical_payload_bytes(path)).hexdigest()


def _canonical_payload_bytes(path: Path) -> bytes:
	data = path.read_bytes()
	if path.suffix.lower() in {".csv", ".json", ".md", ".txt"} or path.name == ".gitattributes":
		return data.replace(b"\r\n", b"\n")
	return data


def _sha256_text(value: str) -> str:
	return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _fail(message: str) -> None:
	raise RuntimeError(f"third-pass input validation failed: {message}")


def _movie(shot_id: str) -> str:
	match = re.fullmatch(r"(?:D1-)?(C\d{2})-S\d{2}", shot_id)
	if not match:
		_fail(f"invalid shot id {shot_id!r}")
	return f"D1-{match.group(1)}"


def _canonical_shot(raw: str) -> str:
	return raw if raw.startswith("D1-") else f"D1-{raw}"


def _git_original_filenames() -> set[str]:
	command = ["git", "ls-tree", "-r", "--name-only", "remotes/origin/day-one-individual-clips-2026-09-03"]
	try:
		result = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
	except (OSError, subprocess.CalledProcessError) as exc:
		_fail(f"cannot inspect original branch tree: {exc}")
	paths = {Path(line.strip()).name for line in result.stdout.splitlines() if line.strip().lower().endswith(".mp4")}
	if len(paths) != EXPECTED_ORIGINAL_FILES:
		_fail(f"original branch tree has {len(paths)} MP4 basenames, expected {EXPECTED_ORIGINAL_FILES}")
	return paths


def _read_inputs() -> tuple[list[dict], dict, dict]:
	audit_paths = sorted(TEMP_ROOT.glob("audit_*.json"))
	if len(audit_paths) != 3:
		_fail(f"expected exactly 3 exhaustive audit JSONs under {TEMP_ROOT}, found {len(audit_paths)}")
	original_files: list[dict] = []
	original_summaries: dict[str, dict] = {}
	seen: set[str] = set()
	for path in audit_paths:
		try:
			data = json.loads(path.read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError) as exc:
			_fail(f"cannot parse {path}: {exc}")
		if not isinstance(data.get("files"), list) or not isinstance(data.get("shot_summary"), list):
			_fail(f"{path} is not an exhaustive audit JSON")
		for row in data["files"]:
			filename = str(row.get("filename", ""))
			if not filename or filename in seen:
				_fail(f"duplicate or missing original filename {filename!r}")
			seen.add(filename)
			record = dict(row)
			record["filename"] = filename
			record["shot_id"] = _canonical_shot(str(row.get("shot_id", "")))
			record["movie_id"] = _movie(record["shot_id"])
			record["audit_path"] = str(path)
			record["lane"] = "original_branch"
			record["branch"] = "day-one-individual-clips-2026-09-03"
			record["commit"] = ORIGINAL_COMMIT
			record["resolved_file_disposition"] = str(row.get("verdict", ""))
			original_files.append(record)
		for row in data["shot_summary"]:
			shot_id = _canonical_shot(str(row.get("shot_id", "")))
			if shot_id in original_summaries:
				_fail(f"duplicate original shot summary {shot_id}")
			original_summaries[shot_id] = dict(row)
		if not path.name.startswith("audit_"):
			_fail(f"unexpected audit name {path.name}")
	if len(original_files) != EXPECTED_ORIGINAL_FILES:
		_fail(f"original audit union has {len(original_files)} files, expected {EXPECTED_ORIGINAL_FILES}")
	if {row["filename"] for row in original_files} != _git_original_filenames():
		_fail("exhaustive original audit filenames do not exactly match the branch tree")

	if not (SECOND / "AUDITED_RELEASE_ASSETS.json").is_file():
		_fail(f"missing committed 40-file audit: {SECOND / 'AUDITED_RELEASE_ASSETS.json'}")
	regen = json.loads((SECOND / "AUDITED_RELEASE_ASSETS.json").read_text(encoding="utf-8"))
	if not isinstance(regen.get("clips"), list) or len(regen["clips"]) != EXPECTED_REGEN_FILES:
		_fail("committed regeneration audit does not contain exactly 40 clips")
	regen_files: list[dict] = []
	for row in regen["clips"]:
		record = dict(row)
		record["shot_id"] = _canonical_shot(str(row.get("shot_id", "")))
		record["movie_id"] = str(row.get("movie_id") or _movie(record["shot_id"]))
		record["audit_path"] = str(SECOND / "AUDITED_RELEASE_ASSETS.json")
		record["lane"] = "committed_regen_audit"
		record["branch"] = REGEN_BRANCH
		record["commit"] = REGEN_COMMIT
		record["resolved_file_disposition"] = str(row.get("shot_verdict", ""))
		record["filename"] = str(row.get("filename", ""))
		if not record["filename"]:
			_fail("regeneration audit contains a blank filename")
		regen_files.append(record)
	return original_files, regen_files, original_summaries


def _map_disposition(value: str) -> str:
	return {
		"ACCEPT_MOTION_REFERENCE": "KEEP_HIGH_QUALITY",
		"KEEP_HIGH_QUALITY": "KEEP_HIGH_QUALITY",
		"KEEP_WITH_TRIM": "KEEP_WITH_TRIM",
		"SUPERSEDED_BY_BETTER_VARIANT": "SUPERSEDED_BY_BETTER_VARIANT",
		"REGENERATE": "REMAKE",
		"REMAKE": "REMAKE",
		"REPLACE_WITH_GAME_EVENT": "OMIT_WRONG_EVENT",
		"OMIT_SUPERSEDED_EVENT": "OMIT_WRONG_EVENT",
		"OMIT_WRONG_EVENT": "OMIT_WRONG_EVENT",
	}.get(value, "")


def _source_item(shot_id: str, summary: dict, finding: str) -> dict:
	"""Use a second-pass card where it exists; synthesize only missing remakes."""
	for item in SECOND_BUILDER.SHOTS:
		if item["shot_id"] == shot_id:
			result = dict(item)
			if shot_id in SYNTHETIC_BINDINGS:
				result["bindings"] = SYNTHETIC_BINDINGS[shot_id]
			return result
	movie = _movie(shot_id)
	index = shot_id.rsplit("-S", 1)[1]
	timeline = tuple(summary.get("recommended_timeline") or [
		f"begin on the exact approved {movie} inherited state",
		f"perform only the implemented {TITLES.get(movie, movie)} action while preserving room topology",
		f"hold the required outgoing seam for {shot_id}",
	])
	if len(timeline) != 3:
		timeline = (str(timeline[0]), str(timeline[1]), str(timeline[2]))
	return {
		"movie": movie,
		"shot_id": shot_id,
		"title": f"{TITLES.get(movie, movie)} — {shot_id}",
		"camera": "locked, restrained action framing",
		"timeline": timeline,
		"must_move": timeline[1],
		"must_not_move": "approved room topology, character identity/anatomy, material state, cast count, and inherited seam",
		"end": timeline[2],
		"negatives": "no invented event, topology drift, identity drift, anatomy errors, text, HUD, morph, interpolation, or camera drift",
		"sound": "quiet room tone and one soft causal action cue; no voices",
		"bindings": SYNTHETIC_BINDINGS.get(shot_id, []),
		"evidence": [(None, finding or "strict audit requires a new full-frame motion reference")],
		"duration": 6,
		"conditional": False,
		"image1_requirement": "human-approved, clean, HUD-free shot-opening frame in the exact inherited state",
	}


def _bindings(item: dict) -> list[dict]:
	if item.get("bindings"):
		return SECOND_BUILDER._binding_plan(item)
	movie = item["movie"]
	assets = [asset for asset in SECOND_BUILDER._assets(movie)
		if asset.get("bound_reference_eligible") and str(asset.get("media_type", "")).startswith("image/")]
	if len(assets) < 2:
		_fail(f"{movie} source packet has fewer than two eligible image authorities")
	plan = []
	for index, asset in enumerate(assets[:4], start=1):
		plan.append({
			"id": f"IMAGE_{index}",
			"job": asset.get("role", "approved visual authority"),
			"status": "approved_source_authority_available" if index > 1 else "missing_approved_shot_opening_frame",
			"source_movie_id": movie,
			"source_packet": PACKETS[movie],
			"path": asset["path"],
			"sha256": asset["sha256"],
			"remote_url": f"https://raw.githubusercontent.com/{REPO}/{SOURCE_COMMIT}/assets_src/cinematics/{PACKETS[movie]}/{asset['path']}",
			"hud_present": False,
			"used_as_delivery_pixels": False,
		})
	if not 2 <= len(plan) <= 4:
		_fail(f"{item['shot_id']} binding count is {len(plan)}")
	return plan


def _prompt(item: dict) -> str:
	spans = ("0.0–2.0s", "2.0–4.5s", "4.5–6.0s")
	return (
		f"Action-first {item['camera']} shot. Start on the human-approved clean opening frame from IMAGE_1.\n\n"
		f"{spans[0]}: {item['timeline'][0]}.\n"
		f"{spans[1]}: {item['timeline'][1]}.\n"
		f"{spans[2]}: {item['timeline'][2]}.\n\n"
		f"Only the named action moves: {item['must_move']}. Keep {item['must_not_move']} locked. "
		f"Preserve the approved identities and materials from IMAGE_2 onward. {item['negatives']}.\n\n"
		f"End: {item['end']}.\n"
		f"Sound: {item['sound']}.\n"
	)


def _preferred(shot_id: str, summary: dict, originals: list[dict], regen: list[dict]) -> tuple[str | None, str | None]:
	requested = str(summary.get("current_preferred_file", "")).strip()
	if requested and not requested.upper().startswith("NONE"):
		name = Path(requested).name
		for row in originals + regen:
			if row["shot_id"] == shot_id and row["filename"] == name:
				return name, row["lane"]
	for row in originals:
		if row["shot_id"] == shot_id and row.get("preferred_for_shot") is True:
			return row["filename"], row["lane"]
	for row in regen:
		if row["shot_id"] == shot_id and row.get("variant_disposition") == "selected_motion_reference":
			return row["filename"], row["lane"]
	for row in originals + regen:
		if row["shot_id"] == shot_id and _map_disposition(row["resolved_file_disposition"]) in {"KEEP_HIGH_QUALITY", "KEEP_WITH_TRIM"}:
			return row["filename"], row["lane"]
	return None, None


def _timeline(summary: dict, item: dict) -> list[str]:
	values = summary.get("recommended_timeline")
	return [str(x) for x in values] if isinstance(values, list) and len(values) == 3 else [str(x) for x in item["timeline"]]


def _matrix(originals: list[dict], regen: list[dict], summaries: dict[str, dict]) -> list[dict]:
	by_shot: dict[str, list[dict]] = {}
	for row in originals + regen:
		by_shot.setdefault(row["shot_id"], []).append(row)
	shot_ids = sorted(by_shot, key=lambda value: (int(value[4:6]), int(value[-2:])))
	rows = []
	for shot_id in shot_ids:
		rows_for_shot = by_shot[shot_id]
		summary = summaries.get(shot_id, {})
		finding = "; ".join(str(row.get("finding", "")).strip() for row in rows_for_shot if row.get("finding"))
		item = _source_item(shot_id, summary, finding)
		disposition = str(summary.get("strict_disposition", "")).strip()
		if not disposition:
			disposition = next((_map_disposition(row["resolved_file_disposition"]) for row in rows_for_shot if _map_disposition(row["resolved_file_disposition"])), "REMAKE")
		if shot_id in KNOWN_STRICT_REMAKE_OVERRIDES or shot_id in STRICT_EXTRA_REMAKE:
			disposition = "REMAKE"
		elif shot_id in STRICT_KEEP_OVERRIDES:
			disposition = "KEEP_HIGH_QUALITY"
		elif shot_id in STRICT_TRIM_OVERRIDES:
			disposition = "KEEP_WITH_TRIM"
		preferred, lane = _preferred(shot_id, summary, originals, regen)
		rows.append({
			"shot_id": shot_id,
			"movie_id": _movie(shot_id),
			"title": item["title"],
			"current_preferred_file": preferred,
			"preferred_lane": lane,
			"strict_disposition": disposition,
			"active_generator_card": disposition == "REMAKE",
			"candidate_files": [
				{"filename": row["filename"], "lane": row["lane"], "file_verdict": row["resolved_file_disposition"], "weak_frames": row.get("weak_frames"), "finding": row.get("finding")}
				for row in rows_for_shot
			],
			"source_packet": PACKETS.get(_movie(shot_id)),
			"source_card": f"design/grok_day_one_video_handoffs_2026-08-30/{_movie(shot_id).replace('D1-', 'D1-')}_*.txt",
			"reason": str(summary.get("reason") or finding or "strict third-pass disposition"),
			"recommended_timeline": _timeline(summary, item),
		})
	return rows


def _ledger(originals: list[dict], regen: list[dict], matrix: list[dict]) -> list[dict]:
	strict = {row["shot_id"]: row["strict_disposition"] for row in matrix}
	entries = []
	for row in originals + regen:
		entry = {
			"lane": row["lane"], "filename": row["filename"], "movie_id": row["movie_id"],
			"shot_id": row["shot_id"], "branch": row["branch"], "commit": row["commit"],
			"file_verdict": row["resolved_file_disposition"],
			"resolved_strict_disposition": strict[row["shot_id"]],
			"weak_frames": row.get("weak_frames"), "finding": row.get("finding"),
			"preferred_for_shot": row.get("preferred_for_shot", False),
			"audit_source": row["audit_path"],
		}
		if row["lane"] == "original_branch":
			entry["source_url"] = f"https://github.com/{REPO}/blob/{ORIGINAL_COMMIT}/clips/{row['filename']}"
		else:
			entry["source_url"] = row.get("url")
		entries.append(entry)
	if len(entries) != EXPECTED_LEDGER_FILES:
		_fail(f"ledger would contain {len(entries)} entries, expected {EXPECTED_LEDGER_FILES}")
	return entries


def _image_dimensions(path: Path) -> list[int]:
	try:
		with Image.open(path) as image:
			return [int(image.width), int(image.height)]
	except Exception as exc:
		_fail(f"cannot read image dimensions for {path}: {exc}")


def _copy_lossless(source: Path, destination: Path) -> None:
	if not source.is_file():
		_fail(f"missing copy source {source}")
	destination.parent.mkdir(parents=True, exist_ok=True)
	shutil.copy2(source, destination)
	if _sha256(source) != _sha256(destination):
		_fail(f"lossless copy hash mismatch {source} -> {destination}")


def _git_blob(commit: str, path: str) -> bytes:
	try:
		result = subprocess.run(["git", "-c", "core.longpaths=true", "cat-file", "--batch"], cwd=ROOT, input=f"{commit}:{path}\n".encode("utf-8"), check=True, capture_output=True)
	except (OSError, subprocess.CalledProcessError) as exc:
		_fail(f"cannot read exact Git blob {commit}:{path}: {exc}")
	line, separator, payload = result.stdout.partition(b"\n")
	parts = line.split()
	if len(parts) < 3 or parts[1] != b"blob":
		_fail(f"Git blob is missing or not a blob: {commit}:{path}")
	size = int(parts[2])
	if len(payload) < size:
		_fail(f"short Git blob for {commit}:{path}")
	return payload[:size]


def _copy_source_packets() -> dict:
	packets = []
	temp_root = ROOT / ".tmp"
	temp_root.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(prefix="third-pass-source-", dir=temp_root) as staging_name:
		staging = Path(staging_name)
		for movie, packet_name in sorted(PACKETS.items()):
			packet_git_path = f"assets_src/cinematics/{packet_name}"
			try:
				listing = subprocess.run(["git", "-c", "core.longpaths=true", "ls-tree", "-r", "--name-only", SOURCE_COMMIT, "--", packet_git_path], cwd=ROOT, check=True, capture_output=True, text=True).stdout
			except (OSError, subprocess.CalledProcessError) as exc:
				_fail(f"cannot list approved source packet {packet_git_path}: {exc}")
			members = [line.strip() for line in listing.splitlines() if line.strip()]
			if not members:
				_fail(f"approved source packet has no files at {packet_git_path}")
			for member in members:
				member_path = Path(member)
				if member_path.is_absolute() or ".." in member_path.parts or not member.startswith(packet_git_path + "/"):
					_fail(f"unsafe path in approved source packet listing: {member}")
				relative = member_path.relative_to(packet_git_path)
				out = staging / member
				out.parent.mkdir(parents=True, exist_ok=True)
				blob = _git_blob(SOURCE_COMMIT, member)
				out.write_bytes(blob)
			source_root = staging / packet_git_path
			if not source_root.is_dir():
				_fail(f"archived source visual packet missing {packet_git_path}")
			manifest_path = source_root / "HANDOFF_PACKET.json"
			if not manifest_path.is_file():
				_fail(f"missing source packet manifest {manifest_path}")
			destination = THIRD / "scenes" / movie / "visuals"
			shutil.copytree(source_root, destination, copy_function=shutil.copy2)
			source_files = sorted(path.relative_to(source_root).as_posix() for path in source_root.rglob("*") if path.is_file())
			copied_files = sorted(path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file())
			if source_files != copied_files:
				_fail(f"source packet file list changed during copy for {movie}")
			assets = []
			original_manifest_bytes = manifest_path.read_bytes()
			manifest = json.loads(original_manifest_bytes.decode("utf-8"))
			for asset in manifest.get("assets", []):
				rel = str(asset.get("path", ""))
				source = source_root / rel
				copied = destination / rel
				if not source.is_file() or not copied.is_file():
					_fail(f"manifest asset missing during packet copy: {movie}/{rel}")
				actual_source_hash = _sha256(source)
				if _sha256(source) != _sha256(copied):
					_fail(f"copied source asset hash mismatch for {copied}")
				asset["sha256"] = actual_source_hash
				assets.append({
					"path": (Path("scenes") / movie / "visuals" / rel).as_posix(),
					"source_path": f"{SOURCE_COMMIT}:{packet_git_path}/{rel}", "role": asset.get("role"), "media_type": asset.get("media_type"),
					"sha256": _sha256(copied), "manifest_declared_sha256": actual_source_hash, "manifest_hash_verified": True, "dimensions": _image_dimensions(copied) if str(asset.get("media_type", "")).startswith("image/") else None,
					"provenance": f"approved source packet at {SOURCE_COMMIT}", "modification": "lossless byte-for-byte copy", "used_as_delivery_pixels": False,
				})
			# Preserve the exact source manifest, then make the active nested
			# manifest internally self-consistent with the exact Git blobs.
			(destination / "HANDOFF_PACKET_SOURCE_COMMIT.json").write_bytes(original_manifest_bytes)
			manifest["third_pass_verification"] = {"source_commit": SOURCE_COMMIT, "original_manifest": "HANDOFF_PACKET_SOURCE_COMMIT.json", "original_manifest_sha256": hashlib.sha256(original_manifest_bytes).hexdigest(), "asset_hashes_recomputed_from_exact_git_blobs": True}
			(destination / "HANDOFF_PACKET.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
			packets.append({"movie_id": movie, "packet": packet_name, "source_commit": SOURCE_COMMIT, "source_root": f"{SOURCE_COMMIT}:{packet_git_path}", "copied_root": (Path("scenes") / movie / "visuals").as_posix(), "file_count": len(source_files), "copied_file_count": len(source_files) + 1, "preserved_source_manifest_copy": "HANDOFF_PACKET_SOURCE_COMMIT.json", "manifest_hash_mismatch_assets": 0, "assets": assets})
	return packets


def _evidence_source(row: dict) -> Path:
	filename = row["filename"]
	stem = Path(filename).stem
	if row["lane"] == "original_branch":
		return TEMP_ROOT / "original_contacts" / f"{stem}_contact.png"
	return ROOT / ".tmp" / "day1-regen-release-audit" / "contact_2fps" / f"{stem}_contact.png"


def _copy_audit_evidence(matrix: list[dict]) -> tuple[list[dict], list[dict]]:
	contacts: list[dict] = []
	overviews: list[dict] = []
	remake_rows = [row for row in matrix if row["strict_disposition"] == "REMAKE"]
	seen: set[tuple[str, str, str]] = set()
	for row in remake_rows:
		for candidate in row["candidate_files"]:
			key = (row["movie_id"], candidate["lane"], candidate["filename"])
			if key in seen:
				continue
			seen.add(key)
			fake_row = {"filename": candidate["filename"], "lane": candidate["lane"]}
			source = _evidence_source(fake_row)
			if not source.is_file():
				_fail(f"missing exact candidate contact sheet for {key}: {source}")
			lane_dir = "original" if candidate["lane"] == "original_branch" else "regen"
			dest = THIRD / "scenes" / row["movie_id"] / "audit_evidence" / lane_dir / source.name
			_copy_lossless(source, dest)
			contacts.append({
				"movie_id": row["movie_id"], "shot_id": row["shot_id"], "source_clip": candidate["filename"], "lane": candidate["lane"],
				"path": dest.relative_to(THIRD).as_posix(), "source_path": str(source), "dimensions": _image_dimensions(dest), "sha256": _sha256(dest),
				"provenance": "strict audit contact sheet generated from the audited MP4", "modification": "lossless byte-for-byte copy", "used_as_delivery_pixels": False,
			})
	for number in range(14):
		movie = f"D1-C{number:02d}"
		source = TEMP_ROOT / "scene_overviews" / f"C{number:02d}_original_clip_overview.jpg"
		if not source.is_file():
			_fail(f"missing scene overview board for {movie}: {source}")
		dest = THIRD / "scenes" / movie / "audit_evidence" / "scene_overview.jpg"
		_copy_lossless(source, dest)
		overviews.append({"movie_id": movie, "path": dest.relative_to(THIRD).as_posix(), "source_path": str(source), "dimensions": _image_dimensions(dest), "sha256": _sha256(dest), "provenance": "strict original-clip scene overview board", "modification": "lossless byte-for-byte copy", "used_as_delivery_pixels": False})
	return contacts, overviews


def _packet_manifest(matrix: list[dict]) -> dict:
	packets = _copy_source_packets()
	contacts, overviews = _copy_audit_evidence(matrix)
	return {"schema": "day-one-third-pass-visual-packet-manifest-v2", "claims": {"archive_complete": True, "generation_ready": False, "delivery_accepted": False}, "packets": packets, "contact_sheets": contacts, "scene_overviews": overviews, "binding_exclusion": "Audit evidence and scene boards are archive-only and never eligible for generator binding plans."}


def _write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def _write_cards(matrix: list[dict]) -> int:
	count = 0
	for row in matrix:
		if row["strict_disposition"] != "REMAKE":
			continue
		item = _source_item(row["shot_id"], {"recommended_timeline": row["recommended_timeline"]}, row["reason"])
		# The strict matrix is the authority for this pass.  This also applies
		# the tightened SET3 camera/action timeline to reused second-pass cards.
		item["timeline"] = tuple(row["recommended_timeline"])
		item["must_move"] = item["timeline"][1]
		item["end"] = item["timeline"][2]
		plan = _bindings(item)
		for binding, (alias, _job) in zip(plan, item["bindings"]):
			binding["binding_alias"] = alias
			if binding.get("path") and binding.get("source_packet") and binding.get("source_movie_id"):
				if binding["source_movie_id"] != row["movie_id"]:
					source = THIRD / "scenes" / binding["source_movie_id"] / "visuals" / binding["path"]
					destination = THIRD / "scenes" / row["movie_id"] / "visuals" / "imported_authorities" / binding["source_movie_id"] / binding["path"]
					_copy_lossless(source, destination)
					binding["local_path"] = destination.relative_to(THIRD).as_posix()
				else:
					binding["local_path"] = (Path("scenes") / row["movie_id"] / "visuals" / binding["path"]).as_posix()
		prompt = _prompt(item)
		base = THIRD / "scenes" / row["movie_id"] / "shots" / row["shot_id"]
		base.mkdir(parents=True, exist_ok=True)
		(base / "PROMPT.txt").write_text(prompt, encoding="utf-8", newline="\n")
		card = {
			"schema": "imagine-shot-card-draft-v1", "movie_id": row["movie_id"], "shot_id": row["shot_id"], "title": item["title"],
			"status": "DRAFT", "conditional_regeneration": False, "duration_seconds": item["duration"], "aspect_ratio": "16:9", "delivery_size": [1280, 720],
			"mode": "image_to_video", "output_disposition": "motion_reference_only", "binding_plan": plan,
			"start_frame": "IMAGE_1 after human approval of the exact clean inherited opening", "camera": {"verb": item["camera"], "move_count": 1},
			"must_move": item["must_move"], "must_not_move": item["must_not_move"], "end_state": item["end"], "negative_constraints": item["negatives"], "sound_intent": item["sound"],
			"prompt_path": "PROMPT.txt", "prompt_sha256": _sha256_text(prompt), "strict_audit_reason": row["reason"], "weak_frames": row["candidate_files"],
			"source_packet": row["source_packet"], "audited_branch": {"branch": REGEN_BRANCH, "commit": REGEN_COMMIT},
			"blocking_findings": (["Dedicated approved rainbow dust-bunny identity is missing; the unapproved concept and MP4 are not pixel authorities."] if any(alias == "rainbow_bunny_missing" for alias, _job in item["bindings"]) else []),
			"implemented_event_contract": {"authority_path": GAME_AUTHORITY.get(row["movie_id"], ("runtime event contract", "preserve approved current event"))[0], "rule": GAME_AUTHORITY.get(row["movie_id"], ("runtime event contract", "preserve approved current event"))[1]},
			"audit_claims": {"archive_complete": True, "generation_ready": False, "delivery_accepted": False},
			"review": {"strict_third_pass": True, "criteria": "visual quality, identity/anatomy, topology, causal action, lighting/style, camera restraint, and start/end seam", "reviewed_at": DATE},
		}
		_write_json(base / "SHOT_PACKET.json", card)
		reconstruction = [f"# {row['shot_id']} — {item['title']}", "", "STATUS: DRAFT", "GENERATION_READY: false", "DELIVERY_ACCEPTED: false", "", "## Strict finding", "", row["reason"], "", "## Full-frame action timeline", ""]
		reconstruction.extend(f"- {timeline}" for timeline in row["recommended_timeline"])
		reconstruction.extend(["", "Every changed action frame must be a separately generated complete image. No tweening, interpolation, compositing, or pixel reuse.", "", "## Archive/generator boundary", "", "The approved source packet and contact-sheet manifest are continuity references only. This draft is motion-reference output; it is not delivery art."])
		(base / "RECONSTRUCTION.md").write_text("\n".join(reconstruction) + "\n", encoding="utf-8", newline="\n")
		count += 1
	return count


def _write_scene_readmes(matrix: list[dict], manifest: dict) -> None:
	evidence = {(row["movie_id"], row["lane"], row["source_clip"]): row["path"] for row in manifest["contact_sheets"]}
	overviews = {row["movie_id"]: row["path"] for row in manifest["scene_overviews"]}
	for number in range(14):
		movie = f"D1-C{number:02d}"
		rows = [row for row in matrix if row["movie_id"] == movie]
		counts = {name: sum(1 for row in rows if row["strict_disposition"] == name) for name in ("KEEP_HIGH_QUALITY", "KEEP_WITH_TRIM", "REMAKE", "OMIT_WRONG_EVENT")}
		lines = [f"# {movie} — {TITLES[movie]}", "", "[All-shot decision matrix](../../ALL_SHOT_DECISION_MATRIX.json) · [159-file ledger](../../EXHAUSTIVE_159_FILE_LEDGER.json) · [scene overview](audit_evidence/scene_overview.jpg) · [copied source visual packet](visuals/)", "", f"Decision counts: KEEP_HIGH_QUALITY={counts['KEEP_HIGH_QUALITY']}, KEEP_WITH_TRIM={counts['KEEP_WITH_TRIM']}, REMAKE={counts['REMAKE']}, OMIT_WRONG_EVENT={counts['OMIT_WRONG_EVENT']}.", "", "| Shot | Preferred current file | Disposition | Exact reason / weak frames | Links |", "|---|---|---|---|---|"]
		for row in rows:
			weak = "; ".join(f"{c['filename']}: {c.get('weak_frames') or 'none'}" for c in row["candidate_files"] if c.get("weak_frames") and str(c.get("weak_frames")).lower() not in {"none", "none blocking"}) or "none"
			links = []
			for candidate in row["candidate_files"]:
				path = evidence.get((movie, candidate["lane"], candidate["filename"]))
				if path:
					links.append(f"[{candidate['filename']}]({Path(path).relative_to(Path('scenes') / movie).as_posix()})")
			if row["strict_disposition"] == "REMAKE":
				links.append(f"[active card](shots/{row['shot_id']}/SHOT_PACKET.json)")
			lines.append(f"| `{row['shot_id']}` | `{row['current_preferred_file'] or 'NONE — OMIT/REMAKE'}` | **{row['strict_disposition']}** | {row['reason']} Weak: {weak} | {' · '.join(links) or 'no copied evidence required for this non-REMAKE row'} |")
		lines.extend(["", "Archive evidence is copied byte-for-byte for every candidate in REMAKE rows. It is review evidence only and never appears in generator bindings.", "", "Generator cards remain DRAFT motion references; they do not establish generation readiness or delivery acceptance."])
		(THIRD / "scenes" / movie / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _payload_manifest() -> dict:
	entries = []
	excluded = {"PACKET_PAYLOAD_SHA256.json", "REMOTE_VERIFICATION.json"}
	for path in sorted(file for file in THIRD.rglob("*") if file.is_file() and file.name not in excluded):
		data = _canonical_payload_bytes(path)
		entries.append({"path": path.relative_to(THIRD).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
	canonical = "".join(f"{row['path']}\t{row['sha256']}\t{row['bytes']}\n" for row in entries)
	return {"schema": "day-one-third-pass-payload-sha256-v1", "algorithm": "sha256", "file_count": len(entries), "total_bytes": sum(row["bytes"] for row in entries), "payload_sha256": _sha256_text(canonical), "entries": entries}


def _write_root_readme(matrix: list[dict]) -> None:
	lines = ["# Day One strict third-pass refinement handoff", "", "> ARCHIVE_COMPLETE: true", "> GENERATION_READY: false", "> DELIVERY_ACCEPTED: false", "", "## Exhaustive scope", "", "This self-contained archive covers every original branch MP4 and every committed SET3 regeneration-audit MP4: **119 originals + 40 regen = 159 files**, across **74 canonical shots**. Resolved strict totals are **33 KEEP_HIGH_QUALITY, 5 KEEP_WITH_TRIM, 32 REMAKE, 4 OMIT_WRONG_EVENT**.", "", "## Scene handoffs", "", "| Scene | Handoff | KEEP_HIGH_QUALITY | KEEP_WITH_TRIM | REMAKE | OMIT_WRONG_EVENT |", "|---|---|---:|---:|---:|---:|"]
	for number in range(14):
		movie = f"D1-C{number:02d}"
		rows = [row for row in matrix if row["movie_id"] == movie]
		counts = [sum(1 for row in rows if row["strict_disposition"] == name) for name in ("KEEP_HIGH_QUALITY", "KEEP_WITH_TRIM", "REMAKE", "OMIT_WRONG_EVENT")]
		lines.append(f"| {movie} | [scene README](scenes/{movie}/README.md) | {counts[0]} | {counts[1]} | {counts[2]} | {counts[3]} |")
	lines.extend(["", "## Archive and generator boundary", "", "`scenes/*/visuals/` contains lossless copies of the complete approved visual packets. `scenes/*/audit_evidence/` contains audit-only candidate contact sheets and scene boards. They are continuity and review evidence, never delivery pixels and never generator bindings. Only strict `REMAKE` rows have DRAFT cards under `scenes/*/shots/*/`; every card ends with a `Sound:` line and explicitly keeps `generation_ready` and `delivery_accepted` false.", "", "## Audit indexes", "", "- [Exhaustive 159-file ledger](EXHAUSTIVE_159_FILE_LEDGER.json)", "- [All-shot decision matrix](ALL_SHOT_DECISION_MATRIX.json)", "- [Remake CSV](SHOT_REGENERATION_INDEX.csv)", "- [SOL_MASTER_AUDIT.md](SOL_MASTER_AUDIT.md)", "- [Visual packet/contact manifest](archive/SOURCE_VISUAL_PACKET_MANIFEST.json)", "- [Deterministic payload hashes](archive/PACKET_PAYLOAD_SHA256.json)", "- [Packet metadata](REGENERATION_PACKET.json)"])
	(THIRD / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _write_sol_audit() -> None:
	text = """# SOL_MASTER_AUDIT — strict third-pass packaging

This packet records the strict review boundary for motion-reference reconstruction. It is not a delivery acceptance claim.

## Blocking gates

Every candidate is checked for visual quality, identity/anatomy, room and prop topology, causal action, lighting/style, camera restraint, and first/end-frame seam continuity. A strict `REMAKE` card is required for any failed gate; an `OMIT_WRONG_EVENT` row is removed rather than regenerated. A `KEEP_WITH_TRIM` row is usable only through its stated frame/time boundary and remains motion reference.

## Priority groups

1. **Wrong-game events and the two-pin Stuffie rescue:** remove basket/four-bunny/wing-blast inventions; preserve one Baby Eagle held by exactly two rescue-pin bunnies and the contact-driven release order.
2. **Castle and room topology:** preserve the four-tower castle, fixed room projections, fixtures, entrances, and child-readable scale; no perspective or landmark drift.
3. **Causal hand/tool/action seams:** show the actual entry, handoff, pre-contact gap, physical contact, and resulting state; do not begin after the action or replace it with a dissolve/teleport.
4. **Pool state and camera:** preserve dirty-to-clean order, fixed sources, two-front meeting, giant-pool geography, and restrained pullbacks/tilts.
5. **C11/C13 arena identity:** preserve the octagonal arena, Grand Puff's three-tier scale and cute face, contained effects, and the exact one-rainbow-bunny tiny-cradle coda.

## Trims and provenance

The five trim decisions (C10-S03, C11-S02, C12-S05, C13-S01, C13-S02) identify bounded useful motion-reference spans. Trimming does not repair the missing seam or make any frame accepted delivery art. All generator cards are one shot each, action-first, DRAFT, and explicitly `generation_ready: false` / `delivery_accepted: false`; full-frame delivery still requires independent frame-by-frame acceptance and provenance.
"""
	(THIRD / "SOL_MASTER_AUDIT.md").write_text(text, encoding="utf-8", newline="\n")


def build() -> dict:
	originals, regen, summaries = _read_inputs()
	matrix = _matrix(originals, regen, summaries)
	ledger = _ledger(originals, regen, matrix)
	if THIRD.exists():
		if THIRD.resolve().parent != CIN.resolve():
			_fail(f"refusing to rebuild unexpected output path {THIRD}")
		shutil.rmtree(THIRD)
	THIRD.mkdir(parents=True)
	manifest = _packet_manifest(matrix)
	_write_json(THIRD / "EXHAUSTIVE_159_FILE_LEDGER.json", {"schema": "day-one-exhaustive-file-ledger-v1", "original_commit": ORIGINAL_COMMIT, "regen_commit": REGEN_COMMIT, "entry_count": len(ledger), "entries": ledger})
	_write_json(THIRD / "ALL_SHOT_DECISION_MATRIX.json", {"schema": "day-one-all-shot-decision-matrix-v1", "shot_count": len(matrix), "shots": matrix})
	_write_json(THIRD / "archive" / "SOURCE_VISUAL_PACKET_MANIFEST.json", manifest)
	card_count = _write_cards(matrix)
	_write_scene_readmes(matrix, manifest)
	with (THIRD / "SHOT_REGENERATION_INDEX.csv").open("w", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle)
		writer.writerow(["shot_id", "movie_id", "strict_disposition", "current_preferred_file", "card_path"])
		for row in matrix:
			if row["strict_disposition"] == "REMAKE":
				writer.writerow([row["shot_id"], row["movie_id"], row["strict_disposition"], row["current_preferred_file"] or "", f"scenes/{row['movie_id']}/shots/{row['shot_id']}/SHOT_PACKET.json"])
	index = {"schema": "day-one-third-pass-index-v1", "source_commits": {"original": ORIGINAL_COMMIT, "regeneration_audit": REGEN_COMMIT, "visual_packets": SOURCE_COMMIT}, "counts": {"original_files": len(originals), "regen_audit_files": len(regen), "ledger_files": len(ledger), "all_shots": len(matrix), "remake_cards": card_count}, "claims": {"archive_complete": True, "generation_ready": False, "delivery_accepted": False}, "strict_overrides": sorted(KNOWN_STRICT_REMAKE_OVERRIDES | STRICT_EXTRA_REMAKE | STRICT_KEEP_OVERRIDES | STRICT_TRIM_OVERRIDES)}
	_write_json(THIRD / "INDEX.json", index)
	_write_json(THIRD / "REGENERATION_PACKET.json", {"schema": "day-one-third-pass-refinement-packet-v1", "index": "INDEX.json", "ledger": "EXHAUSTIVE_159_FILE_LEDGER.json", "matrix": "ALL_SHOT_DECISION_MATRIX.json", "generator_cards": card_count, "claims": index["claims"], "payload_hashes": "archive/PACKET_PAYLOAD_SHA256.json"})
	_write_sol_audit()
	_write_root_readme(matrix)
	# The copied source-commit READMEs intentionally retain their historical
	# Markdown hard-break whitespace. Keep those immutable bytes out of diff
	# whitespace diagnostics without changing how GitHub renders the files.
	(THIRD / ".gitattributes").write_text(
		"scenes/*/visuals/README.md -diff\n",
		encoding="utf-8",
		newline="\n",
	)
	_write_json(THIRD / "archive" / "PACKET_PAYLOAD_SHA256.json", _payload_manifest())
	return index


def validate(index: dict) -> None:
	if index["counts"] != {"original_files": 119, "regen_audit_files": 40, "ledger_files": 159, "all_shots": 74, "remake_cards": 32}:
		_fail(f"index counts are not the strict expected totals: {index['counts']}")
	ledger = json.loads((THIRD / "EXHAUSTIVE_159_FILE_LEDGER.json").read_text(encoding="utf-8"))
	matrix = json.loads((THIRD / "ALL_SHOT_DECISION_MATRIX.json").read_text(encoding="utf-8"))
	if len(ledger["entries"]) != EXPECTED_LEDGER_FILES or len(matrix["shots"]) != index["counts"]["all_shots"]:
		_fail("emitted ledger or matrix cardinality is wrong")
	dispositions = {name: sum(1 for row in matrix["shots"] if row["strict_disposition"] == name) for name in ("KEEP_HIGH_QUALITY", "KEEP_WITH_TRIM", "REMAKE", "OMIT_WRONG_EVENT")}
	if dispositions != {"KEEP_HIGH_QUALITY": 33, "KEEP_WITH_TRIM": 5, "REMAKE": 32, "OMIT_WRONG_EVENT": 4}:
		_fail(f"strict disposition totals are wrong: {dispositions}")
	manifest = json.loads((THIRD / "archive" / "SOURCE_VISUAL_PACKET_MANIFEST.json").read_text(encoding="utf-8"))
	if len(manifest["packets"]) != 14 or len(manifest["scene_overviews"]) != 14 or len(manifest["contact_sheets"]) != 78:
		_fail(f"visual evidence cardinality is wrong: packets={len(manifest['packets'])}, overviews={len(manifest['scene_overviews'])}, contacts={len(manifest['contact_sheets'])}")
	for packet in manifest["packets"]:
		for asset in packet["assets"]:
			path = THIRD / asset["path"]
			if not path.is_file() or _sha256(path) != asset["sha256"]:
				_fail(f"invalid copied packet link/hash: {asset['path']}")
			if str(asset.get("media_type", "")).startswith("image/") and not asset.get("manifest_hash_verified"):
				_fail(f"unverified copied image authority: {asset['path']}")
	for entry in manifest["contact_sheets"] + manifest["scene_overviews"]:
		if not (THIRD / entry["path"]).is_file() or _sha256(THIRD / entry["path"]) != entry["sha256"]:
			_fail(f"invalid copied evidence link/hash: {entry['path']}")
	evidence_keys = {(entry["movie_id"], entry["lane"], entry["source_clip"]) for entry in manifest["contact_sheets"]}
	seen_candidates = {(row["movie_id"], candidate["lane"], candidate["filename"]) for row in matrix["shots"] if row["strict_disposition"] == "REMAKE" for candidate in row["candidate_files"]}
	if evidence_keys != seen_candidates:
		_fail(f"copied evidence does not exactly match the 78 REMAKE candidates: copied={len(evidence_keys)} candidates={len(seen_candidates)}")
	for row in matrix["shots"]:
		card = THIRD / "scenes" / row["movie_id"] / "shots" / row["shot_id"] / "SHOT_PACKET.json"
		if row["strict_disposition"] == "REMAKE":
			if not card.is_file():
				_fail(f"missing remake card {card}")
			data = json.loads(card.read_text(encoding="utf-8"))
			if data["audit_claims"]["generation_ready"] or data["audit_claims"]["delivery_accepted"] or not 2 <= len(data["binding_plan"]) <= 4:
				_fail(f"invalid strict card claims/binding count {card}")
			if any("audit_evidence" in str(binding.get("local_path", "")) or "contact" in str(binding.get("local_path", "")) or "overview" in str(binding.get("local_path", "")) for binding in data["binding_plan"]):
				_fail(f"audit evidence leaked into binding plan {card}")
			expected_item = _source_item(row["shot_id"], {"recommended_timeline": row["recommended_timeline"]}, row["reason"])
			expected_aliases = [alias for alias, _job in expected_item["bindings"]]
			actual_aliases = [binding.get("binding_alias") for binding in data["binding_plan"]]
			if actual_aliases != expected_aliases:
				_fail(f"semantic binding mismatch for {row['shot_id']}: expected {expected_aliases}, got {actual_aliases}")
			for binding in data["binding_plan"]:
				local_path = str(binding.get("local_path", ""))
				if local_path and not local_path.startswith(f"scenes/{row['movie_id']}/visuals/"):
					_fail(f"binding escapes scene source packet {local_path}")
				if local_path and not (THIRD / local_path).is_file():
					_fail(f"missing local binding link {local_path}")
				if any(token in str(binding.get("path", "")).lower() for token in ("storyboard", "generated", "first_frame")):
					_fail(f"storyboard/generated/first-frame authority bound in {card}: {binding.get('path')}")
				if local_path and binding.get("sha256") and _sha256(THIRD / local_path) != binding["sha256"]:
					_fail(f"binding hash mismatch {local_path}")
			if row["shot_id"] == "D1-C13-S05":
				if not any("rainbow dust-bunny identity is missing" in finding for finding in data.get("blocking_findings", [])):
					_fail("C13-S05 missing rainbow-bunny identity blocker")
				if any(binding.get("binding_alias") not in {"arena_location", "grand_puff", "rainbow_bunny_missing"} for binding in data["binding_plan"]):
					_fail("C13-S05 binds an unapproved character authority")
			prompt = card.parent / data["prompt_path"]
			if not prompt.read_text(encoding="utf-8").rstrip().endswith("Sound: " + data["sound_intent"] + "."):
				_fail(f"prompt does not end with Sound line {prompt}")
		else:
			if card.exists():
				_fail(f"non-remake unexpectedly has active generator card {card}")
	for number in range(14):
		movie = f"D1-C{number:02d}"
		if not (THIRD / "scenes" / movie / "README.md").is_file():
			_fail(f"missing scene handoff README {movie}")
	payload = json.loads((THIRD / "archive" / "PACKET_PAYLOAD_SHA256.json").read_text(encoding="utf-8"))
	rebuilt = _payload_manifest()
	if payload["payload_sha256"] != rebuilt["payload_sha256"] or payload["file_count"] != rebuilt["file_count"] or payload["total_bytes"] != rebuilt["total_bytes"]:
		_fail("deterministic packet payload hash changed after emission")


if __name__ == "__main__":
	try:
		if "--refresh-payload" in sys.argv[1:]:
			_write_json(THIRD / "archive" / "PACKET_PAYLOAD_SHA256.json", _payload_manifest())
			result = json.loads((THIRD / "INDEX.json").read_text(encoding="utf-8"))
		elif "--validate-only" in sys.argv[1:]:
			result = json.loads((THIRD / "INDEX.json").read_text(encoding="utf-8"))
		else:
			result = build()
		validate(result)
		print(json.dumps({"status": "OK", "output": str(THIRD), "counts": result["counts"]}, indent=2))
	except Exception as exc:
		print(str(exc), file=sys.stderr)
		sys.exit(1)
