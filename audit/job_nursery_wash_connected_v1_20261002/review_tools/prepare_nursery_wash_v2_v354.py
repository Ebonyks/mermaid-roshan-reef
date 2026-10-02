from pathlib import Path
import json,hashlib,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002'
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert json.loads((F/'candidate_capture_v1/PROCESS_RECEIPT.json').read_text())['source_unchanged']
for name in ['baseline_capture','candidate_capture_v1']:
    write(F/name/'CLAIM_CORRECTION.json',{'status':'EXECUTED_TEMPLATE_PROSE_QUALIFIED','reason':'The copied runner retained historical original-artwork/eight-birthday wording. Baseline is unchanged HEAD artwork; candidate_v1 is newly bound connected draft relative to HEAD. Both use four direct training and four Chapter2 authored CATALOG room fixtures, not ordinary birthday routes. Source_before/after are literal current artifacts and remain preserved. Candidate index_tree is only the Git index, not the untracked rendered candidate source; rely on literal hashes.','no_inherited_acceptance':True,'normal_root_menu_route':False,'complete_career_callback':False,'target_device_child_owner_acceptance':False})
N=R/'scripts/opera_nursery_surface.gd';original=N.read_text();(F/'surface_candidate_v1.gd.txt').write_text(original,encoding='utf-8')
replacement='const WASH_FILES: Array[String] = ["ready", "wet", "rub_palm02", "rub_back", "rinse", "clean"]\n'
text=original.replace('var wash_textures: Array[Texture2D] = []',replacement+'var wash_textures: Array[Texture2D] = []').replace('for state: String in WASH_STATES:\n\t\t\twash_textures.append(load(WASH_ROOT + state + ".png") as Texture2D)','for filename: String in WASH_FILES:\n\t\t\twash_textures.append(load(WASH_ROOT + filename + ".png") as Texture2D)')
assert text!=original
N.write_text(text,encoding='utf-8')
normal='''extends SceneTree

func _initialize() -> void:
	var image: Image = Image.load_from_file("res://assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/native.png")
	assert(not image.is_empty())
	image.resize(1024, 1024, Image.INTERPOLATE_LANCZOS)
	assert(image.save_png("res://assets/opera/worlds/nursery/wash_connected_v1_20261002/rub_palm02.png") == OK)
	print("NURSERY_WASH|PALM02_WHOLE_CANVAS_NORMALIZATION|PASS")
	quit(0)
'''
(F/'review_tools/normalize_runtime_v354.gd').write_text(normal,encoding='utf-8')
fixture=(F/'review_tools/capture_candidate_v350.gd').read_text().replace('/candidate_capture_v1/native_frames/','/candidate_capture_v2/native_frames/').replace('for career: String in ["doctor","nursery"]:','for career: String in ["nursery"]:').replace('PASS_EIGHT_NATIVE_ROOM_ROUTES','PASS_FOUR_NATIVE_ROOM_ROUTES')
needle='\t\t\t\t\tif world.phase_advance_pending and accepted<0:'
insert='''					if opened>=0 and tick==opened+35 and wash_pressed:
						_touch(wash_point,false)
						wash_pressed = false
						event = "viewport_midwash_pause"
					if opened>=0 and tick==opened+50:
						_touch(wash_point,true)
						wash_pressed = true
						event = "viewport_midwash_resume"
'''
assert fixture.count(needle)==1;fixture=fixture.replace(needle,insert+needle)
fixture=fixture.replace('No direct task-open or manual controller ticks.','No direct task-open or manual controller ticks.')
(R/'tmp/capture_nursery_wash_candidate_v354.gd').write_text(fixture,encoding='utf-8')
(F/'review_tools/capture_candidate_v354.gd').write_text(fixture,encoding='utf-8')
run=(F/'review_tools/run_candidate_v350.py').read_text().replace('/candidate_capture_v1\'','/candidate_capture_v2\'').replace('capture_nursery_wash_candidate_v350.gd','capture_nursery_wash_candidate_v354.gd')
run=run.replace('Eight actual training/birthday doctor/nursery room fixtures; original unchanged artwork','Four Nursery direct training/authored Chapter2 catalog room fixtures; connected painted candidate v2 fixed-layout states').replace('candidate_tree','index_tree_not_rendered_source').replace('Original currently bound artwork captured without replacement.','Current newly bound candidate v2 artwork relative to HEAD; original and candidate_v1 sequences preserved.').replace('Original unchanged artwork in a viewport-input/natural-clock fixture','Newly bound candidate v2 artwork in a viewport-input/natural-clock catalog fixture').replace('No production source edited.','Production source was edited before this frozen run, never during it.')
(F/'review_tools/run_candidate_v354.py').write_text(run,encoding='utf-8')
with (R/'ASSET_LICENSES.md').open('a',encoding='utf-8') as out:out.write('| `assets/opera/worlds/nursery/wash_connected_v1_20261002/rub_palm02.png` | Native palm-contact attempt02 above | Project generated art; OpenAI terms | https://openai.com/policies/terms-of-use/ | Uniform whole-canvas 1280to1024 POT normalization, alpha preserved. Original rub_palm.png and candidate_v1 evidence retained; no runtime/source quality transfer. |\n')
impactp=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';impact=json.loads(impactp.read_text());impact['files']=sorted(set(impact['files'])|{'assets/opera/worlds/nursery/wash_connected_v1_20261002/rub_palm02.png','assets/opera/worlds/nursery/wash_connected_v1_20261002/rub_palm02.png.import'}|{p.relative_to(R).as_posix() for parent in [F,R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'] for p in parent.rglob('*') if p.is_file()})
impact['validation'] += [{'command':'Fresh unchanged eight-case baseline capture','result':'PASS','evidence':'audit/job_nursery_wash_connected_v1_20261002/baseline_capture/PROCESS_RECEIPT.json; template prose qualified separately.'},{'command':'Direct all Nursery baseline action review','result':'FAIL','evidence':'audit/job_nursery_wash_connected_v1_20261002/baseline_visual/DIRECT_REVIEW.json; 1051consecutiveframes/24boards, absent subject through earned progress.'},{'command':'Candidate_v1 eight-case frozen route/input capture','result':'PASS','evidence':'audit/job_nursery_wash_connected_v1_20261002/candidate_capture_v1/PROCESS_RECEIPT.json; no complete visual/owner acceptance; clasp source4.4 replaced by palm02.'}]
write(impactp,impact)
print('Prepared corrected palm02 binding and four-case pause/resume fixture. Candidate1 source freeze passed; history retained.')
