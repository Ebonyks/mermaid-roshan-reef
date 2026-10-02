from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out = r / 'audit/job_review_v2_20261001/final_native_supplement_gates_v3'
base = '56d66f63e375b61cf02936b426a05a2b92c14d3b'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rel(p): return p.relative_to(r).as_posix()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a): return subprocess.run(['git',*a],cwd=r,capture_output=True,check=True).stdout
def names(*a): return [p.decode() for p in git(*a,'-z').split(b'\0') if p]
assert git('rev-parse','HEAD').decode().strip() == base
assert not names('diff','--cached','--name-only')
gate = read(out/'RECEIPT.json')
assert gate['status']=='PASS_FINAL_SCOPED_NATIVE_SUPPLEMENT_GATES' and gate['literal_sources_unchanged']
spec = read(r/'tmp/native_supplement_scope_v81.json')
assert spec['baseline']==base
filemap = r/'audit/job_review_v2_20261001/CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2.json'
assert not filemap.exists()
selfcopy = out/'executed_stage_native_job_art_supplement_v82.py'
assert not selfcopy.exists()
shutil.copyfile(__file__,selfcopy)
verification = out/'STAGED_NATIVE_REVIEW_VERIFICATION.json'
recordfile = r/'design/audit_impacts/job-native-final-supplement-gates-20261001.json'
record = read(recordfile)
planned = {rel(verification),rel(filemap)} | {rel(out/(n+s)) for n in ['staged_authority','staged_development','contract_tests'] for s in ['.stdout.log','.stderr.log']}
record['files'] = sorted(set(record['files']) | {rel(selfcopy)} | planned)
record['validation'].append(dict(command='Exact staged canonical-blob map and final scoped coverage verification',result='PENDING',evidence=rel(verification)))
write(recordfile,record)
for p in planned - {rel(filemap),rel(verification)}: (r/p).write_bytes(b'')
write(verification,dict(status='PREPARED_FINAL_STAGED_VERIFICATION',baseline=base,qualification='Not yet verified. This placeholder is finalized before creating the immutable staged-blob map.'))
scope = set(spec['scope']) | {rel(filemap)}
for folder in spec['folders']: scope |= {rel(p) for p in (r/folder).rglob('*') if p.is_file()}
tracked = set(names('ls-files'))
changed = set(names('diff','--name-only','HEAD'))
assert changed <= scope, sorted(changed-scope)
assert not names('diff','--name-only','--diff-filter=D')
paths = sorted(p for p in scope if (r/p).is_file() and (p in changed or p not in tracked))
for p in paths:
    assert not p.startswith(('.github/','.codex/','.claude/','.secrets/','assets/book/','assets/audio/voices/','assets/characters/friends/'))
    assert p not in ['AGENTS.md','CLAUDE.md','SECURITY.md','project.godot']
pathspec = r/'tmp/native_job_art_supplement_v82_pathspec.txt'
def stage(ps):
    pathspec.write_bytes(b'\0'.join(p.encode() for p in sorted(ps))+b'\0')
    git('add','--force','--pathspec-from-file='+str(pathspec),'--pathspec-file-nul')
stage(paths)
processes=[]
for name,cmd in [('staged_authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('staged_development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('contract_tests',[sys.executable,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])]:
    with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:
        proc=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,timeout=900,creationflags=subprocess.CREATE_NO_WINDOW)
    processes.append(dict(name=name,command=cmd,process_exit=proc.returncode,stdout=rel(out/(name+'.stdout.log')),stderr=rel(out/(name+'.stderr.log'))))
    print(name,proc.returncode,flush=True)
    if proc.returncode:
        print((out/(name+'.stdout.log')).read_text(encoding='utf-8',errors='replace')[-2500:],(out/(name+'.stderr.log')).read_text(encoding='utf-8',errors='replace')[-2500:],flush=True)
        raise SystemExit(1)
snapshot=read(r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json')['source_files']
assert len(snapshot)==325 and all(sha(r/x['path'])==x['sha256'] for x in snapshot)
staged=names('diff','--cached','--name-only')
recordnames=[p for p in staged if p.startswith('design/audit_impacts/') and p.endswith('.json')]
coverage=set()
for p in recordnames: coverage.update(json.loads(git('show',':'+p))['files'])
uncovered=set(staged)-coverage-set(recordnames)
assert not uncovered, sorted(uncovered)
expanded=json.loads(git('show',':design/audit_impacts/job-review-separate-v2-20261001.json'))
assert len(expanded['files'])>=3956
write(verification,dict(status='PASS_FINAL_STAGED_NATIVE_REVIEW_COVERAGE',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline=base,changed_before_final_metadata=len(staged),actual_staged_impact_records=recordnames,uncovered_paths=[],expanded_actual_staged_coverage_entries=len(expanded['files']),processes=processes,literal_source_count=325,literal_production_sources_unchanged=True,source_guard_snapshot='audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json',qualification='Review-only supplement. Exact C hosted success remains bound to C. Five selected vector sources meet source4.5,94 static washing views still fail and41 local motion-reference frames remain4.0. Source scores do not grant current mounted/action/device/child/owner, strict2D, dev integration or release acceptance.'))
record=read(recordfile)
record['validation'][-1]=dict(command='Exact staged canonical-blob map and final scoped coverage verification',result='PASS',evidence=rel(verification)+'; final authority/development and contract tests pass;325 source hashes unchanged; actual staged expanded impact included.')
write(recordfile,record)
stage(paths)
assert not names('diff','--name-only'), 'Unstaged tracked changes remain'
staged=names('diff','--cached','--name-only')
assert not names('diff','--cached','--name-only','--diff-filter=D')
index={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry: continue
    info,path=entry.split(b'\t',1);mode,oid,stage_num=info.split()
    assert stage_num==b'0';index[path.decode()]=oid.decode()
batch=subprocess.Popen(['git','cat-file','--batch'],cwd=r,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
files={}
try:
    for path in sorted(staged):
        assert path!=rel(filemap)
        batch.stdin.write((index[path]+'\n').encode());batch.stdin.flush()
        oid,kind,size=batch.stdout.readline().split();assert kind==b'blob'
        count=int(size);remaining=count;digest=hashlib.sha256()
        while remaining:
            chunk=batch.stdout.read(min(1024*1024,remaining));assert chunk
            digest.update(chunk);remaining-=len(chunk)
        assert batch.stdout.read(1)==b'\n'
        files[path]=[count,digest.hexdigest()]
finally:
    batch.stdin.close();batch.wait(timeout=30)
payload=hashlib.sha256(''.join(p+'\t'+str(n)+'\t'+h+'\n' for p,(n,h) in sorted(files.items())).encode()).hexdigest()
data=dict(schema='CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2',base_revision=base,prior_closed_map='audit/job_review_v2_20261001/CURRENT_REVIEW_SUPPLEMENT_FILES_V1.json',payload_revision='Immutable Git commit containing this map; bind the actual published SHA in a separate verification receipt.',meaning='Exact new/changed canonical staged blobs relative to56d66. Earlier c211 and C maps/receipts stay immutable and are not rebound to this supplement.',index_self_excluded=True,payload_hash_formula='SHA256 of sorted UTF-8 lines: path TAB decimal bytes TAB lowercase sha256 LF',files=files,required_files=len(files),required_payload_bytes=sum(x[0] for x in files.values()),payload_sha256=payload,qualification='Source/region/native-static/local-motion-reference review evidence. No all-game floor, mounted-action/device/child/owner acceptance, integration or release.')
filemap.write_text(json.dumps(data,separators=(',',':'),ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
stage([rel(filemap)])
assert set(names('diff','--cached','--name-only'))==set(files)|{rel(filemap)}
assert not names('diff','--name-only')
for p in recordnames: assert git('show',':'+p).replace(b'\r\n',b'\n')==(r/p).read_bytes().replace(b'\r\n',b'\n')
result=dict(status='ALL_NATIVE_REVIEW_CHANGES_STAGED_EXACT_CANONICAL_BLOBS',baseline=base,staged_files=len(files)+1,mapped_files=len(files),payload_bytes=data['required_payload_bytes'],payload_sha256=payload,map_path=rel(filemap),map_sha256=sha(filemap),map_bytes=filemap.stat().st_size,literal_production_sources_unchanged=325,expanded_staged_coverage_entries=len(expanded['files']))
write(r/'tmp/native_job_art_supplement_v82_STAGED.json',result)
print(json.dumps(result),flush=True)
