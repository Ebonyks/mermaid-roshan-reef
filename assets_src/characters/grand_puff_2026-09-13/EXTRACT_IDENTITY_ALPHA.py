from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
root = Path(__file__).resolve().parent
source = np.array(Image.open(root / "owner_local_boss_portrait.png").convert("RGB"))
mask = (source[:, :, 2].astype(int) - source[:, :, 0].astype(int) > 5) & (source[:, :, 2].astype(int) - source[:, :, 1].astype(int) > 12)
mask[:4, :] = mask[-4:, :] = False
mask[:, :4] = mask[:, -4:] = False
labels, _ = ndimage.label(mask)
keep = np.bincount(labels.ravel()) >= 100
keep[0] = False
mask = ndimage.binary_fill_holes(keep[labels])
image = Image.fromarray(np.dstack([source, mask.astype(np.uint8) * 255]))
# Run only on the packet's preserved source; no original is overwritten.
image.save(root / "identity_alpha.png")
