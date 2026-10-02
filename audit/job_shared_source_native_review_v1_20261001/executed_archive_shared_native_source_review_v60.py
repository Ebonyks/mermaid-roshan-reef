from pathlib import Path
import datetime, hashlib, html, json, shutil, subprocess
from PIL import Image

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_shared_source_native_review_v1_20261001'
assert not out.exists()
out.mkdir();(out/'.gdignore').write_text('',encoding='utf-8')
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
ip=r/'design/audit_impacts/job-shared-native-source-review-20261001.json'
impact={'id':'job-shared-native-source-review-20261001','scope':'Direct review of8 previously unassigned shared source images: every88 Roshan atlas region and6 already catalogued pool prop regions. Retain originals, exact hashes, native source opinions and qualified literal-reference evidence. Add all88 Roshan regions to the refreshable library; do not imply the legacy/unreferenced sheets are current job pixels or accept whole actions.','baseline':baseline,'rules':['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-03','DL-ASSET-04','DL-ASSET-06','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08','DL-READ-01','DL-QA-03'],'findings':['MA-VIS-006'],'files':['ASSET_LICENSES.md'],'validation':[{'command':'Direct full-native individual source/region review','result':'PENDING','evidence':'Every source viewed, written record being archived; current job use, mounted scale and complete actions remain separate.'}],'acceptance_gaps':'No production source changes, sequence/gesture contact/loop, every active job binding, target-device, child, owner, strict2D or global4.5 acceptance.'}
write(ip,impact)
poses={
 'roshan_gesture_c.png':[
  'Open arms introduce the collect gesture.','Both arms reach forward with intact shoulders and wrists.','Cupped hands move toward the torso; no carried object is supplied.','Hands meet at the chest in a small waiting clasp.',
  'Arms lower beside the body before the boing accent.','The tail curls inward and the body lowers into a compact anticipation pose.','Both arms rise in an open upward accent.','Arms return outward and down toward a calm posture.',
  'Quiet neutral start for the hair-twirl row.','One hand rises behind the near-side hair while the other stays down.','A small lock is held near the face with a connected forearm.','The hand lowers and the familiar upright silhouette returns.',
  'Hands clasp near the chest with eyes open.','Closed eyes and a gentle smile form the first humming still.','Closed eyes persist while the tail curves inward.','The clasp remains and the tail relaxes toward the opening silhouette.'
 ],
 'roshan_gesture_d.png':[
  'Upright open-mouth start for the flop row.','One arm lifts and the other opens during a diagonal body lean.','Broad diagonal flourish with two raised attached arms and the tail extended across the cell.','The child settles into a gentler tilted upright pose.',
  'Both arms extend down and outward before carrying.','Two palms gather in front of the chest; no held object is baked in.','Palms rise and face upward in a clear offering/receiving shape.','Two connected palms remain gathered; this still does not prove an object handoff.'
 ],
 'roshan_gestures.png':[
  'One raised arm waves with an open hand.','Two attached arms reach upward in a cheer.','Hands clasp at the chest, eyes open.','Arms spread while the tail curls broadly to the side.',
  'One hand rests near the cheek in an attentive looking pose.','Closed eyes and hands near the mouth express giggling.','Closed eyes, joined hands and a curved tail express resting.','One arm points horizontally while the other remains relaxed.',
  'Both arms extend together to reach in front.','Both open palms rise beside an alert face.','One hand approaches the cheek while the other gestures outward.','Closed eyes and a small clasp give a calm humming still.',
  'The whole drawn pose leans broadly with both arms extended.','Both arms lift toward one side during the flourish.','Hands grasp a small horizontal ride/grip bar in a seated tail pose; unsuitable as empty washing hands.','The familiar upright resting silhouette returns.'
 ],
 'roshan_play.png':[
  'Seated curled tail with two raised grip fists.','Body turns to the side while both attached arms rise.','Open raised arms and a long tail create an upward accent.','Arms lower into a familiar upright rest.',
  'Body leans down with one reaching hand and the other arm behind.','A second deeper reaching still keeps both shoulders attached.','Seated tail and two hands around the small horizontal ride/grip bar.','Arms spread in a seated balancing pose.'
 ],
 'roshan_play_a.png':[
  'Compact seated swing pose with two raised grip fists.','Seated pose and fists persist with a small facial/tail variation.','The tail lengthens while the raised grip fists remain.','The seated tail curls again beneath the same gesture.',
  'Both arms reach forward from a compact crouched tail.','Arms reach upward and forward during a body lift.','Both hands rise nearly overhead with the tail extending down.','Arms return forward while the tail curls into a seated shape.',
  'Both hands grip a small horizontal bar while the body leans forward.','A second leaning grip pose lengthens the tail curve.','Both arms lift in a clear open upward accent.','The upward accent continues with a slightly longer tail.',
  'Both hands are raised in an open landing celebration.','Arms spread to the sides for balance.','Closed eyes and chest-level hands provide a small delighted accent.','Arms lower and the figure returns to an upright resting pose.'
 ],
 'roshan_play_b.png':[
  'Upright preparatory pose facing the left-reaching direction.','One connected arm reaches down while the body leans forward.','The body leans more deeply and the reaching hand lowers.','One hand returns toward the torso while the other remains down.',
  'Opposite-facing preparatory pose with corresponding tail direction.','The mirrored reaching arm extends down as the body leans.','The reverse-facing body lowers into a deeper reach.','The hand returns toward the torso in the reverse-facing pose.',
  'Seated curled tail and two raised fists define the seat row.','The seated fists remain with a small tail/facial change.','The seated body rises and the tail lengthens.','The compact seated silhouette returns.',
  'The hop row begins in a seated fists-up pose.','The body leans forward into an anticipation pose.','Both arms lift and the tail lengthens for the upward accent.','The child returns to a seated fists-up still.'
 ],
 'roshan_swim.png':[
  'Front-facing relaxed swim preparation with arms lowered.','Both arms rise diagonally in the front-facing swim row.','Arms spread horizontally and the tail bends.','Arms sweep back in a forward-leaning front-facing still.',
  'Back-facing swim preparation with the rainbow forelock and hair visible.','Both arms rise diagonally in the back-facing row.','Arms spread and the back-facing tail bends.','Arms sweep back in the final back-facing still.'
 ]}
production_bound={'roshan_gesture_c.png':'scripts/player.gd:101, collect/boing/hairtwirl/hum rows','roshan_gesture_d.png':'scripts/player.gd:102, flop/carry rows','roshan_play_a.png':'scripts/player.gd:103, swing/climb/ride/land rows','roshan_play_b.png':'scripts/player.gd:104, dig_l/dig_r/seat/hop rows'}
common='The familiar child face, tiara, brown curls/rainbow forelock, lavender-pink bodice, iridescent lavender tail and paired rainbow fin remain drawn, high-key and identifiable. Full-body contours and transparent cell margins are intact. Small fingers and detailed tail highlights require an in-game phone-size check; native art quality is not motion/contact acceptance.'
sources=[];cells=[]
for sheet,descriptions in poses.items():
    path='assets/characters/roshan_25d/'+sheet;file=r/path;digest=sha(file);dimensions=list(Image.open(file).size)
    assert dimensions==[1024,256*(len(descriptions)//4)]
    bound=sheet in production_bound
    binding=production_bound.get(sheet,'No exact literal runtime reference found in scripts/scenes. Legacy combined sheet remains preserved; dynamic use and actual job presence not proved.')
    row={'path':path,'sha256':digest,'dimensions':dimensions,'source_score':4.6,'direct_full_native_review':True,'regions_reviewed':len(descriptions),'evaluation':common,'literal_reference_evidence':binding,'live_job_pixels_proved':False,'qualification':'All individual cells inspected within the original-size full native sheet. Still-source opinion only; current job visibility, sequence/contact/loop/device/child/owner acceptance remain open.'}
    sources.append(row)
    for n,description in enumerate(descriptions):
        cells.append({'id':'SHARED-'+sheet.removesuffix('.png').upper()+'-%02d'%n,'kind':'pose cell','path':path,'sha256':digest,'region':[256*(n%4),256*(n//4),256,256],'source_score':4.6,'direct_individual_region_review_in_native_sheet':True,'evaluation':description+' '+common,'literal_reference_evidence':binding,'current_mounted_score':None,'current_complete_action_score':None,'qualification':row['qualification']})
assert len(cells)==88
poolpath='assets/castle/day_one_pool/activities/refinement_v2/floating_trash_atlas.png';poolsha=sha(r/poolpath)
pooldescriptions=[
 'Pink star wrapper has a complete crumpled silhouette, broad magenta/cream facets and navy/plum contour; the lime dirt patch reads distinctly.',
 'Open metal can has a wide elliptical rim and few blue-grey value bands; lime dirt patches communicate grime without tiny noisy detail.',
 'Blue bottle cap has one clear circular cavity, broad rim/ridges and grouped green grime; its silhouette is intact.',
 'Existing orange leaf keeps its authored warm outline, broad vein branches and selective wet droplets. White/aqua compositing confirms the apparent rectangular dark background is alpha0 hidden RGB, not visible delivery pixels.',
 'Purple ribbon curls into one readable open S silhouette with broad lavender shadow bands and sparse green grime.',
 'Yellow sponge has a simple rounded block silhouette, grouped pores and broad lime patches. The distinct yellow mass stays readable against the other props.'
]
poolitems=[]
for n,description in enumerate(pooldescriptions):
    poolitems.append({'id':'SHARED-POOL-TRASH-%02d'%n,'kind':'prop region','path':poolpath,'sha256':poolsha,'region':[341*(n%3),341*(n//3),341,341],'source_score':4.6,'evaluation':description,'direct_individual_region_review_in_native_sheet':True,'literal_reference_evidence':'scripts/games/pool_skimmer_activity.gd:14; six341px cells, count6','current_mounted_score':None,'current_complete_action_score':None,'qualification':'Native source and full native white/aqua alpha views directly inspected. Earlier mounted/action review remains separately qualified; no new action acceptance.'})
sources.append({'path':poolpath,'sha256':poolsha,'dimensions':[1024,1024],'source_score':4.6,'direct_full_native_review':True,'regions_reviewed':6,'evaluation':'All six distinct props retain complete painted contours and child-readable colour masses. The original wet orange leaf is deliberately retained; its dark source rectangle and white unused atlas padding are transparent hidden RGB. Two full-size white/aqua composites confirm no visible rectangular plate. No source pixels were repaired or regenerated.','literal_reference_evidence':'scripts/games/pool_skimmer_activity.gd:14; six341px cells, count6','live_job_pixels_proved':False,'qualification':'Whole-source still opinion based on all6 regions, not an average granting rendered composition or whole-action acceptance.'})
for name in ['pool_atlas_white.png','pool_atlas_aqua.png']:
    shutil.copyfile(r/'tmp/shared_source_native_review_v60'/name,out/name)
write(out/'ALPHA_INSPECTION.json',{'source':poolpath,'sha256':poolsha,'sampled_alpha0_positions':[[0,341],[30,360],[335,360],[0,681],[30,675],[340,681],[0,700],[500,800]],'observed_rgba':[[64,43,56,0],[79,48,59,0],[16,13,17,0],[1,1,1,0],[0,0,0,0],[7,5,4,0],[255,255,255,0],[255,255,255,0]],'direct_neutral_views':['pool_atlas_white.png','pool_atlas_aqua.png'],'qualification':'These samples and direct neutral views distinguish hidden RGB from visible background. Native source unchanged; no wider alpha/device claim.'})
review={'status':'ALL8_NATIVE_SOURCES_AND94_REGIONS_DIRECTLY_REVIEWED','baseline':baseline,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':sources,'cells':cells,'pool_regions':poolitems,'source_files_unchanged':all(sha(r/x['path'])==x['sha256'] for x in sources),'source_floor':4.6,'unreviewed_regions_in_this_batch':0,'qualification':'Seven shared Roshan sheets and one packed pool sheet.88 pose cells and6 previously catalogued pool regions are individual native still opinions only. Literal references are bounded source evidence, not actual played job visibility. No new regeneration, runtime change, sequence/gesture/contact/device/child/owner or global acceptance.'}
write(out/'REVIEW.json',review);shutil.copyfile(__file__,out/'executed_archive_shared_native_source_review_v60.py')
sections=[]
for x in sources:
    rows=[v for v in (cells+poolitems) if v['path']==x['path']]
    cards=''.join('<article id="'+v['id']+'"><h3>'+v['id']+'</h3><div class="cell" role="img" aria-label="'+html.escape(v['id'])+'" style="width:'+str(v['region'][2])+'px;height:'+str(v['region'][3])+'px;background-image:url(../../'+v['path']+');background-size:'+str(x['dimensions'][0])+'px '+str(x['dimensions'][1])+'px;background-position:-'+str(v['region'][0])+'px -'+str(v['region'][1])+'px"></div><p>Source'+str(v['source_score'])+'/5 · exact region'+str(v['region'])+'</p><p>'+html.escape(v['evaluation'])+'</p></article>' for v in rows)
    sections.append('<section><h2>'+html.escape(x['path'])+'</h2><p>Source4.6/5 · '+str(x['regions_reviewed'])+' individually reviewed regions.</p><p>'+html.escape(x['literal_reference_evidence'])+'</p><p>'+html.escape(x['evaluation'])+'</p><a href="../../'+x['path']+'"><img class="sheet" loading="lazy" src="../../'+x['path']+'" alt="'+html.escape(x['path'])+'"></a><div class="grid">'+cards+'</div></section>')
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shared job sources:8 native sheets and94 regions</title><style>body{margin:0;font:18px/1.55 system-ui;background:#edf4fa;color:#253447}main{max-width:1260px;margin:auto;padding:24px}header,section,article{background:white;padding:20px;border-radius:20px;margin-bottom:20px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:16px}article{background:#f0f4fa;min-width:0}.sheet{display:block;max-width:100%;height:auto}.cell{background-repeat:no-repeat;background-color:#d0f0f2;max-width:none}p,a,h2,h3{overflow-wrap:anywhere}</style><main><header><h1>Shared artwork:8 source sheets,94 individual regions</h1><p>Every88 Roshan cell and6 pool prop region directly inspected within complete native images. These source-only opinions are4.6/5; current mounted and complete action scores remain unassigned.</p><p><a href="REVIEW.json">Every written evaluation and exact hash</a> · <a href="ALPHA_INSPECTION.json">Pool transparency evidence</a> · <a href="../job_artwork_refinement_live/all_items.html">Searchable register</a></p><p>'+html.escape(review['qualification'])+'</p></header>'+''.join(sections)+'<section><h2>Pool alpha inspection</h2><p>Transparent hidden RGB is preserved; these neutral inspection views show the actual alpha composition.</p><img class="sheet" src="pool_atlas_white.png" alt="Full native pool source on white"><img class="sheet" src="pool_atlas_aqua.png" alt="Full native pool source on aqua"></section></main></html>'
(out/'index.html').write_text(page,encoding='utf-8',newline='\n')
lic=r/'ASSET_LICENSES.md';s=lic.read_text(encoding='utf-8')
for name in ['pool_atlas_white.png','pool_atlas_aqua.png']:
    rel=(out/name).relative_to(r).as_posix();assert rel not in s;s+='\n| '+rel+' | Existing packed pool source; Codex2026-10-01 | Diagnostic source review; underlying provenance retained | Full native alpha composited on neutral field for inspection only | Native source unchanged; no runtime/action/owner acceptance. |\n'
lic.write_text(s,encoding='utf-8',newline='\n')
impact['files']=sorted(set(impact['files'])|{p.relative_to(r).as_posix() for p in out.rglob('*') if p.is_file()});impact['validation']=[{'command':'Individual direct native source/region review and neutral alpha inspection','result':'PASS','evidence':(out/'REVIEW.json').relative_to(r).as_posix()+';8 exact sources,88 cells and6 prop regions; source-only4.6, unchanged originals. No complete-action pass.'}];write(ip,impact)
allow=r/'tmp/v2_preview_allowed.json';allowed=set(json.loads(allow.read_text(encoding='utf-8')));allowed.update(impact['files']);allowed.update(x['path'] for x in sources);write(allow,sorted(allowed))
print(json.dumps({'status':review['status'],'source_files':len(sources),'pose_cells':len(cells),'pool_regions':len(poolitems),'source_edits':False,'sequence_acceptance':None}))
