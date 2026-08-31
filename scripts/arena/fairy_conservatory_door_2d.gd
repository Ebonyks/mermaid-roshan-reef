class_name FairyConservatoryDoor2D
extends RefCounted
# Chapter 3 doorway overlay for the approved Pearl Castle Main Hall. The
# CastleRooms25D source is protected by a hash-backed frame-approval ledger;
# this satellite owns only the new whole-card door, cue, and touch route.

const DoorLanguage := preload("res://scripts/castle_door_language.gd")
const DoorCue := preload("res://scripts/castle_door_cue.gd")
const DOOR_DORMANT := \
	"res://assets/flats/castle/fairy_conservatory/moonflower_door_closed.png"
const DOOR_AVAILABLE := \
	"res://assets/flats/castle/fairy_conservatory/butterfly_gate_available.png"
const HALL_STAGE_SCALE := 1280.0 / 1672.0
const DOOR_Z := 0.70
const DOOR_FOOT := Vector2(1672.0, 620.0)
const DORMANT_CENTER := Vector2(1672.0, 385.0)
const DORMANT_ART_SCALE := 0.4896
const AVAILABLE_ART_SCALE := 0.5372
const AVAILABLE_CENTER := Vector2(
	1672.0,
	DOOR_FOOT.y - (992.0 - 512.0) * AVAILABLE_ART_SCALE)
const DOOR_CARD_ART_RECT := Rect2(1396.0, 87.0, 552.0, 552.0)
const DOOR_HOTSPOT_RECT := Rect2(1396.0, 142.0, 552.0, 498.0)
const REVEALED_KEY := "chapter3_fairy_door_revealed"
const OPENED_KEY := "chapter3_fairy_door_opened"

var m: ReefMain
var fairy_conservatory_card: Sprite2D = null
var fairy_conservatory_cue: Control = null
var fairy_conservatory_hotspot: Button = null
var _render_state := ""
var _opening := false


func _init(main: ReefMain) -> void:
	m = main


func tick() -> void:
	if not _hall_active():
		_remove_nodes()
		return
	if fairy_conservatory_card == null \
			or not is_instance_valid(fairy_conservatory_card):
		_build()
	_sync()


func refresh() -> void:
	tick()


func visual_state() -> String:
	if _flag(OPENED_KEY) or _legacy_open():
		return "open"
	if _flag(REVEALED_KEY) \
			or _flag("chapter3_rainbow_candle_lit") \
			or _flag("rainbow_candle_lit"):
		return "revealed"
	return "closed"


func _hall_active() -> bool:
	return m.castle_room_id == "main_hall" \
		and m.castle_room_layer != null \
		and is_instance_valid(m.castle_room_layer) \
		and m.castle_room_mid_layer != null \
		and is_instance_valid(m.castle_room_mid_layer)


func _build() -> void:
	_remove_nodes()
	var state := visual_state()
	var texture_path := _texture_path(state)
	if not ResourceLoader.exists(texture_path):
		push_warning("Missing Fairy Conservatory door card: "
			+ texture_path)
		return
	var texture: Texture2D = load(texture_path) as Texture2D
	if texture == null:
		return
	fairy_conservatory_card = Sprite2D.new()
	fairy_conservatory_card.name = "MoonflowerConservatoryDoor"
	fairy_conservatory_card.texture = texture
	fairy_conservatory_card.centered = true
	_apply_state_transform(state)
	fairy_conservatory_card.z_index = int(round(DOOR_Z * 100.0))
	fairy_conservatory_card.set_meta("source_asset_role",
		"chapter3_story_door")
	fairy_conservatory_card.set_meta("source_object_id",
		"main_hall:moonflower_conservatory")
	fairy_conservatory_card.set_meta("source_asset_path", texture_path)
	fairy_conservatory_card.set_meta("source_art_position",
		_art_center(state))
	fairy_conservatory_card.set_meta("source_foot", DOOR_FOOT)
	fairy_conservatory_card.set_meta("hall_horizontal_cull", true)
	fairy_conservatory_card.set_meta("hall_horizontal_cull_kind",
		"fairy_conservatory_door")
	fairy_conservatory_card.set_meta("hall_horizontal_cull_rect",
		DOOR_CARD_ART_RECT)
	fairy_conservatory_card.set_meta("depth_z", DOOR_Z)
	m.castle_room_mid_layer.add_child(fairy_conservatory_card)
	_render_state = state


func _sync() -> void:
	if not _hall_active() or fairy_conservatory_card == null \
			or not is_instance_valid(fairy_conservatory_card):
		return
	var state := visual_state()
	if state != _render_state:
		var texture_path := _texture_path(state)
		var texture: Texture2D = load(texture_path) as Texture2D
		if texture != null:
			fairy_conservatory_card.texture = texture
			fairy_conservatory_card.set_meta("source_asset_path",
				texture_path)
			_apply_state_transform(state)
			_render_state = state
	if state == "revealed" or state == "open":
		_ensure_hotspot()
		if state == "open":
			_remove_cue()
	else:
		_remove_hotspot()
	_update_hotspot()
	fairy_conservatory_card.visible = _door_inside_hall_span()


func _texture_path(state: String) -> String:
	return DOOR_DORMANT if state == "closed" else DOOR_AVAILABLE


func _art_center(state: String) -> Vector2:
	return DORMANT_CENTER if state == "closed" else AVAILABLE_CENTER


func _art_scale(state: String) -> float:
	return DORMANT_ART_SCALE if state == "closed" else AVAILABLE_ART_SCALE


func _apply_state_transform(state: String) -> void:
	if fairy_conservatory_card == null:
		return
	var art_center := _art_center(state)
	fairy_conservatory_card.position = _hall_art_to_world(art_center)
	fairy_conservatory_card.scale = Vector2.ONE \
		* _art_scale(state) * HALL_STAGE_SCALE
	fairy_conservatory_card.set_meta("source_art_position", art_center)


func _flag(key: String) -> bool:
	var property_value: Variant = m.get(key)
	if property_value != null:
		return bool(property_value)
	if m.save_data is Dictionary:
		return bool(m.save_data.get(key, false))
	return false


func _legacy_open() -> bool:
	if not (m.save_data is Dictionary):
		return false
	return bool(m.save_data.get("bwdone", false)) \
		or bool(m.save_data.get("fairyskin", false)) \
		or bool(m.save_data.get("galaxy", false))


func _set_flag(key: String) -> void:
	if m.has_method("set_fairy_conservatory_flag"):
		m.call("set_fairy_conservatory_flag", key, true)
	elif m.get(key) != null:
		m.set(key, true)
	if m.save_data is Dictionary:
		m.save_data[key] = true


func _ensure_hotspot() -> void:
	if fairy_conservatory_hotspot != null \
			and is_instance_valid(fairy_conservatory_hotspot):
		return
	if m.castle_room_door_hotspot_layer == null:
		return
	fairy_conservatory_cue = DoorCue.new()
	fairy_conservatory_cue.name = "MoonflowerConservatoryPointer"
	fairy_conservatory_cue.z_index = 0
	fairy_conservatory_cue.set_meta("chapter3_fairy_conservatory", true)
	fairy_conservatory_cue.call("set_door_state", DoorLanguage.PLOT)
	m.castle_room_door_hotspot_layer.add_child(fairy_conservatory_cue)
	fairy_conservatory_hotspot = Button.new()
	fairy_conservatory_hotspot.name = "MoonflowerConservatoryHotspot"
	fairy_conservatory_hotspot.flat = true
	fairy_conservatory_hotspot.focus_mode = Control.FOCUS_NONE
	fairy_conservatory_hotspot.tooltip_text = "Moonflower Conservatory"
	fairy_conservatory_hotspot.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
	fairy_conservatory_hotspot.set_meta("uses_own_sfx", true)
	fairy_conservatory_hotspot.set_meta("chapter3_fairy_conservatory", true)
	fairy_conservatory_hotspot.pressed.connect(_open)
	m.castle_room_door_hotspot_layer.add_child(fairy_conservatory_hotspot)


func _remove_hotspot() -> void:
	_remove_cue()
	if fairy_conservatory_hotspot != null \
			and is_instance_valid(fairy_conservatory_hotspot):
		fairy_conservatory_hotspot.free()
	fairy_conservatory_hotspot = null


func _remove_cue() -> void:
	if fairy_conservatory_cue != null \
			and is_instance_valid(fairy_conservatory_cue):
		fairy_conservatory_cue.free()
	fairy_conservatory_cue = null


func _remove_nodes() -> void:
	_remove_hotspot()
	if fairy_conservatory_card != null \
			and is_instance_valid(fairy_conservatory_card):
		fairy_conservatory_card.free()
	fairy_conservatory_card = null
	_render_state = ""
	_opening = false


func _update_hotspot() -> void:
	if fairy_conservatory_hotspot == null \
			or not is_instance_valid(fairy_conservatory_hotspot) \
			or m.castle_room_world_root == null:
		return
	var world_xform: Transform2D = \
		m.castle_room_world_root.get_global_transform_with_canvas()
	var stage_top_left := _canvas_to_stage(world_xform \
		* _hall_art_to_world(DOOR_HOTSPOT_RECT.position))
	var stage_bottom_right := _canvas_to_stage(world_xform \
		* _hall_art_to_world(DOOR_HOTSPOT_RECT.end))
	var projected := Rect2(
		Vector2(minf(stage_top_left.x, stage_bottom_right.x),
			minf(stage_top_left.y, stage_bottom_right.y)),
		Vector2(absf(stage_bottom_right.x - stage_top_left.x),
			absf(stage_bottom_right.y - stage_top_left.y)))
	var canvas_rect := Rect2(Vector2.ZERO, StorybookUI.CANVAS_SIZE)
	var visible_rect := projected.intersection(canvas_rect) \
		if projected.intersects(canvas_rect) else Rect2()
	var active := (_render_state == "revealed" or _render_state == "open") \
		and visible_rect.has_area()
	fairy_conservatory_hotspot.visible = active
	if fairy_conservatory_cue != null:
		fairy_conservatory_cue.visible = active and _render_state == "revealed"
		fairy_conservatory_cue.position = visible_rect.position
		fairy_conservatory_cue.size = visible_rect.size
	if not active:
		return
	var hit_size := Vector2(maxf(112.0, visible_rect.size.x),
		maxf(112.0, visible_rect.size.y))
	var hit_position := visible_rect.get_center() - hit_size * 0.5
	hit_position.x = clampf(hit_position.x, 0.0,
		StorybookUI.CANVAS_SIZE.x - hit_size.x)
	hit_position.y = clampf(hit_position.y, 0.0,
		StorybookUI.CANVAS_SIZE.y - hit_size.y)
	fairy_conservatory_hotspot.position = hit_position
	fairy_conservatory_hotspot.size = hit_size


func _door_inside_hall_span() -> bool:
	var rooms: CastleRooms25D = m._castle_rooms_ref()
	var span: Vector2 = rooms._hall_horizontal_cull_span()
	return DOOR_CARD_ART_RECT.end.x >= span.x \
		and DOOR_CARD_ART_RECT.position.x <= span.y


func _hall_art_to_world(art_position: Vector2) -> Vector2:
	return art_position * HALL_STAGE_SCALE


func _canvas_to_stage(canvas_position: Vector2) -> Vector2:
	if m.castle_room_stage == null:
		return canvas_position
	return m.castle_room_stage.get_global_transform_with_canvas() \
		.affine_inverse() * canvas_position


func _open() -> void:
	if _opening or not _hall_active():
		return
	if _render_state == "open":
		m.call("_start_fairy_conservatory_handoff")
		return
	if _render_state != "revealed":
		return
	_opening = true
	_set_flag(REVEALED_KEY)
	_set_flag(OPENED_KEY)
	_render_state = "revealed"
	_sync()
	m.call("_ui_tap")
	m.call("_write_save")
	_opening = false
	m.call("_start_fairy_conservatory_handoff")
