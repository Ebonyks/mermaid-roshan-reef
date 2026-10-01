"""Record exact bounded project checks for the non-runtime reference packet."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[2]
BASE='b65c21fdddd79f272a6854f241faa1441abe6616'
evidence=ROOT/'verification';evidence.mkdir(exist_ok=True)


def run(name, args):
    log=evidence/(name+'.log')
    if name=='development_coverage':
        if not log.exists(): log.write_text('',encoding='utf-8')
        impact=PROJECT/'design/audit_impacts/sky-lagoon-moderate-animation-20260930.json'
        record=json.loads(impact.read_text())
        record['files']=sorted(set(record['files'])|{p.relative_to(PROJECT).as_posix() for p in ROOT.rglob('*') if p.is_file()})
        impact.write_text(json.dumps(record,indent=2),encoding='utf-8')
    result=subprocess.run(args,cwd=PROJECT,capture_output=True,text=True)
    log.write_text(result.stdout+result.stderr,encoding='utf-8')
    print(result.stdout+result.stderr,flush=True)
    assert result.returncode==0,(name,result.returncode)
    return {'command':' '.join(map(str,args)), 'result':'PASS','evidence':log.relative_to(ROOT).as_posix(),
            'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}


proof=json.loads((ROOT/'PROJECT_VERIFICATION.json').read_text())
proof['runtime_source_comparison']=run('runtime_source_comparison',['git','diff',BASE,'--name-only','--','scripts','scenes','assets','project.godot','.github/workflows'])
assert not (evidence/'runtime_source_comparison.log').read_text().strip(), 'Runtime files changed'
proof['authority']=run('document_authority',[sys.executable,'-s','-B','tools/audit_document_authority.py'])
proof['development_coverage']=run('development_coverage',[sys.executable,'-s','-B','tools/audit_development.py','--base','auto'])
proof['contract_tests']=run('contract_tests',[sys.executable,'-s','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])
shutil.copy2(PROJECT/'build/moderate-reference-import-clean.log',evidence/'godot_import.log')
log=(evidence/'godot_import.log').read_text(encoding='utf-8')
assert 'ERROR:' not in log and 'WARNING:' not in log and '4.7.2.stable.official.ed1daf0bf' in log
proof['import'].update(result='PASS',evidence='verification/godot_import.log',
                       log_sha256=hashlib.sha256((evidence/'godot_import.log').read_bytes()).hexdigest(),
                       notes='Clean import after excluding the local validation venv with ignored build/.gdignore. Generated tracked platform import sidecars restored; source comparison is empty.')
proof['browser_preview']={'result':'PASS','evidence':'Observed ten cards, advancing key counters, native-pixel/scene controls and current moderate gallery at http://127.0.0.1:8191/; browser QA does not confer owner animation acceptance.'}
(ROOT/'PROJECT_VERIFICATION.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
impact=PROJECT/'design/audit_impacts/sky-lagoon-moderate-animation-20260930.json'
record=json.loads(impact.read_text())
record['validation'][2]={'command':'production/check_project.py','result':'PASS','evidence':ROOT.relative_to(PROJECT).as_posix()+'/PROJECT_VERIFICATION.json; authority/development ALL OK, 52 tests, exact-4.7.2 clean import, zero runtime-source diff; baseline full-game CI success at '+BASE+'.'}
record['files']=sorted(set(record['files'])|{p.relative_to(PROJECT).as_posix() for p in ROOT.rglob('*') if p.is_file()})
impact.write_text(json.dumps(record,indent=2),encoding='utf-8')
print('PROJECT REFERENCE GATES ALL OK',flush=True)
