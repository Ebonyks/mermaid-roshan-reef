from pathlib import Path
import json,subprocess,hashlib,os,shutil,datetime,re,sys
R=Path.cwd();P=Path(__file__).resolve().parent;H=P.parent;W=Path(os.environ.get('R85_SOURCE_WORKTREE','C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef'));S=Path(os.environ['R85_JOB_ROOT']);pin=json.loads((S/'SOURCE_PIN.json').read_text(encoding='utf-8'));width=int(sys.argv[1]);assert width in [1280,1600]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()==pin['source_revision']and not subprocess.check_output(['git','status','--porcelain'],cwd=W).strip();assert all(sha(W/p)==v for p,v in pin['runtime_hashes'].items())and all(sha(W/p)==v for p,v in pin['sidecars'].items())
pre=json.loads((H/'r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding='utf-8'));normal=Path(json.loads(next(x['output']for x in pre['checks']if'R77_USERDIR_PREFLIGHT|'in x['output']).split('R77_USERDIR_PREFLIGHT|',1)[1].strip())['normal_path'])
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else'absent'for x in pin['normal_save_suffixes']}
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=W,text=True).strip();attempt=os.environ.get('R85_ATTEMPT','attempt4');assert attempt in ['attempt4'];name=attempt+'_source_'+str(width);job=S/name;job.mkdir(exist_ok=False);dest=P/'native'/name;dest.mkdir(parents=True,exist_ok=False);fixture=P/'capture_entry.gd';executed=W/'export/flat_vector_r85/capture_entry.gd';assert fixture.read_bytes()==executed.read_bytes()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R85_WIDTH=str(width),R85_OUT=str(job/'output'),R85_REV=pin['source_revision'],R85_PRIVATE_NAME='mermaid-roshan-r85-'+str(width)+'-20261017')
for key,sub in [('APPDATA','roaming'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:env[key]=str(job/sub);Path(env[key]).mkdir()
checks=[]
for cmd in [['python','-B','-m','gdtoolkit.parser',str(fixture)],['python','-B','tools/lint_inference.py',str(fixture)],[G,'--headless','--path',str(W),'--check-only','--script','res://export/flat_vector_r85/capture_entry.gd']]:
 q=subprocess.run(cmd,cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=0x08000000);checks.append({'command':cmd,'exit_code':q.returncode,'output':q.stdout.decode(errors='replace'),'sha256':hashlib.sha256(q.stdout).hexdigest()})
wr(dest/'SYNTAX.json',{'checks':checks});assert all(x['exit_code']==0 for x in checks),checks
before=normals();cmd=[G,'--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r85/capture_entry.gd'];wr(dest/'LAUNCH.json',{'command':cmd,'source_revision':pin['source_revision'],'runtime_pin_sha256':sha(S/'SOURCE_PIN.json'),'fixture_sha256':sha(fixture),'normal_before':before,'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Declared nonruntime material candidate plus excluded style diagnostics, original private entry/actual Menu/Back touch. Original glyph/font/geometry/source/save bytes preserved; no generation or acceptance.','isolation':'Private APPDATA/XDG before engine plus unique custom namespace before Main; actual normal names hashed only.'})
print('R85_NATIVE_BEGIN',width,flush=True)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);code=q.returncode;timed=False
 except subprocess.TimeoutExpired:code=None;timed=True
out=job/'output'
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
raw=(dest/'engine.log').read_bytes();r={'exit_code':code,'timed_out':timed,'normal_before':before,'normal_after':normals(),'runtime_source_changes':[p for p,v in pin['runtime_hashes'].items()if sha(W/p)!=v],'sidecar_changes':[p for p,v in pin['sidecars'].items()if sha(W/p)!=v],'fixture_unchanged':sha(fixture)==sha(executed),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw)),'log_sha256':hashlib.sha256(raw).hexdigest(),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};wr(dest/'RESULT.json',r);print('R85_NATIVE_DONE',width,code,'\n'+raw.decode(errors='replace')[-1600:],flush=True);assert code==0 and not timed and before==r['normal_after']and not r['runtime_source_changes']and not r['sidecar_changes']and r['fixture_unchanged']and not r['script_or_shader_errors'];assert json.loads((dest/'capture_manifest.json').read_text())['observer_status']=='PASS'

from PIL import Image
def roi(name):
 with Image.open(dest/(name+'.png'))as im:return im.convert('RGBA').crop((56,40,92,48)).tobytes()
baseline=roi('candidate_menu_root_before');back=roi('candidate_pause_back_after_release');pixel_rows=[]
for state in ['candidate_menu_root_before','candidate_menu_down_pause_transition','candidate_pause_back_after_release','candidate_back_down_resume_transition','candidate_menu_return_after_release','candidate_restored_before_actual_input']:
 actual=roi(state);reference=back if state in ['candidate_menu_down_pause_transition','candidate_pause_back_after_release']else baseline
 channels=[actual[c::4]for c in range(3)];mean=[sum(x)/len(x)for x in channels];warm=mean[0]-mean[2]>15 and mean[1]-mean[2]>8
 pixel_rows.append({'state':state,'roi_sha256':hashlib.sha256(actual).hexdigest(),'same_mode_reference_exact':actual==reference,'mean_rgb':mean,'warm_parchment_present':warm})
differences={state:roi('declared_'+state)!=roi('declared_normal')for state in ['hover','pressed','hover_pressed','focus','focus_pressed','disabled']};focus_pressed_differs=roi('declared_focus_pressed')!=roi('declared_focus')
pixel={'status':'PASS'if all(x['same_mode_reference_exact']and x['warm_parchment_present']for x in pixel_rows)and all(differences.values())and focus_pressed_differs else'FAIL','roi':[56,40,92,48],'normal_frames':pixel_rows,'diagnostic_roi_differs_from_normal':differences,'focus_pressed_differs_from_focus':focus_pressed_differs,'limits':'Nonglyph opaque-region material-presence/timing guard only. Cross-mode pixel equality is not assumed; not visual acceptance, natural button-state coverage or formal QA11.'}
wr(dest/'PIXEL_GUARDS.json',pixel);assert pixel['status']=='PASS',pixel
print('R85_NATIVE_PIXEL_TIMING_GUARDS_PASS',width,flush=True)
