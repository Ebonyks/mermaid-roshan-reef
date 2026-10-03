from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, time

R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
B='72a15c1c49456e37d81c733b8dd6ef4cdc736a45'
BR='codex/job-art-review-v2-20261001'
P=R/'audit/job_qa_scan_v2_20261002'
S=R/'assets_src/imagegen/nursery_scrub_attention_fresh_v1_20261002'
M=R/'assets_src/local_motion/nursery_connected_scrub_v2_20261002'
MAP='audit/job_review_v2_20261001/SCANNABLE_QA_AND_FRESH_NURSERY_SUPPLEMENT_FILES_V15.json'
PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
IMPACTS=[R/'design/audit_impacts'/x for x in ('job-qa-scanability-20261002.json','job-nursery-fresh-attention-20261002.json','job-nursery-scrub-a2-20261002.json')]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*a,data=None):return subprocess.run(['git',*a],cwd=R,input=data,capture_output=True,check=True).stdout
def rp(p):return p.relative_to(R).as_posix()
def boundary():
 rows=read(R/'audit/job_geode_current_recheck_v1_20261002/SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(rows)==783
 checks=[dict(path=x['path'],sha256=sha((R/x['path']).read_bytes()),matches=sha((R/x['path']).read_bytes())==x['sha256']) for x in rows]
 assert all(x['matches'] for x in checks)
 return dict(status='ALL783_LITERAL_SOURCE_BYTES_UNCHANGED',checked_utc=now(),members=checks)
def blobs(ref,paths):
 values={};proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for path in paths:
  proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush();h=proc.stdout.readline().split();assert len(h)==3 and h[1]==b'blob',path
  n=int(h[2]);raw=proc.stdout.read(n);assert len(raw)==n and proc.stdout.read(1)==b'\n';values[path]=[n,sha(raw)]
 proc.stdin.close();assert proc.wait(timeout=30)==0
 return values
def stage():
 removed=set(read(P/'REPLACED_PATHS.json')['paths']);scope=set()
 for impact,packet in zip(IMPACTS,(P,S,M)):
  d=read(impact);assert d['baseline']==B
  files=set(d['files'])|{rp(x) for x in packet.rglob('*') if x.is_file()}
  if packet==P:files.add(MAP)
  d['files']=sorted(files);write(impact,d);scope|=files|{rp(impact)}
 already={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert already<=scope,already-scope
 present=scope-removed
 for path in present:
  resolved=(R/path).resolve();assert resolved.is_relative_to(R.resolve()) and resolved.is_file(),path
  assert not path.startswith(('.git/','.secrets/','.github/','.codex/','.claude/','scripts/','assets/')),path
 git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=b''.join(x.encode()+b'\0' for x in sorted(present)))
 changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope
 assert {x.decode() for x in git('diff','--cached','--name-only','--diff-filter=D','-z').split(b'\0') if x}==removed
 return changed,removed

assert git('rev-parse','HEAD').decode().strip()==B
assert git('branch','--show-current').decode().strip()==BR
action=sys.argv[1]
if action=='prepare':
 dest=P/'review_tools'/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
 shutil.copyfile('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/BROWSER_FRESH_SOURCE_V411.png',S/'BROWSER_SOURCE_REVIEW_V411.png')
 write(S/'BROWSER_REVIEW_V411.json',dict(status='PASS_ACTUAL_LOCAL_REVIEW_PAGE',checked_utc=now(),source_tab=45,url='http://127.0.0.1:8880/'+rp(S/'index.html'),native_images=[dict(path='attempt01/native.png',complete=True,width=1230,height=1278),dict(path='attempt02/native.png',complete=True,width=1230,height=1278)],library_tab=42,library_query='FRESH-NUR',review_lane='All known items',matched_individual_entries=24,component_opinions=22,screenshot=rp(S/'BROWSER_SOURCE_REVIEW_V411.png'),screenshot_sha256=sha((S/'BROWSER_SOURCE_REVIEW_V411.png').read_bytes()),qualification='Temporary read-only preview. No deliverable/handoff status mark; explicit pending browser persistence permission untouched. Source only; no mounted/action/owner acceptance.'))
 note='Fresh Nursery source and motion continuation (2026-10-02): [both fresh text-only paintings and22 individual component opinions](../assets_src/imagegen/nursery_scrub_attention_fresh_v1_20261002/index.html) preserve A1 source4.1 continuity rejection and A2 unbound still4.5/gaze-style4.6/palm4.5 provisional. No existing reference uploaded. [All41 local prompt-only A2 native frames](../assets_src/local_motion/nursery_connected_scrub_v2_20261002/index.html) directly inspected on3 complete boards and12 full-native details: action3.0/reciprocal2.8/attention3.1 rejected. Current game wash3.9/attention3.8 and all783 production source bytes unchanged. Known V36 register1802 entries/1263 source files/328 pose cells/85 runtime use-action/126 source regions;706 inclusive source priorities/23 current Geologist/10 Nursery priorities/385 source reviews required. Pending original-image upload and browser status approval remain separate; no runtime/mounted/cinematic/device/child/owner/all-job/integration/release acceptance or finding lifecycle closure.'
 master=R/'audit/MASTER_AUDIT_2026-08-09.md';raw=master.read_text(encoding='utf-8');assert note not in raw
 raw=raw.replace('## 0. Planning entry\n','## 0. Planning entry\n\n'+note+'\n',1).replace('### Development task index\n','### Development task index\n\n'+note+'\n',1)
 master.write_text(raw,encoding='utf-8',newline='\n')
 findings=R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';raw=findings.read_text(encoding='utf-8');assert 'Fresh Nursery A2 source/reference continuation (2026-10-02)' not in raw
 raw+='\nFresh Nursery A2 source/reference continuation (2026-10-02): [two fresh paintings/all22 component opinions](../../assets_src/imagegen/nursery_scrub_attention_fresh_v1_20261002/index.html) retain A1 rejected4.1 and A2 unbound static4.5/gaze-style4.6/palm4.5. [Prompt-only local A2](../../assets_src/local_motion/nursery_connected_scrub_v2_20261002/index.html) is rejected action3.0 after all41 native frames on3 complete boards and12 full-native details; reciprocal2.8/attention3.1. Current Nursery wash3.9/attention3.8, current Geologist and all783 source bytes unchanged. MA-VIS-006/MA-PLAY-004/MA-OPERA-012 retain existing lifecycle states. No reference-upload authorization, runtime/action/cinematic/device/child/owner/all-job/integration/release acceptance.\n'
 findings.write_text(raw,encoding='utf-8',newline='\n')
 for impact in IMPACTS:
  d=read(impact)
  if impact==IMPACTS[1]:
   d['files']=sorted(set(d['files'])|{rp(master),rp(findings)})
   d['validation']=[v for v in d['validation'] if v['result']!='PENDING']
   d['validation'].append(dict(command='Fresh text-only native A2 directly inspected, all11 individual component reviews',result='PASS',evidence=rp(S/'attempt02/SOURCE_REVIEW.json')+'; provisional unbound still4.5 only'))
   d['acceptance_gaps']='Both new source originals and all22 opinions preserved. A1 rejected4.1; A2 unbound static4.5/gaze-style4.6/palm4.5. Whole-canvas padding, coherent transitions, actual mounting/action/ordinary route, target-device, child, owner and complete all-job acceptance remain open. Blocked original reference upload has not occurred; no authority transfer from new still to current game.'
  if impact==IMPACTS[2]:
   d['validation']=[v for v in d['validation'] if v['result']!='PENDING']
   for v in d['validation']:
    v['evidence']=v['evidence'].replace('every41 visual review pending.','All41 visual reviews completed independently; action3.0 rejected.')
   d['acceptance_gaps']='Every41 native frame directly reviewed; reference action3.0 rejected/reciprocal2.8/attention3.1, all failures retained. Existing source and current game wash3.9/attention3.8 unchanged. Local motion is non-runtime reference and does not satisfy full-frame cinematic delivery. New fresh source is separate and unbound. Actual complete action/ordinary route/device/child/owner/all-job/integration/release and both pending explicit approvals remain open.'
  write(impact,d)
 write(P/'BOUNDARY_UNCHANGED.json',boundary())
 write(R/MAP,dict(status='PREPARING_SCANNABLE_SOURCE_REVIEW_MAP',base_revision=B))
 # Ensure all upcoming log and receipt paths exist before coverage is checked.
 for label in ('game2d','authority','development','document_tests'):
  (P/'gates').mkdir(exist_ok=True)
  for ext in ('stdout.log','stderr.log'):(P/'gates'/(label+'_v1.'+ext)).touch(exist_ok=False)
  write(P/'gates'/(label+'_v1.receipt.json'),dict(status='PENDING'))
 stage();print('PREPARED_SCOPED_R|fresh stills22 opinions|all41 failed motion frames|428 flat files|bounded complete journals|783 sources unchanged')
 raise SystemExit(0)

commands={'game2d':[PY,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'],'authority':[PY,'-X','utf8','-B','tools/audit_document_authority.py'],'development':[PY,'-X','utf8','-B','tools/audit_development.py','--base','auto'],'document_tests':[PY,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']}
if action in commands:
 label=action+'_v1';receipt=P/'gates'/(label+'.receipt.json');assert read(receipt)['status']=='PENDING'
 stage();start=now();tick=time.monotonic();out=P/'gates'/(label+'.stdout.log');err=P/'gates'/(label+'.stderr.log')
 with out.open('wb') as o,err.open('wb') as e:proc=subprocess.run(commands[action],cwd=R,stdout=o,stderr=e,timeout=1200,creationflags=subprocess.CREATE_NO_WINDOW)
 write(receipt,dict(status='PASS' if proc.returncode==0 else 'FAIL_PRESERVED',command=commands[action],process_exit=proc.returncode,started_utc=start,finished_utc=now(),elapsed_seconds=time.monotonic()-tick,stdout_sha256=sha(out.read_bytes()),stderr_sha256=sha(err.read_bytes()),qualification='Unchanged existing gate; no machine-to-visual/current-action/strict2D/owner acceptance transfer.'))
 d=read(IMPACTS[0]);d['validation'].append(dict(command=' '.join(commands[action]),result='PASS' if proc.returncode==0 else 'FAIL',evidence=rp(receipt)));write(IMPACTS[0],d);stage()
 print(label,proc.returncode)
 print((out.read_text(errors='replace')+err.read_text(errors='replace'))[-3000:])
 raise SystemExit(proc.returncode)

assert action=='seal'
for label in commands:assert read(P/'gates'/(label+'_v1.receipt.json'))['status']=='PASS',label
write(P/'BOUNDARY_UNCHANGED.json',boundary())
# Recheck literal flattened caches and exact reconstructed full journals.
cache=read(P/'CACHE_MANIFEST.json');assert len(cache['members'])==428
for x in cache['members']:
 raw=(R/x['current_path']).read_bytes();assert [len(raw),sha(raw)]==[x['bytes'],x['sha256']]
for j in read(P/'JOURNAL_MANIFEST.json')['journals']:
 parts=[]
 for x in j['chunks']:
  raw=(R/x['path']).read_bytes();assert len(raw)<=1000000 and [len(raw),sha(raw)]==[x['bytes'],x['sha256']];parts.append(raw)
 raw=b''.join(parts);assert [len(raw),sha(raw)]==[j['original_bytes'],j['original_sha256']]
lengths=sorted((len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+x.decode()),x.decode()) for x in git('ls-files','-z').split(b'\0') if x)
assert lengths[-1][0]<260
write(P/'INDEX_PATH_LENGTH_CHECK.json',dict(status='PASS_CONSERVATIVE_WINDOWS_PATH_LENGTH',max_absolute_characters=lengths[-1][0],longest_members=lengths[-12:],qualification='Current full tracked inventory; fresh hosted checkout still independently required.'))
d=read(IMPACTS[0]);d['validation']=[v for v in d['validation'] if v['result']!='PENDING'];d['validation'] += [dict(command='All428 flat cache files and all3 whole journal reconstructions exact SHA256',result='PASS',evidence=rp(P/'CACHE_MANIFEST.json')+'; '+rp(P/'JOURNAL_MANIFEST.json')),dict(command='All783 frozen literal sources unchanged',result='PASS',evidence=rp(P/'BOUNDARY_UNCHANGED.json')),dict(command='Hosted Q exact jobs',result='FAIL',evidence=rp(P/'HOSTED_Q_COMPLETED.json')),dict(command='Fresh corrected hosted suite',result='PENDING',evidence='Pending next exact published revision; red Q blocks integration')];write(IMPACTS[0],d)
changed,removed=stage();files=blobs('',sorted(changed-{MAP}-removed))
prior='audit/job_review_v2_20261001/PORTABLE_JOB_QA_SUPPLEMENT_FILES_V14.json';old=read(R/prior)
refs=(set(old['files'])|set(old['unchanged_required_files'])|{prior})-set(files)-removed-{MAP}
unchanged=blobs('HEAD',sorted(refs));formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=B,prior_closed_map=prior,prior_closed_map_sha256=sha(git('show','HEAD:'+prior)),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=sorted(removed),archived_prior_paths_manifests=[rp(P/'CACHE_MANIFEST.json'),rp(P/'JOURNAL_MANIFEST.json')],qualification='Current checkpoint replaces only3 oversized QA files by428 exact short flat originals and newline-boundary journal chunks. Old immutable V12/13/14 maps retain original O/P/Q meaning; original large files remain physically and at immutable Q URLs. All783 production source bytes unchanged; no gate/ceiling/security/workflow change. Adds2 fresh ImageGen text-only originals with22 component opinions and rejected local A2 all41-frame review. Static A2 unbound4.5/gaze-style4.6/palm4.5 never transfers to current wash3.9; motion3.0 rejected. New library1802 entries is known register, not exhaustive all-job acceptance. Local82/82 production verification, unchanged staged gate passes, previous hosted Q failure and future exact hosted suite remain separate. No pending reference upload/browser status action, runtime/cinematic/device/child/owner/integration/release acceptance.')
write(R/MAP,m);git('add','-f','--',MAP);raw=git('show',':'+MAP)
seal=dict(status='EXACT_SCOPED_SCANNABLE_R_BLOBS_SEALED',base_revision=B,map_path=MAP,map_sha256=sha(raw),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],unchanged_required_files=len(unchanged),removed_qa_paths=len(removed),checked_utc=now())
write(R/'tmp/scannable_job_review_r_sealed_v412.json',seal);print(json.dumps(seal))
