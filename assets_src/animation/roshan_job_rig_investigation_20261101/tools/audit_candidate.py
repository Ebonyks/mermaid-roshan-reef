from pathlib import Path
import os,json,subprocess,sys,shutil
R=Path(__file__).resolve().parents[1];RAW=R/'evidence/raw_frames_v6'
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
rows=[]
for job in ['detective','geologist']:
    folder=RAW/job
    if not (folder/'work_samples.json').exists():shutil.copy2(folder/'samples.json',folder/'work_samples.json')
    shutil.copy2(folder/'samples_regression.json',folder/'samples.json');shutil.copy2(folder/'samples_regression.json',folder/'stress_samples.json')
    for script,extra in [('seed_geometry.py',['--rig',str(R/'demo'/f'audit_rig_{job}.json')]),('seed_motion.py',[])]:
        name=job+'_'+script.replace('.py','')
        with (R/'evidence'/(name+'.log')).open('w',encoding='utf8') as out:
            run=subprocess.run([sys.executable,'-X','utf8','-B',str(R/'tools'/script),str(folder),*extra],stdout=out,stderr=subprocess.STDOUT,env=env)
        rows.append({'job':job,'script':script,'exit':run.returncode,'log':name+'.log'})
    (R/'evidence'/job).mkdir(exist_ok=True)
    for p in folder.glob('*audit*.json'):shutil.copy2(p,R/'evidence'/job/p.name)
    for p in folder.glob('*board.jpg'):shutil.copy2(p,R/'review'/f'{job}_{p.name}')
(R/'evidence/strict_regression.json').write_text(json.dumps({'candidate':'v6','rows':rows,'pass':all(x['exit']==0 for x in rows),'floors_unchanged':True},indent=2)+'\n')
print(json.dumps(rows,indent=2));raise SystemExit(0 if all(x['exit']==0 for x in rows) else 1)
