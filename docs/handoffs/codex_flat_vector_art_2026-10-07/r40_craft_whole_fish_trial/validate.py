"""Source-only R40 evidence validator. No human/art/QA11 acceptance inferred."""
from pathlib import Path
import json,hashlib,subprocess,math,re,struct
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r39_craft_compositor_context';A=R/'assets_src/flat_vector_craft_fish_20261014';BASE='69dfac241fb2bc3a51bbab138d4ddde952d60899';DEV='831d0bbb155b99d75ef0289cc5cc694e0ef00c1e'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def check(x):
 b=git('show',x['revision']+':'+x['path']) if x.get('revision') else (R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
def eq(a,b):
 if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 if isinstance(a,dict) and isinstance(b,dict):return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
 if isinstance(a,(float,int)) and isinstance(b,(float,int)) and not isinstance(a,bool) and not isinstance(b,bool):return math.isfinite(float(a)) and math.isfinite(float(b)) and abs(float(a)-float(b))<=1e-6
 return type(a)==type(b) and a==b
assert eq([0.920000016689301],[.92]) and not eq([.92],[.922]) and not eq([1],[0]) and not eq(['cat'],['bird']) and not eq([0]*8,[0]*6) and not eq([float('nan')],[0]);assert not eq([True],[1])
index=rd(P/'CAPTURE_INDEX.json');s=index['summary'];assert len(index['captures'])==607 and len(index['functional_data'])==13 and s['current_fixture_native']==386 and s['prior_diagnostic_native']==221;assert sum(x['art_context_credit'] for x in index['captures'])==152 and s['excluded_native']==455 and s['current_bounded']==3649 and s['current_retained']==5032 and s['current_excluded']==1383
for x in index['files']:check(x)
for x in index['captures']:assert list(Image.open(R/x['path']).size)==x['aspect'];assert not x['art_context_credit'] or (x['current_fixture'] and x['whole_fish_drawable'] and x['kind']=='fish')
known_hashes={sha(f.read_bytes()) for f in P.rglob('*.gd')}|{sha(f.read_bytes()) for f in P.rglob('*.gdshader')}
seen=set()
for c in index['cases']:
 d=rd(R/c['manifest']);check({'path':c['manifest'],'bytes':(R/c['manifest']).stat().st_size,'sha256':c['manifest_sha256']});launch=rd(R/c['launch']['path']);result=rd(R/c['result']['path']);assert d['source_revision']==BASE and d['normal_save_before']==d['normal_save_after'] and len(d['normal_save_before'])==8 and not d['actual_child_data'];assert launch['fixture_sha256'] in known_hashes and launch['prototype_sha256'] in known_hashes and launch['shader_sha256'] in known_hashes;assert d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['engine']['status']=='stable' and d['engine']['build']=='official' and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and d['renderer']=='mobile' and d['quality']=='speedy';assert len(d['states'])==c['capture_count']
 if not c['current_fixture']:continue
 assert result['exit_code']==0 and d['errors']==[];seen.add((d['profile_id'],d['aspect'][0]));states={x['id']:x for x in d['states']};kind=d['chosen_kind'];private=rd(next((R/c['manifest']).parent.rglob('reef_save.json')));assert eq(private['custom_fish'],d['saved_fish']) and eq(private['custom_friends'],d['saved_friends']) and private['crafts']==d['saved_unlocks']
 seed=d['synthetic_seed'];assert eq(d['saved_fish'][:len(seed.get('custom_fish',[]))],seed.get('custom_fish',[]));assert eq(d['saved_friends'][:len(seed.get('custom_friends',[]))],seed.get('custom_friends',[]));finish=states['finish_release'];expected=finish['input']['expected_new_gene'];assert eq((d['saved_fish'] if kind=='fish' else d['saved_friends'])[-1],expected)
 if kind=='fish':
  for part in ['body','accent']:
   for i in range(8):assert states[f'{part}_color{i}_selected']['input']['palette_index']==i and states[f'{part}_color{i}_selected']['part']==part
  for geneidx,gene in enumerate(d['saved_fish']):
   st=states['reloaded_stored_fish_gene'+str(geneidx)];assert eq(st['input']['gene'],gene) and st['input']['gene_field_count']==len(gene);assert st['body_rainbow']==(len(gene)>=8 and bool(gene[6])) and st['accent_rainbow']==(len(gene)>=8 and bool(gene[7]))
 else:
  purchase=states['purchased_'+kind+'_ready'];assert purchase['pearls']==23-(5 if kind=='cat' else 8) and private['pearls']==purchase['pearls'] and private['crafts'][kind] is True
 for st in d['states']:
  if st['kind']=='fish' and st['preview_layers']:
   assert len(st['preview_layers'])==1;v=st['preview_layers'][0];assert v['role']=='complete_whole_fish' and v['source_art_layers']==1 and v['functional_selector_only'] is True and v['whole_source']=='res://assets_src/flat_vector_craft_fish_20261014/whole_fish_1024.png' and v['mouse_filter']==2
assert seen=={(p,w) for p in ['fresh_locked','saved_fish','saved_cat','saved_bird'] for w in [1280,1600]}
proof=rd(A/'MASTER_PROOF.json');assert proof['layers']==proof['frames']==1 and proof['native_size']==[1254,1254] and proof['normalized_size']==[1024,1024] and proof['part_separation'] is False and proof['redraw'] is False;assert Image.open(A/'whole_fish_native.png').convert('RGBA').tobytes()==Image.open(A/'native_roundtrip.png').convert('RGBA').tobytes();assert Image.open(A/'whole_fish_1024.png').size==(1024,1024)
for n,size in [('whole_fish_native.aseprite',1254),('whole_fish_1024.aseprite',1024)]:
 b=(A/n).read_bytes();assert struct.unpack_from('<H',b,4)[0]==0xa5e0 and struct.unpack_from('<H',b,6)[0]==1 and struct.unpack_from('<HH',b,8)==(size,size)
g=rd(P/'GENERATION.json');assert g['calls_used']==g['attempt_cap']==1 and g['approved']==g['integrated']==g['accepted_removed']==0;check(g['native_output']);assert sha((P/'PROMPT.txt').read_bytes())==g['prompt_sha256'];assert g['model_revision'] is None and g['seed'] is None and g['provider_request_id'] is None
for x in rd(P/'TECHNICAL_DERIVATION.json')['files']:check(x)
review=rd(P/'REVIEW.json');assert len(review['ten_axes'])==10 and len(review['direct_native_views'])==24 and len(review['prior_direct_native_views'])==11
for x in review['source_references']+review['direct_native_views']+review['prior_direct_native_views']:check(x)
for x in rd(P/'CONTEXT_PREREQUISITE.json')['checks']:check(x)
guard=rd(P/'SIDECAR_GUARD.json');assert guard['before']==guard['after'] and len(guard['before'])==4039
for path,digest in guard['after'].items():assert sha((R/path).read_bytes())==digest,path
assert not git('diff','--name-only',BASE,'--','assets','scripts','scenes','shaders','addons','project.godot').strip()
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);assert new['revision']=='FV-AUDIT-20261014-R40';assert new['craft_compositor_context']==old['craft_compositor_context'];assert new['craft_whole_fish_trial']['accepted_removed']==new['craft_whole_fish_trial']['approved']==new['craft_whole_fish_trial']['integrated']==0
 for key in ['pieces','supplemental_piece_records','entries','observations']:
  if key in old:assert new[key]==old[key],(name,key)
t=rd(P/'tally.json');old=rd(O/'tally.json');assert t['historical_totals'][:-1]==old['historical_totals'] and t['current_context']['exact_capture_count']==3649 and t['current_context']['retained_native_capture_count']==5032 and t['current_context']['excluded_diagnostic_native_count']==1383;assert t['all_game_individual_piece_total'] is None and t['accepted_removed']==t['integrated']==t['runtime_verified']==0;assert t['known_named_design_records_including_supplemental']==227 and t['known_family_count_including_supplemental']==30 and t['current_context']['entries_without_current_slice']==98;assert t['current_context_sample_lanes']['unique_whole_drawing_samples']==2 and t['current_context_sample_lanes']['per_piece_context_review_requests']==5
assert rd(P.parent/'CURRENT.json')['revision']=='FV-AUDIT-20261014-R40'
for p in P.rglob('*.json'):assert p.stat().st_size<4*1024*1024,p
print('R40_SOURCE_NATIVE_CANONICAL_PASS 607retained/152credits/455excluded;13functional;8current;24current11priorviews;4039sidecars;2samples;accepted0;globalunknown')
