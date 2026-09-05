from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import audit_document_authority as authority


def _canonical_fixture(
	*,
	lifecycle: str = "CONFIRMED_OPEN",
	anchor: str = "ma-vis-002",
	rule_ids: str = "`DL-QA-01`",
	extra_field: bool = False,
) -> tuple[str, str, str]:
	master = (
		"## 5. Triage item index\n\n"
		f"[`MA-VIS-002`](findings/ACTIVE_FINDINGS_2026-08-13.md#{anchor})\n\n"
		"| ID | Severity | Lifecycle | Verification | Indexed issue | Closure |\n"
		"|---|---|---|---|---|---|\n"
		f"| `MA-VIS-002` | P1 | `{lifecycle}` | V1 | x | y |\n\n"
		"## 6. Evidence\n"
	)
	values = {
		"id": "`MA-VIS-002`",
		"title": "A complete title.",
		"rule_ids": rule_ids,
		"domain / zone": "Visual / Lagoon",
		"source": "Static and runtime audit.",
		"severity": "P1",
		"lifecycle": f"`{lifecycle}`",
		"verification": "V1 confirmed.",
		"reproduction": "Run the exact audit.",
		"child_impact": "The route is harder to read.",
		"evidence": "Source and probe evidence.",
		"owner_decision": "No waiver exists.",
		"fix": "Repair the bounded surface.",
		"surrounding_tests": "Focused and full gates.",
		"acceptance": "All declared gates pass.",
		"closure": "Open pending acceptance.",
		"relationships": "No additional indexed relationship.",
		"history": "2026-08-13: recorded.",
	}
	if extra_field:
		values["invented"] = "not allowed"
	findings = (
		"## MA-VIS-002\n\n| Field | Value |\n|---|---|\n"
		+ "".join(f"| {key} | {value} |\n" for key, value in values.items())
	)
	design = "`DL-QA-01` — A real rule.\n"
	return master, findings, design


class DocumentAuthorityTests(unittest.TestCase):
	def test_grouped_ledger_rows_are_rejected(self) -> None:
		rows, issues = authority._ledger_rows(
			"| Doc | | Note |\n|---|---|---|\n"
			"| `a.md`, `b.md` | 🟠 | `SUPERSEDED`; historical only |\n"
		)
		self.assertEqual({}, rows)
		self.assertTrue(any(issue.check_id == "DOC002" for issue in issues))

	def test_duplicate_ledger_rows_are_rejected(self) -> None:
		rows, issues = authority._ledger_rows(
			"| Doc | | Note |\n|---|---|---|\n"
			"| `a.md` | 🟢 | `BINDING_DOMAIN`; current rule |\n"
			"| `a.md` | 🔵 | `SUPPORTING_CURRENT`; duplicate |\n"
		)
		self.assertEqual(1, len(rows))
		self.assertTrue(any(issue.check_id == "DOC003" for issue in issues))

	def test_non_mixed_state_cannot_claim_mixed_scope(self) -> None:
		_, issues = authority._ledger_rows(
			"| Doc | State | Note |\n|---|---|---|\n"
			"| `a.md` | 🟢 | Mixed authority with `PROPOSAL_DEFERRED` parts. |\n"
		)
		self.assertTrue(any(issue.check_id == "DOC011" for issue in issues))

	def test_mixed_row_requires_explicit_scope(self) -> None:
		_, issues = authority._ledger_rows(
			"| Doc | | Note |\n|---|---|---|\n"
			"| `a.md` | 🟠 | mixed current material |\n"
		)
		self.assertTrue(any(issue.check_id == "DOC006" for issue in issues))

	def test_table_parser_preserves_escaped_and_code_span_pipes(self) -> None:
		cells = authority._split_table_row(
			"| `a.md` | 🟢 | terminal `MUSIC|check` and escaped a\\|b |"
		)
		self.assertEqual(3, len(cells))
		self.assertIn("MUSIC|check", cells[2])
		self.assertIn("a\\|b", cells[2])

	def test_ledger_rejects_an_extra_unescaped_cell(self) -> None:
		rows, issues = authority._ledger_rows(
			"| Doc | State | Note |\n|---|---|---|\n"
			"| `a.md` | 🟢 | `BINDING_DOMAIN`; current | smuggled value |\n"
		)
		self.assertFalse(rows)
		self.assertTrue(any(issue.check_id == "DOC010" for issue in issues))

	def test_index_parser_accepts_linked_ids(self) -> None:
		text = (
			"| ID | Severity | Lifecycle | Verification | Indexed issue | Closure |\n"
			"|---|---|---|---|---|---|\n"
			"| [`MA-VIS-002`](findings/f.md#ma-vis-002) | P1 | `CONFIRMED_OPEN` | V1 | x | y |\n"
		)
		items, issues = authority._index_items(text)
		self.assertFalse(issues)
		self.assertEqual("CONFIRMED_OPEN", items["MA-VIS-002"].lifecycle)

	def test_index_parser_rejects_an_out_of_range_severity(self) -> None:
		text = (
			"| ID | Severity | Lifecycle | Verification | Indexed issue | Closure |\n"
			"|---|---|---|---|---|---|\n"
			"| `MA-VIS-002` | P4 | `CONFIRMED_OPEN` | V1 | x | y |\n"
		)
		items, issues = authority._index_items(text)
		self.assertNotIn("MA-VIS-002", items)
		self.assertTrue(any(issue.check_id == "DOC023" for issue in issues))

	def test_index_parser_rejects_an_unknown_lifecycle(self) -> None:
		text = (
			"| ID | Severity | Lifecycle | Verification | Indexed issue | Closure |\n"
			"|---|---|---|---|---|---|\n"
			"| `MA-VIS-002` | P1 | `NOT_A_REAL_STATE` | V1 | x | y |\n"
		)
		items, issues = authority._index_items(text)
		self.assertEqual("NOT_A_REAL_STATE", items["MA-VIS-002"].lifecycle)
		self.assertTrue(any(issue.check_id == "DOC022" for issue in issues))

	def test_index_parser_accepts_no_outer_or_tight_pipes(self) -> None:
		for row in (
			"`MA-VIS-002`| P1 | `CONFIRMED_OPEN` | V1 | x | y",
			"|`MA-VIS-002`| P1 | `CONFIRMED_OPEN` | V1 | x | y|",
			"| **`MA-VIS-002`** | P1 | `CONFIRMED_OPEN` | V1 | x | y |",
		):
			items, issues = authority._index_items(row)
			self.assertFalse(issues)
			self.assertIn("MA-VIS-002", items)

	def test_canonical_link_pattern_is_not_sensitive_to_table_position(self) -> None:
		master, findings, design = _canonical_fixture()
		self.assertFalse(authority._canonical_issues(master, findings, design))

	def test_canonical_link_must_use_the_matching_anchor(self) -> None:
		master, findings, design = _canonical_fixture(anchor="ma-vis-003")
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC052" for issue in issues))

	def test_finding_parser_requires_exact_fields(self) -> None:
		text = "## MA-VIS-002\n\n| Field | Value |\n|---|---|\n| `id` | `MA-VIS-002` |\n"
		records, issues = authority._finding_records(text)
		self.assertFalse(issues)
		self.assertEqual("`MA-VIS-002`", records["MA-VIS-002"]["id"])

	def test_canonical_heading_must_generate_the_declared_anchor(self) -> None:
		master, findings, design = _canonical_fixture()
		findings = findings.replace("## MA-VIS-002\n", "## MA-VIS-002 — title\n")
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC055" for issue in issues))

	def test_canonical_record_rejects_unexpected_fields(self) -> None:
		master, findings, design = _canonical_fixture(extra_field=True)
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC050" for issue in issues))

	def test_canonical_record_rejects_an_extra_value_cell(self) -> None:
		master, findings, design = _canonical_fixture()
		findings = findings.replace(
			"| title | A complete title. |",
			"| title | A complete title. | smuggled value |",
		)
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC054" for issue in issues))

	def test_canonical_identity_fields_require_exact_values(self) -> None:
		master, findings, design = _canonical_fixture()
		findings = findings.replace("| severity | P1 |", "| severity | P1 plus P2 |")
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC046" for issue in issues))
		master, findings, design = _canonical_fixture()
		findings = findings.replace(
			"| lifecycle | `CONFIRMED_OPEN` |",
			"| lifecycle | `CONFIRMED_OPEN` maybe |",
		)
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC047" for issue in issues))

	def test_canonical_record_requires_a_real_design_rule(self) -> None:
		master, findings, design = _canonical_fixture(rule_ids="No rule available.")
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC051" for issue in issues))
		master, findings, design = _canonical_fixture(rule_ids="`DL-NOT-DEFINED`")
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC048" for issue in issues))

	def test_canonical_record_rejects_an_undefined_audit_reference(self) -> None:
		master, findings, design = _canonical_fixture()
		findings = findings.replace(
			"No additional indexed relationship.",
			"Related to MA-FAKE-001.",
		)
		issues = authority._canonical_issues(master, findings, design)
		self.assertTrue(any(issue.check_id == "DOC053" for issue in issues))

	def test_canonical_record_rejects_an_undefined_audit_reference_in_master(self) -> None:
		master, findings, design = _canonical_fixture()
		master += "\nA current authority sentence cites MA-FAKE-001.\n"
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / authority.MASTER_PATH.parent).mkdir(parents=True)
			(root / authority.MASTER_PATH).write_text(master, encoding="utf-8")
			issues = authority._reference_issues(
				root,
				{"MA-VIS-002": authority.IndexItem("MA-VIS-002", "P1", "CONFIRMED_OPEN")},
				{"DL-QA-01"},
				{},
			)
		self.assertTrue(any(
			issue.check_id == "DOC053" and issue.path == str(authority.MASTER_PATH)
			for issue in issues
		))

	def test_selected_authority_rejects_undefined_ma_and_dl_references(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "current.md").write_text(
				"Current relationships: MA-FAKE-001 and DL-NOT-DEFINED.\n",
				encoding="utf-8",
			)
			issues = authority._reference_issues(
				root,
				{"MA-VIS-002": authority.IndexItem("MA-VIS-002", "P1", "CONFIRMED_OPEN")},
				{"DL-QA-01"},
				{"current.md": ("🔵", "`SUPPORTING_CURRENT`; current detail")},
			)
		self.assertTrue(any(issue.check_id == "DOC053" for issue in issues))
		self.assertTrue(any(issue.check_id == "DOC056" for issue in issues))

	def test_resolvable_design_rule_family_is_allowed(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "current.md").write_text("Apply DL-LAY-* rules.\n", encoding="utf-8")
			issues = authority._reference_issues(
				root,
				{},
				{"DL-LAY-01"},
				{"current.md": ("🔵", "`SUPPORTING_CURRENT`; current detail")},
			)
		self.assertFalse(issues)

	def test_audit_item_family_must_resolve(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "current.md").write_text(
				"Valid MA-OPERA-* and invalid MA-NONESUCH-* families.\n",
				encoding="utf-8",
			)
			issues = authority._reference_issues(
				root,
				{"MA-OPERA-001": authority.IndexItem("MA-OPERA-001", "P1", "CONFIRMED_OPEN")},
				set(),
				{"current.md": ("🔵", "`SUPPORTING_CURRENT`; current detail")},
			)
		self.assertEqual(1, sum(issue.check_id == "DOC057" for issue in issues))
		self.assertIn("MA-NONESUCH-*", next(
			issue.detail for issue in issues if issue.check_id == "DOC057"
		))

	def test_markdown_integrity_rejects_fence_table_and_local_link_drift(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "bad.md").write_text(
				"| A | B |\n|---|---|\n| one | only | extra |\n\n[missing](nope.md)\n\n```text\nopen\n",
				encoding="utf-8",
			)
			issues = authority._markdown_integrity_issues(root, {Path("bad.md")})
		selfEqual = {issue.check_id for issue in issues}
		self.assertTrue({"DOC070", "DOC071", "DOC072"}.issubset(selfEqual))

	def test_markdown_fence_requires_matching_character_and_sufficient_length(self) -> None:
		for opening, closing in (("````text", "```"), ("~~~~text", "~~~")):
			with tempfile.TemporaryDirectory() as directory:
				root = Path(directory)
				(root / "bad.md").write_text(
					f"{opening}\nbody\n{closing}\n",
					encoding="utf-8",
				)
				issues = authority._markdown_integrity_issues(root, {Path("bad.md")})
			self.assertTrue(any(issue.check_id == "DOC070" for issue in issues))

	def test_long_fence_can_wrap_a_short_fence_example(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "good.md").write_text(
				"````markdown\n```python\npass\n```\n````\n",
				encoding="utf-8",
			)
			issues = authority._markdown_integrity_issues(root, {Path("good.md")})
		self.assertFalse(any(issue.check_id == "DOC070" for issue in issues))

	def test_fence_close_rejects_info_text_and_four_space_indent(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "bad.md").write_text(
				"```text\nbody\n```not-a-close\n",
				encoding="utf-8",
			)
			issues = authority._markdown_integrity_issues(root, {Path("bad.md")})
		self.assertTrue(any(issue.check_id == "DOC070" for issue in issues))
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "indented.md").write_text(
				"    ```not-a-fence\nordinary indented code\n",
				encoding="utf-8",
			)
			issues = authority._markdown_integrity_issues(root, {Path("indented.md")})
		self.assertFalse(any(issue.check_id == "DOC070" for issue in issues))

	def test_terminal_record_may_remain_as_stable_history(self) -> None:
		master, findings, design = _canonical_fixture(lifecycle="VERIFIED_FIXED")
		self.assertFalse(authority._canonical_issues(master, findings, design))

	def test_forbidden_claim_is_not_excused_by_another_historical_line(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "design").mkdir()
			(root / "design/05_DOC_LEDGER.md").write_text(
				"| Doc | State | Note |\n|---|---|---|\n"
				"| `binding.md` | 🟢 | `BINDING_DOMAIN`; current authority |\n",
				encoding="utf-8",
			)
			(root / "binding.md").write_text(
				"The old approach is historical.\n"
				"The real 3D Roshan is the current product baseline.\n",
				encoding="utf-8",
			)
			issues = authority._authority_claim_issues(root)
		self.assertTrue(any(issue.check_id == "DOC060" for issue in issues))

	def test_forbidden_claim_is_scoped_when_same_line_marks_it_superseded(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "design").mkdir()
			(root / "design/05_DOC_LEDGER.md").write_text(
				"| Doc | State | Note |\n|---|---|---|\n"
				"| `binding.md` | 🟢 | `BINDING_DOMAIN`; current authority |\n",
				encoding="utf-8",
			)
			(root / "binding.md").write_text(
				"The real 3D Roshan direction is superseded historical debt.\n",
				encoding="utf-8",
			)
			issues = authority._authority_claim_issues(root)
		self.assertFalse(any(issue.check_id == "DOC060" for issue in issues))

	def test_forbidden_claim_variants_are_detected(self) -> None:
		variants = (
			"The real-3D Mermaid Roshan is current.",
			"Keep existing GLBs in the final product.",
			"Meshy work is on hold.",
			"The documentation-control working slice is still uncommitted.",
			"ff068db is the latest full-local checkpoint.",
			"V3 latest full-local, exact-head remote, and exact-head Android dev build green.",
			"There are 28 stable change groups.",
		)
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "design").mkdir()
			(root / "design/05_DOC_LEDGER.md").write_text(
				"| Doc | State | Note |\n|---|---|---|\n"
				"| `binding.md` | 🔵 | `SUPPORTING_CURRENT`; current authority |\n",
				encoding="utf-8",
			)
			(root / "binding.md").write_text("\n".join(variants), encoding="utf-8")
			issues = authority._authority_claim_issues(root)
		self.assertEqual(7, sum(issue.check_id == "DOC060" for issue in issues))

	def test_wrapped_preseal_and_latest_checkpoint_claims_are_detected(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "design").mkdir()
			(root / "design/05_DOC_LEDGER.md").write_text(
				"| Doc | State | Note |\n|---|---|---|\n"
				"| `binding.md` | 🔵 | `SUPPORTING_CURRENT`; current authority |\n",
				encoding="utf-8",
			)
			(root / "binding.md").write_text(
				"The current documentation-\n"
				"control working slice inventories 316 paths. Its CI wiring is still uncommitted.\n\n"
				"Probe head `ff068db002202839f920a6f9fb78c942788a3034` changes only\n"
				"one probe and is the latest full-local checkpoint.\n",
				encoding="utf-8",
			)
			issues = authority._authority_claim_issues(root)
		labels = [issue.detail for issue in issues if issue.check_id == "DOC060"]
		self.assertTrue(any("unsealed document-authority controls" in label for label in labels))
		self.assertTrue(any("predecessor reported as latest full-local" in label for label in labels))

	def test_stress_contract(self) -> None:
		self.assertEqual(0, authority._stress())

	def test_inventory_uses_only_git_declared_paths(self) -> None:
		result = mock.Mock(stdout=b"a.md\0docs/b.md\0", stderr=b"")
		with mock.patch.object(authority.subprocess, "run", return_value=result) as run:
			self.assertEqual({"a.md", "docs/b.md"}, authority._markdown_inventory(Path(".")))
		run.assert_called_once()

	def test_full_audit_rejects_git_declared_missing_markdown(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / "design").mkdir()
			(root / "audit/findings").mkdir(parents=True)
			(root / authority.LEDGER_PATH).write_text(
				"| Doc | State | Note |\n|---|---|---|\n"
				"| `ghost.md` | ⚪ | `HISTORICAL_EVIDENCE`; missing file |\n",
				encoding="utf-8",
			)
			(root / authority.MASTER_PATH).write_text("# Master\n", encoding="utf-8")
			(root / authority.DESIGN_LANGUAGE_PATH).write_text("# Rules\n", encoding="utf-8")
			(root / authority.FINDINGS_PATH).write_text("# Records\n", encoding="utf-8")
			with mock.patch.object(authority, "_markdown_inventory", return_value={"ghost.md"}):
				issues, _ = authority.audit(root)
		self.assertTrue(any(issue.check_id == "DOC009" for issue in issues))

	def test_full_audit_fails_closed_without_required_files(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			issues, counts = authority.audit(Path(directory))
		self.assertEqual(4, len(issues))
		self.assertEqual(0, counts["inventory"])

	def _planning_fixture(self, root: Path) -> None:
		files = {
			"tools/godot_baseline.json": '{"version": "4.7.2"}',
			str(authority.MASTER_PATH): (
				"## 4. Historical evidence\nGodot 4.7.1 passed at an old commit.\n"
				"## 9. Repair protocol\nImport with exact Godot 4.7.2-stable.\n"
				"## 12. Satisfaction gate\n- [ ] Exact Godot 4.7.2-stable passes.\n"
				"## 14. History\nGodot 4.7.1 historical checkpoint.\n"
			),
			"design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md": (
				"Global Opera follows OPERA_ACTIVE_STAR_MASK. Chapter 2 is exactly `0x2C4F`.\n"
				"Canonical sequence array: `[6, 0, 3, 10, 2, 13, 11, 1]`.\n"
			),
			"scripts/save_state.gd": "const OPERA_ACTIVE_STAR_MASK := 0x1BDEF\n",
			"scripts/chapter_two_party_plan.gd": (
				"const ALL_PARTY_MASK := 0x2C4F\n"
				"const GUIDE_ORDER: Array[int] = [6, 0, 3, 10, 2, 13, 11, 1]\n"
			),
		}
		for relative, content in files.items():
			path = root / relative
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_text(content, encoding="utf-8")

	def test_active_planning_gates_preserve_historical_engine_evidence(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			self._planning_fixture(root)
			self.assertEqual([], authority._planning_fact_issues(root))

	def test_stale_engine_in_each_active_gate_fails(self) -> None:
		for heading in ("## 9. Repair protocol", "## 12. Satisfaction gate"):
			with self.subTest(heading=heading), tempfile.TemporaryDirectory() as directory:
				root = Path(directory)
				self._planning_fixture(root)
				path = root / authority.MASTER_PATH
				path.write_text(path.read_text(encoding="utf-8").replace(
					heading, heading + "\nRequired Godot 4.7.1-stable."), encoding="utf-8")
				self.assertTrue(any(i.check_id == "DOC071" for i in authority._planning_fact_issues(root)))

	def test_stale_global_mask_fails_even_with_correct_symbol_present(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			self._planning_fixture(root)
			path = root / "design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md"
			path.write_text(path.read_text(encoding="utf-8") + "Global Opera remains `0xBDEF`.\n", encoding="utf-8")
			self.assertTrue(any(i.check_id == "DOC072" for i in authority._planning_fact_issues(root)))

	def test_changed_chapter_mask_or_order_requires_doc_update(self) -> None:
		for before, after in (("0x2C4F", "0x2C4E"), ("[6, 0, 3", "[0, 6, 3")):
			with self.subTest(change=before), tempfile.TemporaryDirectory() as directory:
				root = Path(directory)
				self._planning_fixture(root)
				path = root / "scripts/chapter_two_party_plan.gd"
				path.write_text(path.read_text(encoding="utf-8").replace(before, after), encoding="utf-8")
				self.assertTrue(any(i.check_id == "DOC073" for i in authority._planning_fact_issues(root)))

	def test_planning_fact_gate_fails_closed_on_missing_or_malformed_source(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			self._planning_fixture(root)
			baseline = root / "tools/godot_baseline.json"
			baseline.write_text('{"version": null}', encoding="utf-8")
			self.assertTrue(any(i.check_id == "DOC070" for i in authority._planning_fact_issues(root)))
			baseline.unlink()
			self.assertTrue(any(i.check_id == "DOC070" for i in authority._planning_fact_issues(root)))


if __name__ == "__main__":
	unittest.main()
