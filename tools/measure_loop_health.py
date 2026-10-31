#!/usr/bin/env python3
"""Read-only, root-aware improvement-loop measures; path presence is not acceptance."""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

FINDINGS = Path("audit/findings/ACTIVE_FINDINGS_2026-08-13.md")
MASTER = Path("audit/MASTER_AUDIT_2026-08-09.md")
TERMINAL = {"VERIFIED_FIXED", "DISMISSED_NOT_A_DEFECT", "DISMISSED_NOT_IN_PROJECT",
            "SUPERSEDED", "DUPLICATE", "WAIVED_WITH_REASON"}
DATE = re.compile(r"20\d\d-\d\d-\d\d")
HANDOFF_TARGETS = {
    "codex_master_audit_refinement_2026-09-30": {"exists": [
        "design/11_DESIGN_REFERENCE.md", "design/reference/owner_decisions.json",
        "design/reference/canon.json", "design/reference/patterns.json",
        "design/reference/tokens.json", "tools/audit_live_status.py", "design/12_JOB_GAME_PLAYBOOK.md"]},
    "codex_job_platform_architecture_2026-09-30": {"exists": [
        "content/jobs", "tools/content_build.py", "scripts/generated/job_catalog_data.gd"]},
    "codex_reference_consolidation_2026-09-30": {"exists": [
        "audit/archive", "design/reference/REF_OPERA_CAREERS.md"]},
    "codex_visual_design_language_2026-09-30": {"exists": [
        "design/reference/VISUAL_LANGUAGE.md", "design/reference/visual_language.json",
        "design/reference/art_registry.json", "tools/visual_language.py",
        "design/templates/ART_STYLE_CARD_V1.md", "design/templates/ART_REVIEW_CARD_V1.md"]},
    "codex_roshan_art_repairs_2026-09-30": {"gone": [
        "assets/characters/roshan_sprite.png", "assets/sprites/sky_lagoon/sky_lagoon_roshan.png",
        "assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png"]},
    "codex_self_improvement_loop_2026-10-03": {"exists": [
        "tools/study_game.py", "audit/cycles/README.md", "design/reference/strengths.json",
        "design/reference/owner_decisions.json", "tools/build_study_roadmap.py",
        "design/reference/prompt_intents.json", "audit/ROADMAP.md"]},
}


def git(root: Path, *args: str, timeout: float = 30) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True, timeout=timeout).stdout


def split_records(text: str) -> dict[str, dict[str, str]]:
    records = {}
    parts = re.split(r"(?m)^## (MA-[A-Z0-9]+-\d{3})\s*$", text)
    for index in range(1, len(parts), 2):
        fields = {}
        for line in parts[index + 1].splitlines():
            match = re.match(r"^\| ([a-z_ /]+) \| (.*) \|$", line)
            if match:
                fields[match.group(1).strip()] = match.group(2)
        records[parts[index]] = fields
    return records


def measure_findings(root: Path, today: dt.date) -> dict:
    records = split_records((root / FINDINGS).read_text(encoding="utf-8"))
    lifecycles = collections.Counter()
    open_rows = []
    for finding_id, fields in records.items():
        match = re.search(r"`([A-Z_]+)`", fields.get("lifecycle", ""))
        lifecycle = match.group(1) if match else fields.get("lifecycle", "").strip()
        lifecycles[lifecycle] += 1
        if lifecycle in TERMINAL:
            continue
        dates = DATE.findall(fields.get("history", ""))
        last = max(dates) if dates else None
        age = (today - dt.date.fromisoformat(last)).days if last else None
        open_rows.append({"id": finding_id, "lifecycle": lifecycle,
                          "severity": fields.get("severity", "").strip(),
                          "last_history": last, "days_since": age})
    ages = [r["days_since"] for r in open_rows if r["days_since"] is not None]
    return {"records": len(records), "lifecycles": dict(sorted(lifecycles.items())),
            "open": len(open_rows), "open_missing_history": sum(r["last_history"] is None for r in open_rows),
            "open_without_history_entry_for": {f"{days}_days": sum(a >= days for a in ages) for days in (7, 14, 30)},
            "fixed_pending_verification": sorted(
                (r for r in open_rows if r["lifecycle"] == "FIXED_PENDING_VERIFICATION"),
                key=lambda r: -(r["days_since"] or 0)),
            "oldest_open": sorted(open_rows, key=lambda r: -(r["days_since"] or 0))[:10]}


def measure_audit_log(root: Path) -> dict:
    text = (root / MASTER).read_text(encoding="utf-8")
    history = text.split("## 14. Change history", 1)[-1].split("\n## ", 1)[0] if "## 14. Change history" in text else ""
    dates = re.findall(r"(?m)^\| (20\d\d-\d\d-\d\d) \|", history)
    updates = re.findall(r"(?m)^[A-Z][^|\n]{0,120}\((20\d\d-\d\d-\d\d)\)", text.split("## 1. Executive verdict", 1)[0])
    return {"history_rows": len(dates), "history_rows_by_month": dict(sorted(collections.Counter(d[:7] for d in dates).items())),
            "latest_history_date": max(dates) if dates else None,
            "dated_update_paragraphs_before_section_1": len(updates)}


def impact_dates(root: Path, timeout: float = 30) -> dict[str, str]:
    # One complete traversal includes merge arrivals; last seen is first change.
    dates = {}
    current = None
    for line in git(root, "log", "--format=DATE:%ad", "--date=short", "--name-only",
                    "--", "design/audit_impacts", timeout=timeout).splitlines():
        if line.startswith("DATE:"):
            current = line[5:]
        elif current and line.startswith("design/audit_impacts/") and line.endswith(".json"):
            dates[line] = current
    return dates


def measure_impact_records(root: Path, timeout: float = 30) -> dict:
    by_month = collections.Counter()
    paths = sorted((root / "design/audit_impacts").glob("*.json"))
    dates = impact_dates(root, timeout)
    no_findings = with_lessons = structured_lessons = 0
    errors = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if relative in dates:
            by_month[dates[relative][:7]] += 1
        try:
            record = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(record, dict):
                raise ValueError("impact record is not an object")
        except (OSError, ValueError) as error:
            errors.append({"path": relative, "reason": str(error)})
            continue
        no_findings += record.get("findings") == []
        with_lessons += any(w in json.dumps(record).lower() for w in ("lesson", "retrospect", "learned", "what worked", "next time"))
        structured_lessons += bool(record.get("lessons"))
    return {"records": len(paths), "added_by_month": dict(sorted(by_month.items())),
            "linking_no_finding": no_findings, "recording_a_lesson": with_lessons,
            "with_structured_lessons": structured_lessons, "invalid_records": errors,
            "uncommitted_records": [p.relative_to(root).as_posix() for p in paths if p.relative_to(root).as_posix() not in dates]}


def measure_handoffs(root: Path) -> list[dict]:
    rows = []
    for folder in sorted((root / "docs/handoffs").glob("*")):
        if not folder.is_dir():
            continue
        revision = None
        try:
            revision = json.loads((folder / "MANIFEST.json").read_text(encoding="utf-8-sig")).get("revision")
        except (OSError, ValueError, AttributeError):
            pass
        targets = HANDOFF_TARGETS.get(folder.name)
        if not targets:
            rows.append({"handoff": folder.name, "revision": revision, "status": "UNTRACKED",
                         "reason": "No target contract defined; existence is not completion"})
            continue
        done = [p for p in targets.get("exists", []) if (root / p).exists()]
        done += [p for p in targets.get("gone", []) if not (root / p).exists()]
        wanted = len(targets.get("exists", [])) + len(targets.get("gone", []))
        status = "TARGETS_PRESENT" if len(done) == wanted else ("PARTLY_BUILT" if done else "NOT_STARTED")
        rows.append({"handoff": folder.name, "revision": revision, "status": status,
                     "targets_done": len(done), "targets": wanted, "present": done,
                     "reason": "Path checks only; implementation and acceptance require review"})
    return rows


def measure_automation(root: Path) -> list[dict]:
    rows = []
    for path in sorted((root / ".github/workflows").glob("*.y*ml")):
        crons = re.findall(r"cron:\s*['\"]([^'\"]+)['\"]", path.read_text(encoding="utf-8"))
        if crons:
            rows.append({"workflow": path.relative_to(root).as_posix(), "cron": crons})
    return rows


def measure(root: Path, today: dt.date, timeout: float = 30) -> dict:
    return {"measure": "loop_health", "today": today.isoformat(),
            "head": git(root, "rev-parse", "HEAD", timeout=timeout).strip(),
            "findings": measure_findings(root, today), "audit_log": measure_audit_log(root),
            "impact_records": measure_impact_records(root, timeout), "handoffs": measure_handoffs(root),
            "scheduled_workflows": measure_automation(root)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--today", "--as-of", default=dt.date.today().isoformat())
    parser.add_argument("--out", type=Path)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args(argv)
    result = measure(args.root.resolve(), dt.date.fromisoformat(args.today), args.timeout)
    text = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
