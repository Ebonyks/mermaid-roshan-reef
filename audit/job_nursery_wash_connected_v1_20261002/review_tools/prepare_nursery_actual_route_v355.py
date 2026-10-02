from pathlib import Path
import json
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002'
gd='''extends SceneTree
## Isolated initial Main/Castle entry and save home; actual Bubble Bath picture
## card, production OperaHouse caller, hotspot approach, wash hold and Back route.
## Partial career exit after earned WASH, never a full-career reward claim.
const OUT := "res://audit/job_nursery_wash_connected_v1_20261002/actual_route_v2/"
var main: ReefMain
var world: OperaCareerWorld2D
var width_now := 1280
var recording := false
var frames: Array[Dictionary] = []
var images: Array[Image] = []
var events: Array[Dictionary] = []
var views: Array[Dictionary] = []


func _initialize() -> void:
	_run.call_deferred()


func _wait(count: int) -> void:
	for _index: int in range(count):
		await process_frame
		if recording:
			await RenderingServer.frame_post_draw
			var image: Image = root.get_texture().get_image()
			images.append(image)
			var alive := is_instance_valid(world)
			var wash: OperaNurserySurface = world.surface as OperaNurserySurface if alive else null
			frames.append({"index":frames.size(),"path":"native_frames/nursery_%d_%04d.webp" % [width_now,frames.size()],
				"ticks_usec":Time.get_ticks_usec(),"phase":world.phase_index if alive else -1,
				"progress":world.phase_progress if alive else 0.0,
				"task_open":alive and world.task_open,"accepted":alive and world.phase_advance_pending,
				"wash_state":wash.wash_state if wash != null else "none",
				"held":wash != null and wash.held,
				"route_actor_visible":alive and world.player_actor.visible,
				"game":main.game,"room":main.castle_room_id,"stars":main.opera_stars})


func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = at
	event.pressed = pressed
	Input.parse_input_event(event)
	await _wait(2)


func _tap(control: Control) -> void:
	assert(control != null and control.is_visible_in_tree())
	var at := control.get_global_transform_with_canvas() * (control.size * 0.5)
	await _touch(at, true)
	await _touch(at, false)


func _view(label: String) -> void:
	await RenderingServer.frame_post_draw
	var path := OUT + "native_views/nursery_%d_%s.webp" % [width_now,label]
	assert(root.get_texture().get_image().save_webp(path,true) == OK)
	views.append({"label":label,"path":path.trim_prefix("res://"),"sha256":FileAccess.get_sha256(path),"direct_review":false})


func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--width="):
			width_now = arg.trim_prefix("--width=").to_int()
	root.size = Vector2i(width_now,720)
	DisplayServer.window_set_size(root.size)
	assert(DirAccess.make_dir_recursive_absolute(OUT + "native_views/") == OK)
	assert(DirAccess.make_dir_recursive_absolute(OUT + "native_frames/") == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	await _wait(20)
	main._chapter_two_ref().restore_state({})
	var initial_stars := main.opera_stars
	var rooms := main._castle_rooms_ref()
	rooms.show_room("bubble_bath",false)
	await _wait(12)
	var routes := main._castle_career_routes_ref()
	routes.sync()
	assert(CastleCareerRoutes.room_for_act(15) == "bubble_bath")
	assert(not ChapterTwoPartyPlan.is_live_act(15))
	var card := routes.button_for_act(15)
	assert(card != null and card.is_visible_in_tree())
	await _view("normal_bubble_bath_card")
	await _tap(card)
	for _tick: int in range(900):
		if main.opera_game != null and main.opera_game.act != null:
			break
		await _wait(1)
	assert(main.opera_game != null and main.opera_game.act != null)
	for _tick: int in range(180):
		if main.fade_rect == null or main.fade_rect.modulate.a <= 0.02:
			break
		await _wait(1)
	world = main.opera_game.act.career_world_2d
	assert(world != null and world.career_id == "nursery" and world.phase_index == 0)
	assert(not main.opera_game.story_mode and not main.opera_game.dev_playtest)
	assert(world.surface is OperaNurserySurface)
	events.append({"event":"actual_bubble_bath_card_production_entry","two_act":world.two_act_enabled,"phase_names":world.phases.map(func(p: Dictionary)->String:return String(p.get("name","")))})
	await _wait(8)
	await _view("normal_nursery_invitation")
	recording = true
	await _wait(15)
	assert(world.phase_progress == 0.0 and not world.task_open)
	for _tick: int in range(180):
		if world.armed_station >= 0:
			break
		await _wait(1)
	assert(world.armed_station >= 0)
	var hotspot: OperaWorldHotspot2D = world.station_nodes[world.armed_station] as OperaWorldHotspot2D
	await _tap(hotspot.touch_button)
	for _tick: int in range(400):
		if world.task_open:
			break
		await _wait(1)
	assert(world.task_open and not world.player_actor.visible)
	await _wait(15)
	await _view("wash_ready")
	var wash_at := world.surface.get_global_transform_with_canvas() * (world.surface.size * Vector2(0.74,0.55))
	await _touch(wash_at,true)
	await _wait(24)
	await _view("wet_to_soap")
	await _touch(wash_at,false)
	await _wait(2)
	var paused_progress := world.phase_progress
	await _wait(15)
	assert(is_equal_approx(world.phase_progress,paused_progress) and not world.phase_advance_pending)
	events.append({"event":"midwash_release_pauses_earned_progress","progress":paused_progress})
	await _view("wash_paused")
	await _touch(wash_at,true)
	var seen: Dictionary = {}
	for _tick: int in range(300):
		var state := (world.surface as OperaNurserySurface).wash_state
		if state != "ready" and not seen.has(state):
			seen[state] = true
			await _view("state_" + state)
		if world.phase_advance_pending:
			break
		await _wait(1)
	assert(world.phase_advance_pending)
	await _touch(wash_at,false)
	await _view("earned_clean_result")
	events.append({"event":"wash_completed_by_real_hold","progress":world.phase_progress})
	for _tick: int in range(400):
		if world.phase_index > 0:
			break
		await _wait(1)
	assert(world.phase_index == 1 and world.player_actor.visible)
	await _wait(12)
	await _view("next_catch_invitation_actor_restored")
	recording = false
	await _tap(main.global_navigation_button)
	for _tick: int in range(180):
		if main.opera_game == null:
			break
		await _wait(1)
	assert(main.opera_game == null and main.game == "level2" and main.castle_room_id == "bubble_bath")
	assert(main.opera_stars == initial_stars)
	await _wait(12)
	await _view("actual_back_to_bubble_bath_no_unearned_star")
	events.append({"event":"actual_partial_career_back","stars_unchanged":true,"full_career_completion":false})
	for index: int in range(images.size()):
		var path := OUT + String(frames[index]["path"])
		assert(images[index].save_webp(path,true) == OK)
		frames[index]["sha256"] = FileAccess.get_sha256(path)
	images.clear()
	var file := FileAccess.open(OUT + "CAPTURE_%d.json" % width_now,FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"ACTUAL_NURSERY_CARD_WASH_PAUSE_EARNED_CLEAN_NEXT_PHASE_AND_PARTIAL_BACK_CAPTURED_REVIEW_PENDING","events":events,"views":views,"frames":frames,"width":width_now,"qualification":"Isolated initial Main/Castle entry and save home. Actual production Bubble Bath card/caller, hotspot touch approach, wash hold/pause/resume, earned clean first phase and normal Back partial exit. No forced phases/results, patched callbacks, manual controller ticks or complete-career reward claim. Not birthday route, physical-device, child, owner or visual acceptance. Native image readback slows capture clock; buffered disk encoding after activity/return."},"\t"))
	file.close()
	print("NURSERY_ACTUAL_ROUTE|",width_now,"|PASS_CAPTURE_REVIEW_PENDING")
	quit(0)
'''
(F/'review_tools/capture_actual_route_v355.gd').write_text(gd,encoding='utf-8')
run=(F/'review_tools/run_candidate_v354.py').read_text()
run=run.replace("out=r/'audit/job_nursery_wash_connected_v1_20261002/candidate_capture_v2';assert not out.exists();out.mkdir()","out=r/'audit/job_nursery_wash_connected_v1_20261002/actual_route_v2'\nwidth=sys.argv[1];assert width in ['1280','1600']\nout.mkdir(exist_ok=True);out=out/('process_'+width);assert not out.exists();out.mkdir()")
run=run.replace('tmp/capture_nursery_wash_candidate_v354.gd','audit/job_nursery_wash_connected_v1_20261002/review_tools/capture_actual_route_v355.gd').replace("'--touch','--classic-touch-test'","'--width='+width,'--touch','--classic-touch-test'")
run=run.replace('Four Nursery direct training/authored Chapter2 catalog room fixtures; connected painted candidate v2 fixed-layout states','Actual production Bubble Bath card/caller, wash first-phase and normal partial-career Back at '+ 'one aspect; connected fixed-layout candidate v2 states')
(F/'review_tools/run_actual_route_v355.py').write_text(run,encoding='utf-8')
print('Prepared real Nursery caller/capture; complete-career and birthday claims excluded.')
