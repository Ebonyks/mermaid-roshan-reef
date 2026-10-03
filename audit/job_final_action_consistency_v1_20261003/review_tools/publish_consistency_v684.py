from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, sys, urllib.request
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
BASE='6c5c1bd4a0951964a08043e72ae6472d2d402a9e';BRANCH='codex/job-art-review-v2-20261001'
REL='audit/job_final_action_consistency_v1_20261003';P=B/REL;IP=B/'design/audit_impacts/job-final-action-consistency-20261003.json'
MAP='audit/job_review_v2_20261001/JOB_FINAL_ACTION_CONSISTENCY_FILES_V29.json';V=B/'tmp/consistency_publish_v684';PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
V.mkdir(parents=True,exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda raw:hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 target=p.with_name(p.name+'.v684_next')
 target.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
 target.replace(p)
def git(*args):
 r=subprocess.run(['git',*args],cwd=B,capture_output=True,check=True);return r.stdout
def run(label,args):
 r=subprocess.run(args,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 (V/(label+'.stdout.log')).write_bytes(r.stdout);(V/(label+'.stderr.log')).write_bytes(r.stderr)
 print(label,r.returncode,flush=True);assert r.returncode==0,(label,r.stderr.decode(errors='replace')[-1000:])
 return r
def facts():
 c=read(P/'PHASE_COVERAGE.json');assert c['counts']['planned_rows']==115
 assert len(c['rows'])==115 and all(r['runtime_final_action_acceptance'] is None for r in c['rows'])
 contract=read(P/'PRESENTATION_CONTRACT.json');assert contract==read(B/'design/animation/JOB_FINAL_ACTION_PRESENTATION_V1.json')
 assert contract['implementation']['runtime_changed'] is False and contract['resolution']['background_native_minimum_per_playable_screen']==[2048,2048]
 for r in read(P/'REGISTER_BOUNDARY_BEFORE.json')['files']:assert sha((B/r['path']).read_bytes())==r['sha256']
 for r in read(P/'PRODUCTION_BOUNDARY.json')['members']:assert sha((B/r['path']).read_bytes())==r['sha256']
 for label in ['authority','development','document_tests','game2d','register_parts']:
  assert read(P/'gates_v1'/(label+'.receipt.json'))['exit_code']==0,label
 for r in read(P/'gates_v1/CANDIDATE_SOURCE.json')['members']:assert sha((B/r['path']).read_bytes())==r['sha256'],r['path']
 return c,contract
if sys.argv[1]=='prepare':
 assert git('rev-parse','HEAD').decode().strip()==BASE
 staged_before=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
 allowed_before=set(read(IP)['files'])|{IP.relative_to(B).as_posix()}
 assert staged_before.issubset(allowed_before),staged_before-allowed_before
 c,contract=facts();attrs=B/'.gitattributes';raw=attrs.read_bytes();rule=b'\naudit/job_final_action_consistency_v1_20261003/** -text\n'
 if rule.strip() not in raw:attrs.write_bytes(raw+rule)
 copy=P/'review_tools'/Path(__file__).name;copy.write_bytes(Path(__file__).read_bytes())
 authority=[]
 for name in ['audit/MASTER_AUDIT_2026-08-09.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/AUDIT_DEVELOPMENT_CONTRACT.md','design/animation/ANIMATION_PRODUCTION_PROTOCOL.md']:
  data=(B/name).read_bytes();authority.append(dict(path=name,sha256=sha(data),bytes=len(data)))
 put(P/'AUTHORITY_REVIEW.json',dict(checked_utc=now(),rules=read(IP)['rules'],findings=['MA-VIS-006','MA-PLAY-004'],members=authority,qualification='Owner direction recorded; no lifecycle closure, native-resolution/motion/runtime/device/child/owner acceptance.'))
 imp=read(IP);imp['validation']=[x for x in imp['validation'] if x['command']!='Source-derived coverage, browser proof and document gates']
 imp['validation'].append(dict(command='Five exact-source structural/document/register/no-regression gates',result='PASS',evidence=REL+'/gates_v1;52 document tests,6/6 stress,9 register tests;strict2D remains UNSATISFIED.'))
 imp['files']=sorted(set(imp['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()}|{'.gitattributes',MAP})
 put(IP,imp)
 payload=sorted(set(imp['files'])-{MAP}|{IP.relative_to(B).as_posix()})
 dependencies=set()
 for r in read(P/'RESOLUTION_REUSE_INVENTORY.json')['inspected_sources']:dependencies.add(r['path'])
 for r in read(P/'ILLUSTRATION_REFERENCES.json')['images']:dependencies.add(r['path'])
 for r in read(P/'PHASE_COVERAGE.json')['source_records']:dependencies.add(r['path'])
 for r in authority:dependencies.add(r['path'])
 for name in ['scripts/opera_world_backdrop_2d.gd','scripts/opera_gesture_surface.gd','scripts/opera_roshan_actor.gd','scripts/comfy_games.gd','project.godot','ASSET_LICENSES.md','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/ATLAS_STATE_ITEMS_V51.json','audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json','audit/job_review_v2_20261001/CANDY_TRANSITION_KEY_FILES_V28.json']:
  dependencies.add(name)
 dependencies-=set(payload)|{MAP}
 # This is a scoped operational packet. The older complete illustrated library
 # is a separately closed, immutable reference verified at BASE, not a new handoff.
 # These exact owned audit paths are ignored by the review-folder default.
 # Force-add only the declared packet, preserving raw evidence as required.
 git('add','-f','--',*payload)
 files={}
 for name in payload:
  data=git('show',':'+name);assert data==(B/name).read_bytes(),name
  files[name]=dict(bytes=len(data),sha256=sha(data),role='CHANGED_REVIEW_PAYLOAD')
 for name in sorted(dependencies):
  assert git('ls-files','--error-unmatch',name)
  data=git('show','HEAD:'+name)
  local=(B/name).read_bytes();bridge='LITERAL_MATCH' if data==local else 'WHOLE_TEXT_CRLF_TO_LF_ONLY'
  if data!=local:assert b'\0' not in local and local.replace(b'\r\n',b'\n')==data,name
  files[name]=dict(bytes=len(data),sha256=sha(data),role='REQUIRED_UNCHANGED_SCOPE_REFERENCE',local_literal_sha256=sha(local),publication_bridge=bridge)
 payload_digest=sha(''.join(name+'\t'+str(files[name]['bytes'])+'\t'+files[name]['sha256']+'\n' for name in sorted(files)).encode())
 manifest=dict(schema='reef.immutable-scoped-owner-direction.v1',baseline=BASE,scope='Owner-selected shared Roshan final-action and native-resolution production brief;115 source-derived plan rows. This revision changes no runtime art/source or score. All-game completion remains open.',required_payload_files=len(payload),required_unchanged_scope_references=len(dependencies),required_files_excluding_manifest=len(files),files=files,payload_sha256=payload_digest,payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',separately_closed_prior_library=dict(revision=BASE,manifest_url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+BASE+'/audit/job_review_v2_20261001/CANDY_TRANSITION_KEY_FILES_V28.json',map_sha256='57a8dc8cdc8343fd0b924354aa27a31028ac5157b94acfbc8f765c44e4ae1fa7',files_verified=24975,receipt=REL+'/previous_AE_remote_verified/RESULT.json',lossless_all_file_journal=REL+'/previous_AE_remote_verified/JOURNAL_SHARDS.json',qualification='Existing comprehensive source library and history remain a separately verified BASE artifact. This scoped brief is not a replacement for the broader audit or permission to omit it.'),browser_review='PENDING_LOCAL_PREVIEW_PERMISSION',runtime_changed=False,owner_product_acceptance=None)
 put(B/MAP,manifest);git('add','-f','--',MAP)
 put(V/'SEALED.json',dict(baseline=BASE,payload=payload,dependencies=sorted(dependencies),map_path=MAP,map_sha256=sha((B/MAP).read_bytes()),required_remote_files_including_manifest=len(files)+1,payload_sha256=payload_digest,sealed_utc=now()))
 print(json.dumps(dict(status='SCOPED_PACKET_SEALED',payload_files=len(payload),unchanged_required_references=len(dependencies),remote_files=len(files)+1,map_sha256=sha((B/MAP).read_bytes()))),flush=True)
elif sys.argv[1]=='publish':
 sealed=read(V/'SEALED.json');assert git('rev-parse','HEAD').decode().strip()==BASE;facts()
 assert sha((B/MAP).read_bytes())==sealed['map_sha256']
 staged=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert staged==set(sealed['payload'])|{MAP}
 run('fetch',['git','fetch','origin','dev',BRANCH]);assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
 for name in ['authority','development']:run('precommit_'+name,[PY,'-X','utf8','-B','tools/audit_document_authority.py'] if name=='authority' else [PY,'-X','utf8','-B','tools/audit_development.py','--base','auto'])
 run('commit',['git','commit','-m','Record shared Roshan final-action format and native-resolution rollout'])
 revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
 for name in ['authority','development']:run('postcommit_'+name,[PY,'-X','utf8','-B','tools/audit_document_authority.py'] if name=='authority' else [PY,'-X','utf8','-B','tools/audit_development.py','--base','auto'])
 run('push',['git','push','origin','HEAD:refs/heads/'+BRANCH])
 receipt=dict(status='PUBLISHED_REMOTE_VERIFICATION_PENDING',revision=revision,tree=tree,map_sha256=sealed['map_sha256'],payload_sha256=sealed['payload_sha256'],entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+REL+'/index.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest_url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+MAP,checked_utc=now(),qualification='Scoped owner-direction review only. Browser/actual rollout/native resolution/source/action/device/child/owner and full goal remain separate.')
 put(V/'INITIAL_PUBLICATION_RECEIPT.json',receipt)
 manifest=read(B/MAP);required=dict(manifest['files']);required[MAP]=dict(bytes=(B/MAP).stat().st_size,sha256=sha((B/MAP).read_bytes()),role='MANIFEST')
 started=now();journal=[]
 def fetch(item):
  name,expected=item;url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+urllib.parse.quote(name)
  try:
   request=urllib.request.Request(url,headers={'User-Agent':'MermaidRoshan-ScopedReviewByteCheck'})
   with urllib.request.urlopen(request,timeout=60) as response:data=response.read();status=response.status
   return dict(path=name,expected_bytes=expected['bytes'],actual_bytes=len(data),expected_sha256=expected['sha256'],actual_sha256=sha(data),http_status=status,checked_utc=now(),pass_check=status==200 and len(data)==expected['bytes'] and sha(data)==expected['sha256'])
  except Exception as e:return dict(path=name,pass_check=False,error=type(e).__name__+': '+str(e),checked_utc=now())
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for record in pool.map(fetch,sorted(required.items())):
   journal.append(record)
   with (V/'REMOTE_JOURNAL.jsonl').open('ab') as stream:stream.write((json.dumps(record,separators=(',',':'))+'\n').encode())
 failures=[r for r in journal if not r['pass_check']]
 result=dict(**{k:v for k,v in receipt.items() if k!='status'},status='PASS_ALL_SCOPED_REMOTE_BYTES' if not failures else 'FAIL_REMOTE_BYTES',files_verified=len(journal),failed_files=failures,access_mode='Anonymous GET; normal TLS; no Authorization header',started_utc=started,finished_utc=now(),browser_review='PENDING_LOCAL_PREVIEW_PERMISSION',runtime_changed=False,goal_status='active',owner_acceptance=None)
 put(V/'RESULT.json',result);print(json.dumps(result),flush=True);assert not failures
else:raise SystemExit('Use prepare or publish')
