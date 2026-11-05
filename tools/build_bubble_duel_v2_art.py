"""Package the three preserved generated atlases without painting source pixels."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets_src/bubble_duel_v2"
DEST = ROOT / "assets/opera/bubble_duel_v2"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    otter = Image.open(SOURCE / "marlo_native.png").convert("RGBA")
    cells = []
    for index in range(4):
        x = index % 2 * (otter.width // 2)
        y = index // 2 * (otter.height // 2)
        cell = otter.crop((x, y, x + otter.width // 2, y + otter.height // 2))
        bounds = cell.getchannel("A").point(lambda a: 255 if a >= 16 else 0).getbbox()
        if bounds is None:
            raise ValueError("Missing otter pose")
        cells.append((cell, bounds))
    factor = 232 / max(b[2] - b[0] for _, b in cells)
    atlas = Image.new("RGBA", (512, 512))
    mappings = []
    for index, (cell, bounds) in enumerate(cells):
        crop = cell.crop(bounds)
        span = (round(crop.width * factor), round(crop.height * factor))
        frame = crop.resize(span, Image.Resampling.LANCZOS)
        offset = (index % 2 * 256 + (256 - span[0]) // 2,
                  index // 2 * 256 + (256 - span[1]) // 2)
        atlas.alpha_composite(frame, offset)
        mappings.append({"cell": index, "bounds": bounds, "uniform_scale": factor, "offset": offset})
    atlas.save(DEST / "marlo_swim.png")
    records.append({"file": "marlo_swim.png", "source": "marlo_native.png",
                    "mapping": mappings, "method": "Threshold bounds for extraction, common whole-figure scale and centering only"})

    bubble = Image.open(SOURCE / "bubble_native.png").convert("RGBA")
    bounds = bubble.getchannel("A").point(lambda a: 255 if a >= 16 else 0).getbbox()
    side = max(bounds[2] - bounds[0], bounds[3] - bounds[1]) + 20
    center = ((bounds[0] + bounds[2]) // 2, (bounds[1] + bounds[3]) // 2)
    crop = (center[0] - side // 2, center[1] - side // 2,
            center[0] - side // 2 + side, center[1] - side // 2 + side)
    bubble.crop(crop).resize((256, 256), Image.Resampling.LANCZOS).save(DEST / "bubble.png")
    records.append({"file": "bubble.png", "source": "bubble_native.png", "crop": crop,
                    "method": "Uniform square crop and whole-canvas downsampling"})

    icons = Image.open(SOURCE / "items_native.png").convert("RGBA")
    icons.resize((1024, 512), Image.Resampling.LANCZOS).save(DEST / "items.png")
    records.append({"file": "items.png", "source": "items_native.png",
                    "method": "Uniform whole-sheet downsampling to 4x2 256-square cells"})
    for row in records:
        row["sha256"] = digest(DEST / row["file"])
        row["source_sha256"] = digest(SOURCE / row["source"])
        row["dimensions"] = Image.open(DEST / row["file"]).size
    (SOURCE / "exports.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()

