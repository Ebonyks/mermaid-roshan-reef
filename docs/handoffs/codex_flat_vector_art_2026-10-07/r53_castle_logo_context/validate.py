from pathlib import Path
import json,hashlib,subprocess,ast,collections
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r52_farmer_panorama_reuse';B='0e3415ae41aae2ae53dd881ef78042066269e70f';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def main():
 idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['captures'])==280 and idx['lanes']=={'EXCLUDED_FIXTURE_COMPARISON_FAILURE':140,'CURRENT_SOURCE_CONTROL':140}
 for x in idx['captures']:
  f=P/x['path'];assert sha(f.read_bytes())==x['sha256'] and list(Image.open(f).size)==x['dimensions']
 for c in idx['cases']:
  n=P/'native'/c['case'];d=rd(n/'capture_manifest.json');q=rd(n/'RESULT.json');expected=[] if c['current'] else ['unknownsavefieldpreserved'];assert d['errors']==expected and q['exit_code']==(0 if c['current'] else 1) and not q['timed_out'] and not q['script_or_shader_errors'];assert d['source_revision']==D and d['renderer']=='mobile' and d['time_scale']==1 and d['boot_count']==2
  e=d['engine'];assert(e['major'],e['minor'],e['patch'],e['status'],e['build'])==(4,7,2,'stable','official') and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
  assert len(d['states'])==70 and len(d['checks'])==68 and sum(x['pass'] for x in d['checks'])==(68 if c['current'] else 67)
  for name,key in [('capture_manifest.json','report_sha256'),('fixture_source.gd','fixture_sha256')]:assert sha((n/name).read_bytes())==c[key]
  assert q['sidecars_exact'] and q['sidecar_before_count']==q['sidecar_after_count']==4041 and not q['source_byte_changes'] and q['normal_before']==q['normal_after'] and q['fixture_unchanged'] and sha((n/'engine.log').read_bytes())==q['log_sha256']
  states={x['id']:x['snapshot'] for x in d['states']};choices={x['id'] for x in d['states'] if x['id'].startswith('choice_')};assert len(choices)==48
  for id in choices:
   _,color,symbol=id.split('_');s=states[id];assert s['color']==s['preview']['color']==color and s['symbol']==s['preview']['symbol']==symbol and s['game']=='level2' and s['navigation_top']=='castle_logo_studio' and s['preview']['is_source_logo_preview']
  for id,room in [('craft_committed_display','craft_room'),('playroom_committed_display','playroom')]:
   s=states[id];display=s['display'];assert s['color']==s['disk']['color']=='purple' and s['symbol']==s['disk']['symbol']=='dog' and display['room']==room and display['mouse_filter']==2 and len(display['banners'])==2
   assert all(b['color']=='purple' and b['symbol']=='dog' and b['mouse_filter']==2 for b in display['banners'])
   assert display['badge']['exists']==(room=='craft_room')
  assert not states['library_unregistered_absence']['display']['exists']
  for id in ['craft_committed_display','draft_after_background','background_cancel_restored','fresh_main_loaded_display']:
   s=states[id];assert s['disk']['unknown']=={'keep':[3,7],'token':'R53_PRIVATE_ONLY'} and s['disk']['color']=='purple' and s['disk']['symbol']=='dog'
  assert states['draft_after_background']['color']=='gold' and states['draft_after_background']['symbol']=='star' and not states['draft_after_background']['save_pending'] and not states['draft_after_background']['save_dirty']
  assert states['fresh_main_logo_reopened']['preview']['color']=='purple' and states['fresh_main_logo_reopened']['preview']['symbol']=='dog'
 for x in rd(P/'SOURCE_REFERENCES.json')['files']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256'] and x['http_status']==200
 rev=rd(P/'REVIEW.json');assert len(rev['actually_viewed_native_frames'])==12 and len(rev['actually_viewed_new_source_images'])==3 and len(rev['comparison_axes'])==10 and not rev['full_context_review_complete'] and rev['accepted_removed']==0
 for x in rev['actually_viewed_native_frames']:assert x in idx['captures'] and x['lane']=='CURRENT_SOURCE_CONTROL'
 for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
  d=rd(P/name);old=rd(O/name);assert d['castle_logo_context']['runtime_source_revision']==D
  if name=='per_piece.json':assert d['pieces']==old['pieces'] and d['supplemental_piece_records']==old['supplemental_piece_records'] and len(d['pieces'])+len(d['supplemental_piece_records'])==240
  if name=='scene_coverage.json':assert d['entries']==old['entries'] and set(d['effective_current_partial_entry_ids'])==set(old['effective_current_partial_entry_ids'])|{'game.logo_studio'} and (d['effective_partial_entries'],d['effective_entries_without_current_slice'],d['complete_entries'])==(84,92,0)
  if name=='tally.json':
   assert d['historical_totals'][:-1]==old['historical_totals'] and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B and d['current_context_sample_lanes']==old['current_context_sample_lanes'];assert(d['current_context']['exact_capture_count'],d['current_context']['retained_native_capture_count'],d['current_context']['excluded_diagnostic_native_count'])==(4313,6211,1898);assert d['current_partial_context_counts']['existing_named_records']==74;assert d['accepted_removed']==d['integrated']==d['runtime_verified']==0 and d['all_game_individual_piece_total'] is None and d['regression_count'] is None
 union=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert len(union['records'])==len({x['id'] for x in union['records']})==74 and len({x['family'] for x in union['records']})==15
 for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
 assert not git('diff','--name-only',B,'--','scripts','scenes','assets','assets_src','shaders','addons','project.godot').strip();assert rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json'
 for f in P.rglob('*'):
  if f.is_file():
   assert f.stat().st_size<4194304,(str(f),f.stat().st_size)
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8-sig'))
 assert not rd(P/'WORK_IN_PROGRESS.json')['mission_complete'];print('R53_INTEGRITY_PASS 280native=140current+140excluded; 136currentchecks/48choices peraspect; 74exactrefs/12native3sourceviews; frozen/runtime unchanged;0accepted/globalunknown',flush=True)
if __name__=='__main__':main()
