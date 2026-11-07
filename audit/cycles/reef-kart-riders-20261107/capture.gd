extends SceneTree

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const SCENE := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const CATALOG := preload("res://scripts/racer/reef_kart_catalog.gd")
const POSES := ["straight", "left", "right", "boost", "spin"]
const COUNT := 12

var pc: PC
var output: String
var count := 0
var failures := 0
var verify_atlases := false

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	root.title = "Reef Grand Prix seated cast visual matrix"
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var args := OS.get_cmdline_user_args()
	output = ProjectSettings.globalize_path(args[0])
	verify_atlases = args.size() > 1 and args[1] == "seated"
	if verify_atlases:
		_check_art()
	DirAccess.make_dir_recursive_absolute(output)
	pc = SCENE.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	if CATALOG.driver_count() != COUNT or CATALOG.RIDES.size() != 3:
		quit(1)
		return
	for players in [1, 2]:
		for ride in range(CATALOG.RIDES.size()):
			for driver in range(CATALOG.driver_count()):
				await _case(players, driver, ride)
	pc._reset_content()
	pc.queue_free()
	await process_frame
	print("SEAT|DONE|", count, "|failures=", failures)
	quit(failures)

func _case(players: int, driver: int, ride: int) -> void:
	pc._show_garage(players, -1 if players == 1 else 6)
	if players == 2:
		pc._join(11)
	pc._drivers[0] = driver
	pc._rides[0] = ride
	pc._drivers[1] = (driver + 5) % COUNT
	pc._rides[1] = (ride + 1) % CATALOG.RIDES.size()
	if verify_atlases and driver == 1:
		pc._build_garage()
		var garage := await _frame()
		if garage.save_jpg(output.path_join("garage-%dp-r%d.jpg" % [players, ride]), 0.88) != OK:
			failures += 1
	for slot in range(players):
		pc._toggle_ready(slot)
	pc._choose_course((driver + ride) % 4)
	pc._start_race()
	var race := pc._race
	if verify_atlases:
		for slot in range(players):
			var k: Dictionary = race.karts[slot]
			var name := String(k["vehicle"])
			var id := String(k["driver"])
			var key := name + ("_straight" if id == "roshan" else "_riders")
			if race._tex.get(key) == null:
				failures += 1
				print("SEAT|FAIL|missing chase art for ", id, " on ", name)
		if players == 2 and not is_same(pc._second_view._tex, race._tex):
			failures += 1
			print("SEAT|FAIL|split-screen cameras do not share chase textures")
	race.state = "race"
	race.go_t = 0.0
	pc._update_race_ui()
	var prefix := "%dp-d%02d-r%d" % [players, driver, ride]
	var station := race.track.length * 0.075
	for index in range(POSES.size()):
		_pose(race, station, index, 100.0)
		var image := await _frame()
		for slot in range(players):
			var x := 640 if players == 1 else (320 if slot == 0 else 960)
			_save(image.get_region(Rect2i(x - 133, 263, 266, 263)), prefix + "-p%d-" % slot + POSES[index])
	if players == 2:
		for direction: float in [-1.0, 1.0]:
			_pose(race, station, 0, 128.0 * direction)
			var image := await _frame()
			var front := 1 if direction > 0 else 0
			var following := race if front == 1 else pc._second_view
			var ahead: Vector2 = race.karts[front]["pos"]
			var on_screen := following.screen_of(ahead) + Vector2(-320.0 if front == 1 else 320.0, 0.0)
			var x := clampi(roundi(on_screen.x), 56 if front == 1 else 696, 584 if front == 1 else 1224)
			var y := clampi(roundi(on_screen.y), 120, 690)
			_save(image.get_region(Rect2i(x - 56, y - 110, 112, 116)), prefix + "-p%d-distance" % front)
	print("SEAT|CASE|", prefix, "|", race.track.id)

func _check_art() -> void:
	var art: GDScript = load("res://scripts/racer/reef_kart_rider_art.gd") as GDScript
	for ride: Dictionary in CATALOG.RIDES:
		var id := String(ride["id"])
		var tex: Texture2D = art.atlas(id)
		if tex == null or tex.get_image().get_mipmap_count() != 10:
			failures += 1
			print("SEAT|FAIL|mipmapped atlas ", id)
		for pose in range(4):
			var authored := load(art.CHASE + id + "_" + art.POSES[pose] + ".png") as Texture2D
			if authored == null or authored.get_image().get_mipmap_count() != 9:
				failures += 1
				print("SEAT|FAIL|authored key mipmaps for ", id, " pose ", pose)
			var box := Rect2(-128, -112.64, 256, 256)
			var registered: Rect2 = art.registered(id, pose, box)
			var axle: Vector2 = art.AXLES[id][pose]
			var contact := registered.position + axle * 256.0 / 627.0
			if contact.distance_to(Vector2(0, 107.52)) > 0.01:
				failures += 1
				print("SEAT|FAIL|authored axle changed with ", id, " pose ", pose)
		print("SEAT|ART|", id, "|mips=10|authored_axles=4")

func _pose(race: ReefKartRace, station: float, pose: int, gap: float) -> void:
	for slot in range(race.karts.size()):
		var k: Dictionary = race.karts[slot]
		var at := station + float(slot) * gap
		var lateral := -29.0 if slot == 0 else 29.0
		k["track_s"] = race.track.wrap_s(at)
		k["race_s"] = at
		k["lat"] = lateral
		k["pos"] = race.track.point_at(at, lateral)
		k["heading"] = race.track.heading_at(at)
		k["steer_vis"] = -0.82 if pose == 1 else (0.82 if pose == 2 else 0.0)
		k["boost_t"] = 0.7 if pose == 3 else 0.0
		k["spin_t"] = 0.42 if pose == 4 else 0.0
		k["spin_vis"] = 1.0 if pose == 4 else 0.0
	race._update_camera(1.0, true)
	race._refresh_view()
	if pc._second_view != null:
		pc._second_view.refresh_camera_view(race, 1.0)

func _frame() -> Image:
	await process_frame
	await RenderingServer.frame_post_draw
	return root.get_texture().get_image()

func _save(image: Image, name: String) -> void:
	var err := image.save_jpg(output.path_join(name + ".jpg"), 0.84)
	if err != OK:
		failures += 1
	count += 1
