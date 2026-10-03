from pathlib import Path
import json,hashlib,datetime,subprocess,shutil,sys
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_painted_fracture_trial_v1_20261003';L=R/'audit/job_artwork_refinement_live'
BASE='ce154e1452c92252b90f5455989a21726d94ff62';BR='codex/job-art-review-v2-20261001'
MAP='audit/job_review_v2_20261001/GEOLOGY_FRACTURE_TRIAL_SUPPLEMENT_FILES_V18.json';PRIOR='audit/job_review_v2_20261001/GEOLOGY_COMPLETE_ACTION_AND_TRAY_SUPPLEMENT_FILES_V17.json'
IP=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json'
sha=lambda raw:hashlib.sha256(raw).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):p.write_text(json.dumps(d,ensure_ascii=False,**({'separators':(',',':')} if compact else {'indent':2}))+'\n',encoding='utf-8',newline='\n')
def git(*args,data=None):return subprocess.run(['git',*args],cwd=R,input=data,capture_output=True,check=True).stdout
def blobs(ref,paths):
 values={};proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 try:
  for path in sorted(paths):
   proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush();head=proc.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path
   n=int(head[2]);left=n;h=hashlib.sha256()
   while left:
    data=proc.stdout.read(min(left,65536));assert data;left-=len(data);h.update(data)
   assert proc.stdout.read(1)==b'\n';values[path]=[n,h.hexdigest()]
  proc.stdin.close();assert proc.wait(timeout=30)==0
 finally:
  if proc.poll() is None:proc.terminate();proc.wait(timeout=30)
 return values
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()==BR
target=J/'review_tools'/Path(__file__).name
if Path(__file__).resolve()!=target.resolve():shutil.copyfile(Path(__file__),target)
pre=Path(__file__).with_name('run_geology_precommit_v460.py').read_text(encoding='utf-8-sig').replace('tmp/geology_precommit_v460','tmp/geology_precommit_u_v475').replace('FINAL_STAGED_PRECOMMIT_GATES_ALL_PASS','U_FINAL_STAGED_PRECOMMIT_GATES_ALL_PASS')
compile(pre,'run_geology_precommit_u_v475.py','exec');(J/'review_tools/run_geology_precommit_u_v475.py').write_text(pre,encoding='utf-8',newline='\n');shutil.copyfile(J/'review_tools/run_geology_precommit_u_v475.py',Path(__file__).with_name('run_geology_precommit_u_v475.py'))
d=read(IP);d['files']=sorted(set(d['files'])|{target.relative_to(R).as_posix(),MAP,(J/'review_tools/run_geology_precommit_u_v475.py').relative_to(R).as_posix(),(J/'SCOPED_PUBLICATION_BOUNDARY_U.json').relative_to(R).as_posix(),(J/'INDEX_PATH_LENGTH_CHECK_U.json').relative_to(R).as_posix()});write(IP,d)
if '--prepare' in sys.argv:print('U_SEALER_PREPARED_NOT_STAGED');raise SystemExit(0)
for label in ['authority','development','document_tests','game2d']:assert read(J/'gates'/(label+'.receipt.json'))['status']=='PASS',label
for attempt,count in [(1,433),(2,435)]:
 review=read(J/f'DIRECT_REVIEW_ATTEMPT0{attempt}.json');assert review['consecutive_frames']==count and review['selected_views']==58 and len(review['opinions'])==12 and len(review['native_details'])==20 and review['production_binding'] is False and review['owner_acceptance'] is None
 boards=read(J/f'QA_BOARD_MANIFEST_A{attempt}.json')['boards'];assert len(boards)==47 and all(x['direct_review'] for x in boards)
 for b in boards:
  assert sha((R/b['path']).read_bytes())==b['sha256']
  for x in b['members']:assert sha((R/x['path']).read_bytes())==x['sha256']
 for p in (J/f'runtime_gate_a{attempt}').glob('*.receipt.json'):assert read(p)['status']=='PASS'
assert read(J/'DIRECT_REVIEW_ATTEMPT02.json')['opinions'][-1]['score']==3.6
register=read(L/'ALL_ITEMS.json');previous=read(L/'ALL_ITEMS_V40.original.json')
assert register['counts']==previous['counts'] and len(register['items'])==1821 and sum(len(x.get('candidate_reviews',[])) for x in register['items'])==24
assert read(J/'REGISTER_CHANGE_PROOF_V41.json')['current_mounted_scores_unchanged']
assert (L/'ALL_ITEMS.json').stat().st_size<4194304
oldreceipt=read(J/'previous_t_remote_verified/RESULT.json');assert oldreceipt['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and oldreceipt['revision']==BASE and oldreceipt['files_including_manifest']==18803
ji=read(J/'previous_t_remote_verified/JOURNAL_INDEX.json');raw=b''.join((R/x['path']).read_bytes() for x in ji['ordered_parts']);assert [len(raw),sha(raw)]==[ji['original_bytes'],ji['original_sha256']] and len(raw.splitlines())==18803
assert read(R/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
source=read(J/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(source)==783
checks=[dict(path=x['path'],sha256=sha((R/x['path']).read_bytes()),matches=sha((R/x['path']).read_bytes())==x['sha256']) for x in source];assert all(x['matches'] for x in checks)
write(J/'SCOPED_PUBLICATION_BOUNDARY_U.json',dict(status='ALL783_LITERAL_PRODUCTION_MEMBERS_UNCHANGED',checked_utc=now(),members=checks,qualification='Unbound renderer review trials only. Current game materials/actions/route, device/child/owner and all-job acceptance remain independently open. Existing local82/82 and parent hosted evidence are separate.'))
d=read(IP);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});write(IP,d);scope=set(d['files'])|{IP.relative_to(R).as_posix()}
retired=set(read(R/'audit/job_qa_scan_v2_20261002/REPLACED_PATHS.json')['paths']);assert not scope&retired
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=scope,staged-scope
tracked=[x.decode() for x in git('ls-files','-z').split(b'\0') if x]
lengths=sorted((len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+x),x) for x in set(tracked)|scope);assert lengths[-1][0]<260
write(J/'INDEX_PATH_LENGTH_CHECK_U.json',dict(status='PASS_CONSERVATIVE_WINDOWS_PATH_LENGTH',max_absolute_characters=lengths[-1][0],longest_members=lengths[-8:],qualification='Existing tracked plus exact new scope. No checkout/security/workflow relaxation.'))
for path in scope-{MAP}:
 p=(R/path).resolve();assert p.is_relative_to(R.resolve()) and p.is_file(),path
 assert not path.startswith(('.git/','.secrets/','.codex/','.claude/','.github/','scripts/','assets/')),path
paths=b''.join(x.encode()+b'\0' for x in sorted(scope-{MAP}));git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths);git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths)
changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope and not git('diff','--cached','--name-only','--diff-filter=D','-z')
files=blobs('',changed-{MAP})
for p in J.rglob('*'):
 path=p.relative_to(R).as_posix()
 if p.is_file() and path in files:assert files[path]==[p.stat().st_size,sha(p.read_bytes())],path
for name in ['ALL_ITEMS_V40.original.json','all_items_V40.original.html','BOUNDARY_V40.original.json']:
 p=L/name;path=p.relative_to(R).as_posix();assert files[path]==[p.stat().st_size,sha(p.read_bytes())]
oldraw=git('show','HEAD:'+PRIOR);old=json.loads(oldraw);refs=(set(old['files'])|set(old['unchanged_required_files'])|{PRIOR})-set(files)-{MAP}
for q in register['items']:
 refs.add(q['image_path']);refs.add(q['path']);refs.update(x.split('#')[0] for x in q['original_reports'])
refs.update(x['path'] for x in register.get('review_resources',[]));refs-=set(files);refs.discard(MAP)
assert not any(x.startswith(('.secrets/','.git/','.codex/','.claude/')) for x in refs)
unchanged=blobs('HEAD',refs);formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=[],qualification='Two explicit non-runtime inherited painted fossil fracture renderers, same original raster/UVs/input/mechanics/save/progress/callbacks. All868 consecutive frames(864fossil+4nextinvitation),116 selected native canvases,94 boards and40 original native details directly reviewed;24 component/action opinions. Exact A1 fixtures preserved before A2 opaque internal contour/snap suppression. A1 fragments4.4 rejected;A2 fragments/join4.5 provisional,whole3.6. Current production fossil3.2/pan3.4/contact2.7/room2.8 and rooted geode repair unchanged. V41 appends only candidate history to1821 items;counts/current source/mounted/action opinions unchanged,377 source reviews outstanding. All783 production literal files unchanged. Full prior T18803 anonymous byte journal durably preserved in10 lossless bounded parts. Exact prior hosted snapshot and both temporary browser QA screenshots preserved; no persistence/status acceptance. Both attempts six fresh parser/inference/officialGodot4.7.2 analyzer/capture checks pass, existing authority/coverage/52document tests/2D no-regression pass, strict-zero2D unsatisfied. Preflight/report helper errors and corrections/thumbnail pixel differences preserved without waiver. Publication is separate from current-action/complete all-job/device/child/owner/finding lifecycle/integration/release acceptance. No new source imagegen upload, bitmap editing, protected original, runtime, security/workflow/gate change or rejected approval retry.')
write(R/MAP,m,compact=True);assert (R/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP)
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
seal=dict(status='EXACT_SCOPED_GEOLOGY_U_BLOBS_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],unchanged_required_files=len(unchanged),checked_utc=now())
out=R/'tmp/geology_review_u_sealed_v473.json';assert not out.exists();write(out,seal);print(json.dumps(seal),flush=True)
