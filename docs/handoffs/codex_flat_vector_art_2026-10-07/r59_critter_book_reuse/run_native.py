from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r59_critter_book_reuse';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-critter-book-reuse-20261015');G=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
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
def normals():return{x:sha(Path(str(n)+x).read_bytes())if Path(str(n)+x).is_file()else'absent'for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old']}
baseline=json.loads((S/'POST_IMPORT_BASELINE.json').read_text());base_source=P/'base_capture_critter.gd';base_fixture=W/'export/flat_vector_r59/base_capture_critter.gd';assert base_source.read_bytes()==base_fixture.read_bytes();base_hash=sha(base_source.read_bytes());source=P/'capture_reuse.gd';fixture=W/'export/flat_vector_r59/capture_reuse.gd';assert source.read_bytes()==fixture.read_bytes();assert sidecars()==baseline['sidecars']and normals()==baseline['normal_save_hashes'];width=int(os.environ.get("R59_TEST_WIDTH","1280"));mode=os.environ.get('R59_MODE','painted');assert mode in ['layout','painted'];job=S/('attempt'+os.environ.get('R59_TEST_ATTEMPT','1')+'_critter_reuse_'+mode+'_'+str(width));assert not job.exists();job.mkdir();dest=P/('native/attempt'+os.environ.get('R59_TEST_ATTEMPT','1')+'_critter_reuse_'+mode+'_'+str(width));dest.mkdir(parents=True);raw_fixture=fixture.read_bytes();shutil.copyfile(fixture,dest/'fixture_source.gd');out=job/'output';env=dict(os.environ,R59_OUT=str(out),R59_WIDTH=str(width),R59_REV=D,R59_MODE=mode);cmd=[G,'--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r59/capture_reuse.gd'];launch={'command':cmd,'source_revision':D,'trial_mode':mode,'base_fixture_sha256':base_hash,'fixture_sha256':sha(raw_fixture),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':normals(),'source_worktree':str(W),'scope':'Isolated '+mode+' layout/painted source-frame trial on original Menu/category/Back controls after R58 private checkpoint. No source/collection/category/progress/hitowner writes; explicit visual/layout/book layer overrides only. No natural/freshOS/QA11/device/child/owner/art acceptance.'};wr(dest/'LAUNCH.json',launch)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=900);exitcode=q.returncode;timeout=False
 except subprocess.TimeoutExpired:exitcode=None;timeout=True
raw=(dest/'engine.log').read_bytes();after=sidecars();changed_sources=[path for path,digest in baseline['runtime_raw_hashes'].items()if sha((W/path).read_bytes())!=digest];result={'exit_code':exitcode,'timed_out':timeout,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':launch['normal_before'],'normal_after':normals(),'sidecar_before_count':len(baseline['sidecars']),'sidecar_after_count':len(after),'sidecars_exact':after==baseline['sidecars'],'source_byte_changes':changed_sources,'fixture_unchanged':raw_fixture==fixture.read_bytes(),'base_fixture_unchanged':sha(base_fixture.read_bytes())==base_hash,'log_sha256':sha(raw),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw))};wr(dest/'RESULT.json',result)
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
print('R59_ACTUAL_GUI_CRITTER_BOOK',width,result,'\n',raw.decode(errors='replace')[-3000:],flush=True)
assert result['normal_before']==result['normal_after']and result['sidecars_exact']and not changed_sources and result['fixture_unchanged']and result['base_fixture_unchanged']
assert exitcode==0 and not timeout and not result['script_or_shader_errors']and(out/'capture_manifest.json').is_file()
