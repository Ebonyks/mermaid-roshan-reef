from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_current_recheck_v1_20261002';p=b/'audit/job_nursery_wash_connected_v1_20261002/remote_verified_v1';baseline='c2538760639d79b063152ce5530807c04545ba6e';mp='audit/job_review_v2_20261001/CURRENT_GEODE_RECHECK_SUPPLEMENT_FILES_V13.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):return subprocess.run(['git',*args],cwd=b,input=input,capture_output=True,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()==baseline
assert git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
target=f/'review_tools'/Path(__file__).name
if target.resolve()!=Path(__file__).resolve():shutil.copyfile(__file__,target)
ips=[b/'design/audit_impacts/job-geode-current-recheck-20261002.json',b/'design/audit_impacts/job-nursery-published-verification-20261002.json']
gip=read(ips[0]);gip['files']=sorted(set(gip['files'])|{x.relative_to(b).as_posix() for x in f.rglob('*') if x.is_file()}|{mp});write(ips[0],gip)
if not (b/mp).exists():write(b/mp,dict(status='PREPARING_EXACT_SCOPED_REVIEW_MAP',base_revision=baseline))
def stage():
 scope={x.relative_to(b).as_posix() for x in ips}
 for ip in ips:scope.update(read(ip)['files'])
 for rel in scope:
  q=(b/rel).resolve();assert q.is_relative_to(b.resolve()) and q.is_file(),rel
  assert not rel.startswith(('.git/','.secrets/','.codex/','.claude/','.github/','assets/book/','assets/audio/voices/','assets/characters/friends/')),rel
 already={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert already<=scope
 paths=''.join(x+'\0' for x in sorted(scope)).encode();git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=paths)
 git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',input=paths)
 changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope
 assert not any(x.startswith('scripts/') or x.startswith('assets/') for x in changed),'This checkpoint has no production changes.'
 return scope,changed
action=sys.argv[1]
if action=='stage':
 scope,changed=stage();print('P_SCOPED_REVIEW_STAGE|'+str(len(changed))+' changed|'+str(len(scope))+' covered|production unchanged');raise SystemExit(0)
if action in ['authority','development']:
 gate=f/'runtime_gate';paths=[gate/(action+'_final_v3.'+x) for x in ['stdout.log','stderr.log','receipt.json']];assert not any(x.exists() for x in paths)
 d=read(ips[0]);d['files']=sorted(set(d['files'])|{x.relative_to(b).as_posix() for x in paths});write(ips[0],d)
 command=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B','tools/audit_document_authority.py' if action=='authority' else 'tools/audit_development.py']
 if action=='development':command+=['--base','auto']
 paths[0].touch();paths[1].touch();write(paths[2],dict(status='PENDING_NOT_RUN',command=command));stage();started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with paths[0].open('wb') as out,paths[1].open('wb') as err:result=subprocess.run(command,cwd=b,stdout=out,stderr=err,timeout=420,creationflags=subprocess.CREATE_NO_WINDOW)
 receipt=dict(status='PASS' if result.returncode==0 else 'FAIL_PRESERVED',command=command,process_exit=result.returncode,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,stdout_sha256=sha(paths[0].read_bytes()),stderr_sha256=sha(paths[1].read_bytes()),qualification='Machine/document traceability only; no visual/device/child/owner/integration/release acceptance.')
 write(paths[2],receipt);d=read(ips[0]);d['validation'].append(dict(command=' '.join(command),result='PASS' if result.returncode==0 else 'FAIL',evidence=paths[2].relative_to(b).as_posix()));write(ips[0],d);stage();print('P_GATE|'+action+'|'+receipt['status']);
 if result.returncode:print(paths[0].read_text(errors='replace')[-7000:]);raise SystemExit(result.returncode)
 raise SystemExit(0)
assert action=='seal'
for label in ['authority_final_v3','development_final_v3','parser_v1','inference_v1','analyzer_v1']:assert read(f/'runtime_gate'/(label+'.receipt.json'))['status']=='PASS'
assert read(f/'BROWSER_QA_V394.json')['status']=='PASS_REVIEW_UI_ONLY'
snap=read(f/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(snap)==783 and all(sha((b/x['path']).read_bytes())==x['sha256'] for x in snap)
assert read(b/'audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json')['status']=='CURRENT_CAPTURE_BOUNDARIES_MATCH'
scope,changed=stage()
def blobs(ref,paths):
 result={};proc=subprocess.Popen(['git','cat-file','--batch'],cwd=b,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for path in paths:
  proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush();head=proc.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path;n=int(head[2]);left=n;digest=hashlib.sha256()
  while left:block=proc.stdout.read(min(left,65536));assert block,path;left-=len(block);digest.update(block)
  assert proc.stdout.read(1)==b'\n';result[path]=[n,digest.hexdigest()]
 proc.stdin.close();assert proc.wait(timeout=30)==0;return result
files=blobs('',sorted(changed-{mp}));prior='audit/job_review_v2_20261001/CONNECTED_NURSERY_WASH_SUPPLEMENT_FILES_V12.json';old=read(b/prior)
refs=set(old['files'])|set(old['unchanged_required_files'])|{prior};refs-=set(files)|{mp}
unchanged=blobs('HEAD',sorted(refs));formula=''.join(path+'\t'+str(v[0])+'\t'+v[1]+'\n' for path,v in sorted(files.items())).encode()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=baseline,prior_closed_map=prior,prior_closed_map_sha256=sha(git('show','HEAD:'+prior)),required_files=len(files),required_payload_bytes=sum(x[0] for x in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,qualification='Current Geologist review checkpoint only:58 selected canvases/318 current geode opening-celebration-earned return frames,37 boards/24 native details directly reviewed;27 bounded opinions/23 inclusive priorities,1778-entry V35 library with exact V34.1 originals preserved. Opening/mounting4.5/rooted material4.6 remain provisional; room2.8/contact2.7/clearing3.9/pan selected-action relationship3.8/whole stage4.1 remain weak. Actual Library caller all four ordinary phases/earned room return and actual Opera elevator developer entry/Back; separate birthday/two-act Geologist route absent. Other complete timed task motions/device/child/owner/all-job completion remain open. No production changes;783 current literal source hashes unchanged, current unmodified official Godot4.7.2 local82/82 receipt with53 raw diagnostics separately retained; generated UID publication snapshots remain non-runtime QA as declared in prior boundary bridge. Durable previousO verification receipt names exactc253 revision and every15118 anonymous remote required member; hostedO remains pending in its dated snapshot. Nursery targeted reference upload and preview-tab persistence remain blocked awaiting separate explicit authorization; no bypass or acceptance granted. No dev/master integration or release.')
write(b/mp,m);git('add','-f','--',mp);raw=git('show',':'+mp)
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{mp}
seal=dict(status='EXACT_SCOPED_P_BLOBS_SEALED',base_revision=baseline,map_path=mp,map_sha256=sha(raw),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],unchanged_required_files=len(unchanged),checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Exact topic review checkpoint; anonymous immutable remote verification and current hosted probes pending. No creative acceptance or blocked-action authorization.')
out=b/'tmp/current_review_checkpoint_p_sealed_v395.json';assert not out.exists();write(out,seal);print(json.dumps(seal))
