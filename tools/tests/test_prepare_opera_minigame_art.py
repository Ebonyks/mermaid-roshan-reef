from __future__ import annotations

import unittest

from tools import prepare_opera_minigame_art as gate


class OperaMinigameArtCheckTests(unittest.TestCase):
	def test_generated_text_artifacts_tolerate_crlf_checkout(self) -> None:
		for name in ("PROVENANCE.json", "REVIEW.md"):
			with self.subTest(name=name):
				path = gate.SOURCE_DIR / name
				self.assertTrue(gate._check_bytes_match(
					path,
					b"first line\r\nsecond line\r\n",
					b"first line\nsecond line\n",
				))

	def test_generated_text_artifacts_reject_content_drift(self) -> None:
		path = gate.SOURCE_DIR / "REVIEW.md"
		self.assertFalse(gate._check_bytes_match(
			path,
			b"accepted\r\nowner review pending\r\n",
			b"accepted\nowner review complete\n",
		))

	def test_png_artifacts_remain_byte_exact(self) -> None:
		path = gate.SOURCE_DIR / "contact.png"
		self.assertFalse(gate._check_bytes_match(
			path,
			b"\x89PNG\r\npayload",
			b"\x89PNG\npayload",
		))


if __name__ == "__main__":
	unittest.main()
