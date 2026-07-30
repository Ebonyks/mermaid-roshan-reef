extends SceneTree

# Fixed Mobile-render audit set for the Pearl Opera House. This is dev-only
# evidence: the shipping 2D lobby, the three 3D boss stages, and one readable
# full-frame shot of every career's actual Canvas world. Run windowed because
# screenshots require a real viewport.

var cam: Camera3D
var main: ReefMain
var opera: OperaHouse
var out_dir := ""


func _settle(frames: int) -> void:
	for frame_index in range(frames):
		await process_frame


func _shot(name: String, pos: Vector3, look: Vector3, fov: float = 62.0) -> void:
	cam.fov = fov
	cam.global_position = pos
	cam.look_at(look, Vector3.UP)
	cam.current = true
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("OPERASHOT|", name, "|", "OK" if error == OK else "FAIL")

func _canvas_shot(name: String) -> void:
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("OPERASHOT|", name, "|", "OK" if error == OK else "FAIL")

func _hide_main_presentation() -> void:
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.player != null:
		main.player.visible = false
		main.player.set_process(false)
	if opera.hud != null:
		opera.hud.visible = false
	if opera.avatar != null:
		opera.avatar.visible = false
	if opera.cam != null:
		opera.cam.current = false


func _capture_lobby() -> void:
	if opera.lobby_2d == null:
		print("OPERASHOT|2D_LOBBY|FAIL")
		return
	main.opera_stars = 0
	opera.lobby_2d.show_lobby(0, main.opera_stars)
	await _canvas_shot("opera_01_lobby_2d_floor1")
	main.opera_stars = (1 << 4)
	opera.lobby_2d.show_lobby(1, main.opera_stars)
	await _canvas_shot("opera_02_lobby_2d_floor2")
	main.opera_stars = (1 << 4) | (1 << 9)
	opera.lobby_2d.show_lobby(2, main.opera_stars)
	await _canvas_shot("opera_03_lobby_2d_floor3")
	main.opera_stars = OperaHouse.ALL_STARS
	opera.lobby_2d.show_lobby(2, main.opera_stars)
	await _canvas_shot("opera_04_lobby_2d_complete")
	main.opera_stars = 0
	opera.lobby_2d.show_lobby(0, main.opera_stars)

func _remove_current_act() -> void:
	if opera.act == null:
		return
	var old_act: OperaAct = opera.act
	if old_act.prev_env != null:
		main.we_node.environment = old_act.prev_env
	old_act.queue_free()
	opera.act = null
	await _settle(3)


func _build_act(index: int) -> OperaAct:
	await _remove_current_act()
	var config: Dictionary = (OperaHouse.ACTS[index] as Dictionary).duplicate()
	config["act_tag"] = String(config["name"]) + "  "
	var current := OperaAct.new()
	opera.add_child(current)
	opera.act = current
	current.start(main, config, Callable())
	await _settle(12)
	current.set_process(false)
	# Shipping career doors are pure Canvas worlds. They intentionally have no
	# 3D actor/stage/camera to pose for this audit; the screenshot below records
	# the exact 2D screen a child plays.
	if current.career_world_2d != null:
		cam.current = true
		return current
	# Art review should show the career as it is played, not the pre-show
	# rescue state. Hide that completed beat, then bring the dressed rival and
	# its work station onto the set.
	for imp: Dictionary in current.imps:
		var imp_node := imp.get("node") as Node3D
		if imp_node != null:
			imp_node.visible = false
	for captive: Dictionary in current.captives:
		var captive_node := captive.get("node") as Node3D
		if captive_node != null:
			captive_node.visible = false
	if current.competition != null:
		current.stage_phase = "puzzle"
		current._begin_competition()
	# Capture the two most materially changed games at their new signature
	# moments: the actual championship bout and the grand illusion portal.
	if current.kind == "box":
		if current.box_bag != null:
			current.box_bag.visible = false
		current._box_wave()
	elif current.kind == "shuffle":
		current._begin_magic_finale()
	if current.hud != null:
		current.hud.visible = false
	if current.cam != null:
		current.cam.current = false
	cam.current = true
	return current


func _capture_shared_theatre() -> void:
	# The shared 3D proscenium now belongs to bosses only. Career doors never
	# enter it, which is the architecture this audit is meant to make visible.
	var current: OperaAct = await _build_act(4)
	var center := OperaAct.CENTER
	await _shot("opera_12_shared_stage_audience_wide", center + Vector3(0, 10, 36),
		center + Vector3(0, 7, -3), 66.0)
	await _shot("opera_13_shared_stage_three_quarter", center + Vector3(34, 11, 25),
		center + Vector3(0, 6, -3), 66.0)
	await _shot("opera_14_backstage_corridor", center + Vector3(-61, 8, 15),
		center + Vector3(-41, 4, 1), 60.0)
	await _shot("opera_15_proscenium_reverse", center + Vector3(-17, 8, -8),
		center + Vector3(0, 7, 16), 64.0)
	current.set_process(false)


func _capture_act_sets() -> void:
	var center := OperaAct.CENTER
	for index in range(OperaHouse.ACTS.size()):
		var current: OperaAct = await _build_act(index)
		var config: Dictionary = OperaHouse.ACTS[index]
		var slug := String(config["career"]).to_lower().replace(" ", "_")
		await _shot("opera_act_%02d_%s" % [index + 1, slug], center + Vector3(0, 10, 34),
			center + Vector3(0, 5.5, -3), 66.0)
		current.set_process(false)


func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("OPERASHOT|RESULT|HEADLESS SKIP")
		quit()
		return
	var requested: String = OS.get_environment("OPERA_SHOT_OUT")
	out_dir = requested if requested != "" else ProjectSettings.globalize_path("res://tmp/opera_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	seed(20260721)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	if main.intro_active:
		main._skip_intro()
	await _settle(12)
	main.opera_progress = 0
	main.opera_stars = 0
	main.opera_done = false
	main.game = "level2"
	main._start_opera()
	await _settle(24)
	opera = main.opera_game
	if opera == null:
		print("OPERASHOT|RESULT|FAIL|opera did not start")
		quit(1)
		return
	main.set_process(false)
	opera.set_process(false)
	_hide_main_presentation()
	cam = Camera3D.new()
	cam.far = 800.0
	get_root().add_child(cam)
	cam.current = true
	await _capture_lobby()
	if opera.lobby_2d != null:
		opera.lobby_2d.hide_lobby()
	await _capture_shared_theatre()
	await _capture_act_sets()
	await _remove_current_act()
	print("OPERASHOT|DONE|", out_dir)
	quit()
