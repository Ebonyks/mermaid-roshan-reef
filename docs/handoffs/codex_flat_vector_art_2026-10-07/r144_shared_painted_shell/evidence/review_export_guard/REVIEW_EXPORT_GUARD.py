from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,os,sys,re,datetime
W=Path.cwd();T=Path(__file__).parent;D=T/'review_export_guard';assert not D.exists(),'Resume existing guarded import operation';D.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
wr=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
full=json.loads((T/'validation/FINAL_RESULT.json').read_text(encoding='utf-8-sig'));assert full['state']=='PASS_ACTUAL_R144_STATIC_IMPORT_ANALYZERS_AND82_STRICT_COMMAND_EXITS'
F=W/'docs/handoffs/codex_flat_vector_art_2026-10-07/r144_shared_painted_shell';assert(F/'.gdignore').is_file()and(F/'.gdignore').stat().st_size==0
assert not list(F.rglob('*.import'));assert sha(W/'scripts/shell_ornament.gd')==full['candidate_source_sha256']
pin=json.loads((T/'validation/SOURCE_PIN.json').read_text(encoding='utf-8-sig'));effective=dict(pin['runtime_hashes'])
for row in full['canonical_text_only_import_normalization']:effective[row['path']]=row['after']
with ThreadPoolExecutor(max_workers=4)as pool:before=dict(pool.map(lambda p:(p,sha(W/p)),effective))
assert before==effective
np=json.loads((T/'NORMAL_SAVE_PIN.json').read_text(encoding='utf-8-sig'));nb=Path(np['normal_base'])
def normals():return{s:sha(Path(str(nb)+s))if Path(str(nb)+s).is_file()else'absent'for s in np['hashes']}
assert normals()==np['hashes']
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip());assert sha(E)=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
 p=D/key;p.mkdir();env[key]=str(p)
results=[]
for label,args in [('import',['--headless','--path',str(W),'--import']),('ignored_fixture_analyzer',['--headless','--path',str(W),'--check-only','--script','res://docs/handoffs/codex_flat_vector_art_2026-10-07/r144_shared_painted_shell/capture_context.gd'])]:
 command=[str(E),*args]
 with(D/(label+'.log')).open('wb')as log:
  p=subprocess.Popen(command,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
  wr(T/'REVIEW_EXPORT_GUARD_STATE.json',{'stage':'RUNNING_'+label,'runner_pid':os.getpid(),'pid':p.pid,'command':command,'log':str(D/(label+'.log')),'source_sha256':full['candidate_source_sha256']})
  rc=p.wait()
 text=(D/(label+'.log')).read_text(encoding='utf-8',errors='replace');errors=[l for l in text.splitlines()if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)',l)]
 row={'label':label,'command':command,'exit_code':rc,'errors':errors,'log_sha256':sha(D/(label+'.log'))};results.append(row);wr(D/'PROCESS_RESULTS.json',{'results':results});assert rc==0 and not errors,(label,rc,errors,text[-2000:]);print('REVIEW_EXPORT_GUARD_PASS',label,flush=True)
caches=list((W/'.godot/editor').glob('filesystem_cache*'));assert caches
hits=[]
for p in caches:
 for line in p.read_text(encoding='utf-8',errors='replace').splitlines():
  if 'r144_shared_painted_shell'in line:hits.append(line)
assert not hits,hits
assert not list(F.rglob('*.import'))
with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda p:(p,sha(W/p)),effective))
assert after==effective and normals()==np['hashes']
wr(D/'RESULT.json',{'state':'PASS_R144_REVIEW_RESOURCE_EXCLUSION_EXACT_ENGINE_IMPORT','source_sha256':full['candidate_source_sha256'],'runtime_input_count':len(effective),'runtime_unchanged':True,'normal_unchanged':True,'guard':(F/'.gdignore').relative_to(W).as_posix(),'ignored_review_resources_in_editor_cache':0,'regenerated_review_import_sidecars':0,'explicit_ignored_fixture_still_loads':True,'process_results':results,'performance_metrics_not_claimed':['physicalFPS','GPUallocation','APKsize'],'formal_QA11':None,'device':None,'child':None,'owner':None})
wr(T/'REVIEW_EXPORT_GUARD_STATE.json',{'stage':'TERMINAL_PASS','source_sha256':full['candidate_source_sha256'],'directory':str(D)});print('R144_REVIEW_EXPORT_BOUNDARY_PASS',flush=True)
