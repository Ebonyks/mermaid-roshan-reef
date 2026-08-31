#!/usr/bin/env python3
"""Reject drift between the approved Godot baseline and release-critical pins."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


REPO = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO / "tools" / "godot_baseline.json"
ENGINE_CONTRACT_KEYS = frozenset({
	"major", "minor", "patch", "status", "build", "version_string",
})


class BaselineError(ValueError):
	"""Raised when the structured Godot baseline cannot be trusted."""


def load_baseline(path: Path = BASELINE_PATH) -> dict[str, Any]:
	try:
		data = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as error:
		raise BaselineError(f"cannot load baseline {path}: {error}") from error
	if not isinstance(data, dict):
		raise BaselineError(f"baseline root must be an object: {path}")
	return data


def validate_metadata(data: dict[str, Any]) -> list[str]:
	errors: list[str] = []
	if not isinstance(data, dict):
		return ["baseline root must be an object"]
	version = str(data.get("version", ""))
	series = str(data.get("series", ""))
	status = str(data.get("status", ""))
	release = str(data.get("release", ""))
	parts = version.split(".")
	if len(parts) != 3 or not all(part.isdigit() for part in parts):
		errors.append(f"version is not major.minor.patch: {version!r}")
	if len(parts) >= 2 and series != ".".join(parts[:2]):
		errors.append(f"series {series!r} does not match version {version!r}")
	if status != "stable":
		errors.append(f"production baseline must be stable, got {status!r}")
	if release != f"{version}-{status}":
		errors.append(f"release {release!r} does not match version/status")
	downloads = data.get("downloads")
	if not isinstance(downloads, dict):
		return errors + ["downloads is not an object"]
	for name, digest_names in {
		"linux_x86_64": ("sha512",),
		"windows_x86_64": ("sha256",),
		"export_templates": ("sha256", "sha512"),
	}.items():
		entry = downloads.get(name)
		if not isinstance(entry, dict):
			errors.append(f"missing download metadata: {name}")
			continue
		if release not in str(entry.get("filename", "")):
			errors.append(f"{name} filename is not pinned to {release}")
		for digest_name in digest_names:
			digest = str(entry.get(digest_name, ""))
			expected_length = 64 if digest_name == "sha256" else 128
			if re.fullmatch(rf"[0-9a-f]{{{expected_length}}}", digest) is None:
				errors.append(f"{name} has invalid {digest_name}")
	return errors


def canonical_engine_contract(data: dict[str, Any]) -> dict[str, Any]:
	"""Derive the normalized engine identity used by runtime evidence."""
	errors = validate_metadata(data)
	if errors:
		raise BaselineError("invalid Godot baseline: " + "; ".join(errors))
	major, minor, patch = (int(part) for part in str(data["version"]).split("."))
	release = str(data["release"])
	return {
		"major": major,
		"minor": minor,
		"patch": patch,
		"status": str(data["status"]),
		"build": "official",
		"version_string": f"{release} (official)",
	}


def engine_version_matches(version_string: str, data: dict[str, Any]) -> bool:
	"""Accept Godot's dotted output and normalized fixture strings alike."""
	try:
		canonical = canonical_engine_contract(data)
	except BaselineError:
		return False
	version = re.escape(str(data["version"]))
	status = re.escape(str(data["status"]))
	return re.match(
		rf"^{version}(?:[.-]){status}(?:[.-]official)?(?:\b|\s|\()",
		str(version_string),
	) is not None or str(version_string) == canonical["version_string"]


def required_pins(data: dict[str, Any]) -> dict[str, list[str]]:
	version = str(data["version"])
	series = str(data["series"])
	release = str(data["release"])
	downloads = data["downloads"]
	linux_sha512 = str(downloads["linux_x86_64"]["sha512"])
	template_sha512 = str(downloads["export_templates"]["sha512"])
	return {
		".github/workflows/android.yml": [
			f'GODOT_VERSION: "{version}"', f'GODOT_RELEASE: "{release}"',
			linux_sha512, template_sha512,
		],
		".github/workflows/probes.yml": [f'GODOT_RELEASE: "{release}"', linux_sha512],
		".github/workflows/race-feel.yml": [f'GODOT_RELEASE: "{release}"', linux_sha512],
		"AGENTS.md": [f"exactly Godot {release}", f"Godot_v{release}_linux.x86_64"],
		"CLAUDE.md": [f"exactly Godot {release}", f"Godot_v{release}_linux.x86_64"],
		"project.godot": [f"Runtime/editor baseline: Godot {release}",
			f'config/features=PackedStringArray("{series}", "Mobile")'],
		"design/01_GAME_DESIGN.md": [f"exact Godot {release} game"],
		"design/03_TECHNICAL_ARCHITECTURE.md": [f"exactly Godot {release}",
			f"Godot_v{release}_linux.x86_64"],
		"design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md": [f"exactly Godot {release}"],
		"tools/audit_visual_design.py": [
			"canonical_engine_contract",
		],
		"tools/plan_audit_rollback.py": [f"exact Godot {release}"],
		"tools/visual_audit_spec.json": [f"exactly Godot {release}"],
	}


def validate_file_pins(root: Path, data: dict[str, Any]) -> list[str]:
	errors: list[str] = []
	for relative, pins in required_pins(data).items():
		path = root / relative
		if not path.is_file():
			errors.append(f"missing pinned file: {relative}")
			continue
		text = path.read_text(encoding="utf-8")
		for pin in pins:
			if pin not in text:
				errors.append(f"{relative} is missing baseline pin: {pin}")
	return errors


def validate_executable(godot: str, data: dict[str, Any]) -> list[str]:
	try:
		completed = subprocess.run(
			[godot, "--version"], cwd=REPO, check=False, timeout=30,
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
			encoding="utf-8", errors="replace",
		)
	except (OSError, subprocess.TimeoutExpired) as error:
		return [f"cannot execute configured Godot {godot!r}: {error}"]
	version_text = completed.stdout.strip()
	version = re.escape(str(data["version"]))
	status = re.escape(str(data["status"]))
	build = re.escape(str(data["official_build"]))
	pattern = rf"^{version}[.-]{status}[.-]official[.-]{build}(?:\b|$)"
	if completed.returncode != 0 or re.match(pattern, version_text) is None:
		return [f"configured Godot is not the approved official build: {version_text!r}"]
	return []


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--godot", help="also verify this Godot executable")
	args = parser.parse_args(argv)
	try:
		data = load_baseline()
	except BaselineError as error:
		print(f"GODOTBASELINE|FAIL|{error}")
		return 1
	errors = validate_metadata(data)
	if not errors:
		errors.extend(validate_file_pins(REPO, data))
	if args.godot:
		errors.extend(validate_executable(args.godot, data))
	if errors:
		for error in errors:
			print(f"GODOTBASELINE|FAIL|{error}")
		return 1
	print(f"GODOTBASELINE|ALL OK|{data['release']}|official.{data['official_build']}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
