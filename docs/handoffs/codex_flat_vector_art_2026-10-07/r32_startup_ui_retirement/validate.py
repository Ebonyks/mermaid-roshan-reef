from pathlib import Path
import json,hashlib,subprocess,re,sys
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r31_startup_ui_context';BASE='a587e4ec5e82dbc86d52115ba41f3ae37e2e24f1'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def blobs(refs):
 refs=list(dict.fromkeys(refs));raw=subprocess.check_output(['git','cat-file','--batch'],cwd=R,input=''.join(x+'\n' for x in refs).encode());result={};i=0
 for ref in refs:
  end=raw.index(b'\n',i);head=raw[i:end].split();assert head[1]==b'blob',ref;n=int(head[2]);result[ref]=raw[end+1:end+1+n];i=end+1+n+1
 return result
sources=rd(P/'SOURCES.json')['sources'];pr=rd(P/'CONTEXT_PREREQUISITE.json');UID=rd(P/'UID_GUARD.json');refs=[x['revision']+':'+x['path'] for x in sources if x['revision']]+[x['revision']+':'+x['path'] for x in pr['checks']]+[BASE+':'+x['path'] for x in UID['checks']]+[BASE+':scripts/start_menu.gd'];B=blobs(refs)
for x in sources:
 raw=(R/x['path']).read_bytes();b=raw if x['revision'] is None else B[x['revision']+':'+x['path']];assert len(b)==x['bytes'] and sha(b)==x['sha256'];assert len(raw)==x['native_read_bytes'] and sha(raw)==x['native_read_sha256']
assert pr['status']=='ALL_SELECTED_CONTEXT_FILES_ANONYMOUSLY_VERIFIED_BEFORE_PRODUCTION_OR_PROBE_EDIT' and pr['file_count']==len(pr['checks'])==87
for x in pr['checks']:b=B[x['revision']+':'+x['path']];assert len(b)==x['bytes'] and sha(b)==x['sha256'] and x['http_status']==200
assert len(UID['checks'])==85 and UID['Git_only_newline_differences']==84
for x in UID['checks']:
 raw=(R/x['path']).read_bytes();b=B[BASE+':'+x['path']];assert len(raw)==x['working_bytes'] and sha(raw)==x['working_sha256'] and len(b)==x['Git_bytes'] and sha(b)==x['Git_sha256'] and raw.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
for n in ['FOCUSED_GATES.json','IMPORT.json','STATIC_GATES.json']:assert rd(P/n)['status']=='PASS'
assert len(rd(P/'FOCUSED_GATES.json')['commands'])==8 and all(x['exit_code']==0 for x in rd(P/'FOCUSED_GATES.json')['commands'])
assert len(rd(P/'CAPTURE_SCRIPT_GATES.json'))==3 and all(x['exit_code']==0 for x in rd(P/'CAPTURE_SCRIPT_GATES.json')) and rd(P/'LAUNCH.json')['returncode']==0
neg=rd(P/'BASELINE_NEGATIVE.json');assert neg['status']=='EXPECTED_BASELINE_FAILURE_VERIFIED' and neg['exit_code']==1 and len(neg['actual_failure_rows'])==2 and neg['expected_failed_checks']==1
old=B[BASE+':scripts/start_menu.gd'].decode();new=(R/'scripts/start_menu.gd').read_text();a=old.index('func _add_button_finish');b=old.index('func _build_options',a);c=new.index('func _add_button_finish');d=new.index('func _build_options',c);assert old[:a]==new[:c] and old[b:]==new[d:];fn=new[c:d];assert fn.count('StorybookUI.add_pearl')==2 and not any(t in fn for t in ['InsetHighlight','PearlSheen','Sparkle','create_tween','StyleBoxFlat','Label.new'])
base=['normal_startup','passive_2s','passive_26s','options_open_pressed','options_open_released','music_off_pressed','music_off_released','music_on_pressed','music_on_released','mic_off_pressed','mic_off_released','mic_on_pressed','mic_on_released','options_close_pressed','options_close_released','declared_focus_out','declared_focus_in']
extra=['newgame_request_pressed','newgame_request_released','newgame_armed','newgame_short_hold','newgame_hold_cancelled','keep_saved_pressed','keep_saved_released','continue_pressed','natural_continue_world','declared_menu_reentry','reentry_idle_1s','continue_again_pressed','natural_continue_after_reentry']
frames=[];manifests=sorted((P/'native').glob('*/*/capture_manifest.json'));assert len(manifests)==4
for f in manifests:
 data=rd(f);e=data['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert data['source_baseline']==BASE and data['quality']=='speedy' and data['rendering_method']=='mobile' and data['display_server']!='headless' and not data['errors'] and not data['teardown_main_valid']
 assert data['normal_save_before']==data['normal_save_after']==data['normal_save_after_teardown'] and len(data['normal_save_before'])==8 and data['initial_progress']==data['final_progress']
 assert '/profiles/startup/' in data['private_profile_path'].replace('\\','/') and [x['id'] for x in data['states']]==base+(extra if data['variant']=='saved_legacy' else [])
 for field,path in [('production_menu_sha256','scripts/start_menu.gd'),('shared_ui_sha256','scripts/storybook_ui.gd'),('production_director_sha256','scripts/living_world.gd'),('regression_probe_sha256','scripts/probe_start_menu_new_game.gd')]:assert data[field]==sha((R/path).read_bytes())
 states={x['id']:x for x in data['states']};previous=-1
 olddata=rd(O/'native'/f.parent.parent.name/f.parent.name/'capture_manifest.json');oldstates={x['id']:x for x in olddata['states']}
 for x in data['states']:
  assert x['elapsed_seconds']>previous;previous=x['elapsed_seconds'];present=x['presentation'];assert not present['boot_splash_present'] and not present['intro_overlay_present'] and present['fade_alpha']<=.02 and x['quality']=='speedy' and x['probe_stage_override']=='' and x['progress']==data['initial_progress'] and not x['retired_ui_nodes']
  for k in ['won','found']:assert x['progress'][k]==sorted(k for k,v in x['stored_progress_maps'][k].items() if bool(v))
  if x['expect_menu']:
   assert present['start_menu_active'] and present['start_menu_layer_present'] and present['intro_active'] and x['suspended'] and not x['layer_visible'] and not x['canvas_visible'] and x['idle_time']==0 and x['event_time']<0 and x['event_count']==0
   assert x['background']['visible'] and x['background']['texture']=='res://assets/ui/boot_splash_mermaid_roshan.png' and x['background']['sha256']=='d5127c4a6227baab05343dc10692e2f76f1dd59f22ca24a22329de402dbb8044'
   if x['id'] in oldstates:
    current={n['name']:n for n in x['ui_nodes'] if n['class']=='Button'};before={n['name']:n for n in oldstates[x['id']]['ui_nodes'] if n['class']=='Button'}
    assert set(current)==set(before)
    for name,n in current.items():
     for key in ['text','font_size','rect','canvas_rect','font_override','font_authority_meta']:assert n[key]==before[name][key],(f,x['id'],name,key)
  else:assert not present['start_menu_active'] and not present['intro_active'] and x['layer_visible'] and x['canvas_visible'] and not x['suspended'] and x['game']=='level2' and x['phase']=='promenade'
  q=f.parent/x['image']['file'];raw=q.read_bytes();im=Image.open(q).convert('RGB');assert sha(raw)==x['image']['sha256'] and len(raw)==x['image']['bytes'] and list(im.size)==data['aspect']==x['image']['dimensions'] and min(ImageStat.Stat(im).stddev)>20;frames.append(sha(raw))
 assert states['passive_26s']['elapsed_seconds']-states['normal_startup']['elapsed_seconds']>=26 and states['options_open_released']['options_visible'] and not states['options_close_released']['options_visible']
 for state,music,mic in [('music_off_released',False,True),('music_on_released',True,True),('mic_off_released',True,False),('mic_on_released',True,True)]:assert states[state]['music_on']==music and states[state]['mic_on']==mic
 if data['variant']=='saved_legacy':assert data['initial_progress']['pearls']==23 and data['initial_progress']['r32_keep_marker']==12345 and states['newgame_short_hold']['new_game_hold_active'] and not states['newgame_hold_cancelled']['new_game_hold_active'] and not states['keep_saved_released']['confirmation_visible']
assert len(frames)==94 and len(set(frames))==70
idx=rd(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==idx['retained_native_added']==94 and idx['current_bounded_file_count']==idx['current_unique_sha256_count']==70 and idx['excluded_duplicate_file_count']==24 and idx['directly_viewed_count']==12 and idx['directly_viewed_unique_count']==11
assert sum(x['context_credit'] for x in idx['frames'])==70
for x in idx['excluded_duplicate_views']:assert not x['context_credit'] and sha((P/x['path']).read_bytes())==sha((P/x['duplicate_of']).read_bytes())
view=rd(P/'REVIEW.json');assert len(view['ten_axes'])==10 and view['direct_native_views']==idx['directly_viewed_native_files'] and view['startup_role_retirement_count']==2 and view['global_accepted_removed']==0
if '--native-only' in sys.argv:print('R32_CURRENT_NATIVE_SOURCE_PASS:94ordered/70unique/24duplicate,12views11unique;oldsame-state actualButton geometry/text/font unchanged;retirednodes0/normal8saves/earnedprogress/teardown.87beforeeditcontext,UIDrawparity. DIAGNOSTIC ONLY');sys.exit(0)
V=rd(P/'FULL_VALIDATION.json');assert V['status']=='PASS_ALL_82_TRUSTED_NATIVE' and V['trusted_required']==V['trusted_passed']==len(V['rows'])==82 and V['normal_save_hashes_unchanged'] and V['tracked_sidecars_preserved']==1913
ci=(R/'scripts/ci.sh').read_text();roster=re.search(r'for p in (probe_reef_districts .*?); do',ci).group(1).split();assert [x['probe'] for x in V['rows']]==roster
for x in V['rows']:
 raw=(P/x['evidence']).read_bytes();assert sha(raw)==x['raw_output_sha256'] and len(raw)==x['raw_output_bytes'] and x['exit_code']==0 and x['result']=='PASS' and not re.search(V['failure_regex'],raw.decode(errors='replace')) and not re.search(V['resource_error_regex'],raw.decode(errors='replace'))
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 data=rd(P/n);before=rd(O/n);assert data['revision']=='FV-AUDIT-20261014-R32' and data['startup_ui_retirement']['startup_role_retirements']==2
 for k in ['pieces','supplemental_piece_records','entries','status_lanes','named_status_counts','startup_ambience_retirement','startup_ui_context','current_context_sample_lanes','current_partial_context_counts']:
  if k in before:assert data[k]==before[k],k
T=rd(P/'tally.json');before=rd(O/'tally.json');c=T['current_context'];assert c['exact_capture_count']==2948 and c['retained_native_capture_count']==c['retained_native_captures']==3379 and c['excluded_diagnostic_native_count']==431 and c['partial_overlapping_entries']==78 and c['complete_entries']==0 and c['entries_without_current_slice']==98
assert T['historical_totals'][:-1]==before['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
assert rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')
changes=subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).splitlines();assert changes==['scripts/probe_start_menu_new_game.gd','scripts/start_menu.gd'],changes
C=rd(P/'CAPTURE_CONTRACT.json');assert C['status']=='PASS_DIAGNOSTIC_ONLY' and C['fixture_hash']==sha((P/'capture_startup_ui_retirement.gd').read_bytes()) and C['native_files']==94 and C['credited_unique_frames']==70 and C['QA11'] is None and C['owner'] is None
print('R32_SOURCE_NATIVE_CANONICAL_FULL82_PASS:87beforeeditcontext/94native70unique24duplicate/8normalhashes/oldGUIgeometry/retired2roles,82trustedstrictzeroexit;2948bounded3379retained431excluded,56existingpartial12families,0acceptedremoved/globaltotalsunknown.')
