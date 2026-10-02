from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip();assert revision=='56d66f63e375b61cf02936b426a05a2b92c14d3b'
out=r/'audit/job_review_v2_20261001/final_native_supplement_gates_v3';assert not out.exists();out.mkdir();(out/'.gdignore').write_text('');shutil.copyfile(Path(__file__),out/'executed_prepare_and_check_native_supplement_v80.py')
proof=r/'assets_src/vector/job_geology_teacher_refinement_v1_20261001/browser_preview_v1';proof.mkdir()
for filename in ['vector_source_library_browser_v79.png','current_register_1532_browser_v79.png']:shutil.copyfile(staging/filename,proof/filename)
write(proof/'QUALIFICATION.json',dict(status='PASS_SCOPED_DESKTOP_REGISTER_AND_VECTOR_GALLERY',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),vector_cards=8,vector_images_loaded=8,register_items=1532,register_source_priorities=571,register_unassigned_source=388,desktop_width=1280,page_width=1265,qualification='Both saved desktop screenshots directly viewed. Every8 vector native previews and5 exact cushion extractions separately directly reviewed. Browser preview/source floors do not establish actual game mount/action/device/child/owner acceptance.'))
license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8')
for p in proof.glob('*.png'):
 if f'`{rel(p)}`' not in s:s+=f'\n| `{rel(p)}` | Codex browser screenshot of the exact current local vector/register gallery, SHA-256 `{sha(p)}`; underlying source and candidate provenance remains in the individual reports. | Project audit evidence; original artwork licenses retained. | Internal browser capture, 2026-10-01. | Unmodified desktop preview, no new authored art or runtime/device/owner acceptance. |\n'
license.write_text(s,encoding='utf-8',newline='\n')
reviewfile=r/'audit/job_source_review_nursery_teacher_geology_v1_20261001/REVIEW.json';d=read(reviewfile)
for x in d['source_object_regions']:x['direct_isolated_native_preview_review']=True
write(reviewfile,d)
impactfile=r/'design/audit_impacts/job-nursery-teacher-geology-native-review-20261001.json';d=read(impactfile);d['files']=sorted(set(d['files'])|{rel(p) for p in proof.rglob('*') if p.is_file()});d['validation'].append(dict(command='Every5 exact native cushion extraction and desktop8-card vector gallery/register preview',result='PASS',evidence=rel(proof/'QUALIFICATION.json')));write(impactfile,d)
ledger=r/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8')
s=s.replace('including the complete shared-source native review. Exact current checkout hashes','including the complete shared-source native review and five exact nursery cushion source-object regions. Exact current checkout hashes')
s=s.replace('328 source pose cells, 6 current pool regions and 32 individually inspected craft prop regions, including the complete shared-source native review.','328 source pose cells, 6 current pool regions, 32 individually inspected craft prop regions and 5 separately illustrated nursery source-object regions, including the complete shared-source native review.')
ledger.write_text(s,encoding='utf-8',newline='\n')
template=read(r/'design/audit_impacts/job-native-supplement-gates-20261001.json')
record=dict(id='job-native-final-supplement-gates-20261001',scope='Final scoped static/native/import, exact literal-source and staged change-coverage verification for the new shared source/94regions, outward/clean doctor originals and41failed local motion frames,94static contact views,7nursery/teacher/geology original opinions,5individual cushion regions and5selected unbound vector source floors. Preserve all prior failures, existing byte maps and current exactC hosted success. No production changes or all-game acceptance.',baseline=revision,rules=template['rules'],findings=template['findings'],files=sorted([rel(p) for p in out.rglob('*') if p.is_file()]+['design/05_DOC_LEDGER.md']),validation=[dict(command='Final scoped verification',result='PENDING',evidence=rel(out))],acceptance_gaps='Five vector source floors and clean source4.5 unbound; washing motion4.0/staticwater3.7 and other full actions remain open. No overall4.5, actual-use completeness, device/child/owner, strict2D, integration or release acceptance. New exact-head hosted check pending after publication.')
recordfile=r/'design/audit_impacts/job-native-final-supplement-gates-20261001.json';write(recordfile,record)
snapshot=read(r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json');assert len(snapshot['source_files'])==325
before={x['path']:sha(r/x['path']) for x in snapshot['source_files']};assert all(before[x['path']]==x['sha256'] for x in snapshot['source_files'])
fetch=subprocess.run(['git','fetch','origin'],cwd=r,capture_output=True);(out/'fetch.stdout.log').write_bytes(fetch.stdout);(out/'fetch.stderr.log').write_bytes(fetch.stderr);assert fetch.returncode==0
write(out/'SOURCE_AND_BRANCH_BOUNDARY.json',dict(status='PREPARED_UNCHANGED325_SOURCE_BOUNDARY',baseline=revision,branch=subprocess.check_output(['git','branch','--show-current'],cwd=r,text=True).strip(),origin_dev=subprocess.check_output(['git','rev-parse','origin/dev'],cwd=r,text=True).strip(),source_snapshot_path='audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json',source_snapshot_sha256=sha(r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json'),literal_source_count=325,all_literal_sources_match_passing_full_suite=True,qualification='Fresh fetch only; no dev integration/release. Earlier local82/82 and publishedC hosted81 trusted headings remain exact boundaries with preserved diagnostics. New ignored source/review additions need their own scoped gates.'))
folders=['audit/job_shared_source_native_review_v1_20261001','audit/day_two_wash_contact_study_v1_20261001/attempt_04','audit/day_two_wash_contact_study_v1_20261001/attempt_05','assets_src/imagegen/day2_doctor_wash_reach_v1_20261001','assets_src/imagegen/day2_doctor_wash_reach_clean_v1_20261001','assets_src/local_motion/day2_doctor_wash_reach_rub_study_v1_20261001','assets_src/vector/job_geology_teacher_refinement_v1_20261001','audit/job_source_review_nursery_teacher_geology_v1_20261001','audit/job_review_v2_20261001/current_supplement_remote_v1','audit/job_review_v2_20261001/hosted_corrected_supplement_v1','audit/job_review_v2_20261001/current_native_supplement_gates_v2',rel(out)]
scope={rel(p) for folder in folders for p in (r/folder).rglob('*') if p.is_file()}
scope.update(['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','audit/job_review_v2_20261001/index.html','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/STATUS.json','design/audit_impacts/job-review-separate-v2-20261001.json'])
for version in [10,11,12]:
 for parent in ['audit/job_review_v2_20261001/review_tools','audit/job_artwork_refinement_live/review_tools']:scope.add(parent+f'/build_current_job_item_register_v{version}.py')
ids=['job-shared-native-source-review-20261001','job-doctor-reach-clean-source-20261001','job-doctor-reach-local-rub-study-20261001','job-doctor-reach-water-contact-study-20261001','job-native-supplement-gates-20261001','job-nursery-teacher-geology-native-review-20261001','job-corrected-supplement-hosted-pass-20261001','job-native-final-supplement-gates-20261001']
for ident in ids:scope.add('design/audit_impacts/'+ident+'.json')
changed={p.decode() for p in subprocess.check_output(['git','diff','--name-only','-z'],cwd=r,stderr=subprocess.DEVNULL).split(b'\0') if p};assert changed<=scope,sorted(changed-scope)
assert all((r/p).is_file() for p in scope),[p for p in scope if not (r/p).is_file()]
write(r/'tmp/native_supplement_scope_v80.json',dict(baseline=revision,folders=folders,scope=sorted(scope)))
scripts=sorted(p for p in scope if p.endswith('.gd'))
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*scripts]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*scripts]),('import',[godot,'--headless','--path',str(r),'--import']),('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('game2d',[sys.executable,'-X','utf8','-B','tools/audit_game_2d.py'])]
rows=[]
for name,command in commands:
 record['files']=sorted(rel(p) for p in out.rglob('*') if p.is_file())+['design/05_DOC_LEDGER.md'];write(recordfile,record)
 start=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as stdout,(out/(name+'.stderr.log')).open('wb') as stderr:
  try:proc=subprocess.run(command,cwd=r,stdout=stdout,stderr=stderr,timeout=240 if name=='import' else 900);exit_code=proc.returncode;timed_out=False
  except subprocess.TimeoutExpired:exit_code=None;timed_out=True
 rows.append(dict(name=name,command=command,process_exit=exit_code,timed_out=timed_out,seconds=time.monotonic()-start,stdout=rel(out/(name+'.stdout.log')),stderr=rel(out/(name+'.stderr.log'))));print(name,exit_code,flush=True)
 if exit_code!=0:print((out/(name+'.stdout.log')).read_text(encoding='utf-8',errors='replace')[-3000:],(out/(name+'.stderr.log')).read_text(encoding='utf-8',errors='replace')[-3000:],flush=True);break
after={p:sha(r/p) for p in before};unchanged=before==after;passed=len(rows)==len(commands) and all(x['process_exit']==0 for x in rows) and unchanged
write(out/'RECEIPT.json',dict(status='PASS_FINAL_SCOPED_NATIVE_SUPPLEMENT_GATES' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,review_gd_files=scripts,literal_sources_unchanged=unchanged,literal_source_count=325,source_mismatches=[p for p in before if before[p]!=after[p]],qualification=record['acceptance_gaps']))
record['files']=sorted(rel(p) for p in out.rglob('*') if p.is_file())+['design/05_DOC_LEDGER.md'];record['validation']=[dict(command='Parser/inference/import/authority/development auto-base/game2d with unchanged325 literal source guard',result='PASS' if passed else 'FAIL',evidence=rel(out/'RECEIPT.json'))];write(recordfile,record)
print(json.dumps(dict(static_gates_pass=passed,review_scripts=len(scripts),literal_source_count=325,literal_sources_unchanged=unchanged,scoped_files=len(scope))))
raise SystemExit(0 if passed else 1)
