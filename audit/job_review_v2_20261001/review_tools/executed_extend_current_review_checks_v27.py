from pathlib import Path
import datetime,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
family=r/'audit/job_review_v2_20261001'
root=r/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03'
review=json.loads((root/'REVIEW_V3.json').read_text(encoding='utf-8'))
assert review['frames']==2074
status=json.loads((root/'STATUS.json').read_text(encoding='utf-8'))
status.update(status='PROCESS_PASS_PARTIAL_FOUR_DOCTOR_KEYS_REVIEWED',machine_capture='Eight actual viewport hotspot/hold/advance cases completed with unchanged source hashes, natural process/render timing and no star awards.',visual_review='Four doctor-training1280 keys directly reviewed: workflow2.7, spatial contact2.3, surface2.9. Other2070 native frames and seven other whole cases remain unreviewed.',evidence='REVIEW_V3.json; native_frames/CAPTURE_RECEIPT.json; PROFILE.json; PROCESS.json',updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(root/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8',newline='\n')
src=(family/'review_tools/check_distinct_review_resources_v6.py').read_text(encoding='utf-8')
src=src.replace('resource_checks_v5','resource_checks_v6').replace('check_distinct_review_resources_v6.py','check_distinct_review_resources_v7.py')
src=src.replace("pages=['audit/job_review", "pages=['audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03/index.html','assets_src/imagegen/day2_doctor_wash_motion_v1_20261001/index.html','audit/job_review")
needle="def head(p):"
addition="root=json.loads((r/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03/FRAME_VIEWER_DATA_V3.json').read_text(encoding='utf-8'))\npaths.update('audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03/native_frames/'+x['path'] for x in root['frames'])\n"
assert needle in src
src=src.replace(needle,addition+needle)
checker=family/'review_tools/check_distinct_review_resources_v7.py'
assert not checker.exists();checker.write_text(src,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,family/'review_tools/executed_extend_current_review_checks_v27.py')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{checker.relative_to(r).as_posix(),'audit/job_review_v2_20261001/review_tools/executed_extend_current_review_checks_v27.py'})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
result=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(checker)],cwd=r)
raise SystemExit(result.returncode)
