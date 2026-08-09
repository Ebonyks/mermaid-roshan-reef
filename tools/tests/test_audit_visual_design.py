from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import audit_visual_design as ava  # noqa: E402
import audit_scene_congruency as asc  # noqa: E402


class BraceExpansionTests(unittest.TestCase):
	"""ASSET_LICENSES.md licenses families; the matcher must read that notation."""

	def test_expands_comma_group(self) -> None:
		self.assertEqual(
			sorted(ava.brace_expand("a/{x,y}.png")),
			["a/x.png", "a/y.png"],
		)

	def test_expands_numeric_range(self) -> None:
		self.assertEqual(
			sorted(ava.brace_expand("tile_{0..3}.png")),
			["tile_0.png", "tile_1.png", "tile_2.png", "tile_3.png"],
		)

	def test_expands_nested_groups(self) -> None:
		self.assertEqual(
			sorted(ava.brace_expand("{a,b}_{0..1}.png")),
			["a_0.png", "a_1.png", "b_0.png", "b_1.png"],
		)

	def test_passes_through_plain_paths(self) -> None:
		self.assertEqual(ava.brace_expand("assets/x.png"), ["assets/x.png"])


class RegistryContractTests(unittest.TestCase):
	"""The invariants that keep the tool honest as Codex extends it."""

	def test_every_check_names_a_rule_in_the_spec(self) -> None:
		rules = ava.load_spec().get("rules", {})
		for cid, chk in ava.REGISTRY.items():
			self.assertIn(chk.rule, rules,
				f"{cid} cites rule '{chk.rule}' which is not in visual_audit_spec.json")

	def test_every_check_has_a_one_line_doc(self) -> None:
		for cid, chk in ava.REGISTRY.items():
			self.assertTrue(chk.doc.strip(), f"{cid} has no docstring")

	def test_every_stressable_check_has_a_stress_case(self) -> None:
		covered = {cid for cid, _kw, _sev in ava.STRESS_CASES}
		stressable = {cid for cid, c in ava.REGISTRY.items() if c.stressable}
		self.assertEqual(stressable - covered, set(),
			"checks with no proof they can fail")

	def test_no_stale_stress_cases(self) -> None:
		for cid, _kw, _sev in ava.STRESS_CASES:
			self.assertIn(cid, ava.REGISTRY, f"stress case for removed check {cid}")

	def test_spec_zone_ids_are_unique(self) -> None:
		ids = [z["id"] for z in ava.load_spec()["zones"]]
		self.assertEqual(len(ids), len(set(ids)))

	def test_spec_uses_current_2d_lifecycle_schema(self) -> None:
		spec = ava.load_spec()
		legacy_fields = {"medium", "status", "charter_order", "supersedes",
			"reversibility_key"}
		self.assertNotIn("reversibility", spec["rules"])
		self.assertNotIn("pilot_first", spec["rules"])
		self.assertNotIn("charter.reversibility_toggle", ava.REGISTRY)
		self.assertNotIn("charter.migration_order", ava.REGISTRY)
		for zone in spec["zones"]:
			self.assertEqual(zone["art_medium"], "flattened_2d")
			self.assertEqual(zone["lifecycle"], "active_shipped")
			self.assertTrue(zone["presentation"])
			self.assertEqual(legacy_fields.intersection(zone), set(),
				f"{zone['id']} retains superseded migration fields")

	def test_declared_builder_and_probe_paths_exist(self) -> None:
		for zone in ava.load_spec()["zones"]:
			for rel in zone.get("builders", []) + zone.get("probes", []):
				self.assertTrue((ROOT / rel).is_file(), f"{zone['id']} declares missing {rel}")

	def test_sky_lagoon_evidence_names_active_runtime_2d_assets(self) -> None:
		sky_lagoon = next(
			zone for zone in ava.load_spec()["zones"]
			if zone["id"] == "sky_lagoon"
		)
		expected = {
			"assets/props/story/play_swing_frame.png",
			"assets/props/story/play_swing_seat.png",
			"assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png",
			"assets/characters/roshan_25d/roshan_base.png",
		}
		retired = {
			"assets/sprites/sky_lagoon/sky_lagoon_swing_single_mermaid_v1.png",
			"assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v3.png",
			"assets/sprites/sky_lagoon/sky_lagoon_roshan_runtime_audited.png",
		}
		manifest_paths = set(
			sky_lagoon.get("murals", [])
			+ sky_lagoon.get("standees", [])
			+ sky_lagoon.get("characters", [])
		)
		congruency_paths = {
			path
			for element in asc.ELEMENTS
			for path in (element.path, *element.runtime_paths)
		}
		congruency_paths.add(
			asc.ROSHAN_PALETTE_REFERENCE.relative_to(ROOT).as_posix()
		)
		probe_source = (ROOT / "scripts/probe_l2.gd").read_text(encoding="utf-8")

		self.assertLessEqual(expected, manifest_paths)
		self.assertTrue(retired.isdisjoint(manifest_paths))
		self.assertLessEqual(expected, congruency_paths)
		self.assertTrue(retired.isdisjoint(congruency_paths))
		for path in expected:
			self.assertIn(f"res://{path}", probe_source)
		for path in retired:
			self.assertNotIn(f"res://{path}", probe_source)

	def test_waivers_satisfy_full_contract(self) -> None:
		spec = ava.load_spec()
		self.assertEqual(ava.waiver_contract_issues(spec), [])

	def test_incomplete_waiver_is_a_contract_failure(self) -> None:
		spec = ava.load_spec()
		spec["waivers"] = [{
			"check": "texture.import_sidecar",
			"zone": "fairy_pond",
			"reason": "incomplete on purpose",
		}]
		issues = ava.waiver_contract_issues(spec)
		self.assertTrue(issues)
		repo = ava.Repo(str(ROOT), spec)
		contract = [f for f in ava.run(repo, zone_ids=["fairy_pond"])
			if f.check == "audit.waiver_contract"]
		self.assertTrue(contract)
		self.assertEqual({f.disposition for f in contract}, {ava.FAIL})

	def test_animation_frame_numbers_are_not_asset_generations(self) -> None:
		with tempfile.TemporaryDirectory() as raw:
			root = Path(raw)
			for name in (
				"roshan_slide_0.png",
				"roshan_slide_1.png",
				"roshan_slide_2_v2.png",
				"roshan_slide_3_v2.png",
			):
				path = root / "assets" / "sprites" / "fx" / name
				path.parent.mkdir(parents=True, exist_ok=True)
				path.write_bytes(b"fixture")
			zone = ava.Zone({
				"id": "fx",
				"name": "fixture",
				"art_medium": "flattened_2d",
				"presentation": "fixed_depth_cards",
				"lifecycle": "active_shipped",
				"asset_roots": ["assets/sprites/fx"],
			}, ava.Repo(str(root), {"budgets": {}, "rules": {}, "waivers": []}))
			rows = list(ava._generations(zone))
			self.assertEqual(len(rows), 1)
			self.assertEqual(rows[0].disposition, ava.PASS)


class LifecycleStateTests(unittest.TestCase):
	"""Strict means complete evidence, not merely an absence of ERROR labels."""

	def test_severity_maps_to_explicit_disposition(self) -> None:
		expected = {
			ava.ERROR: ava.FAIL,
			ava.WARN: ava.REVIEW_OPEN,
			ava.MANUAL: ava.MANUAL_OPEN,
			ava.SKIP: ava.COVERAGE_GAP,
			ava.INFO: ava.PASS,
		}
		for severity, disposition in expected.items():
			with self.subTest(severity=severity):
				finding = ava.Finding("check", "zone", severity, "fixture")
				self.assertEqual(finding.disposition, disposition)

	def test_strict_blocks_fail_review_manual_and_coverage_gap(self) -> None:
		for severity in (ava.ERROR, ava.WARN, ava.MANUAL, ava.SKIP):
			with self.subTest(severity=severity):
				finding = ava.Finding("check", "zone", severity, "fixture")
				self.assertEqual(ava.strict_blockers([finding]), [finding])
				self.assertEqual(ava.satisfaction([finding]), "UNSATISFIED")

	def test_pass_not_applicable_and_waived_do_not_block_strict(self) -> None:
		findings = [
			ava.Finding("pass", "zone", ava.INFO, "complete"),
			ava.Finding("na", "zone", ava.INFO, "out of scope",
				disposition=ava.NOT_APPLICABLE),
			ava.Finding("waived", "zone", ava.WARN, "owner accepted",
				disposition=ava.WAIVED),
		]
		self.assertEqual(ava.strict_blockers(findings), [])
		self.assertTrue(ava.strict_passes(findings))
		self.assertEqual(ava.satisfaction(findings), "SATISFIED_WITH_WAIVERS")

	def test_empty_selection_cannot_be_satisfied(self) -> None:
		self.assertFalse(ava.strict_passes([]))
		self.assertEqual(ava.satisfaction([]), "UNSATISFIED")

	def test_cli_strict_rejects_manual_and_skip_only_results(self) -> None:
		for severity in (ava.MANUAL, ava.SKIP):
			with self.subTest(severity=severity):
				row = ava.Finding("check", "zone", severity, "fixture")
				with mock.patch.object(ava, "run", return_value=[row]):
					with contextlib.redirect_stdout(io.StringIO()):
						exit_code = ava.main(["--strict", "--no-report"])
				self.assertEqual(exit_code, 1)

	def test_cp1252_console_does_not_crash_on_audit_evidence(self) -> None:
		buffer = io.BytesIO()
		stream = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
		row = ava.Finding(
			"check", "zone", ava.ERROR,
			"margin ≥ 8px → repair required",
		)
		with contextlib.redirect_stdout(stream):
			ava.configure_console()
			ava.print_console([row], verbose=True)
		stream.flush()
		output = buffer.getvalue().decode("cp1252")
		self.assertIn("VISUALAUDIT|", output)
		self.assertIn("\\u2265", output)

	def test_presentation_mismatch_is_explicit_not_applicable(self) -> None:
		spec = ava.load_spec()
		repo = ava.Repo(str(ROOT), spec)
		finding = ava.run(
			repo, zone_ids=["storybook_ui"],
			check_ids=["layering.mural_is_a_stack"],
		)
		self.assertEqual(len(finding), 1)
		self.assertEqual(finding[0].disposition, ava.NOT_APPLICABLE)

	def test_empty_runtime_target_list_is_a_coverage_gap(self) -> None:
		spec = ava.load_spec()
		runtime = {"zones": {"fairy_pond": {"targets": []}}}
		repo = ava.Repo(str(ROOT), spec, runtime)
		rows = ava.run(repo, zone_ids=["fairy_pond"],
			check_ids=["readability.tap_target_size"])
		self.assertEqual(len(rows), 1)
		self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)
		self.assertFalse(ava.strict_passes(rows))

	def test_runtime_touch_diameter_boundary_is_enforced(self) -> None:
		spec = ava.load_spec()
		for diameter, expected in ((109.9, ava.REVIEW_OPEN), (110.0, ava.PASS)):
			with self.subTest(diameter=diameter):
				runtime = {"zones": {"fairy_pond": {"targets": [{
					"id": "fixture", "screen_px": diameter,
				}]}}}
				repo = ava.Repo(str(ROOT), spec, runtime)
				rows = ava.run(repo, zone_ids=["fairy_pond"],
					check_ids=["readability.tap_target_size"])
				self.assertEqual(len(rows), 1)
				self.assertEqual(rows[0].disposition, expected)

	def test_waiver_cannot_replace_manual_or_coverage_evidence(self) -> None:
		for check_id, rule, expected in (
			("hygiene.manual_squint_test", "no_text_in_art", ava.MANUAL_OPEN),
			("readability.tap_target_size", "tap_target_size", ava.COVERAGE_GAP),
		):
			with self.subTest(check_id=check_id):
				spec = ava.load_spec()
				spec["waivers"] = [{
					"check": check_id,
					"zone": "fairy_pond",
					"rule": rule,
					"scope": "focused lifecycle fixture",
					"reason": "cannot replace evidence",
					"owner": "test owner",
					"date": "2026-08-09",
					"review_trigger": "next audit",
					"residual_risk": "required evidence remains absent",
				}]
				repo = ava.Repo(str(ROOT), spec)
				rows = ava.run(repo, zone_ids=["fairy_pond"], check_ids=[check_id])
				self.assertEqual(len(rows), 1)
				self.assertEqual(rows[0].disposition, expected)
				self.assertIn("WAIVER CANNOT REPLACE", rows[0].message)
				self.assertFalse(ava.strict_passes(rows))


class StressHarnessTests(unittest.TestCase):
	"""Run the full mutation pass: every check must fire on its own violation."""

	def test_stress_pass_is_green(self) -> None:
		self.assertEqual(ava.stress(fuzz=8), 0)


class RealRepoTests(unittest.TestCase):
	"""The tool must survive the real repository without crashing a check."""

	def test_no_check_crashes_on_the_real_repo(self) -> None:
		repo = ava.Repo(str(ROOT), ava.load_spec())
		crashed = [f for f in ava.run(repo) if "check crashed" in f.message]
		self.assertEqual(crashed, [], f"checks crashed: {crashed}")

	def test_every_zone_check_pair_has_a_disposition(self) -> None:
		"""No applicability filter or empty generator may audit a rule into silence."""
		repo = ava.Repo(str(ROOT), ava.load_spec())
		findings = ava.run(repo)
		seen = {(f.zone, f.check) for f in findings}
		for zone in ava.load_spec()["zones"]:
			for check_id in ava.REGISTRY:
				self.assertIn((zone["id"], check_id), seen,
					f"{zone['id']}/{check_id} was audited into silence")

	def test_valid_waiver_stays_visible_and_does_not_become_pass(self) -> None:
		spec = ava.load_spec()
		spec["waivers"] = [{
			"check": "layering.mural_is_a_stack",
			"zone": "sky_lagoon",
			"rule": "mural_layer_stack",
			"scope": "Sky Lagoon main promenade",
			"reason": "focused fixture",
			"owner": "test owner",
			"date": "2026-08-09",
			"review_trigger": "next art revision",
			"residual_risk": "flat camera motion remains",
		}]
		repo = ava.Repo(str(ROOT), spec)
		rows = ava.run(repo, zone_ids=["sky_lagoon"],
			check_ids=["layering.mural_is_a_stack"])
		self.assertEqual(len(rows), 1)
		self.assertEqual(rows[0].severity, ava.ERROR)
		self.assertEqual(rows[0].disposition, ava.WAIVED)
		self.assertIn("[WAIVED:", rows[0].message)
		with tempfile.TemporaryDirectory() as tmp:
			old_json, old_md = ava.REPORT_JSON, ava.REPORT_MD
			try:
				ava.REPORT_JSON = str(Path(tmp) / "r.json")
				ava.REPORT_MD = str(Path(tmp) / "r.md")
				ava.write_reports(rows, repo)
				payload = json.loads(Path(ava.REPORT_JSON).read_text(encoding="utf-8"))
				self.assertEqual(payload["satisfaction"], "SATISFIED_WITH_WAIVERS")
				self.assertEqual(payload["findings"][0]["disposition"], ava.WAIVED)
				self.assertIn("## WAIVED", Path(ava.REPORT_MD).read_text(encoding="utf-8"))
			finally:
				ava.REPORT_JSON, ava.REPORT_MD = old_json, old_md

	def test_report_writing_round_trips(self) -> None:
		repo = ava.Repo(str(ROOT), ava.load_spec())
		findings = ava.run(repo, zone_ids=["sky_lagoon"])
		with tempfile.TemporaryDirectory() as tmp:
			old_json, old_md = ava.REPORT_JSON, ava.REPORT_MD
			try:
				ava.REPORT_JSON = str(Path(tmp) / "r.json")
				ava.REPORT_MD = str(Path(tmp) / "r.md")
				ava.write_reports(findings, repo)
				self.assertTrue(Path(ava.REPORT_JSON).exists())
				self.assertTrue(Path(ava.REPORT_MD).exists())
				payload = json.loads(Path(ava.REPORT_JSON).read_text(encoding="utf-8"))
				self.assertEqual(payload["satisfaction"], "UNSATISFIED")
				self.assertIn(ava.COVERAGE_GAP, payload["dispositions"])
				self.assertIn("## COVERAGE_GAP",
					Path(ava.REPORT_MD).read_text(encoding="utf-8"))
			finally:
				ava.REPORT_JSON, ava.REPORT_MD = old_json, old_md


if __name__ == "__main__":
	unittest.main()
