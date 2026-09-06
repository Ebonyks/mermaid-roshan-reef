class_name OperaRacerSurface
extends OperaGestureSurface
## Opera's pit-stop gestures and painted-circuit race share one surface.
## KartDriving is also used by KartGame; this class owns only the Canvas race
## presentation, touch ownership and conversion of completed laps to Opera units.

const Driving := preload("res://scripts/kart_driving.gd")
signal race_event(kind: String, value: float)

const LAP_DISTANCE := 800.0
const LAP_SECONDS := 24.0
const ROAD_WALL := 8.0
const INPUT_GRACE := 2.0
const STEERING_RECT := Rect2(258, 570, 770, 126)
const TURBO_CENTER := Vector2(1134, 632)
const TURBO_RADIUS := 60.0
# Centerline on the approved native world_racer composition. The front
# straight passes in front of the pearl daises; no second track is painted.
const ROUTE := [
	Vector2(0.83, 0.651), Vector2(0.71, 0.682), Vector2(0.53, 0.688),
	Vector2(0.34, 0.682), Vector2(0.16, 0.633), Vector2(0.115, 0.535),
	Vector2(0.19, 0.474), Vector2(0.279, 0.395), Vector2(0.279, 0.320),
	Vector2(0.40, 0.246), Vector2(0.54, 0.185), Vector2(0.65, 0.223),
	Vector2(0.755, 0.312), Vector2(0.793, 0.382), Vector2(0.738, 0.464),
	Vector2(0.776, 0.539), Vector2(0.864, 0.597),
]
const ZOOM_STRIPS := [
	{"u": 0.12, "lat": -3.0}, {"u": 0.36, "lat": 3.0},
	{"u": 0.61, "lat": -3.0}, {"u": 0.83, "lat": 3.0},
]
const PEARLS := [
	{"u": 0.18, "lat": -3.0}, {"u": 0.23, "lat": -3.0},
	{"u": 0.43, "lat": 3.0}, {"u": 0.48, "lat": 3.0},
	{"u": 0.70, "lat": -3.0}, {"u": 0.75, "lat": -3.0},
]

var kart: Dictionary = {}
var rival: Dictionary = {}
var race_started := false
var race_finished := false
var race_clock := 0.0
var race_input_t := 0.0
var race_touch_owner := -1
var race_turbo_owner := -1
var race_turbo_held := false
var race_steer := 0.0
var race_countdown := 0.0
var race_flash := 0.0
var race_pearls := 0
var race_turbo_fires := 0
var race_wall_bumps := 0
var _turbo_queued := false
var _route_curve := Curve2D.new()
var _route_length := 0.0
var _collected: Dictionary = {}
var _kart_art: Texture2D = null
var _wheel_art: Texture2D = null
var _driver_art: Texture2D = null
var _rival_art: Texture2D = null
var _boost_art: Texture2D = null
var _steering_style: StyleBoxFlat = null


func configure(next_mode: String, next_accent: Color, choice: int = 1,
		next_context: String = "") -> void:
	super.configure(next_mode, next_accent, choice, next_context)
	cancel_race_touch()
	if next_mode != "kart_race":
		return
	race_started = false
	race_finished = false
	race_clock = 0.0
	race_countdown = 0.0
	race_flash = 0.0
	race_pearls = 0
	race_turbo_fires = 0
	race_wall_bumps = 0
	_collected.clear()
	kart = _new_kart(0.0, 0.0)
	rival = _new_kart(-28.0, 3.0)
	_build_route()
	_kart_art = _load_widget_texture("res://assets/opera/worlds/widgets/widget_crank_racer_kart.png")
	_wheel_art = _load_widget_texture("res://assets/opera/worlds/widgets/widget_crank_racer_wheel.png")
	_driver_art = _load_widget_texture("res://assets/opera/worlds/actors/roshan_racer.png")
	_rival_art = _load_widget_texture("res://assets/opera/worlds/actors/rival_racer.png")
	_boost_art = _load_widget_texture("res://assets/kart/boost_ribbon.png")
	_steering_style = StyleBoxFlat.new()
	_steering_style.bg_color = Color("#f9ecd5")
	_steering_style.border_color = Color("#51416f")
	_steering_style.set_border_width_all(5)
	_steering_style.set_corner_radius_all(54)
	queue_redraw()


func _new_kart(distance: float, lateral: float) -> Dictionary:
	return {"s": distance, "lat": lateral, "latv": 0.0, "speed": 0.0,
		"meter": 0.5, "boost_t": 0.0, "full_t": 0.0, "hop": 0.0, "squash": 0.0}


func _build_route() -> void:
	_route_curve.clear_points()
	for index in range(ROUTE.size()):
		var previous: Vector2 = ROUTE[(index - 1 + ROUTE.size()) % ROUTE.size()] * Vector2(1280, 720)
		var point: Vector2 = ROUTE[index] * Vector2(1280, 720)
		var following: Vector2 = ROUTE[(index + 1) % ROUTE.size()] * Vector2(1280, 720)
		var handle := (following - previous) / 6.0
		_route_curve.add_point(point, -handle, handle)
	var first_handle := (ROUTE[1] - ROUTE[-1]) * Vector2(1280, 720) / 6.0
	_route_curve.add_point(ROUTE[0] * Vector2(1280, 720), -first_handle, first_handle)
	_route_curve.bake_interval = 3.0
	_route_length = _route_curve.get_baked_length()


func road_point(distance: float, lateral: float = 0.0) -> Vector2:
	var at := fposmod(distance / LAP_DISTANCE, 1.0) * _route_length
	var center := _route_curve.sample_baked(at, true)
	var forward := _route_curve.sample_baked(fposmod(at + 3.0, _route_length), true) \
		- _route_curve.sample_baked(fposmod(at - 3.0, _route_length), true)
	return center + forward.normalized().orthogonal() * lateral * 2.4


func road_curvature(distance: float) -> float:
	var before := (road_point(distance) - road_point(distance - 3.0)).normalized()
	var after := (road_point(distance + 3.0) - road_point(distance)).normalized()
	# These chord tangents are centered 3 distance units apart (-1.5/+1.5).
	return clampf(before.angle_to(after) / 3.0, -0.03, 0.03)


func _gui_input(event: InputEvent) -> void:
	if mode != "kart_race":
		super._gui_input(event)
		return
	if armed_only or completion_accepted or race_finished:
		return
	if event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed and touch.position.distance_to(TURBO_CENTER) <= TURBO_RADIUS \
				and race_turbo_owner == -1:
			race_turbo_owner = touch.index
			race_turbo_held = true
			_turbo_queued = true
			_touch_race()
		elif not touch.pressed and touch.index == race_turbo_owner:
			race_turbo_owner = -1
			race_turbo_held = false
		elif touch.pressed and race_touch_owner == -1 \
				and STEERING_RECT.grow(12.0).has_point(touch.position):
			race_touch_owner = touch.index
			_press(touch.position)
		elif not touch.pressed and touch.index == race_touch_owner:
			_release(touch.position)
		accept_event()
	elif event is InputEventScreenDrag:
		var drag := event as InputEventScreenDrag
		if drag.index == race_touch_owner:
			_drag(drag.position)
			accept_event()
	elif event is InputEventMouseButton:
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_LEFT:
			if button.pressed and race_touch_owner == -1:
				race_touch_owner = -2
				_press(button.position)
			elif not button.pressed and race_touch_owner == -2:
				_release(button.position)
			accept_event()
	elif event is InputEventMouseMotion and race_touch_owner == -2:
		_drag((event as InputEventMouseMotion).position)
		accept_event()


func _press(at: Vector2) -> void:
	if mode != "kart_race":
		super._press(at)
		return
	if armed_only or completion_accepted or race_finished:
		return
	if at.distance_to(TURBO_CENTER) <= TURBO_RADIUS:
		race_turbo_held = true
		_turbo_queued = true
		_touch_race()
		return
	if not STEERING_RECT.grow(12.0).has_point(at):
		return
	held = true
	_drag(at)


func _drag(at: Vector2) -> void:
	if mode != "kart_race":
		super._drag(at)
		return
	if not held or armed_only or completion_accepted:
		return
	race_steer = clampf((at.x - STEERING_RECT.get_center().x) / 290.0, -1.0, 1.0)
	_touch_race()


func _release(at: Vector2) -> void:
	if mode != "kart_race":
		super._release(at)
		return
	held = false
	race_turbo_held = race_turbo_owner >= 0
	race_touch_owner = -1
	race_steer = 0.0


func _touch_race() -> void:
	race_input_t = INPUT_GRACE
	input_started = true
	demo_active = false
	if not race_started:
		race_started = true
		race_countdown = 1.5
		race_event.emit("start", 0.0)


func cancel_race_touch() -> void:
	held = false
	race_turbo_held = false
	race_turbo_owner = -1
	race_touch_owner = -1
	race_input_t = 0.0
	race_steer = 0.0
	_turbo_queued = false


func _notification(what: int) -> void:
	if what in [NOTIFICATION_PAUSED, NOTIFICATION_APPLICATION_PAUSED,
			NOTIFICATION_APPLICATION_FOCUS_OUT]:
		cancel_race_touch()


func _process(delta: float) -> void:
	if mode != "kart_race":
		super._process(delta)
		return
	if armed_only or completion_accepted or race_finished:
		return
	race_clock += delta
	demo_t += delta
	race_flash = maxf(0.0, race_flash - delta)
	if held or race_turbo_held:
		race_input_t = INPUT_GRACE
	else:
		race_input_t = maxf(0.0, race_input_t - delta)
	if not race_started or race_input_t <= 0.0:
		demo_active = true
		queue_redraw()
		return
	if race_countdown > 0.0:
		var count_before := ceili(race_countdown * 2.0)
		race_countdown = maxf(0.0, race_countdown - delta)
		if ceili(race_countdown * 2.0) < count_before:
			race_event.emit("countdown", float(3 - ceili(race_countdown * 2.0)))
		queue_redraw()
		return
	var remaining := minf(delta, 0.2)
	while remaining > 0.00001 and not race_finished:
		var step := minf(remaining, 1.0 / 60.0)
		_tick_driving(step)
		remaining -= step
	queue_redraw()


func _tick_driving(delta: float) -> void:
	var vehicle: Dictionary = Driving.KART_HANDLING
	kart["hop"] = maxf(0.0, float(kart["hop"]) - delta)
	kart["squash"] = maxf(0.0, float(kart["squash"]) - delta)
	var previous := float(kart["s"])
	if Driving.tick_turbo(kart, vehicle, _turbo_queued, true, delta):
		race_turbo_fires += 1
		race_flash = 0.6
		race_event.emit("turbo", float(race_turbo_fires))
	_turbo_queued = false
	var boosted: bool = float(kart["boost_t"]) > 0.0
	var speed := LAP_DISTANCE / LAP_SECONDS * (1.0 + (Driving.BOOST_MUL if boosted else 0.0))
	Driving.accelerate(kart, speed, boosted, delta)
	Driving.advance(kart, road_curvature(previous), delta)
	var drift_event := Driving.tick_drift(kart, race_steer, road_curvature(float(kart["s"])), delta)
	if bool(drift_event["release"]):
		var tier := Driving.release_drift(kart)
		if tier > 0:
			race_event.emit("turbo", float(tier))
	var steering := Driving.steering_target(kart, vehicle, race_steer, ROAD_WALL, true)
	Driving.steer_velocity(kart, steering, float(vehicle["slip"]), delta)
	if Driving.apply_lateral(kart, vehicle,
			float(kart["lat"]) + float(kart["latv"]) * delta, ROAD_WALL):
		race_wall_bumps += 1
		Driving.cancel_drift(kart)
		# A rail is a soft rebound. No progress or collected pearl is removed.
		race_flash = 0.18
	var progress := minf(float(kart["s"]), LAP_DISTANCE * float(Driving.LAPS))
	kart["s"] = progress
	_tick_collectibles(delta, previous, progress)
	# Same asymmetric catch-up pattern as the established racing engine.
	var gap := progress - float(rival["s"])
	var rival_target := LAP_DISTANCE / LAP_SECONDS * 0.94 \
		+ clampf(gap * 0.08, -LAP_DISTANCE / LAP_SECONDS * 0.30,
			LAP_DISTANCE / LAP_SECONDS * 0.38)
	Driving.accelerate(rival, maxf(0.0, rival_target), false, delta)
	# The rival follows the inside of the next bend, leaving Roshan room to pass.
	var rival_lane := -signf(road_curvature(float(rival["s"]) + 18.0)) * 3.0
	rival["lat"] = move_toward(float(rival["lat"]), rival_lane, delta * 2.0)
	Driving.advance(rival, road_curvature(float(rival["s"])), delta)
	var lap_before := floori(previous / LAP_DISTANCE)
	var lap_now := floori(progress / LAP_DISTANCE)
	if lap_now > lap_before:
		race_event.emit("lap", float(lap_now))
	if progress >= LAP_DISTANCE * float(Driving.LAPS):
		race_finished = true
		held = false
		race_touch_owner = -1
	# Emit distance in lap units, never frame-count or incidental touch credit.
	gesture.emit("kart_race", (progress - previous) / LAP_DISTANCE, 1.0)


func _tick_collectibles(delta: float, previous: float, progress: float) -> void:
	var within_lap := fposmod(progress, LAP_DISTANCE) / LAP_DISTANCE
	for strip: Dictionary in ZOOM_STRIPS:
		var separation := absf(wrapf(within_lap - float(strip["u"]), -0.5, 0.5))
		if separation < 0.013 and absf(float(kart["lat"]) - float(strip["lat"])) < 2.5:
			kart["boost_t"] = maxf(float(kart["boost_t"]), 0.35)
			Driving.charge(kart, Driving.KART_HANDLING, 0.60 * delta)
	for lap in range(Driving.LAPS):
		for index in range(PEARLS.size()):
			var pearl: Dictionary = PEARLS[index]
			var at := (float(lap) + float(pearl["u"])) * LAP_DISTANCE
			var key := lap * PEARLS.size() + index
			if not _collected.has(key) and previous <= at and progress >= at \
					and absf(float(kart["lat"]) - float(pearl["lat"])) < 2.5:
				_collected[key] = true
				race_pearls += 1
				Driving.charge(kart, Driving.KART_HANDLING, 0.16)
				race_flash = 0.3
				race_event.emit("pearl", float(race_pearls))


func _draw() -> void:
	if mode != "kart_race":
		super._draw()
		return
	if kart.is_empty():
		return
	last_contextual_draw_route = "kart_shared_driving:painted_circuit"
	var lap := mini(Driving.LAPS - 1, floori(float(kart["s"]) / LAP_DISTANCE))
	for strip: Dictionary in ZOOM_STRIPS:
		var at := road_point(float(strip["u"]) * LAP_DISTANCE, float(strip["lat"]))
		if _boost_art != null:
			draw_texture_rect(_boost_art, Rect2(at - Vector2(22, 10), Vector2(44, 20)), false)
		else:
			draw_line(at - Vector2(16, 0), at + Vector2(16, 0), Color("#ffe299"), 9.0, true)
	for index in range(PEARLS.size()):
		if _collected.has(lap * PEARLS.size() + index):
			continue
		var pearl: Dictionary = PEARLS[index]
		var at := road_point(float(pearl["u"]) * LAP_DISTANCE, float(pearl["lat"]))
		draw_circle(at, 10.0, Color("#65547f"))
		draw_circle(at, 7.0, Color("#fff0ce"))
		draw_circle(at + Vector2(-2, -2), 2.5, Color.WHITE)
	var player_at := road_point(float(kart["s"]), float(kart["lat"]))
	var rival_at := road_point(float(rival["s"]), float(rival["lat"]))
	if player_at.y >= rival_at.y:
		_draw_car(rival, _rival_art, false)
		_draw_car(kart, _driver_art, true)
	else:
		_draw_car(kart, _driver_art, true)
		_draw_car(rival, _rival_art, false)
	_draw_race_controls()


func _draw_car(state: Dictionary, driver: Texture2D, is_player: bool) -> void:
	var distance := float(state["s"])
	var at := road_point(distance, float(state["lat"]))
	var depth := lerpf(0.65, 1.0, clampf((at.y - 130.0) / 340.0, 0.0, 1.0))
	var direction := -1.0 if road_point(distance + 2.0).x >= road_point(distance - 2.0).x else 1.0
	# Flat side-view artwork stays upright. Mirror the complete kart/driver
	# group at bends; never turn a painted mermaid upside down.
	draw_set_transform(at, 0.0, Vector2(depth * 1.7, depth * 0.36))
	draw_circle(Vector2(0, 5), 27.0, Color(0.12, 0.10, 0.25, 0.24))
	var hop := sin(clampf(float(state.get("hop", 0.0)) / 0.22, 0.0, 1.0) * PI) * 10.0
	draw_set_transform(at - Vector2(0, hop * depth), 0.0, Vector2(direction * depth, depth))
	if driver != null:
		# Show the authored upper body inside the cockpit. The kart occludes
		# the waist; the source cutout and its proportions stay unchanged.
		draw_texture_rect_region(driver, Rect2(-40, -107, 86, 50.39), Rect2(0, 0, 512, 300))
	if _kart_art != null:
		draw_texture_rect(_kart_art, Rect2(-75, -109, 150, 150), false)
	if _wheel_art != null:
		draw_texture_rect(_wheel_art, Rect2(19.2, -36.25, 36, 36), false)
	draw_set_transform(Vector2.ZERO)
	if is_player:
		draw_circle(at + Vector2(0, 10), 8, Color("#51416f"))
		draw_circle(at + Vector2(0, 10), 5, Color("#ffe3a3"))
		if bool(state.get("drift", false)):
			var tier := Driving.drift_tier(float(state.get("drift_t", 0.0)))
			var colors := [Color("#b4edf2"), Color("#eef6ff"), Color("#ffe08c"), Color("#eea9eb")]
			for index in range(3):
				draw_circle(road_point(distance - float(index + 1) * 4, float(state["lat"])),
					4.0, colors[tier])
		if float(state["boost_t"]) > 0.0:
			for index in range(4):
				var trail := road_point(distance - float(index + 1) * 3.0, float(state["lat"]))
				draw_circle(trail, 7.0 - float(index), Color(0.8, 0.97, 1.0, 0.7 - float(index) * 0.12))
		if race_flash > 0.0 or race_finished:
			for index in range(5):
				var angle := -PI + float(index) * PI / 4.0
				var spark := at - Vector2(0, 30) + Vector2.from_angle(angle) * (55 + race_flash * 20)
				draw_line(spark - Vector2(4, 0), spark + Vector2(4, 0), Color("#fff1ad"), 3, true)
				draw_line(spark - Vector2(0, 4), spark + Vector2(0, 4), Color("#fff1ad"), 3, true)


func _draw_race_controls() -> void:
	for lap in range(Driving.LAPS):
		var center := Vector2(66 + lap * 88, 68)
		var done := float(kart["s"]) >= float(lap + 1) * LAP_DISTANCE
		draw_circle(center, 35, Color("#52406f"))
		draw_circle(center, 29, Color("#ffe2a0") if done else Color("#e7ddef"))
		var fraction := clampf(float(kart["s"]) / LAP_DISTANCE - float(lap), 0.0, 1.0)
		if fraction > 0.001:
			draw_arc(center, 32, -PI * 0.5, -PI * 0.5 + TAU * fraction, 48,
				Color("#71d7d0"), 7, true)
	draw_style_box(_steering_style, STEERING_RECT)
	var center := STEERING_RECT.get_center()
	draw_line(center - Vector2(290, 0), center + Vector2(290, 0), Color("#b3ded7"), 14, true)
	for sign_value: float in [-1.0, 1.0]:
		var at := center + Vector2(sign_value * 316, 0)
		draw_polyline(PackedVector2Array([at + Vector2(-sign_value * 18, -16),
			at, at + Vector2(-sign_value * 18, 16)]), Color("#6b4e81"), 6, true)
	var knob := center + Vector2(race_steer * 270, 0)
	if demo_active:
		knob.x += sin(race_clock * 2.0) * 125.0
	draw_circle(knob, 49, Color("#665180"))
	draw_circle(knob, 42, Color("#e9b88a"))
	draw_arc(knob, 29, 0, TAU, 36, Color("#fff0d0"), 7, true)
	draw_line(knob, knob + Vector2(0, 26), Color("#fff0d0"), 6, true)
	if demo_active:
		_draw_demo_finger()
	draw_circle(TURBO_CENTER, TURBO_RADIUS, Color("#554274"))
	draw_circle(TURBO_CENTER, TURBO_RADIUS - 7, Color("#a5dedd"))
	var meter := float(kart["meter"])
	if meter > 0.001:
		draw_arc(TURBO_CENTER, 52, -PI * 0.5, -PI * 0.5 + TAU * meter, 48,
			Color("#ffe298"), 9, true)
	draw_colored_polygon(PackedVector2Array([TURBO_CENTER + Vector2(4, -33),
		TURBO_CENTER + Vector2(-23, 3), TURBO_CENTER + Vector2(-2, 3),
		TURBO_CENTER + Vector2(-6, 31), TURBO_CENTER + Vector2(24, -8),
		TURBO_CENTER + Vector2(4, -8)]), Color("#fff2bd"))
	if race_countdown > 0.0:
		for index in range(3):
			var lit := race_countdown <= 1.5 - float(index) * 0.5
			draw_circle(Vector2(550 + index * 90, 515), 28,
				Color("#ffe5a8") if lit else Color("#9abcc8"))


func _demo_finger_pose() -> Dictionary:
	if mode != "kart_race":
		return super._demo_finger_pose()
	return {"at": STEERING_RECT.get_center() + Vector2(sin(race_clock * 2.0) * 125.0, 0),
		"pressing": true}
