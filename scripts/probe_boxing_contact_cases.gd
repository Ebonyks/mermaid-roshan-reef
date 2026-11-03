extends RefCounted
## Shared by the focused runner and trusted probe_opera_2d. Exercises real
## InputEventScreenTouch/Drag objects; it never awards career/save state.

const Contact := preload("res://scripts/opera_boxing_contact.gd")
var results: Array[Dictionary] = []
var geometry_cases := 0
var flight_cases := 0
var fuzz_events := 0
var events: Array[Dictionary] = []


func check(label: String, passed: bool) -> void:
	results.append({"label": label, "passed": passed})


func run(host: Node) -> Array[Dictionary]:
	_geometry()
	var boxing := OperaBoxingSurface.new()
	boxing.size = Vector2(1280.0, 720.0)
	host.add_child(boxing)
	boxing.set_process(false)
	boxing.gesture.connect(func(kind: String, amount: float, _quality: float) -> void:
		events.append({"kind": kind, "amount": amount}))
	_flights(boxing)
	_targets(boxing)
	_ownership(boxing)
	_interruptions(boxing)
	_counter_windows(boxing)
	_complete_paths(boxing)
	_completion_feedback(boxing)
	_touch_fuzz(boxing)
	boxing.free()
	check("stress case counts are nontrivial", geometry_cases >= 14000 and flight_cases == 224)
	return results


func _geometry() -> void:
	check("tunnelling opposite moving discs meet at t=0.45",
		is_equal_approx(Contact.sweep(Vector2(-100, 0), Vector2(100, 0), 10, 10,
			Vector2(100, 0), Vector2(-100, 0), 10, 10), 0.45))
	check("tangent contact is included", is_equal_approx(Contact.sweep(Vector2(-100, 20),
		Vector2(100, 20), 10, 10, Vector2.ZERO, Vector2.ZERO, 10, 10), 0.5))
	check("near tangent miss is excluded", Contact.sweep(Vector2(-100, 20.1),
		Vector2(100, 20.1), 10, 10, Vector2.ZERO, Vector2.ZERO, 10, 10) < 0.0)
	check("end contact is included", is_equal_approx(Contact.sweep(Vector2(-100, 0),
		Vector2(-20, 0), 10, 10, Vector2.ZERO, Vector2.ZERO, 10, 10), 1.0))
	check("initial overlap and zero motion are contacts", Contact.sweep(Vector2.ZERO,
		Vector2.ZERO, 10, 10, Vector2(15, 0), Vector2(15, 0), 10, 10) == 0.0)
	check("separated stationary discs miss", Contact.sweep(Vector2.ZERO,
		Vector2.ZERO, 10, 10, Vector2(21, 0), Vector2(21, 0), 10, 10) < 0.0)
	check("growing stationary disc contacts", is_equal_approx(Contact.sweep(Vector2.ZERO,
		Vector2.ZERO, 5, 25, Vector2(30, 0), Vector2(30, 0), 10, 10), 0.75))
	check("nonfinite coordinates and negative radius are rejected",
		Contact.sweep(Vector2(NAN, 0), Vector2.ZERO, 10, 10, Vector2.ZERO, Vector2.ZERO, 10, 10) < 0.0
		and Contact.sweep(Vector2.ZERO, Vector2.ZERO, -1, 10, Vector2.ZERO, Vector2.ZERO, 10, 10) < 0.0
		and Contact.sweep(Vector2.ZERO, Vector2.ZERO, INF, 10, Vector2.ZERO, Vector2.ZERO, 10, 10) < 0.0)
	var rng := RandomNumberGenerator.new()
	rng.seed = 0xB0C531
	var static_ok := true
	var symmetry_ok := true
	var root_ok := true
	for sample in range(12000):
		var a0 := _point(rng)
		var a1 := _point(rng)
		var b0 := _point(rng)
		var b1 := _point(rng)
		var ra := rng.randf_range(1.0, 140.0)
		var rb := rng.randf_range(1.0, 140.0)
		var t := Contact.sweep(a0, a1, ra, ra, b0, b1, rb, rb)
		# Independent nearest-point oracle (not a second quadratic solver).
		var nearest := Geometry2D.get_closest_point_to_segment(Vector2.ZERO, a0 - b0, a1 - b1)
		static_ok = static_ok and ((t >= 0.0) == (nearest.length() <= ra + rb))
		var swapped := Contact.sweep(b0, b1, rb, rb, a0, a1, ra, ra)
		symmetry_ok = symmetry_ok and absf(t - swapped) < 0.00001
		if t > 0.0:
			root_ok = root_ok and absf(a0.lerp(a1, t).distance_to(b0.lerp(b1, t)) - ra - rb) < 0.005
		geometry_cases += 1
	check("12000 seeded sweeps agree with independent closest-point oracle", static_ok)
	check("12000 sweeps preserve hand/object exchange symmetry", symmetry_ok)
	check("reported first-contact points touch actual padding", root_ok)
	var variable_ok := true
	var subdivision_ok := true
	for sample in range(2000):
		var p0 := _point(rng)
		var p1 := _point(rng)
		var r0 := rng.randf_range(2.0, 240.0)
		var r1 := rng.randf_range(2.0, 240.0)
		var t := Contact.sweep(p0, p1, r0, r1, Vector2.ZERO, Vector2.ZERO, 0, 0)
		# Distance minus a linearly varying radius is convex. Ternary minimum
		# and bisection give an independent numerical oracle without roots.
		var lo := 0.0
		var hi := 1.0
		for iteration in range(60):
			var left := lerpf(lo, hi, 1.0 / 3.0)
			var right := lerpf(lo, hi, 2.0 / 3.0)
			if _gap(p0, p1, r0, r1, left) < _gap(p0, p1, r0, r1, right):
				hi = right
			else:
				lo = left
		var minimum := _gap(p0, p1, r0, r1, (lo + hi) * 0.5)
		if absf(minimum) > 0.01:
			variable_ok = variable_ok and ((t >= 0.0) == (minimum <= 0.0))
		if t > 0.0:
			variable_ok = variable_ok and absf(_gap(p0, p1, r0, r1, t)) < 0.005
		var middle := p0.lerp(p1, 0.5)
		var rm := (r0 + r1) * 0.5
		var split := Contact.sweep(p0, middle, r0, rm, Vector2.ZERO, Vector2.ZERO, 0, 0)
		if split >= 0.0:
			split *= 0.5
		else:
			split = Contact.sweep(middle, p1, rm, r1, Vector2.ZERO, Vector2.ZERO, 0, 0)
			if split >= 0.0:
				split = 0.5 + split * 0.5
		subdivision_ok = subdivision_ok and absf(t - split) < 0.0001
		geometry_cases += 1
	check("2000 changing-radius sweeps agree with convex-distance oracle", variable_ok)
	check("subdividing an animation interval preserves contact time", subdivision_ok)


func _point(rng: RandomNumberGenerator) -> Vector2:
	return Vector2(rng.randf_range(-1600.0, 1600.0), rng.randf_range(-900.0, 900.0))


func _gap(p0: Vector2, p1: Vector2, r0: float, r1: float, t: float) -> float:
	return p0.lerp(p1, t).length() - lerpf(r0, r1, t)


func _touch(boxing: OperaBoxingSurface, finger: int, at: Vector2, pressed: bool,
		canceled: bool = false) -> void:
	var event := InputEventScreenTouch.new()
	event.index = finger
	event.position = at
	event.pressed = pressed
	event.canceled = canceled
	boxing._gui_input(event)


func _drag(boxing: OperaBoxingSurface, finger: int, hand: int, at: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = finger
	event.position = boxing.control_drag_position(hand, at)
	boxing._gui_input(event)


func _setup(boxing: OperaBoxingSurface, layout: String, mode: String) -> void:
	boxing.set_control_layout(layout)
	boxing.configure(mode, Color.WHITE)
	boxing.armed_only = false
	events.clear()


func _flights(boxing: OperaBoxingSurface) -> void:
	var held_ok := true
	var misses_ok := true
	var swats_ok := true
	for layout: String in [boxing.PHONE_EDGES, boxing.TABLET_DIRECT]:
		for viewport_size: Vector2 in [Vector2(1280, 720), Vector2(1600, 720)]:
			boxing.size = viewport_size
			for side in range(2):
				for fraction: float in [0.03, 0.17, 0.31, 0.48, 0.64, 0.80, 0.97]:
					for fps: float in [15.0, 30.0, 60.0, 120.0]:
						_setup(boxing, layout, "boxing_guard")
						boxing._guard_side = side
						var hand := (flight_cases / 4) % 2
						_touch(boxing, 7, boxing.control_press_position(hand), true)
						_drag(boxing, 7, hand, boxing.incoming_position(fraction))
						for frame in range(int(4.0 * fps)):
							boxing._process(1.0 / fps)
							if boxing.round_index() > 0:
								break
						held_ok = held_ok and boxing.round_index() == 1 and not boxing.has_friendly_hit_feedback()
						flight_cases += 1
				_setup(boxing, layout, "boxing_guard")
				boxing._guard_side = side
				_touch(boxing, 7, boxing.control_press_position(0), true)
				_drag(boxing, 7, 0, Vector2(90, 300))
				boxing._process(3.21)
				misses_ok = misses_ok and boxing.round_index() == 0 and boxing.has_friendly_hit_feedback()
				_setup(boxing, layout, "boxing_guard")
				boxing._guard_side = side
				boxing._process(1.7)
				_touch(boxing, 7, boxing.control_press_position(0), true)
				var fist := boxing.incoming_position(boxing.incoming_progress())
				_drag(boxing, 7, 0, fist - Vector2(190, 0))
				var before := boxing.round_index()
				_drag(boxing, 7, 0, fist + Vector2(190, 0))
				swats_ok = swats_ok and before == 0 and boxing.round_index() == 1
	check("224 held guards block early/middle/late with either glove, both layouts/aspects at 15/30/60/120Hz", held_ok)
	check("outside-path gloves do not block even through a long frame", misses_ok)
	check("fast lateral swats crossing the travelling fist are never missed", swats_ok)
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_guard")
	_touch(boxing, 2, boxing.control_press_position(0), true)
	_drag(boxing, 2, 0, boxing.incoming_position(0.8))
	boxing._process(8.0)
	check("one hitch spanning a whole flight resolves one guard before player contact", boxing.round_index() == 1)
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_guard")
	boxing._process(1.4)
	_touch(boxing, 2, boxing.control_press_position(0), true)
	_drag(boxing, 2, 0, Vector2(1100, 604))
	_drag(boxing, 2, 0, Vector2(1100, 100))
	_drag(boxing, 2, 0, Vector2(850, 100))
	_touch(boxing, 2, Vector2(850, 100), false)
	events.clear()
	boxing._process(0.5)
	check("unowned returning glove is swept too: physical deflection never banks a drill",
		boxing.round_index() == 0 and not boxing.has_friendly_hit_feedback()
		and events.size() == 1 and events[0]["kind"] == "boxing_contact")
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_guard")
	for hand in range(2):
		_touch(boxing, hand, boxing.control_press_position(hand), true)
		_drag(boxing, hand, hand, boxing.incoming_position(0.5))
	boxing._process(3.21)
	check("two gloves meeting one attack resolve only one guard", boxing.round_index() == 1 and events.size() == 1)
	var passive_ok := true
	for mode: String in boxing.SUPPORTED_MODES:
		_setup(boxing, boxing.TABLET_DIRECT, mode)
		for frame in range(600):
			boxing._process(0.1)
		passive_ok = passive_ok and boxing.round_index() == 0 and boxing.landed_count() == 0 and not boxing.finished
	check("sixty idle seconds in every phase earn no progress or win", passive_ok)


func _targets(boxing: OperaBoxingSurface) -> void:
	var target_ok := true
	var latch_ok := true
	for layout: String in [boxing.PHONE_EDGES, boxing.TABLET_DIRECT]:
		for mode: String in ["boxing_guide", "boxing_jab", "boxing_belt"]:
			for hand in range(2):
				_setup(boxing, layout, mode)
				_touch(boxing, 8, boxing.control_press_position(hand), true)
				var target := boxing.punch_target(hand)
				var beyond := target + (target - boxing.glove_rest(hand)).normalized() * 300.0
				_drag(boxing, 8, hand, beyond)
				target_ok = target_ok and boxing.landed_count() == 1
				for duplicate in range(20):
					_drag(boxing, 8, hand, beyond)
				latch_ok = latch_ok and boxing.landed_count() == 1
	check("fast strikes crossing guide/mitt/belt padding count despite missing endpoint", target_ok)
	check("twenty repeated samples cannot duplicate an extension", latch_ok)
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_jab")
	_touch(boxing, 8, boxing.control_press_position(0), true)
	_drag(boxing, 8, 0, Vector2(70, 180))
	check("wrong-target extension earns nothing", boxing.landed_count() == 0)
	_drag(boxing, 8, 0, boxing.glove_rest(0))
	_drag(boxing, 8, 0, boxing.active_target_position())
	_drag(boxing, 8, 0, boxing.glove_rest(0))
	_drag(boxing, 8, 0, boxing.active_target_position())
	check("one held finger can retract and punch a fresh target", boxing.landed_count() == 2)


func _ownership(boxing: OperaBoxingSurface) -> void:
	var owners_ok := true
	var canceled_ok := true
	for layout: String in [boxing.PHONE_EDGES, boxing.TABLET_DIRECT]:
		_setup(boxing, layout, "boxing_jab")
		_touch(boxing, 2, boxing.control_press_position(0), true)
		_touch(boxing, 9, boxing.control_press_position(1), true)
		_touch(boxing, 2, boxing.control_press_position(1), true)
		_touch(boxing, 50, boxing.control_press_position(0), true)
		_drag(boxing, 2, 0, Vector2(900, 600))
		_drag(boxing, 9, 1, Vector2(380, 600))
		_touch(boxing, 99, Vector2.ZERO, false)
		owners_ok = owners_ok and boxing.touch_owner_snapshot() == {2: 0, 9: 1}
		var right := boxing.glove_positions[1]
		_touch(boxing, 2, Vector2.ZERO, false, true)
		canceled_ok = canceled_ok and boxing.touch_owner_snapshot() == {9: 1} \
			and boxing.glove_positions[1] == right and events.is_empty()
		_touch(boxing, 9, Vector2.ZERO, false)
		_touch(boxing, 9, Vector2.ZERO, false)
		owners_ok = owners_ok and boxing.touch_owner_snapshot().is_empty()
	check("crossed, duplicate, third and unknown fingers never steal ownership", owners_ok)
	check("canceled touch releases only its own glove without contact/award", canceled_ok)
	_setup(boxing, boxing.PHONE_EDGES, "boxing_jab")
	_touch(boxing, 3, boxing.size * 0.5, true)
	check("phone center cannot silently claim an edge control", boxing.touch_owner_snapshot().is_empty())
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_jab")
	_touch(boxing, 3, boxing.size * 0.5, true)
	check("tablet claims are attached to the visible gloves", boxing.touch_owner_snapshot().is_empty())
	_touch(boxing, 3, boxing.control_press_position(0), true)
	var mouse := InputEventMouseButton.new()
	mouse.button_index = MOUSE_BUTTON_LEFT
	mouse.device = InputEvent.DEVICE_ID_EMULATION
	mouse.pressed = true
	mouse.position = boxing.control_press_position(1)
	boxing._gui_input(mouse)
	check("emulated mouse cannot duplicate real touch", boxing.touch_owner_snapshot() == {3: 0})
	var positions := boxing.glove_positions.duplicate()
	_drag(boxing, 3, 0, Vector2(NAN, INF))
	boxing._process(NAN)
	boxing._process(INF)
	boxing._process(-1.0)
	check("invalid geometry/time cannot poison glove state", boxing.glove_positions == positions and boxing.round_index() == 0)


func _interruptions(boxing: OperaBoxingSurface) -> void:
	var canceled_ok := true
	for notification: int in [Node.NOTIFICATION_PAUSED, MainLoop.NOTIFICATION_APPLICATION_FOCUS_OUT,
			Window.NOTIFICATION_WM_WINDOW_FOCUS_OUT]:
		_setup(boxing, boxing.TABLET_DIRECT, "boxing_guard")
		_touch(boxing, 3, boxing.control_press_position(0), true)
		_drag(boxing, 3, 0, boxing.incoming_position(0.5))
		boxing._notification(notification)
		boxing._process(10.0)
		canceled_ok = canceled_ok and boxing.touch_owner_snapshot().is_empty() \
			and boxing.round_index() == 0 and events.is_empty()
	check("pause and both focus-loss routes cancel without stale attacks or rewards", canceled_ok)
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_guard")
	_touch(boxing, 3, boxing.control_press_position(0), true)
	boxing.hide()
	boxing._process(10.0)
	check("hidden activity cancels and stops attack timeline", boxing.touch_owner_snapshot().is_empty() and events.is_empty())
	boxing.show()
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_guard")
	_touch(boxing, 3, boxing.control_press_position(0), true)
	_drag(boxing, 3, 0, boxing.incoming_position(0.5))
	var callback := func(kind: String, amount: float, _quality: float) -> void:
		if kind == "boxing_guard" and amount > 0.0:
			boxing.configure("boxing_jab", Color.WHITE)
	boxing.gesture.connect(callback)
	boxing._process(3.21)
	boxing.gesture.disconnect(callback)
	check("synchronous phase change cannot be overwritten by old attack callback",
		boxing.mode == "boxing_jab" and boxing.round_index() == 0 and boxing._counter_t == boxing.COUNTER_SECONDS
		and boxing.touch_owner_snapshot().is_empty())
	_touch(boxing, 3, boxing.control_press_position(0), true)
	boxing.accept_completion()
	_drag(boxing, 3, 0, boxing.active_target_position())
	boxing._process(10.0)
	check("completion releases input and rejects stale drag", boxing.touch_owner_snapshot().is_empty() and boxing.landed_count() == 0)
	boxing.configure("boxing_guide", Color.WHITE)
	check("re-entry begins clean without deleting persistent work", boxing.round_index() == 0 and not boxing.finished and boxing.touch_owner_snapshot().is_empty())


func _counter_windows(boxing: OperaBoxingSurface) -> void:
	var block_ok := true
	var stale_ok := true
	var counter_ok := true
	for layout: String in [boxing.PHONE_EDGES, boxing.TABLET_DIRECT]:
		_setup(boxing, layout, "boxing_imp")
		_touch(boxing, 3, boxing.control_press_position(0), true)
		_drag(boxing, 3, 0, boxing.incoming_position(0.6))
		boxing._process(4.0)
		block_ok = block_ok and boxing.imp_is_open() and not boxing.has_friendly_hit_feedback() and boxing.landed_count() == 0
		var at := boxing.glove_positions[0]
		_drag(boxing, 3, 0, at)
		_drag(boxing, 3, 0, at + Vector2(0.1, 0.1))
		stale_ok = stale_ok and boxing.landed_count() == 0
		_drag(boxing, 3, 0, boxing.glove_rest(0))
		_drag(boxing, 3, 0, boxing.active_target_position())
		counter_ok = counter_ok and boxing.landed_count() == 1
	check("held contact opens the floating-hand counter window with no automatic strike", block_ok)
	check("old extension and microscopic wiggle cannot become a counter", stale_ok)
	check("same finger can block, retract and counter in both layouts", counter_ok)


func _touch_fuzz(boxing: OperaBoxingSurface) -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 0xE09E531
	var invariant_ok := true
	var cancel_ok := true
	for batch in range(150):
		var layout: String = boxing.PHONE_EDGES if batch % 2 == 0 else boxing.TABLET_DIRECT
		_setup(boxing, layout, boxing.SUPPORTED_MODES[batch % boxing.SUPPORTED_MODES.size()])
		for event_index in range(200):
			var finger := rng.randi_range(0, 4)
			var hand := rng.randi_range(0, 1)
			var at := Vector2(rng.randf_range(-250, boxing.size.x + 250), rng.randf_range(-200, boxing.size.y + 200))
			match rng.randi_range(0, 7):
				0:
					_touch(boxing, finger, boxing.control_press_position(hand), true)
				1:
					_touch(boxing, finger, at, true)
				2, 3:
					if boxing.touch_owners.has(finger):
						hand = int(boxing.touch_owners[finger])
					_drag(boxing, finger, hand, at)
				4:
					_touch(boxing, finger, at, false)
				5:
					var round_before := boxing.round_index()
					var landed_before := boxing.landed_count()
					var signals_before := events.size()
					_touch(boxing, finger, at, false, true)
					cancel_ok = cancel_ok and boxing.round_index() == round_before \
						and boxing.landed_count() == landed_before and events.size() == signals_before
				6:
					boxing._process(rng.randf_range(0.001, 3.5))
				7:
					boxing.cancel_all_touches()
			var owners := boxing.touch_owner_snapshot()
			invariant_ok = invariant_ok and owners.size() <= 2 and boxing.round_index() <= boxing._mode_goal() \
				and boxing.landed_count() <= boxing._mode_goal()
			for owned_finger: int in owners:
				var owned_hand := int(owners[owned_finger])
				invariant_ok = invariant_ok and owned_hand in [0, 1] and boxing.glove_fingers[owned_hand] == owned_finger
			for glove in range(2):
				invariant_ok = invariant_ok and boxing.glove_positions[glove].is_finite()
				if boxing.glove_fingers[glove] != -1:
					invariant_ok = invariant_ok and owners.get(boxing.glove_fingers[glove], -1) == glove
			fuzz_events += 1
	check("30000 seeded adversarial input/time events preserve ownership, finite geometry and bounded progress", invariant_ok)
	check("random per-finger cancellation never emits contact or work", cancel_ok)


func _complete_paths(boxing: OperaBoxingSurface) -> void:
	for layout: String in [boxing.PHONE_EDGES, boxing.TABLET_DIRECT]:
		for mouse: bool in [false, true]:
			var path_ok := true
			for mode_name: String in boxing.SUPPORTED_MODES:
				_setup(boxing, layout, mode_name)
				for unit in range(int(boxing.MODE_GOALS[mode_name])):
					var hand := unit % 2
					if mode_name == "boxing_imp":
						for frame in range(200):
							if boxing.imp_is_open():
								break
							boxing._process(1.0 / 30.0)
					var press := boxing.control_press_position(hand)
					var target := boxing.punch_target(hand)
					if mouse:
						_mouse_button(boxing, press, true)
						var motion := InputEventMouseMotion.new()
						motion.position = boxing.control_drag_position(hand, target)
						boxing._gui_input(motion)
					else:
						_touch(boxing, 6, press, true)
						_drag(boxing, 6, hand, target)
					if mode_name == "boxing_guard":
						boxing._process(3.21)
					if mouse:
						_mouse_button(boxing, boxing.control_drag_position(hand, target), false)
					else:
						_touch(boxing, 6, boxing.control_drag_position(hand, target), false)
					boxing._process(0.5)
				path_ok = path_ok and boxing.round_index() == int(boxing.MODE_GOALS[mode_name]) \
					and boxing.touch_owner_snapshot().is_empty()
			check("all five phases complete sequentially with one " + ("mouse in " if mouse else "finger in ") + layout, path_ok)


func _mouse_button(boxing: OperaBoxingSurface, at: Vector2, pressed: bool) -> void:
	var button := InputEventMouseButton.new()
	button.button_index = MOUSE_BUTTON_LEFT
	button.position = at
	button.pressed = pressed
	boxing._gui_input(button)


func _completion_feedback(boxing: OperaBoxingSurface) -> void:
	_setup(boxing, boxing.TABLET_DIRECT, "boxing_belt")
	var complete := func(kind: String, amount: float, _quality: float) -> void:
		if kind == "boxing_belt" and amount > 0.0:
			boxing.accept_completion()
	boxing.gesture.connect(complete)
	_touch(boxing, 4, boxing.control_press_position(0), true)
	_drag(boxing, 4, 0, boxing.active_target_position())
	boxing.gesture.disconnect(complete)
	check("synchronous phase completion preserves its accepted finishing bell",
		boxing.finished and boxing._bell_player.playing and boxing.touch_owner_snapshot().is_empty())
	boxing.cancel_all_touches()
	check("explicit cancellation still stops owned feedback sounds", not boxing._bell_player.playing)


func run_routed(host: Node) -> Array[Dictionary]:
	var routed_results: Array[Dictionary] = []
	for viewport_size: Vector2i in [Vector2i(1280, 720), Vector2i(1600, 900), Vector2i(1600, 720), Vector2i(1920, 720)]:
		var viewport := SubViewport.new()
		viewport.size = viewport_size
		host.add_child(viewport)
		var boxing := OperaBoxingSurface.new()
		boxing.size = Vector2(1280, 720)
		boxing.scale = Vector2.ONE * minf(float(viewport_size.x) / 1280.0, float(viewport_size.y) / 720.0)
		boxing.position = (Vector2(viewport_size) - boxing.size * boxing.scale) * 0.5
		viewport.add_child(boxing)
		boxing.set_process(false)
		await host.get_tree().process_frame
		for layout: String in [boxing.PHONE_EDGES, boxing.TABLET_DIRECT]:
			for hand in range(2):
				boxing.set_control_layout(layout)
				boxing.configure("boxing_jab", Color.WHITE)
				boxing.armed_only = false
				var press := InputEventScreenTouch.new()
				press.index = 18
				press.pressed = true
				press.position = boxing.get_global_transform() * boxing.control_press_position(hand)
				if layout == boxing.PHONE_EDGES:
					press.position = Vector2(5.0 if hand == 0 else float(viewport_size.x) - 5.0,
						float(viewport_size.y) * 0.84)
				viewport.push_input(press, true)
				await host.get_tree().process_frame
				var owned := boxing.touch_owner_snapshot() == {18: hand}
				var drag := InputEventScreenDrag.new()
				drag.index = 18
				drag.position = boxing.get_global_transform() * boxing.control_drag_position(hand, boxing.active_target_position())
				viewport.push_input(drag, true)
				await host.get_tree().process_frame
				press.pressed = false
				press.position = drag.position
				viewport.push_input(press, true)
				await host.get_tree().process_frame
				routed_results.append({"label": "viewport-routed hand " + str(hand) + " owns, strikes and releases in " + layout + " at " + str(viewport_size),
					"passed": owned and boxing.landed_count() == 1 and boxing.touch_owner_snapshot().is_empty()})
		viewport.queue_free()
		await host.get_tree().process_frame
	await host.get_tree().create_timer(0.15).timeout
	return routed_results
