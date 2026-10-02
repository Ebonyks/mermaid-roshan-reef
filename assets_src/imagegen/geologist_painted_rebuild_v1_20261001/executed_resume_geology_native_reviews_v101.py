from pathlib import Path
import json, shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
previous=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/record_geology_native_reviews_v100.py')
preserve=r/'audit/job_geode_embedded_mount_v2_20261001/report_preparation_attempt_01'
preserve.mkdir(exist_ok=True)
shutil.copyfile(previous,preserve/'executed_record_geology_native_reviews_v100.py')
(preserve/'FAILURE.json').write_text(json.dumps(dict(status='PREPARATION_FAILURE',failed_action='Opening existing ASSET_LICENSES.md for whole-file write',exception='OSError errno22 invalid argument; license file exists and remained8429113bytes',captured_images_unchanged=True,recovery='Resume verified archive bytes and append only missing license rows; do not repeat generation/native capture.'),indent=2)+'\n',encoding='utf-8')
body=previous.read_text(encoding='utf-8')
body=body.replace("assert not dest.exists();dest.mkdir()", "dest.mkdir(exist_ok=True)")
body=body.replace("if license_lines:license_path.write_text(license_text+'\\n'+ '\\n'.join(license_lines)+'\\n',encoding='utf-8',newline='\\n')", "if license_lines:\n with license_path.open('a',encoding='utf-8',newline='\\n') as license_stream: license_stream.write('\\n'+'\\n'.join(license_lines)+'\\n')")
body=body.replace("executed_record_geology_native_reviews_v100.py", "executed_resume_geology_native_reviews_v101.py")
exec(compile(body,str(previous),'exec'))
