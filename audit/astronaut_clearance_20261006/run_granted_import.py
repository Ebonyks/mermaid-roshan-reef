from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, shutil, subprocess, sys, time
ROOT = Path(__file__).resolve().parents[2]
B = Path(__file__).resolve().parent
ENGINE = Path(r"C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe")
CAP = 1536 * 1024 ** 2
RESERVE = 3 * 1024 ** 3
TIME_CAP = 720
CACHE = ROOT / ".godot"
SETTINGS = ROOT / "tmp" / "astronaut_engine_20261006"
LOG = B / "IMPORT_GRANTED_LOG.txt"
RECEIPT = B / "IMPORT_GRANTED_RECEIPT.json"
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def byte_size(path):
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())
assert not RECEIPT.exists()
version = subprocess.check_output([str(ENGINE), "--version"], text=True).strip()
assert version == "4.7.2.stable.official.ed1daf0bf", version
baseline_cache = byte_size(CACHE)
baseline_settings = byte_size(SETTINGS)
assert shutil.disk_usage("C:/").free - CAP >= RESERVE
preflight = B / "IMPORT_GRANTED_PREFLIGHT.json"
pre = json.loads(preflight.read_text(encoding="utf-8"))
assert baseline_cache == pre["owned_existing_cache_bytes"]
assert all(sha(ROOT / x["path"]) == x["sha256"] for x in pre["sources"])
env = os.environ.copy()
for key in ["APPDATA", "LOCALAPPDATA"]:
    d = SETTINGS / key
    d.mkdir(parents=True, exist_ok=True)
    env[key] = str(d)
command = [str(ENGINE), "--headless", "--path", str(ROOT), "--import", "--verbose",
           "--debug-server", "tcp://127.0.0.1:6207", "--lsp-port", "6208", "--dap-port", "6209"]
started = datetime.now(timezone.utc)
t0 = time.monotonic()
last = -30
samples = []
stop_reason = None
with LOG.open("xb") as out:
    process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)
    print(json.dumps({"job": "granted_import", "owned_pid": process.pid, "time_cap_seconds": TIME_CAP}), flush=True)
    while process.poll() is None:
        elapsed = time.monotonic() - t0
        current_cache = byte_size(CACHE)
        current_settings = byte_size(SETTINGS)
        growth = max(0, current_cache - baseline_cache) + max(0, current_settings - baseline_settings) + LOG.stat().st_size
        free = shutil.disk_usage("C:/").free
        remaining = max(0, CAP - growth)
        if elapsed >= TIME_CAP:
            stop_reason = "existing720srunbound"
        elif growth > CAP:
            stop_reason = "additional1.5GiBallocationbound"
        elif free - remaining < RESERVE:
            stop_reason = "3GiBreserveafterremainingestimate"
        if elapsed - last >= 30 or stop_reason:
            last = elapsed
            sample = {"elapsed_seconds": round(elapsed, 2), "owned_pid": process.pid,
                      "cache_bytes": current_cache, "attributed_growth_bytes": growth,
                      "C_free_bytes": free, "remaining_estimate_bytes": remaining,
                      "stop_reason": stop_reason}
            samples.append(sample)
            print(json.dumps(sample), flush=True)
        if stop_reason:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=15)
            break
        time.sleep(5)
text = LOG.read_text(encoding="utf-8", errors="replace")
errors = [l for l in text.splitlines() if any(w in l for w in ["ERROR:", "SCRIPT ERROR", "Parse Error", "Compile Error", "Error importing", "Cannot load resource"])]
final_cache = byte_size(CACHE)
result = "PASS" if process.returncode == 0 and not errors and not stop_reason else "FAIL"
record = {"started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(),
          "command": command, "engine_version": version, "engine_sha256": sha(ENGINE),
          "owned_pid": process.pid, "exit_code": process.returncode, "result": result,
          "stop_reason": stop_reason, "time_cap_seconds": TIME_CAP, "elapsed_seconds": round(time.monotonic()-t0, 2),
          "additional_C_cap_bytes": CAP, "minimum_reserve_bytes": RESERVE,
          "initial_cache_bytes": baseline_cache, "final_cache_bytes": final_cache,
          "cache_growth_bytes": final_cache-baseline_cache, "C_free_bytes": shutil.disk_usage("C:/").free,
          "H_free_bytes": shutil.disk_usage("H:/").free, "samples": samples, "errors": errors,
          "log_path": LOG.relative_to(ROOT).as_posix(), "log_sha256": sha(LOG),
          "preflight_sha256": sha(preflight), "runner_sha256": sha(Path(__file__)), "sources": pre["sources"],
          "source_bindings_still_match": all(sha(ROOT/x["path"])==x["sha256"] for x in pre["sources"]),
          "previous4failedattempts_preserved": pre["prior_attempts"], "slot": "RELEASED_TERMINAL",
          "no_automatic_next_heavy_job": True,
          "meaning": "Single granted import result only; no full trusted suite, visual/action4.6, device, child or owner acceptance."}
with RECEIPT.open("x", encoding="utf-8", newline="\n") as out:
    json.dump(record, out, indent=2)
    out.write("\n")
print(json.dumps({k:record[k] for k in ["result","owned_pid","exit_code","elapsed_seconds","stop_reason","cache_growth_bytes","source_bindings_still_match","slot"]}), flush=True)
print(json.dumps({"receipt_sha256":sha(RECEIPT),"error_count":len(errors)}), flush=True)
sys.exit(0 if result=="PASS" else 1)
