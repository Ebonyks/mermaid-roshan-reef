from pathlib import Path
import os,json,subprocess,hashlib,datetime,shutil,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r49_callback_value_domains';S=Path(os.environ['TEMP'])/'reef-flat-vector-callback-value-domains-20261015';B='61d12c5b7d29cd106a817d8d0064aa60f48f3ed2';G='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sidecars():
 out={}
 for root,dirs,files in os.walk(R):
  dirs[:]=[x for x in dirs if x not in {'.git','.godot','__pycache__'}]
  for name in files:
   f=Path(root)/name
   if f.suffix in {'.uid','.import'}:out[f.relative_to(R).as_posix()]=sha(f.read_bytes())
 return out
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
def normals():return {x:sha(Path(str(normal)+x).read_bytes()) if Path(str(normal)+x).is_file() else 'absent' for x in ['', '.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old']}
a=sidecars();n=normals();assert len(a)==4039
job=S/'engine_attempt1';assert not job.exists();job.mkdir();dest=P/'engine/attempt1';dest.mkdir(parents=True)
source=P/'probe_callback_domains.gd';raw_source=source.read_bytes();shutil.copyfile(source,dest/'fixture_source.gd')
cmd=[G,'--headless','--path',str(R),'--rendering-method','mobile','--audio-driver','Dummy','--script','res://'+source.relative_to(R).as_posix()];env=dict(os.environ,R49_OUT=str(job/'output'),R49_REV=B)
wr(dest/'LAUNCH.json',{'command':cmd,'source_revision':B,'fixture_sha256':sha(raw_source),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Unmodified headless TouchUI component with synthetic receivers; no Main/game instance or rendered art/route acceptance.'})
with (dest/'engine.log').open('wb') as out:q=subprocess.run(cmd,cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT,timeout=180,creationflags=0x08000000)
raw=(dest/'engine.log').read_bytes();proof=job/'output/COMPONENT_PROOF.json'
if proof.exists():shutil.copyfile(proof,dest/proof.name)
result={'exit_code':q.returncode,'normal_before':n,'normal_after':normals(),'sidecars_before_count':len(a),'sidecars_after_count':len(sidecars()),'sidecars_exact':a==sidecars(),'fixture_unchanged':raw_source==source.read_bytes(),'log_sha256':sha(raw),'script_or_shader_errors':bool(re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw)),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};wr(dest/'RESULT.json',result)
print('R49_ACTUAL_COMPONENT',q.returncode,raw.decode(errors='replace')[-5500:],flush=True)
assert result['normal_before']==result['normal_after'] and result['sidecars_exact'] and result['fixture_unchanged']
assert q.returncode==0 and not result['script_or_shader_errors'] and proof.is_file()
