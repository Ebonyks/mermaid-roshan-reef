#!/usr/bin/env python3
"""Read-only measurements behind MA-DOC-010 (chapter development guidance).

Usage:
	python -B measure_chapter_guide.py [--repo PATH] [--rev REV] [--output FILE]

Reads committed blobs at REV through git. It never changes the working tree,
never renders or writes images and never edits a finding, rule or record.
It prints one JSON object (or writes it, with LF line endings, to --output).
Every number in the MA-DOC-010 handoff README comes from this output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

DOCS = {
	"chapter_guide": "design/09_CHAPTER_DEVELOPMENT_GUIDE.md",
	"brief_template": "design/templates/CHAPTER_BRIEF_V1.md",
	"new_chapter_recipe": "design/reference/recipes/new_chapter.md",
	"prompt_intents": "design/reference/prompt_intents.json",
	"reference_library": "design/10_CHAPTER_REFERENCE_LIBRARY.md",
	"northern_branch": "design/chapters/NORTHERN_ICE_WORLD.md",
	"game_design": "design/01_GAME_DESIGN.md",
	"technical_architecture": "design/03_TECHNICAL_ARCHITECTURE.md",
	"design_language": "design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md",
	"master_audit": "audit/MASTER_AUDIT_2026-08-09.md",
	"findings": "audit/findings/ACTIVE_FINDINGS_2026-08-13.md",
	"roadmap": "audit/ROADMAP.md",
	"owner_decisions": "design/reference/owner_decisions.json",
	"save_state": "scripts/save_state.gd",
	"ci_script": "scripts/ci.sh",
	"probe_workflow": ".github/workflows/probes.yml",
}
CAST_TERMS = ("Grand Puff", "Ember King", "Rumi", "Baby Eagle", "Daddy", "Mommy")
NAME_TERMS = (
	"Day One", "Day Two", "Chapter 1", "Chapter One", "Chapter 2",
	"Chapter Two", "Chapter 3", "Chapter Three",
)
DIRECTOR_FILES = (
	"scripts/day_one_director.gd",
	"scripts/chapter_two_director.gd",
	"scripts/day_two_transition_2d.gd",
	"scripts/arena/fairy_conservatory_door_2d.gd",
	"scripts/arena/fairy_conservatory_handoff_2d.gd",
	"scripts/fairy_restoration_prototype.gd",
)
CHAPTER_PROBES = (
	"probe_day_one_director", "probe_day_one_integration", "probe_day_one_story_clips",
	"probe_chapter2", "probe_chapter2_farmer_resume", "probe_chapter2_lawn",
	"probe_alpha_milestone_save", "probe_fairy_conservatory_route",
	"probe_fairy_conservatory_handoff", "probe_fairy_restoration",
)
# File plan of the 2026-09-30 refinement handoff (MA-DOC-006), section 3.2.
PLANNED_REFERENCE_FILES = (
	"design/11_DESIGN_REFERENCE.md",
	"design/reference/canon.json",
	"design/reference/CANON.md",
	"design/reference/engines.json",
	"design/templates/DESIGN_CARD_V1.md",
	"design/templates/CHAPTER_BRIEF_V2.md",
)
STORY_TERMS = (
	"chapter", "story", "grand puff", "day one", "picture-book", "picture book",
	"northern", "delegat", "ember", "canon",
)
NAMED_DECISIONS = (
	"ODR-FASHION-PERSISTENCE-20261006",
	"ODR-POPSTAR-SONG-20261018",
	"ODR-RUMI-REVISION-HANDOFF-20261017",
	"ODR-PRIORITY-JOB-TAKEOVER",
	"ODR-LEARNING-SCOPE-20261018",
)
FINDINGS = (
	"MA-DOC-006", "MA-DOC-007", "MA-DOC-008", "MA-DOC-009",
	"MA-PLAY-001", "MA-PLAY-005", "MA-PLAY-006",
)
NORTHERN_CONCEPT = "assets_src/concepts/northern_forest_concept_2026-07-29.png"
RESCUE_COMMIT = "f07027af253badd8d37f0b3b6aeedb8cbab7336f"
LEARNING_COMMIT = "7b851b3d0be0dd83652751ca5c3085fc4b36b6b8"
SAVE_KEY = re.compile(r'"((?:chapter2_|chapter3_|day_one_|day_two_|fairy)[A-Za-z0-9_]*)"')
RECEIPT_LINK = re.compile(r"/r\d{2,3}_[a-z0-9_]+/")
DATE = re.compile(r"20\d\d-\d\d-\d\d")


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
	result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
	if check and result.returncode != 0:
		raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
	return result


def text(repo: Path, rev: str, path: str) -> str | None:
	result = git(repo, "show", f"{rev}:{path}", check=False)
	return result.stdout.decode("utf-8", "replace") if result.returncode == 0 else None


def exists(repo: Path, rev: str, path: str) -> bool:
	return git(repo, "cat-file", "-e", f"{rev}:{path}", check=False).returncode == 0


def read_many(repo: Path, rev: str, paths: list[str]) -> dict[str, str]:
	request = "".join(f"{rev}:{path}\n" for path in paths).encode("utf-8")
	data = subprocess.run(
		["git", "-C", str(repo), "cat-file", "--batch"], input=request,
		capture_output=True, check=True,
	).stdout
	out: dict[str, str] = {}
	index = 0
	for path in paths:
		end = data.index(b"\n", index)
		header = data[index:end].decode("utf-8", "replace")
		index = end + 1
		if header.endswith("missing"):
			continue
		size = int(header.split()[2])
		out[path] = data[index:index + size].decode("utf-8", "replace")
		index += size + 1
	return out


def count_term(body: str, term: str, ignore_case: bool = False) -> int:
	flags = re.IGNORECASE if ignore_case else 0
	return len(re.findall(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", body, flags))


def last_touch(repo: Path, rev: str, path: str) -> dict:
	line = git(repo, "log", "-1", "--format=%H%x09%cs", rev, "--", path).stdout.decode().strip()
	commit, _, date = line.partition("\t")
	return {"commit": commit, "date": date}


def sections(body: str, marker: str) -> list[dict]:
	"""Split at lines that start with marker ('## ' or '### ')."""
	lines = body.split("\n")
	starts = [i for i, line in enumerate(lines) if line.startswith(marker)]
	result = []
	for n, start in enumerate(starts):
		end = starts[n + 1] if n + 1 < len(starts) else len(lines)
		chunk = "\n".join(lines[start:end])
		result.append({
			"title": lines[start][len(marker):].strip(),
			"first_line": start + 1,
			"last_line": end,
			"bytes": len(chunk.encode("utf-8")),
			"text": chunk,
		})
	return result


def table_rows(chunk: str) -> list[list[str]]:
	rows = []
	for line in chunk.split("\n"):
		if line.startswith("|") and not re.match(r"^\|\s*-", line):
			rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
	return rows


def paragraphs(lines: list[str]) -> list[str]:
	blocks, current = [], []
	for line in lines + [""]:
		plain = line.strip()
		if plain and not plain.startswith(("|", "<!--", "#")) and not re.fullmatch(r"-{3,}", plain):
			current.append(plain)
		elif current:
			blocks.append(" ".join(current))
			current = []
	return blocks


NON_STATUS_OPENINGS = ("[", "Planning guidance updated", "Section 13 owns", "Read the row for the task")


def status_notes(blocks: list[str]) -> int:
	"""Paragraphs other than the entry header, routing instructions and link bars."""
	return sum(1 for block in blocks if not block.startswith(NON_STATUS_OPENINGS))


def task_index(master: str) -> dict:
	start = master.index("<!-- AUDIT_TASK_INDEX_START -->")
	end = master.index("<!-- AUDIT_TASK_INDEX_END -->")
	lines = master[start:end].split("\n")
	header = next(i for i, line in enumerate(lines) if line.startswith("| Task | Start with |"))
	table = []
	for line in lines[header + 2:]:
		if not line.startswith("|"):
			break
		table.append(line)
	orphans = [line for line in lines[:header] if line.startswith("|")]
	receipts = [line for line in table + orphans if RECEIPT_LINK.search(line)]
	blocks = paragraphs(lines)
	return {
		"table_rows": len(table),
		"rows_outside_table": len(orphans),
		"rows_outside_table_first_cells": [row.strip("|").split("|")[0].strip() for row in orphans],
		"candidate_receipt_rows": len(receipts),
		"candidate_receipt_first_cells": [row.strip("|").split("|")[0].strip() for row in receipts],
		"paragraphs_in_index_block": len(blocks),
		"status_notes_in_index_block": status_notes(blocks),
		"route_rows": [row.strip("|").split("|")[0].strip() for row in table if not RECEIPT_LINK.search(row)],
	}


def blame_dates(repo: Path, rev: str, path: str, first: int, last: int) -> list[str]:
	out = git(repo, "blame", "--porcelain", "-L", f"{first},{last}", rev, "--", path).stdout.decode("utf-8", "replace")
	times = {}
	order = []
	current = None
	for line in out.split("\n"):
		match = re.match(r"^([0-9a-f]{40}) \d+ \d+", line)
		if match:
			current = match.group(1)
			order.append(current)
		elif line.startswith("committer-time ") and current:
			times[current] = int(line.split()[1])
	import datetime as dt
	return sorted({dt.datetime.fromtimestamp(times[sha], dt.timezone.utc).strftime("%Y-%m-%d") for sha in order if sha in times})


def finding_fields(register: str, finding: str) -> dict:
	match = re.search(rf"^## {re.escape(finding)}\n(.*?)(?=^## |\Z)", register, re.MULTILINE | re.DOTALL)
	if not match:
		return {"present": False}
	fields = {}
	for name in ("severity", "lifecycle"):
		row = re.search(rf"^\| {name} \| `?([^|`]+)`? \|", match.group(1), re.MULTILINE)
		fields[name] = row.group(1).strip() if row else None
	return {"present": True, **fields}


def measure(repo: Path, rev: str) -> dict:
	head = git(repo, "rev-parse", rev).stdout.decode().strip()
	head_date = git(repo, "show", "-s", "--format=%cs", head).stdout.decode().strip()
	docs = {key: text(repo, head, path) for key, path in DOCS.items()}
	result: dict = {"revision": head, "revision_date": head_date, "measured_by": "docs/handoffs/codex_chapter_guide_2026-10-31/tools/measure_chapter_guide.py"}

	result["last_change"] = {key: last_touch(repo, head, path) for key, path in DOCS.items() if key not in ("save_state", "ci_script", "probe_workflow")}
	guide_commit = result["last_change"]["chapter_guide"]["commit"]
	result["master_audit_commits_since_guide_last_change"] = int(git(
		repo, "rev-list", "--count", f"{guide_commit}..{head}", "--", DOCS["master_audit"]).stdout.decode().strip())

	master = docs["master_audit"] or ""
	level2 = sections(master, "## ")
	result["master_audit"] = {
		"bytes": len(master.encode("utf-8")),
		"lines": master.count("\n"),
		"planning_entry_updated_line": next((line.strip() for line in master.split("\n") if line.startswith("Planning guidance updated")), None),
		"section_bytes": {item["title"]: item["bytes"] for item in level2},
		"chapter_word_count_by_section": {
			item["title"]: count_term(item["text"], "chapter", ignore_case=True)
			for item in level2 if re.match(r"^(1|9|12|13)\. ", item["title"])
		},
		"task_index": task_index(master),
	}
	planning = next(item["text"] for item in level2 if item["title"].startswith("0. "))
	before_index = planning.split("<!-- AUDIT_TASK_INDEX_START -->", 1)[0].split("\n")
	planning_blocks = paragraphs(before_index)
	result["master_audit"]["planning_entry_before_index"] = {
		"paragraphs": len(planning_blocks),
		"status_notes": status_notes(planning_blocks),
	}
	planning_rows = table_rows(planning)
	chapter_row = next((row for row in planning_rows if row[0].startswith("Which chapter sources control")), None)
	result["master_audit"]["chapter_sources_row_links"] = re.findall(r"\]\(([^)]+)\)", chapter_row[1]) if chapter_row else None

	level3 = sections(master, "### ")
	area = next(item for item in level3 if item["title"].startswith("1.4 "))
	area_rows = table_rows(area["text"])[1:]
	first_row_line = area["first_line"] + next(i for i, line in enumerate(area["text"].split("\n")) if line.startswith("|")) + 2
	result["master_audit"]["area_scorecard"] = {
		"rows": [row[0] for row in area_rows],
		"rows_naming_a_chapter_or_day": [row[0] for row in area_rows if re.search(r"Day One|Day Two|Chapter|birthday", row[0], re.IGNORECASE)],
		"blame_dates": blame_dates(repo, head, DOCS["master_audit"], first_row_line, first_row_line + len(area_rows) - 1),
	}

	design06 = docs["design_language"] or ""
	families = Counter()
	for family, _number in set(re.findall(r"\bDL-([A-Z]+)-(\d{2})\b", design06)):
		families[family] += 1
	result["design_language"] = {
		"cast_mentions": {term: count_term(design06, term) for term in CAST_TERMS},
		"rule_families": dict(sorted(families.items())),
		"story_or_canon_family_present": any(name in families for name in ("STORY", "CANON", "CAST", "CHAPTER")),
	}

	game = docs["game_design"] or ""
	cast = next((item for item in sections(game, "## ") if "Cast and story" in item["title"]), None)
	result["game_design"] = {
		"cast_section_title": cast["title"] if cast else None,
		"cast_section_line_range": [cast["first_line"], cast["last_line"]] if cast else None,
		"cast_section_lines_including_heading": (cast["last_line"] - cast["first_line"] + 1) if cast else None,
		"lavender_clothing_lines": [n + 1 for n, line in enumerate(game.split("\n")) if "lavender clothing" in line],
	}

	register = json.loads(docs["owner_decisions"] or "{}")
	decisions = register.get("decisions", [])
	dates = Counter(row.get("date") for row in decisions)
	story_ids = [row["id"] for row in decisions if any(term in f"{row.get('id', '')} {row.get('subject', '')} {row.get('decision', '')}".lower() for term in STORY_TERMS)]
	result["owner_decisions"] = {
		"count": len(decisions),
		"earliest_date": min(dates) if dates else None,
		"by_date": dict(sorted(dates.items())),
		"ids_matching_story_terms": story_ids,
		"named": {
			name: next(({"date": row["date"], "decision": row["decision"]} for row in decisions if row["id"] == name), None)
			for name in NAMED_DECISIONS
		},
		"learning_branch_commit": LEARNING_COMMIT,
		"learning_branch_in_revision": git(repo, "merge-base", "--is-ancestor", LEARNING_COMMIT, head, check=False).returncode == 0,
	}

	directors = {}
	for path in DIRECTOR_FILES:
		body = text(repo, head, path)
		if body is None:
			directors[path] = None
			continue
		class_name = re.search(r"^class_name\s+(\w+)", body, re.MULTILINE)
		extends = re.search(r"^extends\s+(\S+)", body, re.MULTILINE)
		serialize = re.search(r"^func serialize_state\(\).*?(?=^func |\Z)", body, re.MULTILINE | re.DOTALL)
		directors[path] = {
			"newline_count": body.count("\n"),
			"class_name": class_name.group(1) if class_name else None,
			"extends": extends.group(1) if extends else None,
			"signals": re.findall(r"^signal\s+(\w+)", body, re.MULTILINE),
			"public_funcs": re.findall(r"^func\s+([a-z]\w*)\(", body, re.MULTILINE),
			"serialize_state_keys": len(re.findall(r'^\s*"(\w+)":', serialize.group(0), re.MULTILINE)) if serialize else None,
			"serialize_keys_on_main": len(re.findall(r'^\s*"\w+":\s*m\.', serialize.group(0), re.MULTILINE)) if serialize else None,
		}
	result["chapter_code"] = directors
	one = directors.get("scripts/day_one_director.gd") or {}
	two = directors.get("scripts/chapter_two_director.gd") or {}
	result["director_shared_interface"] = sorted(set(one.get("public_funcs", [])) & set(two.get("public_funcs", [])) | (set(one.get("signals", [])) & set(two.get("signals", []))))
	save_body = docs["save_state"] or ""
	result["chapter3_fields_assigned_on_main_by_save_state"] = len(set(re.findall(r"m\.(chapter3_\w+)\s*=", save_body)))
	architecture = docs["technical_architecture"] or ""
	result["technical_architecture_mentions"] = {
		"director_any_case": count_term(architecture, "director", ignore_case=True),
		**{name: architecture.count(name) for name in ("DayOneDirector", "ChapterTwoDirector", "day_one_director", "chapter_two_director", "Mode Platform")},
	}
	keys = sorted(set(SAVE_KEY.findall(docs["save_state"] or "")))
	result["save_state_keys"] = {
		prefix: [key for key in keys if key.startswith(prefix)]
		for prefix in ("chapter2_", "chapter3_", "day_one_", "day_two_", "fairy")
	}
	result["save_state_key_counts"] = {prefix: len(values) for prefix, values in result["save_state_keys"].items()}

	ci = docs["ci_script"] or ""
	workflow = docs["probe_workflow"] or ""
	result["trusted_roster"] = {
		name: {"ci_sh": bool(re.search(rf"\b{name}\b", ci)), "probes_yml": bool(re.search(rf"\b{name}\b", workflow))}
		for name in CHAPTER_PROBES
	}

	listing = git(repo, "ls-tree", "-r", "--name-only", head).stdout.decode("utf-8", "replace").split("\n")
	md_paths = sorted(path for path in listing if path.startswith("design/") and path.endswith(".md"))
	corpus_paths = md_paths + ["AGENTS.md", DOCS["master_audit"]]
	corpus = read_many(repo, head, corpus_paths)
	result["name_usage"] = {
		"scope": "tracked design/**/*.md plus AGENTS.md and the master audit; case-sensitive whole-phrase occurrences",
		"files": len(corpus),
		"occurrences": {term: sum(count_term(body, term) for body in corpus.values()) for term in NAME_TERMS},
	}

	result["planned_reference_files_present"] = {path: exists(repo, head, path) for path in PLANNED_REFERENCE_FILES}
	briefs = git(repo, "grep", "-l", "-E", r"^## 1\. Commission and boundaries", head, "--", "*.md", check=False).stdout.decode().split("\n")
	result["filled_chapter_briefs"] = sorted(line.split(":", 1)[1] for line in briefs if ":" in line and not line.endswith(DOCS["brief_template"]))
	cards = git(repo, "grep", "-i", "-l", "character card", head, "--", "*.md", check=False).stdout.decode().split("\n")
	result["files_mentioning_character_card"] = sorted(line.split(":", 1)[1] for line in cards if ":" in line)
	result["book_mentions"] = {
		key: count_term(docs[key] or "", "book", ignore_case=True) + count_term(docs[key] or "", "books", ignore_case=True)
		for key in ("chapter_guide", "reference_library", "brief_template", "new_chapter_recipe")
	}

	roadmap = docs["roadmap"] or ""
	grow = next((item for item in sections(roadmap, "## ") if item["title"].startswith("Grow")), None)
	result["roadmap"] = {
		"heading": roadmap.split("\n", 1)[0],
		"chapter_mentions": count_term(roadmap, "chapter", ignore_case=True),
		"grow_lane_rows": [row[0] for row in table_rows(grow["text"])[1:]] if grow else None,
		"grow_lane_lines": [line for line in grow["text"].split("\n")[1:] if line.strip()] if grow else None,
	}

	concept = {"in_revision": exists(repo, head, NORTHERN_CONCEPT), "rescue_commit": RESCUE_COMMIT}
	blob = git(repo, "cat-file", "blob", f"{RESCUE_COMMIT}:{NORTHERN_CONCEPT}", check=False)
	if blob.returncode == 0:
		concept["in_rescue_commit"] = True
		concept["sha256"] = hashlib.sha256(blob.stdout).hexdigest()
		concept["git_blob"] = git(repo, "rev-parse", f"{RESCUE_COMMIT}:{NORTHERN_CONCEPT}").stdout.decode().strip()
	else:
		concept["in_rescue_commit"] = False
	result["northern_concept"] = concept

	findings = docs["findings"] or ""
	result["findings"] = {name: finding_fields(findings, name) for name in FINDINGS}
	return result


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
	parser.add_argument("--repo", default=".")
	parser.add_argument("--rev", default="origin/dev")
	parser.add_argument("--output")
	args = parser.parse_args()
	data = measure(Path(args.repo), args.rev)
	payload = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
	if args.output:
		Path(args.output).write_bytes(payload)
	else:
		sys.stdout.buffer.write(payload)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
