extends "res://export/flat_vector_r69/capture_entry.gd"
var route_observations: Array[Dictionary] = []
var profile_reloaded: bool = false
var texture_paths: Dictionary = {}

func _boot() -> bool:
	var before: int = bindings.size()
	var main: ReefMain = source_main.instantiate() as ReefMain
	root.add_child(main)
	current_scene = main
	if not await _wait(func() -> bool: return is_instance_valid(m) and m.is_node_ready() and m.start_menu_layer != null and m.get_node_or_null("BootSplashHandoff") == null, 30.0):
		errors.append("original display menu did not settle")
		return false
	_check("original configured Main/private dependency beforeReady", m.scene_file_path == "res://scenes/main.tscn" and m._save_state.save_path == profile and bindings.size() == before + 1 and bool(bindings[-1]["before_ready"]))
	return true

func _safe(value: Variant) -> Variant:
	if value is Vector2:
		var v: Vector2 = value
		return [v.x, v.y]
	if value is Vector3:
		var v: Vector3 = value
		return [v.x, v.y, v.z]
	if value is Color:
		var v: Color = value
		return [v.r, v.g, v.b, v.a]
	if value is Dictionary:
		var result: Dictionary = {}
		for key: Variant in value:
			result[str(key)] = _safe(value[key])
		return result
	if value is Array:
		var result: Array = []
		for item: Variant in value:
			result.append(_safe(item))
		return result
	if value is Object:
		var object: Object = value as Object
		return {"class": object.get_class(), "id": object.get_instance_id()} if is_instance_valid(object) else null
	return value

func _control_state(name: String) -> Dictionary:
	var c: Control = _button(name)
	if c == null:
		return {"exists": false}
	var data: Dictionary = {"exists": true, "id": c.get_instance_id(), "path": str(c.get_path()), "class": c.get_class(), "visible": c.is_visible_in_tree(), "global_rect": str(c.get_global_rect()), "global_transform": str(c.get_global_transform_with_canvas()), "self_modulate": str(c.self_modulate), "mouse_filter": c.mouse_filter}
	if c is Button:
		var b: Button = c as Button
		data.merge({"text": b.text, "tooltip": b.tooltip_text, "disabled": b.disabled, "flat": b.flat, "focus_mode": b.focus_mode, "pressed_connections": b.pressed.get_connections().size()})
	return data

func _galaxy_nodes(node: Node, rows: Array[Dictionary], counts: Dictionary) -> void:
	if node is Node3D:
		var spatial: Node3D = node as Node3D
		var type_name: String = node.get_class()
		counts[type_name] = int(counts.get(type_name, 0)) + 1
		var row: Dictionary = {"id": node.get_instance_id(), "path": str(node.get_path()), "class": type_name, "visible_in_tree": spatial.is_visible_in_tree(), "position": str(spatial.position), "global_position": str(spatial.global_position), "scale": str(spatial.scale)}
		if node.get_script() != null:
			row["script"] = (node.get_script() as Script).resource_path
		if node is Sprite3D:
			var sprite: Sprite3D = node as Sprite3D
			row["texture"] = _tex(sprite.texture)
			if sprite.texture != null and not sprite.texture.resource_path.is_empty():
				texture_paths[sprite.texture.resource_path] = true
		if node is MeshInstance3D:
			var mesh_node: MeshInstance3D = node as MeshInstance3D
			row["mesh_class"] = mesh_node.mesh.get_class() if mesh_node.mesh != null else ""
			row["mesh_path"] = mesh_node.mesh.resource_path if mesh_node.mesh != null else ""
			var material: Material = mesh_node.material_override
			row["material_override"] = {"class": material.get_class(), "path": material.resource_path} if material != null else {}
		if node is Camera3D:
			row["camera_current"] = (node as Camera3D).current
			row["fov"] = (node as Camera3D).fov
		if rows.size() < 192:
			rows.append(row)
	for child: Node in node.get_children():
		_galaxy_nodes(child, rows, counts)

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	if not is_instance_valid(m):
		return result
	var controller: RefCounted = m._fairy_conservatory_door
	var handoff: RefCounted = m.fairy_conservatory_handoff
	var room: CastleRooms25D = m._castle_rooms_25d
	result["profile_mode"] = mode
	result["profile_reloaded"] = profile_reloaded
	result["fairy_flags"] = {"opera_done": m.opera_done, "revealed": m.chapter3_fairy_door_revealed, "opened": m.chapter3_fairy_door_opened, "mission_started": m.chapter3_fairy_mission_started}
	result["moonflower"] = {"controller_exists": controller != null, "visual_state": str(controller.call("visual_state")) if controller != null else "", "render_state": str(controller.get("_render_state")) if controller != null else "", "hotspot": _control_state("MoonflowerConservatoryHotspot"), "pointer_exists": m.find_child("MoonflowerConservatoryPointer", true, false) != null}
	result["hall"] = {"room": m.castle_room_id, "layer_id": m.castle_room_layer.get_instance_id() if is_instance_valid(m.castle_room_layer) else 0, "layer_visible": m.castle_room_layer.visible if is_instance_valid(m.castle_room_layer) else false, "controller_id": room.get_instance_id() if room != null else 0, "view_left_art": room.get("_hall_view_left_art") if room != null else null, "movement_active": room.get("_movement_tween") != null and (room.get("_movement_tween") as Tween).is_running() if room != null else false}
	result["handoff"] = _safe(handoff.call("audit_snapshot")) if handoff != null else {}
	result["fairy_return_context"] = _safe(m.fairy_conservatory_return_context)
	result["house_control"] = _control_state("ButterflyHouseHotspot")
	var navigation: Array[Dictionary] = []
	for route: Dictionary in m.navigation_routes:
		navigation.append({"id": str(route.get("id", ""))})
	result["navigation"] = navigation
	var galaxy: Node3D = m.galaxy_game
	if galaxy != null and is_instance_valid(galaxy):
		var rows: Array[Dictionary] = []
		var counts: Dictionary = {}
		_galaxy_nodes(galaxy, rows, counts)
		result["galaxy"] = {"active": true, "id": galaxy.get_instance_id(), "script": (galaxy.get_script() as Script).resource_path, "mode": str(galaxy.get("_mode")), "rows": rows, "node_class_counts": counts, "row_limit": 192, "rows_are_not_full_projection_or_pixel_attribution": true}
	else:
		result["galaxy"] = {"active": false}
	return result

func _capture(id: String, role := "R69_CURRENT_ORIGINAL_FAIRY_ROUTE_CONTEXT_NOT_QA11") -> void:
	await super(id, role)

func _raw_tap(point: Vector2) -> void:
	_screen_touch(point, true)
	await _frames(1)
	_screen_touch(point, false)
	await _frames(4)

func _castle_entry(prefix: String) -> bool:
	var continue_button: Button = _button("StartMenuContinueButton") as Button
	_check("original Continue is available " + prefix, continue_button != null and not continue_button.disabled)
	await _tap(continue_button, continue_button.size * 0.5)
	if not await _wait(func() -> bool: return not m.start_menu_active and m._day_one_story_clip == null and str(m.g.get("phase", "")) == "promenade", 70.0):
		errors.append("original Continue did not reach source promenade")
		return false
	await _frames(30)
	await _capture(prefix + "_promenade")
	var anchor: Node2D = m.g.get("lagoon_castle_door_focus") as Node2D
	if anchor == null:
		errors.append("source gate anchor missing")
		return false
	var helper: SkyLagoonPromenade = m._sky_lagoon_promenade
	if str(m.g.get("lagoon_promenade_focus", "")) != "castle_gate":
		await _raw_tap(helper.screen_from_master(anchor.position))
	_check("original gate target focuses " + prefix, str(m.g.get("lagoon_promenade_focus", "")) == "castle_gate")
	await _raw_tap(helper.screen_from_master(anchor.position))
	if not await _wait(func() -> bool: return str(m.g.get("phase", "")) == "hall" and m.castle_room_id == "main_hall" and m._day_one_story_clip == null, 70.0):
		errors.append("original gate did not reach main hall")
		return false
	await _frames(35)
	await _capture(prefix + "_hall_initial")
	return true

func _frame_moonflower(prefix: String) -> bool:
	# Original floor input moves the cutout and source-owned hall view.
	if m.castle_room_stage == null:
		errors.append("source hall stage missing")
		return false
	await _tap(m.castle_room_stage, Vector2(1180, 662))
	if not await _wait(func() -> bool: return m._castle_rooms_25d == null or m._castle_rooms_25d.get("_movement_tween") == null or not (m._castle_rooms_25d.get("_movement_tween") as Tween).is_running(), 20.0):
		errors.append("source hall floor walk did not settle")
		return false
	await _frames(30)
	await _capture(prefix + "_door_framed")
	_check("original floor input keeps main hall " + prefix, m.castle_room_id == "main_hall" and str(m.g.get("phase", "")) == "hall")
	return true

func _enter_handoff(prefix: String) -> bool:
	var door: Button = _button("MoonflowerConservatoryHotspot") as Button
	if door == null or not door.is_visible_in_tree():
		errors.append("source revealed/open Moonflower control missing")
		return false
	var rect: Rect2 = door.get_global_rect()
	var clipped: Rect2 = rect.intersection(Rect2(Vector2.ZERO, Vector2(root.size)))
	_check("Moonflower has a visible native touch area " + prefix, clipped.size.x >= 80.0 and clipped.size.y >= 80.0)
	var point: Vector2 = clipped.get_center()
	await _raw_tap(point)
	if not await _wait(func() -> bool: return m.game == "fairy_conservatory" and m.fairy_conservatory_handoff != null, 20.0):
		errors.append("original Moonflower input did not enter Skyway")
		return false
	await _frames(30)
	await _capture(prefix + "_skyway_entry")
	_check("original door persists open " + prefix, m.chapter3_fairy_door_revealed and m.chapter3_fairy_door_opened)
	return true

func _waypoint_tap(returning: bool) -> bool:
	var handoff: RefCounted = m.fairy_conservatory_handoff
	if handoff == null or not is_instance_valid(handoff):
		errors.append("source handoff no longer active before waypoint input")
		return false
	var world: Node2D = handoff.get("_world") as Node2D
	if world == null or not is_instance_valid(world):
		errors.append("source handoff world absent before waypoint input")
		return false
	var target: Vector2 = handoff.call("_return_waypoint" if returning else "_next_waypoint")
	var point: Vector2 = world.get_global_transform_with_canvas() * target
	await _raw_tap(point)
	return true

func _journey(prefix: String) -> bool:
	var handoff: RefCounted = m.fairy_conservatory_handoff
	var snap: Dictionary = handoff.call("audit_snapshot")
	var initial_index: int = int(snap["waypoint_index"])
	await _frames(30)
	await _capture(prefix + "_skyway_passive")
	_check("one-second passive Skyway does not advance " + prefix, int((handoff.call("audit_snapshot") as Dictionary)["waypoint_index"]) == initial_index)
	var world: Node2D = handoff.get("_world") as Node2D
	var wrong_point: Vector2 = world.get_global_transform_with_canvas() * Vector2(1160, 100)
	_check("off-route point avoids original navigation " + prefix, not _button("GlobalNavigationButton").get_global_rect().has_point(wrong_point))
	await _raw_tap(wrong_point)
	await _capture(prefix + "_skyway_wrong_tap")
	var remained: bool = m.game == "fairy_conservatory" and m.fairy_conservatory_handoff == handoff and not bool((handoff.call("audit_snapshot") as Dictionary)["finished"])
	_check("off-route touch retains the same source handoff " + prefix, remained)
	if not remained:
		return false
	_check("off-route touch does not advance " + prefix, int((handoff.call("audit_snapshot") as Dictionary)["waypoint_index"]) == initial_index)
	var count: int = int(snap["waypoint_count"])
	for i: int in range(count):
		if not await _waypoint_tap(false):
			return false
		await _capture(prefix + "_outbound_%02d" % (i + 1))
		_check("source waypoint input advances " + prefix + str(i), int((handoff.call("audit_snapshot") as Dictionary)["waypoint_index"]) == i + 1)
	snap = handoff.call("audit_snapshot") as Dictionary
	_check("source house becomes available only at endpoint " + prefix, str(snap["state"]) == "butterfly_house" and bool(snap["house_hotspot_visible"]))
	var house: Button = _button("ButterflyHouseHotspot") as Button
	if house == null or m.fairy_conservatory_handoff != handoff:
		errors.append("source house control absent at endpoint")
		return false
	await _tap(house, house.size * 0.5)
	if not await _wait(func() -> bool: return m.game == "galaxy" and m.galaxy_game != null, 25.0):
		errors.append("original Butterfly House input did not enter source garden")
		return false
	await _frames(60)
	await _capture(prefix + "_butterfly_world_entry")
	_check("original garden script and mode bound " + prefix, (m.galaxy_game.get_script() as Script).resource_path == "res://scripts/galaxy.gd" and str(m.galaxy_game.get("_mode")) == "planet")
	await _frames(60)
	await _capture(prefix + "_butterfly_world_passive")
	_check("two-second passive garden remains in source world " + prefix, m.game == "galaxy" and m.galaxy_game != null)
	await _tap(_button("GlobalNavigationButton"), _button("GlobalNavigationButton").size * 0.5)
	if not await _wait(func() -> bool: return m.game == "fairy_conservatory" and m.fairy_conservatory_handoff != null, 25.0):
		errors.append("original garden Back did not return through Skyway")
		return false
	await _frames(30)
	await _capture(prefix + "_skyway_return_entry")
	handoff = m.fairy_conservatory_handoff
	snap = handoff.call("audit_snapshot") as Dictionary
	_check("source return begins at far end " + prefix, str(snap["state"]) == "rainbow_return" and int(snap["waypoint_index"]) == count)
	for i: int in range(count):
		if not await _waypoint_tap(true):
			return false
		await _frames(6)
		await _capture(prefix + "_return_%02d" % (i + 1))
		if i < count - 1:
			_check("source return waypoint input advances " + prefix + str(i), int((m.fairy_conservatory_handoff.call("audit_snapshot") as Dictionary)["waypoint_index"]) == count - i - 1)
	if not await _wait(func() -> bool: return m.game == "level2" and m.castle_room_id == "main_hall" and m.fairy_conservatory_handoff == null, 25.0):
		errors.append("source Skyway did not restore hall")
		return false
	await _frames(30)
	await _capture(prefix + "_hall_returned")
	return true

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("01_original_menu")
	if not await _castle_entry("02") or not await _frame_moonflower("03"):
		return
	var door_state: Dictionary = (_snapshot()["moonflower"] as Dictionary)
	if mode == "dormant":
		_check("dormant relief has no active hotspot", str(door_state["visual_state"]) == "closed" and not bool((door_state["hotspot"] as Dictionary).get("exists", false)) and not bool(door_state["pointer_exists"]))
		var card: Sprite2D = m.find_child("MoonflowerConservatoryDoor", true, false) as Sprite2D
		if card != null:
			await _raw_tap(card.get_global_transform_with_canvas() * Vector2.ZERO)
		await _frames(30)
		await _capture("04_dormant_scenery_touch")
		_check("dormant scenery does not open Chapter3", m.game == "level2" and m.castle_room_id == "main_hall" and m.fairy_conservatory_handoff == null and not m.chapter3_fairy_door_opened)
		return
	_check("source expected door state", str(door_state["visual_state"]) == ("revealed" if mode == "revealed" else "open"))
	var hall_id: int = m.castle_room_layer.get_instance_id()
	var view_left: float = float(m._castle_rooms_25d.get("_hall_view_left_art"))
	if not await _enter_handoff("04") or not await _journey("05"):
		return
	_check("source return resumes same hall composition", m.castle_room_layer.get_instance_id() == hall_id and is_equal_approx(float(m._castle_rooms_25d.get("_hall_view_left_art")), view_left))
	_check("source room remains open and doorway remains open", m.castle_room_layer.visible and m.chapter3_fairy_door_opened)
	if mode == "revealed":
		await _retire()
		profile_reloaded = true
		if not await _boot() or not await _castle_entry("06_reload") or not await _frame_moonflower("07_reload"):
			return
		await _capture("08_saved_open_door")
		_check("source action persists open door across fresh Main load", m.chapter3_fairy_door_opened and str((_snapshot()["moonflower"] as Dictionary)["visual_state"]) == "open" and bindings.size() == 2)

func _run() -> void:
	mode = OS.get_environment("R69_MODE")
	out_dir = OS.get_environment("R69_OUT")
	normal_base = OS.get_environment("R69_NORMAL_BASE")
	var width: int = int(OS.get_environment("R69_WIDTH"))
	if mode not in ["dormant", "revealed", "opened"] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	var engine: Dictionary = Engine.get_version_info()
	if str(engine.get("hash", "")) != "ed1daf0bf001b61586d9930840f2f1394092c079" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() != "Windows" or Engine.time_scale != 1.0:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "day_one_active": false, "opera_done": mode == "revealed", "chapter3_fairy_door_revealed": mode == "opened", "chapter3_fairy_door_opened": mode == "opened", "chapter3_fairy_mission_started": false, "custom_fish": [], "custom_friends": [], "companion": "", "flat_vector_private_unknown": {"token": "R69_PRIVATE_ONLY", "keep": [3, 7]}}
	var file: FileAccess = FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	node_added.connect(_bind_private_before_ready)
	source_main = load("res://scenes/main.tscn") as PackedScene
	if await _aspect(Vector2i(width, 720)):
		await _exercise()
	var final_snapshot: Dictionary = _snapshot()
	await _retire()
	_check("retirement disposes owned Main", m == null)
	if _normal_hashes() != normal_before:
		errors.append("normal save/archive hashes changed")
	var report: Dictionary = {"schema": "reef.fairy_route_context/1", "mode": mode, "source_revision": OS.get_environment("R69_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "aspect": [width, 720], "states": states, "events": events, "checks": checks, "errors": errors, "bindings": bindings, "seed": seed, "normal_before": normal_before, "normal_after": _normal_hashes(), "texture_paths_3d_observed": texture_paths.keys(), "final_snapshot": final_snapshot, "actual_child_data": false, "production_changes": [], "scope": "Current original configured Main and private SaveState dependency beforeReady. Original source inputs, door unlock, Skyway and ordinary Butterfly House route. Existing Galaxy3D is transition debt observed through ordinary caller, not reintroduced source or accepted medium. No probe_tap/direct route/state/clock/camera/quality/geometry writes or art generation. Scene/pixel/hierarchy observations are bounded, not independent projection/compositor/QA11/device/audio/child/owner/creative acceptance; rescue/fountain/mission/all callers and whole-game inventory remain open."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("FAIRY69|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
