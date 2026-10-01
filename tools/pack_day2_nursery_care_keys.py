"""Lossless atlas-window packing; no source pixel repair or resampling."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/imagegen/day2_nursery_motionkeys_20261001"
RUNTIME = ROOT / "assets/opera/worlds/nursery/refinement_v2"
EXPECTED = "2645fcce60cceefe09e50b20be3f7786ee0af2cd0d9097b3f52b26c2409ba663"
# Boundaries lie in fully transparent native corridors. Regular generated
# cell boundaries would cut a fin and leak that fin into its neighbour.
WINDOWS = [(0, 0, 471, 453), (471, 0, 903, 453),
           (903, 0, 1340, 453), (1340, 0, 1774, 453),
           (0, 453, 471, 887), (471, 453, 903, 887),
           (903, 453, 1348, 887), (1348, 453, 1774, 887)]
# Starting manually inspected anatomical/socket estimates in native atlas
# coordinates. Contextual fit review must refine these before acceptance.
HIPS = [(215, 346), (653, 340), (1096, 339), (1529, 338),
        (218, 768), (655, 770), (1110, 771), (1538, 773)]
PALMS = [(106, 264), (533, 249), (981, 229), (1409, 237),
         (104, 725), (535, 723), (985, 750), (1402, 775)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = SOURCE / "candidates/attempt-01.png"
    assert digest(source) == EXPECTED
    native = Image.open(source).convert("RGBA")
    assert native.size == (1774, 887)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    rebuilt = Image.new("RGBA", native.size)
    poses = []
    for index, window in enumerate(WINDOWS):
        crop = native.crop(window)
        offset = ((512 - crop.width) // 2, (512 - crop.height) // 2)
        padded = Image.new("RGBA", (512, 512))
        padded.paste(crop, offset)
        path = RUNTIME / f"care_{index:02}.png"
        padded.save(path)
        reopened = Image.open(path).convert("RGBA")
        recovered = reopened.crop((offset[0], offset[1],
                                   offset[0] + crop.width, offset[1] + crop.height))
        assert recovered.tobytes() == crop.tobytes()
        rebuilt.paste(recovered, window[:2])
        bounds = reopened.getchannel("A").getbbox()
        assert bounds and min(bounds[0], bounds[1], 512 - bounds[2], 512 - bounds[3]) >= 14
        pose = {"index": index, "path": path.relative_to(ROOT).as_posix(),
                "sha256": digest(path), "dimensions": [512, 512],
                "source_window": list(window), "padding_offset": list(offset),
                "alpha_bounds": list(bounds),
                "hip_xy": [HIPS[index][j] - window[j] + offset[j] for j in range(2)],
                "palm_xy": [PALMS[index][j] - window[j] + offset[j] for j in range(2)],
                "pixel_copy_exact": True}
        poses.append(pose)
    assert rebuilt.tobytes() == native.tobytes(), "Native atlas reconstruction must be exact"
    report = {"schema": "reef.nursery-care-pack.v1", "source": source.relative_to(ROOT).as_posix(),
              "source_sha256": EXPECTED, "native_dimensions": list(native.size),
              "method": "Nonoverlapping exact RGBA windows on transparent 512px canvases; no resampling, filtering, recolour, alpha repair, warping, or subject redraw.",
              "native_reconstruction_rgba_sha256": hashlib.sha256(rebuilt.tobytes()).hexdigest(),
              "all_source_rgba_pixels_reconstructed": True,
              "socket_method": "Manual native anatomical/socket estimates; fit review pending.",
              "poses": poses, "owner_accepted": False, "runtime_contact_accepted": False}
    (SOURCE / "PACK_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (RUNTIME / "care_keys.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("NURSERY_CARE_PACK|PASS|8 padded keys|all native RGBA pixels reconstructed")


if __name__ == "__main__":
    main()
