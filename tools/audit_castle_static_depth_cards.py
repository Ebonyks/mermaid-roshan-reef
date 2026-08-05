#!/usr/bin/env python3
"""Block unowned alpha in the Castle's active static depth cards.

The runtime layout and the refinement provenance are independent inputs.  This
gate requires their active ``mid``/``front`` card sets to agree exactly, then
checks the delivered PNG bytes, decoded alpha, crop-local approved shapes, and
transparent-pixel RGB.  It never writes files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
	"assets_src/castle/depth_cards/static_depth_card_refinement.json")
EXPECTED_LAYOUT = "scripts/arena/castle_rooms_25d.gd"
POOL_MID_PATH = (
	"assets/flats/castle/rooms/room_mermaid_pool_mid_pool.png")
POOL_MID_BASENAME = Path(POOL_MID_PATH).name
ROOM_CARD_ROOT = "assets/flats/castle/rooms"
RUNTIME_SCAN_ROOTS = ("scripts", "scenes", "assets")
RUNTIME_TEXT_SUFFIXES = {".gd", ".tscn", ".tres", ".godot", ".cfg"}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"


class AuditInputError(ValueError):
	"""Raised when a required audit input cannot be interpreted."""


def _sha256(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


def _file_sha256(path: Path) -> str:
	return _sha256(path.read_bytes())


def _without_hash_comments(text: str) -> str:
	"""Remove GDScript hash comments while preserving strings and line count."""
	result: list[str] = []
	quote = ""
	escaped = False
	comment = False
	for char in text:
		if comment:
			if char == "\n":
				comment = False
				result.append(char)
			else:
				result.append(" ")
			continue
		if quote:
			result.append(char)
			if escaped:
				escaped = False
			elif char == "\\":
				escaped = True
			elif char == quote:
				quote = ""
			continue
		if char in {'"', "'"}:
			quote = char
			result.append(char)
		elif char == "#":
			comment = True
			result.append(" ")
		else:
			result.append(char)
	return "".join(result)


def _contains_quoted_value(text: str, needle: str) -> bool:
	"""Return whether a non-comment string literal contains ``needle``."""
	clean = _without_hash_comments(text)
	quote = ""
	escaped = False
	value: list[str] = []
	for char in clean:
		if not quote:
			if char in {'"', "'"}:
				quote = char
				value = []
			continue
		if escaped:
			value.append(char)
			escaped = False
		elif char == "\\":
			escaped = True
		elif char == quote:
			if needle in "".join(value):
				return True
			quote = ""
		else:
			value.append(char)
	return False


def _repo_path(root: Path, value: object, label: str) -> tuple[Path, str]:
	text = str(value).replace("\\", "/")
	if not text or text.startswith("/") or re.match(r"^[A-Za-z]:/", text):
		raise AuditInputError(f"{label} must be a repository-relative path")
	normalized = Path(text)
	if any(part == ".." for part in normalized.parts):
		raise AuditInputError(f"{label} may not escape the repository")
	resolved = (root / normalized).resolve()
	try:
		resolved.relative_to(root.resolve())
	except ValueError as exc:
		raise AuditInputError(
			f"{label} may not escape the repository") from exc
	return resolved, normalized.as_posix()


def _split_top_level(text: str, separator: str = ",") -> list[str]:
	"""Split a GDScript literal without splitting nested values or strings."""
	parts: list[str] = []
	start = 0
	stack: list[str] = []
	quote = ""
	escaped = False
	comment = False
	pairs = {"(": ")", "[": "]", "{": "}"}
	for index, char in enumerate(text):
		if comment:
			if char == "\n":
				comment = False
			continue
		if quote:
			if escaped:
				escaped = False
			elif char == "\\":
				escaped = True
			elif char == quote:
				quote = ""
			continue
		if char in {'"', "'"}:
			quote = char
			continue
		if char == "#":
			comment = True
			continue
		if char in pairs:
			stack.append(pairs[char])
			continue
		if char in ")]}" and (not stack or stack.pop() != char):
			raise AuditInputError("unbalanced GDScript literal")
		if char == separator and not stack:
			parts.append(text[start:index].strip())
			start = index + 1
	if quote or stack:
		raise AuditInputError("unterminated GDScript literal")
	parts.append(text[start:].strip())
	return [part for part in parts if part]


def _top_level_colon(text: str) -> int:
	stack: list[str] = []
	quote = ""
	escaped = False
	pairs = {"(": ")", "[": "]", "{": "}"}
	for index, char in enumerate(text):
		if quote:
			if escaped:
				escaped = False
			elif char == "\\":
				escaped = True
			elif char == quote:
				quote = ""
			continue
		if char in {'"', "'"}:
			quote = char
		elif char in pairs:
			stack.append(pairs[char])
		elif char in ")]}":
			if not stack or stack.pop() != char:
				raise AuditInputError("unbalanced GDScript dictionary")
		elif char == ":" and not stack:
			return index
	raise AuditInputError("GDScript dictionary entry lacks ':'")


def _quoted_key(text: str, label: str) -> str:
	match = re.fullmatch(r'\s*"([^"\\]+)"\s*', text)
	if match is None:
		raise AuditInputError(f"{label} must be a quoted string")
	return match.group(1)


def _dictionary(text: str, label: str) -> dict[str, str]:
	value = text.strip()
	if not value.startswith("{") or not value.endswith("}"):
		raise AuditInputError(f"{label} must be a dictionary literal")
	result: dict[str, str] = {}
	for entry in _split_top_level(value[1:-1]):
		colon = _top_level_colon(entry)
		key = _quoted_key(entry[:colon], f"{label} key")
		if key in result:
			raise AuditInputError(f"{label} repeats key {key!r}")
		result[key] = entry[colon + 1:].strip()
	return result


def _extract_layout_literal(text: str) -> str:
	match = re.search(r"\bconst\s+ROOM_LAYOUTS\s*:=\s*\{", text)
	if match is None:
		raise AuditInputError("runtime layout lacks const ROOM_LAYOUTS")
	start = match.end() - 1
	stack: list[str] = []
	quote = ""
	escaped = False
	comment = False
	for index in range(start, len(text)):
		char = text[index]
		if comment:
			if char == "\n":
				comment = False
			continue
		if quote:
			if escaped:
				escaped = False
			elif char == "\\":
				escaped = True
			elif char == quote:
				quote = ""
			continue
		if char in {'"', "'"}:
			quote = char
		elif char == "#":
			comment = True
		elif char == "{":
			stack.append("}")
		elif char == "}":
			if not stack or stack.pop() != "}":
				raise AuditInputError("ROOM_LAYOUTS has unbalanced braces")
			if not stack:
				return text[start:index + 1]
	raise AuditInputError("ROOM_LAYOUTS dictionary is unterminated")


def _array(text: str, label: str) -> list[str]:
	value = text.strip()
	if not value.startswith("[") or not value.endswith("]"):
		raise AuditInputError(f"{label} must be an array literal")
	return _split_top_level(value[1:-1])


def _parse_position(text: str, label: str) -> tuple[float, float]:
	match = re.fullmatch(
		rf"\s*Vector2\s*\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)\s*",
		text)
	if match is None:
		raise AuditInputError(f"{label} must use a numeric Vector2")
	values = (float(match.group(1)), float(match.group(2)))
	if not all(math.isfinite(value) for value in values):
		raise AuditInputError(f"{label} contains a non-finite coordinate")
	return values


def parse_runtime_cards(text: str) -> tuple[list[dict[str, Any]], dict[str, int]]:
	"""Return active static ROOM_LAYOUTS cards and per-room mid counts."""
	text = _without_hash_comments(text)
	layout = _dictionary(_extract_layout_literal(text), "ROOM_LAYOUTS")
	cards: list[dict[str, Any]] = []
	mid_counts: dict[str, int] = {}
	for room, room_text in layout.items():
		room_data = _dictionary(room_text, f"ROOM_LAYOUTS.{room}")
		for layer in ("mid", "front"):
			if layer not in room_data:
				raise AuditInputError(
					f"ROOM_LAYOUTS.{room} lacks the {layer!r} layer")
			entries = _array(
				room_data[layer], f"ROOM_LAYOUTS.{room}.{layer}")
			if layer == "mid":
				mid_counts[room] = len(entries)
			for index, entry in enumerate(entries):
				label = f"ROOM_LAYOUTS.{room}.{layer}[{index}]"
				card = _dictionary(entry, label)
				if "tex" not in card or "pos" not in card:
					raise AuditInputError(f"{label} lacks tex or pos")
				texture = _quoted_key(card["tex"], f"{label}.tex")
				if "/" in texture or "\\" in texture or texture in {".", ".."}:
					raise AuditInputError(
						f"{label}.tex must be a room-card basename")
				path = f"{ROOM_CARD_ROOT}/{texture}"
				prefix = f"room_{room}_"
				if not texture.startswith(prefix) or not texture.endswith(".png"):
					raise AuditInputError(
						f"{label}.tex does not identify a {room} PNG")
				cards.append({
					"room": room,
					"id": texture[len(prefix):-4],
					"layer": layer,
					"path": path,
					"position": _parse_position(card["pos"], f"{label}.pos"),
				})
	return cards, mid_counts


def _normalized_layer(value: object, label: str) -> str:
	layer = str(value)
	aliases = {
		"front": "front",
		"foreground": "front",
		"mid": "mid",
		"midground": "mid",
	}
	if layer not in aliases:
		raise AuditInputError(
			f"{label} must be front/foreground or mid/midground")
	return aliases[layer]


def _manifest_position(value: object, label: str) -> tuple[float, float]:
	if not isinstance(value, list) or len(value) != 2:
		raise AuditInputError(f"{label} must be a two-number array")
	try:
		position = (float(value[0]), float(value[1]))
	except (TypeError, ValueError) as exc:
		raise AuditInputError(f"{label} must be a two-number array") from exc
	if not all(math.isfinite(item) for item in position):
		raise AuditInputError(f"{label} contains a non-finite coordinate")
	return position


def _identity(card: dict[str, Any]) -> tuple[object, ...]:
	return (
		card["room"], card["id"], card["layer"], card["path"],
		float(card["position"][0]), float(card["position"][1]))


def _shape_box(shape: dict[str, Any], label: str) -> tuple[float, float, float, float]:
	value = shape.get("box", shape.get("bbox", shape.get("rect")))
	if not isinstance(value, list) or len(value) != 4:
		raise AuditInputError(f"{label} requires box/bbox/rect [x0,y0,x1,y1]")
	try:
		box = tuple(float(item) for item in value)
	except (TypeError, ValueError) as exc:
		raise AuditInputError(f"{label} has a non-numeric box") from exc
	if not all(math.isfinite(item) for item in box):
		raise AuditInputError(f"{label} has a non-finite box")
	if box[2] < box[0] or box[3] < box[1]:
		raise AuditInputError(f"{label} has an inverted box")
	return box  # type: ignore[return-value]


def rasterize_keep_shapes(
		shapes: object, size: tuple[int, int], label: str) -> Image.Image:
	"""Rasterize the refiner's crop-local approved subject shapes."""
	if not isinstance(shapes, list):
		raise AuditInputError(f"{label} must be an array")
	mask = Image.new("L", size, 0)
	draw = ImageDraw.Draw(mask)
	for index, raw_shape in enumerate(shapes):
		shape_label = f"{label}[{index}]"
		if not isinstance(raw_shape, dict):
			raise AuditInputError(f"{shape_label} must be an object")
		kind = str(raw_shape.get("type", ""))
		if kind == "polygon":
			points = raw_shape.get("points")
			if not isinstance(points, list) or len(points) < 3:
				raise AuditInputError(
					f"{shape_label}.points requires at least three points")
			parsed: list[tuple[float, float]] = []
			for point in points:
				if not isinstance(point, list) or len(point) != 2:
					raise AuditInputError(
						f"{shape_label}.points must contain [x,y] pairs")
				try:
					pair = (float(point[0]), float(point[1]))
				except (TypeError, ValueError) as exc:
					raise AuditInputError(
						f"{shape_label}.points contains non-numeric data") from exc
				if not all(math.isfinite(value) for value in pair):
					raise AuditInputError(
						f"{shape_label}.points contains non-finite data")
				parsed.append(pair)
			draw.polygon(parsed, fill=255)
		elif kind == "ellipse":
			draw.ellipse(_shape_box(raw_shape, shape_label), fill=255)
		elif kind == "rounded_rectangle":
			try:
				radius = float(raw_shape.get("radius", 0.0))
			except (TypeError, ValueError) as exc:
				raise AuditInputError(
					f"{shape_label}.radius must be numeric") from exc
			if not math.isfinite(radius) or radius < 0.0:
				raise AuditInputError(
					f"{shape_label}.radius must be finite and non-negative")
			draw.rounded_rectangle(
				_shape_box(raw_shape, shape_label), radius=radius, fill=255)
		else:
			raise AuditInputError(
				f"{shape_label} has unsupported type {kind!r}")
	return mask


def _metric(record: object, key: str, label: str) -> int:
	if not isinstance(record, dict) or isinstance(record.get(key), bool):
		raise AuditInputError(f"{label}.{key} must be a non-negative integer")
	value = record.get(key)
	if not isinstance(value, int) or value < 0:
		raise AuditInputError(f"{label}.{key} must be a non-negative integer")
	return value


def _declared_sha(record: dict[str, Any], key: str, label: str) -> str:
	value = str(record.get(key, ""))
	if HEX_SHA256.fullmatch(value) is None:
		raise AuditInputError(f"{label}.{key} must be a lowercase SHA-256")
	return value


def _runtime_references(root: Path) -> list[str]:
	paths: set[Path] = set()
	for relative in RUNTIME_SCAN_ROOTS:
		base = root / relative
		if not base.is_dir():
			continue
		for path in base.rglob("*"):
			if path.is_file() and path.suffix.lower() in RUNTIME_TEXT_SUFFIXES:
				paths.add(path)
	project = root / "project.godot"
	if project.is_file():
		paths.add(project)
	references: list[str] = []
	for path in sorted(paths):
		try:
			text = path.read_text(encoding="utf-8")
		except (OSError, UnicodeDecodeError):
			continue
		if _contains_quoted_value(text, POOL_MID_BASENAME):
			references.append(path.relative_to(root).as_posix())
	return references


def audit_repository(
		root: Path = ROOT, manifest_path: Path | None = None
		) -> tuple[dict[str, Any], list[str]]:
	"""Audit the repository and return a deterministic summary and errors."""
	root = root.resolve()
	if manifest_path is None:
		manifest_path = root / DEFAULT_MANIFEST
	elif not manifest_path.is_absolute():
		manifest_path = root / manifest_path
	errors: list[str] = []
	summary: dict[str, Any] = {
		"manifest": manifest_path.relative_to(root).as_posix()
			if manifest_path.is_relative_to(root) else str(manifest_path),
		"runtime_layout": EXPECTED_LAYOUT,
		"active_cards": 0,
		"verified_cards": 0,
		"retired_cards": 0,
		"runtime_pool_mid_references": [],
	}

	try:
		manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		return summary, [f"cannot load provenance manifest: {exc}"]
	if not isinstance(manifest, dict):
		return summary, ["provenance manifest must contain a JSON object"]
	if manifest.get("schema_version") != 1:
		errors.append("provenance schema_version must equal 1")
	if manifest.get("alpha_scissor_threshold") != 128:
		errors.append("provenance alpha_scissor_threshold must equal 128")
	if manifest.get("runtime_layout_path") != EXPECTED_LAYOUT:
		errors.append(
			f"runtime_layout_path must equal {EXPECTED_LAYOUT!r}")
	layout_path = root / EXPECTED_LAYOUT
	try:
		layout_text = layout_path.read_text(encoding="utf-8")
		runtime_cards, mid_counts = parse_runtime_cards(layout_text)
	except (OSError, UnicodeDecodeError, AuditInputError) as exc:
		return summary, sorted(errors + [f"cannot parse runtime layout: {exc}"])
	summary["active_cards"] = len(runtime_cards)
	if mid_counts.get("mermaid_pool", -1) != 0:
		errors.append("ROOM_LAYOUTS.mermaid_pool.mid must be empty")

	references = _runtime_references(root)
	summary["runtime_pool_mid_references"] = references
	for path in references:
		errors.append(
			f"retired {POOL_MID_BASENAME} remains referenced by {path}")

	declared_cards = manifest.get("cards")
	if not isinstance(declared_cards, list):
		return summary, sorted(errors + ["provenance cards must be an array"])
	manifest_cards: list[dict[str, Any]] = []
	seen_identities: set[tuple[object, ...]] = set()
	for index, record in enumerate(declared_cards):
		label = f"cards[{index}]"
		if not isinstance(record, dict):
			errors.append(f"{label} must be an object")
			continue
		try:
			path, relative = _repo_path(root, record.get("path"), f"{label}.path")
			room = str(record.get("room", ""))
			card_id = str(record.get("id", ""))
			layer = _normalized_layer(record.get("role"), f"{label}.role")
			position = _manifest_position(
				record.get("position"), f"{label}.position")
			expected_name = f"room_{room}_{card_id}.png"
			if path.name != expected_name or relative != f"{ROOM_CARD_ROOT}/{expected_name}":
				raise AuditInputError(
					f"{label} room/id/path do not identify the same room card")
			normalized = {
				"room": room,
				"id": card_id,
				"layer": layer,
				"path": relative,
				"position": position,
			}
			identity = _identity(normalized)
			if identity in seen_identities:
				raise AuditInputError(f"{label} duplicates an active card declaration")
			seen_identities.add(identity)
			manifest_cards.append(normalized)
		except AuditInputError as exc:
			errors.append(str(exc))
			continue

		try:
			if not path.is_file():
				raise AuditInputError(f"{label}.path does not exist: {relative}")
			output_hash = _file_sha256(path)
			if output_hash != _declared_sha(record, "output_sha256", label):
				errors.append(f"{label} output_sha256 does not match {relative}")
			_declared_sha(record, "source_sha256", label)
			with Image.open(path) as source:
				image = source.convert("RGBA")
			pixels = np.asarray(image, dtype=np.uint8)
			alpha = pixels[:, :, 3]
			core = (alpha >= 128).astype(np.uint8) * 255
			alpha_pixels = int(np.count_nonzero(alpha))
			core_pixels = int(np.count_nonzero(core))
			hidden_rgb = int(np.count_nonzero(
				(alpha == 0) & np.any(pixels[:, :, :3] != 0, axis=2)))
			if hidden_rgb:
				errors.append(
					f"{label} {relative} has {hidden_rgb} RGB pixels under alpha==0")
			if _sha256(alpha.tobytes()) != _declared_sha(
					record, "alpha_sha256", label):
				errors.append(f"{label} alpha_sha256 does not match decoded alpha")
			if _sha256(core.tobytes()) != _declared_sha(
					record, "core_mask_sha256", label):
				errors.append(
					f"{label} core_mask_sha256 does not match alpha>=128")
			allowed = np.asarray(rasterize_keep_shapes(
				record.get("keep_shapes"), image.size,
				f"{label}.keep_shapes"), dtype=np.uint8) > 0
			outside = int(np.count_nonzero((core > 0) & ~allowed))
			if outside:
				errors.append(
					f"{label} has {outside} alpha>=128 pixels outside keep_shapes")
			for phase in ("before", "after"):
				for key in ("alpha_pixels", "core_pixels", "hidden_rgb_pixels"):
					_metric(record.get(phase), key, f"{label}.{phase}")
			after = record["after"]
			actual_metrics = {
				"alpha_pixels": alpha_pixels,
				"core_pixels": core_pixels,
				"hidden_rgb_pixels": hidden_rgb,
			}
			for key, actual in actual_metrics.items():
				if after[key] != actual:
					errors.append(
						f"{label}.after.{key} is {after[key]}, decoded value is {actual}")
			if not str(record.get("method", "")).strip():
				errors.append(f"{label}.method must describe the refinement")
			summary["verified_cards"] += 1
		except (AuditInputError, OSError, ValueError) as exc:
			errors.append(str(exc))

	runtime_by_identity = {_identity(card): card for card in runtime_cards}
	manifest_by_identity = {_identity(card): card for card in manifest_cards}
	for identity in sorted(set(runtime_by_identity) - set(manifest_by_identity)):
		card = runtime_by_identity[identity]
		errors.append(
			"active runtime card lacks matching provenance: "
			f"{card['room']}:{card['id']} {card['layer']} "
			f"{card['path']} at {list(card['position'])}")
	for identity in sorted(set(manifest_by_identity) - set(runtime_by_identity)):
		card = manifest_by_identity[identity]
		errors.append(
			"provenance card is not active at its declared placement: "
			f"{card['room']}:{card['id']} {card['layer']} "
			f"{card['path']} at {list(card['position'])}")
	if len(runtime_by_identity) != len(runtime_cards):
		errors.append("ROOM_LAYOUTS repeats an active static card declaration")

	retired = manifest.get("retired_cards")
	if not isinstance(retired, list):
		errors.append("provenance retired_cards must be an array")
		retired = []
	summary["retired_cards"] = len(retired)
	pool_retired = []
	for index, record in enumerate(retired):
		if not isinstance(record, dict):
			errors.append(f"retired_cards[{index}] must be an object")
			continue
		if (
				str(record.get("room", "")) == "mermaid_pool"
				and str(record.get("id", "")) == "mid_pool"
				and str(record.get("path", "")).replace("\\", "/") == POOL_MID_PATH):
			pool_retired.append(record)
	if len(pool_retired) != 1:
		errors.append(
			"retired_cards must contain exactly one mermaid_pool:mid_pool record")
	elif not str(pool_retired[0].get("reason", "")).strip():
		errors.append("retired mermaid_pool:mid_pool record requires a reason")
	if any(card["path"] == POOL_MID_PATH for card in manifest_cards):
		errors.append("retired mermaid_pool:mid_pool may not remain in active cards")

	return summary, sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(
		description="audit active Castle static depth-card alpha ownership")
	parser.add_argument(
		"--root", type=Path, default=ROOT,
		help="repository root (defaults to the tool's repository)")
	parser.add_argument(
		"--manifest", type=Path,
		help=f"provenance manifest (default: {DEFAULT_MANIFEST})")
	args = parser.parse_args(argv)
	summary, errors = audit_repository(args.root, args.manifest)
	summary["ok"] = not errors
	summary["error_count"] = len(errors)
	print(json.dumps(summary, indent=2, sort_keys=True))
	for error in errors:
		print(f"FAIL: {error}")
	return 1 if errors else 0


if __name__ == "__main__":
	sys.exit(main())
