from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.parse,urllib.request

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';C=B/'assets_src/local_motion/candy_twist_release_components_v1_20261003';L=B/'audit/job_artwork_refinement_live';IP=B/'design/audit_impacts/job-candy-twist-release-components-20261003.json'
BASE='b6501351a854cc0133b17a74d557ce1c4d14b5af';BRANCH='codex/job-art-review-v2-20261001';MAP='audit/job_review_v2_20261001/CANDY_TWIST_RELEASE_COMPONENT_FILES_V27.json';PRIOR='audit/job_review_v2_20261001/CANDY_TWIST_RELEASE_ENDPOINT_FILES_V26.json';SHARDS='audit/job_review_v2_20261001/v27_unchanged_dependency_shards'
PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe';OUT=B/'tmp/component_publish_v651';VERIFY=B/'tmp/component_remote_v651';SEAL=B/'tmp/component_sealed_v651.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):
    p.parent.mkdir(parents=True,exist_ok=True);n=p.with_name(p.name+'.v651_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode());n.replace(p)
def git(*args,data=None):return subprocess.run(['git',*args],cwd=B,input=data,capture_output=True,check=True).stdout
def blobs(ref,paths):
    values={};p=subprocess.Popen(['git','cat-file','--batch'],cwd=B,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    for path in sorted(paths):
        p.stdin.write((ref+':'+path+'\n').encode());p.stdin.flush();head=p.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path;n=int(head[2]);left=n;h=hashlib.sha256()
        while left:
            chunk=p.stdout.read(min(left,65536));assert chunk;left-=len(chunk);h.update(chunk)
        assert p.stdout.read(1)==b'\n';values[path]=[n,h.hexdigest()]
    p.stdin.close();assert p.wait(timeout=30)==0;return values
def stage(paths):
    raw=b''.join(p.encode()+b'\0' for p in sorted(paths));git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=raw);git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',data=raw)
def checks():
    assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()==BRANCH
    for label in ['authority','development','document_tests','game2d','register_parts']:assert read(C/'gates_v1'/(label+'.receipt.json'))['status']=='PASS',label
    sys.path.insert(0,str(L/'review_tools'));from register_parts_v51 import load_register
    reg=load_register(L);assert reg['display_revision']=='V54' and len(reg['items'])==2152 and reg['counts']['inclusive_current_source_priorities']==1055 and reg['counts']['unique_source_file_priorities']==678 and reg['counts']['unreviewed_current_source']==294
    stamp=read(L/'CURRENT_BOUNDARY_REFRESH.json');assert stamp['registry_items']==stamp['registered_source_matches']==2152 and stamp['assembled_registry_parts_verified'] and stamp['registry_root_sha256']==sha((L/'ALL_ITEMS.json').read_bytes()) and stamp['registry_parts']==reg['item_shards']
    previous=read(C/'previous_v53/ALL_ITEMS.json');current=read(L/'ALL_ITEMS.json');assert current['items']==previous['items'] and len(current['items'])==2064 and current['item_shards']==previous['item_shards']
    review=read(C/'REVIEW_SUMMARY.json');assert review['native_frames']==82 and review['individual_frame_opinions']==82 and review['component_opinions']==24 and review['total_individual_opinions']==106 and review['release_score']==1.7 and review['twist_score']==2.2 and review['source_endpoint_score']==4.5 and review['current_game_wrap_score']==2.8 and review['complete_wrapping_score'] is None and not review['runtime_integration'] and review['owner_acceptance'] is None
    for stage,score in [('release',1.7),('twist',2.2)]:
        M=C/(stage+'_a1');A=M/'attempt01';r=read(A/'DIRECT_REVIEW.json');idx=read(A/'INDEX.json');m=read(M/'checks/SUBMITTED_MANIFEST.exact.json');receipt=read(A/'RENDER_RECEIPT.json');state=read(A/'DISPATCH_STATE.json')
        assert len(r['frames'])==len(idx['frames'])==41 and len(r['components'])==12 and r['whole_component_score']==score and r['acceptance']=='LOCAL_MOTION_REFERENCE_ONLY' and not r['runtime_integration'] and r['complete_wrapping_score'] is None and r['owner_acceptance'] is None and not r['endpoint_conditioned']
        assert state['manifest_sha256']==idx['submitted_manifest_sha256']==sha((M/'checks/SUBMITTED_MANIFEST.exact.json').read_bytes()) and receipt['status']=='PASS' and receipt['source_sha256']==m['input_sha256'] and receipt['settings']==m['renderer']['settings'] and receipt['prompt_id']==idx['prompt_id']
        assert sha((M/m['input_path']).read_bytes())==m['input_sha256'] and sha((M/m['prompt_path']).read_bytes())==m['prompt_sha256']==receipt['prompt_sha256']
        job=m['jobs'][0];assert sha((B/job['source_path']).read_bytes())==job['source_sha256'] and len(m['renderer']['bindings'])==7
        for binding in m['renderer']['bindings']:assert sha((M/binding['packet_path']).read_bytes())==binding['sha256']
        for i,(frame,opinion) in enumerate(zip(idx['frames'],r['frames'])):assert frame['index']==opinion['index']==i and frame['sha256']==opinion['sha256']==sha((B/frame['path']).read_bytes()) and opinion['direct_complete_native_review'] and opinion['whole_component_motion_score'] is None and opinion['current_game_score'] is None
        for row in idx['outputs']+idx['boards']:assert sha((B/row['path']).read_bytes())==row['sha256']
    proof=read(C/'BROWSER_OBSERVATIONS_V649.json');assert proof['library']['summary'].startswith('V54: 2,152') and proof['report']['componentRows']==24 and all(v['error'] is None and v['width']==896 and v['height']==512 for v in proof['report']['videos']) and not proof['library']['overflow']
    snapshot=read(C/'gates_v1/CANDIDATE_COMPONENT_SOURCE_V647.json')
    for row in snapshot['members']:
        if row['path']=='.gitattributes':continue # Exact added map/shard text attributes are separately sealed after source checks.
        assert [(B/row['path']).stat().st_size,sha((B/row['path']).read_bytes())]==[row['bytes'],row['sha256']],row['path']
    prior=read(C/'previous_AC_remote_verified/RESULT.json');assert prior['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and prior['files_including_manifest']==24611
    boundary=read(P/'PRODUCTION_BOUNDARY.json');assert len(boundary['members'])==783 and all(sha((B/x['path']).read_bytes())==x['sha256'] for x in boundary['members'])

def run(label,args):
    r=subprocess.run(args,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=1800);(OUT/(label+'.stdout.log')).write_bytes(r.stdout);(OUT/(label+'.stderr.log')).write_bytes(r.stderr);print(label,r.returncode,flush=True);assert r.returncode==0,r.stderr.decode(errors='replace')[-1000:]

phase=sys.argv[1];assert phase in ['--prepare','--seal','--publish']
if phase=='--prepare':
    checks();assert read(C/'previous_AC_remote_verified/RESULT.json')['revision']==BASE
    dst=C/'review_tools'/Path(__file__).name
    if Path(__file__).resolve()!=dst.resolve():shutil.copyfile(__file__,dst)
    attrs=B/'.gitattributes';old=attrs.read_bytes();extra=('\n'+MAP+' -text\n'+SHARDS+'/** -text\n').encode();assert (MAP+' -text').encode() not in old;n=attrs.with_name(attrs.name+'.v651_next');n.write_bytes(old+extra);n.replace(attrs)
    write(B/MAP,dict(status='PENDING_EXACT_REJECTED_COMPONENT_REVIEW_STAGED_SEAL',base_revision=BASE,qualification='Placeholder metadata only;no predicted remote or creative acceptance.'))
    d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in C.rglob('*') if p.is_file()}|{MAP,'.gitattributes',C.relative_to(B).as_posix()+'/PUBLICATION_BOUNDARY_V651.json'})
    for v in d['validation']:
        if v['command']=='Source-only review structural/document/2D no-regression/register gates':v.update(result='PASS',evidence=C.relative_to(B).as_posix()+'/gates_v1;actual authority/development,52 document tests,9 register-integrity tests and2D no-regression pass. Strict2D remains UNSATISFIED;visual/action/owner independent.')
    write(IP,d);print('PREPARED_EXACT_TWIST_RELEASE_COMPONENT_PUBLICATION_SCOPE',len(d['files']),flush=True);sys.exit(0)
if phase=='--seal':
    checks();source=read(P/'PRODUCTION_BOUNDARY.json')['members'];tracked={x.decode() for x in git('ls-files','-z').split(b'\0') if x};published={x['path'] for x in source if x['path'] in tracked};aux=[x for x in source if x['path'] not in tracked];assert len(published)==543 and len(aux)==240 and all(x['path'].endswith('.gd.uid') for x in aux)
    bridge=[]
    for x in source:
        path=x['path'];raw=(B/path).read_bytes()
        if path in published:
            prior=git('show','HEAD:'+path);exact=raw==prior;normalized=not exact and prior==raw.replace(b'\r\n',b'\n');assert exact or normalized,path;bridge.append(dict(path=path,literal_sha256=sha(raw),published_sha256=sha(prior),exact_bytes=exact,whole_text_crlf_to_lf_only=normalized))
    write(C/'PUBLICATION_BOUNDARY_V651.json',dict(status='PASS_NO_PRODUCTION_DELTA_ALL783_LITERALS_UNCHANGED',checked_utc=now(),source_revision=BASE,published_members=543,auxiliary_uid_members=240,source_bridge=bridge,qualification='Only review sources/QA/local reference outputs/illustrated reports change. All production bytes and previous production checks remain separately source bound. No visual/action/device/child/owner/integration/release acceptance.'))
    scope=set(read(IP)['files'])|{IP.relative_to(B).as_posix()};assert all((B/p).is_file() for p in scope)
    assert not any(p.startswith(('assets/','scripts/','.github/','.secrets/','.codex/','.claude/','.git/')) for p in scope)
    assert max(len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+p) for p in scope)<260
    staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=scope
    stage(scope-{MAP});changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope and not git('diff','--cached','--name-only','--diff-filter=D','-z')
    oldraw=git('show','HEAD:'+PRIOR);old=json.loads(oldraw);assert old['schema']=='reef.immutable-review-supplement.sharded.v1';refs=set(old['files'])|{PRIOR}
    for desc in old['unchanged_dependency_shards']:
        raw=git('show','HEAD:'+desc['path']);assert [len(raw),sha(raw)]==[desc['bytes'],desc['sha256']];part=json.loads(raw);assert len(part['files'])==desc['entries'];refs.update(part['files']);refs.add(desc['path'])
    refs-=changed|{MAP};unchanged=blobs('HEAD',refs);assert not any(p.startswith(('.secrets/','.git/','.codex/','.claude/')) for p in refs)
    shard_dir=B/SHARDS;assert not shard_dir.exists();shard_dir.mkdir(parents=True);desc=[];part={};estimate=250
    def emit(part):
        path=SHARDS+f'/PART_{len(desc)+1:03d}.json';write(B/path,dict(schema='reef.unchanged-review-dependency-shard.v1',base_revision=BASE,files=part),True);raw=(B/path).read_bytes();assert len(raw)<=900000;desc.append(dict(path=path,bytes=len(raw),sha256=sha(raw),entries=len(part)))
    for path,value in sorted(unchanged.items()):
        entry=len(json.dumps(path,ensure_ascii=False).encode())+len(json.dumps(value,separators=(',',':')).encode())+2
        if part and estimate+entry>899000:emit(part);part={};estimate=250
        part[path]=value;estimate+=entry
    if part:emit(part)
    assert sum(x['entries'] for x in desc)==len(unchanged)
    d=read(IP);d['files']=sorted(set(d['files'])|{x['path'] for x in desc});write(IP,d);scope|={x['path'] for x in desc};stage(scope-{MAP})
    changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};files=blobs('',changed-{MAP});assert not set(files)&set(unchanged)
    for path,value in files.items():
        if path.startswith(('assets_src/','audit/job_artwork_refinement_live/',C.relative_to(B).as_posix()+'/',SHARDS)):assert value==[(B/path).stat().st_size,sha((B/path).read_bytes())],path
    formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
    manifest=dict(schema='reef.immutable-review-supplement.sharded.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_dependency_shards=desc,shard_max_bytes=900000,qualification='V54 known2152 entries/1300 primary sources/1055 inclusive source-cell-region priorities/678 unique source priorities/294 unreviewed primary sources. Two sequential unchanged developed-local Comfy references:release1.7 rejected for detached coral thumb/broken cuffs/no quiet rest;opposed twist2.2 rejected for absent wrist roll and paper closure. Every82 complete native frame and24 components/106 opinions individually reviewed. Exact manifests saved before dispatch,all native videos/frames/receipts/workflows preserved. Gold source endpoints4.5 provisional,current actual WRAP2.8/all783 production literals unchanged. Single conditioned start image;target endpoint human QC only. Existing2064 root dictionaries/literal88-item part unchanged,4MiB ceiling retained. Current-first library preserves all old historical links/opinions,actual browser proof,52 document tests/9 register-integrity tests and all24611 prior AC anonymous remote rows. No runtime,protected-original,3D,security/gate/workflow,finding lifecycle,dev/master integration/release or complete fold-cover-gather-opposite-twist-supported-release/actual jobs/Opera training/ordinary route/device/child/owner/comprehensive all-job acceptance.')
    write(B/MAP,manifest,True);assert (B/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP);assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
    write(SEAL,dict(status='EXACT_SHARDED_COMPONENT_REVIEW_BYTES_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=manifest['payload_sha256'],files=files,unchanged=unchanged,dependency_shards=desc,map_bytes=len(raw),checked_utc=now()));print('SEALED',len(files),'changed payloads',len(unchanged),'unchanged dependencies',len(desc),'bounded shards','root bytes',len(raw),flush=True);sys.exit(0)

checks();seal=read(SEAL);assert seal['status']=='EXACT_SHARDED_COMPONENT_REVIEW_BYTES_SEALED';raw=git('show',':'+MAP);assert sha(raw)==seal['map_sha256'];manifest=json.loads(raw);expected=dict(seal['files']);expected[MAP]=[len(raw),sha(raw)];assert blobs('',set(expected))==expected
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected);OUT.mkdir(exist_ok=False);VERIFY.mkdir(exist_ok=False);shutil.copyfile(__file__,OUT/Path(__file__).name)
run('fetch',['git','fetch','origin',BRANCH,'dev']);assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto'])]:run('precommit_'+name,[PY,'-X','utf8','-B',*args])
message=OUT/'COMMIT_MESSAGE.txt';message.write_text('Audit specific gold-wrapper twist and release motion components\n\nPreserve both developed-local native references,every82 complete decoded frame and24 named component opinions. Release1.7 rejected for detached thumb/broken cuffs/no quiet rest. Opposed twist2.2 rejected for absent wrist roll/paper closure despite conserved hands/fans. Exact submitted manifests precede dispatch;all native outputs/workflows/receipts retained.\n\nKeep source endpoints4.5 provisional,current actual WRAP2.8 and all783 production literals unchanged. Preserve V54 known2152 entries,all2064 item dictionaries/literal88-item part and source/mounted/action lane separation. Current-first library retains all dated notices/links. Actual browser proofs,52 document tests/9 integrity tests and all24611 prior AC anonymous remote rows preserved.\n\nNo runtime or cinematic binding,finding closure,integration or release. Full causal wrapping,actual story job/Opera training,ordinary routes,device,child,owner and comprehensive all-job acceptance remain open.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(message)]);revision=git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==BASE;tree=git('rev-parse','HEAD^{tree}').decode().strip()
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto'])]:run('postcommit_'+name,[PY,'-X','utf8','-B',*args])
run('push',['git','push','origin','HEAD:refs/heads/'+BRANCH]);assert git('rev-parse','origin/'+BRANCH).decode().strip()==revision
write(OUT/'RECEIPT.json',dict(status='TOPIC_REVIEW_PUBLISHED_ANONYMOUS_BYTE_VERIFICATION_PENDING',revision=revision,tree=tree,map_path=MAP,map_sha256=seal['map_sha256'],checked_utc=now(),qualification='Review-only. New exact remote/hosted status remains separate from source/action/device/child/owner/all-job/integration/release acceptance.'));print('PUBLISHED',revision,flush=True)
url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/';started=now()
def fetch(path,value):
    for attempt in range(1,4):
        try:
            request=urllib.request.Request(url+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-Anonymous-Review-QA'});h=hashlib.sha256();n=0
            with urllib.request.urlopen(request,timeout=60) as response:
                assert response.status==200
                while True:
                    chunk=response.read(65536)
                    if not chunk:break
                    h.update(chunk);n+=len(chunk)
            return dict(path=path,bytes=n,sha256=h.hexdigest(),expected_bytes=value[0],expected_sha256=value[1],matches=[n,h.hexdigest()]==value,attempt=attempt,checked_utc=now(),status='FETCHED_ANONYMOUS_TLS_GET')
        except Exception as exc:
            if attempt==3:return dict(path=path,matches=False,error=str(exc),checked_utc=now(),status='FETCH_FAILED')
            time.sleep(attempt)
targets=dict(seal['files']);targets.update(seal['unchanged']);targets[MAP]=expected[MAP];failed=[];count=0
with (VERIFY/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for future in concurrent.futures.as_completed([pool.submit(fetch,p,v) for p,v in targets.items()]):
            row=future.result();journal.write(json.dumps(row)+'\n');journal.flush();count+=1
            if not row['matches']:failed.append(row)
            if count%500==0:print('ANONYMOUS_REMOTE_BYTES',count,'FAILURES',len(failed),flush=True)
result=dict(status='PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not failed else 'FAIL_PRESERVED',revision=revision,tree=tree,branch=BRANCH,entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+C.relative_to(B).as_posix()+'/index.html',library_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+L.relative_to(B).as_posix()+'/all_items.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest_url=url+MAP,map_sha256=seal['map_sha256'],payload_sha256=manifest['payload_sha256'],payload_files=len(manifest['files']),required_unchanged_files=len(seal['unchanged']),bounded_dependency_shards=len(manifest['unchanged_dependency_shards']),files_including_manifest=count,access_mode='Anonymous GET; normal TLS; no Authorization header',started_utc=started,finished_utc=now(),failed_files=failed,qualification='All closed review payload/reference bytes verified at exact immutable revision. New exact-head hosted CI, graphics/action/device/child/owner/comprehensive all-job/integration/release acceptance remain separate.');write(VERIFY/'RESULT.json',result);print(json.dumps(result),flush=True);sys.exit(0 if not failed else 1)
