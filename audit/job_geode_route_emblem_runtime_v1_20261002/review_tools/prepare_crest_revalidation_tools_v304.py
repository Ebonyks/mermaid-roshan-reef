from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002';rt=f/'review_tools'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
source=(rt/'run_geode_route_full_ci_v285.py').read_text(encoding='utf-8')
source=source.replace('full_ci_v1','full_ci_v2').replace('372','373').replace('full suite1','full suite2')
p=rt/'run_geode_route_full_ci_v305.py';assert not p.exists();compile(source,str(p),'exec');p.write_text(source,encoding='utf-8',newline='\n')
for old,new in [('prepare_geode_route_boards_v282.py','prepare_geode_route_boards_v306.py'),('prepare_geode_route_native_still_boards_v284.py','prepare_geode_route_native_still_boards_v307.py')]:
 s=(rt/old).read_text(encoding='utf-8').replace('attempt_01','attempt_02').replace('capture{width}v1','capture{width}v2').replace('372','373').replace('BOARD_MANIFEST_{width}.json','BOARD_MANIFEST_V2_{width}.json').replace('STILL_BOARD_MANIFEST.json','STILL_BOARD_MANIFEST_V2.json')
 s=s.replace(";shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)",";\nif Path(__file__).resolve() != (f/'review_tools'/Path(__file__).name).resolve():shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)")
 p=rt/new;assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),rt/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in rt.iterdir() if p.is_file()});write(ip,d)
print('Prepared fresh373-source suite2 and both-width full-frame boards; all prior files untouched.')
