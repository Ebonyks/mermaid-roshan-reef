"""Verify immutable/source/native/canonical claims; never grant art acceptance."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];OLD=P.parent/'r20_candy_stream_contact';BASE='29e90b7acbde7b2c0960979535960af8f0bd3df3';A=R/'assets_src/flat_vector_candy_stream_20261013'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
source=read(P/'SOURCES.json');assert len(source['sources'])==45
for x in source['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
 cur=(R/x['path']).read_bytes();assert cur==b or (x['path'].endswith(('.gd','.json','.godot','.tscn')) and cur.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')),x['path']
assert (P/'FILL_CONTACT_ROWS.json').read_bytes()==(OLD/'FILL_CONTACT_ROWS.json').read_bytes()
meta=read(A/'GENERATION.json');assert meta['call_count']==meta['cap']==1 and meta['tool']=='built-in image_gen';assert meta['model'] is None and meta['seed'] is None and meta['request_id'] is None and meta['billing'] is None
assert meta['local_quality']=='FAILED_LOCAL_VISUAL_QC' and meta['generated_native']['sha256']==sha((A/'stream_native.png').read_bytes())
proof=read(A/'MASTER_PROOF.json');assert proof['frames']==proof['layers']==1 and proof['normalized_size']==[683,1024] and proof['native_size']==[1024,1536]
assert not any(proof[x] for x in ['crop','recolor','repaint','part_separation','glow_removed']);assert proof['native_roundtrip_rgba_equal']
assert Image.open(A/'stream_native.png').convert('RGBA').tobytes()==Image.open(A/'native_roundtrip.png').convert('RGBA').tobytes()
assert Image.open(A/'stream_1024.png').size==(683,1024)
for x in read(P/'CANDIDATE_FILES.json')['files']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
idx=read(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==48 and idx['unique_sha256_count']==45 and idx['directly_viewed_count']==12
assert len(set(idx['directly_viewed_native_files']))==12
for x in idx['files']:
 f=P/x['path'];b=f.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and list(Image.open(f).size)==x['dimensions']
assert len({x['sha256'] for x in idx['files']})==45
manifests=list((P/'native').rglob('capture_manifest.json'));assert len(manifests)==4
for f in manifests:
 d=read(f);assert d['errors']==[] and d['source_revision']==BASE
 e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert d['renderer']=='mobile' and d['quality']=='speedy' and d['aspect'] in [[1280,720],[1600,720]]
 assert d['normal_save_before']==d['normal_save_after'] and len(d['normal_save_before'])==8
 states={x['id']:x for x in d['states']};assert len(states)==12
 for s in d['states']:
  assert s['phase_index']==0 and s['mode']=='pourt' and s['visual_context']=='pour_candymaker';assert s['presentation']['fade_alpha']<=0.02 and not s['presentation']['medal_present']
  image=s['image'];b=(f.parent/image['file']).read_bytes();assert sha(b)==image['sha256'] and len(b)==image['bytes']
  c=s['stream_contract'];assert c['lookup_sha256']==sha((P/'FILL_CONTACT_ROWS.json').read_bytes()) and c['prototype_sha256']==sha((P/'candidate_stream_surface.gd').read_bytes()) and c['candidate_sha256']==sha((A/'stream_1024.png').read_bytes())
 for key in ['ready','passive_03s','wrong_pressed','wrong_released']:assert states[key]['pour_level']==0.0
 for key in ['held_08s','held_14s','held_22s','dragged_12px']:
  s=states[key];assert 0<s['pour_level']<1 and s['pour_hold'] and s['held'] and s['stream_contract']['stream_active'] and s['stream_contract']['valid'] and s['stream_contract']['source_alpha']>=0.5
 assert states['held_02s']['stream_contract']['valid'] is False
 for key in ['released','released_passive_03s']:
  s=states[key];assert 0<s['pour_level']<1 and not s['pour_hold'] and not s['held'] and not s['stream_contract']['stream_active']
assert read(P/'LAUNCH.json')['returncode']==0 and read(P/'IMPORT.json')['returncode']==0
assert all(x['exit_code']==0 for x in read(P/'SCRIPT_GATES.json'))
for f in ['native_capture.log','import.log']:assert b'ERROR:' not in (P/f).read_bytes() and b'SCRIPT ERROR' not in (P/f).read_bytes()
review=read(P/'REVIEW.json');assert len(review['ten_axes'])==10 and len(review['direct_native_views'])==12 and len(review['direct_source_images_viewed'])==6
assert review['status'].startswith('FAILED_LOCAL_VISUAL_QC') and review['acceptance']['accepted_removed']==0 and review['acceptance']['owner'] is None
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=read(P/name);prior=read(OLD/name);assert d['revision']=='FV-AUDIT-20261013-R21' and d['candy_stream_material']['new_design_ids']==0 and d['candy_stream_material']['new_samples_awaiting_owner_review']==0
 for key in ['pieces','supplemental_piece_records','entries','named_status_counts','status_lanes']:
  if key in prior:assert d[key]==prior[key],key
 for key in ['candy_stream_contact','candy_pointer_reuse','pointer_candidate','nonruntime_functional_geometry_R20']:
  if key in prior:assert d[key]==prior[key],key
T=read(P/'tally.json');assert T['accepted_removed']==T['integrated']==T['runtime_verified']==0 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30
C=T['current_context'];assert C['exact_capture_count']==2378 and C['retained_native_capture_count']==C['retained_native_captures']==2492 and C['excluded_diagnostic_native_count']==114
assert C['partial_overlapping_entries']==77 and C['complete_entries']==0 and C['entries_without_current_slice']==99
assert T['current_context_sample_lanes']['samples_awaiting_review']==1 and T['new_nonruntime_R21_artifact_count']['failed_local_qc']==1
assert T['historical_totals'][:-1]==read(OLD/'tally.json')['historical_totals'] and T['historical_totals'][-1]['immutable_receipt_revision']==BASE
U=read(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert U['current_existing_named_records_with_partial_context']==48 and U['current_existing_families_with_partial_context']==9 and U['records']==read(OLD/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records']
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R21_SOURCE_NATIVE_CANONICAL_PASS:45 source inputs,48native/45unique,12direct views;one localQCfailed whole draft,0newapprovalqueue/0removal;unknown totals preserved;production unchanged.')
