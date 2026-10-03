from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';C=B/'assets_src/imagegen/candy_wrap_scene_context_v1_20261003';L=B/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):n=p.with_name(p.name+'.v583_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');n.replace(p)
builder=P/'review_tools/build_candy_local_review_v582.py';failed=builder.with_name('build_candy_local_review_v582.failed_original.py');assert not failed.exists();shutil.copyfile(builder,failed)
write(C/'BUILD_HELPER_SELF_COPY_FAILURE_V582.json',dict(status='ACTUAL_HELPER_SELF_COPY_FAILURE_PRESERVED',observed_utc=now(),command=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(builder)],actual_exit_code=1,preserved_failed_helper=failed.relative_to(B).as_posix(),preserved_failed_helper_sha256=sha(failed),observed_error='shutil.SameFileError: helper path and its archive destination are the same file.',qualification='The illustrated205-frame page and asset license additions were written before this helper-only failure. No renderer rerun or game/artwork change. Original wrapper task remains failed.'))
s=builder.read_text(encoding='utf-8');needle="shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)";assert s.count(needle)==1
builder.write_text(s.replace(needle,"if Path(__file__).resolve() != (P/'review_tools'/Path(__file__).name).resolve():shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)"),encoding='utf-8',newline='\n')
receipts=[]
for label,target in [('gallery',builder),('boundary',L/'review_tools/refresh_current_job_review_v49.py')]:
    cmd=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(target)];start=now();r=subprocess.run(cmd,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    (C/(label+'_recovery_v583.stdout.log')).write_bytes(r.stdout);(C/(label+'_recovery_v583.stderr.log')).write_bytes(r.stderr)
    receipts.append(dict(label=label,command=cmd,exit_code=r.returncode,started_utc=start,finished_utc=now(),status='PASS' if r.returncode==0 else 'FAIL',stdout_sha256=sha(C/(label+'_recovery_v583.stdout.log')),stderr_sha256=sha(C/(label+'_recovery_v583.stderr.log'))))
    print(r.stdout.decode('utf-8',errors='replace').strip());assert r.returncode==0,r.stderr.decode()
assert read(L/'ALL_ITEMS.json')['display_revision']=='V49' and read(L/'CURRENT_BOUNDARY_REFRESH.json')['registered_source_matches']==2049
write(C/'BUILD_RECOVERY_V583.json',dict(status='HELPER_SELF_COPY_FIXED_REPORT_AND_BOUNDARY_REBUILT',checked_utc=now(),actual_processes=receipts,qualification='Recovery of review publication helper only. Both complete originals and existing native motion frames unchanged; no new action/game/owner acceptance.'))
licenses=B/'ASSET_LICENSES.md';raw=licenses.read_bytes();path=(C/'BROWSER_SOURCE_REPORT_V578.jpg').relative_to(B).as_posix()
if ('| `'+path+'` |').encode() not in raw:
    raw+=('\n| `'+path+'` | Actual local browser screenshot of the clean Candy source review | Original project review layout and inherited displayed artwork provenance | BROWSER_VERIFY_V578.json binds exact screenshot and observed loaded sources/opinions | QA proof only, not production/cinematic pixels or owner acceptance. |\n').encode();n=licenses.with_name(licenses.name+'.v583_next');n.write_bytes(raw);n.replace(licenses)
shutil.copyfile(__file__,C/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in(C,P) for p in base.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md','audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json'})
d['validation'].append(dict(command='Preserved self-copy failure and actual gallery/current-boundary recovery',result='PASS',evidence=(C/'BUILD_HELPER_SELF_COPY_FAILURE_V582.json').relative_to(B).as_posix()+'; BUILD_RECOVERY_V583.json and actual raw recovery streams. Registered2049 hashes match; no source/art/motion changes.'))
write(ip,d)
allow=B/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(B).as_posix() for base in(C,P) for p in base.rglob('*') if p.is_file()}|{p.relative_to(B).as_posix() for p in L.iterdir() if p.is_file()}))
print(json.dumps(dict(status='V49_RECOVERED_2049_HASHES_MATCH',registered_items=2049,register_bytes=(L/'ALL_ITEMS.json').stat().st_size,all783_production_literals_unchanged=read(L/'CURRENT_BOUNDARY_REFRESH.json')['candy_capture_boundary_match'])))
