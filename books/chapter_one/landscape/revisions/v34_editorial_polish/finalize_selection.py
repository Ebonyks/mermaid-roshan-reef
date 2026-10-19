"""Keep only seamless reviewed candidates in the manuscript; preserve every reject."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2]
def read(p):return json.loads(p.read_text('utf8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
b=read(L/'book.json');P={q['page']:q for q in b['pages']};e=read(V/'generation_evidence.json')
for q in read(V/'final_selection_outputs.json'):
 p=V/'art'/f"{q['id']}_attempt{q['attempt']}.png";shutil.copy2(Path('C:/Users/Peter/.codex/generated_images/01a0bd6a-0b70-7682-bd4c-44a20e6eed2d')/q['filename'],p)
 q.update(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),native_size=list(Image.open(p).size))
 if not any(x['id']==q['id'] and x['attempt']==q['attempt'] for x in e['native_attempts']):e['native_attempts'].append(q)
 key='v34_closed_door' if q['id']=='door_cutout_repair' else 'v34_quiet_bank'
 b['sources'][key]=dict(file=p.relative_to(L).as_posix(),sha256=q['sha256'],native_size=q['native_size'],provenance_record='revisions/v34_editorial_polish/generation_evidence.json')
P[3].pop('local_patches',None)
for n,id in [(11,'rubbish_bank'),(21,'tidy_art_bank'),(23,'quiet_bank'),(24,'care_bank24')]:
 P[n]['integrated_background']='v34_'+id;P[n].pop('background_patches',None)
P[23].pop('local_patches',None)
P[25]['background_patches']=P[25]['background_patches'][:1]
P[23]['integrated_prop_bounds']=[[.112,.867,.055,.065],[.817,.892,.067,.05],[.837,.869,.028,.038]]
P[10]['local_patches']=[q for q in P[10]['local_patches'] if q['source']!='v34_dirty_pool_floor'];P[10]['caption']['halo']=True
P[15]['local_patches']=[q for q in P[15].get('local_patches',[]) if q['source']!='v34_clean_pool_floor']
for k in ['v34_entry_dust','v34_dirty_pool_floor','v34_clean_pool_floor']:b['sources'].pop(k,None)
for p in P.values():
 if p['caption']['color']=='white':p['caption']['outline']=1
b['back_cover']['caption']['outline']=1
save(L/'book.json',b);save(V/'BOOK_CURRENT.json',b)
active={q['file'] for q in b['sources'].values()}
used=set()
for p in P.values():
 used.update(p['art']);used.add(p.get('integrated_background',''))
 for q in p.get('placements',[]):used.add(q['source'])
 for q in p.get('background_patches',[])+p.get('local_patches',[]):used.add(q['source'])
 if p.get('top_extension'):used.add(p['top_extension']['source'])
used_files={(L/b['sources'][k]['file']).resolve() for k in used if k in b['sources']}
for q in e['native_attempts']:
 q['selection']='DELIVERED' if (R/q['path']).resolve() in used_files else 'NOT_DELIVERED'
 if q['id'] in ['entry_dust','dirty_pool_floor','clean_pool_floor']:q['rejection']='Visible joins in composed proof; original scene retained.'
 elif q['id']=='door_cutout':q['rejection']='Changed hardware; repaired derivative replaces it.'
 elif q['selection']=='NOT_DELIVERED':q['rejection']=q.get('status','Superseded by corrected scale/identity.')
e['count']=len(e['native_attempts']);e['method']='24 built-in candidates;12 selected derivatives. Full new stationery sheets are authorized background variants, not narrative-scene redraws. Scene repairs expose only declared polygons or the empty arrival header. Whole objects/figures are source-bound RGBA isolations/restoration. All originals and rejects preserved.'
save(V/'generation_evidence.json',e)
stale=V/'complete/page_34.png'
if stale.exists():
 assert stale.resolve().is_relative_to(V.resolve());stale.unlink()
print('Final selection: no Grand Puff marginal art, no scene/floor patch seams, source-bound alpha door.')
