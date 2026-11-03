from pathlib import Path
import subprocess,json,hashlib,os,sys,time,shutil
R=Path(__file__).resolve().parents[2];REPO=R.parents[2];OUT=R/'evidence/verification_v3';RAW=OUT/'raw';OUT.mkdir(exist_ok=True);G='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe';rows=[]
def verify():
 f=json.loads((R/'evidence/frozen_candidate_v3.json').read_text());bad=[x['path'] for x in f['files'] if hashlib.sha256((R/x['path']).read_bytes()).hexdigest()!=x['sha256']];return {'frozen':'sport-stage-source-v3','checked':len(f['files']),'mismatches':bad,'pass':not bad}
def save():
 (OUT/'receipt.json').write_text(json.dumps({'scope':'Exact frozenv3 source review; failed lanes remain blocking, no floor or counterexample removed.','input_check':verify(),'rows':rows},indent=2)+'\n')
def run(name,args,timeout=1200):
 start=time.monotonic();out=OUT/(name+'.log');env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 flags=getattr(subprocess,'CREATE_NO_WINDOW',0)|(getattr(subprocess,'BELOW_NORMAL_PRIORITY_CLASS',0) if 'geometry' in name else 0)
 with out.open('w',encoding='utf-8') as f:
  try:p=subprocess.run(args,cwd=REPO,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=timeout,creationflags=flags);code=p.returncode
  except subprocess.TimeoutExpired:code=124
 text=out.read_text(encoding='utf-8',errors='replace');ok=code==0 and not any(x in text for x in ['SCRIPT ERROR','Parse Error','Compile Error','SHADER ERROR','ERROR: Invalid image','Failed to load image'])
 rows.append({'name':name,'args':args,'exit':code,'seconds':round(time.monotonic()-start,2),'pass':ok,'log':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()});save();print(name,ok,flush=True);return ok
assert verify()['pass'];save()
files=[str(p) for p in (R/'demo').glob('*.gd')]
run('import',[G,'--headless','--path',str(R/'demo'),'--editor','--import'])
run('parser',[sys.executable,'-m','gdtoolkit.parser',*files]);run('inference',[sys.executable,'tools/lint_inference.py',*files])
for theme in ['boxer','racer','popstar']:
 out=RAW/'legacy'/theme;out.mkdir(parents=True,exist_ok=True)
 run('render_'+theme,[G,'--path',str(R/'demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s','render_legacy.gd','--',str(out),theme])
 rig=json.loads((R/'demo/rig.json').read_text());rig['meshes'][0]['texture']='art/'+theme+'_composed.png';rig['meshes'][1]['texture']='art/upper_clean.png';rig['meshes'][-1]['texture']='art/'+theme+'_head.png';pin=OUT/('rig_'+theme+'.json');pin.write_text(json.dumps(rig,separators=(',',':'))+'\n')
 run('geometry_'+theme,[sys.executable,str(R/'tools/audit_study.py'),str(out),'--rig',str(pin)])
 run('motion_'+theme,[sys.executable,str(R/'tools/audit_motion.py'),str(out)])
for name,script,out,extra in [('actions','capture.gd',RAW/'actions',['full']),('mixes','capture_mixes.gd',RAW/'mixes',[]),('controls','controls.gd',OUT/'controls',[])]:
 out.mkdir(parents=True,exist_ok=True);run(name,[G,'--path',str(R/'demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s',script,'--',str(out),*extra])
# The independent outline tool writes a report at the source root; preserve this lane's exact copy.
run('mix_outlines',[sys.executable,str(R/'tools/audit_mixed_outlines.py'),str(RAW/'mixes')])
for name in ['mixed_outline_audit.json','mixed_failure_index.json']:
 p=R/'evidence'/name
 if p.exists():shutil.copy2(p,OUT/name)
for theme in ['boxer','racer','popstar']:
 out=RAW/'legacy'/theme
 for name in ['samples.json','stress_samples.json','geometry_audit.json','geometry_audit_Body.json','motion_audit.json','engine_receipt.json']:
  if (out/name).exists():shutil.copy2(out/name,OUT/(theme+'_'+name))
for name,source in [('action_samples.json',RAW/'actions/samples.json'),('mixed_samples.json',RAW/'mixes/samples.json'),('switch_receipt.json',RAW/'mixes/switch_receipt.json')]:
 if source.exists():shutil.copy2(source,OUT/name)
save();print('FROZEN_V3_VERIFICATION_COMPLETE',all(x['pass'] for x in rows),verify(),flush=True)
