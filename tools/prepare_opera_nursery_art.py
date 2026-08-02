#!/usr/bin/env python3
"""Prepare the generated Pearl Opera nursery art for runtime use.

The native chroma and alpha masters stay untouched under ``assets_src``.
This script only makes deterministic, lossless-alpha runtime derivatives:

* 512x512 Roshan and Faron actor cards; and
* three 320x320 baby cards split from the accepted three-lane sheet.

Run from the repository root::

    python tools/prepare_opera_nursery_art.py
    python tools/prepare_opera_nursery_art.py --check-only
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/concepts/opera_nursery_2026-08-01"
ACTOR_OUTPUT = ROOT / "assets/opera/worlds/actors"
BABY_OUTPUT = ROOT / "assets/opera/worlds/nursery"

ACTORS = {
    "roshan_nursery.png": SOURCE / "roshan_nursery_nurse_alpha.png",
    "faron_nursery.png": SOURCE / "faron_nursery_nurse_alpha.png",
}
BABIES = [BABY_OUTPUT / f"baby_{index}.png" for index in range(3)]


def _fit(source: Image.Image, size: tuple[int, int], margin: int) -> Image.Image:
    image = source.convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("alpha source contains no visible subject")
    subject = image.crop(bounds)
    max_width = size[0] - margin * 2
    max_height = size[1] - margin * 2
    scale = min(max_width / subject.width, max_height / subject.height)
    fitted = subject.resize(
        (max(1, round(subject.width * scale)), max(1, round(subject.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (size[0] - fitted.width) // 2
    y = size[1] - fitted.height - margin
    canvas.alpha_composite(fitted, (x, y))
    return canvas


def _prepare() -> None:
    ACTOR_OUTPUT.mkdir(parents=True, exist_ok=True)
    BABY_OUTPUT.mkdir(parents=True, exist_ok=True)
    for output_name, source_path in ACTORS.items():
        with Image.open(source_path) as source:
            output = ACTOR_OUTPUT / output_name
            _fit(source, (512, 512), 12).save(output, optimize=True)
            print(f"prepared {output.relative_to(ROOT)}")

    with Image.open(SOURCE / "nursery_baby_trio_alpha.png") as sheet_source:
        sheet = sheet_source.convert("RGBA")
    for index, output in enumerate(BABIES):
        x0 = round(index * sheet.width / 3.0)
        x1 = round((index + 1) * sheet.width / 3.0)
        cell = sheet.crop((x0, 0, x1, sheet.height))
        _fit(cell, (320, 320), 10).save(output, optimize=True)
        print(f"prepared {output.relative_to(ROOT)}")


def _validate(path: Path, expected_size: tuple[int, int]) -> None:
    if not path.exists():
        raise RuntimeError(f"missing runtime nursery asset: {path.relative_to(ROOT)}")
    with Image.open(path) as loaded:
        image = loaded.convert("RGBA")
    if image.size != expected_size:
        raise RuntimeError(
            f"wrong size for {path.relative_to(ROOT)}: {image.size}, expected {expected_size}"
        )
    alpha = image.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError(f"empty alpha in {path.relative_to(ROOT)}")
    corners = [alpha.getpixel((0, 0)), alpha.getpixel((image.width - 1, 0)),
               alpha.getpixel((0, image.height - 1)), alpha.getpixel((image.width - 1, image.height - 1))]
    if any(value != 0 for value in corners):
        raise RuntimeError(f"opaque corner in {path.relative_to(ROOT)}")
    rgba_bytes = image.tobytes()
    visible = sum(1 for offset in range(3, len(rgba_bytes), 4) if rgba_bytes[offset] > 12)
    coverage = visible / float(image.width * image.height)
    if coverage < 0.12 or coverage > 0.82:
        raise RuntimeError(
            f"implausible subject coverage in {path.relative_to(ROOT)}: {coverage:.3f}"
        )
    key_residue = 0
    for offset in range(0, len(rgba_bytes), 4):
        red = rgba_bytes[offset]
        green = rgba_bytes[offset + 1]
        blue = rgba_bytes[offset + 2]
        opacity = rgba_bytes[offset + 3]
        if opacity > 24 and green > 210 and green > red * 1.65 and green > blue * 1.65:
            key_residue += 1
    if key_residue > image.width * image.height * 0.001:
        raise RuntimeError(
            f"possible chroma residue in {path.relative_to(ROOT)}: {key_residue} pixels"
        )
    print(
        f"OK {path.relative_to(ROOT)} size={image.width}x{image.height} "
        f"coverage={coverage:.3f} key_residue={key_residue}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        _prepare()
    for output_name in ACTORS:
        _validate(ACTOR_OUTPUT / output_name, (512, 512))
    for output in BABIES:
        _validate(output, (320, 320))


if __name__ == "__main__":
    main()
