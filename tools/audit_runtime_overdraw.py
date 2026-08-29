#!/usr/bin/env python3
"""Blocking, state-based transparent-overdraw audit for the mobile target.

The manifest is intentionally state-oriented: a zone name alone cannot expose
modal panels, dirty washes, transition ghosts, or shader-heavy water. Values
are authored from projected 1280x720 screen-space measurements and are updated
only with a matching visual/runtime review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


DEFAULT_MANIFEST = Path("tools/manifests/runtime_overdraw_manifest.json")
REQUIRED_FIELDS = {
	"projected_coverage",
	"transparent_overdraw",
	"full_screen_overlays",
	"temporal_layers",
	"shader_samples",
	"background_routes",
	"cards_full_frame",
}
REQUIRED_EVIDENCE_FIELDS = {"source_path", "source_sha256", "record_type", "card_rectangles"}


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--root", type=Path, default=Path.cwd())
	parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
	args = parser.parse_args()
	path = args.manifest if args.manifest.is_absolute() else args.root / args.manifest
	try:
		data = json.loads(path.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError) as exc:
		print(f"OVERDRAW|FAIL|manifest|{path}|{exc}")
		return 1

	limits = data.get("limits", {})
	max_coverage = float(limits.get("max_projected_coverage", 1.75))
	max_overdraw = float(limits.get("max_transparent_overdraw", 2.0))
	max_shader = int(limits.get("max_shader_samples", 8))
	max_temporal = int(limits.get("max_temporal_layers", 1))
	failures: list[str] = []
	warnings: list[str] = []
	states = data.get("states", {})
	if not states:
		failures.append("no_states")

	for state, record in sorted(states.items()):
		missing = REQUIRED_FIELDS - set(record)
		for field in sorted(missing):
			failures.append(f"{state}:missing:{field}")
		if missing:
			continue
		evidence = record.get("evidence", {})
		missing_evidence = REQUIRED_EVIDENCE_FIELDS - set(evidence)
		for field in sorted(missing_evidence):
			failures.append(f"{state}:missing_evidence:{field}")
		if missing_evidence:
			continue
		source = args.root / evidence["source_path"]
		if not source.is_file():
			failures.append(f"{state}:evidence_source_missing:{evidence['source_path']}")
		else:
			actual_hash = hashlib.sha256(source.read_bytes()).hexdigest()
			if actual_hash.lower() != str(evidence["source_sha256"]).lower():
				failures.append(f"{state}:evidence_source_hash_mismatch")
		if evidence["record_type"] != "runtime_card_rectangles":
			failures.append(f"{state}:evidence_record_type:{evidence['record_type']}")
		if not isinstance(evidence["card_rectangles"], list) or not evidence["card_rectangles"]:
			failures.append(f"{state}:empty_card_rectangles")
		for card in evidence.get("card_rectangles", []):
			rect = card.get("rect", [])
			if len(rect) != 4 or float(rect[2]) <= 0 or float(rect[3]) <= 0:
				failures.append(f"{state}:invalid_card_rect:{card.get('id', '?')}")
			if not 0.0 <= float(card.get("alpha_visible_ratio", -1.0)) <= 1.0:
				failures.append(f"{state}:invalid_alpha_area:{card.get('id', '?')}")
			if card.get("material_class") not in {"opaque", "hard_cutout", "soft_blend"}:
				failures.append(f"{state}:invalid_material_class:{card.get('id', '?')}")
		cards = evidence.get("card_rectangles", [])
		coverage = sum(float(card["rect"][2]) * float(card["rect"][3]) for card in cards) / (1280.0 * 720.0)
		overdraw = sum(float(card["rect"][2]) * float(card["rect"][3]) * float(card["alpha_visible_ratio"]) for card in cards) / (1280.0 * 720.0)
		expected_coverage = record.get("expected_projected_coverage")
		expected_overdraw = record.get("expected_transparent_overdraw")
		if expected_coverage is None or expected_overdraw is None:
			failures.append(f"{state}:missing_expected_derived_metrics")
		else:
			if abs(float(expected_coverage) - coverage) > 0.01:
				failures.append(f"{state}:fabricated_projected_coverage:{expected_coverage}!={coverage:.3f}")
			if abs(float(expected_overdraw) - overdraw) > 0.01:
				failures.append(f"{state}:fabricated_transparent_overdraw:{expected_overdraw}!={overdraw:.3f}")
		shader = int(record["shader_samples"])
		temporal = int(record["temporal_layers"])
		overlays = int(record["full_screen_overlays"])
		routes = int(record["background_routes"])
		if coverage > max_coverage:
			failures.append(f"{state}:coverage:{coverage}>{max_coverage}")
		if overdraw > max_overdraw:
			failures.append(f"{state}:transparent_overdraw:{overdraw}>{max_overdraw}")
		if shader > max_shader:
			failures.append(f"{state}:shader_samples:{shader}>{max_shader}")
		if temporal > max_temporal:
			failures.append(f"{state}:temporal_layers:{temporal}>{max_temporal}")
		if overlays > 0 and not record.get("overlay_replaces_world", False):
			failures.append(f"{state}:full_screen_overlay_over_world")
		if routes != 1:
			failures.append(f"{state}:background_routes:{routes}!=1")
		if record.get("cards_full_frame", 0) > 0:
			failures.append(f"{state}:full_frame_card_count:{record['cards_full_frame']}")
		if coverage >= max_coverage * 0.9 or overdraw >= max_overdraw * 0.9:
			warnings.append(f"{state}:near_limit")
		print(f"OVERDRAW|STATE|{state}|coverage={coverage:.3f}|transparent={overdraw:.3f}|shader={shader}|temporal={temporal}")

	for warning in warnings:
		print(f"OVERDRAW|WARN|{warning}")
	for failure in failures:
		print(f"OVERDRAW|FAIL|{failure}")
	if failures:
		return 1
	print(f"OVERDRAW|PASS|states={len(states)}|limits={max_coverage:.2f},{max_overdraw:.2f},{max_shader}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
