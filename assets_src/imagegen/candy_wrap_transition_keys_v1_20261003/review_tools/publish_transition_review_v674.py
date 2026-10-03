from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.parse,urllib.request

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';C=B/'assets_src/imagegen/candy_wrap_transition_keys_v1_20261003';L=B/'audit/job_artwork_refinement_live';IP=B/'design/audit_impacts/job-candy-wrap-transition-keys-20261003.json'
BASE='296b2adc8cf4e9b3adbc27a5b5d281471893f6bf';BRANCH='codex/job-art-review-v2-20261001';MAP='audit/job_review_v2_20261001/CANDY_TRANSITION_KEY_FILES_V28.json';PRIOR='audit/job_review_v2_20261001/CANDY_TWIST_RELEASE_COMPONENT_FILES_V27.json';SHARDS='audit/job_review_v2_20261001/v28_unchanged_dependency_shards'
PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe';OUT=B/'tmp/transition_publish_v674';VERIFY=B/'tmp/transition_remote_v674';SEAL=B/'tmp/transition_sealed_v674.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):
    p.parent.mkdir(parents=True,exist_ok=True);n=p.with_name(p.name+'.v674_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode());n.replace(p)
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
    reg=load_register(L);assert reg['display_revision']=='V55' and len(reg['items'])==2160 and reg['counts']['inclusive_current_source_priorities']==1063 and reg['counts']['unique_source_file_priorities']==686 and reg['counts']['unreviewed_current_source']==294 and reg['counts']['unique_source_files']==1308
    stamp=read(L/'CURRENT_BOUNDARY_REFRESH.json');assert stamp['registry_items']==stamp['registered_source_matches']==2160 and stamp['assembled_registry_parts_verified'] and stamp['registry_root_sha256']==sha((L/'ALL_ITEMS.json').read_bytes()) and stamp['registry_parts']==reg['item_shards'] and stamp['candy_capture_boundary_match']
    previous=read(C/'previous_v54/ALL_ITEMS.json');current=read(L/'ALL_ITEMS.json');assert len(previous['items'])==2064 and current['items'][:2064]==previous['items'] and len(current['items'])==2072 and current['item_shards']==previous['item_shards'] and (L/'ALL_ITEMS.json').stat().st_size<4194304
    review=read(C/'REVIEW_SUMMARY.json');assert review['native_sources']==8 and review['individual_source_component_opinions']==88 and review['static_neighbor_opinions']==6 and review['total_individual_opinions']==94 and review['best_midturn_source_score']==4.2 and review['selected_midturn_key'] is None and review['early_release_source_score']==4.5 and review['current_game_wrap_score']==2.8 and review['complete_wrapping_score'] is None and not review['runtime_integration'] and not review['new_motion_dispatched'] and review['owner_acceptance'] is None
    for stage,scores in [('midturn',[4.0,4.1,4.0,4.2]),('release',[4.1,4.3,4.2,4.5])]:
        for i,score in enumerate(scores,1):
            M=C/(stage+'_attempt'+str(i).zfill(2));r=read(M/'DIRECT_REVIEW.json');receipt=read(M/'GENERATION_RECEIPT.json');request=read(M/'GENERATION_REQUEST.json')
            assert r['source_score']==score and len(r['opinions'])==11 and r['direct_complete_native_review'] and r['owner_acceptance'] is None and not r['runtime_integration'] and r['mounted_score'] is None and r['sequence_score'] is None and r['action_score'] is None
            assert sha((M/'native.png').read_bytes())==r['native_sha256']==receipt['native_sha256'] and r['native_path']==receipt['native_path'] and r['dimensions']==receipt['native_dimensions']==[1672,941]
            assert sha((M/'PROMPT.txt').read_bytes())==receipt['prompt_sha256']==request['prompt_sha256'] and receipt['method']=='BUILTIN_IMAGEGEN_COMPLETE_FLATTENED_SOURCE' and receipt['references']==request['references']
            for ref in receipt['references']:assert sha((B/ref['path']).read_bytes())==ref['sha256'],ref['path']
    relation=read(C/'NEIGHBOR_SOURCE_REVIEW.json');assert len(relation['opinions'])==6 and all(x['temporal_score'] is None and x['current_game_score'] is None for x in relation['opinions']) and relation['complete_wrapping_score'] is None
    proof=read(C/'TRANSITION_BROWSER_OBSERVATIONS_V670.json');assert 'V55: 2,160' in proof['library']['summary'] and proof['report']['componentRows']==88 and proof['report']['neighborRows']==6 and proof['report']['articles']==8 and proof['report']['stages']==7 and not proof['library']['overflow'] and 'Mounted: unassigned' in proof['item']['item'] and 'Complete action: unassigned' in proof['item']['item']
    preservation=read(C/'DISPLAY_COPY_EDIT.json')
    for path,h in preservation['protected_members'].items():assert sha((B/path).read_bytes())==h,path
    snapshot=read(C/'gates_v1/CANDIDATE_TRANSITION_SOURCE_V672.json')
    for row in snapshot['members']:
        if row['path']=='.gitattributes':continue # Added literal map/shard attributes separately sealed.
        assert [(B/row['path']).stat().st_size,sha((B/row['path']).read_bytes())]==[row['bytes'],row['sha256']],row['path']
    prior=read(C/'previous_AD_remote_verified/RESULT.json');assert prior['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and prior['files_including_manifest']==24850 and prior['revision']==BASE
    journal=read(C/'previous_AD_remote_verified/JOURNAL_SHARDS.json');assert journal['rows']==24850
    for row in journal['shards']:assert [(B/row['path']).stat().st_size,sha((B/row['path']).read_bytes())]==[row['bytes'],row['sha256']]
    boundary=read(P/'PRODUCTION_BOUNDARY.json');assert len(boundary['members'])==783 and all(sha((B/x['path']).read_bytes())==x['sha256'] for x in boundary['members'])

def run(label,args):
    r=subprocess.run(args,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=1800);(OUT/(label+'.stdout.log')).write_bytes(r.stdout);(OUT/(label+'.stderr.log')).write_bytes(r.stderr);print(label,r.returncode,flush=True);assert r.returncode==0,r.stderr.decode(errors='replace')[-1000:]

phase=sys.argv[1];assert phase in ['--prepare','--seal','--publish']
if phase=='--prepare':
    checks();assert read(C/'previous_AD_remote_verified/RESULT.json')['revision']==BASE
    dst=C/'review_tools'/Path(__file__).name
    if Path(__file__).resolve()!=dst.resolve():shutil.copyfile(__file__,dst)
    attrs=B/'.gitattributes';old=attrs.read_bytes();extra=('\n'+MAP+' -text\n'+SHARDS+'/** -text\n').encode();assert (MAP+' -text').encode() not in old;n=attrs.with_name(attrs.name+'.v674_next');n.write_bytes(old+extra);n.replace(attrs)
    write(B/MAP,dict(status='PENDING_EXACT_TRANSITION_SOURCE_REVIEW_STAGED_SEAL',base_revision=BASE,qualification='Placeholder metadata only;no predicted remote or creative acceptance.'))
    d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in C.rglob('*') if p.is_file()}|{MAP,'.gitattributes',C.relative_to(B).as_posix()+'/PUBLICATION_BOUNDARY_V674.json'})
    for v in d['validation']:
        if v['command']=='Source-only structural/document/2D no-regression/register gates':v.update(result='PASS',evidence=C.relative_to(B).as_posix()+'/gates_v1;actual authority/development,52 document tests,9 register-integrity tests and2D no-regression pass. Strict2D remains UNSATISFIED;visual/action/owner independent.')
    write(IP,d);print('PREPARED_EXACT_TRANSITION_PUBLICATION_SCOPE',len(d['files']),flush=True);sys.exit(0)
if phase=='--seal':
    checks();source=read(P/'PRODUCTION_BOUNDARY.json')['members'];tracked={x.decode() for x in git('ls-files','-z').split(b'\0') if x};published={x['path'] for x in source if x['path'] in tracked};aux=[x for x in source if x['path'] not in tracked];assert len(published)==543 and len(aux)==240 and all(x['path'].endswith('.gd.uid') for x in aux)
    bridge=[]
    for x in source:
        path=x['path'];raw=(B/path).read_bytes()
        if path in published:
            prior=git('show','HEAD:'+path);exact=raw==prior;normalized=not exact and prior==raw.replace(b'\r\n',b'\n');assert exact or normalized,path;bridge.append(dict(path=path,literal_sha256=sha(raw),published_sha256=sha(prior),exact_bytes=exact,whole_text_crlf_to_lf_only=normalized))
    write(C/'PUBLICATION_BOUNDARY_V674.json',dict(status='PASS_NO_PRODUCTION_DELTA_ALL783_LITERALS_UNCHANGED',checked_utc=now(),source_revision=BASE,published_members=543,auxiliary_uid_members=240,source_bridge=bridge,qualification='Only review ImageGen source drafts/QA/illustrated reports change. All production bytes and previous production checks remain separately source bound. No visual/action/device/child/owner/integration/release acceptance.'))
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
    manifest=dict(schema='reef.immutable-review-supplement.sharded.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_dependency_shards=desc,shard_max_bytes=900000,qualification='V55:2160 known entries/1308 primary sources/1063 inclusive source-cell-region priorities/686 unique priority sources/294 pending primary opinions. Eight complete native ImageGen transition drafts/88 individual component and6 static-neighbor opinions. Seven intended-stage rejections retained;early-releaseA4 source4.5 provisional with coherent thumbs/cuffs,purple clearance and thin flat paper necks. Midturn best4.2 remains rejected,no selected midpoint or newmotion. Prior localtwist2.2/release1.7,current actualWRAP2.8/all783 production literals unchanged. Current turquoise widget/whisk work atlas do not bind gold family. Prior2064 root dictionaries/literal88-item part and4MiB ceiling preserved. Actual report/library/disclosure/individual-source browser proof,52 document tests/9 integrity tests and all24850 preceding AD anonymous rows retained. No runtime/protected-original/3D/security/gate/workflow/finding lifecycle/integration/release or full causal wrapping/broad jobs/day/Opera training/ordinary routes/device/child/owner/comprehensive report acceptance.')
    write(B/MAP,manifest,True);assert (B/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP);assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
    write(SEAL,dict(status='EXACT_SHARDED_TRANSITION_REVIEW_BYTES_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=manifest['payload_sha256'],files=files,unchanged=unchanged,dependency_shards=desc,map_bytes=len(raw),checked_utc=now()));print('SEALED',len(files),'changed payloads',len(unchanged),'unchanged dependencies',len(desc),'bounded shards','root bytes',len(raw),flush=True);sys.exit(0)

checks();seal=read(SEAL);assert seal['status']=='EXACT_SHARDED_TRANSITION_REVIEW_BYTES_SEALED';raw=git('show',':'+MAP);assert sha(raw)==seal['map_sha256'];manifest=json.loads(raw);expected=dict(seal['files']);expected[MAP]=[len(raw),sha(raw)];assert blobs('',set(expected))==expected
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected);OUT.mkdir(exist_ok=False);VERIFY.mkdir(exist_ok=False);shutil.copyfile(__file__,OUT/Path(__file__).name)
run('fetch',['git','fetch','origin',BRANCH,'dev']);assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto'])]:run('precommit_'+name,[PY,'-X','utf8','-B',*args])
message=OUT/'COMMIT_MESSAGE.txt';message.write_text('Audit gold-wrapper midpoint and early-release source corrections\n\nPreserve all eight complete native ImageGen drafts and94 individual source/neighbor opinions. Early-releaseA4 source4.5 provisional with continuous thumb/cuff ownership,clear paper separation and thin flat neck folds. Midturn best4.2 remains rejected;no selected midpoint or newmotion.\n\nKeep actual story-job/Opera training WRAP2.8 and all783 production literals unchanged. Current turquoise widget/current whisk work row remain distinct from proposed gold family. Preserve V55 known2160 entries,all prior2064 dictionaries/literal88-item part,current-first library and all24850 prior AD anonymous remote rows. Source-bound browser proofs,52 document tests and9 register-integrity tests retained.\n\nNo runtime/cinematic binding,finding closure,integration or release. Full causal action,broad jobs/day/training,ordinary routes,device,child,owner and comprehensive report acceptance remain open.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(message)]);revision=git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==BASE;tree=git('rev-parse','HEAD^{tree}').decode().strip()
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto'])]:run('postcommit_'+name,[PY,'-X','utf8','-B',*args])
run('push',['git','push','origin','HEAD:refs/heads/'+BRANCH]);assert git('rev-parse','origin/'+BRANCH).decode().strip()==revision
write(OUT/'RECEIPT.json',dict(status='TOPIC_REVIEW_PUBLISHED_ANONYMOUS_BYTE_VERIFICATION_PENDING',revision=revision,tree=tree,map_path=MAP,map_sha256=seal['map_sha256'],checked_utc=now(),qualification='Source review-only. New exact remote/hosted status stays separate from motion/current-game/device/child/owner/comprehensive acceptance.'));print('PUBLISHED',revision,flush=True)
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
