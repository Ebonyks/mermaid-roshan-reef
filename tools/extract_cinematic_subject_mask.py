#!/usr/bin/env python3
"""Extract an audit-only subject mask by comparing a frame with a clean plate.

This tool does not create or alter delivery pixels. It produces evidence used
to measure a regenerated subject against a position-only guide. Outputs must
remain under an ignored ``build`` directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def parse_roi(value: str) -> tuple[float, float, float, float]:
    try:
        result = tuple(float(component) for component in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected LEFT,TOP,RIGHT,BOTTOM") from error
    if len(result) != 4:
        raise argparse.ArgumentTypeError("expected LEFT,TOP,RIGHT,BOTTOM")
    left, top, right, bottom = result
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise argparse.ArgumentTypeError(
            "ROI coordinates must be normalized and ordered in [0, 1]"
        )
    return left, top, right, bottom


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_largest_component(
    candidate: Path,
    background: Path,
    roi: tuple[float, float, float, float],
    threshold: int,
    opening_iterations: int,
    closing_iterations: int,
    minimum_area: int,
    segmentation: str = "background_delta",
) -> tuple[np.ndarray, dict[str, object]]:
    with Image.open(candidate).convert("RGB") as candidate_image:
        candidate_pixels = np.asarray(candidate_image, dtype=np.int16)
        size = candidate_image.size
    with Image.open(background).convert("RGB") as background_image:
        background_size = background_image.size
        if segmentation == "background_delta" and background_size != size:
            raise ValueError(
                f"candidate size {size} does not match clean-plate size "
                f"{background_size}"
            )
        background_pixels = (
            np.asarray(background_image, dtype=np.int16)
            if segmentation == "background_delta"
            else None
        )

    width, height = size
    left = round(roi[0] * width)
    top = round(roi[1] * height)
    right = round(roi[2] * width)
    bottom = round(roi[3] * height)
    if segmentation == "background_delta":
        assert background_pixels is not None
        changed = np.max(
            np.abs(candidate_pixels - background_pixels),
            axis=2,
        ) > threshold
    elif segmentation == "purple_outline":
        red = candidate_pixels[:, :, 0]
        green = candidate_pixels[:, :, 1]
        blue = candidate_pixels[:, :, 2]
        # The opening plane's lavender/navy edge is stable against both blue
        # sky and white clouds. This avoids a regenerated cloud touching the
        # plane and falsely extending a clean-plate-difference component.
        changed = (
            (red >= 55)
            & (blue >= 75)
            & (red > green + 8)
            & (blue > green + 12)
        )
    else:
        raise ValueError(f"unsupported segmentation mode: {segmentation}")
    roi_mask = np.zeros((height, width), dtype=bool)
    roi_mask[top:bottom, left:right] = True
    changed &= roi_mask
    if opening_iterations:
        changed = ndimage.binary_opening(
            changed,
            iterations=opening_iterations,
        )
    if closing_iterations:
        changed = ndimage.binary_closing(
            changed,
            iterations=closing_iterations,
        )

    labels, component_count = ndimage.label(changed)
    if component_count == 0:
        raise ValueError("no changed component found in ROI")
    component_sizes = np.bincount(labels.ravel())
    component_sizes[0] = 0
    component_id = int(component_sizes.argmax())
    area = int(component_sizes[component_id])
    if area < minimum_area:
        raise ValueError(
            f"largest component area {area} is below minimum {minimum_area}"
        )
    component = labels == component_id
    rows, columns = np.nonzero(component)
    bounds = (
        int(columns.min()),
        int(rows.min()),
        int(columns.max()) + 1,
        int(rows.max()) + 1,
    )
    box_left, box_top, box_right, box_bottom = bounds
    center = (
        (box_left + box_right) / (2.0 * width),
        (box_top + box_bottom) / (2.0 * height),
    )
    report: dict[str, object] = {
        "schema": "cinematic-subject-mask-v1",
        "candidate": {
            "path": str(candidate.resolve()),
            "sha256": sha256_file(candidate),
        },
        "clean_plate": {
            "path": str(background.resolve()),
            "sha256": sha256_file(background),
            "size": list(background_size),
            "used_for_segmentation": segmentation == "background_delta",
        },
        "size": [width, height],
        "roi": list(roi),
        "threshold": threshold,
        "segmentation": segmentation,
        "opening_iterations": opening_iterations,
        "closing_iterations": closing_iterations,
        "component_count": int(component_count),
        "selected_component_area": area,
        "bbox_pixels": list(bounds),
        "anchors": {
            "center": list(center),
            "bbox_left": [box_left / width, center[1]],
            "bbox_right": [box_right / width, center[1]],
            "bbox_top": [center[0], box_top / height],
            "bbox_bottom": [center[0], box_bottom / height],
        },
    }
    return component, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("clean_plate", type=Path)
    parser.add_argument("output_mask", type=Path)
    parser.add_argument(
        "--roi",
        type=parse_roi,
        default=(0.0, 0.0, 1.0, 1.0),
        help="normalized LEFT,TOP,RIGHT,BOTTOM search region",
    )
    parser.add_argument("--threshold", type=int, default=50)
    parser.add_argument(
        "--segmentation",
        choices=("background_delta", "purple_outline"),
        default="background_delta",
        help="subject evidence signal; purple_outline is tuned for the opening plane",
    )
    parser.add_argument("--opening-iterations", type=int, default=1)
    parser.add_argument("--closing-iterations", type=int, default=3)
    parser.add_argument("--minimum-area", type=int, default=256)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    for label, path in (
        ("candidate", args.candidate),
        ("clean plate", args.clean_plate),
    ):
        if not path.is_file():
            parser.error(f"{label} does not exist: {path}")
    if "build" not in {
        part.lower() for part in args.output_mask.resolve().parts
    }:
        parser.error("output mask must stay under an ignored build directory")
    if args.threshold < 0 or args.threshold > 255:
        parser.error("--threshold must be in [0, 255]")
    if args.opening_iterations < 0 or args.closing_iterations < 0:
        parser.error("morphology iterations must be nonnegative")
    if args.minimum_area < 1:
        parser.error("--minimum-area must be positive")

    try:
        component, report = extract_largest_component(
            args.candidate,
            args.clean_plate,
            args.roi,
            args.threshold,
            args.opening_iterations,
            args.closing_iterations,
            args.minimum_area,
            args.segmentation,
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))
    args.output_mask.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(component.astype(np.uint8) * 255, "L").save(
        args.output_mask,
        optimize=True,
    )
    report["mask"] = {
        "path": str(args.output_mask.resolve()),
        "sha256": sha256_file(args.output_mask),
    }
    report_path = args.report or args.output_mask.with_suffix(".json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    anchors = report["anchors"]
    print(
        "SUBJECT_MASK|"
        f"bbox={report['bbox_pixels']}|"
        f"bbox_right={anchors['bbox_right'][0]:.8f}|"
        f"mask={args.output_mask}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
