"""Preserve literal native PNGs in bounded archives and verify the Aseprite bridge."""
from pathlib import Path
import hashlib
import json
import zipfile
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sha = lambda data: hashlib.sha256(data).hexdigest()
(ROOT / "archives").mkdir(exist_ok=True)
archives = []
for label, folder in [("take01_native_scene", ROOT / "frames/take01"),
                      ("take02_native_figure", ROOT / "frames/take02/rgba"),
                      ("take03_native_figure", ROOT / "frames/take03/rgba"),
                      ("take04_native_figure", ROOT / "frames/take04/rgba")]:
    frames = sorted(folder.glob("[0-9]*.png"))
    for first in range(0, len(frames), 64):
        subset = frames[first:first + 64]
        path = ROOT / "archives" / f"{label}_{first:04d}.zip"
        index = []
        with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as archive:
            for source in subset:
                data = source.read_bytes()
                archive.writestr(source.name, data)
                index.append({"name": source.name, "sha256": sha(data)})
            archive.writestr("index.json", json.dumps({"fps": 30, "frames": index,
                "time": "frame index / 30 seconds; literal original PNG bytes"}, indent=2) + "\n")
        with zipfile.ZipFile(path) as archive:
            assert all(sha(archive.read(row["name"])) == row["sha256"] for row in index)
        archives.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path.read_bytes()),
                         "frames": len(subset), "literal_byte_roundtrip": True})
        print(path.name, len(subset), flush=True)
proof = json.loads((ROOT / "masters/master_proof.json").read_text())
assert proof["layers"] == 1 and proof["count"] == 331
matches = []
for i in range(331):
    source = Image.open(ROOT / "frames/take04/rgba" / f"{i:04d}.png").convert("RGBA")
    reopened = Image.open(ROOT / "masters/frames" / f"{i:04d}.png").convert("RGBA")
    matches.append(bool(np.array_equal(np.array(source), np.array(reopened))))
assert all(matches)
result = {"archives": archives, "aseprite": {"frames": 331, "layers": 1,
    "rgba_exact_reopened_frames": sum(matches), "duration_ms": sum(proof["durations_ms"]),
    "master_sha256": sha((ROOT / "masters/whole_sprite.aseprite").read_bytes())},
    "native_source": "Actual Godot 4.7.2 Mobile captures. No generated/repaired pixels, temporal interpolation, retiming or new art.",
    "mapping": "Native frame i maps to review and Aseprite frame i. Only Aseprite millisecond duration rounding (33/34ms); movie 30fps.",
    "take01_limit": "Exact rendered frames and source seed retained. Pre-launch action-script snapshot was not captured; take02 source snapshot is retained under rejected_take02; take04 source is the current editable study."
}
(ROOT / "export_receipt.json").write_text(json.dumps(result, indent=2) + "\n")
print("ASEPRITE RGBA ROUNDTRIP", sum(matches), "/331")
