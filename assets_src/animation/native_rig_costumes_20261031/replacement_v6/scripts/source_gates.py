"""Parse/lint every changed GDScript, and analyze the current native project."""
from pathlib import Path
import json,subprocess,sys,py_compile
R=Path(__file__).resolve().parents[1];REPO=R.parents[3]
def call(args,name):
 p=subprocess.run(args,cwd=REPO,capture_output=True,text=True,encoding='utf-8',errors='replace');(R/'evidence'/f'{name}.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8');return {'command':args,'exit':p.returncode,'log':f'{name}.log'}
def main():
 changed=subprocess.run(['git','diff','--name-only','26bd6d1f0573f7b1ad76511c22abf584e44b7e24','--','*.gd'],cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines()
 changed+=subprocess.run(['git','ls-files','--others','--exclude-standard','--','*.gd'],cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines();changed=sorted(set(changed))
 rows=[call([sys.executable,'-m','gdtoolkit.parser',*changed],'parse_all_changed_v8'),call([sys.executable,'tools/lint_inference.py',*changed],'inference_all_changed_v8')]
 engine=subprocess.run([sys.executable,'tools/resolve_godot.py','--godot','C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'],cwd=REPO,capture_output=True,text=True,check=True).stdout.strip()
 for p in sorted((R/'godot').glob('*.gd')):rows.append(call([engine,'--headless','--path',str(R/'godot'),'--check-only','-s',p.name],'analyzer_current_v8_'+p.stem))
 compiled=[]
 for p in sorted((R/'scripts').glob('*.py')):
  py_compile.compile(str(p),doraise=True);compiled.append(p.name)
 report={'pass':all(x['exit']==0 for x in rows),'changed_gd':changed,'checks':rows,'compiled_python':compiled}
 (R/'evidence/source_gates_v7.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('SOURCE_GATES',report['pass'],len(changed),len(compiled));raise SystemExit(0 if report['pass'] else 1)
if __name__=='__main__':main()
