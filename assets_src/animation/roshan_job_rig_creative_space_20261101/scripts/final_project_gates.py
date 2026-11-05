"""Consolidate actual unchanged CI verdicts and replay governance after all paths settle."""
from pathlib import Path
import json,re,subprocess,sys,time
P=Path(__file__).resolve().parents[1];R=P.parents[2];O=P/'evidence/regression'
ci=(R/'scripts/ci.sh').read_text(encoding='utf8');expected=re.search(r'(?m)^for p in (.+?); do',ci).group(1).split()
static=json.loads((O/'static_summary.json').read_text(encoding='utf8'))
extra=O/'remaining_static_summary.json'
if extra.exists():
    merged={x['name']:x for x in static}
    for row in json.loads(extra.read_text(encoding='utf8')):
        if row['name'] not in merged:merged[row['name']]=row
        elif not row['passed'] and not row.get('advisory',False):merged[row['name']]=row
    static=[merged[k] for k in sorted(merged)]
serial=json.loads((O/'probes_summary.json').read_text(encoding='utf8'))
tail=json.loads((O/'tail_probe_summary.json').read_text(encoding='utf8')).get('rows',[])
checks=[]
commands=[('final_authority',[sys.executable,'-B','tools/audit_document_authority.py']),('final_coverage',[sys.executable,'-B','tools/audit_development.py','--base','auto']),('final_contract_tests',[sys.executable,'-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']),('final_diff_check',['git','diff','--check','HEAD','--',P.relative_to(R).as_posix(),'ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','design/audit_impacts/roshan-job-rig-creative-space-20261101.json'])]
for name,args in commands:
    start=time.monotonic();result=subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (P/'evidence'/(name+'.log')).write_bytes(result.stdout);checks.append(dict(name=name,command=args,exit=result.returncode,passed=result.returncode==0,seconds=time.monotonic()-start));print(name,'PASS' if result.returncode==0 else 'FAIL',flush=True)
overrides={}
for row in static:
    for path,name in [('tools/audit_document_authority.py','final_authority'),('tools/audit_development.py','final_coverage')]:
        if path in row['command']:overrides[row['name']]=next(x for x in checks if x['name']==name)
effective_static=[dict(row,effective_pass=bool(overrides.get(row['name'],row)['passed'] or row.get('advisory',False)),replay=overrides.get(row['name'])) for row in static]
by_name={name:[x for x in serial+tail if x['name']==name] for name in expected}
probe_pass={name:bool(rows) and all(x['passed'] for x in rows) for name,rows in by_name.items()}
static_count=len([l for l in ci.replace('\\\n',' ').splitlines() if l.strip().startswith('python3 ')])
preflight=[x for x in serial if x['name'] in ['import','game_2d']]
passed=(len(static)==static_count and all(x['effective_pass'] for x in effective_static) and all(probe_pass.values()) and len(preflight)==2 and all(x['passed'] for x in preflight) and all(x['passed'] for x in checks))
result=dict(passed=passed,baseline='93166ab1828ab9857227d038f8833b92dfb2f9f1',static_expected=static_count,static=effective_static,probe_expected=len(expected),probe_pass=probe_pass,probe_evidence=by_name,preflight=preflight,final_checks=checks,scheduling='Serial prefix and isolated final-twenty runner; same original CI commands, eight-minute timeouts, failure/resource regex and positive-output floor. No test assertions changed. Any stopped duplicate gets no verdict.',prior_failures='All f59 attempts and the early structural coverage failure during file creation remain preserved. Governance replay uses the complete actual diff; no narrower base.',candidate_acceptance='FAIL: source candidate numerical/static-visual failures remain separately blocking. Green project regression does not accept it.')
(P/'evidence/final_gates.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print('FULL PROJECT GATES ALL OK' if passed else 'FULL PROJECT GATES FAIL',sum(probe_pass.values()),'/',len(expected),flush=True)
raise SystemExit(0 if passed else 1)
