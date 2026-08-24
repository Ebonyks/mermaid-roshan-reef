class_name DayOneBathroomCleanup
extends Control
## Day One's first bathroom beat: a reading-free two-supply magnifier hunt.
##
## This node owns only the temporary Canvas2D hunt presentation. The later
## sink/tub cleaning gestures are deliberately left behind the handoff signal
## so a partial hunt can never unlock the pool or complete the room.

const DAY_ONE_BATHROOM_CLEANING := preload(
	"res://scripts/games/day_one_bathroom_cleaning.gd")

signal supply_found(index: int, supply_id: String)
signal supply_hunt_completed
signal cleanup_step_completed(step: int, cleanup_id: String)
signal finale_started
signal cleanup_completed

const MAGNIFIER_TEXTURE := "res://assets/opera/worlds/ui/magnifier.png"
const SPARKLE_TEXTURE := "res://assets/opera/worlds/props/fx_stolen_sparkle.png"
# These are the centers of the two painted storage baskets in the approved
# Bubble Bath room (ROOM_ITEMS art positions transformed by ART_TO_STAGE).
# Keep the hunt on existing room pixels; no cabinet card is drawn here.
const CABINET_POSITIONS: Array[Vector2] = [Vector2(138.0, 592.0),
	Vector2(1125.0, 592.0)]
const SUPPLY_DEFINITIONS: Array[Dictionary] = [
	{
		"id": "brush",
		"center": CABINET_POSITIONS[0],
		"hit_radius": 112.0,
	},
	{
		"id": "cleaner",
		"center": CABINET_POSITIONS[1],
		"hit_radius": 112.0,
	},
]
const MAX_SUPPLIES := 2
const MAGNIFIER_RADIUS := 74.0
const DRAG_TARGET_SIZE := Vector2(184.0, 184.0)
const MIN_DRAG_DISTANCE := 36.0
const DRAG_GUIDANCE_POSITION := Vector2(640.0, 360.0)

var m: ReefMain
var _supply_step: int = 0
var _found: Array[bool] = [false, false]
var _supply_nodes: Array[Node2D] = []
var _sparkle_nodes: Array[Sprite2D] = []
var _magnifier: Sprite2D = null
var _drag_surface: Control = null
var _pointer: Label = null
var _progress_pips: Array[ColorRect] = []
var _dragging: bool = false
var _drag_last: Vector2 = Vector2.ZERO
var _drag_distance: float = 0.0
var _busy: bool = false
var _hunt_completed: bool = false
var _handoff_ready: bool = false
var _cleaning_stage: DayOneBathroomCleaning = null
var _announcements_enabled: bool = true
var _pulse_time: float = 0.0
var _hotspot_layer: Control = null
var _hotspot_layer_was_visible: bool = false


class SupplyIcon extends Node2D:
	var supply_kind: String = "brush"

	func configure(kind: String) -> void:
		supply_kind = kind
		queue_redraw()

	func _draw() -> void:
		if supply_kind == "brush":
			draw_line(Vector2(-8.0, 42.0), Vector2(42.0, -24.0),
				Color(0.67, 0.38, 0.19, 1.0), 18.0)
			draw_line(Vector2(42.0, -24.0), Vector2(62.0, -46.0),
				Color(0.98, 0.73, 0.29, 1.0), 22.0)
			for offset: float in [-12.0, -4.0, 4.0, 12.0]:
				draw_line(Vector2(62.0 + offset, -52.0),
					Vector2(66.0 + offset, -72.0),
					Color(0.38, 0.77, 0.82, 1.0), 7.0)
		else:
			draw_circle(Vector2(0.0, 12.0), 48.0,
				Color(0.45, 0.86, 0.93, 1.0))
			draw_circle(Vector2(0.0, 12.0), 48.0,
				Color(0.12, 0.18, 0.38, 1.0), false, 8.0)
			draw_rect(Rect2(-27.0, -52.0, 54.0, 26.0),
				Color(0.83, 0.95, 0.93, 1.0), true)
			draw_rect(Rect2(-10.0, -74.0, 20.0, 23.0),
				Color(0.16, 0.20, 0.40, 1.0), true)
			draw_circle(Vector2(-14.0, 1.0), 7.0,
				Color(0.96, 0.98, 0.70, 0.95))


func setup(main: ReefMain, announcements_enabled: bool = true) -> void:
	m = main
	_announcements_enabled = announcements_enabled
	name = "DayOneBathroomCleanup"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 22
	_suspend_room_hotspots()
	_build_supply_icons()
	_build_drag_surface()
	_build_guidance()
	_supply_step = clampi(m.day_one_bathroom_supply_hunt_step, 0, MAX_SUPPLIES)
	_apply_restored_progress()
	set_process(true)
	if _supply_step >= MAX_SUPPLIES:
		_complete_supply_hunt()
	else:
		call_deferred("_announce_current_supply")


func teardown() -> void:
	set_process(false)
	if _cleaning_stage != null and is_instance_valid(_cleaning_stage):
		_cleaning_stage.teardown()
	_cleaning_stage = null
	if _hotspot_layer != null and is_instance_valid(_hotspot_layer):
		_hotspot_layer.visible = _hotspot_layer_was_visible
	_hotspot_layer = null
	if is_inside_tree():
		queue_free()
	else:
		free()


func audit_snapshot() -> Dictionary:
	var found_count: int = 0
	for found: bool in _found:
		if found:
			found_count += 1
	return {
		"supply_count": MAX_SUPPLIES,
		"found_count": found_count,
		"current_supply_step": _supply_step,
		"active_target_count": 1 if not _hunt_completed else 0,
		"minimum_touch_side": DRAG_TARGET_SIZE.x,
		"drag_target_size": DRAG_TARGET_SIZE,
		"minimum_drag_distance": MIN_DRAG_DISTANCE,
		"guidance_discloses_target": false,
		"magnifier_following_drag": _magnifier != null,
		"voice_guidance_configured": true,
		"announcements_enabled": _announcements_enabled,
		"has_visual_pointer": _pointer != null and _magnifier != null,
		"cabinet_target_count": _supply_nodes.size(),
		"supply_hunt_completed": _hunt_completed,
		"handoff_ready": _handoff_ready,
		"canvas_only": _all_canvas_children(self),
	}


func is_supply_hunt_complete() -> bool:
	return _hunt_completed


func is_handoff_ready() -> bool:
	return _handoff_ready


## Stable seam for the later sink/tub gesture owner. This method intentionally
## does not complete the room; it only acknowledges that both supplies exist.
func begin_cleaning_handoff() -> bool:
	if not _hunt_completed:
		return false
	_handoff_ready = true
	if _cleaning_stage == null or not is_instance_valid(_cleaning_stage):
		_cleaning_stage = DAY_ONE_BATHROOM_CLEANING.new() \
			as DayOneBathroomCleaning
		_cleaning_stage.cleanup_step_completed.connect(
			_on_cleaning_step_completed)
		_cleaning_stage.finale_started.connect(_on_cleaning_finale_started)
		_cleaning_stage.cleanup_completed.connect(_on_cleaning_completed)
		add_child(_cleaning_stage)
		_cleaning_stage.setup(m, _announcements_enabled)
	return true


func cleaning_audit_snapshot() -> Dictionary:
	if _cleaning_stage == null or not is_instance_valid(_cleaning_stage):
		return {"active": false, "handoff_ready": _handoff_ready}
	var snapshot: Dictionary = _cleaning_stage.audit_snapshot()
	snapshot["active"] = true
	snapshot["handoff_ready"] = _handoff_ready
	return snapshot


func probe_cleaning_sink_circle(points: Array[Vector2]) -> bool:
	return _cleaning_stage != null and is_instance_valid(_cleaning_stage) \
		and _cleaning_stage.probe_sink_circle(points)


func probe_cleaning_tub_strokes(points: Array[Vector2]) -> bool:
	return _cleaning_stage != null and is_instance_valid(_cleaning_stage) \
		and _cleaning_stage.probe_tub_strokes(points)


func probe_begin_drag(at: Vector2) -> bool:
	if _hunt_completed or _busy:
		return false
	_dragging = true
	_drag_last = at
	_drag_distance = 0.0
	_move_magnifier(at)
	return true


func probe_drag_to(at: Vector2) -> bool:
	if not _dragging or _hunt_completed or _busy:
		return false
	_drag_distance += _drag_last.distance_to(at)
	_drag_last = at
	_move_magnifier(at)
	return true


func probe_end_drag() -> void:
	_dragging = false


func probe_reveal_supply(index: int) -> bool:
	if _hunt_completed or _busy or index < 0 or index >= MAX_SUPPLIES:
		return false
	if index != _supply_step:
		return false
	if _found[index]:
		return false
	var center: Vector2 = SUPPLY_DEFINITIONS[index]["center"] as Vector2
	if not probe_begin_drag(center - Vector2(MIN_DRAG_DISTANCE, 0.0)):
		return false
	probe_drag_to(center)
	probe_end_drag()
	return _found[index]


func _process(delta: float) -> void:
	_pulse_time += maxf(delta, 0.0)
	if _magnifier != null and is_instance_valid(_magnifier) and _magnifier.visible:
		_magnifier.rotation = sin(_pulse_time * 2.8) * 0.035
		_magnifier.modulate.a = 0.90 + sin(_pulse_time * 4.0) * 0.08
	if _pointer != null and is_instance_valid(_pointer) and _pointer.visible:
		_pointer.rotation = sin(_pulse_time * 2.6) * 0.04


func _suspend_room_hotspots() -> void:
	_hotspot_layer = m.castle_room_item_hotspot_layer
	if _hotspot_layer == null or not is_instance_valid(_hotspot_layer):
		_hotspot_layer = null
		return
	_hotspot_layer_was_visible = _hotspot_layer.visible
	_hotspot_layer.visible = false


func _build_supply_icons() -> void:
	for index: int in range(MAX_SUPPLIES):
		var icon := SupplyIcon.new()
		icon.name = "HiddenSupply_%s" % String(SUPPLY_DEFINITIONS[index]["id"])
		icon.configure(String(SUPPLY_DEFINITIONS[index]["id"]))
		icon.position = SUPPLY_DEFINITIONS[index]["center"] as Vector2
		icon.z_index = 5
		icon.visible = false
		add_child(icon)
		_supply_nodes.append(icon)
		_found[index] = false


func _build_drag_surface() -> void:
	_drag_surface = Control.new()
	_drag_surface.name = "MagnifierDragSurface"
	_drag_surface.position = Vector2.ZERO
	_drag_surface.size = StorybookUI.CANVAS_SIZE
	_drag_surface.mouse_filter = Control.MOUSE_FILTER_STOP
	_drag_surface.z_index = 12
	_drag_surface.gui_input.connect(_on_drag_surface_input)
	add_child(_drag_surface)


func _build_guidance() -> void:
	_magnifier = Sprite2D.new()
	_magnifier.name = "DraggableMagnifyingGlass"
	_magnifier.texture = load(MAGNIFIER_TEXTURE) as Texture2D
	_magnifier.position = DRAG_GUIDANCE_POSITION
	_magnifier.scale = Vector2.ONE * 0.38
	_magnifier.z_index = 32
	_magnifier.set_meta("one_finger_drag", true)
	add_child(_magnifier)

	_pointer = Label.new()
	_pointer.name = "MagnifierPointer"
	_pointer.text = "👇"
	_pointer.size = Vector2(92.0, 92.0)
	_pointer.pivot_offset = _pointer.size * 0.5
	_pointer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pointer.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_pointer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pointer.z_index = 34
	StorybookUI.style_label(_pointer, 60, Color(1.0, 0.87, 0.32), 6)
	add_child(_pointer)

	var progress_row := HBoxContainer.new()
	progress_row.name = "SupplyProgress"
	progress_row.position = Vector2(574.0, 50.0)
	progress_row.size = Vector2(132.0, 34.0)
	progress_row.add_theme_constant_override("separation", 18)
	progress_row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	progress_row.z_index = 34
	add_child(progress_row)
	for index: int in range(MAX_SUPPLIES):
		var pip := ColorRect.new()
		pip.name = "SupplyPip%d" % index
		pip.custom_minimum_size = Vector2(48.0, 28.0)
		pip.color = Color(0.93, 0.84, 0.45, 0.42)
		pip.mouse_filter = Control.MOUSE_FILTER_IGNORE
		progress_row.add_child(pip)
		_progress_pips.append(pip)


func _apply_restored_progress() -> void:
	for index: int in range(MAX_SUPPLIES):
		_found[index] = index < _supply_step
		_supply_nodes[index].visible = false
	_update_progress_pips()
	_refresh_guidance()


func _refresh_guidance() -> void:
	var visible: bool = not _hunt_completed
	if _magnifier != null:
		_magnifier.visible = visible
	if _pointer != null:
		_pointer.visible = visible
	if not visible:
		return
	# Teach the one-finger action in open space. The next hidden basket remains
	# discoverable through the lens, but the pointer never marks its exact spot.
	_pointer.position = DRAG_GUIDANCE_POSITION + Vector2(0.0, -128.0) \
		- _pointer.size * 0.5


func _update_progress_pips() -> void:
	for index: int in range(_progress_pips.size()):
		_progress_pips[index].color = Color(0.98, 0.84, 0.35, 0.96) \
			if _found[index] else Color(0.93, 0.84, 0.45, 0.42)


func _on_drag_surface_input(event: InputEvent) -> void:
	if _hunt_completed or _busy:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_dragging = true
			_drag_last = touch.position
			_drag_distance = 0.0
			_move_magnifier(touch.position)
		else:
			_dragging = false
		get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag:
		if _dragging:
			var drag_position := (event as InputEventScreenDrag).position
			_drag_distance += _drag_last.distance_to(drag_position)
			_drag_last = drag_position
			_move_magnifier(drag_position)
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed:
			_dragging = true
			_drag_last = button.position
			_drag_distance = 0.0
			_move_magnifier(button.position)
		else:
			_dragging = false
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseMotion and _dragging:
		var motion_position := (event as InputEventMouseMotion).position
		_drag_distance += _drag_last.distance_to(motion_position)
		_drag_last = motion_position
		_move_magnifier(motion_position)
		get_viewport().set_input_as_handled()


func _move_magnifier(at: Vector2) -> void:
	if _magnifier == null or _busy or _hunt_completed:
		return
	_magnifier.position = at.clamp(Vector2(88.0, 88.0),
		StorybookUI.CANVAS_SIZE - Vector2(88.0, 88.0))
	var index: int = _supply_step
	if index < 0 or index >= MAX_SUPPLIES or _found[index]:
		return
	var definition: Dictionary = SUPPLY_DEFINITIONS[index]
	var target: Vector2 = definition["center"] as Vector2
	var hit_radius: float = float(definition["hit_radius"])
	if _drag_distance >= MIN_DRAG_DISTANCE \
			and _magnifier.position.distance_to(target) <= hit_radius + MAGNIFIER_RADIUS:
		_reveal_supply(index)


func _reveal_supply(index: int) -> void:
	if _busy or _hunt_completed or _found[index]:
		return
	_busy = true
	_found[index] = true
	_supply_step = clampi(index + 1, 0, MAX_SUPPLIES)
	_supply_nodes[index].visible = true
	_supply_nodes[index].scale = Vector2.ONE * 0.72
	_update_progress_pips()
	if m != null:
		m.day_one_record_bathroom_supply_step(_supply_step)
		if _announcements_enabled:
			m._ui_tap()
	supply_found.emit(index, String(SUPPLY_DEFINITIONS[index]["id"]))
	_spawn_sparkle(SUPPLY_DEFINITIONS[index]["center"] as Vector2)
	var reveal_tween: Tween = _supply_nodes[index].create_tween()
	reveal_tween.tween_property(_supply_nodes[index], "scale", Vector2.ONE, 0.16)
	reveal_tween.tween_interval(0.20)
	reveal_tween.tween_property(_supply_nodes[index], "modulate:a", 0.0, 0.18)
	reveal_tween.tween_callback(_finish_supply_reveal.bind(index))


func _finish_supply_reveal(index: int) -> void:
	_supply_nodes[index].visible = false
	_supply_nodes[index].modulate.a = 1.0
	_busy = false
	if _supply_step >= MAX_SUPPLIES:
		_complete_supply_hunt()
	else:
		_refresh_guidance()
		_announce_current_supply()


func _complete_supply_hunt() -> void:
	if _hunt_completed:
		return
	_hunt_completed = true
	_handoff_ready = true
	_busy = false
	_dragging = false
	_refresh_guidance()
	supply_hunt_completed.emit()
	if _announcements_enabled and m != null:
		m.show_msg("Roshan", "We found both cleaning supplies!", "win")
		m._say("roshan", "win", 0.6)
	begin_cleaning_handoff()


func _announce_current_supply() -> void:
	if not _announcements_enabled or m == null or _hunt_completed:
		return
	var supply_id: String = String(SUPPLY_DEFINITIONS[_supply_step]["id"])
	var message := "Drag the magnifying glass to find the brush!"
	if supply_id == "cleaner":
		message = "Great! Now find the cleaner in the other cabinet!"
	m.show_msg("Roshan", message, "talk")
	m._say("roshan", "talk", 0.8)


func _spawn_sparkle(center: Vector2) -> void:
	var texture: Texture2D = load(SPARKLE_TEXTURE) as Texture2D
	if texture == null:
		return
	var sparkle := Sprite2D.new()
	sparkle.name = "SupplySparkle"
	sparkle.texture = texture
	sparkle.position = center
	sparkle.scale = Vector2.ONE * 0.42
	sparkle.z_index = 40
	add_child(sparkle)
	_sparkle_nodes.append(sparkle)
	var tween: Tween = sparkle.create_tween().set_parallel(true)
	tween.tween_property(sparkle, "scale", Vector2.ONE * 0.82, 0.42)
	tween.tween_property(sparkle, "rotation", 0.35, 0.42)
	tween.tween_property(sparkle, "modulate:a", 0.0, 0.42)
	tween.chain().tween_callback(sparkle.queue_free)


func _all_canvas_children(node: Node) -> bool:
	for child: Node in node.get_children():
		if not child is CanvasItem or not _all_canvas_children(child):
			return false
	return true


func _on_cleaning_step_completed(step: int, cleanup_id: String) -> void:
	cleanup_step_completed.emit(step, cleanup_id)


func _on_cleaning_finale_started() -> void:
	finale_started.emit()


func _on_cleaning_completed() -> void:
	cleanup_completed.emit()
