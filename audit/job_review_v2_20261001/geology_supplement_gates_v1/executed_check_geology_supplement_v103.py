from pathlib import Path
import json, hashlib, shutil, subprocess, sys, time, datetime, urllib.request
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/geology_supplement_gates_v1';assert not out.exists();out.mkdir()
def rel(p):return p.relative_to(r).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json'
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
shutil.copyfile(__file__,out/'executed_check_geology_supplement_v103.py');cover()
snapshot=json.loads((r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];assert len(snapshot)==325
before={x['path']:sha(r/x['path']) for x in snapshot};assert all(before[x['path']]==x['sha256'] for x in snapshot)
write(out/'SOURCE_GUARD.json',dict(status='325_LITERAL_SOURCES_MATCH_PASSING_FULL_CI_AND_PUBLISHED_D',source_files=snapshot,baseline='6edb4ca8c57bfbfe3123636863a29c95165ac23f',full_ci_receipt='audit/job_review_v2_20261001/full_ci_candidate_retry_v2/RECEIPT.json',hosted_receipt='audit/job_review_v2_20261001/hosted_native_supplement_v2/RECEIPT.json',qualification='Carry-forward unchanged runtime verification; new source material is ignored review-only, not a new production art/import integration.'))
# Existing local review server stays scoped to explicit authorized file paths.
allowed_file=r/'tmp/v2_preview_allowed.json';allowed=json.loads(allowed_file.read_text());paths=set(allowed)
prefixes=['assets_src/imagegen/geologist_painted_rebuild_v1_20261001','audit/job_geode_embedded_mount_v2_20261001','audit/job_geology_painted_mount_v1_20261001','audit/job_vector_mount_review_v1_20261001','audit/job_review_v2_20261001/hosted_native_supplement_v2']
paths.update(rel(p) for prefix in prefixes for p in (r/prefix).rglob('*') if p.is_file());paths.update(['audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/ALL_ITEMS.html','audit/job_review_v2_20261001/index.html']);write(allowed_file,sorted(paths))
results=[]
for path in ['audit/job_geode_embedded_mount_v2_20261001/index.html','audit/job_geode_embedded_mount_v2_20261001/attempt_02/index.html','audit/job_geode_embedded_mount_v2_20261001/attempt_02/native_views/geologist_1280_geode_fully_open_embedded_interior_painted_staging.webp','assets_src/imagegen/geologist_painted_rebuild_v1_20261001/open_geode/attempt_02/native.png','audit/job_artwork_refinement_live/ALL_ITEMS.json']:
 with urllib.request.urlopen('http://127.0.0.1:8880/'+path,timeout=20) as response:raw=response.read();code=response.status
 expected=(r/path).read_bytes();assert raw==expected and code==200;results.append(dict(path=path,status=code,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
write(out/'LOCAL_PREVIEW_HTTP.json',dict(status='PASS_EXACT_ALLOWLIST_LOCAL_GET',checks=results));cover()
gds=sorted(rel(p) for prefix in ['audit/job_geode_embedded_mount_v2_20261001','audit/job_geology_painted_mount_v1_20261001','audit/job_vector_mount_review_v1_20261001'] for p in (r/prefix).rglob('*.gd'))
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*gds]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*gds]),('import',[godot,'--headless','--path',str(r),'--import']),('contract_tests',[sys.executable,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']),('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('game2d',[sys.executable,'-X','utf8','-B','tools/audit_game_2d.py'])]
rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as b:
  try:p=subprocess.run(cmd,cwd=r,stdout=a,stderr=b,timeout=240 if name=='import' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed_out=False
  except subprocess.TimeoutExpired:code=None;timed_out=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed_out,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:
  print(so.read_text(encoding='utf-8',errors='replace')[-2300:],se.read_text(encoding='utf-8',errors='replace')[-700:],flush=True);break
after={p:sha(r/p) for p in before};passed=len(rows)==len(cmds) and all(x['process_exit']==0 for x in rows) and after==before
write(out/'RECEIPT.json',dict(status='PASS_SCOPED_GEOLOGY_SOURCE_AND_NATIVE_REVIEW_GATES' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,review_gd_files=gds,literal_sources_unchanged=before==after,literal_source_count=len(before),qualification='Prior unchanged325-file runtime full suite and publishedD hosted CI remain exact evidence; current review fixtures separately pass real analyzer/native. No production geology binding, exhaustive all-job/action, device/child/owner, strict2D, dev integration or release acceptance.'))
cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='Scoped geology supplement parser/inference/official4.7.2 import/contract/authority/development/game2d and325-source hash guard',result='PASS' if passed else 'FAIL',evidence=rel(out/'RECEIPT.json')));write(impact,d)
raise SystemExit(0 if passed else 1)
