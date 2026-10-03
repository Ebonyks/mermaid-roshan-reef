from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');C=R/'audit/job_candy_workflow_current_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
F=C/'attempt01/fixture_originals';F.mkdir(exist_ok=False)
shutil.copyfile(C/'capture.gd',F/'capture.gd.original')
shutil.copyfile(C/'review_tools/run_candy_workflow_v486.py',F/'run_candy_workflow_v486.py.original')
shutil.copyfile(R/'scripts/opera_career_world_2d.gd',F/'production_world.gd.original')
p=C/'capture.gd';s=p.read_text(encoding='utf-8-sig');assert 'attempt01/' in s
s=s.replace('attempt01/','attempt02/').replace('world.phases.size()==(4 if story else 6)','world.phases.size()==4').replace('phase==(2 if story else 3)','phase==2')
p.write_text(s,encoding='utf-8',newline='\n');(C/'attempt02').mkdir()
plan=read(C/'PLAN.json');plan['scope']=plan['scope'].replace('all6 normal/freeplay phases','all4 normal/freeplay phases');plan['correction']='The failed A1 fixture incorrectly expected the obsolete six-phase LEGACY table. The current PHASES table contains4 Candy Maker phases, with circle/WRAP at2. Actual entry correctly loaded4, and the assertion stopped before any phase was opened/worked. Original fixture, raw logs and the captured Kitchen card are preserved. A2 uses the current4-phase table; both lanes circle at2. No production change or game failure is inferred.';write(C/'PLAN.json',plan)
write(C/'FIXTURE_CORRECTION_V488.json',{'status':'A1_INCORRECT_PHASE_COUNT_ASSERTION_PRESERVED_A2_CORRECTED','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'failed_receipt':'runtime_gate_a1/training_1280.receipt.json','original_fixture':'attempt01/fixture_originals/capture.gd.original','original_fixture_sha256':sha(F/'capture.gd.original'),'corrected_fixture_sha256':sha(p),'cause':plan['correction'],'raw_failure_preserved':True,'production_edits':0,'owner_acceptance':None})
ip=R/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=read(ip);d['id']=d.pop('task');d['scope']=plan['scope'];d['validation'][0]['evidence']=C.relative_to(R).as_posix()+'/FIXTURE_CORRECTION_V488.json';d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in C.rglob('*') if x.is_file()});write(ip,d)
runner=(C/'review_tools/run_candy_workflow_v486.py').read_text(encoding='utf-8-sig')
runner=runner.replace("runtime_gate_a1","runtime_gate_a2").replace("candy_v486_","candy_v489_").replace("C/'attempt01'","C/'attempt02'").replace("expected=set(range(4 if lane=='story' else 6))","expected=set(range(4))")
old="with outputs[0].open('wb') as out,outputs[1].open('wb') as err:result=subprocess.run(command,cwd=R,env=env,stdout=out,stderr=err,timeout=900,creationflags=subprocess.CREATE_NO_WINDOW)"
new="""with outputs[0].open('wb') as out,outputs[1].open('wb') as err:
  process=subprocess.Popen(command,cwd=R,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  while process.poll() is None:
   time.sleep(0.5)
   current='\\n'.join(x.read_text(encoding='utf-8',errors='replace') for x in outputs[:2])
   if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed',current) or time.monotonic()-t>600:
    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    break
  result=subprocess.CompletedProcess(command,process.wait())"""
assert old in runner;runner=runner.replace(old,new)
out=Path(__file__).with_name('run_candy_workflow_v489.py');out.write_text(runner,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
print(json.dumps({'status':'FRESH_A2_FIXTURE_PREPARED_CURRENT4_PHASES','failed_attempt_preserved':True,'production_edits':0}))
