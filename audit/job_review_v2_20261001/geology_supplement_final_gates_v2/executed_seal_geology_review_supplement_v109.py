from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time,datetime
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=r/'audit/job_review_v2_20261001/geology_supplement_final_gates_v2';assert not out.exists();out.mkdir()
base='6edb4ca8c57bfbfe3123636863a29c95165ac23f';branch='codex/job-art-review-v2-20261001'
def git(*args):return subprocess.run(['git',*args],cwd=r,capture_output=True,check=True).stdout
def rel(p):return p.relative_to(r).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert git('rev-parse','HEAD').decode().strip()==base and git('branch','--show-current').decode().strip()==branch
assert not git('diff','--cached','--name-only').strip()
shutil.copyfile(__file__,out/'executed_seal_geology_review_supplement_v109.py')
impact=r/'design/audit_impacts/job-geology-painted-rebuild-20261001.json'
prefixes=['assets_src/imagegen/geologist_painted_rebuild_v1_20261001','audit/job_geode_embedded_mount_v2_20261001','audit/job_geology_painted_mount_v1_20261001','audit/job_vector_mount_review_v1_20261001','audit/job_pan_painted_mount_v2_20261001','audit/job_review_v2_20261001/current_native_supplement_remote_v2','audit/job_review_v2_20261001/hosted_native_supplement_v2','audit/job_review_v2_20261001/geology_supplement_gates_v1',rel(out)]
named=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','assets_src/vector/job_geology_teacher_refinement_v1_20261001/index.html','assets_src/vector/job_geology_teacher_refinement_v1_20261001/OWNER_CORRECTION_V1.json','audit/job_review_v2_20261001/index.html','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/ALL_ITEMS.html','audit/job_artwork_refinement_live/STATUS.json','design/audit_impacts/job-geology-painted-rebuild-20261001.json','design/audit_impacts/job-vector-mounted-review-20261001.json','design/audit_impacts/job-review-separate-v2-20261001.json']
named.extend('audit/'+parent+'/review_tools/build_current_job_item_register_v'+str(n)+'.py' for parent in ['job_artwork_refinement_live','job_review_v2_20261001'] for n in [13,14,15])
def payload_paths():return sorted({rel(p) for prefix in prefixes for p in (r/prefix).rglob('*') if p.is_file()}|{p for p in named if (r/p).is_file()})
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{p for p in payload_paths() if not p.startswith('design/audit_impacts/')});write(impact,d)
cover()
current={x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x}|{x.decode() for x in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if x};unknown=current-set(payload_paths());assert not unknown,sorted(unknown)
snapshot=json.loads((r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];before={x['path']:sha(r/x['path']) for x in snapshot};assert len(before)==325 and all(before[x['path']]==x['sha256'] for x in snapshot)
write(out/'BOUNDARY.json',dict(baseline=base,branch=branch,literal_source_count=325,all_literal_sources_match_passing_full_suite=True,prior_full_ci='audit/job_review_v2_20261001/full_ci_candidate_retry_v2/RECEIPT.json',prior_exact_hosted_ci='audit/job_review_v2_20261001/hosted_native_supplement_v2/RECEIPT.json',production_geology_bindings_changed=False,original_closed_map_sha256=sha(r/'audit/job_review_v2_20261001/CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2.json')))
gds=sorted(rel(p) for prefix in prefixes[:5] for p in (r/prefix).rglob('*.gd'))
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*gds]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*gds]),('import',[godot,'--headless','--path',str(r),'--import']),('contract_tests',[sys.executable,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']),('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]
rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as b:
  try:p=subprocess.run(cmd,cwd=r,stdout=a,stderr=b,timeout=240 if name=='import' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed_out=False
  except subprocess.TimeoutExpired:code=None;timed_out=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed_out,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(so.read_text(encoding='utf-8',errors='replace')[-1500:],se.read_text(encoding='utf-8',errors='replace')[-500:],flush=True);break
passed=len(rows)==len(cmds) and all(x['process_exit']==0 for x in rows) and all(sha(r/p)==h for p,h in before.items())
write(out/'RECEIPT.json',dict(status='PASS_FINAL_REVIEW_SUPPLEMENT_GATES' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,review_gd_files=gds,source_unchanged=all(sha(r/p)==h for p,h in before.items()),qualification='Runtime325-file full suite and hostedD exact CI carry forward only unchanged sources. New source-only generation14 and every220 native fixture view are individually reviewed. Current complete training/story/device/child/owner/final report approval and strict2D remain open.'))
cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='Final supplement12 review GDs parser/inference/official4.7.2 import/contract tests/authority/development and325-source boundary',result='PASS' if passed else 'FAIL',evidence=rel(out/'RECEIPT.json')));write(impact,d);assert passed
# Force only enumerated ignored review payload files. Preserve all originals and closed maps.
paths=payload_paths();pathfile=r/'tmp/geology_supplement_v109_paths.nul';pathfile.write_bytes(b'\0'.join(p.encode() for p in paths)+b'\0');git('add','--force','--pathspec-from-file='+str(pathfile),'--pathspec-file-nul')
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=set(paths) and not any(p.endswith('.import') for p in staged)
map_path='audit/job_review_v2_20261001/GEOLOGY_PAINTED_REVIEW_SUPPLEMENT_FILES_V3.json';assert not (r/map_path).exists()
files={p:[len(b),hashlib.sha256(b).hexdigest()] for p in sorted(staged) for b in [git('show',':'+p)]}
digest=hashlib.sha256(''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in files.items()).encode()).hexdigest()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=base,prior_closed_map='audit/job_review_v2_20261001/CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2.json',prior_closed_map_sha256=sha(r/'audit/job_review_v2_20261001/CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2.json'),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=digest,payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,qualification='Closed canonical-Git-blob map for current reversible painted geology supplement only; old maps/receipts immutable. No runtime replacement or global visual/device/child/owner acceptance.')
write(r/map_path,m);d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{map_path});write(impact,d);git('add','--force',map_path,rel(impact))
# The impact changed after mapping; rebuild only this new map before sealing it.
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};files={p:[len(b),hashlib.sha256(b).hexdigest()] for p in sorted(staged-{map_path}) for b in [git('show',':'+p)]};m['files']=files;m['required_files']=len(files);m['required_payload_bytes']=sum(v[0] for v in files.values());m['payload_sha256']=hashlib.sha256(''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in files.items()).encode()).hexdigest();write(r/map_path,m);git('add','--force',map_path)
for name,cmd in [('staged_authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('staged_development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 p=subprocess.run(cmd,cwd=r,capture_output=True,timeout=600);(r/('tmp/geology_supplement_v109_'+name+'.stdout.log')).write_bytes(p.stdout);(r/('tmp/geology_supplement_v109_'+name+'.stderr.log')).write_bytes(p.stderr);print(name,p.returncode,flush=True);assert p.returncode==0,p.stdout.decode(errors='replace')[-1500:]
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{map_path}
assert all([len(b),hashlib.sha256(b).hexdigest()]==v for p,v in files.items() for b in [git('show',':'+p)])
write(r/'tmp/geology_supplement_v109_sealed.json',dict(status='SEALED_AND_STAGED_GEOLOGY_REVIEW_SUPPLEMENT',base_revision=base,map_path=map_path,map_sha256=hashlib.sha256(git('show',':'+map_path)).hexdigest(),files=m['required_files'],payload_bytes=m['required_payload_bytes'],payload_sha256=m['payload_sha256'],qualification='Ready for topic-branch checkpoint publication. All old maps unchanged; no production binding or final owner approval.'))
print('SEALED',m['required_files'],m['required_payload_bytes'],m['payload_sha256'],flush=True)
