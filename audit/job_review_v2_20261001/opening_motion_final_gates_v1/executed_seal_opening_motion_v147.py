from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time,datetime
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'audit/job_review_v2_20261001/opening_motion_final_gates_v1';out.mkdir(exist_ok=False)
base='edbf2a60e4a73ca149ee53b7f8d01990afd32198';branch='codex/job-art-review-v2-20261001'
def git(*args):return subprocess.run(['git',*args],cwd=b,capture_output=True,check=True).stdout
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert git('rev-parse','HEAD').decode().strip()==base and git('branch','--show-current').decode().strip()==branch
assert not git('diff','--cached','--name-only').strip()
shutil.copyfile(__file__,out/'executed_seal_opening_motion_v147.py')
ip=b/'design/audit_impacts/job-geology-opening-motion-review-checkpoint-20261001.json'
prefixes=['assets_src/imagegen/geologist_painted_rebuild_v1_20261001','audit/job_geode_opening_states_v3_20261001','assets_src/local_motion/day2_geologist_pan_motion_v1_20261001','assets_src/local_motion/day2_geologist_pan_motion_v2_20261001','assets_src/local_motion/day2_geologist_pan_motion_v3_20261001','audit/job_review_v2_20261001/pan_contact_remote_verified_v4',rel(out)]
named=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','audit/job_review_v2_20261001/index.html','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/ALL_ITEMS.html','audit/job_artwork_refinement_live/STATUS.json',rel(ip),'design/audit_impacts/job-review-separate-v2-20261001.json','design/audit_impacts/job-geode-opening-continuity-20261001.json','design/audit_impacts/job-geologist-panning-local-motion-20261001.json','audit/job_review_v2_20261001/GEOLOGY_CONTINUATION_REPORT_V5.html','audit/job_review_v2_20261001/GEOLOGY_CONTEXT_PRIORITIES_V5.json']
named.extend('audit/'+parent+'/review_tools/build_current_job_item_register_v18.py' for parent in ['job_artwork_refinement_live','job_review_v2_20261001'])

named.append('audit/job_review_v2_20261001/review_tools/build_geology_context_report_v149.py')

def paths():return sorted({rel(p) for prefix in prefixes for p in (b/prefix).rglob('*') if p.is_file() and p.suffix not in ['.import','.uid']}|{p for p in named if (b/p).is_file()})
def cover():
 d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p for p in paths() if not p.startswith('design/audit_impacts/')});write(ip,d)

cover()
current={x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x}|{x.decode() for x in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if x};unknown=current-set(paths());assert not unknown,sorted(unknown)
receipt_dir=out;gh='C:/Program Files/GitHub CLI/gh.exe';cmd=[gh,'run','view','36959921507','--repo','Ebonyks/mermaid-roshan-reef','--json','status,conclusion,headSha,createdAt,updatedAt,url,jobs'];run=subprocess.run(cmd,cwd=b,capture_output=True,timeout=120);(receipt_dir/'HOSTED_RUN_SNAPSHOT.stdout.json').write_bytes(run.stdout);(receipt_dir/'HOSTED_RUN_SNAPSHOT.stderr.log').write_bytes(run.stderr);write(receipt_dir/'HOSTED_RUN_SNAPSHOT_RECEIPT.json',dict(command=cmd,process_exit=run.returncode,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Exact F hosted result at this check time only. No new supplement or owner acceptance.'));assert run.returncode==0
hosted=json.loads(run.stdout);assert hosted['headSha']==base
print('hostedF',hosted['status'],hosted['conclusion'],flush=True)
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];before={x['path']:sha(b/x['path']) for x in snapshot};assert len(before)==325 and all(before[x['path']]==x['sha256'] for x in snapshot)
write(out/'BOUNDARY.json',dict(baseline=base,branch=branch,literal_source_count=325,all_literal_sources_match_passing_full_suite=True,prior_full_ci='audit/job_review_v2_20261001/full_ci_candidate_retry_v2/RECEIPT.json',prior_exact_hosted_ci='audit/job_review_v2_20261001/hosted_native_supplement_v2/RECEIPT.json',hosted_F_snapshot=rel(receipt_dir/'HOSTED_RUN_SNAPSHOT.stdout.json'),production_bindings_changed=False,prior_closed_map_sha256=sha(b/'audit/job_review_v2_20261001/GEOLOGY_PAN_CONTACT_SUPPLEMENT_FILES_V4.json')))
gds=sorted(rel(p) for p in (b/prefixes[1]).rglob('*.gd'));assert len(gds)==6,len(gds)
for prefix in prefixes:
 for p in (b/prefix).rglob('*.py'):compile(p.read_text(encoding='utf-8-sig'),rel(p),'exec')

godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*gds]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*gds]),('import',[godot,'--headless','--path',str(b),'--import']),('contract_tests',[sys.executable,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']),('2d_regression',[sys.executable,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate']),('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]
rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as c:
  try:p=subprocess.run(cmd,cwd=b,stdout=a,stderr=c,timeout=240 if name=='import' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(so.read_text(encoding='utf-8',errors='replace')[-1700:],se.read_text(encoding='utf-8',errors='replace')[-500:],flush=True);break
passed=len(rows)==len(cmds) and all(x['process_exit']==0 for x in rows) and all(sha(b/p)==h for p,h in before.items())
write(out/'RECEIPT.json',dict(status='PASS_REVIEW_SUPPLEMENT_MACHINE_GATES' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=rows,review_gd_files=gds,source325_unchanged=all(sha(b/p)==h for p,h in before.items()),strict_2d_status='UNSATISFIED; regression-only pass is not strict zero debt',qualification='Original325-source82/82 full suite and hostedD validation carry forward only byte-identical production sources. New6 disposable geode scripts plus local motion Python syntax and official import/contract/authority/development/2D regression gates are checked. Every312 selected native comparison and current reference frame reviews are individually qualified; no full ordinary route/device/child/owner/goal acceptance.'))
cover();d=json.loads(ip.read_text());d['validation'].append(dict(command='6 disposable geode GDs parser/inference and motion Python syntax, official4.7.2 import, authority/development/contract tests,2D regression and325-source boundary',result='PASS' if passed else 'FAIL',evidence=rel(out/'RECEIPT.json')));write(ip,d);assert passed
pathfile=b/'tmp/opening_motion_v147_paths.nul';pathfile.write_bytes(b'\0'.join(p.encode() for p in paths())+b'\0');git('add','--force','--pathspec-from-file='+str(pathfile),'--pathspec-file-nul')
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=set(paths()) and not any(p.endswith('.import') for p in staged)
mp='audit/job_review_v2_20261001/GEOLOGY_OPENING_MOTION_SUPPLEMENT_FILES_V5.json';assert not (b/mp).exists()
d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{mp});write(ip,d);git('add','--force',rel(ip))
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
ordered=sorted(staged);p=subprocess.run(['git','cat-file','--batch'],cwd=b,input=''.join(':'+x+'\n' for x in ordered).encode(),capture_output=True,check=True);data=p.stdout;offset=0;files={}
for path in ordered:
 end=data.index(b'\n',offset);header=data[offset:end].split();size=int(header[2]);offset=end+1;raw=data[offset:offset+size];offset+=size+1;files[path]=[len(raw),hashlib.sha256(raw).hexdigest()]
assert offset==len(data)
digest=hashlib.sha256(''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in files.items()).encode()).hexdigest()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=base,prior_closed_map='audit/job_review_v2_20261001/GEOLOGY_PAN_CONTACT_SUPPLEMENT_FILES_V4.json',prior_closed_map_sha256=sha(b/'audit/job_review_v2_20261001/GEOLOGY_PAN_CONTACT_SUPPLEMENT_FILES_V4.json'),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=digest,payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,qualification='Canonical Git blob map for the new reversible geode opening/local motion review supplement. Every previous map immutable; no production binding, complete motion/route/device/child/owner or release acceptance.');write(b/mp,m);git('add','--force',mp)
for name,cmd in [('staged_authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('staged_development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:
 p=subprocess.run(cmd,cwd=b,capture_output=True,timeout=600);(b/('tmp/opening_motion_v147_'+name+'.stdout.log')).write_bytes(p.stdout);(b/('tmp/opening_motion_v147_'+name+'.stderr.log')).write_bytes(p.stderr);print(name,p.returncode,flush=True);assert p.returncode==0,p.stdout.decode(errors='replace')[-1700:]
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{mp}
write(b/'tmp/opening_motion_v147_sealed.json',dict(status='SEALED_AND_STAGED_REVIEW_SUPPLEMENT',base_revision=base,map_path=mp,map_sha256=hashlib.sha256(git('show',':'+mp)).hexdigest(),files=m['required_files'],payload_bytes=m['required_payload_bytes'],payload_sha256=digest,qualification='Reversible topic review checkpoint only; whole-job goal and owner report acceptance remain open.'))
print('SEALED',m['required_files'],m['required_payload_bytes'],digest,flush=True)
