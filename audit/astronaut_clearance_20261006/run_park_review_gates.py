from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time
root=Path(__file__).resolve().parents[2];packet=Path(__file__).resolve().parent
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
version=subprocess.check_output([str(engine),'--version'],text=True).strip();assert version=='4.7.2.stable.official.ed1daf0bf'
impact=json.loads((root/'design/audit_impacts/astronaut-clearance-20261006.json').read_text(encoding='utf-8-sig'))
gds=[n for n in impact['files'] if n.endswith('.gd') and (root/n).is_file()]
log=packet/'PARK_REVIEW_GATES_LOG.txt';receipt=packet/'PARK_REVIEW_GATES_RECEIPT.json';assert not log.exists() and not receipt.exists()
names=gds+['.gitattributes','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md','tools/audit_document_authority.py','tools/audit_development.py','tools/audit_game_2d.py','audit/astronaut_clearance_20261006/run_park_review_gates.py']
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
commands=[('All changed GDScript parser',[sys.executable,'-B','-m','gdtoolkit.parser',*gds]),('All changed GDScript inference',[sys.executable,'-B','tools/lint_inference.py',*gds])]
for n in ['scripts/opera_astronaut_surface.gd','scripts/opera_career_world_2d.gd','scripts/save_state.gd','scripts/probe_opera_gesture_quality.gd']:
 commands.append(('Analyzer '+n,[str(engine),'--headless','--path',str(root),'--script','res://'+n,'--check-only']))
commands += [('Document authority',[sys.executable,'-B','tools/audit_document_authority.py']),('Authority/development unit',[sys.executable,'-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development']),('Authority stress',[sys.executable,'-B','tools/audit_document_authority.py','--stress']),('2D regression',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate']),('Audit impact coverage',[sys.executable,'-B','tools/audit_development.py','--base','auto']),('Whitespace',['git','diff','--check','HEAD'])]
started=utc();t=time.monotonic();steps=[]
with log.open('xb') as out:
 for label,cmd in commands:
  out.write(('\nSTEP '+label+'\n').encode());out.flush()
  process=subprocess.Popen(cmd,cwd=root,stdout=out,stderr=subprocess.STDOUT)
  print(json.dumps({'label':label,'owned_pid':process.pid}),flush=True)
  timeout=False
  try:process.wait(timeout=max(1,240-(time.monotonic()-t)))
  except subprocess.TimeoutExpired:timeout=True;process.terminate();process.wait(timeout=15)
  steps.append({'label':label,'command':cmd,'owned_pid':process.pid,'exit_code':process.returncode,'timed_out':timeout})
  if timeout:break
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
errors=[l for l in lines if any(x in l for x in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]
matched=all(sha(root/s['path'])==s['sha256'] for s in sources)
passed=len(steps)==len(commands) and all(s['exit_code']==0 and not s['timed_out'] for s in steps) and not errors and matched
value={'result':'PASS' if passed else 'FAIL','started_utc':started,'finished_utc':utc(),'status':'TERMINAL','engine_version':version,'engine_sha256':sha(engine),'sources':sources,'source_bindings_still_match':matched,'steps':steps,'elapsed_seconds':round(time.monotonic()-t,2),'changed_gd_count':len(gds),'errors':errors,'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'impact_input_sha256':sha(root/'design/audit_impacts/astronaut-clearance-20261006.json'),'impact_envelope_binding':'At gate check time; later appending this result changes the envelope, not bound runtime or authority sources.','meaning':'Current-source parser/inference,4runtime analyzers,authority/unit/stress,2D no-regression,exact staged coverage and whitespace only. Full scripts/ci.sh/native visual/device/child/owner pending; strict zero2D remains unsatisfied.'}
receipt.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'result':value['result'],'failed_steps':[s['label'] for s in steps if s['exit_code']!=0 or s['timed_out']],'errors':errors[:5],'changed_gds':len(gds),'elapsed_seconds':value['elapsed_seconds'],'source_bindings_still_match':matched,'receipt_sha256':sha(receipt)}),flush=True)
sys.exit(0 if passed else 1)
