from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r30_startup_ambience_retirement';BASE='849a7de5fa65270d354cb7973ded63b464668988'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
S=rd(P/'SOURCES.json')
for x in S['sources']:
 b=subprocess.check_output(['git','show',BASE+':'+x['path']],cwd=R,stderr=subprocess.PIPE);raw=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];assert len(raw)==x['native_read_bytes'] and sha(raw)==x['native_read_sha256'];assert raw.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
assert rd(P/'LAUNCH.json')['returncode']==0 and len(rd(P/'CAPTURE_SCRIPT_GATES.json'))==3 and all(x['exit_code']==0 for x in rd(P/'CAPTURE_SCRIPT_GATES.json'))
ids=['normal_startup','options_open_pressed','options_open_released','music_off_pressed','music_off_released','music_on_pressed','music_on_released','mic_off_pressed','mic_off_released','mic_on_pressed','mic_on_released','options_close_pressed','options_close_released']
rows=[];manifests=sorted((P/'native').glob('*/*/capture_manifest.json'));assert len(manifests)==4
for f in manifests:
 d=rd(f);e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert d['source_baseline']==BASE and d['quality']=='speedy' and d['rendering_method']=='mobile' and d['display_server']!='headless' and not d['errors'] and not d['teardown_main_valid']
 assert d['normal_save_before']==d['normal_save_after']==d['normal_save_after_teardown'] and len(d['normal_save_before'])==8 and d['initial_progress']==d['final_progress']
 assert '/profiles/startup/' in d['private_profile_path'].replace('\\','/') and [x['id'] for x in d['states']]==ids
 for field,path in [('production_menu_sha256','scripts/start_menu.gd'),('shared_ui_sha256','scripts/storybook_ui.gd'),('production_director_sha256','scripts/living_world.gd'),('regression_probe_sha256','scripts/probe_living_world.gd')]:assert d[field]==sha((R/path).read_bytes())
 states={x['id']:x for x in d['states']};previous=-1
 for x in d['states']:
  assert x['elapsed_seconds']>previous;previous=x['elapsed_seconds'];pr=x['presentation'];assert x['expect_menu'] and pr['start_menu_active'] and pr['start_menu_layer_present'] and pr['intro_active'] and not pr['intro_overlay_present'] and not pr['boot_splash_present'] and pr['fade_alpha']<=.02
  assert x['quality']=='speedy' and x['probe_stage_override']=='' and x['suspended'] and not x['layer_visible'] and not x['canvas_visible'] and x['idle_time']==0 and x['event_time']<0 and x['event_count']==0 and x['progress']==d['initial_progress']
  for k in ['won','found']:assert x['progress'][k]==sorted(k for k,v in x['stored_progress_maps'][k].items() if bool(v))
  assert x['background']['visible'] and x['background']['texture']=='res://assets/ui/boot_splash_mermaid_roshan.png' and x['background']['sha256']=='d5127c4a6227baab05343dc10692e2f76f1dd59f22ca24a22329de402dbb8044'
  q=f.parent/x['image']['file'];b=q.read_bytes();im=Image.open(q).convert('RGB');assert sha(b)==x['image']['sha256'] and len(b)==x['image']['bytes'] and list(im.size)==d['aspect']==x['image']['dimensions'] and min(ImageStat.Stat(im).stddev)>20;rows.append(sha(b))
  for n in x['ui_nodes']:
   if 'coverage' in n:assert not n['missing_negative_10ffff_has_char'] and not n['font_override'] and n['font_class']=='FontFile' and n['font_resource_path']==''
  if x['id']!='normal_startup':assert x['input']['event'].startswith('raw engine touch0')
 assert states['options_open_released']['options_visible'] and not states['options_close_released']['options_visible']
 for state,music,mic in [('options_open_released',True,True),('music_off_pressed',True,True),('music_off_released',False,True),('music_on_pressed',False,True),('music_on_released',True,True),('mic_off_pressed',True,True),('mic_off_released',True,False),('mic_on_pressed',True,False),('mic_on_released',True,True)]:
  x=states[state];assert x['music_on']==music and x['mic_on']==mic
  byname={n['name']:n for n in x['ui_nodes']};assert byname['StartMenuMusicButton']['text']==('♫  MUSIC ON' if music else '♫̸  MUSIC OFF');assert byname['StartMenuMicButton']['text']==('🎤  SAY SPELLS' if mic else '🎤̸  SPELLS OFF')
 if d['variant']=='saved_legacy':assert d['initial_progress']['pearls']==23 and d['initial_progress']['r31_keep_marker']==12345
 assert any('InsetHighlight' in n['name'] for n in states['normal_startup']['ui_nodes']) and any('PearlSheen' in n['name'] for n in states['normal_startup']['ui_nodes']) and any('Sparkle' in n['name'] for n in states['normal_startup']['ui_nodes'])
assert len(rows)==len(set(rows))==52
idx=rd(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==idx['current_bounded_file_count']==idx['current_unique_sha256_count']==52 and idx['directly_viewed_count']==len(idx['directly_viewed_native_files'])==12
for x in idx['frames']:assert sha((P/x['path']).read_bytes())==x['sha256']
view=rd(P/'REVIEW.json');assert len(view['ten_axes'])==10 and view['direct_native_views']==idx['directly_viewed_native_files'] and view['acceptance']['owner'] is None and view['accepted_removed']==0
assert len(rd(P/'REUSE_AUDIT.json')['candidates'])==5 and rd(P/'REUSE_AUDIT.json')['approved_menu_replacements']==0
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n);assert d['revision']=='FV-AUDIT-20261014-R31' and d['startup_ui_context']['piece_ids']==['FV-276E68E0A9DA','FV-619466CA433F']
 for k in ['pieces','supplemental_piece_records','entries','status_lanes','named_status_counts','startup_ambience_retirement','current_retirement_acceptance_lanes','current_context_sample_lanes']:
  if k in old:assert d[k]==old[k],k
T=rd(P/'tally.json');old=rd(O/'tally.json');c=T['current_context'];assert c['exact_capture_count']==2878 and c['retained_native_capture_count']==c['retained_native_captures']==3285 and c['excluded_diagnostic_native_count']==407 and c['partial_overlapping_entries']==78 and c['complete_entries']==0 and c['entries_without_current_slice']==98
assert T['historical_totals'][:-1]==old['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
u=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');uo=rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert u['records'][:54]==uo['records'] and len(u['records'])==len({x['id'] for x in u['records']})==u['current_existing_named_records_with_partial_context']==56 and len({x['family'] for x in u['records']})==u['current_existing_families_with_partial_context']==12
assert T['current_partial_context_counts']['existing_named_records']==56
changed=subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).splitlines();assert not changed,changed
assert rd(P/'SOURCE_PARITY.json')['production_changes_since_baseline']==[]
print('R31_SOURCE_NATIVE_CANONICAL_PASS:52unique native/4privateprofiles/orderedrealGUI/8normalhashes/earnedflags/teardown;56existingpartial/12families;2878bounded/3285retained;0acceptedremoved/globalunknown. Primaryfontmeasurements not fallback acceptance.')

C=rd(P/"CAPTURE_CONTRACT.json");assert C["status"]=="PASS_DIAGNOSTIC_ONLY" and C["fixture_hash"]==sha((P/"capture_startup_ui.gd").read_bytes()) and C["native_manifests"]==4 and C["native_files"]==52 and C["QA11"] is None and C["owner"] is None
