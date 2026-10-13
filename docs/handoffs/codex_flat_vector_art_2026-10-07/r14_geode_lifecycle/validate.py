"""R14 source, native lifecycle, count/history and acceptance-lane consistency checks."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];OLD='8a0db03f72735b67ebb581927051c92ca62eaef9';PREV=P.parent/'r13_geode_source_closure'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def old(n):return json.loads(subprocess.check_output(['git','show',OLD+':'+(PREV/n).relative_to(R).as_posix()],cwd=R,stderr=subprocess.PIPE))
pieces=get('per_piece.json');baseline=old('per_piece.json');assert len(pieces['pieces'])==224
for x,y in zip(pieces['pieces'],baseline['pieces']):
 clean={k:v for k,v in x.items() if k!='geode_lifecycle'};assert clean==y,x['id']
assert pieces['supplemental_piece_records']==baseline['supplemental_piece_records']
c=get('scene_coverage.json');assert len(c['entries'])==176 and (c['partial_entries'],c['complete_entries'],c['entries_without_current_slice'])==(77,0,99)
for x,y in zip(c['entries'],old('scene_coverage.json')['entries']):assert {k:v for k,v in x.items() if k!='geode_lifecycle'}==y
idx=get('CAPTURE_INDEX.json');assert len(idx['captures'])==112 and idx['new_bounded_diagnostics']==100 and sum(x['bounded_diagnostic'] for x in idx['captures'])==100
for x in idx['captures']:
 f=P/x['path'];b=f.read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'];im=Image.open(f);assert list(im.size)==x['dimensions']
for f in sorted((P/'native').rglob('capture_manifest.json')):
 d=json.loads(f.read_text());assert not d['errors'] and d['normal_save_before']==d['normal_save_after'];assert (d['engine']['major'],d['engine']['minor'],d['engine']['patch'],d['engine']['status'],d['engine']['build'])==(4,7,2,'stable','official');assert d['renderer']=='mobile' and d['quality']=='speedy'
 assert d['working_repair_runtime_sha256']['geology']==hashlib.sha256((R/'scripts/opera_geology_surface.gd').read_bytes()).hexdigest()
 states={x['id']:x for x in d['states']}
 if d['part']=='resume':
  assert states['geode_disk_resume060_task']['pull']==60 and sum(states['geode_disk_resume060_task']['seams'])==5
  assert abs(states['geode_119_reentry_task']['pull']-119)<0.001
  complete=states['geode_completed120_held'];assert complete['pull']==120 and complete['completion_accepted'] and complete['phase_advance_pending']
  earned=states['geode_completion_reward_return'];assert earned['save_facts']['opera_stars']==1<<16 and earned['save_facts']['pearls']==3 and earned['save_facts']['checkpoint']=={} and not earned['world_live']
  replay=states['geode_post_reward_reentry_river'];assert replay['phase_index']==0 and replay['mode']=='geology_river'
  assert d['final_facts']['sentinel_preserved']
t=get('tally.json');prior=old('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','known_named_design_records_including_supplemental','known_family_count_including_supplemental','replaced','integrated','runtime_verified','accepted_removed','regression_count','remaining_source_scopes_to_disposition']:assert t[k]==prior[k],k
assert t['historical_totals'][:-1]==prior['historical_totals'];assert t['current_context']['exact_capture_count']==2000
assert t['current_context']['retained_native_captures']==2114 and t['current_context']['excluded_diagnostic_native_count']==114
assert t['current_context']['retained_native_capture_count']==2114 and t['all_game_individual_piece_total'] is None and t['accepted_removed']==0
assert get('REVIEW.json')['actually_viewed_native']==8 and len(get('REVIEW.json')['all_ten_comparison_axes'])==10
assert set(x['after']['path'] for x in get('SOURCE_PARITY.json')['exact_changes'])=={'scripts/opera_geology_surface.gd','scripts/probe_opera_2d.gd'}
for x in get('SOURCES.json')['sources']:
 b=(R/x['path']).read_bytes() if x['immutable_revision'] is None else subprocess.check_output(['git','show',x['immutable_revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
print('R14_VALIDATION_OK; terminal lifecycle/source proof and count/history preserved; all art/QA11/device/child/owner acceptance open')
