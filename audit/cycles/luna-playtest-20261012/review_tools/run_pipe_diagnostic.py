"""Retain the independent viewport-input pipe ownership diagnostic."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / "audit/cycles/luna-playtest-20261012"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="pipe_touch")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9_-]{1,64}", args.output):
        raise ValueError("Simple named evidence output required")
    out = CYCLE / "verification" / args.output
    if out.exists():
        raise ValueError("Preserve the existing diagnostic; do not overwrite")
    out.mkdir()
    explicit = json.loads((ROOT / "tmp/luna_local_config.json").read_text())["godot"]
    resolved = subprocess.check_output([sys.executable, "-B", "tools/resolve_godot.py", "--godot", explicit], cwd=ROOT, text=True).strip()
    engine = Path(resolved)
    version = subprocess.check_output([resolved, "--version"], text=True).strip()
    if version != "4.7.2.stable.official.ed1daf0bf":
        raise ValueError("Exact approved engine required")
    profile = Path(tempfile.mkdtemp(prefix="reef-luna-pipe-touch-"))
    env = os.environ.copy()
    for key, name in [("APPDATA", "appdata"), ("LOCALAPPDATA", "localappdata"), ("XDG_DATA_HOME", "data"), ("XDG_CONFIG_HOME", "config")]:
        path = profile / name
        path.mkdir()
        env[key] = str(path)
    fixture = CYCLE / "review_tools/pipe_touch_diagnostic.gd"
    command = [resolved, "--headless", "--path", str(ROOT), "-s", fixture.relative_to(ROOT).as_posix(), "--", "--touch", "--classic-touch-test"]
    started, clock_start = datetime.now(timezone.utc).isoformat(), time.monotonic()
    log = out / "probe.log"
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=90)
    raw = log.read_text(encoding="utf-8", errors="replace")
    receipt = {"schema": "luna_pipe_diagnostic/1", "baseline": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "command": command, "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
               "engine": {"version": version, "sha256": sha(engine)}, "fixture_sha256": sha(fixture), "helper_sha256": sha(Path(__file__)),
               "source_hashes": {path: sha(ROOT / path) for path in ["scripts/opera_gesture_surface.gd", "scripts/probe_opera_pipe.gd"]},
               "exit_code": result.returncode, "status": "PASS" if result.returncode == 0 and "RESULT: PASS" in raw and "SCRIPT ERROR" not in raw else "FAIL",
               "profile_isolated": True, "save_profile": str(profile), "headless": True, "evidence_kind": "ROUTED_VIEWPORT_INPUT_DIAGNOSTIC",
               "scope": "Standalone first pipe round with synthetic touch IDs7/9; no Castle route, physical device, rendered latency or child acceptance. No production code altered.",
               "wall_clock_is_gameplay_timing": False, "wall_elapsed_seconds": round(time.monotonic() - clock_start, 3),
               "log": log.relative_to(ROOT).as_posix(), "log_sha256": sha(log)}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "exit_code": result.returncode, "checks": [x for x in raw.splitlines() if x.startswith("PIPE_TOUCH_DIAGNOSTIC|")]}))
    return result.returncode

if __name__ == "__main__":
    raise SystemExit(main())
