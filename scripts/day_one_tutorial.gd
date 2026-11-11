class_name DayOneTutorial
extends CanvasLayer
## A stalled Day One objective can offer one picture button beside its live target.

const HELP_SECONDS := 3.0
const HAND := preload("res://assets/castle/training/ghost_hand.png")
const BUTTON_SIZE := Vector2(112.0, 112.0)
const EDGE := Vector2(18.0, 18.0)

var main: ReefMain
var button: Button
var _hand: TextureRect
var _step: StringName
var _progress: Variant
var _idle := 0.0
var _focused := true
var _application_paused := false


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	layer = 29
	hide()
	button = Button.new()
	button.name = "DayOneHelp"
	button.focus_mode = Control.FOCUS_NONE
	button.custom_minimum_size = BUTTON_SIZE
	button.size = BUTTON_SIZE
	button.hide()
	StorybookUI.style_picture_button(button, StorybookUI.PAPER, StorybookUI.GOLD, 34)
	button.pressed.connect(_use_help)
	add_child(button)
	_hand = TextureRect.new()
	_hand.texture = HAND
	_hand.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hand.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hand.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hand.position = Vector2(18.0, 18.0)
	_hand.size = Vector2(76.0, 76.0)
	_hand.pivot_offset = _hand.size * 0.5
	button.add_child(_hand)


func _notification(what: int) -> void:
	match what:
		NOTIFICATION_APPLICATION_FOCUS_OUT:
			_focused = false
			_clear()
		NOTIFICATION_APPLICATION_FOCUS_IN:
			_focused = true
		NOTIFICATION_APPLICATION_PAUSED:
			_application_paused = true
			_clear()
		NOTIFICATION_APPLICATION_RESUMED:
			_application_paused = false


func _process(delta: float) -> void:
	_update_help(_current_offer(), delta)


func _update_help(offer: Dictionary, delta: float) -> void:
	if offer.is_empty():
		_clear()
		return
	var step: StringName = offer["step"]
	var progress: Variant = offer.get("progress")
	if step != _step or progress != _progress:
		_step = step
		_progress = progress
		_idle = 0.0
		_hide_button()
		return
	_idle += maxf(delta, 0.0)
	if _idle < float(offer.get("delay", HELP_SECONDS)) or not bool(offer.get("ready", true)):
		_hide_button()
		return
	var target: Vector2 = offer["point"]
	var target_bounds: Rect2 = offer.get("bounds", Rect2(target - Vector2(40.0, 40.0), Vector2(80.0, 80.0)))
	var position: Vector2 = _position_for(target, target_bounds)
	if not position.is_finite():
		_hide_button()
		return
	layer = int(offer.get("layer", 29))
	button.position = position
	# A stalled gesture still gets a hint. Let its release reach the activity.
	button.mouse_filter = Control.MOUSE_FILTER_IGNORE if offer.get("gesture_held", false) \
		else Control.MOUSE_FILTER_STOP
	button.tooltip_text = String(offer["label"])
	var direction: Vector2 = (target - (position + BUTTON_SIZE * 0.5)).normalized()
	_hand.rotation = Vector2.DOWN.angle_to(direction)
	_hand.position = Vector2(18.0, 18.0) + direction * sin(_idle * 5.0) * 7.0
	show()
	button.show()


func _position_for(target: Vector2, target_bounds: Rect2) -> Vector2:
	var viewport: Rect2 = get_viewport().get_visible_rect()
	var spacing: Vector2 = (target_bounds.size + BUTTON_SIZE) * 0.5 + Vector2(22.0, 22.0)
	var reserved: Array[Rect2] = [target_bounds]
	for control: Control in [main.castle_voice_caption, main.hud_msg, main.global_navigation_button]:
		if is_instance_valid(control) and control.is_visible_in_tree():
			reserved.append(_canvas_bounds(control))
	for offset: Vector2 in [Vector2(0.0, -spacing.y), Vector2(0.0, spacing.y),
			Vector2(-spacing.x, 0.0), Vector2(spacing.x, 0.0)]:
		var position: Vector2 = (target + offset - BUTTON_SIZE * 0.5).clamp(
			viewport.position + EDGE, viewport.end - BUTTON_SIZE - EDGE)
		var proposed := Rect2(position, BUTTON_SIZE)
		var clear := true
		for occupied: Rect2 in reserved:
			if proposed.intersects(occupied.grow(8.0)):
				clear = false
				break
		if clear:
			return position
	return Vector2.INF


static func _canvas_bounds(control: Control) -> Rect2:
	return control.get_global_transform_with_canvas() * Rect2(Vector2.ZERO, control.size)


func _clear() -> void:
	_step = &""
	_progress = null
	_idle = 0.0
	_hide_button()


func _hide_button() -> void:
	hide()
	if is_instance_valid(button):
		button.hide()


func _use_help() -> void:
	if not button.visible:
		return
	var offer: Dictionary = _current_offer()
	if offer.is_empty() or offer["step"] != _step or offer.get("progress") != _progress \
			or not bool(offer.get("ready", true)):
		_clear()
		return
	if bool(offer.get("gesture_held", false)):
		return
	var action: Callable = offer["action"]
	_clear()
	if action.is_valid():
		action.call()


static func at(step: StringName, point: Vector2, action: Callable, label: String,
		progress: Variant = null, gesture_held: bool = false) -> Dictionary:
	return {"step": step, "point": point, "action": action, "label": label,
		"progress": progress, "gesture_held": gesture_held}


static func for_button(step: StringName, target: Button, label: String,
		action: Callable = Callable()) -> Dictionary:
	if not is_instance_valid(target) or not target.is_visible_in_tree() \
			or target.disabled or target.mouse_filter == Control.MOUSE_FILTER_IGNORE:
		return {}
	var callback: Callable = action if action.is_valid() else func() -> void: target.pressed.emit()
	var bounds: Rect2 = _canvas_bounds(target)
	var offer: Dictionary = at(step, bounds.get_center(), callback, label)
	offer["bounds"] = bounds
	return offer


func _current_offer() -> Dictionary:
	if not _focused or _application_paused or not is_instance_valid(main) \
			or main._pause_ref()._navigation_locked() \
			or (is_instance_valid(main.pause_panel) and main.pause_panel.visible):
		return {}
	var clip: DayOneStoryClips = main._day_one_story_clip
	if is_instance_valid(clip):
		return for_button(StringName("story_skip_%d" % clip.get_instance_id()),
			main.global_navigation_button, "Skip this story", clip.skip)
	if get_tree().paused or not main.day_one_is_active():
		return {}
	var route: String = main._navigation_ref().top_id()
	match route:
		"day_one_lagoon_playground":
			return _navigation_offer(&"playground_back", "Back to Sky Lagoon")
		"attack_customizer":
			if is_instance_valid(main._day_one_art_studio) and is_instance_valid(main._attack_customizer):
				var picker: AttackCustomizer = main._attack_customizer
				var confirm: Button = picker.find_child("AttackCustomizerConfirm", true, false) as Button
				var offer: Dictionary = for_button(&"art_confirm", confirm, "Use this magic attack")
				if not offer.is_empty():
					offer["progress"] = [picker.attack_color, picker.attack_effect]
				return offer
			return {}
		"stuffie_picker":
			if main.castle_room_id == "playroom" and is_instance_valid(main.companion_layer):
				var confirm: Button = main.companion_layer.find_child("StuffieConfirmButton", true, false) as Button
				var offer: Dictionary = for_button(&"eagle_confirm", confirm, "Take this friend along")
				if not offer.is_empty():
					offer["progress"] = main.companion_pick_id
				return offer
			return {}
		"day_one_art_studio":
			if is_instance_valid(main._day_one_art_studio):
				return main._day_one_art_studio.tutorial_offer()
			return {}
	if main.game == "dustboss":
		var boss: DustBossGame = main._game_obj("dustboss", DustBossGame) as DustBossGame
		return boss.tutorial_offer()
	if main.game != "level2":
		return {}
	if route == "pearl_castle" and main.castle_room_id == "main_hall":
		return _hall_offer()
	if route == "pearl_castle_room":
		return _room_offer()
	if main.game == "level2" and main.g.get("phase") == "promenade" \
			and main._navigation_ref().at_sky_lagoon_root():
		return main._lagoon_promenade_ref().tutorial_offer()
	return {}


func _navigation_offer(step: StringName, label: String) -> Dictionary:
	return for_button(step, main.global_navigation_button, label, main._navigation_ref().press)


func _hall_offer() -> Dictionary:
	var next_door: String = main._castle_rooms_ref().active_door_highlight_id()
	for record: Dictionary in main.castle_room_door_hotspots:
		var data: Dictionary = record["data"]
		if String(data["id"]) == next_door:
			return for_button(StringName("hall_" + next_door), record["button"] as Button,
				"Go through the glowing door")
	return {}


func _room_offer() -> Dictionary:
	if main._day_one_room_handoff_source == main.castle_room_id \
			and not main._day_one_room_handoff_target.is_empty():
		return _navigation_offer(&"room_back", "Back to the hall")
	match main.castle_room_id:
		"bubble_bath":
			if is_instance_valid(main._day_one_bathroom_cleanup):
				return main._day_one_bathroom_cleanup.tutorial_offer()
		"mermaid_pool":
			var pool: DayOnePoolCleanup = main._castle_rooms_ref().day_one_pool_cleanup
			if is_instance_valid(pool):
				return pool.tutorial_offer()
		"playroom":
			return main._castle_rooms_ref().day_one_rescue_tutorial_offer()
	return {}
