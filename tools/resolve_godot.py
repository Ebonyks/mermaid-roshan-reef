#!/usr/bin/env python3
"""Select the exact approved stable Godot; never silently run an older PATH binary."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys

try:
	from . import audit_godot_baseline as baseline
except ImportError:
	import audit_godot_baseline as baseline


def candidates(root: Path, data: dict, environment: dict) -> list[str]:
	version, release = data["version"], data["release"]
	paths = [root / f"Godot_v{release}_linux.x86_64"]
	for folder in ("editor", "bin"):
		paths.append(root / "tmp" / f"godot-{version}" / folder / f"Godot_v{release}_win64_console.exe")
	if environment.get("LOCALAPPDATA"):
		installed = Path(environment["LOCALAPPDATA"]) / "Programs/MermaidReefTools/Godot" / version
		paths.extend([installed / "godot_console.exe", installed / "godot.exe"])
	result = [str(path.resolve()) for path in paths if path.is_file()]
	for command in ("godot", "godot_console"):
		resolved = shutil.which(command)
		if resolved and resolved not in result:
			result.append(resolved)
	return result


def resolve(root: Path, data: dict, explicit: str | None, environment: dict) -> str:
	issues = baseline.validate_metadata(data)
	if issues:
		raise ValueError("; ".join(issues))
	if explicit:
		requested = Path(explicit)
		if requested.is_absolute() or any(separator in explicit for separator in ("/", "\\")) or (root / requested).is_file():
			executable = str((root / requested).resolve())
		else:
			executable = shutil.which(explicit) or explicit
		issues = baseline.validate_executable(executable, data)
		if issues:
			raise ValueError("Explicit GODOT is invalid: " + "; ".join(issues))
		return executable
	for executable in candidates(root, data, environment):
		if not baseline.validate_executable(executable, data):
			return executable
	raise ValueError(f"No official {data['release']} executable found; set GODOT to that exact build.")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=baseline.REPO)
	parser.add_argument("--godot", default=os.environ.get("GODOT"))
	args = parser.parse_args()
	try:
		data = baseline.load_baseline(args.root / "tools/godot_baseline.json")
		print(resolve(args.root.resolve(), data, args.godot, dict(os.environ)))
		return 0
	except (OSError, ValueError) as exc:
		print(f"GODOTRESOLVE|FAIL|{exc}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
