from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
out=r/'tmp/checkpoint_l_ledger_sync_v320';out.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):return subprocess.run(['git',*args],cwd=r,input=input,capture_output=True,check=True).stdout
seal=read(r/'tmp/geology_checkpoint_l_sealed.json');mp=seal['map_path'];raw=git('show',':'+mp);assert hashlib.sha256(raw).hexdigest()==seal['map_sha256']
m=json.loads(raw);assert git('rev-parse','HEAD').decode().strip()==seal['base_revision']
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(m['files'])|{mp}
(out/'UNPUBLISHED_MAP_BEFORE_LEDGER_SYNC.original.json').write_bytes(raw);write(out/'SEAL_BEFORE_LEDGER_SYNC.json',seal)
ci=read(f/'full_ci_v2/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['probe_results'])==82
assert ci['raw_diagnostic_count']==51
# New review evidence contains literal engine CRLF streams. Preserve those
# bytes without broad renormalization of previously published closed maps.
attrs=r/'.gitattributes';attribute_text=attrs.read_text();patterns=[
 'audit/job_geode_route_emblem_runtime_v1_20261002/** -text whitespace=-blank-at-eol,cr-at-eol',
 'audit/job_wash_root_doctor_sequence_v1_20261002/** -text whitespace=-blank-at-eol,cr-at-eol',
 'audit/job_wash_root_remaining_sequences_v1_20261002/** -text whitespace=-blank-at-eol,cr-at-eol',
 'audit/job_review_v2_20261001/INDEX_BEFORE_CURRENT_LANDING_V312.original.html -text whitespace=-blank-at-eol,cr-at-eol'
]
assert all(pattern not in attribute_text for pattern in patterns)
attrs.write_text(attribute_text+'\n# Literal bytes for geode route and complete preserved washing evidence.\n'+'\n'.join(patterns)+'\n',encoding='utf-8',newline='\n')
p=r/'design/05_DOC_LEDGER.md';s=p.read_text();old='second 373-source suite pending.';assert s.count(old)==1;s=s.replace(old,'second unmodified suite passes 82/82 on all 373 unchanged literal sources; 51 raw diagnostics retained.',1);p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
record=f/'LEDGER_MACHINE_SYNC_V320.json';write(record,dict(status='CURRENT_LEDGER_AND_LITERAL_BYTE_PROVENANCE_SYNCHRONIZED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),receipt='full_ci_v2/RECEIPT.json',probes=82,literal_source_count=373,raw_diagnostics=51,literal_byte_attribute_patterns=patterns,qualification='Synchronizes the ledger row to the completed current receipt and prevents Git newline conversion of new raw evidence. No runtime source, image, visual opinion, acceptance or lifecycle change. Earlier unpublished seal remains in ignored staging; only the final regenerated manifest is a delivery map. Closed prior maps are outside these new patterns.'))
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{'.gitattributes'});write(ip,d)
for gate in ['authorityv5','developmentv5']:
 q=subprocess.run([sys.executable,'-X','utf8','-B',str(f/'review_tools/run_geode_route_gates_v276.py'),gate],cwd=r,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(gate+'.stdout.log')).write_bytes(q.stdout);(out/(gate+'.stderr.log')).write_bytes(q.stderr);print(q.stdout.decode().strip(),flush=True);assert q.returncode==0
scope=set(read(ip)['files'])|set(m['files'])|{ip.relative_to(r).as_posix(),mp}
assert all((r/p).is_file() for p in scope)
git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=''.join(p+'\0' for p in sorted(scope)).encode())
paths={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p};assert paths<=scope and mp in paths
payload=sorted(paths-{mp});data=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in payload).encode());offset=0;files={}
for path in payload:
 end=data.index(b'\n',offset);header=data[offset:end].split();assert header[1]==b'blob';size=int(header[2]);offset=end+1;blob=data[offset:offset+size];offset+=size+1;files[path]=[len(blob),hashlib.sha256(blob).hexdigest()]
assert offset==len(data);assert not set(m['unchanged_required_files'])&set(files)
assert len(m['unchanged_required_files'])==2077
for family in [f,r/'audit/job_wash_root_doctor_sequence_v1_20261002',r/'audit/job_wash_root_remaining_sequences_v1_20261002']:
 for p in family.rglob('*'):
  if p.is_file() and p.relative_to(r).as_posix() in files:
   blob=p.read_bytes();assert files[p.relative_to(r).as_posix()]==[len(blob),hashlib.sha256(blob).hexdigest()],p
assert files['audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/stdout.log'][1]==ci['stdout_sha256']
assert files['audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/stderr.log'][1]==ci['stderr_sha256']
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
prior_map=m['prior_closed_map'];assert hashlib.sha256(git('show','HEAD:'+prior_map)).hexdigest()==m['prior_closed_map_sha256']
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m.update(files=files,required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=hashlib.sha256(formula).hexdigest())
write(r/mp,m);git('add','-f','--',mp);raw=git('show',':'+mp)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(files)|{mp}
seal.update(status='EXACT_CURRENT_SCOPED_BLOBS_SEALED_LEDGER_SYNCHRONIZED',map_sha256=hashlib.sha256(raw).hexdigest(),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),current_document_gates=['authorityv5','developmentv5'])
write(r/'tmp/geology_checkpoint_l_sealed.json',seal);write(out/'RECEIPT.json',seal)
print(json.dumps(seal),flush=True)
