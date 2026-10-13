"""Verify R15 native/source parity,stable units and conservative evidence lanes."""
from pathlib import Path
import json,hashlib,subprocess,math
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];V=P.parent/'r14_geode_lifecycle';OLD='42ef9083c07d15e0436ad981d23a35c6309871c8'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def old(n):return json.loads(subprocess.check_output(['git','show',OLD+':'+(V/n).relative_to(R).as_posix()],cwd=R,stderr=subprocess.PIPE))
assert subprocess.check_output(['git','diff',OLD,'--name-only','--','scripts','assets','scenes','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE)==b''
for x in get('SOURCES.json')['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
 work=(R/x['path']).read_bytes()
 if x['path']=='ASSET_LICENSES.md':
  before=b.replace(b'\r\n',b'\n');after=work.replace(b'\r\n',b'\n');assert after.startswith(before);addition=after[len(before):].decode();assert addition.strip().startswith('| docs/handoffs/codex_flat_vector_art_2026-10-07/r15_geode_cue_reuse/native/') and len(addition.strip().splitlines())==1
 elif Path(x['path']).suffix=='.png':assert b==work,x['path']
 else:assert b.replace(b'\r\n',b'\n')==work.replace(b'\r\n',b'\n'),x['path']

source=(R/'scripts/opera_geology_surface.gd').read_text();f=source[source.index('func _draw_geode()'):source.index('func _draw_work_surface()')];prefix=f[:f.index('\tfor index in range(GEODE_SEAM_SPOTS.size()):')];candidate=(P/'candidate_cue_surface.gd').read_text();assert prefix in candidate
assert 'draw_circle' not in candidate and 'draw_arc' not in candidate
assert math.hypot(32,32)<56 and 'Vector2(64, 64)' in candidate and '0.32 if geode_seams[index]' in candidate
idx=get('CAPTURE_INDEX.json');assert len(idx['captures'])==44 and idx['new_excluded']==0 and idx['unique_png_hashes']==32
for x in idx['captures']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'];assert list(Image.open(P/x['path']).size)==x['dimensions']
for f in (P/'native').rglob('capture_manifest.json'):
 d=json.loads(f.read_text());assert d['errors']==[] and d['normal_save_before']==d['normal_save_after'];assert (d['engine']['major'],d['engine']['minor'],d['engine']['patch'],d['engine']['status'],d['engine']['build'])==(4,7,2,'stable','official') and d['renderer']=='mobile' and d['quality']=='speedy';s={x['id']:x for x in d['states']}
 for k in ['geode_closed_ready','geode_closed_passive_1s','geode_wrong_tap','geode_early_pull_released']:assert s[k]['pull']==0 and sum(s[k]['seams'])==0
 for i in range(5):assert sum(s['geode_seam%02d_pressed'%i]['seams'])==i and sum(s['geode_seam%02d_released'%i]['seams'])==i+1
 assert sum(s['geode_seam_repeat']['seams'])==5 and s['geode_partial_open_released']['pull']==60 and not s['geode_cancel_focus_notification']['held']
for x,y in zip(get('per_piece.json')['pieces'],old('per_piece.json')['pieces']):assert {k:v for k,v in x.items() if k!='geode_cue_reuse'}==y
assert get('per_piece.json')['supplemental_piece_records']==old('per_piece.json')['supplemental_piece_records']
for x,y in zip(get('scene_coverage.json')['entries'],old('scene_coverage.json')['entries']):assert {k:v for k,v in x.items() if k!='geode_cue_reuse'}==y
assert sum('geode_cue_reuse' in x for x in get('scene_coverage.json')['entries'])==1
assert get('scene_coverage.json')['partial_entries']==77 and get('scene_coverage.json')['complete_entries']==0
now=get('tally.json');prior=old('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','known_named_design_records_including_supplemental','known_family_count_including_supplemental','replaced','integrated','runtime_verified','accepted_removed','regression_count','remaining_source_scopes_to_disposition']:assert now[k]==prior[k],k
assert now['historical_totals'][:-1]==prior['historical_totals']
cc=now['current_context'];assert (cc['exact_capture_count'],cc['retained_native_capture_count'],cc['retained_native_captures'],cc['excluded_diagnostic_native_count'])==(2044,2158,2158,114)
review=get('REVIEW.json');assert review['actually_viewed_native']==5 and len(review['all_ten_comparison_axes'])==10 and review['accepted_removed']==0
assert get('SEARCH_SCOPE.json')['all_reuse_exhausted'] is False
union=get('CURRENT_PARTIAL_CONTEXT_UNION.json');assert union['current_existing_named_records_with_partial_context']==47 and union['new_R15_partial_existing_ids']==['FV-1DC9F18904A8'];assert now['current_partial_context_union']==union
print('R15_VALIDATION_OK;44 diagnostic files/32 hashes,unchanged production/input and stable unknown totals; art/QA11/device/child/owner acceptance open')
