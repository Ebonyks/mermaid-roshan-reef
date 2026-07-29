"""Regression tests for position-only cinematic regeneration guides."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


TOOL = Path(__file__).parents[1] / "create_cinematic_position_guides.py"
SPEC = importlib.util.spec_from_file_location(
    "create_cinematic_position_guides",
    TOOL,
)
GUIDES = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = GUIDES
SPEC.loader.exec_module(GUIDES)


class CinematicPositionGuideTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "subject.png"
        subject = Image.new("RGBA", (16, 8), (0, 0, 0, 0))
        ImageDraw.Draw(subject).rectangle((2, 1, 13, 6), fill=(20, 40, 60, 255))
        subject.save(self.source)

    def tearDown(self):
        self.temporary.cleanup()

    def test_guide_has_neutral_background_and_no_scene_reference(self):
        output = self.root / "build" / "guides"
        manifest = GUIDES.render_guides(
            self.source,
            output,
            frame_count=2,
            size=(128, 72),
            start_center=(0.5, 0.5),
            end_center=(0.55, 0.5),
            occupancy_width=0.25,
        )
        self.assertIsNone(manifest["reference_background"])
        self.assertFalse(manifest["appearance_authority"])
        self.assertTrue(manifest["position_authority_only"])
        with Image.open(output / "guides" / "frame_000000_guide.png") as image:
            self.assertEqual(image.getpixel((127, 71)), GUIDES.BACKGROUND_COLOR)
            self.assertIn(GUIDES.GUIDE_COLOR, image.getdata())

    def test_marker_only_guide_contains_no_subject_chroma(self):
        output = self.root / "build" / "markers"
        manifest = GUIDES.render_guides(
            self.source,
            output,
            frame_count=1,
            size=(128, 72),
            start_center=(0.5, 0.5),
            end_center=(0.5, 0.5),
            occupancy_width=0.25,
            guide_mode="marker_only",
        )
        self.assertEqual(manifest["guide_mode"], "marker_only")
        with Image.open(output / "guides" / "frame_000000_guide.png") as image:
            self.assertNotIn(GUIDES.GUIDE_COLOR, image.getdata())


if __name__ == "__main__":
    unittest.main()
