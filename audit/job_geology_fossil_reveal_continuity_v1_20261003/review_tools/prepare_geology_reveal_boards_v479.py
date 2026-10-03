from pathlib import Path
import json,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003'
source=(R/'audit/job_geology_painted_fracture_trial_v1_20261003/review_tools/prepare_geology_fracture_boards_v463.py').read_text(encoding='utf-8-sig')
source=source.replace("J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'","J=R/'audit/job_geology_fossil_reveal_continuity_v1_20261003'").replace('job-geology-painted-fracture-trial-20261003.json','job-geology-fossil-reveal-continuity-20261003.json').replace('Explicit non-runtime inherited draw-only fracture trial, original pixels and mechanics.','Explicit non-runtime reveal/home placement study; same painted raster and contours, changed homes and stage0 underlying drawing, inherited targets/input/state/progress/world callbacks.')
compile(source,'build_geology_reveal_boards_v479.py','exec')
target=J/'review_tools/build_geology_reveal_boards_v479.py';assert not target.exists();target.write_text(source,encoding='utf-8',newline='\n');shutil.copyfile(target,Path(__file__).with_name('build_geology_reveal_boards_v479.py'))
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-fossil-reveal-continuity-20261003.json';d=json.loads(ip.read_text(encoding='utf-8-sig'));d['rules']=sorted(set(d['rules'])|{'DL-AGE-01','DL-AGE-02'});d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('REVEAL_BOARDS_HELPER_PREPARED_NO_VISUAL_SCORE')
