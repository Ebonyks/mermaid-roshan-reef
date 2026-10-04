extends SceneTree
# Feature/contact regression for the existing engine's Canvas conversion.
# The established probe_kart_feel remains the timing/save/pack gate.
var main: Node
var race: KartGame
var failures := 0
var capture := false
const OUTPUT := "res://audit/job_game_refinement_20261003/racer/captures/"

func check(label: String, passed: bool) -> void:
	print("KART2D|", "PASS|" if passed else "FAIL|", label)
	if not passed:
		failures += 1

func _init() -> void:
	capture = "--capture-racer" in OS.get_cmdline_user_args()
	seed(7)
	call_deferred("run")

func run() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate()
	get_root().add_child(main)
	await process_frame
	main._skip_intro()
	await process_frame
	main.set_process(false)
	main._start_menu_ref()._dismiss_menu()
	await process_frame
	main._start_kart_game_now(false, "float")
	race = main.kart_game
	race.set_process(false)
	print("KART2D|SOURCE|kart=", FileAccess.get_sha256("res://scripts/kart.gd"), " canvas=", FileAccess.get_sha256("res://scripts/kart_canvas_2d.gd"), " probe=", FileAccess.get_sha256("res://scripts/probe_kart_canvas_2d.gd"))
	check("developed engine root is Node2D", race is Node2D)
	check("engine subtree has zero spatial nodes", no_spatial(race))
	check("three rides and eight paints retained", race._vehicle_keys().size() == 3 and race.PAINTS.size() == 8)
	check("handling identities retained", float(race.VEHICLES.moto.vmax) > float(race.VEHICLES.kart.vmax) and float(race.VEHICLES.truck.mass) > float(race.VEHICLES.kart.mass))
	if capture:
		await screenshot("01_ride_selection")
		await choose_picture_by_touch()
		await screenshot("01b_paint_selection")
		race._sel_phase = "ride"
		race._sel_idx = 1
		race._select_confirm_queued = false
		race._lbl_big.text = "" if race._minimal() else "Pick your ride!"
		race._refresh_select_controls()
		await screenshot("01c_tablet_picture_targets", Vector2i(1280, 800))
		await choose_picture_by_touch()
		get_root().size = Vector2i(1280, 720)
		await process_frame
	# Use the real selection transition so captures keep the actual race HUD.
	race._sel_idx = 1
	race._sel_phase = "paint"
	race._paint_idx = 2
	race._sel_t = 0.61
	race._select_confirm_queued = true
	race._tick_select(0.01)
	race._state = "race"
	race._refresh_select_controls()
	for k in race._karts:
		race._place_kart(k, 0.0)
	check("full eight-racer pack retained", race._karts.size() == 8)
	check("all strips/items/ramps/pearls/hazards retained", race._strip_data.size() == 7 and race._pickups_live.size() == 11 and race._ramp_data.size() == 3 and race._pearls_live.size() == 33 and race._hazards_live.size() == 6)
	var pl: Dictionary = race._pl
	var node: Node2D = pl["node"]
	# Braking lowers the same auto-cruise target, without touching turbo state.
	pl["speed"] = race._vmax
	race._update_player(pl, 0.0, true, false, 0.5)
	check("desktop brake lowers speed", float(pl["speed"]) < race._vmax * 0.75)
	# A wall gently rebounds; it never removes progress or stops the race.
	pl["speed"] = race._vmax
	var before_s: float = pl["s"]
	race._apply_lat(pl, 100.0)
	check("soft wall retains progress", float(pl["s"]) == before_s and float(pl["speed"]) > 0.0 and float(pl["lat"]) < 20.0)
	# Every item must pay its original immediate effect, not merely a visual burst.
	var pickups: Array = race._pickups_live.duplicate()
	for kind in ["shell", "star", "bubble", "rainbow"]:
		var item: Dictionary = {}
		for pu in pickups:
			if pu["kind"] == kind:
				item = pu
				break
		pl["s"] = item["s"]
		pl["lat"] = item["lat"]
		pl["meter"] = 0.0
		pl["boost_t"] = 0.0
		item["cool"] = 0.0
		race._place_kart(pl, 0.0)
		race._pickups_live = [item]
		race._check_pickups(0.0)
		check("pickup " + kind + " immediate boost and cooldown", float(pl["boost_t"]) >= 0.39 and float(item["cool"]) == 6.0)
		if kind == "rainbow":
			check("rainbow fills meter", float(pl["meter"]) == 1.0)
	race._pickups_live = pickups
	var ramp: Dictionary = race._ramp_data[0]
	pl["s"] = ramp["s"]
	pl["lat"] = ramp["lat"]
	pl["air_t"] = 0.0
	race._place_kart(pl, 0.0)
	race._check_ramps()
	check("ramp starts full hang time", is_equal_approx(float(pl["air_t"]), race.AIR_DUR))
	pl["hop"] = 0.0
	pl["air_t"] = race.AIR_DUR * 0.5
	race._place_kart(pl, 0.0)
	check("ramp apex lifts from its contact shadow", is_equal_approx(float(pl["lift"]), 5.0))
	race._update_camera(1.0)
	if capture:
		await screenshot("02_ramp_apex")
	pl["boost_t"] = 0.0
	race._place_kart(pl, race.AIR_DUR)
	check("landing pays original free boost", float(pl["boost_t"]) >= 0.5 and float(pl["lift"]) < 0.001)
	pl["s"] = race.SHORTCUT_FROM_U * race._len
	pl["lat"] = race._rhalf() * 0.78
	race._place_kart(pl, 0.0)
	race._check_shortcut()
	var shortcut_s: float = pl["s"]
	check("shortcut advances to original exit", is_equal_approx(shortcut_s, race.SHORTCUT_TO_U * race._len))
	pl["s"] = race.SHORTCUT_FROM_U * race._len
	race._place_kart(pl, 0.0)
	race._check_shortcut()
	check("shortcut is limited to once per lap", is_equal_approx(float(pl["s"]), race.SHORTCUT_FROM_U * race._len))
	race._rev = true
	var reverse_curve := race._curv_at(30.0)
	race._rev = false
	check("reverse preserves opposite signed curvature", is_equal_approx(reverse_curve, -race._curv_at(race._len - 30.0)))
	# Heavy truck gets the original shove advantage; player boost survives it.
	var rival: Dictionary = race._karts[1]
	var rival_node: Node2D = rival["node"]
	var full_pack: Array = race._karts.duplicate()
	race._karts = [pl, rival]
	pl["veh"] = "moto"
	rival["veh"] = "truck"
	pl["speed"] = 25.0
	rival["speed"] = 25.0
	pl["boost_t"] = 0.8
	pl["lat"] = 0.0
	rival["lat"] = 1.0
	node.position = Vector2.ZERO
	rival_node.position = Vector2(1, 0)
	node.set_meta("height", 0.0)
	rival_node.set_meta("height", 0.0)
	race._resolve_collisions()
	check("mass-weighted collision and player turbo retained", float(rival["speed"]) > float(pl["speed"]) and float(pl["boost_t"]) == 0.8)
	race._karts = full_pack
	pl["veh"] = "kart"
	pl["speed"] = race._vmax
	pl["s"] = race._len * 1.98
	pl["lat"] = 0.0
	pl["hop"] = 0.0
	pl["air_t"] = 0.0
	pl["boost_t"] = 0.0
	race._place_kart(pl, 0.0)
	race._update_camera(1.0)
	if capture:
		await screenshot("03_finish_approach")
	pl["s"] = race._len * 2.001
	race._place_kart(pl, 0.0)
	race._player_acted = true
	race._finish()
	if capture:
		await screenshot("04_finish_crossing")
		await create_timer(0.75).timeout
		await screenshot("05_result_settle")
	check("finish settles in positive podium state", race._state == "podium")
	print("KART2D|ALL OK" if failures == 0 else "KART2D|FAILURES=" + str(failures))
	quit(0 if failures == 0 else 1)

func no_spatial(node: Node) -> bool:
	if node.get_class().ends_with("3D"):
		return false
	for child in node.get_children():
		if not no_spatial(child):
			return false
	return true

func screenshot(label: String, resolution: Vector2i = Vector2i(1280, 720)) -> void:
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	get_root().size = resolution
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_texture().get_image()
	var result := image.save_png(OUTPUT + label + ".png")
	check("capture " + label, result == OK and image.get_width() >= 1280)
func choose_picture_by_touch() -> void:
	var button: Button = race._ride_choice_buttons[0]
	var bounds := button.get_global_rect()
	var target := bounds.position + bounds.size * Vector2(0.5, 0.3)
	var press := InputEventScreenTouch.new()
	press.index = 51
	press.position = target
	press.pressed = true
	Input.parse_input_event(press)
	await process_frame
	var release := InputEventScreenTouch.new()
	release.index = 51
	release.position = target
	release.pressed = false
	Input.parse_input_event(release)
	await process_frame
	check("actual screen touch selects pictured motorcycle", race._sel_idx == 0 and race._select_confirm_queued)
	race._sel_t = 0.61
	race._tick_select(0.01)
	check("pictured touch advances to paint choice", race._sel_phase == "paint")
