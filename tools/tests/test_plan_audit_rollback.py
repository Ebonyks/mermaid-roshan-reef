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
			planner.AUDIT_RECONCILIATION_COMMIT,
			planner.AUDIT_RECONCILIATION_PARENT,
			planner.AUDIT_RECONCILIATION_AUDIT_PARENT,
			planner.AUDIT_OPERA_RETIREMENT_PARENT,
		}
		for group in planner.CATALOG:
			with self.subTest(change_id=group.change_id):
				source_block = sections[group.change_id].split("- **Paths:**", 1)[0]
				source_refs = set(re.findall(r"\b[0-9a-f]{40}\b", source_block))
				expected_refs = set(group.commits)
				self.assertTrue(expected_refs.issubset(source_refs))
				self.assertEqual(source_refs - expected_refs - constant_refs, set())
		self.assertIn("all 64 trusted local probes green", sections["CHG-024"])
		self.assertIn("Exact-head remote CI was still pending", sections["CHG-024"])
	def test_catalog_has_fixed_change_log_ids(self) -> None:
		planner.validate_catalog()
		self.assertEqual(
			[group.change_id for group in planner.CATALOG],
			[f"CHG-{number:03d}" for number in range(1, 27)],
		)
		owned_refs = [commit for group in planner.CATALOG for commit in group.commits]
		self.assertEqual(len(owned_refs), 71)
		self.assertEqual(len(set(owned_refs)), 71)
		self.assertEqual(
			sum(group.safety != planner.MANUAL for group in planner.CATALOG),
			4,
		)

	def test_followup_commit_anchors_are_catalogued(self) -> None:
		self.assertIn(
			"dacef1405b6a8cb470117e824aebac3a8ca500af",
			planner.select_group("CHG-005").commits,
		)
		self.assertIn(
			"fe10ffd2f36606eaad99e1e8881c1c84ffc5fa08",
			planner.select_group("CHG-015").commits,
		)
		self.assertIn(
			planner.AUDIT_CHG015_FOLLOWUP_COMMIT,
			planner.select_group("CHG-015").commits,
		)
		for change_id in ("CHG-005", "CHG-023"):
			with self.subTest(rollback_start=change_id):
				self.assertEqual(
					planner.select_group(change_id).rollback_start,
					planner.AUDIT_CATALOG_COMMIT,
				)
		self.assertEqual(
			planner.select_group("CHG-015").rollback_start,
			planner.AUDIT_CHG015_FOLLOWUP_COMMIT,
		)
		self.assertEqual(
			planner.select_group("CHG-025").rollback_start,
			planner.AUDIT_SCORECARD_COMMIT,
		)
		for change_id in ("CHG-020", "CHG-021", "CHG-022"):
			with self.subTest(integration_start=change_id):
				self.assertEqual(
					planner.select_group(change_id).rollback_start,
					planner.AUDIT_INTEGRATION_COMMIT,
				)
		repo_root = Path(__file__).resolve().parents[2]
		expected_followup_paths = {
			"CHG-005": {
				".github/workflows/probes.yml",
				"audit/MASTER_AUDIT_2026-08-09.md",
				"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",
				"scripts/ci.sh",
				"tools/audit_probe_parity.py",
				"tools/check_grade_headroom.py",
				"tools/tests/test_check_grade_headroom.py",
			},
			"CHG-015": {
				"assets/flats/castle/interactions_v4/castle_interactions_v4.json",
				"assets_src/castle/interactions_v4/castle_interaction_frame_approval_ledger.json",
				"assets_src/imagegen/opera_minigame_quality_2026-08-09/PROVENANCE.json",
				"assets_src/imagegen/opera_minigame_quality_2026-08-09/REVIEW.md",
				"audit/MASTER_AUDIT_2026-08-09.md",
				"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",
				"tools/build_castle_interaction_v4_delivery.py",
				"tools/build_castle_native_interactions_v4.py",
				"tools/plan_audit_rollback.py",
				"tools/prepare_opera_minigame_art.py",
				"tools/test_build_castle_interaction_v4_delivery.py",
				"tools/tests/test_prepare_opera_minigame_art.py",
			},
		}
		for change_id, expected_paths in expected_followup_paths.items():
			self.assertEqual(set(planner.select_group(change_id).paths), expected_paths)
			for path in planner.select_group(change_id).paths:
				with self.subTest(existing_path=change_id, path=path):
					self.assertTrue((repo_root / path).exists(), path)
		self.assertNotIn(
			"tools/tests/test_audit_probe_parity.py",
			planner.select_group("CHG-005").paths,
		)
		self.assertIn(
			"python -m unittest tools.tests.test_check_grade_headroom",
			planner.select_group("CHG-005").gates,
		)
		self.assertIn(
			"python tools/prepare_opera_minigame_art.py --check-only",
			planner.select_group("CHG-015").gates,
		)
		self.assertIn(
			"python -B -m unittest tools.tests.test_prepare_opera_minigame_art -v",
			planner.select_group("CHG-015").gates,
		)
		process = planner.select_group("CHG-023")
		self.assertEqual(process.commits, ("57bc08d1220594fbabcab15362b5685a9f8514e6",))
		self.assertFalse(process.pending_commit)
		self.assertIn(
			f"Use exactly {planner.AUDIT_CATALOG_COMMIT} as the rollback branch start.",
			planner.render_plan(process),
		)

	def test_human_scorecard_record_is_bounded_and_complete(self) -> None:
		group = planner.select_group("CHG-025")
		self.assertEqual(group.commits, (planner.AUDIT_SCORECARD_COMMIT,))
		self.assertEqual(group.baseline_commit, planner.AUDIT_CHG015_FOLLOWUP_COMMIT)
		self.assertEqual(group.rollback_start, planner.AUDIT_SCORECARD_COMMIT)
		self.assertEqual(
			group.dependencies,
			("CHG-005", "CHG-011", "CHG-015", "CHG-023", "CHG-024"),
		)
		self.assertEqual(group.safety, planner.MANUAL)
		self.assertEqual(
			set(group.paths),
			{
				"audit/MASTER_AUDIT_2026-08-09.md",
				"audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md",
				"design/00_MASTER_INDEX.md",
				"design/03_TECHNICAL_ARCHITECTURE.md",
				"design/04_OPEN_WORK.md",
				"design/05_DOC_LEDGER.md",
				"design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md",
				"tools/plan_audit_rollback.py",
				"tools/tests/test_plan_audit_rollback.py",
			},
		)
		root = Path(__file__).resolve().parents[2]
		master = (root / "audit" / "MASTER_AUDIT_2026-08-09.md").read_text(encoding="utf-8")
		for marker in (
			"### 1.1 How to read the 1–5 ratings",
			"### 1.3 Whole-game systems scorecard",
			"### 1.5 Non-Opera activity scorecard",
			"### 1.6 Current Opera career scorecard",
			"### 1.7 Opera House version and branch comparison",
			"Seek (Evie/Lamb-a')",
			"Game-wide animation-doubling branch `20e9b1f2`",
		):
			self.assertIn(marker, master)
		self.assertIn("1,132 findings", master)
		self.assertIn("never merge wholesale", master)
		with self.assertRaises(planner.UnsafePlanError):
			planner.render_script(group)

	def test_opera_retirement_record_is_exact_manual_and_save_safe(self) -> None:
		group = planner.select_group("CHG-026")
		self.assertEqual(group.commits, (planner.AUDIT_OPERA_RETIREMENT_COMMIT,))
		self.assertEqual(group.baseline_commit, planner.AUDIT_OPERA_RETIREMENT_PARENT)
		self.assertEqual(group.rollback_start, planner.AUDIT_OPERA_RETIREMENT_COMMIT)
		self.assertEqual(
			planner.AUDIT_OPERA_RETIREMENT_COMMIT,
			"e2c25878f6b9c64526d0686c426a9f29c5f1b3da",
		)
		self.assertEqual(
			planner.AUDIT_OPERA_RETIREMENT_PARENT,
			"41087f6634a416540b23a984d1f445b0bdab5f2f",
		)
		self.assertEqual(
			set(group.paths),
			{
				"audit/MASTER_AUDIT_2026-08-09.md",
				"design/00_MASTER_INDEX.md",
				"design/01_GAME_DESIGN.md",
				"design/03_TECHNICAL_ARCHITECTURE.md",
				"design/04_OPEN_WORK.md",
				"design/05_DOC_LEDGER.md",
				"design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md",
				"scripts/hit_engine.gd",
				"scripts/kart.gd",
				"scripts/living_world.gd",
				"scripts/living_world_catalog.gd",
				"scripts/main.gd",
				"scripts/opera_act.gd",
				"scripts/opera_house.gd",
				"scripts/opera_lobby_2d.gd",
				"scripts/player.gd",
				"scripts/probe_audio.gd",
				"scripts/probe_castle_pearl_art.gd",
				"scripts/probe_imp_animation_art.gd",
				"scripts/probe_living_world.gd",
				"scripts/probe_load.gd",
				"scripts/probe_opera.gd",
				"scripts/probe_opera_2d.gd",
				"scripts/probe_opera_2d_balance.gd",
				"scripts/probe_opera_art.gd",
				"scripts/probe_opera_balance.gd",
				"scripts/probe_opera_detective.gd",
				"scripts/probe_opera_nursery.gd",
				"scripts/probe_save_recovery.gd",
				"scripts/probe_ui_system.gd",
				"scripts/save_state.gd",
				"tools/game_2d_migration_manifest.json",
			},
		)
		self.assertEqual(len(group.paths), 32)
		self.assertEqual(
			group.dependencies,
			(
				"CHG-005",
				"CHG-008",
				"CHG-010",
				"CHG-011",
				"CHG-015",
				"CHG-016",
				"CHG-017",
				"CHG-018",
				"CHG-019",
				"CHG-020",
				"CHG-023",
				"CHG-024",
				"CHG-025",
			),
		)
		self.assertEqual(group.safety, planner.MANUAL)
		self.assertEqual(sum(item.safety == planner.MANUAL for item in planner.CATALOG), 22)
		plan = planner.render_plan(group)
		for marker in (
			"16-slot save/raw-mask contract",
			"permanent tombstones",
			"git revert --no-commit e2c25878f6b9c64526d0686c426a9f29c5f1b3da",
			"inspect all 32 paths",
			"MA-OPERA-012 remains open",
			"GODOT=\"$GODOT\" scripts/ci.sh",
		):
			self.assertIn(marker, plan)
		with self.assertRaises(planner.UnsafePlanError):
			planner.render_script(group)

		ledger = (
			Path(__file__).resolve().parents[2]
			/ "audit"
			/ "MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md"
		).read_text(encoding="utf-8")
		for marker in (
			"all 64 trusted local probes green",
			"after 1,428.6",
			"509 models, 66 production files, and 74 probe files",
			"produced 17",
			"fresh diagnostic captures",
			"strict global visual result remains `UNSATISFIED`",
		):
			self.assertIn(marker, ledger)

		repository_root = Path(__file__).resolve().parents[2]
		master = (repository_root / "audit" / "MASTER_AUDIT_2026-08-09.md").read_text(
			encoding="utf-8"
		)
		open_work = (repository_root / "design" / "04_OPEN_WORK.md").read_text(
			encoding="utf-8"
		)
		for text in (master, open_work):
			self.assertIn("CHG-001", text)
			self.assertIn("CHG-026", text)
			self.assertIn("71 unique catalog-owned commit references", text)
			self.assertIn("e2c25878", text)
			self.assertIn("20 unit", text)
		self.assertIn("other 22 refuse automation", master)
		self.assertIn("rollback is recorded under `CHG-026`", master)

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

	def test_racer_records_do_not_overclaim_headless_canvas_parity(self) -> None:
		for change_id in ("CHG-010", "CHG-022", "CHG-024"):
			with self.subTest(change_id=change_id):
				summary = planner.select_group(change_id).summary
				self.assertIn("display/device", summary)
				self.assertIn("ordinary unforced headless", summary)
				self.assertIn("legacy", summary)
		self.assertIn("scripts/kart.gd", planner.select_group("CHG-010").summary)
		self.assertIn("without removing", planner.select_group("CHG-024").summary)

	def test_manual_group_refuses_command_emission(self) -> None:
		group = planner.select_group("CHG-009")
		with self.assertRaisesRegex(planner.UnsafePlanError, "policy-sensitive"):
			planner.render_script(group)

	def test_only_four_explicit_groups_emit_scripts(self) -> None:
		emittable = {"CHG-020", "CHG-021", "CHG-022", "CHG-024"}
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

	def test_current_dev_reconciliation_script_guards_exact_merge_and_scope(self) -> None:
		group = planner.select_group("CHG-024")
		self.assertTrue(group.all_or_nothing)
		self.assertEqual(group.rollback_start, planner.AUDIT_RECONCILIATION_COMMIT)
		self.assertEqual(group.revert_target, planner.AUDIT_RECONCILIATION_COMMIT)
		self.assertEqual(group.revert_mainline, 1)
		self.assertEqual(group.baseline_commit, planner.AUDIT_RECONCILIATION_PARENT)
		self.assertEqual(
			group.merge_parents,
			(
				planner.AUDIT_RECONCILIATION_PARENT,
				planner.AUDIT_RECONCILIATION_AUDIT_PARENT,
			),
		)
		self.assertEqual(
			set(group.paths),
			{
				".github/",
				".gitignore",
				"AGENTS.md",
				"art_library/",
				"ASSET_LICENSES.md",
				"assets/",
				"assets_src/",
				"audit/",
				"backups/",
				"CLAUDE.md",
				"CODEX_ROSHAN_SPRITE_REGENERATION_2026-08-02.md",
				"design/",
				"gen2/",
				"ROSHAN_SPRITE_CUTOFF_AUDIT_2026-08-02.md",
				"scripts/",
				"STUFFIE_COMPANIONS.md",
				"tools/",
				"VISUAL_AUDIT_TOOL.md",
			},
		)
		self.assertEqual(
			group.dependencies,
			tuple(f"CHG-{number:03d}" for number in range(1, 24)),
		)
		self.assertEqual(
			planner.AUDIT_RECONCILIATION_COMMIT,
			"f3b0de078898a8b4faddb2c738c4403180eff928",
		)
		self.assertEqual(
			planner.AUDIT_RECONCILIATION_PARENT,
			"ea6185fdb1a687a20a6d118bdc368400e2c30f60",
		)
		self.assertEqual(
			planner.AUDIT_RECONCILIATION_AUDIT_PARENT,
			"5f58ef0a9db7aa9593f85131e1b855e51b84aea8",
		)

		script = planner.render_script(group)
		self.assertIn(f"CURRENT='{planner.AUDIT_RECONCILIATION_COMMIT}'", script)
		self.assertIn("BRANCH='codex/rollback-chg-024'", script)
		self.assertIn(
			f"EXPECTED_PARENTS='{planner.AUDIT_RECONCILIATION_PARENT} {planner.AUDIT_RECONCILIATION_AUDIT_PARENT}'",
			script,
		)
		self.assertIn(
			f"git revert --no-commit -m 1 {planner.AUDIT_RECONCILIATION_COMMIT}",
			script,
		)
		self.assertIn(
			f"git diff --cached --exit-code {planner.AUDIT_RECONCILIATION_PARENT} --",
			script,
		)
		for path in planner.PROTECTED_PATHS:
			with self.subTest(protected_path=path):
				self.assertIn(path, script)
		for warning in (
			"removes the entire f3b0 reconciliation",
			"intentional archive removals",
			"Never combine CHG-024 with any CHG-001 through CHG-023",
		):
			with self.subTest(warning=warning):
				self.assertIn(warning, script)
				self.assertIn(warning, planner.render_plan(group))
		self.assertNotIn("git commit -m", script)
		self.assertNotIn("git reset", script)
		self.assertIn("git diff --cached --check", script)

	def test_whole_merge_validation_rejects_wrong_topology_mainline_start_and_tree_gate(self) -> None:
		group = planner.select_group("CHG-024")
		mutations = (
			(replace(group, merge_parents=group.merge_parents[:1]), "exactly two parents"),
			(replace(group, revert_mainline=2), "baseline/mainline mismatch"),
			(replace(group, rollback_start=planner.AUDIT_RECONCILIATION_PARENT), "start at its revert target"),
			(replace(group, gates=group.gates[1:]), "exact parent-tree gate"),
		)
		for bad_group, message in mutations:
			with self.subTest(message=message):
				with self.assertRaisesRegex(planner.CatalogError, message):
					planner.validate_catalog((bad_group,))

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
