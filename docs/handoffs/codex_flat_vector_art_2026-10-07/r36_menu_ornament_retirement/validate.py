from pathlib import Path
import json,hashlib,subprocess,re,sys
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r35_menu_panel_reuse';BASE='9730f40bbe725b71e2655653d04d5fea5d27bf34'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
assert rd(P/'CONTEXT_PREREQUISITE.json')['status']=='ALL_SELECTED_CURRENT_CONTEXT_ANONYMOUSLY_VERIFIED_BEFORE_FIXTURE_EDIT'
pr=rd(P/'CONTEXT_PREREQUISITE.json');assert pr['file_count']==len(pr['checks'])==37
for x in pr['checks']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256'] and x['http_status']==200
for x in rd(P/'SOURCES.json')['sources']:
 b=git('show',x['revision']+':'+x['path']);actual=(R/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes'];assert actual.replace(b'\r\n',b'\n')==b if x['path'].endswith('.gd') else actual==b
assert git('diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot').decode().strip()==''
for name in ['SIDECAR_GUARD.json']:
 d=rd(P/name);assert d['status']=='EXACT_PRE_RUN_WORKING_BYTES_PRESERVED' and d['tracked_paths']==len(d['sha256'])==1998 and d['changed_restored']==0
 for path,h in d['sha256'].items():assert sha((R/path).read_bytes())==h,path
expected=['original_source_baseline','painted_before_retirement','normal_startup']+['declared_style_'+x for x in ['normal','hover','pressed','hover_pressed','focus','disabled']]+['declared_actual_focus','passive_2s','options_open_pressed','options_open_released','declared_music_focus']+[s+'_'+k for s in ['music_off','music_on','mic_off','mic_on','options_close'] for k in ['pressed','released']]+['declared_focus_out','declared_focus_in']
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
  old=oldstates.get(x['id'],oldstates['normal_startup']);a={n['name']:n for n in x['ui_nodes'] if n['class']=='Button'};b={n['name']:n for n in old['ui_nodes'] if n['class']=='Button'};assert a.keys()==b.keys()
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
assert len(current_hashes)==130
idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['frames'])==130 and idx['current_unique_sha256_count']==len(set(current_hashes)) and idx['current_bounded_file_count']==sum(x['context_credit'] for x in idx['frames']) and idx['excluded_diagnostic_native']==130-idx['current_bounded_file_count']
prior_hashes={x['sha256'] for n in ['r35_menu_panel_reuse','r34_menu_focus_repair','r33_menu_material_reuse','r32_startup_ui_retirement'] for x in rd(P.parent/n/'CAPTURE_INDEX.json')['frames']};credited=[x for x in idx['frames'] if x['context_credit']];assert len({x['sha256'] for x in credited})==idx['current_bounded_file_count'] and not ({x['sha256'] for x in credited}&prior_hashes)
for x in idx['frames']:assert len((P/x['path']).read_bytes())==x['bytes'] and sha((P/x['path']).read_bytes())==x['sha256']
assert idx['directly_viewed_count']==16 and len(idx['directly_viewed_native_files'])==16 and idx['directly_viewed_unique_count']==len({sha((P/x).read_bytes()) for x in idx['directly_viewed_native_files']}) and idx['excluded_failed_run_native']==0
v=rd(P/'REVIEW.json');assert len(v['ten_axes'])==10 and v['direct_native_views']==idx['directly_viewed_native_files'] and v['status']=='NAMED_MENU_ORNAMENT_NEIGHBOR_CONGRUENCY_REPAIRED_IN_ISOLATED_CANDIDATE_ACCEPTANCE_OPEN' and v['accepted_removed']==0
comparison=rd(P/'PANEL_COMPARISON.json');assert len(comparison['rows'])==12 and comparison['QA11'] is None
for row in comparison['rows']:
 before=row['before'];after=row['candidate'];assert before['style_class']=='StyleBoxFlat' and after['style_class']=='StyleBoxTexture'
 for key in row['preserved_fields']:assert before[key]==after[key]
 assert after['texture_sha256']=='ab4926b5c99c3c6db0efcb4a20a75a9128276e085189bf51f947025659525893' and after['texture_margins']==[36,36,36,36] and after['draw_center'] and after['content_margins']==[18,12,18,12]
for f in sorted((P/'native').glob('*/*/capture_manifest.json')):
 d=rd(f);original={x['name']:x for x in d['states'][0]['panel_nodes']};assert len(original)==3
 for state in d['states']:
  panels=state['panel_nodes'];assert len(panels)==(3 if state['expect_menu'] else 0)
  for panel in panels:
   old=original[panel['name']]
   for key in ['rect','canvas_rect','mouse_filter','node_children','content_margins']:assert panel[key]==old[key]
   if state['id']=='original_source_baseline':assert panel['style_class']=='StyleBoxFlat'
   else:assert panel['style_class']=='StyleBoxTexture' and panel['texture_sha256']=='ab4926b5c99c3c6db0efcb4a20a75a9128276e085189bf51f947025659525893'
orn=rd(P/'ORNAMENT_COMPARISON.json');assert len(orn['rows'])==4 and orn['target_nodes_per_menu_build']==31 and orn['crest_nodes']==3 and orn['blue_pearl_nodes']==28
for f in sorted((P/'native').glob('*/*/capture_manifest.json')):
 d=rd(f);assert len(d['ornament_retirements'])==(2 if d['variant']=='saved_legacy' else 1)
 before_names=None
 for batch in d['ornament_retirements']:
  assert len(batch['before'])==batch['count']==31 and batch['after']==[] and batch['only_decorative_mouse_ignore']
  assert len({x['name'] for x in batch['before']})==31 and all(x['mouse_filter']==2 and (x['storybook_pearl'] or x['storybook_shell']) for x in batch['before'])
  assert sum(x['storybook_shell'] for x in batch['before'])==3 and sum(x['storybook_pearl'] for x in batch['before'])==28
  assert all(x['script']=='res://scripts/shell_ornament.gd' for x in batch['before'] if x['storybook_shell'])
  names={x['name'] for x in batch['before']};assert before_names is None or names==before_names;before_names=names
 for state in d['states']:
  pre=state['id'] in ['original_source_baseline','painted_before_retirement'];assert len(state['ornament_nodes'])==(31 if pre else 0)
  assert state['ornaments_retired'] is (not pre)
  if pre:assert {x['name'] for x in state['ornament_nodes']}==before_names
for row in orn['rows']:
 for key,hashkey in [('negative_before_frame','negative_sha256'),('current_after_frame','current_sha256')]:assert sha((R/row[key]).read_bytes())==row[hashkey]
caller=rd(P/'CALLER_CLOSURE.json');assert len(caller['calls'])==caller['direct_literal_shared_style_calls'] and len({x['path'] for x in caller['calls']})==caller['source_files']
assert caller['production_calls']+caller['probe_calls']==len(caller['calls'])
for row in caller['calls']:
 b=git('show',BASE+':'+row['path']);assert sha(b)==row['source_sha256'] and b.decode('utf-8-sig').splitlines()[row['line']-1].strip()==row['source_text'] and re.search(r'StorybookUI\.(adorn_panel|add_shell_crest|add_pearl)\s*\(',row['source_text'])
for row in caller['additional_shared_self_helper_calls']:assert git('show',BASE+':'+row['path']).decode('utf-8-sig').splitlines()[row['line']-1].strip()==row['source_text']
patch=rd(P/'CANDIDATE_CHANGE.json');raw=patch['utf8_patch'].encode();assert len(raw)==patch['decoded_bytes'] and sha(raw)==patch['decoded_sha256']
q=subprocess.run(['git','diff','--no-index','--',str(O/'capture_menu_panel_reuse.gd'),str(P/'capture_menu_ornament_retirement.gd')],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert q.returncode==1 and q.stdout==raw
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n);assert d['revision']=='FV-AUDIT-20261014-R36' and d['menu_ornament_retirement']['new_context_credits']==idx['current_bounded_file_count']
 for k in ['pieces','supplemental_piece_records','entries','status_lanes','named_status_counts','startup_ui_retirement','startup_ambience_retirement','menu_material_reuse','current_context_sample_lanes','current_partial_context_counts','menu_focus_repair','menu_panel_reuse']:
  if k in old:assert d[k]==old[k],k
T=rd(P/'tally.json');old=rd(O/'tally.json');assert T['historical_totals'][:-1]==old['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
c=T['current_context'];assert c['exact_capture_count']==old['current_context']['exact_capture_count']+idx['current_bounded_file_count'] and c['retained_native_capture_count']==c['retained_native_captures']==old['current_context']['retained_native_capture_count']+130 and c['excluded_diagnostic_native_count']==old['current_context']['excluded_diagnostic_native_count']+130-idx['current_bounded_file_count'] and c['partial_overlapping_entries']==78 and c['entries_without_current_slice']==98 and c['complete_entries']==0
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
assert rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')
retained=rd(P/'MACHINE_BASELINE.json')['retained_full82'];actual=git('show',retained['revision']+':'+retained['path']);assert retained['sha256']==sha(actual) and len(actual)==retained['bytes'] and (R/retained['path']).read_bytes()==actual and json.loads(actual)['trusted_passed']==82
raw=(P/'native_capture.log').read_text(encoding='utf-8');assert not re.search(r'SCRIPT ERROR:|ERROR:|\|FAIL\|',raw) and '"normal_save_unchanged":true' in raw
print('R36_SOURCE_NATIVE_CANONICAL_PASS:37publishedcontext/130native/',idx['current_bounded_file_count'],'newcredits/',idx['excluded_diagnostic_native'],'excluded/16views;31decorativeMOUSE_IGNOREtargets3crests28dots presentbefore/absentafter perbuild,controls/fonts/panels/privateprogress/normal8hashes/teardown/sourcepixels preserved. Ornamentcaller',caller['direct_literal_shared_style_calls'],'/',caller['source_files'],'partial.0acceptedremoved/globalinventory/source/menu/QA11devicechildowneropen.')
