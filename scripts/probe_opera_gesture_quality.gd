extends SceneTree
## Focused contract for the shared Opera gesture surface: the wordless hand
## follows the real control geometry, and a stationary tap cannot impersonate
## a hold, swipe, or circle. This probe deliberately owns no career state.

const BOXING_SURFACE_SCRIPT := preload("res://scripts/opera_boxing_surface.gd")

var checks := 0
var failed := 0
var events: Array[Dictionary] = []

const BalletSurface := preload("res://scripts/opera_ballet_surface.gd")


func _ck(name: String, ok: bool) -> void:
	checks += 1
	if not ok:
		failed += 1
		print("GESTURE_QUALITY|FAIL|%s" % name)


func _record_gesture(kind: String, amount: float, quality: float) -> void:
	events.append({"kind": kind, "amount": amount, "quality": quality})


func _paid(kind: String) -> bool:
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind and float(event.get("amount", 0.0)) > 0.0:
			return true
	return false


func _paid_count(kind: String) -> int:
	var count := 0
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind and float(event.get("amount", 0.0)) > 0.0:
			count += 1
	return count


func _event_count(kind: String) -> int:
	var count := 0
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind:
			count += 1
	return count


func _paid_total(kind: String) -> float:
	var total := 0.0
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind:
			total += maxf(0.0, float(event.get("amount", 0.0)))
	return total


func _cue_frames(kind: String) -> Array[int]:
	var result: Array[int] = []
	for event: Dictionary in events:
		if String(event.get("kind", "")) == kind:
			result.append(int(round(float(event.get("amount", -1.0)))))
	return result


func _collapse_held_cues(source: Array[int]) -> Array[int]:
	var result: Array[int] = []
	for frame: int in source:
		if result.is_empty() or result[-1] != frame:
			result.append(frame)
	return result


func _pose_at(surface: OperaGestureSurface, time: float) -> Dictionary:
	surface.demo_t = time
	return surface._demo_finger_pose()


func _pose_point(pose: Dictionary) -> Vector2:
	return pose.get("at", Vector2.ZERO)


func _rect_inside(bounds: Rect2, rect: Rect2) -> bool:
	return rect.position.x >= bounds.position.x and rect.position.y >= bounds.position.y \
		and rect.end.x <= bounds.end.x and rect.end.y <= bounds.end.y


func _rotation_safe_square(rect: Rect2) -> Rect2:
	var side := maxf(rect.size.x, rect.size.y) * sqrt(2.0)
	return Rect2(rect.get_center() - Vector2.ONE * side * 0.5, Vector2.ONE * side)


func _texture_alpha_used_rect(texture: Texture2D) -> Rect2:
	if texture == null:
		return Rect2()
	var image := texture.get_image()
	if image == null or image.is_empty():
		return Rect2()
	if image.is_compressed() and image.decompress() != OK:
		return Rect2()
	var minimum := Vector2i(image.get_width(), image.get_height())
	var maximum := Vector2i(-1, -1)
	for y in range(image.get_height()):
		for x in range(image.get_width()):
			if image.get_pixel(x, y).a > 0.01:
				minimum.x = mini(minimum.x, x)
				minimum.y = mini(minimum.y, y)
				maximum.x = maxi(maximum.x, x)
				maximum.y = maxi(maximum.y, y)
	if maximum.x < minimum.x:
		return Rect2()
	return Rect2(Vector2(minimum), Vector2(maximum - minimum + Vector2i.ONE))


func _rotated_texture_ink_bounds(texture_size: Vector2, used: Rect2,
		draw_rect: Rect2, rotation: float) -> Rect2:
	var pixel_corners: Array[Vector2] = [
		used.position,
		Vector2(used.end.x, used.position.y),
		used.end,
		Vector2(used.position.x, used.end.y),
	]
	var minimum: Vector2 = Vector2(INF, INF)
	var maximum: Vector2 = Vector2(-INF, -INF)
	for pixel_corner: Vector2 in pixel_corners:
		var uv := pixel_corner / texture_size
		var local := (uv - Vector2.ONE * 0.5) * draw_rect.size
		var transformed := draw_rect.get_center() + local.rotated(rotation)
		minimum = minimum.min(transformed)
		maximum = maximum.max(transformed)
	return Rect2(minimum, maximum - minimum)


func _boxing_touch_event(boxing: OperaBoxingSurface, finger: int,
		pressed: bool, at: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.pressed = pressed
	event.position = at
	boxing._gui_input(event)


func _boxing_drag_event(boxing: OperaBoxingSurface, finger: int,
		at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = at
	boxing._gui_input(event)


func _boxing_mouse_button(boxing: OperaBoxingSurface, pressed: bool,
		at: Vector2, device_id: int = 0) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	event.position = at
	event.device = device_id
	boxing._gui_input(event)


func _boxing_mouse_motion(boxing: OperaBoxingSurface, at: Vector2,
		device_id: int = 0) -> void:
	var event := InputEventMouseMotion.new()
	event.position = at
	event.device = device_id
	boxing._gui_input(event)


func _pose_choice_index(surface: Variant, wanted_frame: int) -> int:
	var frames: Array[int] = surface.pose_option_frames()
	for index in range(frames.size()):
		if frames[index] == wanted_frame:
			return index
	return -1


func _test_ballet_surface() -> void:
	var ballet: Variant = BalletSurface.new()
	ballet.size = Vector2(854, 660)
	get_root().add_child(ballet)
	ballet.set_process(false)
	ballet.gesture.connect(_record_gesture)

	# MIRROR: the first turn is two huge portraits; demonstrations and assists
	# may teach forever but only a real matching touch can bank a round.
	events.clear()
	ballet.configure("ballet_pose", Color("#ff8fc8"))
	ballet.set_process(false)
	var first_rects: Array[Rect2] = ballet.pose_option_rects()
	var first_frames: Array[int] = ballet.pose_option_frames()
	var first_target: int = ballet.pose_target_frame()
	var first_target_index: int = _pose_choice_index(ballet, first_target)
	_ck("ballet phrase uses atlas heart, open, and crown in that order",
		BalletSurface.POSE_FRAMES == [3, 2, 1]
		and first_target == 3 and first_frames == [1, 3])
	var watch_stream := load(
		"res://assets/audio/voices/roshan_op_ballerina_watch.ogg") as AudioStream
	_ck("mirror demo lets the complete watch recording finish before handoff",
		watch_stream != null
		and ballet.demo_duration() >= watch_stream.get_length() + 0.05
		and ballet.demo_duration() <= 2.5)
	_ck("ballet mirror begins with two 180px-or-larger portrait targets",
		first_rects.size() == 2 and first_target_index >= 0
		and first_rects[0].size.x >= 180.0 and first_rects[0].size.y >= 180.0
		and first_rects[1].size.x >= 180.0 and first_rects[1].size.y >= 180.0)
	ballet._press(first_rects[first_target_index].get_center())
	ballet._release(first_rects[first_target_index].get_center())
	_ck("touching during mirror demonstration cannot progress",
		ballet.pose_round == 0 and not _paid("ballet_pose"))
	ballet._process(ballet.demo_duration() + 0.1)
	_ck("mirror emits one your-turn cue after its initial watch demo",
		_event_count("ballet_ready") == 1)
	ballet._process(4.9)
	_ck("ballet assist waits for five playable seconds after the demo",
		ballet.assist_level() == 0 and ballet.pose_round == 0)
	ballet._process(0.2)
	_ck("ballet first assist appears at five seconds without auto-progress",
		ballet.assist_level() == 1 and ballet.pose_round == 0
		and not _paid("ballet_pose"))
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._process(4.8)
	_ck("ballet strong assist waits for ten cumulative playable seconds",
		ballet.assist_level() == 1 and ballet.pose_round == 0)
	ballet._process(0.2)
	_ck("ballet strong assist enlarges guidance at ten seconds without winning",
		ballet.assist_level() == 2 and ballet.pose_round == 0
		and not _paid("ballet_pose"))
	ballet._process(ballet.demo_duration() + 0.1)
	var wrong_index := 0 if first_frames[0] != first_target else 1
	ballet._press(first_rects[wrong_index].get_center())
	ballet._release(first_rects[wrong_index].get_center())
	_ck("wrong ballet portrait replays the same round with zero loss or payout",
		ballet.pose_round == 0 and ballet.demo_active and not _paid("ballet_pose"))
	ballet.restart_demo()
	_ck("mirror replay preserves its unresolved round", ballet.pose_round == 0)
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._press(first_rects[first_target_index].get_center())
	ballet._release(first_rects[first_target_index].get_center())
	_ck("real matching portrait banks exactly one mirror round",
		ballet.pose_round == 1 and _paid_count("ballet_pose") == 1)
	var mirror_targets: Array[int] = [first_target]
	var mirror_target_xs: Array[float] = [
		first_rects[first_target_index].get_center().x,
	]
	var pose_guard := 0
	while ballet.pose_round < int(BalletSurface.POSE_ROUNDS) and pose_guard < 6:
		ballet._process(ballet.demo_duration() + 0.1)
		var target: int = ballet.pose_target_frame()
		mirror_targets.append(target)
		var option_index: int = _pose_choice_index(ballet, target)
		var rects: Array[Rect2] = ballet.pose_option_rects()
		mirror_target_xs.append(rects[option_index].get_center().x)
		ballet._press(rects[option_index].get_center())
		ballet._release(rects[option_index].get_center())
		pose_guard += 1
	_ck("three deliberate portrait matches complete Mirror with three payouts",
		ballet.pose_round == int(BalletSurface.POSE_ROUNDS)
		and _paid_count("ballet_pose") == int(BalletSurface.POSE_ROUNDS))
	_ck("mirror presents the complete low-open-crown pose phrase exactly once",
		mirror_targets == [3, 2, 1])
	_ck("mirror moves the correct portrait right, centre, then left",
		mirror_target_xs.size() == 3
		and mirror_target_xs[0] > ballet.size.x * 0.55
		and absf(mirror_target_xs[1] - ballet.size.x * 0.5) <= 2.0
		and mirror_target_xs[2] < ballet.size.x * 0.40)

	# RIBBON: one curve owns painting and collision. A coarse path with a lift
	# completes; a direct chord cannot skip across distant sine crossings.
	events.clear()
	ballet.configure("ballet_ribbon", Color("#ff8fc8"))
	ballet.set_process(false)
	ballet._process(ballet.demo_duration() + 0.1)
	_ck("ribbon start pearl and corridor exceed the one-finger minimum",
		ballet.ribbon_resume_rect().size.x >= 110.0
		and ballet.ribbon_resume_rect().size.y >= 110.0
		and ballet.ribbon_corridor_width() >= 90.0)
	var ribbon_corner: Vector2 = ballet.ribbon_resume_rect().position + Vector2.ONE * 2.0
	_ck("ribbon visible pearl and accepted start share one circular geometry",
		ballet.ribbon_resume_hit(ballet.ribbon_resume_rect().get_center())
		and not ballet.ribbon_resume_hit(ribbon_corner)
		and is_equal_approx(ballet.ribbon_resume_radius() * 2.0,
			ballet.ribbon_resume_rect().size.x))
	_ck("ribbon demo never echoes its phase instruction as a ready cue",
		_event_count("ballet_ready") == 0)
	ballet._press(ballet.ribbon_resume_rect().get_center())
	ballet._drag(ballet.ribbon_point(1.0))
	ballet._release(ballet.ribbon_point(1.0))
	var chord_progress: float = ballet.ribbon_progress
	_ck("straight ribbon chord cannot skip the visible S current",
		chord_progress < 0.25 and chord_progress >= 0.0)
	ballet.restart_demo()
	_ck("ribbon replay preserves every accepted fraction",
		is_equal_approx(ballet.ribbon_progress, chord_progress))
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._press(ballet.ribbon_resume_rect().get_center())
	var ribbon_guard := 0
	while ballet.ribbon_progress < 0.50 and ribbon_guard < 24:
		var next_ribbon: float = minf(0.50, ballet.ribbon_progress + 0.075)
		ballet._drag(ballet.ribbon_point(next_ribbon))
		ribbon_guard += 1
	ballet._release(ballet.ribbon_point(ballet.ribbon_progress))
	var lifted_progress: float = ballet.ribbon_progress
	ballet.restart_demo()
	_ck("lifting halfway banks ribbon progress for resume",
		lifted_progress >= 0.49 and is_equal_approx(ballet.ribbon_progress, lifted_progress))
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._press(ballet.ribbon_resume_rect().get_center())
	ribbon_guard = 0
	while ballet.ribbon_progress < 0.999 and ribbon_guard < 24:
		var next_ribbon: float = minf(1.0, ballet.ribbon_progress + 0.075)
		ballet._drag(ballet.ribbon_point(next_ribbon))
		ribbon_guard += 1
	ballet._release(ballet.ribbon_point(1.0))
	_ck("coarse twelve-hertz ribbon samples with a lift complete monotonically",
		ballet.ribbon_progress >= 0.999 and _paid("ballet_ribbon"))

	# TWIRL: the visible annulus and pearl handle own the orbit. Centre scrubs
	# pay nothing; an orbit can be resumed and works in either direction.
	events.clear()
	ballet.configure("ballet_twirl", Color("#ff8fc8"))
	ballet.set_process(false)
	ballet._process(ballet.demo_duration() + 0.1)
	_ck("twirl ring and pearl handle meet the one-finger minimum",
		ballet.twirl_ring_width() >= 110.0
		and float(BalletSurface.TWIRL_HANDLE_DIAMETER) >= 110.0)
	_ck("twirl demo never echoes its phase instruction as a ready cue",
		_event_count("ballet_ready") == 0)
	ballet._press(ballet.twirl_center())
	ballet._release(ballet.twirl_center())
	ballet._process(ballet.demo_duration() + 0.1)
	var top_handle: Vector2 = ballet.twirl_handle_position()
	ballet._press(top_handle)
	ballet._drag(ballet.twirl_center())
	ballet._drag(ballet.twirl_center() + Vector2.DOWN * ballet.twirl_radius())
	ballet._release(ballet.twirl_center() + Vector2.DOWN * ballet.twirl_radius())
	_ck("centre scrub and straight diameter cannot pay for a twirl",
		is_zero_approx(ballet.twirl_progress) and not _paid("ballet_twirl"))
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._press(ballet.twirl_handle_position())
	for sector in range(1, 9):
		var angle: float = -PI * 0.5 + float(sector) * TAU / 16.0
		ballet._drag(ballet.twirl_center()
			+ Vector2.from_angle(angle) * ballet.twirl_radius())
	ballet._release(ballet.twirl_handle_position())
	var half_turn: float = ballet.twirl_progress
	ballet.restart_demo()
	_ck("half twirl remains banked across lift and replay",
		half_turn > 0.45 and half_turn < 0.55
		and is_equal_approx(ballet.twirl_progress, half_turn))
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._press(ballet.twirl_handle_position())
	for sector in range(9, 17):
		var angle: float = -PI * 0.5 + float(sector) * TAU / 16.0
		ballet._drag(ballet.twirl_center()
			+ Vector2.from_angle(angle) * ballet.twirl_radius())
	ballet._release(ballet.twirl_handle_position())
	_ck("counter-clockwise adjacent sectors complete one resumed grand twirl",
		ballet.twirl_progress >= 0.999 and ballet.twirl_direction == 1
		and _paid("ballet_twirl"))
	var resumed_twirl_cues: Array[int] = _cue_frames("ballet_pose_cue")
	_ck("twirl replay may re-hold a pose but cannot scramble the phrase",
		_collapse_held_cues(resumed_twirl_cues) == [3, 2, 1])
	events.clear()
	ballet.configure("ballet_twirl", Color("#ff8fc8"))
	ballet.set_process(false)
	ballet._process(ballet.demo_duration() + 0.1)
	ballet._press(ballet.twirl_handle_position())
	for sector in range(1, 17):
		var angle: float = -PI * 0.5 - float(sector) * TAU / 16.0
		ballet._drag(ballet.twirl_center()
			+ Vector2.from_angle(angle) * ballet.twirl_radius())
	ballet._release(ballet.twirl_handle_position())
	_ck("clockwise adjacent sectors are equally valid",
		ballet.twirl_progress >= 0.999 and ballet.twirl_direction == -1
		and _paid("ballet_twirl"))
	_ck("uninterrupted twirl cues low-open-crown exactly once",
		_cue_frames("ballet_pose_cue") == [3, 2, 1])
	ballet.queue_free()


func _finish_after_render(surface: OperaGestureSurface,
		boxing: OperaBoxingSurface) -> void:
	# Let CanvasItem execute each custom draw path once. Analyzer-only tests do
	# not catch invalid draw geometry or texture-region calls.
	for specialist_mode: String in [
		"xray_scan", "dance_sequence", "candy_sort", "paint_reveal", "farm_lob",
		"clue_board", "crown_chest", "garden_plant",
		"magic_cabinet",
	]:
		surface.configure(specialist_mode, Color.WHITE)
		surface.queue_redraw()
		await process_frame
	for boxing_mode: String in [
		"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
	]:
		boxing.configure(boxing_mode, Color.WHITE)
		boxing.queue_redraw()
		await process_frame
	_ck("boxing glove guide, drills, imp finale, and belt paths render", true)
	for causal: Dictionary in [
		{"mode": "hold", "context": "nursery_feed"},
		{"mode": "tap", "context": "nursery_burp"},
		{"mode": "swipe", "context": "nursery_bedtime"},
		{"mode": "hold", "context": "magic_vanish"},
	]:
		surface.configure(String(causal["mode"]), Color.WHITE, 1,
			String(causal["context"]))
		surface.set_fill(0.72)
		surface.nursery_burp_pat_t = 0.20
		surface.queue_redraw()
		await process_frame
	for charge_context: String in [
		"charge_ballerina", "charge_astronaut", "charge_popstar",
	]:
		surface.configure("hold", Color.WHITE, 1, charge_context)
		surface.held = true
		surface.set_fill(0.62)
		surface.queue_redraw()
		await process_frame
		_ck("%s dispatches contextual charge draw" % charge_context,
			surface.last_contextual_draw_route == "charge:%s" % charge_context)
		surface.set_fill(1.0)
		surface.accept_completion()
		surface.queue_redraw()
		await process_frame
	for crank_context: String in [
		"crank_chef", "crank_ballerina", "crank_candymaker",
		"crank_doctor", "crank_astronaut", "crank_popstar",
	]:
		surface.configure("circle", Color.WHITE, 1, crank_context)
		surface.crank_rotation = 1.05
		surface.set_fill(0.64)
		surface.queue_redraw()
		await process_frame
		_ck("%s dispatches diegetic crank draw" % crank_context,
			surface.last_contextual_draw_route == "crank:%s" % crank_context)
		surface.set_fill(1.0)
		surface.accept_completion()
		surface.queue_redraw()
		await process_frame
	for trace_context: String in [
		"trace_chef", "trace_ballerina", "trace_doctor", "trace_magician",
	]:
		surface.configure("swipe", Color.WHITE, 1, trace_context)
		surface.trace_points = [
			surface._trace_demo_point(0.20), surface._trace_demo_point(0.42),
		]
		surface.queue_redraw()
		await process_frame
	for push_context: String in ["push_farmer", "push_racer"]:
		surface.configure("swipe", Color.WHITE, 1, push_context)
		surface.set_fill(0.58)
		surface.queue_redraw()
		await process_frame
		surface.set_fill(1.0)
		surface.accept_completion()
		surface.queue_redraw()
		await process_frame
	surface.configure("circle", Color.WHITE, 1, "crank_magician")
	surface.crank_rotation = 1.1
	surface.set_fill(0.64)
	surface.queue_redraw()
	await process_frame
	_ck("portal renders stationary doorway before visible rotating aperture",
		surface.last_portal_layer_order == "doorway>aperture")
	surface.set_fill(1.0)
	surface.accept_completion()
	surface.queue_redraw()
	await process_frame
	_ck("portal completion glow remains the final composited layer",
		surface.last_portal_layer_order == "doorway>aperture>glow")
	surface.configure("circle", Color.WHITE, 1, "crank_racer")
	surface.crank_rotation = 0.9
	surface.set_fill(0.55)
	surface.queue_redraw()
	await process_frame
	surface.set_fill(1.0)
	surface.accept_completion()
	surface.queue_redraw()
	await process_frame
	surface.configure("oven", Color.WHITE)
	surface.oven_t = 0.62
	surface.oven_done = true
	surface.accept_completion()
	surface.queue_redraw()
	await process_frame
	var ballet: Variant = BalletSurface.new()
	ballet.size = Vector2(854, 660)
	get_root().add_child(ballet)
	for ballet_mode: String in ["ballet_pose", "ballet_ribbon", "ballet_twirl"]:
		ballet.configure(ballet_mode, Color("#ff8fc8"))
		ballet.set_process(false)
		ballet.queue_redraw()
		await process_frame
	_ck("all three full-stage ballet draw routes render headlessly", true)
	ballet.queue_free()
	_ck("specialist, contextual charge/crank/trace, long-push, portal, wheel-install, causal, and oven paths render", true)
	print("GESTURE_QUALITY|result: %s (%d checks)" % [
		"ALL OK" if failed == 0 else "%d FAIL" % failed,
		checks,
	])
	quit(0 if failed == 0 else 1)


func _init() -> void:
	var surface := OperaGestureSurface.new()
	surface.size = Vector2(852, 560)
	get_root().add_child(surface)
	surface.set_process(false)
	surface.gesture.connect(_record_gesture)
	var boxing: OperaBoxingSurface = BOXING_SURFACE_SCRIPT.new()
	boxing.size = Vector2(852, 560)
	get_root().add_child(boxing)
	boxing.set_process(false)
	boxing.gesture.connect(_record_gesture)
	_test_ballet_surface()

	# Directional demos use the same vector as the input gate.
	surface.configure("swipe", Color.WHITE)
	surface.swipe_dir = Vector2.DOWN
	var down_start := _pose_point(_pose_at(surface, 0.0))
	var down_end := _pose_point(_pose_at(surface, 1.85))
	_ck("down-swipe hand travels down, not sideways",
		down_end.y > down_start.y + 250.0 and absf(down_end.x - down_start.x) < 1.0)

	# Specialist demos point at their actual visible controls.
	surface.configure("pourt", Color.WHITE)
	var pour_pose := _pose_at(surface, 1.2)
	_ck("pour hand grabs the real pitcher",
		_pose_point(pour_pose).distance_to(surface._pour_pitcher_rect().get_center()) < 16.0
		and bool(pour_pose.get("pressing", false)))

	# Pixel 10 does not crop the outer 16:9 stage; the reported first-game
	# failure is inside this exact 392x232 shipping surface. Exercise its real
	# press/hold/release path at phone frame rates instead of awarding synthetic
	# progress or checking only the ghost hand.
	surface.size = Vector2(392.0, 232.0)
	for frame_rate: int in [30, 60]:
		events.clear()
		surface.configure("pourt", Color.WHITE, 1, "pour_candymaker")
		var art_set_ok := surface.widget_backdrop != null \
			and surface.widget_overlay != null and surface.widget_mover != null \
			and surface.pour_empty_mover_texture != null \
			and surface.pour_demo_hand_texture != null \
			and surface.widget_backdrop.get_size() == Vector2(1024.0, 576.0) \
			and surface.widget_overlay.get_size() == Vector2(1024.0, 576.0) \
			and surface.widget_mover.get_size() == Vector2(512.0, 256.0) \
			and surface.pour_empty_mover_texture.get_size() == Vector2(512.0, 256.0) \
			and surface.widget_backdrop.resource_path.ends_with(
				"widget_pour_candymaker.png") \
			and surface.widget_overlay.resource_path.ends_with(
				"widget_pour_candymaker_fill.png") \
			and surface.widget_mover.resource_path.ends_with(
				"widget_pour_candymaker_mover.png") \
			and surface.pour_empty_mover_texture.resource_path.ends_with(
				"widget_pour_candymaker_mover_empty.png") \
			and surface.pour_demo_hand_texture.resource_path.ends_with("ghost_hand.png") \
			and surface.target_piece_textures.is_empty()
		_ck("candymaker pour uses only its authored empty-mold, fill, and ladle states at %d fps"
			% frame_rate, art_set_ok)
		var shipping_bounds := Rect2(Vector2.ZERO, surface.size)
		var bowl := surface._pour_bowl_rect()
		var x_bounds := surface._pour_x_bounds()
		var ladle_used := _texture_alpha_used_rect(surface.widget_mover)
		var geometry_ok := _rect_inside(shipping_bounds, bowl) \
			and ladle_used.has_area() \
			and x_bounds.x <= surface._pour_home_x() \
			and surface._pour_home_x() <= x_bounds.y
		for pitcher_x: float in [x_bounds.x, surface._pour_home_x(), x_bounds.y]:
			surface.pour_x = pitcher_x
			geometry_ok = geometry_ok \
				and _rect_inside(shipping_bounds, surface._pour_pitcher_hit_rect())
			for tilt: float in [0.0, 0.37, 0.5, 0.75, 1.0]:
				surface.pour_tilt = tilt
				var spout := surface._pour_spout_point()
				var landing := surface._pour_landing_point()
				var ink_bounds := _rotated_texture_ink_bounds(
					surface.widget_mover.get_size(), ladle_used,
					surface._pour_pitcher_rect(), surface._pour_pitcher_rotation())
				geometry_ok = geometry_ok and _rect_inside(shipping_bounds, ink_bounds) \
					and spout.x >= bowl.position.x and spout.x <= bowl.end.x
				if tilt > 0.36:
					geometry_ok = geometry_ok and surface._pour_pitcher_rotation() > 0.0 \
						and landing.x >= spout.x + 8.0 \
						and landing.y >= spout.y + 8.0 and bowl.has_point(landing)
		_ck("candymaker ladle and down-right pour stay registered and visible at %d fps"
			% frame_rate,
			geometry_ok)

		surface.pour_x = surface._pour_home_x()
		surface.pour_tilt = 0.0
		surface._process(1.0)
		_ck("candymaker pour demo pays no passive progress at %d fps" % frame_rate,
			is_zero_approx(surface.pour_level) and not _paid("pourt"))
		surface._press(Vector2(8.0, 8.0))
		surface._process(0.8)
		surface._release(Vector2(8.0, 8.0))
		_ck("off-ladle touch cannot fill candymaker mold at %d fps" % frame_rate,
			is_zero_approx(surface.pour_level) and not _paid("pourt"))

		var step := 1.0 / float(frame_rate)
		var active_seconds := 0.0
		var grab := surface._pour_pitcher_rect().get_center()
		surface._press(grab)
		while active_seconds < 0.9:
			surface._process(step)
			active_seconds += step
		surface._release(grab)
		var paused_level := surface.pour_level
		for _pause_frame in range(frame_rate):
			surface._process(step)
		_ck("releasing candymaker ladle pauses without losing syrup at %d fps" % frame_rate,
			is_equal_approx(surface.pour_level, paused_level) and paused_level > 0.0)

		grab = surface._pour_pitcher_rect().get_center()
		surface._press(grab)
		# The deliberate release above incurs a second visible tilt-in. Even with
		# that interruption the cumulative finger time stays preschool-short;
		# one uninterrupted hold completes in roughly 3.5 seconds.
		while surface.pour_level < 1.0 and active_seconds < 4.5:
			surface._process(step)
			active_seconds += step
		surface._release(grab)
		_ck("real candymaker hold completes a full five-point pour by %d fps" % frame_rate,
			is_equal_approx(surface.pour_level, 1.0)
			and is_equal_approx(_paid_total("pourt"), 5.0)
			and _event_count("pour_ding") == 1 and active_seconds < 4.5)
		surface.accept_completion()
		for _settle_frame in range(frame_rate):
			surface._process(step)
		_ck("completed candymaker ladle settles upright and visibly empty at %d fps"
			% frame_rate,
			is_zero_approx(surface.pour_tilt) and not surface._pour_stream_active()
			and surface.pour_empty_mover_texture != null
			and is_zero_approx(surface._candymaker_full_ladle_alpha()))
	var retired_pour_source := FileAccess.get_file_as_string(
		"res://scripts/opera_gesture_surface.gd")
	_ck("candymaker pour cannot reuse the retired finished-candy target or ring helper",
		not retired_pour_source.contains("CANDYMAKER_MOLD_PATH")
		and not retired_pour_source.contains("_draw_candymaker_pour_mold"))
	surface.size = Vector2(852.0, 560.0)

	events.clear()
	surface.configure("oven", Color.WHITE)
	surface._process(10.5)
	_ck("oven waits at toasty cap beyond ten seconds with zero passive payout",
		is_equal_approx(surface.oven_t, 1.0) and not surface.oven_done
		and not _paid("oven") and surface.demo_active)
	var capped_handle := surface._oven_handle_hit_rect().get_center()
	surface._press(capped_handle)
	surface._release(capped_handle)
	_ck("real mitt tap completes after indefinite toasty hold",
		surface.oven_done and _paid_count("oven") == 1)
	events.clear()
	surface.configure("oven", Color.WHITE)
	surface.oven_t = 0.2
	var oven_watch := _pose_at(surface, 0.4)
	_ck("cold oven hand watches the thermometer without tapping",
		surface._oven_meter_rect().grow(12.0).has_point(_pose_point(oven_watch))
		and not bool(oven_watch.get("pressing", true)))
	surface.oven_t = 0.55
	var oven_take := _pose_at(surface, 1.2)
	_ck("golden oven hand taps the mitt handle",
		_pose_point(oven_take).distance_to(surface._oven_handle_rect().get_center()) < 1.0
		and bool(oven_take.get("pressing", false)))
	_ck("oven touch target generously grows the painted handle",
		surface._oven_handle_hit_rect().encloses(surface._oven_handle_rect())
		and surface._oven_handle_hit_rect().size.x >= surface._oven_handle_rect().size.x + 48.0)
	events.clear()
	surface._press(Vector2(8.0, 8.0))
	surface._release(Vector2(8.0, 8.0))
	_ck("outside golden-oven tap pays zero and cannot remove cake",
		not _paid("oven") and not surface.oven_done and surface.demo_active)
	surface._press(surface._oven_handle_hit_rect().get_center())
	surface._release(surface._oven_handle_hit_rect().get_center())
	_ck("grown oven handle alone removes golden cake",
		surface.oven_done and _paid_count("oven") == 1)
	surface.accept_completion()
	_ck("oven completion retains baked causal state",
		surface.completion_accepted and surface.oven_done and surface.oven_t >= 0.45)

	surface.size = Vector2(712, 560)
	surface.configure("pipe", Color.WHITE)
	var pipe_start := _pose_point(_pose_at(surface, 0.0))
	var pipe_end := _pose_point(_pose_at(surface, 1.75))
	_ck("pipe hand carries the first tray tile to the first useful gap",
		pipe_start.distance_to(surface._pipe_tray_rect(0).get_center()) < 1.0
		and pipe_end.distance_to(surface._pipe_cell_rect(5).get_center()) < 1.0)
	var expected_demo_slots: Array[int] = [0, 0, 1]
	var compatible_demo_slots := true
	for round_index in range(OperaGestureSurface.PIPE_ROUNDS.size()):
		surface.pipe_round = round_index
		surface._pipe_setup_round()
		var target_cell := surface._pipe_demo_target_cell()
		compatible_demo_slots = compatible_demo_slots \
			and surface._pipe_demo_tray_slot(target_cell) == expected_demo_slots[round_index]
	_ck("every pipe round demonstrates its first useful compatible tray tile",
		compatible_demo_slots)
	# Restore round one for the geometry checks below.
	surface.pipe_round = 0
	surface._pipe_setup_round()
	var pipe_bounds := Rect2(Vector2.ZERO, surface.size)
	var pipe_geometry_inside := true
	for cell in range(OperaGestureSurface.PIPE_COLS * OperaGestureSurface.PIPE_ROWS):
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_cell_rect(cell))
	for slot in range(6):
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_tray_rect(slot))
	for round_data: Dictionary in OperaGestureSurface.PIPE_ROUNDS:
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_tank_rect(round_data))
		pipe_geometry_inside = pipe_geometry_inside and _rect_inside(
			pipe_bounds, surface._pipe_intake_rect(round_data))
	_ck("all pipe cells, six tray pieces, tank, and every intake fit the surface",
		pipe_geometry_inside)
	var stage_bounds := Rect2(Vector2.ZERO, Vector2(1280, 720))
	var both_panel_docks_inside := true
	for panel_position: Vector2 in [Vector2(24, 36), Vector2(496, 36)]:
		both_panel_docks_inside = both_panel_docks_inside and _rect_inside(
			stage_bounds, Rect2(panel_position, Vector2(760, 648)))
		var surface_origin := panel_position + Vector2(24, 24)
		for round_data: Dictionary in OperaGestureSurface.PIPE_ROUNDS:
			var global_intake := surface._pipe_intake_rect(round_data)
			global_intake.position += surface_origin
			both_panel_docks_inside = both_panel_docks_inside and _rect_inside(
				stage_bounds, global_intake)
	_ck("pipe endpoint art fits 1280x720 at either authored panel dock",
		both_panel_docks_inside)
	surface.size = Vector2(852, 560)

	surface.configure("echo", Color.WHITE)
	surface.echo_listening = true
	surface.echo_input_i = 0
	var echo_pose := _pose_at(surface, 1.2)
	_ck("echo hand taps the next sung star on Roshan's turn",
		_pose_point(echo_pose).distance_to(surface._echo_star_center(0)) < 1.0
		and bool(echo_pose.get("pressing", false)))
	surface.echo_glow = 0.40
	surface._echo_tick(0.15)
	_ck("echo listening glow keeps decaying between input frames",
		is_equal_approx(surface.echo_glow, 0.25) and surface.echo_listening)

	# Doctor uses the approved X-ray-machine card and a square scanner sweep,
	# not Detective's stage-wide magnifying glass. Only crossing a new sore spot
	# changes state; taps and unrelated motion are harmless.
	events.clear()
	surface.size = Vector2(392, 232)
	surface.configure("xray_scan", Color.WHITE)
	_ck("X-ray scan binds the approved Doctor machine card",
		surface.visual_context == "target_doctor" and surface.widget_backdrop != null
		and surface.widget_backdrop.resource_path.ends_with("widget_target_doctor.png"))
	var first_xray_target := surface._xray_target_center(0)
	var first_xray_demo := _pose_at(surface, 1.65)
	_ck("X-ray rehint sweeps to the current real sore spot",
		_pose_point(first_xray_demo).distance_to(first_xray_target) < 1.0
		and bool(first_xray_demo.get("pressing", false)))
	surface._press(first_xray_target)
	surface._release(first_xray_target)
	_ck("stationary scanner tap cannot diagnose",
		surface.xray_found_count == 0 and not _paid("xray_scan"))
	var wrong_scan_start := Vector2(24, surface.size.y - 18.0)
	var wrong_scan_end := Vector2(76, surface.size.y - 18.0)
	surface._press(wrong_scan_start)
	surface._drag(wrong_scan_end)
	surface._release(wrong_scan_end)
	_ck("unrelated scanner sweep is safe and pays zero",
		surface.xray_found_count == 0 and not _paid("xray_scan") and surface.demo_active)
	var scan_home := surface._xray_home_point()
	surface._press(scan_home)
	surface._drag(first_xray_target)
	surface._release(first_xray_target)
	_ck("first valid scan banks exactly one diagnosis",
		surface.xray_found_count == 1 and _paid_count("xray_scan") == 1
		and not surface.xray_complete)
	var second_xray_target := surface._xray_target_center(1)
	var second_xray_demo := _pose_at(surface, 1.65)
	_ck("scanner rehint advances to the second deterministic spot",
		_pose_point(second_xray_demo).distance_to(second_xray_target) < 1.0)
	surface._press(scan_home)
	surface._drag(second_xray_target)
	surface._release(second_xray_target)
	_ck("two valid scan transitions complete with exactly two payouts",
		surface.xray_complete and surface.xray_found_count == OperaGestureSurface.XRAY_SPOTS.size()
		and _paid_count("xray_scan") == OperaGestureSurface.XRAY_SPOTS.size())
	surface.size = Vector2(852, 560)

	# A stationary press supplies state/feedback only. Progress comes from a
	# sustained hold in the owner or qualifying movement in _drag().
	var center := surface.size * 0.5
	for stationary_mode: String in ["hold", "swipe", "circle"]:
		events.clear()
		surface.configure(stationary_mode, Color.WHITE)
		surface._press(center)
		_ck("stationary %s press pays no progress" % stationary_mode,
			not _paid(stationary_mode))
		if stationary_mode == "hold":
			_ck("hold press still arms sustained input", surface.held)
		surface._release(center)

	events.clear()
	surface.configure("swipe", Color.WHITE)
	surface._press(center)
	surface._drag(center + Vector2(100.0, 0.0))
	_ck("real swipe motion still advances", _paid("swipe"))
	surface._release(center + Vector2(100.0, 0.0))

	events.clear()
	surface.configure("circle", Color.WHITE)
	var radius := 90.0
	surface._press(center + Vector2.RIGHT * radius)
	surface._drag(center + Vector2.from_angle(0.28) * radius)
	surface._drag(center + Vector2.from_angle(0.56) * radius)
	_ck("real circular motion still advances", _paid("circle"))
	surface._release(center + Vector2.from_angle(0.56) * radius)

	# Farmer HERD and Racer TO THE LINE are destination pushes. Their approved
	# isolated mover crosses most of the shipping card, and only aligned real
	# swipe motion can advance it toward the gate/arch.
	surface.size = Vector2(392, 232)
	var shipping_bounds := Rect2(Vector2.ZERO, surface.size)
	for push_context: String in ["push_farmer", "push_racer"]:
		events.clear()
		surface.configure("swipe", Color.WHITE, 1, push_context)
		var push_start := surface._long_push_start()
		var push_finish := surface._long_push_end()
		var push_distance := push_finish.x - push_start.x
		_ck("%s travels 65-75 percent of card width" % push_context,
			push_distance >= surface.size.x * 0.65
			and push_distance <= surface.size.x * 0.75)
		_ck("%s mover stays fully inside at start and destination" % push_context,
			_rect_inside(shipping_bounds, surface._long_push_mover_rect(0.0))
			and _rect_inside(shipping_bounds, surface._long_push_mover_rect(1.0))
			and _rect_inside(shipping_bounds, surface._long_push_start_hit_rect()))
		_ck("%s has the authored moving subject count" % push_context,
			surface._long_push_actor_count() == (3 if push_context == "push_farmer" else 1))
		var push_demo_start := _pose_point(_pose_at(surface, 0.0))
		var push_demo_finish := _pose_point(_pose_at(surface, 1.85))
		_ck("%s wordless demo traverses the authored lane" % push_context,
			push_demo_start.distance_to(push_start) < 1.0
			and push_demo_finish.distance_to(push_finish) < 1.0)
		var outside_start := Vector2(surface.size.x * 0.52, surface.size.y * 0.12)
		surface._press(outside_start)
		surface._drag(outside_start + Vector2(90.0, 0.0))
		surface._release(outside_start + Vector2(90.0, 0.0))
		_ck("%s outside swipe pays zero and cannot engage journey" % push_context,
			not _paid("swipe") and is_zero_approx(surface.widget_fill)
			and surface.demo_active)
		events.clear()
		surface.configure("swipe", Color.WHITE, 1, push_context)
		var budget_before_wrong := surface.swipe_budget
		surface._press(push_start)
		surface._drag(push_start - Vector2(45.0, 0.0))
		_ck("%s wrong-way travel pays zero without consuming correction budget" % push_context,
			not _paid("swipe") and surface.demo_active
			and is_equal_approx(surface.swipe_budget, budget_before_wrong))
		events.clear()
		# Correct immediately in the same held gesture. One full fast sweep maps to
		# the entire shipping phase goal and parks the subject exactly once.
		surface._drag(push_finish)
		surface._release(push_finish)
		var goal_units := surface._long_push_goal_units()
		_ck("%s one full sweep emits its complete goal exactly once" % push_context,
			_paid_count("swipe") == 1
			and is_equal_approx(_paid_total("swipe"), goal_units)
			and is_equal_approx(surface.widget_fill, 1.0))
		_ck("%s full sweep parks mover at destination" % push_context,
			surface._long_push_position(surface.widget_fill).distance_to(push_finish) < 1.0)
		surface.accept_completion()
		_ck("%s completion holds mover at destination" % push_context,
			surface.completion_accepted
			and surface._long_push_position(surface.widget_fill).distance_to(push_finish) < 1.0)

	# Authored traces are ordered start-to-finish journeys. One traversal maps to
	# the actual phase goal; misses/reverse scrubs cannot bank or exhaust budget.
	var trace_midpoints: Array[Vector2] = []
	for trace_context: String in [
		"trace_chef", "trace_ballerina", "trace_doctor", "trace_magician",
	]:
		events.clear()
		surface.configure("swipe", Color.WHITE, 1, trace_context)
		var trace_geometry_inside := true
		for trace_sample in range(17):
			trace_geometry_inside = trace_geometry_inside and shipping_bounds.has_point(
				surface._trace_demo_point(float(trace_sample) / 16.0))
		_ck("%s authored corridor stays inside shipping card" % trace_context,
			trace_geometry_inside)
		trace_midpoints.append(surface._trace_demo_point(0.25))
		var off_start := Vector2(8.0, 12.0)
		var off_end := Vector2(105.0, 12.0)
		var trace_budget_before := surface.swipe_budget
		surface._press(off_start)
		surface._drag(off_end)
		surface._release(off_end)
		_ck("%s off-object scrub records and pays nothing" % trace_context,
			not _paid("swipe") and surface.trace_points.is_empty()
			and surface.demo_active
			and is_equal_approx(surface.swipe_budget, trace_budget_before))
		events.clear()
		var trace_start := surface._trace_demo_point(0.0)
		surface._press(trace_start)
		for trace_sample in range(1, 3):
			surface._drag(surface._trace_demo_point(float(trace_sample) * 0.05))
		surface._release(surface._trace_demo_point(0.10))
		var trace_goal := surface._trace_goal_units()
		_ck("%s ten-percent sample advances only ten percent" % trace_context,
			is_equal_approx(surface.trace_journey, 0.10)
			and is_equal_approx(_paid_total("swipe"), trace_goal * 0.10)
			and surface.widget_fill < 0.11
			and is_equal_approx(surface.swipe_budget, trace_budget_before))
		events.clear()
		surface._press(surface._trace_demo_point(0.10))
		surface._drag(surface._trace_demo_point(0.05))
		surface._release(surface._trace_demo_point(0.05))
		_ck("%s reverse scrub pays zero, preserves prefix, and rehints" % trace_context,
			not _paid("swipe") and is_equal_approx(surface.trace_journey, 0.10)
			and surface.demo_active)
		events.clear()
		surface._press(surface._trace_demo_point(0.10))
		surface._drag(surface._trace_demo_point(0.15))
		surface._release(surface._trace_demo_point(0.15))
		_ck("%s lift-and-resume continues from the retained endpoint" % trace_context,
			is_equal_approx(surface.trace_journey, 0.15)
			and is_equal_approx(_paid_total("swipe"), trace_goal * 0.05))
		events.clear()
		surface.configure("swipe", Color.WHITE, 1, trace_context)
		trace_budget_before = surface.swipe_budget
		surface._press(surface._trace_demo_point(0.0))
		for trace_sample in range(1, 21):
			surface._drag(surface._trace_demo_point(float(trace_sample) / 20.0))
		surface._release(surface._trace_demo_point(1.0))
		_ck("%s one ordered traversal pays the complete phase goal" % trace_context,
			is_equal_approx(surface.trace_journey, 1.0)
			and is_equal_approx(surface.widget_fill, 1.0)
			and is_equal_approx(_paid_total("swipe"), trace_goal)
			and surface.trace_points.size() >= 10
			and is_equal_approx(surface.swipe_budget, trace_budget_before))
		var completed_total := _paid_total("swipe")
		surface._press(surface._trace_demo_point(1.0))
		surface._drag(surface._trace_demo_point(0.10))
		surface._release(surface._trace_demo_point(0.10))
		_ck("%s completed journey cannot pay a second time" % trace_context,
			is_equal_approx(_paid_total("swipe"), completed_total))
		surface.accept_completion()
	var trace_shapes_distinct := true
	for first_trace in range(trace_midpoints.size()):
		for second_trace in range(first_trace + 1, trace_midpoints.size()):
			trace_shapes_distinct = trace_shapes_distinct \
				and trace_midpoints[first_trace].distance_to(trace_midpoints[second_trace]) > 8.0
	_ck("chef frosting, ballerina ribbon, doctor bandage, and magician rope use distinct paths",
		trace_shapes_distinct)

	# PORTAL may reuse the static magician card and its isolated progress ring,
	# but the rotating subject is portal-only. The Lamba-and-hat mover is never
	# returned by the rotation path.
	events.clear()
	surface.configure("circle", Color.WHITE, 1, "crank_magician")
	var unsafe_magician_tableau := surface.widget_mover
	var stationary_portal_doorway := surface.portal_mover_texture
	var portal_rotator := surface._portal_rotating_texture()
	_ck("magician portal rotates neither tableau nor architectural doorway",
		unsafe_magician_tableau != null
		and stationary_portal_doorway != null
		and portal_rotator != unsafe_magician_tableau
		and portal_rotator != stationary_portal_doorway
		and is_zero_approx(surface._portal_doorway_rotation()))
	_ck("portal rotator is an isolated ring or the code star-field fallback",
		portal_rotator == null
		or portal_rotator.resource_path.to_lower().contains("ring"))
	_ck("portal overlay is isolated art or the code fallback remains available",
		surface.portal_overlay_texture == null
		or surface.portal_overlay_texture == surface.widget_overlay
		or surface.portal_overlay_texture.resource_path.contains("portal"))
	var portal_center := surface._portal_center()
	var portal_radius := surface._portal_radius()
	var portal_legacy_subject := Rect2(surface.size.x * 0.31, surface.size.y * 0.14,
		surface.size.x * 0.39, surface.size.y * 0.80)
	_ck("code portal geometry fits the shipping card",
		portal_center.x - portal_radius >= 0.0
		and portal_center.x + portal_radius <= surface.size.x
		and portal_center.y - portal_radius >= 0.0
		and portal_center.y + portal_radius <= surface.size.y
		and _rect_inside(shipping_bounds, surface._clean_widget_playfield_rect())
		and surface._clean_widget_playfield_rect().encloses(portal_legacy_subject))
	var portal_circle_radius := 74.0
	surface._press(portal_center + Vector2.RIGHT * portal_circle_radius)
	surface._drag(portal_center + Vector2.from_angle(0.30) * portal_circle_radius)
	surface._drag(portal_center + Vector2.from_angle(0.60) * portal_circle_radius)
	surface._release(portal_center + Vector2.from_angle(0.60) * portal_circle_radius)
	_ck("real circular portal motion advances and rotates portal state",
		_paid("circle") and absf(surface.crank_rotation) > 0.5)
	surface.set_fill(1.0)
	surface.accept_completion()
	_ck("completed portal holds fully open without swapping movers",
		surface.completion_accepted and is_equal_approx(surface.widget_fill, 1.0)
		and surface._portal_rotating_texture() != unsafe_magician_tableau
		and surface._portal_rotating_texture() != stationary_portal_doorway
		and is_zero_approx(surface._portal_doorway_rotation()))

	# Revised Racer TUNE art already owns its front wheel. Runtime installs only
	# the missing rear wheel under the rotating wrench.
	surface.configure("circle", Color.WHITE, 1, "crank_racer")
	var rear_wheel_start := surface._racer_wheel_rect(true, 0.0)
	var rear_wheel_done := surface._racer_wheel_rect(true, 1.0)
	var runtime_wheels := surface._racer_runtime_wheel_rects(1.0)
	_ck("racer tune draws only the missing rear wheel and visibly grows it",
		runtime_wheels.size() == 1
		and runtime_wheels[0].get_center().distance_to(surface._racer_rear_hub()) < 1.0
		and rear_wheel_start.size.x < rear_wheel_done.size.x * 0.4)
	_ck("racer wrench rotates at rear hub and all tune art fits card",
		surface._racer_wrench_rect().get_center().distance_to(surface._racer_rear_hub()) < 1.0
		and _rect_inside(shipping_bounds, rear_wheel_done)
		and _rect_inside(shipping_bounds,
			_rotation_safe_square(surface._racer_wrench_rect())))
	surface.set_fill(1.0)
	surface.accept_completion()
	_ck("racer tune completion holds rear install without overlaying authored front",
		surface.completion_accepted
		and surface._racer_runtime_wheel_rects(surface.widget_fill).size() == 1
		and is_equal_approx(rear_wheel_done.size.x,
			surface._racer_runtime_wheel_rects(surface.widget_fill)[0].size.x))

	# POSE / LAUNCH / SOUND CHECK are causal holds, not the same cyan disk and
	# meter. The two old static-subject cards are fully occluded before their
	# approved isolated prop animates.
	for charge_context: String in [
		"charge_ballerina", "charge_astronaut", "charge_popstar",
	]:
		events.clear()
		surface.configure("hold", Color.WHITE, 1, charge_context)
		var charge_action := surface._charge_action_rect()
		_ck("%s uses a shipping-safe causal action ROI" % charge_context,
			surface._uses_contextual_charge()
			and _rect_inside(shipping_bounds, charge_action))
		if charge_context == "charge_ballerina":
			_ck("ballerina pose clean stage covers the floating floor remnant",
				_rect_inside(shipping_bounds, surface._clean_widget_playfield_rect())
				and surface._clean_widget_playfield_rect().encloses(
					surface._charge_legacy_subject_rect()))
		else:
			_ck("%s clean patch encloses its complete old static subject" % charge_context,
				charge_action.encloses(surface._charge_legacy_subject_rect()))
		surface._press(charge_action.get_center())
		surface._release(charge_action.get_center())
		_ck("%s stationary press cannot impersonate a sustained hold" % charge_context,
			not _paid("hold"))
	surface.configure("hold", Color.WHITE, 1, "charge_astronaut")
	_ck("astronaut launch uses the approved isolated rocket",
		surface.charge_astronaut_texture != null
		and surface.charge_astronaut_texture.resource_path.ends_with("goal_astronaut.png"))
	_ck("rocket completion rises materially above its ignition position",
		surface._charge_rocket_center(1.0).y
			< surface._charge_rocket_center(0.0).y - surface.size.y * 0.20)
	surface.configure("hold", Color.WHITE, 1, "charge_popstar")
	_ck("popstar sound check uses the approved isolated microphone",
		surface.charge_popstar_texture != null
		and surface.charge_popstar_texture.resource_path.ends_with("goal_popstar.png"))

	# Six crank phases now have diegetic object motion. Rejected full-tableau
	# movers are never selected for ballerina/candy/doctor, while clean isolated
	# whisk, valve, and microphone props may be used in their local scene.
	for crank_context: String in [
		"crank_chef", "crank_ballerina", "crank_candymaker",
		"crank_doctor", "crank_astronaut", "crank_popstar",
	]:
		surface.configure("circle", Color.WHITE, 1, crank_context)
		_ck("%s contextual action and clean field fit shipping card" % crank_context,
			surface._uses_contextual_crank()
			and _rect_inside(shipping_bounds, surface._crank_action_rect())
			and _rect_inside(shipping_bounds, surface._clean_widget_playfield_rect()))
		if crank_context != "crank_popstar":
			_ck("%s clean field encloses every old subject fragment" % crank_context,
				surface._clean_widget_playfield_rect().encloses(
					surface._crank_legacy_subject_rect()))
		var should_use_isolated := crank_context in [
			"crank_chef", "crank_astronaut", "crank_popstar",
		]
		_ck("%s never falls back to a whole-tableau spinner" % crank_context,
			surface._contextual_crank_uses_mover() == should_use_isolated)

	# Shipping-card geometry audit. These are the actual 392x232 dimensions used
	# by OperaCareerWorld2D; active hit areas, movers, and demo endpoints must all
	# remain visible on the small Android target.
	surface.configure("clue_board", Color.WHITE)
	var clue_geometry_inside := _rect_inside(shipping_bounds, surface._clue_token_rect())
	for clue_slot in range(OperaGestureSurface.CLUE_BOARD_COUNT):
		clue_geometry_inside = clue_geometry_inside and _rect_inside(
			shipping_bounds, surface._clue_target_rect(clue_slot).grow(24.0))
	for clue_demo_time: float in [0.0, 1.60]:
		clue_geometry_inside = clue_geometry_inside and shipping_bounds.has_point(
			_pose_point(_pose_at(surface, clue_demo_time)))
	_ck("shipping clue token, targets, and demo stay inside card", clue_geometry_inside)

	surface.configure("crown_chest", Color.WHITE)
	var crown_geometry_inside := _rect_inside(shipping_bounds,
		surface._crown_handle_rect().grow(22.0))
	for crown_demo_time: float in [0.0, 1.0]:
		crown_geometry_inside = crown_geometry_inside and shipping_bounds.has_point(
			_pose_point(_pose_at(surface, crown_demo_time)))
	_ck("shipping crown handle and demo stay inside card", crown_geometry_inside)

	surface.configure("garden_plant", Color.WHITE)
	var garden_geometry_inside := _rect_inside(shipping_bounds, surface._garden_seed_rect())
	for garden_hole in range(OperaGestureSurface.GARDEN_HOLES.size()):
		var hole_center := surface._garden_hole_point(garden_hole)
		garden_geometry_inside = garden_geometry_inside and _rect_inside(
			shipping_bounds, Rect2(hole_center - Vector2.ONE * 28.0, Vector2.ONE * 56.0))
	for garden_demo_time: float in [0.0, 1.55]:
		garden_geometry_inside = garden_geometry_inside and shipping_bounds.has_point(
			_pose_point(_pose_at(surface, garden_demo_time)))
	_ck("shipping garden seed, holes, and demo stay inside card", garden_geometry_inside)

	surface.configure("magic_cabinet", Color.WHITE)
	var cabinet_base_handle := surface._cabinet_handle_rect()
	var cabinet_pulled_handle := Rect2(
		cabinet_base_handle.position + Vector2.DOWN * surface._cabinet_required_travel(),
		cabinet_base_handle.size)
	var cabinet_geometry_inside := _rect_inside(shipping_bounds,
		cabinet_base_handle.grow(22.0)) and _rect_inside(shipping_bounds, cabinet_pulled_handle)
	for cabinet_demo_time: float in [0.0, 1.65]:
		cabinet_geometry_inside = cabinet_geometry_inside and shipping_bounds.has_point(
			_pose_point(_pose_at(surface, cabinet_demo_time)))
	_ck("shipping cabinet handle, pull, and demo stay inside card", cabinet_geometry_inside)

	var every_target_inside := true
	for target_context: String in [
		"target_chef", "target_candymaker", "target_farmer",
		"target_astronaut", "target_boxer",
	]:
		surface.configure("tap", Color.WHITE, 1, target_context)
		var target_reach := maxf(46.0, minf(surface.size.x, surface.size.y) * 0.15)
		for target_index in range(surface._target_anchor_count()):
			var anchor := surface._target_anchor_point(target_index)
			every_target_inside = every_target_inside and _rect_inside(
				shipping_bounds, surface._target_piece_rect(target_index))
			every_target_inside = every_target_inside and _rect_inside(
				shipping_bounds, Rect2(anchor - Vector2.ONE * target_reach,
					Vector2.ONE * target_reach * 2.0))
			every_target_inside = every_target_inside and shipping_bounds.has_point(
				_pose_point(_pose_at(surface, 1.0)))
			if target_context == "target_candymaker":
				var recipient := surface._candymaker_recipient_rect(target_index)
				every_target_inside = every_target_inside \
					and _rect_inside(shipping_bounds, recipient) \
					and recipient.get_center().distance_to(anchor) \
						< surface._target_piece_rect(target_index).size.x * 0.20
	_ck("all shipping target pieces, hit areas, and demos stay inside card",
		every_target_inside)
	surface.configure("tap", Color.WHITE, 1, "target_candymaker")
	_ck("Candymaker SHARE exposes six recipient hands behind six candy anchors",
		surface._target_anchor_count() == 6)
	surface.configure("tap", Color.WHITE, 1, "target_farmer")
	_ck("Farmer PICNIC exposes one snack anchor for each of three visible piggies",
		surface._target_anchor_count() == 3)

	surface.configure("hold", Color.WHITE, 1, "nursery_feed")
	var nursery_geometry_inside := true
	for feed_fill: float in [0.0, 0.18, 0.48, 0.82, 1.0]:
		surface.set_fill(feed_fill)
		nursery_geometry_inside = nursery_geometry_inside and _rect_inside(
			shipping_bounds,
			_rotation_safe_square(surface._nursery_feed_bottle_rect(true)))
	for baby_index in range(3):
		var baby_center := surface._nursery_baby_center(baby_index)
		var baby_side := minf(surface.size.x, surface.size.y) * 0.29
		nursery_geometry_inside = nursery_geometry_inside and _rect_inside(
			shipping_bounds, Rect2(baby_center - Vector2.ONE * baby_side * 0.5,
				Vector2.ONE * baby_side))
	nursery_geometry_inside = nursery_geometry_inside and shipping_bounds.has_point(
		_pose_point(_pose_at(surface, 0.0)))
	surface.configure("swipe", Color.WHITE, 1, "nursery_bedtime")
	surface.swipe_dir = Vector2.DOWN
	for crib_index in range(3):
		nursery_geometry_inside = nursery_geometry_inside and _rect_inside(
			shipping_bounds, surface._nursery_bedtime_crib_rect(crib_index)) \
			and _rect_inside(shipping_bounds,
				surface._nursery_bedtime_grab_rect(crib_index))
		var bedtime_grab := surface._nursery_bedtime_grab_point(crib_index)
		nursery_geometry_inside = nursery_geometry_inside \
			and shipping_bounds.has_point(bedtime_grab) \
			and shipping_bounds.has_point(bedtime_grab + Vector2.DOWN \
				* surface._nursery_bedtime_required_travel())
		surface.nursery_blanket_progress[crib_index] = 0.0
		var folded_bottom := surface._nursery_blanket_bottom(crib_index)
		surface.nursery_blanket_progress[crib_index] = 1.0
		var tucked_bottom := surface._nursery_blanket_bottom(crib_index)
		surface.nursery_blanket_progress[crib_index] = 0.0
		nursery_geometry_inside = nursery_geometry_inside \
			and tucked_bottom > folded_bottom + surface.size.y * 0.10 \
			and surface._nursery_blanket_top(crib_index) \
				> surface._nursery_baby_center(crib_index).y - surface.size.y * 0.04
	for bedtime_demo_time: float in [0.0, 1.85]:
		nursery_geometry_inside = nursery_geometry_inside and shipping_bounds.has_point(
			_pose_point(_pose_at(surface, bedtime_demo_time)))
	surface.configure("tap", Color.WHITE, 1, "nursery_burp")
	for pat_progress: float in [0.0, 1.0]:
		var hand := surface._nursery_burp_hand_point(pat_progress)
		nursery_geometry_inside = nursery_geometry_inside and _rect_inside(
			shipping_bounds, Rect2(hand - Vector2.ONE * 33.0, Vector2.ONE * 66.0))
	nursery_geometry_inside = nursery_geometry_inside and shipping_bounds.has_point(
		_pose_point(_pose_at(surface, 1.0)))
	_ck("shipping nursery babies, bottle, cribs, pat hand, and demos fit card",
		nursery_geometry_inside)

	surface.configure("hold", Color.WHITE, 1, "magic_vanish")
	var vanish_geometry_inside := true
	for vanish_progress: float in [0.0, 0.58, 0.72, 1.0]:
		vanish_geometry_inside = vanish_geometry_inside and _rect_inside(
			shipping_bounds,
			_rotation_safe_square(surface._magic_vanish_hat_rect(vanish_progress)))
		vanish_geometry_inside = vanish_geometry_inside and _rect_inside(
			shipping_bounds,
			_rotation_safe_square(surface._magic_vanish_wand_rect(vanish_progress)))
		vanish_geometry_inside = vanish_geometry_inside and _rect_inside(
			shipping_bounds, surface._magic_vanish_reveal_rect(vanish_progress))
	vanish_geometry_inside = vanish_geometry_inside and shipping_bounds.has_point(
		_pose_point(_pose_at(surface, 1.2)))
	_ck("shipping vanish hat, wand, reveal, and demo remain fully inside card",
		vanish_geometry_inside)
	surface.size = Vector2(852, 560)
	center = surface.size * 0.5

	# Detective evidence is a three-step object match. Stationary or mismatched
	# releases return the same live token and never trickle scalar progress.
	events.clear()
	surface.configure("clue_board", Color.WHITE)
	var clue_home := surface._clue_home_point()
	var clue_left := surface._clue_target_rect(0).get_center()
	var clue_middle := surface._clue_target_rect(1).get_center()
	var clue_right := surface._clue_target_rect(2).get_center()
	_ck("clue silhouettes follow approved horizontal paw-feather-ribbon order",
		clue_left.x < clue_middle.x and clue_middle.x < clue_right.x
		and is_equal_approx(clue_left.y, clue_middle.y)
		and is_equal_approx(clue_middle.y, clue_right.y))
	surface._press(Vector2(5.0, 5.0))
	surface._release(Vector2(5.0, 5.0))
	_ck("outside clue-board press pays zero",
		surface.clue_index == 0 and not _paid("clue_board"))
	surface._press(clue_home)
	surface._release(clue_home)
	surface._clue_tick(0.40)
	_ck("stationary clue token returns home with zero progress",
		surface.clue_index == 0 and not _paid("clue_board")
		and surface.clue_token_pos.distance_to(clue_home) < 1.0)
	var wrong_clue_target := surface._clue_target_rect(1).get_center()
	surface._press(clue_home)
	surface._drag(wrong_clue_target)
	surface._release(wrong_clue_target)
	surface._clue_tick(0.40)
	_ck("mismatched clue returns and replays without payout",
		surface.clue_index == 0 and not _paid("clue_board") and surface.demo_active
		and surface.clue_token_pos.distance_to(clue_home) < 1.0)
	for clue_index in range(OperaGestureSurface.CLUE_BOARD_COUNT):
		var matching_clue_target := surface._clue_target_rect(clue_index).get_center()
		surface._press(surface._clue_home_point())
		surface._drag(matching_clue_target)
		surface._release(matching_clue_target)
	_ck("three sequential clue matches persist and pay exactly three",
		surface.clue_complete
		and surface.clue_index == OperaGestureSurface.CLUE_BOARD_COUNT
		and _paid_count("clue_board") == OperaGestureSurface.CLUE_BOARD_COUNT)

	# The crown chest is one generous diegetic target and remains open.
	events.clear()
	surface.configure("crown_chest", Color.WHITE)
	surface._press(Vector2(8.0, 8.0))
	surface._release(Vector2(8.0, 8.0))
	_ck("outside crown-chest tap is a zero-progress rehint",
		not surface.crown_opened and not _paid("crown_chest") and surface.demo_active)
	var crown_handle := surface._crown_handle_rect().get_center()
	surface._press(crown_handle)
	surface._release(crown_handle)
	surface._crown_tick(0.50)
	surface._press(crown_handle)
	surface._release(crown_handle)
	_ck("crown handle opens once and holds its reveal",
		surface.crown_opened and surface.crown_open_t > 0.9
		and _paid_count("crown_chest") == 1)

	# Five planting holes accept either the carried seed or an accessible direct
	# tap. A seed dropped elsewhere simply returns; there is no fail state.
	events.clear()
	surface.configure("garden_plant", Color.WHITE)
	var seed_home := surface._garden_seed_home()
	surface._press(Vector2(5.0, 5.0))
	surface._release(Vector2(5.0, 5.0))
	_ck("outside garden press is safe and pays zero",
		surface.garden_planted == 0 and not _paid("garden_plant"))
	surface._press(seed_home)
	surface._release(seed_home)
	_ck("stationary seed drop plants nothing and pays zero",
		surface.garden_planted == 0 and not _paid("garden_plant")
		and surface.garden_seed_pos.distance_to(seed_home) < 1.0)
	for hole_index in range(OperaGestureSurface.GARDEN_HOLES.size()):
		var hole := surface._garden_hole_point(hole_index)
		surface._press(hole)
		surface._release(hole)
	surface._garden_tick(0.60)
	var every_sprout_growing := true
	for growth: float in surface.garden_growth:
		every_sprout_growing = every_sprout_growing and growth > 0.5
	_ck("five garden holes pay once each and animate five sprouts",
		surface.garden_planted == OperaGestureSurface.GARDEN_HOLES.size()
		and _paid_count("garden_plant") == OperaGestureSurface.GARDEN_HOLES.size()
		and every_sprout_growing)

	# Cabinet motion is displacement from the handle, not tap time or scrub
	# distance. Only a direct downward pull crosses the reveal threshold.
	events.clear()
	surface.configure("magic_cabinet", Color.WHITE)
	var cabinet_handle := surface._cabinet_handle_rect().get_center()
	surface._press(Vector2(5.0, 5.0))
	surface._release(Vector2(5.0, 5.0))
	_ck("outside cabinet press is a zero-progress rehint",
		not surface.cabinet_complete and not _paid("magic_cabinet"))
	surface._press(cabinet_handle)
	surface._release(cabinet_handle)
	_ck("stationary cabinet handle press pays zero",
		not surface.cabinet_complete and not _paid("magic_cabinet"))
	surface._press(cabinet_handle)
	var sideways_handle := cabinet_handle + Vector2(surface._cabinet_required_travel() * 1.5, 3.0)
	surface._drag(sideways_handle)
	surface._release(sideways_handle)
	_ck("sideways cabinet scrub cannot become opening travel",
		not surface.cabinet_complete and not _paid("magic_cabinet")
		and is_zero_approx(surface.cabinet_open_t))
	surface._press(cabinet_handle)
	var cabinet_finish := cabinet_handle \
		+ Vector2.DOWN * (surface._cabinet_required_travel() + 8.0)
	surface._drag(cabinet_finish)
	surface._release(cabinet_finish)
	surface._cabinet_tick(0.50)
	surface._press(cabinet_handle)
	surface._release(cabinet_handle)
	_ck("direct cabinet pull opens once and holds reveal",
		surface.cabinet_complete and surface.cabinet_open_t >= 0.99
		and _paid_count("magic_cabinet") == 1)

	# Five career placement scenes use deterministic one-use anchors. Painter is
	# intentionally the exception: her canvas keeps free stamping at the finger.
	for target_context: String in [
		"target_chef", "target_candymaker", "target_farmer",
		"target_astronaut", "target_boxer",
	]:
		events.clear()
		surface.configure("tap", Color.WHITE, 1, target_context)
		var expected_pieces := surface._target_anchor_count()
		if target_context == "target_farmer":
			var picnic_piece_paths: Dictionary = {}
			for picnic_piece: Texture2D in surface.target_piece_textures:
				if picnic_piece != null:
					picnic_piece_paths[picnic_piece.resource_path] = true
			_ck("Farmer PICNIC uses carrot, corn, and pumpkin once each",
				expected_pieces == 3 and picnic_piece_paths.size() == 3)
		surface._press(Vector2(5.0, 5.0))
		surface._release(Vector2(5.0, 5.0))
		_ck("%s stray tap pays zero" % target_context,
			not _paid("tap") and surface._target_next_unplaced() == 0)
		for piece_index in range(expected_pieces):
			var anchor := surface._target_anchor_point(piece_index)
			surface._press(anchor)
			surface._release(anchor)
		var first_anchor := surface._target_anchor_point(0)
		surface._press(first_anchor)
		surface._release(first_anchor)
		_ck("%s accepts each authored anchor once" % target_context,
			surface._target_next_unplaced() == -1
			and _paid_count("tap") == expected_pieces)
	events.clear()
	surface.configure("tap", Color.WHITE, 1, "target_painter")
	for free_point: Vector2 in [Vector2(91.0, 107.0), Vector2(681.0, 421.0)]:
		surface._press(free_point)
		surface._release(free_point)
	_ck("Painter preserves free stamps instead of authored anchors",
		not surface._uses_anchored_targets() and surface.tap_marks.size() == 2
		and _paid_count("tap") == 2)

	# Causal nursery/magic contexts expose their object motion directly through
	# the same fill state owned by the career world.
	events.clear()
	surface.configure("hold", Color.WHITE, 1, "nursery_feed")
	_ck("nursery feed selects the approved 256px bottle asset branch",
		surface._nursery_bottle_art_ready()
		and surface.nursery_bottle_texture != null
		and surface.nursery_bottle_texture.resource_path \
			== OperaGestureSurface.NURSERY_BOTTLE_PATH
		and surface.nursery_bottle_texture.get_size() == Vector2(256.0, 256.0))
	var bottle_home_pose := surface._nursery_feed_bottle_pose(false)
	surface._press(_pose_point(_pose_at(surface, 0.0)))
	_ck("stationary feed press arms bottle but pays no instant progress",
		surface.held and not _paid("hold"))
	surface.set_fill(0.48)
	var bottle_feed_pose := surface._nursery_feed_bottle_pose(true)
	var bottle_home_position: Vector2 = bottle_home_pose["position"]
	var bottle_feed_position: Vector2 = bottle_feed_pose["position"]
	_ck("feed bottle travels, tilts, and visibly drains toward a baby",
		bottle_feed_position.distance_to(bottle_home_position) > 80.0
		and float(bottle_feed_pose["rotation"]) < -0.5
		and float(bottle_feed_pose["remaining"]) < 0.55)
	surface._release(bottle_feed_position)
	events.clear()
	surface.configure("swipe", Color.WHITE, 1, "nursery_bedtime")
	var bedtime_outside := Vector2(10.0, 10.0)
	surface._press(bedtime_outside)
	surface._drag(bedtime_outside + Vector2.DOWN * 120.0)
	surface._release(bedtime_outside + Vector2.DOWN * 120.0)
	_ck("outside bedtime swipe cannot tuck any blanket",
		not _paid("swipe") and surface._nursery_bedtime_next_blanket() == 0)
	var first_blanket_grab := surface._nursery_bedtime_grab_point(0)
	surface._press(first_blanket_grab)
	surface._release(first_blanket_grab)
	_ck("stationary bedtime touch pays zero and leaves blanket folded",
		not _paid("swipe") and is_zero_approx(surface.nursery_blanket_progress[0]))
	surface._press(first_blanket_grab)
	surface._drag(first_blanket_grab + Vector2.UP * 70.0)
	surface._release(first_blanket_grab + Vector2.UP * 70.0)
	_ck("wrong-direction bedtime drag pays zero and gently rehints",
		not _paid("swipe") and is_zero_approx(surface.nursery_blanket_progress[0])
		and surface.demo_active)
	for blanket_index in range(3):
		var blanket_grab := surface._nursery_bedtime_grab_point(blanket_index)
		var blanket_finish := blanket_grab + Vector2.DOWN \
			* (surface._nursery_bedtime_required_travel() + 3.0)
		surface._press(blanket_grab)
		surface._drag(blanket_finish)
		surface._release(blanket_finish)
		var tucked_persist := true
		for prior_blanket in range(blanket_index + 1):
			tucked_persist = tucked_persist and surface.nursery_blankets_tucked[prior_blanket] \
				and is_equal_approx(surface.nursery_blanket_progress[prior_blanket], 1.0)
		_ck("bedtime blanket %d tucks once and persists" % blanket_index,
			tucked_persist and _paid_count("swipe") == blanket_index + 1)
		if blanket_index < 2:
			var next_blanket_pose := _pose_at(surface, 0.0)
			_ck("bedtime demo advances to blanket %d" % (blanket_index + 1),
				_pose_point(next_blanket_pose).distance_to(
					surface._nursery_bedtime_grab_point(blanket_index + 1)) < 1.0)
	_ck("three exact blanket payouts finish bedtime with faces still above cloth",
		surface._nursery_bedtime_next_blanket() == -1
		and _paid_count("swipe") == 3 and is_equal_approx(_paid_total("swipe"), 3.0)
		and surface._nursery_blanket_top(1) > surface._nursery_baby_center(1).y \
			- surface.size.y * 0.04)
	events.clear()
	surface.configure("tap", Color.WHITE, 1, "nursery_burp")
	var pat_point := surface._nursery_burp_hand_point(1.0)
	surface._press(pat_point)
	surface._release(pat_point)
	_ck("burp tap drives a pat/reaction pulse without timing payout",
		surface.nursery_burp_pat_t > 0.4 and _paid_count("tap") == 1)
	events.clear()
	surface.configure("hold", Color.WHITE, 1, "magic_vanish")
	var vanish_layers_loaded := surface.magic_vanish_hat_texture != null \
		and surface.magic_vanish_wand_texture != null \
		and surface.magic_vanish_reveal_texture != null
	var vanish_sources_waiting_for_import := FileAccess.file_exists(
		"res://assets/opera/worlds/widgets/widget_magic_vanish_hat.png") \
		and FileAccess.file_exists(
			"res://assets/opera/worlds/widgets/widget_magic_vanish_wand.png") \
		and FileAccess.file_exists(
			"res://assets/opera/worlds/widgets/widget_magic_vanish_reveal.png")
	_ck("magic vanish binds delivered layers or retains fallback before import",
		vanish_layers_loaded or vanish_sources_waiting_for_import)
	var vanish_hat_start := surface._magic_vanish_hat_position(0.0)
	var vanish_hat_cover := surface._magic_vanish_hat_position(0.70)
	var vanish_wand_start := surface._magic_vanish_wand_position(0.0)
	var vanish_wand_cast := surface._magic_vanish_wand_position(0.70)
	_ck("vanish hat and wand travel as separate causal objects",
		vanish_hat_start.distance_to(vanish_hat_cover) > surface.size.x * 0.16
		and vanish_wand_start.distance_to(vanish_wand_cast) > surface.size.y * 0.08
		and not is_equal_approx(surface._magic_vanish_wand_rotation(0.0),
			surface._magic_vanish_wand_rotation(0.70)))
	_ck("bunny-fish reveal stays hidden until hat contact",
		is_zero_approx(surface._magic_vanish_reveal_amount(0.50))
		and surface._magic_vanish_reveal_amount(0.70) > 0.0)
	surface._press(center)
	surface.set_fill(0.70)
	_ck("magic vanish uses its causal hat scene, not charge-meter art",
		surface._is_magic_vanish_context() and surface.widget_mover == null
		and surface.widget_overlay == null and not _paid("hold"))
	surface._release(center)
	surface.set_fill(1.0)
	surface.accept_completion()
	_ck("magic vanish completion holds the authored full reveal",
		is_equal_approx(surface._magic_vanish_reveal_amount(surface.widget_fill), 1.0)
		and surface.completion_accepted)

	# Four-pad dance is a true call-and-response state machine. A wrong tap
	# preserves the correct prefix and replays only the remaining suffix.
	events.clear()
	surface.configure("dance_sequence", Color.WHITE)
	_ck("dance defaults to the approved ballerina context",
		surface.visual_context == "lanes_ballerina" and surface.widget_backdrop != null)
	for tick in range(28):
		surface._dance_tick(0.15)
	_ck("dance demonstrates before accepting input",
		surface.dance_listening and surface.dance_input_index == 0)
	var dance_pose := _pose_at(surface, 1.25)
	_ck("dance rehint points to the next real floor pad",
		_pose_point(dance_pose).distance_to(surface._dance_pad_rect(
			int(OperaGestureSurface.DANCE_SEQUENCE[0])).get_center()) < 1.0
		and bool(dance_pose.get("pressing", false)))
	var first_dance_pad := int(OperaGestureSurface.DANCE_SEQUENCE[0])
	surface._press(surface._dance_pad_rect(first_dance_pad).get_center())
	surface._release(surface._dance_pad_rect(first_dance_pad).get_center())
	_ck("first correct dance pad banks a prefix without scalar payout",
		surface.dance_input_index == 1 and not _paid("dance_sequence"))
	var expected_second := int(OperaGestureSurface.DANCE_SEQUENCE[1])
	var wrong_pad := (expected_second + 1) % 4
	surface._press(surface._dance_pad_rect(wrong_pad).get_center())
	surface._release(surface._dance_pad_rect(wrong_pad).get_center())
	_ck("wrong dance pad preserves prefix and gently re-shows only suffix",
		not _paid("dance_sequence") and surface.dance_input_index == 1
		and not surface.dance_listening and surface.demo_active)
	for tick in range(28):
		surface._dance_tick(0.15)
	_ck("suffix replay resumes listening at the preserved prefix",
		surface.dance_listening and surface.dance_input_index == 1)
	events.clear()
	for step in range(1, OperaGestureSurface.DANCE_SEQUENCE.size()):
		var pad := int(OperaGestureSurface.DANCE_SEQUENCE[step])
		var pad_center := surface._dance_pad_rect(pad).get_center()
		surface._press(pad_center)
		surface._release(pad_center)
		if step < OperaGestureSurface.DANCE_SEQUENCE.size() - 1:
			_ck("dance prefix %d is state, not scalar payout" % step,
				not _paid("dance_sequence"))
	_ck("exact dance phrase completes once",
		surface.dance_complete and _paid_count("dance_sequence") == 1)

	# Candies move slowly but never expire. Only a matching silhouette changes
	# the deterministic queue; a wrong bin resets the same piece.
	events.clear()
	surface.configure("candy_sort", Color.WHITE)
	_ck("candy sort binds its three-bin authored card",
		surface.visual_context == "lanes_candymaker" and surface.widget_backdrop != null
		and surface.candy_type == int(OperaGestureSurface.CANDY_SEQUENCE[0]))
	var candy_start_type := surface.candy_type
	for tick in range(160):
		surface._candy_tick(0.10)
	_ck("missed candy safely loops without queue progress",
		surface.candy_loops > 0 and surface.candy_piece_index == 0
		and surface.candy_type == candy_start_type and not _paid("candy_sort"))
	var wrong_bin := (surface.candy_type + 1) % 3
	var candy_start := surface.candy_position
	var wrong_target := surface._candy_bin_rect(wrong_bin).get_center()
	surface._press(candy_start)
	surface._drag(wrong_target)
	surface._release(wrong_target)
	_ck("wrong candy bin returns the same piece with no payout",
		surface.candy_sorted == 0 and surface.candy_piece_index == 0
		and surface.candy_type == candy_start_type and not _paid("candy_sort")
		and surface.demo_active)
	var candy_demo_start := _pose_point(_pose_at(surface, 0.0))
	var candy_demo_end := _pose_point(_pose_at(surface, 1.80))
	_ck("candy rehint carries the live piece to its matching bin",
		candy_demo_start.distance_to(surface.candy_position) < 1.0
		and candy_demo_end.distance_to(surface._candy_bin_rect(surface.candy_type).get_center()) < 1.0)
	events.clear()
	for sorted_piece in range(OperaGestureSurface.CANDY_SEQUENCE.size()):
		var expected_type := surface.candy_type
		var piece_center := surface.candy_position
		var matching_bin := surface._candy_bin_rect(expected_type).get_center()
		surface._press(piece_center)
		surface._drag(matching_bin)
		surface._release(matching_bin)
		if sorted_piece == 0:
			_ck("first match advances to the deterministic second piece",
				surface.candy_type == int(OperaGestureSurface.CANDY_SEQUENCE[1]))
	_ck("six valid candy matches complete with six payouts",
		surface.candy_complete and surface.candy_sorted == OperaGestureSurface.CANDY_SEQUENCE.size()
		and _paid_count("candy_sort") == OperaGestureSurface.CANDY_SEQUENCE.size())

	# Paint completion comes from newly covered grid cells. The owner's scalar
	# fill and stationary tap mashing are deliberately irrelevant.
	events.clear()
	surface.configure("paint_reveal", Color.WHITE)
	surface.set_fill(1.0)
	_ck("paint reveal binds the finished sunrise art",
		surface.visual_context == "trace_painter" and surface.paint_reveal_texture != null)
	var paint_canvas := surface._paint_canvas_rect()
	for tap in range(18):
		var tap_point := paint_canvas.position + paint_canvas.size * Vector2(
			(float(tap % 6) + 0.5) / 6.0, (float(tap / 6) + 0.5) / 3.0)
		surface._press(tap_point)
		surface._release(tap_point)
	_ck("stationary paint mashing uncovers no cells",
		surface.paint_covered == 0 and not surface.paint_complete
		and not _paid("paint_reveal"))
	for row in range(OperaGestureSurface.PAINT_GRID_ROWS):
		if surface.paint_complete:
			break
		var y := paint_canvas.position.y + paint_canvas.size.y \
			* (float(row) + 0.5) / float(OperaGestureSurface.PAINT_GRID_ROWS)
		var stroke_start := Vector2(paint_canvas.position.x + 2.0, y)
		var stroke_end := Vector2(paint_canvas.end.x - 2.0, y)
		surface._press(stroke_start)
		surface._drag(stroke_end)
		surface._release(stroke_end)
	_ck("real strokes complete from coarse coverage state",
		surface.paint_complete and surface.paint_covered >= surface._paint_required_cells()
		and surface.paint_coverage() >= OperaGestureSurface.PAINT_REQUIRED_COVERAGE)
	_ck("paint completion emits exactly one whole-picture payout",
		_paid_count("paint_reveal") == 1)
	var paint_demo := _pose_at(surface, 1.1)
	_ck("paint wordless demo stays on the actual canvas",
		paint_canvas.has_point(_pose_point(paint_demo))
		and bool(paint_demo.get("pressing", false)))

	# Farmer feed is a release-driven lob. Carrot/corn/pumpkin cycle
	# deterministically; only the end of a valid arc pays and triggers pig chew.
	events.clear()
	surface.configure("farm_lob", Color.WHITE)
	var farm_food_paths: Dictionary = {}
	for farm_food_texture: Texture2D in surface.farm_vegetable_textures:
		farm_food_paths[farm_food_texture.resource_path] = true
	_ck("farm lob binds three distinct approved food pieces",
		surface.visual_context == "target_farmer" and surface.widget_backdrop != null
		and surface.farm_vegetable_textures.size() == 3
		and farm_food_paths.size() == 3)
	var seen_farm_foods: Dictionary = {surface.farm_food_index: true}
	var farm_anchor := surface._farm_anchor_point()
	var farm_target := surface._farm_target_center()
	var farm_demo_start := _pose_point(_pose_at(surface, 0.0))
	var farm_demo_pull := _pose_point(_pose_at(surface, 1.15))
	_ck("farm demo visibly pulls backward from the basket",
		farm_demo_start.distance_to(farm_anchor) < 1.0
		and (farm_demo_pull - farm_anchor).dot(farm_target - farm_anchor) < 0.0)
	surface._press(farm_anchor)
	surface._release(farm_anchor)
	for tick in range(12):
		surface._farm_tick(0.10)
	_ck("weak farm release loops home without progress",
		surface.farm_loops == 1 and surface.farm_landed == 0
		and surface.farm_piece_position.distance_to(farm_anchor) < 1.0
		and not _paid("farm_lob"))
	var pull_point := surface._farm_demo_pull_point()
	surface._press(farm_anchor)
	surface._drag(pull_point)
	surface._release(pull_point)
	_ck("backward farm release arms a landing but pays only after flight",
		surface.farm_flying and surface.farm_will_land and not _paid("farm_lob"))
	surface._farm_tick(OperaGestureSurface.FARM_FLIGHT_DURATION * 0.5)
	var straight_midpoint := pull_point.lerp(farm_target, 0.5)
	_ck("farm vegetable follows a visible upward arc",
		surface.farm_piece_position.y < straight_midpoint.y - 20.0)
	surface._farm_tick(OperaGestureSurface.FARM_FLIGHT_DURATION * 0.5 + 0.01)
	_ck("first landed food emits once and starts pig munch reaction",
		surface.farm_landed == 1 and _paid_count("farm_lob") == 1
		and surface.farm_last_landed_food == 0 and surface.farm_munch_t > 0.0)
	for landing in range(1, OperaGestureSurface.FARM_LOB_GOAL):
		surface._farm_tick(0.50)
		seen_farm_foods[surface.farm_food_index] = true
		var next_anchor := surface._farm_anchor_point()
		surface._press(next_anchor)
		surface._drag(surface._farm_demo_pull_point())
		surface._release(surface._farm_demo_pull_point())
		for flight_tick in range(10):
			surface._farm_tick(0.10)
	_ck("four deterministic multi-food landings complete with chew and four payouts",
		surface.farm_complete and surface.farm_landed == OperaGestureSurface.FARM_LOB_GOAL
		and _paid_count("farm_lob") == OperaGestureSurface.FARM_LOB_GOAL
		and seen_farm_foods.size() == 3 and surface.farm_munch_t > 0.0)

	# The dedicated boxing surface owns two floating gloves. Its five modes do
	# not progress themselves: only a real owned touch transition may emit work.
	var boxing_modes: Array[String] = [
		"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
	]
	var passive_boxing_safe := true
	for boxing_mode: String in boxing_modes:
		events.clear()
		boxing.configure(boxing_mode, Color.WHITE)
		for passive_tick in range(128):
			boxing._process(0.10)
		passive_boxing_safe = passive_boxing_safe \
			and boxing.landed_count() == 0 and boxing.round_index() == 0 \
			and not _paid(boxing_mode)
	_ck("all boxing modes wait indefinitely with zero passive progress",
		passive_boxing_safe)

	# A jab must travel forward from the glove's owned origin into the target.
	# Once accepted, its per-hand latch rejects drag spam until release.
	events.clear()
	boxing.configure("boxing_jab", Color.WHITE)
	var jab_finger := 7
	var jab_hand := 0
	var jab_start := boxing.glove_rest(jab_hand)
	var jab_target := boxing.active_target_position()
	boxing._handle_press(jab_finger, jab_start)
	boxing._handle_drag(jab_finger, jab_target)
	_ck("real forward glove drag banks one jab",
		boxing.landed_count() == 1 and boxing.round_index() == 1
		and _paid_count("boxing_jab") == 1)
	boxing._handle_drag(jab_finger, jab_target)
	boxing._handle_drag(jab_finger, jab_target + Vector2(2.0, 0.0))
	boxing._handle_release(jab_finger, jab_target)
	_ck("accepted jab latches and cannot duplicate before release",
		boxing.landed_count() == 1 and boxing.round_index() == 1
		and _paid_count("boxing_jab") == 1
		and boxing.touch_owner_snapshot().is_empty())

	# Friendly counter-contact is feedback only. It cannot rewind either the
	# career-owned fill synchronization or the locally accepted punch count.
	boxing.set_fill(0.25)
	var punches_before_hit := boxing.landed_count()
	var round_before_hit := boxing.round_index()
	var fill_before_hit := boxing.widget_fill
	var payouts_before_hit := _paid_count("boxing_jab")
	boxing.receive_friendly_hit()
	_ck("friendly hit is cosmetic and preserves all accepted boxing state",
		boxing.has_friendly_hit_feedback()
		and boxing.landed_count() == punches_before_hit
		and boxing.round_index() == round_before_hit
		and is_equal_approx(boxing.widget_fill, fill_before_hit)
		and _paid_count("boxing_jab") == payouts_before_hit
		and not _paid("boxing_contact") and not boxing.finished)

	# A child with one finger can operate both gloves in sequence. The guide
	# excludes the completed hand and gives the same released finger the other.
	events.clear()
	boxing.configure("boxing_guide", Color.WHITE)
	var solo_finger := 12
	for guide_hand in range(2):
		var guide_start := boxing.glove_rest(guide_hand)
		var guide_target := boxing.guide_target_position(guide_hand)
		boxing._handle_press(solo_finger, guide_start)
		boxing._handle_drag(solo_finger, guide_target)
		boxing._handle_release(solo_finger, guide_target)
	_ck("one finger can finish both floating-glove guide punches",
		boxing.landed_count() == 2 and boxing.round_index() == 2
		and _paid_count("boxing_guide") == 2
		and boxing.touch_owner_snapshot().is_empty() and not boxing.held)

	# Two simultaneous touches must own different hands. Releasing one finger
	# leaves the other owner live and draggable until that exact finger releases.
	events.clear()
	boxing.configure("boxing_jab", Color.WHITE)
	var left_finger := 21
	var right_finger := 22
	var left_rest := boxing.glove_rest(0)
	var right_rest := boxing.glove_rest(1)
	boxing._handle_press(left_finger, left_rest)
	boxing._handle_press(right_finger, right_rest)
	var dual_owners := boxing.touch_owner_snapshot()
	_ck("two touches own two distinct floating gloves",
		dual_owners.size() == 2 and int(dual_owners.get(left_finger, -1)) == 0
		and int(dual_owners.get(right_finger, -1)) == 1)
	boxing._handle_release(left_finger, left_rest)
	var isolated_owner := boxing.touch_owner_snapshot()
	var right_drag := right_rest + Vector2(0.0, -42.0)
	boxing._handle_drag(right_finger, right_drag)
	_ck("releasing one glove preserves the other finger owner",
		isolated_owner.size() == 1 and not isolated_owner.has(left_finger)
		and int(isolated_owner.get(right_finger, -1)) == 1 and boxing.held
		and boxing.glove_positions[1].distance_to(right_drag) < 1.0)
	boxing._handle_release(right_finger, right_drag)
	_ck("last owned glove release clears held state",
		boxing.touch_owner_snapshot().is_empty() and not boxing.held)

	# Desktop/headless fallback uses the same forward travel, while its explicit
	# sentinel remains a real owner if a touch arrives before mouse release.
	events.clear()
	boxing.configure("boxing_jab", Color.WHITE)
	var mouse_start := boxing.glove_rest(0)
	var mouse_target := boxing.active_target_position()
	_boxing_mouse_button(boxing, true, mouse_start)
	_boxing_mouse_motion(boxing, mouse_target)
	_boxing_mouse_button(boxing, false, mouse_target)
	_ck("mouse fallback performs the same causal forward jab",
		boxing.landed_count() == 1 and _paid_count("boxing_jab") == 1
		and boxing.touch_owner_snapshot().is_empty())
	var mouse_all_modes := boxing.landed_count() == 1 \
		and _paid_count("boxing_jab") == 1
	events.clear()
	boxing.configure("boxing_guide", Color.WHITE)
	for guide_hand in range(2):
		_boxing_mouse_button(boxing, true, boxing.glove_rest(guide_hand))
		var guide_target := boxing.guide_target_position(guide_hand)
		_boxing_mouse_motion(boxing, guide_target)
		_boxing_mouse_button(boxing, false, guide_target)
	var mouse_guide_ok := boxing.landed_count() == 2 \
		and _paid_count("boxing_guide") == 2
	_ck("mouse fallback completes the two-glove guide", mouse_guide_ok)
	mouse_all_modes = mouse_all_modes and mouse_guide_ok
	events.clear()
	boxing.configure("boxing_guard", Color.WHITE)
	for guard_round in range(3):
		var guard_hand := boxing.round_index() % 2
		_boxing_mouse_button(boxing, true, boxing.glove_rest(guard_hand))
		var guard_target := boxing.active_target_position()
		_boxing_mouse_motion(boxing, guard_target)
		boxing._process(boxing._counter_t + 0.01)
		_boxing_mouse_button(boxing, false, guard_target)
		boxing._process(0.5)
	var mouse_guard_ok := boxing.round_index() == 3 \
		and _paid_count("boxing_guard") == 3
	_ck("mouse fallback completes all soft guard counters", mouse_guard_ok)
	mouse_all_modes = mouse_all_modes and mouse_guard_ok
	events.clear()
	boxing.configure("boxing_imp", Color.WHITE)
	for imp_round in range(6):
		var imp_ticks := 0
		while not boxing.imp_is_open() and imp_ticks < 20:
			boxing._process(0.4)
			imp_ticks += 1
		if not boxing.imp_is_open():
			mouse_all_modes = false
			break
		var imp_hand := boxing.round_index() % 2
		_boxing_mouse_button(boxing, true, boxing.glove_rest(imp_hand))
		var imp_target := boxing.active_target_position()
		_boxing_mouse_motion(boxing, imp_target)
		_boxing_mouse_button(boxing, false, imp_target)
		boxing._process(0.5)
	var mouse_imp_ok := boxing.landed_count() == 6 \
		and _paid_count("boxing_imp") == 6
	_ck("mouse fallback completes the friendly imp title round", mouse_imp_ok)
	mouse_all_modes = mouse_all_modes and mouse_imp_ok
	events.clear()
	boxing.configure("boxing_belt", Color.WHITE)
	_boxing_mouse_button(boxing, true, boxing.glove_rest(0))
	var belt_target := boxing.active_target_position()
	_boxing_mouse_motion(boxing, belt_target)
	_boxing_mouse_button(boxing, false, belt_target)
	var mouse_belt_ok := boxing.landed_count() == 1 \
		and _paid_count("boxing_belt") == 1
	_ck("mouse fallback earns the belt with a forward punch", mouse_belt_ok)
	mouse_all_modes = mouse_all_modes and mouse_belt_ok
	_ck("mouse fallback can finish every dedicated boxing phase",
		mouse_all_modes and boxing.touch_owner_snapshot().is_empty())

	boxing.configure("boxing_jab", Color.WHITE)
	_boxing_mouse_button(boxing, true, boxing.glove_rest(0))
	_boxing_touch_event(boxing, 51, true, boxing.glove_rest(0))
	var mixed_owners := boxing.touch_owner_snapshot()
	_ck("mouse sentinel and touch cannot claim the same glove",
		int(mixed_owners.get(OperaBoxingSurface.MOUSE_FINGER, -1)) == 0
		and int(mixed_owners.get(51, -1)) == 1)
	_boxing_mouse_button(boxing, false, boxing.glove_rest(0))
	_ck("mouse release preserves the concurrently owned touch glove",
		boxing.touch_owner_snapshot().size() == 1
		and int(boxing.touch_owner_snapshot().get(51, -1)) == 1)
	_boxing_touch_event(boxing, 51, false, boxing.glove_rest(0))

	# Android may synthesize a mouse packet for the same touch. Once any screen
	# touch has been seen, those emulated packets and stray releases are no-ops.
	events.clear()
	boxing.configure("boxing_jab", Color.WHITE)
	var dedupe_start := boxing.glove_rest(0)
	var dedupe_target := boxing.active_target_position()
	_boxing_touch_event(boxing, 61, true, dedupe_start)
	_boxing_drag_event(boxing, 61, dedupe_target)
	var dedupe_count := boxing.landed_count()
	_boxing_mouse_button(boxing, true, boxing.glove_rest(1),
		InputEvent.DEVICE_ID_EMULATION)
	_boxing_mouse_motion(boxing, dedupe_target, InputEvent.DEVICE_ID_EMULATION)
	_boxing_mouse_button(boxing, false, dedupe_target,
		InputEvent.DEVICE_ID_EMULATION)
	_boxing_touch_event(boxing, 999, false, Vector2.ZERO)
	_ck("emulated mouse and unknown release cannot duplicate a touch punch",
		boxing.landed_count() == dedupe_count and dedupe_count == 1
		and _paid_count("boxing_jab") == 1
		and boxing.touch_owner_snapshot().size() == 1
		and boxing.touch_owner_snapshot().has(61))
	_boxing_touch_event(boxing, 61, false, dedupe_target)
	_boxing_touch_event(boxing, 61, false, dedupe_target)
	_ck("duplicate release is harmless after the real owner clears",
		boxing.touch_owner_snapshot().is_empty() and not boxing.held
		and boxing.landed_count() == 1)

	boxing.configure("boxing_jab", Color.WHITE)
	_boxing_mouse_button(boxing, true, boxing.glove_rest(0))
	boxing.configure("boxing_guard", Color.WHITE)
	_ck("phase reconfiguration clears every mouse and touch claim",
		boxing.touch_owner_snapshot().is_empty() and not boxing.held
		and boxing.glove_positions[0].distance_to(boxing.glove_rest(0)) < 1.0
		and boxing.glove_positions[1].distance_to(boxing.glove_rest(1)) < 1.0)

	# Explicit cancellation and application focus loss share the same hard reset:
	# no stale owner, latch, or displaced glove may survive a scene transition.
	events.clear()
	boxing.configure("boxing_jab", Color.WHITE)
	boxing._handle_press(31, boxing.glove_rest(0))
	boxing._handle_press(32, boxing.glove_rest(1))
	boxing.cancel_all_touches()
	_ck("boxing cancel resets both touch owners and glove rests",
		boxing.touch_owner_snapshot().is_empty() and not boxing.held
		and boxing.glove_positions[0].distance_to(boxing.glove_rest(0)) < 1.0
		and boxing.glove_positions[1].distance_to(boxing.glove_rest(1)) < 1.0)
	boxing._handle_press(41, boxing.glove_rest(0))
	boxing._handle_drag(41, boxing.glove_rest(0) + Vector2(0.0, -48.0))
	boxing._notification(NOTIFICATION_APPLICATION_FOCUS_OUT)
	_ck("boxing focus loss cancels every owned touch without progress",
		boxing.touch_owner_snapshot().is_empty() and not boxing.held
		and boxing.glove_positions[0].distance_to(boxing.glove_rest(0)) < 1.0
		and boxing.glove_positions[1].distance_to(boxing.glove_rest(1)) < 1.0
		and boxing.landed_count() == 0 and not _paid("boxing_jab"))

	call_deferred("_finish_after_render", surface, boxing)
