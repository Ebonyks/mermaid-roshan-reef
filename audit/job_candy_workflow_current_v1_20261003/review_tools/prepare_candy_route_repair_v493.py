from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');C=R/'audit/job_candy_workflow_current_v1_20261003';N=R/'assets_src/imagegen/candy_wrap_states_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert all(read(C/f'runtime_gate_entry/story_{w}.receipt.json')['status']=='PASS' for w in (1280,1600))
P=C/'attempt03';P.mkdir(exist_ok=False)
ip=R/'design/audit_impacts/job-candy-workflow-current-20261003.json';impact=read(ip)
impact['scope']+=' Reproduce and repair the four missing Chapter2 Candy physical-station bindings; reuse existing pitcher/berry/tray invitation artwork. Preserve original failed route before editing; no phase, input, save, goal or completion alteration. One fresh text-only transparent wrapping-state atlas fills the independently observed flat-shape/material-causality gap; unbound until source and action review.'
impact['files']=sorted(set(impact['files'])|{'scripts/opera_career_world_2d.gd','assets_src/imagegen/candy_wrap_states_v1_20261003/PLAN.json','assets_src/imagegen/candy_wrap_states_v1_20261003/PROMPT.txt'})
impact['validation'].append({'command':'Two unmodified actual Chapter2 Candy Kitchen-entry diagnostics','result':'PASS','evidence':C.relative_to(R).as_posix()+'/runtime_gate_entry/story_1280.receipt.json; story_1600.receipt.json. Reproduced no station mapping, no opened activity and no earned work. This is diagnostic evidence, not action acceptance.'})
write(ip,impact)
world=R/'scripts/opera_career_world_2d.gd';original=sha(world);assert world.read_bytes()==(C/'attempt02/fixture_originals/production_world.gd.original').read_bytes()
s=world.read_text(encoding='utf-8-sig')
old='\t"candymaker": {"SYRUP": "gumball_vat", "SORT": "taffy_press", "WRAP": "candy_bag_cottage", "SHARE": "candy_cart"},'
new='''\t"candymaker": {
\t\t"SYRUP": "gumball_vat", "SORT": "taffy_press", "WRAP": "candy_bag_cottage", "SHARE": "candy_cart",
\t\t"COAT STRAWBERRIES": "gumball_vat", "SORT STRAWBERRIES": "taffy_press",
\t\t"GLAZE STRAWBERRIES": "candy_bag_cottage", "PLACE ON CAKE": "candy_cart",
\t},'''
assert old in s;s=s.replace(old,new,1)
old='\tvar spec: Dictionary = HotspotCatalog.spec(career_id, invitation_name)'
new='''\tvar spec: Dictionary = HotspotCatalog.spec(career_id, invitation_name)
\tif _is_chapter2_candymaker_scene():
\t\t# Story ingredients retain their identity; the freeplay candy bag/wrapper
\t\t# cannot invite a strawberry-glazing or cake-placement activity.
\t\tspec = _chapter2_candy_hotspot_spec(phase_name)'''
assert old in s;s=s.replace(old,new,1)
needle='\n\nfunc _clear_hotspot_intent() -> void:'
addition='''

func _chapter2_candy_hotspot_spec(phase_name: String) -> Dictionary:
\tvar berry_path := "res://assets/chapter2/birthday/sky_lagoon_strawberry_single.png"
\tmatch phase_name:
\t\t"COAT STRAWBERRIES":
\t\t\treturn HotspotCatalog.spec("candymaker", "SYRUP")
\t\t"SORT STRAWBERRIES", "PLACE ON CAKE":
\t\t\treturn {"path": berry_path, "motion": "bounce", "size": Vector2(104, 104), "presentation": "overlay"}
\t\t"GLAZE STRAWBERRIES":
\t\t\treturn {"path": "res://assets/chapter2/birthday/chapter2_candied_strawberries_tray.png",
\t\t\t\t"motion": "pulse", "size": Vector2(144, 144), "presentation": "overlay"}
\treturn {}
'''
assert needle in s;s=s.replace(needle,addition+needle,1);world.write_text(s,encoding='utf-8',newline='\n')
fixture=C/'capture.gd';s=fixture.read_text(encoding='utf-8-sig').replace('attempt02/','attempt03/');fixture.write_text(s,encoding='utf-8',newline='\n')
boundary=read(C/'SOURCE_CURRENT_BEFORE_CAPTURE.json');changes=[]
for x in boundary['source_files']:
 actual=sha(R/x['path'])
 if actual!=x['sha256']:changes.append({'path':x['path'],'baseline_sha256':x['sha256'],'capture_sha256':actual});x['sha256']=actual
assert changes==[{'path':'scripts/opera_career_world_2d.gd','baseline_sha256':original,'capture_sha256':sha(world)}]
boundary['status']='A3_CAPTURE_SOURCE_BOUNDARY_ONE_DECLARED_CANDY_ROUTE_REPAIR';boundary['declared_changes_from_U']=changes;write(C/'SOURCE_CURRENT_A3_BEFORE_CAPTURE.json',boundary)
write(C/'ROUTE_REPAIR_V493.json',{'status':'FOUR_STORY_STATIONS_REPAIRED_CAPTURE_PENDING','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':'c5977ebb29bb2011b20fc149ad350290f045045c','production_original':'attempt02/fixture_originals/production_world.gd.original','changes':changes,'diagnostics':['entry_diagnostic/ENTRY_1280.json','entry_diagnostic/ENTRY_1600.json'],'scope':'Four name-to-landmark bindings and exact story ingredient invitations only. All original freeplay keys retained. Input, goals, saves, progress, story order, masks, callback and art bytes unchanged. Not a graphics-quality pass.','owner_acceptance':None})
runner=(C/'review_tools/run_candy_workflow_v489.py').read_text(encoding='utf-8-sig').replace('runtime_gate_a2','runtime_gate_a3').replace('candy_v489_','candy_v494_').replace("C/'attempt02'","C/'attempt03'").replace('SOURCE_CURRENT_BEFORE_CAPTURE.json','SOURCE_CURRENT_A3_BEFORE_CAPTURE.json').replace('all783_production_sources_unchanged','all783_declared_capture_source_hashes_unchanged')
needle="for lane in ('training','story'):"
extra="""commands.extend([
 ('parser_world',[py,'-X','utf8','-B','-m','gdtoolkit.parser',str(R/'scripts/opera_career_world_2d.gd')]),
 ('inference_world',[py,'-X','utf8','-B','tools/lint_inference.py',str(R/'scripts/opera_career_world_2d.gd')]),
 ('analyzer_world',[godot,'--headless','--path',str(R),'--check-only','--script',str(R/'scripts/opera_career_world_2d.gd')]),
 ('chapter2_probe',[godot,'--headless','--path',str(R),'-s','scripts/probe_chapter2.gd']),
 ('chapter2_farmer_resume_probe',[godot,'--headless','--path',str(R),'-s','scripts/probe_chapter2_farmer_resume.gd']),
 ('opera2d_probe',[godot,'--headless','--path',str(R),'-s','scripts/probe_opera_2d.gd'])])
"""
assert needle in runner;runner=runner.replace(needle,extra+needle,1)
runner=runner.replace("SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource|Unable to convert a value","SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource|Unable to convert a value|\\\\bFAIL\\\\b")
out=Path(__file__).with_name('run_candy_route_repair_v494.py');out.write_text(runner,encoding='utf-8',newline='\n')
N.mkdir(exist_ok=False)
prompt='''Use case: illustration-story. Asset type: one transparent 2D gameplay wrapping-state atlas, four images of the SAME candy and SAME piece of paper, arranged in a clean 2x2 square grid, no labels, no dividers. Each quadrant has ample transparent gutters and its candy centered at the same scale, horizontal long axis, identical softly elevated front view. This is a polished painted children's storybook game, rounded toy forms, broad painted value bands, subtle gouache texture, dark plum authored contours, aqua/lavender shadows, warm pastel gold wrapper and coral-pink oval sweet. Never flat vector graphics, photorealism, shiny 3D rendering or diagram style.
Top left: unwrapped coral oval sweet rests ON one broad pale-gold rectangular wax-paper sheet, visibly open around it. Top right: the SAME sheet has its upper and lower long edges folded over the middle of that SAME sweet, overlapping paper visibly covering its belly, left and right ends still broad and open. Bottom left: the SAME paper completely covers the body; two continuous open paper end fans extend left and right from the covered body, connected through pinched necks. Bottom right: the SAME covering paper body and attached end fans, both necks now properly twisted tight, with two small visible diagonal twist creases at each neck. The candy silhouette/scale/orientation and paper colour stay consistent across all four stages. Clear paper continuity: each end must attach to the central wrapper, never loose triangles floating beside it. Candy must stay concealed under the completed wrapper. No extra sweets, hands, face, shells, jewel, swirl, rings, glitter, floor, tabletop, shadow cast on an opaque background, text, numbers, watermark, logo or frame. Genuine transparent background everywhere outside the four isolated painted wrapping stages. Target 1024x1024 atlas.'''
(N/'PROMPT.txt').write_text(prompt+'\n',encoding='utf-8',newline='\n')
plan=read(C/'PLAN.json');write(N/'PLAN.json',{'baseline':plan['baseline'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rules':plan['rules'],'findings':plan['findings'],'named_gap':'Direct native current wrapping shows unchanged flat oval, detached rotating gold polygons and no paper coverage. Existing crank and mover have a whole decorative swirl, baked guide/line and only one already-wrapped state; candy bag is a different object. None supplies the required open/fold/cover/twist causal paper states.','reuse_inventory':[x for x in plan['reuse_inventory'] if any(q in x['path'] for q in ['crank_candymaker','goal_candymaker'])],'input_reference_images':[],'generation':'Fresh text-only built-in imagegen; no protected or blocked reference upload. Transparent 2x2 gameplay state atlas. This is static authored gameplay source, not cinematic delivery or accepted motion.','prompt_sha256':sha(N/'PROMPT.txt'),'required_evidence':'Complete native raster/alpha, each individual state, inter-state material continuity, bounded source scores and technical dimensions; any source candidate >=4.5 stays unbound until full actual action/contact/display review. Preserve every rejected attempt.','predicted_score':None,'owner_acceptance':None})
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
impact=read(ip);impact['files']=sorted(set(impact['files'])|{x.relative_to(R).as_posix() for x in C.rglob('*') if x.is_file()}|{x.relative_to(R).as_posix() for x in N.rglob('*') if x.is_file()});write(ip,impact)
print(json.dumps({'status':'A3_ROUTE_REPAIR_AND_FRESH_TEXT_ONLY_WRAP_ATLAS_PLAN_PREPARED','production_changes':changes,'prompt':prompt}))
