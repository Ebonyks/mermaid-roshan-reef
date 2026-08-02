#!/usr/bin/env python3
"""Build the reproducible provenance, acceptance, and license manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


PACKAGE_REL = Path("assets_src/imagegen/imp_animation_states_2026-08-02")
CORE_STATES = ["windup", "charge", "slash", "recover", "guard", "stagger", "flee", "taunt"]
COSTUME_STATES = CORE_STATES + ["hop_a", "hop_b", "bopped", "bow"]
BASE_FAMILIES = ["imp_mischief", "imp_captain"]
COSTUME_FAMILIES = [
	"rival_chef", "rival_detective", "rival_ballerina", "rival_candymaker",
	"rival_doctor", "rival_farmer", "rival_boxer", "rival_magician",
	"rival_painter", "rival_astronaut", "rival_racer", "rival_popstar",
]
FX_SPECS = {
	"fx_telegraph_ring": (512, 512),
	"fx_telegraph_bang": (128, 256),
	"fx_slash_arc": (512, 256),
	"fx_dust_puff": (256, 256),
	"fx_stolen_sparkle": (128, 128),
	"fx_dizzy_stars": (256, 256),
}
FX_REFERENCES = {
	"fx_telegraph_ring": "assets/mg/star.png",
	"fx_telegraph_bang": f"{PACKAGE_REL.as_posix()}/candidates/fx_telegraph_ring_attempt01_chroma_native.png",
	"fx_slash_arc": f"{PACKAGE_REL.as_posix()}/candidates/fx_telegraph_ring_attempt01_chroma_native.png",
	"fx_dust_puff": "assets/opera/worlds/props/fx_bop_puff.png",
	"fx_stolen_sparkle": "assets/mg/star.png",
	"fx_dizzy_stars": "assets/mg/star.png",
}

# Repo-native copies of every ImageGen output. Prompt text lives in PROMPTS.md;
# this registry binds each copy to its tool execution ID and prompt key.
RUNS = {
	"imp_mischief_windup_attempt01_chroma_native.png": ("exec-2a1331a9-dad0-4e08-8da8-42fd17567894", "BASE_STATE_RECOVERED", "accepted", "windup"),
	"imp_mischief_charge_attempt01_chroma_native.png": ("exec-46db4db3-7402-479e-bc32-898da901847e", "BASE_STATE_RECOVERED", "accepted", "charge"),
	"imp_mischief_slash_attempt01_chroma_native.png": ("exec-182cac2a-b8a3-4d31-a199-4bd9a9e9d460", "BASE_STATE_RECOVERED", "accepted", "slash"),
	"imp_mischief_recover_attempt01_chroma_native.png": ("exec-a387619e-0e43-4e6b-9534-6ebbd9a01660", "BASE_STATE_RECOVERED", "accepted", "recover"),
	"imp_mischief_guard_attempt01_chroma_native.png": ("exec-b089c8f6-5ee8-4ee1-9ae0-1237ef632848", "BASE_STATE_RECOVERED", "accepted", "guard"),
	"imp_mischief_stagger_attempt01_chroma_native.png": ("exec-b2bfd5ef-ce7c-4a30-91da-cc001bc95e62", "BASE_STATE_RECOVERED", "accepted", "stagger"),
	"imp_mischief_flee_attempt01_chroma_native.png": ("exec-c9c30477-782d-4c33-aecf-dcfdc2357a90", "BASE_STATE_RECOVERED", "accepted", "flee"),
	"imp_mischief_taunt_attempt01_chroma_native.png": ("exec-ce396692-ed75-46ff-b28f-34b47975301e", "BASE_STATE_RECOVERED", "accepted", "taunt"),
	"imp_captain_windup_attempt01_chroma_native.png": ("exec-33b85b2a-d23c-4ae4-b146-a477fb29b322", "BASE_STATE_RECOVERED", "accepted", "windup"),
	"imp_captain_charge_attempt01_chroma_native.png": ("exec-11d49ba9-0d14-4ca8-a403-1c56be6d43db", "BASE_STATE_RECOVERED", "accepted", "charge"),
	"imp_captain_slash_attempt01_chroma_native.png": ("exec-ae79f6cc-c857-4511-9079-27d1fd3a1017", "BASE_STATE_RECOVERED", "accepted", "slash"),
	"imp_captain_recover_attempt01_chroma_native.png": ("exec-f0efb6a8-dff2-4319-b437-538b1235d80c", "BASE_STATE_RECOVERED", "accepted", "recover"),
	"imp_captain_guard_attempt01_chroma_native.png": ("exec-2f0accec-5651-4cae-9687-7a74ed87fb5a", "BASE_STATE_RECOVERED", "accepted", "guard"),
	"imp_captain_stagger_attempt01_chroma_native.png": ("exec-16f34aee-7339-4515-bc4d-d09c35d11cff", "BASE_STATE_RECOVERED", "accepted", "stagger"),
	"imp_captain_flee_attempt01_chroma_native.png": ("exec-0c5239e9-ce5d-48da-be3e-e5716d36e492", "BASE_STATE_RECOVERED", "accepted", "flee"),
	"imp_captain_taunt_attempt01_chroma_native.png": ("exec-158130fa-4466-4813-a8da-e39d6c0a4741", "BASE_STATE_RECOVERED", "accepted", "taunt"),
	"imp_captain_bow_attempt01_chroma_native.png": ("exec-746d0227-fe1e-47e5-9a24-167fae32a6f2", "BASE_BOW_RECOVERED", "accepted", "repaired captain bow"),
	"rival_chef_sheet_a_attempt01_chroma_native.png": ("exec-c5b9e53c-23d5-4385-8163-b38721acf3c3", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_chef_sheet_b_attempt01_chroma_native.png": ("exec-13955535-065b-45b5-b979-7d092583fcb0", "COSTUME_SHEET_B_RECOVERED", "accepted", "seven-pose sheet"),
	"rival_detective_sheet_a_attempt01_chroma_native.png": ("exec-35307032-1f7d-40f9-9646-9f57d5eca4ab", "COSTUME_SHEET_A_RECOVERED", "partially_accepted", "recover cell rejected"),
	"rival_detective_sheet_b_attempt01_chroma_native.png": ("exec-0439ce62-0b25-4508-af0f-9171dd549a4f", "COSTUME_SHEET_B_RECOVERED", "accepted", "seven-pose sheet"),
	"rival_detective_recover_attempt02_chroma_native.png": ("exec-9736e213-c287-49d7-aee0-494f14be702f", "SINGLE_REPAIR_RECOVERED", "accepted", "recover replacement"),
	"rival_ballerina_sheet_a_attempt01_chroma_native.png": ("exec-83d7bc4c-c3fb-4900-a0e3-cbd795d318ad", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_ballerina_sheet_b_attempt01_chroma_native.png": ("exec-07b3b887-3e39-4b4f-a0ce-820968a78fbd", "COSTUME_SHEET_B_RECOVERED", "partially_accepted", "flee cell rejected"),
	"rival_ballerina_flee_attempt02_chroma_native.png": ("exec-5a2989e8-71b3-49a9-8bd9-4ed9f3645582", "SINGLE_REPAIR_RECOVERED", "accepted", "flee replacement"),
	"rival_candymaker_sheet_a_attempt01_chroma_native.png": ("exec-7f61546d-357e-4ff8-af50-460e40f87d31", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_candymaker_sheet_b_attempt01_chroma_native.png": ("exec-b830d179-c4f4-4b1c-91ce-e159b095b467", "COSTUME_SHEET_B_RECOVERED", "accepted", "seven-pose sheet"),
	"rival_doctor_sheet_a_attempt01_chroma_native.png": ("exec-799307ef-03ec-4013-ac47-95be1dec79b9", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_doctor_sheet_b_attempt01_chroma_native.png": ("exec-267d750e-370a-41bb-80c4-abf49ed48da3", "COSTUME_SHEET_B_RECOVERED", "accepted", "seven-pose sheet"),
	"rival_farmer_sheet_a_attempt01_chroma_native.png": ("exec-c581bacc-6783-4283-97fa-74cf1bd79272", "COSTUME_SHEET_A_RECOVERED", "partially_accepted", "slash cell rejected"),
	"rival_farmer_sheet_b_attempt01_chroma_native.png": ("exec-e616f3c2-2e3c-4b8b-8c4f-8d4e8ceab9f3", "COSTUME_SHEET_B_RECOVERED", "partially_accepted", "bopped cell rejected"),
	"rival_farmer_slash_attempt02_chroma_native.png": ("exec-65806954-eec7-4d46-9bb6-b5dad894e28f", "SINGLE_REPAIR_RECOVERED", "accepted", "slash replacement"),
	"rival_farmer_bopped_attempt02_chroma_native.png": ("exec-1f7b7f80-b97e-4b56-86cd-da9540eef913", "SINGLE_REPAIR_RECOVERED", "accepted", "bopped replacement"),
	"rival_boxer_sheet_a_attempt01_chroma_native.png": ("exec-1dcd5c6d-91a6-40e5-9661-97320b625827", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_boxer_sheet_b_attempt01_chroma_native.png": ("exec-cdb696cb-5a39-46bc-af41-ec6ae6bc51ce", "COSTUME_SHEET_B_RECOVERED", "partially_accepted", "bopped cell rejected"),
	"rival_boxer_bopped_attempt02_chroma_native.png": ("exec-20e77be8-f617-43c7-81a9-6e943e7afe01", "SINGLE_REPAIR_RECOVERED", "accepted", "bopped replacement"),
	"rival_magician_sheet_a_attempt01_chroma_native.png": ("exec-3099de27-c496-497b-8b3a-12769e52ffba", "COSTUME_SHEET_A_RECOVERED", "partially_accepted", "charge cell rejected for detached shoe"),
	"rival_magician_sheet_b_attempt01_chroma_native.png": ("exec-118822bc-306e-4823-a7f3-fee1aa779b22", "COSTUME_SHEET_B_RECOVERED", "partially_accepted", "flee cell rejected"),
	"rival_magician_charge_attempt02_chroma_native.png": ("exec-420b9b01-5608-49e4-b4f5-a00b75dd570b", "SINGLE_REPAIR_RECOVERED", "accepted", "charge replacement"),
	"rival_magician_flee_attempt02_chroma_native.png": ("exec-edf4819f-c35c-47dc-b023-9c2625a1997d", "SINGLE_REPAIR_RECOVERED", "accepted", "flee replacement"),
	"rival_painter_sheet_a_attempt01_chroma_native.png": ("exec-08cd57be-f051-489a-b90f-fa1493cea9c5", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_painter_sheet_b_attempt01_chroma_native.png": ("exec-f18de025-9117-4d99-863f-9bbc32c8f6da", "COSTUME_SHEET_B_RECOVERED", "partially_accepted", "stagger, bopped, bow cells rejected"),
	"rival_painter_sheet_c_attempt01_chroma_native.png": ("exec-06d2d9f4-7cfe-4e3f-b108-1d4d60dc7f49", "REPAIR_SHEET_RECOVERED", "accepted", "stagger, bopped, bow replacements"),
	"rival_astronaut_sheet_a_attempt01_chroma_native.png": ("exec-ac162014-fea2-4de5-a6ec-58984dd48184", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_astronaut_sheet_b_attempt01_chroma_native.png": ("exec-da56aa8e-6b37-452d-b8bb-49f648a0a320", "COSTUME_SHEET_B_RECOVERED", "partially_accepted", "stagger, flee, bopped cells rejected"),
	"rival_astronaut_sheet_d_attempt01_chroma_native.png": ("exec-d1103e4a-7996-45e9-a359-3105f1e66c12", "REPAIR_SHEET_RECOVERED", "partially_accepted", "flee and bopped accepted; stagger replaced again"),
	"rival_astronaut_stagger_attempt02_chroma_native.png": ("exec-41542b65-eef0-405a-8aa0-2603f68c67f6", "SINGLE_REPAIR_RECOVERED", "accepted", "stagger replacement"),
	"rival_racer_sheet_a_attempt01_chroma_native.png": ("exec-573cd0e6-d8fc-41f5-8925-46d877e11179", "COSTUME_SHEET_A_RECOVERED", "accepted", "six-pose sheet"),
	"rival_racer_sheet_b_attempt01_chroma_native.png": ("exec-0fcfd3df-251f-44c7-95d3-c5befe54220e", "COSTUME_SHEET_B_RECOVERED", "accepted", "seven-pose sheet"),
	"rival_popstar_sheet_a_attempt01_chroma_native.png": ("exec-ff584d90-c285-460b-aee9-20c200663312", "POPSTAR_SHEET_A_EXACT", "accepted", "six-pose sheet"),
	"rival_popstar_sheet_b_attempt01_chroma_native.png": ("exec-a6cc4a80-5feb-4081-9945-c916c19c8d50", "POPSTAR_SHEET_B_EXACT", "accepted", "seven-pose sheet"),
	"fx_telegraph_ring_attempt01_chroma_native.png": ("exec-54a8719c-8e2f-4610-9aff-6a7f6cafcb35", "FX_RING_EXACT", "accepted", "telegraph ring"),
	"fx_telegraph_bang_attempt01_chroma_native.png": ("exec-d673f056-920c-4f77-a830-fe6625d3ae8a", "FX_BANG_EXACT", "accepted", "telegraph bang"),
	"fx_slash_arc_attempt01_rejected_checkerboard_native.png": ("exec-1799672d-9e6d-4cbe-b7c6-d3a8729cafa7", "FX_SLASH_TRANSPARENCY_REJECTED_EXACT", "rejected", "checkerboard baked into RGB output"),
	"fx_slash_arc_attempt02_chroma_native.png": ("exec-ca312304-544a-49b8-b88d-e426e750360f", "FX_SLASH_EXACT", "accepted", "slash arc"),
	"fx_dust_puff_attempt01_chroma_native.png": ("exec-3a9d9f66-5ec7-427f-a238-6464405f0b88", "FX_DUST_EXACT", "accepted", "dust puff"),
	"fx_dizzy_stars_attempt01_chroma_native.png": ("exec-745f5436-cfdd-4387-98c4-138f5b0e9a88", "FX_DIZZY_EXACT", "accepted", "dizzy stars"),
}


def hash_file(path: Path) -> str:
	hash_value = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			hash_value.update(chunk)
	return hash_value.hexdigest()


def normalized_key(name: str) -> str:
	for suffix in ("_chroma_native.png", "_alpha_native.png", "_alpha_crop_native.png"):
		if name.endswith(suffix):
			return name[:-len(suffix)]
	return Path(name).stem


def prompt_hashes(path: Path) -> dict[str, str]:
	sections: dict[str, list[str]] = {}
	current: str | None = None
	for line in path.read_text(encoding="utf-8").splitlines():
		if line.startswith("### `") and line.endswith("`"):
			current = line.removeprefix("### `").removesuffix("`")
			sections[current] = []
		elif line.startswith("## "):
			current = None
		elif current is not None:
			sections[current].append(line)
	hashes: dict[str, str] = {}
	for key, lines in sections.items():
		body = "\n".join(lines).strip() + "\n"
		hashes[key] = hashlib.sha256(body.encode("utf-8")).hexdigest()
	return hashes


def find_run(input_path: str) -> str | None:
	name = Path(input_path).name
	input_key = normalized_key(name)
	for candidate in RUNS:
		run_key = normalized_key(candidate)
		if input_key == run_key:
			return candidate
		if "_sheet_" in run_key:
			family, suffix = run_key.split("_sheet_", 1)
			if input_key.startswith(family + "_") and input_key.endswith("_sheet_" + suffix):
				return candidate
	return None


def expected_deliveries(root: Path) -> list[dict]:
	deliveries: list[dict] = []
	for family in BASE_FAMILIES:
		for state in CORE_STATES:
			deliveries.append({"stem": f"{family}_{state}", "family": family, "state": state, "kind": "actor"})
	deliveries.append({"stem": "imp_captain_bow", "family": "imp_captain", "state": "bow", "kind": "actor"})
	for family in COSTUME_FAMILIES:
		deliveries.append({"stem": family, "family": family, "state": "idle", "kind": "actor"})
		for state in COSTUME_STATES:
			deliveries.append({"stem": f"{family}_{state}", "family": family, "state": state, "kind": "actor"})
	for stem, dimensions in FX_SPECS.items():
		deliveries.append({"stem": stem, "family": "shared_fx", "state": stem.removeprefix("fx_"), "kind": "fx", "expected_canvas": list(dimensions)})
	return deliveries


def runtime_captures(package: Path, family: str, kind: str) -> list[str]:
	runtime = package / "runtime"
	paths = sorted(runtime.glob(f"{family}_page_*.png")) if kind == "actor" else sorted(runtime.glob("*_fx.png"))
	return [path.as_posix() for path in paths]


def visual_reference(root: Path, package: Path, expected: dict) -> tuple[str, str]:
	if expected["kind"] == "actor":
		path = package / "references" / f"{expected['family']}_source_idle.png"
	else:
		path = root / FX_REFERENCES[expected["stem"]]
	if not path.exists():
		raise FileNotFoundError(path)
	return path.relative_to(root).as_posix(), hash_file(path)


def license_row(record: dict) -> str:
	path = record["output"]
	if record["provenance_method"] == "approved_asset_reuse":
		source = "Non-destructive derivative of approved project art `assets/mg/star.png`"
		mods = "Uniform whole-star resize and transparent-canvas padding to 128x128; no generated pixels"
	else:
		source = "OpenAI built-in ImageGen using approved project imp/rival or FX style references"
		canvas = "x".join(str(value) for value in record["canvas"])
		mods = f"Accepted generated cutout; chroma removal, uniform whole-subject resize/placement and transparent padding to {canvas}; prompt, hashes and QA in the linked packet"
	return f"| {path} | {source} | **Project-generated © Mermaid Roshan LLC, all rights reserved** | {PACKAGE_REL.as_posix()}/PROMPTS.md | {mods} |"


def update_license_ledger(root: Path, records: list[dict]) -> None:
	ledger = root / "ASSET_LICENSES.md"
	text = ledger.read_text(encoding="utf-8")
	marker = "## Imp combat animation art (2026-08-02)"
	if marker in text:
		print("License section already present; left unchanged")
		return
	for record in records:
		if f"| {record['output']} |" in text:
			raise ValueError(f"license row already exists outside section: {record['output']}")
	lines = [
		"", marker, "",
		"One row per accepted runtime file; all native generations, prompt bindings, hashes, rejection notes, per-file acceptance reports, QA renders, and Mobile-renderer captures are retained in the linked source packet.",
		"", "| Path | Source | License | URL | Modifications |",
		"|---|---|---|---|---|",
	]
	lines.extend(license_row(record) for record in records)
	ledger.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--human-reviewed", action="store_true")
	parser.add_argument("--update-license-ledger", action="store_true")
	args = parser.parse_args()

	root = Path(__file__).resolve().parents[1]
	package = root / PACKAGE_REL
	candidates = package / "candidates"
	reports = package / "reports"
	prompt_path = package / "PROMPTS.md"
	prompt_hash_by_key = prompt_hashes(prompt_path)
	prompt_ledger_hash = hash_file(prompt_path)
	runs: list[dict] = []
	missing_runs: list[str] = []
	for candidate, (generation_id, prompt_key, status, note) in RUNS.items():
		path = candidates / candidate
		if not path.exists():
			missing_runs.append(candidate)
			continue
		with Image.open(path) as image:
			dimensions = list(image.size)
			mode = image.mode
		runs.append({
			"generation_id": generation_id,
			"generation_method": "OpenAI built-in ImageGen",
			"prompt_key": prompt_key,
			"prompt_sha256": prompt_hash_by_key[prompt_key],
			"status": status,
			"note": note,
			"native_copy": path.relative_to(root).as_posix(),
			"native_sha256": hash_file(path),
			"native_canvas": dimensions,
			"native_mode": mode,
		})
	(package / "GENERATION_RUNS.json").write_text(json.dumps({
		"schema": 1,
		"date": "2026-08-02",
		"prompt_ledger": (PACKAGE_REL / "PROMPTS.md").as_posix(),
		"prompt_ledger_sha256": prompt_ledger_hash,
		"missing_run_files": missing_runs,
		"runs": runs,
	}, indent=2) + "\n", encoding="utf-8")

	records: list[dict] = []
	errors: list[str] = []
	for expected in expected_deliveries(root):
		stem = expected["stem"]
		report_path = reports / f"{stem}.json"
		if not report_path.exists():
			errors.append(f"missing report: {report_path.relative_to(root)}")
			continue
		report = json.loads(report_path.read_text(encoding="utf-8"))
		if not report.get("pass", False):
			errors.append(f"failed report: {report_path.relative_to(root)}")
		output = root / Path(report["output"])
		if not output.exists():
			errors.append(f"missing output: {output.relative_to(root)}")
			continue
		actual_hash = hash_file(output)
		if actual_hash != report.get("output_sha256"):
			errors.append(f"output hash mismatch: {output.relative_to(root)}")
		with Image.open(output) as image:
			canvas = list(image.size)
			mode = image.mode
		if expected["kind"] == "actor" and canvas != [512, 512]:
			errors.append(f"actor canvas mismatch: {output.relative_to(root)} {canvas}")
		if expected["kind"] == "fx" and canvas != expected["expected_canvas"]:
			errors.append(f"FX canvas mismatch: {output.relative_to(root)} {canvas}")
		input_path = str(report.get("input", ""))
		run_candidate = find_run(input_path)
		if run_candidate is not None:
			generation_id, prompt_key, _status, _note = RUNS[run_candidate]
			provenance_method = "generated"
		elif input_path.replace("\\", "/").endswith("assets/mg/star.png"):
			generation_id = None
			prompt_key = "APPROVED_STAR_REUSE"
			provenance_method = "approved_asset_reuse"
		elif input_path.replace("\\", "/").endswith("_windup.png") and expected["state"] == "hop_a":
			generation_id = "same_as_accepted_windup"
			prompt_key = "APPROVED_WINDUP_REUSE"
			provenance_method = "approved_state_reuse"
		else:
			generation_id = None
			prompt_key = None
			provenance_method = "unresolved"
			errors.append(f"unresolved provenance: {stem} from {input_path}")
		captures = runtime_captures(package, expected["family"], expected["kind"])
		reference_path, reference_hash = visual_reference(root, package, expected)
		records.append({
			"timeline_or_state": expected["state"],
			"family": expected["family"],
			"kind": expected["kind"],
			"output": output.relative_to(root).as_posix(),
			"output_sha256": actual_hash,
			"canvas": canvas,
			"mode": mode,
			"source_input": input_path.replace("\\", "/"),
			"source_input_sha256": report.get("input_sha256"),
			"generation_id": generation_id,
			"prompt_key": prompt_key,
			"prompt_sha256": prompt_hash_by_key[prompt_key],
			"provenance_method": provenance_method,
			"visual_reference": reference_path,
			"visual_reference_sha256": reference_hash,
			"acceptance_report": report_path.relative_to(root).as_posix(),
			"acceptance_report_sha256": hash_file(report_path),
			"runtime_captures": captures,
			"mobile_renderer_review": "accepted" if args.human_reviewed and captures else "pending",
		})

	ship_ready = not errors and not missing_runs and all(record["runtime_captures"] for record in records) \
		and all(record["mobile_renderer_review"] == "accepted" for record in records)
	manifest = {
		"schema": 1,
		"date": "2026-08-02",
		"generation_method": "OpenAI built-in ImageGen plus declared non-destructive approved-art reuse",
		"prompt_ledger": (PACKAGE_REL / "PROMPTS.md").as_posix(),
		"prompt_ledger_sha256": prompt_ledger_hash,
		"generation_runs": (PACKAGE_REL / "GENERATION_RUNS.json").as_posix(),
		"expected_delivery_count": 179,
		"delivery_count": len(records),
		"static_acceptance_pass": not errors and not missing_runs and len(records) == 179,
		"mobile_review_complete": all(record["mobile_renderer_review"] == "accepted" for record in records),
		"ship_ready": ship_ready,
		"errors": errors + [f"missing native run copy: {name}" for name in missing_runs],
		"deliveries": records,
	}
	(package / "DELIVERY_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
	if args.update_license_ledger:
		update_license_ledger(root, records)
	print(json.dumps({key: manifest[key] for key in (
		"expected_delivery_count", "delivery_count", "static_acceptance_pass",
		"mobile_review_complete", "ship_ready", "errors")}, indent=2))
	return 0 if manifest["static_acceptance_pass"] else 1


if __name__ == "__main__":
	raise SystemExit(main())
