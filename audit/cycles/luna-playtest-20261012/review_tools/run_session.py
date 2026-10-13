"""Retain one unchanged Godot probe invocation, with an isolated save profile.
This measures scripted assertions, not an autonomous GUI/child play session.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, time
ROOT = Path(__file__).resolve().parents[4]
CYCLE = ROOT / 'audit/cycles/luna-playtest-20261012'
FAILURE_RE = r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error'
HYBRID = {'probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def write(path,value): path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument('session'); p.add_argument('--attempt',type=int,default=1); p.add_argument('--godot'); a=p.parse_args()
 matrix=json.loads((CYCLE/'matrix.json').read_text(encoding='utf-8')); row=next((r for r in matrix['sessions'] if r['id']==a.session),None)
 if row is None or a.attempt not in (1,2): raise ValueError('Unknown session or unsupported attempt')
 out=CYCLE/'runtime'/a.session/f'attempt_{a.attempt}'; out.mkdir(parents=True,exist_ok=True)
 receipt=out/'receipt.json'; log=out/'probe.log'
 if receipt.exists() or log.exists(): raise ValueError('Preserve prior evidence: this attempt already exists')
 config=ROOT/'tmp/luna_local_config.json'; explicit=a.godot or os.environ.get('LUNA_GODOT')
 if not explicit and config.exists(): explicit=json.loads(config.read_text())['godot']
 resolver=[sys.executable,'-X','utf8','-B','tools/resolve_godot.py']+(['--godot',explicit] if explicit else [])
 resolved=subprocess.run(resolver,cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
 if resolved.returncode: raise RuntimeError(resolved.stderr)
 engine=Path(resolved.stdout.strip()); version=subprocess.check_output([str(engine),'--version'],text=True,encoding='utf-8').strip()
 baseline=json.loads((ROOT/'tools/godot_baseline.json').read_text())
 if version != '4.7.2.stable.official.ed1daf0bf': raise ValueError('Approved exact engine required: '+version)
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 if head != matrix['baseline']: raise ValueError('Study frozen source HEAD differs; do not silently reinterpret evidence')
 profile=Path(tempfile.mkdtemp(prefix='reef-luna-'+a.session+'-'))
 env=os.environ.copy()
 for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
  target=profile/name; target.mkdir(); env[key]=str(target)
 env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 mode='--hybrid-touch-test' if row['probe'] in HYBRID else '--classic-touch-test'
 cmd=[str(engine),'--headless','--path',str(ROOT),'-s','scripts/'+row['probe']+'.gd','--','--touch',mode]
 tracked=['project.godot', 'scenes/main.tscn', 'scripts/ci.sh', 'scripts/'+row['probe']+'.gd',row['source']]
 data={'schema':'luna_probe_receipt/1','session_id':a.session,'attempt':a.attempt,'baseline':head,'focus':row['focus'],'probe':row['probe'],'command':cmd,'started_utc':now(),'status':'RUNNING','evidence_kind':'SCRIPTED_PROBE','engine':{'version':version,'sha256':sha(engine)},'source_hashes':{x:sha(ROOT/x) for x in tracked},'helper_sha256':sha(Path(__file__)),'save_profile':str(profile),'profile_isolated':True,'headless':True,'rendered_mobile_acceptance':False,'log':log.relative_to(ROOT).as_posix(),'wall_clock_is_gameplay_timing':False}
 write(receipt,data); start=time.monotonic(); timed_out=False
 with log.open('w',encoding='utf-8',newline='\n') as f:
  process=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
  try: code=process.wait(timeout=480)
  except subprocess.TimeoutExpired:
   timed_out=True; process.kill(); code=process.wait(); f.write('\nLUNA_RUNNER|TIMEOUT|480 seconds\n')
 raw=log.read_text(encoding='utf-8',errors='replace')
 failure_lines=[line for line in raw.splitlines() if re.search(FAILURE_RE,line)]
 terminal=[line for line in raw.splitlines() if re.search(r'ALL OK|ALL .*CLEAR|RESULT|DONE|checks.*fail',line,re.I)]
 data.update(finished_utc=now(),wall_elapsed_seconds=round(time.monotonic()-start,3),exit_code=code,timed_out=timed_out,status='PASS' if code==0 and not failure_lines and len(raw.splitlines())>1 else 'FAIL',failure_lines=failure_lines,terminal_lines=terminal[-15:],log_sha256=sha(log),log_bytes=log.stat().st_size)
 write(receipt,data)
 print(json.dumps({'session_id':a.session,'status':data['status'],'probe':row['probe'],'receipt':receipt.relative_to(ROOT).as_posix(),'failures':failure_lines[:8],'wall_seconds':data['wall_elapsed_seconds']},ensure_ascii=False))
 return 0 if data['status']=='PASS' else 1
if __name__=='__main__': sys.exit(main())
