from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
REVIEW = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tmp/reef_kart_visual_inventory"
REVIEW.mkdir(parents=True, exist_ok=True)
scripts = list((ROOT / "scripts/racer").glob("*.gd"))
scripts.append(ROOT / "scripts/racer_game_2d.gd")
direct = set()
for script in scripts:
    direct.update(re.findall(r'res://([^"\n]+\.(?:png|webp|jpg))', script.read_text(encoding="utf-8")))
course_text = (ROOT / "scripts/racer/reef_kart_courses.gd").read_text(encoding="utf-8")
for name in re.findall(r'\["(room_[^"]+)",', course_text):
    direct.add("assets/flats/castle/rooms/" + name + ".png")
for room in ["playroom", "kitchen", "mermaid_pool", "opera_hall"]:
    direct.add("assets/flats/castle/rooms/room_" + room + "_background.png")
rows = []
for path in sorted((ROOT / "assets").rglob("*")):
    if path.suffix.lower() not in {".png", ".webp", ".jpg", ".jpeg"}:
        continue
    rel = path.relative_to(ROOT).as_posix()
    active = rel in direct or rel.startswith(("assets/racer/", "assets/kart/chase/"))
    candidate = active or bool(re.search(r"/(?:props|items|pickups|icons)/|/room_[^/]+_item_|racer|kart|arrow|chevron|gate|finish|start_arch|quality_|/mg/|/depth_cards/", rel, re.I))
    protected = rel.startswith(("assets/book/", "assets/characters/friends/"))
    with Image.open(path) as image:
        dimensions = list(image.size)
        bounds = list(image.convert("RGBA").getchannel("A").getbbox() or (0, 0, 0, 0)) if active else None
    rows.append({"path": rel, "dimensions": dimensions, "bytes": path.stat().st_size,
                 "active_racer_family": active, "replacement_candidate": candidate, "protected": protected,
                 "alpha_bounds": bounds, "sha256": sha256(path.read_bytes()).hexdigest() if candidate else None})
(OUT / "project_asset_inventory.json").write_text(json.dumps({"assets": rows}, indent=2) + "\n", encoding="utf8")

def sheets(items, prefix):
    for page in range((len(items) + 29) // 30):
        subset = items[page * 30:(page + 1) * 30]
        board = Image.new("RGB", (1200, 1050), "#cbd1d5")
        draw = ImageDraw.Draw(board)
        for slot, entry in enumerate(subset):
            x, y = slot % 6 * 200, slot // 6 * 210
            draw.rectangle((x + 4, y + 4, x + 196, y + 169), fill="#496277")
            with Image.open(ROOT / entry["path"]) as image:
                image = image.convert("RGBA")
                if image.getbbox():
                    image = image.crop(image.getbbox())
                image.thumbnail((184, 153))
                board.paste(image, (x + (200 - image.width) // 2, y + 8 + (153 - image.height) // 2), image)
            name = Path(entry["path"]).stem
            draw.text((x + 5, y + 173), name[:27], fill="#17263b")
            draw.text((x + 5, y + 189), name[27:54], fill="#17263b")
        board.save(REVIEW / (prefix + "-" + str(page + 1).zfill(2) + ".png"))
active = [x for x in rows if x["active_racer_family"]]
candidates = [x for x in rows if x["replacement_candidate"] and not x["active_racer_family"]]
sheets(active, "active")
sheets(candidates, "candidates")
print(json.dumps({"raster_inventory": len(rows), "active_racer_family": len(active), "replacement_candidates": len(candidates),
                  "active_boards": (len(active) + 29) // 30, "candidate_boards": (len(candidates) + 29) // 30}))
