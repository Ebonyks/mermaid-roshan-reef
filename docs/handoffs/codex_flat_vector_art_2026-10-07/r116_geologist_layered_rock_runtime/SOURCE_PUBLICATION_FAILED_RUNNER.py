from pathlib import Path
import json,hashlib,subprocess,datetime,os,sys,re,shutil,time,urllib.request,urllib.parse,concurrent.futures
U=Path.cwd();S=Path(__file__).parent;H='docs/handoffs/codex_flat_vector_art_2026-10-07';P=U/H/'r116_geologist_layered_rock_runtime';A=U/'assets_src/imagegen/geologist_layered_rock_20261031';IP=U/'design/audit_impacts/flat-vector-geologist-layered-rock-runtime-20261031.json';BASE='0bd538456b4b7abc9220ca09de072e8577a32014';BR='codex/flat-vector-geologist-pan-runtime-20261017'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def wt(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=U,stderr=subprocess.PIPE)
def gs(*a):return git(*a).decode('utf-8').strip()
def state(n,**x):wr(S/'PUBLICATION_STATE.json',dict(state=n,at_utc=now(),**x))
def gate(label,cmd):
 q=subprocess.run(cmd,cwd=U,capture_output=True,env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8'));b=q.stdout+q.stderr;(S/(label+'.log')).write_bytes(b);assert q.returncode==0,label+' '+b.decode(errors='replace')[-2400:];return dict(gate=label,command=cmd,exit_code=0,log_sha256=digest(b))
def eol(label):
 rows=[]
 for entry in git('status','--porcelain','-z').decode().split('\0'):
  if not entry:continue
  p=entry[3:]
  if p.endswith('.import')and entry[:2]!='??'and(U/p).is_file():
   b=(U/p).read_bytes();old=git('show',':'+p)
   if b.replace(b'\r\n',b'\n')==old.replace(b'\r\n',b'\n'):rows.append(dict(path=p,before_raw_sha256=digest(b),index_sha256=digest(old),lf_sha256=digest(b.replace(b'\r\n',b'\n'))))
 if rows:
  f=S/(label+'_PATHS.txt');wt(f,'\n'.join(x['path']for x in rows)+'\n');subprocess.run(['git','restore','--worktree','--pathspec-from-file='+str(f)],cwd=U,check=True,capture_output=True);assert all(digest((U/x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256']for x in rows)
 wr(S/(label+'.json'),dict(files=rows,count=len(rows),semantics_or_pixels_changed=False,scope='Owned LF-equivalent tracked importsidecars only',checked_at_utc=now()));return rows
def fetch(rev,p):
 req=urllib.request.Request('https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+urllib.parse.quote(p,safe='/'),headers={'User-Agent':'MermaidReef-anonymous-delivery-verifier'})
 for i in range(5):
  try:
   with urllib.request.urlopen(req,timeout=90)as q:return q.status,q.read()
  except Exception:
   if i==4:raise
   time.sleep(2*(i+1))
try:
 state('WAITING_EXISTING_R116_VALIDATION_NO_RESTART');start=time.monotonic()
 while not(S/'full_validation/FINAL_RESULT.json').exists():
  if(S/'VALIDATION_STOP.json').exists():raise RuntimeError('Existing R116 validation stopped; inspect exact handle, no restart')
  assert time.monotonic()-start<10800;time.sleep(15)
 v=rd(S/'full_validation/FINAL_RESULT.json');assert v['status']=='PASS_ALL_82_AND_CURRENT_STATIC'and v['probe_count']==82 and v['normal_unchanged']and not v['runtime_changes'];assert rd(S/'FRAME_REVIEW.json')['all8_candidate_frames_inspected'];assert gs('rev-parse','HEAD')==BASE and gs('branch','--show-current')==BR
 pin=rd(S/'SOURCE_PIN.json');assert all(sha(U/p)==h for p,h in pin['runtime_hashes'].items());assert all(not(U/p).exists()for p in pin['runtime_deletions']);cleanup=eol('DELIVERY_EOL_CLEANUP');shutil.copyfile(S/'DELIVERY_EOL_CLEANUP.json',P/'DELIVERY_EOL_CLEANUP.json');state('PREPARING_ACTUAL_VERIFIED_SOURCE_PAYLOAD')
 for a,b in [('full_validation/FINAL_RESULT.json','LOCAL_82_RESULT.json'),('full_validation/LAUNCH.json','LOCAL_82_LAUNCH.json'),('full_validation/STATIC_RESULT.json','STATIC_RESULT.json'),('full_validation/STATIC_PREFIX.log','STATIC_PREFIX.log'),('full_validation/GAME2D.log','GAME2D.log'),('publish_source.py','SOURCE_PUBLICATION_RUNNER.py')]:shutil.copyfile(S/a,P/b)
 combined=bytearray();index=[]
 for r in v['results']:
  b=Path(r['log']).read_bytes();assert digest(b)==r['log_sha256'];combined.extend(('=== '+r['probe']+' ===\n').encode());offset=len(combined);combined.extend(b);combined.extend(b'\n');index.append(dict(probe=r['probe'],offset=offset,bytes=len(b),sha256=digest(b),passed=r['passed'],exit_code=r['exit_code']))
 (P/'TRUSTED_PROBES.log').write_bytes(combined);wr(P/'TRUSTED_LOG_INDEX.json',dict(combined_log_sha256=digest(combined),preserves_every_original_probe_log_byte=True,entries=index))
 status=rd(P/'STATUS.json');status.update(state='PAINTED_LAYERED_ROCK_NATIVE_LOCAL82_STATIC_PASS_SOURCE_CI_DEV_PENDING',current_static='PASS',local82='PASS_ALL_82_AND_CURRENT_STATIC',source_CI=None,Dev_integrated=False,new_bounded_implementation_artifacts=1,new_frame_events=dict(bounded=8,excluded=2,retained=10));wr(P/'STATUS.json',status)
 wt(P/'README.md',(P/'README.md').read_text()+'\nCurrent static gates and all82trusted probes pass on the actual frozen candidate. [Machine evidence](LOCAL_82_RESULT.json) and [source binding](DELIVERY_SOURCE_BINDING.json). ExactsourceCI/Dev and all formal/external/global acceptance remain independent.\n')
 d=rd(IP);d['validation'].append(dict(command='Actual frozen currentstatic/import/all82/native candidate and all8directly reviewed frames',result='PASS',evidence=P.relative_to(U).as_posix()+'/LOCAL_82_RESULT.json; FRAME_REVIEW.json; SOURCE_PIN.json; exactsourceCI/Dev/formal/external separate'))
 files=set(gs('diff','--name-only').splitlines())|{p.relative_to(U).as_posix()for q in[P,A]for p in q.rglob('*')if p.is_file()}|{'assets/opera/worlds/hotspots/geologist_layered_rock_painted.png','assets/opera/worlds/hotspots/geologist_layered_rock_painted.png.import'}|{(P/'DELIVERY_SOURCE_BINDING.json').relative_to(U).as_posix(),(P/'MANIFEST.json').relative_to(U).as_posix()};files.discard(IP.relative_to(U).as_posix());d['files']=sorted(files);wr(IP,d);files.add(IP.relative_to(U).as_posix())
 existing=sorted(p for p in files if not p.endswith(('/DELIVERY_SOURCE_BINDING.json','/MANIFEST.json')));subprocess.run(['git','add','-f','--',*existing],cwd=U,check=True,capture_output=True)
 cleanup_by={x['path']:x for x in cleanup};binding=[]
 for p,tested in sorted(pin['runtime_hashes'].items()):
  b=(U/p).read_bytes();staged=git('show',':'+p)
  if digest(b)!=tested:assert p in cleanup_by and cleanup_by[p]['before_raw_sha256']==tested and digest(b.replace(b'\r\n',b'\n'))==cleanup_by[p]['lf_sha256'],p
  assert b==staged or b.replace(b'\r\n',b'\n')==staged.replace(b'\r\n',b'\n'),p
  binding.append(dict(path=p,tested_filesystem_sha256=tested,current_filesystem_sha256=digest(b),staged_blob_sha256=digest(staged),binding='EXACT_BYTES'if b==staged and digest(b)==tested else'EXPLICIT_CRLF_LF_EQUIVALENCE_ONLY'))
 wr(P/'DELIVERY_SOURCE_BINDING.json',dict(source_pin='SOURCE_PIN.json',files=binding,runtime_deletions=pin['runtime_deletions'],no_gameplay_or_pixel_change=True));subprocess.run(['git','add','--',(P/'DELIVERY_SOURCE_BINDING.json').relative_to(U).as_posix()],cwd=U,check=True,capture_output=True)
 rows=[]
 for p in sorted(files-{(P/'MANIFEST.json').relative_to(U).as_posix()}):
  if not(U/p).is_file():continue
  b=git('show',':'+p);rows.append(dict(revision=None,path=p,bytes=len(b),sha256=digest(b),role='Actual whole layered-rock source/candidate/machine/review/provenance payload'))
 # Exact unchanged context and style references are immutable baseline dependencies, not recursive prior archives.
 for row in rd(P/'REFERENCE_BINDING.json')['references']:
  p=row['path'];b=git('show',BASE+':'+p);assert digest(b)==row['sha256'];rows.append(dict(revision=BASE,path=p,bytes=len(b),sha256=digest(b),role=row['role']))
 manifest=dict(schema='reef.runtime_trial_delivery/1',revision='FV-AUDIT-20261031-R116',baseline=BASE,stable_id='FV-192FA763EF56',files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows),scope='Whole painted PAN layered-rock overlay; two loaded-only consumers updated with no visual credit;8candidate frames+2excluded stale-remap failureframes,8prior baseline frames reused at immutable exactrevision.',new_generation_calls=1,new_runtime_PNG=1,technical_exports=1,new_bounded_implementation_artifacts=1,new_frame_events=dict(bounded=8,excluded=2,retained=10),runtime_deletions=pin['runtime_deletions'],whole_role_closed=False,accepted_removed=0,mission_complete=False);wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(U).as_posix()],cwd=U,check=True,capture_output=True)
 gates=[gate('FINAL_AUTHORITY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('FINAL_DEVELOPMENT',[sys.executable,'-B','tools/audit_development.py','--base','auto'])];wr(S/'FINAL_PRECOMMIT_GATES.json',gates);assert set(gs('diff','--cached','--name-only').splitlines())<=files and not gs('diff','--name-only')
 subprocess.run(['git','fetch','origin'],cwd=U,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE and gs('rev-parse','origin/dev')==BASE,'Topic/Dev advanced: stop for exactsource reconciliation'
 subprocess.run(['git','commit','-m','Replace Geologist layered-rock SVG with whole painted cutout'],cwd=U,check=True,capture_output=True);rev=gs('rev-parse','HEAD');state('SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev);eol('POSTCOMMIT_EOL_CLEANUP');assert not gs('status','--porcelain');subprocess.run(['git','push','origin',BR],cwd=U,check=True,capture_output=True);state('SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(U).as_posix();mb=git('show',rev+':'+mp);code,b=fetch(rev,mp);assert code==200 and b==mb
 def verify(row):
  rr=row['revision']or rev;code,b=fetch(rr,row['path']);assert code==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return dict(row,revision=rr,http_status=code,verified=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 wr(S/'SOURCE_REMOTE_VERIFICATION.json',dict(schema='reef.remote_delivery_verification/1',repository='Ebonyks/mermaid-roshan-reef',revision=rev,manifest=mp,manifest_sha256=digest(mb),manifest_bytes=len(mb),required_files=len(rows),required_bytes=manifest['required_bytes'],files=verified,access_mode='Anonymous immutable HTTPS GET without Authorization/cookies; exactbytes/SHA256 for manifest/everyrequiredfile',checked_at_utc=now(),state='ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED',limits='Transport/provenance only; formal/device/child/owner/global acceptance remain open.'))
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch',BR,'--limit','8','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=U,text=True,encoding='utf-8'));wr(S/'SOURCE_CI_HANDLES.json',[x for x in runs if x['headSha']==rev]);final=dict(state='SOURCE_DELIVERED_ANONYMOUSLY_VERIFIED_EXACT_CI_PENDING',source_revision=rev,branch=BR,manifest=mp,required_files=len(rows),required_bytes=manifest['required_bytes'],receipt=str(S/'SOURCE_REMOTE_VERIFICATION.json'),source_clean=True,origin_dev_at_publication=BASE,Dev_integrated=False,PR_created=False,completed_at_utc=now());wr(S/'SOURCE_PUBLICATION_FINAL.json',final);state('TERMINAL_SOURCE_DELIVERY_SUCCESS',**{k:v for k,v in final.items()if k!='state'});print('R116_SOURCE_DELIVERED',rev,len(rows),flush=True)
except Exception as e:wr(S/'PUBLICATION_STOP.json',dict(state='STOPPED_NO_AUTOMATIC_RETRY',error=str(e),at_utc=now(),next='Inspect exacthandle/source/log; never restart a healthy engine or duplicate sourcepreparation, no forcepush.'));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
