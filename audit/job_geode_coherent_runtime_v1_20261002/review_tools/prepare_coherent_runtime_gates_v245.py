from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geode_coherent_runtime_v1_20261002';prefix=f.relative_to(b).as_posix()
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
s=(f/'capture.gd').read_text().replace('"pull":surface.geode_pull,','"pull":surface.geode_pull,"authored_state":surface._geode_state_index(),')
(f/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
s=(b/'audit/job_geode_coherent_pilot_v1_20261002/review_tools/run_coherent_pilot_gates_v236.py').read_text()
s=s.replace('audit/job_geode_coherent_pilot_v1_20261002',prefix).replace('job-geode-coherent-opening-20261002.json','job-geode-coherent-runtime-20261002.json').replace('run_coherent_pilot_gates_v236.py','run_coherent_runtime_gates_v245.py').replace('geode_coherent_pilot_','geode_coherent_runtime_')
gds=['scripts/opera_geology_surface.gd',prefix+'/capture.gd']
commands=dict(parser=[py,'-X','utf8','-B','-m','gdtoolkit.parser']+gds,inference=[py,'-X','utf8','-B','tools/lint_inference.py']+gds,importart=[godot,'--headless','--path',str(b),'--import'],analyzer=[godot,'--headless','--path',str(b),'--check-only','--script',prefix+'/capture.gd'],authority=[py,'-X','utf8','-B','tools/audit_document_authority.py'],development=[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'],audit2d=[py,'-X','utf8','-B','tools/audit_game_2d.py'])
for width in [1280,1600]:commands['capture'+str(width)]=[godot,'--path',str(b),'-s',prefix+'/capture.gd','--','--width='+str(width),'--touch','--classic-touch-test']
start=s.index('commands=');end=s.index('\nassert action',start);s=s[:start]+'commands='+repr(commands)+s[end:]
s=s.replace("action == 'import'","action == 'importart'").replace('assets/opera/worlds/geology/painted_river_v1_20261002','assets/opera/worlds/geology/coherent_geode_v1_20261002').replace("timeout=360 if arg.startswith('capture') else 240","timeout=360 if arg.startswith('capture') else 360")
(f/'review_tools/run_coherent_runtime_gates_v245.py').write_text(s,encoding='utf-8',newline='\n')
s=(b/'audit/job_geology_river_runtime_v1_20261002/review_tools/run_geology_river_full_ci_v216.py').read_text()
s=s.replace("family=root/'audit/job_geology_river_runtime_v1_20261002'","family=root/'audit/job_geode_coherent_runtime_v1_20261002'")
s=s.replace('job-geology-river-painted-runtime-20261002.json','job-geode-coherent-runtime-20261002.json').replace('audit/job_geology_painted_work_v1_20261001/full_ci_v1/SOURCE_BEFORE.json','audit/job_geology_river_runtime_v1_20261002/full_ci_v1/SOURCE_BEFORE.json')
needle="paths={r['path'] for r in previous['source_files']}"
s=s.replace(needle,needle+"\n paths.update('assets/opera/worlds/geology/coherent_geode_v1_20261002/'+name+suffix for name in ['opening_six_states.png','opening_bridge.png'] for suffix in ['', '.import'])\n paths.add('audit/job_geode_coherent_runtime_v1_20261002/capture.gd')")
s=s.replace('audit/job_geology_river_runtime_v1_20261002/full_ci_v1/process.exit','audit/job_geode_coherent_runtime_v1_20261002/full_ci_v1/process.exit').replace('painted-work production full suite1','coherent-geode production full suite1')
(f/'review_tools/run_coherent_geode_full_ci_v245.py').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});ip.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Actual renderer captures, scoped gates and fresh unmodified complete-suite runner prepared.')
