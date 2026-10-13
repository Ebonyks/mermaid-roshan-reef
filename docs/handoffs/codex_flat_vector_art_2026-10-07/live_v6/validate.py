"""Check diagnostic R6 integrity; no DL-QA-11 or creative/device acceptance."""
from pathlib import Path
from immutable_source import source_bytes
import argparse,copy,json,hashlib,subprocess,tempfile,urllib.request
from PIL import Image
from json_evidence import read_json,unique,SCHEMA
P=Path(__file__).resolve().parent;R=P.parents[3];REV='6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f'
EXPECTED=read_json(P/'EXPECTED_MATRIX.json');ASPECTS={'1280x720':(1280,720),'1600x720':(1600,720)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def native_node(a,name):return next((n for n in a['visible_canvas'] if n['path'].split('/')[-1]==name),{})
def matrix_errors(m,case,aspect):
 e=[]
 if m['source_revision']!=REV or m['result']!='PASS' or m['failures'] or m['renderer']!='mobile' or m['quality']!='speedy' or m['display_server']=='headless':e.append('native/source/profile mismatch')
 if [m['engine'].get(k) for k in ['major','minor','patch','status','build']]!=[4,7,2,'stable','official']:e.append('engine mismatch')
 if m['run_case']!=case or m['aspect']!=list(ASPECTS[aspect]) or m['expected_ids']!=EXPECTED[case] or [x['id'] for x in m['states']]!=EXPECTED[case]:e.append('matrix mismatch')
 if not m['source_unchanged'] or m['source_signature']['missing'] or len(m['source_signature']['files'])!=6427:e.append('source closure incomplete')
 ss=m['save_isolation']
 if not ss['unchanged'] or ss['before']!=ss['after'] or len(ss['before'])!=8:e.append('normal save mismatch')
 for row in m['states']:
  a=row['actual'];sid=row['id'];t=a['touch']
  if row['status']!='PASS' or a['save_path']!=ss['fresh_fixture_save'] or a['tree_paused'] or a['start_menu_active'] or a['intro_active'] or a['story_clip_present'] or a['fade_alpha']>0.001:e.append('state/pause/overlay mismatch')
  if row['expected_top_target'] and not native_node(a,row['expected_top_target']):e.append('native target missing')
  if any(a.get(k)!=v for k,v in row['variant_expect'].items()):e.append('variant mismatch')
  if len(t['circles'])!=3 or {x['role'] for x in t['circles']}!={'base','knob','hint'} or any(x['visible'] or x['in_tree'] for x in t['circles']):e.append('hidden circle mismatch')
  if case=='menu' and any(sid.startswith('menu_'+s+'_') for s in ['hover','pressed','focus']):
   act=int(sid.split('_')[-1]);n=native_node(a,'PlaytestJob_%02d'%act)
   if not a['menu_open'] or not a['menu_visible'] or a['menu_running'] or not a['menu_guard']:e.append('menu guard/ownership mismatch')
   if sid.startswith('menu_hover_') and n.get('draw_mode')!=2:e.append('hover absent')
   if sid.startswith('menu_pressed_') and n.get('draw_mode') not in [1,4]:e.append('pressed absent')
   if sid.startswith('menu_focus_') and not n.get('focus'):e.append('focus absent')
  if case=='touch':
   if a['phase']!='promenade' or a['castle_layer_present'] or t['mode']!=sid.split('_')[1] or a['saved_touch_mode']!=t['mode']:e.append('touch route/mode mismatch')
   if sid.endswith('_flash') and len(t['flashes'])!=1:e.append('flash absent')
   if sid.endswith('world_release_after_hold') and (t['press_elapsed_ms']<=300 or len(t['flashes'])!=(1 if t['mode']=='hybrid' else 0)):e.append('long hold mismatch')
   if sid.endswith('settled') or sid.endswith('cancelled'):
    if t['flashes'] or t['touch_idx']!=-1:e.append('input/flash not retired')
 return e

def check():
 count=0
 for case in EXPECTED:
  for aspect,size in ASPECTS.items():
   m=read_json(P/case/aspect/'capture_manifest.json');assert not matrix_errors(m,case,aspect),matrix_errors(m,case,aspect)
   assert sha(P/('capture_'+case+'.gd'))==m['harness_sha256']
   for row in m['states']:
    f=P/case/aspect/row['image']['file'];assert f.stat().st_size==row['image']['bytes'] and sha(f)==row['image']['sha256']
    with Image.open(f) as im:assert im.size==size
    count+=1
   for name,h in m['source_signature']['files'].items():assert (R/name).is_file() and sha(R/name)==h, name
 assert count==150
 d=read_json(P/'scope_dispositions.json');items=d['new_dispositions'][0]['instances'];assert len(items)==31 and len({x['id'] for x in items})==31 and d['unresolved_source_scopes']==362 and d['actual_all_game_individual_piece_total'] is None
 assert sum('PENDING_REPLACEMENT' in x['classification'] for x in items)==17
 assert sum(x['classification']=='PAINTED_SOURCE_REVIEW_CANDIDATE' for x in items)==14
 for item in items:
  for b in item['bindings']:
   st=next(x for x in read_json(P/'menu'/b['aspect']/'capture_manifest.json')['states'] if x['id']==b['state']);assert b['node'] in st['actual']['visible_canvas'] and b['image_sha256']==st['image']['sha256']
 assert len(read_json(P/'instance_briefs.json')['briefs'])==35
 c=read_json(P/'coverage.json');s=read_json(P/'scope_review.json');assert len(c['entries'])==176 and c['partial_entries']==45 and c['complete_entries']==0 and len(s['scopes'])==369 and s['fully_resolved']==7
 assert sum(x['fully_dispositioned'] for x in s['scopes'])==7 and s['partial_context_scopes']==40
 launches=read_json(P/'CAPTURE_LAUNCH.json')['records'];assert len(launches)==4 and all(x['exit_code']==0 and x['parent_normal_save_unchanged_after_exit'] for x in launches)
 for row in read_json(P/'MACHINE.json')['sources']:
  b=source_bytes(R,row['revision'],row['path']);assert hashlib.sha256(b).hexdigest()==row['git_blob_sha256'] and sha(R/row['path'])==row['worktree_sha256']
 for x in read_json(P/'contact_index.json')['contacts']:assert sha(P/x['path'])==x['sha256']
 for x in read_json(P/'R5_PRESERVATION_PROOF.json')['checks']:
  url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/5e5140fb0f0b636825354b6db8d28da0e9c07446/'+x['path']
  with urllib.request.urlopen(url,timeout=60) as response: original=response.read();assert response.status==200
  assert hashlib.sha256(original).hexdigest()==x['reconstructed_bytes_sha256'] and len(original)==x['original_bytes'];assert read_json(P/x['derivative_index'])==unique(original)
 print('LIVE6|ALL OK|150native,4matrices,35briefs,31finite-menu-objects,45partial,362unresolved;R5unchanged;noacceptance')

def stress():
 m=read_json(P/'menu/1280x720/capture_manifest.json');tests=[]
 for field,value in [('renderer','gl_compatibility'),('source_revision','0'*40),('display_server','headless')]:
  x=copy.deepcopy(m);x[field]=value;tests.append((field,bool(matrix_errors(x,'menu','1280x720'))))
 x=copy.deepcopy(m);x['states'].pop();tests.append(('missing native state',bool(matrix_errors(x,'menu','1280x720'))))
 x=copy.deepcopy(m);x['save_isolation']['unchanged']=False;tests.append(('save mutation',bool(matrix_errors(x,'menu','1280x720'))))
 x=copy.deepcopy(m);x['states'][0]['actual']['touch']['circles'][0]['visible']=True;tests.append(('hidden art visibility',bool(matrix_errors(x,'menu','1280x720'))))
 x=copy.deepcopy(m);files=x['source_signature']['files'];files.pop(next(iter(files)));tests.append(('missing source closure',bool(matrix_errors(x,'menu','1280x720'))))
 index=json.loads((P/'menu/1280x720/capture_manifest.json').read_text());assert index['schema']==SCHEMA
 # These falsifications touch only a disposable temporary copy of the already verified sections.
 with tempfile.TemporaryDirectory() as tmp:
  q=Path(tmp);import shutil
  for row in index['sections']:
   dest=q/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'menu/1280x720'/row['path'],dest)
  for name,mutate in [('section hash',lambda d:d['sections'][0].update(sha256='0'*64)),('original hash',lambda d:d.update(original_sha256='0'*64)),('path escape',lambda d:d['sections'][0].update(path='../outside')),('duplicate section',lambda d:d['sections'].append(d['sections'][0]))]:
   x=copy.deepcopy(index);mutate(x);f=q/'index.json';f.write_text(json.dumps(x));caught=False
   try:read_json(f)
   except (ValueError,OSError):caught=True
   tests.append((name,caught))
 assert all(v for _,v in tests),tests
 print('LIVE6|STRESS|11/11rejected',tests)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stress',action='store_true');args=ap.parse_args();check()
 if args.stress:stress()
