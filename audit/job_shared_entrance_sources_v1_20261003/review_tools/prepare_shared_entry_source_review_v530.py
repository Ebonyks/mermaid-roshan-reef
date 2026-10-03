from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');q=b/'audit/job_shared_entrance_sources_v1_20261003';assert not q.exists();q.mkdir();(q/'.gdignore').write_text('',encoding='utf-8');(q/'review_tools').mkdir()
reg=json.loads((b/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8'));ids=['D2X-'+f'{n:04d}' for n in [1,2,3,4,5,6,7,10,11,24,25,26,27,28,29,30,31,140]]
items=[next(x for x in reg['items'] if x['id']==ident) for ident in ids];assert len(items)==18 and all(x['current_source_score'] is None for x in items)
ownership=b/'assets_src/castle/room_backgrounds_2k/castle_live_alpha_baseline_repair.json';d=json.loads(ownership.read_text(encoding='utf-8'));bindings={}
def walk(x):
 if isinstance(x,dict):
  if x.get('sheet') and x.get('grid') and x.get('frame_count'):bindings[x['sheet']]=x
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(d);rows=[]
for item in items:
 p=b/item['path'];raw=p.read_bytes();im=Image.open(p);h=hashlib.sha256(raw).hexdigest();assert h==item['current_checkout_sha256']
 binding=bindings.get(item['path']);cells=[]
 if binding:
  assert binding['sheet_sha256']==h;cols,rr=binding['grid'];assert im.width%cols==0 and im.height%rr==0
  for i in range(binding['frame_count']):cells.append({'index':i,'region':[(i%cols)*(im.width//cols),(i//cols)*(im.height//rr),im.width//cols,im.height//rr],'status':'DIRECT_REVIEW_PENDING'})
 rows.append({'id':item['id'],'path':item['path'],'sha256':h,'bytes':len(raw),'dimensions':list(im.size),'mode':im.mode,'cells':cells,'existing_source_binding':binding,'source_review_status':'PENDING','source_score':None,'source_scope':'Existing whole native source and each authored cell; independent from mounted use or complete action.'})
assert sum(len(x['cells']) for x in rows)==104
snapshot={'status':'PLANNED_NATIVE_SOURCE_AND_AUTHORED_CELL_REVIEW','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=b,text=True).strip(),'source_files':rows,'source_count':18,'authored_cells':104,'source_ownership_reference':{'path':ownership.relative_to(b).as_posix(),'sha256':hashlib.sha256(ownership.read_bytes()).hexdigest()},'production_change':False,'qualification':'Shared Kitchen and Opera entrance originals already in known register. Source grids and binding metadata read only; no original modification or new generated artwork. Every18 native source and104 cell requires direct visual review before grading. No current mounted/action/device/child/owner or true2D whole-game acceptance.'}
(q/'PLAN_AND_SOURCE_BOUNDARY.json').write_text(json.dumps(snapshot,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');shutil.copyfile(__file__,q/'review_tools/prepare_shared_entry_source_review_v530.py')
impact={'id':'job-shared-entrance-source-review-20261003','scope':'Complete18 outstanding shared Kitchen/Opera entry native source reviews and individually inspect all104 authored atlas cells. Reuse exact original pixels and existing grid/source-ownership contracts; no new artwork, binding or production change. Add individual written drafting opinions and illustrated library entries without transferring source scores to complete interaction/route/device/owner acceptance. Preserve previous register and all rejected candidate history.','baseline':snapshot['baseline'],'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-MOT-01','DL-MOT-02','DL-MOT-03','DL-MOT-07','DL-ASSET-01','DL-ASSET-03','DL-ASSET-05','DL-ASSET-06'],'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'files':sorted(p.relative_to(b).as_posix() for p in q.rglob('*') if p.is_file()),'validation':[{'command':'Directly inspect all18 full native sources and104 authored cells','result':'PENDING','evidence':'audit/job_shared_entrance_sources_v1_20261003/PLAN_AND_SOURCE_BOUNDARY.json; no grades before review'}],'acceptance_gaps':'Source/cell review pending. Actual shared entrance and interaction ownership, motion, sequencing, ordinary route, target-device/child/owner and full all-job acceptance stay separate. Current game still contains measured3D mounting debt; source review cannot accept that medium. Existing Candy one-file station repair remains the only production delta from U, outside this source-only review. Finding lifecycle states unchanged.'}
(b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json').write_text(json.dumps(impact,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Planned18 existing natives and104 exact authored cells. No assets generated or modified.')
