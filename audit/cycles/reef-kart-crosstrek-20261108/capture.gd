extends SceneTree

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const ID := "crosstrek_2021_paf"
var failures := 0


func _initialize() -> void:
	call_deferred("_run")


func check(condition: bool, label: String) -> void:
	print("CROSSTREK|", "PASS" if condition else "FAIL", "|", label)
	failures += int(not condition)


func _run() -> void:
	var output := OS.get_cmdline_user_args()[0]
	root.unresizable = true
	root.min_size = Vector2i(1280, 720)
	root.max_size = Vector2i(1280, 720)
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var pc := Scene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	for players: int in [1, 2]:
		for course in range(4):
			pc._show_garage(players, -1 if players == 1 else 6)
			if players == 2:
				pc._join(11)
			for slot in range(players):
				pc._toggle_ready(slot)
			pc._choose_course(course)
			pc._start_race()
			var race := pc._race
			var toys := race.track.landmarks.filter(func(prop: Dictionary) -> bool: return prop["id"] == ID)
			var mode := "%s %dP" % [race.track.id, players]
			check(toys.size() == int(course == 0), mode + " has the intended toy count")
			if course != 0 or toys.size() != 1:
				continue
			var toy: Dictionary = toys[0]
			var shelf := race.track.roadside.filter(func(deck: Dictionary) -> bool:
				return deck["pos"] == toy["pos"] and deck["height"] == toy["lift"])
			check(shelf.size() == 1 and bool(toy["supported"]), mode + " places the toy on the shelf")
			var rail_gap := INF
			for point: Vector2 in race.track.center:
				rail_gap = minf(rail_gap, point.distance_to(toy["pos"]))
			check(rail_gap > ReefKartTrack.RAIL + 22.0, mode + " keeps the toy center off the rails")
			var art := race._landmark_tex.get(ID) as AtlasTexture
			check(art != null and art.atlas.get_image().has_mipmaps(), mode + " loads mipmapped artwork")
			race.state = "race"
			race.go_t = 0.0
			var station := approach(race, toy)
			pose(race, 0, station, -24.0)
			if players == 2:
				pose(pc._second_view, 1, station + 24.0, 18.0)
				check(pc._second_view._landmark_tex.get(ID) == art, "P2 uses the same toy texture")
			pc._update_race_ui()
			await process_frame
			await RenderingServer.frame_post_draw
			var frame := root.get_texture().get_image()
			check(frame != null and frame.save_png(output.path_join("playroom-%dp.png" % players)) == OK,
				mode + " writes the real Mobile viewport")
	pc._reset_content()
	pc.queue_free()
	await process_frame
	print("CROSSTREK|DONE|", failures)
	quit(failures)


func approach(race: ReefKartRace, toy: Dictionary) -> float:
	var track := race.track
	var center: Vector2 = toy["pos"]
	var best_s := float(toy["s"]) - 300.0
	var best_score := INF
	for distance in range(120, 750, 5):
		var s := track.wrap_s(float(toy["s"]) - float(distance))
		var forward := track.tangent_at(s)
		var relative := center - (track.point_at(s) - forward * ReefKartRace.CAM_BACK)
		var depth := relative.dot(forward)
		if depth < 130.0:
			continue
		var scale := ReefKartRace.FOCAL / depth
		var x := absf(forward.cross(relative) * scale)
		var width := float(toy["w"]) * scale
		if x + width * 0.5 > 312.0:
			continue
		var score := absf(x - 165.0) + absf(width - 180.0) * 0.9
		if score < best_score:
			best_score = score
			best_s = s
	print("CROSSTREK|approach=", best_s, "|toy_s=", toy["s"], "|fit=", best_score)
	return best_s


func pose(view: ReefKartRace, slot: int, station: float, lateral: float) -> void:
	var kart := view.karts[slot]
	kart["track_s"] = view.track.wrap_s(station)
	kart["race_s"] = station
	kart["lat"] = lateral
	kart["pos"] = view.track.point_at(station, lateral)
	kart["heading"] = view.track.heading_at(station)
	view._update_camera(0.0, true)
	view._refresh_view()
