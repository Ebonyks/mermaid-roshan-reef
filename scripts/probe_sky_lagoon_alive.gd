extends SceneTree

## Bot test for the standalone Sky Lagoon "alive painting" demo.
##
##     godot --headless -s scripts/probe_sky_lagoon_alive.gd
##     xvfb-run -a godot --rendering-method mobile -s scripts/probe_sky_lagoon_alive.gd
##
## Headless runs check classification, every tap reaction, Roshan travel and
## twirl, animal startles and that nothing is written to the save. With a real
## renderer it also measures, in memory only, that painted water/foliage/cloud
## regions move while the path stays steady, and that the M toggle stops the
## painting motion. No capture is written to disk.

const DEMO_SCENE := "res://scenes/demo/sky_lagoon_alive.tscn"
const SAVE_PATH := "user://reef_save.json"

var demo: Node2D
var failures := 0


func _initialize() -> void:
	_run.call_deferred()


func _check(ok: bool, label: String, detail: String = "") -> void:
	if ok:
		print("SKY_ALIVE| OK   %s %s" % [label, detail])
	else:
		failures += 1
		print("SKY_ALIVE| FAIL %s %s" % [label, detail])


func _frames(count: int) -> void:
	for _i: int in range(count):
		await process_frame


func _seconds(seconds: float) -> void:
	var start: int = Time.get_ticks_msec()
	while float(Time.get_ticks_msec() - start) / 1000.0 < seconds:
		await process_frame


func _run() -> void:
	var save_existed: bool = FileAccess.file_exists(SAVE_PATH)
	var save_stamp: int = FileAccess.get_modified_time(SAVE_PATH) if save_existed else 0
	var packed: PackedScene = load(DEMO_SCENE) as PackedScene
	_check(packed != null, "scene_loads")
	if packed == null:
		quit(1)
		return
	demo = packed.instantiate() as Node2D
	root.add_child(demo)
	await _frames(10)

	_check(demo.get_node_or_null("AlivePainting") is Polygon2D, "painting_node")
	_check(demo.get("animals").size() == 4, "animals_placed", str(demo.get("animals").size()))
	_check(demo.get("butterflies").size() == 3, "butterflies_placed")
	var cases: Array = [
		[Vector2(5200, 1250), "water"], [Vector2(200, 1300), "water"],
		[Vector2(4300, 1400), "foliage"], [Vector2(150, 500), "foliage"],
		[Vector2(1800, 1050), "cloud"], [Vector2(2000, 300), "sky"],
		[Vector2(2800, 1350), "ground"], [Vector2(2400, 1620), "ground"],
	]
	for item: Array in cases:
		var at: Vector2 = item[0] as Vector2
		var expected: String = item[1] as String
		var got: String = demo.call("material_at", at) as String
		_check(got == expected, "classify_%s" % expected, "%s -> %s" % [at, got])

	# Every kind of touch answers, and nothing is ever counted as a win.
	var taps: Array = [
		[Vector2(5300, 1300), "water"], [Vector2(4300, 1400), "foliage"],
		[Vector2(1800, 1050), "cloud"], [Vector2(2000, 300), "sky"],
		[Vector2(4790, 500), "cabin"],
	]
	for item: Array in taps:
		var kind: String = demo.call("tap_master", item[0] as Vector2) as String
		_check(kind == (item[1] as String), "tap_%s" % item[1], kind)
		await _frames(2)
	var hare: Dictionary = {}
	for animal: Dictionary in demo.get("animals"):
		if animal["id"] == "hare":
			hare = animal
	if not hare.is_empty():
		var hare_point: Vector2 = (hare["contact"] as Vector2) - Vector2(0, 100)
		_check(demo.call("tap_master", hare_point) == "animal", "tap_animal")
		await _frames(3)
		_check((hare["startle_left"] as float) > 0.0, "animal_startles")
		var hare_sprite: Sprite2D = hare["sprite"] as Sprite2D
		_check(hare_sprite.texture == hare["startle"], "animal_uses_startle_atlas")

	var start_x: float = demo.call("roshan_master_x") as float
	var body := Vector2(start_x, 1650.0 - 172.0)
	_check(demo.call("tap_master", body) == "roshan", "tap_roshan")
	await _frames(3)
	_check((demo.get("roshan_twirl_left") as float) > 0.0, "roshan_twirls")
	await _seconds(1.4)
	_check(demo.call("tap_master", Vector2(3600, 1700)) == "ground", "tap_ground")
	await _seconds(4.0)
	var end_x: float = demo.call("roshan_master_x") as float
	_check(absf(end_x - 3600.0) < 12.0, "roshan_travels", "%.0f -> %.0f" % [start_x, end_x])
	var roshan_sprite: Sprite2D = demo.get_node("Roshan") as Sprite2D
	_check(roshan_sprite.position.y > 1100.0 and roshan_sprite.position.y < 1600.0,
		"roshan_on_route", str(roshan_sprite.position))

	_check((demo.get("reaction_log") as Array).size() >= 8, "reaction_log")
	var after_exists: bool = FileAccess.file_exists(SAVE_PATH)
	var after_stamp: int = FileAccess.get_modified_time(SAVE_PATH) if after_exists else 0
	_check(after_exists == save_existed and after_stamp == save_stamp, "no_save_written")

	if DisplayServer.get_name() != "headless":
		await _measure_motion()
	else:
		print("SKY_ALIVE| SKIP motion_measurement (headless: no renderer)")
	_measure_frame_time()
	await _seconds(1.0)
	print("SKY_ALIVE| %s failures=%d" % ["PASS" if failures == 0 else "FAIL", failures])
	demo.queue_free()
	await _frames(2)
	quit(0 if failures == 0 else 1)


var frame_samples: Array[float] = []


func _measure_frame_time() -> void:
	# Informational only: desktop/Xvfb timing is not phone evidence.
	var fps: float = Engine.get_frames_per_second()
	print("SKY_ALIVE| INFO fps_reported=%.1f renderer=%s" % [fps,
		RenderingServer.get_current_rendering_method()])


func _grab() -> Image:
	await RenderingServer.frame_post_draw
	return root.get_viewport().get_texture().get_image()


func _region_change(a: Image, b: Image, rect: Rect2i) -> float:
	var total := 0.0
	var count := 0
	for y: int in range(rect.position.y, rect.end.y, 3):
		for x: int in range(rect.position.x, rect.end.x, 3):
			var ca: Color = a.get_pixel(x, y)
			var cb: Color = b.get_pixel(x, y)
			total += absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b)
			count += 1
	return total / float(maxi(1, count)) * 255.0 / 3.0


func _screen_rect(master_rect: Rect2) -> Rect2i:
	var xf: Transform2D = demo.get_canvas_transform()
	var a: Vector2 = xf * master_rect.position
	var b: Vector2 = xf * master_rect.end
	var size: Vector2 = root.get_viewport().get_visible_rect().size
	var r := Rect2(a, b - a).intersection(Rect2(Vector2.ZERO, size))
	return Rect2i(r)


func _measure_motion() -> void:
	# Send Roshan off-screen left, then park the camera over the right lake so
	# water, shrubs, sky and bare path share a frame with nothing else moving.
	demo.set("roshan_target_x", 700.0)
	await _seconds(6.0)
	demo.call("park_camera", 4400.0, 60.0)
	await _seconds(2.0)
	var regions := {
		"water": Rect2(5000, 1150, 500, 200),
		"foliage": Rect2(4150, 1300, 300, 200),
		"cloud_sky": Rect2(5150, 140, 500, 170),
		"path_steady": Rect2(3650, 1590, 280, 40),
	}
	demo.set("camera_breathing", false)
	await _seconds(0.5)
	demo.call("set_motion", true)
	var a: Image = await _grab()
	await _seconds(0.7)
	var b: Image = await _grab()
	var moving := {}
	for key: String in regions:
		var rect: Rect2i = _screen_rect(regions[key] as Rect2)
		if rect.size.x < 8 or rect.size.y < 8:
			print("SKY_ALIVE| SKIP motion_%s offscreen" % key)
			continue
		moving[key] = _region_change(a, b, rect)
	demo.call("set_motion", false)
	var c: Image = await _grab()
	await _seconds(0.7)
	var d: Image = await _grab()
	for key: String in moving:
		var rect: Rect2i = _screen_rect(regions[key] as Rect2)
		var still: float = _region_change(c, d, rect)
		var value: float = moving[key] as float
		print("SKY_ALIVE| INFO motion_%s on=%.2f off=%.2f" % [key, value, still])
		if key == "path_steady":
			_check(value < 1.0, "path_does_not_sway", "%.2f" % value)
			_check(still < 0.6, "motion_off_is_still_%s" % key, "%.2f" % still)
		else:
			_check(value > 1.0, "motion_visible_%s" % key, "%.2f" % value)
			_check(still < value * 0.35, "motion_toggle_%s" % key, "%.2f vs %.2f" % [still, value])
	demo.call("set_motion", true)
	demo.set("camera_breathing", true)
