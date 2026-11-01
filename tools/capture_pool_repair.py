"""Source-bound Pool visual fixture with isolated saves and engine-native PNGs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import time

from resolve_godot import resolve
from audit_godot_baseline import load_baseline

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tall", action="store_true")
    parser.add_argument("--motion", action="store_true")
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    engine = resolve(ROOT, load_baseline(ROOT / "tools/godot_baseline.json"), os.environ.get("GODOT"), dict(os.environ))
    environment = dict(os.environ)
    profile = Path(tempfile.mkdtemp(prefix="reef-pool-visual-repair-"))
    for key in ("APPDATA", "LOCALAPPDATA"):
        folder = profile / key.lower()
        folder.mkdir()
        environment[key] = str(folder)
    environment["DAY_ONE_POOL_CAPTURE_OUT"] = str(out)
    environment["POOL_CAPTURE_TALL"] = "1" if args.tall else "0"
    environment["POOL_CAPTURE_MOTION"] = "1" if args.motion else "0"
    environment["POOL_CAPTURE_PROFILE_ROOT"] = str(profile)
    if not all(Path(environment[key]).is_relative_to(profile) for key in ("APPDATA", "LOCALAPPDATA")):
        raise ValueError("Capture save-profile override is not isolated")
    command = [engine, "--path", str(ROOT), "--windowed", "--rendering-method", "mobile", "--resolution", "1280x800" if args.tall else "1280x720", "--audio-driver", "Dummy", "-s", "scripts/probe_day_one_pool_shots.gd", "--", "--touch", "--classic-touch-test"]
    changed = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    sources = sorted(set(changed + ["shaders/pool_floating_debris.gdshader", "shaders/pool_blocked_fountain.gdshader", "scripts/probe_day_one_pool_shots.gd", "assets/flats/castle/interactions_v4/rest_cards/mermaid_pool_seahorse_fountain_rest.png", "assets/castle/day_one_pool/activities/seahorse_mouth_trash.png", "assets/castle/day_one_pool/activities/floating_trash_atlas.png", "assets/characters/rumi/rumi_eight_pose_runtime.png", "assets/sprites/fx_water/fx_water_ripple_ring_atlas.png"]))
    receipt = {"baseline": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "command": command, "engine_sha256": digest(Path(engine)), "profile": str(profile), "save_isolated": True, "renderer_requested": "mobile", "viewport": [1280, 800 if args.tall else 720], "scope": "Direct-room visual fixture; story clips canceled. Agent desktop composition only; no fresh-save traversal, audio listening, device, child or owner acceptance.", "sources": {path: digest(ROOT / path) for path in sources if (ROOT / path).is_file()}}
    start = time.monotonic()
    with (out / "capture.log").open("w", encoding="utf-8") as log:
        try:
            run = subprocess.run(command, cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT, timeout=600)
            code = run.returncode
        except subprocess.TimeoutExpired:
            code = 124
    receipt.update(exit_code=code, wall_seconds=round(time.monotonic() - start, 3), files={path.name: digest(path) for path in sorted(out.glob("*.png"))}, log_sha256=digest(out / "capture.log"))
    receipt["actual_user_data_dir"] = next((line.split("|", 1)[1] for line in (out / "capture.log").read_text(encoding="utf-8", errors="replace").splitlines() if line.startswith("POOL_PROFILE|")), None)
    encoder = shutil.which("ffmpeg")
    if args.motion and encoder:
        samples: dict[str, list[tuple[int, float]]] = {}
        for line in (out / "capture.log").read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("POOL_MOTION|"):
                _, label, index, elapsed = line.split("|")
                samples.setdefault(label, []).append((int(index), float(elapsed)))
        receipt["motion"] = {}
        for label, timing in samples.items():
            listing = out / ("motion_" + label + ".txt")
            entries = []
            for slot, (index, elapsed) in enumerate(timing):
                frame = out / ("motion_" + label) / f"{index:04d}.png"
                duration = timing[slot + 1][1] - elapsed if slot + 1 < len(timing) else 1.0 / 12.0
                entries.extend(["file '" + frame.as_posix() + "'", f"duration {duration:.4f}"])
            listing.write_text("\n".join(entries) + "\n", encoding="utf-8")
            movie = out / ("motion_" + label + ".mp4")
            subprocess.run([encoder, "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-fps_mode", "vfr", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(movie)], check=True)
            receipt["motion"][label] = {"path": movie.name, "sha256": digest(movie), "frame_times": timing, "method": "Native viewport PNGs with actual elapsed-time durations; diagnostic H264 preview, no interpolation or generated frames"}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exit_code": code, "captures": len(receipt["files"]), "output": str(out)}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
