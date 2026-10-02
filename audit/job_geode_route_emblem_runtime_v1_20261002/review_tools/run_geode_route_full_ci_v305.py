from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, sys, time

root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
family=root/'audit/job_geode_route_emblem_runtime_v1_20261002'
folder=family/'full_ci_v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def cover():
 p=root/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(p.read_text())
 d['files']=sorted(set(d['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()})
 write(p,d)
if sys.argv[1:] == ['--prepare']:
 assert not folder.exists(),'Preserve every earlier full-CI attempt.'
 folder.mkdir()
 snapshot=json.loads((family/'SOURCE_CURRENT_BEFORE_CAPTURES.json').read_text())
 assert len(snapshot['source_files'])==373
 assert all(sha(root/r['path'])==r['sha256'] for r in snapshot['source_files'])
 snapshot['status']='CURRENT_LITERAL_SOURCE_SNAPSHOT'
 snapshot['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 snapshot['qualification']='Fresh current literal 373-file boundary, including current Library/goal/invitation bindings and actual route/resource review fixtures. Existing trusted scripts/ci.sh remains unmodified. All hashes frozen throughout the run; no inherited pass, hosted result or visual/device/owner acceptance.'
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==snapshot['baseline']
 paths={r['path'] for r in snapshot['source_files']}
 write(folder/'SOURCE_BEFORE.json',snapshot)
 wrapper='''#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/../.. /.."
'''
 # Absolute workspace avoids changing the trusted suite or copying it.
 workspace=root.as_posix().replace('C:/','/c/')
 wrapper=f'''#!/usr/bin/env bash
set -uo pipefail
cd '{workspace}'
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
python3() {{ /c/Users/Peter/AppData/Local/Python/bin/python.exe -X utf8 -B "$@"; }}
export -f python3
export GODOT="C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe"
export TMPDIR="$PWD/tmp"
bash scripts/ci.sh
result=$?
printf '%s\\n' "$result" > audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v2/process.exit
exit "$result"
'''
 (folder/'wrapper.sh').write_text(wrapper,encoding='utf-8')
 for name in ['stdout.log','stderr.log','process.exit']: (folder/name).write_text('',encoding='utf-8')
 write(folder/'RECEIPT.json',{'status':'PENDING','qualification':'Unmodified current full suite has not yet run.'})
 write(folder/'ENGINE_DIAGNOSTICS.json',{'status':'PENDING','items':[]})
 assert Path(__file__).resolve()==(family/'review_tools'/Path(__file__).name).resolve()
 cover();print('Prepared current full-CI snapshot:',len(paths),'files; source will remain frozen during run.');sys.exit(0)
assert sys.argv[1:]==['--run']
assert json.loads((folder/'RECEIPT.json').read_text())['status']=='PENDING'
snapshot=json.loads((folder/'SOURCE_BEFORE.json').read_text())
assert all(sha(root/r['path'])==r['sha256'] for r in snapshot['source_files'])
started=datetime.datetime.now(datetime.timezone.utc).isoformat();now=time.monotonic()
with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
 result=subprocess.run(['C:/Program Files/Git/bin/bash.exe',(folder/'wrapper.sh').as_posix()],cwd=root,stdout=out,stderr=err,
  creationflags=subprocess.CREATE_NO_WINDOW)
elapsed=time.monotonic()-now
stdout=(folder/'stdout.log').read_text(encoding='utf-8',errors='replace');stderr=(folder/'stderr.log').read_text(encoding='utf-8',errors='replace')
expected=re.search(r'for p in (.+?); do',(root/'scripts/ci.sh').read_text()).group(1).split()
verdicts=[{'probe':p,'process_exit':int(c)} for p,c in re.findall(r'^PROBE (\w+) process exit: (\d+)',stdout,re.M)]
source_checks=[{'path':r['path'],'before_sha256':r['sha256'],'after_sha256':sha(root/r['path']),'match':r['sha256']==sha(root/r['path'])} for r in snapshot['source_files']]
diagnostics=[{'stream':name,'line':i,'text':line} for name,text in [('stdout',stdout),('stderr',stderr)] for i,line in enumerate(text.splitlines(),1) if line.startswith(('ERROR:','WARNING:','SCRIPT ERROR:'))]
passed=result.returncode==0 and len(verdicts)==len(expected) and [r['probe'] for r in verdicts]==expected and all(r['process_exit']==0 for r in verdicts) and all(r['match'] for r in source_checks)
write(folder/'ENGINE_DIAGNOSTICS.json',{'status':'RAW_DIAGNOSTICS_PRESERVED','items':diagnostics,'qualification':'Passing process/probe verdicts do not establish error-free logs or creative acceptance. No diagnostic removed from raw canonical streams.'})
receipt={'status':'PASS_UNMODIFIED_CURRENT_FULL_SUITE' if passed else 'FAIL_PRESERVED_CURRENT_FULL_SUITE',
 'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':elapsed,
 'overall_process_exit':result.returncode,'expected_probe_count':len(expected),'probe_results':verdicts,
 'source_snapshot':'SOURCE_BEFORE.json','source_checks':source_checks,'source_unchanged':all(r['match'] for r in source_checks),
 'stdout_sha256':sha(folder/'stdout.log'),'stderr_sha256':sha(folder/'stderr.log'),'raw_diagnostic_count':len(diagnostics),
 'unittest_runs':[{'count':int(n),'seconds':float(s)} for n,s in re.findall(r'Ran (\d+) tests? in ([\d.]+)s',stderr)],
 'qualification':'Official Godot4.7.2-stable, unmodified scripts/ci.sh with existing isolated probe homes. Literal local source verification, not a hosted result, strict-zero debt, visual/device/child/owner/global approval or integration/release.'}
write(folder/'RECEIPT.json',receipt)
p=root/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(p.read_text())
command='Official Godot4.7.2 unmodified current geode route-emblem full suite2 scripts/ci.sh'
d['validation']=[v for v in d['validation'] if v['command']!=command]+[{'command':command,'result':'PASS' if passed else 'FAIL','evidence':(folder/'RECEIPT.json').relative_to(root).as_posix()+'; literal before/after source hashes and unfiltered raw streams retained.'}]
write(p,d);cover()
print('CURRENT_FULL_CI|'+receipt['status']+'|process'+str(result.returncode)+'|'+str(len(verdicts))+'/'+str(len(expected))+' probes|'+str(len(source_checks))+' source files|'+str(len(diagnostics))+' raw diagnostics')
sys.exit(0 if passed else 1)
