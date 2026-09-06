from __future__ import annotations

import json
import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import audit_development as development


def record() -> dict:
	return {
		"id": "test-change", "scope": "Test audit coverage", "baseline": "a" * 40,
		"rules": ["DL-AUTH-05"], "findings": [], "no_findings_reason": "New capability",
		"files": ["scripts/test.gd"], "acceptance_gaps": "No runtime acceptance claimed",
		"validation": [{"command": "test", "result": "PENDING", "evidence": "Not run yet"}],
	}


class DevelopmentAuditTests(unittest.TestCase):
	def errors(self, value: object) -> list[str]:
		return development.record_issues(value, {"DL-AUTH-05"}, {"MA-DOC-002"})

	def test_valid_feature_and_repair_records(self):
		value = record()
		self.assertEqual([], self.errors(value))
		value["findings"] = ["MA-DOC-002"]
		value.pop("no_findings_reason")
		self.assertEqual([], self.errors(value))

	def test_missing_fields_undefined_ids_and_invalid_types_fail(self):
		for key in record():
			with self.subTest(missing=key):
				value = record()
				value.pop(key)
				self.assertTrue(self.errors(value))
		for key, replacement in (("rules", ["DL-FAKE"]), ("rules", []), ("findings", ["MA-FAKE-001"]), ("findings", "MA-DOC-002"), ("validation", [{}]), ("no_findings_reason", None), ("baseline", "HEAD")):
			with self.subTest(field=key, value=replacement):
				value = record()
				value[key] = replacement
				self.assertTrue(self.errors(value))
		self.assertTrue(self.errors([]))

	def test_unsafe_paths_and_wildcards_fail(self):
		for path in ("../outside", "/outside", "C:/outside", "scripts/*", "scripts/", "scripts\\x.gd", 1):
			value = record()
			value["files"] = [path]
			self.assertTrue(self.errors(value), path)

	def test_verification_is_not_implicit_acceptance(self):
		value = record()
		for result in ("PASS", "FAIL", "PENDING", "NOT_APPLICABLE"):
			value["validation"][0]["result"] = result
			self.assertEqual([], self.errors(value))
		value["validation"][0]["result"] = "ACCEPTED"
		self.assertTrue(self.errors(value))

	def navigation_fixture(self, root: Path):
		for name in ("AGENTS.md", "CLAUDE.md"):
			(root / name).write_text("# Rules\n\n" + development.CONTRACT, encoding="utf-8")
		for path, body in {
			"scripts/ci.sh": 'python3 tools/audit_development.py --base auto \\\n\t|| { echo "AUDIT DEVELOPMENT COVERAGE FAIL"; exit 1; }\n',
			".github/workflows/probes.yml": "          python3 tools/audit_development.py --base auto\n",
			str(development.authority.MASTER_PATH): "## 0. Planning entry\n" + development.INDEX_START + "\n### Development task index\n[planning](#0-planning-entry)\n" + "\n".join(f"| {topic} | [rules](../design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md#1-rules) |" for topic in ("Every task", "New chapter", "Repair", "Code", "Art", "Touch", "Audio", "Cinematic", "Save", "Performance", "Acceptance")) + "\n" + development.INDEX_END + "\n## Sealed audit snapshot\n",
			str(development.authority.DESIGN_LANGUAGE_PATH): "## 1. Rules\n",
			str(development.authority.FINDINGS_PATH): "# Findings\n",
			str(development.authority.LEDGER_PATH): "# Ledger\n",
			"design/AUDIT_DEVELOPMENT_CONTRACT.md": "# Contract\n",
			"design/09_CHAPTER_DEVELOPMENT_GUIDE.md": "# Chapters\n",
		}.items():
			(root / path).parent.mkdir(parents=True, exist_ok=True)
			(root / path).write_text(body, encoding="utf-8")

	def test_entry_contract_and_index_mutations_fail(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			self.navigation_fixture(root)
			self.assertEqual([], development.navigation_issues(root))
			mutations = [
				("scripts/ci.sh", "exit 1", "exit 0"),
				(".github/workflows/probes.yml", "--base auto", ""),
				(str(development.authority.DESIGN_LANGUAGE_PATH), "## 1. Rules", "## 1. Rules\n## 2. New domain"),
				("AGENTS.md", development.CONTRACT, ""),
				("CLAUDE.md", "Before every", "Optionally before every"),
				(str(development.authority.MASTER_PATH), "| Audio |", "| Removed |"),
				(str(development.authority.MASTER_PATH), "#1-rules", "#missing"),
				(str(development.authority.MASTER_PATH), development.INDEX_END, ""),
			]
			for name, before, after in mutations:
				with self.subTest(file=name, mutation=before):
					path = root / name
					original = path.read_text(encoding="utf-8")
					path.write_text(original.replace(before, after), encoding="utf-8")
					self.assertTrue(development.navigation_issues(root))
					path.write_text(original, encoding="utf-8")

	def init_repo(self, root: Path) -> str:
		development.git(root, "init", "-q")
		development.git(root, "config", "user.email", "test@example.invalid")
		development.git(root, "config", "user.name", "Audit test")
		for name, text in {str(development.authority.DESIGN_LANGUAGE_PATH): "`DL-AUTH-05` — Apply this rule.\n", str(development.authority.MASTER_PATH): "# Master\n", "scripts/test.gd": "original\n"}.items():
			(root / name).parent.mkdir(parents=True, exist_ok=True)
			(root / name).write_text(text, encoding="utf-8")
		development.git(root, "add", ".")
		development.git(root, "commit", "-qm", "baseline")
		return development.git(root, "rev-parse", "HEAD")

	def test_real_git_coverage_add_delete_stale_record_and_bad_json(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			base = self.init_repo(root)
			value = record()
			value["baseline"] = base
			impact = root / development.IMPACT_DIR / "test.json"
			impact.parent.mkdir(parents=True)
			impact.write_text(json.dumps(value), encoding="utf-8")
			(root / "scripts/test.gd").write_text("changed\n", encoding="utf-8")
			self.assertEqual([], development.change_issues(root, base))
			(root / "scripts/new.gd").write_text("new\n", encoding="utf-8")
			self.assertTrue(any("scripts/new.gd" in e for e in development.change_issues(root, base)))
			value["files"].append("scripts/new.gd")
			impact.write_text(json.dumps(value), encoding="utf-8")
			(root / "scripts/test.gd").unlink()
			self.assertEqual([], development.change_issues(root, base))
			development.git(root, "add", ".")
			development.git(root, "commit", "-qm", "task")
			new_base = development.git(root, "rev-parse", "HEAD")
			(root / "scripts/new.gd").write_text("later unrelated change\n", encoding="utf-8")
			self.assertTrue(development.change_issues(root, new_base))
			impact.write_text("{", encoding="utf-8")
			self.assertTrue(any("invalid record" in e for e in development.change_issues(root, new_base)))
			impact.unlink()
			self.assertTrue(any("retain historical" in e for e in development.change_issues(root, new_base)))

	def test_auto_base_local_and_ci_events(self):
		with tempfile.TemporaryDirectory() as directory, mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "false", "GITHUB_EVENT_PATH": ""}):
			root = Path(directory)
			base = self.init_repo(root)
			development.git(root, "update-ref", "refs/remotes/origin/dev", base)
			(root / "scripts/test.gd").write_text("dirty\n", encoding="utf-8")
			self.assertEqual(base, development.resolve_base(root, "auto"))
			development.git(root, "add", ".")
			development.git(root, "commit", "-qm", "task")
			self.assertEqual(base, development.resolve_base(root, "auto"))
			development.git(root, "update-ref", "refs/remotes/origin/dev", "HEAD")
			self.assertEqual(base, development.resolve_base(root, "auto"))
			event = root / ".git/event.json"
			with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_PATH": str(event)}):
				for payload in ({"before": base}, {"pull_request": {"base": {"sha": base}}}, {"before": "0" * 40}):
					event.write_text(json.dumps(payload), encoding="utf-8")
					self.assertEqual(base, development.resolve_base(root, "auto"))

	def test_real_merge_checks_both_parents_and_rejects_missing_history(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			base = self.init_repo(root)
			development.git(root, "checkout", "-qb", "integration")
			(root / "scripts/sibling.gd").write_text("sibling\n", encoding="utf-8")
			development.git(root, "add", ".")
			development.git(root, "commit", "-qm", "sibling change")
			integration = development.git(root, "rev-parse", "HEAD")
			development.git(root, "checkout", "-qb", "task", base)
			(root / "scripts/test.gd").write_text("task\n", encoding="utf-8")
			value = record()
			value["baseline"] = base
			impact = root / development.IMPACT_DIR / "task.json"
			impact.parent.mkdir(parents=True)
			impact.write_text(json.dumps(value), encoding="utf-8")
			development.git(root, "add", ".")
			development.git(root, "commit", "-qm", "task change")
			development.git(root, "merge", "--no-ff", "-m", "reconcile", "integration")
			self.assertEqual([], development.change_issues(root, integration))
			self.assertTrue(any("sibling.gd" in e for e in development.change_issues(root, base)))
			value["baseline"] = "f" * 40
			impact.write_text(json.dumps(value), encoding="utf-8")
			self.assertTrue(any("baseline" in e for e in development.change_issues(root, integration)))
			with contextlib.redirect_stdout(io.StringIO()):
				self.assertEqual(1, development.main(["--root", str(root), "--base", "f" * 40]))

	def test_renames_require_old_and_new_path_coverage(self):
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			base = self.init_repo(root)
			development.git(root, "mv", "scripts/test.gd", "scripts/renamed.gd")
			value = record()
			value["baseline"] = base
			impact = root / development.IMPACT_DIR / "task.json"
			impact.parent.mkdir(parents=True)
			impact.write_text(json.dumps(value), encoding="utf-8")
			self.assertTrue(any("renamed.gd" in e for e in development.change_issues(root, base)))
			value["files"].append("scripts/renamed.gd")
			impact.write_text(json.dumps(value), encoding="utf-8")
			self.assertEqual([], development.change_issues(root, base))


if __name__ == "__main__":
	unittest.main()
