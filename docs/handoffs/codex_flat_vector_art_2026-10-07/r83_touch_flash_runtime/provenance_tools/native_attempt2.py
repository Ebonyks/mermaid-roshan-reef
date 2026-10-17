from pathlib import Path
import os,json,datetime,subprocess,hashlib
T=Path.cwd();S=Path(__file__).parent;R=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef');H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime'
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
assert(S/'NATIVE_QUEUE_RESULT.json').is_file()and json.loads((S/'NATIVE_QUEUE_RESULT.json').read_text())['status']=='FAIL'
assert json.loads((S/'IMPORT_EOL_BINDING.json').read_text())['all_differences_exact_CRLF_to_LF_only']
assert not(S/'NATIVE_ATTEMPT2_LAUNCH.json').exists();wr(S/'NATIVE_ATTEMPT2_LAUNCH.json',{'pid':os.getpid(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':'SOURCE_POST_IMPORT_PIN.json','reason':'First attempt terminal in preflight, no Godot/Main/capture. Exact sidecar-only CRLF/LF binding preserved; current exact raw pin separate.'})
pre=json.loads((H/'r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding='utf-8'));paths=json.loads(next(x['output']for x in pre['checks']if'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip())
env=dict(os.environ,R83_JOB_ROOT=str(S),R83_NORMAL_PATH=paths['normal_path'],R83_PIN_FILE='SOURCE_POST_IMPORT_PIN.json',R83_ATTEMPT='2',PYTHONUTF8='1',PYTHONIOENCODING='utf-8');rows=[]
for width in [1280,1600]:
 logfile=S/('attempt2_native_'+str(width)+'_driver.log');cmd=['python','-B',str(P/'run_native.py'),str(width)];print('R83_ATTEMPT2_BEGIN',width,flush=True)
 with logfile.open('wb')as log:q=subprocess.run(cmd,cwd=T,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
 rows.append({'width':width,'exit_code':q.returncode,'driver_log_sha256':hashlib.sha256(logfile.read_bytes()).hexdigest()});print('R83_ATTEMPT2_DONE',width,q.returncode,flush=True)
 if q.returncode:break
wr(S/'NATIVE_ATTEMPT2_RESULT.json',{'status':'PASS'if len(rows)==2 and all(x['exit_code']==0 for x in rows)else'FAIL','cases':rows,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
assert len(rows)==2 and all(x['exit_code']==0 for x in rows)
