"""Run the final twenty unchanged CI probes beside the serial prefix, in isolated profiles."""
from pathlib import Path
import json,os,re,subprocess,sys,time
P=Path(__file__).resolve().parents[1];R=P.parents[2];O=P/'evidence/regression'
source=(R/'scripts/ci.sh').read_text(encoding='utf8')
names=re.search(r'(?m)^for p in (.+?); do',source).group(1).split()[-20:]
godot=subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],cwd=R,text=True).strip()
bad=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
runtime=re.compile(r'Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)')
rows=[];stamp=str(time.time_ns())
for name in names:
    profile=R/'tmp'/('creative-tail-'+stamp+'-'+name)
    for folder in ['appdata','localappdata','data','config']:(profile/folder).mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,APPDATA=str(profile/'appdata'),LOCALAPPDATA=str(profile/'localappdata'),XDG_DATA_HOME=str(profile/'data'),XDG_CONFIG_HOME=str(profile/'config'),PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
    args=[godot,'--headless','-s','scripts/'+name+'.gd','--','--touch','--classic-touch-test'];start=time.monotonic()
    try:
        result=subprocess.run(args,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=480);data=result.stdout;code=result.returncode
    except subprocess.TimeoutExpired as exc:data=exc.stdout or b'';code=124
    text=data.decode('utf8',errors='replace');log='tail_'+name+'.log';(O/log).write_bytes(data)
    exit_hang=code==124 and re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:]))
    passed=bool((code==0 or exit_hang) and data and not bad.search(text) and not runtime.search(text))
    rows.append(dict(name=name,command=args,exit=code,passed=passed,seconds=time.monotonic()-start,log=log,profile='fresh isolated timestamp profile'))
    (O/'tail_probe_summary.json').write_text(json.dumps(dict(rows=rows,complete=len(rows)==len(names),passed=len(rows)==len(names) and all(x['passed'] for x in rows),baseline='93166ab1828ab9857227d038f8833b92dfb2f9f1',scheduling='One tail engine beside one serial-prefix engine; same commands, timeout and verdict floors as scripts/ci.sh; no shared save profile.'),indent=2)+'\n',encoding='utf8')
    print(name,'PASS' if passed else 'FAIL',round(time.monotonic()-start,2),flush=True)
print('TAIL ALL OK' if all(x['passed'] for x in rows) else 'TAIL FAIL',flush=True)
raise SystemExit(0 if all(x['passed'] for x in rows) else 1)
