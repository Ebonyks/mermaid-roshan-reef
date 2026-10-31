from pathlib import Path
import json,sys,subprocess,time
p=Path(__file__).resolve().parents[1];r=p.parents[2];rows=[];start=time.monotonic()
commands=[('tools.audit_document_authority',[]),('tools.audit_development',['--base','auto'])]
with (p/'environment/project_gates.log').open('w',encoding='utf-8') as log:
 for module,tail in commands:
  # Embedded ._pth Python intentionally omits cwd; explicitly expose this exact repository.
  entry=module.replace('.','/')+'.py'
  code='import sys,runpy;sys.path.insert(0,'+repr(str(r))+');sys.argv='+repr([entry]+tail)+';runpy.run_module('+repr(module)+',run_name="__main__")'
  actual=[sys.executable,'-X','utf8','-B','-c',code]
  result=subprocess.run(actual,cwd=r,capture_output=True,text=True,encoding='utf-8')
  requested='python -B '+entry+(' '+' '.join(tail) if tail else '')
  log.write('COMMAND '+requested+'\n'+result.stdout+result.stderr+'\n')
  rows.append({'command':requested,'actual_argv':actual,'embedded_python_path_setup':'Exact repository inserted in sys.path; no validator changes','exit_code':result.returncode,'result':'PASS' if result.returncode==0 else 'FAIL'});print(rows[-1]['command'],rows[-1]['result'],flush=True)
j={'status':'PASS' if all(x['exit_code']==0 for x in rows) else 'FAIL','checks':rows,'elapsed_seconds':round(time.monotonic()-start,3)}
(p/'environment/project_gates.json').write_text(json.dumps(j,indent=2)+'\n')
raise SystemExit(0 if j['status']=='PASS' else 1)
