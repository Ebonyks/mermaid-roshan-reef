"""Run the unchanged required full CI with preserved local evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,shlex,subprocess,sys,time,tempfile
ROOT=Path(__file__).resolve().parents[4]; CYCLE=ROOT/'audit/cycles/luna-playtest-20261012'
def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 output=CYCLE/'verification'; output.mkdir(exist_ok=True)
 log=output/'full_ci_clean.log'; receipt=output/'full_ci_clean_receipt.json'
 if receipt.exists(): raise ValueError('Preserve original evidence; use a named new revision for another gate')
 cfg=json.loads((ROOT/'tmp/luna_local_config.json').read_text()); engine=cfg['godot']
 wrapper=ROOT/'tmp/luna_full_ci_clean.sh'
 # Git Bash Python shim selects existing Python with project dependencies.
 py=Path(sys.executable).as_posix(); cwd=ROOT.as_posix()
 text='#!/usr/bin/env bash\nset -uo pipefail\ncd '+shlex.quote(cwd)+'\nexport PYTHONUTF8=1 PYTHONIOENCODING=utf-8\npython3() { '+shlex.quote(py)+' -X utf8 -B "$@"; }\nexport -f python3\nexport GODOT='+shlex.quote(engine)+'\nexport TMPDIR='+shlex.quote(Path(os.environ['TEMP']).as_posix())+'\nbash --noprofile --norc scripts/ci.sh\nexit "$?"\n'
 wrapper.write_text(text,encoding='utf-8',newline='\n')
 roster=re.search(r'for p in (.+?); do',(ROOT/'scripts/ci.sh').read_text()).group(1).split()
 source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 data={'schema':'luna_full_ci_receipt/1','baseline':source,'status':'RUNNING','started_utc':now(),'command':['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc',str(wrapper)],'ci_sha256':sha(ROOT/'scripts/ci.sh'),'engine_version':subprocess.check_output([engine,'--version'],text=True).strip(),'engine_sha256':sha(Path(engine)),'expected_roster':roster,'wrapper_sha256':sha(wrapper),'helper_sha256':sha(Path(__file__)),'log':'audit/cycles/luna-playtest-20261012/verification/full_ci_clean.log','gates_unchanged':True,'acceptance_scope':'Full local machine regression only; no Mobile/device/child/owner acceptance'}
 profile=Path(tempfile.mkdtemp(prefix='reef-luna-full-ci-clean-')); env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'}
 for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata')]:
  p=profile/name;p.mkdir();env[key]=str(p)
 data['parent_editor_profile']=str(profile);data['parent_editor_profile_isolated']=True;data['environment_difference']='Only editor APPDATA/LOCALAPPDATA isolated; existing CI commands/gates unchanged. Per-probe isolation remains original scripts/ci.sh.'
 receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8'); start=time.monotonic()
 with log.open('w',encoding='utf-8',newline='\n') as f:
  run=subprocess.run(data['command'],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,env=env)
 raw=log.read_text(encoding='utf-8',errors='replace'); observed=re.findall(r'^=== (probe_\w+) ===$',raw,re.M)
 exits=[{'probe':name,'exit_code':int(code)} for name,code in re.findall(r'^PROBE (probe_\w+) process exit: (\d+)',raw,re.M)]
 data.update(finished_utc=now(),wall_seconds=round(time.monotonic()-start,3),exit_code=run.returncode,status='PASS' if run.returncode==0 and observed==roster else 'FAIL',observed_roster=observed,probe_exits=exits,log_sha256=sha(log),failure_lines=[x for x in raw.splitlines() if re.search(r'^PROBE .*reported a failure|\|FAIL\||FAIL .*issue|Parse Error|Compile Error|^.*FAIL.*$',x)][-80:])
 receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':data['status'],'exit_code':run.returncode,'trusted_probes_executed':len(observed),'failures':data['failure_lines'][-12:]})); return run.returncode
if __name__=='__main__': sys.exit(main())
