"""Capture representative live scenes through existing Mobile probes; no input/visual acceptance implied."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,tempfile,time,argparse
ROOT=Path(__file__).resolve().parents[4]; CYCLE=ROOT/'audit/cycles/luna-playtest-20261012'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser(); parser.add_argument('--diagnostic',action='store_true'); parser.add_argument('--burst',action='store_true'); parser.add_argument('--slow',action='store_true'); parser.add_argument('--repeat',action='store_true'); parser.add_argument('--output'); a=parser.parse_args();
 if a.slow and not a.burst: parser.error('--slow requires --burst')
 if a.output and not re.fullmatch(r'[a-z0-9_-]{1,64}',a.output): parser.error('--output must be a simple capture name')
 diagnostic=a.diagnostic or a.burst
 mode='pool_burst_slow' if a.slow else ('pool_burst' if a.burst else ('pool_diagnostic' if a.diagnostic else 'pool'))
 if a.repeat: mode += '_repeat'
 if a.output: mode=a.output
 out=CYCLE/('captures/'+mode); out.mkdir(parents=True,exist_ok=True)
 receipt=out/'receipt.json'; log=out/'capture.log'
 if receipt.exists(): raise ValueError('Preserve prior capture attempt')
 engine=json.loads((ROOT/'tmp/luna_local_config.json').read_text())['godot']; profile=Path(tempfile.mkdtemp(prefix='reef-luna-mobile-capture-')); env=os.environ.copy()
 for key,name in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata')]:
  p=profile/name;p.mkdir();env[key]=str(p)
 env['DAY_ONE_POOL_CAPTURE_OUT']=str(out)
 if a.slow: env['LUNA_TAP_INTERVAL']='1.20'
 probe='audit/cycles/luna-playtest-20261012/review_tools/pool_burst_diagnostic.gd' if a.burst else ('audit/cycles/luna-playtest-20261012/review_tools/pool_diagnostic.gd' if diagnostic else 'scripts/probe_day_one_pool_shots.gd')
 cmd=[engine,'--windowed','--path',str(ROOT),'--rendering-method','mobile','--resolution','1280x720','--audio-driver','Dummy','-s',probe,'--','--touch','--classic-touch-test']
 start=time.monotonic(); data={'schema':'luna_mobile_capture/1','baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'command':cmd,'started_utc':datetime.now(timezone.utc).isoformat(),'status':'RUNNING','probe_sha256':sha(ROOT/probe),'base_probe_sha256':sha(ROOT/'scripts/probe_day_one_pool_shots.gd'),'diagnostic':diagnostic,'story_clip_cancellation':diagnostic,'mode':mode,'declared_tap_interval_seconds':1.20 if a.slow else (0.30 if a.burst else None),'engine_sha256':sha(Path(engine)),'save_profile_isolated':True,'audio':'Dummy; not listening evidence','route_limit':'Existing fixture opens room/restores state directly; captured compositions only, not fresh-save navigation or child touch/fun proof.'}; receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 with log.open('w',encoding='utf-8',newline='\n') as f:
  run=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
  try: code=run.wait(timeout=240)
  except subprocess.TimeoutExpired: run.kill();code=run.wait()
 data.update(exit_code=code,status='CAPTURED_PENDING_VISUAL_REVIEW' if code==0 else 'FAIL',wall_seconds=round(time.monotonic()-start,3),log_sha256=sha(log),files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.glob('*.png'))]); receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':data['status'],'exit_code':code,'captures':len(data['files']),'tail':log.read_text(errors='replace').splitlines()[-5:]})); return code
if __name__=='__main__': raise SystemExit(main())
