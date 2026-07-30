"""Regression tests for pre-generation cinematic job provenance."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


TOOL = Path(__file__).parents[1] / "create_cinematic_regeneration_job.py"
SPEC = importlib.util.spec_from_file_location(
    "create_cinematic_regeneration_job",
    TOOL,
)
JOBS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = JOBS
SPEC.loader.exec_module(JOBS)


class CinematicRegenerationJobTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.template = self.root / "template.txt"
        self.previous = self.root / "previous.png"
        self.guide = self.root / "guide.png"
        self.template.write_text(
            "frame={frame06} prior={previous_frame06} "
            "edge={target_edge} delta={delta}\n",
            encoding="utf-8",
        )
        self.previous.write_bytes(b"previous")
        self.guide.write_bytes(b"guide")

    def tearDown(self):
        self.temporary.cleanup()

    def test_writes_prompt_before_generation_with_hashed_references(self):
        output = self.root / "build" / "frame_000003"
        job = JOBS.render_job(
            self.template,
            self.previous,
            self.guide,
            output,
            frame=3,
            previous_frame=2,
            target_edge=729,
            previous_edge=715,
            canvas_width=1672,
            canvas_height=941,
        )
        self.assertEqual(job["delta"], 14)
        self.assertEqual(
            (output / "prompt.txt").read_text(encoding="utf-8"),
            "frame=000003 prior=000002 edge=729 delta=14\n",
        )
        self.assertEqual(
            [item["role"] for item in job["generation_references"]],
            ["accepted_neighbor", "position_only"],
        )
        self.assertTrue(
            all(
                not item["used_as_delivery_pixels"]
                for item in job["generation_references"]
            )
        )

    def test_rejects_output_outside_build(self):
        with self.assertRaisesRegex(ValueError, "under an ignored build"):
            JOBS.render_job(
                self.template,
                self.previous,
                self.guide,
                self.root / "frame_000003",
                frame=3,
                previous_frame=2,
                target_edge=729,
                previous_edge=715,
                canvas_width=1672,
                canvas_height=941,
            )


if __name__ == "__main__":
    unittest.main()
