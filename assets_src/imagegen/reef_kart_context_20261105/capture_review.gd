extends SceneTree
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const DEST := "res://assets_src/imagegen/reef_kart_context_20261105/review/candidate/"
var records: Array[Dictionary] = []
func _initialize() -> void:
	call_deferred("_run")
func pose(race: ReefKartRace, along: float) -> void:
	for slot in range(race.karts.size()):
		var k: Dictionary = race.karts[slot]
		k["track_s"] = race.track.wrap_s(along)
		k["pos"] = race.track.point_at(along, -28.0 if slot == 0 else 28.0)
		k["heading"] = race.track.heading_at(along)
	race.go_t = 0.0
	race._update_camera(1.0, true)
	race._refresh_view()
func refresh(pc: PC) -> void:
	if pc._second_view != null:
		pc._second_view.refresh_camera_view(pc._race, 1.0)
	pc._update_race_ui()
func _run() -> void:
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	var pc := Scene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
	await shot("mode")
	pc._show_garage(1, -1)
	await shot("garage")
	pc._toggle_ready(0)
	await shot("course-picker")
	for count in [1, 2]:
		for index in range(4):
			pc._show_garage(count, -1 if count == 1 else 6)
			if count == 2:
				pc._join(11)
			pc._toggle_ready(0)
			if count == 2:
				pc._toggle_ready(1)
			pc._choose_course(index)
			pc._start_race()
			var race: ReefKartRace = pc._race
			var tag := race.track.id + ("-solo" if count == 1 else "-split")
			pose(race, 0.0)
			refresh(pc)
			await shot(tag + "-grid")
			race.state = "race"
			pose(race, race.track.length - 390.0)
			refresh(pc)
			await shot(tag + "-finish-approach")
			pose(race, race.track.s_of([5, 25, 10, 18][index], -55.0))
			refresh(pc)
			await shot(tag + "-bend")
			if count == 1:
				root.size = Vector2i(1600, 900)
				await shot(tag + "-1600x900")
				root.size = Vector2i(1280, 720)
			if count == 1:
				var seen: Dictionary = {}
				for landmark: Dictionary in race.track.landmarks:
					var id := String(landmark["id"])
					if id.begins_with("course_") or id == "turn_marker" or seen.has(id):
						continue
					seen[id] = true
					pose(race, float(landmark["s"]) - 320.0)
					refresh(pc)
					await shot("prop-" + id)
			if index == 2:
				root.size = Vector2i(1280, 800)
				await shot(tag + "-16x10")
				root.size = Vector2i(1280, 720)
			race._pl["item"] = "kelp"
			race.traps.append({"pos":race.track.point_at(float(race._pl["track_s"]) + 190.0), "age":3.0, "owner":1})
			race._refresh_view()
			refresh(pc)
			if index == 2:
				await shot(tag + "-kelp")
			race.state = "finished"
			pc._show_result()
			if index == 0:
				await shot(tag + "-results")
	pc.queue_free()
	await process_frame
	var surface := OperaRacerSurface.new()
	root.add_child(surface)
	surface.size = Vector2(1280, 720)
	surface.configure("kart_race", Color.WHITE)
	surface.set_process(false)
	var canal: ReefKartRace = surface._engine
	pose(canal, 0.0)
	await shot("canal-touch-grid")
	canal.state = "race"
	pose(canal, canal.track.length - 420.0)
	await shot("canal-touch-finish-approach")
	pose(canal, canal.track.s_of(15, -100.0))
	await shot("canal-touch-bend")
	var file := FileAccess.open(DEST + "captures.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(records, "\t") + "\n")
	print("VISUAL_CAPTURE|DONE|", records.size())
	quit()
func shot(label: String) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var path := ProjectSettings.globalize_path(DEST + label + ".png")
	var result := image.save_png(path)
	records.append({"label":label, "file":label+".png", "size":[image.get_width(),image.get_height()], "sha256":FileAccess.get_sha256(path), "save_error":result, "kind":"posed runtime view; not canonical QA11 certification"})
	print("VISUAL_CAPTURE|", label, "|", result)
