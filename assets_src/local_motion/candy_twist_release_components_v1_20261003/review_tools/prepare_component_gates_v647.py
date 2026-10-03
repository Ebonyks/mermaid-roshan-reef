from pathlib import Path
import datetime,hashlib,json,re,subprocess
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_twist_release_components_v1_20261003';L=B/'audit/job_artwork_refinement_live';IP=B/'design/audit_impacts/job-candy-twist-release-components-20261003.json';G=P/'gates_v1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,raw):p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.v647_next');t.write_bytes(raw);t.replace(p)
def write(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
for rel in ['index.html','release_a1/index.html','twist_a1/index.html']:
 p=P/rel;s=p.read_text(encoding='utf-8')
 for a,b in [('the4.5','the 4.5'),('release1.7','release 1.7'),('twist2.2','twist 2.2'),('All82','All 82'),('All41','All 41'),('all41','all 41'),('and24','and 24'),('and12','and 12'),('remain4.5','remain 4.5'),('remains2.8','remains 2.8'),('All783','All 783'),('Full2152','Full 2152'),('rejected1.7','rejected 1.7'),('rejected2.2','rejected 2.2'),('separate4.4','separate 4.4'),('source4.5','source 4.5'),('endpoint4.5','endpoint 4.5'),('WRAP2.8','WRAP 2.8'),('at24fps','at 24 fps'),('graph:896','graph: 896'),('512,41','512, 41'),('24fps,24','24 fps, 24'),('mitttens','mittens')]:s=s.replace(a,b)
 put(p,s.encode())
p=P/'twist_a1/attempt01/DIRECT_REVIEW.json';d=read(p);assert d['frames'][37]['evaluation'].count('mitttens')==1;d['frames'][37]['evaluation']=d['frames'][37]['evaluation'].replace('mitttens','mittens');write(p,d)
# Freeze the exact source-only gate runner before any checks.
old=(B/'assets_src/imagegen/candy_twist_release_pose_v1_20261003/review_tools/run_endpoint_gate_v633.py').read_text(encoding='utf-8');new=old.replace('assets_src/imagegen/candy_twist_release_pose_v1_20261003','assets_src/local_motion/candy_twist_release_components_v1_20261003').replace('CANDIDATE_ENDPOINT_SOURCE_V633.json','CANDIDATE_COMPONENT_SOURCE_V647.json');put(P/'review_tools/run_component_gate_v647.py',new.encode())
put(P/'review_tools'/Path(__file__).name,Path(__file__).read_bytes())
G.mkdir();d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()}|{(G/(label+suffix)).relative_to(B).as_posix() for label in ['authority','development','document_tests','game2d','register_parts'] for suffix in ['.stdout.log','.stderr.log','.receipt.json']}|{(G/'CANDIDATE_COMPONENT_SOURCE_V647.json').relative_to(B).as_posix()});d['validation'].append(dict(command='Source-only review structural/document/2D no-regression/register gates',result='PENDING',evidence=G.relative_to(B).as_posix()+';fresh exact-source checks required.'));write(IP,d)
print('COMPONENT_GATE_RUNNER_PREPARED_BROWSER_PROOFS_AND_FINAL_SOURCE_FREEZE_PENDING',flush=True)
