class_name TapMoveDirector
extends RefCounted
# Assisted movement never teleports or writes the player transform. It supplies
# a steering intention to player.gd, which keeps the existing acceleration,
# arena bounds, terrain floor and collision behavior authoritative.

const ARRIVAL_DISTANCE := 2.8
const STALL_WINDOW := 1.15
const MAX_RECOVERIES := 2
# Readiness in InteractionDirector discounts vertical offset by this weight.
# Arrival and stall tracking for interactable routes MUST use the same metric,
# or assisted travel stops at a spot the readiness check rejects and the child
# is told "Tap again!" forever (the elevated-portal wedge).
const VERTICAL_WEIGHT := 0.35

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func start(target: Vector3, interactable_id: String = "", activation_radius: float = 5.0) -> void:
	if m.player == null:
		return
	var clamped_target := _clamp_target(target)
	m.touch_auto_active = true
	m.touch_auto_target = clamped_target
	m.touch_auto_waypoint = Vector3.ZERO
	m.touch_auto_interactable = interactable_id
	m.touch_auto_activation_radius = maxf(activation_radius, ARRIVAL_DISTANCE)
	m.touch_auto_last_distance = _route_distance(m.player.position, clamped_target)
	m.touch_auto_stall_t = 0.0
	m.touch_auto_recoveries = 0

func start_from_screen(screen_pos: Vector2) -> bool:
	if m.player == null:
		return false
	var camera: Camera3D = m.get_viewport().get_camera_3d()
	if camera == null:
		return false
	var origin: Vector3 = camera.project_ray_origin(screen_pos)
	var direction: Vector3 = camera.project_ray_normal(screen_pos)
	var plane_y: float = m.player.position.y
	var target: Vector3
	if absf(direction.y) > 0.025:
		var ray_t: float = (plane_y - origin.y) / direction.y
		if ray_t > 1.0:
			target = origin + direction * minf(ray_t, 120.0)
		else:
			target = origin + direction * 48.0
	else:
		target = origin + direction * 48.0
	target.y = plane_y
	if _horizontal_distance(target, m.player.position) < 3.0:
		return false
	start(target)
	return true

func cancel(_reason: String = "") -> void:
	m.touch_auto_active = false
	m.touch_auto_waypoint = Vector3.ZERO
	m.touch_auto_interactable = ""
	m.touch_auto_stall_t = 0.0

func tick(delta: float) -> void:
	if not m.touch_auto_active or m.player == null:
		return
	var target: Vector3 = _steering_target()
	if m.touch_auto_waypoint != Vector3.ZERO and _horizontal_distance(m.player.position, target) <= ARRIVAL_DISTANCE:
		m.touch_auto_waypoint = Vector3.ZERO
		m.touch_auto_last_distance = _route_distance(m.player.position, m.touch_auto_target)
		m.touch_auto_stall_t = 0.0
		return
	var distance: float = _route_distance(m.player.position, target)
	var arrival: float = ARRIVAL_DISTANCE
	if not m.touch_auto_interactable.is_empty():
		# 0.9: strictly inside the readiness boundary (weighted distance <=
		# activation radius), so declaring arrival always yields a live button
		arrival = maxf(ARRIVAL_DISTANCE, m.touch_auto_activation_radius * 0.9)
	if m.touch_auto_waypoint == Vector3.ZERO and distance <= arrival:
		var arrived_id: String = m.touch_auto_interactable
		m.touch_auto_active = false
		m.touch_auto_interactable = ""
		if not arrived_id.is_empty():
			m._touch_interaction_ready(arrived_id)
		return
	if distance + 0.18 < m.touch_auto_last_distance:
		m.touch_auto_last_distance = distance
		m.touch_auto_stall_t = 0.0
	else:
		m.touch_auto_stall_t += delta
	if m.touch_auto_stall_t < STALL_WINDOW:
		return
	m.touch_auto_stall_t = 0.0
	if m.touch_auto_recoveries >= MAX_RECOVERIES:
		cancel("stalled")
		m.show_msg("Roshan", "That way is snug. Tap another nearby spot!", "hint")
		return
	m.touch_auto_recoveries += 1
	var to_goal: Vector3 = m.touch_auto_target - m.player.position
	to_goal.y = 0.0
	if to_goal.length() < 0.01:
		cancel("arrived")
		return
	var side := Vector3(-to_goal.z, 0.0, to_goal.x).normalized()
	if m.touch_auto_recoveries % 2 == 0:
		side = -side
	m.touch_auto_waypoint = _clamp_target(m.player.position + side * (6.0 + float(m.touch_auto_recoveries) * 3.0))
	m.touch_auto_last_distance = _horizontal_distance(m.player.position, m.touch_auto_waypoint)

func desired_direction() -> Vector3:
	if not m.touch_auto_active or m.player == null:
		return Vector3.ZERO
	var direction: Vector3 = _steering_target() - m.player.position
	direction.y = 0.0
	return direction.normalized() if direction.length() > 0.01 else Vector3.ZERO

func desired_vertical() -> float:
	# Vertical steering intention in units/s toward the FINAL target. Elevated
	# interactables (Butterfly portal, penguin floe) are unreachable by yaw/fwd
	# steering alone. player.gd applies this only in the swim medium — on dry
	# land or breached above the surface it is ignored, and a blocked climb
	# degrades into the normal stall -> recovery -> friendly cancel path.
	if not m.touch_auto_active or m.player == null or m.touch_auto_interactable.is_empty():
		return 0.0
	var dy: float = m.touch_auto_target.y - m.player.position.y
	if absf(dy) < 1.2:
		return 0.0
	return clampf(dy * 0.8, -7.0, 9.0)

func _steering_target() -> Vector3:
	return m.touch_auto_waypoint if m.touch_auto_waypoint != Vector3.ZERO else m.touch_auto_target

func _route_distance(a: Vector3, b: Vector3) -> float:
	# Interactable routes progress in the same weighted metric readiness uses;
	# open-space swims stay purely horizontal (their target y is the tap plane).
	if m.touch_auto_interactable.is_empty():
		return _horizontal_distance(a, b)
	return _horizontal_distance(a, b) + absf(a.y - b.y) * VERTICAL_WEIGHT

func _clamp_target(target: Vector3) -> Vector3:
	var center := Vector2.ZERO
	var radius: float = m.WORLD_R - 4.0
	if m.game != "":
		center = Vector2(m.arena_center.x, m.arena_center.z)
		radius = maxf(8.0, m.arena_dome - 4.0)
	var offset := Vector2(target.x, target.z) - center
	if offset.length() > radius:
		offset = offset.normalized() * radius
	target.x = center.x + offset.x
	target.z = center.y + offset.y
	return target

func _horizontal_distance(a: Vector3, b: Vector3) -> float:
	return Vector2(a.x - b.x, a.z - b.z).length()
