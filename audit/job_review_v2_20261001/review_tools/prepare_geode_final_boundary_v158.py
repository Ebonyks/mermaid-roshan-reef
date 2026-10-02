from pathlib import Path
import json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geode_runtime_v1_20261001';impact=r/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=json.loads(impact.read_text(encoding='utf-8'))
d['scope']+=' The old cheer row starts with a detached held sample. For the geode final/ending only, reuse the existing complete clapping cheer cell1 as an intentional static celebration, so the reveal does not imply extracting an extra crystal. Preserve attempt02 raw36 views; re-run full actual viewport route in attempt03 at both widths. No new character pixels or artificial animation. The first full-suite preparation failed before running because tools/.gdignore means no UID sidecar is generated; preserve the preparation error and snapshot only actual files in suite2.'
d['files']=[p for p in d['files'] if p!='tools/capture_geode_runtime_route.gd.uid']
d['files']=sorted(set(d['files'])|{'audit/job_review_v2_20261001/review_tools/prepare_geode_final_boundary_v158.py','audit/job_geode_runtime_v1_20261001/full_ci_v1/PREPARE_FAILURE.json','audit/job_geode_runtime_v1_20261001/review_tools/run_geode_full_ci_v2.py'})
write(impact,d)
write(out/'full_ci_v1/PREPARE_FAILURE.json',{'status':'FAILED_PREPARATION_SUITE_NOT_STARTED','command':'run_geode_full_ci_v1.py --prepare','process_exit':1,'error':'FileNotFoundError: tools/capture_geode_runtime_route.gd.uid','cause':'tools/.gdignore prevents automatic UID creation; source snapshot must include actual files, not invent a sidecar.','suite_started':False,'qualification':'This is a preparation failure, not a passing or failed trusted82-probe run.'})
p=r/'scripts/opera_career_world_2d.gd';s=p.read_text(encoding='utf-8');needle='\tif player_animator.current_animation != animation:\n\t\tplayer_animator.play(animation)'
assert s.count(needle)==1
s=s.replace(needle,'\tif career_id == "geologist" and animation == "cheer" and phase_index >= 3:\n\t\t# Celebrate the rooted interior with the existing clapping pose. The\n\t\t# sample-in-hand first cheer cell would imply another extracted crystal.\n\t\tplayer_animator.show_pose("cheer", 1)\n\t\treturn\n'+needle,1);p.write_text(s,encoding='utf-8',newline='\n')
p=r/'tools/capture_geode_runtime_route.gd';s=p.read_text(encoding='utf-8').replace('/attempt_02/','/attempt_03/');p.write_text(s,encoding='utf-8',newline='\n')
p=out/'review_tools/run_geode_full_ci_v2.py';s=(out/'review_tools/run_geode_full_ci_v1.py').read_text(encoding='utf-8').replace("folder=family/'full_ci_v1'","folder=family/'full_ci_v2'").replace('audit/job_geode_runtime_v1_20261001/full_ci_v1','audit/job_geode_runtime_v1_20261001/full_ci_v2').replace(",'tools/capture_geode_runtime_route.gd.uid'",'').replace('production full suite1','production full suite2');p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),r/'audit/job_review_v2_20261001/review_tools/prepare_geode_final_boundary_v158.py')
print('Geode uses existing clapping pose; prior actual captures and failed suite preparation preserved. Final source boundary ready.')
