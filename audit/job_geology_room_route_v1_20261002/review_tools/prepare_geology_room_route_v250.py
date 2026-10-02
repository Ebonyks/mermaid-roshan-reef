from pathlib import Path
import datetime,hashlib,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geology_room_route_v1_20261002';f.mkdir(exist_ok=False)
prefix=f.relative_to(b).as_posix();bt=chr(96)
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base='c6f03791aee93f1443d423dd50334804e37313fb'
snap=read(b/'audit/job_geode_coherent_runtime_v1_20261002/full_ci_v2/SOURCE_BEFORE.json')['source_files']
assert len(snap)==368 and all(sha(b/x['path'])==x['sha256'] for x in snap)
rules=read(b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json')['rules']
plan=dict(status='CURRENT_NORMAL_ROOM_ROUTE_CAPTURE_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline=base,rules=rules,findings=['MA-PLAY-004','MA-VIS-006','MA-OPERA-012'],scope='Capture current Geologist through actual Library picture-card entry, all four intentional one-finger phases, actual OperaAct completion and ordinary Library return. Capture actual developer elevator entry/cancel separately; no production edits. Source trace shows no Geologist ChapterTwo PHASE_SET and no Geologist two-act stage rollout; do not invent an additional shipping story/training context.',source_files=snap,training_trace=dict(world_phases='scripts/opera_career_world_2d.gd:348',normal_room='scripts/castle_career_routes.gd:23',geology_not_two_act='scripts/opera_performance_plan.gd:8',chapter_two_career_order='scripts/chapter_two_career_scene_adapter.gd:15'),required_evidence=['Native all-phase stills and complete final opening/celebration/return frames at1280/1600','Input-driven arrival and all four phases; actual wrapper callback/normal return','Individual visible object/action opinions; fixture entry limitations','Every source hash unchanged; no claim current fullCI covers new review fixture','Device/child/owner acceptance separate'])
write(f/'PLAN.json',plan)
(f/'.gdignore').write_text('',encoding='utf-8')
(f/'review_tools').mkdir()
s=(b/'audit/job_geode_coherent_runtime_v1_20261002/capture_v2.gd').read_text(encoding='utf-8')
s=s.replace('res://audit/job_geode_coherent_runtime_v1_20261002/attempt_02/','res://'+prefix+'/attempt_01/')
s=s[:s.index('func _run() -> void:')]
start=s.index('func _motion_frame() -> void:');end=s.index('\nfunc _capture(',start)
s=s[:start]+'''func _motion_frame() -> void:
\tvar index := motion_frames.size()
\tvar path := OUT + "native_frames/geode_%d_%04d.webp" % [width_now,index]
\tvar image := root.get_texture().get_image()
\tassert(image.save_webp(path,true) == OK)
\tvar phase := -1
\tvar state: Dictionary = {}
\tif is_instance_valid(motion_world):
\t\tphase = motion_world.phase_index
\t\tif is_instance_valid(motion_world.surface):
\t\t\tstate = (motion_world.surface as OperaGeologySurface).progress_snapshot()
\tmotion_frames.append({"index":index,"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
\t\t"width":width_now,"time_msec":Time.get_ticks_msec(),"surface":state,
\t\t"phase_index":phase,"game":main.game,"room":main.castle_room_id,"act_active":main.opera_game != null,
\t\t"direct_review":false,"scores":{},"owner_acceptance":null})
''' + s[end:]
start=s.index('func _capture(');end=s.index('\nfunc _open(',start)
s=s[:start]+'''func _capture(world: OperaCareerWorld2D, state_name: String) -> void:
\tawait RenderingServer.frame_post_draw
\tvar name := "geologist_%d_phase%d_%s.webp" % [width_now,world.phase_index,state_name]
\tvar path := OUT + "native_views/" + name
\tvar image := root.get_texture().get_image()
\tassert(image.save_webp(path,true) == OK)
\trecords.append({"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
\t\t"phase_index":world.phase_index,"state":state_name,"viewport":[width_now,720],
\t\t"surface":(world.surface as OperaGeologySurface).progress_snapshot(),"direct_review":false,"scores":{}})

func _screen(state_name: String) -> void:
\tawait RenderingServer.frame_post_draw
\tvar path := OUT + "native_views/geologist_%d_%s.webp" % [width_now,state_name]
\tvar image := root.get_texture().get_image()
\tassert(image.save_webp(path,true) == OK)
\trecords.append({"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),
\t\t"state":state_name,"viewport":[width_now,720],"game":main.game,"room":main.castle_room_id,
\t\t"act_active":main.opera_game != null,"direct_review":false,"scores":{}})

func _tap_control(control: Control) -> void:
\tvar at := control.get_global_transform_with_canvas() * (control.size * 0.5)
\tawait _touch(at,true)
\tawait _touch(at,false)
''' + s[end:]
s+='''func _run() -> void:
\tEngine.max_fps = 30
\tassert(DisplayServer.get_name() != "headless")
\tfor arg: String in OS.get_cmdline_user_args():
\t\tif arg.begins_with("--width="):
\t\t\twidth_now = arg.trim_prefix("--width=").to_int()
\troot.size = Vector2i(width_now,720)
\tDisplayServer.window_set_size(root.size)
\tassert(DirAccess.make_dir_recursive_absolute(OUT + "native_views/") == OK)
\tassert(DirAccess.make_dir_recursive_absolute(OUT + "native_frames/") == OK)
\tmain = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
\troot.add_child(main)
\tawait _wait(5)
\tmain.day_one_active = false
\tmain._skip_intro()
\tmain._start_menu_ref()._dismiss_menu()
\tmain.game = "level2"
\tmain._enter_castle_interior_now(false)
\tawait _wait(20)
\tmain._chapter_two_ref().restore_state({})
\tmain.save_data["opera_geology_checkpoint"] = {}
\tvar rooms := main._castle_rooms_ref()
\trooms.show_room("library",false)
\tawait _wait(12)
\tvar routes := main._castle_career_routes_ref()
\troutes.sync()
\tvar slot := -1
\tfor index: int in range(OperaHouse.ACTS.size()):
\t\tif String((OperaHouse.ACTS[index] as Dictionary).get("costume","")) == "geologist":
\t\t\tslot = index
\tassert(slot >= 0 and CastleCareerRoutes.room_for_act(slot) == "library")
\tassert(not ChapterTwoCareerSceneAdapter.CAREER_ORDER.has("geologist"))
\tassert(not OperaPerformancePlan.ENABLED.has("geologist"))
\tvar card := routes.button_for_act(slot)
\tassert(card != null and card.is_visible_in_tree())
\tawait _screen("normal_library_card")
\tawait _tap_control(card)
\tfor tick: int in range(900):
\t\tif main.opera_game != null and main.opera_game.act != null:
\t\t\tbreak
\t\tawait _wait(1)
\tassert(main.opera_game != null and main.opera_game.act != null)
\tvar world: OperaCareerWorld2D = main.opera_game.act.career_world_2d
\tassert(world != null and world.phase_index == 0 and world.phases.size() == 4)
\tassert(not world.using_chapter_two_phases and not world.two_act_enabled)
\tevents.append({"event":"actual_library_picture_card_entry","slot":slot})
\tfor phase: int in range(4):
\t\tassert(world.phase_index == phase)
\t\tawait _open(world)
\t\tawait _work(world)
\t\tif phase < 3:
\t\t\tfor tick: int in range(300):
\t\t\t\tif world.phase_index == phase + 1:
\t\t\t\t\tbreak
\t\t\t\tawait _wait(1)
\t\t\tassert(world.phase_index == phase + 1)
\tfor tick: int in range(600):
\t\tif main.opera_game == null:
\t\t\tbreak
\t\tawait _wait(1)
\tassert(main.opera_game == null and main.game == "level2" and main.castle_room_id == "library")
\tawait _wait(20)
\trecord_motion = false
\tassert(main.castle_room_layer.visible)
\tawait _screen("actual_earned_library_return")
\tevents.append({"event":"actual_earned_completion_library_return","stars":main.opera_stars})
\trooms.show_room("opera_hall",false)
\tawait _wait(12)
\troutes.sync()
\tassert(routes.open_opera_venue())
\tawait _wait(12)
\tvar venue := routes.opera_venue
\tawait _screen("actual_opera_venue")
\tvar elevator := venue.get_node("OperaLeftElevatorPlaytest") as Button
\tawait _tap_control(elevator)
\tawait _wait(8)
\tvar menu := venue.job_playtest_menu
\tassert(menu.session_open and menu.visible)
\tawait _screen("actual_elevator_menu")
\tvar dev_card: Button = null
\tfor button: Button in menu.job_buttons:
\t\tif int(button.get_meta("act_index",-1)) == slot:
\t\t\tdev_card = button
\tassert(dev_card != null)
\tawait _tap_control(dev_card)
\tawait _wait(20)
\tassert(main.opera_game != null and main.opera_game.dev_playtest)
\tawait _screen("actual_dev_geologist_entry")
\tawait _tap_control(main.global_navigation_button)
\tawait _wait(12)
\tassert(main.opera_game == null and menu.visible and menu.session_open)
\tawait _screen("actual_dev_back_menu")
\tvar file := FileAccess.open(OUT + "CAPTURE_%d.json" % width_now,FileAccess.WRITE)
\tfile.store_string(JSON.stringify({"status":"ACTUAL_LIBRARY_ALL4_PHASES_EARNED_RETURN_AND_DEV_ENTRY_CAPTURED_REVIEW_PENDING",
\t\t"views":records,"events":events,"motion_frames":motion_frames,"width":width_now,
\t\t"qualification":"Isolated main/Castle entry fixture and save home; actual Library card/elevator touch, normal phase inputs, production OperaAct callback and earned room return. No forced phases/results/callback patches or source replacement. Geologist has no separate ChapterTwo story set or two-act stage rollout. Not device/child/owner acceptance. Native capture readback slows wall clock."},"\\t"))
\tfile.close()
\tprint("GEOLOGY_ROOM_ROUTE|ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK|",width_now,"|PASS_CAPTURE_REVIEW_PENDING")
\tquit(0)
'''
(f/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-room-route-review-20261002.json'
write(ip,dict(id='job-geology-room-route-review-20261002',scope=plan['scope'],baseline=base,rules=rules,findings=plan['findings'],files=sorted(p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()),validation=[],acceptance_gaps='Current route capture/visual evaluation pending; no new production edits, machine source368 fullCI remains separate; full-job training/story/device/child/owner acceptance and finding lifecycles remain open.'))
print('Prepared exact non-runtime Library-earned return / actual elevator-back review; all368 frozen sources unchanged.')
