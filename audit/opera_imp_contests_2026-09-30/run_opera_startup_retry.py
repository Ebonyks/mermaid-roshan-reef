import os, pathlib, subprocess, tempfile, sys

r=pathlib.Path.cwd()
log=r/'audit/opera_imp_contests_2026-09-30/focused_opera_r4_retry.log'
with tempfile.TemporaryDirectory(prefix='opera_r4_startup_retry_') as fixture:
    native_temp=pathlib.Path(fixture)/'Temp'
    native_temp.mkdir()
    env=os.environ.copy()
    env.update(APPDATA=fixture,LOCALAPPDATA=fixture,TMP=str(native_temp),TEMP=str(native_temp),TMPDIR=native_temp.as_posix())
    with log.open('w',encoding='utf-8') as out:
        result=subprocess.run(['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe',
                               '--headless','-s','scripts/probe_opera.gd','--','--touch','--classic-touch-test'],
                              cwd=r,env=env,stdout=out,stderr=subprocess.STDOUT)
    print('NATIVE_OPERA_RETRY_EXIT',result.returncode,flush=True)
print(log.read_text(encoding='utf-8',errors='replace')[-5000:])
sys.exit(0 if result.returncode==0 else 1)
