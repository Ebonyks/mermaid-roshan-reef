from pathlib import Path
import json,subprocess,sys,os,time,hashlib
R=Path(__file__).resolve().parents[2];out=R/'evidence/verification_v3';folder=out/'raw/legacy/boxer';rig=out/'rig_boxer.json';reports={};rows=[];f=json.loads((R/'evidence/frozen_candidate_v3.json').read_text());assert all(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in f['files'])
for mesh in json.loads(rig.read_text())['meshes']:
 name=mesh['name'];p=folder/('geometry_audit_'+name+'.json');reused=p.exists();log=out/('resume_boxer_'+name+'.log');start=time.monotonic();code=0
 if not reused:
  args=[sys.executable,str(R/'tools/audit_study.py'),str(folder),'--rig',str(rig),'--mesh',name]
  with log.open('w',encoding='utf-8') as stream:
   try:result=subprocess.run(args,stdout=stream,stderr=subprocess.STDOUT,env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONUTF8='1'),timeout=600);code=result.returncode
   except subprocess.TimeoutExpired:code=124
 if p.exists():reports[name]=json.loads(p.read_text())
 rows.append({'mesh':name,'reused_exact_completed_subreport':reused,'exit':code,'seconds':round(time.monotonic()-start,2),'report':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,'pass':p.exists() and reports[name]['machine_geometry_pass']});(out/'boxer_geometry_resume.json').write_text(json.dumps({'scope':'Resume only unfinished meshes after original1200second wrapper timeout; original FAIL retained. Same frozen inputs, native frames, unchanged audit functions and floors. No completed subreport repeated.','rows':rows,'complete':len(rows)==len(json.loads(rig.read_text())['meshes']),'pass':all(x['pass'] for x in rows)},indent=2)+'\n');print(name,'reuse' if reused else code,rows[-1]['pass'],flush=True)
if len(reports)==len(json.loads(rig.read_text())['meshes']):
 report={'meshes':reports,'machine_geometry_pass':all(x['machine_geometry_pass'] for x in reports.values()),'scope':'All exact frozenv3 meshes, resumed unchanged audit after wrapper timeout; timeout remains an independently failed execution record.'};(out/'boxer_geometry_audit_resumed.json').write_text(json.dumps(report,indent=2)+'\n')
