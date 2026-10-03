from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'audit/day_one_unassigned_sources_v3_20261002'
BASE='ea9f4e00a2af67fc6f81e16a2102754892a18cfd'
assert not P.exists()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==BASE
d=json.loads((R/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8-sig'))
rows=[x for x in d['items'] if x['id'] in ['D1V2-%04d'%i for i in range(1,9)]]
assert len(rows)==8 and all(x['kind']=='source' and x.get('current_source_score') is None and not x['protected_original'] for x in rows)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for x in rows:assert sha(R/x['path'])==x['current_checkout_sha256']
def write(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
P.mkdir();(P/'review_tools').mkdir();(P/'.gdignore').write_text('',encoding='utf-8')
scope='Direct individual first-pass source review of eight previously unreviewed Day One discovery candidate graphics. Record native appearance, child readability, medium/style fit and named refinement gaps with literal hashes. Discovery dependency does not prove job use or mounted/action quality. No source modification, protected-original change, generation or runtime binding.'
rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-QA-01','DL-QA-03','DL-QA-06','DL-QA-07']
plan=dict(status='PLANNED_BEFORE_SOURCE_OPINIONS',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline=BASE,scope=scope,rules=rules,findings=['MA-VIS-006'],inventory=[dict(id=x['id'],path=x['path'],sha256=x['current_checkout_sha256'],dimensions=x['source_dimensions'],current_source_score=None,provenance=x.get('original_reports'),protected_original=False) for x in rows],required_evidence=['All eight full native originals directly inspected individually','Per-source written score/evaluation/refinement and original literal hash','Illustrated individual source page and exact live-register history before updates','Discovery/source/mounted/action/device/child/owner claims separated','All783 actual production source bytes unchanged','Required authority/coverage/2D gates and immutable remote bytes'])
write(P/'PLAN.json',plan)
ip=R/'design/audit_impacts/job-unassigned-source-eight-20261002.json'
assert not ip.exists()
write(ip,dict(id='job-unassigned-source-eight-20261002',scope=scope,baseline=BASE,rules=rules,findings=['MA-VIS-006'],files=[(P/'PLAN.json').relative_to(R).as_posix()],validation=[dict(command='Eight full-native individual first-pass source reviews',result='PENDING',evidence=(P/'PLAN.json').relative_to(R).as_posix())],acceptance_gaps='Sources pending direct review. Current candidate dependency discovery does not establish actual job use, mounted scale, action sequencing, device/child/owner or comprehensive all-job acceptance. Existing originals and all783 production source bytes preserved.'))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
print('SOURCE_REVIEW_PLANNED|8 unreviewed native sources|source-only|no production edits')
