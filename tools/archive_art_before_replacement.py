"""Archive pre-remediation art from git before replacing runtime files."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP_ROOT = ROOT / "backups" / "art_pre_remediation_2026-07-15"
SOURCE_REF = "origin/master"

HISTORICAL_PATHS = [
	"assets/mg/coal.png",
	"assets/mg/fish_body.png",
	"assets/mg/fish_fins.png",
	"assets/mg/fish_line.png",
	"assets/mg/flower.png",
	"assets/mg/flower2.png",
	"assets/mg/flower3.png",
	"assets/mg/flower4.png",
	"assets/mg/k_bush.png",
	"assets/mg/k_bush2.png",
	"assets/mg/k_flower1.png",
	"assets/mg/k_flower2.png",
	"assets/mg/k_pine.png",
	"assets/mg/k_sprout.png",
	"assets/mg/k_xmastree.png",
	"assets/mg/orn1.png",
	"assets/mg/orn2.png",
	"assets/mg/orn3.png",
	"assets/mg/orn4.png",
	"assets/mg/orn5.png",
	"assets/mg/rainbow_swatch.png",
	"assets/mg/seed.png",
	"assets/mg/sprout.png",
	"assets/mg/star.png",
	"assets/mg/sun.png",
	"assets/mg/tree.png",
	"assets/mg/xtree.png",
	"assets/terrain/beachball.png",
	"assets/terrain/flower.png",
	"assets/terrain/flower2.png",
	"assets/terrain/grass.jpg",
	"assets/terrain/leaf.png",
]


def git_bytes(ref: str, path: str) -> bytes:
	result = subprocess.run(
		["git", "show", f"{ref}:{path}"],
		cwd=ROOT,
		check=True,
		stdout=subprocess.PIPE,
	)
	return result.stdout


def sha256(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


def main() -> None:
	BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
	source_sha = subprocess.run(
		["git", "rev-parse", SOURCE_REF],
		cwd=ROOT,
		check=True,
		capture_output=True,
		text=True,
	).stdout.strip()
	entries = []
	for relative in HISTORICAL_PATHS:
		old_data = git_bytes(SOURCE_REF, relative)
		destination = BACKUP_ROOT / relative
		destination.parent.mkdir(parents=True, exist_ok=True)
		destination.write_bytes(old_data)
		current = ROOT / relative
		current_data = current.read_bytes() if current.exists() else b""
		entries.append(
			{
				"path": relative,
				"source_sha256": sha256(old_data),
				"current_sha256": sha256(current_data) if current_data else None,
				"changed": old_data != current_data,
			}
		)
	manifest = {
		"source_ref": SOURCE_REF,
		"source_commit": source_sha,
		"created": "2026-07-15",
		"entries": entries,
	}
	(BACKUP_ROOT / "manifest.json").write_text(
		json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
	)


if __name__ == "__main__":
	main()
