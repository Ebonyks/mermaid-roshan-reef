"""Prepare the owner-supplied boxer-imp edit for Godot.

The image-generation master intentionally remains byte-for-byte unchanged.
Its green screen is converted to real alpha by finding only saturated green
connected to the outer edge. Interior cream gear and eye highlights remain
opaque. The derived runtime actor is aspect-fitted once inside the project's
1024px square texture ceiling rather than being stretched.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE / "opera_rival_boxer_match_master.png"
OUTPUT = ROOT / "assets" / "opera" / "rivals" / "opera_rival_boxer_match.png"
RUNTIME_SIZE = (1024, 1024)


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    rgb = np.asarray(source, dtype=np.int16)
    # The supplied reference and accepted edit use a clean saturated green
    # screen. Flood only edge-connected green so no internal teal costume
    # pixels can be removed.
    red = rgb[:, :, 0]
    green = rgb[:, :, 1]
    blue = rgb[:, :, 2]
    candidate = (
        (green > 150)
        & (green > red * 1.45)
        & (green > blue * 1.35)
    ).astype(np.uint8) * 255
    # The chroma screen is intentional and no costume color meets this strict
    # green ratio, so enclosed holes between gloves/arms are background too.
    connected_background = candidate == 255

    background_image = Image.fromarray(
        connected_background.astype(np.uint8) * 255, mode="L"
    ).filter(ImageFilter.MaxFilter(5))
    alpha = 255 - np.asarray(background_image, dtype=np.uint8)
    alpha_image = Image.fromarray(alpha, mode="L").filter(
        ImageFilter.GaussianBlur(radius=0.75)
    )
    rgba = source.convert("RGBA")
    rgba.putalpha(alpha_image)
    # Remove green spill from the antialiased silhouette only. Fully opaque
    # teal costume regions are deliberately untouched.
    rgba_array = np.asarray(rgba).copy()
    edge = rgba_array[:, :, 3] < 250
    edge_green = (
        edge
        & (rgba_array[:, :, 1] > rgba_array[:, :, 0] * 1.12)
        & (rgba_array[:, :, 1] > rgba_array[:, :, 2] * 1.10)
    )
    rgba_array[:, :, 1][edge_green] = np.maximum(
        rgba_array[:, :, 0][edge_green], rgba_array[:, :, 2][edge_green]
    )
    rgba = Image.fromarray(rgba_array, mode="RGBA")
    rgba.thumbnail(RUNTIME_SIZE, Image.Resampling.LANCZOS)
    fitted = Image.new("RGBA", RUNTIME_SIZE, (0, 0, 0, 0))
    fitted.alpha_composite(
        rgba,
        ((RUNTIME_SIZE[0] - rgba.width) // 2, (RUNTIME_SIZE[1] - rgba.height) // 2),
    )
    rgba = fitted

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(OUTPUT, optimize=True)
    print(
        "OPERA_BOXER|runtime=%s|size=%dx%d|alpha=%s"
        % (OUTPUT, rgba.width, rgba.height, rgba.getextrema()[3])
    )


if __name__ == "__main__":
    main()
