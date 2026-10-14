"""Run all82 current trusted CI probes in fresh isolated profiles;zero exit required."""
from pathlib import Path
import json,subprocess,os,datetime,hashlib,re,pickle
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parent
STAGE=Path('C:/Users/Peter/.codex/visualizations/2026/10/08/01a119cc-74b1-7d23-b956-126129405418/startup_ambience_retirement_20261014')
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=R,stderr=subprocess.PIPE).decode().strip()
ci=(R/'scripts/ci.sh').read_text();names=re.search(r'for p in (probe_reef_districts .*?); do',ci).group(1).split();assert len(names)==82
FAILURE=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
RESOURCE=re.compile(r'SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)')
HYBRID={'probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'}
LOGS=P/'trusted_logs';LOGS.mkdir()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def wr(d):(P/'FULL_VALIDATION.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
normalcmd=[G,'--headless','--path',str(R),'--script','res://.godot/r14_normal_save_hashes.gd']
normalbefore=subprocess.check_output(normalcmd,cwd=R,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
rows=[];d={'schema':'reef.full_validation/1','source_baseline':'fdf41220b8cfe16f129741e364b2ea75f4e5e7f1','runtime_delta':['scripts/living_world.gd','scripts/probe_living_world.gd'],'new_assets_scope':'No newruntime assets/pixels;display StartMenu procedural ambience retirement;allotherstage/headless behavior tested.','approved_engine':G,'engine_version':subprocess.check_output([G,'--version'],creationflags=subprocess.CREATE_NO_WINDOW).decode().strip(),'status':'RUNNING','trusted_required':82,'trusted_passed':0,'rows':rows,'started_at_utc':now(),'CI_roster_sha256_LF':hashlib.sha256(ci.encode()).hexdigest(),'failure_regex':FAILURE.pattern,'resource_error_regex':RESOURCE.pattern,'acceptance_limit':'Machine source/import/probe evidence only; no whole-gameart/QA11/device/child/owner acceptance.'};wr(d)
try:
 for name in names:
  profile=STAGE/'trusted_profiles'/name;env=os.environ.copy()
  for k,leaf in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
   loc=profile/leaf;loc.mkdir(parents=True);env[k]=str(loc)
  mode='--hybrid-touch-test' if name in HYBRID else '--classic-touch-test';cmd=[G,'--headless','--path',str(R),'-s','res://scripts/'+name+'.gd','--','--touch',mode];start=now()
  try:q=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=480,creationflags=subprocess.CREATE_NO_WINDOW);raw=q.stdout;rc=q.returncode
  except subprocess.TimeoutExpired as e:raw=e.stdout or b'';rc=124
  (LOGS/(name+'.log')).write_bytes(raw);txt=raw.decode('utf-8','replace');fail=bool(FAILURE.search(txt) or RESOURCE.search(txt));exit_ok=rc==0
  result='PASS' if exit_ok and not fail else 'FAIL';rows.append({'probe':name,'command':cmd,'started_at_utc':start,'completed_at_utc':now(),'exit_code':rc,'result':result,'raw_output_bytes':len(raw),'raw_output_sha256':hashlib.sha256(raw).hexdigest(),'evidence':'trusted_logs/'+name+'.log','isolated_profile':True,'touch_mode':mode});d['trusted_passed']=sum(x['result']=='PASS' for x in rows);wr(d);print('R30_TRUSTED',len(rows),name,result,flush=True)
  if result!='PASS':break
 d['completed_at_utc']=now();d['status']='PASS_ALL_82_TRUSTED_NATIVE' if len(rows)==82 and d['trusted_passed']==82 else 'INCOMPLETE_OR_FAILED'
finally:
 saved=pickle.loads((STAGE/'import_sidecars_before.pickle').read_bytes());restored=0
 for path,b in saved.items():
  f=R/path
  if f.read_bytes()!=b:f.write_bytes(b);restored+=1
 normalafter=subprocess.check_output(normalcmd,cwd=R,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW);d['normal_save_before_output']=normalbefore.decode('utf-8','replace');d['normal_save_after_output']=normalafter.decode('utf-8','replace');d['normal_save_hashes_unchanged']=normalbefore==normalafter;d['tracked_sidecars_preserved']=len(saved);d['tracked_sidecars_restored_exact']=restored;wr(d)
assert d['status']=='PASS_ALL_82_TRUSTED_NATIVE' and d['normal_save_hashes_unchanged'],d['status']
print('R30_FULL_VALIDATION|ALL_82_OK')
