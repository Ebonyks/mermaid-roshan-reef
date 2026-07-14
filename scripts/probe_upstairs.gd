extends SceneTree
# Upper-story wrap-around probe: the upstairs now spans the full-width back
# block plus a gallery over EACH wing (library left, toy room right), reached
# through the hall's new arcade arches. Checks the y-banded zones hold (floors
# support, ceilings cap, arches are passable) and saves screenshots.
# Prints OK/FAIL lines (ci.sh convention).

const OUT := "C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-Claude-Projects-Book-layout-ocean-game/4b731d89-dcfc-4376-9e9b-a5171faf67ef/scratchpad/live_castle"

var main: Node
var cam: Camera3D
var checks_failed := 0

func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("UPSTAIRS|", label, ": ", ("OK" if ok else "FAIL"), (" " + detail if detail != "" else ""))

func _frames(n: int) -> void:
	for i in range(n):
		await process_frame

func _swim(dir: Vector3, n: int) -> void:
	# sustained swim: drag kills a one-shot impulse in ~0.4s, so re-assert vel.
	# n is in 60fps-frame units but paced by WALL CLOCK — headless frame rates
	# vary wildly, and a raw frame count under-travels on a fast machine
	var t0 := Time.get_ticks_msec()
	while Time.get_ticks_msec() - t0 < int(float(n) * 1000.0 / 60.0):
		main.player.vel = dir
		await process_frame

func _shot(name: String, pos: Vector3, look: Vector3) -> void:
	if DisplayServer.get_name() == "headless":
		return
	cam.position = pos
	cam.look_at(look, Vector3.UP)
	await process_frame
	await RenderingServer.frame_post_draw
	var img: Image = get_root().get_viewport().get_texture().get_image()
	img.save_png(OUT + "/" + name + ".png")
	print("UPSTAIRS|shot " + name + ": OK")

func _init() -> void:
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	main.pearl_count = main.PEARL_TOTAL
	for f in main.friends:
		f["found"] = true
		f["won"] = true
	main.trophies = 5
	cam = Camera3D.new()
	cam.fov = 70.0
	get_root().add_child(cam)
	if DisplayServer.get_name() != "headless":
		cam.current = true
	DirAccess.make_dir_recursive_absolute(OUT)
	main._enter_level2()
	await _frames(10)
	main._enter_castle_interior()
	await _frames(20)
	var o: Vector3 = main.CASTLE_POS
	var player: Node3D = main.player
	# ---- zone checks: wing floors hold Roshan up, ceilings cap her ----
	for wing in [{"name": "left_wing", "x": -44.0}, {"name": "right_wing", "x": 44.0}]:
		player.position = o + Vector3(wing["x"], 40.0, -4.0)
		player.vel = Vector3(0, -20, 0)   # dive at the wing floor
		await _frames(40)
		var rel_y: float = player.position.y - o.y
		_ck(String(wing["name"]) + "_floor_holds", rel_y >= 33.5, "rel_y=%.1f" % rel_y)
		player.vel = Vector3(0, 25, 0)    # rush the wing ceiling
		await _frames(40)
		rel_y = player.position.y - o.y
		_ck(String(wing["name"]) + "_ceil_caps", rel_y <= 48.6, "rel_y=%.1f" % rel_y)
	# ---- arch passable: swim from the hall through the middle arch into the left wing ----
	player.position = o + Vector3(-28.0, 40.0, 4.0)
	await _swim(Vector3(-16, 0, 0), 60)
	_ck("arch_passable", player.position.x - o.x < -36.0, "rel_x=%.1f" % (player.position.x - o.x))
	# ---- arcade piers still solid: charge the wall between arches ----
	player.position = o + Vector3(-28.0, 40.0, 14.0)   # pier at z 9..19
	await _swim(Vector3(-16, 0, 0), 60)
	_ck("pier_blocks", player.position.x - o.x > -36.5, "rel_x=%.1f" % (player.position.x - o.x))
	# ---- downstairs unaffected: music room door still enterable ----
	player.position = o + Vector3(-28.0, 6.0, -16.0)
	await _swim(Vector3(-16, 0, 0), 60)
	_ck("music_door_open", player.position.x - o.x < -36.0, "rel_x=%.1f" % (player.position.x - o.x))
	# ---- screenshots ----
	player.position = o + Vector3(0, 6, 24)
	player.vel = Vector3.ZERO
	await _frames(10)
	await _shot("up_hall_arcade", o + Vector3(18, 8, 30), o + Vector3(-35, 41, 4))
	await _shot("up_left_library", o + Vector3(-44, 44, 14), o + Vector3(-48, 36, -20))
	await _shot("up_right_toyroom", o + Vector3(44, 44, 14), o + Vector3(47, 36, -14))
	await _shot("up_back_block", o + Vector3(0, 44, -38), o + Vector3(-30, 36, -58))
	await _shot("up_wing_from_hall", o + Vector3(0, 40, 10), o + Vector3(-44, 38, 2))
	print("UPSTAIRS|done: ", ("OK" if checks_failed == 0 else "FAIL (%d)" % checks_failed))
	quit()
