from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
work=b/'audit/job_geode_route_emblem_runtime_v1_20261002';out=b/'tmp/geology_checkpoint_l_seal_v296';out.mkdir(exist_ok=False)
baseline='c8f88df058434f1fd1b6d7fade712677003c641a';mp='audit/job_review_v2_20261001/GEOLOGY_GEODE_ROUTE_EMBLEM_SUPPLEMENT_FILES_V10.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):
 q=subprocess.run(['git',*args],cwd=b,input=input,capture_output=True,check=True)
 if q.stderr:(out/'git.stderr.log').open('ab').write(q.stderr)
 return q.stdout
assert git('rev-parse','HEAD').decode().strip()==baseline
assert git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
assert not git('diff','--cached','--name-only').strip(),'Never absorb unrelated staged work.'
ci=read(work/'full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['source_checks'])==372 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
for gate in ['parserv3','inferencev3','importartv1','contractv2','capture1280v1','capture1600v1','authorityv3','developmentv3','audit2dv1']:
 assert read(work/('runtime_gate/'+gate+'.receipt.json'))['status']=='PASS',gate
# Durable helper and explicit audit-impact file coverage precede staging.
target=work/'review_tools'/Path(__file__).name;shutil.copyfile(__file__,target)
ipaths=[b/'design/audit_impacts'/n for n in ['job-geode-route-emblem-runtime-20261002.json','job-wash-root-doctor-sequence-review-20261002.json']]
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
prior='audit/job_review_v2_20261001/GEOLOGY_COHERENT_GEODE_ROUTE_REVIEW_SUPPLEMENT_FILES_V9.json';priorbytes=git('show','HEAD:'+prior)
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m={'schema':'reef.immutable-review-supplement.v1','base_revision':baseline,'prior_closed_map':prior,'prior_closed_map_sha256':hashlib.sha256(priorbytes).hexdigest(),'required_files':len(files),'required_payload_bytes':sum(v[0] for v in files.values()),'payload_sha256':hashlib.sha256(formula).hexdigest(),'payload_hash_formula':'SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF','files':files,'qualification':'Additive reversible current painted-geode Library50px/invitation142px4.5 provisional, shared developer80px4.6 and normal celebration artwork4.6 but placement4.2/composition3.3. Same source atlas pixels; three production bindings and one AtlasTexture resource, function bodies/mechanics/save/reward preserved. All58 current stills/316 current consecutive frames/27 motion boards/10 still boards/eight native details/23 current object-state-context opinions reviewed. Room2.8/contact2.7/fossil clearing3.9/pan3.8/caption4.0 and native-background coverage remain open. Fresh unmodified officialGodot4.7.2 full suite1 82/82 on372 frozen literal files, raw diagnostics retained; no inherited or visual pass. V31 known register1726 entries/1245 sources/49 runtime regions retains676 source priorities/385 unassigned; four old technical labels now distinct, aliases/oldV30 bytes preserved. Separately all256 preservedOctober1 Doctor1280 training WASH frames/22 boards/eight native details/12 opinions reviewed; workflow2.7/contact2.3/subject2.2/basin2.9 remain weak. Other1818 case frames/current rerender/story/device/child/owner/all-job acceptance remain open. Verify required unchanged native references at this exact remote revision as well as every new payload. Earlier closed maps immutable; no finding lifecycle change, dev/master integration or release.'}
refs=json.loads((b/'audit/job_wash_root_doctor_sequence_v1_20261002/REQUIRED_UNCHANGED_REFERENCES.json').read_text())['files']
for ref in ['assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png','assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_bridge.png','assets/opera/worlds/geology/painted_work_v1_20261001/work_slab.png']:
 raw_ref=git('show','HEAD:'+ref);refs[ref]=[len(raw_ref),hashlib.sha256(raw_ref).hexdigest()]
for ref,v in refs.items():
 raw_ref=git('show','HEAD:'+ref);assert [len(raw_ref),hashlib.sha256(raw_ref).hexdigest()]==v,ref
assert not set(refs)&set(files)
m['required_unchanged_files']=len(refs);m['unchanged_required_files']=dict(sorted(refs.items()))
write(b/mp,m);git('add','-f','--',mp);raw=git('show',':'+mp)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(files)|{mp}
seal={'status':'EXACT_CANONICAL_CURRENT_SCOPED_BLOBS_SEALED','base_revision':baseline,'map_path':mp,'map_sha256':hashlib.sha256(raw).hexdigest(),'payload_sha256':m['payload_sha256'],'payload_files':len(files),'payload_bytes':m['required_payload_bytes'],'unchanged_required_files':len(refs),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Exact staged topic-only checkpoint; publisher repeats blob, full-suite and372-source checks before commit/push and anonymously verifies remote bytes.'}
write(b/'tmp/geology_checkpoint_l_sealed.json',seal);write(out/'RECEIPT.json',seal)
print(json.dumps(seal),flush=True)
