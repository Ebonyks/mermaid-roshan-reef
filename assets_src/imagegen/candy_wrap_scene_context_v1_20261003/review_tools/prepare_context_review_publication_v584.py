from pathlib import Path
import datetime,hashlib,json,shutil,subprocess

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';C=B/'assets_src/imagegen/candy_wrap_scene_context_v1_20261003';L=B/'audit/job_artwork_refinement_live'
BASE='2b109a233c14050567aaa84dc975119b2e18a77e';MAP='audit/job_review_v2_20261001/CANDY_CONTEXT_CONTINUITY_FILES_V22.json';SHARDS='audit/job_review_v2_20261001/v22_unchanged_dependency_shards'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);n=p.with_name(p.name+'.v584_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');n.replace(p)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip()==BASE
remote=P/'previous_x_remote_verified';assert not remote.exists();remote.mkdir()
src=B/'tmp/candy_shared_remote_v573';result=read(src/'RESULT.json');assert result['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and result['revision']==BASE and result['files_including_manifest']==23846
shutil.copyfile(src/'RESULT.json',remote/'RESULT.json');shutil.copyfile(B/'tmp/candy_shared_publish_v573/RECEIPT.json',remote/'PUBLICATION_RECEIPT.json')
raw=(src/'VERIFICATION_JOURNAL.jsonl').read_bytes();lines=raw.splitlines(keepends=True);assert len(lines)==23846 and all(json.loads(x)['matches'] for x in lines)
parts=[];group=[];size=0
def emit(group):
    payload=b''.join(group);p=remote/f'JOURNAL_{len(parts)+1:03d}.jsonl';p.write_bytes(payload);assert len(payload)<=900000
    parts.append(dict(path=p.relative_to(B).as_posix(),bytes=len(payload),sha256=sha(payload),rows=len(group)))
for line in lines:
    if group and size+len(line)>899000:emit(group);group=[];size=0
    group.append(line);size+=len(line)
if group:emit(group)
assert b''.join((B/x['path']).read_bytes() for x in parts)==raw
write(remote/'JOURNAL_SHARDS.json',dict(status='ALL23846_EXACT_X_ANONYMOUS_GET_ROWS_LOSSLESSLY_PRESERVED',revision=BASE,original_bytes=len(raw),original_sha256=sha(raw),original_rows=len(lines),parts=parts,shard_max_bytes=900000,qualification='Literal ordered journal reconstruction, no truncation or sampled remote verification. Prior X result does not accept this new review revision.'))
host=P/'previous_x_hosted_snapshot_v584';host.mkdir()
for endpoint,name in [('actions/runs/37111673023','RUN.json'),('actions/runs/37111673023/jobs?per_page=100','JOBS.json')]:
    cmd=['C:/Program Files/GitHub CLI/gh.exe','api','repos/Ebonyks/mermaid-roshan-reef/'+endpoint];start=now();r=subprocess.run(cmd,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    (host/name).write_bytes(r.stdout);(host/(name+'.stderr.log')).write_bytes(r.stderr);assert r.returncode==0
h=read(host/'RUN.json');jobs=read(host/'JOBS.json')['jobs'];assert h['head_sha']==BASE
complete=h['status']=='completed' and h['conclusion']=='success' and bool(jobs) and all(j['status']=='completed' and j['conclusion']=='success' for j in jobs)
write(host/'VERIFICATION.json',dict(status='EXACT_X_HOSTED_JOBS_COMPLETED_SUCCESS' if complete else 'EXACT_X_HOSTED_OBSERVATION_PENDING_OR_FAILED',checked_utc=now(),revision=BASE,run_id=h['id'],url=h['html_url'],run_status=h['status'],run_conclusion=h['conclusion'],jobs=[dict(name=j['name'],status=j['status'],conclusion=j['conclusion']) for j in jobs],steps_with_failed_conclusion=[dict(job=j['name'],step=s['name'],conclusion=s['conclusion']) for j in jobs for s in j.get('steps',[]) if s.get('conclusion')=='failure'],qualification='Actual status snapshot only. Pending or failed does not grant a pass; prior/source machine success cannot accept a new review revision, graphics/action/device/child/owner/all-job or integration/release.'))
attrs=B/'.gitattributes';raw=attrs.read_bytes()
for path in [C.relative_to(B).as_posix()+'/**',MAP,SHARDS+'/**']+['audit/job_artwork_refinement_live/'+n for n in ['ALL_ITEMS_V48.original.json','all_items_V48.original.html','BOUNDARY_V48.original.json']]:
    line=(path+' -text').encode()
    if line not in raw:raw+=b'\n'+line+b'\n'
n=attrs.with_name(attrs.name+'.v584_next');n.write_bytes(raw);n.replace(attrs)
write(B/MAP,dict(status='PENDING_EXACT_SHARDED_CONTEXT_REVIEW_SEAL',base_revision=BASE,qualification='Placeholder only; no predicted revision bytes or new acceptance. Existing scanner ceiling unchanged.'))
write(P/'PUBLICATION_BOUNDARY_V584.json',dict(status='PENDING_EXACT_STAGED_CONTEXT_REVIEW_BYTE_SEAL'))
g=P/'gates_v3';g.mkdir()
shutil.copyfile(__file__,C/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in(C,P) for p in base.rglob('*') if p.is_file()}|{MAP,'.gitattributes'})
d['validation'].append(dict(command='Exact X all23846 anonymous remote journal archival and actual hosted status snapshot',result='PASS',evidence=remote.relative_to(B).as_posix()+'/JOURNAL_SHARDS.json and RESULT.json; '+host.relative_to(B).as_posix()+'/VERIFICATION.json. Complete prior remote proof; hosted run remains qualified by its actual saved state.'))
d['validation'].append(dict(command='Fresh authority/development/document tests/2D regression and exact closed review publication',result='PENDING',evidence='gates_v3 and V22 root/shards to be sealed after A6 native review; no predicted pass or publication.'))
write(ip,d)
print(json.dumps(dict(status='X_REMOTE_PROOF_ARCHIVED_AND_CONTEXT_PUBLICATION_PREPARED',prior_exact_remote_rows=23846,journal_shards=len(parts),actual_prior_hosted_status=h['status'],actual_prior_hosted_conclusion=h['conclusion'],new_map_path=MAP)))
