from pathlib import Path
import json,os,subprocess,hashlib,datetime,re
R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r46_melody_context';S=Path(os.environ['TEMP'])/'reef-flat-vector-melody-context-20261015';B='7cdb9bf63bd8f3846b34b17cce74b065747aae92';G=r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sidecars():
 result={}
 for root,dirs,files in os.walk(R):
  dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__'}]
  for n in files:
   f=Path(root)/n
   if f.suffix in {'.uid','.import'}:result[f.relative_to(R).as_posix()]=sha(f.read_bytes())
 return result
normal_base=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old']
def normals():return {x:sha(Path(str(normal_base)+x).read_bytes()) if Path(str(normal_base)+x).is_file() else 'absent' for x in suffixes}

import shutil
before=sidecars();nb=normals();assert len(before)==4039
rows=[]
for width in [1280,1600]:
 job=S/('native_'+str(width));assert not job.exists();job.mkdir()
 out=job/'output';env=os.environ.copy();env.update(R46_OUT=str(out),R46_WIDTH=str(width),R46_REV=B)
 source=P/'capture_melody_context.gd';cmd=[G,'--path',str(R),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--script','res://'+source.relative_to(R).as_posix()]
 launch={'command':cmd,'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_revision':B,'fixture_sha256':sha(source.read_bytes()),'scope':'Current source API only; real screen-touch events; no natural route proof or art acceptance.'};wr(job/'LAUNCH.json',launch)
 with (job/'engine.log').open('wb') as log:
  q=subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000,timeout=600)
 raw=(job/'engine.log').read_bytes();result={'exit_code':q.returncode,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log_sha256':sha(raw),'normal_before':nb,'normal_after':normals(),'sidecars_before_count':len(before),'sidecars_after_count':len(sidecars()),'sidecars_exact':before==sidecars(),'fixture_unchanged':sha(source.read_bytes())==launch['fixture_sha256']};wr(job/'RESULT.json',result)
 dest=P/'captures'/str(width);dest.mkdir(parents=True)
 for f in [job/'LAUNCH.json',job/'RESULT.json',job/'engine.log',out/'capture_manifest.json',*out.glob('*.png')]:
  if f.is_file():shutil.copyfile(f,dest/f.name)
 rows.append(result);print('R46_ACTUAL_GUI',width,q.returncode,raw.decode(errors='replace')[-1600:],flush=True)
 assert result['sidecars_exact'] and result['normal_before']==result['normal_after'] and result['fixture_unchanged']
 if q.returncode!=0 or re.search(rb'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR',raw):break
wr(P/'ENGINE_RUNS.json',{'runs':rows,'normal_unchanged':nb==normals(),'sidecars_exact':before==sidecars(),'scope':'Unmodified production GUI with private synthetic profiles; each run retains native PNGs/report/log. Any failure stays explicit.'})
