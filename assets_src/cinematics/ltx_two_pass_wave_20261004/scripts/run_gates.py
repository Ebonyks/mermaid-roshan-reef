from pathlib import Path
import subprocess,json,time
p=Path(__file__).resolve().parents[1];r=p.parents[2];rows=[];start=time.monotonic()
commands=[["python","-B","tools/audit_document_authority.py"],["python","-B","tools/audit_development.py","--base","auto"]]
with (p/"environment/project_gates.log").open("w",encoding="utf-8") as log:
 for cmd in commands:
  result=subprocess.run(cmd,cwd=r,capture_output=True,text=True,encoding="utf-8");log.write("COMMAND "+" ".join(cmd)+"\n"+result.stdout+result.stderr+"\n");rows.append({"command":" ".join(cmd),"exit_code":result.returncode,"result":"PASS" if result.returncode==0 else "FAIL"});print(rows[-1],flush=True)
status={"status":"PASS" if all(x["exit_code"]==0 for x in rows) else "FAIL","checks":rows,"elapsed_seconds":round(time.monotonic()-start,3)}
(p/"environment/project_gates.json").write_text(json.dumps(status,indent=2)+"\n");raise SystemExit(0 if status["status"]=="PASS" else 1)
