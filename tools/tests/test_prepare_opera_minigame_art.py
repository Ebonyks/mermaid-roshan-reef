from __future__ import annotations

import io
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from PIL.PngImagePlugin import PngInfo

from tools import prepare_opera_minigame_art as gate


class OperaMinigameArtCheckTests(unittest.TestCase):
	def test_declared_text_source_hash_is_checkout_newline_stable(self) -> None:
		lf = b'{\n  "schema": 1\n}\n'
		crlf = lf.replace(b"\n", b"\r\n")
		with patch.object(Path, "read_bytes", return_value=lf):
			lf_hash = gate._sha256_file(gate.CANDY_GENERATION)
		with patch.object(Path, "read_bytes", return_value=crlf):
			crlf_hash = gate._sha256_file(gate.CANDY_GENERATION)
		self.assertEqual(lf_hash, crlf_hash)
		with patch.object(Path, "read_bytes", return_value=lf.replace(b"1", b"2")):
			changed_hash = gate._sha256_file(gate.CANDY_GENERATION)
		self.assertNotEqual(lf_hash, changed_hash)

	def test_binary_source_hash_remains_byte_exact(self) -> None:
		lf = b"binary\nbytes\x00"
		crlf = lf.replace(b"\n", b"\r\n")
		with patch.object(Path, "read_bytes", return_value=lf):
			lf_hash = gate._sha256_file(gate.CANDY_FILL_ALPHA)
		with patch.object(Path, "read_bytes", return_value=crlf):
			crlf_hash = gate._sha256_file(gate.CANDY_FILL_ALPHA)
		self.assertNotEqual(lf_hash, crlf_hash)

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

	@staticmethod
	def _png_bytes(color: tuple[int, int, int, int], compress_level: int) -> bytes:
		output = io.BytesIO()
		Image.new("RGBA", (5, 3), color).save(
			output,
			format="PNG",
			compress_level=compress_level,
			optimize=False,
		)
		return output.getvalue()

	def test_png_artifacts_accept_reencoded_identical_rgba(self) -> None:
		path = gate.SOURCE_DIR / "contact.png"
		checked_in = self._png_bytes((12, 34, 56, 200), 1)
		generated = self._png_bytes((12, 34, 56, 200), 9)
		self.assertNotEqual(checked_in, generated)
		self.assertTrue(gate._check_bytes_match(path, checked_in, generated))

	def test_png_artifacts_reject_real_pixel_drift_and_invalid_payloads(self) -> None:
		path = gate.SOURCE_DIR / "contact.png"
		checked_in = self._png_bytes((12, 34, 56, 200), 1)
		changed = self._png_bytes((13, 34, 56, 200), 9)
		self.assertFalse(gate._check_bytes_match(path, checked_in, changed))
		self.assertFalse(gate._check_bytes_match(path, checked_in, b"not a png"))

	@staticmethod
	def _append_crc_valid_idat_junk(payload: bytes, junk: bytes) -> bytes:
		offset = 8
		while offset < len(payload):
			length = struct.unpack(">I", payload[offset:offset + 4])[0]
			chunk_type = payload[offset + 4:offset + 8]
			chunk_end = offset + 12 + length
			if chunk_type == b"IDAT":
				data = payload[offset + 8:offset + 8 + length] + junk
				crc = zlib.crc32(chunk_type)
				crc = zlib.crc32(data, crc) & 0xFFFFFFFF
				chunk = struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)
				return payload[:offset] + chunk + payload[chunk_end:]
			offset = chunk_end
		raise AssertionError("fixture PNG has no IDAT chunk")

	def test_png_artifacts_reject_crc_valid_trailing_idat_payload(self) -> None:
		path = gate.SOURCE_DIR / "contact.png"
		checked_in = self._png_bytes((12, 34, 56, 200), 1)
		with_junk = self._append_crc_valid_idat_junk(checked_in, b"hidden payload")
		self.assertFalse(gate._check_bytes_match(path, checked_in, with_junk))

	def test_png_artifacts_report_corrupt_crc_valid_idat_as_mismatch(self) -> None:
		path = gate.SOURCE_DIR / "contact.png"
		checked_in = self._png_bytes((12, 34, 56, 200), 1)
		offset = checked_in.index(b"IDAT") - 4
		length = struct.unpack(">I", checked_in[offset:offset + 4])[0]
		chunk_end = offset + 12 + length
		data = b"X" * length
		crc = zlib.crc32(b"IDAT")
		crc = zlib.crc32(data, crc) & 0xFFFFFFFF
		chunk = struct.pack(">I", length) + b"IDAT" + data + struct.pack(">I", crc)
		corrupt = checked_in[:offset] + chunk + checked_in[chunk_end:]
		self.assertFalse(gate._check_bytes_match(path, checked_in, corrupt))

	def test_png_artifacts_reject_mode_or_metadata_drift(self) -> None:
		path = gate.SOURCE_DIR / "contact.png"
		checked_in = self._png_bytes((12, 34, 56, 255), 1)
		rgb_output = io.BytesIO()
		Image.new("RGB", (5, 3), (12, 34, 56)).save(rgb_output, format="PNG")
		self.assertFalse(gate._check_bytes_match(path, checked_in, rgb_output.getvalue()))
		metadata = PngInfo()
		metadata.add_text("unexpected", "drift")
		metadata_output = io.BytesIO()
		Image.new("RGBA", (5, 3), (12, 34, 56, 255)).save(
			metadata_output,
			format="PNG",
			pnginfo=metadata,
		)
		self.assertFalse(gate._check_bytes_match(
			path,
			checked_in,
			metadata_output.getvalue(),
		))

	def test_check_mode_provenance_keeps_accepted_delivery_bytes(self) -> None:
		checked_in = self._png_bytes((12, 34, 56, 200), 1)
		generated = self._png_bytes((12, 34, 56, 200), 9)
		pixel_drift = self._png_bytes((13, 34, 56, 200), 9)
		with tempfile.TemporaryDirectory() as temp_dir:
			path = Path(temp_dir) / "contact.png"
			path.write_bytes(checked_in)
			self.assertEqual(
				gate._delivery_bytes_for_provenance(path, generated, True),
				checked_in,
			)
			self.assertEqual(
				gate._delivery_bytes_for_provenance(path, generated, False),
				generated,
			)
			self.assertEqual(
				gate._delivery_bytes_for_provenance(path, pixel_drift, True),
				pixel_drift,
			)
			self.assertEqual(
				gate._delivery_bytes_for_provenance(Path(temp_dir) / "missing.png", generated, True),
				generated,
			)


if __name__ == "__main__":
	unittest.main()
