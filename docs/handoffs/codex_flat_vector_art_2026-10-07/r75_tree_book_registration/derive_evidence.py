from pathlib import Path
import os,json,hashlib,subprocess,importlib.util,math,io
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;D='dd799b2d43871b29d1d6e0503646308a194dad1e';B='715c7a230c159e70acae1cd0ddad727e88910cb9';OUT=Path(os.environ['R75_ANALYSIS_OUTPUT']).resolve();assert not OUT.exists(),'Use fresh scratch';OUT.mkdir(parents=True)
s=importlib.util.spec_from_file_location('a75derive',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def wr(n,d):A.write_document(OUT/n,d)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
cases=sorted((P/'native').iterdir());assert len(cases)==6
manifests={c.name:rd(c/'capture_manifest.json')for c in cases};leaf_binding=manifests['attempt2_tree_book_registered_1280']['hint_cycles'][-1]['samples'][0]['target_painted_leaf'];assert leaf_binding['atlas_path']=='res://assets/opera/tree_book_test/leaves_medicine.png'
leaf_raw=git('show',D+':assets/opera/tree_book_test/leaves_medicine.png');leaf=Image.open(io.BytesIO(leaf_raw)).convert('RGBA');alpha=leaf.getchannel('A');points={(x,y)for y in range(249)for x in range(255,513)if alpha.getpixel((x,y))>=64};components=[]
while points:
 start=min(points);points.remove(start);stack=[start];group=set()
 while stack:
  x,y=stack.pop();group.add((x,y))
  for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if n in points:points.remove(n);stack.append(n)
 components.append(group)
components.sort(key=lambda c:(-len(c),min(c)));assert [len(x)for x in components]==[20509,6585]
def semantic(tip,binding):
 x,y=tip;bx,by,bw,bh=binding['fit_box'];tw,th=binding['texture_size'];factor=min(bw/tw,bh/th);rw,rh=tw*factor,th*factor;ox,oy=bx+(bw-rw)/2,by+(bh-rh)/2
 if not(ox<=x<ox+rw and oy<=y<oy+rh):return {'component':'OUTSIDE_TEXTURE_FIT'}
 rx,ry,rw_src,rh_src=binding['region'];sx=rx+(x-ox)/rw*rw_src;sy=ry+(y-oy)/rh*rh_src;pixel=(int(sx),int(sy));kind='PRIMARY_SPOTTED_LEAF'if pixel in components[0]else'SPOTS_BADGE'if pixel in components[1]else'TRANSPARENT_OR_OTHER'
 return {'component':kind,'atlas_pixel':list(pixel),'atlas_subpixel':[sx,sy],'alpha':alpha.getpixel(pixel)}
files=[];case_rows=[];cycles=[];contracts=[];semantic_rows=[];state_comparisons=[]
for c in cases:
 m=manifests[c.name];res=rd(c/'RESULT.json');launch=rd(c/'LAUNCH.json');control=m['mode']=='control';v2=c.name.startswith('attempt2');variant='SOURCE_CONTROL'if control else'LEAF_SILHOUETTE_V2'if v2 else'EDGE_V1_SEMANTIC_REJECTED'
 assert res['exit_code']==0 and not res['timed_out'] and not res['script_or_shader_errors'] and res['normal_before']==res['normal_after'] and len(res['normal_after'])==11 and res['sidecars_exact'] and res['sidecar_after_count']==4088 and not res['source_byte_changes'] and res['fixture_dependency_unchanged']
 assert m['source_revision']==D and not m['actual_child_data'] and not m['production_changes'] and m['time_scale']==1 and not m['errors'] and all(x['pass']for x in m['checks'])
 for name,expected in launch['fixture_dependencies'].items():assert sha((c/name).read_bytes())==expected
 assert sha((c/'engine.log').read_bytes())==res['log_sha256']
 for st in m['states']:
  f=c/st['path'];raw=f.read_bytes();im=Image.open(io.BytesIO(raw));assert sha(raw)==st['sha256'] and list(im.size)==st['size'];bounded=control and st['classification']=='BOUNDED_CURRENT_CONTEXT'
  files.append({'case':c.name,'variant':variant,'id':st['id'],'path':f.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw),'decoded_rgba_sha256':sha(im.convert('RGBA').tobytes()),'dimensions':list(im.size),'classification':'BOUNDED_CURRENT_SOURCE_CONTEXT'if bounded else'EXCLUDED_DIAGNOSTIC','reason':'Current original-source selected context only'if bounded else'Startup room outside selected book context'if control else'Rejected first semantic placement retained;0source-context/acceptance credit'if not v2 else'Nonproduction geometry preview;0source-context/acceptance credit'})
 for cy in m['hint_cycles']:
  errors=[];margins=[];sem=[]
  for q in cy['samples']:
   x,y,w,h=q['target'];e=q['elapsed'];dx=0;dy=0
   if not control:
    if q['stage']<3:dy=-36
    else:dx=-51 if v2 else 0;dy=-114 if v2 else -44
   box=[x+w-68,y+h-55-math.sin(e*3)*9,80,80]if q['stage']<3 else[x+80,y+78+math.sin(e*3)*10,95,95];box[0]+=dx;box[1]+=dy;tip=[box[0]+217*box[2]/512,box[1]+447*box[3]/512];offset=q['native_target'][0]-x;assert offset in [0,160]
   errors.extend(abs(a-b)for a,b in zip(box,q['draw_box']));errors.extend(abs(a-b)for a,b in zip(tip,q['local_tip']));errors.extend([abs(q['native_tip'][0]-tip[0]-offset),abs(q['native_tip'][1]-tip[1])]);inside=x<=tip[0]<x+w and y<=tip[1]<y+h
   assert inside==q['inside'] and q['pointer_visible_by_source_branch'];margins.append(min(tip[0]-x,x+w-tip[0],tip[1]-y,y+h-tip[1]))
   if q['stage']==4:
    binding=q['target_painted_leaf']if v2 else leaf_binding
    if v2:assert binding==leaf_binding
    sem.append(semantic(q['local_tip'],binding))
  assert max(errors)<0.001 and len(cy['samples'])==cy['total'] and cy['end_phase']-cy['start_phase']>=math.tau-0.25
  assert cy['outside']==(cy['total']if control else 0)
  cycles.append({'case':c.name,'variant':variant,'id':cy['id'],'samples':cy['total'],'outside_original_target':cy['outside'],'phase_span':cy['end_phase']-cy['start_phase'],'minimum_inside_rect_margin_px':min(margins),'maximum_projection_error_px':max(errors)})
  if sem:
   counts={kind:sum(x['component']==kind for x in sem)for kind in sorted({x['component']for x in sem})}
   if v2:assert counts=={'PRIMARY_SPOTTED_LEAF':len(sem)}
   else:assert counts.get('PRIMARY_SPOTTED_LEAF',0)==0
   semantic_rows.append({'case':c.name,'variant':variant,'source_binding_mode':'Actual source AtlasTexture/fit metadata in every sample'if v2 else'Retrospective projection using byte-identical current source leaf function and actual v2 source AtlasTexture binding; not fabricated v1 metadata','component_counts':counts,'samples':sem})
 for ct in m['source_contracts']:
  assert ct['input_advanced']is(not control);assert ct['status']==('SOURCE_RENDERED_TIP_MISSES_ACTIONABLE_TARGET'if control else'CANDIDATE_RENDERED_TIP_ADVANCES_ORIGINAL_TARGET');contracts.append({'case':c.name,'variant':variant,**ct})
 for cmp in m['comparisons']:
  assert cmp['source_signature_unchanged']
  if v2:assert cmp['before']==cmp['after']
  state_comparisons.append({'case':c.name,'variant':variant,**cmp})
 assert all(x['source_teardown_disposed_preview']for x in m['teardown_checks'])
 states={x['id']:x['snapshot']for x in m['states']};dose=states['treatment_partial_canceled']['book']['treatment'];assert 0<dose<0.9
 for n in ['partial_reopen_book_open','reload_book_open']:assert states[n]['book']['stage']==4 and abs(states[n]['book']['treatment']-dose)<1e-6
 assert states['healthy_complete']['book']['stage']==states['healthy_reopen_book_open']['book']['stage']==5 and states['replay_started']['book']['stage']==0
 assert all(x['main']['stars']==0 and x['main']['pearls']==23 and x['main']['opera_progress']==0 for x in states.values());assert states['final_venue_restored']['disk']['unknown']=={'keep':[4,7],'token':'R75_SYNTHETIC_ONLY'}
 case_rows.append({'case':c.name,'variant':variant,'source_revision':D,'raw_frames':len(m['states']),'bounded':sum(x['classification']=='BOUNDED_CURRENT_SOURCE_CONTEXT'for x in files if x['case']==c.name),'excluded':sum(x['classification']=='EXCLUDED_DIAGNOSTIC'for x in files if x['case']==c.name),'observer_checks':len(m['checks']),'observer_passes':sum(x['pass']for x in m['checks']),'tip_input_advances':sum(x['input_advanced']for x in m['source_contracts']),'partial_dose':dose,'source_runtime_count':4425,'sidecar_count':4088,'normal_names':11,'observer_status':m['observer_status'],'semantic_or_art_acceptance':False})
old=rd(H/'r74_tree_book_context/SUMMARY.json');bounded=sum(x['bounded']for x in case_rows);excluded=sum(x['excluded']for x in case_rows);total=sum(x['raw_frames']for x in case_rows);assert (total,bounded,excluded)==(230,78,152)
summary={'revision':'FV-AUDIT-20261015-R75','topic_baseline':B,'source_revision':D,'stable_id':'FVR-C6005BD0881E','family':'tree_book_practice','native_cases':6,'source_control_cases':2,'source_control_checks':96,'rejected_first_variant_cases':2,'rejected_first_variant_checks':114,'final_variant_cases':2,'final_variant_checks':114,'all_observer_checks':324,'source_hint_tip_misses':8,'first_variant_input_advances':8,'final_variant_input_advances':8,'new_native_frames':total,'new_bounded_contexts':bounded,'new_excluded_diagnostics':excluded,'retained_bounded':old['retained_bounded']+bounded,'retained_excluded':old['retained_excluded']+excluded,'retained_native_events':old['retained_native_events']+total,'known_roles':254,'known_families':35,'new_roles':0,'new_families':0,'existing_partial_roles':75,'existing_partial_families':15,'supplemental_partial_roles':30,'catalogue_partial':92,'catalogue_without_current_slice':84,'catalogue_complete':0,'new_alias_credits':0,'source_original_status':'UNCHANGED_FLAT_HAND_AND_REPRODUCED_TIP_FAILURES','first_variant_status':'INPUT_PASSES_TREATMENT_SEMANTIC_PLACEMENT_REJECTED','final_variant_status':'ORIGINAL_PIXEL_GEOMETRY_AND_PROJECTED_PRIMARY_LEAF_PREVIEW_ONLY','registration_candidates_awaiting_review':1,'new_drawing_samples':0,'drawing_required':None,'reuse_ready':False,'generation_calls':0,'new_runtime_assets':0,'approved':0,'integrated':0,'runtime_verified_replacements':0,'accepted_removed':0,'all_game_artwork_total':None,'distinct_screen_total':None,'regression_total':None,'allcaller_closure':False,'mission_complete':False,'cases':case_rows,'limits':'Original-source synthetic native controls and visual-only candidate diagnostics. Source hand remains flat, material/contour congruency and painted replacement unresolved. Source-projected alpha-component proof is not independent DL-QA-11/live occlusion, final human/art, actual device/child/owner or global zero-art acceptance. Initial headless import raw-byte guard failure and exact EOL recovery kept separate.'}
wr('CAPTURE_INDEX.json',{'cases':case_rows,'files':files,'raw_frames':total,'bounded_source_contexts':bounded,'excluded_diagnostics':excluded,'scope':'Every230actual raw PNG retained. Only78new current original-source contexts credited; all148candidateframes plus4startup frames excluded from current source inventory review credits. No pixel edits, new artwork or complete route/acceptance.'})
wr('POINTER_MEASUREMENTS.json',{'status':'ORIGINAL_SOURCE_MISSES_REPRODUCED_FINAL_PREVIEW_TARGET_INPUT_PASSES','method':'Independent Python source-draw formula +actual childSprite position/scale/native transform/sourcealpha tip; natural complete bob cycles, original unchanged rects. Geometry and real input evidence only, not authoritative finalQA11.','cycles':cycles,'contracts':contracts,'accepted_removed':0})
wr('SEMANTIC_TARGET_CHECK.json',{'status':'FINAL_PREVIEW_POINTS_AT_PRIMARY_LEAF_ALL_SAMPLED_CYCLES','source_atlas_path':'assets/opera/tree_book_test/leaves_medicine.png','source_atlas_sha256':sha(leaf_raw),'source_revision':D,'actual_source_atlas_binding':leaf_binding,'primary_leaf_alpha64_pixels':len(components[0]),'badge_alpha64_pixels':len(components[1]),'primary_coordinate_sha256':sha(json.dumps(sorted(components[0]),separators=(',',':')).encode()),'cases':semantic_rows,'scope':'Read-only source projection against actual AtlasTexture fit and connected alpha64 components; largest leaf identified by actual source-sheet visual inspection.0modifiedpixels. Final2cases must sample primary leaf throughout fullbob. Rejectedv1mayhitbadge/transparentarea but0primaryleafsamples. This is diagnostic source geometry, not live decoded target layer/occlusion/QA11/device/child/owner proof.'})
wr('SOURCE_STATE_COMPARISONS.json',{'status':'ORIGINAL_SOURCE_INPUT_STATE_CLOCK_TARGETS_PRESERVED_AT_ATTACH_DETACH','comparisons':state_comparisons,'teardown':[{'case':n,'checks':m['teardown_checks']}for n,m in manifests.items()],'scope':'V2keeps full actual before/after signature dictionaries; v1original boolean records retained, no reconstructed v1raw signatures. Private save/normal/source raw guards separate in eachcase manifest/RESULT.'})
source=git('show',D+':scripts/opera_tree_book_test.gd');wr('SOURCE_BINDINGS.json',{'source_revision':D,'script':'scripts/opera_tree_book_test.gd','script_sha256':sha(source),'source_scope':'Exact original class/script/inputs and both existing _fit(hand) calls remain in production. Nonproduction helper mutates only original book.hand drawing resource and owns one Sprite2D/Node2D child. Base source reads hand only in initialization/two draw calls; no alternate input or fallback uses. Original state/action/target/clock source code unmodified.','hand_sha256':sha(git('show',D+':assets/castle/training/ghost_hand.png')),'source_runtime_count':4425,'source_sidecar_count':4088,'normal_save_name_count':11,'current_source_import':'IMPORT_EOL_RECOVERY.json:1102line-ending changes restored exactly;0non-EOL changes, old4041sidecarbytes preserved,47newgeneratedsidecars. Initial importer inner exit code unrecorded/notclaimed. Native six cases and syntax gates separate.','retained_source_scope_ids':['FVF-2BB366CA6FB9','FVF-1AEBA38572AF','FVCS-573FE366C862','FVCS-B8453FA7730D','FVCS-8B4F125AB56E'],'unclosed':['Standalone no-Main book and local Back','All shared-hand consumers/primitive fallbacks','Natural earned traversal/freshOS relaunch','Global captions/ambient overlays/wide margins','Painted hand replacement/congruency/identity and every source lifecycle variant','FinalQA11/runtime/device/child/owner and global inventory zero-art acceptance']})
wr('SUMMARY.json',summary);print('R75_DERIVATION_PASS',total,bounded,excluded,'checks',summary['all_observer_checks'],'source8misses/final8advances','allfinalleafsamples',flush=True)
