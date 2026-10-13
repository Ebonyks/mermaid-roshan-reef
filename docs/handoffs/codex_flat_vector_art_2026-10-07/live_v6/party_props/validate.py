from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from immutable_source import source_bytes
from functools import lru_cache
import argparse,copy,hashlib,json,re,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[4];H='6cde8aeae04aaedcc0b1ff22a05ef93ab9bf666f';HARNESS='e2bc50f3c7fb3110790d1163d19a8421f47fc1bf3f308b499e49ecd53de2534d';ASPECTS=['1280x720','1600x720'];HAT='FVF-75ACAEBD6400';MASKS=['00','01','03','07','0f','1f','3f','7f'];MATRIX=['main_hall_before_ballet','main_hall_after_ballet','main_hall_ready']+['cake_'+kind+'_'+x for kind in ['native','fault'] for x in MASKS]+['candle_'+kind+'_'+lit for kind in ['native','fault'] for lit in ['unlit','lit']]+['table_restored','lawn_ready','lawn_pause_resumed','main_hall_returned']
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def safe(base,n):
 p=(base/n).resolve();assert p.is_relative_to(base.resolve()),'unsafe artifact';return p
@lru_cache(maxsize=None)
def original(n):return source_bytes(R,H,n)
@lru_cache(maxsize=None)
def artifact(n):
 p=safe(P,n);b=p.read_bytes()
 with Image.open(p) as im:im.load();dims=list(im.size)
 return sha(b),len(b),dims
@lru_cache(maxsize=None)
def signature():
 rules=read('native/1280x720/capture_manifest.json')['source_signature']['tree_rules'];paths=['project.godot','tools/audit_opera_capture.py','tools/audit_godot_baseline.py','tools/godot_baseline.json']
 for rule in rules:paths += [p.relative_to(R).as_posix() for p in (R/rule['root']).rglob('*') if p.is_file() and p.suffix in rule['suffixes']]
 paths.sort();files={n:sha(safe(R,n).read_bytes()) for n in paths};return {'algorithm':'sha256_runtime_roots_party_props_v1','files':files,'paths':paths,'missing':[],'tree_rules':rules,'sha256':sha('\n'.join(n+':'+files[n] for n in paths).encode())}
@lru_cache(maxsize=None)
def caller_scan():
 tokens=read('CALLER_PROOFS.json')['tokens'];pattern=re.compile(r'\b(?:'+'|'.join(map(re.escape,tokens))+r')\b');corpus=[];refs=[]
 for n in sorted(subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')):
  p=R/n
  if not p.is_file() or n.startswith(('docs/','audit/','design/','assets_src/','disabled_addons/')) or p.suffix not in {'.gd','.tscn','.tres','.godot','.gdshader'}:continue
  b=p.read_bytes();corpus.append({'path':n,'working_sha256':sha(b),'bytes':len(b)})
  for i,l in enumerate(b.decode('utf-8-sig').splitlines(),1):
   found=sorted(set(pattern.findall(l)))
   if found:refs.append({'path':n,'line':i,'tokens':found,'text':l,'lane':'HISTORICAL_BACKUP_REFERENCE' if n.startswith('backups/') else ('TEST_PROBE' if '/probe' in '/'+n else 'PRODUCTION_SOURCE')})
 return corpus,refs

def nums(s):return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',s)]
def check(overrides=None):
 overrides=overrides or {}
 def get(n):return copy.deepcopy(overrides[n]) if n in overrides else read(n)
 m=get('MACHINE.json');expected={'source_revision':H,'engine':'4.7.2.stable.official.ed1daf0bf','renderer':'mobile','quality':'speedy','aspects':ASPECTS,'native_processes':2,'new_native_frames':54,'boards':4,'cumulative_staged_frames':1488,'R6_total_staged_new_frames':884,'partial_entries':68,'complete_entries':0,'classified_scopes':13,'unresolved_scopes':356,'new_scope_classifications':1,'new_counted_flat_roles':35,'hat_roles':33,'cumulative_flat_named_role_contexts':164,'all_game_individual_piece_total':None,'source_fingerprint_files':6444,'source_fingerprint_algorithm':'sha256_runtime_roots_party_props_v1','normal_child_saves_unchanged':True,'production_unchanged':True,'replacements':0,'accepted_removals':0,'DL_QA_11':False,'visual_device_child_owner_acceptance':False,'publication':'UNPUBLISHED_HANDOFF_BLOCKED'}
 for k,v in expected.items():assert m[k]==v,(k,'claim drift')
 assert get('EXPECTED_MATRIX.json')=={'party_props':MATRIX};assert sha((P.parent/'capture_party_props.gd').read_bytes())==HARNESS
 sp=get('SOURCE_PROOFS.json');assert sp['revision']==H and len(sp['sources'])==20 and len({x['path'] for x in sp['sources']})==20;txt={}
 for x in sp['sources']:
  b=original(x['path']);assert x['revision']==H and sha(b)==x['git_lf_sha256'] and safe(P,x['packet_path']).read_bytes()==b
  c=safe(R,x['path']).read_bytes();assert sha(c)==x['working_tree_sha256'] and c.replace(b'\r\n',b'\n')==b;txt[x['path']]=b.decode('utf-8-sig')
 scan=get('CALLER_PROOFS.json');corpus,refs=caller_scan();assert scan['corpus']==corpus and scan['references']==refs and scan['corpus_count']==349==len(corpus) and len(refs)==107 and len(scan['tokens'])==19
 code=txt['scripts/chapter_two_lawn_finale_2d.gd'];assert 'Vector2(-22, 8), Vector2(0, -38), Vector2(22, 8)' in code and 'edge.width = 3.0' in code and 'stripe.width = 5.0' in code and code.count('_add_hat(rumi,')==1
 table=txt['scripts/chapter_two_party_table_2d.gd'];assert table.count('_build_ember_visitor_stage(')==1 and 'table_glow.size = Vector2(710.0, 238.0)' in table
 factory=table[table.index('func _build_ember_visitor_stage'):table.index('func _add_polygon')];assert factory.count('_add_polygon(')==11 and factory.count('_add_eye(')==4 and factory.count('Line2D.new()')==1
 cake=txt['scripts/chapter_two_giant_cake_2d.gd'];assert 'for index in range(32):' in cake and 'Vector2(166.0, 11.0)' in cake
 ob=get('ROUTE_OBSERVATIONS.json');assert ob['retained_visitor_factory']['ordinary_setup_calls']==0 and len(ob['retained_visitor_factory']['literal_references'])==1 and not ob['native_pending'] and not ob['acceptance']
 assert len(signature()['paths'])==6444 and signature()['sha256']=='0a2525e88036b450309f8434a232d9a34d91a8dcf0dbfa84fcaa8d5055527d3b'
 launch=get('CAPTURE_LAUNCH.json');assert len(launch)==2 and {x['aspect'] for x in launch}==set(ASPECTS)
 captures=get('CAPTURES.json');frames=captures['frames'];assert captures['count']==len(frames)==54 and len({(x['aspect'],x['state']) for x in frames})==54;by={(x['aspect'],x['state']):x for x in frames}
 eo=get('EXACT_OBSERVATIONS.json');assert eo['finite_hat_count']==11 and eo['finite_hat_draw_layers']==33 and not eo['normal_table_old_visitors_present'] and not eo['component_faults_are_natural_routes']
 for a in ASPECTS:
  rec=next(x for x in launch if x['aspect']==a);assert rec['exit_code']==0 and rec['parent_normal_save_unchanged_after_exit'] and rec['harness_sha256']==HARNESS and rec['source_revision']==H
  raw=get('native/'+a+'/capture_manifest.json');assert raw['result']=='PASS' and raw['failures']==0 and raw['source_revision']==H and raw['harness_sha256']==HARNESS and raw['renderer']=='mobile' and raw['quality']=='speedy' and raw['display_server']=='Windows'
  assert raw['engine']['major']==4 and raw['engine']['minor']==7 and raw['engine']['patch']==2 and raw['engine']['build']=='official' and raw['engine']['status']=='stable'
  assert raw['expected_ids']==MATRIX and [x['id'] for x in raw['states']]==MATRIX and all(x['pass'] for x in raw['checks'])
  assert raw['source_unchanged'] and raw['source_signature']==signature();save=raw['save_isolation'];assert save['unchanged'] and save['before']==save['after'] and len(save['before'])==8
  rows={x['id']:x for x in raw['states']};assert not rows['main_hall_before_ballet']['actual']['table']['exists'] and rows['main_hall_after_ballet']['actual']['table']['exists']
  for x in raw['states']:
   assert x['status']=='PASS';f=by[(a,x['id'])];digest,size,dims=artifact(f['path']);assert digest==f['sha256']==x['image']['sha256'] and size==x['image']['bytes'] and dims==f['dimensions']==raw['aspect'] and f['sequence']==x['sequence'] and f['fixture_method']==x['actual']['fixture_method']
   actual=x['actual'];assert actual['chapter_active'] and actual['party_mask'] in [1097,1101,11343]
   if actual['table']['exists']:assert not any(actual['table'][k] for k in ['king_exists','scout_exists','prince_exists','north_arrow_exists'])
   if x['id'].startswith('cake_'):
    assert 'SOURCE_PROP_API' in actual['fixture_method'] and actual['fixture_cake_mask']==int(x['id'][-2:],16) and actual['story_cake_mask']==127
    if 'fault' in x['id']:assert actual['table']['cake']['draw_guard']=='VECTOR_PROP_FALLBACK' and 'RESOURCE_FAILURE' in actual['fixture_method']
   if x['id'].startswith('candle_'):
    assert 'SOURCE_CANDLE' in actual['fixture_method'] and not actual['candle_lit'] and actual['table']['candle']['lit']==x['id'].endswith('_lit')
    assert actual['table']['candle']['draw_guard']==('VECTOR_CANDLE_FALLBACK' if 'fault' in x['id'] else 'PAINTED_SPRITES_SUPPRESS_VECTOR')
  for id in ['lawn_ready','lawn_pause_resumed']:
   actual=rows[id]['actual'];hats=actual['hats'];assert len(hats)==11 and len({h['path'] for h in hats})==11 and actual['game']=='chapter2_lawn' and actual['lawn_beat']==0 and not actual['hud_visible'] and actual['source_normal_navigation']
   expected_hats=[('Guest_wacky_chuck',[59,10],1,0),('Guest_two_friends',[26,37],.65,1),('Guest_two_friends',[56,30],.8,2),('Guest_pearl_friend',[89,27],.8,2),('Guest_mama_baby',[44,26],1,3),('Guest_mama_baby',[81,63],.55,0),('Guest_kareem',[59,10],1,0),('Guest_huluu',[59,10],1,1),('Guest_flower_friend',[59,10],1,2),('Guest_daddy',[59,-8],1,3),('Rumi',[50,20],.65,2)]
   palette=[[244/255,183/255,214/255,1],[247/255,215/255,122/255,1],[155/255,222/255,212/255,1],[197/255,166/255,241/255,1]]
   for hat,(parent,point,scale,color) in zip(hats,expected_hats):
    assert '/'+parent+'/' in hat['path'] and nums(hat['position'])==point and all(abs(v-scale)<1e-5 for v in nums(hat['scale']))
    assert all(abs(a-b)<.001 for a,b in zip(nums(hat['color']),palette[color]))
    assert all(abs(a-b)<.001 for a,b in zip(nums(hat['lines'][0]['color']),[73/255,55/255,95/255,1])) and all(abs(a-b)<.001 for a,b in zip(nums(hat['lines'][1]['color']),[1,242/255,200/255,1]))
    assert hat['visible'] and nums(hat['points'])==[-22,8,0,-38,22,8] and len(hat['lines'])==2
    assert nums(hat['lines'][0]['points'])==[-22,8,0,-38,22,8,-22,8] and hat['lines'][0]['width']==3
    assert nums(hat['lines'][1]['points'])==[-12,-12,12,-12] and hat['lines'][1]['width']==5
   if id=='lawn_ready':assert eo['hats_by_aspect'][a]==hats
  assert rows['main_hall_returned']['actual']['game']=='level2' and not rows['main_hall_returned']['actual']['lawn_exists']
 boards=get('BOARDS.json')['boards'];assert len(boards)==4;covered=[]
 for b in boards:
  digest,_,dims=artifact(b['path']);assert digest==b['sha256'] and dims==b['dimensions']
  for c in b['cells']:
   f=by[(b['aspect'],c['state'])];assert c['source']==f['path'] and c['source_sha256']==f['sha256'] and c['source_dimensions']==f['dimensions'];covered.append((b['aspect'],c['state']))
 assert sorted(covered)==sorted(by)
 vr=get('VISUAL_REVIEW.json');assert {(x['path'],x['sha256']) for x in vr['boards']}=={(x['path'],x['sha256']) for x in boards} and len(vr['native_spots'])==6 and not vr['device_child_owner_review'] and all(not x['replacement_or_acceptance'] for x in vr['boards'])
 for x in vr['native_spots']:assert artifact(x['path'])[0]==x['sha256'] and not x['acceptance']
 roles=get('INSTANCE_BRIEFS.json');assert len(roles['roles'])==48 and len({x['id'] for x in roles['roles']})==48 and roles['counted_flat_roles']==35 and roles['unique_all_game_total'] is None
 counted=[x for x in roles['roles'] if x['counted_in_named_flat_role_contexts']];assert len(counted)==35 and sum(x['source_scope']==HAT for x in counted)==33
 for x in roles['roles']:
  assert x['unique_design_count'] is None and not x['acceptance']
  if x['counted_in_named_flat_role_contexts']:assert x['status']=='FLAT_VISIBLE_ART_REQUIRES_PAINTED_REPLACEMENT' and x['named_context_instance_count']==1 and x['bindings']
  for b in x['bindings']:assert b['native_path']==by[(b['aspect'],b['state'])]['path'] and b['native_sha256']==by[(b['aspect'],b['state'])]['sha256']
 scopes=get('SCOPE_ROUTE_REVIEW.json');assert len(scopes['scopes'])==14 and [x['scope_id'] for x in scopes['scopes'] if x['fully_dispositioned_for_inventory']]==[HAT]
 cv=get('CUMULATIVE_COVERAGE.json');old=read('../promenade/CUMULATIVE_COVERAGE.json');assert [x['id'] for x in cv['entries']]==[x['id'] for x in old['entries']] and len(cv['entries'])==176 and cv['partial_entries']==68 and cv['complete_entries']==0
 for x,y in zip(cv['entries'],old['entries']):
  if x['id'] not in ['game.chapter2_party','game.chapter2_lawn']:assert x==y
  else:assert x['status'].startswith('PARTIAL') and not x['route_or_saved_variants_complete']
 assert sum(x['status'].startswith('PARTIAL') for x in cv['entries'])==68
 cs=get('CUMULATIVE_SCOPES.json');prior=read('../promenade/CUMULATIVE_SCOPES.json');assert len(cs['scopes'])==369 and [x['scope_id'] for x in cs['scopes']]==[x['scope_id'] for x in prior['scopes']] and cs['fully_resolved']==13
 for x,y in zip(cs['scopes'],prior['scopes']):
  if x['scope_id']!=HAT:assert x['fully_dispositioned']==y['fully_dispositioned']
  else:assert x['fully_dispositioned'] and x['instance_count']==33 and x['individual_piece_count'] is None
 inv=get('SOURCE_ASSET_INVENTORY.json');assert len(inv['sources'])==15 and inv['manual_source_inspected_count']==5==sum(x['manual_source_inspected'] for x in inv['sources']) and not inv['complete_replacement_accepted'] and inv['new_generation_calls']==0
 for x in inv['sources']:
  b=safe(R,x['path']).read_bytes();assert sha(b)==x['sha256'] and not x['modified'] and x['license_rows']
  with Image.open(safe(R,x['path'])) as im:assert list(im.size)==x['dimensions'] and im.mode==x['mode']
 print('PARTY_PROPS|PASS|54 native/4 boards/20 sources/349 corpus/107 refs/11 hats/35 counted roles;1488/68 partial/13 classified;no acceptance')

def stress():
 trials=[]
 def add(label,n,fn):
  j=read(n);fn(j);trials.append((label,{n:j}))
 for k,v in [('all_game_individual_piece_total',164),('accepted_removals',35),('DL_QA_11',True),('visual_device_child_owner_acceptance',True),('publication','DELIVERED'),('partial_entries',176),('new_scope_classifications',14)]:add('false_'+k,'MACHINE.json',lambda j,k=k,v=v:j.__setitem__(k,v))
 add('source_hash','SOURCE_PROOFS.json',lambda j:j['sources'][0].__setitem__('git_lf_sha256','0'*64))
 add('caller_omission','CALLER_PROOFS.json',lambda j:j['references'].pop())
 add('dormant_as_current','ROUTE_OBSERVATIONS.json',lambda j:j['retained_visitor_factory'].__setitem__('ordinary_setup_calls',1))
 add('missing_duplicate_hat','native/1280x720/capture_manifest.json',lambda j:next(x for x in j['states'] if x['id']=='lawn_ready')['actual']['hats'].pop())
 add('hat_geometry','native/1280x720/capture_manifest.json',lambda j:next(x for x in j['states'] if x['id']=='lawn_ready')['actual']['hats'][0].__setitem__('points','[(0,0)]'))
 add('hat_color','native/1280x720/capture_manifest.json',lambda j:next(x for x in j['states'] if x['id']=='lawn_ready')['actual']['hats'][0].__setitem__('color','(0,0,0,1)'))
 add('hat_attachment','native/1280x720/capture_manifest.json',lambda j:next(x for x in j['states'] if x['id']=='lawn_ready')['actual']['hats'][0].__setitem__('position','(0,0)'))
 add('fault_as_natural','native/1280x720/capture_manifest.json',lambda j:next(x for x in j['states'] if x['id']=='cake_fault_7f')['actual'].__setitem__('fixture_method','NATURAL_GAMEPLAY'))
 add('save_mutation','native/1280x720/capture_manifest.json',lambda j:j['save_isolation']['after'].__setitem__('','0'*64))
 add('signature_omission','native/1280x720/capture_manifest.json',lambda j:j['source_signature']['files'].pop('scripts/arena/sky_lagoon_layout.json'))
 add('artifact_path_escape','CAPTURES.json',lambda j:j['frames'][0].__setitem__('path','../../escape.png'))
 add('native_hash','CAPTURES.json',lambda j:j['frames'][0].__setitem__('sha256','0'*64))
 add('board_missing_cell','BOARDS.json',lambda j:j['boards'][0]['cells'].pop())
 add('review_absent','VISUAL_REVIEW.json',lambda j:j['boards'].pop())
 add('role_exemption','INSTANCE_BRIEFS.json',lambda j:j['roles'][0].__setitem__('status','FUNCTIONAL_INVISIBLE'))
 add('scope_inflation','SCOPE_ROUTE_REVIEW.json',lambda j:j['scopes'][0].__setitem__('fully_dispositioned_for_inventory',True))
 add('coverage_duplicate','CUMULATIVE_COVERAGE.json',lambda j:j['entries'].append(j['entries'][0]))
 add('reuse_accepted','SOURCE_ASSET_INVENTORY.json',lambda j:j.__setitem__('complete_replacement_accepted',True))
 for label,override in trials:
  try:check(override)
  except (AssertionError,KeyError,ValueError,FileNotFoundError):print('PARTY_PROPS|PASS|reject '+label)
  else:raise AssertionError('accepted falsification '+label)
 print('PARTY_PROPS|PASS|'+str(len(trials))+' integrity falsifications rejected')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--stress',action='store_true');args=parser.parse_args();check()
 if args.stress:stress()
