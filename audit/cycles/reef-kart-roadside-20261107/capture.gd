extends SceneTree
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const Roadside := preload("res://scripts/racer/reef_kart_roadside.gd")
var failures := 0
var total := 0
var output := "res://tmp/roadside/poses"

func _initialize() -> void:
	call_deferred("_run")

func check(condition: bool, label: String) -> void:
	print("ROADSIDE|", "OK" if condition else "FAIL", "|", label)
	if not condition:
		failures += 1

func _run() -> void:
	root.title = "Reef Grand Prix roadside review"
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output))
	var pc := Scene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	for players in [1, 2]:
		for course in range(4):
			pc._show_garage(players, -1 if players == 1 else 6)
			if players == 2:
				pc._join(11)
			for slot in range(players):
				pc._toggle_ready(slot)
			pc._choose_course(course)
			pc._start_race()
			var race := pc._race
			var name := "%s-%dp" % [race.track.id, players]
			var main_count := 0
			var zones: Dictionary = {}
			var valid := true
			for deck: Dictionary in race.track.roadside:
				valid = valid and Roadside._clears_route(race.track, deck["pos"], deck["along"], deck["across"], deck["half"],
					ReefKartTrack.RAIL + 12.0)
				if bool(deck["main"]):
					main_count += 1
					zones[deck["zone"]] = deck
			check(main_count == 4 and zones.size() == 4 and race.track.roadside.size() == 12, name + " four scene bays and eight low trims")
			check(valid, name + " all rectangles clear every rail sample")
			check(race._fascia.get_image().get_mipmap_count() == 10, name + " imported painted atlas has ten mip levels")
			if players == 2:
				check(is_same(pc._second_view.track, race.track) and pc._second_view._fascia == race._fascia,
					name + " shared scenery and texture across cameras")
			race.state = "race"
			race.go_t = 0.0
			for zone in range(4):
				if not zones.has(zone):
					continue
				var deck: Dictionary = zones[zone]
				var station := best_approach(race, deck, 390.0 if players == 1 else 555.0)
				pose(race, station)
				if players == 2:
					pc._second_view.refresh_camera_view(race, 1.0)
				pc._update_race_ui()
				await shot(name + "-z" + str(zone + 1))
				if players == 1:
					pose(race, station + 118.0)
					await shot(name + "-close" + str(zone + 1))
	pc._reset_content()
	pc.queue_free()
	await process_frame
	print("ROADSIDE|DONE|", total, "|failures=", failures)
	quit(failures)

func best_approach(race: ReefKartRace, deck: Dictionary, goal: float) -> float:
	var station := float(deck["s"])
	var fixture: Vector2 = deck["pos"]
	var best := station - goal
	var score := INF
	for step in range(42):
		var at := station - float(step) * 20.0
		var heading := race.track.heading_at(at)
		var fwd := Vector2(sin(heading), -cos(heading))
		var from_eye := fixture - (race.track.point_at(at) - fwd * ReefKartRace.CAM_BACK)
		var depth := from_eye.dot(fwd)
		if depth < 120.0:
			continue
		var side := absf(from_eye.dot(Vector2(-fwd.y, fwd.x)) * ReefKartRace.FOCAL / depth)
		var cost := absf(depth - goal) * 0.7 + absf(side - (330.0 if goal < 500.0 else 235.0))
		if cost < score:
			score = cost
			best = at
	return best

func pose(race: ReefKartRace, station: float) -> void:
	for slot in range(race.karts.size()):
		var k: Dictionary = race.karts[slot]
		var at := station + float(slot) * 110.0
		var lateral := -16.0 if slot == 0 else 16.0
		k["track_s"] = race.track.wrap_s(at)
		k["race_s"] = at
		k["lat"] = lateral
		k["pos"] = race.track.point_at(at, lateral)
		k["heading"] = race.track.heading_at(at)
		race.PCDrive.reset(k)
	race._update_camera(1.0, true)
	race._refresh_view()

func shot(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var frame := root.get_texture().get_image()
	check(frame.save_jpg(output + "/" + name + ".jpg", 0.90) == OK, name)
	total += 1
