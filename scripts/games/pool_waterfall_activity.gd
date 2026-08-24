class_name PoolWaterfallActivity
extends Control
## Wordless, one-finger waterfall cleaning activity for the Day One pool.
##
## The live room supplies the clean waterfall underneath this surface. This
## node owns only the three dirty, independently washable strips and the
## child-readable scrubber affordance. It never starts a water animation or
## replaces the fixture's approved clean artwork.

signal progress_changed(mask: int)
signal completed

const DIRTY_TEXTURE_PATH := \
	"res://assets/castle/day_one_pool/activities/waterfall_clogged_original_match.png"
const SCRUBBER_TEXTURE_PATH := \
	"res://assets/castle/day_one_pool/activities/waterfall_scrubber.png"
const LANE_COUNT := 3
const COMPLETE_MASK := 0b111
const TAP_ASSIST := 0.22
const DRAG_START_DISTANCE := 12.0
const MIN_DRAG_DISTANCE := 4.0
const LANE_GUTTER := 24.0
const TOOL_SIZE := 72.0
const SCRUBBER_CONTACT_OFFSET := Vector2(22.0, 22.0)

var fixture_center := Vector2.ZERO
var fixture_size := Vector2.ZERO
var _fixture_rect := Rect2()
var _dirty_texture: Texture2D = null
var _scrubber_texture: Texture2D = null
var _slice_nodes: Array[Sprite2D] = []
var _slice_base_scales: Array[Vector2] = []
var _lane_progress: Array[float] = [0.0, 0.0, 0.0]
var _lane_revealing: Array[bool] = [false, false, false]
var _clear_mask: int = 0
var _active := false
var _completed_emitted := false
var _touch_active := false
var _touch_id := -1
var _touch_lane := -1
var _touch_start := Vector2.ZERO
var _touch_last := Vector2.ZERO
var _touch_travel := 0.0
var _hint_lane := 0
var _pulse_time := 0.0
var _scrubber: Sprite2D = null
var _wash_overlay: Control = null


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(false)
	set_meta("canvas_only", true)
	set_meta("no_fail", true)


func setup(fixture_center: Vector2, fixture_size: Vector2,
		initial_mask: int = 0) -> void:
	self.fixture_center = fixture_center
	self.fixture_size = Vector2(maxf(1.0, fixture_size.x), maxf(1.0, fixture_size.y))
	_fixture_rect = Rect2(self.fixture_center - self.fixture_size * 0.5, self.fixture_size)
	_clear_mask = initial_mask & COMPLETE_MASK
	_completed_emitted = false
	_active = false
	_pulse_time = 0.0
	_lane_progress = [0.0, 0.0, 0.0]
	_lane_revealing = [false, false, false]
	_hint_lane = _first_uncleared_lane()
	_cancel_touch(false)
	_free_owned_nodes()
	_dirty_texture = load(DIRTY_TEXTURE_PATH) as Texture2D
	_scrubber_texture = load(SCRUBBER_TEXTURE_PATH) as Texture2D
	_build_dirty_slices()
	_build_wash_overlay()
	_build_scrubber()
	_queue_progress_signal()
	queue_redraw()


func start() -> void:
	_active = true
	mouse_filter = Control.MOUSE_FILTER_STOP
	_pulse_time = 0.0
	_hint_lane = _first_uncleared_lane()
	set_process(true)
	if _clear_mask == COMPLETE_MASK:
		_emit_completed_once()
	queue_redraw()


func stop() -> void:
	_active = false
	_cancel_touch(false)
	set_process(false)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_redraw()


func cancel_touch() -> void:
	_cancel_touch(true)


func probe_clear_next_lane() -> bool:
	if not _active:
		start()
	var lane := _first_uncleared_lane()
	if lane < 0:
		_emit_completed_once()
		return false
	_set_lane_progress(lane, 1.0)
	_hint_lane = _first_uncleared_lane()
	return true


func audit_snapshot() -> Dictionary:
	return {
		"canvas_only": true,
		"no_fail": true,
		"active": _active,
		"fixture_center": fixture_center,
		"fixture_size": fixture_size,
		"fixture_rect": _fixture_rect,
		"lane_count": LANE_COUNT,
		"clear_mask": _clear_mask,
		"lane_progress": _lane_progress.duplicate(),
		"lane_revealing": _lane_revealing.duplicate(),
		"hint_lane": _hint_lane,
		"touch_active": _touch_active,
		"completed": _completed_emitted,
		"dirty_texture_path": DIRTY_TEXTURE_PATH,
		"scrubber_texture_path": SCRUBBER_TEXTURE_PATH,
		"dirty_texture_loaded": _dirty_texture != null,
		"scrubber_texture_loaded": _scrubber_texture != null,
		"dirty_slices_aligned": _slice_nodes.size() == LANE_COUNT
			and _slice_base_scales.size() == LANE_COUNT,
		"wash_feedback_above_grime": _wash_overlay != null
			and is_instance_valid(_wash_overlay) and _wash_overlay.z_index > 2,
		"animated_flow_stopped": true,
	}


func _process(delta: float) -> void:
	if not _active:
		return
	_pulse_time += maxf(delta, 0.0)
	if _wash_overlay != null and is_instance_valid(_wash_overlay):
		_wash_overlay.queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if not _active:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_begin_touch(touch.position, touch.index)
		else:
			_end_touch(touch.position, touch.index)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_update_touch(drag.position, drag.index)
		accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index != MOUSE_BUTTON_LEFT:
			return
		if button.pressed:
			_begin_touch(button.position, 0)
		else:
			_end_touch(button.position, 0)
		accept_event()
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		_update_touch((event as InputEventMouseMotion).position, 0)
		accept_event()


func _begin_touch(point: Vector2, touch_id: int) -> void:
	_cancel_touch(false)
	_touch_active = true
	_touch_id = touch_id
	_touch_lane = _lane_at(point)
	_touch_start = point
	_touch_last = point
	_touch_travel = 0.0
	if _touch_lane >= 0:
		_hint_lane = _touch_lane
		_show_scrubber(point)
	else:
		_hint_lane = _first_uncleared_lane()
		_hide_scrubber()
	queue_redraw()


func _update_touch(point: Vector2, touch_id: int) -> void:
	if not _touch_active or touch_id != _touch_id:
		return
	var delta := point - _touch_last
	_touch_last = point
	if _touch_lane < 0:
		queue_redraw()
		return
	_show_scrubber(point)
	if delta.y > 0.0:
		_touch_travel = maxf(_touch_travel, point.y - _touch_start.y)
		var track_length := maxf(fixture_size.y * 0.78, 1.0)
		var drag_amount := _touch_travel / track_length
		# A pass can begin anywhere on the broad strip; a downward stroke to
		# the lower half still gives visible, friendly progress.
		var absolute_amount := clampf(
			(point.y - _fixture_rect.position.y) / maxf(fixture_size.y, 1.0),
			0.0, 1.0) * 0.78
		_advance_lane(_touch_lane, maxf(drag_amount, absolute_amount * 0.52))
	queue_redraw()


func _end_touch(point: Vector2, touch_id: int) -> void:
	if not _touch_active or touch_id != _touch_id:
		return
	if _touch_lane >= 0:
		var moved_down := point.y - _touch_start.y
		if moved_down < DRAG_START_DISTANCE:
			# A tap is a gentle snap-assist, never a penalty or a reset.
			_advance_lane(_touch_lane, TAP_ASSIST)
		elif _touch_travel < MIN_DRAG_DISTANCE:
			_hint_lane = _touch_lane
	else:
		_hint_lane = _first_uncleared_lane()
	_cancel_touch(false)
	_hint_lane = _first_uncleared_lane() if _hint_lane < 0 \
		else _hint_lane
	queue_redraw()


func _cancel_touch(rehint: bool) -> void:
	_touch_active = false
	_touch_id = -1
	_touch_lane = -1
	_touch_start = Vector2.ZERO
	_touch_last = Vector2.ZERO
	_touch_travel = 0.0
	_hide_scrubber()
	if rehint:
		_hint_lane = _first_uncleared_lane()
	queue_redraw()


func _build_dirty_slices() -> void:
	if _dirty_texture == null:
		return
	var source_size := _dirty_texture.get_size()
	var source_lane_width := maxf(source_size.x / float(LANE_COUNT), 1.0)
	var lane_size := Vector2(fixture_size.x / float(LANE_COUNT), fixture_size.y)
	for lane in range(LANE_COUNT):
		var sprite := Sprite2D.new()
		sprite.name = "DirtyWaterfallLane%d" % lane
		sprite.texture = _dirty_texture
		sprite.region_enabled = true
		sprite.region_rect = Rect2(
			Vector2(source_lane_width * float(lane), 0.0),
			Vector2(source_lane_width, source_size.y))
		sprite.position = _fixture_rect.position + Vector2(
			lane_size.x * (float(lane) + 0.5), fixture_size.y * 0.5)
		sprite.scale = Vector2(
			lane_size.x / source_lane_width,
			fixture_size.y / maxf(source_size.y, 1.0))
		sprite.z_index = 2
		sprite.modulate = Color(0.88, 0.91, 0.78, 0.98)
		_slice_nodes.append(sprite)
		_slice_base_scales.append(sprite.scale)
		add_child(sprite)
		if (_clear_mask & (1 << lane)) != 0:
			sprite.visible = false
			_lane_progress[lane] = 1.0


func _build_wash_overlay() -> void:
	_wash_overlay = Control.new()
	_wash_overlay.name = "WaterfallContactAndReveal"
	_wash_overlay.position = Vector2.ZERO
	_wash_overlay.size = size
	_wash_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_wash_overlay.z_index = 4
	_wash_overlay.draw.connect(_draw_wash_overlay)
	add_child(_wash_overlay)


func _build_scrubber() -> void:
	_scrubber = Sprite2D.new()
	_scrubber.name = "WaterfallScrubberTool"
	_scrubber.texture = _scrubber_texture
	_scrubber.z_index = 12
	_scrubber.modulate = Color(0.86, 0.91, 0.88, 0.98)
	_scrubber.visible = false
	if _scrubber_texture != null:
		var source_size := _scrubber_texture.get_size()
		var fit := TOOL_SIZE / maxf(maxf(source_size.x, source_size.y), 1.0)
		_scrubber.scale = Vector2.ONE * fit
	add_child(_scrubber)


func _free_owned_nodes() -> void:
	for sprite: Sprite2D in _slice_nodes:
		if sprite != null and is_instance_valid(sprite):
			sprite.queue_free()
	_slice_nodes.clear()
	_slice_base_scales.clear()
	if _scrubber != null and is_instance_valid(_scrubber):
		_scrubber.queue_free()
	_scrubber = null
	if _wash_overlay != null and is_instance_valid(_wash_overlay):
		_wash_overlay.queue_free()
	_wash_overlay = null


func _show_scrubber(point: Vector2) -> void:
	if _scrubber == null or not is_instance_valid(_scrubber):
		return
	# Register the broad blade to the touch instead of floating the cutout's
	# center over the grime.
	_scrubber.position = point + SCRUBBER_CONTACT_OFFSET
	_scrubber.rotation = clampf(
		(point.y - _touch_start.y) * 0.0015, -0.18, 0.18)
	_scrubber.visible = true


func _hide_scrubber() -> void:
	if _scrubber != null and is_instance_valid(_scrubber):
		_scrubber.visible = false


func _lane_at(point: Vector2) -> int:
	if not _fixture_rect.grow(LANE_GUTTER).has_point(point):
		return -1
	var lane_width := fixture_size.x / float(LANE_COUNT)
	return clampi(int(floor((point.x - _fixture_rect.position.x) / lane_width)), 0, LANE_COUNT - 1)


func _first_uncleared_lane() -> int:
	for lane in range(LANE_COUNT):
		if (_clear_mask & (1 << lane)) == 0:
			return lane
	return -1


func _advance_lane(lane: int, amount: float) -> void:
	if lane < 0 or lane >= LANE_COUNT or (_clear_mask & (1 << lane)) != 0:
		return
	var before := _lane_progress[lane]
	var after := clampf(maxf(before, before + maxf(amount, 0.0)), 0.0, 1.0)
	if is_equal_approx(before, after):
		_hint_lane = lane
		return
	_set_lane_progress(lane, after)


func _set_lane_progress(lane: int, value: float) -> void:
	if lane < 0 or lane >= LANE_COUNT:
		return
	var before := _lane_progress[lane]
	var after := clampf(maxf(before, value), 0.0, 1.0)
	_lane_progress[lane] = after
	if after >= 1.0:
		_clear_mask |= 1 << lane
		_start_lane_reveal(lane)
	_hint_lane = _first_uncleared_lane()
	if not is_equal_approx(before, after):
		progress_changed.emit(_clear_mask)
	if _clear_mask == COMPLETE_MASK:
		_emit_completed_once()
	queue_redraw()


func _start_lane_reveal(lane: int) -> void:
	if lane < 0 or lane >= _slice_nodes.size() or _lane_revealing[lane]:
		return
	_lane_revealing[lane] = true
	var sprite := _slice_nodes[lane]
	if sprite == null or not is_instance_valid(sprite):
		_lane_revealing[lane] = false
		return
	var tween := sprite.create_tween().set_parallel(true)
	tween.tween_property(sprite, "modulate:a", 0.0, 0.34)
	tween.tween_property(sprite, "scale", _slice_base_scales[lane] * 1.035, 0.34) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	tween.chain().tween_callback(Callable(self, "_finish_lane_reveal").bind(lane))


func _finish_lane_reveal(lane: int) -> void:
	if lane < 0 or lane >= _slice_nodes.size():
		return
	var sprite := _slice_nodes[lane]
	if sprite != null and is_instance_valid(sprite):
		sprite.visible = false
	_lane_revealing[lane] = false
	queue_redraw()


func _emit_completed_once() -> void:
	if _completed_emitted:
		return
	_completed_emitted = true
	completed.emit()


func _queue_progress_signal() -> void:
	# Restored lanes are already clean; expose their mask to the owner without
	# starting animation or requiring a frame of play.
	progress_changed.emit(_clear_mask)


func _draw_wash_overlay() -> void:
	if _wash_overlay == null or not is_instance_valid(_wash_overlay) \
			or fixture_size.x <= 1.0 or fixture_size.y <= 1.0:
		return
	var lane_width := fixture_size.x / float(LANE_COUNT)
	for lane in range(LANE_COUNT):
		var lane_rect := Rect2(
			_fixture_rect.position + Vector2(lane_width * float(lane), 0.0),
			Vector2(lane_width, fixture_size.y))
		var complete := (_clear_mask & (1 << lane)) != 0
		if not complete:
			var progress := _lane_progress[lane]
			var wash_rect := Rect2(
				Vector2(lane_rect.position.x + 3.0,
					lane_rect.end.y - fixture_size.y * progress),
				Vector2(lane_rect.size.x - 6.0, fixture_size.y * progress))
			if progress > 0.0:
				_wash_overlay.draw_rect(
					wash_rect, Color(0.50, 0.90, 0.82, 0.26), true)
			var edge_alpha := 0.14 if lane != _hint_lane else 0.32
			_wash_overlay.draw_line(lane_rect.position,
				Vector2(lane_rect.position.x, lane_rect.end.y),
				Color(0.70, 0.96, 1.0, edge_alpha), 2.0)
			if lane == _hint_lane and _active:
				_draw_lane_hint(lane_rect, _pulse_time)
		if lane < LANE_COUNT - 1:
			_wash_overlay.draw_line(
				Vector2(lane_rect.end.x, lane_rect.position.y + 8.0),
				Vector2(lane_rect.end.x, lane_rect.end.y - 8.0),
				Color(0.46, 0.87, 0.92, 0.12), 2.0)
	if _touch_active and _touch_lane >= 0:
		_wash_overlay.draw_set_transform(_touch_last, 0.0, Vector2(1.0, 0.30))
		_wash_overlay.draw_arc(Vector2.ZERO,
			30.0 + sin(_pulse_time * 5.0) * 3.0, 0.10, PI - 0.10, 18,
			Color(0.78, 0.96, 0.90, 0.26), 3.0, true)
		_wash_overlay.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_lane_hint(lane_rect: Rect2, phase: float) -> void:
	var pulse := 1.0 + sin(phase * 4.2) * 0.10
	var x := lane_rect.get_center().x
	var top := lane_rect.position.y + 34.0
	var arrow_color := Color(1.0, 0.89, 0.34, 0.78)
	_wash_overlay.draw_circle(Vector2(x, top), 8.0 * pulse, arrow_color)
	for index in range(3):
		var y := top + 27.0 + float(index) * minf(48.0, fixture_size.y * 0.16)
		var width := 13.0 * pulse
		_wash_overlay.draw_line(
			Vector2(x - width, y), Vector2(x, y + 12.0), arrow_color, 4.0)
		_wash_overlay.draw_line(
			Vector2(x + width, y), Vector2(x, y + 12.0), arrow_color, 4.0)
