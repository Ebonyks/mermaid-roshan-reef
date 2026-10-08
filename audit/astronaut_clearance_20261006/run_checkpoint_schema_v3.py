from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,time
root=Path(__file__).resolve().parents[2];packet=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
engine=Path("C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe")
files=["scripts/opera_astronaut_surface.gd","scripts/opera_career_world_2d.gd","scripts/save_state.gd","audit/astronaut_clearance_20261006/verify_checkpoint_schema_v3.gd","tmp/astronaut_partial_save_repair_20261006/reef_save.json"]
log=packet/"CHECKPOINT_SCHEMA_V3_LOG.txt";receipt=packet/"CHECKPOINT_SCHEMA_V3_RECEIPT.json"
assert not log.exists() and not receipt.exists()
record={"started_utc":datetime.now(timezone.utc).isoformat(),"sources":[{"path":n,"sha256":sha(root/n)} for n in files],"engine_sha256":sha(engine),"status":"RUNNING","scope":"Schema/corruption/context unit checks with actual genuine source save; no native or naturally reached tutorial/birthday acceptance."}
receipt.write_text(json.dumps(record,indent=2)+"\n")
command=[str(engine),"--headless","--path",str(root),"--script","res://audit/astronaut_clearance_20261006/verify_checkpoint_schema_v3.gd"]
t=time.monotonic();r=subprocess.run(command,cwd=root,capture_output=True,timeout=90)
output=(r.stdout+r.stderr).decode("utf-8",errors="replace");log.write_text(output,encoding="utf-8")
errors=[l for l in output.splitlines() if any(x in l for x in ["ERROR:","SCRIPT ERROR","Parse Error","Compile Error"])]
evidence=[json.loads(l.split("|",1)[1]) for l in output.splitlines() if l.startswith("ASTRO_SCHEMA_RESULT|")]
record.update({"command":command,"finished_utc":datetime.now(timezone.utc).isoformat(),"elapsed_seconds":round(time.monotonic()-t,2),"exit_code":r.returncode,"errors":errors,"evidence":evidence,"log_sha256":sha(log),"source_bindings_match":all(sha(root/s["path"])==s["sha256"] for s in record["sources"]),"result":"PASS" if r.returncode==0 and not errors and evidence and not evidence[0]["failures"] else "FAIL","status":"TERMINAL"})
receipt.write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps({"result":record["result"],"checks":evidence[0]["checks"] if evidence else 0,"errors":errors[:5],"failures":[x for e in evidence for x in e["rows"] if not x["pass"]],"receipt_sha256":sha(receipt)}),flush=True)
raise SystemExit(0 if record["result"]=="PASS" else 1)
