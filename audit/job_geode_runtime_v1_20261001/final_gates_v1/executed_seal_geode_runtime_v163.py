from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, time

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
base='d13a28287ef6916fb9c910de9c07d110ced315c2'
branch='codex/job-art-review-v2-20261001'
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
family=b/'audit/job_geode_runtime_v1_20261001'
out=family/'final_gates_v1'
mp='audit/job_review_v2_20261001/GEOLOGY_RUNTIME_REVIEW_SUPPLEMENT_FILES_V6.json'
prior='audit/job_review_v2_20261001/GEOLOGY_OPENING_MOTION_SUPPLEMENT_FILES_V5.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git','-c','core.safecrlf=false',*args],cwd=b,capture_output=True,check=True).stdout
full=json.loads((family/'full_ci_v2/RECEIPT.json').read_text())
assert full['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE',full['status']
assert len(full['probe_results'])==82 and full['source_unchanged']
sources=json.loads((family/'full_ci_v2/SOURCE_BEFORE.json').read_text())['source_files']
assert len(sources)==334 and all(sha(b/p['path'])==p['sha256'] for p in sources)
assert git('rev-parse','HEAD').decode().strip()==base
assert git('branch','--show-current').decode().strip()==branch
assert not git('diff','--cached','--name-only').strip()
assert not out.exists() and not (b/mp).exists()
out.mkdir()
shutil.copyfile(__file__,out/'executed_seal_geode_runtime_v163.py')
named=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md',ip.relative_to(b).as_posix(),
 'scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','tools/capture_geode_runtime_route.gd',
 'assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html','assets_src/imagegen/geologist_painted_rebuild_v1_20261001/REVIEW_V7.json',
 'audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/STATUS.json',
 'audit/job_review_v2_20261001/index.html','audit/job_review_v2_20261001/GEOLOGY_CONTINUATION_REPORT_V5.html',
 'audit/job_artwork_refinement_live/review_tools/build_current_job_item_register_v19.py',
 'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v19.py',
 'audit/job_artwork_refinement_live/review_tools/build_current_job_item_register_v20.py',
 'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v20.py']
helpers=['install_geode_runtime_v152.py','prepare_geode_runtime_evidence_v153.py','run_geode_runtime_gates_v154.py','fix_geology_celebration_v156.py',
 'run_geode_runtime_gates_v156.py','prepare_geode_full_ci_v157.py','prepare_geode_final_boundary_v158.py','prepare_geode_capture_v159.py',
 'run_geode_runtime_gates_v160.py','record_geode_runtime_review_v161.py','update_geode_authority_v162.py']
named.extend('audit/job_review_v2_20261001/review_tools/'+x for x in helpers)
prefixes=['audit/job_geode_runtime_v1_20261001','audit/job_review_v2_20261001/opening_motion_remote_verified_v5','assets/opera/worlds/geology/painted_geode_v1_20261001']
def paths():
 result={p for p in named if (b/p).is_file()}
 for prefix in prefixes:result.update(p.relative_to(b).as_posix() for p in (b/prefix).rglob('*') if p.is_file() and p.suffix not in ['.pyc','.uid'])
 return sorted(result)
def cover():
 d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|set(paths())|{mp});write(ip,d)
changed={x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x}|{x.decode() for x in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if x}
assert not changed-set(paths()),sorted(changed-set(paths()))
gds=['scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','tools/capture_geode_runtime_route.gd']
for p in paths():
 if p.endswith('.py'):compile((b/p).read_text(encoding='utf-8-sig'),p,'exec')
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',*gds]),
 ('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',*gds]),
 ('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),
 ('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]
rows=[]
for name,cmd in commands:
 a=out/(name+'.stdout.log');c=out/(name+'.stderr.log');a.touch();c.touch();cover();start=time.monotonic()
 with a.open('wb') as so,c.open('wb') as se:p=subprocess.run(cmd,cwd=b,stdout=so,stderr=se,timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
 rows.append({'name':name,'command':cmd,'process_exit':p.returncode,'elapsed_seconds':time.monotonic()-start,'stdout':a.relative_to(b).as_posix(),'stderr':c.relative_to(b).as_posix()})
 print(name,p.returncode,flush=True)
 assert p.returncode==0,a.read_text(encoding='utf-8',errors='replace')[-2000:]+c.read_text(encoding='utf-8',errors='replace')[-900:]
assert all(sha(b/p['path'])==p['sha256'] for p in sources)
write(out/'RECEIPT.json',{'status':'PASS_SCOPED_PRODUCTION_REVIEW_MACHINE_GATES','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'processes':rows,'full_ci':'audit/job_geode_runtime_v1_20261001/full_ci_v2/RECEIPT.json','source_files':334,'source_unchanged':True,
 'probe_count':82,'raw_full_ci_diagnostics':full['raw_diagnostic_count'],
 'qualification':'Actual work-branch geode binding and geologist celebration repair; all36 current native views individually reviewed. Engine diagnostics are retained unfiltered. Scoped machine results do not close room/contact/flat siblings, full timed action, castle/story entry, strict2D, device/child/owner/final all-job acceptance or authorize integration/release.'})
d=json.loads(ip.read_text());d['validation'].append({'command':'Final changed GDScript parser/inference and current authority/development gates; source334 matches new82/82 full suite','result':'PASS','evidence':(out/'RECEIPT.json').relative_to(b).as_posix()});write(ip,d);cover()
pathfile=b/'tmp/geode_runtime_v163_paths.nul';pathfile.write_bytes(b'\0'.join(p.encode() for p in paths())+b'\0')
git('add','--force','--pathspec-from-file='+str(pathfile),'--pathspec-file-nul')
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}
assert staged<=set(paths()) and all(not p.endswith('.import') or p.startswith(prefixes[2]+'/') for p in staged)
ordered=sorted(staged);data=subprocess.run(['git','cat-file','--batch'],cwd=b,input=''.join(':'+p+'\n' for p in ordered).encode(),capture_output=True,check=True).stdout
offset=0;files={}
for p in ordered:
 end=data.index(b'\n',offset);size=int(data[offset:end].split()[2]);offset=end+1;raw=data[offset:offset+size];offset+=size+1;files[p]=[len(raw),hashlib.sha256(raw).hexdigest()]
assert offset==len(data)
digest=hashlib.sha256(''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in files.items()).encode()).hexdigest()
write(b/mp,{'schema':'reef.immutable-review-supplement.v1','base_revision':base,'prior_closed_map':prior,'prior_closed_map_sha256':sha(b/prior),
 'required_files':len(files),'required_payload_bytes':sum(v[0] for v in files.values()),'payload_sha256':digest,
 'payload_hash_formula':'SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF','files':files,
 'qualification':'Additive canonical Git-blob map for actual geode runtime candidate, native four-phase route evidence and visible clapping/rest repair. Preserves originals and all prior scoped maps. All82 fresh local probes and334 literal sources verified,36 current native views directly inspected. Not final whole-job quality, cinematic, device/child/owner/integration/release acceptance.'})
git('add','--force',mp)
for name,cmd in commands[-2:]:
 p=subprocess.run(cmd,cwd=b,capture_output=True,timeout=600);(b/('tmp/geode_runtime_v163_staged_'+name+'.stdout.log')).write_bytes(p.stdout);(b/('tmp/geode_runtime_v163_staged_'+name+'.stderr.log')).write_bytes(p.stderr)
 print('staged_'+name,p.returncode,flush=True);assert p.returncode==0,p.stdout.decode(errors='replace')[-1800:]
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==staged|{mp}
write(b/'tmp/geode_runtime_v163_sealed.json',{'base_revision':base,'branch':branch,'map_path':mp,'map_sha256':hashlib.sha256(git('show',':'+mp)).hexdigest(),'payload_sha256':digest,'files':len(files),'bytes':sum(v[0] for v in files.values()),'qualification':'Sealed staged checkpoint; not yet committed or pushed.'})
print('SEALED',len(files),digest,flush=True)
