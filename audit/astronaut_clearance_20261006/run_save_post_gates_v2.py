from pathlib import Path
from datetime import datetime, timezone
import subprocess,json,hashlib,time
root=Path(__file__).resolve().parents[2]; packet=Path(__file__).resolve().parent
engine=Path("C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=["scripts/opera_astronaut_surface.gd","scripts/opera_career_world_2d.gd","scripts/save_state.gd","scripts/probe_opera_gesture_quality.gd"]
bound=[{"path":n,"sha256":sha(root/n)} for n in files]
log=packet/"SAVE_POST_GATES_V2_LOG.txt"; receipt=packet/"SAVE_POST_GATES_V2_RECEIPT.json"
preflight=packet/"SAVE_POST_GATES_V2_PREFLIGHT.json"
assert not log.exists() and not receipt.exists() and not preflight.exists()
version=subprocess.check_output([str(engine),"--version"],text=True).strip()
assert version=="4.7.2.stable.official.ed1daf0bf"
preflight.write_text(json.dumps({"sources":bound,"runner_sha256":sha(Path(__file__)),"engine_version":version,"engine_sha256":sha(engine),"scope":"Four current-source analyzer gates and trusted gesture check; no import/capture; total150s bound."},indent=2)+"\n")
start=time.monotonic()
commands=[[str(engine),"--headless","--path",str(root),"--check-only","--script","res://"+n] for n in files]
commands.append([str(engine),"--headless","--path",str(root),"--script","res://scripts/probe_opera_gesture_quality.gd"])
results=[];started=datetime.now(timezone.utc).isoformat()
with log.open("xb") as output:
 for command in commands:
  r=subprocess.run(command,cwd=root,capture_output=True,timeout=min(90,max(1,150-(time.monotonic()-start))))
  out=(r.stdout+r.stderr).decode("utf-8",errors="replace")
  output.write(("COMMAND "+json.dumps(command)+"\n"+out+"\n").encode());output.flush()
  errors=[l for l in out.splitlines() if any(x in l for x in ["ERROR:","SCRIPT ERROR","Parse Error","Compile Error"])]
  summary=[l for l in out.splitlines() if "GESTURE_QUALITY|result:" in l]
  value={"command":command,"exit_code":r.returncode,"errors":errors,"summary":summary,"result":"PASS" if r.returncode==0 and not errors else "FAIL"}
  results.append(value);print(json.dumps(value),flush=True)
value={"started_utc":started,"finished_utc":datetime.now(timezone.utc).isoformat(),"results":results,"result":"PASS" if all(r["result"]=="PASS" for r in results) else "FAIL","engine_version":subprocess.check_output([str(engine),"--version"],text=True).strip(),"engine_sha256":sha(engine),"sources":bound,"source_bindings_match":all(sha(root / s["path"])==s["sha256"] for s in bound),"log_sha256":sha(log),"preflight_sha256":sha(preflight),"scope":"Current save-repair four-script Godot analyzer and existing 305-check gesture gate only. Full CI/native/device/child/owner acceptance pending."}
receipt.write_text(json.dumps(value,indent=2)+"\n");print(json.dumps({"result":value["result"],"receipt_sha256":sha(receipt)}),flush=True)
raise SystemExit(0 if value["result"]=="PASS" else 1)
