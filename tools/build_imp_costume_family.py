#!/usr/bin/env python3
"""Extract, normalize, and audit one two-sheet imp costume family."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


STATE_LAYOUT = {
	"idle": (485, 8, "a"),
	"windup": (410, 8, "a"),
	"charge": (420, 55, "a"),
	"slash": (485, 8, "a"),
	"recover": (445, 8, "a"),
	"guard": (488, 8, "a"),
	"stagger": (485, 8, "b"),
	"flee": (485, 8, "b"),
	"bopped": (410, 55, "b"),
	"bow": (400, 8, "b"),
	"hop_a": (410, 8, "b"),
	"hop_b": (430, 55, "b"),
	"taunt": (485, 8, "b"),
}


def run(command: list[str]) -> int:
	print("RUN", " ".join(command), flush=True)
	return subprocess.run(command, check=False).returncode


def main() -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument("--family", required=True)
	parser.add_argument("--sheet-a", type=Path, required=True)
	parser.add_argument("--sheet-b", type=Path, required=True)
	parser.add_argument("--reuse-windup-hop-a", action="store_true")
	args = parser.parse_args()

	root = Path(__file__).resolve().parents[1]
	package = root / "assets_src/imagegen/imp_animation_states_2026-08-02"
	candidates = package / "candidates"
	reports = package / "reports"
	qa = package / "qa"
	actors = root / "assets/opera/worlds/actors"
	extractor = root / "tools/extract_imp_animation_sheet.py"
	preparer = root / "tools/prepare_imp_animation_sprite.py"
	results: dict[str, int] = {}

	for sheet, source in (("a", args.sheet_a), ("b", args.sheet_b)):
		results[f"extract_{sheet}"] = run([
			sys.executable, str(extractor),
			"--input", str(source),
			"--family", args.family,
			"--sheet", sheet,
			"--candidates-dir", str(candidates),
			"--report", str(reports / f"{args.family}_sheet_{sheet}_extraction.json"),
		])
	if results["extract_a"] or results["extract_b"]:
		return 1

	idle_output = actors / f"{args.family}.png"
	for state, (height, gap, sheet) in STATE_LAYOUT.items():
		stem = args.family if state == "idle" else f"{args.family}_{state}"
		input_path = candidates / f"{stem}_sheet_{sheet}_attempt01_alpha_crop_native.png"
		if state == "hop_a" and args.reuse_windup_hop_a:
			input_path = actors / f"{args.family}_windup.png"
		output = actors / f"{stem}.png"
		results[state] = run([
			sys.executable, str(preparer),
			"--input", str(input_path),
			"--output", str(output),
			"--idle", str(idle_output),
			"--state", state,
			"--target-height", str(height),
			"--bottom-gap", str(gap),
			"--allow-large-holes", "5",
			"--harden-alpha",
			"--report", str(reports / f"{stem}.json"),
			"--qa-dir", str(qa / stem),
		])

	summary = {
		"family": args.family,
		"sheet_a": str(args.sheet_a),
		"sheet_b": str(args.sheet_b),
		"reuse_windup_hop_a": args.reuse_windup_hop_a,
		"results": results,
		"pass": all(code == 0 for code in results.values()),
	}
	summary_path = reports / f"{args.family}_family_build.json"
	summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(summary, indent=2))
	return 0 if summary["pass"] else 1


if __name__ == "__main__":
	raise SystemExit(main())
