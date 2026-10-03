from pathlib import Path
import json,hashlib,datetime,shutil,subprocess
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
K=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003';C=R/'audit/job_candy_workflow_current_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='c5977ebb29bb2011b20fc149ad350290f045045c'
assert not C.exists();C.mkdir();(C/'review_tools').mkdir();(C/'attempt01').mkdir()
(C/'.gdignore').write_text('',encoding='utf-8')
shutil.copyfile(Path(__file__).with_name('capture_candy_workflow_v484.gd'),C/'capture.gd')
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
baseline=read(K/'SOURCE_CURRENT_BEFORE_CAPTURE.json');assert len(baseline['source_files'])==783 and all(sha(R/x['path'])==x['sha256'] for x in baseline['source_files'])
write(C/'SOURCE_CURRENT_BEFORE_CAPTURE.json',baseline)
reg=read(R/'audit/job_artwork_refinement_live/ALL_ITEMS.json')
items=[x for x in reg['items'] if 'candymaker' in str(x.get('path','')).lower() or 'candy' in x['id'].lower()]
paths=sorted({x['path'] for x in items if x.get('path')})
paths+=['assets/chapter2/birthday/sky_lagoon_strawberry_single.png','assets/chapter2/birthday/chapter2_chef_frosted_rainbow_cake.png','assets/chapter2/birthday/chapter2_candied_strawberries_tray.png','assets/chapter2/birthday/chapter2_grand_five_strawberry_cake.png']
inventory=[]
for p in sorted(set(paths)):
 with Image.open(R/p) as im:dimensions=list(im.size)
 inventory.append({'path':p,'sha256':sha(R/p),'dimensions':dimensions,'role':'Existing source/pose/room/prop/widget inventory; current use resolved separately from capture.','provenance':'Existing ASSET_LICENSES.md row, unchanged.'})
rules=read(R/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json')['rules']
plan={'baseline':'c5977ebb29bb2011b20fc149ad350290f045045c','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rules':rules,'findings':['MA-VIS-006','MA-PLAY-004','MA-OPERA-012'],'scope':'Expand current action audit to Candy Maker: all6 normal/freeplay phases and all4 story phases reached through actual Kitchen card/input. Complete wrapping and glaze circle action at both1280/1600, selected canvases for remaining phases. Prior Farmer/Chef story completion is an explicitly isolated restored-save fixture. No production edits or inferred broader story acceptance.','named_gap':'User asks truthful visible physical action, including candy actually being wrapped. Current training crank replaces the old duplicated backdrop mover with flat candy/end polygons; story uses a distinct five-strawberry glaze action and transparent legacy input surface. Neither code nor a source score proves wrapping/glazing/contact visually.','reuse_inventory':inventory,'existing_register_items':[{'id':x['id'],'kind':x.get('kind'),'path':x.get('path')} for x in items],'route_sources':{p:sha(R/p) for p in ['scripts/castle_career_routes.gd','scripts/opera_house.gd','scripts/opera_career_world_2d.gd','scripts/opera_gesture_surface.gd','scripts/chapter_two_director.gd','scripts/chapter_two_career_scene_adapter.gd','scripts/opera_performance_plan.gd']},'production_method':'Unmodified actual runtime review capture; no image generation or substitution.','required_evidence':['Fresh parser/inference/officialGodot4.7.2 analyzer','Four actual-input captures, explicit prerequisite fixture, all phases earned and normal Kitchen returns','Every original circle sequence canvas ordered/directly reviewed; source details, individual scores and complete-action/contact opinions kept separate','All783 production source hashes unchanged; current registry counts remain source vs action distinct','Document authority/impact coverage/existing applicable gates; exact scoped GitHub publication and complete anonymous byte verification'],'owner_acceptance':None,'predicted_score':None}
write(C/'PLAN.json',plan)
impact={'task':'job-candy-workflow-current-20261003','baseline':plan['baseline'],'scope':plan['scope'],'rules':rules,'findings':plan['findings'],'files':sorted(x.relative_to(R).as_posix() for x in C.rglob('*') if x.is_file()),'validation':[{'command':'Four fresh current runtime routes and complete circle-action review','result':'PENDING','evidence':C.relative_to(R).as_posix()+'/PLAN.json'}],'acceptance_gaps':'Review capture pending. No new scores, image generation, production binding, device/child/owner/all-job acceptance or finding closure.'}
write(R/'design/audit_impacts/job-candy-workflow-current-20261003.json',impact)
print(json.dumps({'status':'CANDY_SCOPE_AND_SOURCE_INVENTORY_RECORDED','existing_images':len(inventory),'register_items':len(items),'source_files_unchanged':783,'production_edits':0}))
