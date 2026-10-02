from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
work=b/'audit/job_geode_coherent_runtime_v1_20261002';out=b/'tmp/geology_checkpoint_k_seal_v274';out.mkdir(exist_ok=False)
baseline='c6f03791aee93f1443d423dd50334804e37313fb';mp='audit/job_review_v2_20261001/GEOLOGY_COHERENT_GEODE_ROUTE_REVIEW_SUPPLEMENT_FILES_V9.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):
 q=subprocess.run(['git',*args],cwd=b,input=input,capture_output=True,check=True)
 if q.stderr:(out/'git.stderr.log').open('ab').write(q.stderr)
 return q.stdout
assert git('rev-parse','HEAD').decode().strip()==baseline
assert git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
assert not git('diff','--cached','--name-only').strip(),'Never absorb unrelated staged work.'
ci=read(work/'full_ci_v3/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['source_checks'])==368 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
for gate in ['parserv2','inferencev2','authorityv1','developmentv1','2dv1']:
 assert read(work/('runtime_gate/'+gate+'.receipt.json'))['status']=='PASS',gate
# Durable helper and explicit audit-impact file coverage precede staging.
target=work/'review_tools'/Path(__file__).name;shutil.copyfile(__file__,target)
ipaths=[b/'design/audit_impacts'/n for n in ['job-geode-coherent-runtime-20261002.json','job-geology-room-route-review-20261002.json','job-geology-geode-emblem-reuse-20261002.json','job-geology-grotto-native-resolution-20261002.json','job-training-shared-source-review-20261002.json']]
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
prior='audit/job_review_v2_20261001/GEOLOGY_RIVER_GEODE_REVIEW_SUPPLEMENT_FILES_V8.json';priorbytes=git('show','HEAD:'+prior)
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m={'schema':'reef.immutable-review-supplement.v1','base_revision':baseline,'prior_closed_map':prior,'prior_closed_map_sha256':hashlib.sha256(priorbytes).hexdigest(),'required_files':len(files),'required_payload_bytes':sum(v[0] for v in files.values()),'payload_sha256':hashlib.sha256(formula).hexdigest(),'payload_hash_formula':'SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF','files':files,'qualification':'Additive canonical Git-blob checkpoint: reversible actual seven-state coherent geode; every312 dedicated opening frames,26 boards,8 native details and seven object states4.5 provisional/rooted4.6; rejected mount4.3, interrupted suite1 and failed suite2 passive127 preserved separately. Unbound same-source closed142px/open50px reuse4.5 provisional and larger open sizes4.6, all ten isolated presentations directly reviewed; new grotto1254-square fails required2048-square native coverage and stays reference-only. Shared training has three source and eleven component opinions with literal caller trace. Actual Library/elevator route: all58 native stills,316 continuous frames,27 boards,4 native details,86 individual mounted object/relationship opinions; actual stage vector emblem2.9/celebration3.2 and earned Library return are separately shown. V30 register1722 known entries has676 inclusive source priorities and385 unassigned; source union is not exhaustive live-use acceptance. Fresh officialGodot4.7.2 unmodified full suite3 82/82 with368 unchanged literal sources and raw diagnostics retained applies only to that frozen production. Extra route fixture has independent parser/analyzer/capture receipts. Earlier closed maps immutable; no all-job/device/child/owner/lifecycle/integration/release acceptance.'}
write(b/mp,m);git('add','-f','--',mp);raw=git('show',':'+mp)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(files)|{mp}
seal={'status':'EXACT_CANONICAL_CURRENT_SCOPED_BLOBS_SEALED','base_revision':baseline,'map_path':mp,'map_sha256':hashlib.sha256(raw).hexdigest(),'payload_sha256':m['payload_sha256'],'payload_files':len(files),'payload_bytes':m['required_payload_bytes'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Exact staged topic-only checkpoint; publisher repeats blob, full-suite and368-source checks before commit/push and anonymously verifies remote bytes.'}
write(b/'tmp/geology_checkpoint_k_sealed.json',seal);write(out/'RECEIPT.json',seal)
print(json.dumps(seal),flush=True)
