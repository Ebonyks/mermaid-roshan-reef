from pathlib import Path
import os,hashlib,json,subprocess,time
r=Path.cwd();f=r/'audit/day_one_pool_live_refinement_v2_20261001/probe_completion_timing_v1';e=os.environ.copy()
for k,n in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:
 p=r/'tmp/pool_probe_phase_diagnostic_v1'/n;p.mkdir(parents=True,exist_ok=True);e[k]=str(p)
cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe','--headless','--path',str(r),'-s','res://audit/day_one_pool_live_refinement_v2_20261001/probe_completion_timing_v1/diagnostic_unchanged_checks.gd','--','--touch','--classic-touch-test'];t=time.monotonic()
with (f/'stdout.log').open('wb') as o,(f/'stderr.log').open('wb') as err:q=subprocess.run(cmd,cwd=r,env=e,stdout=o,stderr=err)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(f/'RECEIPT.json').write_text(json.dumps({'status':'DIAGNOSTIC_ONLY_UNCHANGED_CHECKS','exit':q.returncode,'command':cmd,'seconds':time.monotonic()-t,'original_probe_sha256':sha(r/'scripts/probe_day_one_pool_cleanup.gd'),'copy_sha256':sha(f/'diagnostic_unchanged_checks.gd'),'difference':'One extra state print immediately after the existing0.72s wait; every check and deadline unchanged. Not a trusted run or a repair.'},indent=2)+'\n',encoding='utf-8')
t=(f/'stdout.log').read_text();print('\n'.join(x for x in t.splitlines() if 'POOL_PHASE_TIMING|' in x or ': FAIL' in x or '|RESULT:' in x))
