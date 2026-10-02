from pathlib import Path
import datetime, json, shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geology_river_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
out=b/'audit/job_artwork_refinement_live'
for src,dst in [('ALL_ITEMS.json','ALL_ITEMS_V25.json'),('all_items.html','all_items_V25.html')]:
 if not (out/dst).exists():shutil.copyfile(out/src,out/dst)
code=(b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v25.py').read_text(encoding='utf-8').replace('build_current_job_item_register_v25.py','build_current_job_item_register_v26.py')
addition='''
# V26 current runtime copies remain complete-source scores, not averaged mount passes.
runtime_prefix='audit/job_geology_river_runtime_v1_20261002'
runtime=read(runtime_prefix+'/ARTWORK_ITEMS.json')
runtime_review=read(runtime_prefix+'/REVIEW.json')
for x in runtime['items']:
 p=x['path']
 items[p]=dict(id=x['id'],aliases=[],kind='source',path=p,earlier_sha256=x['sha256'],historical_source_score=x['complete_source_score'],evaluation='Exact complete runtime-copy source; selected visible region '+str(x['visible_region_score'])+'/5 is separate from complete-source '+str(x['complete_source_score'])+'/5. Unused closed connectors and generated red port fringes retain failed source scores.',refinement='Current actual-route open/final rendering reviewed at both widths; full timed/arbitrary join/contact/room/training/story and owner approval remain separate.',families=['Geologist river','Bound reversible topic runtime copy'],original_reports=[runtime_prefix+'/index.html'],source_qualification=runtime['qualification'],preview_path=p,native_reference_observations=[],runtime_binding_state=x['runtime_binding_state'],latest_refinement=dict(report=runtime_prefix+'/index.html',note='All46 actual native route stills directly inspected. Visible bed4.6/joined network4.5 provisional. Room2.8/contact2.7 remain weak. Exact six mechanics unchanged; full suite receipt separately linked.',evidence=x))
for q in items.values():
 if q['id'].startswith('GEO-RIVER-'):
  q['latest_refinement']=dict(report=runtime_prefix+'/index.html',note='Current reversible game renderer now binds six exact complete-source copies. Every46 actual four-phase still reviewed at both widths. Selected visible joins4.5 provisional/earth4.6; source A2/A3 red-fringe4.4 and A4/A5 glow3.8 remain rejected outside selected join planes/runtime. Room2.8/contact2.7, continuous action/training/story/device/child/owner/global acceptance remain open.')
'''
needle="for q in items.values():\n p=q['path']";assert code.count(needle)==1;code=code.replace(needle,addition+'\n'+needle)
code=code.replace('six first river candidates and eight dry/wet junctions','six first river candidates and30 dry/wet/junction source components')
p=b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v26.py';p.write_text(code,encoding='utf-8',newline='\n')
# Extend exact scoped gate commands with every new study fixture and direct renderer fixture.
code=(f/'review_tools/run_geology_river_gates_v216.py').read_text(encoding='utf-8').replace('run_geology_river_gates_v216.py','run_geology_river_gates_v219.py')
fixtures=['audit/job_river_join_study_v1_20261001/'+s+str(v)+'.gd' for v in [5,6,7] for s in ['join_surface_v','capture_join_study_v']]+['audit/job_geology_river_runtime_v1_20261002/capture_production_river_network.gd']
needle="assert action in commands";code=code.replace(needle,"commands['parser'] += "+repr(fixtures)+"\ncommands['inference'] += "+repr(fixtures)+"\ncommands['networkanalyzer']=[godot,'--headless','--path',str(r),'--check-only','--script','audit/job_geology_river_runtime_v1_20261002/capture_production_river_network.gd']\nfor w in [1280,1600]:\n commands['network'+str(w)]=[godot,'--path',str(r),'-s','audit/job_geology_river_runtime_v1_20261002/capture_production_river_network.gd','--','--width='+str(w),'--touch','--classic-touch-test']\n"+needle)
code=code.replace("if arg.startswith('capture'):","if arg.startswith(('capture','network1280','network1600')):")
code=code.replace("if arg.startswith('capture') or action == 'import':","if arg.startswith(('capture','network1280','network1600')) or action == 'import':")
(f/'review_tools/run_geology_river_gates_v219.py').write_text(code,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-river-painted-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}|{p.relative_to(b).as_posix()});write(ip,d)
print('V26 builder and exact actual-renderer network fixtures/gates prepared.')
