from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from PIL import Image, ImageDraw

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
		fairy = next(zone for zone in spec["zones"] if zone["id"] == "fairy_pond")
		self.assertEqual(fairy["presentation"], "legacy_3d_debt")
		self.assertEqual(fairy["target_presentation"], "overhead_canvas")

	def test_declared_builder_and_probe_paths_exist(self) -> None:
		for zone in ava.load_spec()["zones"]:
			for rel in zone.get("builders", []) + zone.get("probes", []):
				self.assertTrue((ROOT / rel).is_file(), f"{zone['id']} declares missing {rel}")

	def test_lagoon_probe_stops_before_missing_holder_dereference(self) -> None:
		probe_source = (ROOT / "scripts/probe_l2.gd").read_text(encoding="utf-8")
		contract_start = probe_source.index("var holder_contract_ok")
		guard_start = probe_source.index("if not holders_present:", contract_start)
		first_coordinate_access = probe_source.index(
			"var locked_before: Array[Vector2]", contract_start)
		self.assertLess(guard_start, first_coordinate_access)
		self.assertIn("\n\t\treturn\n", probe_source[
			guard_start:first_coordinate_access])

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

	def test_sky_lagoon_texture_peak_declares_resident_auxiliary_and_actions(self) -> None:
		sky_lagoon = next(
			zone for zone in ava.load_spec()["zones"]
			if zone["id"] == "sky_lagoon"
		)
		expected_auxiliary = {
			"assets/characters/roshan_25d/roshan_directional.png",
			"assets/characters/roshan_25d/roshan_swim_front.png",
			"assets/characters/roshan_25d/roshan_swim_back.png",
			"assets/fairy/sprites/bug_firefly.png",
			"assets/sprites/sky_lagoon/animals/otter_idle_atlas.png",
			"assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png",
			"assets/sprites/sky_lagoon/sky_lagoon_contact_shadow.png",
			"assets/sprites/sky_lagoon/sky_lagoon_smoke_wisp_v2.png",
		}
		self.assertEqual(set(sky_lagoon["runtime_auxiliary"]), expected_auxiliary)
		groups = sky_lagoon["texture_peak_alternatives"]
		self.assertEqual(len(groups), 1)
		self.assertEqual(groups[0]["id"], "roshan_playground_action")
		self.assertEqual(
			{alternative["id"] for alternative in groups[0]["alternatives"]},
			{"swing", "slide", "seesaw"},
		)
		self.assertTrue(all(
			alternative["expected_count"] == 4
			for alternative in groups[0]["alternatives"]
		))
		repo = ava.Repo(str(ROOT), ava.load_spec())
		rows = ava.run(repo, zone_ids=["sky_lagoon"],
			check_ids=["texture.zone_budget"])
		self.assertEqual(len(rows), 1)
		self.assertEqual(rows[0].disposition, ava.PASS)
		self.assertLess(float(rows[0].evidence["vram_mb"]), 24.0)
		self.assertEqual(rows[0].evidence["files"], 41)
		self.assertEqual(rows[0].evidence["peak_files"], 33)

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
		for diameter, expected in ((109.9, ava.REVIEW_OPEN), (110.0, ava.PASS)):
			with self.subTest(diameter=diameter), \
					tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				target = spec["_runtime_facts"]["zones"]["fx"]["targets"][0]
				radius = min(diameter * 0.5, 55.0)
				diagonal = round(radius / ava.math.sqrt(2.0), 1)
				offsets = [
					(0.0, 0.0), (round(radius, 1), 0.0),
					(-round(radius, 1), 0.0), (0.0, round(radius, 1)),
					(0.0, -round(radius, 1)), (diagonal, diagonal),
					(diagonal, -diagonal), (-diagonal, diagonal),
					(-diagonal, -diagonal),
				]
				target.update({
					"screen_px": diameter, "hit_diameter_px": diameter,
					"resolver_reach_radius_px": round(radius, 1),
					"resolver_reach_samples": [{
						"offset_px": [x, y], "screen_px": [640.0 + x, 360.0 + y],
						"returned_id": "standee", "inside_viewport": True,
						"matches_target": True,
					} for x, y in offsets],
					"meets_min_touch": diameter >= 110.0,
				})
				runtime = spec["_runtime_facts"]
				attestation_repo = ava.Repo(str(root), spec, runtime)
				spec["_fresh_attestation"] = ava.attest_fresh_runtime_response(
					attestation_repo, spec, runtime,
					runtime["evidence_contract"]["fresh_challenge"],
					str(root / "audit"))
				repo = ava.Repo(str(root), spec, spec["_runtime_facts"],
					spec["_fresh_attestation"])
				rows = ava.run(repo, zone_ids=["fx"],
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


class VisualEvidenceContractTests(unittest.TestCase):
	"""Layer/palette gates accept only current, measured Canvas/composite facts."""

	@staticmethod
	def _rows(root: Path, spec: dict, check_id: str) -> list[ava.Finding]:
		repo = ava.Repo(str(root), spec, spec.get("_runtime_facts"),
			spec.get("_fresh_attestation"))
		return ava.run(repo, zone_ids=["fx"], check_ids=[check_id])

	@staticmethod
	def _reseal(root: Path, spec: dict) -> None:
		"""Model facts consumed immediately inside one orchestrated fresh run."""
		runtime = spec["_runtime_facts"]
		challenge = runtime["evidence_contract"]["fresh_challenge"]
		repo = ava.Repo(str(root), spec, runtime)
		spec["_fresh_attestation"] = ava.attest_fresh_runtime_response(
			repo, spec, runtime, challenge, str(root / "audit"))

	def test_static_palette_average_is_review_risk_never_hard_failure(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(
				str(root), mural_rgb=(0, 255, 255), fg_rgb=(150, 150, 155))
			spec["_runtime_facts"]["zones"]["fx"].pop("rendered_composites")
			rows = self._rows(root, spec, "palette.background_recessive")
			self.assertEqual(len(rows), 1)
			self.assertEqual(rows[0].severity, ava.WARN)
			self.assertEqual(rows[0].disposition, ava.REVIEW_OPEN)
			self.assertFalse(rows[0].evidence["can_fail_gameplay_readability"])

	def test_saved_or_replayed_facts_have_no_pass_authority(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), mural_rgb=(0, 255, 255),
				fg_rgb=(150, 150, 155), layers_api=True, murals=2,
				canvas_layer_count=2)
			runtime = spec["_runtime_facts"]
			for attestation in (None, {
				"challenge": "d" * 64,
				"bundle_sha256": spec["_fresh_attestation"]["bundle_sha256"],
			}):
				with self.subTest(attestation=attestation):
					repo = ava.Repo(str(root), spec, runtime, attestation)
					for check_id in (
						"palette.rendered_composite_readability",
						"layering.mural_is_a_stack", "readability.tap_target_size",
					):
						row = ava.run(repo, zone_ids=["fx"], check_ids=[check_id])[0]
						self.assertEqual(row.disposition, ava.COVERAGE_GAP)
				static = ava.run(repo, zone_ids=["fx"],
					check_ids=["palette.background_recessive"])[0]
				self.assertEqual(static.disposition, ava.REVIEW_OPEN)

	def test_plausible_clean_git_forgery_without_live_challenge_stays_open(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), mural_rgb=(0, 255, 255),
				fg_rgb=(150, 150, 155), layers_api=True, murals=2,
				canvas_layer_count=2)
			state, sample = self._state_and_sample(spec)
			sample["target_instance_path"] = "/root/Fx/PlausibleTarget"
			sample["visuals"][0]["instance_path"] = \
				"/root/Fx/PlausibleTarget/StorySprite"
			# Make the pixels exactly agree with current source alpha and every
			# renewable hash, then discard the private same-process capability.
			self._rewrite_difference_shape(root, spec, "plausible_saved_forgery")
			spec["_fresh_attestation"] = None
			repo = ava.Repo(str(root), spec, spec["_runtime_facts"])
			self.assertTrue(ava.git_source_identity(repo)["dependencies_clean"])
			rendered = self._rows(
				root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(rendered.disposition, ava.COVERAGE_GAP)
			self.assertIn("no current one-use", rendered.message)
			static = self._rows(root, spec, "palette.background_recessive")[0]
			self.assertEqual(static.disposition, ava.REVIEW_OPEN)

	def test_fresh_same_process_fixture_attestation_is_positive_control(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			for check_id in (
				"palette.rendered_composite_readability",
				"layering.mural_is_a_stack", "readability.tap_target_size",
			):
				with self.subTest(check_id=check_id):
					self.assertEqual(self._rows(root, spec, check_id)[0].disposition,
						ava.PASS)

	def test_fresh_runtime_cli_orchestrates_challenge_and_consumes_response(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			fake_godot = root / "audit" / "fake_godot.exe"
			fake_godot.parent.mkdir(parents=True, exist_ok=True)
			fake_godot.write_bytes(b"trusted fixture executable")
			fake_godot.chmod(0o755)
			original_run = ava.subprocess.run

			def process(command: list[str], **kwargs: object):
				if command[-1] == "--version":
					return ava.subprocess.CompletedProcess(
						command, 0, stdout="4.7.2.stable.official.fixture\n")
				if "-s" in command and "scripts/probe_visual_audit.gd" in command:
					challenge = next(value.split("=", 1)[1] for value in command
						if value.startswith("--visual-audit-challenge="))
					facts_path = Path(next(value.split("=", 1)[1] for value in command
						if value.startswith("--visual-facts-out=")))
					runtime = json.loads(json.dumps(spec["_runtime_facts"]))
					capture_dir = facts_path.parent / "visual_runtime_captures"
					capture_dir.mkdir(parents=True, exist_ok=True)
					replacements: dict[str, str] = {}
					for old in spec["_fresh_attestation"]["capture_paths"]:
						new = capture_dir / Path(old).name
						new.write_bytes((root / old).read_bytes())
						replacements[old] = new.as_posix()

					def replace_paths(value: object) -> object:
						if isinstance(value, dict):
							return {key: replace_paths(child)
								for key, child in value.items()}
						if isinstance(value, list):
							return [replace_paths(child) for child in value]
						return replacements.get(value, value) \
							if isinstance(value, str) else value

					runtime = replace_paths(runtime)
					contract = runtime["evidence_contract"]
					contract["fresh_challenge"] = challenge
					contract["run_identity"] = ava.hashlib.sha256("|".join([
						contract["git_revision"], contract["git_tree"], challenge,
						contract["source_revision"], contract["run_nonce"],
						contract["run_started_utc"],
						contract["engine"]["version_string"],
						contract["renderer"]["actual"],
					]).encode("utf-8")).hexdigest()
					zone = runtime["zones"]["fx"]
					zone["run_identity"] = contract["run_identity"]
					for key in ("canvas_parallax", "canvas_occlusion"):
						zone[key]["run_identity"] = contract["run_identity"]
					for state in zone["rendered_composites"]:
						state["run_identity"] = contract["run_identity"]
					facts_path.write_text(json.dumps(runtime), encoding="utf-8")
					return ava.subprocess.CompletedProcess(
						command, 0, stdout="VISUALFACTS|written\n")
				return original_run(command, **kwargs)

			stdout = io.StringIO()
			with mock.patch.object(ava, "REPO", str(root)), \
					mock.patch.object(ava, "load_spec", return_value=spec), \
					mock.patch.object(ava.subprocess, "run", side_effect=process), \
					contextlib.redirect_stdout(stdout):
				exit_code = ava.main([
					"--fresh-runtime", "--godot", str(fake_godot),
					"--zone", "fx", "--check", "readability.tap_target_size",
					"--format", "json", "--strict", "--no-report",
				])
			self.assertEqual(exit_code, 0)
			rows = json.loads(stdout.getvalue())
			self.assertEqual(rows[0]["disposition"], ava.PASS)

	def test_failed_fresh_probe_never_falls_back_to_saved_pass_facts(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			fake_godot = root / "audit" / "fake_godot.exe"
			fake_godot.parent.mkdir(parents=True, exist_ok=True)
			fake_godot.write_bytes(b"trusted fixture executable")
			fake_godot.chmod(0o755)
			original_run = ava.subprocess.run

			def process(command: list[str], **kwargs: object):
				if command[-1] == "--version":
					return ava.subprocess.CompletedProcess(
						command, 0, stdout="4.7.2.stable.official.fixture\n")
				if "-s" in command and "scripts/probe_visual_audit.gd" in command:
					return ava.subprocess.CompletedProcess(
						command, 7, stdout="fixture probe failure\n")
				return original_run(command, **kwargs)

			stdout = io.StringIO()
			with mock.patch.object(ava, "REPO", str(root)), \
					mock.patch.object(ava, "load_spec", return_value=spec), \
					mock.patch.object(ava.subprocess, "run", side_effect=process), \
					contextlib.redirect_stdout(stdout), \
					contextlib.redirect_stderr(io.StringIO()):
				exit_code = ava.main([
					"--fresh-runtime", "--godot", str(fake_godot),
					"--runtime-facts", str(root / "saved_pass.json"),
					"--zone", "fx", "--check", "readability.tap_target_size",
					"--format", "json", "--strict", "--no-report",
				])
			self.assertEqual(exit_code, 1)
			rows = json.loads(stdout.getvalue())
			self.assertEqual(rows[0]["disposition"], ava.COVERAGE_GAP)

	def test_fresh_capture_snapshot_survives_consumed_temp_files(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			for path in spec["_fresh_attestation"]["capture_paths"]:
				(root / path).unlink()
			self.assertEqual(self._rows(
				root, spec, "palette.rendered_composite_readability")[0].disposition,
				ava.PASS)

	def test_fresh_attestation_rejects_output_path_substitution(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			runtime = spec["_runtime_facts"]
			state, _sample = self._state_and_sample(spec)
			state["capture_path"] = spec["zones"][0]["standees"][0]
			state["capture_sha256"] = ava.Repo(str(root), spec).sha256(
				state["capture_path"])
			with self.assertRaisesRegex(ValueError, "escaped its private output"):
				ava.attest_fresh_runtime_response(
					ava.Repo(str(root), spec, runtime), spec, runtime,
					runtime["evidence_contract"]["fresh_challenge"],
					str(root / "audit"))

	def test_complete_rendered_pass_supersedes_static_palette_risks(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(
				str(root), mural_rgb=(0, 255, 0), fg_rgb=(182, 182, 182),
				rendered_mode="same_luminance_color", layers_api=True,
				murals=2, canvas_layer_count=2)
			for check_id in (
				"palette.background_recessive", "palette.figure_ground_luminance"):
				with self.subTest(check_id=check_id):
					rows = self._rows(root, spec, check_id)
					self.assertEqual(rows[0].disposition, ava.PASS)
					self.assertEqual(
						rows[0].evidence["superseded_by"],
						"palette.rendered_composite_readability",
					)

	def test_same_luminance_colour_separation_passes_rendered_gate(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(
				str(root), rendered_mode="same_luminance_color", layers_api=True,
				murals=2, canvas_layer_count=2)
			rows = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(len(rows), 1)
			self.assertEqual(rows[0].disposition, ava.PASS)
			metrics = rows[0].evidence["passing_samples"][0]["metrics"]
			self.assertLess(metrics["luminance_delta"], 0.04)
			self.assertGreaterEqual(metrics["color_distance"], 0.10)

	def test_only_low_all_channels_is_a_hard_readability_failure(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(
				str(root), rendered_mode="low_all_channels", layers_api=True,
				murals=2, canvas_layer_count=2)
			state = spec["_runtime_facts"]["zones"]["fx"]["rendered_composites"][0]
			# Hand-authored claims cannot overrule the pixels; the tool recomputes.
			state["samples"][0].update({
				"luminance_delta": 1.0,
				"color_distance": 1.0,
				"boundary_contrast": 1.0,
			})
			self._reseal(root, spec)
			rows = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rows[0].severity, ava.ERROR)
			self.assertEqual(rows[0].disposition, ava.FAIL)
			failed = rows[0].evidence["failed_all_channels"][0]
			self.assertEqual(failed["channels"], {
				"luminance": False, "color": False, "boundary": False,
			})

	def test_fake_capture_hash_is_coverage_gap(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			state = spec["_runtime_facts"]["zones"]["fx"]["rendered_composites"][0]
			state["capture_sha256"] = "f" * 64
			rows = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)
			self.assertIn("does not match its bytes", rows[0].message)

	def test_missing_stale_or_misaligned_target_mask_is_coverage_gap(self) -> None:
		mutations = {
			"fake_mask_hash": lambda sample: sample.update({"mask_sha256": "f" * 64}),
			"misaligned_mask": lambda sample: sample.update({"figure_rect": [0, 0, 32, 32]}),
			"unbound_mask": lambda sample: sample.update({"mask_source": "hand_drawn"}),
		}
		for name, mutate in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				sample = spec["_runtime_facts"]["zones"]["fx"] \
					["rendered_composites"][0]["samples"][0]
				mutate(sample)
				rows = self._rows(root, spec, "palette.rendered_composite_readability")
				self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)

	def test_irregular_alpha_mask_defeats_bounding_box_false_pass(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(
				str(root), rendered_mode="irregular_bbox_lie", layers_api=True,
				murals=2, canvas_layer_count=2)
			rows = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rows[0].disposition, ava.FAIL)
			metrics = rows[0].evidence["failed_all_channels"][0]["metrics"]
			self.assertLess(metrics["luminance_delta"], 0.04)
			self.assertLess(metrics["color_distance"], 0.10)
			self.assertLess(metrics["boundary_contrast"], 0.08)

	def test_stale_builder_or_art_invalidates_rendered_evidence(self) -> None:
		for changed in ("scripts/fx_stage.gd", "assets/sprites/fx/standee_thing.png"):
			with self.subTest(changed=changed), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				path = root / changed
				path.write_bytes(path.read_bytes() + b"stale-evidence-mutation")
				rows = self._rows(root, spec, "palette.rendered_composite_readability")
				self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)
				self.assertIn("is stale", rows[0].message)

	def test_missing_composite_evidence_is_coverage_gap(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			spec["_runtime_facts"]["zones"]["fx"].pop("rendered_composites")
			rows = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)

	def test_canvas_layer_contract_positive_control(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			rows = self._rows(root, spec, "layering.mural_is_a_stack")
			self.assertEqual(len(rows), 1)
			self.assertEqual(rows[0].disposition, ava.PASS)

	def test_canvas_layer_contract_rejects_duplicate_and_uninstantiated_layers(self) -> None:
		mutations = {
			"duplicate_declared_pixels": lambda spec: spec["zones"][0]["canvas_layers"][1].update(
				{"assets": spec["zones"][0]["canvas_layers"][0]["assets"]}),
			"uninstantiated_l1": lambda spec: spec["_runtime_facts"]["zones"]["fx"]
				["canvas_parallax"]["layers"].pop(),
			"duplicate_runtime_signature": lambda spec: spec["_runtime_facts"]["zones"]
				["fx"]["canvas_parallax"]["layers"][1].update(
					{"content_signature": spec["_runtime_facts"]["zones"]["fx"]
						["canvas_parallax"]["layers"][0]["content_signature"]}),
			"thin_coverage": lambda spec: spec["_runtime_facts"]["zones"]["fx"]
				["canvas_parallax"]["layers"][1].update({"screen_coverage_ratio": 0.10}),
			"unmeasured_coverage": lambda spec: spec["_runtime_facts"]["zones"]["fx"]
				["canvas_parallax"]["layers"][1].update({"coverage_method": "bbox"}),
			"no_differential_motion": lambda spec: spec["_runtime_facts"]["zones"]
				["fx"]["canvas_parallax"]["layers"][1].update({"screen_delta_px": 0.0}),
			"legacy_spatial_backend": lambda spec: spec["_runtime_facts"]["zones"]["fx"]
				["canvas_parallax"].update({"backend": "legacy_spatial"}),
		}
		for name, mutate in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				mutate(spec)
				self._reseal(root, spec)
				rows = self._rows(root, spec, "layering.mural_is_a_stack")
				self.assertEqual(rows[0].disposition, ava.FAIL)

	def test_canvas_layer_contract_rejects_renamed_byte_duplicate(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			first = root / spec["zones"][0]["canvas_layers"][0]["assets"][0]
			second = root / spec["zones"][0]["canvas_layers"][1]["assets"][0]
			second.write_bytes(first.read_bytes())
			rows = self._rows(root, spec, "layering.mural_is_a_stack")
			self.assertEqual(rows[0].disposition, ava.FAIL)
			self.assertIn("identical decoded visible pixels", rows[0].message)

	def test_canvas_content_identity_ignores_png_encoding_and_hidden_rgb(self) -> None:
		for case in ("compression", "hidden_rgb"):
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				first = root / spec["zones"][0]["canvas_layers"][0]["assets"][0]
				second = root / spec["zones"][0]["canvas_layers"][1]["assets"][0]
				if case == "compression":
					with Image.open(first) as source:
						source.convert("RGBA").save(second, compress_level=0)
				else:
					for path, hidden in ((first, (255, 0, 0, 0)),
							(second, (0, 255, 0, 0))):
						image = Image.new("RGBA", (512, 512), hidden)
						ImageDraw.Draw(image).rectangle(
							(80, 80, 431, 431), fill=(25, 90, 180, 255))
						image.save(path)
				repo = ava.Repo(str(root), spec)
				self.assertNotEqual(repo.sha256(first.as_posix()),
					repo.sha256(second.as_posix()))
				self.assertEqual(
					ava.canonical_visible_pixel_signature(
						repo, first.relative_to(root).as_posix()),
					ava.canonical_visible_pixel_signature(
						repo, second.relative_to(root).as_posix()),
				)
				row = self._rows(root, spec, "layering.mural_is_a_stack")[0]
				self.assertEqual(row.disposition, ava.FAIL)

	def test_transparent_asset_cannot_distinguish_equal_canvas_layers(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			declared = spec["zones"][0]["canvas_layers"]
			runtime = spec["_runtime_facts"]["zones"]["fx"]["canvas_parallax"]["layers"]
			first = root / declared[0]["assets"][0]
			second = root / declared[1]["assets"][0]
			with Image.open(first) as source:
				source.convert("RGBA").save(second, compress_level=0)
			transparent_rel = "assets/flats/fx/stage/inert_transparent.png"
			Image.new("RGBA", (512, 512), (17, 93, 201, 0)).save(
				root / transparent_rel)
			declared[1]["assets"].append(transparent_rel)
			runtime[1]["assets"].append(transparent_rel)
			repo = ava.Repo(str(root), spec)
			for index in range(2):
				signature = ava.asset_content_signature(repo, declared[index]["assets"])
				runtime[index]["content_signature"] = signature
				runtime[index]["painted_composite_signature"] = signature
			self.assertEqual(runtime[0]["content_signature"], runtime[1]["content_signature"])
			row = self._rows(root, spec, "layering.mural_is_a_stack")[0]
			self.assertEqual(row.disposition, ava.FAIL)

	def test_equal_runtime_painted_composites_cannot_pass(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			layers = spec["_runtime_facts"]["zones"]["fx"] \
				["canvas_parallax"]["layers"]
			layers[1]["painted_composite_signature"] = \
				layers[0]["painted_composite_signature"]
			self._reseal(root, spec)
			row = self._rows(root, spec, "layering.mural_is_a_stack")[0]
			self.assertEqual(row.disposition, ava.FAIL)
			self.assertIn("same canonical viewport composite", row.message)

	def test_filenames_and_layers_key_cannot_game_canvas_gate(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), murals=2,
				mural_layer_names=("L0", "L1"), canvas_layer_count=0)
			mural = self._rows(root, spec, "layering.mural_is_a_stack")
			engine = self._rows(root, spec, "layering.engine_layer_api")
			self.assertEqual(mural[0].disposition, ava.COVERAGE_GAP)
			self.assertEqual(engine[0].disposition, ava.FAIL)
			self.assertIn("spatial stage/resource/API debt", engine[0].message)

	@staticmethod
	def _state_and_sample(spec: dict) -> tuple[dict, dict]:
		state = spec["_runtime_facts"]["zones"]["fx"]["rendered_composites"][0]
		return state, state["samples"][0]

	@staticmethod
	def _rewrite_difference_shape(root: Path, spec: dict, case: str) -> None:
		state, sample = VisualEvidenceContractTests._state_and_sample(spec)
		hidden_path = root / sample["target_hidden_capture_path"]
		capture_path = root / state["capture_path"]
		restored_path = root / sample["target_restored_capture_path"]
		mask_path = root / sample["mask_path"]
		hidden = Image.open(hidden_path).convert("RGB")
		repo = ava.Repo(str(root), spec, spec.get("_runtime_facts"))
		zone = ava.Zone(spec["zones"][0], repo)
		projected, _evidence = ava._source_alpha_projection(
			zone, sample["visuals"][0], 1280, 720)
		mask = Image.fromarray((projected.astype("uint8") * 255), mode="L")
		visible = hidden.copy()
		visible.paste(Image.new("RGB", hidden.size, (240, 220, 245)), mask=mask)
		visible.save(capture_path)
		visible.save(restored_path)
		for binding in sample["target_visible_stability_captures"]:
			visible.save(root / binding["path"])
		mask.save(mask_path)
		bbox = mask.getbbox()
		assert bbox is not None
		sample["figure_rect"] = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
		repo = ava.Repo(str(root), spec)
		state["capture_sha256"] = repo.sha256(state["capture_path"])
		sample["target_restored_capture_sha256"] = repo.sha256(
			sample["target_restored_capture_path"])
		sample["mask_sha256"] = repo.sha256(sample["mask_path"])
		for binding in sample["target_visible_stability_captures"]:
			binding["sha256"] = repo.sha256(binding["path"])
		VisualEvidenceContractTests._reseal(root, spec)

	def test_forged_self_consistent_rectangle_or_unrelated_patch_cannot_pass(self) -> None:
		for case, box in {
			"small_rectangle": (610, 345, 626, 361),
			"unrelated_corner_patch": (80, 80, 104, 104),
		}.items():
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(
					str(root), mural_rgb=(0, 255, 255), fg_rgb=(150, 150, 155),
					layers_api=True, murals=2, canvas_layer_count=2)
				_state, sample = self._state_and_sample(spec)
				mask_path = root / sample["mask_path"]
				forged = Image.new("L", (1280, 720), 0)
				ImageDraw.Draw(forged).rectangle(box, fill=255)
				forged.save(mask_path)
				sample["mask_sha256"] = ava.Repo(str(root), spec).sha256(sample["mask_path"])
				sample["figure_rect"] = [box[0], box[1], box[2] - box[0] + 1,
					box[3] - box[1] + 1]
				self._reseal(root, spec)
				rendered = self._rows(root, spec, "palette.rendered_composite_readability")
				self.assertEqual(rendered[0].disposition, ava.COVERAGE_GAP)
				self.assertIn("target mask differs", rendered[0].message)
				static = self._rows(root, spec, "palette.background_recessive")
				self.assertEqual(static[0].disposition, ava.REVIEW_OPEN)

	def test_runtime_contract_rejects_wrong_engine_renderer_or_stale_harness(self) -> None:
		def mutate_file(spec: dict, root: Path, role: str) -> None:
			path = root / spec["_runtime_facts"]["evidence_contract"]["files"][role]["path"]
			path.write_bytes(path.read_bytes() + b"\nstale runtime evidence\n")

		mutations = {
			"godot_4_4": lambda spec, _root: spec["_runtime_facts"]["evidence_contract"]
				["engine"].update({"minor": 4, "patch": 0,
					"version_string": "4.4.stable.official"}),
			"gl_compatibility": lambda spec, _root: spec["_runtime_facts"]
				["evidence_contract"]["renderer"].update({"actual": "gl_compatibility"}),
			"fake_probe_hash": lambda spec, _root: spec["_runtime_facts"]
				["evidence_contract"]["files"]["probe"].update({"sha256": "f" * 64}),
			"changed_probe": lambda spec, root: mutate_file(spec, root, "probe"),
			"changed_spec": lambda spec, root: mutate_file(spec, root, "spec"),
			"changed_scene": lambda spec, root: mutate_file(spec, root, "scene"),
			"changed_project": lambda spec, root: mutate_file(spec, root, "project"),
			"changed_main": lambda spec, root: mutate_file(spec, root, "main_script"),
			"changed_player": lambda spec, root: mutate_file(spec, root, "player_script"),
			"changed_builder_shader": lambda _spec, root: (
				root / "assets" / "shaders" / "fixture.gdshader").write_text(
					"shader_type canvas_item;\n// changed after capture\n", encoding="utf-8"),
			"changed_transitive_script": lambda _spec, root: (
				root / "scripts" / "new_runtime_dependency.gd").write_text(
					"extends Node2D\n", encoding="utf-8"),
		}
		for name, mutate in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				mutate(spec, root)
				for check_id in (
					"palette.rendered_composite_readability", "layering.mural_is_a_stack"):
					rows = self._rows(root, spec, check_id)
					self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)

	def test_stale_builder_and_source_token_only_cannot_pass_engine_gate(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			builder = root / "scripts/fx_stage.gd"
			builder.write_text(builder.read_text(encoding="utf-8")
				+ "\nfunc never_called_token() -> void:\n\tvar unused := Node2D.new()\n",
				encoding="utf-8")
			rows = self._rows(root, spec, "layering.engine_layer_api")
			self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)
			self.assertIn("current bound runtime evidence is missing", rows[0].message)
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			spec["_runtime_facts"]["zones"]["fx"].pop("canvas_parallax")
			rows = self._rows(root, spec, "layering.engine_layer_api")
			self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)

	def test_equal_canvas_draw_order_is_a_hard_failure(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			layer = spec["_runtime_facts"]["zones"]["fx"]["canvas_parallax"]["layers"][1]
			layer.update({"draw_order": 0, "z_index": 0})
			self._reseal(root, spec)
			rows = self._rows(root, spec, "layering.mural_is_a_stack")
			self.assertEqual(rows[0].disposition, ava.FAIL)
			self.assertIn("equal z_index", rows[0].message)

	def test_exact_hidden_difference_handles_all_projection_families(self) -> None:
		cases = (
			"sprite_region_hframes_flip", "sprite_rotation_nonuniform_scale",
			"texture_keep_aspect", "texture_cover_crop",
		)
		for case in cases:
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				_state, sample = self._state_and_sample(spec)
				visual = sample["visuals"][0]
				if case.startswith("sprite"):
					if case == "sprite_region_hframes_flip":
						visual["projection"].update({
							"region_enabled": True,
							"region_rect": [32, 16, 128, 96],
							"hframes": 4, "vframes": 2,
							"frame_coords": [2, 1],
							"flip_h": True, "flip_v": True,
						})
						visual["local_rect"] = [-16.0, -24.0, 32.0, 48.0]
						visual["canvas_transform"] = [3.0, 0.0, 0.0, 2.0, 640, 360]
					else:
						visual["canvas_transform"] = [0.3, 0.2, -0.1, 0.25, 640, 360]
				else:
					visual.update({"node_type": "TextureRect"})
					visual["local_rect"] = [0.0, 0.0, 160.0, 100.0]
					visual["canvas_transform"] = [1.0, 0.0, 0.0, 1.0, 560.0, 310.0]
					visual["projection"] = {
						"kind": "TextureRect",
						"stretch_mode": 4 if case == "texture_keep_aspect" else 6,
						"expand_mode": 0, "flip_h": False, "flip_v": False,
						"control_size": [160, 100], "clip_contents": True,
					}
				self._rewrite_difference_shape(root, spec, case)
				rows = self._rows(root, spec, "palette.rendered_composite_readability")
				self.assertEqual(rows[0].disposition, ava.PASS)

	def test_hidden_visual_and_non_base_viewport_are_coverage_gaps(self) -> None:
		mutations = {
			"hidden_child": lambda state, sample: sample["visuals"][0].update(
				{"visible_in_tree": False}),
			"wrong_viewport": lambda state, _sample: state.update({"viewport": [320, 180]}),
		}
		for name, mutate in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				state, sample = self._state_and_sample(spec)
				mutate(state, sample)
				rows = self._rows(root, spec, "palette.rendered_composite_readability")
				self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)

	def test_visible_restore_drift_invalidates_target_difference(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			_state, sample = self._state_and_sample(spec)
			path = root / sample["target_restored_capture_path"]
			image = Image.open(path).convert("RGB")
			image.putpixel((12, 12), (255, 0, 255))
			image.save(path)
			sample["target_restored_capture_sha256"] = ava.Repo(
				str(root), spec).sha256(sample["target_restored_capture_path"])
			self._reseal(root, spec)
			rows = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rows[0].disposition, ava.COVERAGE_GAP)
			self.assertIn("visible frames are temporally unstable", rows[0].message)

	def test_3d_render_cannot_suppress_static_palette_risk(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(
				str(root), mural_rgb=(0, 255, 255), fg_rgb=(150, 150, 155),
				layers_api=True, murals=2, canvas_layer_count=2)
			canvas = spec["_runtime_facts"]["zones"]["fx"]["canvas_parallax"]
			canvas.update({"backend": "legacy_spatial", "non_canvas_spatial_nodes": 1})
			self._reseal(root, spec)
			rendered = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rendered[0].disposition, ava.PASS)
			static = self._rows(root, spec, "palette.background_recessive")
			self.assertEqual(static[0].disposition, ava.REVIEW_OPEN)

	def test_active_legacy_debt_and_unimplemented_fairy_states_stay_open(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), presentation="legacy_3d_debt",
				layers_api=True, murals=2, canvas_layer_count=2)
			legacy = self._rows(root, spec, "layering.legacy_3d_debt")
			self.assertEqual(legacy[0].disposition, ava.FAIL)
			spec["zones"][0]["rendered_readability_states"] = [
				{"id": "fairy_intro", "capture_adapter": "not_implemented",
					"coverage_gap_reason": "intro adapter absent"},
				{"id": "fairy_boss", "capture_adapter": "not_implemented",
					"coverage_gap_reason": "boss adapter absent"},
			]
			rendered = self._rows(root, spec, "palette.rendered_composite_readability")
			self.assertEqual(rendered[0].disposition, ava.COVERAGE_GAP)
			self.assertIn("fairy_intro", rendered[0].message)
			self.assertIn("fairy_boss", rendered[0].message)

	def test_game_wide_active_3d_builder_debt_fails_every_presentation(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), presentation="free_swim", layers_api=False)
			rows = self._rows(root, spec, "layering.legacy_3d_debt")
			self.assertEqual(rows[0].disposition, ava.FAIL)
			self.assertIn("Sprite3D", rows[0].evidence["source"]["forbidden_types"])
		repo = ava.Repo(str(ROOT), ava.load_spec())
		rows = ava.run(repo, check_ids=["layering.legacy_3d_debt"])
		by_zone = {row.zone: row for row in rows}
		for zone_id in (
			"reef", "castle", "courtyard", "northern", "ember", "opera", "galaxy",
		):
			with self.subTest(zone_id=zone_id):
				self.assertEqual(by_zone[zone_id].disposition, ava.FAIL)

	def test_game_wide_3d_gate_rejects_all_common_class_and_resource_families(self) -> None:
		cases = {
			"mesh": "var n := MeshInstance3D.new()",
			"area": "var n := Area3D.new()",
			"body": "var n := RigidBody3D.new()",
			"particles": "var n := GPUParticles3D.new()",
			"light": "var n := DirectionalLight3D.new()",
			"environment": "var n := WorldEnvironment.new()",
			"dynamic": 'var n := ClassDB.instantiate("Area3D")',
			"resource": 'var n := load("res://deprecated_resources/old.glb")',
			"fog_volume": "var n := FogVolume.new()",
			"decal": "var n := Decal.new()",
			"voxel_gi": "var n := VoxelGI.new()",
			"lightmap_gi": "var n := LightmapGI.new()",
			"reflection_probe": "var n := ReflectionProbe.new()",
		}
		for name, statement in cases.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim",
					layers_api=True)
				(root / "scripts" / "fx_stage.gd").write_text(
					"extends RefCounted\nfunc build(parent: Node) -> void:\n\t"
					+ statement + "\n\tparent.add_child(n)\n", encoding="utf-8")
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, ava.FAIL)
				evidence = row.evidence["source"]
				self.assertTrue(evidence["forbidden_types"]
					or evidence["forbidden_resources"])

	def test_unknown_active_builder_is_gap_and_comments_do_not_create_3d_debt(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), presentation="free_swim", layers_api=True)
			builder = root / "scripts" / "fx_stage.gd"
			builder.write_text(
				"extends RefCounted\nfunc build() -> void:\n\tpass\n",
				encoding="utf-8")
			unknown = self._rows(root, spec, "layering.legacy_3d_debt")[0]
			self.assertEqual(unknown.disposition, ava.COVERAGE_GAP)
			builder.write_text(
				"extends RefCounted\nfunc build() -> void:\n"
				"\tconst DISABLE_3D := false\n"
				"\tconst MODE_3D := 3\n"
				"\tconst STORY3D := false\n"
				"\tconst NOT_A_CLASS3D := false\n"
				"\tvar root := Node2D.new()\n"
				"\tprint(\"MeshInstance3D was removed\") # Area3D.new()\n",
				encoding="utf-8")
			comment_only = self._rows(root, spec, "layering.legacy_3d_debt")[0]
			self.assertEqual(comment_only.disposition, ava.PASS)

	def test_game_wide_3d_gate_follows_helpers_scenes_and_main_indirection(self) -> None:
		cases = ("helper", "scene", "main")
		for case in cases:
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim",
					layers_api=True)
				builder = root / "scripts" / "fx_stage.gd"
				if case == "helper":
					(root / "scripts" / "spatial_factory.gd").write_text(
						"extends RefCounted\nstatic func spawn(parent: Node) -> void:\n"
						"\tparent.add_child(Node3D.new())\n", encoding="utf-8")
					builder.write_text(
						"extends RefCounted\nconst Factory = preload("
						"\"res://scripts/spatial_factory.gd\")\n"
						"func build(parent: Node) -> void:\n"
						"\tparent.add_child(Node2D.new())\n\tFactory.spawn(parent)\n",
						encoding="utf-8")
				elif case == "scene":
					(root / "scenes" / "spatial_stage.tscn").write_text(
						"[gd_scene format=3]\n[node name=\"Spatial\" type=\"Node3D\"]\n"
						"[node name=\"Mesh\" type=\"MeshInstance3D\" parent=\".\"]\n",
						encoding="utf-8")
					builder.write_text(
						"extends RefCounted\nconst Stage = preload("
						"\"res://scenes/spatial_stage.tscn\")\n"
						"func build(parent: Node) -> void:\n"
						"\tparent.add_child(Node2D.new())\n"
						"\tparent.add_child(Stage.instantiate())\n", encoding="utf-8")
				else:
					(root / "scripts" / "main.gd").write_text(
						"extends Node2D\nfunc spawn_stage(parent: Node) -> void:\n"
						"\tparent.add_child(Node3D.new())\n", encoding="utf-8")
					builder.write_text(
						"extends RefCounted\nfunc build(m: Node) -> void:\n"
						"\tvar root := Node2D.new()\n\tm.spawn_stage(root)\n",
						encoding="utf-8")
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, ava.FAIL)

	def test_game_wide_3d_gate_closes_class_value_global_class_and_resource_types(self) -> None:
		for case in ("class_value", "global_class", "lower_global_class",
				"underscore_global_class", "resource_type", "shader"):
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim",
					layers_api=True)
				builder = root / "scripts" / "fx_stage.gd"
				if case == "class_value":
					builder.write_text(
						"extends RefCounted\nfunc build(parent: Node) -> void:\n"
						"\tvar constructors := [Node2D, MeshInstance3D]\n"
						"\tvar spatial = constructors[1].new()\n"
						"\tparent.add_child(spatial)\n", encoding="utf-8")
				elif case in {"global_class", "lower_global_class",
						"underscore_global_class"}:
					class_name = {"global_class": "SpatialFactory",
						"lower_global_class": "spatial_factory",
						"underscore_global_class": "_SpatialFactory"}[case]
					(root / "scripts" / "spatial_factory.gd").write_text(
						f"class_name {class_name}\nextends RefCounted\n"
						"static func spawn(parent: Node) -> void:\n"
						"\tparent.add_child(MeshInstance3D.new())\n", encoding="utf-8")
					builder.write_text(
						"extends RefCounted\nfunc build(parent: Node) -> void:\n"
						"\tparent.add_child(Node2D.new())\n"
						f"\t{class_name}.spawn(parent)\n", encoding="utf-8")
				elif case == "resource_type":
					resource = root / "deprecated_resources" / "legacy_environment.tres"
					resource.parent.mkdir(parents=True)
					resource.write_text(
						'[gd_resource type="Environment" format=3]\n', encoding="utf-8")
					builder.write_text(
						"extends RefCounted\nfunc build(parent: Node) -> void:\n"
						"\tvar environment := preload("
						"\"res://deprecated_resources/legacy_environment.tres\")\n"
						"\tparent.add_child(Node2D.new())\n", encoding="utf-8")
				else:
					shader = root / "assets" / "shaders" / "spatial_fixture.gdshader"
					shader.write_text("shader_type spatial;\n", encoding="utf-8")
					builder.write_text(
						"extends RefCounted\nfunc build(parent: Node) -> void:\n"
						"\tvar shader := load("
						"\"res://assets/shaders/spatial_fixture.gdshader\")\n"
						"\tparent.add_child(Node2D.new())\n", encoding="utf-8")
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, ava.FAIL)

	def test_game_wide_3d_gate_covers_loader_autoload_uid_and_dynamic_edges(self) -> None:
		for case, expected in (
				("threaded_model", ava.FAIL), ("autoload", ava.FAIL),
				("scene_change", ava.FAIL), ("split_classdb", ava.FAIL),
				("uid", ava.COVERAGE_GAP), ("opaque_scene", ava.COVERAGE_GAP),
				("opaque_resource", ava.COVERAGE_GAP),
				("resource_pack", ava.COVERAGE_GAP),
				("zip_pack", ava.COVERAGE_GAP),
				("callable_pack", ava.COVERAGE_GAP),
				("bound_pack", ava.COVERAGE_GAP),
				("callable_resource", ava.COVERAGE_GAP),
				("threaded_get", ava.COVERAGE_GAP),
				("interactive_load", ava.COVERAGE_GAP),
				("resource_call", ava.COVERAGE_GAP),
				("resource_callv", ava.COVERAGE_GAP),
				("project_call", ava.COVERAGE_GAP),
				("dynamic_script", ava.COVERAGE_GAP),
				("scene_tree_call", ava.COVERAGE_GAP),
				("scene_tree_callable", ava.COVERAGE_GAP),
				("native_extension", ava.COVERAGE_GAP),
				("dynamic_library", ava.COVERAGE_GAP),
				("compiled_gdscript", ava.COVERAGE_GAP),
				("external_scene", ava.COVERAGE_GAP)):
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim",
					layers_api=True)
				builder = root / "scripts" / "fx_stage.gd"
				if case == "threaded_model":
					body = ('ResourceLoader.load_threaded_request('
						'"res://deprecated_resources/old.glb")')
				elif case == "uid":
					body = 'load("uid://dummylegacy3d")'
				elif case == "opaque_scene":
					body = 'load("res://deprecated-resources/legacy.scn").instantiate()'
				elif case == "opaque_resource":
					body = 'load("res://deprecated-resources/legacy.res")'
				elif case == "resource_pack":
					body = ('ProjectSettings.load_resource_pack('
						'"res://deprecated-resources/legacy.pck")')
				elif case == "zip_pack":
					body = ('ProjectSettings.load_resource_pack('
						'"res://deprecated-resources/legacy.zip")')
				elif case == "callable_pack":
					body = ('var fn := Callable(ProjectSettings, "load_resource_pack")\n'
						'\tfn.call("res://deprecated-resources/legacy.pck")')
				elif case == "bound_pack":
					body = ('var fn := ProjectSettings.load_resource_pack.bind('
						'"res://deprecated-resources/legacy.zip")\n\tfn.call()')
				elif case == "callable_resource":
					body = ('var fn := Callable(ResourceLoader, "load")\n'
						'\tfn.call("res://scripts/spatial_helper.gd")')
				elif case == "threaded_get":
					body = ('ResourceLoader.load_threaded_get('
						'"res://assets/opaque.scn")')
				elif case == "interactive_load":
					body = ('ResourceLoader.load_interactive('
						'"res://assets/opaque.scn")')
				elif case == "resource_call":
					body = ('ResourceLoader.call("load", '
						'"res://assets/opaque.scn")')
				elif case == "resource_callv":
					body = ('ResourceLoader.callv("load", '
						'["res://assets/opaque.scn"])')
				elif case == "project_call":
					body = ('ProjectSettings.call("load_resource_pack", '
						'"res://assets/opaque.pck")')
				elif case == "dynamic_script":
					body = ('var script := GDScript.new()\n'
						'\tscript.source_code = "extends Node" + str(3) + "D"\n'
						'\tscript.reload()\n\tvar value = script.new()')
				elif case == "scene_tree_call":
					body = ('parent.get_tree().call("change_scene_to_file", '
						'"res://assets/opaque.scn")')
				elif case == "scene_tree_callable":
					body = ('var fn := Callable(parent.get_tree(), '
						'"change_scene_to_file")\n'
						'\tfn.call("res://assets/opaque.scn")')
				elif case == "native_extension":
					body = ('GDExtensionManager.load_extension('
						'"res://assets/evil.gdextension")')
				elif case == "dynamic_library":
					body = ('OS.open_dynamic_library('
						'"res://assets/evil.dll")')
				elif case == "compiled_gdscript":
					body = 'load("res://scripts/evil.gdc")'
				elif case == "external_scene":
					body = 'load("user://legacy.scn")'
				elif case == "split_classdb":
					body = ('var spatial := ClassDB.instantiate('
						'"MeshInstance" + "3D")\n\tparent.add_child(spatial)')
				elif case == "autoload":
					(root / "scripts" / "spatial_autoload.gd").write_text(
						"extends Node\nfunc _ready() -> void:\n"
						"\tadd_child(MeshInstance3D.new())\n", encoding="utf-8")
					with (root / "project.godot").open("a", encoding="utf-8") as handle:
						handle.write('[autoload]\nSpatialAutoload="*res://scripts/spatial_autoload.gd"\n')
					body = "parent.add_child(Node2D.new())"
				else:
					(root / "scenes" / "legacy_world.tscn").write_text(
						'[gd_scene format=3]\n[node name="Legacy" type="Node3D"]\n',
						encoding="utf-8")
					body = ('get_tree().change_scene_to_file('
						'"res://scenes/legacy_world.tscn")')
				builder.write_text(
					"extends RefCounted\nfunc build(parent: Node) -> void:\n\t" + body
					+ "\n", encoding="utf-8")
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, expected)

	def test_low_level_rendering_server_spatial_rids_cannot_pass(self) -> None:
		for case, body, expected in (
			("spatial", "var scenario := RenderingServer.scenario_create()\n"
				"\tvar instance := RenderingServer.instance_create()\n"
				"\tvar mesh := RenderingServer.mesh_create()\n"
				"\tRenderingServer.instance_set_scenario(instance, scenario)\n"
				"\tRenderingServer.instance_set_base(instance, mesh)", ava.FAIL),
			("canvas", "var canvas := RenderingServer.canvas_create()\n"
				"\tvar item := RenderingServer.canvas_item_create()\n"
				"\tRenderingServer.canvas_item_set_parent(item, canvas)", ava.PASS),
			("alias_spatial", "var server = RenderingServer\n"
				"\tvar scenario := server.scenario_create()", ava.FAIL),
			("singleton_spatial", "var server = Engine.get_singleton("
				"\"Rendering\" + \"Server\")\n"
				"\tvar mesh := server.mesh_create()", ava.FAIL),
			("callable_spatial", "var fn := Callable(RenderingServer, "
				"\"scenario_\" + \"create\")\n\tvar scenario = fn.call()", ava.FAIL),
			("dispatch_spatial", "var mesh := RenderingServer.call("
				"\"mesh_\" + \"create\")", ava.FAIL),
			("alias_canvas", "var server = RenderingServer\n"
				"\tvar canvas := server.canvas_create()", ava.PASS),
			("callable_canvas", "var fn := Callable(RenderingServer, "
				"\"canvas_create\")\n\tvar canvas = fn.call()", ava.PASS),
			("observation", "var server = RenderingServer\n"
				"\tprint(server.get_current_rendering_method())\n"
				"\tawait server.frame_post_draw", ava.PASS),
			("unresolved_escape", "var server = RenderingServer\n"
				"\tconsume(server)", ava.COVERAGE_GAP),
			("unresolved_singleton", "var suffix := get_suffix()\n"
				"\tvar server = Engine.get_singleton("
				"\"Rendering\" + suffix + \"Server\")\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
			("conditional_singleton", "var name := \"RenderingServer\" if "
				"Time.get_ticks_msec() >= 0 else \"AudioServer\"\n"
				"\tvar server = Engine.get_singleton(name)\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
			("non_render_singleton", "var server = Engine.get_singleton("
				"\"AudioServer\")\n\tprint(server)", ava.PASS),
			("cast_render_singleton", "var server = Engine.get_singleton("
				"\"RenderingServer\") as Object\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
			("helper_render_singleton", "var server = helper_server()\n"
				"\tvar mesh = server.mesh_create()\n"
				"func helper_server():\n"
				"\treturn Engine.get_singleton(\"RenderingServer\")",
				ava.COVERAGE_GAP),
			("physics_3d_singleton", "var server = Engine.get_singleton("
				"\"PhysicsServer3D\")\n\tvar space = server.space_create()", ava.FAIL),
			("xr_singleton", "var server = Engine.get_singleton("
				"\"XRServer\")\n\tprint(server)", ava.FAIL),
			("physics_2d_singleton", "var server = Engine.get_singleton("
				"\"PhysicsServer2D\")\n\tprint(server)", ava.PASS),
			("engine_call_singleton", "var server = Engine.call("
				"\"get_singleton\", \"RenderingServer\")\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
			("engine_callv_singleton", "var server = Engine.callv("
				"\"get_singleton\", [\"RenderingServer\"])\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
			("engine_callable_singleton", "var fn = Callable(Engine, "
				"\"get_singleton\")\n\tvar server = fn.call(\"RenderingServer\")\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
			("engine_bound_singleton", "var fn = Engine.get_singleton.bind("
				"\"RenderingServer\")\n\tvar server = fn.call()\n"
				"\tvar mesh = server.mesh_create()", ava.COVERAGE_GAP),
		):
			with self.subTest(case=case), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim",
					layers_api=True)
				(root / "scripts" / "fx_stage.gd").write_text(
					"extends RefCounted\nfunc build(parent: Node) -> void:\n"
					"\tparent.add_child(Node2D.new())\n\t" + body + "\n",
					encoding="utf-8")
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, expected)

	def test_active_unsupported_script_dependencies_are_coverage_gaps(self) -> None:
		for suffix in ("cs", "gdextension", "gdc", "gde", "lua"):
			with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim",
					layers_api=True)
				dependency = root / "scripts" / f"spatial.{suffix}"
				dependency.write_text(
					"public class Spatial { /* new Node3D(); */ }\n",
					encoding="utf-8")
				(root / "scenes" / "canvas_stage.tscn").write_text(
					'[gd_scene load_steps=2 format=3]\n'
					f'[ext_resource type="Script" path="res://scripts/spatial.{suffix}" id="1"]\n'
					'[node name="Canvas" type="Node2D"]\nscript = ExtResource("1")\n',
					encoding="utf-8")
				(root / "scripts" / "fx_stage.gd").write_text(
					"extends RefCounted\nconst Stage = preload("
					"\"res://scenes/canvas_stage.tscn\")\n"
					"func build(parent: Node) -> void:\n"
					"\tparent.add_child(Stage.instantiate())\n", encoding="utf-8")
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, ava.COVERAGE_GAP)
				self.assertTrue(any("unsupported-" in value
					for value in row.evidence["dependency_gaps"]))

	def test_ignored_custom_runtime_helper_is_bound_by_source_revision(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), presentation="free_swim", layers_api=True)
			(root / ".gitignore").write_text(
				"/audit/\n/custom/\n", encoding="utf-8")
			(root / "scripts" / "fx_stage.gd").write_text(
				"extends RefCounted\nconst Helper = load("
				"\"res://custom/helper.gd\")\n"
				"func build(parent: Node) -> void:\n"
				"\tparent.add_child(Node2D.new())\n\tHelper.make(parent)\n",
				encoding="utf-8")
			ava.subprocess.run(
				["git", "-C", str(root), "add", "-f", "--", ".gitignore",
				 "scripts/fx_stage.gd"], check=True,
				stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
			ava.subprocess.run(
				["git", "-C", str(root), "commit", "-q", "-m", "active helper edge"],
				check=True, stdout=ava.subprocess.DEVNULL,
				stderr=ava.subprocess.DEVNULL)
			helper = root / "custom" / "helper.gd"
			helper.parent.mkdir(parents=True)
			helper.write_text(
				"extends RefCounted\nstatic func make(parent: Node) -> void:\n"
				"\tparent.add_child(Node2D.new())\n", encoding="utf-8")
			repo_before = ava.Repo(str(root), spec)
			manifest_before = ava.source_manifest_signature(repo_before)
			revision_before = ava.source_revision_signature(repo_before)
			self.assertTrue(ava.git_source_identity(repo_before)["dependencies_clean"])
			self.assertIn("custom/helper.gd",
				ava.builder_stage_evidence(ava.Zone(spec["zones"][0], repo_before))
				["source_dependencies"])
			helper.write_text(
				"extends RefCounted\nstatic func make(parent: Node) -> void:\n"
				"\tvar mesh := RenderingServer.mesh_create()\n", encoding="utf-8")
			repo_after = ava.Repo(str(root), spec)
			self.assertTrue(ava.git_source_identity(repo_after)["dependencies_clean"])
			self.assertNotEqual(manifest_before,
				ava.source_manifest_signature(repo_after))
			self.assertNotEqual(revision_before,
				ava.source_revision_signature(repo_after))
			self.assertEqual(
				ava.builder_stage_evidence(ava.Zone(spec["zones"][0], repo_after))
				["backend"], "legacy_3d")

	def test_active_ignored_tmp_and_audit_helpers_never_mint_pass(self) -> None:
		for ignored_root in ("tmp", "audit"):
			with self.subTest(ignored_root=ignored_root), \
					tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), presentation="free_swim", layers_api=True)
				(root / ".gitignore").write_text(
					f"/audit/\n/{ignored_root}/\n", encoding="utf-8")
				(root / "scripts" / "fx_stage.gd").write_text(
					"extends RefCounted\nconst Helper = load("
					f"\"res://{ignored_root}/helper.gd\")\n"
					"func build(parent: Node) -> void:\n"
					"\tparent.add_child(Node2D.new())\n\tHelper.make(parent)\n",
					encoding="utf-8")
				ava.subprocess.run(
					["git", "-C", str(root), "add", "-f", "--", ".gitignore",
					 "scripts/fx_stage.gd"], check=True,
					stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
				ava.subprocess.run(
					["git", "-C", str(root), "commit", "-q", "-m",
					 "active ignored helper edge"], check=True,
					stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
				helper = root / ignored_root / "helper.gd"
				helper.parent.mkdir(parents=True, exist_ok=True)
				(helper.parent / ".gdignore").write_text("", encoding="utf-8")
				helper.write_text(
					"extends RefCounted\nstatic func make(parent: Node) -> void:\n"
					"\tparent.add_child(Node2D.new())\n", encoding="utf-8")
				repo_before = ava.Repo(str(root), spec)
				identity_before = ava.git_source_identity(repo_before)
				revision_before = ava.source_revision_signature(repo_before)
				self.assertTrue(identity_before["dependencies_clean"])
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, ava.COVERAGE_GAP)
				self.assertIn(
					f"untracked-active-source:{ignored_root}/helper.gd",
					row.evidence["dependency_gaps"])
				helper.write_text(
					"extends RefCounted\nstatic func make(parent: Node) -> void:\n"
					"\tvar mesh := RenderingServer.mesh_create()\n", encoding="utf-8")
				repo_after = ava.Repo(str(root), spec)
				self.assertTrue(ava.git_source_identity(repo_after)["dependencies_clean"])
				self.assertEqual(revision_before,
					ava.source_revision_signature(repo_after))
				row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
				self.assertEqual(row.disposition, ava.FAIL)
				self.assertIn(f"{ignored_root}/helper.gd",
					row.evidence["source"]["source_dependencies"])

	def test_inactive_ignored_source_does_not_create_dependency_debt(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), presentation="free_swim", layers_api=True)
			(root / ".gitignore").write_text("/audit/\n/tmp/\n", encoding="utf-8")
			ava.subprocess.run(
				["git", "-C", str(root), "add", "--", ".gitignore"], check=True,
				stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
			ava.subprocess.run(
				["git", "-C", str(root), "commit", "-q", "-m",
				 "ignore non-runtime output"], check=True,
				stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
			helper = root / "tmp" / "inactive_helper.gd"
			helper.parent.mkdir(parents=True)
			(helper.parent / ".gdignore").write_text("", encoding="utf-8")
			helper.write_text(
				"extends RefCounted\nfunc make() -> Object:\n"
				"\treturn MeshInstance3D.new()\n", encoding="utf-8")
			self.assertTrue(ava.git_source_identity(
				ava.Repo(str(root), spec))["dependencies_clean"])
			row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
			self.assertEqual(row.disposition, ava.PASS)

	def test_clean_cyclic_canvas_helper_closure_terminates_and_passes(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), presentation="free_swim", layers_api=True)
			(root / "scripts" / "canvas_a.gd").write_text(
				"extends RefCounted\nconst B = preload(\"res://scripts/canvas_b.gd\")\n"
				"static func spawn() -> Node2D:\n\treturn Node2D.new()\n",
				encoding="utf-8")
			(root / "scripts" / "canvas_b.gd").write_text(
				"extends RefCounted\nconst A = preload(\"res://scripts/canvas_a.gd\")\n",
				encoding="utf-8")
			(root / "scripts" / "fx_stage.gd").write_text(
				"extends RefCounted\nconst A = preload(\"res://scripts/canvas_a.gd\")\n"
				"func build(parent: Node) -> void:\n\tparent.add_child(A.spawn())\n",
				encoding="utf-8")
			ava.subprocess.run(
				["git", "-C", str(root), "add", "--", "scripts/canvas_a.gd",
				 "scripts/canvas_b.gd", "scripts/fx_stage.gd"], check=True,
				stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
			ava.subprocess.run(
				["git", "-C", str(root), "commit", "-q", "-m",
				 "tracked Canvas helper closure"], check=True,
				stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
			row = self._rows(root, spec, "layering.legacy_3d_debt")[0]
			self.assertEqual(row.disposition, ava.PASS)

	def test_canvas_depth_and_occlusion_use_live_facts_without_spatial_constants(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2, depths=(), band=False)
			for check_id in ("layering.depth_spread", "layering.occlusion_band"):
				with self.subTest(check_id=check_id):
					rows = self._rows(root, spec, check_id)
					self.assertEqual(rows[0].disposition, ava.PASS)

	def test_bbox_only_occlusion_overlap_cannot_pass(self) -> None:
		for mutation in ("missing_method", "missing_painted_samples"):
			with self.subTest(mutation=mutation), \
					tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2, depths=(), band=False)
				row = spec["_runtime_facts"]["zones"]["fx"] \
					["canvas_occlusion"]["samples"][0]["front"][0]
				if mutation == "missing_method":
					row["overlap_method"] = "rectangle_intersection_v1"
				else:
					row.pop("painted_sample_count")
				self._reseal(root, spec)
				finding = self._rows(root, spec, "layering.occlusion_band")[0]
				self.assertEqual(finding.disposition, ava.FAIL)
		probe_source = (ROOT / "scripts" / "probe_visual_audit.gd").read_text(
			encoding="utf-8")
		self.assertIn("_visual_alpha_at_screen_point", probe_source)
		self.assertNotIn("_collect_canvas_bounds", probe_source)

	def test_unresolved_canvas_alpha_effects_are_coverage_gaps(self) -> None:
		mutations = {
			"layer_material_or_clip": (
				"layering.mural_is_a_stack",
				lambda spec: spec["_runtime_facts"]["zones"]["fx"]
					["canvas_parallax"]["layers"][0].update(
						{"unresolved_alpha_effects": 1}),
			),
			"occluder_material_or_clip": (
				"layering.occlusion_band",
				lambda spec: spec["_runtime_facts"]["zones"]["fx"]
					["canvas_occlusion"].update({"unresolved_alpha_effects": 1}),
			),
			"layer_draw_order": (
				"layering.mural_is_a_stack",
				lambda spec: spec["_runtime_facts"]["zones"]["fx"]
					["canvas_parallax"]["layers"][0].update(
						{"unresolved_draw_order_effects": 1}),
			),
			"occluder_draw_order": (
				"layering.occlusion_band",
				lambda spec: spec["_runtime_facts"]["zones"]["fx"]
					["canvas_occlusion"].update(
						{"unresolved_draw_order_effects": 1}),
			),
		}
		for name, (check_id, mutate) in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2, depths=(), band=False)
				mutate(spec)
				self._reseal(root, spec)
				finding = self._rows(root, spec, check_id)[0]
				self.assertEqual(finding.disposition, ava.COVERAGE_GAP)
		probe_source = (ROOT / "scripts" / "probe_visual_audit.gd").read_text(
			encoding="utf-8")
		for required in (
				"_effective_canvas_opacity", "item.self_modulate",
				"_point_inside_canvas_clips", "clip_contents",
				"_visual_has_unresolved_alpha_effect", "CanvasGroup",
				"canvas_cull_mask", "visibility_layer", "custom_viewport",
				"CanvasModulate", "Light2D", "_draw_order_effect_count",
				"show_behind_parent", "y_sort_enabled", "layer_order_groups",
				"visual_order == target_order", "_zone_canvas_audit_root",
				'is_class("Node" + "3D")'):
			self.assertIn(required, probe_source)
		self.assertIn(
			"current_canvas_global_effects = _visible_canvas_global_effect_count(get_root())",
			probe_source)
		self.assertGreaterEqual(
			probe_source.count("_zone_canvas_audit_root(main, zone_id)"), 2)
		self.assertGreaterEqual(probe_source.count("_refresh_canvas_global_effects()"), 8)

	def test_descendant_z_outside_declared_band_cannot_pass(self) -> None:
		for mutation in ("visual_crosses_band", "runtime_widens_band"):
			with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2, depths=(), band=False)
				row = spec["_runtime_facts"]["zones"]["fx"] \
					["canvas_parallax"]["layers"][0]
				if mutation == "visual_crosses_band":
					row["relative_z_max"] = 5
					row["visual_draw_order_max"] = 5
				else:
					row["allowed_relative_z_max"] = 5
				self._reseal(root, spec)
				finding = self._rows(
					root, spec, "layering.mural_is_a_stack")[0]
				self.assertEqual(finding.disposition, ava.FAIL)

	def test_occlusion_requires_meaningful_alpha_area_and_ratio(self) -> None:
		for mutation in ("alpha", "samples", "ratio"):
			with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2, depths=(), band=False)
				row = spec["_runtime_facts"]["zones"]["fx"] \
					["canvas_occlusion"]["samples"][0]["front"][0]
				if mutation == "alpha":
					row["alpha_threshold"] = 1.0 / 255.0
				elif mutation == "samples":
					row["painted_sample_count"] = 1
				else:
					row["target_overlap_ratio"] = 0.001
				self._reseal(root, spec)
				finding = self._rows(root, spec, "layering.occlusion_band")[0]
				self.assertEqual(finding.disposition, ava.FAIL)

	def test_touch_target_outside_audited_viewport_is_gap(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			spec["_runtime_facts"]["zones"]["fx"]["targets"][0] \
				["audited_viewport"] = False
			self._reseal(root, spec)
			row = self._rows(root, spec, "readability.tap_target_size")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)

	def test_touch_target_requires_live_registry_and_consistent_visible_size(self) -> None:
		mutations = {
			"zero_hit": lambda target: target.update({"hit_diameter_px": 0.0}),
			"false_result": lambda target: target.update({"meets_min_touch": False}),
			"tiny_visual": lambda target: target.update(
				{"visual_screen_px": 1.0, "visual_width_px": 1.0}),
			"wrong_registry": lambda target: target.update(
				{"interaction_registry": "highlight_only"}),
			"offscreen_resolver": lambda target: target.update(
				{"resolver_hit_screen_px": [5000.0, 5000.0],
				 "resolver_center_in_viewport": False}),
			"wrong_resolver_id": lambda target: target.update(
				{"resolver_returned_id": "some_other_target",
				 "resolver_hit_confirmed": False}),
			"resolver_far_from_art": lambda target: target.update(
				{"resolver_nearest_painted_px": 500.0}),
			"short_actual_reach": lambda target: target["resolver_reach_samples"][1]
				.update({"returned_id": "", "matches_target": False}),
		}
		for name, mutate in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				mutate(spec["_runtime_facts"]["zones"]["fx"]["targets"][0])
				self._reseal(root, spec)
				row = self._rows(root, spec, "readability.tap_target_size")[0]
				self.assertNotEqual(row.disposition, ava.PASS)
		probe_source = (ROOT / "scripts" / "probe_visual_audit.gd").read_text(
			encoding="utf-8")
		self.assertNotIn('target.get("highlight")', probe_source)
		self.assertIn('resolver.call("_target_at", point)', probe_source)
		self.assertIn("_nearest_painted_distance", probe_source)
		self.assertIn("_production_resolver_reach_samples", probe_source)

	def test_touch_visible_size_is_bound_to_clip_aware_rendered_silhouette(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			sample = spec["_runtime_facts"]["zones"]["fx"] \
				["rendered_composites"][0]["samples"][0]
			sample["figure_rect"] = [621, 328, 38, 64]
			self._reseal(root, spec)
			row = self._rows(root, spec, "readability.tap_target_size")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("rendered silhouette", row.message)
		probe_source = (ROOT / "scripts" / "probe_visual_audit.gd").read_text(
			encoding="utf-8")
		self.assertIn("_painted_visual_screen_rect", probe_source)

	def test_rendered_states_require_explicit_implemented_adapter_dispatch(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			requirements = spec["zones"][0]["rendered_readability_states"]
			requirements.append({
				"id": "pretend_boss",
				"capture_adapter": "probe_visual_audit:fx_pretend_boss",
				"required_targets": ["standee"],
			})
			duplicate = json.loads(json.dumps(spec["_runtime_facts"]["zones"]
				["fx"]["rendered_composites"][0]))
			duplicate["id"] = "pretend_boss"
			duplicate["capture_adapter"] = "probe_visual_audit:fx_pretend_boss"
			spec["_runtime_facts"]["zones"]["fx"]["rendered_composites"].append(
				duplicate)
			self._reseal(root, spec)
			row = self._rows(
				root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("not an implemented state transition", row.message)

	def test_rendered_state_assertion_and_capture_are_not_relabelable(self) -> None:
		mutations = {
			"state": lambda state: state.update(
				{"adapter_state": {"fixture": "boss", "zone": "fx"}}),
			"signature": lambda state: state.update(
				{"adapter_state_signature": "0" * 64}),
			"method": lambda state: state.update(
				{"adapter_method": "string_label_only"}),
		}
		for name, mutate in mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), layers_api=True, murals=2,
					canvas_layer_count=2)
				mutate(spec["_runtime_facts"]["zones"]["fx"]
					["rendered_composites"][0])
				self._reseal(root, spec)
				row = self._rows(
					root, spec, "palette.rendered_composite_readability")[0]
				self.assertEqual(row.disposition, ava.COVERAGE_GAP)
		probe_source = (ROOT / "scripts" / "probe_visual_audit.gd").read_text(
			encoding="utf-8")
		self.assertIn("func _capture_adapter_state", probe_source)
		self.assertIn('zone_id != "sky_lagoon"', probe_source)
		self.assertNotIn(
			'adapter == "probe_visual_audit:%s_%s"', probe_source)
		for assertion in (
			'main.g.get("lagoon_promenade_focus", "")',
			'"lagoon_play_anim", {})', "main.mg_kind",
			"main.intro_active", "main.get_tree().paused",
			"world_controls_enabled",
		):
			self.assertIn(assertion, probe_source)

	def test_touch_facts_require_the_same_current_provenance(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			self.assertEqual(
				self._rows(root, spec, "readability.tap_target_size")[0].disposition,
				ava.PASS,
			)
			(root / "scripts" / "main.gd").write_text(
				"extends Node2D\n# changed after touch measurement\n", encoding="utf-8")
			row = self._rows(root, spec, "readability.tap_target_size")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("clean checkout", row.message)

	@staticmethod
	def _rewrite_forged_triple(root: Path, spec: dict,
			boxes: list[tuple[int, int, int, int]]) -> None:
		state, sample = VisualEvidenceContractTests._state_and_sample(spec)
		hidden = Image.open(root / sample["target_hidden_capture_path"]).convert("RGB")
		mask = Image.new("L", hidden.size, 0)
		draw = ImageDraw.Draw(mask)
		for box in boxes:
			draw.rectangle(box, fill=255)
		visible = hidden.copy()
		visible.paste(Image.new("RGB", hidden.size, (255, 250, 255)), mask=mask)
		visible.save(root / state["capture_path"])
		visible.save(root / sample["target_restored_capture_path"])
		for binding in sample["target_visible_stability_captures"]:
			visible.save(root / binding["path"])
		mask.save(root / sample["mask_path"])
		bbox = mask.getbbox()
		assert bbox is not None
		sample["figure_rect"] = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
		repo = ava.Repo(str(root), spec)
		state["capture_sha256"] = repo.sha256(state["capture_path"])
		sample["target_restored_capture_sha256"] = repo.sha256(
			sample["target_restored_capture_path"])
		for binding in sample["target_visible_stability_captures"]:
			binding["sha256"] = repo.sha256(binding["path"])
		sample["mask_sha256"] = repo.sha256(sample["mask_path"])
		VisualEvidenceContractTests._reseal(root, spec)

	def test_forged_complete_triple_and_impossible_metadata_cannot_pass(self) -> None:
		metadata_mutations = {
			"forged_paths": lambda state, sample: (
				sample.update({"target_instance_path": "/root/Forged/Target"}),
				sample["visuals"][0].update({"instance_path": "/root/Forged/Target/Visual"})),
			"singular_transform": lambda _state, sample: sample["visuals"][0].update(
				{"canvas_transform": [1.0, 2.0, 2.0, 4.0, 640.0, 360.0]}),
			"offscreen_transform": lambda _state, sample: sample["visuals"][0].update(
				{"canvas_transform": [1.0, 0.0, 0.0, 1.0, 5000.0, 5000.0]}),
			"impossible_frame": lambda _state, sample: sample["visuals"][0]
				["projection"].update({"frame_coords": [2, 0]}),
			"impossible_region": lambda _state, sample: sample["visuals"][0]
				["projection"].update({"region_enabled": True,
					"region_rect": [250, 250, 64, 64]}),
			"non_boolean_flip": lambda _state, sample: sample["visuals"][0]
				["projection"].update({"flip_h": "false"}),
		}
		for name, mutate in metadata_mutations.items():
			with self.subTest(name=name), tempfile.TemporaryDirectory() as raw_root:
				root = Path(raw_root)
				spec = ava._fixture(str(root), mural_rgb=(0, 255, 255),
					fg_rgb=(150, 150, 155), layers_api=True, murals=2,
					canvas_layer_count=2)
				state, sample = self._state_and_sample(spec)
				mutate(state, sample)
				self._reseal(root, spec)
				self.assertEqual(self._rows(
					root, spec, "palette.rendered_composite_readability")[0].disposition,
					ava.COVERAGE_GAP)
				self.assertEqual(self._rows(
					root, spec, "palette.background_recessive")[0].disposition,
					ava.REVIEW_OPEN)
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), mural_rgb=(0, 255, 255),
				fg_rgb=(150, 150, 155), layers_api=True, murals=2,
				canvas_layer_count=2)
			self._rewrite_forged_triple(root, spec, [(80, 80, 104, 104)])
			row = self._rows(root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("source-alpha projection", row.message)
			self.assertEqual(self._rows(
				root, spec, "palette.background_recessive")[0].disposition,
				ava.REVIEW_OPEN)

	def test_inner_rectangle_cannot_substitute_for_projected_silhouette(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), mural_rgb=(0, 255, 255),
				fg_rgb=(150, 150, 155), layers_api=True, murals=2,
				canvas_layer_count=2)
			self._rewrite_forged_triple(root, spec, [(615, 340, 664, 379)])
			row = self._rows(
				root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("silhouette contour", row.message)
			self.assertEqual(self._rows(
				root, spec, "palette.background_recessive")[0].disposition,
				ava.REVIEW_OPEN)

	def test_required_target_ids_cannot_reuse_one_live_instance(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			state = spec["_runtime_facts"]["zones"]["fx"]["rendered_composites"][0]
			proxy = json.loads(json.dumps(state["samples"][0]))
			proxy["id"] = "proxy"
			state["samples"].append(proxy)
			requirement = spec["zones"][0]["rendered_readability_states"][0]
			requirement["required_targets"] = ["standee", "proxy"]
			requirement["min_samples"] = 2
			self._reseal(root, spec)
			row = self._rows(
				root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("reuses live target instance ownership", row.message)

	def test_periodic_unrelated_patch_cannot_establish_target_causality(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			state, sample = self._state_and_sample(spec)
			hidden_bindings = [{
				"path": sample["target_hidden_capture_path"],
				"sha256": sample["target_hidden_capture_sha256"],
			}, *sample["target_hidden_stability_captures"]]
			for binding in hidden_bindings:
				image = Image.open(root / binding["path"]).convert("RGB")
				ImageDraw.Draw(image).rectangle((40, 40, 99, 99), fill=(0, 0, 0))
				image.save(root / binding["path"])
			mask = Image.open(root / sample["mask_path"]).convert("L")
			ImageDraw.Draw(mask).rectangle((40, 40, 99, 99), fill=255)
			mask.save(root / sample["mask_path"])
			bbox = mask.getbbox()
			assert bbox is not None
			sample["figure_rect"] = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
			repo = ava.Repo(str(root), spec)
			sample["target_hidden_capture_sha256"] = repo.sha256(
				sample["target_hidden_capture_path"])
			for binding in sample["target_hidden_stability_captures"]:
				binding["sha256"] = repo.sha256(binding["path"])
			sample["mask_sha256"] = repo.sha256(sample["mask_path"])
			self._reseal(root, spec)
			row = self._rows(root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("projection", row.message)

	def test_renewing_json_hashes_cannot_bless_dirty_source(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), layers_api=True, murals=2,
				canvas_layer_count=2)
			(root / "scripts" / "main.gd").write_text(
				"extends Node2D\n# stale capture source\n", encoding="utf-8")
			repo = ava.Repo(str(root), spec, spec["_runtime_facts"])
			contract = spec["_runtime_facts"]["evidence_contract"]
			contract["files"]["main_script"]["sha256"] = repo.sha256("scripts/main.gd")
			contract["source_manifest"] = ava.source_manifest_signature(repo)
			contract["source_revision"] = ava.source_revision_signature(repo)
			contract["run_identity"] = "0" * 64
			for block in spec["_runtime_facts"]["zones"]["fx"].values():
				if isinstance(block, dict) and "run_identity" in block:
					block["run_identity"] = "0" * 64
			for state in spec["_runtime_facts"]["zones"]["fx"]["rendered_composites"]:
				state["run_identity"] = "0" * 64
			row = self._rows(root, spec, "palette.rendered_composite_readability")[0]
			self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			self.assertIn("clean checkout", row.message)

	def test_committed_source_and_renewed_json_cannot_reuse_old_captures(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			spec = ava._fixture(str(root), mural_rgb=(0, 255, 255),
				fg_rgb=(150, 150, 155), layers_api=True, murals=2,
				canvas_layer_count=2)
			runtime = spec["_runtime_facts"]
			(root / "scripts" / "main.gd").write_text(
				"extends Node2D\n# committed post-capture change\n", encoding="utf-8")
			(root / "assets" / "shaders" / "fixture.gdshader").write_text(
				"shader_type canvas_item;\n# committed post-capture shader\n",
				encoding="utf-8")
			ava.subprocess.run(
				["git", "-C", str(root), "add", "--", "scripts/main.gd",
					"assets/shaders/fixture.gdshader"], check=True,
				stdout=ava.subprocess.DEVNULL, stderr=ava.subprocess.DEVNULL)
			ava.subprocess.run(
				["git", "-C", str(root), "commit", "-q", "-m", "renew source"],
				check=True, stdout=ava.subprocess.DEVNULL,
				stderr=ava.subprocess.DEVNULL)

			repo = ava.Repo(str(root), spec, runtime)
			contract = runtime["evidence_contract"]
			identity = ava.git_source_identity(repo)
			contract["files"]["main_script"]["sha256"] = repo.sha256(
				"scripts/main.gd")
			contract["source_manifest"] = ava.source_manifest_signature(repo)
			contract["source_revision"] = ava.source_revision_signature(repo)
			contract["git_revision"] = identity["revision"]
			contract["git_tree"] = identity["tree"]
			contract["git_dependencies_clean"] = identity["dependencies_clean"]
			contract["run_identity"] = ava.hashlib.sha256("|".join([
				identity["revision"], identity["tree"], contract["fresh_challenge"],
				contract["source_revision"], contract["run_nonce"],
				contract["run_started_utc"], contract["engine"]["version_string"],
				contract["renderer"]["actual"],
			]).encode("utf-8")).hexdigest()
			zone = runtime["zones"]["fx"]
			zone["run_identity"] = contract["run_identity"]
			for key in ("canvas_parallax", "canvas_occlusion"):
				zone[key]["run_identity"] = contract["run_identity"]
			for state in zone["rendered_composites"]:
				state["run_identity"] = contract["run_identity"]
			self.assertTrue(ava.git_source_identity(repo)["dependencies_clean"])
			for check_id in (
				"palette.rendered_composite_readability",
				"layering.mural_is_a_stack", "readability.tap_target_size",
			):
				with self.subTest(check_id=check_id):
					row = self._rows(root, spec, check_id)[0]
					self.assertEqual(row.disposition, ava.COVERAGE_GAP)
			static = self._rows(root, spec, "palette.background_recessive")[0]
			self.assertEqual(static.disposition, ava.REVIEW_OPEN)


class TextureBudgetTests(unittest.TestCase):
	"""The M11 peak follows Godot imports and mutually exclusive action sets."""

	@staticmethod
	def _asset(root: Path, name: str, size: tuple[int, int], mode: int,
			alpha: int = 255) -> str:
		path = root / "assets" / name
		path.parent.mkdir(parents=True, exist_ok=True)
		Image.new("RGBA", size, (24, 96, 160, alpha)).save(path)
		Path(f"{path}.import").write_text(
			"[params]\n"
			f"compress/mode={mode}\n"
			"compress/high_quality=false\n"
			"mipmaps/generate=false\n",
			encoding="utf-8",
		)
		return path.relative_to(root).as_posix()

	@staticmethod
	def _zone(root: Path, raw: dict) -> ava.Zone:
		spec = {"budgets": {}, "rules": {}, "waivers": []}
		return ava.Zone(raw, ava.Repo(str(root), spec))

	def test_vram_compressed_opaque_import_uses_etc2_rgb_blocks(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			rel = self._asset(root, "opaque.png", (64, 64), 2)
			raw = {
				"id": "fixture", "name": "fixture", "murals": [rel],
				"budgets": {"zone_runtime_texture_mb": 0.005},
			}
			compressed_zone = self._zone(root, raw)
			compressed = list(ava._texture_budget(compressed_zone))[0]
			self.assertEqual(compressed.disposition, ava.PASS)
			self.assertEqual(compressed_zone.repo.texture_vram_bytes(rel), 2048)
			alpha_rel = self._asset(root, "alpha.png", (64, 64), 2, alpha=128)
			self.assertEqual(
				self._zone(root, raw).repo.texture_vram_bytes(alpha_rel), 4096)

			Path(f"{root / rel}.import").write_text(
				"[params]\ncompress/mode=0\n"
				"compress/high_quality=false\nmipmaps/generate=false\n",
				encoding="utf-8",
			)
			uncompressed_zone = self._zone(root, raw)
			uncompressed = list(ava._texture_budget(uncompressed_zone))[0]
			self.assertEqual(uncompressed.disposition, ava.FAIL)
			self.assertEqual(uncompressed_zone.repo.texture_vram_bytes(rel), 16384)
			self.assertGreater(uncompressed.evidence["vram_mb"], 0.015)

	def test_peak_alternatives_count_one_complete_action_set(self) -> None:
		with tempfile.TemporaryDirectory() as raw_root:
			root = Path(raw_root)
			base = self._asset(root, "base.png", (64, 64), 0)
			for name, size in (("swing_0.png", (32, 32)),
					("swing_1.png", (32, 32)), ("slide_0.png", (16, 16)),
					("slide_1.png", (16, 16))):
				self._asset(root, f"actions/{name}", size, 0)
			raw = {
				"id": "fixture", "name": "fixture",
				"murals": [base], "characters": ["assets/actions/*.png"],
				"budgets": {"zone_runtime_texture_mb": 0.024},
				"texture_peak_alternatives": [{
					"id": "action",
					"alternatives": [
						{"id": "swing", "files": ["assets/actions/swing_*.png"],
							"expected_count": 2},
						{"id": "slide", "files": ["assets/actions/slide_*.png"],
							"expected_count": 2},
					],
				}],
			}
			grouped = list(ava._texture_budget(self._zone(root, raw)))[0]
			self.assertEqual(grouped.disposition, ava.PASS)
			self.assertEqual(grouped.evidence["peak_files"], 3)
			self.assertEqual(grouped.evidence["alternatives"][0]["selected"], "swing")

			ungrouped_raw = dict(raw)
			ungrouped_raw.pop("texture_peak_alternatives")
			ungrouped = list(ava._texture_budget(
				self._zone(root, ungrouped_raw)))[0]
			self.assertEqual(ungrouped.disposition, ava.REVIEW_OPEN)

			bad_raw = dict(raw)
			bad_raw["texture_peak_alternatives"] = [{
				"id": "action", "alternatives": [{
					"id": "swing", "files": ["assets/actions/swing_*.png"],
					"expected_count": 3,
				}],
			}]
			invalid = list(ava._texture_budget(self._zone(root, bad_raw)))[0]
			self.assertEqual(invalid.disposition, ava.FAIL)


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
		# Keep this a deterministic hard-failure fixture. The real Lagoon layer
		# contract may legitimately move from a declaration error to a runtime
		# coverage gap as its registered holders are repaired.
		sky_zone = next(zone for zone in spec["zones"]
			if zone["id"] == "sky_lagoon")
		sky_zone["canvas_layers"][1]["id"] = \
			sky_zone["canvas_layers"][0]["id"]
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
