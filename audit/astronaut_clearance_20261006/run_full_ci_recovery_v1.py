from pathlib import Path
import json,hashlib,time,datetime,subprocess,os,re
ROOT=Path(__file__).resolve().parents[2]
AD=Path(__file__).resolve().parent
GODOT=Path(r"C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe")
PLAN=json.loads((AD/'FULL_CI_RECOVERY_V1_PLAN.json').read_text())
BINDINGS=json.loads((AD/'FULL_CI_RECOVERY_V1_SOURCE_BINDINGS.json').read_text())
TEMP=Path(PLAN['temporary_root'])
assert TEMP.is_dir() and TEMP.parent.resolve()==Path(r'C:/Users/Peter/AppData/Local/Temp').resolve()
assert hashlib.sha256(GODOT.read_bytes()).hexdigest()=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
for name,h in BINDINGS.items(): assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
started=time.monotonic(); deadline=started+PLAN['recovery_ceiling_seconds']
rows=[]
def save(result):
    changes=[n for n,h in BINDINGS.items() if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h]
    receipt={'result':result,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-started,3),'steps':rows,'source_binding_changes':changes,'scope':'Direct-native focused recovery only; full CI V3 retains FAIL. All82 source-bound per-probe reconciliation and metadata closure not inferred.'}
    (AD/'FULL_CI_RECOVERY_V1_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return receipt
steps=[('analyzer',['--headless','--path',str(ROOT),'--check-only','-s','scripts/probe_opera_2d.gd']),('probe_opera_2d',['--headless','--path',str(ROOT),'-s','scripts/probe_opera_2d.gd','--','--touch','--classic-touch-test']),('probe_day_one_bathroom_cleanup',['--headless','--path',str(ROOT),'-s','scripts/probe_day_one_bathroom_cleanup.gd','--','--touch','--classic-touch-test']),('probe_dust_boss_balance',['--headless','--path',str(ROOT),'-s','scripts/probe_dust_boss_balance.gd','--','--touch','--classic-touch-test'])]
FAILURE=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
RESOURCE=re.compile(r'Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)')
for name,args in steps:
    available=deadline-time.monotonic()
    if available<=0: save('FAIL_CAP'); raise SystemExit(1)
    home=TEMP/name; home.mkdir()
    for folder in ['appdata','localappdata','data','config']: (home/folder).mkdir()
    env=os.environ.copy(); env.update(APPDATA=str(home/'appdata'),LOCALAPPDATA=str(home/'localappdata'),XDG_DATA_HOME=str(home/'data'),XDG_CONFIG_HOME=str(home/'config'),PYTHONIOENCODING='utf-8',PYTHONUTF8='1',GODOT=str(GODOT))
    path=AD/f'FULL_CI_RECOVERY_V1_{name}_LOG.txt'
    with path.open('wb') as out:
        proc=subprocess.Popen([str(GODOT),*args],cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        row={'step':name,'pid':proc.pid,'argv':[str(GODOT),*args],'save_profile':str(home),'log':path.name,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RUNNING'}
        rows.append(row); save('RUNNING'); print(f'START {name} PID{proc.pid}',flush=True)
        wall=time.monotonic(); cap=min(480.0,available)
        try: rc=proc.wait(timeout=cap)
        except subprocess.TimeoutExpired:
            proc.kill(); rc=proc.wait(timeout=10); row['terminated_at_cap']=True
        row.update(exit_code=rc,elapsed_seconds=round(time.monotonic()-wall,3))
    text=path.read_text(encoding='utf-8',errors='replace')
    issues=[l for l in text.splitlines() if FAILURE.search(l) or RESOURCE.search(l)]
    row.update(log_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),failure_lines=issues,nonempty=bool(text.strip()),final_result_seen=(name=='analyzer' or any('result:' in l.lower() and ('all ok' in l.lower() or 'pass' in l.lower()) for l in text.splitlines())))
    okay=rc==0 and not issues and row['nonempty'] and row['final_result_seen'] and not row.get('terminated_at_cap')
    row['status']='PASS' if okay else 'FAIL'
    save('RUNNING' if okay else 'FAIL'); print(f'END {name} {row["status"]} exit{rc} seconds{row["elapsed_seconds"]}',flush=True)
    if not okay: raise SystemExit(1)
r=save('PASS'); print(json.dumps({'result':r['result'],'elapsed_seconds':r['elapsed_seconds']}),flush=True)
