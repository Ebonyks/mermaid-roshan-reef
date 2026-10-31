extends SceneTree
## Configured real-world fixture with routed GUI touch. No natural-route,
## device, child, owner or canonical QA11 certification claim.
const OUT := "res://assets_src/imagegen/job_art_teacher_20261018/review/"
var m: ReefMain
var act: OperaAct
var world: OperaCareerWorld2D
var surface: OperaTeacherSurface
var records: Array[Dictionary] = []
var phase_id := ""
var width_now := 1280
var failures: Array[String] = []
func _initialize() -> void:
	call_deferred("_run")
func _shot(state: String) -> void:
	await create_timer(0.08).timeout
	await RenderingServer.frame_post_draw
	var id := "%s-%s-%d" % [phase_id, state, width_now]
	var path := OUT + id + ".png"
	assert(root.get_texture().get_image().save_png(path) == OK)
	records.append({"id":id,"path":path.trim_prefix("res://"),"renderer":RenderingServer.get_current_rendering_method(),
		"viewport":[root.size.x,root.size.y],"hud":true,"runtime":true,"fixture":"configured current Opera world; routed GUI input"})
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
func _run() -> void:
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

	var act_index := -1
	for index: int in range(OperaHouse.ACTS.size()):
		if OperaHouse.ACTS[index].get("costume", "") == "teacher":
			act_index = index
	assert(act_index >= 0)
	for aspect: int in [1280,1600]:
		width_now = aspect
		root.size = Vector2i(aspect,720)
		DisplayServer.window_set_size(root.size)
		m._castle_rooms_ref().show_room(CastleCareerRoutes.room_for_act(act_index),false)
		await create_timer(0.8).timeout
		phase_id = "room-entry"
		await _shot("crest")
	var file := FileAccess.open(OUT+"capture_crest.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"captures":records,"scope":"Actual Castle room picture-card context; no device/owner acceptance"},"\t"))
	file.close()
	quit()
