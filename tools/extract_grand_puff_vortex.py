"""Reproduce the owner-authorized 2026-09-13 vortex matte extraction."""
import argparse
import hashlib
import io
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/grand_puff_warning_v4/purple_vortex_native.png"
OUTPUT = ROOT / "assets/effects/grand_puff/purple_vortex_v4.png"
SOURCE_SHA256 = "94ba2b507e3e5925eac7dda8c3f01cfbe734c43ad5324cdf051d701fe924f35e"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("VORTEX: native source differs from the approved extraction input")
    image = Image.open(SOURCE).convert("RGB")
    pixels = np.asarray(image).astype(np.int16)
    strong = pixels[:, :, 2] - pixels[:, :, 1] > 20
    labels, _count = ndimage.label(strong)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    mask = ndimage.binary_fill_holes(labels == int(sizes.argmax()))
    # Exclude the matte-mixed outer antialias pixels; retained RGB stays intact.
    mask = ndimage.binary_erosion(mask, iterations=2)
    image = image.convert("RGBA")
    image.putalpha(Image.fromarray(mask.astype(np.uint8) * 255))
    result = io.BytesIO()
    image.resize((512, 512), Image.Resampling.LANCZOS).save(result, format="PNG")
    payload = result.getvalue()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != payload:
            raise SystemExit("VORTEX: runtime asset differs from reproducible extraction")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(payload)
    print("VORTEX|ALL OK|" + hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
