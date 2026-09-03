#!/usr/bin/env python3
"""Claim-freshness gate for the governance documents.

The master audit and its satellites state many concrete numbers and
`file:line` anchors. Nothing else re-checks them, so they rot silently (the
2026-09-01 re-audit found a fifth of them drifted and six false). This tool
makes every registered claim re-measurable:

* `tools/claims_manifest.json` records each claim with a measurement from a
  CLOSED vocabulary of kinds (line counts, regex/literal counts, file globs,
  roster tokens, anchor tokens) — never arbitrary shell — plus the value the
  governing document states and a regex that document must still contain.
* Every claim is re-measured against the tree. `STALE_TREE` means the tree
  moved and the document (and manifest) must be updated; `STALE_DOC` means the
  document no longer states what the manifest says; `DRIFT` means an anchor's
  token still exists but at a different line; `FAIL` means an anchor's token is
  gone; `BROKEN` means the manifest itself cannot be evaluated.
* Every bare `path:line` anchor in the listed documents is swept: the file
  must resolve (directly, or as the unique suffix of one file under the search
  roots, so `games/side_scroll.gd` and `main.gd` both work) and the line must
  be inside it. An anchor whose neighbourhood on its line — the text between
  the adjacent anchors — carries a commit hash or historical wording is
  treated as pinned history and skipped.

Modes: default is report-only (only BROKEN exits 1, so an implementation
branch that legitimately moves code is not blocked by governance prose it
may not edit); `--strict` exits 1 on any non-OK claim and is the mode the
governance branch runs. `--refresh-anchors` rewrites drifted anchor lines in
the manifest (never expected counts — those are updated deliberately with the
document). `--stress` self-falsifies the checker. Output lines: `CLAIMS|...`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

REPO = Path(__file__).resolve().parents[1]
MANIFEST = Path("tools/claims_manifest.json")
DEFAULT_TOLERANCE = 12
ANCHOR_PATTERN = re.compile(
	r"`?((?:[\w.-]+/)*[\w.-]+\.(?:gd|py|yml|yaml|sh|cfg|godot|json|tres|tscn|md)):(\d+)(?:-(\d+))?((?:,\d+)+)?`?",
)
PINNED_PATTERN = re.compile(r"`[0-9a-f]{7,40}`|\bhistorical\b|\bat that checkpoint\b|\bthen at\b", re.I)


@dataclass(frozen=True)
class Result:
	claim_id: str
	status: str  # OK | STALE_TREE | STALE_DOC | DRIFT | FAIL | BROKEN
	detail: str
	line: int | None = None  # DRIFT only: the line the anchor token now sits on


# ---------------------------------------------------------------- measurements

def _globs(root: Path, claim: dict) -> list[Path]:
	patterns = claim.get("paths") or [claim.get("path", "")]
	exclude = re.compile(claim["exclude"]) if claim.get("exclude") else None
	files: list[Path] = []
	for pattern in patterns:
		for path in sorted(root.glob(pattern)):
			if not path.is_file():
				continue
			relative = path.relative_to(root).as_posix()
			if exclude is not None and exclude.search(relative):
				continue
			files.append(path)
	return files


def _flags(claim: dict) -> int:
	flags = re.MULTILINE
	if "i" in claim.get("flags", ""):
		flags |= re.IGNORECASE
	return flags


def _read(path: Path) -> str:
	return path.read_text(encoding="utf-8", errors="replace")


def measure_line_count(root: Path, claim: dict) -> int:
	return sum(len(_read(p).splitlines()) for p in _globs(root, claim))


def measure_regex_count(root: Path, claim: dict) -> int:
	pattern = re.compile(claim["pattern"], _flags(claim))
	return sum(len(pattern.findall(_read(p))) for p in _globs(root, claim))


def measure_regex_line_count(root: Path, claim: dict) -> int:
	pattern = re.compile(claim["pattern"], _flags(claim) & ~re.MULTILINE)
	return sum(
		1 for p in _globs(root, claim) for line in _read(p).splitlines() if pattern.search(line)
	)


def measure_regex_distinct(root: Path, claim: dict) -> int:
	pattern = re.compile(claim["pattern"], _flags(claim))
	values: set[str] = set()
	for p in _globs(root, claim):
		values.update(pattern.findall(_read(p)))
	return len(values)


def measure_literal_count(root: Path, claim: dict) -> int:
	literal = claim["literal"]
	return sum(_read(p).count(literal) for p in _globs(root, claim))


def measure_literal_line_count(root: Path, claim: dict) -> int:
	literal = claim["literal"]
	return sum(
		1 for p in _globs(root, claim) for line in _read(p).splitlines() if literal in line
	)


def measure_glob_count(root: Path, claim: dict) -> int:
	return len(_globs(root, claim))


def measure_files_over(root: Path, claim: dict) -> int:
	threshold = int(claim["threshold"])
	return sum(1 for p in _globs(root, claim) if len(_read(p).splitlines()) > threshold)


def measure_line_tokens(root: Path, claim: dict) -> int:
	line_pattern = re.compile(claim["line_regex"])
	token_pattern = re.compile(claim["token_regex"])
	for p in _globs(root, claim):
		for line in _read(p).splitlines():
			if line_pattern.search(line):
				return len(token_pattern.findall(line))
	raise ValueError(f"no line matches {claim['line_regex']!r}")


MEASURES: dict[str, Callable[[Path, dict], int]] = {
	"line_count": measure_line_count,
	"regex_count": measure_regex_count,
	"regex_line_count": measure_regex_line_count,
	"regex_distinct": measure_regex_distinct,
	"literal_count": measure_literal_count,
	"literal_line_count": measure_literal_line_count,
	"glob_count": measure_glob_count,
	"files_over": measure_files_over,
	"line_tokens": measure_line_tokens,
}


# -------------------------------------------------------------------- anchors

def resolve_anchor_path(root: Path, raw: str, search_roots: list[str]) -> Path | None:
	"""A path that exists relative to the root resolves directly; otherwise a
	bare basename or partial path (`games/side_scroll.gd`) resolves only when
	exactly one file under the search roots ends with it. `.` as a search root
	means the top level only; every other root is searched recursively."""
	direct = root / raw
	if direct.is_file():
		return direct
	suffix = "/" + raw
	matches: set[Path] = set()
	for base in search_roots:
		base_path = root / base
		if not base_path.is_dir():
			continue
		for candidate in base_path.glob("*" if base == "." else "**/*"):
			if not candidate.is_file() or ".git" in candidate.parts:
				continue
			if candidate.relative_to(root).as_posix().endswith(suffix):
				matches.add(candidate)
	unique = sorted(matches)
	return unique[0] if len(unique) == 1 else None


def check_anchor(root: Path, claim: dict, search_roots: list[str]) -> Result:
	path = resolve_anchor_path(root, claim["path"], search_roots)
	if path is None:
		return Result(claim["id"], "FAIL", f"anchor file not found or ambiguous: {claim['path']}")
	lines = _read(path).splitlines()
	line = int(claim["line"])
	token = claim["token"]
	tolerance = int(claim.get("tolerance", DEFAULT_TOLERANCE))
	if 1 <= line <= len(lines) and token in lines[line - 1]:
		return Result(claim["id"], "OK", f"{claim['path']}:{line} carries {token!r}")
	low = max(1, line - tolerance)
	high = min(len(lines), line + tolerance)
	for candidate in range(low, high + 1):
		if token in lines[candidate - 1]:
			return Result(
				claim["id"], "DRIFT",
				f"{claim['path']}: {token!r} moved from line {line} to line {candidate} (refresh the anchor)",
				line=candidate,
			)
	return Result(claim["id"], "FAIL", f"{claim['path']}: {token!r} not within ±{tolerance} of line {line}")


def sweep_bare_anchors(root: Path, documents: list[str], search_roots: list[str]) -> tuple[list[Result], dict[str, int]]:
	results: list[Result] = []
	stats = {"checked": 0, "pinned": 0, "failed": 0}
	for relative in documents:
		doc = root / relative
		if not doc.is_file():
			continue
		for line_number, line in enumerate(_read(doc).splitlines(), 1):
			matches = list(ANCHOR_PATTERN.finditer(line))
			for index, match in enumerate(matches):
				raw, start, end, extra = match.group(1), int(match.group(2)), match.group(3), match.group(4)
				# The anchor's neighbourhood is the text between its adjacent anchors
				# on the same line, so one pinned citation does not exempt a live
				# citation that merely shares the line.
				left = matches[index - 1].end() if index else 0
				right = matches[index + 1].start() if index + 1 < len(matches) else len(line)
				if PINNED_PATTERN.search(line[left:right]):
					stats["pinned"] += 1
					continue
				stats["checked"] += 1
				path = resolve_anchor_path(root, raw, search_roots)
				where = f"{relative}:{line_number}"
				if path is None:
					stats["failed"] += 1
					results.append(Result("anchor-sweep", "FAIL", f"{where}: {raw} does not resolve to one file"))
					continue
				total = len(_read(path).splitlines())
				numbers = [start] + ([int(end)] if end else []) + (
					[int(n) for n in extra.strip(",").split(",")] if extra else []
				)
				beyond = [n for n in numbers if n > total]
				if beyond:
					stats["failed"] += 1
					results.append(Result(
						"anchor-sweep", "FAIL",
						f"{where}: {raw}:{','.join(map(str, beyond))} is beyond the file's {total} lines",
					))
	return results, stats


# ---------------------------------------------------------------------- driver

def load_manifest(root: Path) -> dict:
	return json.loads(_read(root / MANIFEST))


def evaluate_claim(root: Path, claim: dict, search_roots: list[str]) -> list[Result]:
	kind = claim.get("kind", "")
	claim_id = claim.get("id", "<unnamed>")
	if kind == "anchor":
		results = [check_anchor(root, claim, search_roots)]
	elif kind in MEASURES:
		try:
			measured = MEASURES[kind](root, claim)
		except (KeyError, ValueError, OSError, re.error) as error:
			return [Result(claim_id, "BROKEN", f"cannot measure ({kind}): {error}")]
		expected = claim.get("expected")
		if expected is None:
			return [Result(claim_id, "BROKEN", "manifest claim has no expected value")]
		if measured == int(expected):
			results = [Result(claim_id, "OK", f"{kind} = {measured}")]
		else:
			results = [Result(
				claim_id, "STALE_TREE",
				f"{kind} measures {measured}, manifest/document say {expected} — update the document and the manifest together",
			)]
	else:
		return [Result(claim_id, "BROKEN", f"unknown claim kind {kind!r}")]
	doc = claim.get("doc")
	statement = claim.get("statement")
	if doc and statement:
		doc_path = root / doc
		if not doc_path.is_file():
			results.append(Result(claim_id, "BROKEN", f"document {doc} is missing"))
		elif re.search(statement, _read(doc_path)) is None:
			results.append(Result(
				claim_id, "STALE_DOC", f"{doc} no longer states /{statement}/ — refresh the manifest statement",
			))
	return results


def run(root: Path, manifest: dict) -> tuple[list[Result], dict[str, int]]:
	search_roots = manifest.get("search_roots", ["scripts", "tools", ".github", "."])
	results: list[Result] = []
	for claim in manifest.get("claims", []):
		results.extend(evaluate_claim(root, claim, search_roots))
	sweep, stats = sweep_bare_anchors(root, manifest.get("documents", []), search_roots)
	results.extend(sweep)
	return results, stats


def refresh_anchors(root: Path, manifest: dict) -> int:
	search_roots = manifest.get("search_roots", ["scripts", "tools", ".github", "."])
	refreshed = 0
	for claim in manifest.get("claims", []):
		if claim.get("kind") != "anchor":
			continue
		result = check_anchor(root, claim, search_roots)
		if result.status == "DRIFT" and result.line is not None:
			claim["line"] = result.line
			refreshed += 1
	(root / MANIFEST).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
	return refreshed


def stress() -> int:
	import tempfile
	checks: list[bool] = []
	with tempfile.TemporaryDirectory() as directory:
		root = Path(directory)
		(root / "a.gd").write_text("func one():\n\tpass\nfunc two():\n\tpass\n", encoding="utf-8")
		(root / "doc.md").write_text("The file has 2 functions (`a.gd:3`).\n", encoding="utf-8")
		good = {"id": "funcs", "kind": "regex_line_count", "paths": ["a.gd"], "pattern": r"^func ", "expected": 2, "doc": "doc.md", "statement": r"2 functions"}
		checks.append(all(r.status == "OK" for r in evaluate_claim(root, good, ["."])))
		bad = dict(good, expected=3)
		checks.append(any(r.status == "STALE_TREE" for r in evaluate_claim(root, bad, ["."])))
		stale_doc = dict(good, statement=r"9 functions")
		checks.append(any(r.status == "STALE_DOC" for r in evaluate_claim(root, stale_doc, ["."])))
		checks.append(any(r.status == "BROKEN" for r in evaluate_claim(root, {"id": "x", "kind": "nonsense"}, ["."])))
		anchor = {"id": "anc", "kind": "anchor", "path": "a.gd", "line": 3, "token": "func two"}
		checks.append(check_anchor(root, anchor, ["."]).status == "OK")
		checks.append(check_anchor(root, dict(anchor, line=1), ["."]).status == "DRIFT")
		checks.append(check_anchor(root, dict(anchor, token="func nine"), ["."]).status == "FAIL")
		(root / "doc2.md").write_text("See `a.gd:40` and pinned `a.gd:99` at commit `deadbeef1` historical.\n", encoding="utf-8")
		sweep, stats = sweep_bare_anchors(root, ["doc2.md"], ["."])
		checks.append(stats["failed"] == 1 and stats["pinned"] == 1)
	print(f"CLAIMS|STRESS|{sum(checks)}/{len(checks)}")
	return 0 if all(checks) else 1


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=REPO)
	parser.add_argument("--strict", action="store_true", help="exit 1 on any non-OK claim")
	parser.add_argument("--refresh-anchors", action="store_true", help="rewrite drifted anchor lines in the manifest")
	parser.add_argument("--stress", action="store_true")
	args = parser.parse_args(argv)
	if args.stress:
		return stress()
	root = args.root.resolve()
	try:
		manifest = load_manifest(root)
	except (OSError, json.JSONDecodeError) as error:
		print(f"CLAIMS|FAIL|manifest|{error}")
		return 1
	if args.refresh_anchors:
		print(f"CLAIMS|REFRESHED|{refresh_anchors(root, manifest)} anchor(s)")
		manifest = load_manifest(root)
	results, stats = run(root, manifest)
	tally = {status: sum(r.status == status for r in results) for status in ("OK", "DRIFT", "STALE_TREE", "STALE_DOC", "FAIL", "BROKEN")}
	print(
		"CLAIMS|CLAIMS={}|OK={OK}|DRIFT={DRIFT}|STALE_TREE={STALE_TREE}|STALE_DOC={STALE_DOC}|FAIL={FAIL}|BROKEN={BROKEN}".format(
			len(manifest.get("claims", [])), **tally,
		)
	)
	print(f"CLAIMS|ANCHORS|checked={stats['checked']}|pinned={stats['pinned']}|failed={stats['failed']}")
	blocking = {"BROKEN"} if not args.strict else {"DRIFT", "STALE_TREE", "STALE_DOC", "FAIL", "BROKEN"}
	exit_code = 0
	for result in results:
		if result.status == "OK":
			continue
		level = "FAIL" if result.status in blocking else "WARN"
		print(f"CLAIMS|{level}|{result.status}|{result.claim_id}|{result.detail}")
		if result.status in blocking:
			exit_code = 1
	mode = "strict" if args.strict else "report"
	print(f"CLAIMS|RESULT|{'ALL OK' if exit_code == 0 else 'ISSUES'}|mode={mode}")
	return exit_code


if __name__ == "__main__":
	sys.exit(main())
