from pathlib import Path
import json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geology_painted_work_v1_20261001'
source=(r/'audit/job_geode_runtime_v1_20261001/review_tools/run_geode_full_ci_v2.py').read_text()
source=source.replace('job_geode_runtime_v1_20261001','job_geology_painted_work_v1_20261001').replace('job-geode-painted-runtime-20261001','job-geology-painted-work-20261001').replace('full_ci_v2','full_ci_v1').replace('painted-geode production full suite2','painted-work production full suite1')
source=source.replace("root/'audit/job_art_current_source_reconciliation_20261001/SOURCE_BEFORE_CI.json'", "root/'audit/job_geode_runtime_v1_20261001/full_ci_v2/SOURCE_BEFORE.json'")
source=source.replace("  write(folder/'SOURCE_BEFORE.json'", "  paths.update(['scripts/opera_hotspot_catalog.gd','scripts/opera_world_hotspot_2d.gd','audit/job_geology_painted_work_v1_20261001/capture_geology_painted_work.gd'])\n  paths.update(p.relative_to(root).as_posix() for p in (root/'assets/opera/worlds/geology/painted_work_v1_20261001').rglob('*') if p.is_file())\n  write(folder/'SOURCE_BEFORE.json'")
source=source.replace('actual painted geode and visible celebration-rest repair plus current pool/boxing/character family','actual seven painted-work runtime sources, four changed production scripts and current capture plus established painted geode/pool/boxing/character family')
source=source.replace('inheritedG suite','inheritedH suite')
target=f/'review_tools/run_geology_work_full_ci_v177.py';assert not target.exists();target.write_text(source,encoding='utf-8')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
p=r/'design/audit_impacts/job-geology-painted-work-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in f.rglob('*') if x.is_file()});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Fresh unmodified official full-suite runner staged; H result cannot validate changed current production.')
