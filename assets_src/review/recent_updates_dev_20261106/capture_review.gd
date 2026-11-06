extends SceneTree
const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const DEST := "res://assets_src/review/recent_updates_dev_20261106/captures/"
var records: Array[Dictionary] = []
var quality_context: String = "fixed_pc_no_quality_selector"
var profile: Dictionary = {}
func _initialize() -> void:
	call_deferred("_run")
func pose(race: ReefKartRace, along: float) -> void:
	for slot in range(race.karts.size()):
		var k: Dictionary = race.karts[slot]
		k["track_s"] = race.track.wrap_s(along)
		k["race_s"] = along
		k["pos"] = race.track.point_at(along, -28.0 if slot == 0 else 28.0)
		k["lat"] = -28.0 if slot == 0 else 28.0
		k["heading"] = race.track.heading_at(along)
		race.PCDrive.reset(k)
	race.go_t = 0.0
	race._update_camera(1.0, true)
	race._refresh_view()
func refresh(pc: PC) -> void:
	if pc._second_view != null:
		pc._second_view.refresh_camera_view(pc._race, 1.0)
	pc._update_race_ui()
func _run() -> void:
	var version: Dictionary = Engine.get_version_info()
	assert(int(version["major"]) == 4 and int(version["minor"]) == 7 and int(version["patch"]) == 2)
	assert(RenderingServer.get_current_rendering_method() == "mobile")
	assert(DisplayServer.get_name() == "Windows")
	Engine.max_fps = 30
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_EXPAND
	profile = {"version": version, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "frame_cap": Engine.max_fps, "canvas_size": [root.content_scale_size.x, root.content_scale_size.y], "window_size": [root.size.x, root.size.y], "scale_mode": root.content_scale_mode, "scale_aspect": root.content_scale_aspect, "PC_tier_limit": "fixed PC renderer has no separate quality selector; 30fps cap configured", "formal_QA11": false, "device_performance": false}
	var pc := Scene.instantiate() as PC
	root.add_child(pc)
	pc.set_physics_process(false)
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
			race.state = "race"
			var tag := race.track.id + ("-solo" if count == 1 else "-split")
			for zone in range(1):
				var props: Array = race.track.room["zones"][zone]["props"]
				pose(race, race.track.length * float(props[0]["at"]) - 370.0)
				refresh(pc)
				await shot(tag + "-zone-" + str(zone), "posed actual Mobile view")
				pose(race, race.track.length * (float(zone + 1) * 0.25) - 90.0)
				refresh(pc)
				await shot(tag + "-threshold-" + str(zone), "posed section threshold")
	pc.queue_free()
	await process_frame
	var surface := OperaRacerSurface.new()
	root.add_child(surface)
	surface.size = Vector2(1280, 720)
	surface.configure("kart_race", Color.WHITE)
	surface.set_process(false)
	surface.quality = "speedy"
	assert(surface.quality == "speedy")
	quality_context = surface.quality
	await shot("canal-gas", "actual touch layout")
	var file := FileAccess.open(DEST + "captures.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(records, "\t") + "\n")
	var profile_file := FileAccess.open(DEST + "profile.json", FileAccess.WRITE)
	profile_file.store_string(JSON.stringify(profile, "\t") + "\n")
	print("ZONE_CAPTURE|DONE|", records.size())
	quit()
func shot(label: String, kind: String) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var picture := root.get_texture().get_image()
	var path := ProjectSettings.globalize_path(DEST + label + ".png")
	var result := picture.save_png(path)
	records.append({"label":label, "file":label+".png", "size":[picture.get_width(),picture.get_height()], "sha256":FileAccess.get_sha256(path), "save_error":result, "kind":kind, "quality_context":quality_context, "renderer":RenderingServer.get_current_rendering_method()})
	print("ZONE_CAPTURE|", label, "|", result)
