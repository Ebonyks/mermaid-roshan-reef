from pathlib import Path
import json,hashlib,subprocess,os,re,datetime,sys
U=Path.cwd();S=Path(__file__).parent;P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r129_melody_guide_runtime';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe');BASE='27c88288bf6e39582072811443df79919e7bbb89';W=S/'candidate_import';N=S/'candidate_native'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'NATIVE_STATE.json',dict(state=n,at_utc=now(),**kw))
def sandbox(d):
 env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 for k,n in[('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir(exist_ok=True);env[k]=str(p)
 return env
assert not W.exists() and not N.exists(),'An operation already exists; resume its exact handle';assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE;assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/flat-vector-melody-guide-20261102';assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424';W.mkdir();N.mkdir();imports={p:(U/p).read_bytes()for p in subprocess.check_output(['git','ls-files','*.import'],text=True,encoding='utf-8').splitlines()if(U/p).is_file()};normal=Path(json.loads((U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json').read_text(encoding='utf-8-sig'))['normal_base']);suffixes=['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.bak','.before_new_game.tmp']
def normals():return{n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in suffixes}
before=normals();rows=[]
try:
 env=sandbox(W);cmd=[str(E),'--headless','--path',str(U),'--rendering-method','mobile','--import']
 for leg in['initial_new_asset','final_new_import_settings']:
  state('IMPORTING_ACTUAL_GUIDE',leg=leg);log=W/(leg+'.log')
  with log.open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=360,creationflags=0x08000000)
  text=log.read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',text),text[-4000:];rows.append(dict(leg=leg,exit_code=q.returncode,log_sha256=sha(log)))
  if leg=='initial_new_asset':
   for item in json.loads((U/'assets_src/imagegen/melody_guide_20261102/EXPORT.json').read_text(encoding='utf-8'))['engine_textures']:
    p=U/(item['path']+'.import');t=p.read_text(encoding='utf-8');assert 'compress/mode=0'in t and '"vram_texture": false'in t;limit=1024;t=t.replace('mipmaps/generate=false','mipmaps/generate=true').replace('process/size_limit=0','process/size_limit='+str(limit));p.write_text(t,encoding='utf-8',newline='\n')
 drift=[]
 for rel,raw in imports.items():
  after=(U/rel).read_bytes()
  if raw!=after:
   assert raw.replace(b'\r\n',b'\n')==after.replace(b'\r\n',b'\n'),rel;drift.append(dict(path=rel,before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=sha(U/rel),change='EOL_ONLY'))
 wr(S/'IMPORT_EOL_BINDING.json',dict(state='ALL_OLD_IMPORT_DRIFT_EOL_ONLY',files=drift));wr(W/'FINAL_RESULT.json',dict(state='PASS_NEW_GUIDE_LOSSLESS_MIPMAPS_NO_VRAM',legs=rows,old_import_drift=len(drift),new_assets=json.loads((U/'assets_src/imagegen/melody_guide_20261102/EXPORT.json').read_text(encoding='utf-8'))['engine_textures']));print('R129_IMPORT_PASS',flush=True)
 paths=[p for p in subprocess.check_output(['git','ls-files'],text=True,encoding='utf-8').splitlines()if p.startswith(('assets/','scripts/','scenes/'))or p in['project.godot','tools/godot_baseline.json']];paths += [suffix for item in json.loads((U/'assets_src/imagegen/melody_guide_20261102/EXPORT.json').read_text(encoding='utf-8'))['engine_textures'] for suffix in [item['path'],item['path']+'.import']];hashes={p:sha(U/p)for p in sorted(set(paths))if(U/p).is_file()};pin=dict(baseline=BASE,runtime_hashes=hashes,engine=str(E),engine_sha256=sha(E),fixture_sha256=sha(P/'capture_guide.gd'),normal_before=before,Dev_integrated=False);wr(N/'SOURCE_PIN.json',pin);pinsha=sha(N/'SOURCE_PIN.json');cases=[]
 for width,height in[(1280,720),(1600,720),(1280,800)]:
  d=N/(str(width)+'x'+str(height));d.mkdir();env=sandbox(d);env.update(R129_OUT=str(d/'output'),R129_LANE='candidate',R129_WIDTH=str(width),R129_HEIGHT=str(height),R129_PIN_SHA256=pinsha);cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x'+str(height),'--max-fps','30','--script','res://export/flat_vector_r128/capture_guide.gd'];wr(d/'LAUNCH.json',dict(command=cmd,at_utc=now(),pin_sha256=pinsha));state('RUNNING_NATIVE_CANDIDATE',width=width,height=height)
  with(d/'engine.log').open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=240,creationflags=0x08000000)
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:.*(Failed loading resource|Cannot open file|No loader found)',text),text[-4000:];r=json.loads((d/'output/RESULT.json').read_text(encoding='utf-8-sig'));assert r['status']=='PASS' and all(x['pass']for x in r['checks']);cases.append(dict(width=width,height=height,checks=len(r['checks']),frames=r['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R129_NATIVE',width,height,len(r['checks']),flush=True)
 changed=[p for p,h in hashes.items()if sha(U/p)!=h];assert not changed and normals()==before;wr(N/'FINAL_RESULT.json',dict(state='PASS_CONFIGURED_CURRENT_NATIVE_REVIEW_REQUIRED',cases=cases,checks=sum(x['checks']for x in cases),new_native_frame_events=sum(len(x['frames'])for x in cases),source_drift=changed,normal_unchanged=True,normal_before=before,normal_after=normals(),formal_QA11=None,device=None,child=None,owner=None,completed_at_utc=now()));state('TERMINAL_NATIVE_PASS');print('R129_NATIVE_ALL_OK',flush=True)
except Exception as e:wr(S/'NATIVE_STOP.json',dict(state='STOPPED_NO_AUTOMATIC_RESTART',error=str(e),at_utc=now()));state('TERMINAL_NATIVE_FAILURE',error=str(e));raise
