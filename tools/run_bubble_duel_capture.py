"""Capture the actual Mobile game with a dedicated, explicitly guarded save fixture."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("scripts/opera_bubble_duel.gd", "scripts/bubble_duel_inventory.gd",
           "scripts/bubble_duel_cast.gd", "scripts/bubble_duel_two_player.gd",
           "scripts/bubble_duel_preview.gd", "scripts/probe_bubble_duel_capture.gd",
           "scripts/probe_bubble_duel_cast_capture.gd")


def bindings():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--widths", type=int, nargs="+", default=[1280])
    parser.add_argument("--cast", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    engine = subprocess.check_output([sys.executable, "-B", str(ROOT / "tools/resolve_godot.py")], cwd=ROOT, text=True).strip()
    before = bindings()
    probe = "scripts/probe_bubble_duel_cast_capture.gd" if args.cast else "scripts/probe_bubble_duel_capture.gd"
    for width in args.widths:
        if width < 640:
            raise SystemExit("Capture width must be at least640")
        target = output / str(width)
        if target.exists() and any(target.iterdir()):
            raise SystemExit("Use a fresh capture directory; existing evidence is preserved.")
        target.mkdir(parents=True, exist_ok=True)
        state = output / "_userdata" / (str(width) + "-" + uuid.uuid4().hex)
        state.mkdir(parents=True)
        env = os.environ.copy()
        for key, folder in (("APPDATA", "roaming"), ("LOCALAPPDATA", "local"),
                            ("XDG_DATA_HOME", "data"), ("XDG_CONFIG_HOME", "config")):
            path = state / folder
            path.mkdir()
            env[key] = str(path)
        env.update(DUEL_CAPTURE_SAVE_ROOT=str(state), DUEL_CAPTURE_DIR=str(target),
                   DUEL_CAPTURE_WIDTH=str(width))
        startup = None
        if os.name == "nt":
            startup = subprocess.STARTUPINFO()
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup.wShowWindow = 0
        with (target / "capture.log").open("wb") as transcript:
            run = subprocess.run([engine, "--path", str(ROOT), "--rendering-method", "mobile",
                                  "--audio-driver", "Dummy", "--resolution", f"{width}x720",
                                  "-s", probe, "--", "--touch", "--classic-touch-test"],
                                 cwd=ROOT, env=env, stdout=transcript,
                                 stderr=subprocess.STDOUT, startupinfo=startup, timeout=600)
        text = (target / "capture.log").read_text(encoding="utf-8", errors="replace")
        if run.returncode or "SCRIPT ERROR" in text or not (target / "captures.json").exists():
            print(text[-6000:])
            return run.returncode or 1
        capture = json.loads((target / "captures.json").read_text(encoding="utf-8"))
        if capture["renderer"] != "mobile" or capture["quality"] != "speedy":
            raise SystemExit("Requested renderer/quality not proved")
        for row in capture["captures"]:
            image = target / row["file"]
            if row["w"] != width or row["h"] != 720 or hashlib.sha256(image.read_bytes()).hexdigest() != row["sha256"]:
                raise SystemExit("Capture size/hash mismatch")
        print(f"CAPTURE|{width}x720|Mobile/Speedy|{len(capture['captures'])} frames|PASS", flush=True)
    if bindings() != before:
        raise SystemExit("Feature source changed during capture")
    (output / "source-bindings.json").write_text(json.dumps({"bindings": before,
        "scope": "Own feature files only; not formal same-process QA11 active dependency closure.",
        "claim": "Diagnostic appearance captures, not device/child/owner acceptance."}, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
