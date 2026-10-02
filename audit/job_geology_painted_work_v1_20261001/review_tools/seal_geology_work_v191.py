from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
work=b/'audit/job_geology_painted_work_v1_20261001';out=b/'tmp/geology_work_seal_v191';out.mkdir(exist_ok=False)
baseline='e1b431f49258eef1d293b11a732353f0a3aa12e9';mp='audit/job_review_v2_20261001/GEOLOGY_PAINTED_WORK_REVIEW_SUPPLEMENT_FILES_V7.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):
 q=subprocess.run(['git',*args],cwd=b,input=input,capture_output=True,check=True)
 if q.stderr:(out/'git.stderr.log').open('ab').write(q.stderr)
 return q.stdout
assert git('rev-parse','HEAD').decode().strip()==baseline
assert git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
assert not git('diff','--cached','--name-only').strip(),'Never absorb unrelated staged work.'
ci=read(work/'full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['source_checks'])==349 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
for gate in ['parserv5','inferencev5','authorityv2','developmentv2','2dv1']:
 assert read(work/('runtime_gate/'+gate+'.receipt.json'))['status']=='PASS',gate
# Durable helper and explicit audit-impact file coverage precede staging.
target=work/'review_tools'/Path(__file__).name;shutil.copyfile(__file__,target)
ipaths=[b/'design/audit_impacts'/n for n in ['job-geology-painted-work-20261001.json','job-geology-river-painted-source-20261001.json']]
d=read(ipaths[0]);d['files']=sorted(set(d['files'])|{target.relative_to(b).as_posix(),mp});write(ipaths[0],d)
for name,args in [('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 q=subprocess.run(args,cwd=b,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(name+'.stdout.log')).write_bytes(q.stdout);(out/(name+'.stderr.log')).write_bytes(q.stderr)
 assert q.returncode==0,(name,q.stdout.decode(errors='replace')[-2000:])
 print('Precommit seal '+name+':PASS',flush=True)
scope=set().union(*(set(read(p)['files'])|{p.relative_to(b).as_posix()} for p in ipaths))
assert mp in scope
for path in scope:
 resolved=(b/path).resolve();assert resolved.is_relative_to(b.resolve()) and resolved.is_file(),path
assert not any(p.startswith(('.git/','.secrets/','.codex/','.claude/','.github/')) for p in scope)
literal=''.join(p+'\0' for p in sorted(scope)).encode();git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=literal)
paths={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};assert paths<=scope and mp in paths
payload=sorted(paths-{mp});assert len(payload)>250
data=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in payload).encode());off=0;files={}
for path in payload:
 end=data.index(b'\n',off);header=data[off:end].split();assert header[1]==b'blob';n=int(header[2]);off=end+1;raw=data[off:off+n];off+=n+1;files[path]=[len(raw),hashlib.sha256(raw).hexdigest()]
assert off==len(data)
prior='audit/job_review_v2_20261001/GEOLOGY_RUNTIME_REVIEW_SUPPLEMENT_FILES_V6.json';priorbytes=git('show','HEAD:'+prior)
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m={'schema':'reef.immutable-review-supplement.v1','base_revision':baseline,'prior_closed_map':prior,'prior_closed_map_sha256':hashlib.sha256(priorbytes).hexdigest(),'required_files':len(files),'required_payload_bytes':sum(v[0] for v in files.values()),'payload_sha256':hashlib.sha256(formula).hexdigest(),'payload_hash_formula':'SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF','files':files,'qualification':'Additive exact canonical Git-blob map for seven painted-work runtime sources, all46 current/174 archived native views, two soil generations, six river components/two originals/two complete derivatives and V22 individual register1596. Current unmodified officialGodot4.7.2 local full suite82/82;349 literal hashes unchanged;53 raw diagnostics preserved. Source/mounted/action/context scores remain separately qualified. River components are unbound. Prior immutable map chain retains baseline dependency evidence; this supplement never rewrites old receipts or grants full timed/training/story/device/child/owner/all-job/integration/release acceptance.'}
write(b/mp,m);git('add','--',mp);raw=git('show',':'+mp)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(files)|{mp}
seal={'status':'EXACT_CANONICAL_CURRENT_SCOPED_BLOBS_SEALED','base_revision':baseline,'map_path':mp,'map_sha256':hashlib.sha256(raw).hexdigest(),'payload_sha256':m['payload_sha256'],'payload_files':len(files),'payload_bytes':m['required_payload_bytes'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Exact staged topic-only checkpoint; publisher repeats blob, full-suite and349-source checks before commit/push and anonymously verifies remote bytes.'}
write(b/'tmp/geology_work_v182_sealed.json',seal);write(out/'RECEIPT.json',seal)
print(json.dumps(seal),flush=True)
