extends Node
## Entry scene for the isolated Windows playtest package.

const PC := preload("res://scripts/racer/reef_kart_pc.gd")
const Scene := preload("res://scenes/racer/reef_grand_prix_pc.tscn")
const Catalog := preload("res://scripts/racer/reef_kart_catalog.gd")
const Trace := preload("res://controller_trace.gd")


func _ready() -> void:
	var arguments := OS.get_cmdline_user_args()
	var pc := _controller_trace() if "--controller-trace" in arguments else Scene.instantiate() as PC
	if pc == null:
		get_tree().quit(1)
		return
	pc._mode_choice = 1
	add_child(pc)
	if "--verify-portable" in arguments:
		_verify_portable.call_deferred(pc)


func _controller_trace() -> PC:
	var pc := Trace.TracePC.new()
	var output := OS.get_executable_path().get_base_dir().path_join("controller-trace.jsonl")
	pc.trace = FileAccess.open(output, FileAccess.WRITE)
	if pc.trace == null:
		OS.alert("Extract the demo into a writable folder to save the controller trace.", "Reef Grand Prix")
		pc.free()
		return null
	pc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	Input.joy_connection_changed.connect(pc.scan)
	for id: int in Input.get_connected_joypads():
		pc.scan(id, true)
	pc.record("ready", {"engine": Engine.get_version_info()["string"], "detected": Input.get_connected_joypads().size()})
	pc.trace.flush()
	return pc


func _verify_portable(pc: PC) -> void:
	pc.set_physics_process(false)
	var failures := 0
	for driver in range(Catalog.driver_count()):
		var cast_member := Catalog.driver(driver)
		failures += int(Catalog.portrait(cast_member) == null)
		failures += int(PC.RiderArt.motion_atlas(String(cast_member["id"])) == null)
		for ride: Dictionary in Catalog.RIDES:
			failures += int(PC.RiderArt.preview(cast_member["id"], ride["id"]) == null)
	for key: String in ["zoom", "kelp", "pearls", "sparkle", "sparkle_duel"]:
		failures += int(not ResourceLoader.exists("res://assets/audio/objective_guides/guide_kart_" + key + ".ogg"))
	pc._show_garage(2, 6)
	pc._join(11)
	pc._toggle_ready(0)
	pc._toggle_ready(1)
	for course in range(PC.Courses.COURSES.size()):
		pc._choose_course(course)
		pc._start_race()
		var race := pc._race
		if race == null or pc._second_view == null:
			failures += 1
			continue
		var missing := 0
		for landmark: Dictionary in race.track.landmarks:
			missing += int(not race._landmark_tex.has(String(landmark["id"])))
		var loaded := race._room_art != null and race._fascia != null 			and race._tex.has("item_bubble") and race._tex.has("socket_empty") and missing == 0 			and is_same(race.track, pc._second_view.track)
		print("PORTABLE|", race.track.id, "|two_seats=", pc._devices == [6, 11], "|assets=", loaded)
		failures += int(not loaded or pc._devices != [6, 11])
		pc._return_to_garage()
		await get_tree().process_frame
	print("PORTABLE|DONE|", failures)
	get_tree().quit(failures)
