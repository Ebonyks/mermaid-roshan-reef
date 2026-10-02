from pathlib import Path
import json, hashlib, shutil, subprocess, datetime, html, sys

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
def rel(p): return p.relative_to(r).as_posix()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((r/p).read_text(encoding='utf-8'))
def write(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
geo='assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
source=geo+'/open_geode/attempt_02/native.png'
record=read(geo+'/open_geode/attempt_02/GENERATION_RECORD.json')
source_review=dict(id='GEO-PAINT-OPEN_GEODE-02',path=source,sha256=sha(r/source),dimensions=record['native_dimensions'],source_score=4.6,status='SELECTED_SOURCE_ONLY_EMBEDDED_INTERIOR',evaluation='Two rounded mineral halves have clear concave purple cavities enclosed by a cream rim. Three large aqua/lavender crystals in each half have roots visibly buried in the lining; none floats in the gap or detaches as loot. Broad matte paint, plum contours and aqua underside preserve the closed geode material family. Both halves and generous transparent margins are complete. Closed-to-open apparent width and actor contact remain independent action priorities.',qualification='Direct generated native, white and aqua native alpha displays and complete1024x683 uniform derivative directly inspected. Source-only agent drafting score; no production binding, complete career/training/story, device, child or owner acceptance.',source_record=geo+'/open_geode/attempt_02/GENERATION_RECORD.json',native_direct_review=True,neutral_previews_direct_review=[geo+'/open_geode/attempt_02/audit_white.png',geo+'/open_geode/attempt_02/audit_aqua.png'],mounted_score=None,complete_action_score=None,owner_approval=None)
assert source_review['sha256']=='1191313bc32098ef4c1acede1c2bf547448b6a57a32905e7324e87bc092d87d8'
write(r/(geo+'/open_geode/attempt_02/SOURCE_REVIEW.json'),source_review)
d=read(geo+'/REVIEW.json');d['previous_review']=geo+'/REVIEW.json';d['reviewed_utc']=now;d['status']='PAINTED_SOURCE_AND_NATIVE_FIXTURE_REVIEW_COMPLETE_WITH_OPEN_ACTION_PRIORITIES';d['items'].append(source_review)
technical=read(geo+'/open_geode/attempt_02/whole_canvas_1024.json')
derivative=dict(path=geo+'/open_geode/attempt_02/whole_canvas_1024.png',sha256=sha(r/(geo+'/open_geode/attempt_02/whole_canvas_1024.png')),dimensions=[1024,683],source_path=source,source_sha256=source_review['sha256'],method='WHOLE_CANVAS_UNIFORM_DOWNSCALE_1536x1024_TO1024x683_RGBA_PNG',alpha_preserved=True,pixel_repair=False,qualification='Whole-canvas uniform technical conversion, preserved original; directly inspected. No alpha repair, image compositing or independently awarded action score.',source_score=4.6,status='TECHNICAL_DERIVATIVE_UNBOUND',evaluation=source_review['evaluation'])
d['technical_derivatives'].append(derivative)
for x in d['items']+d['technical_derivatives']:
 if '/open_geode/attempt_01/' in x['path']:
  x['historical_source_score']=x['source_score'];x['historical_evaluation']=x['evaluation'];x['source_score']=3.0;x['status']='OWNER_REJECTED_EMPTY_INTERIOR';x['evaluation']='Owner correction withdraws the earlier finish-only4.6 as a current acceptance claim: empty cream halves and a separate crystal reward do not show crystals embedded in the geode. Original native and dated source review remain unchanged. Current semantic3.0; replaced by attempt02.'
 if '/crystal_reward/' in x['path']:
  x['evaluation']+=' Owner correction: excluded from the geode reveal. May inform crystal color/material or a separately audited badge only; never a loose reward layer in the opening.'
d['native_outputs_directly_reviewed']=13;d['neutral_native_displays_directly_reviewed']=24;d['technical_derivatives_directly_reviewed']=8
d['native_context_reports']=['audit/job_vector_mount_review_v1_20261001/index.html','audit/job_geology_painted_mount_v1_20261001/index.html','audit/job_geode_embedded_mount_v2_20261001/index.html']
d['acceptance_gaps']=['Native1672x941 room fails2048x2048-per-screen coverage; reference only','Work slab source aspect2.41 squeezed into860x560 gives overly tall depth','Fossil cover conceals source; three assembly thirds remain stretched and poorly seated','River and pan residual procedural graphics remain below painted style target','Geode invitation floats over imp; immediate state-switch geometry/contact still below target','Complete ordinary training/story career traversal, audio/feedback, device, child and owner acceptance','All known weak items and388 unassigned source opinions require continued broad review; no final comprehensive approval']
write(r/(geo+'/REVIEW_V2.json'),d)
old=read(geo+'/GENERATED_NATIVE_REGISTER_V1.json');old['status']='THIRTEEN_NATIVE_GENERATIONS_PRESERVED';old['previous_register']=geo+'/GENERATED_NATIVE_REGISTER_V1.json';old['records'].append(record);write(r/(geo+'/GENERATED_NATIVE_REGISTER_V2.json'),old)
correction=read(geo+'/GEODE_OWNER_CORRECTION_V2.json');correction.update(status='OWNER_CORRECTION_GENERATED_AND_DIRECTLY_REVIEWED',new_source_score=4.6,source_review=geo+'/open_geode/attempt_02/SOURCE_REVIEW.json',latest_native_report='audit/job_geode_embedded_mount_v2_20261001/attempt_02/REVIEW.json',provisional_mounted_open_object_score=4.5,complete_action_score=None,owner_approval=None);write(r/(geo+'/GEODE_OWNER_CORRECTION_V2.json'),correction)

common='Direct inspection of this exact unmodified Godot4.7.2 Mobile native capture. Desktop drafting evidence only. Phase selected in a disposable fixture with inherited touch/progress; no complete ordinary job/training/story route, child/device or owner acceptance. A null object score means absent or too hidden to judge; it is never a pass.'
def evaluate(v,kind):
 lane=v['variant'];phase=v['phase'];state=v['state'];paint=lane=='painted_staging';candidate=lane=='candidate';wide=v['viewport'][0]==1600
 scores=dict(object_finish=None,object_semantics=None,scene_style=None,layout=None,actor_work_contact=None,complete_action=None)
 if v['career']=='teacher':
  scores.update(scene_style=4.4,layout=4.4)
  if state=='invitation':
   scores.update(object_finish=4.5 if candidate else 4.2,object_semantics=4.6)
   text='Lesson board remains a stable readable framed prop with attached legs. Candidate uses a warmer rim and quieter thinner plum contours; it fits the painted classroom better. Candidate4.5 is provisional and remains an inclusive refinement priority. Full lesson contact/transition is not represented.'
  else:
   text='The actual '+phase+' lesson uses the same production surface in both texture lanes; replacement invitation-board pixels are absent after opening. Large tokens and spacing remain legible. No candidate-board mounted score is awarded for this view, and no completed answer/lesson was played.'
  return scores,text
 scores.update(scene_style=4.3 if paint else 2.8,layout=4.2 if paint else 3.0)
 if paint and wide and kind=='painted':scores['layout']=4.0
 if state=='invitation':
  if paint:
   scores.update(object_finish=4.4,object_semantics=4.5)
   text='Correct painted '+phase.lower()+' invitation object is finally visible in this explicitly restaged study. Gouache masses fit the approved characters, but the prop floats independently of shelves and may overlap the imp hat; support and invitation ownership remain priorities. The room is an undersize reference, never runtime-ready.'
  elif phase=='PAN':
   scores.update(object_finish=3.9,object_semantics=3.0)
   text='The pan invitation displays a layered-rock specimen. A texture/style replacement cannot repair that wrong semantic cue; the child needs the washing pan. Current flat room and tray graphics compete with the characters.'
  else:
   scores['object_semantics']=2.8
   text='Only the halo and room graphics appear at the invitation target: the assigned '+phase.lower()+' texture is suppressed in this presentation. No visible object pixels means no individual mounted-art score; replacing the resource alone does not repair it.'
  return scores,text
 scores['actor_work_contact']=2.7
 board=' Painted work material is stronger, but its2.41 source ratio is squeezed into860x560 and makes the slab disproportionately deep.' if paint else ' Flat tan work card and thick navy contour do not match the painted characters.'
 if phase=='RIVER':
  scores.update(object_finish=3.8 if paint else 3.0,object_semantics=4.0)
  text='River still uses uniform flat grid circles and cyan connecting tracks; '+('four connected nodes are actual partial-input progress' if 'partial' in state else 'the initial dot field is visible')+'. It is readable but still needs painted grouping/material. Roshan is far from the active work, with no connected hand contact.'+board
 elif phase=='FOSSIL':
  if 'assembly' in state:
   scores.update(object_finish=4.2 if paint else 3.9 if candidate else 3.8,object_semantics=3.8)
   text='Three vertical source thirds are stretched into broad shallow assembly pieces. Painted texture is better, yet the oval is flattened, translucent target ghosts remain, and lower pieces overlap the slab depth instead of seating on its top. No assembly snap/completion is represented; hand and work are disconnected.'+board
  else:
   scores['object_semantics']=3.0
   text='Opaque orange excavation cells fully conceal the fossil at opening; the brush partial gesture reveals only a tiny upper rim. That sliver cannot establish the source shape or finish, so object score stays null. Brush/bristle contact and distant actor position remain weak.'+board
 elif phase=='PAN':
  scores.update(object_finish=4.4 if lane=='literal_raster' or paint else 3.5,object_semantics=4.3)
  text='Painted lavender rim and aqua bowl improve the material substantially.' if lane=='literal_raster' or paint else 'Production ellipse remains flat with a very thick navy rim.'
  text+=' Grains lie inside the bowl; partial input records three reversals. The revealed mineral is still a flat outlined pentagon, scored3.8 separately in this evaluation. Hand contact is distant; whole panning/settle remains open.'+board
 elif phase=='GEODE':
  if state=='opened_task':
   if paint and kind=='painted':
    text='The old study accidentally lost its painted closed texture during _arm_phase reload: seam dots appear over an empty slab. This is a disposable fixture defect, not a new production finding. Object score is null. The later embedded-geode fixture restores that assignment explicitly.'+board
   else:
    scores.update(object_finish=4.5 if paint else 3.0,object_semantics=4.3 if paint else 3.5)
    text='Closed painted geode is visible with its single seam and five inherited touch cues.' if paint else 'Closed geode remains a flat plum ellipse with five large dots.'
    text+=' Painted seam cues only approximately follow the irregular seam; no continuous opening transition has been reviewed.'+board
  elif paint and kind in ['embedded_initial','embedded_revised']:
   score=4.5 if kind=='embedded_revised' else 4.2
   scores.update(object_finish=4.6,object_semantics=4.6,layout=min(scores['layout'],score))
   text='Three crystals remain permanently embedded in each visible cavity. The cream rim encloses their roots, both halves preserve the generated aspect, and no detached reward image is drawn. '+('Uniform320px half height keeps the full-open right contour within the work card; placement remains close to its right boundary, provisional object-in-layout4.5.' if kind=='embedded_revised' else 'At350px height, the fully separated right half overhangs the work card; placement4.2 and the view is retained as a failed layout attempt.')+' The switch from closed to visible interiors occurs immediately once pull begins; width/acting continuity and distant hands remain below target.'+board
  else:
   scores.update(object_finish=4.4 if paint else 3.4 if lane=='literal_raster' or candidate else 3.0,object_semantics=3.0)
   text='The shell opens around a separate crystal cluster in the central gap; painted empty cream halves still imply a loose loot reward. Owner rejected that meaning. Source finish cannot override the semantic3.0. This view is historical comparison only, superseded by embedded-interior attempt02.'+board
 return scores,text

sets=[('vector','tmp/vector_mount_v87/native_views','audit/job_vector_mount_review_v1_20261001/attempt_02',76),('painted','tmp/geology_painted_mount_v96/native_views','audit/job_geology_painted_mount_v1_20261001/attempt_02',78),('embedded_initial','tmp/geode_embedded_mount_v98/native_views','audit/job_geode_embedded_mount_v2_20261001',24),('embedded_revised','tmp/geode_embedded_mount_v99/native_views','audit/job_geode_embedded_mount_v2_20261001/attempt_02',24)]
license_path=r/'ASSET_LICENSES.md';license_text=license_path.read_text(encoding='utf-8');license_lines=[]
reports=[]
for kind,temp,destination,count in sets:
 receipt=read(temp+'/CAPTURE_RECEIPT.json');assert len(receipt['views'])==count
 out=r/destination;dest=out/'native_views';assert not dest.exists();dest.mkdir()
 shutil.copyfile(r/(temp+'/CAPTURE_RECEIPT.json'),dest/'CAPTURE_RECEIPT.json')
 views=[]
 for v in receipt['views']:
  src=r/temp/v['path'];target=dest/v['path'];assert sha(src)==v['sha256'];shutil.copyfile(src,target);assert sha(target)==v['sha256']
  scores,text=evaluate(v,kind);q=dict(v);q.update(archive_path=rel(target),direct_native_review=True,reviewed_utc=now,scores=scores,evaluation=text,qualification=common,owner_acceptance=None,production_binding_changed=False)
  if kind=='embedded_revised' and v['variant']=='painted_staging' and ('partial' in v['state'] or 'fully_open' in v['state']):q['provisional_individual_object_in_layout_score']=4.5
  q['priority_dimensions']=[k for k,value in scores.items() if value is not None and value<=4.5]
  views.append(q)
  if rel(target) not in license_text:license_lines.append('| `'+rel(target)+'` | Mermaid Roshan project native Godot4.7.2 Mobile review capture; local authored/project source licenses retained | Project review evidence, not new runtime artwork | `'+destination+'/PROFILE.json` | Unmodified lossless native capture; review-only; original images and protected assets retained. |')
 summary=dict(schema='reef.individual-native-graphics-review.v1',status='EVERY_REGISTERED_NATIVE_VIEW_DIRECTLY_REVIEWED_OPEN_PRIORITIES',baseline='6edb4ca8c57bfbfe3123636863a29c95165ac23f',reviewed_utc=now,native_views=count,directly_reviewed=count,capture_receipt=destination+'/native_views/CAPTURE_RECEIPT.json',process_receipt=destination+'/PROCESS_RECEIPT.json',fixture_kind=kind,qualification=common,views=views)
 write(out/'REVIEW.json',summary);reports.append(destination+'/REVIEW.json')
 esc=html.escape
 cards=''.join('<article id="'+esc(q['id'])+'"><h2>'+esc(q['id'])+'</h2><a href="native_views/'+esc(q['path'])+'"><img loading="lazy" src="native_views/'+esc(q['path'])+'" alt="'+esc(q['id'])+'"></a><p>'+esc(q['evaluation'])+'</p><p><strong>Scores /5:</strong> '+esc(', '.join(k.replace('_',' ')+': '+('unassigned' if value is None else str(value)) for k,value in q['scores'].items()))+'</p><p>'+esc(q['qualification'])+'</p><details><summary>Exact identity and actual progress</summary><pre>'+esc(json.dumps(dict(sha256=q['sha256'],viewport=q['viewport'],progress=q['surface_progress'],qualification=q['fixture']),indent=2))+'</pre></details></article>' for q in views)
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(kind)+' geology/teacher native review</title><style>body{background:#edf2fa;color:#26304b;font:17px/1.5 system-ui;margin:0}main{max-width:1450px;padding:24px;margin:auto}article,header{padding:20px;background:white;border-radius:14px;margin-bottom:24px}h2,pre{overflow-wrap:anywhere}img{width:100%;height:auto}pre{white-space:pre-wrap;font-size:13px}a{color:#57418a}</style><main><header><h1>'+esc(kind.replace('_',' '))+' — '+str(count)+' individual native views</h1><p>Every image below was directly inspected at its native capture size. Scores remain first-pass agent evaluations. Texture assignments are not proof of visible pixels; hidden objects stay unassigned.</p><p><a href="REVIEW.json">Complete written scores and hashes</a> · <a href="native_views/CAPTURE_RECEIPT.json">Original machine capture receipt</a></p><p>'+esc(common)+'</p></header>'+cards+'</main></html>'
 (out/'index.html').write_text(page,encoding='utf-8',newline='\n')
 if destination.endswith('attempt_02'):
  parent=out.parent;(parent/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Native comparison review</title><main style="font:18px/1.5 system-ui;max-width:1000px;margin:32px auto"><h1>Native comparison review</h1><p><a href="attempt_02/index.html">All '+str(count)+' latest native captures, individual scores and evaluations</a></p><p>Earlier preparation/runtime failures and raw logs remain preserved. This is reversible review material, with no production replacement or full-job acceptance.</p></main></html>',encoding='utf-8',newline='\n')

# The geode root keeps both successful visual attempts accessible.
(r/'audit/job_geode_embedded_mount_v2_20261001/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geode embedded crystal redraw</title><main style="font:18px/1.5 system-ui;max-width:1200px;margin:24px auto"><h1>Geode opens to reveal its own crystals</h1><p>The new ImageGen source scores4.6/5. Three rooted crystals in each cream-rimmed cavity remain attached to that half. No detached crystal reward is drawn in painted staging.</p><img style="width:100%" src="attempt_02/native_views/geologist_1280_geode_fully_open_embedded_interior_painted_staging.webp" alt="New embedded geode reveal"><p><a href="attempt_02/index.html">24 revised native views and individual evaluations</a> · <a href="REVIEW.json">24 earlier views, preserved overhang scores and exact identities</a></p><p>Revised individual open object-in-layout4.5 remains provisional. Work depth, invitation support, hand contact and immediate closed/open switch still require refinement. No complete career/training/story, device, child or owner acceptance is claimed.</p><details><summary>Earlier full-open overhang</summary><img style="width:100%" src="native_views/geologist_1280_geode_fully_open_embedded_interior_painted_staging.webp" alt="Preserved earlier full-open overhang"></details></main></html>',encoding='utf-8',newline='\n')
write(r/'audit/job_geode_embedded_mount_v2_20261001/ALL_NATIVE_REVIEWS.json',dict(status='48_NATIVE_VIEWS_DIRECTLY_REVIEWED',reports=reports[-2:],latest=reports[-1],qualification=common))
if license_lines:license_path.write_text(license_text+'\n'+ '\n'.join(license_lines)+'\n',encoding='utf-8',newline='\n')

# Preserve V13 and the earlier native opinion receipts; current register uses new V2 opinions.
old_builder=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v13.py'
body=old_builder.read_text(encoding='utf-8').replace('build_current_job_item_register_v13.py','build_current_job_item_register_v14.py').replace("geo=read(geo_prefix+'/REVIEW.json')","geo=read(geo_prefix+'/REVIEW_V2.json')").replace('12 new generated originals,22 neutral displays and7 technical derivatives','13 generated originals,24 neutral displays and8 technical derivatives')
needle="correction=read('assets_src/vector/job_geology_teacher_refinement_v1_20261001/OWNER_CORRECTION_V1.json')"
insert="""for x in geo['items']+geo['technical_derivatives']:
 if x.get('historical_source_score') is not None:
  q=items[x['path']];q['historical_source_score']=x['historical_source_score'];q['latest_source_score']=x['source_score'];q['latest_source_sha256']=x['sha256'];q['earlier_written_evaluation']=x['historical_evaluation'];q['source_qualification']='Owner rejected empty geode semantics; historical finish score remains visible. New embedded-interior attempt02 separately reviewed.'
"""
assert needle in body;body=body.replace(needle,insert+needle)
new_builder=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v14.py';new_builder.write_text(body,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,'-X','utf8','-B',str(new_builder)],cwd=r,check=True)
shutil.copyfile(__file__,r/(geo+'/executed_record_geology_native_reviews_v100.py'))

# Updated illustrated source gallery uses only native/neutral files, preserving all attempts.
cards=[]
for x in d['items']:
 p=x['path'];relative=p[len(geo)+1:];preview=relative.replace('native.png','audit_aqua.png') if (r/p.replace('native.png','audit_aqua.png')).is_file() else relative
 cards.append('<article id="'+html.escape(x['id'])+'"><h2>'+html.escape(x['id'])+' — '+str(x['source_score'])+'/5</h2><a href="'+relative+'"><img loading="lazy" src="'+preview+'" alt="'+html.escape(x['id'])+'"></a><p>'+html.escape(x['evaluation'])+'</p><p>'+html.escape(x['status'])+' · source-only drafting opinion</p><code>'+x['sha256']+'</code></article>')
(r/(geo+'/index.html')).write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Painted geology rebuild</title><style>body{background:#ecf3f9;color:#29334e;font:17px/1.5 system-ui;margin:0}main{max-width:1250px;padding:24px;margin:auto}header,article{background:white;padding:20px;border-radius:14px;margin-bottom:20px}img{width:100%;max-height:650px;object-fit:contain}code{overflow-wrap:anywhere}</style><main><header><h1>Painted geology rebuild and embedded-crystal correction</h1><p>13 native ImageGen originals,24 neutral alpha displays and8 whole-canvas technical derivatives directly inspected. Every attempt is preserved. Empty geode interiors are owner-rejected; the new source scores4.6.</p><p><a href="../../../audit/job_geode_embedded_mount_v2_20261001/index.html">Geode opening:48 native comparisons</a> · <a href="../../../audit/job_geology_painted_mount_v1_20261001/index.html">All78 painted geology contexts</a> · <a href="../../../audit/job_vector_mount_review_v1_20261001/index.html">All76 earlier teacher/geology comparisons</a></p><p>The room is1672x941 and fails2048x2048 native coverage; source-only reference. Source finish, object fit and complete actions have separate scores. Weak contact, fossil masking/assembly, pan material and all-job review remain open.</p><p><a href="REVIEW_V2.json">Current written source reviews</a> · <a href="REVIEW.json">Preserved earlier source opinions</a> · <a href="GEODE_OWNER_CORRECTION_V2.json">Owner correction</a></p></header>'+''.join(cards)+'</main></html>',encoding='utf-8',newline='\n')
print('Archived and individually reviewed202 native views; generated register13 originals, current source opinionsV2 and item builderV14.',flush=True)
