from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r70_skyway_art_reuse';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-skyway-art-reuse-20261015');G=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sidecars():
 result={}
 for root,dirs,files in os.walk(W):
  dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
  for name in files:
   f=Path(root)/name
   if f.suffix in {'.uid','.import'}:result[f.relative_to(W).as_posix()]=sha(f.read_bytes())
 return result
n=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
def normals():return{x:sha(Path(str(n)+x).read_bytes())if Path(str(n)+x).is_file()else'absent'for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
baseline=json.loads((S/'POST_IMPORT_BASELINE.json').read_text(encoding='utf-8'));gate=json.loads((P/'FIXTURE_SYNTAX_GATES.json').read_text(encoding='utf-8'));assert gate['status']=='PASS_BEFORE_NATIVE'
deps={}
for name in ['base_capture.gd','capture_entry.gd','capture_fairy.gd','capture_skyway.gd','skyway_reuse.gd']:
 a=P/name;b=W/'export/flat_vector_r70'/name;raw=a.read_bytes();assert raw==b.read_bytes();assert next(x['sha256'] for x in gate['fixture_files'] if x['path']==name)==sha(raw);deps[name]=raw
assert sidecars()==baseline['sidecars'] and all(normals()[k]==v for k,v in baseline['normal_save_hashes'].items());before_changes=[path for path,digest in baseline['runtime_raw_hashes'].items()if sha((W/path).read_bytes())!=digest];assert not before_changes
width=int(os.environ.get('R70_TEST_WIDTH','1280'));mode=os.environ.get('R70_TEST_MODE','opened');assert mode in ['dormant','revealed','opened']
visual=os.environ.get('R70_TEST_VISUAL','z_only');assert visual in ['z_only','cover'];name='attempt'+os.environ.get('R70_TEST_ATTEMPT','1')+'_'+visual+'_'+str(width)
job=S/name;assert not job.exists();job.mkdir();dest=P/'native'/name;dest.mkdir(parents=True)
for file,raw in deps.items():(dest/file).write_bytes(raw)
out=job/'output';env=dict(os.environ,R70_OUT=str(out),R70_WIDTH=str(width),R70_REV=D,R70_MODE=mode,R70_NORMAL_BASE=str(n),R70_VISUAL=visual);cmd=[G,'--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r70/capture_skyway.gd'];launch={'command':cmd,'source_revision':D,'mode':mode,'source_before_byte_changes':before_changes,'fixture_dependencies':{k:sha(v)for k,v in deps.items()},'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':normals(),'source_worktree':str(W),'scope':'R70 nonruntime backdrop/background-only visual candidate on actual original source controller. Original Main/private dependency beforeReady and original input/caller/callback/foreground geometry/state preserved. Only declared existing-node visual delta; no production/art generation/adoption or device/child/owner acceptance.'};wr(dest/'LAUNCH.json',launch)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);exitcode=q.returncode;timeout=False
 except subprocess.TimeoutExpired:exitcode=None;timeout=True
raw=(dest/'engine.log').read_bytes();after=sidecars();changed_sources=[path for path,digest in baseline['runtime_raw_hashes'].items()if sha((W/path).read_bytes())!=digest];result={'exit_code':exitcode,'timed_out':timeout,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':launch['normal_before'],'normal_after':normals(),'sidecar_before_count':len(baseline['sidecars']),'sidecar_after_count':len(after),'sidecars_exact':after==baseline['sidecars'],'source_byte_changes':changed_sources,'fixture_dependencies_unchanged':all(rawbytes==(W/'export/flat_vector_r70'/filename).read_bytes() for filename,rawbytes in deps.items()),'log_sha256':sha(raw),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw))};wr(dest/'RESULT.json',result)
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
print('R70_NATIVE',name,json.dumps(result),'\n',raw.decode(errors='replace')[-1000:],flush=True)
assert result['normal_before']==result['normal_after']and result['sidecars_exact']and not changed_sources and result['fixture_dependencies_unchanged']
assert exitcode==0 and not timeout and not result['script_or_shader_errors']and(out/'capture_manifest.json').is_file()
