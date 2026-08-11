#!/usr/bin/env python3
"""Keep local and protected trusted-probe rosters in lockstep.

The display-only human-art capture is the sole intentional exception: local
CI runs it in the normal loop while GitHub runs it under Xvfb. Every other
trusted probe must appear exactly once in both loops. ``--stress`` mutates a
clean fixture so the gate proves each rule can fail before checking the repo.
"""

from __future__ import annotations

import argparse
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


LOOP_RE = re.compile(r"(?m)^\s*for p in\s+(.+?);\s*do\s*$")
SEPARATE_WORKFLOW_PROBES = {"probe_human_art_audit"}
GATE_COMMANDS = (
	"python3 tools/audit_probe_parity.py --stress",
	"python3 tools/audit_probe_parity.py",
)
AREA_MUSIC_LOCAL_COMMAND = "python3 tools/build_area_music.py --check"
AREA_MUSIC_WORKFLOW_TOKENS = (
	"runs-on: windows-2025",
	"actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
	'python-version: "3.13.14"',
	"numpy==2.5.1 scipy==1.18.0",
	"& ./tools/setup_video_tools.ps1",
	"python -B tools/build_area_music.py --check",
)


@dataclass(frozen=True)
class Issue:
	check_id: str
	path: str
	detail: str


def _read(path: Path) -> str:
	return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _loop_names(text: str) -> list[str] | None:
	match = LOOP_RE.search(text)
	return match.group(1).split() if match else None


def audit(root: Path, require_gate: bool = True) -> list[Issue]:
	root = root.resolve()
	ci_path = root / "scripts/ci.sh"
	workflow_path = root / ".github/workflows/probes.yml"
	ci_text = _read(ci_path)
	workflow_text = _read(workflow_path)
	issues: list[Issue] = []
	ci_names = _loop_names(ci_text)
	workflow_names = _loop_names(workflow_text)

	if ci_names is None:
		issues.append(Issue("PRB001", "scripts/ci.sh", "trusted probe loop was not found"))
	if workflow_names is None:
		issues.append(Issue("PRB001", ".github/workflows/probes.yml", "trusted probe loop was not found"))
	if ci_names is None or workflow_names is None:
		return issues

	for path, names in (("scripts/ci.sh", ci_names), (".github/workflows/probes.yml", workflow_names)):
		duplicates = sorted({name for name in names if names.count(name) > 1})
		for name in duplicates:
			issues.append(Issue("PRB002", path, f"probe is listed more than once: {name}"))

	ci_set = set(ci_names)
	workflow_set = set(workflow_names)
	missing_remote = sorted((ci_set - SEPARATE_WORKFLOW_PROBES) - workflow_set)
	extra_remote = sorted(workflow_set - ci_set)
	for name in missing_remote:
		issues.append(Issue("PRB003", ".github/workflows/probes.yml", f"local trusted probe is not remotely gated: {name}"))
	for name in extra_remote:
		issues.append(Issue("PRB003", "scripts/ci.sh", f"remote trusted probe is not locally gated: {name}"))

	for name in sorted(ci_set | workflow_set):
		if not (root / f"scripts/{name}.gd").is_file():
			issues.append(Issue("PRB004", f"scripts/{name}.gd", "listed trusted probe file is missing"))

	for name in sorted(SEPARATE_WORKFLOW_PROBES):
		if name not in ci_set:
			issues.append(Issue("PRB005", "scripts/ci.sh", f"separate visual probe is missing locally: {name}"))
		if f"scripts/{name}.gd" not in workflow_text:
			issues.append(Issue("PRB005", ".github/workflows/probes.yml", f"separate visual probe is not invoked: {name}"))

	if require_gate:
		for relative, text in (("scripts/ci.sh", ci_text), (".github/workflows/probes.yml", workflow_text)):
			for command in GATE_COMMANDS:
				if command not in text:
					issues.append(Issue("PRB006", relative, f"probe-parity gate is missing: {command}"))
		if AREA_MUSIC_LOCAL_COMMAND not in ci_text:
			issues.append(Issue("PRB007", "scripts/ci.sh", "deterministic area-music gate is missing locally"))
		for token in AREA_MUSIC_WORKFLOW_TOKENS:
			if token not in workflow_text:
				issues.append(Issue("PRB007", ".github/workflows/probes.yml", f"pinned area-music verifier is missing: {token}"))

	return sorted(issues, key=lambda issue: (issue.check_id, issue.path, issue.detail))


def _write_fixture(root: Path) -> None:
	(root / "scripts").mkdir(parents=True)
	(root / ".github/workflows").mkdir(parents=True)
	for name in ("probe_a", "probe_human_art_audit"):
		(root / f"scripts/{name}.gd").write_text("extends SceneTree\n", encoding="utf-8")
	gate_text = "\n".join(GATE_COMMANDS)
	(root / "scripts/ci.sh").write_text(
		f"{gate_text}\n{AREA_MUSIC_LOCAL_COMMAND}\n"
		"for p in probe_a probe_human_art_audit; do\n\ttrue\ndone\n",
		encoding="utf-8",
	)
	(root / ".github/workflows/probes.yml").write_text(
		f"{gate_text}\nfor p in probe_a; do\n  true\ndone\n"
		"godot -s scripts/probe_human_art_audit.gd\n"
		+ "\n".join(AREA_MUSIC_WORKFLOW_TOKENS)
		+ "\n",
		encoding="utf-8",
	)


def _stress_case(name: str, expected: str, mutate) -> tuple[bool, str]:
	with tempfile.TemporaryDirectory(prefix="probe-parity-") as temp:
		root = Path(temp)
		_write_fixture(root)
		mutate(root)
		fired = {issue.check_id for issue in audit(root)}
		return expected in fired, f"{name}: expected {expected}, fired {sorted(fired)}"


def stress() -> int:
	with tempfile.TemporaryDirectory(prefix="probe-parity-clean-") as temp:
		root = Path(temp)
		_write_fixture(root)
		if audit(root):
			print("PROBE_PARITY|FAIL clean fixture does not pass")
			return 1

	def remove_loop(root: Path) -> None:
		(root / "scripts/ci.sh").write_text("\n".join(GATE_COMMANDS), encoding="utf-8")

	def duplicate_probe(root: Path) -> None:
		path = root / "scripts/ci.sh"
		path.write_text(_read(path).replace("probe_a probe_human", "probe_a probe_a probe_human"), encoding="utf-8")

	def lose_remote_probe(root: Path) -> None:
		path = root / ".github/workflows/probes.yml"
		path.write_text(
			_read(path).replace("for p in probe_a", "for p in probe_human_art_audit"),
			encoding="utf-8",
		)

	def list_missing_file(root: Path) -> None:
		path = root / "scripts/ci.sh"
		path.write_text(_read(path).replace("probe_a probe_human", "probe_a probe_ghost probe_human"), encoding="utf-8")
		workflow = root / ".github/workflows/probes.yml"
		workflow.write_text(_read(workflow).replace("for p in probe_a", "for p in probe_a probe_ghost"), encoding="utf-8")

	def lose_separate_invocation(root: Path) -> None:
		path = root / ".github/workflows/probes.yml"
		path.write_text(_read(path).replace("godot -s scripts/probe_human_art_audit.gd", "true"), encoding="utf-8")

	def lose_gate(root: Path) -> None:
		path = root / ".github/workflows/probes.yml"
		path.write_text(_read(path).replace(GATE_COMMANDS[0], "true"), encoding="utf-8")

	def lose_music_toolchain(root: Path) -> None:
		path = root / ".github/workflows/probes.yml"
		path.write_text(_read(path).replace(AREA_MUSIC_WORKFLOW_TOKENS[1], "actions/setup-python@unpinned"), encoding="utf-8")

	def lose_local_music_gate(root: Path) -> None:
		path = root / "scripts/ci.sh"
		path.write_text(_read(path).replace(AREA_MUSIC_LOCAL_COMMAND, "true"), encoding="utf-8")

	cases = (
		("missing loop", "PRB001", remove_loop),
		("duplicate probe", "PRB002", duplicate_probe),
		("local/remote mismatch", "PRB003", lose_remote_probe),
		("missing probe file", "PRB004", list_missing_file),
		("missing separate invocation", "PRB005", lose_separate_invocation),
		("missing parity gate", "PRB006", lose_gate),
		("missing local music verifier", "PRB007", lose_local_music_gate),
		("missing pinned music verifier", "PRB007", lose_music_toolchain),
	)
	failed = 0
	for name, expected, mutate in cases:
		ok, detail = _stress_case(name, expected, mutate)
		print(f"PROBE_PARITY|stress {name}: {'OK' if ok else 'FAIL'}")
		if not ok:
			print(f"  {detail}")
			failed += 1
	return 1 if failed else 0


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
	parser.add_argument("--stress", action="store_true")
	args = parser.parse_args()
	if args.stress:
		return stress()
	issues = audit(args.root)
	for issue in issues:
		print(f"PROBE_PARITY|{issue.check_id}|{issue.path}|{issue.detail}")
	print(f"PROBE_PARITY|result: {'ALL OK' if not issues else f'{len(issues)} issue(s)'}")
	return 1 if issues else 0


if __name__ == "__main__":
	raise SystemExit(main())
