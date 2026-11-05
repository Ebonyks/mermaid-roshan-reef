from pathlib import Path
import os,json,subprocess,hashlib,datetime,time,re,shutil
U=Path.cwd();S=Path(__file__).parent;D=S/'geologist_rest_repair';P=U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r119_dolls_progress_pips_runtime/geologist_rest_repair';E=Path(r'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(D/'NATIVE_STATE.json',dict(state=n,at_utc=now(),**kw))
try:
 state('WAITING_EXISTING_POST_REPAIR_DIAGNOSTIC');start=time.monotonic()
 while not(S/'opera2d_staging_diagnostic_after_rest_repair/RESULT.json').exists():
  assert time.monotonic()-start<600;time.sleep(5)
 diag=rd(S/'opera2d_staging_diagnostic_after_rest_repair/RESULT.json');assert diag['exit_code']==0 and rd(S/'opera2d_staging_diagnostic_after_rest_repair/GEOMETRY.json')['final_separated']
 for n in ['RESULT.json','GEOMETRY.json','engine.log']:shutil.copy2(S/'opera2d_staging_diagnostic_after_rest_repair'/n,P/('after_repair_diagnostic_'+n))
 pin=rd(S/'SOURCE_PIN.json');normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
 def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in pin['normal_before']}
 before=normals();assert before==pin['normal_before'];world_hash=sha(U/'scripts/opera_career_world_2d.gd');cases=[]
 for width in [1280,1600]:
  d=D/str(width);d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
  for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir();env[k]=str(p)
  env.update(R95_OUT=str(d/'output'),R95_WIDTH=str(width),R119_GEO_PHASE='3',R95_NORMAL_BASE=str(normal),R95_REV='218ae766f8e60afb3f6338b8fafce28ec9fab7f2 + Geologist rest repair rawSHA256 '+world_hash)
  cmd=[str(E),'--path',str(U),'--rendering-method','mobile','--audio-driver','Dummy','--resolution',str(width)+'x720','--max-fps','30','--log-file',str(d/'native_engine.log'),'--script','res://export/flat_vector_r119/capture_geologist_rest.gd'];wr(d/'LAUNCH.json',dict(command=cmd,at_utc=now(),world_raw_sha256=world_hash));state('RUNNING_NATIVE_REACTION_CONTEXT',width=width)
  with(d/'engine.log').open('wb')as f:q=subprocess.run(cmd,cwd=U,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=360,creationflags=0x08000000)
  text=(d/'engine.log').read_text(errors='replace');assert q.returncode==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|R119GEO\|RESULT\|FAIL',text),text[-2500:]
  result=rd(d/'output/RESULT.json');assert result['status']=='PASS' and len(result['captures'])==3 and result['normal_before']==result['normal_after'] and all(x['pass']for x in result['checks'])
  dest=P/str(width);dest.mkdir()
  for n in ['LAUNCH.json','engine.log']:shutil.copy2(d/n,dest/n)
  for f in (d/'output').iterdir():
   if f.is_file():shutil.copy2(f,dest/f.name)
  cases.append(dict(width=width,checks=len(result['checks']),frames=result['captures'],result_sha256=sha(d/'output/RESULT.json')));print('R119_GEO_NATIVE_PASS',width,len(result['checks']),flush=True)
 assert normals()==before and sha(U/'scripts/opera_career_world_2d.gd')==world_hash
 out=dict(state='NATIVE_REACTION_CONTEXT_PASS_AGENT_REVIEW_PENDING',cases=cases,checks=sum(x['checks']for x in cases),new_native_frame_events=6,new_bounded_frame_events=6,new_excluded_frame_events=0,world_raw_sha256=world_hash,normal_before=before,normal_after=normals(),normal_unchanged=True,formal_QA11=None,device=None,child=None,owner=None,new_generation_calls=0,new_piece_or_implementation_credit=0,completed_at_utc=now());wr(D/'NATIVE_RESULT.json',out);wr(P/'NATIVE_RESULT.json',out);state(out['state']);print('R119_GEO_NATIVE_TERMINAL_PASS',flush=True)
except Exception as e:wr(D/'NATIVE_STOP.json',dict(state='STOPPED_INSPECT_EXACT_FAILURE_NO_RETRY',error=str(e),at_utc=now()));state('STOPPED',error=str(e));raise
