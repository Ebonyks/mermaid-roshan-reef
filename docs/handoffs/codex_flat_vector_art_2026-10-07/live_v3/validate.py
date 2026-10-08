"""Validate R3 evidence without granting complete inventory or artistic acceptance."""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];REV='fab9043e3e5f0b317424d89e234d6865a9605c11'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
EXPECTED=read(P/'EXPECTED_MATRIX.json');SIZES={'1280x720':(1280,720),'1600x720':(1600,720)}
def matrix_errors(m,case,aspect):
 e=[]
 if m.get('result')!='PASS' or m.get('failures')!=0 or any(not x['pass'] for x in m['checks']):e.append('native run/check failure')
 if m['source_revision']!=REV or m['renderer']!='mobile' or m['quality']!='speedy' or m['display_server']=='headless':e.append('wrong capture profile')
 if [m['engine'].get(k) for k in ['major','minor','patch','status','build']]!=[4,7,2,'stable','official']:e.append('wrong exact engine')
 if m['aspect']!=list(SIZES[aspect]) or m['run_case']!=case:e.append('wrong case/aspect')
 if m['expected_ids']!=EXPECTED[case] or [x['id'] for x in m['states']]!=EXPECTED[case]:e.append('incomplete/reordered matrix')
 save=m['save_isolation']
 if not save['unchanged'] or save['before']!=save['after'] or len(save['before'])!=8:e.append('normal save mutation/unattested')
 if not m['source_unchanged'] or m['source_signature']['missing'] or len(m['source_signature']['files'])!=6427:e.append('source drift/closure gap')
 for row in m['states']:
  a=row['actual'];im=row['image']
  if row['status']!='PASS' or a['castle_room_id']!=row['expected_room'] or a['save_path']!=save['fresh_fixture_save']:e.append('wrong state')
  if a['start_menu_active'] or a['intro_active'] or any(x['class']=='VideoStreamPlayer' for x in a['visible_canvas']):e.append('scene obscured by menu/movie')
  if case!='bathroom' and (a['tree_paused'] or a['story_clip_present'] or not a['castle_layer_visible'] or not a['castle_stage_visible'] or a['fade_alpha']>0.001):e.append('scene not live/visible')
  if (im['width'],im['height'])!=SIZES[aspect]:e.append('wrong encoded dimensions')
  if case=='pool':
   pool=a['pool'];sid=row['id'];mask=pool['skimmer']['mask']
   if sid=='01_skimmer_catch' and mask!=1:e.append('false first catch')
   if sid in ['02_pool_clear_waterfall_dirty','03_waterfall_scrub'] and (mask!=63 or pool['current_activity']!='waterfall'):e.append('false waterfall state')
   if sid in ['04_waterfall_clear_static','05_seahorse_tug_midway','06_seahorse_trash_release'] and pool['current_activity']!='seahorse':e.append('false seahorse state')
   if sid=='05_seahorse_tug_midway' and pool['seahorse']['taps']!=4:e.append('false midway state')
   if sid in ['07_rainbow_reveal_active','08_clean_pool_reveal'] and (not pool['finale_started'] or not pool['reveal_beat_holding'] or pool['tint_ratio']>0.05):e.append('false clean reveal')
  if case=='bathroom' and row['id']=='08b_toilet_scrubbing':
   t=a['bathroom_cleaning']['toilet']
   if not t['arrived'] or t['suspended'] or not 0<t['clean_progress']<1:e.append('paused/cancelled/missing toilet contact')
 return e

def functional_errors(d):
 e=[];ids=['FVF-A8BBC99C5C9E','FVF-F23CFD596774']
 if [s['scope_id'] for s in d['scopes']]!=ids:e.append('false functional scope expansion')
 for s in d['scopes']:
  if s['classification']!='FUNCTIONAL_TEXTURE_REVEAL_NO_FLAT_ART_RGB' or s['art_texture']!='assets/flats/castle/rooms/room_bubble_bath.png' or len(s['evidence'])!=10:e.append('unsupported art exemption')
 return e

def validate():
 e=[];source=None;launch=read(P/'CAPTURE_LAUNCH.json')['records']
 for case in EXPECTED:
  for aspect,size in SIZES.items():
   folder=P/case/aspect;m=read(folder/'capture_manifest.json');e+=matrix_errors(m,case,aspect)
   if source is None:source=m['source_signature']
   if source!=m['source_signature']:e.append('source changed across cases/aspects')
   rec=next(r for r in launch if r['case']==case and r['aspect']==aspect)
   if rec['exit_code']!=0 or not rec['parent_normal_save_unchanged_after_exit'] or rec['harness_sha256']!=m['harness_sha256'] or sha(P/rec['archived_harness'])!=m['harness_sha256']:e.append('launch/harness/parent-save mismatch')
   log=(folder/'capture.log').read_bytes().decode('utf8',errors='replace')
   if any(s in log for s in ['SCRIPT ERROR','ERROR:','|FAIL|']):e.append('native diagnostic error')
   for row in m['states']:
    im=row['image'];path=folder/im['file']
    if path.parent!=folder or sha(path)!=im['sha256'] or path.stat().st_size!=im['bytes']:e.append('image path/bytes/hash mismatch')
    with Image.open(path) as image:
     if image.size!=size:e.append('decoded dimensions mismatch')
     lo,hi=image.convert('L').resize((64,36)).getextrema()
     if hi-lo<51:e.append('blank frame')
 for path,h in source['files'].items():
  if sha(R/path)!=h:e.append('source closure drift '+path)
 for contact in read(P/'contact_index.json')['contacts']:
  if sha(P/contact['path'])!=contact['sha256']:e.append('contact hash mismatch')
  for s in contact['sources']:
   if sha(P/s['path'])!=s['sha256']:e.append('board source drift')
 d=read(P/'functional_dispositions.json');e+=functional_errors(d)
 cleanup=(R/'scripts/games/day_one_bathroom_cleanup.gd').read_text(encoding='utf8');scrub=(R/'scripts/games/day_one_fixture_scrub.gd').read_text(encoding='utf8')
 if 'sink.texture = CLEAN_ROOM_TEXTURE' not in cleanup or 'COLOR.a *= dirt_layer ? 1.0 - cleaned : cleaned;' not in scrub or 'Image.FORMAT_L8' not in scrub:e.append('functional derivation changed')
 frozen={s['id']:s for s in read(P.parent/'source_scopes.json')['scopes']}
 for s in d['scopes']:
  f=frozen[s['scope_id']];ls=(R/f['path']).read_text(encoding='utf8').splitlines(keepends=True);text=''.join(ls[f['start_line']-1:f['end_line']]).replace('\r\n','\n')
  # Frozen hash is supplied by R1 scope contract; R1 validator owns exact range convention.
  if s['source']!=f:e.append('functional frozen source binding mismatch')
  for ref in s['evidence']:
   m=read((P/ref).parent/'capture_manifest.json');state=next(x for x in m['states'] if x['image']['file']==Path(ref).name)
   for row in state['actual']['visible_canvas']:
    if row['class']=='Polygon2D' and not row.get('textured_polygon'):e.append('untextured functional polygon')
 coverage=read(P/'coverage.json');scopes=read(P/'scope_review.json');obs=read(P/'observations.json')
 if len(coverage['entries'])!=176 or coverage['partial_entries']!=30 or coverage['complete_entries']!=0 or any(x['route_or_saved_variants_complete'] for x in coverage['entries']):e.append('false route closure')
 if len(scopes['scopes'])!=369 or scopes['fully_resolved']!=2 or sum(x['fully_dispositioned'] for x in scopes['scopes'])!=2:e.append('false scope closure')
 if obs['whole_game_denominator'] is not None or obs['replacements']!=0 or obs['accepted_removals']!=0:e.append('false art total/removal')
 if subprocess.run(['git','diff','--quiet','92c9fe70319ef46bfaa8f61348a6f51512141ec3','HEAD','--','scripts','scenes','assets','shaders','project.godot'],cwd=R).returncode:e.append('production source changed')
 return e

def stress():
 m=read(P/'pool/1280x720/capture_manifest.json');cases=[]
 for change in ['missing','renderer','engine','save','menu','pause','endpoint']:
  a=copy.deepcopy(m)
  if change=='missing':a['states'].pop()
  if change=='renderer':a['renderer']='gl_compatibility'
  if change=='engine':a['engine']['patch']=1
  if change=='save':a['save_isolation']['unchanged']=False
  if change=='menu':a['states'][0]['actual']['start_menu_active']=True
  if change=='pause':a['states'][0]['actual']['tree_paused']=True
  if change=='endpoint':a['states'][-1]['actual']['pool']['finale_started']=False
  cases.append(bool(matrix_errors(a,'pool','1280x720')))
 d=copy.deepcopy(read(P/'functional_dispositions.json'));d['scopes'][0]['art_texture']='generated_flat_shape.png';cases.append(bool(functional_errors(d)))
 b=read(P/'bathroom/1280x720/capture_manifest.json');next(s for s in b['states'] if s['id']=='08b_toilet_scrubbing')['actual']['bathroom_cleaning']['toilet']['suspended']=True;cases.append(bool(matrix_errors(b,'bathroom','1280x720')))
 print('R3 falsification:',sum(cases),'/',len(cases),'rejected');return all(cases)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stress',action='store_true');a=ap.parse_args()
 if a.stress:raise SystemExit(0 if stress() else 1)
 e=validate()
 if e:print('\n'.join(e));raise SystemExit(1)
 print('R3 PASS:100 native frames, six matrices,6427 source hashes/save isolation;30/176 partial,0 complete,2 functional scopes,367 unresolved;no replacement/acceptance')
