from __future__ import annotations

from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from PIL import Image, ImageDraw

from tools import build_seek_animation_assets as build_seek


class SeekAnimationAssetTests(unittest.TestCase):
    def test_border_connected_chroma_preserves_enclosed_key_color(self) -> None:
        source = Image.new("RGB", (64, 64), (0, 255, 0))
        draw = ImageDraw.Draw(source)
        draw.rectangle((14, 14, 49, 49), fill=(18, 20, 36))
        draw.rectangle((24, 24, 39, 39), fill=(0, 255, 0))

        result, metrics = build_seek._remove_border_chroma(
            source,
            (0, 255, 0),
        )

        self.assertEqual(result.getpixel((0, 0))[3], 0)
        self.assertEqual(result.getpixel((31, 31))[3], 255)
        self.assertGreater(metrics["transparent_pixels"], 0)

    def test_neighbor_fragment_is_removed_without_clipping_primary_actor(self) -> None:
        source = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(source)
        draw.ellipse((20, 10, 62, 72), fill=(240, 245, 255, 255))
        draw.rectangle((0, 35, 7, 44), fill=(255, 190, 90, 255))

        cleaned, removed = build_seek._keep_primary_component(source)

        self.assertGreater(removed, 0)
        self.assertEqual(cleaned.getpixel((3, 39))[3], 0)
        self.assertEqual(cleaned.getpixel((40, 40))[3], 255)

    def test_edge_despill_preserves_enclosed_key_colored_art(self) -> None:
        source = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(source)
        draw.rectangle((10, 10, 69, 69), fill=(30, 40, 70, 255))
        draw.rectangle((10, 10, 69, 12), fill=(20, 220, 30, 255))
        draw.rectangle((35, 35, 44, 44), fill=(0, 255, 0, 255))

        cleaned, metrics = build_seek._despill_transparent_edges(
            source,
            (0, 255, 0),
            radius=8,
        )

        edge = cleaned.getpixel((30, 11))
        self.assertLessEqual(edge[1], max(edge[0], edge[2]))
        self.assertEqual(cleaned.getpixel((39, 39)), (0, 255, 0, 255))
        self.assertGreater(metrics["pixels"], 0)

    def test_current_sources_build_bounded_power_of_two_atlases(self) -> None:
        outputs, manifest = build_seek.build()

        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["grid"], [4, 2])
        self.assertEqual(manifest["cell_size"], [256, 256])
        self.assertEqual(len(outputs), 3)
        for path, payload in outputs.items():
            with Image.open(BytesIO(payload)) as image:
                expected_size = (256, 256) if path.name == "evie_portrait.png" \
                    else (1024, 512)
                self.assertEqual(image.size, expected_size)
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.getpixel((0, 0))[3], 0)
                self.assertEqual(image.getpixel((image.width - 1, image.height - 1))[3], 0)
                actor = "lamma" if "lamma" in path.name else "evie"
                spec = next(item for item in build_seek.ACTORS if item.actor == actor)
                _cleaned, residue = build_seek._despill_transparent_edges(
                    image,
                    spec.declared_key,
                )
                self.assertEqual(residue["pixels"], 0)

        for actor in ("evie", "lamma"):
            self.assertGreater(
                manifest["actors"][actor]["atlas"]["edge_despill"]["pixels"],
                0,
            )
            boxes = manifest["actors"][actor]["atlas"]["runtime_cell_boxes"]
            self.assertEqual(len(boxes), 8)
            for left, top, right, bottom in boxes:
                self.assertGreater(left, 0)
                self.assertGreater(top, 0)
                self.assertLess(right, 256)
                self.assertLess(bottom, 256)
                self.assertGreater((right - left) * (bottom - top), 5000)

    def test_authored_lamma_hop_keeps_vertical_motion(self) -> None:
        _outputs, manifest = build_seek.build()
        boxes = manifest["actors"]["lamma"]["atlas"]["runtime_cell_boxes"][4:8]
        tops = [box[1] for box in boxes]
        bottoms = [box[3] for box in boxes]
        self.assertGreater(max(tops) - min(tops), 8)
        self.assertGreater(max(bottoms) - min(bottoms), 8)

    def test_source_fingerprint_rejects_drift(self) -> None:
        spec = build_seek.ACTORS[0]
        with tempfile.TemporaryDirectory() as directory:
            source_dir = Path(directory)
            original = build_seek.SOURCE_DIR / spec.source_name
            payload = bytearray(original.read_bytes())
            payload[-1] ^= 1
            (source_dir / spec.source_name).write_bytes(payload)
            with mock.patch.object(build_seek, "SOURCE_DIR", source_dir):
                with self.assertRaisesRegex(ValueError, "expected"):
                    build_seek._build_actor(spec)


if __name__ == "__main__":
    unittest.main()
