"""Check R4 diagnostic capture/scope evidence. Never grant DL-QA-11/owner acceptance."""
from pathlib import Path
import argparse,copy,json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];REV='e97a6db8ce823a6730b08318d463469d16d9a472'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
EXPECTED=read(P/'EXPECTED_MATRIX.json');SIZES={'1280x720':(1280,720),'1600x720':(1600,720)}
def node(a,name):return next((n for n in a['visible_canvas'] if n['path'].split('/')[-1]==name),{})
def matrix_errors(m,case,aspect):
 e=[]
 if m['result']!='PASS' or m['failures'] or not all(x['pass'] for x in m['checks']):e.append('native checks fail')
 if m['source_revision']!=REV or m['renderer']!='mobile' or m['quality']!='speedy' or m['display_server']=='headless':e.append('wrong native/source/profile')
 if [m['engine'].get(k) for k in ['major','minor','patch','status','build']]!=[4,7,2,'stable','official']:e.append('wrong exact engine')
 if m['aspect']!=list(SIZES[aspect]) or m['run_case']!=case:e.append('wrong aspect/case')
 if m['expected_ids']!=EXPECTED[case] or [x['id'] for x in m['states']]!=EXPECTED[case]:e.append('matrix incomplete')
 ss=m['save_isolation']
 if not ss['unchanged'] or ss['before']!=ss['after'] or len(ss['before'])!=8:e.append('normal save changed/unbound')
 if not m['source_unchanged'] or m['source_signature']['missing'] or len(m['source_signature']['files'])!=6427:e.append('source closure changed/incomplete')
 for row in m['states']:
  a=row['actual'];sid=row['id'];im=row['image']
  if row['status']!='PASS' or a['save_path']!=ss['fresh_fixture_save'] or a['tree_paused']!=row['expected_pause'] or a['tree_paused']!=(sid=='pause_castle'):e.append('state/pause/save mismatch')
  if a['story_clip_present'] or a['fade_alpha']>0.001 or any(n['class']=='VideoStreamPlayer' for n in a['visible_canvas']):e.append('obscured by movie/fade')
  if (im['width'],im['height'])!=SIZES[aspect]:e.append('encoded dimensions mismatch')
  if case in ['fresh','saved']:
   if not a['start_menu_active'] or not a['intro_active']:e.append('menu absent')
   if sid.endswith('options_on') and (not a['options_visible'] or not a['music_on'] or not a['mic_on']):e.append('options-on absent')
   if sid.endswith('options_off') and (not a['options_visible'] or a['music_on'] or a['mic_on']):e.append('options-off absent')
   if sid=='fresh_default' and (a['has_saved_game'] or not node(a,'StartMenuContinueButton').get('disabled')):e.append('fresh disabled state absent')
   if sid=='saved_default' and (not a['has_saved_game'] or node(a,'StartMenuContinueButton').get('disabled')):e.append('saved state absent')
   if sid=='saved_hover' and node(a,'StartMenuOptionsTab').get('draw_mode')!=2:e.append('hover not reached')
   if sid=='saved_pressed' and node(a,'StartMenuOptionsTab').get('draw_mode') not in [1,4]:e.append('pressed not reached')
   if sid.startswith('confirm') and not a['confirm_visible']:e.append('confirmation absent')
   if sid=='confirm_disarmed' and not node(a,'StartMenuConfirmNewGameButton').get('disabled'):e.append('disarmed absent')
   if sid=='confirm_armed' and node(a,'StartMenuConfirmNewGameButton').get('disabled'):e.append('armed absent')
   if sid=='confirm_holding' and (not a['hold_active'] or not 0<a['hold_fill_width']<240):e.append('partial hold absent')
   if sid=='confirm_cancelled' and (a['hold_active'] or a['hold_fill_width']!=0):e.append('hold not cancelled')
   if sid=='saved_kept' and (a['confirm_visible'] or a['options_visible']):e.append('keep-game return absent')
  else:
   if a['start_menu_active'] or a['intro_active']:e.append('overlay obscured by menu')
   key='pause_visible' if sid=='pause_castle' else ('craft_visible' if sid.startswith('craft_') else ('wardrobe_visible' if sid.startswith('wardrobe_') else ('stickers_visible' if sid.startswith('stickers_') else 'collection_visible')))
   if not a.get(key):e.append('expected overlay absent')
   if sid=='craft_rainbow' and not a['craft_body_rainbow']:e.append('rainbow state absent')
   if sid=='craft_cat' and a['craft_kind']!='cat':e.append('kitty selection absent')
   if sid=='craft_bird_detail' and (a['craft_kind']!='bird' or a['craft_part']!='third'):e.append('bird detail absent')
   if sid in ['wardrobe_unlocked','wardrobe_fairy_selected'] and not a['fairy_unlocked']:e.append('unlock absent')
   if sid=='wardrobe_fairy_selected' and not a['skin_id'].startswith('fairy'):e.append('fairy selection absent')
   if sid=='stickers_empty' and a['stickers']:e.append('empty stickers absent')
   if sid=='stickers_earned' and len(a['stickers'])<18:e.append('earned stickers incomplete')
   if sid.startswith('critter_'):
    if a['critter_category']!=sid.split('_')[1] or len(a['critters'])!=(18 if sid.endswith('caught') else 0):e.append('category/caught fixture absent')
 return e

def scope_errors(j):
 e=[];d=j['new_dispositions'][0]
 if d['scope_id']!='FVF-ED05296B9B54' or d['classification']!='DISPOSITIONED_FLAT_VISIBLE_ART_PENDING_REPLACEMENT' or d['role_count']!=5 or d['named_instance_count']!=40 or len(d['instances'])!=40 or len({x['name'] for x in d['instances']})!=40:e.append('helper split/claim incorrect')
 if len(d['callers'])!=8 or d['artistic_acceptance'] or d['replacement_count'] or j['actual_all_game_individual_piece_total'] is not None:e.append('false completeness/acceptance')
 for x in d['instances']:
  if x['classification']!='FLAT_VISIBLE_ART_PENDING_REPLACEMENT' or {v['aspect'] for v in x['native_instances']}!={'1280x720','1600x720'}:e.append('instance false exemption/missing aspect')
 return e

def check():
 errors=[];count=0;launch=read(P/'CAPTURE_LAUNCH.json')['records'];assert len(launch)==6
 signatures=set()
 for case in EXPECTED:
  for aspect in SIZES:
   folder=P/case/aspect;m=read(folder/'capture_manifest.json');errors+=matrix_errors(m,case,aspect)
   signatures.add(m['source_signature']['sha256']);rec=next(r for r in launch if r['case']==case and r['aspect']==aspect)
   if not rec['parent_normal_save_unchanged_after_exit'] or sha(P/rec['archived_harness'])!=m['harness_sha256']:errors.append('launch/save/harness drift')
   raw=(folder/'capture.log').read_text(encoding='utf8')
   if any(x in raw for x in ['SCRIPT ERROR','ERROR:','|FAIL|']):errors.append('native log has error')
   for row in m['states']:
    p=folder/row['image']['file'];count+=1
    if p.stat().st_size!=row['image']['bytes'] or sha(p)!=row['image']['sha256']:errors.append('native image hash/byte drift')
    with Image.open(p) as im:
     if im.size!=SIZES[aspect] or max(im.convert('L').getextrema())-min(im.convert('L').getextrema())<20:errors.append('blank/wrong-dimension image')
 if count!=62 or len(signatures)!=1:errors.append('wrong capture/source total')
 for row in read(P/'MACHINE.json')['sources']:
  raw=subprocess.check_output(['git','show',row['revision']+':'+row['path']],cwd=R)
  if hashlib.sha256(raw).hexdigest()!=row['git_blob_sha256'] or sha(R/row['path'])!=row['worktree_sha256']:errors.append('bound source drift')
 for row in read(P/'contact_index.json')['contacts']:
  if sha(P/row['path'])!=row['sha256']:errors.append('board drift')
  for source in row['sources']:
   if sha(P/source['path'])!=source['sha256']:errors.append('board source drift')
 errors+=scope_errors(read(P/'scope_dispositions.json'))
 briefs=read(P/'instance_briefs.json')['briefs'];instances=read(P/'scope_dispositions.json')['new_dispositions'][0]['instances']
 if len(briefs)!=40 or {b['instance_id'] for b in briefs}!={x['id'] for x in instances} or any(not b.get('occlusion_contact') or not b.get('states') or b['replacement_count'] for b in briefs):errors.append('missing/false instance context brief')
 c=read(P/'coverage.json');s=read(P/'scope_review.json')
 if c['declared_overlapping_entries']!=176 or c['partial_entries']!=39 or c['complete_entries']!=0 or any(x['route_or_saved_variants_complete'] for x in c['entries']):errors.append('false route completeness')
 if s['fully_resolved']!=3 or s['source_scope_count']!=369 or sum(x['fully_dispositioned'] for x in s['scopes'])!=3:errors.append('scope tally drift')
 if read(P/'observations.json')['replacements'] or read(P/'observations.json')['accepted_removals']:errors.append('false replacement')
 print('LIVE4|RESULT|'+('ALL OK;62 frames,6 matrices,40 helper instances,39 partial entries,366 unresolved scopes' if not errors else str(errors)))
 return int(bool(errors))

def stress():
 if check():return 1
 mutations=[('missing frame',lambda d:d['states'].pop()),('wrong renderer',lambda d:d.update(renderer='gl_compatibility')),('wrong engine',lambda d:d['engine'].update(patch=1)),('normal save mutation',lambda d:d['save_isolation']['after'].update(bak='bad')),('false menu',lambda d:d['states'][0]['actual'].update(start_menu_active=False)),('false pressed',lambda d:d['states'][2]['actual']['visible_canvas'].append({})),('false hold',lambda d:d['states'][7]['actual'].update(hold_fill_width=0)),('obscuring fade',lambda d:d['states'][0]['actual'].update(fade_alpha=1))]
 # Target draw-mode mutation uses exact observed node.
 mutations[5]=('false pressed',lambda d:node(d['states'][2]['actual'],'StartMenuOptionsTab').update(draw_mode=0))
 base=read(P/'saved/1280x720/capture_manifest.json')
 for name,mutate in mutations:
  d=copy.deepcopy(base);mutate(d);assert matrix_errors(d,'saved','1280x720'),name
 for name,mutate in [('missing instance',lambda d:d['new_dispositions'][0]['instances'].pop()),('false functional exemption',lambda d:d['new_dispositions'][0]['instances'][0].update(classification='EXEMPT_FUNCTIONAL')),('invented art total',lambda d:d.update(actual_all_game_individual_piece_total=40))]:
  d=read(P/'scope_dispositions.json');mutate(d);assert scope_errors(d),name
 print('LIVE4|STRESS|PASS11/11 falsifications rejected');return 0
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stress',action='store_true');a=ap.parse_args();raise SystemExit(stress() if a.stress else check())
