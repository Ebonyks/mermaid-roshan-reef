#!/usr/bin/env python3
"""Rebuild the deterministic Day One Parler trial ledger from intact WAVs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "audit" / "DAY_ONE_CONTEXTUAL_VOICE_COVERAGE_2026-09-01.json"
DEFAULT_TRIALS = ROOT / "tmp" / "day_one_contextual_parler_trials"
WAV_RE = re.compile(r"^(?P<key>[a-z0-9_]+)__attempt_(?P<attempt>[0-9]+)\.wav$")


def load_generator():
	spec = importlib.util.spec_from_file_location(
		"day_one_make_parler_voice_trials", ROOT / "tools" / "make_parler_voice_trials.py")
	if spec is None or spec.loader is None:
		raise RuntimeError("could not load tools/make_parler_voice_trials.py")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def rebuild(catalog_path: Path, trials: Path, profile: str,
		elevated_from: int | None = None) -> list[dict[str, object]]:
	document = json.loads(catalog_path.read_text(encoding="utf-8"))
	rows = {
		str(row["cue_id"]): str(row["caption"])
		for row in document.get("rows", [])
		if row.get("status") == "PENDING_GENERATION"
	}
	if not rows:
		raise ValueError("contextual catalog has no pending rows")
	generator = load_generator()
	manifest: list[dict[str, object]] = []
	for wav_path in sorted(trials.glob("*.wav")):
		match = WAV_RE.fullmatch(wav_path.name)
		if match is None:
			continue
		key = match.group("key")
		if key not in rows:
			raise ValueError(f"trial WAV key is outside the contextual catalog: {key}")
		attempt = int(match.group("attempt"))
		row_profile = "elevated" if elevated_from is not None and attempt >= elevated_from else profile
		text = rows[key]
		mood = generator.mood_for(key, text)
		description = generator.description_for("roshan", mood, text, row_profile)
		spoken_text = generator.KEY_SPOKEN_TEXT.get(key, generator.spoken_text_for(text))
		segments = generator.KEY_SPOKEN_SEGMENTS.get(key, [spoken_text])
		seed = generator.seed_for(key, attempt)
		segment_seeds = [
			(seed + index * 104729) & 0x7FFFFFFF
			for index in range(len(segments))
		]
		manifest.append({
			"key": key,
			"character": "roshan",
			"text": text,
			"generation_text": spoken_text,
			"generation_segments": segments,
			"segment_seeds": segment_seeds,
			"mood": mood,
			"speaker": generator.SPEAKERS["roshan"],
			"description": description,
			"roshan_register_profile": row_profile,
			"seed": seed,
			"attempt": attempt,
			"raw_path": str(wav_path.resolve()),
			"raw_sha256": hashlib.sha256(wav_path.read_bytes()).hexdigest(),
			"model": generator.MODEL_ID,
			"model_revision": generator.MODEL_REVISION,
			"description_tokenizer_revision": generator.DESCRIPTION_TOKENIZER_REVISION,
		})
	covered = {str(row["key"]) for row in manifest}
	missing = sorted(set(rows) - covered)
	if missing:
		raise ValueError("missing contextual trial WAVs: " + ", ".join(missing))
	return manifest


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
	parser.add_argument("--trials", type=Path, default=DEFAULT_TRIALS)
	parser.add_argument("--roshan-register-profile", default="baseline")
	parser.add_argument("--elevated-from", type=int)
	args = parser.parse_args()
	manifest = rebuild(args.catalog, args.trials, args.roshan_register_profile,
		args.elevated_from)
	output = args.trials / "trial_manifest.json"
	output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
	print(f"DAY_ONE_CONTEXTUAL|TRIAL_MANIFEST_REBUILT|rows={len(manifest)}|{output}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
