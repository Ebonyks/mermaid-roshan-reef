from pathlib import Path
import subprocess,json,hashlib,datetime,time,os
S=Path(__file__).parent;R=Path.cwd()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
bash=Path(r"C:\Program Files\Git\bin\bash.exe");assert bash.is_file()
script=S/"current_ci_static_prefix.sh";start=now();t=time.monotonic()
wr(S/"STATIC_LAUNCH.json",{"started_at_utc":start,"method":"Exact scripts/ci.sh static prefix; only working-directory expression replaced with actual owned worktree. No importer/probe restart.","script_sha256":sha(script),"repo_ci_sha256":sha(R/"scripts/ci.sh"),"HEAD":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"MERGE_HEAD":subprocess.check_output(["git","rev-parse","MERGE_HEAD"],text=True).strip(),"supersedes_stale_static_reuse_field_in_probe_LAUNCH":True})
with(S/"STATIC_PREFIX.log").open("wb") as log:
 q=subprocess.run([str(bash),str(script)],cwd=R,env=dict(os.environ,PYTHONUTF8="1",PYTHONIOENCODING="utf-8"),stdout=log,stderr=subprocess.STDOUT,timeout=5400)
txt=(S/"STATIC_PREFIX.log").read_text(encoding="utf-8",errors="replace")
passed=q.returncode==0 and "R100_STATIC_PREFIX_ALL_OK" in txt
wr(S/"STATIC_RESULT.json",{"status":"PASS"if passed else"FAIL","exit_code":q.returncode,"started_at_utc":start,"completed_at_utc":now(),"elapsed_seconds":round(time.monotonic()-t,3),"log_sha256":sha(S/"STATIC_PREFIX.log"),"repo_ci_sha256":sha(R/"scripts/ci.sh"),"correction":"The trusted-probe LAUNCH static_reuse text was inherited from a prior validator and incorrectly said no audio/assets changed. This exact current-source prefix separately validates incoming Opera assets/audio and supersedes that field. Historical raw LAUNCH remains unchanged.","acceptance":"Machine lane only; no visual/device/child/owner acceptance."})
print("R100_STATIC_PREFIX",q.returncode,"PASS"if passed else"FAIL",flush=True)
assert passed
