extends SceneTree
## Configured current Boxer, real routed one-finger GUI input and explicit negatives.
const OUT := "res://assets_src/imagegen/job_art_boxer_20261019/review_current01/"
var m: ReefMain
var world: OperaCareerWorld2D
var boxer: OperaBoxingSurface
var records: Array[Dictionary] = []
var failures: Array[String] = []
var phase_id := ""
var width_now := 1280
func _initialize() -> void:
	call_deferred("_run")
func _ck(label: String, ok: bool) -> void:
	if not ok:
		failures.append(label)
		push_error("BOXER_CAPTURE " + label)
func _shot(state: String) -> void:
	await create_timer(0.045).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d" % [phase_id,state,width_now]
	var path := OUT+id+".png"
	assert(root.get_texture().get_image().save_png(path)==OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"phase_progress":world.phase_progress,
		"round_index":boxer.round_index(),"imp_state":boxer._imp_state,
		"owners":boxer.touch_owner_snapshot(),"glove0":[boxer.glove_positions[0].x,boxer.glove_positions[0].y],
		"glove1":[boxer.glove_positions[1].x,boxer.glove_positions[1].y],
		"fixture":"Configured current five-phase specialist; GUI input, no device/owner/canonicalQA11 acceptance"})
func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index=0
	event.position=boxer.get_global_transform_with_canvas()*at
	event.pressed=pressed
	root.push_input(event)
	await process_frame
func _drag(at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index=0
	event.position=boxer.get_global_transform_with_canvas()*at
	root.push_input(event)
	await process_frame
func _settle() -> void:
	for tick: int in range(45):
		boxer._process(1.0/60.0)
	await process_frame
func _punch(hand: int, target: Vector2, tag: String) -> void:
	var start := boxer.glove_positions[hand]
	var before := boxer.round_index()
	await _touch(start,true)
	for step: int in range(1,13):
		await _drag(start.lerp(target,float(step)/12.0))
		if step==4:
			await _shot(tag+"-forward-partial")
		if step==8:
			await _shot(tag+"-near-contact")
		boxer._process(1.0/60.0)
	await _shot(tag+"-contact")
	var after := boxer.round_index()
	await _drag(target)
	await _drag(target)
	_ck("held extension cannot bank twice",boxer.round_index()==after)
	await _touch(target,false)
	_ck("one finger ownership releases",boxer.touch_owner_snapshot().is_empty())
	_ck("one forward GUI action earns one unit",after==before+1)
	await _settle()
	await _shot(tag+"-settled")
func _run() -> void:
	var expected := ProjectSettings.globalize_path("res://tmp/boxer_capture_appdata_current01/Roaming").replace("\\","/")
	if not OS.get_user_data_dir().replace("\\","/").begins_with(expected+"/"):
		push_error("USERDATA_ISOLATION_FAILED_BEFORE_GAME_INITIALIZATION")
		quit(2)
		return
	print("USERDATA_ISOLATION|PASS|",OS.get_user_data_dir())
	DirAccess.make_dir_recursive_absolute(OUT)
	m=(load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(2).timeout
	m._start_menu_ref()._dismiss_menu()
	m._skip_intro()
	m._day_one_ref().restore_state({"day_one_active":false})
	m.chapter2_story_complete=true
	m.pearl_count=m.PEARL_TOTAL
	m.level2_done_once=true
	m._enter_level2_now(true,false,false)
	await create_timer(0.5).timeout
	m._enter_castle_interior_now(false)
	await create_timer(0.5).timeout
	var act_index := -1
	for i: int in range(OperaHouse.ACTS.size()):
		if OperaHouse.ACTS[i].get("costume","")=="boxer":
			act_index=i
	assert(act_index>=0)
	for aspect: int in [1280,1600]:
		width_now=aspect
		root.size=Vector2i(aspect,720)
		DisplayServer.window_set_size(root.size)
		var room := CastleCareerRoutes.room_for_act(act_index)
		m._castle_rooms_ref().show_room(room,false)
		await create_timer(0.8).timeout
		m._start_opera_from_room(act_index,room)
		for tick: int in range(600):
			await process_frame
			if m.opera_game!=null and m.opera_game.act!=null and m.opera_game.act.career_world_2d!=null:
				break
		world=m.opera_game.act.career_world_2d
		assert(world!=null)
		for requested: String in ["boxing_guide","boxing_jab","boxing_guard","boxing_imp","boxing_belt"]:
			var phase := -1
			for i: int in range(world.phases.size()):
				if world.phases[i].get("mode","")==requested:
					phase=i
			assert(phase>=0)
			world.active=true
			world.phase_index=phase
			world._show_phase()
			world.phase_gap=0
			world._open_task()
			await create_timer(0.6).timeout
			boxer=world.surface as OperaBoxingSurface
			assert(boxer!=null and world.task_open)
			world.set_process(false)
			boxer.set_process(false)
			phase_id=requested
			_ck("both source gloves loaded",boxer._painted_gloves.size()==2 and boxer._painted_gloves[0]!=null and boxer._painted_gloves[1]!=null)
			await _shot("ready")
			if requested=="boxing_guide":
				for tick: int in range(90):
					boxer._process(1.0/30.0)
				_ck("passive guide never banks",boxer.round_index()==0 and world.phase_progress==0)
				for hand: int in range(2):
					await _punch(hand,boxer.guide_target_position(hand),"guide-"+str(hand))
			elif requested=="boxing_jab":
				for n: int in range(4):
					await _punch(n%2,boxer.active_target_position(),"jab-"+str(n))
			elif requested=="boxing_guard":
				# One unguarded harmless cue: no progress and no loss.
				for tick: int in range(120):
					boxer._process(1.0/30.0)
				_ck("passive counter cannot bank",boxer.round_index()==0 and world.phase_progress==0)
				await _shot("harmless-counter-reset")
				for n: int in range(3):
					var side := boxer._guard_side
					var start := boxer.glove_positions[side]
					var target := boxer.guard_target_position(side)
					await _touch(start,true)
					for step: int in range(1,13):
						await _drag(start.lerp(target,float(step)/12.0))
					await _shot("guard-"+str(n)+"-held")
					for tick: int in range(150):
						boxer._process(1.0/30.0)
						if tick==30:
							await _shot("guard-"+str(n)+"-incoming")
						if boxer.round_index()>n:
							break
					await _shot("guard-"+str(n)+"-contact")
					await _touch(target,false)
					_ck("held guarded GUI action banks one",boxer.round_index()==n+1)
					await _settle()
			elif requested=="boxing_imp":
				for n: int in range(6):
					var prior := ""
					for tick: int in range(600):
						boxer._process(1.0/30.0)
						if boxer._imp_state!=prior and n==0:
							prior=boxer._imp_state
							await _shot("opponent-"+prior)
						if boxer.imp_is_open():
							break
					_ck("only existing open window selected",boxer.imp_is_open())
					await _punch(n%2,boxer.active_target_position(),"title-"+str(n))
			elif requested=="boxing_belt":
				await _punch(0,boxer.active_target_position(),"belt")
			_ck("phase exact goal earned by GUI",world.phase_advance_pending and boxer.completion_accepted)
			await _shot("earned-phase-complete")
			world.task_open=false
			world.action_panel.visible=false
			await process_frame
		world.set_process(true)
		m.opera_game._leave_early()
		await process_frame
		await process_frame
	var file := FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"failures":failures,"baseline":"e90c0daa83cf05644f0e9942e85c1198ed7901f7","scope":"Configured fullfive-phase Boxer; real one-finger GUI earning/passive/no-double-payout/cleanup; not canonical/device/child/owner acceptance"},"\t"))
	file.close()
	print("BOXER_CURRENT_CAPTURE|","PASS" if failures.is_empty() else "FAIL","|",records.size(),"frames")
	quit(0 if failures.is_empty() else 1)
