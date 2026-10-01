from pathlib import Path
import hashlib, json, shutil
from PIL import Image

root=Path(__file__).resolve().parents[1]
family=root/'audit/day_one_pool_live_refinement_v2_20261001'
folder=family/'actor_reuse_inventory_v1'
assert not folder.exists(),'Preserve prior reuse inventory.'
folder.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selections=[('gesture_c',1,'two_open_reaching_hands'),('gesture_c',2,'cupped_collect_hands'),
 ('gesture_d',5,'supported_carry_hands'),('play_a',8,'closed_grasp_ride_a'),('play_a',9,'closed_grasp_ride_b')]
rows=[]
for sheet,index,role in selections:
 src=root/f'assets/characters/roshan_25d/roshan_{sheet}.png'
 with Image.open(src) as image:
  image=image.convert('RGBA');box=(index%4*256,index//4*256,(index%4+1)*256,(index//4+1)*256)
  cell=image.crop(box);dst=folder/f'{sheet}_{index:02d}_exact_source_window.png';cell.save(dst)
  rows.append({'path':dst.relative_to(root).as_posix(),'sha256':sha(dst),'source':src.relative_to(root).as_posix(),
   'source_sha256':sha(src),'source_region':list(box),'role':role,'modification':'Exact approved256px RGBA source window only; no painting, anatomy change, subject transform or runtime binding.',
   'visual_score':None,'hand_socket':None,'status':'PENDING_INDIVIDUAL_REUSE_PURPOSE_REVIEW'})
inventory={'schema':'reef.pool-actor-reuse-inventory.v1','status':'PROSPECTIVE_REUSE_STUDY_NOT_RUNTIME',
 'scope':'Investigate the newly measured classic skimmer grasp gap before generating any character artwork. Approved collect/carry and closed-hand playground poses are purpose candidates, not accepted skimmer actions. Preserve authored contour, face, clothing, iridescent tail and originals.',
 'source_gap':'Current classic relaxed hand4.2, Fairy4.1/Huluu3.5 painted grips and shared static body acting3.8. Socket distance does not certify grasp.',
 'items':rows,'wardrobe_sources':[{'path':p,'sha256':sha(root/p),'purpose_gap':gap} for p,gap in [
  ('assets/characters/skins/fairy_mermaid.png','One unchanged full-body relaxed-hand source; no same-costume authored skimmer grasp pose discovered in scoped inventory.'),
  ('assets/characters/friends/huluu.png','Protected full-body folded-arm portrait; no same-costume authored skimmer grasp pose discovered in scoped inventory. Original remains unchanged.')]],
 'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-03','DL-ASSET-04','DL-VIS-01','DL-READ-05','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13'],
 'acceptance':'No pose selected yet. A source-cell reuse opinion does not establish mounted tool fit, temporal continuity, body acting, wardrobe approval, device/child/owner or global quality.'}
(folder/'INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
lic=root/'ASSET_LICENSES.md';text=lic.read_text(encoding='utf-8')
text=text.rstrip()+'\n'+'\n'.join(f'| `{r["path"]}` | Existing owner-approved Roshan RGBA atlas; original source rights retained | {r["source"]}; exact source/output SHA-256 in actor_reuse_inventory_v1/INVENTORY.json | {r["modification"]} Diagnostic purpose review only. |' for r in rows)+'\n'
lic.write_text(text,encoding='utf-8')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
impact=root/'design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json';d=json.loads(impact.read_text())
d['scope']+=' Inventory five exact approved collect/carry/closed-hand pose windows as prospective solutions to classic grip4.2 before new character generation. No runtime selection, protected-original edit or performance acceptance. Fairy/Huluu source gaps retain scoped search limits.'
d['files']=sorted(set(d['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()})
d['validation']+=[{'command':'Current focused_return_v7 and literal native action/wardrobe review','result':'PASS','evidence':'focused_return_v7/RECEIPT.json and INDEPENDENT_TRANSFER_CHECKS.json:41 independent checks; classic435 and two wide432 captures26 machine checks each. REVIEW.json attributes all433 classic action-frame direct reviews; weak actor/limited costume lanes explicitly retained.'},
 {'command':'Purpose-specific approved pose reuse and current complete actor performance','result':'PENDING','evidence':'actor_reuse_inventory_v1/INVENTORY.json; exact source windows and preserved originals, no selected/mounted/timed pose yet.'}]
d['acceptance_gaps']='Six classic prop mount/contact/carry/drop/stored lanes have4.6 drafting opinions. Whole actions4.2, body acting3.8, classic/Fairy/Huluu grip4.2/4.1/3.5 and initial actor overlap4.3 remain weak. Current wholeCI, full wardrobe sequences, continuous playback/listening, ordinary routes, remaining pool/all-job items, device/child/owner acceptance and final comprehensive report approval remain open. No finding closure/integration/release.'
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Preserved five exact approved pose windows for purpose-specific grasp reuse study. No runtime or protected-original edit.')
