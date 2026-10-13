"""Verify the claimed Luna session count against actual coordinator/report receipts."""
from pathlib import Path
from datetime import datetime, timezone
import argparse,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[4]; CYCLE=ROOT/'audit/cycles/luna-playtest-20261012'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--partial',action='store_true'); a=parser.parse_args()
 matrix=json.loads((CYCLE/'matrix.json').read_text()); expected=len(matrix['sessions']); errors=[]; sessions=[]; report_paths=sorted((CYCLE/'reports').glob('L*.json'))
 coordinator=json.loads((CYCLE/'coordinator.json').read_text()); invoked={x['session_id']:x for x in coordinator['agents']}
 names=set(); ids=set(); stats={'runtime_PASS':0,'runtime_FAIL':0,'INTERNAL_PROBE':0,'ROUTED_INPUT_PROBE':0}; observations=[]
 for path in report_paths:
  try:
   report=json.loads(path.read_text(encoding='utf-8')); sid=report['session_id']; row=next(x for x in matrix['sessions'] if x['id']==sid)
   if path.name!=sid+'.json' or sid in ids: raise ValueError('Duplicate/mismatched session')
   ids.add(sid)
   if report.get('schema')!='luna_playthrough_report/1' or report.get('baseline')!=matrix['baseline']: raise ValueError('Schema/source mismatch')
   reviewer=report['reviewer']; name=reviewer['agent_id']
   if reviewer.get('model')!='gpt-6-luna' or name in names or not name.endswith('/luna_'+sid.lower()): raise ValueError('Actual independent Luna reviewer identity missing/duplicate')
   if sid not in invoked or invoked[sid]['agent_id']!=name or invoked[sid]['model']!='gpt-6-luna': raise ValueError('Report identity absent from actual invocation manifest')
   names.add(name)
   for field in ['focus','runtime_receipt','evidence_kind','route_status','verdict','timing','tactile','play_appeal','observations','strengths','acceptance_gaps']:
    if field not in report: raise ValueError('Missing field '+field)
   if report['evidence_kind'] not in ['INTERNAL_PROBE','ROUTED_INPUT_PROBE']: raise ValueError('Evidence kind overstated/unknown')
   receipt_path=ROOT/report['runtime_receipt']
   if not receipt_path.resolve().is_relative_to(CYCLE.resolve()): receipt_path=path.parent/report['runtime_receipt']
   receipt_path=receipt_path.resolve()
   if not receipt_path.is_relative_to(CYCLE.resolve()): raise ValueError('Receipt outside cycle')
   receipt=json.loads(receipt_path.read_text()); log=ROOT/receipt['log']
   if receipt['session_id']!=sid or receipt['probe']!=row['probe'] or receipt['baseline']!=matrix['baseline']: raise ValueError('Runtime provenance mismatch')
   if receipt['status'] not in ['PASS','FAIL'] or receipt.get('log_sha256')!=sha(log): raise ValueError('Runtime incomplete/log hash mismatch')
   if not receipt['profile_isolated'] or receipt['engine']['version']!='4.7.2.stable.official.ed1daf0bf': raise ValueError('Engine/profile mismatch')
   if receipt['status']=='FAIL' and report['verdict']=='PASS': raise ValueError('Report masks failed runtime')
   # Reporting a fun score would fabricate a child/product acceptance measure.
   def scores(value):
    if isinstance(value,dict):
     for key,v in value.items():
      if key=='fun_score' and v is not None: raise ValueError('Numeric fun score forbidden')
      scores(v)
    elif isinstance(value,list):
     for v in value: scores(v)
   scores(report)
   stats['runtime_'+receipt['status']]+=1; stats[report['evidence_kind']]+=1
   for observation in report['observations']:
    if observation.get('classification') not in ['CONFIRMED_RUNTIME','CONFIRMED_CODE','HYPOTHESIS','COVERAGE_GAP']: raise ValueError('Unknown observation evidence class')
    for key,prefix in [('rules','DL'),('existing_findings','MA')]:
     values=observation.get(key)
     if not isinstance(values,list) or any(not isinstance(v,str) or not re.fullmatch(prefix+r'-[A-Z0-9]+-\d+',v) for v in values): raise ValueError('Observation '+key+' must be an ID array')
    observations.append({'session_id':sid,**observation})
   sessions.append({'id':sid,'agent_id':name,'model':reviewer['model'],'focus':row['focus'],'probe':row['probe'],'evidence_kind':report['evidence_kind'],'runtime_status':receipt['status'],'report_verdict':report['verdict'],'report':path.relative_to(ROOT).as_posix(),'report_sha256':sha(path),'receipt':receipt_path.relative_to(ROOT).as_posix(),'receipt_sha256':sha(receipt_path),'log_sha256':sha(log)})
  except Exception as exc: errors.append(path.name+': '+str(exc))
 if not a.partial and len(sessions)!=expected: errors.append(f'Only {len(sessions)} valid actual sessions of{expected}')
 if not a.partial and coordinator.get('completed_count')!=expected: errors.append(f'Coordinator has not confirmed{expected} completed agent sessions')
 if not a.partial and any(not invoked[x['id']].get('status','').startswith('completed') for x in sessions): errors.append('One or more actual agents have not completed')
 result={'schema':'luna_playtest_verification/1','baseline':matrix['baseline'],'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not errors and len(sessions)==expected else ('IN_PROGRESS' if a.partial and not errors else 'FAIL'),'planned':expected,'completed_valid_sessions':len(sessions),'errors':errors,'counts':stats,'sessions':sessions,'observations':observations,'limits':'Count is separate invoked Luna source/runtime reviews; repeated unchanged probe programs are shared anchors, not separate full-game GUI playthroughs. No Mobile/device/child/fun acceptance.'}
 out=CYCLE/'verification'; out.mkdir(exist_ok=True); (out/'sessions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k not in ['sessions','observations']},ensure_ascii=False)); return 1 if errors or (not a.partial and len(sessions)!=expected) else 0
if __name__=='__main__': sys.exit(main())
