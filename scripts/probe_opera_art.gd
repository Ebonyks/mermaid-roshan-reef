extends SceneTree
## Windowed Mobile-render capture set for the current Pearl Opera product:
## three direct Canvas lobby pages and the thirteen live Canvas career worlds.

var main: ReefMain
var opera: OperaHouse
var out_dir := ""


func _settle(frames: int) -> void:
	for _frame: int in range(frames):
		await process_frame


func _shot(name: String) -> void:
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name + ".png"))
	print("OPERASHOT|", name, "|", "OK" if error == OK else "FAIL")


func _capture_lobby() -> void:
	if opera.lobby_2d == null:
		print("OPERASHOT|CANVAS_LOBBY|FAIL")
		return
	for floor_index: int in range(3):
		opera.lobby_2d.show_lobby(floor_index, 0)
		await _shot("opera_lobby_page_%d" % (floor_index + 1))
	opera.lobby_2d.show_lobby(2, OperaHouse.ACTIVE_STAR_MASK)
	await _shot("opera_lobby_all_13_complete")
	opera.lobby_2d.show_lobby(0, 0)


func _remove_current_act() -> void:
	if opera.act == null:
		return
	var old_act: OperaAct = opera.act
	opera.act = null
	opera.act_index = -1
	old_act.cancel()
	await _settle(3)


func _capture_act_sets() -> void:
	if opera.lobby_2d != null:
		opera.lobby_2d.hide_lobby()
	for index: int in OperaHouse.LIVE_ACT_INDICES:
		await _remove_current_act()
		opera._start_act(index)
		await _settle(12)
		var current := opera.act as OperaAct
		var config: Dictionary = OperaHouse.ACTS[index]
		var slug := String(config.get("career", "career")).to_lower().replace(" ", "_")
		if current == null or current.career_world_2d == null:
			print("OPERASHOT|opera_act_%02d_%s|FAIL" % [index + 1, slug])
			continue
		current.set_process(false)
		current.career_world_2d.set_process(false)
		await _shot("opera_act_%02d_%s" % [index + 1, slug])


func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("OPERASHOT|RESULT|HEADLESS SKIP")
		quit()
		return
	var requested: String = OS.get_environment("OPERA_SHOT_OUT")
	out_dir = requested if not requested.is_empty() \
		else ProjectSettings.globalize_path("res://tmp/opera_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	seed(20260721)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _settle(2)
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
	if opera == null or opera.lobby_2d == null:
		print("OPERASHOT|RESULT|FAIL|Canvas Opera did not start")
		quit(1)
		return
	main.set_process(false)
	opera.set_process(false)
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.player != null:
		main.player.visible = false
		main.player.set_process(false)
	await _capture_lobby()
	await _capture_act_sets()
	await _remove_current_act()
	print("OPERASHOT|DONE|", out_dir)
	quit()
