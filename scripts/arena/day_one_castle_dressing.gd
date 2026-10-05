class_name DayOneCastleDressing
extends Node2D
## Day One's temporary castle dressing layer.
##
## The layer owns the approved Sprite2D dust-bunny cutouts and one child
## DayOneCastleGrime node that draws the code-shaped disrepair marks: grime at
## the exterior edge, a soft interior disrepair tint and room cracks. It sits
## above the castle cards and can be mounted or removed without changing those
## cards. A room listed in AUTHORED_DIRT_ROOMS shows its dirt through authored
## art and a declared room tint instead, so the grime child is hidden there
## (MA-VIS-009). CastleRooms25D owns the unified four-state door cues so this
## dressing never creates a second glow.

const ROOM_IDS: Array[String] = [
	"bubble_bath", "mermaid_pool", "playroom", "craft_room",
]
const DEFAULT_ROOM_CENTERS: Dictionary = {
	# Coordinates are room-local defaults. Integrators should provide the
	# current room's center when mounting a room camera; these are never a
	# four-room overview layout.
	"bubble_bath": Vector2(640.0, 390.0),
	# The pool bunny owns the lower-left shore and never crosses the water rim.
	"mermaid_pool": Vector2(220.0, 508.0),
	"playroom": Vector2(640.0, 390.0),
	"craft_room": Vector2(640.0, 390.0),
}
const DEFAULT_DOOR_RECTS: Dictionary = {
	"bubble_bath": Rect2(612.0, 250.0, 56.0, 112.0),
	"mermaid_pool": Rect2(612.0, 250.0, 56.0, 112.0),
	"playroom": Rect2(612.0, 250.0, 56.0, 112.0),
	"craft_room": Rect2(612.0, 250.0, 56.0, 112.0),
}
const DEFAULT_BOSS_BACK_DOOR := Rect2(610.0, 104.0, 60.0, 108.0)
const MAIN_HALL_ID := "main_hall"
const DUST_BUNNY_TEXTURES: Dictionary = {
	"bubble_bath": "res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_shell_hide.png",
	"mermaid_pool": "res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_curl_ears.png",
	"craft_room": "res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_curl_ears.png",
}
# Rooms whose cleanup authors its own dirty state (dirty fixture art, a declared
# room tint with Roshan counter-tinted, gold-star pattern GS-17) and therefore
# draw no code-shaped wash, grime, drips or cracks over the room and Roshan.
const AUTHORED_DIRT_ROOMS: Array[String] = ["mermaid_pool"]
var _room_centers: Dictionary = {}
var _door_rects: Dictionary = {}
var _hall_door_rects: Dictionary = {}
var _room_dirty: Dictionary = {}
var _door_unlocked: Dictionary = {}
var _boss_back_door_rect: Rect2 = DEFAULT_BOSS_BACK_DOOR
var _boss_back_door_active := false
var _visible_room_id := MAIN_HALL_ID
var _dust_bunnies: Dictionary = {}
var _elapsed := 0.0
var _configured := false
var _grime: DayOneCastleGrime = null


static func create_dressing(parent: Node, config: Dictionary = {}) -> DayOneCastleDressing:
	var dressing: DayOneCastleDressing = DayOneCastleDressing.new()
	dressing.configure(config)
	if parent != null:
		parent.add_child(dressing)
	return dressing


func _ready() -> void:
	if not _configured:
		configure()
	_ensure_grime()
	_ensure_dust_bunnies()
	set_process(true)


func configure(config: Dictionary = {}) -> void:
	_room_centers.clear()
	_door_rects.clear()
	_hall_door_rects.clear()
	_room_dirty.clear()
	_door_unlocked.clear()
	for room_id: String in ROOM_IDS:
		var center: Vector2 = DEFAULT_ROOM_CENTERS[room_id]
		var center_value: Variant = config.get("room_centers", {}).get(room_id, center)
		if center_value is Vector2:
			center = center_value
		_room_centers[room_id] = center
		var door_rect: Rect2 = DEFAULT_DOOR_RECTS[room_id]
		var door_value: Variant = config.get("door_rects", {}).get(room_id, door_rect)
		if door_value is Rect2:
			door_rect = door_value
		_door_rects[room_id] = door_rect
		_room_dirty[room_id] = true
		_door_unlocked[room_id] = false
	var boss_rect_value: Variant = config.get("boss_back_door_rect", DEFAULT_BOSS_BACK_DOOR)
	if boss_rect_value is Rect2:
		_boss_back_door_rect = boss_rect_value
	_boss_back_door_active = bool(config.get("boss_back_door_active", false))
	_visible_room_id = String(config.get("visible_room_id", MAIN_HALL_ID))
	if _visible_room_id != MAIN_HALL_ID and not _room_centers.has(_visible_room_id):
		_visible_room_id = MAIN_HALL_ID
	_configured = true
	_ensure_grime()
	_ensure_dust_bunnies()
	_refresh_dust_visibility()
	_refresh_grime()


func update_dressing(delta: float, state: Dictionary = {}) -> void:
	if not _configured:
		configure()
	_elapsed += maxf(delta, 0.0)
	var dirty_rooms: Variant = state.get("room_dirty", {})
	if dirty_rooms is Dictionary:
		for room_id: String in ROOM_IDS:
			if dirty_rooms.has(room_id):
				_room_dirty[room_id] = bool(dirty_rooms[room_id])
	var unlocked_doors: Variant = state.get("door_unlocked", {})
	if unlocked_doors is Dictionary:
		for room_id: String in ROOM_IDS:
			if unlocked_doors.has(room_id):
				_door_unlocked[room_id] = bool(unlocked_doors[room_id])
	if state.has("boss_back_door_active"):
		_boss_back_door_active = bool(state["boss_back_door_active"])
	if state.has("visible_room_id"):
		set_visible_room(String(state["visible_room_id"]))
	_refresh_dust_visibility()
	_refresh_grime()


func set_visible_room(room_id: String) -> void:
	if room_id != MAIN_HALL_ID and not _room_centers.has(room_id):
		return
	_visible_room_id = room_id
	_refresh_dust_visibility()
	_refresh_grime()


func visible_room_id() -> String:
	return _visible_room_id


func set_room_dirty(room_id: String, dirty: bool) -> void:
	if not _room_dirty.has(room_id):
		return
	_room_dirty[room_id] = dirty
	_refresh_dust_visibility()
	_refresh_grime()


func set_door_unlocked(door_id: String, unlocked: bool) -> void:
	if not _door_unlocked.has(door_id):
		return
	_door_unlocked[door_id] = unlocked


func set_room_door_rect(door_id: String, stage_rect: Rect2) -> void:
	if not _door_rects.has(door_id):
		return
	if stage_rect.size.x <= 0.0 or stage_rect.size.y <= 0.0:
		_hall_door_rects.erase(door_id)
	else:
		_hall_door_rects[door_id] = stage_rect


func activate_boss_back_door(active: bool = true) -> void:
	_boss_back_door_active = active


func set_boss_back_door_rect(stage_rect: Rect2) -> void:
	if stage_rect.size.x <= 0.0 or stage_rect.size.y <= 0.0:
		return
	_boss_back_door_rect = stage_rect


func room_ids() -> Array[String]:
	var ids: Array[String] = []
	for room_id: String in ROOM_IDS:
		ids.append(room_id)
	return ids


func room_is_dirty(room_id: String) -> bool:
	return bool(_room_dirty.get(room_id, false))


func door_is_unlocked(door_id: String) -> bool:
	return bool(_door_unlocked.get(door_id, false))


func boss_back_door_is_active() -> bool:
	return _boss_back_door_active


func audit_snapshot() -> Dictionary:
	return {
		"room_count": ROOM_IDS.size(),
		"room_ids": room_ids(),
		"visible_room_id": _visible_room_id,
		"dirty_room_count": _count_true(_room_dirty),
		"unlocked_door_count": _count_true(_door_unlocked),
		"readable_door_count": _door_rects.size(),
		"visible_hall_door_count": _hall_door_rects.size(),
		"dust_bunny_count": _dust_bunnies.size(),
		"dust_bunny_sprite2d": true,
		"pool_land_bunny": _pool_land_bunny_snapshot(),
		"exterior_grime": true,
		"interior_disrepair": true,
		"boss_back_door_active": _boss_back_door_active,
		"door_visual_owner": "castle_rooms",
		"independent_door_glows": false,
		"procedural_canvas": true,
		"procedural_grime_owner": "day_one_castle_grime",
		"authored_dirt_rooms": AUTHORED_DIRT_ROOMS.duplicate(),
		"procedural_grime_visible": _grime != null and is_instance_valid(_grime)
			and _grime.visible,
		"canvas_only": true,
	}


func _pool_land_bunny_snapshot() -> Dictionary:
	var bunny: Sprite2D = _dust_bunnies.get("mermaid_pool") as Sprite2D
	if bunny == null or not is_instance_valid(bunny):
		return {}
	var shore_bounds := Rect2(160.0, 550.0, 140.0, 80.0)
	return {
		"count": 1,
		"position": bunny.position,
		"shore_bounds": shore_bounds,
		"landlocked": shore_bounds.has_point(bunny.position),
		"asset": bunny.texture.resource_path if bunny.texture != null else "",
		"true_2d": true,
	}


func teardown() -> void:
	set_process(false)
	if is_inside_tree():
		queue_free()
	else:
		free()


func _process(delta: float) -> void:
	update_dressing(delta)


func _ensure_dust_bunnies() -> void:
	if not is_inside_tree() and get_parent() == null:
		return
	for room_id: String in ROOM_IDS:
		# The playroom already owns the two interactive pinning bunnies.
		# A third decorative family overlapped Eagle and confused the rescue.
		if not DUST_BUNNY_TEXTURES.has(room_id) or _dust_bunnies.has(room_id):
			continue
		var texture_path: String = DUST_BUNNY_TEXTURES[room_id]
		var texture: Texture2D = load(texture_path) as Texture2D
		if texture == null:
			continue
		var bunny: Sprite2D = Sprite2D.new()
		bunny.name = "DustBunny_%s" % room_id
		bunny.texture = texture
		bunny.z_index = 5
		var longest_side: float = maxf(texture.get_size().x, texture.get_size().y)
		bunny.scale = Vector2.ONE * minf(1.0, 86.0 / maxf(longest_side, 1.0))
		add_child(bunny)
		_dust_bunnies[room_id] = bunny


func _refresh_dust_visibility() -> void:
	for room_id: String in ROOM_IDS:
		var bunny: Sprite2D = _dust_bunnies.get(room_id) as Sprite2D
		if bunny == null:
			continue
		var center: Vector2 = _room_centers[room_id]
		var room_index: int = ROOM_IDS.find(room_id)
		var phase: float = _elapsed * (0.8 + float(room_index) * 0.08) + float(room_index) * 1.45
		bunny.position = center + Vector2(sin(phase) * 42.0, 82.0 + sin(phase * 1.8) * 2.0)
		bunny.visible = _visible_room_id == room_id and room_is_dirty(room_id)


func room_owns_authored_dirt(room_id: String) -> bool:
	return AUTHORED_DIRT_ROOMS.has(room_id)


func _ensure_grime() -> void:
	if _grime != null and is_instance_valid(_grime):
		return
	_grime = DayOneCastleGrime.new()
	_grime.name = "DayOneCastleGrime"
	add_child(_grime)


func _refresh_grime() -> void:
	if _grime == null or not is_instance_valid(_grime):
		return
	# The exterior edge grime belongs to the shared castle frame, so a room that
	# authors its own dirt hides the whole code-drawn layer, not just its wash.
	_grime.visible = _configured and not room_owns_authored_dirt(_visible_room_id)
	var center: Vector2 = _room_centers.get(_visible_room_id, Vector2.ZERO) as Vector2
	_grime.show_for(_visible_room_id, center, room_is_dirty(_visible_room_id))


func _count_true(values: Dictionary) -> int:
	var count := 0
	for value: Variant in values.values():
		if bool(value):
			count += 1
	return count
