"""Verify independent action diagnostics without inflating artwork or acceptance counts."""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2];D=P/'root_picture_actions_review_20261012'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def require(ok,msg):
 if not ok:raise ValueError(msg)
def guard(q,t,a,p):
 require(len(q['captures'])==146 and len({x['path'] for x in q['captures']})==146,'capture cardinality')
 require(sum(x['run_returncode']==0 for x in q['captures'])==52,'successful fixture count')
 require(sum(x['run_returncode']!=0 for x in q['captures'])==94,'failed diagnostic count')
 require(set(x['run_role'] for x in q['captures'] if x['run_returncode']==0)=={'bounded_snow','completed_snow_fixture'},'failed runs cannot become green fixtures')
 require(len(set(q['reviewed_capture_paths']))==q['independently_viewed_unique_native_count']==12,'independent views')
 require(len(q['observations'])==8 and all(x['accepted_removals']==0 for x in q['observations']),'observations/no acceptance')
 ids={sid for x in q['observations'] for sid in x['existing_piece_ids']}
 require(len(ids)==6 and ids.issubset({x['id'] for x in p['pieces']}),'stable design IDs')
 require(all(q['evidence_lanes'][k]=='PENDING' for k in ['device','child','owner']),'acceptance lanes')
 require(a['new_scope_classification_count']==0 and a['new_route_partial_count']==0,'scope/route deduplication')
 require(a['combined_named_records_with_partial_review']==44,'combined partial review count')
 require(t['all_game_individual_piece_total'] is None and all(t[k]==0 for k in ['replaced','integrated','runtime_verified','accepted_removed']),'unknown denominator/no removal')
 require(t['current_context']['exact_capture_count']==1584 and t['current_context']['new_R6_capture_count']==980 and t['current_context']['retained_native_capture_count']==1686 and t['current_context']['failed_run_capture_count']==94,'capture units')
 require(t['current_context']['fully_dispositioned_scopes']==18 and t['remaining_source_scopes_to_disposition']==351,'no duplicated scope closure')
def check():
 q=read('root_picture_actions_review_20261012/review.json');t=read('tally.json');a=read('ACTION_CONTEXT_RECONCILIATION.json');p=read('per_piece.json');guard(q,t,a,p)
 require(sha((D/'review.json').read_bytes())=='54b167f9b14b4de7e79ca570a30828fcf48d394d54937376e7468461dd9399f1','exact independent review')
 require(sha((D/'manifest.json').read_bytes())=='b59675c94e0f0e51d5ae9aa61a92a0072e912427bff454e75b5f78963a617570','exact independent manifest')
 m=read('root_picture_actions_review_20261012/manifest.json');require(len(m['files'])==194,'payload count')
 for x in m['files']:
  b=(D/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'exact diagnostic payload '+x['path'])
 require(sha(''.join(x['path']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\n' for x in sorted(m['files'],key=lambda x:x['path'])).encode())==m['packet_payload_sha256']=='b81a6159eb8b3b924f4e1d9c6363072027b9a4261fb09976cbaf36732fe8fb8f','payload hash')
 for x in q['captures']:
  require(sha((D/x['path']).read_bytes())==x['sha256'],'capture hash')
  with Image.open(D/x['path']) as im:require(list(im.size)==[int(v) for v in x['aspect'].split('x')],'capture dimensions')
 for x in q['reuse_inventory']:
  b=subprocess.check_output(['git','show',q['source_revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);require(sha(b)==x['sha256'] and x['modifications']=='NONE','reuse source')
 require((D/'source_scope_dispositions.json').read_bytes()==(P/'ROOT_PICTURE_SCOPE_DISPOSITIONS_20261012.json').read_bytes(),'exact duplicated scope evidence')
 receipts=list((D/'receipts').glob('*receipt.json'));require(len(receipts)==7,'execution history')
 for f in receipts:
  j=json.loads(f.read_text());require(j['changed_runtime_sources']==[] and j['runtime_source_file_count']==6452,'unchanged source proof')
  script=Path(j['command'][-1].replace('\\','/')).name;require(sha((D/'harnesses'/script).read_bytes())==j['harness_sha256'],'executed harness binding')
 for f in D.rglob('*source_before.json'):
  before=json.loads(f.read_text());receipt=json.loads(f.with_name(f.name.replace('_source_before','_receipt')).read_text());require(before['file_count']==receipt['runtime_source_file_count']==6452 and receipt['changed_runtime_sources']==[], 'source before/after executed receipt')
 for f in D.rglob('capture_manifest.json'):
  j=json.loads(f.read_text());require(j['normal_save_before']==j['normal_save_after'] and len(j['normal_save_before'])==8,'normal saves preserved')
 b=next(D.rglob('*v7*_source_before.json'));j=json.loads(b.read_text())
 for x in j['files']:require(sha((R/x['path']).read_bytes())==x['sha256'],'publication-source parity '+x['path'])
 v=read('root_picture_actions_review_20261012/harness_validation.json');require(len(v['gates'])==21 and all(x['returncode']==0 for x in v['gates']),'original syntax/type/engine checks')
 g=read('GARDEN_CLAY_POT_BINDING.json');require(g['canonical_piece_id']=='FVR-5A761C05C31C' and g['used_calls']==0 and g['accepted_removals']==0,'separate prepared job')
 print('ACTION|ALL OK|146retained/52successful/94failed;12viewed/8observations/6IDs;6452same-source;scopes countedonce;0removed')
def stress():
 base=[read(n) for n in ['root_picture_actions_review_20261012/review.json','tally.json','ACTION_CONTEXT_RECONCILIATION.json','per_piece.json']]
 controls=[('fake_owner',0,lambda x:x['evidence_lanes'].update(owner='ACCEPTED')),('failed_as_green',0,lambda x:x['captures'][0].update(run_returncode=0)),('double_count_scopes',2,lambda x:x.update(new_scope_classification_count=5)),('fake_capture_total',1,lambda x:x['current_context'].update(exact_capture_count=1678)),('fake_removal',1,lambda x:x.update(accepted_removed=1)),('fake_denominator',1,lambda x:x.update(all_game_individual_piece_total=224))]
 for name,i,fn in controls:
  a=copy.deepcopy(base);fn(a[i]);caught=False
  try:guard(*a)
  except ValueError:caught=True
  require(caught,'missed falsification '+name)
 print('ACTION|STRESS|6/6 inflated progress or acceptance claims rejected')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--stress',action='store_true');args=a.parse_args();check()
 if args.stress:stress()
