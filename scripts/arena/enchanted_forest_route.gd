extends RefCounted
## Canvas route host. ReefMain owns entry policy, save storage and spoken cues.
## The host owns an attached actor until teardown returns it to the caller.

signal objective_changed(key: StringName, world_point: Vector2)
signal progress_changed(bridge_bits: int, cove_charm: bool)

const Terrain := preload("res://scripts/arena/enchanted_forest_terrain.gd")
const Bridge := preload("res://scripts/arena/enchanted_forest_shell_bridge.gd")
const Cove := preload("res://scripts/arena/enchanted_forest_reed_cove.gd")
const Valley := preload("res://scripts/arena/enchanted_forest_landing_valley.gd")

const LANDING := Vector2(660, 1190)
const COVE_APPROACH := Vector2(2335, 1190)
const BRIDGE_STAND := Vector2(-83, 43)
const SPEED := 514.0

enum Action { WALK, COVE_WAYMARK, COVE_CONTROL, BRIDGE_SHELL }

var _root: Node2D
var _ground: Node2D
var _terrain: Terrain
var _bridge: Bridge
var _cove: Cove
var _camera: Camera2D
var _previous_camera: Camera2D
var _actor: Node2D
var _valley := Valley.new()
var _wildlife_hit: Callable
var _path := PackedVector2Array()
var _action := Action.WALK
var _target := -1
var _contact_time := 0.0
var _bridge_bits := 0
var _bridge_opening := 0.0
var _clock := 0.0
var _objective: StringName
var _objective_point := Vector2.INF


## Actor and parent must use one Canvas and the actor must be unattached.
## The caller supplies persisted progress and retains its existing save lifecycle.
func mount(parent: Node2D, actor: Node2D, spawn: Vector2,
		bridge_bits: int, cove_charm: bool, wildlife_hit: Callable = Callable()) -> bool:
	if is_instance_valid(_root) or not is_instance_valid(parent) or not is_instance_valid(actor):
		return false
	if not parent.is_inside_tree() or actor.get_parent() != null or not spawn.is_finite():
		return false
	_root = Node2D.new()
	_root.name = "EnchantedForestRoute"
	parent.add_child(_root)
	_previous_camera = _root.get_viewport().get_camera_2d()
	_terrain = Terrain.new()
	_terrain.z_index = -30
	_root.add_child(_terrain)
	_bridge_bits = bridge_bits & 3
	_bridge_opening = 1.0 if _bridge_bits == 3 else 0.0
	_terrain.bridge_open = _bridge_opening == 1.0
	_bridge = Bridge.new()
	_root.add_child(_bridge)
	_bridge.sync(_bridge_bits, _bridge_opening)
	_cove = Cove.new()
	_cove.position = Terrain.LILY_BASIN
	_cove.z_index = 3
	_cove.found = cove_charm
	_cove.discovery.connect(_publish_progress)
	_root.add_child(_cove)
	_ground = Node2D.new()
	_ground.name = "GroundedSprites"
	_ground.y_sort_enabled = true
	_root.add_child(_ground)
	_actor = actor
	_ground.add_child(_actor)
	_actor.position = _terrain.safe_point(spawn, LANDING)
	_wildlife_hit = wildlife_hit
	_valley.build(_ground, _can_place_scenery)
	_camera = Camera2D.new()
	_camera.zoom = Vector2.ONE * 0.98
	_root.add_child(_camera)
	_camera.make_current()
	_update_camera(0.0, true)
	_camera.force_update_scroll()
	return true


## One shared transform serves taps, drags and the caller's on-screen pointer.
func screen_from_world(point: Vector2) -> Vector2:
	return _root.get_global_transform_with_canvas() * point if is_instance_valid(_root) else Vector2.INF


func handle_touch(screen: Vector2) -> bool:
	if not is_instance_valid(_root) or not screen.is_finite():
		return false
	var point: Vector2 = _root.get_global_transform_with_canvas().affine_inverse() * screen
	if _bridge.cove_waymark_at(point):
		_request(COVE_APPROACH, Action.COVE_WAYMARK)
		return true
	var global_point: Vector2 = _root.to_global(point)
	var control: int = _cove.target(global_point)
	if control >= 0:
		if not _cove.hits_painted_control(global_point, control) and _hit_wildlife(point):
			cancel_navigation()
			return true
		_request(_root.to_local(_cove.interaction_stand(control)), Action.COVE_CONTROL, control)
		return true
	var shell: int = _bridge.switch_at(point)
	if shell >= 0 and not (_bridge_bits & (1 << shell)):
		_request(Bridge.SWITCHES[shell] + BRIDGE_STAND, Action.BRIDGE_SHELL, shell)
	elif not _hit_wildlife(point):
		_request(point)
	else:
		cancel_navigation()
	return true


func handle_drag(screen: Vector2) -> bool:
	if not is_instance_valid(_root) or not screen.is_finite():
		return false
	_request(_root.get_global_transform_with_canvas().affine_inverse() * screen)
	return true


func cancel_navigation() -> void:
	_path.clear()
	_action = Action.WALK
	_target = -1
	_contact_time = 0.0
	if is_instance_valid(_cove):
		_cove.select_target(-1)
	_set_objective(&"", Vector2.INF)


## Called by the route owner only while this world is active.
func tick(delta: float) -> void:
	if not is_instance_valid(_root):
		return
	_clock += delta
	if not _path.is_empty():
		var next: Vector2 = _actor.position.move_toward(_path[0], SPEED * delta)
		if not _terrain.contains(next):
			cancel_navigation()
			return
		_actor.position = next
		if _actor.position == _path[0]:
			_path.remove_at(0)
			if _path.is_empty():
				_arrive()
	elif _contact_time > 0.0:
		_contact_time = maxf(0.0, _contact_time - delta)
		if _contact_time == 0.0:
			_finish_contact()
	if _bridge_bits == 3 and not _terrain.bridge_open:
		_bridge_opening = move_toward(_bridge_opening, 1.0, delta / 0.86)
		_bridge.sync(_bridge_bits, smoothstep(0.0, 1.0, _bridge_opening))
		if _bridge_opening == 1.0:
			_terrain.bridge_open = true
			_bridge.celebrate()
	_bridge.tick(delta)
	_cove.tick(delta, _actor.global_position)
	_terrain.set_wind_time(_clock)
	_valley.tick(_clock, _actor.position, delta)
	_update_camera(delta)


func teardown() -> Node2D:
	cancel_navigation()
	_valley.teardown()
	var actor: Node2D
	if is_instance_valid(_actor):
		actor = _actor
		if actor.get_parent() == _ground:
			_ground.remove_child(actor)
	var restore_camera: bool = is_instance_valid(_camera) and _camera.is_current()
	if is_instance_valid(_root):
		_root.free()
	if restore_camera and is_instance_valid(_previous_camera) and _previous_camera.is_inside_tree():
		_previous_camera.make_current()
	_root = null
	_ground = null
	_actor = null
	_terrain = null
	_bridge = null
	_cove = null
	_camera = null
	_previous_camera = null
	_wildlife_hit = Callable()
	_clock = 0.0
	return actor


func _can_place_scenery(foot: Vector2) -> bool:
	return _terrain.plantable(foot) and _terrain.clear_of_trail(foot)


func _hit_wildlife(point: Vector2) -> bool:
	return _wildlife_hit.is_valid() and bool(_wildlife_hit.call(point))


func _request(point: Vector2, action: Action = Action.WALK, target: int = -1) -> void:
	if action != Action.WALK and _action == action and _target == target:
		return
	# Resolve the destination before granting an action or selecting its object.
	if action == Action.WALK and not _terrain.bridge_open:
		if _actor.position.x < Terrain.BRIDGE.x and point.x > Terrain.BRIDGE.x:
			point = Terrain.BRIDGE_APPROACH
	var dest: Vector2 = _terrain.safe_point(point, _actor.position)
	if not _terrain.contains(dest):
		return
	var path: PackedVector2Array = _terrain.route(_actor.position, dest)
	if point.distance_to(dest) > 8.0 and action != Action.WALK:
		return
	if path.is_empty() and _actor.position.distance_to(dest) > 2.0:
		return
	_path = path
	_contact_time = 0.0
	_action = action
	_target = target
	_cove.select_target(target if action == Action.COVE_CONTROL else -1)
	if action == Action.COVE_WAYMARK or action == Action.COVE_CONTROL:
		_set_objective(&"", Vector2.INF)
	if _path.is_empty():
		_arrive()


func _arrive() -> void:
	match _action:
		Action.COVE_WAYMARK:
			_action = Action.WALK
			if not _cove.found:
				_set_objective(&"forest_cove_valve", _root.to_local(_cove.interaction_point(1)))
		Action.COVE_CONTROL:
			_contact_time = 0.10
		Action.BRIDGE_SHELL:
			_contact_time = 0.30
		Action.WALK:
			_update_bridge_objective()


func _finish_contact() -> void:
	var action: Action = _action
	var target: int = _target
	_action = Action.WALK
	_target = -1
	if action == Action.COVE_CONTROL:
		_cove.interact(target)
		_set_objective(&"", Vector2.INF)
	elif action == Action.BRIDGE_SHELL:
		_bridge_bits |= 1 << target
		_bridge.sync(_bridge_bits, _bridge_opening)
		_publish_progress()
		_update_bridge_objective()


func _update_bridge_objective() -> void:
	if _bridge_bits != 3 and _actor.position.distance_to(Terrain.BRIDGE_APPROACH) < 320.0:
		var next_shell: int = 0 if not (_bridge_bits & 1) else 1
		_set_objective(&"forest_bridge_shells", Bridge.SWITCHES[next_shell])
	else:
		_set_objective(&"", Vector2.INF)


func _set_objective(key: StringName, point: Vector2) -> void:
	if _objective == key and _objective_point == point:
		return
	_objective = key
	_objective_point = point
	objective_changed.emit(key, point)


func _publish_progress() -> void:
	progress_changed.emit(_bridge_bits, _cove.found)


func _update_camera(delta: float, snap: bool = false) -> void:
	var pond_framing: float = 1.0 - smoothstep(95.0, 255.0,
		_actor.position.distance_to(COVE_APPROACH))
	var lead: float = 110.0 - pond_framing * 116.0
	var target: Vector2 = _actor.position - Vector2(0, lead)
	_camera.position = target if snap else _camera.position.lerp(target, 1.0 - exp(-delta * 5.8))
