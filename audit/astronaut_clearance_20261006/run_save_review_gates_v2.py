from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib
root=Path(__file__).resolve().parents[2];b=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
python="C:/Users/Peter/AppData/Local/Python/bin/python.exe"
commands=[[python,"-X","utf8","-B","tools/audit_document_authority.py"],[python,"-X","utf8","-B","tools/audit_game_2d.py","--regression-gate"],[python,"-X","utf8","-B","tools/audit_development.py","--base","auto"]]
receipt=b/"SAVE_REVIEW_GATES_V2_RECEIPT.json";log=b/"SAVE_REVIEW_GATES_V2_LOG.txt";record=json.loads(receipt.read_text());assert record["status"]=="PREFLIGHT" and log.stat().st_size==0
files=["scripts/opera_astronaut_surface.gd","scripts/opera_career_world_2d.gd","scripts/save_state.gd","scripts/probe_opera_gesture_quality.gd","audit/MASTER_AUDIT_2026-08-09.md","audit/findings/ACTIVE_FINDINGS_2026-08-13.md","design/05_DOC_LEDGER.md"]
record.update({"status":"RUNNING","started_utc":datetime.now(timezone.utc).isoformat(),"sources":[{"path":n,"sha256":sha(root/n)} for n in files],"results":[]});receipt.write_text(json.dumps(record,indent=2)+"\n")
with log.open("ab") as f:
 for cmd in commands:
  r=subprocess.run(cmd,cwd=root,capture_output=True,timeout=180);out=(r.stdout+r.stderr).decode("utf-8",errors="replace");f.write(("COMMAND "+json.dumps(cmd)+"\n"+out+"\n").encode());f.flush();item={"command":cmd,"exit_code":r.returncode,"result":"PASS" if r.returncode==0 else "FAIL","summary":out.splitlines()[-7:]};record["results"].append(item);receipt.write_text(json.dumps(record,indent=2)+"\n");print(json.dumps({"command":cmd[4:],"result":item["result"],"summary":item["summary"]}),flush=True)
record.update({"status":"TERMINAL","finished_utc":datetime.now(timezone.utc).isoformat(),"result":"PASS" if all(x["result"]=="PASS" for x in record["results"]) else "FAIL","source_bindings_match":all(sha(root/x["path"])==x["sha256"] for x in record["sources"]),"log_sha256":sha(log),"scope":"Recheck corrected audit facts, exact coverage and unchanged2D classifier. Prior parser/lint/54unit/6stress still source-current; fullCI/native/device/child/owner pending."});receipt.write_text(json.dumps(record,indent=2)+"\n");print(json.dumps({"result":record["result"],"receipt_sha256":sha(receipt)}),flush=True);raise SystemExit(0 if record["result"]=="PASS" else 1)
