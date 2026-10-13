"""Retain config/room-opening diagnostics without altering production paths."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / "audit/cycles/luna-playtest-20261012"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--supplied-phases", action="store_true")
    args = parser.parse_args()
    mode = "farmer_supplied_phases" if args.supplied_phases else "farmer_production_config"
    destination = CYCLE / "verification" / mode
    if destination.exists():
        raise ValueError("Preserve existing evidence; this diagnostic already exists")
    destination.mkdir()
    explicit = json.loads((ROOT / "tmp/luna_local_config.json").read_text())["godot"]
    resolved = subprocess.check_output([sys.executable, "-B", "tools/resolve_godot.py", "--godot", explicit], cwd=ROOT, text=True).strip()
    engine = Path(resolved)
    version = subprocess.check_output([resolved, "--version"], text=True).strip()
    if version != "4.7.2.stable.official.ed1daf0bf":
        raise ValueError("Exact approved engine required")
    profile = Path(tempfile.mkdtemp(prefix="reef-luna-" + mode + "-"))
    environment = os.environ.copy()
    for key, name in [("APPDATA", "appdata"), ("LOCALAPPDATA", "localappdata"), ("XDG_DATA_HOME", "data"), ("XDG_CONFIG_HOME", "config")]:
        path = profile / name
        path.mkdir()
        environment[key] = str(path)
    script = CYCLE / "review_tools/chapter2_farmer_diagnostic.gd"
    command = [resolved, "--headless", "--path", str(ROOT), "-s", script.relative_to(ROOT).as_posix(), "--", "--touch", "--classic-touch-test"]
    if args.supplied_phases:
        command.append("--supplied-phases")
    log = destination / "probe.log"
    started = datetime.now(timezone.utc).isoformat()
    clock_start = time.monotonic()
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=ROOT, env=environment, stdout=output, stderr=subprocess.STDOUT, timeout=120)
    raw = log.read_text(encoding="utf-8", errors="replace")
    paths = ["scripts/main.gd", "scripts/chapter_two_director.gd", "scripts/opera_house.gd", "scripts/opera_act.gd", "scripts/opera_career_world_2d.gd", "scripts/chapter_two_career_scene_adapter.gd"]
    receipt = {"schema": "luna_farmer_diagnostic/1", "baseline": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "command": command, "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
               "engine": {"version": version, "sha256": sha(engine)}, "fixture_sha256": sha(script), "helper_sha256": sha(Path(__file__)),
               "source_hashes": {path: sha(ROOT / path) for path in paths}, "exit_code": result.returncode,
               "status": "PASS" if result.returncode == 0 and "Healthy first task: OK" in raw else "FAIL",
               "explicit_phases_supplied": args.supplied_phases, "profile_isolated": True, "save_profile": str(profile),
               "headless": True, "evidence_kind": "INTERNAL_PRODUCTION_CALL_CHAIN_DIAGNOSTIC",
               "scope": "Injected post-boss state; production director/House/Act chain, no visible room/fresh child route/device/child acceptance.",
               "wall_clock_is_gameplay_timing": False, "wall_elapsed_seconds": round(time.monotonic() - clock_start, 3),
               "log": log.relative_to(ROOT).as_posix(), "log_sha256": sha(log)}
    (destination / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mode": mode, "status": receipt["status"], "exit_code": result.returncode, "diagnostic": [x for x in raw.splitlines() if x.startswith("FARMER_CONFIG_DIAGNOSTIC|")]}))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
