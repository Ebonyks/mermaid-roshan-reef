extends SceneTree

# Representative Mobile-renderer evidence for the regenerated Ember Fortress.
# This is an art capture probe, not a gameplay gate; probe_ember.gd owns the
# deterministic interaction assertions.

const OUT := "res://audit/ember_runtime_2026-07-21"

var main: ReefMain
var ember: EmberFortressLevel
var cam: Camera3D


func _frames(count: int) -> void:
	for i in range(count):
		await process_frame


func _save(name: String) -> void:
	await _frames(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(OUT.path_join(name + ".png"))
	print("EMBERSHOT|", name, "|", "OK" if error == OK else "FAIL")


func _shot(name: String, position: Vector3, target: Vector3, up: Vector3, fov: float = 62.0) -> void:
	cam.fov = fov
	cam.position = position
	cam.look_at(target, up)
	cam.current = true
	await _save(name)


func _surface_shot(name: String, direction: Vector3, distance: float = 17.0,
		height: float = 7.0, fov: float = 58.0) -> void:
	var up := direction.normalized()
	var tangent := Vector3.RIGHT - up * Vector3.RIGHT.dot(up)
	if tangent.length() < 0.1:
		tangent = Vector3.FORWARD - up * Vector3.FORWARD.dot(up)
	tangent = tangent.normalized()
	var approach := tangent.cross(up).normalized() * -1.0
	var avatar_axis := up.cross(tangent).normalized()
	ember._dir = up.rotated(avatar_axis, 0.10)
	ember._fwd = tangent
	ember._h = 0.0
	ember._update_avatar_transform()
	var target: Vector3 = ember._surf(up, 2.8)
	await _shot(name, target + up * (height - 2.8) + approach * distance, target, up, fov)


func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("EMBERSHOT|RESULT|HEADLESS SKIP")
		quit()
		return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	var packed: PackedScene = load("res://scenes/main.tscn")
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(3)
	main._skip_intro()
	main.quality = "speedy"
	main._start_ember()
	await _frames(45)
	ember = main.ember_game as EmberFortressLevel
	ember._sync_detail_lights()
	# Fixed review cameras must not accidentally trigger a gameplay portal.
	ember.set_process(false)
	ember._lbl_big.visible = false
	cam = Camera3D.new()
	cam.far = 450.0
	get_root().add_child(cam)
	var origin := EmberFortressLevel.ORIGIN
	await _shot("01_planet_arrival", origin + Vector3(88, 48, 92), origin + Vector3(0, 4, 0), Vector3.UP, 54.0)
	await _surface_shot("02_citadel_gate_closed", EmberFortressLevel.GATE_DIR, 31.0, 16.0, 50.0)
	var first_lantern: Dictionary = ember._lanterns[0]
	await _surface_shot("03_lantern_unlit_gameplay", first_lantern["dir"] as Vector3, 22.0, 13.0, 48.0)
	ember._light_lantern(0)
	ember._sync_detail_lights()
	await _surface_shot("04_lantern_lit_gameplay", first_lantern["dir"] as Vector3, 20.0, 12.0, 46.0)
	var first_vent: Dictionary = ember._vents[0]
	await _surface_shot("05_friendly_geyser", first_vent["dir"] as Vector3, 20.0, 12.0, 48.0)
	for i in range(1, EmberFortressLevel.LANTERNS):
		ember._light_lantern(i)
	await _surface_shot("06_citadel_gate_open", EmberFortressLevel.GATE_DIR, 31.0, 16.0, 50.0)
	var home_target: Vector3 = ember._home_pos
	ember._dir = Vector3.DOWN.rotated(Vector3.FORWARD, 0.13)
	ember._fwd = Vector3.FORWARD
	ember._h = 0.0
	ember._update_avatar_transform()
	await _shot("07_home_ring", home_target + Vector3.DOWN * 10.0 + Vector3.RIGHT * 18.0,
		home_target, Vector3.DOWN, 46.0)
	var moon_target: Vector3 = ember._moon.global_position
	await _shot("08_ash_moon", moon_target + Vector3(30, 18, 38), moon_target, Vector3.UP, 54.0)
	ember._hud.visible = false
	main._start_ember_dungeon()
	await _frames(24)
	var dungeon: DungeonLevel = main.dungeon_game
	cam.current = false
	await _save("09_dungeon_combat")
	dungeon.arena._win()
	dungeon.arena.win_t = 0.0
	await _frames(16)
	await _save("10_dungeon_puzzle")
	print("EMBERSHOT|DONE|", ProjectSettings.globalize_path(OUT))
	quit()
