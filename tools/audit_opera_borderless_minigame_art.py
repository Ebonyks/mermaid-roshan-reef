#!/usr/bin/env python3
"""Validate the generated borderless Opera minigame subjects and evidence."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
LICENSES = ROOT / "ASSET_LICENSES.md"
PACKAGES = {
    "racer_pitstop_kart": {
        "source_dir": "assets_src/imagegen/opera_borderless_pitstop_2026-08-10",
        "native": (
            "native/racer_pitstop_kart_chroma_native.png",
            "1943f7ad22c69a66c7ea155e8c6422941b39f8e318dc0bf17ddfcee4ee3281e8",
        ),
        "alpha": (
            "racer_pitstop_kart_alpha_native.png",
            "dfb56ac964fe91feadbeddbefa76bea38924291b819ddc0fa070a130dcdb6e84",
        ),
        "runtime": (
            "assets/opera/worlds/widgets/widget_crank_racer_kart.png",
            "59ea76d8be40b604cbf3691e9c9508287334ddf6cf0f81fea08c7f68fd22fe8c",
        ),
        "bbox": (14, 93, 483, 372),
    },
    "doctor_starfish_patient": {
        "source_dir": "assets_src/imagegen/opera_borderless_doctor_2026-08-10",
        "native": (
            "native/doctor_starfish_patient_chroma_native.png",
            "b563608b0f9152bd2174ea2cb7b0c4e9fc408680c993137c98db0c148c70a403",
        ),
        "alpha": (
            "doctor_starfish_patient_alpha_native.png",
            "dcbe51506d132c4796e4e1c32936d5bb9a5f5e76aae2827647b2cec66879003a",
        ),
        "runtime": (
            "assets/opera/worlds/widgets/widget_crank_doctor_patient.png",
            "ecf354fd812decbae250078cc2dc7bce8b8bb5c403afe5016bdabedbe0c8ffc9",
        ),
        "bbox": (46, 24, 466, 452),
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _component_count(mask: list[list[bool]]) -> int:
    height = len(mask)
    width = len(mask[0]) if height else 0
    count = 0
    for y in range(height):
        for x in range(width):
            if not mask[y][x]:
                continue
            count += 1
            mask[y][x] = False
            queue: deque[tuple[int, int]] = deque([(x, y)])
            while queue:
                at_x, at_y = queue.popleft()
                for next_x, next_y in (
                    (at_x - 1, at_y),
                    (at_x + 1, at_y),
                    (at_x, at_y - 1),
                    (at_x, at_y + 1),
                ):
                    if (
                        0 <= next_x < width
                        and 0 <= next_y < height
                        and mask[next_y][next_x]
                    ):
                        mask[next_y][next_x] = False
                        queue.append((next_x, next_y))
    return count


def main() -> int:
    failures: list[str] = []
    license_text = LICENSES.read_text(encoding="utf-8")
    for label, record in PACKAGES.items():
        source_dir = ROOT / str(record["source_dir"])
        for evidence in ("PROMPT.md", "REVIEW.md", "PROVENANCE.json"):
            if not (source_dir / evidence).is_file():
                failures.append(f"{label}: missing {evidence}")

        native_rel, native_hash = record["native"]
        alpha_rel, alpha_hash = record["alpha"]
        runtime_rel, runtime_hash = record["runtime"]
        paths = (
            (source_dir / native_rel, native_hash),
            (source_dir / alpha_rel, alpha_hash),
            (ROOT / runtime_rel, runtime_hash),
        )
        for path, expected_hash in paths:
            if not path.is_file():
                failures.append(f"{label}: missing {path.relative_to(ROOT)}")
                continue
            actual_hash = _sha256(path)
            if actual_hash != expected_hash:
                failures.append(
                    f"{label}: stale hash for {path.relative_to(ROOT)} "
                    f"({actual_hash} != {expected_hash})"
                )
            normalized = str(path.relative_to(ROOT)).replace("\\", "/")
            if normalized not in license_text:
                failures.append(f"{label}: missing ASSET_LICENSES entry for {normalized}")

        runtime_path = ROOT / runtime_rel
        if not runtime_path.is_file():
            continue
        image = Image.open(runtime_path).convert("RGBA")
        if image.size != (512, 512):
            failures.append(f"{label}: runtime dimensions are {image.size}, expected 512x512")
        pixels = image.load()
        visible: list[tuple[int, int]] = []
        mask: list[list[bool]] = [[False] * image.width for _ in range(image.height)]
        green_spill = 0
        for y in range(image.height):
            for x in range(image.width):
                red, green, blue, alpha = pixels[x, y]
                if alpha > 12:
                    visible.append((x, y))
                    if green > 200 and red < 80 and blue < 100:
                        green_spill += 1
                if alpha > 32:
                    mask[y][x] = True
        if not visible:
            failures.append(f"{label}: runtime sprite is fully transparent")
            continue
        xs = [point[0] for point in visible]
        ys = [point[1] for point in visible]
        bbox = (min(xs), min(ys), max(xs), max(ys))
        if bbox != tuple(record["bbox"]):
            failures.append(f"{label}: alpha bbox {bbox} != {record['bbox']}")
        if min(bbox[0], bbox[1], 511 - bbox[2], 511 - bbox[3]) < 12:
            failures.append(f"{label}: unsafe alpha gutter {bbox}")
        components = _component_count(mask)
        if components != 1:
            failures.append(f"{label}: expected one connected subject, found {components}")
        if green_spill:
            failures.append(f"{label}: {green_spill} visible chroma pixels")

        provenance = json.loads((source_dir / "PROVENANCE.json").read_text(encoding="utf-8"))
        qa = provenance.get("qa_summary", {})
        if qa.get("codex_visual_review") != "accepted":
            failures.append(f"{label}: Codex visual review is not accepted")
        if qa.get("owner_human_review") != "pending":
            failures.append(f"{label}: owner review must remain truthful/pending")

    if failures:
        print("OPERA_BORDERLESS_ART|result: FAIL")
        for failure in failures:
            print(f"OPERA_BORDERLESS_ART|FAIL|{failure}")
        return 1
    print(
        "OPERA_BORDERLESS_ART|result: ALL OK "
        "(2 subjects, exact hashes, connected alpha, no chroma spill)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

