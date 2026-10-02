from pathlib import Path
import datetime, hashlib, html, json, shutil, subprocess, sys, time, zipfile

R = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
Q = R / 'audit/job_qa_portable_v1_20261002'
F = R / 'audit/job_nursery_wash_connected_v1_20261002'
BASE = '9cd42f3acfe80c424aa4ca28288c3331b4340f0a'
BRANCH = 'codex/job-art-review-v2-20261001'
MAP = 'audit/job_review_v2_20261001/PORTABLE_JOB_QA_SUPPLEMENT_FILES_V14.json'
IMPACT = R / 'design/audit_impacts/job-qa-portability-20261002.json'
PY = 'C:/Users/Peter/AppData/Local/Python/bin/python.exe'
GH = 'C:/Program Files/GitHub CLI/gh.exe'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda raw: hashlib.sha256(raw).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')

def git(*args, data=None):
    return subprocess.run(['git', *args], input=data, cwd=R, capture_output=True, check=True).stdout

def boundary():
    rows = read(R/'audit/job_geode_current_recheck_v1_20261002/SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files']
    assert len(rows)==783
    checked=[dict(path=row['path'], sha256=sha((R/row['path']).read_bytes()), matches=sha((R/row['path']).read_bytes())==row['sha256']) for row in rows]
    assert all(row['matches'] for row in checked)
    return dict(status='ALL783_LITERAL_SOURCE_BYTES_UNCHANGED', checked_utc=now(), members=checked)

def blob_values(ref, paths):
    values={}
    proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    for path in paths:
        proc.stdin.write((ref+':'+path+'\n').encode());proc.stdin.flush()
        head=proc.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path
        n=int(head[2]);raw=proc.stdout.read(n);assert len(raw)==n and proc.stdout.read(1)==b'\n'
        values[path]=[n,sha(raw)]
    proc.stdin.close();assert proc.wait(timeout=30)==0
    return values

def stage():
    d=read(IMPACT)
    tracked={p.decode() for p in git('ls-files','-z').split(b'\0') if p}
    removed={x['original_path'] for x in read(Q/'ARCHIVE_MANIFEST.json')['members']}
    additions={p.relative_to(R).as_posix() for p in Q.rglob('*') if p.is_file()}
    scope=additions|removed|{MAP,'audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','.gitattributes','ASSET_LICENSES.md'}
    d['files']=sorted(scope);write(IMPACT,d)
    already={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}
    assert already<=scope|{IMPACT.relative_to(R).as_posix()}
    rm=sorted(removed&tracked)
    if rm:
        git('rm','--cached','--quiet','--pathspec-from-file=-','--pathspec-file-nul',data=b''.join(p.encode()+b'\0' for p in rm))
    present=scope-removed|{IMPACT.relative_to(R).as_posix()}
    for p in present:
        target=(R/p).resolve();assert target.is_relative_to(R.resolve()) and target.is_file(),p
        assert not p.startswith(('.git/','.secrets/','.github/','.codex/','.claude/','assets/book/','assets/audio/voices/','assets/characters/friends/','scripts/','assets/')),p
    git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=b''.join(p.encode()+b'\0' for p in sorted(present)))
    changed={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}
    assert changed<=scope|{IMPACT.relative_to(R).as_posix()}
    return changed,removed

action=sys.argv[1]
assert git('rev-parse','HEAD').decode().strip()==BASE
assert git('branch','--show-current').decode().strip()==BRANCH
if action=='prepare':
    assert not Q.exists()
    git('fetch','origin',BRANCH)
    assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
    Q.mkdir();(Q/'review_tools').mkdir();(Q/'gates').mkdir()
    (Q/'.gdignore').write_text('',encoding='utf-8')
    shutil.copyfile(__file__,Q/'review_tools'/Path(__file__).name)
    plan=dict(status='PLANNED_BEFORE_ARCHIVE_CHANGE',baseline=BASE,checked_utc=now(),scope='Reversible packaging repair for Windows checkout of already-published job QA. Preserve every original byte/path/hash in a lossless short-member ZIP, historical commits and physical local originals. Untrack only these 428 isolated Godot process/cache/log files. Do not change production art, source, workflows, security settings, engine, scores, protected originals or owner decisions.',rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-QA-01','DL-QA-02','DL-QA-03','DL-QA-06','DL-QA-07'],findings=[],no_findings_reason='The concrete hosted Windows checkout failure is new QA evidence packaging portability, not a new game visual defect. Preserve MA-VIS-006, MA-PLAY-004 and MA-OPERA-012 lifecycle states; no visual closure claimed.',required_evidence=['Exact completed O hosted job status and checkout fatal lines','All 428 archive members roundtrip byte/SHA matched to P Git blobs','All current783 production boundary members literal unchanged','Current index Windows absolute-path length inventory','Document authority/development gates','Exact immutable anonymous remote payload verification','Fresh hosted suite at corrected revision; no integration while red'])
    write(Q/'PLAN.json',plan)
    write(IMPACT,dict(id='job-qa-portability-20261002',scope=plan['scope'],baseline=BASE,rules=plan['rules'],findings=[],no_findings_reason=plan['no_findings_reason'],files=[(Q/'PLAN.json').relative_to(R).as_posix()],validation=[dict(command='Lossless QA archive roundtrip, source freeze, document authority and development checks, immutable publication and fresh hosted suite',result='PENDING',evidence='audit/job_qa_portable_v1_20261002/PLAN.json')],acceptance_gaps='Packaging does not change any visual/action score or confer creative, device, child, all-job, integration or release acceptance. Corrected hosted CI must be green before integration; source-specific imagegen upload and browser persistence remain separately blocked pending explicit authorization.'))
    status=json.loads(subprocess.check_output([GH,'run','view','37075551850','--json','status,conclusion,headSha,jobs,url'],cwd=R))
    assert status['headSha']=='c2538760639d79b063152ce5530807c04545ba6e' and status['conclusion']=='failure'
    status['captured_utc']=now();write(Q/'HOSTED_O_COMPLETED.json',status)
    log=subprocess.check_output([GH,'run','view','37075551850','--log-failed'],cwd=R)
    lines=[line for line in log.decode('utf-8',errors='replace').splitlines() if 'fatal:' in line or '##[error]' in line]
    assert any('Filename too long' in line for line in lines)
    assert not any('AUTHORIZATION' in line.upper() or 'EXTRAHEADER' in line.upper() or 'TOKEN=' in line.upper() for line in lines)
    (Q/'HOSTED_O_FAILURE_EXCERPT.log').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    write(Q/'HOSTED_O_LOG_SELECTION.json',dict(status='ERROR_LINES_ONLY',full_stdout_sha256=sha(log),full_stdout_bytes=len(log),selected_lines=len(lines),qualification='Only fatal/error lines saved; no credential-bearing checkout setup output saved. Full job remains accessible at exact Actions run. Gameplay probes success; independent Windows area-music job failed during checkout, before tests.'))
    prefix='audit/job_nursery_wash_connected_v1_20261002/'
    paths=sorted(p.decode() for p in git('ls-files','-z').split(b'\0') if p and p.decode().startswith(prefix) and '/Roaming/' in p.decode())
    assert len(paths)==428 and all(Path(p).suffix in ('.cache','.log') for p in paths)
    expected=blob_values('HEAD',paths)
    archive=Q/'nursery_process.zip';members=[]
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for i,p in enumerate(paths):
            target=(R/p).resolve();assert target.is_relative_to(F.resolve()) and target.is_file()
            raw=target.read_bytes();assert [len(raw),sha(raw)]==expected[p],p
            name=f'f{i:04d}{Path(p).suffix}'
            info=zipfile.ZipInfo(name,date_time=(2026,10,2,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
            members.append(dict(original_path=p,archive_member=name,bytes=len(raw),sha256=sha(raw),original_revision=BASE,original_url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+BASE+'/'+p.replace(' ','%20'),source_role='isolated generated QA engine cache/log; non-runtime evidence',physical_original_preserved=True))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.infolist())==428
        for row in members:
            raw=z.read(row['archive_member']);assert [len(raw),sha(raw)]==[row['bytes'],row['sha256']]
    formula=''.join(row['original_path']+'\t'+str(row['bytes'])+'\t'+row['sha256']+'\n' for row in members).encode()
    write(Q/'ARCHIVE_MANIFEST.json',dict(status='PASS_ALL428_LOSSLESS_ARCHIVE_MEMBERS',original_revision=BASE,archive_path=archive.relative_to(R).as_posix(),archive_bytes=archive.stat().st_size,archive_sha256=sha(archive.read_bytes()),members_count=428,original_payload_bytes=sum(row['bytes'] for row in members),original_payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted original path TAB bytes TAB SHA256 LF',members=members,qualification='Current short ZIP is inspectable lossless evidence; ZIP member mapping preserves original names. Current Git removes only standalone process/cache/log paths. Physical local originals and published O/P original paths remain untouched. No source/image/score change.'))
    write(Q/'BOUNDARY_UNCHANGED.json',boundary())
    attrs=R/'.gitattributes';attrs.write_bytes(attrs.read_bytes()+b'\n# Lossless short-path job QA archive and provenance retain literal bytes.\naudit/job_qa_portable_v1_20261002/** -text\n')
    licenses=R/'ASSET_LICENSES.md';licenses.write_bytes(licenses.read_bytes()+b'\n| `audit/job_qa_portable_v1_20261002/nursery_process.zip` | Local Godot 4.7.2 isolated QA process cache/log evidence | Generated diagnostic data; engine provenance preserved (Godot MIT) | https://godotengine.org/license/ | Lossless ZIP packaging only; all 428 original bytes, paths and hashes in ARCHIVE_MANIFEST.json; no runtime asset or delivery pixels. |\n')
    note='QA portability continuation (2026-10-02): [lossless short-path package and hosted failure evidence](job_qa_portable_v1_20261002/index.html) preserves all428 generated process/cache/log files, every original byte/path/hash, local originals and immutable P/O revisions. Hosted O gameplay probes passed; Windows area-music checkout failed with Filename too long before its test. No workflow/security/source/art/score changes. All783 current literal source bytes unchanged; local82/82 remains scoped machine evidence. Fresh corrected hosted/remote verification is pending; no integration/release or visual/owner acceptance. [Impact](../design/audit_impacts/job-qa-portability-20261002.json).'
    master=R/'audit/MASTER_AUDIT_2026-08-09.md';raw=master.read_text(encoding='utf-8');raw=raw.replace('## 0. Planning entry\n','## 0. Planning entry\n\n'+note+'\n',1).replace('### Development task index\n','### Development task index\n\n'+note+'\n',1);master.write_text(raw,encoding='utf-8',newline='\n')
    ledger=R/'design/05_DOC_LEDGER.md';ledger.write_bytes(ledger.read_bytes()+b'\n| `audit/job_qa_portable_v1_20261002/index.html` | '+ '🔵'.encode()+b' | `SUPPORTING_CURRENT`; reversible lossless short-path archive of428 previously-published isolated Godot QA files; original path/hash mapping and O completed hosted failure preserved. Gameplay probes success is separate from Windows checkout failure. All783 source bytes and artwork scores unchanged; corrected hosted/anonymous publication verification pending; no creative/device/child/all-job/integration/release acceptance. |\n')
    pverify=R/'tmp/current_review_checkpoint_p_remote_v398/RESULT.json'
    if pverify.exists():
        result=read(pverify);assert result['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and result['revision']==BASE
        dest=Q/'previous_p_remote_verified';dest.mkdir()
        for name in ('RESULT.json','VERIFICATION_JOURNAL.jsonl'):shutil.copyfile(pverify.parent/name,dest/name)
    (Q/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Job QA portability review</title><style>body{font:18px system-ui;max-width:1000px;margin:36px auto;padding:0 20px;color:#253449;background:#f3f5fa}a{color:#25467c}li{margin:8px 0}</style><h1>Lossless job QA packaging repair</h1><p>Geologist opens the rock to reveal rooted crystals. Current source and in-game scores remain unchanged. This package repairs a Windows checkout problem in archived Nursery QA evidence.</p><p>At exact O revision, the gameplay probe job passed; the separate Windows area-music job failed during checkout with “Filename too long”, before running its test. Corrected hosted CI remains pending.</p><p>All 428 original process/cache/log files are preserved byte-for-byte in a ZIP with short member names. The manifest maps every original name, size and SHA-256 to its archive member and immutable P revision. Physical local originals remain untouched. No workflow, security, source, art or score changes.</p><ul><li><a href="ARCHIVE_MANIFEST.json">Complete original path and hash manifest</a></li><li><a href="nursery_process.zip">Lossless evidence archive</a></li><li><a href="HOSTED_O_COMPLETED.json">Exact hosted O jobs and steps</a></li><li><a href="HOSTED_O_FAILURE_EXCERPT.log">Windows checkout failure lines</a></li><li><a href="BOUNDARY_UNCHANGED.json">All 783 current source bytes unchanged</a></li><li><a href="../job_geode_current_recheck_v1_20261002/index.html">Current illustrated Geologist review</a></li><li><a href="../job_artwork_refinement_live/all_items.html">Individual all-job library: 1778 items</a></li></ul><p>The local unmodified 82/82 suite remains separately qualified. Visual/action, device, child, owner, complete all-job and release acceptance remain open. Prior scores and failed drafts are preserved. This report is a review draft.</p></html>',encoding='utf-8',newline='\n')
    write(R/MAP,dict(status='PREPARING_PORTABLE_REVIEW_MAP',base_revision=BASE))
    changed,removed=stage()
    paths=[p.decode() for p in git('ls-files','-z').split(b'\0') if p]
    runner_prefix='D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'
    longest=sorted(((len(runner_prefix+p),p) for p in paths),reverse=True)
    assert longest[0][0]<260
    write(Q/'INDEX_PATH_LENGTH_CHECK.json',dict(status='PASS_CONSERVATIVE_WINDOWS_PATH_LENGTH',runner_prefix=runner_prefix,tracked_files=len(paths),max_absolute_characters=longest[0][0],max_relative_characters=len(longest[0][1]),longest_members=longest[:12],archive_member_max_characters=max(len(x['archive_member']) for x in members),qualification='Static full-index path bound with exact observed GitHub checkout root; fresh hosted Windows checkout still required.'))
    d=read(IMPACT);d['validation']=[dict(command='All428 ZIP member roundtrip SHA256 against exact P Git blobs',result='PASS',evidence=(Q/'ARCHIVE_MANIFEST.json').relative_to(R).as_posix()),dict(command='All783 literal frozen source members',result='PASS',evidence=(Q/'BOUNDARY_UNCHANGED.json').relative_to(R).as_posix()),dict(command='Conservative Windows absolute tracked path inventory',result='PASS',evidence=(Q/'INDEX_PATH_LENGTH_CHECK.json').relative_to(R).as_posix()),dict(command='Hosted O completed jobs',result='FAIL',evidence=(Q/'HOSTED_O_COMPLETED.json').relative_to(R).as_posix()),dict(command='Fresh corrected hosted suite',result='PENDING',evidence='Pending corrected exact revision; no integration')];write(IMPACT,d);stage()
    print('PORTABLE_QA_PREPARED|428 byte-exact archive members|783 sources unchanged|max Windows path '+str(longest[0][0]))
    raise SystemExit(0)

if action in ('authority','development'):
    label=action+'_v1';out=Q/'gates'/(label+'.stdout.log');err=Q/'gates'/(label+'.stderr.log');rp=Q/'gates'/(label+'.receipt.json')
    assert not rp.exists();out.touch();err.touch();write(rp,dict(status='PENDING'))
    command=[PY,'-X','utf8','-B','tools/audit_document_authority.py' if action=='authority' else 'tools/audit_development.py']
    if action=='development':command+=['--base','auto']
    stage();t=time.monotonic();start=now()
    with out.open('wb') as o,err.open('wb') as e:p=subprocess.run(command,cwd=R,stdout=o,stderr=e,timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
    write(rp,dict(status='PASS' if p.returncode==0 else 'FAIL_PRESERVED',command=command,process_exit=p.returncode,started_utc=start,finished_utc=now(),elapsed_seconds=time.monotonic()-t,stdout_sha256=sha(out.read_bytes()),stderr_sha256=sha(err.read_bytes()),qualification='Traceability only; no visual or hosted acceptance.'))
    d=read(IMPACT);d['validation'].append(dict(command=' '.join(command),result='PASS' if p.returncode==0 else 'FAIL',evidence=rp.relative_to(R).as_posix()));write(IMPACT,d);stage()
    print(label,p.returncode)
    if p.returncode:print(out.read_text(errors='replace')[-6500:])
    raise SystemExit(p.returncode)

assert action=='seal'
for label in ('authority_v1','development_v1'):assert read(Q/'gates'/(label+'.receipt.json'))['status']=='PASS'
write(Q/'BOUNDARY_UNCHANGED.json',boundary())
resultpath=R/'tmp/current_review_checkpoint_p_remote_v398/RESULT.json';assert resultpath.exists()
result=read(resultpath);assert result['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and result['revision']==BASE
dest=Q/'previous_p_remote_verified';dest.mkdir(exist_ok=True)
for name in ('RESULT.json','VERIFICATION_JOURNAL.jsonl'):shutil.copyfile(resultpath.parent/name,dest/name)
changed,removed=stage()
files=blob_values('',sorted(changed-{MAP}-removed))
prior='audit/job_review_v2_20261001/CURRENT_GEODE_RECHECK_SUPPLEMENT_FILES_V13.json';old=read(R/prior)
refs=(set(old['files'])|set(old['unchanged_required_files'])|{prior})-set(files)-removed-{MAP}
unchanged=blob_values('HEAD',sorted(refs));formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
m=dict(schema='reef.immutable-review-supplement.v1',base_revision=BASE,prior_closed_map=prior,prior_closed_map_sha256=sha(git('show','HEAD:'+prior)),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=sorted(removed),archived_prior_paths_manifest='audit/job_qa_portable_v1_20261002/ARCHIVE_MANIFEST.json',qualification='Current portable checkpoint substitutes only428 long standalone QA process/cache/log paths with a lossless ZIP and complete byte/path mapping. Prior V12/V13 maps remain unchanged historical maps of original O/P revisions; removed members resolve inside new archive or original P Git URLs, not standalone at this new revision. Every783 source byte and current art/action score unchanged. Local82/82 and hosted O gameplay job success separate from hosted O Windows checkout failure; corrected hosted CI remains pending. No workflow/security or production changes, blocked-action authorization, creative/device/child/all-job/integration/release acceptance.')
write(R/MAP,m);git('add','-f','--',MAP);raw=git('show',':'+MAP)
seal=dict(status='EXACT_SCOPED_PORTABLE_Q_BLOBS_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=m['payload_sha256'],payload_files=len(files),payload_bytes=m['required_payload_bytes'],unchanged_required_files=len(unchanged),removed_qa_paths=len(removed),checked_utc=now())
write(R/'tmp/portable_job_qa_q_sealed_v399.json',seal);print(json.dumps(seal))
