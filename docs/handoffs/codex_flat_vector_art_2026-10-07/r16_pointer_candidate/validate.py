"""R16 whole-unit/provenance/capture/unchanged-source and conservative-count checks."""
from pathlib import Path
import json,hashlib,subprocess,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];V=P.parent/'r15_geode_cue_reuse';OLD='1910dc272025ca53b049f559245eb0c4ee8675fb'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def old(n):return json.loads(subprocess.check_output(['git','show',OLD+':'+(V/n).relative_to(R).as_posix()],cwd=R,stderr=subprocess.PIPE))
assert subprocess.check_output(['git','diff',OLD,'--name-only','--','scripts','assets','scenes','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE)==b''
for x in get('SOURCES.json')['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
A=R/'assets_src/flat_vector_pointer_20261013';native=Image.open(A/'native.png').convert('RGBA');rt=Image.open(A/'native_roundtrip.png').convert('RGBA');clean=Image.open(A/'clean_native.png').convert('RGBA');assert native.tobytes()==rt.tobytes();assert all(c==o or c==(0,0,0,0) for o,c in zip(native.getdata(),clean.getdata()))
D=get('DERIVATIVES.json');assert D['master_proof']['layers']==1 and D['master_proof']['frames']==1 and D['master_proof']['matte_cleanup']['removed_nonzero_alpha_pixels']==3064
for x in D['files']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
assert Image.open(A/'pointer_1024.png').size==(1024,1024)
assert get('REUSE_JOB.json')['calls_used']==1 and get('REUSE_JOB.json')['attempt_cap']==1
candidate=(P/'candidate_pointer_surface.gd').read_text();prior=(V/'candidate_cue_surface.gd').read_text();assert prior[prior.index('func _draw_geode()'):] in candidate
body=candidate[candidate.index('func _draw_demo_finger()'):];assert 'draw_circle' not in body and 'draw_arc' not in body and 'HAND_SIDE := 74.0' in candidate and 'HAND_TIP_UV := Vector2(0.44580078125, 0.90625)' in candidate
idx=get('CAPTURE_INDEX.json');assert len(idx['captures'])==94 and idx['new_excluded']==0 and idx['unique_png_hashes']==84
for x in idx['captures']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'];assert list(Image.open(P/x['path']).size)==x['dimensions']
for folder in ['native','restored_native']:
 for f in (P/folder).rglob('capture_manifest.json'):
  d=json.loads(f.read_text());assert d['errors']==[] and d['normal_save_before']==d['normal_save_after'];assert (d['engine']['major'],d['engine']['minor'],d['engine']['patch'],d['engine']['status'],d['engine']['build'])==(4,7,2,'stable','official') and d['renderer']=='mobile' and d['quality']=='speedy'
  for x in d['states']:
   h=x['hand_contract'];assert h['rect'][2:]==[74,74];delta=[h['visible_fingertip'][i]-h['at'][i] for i in [0,1]];assert abs(delta[0])<0.001 and abs(delta[1]-(0 if h['pressing'] else -8))<0.001
   if folder=='restored_native':assert x['pull']==60 and sum(x['seams'])==5
for x,y in zip(get('per_piece.json')['pieces'],old('per_piece.json')['pieces']):assert {k:v for k,v in x.items() if k!='pointer_candidate'}==y
assert get('per_piece.json')['supplemental_piece_records']==old('per_piece.json')['supplemental_piece_records']
for x,y in zip(get('scene_coverage.json')['entries'],old('scene_coverage.json')['entries']):assert {k:v for k,v in x.items() if k!='pointer_candidate'}==y
assert get('scene_coverage.json')['partial_entries']==77 and get('scene_coverage.json')['complete_entries']==0
now=get('tally.json');prior=old('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','known_named_design_records_including_supplemental','known_family_count_including_supplemental','replaced','integrated','runtime_verified','accepted_removed','regression_count','remaining_source_scopes_to_disposition','current_partial_context_union']:assert now[k]==prior[k],k
assert now['historical_totals'][:-1]==prior['historical_totals'];cc=now['current_context'];assert (cc['exact_capture_count'],cc['retained_native_capture_count'],cc['retained_native_captures'],cc['excluded_diagnostic_native_count'])==(2138,2252,2252,114)
assert now['current_context_sample_lanes']['samples_awaiting_review']==1 and now['current_context_sample_lanes']['approved']==0
review=get('REVIEW.json');assert review['actually_viewed_native']==9 and len(review['all_ten_comparison_axes'])==10 and review['accepted_removed']==0
full=get('FULL_VALIDATION.json');assert full['status']=='PASS_ALL_82_TRUSTED_NATIVE' and full['trusted_passed']==82 and full['normal_save_hashes_unchanged'];names=re.search(r'for p in (probe_reef_districts .*?); do',(R/'scripts/ci.sh').read_text()).group(1).split();assert [x['probe'] for x in full['rows']]==names
for x in full['rows']:
 b=(P/x['evidence']).read_bytes();assert len(b)==x['raw_output_bytes'] and hashlib.sha256(b).hexdigest()==x['raw_output_sha256'];assert not re.search(full['failure_regex'],b.decode('utf-8','replace')) and not re.search(full['resource_error_regex'],b.decode('utf-8','replace'))
print('R16_VALIDATION_OK;one whole-hand sample/94 native files/all82 trusted probes; stable IDs/unknown totals and all art acceptance limits preserved')
