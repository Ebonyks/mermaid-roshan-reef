from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r57_catalogue_selector_crosswalk';W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');S=Path(r'C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-catalogue-selector-crosswalk-20261015');G=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
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
baseline=json.loads((S/'POST_IMPORT_BASELINE.json').read_text());source=P/'selector_component.gd';fixture=W/'export/flat_vector_r57/selector_component.gd';assert source.read_bytes()==fixture.read_bytes();assert sidecars()==baseline['sidecars']and normals()==baseline['normal_save_hashes'];dest=P/'component';assert not dest.exists();dest.mkdir();out=S/'COMPONENT.json';assert not out.exists()
env=dict(os.environ,R57_OUT=str(out),R57_ALIASES=str(S/'ALIASES.json'));cmd=[G,'--headless','--path',str(W),'--rendering-method','mobile','--audio-driver','Dummy','--script','res://export/flat_vector_r57/selector_component.gd'];launch={'command':cmd,'source_revision':D,'fixture_sha256':sha(source.read_bytes()),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':normals(),'scope':'Bare unchanged Main outside tree. Pure unchanged catalogue/selector synthetic component only. No ready/tick/setup/game constructors/player/render/art/captures/route acceptance.'};wr(dest/'LAUNCH.json',launch)
with(dest/'engine.log').open('wb')as log:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=90)
raw=(dest/'engine.log').read_bytes();changed=[p for p,h in baseline['runtime_raw_hashes'].items()if sha((W/p).read_bytes())!=h];result={'exit_code':q.returncode,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_before':launch['normal_before'],'normal_after':normals(),'sidecar_count':len(baseline['sidecars']),'sidecars_exact':sidecars()==baseline['sidecars'],'runtime_file_count':len(baseline['runtime_raw_hashes']),'changed_runtime_files':changed,'fixture_unchanged':source.read_bytes()==fixture.read_bytes(),'log_sha256':sha(raw),'engine_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw))};wr(dest/'RESULT.json',result)
if out.is_file():shutil.copyfile(out,dest/'COMPONENT.json')
print('R57_COMPONENT_RESULT',result,raw.decode(errors='replace')[-2000:],flush=True)
assert q.returncode==0 and not result['engine_errors']and result['sidecars_exact']and not changed and result['fixture_unchanged']and result['normal_before']==result['normal_after']and out.is_file()
a=json.loads(out.read_text());assert a['failed']==0 and a['engine']['string']=='4.7.2-stable (official)'
