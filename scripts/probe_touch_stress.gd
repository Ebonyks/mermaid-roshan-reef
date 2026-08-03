extends SceneTree
# TOUCH RESPONSE STRESS TEST — owner report 2026-08-03: "touching the left side
# of the screen will sometimes cause motion to the right, specifically in Sky
# Lagoon."
#
# Everything here goes through the REAL router: synthetic InputEventScreenTouch
# events are handed to touch_ui exactly as a finger would arrive. Nothing writes
# stick_vec or player.position to manufacture a result, because the defect this
# probe exists to catch lived entirely in the mapping from a screen point to a
# direction, and a probe that pokes stick_vec directly cannot see it.
#
# Gate 1  AGREEMENT — across the whole thumb bay, a drag steers where it points
#                     and a press with no drag steers nowhere.
# Gate 2  LAGOON    — in the Sky Lagoon promenade, a real gesture on the left
#                     of the screen carries Roshan LEFT (and right, right), for
#                     taps, holds and drags, with no wrong-way excursion at all.
# Gate 3  CHURN     — 240 randomized multi-finger events: no inverted frame, no
#                     stuck stick, no stuck action, no leaked owners.
#
# Scope note: hold-to-travel reads Godot's emulated mouse, which headless input
# does not synthesize from these events, so Gate 2 covers taps/holds/drags and
# the hold-to-travel path is covered by its ownership contract instead
# (reserved_zone_hit, asserted in Gate 1 and in probe_touch_router).

const CHURN_EVENTS := 240
const TRAVEL_FRAME_CAP := 400
const TRAVEL_ENOUGH := 2.0     # stage units: stop sampling once clearly underway
const TRAVEL_MIN := 0.5        # stage units: below this the gesture did nothing
const WRONG_WAY_SLOP := 0.12   # stage units of tolerated bob/settle jitter
const OWNER_STICK := 2         # TouchUI.TouchOwner.STICK
# Where to nudge a press when a wandering animal or a toy is standing on it.
# Targets claim a 92 px pick radius, so the sweep has to clear that generously.
# The x nudges always run AWAY from screen centre, in the direction the case
# already expects to travel — a retry must never quietly cross to the other
# side of Roshan and turn a real regression into a pass.
const RETRY_STEPS: Array[Vector2] = [
	Vector2(0.0, 0.0), Vector2(0.0, -34.0), Vector2(0.0, 28.0),
	Vector2(1.0, 0.0), Vector2(1.0, -34.0), Vector2(2.0, 0.0),
	Vector2(2.0, -34.0), Vector2(3.0, 0.0),
]
const RETRY_STEP_PX := 105.0

var main: ReefMain
var touch: CanvasLayer
var prom: Object
var fingers: Dictionary = {}
var taps: Array[Vector2] = []
var failures := 0

func _init() -> void:
	var packed: PackedScene = load("res://scenes/main.tscn")
	main = packed.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await _frames(5)
	touch = main.touch_ui
	if touch == null or not touch.wants_touch():
		_bad("touch router unavailable; run with -- --touch --hybrid-touch-test")
		_finish()
		return
	main._set_touch_mode("hybrid", false)
	main._populate_touch_interactables()
	await _agreement_gate()
	await _lagoon_gate()
	await _churn_gate()
	_finish()

# ---------------------------------------------------------------- gate 1 -----

func _agreement_gate() -> void:
	var bay: Rect2 = touch.movement_zone()
	var directions: Array[Vector2] = [
		Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN,
		Vector2(-1.0, -1.0).normalized(), Vector2(1.0, -1.0).normalized(),
		Vector2(-1.0, 1.0).normalized(), Vector2(1.0, 1.0).normalized(),
	]
	var worst_agreement := 1.0
	var presses := 0
	for column: int in range(5):
		for row: int in range(3):
			# inset so every sample point is a real press inside the bay
			var press := Vector2(
				lerpf(bay.position.x + 30.0, bay.end.x - 30.0, float(column) / 4.0),
				lerpf(bay.position.y + 30.0, bay.end.y - 30.0, float(row) / 2.0))
			for direction: Vector2 in directions:
				presses += 1
				_down(0, press)
				await process_frame
				if not (touch.stick_vec as Vector2).is_zero_approx():
					_bad("press at %s steered before any drag: %s" \
						% [press, touch.stick_vec])
				_drag(0, press + direction * 90.0)
				await process_frame
				var steer: Vector2 = touch.stick_vec
				if steer.length() < 0.45:
					_bad("drag %s at %s barely steered: %s" \
						% [direction, press, steer])
				else:
					var agreement: float = steer.normalized().dot(direction)
					worst_agreement = minf(worst_agreement, agreement)
					if agreement < 0.99:
						_bad("drag %s at %s steered %s (agreement %.3f)" \
							% [direction, press, steer.normalized(), agreement])
				_up(0, fingers[0])
				await process_frame
				if not (touch.stick_vec as Vector2).is_zero_approx():
					_bad("stick stayed live after release at %s" % press)
	_ok("agreement", "%d bay gestures, worst direction agreement %.4f" \
		% [presses, worst_agreement])

	# The bay must not be a hole in the world: a press there that never became a
	# drag is still a tap, so tap-to-travel works in the lower-left too.
	touch.world_touched.connect(_record_tap)
	var bay_tap: Vector2 = bay.get_center()
	_down(0, bay_tap)
	_up(0, bay_tap)
	await process_frame
	if taps.size() != 1 or taps[0].distance_to(bay_tap) > 0.1:
		_bad("a tap in the thumb bay never reached the world: %s" % [taps])
	taps.clear()
	# ...but a press that DID drag is movement, and must not also fire a tap.
	_down(0, bay_tap)
	_drag(0, bay_tap + Vector2(80.0, 0.0))
	_up(0, fingers[0])
	await process_frame
	if not taps.is_empty():
		_bad("a bay drag leaked a world tap: %s" % [taps])
	touch.world_touched.disconnect(_record_tap)
	taps.clear()
	_ok("bay_tap_fallthrough", "press taps, drag steers, never both")

	# Hold-to-travel clients read the emulated pointer, which is blind to touch
	# ownership. They ask the router first, so a held BUTTON is never "walk here".
	var screen: Vector2 = get_root().get_viewport().get_visible_rect().size
	var reserved_ok: bool = touch.reserved_zone_hit(touch.action_zone().get_center()) \
		and touch.reserved_zone_hit(bay.get_center()) \
		and touch.reserved_zone_hit(touch.pause_zone().get_center()) \
		and not touch.reserved_zone_hit(Vector2(screen.x * 0.58, screen.y * 0.32))
	if not reserved_ok:
		_bad("hold-to-travel reservation does not match the router's own zones")
	else:
		_ok("hold_travel_reservation", "medallion, bay and pause reserved; world free")
	main._tap_move_ref().cancel("stress reset")
	main._interaction_ref().clear_focus()

# ---------------------------------------------------------------- gate 2 -----

func _lagoon_gate() -> void:
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.save_data["lagoon_plane_departed"] = false
	main._enter_level2()
	await _frames(10)
	if main.game != "level2" or String(main.g.get("phase", "")) != "promenade":
		_bad("could not reach the Sky Lagoon promenade (game=%s phase=%s)" \
			% [main.game, main.g.get("phase", "")])
		return
	prom = main._lagoon_promenade_ref()
	await _await_input_ready()
	var screen: Vector2 = get_root().get_viewport().get_visible_rect().size
	var low_y: float = screen.y * 0.78          # deep in the thumb bay
	var high_y: float = screen.y * 0.40         # clear of every thumb control

	# x fractions chosen from the report: 0.12 is the corner the bay was built
	# for, 0.25 is where the old invisible anchor flipped the sign, 0.85 is the
	# mirror case that must still go right.
	await _travel_case("tap_far_left", "tap", Vector2(screen.x * 0.12, low_y), -1)
	await _travel_case("tap_left_of_anchor", "tap", Vector2(screen.x * 0.25, low_y), -1)
	await _travel_case("tap_left_high", "tap", Vector2(screen.x * 0.18, high_y), -1)
	await _travel_case("tap_right", "tap", Vector2(screen.x * 0.72, high_y), 1)
	await _travel_case("hold_left_in_bay", "hold", Vector2(screen.x * 0.25, low_y), -1)
	await _travel_case("drag_left_in_bay", "drag_left", Vector2(screen.x * 0.25, low_y), -1)
	await _travel_case("drag_right_in_bay", "drag_right", Vector2(screen.x * 0.25, low_y), 1)
	await _held_medallion_case()

func _travel_case(label: String, gesture: String, press: Vector2, expect: int) -> void:
	var screen: Vector2 = get_root().get_viewport().get_visible_rect().size
	for step: Vector2 in RETRY_STEPS:
		var point := Vector2(
			clampf(press.x + step.x * float(expect) * RETRY_STEP_PX, 30.0, screen.x - 30.0),
			clampf(press.y + step.y, 30.0, screen.y - 30.0))
		if gesture != "tap":
			# hold and drag cases are specifically about the thumb bay: a retry
			# nudge must not push the press out of the zone under test
			var bay: Rect2 = touch.movement_zone()
			point.x = clampf(point.x, bay.position.x + 30.0, bay.end.x - 30.0)
			point.y = clampf(point.y, bay.position.y + 30.0, bay.end.y - 30.0)
		if not _press_is_open_ground(point):
			continue
		await _reset_promenade()
		var start_x: float = prom.stage.px()
		var worst_wrong := 0.0
		var moved := 0.0
		if gesture == "hold":
			_down(0, point)
			for _hold_frame: int in range(40):
				await process_frame
				var wrong: float = float(-expect) * (prom.stage.px() - start_x)
				worst_wrong = maxf(worst_wrong, wrong)
			var still_open: bool = _press_is_open_ground(point)
			_up(0, point)
			if not still_open:
				continue              # a wanderer drifted under the finger; retry
		elif gesture == "drag_left" or gesture == "drag_right":
			var slide: float = -150.0 if gesture == "drag_left" else 150.0
			_down(0, point)
			await process_frame
			_drag(0, point + Vector2(slide, 0.0))
			for _drag_frame: int in range(60):
				await process_frame
				var wrong: float = float(-expect) * (prom.stage.px() - start_x)
				worst_wrong = maxf(worst_wrong, wrong)
				moved = maxf(moved, float(expect) * (prom.stage.px() - start_x))
				if moved >= TRAVEL_ENOUGH:
					break
			_up(0, fingers[0])
		else:
			_down(0, point)
			_up(0, point)
		for _travel_frame: int in range(TRAVEL_FRAME_CAP):
			await process_frame
			var delta_x: float = prom.stage.px() - start_x
			worst_wrong = maxf(worst_wrong, float(-expect) * delta_x)
			moved = maxf(moved, float(expect) * delta_x)
			if moved >= TRAVEL_ENOUGH:
				break
		var way: String = "left" if expect < 0 else "right"
		if worst_wrong > WRONG_WAY_SLOP:
			_bad("%s: a %s-side gesture carried Roshan the wrong way by %.2f units" \
				% [label, way, worst_wrong])
		elif moved < TRAVEL_MIN:
			_bad("%s: the gesture produced no travel at all (%.2f units, press %s, walk goal %s)" \
				% [label, moved, point, main.g.get("ss_walk_goal")])
		else:
			_ok(label, "travelled %.2f units %s, wrong-way excursion %.3f" \
				% [moved, way, worst_wrong])
		return
	_bad("%s: no open ground under any of the %d sample presses" \
		% [label, RETRY_STEPS.size()])

func _held_medallion_case() -> void:
	# Holding PLAY is a button press, never a request to walk to the bottom-right
	# corner of the screen. (The emulated-pointer hold-to-travel path used to read
	# it as exactly that.)
	await _reset_promenade()
	var start_x: float = prom.stage.px()
	var drift := 0.0
	var press: Vector2 = touch.action_zone().get_center()
	_down(0, press)
	for _hold_frame: int in range(90):
		await process_frame
		drift = maxf(drift, absf(prom.stage.px() - start_x))
	_up(0, press)
	await _frames(30)
	drift = maxf(drift, absf(prom.stage.px() - start_x))
	if drift > 1.0:
		_bad("holding the action medallion walked Roshan %.2f units" % drift)
	else:
		_ok("held_medallion", "stayed put (%.3f units of hop settle)" % drift)
	touch.consume_action()

func _reset_promenade() -> void:
	touch.cancel_all_touches()
	main.g["ss_walk_goal"] = null
	main.g["lagoon_play_anim"] = {}
	main.g["lagoon_promenade_focus"] = ""
	main._tap_move_ref().cancel("stress reset")
	prom._set_spawn(prom._walk_x(0.0))
	await _frames(4)
	await _await_input_ready()

func _await_input_ready() -> void:
	# _on_touch_world deliberately drops taps while a world-transition fade is up.
	# That is correct game behaviour, so the probe waits for the curtain instead of
	# reading the dropped tap as a routing defect.
	for _wait_frame: int in range(300):
		if main.mg_kind == "" and not main.get_tree().paused \
				and (main.fade_rect == null or main.fade_rect.modulate.a <= 0.02):
			return
		await process_frame

func _press_is_open_ground(point: Vector2) -> bool:
	# The promenade routes taps itself: an animal or a toy under the finger is a
	# legitimate different verb, not travel, so those samples are not evidence.
	return (prom._animal_at(point) as Dictionary).is_empty() \
		and (prom._target_at(point) as Dictionary).is_empty()

# ---------------------------------------------------------------- gate 3 -----

func _churn_gate() -> void:
	seed(20260803)
	var screen: Vector2 = get_root().get_viewport().get_visible_rect().size
	var live: Dictionary = {}       # finger index -> accumulated drag offset
	var inversions := 0
	var events := 0
	while events < CHURN_EVENTS:
		events += 1
		var index: int = randi() % 4
		var roll: float = randf()
		if not live.has(index):
			var point := Vector2(randf() * screen.x, randf() * screen.y)
			live[index] = {"pos": point, "off": Vector2.ZERO}
			_down(index, point)
		elif roll < 0.55:
			var record: Dictionary = live[index]
			var step := Vector2(randf_range(-70.0, 70.0), randf_range(-70.0, 70.0))
			record["off"] = (record["off"] as Vector2) + step
			_drag(index, (fingers[index] as Vector2) + step)
			await process_frame
			# The one invariant the report is about: while a finger owns the
			# stick, the commanded direction agrees with where it dragged.
			if touch.touch_owners.get(index, 0) == OWNER_STICK \
					and index == int(touch._touch_idx):
				var off: Vector2 = record["off"]
				var steer: Vector2 = touch.stick_vec
				if off.length() > 40.0 and steer.length() > 0.05 \
						and steer.normalized().dot(off.normalized()) < 0.98:
					inversions += 1
		else:
			_up(index, fingers[index])
			live.erase(index)
		if events % 7 == 0:
			await process_frame
	for index: Variant in live.keys():
		_up(int(index), fingers[index])
	await _frames(6)
	if inversions > 0:
		_bad("churn produced %d frames where the stick fought the drag" % inversions)
	else:
		_ok("churn_agreement", "%d randomized events, no inverted frame" % CHURN_EVENTS)
	var residue: Array[String] = []
	if not touch.touch_owners.is_empty():
		residue.append("owners %s" % [touch.touch_owners])
	if not (touch.stick_vec as Vector2).is_zero_approx():
		residue.append("stick %s" % touch.stick_vec)
	if bool(touch.action_down):
		residue.append("action held")
	if int(touch._touch_idx) != -1:
		residue.append("stick owner %d" % int(touch._touch_idx))
	if not (touch._world_pend as Dictionary).is_empty():
		residue.append("pending world touches %s" % [touch._world_pend])
	if residue.is_empty():
		_ok("churn_hygiene", "router returned to rest")
	else:
		_bad("churn left the router holding state: %s" % ", ".join(residue))

# ---------------------------------------------------------------- helpers ----

func _record_tap(pos: Vector2) -> void:
	taps.append(pos)

func _down(index: int, pos: Vector2) -> void:
	fingers[index] = pos
	var event := InputEventScreenTouch.new()
	event.index = index
	event.position = pos
	event.pressed = true
	touch._unhandled_input(event)

func _drag(index: int, pos: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = index
	event.position = pos
	event.relative = pos - (fingers[index] as Vector2)
	fingers[index] = pos
	touch._unhandled_input(event)

func _up(index: int, pos: Vector2) -> void:
	fingers[index] = pos
	var event := InputEventScreenTouch.new()
	event.index = index
	event.position = pos
	event.pressed = false
	touch._unhandled_input(event)

func _frames(count: int) -> void:
	for _frame_index: int in range(count):
		await process_frame

func _ok(label: String, detail: String) -> void:
	print("TOUCHSTRESS|%s: OK %s" % [label, detail])

func _bad(message: String) -> void:
	failures += 1
	print("TOUCHSTRESS|FAIL ", message)

func _finish() -> void:
	if failures == 0:
		print("TOUCHSTRESS|ALL OK")
		quit()
	else:
		print("TOUCHSTRESS|FAIL %d issue(s)" % failures)
		quit(1)
