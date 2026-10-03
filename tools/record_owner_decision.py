#!/usr/bin/env python3
"""Append evidence-backed owner answers; never infer owner consent from defaults."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

REGISTER = Path("design/reference/owner_decisions.json")
VIEW = Path("design/reference/OWNER_DECISIONS.md")
AUTHORITIES = {"recorded_owner", "operating_default"}


def source_path(root: Path, value: str) -> Path:
	if not isinstance(value, str) or not value.strip():
		raise ValueError("source/check must be nonempty text")
	name = value.split("#", 1)[0]
	path = (root / name).resolve()
	if Path(name).is_absolute() or ".." in Path(name).parts or not path.is_relative_to(root.resolve()):
		raise ValueError("source/check must stay inside the repository")
	if any(part.lower() in {".secrets", ".git", ".aws"} for part in path.relative_to(root.resolve()).parts):
		raise ValueError("source/check cannot reference private operational data")
	return path


def validate(root: Path, data: dict) -> list[str]:
	issues: list[str] = []
	if not isinstance(data, dict) or data.get("schema") != "owner_decisions/1" or not isinstance(data.get("decisions"), list):
		return ["expected owner_decisions/1 and decisions array"]
	seen: set[str] = set()
	for row in data["decisions"]:
		if not isinstance(row, dict):
			issues.append("decision must be an object")
			continue
		identity = row.get("id", "")
		if not isinstance(identity, str) or not re.fullmatch(r"ODR-[A-Z0-9-]+", identity) or identity in seen:
			issues.append(f"invalid/duplicate decision id: {identity}")
		seen.add(str(identity))
		for field in ("date", "subject", "decision", "source", "question"):
			if not isinstance(row.get(field), str) or not row[field].strip():
				issues.append(f"{identity}: {field} must be nonempty text")
		try:
			dt.date.fromisoformat(row.get("date", ""))
		except (ValueError, TypeError):
			issues.append(f"{identity}: invalid decision date")
		if row.get("authority") not in AUTHORITIES:
			issues.append(f"{identity}: unknown authority")
		if row.get("cycle") is not None and (not isinstance(row["cycle"], str) or not re.fullmatch(r"[A-Za-z0-9_-]+", row["cycle"])):
			issues.append(f"{identity}: unsafe cycle id")
		checks = row.get("checks")
		if not isinstance(checks, list) or any(not isinstance(value, str) or not value.strip() for value in checks):
			issues.append(f"{identity}: checks must be a list of paths")
			checks = []
		for reference in [row.get("source", ""), *checks]:
			try:
				if not source_path(root, reference).is_file():
					issues.append(f"{identity}: missing evidence/check {reference}")
			except (ValueError, TypeError):
				issues.append(f"{identity}: unsafe evidence/check {reference}")
		if "checkable" in row and not isinstance(row["checkable"], bool):
			issues.append(f"{identity}: checkable must be a boolean")
		if row.get("checkable") is True:
			if not checks:
				issues.append(f"{identity}: checkable correction requires an executable check reference")
			for reference in checks:
				name = Path(reference.split("#", 1)[0])
				workflow = name.suffix.lower() in {".yml", ".yaml"} and name.as_posix().startswith(".github/workflows/")
				if name.suffix.lower() not in {".py", ".gd", ".sh", ".ps1", ".bat", ".cmd"} and not workflow:
					issues.append(f"{identity}: checkable correction needs executable source, not documentary reference {reference}")
	return issues


def append(root: Path, data: dict, answers: list[dict], cycle: str, answered_on: str) -> dict:
	"""Intake supplied answers as immutable records; at most five per owner page."""
	if not re.fullmatch(r"[A-Za-z0-9_-]+", cycle):
		raise ValueError("unsafe cycle id")
	dt.date.fromisoformat(answered_on)
	if not isinstance(answers, list) or not 1 <= len(answers) <= 5:
		raise ValueError("provide one to five actual owner answers")
	rows: list[dict] = []
	for answer in answers:
		if not isinstance(answer, dict) or answer.get("authority") != "recorded_owner":
			raise ValueError("intake requires recorded_owner evidence; defaults are not owner answers")
		if answer.get("date") != answered_on:
			raise ValueError("answer dates must equal the stated owner session date")
		rows.append({**answer, "cycle": cycle})
	merged = {**data, "decisions": [*data.get("decisions", []), *rows]}
	issues = validate(root, merged)
	if issues:
		raise ValueError("; ".join(issues))
	return merged


def render(data: dict) -> str:
	lines = ["# Owner decisions", "", "Generated from owner_decisions.json by tools/record_owner_decision.py. Recorded owner decisions retain their source and scope. Operating defaults implement the handoff's default policy; they are not owner answers or creative acceptance.", "", "| ID | Date | Authority | Decision | Evidence / checks |", "|---|---|---|---|---|"]
	for row in data["decisions"]:
		escape = lambda value: str(value).replace("|", "\\|").replace("\n", " ")
		reference = f"[{escape(row['source'])}](../../{row['source']})"
		checks = ", ".join(f"[{escape(value)}](../../{value})" for value in row["checks"])
		lines.append(f"| `{row['id']}` | {row['date']} | `{row['authority']}` | {escape(row['decision'])} | {reference}; {checks or 'Human review remains required where applicable.'} |")
	return "\n".join(lines) + "\n"


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
	parser.add_argument("--answers", type=Path, help="JSON array of actual, source-backed owner answers")
	parser.add_argument("--cycle")
	parser.add_argument("--answered-on", help="Owner session date YYYY-MM-DD, supplied explicitly")
	parser.add_argument("--check", action="store_true", help="Validate register and generated view without writing")
	args = parser.parse_args()
	root = args.root.resolve()
	try:
		data = json.loads((root / REGISTER).read_text(encoding="utf-8"))
		initial_issues = validate(root, data)
		if initial_issues:
			raise ValueError("; ".join(initial_issues))
		cycle_path = None
		cycle_text = None
		if args.answers:
			if args.check or not args.cycle or not args.answered_on:
				raise ValueError("intake requires --cycle and --answered-on, and cannot use --check")
			answers = json.loads(args.answers.read_text(encoding="utf-8"))
			data = append(root, data, answers, args.cycle, args.answered_on)
			cycle_path = root / "audit/cycles" / args.cycle / "owner_answers.json"
			prior = json.loads(cycle_path.read_text(encoding="utf-8")) if cycle_path.exists() else []
			if not isinstance(prior, list):
				raise ValueError("existing cycle answers must be an array; nothing was written")
			cycle_text = json.dumps([*prior, *data["decisions"][-len(answers):]], indent=2) + "\n"
		issues = validate(root, data)
		if issues:
			raise ValueError("; ".join(issues))
		view = render(data)
		if args.check:
			if not (root / VIEW).is_file() or (root / VIEW).read_text(encoding="utf-8") != view:
				raise ValueError("owner decision view is stale")
		else:
			if args.answers:
				cycle_path.parent.mkdir(parents=True, exist_ok=True)
				# Validate every input before publishing either register or cycle answers.
				cycle_path.write_text(cycle_text, encoding="utf-8")
				(root / REGISTER).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
			(root / VIEW).write_text(view, encoding="utf-8")
		print(f"DECISIONS|COUNT|{len(data['decisions'])}")
		print("DECISIONS|RESULT|ALL OK")
		return 0
	except (ValueError, OSError) as exc:
		print(f"DECISIONS|RESULT|FAIL|{exc}")
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
