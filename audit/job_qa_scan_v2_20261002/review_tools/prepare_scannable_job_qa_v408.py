from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,zipfile
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'audit/job_qa_scan_v2_20261002';Q=R/'audit/job_qa_portable_v1_20261002'
BASE='72a15c1c49456e37d81c733b8dd6ef4cdc736a45'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*a,data=None):return subprocess.run(['git',*a],cwd=R,input=data,capture_output=True,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()==BASE and not P.exists()
git('fetch','origin','codex/job-art-review-v2-20261001');assert git('rev-parse','origin/codex/job-art-review-v2-20261001').decode().strip()==BASE
P.mkdir();(P/'.gdignore').write_text('',encoding='utf-8');(P/'cache').mkdir();(P/'journals').mkdir();(P/'review_tools').mkdir();(P/'gates').mkdir()
rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-MED-01','DL-ASSET-01','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-QA-01','DL-QA-02','DL-QA-03','DL-QA-06','DL-QA-07']
scope='Repair scanability of current job QA evidence after exact hosted Q2D gate failure: replace oversized ZIP by428 byte-identical short flat cache/log files, and split oversized remote JSONL journals on line boundaries into individually inspectable <=1MB chunks. Preserve every original byte/path/hash, old physical originals, all historical published maps/revisions/failures and current783 production source bytes. No validator, manifest ceiling, workflow, security, production art/code, score or owner-policy changes.'
plan=dict(status='PLANNED_BEFORE_SCANABILITY_REPAIR',baseline=BASE,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope=scope,rules=rules,findings=[],no_findings_reason='QA packaging alone exceeded unchanged model audit bounded scan caps; this is not a new game visual defect and does not close existing findings.',required_evidence=['Exact Q hosted Windows success and model-audit failure','All428 short flat files match preserved ZIP/P original hashes','Each journal parses all rows and concatenates to exact original byte/hash; chunks <=1MB','All783 current source bytes unchanged','Fresh staged unchanged tools/audit_game_2d.py --regression-gate; no ceiling expansion','Document authority/development and exact immutable anonymous remote checks','Fresh hosted suite; no integration while red'])
write(P/'PLAN.json',plan)
ip=R/'design/audit_impacts/job-qa-scanability-20261002.json'
write(ip,dict(id='job-qa-scanability-20261002',scope=scope,baseline=BASE,rules=rules,findings=[],no_findings_reason=plan['no_findings_reason'],files=[(P/'PLAN.json').relative_to(R).as_posix()],validation=[dict(command='Byte-exact bounded QA packaging, unchanged model/development/authority gates and hosted suite',result='PENDING',evidence=P.relative_to(R).as_posix()+'/PLAN.json')],acceptance_gaps='Existing 2D debt remains UNSATISFIED, requiring exact no-regression check with unchanged gate. QA packaging cannot confer current-action/visual/device/child/owner/all-job/integration/release acceptance. Pending external reference upload and browser status approval remain untouched.'))
for src,dst in [('HOSTED.json','HOSTED_Q_COMPLETED.json'),('FAILURE_SELECTION.log','HOSTED_Q_FAILURE_EXCERPT.log')]:shutil.copyfile(R/'tmp/portable_q_hosted_failure_v407'/src,P/dst)
manifest=read(Q/'ARCHIVE_MANIFEST.json');archive=Q/'nursery_process.zip';assert sha(archive.read_bytes())==manifest['archive_sha256']
members=[]
with zipfile.ZipFile(archive) as z:
 for old in manifest['members']:
  raw=z.read(old['archive_member']);assert [len(raw),sha(raw)]==[old['bytes'],old['sha256']]
  target=P/'cache'/old['archive_member'];target.write_bytes(raw);assert sha(target.read_bytes())==old['sha256']
  members.append(dict(original_path=old['original_path'],original_revision=old['original_revision'],current_path=target.relative_to(R).as_posix(),bytes=old['bytes'],sha256=old['sha256'],prior_archive_member=old['archive_member'],role='Exact generated isolated QA cache/log, non-runtime; direct file supports bounded signature inspection.'))
assert len(members)==428
write(P/'CACHE_MANIFEST.json',dict(status='PASS_ALL428_FLAT_FILES_EXACT',prior_archive_path=archive.relative_to(R).as_posix(),prior_archive_revision=BASE,prior_archive_sha256=manifest['archive_sha256'],prior_archive_url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+BASE+'/'+archive.relative_to(R).as_posix(),members=members,qualification='Not compressed or hidden from scan. Every file individually available at short path with unchanged source bytes. Prior ZIP physically intact and immutable on Q.'))
sources=[('o',R/'audit/job_nursery_wash_connected_v1_20261002/remote_verified_v1/VERIFICATION_JOURNAL.jsonl'),('p',Q/'previous_p_remote_verified/VERIFICATION_JOURNAL.jsonl'),('q',R/'tmp/portable_job_qa_q_remote_v400/VERIFICATION_JOURNAL.jsonl')]
journals=[]
for lane,src in sources:
 raw=src.read_bytes();lines=raw.splitlines(keepends=True);assert b''.join(lines)==raw
 for line in lines:assert isinstance(json.loads(line),dict)
 chunks=[];buffer=b'';rows=0
 def flush():
  global buffer,rows
  if not buffer:return
  target=P/'journals'/(lane+'_'+str(len(chunks)).zfill(3)+'.jsonl');target.write_bytes(buffer)
  chunks.append(dict(path=target.relative_to(R).as_posix(),bytes=len(buffer),sha256=sha(buffer),rows=rows))
  buffer=b'';rows=0
 for line in lines:
  assert len(line)<=1000000
  if len(buffer)+len(line)>1000000:flush()
  buffer+=line;rows+=1
 flush();combined=b''.join((R/x['path']).read_bytes() for x in chunks);assert combined==raw and sum(x['rows'] for x in chunks)==len(lines)
 for x in chunks:assert x['bytes']<=1000000
 journals.append(dict(lane=lane,original_path=src.relative_to(R).as_posix(),original_bytes=len(raw),original_sha256=sha(raw),rows=len(lines),chunks=chunks,concatenation='Literal concatenation of chunks in listed order reconstructs every original byte and newline; no JSON rewriting, row omission or compression.'))
write(P/'JOURNAL_MANIFEST.json',dict(status='PASS_ALL3_BYTE_EXACT_JOURNAL_RECONSTRUCTIONS',max_chunk_bytes=1000000,journals=journals,qualification='All rows individually parse and are available in bounded scanable JSONL chunks. Original large journals physically preserved and previous tracked originals immutable on Q.'))
qresult=read(R/'tmp/portable_job_qa_q_remote_v400/RESULT.json');assert qresult['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and qresult['revision']==BASE
shutil.copyfile(R/'tmp/portable_job_qa_q_remote_v400/RESULT.json',P/'PREVIOUS_Q_REMOTE_RESULT.json')
removed=[archive.relative_to(R).as_posix(),sources[0][1].relative_to(R).as_posix(),sources[1][1].relative_to(R).as_posix()]
for rel in removed:
 raw=(R/rel).read_bytes();assert raw==git('show','HEAD:'+rel)
git('rm','--cached','--quiet','--pathspec-from-file=-','--pathspec-file-nul',data=b''.join(p.encode()+b'\0' for p in removed))
write(P/'REPLACED_PATHS.json',dict(status='REPLACED_IN_CURRENT_INDEX_PHYSICAL_ORIGINALS_PRESERVED',baseline=BASE,paths=removed,all_original_bytes_physically_preserved=True,all_original_revision_urls_reachable=True,qualification='Previous immutable maps retain exact original Q/P/O meaning; next current map substitutes only these files with flat member/shard manifests. No revision history rewritten.'))
snapshot=read(R/'audit/job_geode_current_recheck_v1_20261002/SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files'];assert len(snapshot)==783
checked=[dict(path=x['path'],sha256=sha((R/x['path']).read_bytes()),matches=sha((R/x['path']).read_bytes())==x['sha256']) for x in snapshot];assert all(x['matches'] for x in checked)
write(P/'BOUNDARY_UNCHANGED.json',dict(status='ALL783_LITERAL_SOURCE_BYTES_UNCHANGED',members=checked))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
attrs=R/'.gitattributes';attrs.write_bytes(attrs.read_bytes()+b'\naudit/job_qa_scan_v2_20261002/** -text\n')
lic=R/'ASSET_LICENSES.md';lic.write_bytes(lic.read_bytes()+b'\n| `audit/job_qa_scan_v2_20261002/cache/**` | Original Godot4.7.2 isolated QA cache/log files | Inherited generated diagnostic provenance; Godot MIT engine | CACHE_MANIFEST.json exact original P and Q archive hashes | Byte-identical short flat files only; no runtime asset, compression, hidden model or added 3D resource. |\n')
note='QA scanability continuation (2026-10-02): [428 exact short flat files and lossless bounded journal chunks](job_qa_scan_v2_20261002/index.html) supersedes the oversized current ZIP/journals. Hosted Q Windows checkout/area-music passed; 2D model audit correctly stopped on scan budgets before later probes. All original bytes/hashes/revisions and failures preserved, current783 source bytes unchanged. Existing validator/ceiling/workflow remain unchanged; fresh staged no-regression/authority/coverage/hosted gates required. No visual/action/owner or integration/release acceptance. [Impact](../design/audit_impacts/job-qa-scanability-20261002.json).'
master=R/'audit/MASTER_AUDIT_2026-08-09.md';s=master.read_text(encoding='utf-8');s=s.replace('## 0. Planning entry\n','## 0. Planning entry\n\n'+note+'\n',1).replace('### Development task index\n','### Development task index\n\n'+note+'\n',1);master.write_text(s,encoding='utf-8',newline='\n')
ledger=R/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8');rows=[x for x in s.splitlines() if '`audit/job_qa_portable_v1_20261002/index.html`' in x];write(P/'PREVIOUS_LEDGER_ROWS.json',dict(rows=rows));s=s.replace(rows[0],rows[0].replace('SUPPORTING_CURRENT','SUPPORTING_HISTORICAL').rstrip().rstrip('|')+' Hosted Q Windows job passed; 2D probe job stopped at oversized archive/journal scan caps. See current bounded package. |') if rows else s;s+='\n| `audit/job_qa_scan_v2_20261002/index.html` | 🔵 | `SUPPORTING_CURRENT`; unchanged428 short flat QA files and exact line-boundary chunks of all3 remote journals. Previous ZIP/large journals/historical revisions/failures preserved. Corrected staged unchanged 2D gate and fresh hosted checks required; current783 source bytes/artwork opinions unchanged. No debt-ceiling growth, validator waiver or creative/device/child/owner/all-job/integration/release acceptance. |\n';ledger.write_text(s,encoding='utf-8',newline='\n')
oldindex=Q/'index.html';oldraw=oldindex.read_text(encoding='utf-8');(P/'Q_INDEX_BEFORE_SCANABILITY.original.html').write_bytes(oldindex.read_bytes());oldraw=oldraw.replace('href="nursery_process.zip"','href="https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+BASE+'/audit/job_qa_portable_v1_20261002/nursery_process.zip"').replace('Corrected hosted CI remains pending.','Hosted Q Windows checkout/music passed; its 2D gate stopped on bounded scan limits in the oversized ZIP/journals. See the current <a href="../job_qa_scan_v2_20261002/index.html">flat files and journal chunks</a>. Fresh hosted validation remains required.');oldindex.write_text(oldraw,encoding='utf-8',newline='\n')
(P/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Scanable job QA evidence</title><style>body{font:18px system-ui;max-width:1050px;margin:36px auto;padding:0 20px;background:#f2f5fa;color:#253449}</style><h1>Complete inspectable QA evidence</h1><p>All428 generated QA cache/log files are now separately available at short paths. All3 complete remote-verification journals are split at exact line boundaries into chunks under1MB; concatenation reconstructs every original byte. No compression, omitted row, gate change or increased 3D-debt ceiling.</p><p>Hosted Q Windows checkout and music verification passed. Its 2D gate correctly stopped on the old package scan budgets; the complete failure remains recorded. Current783 source bytes and all artwork/action scores remain unchanged. Fresh staged and hosted gates are required.</p><ul><li><a href="CACHE_MANIFEST.json">Every428 original/current file and hash</a></li><li><a href="JOURNAL_MANIFEST.json">All journal chunks, rows and reconstruction hashes</a></li><li><a href="HOSTED_Q_COMPLETED.json">Exact Q hosted jobs</a></li><li><a href="HOSTED_Q_FAILURE_EXCERPT.log">Preserved 2D scan-budget failure</a></li><li><a href="PREVIOUS_Q_REMOTE_RESULT.json">Q anonymous remote verification</a></li><li><a href="BOUNDARY_UNCHANGED.json">All783 source bytes unchanged</a></li><li><a href="../job_geode_current_recheck_v1_20261002/index.html">Illustrated Geologist review</a></li><li><a href="../job_artwork_refinement_live/all_items.html">Individual artwork library</a></li></ul><p>Local82/82 source-bound machine evidence remains separate. Visual/action, device, child, owner, all-job and release acceptance remain open.</p></html>',encoding='utf-8',newline='\n')
d=read(ip);d['files']=sorted(set(removed)|{p.relative_to(R).as_posix() for p in P.rglob('*') if p.is_file()}|{'.gitattributes','ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md',oldindex.relative_to(R).as_posix()});write(ip,d)
print('SCANABLE_QA_PREPARED|428 flat exact files|3 exact full journals|bounded line chunks|783 sources unchanged|validator unchanged')
