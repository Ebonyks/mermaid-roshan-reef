"""Build the C14 cleanup visual handoff without granting human approval."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import shutil
from pathlib import Path

from PIL import Image

from build_day_one_grok_fourth_pass import frame_plan

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "assets_src/cinematics/d1_c14_castle_team_cleanup_v1"
EXPECTED_SHOTS = [f"C14-S{i:02d}" for i in range(1, 7)]
EXPECTED_DURATIONS = [5, 4, 5, 5, 6, 6]
EXCLUDED_FROM_PAYLOAD = {"HANDOFF_PACKET.json", "DRAFT_VALIDATION.json", "REMOTE_VERIFICATION.json"}
RASTER = {".png", ".jpg", ".jpeg", ".webp"}


class PacketError(ValueError):
	pass


def read_json(path: Path):
	return json.loads(path.read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value) -> None:
	write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(path: Path) -> str:
	with path.open("rb") as handle:
		return hashlib.file_digest(handle, "sha256").hexdigest()


def safe_inside(base: Path, relative: str) -> Path:
	target = (base / relative).resolve()
	try:
		target.relative_to(base.resolve())
	except ValueError as exc:
		raise PacketError(f"path escapes packet: {relative}") from exc
	return target


def dimensions(path: Path):
	if path.suffix.lower() not in RASTER:
		return None
	with Image.open(path) as image:
		return list(image.size)


def asset_row(packet: Path, path: Path, *, source_path: str, role: str,
		license_text: str, modifications: str) -> dict:
	row = {
		"path": path.relative_to(packet).as_posix(), "sha256": digest(path),
		"bytes": path.stat().st_size, "source_path": source_path, "role": role,
		"license_provenance": license_text, "modifications": modifications,
		"used_as_delivery_pixels": False,
		"media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
	}
	size = dimensions(path)
	if size:
		row["dimensions"] = size
	return row


def walk(value):
	if isinstance(value, dict):
		yield value
		for child in value.values():
			yield from walk(child)
	elif isinstance(value, list):
		for child in value:
			yield from walk(child)


def review_for(review_path: Path, visual_rel: str, sha256: str) -> dict | None:
	"""Return an exact path+hash record; never infer acceptance from prose."""
	if not review_path.is_file() or review_path.suffix.lower() != ".json":
		return None
	data = read_json(review_path)
	for row in walk(data):
		path = row.get("path") or row.get("file") or row.get("output_path")
		sha = row.get("sha256") or row.get("output_sha256") or row.get("hash")
		if isinstance(path, str) and isinstance(sha, str):
			if Path(path).as_posix() == Path(visual_rel).as_posix() and sha.lower() == sha256.lower():
				return row
	return None


def generation_record_for(packet: Path, visual_rel: str, sha256: str) -> tuple[Path, dict] | None:
	for path in sorted((packet / "generation_records").glob("*.json")):
		if path.name.startswith("SOL_"):
			continue
		data = read_json(path)
		for row in walk(data):
			output = row.get("output_path") or row.get("output") or row.get("path")
			declared = row.get("output_sha256") or row.get("sha256")
			if not isinstance(output, str) or not isinstance(declared, str):
				continue
			output_posix = Path(output).as_posix()
			visual_posix = Path(visual_rel).as_posix()
			if not (output_posix == visual_posix or output_posix.endswith("/" + visual_posix)) or declared.lower() != sha256.lower():
				continue
			prompt = row.get("prompt") or row.get("exact_tool_prompt") or row.get("full_prompt")
			method = row.get("generation_method") or row.get("method")
			inputs = row.get("input_images") or row.get("referenced_image_paths") or row.get("references")
			if not isinstance(prompt, str) or not prompt.strip() or not isinstance(method, str) or not method or not isinstance(inputs, list) or not inputs:
				continue
			prompt_sha = row.get("prompt_sha256")
			if prompt_sha and hashlib.sha256(prompt.encode()).hexdigest() != prompt_sha.lower():
				continue
			return path, row
	return None


def prompt_for(shot: dict) -> str:
	lines = []
	for phase in shot["phases"]:
		a, b = phase["range"]
		lines.append(f"{a / 24:.3f}–{b / 24:.3f}s: {phase['instruction'].rstrip('.')}.")
	keep = shot.get("prompt_keep", "architecture, declared cast identities, tools, and unaffected mess fixed")
	if isinstance(keep, list):
		keep = "; ".join(keep)
	negative = shot["negative"].strip().rstrip(".")
	if negative.lower().startswith("no "):
		negative = negative[3:]
	lines += ["", f"Camera: {shot['camera'].rstrip('.')}.", "Keep " + keep.rstrip(".") + ".",
		"End: " + shot["end"].rstrip(".") + ".",
		"No " + negative + ".",
		"Sound: " + shot["sound"].rstrip(".") + "."]
	return "\n".join(lines) + "\n"


def review_lines(review: dict | None) -> list[str]:
	if review is None:
		return ["Decision: **NOT EXACT-HASH REVIEWED**; human pending."]
	lines = [f"Decision: **{review.get('sol_decision', 'REVIEWED_WITHOUT_DECISION')}**; human pending."]
	fails = review.get("fails") or []
	if fails:
		lines += ["", "Known review findings:", "", *[f"- {finding}" for finding in fails]]
	caveat = review.get("required_caption") or review.get("targeted_revision") or review.get("note")
	if caveat:
		lines += ["", f"Review caveat: {caveat}"]
	return lines


def source_map(packet: Path) -> dict:
	data = read_json(packet / "SOURCE_ASSETS.json")
	rows = data.get("assets", [])
	if len({row.get("id") for row in rows}) != len(rows):
		raise PacketError("SOURCE_ASSETS ids must be unique")
	return {row["id"]: row for row in rows}


def _copy_reference(root: Path, packet: Path, row: dict) -> dict:
	source = (root / row["path"]).resolve()
	if not source.is_file():
		raise PacketError(f"missing source asset: {row['path']}")
	ext = source.suffix.lower() or ".bin"
	target = packet / "references" / f"{row['id']}{ext}"
	target.parent.mkdir(parents=True, exist_ok=True)
	if target.exists() and digest(target) != digest(source):
		raise PacketError(f"changed reference target: {target}")
	if not target.exists():
		shutil.copyfile(source, target)
	return asset_row(packet, target, source_path=row["path"], role=row["role"],
		license_text=row.get("license_provenance", "Inherits project ASSET_LICENSES.md and source restrictions; no new rights granted."),
		modifications="byte-identical non-destructive copy")


def audit_frame_source(packet: Path, path: Path) -> dict | None:
	if path.parent != packet / "audit/frames":
		return None
	prefix = path.stem.split("_t", 1)[0]
	review_path = packet / "audit/DOWNLOADS_REUSE_REVIEW.json"
	if not review_path.is_file():
		return None
	clip = next((row for row in read_json(review_path).get("clips", []) if row.get("prefix") == prefix), None)
	if clip is None:
		return None
	match = re.search(r"_t(\d+)_(\d+)$", path.stem)
	seconds = float(f"{match.group(1)}.{match.group(2)}") if match else None
	return {"source_path": clip["path"], "source_sha256": clip["sha256"], "timestamp_seconds": seconds,
		"method": "FFmpeg exact single-frame diagnostic decode at the filename wall-clock timestamp; representative audit evidence only, never generation or delivery pixels."}


def _design(packet: Path) -> list[dict]:
	shots = read_json(packet / "DESIGN.json").get("shots", [])
	if [s.get("shot") for s in shots] != EXPECTED_SHOTS:
		raise PacketError("DESIGN must contain C14-S01 through C14-S06 in order")
	if [s.get("duration_s") for s in shots] != EXPECTED_DURATIONS:
		raise PacketError("C14 durations must be 5/4/5/5/6/6 seconds")
	for shot in shots:
		count = shot["duration_s"] * 24
		for key in ("title", "camera", "invariants", "start", "end", "cast", "zone", "sound", "negative", "binding_ids", "editorial_start_s"):
			if key not in shot:
				raise PacketError(f"{shot['shot']}: missing {key}")
		if not 2 <= len(shot["binding_ids"]) <= 3 or len(set(shot["binding_ids"])) != len(shot["binding_ids"]):
			raise PacketError(f"{shot['shot']}: binding_ids must contain 2-3 unique source ids after IMAGE_1")
		ranges = [p.get("range") for p in shot.get("phases", [])]
		if not ranges or ranges[0][0] != 0 or ranges[-1][1] != count or any(ranges[i][1] != ranges[i + 1][0] for i in range(len(ranges) - 1)):
			raise PacketError(f"{shot['shot']}: phases must be contiguous [0,{count})")
	return shots


def build(packet: Path = DEFAULT_PACKET, root: Path = ROOT, *, develop: bool = True) -> dict:
	packet = packet.resolve(); root = root.resolve()
	shots = _design(packet); sources = source_map(packet)
	visuals = read_json(packet / "VISUALS.json").get("shots", {})
	template = root / "design/templates/IMAGINE_SHOT_CARD_V1.md"
	if not template.is_file():
		raise PacketError("missing design/templates/IMAGINE_SHOT_CARD_V1.md")
	template_copy = packet / "written_guide/IMAGINE_SHOT_CARD_V1.md"
	template_copy.parent.mkdir(parents=True, exist_ok=True)
	if template_copy.exists() and digest(template_copy) != digest(template):
		raise PacketError("changed shot-card template copy")
	if not template_copy.exists():
		shutil.copyfile(template, template_copy)
	reference_rows = {sid: _copy_reference(root, packet, row) for sid, row in sources.items()}
	gallery = ["# C14 approval gallery", "", "All visuals are human-pending drafts; boards are narrative-only and are never image bindings.", ""]
	readme = ["# D1 C14 castle team cleanup handoff", "", "ARCHIVE_COMPLETE: false  ", "GENERATION_READY: false  ", "DELIVERY_ACCEPTED: false", "", "Six shots, 31 seconds, 744 target frames. Human approval remains pending.", "", "[Approval gallery](APPROVAL_GALLERY.md) | [Cinematic direction](CINEMATIC_DIRECTION.md) | [Runtime seam plan](RUNTIME_SEAM_PLAN.md) | [Character locks](CHARACTER_LOCKS.json)", "", "[Downloads reuse review](audit/DOWNLOADS_REUSE_REVIEW.md) | [Visual audit](audit/SOL_VISUAL_REVIEW.md) | [Payload manifest](HANDOFF_PACKET.json) | [Draft validation](DRAFT_VALIDATION.json)", "", "## Shot jobs", ""]
	missing = []
	job_rows = []
	for shot in shots:
		sid = shot["shot"]; selected = visuals.get(sid, {})
		first_rel = selected.get("first_frame"); board_rel = selected.get("board"); review_rel = selected.get("review")
		first = safe_inside(packet, first_rel) if first_rel else None
		board = safe_inside(packet, board_rel) if board_rel else None
		for label, path in (("first_frame", first), ("board", board)):
			if path is None or not path.is_file():
				missing.append(f"{sid}: missing {label}")
		if any(bind not in sources for bind in shot["binding_ids"]):
			raise PacketError(f"{sid}: unknown binding id")
		if first is None or not first.is_file():
			continue
		first_sha = digest(first)
		review_path = safe_inside(packet, review_rel) if review_rel else Path()
		review = review_for(review_path, first_rel, first_sha) if review_rel else None
		if review is None:
			missing.append(f"{sid}: no exact path+hash first-frame review")
		first_generation = generation_record_for(packet, first_rel, first_sha)
		if first_generation is None:
			missing.append(f"{sid}: no exact first-frame generation record")
		board_generation = generation_record_for(packet, board_rel, digest(board)) if board is not None and board.is_file() else None
		board_review = review_for(review_path, board_rel, digest(board)) if review_rel and board is not None and board.is_file() else None
		if board is not None and board.is_file() and board_generation is None:
			missing.append(f"{sid}: no exact board generation record")
		bindings = [{"id": "IMAGE_1", "path": first_rel, "sha256": first_sha,
			"role": "approved_clean_first_frame", "role_status": "intended_role_pending_human_approval",
			"hud_present": False, "human_decision": "pending"}]
		for index, bind in enumerate(shot["binding_ids"], 2):
			row = reference_rows[bind]
			bindings.append({"id": f"IMAGE_{index}", "path": row["path"], "sha256": row["sha256"], "role": sources[bind]["role"],
				"hud_present": False, "human_decision": "pending", "source_authority_not_automatic_shot_approval": True})
		job = packet / "shots" / sid
		prompt = prompt_for(shot)
		write_text(job / "PROMPT.txt", prompt)
		plan = frame_plan({**shot, "shot": sid})
		write_json(job / "FRAME_PLAN.json", plan)
		camera_move = 0 if shot["camera"].lower().startswith("fixed") or "no camera movement" in shot["camera"].lower() else 1
		camera_verb = "locked" if camera_move == 0 else "pull_back" if "pullback" in shot["camera"].lower() else "single_move"
		write_json(job / "SHOT_PACKET.json", {
			"schema": "imagine-shot-packet-v1", "movie_id": "D1-C14", "shot_id": sid,
			"status": "DRAFT", "duration_seconds": shot["duration_s"], "fps": 24,
			"aspect_ratio": "16:9", "delivery_size": [1280, 720],
			"mode": "image_to_video", "output_disposition": "motion_reference_only",
			"bound_references": bindings, "camera": {"verb": camera_verb, "move_count": camera_move, "description": shot["camera"]}, "start_state": shot["start"],
			"end_state": shot["end"], "cast": shot["cast"], "zone": shot["zone"],
			"must_move": " ".join(phase["instruction"] for phase in shot["phases"] if phase.get("state") != "hold"),
			"must_not_move": shot["invariants"], "sound_intent": shot["sound"],
			"negative_constraints": [shot["negative"]], "prompt_path": f"shots/{sid}/PROMPT.txt",
			"prompt_sha256": digest(job / "PROMPT.txt"),
			"non_pixel_references": [] if board is None or not board.is_file() else [{"path": board_rel, "role": "narrative_storyboard", "used_as_pixel_reference": False}],
			"review_record": review_rel, "review_match": review is not None,
			"generation_provenance": {
				"first_frame_record": first_generation[0].relative_to(packet).as_posix() if first_generation else None,
				"board_record": board_generation[0].relative_to(packet).as_posix() if board_generation else None,
			},
			"human_decision": "pending", "generation_ready": False, "delivery_accepted": False,
		})
		binding_md = "\n".join(f"- {row['id']}: [{row['role']}](../../{row['path']})" for row in bindings)
		first_review_md = "\n".join(review_lines(review))
		board_review_md = "\n".join(review_lines(board_review))
		board_md = "" if board is None or not board.is_file() else f"\n## Narrative board — never bind\n\n{board_review_md}\n\n![{sid} board](../../{board_rel})\n"
		write_text(job / "README.md", f"# {sid} — {shot['title']}\n\nDraft only; human approval pending. Zone: {shot['zone']}. Duration: {shot['duration_s']}s.\n\nStart: {shot['start']}\n\nEnd: {shot['end']}\n\nCamera: {shot['camera']}\n\n## First frame\n\n{first_review_md}\n\n![{sid} first frame](../../{first_rel})\n{board_md}\n## Bound identities and layout\n\n{binding_md}\n\n[Prompt](PROMPT.txt) | [shot packet](SHOT_PACKET.json) | [target-frame plan](FRAME_PLAN.json)\n")
		gallery += [f"## {sid} — {shot['title']}", "", f"First frame `{first_rel}` / `{first_sha}`.", "", *review_lines(review), "", f"![{sid} first frame]({first_rel})", ""]
		if board is not None and board.is_file():
			gallery += ["Narrative board only; never bind as IMAGE input.", "", *review_lines(board_review), "", f"![{sid} board]({board_rel})", ""]
		job_rows.append({"shot_id": sid, "card": f"shots/{sid}/SHOT_PACKET.json", "human_approval_pending": True})
		readme += [f"- [{sid} — {shot['title']}](shots/{sid}/README.md): {shot['duration_s']}s; human pending."]
	write_text(packet / "README.md", "\n".join(readme))
	write_text(packet / "APPROVAL_GALLERY.md", "\n".join(gallery))
	write_json(packet / "IMAGINE_HANDOFF.json", {
		"schema": "imagine-handoff-v1", "archive_status": "incomplete", "generation_status": "blocked",
		"delivery_status": "not_accepted",
		"blocking_findings": sorted(set(missing + ["Exact first-frame human approval is pending for every job."])),
		"shot_packets": [], "pending_shot_packets": [row["card"] for row in job_rows],
		"note": "No executable jobs enabled. Structural validity and Sol review never imply visual quality or human approval."
	})
	# Manifest every packet payload file except self-referential/validation outputs.
	rows = []
	reference_by_path = {row["path"]: row for row in reference_rows.values()}
	for path in sorted(packet.rglob("*"), key=lambda p: p.relative_to(packet).as_posix()):
		if not path.is_file() or path.name in EXCLUDED_FROM_PAYLOAD or path.suffix.lower() in {".import", ".uid"}:
			continue
		rel = path.relative_to(packet).as_posix()
		if rel in reference_by_path:
			rows.append(reference_by_path[rel]); continue
		role = "archive_sidecar"
		if rel.startswith("references/"): role = "bound_reference_copy"
		elif rel.startswith("first_frames/"): role = "first_frame_candidate"
		elif rel.startswith("storyboards/"): role = "narrative_storyboard_not_binding"
		generation = generation_record_for(packet, rel, digest(path)) if role in {"first_frame_candidate", "narrative_storyboard_not_binding"} else None
		audit_source = audit_frame_source(packet, path)
		if audit_source:
			role = "diagnostic_downloads_source_frame"
		row = asset_row(packet, path, source_path=(audit_source["source_path"] if audit_source else generation[1].get("native_output_path") if generation else rel), role=role,
			license_text="Inherits SOURCE_ASSETS.json, generation record, and project ASSET_LICENSES.md restrictions; no new rights granted.",
			modifications=(audit_source["method"] if audit_source else f"native generated output preserved; method={generation[1].get('generation_method') or generation[1].get('method')}; attempt={generation[1].get('attempt')}" if generation else "packet-authored sidecar or preserved existing visual; see role and source ledger"))
		if generation:
			row["generation_record"] = generation[0].relative_to(packet).as_posix()
		if audit_source:
			row.update({"source_sha256": audit_source["source_sha256"], "decode_timestamp_seconds": audit_source["timestamp_seconds"], "diagnostic_only": True})
		rows.append(row)
	payload = "".join(f"{r['path']}\t{r['sha256']}\t{r['bytes']}\n" for r in rows).encode()
	write_json(packet / "HANDOFF_PACKET.json", {
		"schema": "external-animation-visual-packet-v1", "packet_id": packet.name,
		"archive_complete": False, "generation_ready": False, "delivery_accepted": False,
		"shot_count": len(shots), "duration_seconds": sum(s["duration_s"] for s in shots),
		"target_frame_count": sum(round(s["duration_s"] * 24) for s in shots),
		"assets": rows, "payload_sha256": hashlib.sha256(payload).hexdigest(),
		"payload_hash_formula": "SHA256 of sorted UTF-8 path TAB sha256 TAB bytes LF; excludes HANDOFF_PACKET.json, DRAFT_VALIDATION.json, REMOTE_VERIFICATION.json, .import and .uid",
		"jobs": job_rows, "blocking_findings": sorted(set(missing + ["human approval pending for every first frame"])),
	})
	result = validate(packet, root, strict=not develop)
	write_json(packet / "DRAFT_VALIDATION.json", result)
	return result


def validate(packet: Path = DEFAULT_PACKET, root: Path = ROOT, *, strict: bool = True) -> dict:
	packet = packet.resolve(); findings = []
	try:
		shots = _design(packet); sources = source_map(packet)
	except (OSError, KeyError, TypeError, PacketError, json.JSONDecodeError) as exc:
		return {"ok": False, "strict": strict, "findings": [str(exc)]}
	visuals = read_json(packet / "VISUALS.json").get("shots", {})
	if sum(s["duration_s"] for s in shots) != 31 or sum(round(s["duration_s"] * 24) for s in shots) != 744:
		findings.append("slate must total 31 seconds / 744 frames")
	for shot in shots:
		sid = shot["shot"]; selected = visuals.get(sid, {})
		for key in ("first_frame", "board", "review"):
			rel = selected.get(key)
			if not rel or not safe_inside(packet, rel).is_file(): findings.append(f"{sid}: missing {key}")
		first_rel = selected.get("first_frame")
		if first_rel and safe_inside(packet, first_rel).is_file():
			sha = digest(safe_inside(packet, first_rel))
			review_rel = selected.get("review")
			if not review_rel or review_for(safe_inside(packet, review_rel), first_rel, sha) is None:
				findings.append(f"{sid}: exact output path/hash absent from review record")
			if generation_record_for(packet, first_rel, sha) is None:
				findings.append(f"{sid}: exact first-frame generation provenance absent")
		board_rel = selected.get("board")
		if board_rel and safe_inside(packet, board_rel).is_file() and generation_record_for(packet, board_rel, digest(safe_inside(packet, board_rel))) is None:
			findings.append(f"{sid}: exact board generation provenance absent")
		card = packet / "shots" / sid / "SHOT_PACKET.json"
		prompt = packet / "shots" / sid / "PROMPT.txt"
		plan = packet / "shots" / sid / "FRAME_PLAN.json"
		if not all(p.is_file() for p in (card, prompt, plan)):
			findings.append(f"{sid}: generated job files missing"); continue
		card_data = read_json(card)
		if len(card_data.get("bound_references", [])) not in (3, 4): findings.append(f"{sid}: requires IMAGE_1 plus 2-3 sources")
		if any(r.get("role") == "narrative_storyboard" for r in card_data.get("bound_references", [])): findings.append(f"{sid}: board used as image binding")
		text = prompt.read_text(encoding="utf-8")
		if not text.rstrip().splitlines()[-1].startswith("Sound:"): findings.append(f"{sid}: Sound must be last")
		if read_json(plan).get("target_frame_count") != shot["duration_s"] * 24: findings.append(f"{sid}: frame-plan count mismatch")
	for sid, row in sources.items():
		source = (root / row["path"]).resolve(); target = packet / "references" / f"{sid}{source.suffix.lower() or '.bin'}"
		if not source.is_file() or not target.is_file() or digest(source) != digest(target): findings.append(f"{sid}: reference copy missing or not byte-identical")
	manifest_path = packet / "HANDOFF_PACKET.json"
	if not manifest_path.is_file(): findings.append("HANDOFF_PACKET.json missing")
	else:
		manifest = read_json(manifest_path); rows = manifest.get("assets", [])
		if manifest.get("archive_complete") or manifest.get("generation_ready") or manifest.get("delivery_accepted"):
			findings.append("packet status must remain fail-closed")
		for row in rows:
			path = safe_inside(packet, row["path"])
			if not path.is_file() or digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
				findings.append(f"manifest mismatch: {row.get('path')}")
		expected_paths = sorted(path.relative_to(packet).as_posix() for path in packet.rglob("*") if path.is_file() and path.name not in EXCLUDED_FROM_PAYLOAD and path.suffix.lower() not in {".import", ".uid"})
		if sorted(row.get("path") for row in rows) != expected_paths:
			findings.append("manifest payload file list is incomplete or contains extras")
		payload = "".join(f"{r['path']}\t{r['sha256']}\t{r['bytes']}\n" for r in sorted(rows, key=lambda r: r["path"])).encode()
		if hashlib.sha256(payload).hexdigest() != manifest.get("payload_sha256"): findings.append("payload hash mismatch")
	# Generated packet navigation is locally resolvable; external and anchor links are ignored.
	for markdown in [packet / "README.md", packet / "APPROVAL_GALLERY.md", *sorted((packet / "shots").glob("*/README.md"))]:
		if not markdown.is_file():
			continue
		for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
			target = target.strip().split("#", 1)[0]
			if not target or "://" in target or target.startswith("#"):
				continue
			if markdown == packet / "README.md" and target == "DRAFT_VALIDATION.json":
				continue  # Written immediately after this validation pass; excluded from payload by design.
			if not (markdown.parent / target).resolve().is_file():
				findings.append(f"broken local markdown link: {markdown.relative_to(packet).as_posix()} -> {target}")
	ok = not findings if strict else not [f for f in findings if "missing" not in f and "absent" not in f]
	return {"schema": "c14-handoff-validation-v1", "ok": ok, "strict": strict,
		"archive_complete": False, "generation_ready": False, "delivery_accepted": False,
		"shot_count": 6, "duration_seconds": 31, "target_frame_count": 744, "findings": findings}


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
	parser.add_argument("--root", type=Path, default=ROOT)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--build", action="store_true", help="develop build; records missing visuals without claiming readiness")
	mode.add_argument("--validate", action="store_true", help="strict validation; missing visuals/reviews fail")
	args = parser.parse_args()
	result = build(args.packet, args.root, develop=True) if args.build else validate(args.packet, args.root, strict=True)
	print(json.dumps(result, indent=2))
	return 0 if result["ok"] else 1


if __name__ == "__main__":
	raise SystemExit(main())
