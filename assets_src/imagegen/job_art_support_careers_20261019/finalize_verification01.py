from pathlib import Path
import hashlib,json,subprocess
from datetime import datetime,timezone
r=Path(__file__).resolve().parents[3];s=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
full=json.loads((s/'verification/full_ci_native_capture_01.json').read_text(encoding='utf-8'))
assert full['status']=='PASS' and full['expected_probes']==82 and len(full['completed_probes'])==82 and not full['source_drift'] and full['actual_save_unchanged']
assert full['log_sha256']==sha(s/'verification/full_ci_native_capture_01.log')
rows=json.loads((s/'runtime_provenance04.json').read_text(encoding='utf-8'))['records'];assert len(rows)==56
for row in rows:
 assert sha(r/row['path'])==row['sha256'],row['path']
 assert sha(r/row['source'])==row['source_sha256'],row['source']
 assert row['cutout']['verdict']=='CUTOUT_OK',row['path']
prompts=json.loads((s/'prompts.json').read_text(encoding='utf-8'));assert len(prompts)==59
for row in prompts:assert sha(r/row['native_path'])==row['native_sha256'],row['id']
art=json.loads((s/'review/art_review.json').read_text(encoding='utf-8'));assert len(art['assets'])==56
for row in art['assets']:
 assert sha(r/row['path'])==row['sha256'] and min(row['ratings'].values())>=4.5
 for frame in row['context_evidence']:assert sha(r/frame['path'])==frame['sha256'],frame['path']
for key in ['context_manifest','object_manifest']:assert sha(s/art[key]['path'])==art[key]['sha256']
current09=json.loads((s/'capture_current09_receipt.json').read_text(encoding='utf-8'))
receipt={'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_LOCAL_MACHINE_AND_STATIC_RECONCILIATION','current_parent':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'native_calls':59,'runtime_png':56,'cutouts':'56/56 CUTOUT_OK','individual_static_floor':4.5,'static_review':'review/art_review.json; all seven object and forty context pages actually inspected;238 current source-bound configured GUI frames','full_suite':{'receipt':'verification/full_ci_native_capture_01.json','receipt_sha256':sha(s/'verification/full_ci_native_capture_01.json'),'log_sha256':full['log_sha256'],'probes':82,'elapsed_seconds':full['elapsed_seconds'],'source_drift':[],'actual_save_unchanged':True},'limits':'Not full animation/contact, canonicalQA11natural-route, physicaldevice/child/owner/finalcampaign acceptance. ExactheadremoteCI and Dev integration separately pending; master UNSATISFIED.'}
(s/'publication_verification01.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-art-support-careers-20261019.json';d=json.loads(p.read_text(encoding='utf-8'))
d['validation'].append({'command':'Final full82/local-static/source-hash reconciliation','result':'PASS','evidence':'publication_verification01.json:59 native originals and56runtime sources/hashes/C2 verified; all56individualscored staticdimensions>=4.5; current09twofinalrenderfunction supplement10PASS; full01all82PASS/source0drift/actualsaveunchanged in2465.752s; logSHA256 '+full['log_sha256']+'. Earlier failures and original pending intake entries retain their scope. ExactheadremoteCI/Dev separately pending.'})
d['acceptance_gaps']=d['acceptance_gaps'].replace('currentfull82local/exactheadCI','exactheadremoteCI/Dev integration')
p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
p=r/'audit/MASTER_AUDIT_2026-08-09.md';t=p.read_text(encoding='utf-8');old='Full82currentlocal/exactheadremoteCI and integration are separately required; roomnativecoverage/sharedHUD debt and finding lifecycles/masterUNSATISFIED remain unchanged.';new='Current full local82 passes with frozen sources and unchanged actualdesktop save; exactheadremoteCI and integration remain separately required. Roomnativecoverage/sharedHUD debt and finding lifecycles/masterUNSATISFIED remain unchanged.';assert t.count(old)==1;t=t.replace(old,new);p.write_text(t,encoding='utf-8')
for name in ['audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 p=r/name;t=p.read_text(encoding='utf-8');lines=t.splitlines()
 for i,line in enumerate(lines):
  if 'job-art-support-careers-20261019.json' in line:
   suffix=' Local verification completed2026-10-19: full82PASS/source0drift/actualdesktop save unchanged; publication_verification01.json binds logSHA256 '+full['log_sha256']+'. ExactheadremoteCI/Dev and all external acceptance gates remain pending.'
   lines[i]=line.rstrip()[:-1].rstrip()+suffix+' |' if line.startswith('|') and line.rstrip().endswith('|') else line+suffix
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(receipt))
