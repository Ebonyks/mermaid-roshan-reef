class_name LivingWorldDirector
extends RefCounted

# Logic-only coordinator. All mutable state lives on ReefMain; this class
# resolves the current authored area, resets true-idle time on every supported
# input path, and drives one reusable CanvasItem.

const CanvasLogic = preload("res://scripts/living_world_canvas.gd")
const CatalogLogic = preload("res://scripts/living_world_catalog.gd")
const HELD_KEYCODES := [
	KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
	KEY_W, KEY_A, KEY_S, KEY_D,
	KEY_SPACE, KEY_ENTER,
]

var m: ReefMain


func _init(main: ReefMain) -> void:
	m = main


func setup() -> void:
	if m.living_specs.is_empty():
		m.living_specs = CatalogLogic.build()
	if m.living_layer == null or not is_instance_valid(m.living_layer):
		m.living_layer = CanvasLayer.new()
		m.living_layer.name = "LivingWorldLayer"
		m.add_child(m.living_layer)
	if m.living_canvas == null or not is_instance_valid(m.living_canvas):
		m.living_canvas = CanvasLogic.new()
		m.living_canvas.name = "LivingWorldCanvas"
		m.living_canvas.mouse_filter = Control.MOUSE_FILTER_IGNORE
		m.living_canvas.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		m.living_layer.add_child(m.living_canvas)
	m.living_layer.visible = false


func note_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch or event is InputEventScreenDrag:
		note_activity()
	elif event is InputEventMouseButton:
		if (event as InputEventMouseButton).pressed:
			note_activity()
	elif event is InputEventMouseMotion:
		if (event as InputEventMouseMotion).button_mask != 0:
			note_activity()
	elif event is InputEventKey:
		if (event as InputEventKey).pressed:
			note_activity()
	elif event is InputEventJoypadButton:
		if (event as InputEventJoypadButton).pressed:
			note_activity()
	elif event is InputEventJoypadMotion:
		if absf((event as InputEventJoypadMotion).axis_value) > 0.18:
			note_activity()
	elif event is InputEventAction:
		if (event as InputEventAction).pressed:
			note_activity()


func note_activity() -> void:
	m.living_idle_time = 0.0
	if m.living_event_time >= 0.0:
		m.living_event_time = -1.0
		m.living_cooldown = maxf(m.living_cooldown, 6.0)
		if m.living_canvas != null and is_instance_valid(m.living_canvas):
			m.living_canvas.clear_event()


func tick(delta: float) -> void:
	setup()
	if _suspended():
		note_activity()
		m.living_layer.visible = false
		return
	var next_stage: String = resolve_stage_id()
	if next_stage == "" or not m.living_specs.has(next_stage):
		deactivate()
		return
	if next_stage != m.living_stage_id:
		_switch_stage(next_stage)
	if _held_input_active():
		note_activity()
	else:
		m.living_idle_time += delta
	m.living_time = fmod(m.living_time + delta, 3600.0)
	m.living_cooldown = maxf(0.0, m.living_cooldown - delta)
	var spec: Dictionary = m.living_specs[m.living_stage_id]
	var idle: Dictionary = spec["idle_event"]
	var event_progress := -1.0
	if m.living_event_time >= 0.0:
		m.living_event_time += delta
		var duration: float = float(idle["duration"])
		if m.living_event_time >= duration:
			m.living_event_time = -1.0
			m.living_idle_time = 0.0
		else:
			event_progress = m.living_event_time / duration
	elif m.living_idle_time >= float(idle["delay"]) and m.living_cooldown <= 0.0:
		m.living_event_time = 0.0
		m.living_cooldown = float(idle["cooldown"])
		m.living_event_count += 1
		event_progress = 0.0
	m.living_layer.visible = true
	m.living_canvas.set_motion(m.living_time, event_progress)


func deactivate() -> void:
	if m.living_stage_id == "" and (m.living_layer == null or not m.living_layer.visible):
		return
	m.living_stage_id = ""
	m.living_time = 0.0
	m.living_idle_time = 0.0
	m.living_cooldown = 0.0
	m.living_event_time = -1.0
	m.living_probe_stage_override = ""
	if m.living_canvas != null and is_instance_valid(m.living_canvas):
		m.living_canvas.configure({})
	if m.living_layer != null and is_instance_valid(m.living_layer):
		m.living_layer.visible = false


func resolve_stage_id() -> String:
	if DisplayServer.get_name() == "headless" and m.living_probe_stage_override != "":
		return m.living_probe_stage_override
	if m.intro_active:
		return "intro.storybook"
	if m.dance_engine != null and is_instance_valid(m.dance_engine) \
			and bool(m.dance_engine.get("active")):
		return "dance.rhythm_stage"
	if m.companion_care_layer != null and is_instance_valid(m.companion_care_layer):
		return "overlay.companion_care"
	if m.companion_layer != null and is_instance_valid(m.companion_layer):
		return "overlay.companion_picker"
	if m.collection_layer != null and is_instance_valid(m.collection_layer):
		return "overlay.critter_book"
	if m.stickers_layer != null and is_instance_valid(m.stickers_layer):
		return "overlay.sticker_book"
	if m.wardrobe_layer != null and is_instance_valid(m.wardrobe_layer):
		return "overlay.wardrobe"
	if m.craft_layer != null and is_instance_valid(m.craft_layer):
		return "overlay.craft_studio"
	if m.mg_kind != "":
		return _picture_stage_id(m.mg_kind)
	match m.game:
		"":
			return _reef_stage_id()
		"level2":
			return _level2_stage_id()
		"north":
			return _north_stage_id()
		"fetch":
			return "minigame.fetch"
		"dolls":
			return "minigame.dolls"
		"brawl":
			return "minigame.brawl"
		"seek":
			return "minigame.seek"
		"race":
			return "minigame.race_sunset"
		"shop":
			return "minigame.shop"
		"treasure":
			return "minigame.treasure"
		"melody":
			return "minigame.melody"
		"slide":
			return _slide_stage_id()
		"fairyshoot":
			return _fairy_stage_id()
		"kart":
			return "kart.rainbow_road" if m.kart_ground == "float" else "kart.ocean_circuit"
		"galaxy":
			return _galaxy_stage_id()
		"ember":
			return "ember.fortress_planet"
		"combat":
			return _combat_stage_id()
		"stuffie":
			return "stuffie.sparring_den"
		"dungeon":
			return _dungeon_stage_id("dungeon.ice", 10)
		"emberdun":
			return _dungeon_stage_id("dungeon.ember", 6)
		"opera":
			return _opera_stage_id()
	return ""


func set_probe_stage(stage_id: String) -> void:
	if DisplayServer.get_name() != "headless":
		return
	if not m.living_specs.has(stage_id):
		return
	m.living_probe_stage_override = stage_id
	_switch_stage(stage_id)


func clear_probe_stage() -> void:
	m.living_probe_stage_override = ""
	deactivate()


func force_idle_event_for_probe() -> void:
	if DisplayServer.get_name() != "headless" or m.living_stage_id == "":
		return
	var spec: Dictionary = m.living_specs[m.living_stage_id]
	var idle: Dictionary = spec["idle_event"]
	m.living_idle_time = float(idle["delay"])
	m.living_cooldown = 0.0


func runtime_counts() -> Dictionary:
	var layers := 0
	var canvases := 0
	for child in m.get_children():
		if child.name == &"LivingWorldLayer":
			layers += 1
			for grandchild in child.get_children():
				if grandchild.name == &"LivingWorldCanvas":
					canvases += 1
	return {
		"layers": layers,
		"canvases": canvases,
		"timers": 0,
		"tweens": 0,
		"particles": 0,
	}


func _switch_stage(stage_id: String) -> void:
	setup()
	var spec: Dictionary = m.living_specs[stage_id]
	m.living_stage_id = stage_id
	m.living_time = 0.0
	m.living_idle_time = 0.0
	m.living_cooldown = 0.0
	m.living_event_time = -1.0
	m.living_generation += 1
	m.living_layer.layer = int(spec["canvas_layer"])
	m.living_layer.visible = true
	m.living_canvas.configure(spec)


func _held_input_active() -> bool:
	if m.touch_auto_active:
		return true
	if m.touch_ui != null and is_instance_valid(m.touch_ui):
		if m.touch_ui.stick_vec.length_squared() > 0.01:
			return true
		if m.touch_ui.action_down or m.touch_ui.drag_active:
			return true
	for keycode in HELD_KEYCODES:
		if Input.is_physical_key_pressed(keycode):
			return true
	for axis in [JOY_AXIS_LEFT_X, JOY_AXIS_LEFT_Y, JOY_AXIS_RIGHT_X, JOY_AXIS_RIGHT_Y]:
		if absf(m.joy_axis(axis)) > 0.18:
			return true
	if m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B):
		return true
	return false


func _suspended() -> bool:
	if m.get_tree() == null or m.get_tree().paused:
		return true
	if m.fade_rect != null and m.fade_rect.modulate.a > 0.02:
		return true
	if m.sleep_t >= 0.0 or m.hug_layer != null or m.finale_t >= 0.0 or m.pose_t >= 0.0:
		return true
	return false


func _reef_stage_id() -> String:
	if m.player == null:
		return ""
	var region: String = ReefDistricts.region_at(Vector2(m.player.position.x, m.player.position.z))
	var ids := {
		"pearl": "reef.pearl_plaza",
		"kelp": "reef.kelp_gardens",
		"wreck": "reef.wreck_canyon",
		"moon": "reef.moon_pool",
		"rainbow": "reef.rainbow_bazaar",
		"ice": "reef.ice_shelf",
	}
	return String(ids.get(region, "reef.pearl_plaza"))


func _level2_stage_id() -> String:
	var phase: String = String(m.g.get("phase", "court"))
	if phase == "promenade":
		if m.player == null:
			return "sky.promenade_runway"
		var local_x: float = m.player.position.x - m.LEVEL2_POS.x
		if local_x < -25.0:
			return "sky.promenade_runway"
		if local_x < 25.0:
			return "sky.promenade_playground"
		return "sky.promenade_castle"
	if phase == "hall":
		return _castle_stage_id()
	return _legacy_sky_stage_id()


func _legacy_sky_stage_id() -> String:
	if m.player == null:
		return "sky.courtyard"
	var p: Vector3 = m.player.position
	var local: Vector3 = p - m.LEVEL2_POS
	if local.z > 145.0:
		return "sky.gatehouse"
	if _near_dictionary_point("alpine_mountain_center", p, 46.0):
		return "sky.alpine_mountain"
	if _near_dictionary_point("alpine_village_center", p, 52.0):
		return "sky.alpine_village"
	if local.z < -125.0:
		return "sky.alpine_village"
	if Vector2(local.x + 95.0, local.z - 70.0).length() < 42.0:
		return "sky.fairy_pond"
	if local.x > 42.0 and local.z > 42.0:
		return "sky.playground"
	if _near_any_gateway(p, 48.0):
		return "sky.rainbow_junction"
	if _near_dictionary_point("entry", p, 64.0) or _near_dictionary_point("back_entry", p, 36.0):
		return "sky.castle_exterior"
	return "sky.courtyard"


func _near_any_gateway(point: Vector3, radius: float) -> bool:
	for gateway in [m.bw_portal_pos, m.ember_portal_pos, m.kart_legA, m.kart_legB]:
		var pos: Vector3 = gateway
		if pos != Vector3.ZERO and pos.distance_to(point) < radius:
			return true
	return false


func _near_dictionary_point(key: String, point: Vector3, radius: float) -> bool:
	if not m.g.has(key):
		return false
	var value: Variant = m.g[key]
	return value is Vector3 and (value as Vector3).distance_to(point) < radius


func _north_stage_id() -> String:
	if m.player == null:
		return "north.mountain_pass"
	var local: Vector3 = m.player.position - m.NORTHERN_POS
	var xz := Vector2(local.x, local.z)
	if xz.distance_to(Vector2(18.0, 138.0)) < 25.0:
		return "north.spirit_clearing_a"
	if xz.distance_to(Vector2(-20.0, -58.0)) < 25.0:
		return "north.spirit_clearing_b"
	if local.z < -292.0 and absf(local.x) < 48.0:
		return "north.grand_hall"
	if local.z < -275.0:
		return "north.ice_castle_exterior"
	if local.z < -110.0:
		return "north.riverside_town"
	if local.z < 275.0:
		return "north.magic_forest"
	return "north.mountain_pass"


func _castle_stage_id() -> String:
	if m.player == null:
		return "castle.grand_hall"
	var local: Vector3 = m.player.position - m.CASTLE_POS
	if local.y >= 48.0:
		if local.z > -51.0:
			return "castle.dreaming_corridor"
		if local.x < -27.0:
			return "castle.dream_huluu"
		if local.x < -9.0:
			return "castle.dream_daddy"
		if local.x < 9.0:
			return "castle.dream_mama_baby"
		if local.x < 27.0:
			return "castle.dream_kareem"
		return "castle.dream_evie"
	if local.y >= 30.0:
		if local.z < -36.0:
			return "castle.upper_star_chamber" if local.x < 0.0 else "castle.upper_cloud_lounge"
		if local.x < -35.0:
			return "castle.upper_library"
		if local.x > 35.0:
			return "castle.upper_toy_gallery"
		return "castle.upper_gallery"
	if local.y < -8.0:
		if local.x < -25.0 and local.z < -20.0:
			return "castle.royal_loo"
		if local.x < -8.0 and local.z > -15.0:
			return "castle.pantry"
		if local.x > 8.0 and local.z > -15.0:
			return "castle.kitchen"
		if local.x < -8.0 and local.z <= -15.0:
			return "castle.bubble_bath"
		if local.x > 8.0 and local.z <= -15.0:
			return "castle.craft_room"
		return "castle.basement_corridor"
	if local.z > 8.0:
		return "castle.undercroft"
	if local.x < -34.0 and local.z > -27.0 and local.z < 17.0:
		return "castle.music_room"
	if local.x > 34.0 and local.z > -30.0 and local.z < -4.0:
		return "castle.royal_bedroom"
	return "castle.grand_hall"


func _picture_stage_id(kind: String) -> String:
	var ids := {
		"snowman": "picture.snowman",
		"garden": "picture.garden",
		"trampoline": "picture.trampoline",
		"xmas": "picture.xmas",
	}
	return String(ids.get(kind, ""))


func _slide_stage_id() -> String:
	var friend: Dictionary = m.g.get("fr", {})
	return "minigame.slide_rainbow" if String(friend.get("theme", "ice")) == "rainbow" \
		else "minigame.slide_ice"


func _fairy_stage_id() -> String:
	var phase: String = String(m.g.get("phase", "fly"))
	return "minigame.fairy_flight" if phase == "fly" else "minigame.fairy_boss"


func _galaxy_stage_id() -> String:
	if m.galaxy_game != null and is_instance_valid(m.galaxy_game) \
			and String(m.galaxy_game.get("_mode")) == "hall":
		return "galaxy.star_hall"
	return "galaxy.butterfly_garden"


func _combat_stage_id() -> String:
	if m.combat_game != null and is_instance_valid(m.combat_game) \
			and String(m.combat_game.kind) == "fire":
		return "combat.pepper"
	return "combat.ice_berry"


func _dungeon_stage_id(prefix: String, room_count: int) -> String:
	var room_index := 0
	if m.dungeon_game != null and is_instance_valid(m.dungeon_game):
		room_index = clampi(m.dungeon_game.room_index, 0, room_count - 1)
	return "%s.%02d" % [prefix, room_index]


func _opera_stage_id() -> String:
	if m.opera_game == null or not is_instance_valid(m.opera_game):
		return "opera.lobby_floor_1"
	if m.opera_game.act != null and m.opera_game.act_index >= 0:
		return "opera.act.%02d" % clampi(m.opera_game.act_index, 0, 14)
	var floor_index: int = clampi(roundi(m.opera_game.lobby_y / 13.0), 0, 2)
	return "opera.lobby_floor_%d" % (floor_index + 1)
