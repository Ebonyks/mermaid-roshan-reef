from pathlib import Path
import subprocess,json,os,time,hashlib,sys
R=Path(__file__).resolve().parents[1];REPO=R.parents[2];G='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe';rows=[]
def run(name,args,timeout=600):
 t=time.monotonic();out=R/'evidence'/(name+'.log')
 with out.open('w',encoding='utf-8') as f:p=subprocess.run(args,cwd=REPO,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1'))
 text=out.read_text(encoding='utf-8',errors='replace');ok=p.returncode==0 and not any(x in text for x in ['SCRIPT ERROR','Parse Error','Compile Error','ERROR: Invalid image','Failed to load image'])
 rows.append({'name':name,'args':args,'exit':p.returncode,'seconds':time.monotonic()-t,'pass':ok,'log':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()});(R/'evidence/native_gate.json').write_text(json.dumps({'rows':rows},indent=2)+'\n');print(name,ok,flush=True)
 return ok
if not run('native_import',[G,'--headless','--path',str(R/'demo'),'--editor','--import']):raise SystemExit(1)
files=[str(p) for p in (R/'demo').glob('*.gd')]
if not run('native_parser',[sys.executable,'-m','gdtoolkit.parser',*files]):raise SystemExit(1)
if not run('native_lint',[sys.executable,'tools/lint_inference.py',*files]):raise SystemExit(1)
for theme in ['boxer','racer','popstar']:
 out=R/'evidence/legacy_raw'/theme;out.mkdir(parents=True,exist_ok=True)
 if not run('legacy_render_'+theme,[G,'--path',str(R/'demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s','render_legacy.gd','--',str(out),theme]):raise SystemExit(1)
 rig=json.loads((R/'demo/rig.json').read_text());rig['meshes'][0]['texture']='art/'+theme+'_composed.png';rig['meshes'][1]['texture']='art/upper_clean.png';rig['meshes'][-1]['texture']='art/'+theme+'_head.png';pin=R/'evidence'/('rig_'+theme+'.json');pin.write_text(json.dumps(rig,separators=(',',':'))+'\n')
 run('legacy_geometry_'+theme,[sys.executable,str(R/'tools/audit_study.py'),str(out),'--rig',str(pin)])
 run('legacy_motion_'+theme,[sys.executable,str(R/'tools/audit_motion.py'),str(out)])
if not run('full_action_capture',[G,'--path',str(R/'demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s','capture.gd','--',str(R/'evidence/action_raw'),'full']):raise SystemExit(1)
if not run('mix_capture',[G,'--path',str(R/'demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s','capture_mixes.gd','--',str(R/'evidence/mixed_raw')],1200):raise SystemExit(1)
run('mixed_outlines',[sys.executable,str(R/'tools/audit_mixed_outlines.py')])
run('fault_controls',[G,'--path',str(R/'demo'),'--rendering-method','mobile','--resolution','1280x720','--position','10000,10000','-s','controls.gd','--',str(R/'evidence/controls')])
raise SystemExit(0 if all(r['pass'] for r in rows) else 1)
