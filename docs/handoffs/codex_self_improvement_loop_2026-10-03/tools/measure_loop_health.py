#!/usr/bin/env python3
"""Measure the health of the project's improvement loop. Read-only; prints JSON.

Run from the repository root:

  python -B docs/handoffs/codex_self_improvement_loop_2026-10-03/tools/measure_loop_health.py [--today YYYY-MM-DD] [--out PATH]

It measures the loop, not the game:

  findings      lifecycle counts and how long each open finding has gone
                without a dated history entry
  audit_log     how often the master audit's change history moves
  impact        how many change records exist per month, how many link no
                finding, and how many record a lesson
  handoffs      for each published Codex handoff, whether the files it asks
                for exist yet (built, partly built or not started)
  automation    workflows that run on a schedule

Standard library only. Uses `git log` for dates. Writes nothing unless --out.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

FINDINGS = Path("audit/findings/ACTIVE_FINDINGS_2026-08-13.md")
MASTER = Path("audit/MASTER_AUDIT_2026-08-09.md")
TERMINAL = {
	"VERIFIED_FIXED", "DISMISSED_NOT_A_DEFECT", "DISMISSED_NOT_IN_PROJECT",
	"SUPERSEDED", "DUPLICATE", "WAIVED_WITH_REASON",
}
DATE = re.compile(r"(20\d\d-\d\d-\d\d)")

# What each published handoff asks to exist when it is built. A path counts as
# built when it exists in the working tree (or, for deletions, is gone).
HANDOFF_TARGETS = {
	"codex_master_audit_refinement_2026-09-30": {
		"exists": ["design/11_DESIGN_REFERENCE.md", "design/reference/owner_decisions.json",
			"design/reference/canon.json", "design/reference/patterns.json", "design/reference/tokens.json",
			"tools/audit_live_status.py", "design/12_JOB_GAME_PLAYBOOK.md"],
	},
	"codex_job_platform_architecture_2026-09-30": {
		"exists": ["content/jobs", "tools/content_build.py", "scripts/generated/job_catalog_data.gd"],
	},
	"codex_reference_consolidation_2026-09-30": {
		"exists": ["audit/archive", "design/reference/REF_OPERA_CAREERS.md"],
	},
	"codex_visual_design_language_2026-09-30": {
		"exists": ["design/reference/VISUAL_LANGUAGE.md", "design/reference/visual_language.json",
			"design/reference/art_registry.json", "tools/visual_language.py",
			"design/templates/ART_STYLE_CARD_V1.md", "design/templates/ART_REVIEW_CARD_V1.md"],
	},
	"codex_roshan_art_repairs_2026-09-30": {
		"gone": ["assets/characters/roshan_sprite.png", "assets/sprites/sky_lagoon/sky_lagoon_roshan.png",
			"assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png"],
	},
}


def git(*args: str) -> str:
	return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def split_records(text: str) -> dict[str, dict[str, str]]:
	records: dict[str, dict[str, str]] = {}
	parts = re.split(r"(?m)^## (MA-[A-Z0-9]+-\d{3})\s*$", text)
	for index in range(1, len(parts), 2):
		fields: dict[str, str] = {}
		for line in parts[index + 1].splitlines():
			match = re.match(r"^\| ([a-z_ /]+) \| (.*) \|$", line)
			if match:
				fields[match.group(1).strip()] = match.group(2)
		records[parts[index]] = fields
	return records


def measure_findings(today: datetime.date) -> dict:
	records = split_records(FINDINGS.read_text(encoding="utf-8"))
	lifecycles: collections.Counter[str] = collections.Counter()
	open_rows = []
	for finding_id, fields in records.items():
		match = re.search(r"`([A-Z_]+)`", fields.get("lifecycle", ""))
		lifecycle = match.group(1) if match else fields.get("lifecycle", "").strip()
		lifecycles[lifecycle] += 1
		if lifecycle in TERMINAL:
			continue
		dates = DATE.findall(fields.get("history", ""))
		last = max(dates) if dates else None
		age = (today - datetime.date.fromisoformat(last)).days if last else None
		open_rows.append({"id": finding_id, "lifecycle": lifecycle, "severity": fields.get("severity", "").strip(),
			"last_history": last, "days_since": age})
	ages = [row["days_since"] for row in open_rows if row["days_since"] is not None]
	return {
		"records": len(records),
		"lifecycles": dict(sorted(lifecycles.items())),
		"open": len(open_rows),
		"open_without_history_entry_for": {f"{days}_days": sum(1 for age in ages if age > days) for days in (7, 14, 30)},
		"fixed_pending_verification": sorted(
			(row for row in open_rows if row["lifecycle"] == "FIXED_PENDING_VERIFICATION"),
			key=lambda row: -(row["days_since"] or 0)),
		"oldest_open": sorted(open_rows, key=lambda row: -(row["days_since"] or 0))[:10],
	}


def measure_audit_log() -> dict:
	text = MASTER.read_text(encoding="utf-8")
	history = text.split("## 14. Change history", 1)[1].split("\n## ", 1)[0] if "## 14. Change history" in text else ""
	dates = re.findall(r"(?m)^\| (20\d\d-\d\d-\d\d) \|", history)
	by_month = collections.Counter(date[:7] for date in dates)
	updates = re.findall(r"(?m)^[A-Z][^|\n]{0,120}\((20\d\d-\d\d-\d\d)\)", text.split("## 1. Executive verdict", 1)[0])
	return {
		"history_rows": len(dates),
		"history_rows_by_month": dict(sorted(by_month.items())),
		"latest_history_date": max(dates) if dates else None,
		"dated_update_paragraphs_before_section_1": len(updates),
	}


def measure_impact_records() -> dict:
	by_month: collections.Counter[str] = collections.Counter()
	no_findings = with_lessons = total = 0
	for path in sorted(glob.glob("design/audit_impacts/*.json")):
		total += 1
		added = git("log", "--diff-filter=A", "--format=%ad", "--date=short", "--", path).split()
		if not added:
			# Files that arrived through a merge have no plain add commit; use the first commit that touches them.
			added = git("log", "--format=%ad", "--date=short", "--", path).split()
		if added:
			by_month[added[-1][:7]] += 1
		try:
			record = json.loads(Path(path).read_text(encoding="utf-8"))
		except (OSError, ValueError):
			continue
		if record.get("findings") == []:
			no_findings += 1
		blob = json.dumps(record).lower()
		if any(word in blob for word in ("lesson", "retrospect", "learned", "what worked", "next time")):
			with_lessons += 1
	return {"records": total, "added_by_month": dict(sorted(by_month.items())),
		"linking_no_finding": no_findings, "recording_a_lesson": with_lessons}


def measure_handoffs() -> list[dict]:
	rows = []
	for folder in sorted(glob.glob("docs/handoffs/*/")):
		name = Path(folder).name
		manifest = Path(folder) / "MANIFEST.json"
		revision = None
		if manifest.is_file():
			try:
				revision = json.loads(manifest.read_text(encoding="utf-8")).get("revision")
			except ValueError:
				revision = None
		targets = HANDOFF_TARGETS.get(name)
		if not targets:
			rows.append({"handoff": name, "revision": revision, "status": "not tracked by this script"})
			continue
		done = [p for p in targets.get("exists", []) if Path(p).exists()]
		done += [p for p in targets.get("gone", []) if not Path(p).exists()]
		wanted = len(targets.get("exists", [])) + len(targets.get("gone", []))
		status = "BUILT" if len(done) == wanted else ("PARTLY_BUILT" if done else "NOT_STARTED")
		rows.append({"handoff": name, "revision": revision, "status": status, "targets_done": len(done), "targets": wanted})
	return rows


def measure_automation() -> list[dict]:
	rows = []
	for path in sorted(glob.glob(".github/workflows/*.yml")):
		text = Path(path).read_text(encoding="utf-8")
		crons = re.findall(r"cron:\s*['\"]([^'\"]+)['\"]", text)
		if crons:
			rows.append({"workflow": Path(path).as_posix(), "cron": crons})
	return rows


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	parser.add_argument("--today", default=datetime.date.today().isoformat())
	parser.add_argument("--out")
	args = parser.parse_args(argv)
	today = datetime.date.fromisoformat(args.today)
	result = {
		"measure": "loop_health",
		"today": today.isoformat(),
		"head": git("rev-parse", "HEAD").strip(),
		"findings": measure_findings(today),
		"audit_log": measure_audit_log(),
		"impact_records": measure_impact_records(),
		"handoffs": measure_handoffs(),
		"scheduled_workflows": measure_automation(),
	}
	text = json.dumps(result, indent=1, ensure_ascii=False) + "\n"
	if args.out:
		Path(args.out).write_text(text, encoding="utf-8", newline="\n")
	else:
		sys.stdout.write(text)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
