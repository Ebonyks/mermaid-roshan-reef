"""Check R5 diagnostic capture/scope evidence. Never grant DL-QA-11/owner acceptance."""
from pathlib import Path
import argparse,copy,json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];REV='6c2f3fb6b47ac247521cb4bd029d258c4f060693'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
EXPECTED=read(P/'EXPECTED_MATRIX.json');SIZES={'1280x720':(1280,720),'1600x720':(1600,720)}
def node(a,name):return next((n for n in a['visible_canvas'] if n['path'].split('/')[-1]==name),{})

IDS={'FVF-338855F9AA24':14,'FVF-C0BEBF640F83':2,'FVF-0F7C86F20C97':7}
COLORS=['45dbebff','85f2b8ff','ffc74dff','ff7a8cff','bd94ffff']
PALETTE=['fa8ca6','ffb86b','ffe673','8ce699','73d1f2','9e8cf2','f2b3e6','f7f5ed']
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
  if row['status']!='PASS' or a['save_path']!=ss['fresh_fixture_save'] or a['tree_paused'] or row['expected_pause']:e.append('state/pause/save mismatch')
  if a['start_menu_active'] or a['intro_active']:e.append('obscured by menu')
  if a['story_clip_present'] or a['fade_alpha']>0.001 or any(n['class']=='VideoStreamPlayer' for n in a['visible_canvas']):e.append('obscured by movie/fade')
  if (im['width'],im['height'])!=SIZES[aspect]:e.append('encoded dimensions mismatch')
  if not node(a,row['expected_top_target']):e.append('expected native target missing')
  for key,value in row['variant_expect'].items():
   if a.get(key)!=value:e.append('variant mismatch '+key)
  for n in a['visible_canvas']:
   if n.get('text') and not n.get('font',{}).get('family'):e.append('missing theme font context')
  if case=='companion':
   if sid.startswith('care_'):
    if not a['care_visible'] or a.get('castle_layer_present') or a['phase']!='promenade':e.append('care route not currentCanvasforeground')
    if sid.startswith('care_active_') and a['care_want']!=sid[12:]:e.append('active want mismatch')
    if sid.startswith('care_queued_') and a['care_queue']!=[sid[12:]]:e.append('queued want mismatch')
    if sid=='care_busy' and (a['care_t']<=0 or not all(node(a,'StuffieCareAction_'+w).get('disabled') for w in ['feed','nap','bath','cuddle','play'])):e.append('disabled care state absent')
    if sid.startswith('care_growth_') and a['care_points']!=int(sid.split('_')[-1]):e.append('growth state mismatch')
    if sid=='care_canvas_fulfilled' and (a['care_want'] or a['care_points']!=1):e.append('Canvas care feedback mismatch')
   else:
    if not a['picker_visible']:e.append('picker absent')
    if sid.startswith('palette_'):
     _,slot,color=sid.split('_');slot=int(slot);color=int(color)
     if a['pick_id']!='mewsha' or a['pick_slot']!=slot or a['pick_colors'][slot].lower()!=PALETTE[color]:e.append('palette selection/paint profile mismatch')
    if sid=='picker_rescue_current_step2' and (not a['rescue'] or a['rescue_step']!=2 or a['pick_id']!='eagle' or a['castle_room']!='playroom'):e.append('normal rescue guard mismatch')
  elif case=='logo':
   if sid in EXPECTED['logo'][:48]:
    _,color,symbol=sid.split('_')
    target=node(a,'CastleLogoPreview');children=[x for x in a['visible_canvas'] if x['path'].startswith(target.get('path','')+'/')]
    if a['logo_color']!=color or a['logo_symbol']!=symbol or not a['logo_visible'] or not any(x.get('texture','').endswith('/castle_banner_motif_'+symbol+'.png') for x in children):e.append('logo motif/color/native binding mismatch')
   if sid=='logo_hover' and node(a,'CastleLogoColor_pink').get('draw_mode')!=2:e.append('logo hover absent')
   if sid=='logo_pressed' and node(a,'CastleLogoColor_pink').get('draw_mode') not in [1,4]:e.append('logo pressed absent')
   if sid.startswith('logo_badge_') and (a['logo_visible'] or a['logo_color']!=sid[11:] or node(a,'CastleLogoCraftBoardBadge').get('properties',{}).get('color_id')!=sid[11:]):e.append('badge color absent')
   if sid=='logo_no_room_badge' and any('CastleLogoRoomDisplay' in n['path'] for n in a['visible_canvas']):e.append('negative room display still present')
  elif case=='attack' and sid!='attack_confirmed':
   cs=[n for n in a['visible_canvas'] if n.get('properties',{}).get('choice_effect')==''];fx=[n for n in a['visible_canvas'] if n.get('properties',{}).get('choice_effect') in ['bubbles','splashes']]
   if not a['attack_visible'] or len(cs)!=5 or len(fx)!=2:e.append('attack draw instances missing')
   if sid in EXPECTED['attack'][:10] and len(cs)==5 and len(fx)==2:
    _,i,effect=sid.split('_');i=int(i)
    if a['attack_color']!=COLORS[i] or a['attack_effect']!=effect or [n['properties']['selected'] for n in cs]!=[k==i for k in range(5)] or any(n['properties']['selected']!=(n['properties']['choice_effect']==effect) for n in fx):e.append('selected attack profile mismatch')
    for n in fx:
     p=n['properties'];b=p['choice_effect']=='bubbles'
     if p['atlas_frame']!=(2 if b else 5) or p['atlas_grid']!=('(4, 2)' if b else '(3, 3)') or not p['choice_texture'].endswith('fx_water_bubble_burst_atlas.png' if b else 'fx_water_splash_medium_atlas.png'):e.append('atlas binding mismatch')
   if cs and sid=='attack_hover' and cs[0]['draw_mode']!=2:e.append('attack hover absent')
   if cs and sid=='attack_pressed' and cs[0]['draw_mode'] not in [1,4]:e.append('attack pressed absent')
 return e

def scope_errors(d):
 e=[];sc=d['new_dispositions'];items=[x for s in sc for x in s['instances']]
 if {s['scope_id']:s['named_instance_count'] for s in sc}!=IDS or len(items)!=23 or len({x['id'] for x in items})!=23 or d['actual_all_game_individual_piece_total'] is not None:e.append('invented/missing instance count')
 for s in sc:
  if len(s['instances'])!=s['named_instance_count'] or not s['callers'] or not s['branch_proof']:e.append('scope caller/branch proof missing')
 for x in items:
  if x['classification'] not in ['FLAT_VISIBLE_ART_PENDING_REPLACEMENT','FLAT_RASTER_ART_PENDING_REPLACEMENT','FONT_ILLUSTRATIVE_ART_PENDING_REPLACEMENT'] or x['replacement_count'] or x['accepted_removal_count'] or {b['aspect'] for b in x['bindings']}!={'1280x720','1600x720'}:e.append('false exemption/unbound instance')
 return e

def check():
 errors=[];count=0;launch=read(P/'CAPTURE_LAUNCH.json')['records'];assert len(launch)==6
 signatures=set();capture_data={}
 for case in EXPECTED:
  for aspect in SIZES:
   folder=P/case/aspect;m=read(folder/'capture_manifest.json');errors+=matrix_errors(m,case,aspect)
   capture_data[(case,aspect)]={x['id']:x for x in m['states']};signatures.add(m['source_signature']['sha256']);rec=next(r for r in launch if r['case']==case and r['aspect']==aspect)
   if not rec['parent_normal_save_unchanged_after_exit'] or sha(P/rec['archived_harness'])!=m['harness_sha256']:errors.append('launch/save/harness drift')
   raw=(folder/'capture.log').read_text(encoding='utf8')
   if any(x in raw for x in ['SCRIPT ERROR','ERROR:','|FAIL|']):errors.append('native log error')
   for row in m['states']:
    p=folder/row['image']['file'];count+=1
    if p.stat().st_size!=row['image']['bytes'] or sha(p)!=row['image']['sha256']:errors.append('native image hash/byte drift')
    with Image.open(p) as im:
     if im.size!=SIZES[aspect] or max(im.convert('L').getextrema())-min(im.convert('L').getextrema())<20:errors.append('blank/wrong-dimension image')
 if count!=250 or len(signatures)!=1:errors.append('wrong native/source count')
 for row in read(P/'MACHINE.json')['sources']:
  raw=subprocess.check_output(['git','show',row['revision']+':'+row['path']],cwd=R)
  if hashlib.sha256(raw).hexdigest()!=row['git_blob_sha256'] or sha(R/row['path'])!=row['worktree_sha256']:errors.append('source drift')
 for row in read(P/'contact_index.json')['contacts']:
  if sha(P/row['path'])!=row['sha256']:errors.append('board drift')
  for source in row['sources']:
   if sha(P/source['path'])!=source['sha256']:errors.append('board source drift')
 errors+=scope_errors(read(P/'scope_dispositions.json'))
 instances=[x for s in read(P/'scope_dispositions.json')['new_dispositions'] for x in s['instances']];briefs=read(P/'instance_briefs.json')['briefs']
 for item in instances:
  for binding in item['bindings']:
   case,aspect,_=binding['capture_manifest'].split('/')
   original=capture_data[(case,aspect)].get(binding['state'],{})
   if not original or binding['node'] not in original['actual']['visible_canvas'] or binding['image_sha256']!=original['image']['sha256'] or binding['image']!=case+'/'+aspect+'/'+original['image']['file']:errors.append('instance binding not native evidence')
   if item['id'].startswith('AttackSelectedRing') and not binding['node'].get('properties',{}).get('selected'):errors.append('ring claimed while unselected')
 if len(briefs)!=23 or {b['instance_id'] for b in briefs}!={x['id'] for x in instances} or any(not b.get('occlusion_contact') or not b.get('states') or b['replacement_count'] for b in briefs):errors.append('missing/false instance brief')
 c=read(P/'coverage.json');s=read(P/'scope_review.json')
 if c['declared_overlapping_entries']!=176 or c['partial_entries']!=43 or c['complete_entries']!=0 or any(x['route_or_saved_variants_complete'] for x in c['entries']):errors.append('false entry completeness')
 if s['fully_resolved']!=6 or s['source_scope_count']!=369 or sum(x['fully_dispositioned'] for x in s['scopes'])!=6:errors.append('scope tally drift')
 if read(P/'observations.json')['replacements'] or read(P/'observations.json')['accepted_removals']:errors.append('false replacement')
 print('LIVE5|RESULT|'+('ALL OK;250 frames,6 matrices,23 namedinstances,43 partialentries,363 unresolvedscopes' if not errors else str(errors)))
 return int(bool(errors))

def stress():
 if check():return 1
 tests=[('missingframe','logo',lambda d:d['states'].pop()),('wrongengine','logo',lambda d:d['engine'].update(patch=1)),('sourcegap','logo',lambda d:d['source_signature']['files'].pop(next(iter(d['source_signature']['files'])))),('normalSave','logo',lambda d:d['save_isolation']['after'].update(bak='bad')),('menucovers','logo',lambda d:d['states'][0]['actual'].update(start_menu_active=True)),('moviecovers','logo',lambda d:d['states'][0]['actual'].update(story_clip_present=True)),('wrongLogo','logo',lambda d:d['states'][0]['actual'].update(logo_symbol='dog')),('wrongfont','logo',lambda d:node(d['states'][0]['actual'],'CastleLogoTitle').update(font={})),('careCachedCastle','companion',lambda d:d['states'][32]['actual'].update(castle_layer_present=True)),('wrongPalette','companion',lambda d:d['states'][7]['actual'].update(pick_slot=2)),('falseCircleSelection','attack',lambda d:next(n for n in d['states'][0]['actual']['visible_canvas'] if n.get('properties',{}).get('choice_effect')=='')['properties'].update(selected=False))]
 for name,case,mut in tests:
  d=read(P/case/'1280x720/capture_manifest.json');mut(d);assert matrix_errors(d,case,'1280x720'),name
 for name,mut in [('missinginstance',lambda d:d['new_dispositions'][0]['instances'].pop()),('falseRasterExemption',lambda d:d['new_dispositions'][0]['instances'][0].update(classification='EXEMPT_FUNCTIONAL')),('inventedGlobalTotal',lambda d:d.update(actual_all_game_individual_piece_total=23))]:
  d=read(P/'scope_dispositions.json');mut(d);assert scope_errors(d),name
 print('LIVE5|STRESS|PASS14/14 falsifications rejected');return 0
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stress',action='store_true');a=ap.parse_args();raise SystemExit(stress() if a.stress else check())
