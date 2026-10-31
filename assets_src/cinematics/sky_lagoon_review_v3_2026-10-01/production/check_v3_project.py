import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT.parents[2]
REL=ROOT.relative_to(PROJECT).as_posix()
PY=PROJECT/'build/validation-venv/Scripts/python.exe'
GODOT='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
def write(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def main():
 logs=ROOT/'verification';logs.mkdir(exist_ok=True)
 results=[]
 def run(name,args):
  before=time.monotonic();r=subprocess.run(list(map(str,args)),cwd=PROJECT,capture_output=True,text=True,encoding='utf-8',errors='replace')
  (logs/(name+'.log')).write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
  print(name,'PASS' if r.returncode==0 else 'FAIL',round(time.monotonic()-before,1),'s',flush=True)
  results.append({'check':name,'command':list(map(str,args)),'result':'PASS' if r.returncode==0 else 'FAIL','evidence':REL+'/verification/'+name+'.log'})
  if r.returncode:raise RuntimeError(name)
 run('runtime_source_comparison',['git','diff','origin/dev','--','scripts','scenes','assets','project.godot'])
 assert not (logs/'runtime_source_comparison.log').read_text().strip(),'Unexpected runtime changes'
 run('document_authority',[PY,'-s','-B','tools/audit_document_authority.py'])
 run('document_tests',[PY,'-s','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])
 run('godot_version',[GODOT,'--version'])
 assert (logs/'godot_version.log').read_text().strip()=='4.7.2.stable.official.ed1daf0bf'
 run('godot_import',[GODOT,'--headless','--path',PROJECT,'--import'])
 text=(logs/'godot_import.log').read_text();assert not any(x in text for x in ['ERROR:','SCRIPT ERROR:','Parse Error:']), 'Import diagnostics'
 run('restore_platform_sidecars',[PY,'-s','-B','C:/Users/Peter/Documents/mermaid-roshan-reef/build/local-sky-animation/restore_import_status.py'])
 write(ROOT/'PROJECT_VERIFICATION.json',{'status':'PASS','checks':results,'runtime_changes':'None relative to origin/dev 1e62991ee8db27afe045ed1791d938976762e38d; reference packet excluded by .gdignore','full_game_ci':'Exact new-topic CI required before integration; not inferred from these checks','acceptance_limits':'No runtime visual, device, child, owner or cinematic claim'})
 impact=PROJECT/'design/audit_impacts/sky-lagoon-review-v3-20261001.json';d=json.loads(impact.read_text())
 d['files']=sorted(set(d['files'])|{p.relative_to(PROJECT).as_posix() for p in ROOT.rglob('*') if p.is_file()})
 d['validation'][2]={'command':'authority, 52 authority/development tests, exact 4.7.2 import, empty runtime-source comparison','result':'PASS','evidence':REL+'/PROJECT_VERIFICATION.json and verification/*.log'}
 write(impact,d)
 run('development_coverage',[PY,'-s','-B','tools/audit_development.py','--base','auto'])
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(PROJECT).as_posix() for p in ROOT.rglob('*') if p.is_file()});write(impact,d)
 run('development_coverage_origin_dev',[PY,'-s','-B','tools/audit_development.py','--base','origin/dev'])
 write(ROOT/'PROJECT_VERIFICATION.json',{'status':'PASS','checks':results,'runtime_changes':'None relative to origin/dev 1e62991ee8db27afe045ed1791d938976762e38d; packet excluded by .gdignore','full_game_ci':'Exact new-topic CI required before integration','acceptance_limits':'Machine reference-only checks; no runtime/owner/device/child/cinematic acceptance'})
 print('Project reference gates PASS.',flush=True)
if __name__=='__main__':main()
