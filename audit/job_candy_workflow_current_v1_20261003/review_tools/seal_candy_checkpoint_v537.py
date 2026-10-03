from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');c=b/'audit/job_candy_workflow_current_v1_20261003';k=b/'audit/job_geology_fossil_reveal_continuity_v1_20261003';l=b/'audit/job_artwork_refinement_live'
base='c5977ebb29bb2011b20fc149ad350290f045045c';branch='codex/job-art-review-v2-20261001'
mp='audit/job_review_v2_20261001/CANDY_WRAPPER_AND_FOSSIL_REVEAL_FILES_V19.json';prior='audit/job_review_v2_20261001/GEOLOGY_FRACTURE_TRIAL_SUPPLEMENT_FILES_V18.json'
ip=b/'design/audit_impacts/job-candy-workflow-current-20261003.json';kip=b/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json'
sha=lambda raw:hashlib.sha256(raw).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):
 n=p.with_name(p.name+'.new');n.write_text(json.dumps(d,ensure_ascii=False,**({'separators':(',',':')} if compact else {'indent':2}))+'\n',encoding='utf-8',newline='\n');n.replace(p)
def git(*args,data=None):return subprocess.run(['git',*args],cwd=b,input=data,capture_output=True,check=True).stdout
def blobs(ref,paths):
 values={};proc=subprocess.Popen(['git','cat-file','--batch'],cwd=b,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 try:
  for path in sorted(paths):
   proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush();head=proc.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path
   n=int(head[2]);left=n;h=hashlib.sha256()
   while left:
    raw=proc.stdout.read(min(left,65536));assert raw;left-=len(raw);h.update(raw)
   assert proc.stdout.read(1)==b'\n';values[path]=[n,h.hexdigest()]
  proc.stdin.close();assert proc.wait(timeout=30)==0
 finally:
  if proc.poll() is None:proc.terminate();proc.wait(timeout=30)
 return values
assert git('rev-parse','HEAD').decode().strip()==base and git('branch','--show-current').decode().strip()==branch
target=c/'review_tools'/Path(__file__).name
if Path(__file__).resolve()!=target.resolve():shutil.copyfile(__file__,target)
d=read(ip);d['files']=sorted(set(d['files'])|{target.relative_to(b).as_posix(),mp,(c/'SCOPED_PUBLICATION_BOUNDARY_V537.json').relative_to(b).as_posix(),(c/'INDEX_PATH_LENGTH_V537.json').relative_to(b).as_posix(),(c/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json').relative_to(b).as_posix()});write(ip,d)
if sys.argv[1:]==['--prepare']:print('CANDY_SEALER_PREPARED_NOT_SEALED');sys.exit(0)
assert sys.argv[1:]==['--seal']
for label in ['authority','development','document_tests','game2d']:assert read(b/'audit/job_shared_entrance_sources_v1_20261003/gates_v1'/(label+'.receipt.json'))['status']=='PASS',label
ci=read(c/'full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(r['process_exit']==0 for r in ci['probe_results']) and ci['source_unchanged']
assert len(ci['source_checks'])==783 and all(sha((b/r['path']).read_bytes())==r['before_sha256'] for r in ci['source_checks'])
reg=read(l/'ALL_ITEMS.json');assert len(reg['items'])==2038 and reg['counts']['inclusive_current_source_priorities']==888 and reg['counts']['unique_source_file_priorities']==602 and reg['counts']['unreviewed_current_source']==359
boundary=read(l/'CURRENT_BOUNDARY_REFRESH.json');assert boundary['registered_source_matches']==2038 and boundary['candy_capture_boundary_match'] and not boundary['geode_capture_boundary_match'] and not boundary['nursery_capture_boundary_match']
assert (l/'ALL_ITEMS.json').stat().st_size<4194304
assert read(c/'DIRECT_REVIEW_CURRENT_A3.json')['owner_acceptance'] is None
contact=read(b/'audit/job_candy_wrap_contact_runtime_v1_20261003/DIRECT_REVIEW_A5.json');assert contact['binding_changed'] is False and contact['opinions'][-1]['score']==4.1
assert len(read(b/'assets_src/imagegen/candy_wrap_contact_v1_20261003/COMPLETE_SOURCE_REVIEW.json')['sources'])==10
assert read(b/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
u=read(k/'previous_u_remote_verified/RESULT.json');assert u['revision']==base and u['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and u['files_including_manifest']==20087
ji=read(k/'previous_u_remote_verified/JOURNAL_INDEX.json');raw=b''.join((b/x['path']).read_bytes() for x in ji['ordered_parts']);assert [len(raw),sha(raw)]==[ji['original_bytes'],ji['original_sha256']] and len(raw.splitlines())==20087
source=read(c/'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json')['source_files'];assert len(source)==783
checks=[dict(path=x['path'],sha256=sha((b/x['path']).read_bytes()),matches=sha((b/x['path']).read_bytes())==x['sha256']) for x in source];assert all(x['matches'] for x in checks)
delta=read(c/'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json')['declared_changes_from_U'];assert len(delta)==1 and delta[0]['path']=='scripts/opera_career_world_2d.gd'
write(c/'SCOPED_PUBLICATION_BOUNDARY_V537.json',dict(status='ALL783_CURRENT_CANDY_LITERAL_MEMBERS_MATCH_ONE_DECLARED_BASELINE_CHANGE',checked_utc=now(),members=checks,declared_changes_from_U=delta,qualification='Four birthday station bindings repaired in one shared source. Candy current captured boundary matches; Geologist/Nursery historical mounted claims withheld. New wrapper/contact sources and fossil candidate remain unbound and rejected.'))
families=[c,k,l,b/'audit/job_candy_wrap_contact_runtime_v1_20261003',b/'assets_src/imagegen/candy_wrap_states_v1_20261003',b/'assets_src/imagegen/candy_wrap_contact_v1_20261003']
d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for f in families if f!=k for p in f.rglob('*') if p.is_file()});write(ip,d)
kd=read(kip);kd['files']=sorted(set(kd['files'])|{p.relative_to(b).as_posix() for p in k.rglob('*') if p.is_file()});write(kip,kd)
qip=b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json';qd=read(qip);shared=b/'audit/job_shared_entrance_sources_v1_20261003';qd['files']=sorted(set(qd['files'])|{p.relative_to(b).as_posix() for p in shared.rglob('*') if p.is_file()});write(qip,qd)
assert read(shared/'DIRECT_NATIVE_REVIEW.json')['individual_opinion_count']==122 and read(shared/'DIRECT_NATIVE_REVIEW.json')['source_pixels_modified'] is False
families.append(shared)
scope=set(d['files'])|set(kd['files'])|set(qd['files'])|{ip.relative_to(b).as_posix(),kip.relative_to(b).as_posix(),qip.relative_to(b).as_posix()}
retired=set(read(b/'audit/job_qa_scan_v2_20261002/REPLACED_PATHS.json')['paths']);assert not scope&retired
staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=scope,staged-scope
tracked={x.decode() for x in git('ls-files','-z').split(b'\0') if x}
lengths=sorted((len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+x),x) for x in tracked|scope);assert lengths[-1][0]<260
write(c/'INDEX_PATH_LENGTH_V537.json',dict(status='PASS_CONSERVATIVE_WINDOWS_PATH_LENGTH',max_absolute_characters=lengths[-1][0],longest_members=lengths[-8:],qualification='No checkout/security/workflow relaxation.'))
pending_bridge=(c/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json').relative_to(b).as_posix()
# This file is generated from the staged tested sources below, then separately staged and verified.
for path in scope-{mp,pending_bridge}:
 p=(b/path).resolve();assert p.is_relative_to(b.resolve()) and p.is_file(),path
 assert not path.startswith(('.git/','.secrets/','.codex/','.claude/','.github/','assets/')),path
 assert not path.startswith('scripts/') or path=='scripts/opera_career_world_2d.gd',path
paths=b''.join(p.encode()+b'\0' for p in sorted(scope-{mp,pending_bridge}));git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths);git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths)
# Prove the literal tested source against every staged/current revision member.
revision_paths={x['path'] for x in source if x['path'] in tracked};aux=[x for x in source if x['path'] not in tracked];assert len(revision_paths)==543 and len(aux)==240 and all(x['path'].endswith('.gd.uid') for x in aux)
blobvals=blobs('',revision_paths);bridge=[]
for x in source:
 p=x['path'];literal=(b/p).read_bytes()
 if p in revision_paths:
  raw=git('show',':'+p);exact=raw==literal;normalized=False
  if not exact:
   assert Path(p).suffix in {'.gd','.tscn','.tres','.godot','.import','.uid'} or p=='scripts/ci.sh',p
   literal.decode('utf-8');raw.decode('utf-8');normalized=raw==literal.replace(b'\r\n',b'\n');assert normalized,p
  assert [len(raw),sha(raw)]==blobvals[p];bridge.append(dict(path=p,literal_sha256=sha(literal),publication_sha256=sha(raw),exact_bytes=exact,whole_text_crlf_to_lf_only=normalized,role='revision_source_member'))
 else:bridge.append(dict(path=p,literal_sha256=sha(literal),role='auxiliary_generated_uid_not_published'))
write(c/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json',dict(status='PASS_ALL783_PUBLICATION_BOUNDARY_MEMBERS',revision_source_members=543,auxiliary_generated_uid_members=240,members=bridge,qualification='Exact native bitmap bytes. Text-only whole-file newline normalization explicitly proved against frozen tested literals. Generated untracked UIDs remain auxiliary, not falsely claimed as published.'))
git('add','-f','--',str((c/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json').relative_to(b)))
changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope and not git('diff','--cached','--name-only','--diff-filter=D','-z')
assert {x for x in changed if x.startswith('scripts/')}=={'scripts/opera_career_world_2d.gd'}
files=blobs('',changed-{mp})
for f in families:
 for p in f.rglob('*'):
  path=p.relative_to(b).as_posix()
  if p.is_file() and path in files:assert files[path]==[p.stat().st_size,sha(p.read_bytes())],path
oldraw=git('show','HEAD:'+prior);old=json.loads(oldraw);refs=(set(old['files'])|set(old['unchanged_required_files'])|{prior})-set(files)-{mp}
for q in reg['items']:refs.add(q['image_path']);refs.add(q['path']);refs.update(x.split('#')[0] for x in q['original_reports'])
refs.update(x['path'] for x in reg.get('review_resources',[]));refs-=set(files);refs.discard(mp)
assert not any(x.startswith(('.secrets/','.git/','.codex/','.claude/')) for x in refs)
unchanged=blobs('HEAD',refs);formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
manifest=dict(schema='reef.immutable-review-supplement.v1',base_revision=base,prior_closed_map=prior,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=[],qualification='Current Candy actual Kitchen training and birthday review:626 wrapping/glaze canvases,64 selected views,66 boards,12 native details and48 individual opinions. Exactly one production source repairs four absent birthday station bindings with existing invitation art; no new wrapper/contact art bound. Current WRAP2.8/GLAZE2.6 and birthday wrong-tier/duplicate berries/cake occlusion remain weak. Separate unbound inherited actual-input connected study:412 canvases,32 views,42 boards,22 native details,13 opinions; endpoints4.5-4.6,whole4.1 rejected. Three wrapper and ten contact natives preserve all prompts/references/hashes;52 source states separately scored. Latest bridgesA8/A9/A10 whole4.1/4.1/4.2 rejected. V45 known2038 entries,888 source/cell/region priorities,602 unique source priorities,48 current Candy priorities,359 source reviews outstanding. Shared Kitchen/Opera entrance source-only review directly inspects18 unchanged natives and104 authored prop cells:122 individual opinions,17 source/99 cell inclusive priorities. Current V2/V4 manifests match all13 atlases; two old ownership hashes retained as stale. No source pixel or production changes from this extra review. Current Candy783-source boundary matches; older Geologist/Nursery mounted claims withheld after shared-source delta. Separate fossil reveal/home trial437 frames/58 views/48 boards/20 native details/13 opinions remains unbound whole3.8. Complete previous U20087 anonymous byte journal and exact hosted SUCCESS retained. Fresh official4.7.2 unmodified full suite82/82 process0 and all783 frozen literal source hashes verified; exact staged publication newline bridge543 revision members/240 auxiliary generated UIDs. Raw diagnostics, failed fixtures/window change, source/registry/report-helper failures and originals preserved. Temporary browser report QA/search/playback screenshots only, no persistence/status claim. No protected art, new 3D, security/workflow/gate changes, rejected approval retry, finding lifecycle closure, owner/device/child/all-job/integration/release acceptance.')
write(b/mp,manifest,compact=True);assert (b/mp).stat().st_size<4194304;git('add','-f','--',mp);raw=git('show',':'+mp)
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{mp}
seal=dict(status='EXACT_SCOPED_CANDY_V_BLOBS_SEALED',base_revision=base,map_path=mp,map_sha256=sha(raw),payload_sha256=manifest['payload_sha256'],payload_files=len(files),payload_bytes=manifest['required_payload_bytes'],unchanged_required_files=len(unchanged),map_bytes=len(raw),checked_utc=now())
out=b/'tmp/candy_review_v_sealed_v537.json';assert not out.exists();write(out,seal);print(json.dumps(seal),flush=True)
