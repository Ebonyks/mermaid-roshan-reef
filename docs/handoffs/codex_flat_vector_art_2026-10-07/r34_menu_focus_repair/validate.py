from pathlib import Path
import json,hashlib,subprocess,re,sys
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r33_menu_material_reuse';BASE='4adea70d348b0650a1ef490a42dbcfc39407e689'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
assert rd(P/'CONTEXT_PREREQUISITE.json')['status']=='ALL_SELECTED_CURRENT_CONTEXT_ANONYMOUSLY_VERIFIED_BEFORE_FIXTURE_EDIT'
pr=rd(P/'CONTEXT_PREREQUISITE.json');assert pr['file_count']==len(pr['checks'])==35
for x in pr['checks']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256'] and x['http_status']==200
for x in rd(P/'SOURCES.json')['sources']:
 b=git('show',x['revision']+':'+x['path']);actual=(R/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes'];assert actual.replace(b'\r\n',b'\n')==b if x['path'].endswith('.gd') else actual==b
assert git('diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot').decode().strip()==''
for name in ['SIDECAR_GUARD.json']:
 d=rd(P/name);assert d['status']=='EXACT_PRE_RUN_WORKING_BYTES_PRESERVED' and d['tracked_paths']==len(d['sha256'])==1998 and d['changed_restored']==0
 for path,h in d['sha256'].items():assert sha((R/path).read_bytes())==h,path
expected=['original_source_baseline','normal_startup']+['declared_style_'+x for x in ['normal','hover','pressed','hover_pressed','focus','disabled']]+['declared_actual_focus','passive_2s','options_open_pressed','options_open_released','declared_music_focus']+[s+'_'+k for s in ['music_off','music_on','mic_off','mic_on','options_close'] for k in ['pressed','released']]+['declared_focus_out','declared_focus_in']
saved=['newgame_request_pressed','newgame_request_released','newgame_armed','newgame_short_hold','newgame_hold_cancelled','keep_saved_pressed','keep_saved_released','continue_pressed','natural_continue_world','declared_menu_reentry','reentry_idle_1s','continue_again_pressed','natural_continue_after_reentry']
current_hashes=[]
for f in sorted((P/'native').glob('*/*/capture_manifest.json')):
 d=rd(f);i=rd(O/f.relative_to(P));e=d['engine'];assert e['major']==4 and e['minor']==7 and e['patch']==2 and e['status']=='stable' and e['build']=='official' and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
 assert d['source_baseline']==BASE and d['rendering_method']=='mobile' and d['quality']=='speedy' and d['display_server']!='headless' and d['errors']==[] and d['teardown_main_valid']==False
 assert [x['id'] for x in d['states']]==expected+(saved if d['variant']=='saved_legacy' else [])
 assert len(d['normal_save_before'])==8 and d['normal_save_before']==d['normal_save_after']==d['normal_save_after_teardown'] and d['initial_progress']==d['final_progress']
 assert d['initial_progress']['r32_keep_marker']==12345 if d['variant']=='saved_legacy' else True
 oldstates={x['id']:x for x in i['states']};states={x['id']:x for x in d['states']}
 for name in ['declared_music_focus','music_off_pressed','music_off_released']:
  node=next(z for z in states[name]['ui_nodes'] if z['name']=='StartMenuMusicButton');assert node['has_focus'] is True
  focus=next(z for z in node['material_states'] if z['state']=='focus');assert focus['draw_center'] is True
  assert focus['expand_margins']==([-2,-2] if name=='music_off_pressed' else [0,0])
 for x in d['states']:
  old=oldstates.get(x['id'],oldstates['options_open_released']);a={n['name']:n for n in x['ui_nodes'] if n['class']=='Button'};b={n['name']:n for n in old['ui_nodes'] if n['class']=='Button'};assert a.keys()==b.keys()
  for name,n in a.items():
   for k in ['text','font_size','rect','canvas_rect','font_override','font_authority_meta']:assert n[k]==b[name][k],(f,x['id'],name,k)
   if name in ['StartMenuContinueButton','StartMenuNewGameButton','StartMenuOptionsTab','StartMenuMusicButton','StartMenuQualityButton','StartMenuMicButton','StartMenuKeepGameButton','StartMenuConfirmNewGameButton']:
    resources=n['material_states'];assert len(resources)==6
    if x['id']!='original_source_baseline':
     for y in resources:assert y['class']=='StyleBoxTexture' and y['texture_sha256']=='ab4926b5c99c3c6db0efcb4a20a75a9128276e085189bf51f947025659525893' and y['margins']==[36,36,36,36] and y['region_rect']=='[P: (10.0, 23.0), S: (222.0, 209.0)]' and y['draw_center'] is True
  assert not x['isolated_candidate_active'] if x['id']=='original_source_baseline' else x['isolated_candidate_active']
  if x['expect_menu']:assert x['presentation']['start_menu_active'] and x['presentation']['intro_active'] and x['suspended'] and not x['layer_visible'] and not x['canvas_visible'] and x['retired_ui_nodes']==[] and x['background']['sha256']=='d5127c4a6227baab05343dc10692e2f76f1dd59f22ca24a22329de402dbb8044'
  else:assert not x['presentation']['start_menu_active'] and not x['presentation']['intro_active'] and x['layer_visible'] and x['canvas_visible'] and not x['suspended'] and x['game']=='level2' and x['phase']=='promenade'
  q=f.parent/x['image']['file'];raw=q.read_bytes();im=Image.open(q).convert('RGB');assert sha(raw)==x['image']['sha256'] and len(raw)==x['image']['bytes'] and list(im.size)==d['aspect']==x['image']['dimensions'] and min(ImageStat.Stat(im).stddev)>20;current_hashes.append(sha(raw))
 for state,music,mic in [('music_off_released',False,True),('music_on_released',True,True),('mic_off_released',True,False),('mic_on_released',True,True)]:assert states[state]['music_on']==music and states[state]['mic_on']==mic
 if d['variant']=='saved_legacy':assert states['newgame_short_hold']['new_game_hold_active'] and not states['newgame_hold_cancelled']['new_game_hold_active'] and not states['keep_saved_released']['confirmation_visible']
assert len(current_hashes)==126
idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['frames'])==126 and idx['current_unique_sha256_count']==len(set(current_hashes)) and idx['current_bounded_file_count']==sum(x['context_credit'] for x in idx['frames'])==33 and idx['excluded_diagnostic_native']==93
prior_hashes={x['sha256'] for x in rd(O/'CAPTURE_INDEX.json')['frames']}|{x['sha256'] for x in rd(P.parent/'r32_startup_ui_retirement/CAPTURE_INDEX.json')['frames']};credited=[x for x in idx['frames'] if x['context_credit']];assert len({x['sha256'] for x in credited})==33 and not ({x['sha256'] for x in credited}&prior_hashes)
for x in idx['frames']:assert len((P/x['path']).read_bytes())==x['bytes'] and sha((P/x['path']).read_bytes())==x['sha256']
assert idx['directly_viewed_count']==16 and len(idx['directly_viewed_native_files'])==16 and idx['excluded_failed_run_native']==0
v=rd(P/'REVIEW.json');assert len(v['ten_axes'])==10 and v['direct_native_views']==idx['directly_viewed_native_files'] and v['status']=='NAMED_FOCUS_SEAM_REPAIRED_IN_ISOLATED_CANDIDATE_ACCEPTANCE_OPEN' and v['accepted_removed']==0
comparison=rd(P/'FOCUS_COMPARISON.json');assert len(comparison['rows'])==4 and comparison['QA11'] is None
from PIL import ImageStat
for row in comparison['rows']:
 for prefix,pathkey,meanskey in [('old','old_focus_frame','old_mean_rgb'),('new','current_focus_frame','new_mean_rgb')]:
  path=R/row[pathkey];assert sha(path.read_bytes())==row['old_focus_sha256' if prefix=='old' else 'current_focus_sha256']
  means=[ImageStat.Stat(Image.open(path).convert('RGB').crop(tuple(box))).mean for box in row['paper_sample_boxes']];assert means==row[meanskey]
  value=max(abs(a-b) for a,b in zip(*means));assert value==row['old_max_channel_boundary_contrast' if prefix=='old' else 'new_max_channel_boundary_contrast']
 currentpath=R/row['current_focus_frame'];box=tuple(row['press_release_nontext_box']);press=ImageStat.Stat(Image.open(currentpath.parent/'music_off_pressed.png').convert('RGB').crop(box)).mean;release=ImageStat.Stat(Image.open(currentpath.parent/'music_off_released.png').convert('RGB').crop(box)).mean;assert press==row['pressed_mean_rgb'] and release==row['released_mean_rgb'] and max(abs(a-b) for a,b in zip(press,release))==row['pressed_release_max_channel_contrast']
 assert row['old_max_channel_boundary_contrast']>10 and row['new_max_channel_boundary_contrast']<5 and row['pressed_release_max_channel_contrast']>10 and row['focus_press_live']['has_focus'] is True and row['focus_press_live']['draw_mode']==1
caller=rd(P/'CALLER_CLOSURE.json');assert len(caller['calls'])==caller['direct_literal_shared_style_calls']==33 and len({x['path'] for x in caller['calls']})==caller['source_files']==17 and caller['production_calls']==30 and caller['probe_calls']==3
for row in caller['calls']:
 b=git('show',BASE+':'+row['path']);assert sha(b)==row['source_sha256'] and b.decode('utf-8-sig').splitlines()[row['line']-1].strip()==row['source_text']
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n);assert d['revision']=='FV-AUDIT-20261014-R34' and d['menu_focus_repair']['new_context_credits']==33
 for k in ['pieces','supplemental_piece_records','entries','status_lanes','named_status_counts','startup_ui_retirement','startup_ambience_retirement','menu_material_reuse','current_context_sample_lanes','current_partial_context_counts']:
  if k in old:assert d[k]==old[k],k
T=rd(P/'tally.json');old=rd(O/'tally.json');assert T['historical_totals'][:-1]==old['historical_totals'] and T['historical_totals'][-1]['immutable_final_route_revision']==BASE
c=T['current_context'];assert c['exact_capture_count']==3053 and c['retained_native_capture_count']==c['retained_native_captures']==3749 and c['excluded_diagnostic_native_count']==696 and c['partial_overlapping_entries']==78 and c['entries_without_current_slice']==98 and c['complete_entries']==0
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
assert rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')
retained=rd(P/'MACHINE_BASELINE.json')['retained_full82'];actual=git('show',retained['revision']+':'+retained['path']);assert retained['sha256']==sha(actual) and len(actual)==retained['bytes'] and (R/retained['path']).read_bytes()==actual and json.loads(actual)['trusted_passed']==82
raw=(P/'native_capture.log').read_text(encoding='utf-8');assert not re.search(r'SCRIPT ERROR:|ERROR:|\|FAIL\|',raw) and '"normal_save_unchanged":true' in raw
print('R34_SOURCE_NATIVE_CANONICAL_PASS:35publishedcontext/126native33newcredits93excluded/16views;fourbefore-seam-fail/current-clear diagnosticcomparisons andactualGUIpresscontrast,sourcecaller33/17.Originalgeometry/fonts/private8normalhashes/progress/teardown/sourcepixels preserved.3053bounded3749retained696excluded;0approvedintegratedacceptedremoved/globaltotalsunknown/QA11devicechildowneropen.')
