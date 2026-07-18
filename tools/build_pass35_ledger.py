#!/usr/bin/env python3
"""Build the exhaustive pass-35 ledger from the prior 88-role human audit."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "audit" / "human_art_ledger_2026-07-16.csv"
OUTPUT = ROOT / "audit" / "game_art_ledger_pass35_2026-07-16.csv"

SCORES = {
	"Reef": {
		"hub overall": 2.5, "portal presentation": 3.0, "coral mass placement": 3.5,
		"kelp cards": 3.5, "seagrass cards": 3.5, "rock family": 3.5,
		"caustic ground treatment": 2.5, "backdrop seamounts": 2.5,
		"coral flower hybrid": 4.0, "clownfish model": 4.0, "octopus model": 4.0,
		"shrimp role": 4.0, "jellyfish role": 4.0,
	},
	"Sky Lagoon": {
		"world composition": 3.0, "main castle": 4.0, "castle towers": 4.0,
		"cloud family": 4.0, "rainbow route": 3.5, "snow terrain": 3.0,
		"painting displays": 3.5, "train presentation": 3.0, "palm repetition": 3.5,
	},
	"Castle": {
		"castle hall overall": 3.0, "wall modules": 3.0, "stairs": 3.0,
		"columns": 3.0, "doors": 3.0, "throne room presentation": 3.0,
		"throne model": 3.5, "bed model": 4.0, "kitchen room": 4.0,
		"kitchen counter texture": 3.5, "kitchen floor texture": 4.0,
		"kitchen wood texture": 4.0, "kitchen stove": 4.0, "kitchen kettle": 4.0,
		"kitchen pans": 4.0, "kitchen teapot": 4.0, "kitchen table and stools": 4.0,
	},
	"Stars": {
		"dream star": 4.0, "crown star": 4.0, "star chamber focal": 4.0,
	},
	"Butterfly World": {
		"world overall": 2.5, "planet surface": 2.5, "home gate": 4.0,
		"inter-world gate": 4.0, "gate transition composition": 4.0,
		"butterfly environment family": 4.0,
	},
	"Dungeon": {
		"combat arena overall": 4.0, "arena floor": 4.0, "arena walls": 4.0,
		"standard enemies": 4.0, "boss": 4.0, "pepper projectile": 4.0,
		"basket": 4.0, "puzzle room overall": 4.0, "puzzle door": 4.0,
		"crystal pads": 4.0, "puzzle crystals": 4.0, "torch family": 4.0,
		"shell props": 4.0, "puzzle symbols": 4.0,
	},
	"Kart": {
		"kart world overall": 3.0, "vehicle selection pads": 4.0,
		"track barriers": 4.0, "boost ribbon": 3.5, "finish banner": 4.0,
		"coral dressing": 3.5, "gokart source": 3.0, "monster truck source": 3.0,
	},
	"Picture Games": {
		"coal": 4.0, "star": 4.0, "sun": 4.0, "tree": 4.0,
		"christmas tree": 4.0, "decorated christmas tree": 4.0, "bush": 4.0,
		"fish body": 4.0, "fish fins": 4.0, "butterfly": 4.0,
		"carrot": 5.0, "watering can": 5.0, "cat parts": 1.0,
		"ornament set": 4.0,
	},
	"Development": {
		"alpine interiors": 2.0, "northern kingdom additions": 3.0,
		"undersea additions": 3.5,
	},
	"Pipeline": {"generated provenance integrity": 2.0},
}

EVIDENCE = {
	"Reef": "pass35_reef.jpg; 01-09 runtime captures",
	"Sky Lagoon": "pass35_lagoon.jpg; 10-16 runtime captures",
	"Castle": "pass35_castle.jpg; 30-43 runtime captures",
	"Stars": "14, 32, and 43 runtime captures",
	"Butterfly World": "pass35_galaxy.jpg; 60-64 runtime captures",
	"Dungeon": "pass35_dungeon.jpg; all ten room captures; Blender projectile QA",
	"Kart": "pass35_picture_kart.jpg; 90-92 runtime captures",
	"Picture Games": "pass35_picture_kart.jpg; four live picture-game states",
	"Development": "17-23 northern captures plus repository branch inventory",
	"Pipeline": "isolated clean import and source-integrity review",
}


def status(row: dict[str, str], score: float) -> str:
	if row["runtime_role"] in {"carrot", "watering can"}:
		return "source_locked_5"
	if row["runtime_role"] == "cat parts":
		return "protected_manual_only"
	if score >= 4.0:
		return "4_candidate_owner_review"
	return "residual_below_4"


def action(row: dict[str, str], score: float) -> str:
	role = row["runtime_role"]
	if role == "coral flower hybrid":
		return "Removed mixed above-water/undersea role; replaced with habitat-specific modeled coral."
	if role in {"carrot", "watering can"}:
		return "Preserved byte-for-byte as book-source art."
	if role == "cat parts":
		return "No automatic generation; reserved for the child's own toy source."
	if score >= 4.0:
		return "Replacement integrated and verified in the Mobile runtime evidence set."
	return "Audited after replacement work; runtime composition remains below the 4/5 gate."


def main() -> None:
	with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
		rows = list(csv.DictReader(handle))
	missing = [
		f"{row['area']}::{row['runtime_role']}"
		for row in rows
		if row["area"] not in SCORES or row["runtime_role"] not in SCORES[row["area"]]
	]
	if missing:
		raise SystemExit("Missing pass-35 scores: " + ", ".join(missing))
	fields = list(rows[0]) + ["post_score", "post_status", "evidence", "pass35_action"]
	with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=fields)
		writer.writeheader()
		for row in rows:
			score = SCORES[row["area"]][row["runtime_role"]]
			row["post_score"] = f"{score:.1f}"
			row["post_status"] = status(row, score)
			row["evidence"] = EVIDENCE[row["area"]]
			row["pass35_action"] = action(row, score)
			writer.writerow(row)
	print(f"ART35_LEDGER|rows={len(rows)}|{OUTPUT}")


if __name__ == "__main__":
	main()
