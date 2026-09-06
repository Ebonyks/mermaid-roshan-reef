#!/usr/bin/env python3
"""Validate audit entry points, navigation, and change-level audit traceability.

Document checks always run. --base adds a Git diff coverage gate; CI uses
--base auto to select the event's base. No check grants product acceptance.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Sequence

try:
	from tools import audit_document_authority as authority
except ModuleNotFoundError:
	import audit_document_authority as authority


CONTRACT = """## Mandatory master-audit development contract

Before every game development task, read the [master audit planning entry](audit/MASTER_AUDIT_2026-08-09.md#0-planning-entry) and its [task index](audit/MASTER_AUDIT_2026-08-09.md#development-task-index).
Read the applicable [design rules](design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md), [active findings](audit/findings/ACTIVE_FINDINGS_2026-08-13.md), and [document ledger](design/05_DOC_LEDGER.md) before choosing an implementation. The ledger determines which domain documents are current.

- At task start, record applicable `DL-*` rules, related `MA-*` findings (or an explicit reason none apply), scope, and required evidence using the [audit-impact guide](design/AUDIT_DEVELOPMENT_CONTRACT.md). New features need rule coverage even when they repair no finding.
- Recheck those sources when scope changes, during review, and before completion. Repairs follow master audit section 9; commissioned chapters follow the [chapter guide](design/09_CHAPTER_DEVELOPMENT_GUIDE.md). Apply `DL-AUTH-05` through `DL-AUTH-07` throughout.
- Commit a new or updated `design/audit_impacts/*.json` record covering every changed project file. Update affected finding lifecycle/history, the master index, and document-ledger entries in the same change when their facts or authority change. Do not fabricate a defect or rewrite unchanged findings to satisfy paperwork.
- Before commit/push, run `python -B tools/audit_document_authority.py` and `python -B tools/audit_development.py --base auto`, plus all existing applicable gates. Missing coverage or broken authority/navigation blocks the change. Preserve exact baseline and evidence references in the impact record.
- Report implementation, machine verification, and outstanding visual/device/child/owner acceptance separately. Green regression checks do not establish master-audit satisfaction. Existing security, protected-content, save, owner-decision, and release precedence remains unchanged; this contract grants no new approval checkpoint or release authority.

"""
IMPACT_DIR = "design/audit_impacts/"
INDEX_START = "<!-- AUDIT_TASK_INDEX_START -->"
INDEX_END = "<!-- AUDIT_TASK_INDEX_END -->"


def git(root: Path, *args: str) -> str:
	return subprocess.check_output(
		["git", *args], cwd=root, text=True, encoding="utf-8", stderr=subprocess.PIPE,
	).strip()


def pending_merge_head(root: Path) -> str | None:
	try:
		return git(root, "rev-parse", "--verify", "MERGE_HEAD")
	except subprocess.CalledProcessError:
		return None


def validate_ancestor(root: Path, revision: str) -> None:
	try:
		git(root, "merge-base", "--is-ancestor", revision, "HEAD")
	except subprocess.CalledProcessError:
		merge_head = pending_merge_head(root)
		if not merge_head:
			raise
		git(root, "merge-base", "--is-ancestor", revision, merge_head)


def heading_anchors(text: str) -> set[str]:
	"""GitHub-style anchors for the plain Markdown headings used by our index."""
	counts: dict[str, int] = {}
	anchors: set[str] = set()
	in_fence = False
	for line in text.splitlines():
		if line.startswith(("```", "~~~")):
			in_fence = not in_fence
		if in_fence or not re.match(r"^#{1,6} ", line):
			continue
		heading = re.sub(r"^#+\s+", "", line).strip().lower()
		anchor = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
		count = counts.get(anchor, 0)
		counts[anchor] = count + 1
		anchors.add(f"{anchor}-{count}" if count else anchor)
	return anchors


def navigation_issues(root: Path) -> list[str]:
	issues: list[str] = []
	for name in ("scripts/ci.sh", ".github/workflows/probes.yml"):
		path = root / name
		text = path.read_text(encoding="utf-8") if path.is_file() else ""
		command = r"python3 tools/audit_development\.py --base auto"
		if name.endswith(".sh"):
			connected = re.search(r"(?m)^" + command + r" \\\n\s*\|\| \{[^\n]*exit 1; \}", text)
		else:
			connected = re.search(r"(?m)^ +" + command + r"$", text)
		if not connected:
			issues.append(f"{name}: blocking audit change-coverage invocation missing or changed")
	for name in ("AGENTS.md", "CLAUDE.md"):
		path = root / name
		text = path.read_text(encoding="utf-8") if path.is_file() else ""
		if text.count(CONTRACT) != 1 or text.find(CONTRACT) > 2000:
			issues.append(f"{name}: mandatory contract missing, changed, duplicated, or below entry point")
	master = root / authority.MASTER_PATH
	text = master.read_text(encoding="utf-8") if master.is_file() else ""
	if text.count(INDEX_START) != 1 or text.count(INDEX_END) != 1:
		return issues + ["master audit: task index markers missing or duplicated"]
	index = text.split(INDEX_START, 1)[1].split(INDEX_END, 1)[0]
	if text.index(INDEX_START) > text.find("## Sealed audit snapshot"):
		issues.append("master audit: task index must precede sealed evidence")
	link_pattern = r"\[[^\]]+\]\(([^)]+)\)"
	for topic in ("Every task", "New chapter", "Repair", "Code", "Art", "Touch", "Audio", "Cinematic", "Save", "Performance", "Acceptance"):
		rows = [line for line in index.splitlines() if line.startswith(f"| {topic} |")]
		if len(rows) != 1 or not re.search(link_pattern, rows[0]):
			issues.append(f"master audit: missing task route {topic}")
	links = [(master.parent, target) for target in re.findall(link_pattern, index)]
	index_targets = {target for _, target in links}
	for relative, prefix in ((authority.MASTER_PATH, ""), (authority.DESIGN_LANGUAGE_PATH, "../" + authority.DESIGN_LANGUAGE_PATH.as_posix())):
		path = root / relative
		if not path.is_file():
			issues.append(f"index source missing: {relative}")
			continue
		for heading in path.read_text(encoding="utf-8").splitlines():
			if re.match(r"^## [0-9]+\. ", heading):
				target = prefix + "#" + next(iter(heading_anchors(heading)))
				if target not in index_targets:
					issues.append(f"numbered authority section absent from task index: {target}")
	links.extend((root, target) for target in re.findall(link_pattern, CONTRACT))
	for base, target in links:
		filename, _, fragment = target.partition("#")
		path = (base / filename).resolve() if filename else master.resolve()
		if not path.is_relative_to(root.resolve()) or not path.is_file():
			issues.append(f"navigation target missing or outside repository: {target}")
		elif fragment and fragment not in heading_anchors(path.read_text(encoding="utf-8")):
			issues.append(f"navigation heading missing: {target}")
	return issues


def record_issues(record: object, rules: set[str], findings: set[str]) -> list[str]:
	if not isinstance(record, dict):
		return ["record must be an object"]
	issues: list[str] = []
	for field in ("id", "scope", "baseline", "acceptance_gaps"):
		if not isinstance(record.get(field), str) or not record[field].strip():
			issues.append(f"missing {field}")
	if not re.fullmatch(r"[0-9a-f]{40}", str(record.get("baseline", ""))):
		issues.append("baseline must be a full Git commit SHA")
	for field, known in (("rules", rules), ("findings", findings)):
		values = record.get(field)
		if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
			issues.append(f"{field} must be a list of IDs")
		elif any(v not in known for v in values):
			issues.append(f"undefined {field} reference")
	if not record.get("rules"):
		issues.append("at least one applicable design rule is required")
	if record.get("findings") == [] and (not isinstance(record.get("no_findings_reason"), str) or not record["no_findings_reason"].strip()):
		issues.append("no findings requires an explicit reason")
	files = record.get("files")
	if not isinstance(files, list) or not files:
		issues.append("files must be a nonempty list of exact repository paths")
	else:
		for name in files:
			if not isinstance(name, str) or not name or "\\" in name or any(c in name for c in "*?:") or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts or name.endswith("/"):
				issues.append("files contain an unsafe path, directory, or wildcard")
	validation = record.get("validation")
	if not isinstance(validation, list) or not validation:
		issues.append("validation must name commands, results, and evidence")
	else:
		for check in validation:
			if not isinstance(check, dict) or any(not isinstance(check.get(k), str) or not check[k].strip() for k in ("command", "result", "evidence")):
				issues.append("validation requires command, result, and evidence")
			elif check["result"] not in {"PASS", "FAIL", "PENDING", "NOT_APPLICABLE"}:
				issues.append("invalid validation result")
	return issues


def resolve_base(root: Path, requested: str) -> str:
	if requested != "auto":
		return git(root, "rev-parse", "--verify", requested + "^{commit}")
	event_path = os.environ.get("GITHUB_EVENT_PATH")
	if os.environ.get("GITHUB_ACTIONS") == "true" and event_path:
		event = json.loads(Path(event_path).read_text(encoding="utf-8"))
		if "pull_request" in event:
			return git(root, "merge-base", "HEAD", event["pull_request"]["base"]["sha"])
		before = event.get("before", "")
		if before and before != "0" * 40:
			return git(root, "rev-parse", "--verify", before + "^{commit}")
	merge_head = pending_merge_head(root)
	if merge_head:
		integration = git(root, "rev-parse", "origin/dev")
		if git(root, "merge-base", integration, merge_head) == integration:
			return integration
	# Topic branch / local work: the integration merge-base covers the full task.
	base = git(root, "merge-base", "HEAD", "origin/dev")
	if base == git(root, "rev-parse", "HEAD"):
		if os.environ.get("GITHUB_ACTIONS") != "true" and (git(root, "diff", "--name-only", "HEAD", "--") or git(root, "ls-files", "--others", "--exclude-standard")):
			return base
		# On integration HEAD, include its final commit/merge rather than an empty diff.
		return git(root, "rev-parse", "HEAD^1")
	return base


def change_issues(root: Path, base: str) -> list[str]:
	if git(root, "diff", "--name-only", "--diff-filter=U"):
		return ["resolve merge conflicts before checking audit coverage"]
	validate_ancestor(root, base)
	changed = set(filter(None, git(root, "diff", "--name-only", "--no-renames", "-z", base, "--").split("\0")))
	changed.update(filter(None, git(root, "ls-files", "--others", "--exclude-standard", "-z").split("\0")))
	if not changed:
		return []
	rules, _ = authority._dl_definitions((root / authority.DESIGN_LANGUAGE_PATH).read_text(encoding="utf-8"))
	findings, _ = authority._index_items((root / authority.MASTER_PATH).read_text(encoding="utf-8"))
	covered: set[str] = set()
	issues: list[str] = []
	for name in sorted(changed):
		if not name.startswith(IMPACT_DIR) or not name.endswith(".json"):
			continue
		if not (root / name).is_file():
			issues.append(f"{name}: retain historical impact records at their stable paths")
			continue
		try:
			record = json.loads((root / name).read_text(encoding="utf-8"))
			errors = record_issues(record, rules, set(findings))
			if not errors:
				validate_ancestor(root, record["baseline"])
				covered.update(record["files"])
			issues.extend(f"{name}: {error}" for error in errors)
		except (ValueError, OSError, subprocess.CalledProcessError) as exc:
			issues.append(f"{name}: invalid record or unavailable/non-ancestor baseline ({type(exc).__name__})")
	# Records are self-describing metadata; all other additions/deletions need coverage.
	required = {p for p in changed if not (p.startswith(IMPACT_DIR) and p.endswith(".json"))}
	issues.extend(f"no changed audit-impact record covers {p}" for p in sorted(required - covered))
	return issues


def main(argv: Sequence[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
	parser.add_argument("--base", help="Git commit/ref or auto; includes working-tree and untracked changes")
	args = parser.parse_args(argv)
	root = args.root.resolve()
	try:
		issues = navigation_issues(root)
		if args.base:
			base = resolve_base(root, args.base)
			print(f"AUDITDEV|BASE|{base}")
			issues.extend(change_issues(root, base))
	except (OSError, ValueError, subprocess.CalledProcessError) as exc:
		issues = [f"unable to establish audit inputs: {type(exc).__name__}"]
	for issue in issues:
		print(f"AUDITDEV|FAIL|{issue}")
	print(f"AUDITDEV|RESULT|{len(issues)} ISSUE(S)" if issues else "AUDITDEV|RESULT|ALL OK")
	return 1 if issues else 0


if __name__ == "__main__":
	raise SystemExit(main())
