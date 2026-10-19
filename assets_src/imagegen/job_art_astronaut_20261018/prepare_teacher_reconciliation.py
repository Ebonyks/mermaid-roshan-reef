from pathlib import Path
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
out=src/'verification'
def git(*args):return subprocess.run(['git',*args],cwd=root,capture_output=True,encoding='utf-8',text=True,check=True).stdout
current=(root/'ASSET_LICENSES.md').read_text('utf-8')
for ref in ['HEAD','MERGE_HEAD']:
    required={line for line in git('show',ref+':ASSET_LICENSES.md').splitlines() if line.startswith('| `')}
    present=set(current.splitlines())
    assert required<=present,(ref,len(required-present))
assert not git('diff','HEAD','--','scripts/opera_gesture_surface.gd').strip(),'Astronaut renderer must stay exact'
source_receipt=json.loads((out/'full_ci_03.json').read_text())
asset_drift=[p for p,h in source_receipt['source_sha256_raw_checkout'].items()
    if p.startswith('assets/opera/worlds/widgets/') and hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
assert not asset_drift,asset_drift
remote={'commit':'90508b85f2278ec27d4bdad24fac4ba747d28e2f','run':39227500753,'conclusion':'success',
    'url':'https://github.com/Ebonyks/mermaid-roshan-reef/actions/runs/39227500753',
    'teacher_dev':'e90c0daa83cf05644f0e9942e85c1198ed7901f7','integration':'New combined source must pass local82 and exact remoteCI beforedev. No master promotion.',
    'retained_AST_rendering_and_widgets':'Exact90508b85bytes; Teacher changes use their own career scope, no production code conflicts.',
    'license_rows_from_both_parents':'All preserved byte-for-byte as text rows'}
(out/'remote_ci_and_merge_20261019.json').write_text(json.dumps(remote,indent=2)+'\n')
adapter=(out/'windows_native_capture_05.py').read_text().replace('native_capture_05_events.jsonl','native_capture_04_events.jsonl')
(out/'windows_native_capture_04.py').write_text(adapter)
shell=(out/'run_ci_native_capture_03.sh').read_text().replace('windows_native_capture_05.py','windows_native_capture_04.py')
(out/'run_ci_native_capture_04.sh').write_text(shell)
runner=(out/'run_full_ci_03.py').read_text().replace('full_ci_03','full_ci_04').replace('run_ci_native_capture_03.sh','run_ci_native_capture_04.sh')
runner=runner.replace('sha = lambda p:', '''teacher_impact=json.loads((root/'design/audit_impacts/job-art-teacher-20261018.json').read_text())
sources += [root/p for p in teacher_impact['files'] if p.startswith('assets/') and p.endswith('.png') and (root/p).is_file()]
sha = lambda p:''')
(out/'run_full_ci_04.py').write_text(runner)
for name in ['full_ci_04.log','native_capture_04_events.jsonl']:
    p=out/name;assert not p.exists();p.touch()
(out/'full_ci_04.json').write_text(json.dumps({'status':'PENDING','scope':'Combined greenTeacher e90 plus greenAstronaut905 source; full unchanged scripts/ci.sh82probes, no retries, original deadlines/classifiers, exact4.7.2'},indent=2)+'\n')
paragraph='Combined art reconciliation2026-10-19: Teacher e90c0daa passed exact remoteCI39217603860 and was fast-forward integrated into dev; Astronaut90508b85 passed exact remoteCI39227500753. Their topic merge preserves both license/index/history tails, all Astronaut widget bytes and its exact rendering file; no production-code conflict. New combined full82local and exact-head remoteCI remain required before Astronaut integration. Shared P8/formal/human motion/device/child/owner acceptance and master UNSATISFIED remain unchanged.'
p=root/'audit/MASTER_AUDIT_2026-08-09.md';text=p.read_text('utf-8');assert paragraph not in text
text=text.replace('### Development task index',paragraph+'\n\n### Development task index',1);p.write_text(text,encoding='utf-8')
p=root/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';text=p.read_text('utf-8')+'\nCHG-105 Teacher reconciliation2026-10-19: '+paragraph+' See assets_src/imagegen/job_art_astronaut_20261018/verification/teacher_reconciliation.json and remote_ci_and_merge_20261019.json; full_ci_04 binds the new combined runtime.\n';p.write_text(text,encoding='utf-8')
p=root/'design/audit_impacts/job-art-astronaut-20261018.json';d=json.loads(p.read_text())
d['scope']+=' Reconcile the exact green Teacher dev e90c0daa into green Astronaut90508b85 before integration. Preserve all license/history/index tails and own-state art; no production code conflicts or Astronaut rendering/widget changes. Re-run complete82local and exact-head remoteCI for combined source; original per-package passes retain their own scopes.'
d['validation'] += [{'command':'Exact-head remoteCI39227500753 on90508b85','result':'PASS','evidence':'verification/remote_ci_and_merge_20261019.json; both probes and area-music jobs success.'},
    {'command':'Combined Teacher/Astronaut complete82 local suite04','result':'PENDING','evidence':'verification/full_ci_04.json/log; exact combined source pins, original commands/classifiers/deadlines, no retry.'}]
d['acceptance_gaps']='Astronaut90508b85 local82 and remoteCI39227500753pass. Teacher e90c0daa already integrateddev after its own exact greenCI. New combined local82/remoteCI and Astronautdev integration remain pending; sharedP8/global/formal/human motion/device/child/owner gates unchanged.'
d['files']=sorted(set(d['files']+[p.relative_to(root).as_posix()]+[p.relative_to(root).as_posix() for p in src.rglob('*') if p.is_file()]))
p.write_text(json.dumps(d,indent=2)+'\n')
print('Combined source and license assertions pass; full04prepared, integration still pending')
