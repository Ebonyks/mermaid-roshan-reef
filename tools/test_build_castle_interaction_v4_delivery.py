#!/usr/bin/env python3
"""Self-tests for V4 delivery provenance binding."""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.build_castle_interaction_v4_delivery import audit_upstream_provenance
from tools.build_castle_native_interactions_v4 import _repository_text_sha256


class UpstreamProvenanceTests(unittest.TestCase):
    def _fixture(self, root: Path) -> dict[str, str]:
        bindings = {
            "generator": "tools/native.py",
            "spec": "tools/spec.json",
            "source_layer_manifest": "layers.json",
        }
        manifest: dict[str, str] = {}
        for key, relative in bindings.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(key, encoding="utf-8")
            manifest[key] = relative
            manifest[f"{key}_sha256"] = hashlib.sha256(
                path.read_bytes()).hexdigest()
        return manifest

    def test_accepts_exact_bound_inputs(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            self.assertEqual(
                audit_upstream_provenance(root, self._fixture(root)), [])

    def test_rejects_stale_hash(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            manifest = self._fixture(root)
            manifest["source_layer_manifest_sha256"] = "0" * 64
            errors = audit_upstream_provenance(root, manifest)
            self.assertTrue(any(
                "stale upstream provenance hash" in error
                and "source_layer_manifest_sha256" in error
                for error in errors))

    def test_accepts_repository_hash_across_checkout_line_endings(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            manifest = self._fixture(root)
            generator = root / manifest["generator"]
            generator.write_bytes(b"first line\r\nsecond line\r\n")
            manifest["generator_sha256"] = hashlib.sha256(
                b"first line\nsecond line\n").hexdigest()
            self.assertEqual(audit_upstream_provenance(root, manifest), [])

            generator.write_bytes(b"first line\r\nchanged line\r\n")
            errors = audit_upstream_provenance(root, manifest)
            self.assertTrue(any(
                "stale upstream provenance hash" in error
                and "generator_sha256" in error
                for error in errors))

    def test_native_generator_records_repository_text_hash(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "source.json"
            path.write_bytes(b'{\r\n  "value": true\r\n}\r\n')
            self.assertEqual(
                _repository_text_sha256(path),
                hashlib.sha256(b'{\n  "value": true\n}\n').hexdigest(),
            )

    def test_rejects_repository_escape(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            manifest = self._fixture(root)
            manifest["spec"] = "../outside.json"
            errors = audit_upstream_provenance(root, manifest)
            self.assertTrue(any(
                "escapes repository" in error for error in errors))

    def test_rejects_missing_binding(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            manifest = self._fixture(root)
            del manifest["generator_sha256"]
            errors = audit_upstream_provenance(root, manifest)
            self.assertTrue(any(
                "missing upstream provenance hash" in error
                for error in errors))


if __name__ == "__main__":
    unittest.main()
