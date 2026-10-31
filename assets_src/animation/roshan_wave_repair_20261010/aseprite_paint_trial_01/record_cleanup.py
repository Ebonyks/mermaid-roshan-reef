"""Record actual local timestamps; no pixels or campaign/job file mutations."""
from pathlib import Path
import json
from datetime import datetime,timezone
base=Path(__file__).resolve().parent
utc=lambda t:datetime.fromtimestamp(t,timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
now=datetime.now(timezone.utc);start=(base/'paint_connected.lua').stat().st_ctime
passes=[]
for folder in sorted((p for p in base.iterdir() if p.is_dir() and (p/'joint_geometry.json').exists()),key=lambda p:p.stat().st_ctime):
    data=json.loads((folder/'joint_geometry.json').read_text(encoding='utf-8-sig'))
    masters=list(folder.glob('*.aseprite'))
    passes.append({'pass':folder.name,'first_directory_creation_utc':utc(folder.stat().st_ctime),
        'execution_start_utc':data.get('run_started_utc'),'execution_end_utc':data.get('run_finished_utc'),
        'execution_wall_seconds':data.get('run_wall_seconds'),
        'master_write_completed_utc':utc(max(p.stat().st_mtime for p in masters)) if masters else None,
        'time_evidence':'Aseprite instrumented execution times where present; filesystem directory/master timestamps are explicitly proxies otherwise',
        'generated_api_calls':0,'gpu_jobs':0,'external_cost':0})
record={'schema':'reef.aseprite-local-cleanup-time.v1','tracked_working_interval_start_utc':utc(start),
    'tracked_working_interval_end_utc':now.isoformat(timespec='seconds').replace('+00:00','Z'),
    'tracked_contiguous_working_wall_minutes':round((now.timestamp()-start)/60,3),
    'start_evidence':'Windows creation timestamp of the first direct-paint Lua recipe; actual timestamp, not a fabricated retrospective clock',
    'scope':'This contiguous interval conservatively includes authoring, native visual review, cleanup pilots, failed drafts and local execution/wait; these pass times are not summed again',
    'untracked_pre_start_limit':'Earlier conversation/geometry planning before first recipe creation is not separately clocked here; parent campaign ledger must include any previously recorded cleanup and other agents',
    'task_cleanup_cap_minutes':180,'generated_api_calls':0,'gpu_jobs':0,'external_monetary_cost':0,'passes':passes,'human_acceptance':False}
(base/'cleanup_time_ledger.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'tracked_start':record['tracked_working_interval_start_utc'],'tracked_end':record['tracked_working_interval_end_utc'],
    'tracked_cleanup_wall_minutes':record['tracked_contiguous_working_wall_minutes'],'passes':len(passes)}))
