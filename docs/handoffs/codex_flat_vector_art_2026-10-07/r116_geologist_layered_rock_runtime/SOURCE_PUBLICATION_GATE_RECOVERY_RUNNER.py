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
def state(n,**x):wr(S/'PUBLICATION_GATE_RECOVERY_STATE.json',dict(state=n,at_utc=now(),**x))
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
 state('RESUMING_FAILED_REFERENCE_MANIFEST_BOUNDARY_ENGINE_RETAINED')
 v=rd(S/'full_validation/FINAL_RESULT.json');assert v['status']=='PASS_ALL_82_AND_CURRENT_STATIC'and v['probe_count']==82 and v['normal_unchanged']and not v['runtime_changes'];assert gs('rev-parse','HEAD')==BASE and gs('branch','--show-current')==BR;assert rd(P/'MANIFEST.json')['baseline']==BASE
 bind=rd(P/'DELIVERY_SOURCE_BINDING.json')
 for row in bind['files']:
  p=row['path'];assert sha(U/p)==row['current_filesystem_sha256']and digest(git('show',':'+p))==row['staged_blob_sha256'],p
 assert all(not(U/p).exists()for p in bind['runtime_deletions'])
 shutil.copyfile(S/'resume_source_gate_publication.py',P/'SOURCE_PUBLICATION_GATE_RECOVERY_RUNNER.py')
 files=set(gs('diff','--cached','--no-renames','--name-only').splitlines())|{p.relative_to(U).as_posix()for q in[P,A]for p in q.rglob('*')if p.is_file()}|{IP.relative_to(U).as_posix(),(P/'MANIFEST.json').relative_to(U).as_posix()}
 d=rd(IP);d['files']=sorted(files-{IP.relative_to(U).as_posix()});wr(IP,d);existing=sorted(p for p in files if (U/p).is_file() and p!=(P/'MANIFEST.json').relative_to(U).as_posix());subprocess.run(['git','add','-f','--',*existing],cwd=U,check=True,capture_output=True)
 rows=[]
 for p in existing:
  if not(U/p).is_file():continue
  b=git('show',':'+p);rows.append(dict(revision=None,path=p,bytes=len(b),sha256=digest(b),role='Actual whole layered-rock source/candidate/machine/review/provenance payload'))
 for row in rd(P/'REFERENCE_BINDING.json')['references']:
  p=row['path'];b=git('show',BASE+':'+p);assert digest(b)==row['immutable_blob_sha256'];rows.append(dict(revision=BASE,path=p,bytes=len(b),sha256=digest(b),role=row['role'],worktree_original_sha256=row['sha256'],binding=row['binding']))
 manifest=dict(schema='reef.runtime_trial_delivery/1',revision='FV-AUDIT-20261031-R116',baseline=BASE,stable_id='FV-192FA763EF56',files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows),scope='Whole painted PAN layered-rock overlay; two loaded-only consumers updated with no visual credit;8candidate frames+2excluded stale-remap failureframes,8prior baselineframes reused at immutable exactrevision. Original workspaceCRLF source archived exactly; original immutableGitLF pinned separately.',new_generation_calls=1,new_runtime_PNG=1,technical_exports=1,new_bounded_implementation_artifacts=1,new_frame_events=dict(bounded=8,excluded=2,retained=10),runtime_deletions=bind['runtime_deletions'],whole_role_closed=False,accepted_removed=0,mission_complete=False);wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(U).as_posix()],cwd=U,check=True,capture_output=True)
 gates=[gate('FINAL_AUTHORITY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('FINAL_DEVELOPMENT',[sys.executable,'-B','tools/audit_development.py','--base','auto'])];wr(S/'FINAL_PRECOMMIT_GATES.json',gates);assert set(gs('diff','--cached','--no-renames','--name-only').splitlines())<=files and not gs('diff','--name-only')
 subprocess.run(['git','fetch','origin'],cwd=U,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE and gs('rev-parse','origin/dev')==BASE,'Topic/Dev advanced: stop for exactsource reconciliation'
 subprocess.run(['git','commit','-m','Replace Geologist layered-rock SVG with whole painted cutout'],cwd=U,check=True,capture_output=True);rev=gs('rev-parse','HEAD');state('SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev);eol('POSTCOMMIT_EOL_CLEANUP');assert not gs('status','--porcelain');subprocess.run(['git','push','origin',BR],cwd=U,check=True,capture_output=True);state('SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(U).as_posix();mb=git('show',rev+':'+mp);code,b=fetch(rev,mp);assert code==200 and b==mb
 def verify(row):
  rr=row['revision']or rev;code,b=fetch(rr,row['path']);assert code==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return dict(row,revision=rr,http_status=code,verified=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 wr(S/'SOURCE_REMOTE_VERIFICATION.json',dict(schema='reef.remote_delivery_verification/1',repository='Ebonyks/mermaid-roshan-reef',revision=rev,manifest=mp,manifest_sha256=digest(mb),manifest_bytes=len(mb),required_files=len(rows),required_bytes=manifest['required_bytes'],files=verified,access_mode='Anonymous immutable HTTPS GET without Authorization/cookies; exactbytes/SHA256 for manifest/everyrequiredfile',checked_at_utc=now(),state='ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED',limits='Transport/provenance only; formal/device/child/owner/global acceptance remain open.'))
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch',BR,'--limit','8','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=U,text=True,encoding='utf-8'));wr(S/'SOURCE_CI_HANDLES.json',[x for x in runs if x['headSha']==rev]);final=dict(state='SOURCE_DELIVERED_ANONYMOUSLY_VERIFIED_EXACT_CI_PENDING',source_revision=rev,branch=BR,manifest=mp,required_files=len(rows),required_bytes=manifest['required_bytes'],receipt=str(S/'SOURCE_REMOTE_VERIFICATION.json'),source_clean=True,origin_dev_at_publication=BASE,Dev_integrated=False,PR_created=False,recovery='Publication reference bytebinding boundary only; noengine/native replay',completed_at_utc=now());wr(S/'SOURCE_PUBLICATION_FINAL.json',final);wr(S/'PUBLICATION_GATE_RECOVERY_FINAL.json',final);state('TERMINAL_SOURCE_DELIVERY_SUCCESS',**{k:v for k,v in final.items()if k!='state'});print('R116_SOURCE_RECOVERY_DELIVERED',rev,len(rows),flush=True)
except Exception as e:wr(S/'PUBLICATION_GATE_RECOVERY_STOP.json',dict(state='STOPPED_NO_AUTOMATIC_RETRY',error=str(e),at_utc=now(),next='Inspect exactsource/manifest/recovery boundary; nohealthyengine rerun or forcepush.'));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
