"""Run final source/document gates and preserve commands, exits and transcripts."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,py_compile
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[2];E=ROOT/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,args,cwd=REPO):
 r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (E/(name+'.log')).write_bytes(r.stdout);(E/(name+'.err')).write_bytes(r.stderr)
 return {'name':name,'command':args,'cwd':str(cwd),'exit':r.returncode,'stdout_sha256':sha(E/(name+'.log')),'stderr_sha256':sha(E/(name+'.err'))}
def main():
 godot=subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],cwd=REPO,text=True).strip()
 rel=ROOT.relative_to(REPO).as_posix()
 gd=['scripts/probe_opera_2d.gd']+[p.relative_to(REPO).as_posix() for folder in ['scripts','godot'] for p in sorted((ROOT/folder).glob('*.gd'))]
 commands=[('final_gd_parser',[sys.executable,'-m','gdtoolkit.parser',*gd],REPO),('final_inference',[sys.executable,'tools/lint_inference.py',*gd],REPO)]
 for n in gd:
  cwd=ROOT/'godot' if n.startswith(rel+'/godot/') else REPO
  target='res://'+Path(n).name if cwd!=REPO else 'res://'+n
  commands.append(('final_analyzer_'+Path(n).stem,[godot,'--headless','--path',str(cwd),'--check-only','-s',target],cwd))
 commands.extend([('final_authority',[sys.executable,'-B','tools/audit_document_authority.py'],REPO),('final_development',[sys.executable,'-B','tools/audit_development.py','--base','auto'],REPO),('final_whitespace',['git','diff','HEAD','--check'],REPO)])
 # Create every coverage path before inventory; no in-flight output gap.
 for n,a,c in commands:
  for suffix in ['.log','.err']:(E/(n+suffix)).touch()
 (E/'final_gate_receipt.json').write_text('{"pass":null}\n',encoding='utf-8')
 subprocess.run([sys.executable,str(ROOT/'scripts/record_evidence.py')],cwd=REPO,check=True)
 checks=[run(n,a,c) for n,a,c in commands]
 python_files=sorted((ROOT/'scripts').glob('*.py'));errors=[]
 for p in python_files:
  try:py_compile.compile(str(p),doraise=True)
  except py_compile.PyCompileError as ex:errors.append(str(ex))
 receipt={'pass':all(r['exit']==0 for r in checks) and not errors,'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'python_compile':{'files':len(python_files),'errors':errors},'limits':'Source/document checks; local complete 82-probe receipt and published exact-head CI are separate. No device/child/owner acceptance.'}
 (E/'final_gate_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
 subprocess.run([sys.executable,str(ROOT/'scripts/record_evidence.py')],cwd=REPO,check=True)
 print(json.dumps({'pass':receipt['pass'],'checks':[(r['name'],r['exit']) for r in checks],'python_compile_files':len(python_files),'python_errors':errors},indent=2));return 0 if receipt['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
