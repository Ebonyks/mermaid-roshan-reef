class_name OperaGestureSurface
extends Control
## One-finger input surface shared by all thirteen 2D Opera career worlds.
##
## The surrounding world chooses a gesture mode; this node turns mouse and
## touchscreen input into normalized progress without owning career state.
## Incorrect timing/choices report lower quality but still make a little
## progress, so there is no dead end for a non-reader.

signal gesture(kind: String, amount: float, quality: float)

var mode := "tap"
var accent := Color(1.0, 0.62, 0.8)
var target_choice := 1
var choice_count := 3
var timing_position := 0.0
var timing_zone := Vector2(0.30, 0.72)
var held := false
var pointer_pos := Vector2.ZERO
var previous_pos := Vector2.ZERO
var previous_angle := 0.0
var have_angle := false
var _last_spin := 0.0
## Friendly imp-scuffle targets for the "bop" combat beats. Each entry:
## {home: Vector2, pos: Vector2, r: float, hp: int, captain: bool, popped: bool}
var bop_targets: Array = []
var bop_texture: Texture2D = null
var bop_captain_texture: Texture2D = null
var last_bop_pos := Vector2.ZERO


## Ghost-finger demo: until the child touches, a glowing dot acts out the
## expected gesture so no phase ever needs reading to understand.
var demo_active := true
var demo_t := 0.0
var _demo_redraw := 0.0
var input_started := false
var feedback_t := 0.0
var feedback_positive := false
var feedback_position := 0.0
var feedback_anchor := Vector2.ZERO
var completion_accepted := false
## Choice lanes flash gold briefly, then dim so the pick uses recognition
## memory instead of tap-the-highlight; wrong picks kindly re-flash.
var choice_flash := 1.4
## Directional hint for swipe phases (DUCK draws a downward arrow).
var swipe_dir := Vector2.RIGHT
## Tap phases aim at a moving point that leaves a happy mark per hit.
var tap_point := Vector2.ZERO
var tap_marks: Array = []
var tap_relocate_pending := false
## Diegetic scene painted behind the affordance (nursery basin/bottle/cribs).
var visual_context := ""
var nursery_textures: Array[Texture2D] = []
var widget_template := ""
var widget_fill := 0.0
var widget_backdrop: Texture2D = null
var widget_mover: Texture2D = null
var widget_overlay: Texture2D = null
var widget_stamp: Texture2D = null
var widget_shared: Texture2D = null
var crank_rotation := 0.0
## Trickle-by-assist (house pattern from fetch/melody/dolls): wrong input
## always celebrates but pays ~nothing, and repeat misses inside the
## cooldown pay zero — correct play must strictly beat mashing.
const MISS_COOLDOWN := {"tap": 0.5, "choice": 0.6, "timing": 1.0}
var miss_cool := 0.0
## Swipe honesty: per-event travel cap plus a refilling per-second budget
## so scrubbing cannot trivialize goals; direction gates only when the
## phase declares one (DUCK down, BEDTIME down).
var swipe_budget := 1.3
var swipe_require_dir := false


func _miss_pay() -> float:
	# first miss trickles a crumb; repeats inside the cooldown pay nothing
	if miss_cool > 0.0:
		return 0.0
	miss_cool = float(MISS_COOLDOWN.get(mode, 0.5))
	return 0.05


func configure(next_mode: String, next_accent: Color, choice: int = 1, next_context: String = "") -> void:
	mode = next_mode
	accent = next_accent
	target_choice = choice
	visual_context = next_context
	widget_fill = 0.0
	completion_accepted = false
	feedback_t = 0.0
	feedback_positive = false
	feedback_position = 0.0
	feedback_anchor = Vector2.ZERO
	input_started = false
	crank_rotation = 0.0
	_load_widget_set()
	if visual_context.ends_with("_nursery") and nursery_textures.is_empty():
		for index in range(3):
			var path := "res://assets/opera/worlds/nursery/baby_%d.png" % index
			var texture := load(path) as Texture2D
			if texture != null:
				nursery_textures.append(texture)
	held = false
	have_angle = false
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.4
	miss_cool = 0.0
	swipe_budget = 1.3
	swipe_require_dir = false
	swipe_dir = Vector2.RIGHT
	tap_marks = []
	tap_point = size * 0.5
	tap_relocate_pending = false
	if next_mode != "bop":
		bop_targets = []
	queue_redraw()


func _load_widget_texture(path: String) -> Texture2D:
	return load(path) as Texture2D if ResourceLoader.exists(path) else null


func _load_widget_set() -> void:
	widget_template = visual_context.get_slice("_", 0) if not visual_context.is_empty() else ""
	widget_backdrop = null
	widget_mover = null
	widget_overlay = null
	widget_stamp = null
	widget_shared = null
	if widget_template.is_empty():
		return
	var prefix := "res://assets/opera/worlds/widgets/widget_%s" % visual_context
	widget_backdrop = _load_widget_texture("%s.png" % prefix)
	match widget_template:
		"gauge":
			widget_mover = _load_widget_texture("res://assets/opera/worlds/widgets/widget_gauge_shared_needle.png")
			widget_overlay = _load_widget_texture("%s_success.png" % prefix)
		"track":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_track_shared_hit.png")
		"pour":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_overlay = _load_widget_texture("%s_fill.png" % prefix)
		"basin":
			widget_overlay = _load_widget_texture("%s_bubbles.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_basin_shared_shine.png")
		"charge":
			widget_mover = _load_widget_texture("%s_glow.png" % prefix)
			widget_overlay = _load_widget_texture("%s_full.png" % prefix)
		"crank":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_overlay = _load_widget_texture("%s_progress.png" % prefix)
		"trace":
			widget_overlay = _load_widget_texture("%s_lit.png" % prefix)
		"push":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			var down := visual_context.ends_with("_boxer") or visual_context.ends_with("_nursery")
			var shared_name := "arrow_down" if down else "arrow_lr"
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_push_shared_%s.png" % shared_name)
		"target":
			widget_mover = _load_widget_texture("%s_mover.png" % prefix)
			widget_stamp = _load_widget_texture("%s_mark.png" % prefix)
			widget_overlay = _load_widget_texture("%s_success.png" % prefix)
		"lanes":
			widget_mover = _load_widget_texture("%s_lit.png" % prefix)
			widget_shared = _load_widget_texture("res://assets/opera/worlds/widgets/widget_lanes_shared_pick.png")


func note_input() -> void:
	input_started = true
	demo_active = false
	queue_redraw()


func note_result(accepted: bool) -> void:
	feedback_positive = accepted
	feedback_t = 0.32
	queue_redraw()


func accept_completion() -> void:
	completion_accepted = true
	feedback_positive = true
	feedback_t = maxf(feedback_t, 0.32)
	queue_redraw()


func restart_demo() -> void:
	demo_active = true
	demo_t = 0.0
	choice_flash = 1.2


func reflash_choice() -> void:
	choice_flash = 1.2
	queue_redraw()


func _process(delta: float) -> void:
	if miss_cool > 0.0:
		miss_cool = maxf(0.0, miss_cool - delta)
	swipe_budget = minf(1.3, swipe_budget + delta * 1.3)
	if feedback_t > 0.0:
		feedback_t = maxf(0.0, feedback_t - delta)
		queue_redraw()
	if choice_flash > 0.0 and mode == "choice":
		choice_flash -= delta
		if choice_flash <= 0.0:
			queue_redraw()
	if not demo_active:
		return
	demo_t += delta
	_demo_redraw += delta
	if _demo_redraw >= 0.05:
		_demo_redraw = 0.0
		queue_redraw()


func set_bop_targets(targets: Array) -> void:
	bop_targets = targets
	queue_redraw()


func bop_remaining() -> int:
	var left := 0
	for target: Dictionary in bop_targets:
		if not bool(target.get("popped", false)):
			left += 1
	return left


func set_timing_position(value: float) -> void:
	timing_position = clampf(value, 0.0, 1.0)
	if mode == "timing":
		queue_redraw()


func set_fill(value: float) -> void:
	widget_fill = clampf(value, 0.0, 1.0)
	if widget_backdrop != null:
		queue_redraw()


func _press(at: Vector2) -> void:
	note_input()
	held = true
	pointer_pos = at
	previous_pos = at
	previous_angle = (at - size * 0.5).angle()
	have_angle = true
	_last_spin = 0.0
	feedback_anchor = at
	feedback_position = timing_position
	match mode:
		"tap":
			if at.distance_to(tap_point) <= 92.0:
				tap_marks.append(tap_point)
				tap_relocate_pending = true
				gesture.emit("tap", 1.0, 1.0)
			else:
				# near-misses still sparkle, but mashing pays no wage
				gesture.emit("tap", _miss_pay(), 0.4)
		"choice":
			var lane := clampi(int(at.x / maxf(1.0, size.x) * float(choice_count)), 0, choice_count - 1)
			if lane == target_choice:
				gesture.emit("choice", 1.0, 1.0)
			else:
				gesture.emit("choice", _miss_pay(), 0.0)
		"timing":
			if timing_position >= timing_zone.x and timing_position <= timing_zone.y:
				gesture.emit("timing", 1.0, 1.0)
			else:
				gesture.emit("timing", _miss_pay(), 0.32)
		"bop":
			_bop_press(at)
		"hold":
			# a tap on the hold circle answers with a small warm trickle
			gesture.emit("hold", 0.06, 0.6)
		"swipe", "circle":
			gesture.emit(mode, 0.05, 0.6)
	queue_redraw()


func _relocate_tap_point() -> void:
	var n := tap_marks.size()
	tap_point = Vector2(
		size.x * 0.5 + sin(float(n) * 2.4 + 0.9) * size.x * 0.3,
		size.y * 0.5 + cos(float(n) * 1.7 + 0.4) * size.y * 0.26
	)


func _bop_press(at: Vector2) -> void:
	for target: Dictionary in bop_targets:
		if bool(target.get("popped", false)):
			continue
		var pos: Vector2 = target.get("pos", Vector2.ZERO)
		var reach := float(target.get("r", 44.0)) * 1.45
		if at.distance_to(pos) <= reach:
			target["hp"] = int(target.get("hp", 1)) - 1
			last_bop_pos = pos
			if int(target["hp"]) <= 0:
				target["popped"] = true
			gesture.emit("bop", 1.0, 1.0)
			return
	# a stray tap fizzles kindly and still trickles a little progress
	last_bop_pos = at
	gesture.emit("bop", 0.12, 0.2)


func _drag(at: Vector2) -> void:
	note_input()
	pointer_pos = at
	var distance := at.distance_to(previous_pos)
	if mode == "swipe" and distance > 0.0:
		var travel := minf(distance, 34.0) / 150.0
		travel = minf(travel, swipe_budget)
		if travel > 0.0:
			swipe_budget -= travel
			var aligned := 1.0
			if swipe_require_dir:
				aligned = maxf(0.0, (at - previous_pos).normalized().dot(swipe_dir))
			if aligned >= 0.35:
				gesture.emit("swipe", travel, 1.0)
			else:
				# wrong-direction wiggles fizzle kindly, tiny trickle
				gesture.emit("swipe", travel * 0.2, 0.4)
	elif mode == "circle":
		var center := size * 0.5
		var radius := at.distance_to(center)
		if radius > minf(size.x, size.y) * 0.13:
			var angle := (at - center).angle()
			if have_angle:
				var change := wrapf(angle - previous_angle, -PI, PI)
				crank_rotation = angle
				# straight-line scrubs cross the center as big sign-flipping
				# jumps; honest circling is small same-sign steps
				if absf(change) <= 0.9 and signf(change) == signf(_last_spin) and absf(_last_spin) > 0.0001:
					gesture.emit("circle", absf(change) / TAU, 1.0)
				_last_spin = change
			previous_angle = angle
			have_angle = true
	previous_pos = at
	queue_redraw()


func _release(at: Vector2) -> void:
	held = false
	pointer_pos = at
	have_angle = false
	if tap_relocate_pending:
		tap_relocate_pending = false
		_relocate_tap_point()
	queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			_press(touch.position)
		else:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		_drag(drag.position)
		accept_event()
	elif event is InputEventMouseButton and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT:
		var button := event as InputEventMouseButton
		if button.device == InputEvent.DEVICE_ID_EMULATION:
			return  # already handled as the touch event on tablets
		if button.pressed:
			_press(button.position)
		else:
			_release(button.position)
		accept_event()
	elif event is InputEventMouseMotion and held:
		if (event as InputEventMouseMotion).device == InputEvent.DEVICE_ID_EMULATION:
			return
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _draw() -> void:
	var panel := Rect2(Vector2.ZERO, size)
	# light paper inset window per the StorybookUI language
	draw_rect(panel, Color(0.94, 0.97, 1.0, 0.96), true)
	draw_rect(panel.grow(-3.0), accent.lerp(Color("#382485"), 0.62), false, 4.0)
	var center := size * 0.5
	if widget_backdrop != null:
		# authored at 1024x608 (1.684); the panel is not that aspect, so a plain
		# stretch squashed every round object into an egg. Cover-fit instead.
		draw_texture_rect(widget_backdrop, _cover_rect(widget_backdrop), false)
		_draw_widget_layers(center)
		if demo_active:
			_draw_demo_finger()
		return
	if visual_context.begins_with("nursery"):
		_draw_nursery_context(center)
		if demo_active:
			_draw_demo_finger()
		return
	match mode:
		"tap":
			for mark: Vector2 in tap_marks:
				draw_circle(mark, 13.0, Color(accent, 0.85))
				draw_circle(mark, 6.0, Color.WHITE)
			draw_circle(tap_point, 64.0, Color(accent, 0.25))
			draw_arc(tap_point, 64.0, 0.0, TAU, 48, accent, 9.0)
			draw_circle(tap_point, 18.0, Color.WHITE)
		"hold":
			draw_circle(center, minf(size.x, size.y) * 0.25, Color(accent, 0.24))
			draw_arc(center, minf(size.x, size.y) * 0.25, 0.0, TAU, 48, accent, 10.0)
			draw_circle(center, 24.0 if held else 16.0, Color.WHITE)
		"swipe":
			var span := minf(size.x, size.y) * 0.42
			var tail := center - swipe_dir * span
			var head := center + swipe_dir * span
			var side := swipe_dir.orthogonal()
			draw_line(tail, head, accent, 16.0, true)
			draw_colored_polygon(PackedVector2Array([
				head + side * 34.0, head + swipe_dir * 58.0, head - side * 34.0,
			]), accent)
			draw_circle(tail, 22.0, Color.WHITE)
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			draw_arc(center, radius, -2.7, 2.2, 48, accent, 16.0)
			var tip := center + Vector2.from_angle(2.2) * radius
			draw_colored_polygon(PackedVector2Array([
				tip, tip + Vector2(-10, -36), tip + Vector2(30, -14),
			]), accent)
		"choice":
			var show_answer := choice_flash > 0.0 or demo_active
			for index in range(choice_count):
				var point := Vector2(size.x * (float(index) + 0.5) / float(choice_count), center.y)
				var is_answer := index == target_choice and show_answer
				var colour := Color(1.0, 0.86, 0.32) if is_answer else Color(0.34, 0.42, 0.62)
				draw_circle(point, 54.0, Color(colour, 0.34))
				draw_arc(point, 54.0, 0.0, TAU, 36, colour, 9.0)
				if is_answer:
					draw_circle(point, 15.0, Color.WHITE)
		"timing":
			var bar := Rect2(size.x * 0.12, center.y - 23.0, size.x * 0.76, 46.0)
			draw_rect(bar, Color(0.2, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 28.0), Vector2(marker_x, bar.end.y + 28.0), Color.WHITE, 12.0)
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					_draw_imp(target)
	if demo_active:
		_draw_demo_finger()


## Overlay ink bounds, cached per texture: the reveal must sweep the PAINTED
## band, not the whole 608px canvas. Sweeping the canvas made the pour
## saturate at 43% of the hold and then sit frozen — the exact playtest
## complaint ("no animation, no feedback").
var _ink_cache: Dictionary = {}


func _ink_bounds(texture: Texture2D) -> Vector2:
	var key := texture.resource_path
	if _ink_cache.has(key):
		return _ink_cache[key]
	var bounds := Vector2(0.0, 1.0)
	var image := texture.get_image()
	if image != null:
		var h := image.get_height()
		var w := image.get_width()
		var top := -1
		var bottom := -1
		for y in range(h):
			var painted := false
			for x in range(0, w, 4):
				if image.get_pixel(x, y).a > 0.08:
					painted = true
					break
			if painted:
				if top < 0:
					top = y
				bottom = y
		if top >= 0 and bottom > top:
			bounds = Vector2(float(top) / float(h), float(bottom + 1) / float(h))
	_ink_cache[key] = bounds
	return bounds


## Aspect-preserving cover rect: fills the panel, centred, never distorted.
func _cover_rect(texture: Texture2D) -> Rect2:
	var tex := texture.get_size()
	if tex.x <= 0.0 or tex.y <= 0.0:
		return Rect2(Vector2.ZERO, size)
	var scale := maxf(size.x / tex.x, size.y / tex.y)
	var drawn := tex * scale
	return Rect2((size - drawn) * 0.5, drawn)


func _draw_progress_overlay(texture: Texture2D, progress: float, horizontal: bool) -> void:
	var amount := clampf(progress, 0.0, 1.0)
	if amount <= 0.0:
		return
	var texture_size := texture.get_size()
	if horizontal:
		var source := Rect2(0.0, 0.0, texture_size.x * amount, texture_size.y)
		var destination := Rect2(0.0, 0.0, size.x * amount, size.y)
		draw_texture_rect_region(texture, destination, source)
		return
	# sweep the reveal edge across the ink band so 0%..100% of the hold maps
	# to 0%..100% of the visible liquid
	var ink := _ink_bounds(texture)
	var ink_top := ink.x
	var ink_bottom := ink.y
	var edge := ink_bottom - (ink_bottom - ink_top) * amount
	var source_y := texture_size.y * edge
	var source_h := texture_size.y * (ink_bottom - edge)
	if source_h <= 0.0:
		return
	var cover := _cover_rect(texture)
	var destination_y := cover.position.y + cover.size.y * edge
	var destination_h := cover.size.y * (ink_bottom - edge)
	draw_texture_rect_region(
		texture,
		Rect2(cover.position.x, destination_y, cover.size.x, destination_h),
		Rect2(0.0, source_y, texture_size.x, source_h)
	)


func _draw_widget_sprite(texture: Texture2D, center: Vector2, side: float, modulate := Color.WHITE) -> void:
	if texture == null:
		return
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * side * 0.5, Vector2.ONE * side), false, modulate)


func _draw_widget_layers(center: Vector2) -> void:
	match widget_template:
		"gauge":
			if widget_mover != null:
				var pivot := Vector2(size.x * 0.5, size.y * 0.82)
				var rotation := deg_to_rad(lerpf(-60.0, 60.0, timing_position))
				draw_set_transform(pivot, rotation)
				draw_texture_rect(widget_mover, Rect2(-48.0, -84.0, 96.0, 96.0), false)
				draw_set_transform(Vector2.ZERO)
			if widget_overlay != null and (completion_accepted or (feedback_t > 0.0 and feedback_positive)):
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
		"track":
			var run_point := Vector2(lerpf(size.x * 0.12, size.x * 0.88, timing_position), size.y * 0.66)
			_draw_widget_sprite(widget_mover, run_point, 128.0)
			if widget_shared != null and feedback_t > 0.0 and feedback_positive:
				var hit_point := Vector2(lerpf(size.x * 0.12, size.x * 0.88, feedback_position), size.y * 0.66)
				_draw_widget_sprite(widget_shared, hit_point, 82.0)
		"pour":
			if held:
				_draw_widget_sprite(widget_mover, center - Vector2(0.0, 18.0), 138.0)
			if widget_overlay != null:
				_draw_progress_overlay(widget_overlay, widget_fill, false)
		"basin":
			if widget_overlay != null and (held or completion_accepted):
				_draw_progress_overlay(widget_overlay, widget_fill, false)
			if completion_accepted:
				_draw_widget_sprite(widget_shared, center, 118.0)
		"charge":
			if widget_mover != null and (held or completion_accepted):
				_draw_widget_sprite(widget_mover, center, 108.0 + widget_fill * 126.0)
			if widget_overlay != null:
				if completion_accepted:
					draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
				else:
					# the meter tube fills as she holds — it used to stay dark
					# for 3+ seconds and then fade in whole over the last 18%
					_draw_progress_overlay(widget_overlay, widget_fill, false)
		"crank":
			if widget_mover != null:
				draw_set_transform(center, crank_rotation)
				draw_texture_rect(widget_mover, Rect2(-70.0, -70.0, 140.0, 140.0), false)
				draw_set_transform(Vector2.ZERO)
			if widget_overlay != null:
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false, Color(1.0, 1.0, 1.0, widget_fill))
		"trace":
			if widget_overlay != null:
				_draw_progress_overlay(widget_overlay, widget_fill, true)
		"push":
			var mover_point := center + swipe_dir * widget_fill * 42.0
			_draw_widget_sprite(widget_mover, mover_point, 136.0)
			_draw_widget_sprite(widget_shared, center + swipe_dir * 92.0, 92.0, Color(1.0, 1.0, 1.0, 0.72))
		"target":
			for mark: Vector2 in tap_marks:
				_draw_widget_sprite(widget_stamp, mark, 76.0)
			_draw_widget_sprite(widget_mover, tap_point, 142.0)
			if widget_overlay != null and completion_accepted:
				draw_texture_rect(widget_overlay, Rect2(Vector2.ZERO, size), false)
		"lanes":
			var show_answer := choice_flash > 0.0 or demo_active
			if show_answer and widget_mover != null:
				var lane_point := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), size.y * 0.70)
				var source := Rect2(float(target_choice) * 256.0, 0.0, 256.0, 256.0)
				draw_texture_rect_region(widget_mover, Rect2(lane_point - Vector2(62.0, 62.0), Vector2(124.0, 124.0)), source)
			if widget_shared != null and feedback_t > 0.0:
				_draw_widget_sprite(widget_shared, feedback_anchor, 82.0,
					Color.WHITE if feedback_positive else Color(1.0, 0.82, 0.92, 0.82))


func _draw_nursery_baby(texture_index: int, center: Vector2, extent: float) -> void:
	if nursery_textures.is_empty():
		draw_circle(center, extent * 0.30, Color("#ffd6bf"))
		return
	var texture: Texture2D = nursery_textures[posmod(texture_index, nursery_textures.size())]
	draw_texture_rect(texture, Rect2(center - Vector2.ONE * extent * 0.5, Vector2.ONE * extent), false)


func _draw_nursery_context(center: Vector2) -> void:
	match visual_context:
		"nursery_wash":
			var basin := Rect2(center.x - 92.0, center.y - 12.0, 184.0, 82.0)
			draw_rect(basin, Color("#78cfd0"), true)
			draw_arc(Vector2(center.x, basin.position.y), 92.0, 0.0, PI, 32, Color("#ecfbf4"), 10.0)
			for index in range(7):
				var bubble := center + Vector2(-70.0 + float(index) * 23.0, -48.0 - float(index % 3) * 17.0)
				draw_circle(bubble, 9.0 + float(index % 2) * 4.0, Color(0.82, 0.97, 1.0, 0.62))
			draw_circle(center, 25.0 if held else 17.0, Color.WHITE)
			draw_arc(center, 58.0, 0.0, TAU, 40, accent, 9.0)
		"nursery_feed":
			for index in range(3):
				_draw_nursery_baby(index, Vector2(86.0 + float(index) * 100.0, center.y + 48.0), 88.0)
			var bottle_center := Vector2(center.x, center.y - 58.0)
			draw_rect(Rect2(bottle_center - Vector2(23, 38), Vector2(46, 76)), Color("#edf9ee"), true)
			draw_rect(Rect2(bottle_center - Vector2(17, 31), Vector2(34, 51)), Color("#ffe7ac"), true)
			draw_circle(bottle_center + Vector2(0, -44), 12.0, Color("#f1b1a1"))
			draw_arc(bottle_center, 61.0, 0.0, TAU, 40, accent, 9.0)
			draw_circle(bottle_center, 22.0 if held else 15.0, Color.WHITE)
		"nursery_burp":
			_draw_nursery_baby(1, Vector2(center.x, 70.0), 105.0)
			var hand := Vector2(center.x + 92.0, 78.0)
			draw_circle(hand, 28.0, Color("#ffd8bd"))
			draw_arc(hand, 45.0, -1.2, 1.2, 24, accent, 8.0)
			var bar := Rect2(size.x * 0.12, size.y - 82.0, size.x * 0.76, 42.0)
			draw_rect(bar, Color(0.20, 0.23, 0.38), true)
			var good := Rect2(
				lerpf(bar.position.x, bar.end.x, timing_zone.x), bar.position.y,
				bar.size.x * (timing_zone.y - timing_zone.x), bar.size.y
			)
			draw_rect(good, Color(0.46, 0.94, 0.62), true)
			var marker_x := lerpf(bar.position.x, bar.end.x, timing_position)
			draw_line(Vector2(marker_x, bar.position.y - 22.0), Vector2(marker_x, bar.end.y + 22.0), Color.WHITE, 11.0)
		"nursery_bedtime":
			for index in range(3):
				var crib_center := Vector2(72.0 + float(index) * 114.0, center.y + 20.0)
				draw_rect(Rect2(crib_center - Vector2(48, 30), Vector2(96, 78)), Color("#f1d2c2"), true)
				_draw_nursery_baby(index, crib_center - Vector2(0, 10), 74.0)
				draw_rect(Rect2(crib_center.x - 43.0, crib_center.y + 7.0, 86.0, 37.0), Color(0.52, 0.81, 0.77, 0.94), true)
			for star in [Vector2(55, 44), Vector2(145, 30), Vector2(235, 50)]:
				draw_circle(star, 7.0, Color("#ffe483"))
			var arrow_x := size.x - 24.0
			draw_line(Vector2(arrow_x, 54.0), Vector2(arrow_x, size.y - 42.0), accent, 13.0, true)
			draw_colored_polygon(PackedVector2Array([
				Vector2(arrow_x - 28.0, size.y - 68.0), Vector2(arrow_x + 28.0, size.y - 68.0), Vector2(arrow_x, size.y - 28.0),
			]), accent)

func _draw_demo_finger() -> void:
	var center := size * 0.5
	var cycle := fmod(demo_t, 2.4)
	var pressing := cycle > 1.1
	var at := center
	match mode:
		"swipe":
			at = Vector2(lerpf(size.x * 0.22, size.x * 0.78, cycle / 2.4), center.y)
			pressing = true
		"circle":
			var radius := minf(size.x, size.y) * 0.26
			at = center + Vector2.from_angle(-2.7 + cycle * 2.0) * radius
			pressing = true
		"choice":
			var lane := Vector2(size.x * (float(target_choice) + 0.5) / float(choice_count), center.y)
			at = center.lerp(lane, clampf(cycle / 1.1, 0.0, 1.0))
		"timing":
			var bar_x := lerpf(size.x * 0.12, size.x * 0.88, timing_position)
			at = Vector2(bar_x, center.y + 58.0)
			pressing = timing_position >= timing_zone.x and timing_position <= timing_zone.y
		"bop":
			for target: Dictionary in bop_targets:
				if not bool(target.get("popped", false)):
					var pos: Vector2 = target.get("pos", Vector2.ZERO)
					at = center.lerp(pos, clampf(cycle / 1.1, 0.0, 1.0))
					break
		"hold":
			pressing = true
	var halo := 30.0 if pressing else 20.0
	draw_circle(at, halo, Color(0.22, 0.14, 0.52, 0.18))
	draw_circle(at, 14.5, Color("#382485"))
	draw_circle(at, 12.0, Color(1.0, 0.98, 0.86, 0.98))
	if pressing:
		var ring := 18.0 + fmod(demo_t * 46.0, 26.0)
		draw_arc(at, ring, 0.0, TAU, 24, Color(1.0, 0.95, 0.6, 0.6), 4.0)


func _draw_imp(target: Dictionary) -> void:
	var pos: Vector2 = target.get("pos", Vector2.ZERO)
	var radius := float(target.get("r", 44.0))
	var captain := bool(target.get("captain", false))
	var texture := bop_captain_texture if captain else bop_texture
	if texture != null:
		var side := radius * 2.4
		draw_texture_rect(texture, Rect2(pos - Vector2(side, side) * 0.5, Vector2(side, side)), false)
		if captain:
			# plain gold band ring marks the captain over the costume sprite
			draw_arc(pos, radius * 1.16, 0.0, TAU, 36, Color("#e0b34c"), 6.0)
			if int(target.get("hp", 1)) > 1:
				draw_arc(pos, radius * 1.3, 0.0, TAU, 36, Color(1.0, 0.9, 0.5, 0.45), 4.0)
		return
	# basic place-in imp until the codex mischief-imp sprite set lands
	var body := Color("#7a4f9a") if not captain else Color("#5f3a85")
	var belly := Color("#b28ccd")
	draw_circle(pos, radius * 1.18, Color(1.0, 0.86, 0.4, 0.16))
	# curled striped horns
	for side_sign in [-1.0, 1.0]:
		var horn := pos + Vector2(side_sign * radius * 0.62, -radius * 0.78)
		draw_arc(horn, radius * 0.34, PI * 0.2, PI * 1.4, 12, Color("#e8d6a8"), 9.0)
		draw_arc(horn, radius * 0.34, PI * 0.5, PI * 1.1, 8, Color("#a8794f"), 9.0)
	# curled tail
	draw_arc(pos + Vector2(radius * 0.95, radius * 0.55), radius * 0.4, -PI * 0.6, PI * 0.7, 10, body.lightened(0.1), 8.0)
	draw_circle(pos, radius, body)
	draw_circle(pos + Vector2(0, radius * 0.3), radius * 0.55, belly)
	# amber eyes and a friendly fanged grin
	for side_sign in [-1.0, 1.0]:
		var eye := pos + Vector2(side_sign * radius * 0.34, -radius * 0.22)
		draw_circle(eye, radius * 0.17, Color("#f4b642"))
		draw_circle(eye, radius * 0.08, Color("#33203f"))
	draw_arc(pos + Vector2(0, radius * 0.1), radius * 0.34, 0.35, PI - 0.35, 12, Color("#33203f"), 5.0)
	for side_sign in [-1.0, 1.0]:
		var fang := pos + Vector2(side_sign * radius * 0.18, radius * 0.36)
		draw_colored_polygon(PackedVector2Array([
			fang + Vector2(-5, 0), fang + Vector2(5, 0), fang + Vector2(0, 10),
		]), Color.WHITE)
	if captain:
		# plain gold waistband marks the captain (no shell or crest motifs)
		draw_line(pos + Vector2(-radius * 0.8, radius * 0.62), pos + Vector2(radius * 0.8, radius * 0.62), Color("#e0b34c"), 8.0)
		if int(target.get("hp", 1)) > 1:
			draw_arc(pos, radius * 1.12, 0.0, TAU, 32, Color("#e0b34c"), 5.0)
