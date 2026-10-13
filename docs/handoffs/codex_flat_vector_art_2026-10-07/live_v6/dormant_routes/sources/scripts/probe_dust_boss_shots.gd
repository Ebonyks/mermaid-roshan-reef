extends SceneTree

## Live visual capture for the rebuilt Dust Bunny encounter.
## This owns only the encounter clock after the real main scene is running;
## every image is read from the rendered viewport after frame_post_draw.

const DT := 0.05
const FRAME_CAP := 3600

var main: ReefMain
var boss: DustBossGame
var out_dir := ""
var frames := 0

func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("DUSTSHOT|HEADLESS SKIP (needs a real viewport; run with display)")
		quit()
		return
	Engine.time_scale = 2.0
	Engine.max_fps = 60
	var capture_width: int = maxi(1280, OS.get_environment("DUSTBOSS_SHOT_WIDTH").to_int())
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_size(Vector2i(capture_width, 720))
	out_dir = OS.get_environment("DUSTBOSS_SHOT_OUT")
	if out_dir == "":
		out_dir = ProjectSettings.globalize_path("res://tmp/dust_boss_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _settle(4)
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
	elif main.intro_active:
		main._skip_intro()
	await _settle(20)
	main.dust_boss_cool = 0.0
	main.game = ""
	main.save_data["dustboss_pending_rounds"] = 0
	main.save_data["dustboss_pending_damage"] = 0
	main.save_data["dustboss_pending_misses"] = 0
	main._start_game_now(main.dust_boss_fr)
	await _settle(4)
	boss = main._game_obj("dustboss", DustBossGame) as DustBossGame
	await _capture_splash()
	await _capture_first_hit()
	await _capture_avoided_counter()
	if String(main.g.get("db_state", "")) != "friends":
		print("DUSTSHOT|INCOMPLETE|encounter interrupted before final review state")
		quit(1)
		return
	print("DUSTSHOT|DONE|", out_dir)
	quit()

func _settle(count: int) -> void:
	for _i in range(count):
		await process_frame

func _tick() -> void:
	if not main.g.has("db_state"):
		return
	frames += 1
	await process_frame

func _capture_splash() -> void:
	await _shot("00_splash")
	var cap := 300
	var saw_identity := false
	var saw_weakness := false
	while cap > 0 and main.g.has("db_state"):
		var splash: BossSplash2D = main.g.get("db_splash") as BossSplash2D
		if splash == null or not is_instance_valid(splash):
			break
		if splash._elapsed >= 0.95 and not saw_identity:
			saw_identity = true
			await _shot("00b_splash_identity")
		if splash._elapsed >= 1.8 and not saw_weakness:
			saw_weakness = true
			await _shot("00c_splash_weakness_lesson")
		await _tick()
		cap -= 1

func _capture_first_hit() -> void:
	await _until_state("tell", 900)
	await _shot("01_tell_deliberate_hit")
	await _until_state("strike", 120)
	await _shot("02_strike_impact")
	await _until_state("damage_recovery", 120)
	await _shot("03_damage_recovery")

func _capture_avoided_counter() -> void:
	await _until_state("tell", 1200)
	await _shot("04_tell_safe_destination")
	var captured: Dictionary = {}
	while frames < FRAME_CAP and main.g.has("db_state"):
		var state := String(main.g.get("db_state", ""))
		var phase: int = int(main.g.get("db_hits", 0))
		var geometry: Dictionary = boss.danger_geometry()
		var step: int = int(geometry.get("step", 0))
		var key: String = "phase_%d_step_%d_%s" % [phase, step, state]
		main.touch_ui.stick_vec = Vector2.ZERO
		if state == "tell" or state == "strike":
			_move_to_safe_point()
			if not captured.has(key) and float(main.g.get("db_st", 0.0)) > 0.2:
				captured[key] = true
				await _shot(key)
		elif state == "vuln":
			var k: DustBunnyBossSprite = boss.kit()
			if k != null and k.vulnerable:
				if not captured.has(key):
					captured[key] = true
					await _shot(key)
				if float(main.g.get("db_st", 0.0)) >= 1.0:
					main.touch_ui.action_down = true
					await _tick()
					main.touch_ui.action_down = false
		elif state == "struck" or state == "friends":
			if not captured.has(key):
				captured[key] = true
				await _shot(key)
			if state == "friends":
				return
		await _tick()

func _wait_and_tap_counter() -> void:
	var waited := 0.0
	var tapped := false
	while waited < 2.0 and main.g.has("db_state"):
		if String(main.g.get("db_state", "")) == "vuln" \
				and not tapped and waited >= 0.55:
			main.touch_ui.action_down = true
			await _tick()
			main.touch_ui.action_down = false
			tapped = true
		else:
			await _tick()
		waited += DT
	if main.g.has("db_state"):
		await _shot("06_flinch_or_friends")

func _move_to_safe_point() -> void:
	var danger: Dictionary = boss.danger_geometry()
	var safe: Vector2 = danger.get("safe_point", Vector2.ZERO) as Vector2
	if safe == Vector2.ZERO:
		return
	var offset: Vector2 = safe - boss.stage.player_local()
	var delta: float = maxf(0.001, main.get_process_delta_time())
	main.touch_ui.stick_vec = (offset / (24.0 * delta)).limit_length(0.8)

func _until_state(want: String, cap: int) -> void:
	var remaining := cap
	while remaining > 0 and frames < FRAME_CAP and main.g.has("db_state"):
		if String(main.g.get("db_state", "")) == want:
			return
		await _tick()
		remaining -= 1

func _shot(name: String) -> void:
	await RenderingServer.frame_post_draw
	print("DUSTSHOT|diagnostic|player_visible=", main.player.visible,
		"|sprite_visible=", main.player.classic_sprite.visible,
		"|player_screen=", boss.stage.project_floor_point(boss.stage.player_local()),
		"|layer_visible=", (main.g.get("db_mastery_layer") as CanvasLayer).visible,
		"|viewport=", root.get_visible_rect().size)
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var path := out_dir.path_join(name + ".png")
	var error: Error = image.save_png(path)
	print("DUSTSHOT|", name, "|state=", String(main.g.get("db_state", "-")),
		"|damage=", int(main.g.get("db_damage_taken", 0)), "|",
		"OK|path=", path if error == OK else "SAVE_ERROR")
