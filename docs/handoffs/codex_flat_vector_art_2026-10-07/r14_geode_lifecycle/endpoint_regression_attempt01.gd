extends SceneTree
var awards: Array[String] = []
var failed := false
func _init() -> void:
	call_deferred("_run")
func _award(kind: String, _amount: float, _quality: float) -> void:
	awards.append(kind)
func _touch(surface: OperaGeologySurface, point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = point
	event.pressed = pressed
	surface._gui_input(event)
func _drag(surface: OperaGeologySurface, point: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = point
	surface._gui_input(event)
func _run() -> void:
	var surface := OperaGeologySurface.new()
	get_root().add_child(surface)
	surface.action.connect(_award)
	for saved_pull: float in [119.0,119.25]:
		awards.clear()
		surface.configure("geology_geode",Color.WHITE)
		surface.armed_only = false
		surface.restore_progress({"mode":"geology_geode","seams":[true,true,true,true,true],"pull":saved_pull})
		var half := surface.geode_half_center()
		_touch(surface,half,true)
		_drag(surface,half+Vector2(8,0))
		_touch(surface,half+Vector2(8,0),false)
		var ok := surface.geode_pull == 120.0 and awards == ["geology_geode"]
		print("GEODE_ENDPOINT|",saved_pull,"|travel8|pull=",surface.geode_pull,"|awards=",awards,"|", "PASS" if ok else "FAIL")
		failed = failed or not ok
	surface.queue_free()
	await process_frame
	quit(1 if failed else 0)
