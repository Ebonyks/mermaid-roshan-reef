"""Retain the unchanged advisory Opera simulation and honest incomplete verdicts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / "audit/cycles/luna-playtest-20261012"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    out = CYCLE / "verification/opera_pacing"
    if out.exists():
        raise ValueError("Preserve existing evidence")
    out.mkdir()
    explicit = json.loads((ROOT / "tmp/luna_local_config.json").read_text())["godot"]
    resolved = subprocess.check_output([sys.executable, "-B", "tools/resolve_godot.py", "--godot", explicit], cwd=ROOT, text=True).strip()
    engine = Path(resolved)
    version = subprocess.check_output([resolved, "--version"], text=True).strip()
    if version != "4.7.2.stable.official.ed1daf0bf":
        raise ValueError("Exact approved engine required")
    profile = Path(tempfile.mkdtemp(prefix="reef-luna-opera-pacing-"))
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    for key, name in [("APPDATA", "appdata"), ("LOCALAPPDATA", "localappdata"), ("XDG_DATA_HOME", "data"), ("XDG_CONFIG_HOME", "config")]:
        path = profile / name
        path.mkdir()
        env[key] = str(path)
    command = [sys.executable, "-X", "utf8", "-B", "tools/run_advisory_sensor.py", "--name", "opera-pacing", "--report-dir", str(out), "--expected", "BALANCE|RESULT|", "--timeout", "610", "--", resolved, "--headless", "--path", str(ROOT), "-s", "scripts/probe_opera_balance.gd", "--", "--touch"]
    receipt_path, log = out / "receipt.json", out / "wrapper.log"
    paths = ["scripts/probe_opera_balance.gd", "scripts/probe_opera_2d_balance.gd", "scripts/opera_act.gd", "scripts/opera_career_world_2d.gd", "tools/run_advisory_sensor.py"]
    data = {"schema": "luna_pacing_receipt/1", "baseline": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "command": command,
            "started_utc": datetime.now(timezone.utc).isoformat(), "status": "RUNNING", "engine": {"version": version, "sha256": sha(engine)},
            "source_hashes": {path: sha(ROOT / path) for path in paths}, "helper_sha256": sha(Path(__file__)), "profile_isolated": True, "save_profile": str(profile),
            "evidence_kind": "INTERNAL_SCRIPTED_TIME_MODEL", "headless": True, "wall_clock_is_gameplay_timing": False,
            "scope": "Unchanged advisory runner, synthetic persona assumptions, direct setup/callbacks/manual0.1s ticks; no ordinary room entry, full child playthrough, physical input, actual session duration or fun acceptance."}
    receipt_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    clock_start = time.monotonic()
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT)
    sensor = json.loads((out / "opera-pacing.json").read_text(encoding="utf-8"))
    data.update(status=sensor["status"], exit_code=result.returncode, reason=sensor["reason"], finished_utc=datetime.now(timezone.utc).isoformat(),
                wall_elapsed_seconds=round(time.monotonic() - clock_start, 3), log=log.relative_to(ROOT).as_posix(), log_sha256=sha(log),
                sensor=(out / "opera-pacing.json").relative_to(ROOT).as_posix(), sensor_sha256=sha(out / "opera-pacing.json"))
    receipt_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": data["status"], "reason": data["reason"], "wrapper_exit": result.returncode, "wall_seconds": data["wall_elapsed_seconds"]}))
    return result.returncode

if __name__ == "__main__":
    raise SystemExit(main())
