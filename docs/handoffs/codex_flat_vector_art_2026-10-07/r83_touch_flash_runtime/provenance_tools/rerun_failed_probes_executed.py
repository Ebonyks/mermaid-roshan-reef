from pathlib import Path
import subprocess,json,hashlib,os,datetime,time,re,shutil
T=Path.cwd();S=Path(__file__).parent;P=T/'docs/handoffs/codex_flat_vector_art_2026-10-07/r83_touch_flash_runtime';O=P/'focused_after_suite_failures';O.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
pin=json.loads((S/'SOURCE_POST_IMPORT_PIN.json').read_text(encoding='utf-8'));assert all(sha(T/p)==v for p,v in pin['runtime_hashes'].items())
old=json.loads((S/'FULL_CI_RESULT.json').read_text());bad=[x for x in old['probe_exits']if x['exit_code']!=0];assert bad==[{'probe':'probe_melody','exit_code':127},{'probe':'probe_l2_living_cards','exit_code':127}],bad
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],text=True).strip();R=Path('C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef');pre=json.loads((R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding='utf-8'));normal=Path(json.loads(next(x['output']for x in pre['checks']if'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip())['normal_path'])
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else'absent'for x in pin['normal_save_hashes_before']}
before=normals();rows=[]
for item in bad:
 name=item['probe'];job=S/('focused_'+name);job.mkdir(exist_ok=False);out=O/name;out.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 for key,sub in [('APPDATA','roaming'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:env[key]=str(job/sub);Path(env[key]).mkdir()
 cmd=[G,'--headless','-s','scripts/'+name+'.gd','--','--touch','--classic-touch-test'];start=time.monotonic();print('R83_FOCUSED_BEGIN',name,flush=True)
 with(out/'engine.log').open('wb')as log:
  try:q=subprocess.run(cmd,cwd=T,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=480);code=q.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 raw=(out/'engine.log').read_bytes();text=raw.decode(errors='replace');row={'probe':name,'command':cmd,'exit_code':code,'timed_out':timed,'elapsed_seconds':round(time.monotonic()-start,3),'log_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':sha(T/('scripts/'+name+'.gd')),'runtime_pin_sha256':sha(S/'SOURCE_POST_IMPORT_PIN.json'),'error_or_FAIL':bool(re.search(r'SCRIPT ERROR|SHADER ERROR|Parse Error|Compile Error|(?m:^ERROR:)|\bFAIL\b',text)),'has_positive_verdict':'ALL OK'in text,'normal_before':before,'normal_after':normals(),'source_pin_exact':all(sha(T/p)==v for p,v in pin['runtime_hashes'].items()),'scope':'Original trusted source/mode, direct native Python launcher instead of MSYS timeout; focused diagnostic only, not a clean full-suite claim.'};wr(out/'RESULT.json',row);rows.append(row);print('R83_FOCUSED_DONE',name,code,'positive',row['has_positive_verdict'],'\n'+text[-800:],flush=True)
 if code!=0 or timed or row['error_or_FAIL']or not row['has_positive_verdict']:break
result={'status':'PASS_FOCUSED_ONLY'if len(rows)==2 and all(x['exit_code']==0 and x['source_pin_exact']and x['normal_before']==x['normal_after']for x in rows)else'FAIL','original_full_suite_exit_code':old['exit_code'],'original_nonzero_probes':bad,'reruns':rows,'original_failures_preserved':True,'root_cause':'UNKNOWN; both original127exits had only engine banner/no assertion verdict. Do not infer infrastructure or application cause from reruns.','clean_full_suite_required':True,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};wr(O/'SUMMARY.json',result);wr(S/'FOCUSED_RESULT.json',result);assert result['status']=='PASS_FOCUSED_ONLY'
