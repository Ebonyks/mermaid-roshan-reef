from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
BASE='ea9f4e00a2af67fc6f81e16a2102754892a18cfd';BR='codex/job-art-review-v2-20261001'
P3=R/'assets_src/local_motion/nursery_connected_scrub_v3_20261002'
P4=R/'assets_src/local_motion/nursery_connected_scrub_v4_20261002'
S=R/'audit/day_one_unassigned_sources_v3_20261002'
PACKETS=[P3,P4,S]
IMPACTS=[R/'design/audit_impacts'/x for x in ('job-nursery-scrub-fresh-a3-20261002.json','job-nursery-scrub-prompt-a4-20261002.json','job-unassigned-source-eight-20261002.json')]
MAP='audit/job_review_v2_20261001/NURSERY_MOTION_AND_SOURCE_REVIEW_SUPPLEMENT_FILES_V16.json'
PRIOR='audit/job_review_v2_20261001/SCANNABLE_QA_AND_FRESH_NURSERY_SUPPLEMENT_FILES_V15.json'
PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
rp=lambda p:p.relative_to(R).as_posix()
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*a,data=None):return subprocess.run(['git',*a],cwd=R,input=data,capture_output=True,check=True).stdout
def boundary():
 rows=read(R/'audit/job_geode_current_recheck_v1_20261002/SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(rows)==783
 members=[dict(path=x['path'],sha256=sha((R/x['path']).read_bytes()),matches=sha((R/x['path']).read_bytes())==x['sha256']) for x in rows];assert all(x['matches'] for x in members)
 return dict(status='ALL783_LITERAL_SOURCE_BYTES_UNCHANGED',checked_utc=now(),members=members)
def blobs(ref,paths):
 values={};proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for path in paths:
  proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();assert len(header)==3 and header[1]==b'blob',path
  n=int(header[2]);raw=proc.stdout.read(n);assert len(raw)==n and proc.stdout.read(1)==b'\n';values[path]=[n,sha(raw)]
 proc.stdin.close();assert proc.wait(timeout=30)==0
 return values
def stage():
 scope=set();retired=set(read(R/'audit/job_qa_scan_v2_20261002/REPLACED_PATHS.json')['paths'])
 for impact,packet in zip(IMPACTS,PACKETS):
  d=read(impact);assert d['baseline']==BASE
  files=set(d['files'])|{rp(x) for x in packet.rglob('*') if x.is_file()}
  if packet==P4:files.add(MAP)
  d['files']=sorted(files);write(impact,d);scope|=files|{rp(impact)}
 assert not (scope&retired)
 already={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert already<=scope,already-scope
 for path in scope:
  resolved=(R/path).resolve();assert resolved.is_relative_to(R.resolve()) and resolved.is_file(),path
  assert not path.startswith(('.git/','.secrets/','.github/','.codex/','.claude/','scripts/','assets/')),path
 git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=b''.join(x.encode()+b'\0' for x in sorted(scope)))
 changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope
 assert not git('diff','--cached','--name-only','--diff-filter=D','-z')
 return changed
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()==BR
action=sys.argv[1]
commands={'game2d':[PY,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'],'authority':[PY,'-X','utf8','-B','tools/audit_document_authority.py'],'development':[PY,'-X','utf8','-B','tools/audit_development.py','--base','auto'],'document_tests':[PY,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']}
if action=='prepare':
 dest=P4/'review_tools'/Path(__file__).name;assert not dest.exists();shutil.copyfile(__file__,dest)
 for packet,stem in ((P4,'BROWSER_A4_REVIEW_V427'),(S,'BROWSER_EIGHT_SOURCES_V427')):
  for suffix in ('json','png'):shutil.copyfile('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/'+stem+'.'+suffix,packet/('BROWSER_REVIEW_V427.'+suffix))
  proof=read(packet/'BROWSER_REVIEW_V427.json');assert all(x['complete'] and x['width']>0 for x in proof['images'])
  if packet==P4:assert proof['frames']==41 and proof['articles']==49 and proof['video'][0]['readyState']==4 and proof['video'][0]['width']==896 and proof['video'][0]['height']==512
  else:assert proof['articles']==8 and len(proof['images'])==8
 # Preserve exact literal consumer-table references, qualified as static rather than played job use.
 inv=read(S/'PLAN.json')['inventory'];trace=[]
 for name in ('scripts/dungeon_art.gd','scripts/ember_fortress.gd'):
  path=R/name;lines=path.read_text(encoding='utf-8').splitlines()
  matches=[dict(line=i+1,text=line,source_ids=[x['id'] for x in inv if x['path'] in line]) for i,line in enumerate(lines) if any(x['path'] in line for x in inv)]
  trace.append(dict(script=name,sha256=sha(path.read_bytes()),matches=matches))
 assert {i for file in trace for row in file['matches'] for i in row['source_ids']}=={x['id'] for x in inv}
 write(S/'STATIC_CONSUMER_REFERENCES.json',dict(status='EXPLICIT_DUNGEON_EMBER_TABLE_REFERENCES_RECORDED',checked_utc=now(),members=trace,qualification='All eight exact paths have explicit references in dungeon/Ember rendering tables. This static trace does not establish actual job use, exclude dynamic/shared use, or accept measured 3D migration debt. No non-job source regeneration or runtime replacement is performed. Source opinions stay separate.'))
 raw=(S/'index.html').read_text(encoding='utf-8');raw=raw.replace('</header>','<p><a href="STATIC_CONSUMER_REFERENCES.json">Exact static consumer-table references</a>: all eight paths occur in dungeon/Ember rendering tables. Actual job use and dynamic/shared use remain unverified; no non-job regeneration is performed.</p></header>',1);(S/'index.html').write_text(raw,encoding='utf-8',newline='\n')
 write(P4/'BOUNDARY_UNCHANGED.json',boundary())
 write(R/MAP,dict(status='PREPARING_MOTION_AND_SOURCE_REVIEW_MAP',base_revision=BASE))
 for label in commands:
  (P4/'gates').mkdir(exist_ok=True)
  for suffix in ('stdout.log','stderr.log'):(P4/'gates'/(label+'_v1.'+suffix)).touch(exist_ok=False)
  write(P4/'gates'/(label+'_v1.receipt.json'),dict(status='PENDING'))
 for ip,packet in zip(IMPACTS,PACKETS):
  d=read(ip);d['files']=sorted(set(d['files'])|{rp(x) for x in packet.rglob('*') if x.is_file()});d['validation'].append(dict(command='Actual temporary browser review: complete native artwork loading',result='PASS',evidence=rp(packet/('BROWSER_REVIEW_V421.json' if packet==P3 else 'BROWSER_REVIEW_V427.json'))+'; no deliverable/handoff status mark, pending explicit browser approval untouched.'));write(ip,d)
 stage();print('PREPARED_SCOPED_S|all82 failed native motion frames|eight new native source opinions|783 actual production bytes unchanged')
 raise SystemExit(0)
if action in commands:
 label=action+'_v1';receipt=P4/'gates'/(label+'.receipt.json');assert read(receipt)['status']=='PENDING';stage();start=now();tick=time.monotonic();out=P4/'gates'/(label+'.stdout.log');err=P4/'gates'/(label+'.stderr.log')
 with out.open('wb') as o,err.open('wb') as e:proc=subprocess.run(commands[action],cwd=R,stdout=o,stderr=e,timeout=1800,creationflags=subprocess.CREATE_NO_WINDOW)
 write(receipt,dict(status='PASS' if proc.returncode==0 else 'FAIL_PRESERVED',command=commands[action],process_exit=proc.returncode,started_utc=start,finished_utc=now(),elapsed_seconds=time.monotonic()-tick,stdout_sha256=sha(out.read_bytes()),stderr_sha256=sha(err.read_bytes()),qualification='Unchanged existing machine gate; no machine-to-visual/current-action/strict2D/owner acceptance transfer.'))
 d=read(IMPACTS[1]);d['validation'].append(dict(command=' '.join(commands[action]),result='PASS' if proc.returncode==0 else 'FAIL',evidence=rp(receipt)));write(IMPACTS[1],d);stage();print(label,proc.returncode);print((out.read_text(errors='replace')+err.read_text(errors='replace'))[-2200:]);raise SystemExit(proc.returncode)
assert action=='seal'
for label in commands:assert read(P4/'gates'/(label+'_v1.receipt.json'))['status']=='PASS',label
write(P4/'BOUNDARY_UNCHANGED.json',boundary())
for packet,expected in ((P3,2.7),(P4,3.2)):
 assert read(packet/'REVIEW_STATUS.json')['status']=='MACHINE_RENDER_COMPLETE_VISUAL_REJECTED'
 field='reference_action_score' if packet==P3 else 'whole_reference_action_score'
 assert read(packet/'REVIEW_STATUS.json')[field]==expected
 idx=read(packet/'attempt01/INDEX.json');assert len(idx['frames'])==41
 for row in idx['frames']:assert sha((R/row['path']).read_bytes())==row['sha256']
rv=read(P3/'previous_r_remote_verified/RESULT.json');assert rv['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and rv['revision']==BASE and rv['files_including_manifest']==15802
j=read(P3/'previous_r_remote_verified/JOURNAL_MANIFEST.json');raw=b''.join((R/x['path']).read_bytes() for x in j['chunks']);assert [len(raw),sha(raw)]==[j['original_bytes'],j['original_sha256']] and len(raw.splitlines())==15802
assert read(S/'DIRECT_REVIEW.json')['source_count']==8
reg=read(R/'audit/job_artwork_refinement_live/ALL_ITEMS.json');assert len(reg['items'])==1802 and reg['counts']['unreviewed_current_source']==377 and reg['counts']['inclusive_current_source_priorities']==713
lengths=sorted((len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+x.decode()),x.decode()) for x in git('ls-files','-z').split(b'\0') if x);assert lengths[-1][0]<260
write(P4/'INDEX_PATH_LENGTH_CHECK.json',dict(status='PASS_CONSERVATIVE_WINDOWS_PATH_LENGTH',max_absolute_characters=lengths[-1][0],longest_members=lengths[-8:],qualification='Complete tracked inventory; fresh hosted checkout independent.'))
changed=stage();files=blobs('',sorted(changed-{MAP}));old=read(R/PRIOR)
refs=(set(old['files'])|set(old['unchanged_required_files'])|{PRIOR})-set(files)-{MAP}
unchanged=blobs('HEAD',sorted(refs));formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(git('show','HEAD:'+PRIOR)),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=[],qualification='Preserve every41 native fresh-source A3 and every41 prompt-only A4 frame, eight component/action opinions each; action2.7 and3.2 both rejected. A4 removes large arch but still lacks reciprocal rubbing2.8/material3.4. All original source/input/workflow/seed/settings preserved; no source-to-current-action score transfer. Adds eight previously unassigned whole-native source opinions, seven inclusive priorities/six below4.5; explicit dungeon/Ember table references do not prove actual job use. Register V39 remains1802 entries/713 known source-cell-region priorities/377 source reviews outstanding. All783 actual production literal source bytes unchanged. Complete immutable R15802 anonymous verification receipt/all journal rows preserved as bounded exact reconstruction. Existing machine gates PASS; hosted R and next exact run independently qualified. No protected source/security/workflow/gate change, rejected upload/browser status action, runtime/cinematic/device/child/owner/all-job/integration/release acceptance.')
write(R/MAP,m);git('add','-f','--',MAP);raw=git('show',':'+MAP)
seal=dict(status='EXACT_SCOPED_MOTION_SOURCE_S_BLOBS_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],unchanged_required_files=len(unchanged),checked_utc=now())
write(R/'tmp/nursery_review_s_sealed_v428.json',seal);print(json.dumps(seal))
