from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re
R=Path.cwd();P=Path(__file__).resolve().parent;H=P.parent;W=Path(os.environ.get('R76_SOURCE_WORKTREE',r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef'));S=Path(os.environ.get('R76_JOB_ROOT',str(Path(os.environ['TEMP'])/'reef-flat-vector-stuffie-care-context-20261016')));D='dd799b2d43871b29d1d6e0503646308a194dad1e'
G=subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=W,text=True).strip()
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sidecars():
 rows={}
 for root,dirs,files in os.walk(W):
  dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
  for name in files:
   f=Path(root)/name
   if f.suffix in {'.uid','.import'}:rows[f.relative_to(W).as_posix()]=sha(f.read_bytes())
 return rows
n=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
def normals():return {x:sha(Path(str(n)+x).read_bytes()) if Path(str(n)+x).is_file() else 'absent' for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
base=json.loads((H/'r75_tree_book_registration/RUNTIME_BYTE_BASELINE.json').read_text(encoding='utf-8'));gate=json.loads((P/'FIXTURE_SYNTAX_GATES.json').read_text(encoding='utf-8'));assert gate['status']=='PASS_BEFORE_NATIVE';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()==D and not subprocess.check_output(['git','status','--porcelain'],cwd=W).strip()
fixture=P/'capture_care.gd';executed=W/'export/flat_vector_r76/capture_care.gd';assert fixture.read_bytes()==executed.read_bytes() and sha(fixture.read_bytes())==gate['fixture_files'][0]['sha256'];assert sidecars()==base['sidecars'];changed=[p for p,d in base['runtime_raw_hashes'].items() if sha((W/p).read_bytes())!=d];assert not changed
deps={'capture_care.gd':sha(fixture.read_bytes())};mode='source'
width=int(os.environ.get('R76_TEST_WIDTH','1280'));assert width in [1280,1600];name='attempt'+os.environ.get('R76_TEST_ATTEMPT','1')+'_care_'+mode+'_'+str(width);job=S/name;assert not job.exists();job.mkdir(parents=True);dest=P/'native'/name;dest.mkdir(parents=True);shutil.copyfile(fixture,dest/fixture.name);out=job/'output';env=dict(os.environ,R76_OUT=str(out),R76_WIDTH=str(width),R76_REV=D,R76_MODE=mode);cmd=[G,'--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r76/capture_care.gd'];launch={'mode':mode,'fixture_dependencies':deps,'command':cmd,'source_revision':D,'source_worktree':str(W),'fixture_sha256':sha(fixture.read_bytes()),'normal_before':normals(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_byte_changes_before':changed,'scope':'Original Main/private beforeReady dependency and declared source promenade startup seam. Original Menu/Stuffie/care/Back inputs and natural clocks; no visual/source/want/timer override. No fullroute/finalQA11/device/child/owner acceptance.'};wr(dest/'LAUNCH.json',launch)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);code=q.returncode;timed=False
 except subprocess.TimeoutExpired:code=None;timed=True
raw=(dest/'engine.log').read_bytes();after=sidecars();changed=[p for p,d in base['runtime_raw_hashes'].items() if sha((W/p).read_bytes())!=d];res={'exit_code':code,'timed_out':timed,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':launch['normal_before'],'normal_after':normals(),'sidecar_before_count':len(base['sidecars']),'sidecar_after_count':len(after),'sidecars_exact':after==base['sidecars'],'source_byte_changes':changed,'fixture_dependency_unchanged':all(sha((W/'export/flat_vector_r76'/n).read_bytes())==v for n,v in deps.items()),'log_sha256':sha(raw),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw))};wr(dest/'RESULT.json',res)
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
print('R76_NATIVE',name,'exit',code,'timeout',timed,'normal_exact',res['normal_before']==res['normal_after'],'source_exact',not changed,'sidecars_exact',res['sidecars_exact'],'\n'+raw.decode(errors='replace')[-1500:],flush=True)
assert res['normal_before']==res['normal_after'] and res['sidecars_exact'] and not changed and res['fixture_dependency_unchanged']
assert code==0 and not timed and not res['script_or_shader_errors'] and (dest/'capture_manifest.json').is_file()
