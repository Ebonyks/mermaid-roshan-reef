from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/current_supplement_gates_v1'
receipt=json.loads((out/'RECEIPT.json').read_text(encoding='utf-8'));assert receipt['status']=='PASS_CURRENT_WORKING_REVIEW_GATES'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git',*args],cwd=r,capture_output=True,check=True).stdout
def names(*args):return [x.decode('utf-8') for x in git(*args,'-z').split(b'\0') if x]
head=git('rev-parse','HEAD').decode().strip();assert head=='fb03e0ac3dda1658e9ea188d33cc6e084871642b'
records=[r/'design/audit_impacts'/name for name in ['job-review-separate-v2-20261001.json','job-wash-contact-study-20261001.json','job-review-current-remote-receipt-20261001.json','job-doctor-local-rub-study-20261001.json']]
publication=records[2];d=json.loads(publication.read_text(encoding='utf-8'))
selfcopy=out/'executed_stage_and_verify_review_supplement_v52.py';shutil.copyfile(__file__,selfcopy)
verification=out/'STAGED_REVIEW_VERIFICATION.json'
filemap=r/'audit/job_review_v2_20261001/CURRENT_REVIEW_SUPPLEMENT_FILES_V1.json'
d['files']=sorted(set(d['files'])|{selfcopy.relative_to(r).as_posix(),verification.relative_to(r).as_posix(),filemap.relative_to(r).as_posix(),*[str((out/(n+suffix)).relative_to(r).as_posix()) for n in ['parser','inference','final_authority','final_development'] for suffix in ['.stdout.log','.stderr.log']]})
d['validation'].append({'command':'Exact staged source/coverage and parser/inference verification','result':'PENDING','evidence':verification.relative_to(r).as_posix()+'; populated before commit; no game source changes or threshold edits.'});write(publication,d)
allowed={p for record in records for p in json.loads(record.read_text(encoding='utf-8'))['files']}
allowed.update(x.relative_to(r).as_posix() for x in records)
tracked=set(names('ls-files'));changed=set(names('diff','--name-only','HEAD'))
uncovered=changed-allowed;assert not uncovered,sorted(uncovered)
to_stage=sorted({p for p in allowed if (r/p).is_file() and (p in changed or p not in tracked)})
for p in to_stage:assert not p.startswith(('.github/','.codex/','.claude/','.secrets/','assets/book/','assets/audio/voices/','assets/characters/friends/')) and p not in ['AGENTS.md','CLAUDE.md','SECURITY.md','project.godot']
stagefile=r/'tmp/review_supplement_v52_pathspec.txt';stagefile.write_bytes(b'\0'.join(p.encode() for p in to_stage)+b'\0')
git('add','--force','--pathspec-from-file='+str(stagefile),'--pathspec-file-nul')
changed_gd=[p for p in names('diff','--cached','--name-only') if p.endswith('.gd')]
rows=[]
for name,cmd in [('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*changed_gd]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*changed_gd]),('final_authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('final_development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 assert changed_gd or name not in ['parser','inference']
 with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW,timeout=240)
 rows.append({'name':name,'process_exit':p.returncode,'command':cmd,'stdout':(out/(name+'.stdout.log')).relative_to(r).as_posix(),'stderr':(out/(name+'.stderr.log')).relative_to(r).as_posix()})
 assert p.returncode==0,name
literal=json.loads((r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text(encoding='utf-8'))['source_files']
assert len(literal)==325 and all(sha(r/x['path'])==x['sha256'] for x in literal)
record_snapshot={x.relative_to(r).as_posix():sha(x) for x in records}
staged_paths=names('diff','--cached','--name-only')
verificationdata={'status':'PASS_STAGED_REVIEW_COVERAGE_AND_STATIC_GATES','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':head,'staged_before_final_metadata':len(staged_paths),'changed_gd':changed_gd,'processes':rows,'literal_production_source_count':325,'literal_production_sources_unchanged':True,'coverage_record_sha256_before_final_pass_note':record_snapshot,'uncovered_paths':[],'qualification':'Parser/inference and unchanged authority/development gate pass.2D no-regression is separately bound. Local82/82 full suite remains an unchanged325-source boundary with51 diagnostics; no new game source changes. Hosted retry, visual/action/device/child/owner and strict2D acceptance remain open.'}
write(verification,verificationdata)
d=json.loads(publication.read_text(encoding='utf-8'));d['validation'][-1]={'command':'Exact staged source/coverage and parser/inference verification','result':'PASS','evidence':verification.relative_to(r).as_posix()+'; all changed ignored capture scripts parsed/linted;325 production source hashes unchanged; final authority/development pass.'};write(publication,d)
correction=r/'audit/job_review_v2_20261001/STAGING_COVERAGE_CORRECTION_V1.json';v=json.loads(correction.read_text(encoding='utf-8'));v['status']='CORRECTION_STAGED_STATIC_VERIFICATION_PASS_HOSTED_PENDING';v['verification']=verification.relative_to(r).as_posix();write(correction,v)
stagefile.write_bytes(b'\0'.join(p.encode() for p in sorted({p for p in allowed if (r/p).is_file() and (p in changed or p not in tracked)}|{correction.relative_to(r).as_posix()}))+b'\0');git('add','--force','--pathspec-from-file='+str(stagefile),'--pathspec-file-nul')
paths=names('diff','--cached','--name-only');assert not names('diff','--cached','--name-only','--diff-filter=D')
# Hash canonical staged blobs rather than platform-dependent working-tree newlines.
index={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
 if not entry:continue
 info,path=entry.split(b'\t',1);mode,oid,stage=info.split();assert stage==b'0';index[path.decode()]=oid.decode()
batch=subprocess.Popen(['git','cat-file','--batch'],cwd=r,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
files={}
try:
 for path in sorted(paths):
  if path==filemap.relative_to(r).as_posix():continue
  batch.stdin.write((index[path]+'\n').encode());batch.stdin.flush();oid,kind,size=batch.stdout.readline().split();assert kind==b'blob';count=int(size);remaining=count;digest=hashlib.sha256()
  while remaining:chunk=batch.stdout.read(min(1024*1024,remaining));assert chunk;digest.update(chunk);remaining-=len(chunk)
  assert batch.stdout.read(1)==b'\n';files[path]=[count,digest.hexdigest()]
finally:batch.stdin.close();batch.wait(timeout=30)
payload=hashlib.sha256(''.join(p+'\t'+str(n)+'\t'+h+'\n' for p,(n,h) in sorted(files.items())).encode()).hexdigest()
mapdata={'schema':'CURRENT_REVIEW_SUPPLEMENT_FILES_V1','base_revision':head,'base_verified_content_commit':'c2116877de10202c40e1d939c77eb3646b5f202f','payload_revision':'Immutable Git commit containing this manifest; pin the actual commit SHA in the separate remote verifier.','meaning':'Exact new/changed canonical staged blobs relative tofb03. Original c211 full file map remains immutable historical evidence; this supplement does not silently rebind its records.','index_self_excluded':True,'files':files,'required_files':len(files),'required_payload_bytes':sum(x[0] for x in files.values()),'payload_sha256':payload,'qualification':'Review/source/static/motion evidence only; individual/art/action/device/child/owner and hosted gates remain independent.'}
filemap.write_text(json.dumps(mapdata,separators=(',',':'),ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');git('add','--force',filemap.relative_to(r).as_posix())
staged=names('diff','--cached','--name-only');assert set(staged)==set(files)|{filemap.relative_to(r).as_posix()}
for record in records:assert git('show',':'+record.relative_to(r).as_posix()).replace(b'\r\n',b'\n')==record.read_bytes().replace(b'\r\n',b'\n')
# The expanded coverage record is now included in the actual index.
expanded=json.loads(git('show',':design/audit_impacts/job-review-separate-v2-20261001.json'));assert len(expanded['files'])>3900
print(json.dumps({'status':'ALL_REVIEW_CHANGES_STAGED_EXACT_BLOBS_INDEXED','staged_files':len(staged),'mapped_files':len(files),'payload_bytes':mapdata['required_payload_bytes'],'map_sha256':sha(filemap),'expanded_staged_coverage_entries':len(expanded['files']),'changed_gd':len(changed_gd),'production_source_hashes_unchanged':325}))
