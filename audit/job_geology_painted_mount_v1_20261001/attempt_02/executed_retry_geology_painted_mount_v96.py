from pathlib import Path
import json,shutil,datetime
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old=r/'audit/job_geology_painted_mount_v1_20261001';failure=dict(status='PREPARATION_FAILED_BEFORE_ANY_GATE_OR_NATIVE_CAPTURE',error='TypeError reading dict source snapshot as a list; actual source list is source_files. No production files or source snapshot modified.',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(old/'PREPARATION_FAILURE.json').write_text(json.dumps(failure,indent=2)+'\n',encoding='utf-8',newline='\n')
source=(old/'executed_run_geology_painted_mount_v95.py').read_text(encoding='utf-8')
source=source.replace("out=r/'audit/job_geology_painted_mount_v1_20261001';assert not out.exists();out.mkdir()","out=r/'audit/job_geology_painted_mount_v1_20261001/attempt_02';assert not out.exists();out.mkdir()")
source=source.replace("before={x['path']:sha(r/x['path']) for x in bound}","before={x['path']:sha(r/x['path']) for x in bound['source_files']}")
source=source.replace('tmp/geology_painted_mount_v95/native_views','tmp/geology_painted_mount_v96/native_views').replace('executed_run_geology_painted_mount_v95.py','executed_retry_geology_painted_mount_v96.py')
exec(compile(source,str(Path(__file__)),'exec'))
