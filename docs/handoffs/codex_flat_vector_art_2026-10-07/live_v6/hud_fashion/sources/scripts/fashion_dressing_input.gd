class_name FashionDressingInput
extends Control
## Optional generous one-finger garment placement. Tapping remains sufficient.
## All gesture state lives in main.wd; closing/focus loss cannot equip later.
var m: ReefMain
var wardrobe: FashionWardrobe

func setup(main: ReefMain, owner_ui: FashionWardrobe) -> void:
	m = main
	wardrobe = owner_ui
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_meta("fashion_fixed_preview", true)

func _point(event: InputEvent) -> Vector2:
	if event is InputEventScreenTouch:
		return (event as InputEventScreenTouch).position
	if event is InputEventScreenDrag:
		return (event as InputEventScreenDrag).position
	if event is InputEventMouseButton:
		return (event as InputEventMouseButton).position
	return (event as InputEventMouseMotion).position

func _pointer(event: InputEvent) -> int:
	if event is InputEventScreenTouch:
		return (event as InputEventScreenTouch).index
	if event is InputEventScreenDrag:
		return (event as InputEventScreenDrag).index
	return -1

func card_input(event: InputEvent, id: String, card: Button) -> void:
	var pressed: bool = event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed
	pressed = pressed or (event is InputEventMouseButton and (event as InputEventMouseButton).pressed and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT)
	if not pressed or m == null or not FashionDesigner.owned(m, id):
		return
	if not (m.wd.get("fashion_drag", {}) as Dictionary).is_empty():
		card.accept_event()
		return
	var source: Texture2D = FashionSkinEngine.garment(id)
	var stage: Control = m.wd.get("stage") as Control
	if source == null or stage == null:
		return
	var ghost := TextureRect.new()
	ghost.name = "FashionDraggedGarment"
	ghost.texture = source
	ghost.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	ghost.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	ghost.size = Vector2(152,152)
	ghost.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ghost.z_index = 30
	stage.add_child(ghost)
	# GUI-local card position is converted through the same stage transform.
	var global: Vector2 = card.get_global_transform_with_canvas() * _point(event)
	var local: Vector2 = stage.get_global_transform_with_canvas().affine_inverse() * global
	ghost.position = local - ghost.size * 0.5
	m.wd["fashion_drag"] = {"pointer":_pointer(event),"id":id,"start":global,"last":global,"moved":false,"ghost":ghost}
	card.accept_event()

func _input(event: InputEvent) -> void:
	if m == null or not is_instance_valid(m.wardrobe_layer):
		return
	var viewport: Viewport = get_viewport()
	var drag: Dictionary = m.wd.get("fashion_drag", {}) as Dictionary
	if drag.is_empty():
		var cancelled: Variant = m.wd.get("fashion_cancelled_release")
		if cancelled != null and (event is InputEventScreenTouch or event is InputEventScreenDrag or event is InputEventMouseButton or event is InputEventMouseMotion) and _pointer(event) == int(cancelled):
			var new_press: bool = event is InputEventScreenTouch and (event as InputEventScreenTouch).pressed
			new_press = new_press or (event is InputEventMouseButton and (event as InputEventMouseButton).pressed)
			if new_press:
				m.wd.erase("fashion_cancelled_release")
			else:
				viewport.set_input_as_handled()
		return
	if not (event is InputEventScreenTouch or event is InputEventScreenDrag or event is InputEventMouseButton or event is InputEventMouseMotion):
		return
	if _pointer(event) != int(drag["pointer"]):
		viewport.set_input_as_handled()
		return
	var point: Vector2 = _point(event)
	var stage: Control = m.wd.get("stage") as Control
	var ghost: TextureRect = drag.get("ghost") as TextureRect
	if stage == null or ghost == null:
		cancel()
		return
	drag["last"] = point
	drag["moved"] = bool(drag["moved"]) or point.distance_to(drag["start"] as Vector2) > 24.0
	ghost.position = stage.get_global_transform_with_canvas().affine_inverse() * point - ghost.size * 0.5
	var released: bool = event is InputEventScreenTouch and not (event as InputEventScreenTouch).pressed
	released = released or (event is InputEventMouseButton and not (event as InputEventMouseButton).pressed and (event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT)
	if released:
		var fit: Rect2 = m.wd.get("fashion_fit_rect", Rect2()) as Rect2
		var local: Vector2 = stage.get_global_transform_with_canvas().affine_inverse() * point
		var accepted: bool = not bool(drag["moved"]) or fit.has_point(local)
		var chosen: String = String(drag["id"])
		cancel()
		if accepted:
			wardrobe._pick(chosen)
		else:
			wardrobe._cue("help")
	viewport.set_input_as_handled()

func cancel(block_release: bool = false) -> void:
	if m == null:
		return
	var drag: Dictionary = m.wd.get("fashion_drag", {}) as Dictionary
	if block_release and not drag.is_empty():
		m.wd["fashion_cancelled_release"] = drag["pointer"]
	var ghost: TextureRect = drag.get("ghost") as TextureRect
	if is_instance_valid(ghost):
		ghost.queue_free()
	m.wd["fashion_drag"] = {}

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_WINDOW_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED:
		cancel(true)

func _exit_tree() -> void:
	if m != null and m.wd.get("dressing_input") == self:
		cancel()
