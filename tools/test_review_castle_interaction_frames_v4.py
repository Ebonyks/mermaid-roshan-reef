#!/usr/bin/env python3
"""Focused tests for the repository-level Castle V4 per-frame review gate."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image


sys.path.insert(0, str(Path(__file__).resolve().parent))
import castle_interaction_frame_qa as qa  # noqa: E402
import review_castle_interaction_frames_v4 as review  # noqa: E402


def rgba(size: tuple[int, int], color: tuple[int, int, int, int]) -> Image.Image:
    return Image.new("RGBA", size, color)


def placed(image: Image.Image) -> qa.PlacedFrame:
    alpha = qa.binary_mask(image.getchannel("A"), 128)
    values = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    values[np.asarray(alpha, dtype=np.uint8) == 0] = 0
    return qa.PlacedFrame(Image.fromarray(values, mode="RGBA"), alpha)


def candidate_with_relation(
        relation: list[dict[str, object]] | None = None,
        findings: tuple[str, ...] = (),
        ) -> review.RepositoryReviewBuild:
    relation = relation or []
    candidate = review.seal_candidate({
        "schema_version": review.CANDIDATE_SCHEMA,
        "inputs": {
            "v4_manifest": {"semantic_sha256": "1" * 64},
        },
        "assets": [{
            "id": "test_asset",
            "frames": [{
                "frame_index": 0,
                "frame_review_sha256": "2" * 64,
            }],
            "required_occlusion_relation": relation,
        }],
        "blocking_findings": list(findings),
    })
    return review.RepositoryReviewBuild(candidate, {}, findings)


def exact_ledger(build: review.RepositoryReviewBuild) -> dict[str, object]:
    asset = build.candidate["assets"][0]
    return {
        "schema_version": review.APPROVAL_SCHEMA,
        "candidate_payload_sha256": build.candidate[
            "candidate_payload_sha256"],
        "manifest_semantic_sha256": build.candidate[
            "inputs"]["v4_manifest"]["semantic_sha256"],
        "reviewer": "Human visual review",
        "assets": {
            asset["id"]: {
                "frame_review_sha256": {
                    str(frame["frame_index"]): frame["frame_review_sha256"]
                    for frame in asset["frames"]
                },
                "occlusion_relation": asset["required_occlusion_relation"],
            },
        },
    }


class CastleInteractionRepositoryReviewTests(unittest.TestCase):
    def test_json_semantic_hash_ignores_formatting_and_line_endings(self) -> None:
        left = json.loads('{\r\n  "b": 2,\r\n  "a": [1, 3]\r\n}')
        right = json.loads('{"a":[1,3],"b":2}\n')
        self.assertEqual(
            review.semantic_json_sha256(left),
            review.semantic_json_sha256(right))
        right["b"] = 4
        self.assertNotEqual(
            review.semantic_json_sha256(left),
            review.semantic_json_sha256(right))

    def test_text_semantic_hash_normalizes_line_endings_only(self) -> None:
        self.assertEqual(
            review.normalized_text_sha256("one\r\ntwo\r\n"),
            review.normalized_text_sha256("one\ntwo\n"))
        self.assertNotEqual(
            review.normalized_text_sha256("one\ntwo\n"),
            review.normalized_text_sha256("one\nthree\n"))

    def test_contact_evidence_ignores_encoding_but_rejects_pixel_drift(self) -> None:
        source = rgba((8, 6), (80, 180, 220, 255))
        fast = BytesIO()
        compact = BytesIO()
        source.save(fast, format="PNG", compress_level=0)
        source.save(compact, format="PNG", compress_level=9, optimize=True)
        self.assertNotEqual(fast.getvalue(), compact.getvalue())
        fast_image = Image.open(BytesIO(fast.getvalue())).convert("RGBA")
        compact_image = Image.open(BytesIO(compact.getvalue())).convert("RGBA")
        fast_evidence = review.contact_sheet_evidence("review.png", fast_image)
        compact_evidence = review.contact_sheet_evidence(
            "review.png", compact_image)
        self.assertEqual(fast_evidence, compact_evidence)
        self.assertNotIn("file_sha256", fast_evidence)
        changed = compact_image.copy()
        changed.putpixel((3, 2), (81, 180, 220, 255))
        self.assertNotEqual(
            fast_evidence["pixel_sha256"],
            review.contact_sheet_evidence(
                "review.png", changed)["pixel_sha256"])

    def test_shipping_manifest_has_all_twelve_v4_assets(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads(
            (root / review.V4_MANIFEST_RELATIVE).read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["assets"]), review.EXPECTED_V4_ASSET_COUNT)
        self.assertEqual(len({asset["id"] for asset in manifest["assets"]}), 12)

    def test_static_card_placement_uses_alpha_128(self) -> None:
        image = rgba((2, 1), (90, 160, 220, 0))
        image.putpixel((0, 0), (90, 160, 220, 127))
        image.putpixel((1, 0), (90, 160, 220, 128))
        placed_rgba, alpha = review.place_static_card_rgba(
            image, (3.0, 2.0), room_size=(8, 6))
        self.assertEqual(alpha.getbbox(), (4, 2, 5, 3))
        self.assertEqual(placed_rgba.getpixel((3, 2)), (0, 0, 0, 0))
        self.assertEqual(placed_rgba.getpixel((4, 2))[3], 128)

    def test_runtime_depths_preserve_existing_item_and_default_new_item(self) -> None:
        runtime = '''
const MIDGROUND_Z := 2.0
const FOREGROUND_Z := 4.0
const ROOM_ITEMS := {
\t"pool": [
\t\t{"id": "existing", "name": "Existing",
\t\t\t"z": MIDGROUND_Z + 0.02},
\t],
}
'''
        fixture = '''
return {
    "z": float(entry.get("z", 0.82)),
}
'''
        depths = review.runtime_asset_depths(runtime, fixture, [
            {"id": "existing_asset", "room": "pool", "instances": ["existing"]},
            {"id": "new_asset", "room": "pool", "instances": ["new"]},
        ])
        self.assertEqual(depths["existing_asset"], (2.02, "ROOM_ITEMS.pool:existing"))
        self.assertEqual(depths["new_asset"], (
            0.82, "CastleFixtureRigs native default"))

    def test_reconstructs_underlay_from_manifest_runtime_tiles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tile_dir = root / "tiles"
            tile_dir.mkdir()
            records = []
            for name, color in (
                    ("left.png", (20, 90, 130, 255)),
                    ("right.png", (220, 170, 150, 255))):
                path = tile_dir / name
                rgba((2, 2), color).save(path)
                records.append({
                    "path": f"tiles/{name}",
                    "sha256": review.sha256_file(path),
                })
            underlay, evidence = review.reconstruct_logical_underlay(
                root, "test_room", {
                    "route": "generated_full_frame_pixel_ownership_tiles",
                    "grid": [2, 1],
                    "tile_dimensions": [2, 2],
                    "native_canvas_size": [4, 2],
                    "logical_canvas_size": [1024, 576],
                    "tiles": records,
                })
            self.assertEqual(underlay.size, review.LOGICAL_ROOM_SIZE)
            self.assertEqual(underlay.getpixel((10, 10))[:3], (20, 90, 130))
            self.assertEqual(underlay.getpixel((1010, 10))[:3], (220, 170, 150))
            self.assertEqual(evidence["reconstruction"],
                             "per_tile_lanczos_to_runtime_logical_cells")

    def test_depth_aware_composite_respects_static_card_z(self) -> None:
        size = (6, 4)
        approved = rgba(size, (50, 100, 80, 255))
        underlay = rgba(size, (20, 40, 100, 255))
        ownership = Image.new("L", size, 0)
        ownership.putpixel((2, 1), 255)
        primary_image = rgba(size, (0, 0, 0, 0))
        primary_image.putpixel((2, 1), (230, 40, 180, 255))
        primary = placed(primary_image)
        card_image = rgba(size, (0, 0, 0, 0))
        card_image.putpixel((2, 1), (245, 210, 40, 255))
        card = review.StaticCard(
            room="room", card_id="card", layer="mid", path="card.png",
            position=(0.0, 0.0), z=2.0, rgba=card_image,
            alpha_mask=qa.binary_mask(card_image.getchannel("A")),
            file_sha256="a" * 64, alpha_pixel_sha256="b" * 64)
        behind = review.compose_depth_aware_frame(
            approved, underlay, ownership, primary, [card], asset_z=3.0)
        ahead = review.compose_depth_aware_frame(
            approved, underlay, ownership, primary, [card], asset_z=1.0)
        self.assertEqual(behind.getpixel((0, 0)), (20, 40, 100, 255))
        self.assertEqual(ahead.getpixel((0, 0)), (20, 40, 100, 255))
        self.assertEqual(behind.getpixel((2, 1)), (230, 40, 180, 255))
        self.assertEqual(ahead.getpixel((2, 1)), (245, 210, 40, 255))

    def test_static_overlap_reports_signed_delta_and_exact_mask(self) -> None:
        size = (7, 5)
        primary = Image.new("L", size, 0)
        primary.putpixel((3, 2), 255)
        card_rgba = rgba(size, (0, 0, 0, 0))
        card_rgba.putpixel((3, 2), (220, 180, 100, 255))
        card = review.StaticCard(
            room="room", card_id="front", layer="front", path="front.png",
            position=(0.0, 0.0), z=4.0, rgba=card_rgba,
            alpha_mask=qa.binary_mask(card_rgba.getchannel("A")),
            file_sha256="a" * 64, alpha_pixel_sha256="b" * 64)
        relations, masks = review.measure_frame_occlusions(
            primary, [card], asset_z=0.82)
        self.assertEqual(len(relations), 1)
        self.assertEqual(relations[0]["signed_z_delta"], -3.18)
        self.assertEqual(relations[0]["relation"], "card_in_front_of_asset")
        self.assertEqual(relations[0]["overlap_pixels"], 1)
        self.assertEqual(masks[0].getbbox(), (3, 2, 4, 3))

    def test_secondary_water_overlay_cannot_satisfy_primary_coverage(self) -> None:
        size = (8, 6)
        approved = rgba(size, (180, 130, 100, 255))
        underlay = rgba(size, (20, 90, 130, 255))
        ownership = Image.new("L", size, 0)
        for y in range(1, 5):
            for x in range(2, 6):
                ownership.putpixel((x, y), 255)
        primary_image = rgba(size, (0, 0, 0, 0))
        for y in range(1, 5):
            for x in range(2, 5):
                primary_image.putpixel((x, y), (80, 180, 220, 255))
        water = rgba(size, (0, 0, 0, 0))
        for y in range(1, 5):
            water.putpixel((5, y), (20, 180, 255, 255))
        result = qa.compute_asset_frame_qa(
            approved,
            underlay,
            ownership,
            [placed(primary_image)],
            healing_mask=ownership,
            secondary_overlays_by_frame=[[water]],
        )[0]
        self.assertEqual(result.record.exposed_heal_pixels, 4)
        self.assertEqual(result.primary_alpha_mask.getpixel((5, 2)), 0)
        self.assertEqual(result.composite.getpixel((5, 2)), (20, 180, 255, 255))

    def test_duplicate_source_component_is_nonwaivable(self) -> None:
        size = (8, 6)
        approved = rgba(size, (180, 130, 100, 255))
        underlay = approved.copy()
        ownership = Image.new("L", size, 0)
        for y in range(1, 5):
            for x in range(2, 6):
                ownership.putpixel((x, y), 255)
        empty = placed(rgba(size, (0, 0, 0, 0)))
        result = qa.compute_asset_frame_qa(
            approved, underlay, ownership, [empty], healing_mask=ownership)[0]
        issues = review.nonwaivable_frame_issues("asset", result, [])
        self.assertTrue(any("exposed source duplicate" in issue for issue in issues))

    def test_coplanar_static_overlap_is_nonwaivable(self) -> None:
        size = (5, 4)
        ownership = Image.new("L", size, 255)
        result = qa.compute_asset_frame_qa(
            rgba(size, (180, 130, 100, 255)),
            rgba(size, (20, 90, 130, 255)),
            ownership,
            [placed(rgba(size, (80, 180, 220, 255)))],
            healing_mask=ownership,
        )[0]
        relation = [{
            "card_path": "mid.png",
            "signed_z_delta": 0.005,
        }]
        issues = review.nonwaivable_frame_issues("asset", result, relation)
        self.assertTrue(any("minimum absolute delta" in issue for issue in issues))

    def test_missing_approval_ledger_blocks_candidate(self) -> None:
        errors = review.validate_approval_ledger(candidate_with_relation(), None)
        self.assertTrue(any("missing approval ledger" in error for error in errors))

    def test_exact_review_hashes_and_explicit_occlusion_relation_pass(self) -> None:
        relation = [{
            "frame_index": 0,
            "card_id": "front",
            "card_path": "front.png",
            "layer": "front",
            "card_z": 4.0,
            "asset_z": 0.82,
            "signed_z_delta": -3.18,
            "relation": "card_in_front_of_asset",
            "overlap_pixels": 8,
            "overlap_pixel_sha256": "3" * 64,
        }]
        build = candidate_with_relation(relation)
        ledger = exact_ledger(build)
        self.assertEqual(review.validate_approval_ledger(build, ledger), [])
        ledger["assets"]["test_asset"]["occlusion_relation"] = []  # type: ignore[index]
        errors = review.validate_approval_ledger(build, ledger)
        self.assertTrue(any("occlusion_relation" in error for error in errors))

    def test_stale_candidate_or_frame_hash_blocks(self) -> None:
        build = candidate_with_relation()
        ledger = exact_ledger(build)
        ledger["candidate_payload_sha256"] = "0" * 64
        ledger["assets"]["test_asset"]["frame_review_sha256"]["0"] = "9" * 64  # type: ignore[index]
        errors = review.validate_approval_ledger(build, ledger)
        self.assertTrue(any("candidate_payload_sha256" in error for error in errors))
        self.assertTrue(any("per-frame review hashes" in error for error in errors))

    def test_contact_sheet_bytes_are_deterministic(self) -> None:
        size = (8, 6)
        ownership = Image.new("L", size, 255)
        result = qa.compute_asset_frame_qa(
            rgba(size, (180, 130, 100, 255)),
            rgba(size, (20, 90, 130, 255)),
            ownership,
            [placed(rgba(size, (80, 180, 220, 255)))],
            healing_mask=ownership,
        )[0]
        record = {"id": "asset", "room": "room", "asset_z": 0.82}
        first = review.png_bytes(review.render_contact_sheet(
            record, [result], [[]]))
        second = review.png_bytes(review.render_contact_sheet(
            record, [result], [[]]))
        self.assertEqual(first, second)

    def test_plain_contact_sheet_omits_diagnostic_tint(self) -> None:
        size = (8, 6)
        ownership = Image.new("L", size, 255)
        result = qa.compute_asset_frame_qa(
            rgba(size, (180, 130, 100, 255)),
            rgba(size, (20, 90, 130, 255)),
            ownership,
            [placed(rgba(size, (80, 180, 220, 255)))],
            healing_mask=ownership,
        )[0]
        record = {"id": "asset", "room": "room", "asset_z": 0.82}
        diagnostic = review.render_contact_sheet(record, [result], [[]])
        plain = review.render_contact_sheet(
            record, [result], [[]], show_diagnostics=False)
        self.assertNotEqual(
            qa.raw_pixel_sha256(diagnostic), qa.raw_pixel_sha256(plain))


if __name__ == "__main__":
    unittest.main()
