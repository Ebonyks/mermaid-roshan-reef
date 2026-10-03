from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.parse,urllib.request

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';C=B/'audit/job_shared_atlas_state_review_v1_20261003';L=B/'audit/job_artwork_refinement_live';IP=B/'design/audit_impacts/job-shared-atlas-state-review-20261003.json'
BASE='c7817974fb23913c1d764c718a70a5932cacb883';BRANCH='codex/job-art-review-v2-20261001';MAP='audit/job_review_v2_20261001/SHARED_PROP_CELL_REVIEW_FILES_V24.json';PRIOR='audit/job_review_v2_20261001/CANDY_COVER_POSE_FILES_V23.json';SHARDS='audit/job_review_v2_20261001/v24_unchanged_dependency_shards'
PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe';OUT=B/'tmp/atlas_publish_v604';VERIFY=B/'tmp/atlas_remote_v604';SEAL=B/'tmp/atlas_sealed_v604.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):
    p.parent.mkdir(parents=True,exist_ok=True);n=p.with_name(p.name+'.v604_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode());n.replace(p)
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
    reg=load_register(L);assert reg['display_revision']=='V51' and len(reg['items'])==2138 and reg['counts']['inclusive_current_source_priorities']==1041 and reg['counts']['unique_source_file_priorities']==664 and reg['counts']['unreviewed_current_source']==294
    stamp=read(L/'CURRENT_BOUNDARY_REFRESH.json');assert stamp['registry_items']==stamp['registered_source_matches']==2138 and stamp['assembled_registry_parts_verified'] and stamp['registry_root_sha256']==sha((L/'ALL_ITEMS.json').read_bytes()) and stamp['registry_parts']==reg['item_shards']
    review=read(C/'DIRECT_CELL_REVIEW.json');assert review['individual_source_cells']==review['inclusive_cell_priorities']==88 and review['relationship_opinions']==33 and review['full_timed_motion_score'] is None and not review['runtime_changed']
    assert all(len(a['cells'])==8 and all(c['direct_native_cell_review'] and c['current_mounted_score'] is None and c['current_complete_action_score'] is None for c in a['cells']) for a in review['atlases'])
    assert read(B/'tmp/cover_remote_v594/RESULT.json')['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
    boundary=read(P/'PRODUCTION_BOUNDARY.json');assert len(boundary['members'])==783 and all(sha((B/x['path']).read_bytes())==x['sha256'] for x in boundary['members'])

def run(label,args):
    r=subprocess.run(args,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=1800);(OUT/(label+'.stdout.log')).write_bytes(r.stdout);(OUT/(label+'.stderr.log')).write_bytes(r.stderr);print(label,r.returncode,flush=True);assert r.returncode==0,r.stderr.decode(errors='replace')[-1000:]

phase=sys.argv[1];assert phase in ['--prepare','--seal','--publish']
if phase=='--prepare':
    checks();remote=C/'previous_z_remote_verified';assert not remote.exists();remote.mkdir()
    source=B/'tmp/cover_remote_v594';result=read(source/'RESULT.json');assert result['revision']==BASE and result['files_including_manifest']==24146 and not result['failed_files']
    shutil.copyfile(source/'RESULT.json',remote/'RESULT.json');shutil.copyfile(B/'tmp/cover_publish_v594/RECEIPT.json',remote/'PUBLICATION_RECEIPT.json')
    raw=(source/'VERIFICATION_JOURNAL.jsonl').read_bytes();lines=raw.splitlines(keepends=True);assert len(lines)==24146 and all(json.loads(x)['matches'] for x in lines);parts=[];group=[];size=0
    def emit_rows():
        payload=b''.join(group);p=remote/f'JOURNAL_{len(parts)+1:03d}.jsonl';p.write_bytes(payload);assert len(payload)<=900000;parts.append(dict(path=p.relative_to(B).as_posix(),bytes=len(payload),sha256=sha(payload),rows=len(group)))
    for line in lines:
        if group and size+len(line)>899000:emit_rows();group=[];size=0
        group.append(line);size+=len(line)
    if group:emit_rows()
    assert b''.join((B/x['path']).read_bytes() for x in parts)==raw
    write(remote/'JOURNAL_SHARDS.json',dict(status='ALL24146_EXACT_Z_ANONYMOUS_GET_ROWS_LOSSLESSLY_PRESERVED',revision=BASE,original_bytes=len(raw),original_sha256=sha(raw),original_rows=len(lines),parts=parts,shard_max_bytes=900000,qualification='Complete literal per-file anonymous remote verification at exact Z. Prior Z proof does not accept the new atlas-review revision. Initial pending publication receipt is preserved separately from the terminal PASS result.'))
    dst=C/'review_tools'/Path(__file__).name
    if Path(__file__).resolve()!=dst.resolve():shutil.copyfile(__file__,dst)
    attrs=B/'.gitattributes';old=attrs.read_bytes();extra=('\n'+MAP+' -text\n'+SHARDS+'/** -text\n'+C.relative_to(B).as_posix()+'/** -text\n').encode();assert (MAP+' -text').encode() not in old;n=attrs.with_name(attrs.name+'.v604_next');n.write_bytes(old+extra);n.replace(attrs)
    write(B/MAP,dict(status='PENDING_EXACT_ATLAS_REVIEW_STAGED_SEAL',base_revision=BASE,qualification='Metadata placeholder only. No predicted published bytes or acceptance.'))
    d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in C.rglob('*') if p.is_file()}|{MAP,'.gitattributes',C.relative_to(B).as_posix()+'/PUBLICATION_BOUNDARY_V604.json'})
    d['validation'].append(dict(command='Prior Z all24146 exact anonymous remote journal archival',result='PASS',evidence=remote.relative_to(B).as_posix()+'/RESULT.json and JOURNAL_SHARDS.json;all literal ordered rows retained. Does not grant new revision or creative acceptance.'))
    write(IP,d);print('PREPARED_NEW_ATLAS_REVIEW_PUBLICATION_SCOPE',len(d['files']),flush=True);sys.exit(0)
if phase=='--seal':
    checks();source=read(P/'PRODUCTION_BOUNDARY.json')['members'];tracked={x.decode() for x in git('ls-files','-z').split(b'\0') if x};published={x['path'] for x in source if x['path'] in tracked};aux=[x for x in source if x['path'] not in tracked];assert len(published)==543 and len(aux)==240 and all(x['path'].endswith('.gd.uid') for x in aux)
    bridge=[]
    for x in source:
        path=x['path'];raw=(B/path).read_bytes()
        if path in published:
            prior=git('show','HEAD:'+path);exact=raw==prior;normalized=not exact and prior==raw.replace(b'\r\n',b'\n');assert exact or normalized,path;bridge.append(dict(path=path,literal_sha256=sha(raw),published_sha256=sha(prior),exact_bytes=exact,whole_text_crlf_to_lf_only=normalized))
    write(C/'PUBLICATION_BOUNDARY_V604.json',dict(status='PASS_NO_PRODUCTION_DELTA_ALL783_LITERALS_UNCHANGED',checked_utc=now(),source_revision=BASE,published_members=543,auxiliary_uid_members=240,source_bridge=bridge,qualification='Only review sources/QA/local reference outputs/illustrated reports change. All production bytes and previous production checks remain separately source bound. No visual/action/device/child/owner/integration/release acceptance.'))
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
    manifest=dict(schema='reef.immutable-review-supplement.sharded.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_dependency_shards=desc,shard_max_bytes=900000,qualification='V51 known2138 items/1286 primary sources/1041 inclusive source-cell-region priorities/664 unique source priorities/294 unreviewed primary sources. All88 shared Library/Playroom native state cells and33 static source relationships individually inspected, all88 inclusive priorities. Root2050 earlier records remain identical; one literal SHA/size/count-bound88-item part, existing4MiB ceiling unchanged,9 meaningful register tests and52 document tests pass. Tent source occlusion and three-block identity are bounded successes; stacking-ring/pearl conservation, changing wave silhouettes, book turn/return and sailboat loop remain weak. Declared tent order skips5/6/7; no full timed/current mounted/action score from source inspection. All783 production literals unchanged,current Candy WRAP2.8. Prior Z all24146 anonymous remote rows losslessly preserved. No production,protected originals,3D,security/gate/workflow,finding lifecycle,dev/master integration/release or device/child/owner/comprehensive all-job acceptance.')
    write(B/MAP,manifest,True);assert (B/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP);assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
    write(SEAL,dict(status='EXACT_SHARDED_ATLAS_REVIEW_BYTES_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=manifest['payload_sha256'],files=files,unchanged=unchanged,dependency_shards=desc,map_bytes=len(raw),checked_utc=now()));print('SEALED',len(files),'changed payloads',len(unchanged),'unchanged dependencies',len(desc),'bounded shards','root bytes',len(raw),flush=True);sys.exit(0)

checks();seal=read(SEAL);assert seal['status']=='EXACT_SHARDED_ATLAS_REVIEW_BYTES_SEALED';raw=git('show',':'+MAP);assert sha(raw)==seal['map_sha256'];manifest=json.loads(raw);expected=dict(seal['files']);expected[MAP]=[len(raw),sha(raw)];assert blobs('',set(expected))==expected
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected);OUT.mkdir(exist_ok=False);VERIFY.mkdir(exist_ok=False);shutil.copyfile(__file__,OUT/Path(__file__).name)
run('fetch',['git','fetch','origin',BRANCH,'dev']);assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto']),('game2d',['tools/audit_game_2d.py','--regression-gate'])]:run('precommit_'+name,[PY,'-X','utf8','-B',*args])
message=OUT/'COMMIT_MESSAGE.txt';message.write_text('Audit all88 remaining shared-prop atlas states individually\n\nPreserve exact native Library/Playroom crops and separate written scores for every authored state, plus33 static source relationships and literal manifest order. All88 cells are inclusive priorities. Record ring duplication/colour/pearl continuity, ambiguous stuffed-toy wave silhouettes, page-turn/return gaps, sailboat loop identity and three tent poses absent from the manifest. Source occlusion and conserved block identities do not grant a complete played interaction. No production artwork changes.\n\nExtend the illustrated V51 register to2138 known entries,1041 source-cell-region priorities,664 unique source priorities and294 unreviewed primary sources. Keep all2050 prior item records identical and the exact V50 archive. Load88 extra cells through one literal hash/size/count/ID-verified part with the existing4MiB ceiling; missing or altered parts fail closed. Nine integrity tests,52 document tests, fresh authority/development and2D no-regression checks pass. All2138 source hashes/all783 production members match. Save actual browser proof and all24146 prior Z anonymous remote verification rows in bounded lossless shards.\n\nNo runtime,protected originals,security,gates,workflows,3D,finding lifecycle,dev/master integration or release change. Candy wrapping remains2.8; complete action/game/training/device/child/owner/all-job report approval remains open.\n',encoding='utf-8',newline='\n')
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
