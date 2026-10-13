"""Validate known-only R8 context/count deltas; never grants artwork acceptance."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];OLD=P.parent/'r7_craft_context'
def read(x):return json.loads(x.read_text(encoding='utf-8'))
def digest(b):return hashlib.sha256(b).hexdigest()
registry=read(P/'per_piece.json');prior=read(OLD/'per_piece.json')
assert len(registry['pieces'])==224 and len(registry['supplemental_piece_records'])==1
assert registry['known_named_design_records_including_supplemental']==225 and registry['known_family_count_including_supplemental']==30
for old,new in zip(prior['pieces'],registry['pieces']):
 filtered={k:v for k,v in new.items() if k!='geode_addendum'}
 assert filtered==old,old['id']
assert registry['supplemental_piece_records']==prior['supplemental_piece_records']
t=read(P/'tally.json');old=read(OLD/'tally.json')
for key in ['named_status_counts','known_named_design_records_including_supplemental','known_family_count_including_supplemental','remaining_source_scopes_to_disposition','all_game_individual_piece_total','regression_count','replaced','integrated','runtime_verified','accepted_removed']:
 assert t[key]==old[key],key
assert t['current_context']['exact_capture_count']==old['current_context']['exact_capture_count']+44==1708
assert t['current_context']['retained_native_captures']==1810
coverage=read(P/'scene_coverage.json');assert len(coverage['entries'])==176
assert coverage['partial_entries']==77 and coverage['complete_entries']==0 and coverage['entries_without_current_slice']==99
proof=read(P/'SOURCE_PARITY.json');assert len(proof['captures'])==44 and not proof['raw_byte_changes'] and proof['normal_save_hashes_unchanged_both_aspects']
for cap in proof['captures']:
 file=P/cap['path'];raw=file.read_bytes();assert len(raw)==cap['bytes'] and digest(raw)==cap['sha256'];assert list(Image.open(file).size)==cap['dimensions']
for aspect in ['1280x720','1600x720']:
 data=read(P/'native'/aspect/'capture_manifest.json');assert len(data['states'])==22 and not data['errors']
 assert data['renderer']=='mobile' and data['quality']=='speedy' and data['normal_save_before']==data['normal_save_after']
 assert [x['seams'].count(True) for x in data['states'][6:16]]==[0,1,1,2,2,3,3,4,4,5]
 assert all(x['pull']==60.0 for x in data['states'][-4:])
for source in read(P/'SOURCES.json')['sources']:
 raw=subprocess.check_output(['git','show',source['immutable_revision']+':'+source['path']],cwd=R,stderr=subprocess.PIPE)
 assert len(raw)==source['bytes'] and digest(raw)==source['sha256'],source['path']
assert not subprocess.check_output(['git','diff','--name-only',read(P/'PREFLIGHT.json')['baseline'],'--','scripts','scenes','assets','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE).strip()
review=read(P/'REVIEW.json');assert review['actually_viewed_unique_native']==5 and len(review['all_ten_comparison_axes'])==10
assert review['new_generation_calls']==0 and not review['runtime_changes'] and review['accepted_removed']==0 and not review['full_context_review_complete']
assert all(x is None for x in review['acceptance_lanes'].values())
print('R8_CONTEXT|ALL OK|44 captures/5 inspected;225 known/30 families;unknown denominators;zero acceptance;runtime unchanged')
