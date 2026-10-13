"""Independent integrity checks for the staged HUD/fashion diagnostic inventory.
No runtime/device/child/owner or DL-QA-11 acceptance is asserted.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from immutable_source import source_bytes
import argparse,copy,hashlib,json,math,re,sys,subprocess
from PIL import Image
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent));from json_evidence import read_json
REV='6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f'
ASPECTS=['1280x720','1600x720'];CASES=['fashion','practice','hud']
MODE={0:'normal',1:'pressed',2:'hover',3:'disabled',4:'hover_pressed'}
def sha(data):return hashlib.sha256(data).hexdigest()
def need(ok,why):
 if not ok:raise ValueError(why)
def safe(path):
 p=Path(path);need(not p.is_absolute() and '..' not in p.parts,'unsafe path');q=(HERE/p).resolve();need(q.is_relative_to(HERE),'outside packet');return q
def tree_root():
 for p in HERE.parents:
  if (p/'project.godot').is_file() and (p/'tools/audit_game_2d.py').is_file():return p
 raise ValueError('project root absent')
def state(m,sid):return next(s for s in m['states'] if s['id']==sid)
def geometry_guard(native,catalog,dis,obs):
 for (case,aspect),m in native.items():
  need(m['result']=='PASS' and not m['failures'] and all(c['pass'] for c in m['checks']),'native process failed')
  need(m['source_revision']==REV and m['source_unchanged'],'source changed')
  need(m['save_isolation']['unchanged'] and m['save_isolation']['before']==m['save_isolation']['after'] and len(m['save_isolation']['before'])==8,'normal save changed')
  need([m['engine'].get(k) for k in ['major','minor','patch','status','build']]==[4,7,2,'stable','official'],'wrong engine')
  need(m['renderer']=='mobile' and m['quality']=='speedy','wrong runtime profile')
  need(m['aspect']==[int(v) for v in aspect.split('x')],'wrong backing aspect')
  ids=[s['id'] for s in m['states']];need(ids==m['expected_ids'] and len(ids)==len(set(ids)),'wrong ordered matrix')
  need(len(ids)=={'fashion':79,'practice':6,'hud':19}[case],'wrong matrix count')
  for i,s in enumerate(m['states']):
   need(s['sequence']==i and s['status']=='PASS','state sequence/status failed')
   need(s['actual']['tree_paused']==s['expected_pause'] and not s['actual']['intro_active'],'unexpected overlay/pause')
   need([s['image']['width'],s['image']['height']]==m['aspect'],'image aspect mismatch')
  sig=m['source_signature'];need(len(sig['files'])==6442 and not sig['missing'] and sig['paths']==sorted(sig['files']),'incomplete measured source set')
  need(sig['algorithm']=='sha256_runtime_roots_hud_fashion_v3','wrong measured source algorithm')
  need(sha('\n'.join(f"{p}:{sig['files'][p]}" for p in sig['paths']).encode())==sig['sha256'],'source list identity')
 # Source-derived TRES IDs independently reconstructed,not from hand-authored brief counts.
 root=tree_root();data=json.loads((root/'assets/fashion/slots_v1/catalog.tres').read_text(encoding='utf8').split('data = ',1)[1]);items=data['items']
 skin=json.loads((root/'assets/fashion/skin_engine_v2/catalog.tres').read_text(encoding='utf8').split('data = ',1)[1]);source_contexts=set()
 for person in ['roshan','rumi','daddy_mermaid']:
  for item in items:
   if item['character'] in ['*',person]:source_contexts.add((person,item['slot'],item['id']))
  for item in skin['outfits']:
   if item['character']==person:source_contexts.add((person,'body',item['id']))
 need({(e['person'],e['slot'],e['item_id']) for e in catalog['entries']}==source_contexts,'source catalog closure differs')
 need(catalog['total']==79 and len(catalog['entries'])==79,'catalog count')
 seen=set()
 for e in catalog['entries']:
  key=(e['person'],e['slot'],e['item_id']);need(key not in seen,'duplicate catalog context');seen.add(key)
  need(e['person'] in ['roshan','rumi','daddy_mermaid'] and e['slot'] in ['head','body','tail'],'invalid current picker')
  # Preflight source-derived groups are independently bound to exact current source/catalog files below.
  need(len(e['bindings'])==4 and len({(b['aspect'],b['profile']) for b in e['bindings']})==4,'missing catalog states')
  for b in e['bindings']:
   s=state(native['fashion',b['aspect']],b['state']);hf=s['actual']['hud_fashion'];need(hf['person']==e['person'] and hf['slot']==e['slot'] and hf['page']==e['source_page'],'wrong catalog selection/page')
   need(b['image_sha256']==s['image']['sha256'],'catalog image detached');card=next(n for n in s['actual']['visible_canvas'] if n['path']==b['node']);need(card['path'].endswith('/FashionOutfit_'+e['item_id']),'wrong card target');need(card['draw_mode']==b['draw_mode'] and card['styles'][MODE[card['draw_mode']]]['class']==b['selected_style_class']=='StyleBoxTexture','wrong drawn card style')
   portraits=[{'path':n['path'],'texture':n.get('texture')} for n in s['actual']['visible_canvas'] if n['path'].startswith(card['path']+'/') and n['class']=='TextureRect'];need(portraits==b['portraits'] and portraits,'missing portrait')
 for a in ASPECTS:
  fm=native['fashion',a]
  # Actual native pick/reload/focus-cancel facts,not saved phase display fixtures.
  need(not state(fm,'fashion_drag_focus_cancelled')['actual']['hud_fashion']['drag_active'],'held garment not cancelled')
  need(state(fm,'fashion_drag_moved')['actual']['hud_fashion']['drag_active'],'drag missing')
  need(state(fm,'fashion_saved_reload')['actual']['hud_fashion']['selected_parts']==state(fm,'fashion_daddy_mermaid_ribbon_settled')['actual']['hud_fashion']['selected_parts'],'clothing reload differs')
  need(state(fm,'fashion_locked_pressed')['actual']['hud_fashion']['selected_parts']==state(fm,'fashion_locked_released')['actual']['hud_fashion']['selected_parts'],'locked card changed clothes')
  for person in ['roshan','rumi','daddy_mermaid']:
   s=state(fm,f'fashion_{person}_ribbon_picked');hf=s['actual']['hud_fashion'];need(hf['person']==person and hf['burst_children']==14,'wrong pick/burst person')
   need(hf['selected_parts'][person]['body']==person+'_ribbon_v1','actual ribbon pick absent')
   need(state(fm,f'fashion_{person}_ribbon_settled')['actual']['hud_fashion']['burst_children']==0,'burst not freed')
  pm=native['practice',a]
  for sid,mask in [('fashion_practice_saved_phase0',0),('fashion_practice_phase0_after_pointer',0),('fashion_practice_saved_phase1',1),('fashion_practice_saved_phase2',3),('fashion_practice_saved_complete',7)]:
   s=state(pm,sid);hf=s['actual']['hud_fashion'];need(hf['disguise_progress']['completed_mask']==mask and hf['story_complete_seed'],'wrong declared practice fixture')
   cards=[n for n in s['actual']['visible_canvas'] if n['class']=='Button' and '/FashionOutfit_' in n['path']];need(cards,'practice cards absent')
   picks=[any(c['valid'] and c['method']=='_pick' for c in n['pressed_callbacks']) for n in cards]
   need(all(picks) if mask==7 else not any(picks),'practice callback blocker changed')
  hm=native['hud',a];hold=state(hm,'hud_library_after_4seconds')['actual']['hud_fashion'];need(hold['objective_card']['in_tree'] and hold['objective_seen_t']==0,'HUD hold fact changed')
  need(not state(hm,'hud_objective_cleared')['actual']['hud_fashion']['objective_card']['in_tree'],'HUD clear failed')
  for s in hm['states']:
   hf=s['actual']['hud_fashion'];need(all(not hf[k].get('in_tree',False) for k in ['status_tray','pearls','stars','sentence_objective']),'hidden HUD visible')
  need(state(hm,'hud_fade_black_held')['actual']['fade_alpha']==1 and state(hm,'hud_fade_restored')['actual']['fade_alpha']==0,'fade cover facts')
 need(dis['total_inventory_classified_scopes']==9 and dis['unresolved_source_scopes']==360 and dis['new_replacements']==dis['accepted_removals']==0 and dis['actual_all_game_individual_piece_total'] is None,'false closure/count')
 f,b=dis['new_dispositions'];need(f['source_scope_id']=='FVF-C8A0BAF33B80' and f['classification']=='FUNCTIONAL_UNIFORM_BLACK_REBUILD_COVER' and f['art_replacement_count']==0,'wrong functional classification')
 need(b['source_scope_id']=='FVF-8C02E5F13D1D' and b['flat_pending_replacement']==14 and len(b['instances'])==14 and b['repeated_instances_total'] is None,'false repeated art tally')
 for row in obs['bursts']:
  need(len(row['instances'])==14 and [n['source_index'] for n in row['instances']]==list(range(14)),'burst roles missing')
  for i,n in enumerate(row['instances']):
   need(n['class']=='Polygon2D' and n['polygon']=='[(0.0, -14.0), (4.0, -4.0), (14.0, 0.0), (4.0, 4.0), (0.0, 14.0), (-4.0, 4.0), (-14.0, 0.0), (-4.0, -4.0)]','wrong painted/polygon role')
   angle=math.tau*i/14+0.09*(i%2);need(abs(n['rotation']-angle)<0.00001,'wrong repeated role geometry')
  s=state(native['fashion',row['aspect']],row['state']);actual=[n for n in s['actual']['visible_canvas'] if 'WardrobePreviewFeedbackBurst/' in n['path'] and n['class']=='Polygon2D'];need([{k:v for k,v in n.items() if k!='source_index'} for n in row['instances']]==actual and row['image_sha256']==s['image']['sha256'],'burst observations detached')
 for row in obs['practice_callbacks']:
  s=state(native['practice',row['aspect']],row['state']);hf=s['actual']['hud_fashion'];cards=[{'node':n['path'],'callbacks':n['pressed_callbacks']} for n in s['actual']['visible_canvas'] if n['class']=='Button' and '/FashionOutfit_' in n['path']]
  need(row['cards']==cards and row['mask']==hf['disguise_progress'].get('completed_mask') and row['practice']==hf['practice'] and row['image_sha256']==s['image']['sha256'],'practice observation detached')
 for row in obs['hud']:
  s=state(native['hud',row['aspect']],row['state']);hf=s['actual']['hud_fashion'];nodes=[n for n in s['actual']['visible_canvas'] if 'HudPictureTargetCard' in n['path'] or 'HudVoiceCaption' in n['path']]
  need(row['nodes']==nodes and row['seen_t']==hf['objective_seen_t'] and row['card_visible_in_tree']==hf['objective_card'].get('in_tree',False) and row['icon']==hf['objective_texture'].get('texture') and row['image_sha256']==s['image']['sha256'],'HUD observation detached')
 for row in obs['fade']:
  s=state(native['hud',row['aspect']],row['state']);need(row['image_sha256']==s['image']['sha256'] and row['fade_alpha']==s['actual']['fade_alpha'],'fade observation detached')
  actual=[n for n in s['actual']['visible_canvas'] if n['class']=='ColorRect' and n['canvas_layer']==30];need(len(actual)==1 and actual[0]==row['node'],'functional native target detached')
  if row['state']=='hud_fade_black_held':need(row['uniform_opaque_black'] and row['channel_extrema']==[[0,0],[0,0],[0,0],[255,255]],'functional cover not black')
 return True

def validate(stress=False):
 native={(c,a):read_json(HERE/c/a/'capture_manifest.json') for c in CASES for a in ASPECTS};catalog=read_json(HERE/'CATALOG_CONTEXTS.json');dis=read_json(HERE/'SCOPE_DISPOSITIONS.json');obs=read_json(HERE/'EXACT_OBSERVATIONS.json');geometry_guard(native,catalog,dis,obs)
 root=tree_root();sig=next(iter(native.values()))['source_signature'];hashes={}
 for name,digest in sig['files'].items():
  p=Path(name);need(not p.is_absolute() and '..' not in p.parts,'unsafe source name');q=root/p;need(q.is_file() and sha(q.read_bytes())==digest,'runtime source hash '+name);hashes[name]=digest
 for m in native.values():need(m['source_signature']['files']==hashes,'source sets differ');need(m['harness_sha256']==sha((HERE.parent/'capture_hud_fashion.gd').read_bytes()),'executed harness bytes differ')
 briefs=read_json(HERE/'INSTANCE_BRIEFS.json');need(briefs['role_brief_count']==len(briefs['briefs'])==57 and len({b['instance_id'] for b in briefs['briefs']})==57 and all(b['bindings'] for b in briefs['briefs']),'role brief coverage')
 reuse=read_json(HERE/'REUSE_INVENTORY.json');need(reuse['source_count']==len(reuse['native_file_backed_sources'])==49 and reuse['new_art_generations']==reuse['protected_originals_changed']==0,'reuse source count')
 for r in reuse['native_file_backed_sources']:
  q=root/r['path'];need(sha(q.read_bytes())==r['sha256'] and list(Image.open(q).size)==r['dimensions'],'reuse source identity')
 index=read_json(HERE/'NATIVE_INDEX.json');need(index['native_frames']==len(index['records'])==208 and index['new_replacement_pixels']==0,'wrong image total');seen=set()
 for r in index['records']:
  key=(r['case'],r['aspect'],r['state']);need(key not in seen,'duplicate native image');seen.add(key);m=native[r['case'],r['aspect']];s=state(m,r['state']);need(r['sha256']==s['image']['sha256'] and r['bytes']==s['image']['bytes'] and r['dimensions']==m['aspect'],'native index detached');q=safe(r['path']);raw=q.read_bytes();need(sha(raw)==r['sha256'] and len(raw)==r['bytes'],'native bytes changed');im=Image.open(q).convert('RGBA');need(list(im.size)==r['dimensions'],'decoded dimensions');ext=im.getextrema();blank=all(lo==hi for lo,hi in ext)
  need(not blank or r['state']=='hud_fade_black_held','unexpected blank frame')
  if r['state']=='hud_fade_black_held':need(ext==((0,0),(0,0),(0,0),(255,255)),'cover pixels differ')
 launch=read_json(HERE/'diagnostics/native_launch.json');need(len(launch)==6 and all(x['exit_code']==0 and x['parent_normal_save_unchanged_after_exit'] for x in launch),'native driver rejected process')
 for c in CASES:
  for a in ASPECTS:
   log=(HERE/c/a/'native.log').read_text(encoding='utf8');need('SCRIPT ERROR' not in log and not re.search(r'(^|\n)(ERROR|FAIL)',log),'native script error')
 for f in ['SOURCE_PROOFS.json','CALLER_PROOFS.json']:
  d=read_json(HERE/f)
  for row in d.get('sources',d.get('source_files',[])):
   b=safe(row['packet_path']).read_bytes();expected=row.get('git_lf_sha256',row.get('head_lf_sha256'));need(sha(b)==expected,'source proof changed');need(b==source_bytes(root,REV,row['path']),'source no longer revision-bound')
 pre=read_json(HERE.parent/'hud_fashion_preflight.json');expected={(g['person'],g['slot'],iid) for g in pre['current_catalog_pages'] for iid in g['items']};need({(e['person'],e['slot'],e['item_id']) for e in catalog['entries']}==expected,'catalog contexts omit source group')
 boards=read_json(HERE/'BOARDS.json');vr=read_json(HERE/'VISUAL_REVIEW.json');need(boards['total']==len(boards['boards'])==len(vr['boards'])==16,'missing contact review');covered=[]
 for b in boards['boards']:
  q=safe(b['path']);need(sha(q.read_bytes())==b['sha256'] and list(Image.open(q).size)==b['dimensions'],'board identity');need(b['visual_review']=='AGENT_DIAGNOSTIC_CONTACT_SHEET_REVIEWED_NOT_OWNER_ACCEPTED','false/missing board review')
  for x in b['bindings']:need(sha(safe(x['native_path']).read_bytes())==x['sha256'],'board bound image changed');covered.append(x['native_path'])
 need(len(covered)==len(set(covered))==208 and set(covered)=={r['path'] for r in index['records']},'boards fail complete extension coverage')
 cv=read_json(HERE/'CUMULATIVE_COVERAGE.json');sv=read_json(HERE/'CUMULATIVE_SCOPES.json');need(len(cv['entries'])==176 and cv['complete_entries']==0 and sum('PARTIAL' in e['status'] for e in cv['entries'])==cv['partial_entries']==47,'false screen coverage');need(len(sv['scopes'])==369 and sum(s['fully_dispositioned'] for s in sv['scopes'])==sv['fully_resolved']==9,'false scope coverage')
 need(sum('PARTIAL' in s['status'] for s in sv['scopes'])==sv['partial_context_scopes']==39,'false partial scope coverage')
 machine=read_json(HERE/'MACHINE.json');need(machine['cumulative_staged_frames']==962 and machine['DL_QA_11']=='NOT_CLAIMED' and machine['actual_all_game_individual_piece_total'] is None and machine['replacements']==machine['accepted_removals']==0,'false acceptance')
 need(max(p.stat().st_size for p in HERE.rglob('*.json'))<=4*1024*1024,'new JSON oversized')
 negative=[]
 if stress:
  tests=[('ordered state',lambda n,c,d,o:n['hud','1280x720']['states'].reverse()),('save unchanged',lambda n,c,d,o:n['fashion','1280x720']['save_isolation']['after'].update({'': '0'*64})),('source omission',lambda n,c,d,o:n['hud','1280x720']['source_signature']['files'].pop('assets/fashion/slots_v1/catalog.tres')),('wrong aspect',lambda n,c,d,o:n['hud','1280x720'].update({'aspect':[1280,719]})),('catalog target',lambda n,c,d,o:c['entries'][0].update({'item_id':'invented'})),('invented earned phase',lambda n,c,d,o:state(n['practice','1280x720'],'fashion_practice_phase0_after_pointer')['actual']['hud_fashion']['disguise_progress'].update({'completed_mask':1})),('missing burst index',lambda n,c,d,o:o['bursts'][0]['instances'].pop()),('false black cover',lambda n,c,d,o:o['fade'][0].update({'uniform_opaque_black':False})),('false art exemption',lambda n,c,d,o:d['new_dispositions'][1].update({'flat_pending_replacement':0})),('closure inflation',lambda n,c,d,o:d.update({'accepted_removals':1})),('held drag',lambda n,c,d,o:state(n['fashion','1280x720'],'fashion_drag_focus_cancelled')['actual']['hud_fashion'].update({'drag_active':True})),('detached callback observation',lambda n,c,d,o:o['practice_callbacks'][0]['cards'][0].update({'callbacks':[]})),('detached functional target',lambda n,c,d,o:o['fade'][0]['node'].update({'rect':'invented'}))]
  for label,mutate in tests:
   n,c,d,o=copy.deepcopy((native,catalog,dis,obs));mutate(n,c,d,o)
   try:geometry_guard(n,c,d,o)
   except (ValueError,KeyError,StopIteration):negative.append(label)
   else:raise ValueError('falsification escaped: '+label)
 print('HUD_FASHION_INTEGRITY PASS:208 native;6 matrices;79 catalog contexts;57 role briefs;16 reviewed boards;47 partial entries;9 classified scopes;360 unresolved;'+str(len(negative))+' falsifications rejected. Diagnostic only;no runtime/creative acceptance.')
 return {'result':'PASS','native_frames':208,'falsifications_rejected':negative}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--stress',action='store_true');args=ap.parse_args();validate(args.stress)
