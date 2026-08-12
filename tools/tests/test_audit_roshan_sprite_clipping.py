from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from tools.audit_roshan_sprite_clipping import inspect_playground_frame


class PlaygroundFrameAuditTests(unittest.TestCase):
	def _write(self, path: Path, boxes: list[tuple[int, int, int, int]]) -> None:
		image = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
		draw = ImageDraw.Draw(image)
		for box in boxes:
			draw.rectangle(box, fill=(240, 120, 220, 255))
		image.save(path)

	def test_accepts_one_complete_silhouette_with_review_margin(self) -> None:
		with tempfile.TemporaryDirectory() as raw:
			path = Path(raw) / "good.png"
			self._write(path, [(20, 20, 491, 491)])
			self.assertEqual(inspect_playground_frame(path, 8), [])

	def test_rejects_edge_contact(self) -> None:
		with tempfile.TemporaryDirectory() as raw:
			path = Path(raw) / "clipped.png"
			self._write(path, [(0, 20, 491, 491)])
			failures = inspect_playground_frame(path, 8)
			self.assertTrue(any("silhouette margins" in line for line in failures))

	def test_rejects_detached_generation_fragment(self) -> None:
		with tempfile.TemporaryDirectory() as raw:
			path = Path(raw) / "ghost.png"
			self._write(path, [(20, 20, 450, 491), (480, 100, 490, 112)])
			failures = inspect_playground_frame(path, 8)
			self.assertTrue(any("disconnected visible components" in line for line in failures))

	def test_rejects_missing_alpha_channel(self) -> None:
		with tempfile.TemporaryDirectory() as raw:
			path = Path(raw) / "opaque_rgb.png"
			Image.new("RGB", (512, 512), (240, 120, 220)).save(path)
			failures = inspect_playground_frame(path, 8)
			self.assertTrue(any("missing alpha channel" in line for line in failures))

	def test_rejects_wrong_canvas_size(self) -> None:
		with tempfile.TemporaryDirectory() as raw:
			path = Path(raw) / "wrong_size.png"
			Image.new("RGBA", (256, 512), (240, 120, 220, 255)).save(path)
			failures = inspect_playground_frame(path, 8)
			self.assertTrue(any("expected 512x512" in line for line in failures))


if __name__ == "__main__":
	unittest.main()
