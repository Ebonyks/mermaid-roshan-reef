from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re
R=Path.cwd();P=Path(__file__).resolve().parent;H=P.parent;W=Path(os.environ.get('R79_SOURCE_WORKTREE',r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef'));S=Path(os.environ.get('R79_JOB_ROOT',str(Path(os.environ['TEMP'])/'reef-flat-vector-promenade-slide-20261016')));D='dd799b2d43871b29d1d6e0503646308a194dad1e'
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
pre=next(x['output'] for x in json.loads((H/'r77_intro_entry_ownership/USERDIR_PREFLIGHT.json').read_text(encoding='utf-8'))['checks'] if 'R77_USERDIR_PREFLIGHT|' in x['output']);native_paths=json.loads(pre.split('R77_USERDIR_PREFLIGHT|',1)[1].strip());n=Path(native_paths['normal_path'])
def normals():return {x:sha(Path(str(n)+x).read_bytes()) if Path(str(n)+x).is_file() else 'absent' for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
base=json.loads((H/'r75_tree_book_registration/RUNTIME_BYTE_BASELINE.json').read_text(encoding='utf-8'));gate=json.loads((P/'FIXTURE_SYNTAX_GATES.json').read_text(encoding='utf-8'));assert gate['status']=='PASS_BEFORE_NATIVE';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()==D and not subprocess.check_output(['git','status','--porcelain'],cwd=W).strip()
fixture=P/'capture_entry.gd';executed=W/'export/flat_vector_r79/capture_entry.gd';assert fixture.read_bytes()==executed.read_bytes() and sha(fixture.read_bytes())==gate['fixture_files'][0]['sha256'];assert sidecars()==base['sidecars'];changed=[p for p,d in base['runtime_raw_hashes'].items() if sha((W/p).read_bytes())!=d];assert not changed
deps={'capture_entry.gd':sha(fixture.read_bytes())};mode='source'
width=int(os.environ.get('R79_TEST_WIDTH','1280'));assert width in [1280,1600];name='attempt'+os.environ.get('R79_TEST_ATTEMPT','1')+'_entry_'+mode+'_'+str(width);job=S/name;assert not job.exists();job.mkdir(parents=True);dest=P/'native'/name;dest.mkdir(parents=True);shutil.copyfile(fixture,dest/fixture.name);out=job/'output';env=dict(os.environ,R79_OUT=str(out),R79_WIDTH=str(width),R79_REV=D,R79_MODE=mode,R79_PRIVATE_NAME='mermaid-roshan-r79-'+name.replace('_','-')+'-20261016');cmd=[G,'--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r79/capture_entry.gd'];launch={'mode':mode,'fixture_dependencies':deps,'command':cmd,'source_revision':D,'source_worktree':str(W),'fixture_sha256':sha(fixture.read_bytes()),'normal_before':normals(),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_byte_changes_before':changed,'scope':'Original Main default user://save isolated globally before Ready and through original NewGame scene reload. Original Options selectSpeedy/mute, held NewGame/reload/opening and original travel/focus/slide action/settle. No source/visual/game/timer/position overrides; no fullQA11/device/child/owner acceptance.'};wr(dest/'LAUNCH.json',launch)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);code=q.returncode;timed=False
 except subprocess.TimeoutExpired:code=None;timed=True
raw=(dest/'engine.log').read_bytes();after=sidecars();changed=[p for p,d in base['runtime_raw_hashes'].items() if sha((W/p).read_bytes())!=d];res={'exit_code':code,'timed_out':timed,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':launch['normal_before'],'normal_after':normals(),'sidecar_before_count':len(base['sidecars']),'sidecar_after_count':len(after),'sidecars_exact':after==base['sidecars'],'source_byte_changes':changed,'fixture_dependency_unchanged':all(sha((W/'export/flat_vector_r79'/n).read_bytes())==v for n,v in deps.items()),'log_sha256':sha(raw),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw))};wr(dest/'RESULT.json',res)
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
print('R79_NATIVE',name,'exit',code,'timeout',timed,'normal_exact',res['normal_before']==res['normal_after'],'source_exact',not changed,'sidecars_exact',res['sidecars_exact'],'\n'+raw.decode(errors='replace')[-1500:],flush=True)
assert res['normal_before']==res['normal_after'] and res['sidecars_exact'] and not changed and res['fixture_dependency_unchanged']
assert code==0 and not timed and not res['script_or_shader_errors'] and (dest/'capture_manifest.json').is_file()
