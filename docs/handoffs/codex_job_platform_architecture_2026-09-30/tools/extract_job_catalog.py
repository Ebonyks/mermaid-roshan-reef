#!/usr/bin/env python3
"""Prototype extractor: rebuild per-job records from today's code registries.

Read-only. Run from the repository root:

    python -B <packet>/tools/extract_job_catalog.py --out <packet>/data

where <packet> is docs/handoffs/codex_job_platform_architecture_2026-09-30.

It parses the GDScript constants that describe Opera careers today, joins them
into one record per job, recomputes every mask, count, loop bound and clamp
from those records, and compares each derived value with the literal the code
hard-codes. It writes two JSON files and prints a summary. It changes nothing.

This is evidence for the architecture's claim that a single job catalogue can
regenerate the scattered registries (Codex package JP0 replaces it with the
real round-trip extractor and generator).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

BS = chr(92)  # backslash, kept out of literals on purpose


class GDParser:
	"""Minimal reader for GDScript constant literals (dicts, arrays, strings,
	numbers, booleans, calls such as Color(...), identifiers). Anything it does
	not understand is kept as {"__raw__": text} rather than guessed."""

	def __init__(self, text: str, start: int) -> None:
		self.s = text
		self.i = start

	def ws(self) -> None:
		while self.i < len(self.s):
			c = self.s[self.i]
			if c in " \t\r\n":
				self.i += 1
			elif c == "#":
				while self.i < len(self.s) and self.s[self.i] != "\n":
					self.i += 1
			else:
				break

	def peek(self) -> str:
		self.ws()
		return self.s[self.i] if self.i < len(self.s) else ""

	def value(self):
		c = self.peek()
		if c == "{":
			return self.dict_()
		if c == "[":
			return self.list_()
		if c in "\"'":
			return self.string()
		if c == "&" and self.s[self.i + 1:self.i + 2] in "\"'":
			self.i += 1
			return self.string()
		if c.isdigit() or c == "-" or c == ".":
			return self.number()
		if c.isalpha() or c == "_":
			ident = self.ident()
			if ident == "true":
				return True
			if ident == "false":
				return False
			if ident == "null":
				return None
			if self.peek() == "(":
				return {"__call__": ident, "args": self.args()}
			return {"__ident__": ident}
		return {"__raw__": self.raw()}

	def ident(self) -> str:
		m = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*").match(self.s, self.i)
		self.i = m.end()
		return m.group(0)

	def args(self) -> list:
		self.i += 1  # (
		out = []
		while True:
			c = self.peek()
			if c == ")":
				self.i += 1
				return out
			out.append(self.value())
			if self.peek() == ",":
				self.i += 1

	def string(self) -> str:
		quote = self.s[self.i]
		self.i += 1
		out = []
		while self.i < len(self.s):
			c = self.s[self.i]
			if c == BS:
				out.append(self.s[self.i + 1])
				self.i += 2
				continue
			if c == quote:
				self.i += 1
				return "".join(out)
			out.append(c)
			self.i += 1
		raise ValueError("unterminated string")

	def number(self):
		m = re.compile(r"-?(0x[0-9A-Fa-f_]+|\d[\d_]*(\.\d+)?([eE][-+]?\d+)?|\.\d+)").match(self.s, self.i)
		self.i = m.end()
		text = m.group(0).replace("_", "")
		if "0x" in text:
			return int(text, 16)
		return float(text) if any(ch in text for ch in ".eE") else int(text)

	def raw(self) -> str:
		depth = 0
		start = self.i
		while self.i < len(self.s):
			c = self.s[self.i]
			if c in "([{":
				depth += 1
			elif c in ")]}":
				if depth == 0:
					break
				depth -= 1
			elif c in ",\n" and depth == 0:
				break
			self.i += 1
		return self.s[start:self.i].strip()

	def dict_(self) -> dict:
		self.i += 1
		out = {}
		while True:
			if self.peek() == "}":
				self.i += 1
				return out
			key = self.value()
			if self.peek() in ":=":
				self.i += 1
			val = self.value()
			out[key if isinstance(key, (str, int, float, bool)) else json.dumps(key)] = val
			if self.peek() == ",":
				self.i += 1

	def list_(self) -> list:
		self.i += 1
		out = []
		while True:
			if self.peek() == "]":
				self.i += 1
				return out
			out.append(self.value())
			if self.peek() == ",":
				self.i += 1


def const(path: str, name: str):
	text = Path(path).read_text(encoding="utf-8")
	m = re.search(r"(?m)^const\s+" + re.escape(name) + r"\b[^=\n]*=", text)
	if m is None:
		return None
	return GDParser(text, m.end()).value()


def literal_ints(path: str, pattern: str) -> list[int]:
	text = Path(path).read_text(encoding="utf-8")
	return [int(x, 0) for x in re.findall(pattern, text)]


def star_clamps(path: str) -> list[int]:
	"""Upper bound of every clampi(...) call that clamps opera_stars, however it wraps."""
	text = Path(path).read_text(encoding="utf-8")
	bounds = []
	for m in re.finditer(r"clampi\(", text):
		depth, j = 1, m.end()
		while depth and j < len(text):
			depth += {"(": 1, ")": -1}.get(text[j], 0)
			j += 1
		call = text[m.start():j]
		if "opera_stars" in call:
			bounds.append(int(re.findall(r"(\d+)\s*\)\s*$", call)[0]))
	return bounds


def py_list(path: str, name: str) -> list[str]:
	text = Path(path).read_text(encoding="utf-8")
	m = re.search(r"(?m)^" + re.escape(name) + r"\b[^=\n]*=\s*[\[(]", text)
	if m is None:
		return []
	depth, j = 1, m.end()
	while depth and j < len(text):
		depth += {"[": 1, "(": 1, "]": -1, ")": -1}.get(text[j], 0)
		j += 1
	return re.findall(r"[\"']([^\"']+)[\"']", text[m.end():j])


def color(v):
	if isinstance(v, dict) and v.get("__call__") == "Color":
		return v["args"]
	return v


def main() -> int:
	ap = argparse.ArgumentParser(description=__doc__)
	ap.add_argument("--out", required=True)
	args = ap.parse_args()
	out = Path(args.out)
	out.mkdir(parents=True, exist_ok=True)
	head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()

	acts = const("scripts/opera_house.gd", "ACTS")
	live_literal = const("scripts/opera_house.gd", "LIVE_ACT_INDICES")
	retired_literal = const("scripts/opera_house.gd", "RETIRED_ACT_INDICES")
	rooms = const("scripts/castle_career_routes.gd", "ROOM_ACT_INDICES")
	crests = const("scripts/castle_career_routes.gd", "CAREER_CREST_FILES") or {}
	phases = const("scripts/opera_career_world_2d.gd", "PHASES") or {}
	finale = const("scripts/opera_career_world_2d.gd", "FINALE_START") or {}
	stations = const("scripts/opera_career_world_2d.gd", "PHASE_STATIONS") or {}
	goals = const("scripts/opera_career_world_2d.gd", "GOAL_PROPS") or {}
	competition = const("scripts/opera_competition.gd", "CAREERS") or {}
	mastery = const("scripts/opera_mastery.gd", "RULES") or {}
	enabled = const("scripts/opera_performance_plan.gd", "ENABLED") or []
	practice = const("scripts/opera_performance_plan.gd", "PRACTICE_COUNTS") or {}
	colors = const("scripts/opera_performance_overlay.gd", "CAREER_COLORS") or {}
	party = const("scripts/chapter_two_party_plan.gd", "LIVE_CAREERS") or []
	music_build = set(py_list("tools/build_area_music.py", "EXPECTED_IDS"))
	atlas_gate = set(py_list("tools/audit_opera_roshan_animation.py", "CAREERS"))

	jobs = []
	for slot, act in enumerate(acts):
		if act.get("retired"):
			jobs.append({"slot": slot, "status": "TOMBSTONE"})
			continue
		jid = act["costume"]
		room = next((r for r, idx in rooms.items() if slot in idx), None)
		cue = act.get("music", "")
		chapter2 = next((p for p in party if isinstance(p, dict) and p.get("act_index") == slot), None)
		comp = competition.get(jid, {})
		jobs.append({
			"id": jid,
			"slot": slot,
			"status": "LIVE",
			"title": act.get("name"),
			"career_label": act.get("career"),
			"kind": act.get("kind"),
			"home": {"room": room, "room_order": rooms[room].index(slot) if room else None},
			"crest": crests.get(jid),
			"music": {"cue": cue, "in_build_tool": cue in music_build,
				"ogg_exists": Path(f"assets/audio/music/{cue}.ogg").is_file()},
			"phases": [{"name": p.get("name"), "mode": p.get("mode"), "vo": p.get("vo")}
				for p in phases.get(jid, []) if isinstance(p, dict)],
			"finale_start": finale.get(jid),
			"stations": stations.get(jid),
			"goal_prop": goals.get(jid),
			"competition": {k: color(comp.get(k)) for k in ("par_time", "rival_cap", "cooperative", "timed_retry", "accent") if k in comp},
			"mastery": mastery.get(jid),
			"performance": {"two_act": jid in enabled, "practice": practice.get(jid)},
			"overlay_color": color(colors.get(jid)),
			"chapter2": {k: chapter2.get(k) for k in ("career", "room", "piece")} if chapter2 else None,
			"art": {"costume_sheet": f"assets/opera/worlds/actors/animation/roshan_{jid}_sheet_a.png",
				"costume_sheet_exists": Path(f"assets/opera/worlds/actors/animation/roshan_{jid}_sheet_a.png").is_file(),
				"in_atlas_gate": jid in atlas_gate},
		})

	live = [j for j in jobs if j["status"] == "LIVE"]
	tomb = [j for j in jobs if j["status"] == "TOMBSTONE"]
	slots = len(jobs)
	derived = {
		"active_star_mask": sum(1 << j["slot"] for j in live),
		"retired_star_mask": sum(1 << j["slot"] for j in tomb),
		"active_count": len(live),
		"live_indices": [j["slot"] for j in live],
		"retired_indices": [j["slot"] for j in tomb],
		"slot_count": slots,
		"star_ceiling": (1 << slots) - 1,
		"shipping_phase_total": sum(len(j["phases"]) for j in live),
		"party_mask": sum(1 << p["act_index"] for p in party if isinstance(p, dict)),
		"next_free_bit": slots,
		"star_ceiling_after_next_job": (1 << (slots + 1)) - 1,
	}
	clamps = star_clamps("scripts/save_state.gd")
	loop = literal_ints("scripts/save_state.gd", r"for bit_index in range\((\d+)\)")
	phase_pin = literal_ints("scripts/probe_opera_2d.gd", r"shipping_phase_count == (\d+)")
	checks = [
		("ACTIVE_STAR_MASK (opera_house.gd)", const("scripts/opera_house.gd", "ACTIVE_STAR_MASK"), derived["active_star_mask"]),
		("OPERA_ACTIVE_STAR_MASK (save_state.gd)", const("scripts/save_state.gd", "OPERA_ACTIVE_STAR_MASK"), derived["active_star_mask"]),
		("RETIRED_STAR_MASK (opera_house.gd)", const("scripts/opera_house.gd", "RETIRED_STAR_MASK"), derived["retired_star_mask"]),
		("ACTIVE_ACT_COUNT (opera_house.gd)", const("scripts/opera_house.gd", "ACTIVE_ACT_COUNT"), derived["active_count"]),
		("OPERA_ACTIVE_ACT_COUNT (save_state.gd)", const("scripts/save_state.gd", "OPERA_ACTIVE_ACT_COUNT"), derived["active_count"]),
		("LIVE_ACT_INDICES (opera_house.gd)", live_literal, derived["live_indices"]),
		("RETIRED_ACT_INDICES (opera_house.gd)", retired_literal, derived["retired_indices"]),
		("star loop bound range(N) (save_state.gd)", loop, [derived["slot_count"]]),
		("opera_stars clamps (save_state.gd)", clamps, [derived["star_ceiling"]] * len(clamps)),
		("ALL_PARTY_MASK (chapter_two_party_plan.gd)", const("scripts/chapter_two_party_plan.gd", "ALL_PARTY_MASK"), derived["party_mask"]),
		("shipping phase pin (probe_opera_2d.gd)", phase_pin, [derived["shipping_phase_total"]]),
	]
	results = [{"literal": name, "code_value": code, "derived_value": want,
		"result": "MATCH" if code == want else "DIFFERS"} for name, code, want in checks]
	drift = {
		"music_cue_missing_from_build_tool": [j["id"] for j in live if not j["music"]["in_build_tool"]],
		"music_ogg_missing": [j["id"] for j in live if not j["music"]["ogg_exists"]],
		"costume_sheet_not_in_atlas_gate": [j["id"] for j in live if not j["art"]["in_atlas_gate"]],
		"no_home_room": [j["id"] for j in live if not j["home"]["room"]],
		"no_mastery_rule": [j["id"] for j in live if not j["mastery"]],
		"no_overlay_color": [j["id"] for j in live if j["overlay_color"] is None],
		"no_crest": [j["id"] for j in live if not j["crest"]],
		"next_job_trap": {
			"next_free_bit": derived["next_free_bit"],
			"clamp_in_code": sorted(set(clamps)),
			"ceiling_needed": derived["star_ceiling_after_next_job"],
			"a_save_with_the_next_bit_would_clamp_to": derived["star_ceiling"],
			"which_sets_bits": f"0..{derived['slot_count'] - 1} (every career, including tombstones)",
		},
	}
	(out / "extracted_catalog.json").write_bytes((json.dumps(
		{"measured_at_head": head, "source": "scripts/*.gd registries, parsed read-only", "jobs": jobs},
		indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
	(out / "derivation_check.json").write_bytes((json.dumps(
		{"measured_at_head": head, "derived": derived, "checks": results, "drift": drift},
		indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
	print(f"HEAD {head}")
	print(f"jobs: {len(live)} live, {len(tomb)} tombstones, {slots} slots")
	for r in results:
		print(f"{r['result']:8} {r['literal']}: code={r['code_value']} derived={r['derived_value']}")
	for k, v in drift.items():
		print(f"DRIFT {k}: {v}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
