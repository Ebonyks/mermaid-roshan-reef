from pathlib import Path
import json,hashlib,subprocess,os,math
from PIL import Image
from evidence_rules import validate_lane,validate_card
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r79_promenade_slide_ownership';D='dd799b2d43871b29d1d6e0503646308a194dad1e';B='fab29b2b25db8bfc732cda623190f32c5edd9d41';OUT=Path(os.environ.get('R80_ANALYSIS_OUTPUT',str(P)));OUT.mkdir(exist_ok=True,parents=True)
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def wr(n,d):(OUT/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
frames=[];cases=[];trials=[];geometry=[];textures={}
for folder in sorted((P/'native').iterdir()):
 if not folder.is_dir():continue
 d=rd(folder/'capture_manifest.json');res=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json');assert res['exit_code']==0 and not res['timed_out']and not res['script_or_shader_errors']and res['normal_before']==res['normal_after']and res['sidecars_exact']and not res['source_byte_changes']and res['fixture_dependency_unchanged']
 assert d['observer_status']=='PASS'and all(x['pass']for x in d['checks'])and d['renderer']=='mobile'and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and d['time_scale']==1.0
 assert sha((folder/'capture_entry.gd').read_bytes())==launch['fixture_sha256']
 cases.append({'path':folder.relative_to(P).as_posix(),'aspect':d['aspect'],'observer_checks':len(d['checks']),'frames':len(d['states']),'status':'PASS_BOUNDED_INPUT_AND_SEPARATE_NONRUNTIME_PROTOTYPE','scope_caption_qualification':'SCOPE_CLARIFICATION.json; per-state mode/classification and actual trials define scope, generic inherited caption is not execution evidence'})
 for f in d['states']:
  path=folder/f['path'];raw=path.read_bytes();im=Image.open(path);assert sha(raw)==f['sha256']and list(im.size)==f['dimensions']and any(hi>lo for lo,hi in im.getextrema()[:3]);snap=f['snapshot'];mode=snap['mode'];lane=f['classification'];source=lane=='BOUNDED_CURRENT_ORIGINAL_CUE_INPUT';candidate=mode=='LOCAL_NONRUNTIME_STAR_REUSE';assert source==(mode=='ORIGINAL_SOURCE'and not lane.startswith('EXCLUDED_'))
  validate_lane(mode,lane)
  w=snap['world']
  if source or candidate:assert snap['quality']=='speedy'and w['game']=='level2'and w['phase']=='promenade'and w['wall_pics_count']==0 and not w['legacy_lagoon_constructed']and w['promenade_constructed']
  frames.append({'case':folder.name,'id':f['id'],'path':path.relative_to(R).as_posix(),'sha256':sha(raw),'bytes':len(raw),'dimensions':f['dimensions'],'mode':mode,'classification':lane,'bounded_original_source':source,'nonruntime_candidate':candidate})
  for node in w['nodes']+snap['nodes']:
   tex=node.get('texture_path','')
   if tex.startswith('res://'):textures.setdefault(tex[6:],set()).add(folder.name+'/'+f['id'])
  tex=w['actor'].get('texture','')
  if tex.startswith('res://'):textures.setdefault(tex[6:],set()).add(folder.name+'/'+f['id'])
  if candidate:
   assert lane=='EXCLUDED_NONRUNTIME_PAINTED_CUE_PROTOTYPE'and len(snap['candidate'])==3
   for row in snap['candidate']:
    validate_card(row)
    assert row['texture_path']=='res://assets/mg/star.png'and row['rgba'][:3]==[1.0,1.0,1.0]and row['full_card_inside_source_hit_disk']and row['original_cue_texture_null']and row['original_pointer_child_count']==0 and not row['production_integration']
    geometry.append(dict(row,case=folder.name,capture_id=f['id'],capture_sha256=sha(raw),scope='Full source-bitmap rectangle/source hit-disk projection; original input separately measured. No QA11/production/device/child/owner acceptance.'))
 for t in d['cue_trials']:
  a=t['after'];active=a['play']['kind'];source=t['mode']=='ORIGINAL_SOURCE';entry={'case':folder.name,'mode':t['mode'],'consumer':t['consumer'],'part':t['part'],'native_point':t['native_point'],'source_lookup':t.get('pure_source_target_lookup'),'after_play_kind':active,'after_focus':a['focus'],'after_walk_goal':a['walk_goal'],'activated_requested_toy':active==t['consumer'],'actual_original_input':True,'candidate_visual_override':not source,'child_observed':False,'production_repair':False}
  if source:
   expected_active=t['part']=='tip'or t['consumer']=='seesaw';assert entry['activated_requested_toy']==expected_active
   if not expected_active:assert a['focus']==''and a['walk_goal']!='<null>'
  else:assert entry['activated_requested_toy']and t['source_controller_unchanged']
  trials.append(entry)
assert len(cases)==2 and len(frames)==61 and len(trials)==18 and sum(x['observer_checks']for x in cases)==84
source_count=sum(x['bounded_original_source']for x in frames);candidate_count=sum(x['nonruntime_candidate']for x in frames);assert source_count==39 and candidate_count==18 and len(frames)-source_count-candidate_count==4
source_trials=[x for x in trials if x['mode']=='ORIGINAL_SOURCE'];candidate_trials=[x for x in trials if x['mode']=='LOCAL_NONRUNTIME_STAR_REUSE'];assert len(source_trials)==12 and len(candidate_trials)==6 and sum(x['activated_requested_toy']for x in source_trials)==8
wr('CAPTURE_INDEX.json',{'cases':cases,'captures':frames,'original_source_frames':source_count,'excluded_candidate_frames':candidate_count,'excluded_bootstrap_frames':4,'raw_frames':len(frames),'scope':'Actual original source and explicitly separate local prototype; no state/alias/acceptance credit for candidate/boot frames.'})
wr('INPUT_OUTCOMES.json',{'source_revision':D,'trials':trials,'source_trials':12,'source_activations':8,'source_glow_center_defocus_walk':4,'source_arrow_tip_activations':6,'source_seesaw_center_activations':2,'prototype_center_trials':6,'prototype_center_activations':6,'actual_input_executed':True,'actual_child_behavior_verified':False,'scope':'Source slide/swing centers clear focus and start walking; their tips activate. Seesaw center/tip activate. Prototype badge centers activate through original controller; child/owner/new-use acceptance remains open.'})
wr('CANDIDATE_GEOMETRY.json',{'sample_id':'FV-CAND-R80-STAR-01','role_id':'FVR-5344465CE503','source_revision':D,'source_asset':'assets/mg/star.png','source_sha256':sha(git('show',D+':assets/mg/star.png')),'source_rgb_and_aspect_preserved':True,'whole_bitmap_used':True,'native_nominal_long_edge_px':72,'native_pulse_fraction':.025,'native_center_upward_radius_fraction':.45,'measurements':geometry,'minimum_card_to_hit_boundary_margin_px':min(x['native_hit_radius']-x['farthest_card_corner_distance']for x in geometry),'flat_cue_visuals_retired_in_prototype_only':True,'production_fallbacks_retired':False,'runtime_verified_replacement':False})
refs={x['path']:{k:x[k]for k in ['path','revision','bytes','sha256']}for x in rd(O/'DELIVERY_SOURCE_REFERENCES.json')['files']}
for row in rd(P/'REUSE_INVENTORY.json')['shortlist']:refs[row['path']]={k:row[k]for k in ['path','revision','bytes','sha256']}
for path,states in sorted(textures.items()):
 raw=git('show',D+':'+path);refs.setdefault(path,{'path':path,'revision':D,'sha256':sha(raw),'bytes':len(raw)})
 refs[path]['present_in_native_scene_snapshot_ids']=sorted(states);refs[path]['qualification']='Scene-tree source binding may be offscreen/occluded; use exact native captures for state-local visual review, no pixel/acceptance credit from a reference alone.'
wr('DELIVERY_SOURCE_REFERENCES.json',{'files':sorted(refs.values(),key=lambda x:x['path']),'scope':'Exact existing current source/scene/provenance/art dependencies; whole approved source reused locally, no new external generation export or pixel acceptance.'})
functions=rd(O/'SOURCE_BINDINGS.json')['source_functions'];wr('SOURCE_BINDINGS.json',{'source_revision':D,'current_owner_graph_reference':{'path':(O/'SOURCE_OWNER_GRAPH.json').relative_to(R).as_posix(),'revision':B,'sha256':sha((O/'SOURCE_OWNER_GRAPH.json').read_bytes()),'parsed_current_scripts':313,'allcaller_closure':False},'source_functions':functions,'exact_sources':sorted(refs.values(),key=lambda x:x['path']),'role_id':'FVR-5344465CE503','scope_caption_qualification':'SCOPE_CLARIFICATION.json','source_or_candidate_acceptance':False})
s=rd(O/'SUMMARY.json');s.update(revision='FV-AUDIT-20261016-R80',topic_baseline=B,source_revision=D,native_cases=2,healthy_cases=2,healthy_observer_checks=84,new_native_frames=61,new_bounded_contexts=39,new_excluded_diagnostics=22,retained_bounded=6451,retained_excluded=3528,retained_native_events=9979,new_roles=0,new_families=0,new_alias_credits=0,new_reuse_samples=1,current_role_samples_awaiting_review=1,samples_awaiting_review_global=None,source_status='ACTUAL_SOURCE_GLOW_CENTER_TIP_INPUT_CONFIRMED;SEPARATE_APPROVED_STAR_REUSE_PROTOTYPE',source_extraction_tests=0,new_analysis_tests=8,language_semantic_checks=0,source_glow_center_gesture_verified=True,source_input_trials=12,candidate_input_trials=6,candidate_center_activations=6,candidate_is_production=False,production_cue_still_flat=True,source_eligible_reuse_asset=True,reuse_ready=False,drawing_required=None,limits='Original actual input across3toys/twoaspects confirms slide/swing glow centers walk/defocus and all tips activate. One separate local whole-bitmap approved-star reuse sample retires the source gradient/polygon visuals only in ignored prototype; all6painted-center taps activate through unchanged source controller and full bitmap bounds remain inside original hit disks. Candidate/boot22frames excluded from current source context; no new role/family/alias/art generation/production change or accepted removal. Star motif/readability/occlusion/full motion/caller/QA11/device/child/owner/global inventory remain open. Raw generic scope caption retained and clarified against explicit modes/trials.');wr('SUMMARY.json',s)
wr('CANDIDATE_SAMPLE.json',{'sample_id':'FV-CAND-R80-STAR-01','role_id':'FVR-5344465CE503','source_revision':D,'source':rd(P/'REUSE_INVENTORY.json')['shortlist'][0],'method':'Declared local whole-source Sprite2D reuse, uniform aspect-preserving scale and authoredRGB; alpha/size-only focus cadence. No source pixel edit, rotation, generation or production integration.','consumers':['slide','swing','seesaw'],'native_aspects':[[1280,720],[1600,720]],'geometry':'CANDIDATE_GEOMETRY.json','actual_input':'INPUT_OUTCOMES.json','context':'CAPTURE_INDEX.json','state':'NONRUNTIME_REUSE_SAMPLE_AWAITING_NEW_USE_REVIEW','review_gaps':['Star may imply reward/completion rather than selection; original downward pointer meaning is absent','Badge overlaps equipment silhouette; exact motif/placement/occlusion and phone recognition require review','Source untouched in production; allcaller/fallback/QA11/device/child/owner evidence incomplete'],'approved':False,'integrated':False,'runtime_verified_replacement':False,'accepted_removed':0,'generation_calls':0})
print('R80_DERIVED 61raw39source22excluded;84checks;12source+6candidateinputs;1reuseSample;263/35;0accepted',flush=True)