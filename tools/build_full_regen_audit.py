#!/usr/bin/env python3
"""Freeze the full-regeneration target ledger and summarize failure patterns."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "audit" / "game_art_ledger_pass35_2026-07-16.csv"
OUT_DIR = ROOT / "audit" / "full_regen_2026-07-18"
LEDGER = OUT_DIR / "target_ledger.csv"
SUMMARY = OUT_DIR / "target_summary.json"
REPORT = ROOT / "FULL_TEXTURE_REGEN_FAILURE_ANALYSIS_2026-07-18.md"
PACK = "assets/full_texture_regen_2026-07-18"


FAILURE_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
	("primitive_or_generic_geometry", ("primitive", "box", "cylinder", "sphere", "slab", "generic", "flat boxes", "floating")),
	("composition_scale_or_occlusion", ("composition", "occlud", "scale", "sightline", "camera", "sparse", "placement", "conflicting focal")),
	("repetition_tiling_or_overdraw", ("repeat", "tiling", "overdraw", "crossed card", "billboard", "clutter")),
	("material_or_rendering_mismatch", ("material", "atlas style", "monochrome", "painted draft", "source does not integrate", "flat fill")),
	("exposure_bloom_or_emission", ("bloom", "overexposure", "overexposed", "emissive", "white clipping")),
	("anatomy_or_identity_error", ("anatom", "incomplete", "silhouette", "wing", "generic form")),
	("environment_or_biome_language", ("biome", "terrain", "surface", "above-water", "undersea", "environment")),
	("missing_runtime_validation", ("unverified", "not runtime validated", "owner review", "capture", "candidate")),
	("pipeline_integrity_or_orphans", ("corrupt", "invalid", "orphan", "unwired", "provenance", "branch-only")),
)


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def target_kind(row: dict[str, str]) -> str:
	role = row["runtime_role"].lower()
	source = row["source_or_builder"].lower()
	if row["area"] == "Pipeline":
		return "pipeline_repair"
	if any(word in role for word in ("overall", "presentation", "composition", "placement", "transition", "route")):
		return "composition_kit"
	if role in {"kelp cards", "seagrass cards", "coral flower hybrid"}:
		return "modeled_3d"
	if source.endswith((".png", ".jpg", ".jpeg", ".webp", ".hdr")) or any(
		word in role for word in ("texture", "surface", "ground", "backdrop", "canvas", "caustic", "floor")
	):
		return "painted_2d"
	return "modeled_3d"


def failure_categories(row: dict[str, str]) -> list[str]:
	haystack = row.get("primary_defect", "").lower()
	matches = [name for name, needles in FAILURE_RULES if any(needle in haystack for needle in needles)]
	return matches or ["uncategorized_polish_gap"]


def disposition(row: dict[str, str]) -> str:
	if row.get("protected", "").lower() == "yes":
		if row.get("post_status") not in {"source_locked_5", "protected_manual_only"}:
			return "regenerate_presentation_only"
		return "exclude_protected"
	if row.get("post_status") in {"source_locked_5", "protected_manual_only"}:
		return "exclude_protected_or_manual"
	return "regenerate_candidate"


def build_rows() -> list[dict[str, str]]:
	with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
		source_rows = list(csv.DictReader(handle))
	rows: list[dict[str, str]] = []
	for index, source_row in enumerate(source_rows, start=1):
		disp = disposition(source_row)
		kind = target_kind(source_row)
		role_id = f"R{index:03d}_{slug(source_row['area'])}_{slug(source_row['runtime_role'])}"
		categories = failure_categories(source_row)
		rows.append(
			{
				"role_id": role_id,
				"area": source_row["area"],
				"runtime_role": source_row["runtime_role"],
				"current_source": source_row["source_or_builder"],
				"baseline_score": source_row["score"],
				"current_post_score": source_row["post_score"],
				"current_status": source_row["post_status"],
				"focality": source_row["focality"],
				"disposition": disp,
				"target_kind": kind,
				"failure_categories": ";".join(categories),
				"primary_defect": source_row["primary_defect"],
				"replacement_contract": source_row["replacement_contract"],
				"candidate_folder": f"{PACK}/{slug(source_row['area'])}/{role_id.lower()}",
				"stress_status": "pending" if disp.startswith("regenerate_") else "not_applicable",
				"candidate_score_cap": "4" if disp.startswith("regenerate_") else source_row["post_score"],
				"owner_5_status": "pending_owner_acceptance" if disp.startswith("regenerate_") else "not_applicable",
			}
		)
	return rows


def write_ledger(rows: list[dict[str, str]]) -> None:
	OUT_DIR.mkdir(parents=True, exist_ok=True)
	with LEDGER.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
		writer.writeheader()
		writer.writerows(rows)


def write_summary(rows: list[dict[str, str]]) -> dict[str, object]:
	targets = [row for row in rows if row["disposition"].startswith("regenerate_")]
	exclusions = [row for row in rows if not row["disposition"].startswith("regenerate_")]
	areas = Counter(row["area"] for row in targets)
	kinds = Counter(row["target_kind"] for row in targets)
	failures: Counter[str] = Counter()
	for row in targets:
		failures.update(row["failure_categories"].split(";"))
	summary: dict[str, object] = {
		"source_role_count": len(rows),
		"regeneration_target_count": len(targets),
		"protected_or_manual_exclusion_count": len(exclusions),
		"northern_in_scope": any(row["area"].lower().startswith("development") and "northern" in row["runtime_role"].lower() for row in targets),
		"target_pack": PACK,
		"areas": dict(sorted(areas.items())),
		"target_kinds": dict(sorted(kinds.items())),
		"failure_categories": dict(failures.most_common()),
		"score_policy": "Automated candidates cap at 4; owner acceptance is required for 5.",
	}
	SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
	return summary


def write_report(rows: list[dict[str, str]], summary: dict[str, object]) -> None:
	targets = [row for row in rows if row["disposition"].startswith("regenerate_")]
	exclusions = [row for row in rows if not row["disposition"].startswith("regenerate_")]
	failure_counts = summary["failure_categories"]
	lines = [
		"# Full Texture Regeneration Failure Analysis - 2026-07-18",
		"",
		"This report freezes the pre-regeneration baseline for every runtime role in",
		"`audit/game_art_ledger_pass35_2026-07-16.csv`. Northern Kingdom is in scope.",
		"Protected book/family art and manually sourced cat/toy work remain excluded.",
		"",
		"## Scope",
		"",
		f"- Audited runtime roles: **{len(rows)}**",
		f"- Regeneration targets: **{len(targets)}**",
		f"- Protected/manual exclusions: **{len(exclusions)}**",
		f"- Candidate destination: `{PACK}/`",
		"- Score ceiling before owner review: **4/5**",
		"",
		"## Frequent failure patterns",
		"",
	]
	for name, count in failure_counts.items():
		lines.append(f"- **{name.replace('_', ' ')}:** {count} target roles")
	lines.extend(
		[
			"",
			"## Production implications",
			"",
			"1. Silhouette and composition are judged before surface detail. A painted texture cannot rescue primitive focal geometry.",
			"2. Repeated families require multiple asymmetric profiles and mass-placement captures; one attractive close-up is insufficient.",
			"3. Materials use broad pastel color blocks, indigo outline shells, and matte-to-satin response. Avoid glossy plastic, black shadows, and white clipping.",
			"4. Creatures must pass explicit anatomy checks. Butterflies need four separable wings; beetles need six legs and three readable body masses.",
			"5. Reusable assets cannot bake ground islands, mixed biomes, cast shadows, or unrelated props into one texture or mesh.",
			"6. Functional pieces remain separate when gameplay manipulates them: gates, ornaments, music bars, bells, and vehicle track signals.",
			"7. Every candidate requires near, mid, gameplay-distance, repetition, reverse-angle, and Mobile-renderer evidence before owner review.",
			"8. Orphans, duplicate extraction textures, corrupt provenance images, and unmerged material exports fail the pack even when they look acceptable.",
			"",
			"## Exclusions retained in the ledger",
			"",
		]
	)
	for row in exclusions:
		lines.append(f"- `{row['role_id']}` - {row['area']} / {row['runtime_role']}: {row['disposition']}")
	lines.extend(
		[
			"",
			"## Next evidence update",
			"",
			"After generation and stress testing, this report will gain post-pass failure",
			"counts, rejected-iteration reasons, structural metrics, and links to the full",
			"near/mid/gameplay contact sheets. No role becomes 5/5 until owner acceptance.",
			"",
		]
	)
	REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
	rows = build_rows()
	write_ledger(rows)
	summary = write_summary(rows)
	write_report(rows, summary)
	print(
		f"Frozen {summary['source_role_count']} roles: "
		f"{summary['regeneration_target_count']} targets, "
		f"{summary['protected_or_manual_exclusion_count']} exclusions."
	)


if __name__ == "__main__":
	main()
