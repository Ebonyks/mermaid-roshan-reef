"""Build bounded R17 source-only pointer closure against exact Git bytes."""
from pathlib import Path
import json,hashlib,subprocess,re,datetime
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;V=H/'r16_pointer_candidate'
BASE='182f2e522a330b89bf7329b26516583160f343e0';PAYLOAD='a75dff44fdb594323b09069e9e53ccfeb42bc653';REV='FV-AUDIT-20261013-R17'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,d):
 (P/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def blob(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R,stderr=subprocess.PIPE)
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'scripts'],cwd=R,text=True).splitlines()
paths=[p for p in paths if p.endswith('.gd') and not Path(p).name.startswith('probe')]
raw={p:blob(p) for p in paths};texts={p:b.decode('utf-8-sig') for p,b in raw.items()}
census=[{'path':p,'revision':BASE,'bytes':len(b),'sha256':sha(b)} for p,b in sorted(raw.items())]
put('SCRIPT_CENSUS.json',{'schema':1,'revision':REV,'source_revision':BASE,'predicate':'Git-declared scripts/**/*.gd, basename not starting probe; includes prototypes/test helpers,not proof of live reachability','count':len(census),'files':census})
references=[];shared=[]
for p,t in texts.items():
 for i,l in enumerate(t.splitlines(),1):
  if 'assets/castle/training/ghost_hand.png' in l:references.append({'path':p,'line':i,'text':l,'status':'SOURCE_REFERENCE_ONLY_LIVE_VISIBILITY_AND_MISSING_PATH_UNREVIEWED'})
  if re.search(r'\b_draw_demo_finger\s*\(',l) and not l.startswith('func '):shared.append({'path':p,'line':i,'text':l})
S='scripts/opera_gesture_surface.gd';W='scripts/opera_career_world_2d.gd'
requested={S:['_load_widget_texture','_load_widget_set','_draw','_demo_finger_pose','_draw_demo_finger','_is_candymaker_pour','arm_only','set_fill'],
'scripts/opera_ballet_surface.gd':['_draw','_draw_ballet_demo','_draw_ghost_finger'],
'scripts/opera_teacher_surface.gd':['_draw','_draw_demo'],
'scripts/opera_boxing_surface.gd':['_draw','_draw_demo'],
'scripts/opera_chef_surface.gd':['_draw'],
'scripts/opera_geology_surface.gd':['_draw','_demo_finger_pose'],
'scripts/opera_racer_surface.gd':['_draw','_draw_race_controls','_demo_finger_pose'],
'scripts/encounter_gesture_guide_2d.gd':['_ready','_draw','_pressing'],W:['_widget_template','_draw_performance_rival','_is_chapter2_story_scene']}
excerpts=[]
for p,fs in requested.items():
 lines=texts[p].splitlines()
 for fn in fs:
  starts=[i for i,l in enumerate(lines) if l.startswith('func '+fn+'(')]
  if not starts:continue
  a=starts[0];b=next((i for i in range(a+1,len(lines)) if lines[i].startswith('func ')),len(lines))
  txt='\n'.join(lines[a:b])+'\n';excerpts.append({'path':p,'revision':BASE,'function':fn,'start_line':a+1,'end_line':b,'sha256_excerpt_lf':sha(txt.encode()),'text_lf':txt})
for a,b in [(263,354),(682,733),(766,780),(1267,1314),(2538,2578),(5094,5108)]:
 lines=texts[W].splitlines();txt='\n'.join(lines[a-1:b])+'\n';excerpts.append({'path':W,'revision':BASE,'section':'factory/phase/context/rival selector','start_line':a,'end_line':b,'sha256_excerpt_lf':sha(txt.encode()),'text_lf':txt})
put('SOURCE_EXCERPTS.json',{'schema':1,'revision':REV,'entries':excerpts,'hash_mode':'Exact Git file bytes in SOURCES; excerpts deliberately LF-joined lines with recorded ranges'})
prior=json.loads((V/'scene_coverage.json').read_text());career_map={c['costume']:c for c in prior['live_opera_careers']}
phases={};career=''
for i,l in enumerate(texts[W].splitlines()[262:354],263):
 m=re.match(r'\t"([a-z]+)": \[',l)
 if m:career=m[1];phases[career]=[]
 if '"name"' in l:
  d=dict(re.findall(r'"(name|mode|visual_context|widget)": "([^"]*)"',l));d['source_line']=i;phases[career].append(d)
assert len(phases)==15 and sum(map(len,phases.values()))==61
for c,old in career_map.items():assert [(x['name'],x['mode']) for x in phases[c]]==[(x['name'],x['mode']) for x in old['phases']]
independent={'ballerina':('scripts/opera_ballet_surface.gd','_draw_ballet_demo -> _draw_ghost_finger','FV-D2EA0464919A','demo_active and not armed_only and not completion_accepted and not _mode_complete()'),
'boxer':('scripts/opera_boxing_surface.gd','_draw_demo','FV-DAA9072B905A','demo_active and not completion_accepted'),
 'teacher':('scripts/opera_teacher_surface.gd','_draw_demo','FV-E1049E4945A3','not solved; demo returns unless add not joined,uncounted counters,or help_visible')}
rows=[]
for c,old in career_map.items():
 if c in independent:path,method,piece,guard=independent[c];uses=False
 else:
  path='scripts/opera_geology_surface.gd' if c=='geologist' else 'scripts/opera_racer_surface.gd' if c=='racer' else S
  method='_draw_demo_finger';piece='FV-1DC9F18904A8';guard='demo_active and not armed_only and not _completion_emitted' if c=='geologist' else 'demo_active';uses=True
 alternatives=[]
 if c=='chef':alternatives=['Chapter2 story scene selects OperaChefSurface; calls inherited pointer guarded by demo_active. Generic dev/Opera uses parent.']
 if c=='racer':alternatives=['kart_race uses _draw_race_controls and its pose override; other modes delegate super._draw()/super._demo_finger_pose().']
 phase_rows=[]
 for j,d in enumerate(phases[c]):
  phase_rows.append(dict(d,phase_index=j,pointer_branch='INDEPENDENT_PROCEDURAL_GUIDE' if not uses else 'OLD_WHOLE_HAND_IF_TEXTURE_PRESENT_OTHERWISE_GENERIC_DOT_ARC' if c=='candymaker' and d['mode']=='pourt' else 'GENERIC_DOT_ARC',missing_texture='Generic dot/arc branch unchanged' if uses else 'No hand texture dependency for this independent guide; other art fallbacks unreviewed'))
 rows.append({'route_id':f"opera.act.{old['save_bit']:02d}",'career':c,'source_phase_rows':phase_rows,'surface_path':path,'guide_method':method,'existing_piece_id':piece,'uses_shared_helper':uses,'draw_guard':guard,'factory_alternatives':alternatives,'source_only':True,'runtime_context_complete':False,'ten_axis_review':'PENDING actual mode/rest/action/contact/payoff captures and same-scene comparison; R16 covers Geode candidate only'})
source_paths=set(requested)|{x['path'] for x in references}|{'scripts/opera_house.gd','scripts/opera_performance_plan.gd','scripts/chapter_two_career_scene_adapter.gd','scripts/combat_tutorial.gd'}
source_paths={p for p in source_paths if p in raw}
sources=[dict(next(x for x in census if x['path']==p),role='Exact source-only pointer load/draw/consumer or selector evidence') for p in sorted(source_paths)]
for p in ['assets/castle/training/ghost_hand.png','assets_src/flat_vector_pointer_20261013/pointer_1024.png']:
 b=blob(p);sources.append({'path':p,'revision':BASE,'bytes':len(b),'sha256':sha(b),'role':'Preserved existing hand / R16 Geode-only candidate identity; no new image review in R17'})
put('SOURCES.json',{'schema':1,'revision':REV,'source_revision':BASE,'sources':sources,'source_only':True,'unchanged_runtime_against_previous_head':True})
audit={'schema':1,'revision':REV,'source_revision':BASE,'origin_dev':'831d0bbb155b99d75ef0289cc5cc694e0ef00c1e','piece_id':'FV-1DC9F18904A8','scope_id':'FVF-6CF7C85C1B16','status':'BOUNDED_SOURCE_CALLER_MAP_VERIFIED_CONTEXT_CLOSURE_OPEN','live_career_routes':15,'current_constant_phase_rows':61,'shared_helper_player_routes':12,'shared_helper_constant_phase_rows':49,'independent_player_routes':3,'independent_constant_phase_rows':12,'rows':rows,'shared_helper_call_sites':shared,'old_hand_path_references':references,'old_hand_source_reference_files':len({x['path'] for x in references}),
 'load_branch':{'predicate':'mode == pourt and visual_context == pour_candymaker and pour_demo_hand_texture != null','loader':'_load_widget_set resets hand null; pour family + pour_candymaker loads through ResourceLoader.exists/load','normal':'54px unpressed/58px pressed whole old hand,UV(.455,.91),alpha.96; return skips parent circles/arc','missing':'null hand falls through to 3 circles and pressing arc; no retirement'},
 'generic_branch':{'normal':'3 circles always; arc only pressing; used in remaining shared contexts','missing':'Same procedural pointer; it has no general texture dependency'},
 'phase_variants':['PHASES constant table61 is a bounded selector table,not all reachable states','Chapter2 adapter/config phase overrides may replace it','chapter2_tutorial truncates to first phase','PerformancePlan may rebuild two-act phase lists','Rival generic surface exists for non-Ballet two-act careers; armed_only/process-disabled/visibility cannot alone imply suppression because parent _draw guards only demo_active. Actual displayed rivalry states not captured here.'],
 'encounter_guide':{'source':'scripts/encounter_gesture_guide_2d.gd','actual_direct_caller':'scripts/combat_tutorial.gd:142','draw_guard':'anchor != Vector2.ZERO','normal':'Old hand82square,UV(.435,.875),10px unpressed lift; halo always,press arc and hold-stage arc remain','missing':'13px cream dot; halo/press/hold arcs remain; optional chip missing silently omits chip','scope':'Separate renderer; not affected by replacement of OperaGestureSurface._draw_demo_finger'},
 'limits':['String references establish potential dependencies only,not live reachability or visual weakness','No new source image/current capture/ten-axis human review','All old-hand consumers need actual normal/missing/rest/action/state context before repair','Inherited current registry route_refs retain historical broad candidate scope; R17 direct player route overlay corrects only this source boundary','No full function-scope disposition/global caller closure or zero-art claim'],
 'native_captures_added':0,'new_design_ids':0,'new_art_drawings':0,'samples_awaiting_review':1,'approved':0,'integrated':0,'runtime_verified_replacement':0,'accepted_removed':0,'whole_game_individual_total':None,'distinct_screen_total':None}
put('SOURCE_AUDIT.json',audit)
closure={k:audit[k] for k in ['revision','status','piece_id','scope_id','live_career_routes','current_constant_phase_rows','shared_helper_player_routes','shared_helper_constant_phase_rows','independent_player_routes','independent_constant_phase_rows','old_hand_source_reference_files','native_captures_added','new_design_ids','accepted_removed']};closure.update(evidence='SOURCE_AUDIT.json',source_only=True,source_revision=BASE,independent_piece_ids=[x[2] for x in independent.values()],global_caller_closure_complete=False,context_review_complete=False)
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=json.loads((V/n).read_text());d['revision']=REV;d['inherited_r16_reference_base']=V.relative_to(R).as_posix();d['pointer_caller_closure']=closure
 prior_res=d.get('reference_resolution');d['reference_resolution']={'inherited':prior_res,'R17':'SOURCE_AUDIT.json and current R17 fields resolve in this folder; inherited R16 fields/captures/reviews resolve at inherited_r16_reference_base or their prior explicit immutable bases. Earlier scope/history unchanged.'}
 if n=='per_piece.json':
  for x in d['pieces']:
   if x['id']=='FV-1DC9F18904A8':x['pointer_caller_closure']=dict(closure,direct_player_route_refs=[x['route_id'] for x in rows if x['uses_shared_helper']],historical_route_refs_retained=True)
   if x['id'] in closure['independent_piece_ids']:x['pointer_caller_boundary']={'revision':REV,'evidence':'SOURCE_AUDIT.json','uses_shared_helper':False,'source_only':True,'runtime_review':None,'accepted_removed':0}
 if n=='scene_coverage.json':
  for x in d['entries']:
   m=next((r for r in rows if r['route_id']==x['id']),None)
   if m:x['pointer_source_boundary']={'revision':REV,'evidence':'SOURCE_AUDIT.json','uses_shared_helper':m['uses_shared_helper'],'existing_piece_id':m['existing_piece_id'],'source_only':True,'no_runtime_coverage_credit':True}
 if n=='tally.json':
  d['historical_totals'].append({'revision':'FV-AUDIT-20261013-R16','immutable_payload_revision':PAYLOAD,'immutable_receipt_revision':BASE,'known_designs':225,'families':30,'bounded_captures':2138,'retained_native':2252,'excluded':114,'samples_awaiting_review':1,'partial_entries':77,'complete_entries':0,'without':99,'accepted_removed':0,'all_game_individual_piece_total':None})
  d['current_context']['source_revision']=BASE;d['phase']='BOUNDED_POINTER_SOURCE_CALLER_AUDIT';d['publication']={'status':'PENDING_PUBLICATION','candidate_sample_count':1,'accepted_removed':0};d['current_ci']={'prior_R16_receipt_head':BASE,'prior_run':38429525625,'status':'IN_PROGRESS_AT_INITIAL_CHECK','evidence':'PREVIOUS_HEAD_CI.json','local_trusted_suite':'Inherited R16 FULL_VALIDATION.json,82/82 over unchanged runtime bytes; no rerun for source-only documents','new_R17_exact_head':'PENDING_AFTER_PUBLICATION'}
 put(n,d)
README='''# R17 shared-pointer caller audit

Source-only evidence at `182f2e522a330b89bf7329b26516583160f343e0`, reconciled with `origin/dev` `831d0bbb155b99d75ef0289cc5cc694e0ef00c1e`.

The existing shared finger ID `FV-1DC9F18904A8` reaches 12 player career routes and 49 of the 61 current constant phase rows. Ballet, Boxer and Teacher bypass it with their own existing guide IDs. This corrects the direct-caller boundary; it does not grant runtime or style coverage.

CandyMaker SYRUP alone can use the old whole hand. A missing hand falls back to the procedural dots/ring. Other shared modes already use that procedural branch. Replacing the Geode pointer therefore does not retire these fallbacks. The separate encounter guide keeps its own old hand, halo, press/hold arcs and missing-hand dot.

See [source audit](SOURCE_AUDIT.json), [exact source hashes](SOURCES.json), [method/selector excerpts](SOURCE_EXCERPTS.json), and [full declared script census](SCRIPT_CENSUS.json). The old-hand path-reference list includes prototypes and test helpers; each row requires live route/state tracing. It is not a count of new drawings or accepted removals. Chapter 2 overrides, performance phases and rival surfaces retain explicit coverage gaps.

The [registry](per_piece.json), [coverage](scene_coverage.json), [backlog](CONGRUENCY_BACKLOG.json) and [tally](tally.json) preserve stable IDs and historical evidence. Unchanged R16 evidence resolves in `../r16_pointer_candidate/`; earlier immutable bases remain explicit. R16's single painted hand is still a Geode-only candidate awaiting review. No new art or runtime code was produced here.

225 known records / 30 families; one sample awaiting review; 2,138 bounded native captures / 2,252 retained, 114 excluded; 77 partial / zero complete / 99 without a current slice among 176 overlapping route entries. The 369 primitive scopes retain 18 inventory dispositions and 351 unresolved scopes; two additional compositor scopes remain incomplete. Whole-game individual and distinct screen/state totals remain unknown. Zero approved, integrated, runtime-verified replacements or accepted removals.

Next bounded work: current-context normal and missing-hand captures for CandyMaker SYRUP, including contour, material, palette, light, perspective, scale, contact, occlusion, readability and action-state comparison. Then choose its source-bound repair using the existing R16 candidate only if exact-purpose scene fit earns review. Independent Ballet/Boxer/Teacher and outside-Opera consumers continue as separate items. All QA11, natural route, device, child and owner lanes remain open.

[Manifest](MANIFEST.json) declares every exact immutable dependency. [Remote receipt](REMOTE_VERIFICATION.json) follows anonymous byte verification; [receipt gates](RECEIPT_GATES.json) verify final metadata. Public publication is evidence delivery, not artwork acceptance. The mission remains open.
'''
(P/'README.md').write_text(README,encoding='utf-8',newline='\n')
current=json.loads((H/'CURRENT.json').read_text());current.update(revision=REV,current_entry='r17_pointer_callers/README.md',current_per_piece='r17_pointer_callers/per_piece.json',current_scene_coverage='r17_pointer_callers/scene_coverage.json',current_tally='r17_pointer_callers/tally.json',current_backlog='r17_pointer_callers/CONGRUENCY_BACKLOG.json',current_manifest='r17_pointer_callers/MANIFEST.json',current_ci_evidence='r17_pointer_callers/tally.json',immutable_r16_receipt_revision=BASE)
(H/'CURRENT.json').write_text(json.dumps(current,indent=2)+'\n',encoding='utf-8',newline='\n')
print('R17_SOURCE_AUDIT',len(census),'scripts;',len(sources),'bound sources;',len(references),'old-hand references;',len(shared),'shared calls;15routes/61rows/12shared/3independent')
