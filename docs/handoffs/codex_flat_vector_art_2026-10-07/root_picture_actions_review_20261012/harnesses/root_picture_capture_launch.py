from pathlib import Path
import json,hashlib,subprocess,os,datetime,sys
sys.stdout.reconfigure(encoding="utf-8")
r=Path(r"C:\Users\Peter\.codex\worktrees\flat-vector-art-audit-20261007\mermaid-roshan-reef")
p=Path(__file__).parent
h=p/sys.argv[1]
rev=subprocess.check_output(["git","rev-parse","HEAD"],cwd=r,text=True).strip()
paths=[r/"project.godot",r/"tools/godot_baseline.json"]
for folder in ["assets","scripts","scenes","shaders"]:
 paths.extend(f for f in (r/folder).rglob("*") if f.is_file())
rows=[{"path":f.relative_to(r).as_posix(),"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"bytes":f.stat().st_size} for f in sorted(paths)]
run=p/(sys.argv[2]+"_"+datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S"))
pre={"schema":1,"source_revision":rev,"files":rows,"file_count":len(rows),"scope":"All regular files below assets/scripts/scenes/shaders plus project.godot and engine baseline; not independent proof of every active dependency.","harness_sha256":hashlib.sha256(h.read_bytes()).hexdigest(),"recorded_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
(p/(run.name+"_source_before.json")).write_text(json.dumps(pre,indent=2)+"\n",encoding="utf-8",newline="\n")
env=os.environ.copy();env["ROOTPIC_OUT"]=str(run);env["ROOTPIC_REV"]=rev
cmd=[r"C:\Users\Peter\AppData\Local\Programs\MermaidReefTools\Godot\4.7.2\godot_console.exe","--path",str(r),"--rendering-method","mobile","--audio-driver","Dummy","--windowed","--position","-2400,0","-s",str(h)]
print("CAPTURE_OUTPUT",run,flush=True)
try:
 result=subprocess.run(cmd,cwd=r,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace",creationflags=subprocess.CREATE_NO_WINDOW,timeout=160)
 output=result.stdout;returncode=result.returncode
except subprocess.TimeoutExpired as error:
 output=error.stdout or b"";output=output.decode("utf-8",errors="replace") if isinstance(output,bytes) else output
 returncode=124
(p/(run.name+"_capture.log")).write_text(output,encoding="utf-8",newline="\n")
changed=[x["path"] for x in rows if not (r/x["path"]).is_file() or hashlib.sha256((r/x["path"]).read_bytes()).hexdigest()!=x["sha256"]]
receipt={"schema":1,"source_revision":rev,"command":cmd,"returncode":returncode,"runtime_source_file_count":len(rows),"changed_runtime_sources":changed,"harness_sha256":pre["harness_sha256"],"output":str(run),"log":run.name+"_capture.log","recorded_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Diagnostic context only; no replacement or acceptance."}
(p/(run.name+"_receipt.json")).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8",newline="\n")
for line in output.splitlines():
 if line.startswith("ROOTPIC|") or any(t in line for t in ["SCRIPT ERROR","ERROR:","Vulkan","Godot Engine"]):print(line)
print("SOURCE_PRESERVATION",len(changed)==0,"EXIT",returncode,flush=True)
sys.exit(0 if returncode==0 and not changed else 1)
