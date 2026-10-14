from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r38_glyph_reconciliation';BASE='9d19fdc1f0ebdcac8c11d75adc56926bc43d136f'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
c=rd(P/'CAPTURE_INDEX.json');s=c['summary'];assert s['retained_native']==420 and s['successful_native']==338 and s['failed_native']==82 and s['bounded_art_context_credits']==300 and s['excluded_native']==120
assert s['current_bounded']==3497 and s['current_retained']==4425 and s['current_excluded']==928 and s['current_bounded']+s['current_excluded']==s['current_retained']
assert len(c['captures'])==420 and len({x['path'] for x in c['captures']})==420 and len(c['cases'])==10
success=[x for x in c['cases'] if x['native_exit_code']==0];assert len(success)==8 and {(x['aspect'][0],x['profile']) for x in success}=={(w,k) for w in [1280,1600] for k in ['fresh_locked','saved_fish','saved_cat','saved_bird']}
assert sum(x['art_context_credit'] for x in c['captures'])==300
for x in c['files']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
for case in c['cases']:
 f=R/case['manifest'];d=rd(f);assert sha(f.read_bytes())==case['manifest_sha256'] and d['normal_save_before']==d['normal_save_after'] and d['source_revision']==BASE and d['renderer']=='mobile' and d['quality']=='speedy'
 assert d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['engine']['status']=='stable' and d['engine']['build']=='official' and not d['actual_child_data']
 assert len(d['states'])==case['capture_count'] and d['errors']==case['errors']
 if case['native_exit_code']!=0:continue
 assert not d['errors'];states={x['id']:x for x in d['states']};seed=d['synthetic_seed'];first=d['states'][0]
 for key in ['custom_fish','custom_friends']:assert first[key][:len(seed.get(key,[]))]==seed.get(key,[])
 assert states['finish_release']['closing'] and states['duplicate_finish_guarded']['custom_fish']==states['finish_release']['custom_fish'] and states['duplicate_finish_guarded']['custom_friends']==states['finish_release']['custom_friends']
 expected=len(seed.get('custom_fish',[]))+(case['chosen_kind']=='fish');assert len(d['saved_fish'])==expected
 expected=len(seed.get('custom_friends',[]))+(case['chosen_kind']!='fish');assert len(d['saved_friends'])==expected
 if case['chosen_kind']!='fish':assert d['saved_unlocks'][case['chosen_kind']] and states['purchased_'+case['chosen_kind']+'_ready']['pearls']==23-({'cat':5,'bird':8}[case['chosen_kind']]) and states['unlocked_repeat_'+case['chosen_kind']]['pearls']==states['purchased_'+case['chosen_kind']+'_ready']['pearls']
 assert all(not x['profile_is_actual_child_data'] for x in d['states'])
sg=rd(P/'SIDECAR_GUARD.json');assert sg['before']==sg['after'] and len(sg['before'])==4039
src=rd(P/'SOURCE_AUDIT.json');assert len(src['source_texture_scopes'])==5 and len({x['id'] for x in src['source_texture_scopes']})==5
for x in src['source_texture_scopes']:
 assert x['id']=='FVT-'+sha((x['path']+'::'+x['function']).encode())[:12].upper();assert sha(git('show',BASE+':'+x['path']))==x['file_sha256']==sha((R/x['path']).read_bytes().replace(b'\r\n',b'\n'));assert sha(x['body_utf8'].encode())==x['function_sha256_lf']
for x in src['textures']:assert sha((R/x['path']).read_bytes())==x['sha256']
reuse=rd(P/'SOURCE_REUSE.json')
for x in reuse['inputs']:b=git('show',x['revision']+':'+x['path']);assert sha(b)==x['sha256'] and len(b)==x['bytes']
rev=rd(P/'COMPOSITOR_REVIEW.json');assert len(rev['ten_axes'])==10 and len(rev['direct_native_views'])==10 and len(rev['direct_source_view_paths'])==10 and not rev['full_context_review_complete'] and rev['approved']==rev['integrated']==rev['accepted_removed']==0
for name,array in [('per_piece.json','pieces'),('scene_coverage.json','entries'),('CONGRUENCY_BACKLOG.json','observations')]:assert rd(P/name)[array]==rd(O/name)[array] and rd(P/name)['revision']=='FV-AUDIT-20261014-R39'
x=rd(P/'per_piece.json');z=rd(O/'per_piece.json');assert x['supplemental_piece_records'][:1]==z['supplemental_piece_records'] and len(x['supplemental_piece_records'])==3;assert len(set(v['id'] for v in x['pieces']+x['supplemental_piece_records']))==227 and x['known_named_design_records_including_supplemental']==227 and x['known_family_count_including_supplemental']==30
T=rd(P/'tally.json');Z=rd(O/'tally.json');assert T['historical_totals'][:-1]==Z['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
for key in ['accepted_removed','integrated','runtime_verified','replaced']:assert T[key]==Z[key]==0
for key in ['all_game_individual_piece_total','current_distinct_screen_total','regression_count']:assert T[key] is None
assert T['remaining_source_scopes_to_disposition']==Z['remaining_source_scopes_to_disposition']==351 and T['current_partial_context_union']==Z['current_partial_context_union'] and T['supplemental_texture_compositor_scopes']==5
assert T['current_context']['exact_capture_count']==3497 and T['current_context']['retained_native_capture_count']==4425 and T['current_context']['excluded_diagnostic_native_count']==928 and T['current_partial_context_counts']['supplemental_craft_records']==3
C=rd(P/'scene_coverage.json');assert C['entries']==rd(O/'scene_coverage.json')['entries'] and C['effective_current_partial_entry_ids']==rd(O/'scene_coverage.json')['effective_current_partial_entry_ids'] and len(C['effective_current_partial_entry_ids'])==78
cur=rd(H/'CURRENT.json');assert cur['revision']==T['revision'] and cur['current_tally']==P.name+'/tally.json' and not cur['mission_complete']
assert not git('diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','addons','project.godot').strip()
for key in ['retained_full_validation','retained_ci']:
 x=rd(P/'MACHINE_BASELINE.json')[key];assert sha((R/x['path']).read_bytes())==x['sha256']
assert git('rev-parse','origin/dev').decode().strip()==rd(P/'SOURCE_PARITY.json')['reconciled_origin_dev']
assert not git('diff','--name-only',BASE,'--','tools/audit_game_2d.py','tools/game_2d_migration_manifest.json').strip()
print('R39_ALL_OK:420 retained/300 credits/120 excluded;8 exact native diagnostic cases;normal saves/protected sources/frozen arrays preserved;227role records/30families/5source units;0accepted/globalunknown/QA11/device/child/owner open.')
