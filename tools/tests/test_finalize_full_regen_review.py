from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import finalize_full_regen_review as finalizer  # noqa: E402


class RenderMetricIndexTests(unittest.TestCase):
	def test_indexes_png_metric_by_shared_model_name(self) -> None:
		rows = [{
			"name": "example_model",
			"path": "audit/renders/example_model.png",
			"status": "pass",
		}]

		indexed = finalizer.index_render_metrics(rows)

		self.assertEqual(indexed["example_model"]["path"], rows[0]["path"])

	def test_rejects_duplicate_model_names(self) -> None:
		rows = [
			{"name": "duplicate", "status": "pass"},
			{"name": "duplicate", "status": "reject"},
		]

		with self.assertRaisesRegex(ValueError, "duplicate model name duplicate"):
			finalizer.index_render_metrics(rows)

	def test_rejects_non_verdict_status(self) -> None:
		with self.assertRaisesRegex(ValueError, "invalid render status"):
			finalizer.index_render_metrics([{"name": "model", "status": "not_applicable"}])

	def test_rejects_missing_model_metric(self) -> None:
		assets = [Path("models/model.glb"), Path("textures/tile.png")]

		with self.assertRaisesRegex(ValueError, "missing metrics for model"):
			finalizer.validate_render_metric_coverage(assets, {})

	def test_rejects_stale_model_metric(self) -> None:
		metrics = {"removed_model": {"name": "removed_model", "status": "pass"}}

		with self.assertRaisesRegex(ValueError, "stale metrics for removed_model"):
			finalizer.validate_render_metric_coverage([], metrics)


class FinalizedLedgerTests(unittest.TestCase):
	def test_every_candidate_model_has_a_real_render_verdict(self) -> None:
		rows = finalizer.read_csv(finalizer.AUDIT / "candidate_asset_review.csv")
		model_rows = [row for row in rows if row["kind"] == "model_3d"]
		texture_rows = [row for row in rows if row["kind"] == "texture_2d"]

		self.assertEqual(len(model_rows), 137)
		self.assertEqual(len(texture_rows), 30)
		self.assertTrue(
			all(row["render_status"] in finalizer.VALID_RENDER_STATUSES for row in model_rows)
		)
		self.assertTrue(all(row["render_status"] == "not_applicable" for row in texture_rows))


if __name__ == "__main__":
	unittest.main()
