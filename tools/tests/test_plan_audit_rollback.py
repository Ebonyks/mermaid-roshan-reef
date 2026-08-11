from __future__ import annotations

import contextlib
import ast
import io
import inspect
import re
import unittest
from dataclasses import replace
from pathlib import Path

from tools import plan_audit_rollback as planner


class AuditRollbackPlannerTests(unittest.TestCase):
	def test_written_ledger_matches_catalog_sources(self) -> None:
		ledger_path = Path(__file__).resolve().parents[2] / "audit" / "MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md"
		ledger = ledger_path.read_text(encoding="utf-8")
		sections: dict[str, str] = {}
		for part in re.split(r"(?=^### CHG-[0-9]{3} )", ledger, flags=re.MULTILINE):
			match = re.match(r"### (CHG-[0-9]{3}) ", part)
			if match:
				sections[match.group(1)] = part
		self.assertEqual(list(sections), [group.change_id for group in planner.CATALOG])
		constant_refs = {
			planner.AUDIT_BASELINE_COMMIT,
			planner.AUDIT_INTEGRATION_COMMIT,
			planner.AUDIT_INTEGRATION_PARENT,
			planner.AUDIT_UPSTREAM_PARENT,
		}
		for group in planner.CATALOG:
			with self.subTest(change_id=group.change_id):
				source_block = sections[group.change_id].split("- **Paths:**", 1)[0]
				source_refs = set(re.findall(r"\b[0-9a-f]{40}\b", source_block))
				expected_refs = set(group.commits)
				self.assertTrue(expected_refs.issubset(source_refs))
				self.assertEqual(source_refs - expected_refs - constant_refs, set())
	def test_catalog_has_fixed_change_log_ids(self) -> None:
		planner.validate_catalog()
		self.assertEqual(
			[group.change_id for group in planner.CATALOG],
			[f"CHG-{number:03d}" for number in range(1, 24)],
		)

	def test_catalog_rejects_duplicate_ids(self) -> None:
		duplicate = replace(planner.CATALOG[1], change_id=planner.CATALOG[0].change_id)
		with self.assertRaisesRegex(planner.CatalogError, "duplicate change ID"):
			planner.validate_catalog((planner.CATALOG[0], duplicate))

	def test_catalog_rejects_duplicate_commit_ownership(self) -> None:
		duplicate = replace(planner.CATALOG[1], commits=planner.CATALOG[0].commits[:1])
		with self.assertRaisesRegex(planner.CatalogError, "owned by both"):
			planner.validate_catalog((planner.CATALOG[0], duplicate))

	def test_catalog_rejects_path_traversal_and_absolute_paths(self) -> None:
		for unsafe in ("../escape", "tools/../../escape", "/absolute", "C:/absolute", "tools\\escape"):
			with self.subTest(unsafe=unsafe):
				group = replace(planner.CATALOG[0], paths=(unsafe,))
				with self.assertRaisesRegex(planner.CatalogError, "unsafe catalog path"):
					planner.validate_catalog((group,))

	def test_unknown_or_malformed_id_is_rejected(self) -> None:
		for change_id in ("CHG-999", "../CHG-001", "CHG-1", "CHG-001;git reset"):
			with self.subTest(change_id=change_id):
				with self.assertRaises(planner.UnknownChangeError):
					planner.select_group(change_id)

	def test_rendered_plan_is_deterministic_and_complete(self) -> None:
		group = planner.select_group("CHG-013")
		first = planner.render_plan(group)
		second = planner.render_plan(group)
		self.assertEqual(first, second)
		for marker in (
			"Exact baseline requirements:",
			planner.AUDIT_BASELINE_COMMIT,
			"Exact current/start requirements:",
			planner.AUDIT_INTEGRATION_COMMIT,
			"Owned commits",
			"Affected path selectors",
			"Coupled change IDs",
			"Required gates",
			"Branch-based plan",
		):
			self.assertIn(marker, first)

	def test_manual_group_refuses_command_emission(self) -> None:
		group = planner.select_group("CHG-009")
		with self.assertRaisesRegex(planner.UnsafePlanError, "policy-sensitive"):
			planner.render_script(group)

	def test_only_three_explicit_groups_emit_scripts(self) -> None:
		emittable = {"CHG-020", "CHG-021", "CHG-022"}
		for group in planner.CATALOG:
			with self.subTest(change_id=group.change_id):
				if group.change_id in emittable:
					self.assertTrue(planner.render_script(group).startswith("#!/usr/bin/env sh\n"))
				else:
					with self.assertRaises(planner.UnsafePlanError):
						planner.render_script(group)

	def test_reviewable_script_guards_clean_tree_before_git_mutation(self) -> None:
		script = planner.render_script(planner.select_group("CHG-020"))
		clean_guard = script.index("git status --porcelain=v1 --untracked-files=all")
		branch_creation = script.index("git switch -c")
		revert = script.index("git revert --no-commit")
		self.assertLess(clean_guard, branch_creation)
		self.assertLess(branch_creation, revert)
		self.assertIn(planner.AUDIT_INTEGRATION_COMMIT, script)
		self.assertIn(
			f"git revert --no-commit -m 1 {planner.AUDIT_UPSTREAM_PARENT}",
			script,
		)
		self.assertNotIn("git commit -m", script)
		self.assertNotIn("git reset", script)
		warning = "never combine it on one rollback branch with CHG-018"
		self.assertIn(warning, script)
		self.assertIn(warning, planner.render_plan(planner.select_group("CHG-020")))
		self.assertIn("known to stop on a scripts/games/picture_games.gd conflict", script)

	def test_castle_logo_script_has_exact_source_and_scope(self) -> None:
		group = planner.select_group("CHG-021")
		script = planner.render_script(group)
		self.assertIn("git revert --no-commit 9e75e8e392d34b784b9899e7434cdf954fb0e31d", script)
		for path in ("scripts/castle_logo_studio.gd", "scripts/probe_interaction.gd"):
			self.assertIn(path, script)

	def test_full_merge_script_is_explicit_parent_one_all_or_nothing(self) -> None:
		group = planner.select_group("CHG-022")
		self.assertTrue(group.all_or_nothing)
		script = planner.render_script(group)
		self.assertIn(
			f"git revert --no-commit -m 1 {planner.AUDIT_INTEGRATION_COMMIT}",
			script,
		)
		self.assertIn(
			f"git diff --cached --exit-code {planner.AUDIT_INTEGRATION_PARENT} --",
			script,
		)
		self.assertEqual(planner.AUDIT_INTEGRATION_COMMIT, "ad36ee9ffe4eae4d5c4183d0546d775de0218213")
		self.assertEqual(planner.AUDIT_INTEGRATION_PARENT, "7b5d1209063a22002118c364767d537b34b3dc6f")
		self.assertEqual(planner.AUDIT_UPSTREAM_PARENT, "245c16137fae82271dabac456d5ab04d843463a8")

	def test_planner_imports_no_git_or_filesystem_mutation_api(self) -> None:
		tree = ast.parse(inspect.getsource(planner))
		imported_roots: set[str] = set()
		for node in ast.walk(tree):
			if isinstance(node, ast.Import):
				imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
			elif isinstance(node, ast.ImportFrom) and node.module:
				imported_roots.add(node.module.split(".", 1)[0])
		self.assertTrue(imported_roots.isdisjoint({"os", "pathlib", "shutil", "subprocess"}))
		for node in ast.walk(tree):
			if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
				self.assertNotIn(node.func.id, {"open", "exec", "eval", "compile"})

	def test_cli_refuses_unknown_and_manual_emit_without_side_effects(self) -> None:
		stdout = io.StringIO()
		stderr = io.StringIO()
		with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
			unknown_result = planner.main(("CHG-999",))
		self.assertEqual(unknown_result, 2)
		self.assertEqual(stdout.getvalue(), "")
		self.assertIn("unknown change ID", stderr.getvalue())

		stdout = io.StringIO()
		stderr = io.StringIO()
		with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
			manual_result = planner.main(("CHG-017", "--emit-script"))
		self.assertEqual(manual_result, 3)
		self.assertEqual(stdout.getvalue(), "")
		self.assertIn("refused:", stderr.getvalue())


if __name__ == "__main__":
	unittest.main()
