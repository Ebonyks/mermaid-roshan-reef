"""Regression tests for regenerated cinematic subject-mask extraction."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


TOOL = Path(__file__).parents[1] / "extract_cinematic_subject_mask.py"
SPEC = importlib.util.spec_from_file_location("extract_cinematic_subject_mask", TOOL)
EXTRACT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = EXTRACT
SPEC.loader.exec_module(EXTRACT)


class CinematicSubjectMaskTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.background = self.root / "background.png"
        self.candidate = self.root / "candidate.png"
        Image.new("RGB", (64, 36), (20, 100, 180)).save(self.background)
        image = Image.new("RGB", (64, 36), (20, 100, 180))
        draw = ImageDraw.Draw(image)
        draw.rectangle((4, 10, 29, 25), fill=(245, 240, 255))
        draw.rectangle((50, 2, 52, 4), fill=(245, 240, 255))
        image.save(self.candidate)

    def tearDown(self):
        self.temporary.cleanup()

    def test_extracts_largest_changed_component_and_anchors(self):
        component, report = EXTRACT.extract_largest_component(
            self.candidate,
            self.background,
            (0.0, 0.0, 1.0, 1.0),
            threshold=50,
            opening_iterations=0,
            closing_iterations=0,
            minimum_area=10,
        )
        self.assertEqual(report["bbox_pixels"], [4, 10, 30, 26])
        self.assertAlmostEqual(report["anchors"]["bbox_right"][0], 30 / 64)
        self.assertEqual(int(component.sum()), 26 * 16)

    def test_rejects_mismatched_clean_plate_size(self):
        Image.new("RGB", (32, 18)).save(self.background)
        with self.assertRaisesRegex(ValueError, "does not match clean-plate size"):
            EXTRACT.extract_largest_component(
                self.candidate,
                self.background,
                (0.0, 0.0, 1.0, 1.0),
                threshold=50,
                opening_iterations=0,
                closing_iterations=0,
                minimum_area=10,
            )

    def test_purple_outline_ignores_touching_white_cloud_change(self):
        image = Image.new("RGB", (64, 36), (20, 100, 180))
        draw = ImageDraw.Draw(image)
        draw.rectangle((4, 10, 29, 25), fill=(145, 80, 190))
        draw.rectangle((29, 10, 50, 25), fill=(245, 245, 250))
        image.save(self.candidate)
        _, report = EXTRACT.extract_largest_component(
            self.candidate,
            self.background,
            (0.0, 0.0, 1.0, 1.0),
            threshold=50,
            opening_iterations=0,
            closing_iterations=0,
            minimum_area=10,
            segmentation="purple_outline",
        )
        self.assertEqual(report["bbox_pixels"], [4, 10, 29, 26])

    def test_purple_outline_allows_a_different_clean_plate_size(self):
        Image.new("RGB", (32, 18)).save(self.background)
        image = Image.new("RGB", (64, 36), (20, 100, 180))
        ImageDraw.Draw(image).rectangle(
            (4, 10, 29, 25),
            fill=(145, 80, 190),
        )
        image.save(self.candidate)
        _, report = EXTRACT.extract_largest_component(
            self.candidate,
            self.background,
            (0.0, 0.0, 1.0, 1.0),
            threshold=50,
            opening_iterations=0,
            closing_iterations=0,
            minimum_area=10,
            segmentation="purple_outline",
        )
        self.assertEqual(report["size"], [64, 36])
        self.assertEqual(report["clean_plate"]["size"], [32, 18])
        self.assertFalse(report["clean_plate"]["used_for_segmentation"])


if __name__ == "__main__":
    unittest.main()
