from pathlib import Path
import datetime,hashlib,json,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_geology_complete_actions_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert read(F/'runtime_gate/capture1280.receipt.json')['status']=='FAIL_PRESERVED'
old=F/'capture.gd';assert not (F/'capture_attempt01.gd.original').exists()
shutil.copyfile(old,F/'capture_attempt01.gd.original')
s=old.read_text(encoding='utf-8').replace('/attempt01/','/attempt02/')
s=s.replace('var record_motion := false','var record_motion := false\nvar observed_work_completion := false')
needle='\tfor step: int in range(1, 11):\n\t\tawait _drag'
assert s.count(needle)==1
s=s.replace(needle,'\tfor step: int in range(1, 11):\n\t\tif observed_work_completion:\n\t\t\treturn\n\t\tawait _drag')
needle='func _work(world: OperaCareerWorld2D) -> void:\n\tvar surface := world.surface as OperaGeologySurface\n'
assert s.count(needle)==1
s=s.replace(needle,needle+'''\tvar requested_phase := world.phase_index
\tvar requested_mode := surface.mode
\tvar completion_record: Dictionary = {}
\tobserved_work_completion = false
\tsurface.gesture.connect(func(kind: String, amount: float, quality: float) -> void:
\t\tcompletion_record["kind"] = kind
\t\tcompletion_record["amount"] = amount
\t\tcompletion_record["quality"] = quality
\t\tcompletion_record["phase_at_event"] = world.phase_index
\t\tcompletion_record["pending_at_event"] = world.phase_advance_pending
\t\tcompletion_record["surface_at_event"] = surface.progress_snapshot()
\t\tcompletion_record["time_msec"] = Time.get_ticks_msec()
\t\tobserved_work_completion = true
\t, CONNECT_ONE_SHOT)
''')
needle='\tassert(surface._completion_emitted and world.phase_advance_pending)\n'
assert s.count(needle)==1
s=s.replace(needle,'''\tassert(completion_record.get("kind", "") == requested_mode)
\tassert(is_equal_approx(float(completion_record.get("amount", 0.0)), 1.0))
\tassert(is_equal_approx(float(completion_record.get("quality", 0.0)), 1.0))
\tassert(int(completion_record.get("phase_at_event", -1)) == requested_phase)
\tassert(bool(completion_record.get("pending_at_event", false)))
\tassert(bool((completion_record.get("surface_at_event", {}) as Dictionary).get("complete", false)))
''')
needle='\tawait _capture(world, "earned_completion")\n\tevents.append({"event":"intentional_completed","phase_index":world.phase_index,"progress":surface.progress()})'
assert s.count(needle)==1
s=s.replace(needle,'''\tif world.phase_index == requested_phase:
\t\tawait _capture(world, "earned_completion")
\telse:
\t\tawait _screen("phase_%d_earned_completion_already_advanced" % requested_phase)
\tevents.append({"event":"intentional_completed","phase_index":requested_phase,
\t\t"phase_at_capture_exit":world.phase_index,"completion_record":completion_record})''')
old.write_text(s,encoding='utf-8',newline='\n')
write(F/'CAPTURE_RETRY_PLAN_V436.json',{'status':'PREPARED_BEFORE_RETRY','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'failed_receipt':'runtime_gate/capture1280.receipt.json','failed_fixture':'capture_attempt01.gd.original','failed_fixture_sha256':sha(F/'capture_attempt01.gd.original'),
 'cause':'Readback-delayed PAN sequence advances to phase3 before the inherited end-of-work assertion examines the reused/reset surface. Failed run contains449 native frames and remains a failed whole-capture result, despite eventual return. No green process/printed route token overrides the SCRIPT ERROR.',
 'repair':'Non-runtime capture only: listen once to the real production gesture completion event; strictly require exact requested mode, amount1, quality1, correct phase, actual pending flag and complete snapshot at that event. Stop further synthetic drag segments after observing that event. Preserve actual phase advancement; do not force phase, patch callbacks, hold timers, input owners, production or probes. Label a selected post-advance canvas honestly rather than calling it the previous phase earned-completion image.',
 'changed_fixture_sha256':sha(old),'new_output':'attempt02','production_edits':False,'blocking_capture_checks_unchanged':['Process exit0','No SCRIPT ERROR/Parse Error/Compile Error/Assertion failed/Failed loading resource','Every783 exact production hash unchanged','All four intentional completions, actual earned Library return and Opera elevator/Back events'],'visual_acceptance':None})
src=F/'review_tools/run_geology_complete_actions_v434.py'
runner=src.read_text(encoding='utf-8')
runner=runner.replace("outputs=[G/(label+'.'+s)","outputs=[G/(label+'_a2.'+s)")
runner=runner.replace("'_v434'","'_v437'")
runner=runner.replace("F/'attempt01'","F/'attempt02'")
needle="cap=read(receipt_path)\n   passed=passed and"
assert runner.count(needle)==1
runner=runner.replace(needle,"cap=read(receipt_path)\n   passed=passed and {e.get('phase_index') for e in cap['events'] if e.get('event')=='intentional_completed'}=={0,1,2,3}\n   passed=passed and")
dest=R/'tmp/run_geology_complete_actions_v437.py';assert not dest.exists();dest.write_text(runner,encoding='utf-8',newline='\n')
shutil.copyfile(dest,F/'review_tools'/dest.name)
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-complete-actions-20261003.json';imp=read(ip)
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()})
imp['validation'].append({'command':'Preserved first capture failure and real-event-bound helper-only retry','result':'PENDING','evidence':(F/'CAPTURE_RETRY_PLAN_V436.json').relative_to(R).as_posix()});write(ip,imp)
print('GEOLOGY_CAPTURE_RETRY_PREPARED|real completion event required|failed original preserved|production unchanged')
