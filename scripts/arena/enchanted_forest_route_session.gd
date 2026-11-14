extends RefCounted
## Production boundaries for the Forest route. The current game has no caller.

const Route := preload("res://scripts/arena/enchanted_forest_route.gd")
const SAVE_KEY := "enchanted_forest_route"
const GUIDE_MODE := "level2"

var _main: ReefMain
var _route := Route.new()
var _pointer_world := Vector2.INF
var _guide_key: StringName


func _init(main: ReefMain) -> void:
	_main = main
	_route.objective_changed.connect(_on_objective)
	_route.progress_changed.connect(_write_progress)


## The caller chooses the entry and supplies the current character and wildlife.
func mount(parent: Node2D, actor: Node2D, spawn: Vector2,
		wildlife_hit: Callable = Callable()) -> bool:
	var saved: Dictionary = _stored_progress()
	var raw_bits: Variant = saved.get("bridge_bits", 0)
	var bits: int = clampi(int(raw_bits), 0, 3) if raw_bits is int or raw_bits is float else 0
	var charm: Variant = saved.get("cove_charm", false)
	return _route.mount(parent, actor, spawn, bits, charm is bool and charm, wildlife_hit)


func handle_touch(screen: Vector2) -> bool:
	return _can_receive_input() and _route.handle_touch(screen)


func handle_drag(screen: Vector2) -> bool:
	return _can_receive_input() and _route.handle_drag(screen)


func cancel_navigation() -> void:
	_route.cancel_navigation()


func tick(delta: float) -> void:
	if not _can_receive_input():
		cancel_navigation()
		return
	_route.tick(delta)


func objective_screen_position() -> Vector2:
	return _route.screen_from_world(_pointer_world) if _pointer_world.is_finite() else Vector2.INF


func teardown() -> Node2D:
	return _route.teardown()


func _can_receive_input() -> bool:
	return _main.game == GUIDE_MODE and not _main._world_tap_gated()


func _stored_progress() -> Dictionary:
	var value: Variant = _main.save_data.get(SAVE_KEY, {})
	return value as Dictionary if value is Dictionary else {}


func _write_progress(bits: int, charm: bool) -> void:
	# SaveState owns compatibility, atomic writes and backup recovery.
	var next: Dictionary = _stored_progress().duplicate(true)
	next["bridge_bits"] = bits
	next["cove_charm"] = charm
	_main.save_data[SAVE_KEY] = next
	_main._write_save()


func _on_objective(key: StringName, world_point: Vector2) -> void:
	_pointer_world = world_point
	if key == _guide_key:
		return
	var sound: AudioDirector = _main._audio_ref()
	if _guide_key != &"":
		sound.clear_objective_guide(GUIDE_MODE, String(_guide_key))
	_guide_key = key
	if key != &"":
		sound.objective_guide(String(key))
