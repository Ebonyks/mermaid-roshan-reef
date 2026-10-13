"""Exact independent picture evidence, rejected context and stable-count verification."""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2];D=P/'root_picture_review_20261012'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def require(ok,msg):
 if not ok:raise ValueError(msg)
def guard(q,c,t,p):
 require(len(q['captures'])==52 and len({x['path'] for x in q['captures']})==52,'capture cardinality')
 require(sum(x['run_role']=='rejected_fresh' for x in q['captures'])==8,'rejected diagnostics retained')
 require(q['capture_counts']['actually_independently_viewed_unique']==24 and len(set(q['reviewed_capture_paths']))==24,'personally viewed count')
 require(len(q['observations'])==17 and len(set(q['piece_ids_bound']))==15,'observation/design count')
 require(set(q['piece_ids_bound']).issubset({x['id'] for x in p['pieces']}),'stable named IDs')
 require(all(o['accepted_removals']==o['runtime_integrations']==o['replacement_pixels']==0 for o in q['observations']),'no inferred implementation/acceptance')
 require(q['evidence_lanes']['device']==q['evidence_lanes']['child']==q['evidence_lanes']['owner']=='PENDING','separate acceptance lanes')
 require(t['all_game_individual_piece_total'] is None and t['accepted_removed']==0,'unknown all-game total/no removal')
 require(t['current_context']['exact_capture_count']==1584 and t['current_context']['new_R6_capture_count']==980 and t['current_context']['rejected_boot_capture_count']==8,'bounded/retained units')
 entries=[e for e in c['entries'] if e['id'] in ['picture.'+k for k in ['garden','snowman','trampoline','xmas']]+['game.pic_'+k for k in ['garden','snowman','trampoline','xmas']]]
 require(len(entries)==8 and all('PARTIAL' in e['status'] and not e['route_or_saved_variants_complete'] for e in entries),'partial route aliases')
 require(all(x['run_role']!='rejected_fresh' for e in entries for x in e['captures']),'rejected boot cannot be clean context')
 require(t['current_context']['counted_flat_role_contexts']==164,'no unique design/caller inflation')
def check():
 q=read('root_picture_review_20261012/review.json');c=read('scene_coverage.json');t=read('tally.json');p=read('per_piece.json');guard(q,c,t,p)
 m=read('root_picture_review_20261012/manifest.json')
 require(sha((D/'review.json').read_bytes())=='5eb465c1e48be3f665100a526ec05fa8620afd078bd4f462cf2b69c5c8ec78dc','immutable independent review')
 require(sha((D/'manifest.json').read_bytes())=='566b99282a9f2932a2b6dee92277895e7edce6a08cd19e8518394dabab4bcce3','immutable independent manifest')
 for x in m['files']:
  b=(D/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'independent payload byte '+x['path'])
 require(sha(''.join(x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in sorted(m['files'],key=lambda x:x['path'])).encode())==m['packet_payload_sha256'],'independent sorted payload')
 for x in q['captures']:
  require(sha((D/x['path']).read_bytes())==x['sha256'],'native binding')
  with Image.open(D/x['path']) as im:require(list(im.size)==[int(a) for a in x['aspect'].split('x')],'native dimensions')
 dispositions=read('ROOT_PICTURE_SCOPE_DISPOSITIONS_20261012.json')
 require(sha((P/'ROOT_PICTURE_SCOPE_DISPOSITIONS_20261012.json').read_bytes())=='2aff4d2a5b16bea838386e226f9e1bd16e9e951301004d2fe094fadfdcba548a','exact independent source dispositions')
 for x in dispositions['new_dispositions']:
  b=subprocess.check_output(['git','show',x['source_revision']+':'+x['source']['path']],cwd=R,stderr=subprocess.PIPE);require(sha(b.replace(b'\r\n',b'\n'))==x['source_sha256_lf_current'] and x['accepted_removals']==0,'source disposition exact bytes/no removal')
 proof=read('PICTURE_IMPORT_PREFLIGHT.json')['license_snapshot'];parts=[]
 for x in proof['parts']:
  b=(P/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'literal license part');parts.append(b)
 require(len(b''.join(parts))==proof['bytes'] and sha(b''.join(parts))==proof['recorded_worktree_sha256'],'exact working license snapshot')
 for x in q['source_files']:
  b=subprocess.check_output(['git','show',q['source_revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE)
  require(sha(b.replace(b'\r\n',b'\n'))==(proof['historical_git_sha256'] if x['path']=='ASSET_LICENSES.md' else x['lf_text_sha256']),'immutable source binding')
 for role in read('PICTURE_CONTEXT_RECONCILIATION.json')['supplementary_roles']:
  b=subprocess.check_output(['git','show',role['source_revision']+':'+role['source_path']],cwd=R,stderr=subprocess.PIPE)
  require(sha(b)==role['git_export_sha256'] and not role['counted_as_new_unique_design'] and not role['scope_disposition_complete'],'supplemental role scope')
 for x in q['reuse_inventory']:
  if 'runtime' in x:
   a=subprocess.check_output(['git','show',q['source_revision']+':'+x['runtime']],cwd=R,stderr=subprocess.PIPE);b=subprocess.check_output(['git','show',q['source_revision']+':'+x['alternate']],cwd=R,stderr=subprocess.PIPE);require(a==b and sha(a)==x['runtime_sha256']==x['alternate_sha256'],'alternate duplicate exact bytes')
  else:require(sha(subprocess.check_output(['git','show',q['source_revision']+':'+x['source']],cwd=R,stderr=subprocess.PIPE))==x['sha256'],'reuse source hash')
 print('PICTURE|ALL OK|52retained/44bounded/8rejected;24viewed;17observations/15IDs;76partial/0complete;0removed')
def stress():
 base=[read(n) for n in ['root_picture_review_20261012/review.json','scene_coverage.json','tally.json','per_piece.json']]
 controls=[('fake_approval',0,lambda q:q['evidence_lanes'].update(owner='ACCEPTED')),('fake_observation_removal',0,lambda q:q['observations'][0].update(accepted_removals=1)),('invent_view',0,lambda q:q['capture_counts'].update(actually_independently_viewed_unique=52)),('invent_design',0,lambda q:q['piece_ids_bound'].append('UNKNOWN')),('reject_as_ready',1,lambda c:next(e for e in c['entries'] if e['id']=='picture.garden')['captures'][0].update(run_role='rejected_fresh')),('fake_bounded_count',2,lambda t:t['current_context'].update(exact_capture_count=1540)),('fake_total',2,lambda t:t.update(all_game_individual_piece_total=224)),('fake_role_count',2,lambda t:t['current_context'].update(counted_flat_role_contexts=167))]
 for name,i,fn in controls:
  a=copy.deepcopy(base);fn(a[i]);caught=False
  try:guard(*a)
  except ValueError:caught=True
  require(caught,'missed falsification '+name)
 print('PICTURE|STRESS|8/8false-count/acceptance/clean-context claims rejected')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--stress',action='store_true');args=a.parse_args();check()
 if args.stress:stress()
