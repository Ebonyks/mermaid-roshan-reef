from pathlib import Path
import json,hashlib,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');C=R/'audit/job_candy_workflow_current_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
F=C/'attempt02/fixture_originals';F.mkdir(exist_ok=True)
for source,target in [(C/'capture.gd',F/'capture.gd.original'),(C/'review_tools/run_candy_workflow_v489.py',F/'run_candy_workflow_v489.py.original'),(R/'scripts/opera_career_world_2d.gd',F/'production_world.gd.original')]:
 if target.exists():assert target.read_bytes()==source.read_bytes()
 else:shutil.copyfile(source,target)
s=(C/'capture.gd').read_text(encoding='utf-8-sig').replace('attempt02/','entry_diagnostic/')
needle='\tassert(h!=null and h.visible and not world.task_open)'
replacement='''\tif h==null:
\t\tawait _view("unmapped_story_phase_no_activity_opens")
\t\tvar f := FileAccess.open(OUT+"ENTRY_%d.json" % width_now,FileAccess.WRITE)
\t\tf.store_string(JSON.stringify({"status":"UNMODIFIED_STORY_ENTRY_UNMAPPED_PHASE_REPRODUCED","width":width_now,"state":_state(),"armed_station":world.armed_station,"station_for_phase":world.station_for_phase,"station_count":world.station_nodes.size(),"views":views,"events":events,"qualification":"Actual Kitchen card, isolated prior-story save prerequisites, unmodified production. No task opened and no work earned. This diagnostic does not bypass the missing room mapping."},"\\t"))
\t\tf.close()
\t\tprint("CANDY_ENTRY_DIAGNOSTIC|",width_now,"|NO_MAPPED_STATION_REPRODUCED")
\t\tquit(0)
\t\tawait process_frame
\t\treturn
\tassert(h!=null and h.visible and not world.task_open)'''
assert needle in s;s=s.replace(needle,replacement)
p=C/'capture_entry_diagnostic.gd';p.write_text(s,encoding='utf-8',newline='\n')
(C/'entry_diagnostic').mkdir(exist_ok=True)
runner=(C/'review_tools/run_candy_workflow_v489.py').read_text(encoding='utf-8-sig')
runner=runner.replace("runtime_gate_a2","runtime_gate_entry").replace("candy_v489_","candy_v491_").replace("C/'capture.gd'","C/'capture_entry_diagnostic.gd'")
runner=runner.replace("for lane in ('training','story'):","for lane in ('story',):")
a=runner.index(" if label.startswith(('training','story')):\n  cap_path=")
z=runner.index(' write(outputs[2]',a)
runner=runner[:a]+''' if label.startswith('story'):
  cap=read(C/'entry_diagnostic'/('ENTRY_'+label.split('_')[1]+'.json'))
  passed=passed and 'NO_MAPPED_STATION_REPRODUCED' in logs and cap['armed_station']==-1 and not cap['station_for_phase'] and not cap['state']['task_open']
'''+runner[z:]
runner=runner.replace('FOUR_CURRENT_ROUTES_MACHINE_COMPLETE_VISUAL_REVIEW_PENDING','UNMODIFIED_STORY_ENTRY_DIAGNOSTIC_REPRODUCED_NOT_ACTION_ACCEPTANCE')
out=Path(__file__).with_name('run_candy_entry_diagnostic_v491.py');out.write_text(runner,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(R).as_posix() for p in C.rglob('*') if p.is_file()});write(ip,d)
print('CANDY_ENTRY_DIAGNOSTIC|PREPARED|ORIGINAL_A2_PRESERVED')
