"""Independent integrity of diagnostic R6 room-route evidence; no QA11/acceptance PASS."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from immutable_source import source_bytes
import json,sys,hashlib,re,copy,argparse,subprocess
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent));from json_evidence import read_json
REV='6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f';ASPECTS=['1280x720','1600x720'];CASES=['cards','entry'];MODE={0:'normal',1:'pressed',2:'hover',3:'disabled',4:'hover_pressed'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,why):
 if not ok:raise ValueError(why)
def safe(name):
 p=Path(name);q=(HERE/p).resolve();need(not p.is_absolute() and '..' not in p.parts and q.is_relative_to(HERE),'unsafe packet path');return q
def root():
 return next(p for p in HERE.parents if (p/'project.godot').is_file())
def st(m,sid):return next(x for x in m['states'] if x['id']==sid)
def source_contract():
 src=(root()/'scripts/castle_career_routes.gd').read_text();reg=src.split('const ROOM_ACT_INDICES := {',1)[1].split('\n}',1)[0];rooms={k:[int(v) for v in re.findall(r'\d+',a)] for k,a in re.findall(r'"([^"]+)": \[([^]]+)\]',reg)}
 src=(root()/'scripts/opera_house.gd').read_text();acts={int(a):b for a,b in re.findall(r'"save_bit": (\d+),[^\n]+ "career": "[^"]+",\n\s*"costume": "([^"]+)"',src)};live=[int(v) for v in re.findall(r'\d+',src.split('const LIVE_ACT_INDICES: Array[int] = [',1)[1].split(']',1)[0])];mask=int(re.search(r'const ACTIVE_STAR_MASK := (0x[0-9A-Fa-f]+)',src)[1],16);need(sorted(acts)==live==sorted(x for a in rooms.values() for x in a),'source routes differ')
 ids={'cards':[],'entry':[]}
 for profile in ['unplayed','completed']:
  for room,indices in rooms.items():
   ids['cards'].append(f'cards_{profile}_{room}_idle')
   if profile=='unplayed':
    for act in indices:ids['cards'] += [f'cards_{room}_{act:02d}_{v}' for v in ['hover','pressed','focus']]
 for act in live:ids['entry'] += [f'route_{act:02d}_{v}' for v in ['before','entered','returned']]
 return rooms,acts,mask,ids

def guard(native,briefs,dis,obs,coverage):
 rooms,acts,mask,expected=source_contract();need(read_json(HERE/'EXPECTED_MATRIX.json')==expected,'detached expected matrix');need(len(briefs['briefs'])==48 and briefs['flat_caller_role_contexts']==25,'wrong caller role counts');seen=set()
 for (case,aspect),m in native.items():
  need(m['result']=='PASS' and m['failures']==0 and all(c['pass'] for c in m['checks']),'native failed');need(m['source_revision']==REV and m['source_unchanged'],'wrong source binding');need(m['renderer']=='mobile' and m['quality']=='speedy' and m['display_server']!='headless','wrong native renderer/display');need([m['engine'][k] for k in ['major','minor','patch','status','build']]==[4,7,2,'stable','official'],'wrong approved engine');need(m['aspect']==[int(v) for v in aspect.split('x')],'wrong aspect');need(m['harness_sha256']==sha((HERE.parent/'capture_room_routes.gd').read_bytes()),'detached harness');need(m['save_isolation']['unchanged'] and m['save_isolation']['before']==m['save_isolation']['after'] and len(m['save_isolation']['before'])==8,'normal save touched')
  need(m['expected_ids']==expected[case] and [s['id'] for s in m['states']]==expected[case],'wrong matrix');sig=m['source_signature'];need(len(sig['files'])==6442 and sig['paths']==sorted(sig['files']) and not sig['missing'],'wrong measured source list');need(sig['algorithm']=='sha256_runtime_roots_room_routes_v1' and sha('\n'.join(f"{p}:{sig['files'][p]}" for p in sig['paths']).encode())==sig['sha256'],'source fingerprint differs')
  for i,s in enumerate(m['states']):
   a=s['actual'];rr=a['room_routes'];need(s['sequence']==i and s['status']=='PASS','bad sequence/state');need(not a['tree_paused'] and not a['intro_active'] and not a['start_menu_active'] and not a['story_clip_present'] and a['fade_alpha']<=.001,'blocking overlay');need([s['image']['width'],s['image']['height']]==m['aspect'],'wrong image dimensions');need(rr['chapter2_story_complete'] and not rr['chapter2_active'] and not rr['day_one_jobs_locked'],'wrong route checkpoint');need(a['save_path']==m['save_isolation']['fresh_fixture_save'],'save path detached')
   for k,v in s['variant_expect'].items():need(a[k]==v,'variant detached')
   if case=='cards':
    completed=s['id'].startswith('cards_completed_');need(rr['opera_stars']==(mask if completed else 0),'saved marker wrong');need(sorted(b['act'] for b in rr['buttons'])==sorted(rooms[a['castle_room']]),'wrong room buttons');need(rr['routes_visible'] and not rr['opera_present'],'route hidden/launched unexpectedly')
    for b in rr['buttons']:
     need(b['visible'] and not b['disabled'],'route not reachable');need(b['rect'] and b['presentation'] in ['room_picture_card','historical_three_floor_portal'],'wrong button semantics')
     if a['castle_room']!='opera_hall':need(b['CareerPearl']['complete']==completed and b['CareerPearl']['visible'] and b['RoshanActor']['visible'] and b['CareerCrest']['visible'],'card/marker hidden/wrong')
    if s['id'].endswith(('_hover','_pressed','_focus')):
     act=int(s['id'].split('_')[-2]);b=next(b for b in rr['buttons'] if b['act']==act);need(b['draw_mode']=={'hover':2,'pressed':1,'focus':0}[s['id'].split('_')[-1]],'wrong observed draw mode')
     if s['id'].endswith('_focus'):need(b['focus'],'focus absent')
   else:
    act=int(s['id'].split('_')[1]);room=next(k for k,v in rooms.items() if act in v);need(a['castle_room']==room and rr['opera_stars']==0,'wrong owner room/reward');
    if s['id'].endswith('_entered'):need(a['game']=='opera' and rr['opera_present'] and rr['opera_act']==act and rr['act_state']=='play' and not rr['dev_playtest'] and not rr['story_mode'] and rr['return_room']==room and rr['living_stage']==f'opera.act.{act:02d}' and rr['world_layer']==10 and rr['world_visible'],'actual career entry owner differs')
    else:need(a['game']=='level2' and not rr['opera_present'] and rr['routes_visible'],'actual return/before differs')
 for b in briefs['briefs']:
  k=(b['act_index'],b['role']);need(k not in seen and b['act_index'] not in [2,8,13],'duplicate/noncard role');seen.add(k);need(b['career']==acts[b['act_index']] and b['room']==next(k for k,v in rooms.items() if b['act_index'] in v),'brief source detached');flat=b['role'] in ['frame','CareerPearl'] or (b['act_index']==16 and b['role']=='CareerCrest');need(b['classification']==('FLAT_VISIBLE_ART_PENDING_REPLACEMENT' if flat else 'PAINTED_RASTER_OR_ATLAS_SOURCE_CANDIDATE_PENDING_ACCEPTANCE'),'role misclassified');need(len(b['bindings'])==10 and len({(x['aspect'],x['state']) for x in b['bindings']})==10,'missing role variant')
  for x in b['bindings']:
   s=st(native[x['case'],x['aspect']],x['state']);button=next(q for q in s['actual']['room_routes']['buttons'] if q['act']==b['act_index']);value=button['styles'] if b['role']=='frame' else button[b['role']];need(x['observed']==value and x['image_sha256']==s['image']['sha256'] and x['draw_mode']==button['draw_mode'],'brief observations detached');need(x['node']==button['path']+('' if b['role']=='frame' else '/'+b['role']),'wrong role node')
 scope=dis['scopes'][0];need(scope['scope_id']=='FVF-C0A9DB89D09B' and scope['source_call_count']==5 and scope['visible_art_piece_count']==0 and scope['fully_dispositioned_for_inventory'],'invalid functional helper claim');src=(root()/'scripts/opera_house_venue_2d.gd').read_text();need(len(re.findall(r'_outline_style\(\s*Color.TRANSPARENT, Color.TRANSPARENT, 0, 54\)',src))==5,'helper callers changed')
 for x in scope['native_bindings']:
  s=st(native['cards',x['aspect']],x['state']);b=next(q for q in s['actual']['room_routes']['buttons'] if q['path']==x['button']);need(x['image_sha256']==s['image']['sha256'] and x['draw_mode']==b['draw_mode'],'helper detached');need(x['five_custom_styles']=={k:b['styles'][k] for k in ['normal','hover','pressed','focus','disabled']},'helper styles detached')
  for style in x['five_custom_styles'].values():need(style['bg_color'].endswith(', 0.0)') and style['border_color'].endswith(', 0.0)') and style['border_widths']==[0]*4 and style['shadow_size']==0,'visible functional helper art')
 need(len(obs['routes'])==30,'wrong pointer route observations')
 for x in obs['routes']:
  for y in x['states']:
   s=st(native['entry',x['aspect']],y['state']);need(y['actual']==s['actual']['room_routes'] and y['image_sha256']==s['image']['sha256'] and y['game']==s['actual']['game'] and y['castle_room']==s['actual']['castle_room'],'route observation detached')
 need(coverage['partial_entries']==sum(x['status'].startswith('PARTIAL_') for x in coverage['entries'])==62 and coverage['complete_entries']==0 and len(coverage['entries'])==176,'inflated coverage');need(all(next(x for x in coverage['entries'] if x['id']=='game.'+c)['status'].startswith('PARTIAL_') for c in acts.values()),'missing catalogue route context')
 return True

def validate(stress=False):
 native={(c,a):read_json(HERE/c/a/'capture_manifest.json') for c in CASES for a in ASPECTS};briefs=read_json(HERE/'INSTANCE_BRIEFS.json');dis=read_json(HERE/'SCOPE_DISPOSITIONS.json');obs=read_json(HERE/'EXACT_OBSERVATIONS.json');cov=read_json(HERE/'CUMULATIVE_COVERAGE.json');guard(native,briefs,dis,obs,cov)
 index=read_json(HERE/'NATIVE_INDEX.json');need(index['native_frames']==len(index['records'])==216,'native count');unique=set()
 for x in index['records']:
  need(x['path'] not in unique,'duplicate native');unique.add(x['path']);s=st(native[x['case'],x['aspect']],x['state']);f=s['image'];p=safe(x['path']);b=p.read_bytes();need(sha(b)==x['sha256']==f['sha256'] and len(b)==x['bytes']==f['bytes'],'native image bytes detached');im=Image.open(p);need(list(im.size)==x['dimensions']==native[x['case'],x['aspect']]['aspect'],'native image dimension detached')
 # Independently rehash every file in the measured declared suffix inventory; this is not full active closure.
 first=next(iter(native.values()))['source_signature'];need(all(m['source_signature']==first for m in native.values()),'per-run source list differs')
 for p,digest in first['files'].items():need(sha((root()/p).read_bytes())==digest,'current measured source changed '+p)
 for x in read_json(HERE/'SOURCE_PROOFS.json')['sources']:
  need(sha(safe(x['packet_path']).read_bytes())==x['git_lf_sha256'],'source proof bytes');need(sha(source_bytes(root(),REV,x['path']))==x['git_lf_sha256'],'git source proof changed')
 for x in read_json(HERE/'REUSE_INVENTORY.json')['sources']:need(sha((root()/x['path']).read_bytes())==x['sha256'],'reuse source changed')
 boards=read_json(HERE/'BOARDS.json')['boards'];need(len(boards)==14,'boards missing');covered=[]
 for x in boards:
  need(sha(safe(x['path']).read_bytes())==x['sha256'] and list(Image.open(safe(x['path'])).size)==x['dimensions'],'board bytes');need(x['visual_review']=='AGENT_DIAGNOSTIC_REVIEWED_NOT_ACCEPTED','board not reviewed')
  for b in x['bindings']:
   y=next(y for y in index['records'] if y['path']==b['native_path']);need(y['state']==b['state'] and y['sha256']==b['sha256'],'board detached');covered.append(b['native_path'])
 need(sorted(covered)==sorted(unique),'boards incomplete/duplicate');review=read_json(HERE/'VISUAL_REVIEW.json');need({(x['path'],x['sha256']) for x in review['boards']}=={(x['path'],x['sha256']) for x in boards},'review detached')
 for x in review['native_spot_reviews']:need(sha(safe(x['path']).read_bytes())==x['sha256'],'native spot detached')
 for x in read_json(HERE/'EARLIER_PHASE_BINDINGS.json')['phase_fixture_frames']:
  p=HERE.parent/'prior_native'/x['path'];need(sha(p.read_bytes())==x['sha256'] and x['input']['method']=='declared_phase_fixture','earlier phase bytes/method changed')
 for x in read_json(HERE/'diagnostics/native_launch.json'):need(x['exit_code']==0 and x['parent_normal_save_unchanged_after_exit'],'native driver failed')
 for c in CASES:
  for a in ASPECTS:
   text=(HERE/c/a/'native.log').read_text(encoding='utf8');need(not any(v in text for v in ['SCRIPT ERROR','|FAIL|','ERROR:']),'native log errors')
 need(not subprocess.check_output(['git','diff','92c9fe70319ef46bfaa8f61348a6f51512141ec3','--','scripts','scenes','assets','shaders','project.godot'],cwd=root()),'production changed')
 machine=read_json(HERE/'MACHINE.json');need(machine['cumulative_staged_frames']==1178 and machine['R6_total_staged_new_frames']==574 and machine['partial_entries']==62 and machine['cumulative_classified_scopes']==10 and machine['cumulative_unresolved_scopes']==359 and machine['replacements']==0,'machine inflated')
 scopes=read_json(HERE/'CUMULATIVE_SCOPES.json');need(len(scopes['scopes'])==369 and sum(bool(x['fully_dispositioned']) for x in scopes['scopes'])==10,'scope counts')
 negatives=[]
 if stress:
  tests=[('engine',lambda n,b,d,o,c:n['cards','1280x720']['engine'].update(patch=1)),('source set',lambda n,b,d,o,c:n['cards','1280x720']['source_signature']['files'].pop('project.godot')),('save drift',lambda n,b,d,o,c:n['cards','1280x720']['save_isolation']['after'].update({'':'fake'})),('saved marker',lambda n,b,d,o,c:st(n['cards','1280x720'],'cards_completed_library_idle')['actual']['room_routes'].update(opera_stars=0)),('wrong owner room',lambda n,b,d,o,c:st(n['entry','1280x720'],'route_16_entered')['actual'].update(castle_room='kitchen')),('dev launcher',lambda n,b,d,o,c:st(n['entry','1280x720'],'route_00_entered')['actual']['room_routes'].update(dev_playtest=True)),('hidden hit target',lambda n,b,d,o,c:st(n['cards','1280x720'],'cards_unplayed_library_idle')['actual']['room_routes']['buttons'][0].update(visible=False)),('missing caller role',lambda n,b,d,o,c:b['briefs'].pop()),('flat exempted',lambda n,b,d,o,c:b['briefs'][0].update(classification='ACCEPTED_PAINTED')),('wrong pressed draw mode',lambda n,b,d,o,c:next(x for x in st(n['cards','1280x720'],'cards_library_16_pressed')['actual']['room_routes']['buttons'] if x['act']==16).update(draw_mode=0)),('visible functional style',lambda n,b,d,o,c:d['scopes'][0]['native_bindings'][0]['five_custom_styles']['normal'].update(bg_color='(1.0, 1.0, 1.0, 1.0)')),('detached route observations',lambda n,b,d,o,c:o['routes'][0]['states'][0].update(image_sha256='0'*64)),('inflated catalogue coverage',lambda n,b,d,o,c:c.update(complete_entries=15))]
  for name,mutate in tests:
   args=copy.deepcopy((native,briefs,dis,obs,cov));mutate(*args)
   try:guard(*args)
   except (ValueError,KeyError,StopIteration):negatives.append(name)
   else:raise ValueError('falsification accepted: '+name)
 return {'result':'PASS_DIAGNOSTIC_INTEGRITY_ONLY','native_frames':216,'boards':14,'pointer_entries':30,'source_owner_returns':30,'caller_role_briefs':48,'flat_caller_context_roles':25,'classified_scopes':10,'unresolved_scopes':359,'partial_entries':62,'falsifications_rejected':negatives,'new_replacement_pixels':0,'DL_QA_11':'NOT_ACCEPTED','device_child_owner':'NOT_ACCEPTED'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stress',action='store_true');a=p.parse_args();print(json.dumps(validate(a.stress),indent=2))
