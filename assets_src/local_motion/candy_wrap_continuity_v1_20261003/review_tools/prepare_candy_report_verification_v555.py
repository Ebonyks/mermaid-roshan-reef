from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';M=B/'assets_src/imagegen/candy_wrap_contact_v1_20261003';IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
 n=p.with_name(p.name+'.v555_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');n.replace(p)
write(P/'PREVIEW_SOURCE_WHITELIST_FAILURE.json',dict(observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),observation='Updated browser report listed all82 frames, but A12/A13 source images had naturalWidth/naturalHeight0. Exact new source paths were absent from strict static preview whitelist.',qualification='Preview-only delivery error. Native sources exist and hashes match. No source changes or broad server permission changes; admit only the already-authorized listed new files.'))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ci=P/'previous_v_hosted_complete';assert not ci.exists();ci.mkdir();gh='C:/Program Files/GitHub CLI/gh.exe'
for label,endpoint in [('RUN','repos/Ebonyks/mermaid-roshan-reef/actions/runs/37104237716'),('JOBS','repos/Ebonyks/mermaid-roshan-reef/actions/runs/37104237716/jobs')]:
 r=subprocess.run([gh,'api',endpoint],cwd=B,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);(ci/(label+'.json')).write_bytes(r.stdout);(ci/(label+'.stderr.log')).write_bytes(r.stderr)
run=read(ci/'RUN.json');jobs=read(ci/'JOBS.json');assert run['head_sha']=='79f20126e01454132fe245fb3b8a03e700b9ca31' and run['status']=='completed' and run['conclusion']=='success';assert len(jobs['jobs'])==2 and all(x['conclusion']=='success' for x in jobs['jobs'])
write(ci/'VERIFICATION.json',dict(status='PREVIOUS_V_EXACT_HOSTED_JOBS_COMPLETED_SUCCESS',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision=run['head_sha'],run_id=run['id'],run_url=run['html_url'],jobs=[dict(id=x['id'],name=x['name'],conclusion=x['conclusion'],completed_at=x['completed_at']) for x in jobs['jobs']],raw_run_sha256=sha(ci/'RUN.json'),raw_jobs_sha256=sha(ci/'JOBS.json'),qualification='Exact previous immutable V hosted result, not a new review revision CI pass, visual/owner acceptance or integration/release authority. Original pending snapshots preserved unchanged.'))
for name in ['BROWSER_A2_REFERENCE_V555.png','BROWSER_SOURCE_GALLERY_V555.png','BROWSER_VERIFY_V555.json']:
 assert not (P/name).exists()
d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()}|{(P/x).relative_to(B).as_posix() for x in ['BROWSER_A2_REFERENCE_V555.png','BROWSER_SOURCE_GALLERY_V555.png','BROWSER_VERIFY_V555.json']});write(IP,d)
ap=B/'tmp/v2_preview_allowed.json';write(ap,sorted(set(read(ap))|set(d['files'])))
shutil.copyfile(P/'review_tools/run_candy_local_review_gates_v549.py',B/'tmp/run_candy_local_review_gates_v549.py')
print('Previous exact V hosted CI success preserved; exact new sources admitted to strict preview; browser evidence routes scoped.')
