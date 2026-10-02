from pathlib import Path
import datetime, hashlib, json, shutil

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
srcdir = r / 'assets_src/imagegen/day2_doctor_wash_reach_v1_20261001'
alpha = json.loads((srcdir / 'ATTEMPT01_ALPHA.json').read_text(encoding='utf-8'))
review = {'id': 'WASH-DOCTOR-REACH-KEY01', 'status': 'SOURCE_FLOOR_CANDIDATE_UNBOUND', 'reviewed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'path': alpha['native_path'], 'sha256': alpha['native_sha256'], 'dimensions': alpha['dimensions'], 'source_score': 4.5, 'identity_score': 4.5, 'work_pose_meaning_source_score': 4.6, 'direct_review': ['Complete generated native RGBA output', 'Original-size neutral white and aqua alpha views'], 'evaluation': 'The child face, curls, pearl flower, rainbow forelock, coral-trim doctor coat, heart satchel, broad rainbow tail and two connected fin lobes remain coherent with the prior draft. Both forearms now reach out from the body; one palm rests visibly on the back of the other hand with a small attached soap cluster. This clearer back-of-hand washing pose addresses the chest-clasp gap. Finger grouping, foam and the side-basin fit still require exact native game-size and whole-action review. Small hair/costume line differences from the preceding source prevent claiming pixel-locked temporal identity.', 'alpha_evaluation': 'Original-size white and aqua views show clean connected outlines and no visible detached colour specks; native hidden RGB and alpha are preserved.', 'method': 'One complete built-in imagegen RGBA source edit; provider and native bytes preserved. No manual subject repair, interpolation or composite delivery frame.', 'provider_path': alpha['provider_path'], 'prompt_sha256': json.loads((srcdir / 'ATTEMPT01_PROMPT.json').read_text(encoding='utf-8'))['prompt_sha256'], 'measured_by_eye_hand_landmarks': {'soap_contact': [684,680], 'lower_hand_tip': [733,739]}, 'mounted_contact_score': None, 'complete_action_score': None, 'runtime_bound': False, 'owner_accepted': False, 'qualification': 'Source-only drafting floor; context, water/rinse/clean consequence, continuous motion, interruption/return, device/child/owner and cinematic gates remain open.'}
(srcdir / 'ATTEMPT01_REVIEW.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8')
page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doctor outward washing reach</title><style>body{font:18px/1.55 system-ui;background:#edf4fa;color:#253447}main{max-width:1100px;margin:auto;padding:24px}img{max-width:100%;height:auto}section{background:white;padding:20px;border-radius:20px;margin:20px 0}p,a{overflow-wrap:anywhere}</style><main><h1>Doctor: outward washing reach</h1><p>Source4.5/5; working-pose meaning4.6/5. Unbound candidate; native side-basin and complete action are pending.</p><p><a href="ATTEMPT01_REVIEW.json">Written evaluation</a> · <a href="ATTEMPT01_PROMPT.json">Prompt and named gap</a> · <a href="../../../../audit/day_two_wash_contact_study_v1_20261001/attempt_03/index.html">Earlier below-floor contact review</a></p><p>'+review['evaluation']+'</p><section><img src="attempt01_native.png" alt="Doctor Roshan reaching outward to wash hands"></section><section><img src="attempt01_review_white.png" alt="Native pose on neutral white"></section><section><img src="attempt01_review_aqua.png" alt="Native pose on neutral aqua"></section><p>'+review['qualification']+'</p></main></html>'
# The source directory is three levels below the root.
page = page.replace('../../../../audit/', '../../../audit/')
(srcdir / 'index.html').write_text(page, encoding='utf-8')

gd = (r / 'tmp/capture_doctor_sink_contact_v44.gd').read_text(encoding='utf-8')
gd = gd.replace('doctor_sink_contact_v44', 'doctor_sink_contact_v58')
a = gd.index('const SOURCES := [')
b = gd.index('class ContactCanvas', a)
gd = gd[:a] + 'const SOURCES := [\n\t"res://'+alpha['native_path']+'",\n]\n' + gd[b:]
gd = gd.replace('var hand_source := Vector2(535.0,594.0)', 'var hand_source := Vector2(733.0,739.0)')
gd = gd.replace('hand_source * (250.0/1402.0)', 'hand_source * (character_rect.size.y/1402.0)')
a = gd.index('\t\tfor source_index: int in range(SOURCES.size()):')
b = gd.index('\t\tassert(main.opera_stars', a)
block = '''		canvas.character=ImageTexture.create_from_image(Image.load_from_file(SOURCES[0]))
		for fit: float in [250.0,300.0]:
			canvas.character_rect=Rect2(25.0,0.0,fit*1122.0/1402.0,fit)
			for extent: float in [140.0,160.0]:
				for offset: float in [0.0,20.0]:
					canvas.sink_extent=extent
					canvas.sink_offset=offset
					canvas.refresh_geometry()
					await _wait(2)
					var ident := "doctor_%d_reach_fit%d_sink%d_offset%d"%[width,int(fit),int(extent),int(offset)]
					await _capture(ident,{"variant":"static_reach_contact_placement","source":SOURCES[0],"source_sha256":FileAccess.get_sha256(SOURCES[0]),"sink_source":"res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png","sink_source_sha256":FileAccess.get_sha256("res://assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png"),"sink_region":[0,0,256,256],"sink_extent":extent,"sink_offset_x":offset,"front_region":[0,116,256,140],"draw_order":"whole_sink_behind_character_then_same_sink_front_region","actor_position":[canvas.position.x,canvas.position.y],"character_rect":[canvas.character_rect.position.x,canvas.character_rect.position.y,canvas.character_rect.size.x,canvas.character_rect.size.y],"hand_source_landmark":[canvas.hand_source.x,canvas.hand_source.y],"hand_local":[canvas.hand.x,canvas.hand.y],"sink_rect":[canvas.sink_rect.position.x,canvas.sink_rect.position.y,canvas.sink_rect.size.x,canvas.sink_rect.size.y]})
'''
gd = gd[:a] + block + gd[b:]
gd = gd.replace('assert(records.size()==14)', 'assert(records.size()==18)').replace('14_CAPTURED', '18_CAPTURED')
target = r / 'tmp/capture_doctor_sink_contact_v58.gd'
assert not target.exists()
target.write_text(gd, encoding='utf-8', newline='\n')
runner = (r / 'tmp/run_closer_sink_contact_v44.py').read_text(encoding='utf-8')
runner = runner.replace('doctor_sink_contact_v44', 'doctor_sink_contact_v58').replace('capture_doctor_sink_contact_v44', 'capture_doctor_sink_contact_v58')
runner = runner.replace("'fb03e0ac3dda1658e9ea188d33cc6e084871642b'", "'56d66f63e375b61cf02936b426a05a2b92c14d3b'")
runner = runner.replace("'assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001/attempt01_native.png']", "'assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001/attempt01_native.png','"+alpha['native_path']+"']")
runner = runner.replace('Three complete authored doctor keys including the clean ending, sink extent180, hand-to-basin offsets0/15px,1280/1600 desktop widths;14 static views.', 'One complete outward-reaching doctor key, uniform figure fits250/300px, reused sink extents140/160px, offsets0/20px,1280/1600 desktop widths;18 static views including2 current originals.')
runner = runner.replace('Complete generated doctor source6 and consecutive key1 unchanged.', 'Complete outward-reaching doctor source unchanged; preceding keys also checked unchanged.')
runpath = r / 'tmp/run_reach_sink_contact_v58.py'
assert not runpath.exists()
runpath.write_text(runner, encoding='utf-8', newline='\n')
shutil.copyfile(__file__, srcdir / 'executed_prepare_reach_sink_contact_v58.py')
lic = r / 'ASSET_LICENSES.md'
s = lic.read_text(encoding='utf-8')
for name in ['attempt01_native.png','attempt01_review_white.png','attempt01_review_aqua.png']:
    rel = (srcdir / name).relative_to(r).as_posix()
    assert rel not in s
    s += '\n| '+rel+' | OpenAI built-in imagegen complete source edit2026-10-01 | Generated for Mermaid Roshan project; provider native retained | '+('None; exact generated native bytes' if name.endswith('native.png') else 'Neutral alpha inspection only, native image unchanged')+' | Outward connected-hand washing gap; source-only4.5, unbound, no context/action/owner acceptance. |\n'
lic.write_text(s, encoding='utf-8', newline='\n')
ip = r / 'design/audit_impacts/job-wash-contact-study-20261001.json'
d = json.loads(ip.read_text(encoding='utf-8'))
d['files'] = sorted(set(d['files']) | {p.relative_to(r).as_posix() for p in srcdir.rglob('*') if p.is_file()})
d['validation'].append({'command':'Native and neutral alpha inspection of outward washing source', 'result':'PASS', 'evidence':(srcdir/'ATTEMPT01_REVIEW.json').relative_to(r).as_posix()+'; source4.5 only, mounted/whole-action pending.'})
d['validation'].append({'command':'Official Godot4.7.2 outward-reach18 native contact capture and individual review', 'result':'PENDING', 'evidence':'tmp/doctor_sink_contact_v58; actual approach then static test-only composition, no production edit or progress.'})
ip.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status':review['status'],'planned_native_views':18,'prepared_script':target.relative_to(r).as_posix(),'production_edits':False}))
