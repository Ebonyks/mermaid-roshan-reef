from pathlib import Path
import json,hashlib,subprocess,os,math
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;B='ce4a454f65fc5b61f915ce41176af866fdf633ab';D='dd799b2d43871b29d1d6e0503646308a194dad1e';OUT=Path(os.environ.get('R79_ANALYSIS_OUTPUT',str(P)));OUT.mkdir(exist_ok=True,parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def wr(n,d):(OUT/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
g=rd(P/'SOURCE_OWNER_GRAPH.json');paths={};captures=[];cases=[];measure=[]
for folder in sorted((P/'native').iterdir()):
 if not folder.is_dir():continue
 d=rd(folder/'capture_manifest.json');res=rd(folder/'RESULT.json');assert res['exit_code']==0 and not res['script_or_shader_errors']and not res['source_byte_changes']and res['sidecars_exact']and res['normal_before']==res['normal_after']and d['observer_status']=='PASS'and all(x['pass']for x in d['checks'])
 assert d['renderer']=='mobile'and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and d['time_scale']==1.0
 cases.append({'path':folder.relative_to(P).as_posix(),'frames':len(d['states']),'observer_checks':len(d['checks']),'aspect':d['aspect'],'status':'PASS_BOUNDED_ORIGINAL_INPUT_ONLY'})
 for row in d['states']:
  f=folder/row['path'];raw=f.read_bytes();assert sha(raw)==row['sha256'];im=Image.open(f);assert list(im.size)==row['dimensions']and len(im.getextrema())>=3 and any(b>a for a,b in im.getextrema()[:3])
  bounded=row['classification'].startswith('BOUNDED_');w=row['snapshot']['world'];captures.append({'case':folder.name,'id':row['id'],'path':f.relative_to(R).as_posix(),'sha256':sha(raw),'bytes':len(raw),'dimensions':row['dimensions'],'bounded':bounded,'classification':row['classification'],'game':w['game'],'phase':w['phase'],'focus':w['focus'],'play':w['play']})
  if bounded:assert w['game']=='level2'and w['phase']=='promenade'and w['wall_pics_count']==0 and not w['legacy_lagoon_constructed']and w['promenade_constructed']and row['snapshot']['quality']=='speedy'
  for node in w['nodes']+row['snapshot']['nodes']:
   path=node.get('texture_path','')
   if path.startswith('res://'):paths.setdefault(path[6:],set()).add(row['id'])
  actor=w['actor'];path=actor.get('texture','')
  if path.startswith('res://'):paths.setdefault(path[6:],set()).add(row['id'])
  if row['id'].endswith('_focused') and row['id'].split('_')[0]in ['slide','swing','seesaw']:
   active_kind=row['id'].split('_')[0]
   t=next(x for x in w['targets']if x['id']==active_kind);other=next(x for x in w['targets']if x['id']!=active_kind);node=next(x for x in w['nodes']if x['path']==t['node_path']);asset=t['source_texture'][6:];source=git('show',D+':'+asset);import io
   source_image=Image.open(io.BytesIO(source)).convert('RGBA');alpha=source_image.getchannel('A');box=alpha.getbbox();scale=(other['source_hit_point'][0]-t['source_hit_point'][0])/(other['position_master'][0]-t['position_master'][0]);assert abs(scale-720/2048)<0.000001
   top=t['source_hit_point'][1]+(box[1]-source_image.height*.5)*node['scale'][1]*scale;outline=next(x for x in t['pointers']if x['name']=='PointerOutline');tip=max(outline['native_vertices'],key=lambda v:v[1]);bounds=[min(v[0]for v in outline['native_vertices']),min(v[1]for v in outline['native_vertices']),max(v[0]for v in outline['native_vertices']),max(v[1]for v in outline['native_vertices'])]
   measure.append({'case':folder.name,'consumer':active_kind,'native_hit_radius_px':t['radius_px'],'glow_center_to_hit_center_px':math.dist(t['highlight_native_origin'],t['source_hit_point']),'source_hit_disk_contains_glow_center':math.dist(t['highlight_native_origin'],t['source_hit_point'])<=t['radius_px'],'source_hit_disk_contains_outline_tip':math.dist(tip,t['source_hit_point'])<=t['radius_px'],'direct_glow_center_gesture_executed':False,'capture':f.relative_to(R).as_posix(),'source_asset':asset,'source_sha256':sha(source),'source_dimensions':list(source_image.size),'source_alpha_bbox':list(box),'master_to_native_uniform_scale':scale,'target_native_hit_point':t['source_hit_point'],'highlight_native_origin':t['highlight_native_origin'],'highlight_modulate':t['highlight_color'],'highlight_scale_master':t['highlight_scale'],'gradient_native_size':[192*t['highlight_scale'][0]*scale,192*t['highlight_scale'][1]*scale],'outline_native_bounds':bounds,'outline_tip_native':tip,'source_alpha_bbox_top_native':top,'tip_to_global_source_alpha_top_px':top-tip[1],'limits':'Source-alpha/global-bbox projection only, not the contour at this x, actual hidden/restored Canvas isolation, contact acceptance or QA11 proof. Per-consumer captured native hit radius is recorded separately; source hit-disk containment is a geometric predicate, not a direct marker gesture or child acceptance test.'})
refs=[]
for path,uses in sorted(paths.items()):
 raw=git('show',D+':'+path);ref={'path':path,'revision':D,'bytes':len(raw),'sha256':sha(raw),'observed_in_capture_ids':sorted(uses),'role':'Exact same-scene native texture dependency; no approval implied'}
 try:
  import io
  im=Image.open(io.BytesIO(raw));ref['dimensions']=list(im.size)
 except Exception:pass
 refs.append(ref)
for path in ['ASSET_LICENSES.md','scripts/interaction_affordance.gd','scripts/arena/sky_lagoon_layout.json','project.godot','scenes/main.tscn','assets/cinematics/day_one/day_one_clips.json']:
 try:raw=git('show',D+':'+path)
 except subprocess.CalledProcessError:continue
 if not any(x['path']==path for x in refs):refs.append({'path':path,'revision':D,'bytes':len(raw),'sha256':sha(raw),'role':'Source/provenance/config dependency; not art approval'})
wr('CAPTURE_INDEX.json',{'captures':captures,'cases':cases,'scope':'Original private NewGame/input/travel/focus/action/settle under current production owners; static partial diagnostics, not fullQA11/motion/device/child/owner acceptance.'});wr('CUE_MEASUREMENTS.json',{'measurements':measure,'count_unit':'Eight selected source-owned focus captures from four retained runs across three consumers at two supported native aspects; no acceptance from geometry.'})
stable='scripts/arena/sky_lagoon_promenade.gd::_register_target::Playground procedural focus ring and pointer';rid='FVR-'+sha(stable.encode())[:12].upper();prior=rd(H/'r78_game_payload_closure/CURRENT_KNOWN_ROLE_UNION.json');assert rid not in {x['id']for x in prior['records']}
functions=[x for x in g['function_bodies']if x['path']=='scripts/arena/sky_lagoon_promenade.gd'and x['function']in ['_register_target','_build_playground_screen','_activate','_start_playground_animation','_tick_slide_animation']]
# Supplement the two named source functions that deliberately have no external named target in the scanner.
raw=git('show',D+':scripts/arena/sky_lagoon_promenade.gd').decode('utf-8-sig');lines=raw.splitlines()
for name in ['_affordance_diamond_texture','_add_affordance_pointer','_tick_target_affordances','_tick_swing_animation','_tick_seesaw_animation','_finish_playground_animation','_tick_playground_settle']:
 start=next(i for i,l in enumerate(lines)if l.startswith('func '+name+'('));end=next((i for i in range(start+1,len(lines))if lines[i].startswith('func ')),len(lines));body='\n'.join(lines[start:end]);functions.append({'path':'scripts/arena/sky_lagoon_promenade.gd','function':name,'line':start+1,'end_line':end,'text':body,'sha256_lf':sha(body.encode())})
new={'id':rid,'stable_id_input':stable,'name':'Playground procedural focus ring and pointer','family':'sky_lagoon_affordances','status':'PARTIAL_CONTEXT_VISIBLE_PROCEDURAL_CUE_REPLACEMENT_OPEN','source_revision':D,'source_functions':functions,'visible_artwork_not_functional_geometry':True,'source_defined_instances':['slide','swing','seesaw'],'reviewed_active_instances':['slide','swing','seesaw'],'count_unit':'One shared authored procedural cue design-role with three source-defined consumers; consumer instances are not new pieces/families. Castle gate flat mask retains its separate existing ID.','context_evidence':['CAPTURE_INDEX.json','CUE_MEASUREMENTS.json','REVIEW.json'],'reuse_ready':False,'drawing_required':None,'samples_awaiting_review':0,'integration_sha':None,'acceptance_evidence':{'candidate':None,'integration':None,'runtime_replacement':None,'QA11':None,'device':None,'child':None,'owner':None},'blocked_dependencies':['Direct original-input glow-center/tip versus equipment-target behavior and child interpretation; source geometry alone is not that gesture test','Approved painted cue/source reuse fit inventory; do not generate merely from a source gap assumption','Other consumer focus/idle/cancellation/reentry states and complete current caller/resource closure','Painted material/style, action/contact/motion/QA11/device/child/owner and zero-art evidence']};wr('NEW_ROLE_RECORDS.json',{'pieces':[new],'new_families':[],'new_role_count':1})
wr('SOURCE_BINDINGS.json',{'source_revision':D,'files':refs,'visible_flat_role':rid,'source_functions':functions,'scope':'Same-scene exact sources/native observation; no asset changes/generation/approval.'})
bounded=sum(x['bounded']for x in captures);excluded=len(captures)-bounded;assert len(cases)==4 and excluded==8 and sum(x['observer_checks']for x in cases)==100
for case in cases:
 if 'attempt2_'in case['path']:
  ids={x['id']for x in captures if x['case']==Path(case['path']).name}
  for kind in ['slide','swing','seesaw']:
   assert all(kind+'_action_'+str(i)in ids for i in range(4))and kind+'_completed'in ids
s=rd(H/'r78_game_payload_closure/SUMMARY.json');s.update(revision='FV-AUDIT-20261016-R79',topic_baseline=B,source_revision=D,native_cases=len(cases),healthy_cases=len(cases),healthy_observer_checks=sum(x['observer_checks']for x in cases),new_native_frames=len(captures),new_bounded_contexts=bounded,new_excluded_diagnostics=excluded,retained_bounded=6342+bounded,retained_excluded=3498+excluded,retained_native_events=9840+len(captures),known_roles=263,new_roles=1,supplemental_partial_roles=39,source_ast_scripts=313,named_target_calls=g['summary']['named_target_calls'],source_candidate_target_calls=g['summary']['non_test_named_target_calls'],source_status='CURRENT_CANVAS_PROMENADE_ORIGINAL_INPUT_THREE_TOYS;LEGACY_PORTRAIT_ARRAY_EMPTY_IN_THIS_ROUTE',source_extraction_tests=10,language_semantic_checks=0,named_entry_producer_sites=0,named_slide_caller_sites=0,limits='Four original input/current Canvas cases: two retained slide-only plus two three-toy family observations. Current route retains level2/promenade and emptywall_pics, no legacy SkyLagoon constructed. This does not globally retire retained picture/race/reflection/native paths, accept four-key motion/contact or complete a catalogue alias. One newly observed shared procedural cue role, three source-defined consumers; no production/art/generation/accepted removal. Global totals/QA11/device/child/owner open.');wr('SUMMARY.json',s)
# Current sources used by analysis, original private entry/bootstrap and same-scene review.
deliver={x['path']:x for x in refs}
for x in rd(H/'r77_intro_entry_ownership/DELIVERY_SOURCE_REFERENCES.json')['files']:
 deliver.setdefault(x['path'],{k:x[k]for k in ['path','revision','bytes','sha256']})
for x in g['files']:deliver.setdefault(x['path'],{k:x[k]for k in ['path','revision','bytes','sha256']})
wr('DELIVERY_SOURCE_REFERENCES.json',{'files':sorted(deliver.values(),key=lambda x:x['path']),'scope':'Current original source corpus and exact observed same-scene texture/provenance/config bindings; no external generation export or creative approval.'})
print('R79_DERIVED',rid,len(captures),'raw',bounded,'bounded',excluded,'excluded;100checks;263roles35families;0accepted',flush=True)