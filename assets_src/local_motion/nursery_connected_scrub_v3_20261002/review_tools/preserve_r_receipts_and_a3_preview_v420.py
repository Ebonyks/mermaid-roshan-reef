from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'assets_src/local_motion/nursery_connected_scrub_v3_20261002'
V=R/'tmp/scannable_job_review_r_remote_v415'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
rv=read(V/'RESULT.json');assert rv['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and rv['files_including_manifest']==15802 and rv['revision']=='ea9f4e00a2af67fc6f81e16a2102754892a18cfd'
D=P/'previous_r_remote_verified';assert not D.exists();D.mkdir()
shutil.copyfile(V/'RESULT.json',D/'RESULT.json')
raw=(V/'VERIFICATION_JOURNAL.jsonl').read_bytes();lines=raw.splitlines(keepends=True);assert len(lines)==15802
chunks=[];part=[];n=0
def save():
 global part,n
 if not part:return
 data=b''.join(part);target=D/('journal_%03d.jsonl'%len(chunks));target.write_bytes(data)
 chunks.append(dict(path=target.relative_to(R).as_posix(),bytes=len(data),sha256=sha(data),rows=len(part)));part=[];n=0
for line in lines:
 obj=json.loads(line);assert obj['matches'] is True
 if n+len(line)>1000000:save()
 part.append(line);n+=len(line)
save();assert b''.join((R/x['path']).read_bytes() for x in chunks)==raw
write(D/'JOURNAL_MANIFEST.json',dict(status='PASS_ALL15802_ROWS_BYTE_EXACT_BOUNDED_JOURNAL',revision=rv['revision'],original_bytes=len(raw),original_sha256=sha(raw),original_rows=len(lines),max_chunk_bytes=1000000,chunks=chunks,access_mode=rv['access_mode'],started_utc=rv['started_utc'],finished_utc=rv['finished_utc'],qualification='All exact current R positive/unchanged files and manifest fetched anonymously with normal TLS; every byte/SHA matches. Journal sharding preserves all literal bytes and rows. Source/action/device/child/owner/integration/release acceptance remains separate.'))
gh='C:/Program Files/GitHub CLI/gh.exe';status=json.loads(subprocess.check_output([gh,'run','view','37083138864','--json','status,conclusion,headSha,jobs,url'],cwd=R))
assert status['headSha']==rv['revision'];status['captured_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();status['qualification']='Actual exact R snapshot; in-progress jobs and pending steps are not final success.';write(P/'HOSTED_R_PROGRESS_V420.json',status)
links=''.join('<li><a href="'+Path(x['path']).name+'">Journal chunk '+str(i+1)+' — '+str(x['rows'])+' rows</a></li>' for i,x in enumerate(chunks))
(D/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Immutable R review verification</title><style>body{font:18px system-ui;max-width:1000px;margin:36px auto;padding:0 20px;background:#f3f5fa;color:#253449}a{overflow-wrap:anywhere}</style><h1>Immutable R review: all15,802 required files verified</h1><p>Revision '+rv['revision']+'. Every required positive/unchanged file and manifest fetched anonymously with normal TLS and literal SHA-256 checked. No failed file. '+rv['started_utc']+' to '+rv['finished_utc']+'.</p><p><a href="'+rv['entry_url']+'">Published individual artwork library</a> · <a href="'+rv['tree_url']+'">Immutable tree</a> · <a href="'+rv['manifest_url']+'">Direct immutable manifest</a></p><p>Manifest SHA-256 '+rv['map_sha256']+'; positive payload SHA-256 '+rv['payload_sha256']+'.</p><p>All15802 literal journal rows are preserved in bounded newline-boundary chunks; concatenation reconstructs the original whole journal hash. Current production783 source bytes unchanged. Publication verification is separate from hosted machine/visual/action/device/child/owner/all-job/integration/release acceptance.</p><p><a href="RESULT.json">Exact verification receipt</a> · <a href="JOURNAL_MANIFEST.json">Complete reconstruction manifest</a></p><ul>'+links+'</ul></html>',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-nursery-scrub-fresh-a3-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()});d['validation'].append(dict(command='Exact immutable R15802 anonymous required bytes, every journal row preserved and whole reconstruction exact',result='PASS',evidence=(D/'RESULT.json').relative_to(R).as_posix()+'; '+(D/'JOURNAL_MANIFEST.json').relative_to(R).as_posix()));write(ip,d)
allow=R/'tmp/v2_preview_allowed.json';paths=set(read(allow));paths|={x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()};write(allow,sorted(paths))
print('R_RECEIPT_PRESERVED|15802 exact anonymous bytes|all bounded journal rows|A3 exact preview files whitelisted|hosted '+status['status'])
