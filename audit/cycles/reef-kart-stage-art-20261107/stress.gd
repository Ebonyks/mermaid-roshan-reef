extends SceneTree
## Ten named visual stress passes per course and camera mode. Each pass draws
## three successive track poses spaced like a 300-world-unit/s race.

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const StageArt := preload("res://scripts/racer/reef_kart_stage_art.gd")
const NAMES := ["zone-1", "zone-2", "zone-3", "zone-4", "cross-1-2", "cross-2-3",
	"cross-3-4", "pickup-ready", "pickup-cooldown", "finish-wrap"]

var failures := 0
var total := 0
var output: String
var pc: PC
var race: ReefKartRace


func _initialize() -> void:
	call_deferred("_run")


func check(condition: bool, label: String) -> void:
	print("STAGE|", "OK" if condition else "FAIL", "|", label)
	if not condition:
		failures += 1


func _run() -> void:
	root.title = "Reef Grand Prix stage stress review"
	root.unresizable = true
	root.min_size = Vector2i(1280, 720)
	root.max_size = Vector2i(1280, 720)
	root.size = Vector2i(1280, 720)
	root.content_scale_size = Vector2i(1280, 720)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	output = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(output))
	pc = Scene.instantiate() as PC
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
			race = pc._race
			race.state = "race"
			race.go_t = 0.0
			var label := "%s-%dp" % [race.track.id, players]
			var pieces: Array[Dictionary] = []
			for prop: Dictionary in race.track.landmarks:
				if prop.has("stage_zone"):
					check(StageArt.clears_course(race.track, prop["pos"], float(prop["w"]) * 0.5, pieces),
						label + " clear footprint " + String(prop["id"]))
					var tile: AtlasTexture = race._landmark_tex.get(prop["id"])
					check(tile != null and tile.atlas.get_image().get_mipmap_count() == 10,
						label + " mip chain " + String(prop["id"]))
					pieces.append(prop)
			check(pieces.size() == 4, label + " four unique set pieces")
			if pieces.size() != 4:
				continue
			var active: AtlasTexture = race._tex["item_bubble"]
			var inactive: AtlasTexture = race._tex["socket_empty"]
			check(active.atlas == inactive.atlas and active.atlas.get_image().get_mipmap_count() == 9,
				label + " pickup states share mipmapped atlas")
			if players == 2:
				check(is_same(pc._second_view.track, race.track) and pc._second_view._tex["socket_empty"] == inactive,
					label + " seats see shared pickup state and assets")
			var quarter := race.track.length * 0.25
			var pickup_s := float(race.track.bubbles[1]["s"])
			for trial in range(NAMES.size()):
				var first: float
				var second: float
				if trial < 4:
					first = float(pieces[trial]["approach"]) - 22.0
					second = float(pieces[(trial + 2) % 4]["approach"]) - 22.0
				elif trial < 7:
					first = quarter * (trial - 3) - 26.0
					second = quarter * ((trial - 2) % 4) - 34.0
				elif trial < 9:
					first = pickup_s - 100.0
					second = pickup_s - 129.0
					if trial == 8:
						_take_pickup(label)
				else:
					first = race.track.length - 34.0
					second = race.track.length - 42.0
				for frame in range(3):
					var advance := float(frame) * 26.0
					_pose(0, first + advance, -9.0, trial, frame)
					if players == 2:
						_pose(1, second + advance, 19.0, trial, frame)
					var name := label + "-" + String(NAMES[trial]) + "-" + str(frame)
					await _capture(name)
				if trial == 8:
					race._tick_pickups(3.1)
					check(float(race.track.bubbles[1]["respawn_t"]) == 0.0, label + " socket refills")
	pc._reset_content()
	pc.queue_free()
	await process_frame
	print("STAGE|DONE|", total, "|failures=", failures)
	quit(failures)


func _take_pickup(label: String) -> void:
	var k := race.karts[0]
	var pickup := race.track.bubbles[1]
	k["pos"] = pickup["pos"]
	k["item"] = ""
	k["roulette_t"] = 0.5
	race._contact_features(k, 0.0)
	check(float(pickup["respawn_t"]) == 0.0, label + " occupied roulette leaves capsule ready")
	k["roulette_t"] = 0.0
	race._contact_features(k, 0.0)
	check(float(pickup["respawn_t"]) > 0.0 and float(k["roulette_t"]) > 0.0,
		label + " successful contact starts cooldown and roulette")
	race._contact_features(k, 2.0)
	check(String(k["item"]) in race.ITEM_KINDS, label + " cooldown follows a real award")
	k["item"] = ""


func _pose(slot: int, station: float, lateral: float, trial: int, frame: int) -> void:
	var k := race.karts[slot]
	var track := race.track
	k["track_s"] = track.wrap_s(station)
	k["race_s"] = station
	k["lat"] = lateral
	k["pos"] = track.point_at(station, lateral)
	k["heading"] = track.heading_at(station) + (0.035 if trial >= 4 and frame == 2 else 0.0)
	race.PCDrive.reset(k)
	k["speed"] = 300.0
	k["velocity"] = track.tangent_at(station) * 300.0
	if slot == 0:
		race._time += 0.087
		race._update_camera(1.0, true)
		race._refresh_view()
	else:
		pc._second_view.refresh_camera_view(race, 2.0)
	pc._update_race_ui()


func _capture(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var frame := root.get_texture().get_image()
	if frame.get_size() != Vector2i(1280, 720):
		check(false, name + " capture dimensions")
		return
	frame.resize(640, 360, Image.INTERPOLATE_LANCZOS)
	if frame.save_jpg(output.path_join(name + ".jpg"), 0.82) == OK:
		total += 1
	else:
		check(false, name + " capture write")
