from pathlib import Path
import json,subprocess,hashlib,datetime,os
packet=Path(__file__).resolve().parent
r=Path(subprocess.check_output(["git","rev-parse","--show-toplevel"],cwd=packet,text=True).strip());stage=r/"tmp/flat-vector-castle-dayone-recapture";stage.mkdir(parents=True,exist_ok=True)
exe="C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe"
script=packet/"capture_castle.gd"
head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=r,text=True).strip()
run_id=datetime.datetime.now(datetime.timezone.utc).strftime("run-%Y%m%dT%H%M%S")
records=[]
for case in (os.environ["LIVE3_ONLY"].split(",") if os.environ.get("LIVE3_ONLY") else ["castle","bathroom","pool"]):
 script=packet/("capture_"+case+".gd")
 for aspect in ["1280x720","1600x720"]:
  name=run_id+"-"+case+"-"+aspect;out=stage/name;log=stage/(name+".log")
  env=os.environ.copy();env.update(LIVE3_CASE=case,LIVE3_ASPECT=aspect,LIVE3_OUT=out.as_posix(),GITHUB_SHA=head)
  cmd=[exe,"--path",str(r),"--rendering-method","mobile","--audio-driver","Dummy","--windowed","--position","-2400,0","-s",str(script)]
  startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
  rec={"case":case,"aspect":aspect,"source_revision":head,"harness_sha256":hashlib.sha256(script.read_bytes()).hexdigest(),"command":cmd,"out":out.as_posix(),"log":log.as_posix(),"started_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
  with log.open("wb") as f:
   proc=subprocess.Popen(cmd,cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,startupinfo=startup,creationflags=subprocess.CREATE_NO_WINDOW)
   rec["pid"]=proc.pid;records.append(rec)
   (stage/(run_id+"-launch.json")).write_text(json.dumps(records,indent=2)+"\n",encoding="utf8",newline="\n")
   print("RUNNING",case,aspect,"PID",proc.pid,flush=True)
   try:rec["exit_code"]=proc.wait(timeout=300)
   except subprocess.TimeoutExpired:
    proc.terminate();proc.wait();rec["exit_code"]="TIMEOUT"
  rec["ended_at_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
  (stage/(run_id+"-launch.json")).write_text(json.dumps(records,indent=2)+"\n",encoding="utf8",newline="\n")
  print("FINISHED",case,aspect,"EXIT",rec["exit_code"],log.read_bytes()[-1800:].decode("utf8",errors="replace"),flush=True)
  text=log.read_bytes().decode("utf8",errors="replace")
  if rec["exit_code"]!=0 or "SCRIPT ERROR" in text or "|FAIL|" in text or "ERROR:" in text:raise SystemExit(1)
  manifest=json.loads((out/"capture_manifest.json").read_text(encoding="utf8"))
  expected=json.loads((packet/"EXPECTED_MATRIX.json").read_text(encoding="utf8"))[case]
  assert manifest["result"]=="PASS" and manifest["expected_ids"]==expected
  assert [x["id"] for x in manifest["states"]]==expected
  for row in manifest["states"]:
   image=out/row["image"]["file"];assert row["status"]=="PASS" and image.stat().st_size==row["image"]["bytes"] and hashlib.sha256(image.read_bytes()).hexdigest()==row["image"]["sha256"]
  normal=manifest["save_isolation"]["normal_save_file"]
  parent_after={suffix:hashlib.sha256(Path(normal+suffix).read_bytes()).hexdigest() if Path(normal+suffix).is_file() else "absent" for suffix in manifest["save_isolation"]["before"]}
  assert parent_after==manifest["save_isolation"]["before"]
  rec["parent_normal_save_unchanged_after_exit"]=True
  (stage/(run_id+"-launch.json")).write_text(json.dumps(records,indent=2)+"\n",encoding="utf8",newline="\n")
print("LIVE3 SELECTED CAPTURE RUNS PASS", len(records), run_id,flush=True)
