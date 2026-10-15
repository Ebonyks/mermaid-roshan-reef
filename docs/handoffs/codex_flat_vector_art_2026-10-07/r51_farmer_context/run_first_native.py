from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r51_farmer_context';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-farmer-context-20261015');G=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
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
baseline=json.loads((S/'POST_IMPORT_BASELINE.json').read_text());source=P/'capture_farmer.gd';fixture=W/'export/flat_vector_r51/capture_farmer.gd';assert source.read_bytes()==fixture.read_bytes();assert sidecars()==baseline['sidecars']and normals()==baseline['normal_save_hashes'];width=1280;job=S/'attempt1_farmer_1280';assert not job.exists();job.mkdir();dest=P/'native/attempt1_farmer_1280';dest.mkdir(parents=True);raw_fixture=fixture.read_bytes();shutil.copyfile(fixture,dest/'fixture_source.gd');out=job/'output';env=dict(os.environ,R51_OUT=str(out),R51_WIDTH=str(width),R51_REV=D);cmd=[G,'--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--script','res://export/flat_vector_r51/capture_farmer.gd'];launch={'command':cmd,'source_revision':D,'fixture_sha256':sha(raw_fixture),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':normals(),'source_worktree':str(W),'scope':'Actual unchanged Mobile/Speedy original Farmer controls from private post-boss seed and original room startup API seam. Engine time scale1;no target/phase/progress/geometry/source writes. No natural earned journey/device/child/owner/QA11/art acceptance.'};wr(dest/'LAUNCH.json',launch)
with(dest/'engine.log').open('wb')as log:
 try:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=600);exitcode=q.returncode;timeout=False
 except subprocess.TimeoutExpired:exitcode=None;timeout=True
raw=(dest/'engine.log').read_bytes();after=sidecars();changed_sources=[path for path,digest in baseline['runtime_raw_hashes'].items()if sha((W/path).read_bytes())!=digest];result={'exit_code':exitcode,'timed_out':timeout,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':launch['normal_before'],'normal_after':normals(),'sidecar_before_count':len(baseline['sidecars']),'sidecar_after_count':len(after),'sidecars_exact':after==baseline['sidecars'],'source_byte_changes':changed_sources,'fixture_unchanged':raw_fixture==fixture.read_bytes(),'log_sha256':sha(raw),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw))};wr(dest/'RESULT.json',result)
for f in [out/'capture_manifest.json',*out.glob('*.png')]:
 if f.is_file():shutil.copyfile(f,dest/f.name)
print('R51_ACTUAL_GUI',width,result,'\n',raw.decode(errors='replace')[-3000:],flush=True)
assert result['normal_before']==result['normal_after']and result['sidecars_exact']and not changed_sources and result['fixture_unchanged']
assert exitcode==0 and not timeout and not result['script_or_shader_errors']and(out/'capture_manifest.json').is_file()
