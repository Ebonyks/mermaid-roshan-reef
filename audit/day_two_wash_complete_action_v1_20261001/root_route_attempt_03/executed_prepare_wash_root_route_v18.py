from pathlib import Path
import hashlib,json,re,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
t=Path(__file__).parent
family=r/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03'
assert not family.exists(),'Preserve previous attempts.'
family.mkdir()
shutil.copyfile(t/'capture_wash_root_route_v3.gd',r/'tmp/capture_wash_root_route_v3.gd')
shutil.copyfile(t/'capture_wash_root_route_v3.gd',family/'executed_capture_wash_root_route_v3.gd')
old=(r/'audit/day_two_wash_complete_action_v1_20261001/local_hold_attempt_02/executed_run_complete_wash_v2.py').read_text(encoding='utf-8')
code=old.replace('wash_complete_action_v2','wash_root_route_v3').replace('capture_complete_wash_v2','capture_wash_root_route_v3')
code=code.replace('actual training/birthday doctor/nursery complete washing fixtures, original unchanged artwork and real local GUI press/controller30Hz ticks, passive start through earned completion and next-phase arming. No ordinary root route or creative/device/child/owner acceptance.','actual training/birthday doctor/nursery room fixtures; original unchanged artwork, viewport touch, production approach and natural clocks with measured timestamps. Main/menu room arrival remains a fixture; no complete visual/device/child/owner acceptance.')
code=code.replace('Eight actual training/birthday doctor/nursery complete washing fixtures, original unchanged artwork and real local GUI press/controller30Hz ticks, passive start through earned completion and next-phase arming. No ordinary root route or creative/device/child/owner acceptance.','Eight actual training/birthday doctor/nursery room fixtures; original unchanged artwork, viewport touch, production approach and natural clocks with measured timestamps. Main/menu room arrival remains a fixture; no complete visual/device/child/owner acceptance.')
code=code.replace('Original unchanged artwork in a local-input/manual-tick fixture; process checks only.','Original unchanged artwork in a viewport-input/natural-clock fixture; process checks only.').replace('No complete played action/route/device/child/owner acceptance.','No complete visual, full menu/story-route, target-device, child or owner acceptance.')
code=code.replace('PASS_ORIGINAL_LOCAL_INPUT_NATIVE_CAPTURE','PASS_ORIGINAL_VIEWPORT_ROUTE_NATIVE_CAPTURE')
code=code.replace('full_ci_candidate_v1/SOURCE_BEFORE.json','full_ci_candidate_retry_v2/SOURCE_BEFORE.json')
code=code.replace('timeout=300','timeout=900')
assert "_gui_input" not in (r/'tmp/capture_wash_root_route_v3.gd').read_text(encoding='utf-8')
assert '_open_task(' not in (r/'tmp/capture_wash_root_route_v3.gd').read_text(encoding='utf-8')
runner=r/'tmp/run_wash_root_route_v3.py';runner.write_text(code,encoding='utf-8',newline='\n')
shutil.copyfile(runner,family/'executed_run_wash_root_route_v3.py')
shutil.copyfile(__file__,family/'executed_prepare_wash_root_route_v18.py')
(family/'STATUS.json').write_text(json.dumps(dict(status='PREPARED_NOT_EXECUTED',scope='Eight unchanged-source actual career-room washing routes via viewport hotspot/wash touches and natural process/render timing. Main/menu entry remains fixture setup.',prior_evidence='local_hold_attempt_02 preserved:1520 manual-tick frames,108 selected keys directly reviewed; no ordinary approach/timing acceptance.'),indent=2)+'\n',encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in family.rglob('*') if p.is_file()})
d['scope']+=' Prepare a separate unchanged-source viewport-touch/natural-clock washing route fixture; earlier direct-open/manual-tick evidence remains preserved, and execution/visual acceptance are pending.'
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
log=(r/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/stdout.log').read_text(encoding='utf-8',errors='replace')
probes=re.findall(r'^PROBE (\w+) process exit: (\d+)',log,re.M)
print(json.dumps(dict(prepared=family.relative_to(r).as_posix(),completed_probe_processes=len(probes),failed_probe_processes=[p for p,c in probes if int(c)!=0],latest_probe=probes[-1] if probes else None)))
