class_name DayOneStuffieCleanup
extends Control
## Day One's two-step Stuffie Room rescue lesson.
##
## A child first taps a visible dust bunny to wake it, then crosses that bunny
## with one deliberate finger swipe to brush its dust away. The activity owns
## only transient Canvas2D presentation and touch state; the caller owns the
## restored two-bit mask through progress_changed().

signal progress_changed(mask: int)
signal completed

const CANVAS_SIZE := Vector2(1280.0, 720.0)
const TARGET_COUNT := 2
const COMPLETE_MASK := (1 << TARGET_COUNT) - 1
const SWIPE_MIN_LENGTH := 90.0
const SWIPE_BAND := 110.0
const TARGET_CENTERS: Array[Vector2] = [
	# The authored playroom pin positions are (189,109) and (323,109)
	# in the 1024x576 room art; ART_TO_STAGE=1.25 places their 512px
	# card centers at these 1280x720 canvas coordinates.
	Vector2(556.0, 456.0),
	Vector2(724.0, 456.0),
]
const TARGET_SIZES: Array[Vector2] = [
	Vector2(190.0, 170.0),
	Vector2(190.0, 170.0),
]
const TARGET_TEXTURES: Array[String] = [
	"res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_hop.png",
	"res://assets/castle/dirty_cleanup_2d/critters/dust_bunnies/dust_bunny_shell_hide.png",
]
const BRUSH_TEXTURE_PATH := \
	"res://assets/castle/day_one_art_studio/magic_cleaning_brush.png"
const FEEDBACK_LIFETIME := 0.42

var _progress_mask := 0
var _woken_mask := 0
var _show_cards := true
var _running := false
var _completed := false
var _touch_active := false
var _touch_id := -1
var _stroke_target := -1
var _stroke_from := Vector2.ZERO
var _stroke_last := Vector2.ZERO
var _stroke_length := 0.0
var _stroke_crossed := false
var _feedback_time := 0.0
var _feedback_position := Vector2.ZERO
var _feedback_good := false
var _elapsed := 0.0
var _bunnies: Array[Sprite2D] = []
var _brush: Sprite2D = null


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	set_meta("canvas_only", true)
	set_meta("no_fail", true)
	set_meta("one_finger", true)


func setup(initial_mask: int = 0, show_cards: bool = true) -> void:
	_clear_owned_nodes()
	_progress_mask = initial_mask & COMPLETE_MASK
	_woken_mask = 0
	_show_cards = show_cards
	_completed = _progress_mask == COMPLETE_MASK
	_running = false
	_elapsed = 0.0
	_feedback_time = 0.0
	_cancel_touch(false)
	if size.x <= 1.0 or size.y <= 1.0:
		size = CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_STOP
	_build_art()
	queue_redraw()


func start() -> void:
	_running = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(true)
	queue_redraw()


func stop() -> void:
	_running = false
	_cancel_touch(false)
	set_process(false)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_redraw()


func teardown() -> void:
	stop()
	_clear_owned_nodes()
	if is_inside_tree():
		queue_free()
	else:
		free()


func cancel_touch() -> void:
	_cancel_touch(true)


func audit_snapshot() -> Dictionary:
	return {
		"activity": "day_one_stuffie_cleanup",
		"running": _running,
		"progress_mask": _progress_mask,
		"mask": _progress_mask,
		"woken_mask": _woken_mask,
		"cleaned_mask": _progress_mask,
		"target_count": TARGET_COUNT,
		"woken_count": _count_woken(),
		"cleaned_count": _count_cleaned(),
		"completed": _completed,
		"target_sizes": TARGET_SIZES.duplicate(),
		"swipe_min_length": SWIPE_MIN_LENGTH,
		"swipe_band": SWIPE_BAND,
		"bunny_count": _bunnies.size(),
		"target_centers": TARGET_CENTERS.duplicate(),
		"show_cards": _show_cards,
		"brush_present": _brush != null and is_instance_valid(_brush),
		"touch_active": _touch_active,
		"touch_id": _touch_id,
		"canvas_only": true,
		"one_finger": true,
		"no_fail": true,
		"no_fail_state": true,
		"no_timer": true,
		"text_free": true,
		"live_input_required": true,
	}


## Probe helper: wake the next unresolved target through the same state gate
## used by a live tap. It never cleans a target by itself.
func probe_wake_next() -> bool:
	if not _running:
		start()
	var index := _next_unresolved_target()
	if index < 0:
		return false
	return _wake_target(index)


## Probe helper: perform the minimum valid crossed swipe on the next woken
## target. The explicit segment keeps the probe honest about swipe geometry.
func probe_swipe_next() -> bool:
	if not _running:
		start()
	var index := _next_woken_target()
	if index < 0:
		return false
	var center := TARGET_CENTERS[index]
	return _accept_swipe(index, center - Vector2(SWIPE_MIN_LENGTH * 0.5, 0.0),
		center + Vector2(SWIPE_MIN_LENGTH * 0.5, 0.0))


## Probe helper: complete one target only after its tap and swipe stages.
func probe_complete_current() -> bool:
	if not _running:
		start()
	var index := _next_unresolved_target()
	if index < 0:
		return false
	if not _wake_target(index):
		return false
	return probe_swipe_next()


func probe_wake_target(index: int) -> bool:
	if not _running:
		start()
	return _wake_target(index)


func probe_swipe_target(index: int) -> bool:
	if not _running:
		start()
	if index < 0 or index >= TARGET_COUNT or not _is_woken(index):
		return false
	var center := TARGET_CENTERS[index]
	return _accept_swipe(index, center - Vector2(SWIPE_MIN_LENGTH * 0.5, 0.0),
		center + Vector2(SWIPE_MIN_LENGTH * 0.5, 0.0))


func _process(delta: float) -> void:
	_elapsed += maxf(delta, 0.0)
	_feedback_time = maxf(0.0, _feedback_time - maxf(delta, 0.0))
	if _brush != null and is_instance_valid(_brush) and _brush.visible:
		if _touch_active:
			_brush.position = _stroke_last
			_brush.rotation = (_stroke_last - _stroke_from).angle() + 0.35
		else:
			var hint := _next_hint_target()
			if hint >= 0:
				_brush.position = TARGET_CENTERS[hint] + Vector2(84.0, -82.0)
				_brush.rotation = -0.52 + sin(_elapsed * 2.0) * 0.05
	queue_redraw()


func _draw() -> void:
	for index: int in range(TARGET_COUNT):
		var center := TARGET_CENTERS[index]
		var half := TARGET_SIZES[index] * 0.5
		var rect := Rect2(center - half, TARGET_SIZES[index])
		var phase := 0.5 + 0.5 * sin(_elapsed * 3.0 + float(index))
		if _is_cleaned(index):
			draw_arc(center, 82.0 + phase * 5.0, 0.0, TAU, 32,
				Color(0.48, 0.94, 0.78, 0.54), 7.0, true)
			for burst_index: int in range(4):
				var angle := TAU * float(burst_index) / 4.0
				draw_line(center + Vector2(cos(angle), sin(angle)) * 92.0,
					center + Vector2(cos(angle), sin(angle)) * 108.0,
					Color(1.0, 0.84, 0.38, 0.62), 4.0, true)
		elif _is_woken(index):
			draw_arc(center, 80.0 + phase * 6.0, 0.0, TAU, 32,
				Color(0.52, 0.90, 1.0, 0.80), 8.0, true)
			draw_arc(center, 60.0 + phase * 4.0, -0.7, 0.7, 16,
				Color(1.0, 0.84, 0.38, 0.80), 6.0, true)
		else:
			draw_arc(center, 82.0 + phase * 5.0, 0.0, TAU, 32,
				Color(1.0, 0.84, 0.38, 0.62), 7.0, true)
			# The arc and bobbing brush are the wordless “tap this” pointer.
			draw_line(center + Vector2(74.0, -70.0),
				center + Vector2(52.0, -46.0),
				Color(1.0, 0.94, 0.64, 0.78), 5.0, true)
		if _touch_active and _stroke_target == index:
			draw_arc(center, maxf(half.x, half.y) + 18.0, 0.0, TAU, 32,
				Color(0.92, 0.74, 1.0, 0.68), 5.0, true)
	if _feedback_time > 0.0:
		var ratio := 1.0 - _feedback_time / FEEDBACK_LIFETIME
		var alpha := (1.0 - ratio) * 0.75
		var color := Color(0.48, 0.94, 0.78, alpha) if _feedback_good \
			else Color(0.74, 0.70, 0.96, alpha)
		draw_circle(_feedback_position, 26.0 + ratio * 42.0, color, false, 6.0)


func _gui_input(event: InputEvent) -> void:
	if not _running or _completed:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_begin_touch(touch.position, touch.index)
		else:
			_end_touch(touch.position, touch.index)
		accept_event()
		return
	if event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_update_touch(drag.position, drag.index)
		accept_event()
		return
	if event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed:
			_begin_touch(button.position, 0)
		else:
			_end_touch(button.position, 0)
		accept_event()
		return
	if event is InputEventMouseMotion and Input.is_mouse_button_pressed(
			MOUSE_BUTTON_LEFT):
		_update_touch((event as InputEventMouseMotion).position, 0)
		accept_event()


func _begin_touch(point: Vector2, touch_id: int) -> void:
	if _touch_active:
		return
	var unresolved := _target_at(point, false)
	if unresolved >= 0:
		_wake_target(unresolved)
		# The waking tap is deliberately not also the swipe's first stroke.
		_cancel_touch(false)
		return
	var woken := _next_woken_target()
	if woken < 0:
		_feedback(false, point)
		return
	_touch_active = true
	_touch_id = touch_id
	_stroke_target = woken
	_stroke_from = point
	_stroke_last = point
	_stroke_length = 0.0
	_stroke_crossed = _target_rect(woken).has_point(point)
	_show_brush(point)


func _update_touch(point: Vector2, touch_id: int) -> void:
	if not _touch_active or touch_id != _touch_id:
		return
	var delta := point - _stroke_last
	_stroke_length += delta.length()
	_stroke_last = point
	_stroke_crossed = _stroke_crossed or _segment_hits_target(
		_stroke_target, _stroke_last - delta, point)
	_show_brush(point)
	if _stroke_length >= SWIPE_MIN_LENGTH and _stroke_crossed:
		_accept_swipe(_stroke_target, _stroke_from, _stroke_last)
		_cancel_touch(false)


func _end_touch(point: Vector2, touch_id: int) -> void:
	if not _touch_active or touch_id != _touch_id:
		return
	_update_touch(point, touch_id)
	if _touch_active:
		if _stroke_length >= SWIPE_MIN_LENGTH and _stroke_crossed:
			_accept_swipe(_stroke_target, _stroke_from, point)
		else:
			_feedback(false, point)
		_cancel_touch(false)


func _cancel_touch(rehint: bool) -> void:
	_touch_active = false
	_touch_id = -1
	_stroke_target = -1
	_stroke_from = Vector2.ZERO
	_stroke_last = Vector2.ZERO
	_stroke_length = 0.0
	_stroke_crossed = false
	if _brush != null and is_instance_valid(_brush):
		_brush.visible = rehint and _next_hint_target() >= 0


func _accept_swipe(index: int, from: Vector2, to: Vector2) -> bool:
	if index < 0 or index >= TARGET_COUNT or not _is_woken(index) \
			or _is_cleaned(index):
		return false
	if from.distance_to(to) < SWIPE_MIN_LENGTH \
			or not _segment_hits_target(index, from, to):
		_feedback(false, to)
		return false
	_progress_mask |= 1 << index
	_feedback(true, TARGET_CENTERS[index])
	if _bunnies.size() > index:
		_bunnies[index].visible = false
	progress_changed.emit(_progress_mask)
	if _progress_mask == COMPLETE_MASK:
		_completed = true
		_running = false
		set_process(false)
		completed.emit()
	queue_redraw()
	return true


func _wake_target(index: int) -> bool:
	if index < 0 or index >= TARGET_COUNT or _is_woken(index) \
			or _is_cleaned(index):
		return false
	_woken_mask |= 1 << index
	_feedback(true, TARGET_CENTERS[index])
	queue_redraw()
	return true


func _target_at(point: Vector2, include_woken: bool) -> int:
	for index: int in range(TARGET_COUNT):
		if _is_cleaned(index) or (not include_woken and _is_woken(index)):
			continue
		if _target_rect(index).has_point(point):
			return index
	return -1


func _target_rect(index: int) -> Rect2:
	if index < 0 or index >= TARGET_COUNT:
		return Rect2()
	return Rect2(TARGET_CENTERS[index] - TARGET_SIZES[index] * 0.5,
		TARGET_SIZES[index])


func _segment_hits_target(index: int, from: Vector2, to: Vector2) -> bool:
	if index < 0 or index >= TARGET_COUNT:
		return false
	var rect := _target_rect(index).grow(SWIPE_BAND * 0.5)
	var steps := maxi(1, int(ceil(from.distance_to(to) / 18.0)))
	for step: int in range(steps + 1):
		var point := from.lerp(to, float(step) / float(steps))
		if rect.has_point(point):
			return true
	return false


func _show_brush(point: Vector2) -> void:
	if _brush == null or not is_instance_valid(_brush):
		return
	_brush.visible = true
	_brush.position = point
	_brush.rotation = (_stroke_last - _stroke_from).angle() + 0.35


func _feedback(good: bool, position: Vector2) -> void:
	_feedback_good = good
	_feedback_position = position
	_feedback_time = FEEDBACK_LIFETIME
	queue_redraw()


func _build_art() -> void:
	if _show_cards:
		for index: int in range(TARGET_COUNT):
			var bunny := Sprite2D.new()
			bunny.name = "StuffieCleanupBunny%d" % index
			bunny.texture = load(TARGET_TEXTURES[index]) as Texture2D
			bunny.position = TARGET_CENTERS[index]
			bunny.z_index = 3
			bunny.flip_h = index == 1
			_fit_sprite(bunny, TARGET_SIZES[index] * 0.76)
			bunny.set_meta("target_index", index)
			add_child(bunny)
			_bunnies.append(bunny)
	_brush = Sprite2D.new()
	_brush.name = "StuffieCleanupMagicBrush"
	_brush.texture = load(BRUSH_TEXTURE_PATH) as Texture2D
	_brush.z_index = 8
	_fit_sprite(_brush, Vector2(132.0, 112.0))
	_brush.visible = not _completed
	add_child(_brush)
	for index: int in range(TARGET_COUNT):
		if _is_cleaned(index) and index < _bunnies.size():
			_bunnies[index].visible = false


func _clear_owned_nodes() -> void:
	for bunny: Sprite2D in _bunnies:
		if bunny != null and is_instance_valid(bunny):
			bunny.queue_free()
	if _brush != null and is_instance_valid(_brush):
		_brush.queue_free()
	_bunnies.clear()
	_brush = null


func _fit_sprite(sprite: Sprite2D, max_size: Vector2) -> void:
	if sprite.texture == null:
		return
	var source := sprite.texture.get_size()
	var fit := minf(max_size.x / maxf(source.x, 1.0),
		max_size.y / maxf(source.y, 1.0))
	sprite.scale = Vector2.ONE * fit


func _is_woken(index: int) -> bool:
	return index >= 0 and index < TARGET_COUNT \
		and (_woken_mask & (1 << index)) != 0


func _is_cleaned(index: int) -> bool:
	return index >= 0 and index < TARGET_COUNT \
		and (_progress_mask & (1 << index)) != 0


func _next_unresolved_target() -> int:
	for index: int in range(TARGET_COUNT):
		if not _is_woken(index) and not _is_cleaned(index):
			return index
	return -1


func _next_woken_target() -> int:
	for index: int in range(TARGET_COUNT):
		if _is_woken(index) and not _is_cleaned(index):
			return index
	return -1


func _next_hint_target() -> int:
	var woken := _next_woken_target()
	return woken if woken >= 0 else _next_unresolved_target()


func _count_woken() -> int:
	var count := 0
	for index: int in range(TARGET_COUNT):
		if _is_woken(index):
			count += 1
	return count


func _count_cleaned() -> int:
	var count := 0
	for index: int in range(TARGET_COUNT):
		if _is_cleaned(index):
			count += 1
	return count
