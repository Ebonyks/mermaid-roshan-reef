from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
S2=R/'assets_src/imagegen/nursery_palm_attention_v1_20261002'
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
mp='audit/job_review_v2_20261001/CONNECTED_NURSERY_WASH_SUPPLEMENT_FILES_V12.json'
prior='audit/job_review_v2_20261001/GEOLOGY_SUPPORTED_GEODE_SUPPLEMENT_FILES_V11.json'
baseline='e4e26aeaa1f7e55985cb3915d35dca5aeba00d40'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args,input=None):return subprocess.run(['git',*args],cwd=R,input=input,capture_output=True,check=True).stdout
target=F/'review_tools'/Path(__file__).name
if Path(__file__).resolve()!=target.resolve():shutil.copyfile(Path(__file__),target)
imp=read(ip);imp['files']=sorted(set(imp['files'])|{target.relative_to(R).as_posix()});write(ip,imp)
if '--prepare' in __import__('sys').argv:
 print('SCOPED_O_SEAL_HELPER_PREPARED');raise SystemExit(0)
assert git('rev-parse','HEAD').decode().strip()==baseline
assert git('branch','--show-current').decode().strip()=='codex/job-art-review-v2-20261001'
ci=read(F/'full_ci_v1/RECEIPT.json')
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and ci['overall_process_exit']==0
assert len(ci['source_checks'])==783 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(sha((R/x['path']).read_bytes())==x['before_sha256'] for x in ci['source_checks'])
for n in ['stdout','stderr']:assert sha((F/'full_ci_v1'/(n+'.log')).read_bytes())==ci[n+'_sha256']
for label in ['parser_v1','inference_v1','analyzer_v1','authority_v3','development_v3']:
 assert read(F/'runtime_gate'/(label+'.receipt.json'))['status']=='PASS',label
assert read(F/'DIRECT_REVIEW_CURRENT_V3.json')['source_boundary_unchanged']
assert read(F/'BROWSER_QA_V381.json')['status']=='PASS_REVIEW_UI_ONLY'
assert read(S2/'REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
assert read(S2/'PLAN.json')['status']=='BLOCKED_AWAITING_EXPLICIT_REFERENCE_UPLOAD_APPROVAL'
scope=set(imp['files'])|{ip.relative_to(R).as_posix()}
staged={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}
assert staged<=scope,'Unrelated staged changes remain untouched.'
for path in scope:
 assert (R/path).resolve().is_relative_to(R.resolve()) and (R/path).is_file(),path
 assert not path.startswith(('.git/','.secrets/','.codex/','.claude/','.github/','assets/book/','assets/audio/voices/','assets/characters/friends/')),path
paths=''.join(p+'\0' for p in sorted(scope)).encode()
git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',input=paths)
git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',input=paths)
bridge=F/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V381.json';checks=[]
aux=read(F/'PUBLICATION_AUXILIARY_UID_INDEX_V384.json')
assert aux['original_local_ci_members']==783 and len(aux['uids'])==240 and aux['revision_source_members']==543
uid_map={x['original_local_path']:x for x in aux['uids']}
for x in ci['source_checks']:
 raw=(R/x['path']).read_bytes();auxiliary=x['path'] in uid_map
 published_path=uid_map[x['path']]['published_snapshot_path'] if auxiliary else x['path']
 if auxiliary:assert (R/published_path).read_bytes()==raw
 staged_blob=git('show',':'+published_path)
 text=Path(x['path']).suffix.lower() in {'.gd','.godot','.import','.json','.tres','.tscn','.sh','.py','.uid','.cfg'}
 normalize=lambda d:d.replace(b'\r\n',b'\n') if text else d
 assert normalize(raw)==normalize(staged_blob),x['path']
 checks.append({'path':x['path'],'git_blob_path':published_path,'role':'generated_uid_qa_snapshot' if auxiliary else 'revision_source_or_import','literal_local_sha256':sha(raw),'exact_git_blob_sha256':sha(staged_blob),'bytes_git':len(staged_blob),'declared_text_newline_comparison':text,'literal_bytes_match':raw==staged_blob,'canonical_equivalence':True})
write(bridge,{'status':'PASS_ALL783_PUBLICATION_BOUNDARY_MEMBERS','source_count':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'checks':checks,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Full CI preserves all783 literal local hashes. Publication verifies543 revision source/import files and240 unchanged generated script UID snapshots at explicit non-runtime QA paths. No frozen member is omitted and no generated UID snapshot is promoted into runtime scripts. For declared source text only, Git LF and Windows CRLF may compare canonically. Native image/audio and QA snapshot bytes remain literal. Remote verification uses each exact git_blob_path; this does not grant hosted/visual/device/child/owner acceptance.'})
git('add','-f','--',bridge.relative_to(R).as_posix())
changed={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}
assert changed<=scope and mp in changed
def blobs(ref,paths):
 result={};proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for path in paths:
   proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush()
   header=proc.stdout.readline().split();assert len(header)==3 and header[1]==b'blob',path
   n=int(header[2]);left=n;digest=hashlib.sha256()
   while left:
    block=proc.stdout.read(min(left,65536));assert block,path;digest.update(block);left-=len(block)
   assert proc.stdout.read(1)==b'\n';result[path]=[n,digest.hexdigest()]
  proc.stdin.close();assert proc.wait(timeout=30)==0
 finally:
  if proc.poll() is None:proc.terminate();proc.wait(timeout=30)
 return result
files=blobs('',sorted(changed-{mp}))
for root in [F,S,P,S2]:
 for p in root.rglob('*'):
  path=p.relative_to(R).as_posix()
  if p.is_file() and path in files:assert files[path]==[p.stat().st_size,sha(p.read_bytes())],path
registry=read(R/'audit/job_artwork_refinement_live/ALL_ITEMS.json');assert len(registry['items'])==1756
prior_raw=git('show','HEAD:'+prior);old=json.loads(prior_raw)
refs=set(old['files'])|set(old.get('unchanged_required_files',{}))|{prior}
for item in registry['items']:
 refs.add(item['image_path']);refs.update(p.split('#')[0] for p in item['original_reports'])
refs.update(x['git_blob_path'] for x in checks);refs-=set(files);refs.discard(mp)
for path in refs:assert not path.startswith(('.secrets/','.git/','.codex/','.claude/')),path
unchanged=blobs('HEAD',sorted(refs))
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m={'schema':'reef.immutable-review-supplement.v1','base_revision':baseline,'prior_closed_map':prior,'prior_closed_map_sha256':sha(prior_raw),'required_files':len(files),'required_payload_bytes':sum(v[0] for v in files.values()),'payload_sha256':sha(formula),'payload_hash_formula':'SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF','files':files,'required_unchanged_files':len(unchanged),'unchanged_required_files':unchanged,'qualification':'Connected Nursery washing v3 reversible draft. Seven1254-square native sources and seven1024-POT whole-canvas derivatives preserved, six selected mounted states4.5–4.6; weak clasp4.4 and earlier boxing-puff overlap preserved. Current meaningful wash3.9/attention3.8/room2.9/transition4.0 remain priorities; static floor is not motion approval. Direct all1631 current consecutive frames on36 complete QA boards plus36 full native details across four direct training/authored catalog fixtures and actual Bubble Bath card/caller partial-career routes1280/1600. No ordinary birthday or complete-career reward claim; both roles absent from current birthday roster. Current v3 clean result no generic boxing puff; source/mechanics owners preserved. V34.1 register1756 entries,690 source/cell/region inclusive priorities,10 extra current Nursery state/use/action priorities,385 unassigned source reviews; old Geologist mounted claims withheld after shared CareerWorld changed. All1023 preserved dated Doctor frames on24 boards plus12 native details directly reviewed;12 individual dated priorities and whole2.7 retained, no current Doctor improvement claim. Local ComfyUI A1 exact developed GGUF graph machine render passes; all41 unchanged native frames directly inspected and reference action3.6/contact3.8/attention3.1 rejected. Failed native output/input/prompt/workflow/dispatch and initial overlapping QA boards preserved; no runtime/cinematic integration. Targeted eyes-to-hands source edit blocked before any reference upload by automatic approval review, exact source/destination authorization pending; no generated attention art exists. Official Godot4.7.2 unmodified local full suite82/82 process0 on783 unchanged literal local members (543 revision source/import files and240 preserved generated script UID snapshots),53 raw engine diagnostics retained; separate exact revision/auxiliary publication bridge, authority/development/parser/inference/analyzer and UI evidence. Global visual/strict2D, device/child/owner/all-job completion/integration/release remain open. Publication is durable review evidence, not a workaround for the blocked image-generation upload; that action remains prohibited until explicitly authorized.'}
write(R/mp,m);git('add','-f','--',mp)
raw=git('show',':'+mp)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(files)|{mp}
seal={'status':'EXACT_SCOPED_O_BLOBS_SEALED','base_revision':baseline,'map_path':mp,'map_sha256':sha(raw),'payload_sha256':m['payload_sha256'],'payload_files':len(files),'payload_bytes':m['required_payload_bytes'],'unchanged_required_files':len(unchanged),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_bridge':bridge.relative_to(R).as_posix(),'qualification':'Exact topic checkpoint only; anonymous immutable remote verification and fresh hosted probes remain pending. No acceptance, integration, release or blocked imagegen-reference upload authorization.'}
out=R/'tmp/connected_nursery_checkpoint_o_sealed_v385.json';assert not out.exists();write(out,seal)
print(json.dumps(seal),flush=True)
