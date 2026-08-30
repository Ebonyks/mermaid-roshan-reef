class_name FairyConservatoryHandoff2D
extends RefCounted
## True-2D, touch-first bridge from the Moonflower doorway to Butterfly House.
##
## This satellite owns only temporary Canvas nodes and interaction logic. The
## caller remains the state owner and receives exactly "butterfly_house" or
## "back" from the finish callback. Progress advances only from an explicit
## tap on the next rainbow waypoint; there is no timer, penalty, or fail state.

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const CANVAS_LAYER := 22
const TILE_COLUMNS := 4
const TILE_ROWS := 2
const TILE_SIZE := Vector2(910.0, 1024.0)
const TILE_PATHS: Array[String] = [
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r0_c0.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r0_c1.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r0_c2.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r0_c3.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r1_c0.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r1_c1.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r1_c2.png",
	"res://assets/flats/fairy_conservatory_handoff/background/handoff_background_r1_c3.png",
]
const WALKWAY_PATH := "res://assets/flats/fairy_conservatory_handoff/rainbow_walkway.png"
const HOUSE_PATH := "res://assets/flats/fairy_conservatory_handoff/butterfly_house.png"
const ROSHAN_PATH := "res://assets/characters/roshan_25d/roshan_base.png"
const POINTER_PATH := "res://assets/castle/training/ghost_hand.png"
const WALK_WAYPOINTS: Array[Vector2] = [
	Vector2(640.0, 600.0),
	Vector2(640.0, 500.0),
	Vector2(640.0, 375.0),
]
const HOUSE_HOTSPOT := Rect2(500.0, 44.0, 280.0, 300.0)
const MIN_TOUCH := Vector2(112.0, 112.0)
const ROSHAN_NEAR_POSITION := Vector2(640.0, 594.0)
const ROSHAN_FAR_POSITION := Vector2(640.0, 330.0)
const ROSHAN_VISIBLE_SOURCE_SIZE := Vector2(171.0, 219.0)
const ROSHAN_NEAR_VISIBLE_SIZE := Vector2(134.0, 172.0)
const ROSHAN_FAR_VISIBLE_SIZE := Vector2(76.0, 98.0)

var _main: Node = null
var _finish_cb: Callable
var _layer: CanvasLayer = null
var _root: Control = null
var _world: Node2D = null
var _backdrop: ColorRect = null
var _walkway: Sprite2D = null
var _house: Sprite2D = null
var _roshan: Sprite2D = null
var _pointer: Sprite2D = null
var _house_button: Button = null
var _back_button: Button = null
var _tiles: Array[Sprite2D] = []
var _state := "rainbow_stage"
var _waypoint_index := 0
var _finished := false
var _returning_from_butterfly := false
var _pointer_base := Vector2.ZERO
var _pointer_phase := 0.0


func start(main: Node, finish_cb: Callable,
		returning_from_butterfly: bool = false) -> void:
	teardown()
	_main = main
	_finish_cb = finish_cb
	_returning_from_butterfly = returning_from_butterfly
	_state = "rainbow_return" if returning_from_butterfly else "rainbow_stage"
	_waypoint_index = WALK_WAYPOINTS.size() if returning_from_butterfly else 0
	_finished = false
	_pointer_phase = 0.0

	_layer = CanvasLayer.new()
	_layer.name = "FairyConservatoryHandoff2D"
	_layer.layer = CANVAS_LAYER
	_layer.process_mode = Node.PROCESS_MODE_ALWAYS
	_main.add_child(_layer)

	_root = Control.new()
	_root.name = "HandoffRoot"
	_root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_STOP
	_root.gui_input.connect(_on_root_gui_input)
	_root.resized.connect(_layout_world)
	_layer.add_child(_root)

	_backdrop = ColorRect.new()
	_backdrop.name = "HandoffBackdropFallback"
	_backdrop.color = Color(0.20, 0.12, 0.36, 1.0)
	_backdrop.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_root.add_child(_backdrop)
	_backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	_world = Node2D.new()
	_world.name = "HandoffCanvasWorld"
	_root.add_child(_world)
	_build_tiles()
	_walkway = _make_sprite("RainbowWalkway", WALKWAY_PATH)
	_house = _make_sprite("ButterflyHouse", HOUSE_PATH)
	_roshan = _make_sprite("RoshanHandoff", ROSHAN_PATH)
	_pointer = _make_sprite("HandoffPointer", POINTER_PATH)
	if _walkway != null:
		_world.add_child(_walkway)
	if _house != null:
		_world.add_child(_house)
	if _roshan != null:
		_world.add_child(_roshan)
	if _pointer != null:
		_world.add_child(_pointer)
	_build_navigation()
	_layout_world()
	_refresh_state()
	_announce_state()
	if _main.has_method("_set_world_controls_enabled"):
		_main.call("_set_world_controls_enabled", false,
			"fairy_conservatory_handoff_2d")


func teardown() -> void:
	if _main != null and is_instance_valid(_main) \
			and _main.has_method("_set_world_controls_enabled"):
		_main.call("_set_world_controls_enabled", true,
			"fairy_conservatory_handoff_2d")
	if _layer != null and is_instance_valid(_layer):
		_layer.queue_free()
	_layer = null
	_root = null
	_world = null
	_backdrop = null
	_walkway = null
	_house = null
	_roshan = null
	_pointer = null
	_house_button = null
	_back_button = null
	_tiles.clear()
	_finish_cb = Callable()
	_main = null


func tick(delta: float) -> void:
	if _finished or _pointer == null or not is_instance_valid(_pointer):
		return
	_pointer_phase += maxf(delta, 0.0)
	_pointer.position = _pointer_base + Vector2(0.0,
		sin(_pointer_phase * 4.0) * 7.0)


func probe_tap(logical_position: Vector2) -> void:
	_handle_logical_tap(logical_position)


func audit_snapshot() -> Dictionary:
	var loaded_tiles := 0
	for tile: Sprite2D in _tiles:
		if tile != null and tile.texture != null:
			loaded_tiles += 1
	return {
		"active": _layer != null and is_instance_valid(_layer),
		"state": _state,
		"returning_from_butterfly": _returning_from_butterfly,
		"waypoint_index": _waypoint_index,
		"waypoint_count": WALK_WAYPOINTS.size(),
		"progress": float(_waypoint_index) / float(WALK_WAYPOINTS.size()),
		"background_tile_paths": TILE_PATHS.duplicate(),
		"background_tile_count": _tiles.size(),
		"background_tiles_loaded": loaded_tiles,
		"rainbow_walkway_path": WALKWAY_PATH,
		"rainbow_walkway_loaded": _walkway != null and _walkway.texture != null,
		"butterfly_house_path": HOUSE_PATH,
		"butterfly_house_loaded": _house != null and _house.texture != null,
		"rainbow_walkway_visible": _walkway != null and _walkway.visible,
		"butterfly_house_visible": _house != null and _house.visible,
		"one_point_route_centered": _route_is_centered(),
		"roshan_is_sprite2d": _roshan != null,
		"pointer_is_sprite2d": _pointer != null,
		"has_house_hotspot": _house_button != null,
		"house_hotspot_size": _house_button.size if _house_button != null else Vector2.ZERO,
		"has_back_button": _back_button != null,
		"no_fail_state": true,
		"has_timer": false,
		"uses_spatial_runtime": false,
		"roshan_position": _roshan.position if _roshan != null else Vector2.ZERO,
		"pointer_base": _pointer_base,
		"house_hotspot_visible": _house_button != null and _house_button.visible,
		"finished": _finished,
	}


func _build_tiles() -> void:
	for index: int in range(TILE_PATHS.size()):
		var tile := _make_sprite("HandoffBackground_r%d_c%d" % [
			index / TILE_COLUMNS, index % TILE_COLUMNS], TILE_PATHS[index])
		if tile == null:
			continue
		tile.z_index = -20
		_tiles.append(tile)
		_world.add_child(tile)


func _make_sprite(node_name: String, path: String) -> Sprite2D:
	var sprite := Sprite2D.new()
	sprite.name = node_name
	sprite.centered = true
	sprite.texture = load(path) as Texture2D if ResourceLoader.exists(path) else null
	sprite.set_meta("approved_runtime_path", path)
	sprite.set_meta("canvas_only", true)
	return sprite


func _build_navigation() -> void:
	_back_button = Button.new()
	_back_button.name = "HandoffBack"
	_back_button.position = Vector2(28.0, 24.0)
	_back_button.size = Vector2(148.0, 112.0)
	_back_button.text = "←"
	_back_button.tooltip_text = "Back to the castle"
	_back_button.focus_mode = Control.FOCUS_NONE
	_back_button.pressed.connect(_finish.bind("back"))
	_root.add_child(_back_button)

	_house_button = Button.new()
	_house_button.name = "ButterflyHouseHotspot"
	_house_button.position = HOUSE_HOTSPOT.position
	_house_button.size = HOUSE_HOTSPOT.size
	_house_button.text = ""
	_house_button.tooltip_text = "Enter Butterfly House"
	_house_button.focus_mode = Control.FOCUS_NONE
	_house_button.flat = true
	_house_button.self_modulate = Color(1.0, 1.0, 1.0, 0.0)
	_house_button.pressed.connect(_enter_house)
	_root.add_child(_house_button)


func _layout_world() -> void:
	if _root == null or _world == null:
		return
	var viewport_size := _root.size
	if viewport_size.x <= 0.0 or viewport_size.y <= 0.0:
		viewport_size = CANVAS_SIZE
	var fit_scale := minf(viewport_size.x / CANVAS_SIZE.x,
		viewport_size.y / CANVAS_SIZE.y)
	_world.scale = Vector2.ONE * fit_scale
	_world.position = (viewport_size - CANVAS_SIZE * fit_scale) * 0.5
	for index: int in range(_tiles.size()):
		var tile: Sprite2D = _tiles[index]
		var row: int = index / TILE_COLUMNS
		var column: int = index % TILE_COLUMNS
		tile.position = Vector2(
			(float(column) + 0.5) * CANVAS_SIZE.x / TILE_COLUMNS,
			(float(row) + 0.5) * CANVAS_SIZE.y / TILE_ROWS)
		tile.scale = Vector2(
			CANVAS_SIZE.x / float(TILE_COLUMNS) / TILE_SIZE.x,
			CANVAS_SIZE.y / float(TILE_ROWS) / TILE_SIZE.y)
	if _walkway != null:
		_walkway.position = Vector2(640.0, 500.0)
		_fit_sprite(_walkway, Vector2(620.0, 620.0))
		_walkway.z_index = -5
	if _house != null:
		_house.position = Vector2(640.0, 184.0)
		_fit_sprite(_house, Vector2(270.0, 270.0))
		_house.z_index = -4
	if _roshan != null:
		_roshan.z_index = 4
		_update_roshan_position()
	if _pointer != null:
		_pointer.z_index = 8
		_pointer.scale = Vector2.ONE * 0.12
	if _back_button != null:
		_back_button.position = _world.position + Vector2(28.0, 24.0) * fit_scale
		_back_button.size = Vector2(148.0, 112.0) * fit_scale
	if _house_button != null:
		_house_button.position = _world.position + HOUSE_HOTSPOT.position * fit_scale
		_house_button.size = Vector2(
			maxf(HOUSE_HOTSPOT.size.x, MIN_TOUCH.x),
			maxf(HOUSE_HOTSPOT.size.y, MIN_TOUCH.y)) * fit_scale


func _fit_sprite(sprite: Sprite2D, target_size: Vector2) -> void:
	if sprite.texture == null:
		return
	var source_size := sprite.texture.get_size()
	if source_size.x <= 0.0 or source_size.y <= 0.0:
		return
	var scale_value := minf(target_size.x / source_size.x,
		target_size.y / source_size.y)
	sprite.scale = Vector2.ONE * scale_value


func _refresh_state() -> void:
	var house_visible := _state == "butterfly_house"
	if _walkway != null:
		_walkway.visible = true
	if _house != null:
		_house.visible = true
	if _house_button != null:
		_house_button.visible = house_visible
	if _roshan != null:
		_roshan.visible = true
		_update_roshan_position()
	if _pointer != null:
		_pointer.visible = true
		if house_visible:
			_pointer_base = HOUSE_HOTSPOT.get_center() + Vector2(-44.0, -88.0)
		elif _state == "rainbow_return":
			_pointer_base = _return_waypoint() + Vector2(-42.0, -82.0)
		else:
			_pointer_base = _next_waypoint() + Vector2(-42.0, -82.0)
		_pointer.position = _pointer_base


func _update_roshan_position() -> void:
	if _roshan == null:
		return
	var progress := clampf(float(_waypoint_index)
		/ float(WALK_WAYPOINTS.size()), 0.0, 1.0)
	_roshan.position = ROSHAN_NEAR_POSITION.lerp(
		ROSHAN_FAR_POSITION, progress)
	_fit_sprite_visible(_roshan,
		ROSHAN_NEAR_VISIBLE_SIZE.lerp(ROSHAN_FAR_VISIBLE_SIZE, progress),
		ROSHAN_VISIBLE_SOURCE_SIZE)


func _fit_sprite_visible(sprite: Sprite2D, target_visible_size: Vector2,
		source_visible_size: Vector2) -> void:
	# Roshan's approved 256-square registration card has transparent animation
	# padding. Scale its known visible alpha bounds so runtime and the flattened
	# review composite agree on the child's actual on-screen height.
	if sprite.texture == null or source_visible_size.x <= 0.0 \
			or source_visible_size.y <= 0.0:
		return
	var scale_value := minf(target_visible_size.x / source_visible_size.x,
		target_visible_size.y / source_visible_size.y)
	sprite.scale = Vector2.ONE * scale_value


func _route_is_centered() -> bool:
	for waypoint: Vector2 in WALK_WAYPOINTS:
		if absf(waypoint.x - CANVAS_SIZE.x * 0.5) > 1.0:
			return false
	return true


func _next_waypoint() -> Vector2:
	if _waypoint_index >= WALK_WAYPOINTS.size():
		return HOUSE_HOTSPOT.get_center()
	return WALK_WAYPOINTS[_waypoint_index]


func _return_waypoint() -> Vector2:
	if _waypoint_index <= 0:
		return WALK_WAYPOINTS[0]
	return WALK_WAYPOINTS[mini(
		_waypoint_index - 1, WALK_WAYPOINTS.size() - 1)]


func _on_root_gui_input(event: InputEvent) -> void:
	if _finished:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_handle_viewport_tap(touch.position)
	elif event is InputEventMouseButton:
		var mouse := event as InputEventMouseButton
		if mouse.pressed and mouse.button_index == MOUSE_BUTTON_LEFT:
			_handle_viewport_tap(mouse.position)


func _handle_viewport_tap(viewport_position: Vector2) -> void:
	if _world == null:
		return
	var logical := _world.get_global_transform_with_canvas().affine_inverse() \
		* viewport_position
	_handle_logical_tap(logical)


func _handle_logical_tap(logical_position: Vector2) -> void:
	if _finished:
		return
	if _state == "butterfly_house":
		if HOUSE_HOTSPOT.has_point(logical_position):
			_enter_house()
		return
	if _state == "rainbow_return":
		var return_target := _return_waypoint()
		var return_touch := Rect2(return_target - MIN_TOUCH * 0.5, MIN_TOUCH)
		if not return_touch.has_point(logical_position):
			return
		_waypoint_index = maxi(_waypoint_index - 1, 0)
		if _main != null and is_instance_valid(_main) \
				and _main.has_method("_ui_tap"):
			_main.call("_ui_tap")
		if _waypoint_index <= 0:
			_finish("back")
		else:
			_refresh_state()
		return
	var next := _next_waypoint()
	var touch_size := Rect2(next - MIN_TOUCH * 0.5, MIN_TOUCH)
	if touch_size.has_point(logical_position):
		_waypoint_index = mini(_waypoint_index + 1, WALK_WAYPOINTS.size())
		if _main != null and is_instance_valid(_main) \
				and _main.has_method("_ui_tap"):
			_main.call("_ui_tap")
		if _waypoint_index >= WALK_WAYPOINTS.size():
			_state = "butterfly_house"
			_announce_state()
		_refresh_state()


func _enter_house() -> void:
	if _state != "butterfly_house" or _finished:
		return
	_finish("butterfly_house")


func _finish(result: String) -> void:
	if _finished:
		return
	_finished = true
	if _finish_cb.is_valid():
		_finish_cb.call(result)


func _announce_state() -> void:
	if _main == null or not is_instance_valid(_main):
		return
	if _state == "butterfly_house":
		if _main.has_method("show_msg"):
			_main.call("show_msg", "Rosalina",
				"The Butterfly House is here! Tap the big house to go inside!",
				"open")
	elif _state == "rainbow_return":
		if _main.has_method("show_msg"):
			_main.call("show_msg", "Rosalina",
				"Follow the rainbow home! Tap the bright path back to the castle!",
				"home")
	else:
		if _main.has_method("show_msg"):
			_main.call("show_msg", "Rosalina",
				"Walk along the rainbow to the Butterfly House! Tap the next bright path!",
				"talk")
	if _main.has_method("_say"):
		_main.call("_say", "roshan", "talk", 0.0)
