"""Build the Godot atlases from the archived ImageGen RGBA sheets.

Run from the repository root with Pillow, NumPy and SciPy installed.
"""
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

SOURCES = Path(__file__).resolve().parent
RUNTIME = Path("assets/racer/stage_art_v1")


def prepare(source: Path) -> list[tuple[int, int, int, int]]:
    key = source.stem.removesuffix("_native")
    cell_size = 256 if key == "pickups" else 512
    padding = 12
    atlas = Image.new("RGBA", (cell_size * 2, cell_size * 2))
    regions = []
    with Image.open(source) as sheet:
        middle_x = sheet.width // 2
        # The pantry finial in the kitchen sheet reaches above the nominal midline.
        middle_y = 600 if key == "kitchen" else sheet.height // 2
        for row, (y0, y1) in enumerate(((0, middle_y), (middle_y, sheet.height))):
            for column, (x0, x1) in enumerate(((0, middle_x), (middle_x, sheet.width))):
                card = sheet.crop((x0, y0, x1, y1))
                alpha = np.asarray(card.getchannel("A"))
                labels, _ = ndimage.label(alpha >= 125)
                areas = np.bincount(labels.ravel())
                areas[0] = 0
                silhouette = labels == areas.argmax()
                # Keep the painted antialiasing at the contour and drop the
                # generator's disconnected colour fringe outside the subject.
                edge = ndimage.binary_dilation(silhouette, iterations=2)
                matte = np.where(edge, alpha, 0).astype(np.uint8)
                card.putalpha(Image.fromarray(matte))
                card = card.crop(card.getchannel("A").getbbox())
                card.thumbnail((cell_size - 2 * padding, cell_size - 2 * padding), Image.Resampling.LANCZOS)
                at = (column * cell_size + padding, row * cell_size + padding)
                atlas.paste(card, at)
                regions.append((*at, *card.size))
    atlas.save(RUNTIME / f"{key}.png", optimize=True)
    return regions


if __name__ == "__main__":
    for master in sorted(SOURCES.glob("*_native.png")):
        print(master.stem, prepare(master))
