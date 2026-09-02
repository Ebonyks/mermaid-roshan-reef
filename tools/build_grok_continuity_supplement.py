#!/usr/bin/env python3
"""Build a deterministic provenance manifest for files added after a visual packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


def digest(path: Path) -> str:
	hash_value = hashlib.sha256()
	with path.open("rb") as handle:
		for block in iter(lambda: handle.read(1024 * 1024), b""):
			hash_value.update(block)
	return hash_value.hexdigest()


def image_dimensions(path: Path) -> list[int] | None:
	if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
		return None
	with Image.open(path) as image:
		return [image.width, image.height]


def disposition(relative: str) -> tuple[str, bool, bool, str]:
	lower = relative.lower()
	if "/rejected/" in f"/{lower}" or lower.startswith("rejected/"):
		return "rejected_first_frame_evidence", False, False, "project-original generated candidate; rejected and retained unchanged"
	if lower.startswith("first_frames/") and lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
		return "human_pending_first_frame_candidate", False, False, "project-original complete flattened image generation; human review pending"
	if lower.startswith("location_authorities/"):
		return "human_pending_location_authority_candidate", False, False, "project-original complete flattened image generation; human review pending"
	if lower.startswith("generation_inputs/") and lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
		return "generator_compatible_lossless_authority_derivative", True, True, "non-destructive whole-canvas normalization; source original preserved"
	if lower.startswith("generation_prompts/"):
		return "exact_first_frame_generation_prompt", False, False, "project-authored provenance record"
	if lower == "location_geometry_lock.json":
		return "location_topology_and_candidate_review_record", False, False, "project-authored audit record"
	if lower == "first_frames/first_frame_review.json":
		return "first_frame_review_record", False, False, "project-authored audit record"
	if lower.startswith("generation_inputs/") and lower.endswith(".json"):
		return "normalization_provenance_record", False, False, "project-authored deterministic transform record"
	return "continuity_handoff_support_record", False, False, "project-authored handoff record"


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("packet", type=Path)
	args = parser.parse_args()
	packet = args.packet.resolve()
	base = json.loads((packet / "HANDOFF_PACKET.json").read_text(encoding="utf-8"))
	base_paths = {
		item.get("path") for item in base.get("assets", []) if isinstance(item, dict)
	}
	excluded = {
		"HANDOFF_PACKET.json",
		"CONTINUITY_SUPPLEMENT.json",
		"README.md",
		"IMAGINE_HANDOFF.json",
	}
	assets: list[dict[str, Any]] = []
	for path in sorted(item for item in packet.rglob("*") if item.is_file()):
		relative = path.relative_to(packet).as_posix()
		if relative in excluded or relative in base_paths:
			continue
		role, appearance, binding, provenance = disposition(relative)
		assets.append({
			"path": relative,
			"role": role,
			"media_type": "image/png" if path.suffix.lower() == ".png" else "text/plain",
			"dimensions": image_dimensions(path),
			"sha256": digest(path),
			"license_provenance": provenance,
			"modifications": "none after recorded generation or transform",
			"appearance_authority": appearance,
			"bound_reference_eligible": binding,
			"used_as_delivery_pixels": False,
		})
	payload_lines = [f"{item['path']}|{item['sha256']}\n" for item in assets]
	payload_sha = hashlib.sha256("".join(payload_lines).encode("utf-8")).hexdigest()
	manifest = {
		"schema": "external-animation-continuity-supplement-v1",
		"packet_id": base.get("packet_id"),
		"runtime_asset": False,
		"used_as_delivery_pixels": False,
		"payload_sha256": payload_sha,
		"payload_hash_formula": "SHA256 of UTF-8 sorted <relative_path>|<lowercase_sha256>\\n records",
		"assets": assets,
	}
	(packet / "CONTINUITY_SUPPLEMENT.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(f"wrote {packet / 'CONTINUITY_SUPPLEMENT.json'} with {len(assets)} records and payload {payload_sha}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
