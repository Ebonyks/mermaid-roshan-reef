"""Run the dedicated Bubble Duel checks with a fresh, disposable Godot save."""
from pathlib import Path
import argparse
import os
import subprocess
import tempfile
import sys
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    resolver = subprocess.run([sys.executable, "-B", str(ROOT / "tools/resolve_godot.py")],
                              cwd=ROOT, capture_output=True, text=True, check=True)
    engine = resolver.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="bubble-duel-stress-") as temporary:
        state = Path(temporary)
        env = os.environ.copy()
        for key, folder in (("APPDATA", "roaming"), ("LOCALAPPDATA", "local"),
                            ("XDG_DATA_HOME", "data"), ("XDG_CONFIG_HOME", "config")):
            target = state / folder
            target.mkdir()
            env[key] = str(target)
        env["BUBBLE_DUEL_STRESS_ROOT"] = str(state)
        env["BUBBLE_DUEL_STRESS_OUTPUT"] = str(output)
        log = output.with_suffix(".log")
        with log.open("w", encoding="utf-8") as transcript:
            run = subprocess.run([engine, "--headless", "--path", str(ROOT),
                                  "-s", "scripts/probe_bubble_duel_stress.gd", "--",
                                  "--touch", "--classic-touch-test"],
                                 cwd=ROOT, env=env, stdout=transcript,
                                 stderr=subprocess.STDOUT, timeout=600)
        text = log.read_text(encoding="utf-8", errors="replace")
        print(text[-6000:])
        if "SCRIPT ERROR" in text:
            return 1
        if run.returncode or not output.exists():
            return run.returncode or 1
        result = json.loads(output.read_text(encoding="utf-8"))
        if len(result["cycles"]) != 100 or result["failures"] or any(not r["passed"] for r in result["cycles"]):
            return 1
        reload_output = output.with_name(output.stem + "-reload.json")
        env["BUBBLE_DUEL_VERIFY_RELOAD"] = "1"
        env["BUBBLE_DUEL_RELOAD_OUTPUT"] = str(reload_output)
        with log.open("a", encoding="utf-8") as transcript:
            transcript.write("\nRELOAD_PHASE: new Godot process, same isolated save\n")
            transcript.flush()
            reload_run = subprocess.run([engine, "--headless", "--path", str(ROOT),
                                         "-s", "scripts/probe_bubble_duel_stress.gd", "--",
                                         "--touch", "--classic-touch-test"],
                                        cwd=ROOT, env=env, stdout=transcript,
                                        stderr=subprocess.STDOUT, timeout=120)
        print(log.read_text(encoding="utf-8", errors="replace")[-1500:])
        if reload_run.returncode or not reload_output.exists():
            return reload_run.returncode or 1
        reload_data = json.loads(reload_output.read_text(encoding="utf-8"))
        return 1 if reload_data["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

