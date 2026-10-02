from pathlib import Path
import datetime, json, shutil, subprocess, sys

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v10.py'
s=f.read_text(encoding='utf-8');old='individual_pose_cells=len(cells)';assert s.count(old)==1
s=s.replace(old,"individual_pose_cells=sum(q['kind']=='pose cell' for q in rows)")
f.write_text(s,encoding='utf-8',newline='\n')
d=r/'audit/job_shared_source_native_review_v1_20261001'
correction={'status':'FIXED_UNPUBLISHED_POSE_COUNT_CALCULATION','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_v10_count':240,'actual_pose_rows':328,'cause':'Inherited len(cells) measured original240 Opera cells before88 shared cells were inserted into items. Replaced by exact final row-kind count. No art or score changes.','previous_registered_entries':1518,'first_shell_attempt':'PowerShell rejected incorrectly nested quotes before the count correction ran; helper-file retry preserves literal Python and performs the change.'}
(d/'REGISTER_COUNT_CORRECTION.json').write_text(json.dumps(correction,indent=2)+'\n',encoding='utf-8')
run=subprocess.run([sys.executable,'-X','utf8','-B',str(f)],cwd=r,capture_output=True,text=True)
(r/'tmp/register_v10_count_retry.stdout.log').write_text(run.stdout,encoding='utf-8');(r/'tmp/register_v10_count_retry.stderr.log').write_text(run.stderr,encoding='utf-8');assert run.returncode==0,run.stderr
x=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8'))
assert x['counts']['individual_pose_cells']==sum(v['kind']=='pose cell' for v in x['items'])==328
assert x['counts']['unique_source_files']+328+x['counts']['additional_runtime_prop_regions']==1518
print(json.dumps(x['counts']))
shutil.copyfile(__file__,d/'executed_fix_register_pose_count_v63.py')
ip=r/'design/audit_impacts/job-shared-native-source-review-20261001.json';q=json.loads(ip.read_text(encoding='utf-8'));q['files']=sorted(set(q['files'])|{p.relative_to(r).as_posix() for p in d.rglob('*') if p.is_file()});ip.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
