extends SceneTree
## Configured current room, real GUI input. Not a natural-route, device,
## child, owner or canonical QA11 acceptance session.
const OUT := "res://assets_src/imagegen/job_art_chef_20261019/review_chapter2_03/"
var m: ReefMain
var world: OperaCareerWorld2D
var surface: OperaGestureSurface
var records: Array[Dictionary] = []
var failures: Array[String] = []
var phase_id := ""
var width_now := 1280
func _initialize() -> void:
	call_deferred("_run")
func _ck(label: String, ok: bool) -> void:
	if not ok:
		failures.append(label)
		push_error("AST_ART_CAPTURE " + label)
func _shot(state: String) -> void:
	await create_timer(0.045).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d" % [phase_id,state,width_now]
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"hud":true,"phase_progress":world.phase_progress,
		"widget_fill":surface.widget_fill,"pipe_round":surface.pipe_round,
		"fixture":"configured current Castle career phase; routed GUI input"})
func _touch(at: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * at
	event.pressed = pressed
	root.push_input(event)
	await process_frame
func _drag(at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = surface.get_global_transform_with_canvas() * at
	root.push_input(event)
	await process_frame
func _place(tile: String, cell: int) -> void:
	var slot: int = surface.pipe_tray.find(tile)
	_ck("tray has " + tile,slot >= 0)
	if slot < 0:
		return
	await _touch(surface._pipe_tray_rect(slot).get_center(),true)
	await _drag(surface._pipe_cell_rect(cell).get_center())
	await _touch(surface._pipe_cell_rect(cell).get_center(),false)
	_ck("placed " + tile + " in " + str(cell),String(surface.pipe_grid[cell]) == tile)
func _run() -> void:
	var expected := ProjectSettings.globalize_path("res://tmp/chef_capture_appdata_chapter2_03").replace("\\", "/")
	if not OS.get_user_data_dir().replace("\\", "/").begins_with(expected + "/"):
		push_error("USERDATA_ISOLATION_FAILED_BEFORE_GAME_INITIALIZATION")
		quit(2)
		return
	print("USERDATA_ISOLATION|PASS|", OS.get_user_data_dir())
	DirAccess.make_dir_recursive_absolute(OUT)
	m = (load("res://scenes/main.tscn") as PackedScene).instantiate() as ReefMain
	root.add_child(m)
	await create_timer(2.0).timeout
	m._start_menu_ref()._dismiss_menu()
	m._skip_intro()
	m._day_one_ref().restore_state({"day_one_active":false})
	m.chapter2_story_complete = true
	m.pearl_count = m.PEARL_TOTAL
	m.level2_done_once = true
	m._enter_level2_now(true,false,false)
	await create_timer(0.5).timeout
	m._enter_castle_interior_now(false)
	await create_timer(0.5).timeout

	m._castle_rooms_ref().suspend()
	m.game="opera"
	m.set_process(false)
	m.hud_layer.layer=12
	m.hud_game.visible=false
	m.obj_card.visible=false
	m.hud_msg.visible=false
	m.player.visible=false
	m.chapter2_active=true
	m.chapter2_active_objective=ChapterTwoDirector.OBJECTIVE_PARTY_PREP
	m.chapter2_strawberry_mask=0x1F
	for aspect: int in [1280,1600]:
		width_now=aspect
		root.size=Vector2i(aspect,720)
		DisplayServer.window_set_size(root.size)
		for phase in range(5):
			m.chapter2_cake_piece_mask=[0,1,3,7,15][phase]
			var competition := OperaCompetition.new()
			competition.configure("chef")
			world=OperaCareerWorld2D.new()
			m.add_child(world)
			world.setup(m,{"costume":"chef","chapter":"chapter2",
				"phase_overrides":ChapterTwoCareerSceneAdapter.phase_set("chef").get("phases",[]),
				"finale_start":5,"chapter2_resume_phase_index":phase},competition,Callable(),[],
				ChapterTwoCareerSceneAdapter.adapter_config("chef"),{"chapter":"chapter2"})
			await process_frame
			world.phase_gap=0.0
			world.reveal_t=0.0
			world._open_task()
			await create_timer(0.36).timeout
			world.reveal_t=0.0
			world.set_process(false)
			surface=world.surface as OperaGestureSurface
			_ck("Chapter Two uses room-coordinate Chef surface",surface is OperaChefSurface)
			surface.set_process(false)
			phase_id="chapter2-"+str(phase)+"-"+surface.mode
			m._sync_castle_voice_caption()
			m.clear_dialogue()
			m.hud_msg.visible=false
			m.obj_card.visible=false
			await _shot("ready")
			match phase:
				0:
					var at:=surface._pour_pitcher_rect().get_center()
					await _touch(at,true)
					for tick in range(180):
						surface._process(1.0/30.0)
						if tick==45:
							await _shot("earned-mid-pour")
						if surface.pour_level>=0.999:
							break
					await _touch(at,false)
					_ck("Child pour earns full bowl",surface.pour_level>=0.999)
				1:
					var pivot:=surface._circle_pivot()
					await _touch(pivot+Vector2(42,0),true)
					for sample in range(1,121):
						await _drag(pivot+Vector2.from_angle(float(sample)*TAU/36.0)*42.0)
						if sample in [9,18,27,36]:
							await _shot("whisk-angle-"+str(sample))
						if world.phase_advance_pending:
							break
					await _touch(pivot+Vector2(42,0),false)
					_ck("Child stir earns completion",world.phase_advance_pending)
				2:
					surface.oven_t=0.62
					var at:=surface._oven_handle_rect().get_center()
					await _touch(at,true)
					await _touch(at,false)
					_ck("Child hearth tap earns bake",world.phase_progress>0)
				3:
					for index in range(3):
						var at:=surface._target_anchor_point(index)-Vector2(0,17)
						await _touch(at,true)
						await _touch(at,false)
						_ck("One earned pair per tray",is_equal_approx(world.phase_progress,float(index+1)))
						await _shot("earned-stack-"+str(index+1))
				4:
					await _touch(surface._trace_demo_point(0),true)
					for sample in range(1,65):
						await _drag(surface._trace_demo_point(float(sample)/64.0))
						if sample in [16,32,48]:
							await _shot("earned-frost-"+str(sample))
					await _touch(surface._trace_demo_point(1),false)
					_ck("Child frosting earns completion",surface.trace_journey>=0.99)
			await _shot("earned-endpoint")
			world.queue_free()
			await process_frame
			await process_frame
	var file:=FileAccess.open(OUT+"capture.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"failures":failures,
		"scope":"Configured Chapter Two actual GUI input and current Mobile/HUD; no physical-device/owner acceptance"},"\t"))
	file.close()
	print("CHEF_CHAPTER2_CAPTURE|", "PASS" if failures.is_empty() else "FAIL", "|",records.size(),"frames")
	quit(0 if failures.is_empty() else 1)
