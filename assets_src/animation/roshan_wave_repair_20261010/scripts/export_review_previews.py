"""Encode whole-frame review media and verify metadata; never repair pixels."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

from PIL import Image

PACKET = Path(__file__).resolve().parent.parent
ROOT = next(p for p in PACKET.parents if (p / "project.godot").is_file())
sys.path.insert(0, str(ROOT))
from tools import sprite_pipeline as engine


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", required=True)
    parser.add_argument("--aseprite", required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()
    final = (PACKET / args.final).resolve()
    final.relative_to(PACKET)
    rows = []
    for label, folder, canvas in [("native", "native_rgba", [768, 896]),
                                  ("sprite", "frames", [256, 256])]:
        paths = [final / folder / f"{i:04d}.png" for i in range(41)]
        if not all(p.is_file() for p in paths):
            raise ValueError("All 41 complete source frames must exist")
        job = {"id": "roshan-wave-repair-20261010-" + label,
               "native_canvas": canvas, "frames": [{} for _ in paths],
               "frame_paths": paths,
               "action": {"fps": 24, "phases": [
                   {"from": 0, "to": 4, "name": "entry"},
                   {"from": 5, "to": 13, "name": "raise"},
                   {"from": 14, "to": 24, "name": "wave"},
                   {"from": 25, "to": 33, "name": "lower"},
                   {"from": 34, "to": 40, "name": "settle"}]}}
        rows.append(engine.export_master(ROOT, job, final / (label + "_roundtrip"), args.aseprite))
    out = final / "preview"
    out.mkdir()
    common = [args.ffmpeg, "-hide_banner", "-loglevel", "error", "-framerate", "24",
              "-i", str(final / "frames/%04d.png")]
    commands = [
        common + ["-frames:v", "41", "-c:v", "libwebp_anim", "-lossless", "1", "-loop", "0",
                  "-vsync", "0", str(out / "roshan_wave.webp")],
        common + ["-f", "lavfi", "-i", "color=c=0x2d3744:s=512x512:r=24",
                  "-filter_complex", "[0:v]scale=512:512:flags=lanczos[fg];[1:v][fg]overlay=shortest=1:format=auto,format=yuv420p,setsar=1[v]",
                  "-map", "[v]", "-frames:v", "41", "-c:v", "libx264", "-crf", "12",
                  "-preset", "medium", "-movflags", "+faststart", "-an", str(out / "roshan_wave_dark.mp4")]]
    for command in commands:
        subprocess.run(command, check=True, capture_output=True, timeout=120)
    media = []
    for path in [out / "roshan_wave.webp", out / "roshan_wave_dark.mp4"]:
        media.append({"path": path.relative_to(ROOT).as_posix(),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "bytes": path.stat().st_size})
    with Image.open(out / "roshan_wave.webp") as im:
        count = im.n_frames
        durations = []
        for i in range(count):
            im.seek(i)
            decoded = np.asarray(im.convert("RGBA"))
            with Image.open(final / "frames" / f"{i:04d}.png") as source:
                expected = np.asarray(source.convert("RGBA"))
            visible = expected[:, :, 3] != 0
            if not np.array_equal(decoded[:, :, 3], expected[:, :, 3]) or not np.array_equal(decoded[visible], expected[visible]):
                raise ValueError(f"Lossless WebP changed visible pixels at frame{i}")
            durations.append(im.info.get("duration"))
        if count != 41:
            raise ValueError("Animated preview dropped complete frames")
    if any(type(d) is not int or not 40 <= d <= 43 for d in durations) or abs(sum(durations) - 1708) > 2:
        raise ValueError("WebP preview clock differs materially from the source clock")
    probe = json.loads(subprocess.check_output([
        args.ffprobe, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json",
        str(out / "roshan_wave_dark.mp4")], text=True, timeout=60))
    stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
    rotations = [int(stream.get("tags", {}).get("rotate", 0))] + [int(s.get("rotation", 0)) for s in stream.get("side_data_list", [])]
    if int(stream["nb_read_frames"]) != 41 or stream["avg_frame_rate"] != "24/1" or [stream["width"], stream["height"]] != [512, 512] or stream["sample_aspect_ratio"] != "1:1" or any(rotations) or abs(float(probe["format"]["duration"]) - 41 / 24) > .002:
        raise ValueError("MP4 decoded geometry/count/clock/rotation differs from declared preview")
    record = {"schema": "reef.whole-wave-review-export.v1",
              "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "source_roundtrips": rows, "media": media,
              "source_clock_ms": engine.frame_clock(41, 24),
              "source_total_ms": 1708, "webp_count": count,
              "webp_visible_rgba_exact_frames": count,
              "webp_durations_ms": durations,
              "webp_total_ms": sum(durations), "mp4_probe": probe,
              "preview_derivation": "41 complete sprite PNGs at24fps; lossless animated WebP; MP4 whole-frame2x resize/composite on solid dark field with H264 encoding. No interpolation, per-part transform or added motion.",
              "review_scope": "Model review sample. Owner/device/child and runtime integration remain pending."}
    (out / "export_receipt.json").write_text(json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
