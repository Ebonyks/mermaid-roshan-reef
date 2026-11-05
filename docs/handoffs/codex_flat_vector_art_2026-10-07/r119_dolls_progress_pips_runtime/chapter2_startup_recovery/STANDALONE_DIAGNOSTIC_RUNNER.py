from pathlib import Path
import json,hashlib,subprocess,os,time,datetime,shutil
S=Path(__file__).parent;U=Path.cwd();OLD=S/'full_validation_rest_coverage_recovery/probe_chapter2';D=S/'chapter2_standalone_child_diagnostic'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
pin=rd(S/'SOURCE_PIN.json');plan=rd(D/'PLAN.json');assert not(D/'LAUNCH.json').exists();assert sha(S/'SOURCE_PIN.json')==plan['source_pin_sha256'];E=Path(pin['engine']);assert sha(E)==pin['engine_sha256'] and sha(U/'scripts/probe_chapter2.gd')==plan['trusted_script_sha256']
normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in pin['normal_before']}
try:
 before=normals();assert before==pin['normal_before'];env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
 for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=D/n;p.mkdir();env[k]=str(p)
 old_expectations=list(OLD.rglob('*.expected.json'));assert len(old_expectations)==1;old=old_expectations[0];record=rd(old);user=D/'appdata'/old.parent.relative_to(OLD/'appdata');user.mkdir(parents=True);fixture=user/('probe_chapter2_isolated_%d_diagnostic.json'%os.getpid());expected=Path(str(fixture)+'.milestone_career_06.expected.json');stem=Path(str(expected).removesuffix('.expected.json'));bindings=[]
 for kind,suffix in [('primary',''),('backup','.bak')]:
  info=record['frozen_inputs'][kind];source=Path(info['path']) if info.get('path')else None
  if source is None:assert not record.get('backup_sha256');continue
  assert source.resolve().is_relative_to(OLD.resolve()) and sha(source)==info['sha256']==record[kind+'_sha256'];destination=Path(str(fixture)+suffix);frozen=Path(str(stem)+'.'+kind+'.input.json');shutil.copy2(source,destination);shutil.copy2(source,frozen);record['frozen_inputs'][kind]['path']=frozen.as_posix();bindings.append(dict(role=kind,source=str(source),source_sha256=sha(source),diagnostic_input=str(destination),diagnostic_sha256=sha(destination),frozen_copy=str(frozen),exact_bytes=True))
 original_parent=record['parent_process_id'];record['parent_process_id']=os.getpid();wr(expected,record)
 cmd=[str(E),'--verbose','--headless','--path',str(U),'--log-file',str(D/'native_engine.log'),'--script','scripts/probe_chapter2.gd','--','--chapter2-resume',fixture.as_posix(),'--expectation',expected.as_posix(),'--touch','--classic-touch-test'];wr(D/'LAUNCH.json',dict(role='DIAGNOSTIC_ONLY_NOT_TRUSTED_GATE',command=cmd,inputs=bindings,original_expectation_sha256=sha(old),diagnostic_expectation_sha256=sha(expected),metadata_edits_only=['owned fixture/frozen inputpaths','actualPython parentPID'],original_parent_pid=original_parent,actual_diagnostic_parent_pid=os.getpid(),source_pin_sha256=sha(S/'SOURCE_PIN.json'),normal_before=before,started_at_utc=now()))
 start=time.monotonic();first=None;header=None;offset=0;timed=False
 with(D/'engine.log').open('wb')as f:
  q=subprocess.Popen(cmd,cwd=U,env=env,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);wr(D/'RUNNING.json',dict(pid=q.pid,started_at_utc=now(),role='DIAGNOSTIC_ONLY_NOT_TRUSTED_GATE',budget_seconds=180))
  while q.poll()is None:
   elapsed=time.monotonic()-start
   with(D/'engine.log').open('rb')as r:r.seek(offset);chunk=r.read();offset=r.tell()
   if header is None and b'Godot Engine'in chunk:header=elapsed
   if first is None and b'CHAPTER2|'in chunk:first=elapsed;print('R119_CHAPTER2_DIAGNOSTIC_FIRST_ASSERTION',round(first,3),flush=True)
   if elapsed>=180:q.kill();q.wait();timed=True;break
   time.sleep(0.5)
  rc=q.wait()
 text=(D/'engine.log').read_text(encoding='utf-8',errors='replace');receipt=Path(str(expected)+'.receipt.json');after=normals();assert after==before;out=dict(role='DIAGNOSTIC_ONLY_NOT_TRUSTED_GATE',exit_code=rc,timeout=timed,elapsed_seconds=round(time.monotonic()-start,3),first_engine_header_seconds=round(header,3)if header is not None else None,first_child_assertion_seconds=round(first,3)if first is not None else None,child_result_observed='CHAPTER2_RESUME_CHILD|RESULT: PASS'in text,receipt_written=receipt.exists(),receipt_sha256=sha(receipt)if receipt.exists()else None,log_sha256=sha(D/'engine.log'),normal_unchanged=True,original_trusted_gate_satisfied=False,new_frames=0,new_generation_calls=0,completed_at_utc=now());wr(D/'RESULT.json',out);print(json.dumps(out),flush=True)
except Exception as e:wr(D/'STOP.json',dict(role='DIAGNOSTIC_ONLY_NOT_TRUSTED_GATE',error=str(e),at_utc=now()));raise
