#!/usr/bin/env python3
"""Focused regression tests for the native castle ownership gate."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_castle_native_interactions as audit  # noqa: E402


class NativeInteractionAuditTests(unittest.TestCase):
    def test_unfiltered_legacy_manifest_exposes_v3_addition(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        fixture = (
            'const MANIFEST_PATH := '
            '"res://assets/flats/castle/interactions_v3/'
            'castle_interactions_v3.json"\n'
        )
        self.assertEqual(
            audit.active_v3_additions(root, fixture, []),
            ["assets/flats/castle/interactions_v3/castle_interactions_v3.json"],
        )

    def test_even_filtered_v3_runtime_route_is_rejected(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        fixture = """
const V2_BASE_MANIFEST_PATH := \\
    "res://assets/flats/castle/interactions_v3/castle_interactions_v3.json"
const V2_BASE_PACK := "v2_base"
func load_entry(pack):
    if pack == "v3_addition":
        rejected += 1
        continue
    if pack != V2_BASE_PACK:
        continue
"""
        self.assertTrue(audit.active_v3_additions(root, fixture, []))

    def test_missing_retired_v3_manifest_is_healthy_without_route(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        errors: list[str] = []
        self.assertEqual(
            audit.active_v3_additions(Path(temporary.name), "", errors), [])
        self.assertEqual(errors, [])

    def test_duplicate_pixel_measurement_is_not_review_metadata(self) -> None:
        rest = Image.new("RGBA", (8, 8), (80, 170, 220, 255))
        mask = Image.new("L", (8, 8), 255)
        duplicate = rest.copy()
        healed = Image.new("RGBA", (8, 8), (210, 180, 150, 255))
        self.assertEqual(audit.match_ratio(rest, duplicate, mask), 1.0)
        self.assertEqual(audit.match_ratio(rest, healed, mask), 0.0)
        self.assertEqual(audit.change_ratio(rest, duplicate, mask), 0.0)
        self.assertEqual(audit.change_ratio(rest, healed, mask), 1.0)

    def test_one_source_rect_must_be_inside_room(self) -> None:
        self.assertEqual(audit.source_rect([10, 20, 30, 40], "kitchen"),
                         (10, 20, 30, 40))
        self.assertIsNone(audit.source_rect([1000, 20, 30, 40], "kitchen"))
        self.assertIsNone(audit.source_rect([10, 20, -1, 40], "kitchen"))

    def test_one_source_rect_cannot_authorize_two_instances(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        errors: list[str] = []
        keys = audit.audit_asset(
            Path(temporary.name),
            {"id": "bad", "room": "kitchen", "instances": ["a", "b"]},
            {}, {}, {}, errors,
        )
        self.assertEqual(keys, set())
        self.assertIn(
            "asset bad: V4 source ownership requires exactly one instance",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
