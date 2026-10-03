from pathlib import Path
import datetime, hashlib, json, re, shutil, subprocess
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'audit/job_shared_background_review_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert not P.exists();P.mkdir();(P/'review_tools').mkdir()
baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip();assert baseline=='ae3880df4244139a4f681034b530a5ee2c68895d'
registry=read(B/'audit/job_artwork_refinement_live/ALL_ITEMS.json')
rows=[dict(id=x['id'],aliases=x['aliases'],path=x['path'],sha256=sha(B/x['path']),dimensions=x['source_dimensions'],families=x['families'],prior_score=x['current_source_score'],status='DIRECT_SOURCE_REVIEW_PENDING') for x in registry['items'] if x['kind']=='source' and x['current_source_score'] is None and 'Day Two' in x['families']]
assert len(rows)==65
selected=[x for x in rows if '/background_tiles/room_kitchen_background_' in x['path']];assert len(selected)==12
write(P/'PENDING_DAY_TWO_SHARED_SOURCES.json',dict(baseline=baseline,inventory_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),count=65,items=rows,qualification='All65 inventory omissions remain pending until each native source is directly seen. Shared job-room sources, not new artwork or current mounted acceptance.'))
write(P/'PLAN.json',dict(baseline=baseline,scope='Audit all remaining65 shared Day Two primary-source omissions, starting with all12 Kitchen room tiles; preserve individual source IDs, hashes, exact source opinions, joined composition/seam evidence and later actual use/action qualification. No production art mutation or speculative redraw.',relevant_rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-07','DL-LAY-01','DL-LAY-03','DL-LAY-05','DL-LAY-06','DL-LAY-07','DL-QA-03','DL-QA-07'],related_findings=['MA-VIS-006'],required_evidence=['Direct native whole source inspection for each item with individual drafting score and refinement','Every Kitchen tile and exact join context seen; known row/column edges conserved','Source/crop/seam quality distinct from native per-screen coverage, current room mounting and whole action acceptance','Refresh exact registered source bytes without inventing new source counts or finding lifecycle changes'],selected_items=selected,owner_acceptance=None))
# QA-only reconstruction of unchanged tiles. No resampling, repainting or delivery pixels.
joined=Image.new('RGB',(4096,2304));join_rows=[]
for x in selected:
    m=re.search(r'_r(\d+)_c(\d+)\.png$',x['path']);rr,cc=map(int,m.groups())
    with Image.open(B/x['path']) as im:
        assert im.size==(1024,768);joined.paste(im.convert('RGB'),(cc*1024,rr*768))
    join_rows.append(dict(x,row=rr,column=cc))
joined.save(P/'KITCHEN_UNCHANGED_NATIVE_QA_JOIN.png')
write(P/'KITCHEN_QA_JOIN.json',dict(dimensions=[4096,2304],sha256=sha(P/'KITCHEN_UNCHANGED_NATIVE_QA_JOIN.png'),sources=join_rows,qa_only=True,resampled=False,production_pixels=False,qualification='Unchanged source pixels assembled at literal row/column offsets for seam/context inspection only; does not prove source-master provenance or per-playable-screen native coverage.'))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-shared-background-source-review-20261003.json';plan=read(P/'PLAN.json')
write(ip,dict(id=ip.stem,scope=plan['scope'],baseline=baseline,rules=plan['relevant_rules'],findings=plan['related_findings'],files=sorted(x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()),validation=[dict(command='Literal65-item remaining Day Two source inventory and full Kitchen QA reconstruction',result='PASS',evidence='PENDING_DAY_TWO_SHARED_SOURCES.json and KITCHEN_QA_JOIN.json; no scores assigned before inspection.'),dict(command='Direct every selected native source and joined seam/shape/material context',result='PENDING',evidence='All12 Kitchen source opinions and65 total inventory gaps remain explicitly pending.')],acceptance_gaps='Source-only review; runtime use/contact/layers, per-screen native source coverage, ordinary story/training/device/child/owner/all-job acceptance and existing finding lifecycle remain open. No production art or protected originals changed.'))
print('65 shared Day Two omissions frozen; all12 unchanged Kitchen tiles ready for direct native review.')
