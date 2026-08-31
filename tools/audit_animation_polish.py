#!/usr/bin/env python3
"""Animation-improvement wing gate (design 06 §20, DL-ANIM-*).

Two deterministic checks:

1. The shared feedback vocabulary (scripts/juice.gd) keeps its child-safe
   bounds: the wing constants exist and stay inside hard limits, every
   animated primitive guards `is_inside_tree()`, every scale-writing
   primitive uses the remembered-rest-scale discipline, and the default
   timings sit inside [MIN_DUR, MAX_DUR] with pulse cycles no faster than
   MIN_PULSE_PERIOD.

2. The wing's accepted exemplars stay wired. They are the reference
   implementations future work is measured against ("similar to previous
   work" is enforceable only against named previous work), so silently
   removing one un-teaches the pattern.

Exit 1 on any failure, ANIMPOLISH|... report lines either way.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
JUICE = "scripts/juice.gd"

# Hard limits the vocabulary constants must stay inside. These are the
# checker's own floor/ceiling — juice.gd may tighten them, never widen.
DUR_FLOOR_RANGE = (0.03, 0.10)
DUR_CEIL_RANGE = (0.5, 2.0)
PULSE_PERIOD_MIN = 0.30
PULSE_PEAK_MAX = 1.35

# Primitives that animate a node and must carry the in-tree guard; the
# subset that writes `scale` must also touch a juice_rest_scale meta.
ANIMATED_FUNCS = ("squash", "flash", "shake", "pop_in", "pulse3d", "vanish3d")
SCALE_FUNCS = ("squash", "pop_in", "pulse3d", "vanish3d")

# The wing's accepted exemplars: (file, required fragment, what it teaches).
EXEMPLARS = (
	("scripts/medal_system.gd", "Juice.pop_in(",
		"HUD entrance pattern on the medal celebration card"),
	("scripts/stuffie_battle.gd", "Juice.pulse3d(",
		"telegraph loop with rest-scale hygiene on the QTE"),
	("scripts/main.gd", "Juice.vanish3d(",
		"pickup payoff on the pearl path"),
	("scripts/main.gd", "_sparkle_mats",
		"cached burst material (no per-call material creation)"),
	("scripts/games/fairy.gd", "pow(1.0 - f, 3.0)",
		"eased in-place curve instead of a tween fighting per-frame math"),
)


def _const_float(text: str, name: str) -> float | None:
	match = re.search(rf"^const {name} := ([0-9.]+)$", text, re.MULTILINE)
	return float(match.group(1)) if match else None


def _func_bodies(text: str) -> dict[str, str]:
	"""Map each static func name to its signature+body text."""
	bodies: dict[str, str] = {}
	matches = list(re.finditer(r"^static func (\w+)\(", text, re.MULTILINE))
	for index, match in enumerate(matches):
		end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
		bodies[match.group(1)] = text[match.start():end]
	return bodies


def validate_vocabulary(text: str) -> list[str]:
	errors: list[str] = []
	min_dur = _const_float(text, "MIN_DUR")
	max_dur = _const_float(text, "MAX_DUR")
	min_period = _const_float(text, "MIN_PULSE_PERIOD")
	if min_dur is None or not (DUR_FLOOR_RANGE[0] <= min_dur <= DUR_FLOOR_RANGE[1]):
		errors.append(f"MIN_DUR missing or outside {DUR_FLOOR_RANGE}: {min_dur}")
	if max_dur is None or not (DUR_CEIL_RANGE[0] <= max_dur <= DUR_CEIL_RANGE[1]):
		errors.append(f"MAX_DUR missing or outside {DUR_CEIL_RANGE}: {max_dur}")
	if min_period is None or min_period < PULSE_PERIOD_MIN:
		errors.append(
			f"MIN_PULSE_PERIOD missing or under {PULSE_PERIOD_MIN}: {min_period}")
	bodies = _func_bodies(text)
	for name in ANIMATED_FUNCS:
		body = bodies.get(name)
		if body is None:
			errors.append(f"primitive {name}() is missing from {JUICE}")
			continue
		if "is_inside_tree()" not in body:
			errors.append(f"{name}() lost its is_inside_tree() guard")
		if name in SCALE_FUNCS and "juice_rest_scale" not in body:
			errors.append(f"{name}() writes scale without the rest-scale meta")
	if min_dur is None or max_dur is None:
		return errors
	for name, key in (("pop_in", "dur"), ("vanish3d", "dur"), ("pulse3d", "half")):
		body = bodies.get(name, "")
		match = re.search(rf"{key}: float = ([0-9.]+)", body)
		if match is None:
			errors.append(f"{name}() has no float default for {key}")
			continue
		value = float(match.group(1))
		if key == "half":
			if value * 2.0 < (min_period or PULSE_PERIOD_MIN):
				errors.append(
					f"pulse3d() default cycle {value * 2.0:.2f}s is under MIN_PULSE_PERIOD")
		elif not (min_dur <= value <= max_dur):
			errors.append(f"{name}() default {key}={value} outside [MIN_DUR, MAX_DUR]")
	peak = re.search(r"peak: float = ([0-9.]+)", bodies.get("pulse3d", ""))
	if peak is None or float(peak.group(1)) > PULSE_PEAK_MAX:
		errors.append(
			f"pulse3d() default peak missing or over {PULSE_PEAK_MAX} (gentle-motion bound)")
	return errors


def validate_exemplars(repo: pathlib.Path) -> list[str]:
	errors: list[str] = []
	for rel_path, fragment, teaches in EXEMPLARS:
		path = repo / rel_path
		if not path.is_file():
			errors.append(f"exemplar file missing: {rel_path}")
			continue
		if fragment not in path.read_text(encoding="utf-8"):
			errors.append(
				f"exemplar unwired: {rel_path} no longer contains {fragment!r} ({teaches})")
	return errors


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.parse_args(argv)
	juice_path = REPO / JUICE
	if not juice_path.is_file():
		print(f"ANIMPOLISH|FAIL|{JUICE} is missing")
		return 1
	errors = validate_vocabulary(juice_path.read_text(encoding="utf-8"))
	errors.extend(validate_exemplars(REPO))
	if errors:
		for error in errors:
			print(f"ANIMPOLISH|FAIL|{error}")
		return 1
	print(f"ANIMPOLISH|ALL OK|{len(ANIMATED_FUNCS)} primitives|{len(EXEMPLARS)} exemplars")
	return 0


if __name__ == "__main__":
	sys.exit(main())
