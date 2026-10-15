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
baseline=json.loads((S/'POST_IMPORT_BASELINE.json').read_text());assert sidecars()==baseline['sidecars']and normals()==baseline['normal_save_hashes'];out=P/'SOURCE_RECIPE_REPLAY.json';assert not out.exists();before=normals();cmd=[G,'--headless','--path',str(W),'--rendering-method','mobile','--script','res://export/flat_vector_r59/verify_frame_recipe.gd'];env=dict(os.environ,R59_RECIPE_OUT=str(out))
with(P/'recipe.log').open('wb')as log:q=subprocess.run(cmd,cwd=W,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=90)
changes=[p for p,h in baseline['runtime_raw_hashes'].items()if sha((W/p).read_bytes())!=h];result={'exit_code':q.returncode,'command':cmd,'normal_before':before,'normal_after':normals(),'sidecars_exact':sidecars()==baseline['sidecars'],'runtime_files_changed':changes,'log_sha256':sha((P/'recipe.log').read_bytes()),'scope':'In-memory recipe-only component; no rendered candidate/context credit, source/master/UI approval or source builder write.'};wr(P/'RECIPE_RESULT.json',result);print('R59_RECIPE',result,flush=True);assert result['sidecars_exact']and not changes and result['normal_before']==result['normal_after']and q.returncode==0
