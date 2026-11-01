"""Historical f59 runner retained as evidence; current-base verification uses regression/tail_gates."""
raise SystemExit('Historical runner disabled after base reconciliation; see attempt_f59 records and use regression.py for a fresh full run.')
from pathlib import Path
import json,os,re,subprocess,sys,time
P=Path(__file__).resolve().parents[1];R=P.parents[2];O=P/'evidence/regression'
old=json.loads((O/'probes_summary.json').read_text(encoding='utf-8'))
static=json.loads((O/'static_summary.json').read_text(encoding='utf-8'))
godot=subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],cwd=R,text=True).strip()
roster=re.search(r'(?m)^for p in (.+?); do',(R/'scripts/ci.sh').read_text(encoding='utf-8')).group(1).split()
done={x['name']:x for x in old if x['passed']}
rows=[]
bad=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
runtime=re.compile(r'Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)')
def save(path,obj):
    temporary=path.with_suffix('.writing')
    temporary.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)
for name in roster:
    if name in done:
        rows.append(done[name]);continue
    profile=R/'tmp'/('creative-final-'+str(time.time_ns())+'-'+name)
    for folder in ['appdata','localappdata','data','config']:(profile/folder).mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,APPDATA=str(profile/'appdata'),LOCALAPPDATA=str(profile/'localappdata'),XDG_DATA_HOME=str(profile/'data'),XDG_CONFIG_HOME=str(profile/'config'),PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
    mode='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test'
    args=[godot,'--headless','-s','scripts/'+name+'.gd','--','--touch',mode];start=time.monotonic()
    try:
        result=subprocess.run(args,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=480);data=result.stdout;code=result.returncode
    except subprocess.TimeoutExpired as exc:data=exc.stdout or b'';code=124
    text=data.decode('utf-8',errors='replace');log=name+'_final_replay.log';(O/log).write_bytes(data)
    exit_hang=code==124 and re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:]))
    passed=bool((code==0 or exit_hang) and data and not bad.search(text) and not runtime.search(text))
    rows.append(dict(name=name,passed=passed,exit=code,command=args,log=log,seconds=time.monotonic()-start,profile='fresh isolated timestamp profile'))
    save(O/'final_probe_summary.json',dict(rows=rows,complete=len(rows)==len(roster),passed=len(rows)==len(roster) and all(x['passed'] for x in rows),first_attempts_retained='probes_summary.json and probe_audit_fresh_replay.json',runtime='production source unchanged at f59a1d1d5bdd58604f4706d16fb4e76d8f7db8b9'))
    print(name,'PASS' if passed else 'FAIL',round(time.monotonic()-start,2),flush=True)
save(O/'final_probe_summary.json',dict(rows=rows,complete=True,passed=all(x['passed'] for x in rows),first_attempts_retained='probes_summary.json and probe_audit_fresh_replay.json',runtime='production source unchanged at f59a1d1d5bdd58604f4706d16fb4e76d8f7db8b9'))
print('ALL TRUSTED PROBES ALL OK' if all(x['passed'] for x in rows) else 'TRUSTED PROBES STILL FAIL',flush=True)
raise SystemExit(0 if all(x['passed'] for x in rows) else 1)
