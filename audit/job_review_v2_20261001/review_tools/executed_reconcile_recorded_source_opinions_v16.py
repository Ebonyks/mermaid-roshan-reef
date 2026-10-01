from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_artwork_refinement_live'
family=r/'audit/job_review_v2_20261001'
builder=family/'review_tools/build_current_job_item_register_v7.py'
s=(family/'review_tools/build_current_job_item_register_v6.py').read_text(encoding='utf-8')
needle=" q['priority']=q['current_source_score'] is not None and q['current_source_score']<=4.5"
assert s.count(needle)==1
block=''' if q['current_source_score'] is None and q['kind']=='source' and hashes[p]:
  matched=[v for v in q['native_reference_observations'] if v.get('sha256')==hashes[p] and v.get('source_opinion') is not None and v.get('atlas_region') is None and v.get('earlier_written_evaluation')]
  if matched and len({v['source_opinion'] for v in matched})==1:
   prior=matched[-1]
   q['current_source_score']=prior['source_opinion']
   q['additional_recorded_source_opinion']=dict(score=prior['source_opinion'],sha256=prior['sha256'],record=prior.get('source_review_record') or 'audit/day_one_job_art_census_v2_20261001/INDIVIDUAL_NATIVE_ITEMS.json#'+str(prior.get('id','')),attribution=prior.get('source_opinion_attribution'),evaluation=prior['earlier_written_evaluation'],qualification='Carried forward existing whole-source drafting opinion for exact unchanged bytes. This reconciliation is not a new visual inspection, individual atlas-cell, mounted or complete-action pass.')
   q['evaluation']=prior['earlier_written_evaluation']
   q['source_qualification']+=' Exact-hash recorded Day One whole-source opinion reconciled separately; no new visual acceptance.'
'''
# The actual source record file is resolved from the V6 reader below.
import re
references=re.findall(r"read\('([^']+)'\)",s)
native_paths=[p for p in references if 'native' in p.lower() or 'NATIVE' in p]
print('native_record_inputs',native_paths)
assert 'INDIVIDUAL_NATIVE_ITEMS.json' in s or native_paths
actual=next(p for p in references if p.endswith('INDIVIDUAL_NATIVE_ITEMS.json')) if any(p.endswith('INDIVIDUAL_NATIVE_ITEMS.json') for p in references) else next(p for p in references if 'NATIVE' in p)
assert (r/actual).is_file(),actual
block=block.replace('audit/day_one_job_art_census_v2_20261001/INDIVIDUAL_NATIVE_ITEMS.json',actual)
s=s.replace(needle,block+needle).replace('build_current_job_item_register_v5.py','build_current_job_item_register_v7.py')
s=s.replace('earlier_written_evaluation:q.earlier_written_evaluation,latest_refinement:','earlier_written_evaluation:q.earlier_written_evaluation,additional_recorded_source_opinion:q.additional_recorded_source_opinion,latest_refinement:')
builder.write_text(s,encoding='utf-8',newline='\n')
before=json.loads((out/'ALL_ITEMS.json').read_text(encoding='utf-8'))
subprocess.run([sys.executable,'-X','utf8','-B',str(builder)],cwd=r,check=True)
after=json.loads((out/'ALL_ITEMS.json').read_text(encoding='utf-8'))
old={x['id']:x for x in before['items']}
changes=[dict(id=x['id'],path=x['path'],old_score=old[x['id']]['current_source_score'],reconciled=x['additional_recorded_source_opinion']) for x in after['items'] if x.get('additional_recorded_source_opinion')]
assert all(x['old_score'] is None for x in changes)
receipt=family/'SOURCE_OPINION_RECONCILIATION_V1.json'
receipt.write_text(json.dumps(dict(status='EXACT_BYTE_ATTRIBUTION_RECONCILIATION',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),before_counts=before['counts'],after_counts=after['counts'],restored_source_opinions=len(changes),changed_items=changes,qualification='Existing recorded source opinions only. No new direct source/cell/mounted/action or owner acceptance; unknown, changed or conflicting evidence stays unassigned.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,family/'review_tools/executed_reconcile_recorded_source_opinions_v16.py')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{builder.relative_to(r).as_posix(),receipt.relative_to(r).as_posix(),'audit/job_review_v2_20261001/review_tools/executed_reconcile_recorded_source_opinions_v16.py'})
d['rules']=list(dict.fromkeys(d['rules']+['DL-ASSET-02','DL-ASSET-06']))
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(restored=len(changes),before=before['counts'],after=after['counts'])))
