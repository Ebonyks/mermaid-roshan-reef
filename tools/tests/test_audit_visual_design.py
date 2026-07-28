from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import audit_visual_design as ava  # noqa: E402


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

	def test_waivers_reference_real_checks_and_zones(self) -> None:
		spec = ava.load_spec()
		zone_ids = {z["id"] for z in spec["zones"]}
		for w in spec.get("waivers", []):
			self.assertIn(w["check"], ava.REGISTRY, "waiver for unknown check")
			self.assertIn(w["zone"], zone_ids, "waiver for unknown zone")
			self.assertTrue(w.get("reason"), "a waiver without a reason is a silent bug")


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

	def test_every_zone_produces_at_least_one_finding(self) -> None:
		"""A zone that produces nothing is invisible — SKIP is a finding, silence is not."""
		repo = ava.Repo(str(ROOT), ava.load_spec())
		findings = ava.run(repo)
		seen = {f.zone for f in findings}
		for zone in ava.load_spec()["zones"]:
			self.assertIn(zone["id"], seen, f"{zone['id']} was audited into silence")

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
			finally:
				ava.REPORT_JSON, ava.REPORT_MD = old_json, old_md


if __name__ == "__main__":
	unittest.main()
