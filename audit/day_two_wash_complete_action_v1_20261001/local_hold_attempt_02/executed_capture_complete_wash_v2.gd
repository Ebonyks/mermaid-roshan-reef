extends SceneTree
## Actual training and birthday wash surfaces; diagnostic local input/tick, no root route.
const OUT := "res://tmp/wash_complete_action_v2/native_frames/"
const STEP := 1.0 / 30.0
var main: ReefMain
var records: Array[Dictionary] = []
var cases: Array[Dictionary] = []
func _initialize() -> void:
	_run.call_deferred()
func _wait(count: int) -> void:
	for _i: int in range(count):
		await process_frame
func _capture(world: OperaCareerWorld2D, ident: String, tick: int, event: String) -> void:
	await RenderingServer.frame_post_draw
	var screenshot: Image = root.get_texture().get_image()
	var name: String = "%s/%04d.webp" % [ident, tick]
	assert(screenshot.save_webp(OUT + name, true) == OK)
	var actor: OperaRoshanActor = world.player_animator
	var row: Dictionary = {"path":name,"sha256":FileAccess.get_sha256(OUT + name),"case":ident,"logical_tick":tick,"logical_seconds":float(tick)*STEP,"event":event,"phase_index":world.phase_index,"phase_progress":world.phase_progress,"phase_name":String(world.phases[world.phase_index].get("name", "")),"phase_advance_pending":world.phase_advance_pending,"surface_held":world.surface.held,"surface_completion":world.surface.completion_accepted,"visual_context":world.surface.visual_context,"widget_template":world.surface.widget_template,"player_animation":actor.current_animation,"player_frame":actor.current_frame,"player_position":[world.player_actor.position.x,world.player_actor.position.y],"player_size":[world.player_actor.size.x,world.player_actor.size.y],"viewport":[screenshot.get_width(),screenshot.get_height()]}
	records.append(row)
func _run() -> void:
	Engine.max_fps = 30
	assert(DisplayServer.get_name() != "headless")
	assert(DirAccess.make_dir_recursive_absolute(OUT) == OK)
	main = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(main)
	await _wait(5)
	main.day_one_active = false
	main._skip_intro()
	main._start_menu_ref()._dismiss_menu()
	main.game = "level2"
	main.g["phase"] = "hall"
	main.g["t"] = 0.0
	main.set_process(false)
	main.set_physics_process(false)
	main.hud_layer.visible = false
	main.player.visible = false
	var original_stars: int = main.opera_stars
	for width: int in [1280,1600]:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		root.size = Vector2i(width,720)
		DisplayServer.window_set_size(root.size)
		await _wait(4)
		for run_mode: String in ["opera_training", "birthday_story_catalog"]:
			for career: String in ["doctor","nursery"]:
				var config: Dictionary = {}
				for act: Dictionary in OperaHouse.ACTS:
					if String(act.get("costume", "")) == career:
						config = act.duplicate(true)
				assert(not config.is_empty())
				var context: Dictionary = {"chapter":"chapter2"} if run_mode=="birthday_story_catalog" else {}
				var director: OperaCompetition = OperaCompetition.new()
				director.configure(career)
				var world: OperaCareerWorld2D = OperaCareerWorld2D.new()
				main.add_child(world)
				world.setup(main,config,director,Callable(),[],{},context)
				await _wait(8)
				world.set_process(false)
				world.phase_index=0
				world.phase_progress=0.0
				world.active=true
				world.reveal_t=0.0
				world.phase_advance_pending=false
				world.phase_gap=0.0
				world._arm_phase()
				world._open_task()
				await _wait(8)
				world.surface.set_process(false)
				world.player_animator.set_process(false)
				assert(world.surface.mode=="hold" and world.task_open)
				assert(String(world.phases[0].get("name","")) in ["WASH","WASH HANDS"])
				var ident: String = "%s_%s_%d" % [run_mode,career,width]
				assert(DirAccess.make_dir_recursive_absolute(OUT+ident)==OK)
				var start: int=records.size()
				var accepted_tick: int=-1
				var next_phase_tick: int=-1
				for tick: int in range(240):
					var event: String="passive"
					if tick==12:
						var wash_touch: InputEventScreenTouch = InputEventScreenTouch.new()
						wash_touch.index=0
						wash_touch.pressed=true
						wash_touch.position=world.surface.size*0.5
						world.surface._gui_input(wash_touch)
						event="local_gui_press"
					elif tick>12:
						event="holding" if accepted_tick<0 else "completion_hold"
					world._process(STEP)
					world.surface._process(STEP)
					world.player_animator._process(STEP)
					# Phase/pose changes can re-enable these; keep this diagnostic at one manual tick.
					world.surface.set_process(false)
					world.player_animator.set_process(false)
					if tick<12:assert(world.phase_progress==0.0 and not world.phase_advance_pending)
					if world.phase_advance_pending and accepted_tick<0:
						accepted_tick=tick
						event="first_accepted_completion"
					if world.phase_index>0 and next_phase_tick<0:
						next_phase_tick=tick
						event="next_phase_armed"
						world.surface.set_process(false)
						world.player_animator.set_process(false)
					await _capture(world,ident,tick,event)
					if next_phase_tick>=0 and tick>=next_phase_tick+6:break
				assert(accepted_tick>=12 and next_phase_tick>accepted_tick)
				cases.append({"id":ident,"career":career,"run_mode":run_mode,"width":width,"using_chapter_two_phases":world.using_chapter_two_phases,"two_act_enabled":world.two_act_enabled,"first_record":start,"frame_count":records.size()-start,"accepted_tick":accepted_tick,"next_phase_tick":next_phase_tick,"phase_names":world.phases.map(func(p: Dictionary) -> String: return String(p.get("name",""))),"stars_unchanged":main.opera_stars==original_stars})
				assert(main.opera_stars==original_stars)
				world.close()
				world.queue_free()
				await _wait(4)
	var file: FileAccess=FileAccess.open(OUT+"CAPTURE_RECEIPT.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"status":"EIGHT_COMPLETE_NATIVE_WASH_FIXTURE_CASES","cases":cases,"frames":records,"qualification":"Actual existing career/story phase setup and local GUI press with manual unchanged controller/animator30Hz ticks. Initial passive hold, earned completion and next-phase arming captured. Root navigation, real wall-clock/input routing, device, child, owner and cinematic acceptance are not established."},"\t")+"\n")
	file.close()
	print("WASH_COMPLETE_CAPTURE|PASS ",records.size()," frames in8 cases")
	main.queue_free()
	await _wait(3)
	quit(0)
