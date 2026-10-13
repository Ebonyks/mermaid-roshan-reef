"""Verify R6 count units, immutable historical routing and exact independent review bindings."""
from pathlib import Path
import copy,json,hashlib,argparse,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2];OLD='92c9fe70319ef46bfaa8f61348a6f51512141ec3'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def guard(tally,pieces,coverage,review):
 require(tally['all_game_individual_piece_total'] is None,'unknown denominator required')
 require(all(tally[k]==0 for k in ['replaced','integrated','runtime_verified','accepted_removed']),'no acceptance')
 require(tally['remaining_source_scopes_to_disposition']==351,'scope count')
 require(len(pieces['pieces'])==224 and len({x['id'] for x in pieces['pieces']})==224,'stable design register')
 ids={x['id'] for x in pieces['pieces']};reviewed={sid for o in review['observations'] for sid in o['piece_ids']}
 require(reviewed.issubset(ids) and len(reviewed)==30,'independent review IDs')
 require(len(review['observations'])==20 and len(review['capture_bindings'])==20,'independent review count')
 require(len(coverage['entries'])==176 and len({x['id'] for x in coverage['entries']})==176,'route IDs')
 require(sum('PARTIAL' in x['status'] for x in coverage['entries'])==76,'partial entries')
 require(coverage['complete_entries']==0 and not any(x.get('route_or_saved_variants_complete') for x in coverage['entries']),'no complete coverage')
 require(tally['current_context']['counted_flat_role_contexts']==164,'role count')
 require(review['acceptance']['accepted_removed']==0 and review['acceptance']['owner'] is None,'no inherited acceptance')
def check():
 t=read('tally.json');p=read('per_piece.json');c=read('scene_coverage.json');review=read('ROOT_CONTEXT_REVIEW_20261012.json');guard(t,p,c,review)
 for b in review['capture_bindings']:
  f=R/b['path']
  if not f.exists():f=P/'live_v6/prior_native'/Path(b['path']).relative_to(P.relative_to(R))
  raw=f.read_bytes();require(sha(raw)==b['sha256'] and len(raw)==b['bytes'],'review image binding')
  with Image.open(f) as im:require(list(im.size)==b['dimensions'],'review image dimensions')
 for b in review['source_bindings']:
  raw=(R/b['path']).read_bytes();require(b['sha256'] in [sha(raw),sha(raw.replace(b'\r\n',b'\n'))] and not b['modified'],'review source binding')
 scopes=read('CURRENT_SCOPE_CONTEXT_OVERLAY.json');require(len(scopes['scopes'])==369 and sum(x['fully_dispositioned'] for x in scopes['scopes'])==18,'scope inventory')
 require(not (P/'live_v5').exists(),'R5 stays only on immutable archive branch')
 require(not subprocess.check_output(['git','diff',OLD,'--','scripts','scenes','assets','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE),'runtime source changed')
 print('PACKET|ALL OK|224named designs;164overlapping flat roles;76partial/0complete;351unresolved;20review observations;0removals')
def stress():
 base=[read(n) for n in ['tally.json','per_piece.json','scene_coverage.json','ROOT_CONTEXT_REVIEW_20261012.json']];controls=[]
 for name,index,mutate in [('fake_denominator',0,lambda x:x.update(all_game_individual_piece_total=224)),('fake_removal',0,lambda x:x.update(accepted_removed=1)),('duplicate_design',1,lambda x:x['pieces'].append(x['pieces'][0])),('scope_inflation',0,lambda x:x.update(remaining_source_scopes_to_disposition=0)),('complete_screen',2,lambda x:x.update(complete_entries=1)),('foreign_review_id',3,lambda x:x['observations'][0]['piece_ids'].append('UNKNOWN')),('owner_acceptance',3,lambda x:x['acceptance'].update(owner='ACCEPTED'))]:
  a=copy.deepcopy(base);mutate(a[index]);caught=False
  try:guard(*a)
  except ValueError:caught=True
  require(caught,'missed falsification '+name);controls.append(name)
 print('PACKET|STRESS|7/7rejected',controls)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--stress',action='store_true');args=a.parse_args();check()
 if args.stress:stress()
