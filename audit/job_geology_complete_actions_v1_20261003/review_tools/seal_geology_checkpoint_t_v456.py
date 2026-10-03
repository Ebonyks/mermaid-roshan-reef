from pathlib import Path
import json,hashlib,datetime,subprocess,shutil,sys
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_geology_complete_actions_v1_20261003';P=R/'audit/job_geology_painted_invitation_fit_v1_20261003';T=R/'assets_src/imagegen/geologist_specimen_tray_v1_20261003';L=R/'audit/job_artwork_refinement_live'
BASE='1652a9bb33af0d11a594b5996df66d2266c02d39';BR='codex/job-art-review-v2-20261001';MAP='audit/job_review_v2_20261001/GEOLOGY_COMPLETE_ACTION_AND_TRAY_SUPPLEMENT_FILES_V17.json';PRIOR='audit/job_review_v2_20261001/NURSERY_MOTION_AND_SOURCE_REVIEW_SUPPLEMENT_FILES_V16.json'
IMPACTS=[R/'design/audit_impacts'/x for x in ['job-geology-complete-action-register-20261003.json','job-geology-complete-actions-20261003.json','job-geology-painted-invitation-fit-20261003.json','job-geology-specimen-tray-20261003.json']]
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
target=F/'review_tools'/Path(__file__).name
if Path(__file__).resolve()!=target.resolve():shutil.copyfile(Path(__file__),target)
d=read(IMPACTS[0]);d['files']=sorted(set(d['files'])|{target.relative_to(R).as_posix(),(F/'review_tools/make_geology_publisher_t_v455.py').relative_to(R).as_posix()});write(IMPACTS[0],d)
if '--prepare' in sys.argv:print('T_SEALER_PREPARED_NOT_STAGED');raise SystemExit(0)
for label in ['authority','development','document_tests','game2d_compact_v2']:assert read(F/'gates'/(label+'.receipt.json'))['status']=='PASS',label
cr=read(F/'DIRECT_REVIEW.json');assert cr['consecutive_frames']==884 and len(cr['views'])==58 and len(cr['individual_objects'])==22 and all(x['direct_review'] for x in cr['frames']+cr['views'])
for x in cr['frames']+cr['views']:assert sha((R/x['path']).read_bytes())==x['sha256']
for n in [1,2,3]:
 d=read(P/f'DIRECT_REVIEW_ATTEMPT0{n}.json');assert d['selected_views']==58 and d['owner_acceptance'] is None
 assert len(read(P/('QA_BOARD_MANIFEST.json' if n==1 else f'QA_BOARD_MANIFEST_A{n}.json'))['boards'])==10
assert read(P/'DIRECT_REVIEW_ATTEMPT03.json')['whole_fit_score']==4.2
assert sha((T/'attempt01/native.png').read_bytes())=='6d91458161f5d234354293c1836fe26b07306377916cd18ec59e785fd76a5cbb'
assert read(T/'attempt01/DIRECT_SOURCE_REVIEW.json')['runtime_binding'] is False
register=read(L/'ALL_ITEMS.json');assert len(register['items'])==1821 and register['counts']['unique_source_file_priorities']==572 and register['counts']['unreviewed_current_source']==377
assert (L/'ALL_ITEMS.json').stat().st_size<4194304
assert read(R/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
oldreceipt=read(F/'previous_s_remote_verified/RESULT.json');assert oldreceipt['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and oldreceipt['revision']==BASE and oldreceipt['files_including_manifest']==16023
j=read(F/'previous_s_remote_verified/JOURNAL_INDEX.json');raw=b''.join((R/x['path']).read_bytes() for x in j['parts']);assert [len(raw),sha(raw)]==[j['literal_original_bytes'],j['literal_original_sha256']] and len(raw.splitlines())==16023
assert read(F/'previous_s_remote_verified/HOSTED_S_VERIFICATION.json')['status']=='EXACT_S_HOSTED_SUCCESS'
source=read(F/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(source)==783
checks=[dict(path=x['path'],sha256=sha((R/x['path']).read_bytes()),matches=sha((R/x['path']).read_bytes())==x['sha256']) for x in source];assert all(x['matches'] for x in checks)
write(F/'SCOPED_PUBLICATION_BOUNDARY_T.json',dict(status='ALL783_LITERAL_PRODUCTION_MEMBERS_UNCHANGED',checked_utc=now(),members=checks,qualification='Current complete actual capture boundary; no source/art/gameplay changes. Existing82/82 local and exact S hosted remain independent machine evidence; graphics/actions/device/child/owner and all-job completion remain open.'))
scope=set()
for packet,impact in [(F,IMPACTS[1]),(P,IMPACTS[2]),(T,IMPACTS[3])]:
 d=read(impact);assert d['baseline']==BASE;d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in packet.rglob('*') if x.is_file()});write(impact,d)
for impact in IMPACTS:scope|=set(read(impact)['files'])|{impact.relative_to(R).as_posix()}
retired=set(read(R/'audit/job_qa_scan_v2_20261002/REPLACED_PATHS.json')['paths']);assert not scope&retired
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=scope,staged-scope
# The path-length record is written before staging its already-covered exact path.
tracked=[x.decode() for x in git('ls-files','-z').split(b'\0') if x]
lengths=sorted((len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+x),x) for x in set(tracked)|scope);assert lengths[-1][0]<260
write(F/'INDEX_PATH_LENGTH_CHECK_T.json',dict(status='PASS_CONSERVATIVE_WINDOWS_PATH_LENGTH',max_absolute_characters=lengths[-1][0],longest_members=lengths[-8:],qualification='Existing tracked and exact new scoped paths. No Windows checkout contract relaxation.'))
for path in scope:
 p=(R/path).resolve();assert p.is_relative_to(R.resolve()) and p.is_file(),path
 assert not path.startswith(('.git/','.secrets/','.codex/','.claude/','.github/','scripts/','assets/')),path
paths=b''.join(x.encode()+b'\0' for x in sorted(scope));git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths)
git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths)
changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope and not git('diff','--cached','--name-only','--diff-filter=D','-z')
files=blobs('',changed-{MAP})
for packet in [F,P,T]:
 for p in packet.rglob('*'):
  path=p.relative_to(R).as_posix()
  if p.is_file() and path in files:assert files[path]==[p.stat().st_size,sha(p.read_bytes())],path
oldraw=git('show','HEAD:'+PRIOR);old=json.loads(oldraw);refs=(set(old['files'])|set(old['unchanged_required_files'])|{PRIOR})-set(files)-{MAP}
for q in register['items']:
 refs.add(q['image_path']);refs.add(q['path']);refs.update(x.split('#')[0] for x in q['original_reports'])
refs.update(x['path'] for x in register.get('review_resources',[]));refs-=set(files);refs.discard(MAP)
assert not any(x.startswith(('.secrets/','.git/','.codex/','.claude/')) for x in refs)
unchanged=blobs('HEAD',refs);formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=[],qualification='Complete actual fossil/pan review: all884 consecutive frames,58 selected canvases,85 boards/34 full native details/22 individually scored objects/actions. Fossil3.2/pan3.4/contact2.7 remain weak; rooted geode correction unchanged. One fresh text-only tray source4.6, six source opinions; three separately reviewed58-view counterfactual placements with eight full native invitation details each. A1 whole3.5 rejected/A2 support3.8 whole4.0/A3 selected materials-scale-clearance4.5 provisional but whole room4.2 belowfloor. Current production unchanged and source/counterfactual action acceptance separate. Register1821 entries/713 source-cell-region priorities/572 unique source-file priorities/38 current Geologist/10 Nursery/377 source reviews outstanding; exact V39 history and every failed capture/layout/gate preserved. Current JSON whitespace compacted with all1821 structured objects equal after unchanged4MiB budget failure; exact failed preformat bytes reconstructed by bounded shards. Complete S16023 anonymous byte verification and exact hosted success retained. All783 production literal members unchanged; existing783 local CI/543 revision-source/240 generated UID publication bounds remain separate. Existing authority/coverage/document tests and corrected2D no-regression checks pass; strict-zero2D/graphics/complete actions/device/child/owner/all-job/finding closure/integration/release remain open. No protected original,security/workflow/gate change,forbidden upload/browser-status action or owner approval.')
write(R/MAP,m,compact=True);assert (R/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP)
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
seal=dict(status='EXACT_SCOPED_GEOLOGY_T_BLOBS_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],unchanged_required_files=len(unchanged),checked_utc=now())
out=R/'tmp/geology_review_t_sealed_v456.json';assert not out.exists();write(out,seal);print(json.dumps(seal),flush=True)
