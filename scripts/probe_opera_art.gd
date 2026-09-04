extends SceneTree
## Fail-closed Mobile-render capture for the visible Castle-to-Opera routes.
##
## A fresh run writes two independent aspect manifests. Each records eight
## non-Hall Castle route views, all three physical Opera venue floors, and the
## live career states entered through the guarded production route callback.
## These are machine-review artifacts, never device/child/owner acceptance.

const SCHEMA := "reef.opera.route_capture.v1"
const MANIFEST_NAME := "opera_capture_manifest.json"
const CAPTURE_METHOD := "same_process_viewport"
const ROUTE_ENTRY_METHOD := "guarded_castle_career_route_launch"
const READY_FRAME_LIMIT := 240
const VENUE_READY_FRAME_LIMIT := 1200
const VENUE_READY_TIMEOUT_MSEC := 5000
const ASPECTS: Array[Vector2i] = [
	Vector2i(1280, 720),
	Vector2i(1600, 720),
]
const NON_HALL_ROOMS: Array[String] = [
	"kitchen", "library", "craft_room", "playroom", "bubble_bath",
	"mermaid_pool", "dining_room", "movie_lounge",
]
const VENUE_FLOOR_ACTS: Array[int] = [2, 8, 13]
const SOURCE_FIXED_FILES: Array[String] = [
	"project.godot",
	"tools/audit_opera_capture.py",
]
const SOURCE_TREE_ROOTS: Array[String] = [
	"assets", "scenes", "scripts", "shaders",
]
const SOURCE_TREE_SUFFIXES := {
	"assets": [
		".bmp", ".dds", ".exr", ".gdshader", ".hdr", ".import", ".jpeg",
		".jpg", ".json", ".ktx", ".mp3", ".ogg", ".png", ".svg", ".tga",
		".uid", ".wav", ".webp",
	],
	"scenes": [".res", ".tres", ".tscn", ".uid"],
	"scripts": [".gd", ".uid"],
	"shaders": [".gdshader", ".uid"],
}

var main: ReefMain
var rooms: CastleRooms25D
var routes: CastleCareerRoutes
var out_dir := ""
var aspect_dir := ""
var aspect_size := Vector2i.ZERO
var run_nonce := ""
var states: Array[Dictionary] = []
var global_failures: Array[Dictionary] = []
var capture_source_signature: Dictionary = {}
var capture_frame_drawn := false


func _init() -> void:
	call_deferred("_run")


func _settle(frames: int) -> void:
	for _frame: int in range(frames):
		await process_frame


func _fail(code: String, detail: String) -> void:
	global_failures.append({"code": code, "detail": detail})
	print("OPERASHOT|GLOBAL|FAIL|%s|%s" % [code, detail])


func _directory_entries(path: String) -> Array[String]:
	var entries: Array[String] = []
	if not DirAccess.dir_exists_absolute(path):
		return entries
	for directory_name: String in DirAccess.get_directories_at(path):
		entries.append(directory_name + "/")
	for file_name: String in DirAccess.get_files_at(path):
		entries.append(file_name)
	entries.sort()
	return entries


func _prepare_fresh_output() -> bool:
	var error := DirAccess.make_dir_recursive_absolute(out_dir)
	if error != OK:
		print("OPERASHOT|RESULT|FAIL|output_directory=%d" % error)
		return false
	var prior := _directory_entries(out_dir)
	if not prior.is_empty():
		print("OPERASHOT|RESULT|FAIL|stale_output=%s" % str(prior))
		return false
	return true


func _aspect_id(size: Vector2i) -> String:
	return "%dx%d" % [size.x, size.y]


func _set_aspect(size: Vector2i) -> bool:
	get_root().mode = Window.MODE_WINDOWED
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	await process_frame
	for _frame: int in range(READY_FRAME_LIMIT):
		# Windows applies a maximized-to-windowed transition asynchronously.
		# Reassert the requested client size after that transition instead of
		# accepting the monitor-sized backing texture as capture evidence.
		get_root().size = size
		DisplayServer.window_set_size(size)
		await process_frame
		var image: Image = get_root().get_viewport().get_texture().get_image()
		if image != null and image.get_size() == size:
			return true
	return false


func _engine_contract() -> Dictionary:
	var version := Engine.get_version_info()
	return {
		"major": int(version.get("major", -1)),
		"minor": int(version.get("minor", -1)),
		"patch": int(version.get("patch", -1)),
		"status": String(version.get("status", "")),
		"build": String(version.get("build", "")),
		"version_string": String(version.get("string", "")),
	}


func _exact_engine() -> bool:
	var engine := _engine_contract()
	return int(engine["major"]) == 4 and int(engine["minor"]) == 7 \
		and int(engine["patch"]) == 1 and String(engine["status"]) == "stable" \
		and String(engine["build"]) == "official"


func _source_suffixes(root_name: String) -> Array[String]:
	var suffixes: Array[String] = []
	var raw_suffixes: Array = SOURCE_TREE_SUFFIXES.get(root_name, []) as Array
	for value: Variant in raw_suffixes:
		suffixes.append(String(value))
	return suffixes


func _source_file_matches(file_name: String, suffixes: Array[String]) -> bool:
	var lower_name := file_name.to_lower()
	for suffix: String in suffixes:
		if lower_name.ends_with(suffix):
			return true
	return false


func _collect_source_tree(relative_dir: String, suffixes: Array[String],
		paths: Array[String], missing: Array[String]) -> void:
	var resource_dir := "res://" + relative_dir
	if not DirAccess.dir_exists_absolute(resource_dir):
		missing.append(relative_dir + "/")
		return
	var file_names := DirAccess.get_files_at(resource_dir)
	file_names.sort()
	for file_name: String in file_names:
		if _source_file_matches(file_name, suffixes):
			paths.append(relative_dir + "/" + file_name)
	var directory_names := DirAccess.get_directories_at(resource_dir)
	directory_names.sort()
	for directory_name: String in directory_names:
		_collect_source_tree(
			relative_dir + "/" + directory_name, suffixes, paths, missing)


func _source_path_contract() -> Dictionary:
	var paths: Array[String] = SOURCE_FIXED_FILES.duplicate()
	var missing: Array[String] = []
	var tree_rules: Array[Dictionary] = []
	for root_name: String in SOURCE_TREE_ROOTS:
		var suffixes := _source_suffixes(root_name)
		tree_rules.append({"root": root_name, "suffixes": suffixes})
		_collect_source_tree(root_name, suffixes, paths, missing)
	paths.sort()
	missing.sort()
	return {
		"paths": paths,
		"missing": missing,
		"tree_rules": tree_rules,
	}


func _source_signature() -> Dictionary:
	var contract := _source_path_contract()
	var source_paths: Array = contract.get("paths", []) as Array
	var file_hashes: Dictionary = {}
	var missing: Array = contract.get("missing", []) as Array
	var entries: Array[String] = []
	for relative_value: Variant in source_paths:
		var relative := String(relative_value)
		var resource_path := "res://" + relative
		var digest := ""
		if FileAccess.file_exists(resource_path):
			digest = FileAccess.get_sha256(resource_path)
		if digest.is_empty():
			missing.append(relative)
		else:
			file_hashes[relative] = digest
		entries.append("%s:%s" % [relative, digest])
	missing.sort()
	return {
		"algorithm": "sha256_opera_capture_source_closure_v2",
		"tree_rules": contract.get("tree_rules", []),
		"paths": source_paths,
		"files": file_hashes,
		"missing": missing,
		"sha256": "\n".join(entries).sha256_text(),
	}


func _career_slug(index: int) -> String:
	var config: Dictionary = OperaHouse.ACTS[index]
	return String(config.get("career", "career")).to_lower().replace(" ", "_")


func _career_id(index: int) -> String:
	return String((OperaHouse.ACTS[index] as Dictionary).get("costume", "career"))


func _start_menu_visible() -> bool:
	if main == null:
		return false
	var layer := main.get_node_or_null("StartMenu") as CanvasLayer
	return main.start_menu_active or (layer != null and layer.visible)


func _expected_state_ids() -> Array[String]:
	var result: Array[String] = []
	for room_id: String in NON_HALL_ROOMS:
		result.append("castle_career_routes_%s" % room_id)
	for floor_index: int in range(VENUE_FLOOR_ACTS.size()):
		result.append("opera_venue_floor_%02d_%s" % [
			floor_index + 1, _career_id(VENUE_FLOOR_ACTS[floor_index]),
		])
	for index: int in OperaHouse.LIVE_ACT_INDICES:
		result.append("opera_act_%02d_%s_from_%s" % [
			index + 1, _career_slug(index), CastleCareerRoutes.room_for_act(index),
		])
	return result


func _route_expected_state(room_id: String) -> Dictionary:
	return {
		"game": "level2",
		"phase": "hall",
		"room_id": room_id,
		"stage_id": "castle.room.%s" % room_id,
		"route_visible": true,
		"act_indices": CastleCareerRoutes.act_indices_for_room(room_id),
		"castle_layer": 14,
		"living_layer": 15,
		"pause_layer": 16,
		"opera_active": false,
		"venue_open": false,
		"start_menu_visible": false,
	}


func _route_actual_state(room_id: String) -> Dictionary:
	var actual_indices: Array[int] = []
	if routes != null:
		for button: Button in routes.buttons:
			actual_indices.append(int(button.get_meta("act_index", -1)))
	var venue_open := routes != null and routes.opera_venue != null \
		and is_instance_valid(routes.opera_venue) and routes.opera_venue.is_open()
	return {
		"game": main.game if main != null else "",
		"phase": String(main.g.get("phase", "")) if main != null else "",
		"room_id": main.castle_room_id if main != null else room_id,
		"stage_id": main.living_stage_id if main != null else "",
		"route_visible": routes != null and routes.root != null \
			and is_instance_valid(routes.root) and routes.root.visible,
		"act_indices": actual_indices,
		"castle_layer": main.castle_room_layer.layer \
			if main != null and main.castle_room_layer != null else -1,
		"living_layer": main.living_layer.layer \
			if main != null and main.living_layer != null else -1,
		"pause_layer": main.pause_layer.layer \
			if main != null and main.pause_layer != null else -1,
		"opera_active": main != null and main.opera_game != null,
		"venue_open": venue_open,
		"start_menu_visible": _start_menu_visible(),
	}


func _venue_expected_state(floor_index: int, act_index: int) -> Dictionary:
	return {
		"game": "level2",
		"phase": "hall",
		"room_id": "opera_hall",
		"stage_id": "castle.room.opera_hall",
		"venue_open": true,
		"accepting_input": true,
		"floor_index": floor_index,
		"floor_act_index": act_index,
		"guide_act_index": act_index,
		"enabled_act_indices": [act_index],
		"castle_layer": 14,
		"living_layer": 15,
		"pause_layer": 16,
		"opera_active": false,
		"start_menu_visible": false,
	}


func _venue_actual_state() -> Dictionary:
	var venue: OperaHouseVenue2D = routes.opera_venue if routes != null else null
	var enabled_indices: Array[int] = []
	var guide_act := -1
	if venue != null and is_instance_valid(venue):
		for button: Button in venue.buttons:
			if button.visible and not button.disabled:
				enabled_indices.append(int(button.get_meta("act_index", -1)))
		if venue.guide_button != null and is_instance_valid(venue.guide_button):
			guide_act = int(venue.guide_button.get_meta("act_index", -1))
	return {
		"game": main.game if main != null else "",
		"phase": String(main.g.get("phase", "")) if main != null else "",
		"room_id": main.castle_room_id if main != null else "",
		"stage_id": main.living_stage_id if main != null else "",
		"venue_open": venue != null and is_instance_valid(venue) and venue.is_open(),
		"accepting_input": venue != null and is_instance_valid(venue) \
			and venue.accepting_input,
		"floor_index": venue.floor_index \
			if venue != null and is_instance_valid(venue) else -1,
		"floor_act_index": VENUE_FLOOR_ACTS[venue.floor_index] \
			if venue != null and is_instance_valid(venue) \
				and venue.floor_index >= 0 and venue.floor_index < VENUE_FLOOR_ACTS.size() \
			else -1,
		"guide_act_index": guide_act,
		"enabled_act_indices": enabled_indices,
		"castle_layer": main.castle_room_layer.layer \
			if main != null and main.castle_room_layer != null else -1,
		"living_layer": main.living_layer.layer \
			if main != null and main.living_layer != null else -1,
		"pause_layer": main.pause_layer.layer \
			if main != null and main.pause_layer != null else -1,
		"opera_active": main != null and main.opera_game != null,
		"start_menu_visible": _start_menu_visible(),
	}


func _career_expected_state(index: int, room_id: String) -> Dictionary:
	return {
		"game": "opera",
		"act_index": index,
		"career_id": _career_id(index),
		"room_id": room_id,
		"return_room": room_id,
		"stage_id": "opera.act.%02d" % index,
		"act_state": "play",
		"career_world_present": true,
		"career_world_visible": true,
		"career_world_layer": 10,
		"living_layer": 11,
		"hud_layer": 12,
		"pause_layer": 13,
		"castle_layer_visible": false,
		"player_visible": false,
		"entry_method": ROUTE_ENTRY_METHOD,
		"start_menu_visible": false,
	}


func _career_actual_state(index: int, room_id: String,
		entry_method: String) -> Dictionary:
	var opera := main.opera_game as OperaHouse if main != null else null
	var current := opera.act as OperaAct if opera != null else null
	var world: OperaCareerWorld2D = current.career_world_2d \
		if current != null else null
	return {
		"game": main.game if main != null else "",
		"act_index": opera.act_index if opera != null else -1,
		"career_id": String(current.config.get("costume", "")) \
			if current != null else "",
		"room_id": main.castle_room_id if main != null else room_id,
		"return_room": main.opera_return_room if main != null else "",
		"stage_id": main.living_stage_id if main != null else "",
		"act_state": current.state if current != null else "",
		"career_world_present": world != null and is_instance_valid(world),
		"career_world_visible": world.visible \
			if world != null and is_instance_valid(world) else false,
		"career_world_layer": world.layer \
			if world != null and is_instance_valid(world) else -1,
		"living_layer": main.living_layer.layer \
			if main != null and main.living_layer != null else -1,
		"hud_layer": main.hud_layer.layer \
			if main != null and main.hud_layer != null else -1,
		"pause_layer": main.pause_layer.layer \
			if main != null and main.pause_layer != null else -1,
		"castle_layer_visible": main.castle_room_layer.visible \
			if main != null and main.castle_room_layer != null else false,
		"player_visible": main.player != null and main.player.visible \
			if main != null else false,
		"entry_method": entry_method,
		"start_menu_visible": _start_menu_visible(),
	}


func _states_match(expected: Dictionary, actual: Dictionary) -> bool:
	for key: Variant in expected:
		if not actual.has(key) or actual[key] != expected[key]:
			return false
	return true


func _state_differences(expected: Dictionary, actual: Dictionary) -> Array[String]:
	var differences: Array[String] = []
	for key: Variant in expected:
		if not actual.has(key) or actual[key] != expected[key]:
			differences.append("%s expected=%s actual=%s" % [
				str(key), str(expected[key]), str(actual.get(key)),
			])
	return differences


func _file_length(path: String) -> int:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return -1
	var length := file.get_length()
	file.close()
	return length


func _on_capture_frame_post_draw() -> void:
	capture_frame_drawn = true


func _wait_capture_frame_post_draw() -> bool:
	capture_frame_drawn = false
	var callback := Callable(self, "_on_capture_frame_post_draw")
	if RenderingServer.frame_post_draw.is_connected(callback):
		RenderingServer.frame_post_draw.disconnect(callback)
	RenderingServer.frame_post_draw.connect(callback, CONNECT_ONE_SHOT)
	for _frame: int in range(READY_FRAME_LIMIT):
		await process_frame
		if capture_frame_drawn:
			return true
	if RenderingServer.frame_post_draw.is_connected(callback):
		RenderingServer.frame_post_draw.disconnect(callback)
	return false


func _capture_state(state_id: String, kind: String, expected: Dictionary,
		actual_provider: Callable, semantic_ready: bool,
		input_evidence: Dictionary = {}) -> void:
	var sequence := states.size()
	var failures: Array[String] = []
	if not await _set_aspect(aspect_size):
		failures.append("viewport resize readiness timed out")
	# Keep desktop-only hover tooltips out of deterministic review frames.
	get_root().warp_mouse(Vector2(aspect_size.x * 0.5, aspect_size.y - 2.0))
	await _settle(2)
	var file_name := state_id + ".png"
	var file_path := aspect_dir.path_join(file_name)
	if FileAccess.file_exists(file_path):
		failures.append("capture path already exists")
	var previous_mode := main.process_mode if main != null else Node.PROCESS_MODE_INHERIT
	if main != null:
		main.process_mode = Node.PROCESS_MODE_DISABLED
	var actual: Dictionary = {}
	if actual_provider.is_valid():
		var actual_value: Variant = actual_provider.call()
		if actual_value is Dictionary:
			actual = actual_value as Dictionary
		else:
			failures.append("actual state provider did not return a dictionary")
	else:
		failures.append("actual state provider is invalid")
	failures.append_array(_state_differences(expected, actual))
	if not semantic_ready and failures.is_empty():
		failures.append("semantic readiness predicate timed out")
	if not await _wait_capture_frame_post_draw():
		failures.append("render frame readiness timed out")
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var save_error := ERR_CANT_CREATE
	var image_width := 0
	var image_height := 0
	if image != null:
		image_width = image.get_width()
		image_height = image.get_height()
		if image.get_size() != aspect_size:
			failures.append("viewport expected=%s actual=%s" % [
				str(aspect_size), str(image.get_size()),
			])
		if not FileAccess.file_exists(file_path):
			save_error = image.save_png(file_path)
	if main != null:
		main.process_mode = previous_mode
	if save_error != OK:
		failures.append("png save error=%d" % save_error)
	var passed := failures.is_empty()
	states.append({
		"id": state_id,
		"sequence": sequence,
		"kind": kind,
		"expected_state": expected,
		"actual_state": actual,
		"state_signature": JSON.stringify(actual, "", true).sha256_text(),
		"input": input_evidence,
		"status": "PASS" if passed else "FAIL",
		"failures": failures,
		"image": {
			"file": file_name,
			"width": image_width,
			"height": image_height,
			"bytes": _file_length(file_path) if save_error == OK else -1,
			"sha256": FileAccess.get_sha256(file_path) if save_error == OK else "",
		},
	})
	if passed:
		print("OPERASHOT|%s|%s|PASS" % [_aspect_id(aspect_size), state_id])
	else:
		print("OPERASHOT|%s|%s|FAIL|%s" % [
			_aspect_id(aspect_size), state_id, "; ".join(failures),
		])


func _room_ready(room_id: String) -> bool:
	return main != null and rooms != null and rooms.is_open() \
		and main.game == "level2" and String(main.g.get("phase", "")) == "hall" \
		and main.castle_room_id == room_id and main.opera_game == null \
		and main.castle_room_layer != null and main.castle_room_layer.visible \
		and main.castle_room_layer.layer == 14 \
		and main.living_layer != null and main.living_layer.visible \
		and main.living_layer.layer == 15 \
		and main.living_stage_id == "castle.room.%s" % room_id \
		and main.pause_layer != null and main.pause_layer.layer == 16


func _wait_room_ready(room_id: String) -> bool:
	for _frame: int in range(READY_FRAME_LIMIT):
		routes.sync()
		if _room_ready(room_id) and routes.root != null \
				and is_instance_valid(routes.root) and routes.root.visible:
			return true
		await process_frame
	return false


func _wait_venue_floor(floor_index: int) -> bool:
	var deadline_msec := Time.get_ticks_msec() + VENUE_READY_TIMEOUT_MSEC
	for _frame: int in range(VENUE_READY_FRAME_LIMIT):
		var venue: OperaHouseVenue2D = routes.opera_venue \
			if routes != null else null
		if _room_ready("opera_hall") and venue != null \
				and is_instance_valid(venue) and venue.is_open() \
				and venue.accepting_input and venue.floor_index == floor_index \
				and venue.guide_button != null \
				and int(venue.guide_button.get_meta("act_index", -1)) \
					== VENUE_FLOOR_ACTS[floor_index]:
			return true
		if Time.get_ticks_msec() >= deadline_msec:
			break
		await process_frame
	return false


func _fade_ready() -> bool:
	return main.fade_rect == null or (main.fade_rect.modulate.a <= 0.02 \
		and main.fade_rect.mouse_filter == Control.MOUSE_FILTER_IGNORE)


func _career_ready(index: int, room_id: String) -> bool:
	var opera := main.opera_game as OperaHouse if main != null else null
	var current := opera.act as OperaAct if opera != null else null
	return main != null and opera != null and current != null \
		and _fade_ready() and main.game == "opera" and opera.act_index == index \
		and main.opera_active_act_index == index \
		and main.opera_return_room == room_id and main.castle_room_id == room_id \
		and current.state == "play" and current.use_career_world_2d \
		and current.career_world_2d != null \
		and is_instance_valid(current.career_world_2d) \
		and current.career_world_2d.visible \
		and current.career_world_2d.layer == 10 \
		and main.living_stage_id == "opera.act.%02d" % index \
		and main.living_layer != null and main.living_layer.visible \
		and main.living_layer.layer == 11 \
		and main.hud_layer != null and main.hud_layer.visible \
		and main.hud_layer.layer == 12 \
		and main.pause_layer != null and main.pause_layer.layer == 13 \
		and main.castle_room_layer != null and not main.castle_room_layer.visible


func _wait_career_ready(index: int, room_id: String) -> bool:
	for _frame: int in range(READY_FRAME_LIMIT):
		if _career_ready(index, room_id):
			return true
		await process_frame
	return false


func _show_room(room_id: String) -> bool:
	if routes.opera_venue != null and is_instance_valid(routes.opera_venue):
		routes.close_opera_venue()
	rooms.show_room(room_id, false)
	return await _wait_room_ready(room_id)


func _capture_non_hall_routes() -> void:
	for room_id: String in NON_HALL_ROOMS:
		var ready := await _show_room(room_id)
		routes.sync()
		var expected := _route_expected_state(room_id)
		await _capture_state(
			"castle_career_routes_%s" % room_id,
			"castle_route", expected,
			Callable(self, "_route_actual_state").bind(room_id), ready,
		)


func _select_venue_floor_for_capture(target_floor: int) -> bool:
	var venue: OperaHouseVenue2D = routes.opera_venue
	if venue == null or not is_instance_valid(venue) \
			or target_floor < 0 or target_floor >= VENUE_FLOOR_ACTS.size():
		return false
	# The accepted foyer painting remains three-tiered, but every painted door
	# is now directly tappable. This visual probe positions Roshan for each art
	# capture without reviving the removed bubble-lift interaction.
	venue.floor_index = target_floor
	venue.refresh(main.opera_stars)
	await process_frame
	return venue.floor_index == target_floor and venue.accepting_input


func _capture_venue_floors() -> void:
	var room_ready := await _show_room("opera_hall")
	routes.sync()
	var opened := room_ready and routes.open_opera_venue()
	if opened:
		opened = await _wait_venue_floor(0)
	for floor_index: int in range(VENUE_FLOOR_ACTS.size()):
		var floor_ready := opened
		if floor_ready and routes.opera_venue.floor_index != floor_index:
			floor_ready = await _select_venue_floor_for_capture(floor_index)
		var act_index := VENUE_FLOOR_ACTS[floor_index]
		var expected := _venue_expected_state(floor_index, act_index)
		await _capture_state(
			"opera_venue_floor_%02d_%s" % [floor_index + 1, _career_id(act_index)],
			"opera_venue_floor", expected,
			Callable(self, "_venue_actual_state"), floor_ready,
		)
	if routes.opera_venue != null and is_instance_valid(routes.opera_venue):
		routes.close_opera_venue()


func _remove_current_act() -> bool:
	var opera := main.opera_game as OperaHouse if main != null else null
	if opera == null:
		return true
	var return_room := main.opera_return_room
	opera._leave_early()
	return await _wait_room_ready(return_room)


func _prepare_career_route(room_id: String, index: int) -> bool:
	if not await _remove_current_act():
		return false
	if not await _show_room(room_id):
		return false
	routes.sync()
	if room_id != "opera_hall":
		return true
	if not routes.open_opera_venue() or not await _wait_venue_floor(0):
		return false
	var target_floor := VENUE_FLOOR_ACTS.find(index)
	if target_floor < 0:
		return false
	if routes.opera_venue.floor_index != target_floor:
		if not await _navigate_venue_floor(target_floor):
			return false
	return await _wait_venue_floor(target_floor)


func _capture_career_entries() -> void:
	for index: int in OperaHouse.LIVE_ACT_INDICES:
		var room_id := CastleCareerRoutes.room_for_act(index)
		var route_ready := await _prepare_career_route(room_id, index)
		var button := routes.button_for_act(index) if routes != null else null
		var input_evidence: Dictionary = {}
		if route_ready and button != null and button.is_visible_in_tree() \
				and not button.disabled:
			# probe_opera.gd owns raw-touch verification. This visual harness calls
			# the same guarded callback that the shipping button signal reaches.
			routes._launch(room_id, index)
			input_evidence = {
				"method": ROUTE_ENTRY_METHOD,
				"room_id": room_id,
				"act_index": index,
				"control_path": String(button.get_path()),
			}
		var career_ready := route_ready and not input_evidence.is_empty() \
			and await _wait_career_ready(index, room_id)
		var expected := _career_expected_state(index, room_id)
		var entry_method := String(input_evidence.get("method", "not_sent"))
		var opera := main.opera_game as OperaHouse if main != null else null
		var current := opera.act as OperaAct if opera != null else null
		if current != null:
			current.set_process(false)
			if current.career_world_2d != null:
				current.career_world_2d.set_process(false)
		await _capture_state(
			"opera_act_%02d_%s_from_%s" % [index + 1, _career_slug(index), room_id],
			"career_entry", expected,
			Callable(self, "_career_actual_state").bind(
				index, room_id, entry_method,
			), career_ready, input_evidence,
		)


func _start_runtime() -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	if scene == null:
		_fail("main_scene", "could not load scenes/main.tscn")
		return false
	main = scene.instantiate() as ReefMain
	if main == null:
		_fail("main_instance", "main scene did not instantiate ReefMain")
		return false
	get_root().add_child(main)
	await _settle(2)
	main.day_one_active = false
	if main.start_menu_active:
		main._start_menu_ref()._dismiss_menu()
		await _settle(2)
	if main.intro_active:
		main._skip_intro()
	await _settle(2)
	main.opera_progress = 0
	main.opera_stars = 0
	main.opera_done = false
	main.game = "level2"
	main.g["t"] = 0.0
	main._enter_castle_interior_now(false)
	rooms = main._castle_rooms_ref()
	routes = main._castle_career_routes_ref()
	rooms.show_room("kitchen", false)
	var ready := await _wait_room_ready("kitchen")
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.player != null:
		main.player.visible = false
		main.player.set_process(false)
	return ready and rooms.is_open() and main.castle_room_stage != null


func _teardown_runtime() -> void:
	if main == null:
		return
	await _remove_current_act()
	if rooms != null and rooms.is_open():
		rooms.close()
	main.set_process(false)
	main.queue_free()
	await _settle(4)
	main = null
	rooms = null
	routes = null


func _summary() -> Dictionary:
	var passed := 0
	var written := 0
	for row: Dictionary in states:
		if String(row.get("status", "")) == "PASS":
			passed += 1
		var image: Dictionary = row.get("image", {}) as Dictionary
		if not String(image.get("sha256", "")).is_empty():
			written += 1
	return {
		"expected": 24,
		"rows": states.size(),
		"written": written,
		"passed": passed,
		"failed": states.size() - passed,
	}


func _state_ids_exact() -> bool:
	var actual: Array[String] = []
	for row: Dictionary in states:
		actual.append(String(row.get("id", "")))
	return actual == _expected_state_ids()


func _aspect_complete() -> bool:
	var summary := _summary()
	return states.size() == 24 and _state_ids_exact() \
		and int(summary["written"]) == 24 and int(summary["passed"]) == 24 \
		and int(summary["failed"]) == 0 and global_failures.is_empty() \
		and (capture_source_signature.get("missing", []) as Array).is_empty() \
		and _exact_engine() \
		and String(RenderingServer.get_current_rendering_method()) == "mobile"


func _write_manifest(result: String) -> bool:
	var manifest := {
		"schema": SCHEMA,
		"run_nonce": run_nonce,
		"source_revision": OS.get_environment("GITHUB_SHA") \
			if not OS.get_environment("GITHUB_SHA").is_empty() else "unknown",
		"aspect_id": _aspect_id(aspect_size),
		"viewport": {"width": aspect_size.x, "height": aspect_size.y},
		"capture_method": CAPTURE_METHOD,
		"rendering_method": String(RenderingServer.get_current_rendering_method()),
		"engine": _engine_contract(),
		"source_signature": capture_source_signature,
		"expected_state_ids": _expected_state_ids(),
		"states": states,
		"global_failures": global_failures,
		"summary": _summary(),
		"result": result,
	}
	var path := aspect_dir.path_join(MANIFEST_NAME)
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		print("OPERASHOT|%s|MANIFEST|FAIL|open_error=%d" % [
			_aspect_id(aspect_size), FileAccess.get_open_error(),
		])
		return false
	file.store_string(JSON.stringify(manifest, "\t", true) + "\n")
	file.close()
	print("OPERASHOT|%s|MANIFEST|%s" % [_aspect_id(aspect_size), path])
	return true


func _run_aspect(size: Vector2i) -> bool:
	aspect_size = size
	aspect_dir = out_dir.path_join(_aspect_id(size))
	states.clear()
	global_failures.clear()
	var directory_error := DirAccess.make_dir_recursive_absolute(aspect_dir)
	if directory_error != OK:
		_fail("aspect_directory", "%s error=%d" % [aspect_dir, directory_error])
		return false
	if not (capture_source_signature.get("missing", []) as Array).is_empty():
		_fail("source_closure", str(capture_source_signature.get("missing", [])))
	if not await _set_aspect(size):
		_fail("viewport_readiness", "expected=%s" % str(size))
	if not _exact_engine():
		_fail("engine_version", String(_engine_contract().get("version_string", "")))
	if String(RenderingServer.get_current_rendering_method()) != "mobile":
		_fail("rendering_method",
			String(RenderingServer.get_current_rendering_method()))
	if not await _start_runtime():
		_fail("runtime_readiness", "Castle route stage did not become ready")
	else:
		await _capture_non_hall_routes()
		await _capture_venue_floors()
		await _capture_career_entries()
	await _teardown_runtime()
	var complete := _aspect_complete()
	var manifest_written := _write_manifest("PASS" if complete else "FAIL")
	return complete and manifest_written


func _run() -> void:
	if DisplayServer.get_name() == "headless":
		print("OPERASHOT|RESULT|FAIL|windowed display required")
		quit(1)
		return
	var requested := OS.get_environment("OPERA_SHOT_OUT").strip_edges()
	out_dir = requested if not requested.is_empty() \
		else ProjectSettings.globalize_path("res://tmp/opera_capture")
	if not _prepare_fresh_output():
		quit(1)
		return
	run_nonce = "%d-%d-%d" % [
		int(Time.get_unix_time_from_system()), Time.get_ticks_usec(), randi(),
	]
	seed(20260829)
	capture_source_signature = _source_signature()
	var all_complete := true
	for size: Vector2i in ASPECTS:
		var aspect_complete := await _run_aspect(size)
		all_complete = all_complete and aspect_complete
	print("OPERASHOT|RESULT|%s|%s" % [
		"PASS" if all_complete else "FAIL", out_dir,
	])
	quit(0 if all_complete else 1)
