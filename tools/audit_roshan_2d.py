#!/usr/bin/env python3
"""Blocking contract audit for Mermaid Roshan's 2D-only character medium.

The project may use Godot's 3D scene graph to stage flat art, but Mermaid
Roshan herself is authored and rendered only as 2D atlas/cutout imagery. This
gate keeps retired models out of the editor, exports, runtime loaders, and
player implementation. It follows the visual-master-audit principle that each
check must be falsifiable: ``--stress`` injects one defect per rule and proves
that the rule fires.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


MODEL_EXTENSIONS = {".blend", ".dae", ".fbx", ".glb", ".gltf", ".obj"}
IGNORED_DIRS = {".git", ".godot", ".venv", "__pycache__", "decommissioned"}
RUNTIME_TEXT_SUFFIXES = {
	".cfg", ".gd", ".godot", ".json", ".sh", ".tscn", ".tres", ".yaml", ".yml",
}
RUNTIME_ROOTS = ("scripts", "scenes", ".github/workflows")
RUNTIME_FILES = ("project.godot", "export_presets.cfg")
REQUIRED_ATLASES = (
	"assets/characters/roshan_25d/roshan_directional.png",
	"assets/characters/roshan_25d/roshan_swim_front.png",
	"assets/characters/roshan_25d/roshan_swim_back.png",
	"assets/characters/roshan_25d/roshan_gesture_a.png",
	"assets/characters/roshan_25d/roshan_gesture_b.png",
	"assets/characters/roshan_25d/roshan_gesture_c.png",
	"assets/characters/roshan_25d/roshan_gesture_d.png",
	"assets/characters/roshan_25d/roshan_play_a.png",
	"assets/characters/roshan_25d/roshan_play_b.png",
)

MODEL_PATH_RE = re.compile(
	r"(?i)(?:res://|assets/|gen2/)[^\s\"']*roshan[^\s\"']*"
	r"\.(?:blend|dae|fbx|glb|gltf|obj)"
	"|"
	r"(?:res://|assets/|gen2/)[^\s\"']*roshan[^\s\"']*/[^\s\"']*"
	r"\.(?:blend|dae|fbx|glb|gltf|obj)"
)
OBSOLETE_PLAYER_API_RE = re.compile(
	r"(?i)\b(?:player|pl)\.(?:model_v\d*|skel|hair_sim|bone_idx|_rot_bone)\b"
)
OBSOLETE_DIRECTION_RE = re.compile(
	r"(?i)(?:rigged\s+3d\s+roshan|real\s+roshan\s+rig|roshan.{0,32}\bglb\b)"
)


@dataclass(frozen=True)
class Issue:
	check_id: str
	path: str
	detail: str


def _is_ignored(path: Path, root: Path) -> bool:
	try:
		parts = path.relative_to(root).parts
	except ValueError:
		return True
	return any(part in IGNORED_DIRS for part in parts)


def _iter_files(root: Path):
	for path in root.rglob("*"):
		if path.is_file() and not _is_ignored(path, root):
			yield path


def _relative(path: Path, root: Path) -> str:
	return path.relative_to(root).as_posix()


def _runtime_text_files(root: Path):
	seen: set[Path] = set()
	for relative_root in RUNTIME_ROOTS:
		base = root / relative_root
		if not base.exists():
			continue
		for path in base.rglob("*"):
			if path.is_file() and path.suffix.lower() in RUNTIME_TEXT_SUFFIXES:
				resolved = path.resolve()
				if resolved not in seen:
					seen.add(resolved)
					yield path
	for relative in RUNTIME_FILES:
		path = root / relative
		if path.is_file():
			yield path


def audit(root: Path, require_ci: bool = True) -> list[Issue]:
	root = root.resolve()
	issues: list[Issue] = []

	for path in _iter_files(root):
		if path.suffix.lower() not in MODEL_EXTENSIONS:
			continue
		relative = _relative(path, root)
		if any("roshan" in part.lower() for part in path.relative_to(root).parts):
			issues.append(Issue(
				"R2D001", relative,
				"3D Mermaid Roshan asset is present in the active project",
			))

	for path in _runtime_text_files(root):
		relative = _relative(path, root)
		text = path.read_text(encoding="utf-8", errors="replace")
		for line_number, line in enumerate(text.splitlines(), 1):
			if MODEL_PATH_RE.search(line):
				issues.append(Issue(
					"R2D002", f"{relative}:{line_number}",
					"runtime/editor configuration references a Roshan 3D model",
				))
			if OBSOLETE_PLAYER_API_RE.search(line):
				issues.append(Issue(
					"R2D003", f"{relative}:{line_number}",
					"removed Roshan rig API is still referenced",
				))
			if OBSOLETE_DIRECTION_RE.search(line):
				issues.append(Issue(
					"R2D004", f"{relative}:{line_number}",
					"runtime source still describes Roshan as a 3D rig/model",
				))

	player_path = root / "scripts/player.gd"
	if not player_path.is_file():
		issues.append(Issue("R2D005", "scripts/player.gd", "player implementation is missing"))
	else:
		player = player_path.read_text(encoding="utf-8", errors="replace")
		required_tokens = (
			"const ROSHAN_25D_SHEETS",
			"classic_sprite = Sprite3D.new()",
			"classic_sprite.shaded = false",
		)
		for token in required_tokens:
			if token not in player:
				issues.append(Issue(
					"R2D005", "scripts/player.gd",
					f"2D player renderer contract is missing token: {token}",
				))
		for forbidden in ("Skeleton3D", "model_v3", "hair_sim", "roshan.glb", "roshan_v"):
			if forbidden in player:
				issues.append(Issue(
					"R2D005", "scripts/player.gd",
					f"player implementation contains retired model token: {forbidden}",
				))

	for relative in REQUIRED_ATLASES:
		if not (root / relative).is_file():
			issues.append(Issue("R2D006", relative, "required 2D Roshan atlas is missing"))

	if require_ci:
		ci_contracts = {
			"scripts/ci.sh": (
				"python3 tools/audit_roshan_2d.py --stress",
				"python3 tools/audit_roshan_2d.py",
			),
			".github/workflows/probes.yml": (
				"python3 tools/audit_roshan_2d.py --stress",
				"python3 tools/audit_roshan_2d.py",
			),
		}
		for relative, commands in ci_contracts.items():
			path = root / relative
			text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
			for command in commands:
				if command not in text:
					issues.append(Issue(
						"R2D007", relative,
						f"blocking 2D-only gate is missing command: {command}",
					))

	return sorted(issues, key=lambda issue: (issue.check_id, issue.path, issue.detail))


def _write_fixture(root: Path) -> None:
	player = root / "scripts/player.gd"
	player.parent.mkdir(parents=True, exist_ok=True)
	player.write_text(
		"const ROSHAN_25D_SHEETS = {}\n"
		"func _ready():\n"
		"\tclassic_sprite = Sprite3D.new()\n"
		"\tclassic_sprite.shaded = false\n",
		encoding="utf-8",
	)
	for relative in REQUIRED_ATLASES:
		path = root / relative
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(b"fixture")
	ci = root / "scripts/ci.sh"
	ci.write_text(
		"python3 tools/audit_roshan_2d.py --stress\n"
		"python3 tools/audit_roshan_2d.py\n",
		encoding="utf-8",
	)
	workflow = root / ".github/workflows/probes.yml"
	workflow.parent.mkdir(parents=True, exist_ok=True)
	workflow.write_text(
		"python3 tools/audit_roshan_2d.py --stress\n"
		"python3 tools/audit_roshan_2d.py\n",
		encoding="utf-8",
	)


def _stress_case(name: str, expected: str, mutate) -> tuple[bool, str]:
	with tempfile.TemporaryDirectory(prefix="roshan-2d-audit-") as temp:
		root = Path(temp)
		_write_fixture(root)
		mutate(root)
		fired = {issue.check_id for issue in audit(root)}
		return expected in fired, f"{name}: expected {expected}, fired {sorted(fired)}"


def stress() -> int:
	with tempfile.TemporaryDirectory(prefix="roshan-2d-audit-clean-") as temp:
		root = Path(temp)
		_write_fixture(root)
		clean_issues = audit(root)
		if clean_issues:
			print(f"ROSHAN2D| stress fixture invalid: {clean_issues}")
			return 1

	def add_runtime_model(root: Path) -> None:
		path = root / "assets/characters/roshan_return.glb"
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(b"model")

	def add_source_model(root: Path) -> None:
		path = root / "gen2/meshy/roshan_return/static.glb"
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(b"model")

	def add_runtime_reference(root: Path) -> None:
		(root / "scripts/bad.gd").write_text(
			'var avatar = load("res://assets/characters/roshan_return.glb")\n',
			encoding="utf-8",
		)

	def add_old_api(root: Path) -> None:
		(root / "scripts/bad.gd").write_text("var old = player.model_v3\n", encoding="utf-8")

	def add_old_direction(root: Path) -> None:
		(root / "scripts/bad.gd").write_text("# rigged 3D Roshan\n", encoding="utf-8")

	def break_player(root: Path) -> None:
		with (root / "scripts/player.gd").open("a", encoding="utf-8") as handle:
			handle.write("var old: Skeleton3D\n")

	def remove_atlas(root: Path) -> None:
		(root / REQUIRED_ATLASES[0]).unlink()

	def remove_ci_gate(root: Path) -> None:
		(root / "scripts/ci.sh").write_text("true\n", encoding="utf-8")

	cases = (
		("runtime model", "R2D001", add_runtime_model),
		("source model", "R2D001", add_source_model),
		("runtime model reference", "R2D002", add_runtime_reference),
		("removed player API", "R2D003", add_old_api),
		("retired direction", "R2D004", add_old_direction),
		("player renderer regression", "R2D005", break_player),
		("missing atlas", "R2D006", remove_atlas),
		("missing CI gate", "R2D007", remove_ci_gate),
	)
	failures: list[str] = []
	for name, expected, mutate in cases:
		passed, detail = _stress_case(name, expected, mutate)
		if not passed:
			failures.append(detail)
	if failures:
		for failure in failures:
			print(f"ROSHAN2D| STRESS FAIL| {failure}")
		return 1
	print(f"ROSHAN2D| stress: {len(cases)} falsification cases ALL OK")
	return 0


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
	parser.add_argument("--stress", action="store_true", help="prove every rule can fail")
	args = parser.parse_args()
	if args.stress:
		return stress()
	issues = audit(args.root)
	if issues:
		for issue in issues:
			print(f"ROSHAN2D| FAIL| {issue.check_id}| {issue.path}| {issue.detail}")
		print(f"ROSHAN2D| RESULT: FAIL ({len(issues)} issue(s))")
		return 1
	print("ROSHAN2D| RESULT: ALL OK - active project is 2D Roshan only")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
