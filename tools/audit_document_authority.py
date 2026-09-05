#!/usr/bin/env python3
"""Fail-closed authority and canonical-finding audit for Markdown sources."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


LEDGER_PATH = Path("design/05_DOC_LEDGER.md")
MASTER_PATH = Path("audit/MASTER_AUDIT_2026-08-09.md")
DESIGN_LANGUAGE_PATH = Path("design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md")
FINDINGS_PATH = Path("audit/findings/ACTIVE_FINDINGS_2026-08-13.md")
AUDIT_ITEM_PATTERN = re.compile(
	r"(?<![A-Z0-9-])(MA-(?:2D|[A-Z]+)-\d{3})(?![A-Z0-9-])",
)
AUDIT_FAMILY_PATTERN = re.compile(
	r"(?<![A-Z0-9-])(MA-(?:2D|[A-Z]+)-\*)(?![A-Z0-9-])",
)
DESIGN_RULE_PATTERN = re.compile(
	r"(?<![A-Z0-9-])(DL-[A-Z0-9]+(?:-[A-Z0-9]+)*(?:-\*)?)(?![A-Z0-9-])",
)

TERMINAL_LIFECYCLES = {
	"VERIFIED_FIXED",
	"DISMISSED_NOT_A_DEFECT",
	"DISMISSED_NOT_IN_PROJECT",
	"SUPERSEDED",
	"DUPLICATE",
}
LIFECYCLES = {
	"REPORTED_UNCONFIRMED",
	"CONFIRMED_OPEN",
	"IN_PROGRESS",
	"FIXED_PENDING_VERIFICATION",
	"VERIFIED_FIXED",
	"REGRESSED",
	"OWNER_DECISION_REQUIRED",
	"BLOCKED_EXTERNAL",
	"DEFERRED_WITH_REASON",
	"WAIVED_WITH_REASON",
	"DISMISSED_NOT_A_DEFECT",
	"DISMISSED_NOT_IN_PROJECT",
	"SUPERSEDED",
	"DUPLICATE",
}
SEVERITIES = {"P0", "P1", "P2", "P3"}
LEDGER_STATES = {"🟢", "🟣", "🔵", "🟠", "🟡", "⚪"}
MIXED_CONTEXT = {
	"SUPERSEDED",
	"HISTORICAL_EVIDENCE",
	"PROPOSAL_DEFERRED",
	"PARTIALLY SUPERSEDED",
	"UNCOMMITTED_CANDIDATE",
}
FINDING_FIELDS = (
	"id",
	"title",
	"rule_ids",
	"domain / zone",
	"source",
	"severity",
	"lifecycle",
	"verification",
	"reproduction",
	"child_impact",
	"evidence",
	"owner_decision",
	"fix",
	"surrounding_tests",
	"acceptance",
	"closure",
	"relationships",
	"history",
)
CURRENT_AUTHORITY_PATHS = {
	Path("AGENTS.md"),
	Path("CLAUDE.md"),
	MASTER_PATH,
	FINDINGS_PATH,
	*(Path("design") / f"0{index}_{name}.md" for index, name in (
		(0, "MASTER_INDEX"),
		(1, "GAME_DESIGN"),
		(2, "ART_DIRECTION"),
		(3, "TECHNICAL_ARCHITECTURE"),
		(4, "OPEN_WORK"),
		(5, "DOC_LEDGER"),
		(6, "COMPREHENSIVE_DESIGN_LANGUAGE"),
	)),
}
FORBIDDEN_CURRENT_PATTERNS = (
	("real 3D Roshan", re.compile(r"\breal[- ]3d\s+(?:mermaid\s+)?roshan\b")),
	("Sprite3D as final 2D", re.compile(r"\bsprite3d\b.{0,40}\bfinal\b.{0,20}\b2d\b")),
	("retaining existing GLBs", re.compile(
		r"(?:\b(?:landed|existing|current)\s+glbs?\b.{0,30}\b(?:stay|remain|keep)\b|"
		r"\bkeep\b.{0,30}\b(?:landed|existing|current)\s+glbs?\b)",
	)),
	("paused Meshy migration", re.compile(
		r"\bmeshy\s+(?:migration|work)\b.{0,30}\b(?:paused|on\s+hold)\b",
	)),
	("unsealed document-authority controls", re.compile(
		r"(?:\bdocumentation(?:\s*-\s*|\s+)control\b.{0,160}?\b"
		r"(?:working(?:\s*-\s*|\s+)slice|still\s+uncommitted)\b|"
		r"\bexhaustive\s+working(?:\s*-\s*|\s+)slice\s+authority\b)",
	)),
	("predecessor reported as latest full-local", re.compile(
		r"(?:\bff068db[0-9a-f]*\b`?\s+"
		r"(?:changes\s+only\s+(?:`?scripts/probe_opera\.gd`?|one\s+probe)\s+and\s+)?"
		r"is\s+(?:the\s+)?latest\s+"
		r"(?:completed\s+)?full[- ]local\s+checkpoint\b|"
		r"\blatest\s+(?:completed\s+)?full[- ]local\s+checkpoint\b.{0,240}?"
		r"\b(?:is|at)\s+`?ff068db[0-9a-f]*\b)",
	)),
	("cross-head release evidence presented as one candidate", re.compile(
		r"\bv3\s+latest\s+full[- ]local,\s*exact[- ]head\s+remote,\s*and\s+"
		r"exact[- ]head\s+android\s+dev\s+build\s+green\b",
	)),
	("stale stable-change-group count", re.compile(r"\b28\s+stable\s+change\s+groups\b")),
)
HISTORICAL_CONTEXT = (
	"superseded",
	"historical",
	"debt",
	"reject",
	"forbid",
	"removed",
	"not current",
	"never",
	"do not",
	"does not",
	"cannot",
	"not permit",
	"no active",
	"transition",
	"quoted claim",
)


@dataclass(frozen=True, order=True)
class Issue:
	check_id: str
	path: str
	detail: str


@dataclass(frozen=True)
class IndexItem:
	item_id: str
	severity: str
	lifecycle: str


def _read(path: Path) -> str:
	return path.read_text(encoding="utf-8")


def _split_table_row(line: str) -> list[str]:
	line = line.strip()
	if not line:
		return []
	if line.startswith("|"):
		line = line[1:]
	if line.endswith("|"):
		line = line[:-1]
	if "|" not in line:
		return []
	cells: list[str] = []
	cell: list[str] = []
	escaped = False
	in_code = False
	for character in line:
		if escaped:
			cell.append(character)
			escaped = False
			continue
		if character == "\\":
			cell.append(character)
			escaped = True
			continue
		if character == "`":
			in_code = not in_code
			cell.append(character)
			continue
		if character == "|" and not in_code:
			cells.append("".join(cell).strip())
			cell = []
			continue
		cell.append(character)
	cells.append("".join(cell).strip())
	return cells


def _markdown_inventory(root: Path) -> set[str]:
	command = [
		"git", "ls-files", "--cached", "--others", "--exclude-standard",
		"-z", "--", "*.md",
	]
	result = subprocess.run(
		command,
		cwd=root,
		check=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	)
	return {
		entry.replace("\\", "/")
		for entry in result.stdout.decode("utf-8").split("\0")
		if entry
	}


def _ledger_rows(text: str) -> tuple[dict[str, tuple[str, str]], list[Issue]]:
	rows: dict[str, tuple[str, str]] = {}
	issues: list[Issue] = []
	for line_number, line in enumerate(text.splitlines(), 1):
		cells = _split_table_row(line)
		if len(cells) < 3 or cells[0] in {"Doc", "---"}:
			continue
		paths = re.findall(r"`([^`]+\.md)`", cells[0])
		if not paths:
			continue
		if len(paths) != 1 or cells[0] != f"`{paths[0]}`":
			issues.append(Issue(
				"DOC002", str(LEDGER_PATH),
				f"line {line_number}: each authority row must name exactly one Markdown path",
			))
			continue
		if len(cells) != 3:
			issues.append(Issue(
				"DOC010", str(LEDGER_PATH),
				f"line {line_number}: authority row for {paths[0]} must have exactly three cells",
			))
			continue
		path = paths[0].replace("\\", "/")
		state = cells[1]
		note = cells[2].strip()
		if path in rows:
			issues.append(Issue(
				"DOC003", str(LEDGER_PATH),
				f"line {line_number}: duplicate authority row for {path}",
			))
			continue
		rows[path] = (state, note)
		if state not in LEDGER_STATES:
			issues.append(Issue(
				"DOC004", str(LEDGER_PATH),
				f"line {line_number}: {path} has invalid authority state {state!r}",
			))
		if len(note) < 12:
			issues.append(Issue(
				"DOC005", str(LEDGER_PATH),
				f"line {line_number}: {path} lacks explicit scoped authority text",
			))
		if state == "🟠" and not any(marker in note for marker in MIXED_CONTEXT):
			issues.append(Issue(
				"DOC006", str(LEDGER_PATH),
				f"line {line_number}: mixed row {path} lacks explicit supersession scope",
			))
		if state in {"🟢", "🟣", "🔵"} and (
			"Mixed authority" in note or "PARTIALLY SUPERSEDED" in note
		):
			issues.append(Issue(
				"DOC011", str(LEDGER_PATH),
				f"line {line_number}: {path} declares mixed/superseded scope but is not orange",
			))
	return rows, issues


def _index_items(master_text: str) -> tuple[dict[str, IndexItem], list[Issue]]:
	items: dict[str, IndexItem] = {}
	issues: list[Issue] = []
	for line_number, line in enumerate(master_text.splitlines(), 1):
		cells = _split_table_row(line)
		if not cells:
			continue
		first_ids = AUDIT_ITEM_PATTERN.findall(cells[0])
		if not first_ids:
			continue
		item_id = first_ids[0]
		if len(first_ids) != 1 or len(cells) < 3:
			issues.append(Issue(
				"DOC023", str(MASTER_PATH),
				f"line {line_number}: malformed severity/lifecycle row for {item_id}",
			))
			continue
		severity = cells[1]
		lifecycle_match = re.fullmatch(r"`([A-Z_]+)`", cells[2])
		if not re.fullmatch(r"P[0-3]", severity) or lifecycle_match is None:
			issues.append(Issue(
				"DOC023", str(MASTER_PATH),
				f"line {line_number}: malformed severity/lifecycle row for {item_id}",
			))
			continue
		lifecycle = lifecycle_match.group(1)
		if item_id in items:
			issues.append(Issue(
				"DOC020", str(MASTER_PATH),
				f"line {line_number}: duplicate indexed item {item_id}",
			))
			continue
		items[item_id] = IndexItem(item_id, severity, lifecycle)
		if severity not in SEVERITIES:
			issues.append(Issue(
				"DOC021", str(MASTER_PATH),
				f"line {line_number}: invalid severity {severity} for {item_id}",
			))
		if lifecycle not in LIFECYCLES:
			issues.append(Issue(
				"DOC022", str(MASTER_PATH),
				f"line {line_number}: invalid lifecycle {lifecycle} for {item_id}",
			))
	return items, issues


def _dl_definitions(design_text: str) -> tuple[set[str], list[Issue]]:
	definitions: set[str] = set()
	issues: list[Issue] = []
	for line_number, line in enumerate(design_text.splitlines(), 1):
		match = re.match(r"^`(DL-[A-Z0-9-]+)`\s+—", line)
		if match is None:
			continue
		rule_id = match.group(1)
		if rule_id in definitions:
			issues.append(Issue(
				"DOC030", str(DESIGN_LANGUAGE_PATH),
				f"line {line_number}: duplicate rule definition {rule_id}",
			))
		definitions.add(rule_id)
	return definitions, issues


def _finding_records(text: str) -> tuple[dict[str, dict[str, str]], list[Issue]]:
	records: dict[str, dict[str, str]] = {}
	issues: list[Issue] = []
	lines = text.splitlines()
	headings: list[tuple[int, str]] = []
	for index, line in enumerate(lines):
		match = re.match(r"^## (MA-[A-Z0-9-]+)(?:\s|$)", line)
		if match is not None:
			headings.append((index, match.group(1)))
	for position, (start, item_id) in enumerate(headings):
		end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
		if item_id in records:
			issues.append(Issue(
				"DOC040", str(FINDINGS_PATH), f"duplicate finding heading {item_id}",
			))
			continue
		if lines[start] != f"## {item_id}":
			issues.append(Issue(
				"DOC055", str(FINDINGS_PATH),
				f"line {start + 1}: canonical finding heading must be exactly ## {item_id}",
			))
		fields: dict[str, str] = {}
		for line_number in range(start + 1, end):
			cells = _split_table_row(lines[line_number])
			if len(cells) < 2:
				continue
			key = cells[0].strip("`")
			if key in {"Field", "---"}:
				continue
			if len(cells) != 2:
				issues.append(Issue(
					"DOC054", str(FINDINGS_PATH),
					f"line {line_number + 1}: {item_id} field {key} must have exactly two cells",
				))
				continue
			value = cells[1].strip()
			if key in fields:
				issues.append(Issue(
					"DOC041", str(FINDINGS_PATH),
					f"line {line_number + 1}: duplicate {key} field in {item_id}",
				))
			fields[key] = value
		records[item_id] = fields
	return records, issues


def _extract_token(value: str, pattern: str) -> str:
	match = re.search(pattern, value)
	return match.group(1) if match is not None else ""


def _canonical_issues(
	master_text: str,
	findings_text: str,
	design_text: str,
) -> list[Issue]:
	items, issues = _index_items(master_text)
	rules, rule_issues = _dl_definitions(design_text)
	records, record_issues = _finding_records(findings_text)
	issues.extend(rule_issues)
	issues.extend(record_issues)
	active = {
		item_id: item
		for item_id, item in items.items()
		if item.lifecycle not in TERMINAL_LIFECYCLES
	}
	missing = sorted(set(active) - set(records))
	extra = sorted(set(records) - set(items))
	for item_id in missing:
		issues.append(Issue(
			"DOC042", str(FINDINGS_PATH), f"active indexed item {item_id} has no canonical record",
		))
	for item_id in extra:
		issues.append(Issue(
			"DOC043", str(FINDINGS_PATH), f"record {item_id} is not an indexed item",
		))
	for item_id in sorted(set(items) & set(records)):
		item = items[item_id]
		fields = records[item_id]
		for field in FINDING_FIELDS:
			if not fields.get(field, "").strip():
				issues.append(Issue(
					"DOC044", str(FINDINGS_PATH), f"{item_id} is missing non-empty field {field}",
				))
		for field in sorted(set(fields) - set(FINDING_FIELDS)):
			issues.append(Issue(
				"DOC050", str(FINDINGS_PATH), f"{item_id} has unexpected field {field}",
			))
		if fields.get("id", "").strip() != f"`{item_id}`":
			issues.append(Issue(
				"DOC045", str(FINDINGS_PATH), f"{item_id} id field is not the exact backticked ID",
			))
		severity = fields.get("severity", "").strip()
		if severity != item.severity:
			issues.append(Issue(
				"DOC046", str(FINDINGS_PATH),
				f"{item_id} severity {severity!r} does not match index {item.severity}",
			))
		lifecycle_value = fields.get("lifecycle", "").strip()
		lifecycle = lifecycle_value[1:-1] if re.fullmatch(r"`[A-Z][A-Z_]+`", lifecycle_value) else lifecycle_value
		if lifecycle_value != f"`{item.lifecycle}`":
			issues.append(Issue(
				"DOC047", str(FINDINGS_PATH),
				f"{item_id} lifecycle {lifecycle!r} does not match index {item.lifecycle}",
			))
		rule_ids = sorted(set(re.findall(r"DL-[A-Z0-9-]+", fields.get("rule_ids", ""))))
		if not rule_ids:
			issues.append(Issue(
				"DOC051", str(FINDINGS_PATH), f"{item_id} does not cite a design-language rule",
			))
		for rule_id in rule_ids:
			if rule_id not in rules:
				issues.append(Issue(
					"DOC048", str(FINDINGS_PATH), f"{item_id} cites undefined rule {rule_id}",
				))
		for reference in sorted(set(AUDIT_ITEM_PATTERN.findall(" ".join(fields.values())))):
			if reference not in items:
				issues.append(Issue(
					"DOC053", str(FINDINGS_PATH),
					f"{item_id} cites undefined audit item {reference}",
				))
	section_five = master_text
	section_start = master_text.find("## 5.")
	section_end = master_text.find("## 6.", section_start + 1)
	if section_start >= 0 and section_end > section_start:
		section_five = master_text[section_start:section_end]
	linked_pairs = re.findall(
		r"\[`(MA-[A-Z0-9-]+)`\]\(findings/ACTIVE_FINDINGS_2026-08-13\.md#(ma-[a-z0-9-]+)\)",
		section_five,
	)
	linked_ids = {item_id for item_id, _ in linked_pairs}
	for item_id, anchor in linked_pairs:
		if anchor != item_id.lower():
			issues.append(Issue(
				"DOC052", str(MASTER_PATH),
				f"{item_id} canonical link has mismatched anchor {anchor}",
			))
	for item_id in sorted(active):
		if item_id not in linked_ids:
			issues.append(Issue(
				"DOC049", str(MASTER_PATH), f"{item_id} section-5 index lacks canonical-record link",
			))
	return issues


def _selected_authority_paths(
	root: Path,
	ledger_rows: dict[str, tuple[str, str]] | None = None,
) -> set[Path]:
	paths = set(CURRENT_AUTHORITY_PATHS)
	if ledger_rows is None:
		ledger_path = root / LEDGER_PATH
		ledger_rows = _ledger_rows(_read(ledger_path))[0] if ledger_path.is_file() else {}
	for path, (state, note) in ledger_rows.items():
		if state in {"🟢", "🟣", "🔵", "🟠"} or "BINDING_" in note \
				or "PROPOSED_CANONICAL" in note or "SUPPORTING_CURRENT" in note:
			paths.add(Path(path))
	return paths


def _reference_issues(
	root: Path,
	items: dict[str, IndexItem],
	rules: set[str],
	ledger_rows: dict[str, tuple[str, str]],
) -> list[Issue]:
	issues: list[Issue] = []
	for relative in sorted(_selected_authority_paths(root, ledger_rows)):
		path = root / relative
		if not path.is_file():
			continue
		text = _read(path)
		for reference in sorted(set(AUDIT_ITEM_PATTERN.findall(text)) - set(items)):
			issues.append(Issue(
				"DOC053", str(relative),
				f"current authority cites undefined audit item {reference}",
			))
		for reference in sorted(set(AUDIT_FAMILY_PATTERN.findall(text))):
			prefix = reference[:-1]
			if reference == "MA-*" or any(item_id.startswith(prefix) for item_id in items):
				continue
			issues.append(Issue(
				"DOC057", str(relative),
				f"current authority cites undefined audit-item family {reference}",
			))
		for reference in sorted(set(DESIGN_RULE_PATTERN.findall(text))):
			if reference == "DL-*":
				continue
			if reference.endswith("-*"):
				prefix = reference[:-1]
				if any(rule.startswith(prefix) for rule in rules):
					continue
			elif reference in rules:
				continue
			issues.append(Issue(
				"DOC056", str(relative),
				f"current authority cites undefined design rule {reference}",
			))
	return issues


def _markdown_integrity_issues(
	root: Path,
	paths: Iterable[Path],
) -> list[Issue]:
	issues: list[Issue] = []
	link_pattern = re.compile(
		r"!?\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\"']*[\"'])?\)",
	)
	for relative in sorted(set(paths)):
		path = root / relative
		if not path.is_file():
			continue
		lines = _read(path).splitlines()
		in_fence = False
		fence_character = ""
		fence_length = 0
		table_width: int | None = None
		pending_table_width: int | None = None
		for line_number, line in enumerate(lines, 1):
			if not in_fence:
				fence = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
				if fence is not None:
					marker = fence.group(1)
					in_fence = True
					fence_character = marker[0]
					fence_length = len(marker)
					table_width = None
					pending_table_width = None
					continue
			else:
				close = re.match(r"^ {0,3}(`{3,}|~{3,})[ \t]*$", line)
				if close is not None:
					marker = close.group(1)
					if marker[0] == fence_character and len(marker) >= fence_length:
						in_fence = False
						fence_character = ""
						fence_length = 0
						table_width = None
						pending_table_width = None
						continue
			if in_fence:
				continue
			cells = _split_table_row(line)
			is_separator = bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)
			if cells:
				if table_width is None and pending_table_width is None:
					pending_table_width = len(cells)
				elif table_width is None and is_separator:
					if len(cells) != pending_table_width:
						issues.append(Issue(
							"DOC071", str(relative),
							f"line {line_number}: table separator width {len(cells)} does not match {pending_table_width}",
						))
					table_width = pending_table_width
					pending_table_width = None
				elif table_width is None:
					# Adjacent pipe-rich prose is not a Markdown table until a separator
					# confirms the header; keep only the newest possible header.
					pending_table_width = len(cells)
				elif len(cells) != table_width:
					issues.append(Issue(
						"DOC071", str(relative),
						f"line {line_number}: table width {len(cells)} does not match {table_width}",
					))
			else:
				table_width = None
				pending_table_width = None
			for match in link_pattern.finditer(line):
				target = urllib.parse.unquote((match.group(1) or match.group(2)).strip())
				if not target or target.startswith(("#", "//")) \
						or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
					continue
				target = target.split("#", 1)[0].split("?", 1)[0]
				if not target:
					continue
				resolved = (path.parent / target).resolve()
				try:
					resolved.relative_to(root.resolve())
				except ValueError:
					issues.append(Issue(
						"DOC072", str(relative),
						f"line {line_number}: local link escapes repository: {target}",
					))
					continue
				if not resolved.exists():
					issues.append(Issue(
						"DOC072", str(relative),
						f"line {line_number}: local link target is missing: {target}",
					))
		if in_fence:
			issues.append(Issue(
				"DOC070", str(relative), "Markdown code fence is not closed",
			))
	return issues


def _paragraphs(text: str) -> Iterable[str]:
	for paragraph in re.split(r"\n\s*\n", text):
		clean = " ".join(line.strip() for line in paragraph.splitlines())
		if clean:
			yield clean


def _claim_units(text: str) -> Iterable[tuple[int, str]]:
	paragraph: list[tuple[int, str]] = []
	def flush() -> Iterable[tuple[int, str]]:
		if not paragraph:
			return ()
		start = paragraph[0][0]
		joined = " ".join(line.strip() for _, line in paragraph)
		return tuple((start, sentence) for sentence in re.split(r"(?<=[.!?;])\s+", joined) if sentence)
	for line_number, line in enumerate(text.splitlines(), 1):
		if line.startswith("|"):
			yield from flush()
			paragraph.clear()
			yield line_number, line
		elif not line.strip():
			yield from flush()
			paragraph.clear()
		else:
			paragraph.append((line_number, line))
	yield from flush()


def _has_nearby_context(text: str, position: int, phrase_length: int) -> bool:
	window = text[max(0, position - 120):position + phrase_length + 160]
	return any(context in window for context in HISTORICAL_CONTEXT)


def _authority_claim_issues(root: Path) -> list[Issue]:
	issues: list[Issue] = []
	for relative in sorted(_selected_authority_paths(root)):
		path = root / relative
		if not path.exists():
			continue
		for line_number, unit in _claim_units(_read(path)):
			lower = unit.lower()
			if not lower.strip():
				continue
			for label, pattern in FORBIDDEN_CURRENT_PATTERNS:
				match = pattern.search(lower)
				if match is not None and not _has_nearby_context(lower, match.start(), len(match.group(0))):
					issues.append(Issue(
						"DOC060", str(relative),
						f"line {line_number}: current authority presents forbidden claim without nearby historical/debt scope: {label}",
					))
			position = lower.find("godot 4.4")
			if position >= 0 and any(word in lower for word in ("baseline", "required", "release", "validate")) \
					and not _has_nearby_context(lower, position, len("godot 4.4")):
				issues.append(Issue(
					"DOC061", str(relative),
					f"line {line_number}: current authority presents Godot 4.4 as a release baseline",
				))
	return issues


def _planning_fact_issues(root: Path) -> list[Issue]:
	"""Check selected active planning facts; preserve historical engine evidence."""
	baseline_path = Path("tools/godot_baseline.json")
	spine_path = Path("design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md")
	save_path = Path("scripts/save_state.gd")
	party_path = Path("scripts/chapter_two_party_plan.gd")
	paths = (baseline_path, MASTER_PATH, spine_path, save_path, party_path)
	missing = [path for path in paths if not (root / path).is_file()]
	if missing:
		return [Issue("DOC070", str(path), "planning fact source is missing") for path in missing]
	try:
		baseline = json.loads(_read(root / baseline_path))
		version = baseline["version"]
		if not isinstance(version, str) or re.fullmatch(r"\d+\.\d+\.\d+", version) is None:
			raise ValueError("invalid version")
	except (ValueError, KeyError, TypeError) as error:
		return [Issue("DOC070", str(baseline_path), f"cannot read planning baseline: {error}")]
	issues: list[Issue] = []
	master = _read(root / MASTER_PATH)
	for number in (9, 12):
		section = re.search(rf"^## {number}\.[^\n]*\n(.*?)(?=^## |\Z)", master, re.M | re.S)
		if section is None:
			issues.append(Issue("DOC071", str(MASTER_PATH), f"active section {number} is missing"))
			continue
		versions = re.findall(r"\bGodot\s+(\d+\.\d+\.\d+)", section.group(1), re.I)
		if not versions or any(found != version for found in versions):
			issues.append(Issue("DOC071", str(MASTER_PATH),
				f"active section {number} must use Godot {version}; historical evidence belongs outside active gates"))
	spine = _read(root / spine_path)
	if "OPERA_ACTIVE_STAR_MASK" not in spine:
		issues.append(Issue("DOC072", str(spine_path), "global progression must reference OPERA_ACTIVE_STAR_MASK"))
	global_mask = re.search(r"^const OPERA_ACTIVE_STAR_MASK\s*:?=\s*(0x[0-9a-f]+)",
		_read(root / save_path), re.M | re.I)
	party_mask = re.search(r"^const ALL_PARTY_MASK\s*:?=\s*(0x[0-9a-f]+)",
		_read(root / party_path), re.M | re.I)
	if global_mask is None or party_mask is None:
		issues.append(Issue("DOC072", str(spine_path), "cannot resolve authoritative progression constants"))
		return issues
	for value in re.findall(r"Global Opera\s+(?:remains|is|uses)\s+`?(0x[0-9a-f]+)", spine, re.I):
		if int(value, 16) != int(global_mask.group(1), 16):
			issues.append(Issue("DOC072", str(spine_path), "global mask conflicts with SaveState"))
	declared = re.search(r"Chapter 2 is exactly `(0x[0-9a-f]+)`", spine, re.I)
	if declared is None or int(declared.group(1), 16) != int(party_mask.group(1), 16):
		issues.append(Issue("DOC073", str(spine_path), "chapter mask conflicts with ALL_PARTY_MASK"))
	sequence = re.search(r"Canonical sequence array: `\[([\d,\s]+)\]`", spine)
	actual = re.search(r"^const GUIDE_ORDER[^\n]*=\s*\[([\d,\s]+)\]", _read(root / party_path), re.M)
	if sequence is None or actual is None or re.findall(r"\d+", sequence.group(1)) != re.findall(r"\d+", actual.group(1)):
		issues.append(Issue("DOC073", str(spine_path), "chapter sequence conflicts with GUIDE_ORDER"))
	return issues


def audit(root: Path) -> tuple[list[Issue], dict[str, int]]:
	issues: list[Issue] = []
	ledger = root / LEDGER_PATH
	master = root / MASTER_PATH
	design = root / DESIGN_LANGUAGE_PATH
	findings = root / FINDINGS_PATH
	for required in (ledger, master, design, findings):
		if not required.is_file():
			issues.append(Issue("DOC001", str(required.relative_to(root)), "required authority file is missing"))
	if issues:
		return sorted(issues), {"inventory": 0, "ledger": 0, "active": 0, "records": 0}

	inventory = _markdown_inventory(root)
	ledger_rows, ledger_issues = _ledger_rows(_read(ledger))
	issues.extend(ledger_issues)
	for path in sorted(inventory):
		if not (root / path).is_file():
			issues.append(Issue("DOC009", path, "Git-declared Markdown path is missing from the working tree"))
	for path in sorted(inventory - set(ledger_rows)):
		issues.append(Issue("DOC007", str(LEDGER_PATH), f"tracked/unignored Markdown lacks authority row: {path}"))
	for path in sorted(set(ledger_rows) - inventory):
		issues.append(Issue("DOC008", str(LEDGER_PATH), f"authority row points to absent Markdown: {path}"))

	master_text = _read(master)
	findings_text = _read(findings)
	design_text = _read(design)
	issues.extend(_canonical_issues(master_text, findings_text, design_text))
	items, _ = _index_items(master_text)
	rules, _ = _dl_definitions(design_text)
	issues.extend(_reference_issues(root, items, rules, ledger_rows))
	# Structure and local-link integrity apply to the exhaustive inventory, even
	# when a document is historical: a broken source cannot remain auditable.
	issues.extend(_markdown_integrity_issues(root, {Path(path) for path in inventory}))
	issues.extend(_authority_claim_issues(root))
	issues.extend(_planning_fact_issues(root))
	records, _ = _finding_records(findings_text)
	active_count = sum(item.lifecycle not in TERMINAL_LIFECYCLES for item in items.values())
	counts = {
		"inventory": len(inventory),
		"ledger": len(ledger_rows),
		"active": active_count,
		"records": len(records),
	}
	return sorted(set(issues)), counts


def _stress() -> int:
	checks: list[bool] = []
	ledger, issues = _ledger_rows(
		"| Doc | | Note |\n|---|---|---|\n"
		"| `a.md`, `b.md` | 🟠 | `SUPERSEDED` grouping |\n"
	)
	checks.append(not ledger and any(issue.check_id == "DOC002" for issue in issues))
	ledger, issues = _ledger_rows(
		"| Doc | | Note |\n|---|---|---|\n"
		"| `a.md` | 🟢 | `BINDING_DOMAIN`; current |\n"
		"| `a.md` | 🟢 | `BINDING_DOMAIN`; duplicate |\n"
	)
	checks.append(len(ledger) == 1 and any(issue.check_id == "DOC003" for issue in issues))
	_, issues = _ledger_rows(
		"| Doc | | Note |\n|---|---|---|\n"
		"| `a.md` | 🟠 | mixed but unscoped current text |\n"
	)
	checks.append(any(issue.check_id == "DOC006" for issue in issues))
	_, issues = _index_items(
		"| `MA-X-001` | P4 | `CONFIRMED_OPEN` | V1 | bad severity | close |\n"
	)
	checks.append(any(issue.check_id == "DOC023" for issue in issues))
	paragraph = "The real 3D Roshan is the current product baseline."
	match = FORBIDDEN_CURRENT_PATTERNS[0][1].search(paragraph.lower())
	checks.append(match is not None and not _has_nearby_context(
		paragraph.lower(), match.start(), len(match.group(0)),
	))
	historical = "The real 3D Roshan direction is SUPERSEDED historical debt."
	match = FORBIDDEN_CURRENT_PATTERNS[0][1].search(historical.lower())
	checks.append(match is not None and _has_nearby_context(
		historical.lower(), match.start(), len(match.group(0)),
	))
	print(f"DOCAUTH|STRESS|{sum(checks)}/{len(checks)}")
	return 0 if all(checks) else 1


def main(argv: Sequence[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
	parser.add_argument("--stress", action="store_true")
	args = parser.parse_args(argv)
	if args.stress:
		return _stress()
	issues, counts = audit(args.root.resolve())
	print(
		"DOCAUTH|INVENTORY={inventory}|LEDGER={ledger}|ACTIVE={active}|RECORDS={records}".format(
			**counts,
		)
	)
	for issue in issues:
		print(f"DOCAUTH|FAIL|{issue.check_id}|{issue.path}|{issue.detail}")
	if issues:
		print(f"DOCAUTH|RESULT|{len(issues)} ISSUE(S)")
		return 1
	print("DOCAUTH|RESULT|ALL OK")
	return 0


if __name__ == "__main__":
	sys.exit(main())
