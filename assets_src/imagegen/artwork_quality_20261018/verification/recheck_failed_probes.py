from pathlib import Path
import subprocess, os, json, hashlib, time, tempfile
root=Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
out=root/'assets_src/imagegen/artwork_quality_20261018/verification'
engine=root/'tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
rows=[]
for probe in ['probe_partner','probe_dust_boss_balance','probe_props']:
    start=time.monotonic();home=Path(tempfile.mkdtemp(prefix='art-native-probe-'));env=os.environ.copy()
    env.update(APPDATA=str(home/'appdata'),LOCALAPPDATA=str(home/'localappdata'),XDG_DATA_HOME=str(home/'data'),XDG_CONFIG_HOME=str(home/'config'))
    for p in ['appdata','localappdata','data','config']:(home/p).mkdir()
    command=[str(engine),'--headless','--path',str(root),'-s','scripts/'+probe+'.gd','--','--touch','--classic-touch-test']
    log=out/(probe+'_native_retry.log')
    with log.open('w',encoding='utf-8') as stream:
        process=subprocess.Popen(command,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT)
        try: code=process.wait(timeout=480)
        except subprocess.TimeoutExpired:
            process.kill();code=process.wait();code='TIMEOUT:'+str(code)
    text=log.read_text(encoding='utf-8',errors='replace')
    row={'probe':probe,'command':command,'exit':code,'elapsed_seconds':time.monotonic()-start,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'last_lines':text.splitlines()[-5:]}
    rows.append(row);(out/'native_probe_retries.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(row),flush=True)
