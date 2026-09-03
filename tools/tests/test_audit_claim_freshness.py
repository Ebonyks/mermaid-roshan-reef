from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import audit_claim_freshness as claims


def _fixture_root() -> tempfile.TemporaryDirectory:
	directory = tempfile.TemporaryDirectory()
	root = Path(directory.name)
	(root / "scripts").mkdir()
	(root / "scripts" / "a.gd").write_text(
		"func one():\n\tm._helper()\n\tg[\"alpha\"] = 1\nfunc two():\n\tm._helper()\n\tg[\"beta\"] = 2\n\tg[\"alpha\"] = 3\n",
		encoding="utf-8",
	)
	(root / "scripts" / "probe_x.gd").write_text("x\n" * 5, encoding="utf-8")
	(root / "doc.md").write_text(
		"Two functions live in `scripts/a.gd:4`; a pinned `a.gd:900` at `deadbeef1` is history.\n"
		"There are 2 distinct keys and the roster is `for p in probe_x probe_y probe_z; do`.\n",
		encoding="utf-8",
	)
	(root / "ci.sh").write_text("for p in probe_x probe_y probe_z; do\n\techo $p\ndone\n", encoding="utf-8")
	return directory


class MeasurementTests(unittest.TestCase):
	def test_each_kind_measures_the_fixture(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			cases = {
				"line_count": ({"paths": ["scripts/a.gd"]}, 7),
				"regex_count": ({"paths": ["scripts/*.gd"], "pattern": r"m\._helper\("}, 2),
				"regex_line_count": ({"paths": ["scripts/a.gd"], "pattern": r"^func "}, 2),
				"regex_distinct": ({"paths": ["scripts/*.gd"], "pattern": r'g\["[a-z]+"\]'}, 2),
				"literal_count": ({"paths": ["scripts/a.gd"], "literal": "g["}, 3),
				"literal_line_count": ({"paths": ["scripts/a.gd"], "literal": "func"}, 2),
				"glob_count": ({"paths": ["scripts/probe_*.gd"]}, 1),
				"files_over": ({"paths": ["scripts/*.gd"], "threshold": 6, "exclude": "probe_"}, 1),
				"line_tokens": ({"paths": ["ci.sh"], "line_regex": r"^for p in", "token_regex": r"\bprobe_[a-z]+"}, 3),
			}
			for kind, (params, expected) in cases.items():
				measured = claims.MEASURES[kind](root, dict(params, id=kind))
				self.assertEqual(expected, measured, kind)

	def test_evaluate_claim_reports_each_status(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			base = {"id": "funcs", "kind": "regex_line_count", "paths": ["scripts/a.gd"], "pattern": r"^func ",
				"expected": 2, "doc": "doc.md", "statement": r"Two functions"}
			self.assertTrue(all(r.status == "OK" for r in claims.evaluate_claim(root, base, ["."])))
			self.assertIn("STALE_TREE", {r.status for r in claims.evaluate_claim(root, dict(base, expected=5), ["."])})
			self.assertIn("STALE_DOC", {r.status for r in claims.evaluate_claim(root, dict(base, statement="Nine"), ["."])})
			self.assertIn("BROKEN", {r.status for r in claims.evaluate_claim(root, {"id": "x", "kind": "nope"}, ["."])})
			self.assertIn("BROKEN", {r.status for r in claims.evaluate_claim(root, dict(base, pattern="("), ["."])})


class AnchorTests(unittest.TestCase):
	def test_anchor_ok_drift_and_fail(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			anchor = {"id": "a", "kind": "anchor", "path": "a.gd", "line": 4, "token": "func two"}
			self.assertEqual("OK", claims.check_anchor(root, anchor, ["scripts"]).status)
			drift = claims.check_anchor(root, dict(anchor, line=1), ["scripts"])
			self.assertEqual("DRIFT", drift.status)
			self.assertIn("to line 4", drift.detail)
			self.assertEqual("FAIL", claims.check_anchor(root, dict(anchor, token="func nine"), ["scripts"]).status)
			self.assertEqual("FAIL", claims.check_anchor(root, dict(anchor, path="missing.gd"), ["scripts"]).status)

	def test_bare_anchor_sweep_flags_beyond_eof_and_skips_pinned_history(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			(root / "doc3.md").write_text("Live `scripts/a.gd:40` is beyond the file.\n", encoding="utf-8")
			results, stats = claims.sweep_bare_anchors(root, ["doc.md", "doc3.md"], ["scripts", "."])
			self.assertEqual(1, stats["pinned"])
			self.assertEqual(2, stats["checked"])
			self.assertEqual(1, stats["failed"])
			self.assertTrue(any("beyond the file" in r.detail for r in results))

	def test_refresh_anchors_rewrites_only_drifted_lines(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			(root / "tools").mkdir()
			manifest = {"search_roots": ["scripts"], "documents": [], "claims": [
				{"id": "a", "kind": "anchor", "path": "a.gd", "line": 1, "token": "func two"},
				{"id": "b", "kind": "anchor", "path": "a.gd", "line": 1, "token": "func one"},
				{"id": "c", "kind": "line_count", "paths": ["scripts/a.gd"], "expected": 1},
			]}
			(root / claims.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
			self.assertEqual(1, claims.refresh_anchors(root, manifest))
			saved = json.loads((root / claims.MANIFEST).read_text(encoding="utf-8"))
			self.assertEqual(4, saved["claims"][0]["line"])
			self.assertEqual(1, saved["claims"][1]["line"])
			self.assertEqual(1, saved["claims"][2]["expected"], "expected counts are never auto-refreshed")


class ModeTests(unittest.TestCase):
	def test_report_mode_warns_and_strict_mode_fails_on_stale_claims(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			(root / "tools").mkdir()
			manifest = {"search_roots": ["scripts", "."], "documents": ["doc.md"], "claims": [
				{"id": "funcs", "kind": "regex_line_count", "paths": ["scripts/a.gd"], "pattern": r"^func ",
					"expected": 9, "doc": "doc.md", "statement": r"Two functions"},
			]}
			(root / claims.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
			self.assertEqual(0, claims.main(["--root", str(root)]))
			self.assertEqual(1, claims.main(["--root", str(root), "--strict"]))

	def test_broken_manifest_fails_even_in_report_mode(self) -> None:
		with _fixture_root() as directory:
			root = Path(directory)
			(root / "tools").mkdir()
			manifest = {"claims": [{"id": "x", "kind": "nonsense"}]}
			(root / claims.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
			self.assertEqual(1, claims.main(["--root", str(root)]))


class RepositoryManifestTests(unittest.TestCase):
	def test_repository_manifest_is_measurable(self) -> None:
		manifest = claims.load_manifest(claims.REPO)
		results, _ = claims.run(claims.REPO, manifest)
		broken = [r for r in results if r.status == "BROKEN"]
		self.assertEqual([], broken)
		self.assertTrue(manifest["claims"], "manifest must register claims")


if __name__ == "__main__":
	unittest.main()
