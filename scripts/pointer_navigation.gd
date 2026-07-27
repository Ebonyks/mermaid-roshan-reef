class_name PointerNavigation
extends RefCounted
# One persistent point-and-goal channel shared by fixed rooms, flat stages and
# rails. TouchUI decides whether a press belongs to UI, an action or a gesture;
# InteractionDirector decides target versus open ground. Only an unclaimed
# ground press reaches this class.

const ARRIVAL_X := 0.35
const ARRIVAL_2D := 0.55

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func set_context(context: String) -> void:
	cancel("context")
	m.pointer_nav_context = context

func clear_context(context: String = "") -> void:
	if not context.is_empty() and m.pointer_nav_context != context:
		return
	cancel("context")
	m.pointer_nav_context = ""

func begin(screen_pos: Vector2) -> bool:
	if m.pointer_nav_context.is_empty():
		return false
	m.pointer_nav_goal_screen = screen_pos
	m.pointer_nav_goal_active = true
	m.pointer_nav_pointer_down = true
	m.pointer_nav_press_edge = true
	m.pointer_nav_world_valid = false
	return true

func update(screen_pos: Vector2) -> void:
	if not m.pointer_nav_pointer_down:
		return
	m.pointer_nav_goal_screen = screen_pos
	m.pointer_nav_goal_active = true
	m.pointer_nav_world_valid = false

func finish(screen_pos: Vector2) -> void:
	m.pointer_nav_goal_screen = screen_pos
	m.pointer_nav_pointer_down = false
	m.pointer_nav_world_valid = false

func cancel(_reason: String = "") -> void:
	m.pointer_nav_goal_active = false
	m.pointer_nav_pointer_down = false
	m.pointer_nav_press_edge = false
	m.pointer_nav_world_valid = false

func has_goal() -> bool:
	return m.pointer_nav_goal_active and not m.pointer_nav_context.is_empty()

func consume_press() -> bool:
	var pressed: bool = m.pointer_nav_press_edge
	m.pointer_nav_press_edge = false
	return pressed

func screen_distance_to(world_pos: Vector3) -> float:
	var camera: Camera3D = m.get_viewport().get_camera_3d()
	if camera == null or camera.is_position_behind(world_pos):
		return INF
	return camera.unproject_position(world_pos).distance_to(m.pointer_nav_goal_screen)

func axis_x(manual: float, current_x: float, min_x: float, max_x: float) -> float:
	if absf(manual) > 0.05:
		cancel("manual")
		return clampf(manual, -1.0, 1.0)
	if not has_goal():
		return 0.0
	var target_x: float = lerpf(min_x, max_x, _screen_fraction().x)
	var distance: float = target_x - current_x
	if absf(distance) <= ARRIVAL_X:
		m.pointer_nav_goal_active = false
		return 0.0
	return signf(distance)

func axis_stage(manual: Vector2, current: Vector2, bounds: Rect2) -> Vector2:
	if manual.length() > 0.05:
		cancel("manual")
		return manual.limit_length(1.0)
	if not has_goal():
		return Vector2.ZERO
	var fraction: Vector2 = _screen_fraction()
	var target := Vector2(
		lerpf(bounds.position.x, bounds.end.x, fraction.x),
		lerpf(bounds.position.y, bounds.end.y, fraction.y))
	var distance: Vector2 = target - current
	if distance.length() <= ARRIVAL_2D:
		m.pointer_nav_goal_active = false
		return Vector2.ZERO
	return distance.normalized()

func axis_world(manual: Vector2, current: Vector3, plane_y: float) -> Vector2:
	if manual.length() > 0.05:
		cancel("manual")
		return manual.limit_length(1.0)
	if not has_goal():
		return Vector2.ZERO
	if not m.pointer_nav_world_valid:
		m.pointer_nav_goal_world = _project_to_horizontal_plane(plane_y)
		m.pointer_nav_world_valid = true
	var target: Vector3 = m.pointer_nav_goal_world
	var distance := Vector2(target.x - current.x, target.z - current.z)
	if distance.length() <= ARRIVAL_2D:
		m.pointer_nav_goal_active = false
		return Vector2.ZERO
	return distance.normalized()

func _screen_fraction() -> Vector2:
	var viewport: Viewport = m.get_viewport()
	if viewport == null:
		return Vector2(0.5, 0.5)
	var visible: Rect2 = viewport.get_visible_rect()
	if visible.size.x <= 1.0 or visible.size.y <= 1.0:
		return Vector2(0.5, 0.5)
	return Vector2(
		clampf((m.pointer_nav_goal_screen.x - visible.position.x) / visible.size.x, 0.0, 1.0),
		clampf((m.pointer_nav_goal_screen.y - visible.position.y) / visible.size.y, 0.0, 1.0))

func _project_to_horizontal_plane(plane_y: float) -> Vector3:
	var camera: Camera3D = m.get_viewport().get_camera_3d()
	if camera == null:
		return Vector3.ZERO
	var origin: Vector3 = camera.project_ray_origin(m.pointer_nav_goal_screen)
	var direction: Vector3 = camera.project_ray_normal(m.pointer_nav_goal_screen)
	if absf(direction.y) <= 0.001:
		return origin + direction * 40.0
	var ray_t: float = (plane_y - origin.y) / direction.y
	if ray_t <= 0.0:
		return origin + direction * 40.0
	return origin + direction * minf(ray_t, 160.0)
