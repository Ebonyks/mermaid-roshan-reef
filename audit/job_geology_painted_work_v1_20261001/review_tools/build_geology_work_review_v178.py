from pathlib import Path
import datetime, hashlib, json, html, shutil, sys, posixpath
from PIL import Image

root=Path(sys.argv[1]); family=root/'audit/job_geology_painted_work_v1_20261001'
source=root/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
rp=lambda p:p.relative_to(root).as_posix()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
base='e1b431f49258eef1d293b11a732353f0a3aa12e9'
qual='Direct native still review in actual Mobile-rendered desktop career progression. Material, composition, contact and sampled state progression are separate drafting opinions. No complete timed action, physical device, child, owner, cinematic or whole-game acceptance.'
notes={
 'river_invitation':(4.6,4.1,'The isolated layered specimen now clears Roshan and reads in three broad painted strata. Its floating position lacks a physical shelf; the layered specimen also only partly communicates the river connection task.',4.3),
 'river_task_open':(3.5,3.5,'Four angular river rows, small connection rings and a broad flat work panel remain diagram-like. The painted invitation does not repair the actual river activity.',3.5),
 'river_earned_completion':(3.8,3.8,'Connected rows gain a bright cyan water cue, but the flat zigzag bands and dots remain below the painted world language. Roshan is visibly celebrating.',3.8),
 'fossil_invitation':(4.6,4.1,'The warm spiral and lavender matrix have a readable contour at invitation scale and clear the actor. The specimen floats above a procedural station instead of resting in the room.',4.1),
 'fossil_task_open':(4.6,4.6,'The new deep ochre soil bed conceals the fossil. Broad cream stone and lavender shaded edges sit inside the slab at authored aspect; the fine soil marks are grouped near the perimeter.',4.6),
 'fossil_partial_brush':(4.6,3.9,'Painted soil is coherent and the newly exposed warm spiral is clear. Removing the first cell row creates a conspicuously straight horizontal boundary; material approval does not pass the clearing transition.',3.9),
 'fossil_brushed':(4.6,4.5,'The same fossil painting appears as three conserved vertical thirds without stretch. The pieces reach the slab front face, and their straight slice edges still feel like a cut picture rather than broken stone.',4.5),
 'fossil_one_piece':(4.6,4.5,'The first third seats in the target at the same width and height as its source partition. Unplaced thirds retain their contours; straight assembly seams and front-face support remain provisional.',4.5),
 'fossil_two_pieces':(4.6,4.5,'Two source-conserving thirds meet in the target and the spiral remains continuous. The last narrow third retains its original image; the broken-rock fiction and physical support need refinement.',4.5),
 'fossil_earned_completion':(4.6,4.6,'The three thirds reconstruct exactly one original painted fossil with a readable spiral and continuous lavender rim. Roshan is visible in celebration. This endpoint does not approve the entire assembly action.',4.6),
 'pan_invitation':(4.6,4.1,'The shallow lavender basin and aqua water stay legible at the invitation size and clear Roshan. The pan still floats above a flat station, so room mounting remains a priority.',4.1),
 'pan_task_open':(4.6,4.6,'A complete painted rim encloses the aqua water. All twenty repeated grain instances are visibly inside the basin at this sampled starting state; the slab remains within the canvas.',4.6),
 'pan_pan_right':(4.6,4.6,'The rightward sampled basin preserves its whole contour and the grains remain within the water footprint. The bowl slides rather than showing a connected hand-held rocking action.',3.8),
 'pan_pan_left':(4.6,4.6,'The leftward sampled basin preserves its whole contour and grain containment. The still documents alternation of position, not an accepted articulated panning performance.',3.8),
 'pan_partial_pan':(4.6,4.6,'The first painted mineral cluster appears inside the water alongside reduced grains. Its small contact ellipse helps anchor the base; source identity is stable and it is not a geode loot drop.',4.6),
 'pan_earned_completion':(4.6,4.6,'Three instances of one painted mineral image sit inside the basin, with a few retained grains. The broad rim and visible clapping are clear. Repeated instances are not three new source images.',4.6),
 'geode_invitation':(4.6,4.1,'The lavender closed geode now clears the guide hat with a distinct seam. It remains a floating invitation in the procedural room; physical room context is not accepted.',4.1),
 'geode_task_open':(4.6,4.6,'The complete rounded closed shell sits on the painted slab. Five bright seam prompts identify the retained input task without changing the shell artwork.',4.6),
 'geode_five_seams_ready':(4.6,4.6,'All five seam marks show the completed prerequisite while the shell remains closed. The bright markers are readable; remote actor contact remains unresolved.',4.6),
 'geode_early_crack':(4.6,4.5,'A narrow cream-lined crack begins revealing rooted cyan and lavender crystals. They stay embedded in the shell; the sampled state substitution needs full timeline review.',4.5),
 'geode_middle_open':(4.6,4.5,'Both cavities open visibly around the embedded crystals, with readable cream rims and broad lavender shell values. Sampled continuity is provisional because intervening frames are not fully audited.',4.5),
 'geode_full_interior_before_award':(4.6,4.5,'Two open halves reveal six crystal details fixed inside their cavities before the award. No loose cluster is spawned. Base contact reads clearly; the complete opening performance remains unaccepted.',4.5),
 'geode_earned_completion':(4.6,4.5,'The two cavities and embedded crystal details remain visible while Roshan claps outside the work panel. This endpoint preserves the owner-directed reveal, with sampled progression still provisional.',4.5),
}
current=[]; archive=[]
for attempt in range(1,5):
 for p in sorted((family/f'attempt_{attempt:02d}/native_views').glob('*.webp')):
  tokens=p.stem.split('_',2);width=int(tokens[1]);state=tokens[2]
  direct=attempt==4 or attempt==3 and width==1280 or attempt==2 and width==1280 and state.startswith('fossil_') or attempt==1 and width==1280 and state in ['fossil_invitation','fossil_brushed','fossil_earned_completion','pan_invitation','pan_task_open','pan_partial_pan','geode_task_open']
  row=dict(id=f'GEO-WORK-A{attempt:02d}-{width}-{state.upper()}',path=rp(p),sha256=sha(p),dimensions=list(Image.open(p).size),attempt=attempt,width=width,state=state,direct_review=direct,current=attempt==4)
  if attempt==4:
   material,mount,note,sequence=notes[state]
   row.update(material_score=material,mounted_detail_score=mount,sampled_state_score=sequence,room_composition_score=2.8,actor_contact_score=None if state.endswith('invitation') or state.endswith('completion') else 2.7,completion_actor_visibility_score=4.6 if state.endswith('completion') else None,complete_action_score=None,evaluation=note,qualification=qual)
   row['priority_lanes']=[k for k in ['material_score','mounted_detail_score','sampled_state_score','room_composition_score','actor_contact_score'] if isinstance(row.get(k),(int,float)) and row[k]<=4.5]
   current.append(row)
  else:
   row.update(evaluation='Historical attempted mounting; current final-state scores do not transfer to this image.',source_finish_score=None,mounted_score=None,qualification='Direct inspection status records actual earlier coverage only. All earlier native bytes preserved; no new per-image score inferred from similar current artwork.')
  archive.append(row)
assert len(current)==46 and len(archive)==174 and sum(x['direct_review'] for x in archive)==83
priority=[
 dict(id='GEO-WORK-ROOM',score=2.8,item='Procedural room and stage stations',evaluation='Broad flat stripes, cyan frames and crystal mural remain inconsistent with the painted props. No suitable native2048x2048-per-screen approved source has been identified.',next_step='Resolve the native background source and rebuild the literal room composition; do not pass an upscaled undersize reference.'),
 dict(id='GEO-WORK-CONTACT',score=2.7,item='Roshan working contact',evaluation='Roshan reaches the floor far to the left of the work surface. The prop changes occur remotely.',next_step='Build connected pickup/work/release/return evidence with the approved character family; no detached overlay or still can approve the action.'),
 dict(id='GEO-WORK-RIVER-START',score=3.5,item='River task graphics',evaluation=notes['river_task_open'][2],next_step='Inventory painted river/channel components and replace the named flat diagram after a local gameplay review.'),
 dict(id='GEO-WORK-RIVER-END',score=3.8,item='River completed water graphics',evaluation=notes['river_earned_completion'][2],next_step='Use continuous painted channels and water consequence while retaining the four connections.'),
 dict(id='GEO-WORK-SOIL-CLEAR',score=3.9,item='Soil clearing boundary',evaluation=notes['fossil_partial_brush'][2],next_step='Refine the visible cleared-cell boundary while preserving the8x5 state/save mapping and passive guard.'),
 dict(id='GEO-WORK-PAN-ACTION',score=3.8,item='Articulated alternating panning',evaluation='Whole-bowl lateral movement has no connected grip, elbow or torso action. Three ComfyUI references also remain rejected for weak alternation/contact.',next_step='Continue bounded motion refinement; none of the existing123 reference frames are an accepted runtime action.'),
 dict(id='GEO-WORK-INVITATION-CONTEXT',score=4.1,item='Four floating station invitations',evaluation='Current offsets fix actor overlap, but the props still float above the flat room stations.',next_step='Seat each intact prop into the matching physical station and retain generous touch targets.'),
 dict(id='GEO-WORK-RIVER-SEMANTICS',score=4.3,item='Layered rock as river invitation',evaluation='The specimen reads well as geology but does not directly depict channel connection.',next_step='Choose a source that communicates the actual river work without requiring reading.'),
 dict(id='GEO-WORK-ASSEMBLY',score=4.5,item='Fossil partition and support',evaluation=notes['fossil_brushed'][2],next_step='Keep the conserved spiral while improving the split edge and physical support; inclusive4.5 remains a refinement priority.'),
 dict(id='GEO-WORK-GEODE-PROGRESSION',score=4.5,item='Geode sampled opening continuity',evaluation='Embedded-cavity meaning is4.6. The four sampled opening states receive provisional4.5 only; continuous acting/contact/transitions remain open.',next_step='Review the entire ordinary opening timeline, retain embedded crystals, and refine every weak transition.'),
]
write(family/'REVIEW.json',dict(status='CURRENT_46_NATIVE_VIEWS_DIRECTLY_REVIEWED_WITH_OPEN_PRIORITIES',baseline=base,reviewed_utc=now,current_views=current,archive_views=archive,archive_count=174,archive_direct_count=83,archive_not_direct_count=91,current_direct_count=46,priority_items=priority,threshold='Every lane<=4.5 remains an inclusive refinement priority. A4.6 material opinion cannot approve a2.7 interaction.',qualification=qual,acceptance_gaps=['Castle/story entry and training routes','Every intervening native action frame','Native background resolution','Physical target device/performance','Child and owner acceptance','Other job items and final comprehensive report']))
prov=read(family/'PROVENANCE.json')
soil=read(family/'SOIL_SOURCE_REVIEW.json')
soilrow=dict(id='fossil_soil',source_path=rp(source/'fossil_soil/attempt_02/whole_canvas_1024.png'),runtime_path='assets/opera/worlds/geology/painted_work_v1_20261001/fossil_soil.png',sha256=sha(root/'assets/opera/worlds/geology/painted_work_v1_20261001/fossil_soil.png'),atlas_region=[72,171,881,684],source_score=4.6,pixel_modifications='Exact byte copy of uniformly downscaled whole canvas. No painted-pixel repair or alpha cleanup.',owner_acceptance=None)
if not any(x['id']=='fossil_soil' for x in prov['assets']):prov['assets'].append(soilrow)
evaluations={
 'fossil':'One bold warm spiral inside a broad lavender matrix. The intact painting and its exact three thirds preserve the source aspect and contour.',
 'pan':'Broad lavender rim, quiet aqua water and one shallow rounded basin. The whole contour is preserved at every sampled side position.',
 'work_slab':'Cream stone plane and broad lavender front edge unite the work material. It stays within the canvas; fossil loose-piece front-face placement remains provisional4.5.',
 'grain':'Rounded ochre pebble with grouped cream highlight and lavender shadow. Twenty repeated instances share one source image and remain in the sampled initial basin.',
 'mineral':'One readable cyan/lilac cluster with calm broad facets. Three pan instances reuse it; it is never the geode interior or a geode loot drop.',
 'layered_rock':'Three broad painted strata and rounded dark contour retain geology teaching readability. River-invitation task semantics4.3 remain separate.',
 'fossil_soil':'Deep opaque ochre patch with grouped perimeter pebbles, cream values and lavender edge shadows fully conceals the fossil initially. The straight clearing edge3.9 is a separate rendering issue.',
}
objects=[]
for x in prov['assets']:
 x['mounted_material_score']=4.6;x['mounted_score']=None;x['complete_action_score']=None;x['qualification']='Current material appearance4.6; room/contact/transition scores separate in REVIEW.json.'
 assert sha(root/x['source_path'])==sha(root/x['runtime_path'])==x['sha256']
 objects.append(dict(id='GEO-WORK-'+x['id'].upper(),kind='source',path=x['runtime_path'],sha256=x['sha256'],source_path=x['source_path'],source_dimensions=list(Image.open(root/x['runtime_path']).size),region=x['atlas_region'],source_finish=4.6,mounted_object_finish=4.6,complete_action_score=None,owner_acceptance=None,evaluation=evaluations[x['id']],qualification=qual))
prov.update(status='SEVEN_EXACT_SOURCE_COPIES_WITH_DIRECT_CURRENT_MATERIAL_REVIEW',new_generations=2,selected_new_generations=1,rejected_new_generations=1,native_report='audit/job_geology_painted_work_v1_20261001/REVIEW.json');write(family/'PROVENANCE.json',prov)
soil.update(mounted_cover_material_score=4.6,initial_concealment_score=4.6,partial_clearing_boundary_score=3.9,complete_action_score=None,current_evidence='audit/job_geology_painted_work_v1_20261001/attempt_04/native_views/geologist_1280_fossil_partial_brush.webp');write(family/'SOIL_SOURCE_REVIEW.json',soil)
f=objects[0]
parts=[]
for i in range(3):
 region=[115+802*i/3,171,802/3,674]
 parts.append(dict(id='GEO-WORK-FOSSIL-PART-'+str(i+1),kind='source object region',path=f['path'],sha256=f['sha256'],source_dimensions=f['source_dimensions'],region=region,review_annotation_source_rect=region,source_finish=4.6,mounted_object_finish=4.6,partition_and_support_score=4.5,complete_action_score=None,evaluation=f'Conserved vertical third{i+1} of the same fossil painting; no independent regeneration or extra source file. Painted material4.6, straight partition/support4.5 provisional. Exactly rejoins the original spiral.',qualification=qual,owner_acceptance=None))
instances=[]
for kind,n in [('grain',20),('mineral',3)]:
 item=next(x for x in objects if x['id']=='GEO-WORK-'+kind.upper())
 for i in range(n):instances.append(dict(id=f'GEO-WORK-PAN-{kind.upper()}-INSTANCE-{i+1:02d}',kind='repeated runtime instance',source_item_id=item['id'],path=item['path'],sha256=item['sha256'],sampled_material_score=4.6,sampled_containment_score=4.6,complete_action_score=None,qualification='Same source bytes reused; instance index is a scene identity, not a new image. Containment directly inspected in current start or earned endpoint at both widths. No independent animation acceptance.'))
write(family/'ARTWORK_ITEMS.json',dict(status='INDIVIDUAL_SOURCES_PARTITIONS_AND_REPEATED_INSTANCES',source_items=objects,fossil_source_regions=parts,pan_runtime_instances=instances,geode_items_reference='audit/job_geode_runtime_v1_20261001/ARTWORK_ITEMS.json',qualification='Seven new runtime source paths, three conserved fossil regions and23 repeated pan instances. Existing four geode sources/six embedded details retain their separate exact register. Repeated instances do not inflate source-file or generated-image counts.'))
# New current source review; preserve all earlier opinions and receipts byte-for-byte.
d=read(source/'REVIEW_V7.json');d['previous_review']=rp(source/'REVIEW_V7.json');d['baseline']=base;d['reviewed_utc']=now
for attempt,score,decision in [(1,4.5,'REJECTED_FOR_COVER_GEOMETRY'),(2,4.6,'SELECTED_RUNTIME_TOPIC_CANDIDATE')]:
 q=source/f'fossil_soil/attempt_{attempt:02d}';v=read(q/'REVIEW.json');p=q/'native_generated.png'
 d['items'].append(dict(id=f'GEO-PAINT-FOSSIL-SOIL-{attempt:02d}',path=rp(p),sha256=sha(p),dimensions=list(Image.open(p).size),source_score=score,status=decision,evaluation='Broad warm painted soil material with clustered perimeter pebbles. '+('Too shallow to cover the fossil at required height; cover geometry4.0, never bound.' if attempt==1 else 'Deeper opaque patch meets the concealment geometry; material4.6, current straight clearing edge3.9 remains open.'),native_direct_review=True,neutral_previews_direct_review=[],source_record=rp(q/'PROVENANCE_PENDING.json'),mounted_score=None,complete_action_score=None,owner_approval=None,qualification='Direct native-only review. No neutral preview exists for these two new sources; generation tool native output retained without pixel edits.'))
p=source/'fossil_soil/attempt_02/whole_canvas_1024.png'
d['technical_derivatives'].append(dict(path=rp(p),sha256=sha(p),dimensions=list(Image.open(p).size),source_path=rp(p.parent/'native_generated.png'),source_sha256=sha(p.parent/'native_generated.png'),method='WHOLE_CANVAS_UNIFORM_1254_TO_1024_LANCZOS_RGBA',alpha_preserved=True,pixel_repair=False,source_score=4.6,status='SELECTED_RUNTIME_TOPIC_CANDIDATE',evaluation=evaluations['fossil_soil'],qualification='One uniform whole-canvas technical transform only; native original preserved. Direct derivative/material review separate from clearing/contact acceptance.'))
selected={x['source_path']:x['runtime_path'] for x in prov['assets']}
for x in d['items']+d['technical_derivatives']:
 if x['path'] in selected:
  x['status']='SELECTED_RUNTIME_TOPIC_CANDIDATE';x['runtime_path']=selected[x['path']];x['mounted_material_score']=4.6
  x['qualification']=x.get('qualification','')+' Exact derivative is now bound at the new reversible runtime path;46 current native states reviewed. Full scene/action acceptance remains open.'
  if x.get('source_path'):
   for y in d['items']:
    if y['path']==x['source_path']:y['status']='SELECTED_ORIGINAL_WITH_BOUND_DERIVATIVE';y['runtime_path']=x['runtime_path']
d.update(native_outputs_directly_reviewed=20,neutral_native_displays_directly_reviewed=34,technical_derivatives_directly_reviewed=14,qualification='All20 native outputs,34 existing neutral fields and14 whole-canvas derivatives directly reviewed. New soil has no neutral previews.46 current production stills directly reviewed;174 current-work archive stills preserved,83 direct/91 not directly inspected. Previous36 geode runtime stills and302 fixture comparisons remain historical evidence, not extra current views.',runtime_binding_supplement=dict(geode_previous_review='audit/job_geode_runtime_v1_20261001/index.html',painted_work_review=rp(family/'index.html'),painted_work_assets=prov['assets'],complete_action_accepted=False,owner_accepted=False))
d['native_context_reports'].append(rp(family/'index.html'));write(source/'REVIEW_V8.json',d)
write(source/'GENERATED_NATIVE_REGISTER_V7.json',dict(status='20_NATIVE_GENERATED_SOURCE_FILES_PRESERVED',sources=[dict(path=x['path'],sha256=x['sha256'],dimensions=x['dimensions'],score=x['source_score'],status=x['status']) for x in d['items']],qualification=d['qualification']))
# Illustrated report: all46 current native images, seven sources and every archived native file.
esc=html.escape
def url(p):return posixpath.relpath(p,family.relative_to(root).as_posix())
def img(p,alt):return '<a href="'+esc(url(p))+'"><img loading="lazy" src="'+esc(url(p))+'" alt="'+esc(alt)+'"></a>'
def card(x):
 p=x['path'];return '<article id="'+esc(x['id'])+'"><h3>'+esc(x['id'])+'</h3>'+img(p,x.get('state',x['id']))+'<p>'+esc(x['evaluation'])+'</p><p class="scores">'+esc(' · '.join(k.replace('_score','').replace('_',' ')+': '+str(x[k])+'/5' for k in ['material_score','mounted_detail_score','sampled_state_score','room_composition_score','actor_contact_score','completion_actor_visibility_score'] if x.get(k) is not None))+'</p><p class="tiny">'+esc(x.get('qualification',qual))+'</p><details><summary>File and SHA-256</summary><code>'+esc(p)+'<br>'+x['sha256']+'</code></details></article>'
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geology — painted work, every current state</title><style>*{box-sizing:border-box}body{margin:0;background:#ecf4f6;color:#29314e;font:17px/1.55 system-ui}main{max-width:1320px;margin:auto;padding:24px}header,section{background:white;border-radius:16px;padding:24px;margin-bottom:22px}h1,h2,h3{line-height:1.25}a{color:#57468c}nav{display:flex;gap:18px;flex-wrap:wrap}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,480px),1fr));gap:22px}article{padding:18px;background:#f4f2f8;border-radius:12px;min-width:0}img{display:block;max-width:100%;height:auto;background:#d7e4ec;border-radius:8px}.sources img{max-height:320px;object-fit:contain;width:100%}.scores{font-weight:650;color:#5d477d}.tiny,code{font-size:13px;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%}td,th{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #ccd5df}code{white-space:normal}.priority{border-left:5px solid #bd734f}.archive img{max-height:240px;object-fit:contain}summary{cursor:pointer}@media(max-width:600px){main{padding:10px}header,section{padding:16px}td,th{padding:7px}}</style><main>'''
page+='<header><h1>Geology: painted work and every current state</h1><p>Seven painted runtime sources now replace the flat fossil, pan contents, soil bed, invitation props and work slab. The geode opens around crystals embedded inside its two cavities. These are reversible topic-branch candidates; originals and failed attempts are retained.</p><p><strong>46 current native views directly inspected at1280×720 and1600×720.</strong> Four attempts preserve174 views:83 directly inspected,91 archived without a new visual opinion. This is a bounded geology continuation; the all-job library and final owner-approved report remain unfinished.</p><nav><a href="#sources">Individual artwork</a><a href="#priorities">Weak items</a><a href="#current">Every current state</a><a href="#soil">Soil retries</a><a href="#archive">Earlier attempts</a><a href="#verification">Verification</a><a href="../job_artwork_refinement_live/all_items.html">All-job register</a></nav></header>'
page+='<section id="sources"><h2>Seven individual mounted source images</h2><p>Each exact source and its current sampled material appearance is4.6/5. That score does not pass room mounting, contact or a complete action. Three fossil pieces are conserved regions of one image; twenty grains and three pan minerals are repeated instances of one image each.</p><div class="grid sources">'
for x in objects:page+='<article><h3>'+esc(x['id'])+' · material4.6/5</h3>'+img(x['path'],x['id'])+'<p>'+esc(x['evaluation'])+'</p><details><summary>Original source and exact provenance</summary><a href="'+esc(url(x['source_path']))+'">Whole-canvas derivative</a><p class="tiny">'+esc(x['sha256'])+'</p></details></article>'
page+='</div><p><a href="ARTWORK_ITEMS.json">Individual source / partition / instance records</a> · <a href="PROVENANCE.json">Exact copy provenance</a> · <a href="../job_geode_runtime_v1_20261001/index.html#embedded-components">Four geode sources and six embedded crystal details</a></p></section>'
page+='<section id="priorities"><h2>Every remaining named weak item</h2><p>Scores of4.5/5 or lower stay in the refinement queue, including provisional states. A stronger prop does not erase the weaker stage or action in which it appears.</p><div class="grid">'
for x in priority:page+='<article class="priority"><h3>'+esc(x['item'])+' · '+str(x['score'])+'/5</h3><p>'+esc(x['evaluation'])+'</p><p>'+esc(x['next_step'])+'</p></article>'
page+='</div></section><section id="current"><h2>All46 current actual-game native views</h2><p>Ordinary viewport invitation taps and arrival open each activity; real task input earns one completion and the normal hold advances the career. The isolated fixture hides the main HUD and freezes only for still capture. It does not prove Castle/story entrance, training, naturally timed acting or device acceptance.</p>'
for phase in ['river','fossil','pan','geode']:
 page+='<h2>'+phase.title()+'</h2><div class="grid">'+''.join(card(x) for x in current if x['state'].startswith(phase+'_'))+'</div>'
page+='</section><section id="soil"><h2>Soil generation: preserve rejection and selected retry</h2><p>The existing painted family had no deep loose-earth cover. Two fresh ImageGen originals were made for this named gap with no image bindings. Only the second source is bound, after one uniform whole-canvas downscale. No masking, alpha repair or subject edits were used.</p><div class="grid sources">'
for attempt in [1,2]:
 p=rp(source/f'fossil_soil/attempt_{attempt:02d}/native_generated.png');page+='<article><h3>Attempt'+str(attempt)+(' · source4.5 / cover geometry4.0, rejected' if attempt==1 else ' · source4.6, selected; clearing boundary3.9')+'</h3>'+img(p,'Native soil attempt'+str(attempt))+'<p>'+('Too shallow to conceal the fossil correctly. Preserved and never bound.' if attempt==1 else 'Deep patch conceals the whole fossil, but clearing still removes a straight grid row.')+'</p><a href="'+esc(url(rp(source/f'fossil_soil/attempt_{attempt:02d}/REVIEW.json')))+'">Exact native review</a></article>'
page+='</div></section><section id="archive"><h2>Every earlier native attempt</h2><p>Attempt1: clipped slab/overlapped invitations;7 of36 directly inspected. Attempt2: corrected slab and fossil/pan offsets;7 of46 directly inspected. Attempt3: deeper soil;all23 native1280 views directly inspected,1600 views archived unreviewed. Attempt4 above:all46 directly inspected. Historical images never inherit current scores.</p>'
for attempt in range(1,4):
 page+='<details><summary>Attempt'+str(attempt)+' — every preserved image</summary><div class="grid archive">'
 for x in archive:
  if x['attempt']==attempt:page+='<article><h3>'+esc(x['id'])+'</h3>'+img(x['path'],x['state'])+'<p>'+('Earlier directly inspected; historical scores stay in their dated records.' if x['direct_review'] else 'Archived only; not directly visually inspected.')+'</p><p class="tiny">'+x['sha256']+'</p></article>'
 page+='</div></details>'
page+='</section><section id="verification"><h2>Implementation, machines and acceptance</h2><p>New assets live at separate paths with lossless import; the seven runtime PNGs exactly match their recorded whole-canvas sources. Atlas windows retain authored aspect. Original paintings, rejected drafts, protected book/voices/friend assets and earlier receipts remain preserved.</p><p id="ci-state">Fresh current full suite is pending. The earlier82/82 geode checkpoint validates its own334-file source boundary only.</p><p><a href="full_ci_v1/RECEIPT.json">Fresh complete suite receipt</a> · <a href="full_ci_v1/SOURCE_BEFORE.json">Current349-file source freeze</a> · <a href="full_ci_v1/ENGINE_DIAGNOSTICS.json">Unfiltered engine diagnostic index</a> · <a href="REVIEW.json">Every native evaluation</a> · <a href="../../design/audit_impacts/job-geology-painted-work-20261001.json">Audit impact</a> · <a href="../job_geode_runtime_v1_20261001/index.html">Immutable previous geode evidence</a></p><p>Machine regression does not establish strict zero3D debt or visual satisfaction. Room, contact, intervening action frames, Castle/story/training routes, physical device, child and owner acceptance remain open. MA-PLAY-004 and MA-VIS-006 stay open. No integration, release or final comprehensive approval is claimed.</p></section></main></html>'
(family/'index.html').write_text(page,encoding='utf-8',newline='\n')
# Append current source-library note and both raw new originals; never overwrite historical source cards.
p=source/'index.html';s=p.read_text(encoding='utf-8')
if 'id="painted-work-current"' not in s:
 fragment='<section id="painted-work-current"><h2>Current painted-work continuation</h2><p>REVIEW_V8:20 native originals,34 existing neutral displays and14 whole-canvas derivatives directly inspected. Seven painted-work derivatives join the four existing geode bindings at separate runtime paths. All46 current native game states directly reviewed; room2.8/contact2.7/clearing3.9 remain priorities. No full action/device/child/owner acceptance.</p><p><a href="../../../audit/job_geology_painted_work_v1_20261001/index.html">Every current game state and weak item</a> · <a href="REVIEW_V8.json">Current individual source review</a> · <a href="GENERATED_NATIVE_REGISTER_V7.json">Every native original</a></p>'
 for attempt in [1,2]:fragment+=f'<article><h3>Soil attempt{attempt}</h3><a href="fossil_soil/attempt_{attempt:02d}/native_generated.png"><img loading="lazy" style="max-width:100%;height:auto;max-height:360px" src="fossil_soil/attempt_{attempt:02d}/native_generated.png" alt="Native soil attempt{attempt}"></a><p>'+('Source4.5 / cover4.0 rejected and unbound.' if attempt==1 else 'Source/material4.6; selected derivative bound. Clearing edge3.9 remains weak.')+'</p></article>'
 s=s.replace('</body>',fragment+'</section></body>') if '</body>' in s else s.replace('</html>',fragment+'</section></html>');p.write_text(s,encoding='utf-8',newline='\n')
# One provenance entry for each native screenshot, no aggregate missing rows.
p=root/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8');add=[]
for x in archive:
 if '`'+x['path']+'`' not in s:add.append('| `'+x['path']+'` | Project native Godot4.7.2 Mobile-rendered review screenshot; existing project artwork provenance retained | Project review evidence; not a newly licensed source artwork | '+rp(family/f"attempt_{x['attempt']:02d}/CAPTURE_{x['width']}.json")+' | Exact native lossless WebP; no pixel edits; isolated review fixture, not runtime art or creative acceptance |')
if add:p.write_text(s+'\n\n'+('\n'.join(add))+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
p=root/'design/audit_impacts/job-geology-painted-work-20261001.json';d=read(p)
d['files']=sorted(set(d['files'])|{rp(p) for p in family.rglob('*') if p.is_file()}|{rp(p) for p in [source/'REVIEW_V8.json',source/'GENERATED_NATIVE_REGISTER_V7.json',source/'index.html']})
d['validation'].append(dict(command='Direct current painted-work native artwork review',result='PASS',evidence='audit/job_geology_painted_work_v1_20261001/REVIEW.json;46/46 current stills directly viewed;83/174 archive direct. PASS means review coverage, not weak-lane acceptance.'))
write(p,d)
print('REVIEW178|46 current direct|174 archive83 direct|7 source14 total derivatives20 native|174 screenshot license rows')
