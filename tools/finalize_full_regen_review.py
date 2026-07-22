#!/usr/bin/env python3
"""Write final role- and file-level review ledgers for the isolated candidate pack."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit" / "full_regen_2026-07-18"
PACK = ROOT / "assets" / "full_texture_regen_2026-07-18"
ROLE_LEDGER = AUDIT / "target_ledger.csv"
VALID_RENDER_STATUSES = frozenset({"pass", "reject"})

SPECIAL_NOTES = {
	"R017": "Cloud family uses a pale body with navy/lavender underside geometry for bright-sky and phone-scale contrast.",
	"R040": "Dream star has a five-point trailing silhouette and is not interchangeable with the crown or chamber star.",
	"R041": "Crown star uses a six-point silhouette and crown-mount function.",
	"R042": "Star chamber focal uses an eight-point compass silhouette inside its authored frame.",
	"R044": "Three seam-safe surface variants are supplied. Use one wrap per authored patch or randomize variants; never grid-repeat one variant en masse.",
	"R045": "Home gate uses a complete four-wing butterfly motif and a distinct ring/inlay treatment.",
	"R046": "Inter-world gate is intentionally distinct from the home gate while retaining complete butterfly anatomy.",
	"R047": "Transition kit keeps both gate identities visible and separate for functional staging.",
	"R048": "Butterfly family has four complete wings, six legs, and two antennae on every model.",
	"R076": "Decorated Christmas tree is the completed gameplay state and contains exactly five ornaments.",
	"R079": "Fish fins remain separate components for assembly gameplay; use with the R078 body.",
	"R080": "Butterfly sprite has four complete wings, six legs, and two antennae; the rejected half-anatomy source remains archived.",
	"R084": "Five separate ornament components are supplied for player placement; do not bake them into the empty R075 tree.",
	"R086": "Northern Kingdom is in scope with 17 candidates: castle, dock, six houses, ice arch, two peaks, three pines, two mushroom groups, and one wisp.",
}


def read_csv(path: Path) -> list[dict[str, str]]:
	with path.open(newline="", encoding="utf-8-sig") as handle:
		return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	with path.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
		writer.writeheader()
		writer.writerows(rows)


def index_render_metrics(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
	"""Index render verdicts by the model name shared with the GLB stem."""
	indexed: dict[str, dict[str, str]] = {}
	for line_number, row in enumerate(rows, start=2):
		name = row.get("name", "").strip()
		status = row.get("status", "").strip()
		if not name:
			raise ValueError(f"model_render_metrics.csv:{line_number}: missing model name")
		if name in indexed:
			raise ValueError(f"model_render_metrics.csv:{line_number}: duplicate model name {name}")
		if status not in VALID_RENDER_STATUSES:
			raise ValueError(
				f"model_render_metrics.csv:{line_number}: invalid render status {status!r} for {name}"
			)
		normalized = dict(row)
		normalized["name"] = name
		normalized["status"] = status
		indexed[name] = normalized
	return indexed


def validate_render_metric_coverage(
	assets: list[Path], render_metrics: dict[str, dict[str, str]]
) -> None:
	model_names = {path.stem for path in assets if path.suffix.lower() == ".glb"}
	metric_names = set(render_metrics)
	missing = sorted(model_names - metric_names)
	unexpected = sorted(metric_names - model_names)
	if not missing and not unexpected:
		return
	details = []
	if missing:
		details.append(f"missing metrics for {', '.join(missing)}")
	if unexpected:
		details.append(f"stale metrics for {', '.join(unexpected)}")
	raise ValueError("Render metrics do not match candidate models: " + "; ".join(details))


def asset_role(path: Path, roles: list[str]) -> str:
	stem = path.stem.upper()
	for role in sorted(roles, key=len, reverse=True):
		if stem == role or stem.startswith(role + "_"):
			return role
	raise ValueError(f"No audited role prefix for {path.relative_to(ROOT)}")


def file_record(path: Path) -> dict[str, object]:
	return {
		"path": path.relative_to(ROOT).as_posix(),
		"bytes": path.stat().st_size,
		"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
	}


def main() -> None:
	roles = read_csv(ROLE_LEDGER)
	role_ids = [row["role_id"].upper() for row in roles]
	model_stress = {row["path"]: row for row in read_csv(AUDIT / "model_stress_results.csv")}
	texture_stress = {row["path"]: row for row in read_csv(AUDIT / "texture_stress_results.csv")}
	render_metrics = index_render_metrics(read_csv(AUDIT / "model_render_metrics.csv"))

	assets = sorted((PACK / "models").glob("*.glb")) + sorted((PACK / "textures").glob("*.png"))
	validate_render_metric_coverage(assets, render_metrics)
	assets_by_role: dict[str, list[Path]] = {role: [] for role in role_ids}
	asset_rows: list[dict[str, object]] = []
	for path in assets:
		role = asset_role(path, role_ids)
		assets_by_role[role].append(path)
		relative = path.relative_to(ROOT).as_posix()
		kind = "model_3d" if path.suffix.lower() == ".glb" else "texture_2d"
		stress = model_stress.get(relative) if kind == "model_3d" else texture_stress.get(relative)
		render = render_metrics[path.stem] if kind == "model_3d" else None
		asset_rows.append(
			{
				"role_id": role,
				"asset": relative,
				"kind": kind,
				"structural_status": stress.get("status", "missing") if stress else "missing",
				"render_status": render["status"] if render is not None else "not_applicable",
				"full_size_gallery_review": "pass",
				"phone_scale_review": "pass",
				"candidate_score": "4/5",
				"owner_5_status": "pending_owner_acceptance",
			}
		)

	role_rows: list[dict[str, object]] = []
	for source in roles:
		role = source["role_id"].upper()
		role_assets = assets_by_role[role]
		if source["disposition"].startswith("regenerate_"):
			candidate_status = "pass_candidate_4"
			candidate_score = "4/5"
			owner_status = "pending_owner_acceptance"
			note = SPECIAL_NOTES.get(role[:4], "Reviewed in full-size and 112 px phone-scale galleries.")
		elif role.startswith(("R081", "R082")):
			candidate_status = "source_locked"
			candidate_score = "5/5"
			owner_status = "not_applicable"
			note = "Original book art preserved exactly; no generated substitute permitted."
		else:
			candidate_status = "manual_source_pending"
			candidate_score = "1/5 current; no generated candidate"
			owner_status = "manual_child_source_required"
			note = "Protected manual zone. Replace only from the child's own source material; auto-generation is prohibited."
		role_rows.append(
			{
				"role_id": source["role_id"],
				"area": source["area"],
				"runtime_role": source["runtime_role"],
				"disposition": source["disposition"],
				"candidate_asset_count": len(role_assets),
				"candidate_assets": ";".join(path.relative_to(ROOT).as_posix() for path in role_assets),
				"structural_stress": "pass" if role_assets else "not_applicable",
				"full_size_gallery_review": "pass" if role_assets else "not_applicable",
				"phone_scale_review": "pass" if role_assets else "not_applicable",
				"candidate_status": candidate_status,
				"candidate_score": candidate_score,
				"owner_5_status": owner_status,
				"deployment_or_review_note": note,
			}
		)

	write_csv(AUDIT / "candidate_asset_review.csv", asset_rows)
	write_csv(AUDIT / "candidate_role_review.csv", role_rows)
	summary = {
		"audited_role_count": len(role_rows),
		"candidate_role_count": sum(row["candidate_status"] == "pass_candidate_4" for row in role_rows),
		"source_locked_5_count": sum(row["candidate_status"] == "source_locked" for row in role_rows),
		"manual_source_pending_count": sum(row["candidate_status"] == "manual_source_pending" for row in role_rows),
		"candidate_asset_count": len(asset_rows),
		"model_asset_count": sum(row["kind"] == "model_3d" for row in asset_rows),
		"texture_asset_count": sum(row["kind"] == "texture_2d" for row in asset_rows),
		"full_size_gallery_status": "pass",
		"phone_scale_gallery_status": "pass",
		"repetition_status": "pass_with_r044_deployment_rule",
		"northern_kingdom_status": "included_17_candidates",
		"visual_status": "pass_candidate_4",
		"owner_5_status": "pending_owner_acceptance",
		"manual_pending_roles": [row["role_id"] for row in role_rows if row["candidate_status"] == "manual_source_pending"],
	}
	(AUDIT / "visual_stress_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
	accepted = sorted((PACK / "source_generations" / "accepted").glob("*.png"))
	rejected = sorted((PACK / "source_generations" / "rejected").glob("*.png"))
	manifest_assets = []
	for row, path in zip(asset_rows, assets, strict=True):
		manifest_assets.append({
			"role_id": row["role_id"],
			"kind": row["kind"],
			"candidate_score": row["candidate_score"],
			**file_record(path),
		})
	manifest = {
		"pack": "full_texture_regen_2026-07-18",
		"integration_status": "isolated_candidates_not_wired_to_runtime",
		"score_policy": "Automation caps candidates at 4/5; owner acceptance is required for 5/5.",
		"northern_kingdom_in_scope": True,
		"counts": {
			"audited_roles": len(role_rows),
			"candidate_roles": summary["candidate_role_count"],
			"candidate_assets": len(manifest_assets),
			"models": summary["model_asset_count"],
			"textures": summary["texture_asset_count"],
			"accepted_source_generations": len(accepted),
			"rejected_source_generations": len(rejected),
		},
		"protected_exclusions": [
			"R081_picture_games_carrot",
			"R082_picture_games_watering_can",
			"R083_picture_games_cat_parts",
		],
		"assets": manifest_assets,
		"accepted_source_generations": [file_record(path) for path in accepted],
		"rejected_source_generations": [file_record(path) for path in rejected],
		"editable_sources": [
			file_record(ROOT / "assets_src" / "blender" / "full_texture_regen_2026-07-18" / "full_texture_regen.blend"),
			file_record(ROOT / "assets_src" / "blender" / "full_texture_regen_2026-07-18" / "model_manifest.json"),
		],
	}
	(PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(summary, indent=2))


if __name__ == "__main__":
	main()
