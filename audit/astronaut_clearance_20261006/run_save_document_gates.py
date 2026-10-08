from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib
root=Path(__file__).resolve().parents[2];b=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
python="C:/Users/Peter/AppData/Local/Python/bin/python.exe"
r=subprocess.run(["git","diff","--name-only","96274aab9cebd563b10846a4a48de5d017588563"],cwd=root,capture_output=True,text=True);assert r.returncode==0
files=[n for n in r.stdout.splitlines() if n.endswith(".gd")]
commands=[[python,"-X","utf8","-B","-m","gdtoolkit.parser",*files],[python,"-X","utf8","-B","tools/lint_inference.py",*files],[python,"-X","utf8","-B","tools/audit_document_authority.py"],[python,"-X","utf8","-B","-m","unittest","tools.tests.test_audit_document_authority","tools.tests.test_audit_development"],[python,"-X","utf8","-B","tools/audit_document_authority.py","--stress"],[python,"-X","utf8","-B","tools/audit_game_2d.py","--regression-gate"],[python,"-X","utf8","-B","tools/audit_development.py","--base","auto"]]
receipt=b/"SAVE_DOCUMENT_GATES_RECEIPT.json";log=b/"SAVE_DOCUMENT_GATES_LOG.txt"
record=json.loads(receipt.read_text());assert record["status"]=="PREFLIGHT" and log.stat().st_size==0
record.update({"status":"RUNNING","started_utc":datetime.now(timezone.utc).isoformat(),"sources":[{"path":n,"sha256":sha(root/n)} for n in files+["audit/MASTER_AUDIT_2026-08-09.md","audit/findings/ACTIVE_FINDINGS_2026-08-13.md","design/05_DOC_LEDGER.md"]],"gd_file_count":len(files),"results":[]})
receipt.write_text(json.dumps(record,indent=2)+"\n")
with log.open("ab") as f:
 for cmd in commands:
  r=subprocess.run(cmd,cwd=root,capture_output=True,timeout=180);out=(r.stdout+r.stderr).decode("utf-8",errors="replace");f.write(("COMMAND "+json.dumps(cmd)+"\n"+out+"\n").encode());f.flush()
  item={"command":cmd,"exit_code":r.returncode,"result":"PASS" if r.returncode==0 else "FAIL","summary":out.splitlines()[-7:]};record["results"].append(item);receipt.write_text(json.dumps(record,indent=2)+"\n");print(json.dumps({"command":cmd[4:7],"result":item["result"],"summary":item["summary"]}),flush=True)
record.update({"status":"TERMINAL","finished_utc":datetime.now(timezone.utc).isoformat(),"result":"PASS" if all(x["result"]=="PASS" for x in record["results"]) else "FAIL","source_bindings_match":all(sha(root/x["path"])==x["sha256"] for x in record["sources"]),"log_sha256":sha(log),"scope":"Changed GDScript and canonical document/2D regression/coverage gates only. Full CI, strict zero-3D and visual/device/child/owner acceptance pending."})
receipt.write_text(json.dumps(record,indent=2)+"\n");print(json.dumps({"result":record["result"],"receipt_sha256":sha(receipt)}),flush=True)
raise SystemExit(0 if record["result"]=="PASS" else 1)
