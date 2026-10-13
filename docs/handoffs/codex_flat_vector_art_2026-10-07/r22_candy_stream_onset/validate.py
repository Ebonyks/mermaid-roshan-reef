"""Validate exact source/native/frozen unit claims;no acceptance inference."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r21_candy_stream_material';BASE='fa6402f4b1dd382c0d32c740eb034d67a6ac72f8'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
sources=read(P/'SOURCES.json')['sources'];assert len(sources)==50
for x in sources:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
 cur=(R/x['path']).read_bytes();assert cur==b or (x['path'].endswith(('.gd','.json','.godot','.tscn')) and cur.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')),x['path']
ctx=read(P/'CONTEXT_PREREQUISITE.json');assert ctx['status']=='PASS' and len(ctx['files'])==10
for row in ctx['files']:assert row['revision']==BASE and sha(subprocess.check_output(['git','show',BASE+':'+row['path']],cwd=R,stderr=subprocess.PIPE))==row['sha256']
floor=read(P/'EMPTY_FLOOR_COLUMNS.json');im=Image.open(R/floor['source_path']).convert('RGB');assert list(im.size)==floor['dimensions'] and sha((R/floor['source_path']).read_bytes())==floor['source_sha256']
assert floor['columns'][580]=={'top':204,'boundary':537,'floor':533}
for x,c in enumerate(floor['columns']):
 ys=[y for y in range(im.height) if min(im.getpixel((x,y)))>=128]
 assert c==({'top':min(ys),'boundary':max(ys),'floor':max(ys)-4} if len(ys)>8 else None)
assert (P/'FILL_CONTACT_ROWS.json').read_bytes()==(O/'FILL_CONTACT_ROWS.json').read_bytes()
idx=read(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==78 and idx['unique_sha256_count']==72 and idx['directly_viewed_count']==18 and len(set(idx['directly_viewed_native_files']))==18
for row in idx['files']:
 f=P/row['path'];b=f.read_bytes();assert sha(b)==row['sha256'] and len(b)==row['bytes'] and list(Image.open(f).size)==row['dimensions']
assert len({x['sha256'] for x in idx['files']})==72
manifests=list(P.rglob('capture_manifest.json'));assert len(manifests)==6
for f in manifests:
 d=read(f);assert d['errors']==[] and d['source_revision']==BASE and len(d['states'])==13
 e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert d['renderer']=='mobile' and d['quality']=='speedy' and d['normal_save_before']==d['normal_save_after'] and len(d['normal_save_before'])==8
 states={x['id']:x for x in d['states']};initial='native_attempt01' in f.parts;prototype=P/('candidate_attempt01.gd' if initial else 'candidate_stream_surface.gd')
 for s in d['states']:
  assert s['phase_index']==0 and s['mode']=='pourt' and s['visual_context']=='pour_candymaker'
  b=(f.parent/s['image']['file']).read_bytes();assert len(b)==s['image']['bytes'] and sha(b)==s['image']['sha256']
  c=s['stream_contract'];assert c['prototype_sha256']==sha(prototype.read_bytes()) and c['lookup_sha256']==sha((P/'FILL_CONTACT_ROWS.json').read_bytes())
  assert c['candidate_sha256']==sha((R/'assets_src/flat_vector_candy_stream_20261013/stream_1024.png').read_bytes())
  assert s['presentation']['fade_alpha']<=0.02 and not s['presentation']['medal_present']
  if not initial and c['stream_active']:
   assert c['valid'] and c['contact_kind'] in ['empty_cavity_floor_mask','revealed_pool_same_column']
   pixel=c['floor_source_pixel'] if c['contact_kind']=='empty_cavity_floor_mask' else c['source_pixel'];assert pixel[0]==580
   if c['contact_kind']=='empty_cavity_floor_mask':assert pixel==[580,533] and c['floor_source_boundary_y']==537
   else:assert c['source_alpha']>=0.5
   assert c['floor_lookup_sha256']==sha((P/'EMPTY_FLOOR_COLUMNS.json').read_bytes())
 for key in ['ready','passive_03s','wrong_pressed','wrong_released']:assert states[key]['pour_level']==0.0
 for key in ['held_08s','held_14s','held_22s','dragged_12px']:assert 0<states[key]['pour_level']<1 and states[key]['held'] and states[key]['pour_hold']
 for key in ['released','released_passive_03s']:assert 0<states[key]['pour_level']<1 and not states[key]['held'] and not states[key]['pour_hold'] and not states[key]['stream_contract']['stream_active']
 if not initial:
  assert states['held_02s']['stream_contract']['contact_kind']=='empty_cavity_floor_mask'
  assert states['held_03s']['stream_contract']['contact_kind']=='empty_cavity_floor_mask'
for f in ['LAUNCH.json','LAUNCH_ATTEMPT01.json']:assert read(P/f)['returncode']==0
for f in ['SCRIPT_GATES.json','SCRIPT_GATES_ATTEMPT01.json']:assert all(x['exit_code']==0 for x in read(P/f))
for f in ['native_capture.log','native_attempt01.log']:assert b'ERROR:' not in (P/f).read_bytes() and b'SCRIPT ERROR' not in (P/f).read_bytes()
review=read(P/'REVIEW.json');assert len(review['ten_axes'])==10 and review['direct_native_views']==idx['directly_viewed_native_files'] and review['calls']==0 and review['acceptance']['owner'] is None
for f in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=read(P/f);old=read(O/f);assert d['revision']=='FV-AUDIT-20261013-R22'
 for key in ['pieces','supplemental_piece_records','entries','status_lanes','named_status_counts','candy_stream_material','candy_stream_contact','candy_pointer_reuse']:
  if key in old:assert d[key]==old[key],key
 assert d['candy_stream_onset']['new_generated_drawings']==d['candy_stream_onset']['new_generation_calls']==d['candy_stream_onset']['new_design_ids']==0
T=read(P/'tally.json');assert T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None
assert T['integrated']==T['runtime_verified']==T['accepted_removed']==0 and T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30
C=T['current_context'];assert C['exact_capture_count']==2456 and C['retained_native_capture_count']==C['retained_native_captures']==2570 and C['excluded_diagnostic_native_count']==114
assert C['partial_overlapping_entries']==77 and C['complete_entries']==0 and C['entries_without_current_slice']==99
assert T['historical_totals'][:-1]==read(O/'tally.json')['historical_totals'] and T['historical_totals'][-1]['immutable_receipt_revision']==BASE
assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R22_SOURCE_NATIVE_CANONICAL_PASS:50source bindings;78native/72unique/18directviews;RGBfloor/samecolumn contact;no new art/calls/status/acceptance;unknown totals preserved.')
