#!/usr/bin/env python3
"""Audit the fixed-view 2.5D Sprite3D contract.

This is deliberately a migration/no-regression audit.  The project contains
older Canvas/Node2D rooms, so legacy findings are reported and compared with
the checked-in inventory instead of making the first migration build unusable.
New runtime 2.5D work is held to the strict contract in the manifest.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
from pathlib import Path


DEFAULT_MANIFEST = Path("tools/manifests/fixed_view_25d_manifest.json")
SCAN_SUFFIXES = {".gd", ".tscn", ".tres", ".res", ".godot"}
SKIP_PARTS = {".git", ".godot", "attic", "archive", "disabled_addons"}

FORBIDDEN_PATTERNS = {
	"model_resource": re.compile(r"(?i)(\.glb|\.gltf|MeshInstance3D|CSG|Skeleton3D|骨格)"),
	# Camera mutation is evaluated only by the declared authority group's
	# runtime-pattern checks; generic `.size =` is common UI code.
	"spatial_physics": re.compile(r"(?i)(CharacterBody3D|RigidBody3D|StaticBody3D|Area3D|CollisionShape3D|Jolt|PhysicsServer3D)"),
}
WORLD_2D_PATTERNS = {
	"sprite2d_world": re.compile(r"(?i)(Sprite2D|AnimatedSprite2D|TextureRect|TileMapLayer|GPUParticles2D)"),
	"camera2d_world": re.compile(r"(?i)Camera2D"),
}


def load_manifest(root: Path, path: Path) -> dict:
	manifest_path = path if path.is_absolute() else root / path
	try:
		return json.loads(manifest_path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		print(f"25D|FAIL|manifest|{manifest_path}|{exc}")
		return {}


def production_files(root: Path) -> list[Path]:
	files: list[Path] = []
	for base in (root / "scripts", root / "scenes", root / "addons"):
		if not base.exists():
			continue
		for path in base.rglob("*"):
			if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
				continue
			if any(part in SKIP_PARTS for part in path.parts):
				continue
			files.append(path)
	return sorted(files)


def relative(path: Path, root: Path) -> str:
	return path.relative_to(root).as_posix()


def is_allowed(path: str, patterns: list[str]) -> bool:
	return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def path_hash(paths: list[str]) -> str:
	return hashlib.sha256("\n".join(sorted(paths)).encode("utf-8")).hexdigest()


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--root", type=Path, default=Path.cwd())
	parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
	args = parser.parse_args()
	root = args.root.resolve()
	manifest = load_manifest(root, args.manifest)
	if not manifest:
		return 1

	legacy_patterns = manifest.get("legacy_2d_paths", [])
	strict_patterns = manifest.get("strict_25d_paths", [])
	legacy: dict[str, list[str]] = {}
	hard_failures: list[str] = []
	files = production_files(root)

	strict_files = {rel for rel in (relative(path, root) for path in files) if is_allowed(rel, strict_patterns)}
	for path in files:
		rel = relative(path, root)
		try:
			text = path.read_text(encoding="utf-8", errors="replace")
		except OSError as exc:
			hard_failures.append(f"read:{rel}:{exc}")
			continue

		for rule, pattern in FORBIDDEN_PATTERNS.items():
			if pattern.search(text):
				legacy.setdefault(rule, []).append(rel)
				# Camera mutation is a strict-stage failure only when the file is a
				# declared camera authority. Existing legacy stages are inventory.
				if rel in strict_files:
					hard_failures.append(f"{rule}_in_strict_stage:{rel}")

		for rule, pattern in WORLD_2D_PATTERNS.items():
			if pattern.search(text):
				legacy.setdefault(rule, []).append(rel)

		if rel in strict_files:
			for rule in ("model_resource", "spatial_physics"):
				if rule in legacy and rel in legacy[rule]:
					hard_failures.append(f"{rule}_in_strict_stage:{rel}")

	strict_text = "\n".join(
		path.read_text(encoding="utf-8", errors="replace")
		for path in files
		if relative(path, root) in strict_files
	)
	for group in manifest.get("strict_authority_groups", []):
		group_paths = group.get("paths", [])
		group_text = "\n".join(
			path.read_text(encoding="utf-8", errors="replace")
			for path in files
			if is_allowed(relative(path, root), group_paths)
		)
		for token in group.get("required_constructors", []):
			if token not in group_text:
				hard_failures.append(f"strict_missing_constructor:{group.get('id', '?')}:{token}")
		for pattern_text in group.get("required_structural_patterns", []):
			if not re.search(pattern_text, group_text, re.IGNORECASE | re.DOTALL):
				hard_failures.append(f"strict_missing_structure:{group.get('id', '?')}:{pattern_text}")
		for token in group.get("required_touch_tokens", []):
			if token not in group_text:
				hard_failures.append(f"strict_missing_touch_mapping:{group.get('id', '?')}:{token}")
		for pattern_text in group.get("required_touch_patterns", []):
			if not re.search(pattern_text, group_text, re.IGNORECASE | re.DOTALL):
				hard_failures.append(f"strict_missing_touch_pattern:{group.get('id', '?')}:{pattern_text}")
		for pattern_text in group.get("required_factory_patterns", []):
			if not re.search(pattern_text, group_text, re.IGNORECASE | re.DOTALL):
				hard_failures.append(f"strict_missing_factory:{group.get('id', '?')}:{pattern_text}")
		for pattern_text in group.get("forbidden_runtime_mutations", []):
			if re.search(pattern_text, group_text, re.IGNORECASE | re.DOTALL):
				hard_failures.append(f"strict_runtime_camera_mutation:{group.get('id', '?')}")

	for contract in manifest.get("strict_file_contracts", []):
		contract_path = root / contract.get("path", "")
		if not contract_path.is_file():
			hard_failures.append(f"strict_file_missing:{contract.get('path', '?')}")
			continue
		contract_text = contract_path.read_text(encoding="utf-8", errors="replace")
		for pattern_text in contract.get("required_patterns", []):
			if not re.search(pattern_text, contract_text, re.IGNORECASE | re.DOTALL):
				hard_failures.append(f"strict_file_missing_structure:{contract.get('path', '?')}:{pattern_text}")
		for pattern_text in contract.get("forbidden_patterns", []):
			if re.search(pattern_text, contract_text, re.IGNORECASE | re.DOTALL):
				hard_failures.append(f"strict_file_forbidden_structure:{contract.get('path', '?')}:{pattern_text}")

	# The baseline is an explicit, reviewable inventory.  It prevents old rooms
	# from blocking every build while still catching migration regressions.
	baseline = manifest.get("legacy_baseline", {})
	if not baseline or any("count" not in value or "paths_sha256" not in value for value in baseline.values()):
		hard_failures.append("legacy_baseline_missing_explicit_count_or_hash")
	for rule, paths in legacy.items():
		if rule not in baseline:
			hard_failures.append(f"legacy_baseline_missing:{rule}")
			continue
		baseline_count = int(baseline[rule]["count"])
		if len(paths) > baseline_count:
			hard_failures.append(f"legacy_growth:{rule}:{len(paths)}>{baseline_count}")
		if "paths_sha256" not in baseline[rule]:
			print(f"25D|BASELINE_REQUIRED|{rule}|count={len(paths)}|sha256={path_hash(paths)}")
			continue
		if path_hash(paths) != baseline[rule]["paths_sha256"]:
			hard_failures.append(f"legacy_inventory_changed:{rule}")

	for rule, paths in sorted(legacy.items()):
		print(f"25D|LEGACY|{rule}|count={len(paths)}|baseline={baseline.get(rule, {}).get('count', '?')}|sha256={path_hash(paths)}")

	rooms = manifest.get("rooms", {})
	for room, config in sorted(rooms.items()):
		camera = config.get("camera", "fixed_projection")
		if camera not in {"fixed_projection", "bounded_x_projection"}:
			hard_failures.append(f"camera_mode:{room}:{camera}")
		projection = config.get("projection")
		if projection not in {"perspective", "orthographic"}:
			hard_failures.append(f"projection:{room}:{projection}")
		if not config.get("projection_locked", False):
			hard_failures.append(f"projection_not_locked:{room}")
		if camera == "bounded_x_projection" and not config.get("x_bounds"):
			hard_failures.append(f"bounded_x_without_bounds:{room}")
		if camera == "fixed_projection" and config.get("x_bounds"):
			hard_failures.append(f"ordinary_room_x_bounds:{room}")
		if config.get("world_card_medium") not in {"Sprite3D", "AnimatedSprite3D"}:
			hard_failures.append(f"world_card_medium:{room}:{config.get('world_card_medium')}")
		if config.get("canvas_exception") not in {None, "ui", "cinematic", "touch_feedback"}:
			hard_failures.append(f"canvas_exception:{room}:{config.get('canvas_exception')}")
		if config.get("allow_free_camera", False):
			hard_failures.append(f"free_camera_manifest:{room}")
		if config.get("allow_meshes", False) or config.get("allow_3d_physics", False):
			hard_failures.append(f"geometry_or_physics_manifest:{room}")
		for card in config.get("cards", []):
			if card.get("medium") not in {"Sprite3D", "AnimatedSprite3D"}:
				hard_failures.append(f"card_medium:{room}:{card.get('id', '?')}")
			if card.get("clipped", False) and not card.get("intentional_bleed", False):
				hard_failures.append(f"clipped_card:{room}:{card.get('id', '?')}")

	for failure in hard_failures:
		print(f"25D|FAIL|{failure}")
	if hard_failures:
		return 1
	print(f"25D|PASS|rooms={len(rooms)}|files={len(files)}|legacy_rules={len(legacy)}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
