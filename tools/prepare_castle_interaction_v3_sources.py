#!/usr/bin/env python3
"""Prepare the 38 Pearl Castle v3 ImageGen source sheets exactly once.

Native ImageGen files are retained outside the repository and identified by
hash in the batch provenance drafts.  Repository source masters must be small,
deterministic 4x2 chroma sheets.  This tool splits the conceptual source grid,
fits every complete cell without aspect distortion onto a 256px square, and
normalizes only the border-connected magenta field.  Subject edge pixels get a
bounded chroma despill; no state is painted, warped, or synthesized.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

from PIL import Image

from castle_interaction_v3_specs import ADDITIONS


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "assets_src/imagegen/castle_object_animations_v3"
REPORT = RAW_ROOT / "castle_interactions_v3_source_preparation.json"
TARGET_SIZE = (1024, 512)
TARGET_CELL = 256
TARGET_INSET = 4
GLOBAL_KEY_DISTANCE = 96.0
GRID = (4, 2)
KEY = (255, 0, 255)
EXPECTED_COUNT = 38


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def text_sha256(value: str) -> str:
	return hashlib.sha256(value.encode("utf-8")).hexdigest()


def repository_text_sha256(path: Path) -> str:
	data = path.read_bytes().replace(b"\r\n", b"\n")
	return hashlib.sha256(data).hexdigest()


def source_path(entry: dict[str, Any]) -> Path:
	name = f"{entry['id']}_sheet_chroma.png"
	matches = sorted(RAW_ROOT.rglob(name))
	if len(matches) != 1:
		raise ValueError(f"{entry['id']}: expected one {name}, found {len(matches)}")
	return matches[0]


def _nested(entry: dict[str, Any], *keys: str) -> Any:
	value: Any = entry
	for key in keys:
		if not isinstance(value, dict):
			return None
		value = value.get(key)
	return value


def _first_string(entry: dict[str, Any], candidates: list[tuple[str, ...]]) -> str:
	for keys in candidates:
		value = _nested(entry, *keys)
		if isinstance(value, str) and value.strip():
			return value.strip()
	return ""


def _first_dimensions(entry: dict[str, Any]) -> list[int]:
	for keys in [
		("generation", "native_dimensions"),
		("generation", "dimensions"),
		("copied_output", "dimensions"),
	]:
		value = _nested(entry, *keys)
		if isinstance(value, dict):
			value = [value.get("width"), value.get("height")]
		if (
			isinstance(value, list)
			and len(value) == 2
			and all(isinstance(component, int) for component in value)
		):
			return [int(value[0]), int(value[1])]
	return []


def provenance_records() -> dict[str, dict[str, Any]]:
	"""Flatten deliberately heterogeneous batch drafts into one contract."""
	index: dict[str, dict[str, Any]] = {}
	for path in sorted(RAW_ROOT.rglob("provenance_draft.json")):
		parsed = json.loads(path.read_text(encoding="utf-8"))
		assets = parsed.get("assets", [])
		if not isinstance(assets, list):
			raise ValueError(f"{path.relative_to(ROOT)}: assets is not a list")
		for value in assets:
			if not isinstance(value, dict):
				continue
			asset_id = str(value.get("id", ""))
			if not asset_id:
				continue
			if asset_id in index:
				raise ValueError(f"duplicate provenance for {asset_id}")
			prompt = _first_string(value, [
				("generation", "accepted_prompt"),
				("accepted_retry_prompt",),
				("accepted_prompt",),
				("prompt",),
			])
			native_path = _first_string(value, [
				("generation", "accepted_native_path"),
				("generation", "native_path"),
				("generation", "native"),
				("native",),
			])
			native_hash = _first_string(value, [
				("generation", "native_sha256"),
				("native_sha256",),
				("copied_output", "sha256"),
				("chroma_master", "sha256"),
				("sha256",),
			])
			review_status = _first_string(value, [
				("codex_visual_review", "status"),
				("visual_review", "status"),
				("review_status",),
			]) or str(parsed.get("review_status", ""))
			review_notes = _first_string(value, [
				("codex_visual_review", "notes"),
				("visual_review", "notes"),
				("review_notes",),
			])
			attempt_value = (
				_nested(value, "generation", "accepted_attempt")
				or _nested(value, "generation", "attempt")
				or value.get("attempt", 1)
			)
			index[asset_id] = {
				"batch_manifest": path.relative_to(ROOT).as_posix(),
				"batch_manifest_sha256": repository_text_sha256(path),
				"generation_method": _first_string(value, [
					("generation", "method"),
				]) or str(parsed.get("generation_method", "OpenAI built-in image_gen.imagegen")),
				"accepted_attempt": int(attempt_value),
				"accepted_prompt": prompt,
				"accepted_prompt_sha256": text_sha256(prompt) if prompt else "",
				"accepted_native_path": native_path,
				"accepted_native_sha256": native_hash,
				"accepted_native_dimensions": _first_dimensions(value),
				"codex_visual_review_status": review_status,
				"codex_visual_review_notes": review_notes,
				"human_review_status": _first_string(value, [
					("human_review", "status"),
				]) or "pending",
			}
	return index


def _review_is_accepted(status: str) -> bool:
	normalized = status.strip().lower()
	return "accepted" in normalized or normalized.startswith("pass")


def provenance_errors(asset_id: str, record: dict[str, Any]) -> list[str]:
	errors: list[str] = []
	if int(record.get("accepted_attempt", 0)) < 1:
		errors.append(f"{asset_id}: accepted generation attempt is missing")
	if not record.get("accepted_prompt") or not record.get("accepted_prompt_sha256"):
		errors.append(f"{asset_id}: accepted prompt provenance is missing")
	native_hash = str(record.get("accepted_native_sha256", ""))
	if len(native_hash) != 64 or any(character not in "0123456789abcdef" for character in native_hash):
		errors.append(f"{asset_id}: accepted native SHA-256 is invalid")
	dimensions = record.get("accepted_native_dimensions", [])
	if (
		not isinstance(dimensions, list)
		or len(dimensions) != 2
		or not all(isinstance(value, int) and value > 0 for value in dimensions)
	):
		errors.append(f"{asset_id}: accepted native dimensions are invalid")
	if not _review_is_accepted(str(record.get("codex_visual_review_status", ""))):
		errors.append(f"{asset_id}: Codex visual review is not accepted")
	if str(record.get("human_review_status", "")).strip().lower() not in {"pending", "accepted"}:
		errors.append(f"{asset_id}: human review status is invalid")
	manifest_value = str(record.get("batch_manifest", ""))
	manifest_path = ROOT / manifest_value
	if not manifest_value or not manifest_path.is_file():
		errors.append(f"{asset_id}: batch provenance manifest is missing")
	elif record.get("batch_manifest_sha256") != repository_text_sha256(manifest_path):
		errors.append(f"{asset_id}: batch provenance manifest hash is stale")
	return errors


def _magenta_like(pixel: tuple[int, int, int]) -> bool:
	red, green, blue = pixel
	return (
		red >= 145
		and blue >= 145
		and green <= 145
		and min(red, blue) - green >= 52
		and abs(red - blue) <= 96
	)


def _key_distance(pixel: tuple[int, int, int]) -> float:
	red, green, blue = pixel
	return math.sqrt((255 - red) ** 2 + green ** 2 + (255 - blue) ** 2)


def normalize_connected_chroma(cell: Image.Image) -> tuple[Image.Image, dict[str, int]]:
	"""Flatten the exterior field and safely remove edge-key contamination."""
	image = cell.convert("RGB")
	width, height = image.size
	pixels = list(image.getdata())
	seen = bytearray(width * height)
	field = bytearray(width * height)
	queue: deque[int] = deque()

	def offer(index: int) -> None:
		if not seen[index] and _magenta_like(pixels[index]):
			seen[index] = 1
			queue.append(index)

	for x in range(width):
		offer(x)
		offer((height - 1) * width + x)
	for y in range(height):
		offer(y * width)
		offer(y * width + width - 1)
	while queue:
		current = queue.popleft()
		field[current] = 1
		x = current % width
		y = current // width
		if x:
			offer(current - 1)
		if x + 1 < width:
			offer(current + 1)
		if y:
			offer(current - width)
		if y + 1 < height:
			offer(current + width)

	# ImageGen can shade the key field inside enclosed fixture gaps slightly
	# differently from the exterior field. Prompts prohibit key-magenta inside
	# subjects, so classify the bounded near-key cluster globally. This removes
	# the opaque magenta cards formerly left inside horse rockers and quill arms.
	global_near_key = 0
	for index, pixel in enumerate(pixels):
		if _key_distance(pixel) <= GLOBAL_KEY_DISTANCE:
			if not field[index]:
				global_near_key += 1
			field[index] = 1

	output = list(pixels)
	for index, is_field in enumerate(field):
		if is_field:
			output[index] = KEY

	# Despill only subject pixels immediately adjacent to the proven field.
	# Estimate a foreground color by undoing a bounded magenta mix.
	despilled = 0
	for index, pixel in enumerate(pixels):
		if field[index] or not _magenta_like(pixel):
			continue
		x = index % width
		y = index // width
		neighbors = []
		if x:
			neighbors.append(index - 1)
		if x + 1 < width:
			neighbors.append(index + 1)
		if y:
			neighbors.append(index - width)
		if y + 1 < height:
			neighbors.append(index + width)
		if not any(field[neighbor] for neighbor in neighbors):
			continue
		distance = _key_distance(pixel)
		if distance >= 150.0:
			continue
		alpha = min(1.0, max(0.24, distance / 150.0))
		foreground = []
		for value, key_value in zip(pixel, KEY):
			unmixed = (float(value) - (1.0 - alpha) * key_value) / alpha
			foreground.append(max(0, min(255, int(round(unmixed)))))
		output[index] = tuple(foreground)
		despilled += 1

	prepared = Image.new("RGB", image.size)
	prepared.putdata(output)
	return prepared, {
		"key_field_pixels": int(sum(field)),
		"global_near_key_pixels": global_near_key,
		"edge_despill_pixels": despilled,
	}


def prepare_sheet(path: Path, destination: Path) -> dict[str, Any]:
	with Image.open(path) as source_image:
		source = source_image.convert("RGB")
	input_size = list(source.size)
	canvas = Image.new("RGB", TARGET_SIZE, KEY)
	field_pixels = 0
	global_near_key_pixels = 0
	despill_pixels = 0
	cell_transforms: list[dict[str, Any]] = []
	for index in range(8):
		column = index % GRID[0]
		row = index // GRID[0]
		left = int(round(column * source.width / GRID[0]))
		right = int(round((column + 1) * source.width / GRID[0]))
		top = int(round(row * source.height / GRID[1]))
		bottom = int(round((row + 1) * source.height / GRID[1]))
		cell, stats = normalize_connected_chroma(
			source.crop((left, top, right, bottom))
		)
		field_pixels += stats["key_field_pixels"]
		global_near_key_pixels += stats["global_near_key_pixels"]
		despill_pixels += stats["edge_despill_pixels"]
		available = TARGET_CELL - TARGET_INSET * 2
		scale = min(available / cell.width, available / cell.height)
		resized_size = (
			max(1, int(round(cell.width * scale))),
			max(1, int(round(cell.height * scale))),
		)
		if resized_size != cell.size:
			cell = cell.resize(resized_size, Image.Resampling.LANCZOS)
		# Resampling can perturb the uniform key along the image boundary.
		cell, post_stats = normalize_connected_chroma(cell)
		field_pixels += post_stats["key_field_pixels"]
		global_near_key_pixels += post_stats["global_near_key_pixels"]
		despill_pixels += post_stats["edge_despill_pixels"]
		destination_xy = (
			column * TARGET_CELL + (TARGET_CELL - cell.width) // 2,
			row * TARGET_CELL + (TARGET_CELL - cell.height) // 2,
		)
		canvas.paste(cell, destination_xy)
		cell_transforms.append({
			"frame": index,
			"source_box": [left, top, right, bottom],
			"uniform_scale": round(scale, 9),
			"prepared_size": list(cell.size),
			"prepared_offset": list(destination_xy),
			"exact_chroma_inset_pixels": TARGET_INSET,
		})
	destination.parent.mkdir(parents=True, exist_ok=True)
	canvas.save(destination, optimize=True, compress_level=9)
	return {
		"input_dimensions": input_size,
		"prepared_dimensions": list(TARGET_SIZE),
		"grid": list(GRID),
		"cell_size": [TARGET_CELL, TARGET_CELL],
		"exact_chroma_inset_pixels": TARGET_INSET,
		"whole_cell_uniform_scale_only": True,
		"cell_transforms": cell_transforms,
		"key_field_pixels_normalized": field_pixels,
		"global_near_key_pixels_normalized": global_near_key_pixels,
		"global_key_distance": GLOBAL_KEY_DISTANCE,
		"edge_despill_pixels": despill_pixels,
	}


def validate_prepared(path: Path) -> list[str]:
	errors: list[str] = []
	if not path.is_file():
		return ["prepared source is missing"]
	with Image.open(path) as image_value:
		image = image_value.convert("RGB")
	if image.size != TARGET_SIZE:
		errors.append(f"dimensions {image.size} != {TARGET_SIZE}")
	if max(image.size) > 1024:
		errors.append("longest edge exceeds 1024")
	for index in range(8):
		column = index % 4
		row = index // 4
		cell = image.crop((
			column * TARGET_CELL,
			row * TARGET_CELL,
			(column + 1) * TARGET_CELL,
			(row + 1) * TARGET_CELL,
		))
		inset_pixels = (
			list(cell.crop((0, 0, cell.width, TARGET_INSET)).getdata())
			+ list(cell.crop((0, cell.height - TARGET_INSET, cell.width, cell.height)).getdata())
			+ list(cell.crop((0, TARGET_INSET, TARGET_INSET, cell.height - TARGET_INSET)).getdata())
			+ list(cell.crop((cell.width - TARGET_INSET, TARGET_INSET, cell.width, cell.height - TARGET_INSET)).getdata())
		)
		if any(pixel != KEY for pixel in inset_pixels):
			errors.append(
				f"frame {index} does not have an exact {TARGET_INSET}px chroma inset")
	return errors


def check_report() -> int:
	if not REPORT.is_file():
		print("FAIL: v3 source preparation report is missing")
		return 1
	report = json.loads(REPORT.read_text(encoding="utf-8"))
	errors: list[str] = []
	entries = report.get("assets", [])
	expected_ids = {str(entry["id"]) for entry in ADDITIONS}
	if report.get("tool_sha256") != repository_text_sha256(Path(__file__)):
		errors.append("preparation tool hash differs from report")
	if int(report.get("schema_version", 0)) != 3:
		errors.append("source preparation schema is not 3")
	if report.get("target_dimensions") != list(TARGET_SIZE):
		errors.append("source preparation target dimensions are stale")
	if report.get("grid") != list(GRID):
		errors.append("source preparation grid is stale")
	if int(report.get("exact_chroma_inset_pixels", -1)) != TARGET_INSET:
		errors.append("source preparation chroma inset is stale")
	if float(report.get("global_key_distance", -1.0)) != GLOBAL_KEY_DISTANCE:
		errors.append("source preparation global key distance is stale")
	if "before this one-time preparation" not in str(report.get("repository_copy_semantics", "")):
		errors.append("source preparation repository-copy semantics are missing")
	if int(report.get("asset_count", -1)) != EXPECTED_COUNT or len(entries) != EXPECTED_COUNT:
		errors.append(f"prepared roster has {len(entries)} assets")
	entry_ids = {str(entry.get("id", "")) for entry in entries}
	if entry_ids != expected_ids:
		errors.append("prepared source IDs differ from the 38 v3 specs")
	current_provenance = provenance_records()
	for entry in entries:
		asset_id = str(entry.get("id", ""))
		path = ROOT / str(entry.get("path", ""))
		if not path.is_file() or sha256(path) != entry.get("prepared_sha256"):
			errors.append(f"{asset_id}: prepared source is missing or stale")
		for error in validate_prepared(path):
			errors.append(f"{asset_id}: {error}")
		provenance = entry.get("provenance", {})
		if not isinstance(provenance, dict):
			errors.append(f"{asset_id}: prepared provenance is malformed")
			continue
		errors.extend(provenance_errors(asset_id, provenance))
		current = current_provenance.get(asset_id, {})
		for field in (
			"batch_manifest",
			"batch_manifest_sha256",
			"generation_method",
			"accepted_attempt",
			"accepted_prompt",
			"accepted_prompt_sha256",
			"accepted_native_path",
			"codex_visual_review_status",
			"codex_visual_review_notes",
			"human_review_status",
		):
			if provenance.get(field) != current.get(field):
				errors.append(f"{asset_id}: provenance field {field} is stale")
		current_hash = str(current.get("accepted_native_sha256", ""))
		if current_hash and provenance.get("accepted_native_sha256") != current_hash:
			errors.append(f"{asset_id}: accepted native hash differs from provenance")
	if errors:
		for error in errors:
			print("FAIL: " + error)
		return 1
	print(f"CASTLEV3|SOURCE_PREPARATION_OK|assets={len(entries)}|size=1024x512")
	return 0


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	if args.check:
		return check_report()
	if REPORT.exists():
		print("FAIL: source preparation report exists; use --check")
		return 1
	provenance = provenance_records()
	expected_ids = {str(entry["id"]) for entry in ADDITIONS}
	if set(provenance) != expected_ids:
		missing = sorted(expected_ids - set(provenance))
		extra = sorted(set(provenance) - expected_ids)
		raise SystemExit(f"provenance roster mismatch; missing={missing}, extra={extra}")
	for asset_id, record in provenance.items():
		if not record.get("accepted_prompt") or not _review_is_accepted(
			str(record.get("codex_visual_review_status", ""))
		):
			raise SystemExit(f"{asset_id}: prompt or accepted Codex review is missing")
	paths = [source_path(entry) for entry in ADDITIONS]
	missing_paths = [path.relative_to(ROOT).as_posix() for path in paths if not path.is_file()]
	if missing_paths:
		raise SystemExit("missing source masters: " + ", ".join(missing_paths))

	stage_root = Path(tempfile.mkdtemp(prefix=".castle_v3_prepare_", dir=RAW_ROOT))
	backup_root = stage_root / "backup"
	prepared_root = stage_root / "prepared"
	assets: list[dict[str, Any]] = []
	committed: list[Path] = []
	try:
		staged: dict[Path, Path] = {}
		for spec in ADDITIONS:
			asset_id = str(spec["id"])
			path = source_path(spec)
			input_hash = sha256(path)
			record = provenance[asset_id].copy()
			native_candidate = Path(str(record.get("accepted_native_path", "")))
			metadata_path = native_candidate if native_candidate.is_file() else path
			metadata_source = (
				"accepted_native_file" if native_candidate.is_file()
				else "byte_identical_repository_copy"
			)
			metadata_hash = sha256(metadata_path)
			with Image.open(metadata_path) as native_image:
				metadata_dimensions = list(native_image.size)
			if metadata_hash != input_hash:
				raise ValueError(
					f"{asset_id}: repository copy differs from accepted native")
			native_hash = str(record.get("accepted_native_sha256", ""))
			if native_hash and native_hash != metadata_hash:
				raise ValueError(f"{asset_id}: declared native hash is stale")
			native_dimensions = record.get("accepted_native_dimensions", [])
			if native_dimensions and list(native_dimensions) != metadata_dimensions:
				raise ValueError(f"{asset_id}: declared native dimensions are stale")
			record["accepted_native_sha256"] = metadata_hash
			record["accepted_native_dimensions"] = metadata_dimensions
			record["native_metadata_source"] = metadata_source
			record_errors = provenance_errors(asset_id, record)
			if record_errors:
				raise ValueError("; ".join(record_errors))
			staged_path = prepared_root / str(spec["room"]) / path.name
			metrics = prepare_sheet(path, staged_path)
			validation_errors = validate_prepared(staged_path)
			if validation_errors:
				raise ValueError(f"{asset_id}: {'; '.join(validation_errors)}")
			staged[path] = staged_path
			assets.append({
				"id": asset_id,
				"room": spec["room"],
				"path": path.relative_to(ROOT).as_posix(),
				"native_copy_sha256": input_hash,
				"prepared_sha256": sha256(staged_path),
				**metrics,
				"connected_outer_field_plus_global_near_key": True,
				"accepted_native_copy_before_preparation_sha256": input_hash,
				"current_repository_path_hash_field": "prepared_sha256",
				"subject_geometry_warped": False,
				"state_pixels_synthesized": False,
				"provenance": record,
			})
		counts = Counter(str(entry["room"]) for entry in assets)
		payload = {
			"schema_version": 3,
			"generated_on": "2026-08-02",
			"tool": "tools/prepare_castle_interaction_v3_sources.py",
			"tool_sha256": repository_text_sha256(Path(__file__)),
			"transactional": True,
			"one_time_guard": True,
			"target_dimensions": list(TARGET_SIZE),
			"grid": list(GRID),
			"exact_chroma_inset_pixels": TARGET_INSET,
			"method": "conceptual_cell_uniform_fit_plus_connected_and_global_near_key_normalization_and_edge_despill",
			"global_key_distance": GLOBAL_KEY_DISTANCE,
			"native_files_preserved_outside_repository": True,
			"repository_copy_semantics": (
				"Batch provenance chroma_master/copied_output hashes identify the "
				"accepted byte-identical repository copy before this one-time "
				"preparation. After preparation, each current repository path is "
				"authoritative only through its prepared_sha256 field."
			),
			"asset_count": len(assets),
			"room_counts": dict(sorted(counts.items())),
			"assets": assets,
		}
		report_stage = stage_root / REPORT.name
		report_stage.write_bytes((json.dumps(payload, indent=2) + "\n").encode("utf-8"))
		backup_root.mkdir(parents=True, exist_ok=True)
		for path in paths:
			shutil.copy2(path, backup_root / path.name)
		try:
			for path, staged_path in staged.items():
				os.replace(staged_path, path)
				committed.append(path)
			os.replace(report_stage, REPORT)
		except Exception:
			if REPORT.exists():
				REPORT.unlink()
			for path in committed:
				shutil.copy2(backup_root / path.name, path)
			raise
	finally:
		shutil.rmtree(stage_root, ignore_errors=True)
	print(f"PREPARED|assets={len(assets)}|size=1024x512|transactional=true")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
