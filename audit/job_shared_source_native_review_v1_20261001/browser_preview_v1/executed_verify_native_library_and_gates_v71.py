from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,urllib.parse,urllib.request
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
staging=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
shared=r/'audit/job_shared_source_native_review_v1_20261001'
proof=shared/'browser_preview_v1';proof.mkdir(exist_ok=True)
for name in ['shared_native_library_browser_v64.png','shared_native_art_browser_v64.png','current_register_browser_v70.png','shared_native_browser_resource_refs_v70.json']:
 shutil.copyfile(staging/name,proof/name)
references=read(proof/'shared_native_browser_resource_refs_v70.json');assert len(references)==104
def fetch(x):
 u=urllib.parse.urlparse(x['url']);assert u.scheme=='http' and u.hostname=='127.0.0.1' and u.port==8880
 path=urllib.parse.unquote(u.path).lstrip('/');p=(r/path).resolve();assert p.is_relative_to(r.resolve()) and p.is_file()
 with urllib.request.urlopen(x['url'],timeout=25) as response:payload=response.read();code=response.status
 actual=hashlib.sha256(payload).hexdigest();assert code==200 and actual==sha(p),path
 return dict(path=path,status=code,bytes=len(payload),sha256=actual,exact_local_bytes=True,browser_lazy_load_observed=x['nativeLoaded'])
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:results=list(executor.map(fetch,references))
write(proof/'RESOURCE_AVAILABILITY.json',dict(status='ALL104_DECLARED_IMAGE_RESOURCES_FETCHED_EXACT',start_utc=start,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),items=results,qualification='Exact allowlisted loopback GET bytes only. Browser94 cards/104 images/no horizontal overflow and screenshots are separately recorded. Lazy images not all visibly loaded at once; no runtime/action acceptance.'))
write(proof/'QUALIFICATION.json',dict(status='PASS_SCOPED_DESKTOP_LIBRARY_PREVIEW',registered_items=1519,shared_individual_cards=94,declared_image_elements=104,desktop_browser_viewport=1280,page_scroll_width=1265,all104_exact_local_resources_available=True,qualification='Three saved browser screenshots directly viewed. Shared-source artwork/static opinions were directly reviewed at native scale separately. 94 region cards and 1519-item searchable register render without horizontal overflow in this desktop observation. This does not assign phone/runtime/complete-action acceptance.'))
shutil.copyfile(Path(__file__),proof/'executed_verify_native_library_and_gates_v71.py')
license=r/'ASSET_LICENSES.md';text=license.read_text(encoding='utf-8')
for p in proof.glob('*.png'):
 if f'`{rel(p)}`' not in text:text+=f'\n| `{rel(p)}` | Codex browser screenshot of the local illustrated audit library, SHA-256 `{sha(p)}`; underlying artwork/source provenance remains in its individual report. | Project audit evidence; original artwork licenses retained. | Internal browser capture, 2026-10-01. | Unmodified desktop preview screenshot; no new game art or runtime/device/owner acceptance. |\n'
license.write_text(text,encoding='utf-8',newline='\n')
recordfile=r/'design/audit_impacts/job-shared-native-source-review-20261001.json';record=read(recordfile);record['files']=sorted(set(record['files'])|{rel(p) for p in shared.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'})
record['validation'].append(dict(command='Desktop browser DOM/screenshot and104 exact allowlisted image GETs',result='PASS',evidence=rel(proof/'QUALIFICATION.json')+'; '+rel(proof/'RESOURCE_AVAILABILITY.json')));write(recordfile,record)
out=r/'audit/job_review_v2_20261001/current_native_supplement_gates_v2';assert not out.exists();out.mkdir()
(out/'.gdignore').write_text('')
shutil.copyfile(Path(__file__),out/'executed_verify_native_library_and_gates_v71.py')
snapshot=read(r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json')
mismatches=[x['path'] for x in snapshot['source_files'] if sha(r/x['path'])!=x['sha256']]
assert not mismatches,mismatches
write(out/'LITERAL_SOURCE_BOUNDARY.json',dict(status='ALL325_LITERAL_PRODUCTION_SOURCES_UNCHANGED',source_snapshot_path='audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json',source_snapshot_sha256=sha(r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json'),source_count=len(snapshot['source_files']),mismatches=mismatches,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Unchanged literal production boundary preserves earlier82/82 official4.7.2 local full-suite evidence and51 diagnostics. No current full-action or new hosted pass is inferred.'))
template=read(recordfile)
impact=dict(id='job-native-supplement-gates-20261001',scope='Exact structural/literal-source verification for the source-only shared native region, reaching/clean image and reference-motion/contact supplement. Preserve failed art/motion grades and original byte maps, verify new native fixture scripts and document/development/2D gates, stage exact coverage before a separate review-only publication.',baseline='56d66f63e375b61cf02936b426a05a2b92c14d3b',rules=template['rules'],findings=template['findings'],files=sorted(rel(p) for p in out.rglob('*') if p.is_file()),validation=[dict(command='Static supplement gates',result='PENDING',evidence=rel(out))],acceptance_gaps='Game code and all325 literal sources unchanged; no global4.5/complete-action/device/child/owner/strict2D/release acceptance. New exact hosted candidate pending.')
impactfile=r/'design/audit_impacts/job-native-supplement-gates-20261001.json';write(impactfile,impact)
scripts=['audit/day_two_wash_contact_study_v1_20261001/attempt_04/executed_capture_doctor_sink_contact_v58.gd','audit/day_two_wash_contact_study_v1_20261001/attempt_05/capture.gd']
assert all((r/p).is_file() for p in scripts)
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*scripts]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*scripts]),('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('game2d',[sys.executable,'-X','utf8','-B','tools/audit_game_2d.py']),('contract_tests',[sys.executable,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])]
rows=[]
for name,command in commands:
 impact['files']=sorted(rel(p) for p in out.rglob('*') if p.is_file());write(impactfile,impact)
 proc=subprocess.run(command,cwd=r,capture_output=True)
 for channel,payload in [('stdout',proc.stdout),('stderr',proc.stderr)]:(out/(name+'.'+channel+'.log')).write_bytes(payload)
 rows.append(dict(name=name,command=command,process_exit=proc.returncode,stdout=rel(out/(name+'.stdout.log')),stderr=rel(out/(name+'.stderr.log'))));print(name,proc.returncode,flush=True)
 if proc.returncode:print(proc.stdout[-5000:].decode('utf-8','replace'),proc.stderr[-2000:].decode('utf-8','replace'),flush=True);break
passed=len(rows)==len(commands) and all(x['process_exit']==0 for x in rows)
write(out/'RECEIPT.json',dict(status='PASS_STATIC_NATIVE_REVIEW_GATES' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,changed_review_gd=scripts,literal_sources_unchanged=True,qualification=impact['acceptance_gaps']))
impact['files']=sorted(rel(p) for p in out.rglob('*') if p.is_file());impact['validation']=[dict(command='Parser/inference, document authority, development auto-base, existing2D gate and contract tests',result='PASS' if passed else 'FAIL',evidence=rel(out/'RECEIPT.json'))];write(impactfile,impact)
registry=read(r/'audit/job_artwork_refinement_live/ALL_ITEMS.json')
unknown=[dict(id=x['id'],path=x['path'],families=x['families']) for x in registry['items'] if x['kind']=='source' and x['current_source_score'] is None and x['path'].startswith(('assets/opera/','assets/flats/','assets/characters/roshan_25d/'))]
write(r/'tmp/remaining_job_source_candidates_v71.json',unknown)
print(json.dumps(dict(all104_resources_exact=True,remaining_job_source_candidates=unknown[:18],static_gates_pass=passed,literal_production_sources=len(snapshot['source_files']))))
raise SystemExit(0 if passed else 1)
