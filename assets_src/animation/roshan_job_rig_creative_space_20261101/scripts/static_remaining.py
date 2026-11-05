"""Overlap unchanged read-only checks after the long audio scan; retain exact exit verdicts."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,os,shlex,subprocess,sys,time
P=Path(__file__).resolve().parents[1];R=P.parents[2];O=P/'evidence/regression'
source=(R/'scripts/ci.sh').read_text(encoding='utf8').replace('\\\n',' ')
commands=[line.strip() for line in source.splitlines() if line.strip().startswith('python3 ')]
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
def run(index):
    command=commands[index];advisory='|| true' in command;args=shlex.split(command.split('||')[0].strip());args[0]=sys.executable;start=time.monotonic()
    result=subprocess.run(args,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log='remaining_static_%02d.log'%index;(O/log).write_bytes(result.stdout)
    row=dict(name='static_%02d'%index,command=args,exit=result.returncode,passed=result.returncode==0,advisory=advisory,seconds=time.monotonic()-start,log=log)
    print(row['name'],'PASS' if row['passed'] else 'ADVISORY' if advisory else 'FAIL',round(row['seconds'],2),flush=True);return row
rows=[]
with ThreadPoolExecutor(max_workers=2) as pool:
    jobs=[pool.submit(run,i) for i in range(38,57)]
    for future in as_completed(jobs):
        rows.append(future.result());(O/'remaining_static_summary.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
# The normal CI executes this gate once. regression.py probes already executed
# that same gate on this base; preserve that actual transcript rather than rescan.
preflight=json.loads((O/'probes_summary.json').read_text(encoding='utf8'))
gate=next(x for x in preflight if x['name']=='game_2d')
rows.append(dict(gate,name='static_57',log='game_2d.log',evidence_reuse='Same actual current-base 2D regression gate as CI static_57; no production file changed. Not a second execution.'))
(O/'remaining_static_summary.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
print('REMAINING STATIC ALL OK' if all(x['passed'] or x.get('advisory',False) for x in rows) else 'REMAINING STATIC FAIL',flush=True)
raise SystemExit(0 if all(x['passed'] or x.get('advisory',False) for x in rows) else 1)
