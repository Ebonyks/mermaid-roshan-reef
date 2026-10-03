from pathlib import Path
import datetime,hashlib,json,shutil
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';G=P/'gates_v2';IP=B/'design/audit_impacts/job-candy-shared-library-continuation-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['run_review_gate_v571.py','freeze_review_gate_source_v571.py']:shutil.copyfile(Path(__file__).parent/name,P/'review_tools'/name)
d=read(IP);d['files']=sorted(set(d['files'])|{(P/'review_tools'/x).relative_to(B).as_posix() for x in ['run_review_gate_v571.py','freeze_review_gate_source_v571.py']}|{(G/'CANDIDATE_REVIEW_SOURCE_V571.json').relative_to(B).as_posix()})
members=[dict(path=path,bytes=(B/path).stat().st_size,sha256=sha(B/path)) for path in d['files'] if not path.startswith(G.relative_to(B).as_posix()+'/') and (B/path).is_file()]
(G/'CANDIDATE_REVIEW_SOURCE_V571.json').write_text(json.dumps(dict(status='EXACT_REVIEW_SOURCE_SNAPSHOT_BEFORE_GATES',frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline=d['baseline'],members=members,excluded='Self-changing gate receipts/logs and self-describing impact records; all783 production members independently bound by PRODUCTION_BOUNDARY_END_V565.json.',qualification='No art/action/owner acceptance.'),indent=2)+'\n',encoding='utf-8',newline='\n')
n=IP.with_name(IP.name+'.v571_next');n.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');n.replace(IP);print('FROZEN_REVIEW_MEMBERS',len(members))
