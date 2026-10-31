#!/usr/bin/env python3
"""Measure how usable the master audit and design language are as a design reference.

Read-only. Run from the repository root:

    python -B <packet>/tools/measure_reference_health.py --out <packet>/data

where <packet> is docs/handoffs/codex_master_audit_refinement_2026-09-30.

Writes six JSON files and prints a one-screen summary. Nothing in the game or
its governance documents is modified. Every number is recomputed from the
checked-out tree and Git history, so rerunning at a newer head refreshes it.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

MASTER = "audit/MASTER_AUDIT_2026-08-09.md"
DESIGN = "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md"
FINDINGS = "audit/findings/ACTIVE_FINDINGS_2026-08-13.md"
LEDGER = "design/05_DOC_LEDGER.md"
AUTHORITY_DOCS = [
	"CLAUDE.md",
	"AGENTS.md",
	MASTER,
	DESIGN,
	FINDINGS,
	"design/00_MASTER_INDEX.md",
	"design/01_GAME_DESIGN.md",
	"design/02_ART_DIRECTION.md",
	"design/03_TECHNICAL_ARCHITECTURE.md",
	"design/04_OPEN_WORK.md",
	"design/09_CHAPTER_DEVELOPMENT_GUIDE.md",
	"design/10_CHAPTER_REFERENCE_LIBRARY.md",
]
TERMINAL = {"VERIFIED_FIXED", "DISMISSED_NOT_A_DEFECT", "DISMISSED_NOT_IN_PROJECT", "SUPERSEDED", "DUPLICATE"}

SHA_RE = re.compile(r"`([0-9a-f]{7,40})(?:…[0-9a-f]{4,})?`")
RUN_RE = re.compile(r"(?<![0-9])3[0-9]{10}(?![0-9])")
DURATION_RE = re.compile(r"\b\d[\d,]*\.\d+\s*seconds\b|\b\d+m\d+s\b")
DATE_RE = re.compile(r"20\d\d-\d\d-\d\d")
PATH_RE = re.compile(r"(?<![\w/.-])((?:scripts|assets|tools|design|audit|assets_src|scenes|books)/[\w./-]+\.[A-Za-z0-9]+)")
OWNER_RE = re.compile(
	r"owner[- ](?:decision|direction|ruling|clarification|request|rule)s?[^\n]{0,40}?(20\d\d-\d\d-\d\d)"
	r"|(20\d\d-\d\d-\d\d)[^\n]{0,20}?owner[- ](?:decision|direction|ruling|clarification)",
	re.I,
)


def git(*args: str) -> str:
	return subprocess.check_output(["git", *args], text=True, encoding="utf-8", errors="replace").strip()


def read(path: str) -> str:
	return Path(path).read_text(encoding="utf-8")


def sections(text: str) -> list[tuple[str, int, int]]:
	"""Top-level '## ' sections as (heading, start_line, end_line), 1-based inclusive."""
	lines = text.splitlines()
	marks = [(i, line[3:].strip()) for i, line in enumerate(lines) if line.startswith("## ")]
	out = []
	if marks and marks[0][0] > 0:
		out.append(("(preamble)", 1, marks[0][0]))
	for n, (i, title) in enumerate(marks):
		end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
		out.append((title, i + 1, end))
	return out


def composition() -> dict:
	result = {}
	for path in (MASTER, DESIGN, "design/00_MASTER_INDEX.md"):
		text = read(path)
		lines = text.splitlines()
		rows = []
		for title, start, end in sections(text):
			body = "\n".join(lines[start - 1:end])
			shas = len(SHA_RE.findall(body))
			runs = len(RUN_RE.findall(body))
			durations = len(DURATION_RE.findall(body))
			n = end - start + 1
			rows.append({
				"section": title,
				"lines": n,
				"bytes": len(body.encode("utf-8")),
				"commit_shas": shas,
				"ci_run_ids": runs,
				"durations": durations,
				"evidence_tokens_per_100_lines": round(100 * (shas + runs + durations) / max(n, 1), 1),
			})
		total_bytes = sum(r["bytes"] for r in rows)
		result[path] = {
			"lines": len(lines),
			"bytes": len(text.encode("utf-8")),
			"sections": rows,
			"evidence_token_total": sum(r["commit_shas"] + r["ci_run_ids"] + r["durations"] for r in rows),
			"share_of_bytes_in_sections_with_>=10_tokens_per_100_lines": round(
				sum(r["bytes"] for r in rows if r["evidence_tokens_per_100_lines"] >= 10) / max(total_bytes, 1), 3,
			),
		}
	return result


def duplicated_tokens() -> dict:
	master = read(MASTER)
	candidates = collections.Counter(SHA_RE.findall(master)) + collections.Counter(RUN_RE.findall(master))
	inventory = [p for p in git("ls-files", "*.md").splitlines() if p]
	spread = {}
	for token, _ in candidates.most_common(60):
		files = {}
		for path in inventory:
			try:
				count = read(path).count(token)
			except (OSError, UnicodeDecodeError):
				continue
			if count:
				files[path] = count
		spread[token] = {"hits": sum(files.values()), "files": len(files), "paths": sorted(files)}
	top = sorted(spread.items(), key=lambda kv: (-kv[1]["files"], -kv[1]["hits"]))[:20]
	return {"markdown_inventory": len(inventory), "top_tokens_by_file_spread": dict(top)}


def live_values() -> dict:
	values = {}
	values["main_gd_lines"] = sum(1 for _ in open("scripts/main.gd", encoding="utf-8"))
	values["probe_scripts"] = len(glob.glob("scripts/probe*.gd"))
	values["gdscript_files"] = len([p for p in git("ls-files", "*.gd").splitlines() if p])
	try:
		out = subprocess.run([sys.executable, "-B", "tools/audit_game_2d.py"], capture_output=True, text=True,
			encoding="utf-8", errors="replace", timeout=900).stdout
		debt = re.search(r"GAME2D\| DEBT\|(.*)", out)
		if debt:
			for key, val in re.findall(r"(\w+)=(\d+)", debt.group(1)):
				values[f"game2d_{key}"] = int(val)
		status = re.search(r"GAME2D\| STATUS\| (\w+)", out)
		values["game2d_status"] = status.group(1) if status else "unknown"
	except (OSError, subprocess.TimeoutExpired) as error:
		values["game2d_error"] = type(error).__name__
	return values


CLAIMS = [
	("model files", re.compile(r"\b(\d{3})\s+model(?:/export)?\s+files\b|\b(\d{3})[- ]model\b"), "game2d_model_files"),
	("production 3D files", re.compile(r"\b(\d{2})\s+production[ -]3D\s+files\b|/(\d{2})\s+production\b"), "game2d_production_3d_files"),
	("main.gd lines", re.compile(r"main\.gd`?\s+(?:is|at|\()?\s*([\d,]{4,6})\s+lines|\b([\d,]{5,6})\s+lines\b[^\n]{0,40}main\.gd|main\.gd[^\n]{0,60}?\b([\d,]{5,6})\s+lines"), "main_gd_lines"),
	("probe scripts", re.compile(r"\b(\d{3})\s+probe scripts\b|all\s+(\d{3})\s+probes\b"), "probe_scripts"),
]


# Change-history rows, finding history cells and explicit targets are historical
# or aspirational by design; only present-tense claims are compared.
HISTORICAL_LINE_RE = re.compile(r"^\| 20\d\d-\d\d-\d\d |^\| `?history`? \||target|below 2,500|<\s*2[,.]?5")


def hand_copied_counts(live: dict) -> list[dict]:
	rows = []
	for path in AUTHORITY_DOCS:
		if not Path(path).is_file():
			continue
		for number, line in enumerate(read(path).splitlines(), 1):
			if HISTORICAL_LINE_RE.search(line):
				continue
			for label, pattern, key in CLAIMS:
				for match in pattern.finditer(line):
					raw = next(g for g in match.groups() if g)
					claimed = int(raw.replace(",", ""))
					actual = live.get(key)
					if actual is None or claimed == actual:
						continue
					rows.append({
						"path": path, "line": number, "claim": label,
						"claimed": claimed, "live": actual,
						"text": line.strip()[:160],
					})
	return rows


def _day(value: str) -> int:
	import datetime
	return datetime.date.fromisoformat(value).toordinal()


def finding_staleness() -> list[dict]:
	text = read(FINDINGS)
	parts = re.split(r"(?m)^## (MA-[A-Z0-9-]+)\s*$", text)
	rows = []
	for i in range(1, len(parts), 2):
		fid, body = parts[i], parts[i + 1]

		def field(name: str) -> str:
			m = re.search(r"(?m)^\| `?" + re.escape(name) + r"`? \| (.*) \|\s*$", body)
			return m.group(1) if m else ""

		lifecycle = field("lifecycle").strip("`")
		if lifecycle in TERMINAL:
			continue
		dates = DATE_RE.findall(field("history"))
		last = max(dates) if dates else "0000-00-00"
		paths = sorted({p.rstrip(".") for p in PATH_RE.findall(" ".join(
			field(k) for k in ("evidence", "fix", "reproduction", "surrounding_tests", "closure")))})
		existing = [p for p in paths if Path(p).exists()]
		touched = 0
		if existing:
			log = git("log", "--format=%h", f"--since={last} 23:59", "HEAD", "--", *existing[:40])
			touched = len([h for h in log.splitlines() if h])
		reference_day = git("log", "-1", "--format=%cs", "HEAD")
		rows.append({
			"days_since_last_history": (_day(reference_day) - _day(last)) if dates else None,
			"id": fid,
			"severity": field("severity"),
			"lifecycle": lifecycle,
			"last_history_date": last,
			"referenced_paths": len(paths),
			"referenced_paths_missing_now": len(paths) - len(existing),
			"commits_touching_referenced_paths_since_last_history": touched,
		})
	rows.sort(key=lambda r: (-r["commits_touching_referenced_paths_since_last_history"], r["last_history_date"]))
	return rows


def owner_decisions() -> dict:
	inventory = [p for p in git("ls-files", "*.md").splitlines() if p]
	design_text = read(DESIGN)
	mentions = []
	for path in inventory:
		try:
			lines = read(path).splitlines()
		except (OSError, UnicodeDecodeError):
			continue
		for number, line in enumerate(lines, 1):
			for match in OWNER_RE.finditer(line):
				date = match.group(1) or match.group(2)
				mentions.append({"path": path, "line": number, "date": date, "text": line.strip()[:140]})
	by_date = collections.defaultdict(set)
	for m in mentions:
		by_date[m["date"]].add(m["path"])
	dates = sorted(by_date)
	return {
		"mentions": len(mentions),
		"files": len({m["path"] for m in mentions}),
		"distinct_dates": len(dates),
		"dates": {d: {"files": sorted(by_date[d]), "named_in_design_06": d in design_text} for d in dates},
		"mentions_list": mentions,
	}


def rule_inventory() -> list[dict]:
	text = read(DESIGN)
	lines = text.splitlines()
	current_section = ""
	rules = []
	for i, line in enumerate(lines):
		if line.startswith("## "):
			current_section = line[3:].strip()
		m = re.match(r"^`(DL-[A-Z0-9-]+)`\s+—", line)
		if not m:
			continue
		body = [line]
		for follow in lines[i + 1:]:
			if not follow.strip() or follow.startswith("`DL-") or follow.startswith("## "):
				break
			body.append(follow)
		joined = " ".join(body)
		rules.append({
			"id": m.group(1),
			"family": m.group(1).split("-")[1],
			"section": current_section,
			"words": len(joined.split()),
			"embeds_commit_or_hash": bool(SHA_RE.search(joined) or re.search(r"\b[0-9a-f]{40,64}\b", joined)),
			"embeds_run_or_duration": bool(RUN_RE.search(joined) or DURATION_RE.search(joined)),
			"embeds_count_snapshot": bool(re.search(r"\b\d{2,}\s+(?:careers|phases|modes|cells|frames|cues|probes|files|lines)\b", joined)),
		})
	cites = collections.Counter()
	for path in glob.glob("design/audit_impacts/*.json"):
		try:
			record = json.loads(Path(path).read_text(encoding="utf-8"))
		except (OSError, ValueError):
			continue
		for rule in record.get("rules", []):
			cites[rule] += 1
	findings = read(FINDINGS)
	for rule in rules:
		rule["impact_record_citations"] = cites.get(rule["id"], 0)
		rule["finding_citations"] = len(re.findall(re.escape(rule["id"]) + r"(?![0-9])", findings))
	return rules


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--out", required=True)
	args = parser.parse_args()
	out = Path(args.out)
	out.mkdir(parents=True, exist_ok=True)
	head = git("rev-parse", "HEAD")
	live = live_values()
	data = {
		"composition.json": composition(),
		"duplicated_evidence_tokens.json": duplicated_tokens(),
		"live_vs_documented_counts.json": {"live": live, "stale_claims": hand_copied_counts(live)},
		"finding_staleness.json": finding_staleness(),
		"owner_decisions.json": owner_decisions(),
		"rule_inventory.json": rule_inventory(),
	}
	for name, payload in data.items():
		blob = json.dumps({"measured_at_head": head, "data": payload}, indent=1, ensure_ascii=False) + "\n"
		(out / name).write_bytes(blob.encode("utf-8"))
	comp = data["composition.json"][MASTER]
	stale = data["live_vs_documented_counts.json"]["stale_claims"]
	staleness = data["finding_staleness.json"]
	owners = data["owner_decisions.json"]
	rules = data["rule_inventory.json"]
	print(f"HEAD {head}")
	print(f"master audit: {comp['lines']} lines, {comp['bytes']} bytes, {comp['evidence_token_total']} evidence tokens")
	print(f"live: {json.dumps(live)}")
	print(f"stale hand-copied counts in authority docs: {len(stale)}")
	print(f"open findings: {len(staleness)}; untouched since 2026-09-01: "
		f"{sum(r['last_history_date'] < '2026-09-01' for r in staleness)}; with referenced code changed since last history: "
		f"{sum(r['commits_touching_referenced_paths_since_last_history'] > 0 for r in staleness)}")
	print(f"owner-decision mentions: {owners['mentions']} in {owners['files']} files over {owners['distinct_dates']} dates; "
		f"dates not named in design 06: {sum(not v['named_in_design_06'] for v in owners['dates'].values())}")
	print(f"rules: {len(rules)}; embedding commits/hashes: {sum(r['embeds_commit_or_hash'] for r in rules)}; "
		f"embedding count snapshots: {sum(r['embeds_count_snapshot'] for r in rules)}; "
		f"never cited by an impact record or finding: {sum(r['impact_record_citations'] == 0 and r['finding_citations'] == 0 for r in rules)}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
