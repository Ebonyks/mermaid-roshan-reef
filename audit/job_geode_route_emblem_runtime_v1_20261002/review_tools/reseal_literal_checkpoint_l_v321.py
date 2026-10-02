from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
out=r/'tmp/checkpoint_l_literal_reseal_v321';out.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):return subprocess.run(['git',*args],cwd=r,input=input,capture_output=True,check=True).stdout
seal=read(r/'tmp/geology_checkpoint_l_sealed.json');mp=seal['map_path'];m=json.loads(git('show',':'+mp))
assert git('rev-parse','HEAD').decode().strip()==seal['base_revision']
ci=read(f/'full_ci_v2/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['source_checks'])==373
failed='audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/ENGINE_DIAGNOSTICS.json'
raw=(r/failed).read_bytes();staged=git('show',':'+failed)
record=f/'LITERAL_BYTE_STAGING_CORRECTION_V321.json'
d=dict(status='LITERAL_RESTAGING_PENDING',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),earlier_unpublished_staging_failure=dict(path=failed,literal_bytes=len(raw),literal_sha256=hashlib.sha256(raw).hexdigest(),staged_bytes=len(staged),staged_sha256=hashlib.sha256(staged).hexdigest()),cause='Git add retained stat-clean already-staged normalized text after adding byte-preservation attributes. Explicit exact-scope renormalization is required for those new review files.',qualification='No raw working evidence was altered or published in the failed staging attempt. Existing closed maps and unrelated files are outside the correction scope.')
write(record,d);shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';impact=read(ip);impact['files']=sorted(set(impact['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{'.gitattributes'});write(ip,impact)
for gate in ['authorityv6','developmentv6']:
 q=subprocess.run([sys.executable,'-X','utf8','-B',str(f/'review_tools/run_geode_route_gates_v276.py'),gate],cwd=r,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(gate+'.stdout.log')).write_bytes(q.stdout);(out/(gate+'.stderr.log')).write_bytes(q.stderr);print(q.stdout.decode().strip(),flush=True);assert q.returncode==0
ipaths=[r/'design/audit_impacts'/n for n in ['job-geode-route-emblem-runtime-20261002.json','job-wash-root-doctor-sequence-review-20261002.json','job-wash-root-remaining-sequences-review-20261002.json']]
scope=set().union(*(set(read(p)['files'])|{p.relative_to(r).as_posix()} for p in ipaths));scope.add(mp)
staged_paths={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};assert staged_paths<=scope
literal=''.join(p+'\0' for p in sorted(scope)).encode();git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=literal)
git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',input=literal)
groups=[f,r/'audit/job_wash_root_doctor_sequence_v1_20261002',r/'audit/job_wash_root_remaining_sequences_v1_20261002']
# Exact staged raw-log proof precedes acceptance of this restaging.
for relative,expected in [('audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/stdout.log',ci['stdout_sha256']),('audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/stderr.log',ci['stderr_sha256'])]:assert hashlib.sha256(git('show',':'+relative)).hexdigest()==expected,relative
d.update(status='PASS_EXACT_LITERAL_STAGED_STREAMS_AND_FAMILIES',verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),current_full_ci_source_count=373,current_full_ci_source_unchanged=True,method='Exact scoped git add --renormalize after -text attribute declarations, followed by literal working/staged byte comparison of every file in the three new evidence families.')
write(record,d);git('add','-f','--',record.relative_to(r).as_posix())
paths={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};assert paths<=scope
payload=sorted(paths-{mp});data=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in payload).encode());offset=0;files={}
for path in payload:
 end=data.index(b'\n',offset);header=data[offset:end].split();assert header[1]==b'blob';size=int(header[2]);offset=end+1;blob=data[offset:offset+size];offset+=size+1;files[path]=[len(blob),hashlib.sha256(blob).hexdigest()]
assert offset==len(data)
for group in groups:
 for p in group.rglob('*'):
  rel=p.relative_to(r).as_posix()
  if p.is_file() and rel in files:
   raw=p.read_bytes();assert files[rel]==[len(raw),hashlib.sha256(raw).hexdigest()],rel
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
assert len(m['unchanged_required_files'])==2077 and not set(m['unchanged_required_files'])&set(files)
assert hashlib.sha256(git('show','HEAD:'+m['prior_closed_map'])).hexdigest()==m['prior_closed_map_sha256']
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m.update(files=files,required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=hashlib.sha256(formula).hexdigest())
write(r/mp,m);git('add','-f','--',mp);raw=git('show',':'+mp)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(files)|{mp}
seal.update(status='EXACT_CURRENT_LITERAL_SCOPED_BLOBS_SEALED',map_sha256=hashlib.sha256(raw).hexdigest(),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),current_document_gates=['authorityv6','developmentv6'],literal_stream_hashes_match_receipts=True)
write(r/'tmp/geology_checkpoint_l_sealed.json',seal);write(out/'RECEIPT.json',seal)
print(json.dumps(seal),flush=True)
