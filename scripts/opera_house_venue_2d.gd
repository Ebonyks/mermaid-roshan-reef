class_name OperaHouseVenue2D
extends Control
## Four physical galleries, four doors each. Save slots stay sparse and stable;
## the sixteenth door is a mystery, never an invented activity or completion bit.

const CANVAS_SIZE := Vector2(1280, 720)
const ART_ROOT := "res://assets/flats/castle/opera_house_four_floors/"
const ROSHAN_TEXTURE := "res://assets/characters/roshan_25d/roshan_base.png"
const GHOST_HAND_TEXTURE := "res://assets/castle/training/ghost_hand.png"
const FLOOR_NAMES: Array[String] = ["Lagoon Lights Foyer", "Starlight Balcony",
	"Grand Gallery", "Moonlight Gallery"]
const DOOR_X: Array[float] = [452.0, 576.0, 698.0, 820.0]
const WALK_SPEED := 270.0
const LIFT_SPEED := 115.0
const ACTOR_SIZE := Vector2(74, 88)

var background_textures: Array[Texture2D] = []
var m: ReefMain
var launch_career: Callable
var buttons: Array[Button] = []
var active_act_indices: Array[int] = []
var portal_rects: Dictionary = {}
var act_floors: Dictionary = {}
var chapter2_tutorial_mode := false
var floor_index := 0
var accepting_input := false
var actor: TextureRect
var floor_glow: ColorRect
var guide_button: Button
var guide_pointer: Sprite2D
var guide_pointer_base := Vector2.ZERO
var elapsed := 0.0
var navigation := OperaVenueNavigation.new()
var access_controls: Array[Button] = []
var mystery_door: Button
var current_mask := 0
var current_stage := -1
var foot := Vector2(530, 689)
var waypoints := PackedVector2Array()
var waypoint_index := 0
var target_floor := 0
var pending_act := -1
var mystery_pending := false
var queued_target := Vector2.ZERO
var queued_floor := -1
var queued_act := -1
var queued_mystery := false
var foreground: OperaVenueForeground
var pending_interaction := ""
var queued_interaction := ""


func setup(main: ReefMain, star_mask: int, launch_callback: Callable) -> void:
	m = main
	launch_career = launch_callback
	name = "OperaHouseVenue2D"
	visible = false
	size = CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 42
	_configure_portals()
	set_meta("true_2d_venue", true)
	set_meta("floor_count", 4)
	set_meta("portal_count", 16)
	set_meta("mystery_door_count", 1)
	set_meta("chapter2_initial_tutorial_mode", chapter2_tutorial_mode)
	_build_background()
	_build_portals()
	_build_access()
	_build_actor()
	foreground = OperaVenueForeground.new()
	foreground.setup(self)
	add_child(foreground)
	refresh(star_mask)


func open(star_mask: int) -> void:
	foreground.reset_scene()
	m._navigation_push("opera_venue", self, Callable(self, "close"))
	visible = true
	accepting_input = true
	refresh(star_mask)
	guide_current_floor()
	m._say("roshan", "castle_opera_enter", 8.0)


func close() -> void:
	m._navigation_remove("opera_venue")
	accepting_input = false
	foreground.cancel(true)
	pending_interaction = ""
	queued_interaction = ""
	# Finish a cancelled transit at its last safe landing on reopening.
	waypoints.clear()
	queued_floor = -1
	pending_act = -1
	mystery_pending = false
	foot = Vector2(DOOR_X[0], OperaVenueNavigation.FLOOR_Y[floor_index])
	guide_pointer.visible = false
	visible = false


func is_open() -> bool:
	return visible


func is_chapter2_tutorial_mode() -> bool:
	return chapter2_tutorial_mode


func career_buttons() -> Array[Button]:
	return buttons.duplicate()


func _configure_portals() -> void:
	chapter2_tutorial_mode = m != null and m.chapter2_is_active() \
		and m._chapter_two_ref().is_opera_priority()
	active_act_indices = OperaVenueNavigation.LIVE_ORDER.duplicate()
	for act_index: int in active_act_indices:
		var floor_number := OperaVenueNavigation.floor_for_act(act_index)
		var column := OperaVenueNavigation.LIVE_ORDER.find(act_index) % 4
		act_floors[act_index] = floor_number
		portal_rects[act_index] = Rect2(Vector2(DOOR_X[column] - 55.0,
			OperaVenueNavigation.FLOOR_Y[floor_number] - 108.0), Vector2(110, 110))


func _completion_mask(star_mask: int) -> int:
	if m == null or not m.chapter2_is_active():
		return star_mask
	var director := m._chapter_two_ref()
	return star_mask | int(director.skill_mask) | int(director.party_piece_mask)


func _access_stage(mask: int) -> int:
	# Chapter Two retains its existing room-owned story routes. It must not
	# bypass this venue's four/eight/twelve completion gates.
	return OperaVenueNavigation.stage_for_mask(mask)


func refresh(star_mask: int) -> void:
	current_mask = _completion_mask(star_mask)
	var stage := _access_stage(current_mask)
	var changed := stage != current_stage
	if changed:
		current_stage = stage
		navigation.rebuild(stage)
		if floor_index > stage:
			floor_index = stage
			foot = Vector2(DOOR_X[0], OperaVenueNavigation.FLOOR_Y[stage])
			waypoints.clear()
			pending_act = -1
			queued_floor = -1
	for button: Button in buttons:
		var act_index := int(button.get_meta("act_index"))
		var completed := _portal_is_complete(act_index, star_mask)
		var allowed := int(act_floors[act_index]) <= current_stage \
			and m.chapter2_can_start_opera_act(act_index)
		button.disabled = not accepting_input or not allowed \
			or (m.chapter2_is_active() and completed)
		button.set_meta("complete", completed)
		button.set_meta("chapter2_skill_complete", chapter2_tutorial_mode and completed)
		button.set_meta("chapter2_party_complete", m.chapter2_is_active() \
			and not chapter2_tutorial_mode and completed)
		var portrait := button.get_node("CareerPortrait") as TextureRect
		portrait.modulate = Color.WHITE if allowed else Color(0.55, 0.53, 0.64, 0.72)
		var pearl := button.get_node("CompletionPearl") as Panel
		pearl.visible = completed
	for control: Button in access_controls:
		var required := int(control.get_meta("required_stage"))
		var unlocked := current_stage >= required
		control.set_meta("unlocked", unlocked)
		control.disabled = not accepting_input
		var gate := control.get_node("Gate") as Control
		gate.visible = not unlocked
		var light := control.get_node("LandingLight") as Panel
		light.modulate = Color(0.58, 1.0, 0.9) if unlocked else Color(0.55, 0.52, 0.66)
	mystery_door.disabled = not accepting_input or current_stage < 3
	_update_actor()
	if changed and visible:
		guide_current_floor()
		m._say("roshan", "castle_opera_enter", 8.0)


func _portal_is_complete(act_index: int, star_mask: int) -> bool:
	var bit := 1 << act_index
	if chapter2_tutorial_mode:
		return (int(m._chapter_two_ref().skill_mask) & bit) != 0
	if m != null and m.chapter2_is_active():
		return (int(m._chapter_two_ref().party_piece_mask) & bit) != 0
	return (star_mask & bit) != 0


func can_enter_act(act_index: int) -> bool:
	return accepting_input and portal_rects.has(act_index) \
		and int(act_floors[act_index]) <= current_stage \
		and m.chapter2_can_start_opera_act(act_index) \
		and not (m.chapter2_is_active() and _portal_is_complete(act_index, m.opera_stars))


func guide_current_floor() -> bool:
	guide_button = null
	for button: Button in buttons:
		if not button.disabled and not bool(button.get_meta("complete", false)):
			guide_button = button
			break
	if guide_button == null:
		guide_pointer.visible = false
		return false
	guide_pointer_base = guide_button.position + Vector2(55, 6)
	guide_pointer.position = guide_pointer_base
	guide_pointer.visible = visible and accepting_input
	return true


func _build_background() -> void:
	# Exact non-overlapping native image tiles; no stretched standees or mesh.
	for column in range(2):
		var tile := TextureRect.new()
		tile.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tile.name = "VenueTile_%d" % column
		tile.texture = background_textures[column] if background_textures.size() == 2 \
			else load(ART_ROOT + "venue_%d.png" % column) as Texture2D
		tile.position = Vector2(column * 640, 0)
		tile.size = Vector2(640, 720)
		tile.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tile.stretch_mode = TextureRect.STRETCH_SCALE
		tile.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(tile)
	var blocker := Control.new()
	blocker.name = "VenueWorldInputBlocker"
	blocker.size = CANVAS_SIZE
	blocker.mouse_filter = Control.MOUSE_FILTER_STOP
	blocker.gui_input.connect(_background_input)
	add_child(blocker)


func _button(rect: Rect2, node_name: String) -> Button:
	var button := Button.new()
	button.name = node_name
	button.position = rect.position
	button.size = rect.size
	button.text = ""
	button.mouse_filter = Control.MOUSE_FILTER_STOP
	for state: String in ["normal", "hover", "pressed", "disabled"]:
		button.add_theme_stylebox_override(state, StyleBoxEmpty.new())
	var focus := StyleBoxFlat.new()
	focus.bg_color = Color.TRANSPARENT
	focus.border_color = Color(1, 0.88, 0.52, 0.9)
	focus.set_border_width_all(3)
	focus.set_corner_radius_all(18)
	button.add_theme_stylebox_override("focus", focus)
	add_child(button)
	return button


func _build_portals() -> void:
	for act_index: int in active_act_indices:
		var rect: Rect2 = portal_rects[act_index]
		var button := _button(rect, "OperaVenuePortal_%02d" % act_index)
		button.set_meta("act_index", act_index)
		button.set_meta("floor_index", act_floors[act_index])
		button.set_meta("castle_room_id", "opera_hall")
		button.set_meta("presentation", "four_floor_painted_portal")
		button.set_meta("painted_door_hit_region", true)
		button.set_meta("opaque_card", false)
		button.set_meta("floating_decoration", false)
		button.set_meta("screen_hit_size", rect.size)
		button.tooltip_text = String((OperaHouse.ACTS[act_index] as Dictionary).get("career", ""))
		button.pressed.connect(_choose_career.bind(act_index))
		var portrait := TextureRect.new()
		portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		portrait.name = "CareerPortrait"
		var costume := String((OperaHouse.ACTS[act_index] as Dictionary).get("costume", ""))
		portrait.texture = OperaRoshanActor.idle_frame(costume, load(ROSHAN_TEXTURE) as Texture2D)
		portrait.position = Vector2(24, 20)
		portrait.size = Vector2(62, 78)
		portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		portrait.mouse_filter = Control.MOUSE_FILTER_IGNORE
		button.add_child(portrait)
		var pearl := Panel.new()
		pearl.name = "CompletionPearl"
		pearl.position = Vector2(80, 78)
		pearl.size = Vector2(16, 16)
		pearl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pearl.add_theme_stylebox_override("panel", _gold_style())
		button.add_child(pearl)
		buttons.append(button)
	mystery_door = _button(Rect2(Vector2(DOOR_X[3] - 55, 43), Vector2(110, 110)), "MysteryDoor")
	mystery_door.set_meta("mystery", true)
	mystery_door.set_meta("floor_index", 3)
	mystery_door.tooltip_text = "A mystery for another adventure"
	mystery_door.pressed.connect(_choose_mystery)


func _build_access() -> void:
	_access("LeftStairs", Rect2(210, 416, 110, 110), 1, 1, Vector2(356, 389))
	_access("RightStairs", Rect2(954, 416, 110, 110), 1, 1, Vector2(918, 389))
	_access("LeftElevatorLower", Rect2(208, 294, 110, 110), 2, 2, Vector2(263, 270))
	_access("LeftElevatorUpper", Rect2(208, 175, 110, 110), 2, 1, Vector2(263, 389))
	_access("RightElevatorLower", Rect2(955, 175, 110, 110), 3, 3, Vector2(1010, 151))
	_access("RightElevatorUpper", Rect2(955, 56, 110, 110), 3, 2, Vector2(1010, 270))


func _access(node_name: String, rect: Rect2, required: int,
		destination_floor: int, destination: Vector2) -> void:
	var button := _button(rect, node_name)
	button.set_meta("required_stage", required)
	button.set_meta("destination_floor", destination_floor)
	var source_floor := required - 1 if destination_floor == required else required
	var source_position := Vector2(rect.get_center().x, OperaVenueNavigation.FLOOR_Y[source_floor])
	button.set_meta("source_floor", source_floor)
	button.pressed.connect(_use_access.bind(required, source_floor, source_position,
		destination_floor, destination))
	var gate := Control.new()
	gate.name = "Gate"
	gate.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.add_child(gate)
	# Scene-owned rails retract entirely on unlocking; no closed gate remains
	# baked into the background and no solid barrier is walked through.
	for x in range(16, 96, 16):
		var rail := Panel.new()
		rail.position = Vector2(x, 42)
		rail.size = Vector2(5, 54)
		rail.mouse_filter = Control.MOUSE_FILTER_IGNORE
		rail.add_theme_stylebox_override("panel", _gold_style())
		gate.add_child(rail)
	for y in [48, 89]:
		var crossbar := Panel.new()
		crossbar.position = Vector2(12, y)
		crossbar.size = Vector2(86, 6)
		crossbar.mouse_filter = Control.MOUSE_FILTER_IGNORE
		crossbar.add_theme_stylebox_override("panel", _gold_style())
		gate.add_child(crossbar)
	var light := Panel.new()
	light.name = "LandingLight"
	light.position = Vector2(44, 82)
	light.size = Vector2(22, 12)
	light.mouse_filter = Control.MOUSE_FILTER_IGNORE
	light.add_theme_stylebox_override("panel", _gold_style())
	button.add_child(light)
	access_controls.append(button)


func _gold_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.96, 0.79, 0.42)
	style.border_color = Color(0.42, 0.25, 0.26)
	style.set_border_width_all(1)
	style.set_corner_radius_all(5)
	return style


func _build_actor() -> void:
	floor_glow = ColorRect.new()
	floor_glow.size = Vector2(46, 5)
	floor_glow.color = Color(1, 0.9, 0.6, 0.6)
	floor_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	floor_glow.z_index = 9
	# A flat status stripe is not a physical contact shadow.
	floor_glow.visible = false
	add_child(floor_glow)
	actor = TextureRect.new()
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.name = "LobbyRoshanCutout"
	actor.texture = load(ROSHAN_TEXTURE) as Texture2D
	actor.size = ACTOR_SIZE
	actor.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	actor.mouse_filter = Control.MOUSE_FILTER_IGNORE
	actor.z_index = 10
	add_child(actor)
	guide_pointer = Sprite2D.new()
	guide_pointer.name = "OperaDoorPointer"
	guide_pointer.texture = load(GHOST_HAND_TEXTURE) as Texture2D
	guide_pointer.scale = Vector2.ONE * 0.10
	guide_pointer.visible = false
	guide_pointer.z_index = 12
	add_child(guide_pointer)
	_update_actor()


func _background_input(event: InputEvent) -> void:
	if not accepting_input:
		return
	if event is InputEventMouseButton:
		var mouse := event as InputEventMouseButton
		if mouse.pressed and mouse.button_index == MOUSE_BUTTON_LEFT:
			point_to(mouse.position)
	elif event is InputEventScreenTouch:
		var touch := event as InputEventScreenTouch
		if touch.pressed:
			point_to(touch.position)


func point_to(point: Vector2) -> void:
	if not accepting_input:
		return
	var destination_floor := navigation.floor_at(point)
	if destination_floor > current_stage:
		guide_current_floor()
		return
	_request_walk(point, destination_floor)


func _choose_career(act_index: int) -> void:
	if not can_enter_act(act_index):
		guide_current_floor()
		return
	var rect: Rect2 = portal_rects[act_index]
	var destination_floor := int(act_floors[act_index])
	_request_walk(Vector2(rect.get_center().x, OperaVenueNavigation.FLOOR_Y[destination_floor]),
		destination_floor, act_index)


func _choose_mystery() -> void:
	if accepting_input and current_stage >= 3:
		_request_walk(Vector2(DOOR_X[3], OperaVenueNavigation.FLOOR_Y[3]), 3, -1, true)


func _use_access(required: int, source_floor: int, source_position: Vector2,
		destination_floor: int, destination: Vector2) -> void:
	if not accepting_input:
		return
	if current_stage < required:
		guide_current_floor()
		m._say("roshan", "castle_opera_enter", 8.0)
		return
	if floor_index == source_floor:
		_request_walk(destination, destination_floor)
	else:
		_request_walk(source_position, source_floor)


func request_foreground(id: String) -> void:
	if accepting_input and OperaVenueForeground.OBJECTS.has(id):
		var spec: Dictionary = OperaVenueForeground.OBJECTS[id]
		_request_walk(spec["approach"], 0, -1, false, id)


func _request_walk(destination: Vector2, destination_floor: int,
		act_index: int = -1, mystery: bool = false, interaction_id: String = "") -> void:
	foreground.cancel()
	# Retarget at the next graph vertex, including inside stairs/lifts. This
	# avoids teleporting sideways out of a shaft or cutting through a banister.
	if not waypoints.is_empty():
		queued_target = destination
		queued_floor = destination_floor
		queued_act = act_index
		queued_mystery = mystery
		queued_interaction = interaction_id
		pending_interaction = ""
		pending_act = -1
		mystery_pending = false
		return
	_start_walk(destination, destination_floor, act_index, mystery, interaction_id)


func _start_walk(destination: Vector2, destination_floor: int,
		act_index: int, mystery: bool, interaction_id: String = "") -> void:
	pending_interaction = interaction_id
	waypoints = navigation.route(foot, floor_index, destination, destination_floor)
	waypoint_index = 0
	target_floor = destination_floor
	pending_act = act_index
	mystery_pending = mystery
	if waypoints.is_empty():
		pending_act = -1
		mystery_pending = false
	guide_pointer.visible = false


func _update_actor() -> void:
	actor.position = foot - Vector2(ACTOR_SIZE.x * 0.5, ACTOR_SIZE.y)
	if foreground != null:
		actor.position += foreground.actor_offset
	floor_glow.position = foot - Vector2(23, 2)


func _process(delta: float) -> void:
	if not is_visible_in_tree() or not accepting_input:
		return
	elapsed += delta
	foreground.tick(delta)
	_update_actor()
	if guide_pointer.visible:
		guide_pointer.position.y = guide_pointer_base.y + sin(elapsed * 4.0) * 7.0
	if waypoints.is_empty():
		return
	var destination := waypoints[waypoint_index]
	var vertical := absf(destination.x - foot.x) < 0.1 and absf(destination.y - foot.y) > 1.0
	foot = foot.move_toward(destination, (LIFT_SPEED if vertical else WALK_SPEED) * delta)
	_update_actor()
	if not foot.is_equal_approx(destination):
		return
	for level in range(4):
		if is_equal_approx(foot.y, OperaVenueNavigation.FLOOR_Y[level]):
			floor_index = level
	if queued_floor >= 0:
		var next_floor := queued_floor
		queued_floor = -1
		waypoints.clear()
		_start_walk(queued_target, next_floor, queued_act, queued_mystery, queued_interaction)
		queued_interaction = ""
		return
	waypoint_index += 1
	if waypoint_index < waypoints.size():
		return
	waypoints.clear()
	floor_index = target_floor
	var interaction_id := pending_interaction
	pending_interaction = ""
	if not interaction_id.is_empty():
		foreground.begin(interaction_id)
	var act_index := pending_act
	pending_act = -1
	if act_index >= 0 and can_enter_act(act_index) and launch_career.is_valid():
		launch_career.call(act_index)
	elif mystery_pending:
		# A gentle acknowledgment, no fake win, save bit, or impossible objective.
		mystery_pending = false
		guide_pointer_base = mystery_door.position + Vector2(55, 12)
		guide_pointer.position = guide_pointer_base
		guide_pointer.visible = true
		m._say("roshan", "castle_opera_enter", 8.0)
