#!/usr/bin/env python3
"""Stress-test the isolated full-regeneration model and texture pack."""

from __future__ import annotations

import csv
import hashlib
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets" / "full_texture_regen_2026-07-18"
MODEL_MANIFEST = PACK / "model_manifest.json"
TARGET_LEDGER = ROOT / "audit" / "full_regen_2026-07-18" / "target_ledger.csv"
OUT_DIR = ROOT / "audit" / "full_regen_2026-07-18"
MODEL_RESULTS = OUT_DIR / "model_stress_results.csv"
TEXTURE_RESULTS = OUT_DIR / "texture_stress_results.csv"
SUMMARY = OUT_DIR / "stress_summary.json"
PROVENANCE = OUT_DIR / "generated_provenance_integrity.csv"


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def read_glb_json(path: Path) -> dict[str, Any]:
	data = path.read_bytes()
	if len(data) < 20 or data[:4] != b"glTF":
		raise ValueError("invalid GLB magic or truncated header")
	version, total_length = struct.unpack_from("<II", data, 4)
	if version != 2 or total_length != len(data):
		raise ValueError(f"invalid GLB header version={version} length={total_length}/{len(data)}")
	chunk_length, chunk_type = struct.unpack_from("<II", data, 12)
	if chunk_type != 0x4E4F534A:
		raise ValueError("first GLB chunk is not JSON")
	return json.loads(data[20:20 + chunk_length].decode("utf-8").rstrip(" \t\r\n\x00"))


def normalized_components(entry: dict[str, Any]) -> list[str]:
	return [str(name).split(".", 1)[0].lower() for name in entry.get("components", [])]


def count_prefix(components: list[str], prefix: str) -> int:
	return sum(name.startswith(prefix) for name in components)


def anatomy_failures(entry: dict[str, Any]) -> list[str]:
	kind = str(entry["kind"])
	components = normalized_components(entry)
	failures: list[str] = []
	if kind in {"butterfly", "butterfly_gate"}:
		if not all(name in components for name in ("front_wing_left", "front_wing_right")):
			failures.append("butterfly_requires_two_front_wings")
		if not all(name in components for name in ("rear_wing_left", "rear_wing_right")):
			failures.append("butterfly_requires_two_rear_wings")
		if count_prefix(components, "antenna_") != 2:
			failures.append("butterfly_requires_two_antennae")
		for required in ("body", "thorax", "head"):
			if required not in components:
				failures.append(f"butterfly_missing_{required}")
	if kind == "octopus":
		if count_prefix(components, "arm_") != 8:
			failures.append("octopus_requires_eight_arms")
		for required in ("octopus_mantle", "octopus_head"):
			if required not in components:
				failures.append(f"octopus_missing_{required}")
	if kind == "shrimp":
		if count_prefix(components, "abdomen_segment_") != 7:
			failures.append("shrimp_requires_seven_abdomen_segments")
		if count_prefix(components, "leg_") < 10:
			failures.append("shrimp_requires_ten_readable_legs")
		if count_prefix(components, "antenna_") < 4:
			failures.append("shrimp_requires_four_antennae")
		if count_prefix(components, "tail_fan_") != 2:
			failures.append("shrimp_requires_two_tail_fans")
	if kind == "jellyfish":
		if count_prefix(components, "oral_arm_") != 4:
			failures.append("jellyfish_requires_four_oral_arms")
		if count_prefix(components, "tentacle_") != 8:
			failures.append("jellyfish_requires_eight_tentacles")
		for required in ("bell", "bell_rim"):
			if required not in components:
				failures.append(f"jellyfish_missing_{required}")
	if kind == "dragon_turtle":
		if count_prefix(components, "flipper_") != 4:
			failures.append("dragon_turtle_requires_four_flippers")
		for required in ("shell", "dragon_head", "tail"):
			if required not in components:
				failures.append(f"dragon_turtle_missing_{required}")
	if kind == "clownfish":
		if count_prefix(components, "pectoral_fin_") != 2:
			failures.append("fish_requires_two_pectoral_fins")
		if count_prefix(components, "tail_") != 2:
			failures.append("fish_requires_complete_tail")
	return failures


def stress_models() -> tuple[list[dict[str, str]], dict[str, Any]]:
	manifest = json.loads(MODEL_MANIFEST.read_text(encoding="utf-8"))
	rows: list[dict[str, str]] = []
	hashes_by_role: dict[str, list[str]] = defaultdict(list)
	for entry in manifest["assets"]:
		path = ROOT / entry["path"]
		failures: list[str] = []
		if not path.exists():
			failures.append("missing_file")
			glb: dict[str, Any] = {}
			file_hash = ""
		else:
			file_hash = sha256(path)
			try:
				glb = read_glb_json(path)
			except (OSError, ValueError, json.JSONDecodeError) as error:
				glb = {}
				failures.append(f"glb_parse:{error}")
		if path.exists() and path.stat().st_size > 2 * 1024 * 1024:
			failures.append("file_over_2mib")
		triangles = int(entry["triangles"])
		materials = int(entry["materials"])
		if triangles < 100:
			failures.append("too_trivial_under_100_triangles")
		if triangles > 12000:
			failures.append("over_mobile_hero_budget")
		if materials < 2:
			failures.append("one_note_single_material")
		if materials > 12:
			failures.append("over_12_material_slots")
		if glb.get("images") or glb.get("textures"):
			failures.append("embedded_texture_in_flat_material_pack")
		for index, material in enumerate(glb.get("materials", [])):
			pbr = material.get("pbrMetallicRoughness", {})
			if float(pbr.get("metallicFactor", 0.0)) > 0.05:
				failures.append(f"material_{index}_metallic")
			roughness = float(pbr.get("roughnessFactor", 1.0))
			if roughness < 0.62 or roughness > 0.95:
				failures.append(f"material_{index}_roughness_{roughness:.2f}")
			color = pbr.get("baseColorFactor", [1.0, 1.0, 1.0, 1.0])
			if min(float(value) for value in color[:3]) > 0.985:
				failures.append(f"material_{index}_pure_white")
		lo = [float(value) for value in entry["bounds_min"]]
		hi = [float(value) for value in entry["bounds_max"]]
		dimensions = [max(0.0, hi[index] - lo[index]) for index in range(3)]
		if max(dimensions) <= 0.01:
			failures.append("zero_bounds")
		nonzero = [value for value in dimensions if value > 0.01]
		if nonzero and max(nonzero) / min(nonzero) > 40 and entry["kind"] not in {"rainbow_route"}:
			failures.append("extreme_dimension_ratio")
		failures.extend(anatomy_failures(entry))
		hashes_by_role[str(entry["role_id"])].append(file_hash)
		rows.append(
			{
				"name": str(entry["name"]),
				"role_id": str(entry["role_id"]),
				"path": str(entry["path"]),
				"triangles": str(triangles),
				"vertices": str(entry["vertices"]),
				"materials": str(materials),
				"bytes": str(path.stat().st_size if path.exists() else 0),
				"sha256": file_hash,
				"status": "pass" if not failures else "reject",
				"failures": ";".join(failures),
			}
		)

	duplicate_roles: dict[str, int] = {}
	for role_id, hashes in hashes_by_role.items():
		if len(hashes) > 1 and len(set(hashes)) != len(hashes):
			duplicate_roles[role_id] = len(hashes) - len(set(hashes))
			for row in rows:
				if row["role_id"] == role_id:
					row["status"] = "reject"
					row["failures"] = (row["failures"] + ";" if row["failures"] else "") + "duplicate_family_binary"

	with MODEL_RESULTS.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
		writer.writeheader()
		writer.writerows(rows)
	passed = sum(row["status"] == "pass" for row in rows)
	return rows, {
		"asset_count": len(rows),
		"pass_count": passed,
		"reject_count": len(rows) - passed,
		"duplicate_roles": duplicate_roles,
		"total_bytes": sum(int(row["bytes"]) for row in rows),
		"max_triangles": max(int(row["triangles"]) for row in rows),
	}


def stress_textures() -> tuple[list[dict[str, str]], dict[str, Any]]:
	texture_dir = PACK / "textures"
	paths = sorted(path for path in texture_dir.glob("**/*") if path.is_file()) if texture_dir.exists() else []
	rows: list[dict[str, str]] = []
	for path in paths:
		failures: list[str] = []
		width = height = 0
		mode = ""
		entropy = 0.0
		transparent_ratio = 0.0
		partial_ratio = 0.0
		opaque_ratio = 1.0
		edge_error = 0.0
		try:
			with Image.open(path) as image:
				image.load()
				width, height = image.size
				mode = image.mode
				entropy = sum(ImageStat.Stat(image.convert("RGB").resize((64, 64))).var) / 3.0
				if max(width, height) > 1024 and not (
					width > 0 and height > 0 and width & (width - 1) == 0 and height & (height - 1) == 0
				):
					failures.append("texture_dimension_rule")
				if entropy < 12.0:
					failures.append("near_blank_texture")
				if "A" in image.getbands():
					alpha = image.getchannel("A")
					histogram = alpha.histogram()
					pixels = float(width * height)
					transparent_ratio = sum(histogram[:9]) / pixels
					partial_ratio = sum(histogram[9:247]) / pixels
					opaque_ratio = sum(histogram[247:]) / pixels
					if transparent_ratio < 0.08:
						failures.append("isolated_sprite_missing_transparency")
					if opaque_ratio < 0.08:
						failures.append("isolated_sprite_too_transparent")
					if partial_ratio > 0.12:
						failures.append("isolated_sprite_excess_soft_alpha")
				role = path.stem.split("__", 1)[0].upper()
				if role in {
					"R007_REEF_CAUSTIC_GROUND_TREATMENT",
					"R032_CASTLE_KITCHEN_COUNTER_TEXTURE",
					"R033_CASTLE_KITCHEN_FLOOR_TEXTURE",
					"R034_CASTLE_KITCHEN_WOOD_TEXTURE",
					"R044_BUTTERFLY_WORLD_PLANET_SURFACE",
					"R050_DUNGEON_ARENA_FLOOR",
					"R008_REEF_BACKDROP_SEAMOUNTS",
				}:
					rgb = image.convert("RGB")
					left = [rgb.getpixel((0, y)) for y in range(height)]
					right = [rgb.getpixel((width - 1, y)) for y in range(height)]
					edge_error = sum(abs(a - b) for x, y in zip(left, right) for a, b in zip(x, y)) / float(height * 3)
					if edge_error > 1.0:
						failures.append("horizontal_tile_edge_mismatch")
		except (OSError, ValueError) as error:
			failures.append(f"image_parse:{error}")
		rows.append(
			{
				"path": path.relative_to(ROOT).as_posix(),
				"width": str(width),
				"height": str(height),
				"mode": mode,
				"variance": f"{entropy:.2f}",
				"transparent_ratio": f"{transparent_ratio:.4f}",
				"partial_ratio": f"{partial_ratio:.4f}",
				"opaque_ratio": f"{opaque_ratio:.4f}",
				"edge_error": f"{edge_error:.2f}",
				"bytes": str(path.stat().st_size),
				"sha256": sha256(path),
				"status": "pass" if not failures else "reject",
				"failures": ";".join(failures),
			}
		)
	with TEXTURE_RESULTS.open("w", newline="", encoding="utf-8") as handle:
		fieldnames = ["path", "width", "height", "mode", "variance", "transparent_ratio", "partial_ratio", "opaque_ratio", "edge_error", "bytes", "sha256", "status", "failures"]
		writer = csv.DictWriter(handle, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)
	passed = sum(row["status"] == "pass" for row in rows)
	return rows, {"asset_count": len(rows), "pass_count": passed, "reject_count": len(rows) - passed}


def scan_provenance() -> dict[str, int]:
	paths = sorted(path for path in (ROOT / "gen2").glob("**/*") if path.is_file() and path.suffix.lower() in {
		".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tga"
	})
	rows: list[dict[str, str]] = []
	for path in paths:
		failure = ""
		width = height = 0
		try:
			with Image.open(path) as image:
				image.verify()
				width, height = image.size
		except (OSError, ValueError) as error:
			failure = str(error)
		rows.append({
			"path": path.relative_to(ROOT).as_posix(),
			"width": str(width),
			"height": str(height),
			"sha256": sha256(path),
			"status": "valid" if not failure else "quarantine",
			"failure": failure,
		})
	with PROVENANCE.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["path", "width", "height", "sha256", "status", "failure"])
		writer.writeheader()
		writer.writerows(rows)
	return dict(Counter(row["status"] for row in rows))


def role_coverage(model_rows: list[dict[str, str]], texture_rows: list[dict[str, str]]) -> dict[str, Any]:
	with TARGET_LEDGER.open(newline="", encoding="utf-8") as handle:
		targets = list(csv.DictReader(handle))
	model_roles = {row["role_id"].lower() for row in model_rows if row["status"] == "pass"}
	texture_roles = {
		Path(row["path"]).stem.split("__", 1)[0].lower()
		for row in texture_rows if row["status"] == "pass" and "__" in Path(row["path"]).stem
	}
	pending: list[str] = []
	covered: list[str] = []
	for target in targets:
		if not target["disposition"].startswith("regenerate_"):
			continue
		role_id = target["role_id"]
		normalized_role_id = role_id.lower()
		kind = target["target_kind"]
		if kind in {"modeled_3d", "composition_kit"} and normalized_role_id in model_roles:
			covered.append(role_id)
		elif kind == "painted_2d" and normalized_role_id in texture_roles:
			covered.append(role_id)
		elif kind == "pipeline_repair":
			covered.append(role_id)
		else:
			pending.append(role_id)
	return {"covered_count": len(covered), "pending_count": len(pending), "pending_roles": pending}


def main() -> None:
	OUT_DIR.mkdir(parents=True, exist_ok=True)
	model_rows, model_summary = stress_models()
	texture_rows, texture_summary = stress_textures()
	provenance_summary = scan_provenance()
	coverage = role_coverage(model_rows, texture_rows)
	summary = {
		"models": model_summary,
		"textures": texture_summary,
		"provenance": provenance_summary,
		"role_coverage": coverage,
		"structural_status": "pass" if model_summary["reject_count"] == 0 and texture_summary["reject_count"] == 0 else "reject",
		"visual_status": "pending_mobile_stress",
		"owner_5_status": "pending_owner_acceptance",
	}
	SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(summary, indent=2))
	if summary["structural_status"] != "pass":
		raise SystemExit(1)


if __name__ == "__main__":
	main()
