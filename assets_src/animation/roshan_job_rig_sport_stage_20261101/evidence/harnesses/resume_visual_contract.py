from pathlib import Path
import unittest,json,time,re,hashlib,datetime,sys
R=Path(__file__).resolve().parents[2];repo=R.parents[2];sys.path.insert(0,str(repo));out=R/'evidence/visual_contract_resume';out.mkdir(exist_ok=True);retry=R/'evidence/baseline_retry_after_native';
while not (retry/'receipt.json').exists() or not json.loads((retry/'receipt.json').read_text()).get('complete',False):time.sleep(10)
receipt=json.loads((retry/'receipt.json').read_text());prior=next(x for x in receipt['rows'] if x['name']=='visual_contract_unittest');log=(retry/prior['log']).read_text(errors='replace')
if prior['pass']:
 (out/'receipt.json').write_text(json.dumps({'pass':True,'scope':'Focused full95test retry already completed; no tests repeated.','reused':prior},indent=2)+'\n');print('VISUAL_CONTRACT_RESUME_NOT_NEEDED',flush=True);raise SystemExit(0)
if prior['exit']!=124 or re.fullmatch(r'\.*\s*',log) is None:raise SystemExit('Cannot establish successful test prefix; no partial proof claimed')
finished=log.count('.');suite=unittest.defaultTestLoader.loadTestsFromName('tools.tests.test_audit_visual_design')
def flat(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from flat(t)
  else:yield t
alltests=list(flat(suite));assert 0<finished<len(alltests),(finished,len(alltests));names=[x.id() for x in alltests];remaining=unittest.TestSuite(alltests[finished:]);start=time.monotonic()
with (out/'remaining_tests.log').open('w',encoding='utf-8') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(remaining)
d={'scope':'Resume ONLY unfinished original unit cases after bounded wrapper timeout. The retained leading success-dot prefix maps to default unittest loader order; identical module and unmodified assertions. Timeout itself remains in history. No completed successful test repeated.','module_sha256':hashlib.sha256((repo/'tools/tests/test_audit_visual_design.py').read_bytes()).hexdigest(),'total_original_tests':len(alltests),'successful_prefix_count':finished,'successful_prefix_ids':names[:finished],'prefix_log_sha256':hashlib.sha256((retry/prior['log']).read_bytes()).hexdigest(),'remaining_tests_count':result.testsRun,'remaining_test_ids':names[finished:],'errors':len(result.errors),'failures':len(result.failures),'skips':len(result.skipped),'seconds':round(time.monotonic()-start,2),'pass':result.wasSuccessful() and finished+result.testsRun==len(alltests)};(out/'receipt.json').write_text(json.dumps(d,indent=2)+'\n');print('VISUAL_CONTRACT_RESUMED',finished,result.testsRun,d['pass'],flush=True)
