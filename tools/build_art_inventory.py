#!/usr/bin/env python3
"""Build a deterministic inventory of all retained project artwork."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "art_library"
CSV_PATH = OUTPUT_DIR / "ART_INVENTORY.csv"
SUMMARY_PATH = OUTPUT_DIR / "ART_INVENTORY_SUMMARY.json"

ART_EXTENSIONS = {
	".blend",
	".bmp",
	".exr",
	".glb",
	".gltf",
	".hdr",
	".jpeg",
	".jpg",
	".png",
	".svg",
	".tga",
	".webp",
}

COLLECTIONS = (
	("assets", "runtime_pool", "yes", "Runtime-eligible art; reference status is determined by game content."),
	("assets_src", "editable_source", "no", "Editable source, generation original, or QA render."),
	("gen2/generated", "candidate_or_reject", "no", "Earlier generated alternate or rejected experiment; not approved by location."),
	("gen2", "generation_source_or_review", "no", "Generation workbench source, turnaround, prompt image, or review output."),
	("backups", "superseded_backup", "no", "Exact or dated pre-replacement rollback copy."),
	("audit", "review_evidence", "no", "Screenshot, contact sheet, or other visual audit evidence."),
	("art_library/candidates", "preserved_candidate", "no", "Unintegrated candidate retained from work in progress."),
	("tools/out", "tool_output", "no", "Generated tooling render, imported source-pack art, or QA output."),
	("disabled_addons", "disabled_addon_art", "no", "Artwork retained with disabled third-party tooling."),
	("example", "example_art", "yes", "Project example artwork retained in Godot import scope."),
)

EXCLUDED_DIRECTORY_NAMES = {".git", ".godot", ".worktrees", "__pycache__", "tmp"}


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def collect_rows() -> list[dict[str, str | int]]:
	rows: list[dict[str, str | int]] = []
	paths = sorted(ROOT.rglob("*"), key=lambda item: item.as_posix().lower())
	for path in paths:
		if (
			not path.is_file()
			or path.suffix.lower() not in ART_EXTENSIONS
			or any(part in EXCLUDED_DIRECTORY_NAMES for part in path.relative_to(ROOT).parts)
		):
			continue
		relative = path.relative_to(ROOT).as_posix()
		collection = "other_project_art"
		status = "project_support_art"
		godot_scope = "yes"
		row_note = "Project art outside the primary runtime and archive collections."
		for directory, default_status, directory_scope, note in COLLECTIONS:
			if relative == directory or relative.startswith(directory + "/"):
				collection = directory
				status = default_status
				godot_scope = directory_scope
				row_note = note
				break
		if collection == "assets_src" and any(part.lower().startswith("qa_") for part in path.parts):
			status = "qa_render"
			row_note = "Visual QA render retained with its editable source."
		rows.append(
			{
				"path": relative,
				"collection": collection,
				"status": status,
				"godot_import_scope": godot_scope,
				"extension": path.suffix.lower(),
				"bytes": path.stat().st_size,
				"sha256": sha256(path),
				"note": row_note,
			}
		)
	return sorted(rows, key=lambda row: str(row["path"]).lower())


def main() -> None:
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	rows = collect_rows()
	fieldnames = [
		"path",
		"collection",
		"status",
		"godot_import_scope",
		"extension",
		"bytes",
		"sha256",
		"note",
	]
	with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
		writer.writeheader()
		writer.writerows(rows)

	collection_counts = Counter(str(row["collection"]) for row in rows)
	status_counts = Counter(str(row["status"]) for row in rows)
	summary = {
		"file_count": len(rows),
		"total_bytes": sum(int(row["bytes"]) for row in rows),
		"collections": dict(sorted(collection_counts.items())),
		"statuses": dict(sorted(status_counts.items())),
	}
	SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
	print(f"Indexed {summary['file_count']} art files ({summary['total_bytes']} bytes).")


if __name__ == "__main__":
	main()
