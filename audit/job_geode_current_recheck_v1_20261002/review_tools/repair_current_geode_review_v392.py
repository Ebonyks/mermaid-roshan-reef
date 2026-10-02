from pathlib import Path
import json,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_current_recheck_v1_20261002'
p=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/record_current_geode_review_v391.py')
(f/'review_tools'/p.name).write_bytes(p.read_bytes())
s=p.read_text().replace('history.mkdir(exist_ok=False)','history.mkdir(exist_ok=True)').replace("['source','pose cell','source object region']","['source','runtime source','pose cell','source object region']")
q=b/'tmp/record_current_geode_review_v392.py';q.write_text(s,encoding='utf-8')
(f/'REVIEW_BUILD_FAILURE_V391.json').write_text(json.dumps(dict(status='PRESERVED_REPAIRED_QA_METADATA_FAILURE',error='Count assertion included two runtime source records as use/action entries; registry unchanged because assertion occurred before its write. Corrected count excludes source and runtime source equally. Every direct image review unchanged.',repair='review_tools/record_current_geode_review_v392.py',intermediate_shell_failure='Quoted inline repair was rejected by Python syntax parser before writing or executing. This saved helper replaces the failed inline command.'),indent=2)+'\n',encoding='utf-8')
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(q)],cwd=b,check=True)
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B','audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v35.py'],cwd=b,check=True)
