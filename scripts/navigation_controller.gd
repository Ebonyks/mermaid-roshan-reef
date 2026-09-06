class_name NavigationController
extends RefCounted

# One explicit navigation stack for the whole game. Mutable route state stays
# on ReefMain; this satellite only owns the routing rules.

const IDLE_CUE_SECONDS: float = 15.0
const PULSE_SECONDS: float = 2.0

var m: ReefMain


func _init(main: ReefMain) -> void:
	m = main


func set_root(route_id: String) -> void:
	m.navigation_root_id = route_id
	if route_id == "":
		m.navigation_routes.clear()
	sync_button()


func push(route_id: String, owner: Object, close_action: Callable) -> void:
	if route_id == "" or not close_action.is_valid():
		return
	remove(route_id, false)
	m.navigation_routes.append({
		"id": route_id,
		"owner": weakref(owner) if owner != null else null,
		"close": close_action,
	})
	sync_button()


func remove(route_id: String, refresh: bool = true) -> void:
	for index: int in range(m.navigation_routes.size() - 1, -1, -1):
		if String((m.navigation_routes[index] as Dictionary).get("id", "")) == route_id:
			m.navigation_routes.remove_at(index)
	if refresh:
		sync_button()


func clear() -> void:
	m.navigation_routes.clear()
	sync_button()


func top_id() -> String:
	_prune_invalid()
	if m.navigation_routes.is_empty():
		return ""
	return String((m.navigation_routes.back() as Dictionary).get("id", ""))


func at_sky_lagoon_root() -> bool:
	return m.navigation_root_id == "sky_lagoon" \
		and m.game == "level2" \
		and String(m.g.get("phase", "")) == "promenade" \
		and top_id() == "" \
		and (m.pause_panel == null or not m.pause_panel.visible)


func press() -> void:
	reset_attention()
	if m.navigation_attention_blocks != 0 or m._pause_ref()._navigation_locked():
		return
	if m.pause_panel != null and m.pause_panel.visible:
		m._pause_ref().toggle_pause()
		return
	if handoff_actionable():
		m._open_day_one_room_route(m._day_one_room_handoff_target)
		sync_button()
		return
	_prune_invalid()
	if not m.navigation_routes.is_empty():
		var route: Dictionary = m.navigation_routes.pop_back() as Dictionary
		var close_action: Callable = route.get("close", Callable()) as Callable
		if close_action.is_valid():
			close_action.call()
		sync_button()
		return
	if at_sky_lagoon_root():
		m._pause_ref().toggle_pause()
	elif m._pause_ref()._has_leave_context():
		# Older activities predate explicit route registration. Back must still be
		# functional game-wide while those controllers migrate onto the stack.
		m._pause_ref()._leave_current_activity()
	sync_button()


func sync_button() -> void:
	var button: Button = m.global_navigation_button
	if button == null or not is_instance_valid(button):
		return
	_prune_invalid()
	button.visible = not m._pause_ref()._navigation_locked()
	button.disabled = not button.visible
	if not button.visible:
		return
	var menu_mode: bool = at_sky_lagoon_root()
	var mode := "menu" if menu_mode else "back"
	if String(button.get_meta("global_navigation_mode", "")) == mode:
		return
	button.set_meta("global_navigation_mode", mode)
	StorybookUI.style_icon_button(button, "☰" if menu_mode else "↩",
		"secondary", Vector2(112.0, 112.0), "Menu" if menu_mode else "Back")
	position_button(button)


func _prune_invalid() -> void:
	for index: int in range(m.navigation_routes.size() - 1, -1, -1):
		var route: Dictionary = m.navigation_routes[index] as Dictionary
		var owner_ref: WeakRef = route.get("owner") as WeakRef
		if owner_ref != null and owner_ref.get_ref() == null:
			m.navigation_routes.remove_at(index)


func position_button(button: Button) -> void:
	button.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	button.offset_left = -130.0
	button.offset_right = -18.0
	button.offset_top = 18.0
	button.offset_bottom = 130.0


func handoff_actionable() -> bool:
	return m.day_one_is_active() and not m._day_one_room_handoff_target.is_empty() \
		and m._day_one_room_handoff_source == m.castle_room_id \
		and m.castle_room_stage != null and is_instance_valid(m.castle_room_stage) \
		and m.castle_room_stage.is_visible_in_tree() \
		and top_id() == "pearl_castle_room" \
		and not m._pause_ref()._navigation_locked() \
		and not m._day_one_bathroom_movie_handoff_pending \
		and not m._day_one_bathroom_movie_is_playing() \
		and m._day_one_draft_movie == null \
		and (m.pause_panel == null or not m.pause_panel.visible) \
		and m.navigation_attention_blocks == 0


func begin_handoff() -> void:
	var button: Button = m.global_navigation_button
	if button.get_node_or_null("DayOneRouteGhostHand") == null:
		var hand := Sprite2D.new()
		hand.name = "DayOneRouteGhostHand"
		hand.texture = load("res://assets/castle/training/ghost_hand.png") as Texture2D
		hand.position = Vector2(-16.0, 56.0)
		hand.rotation = -PI * 0.5
		hand.scale = Vector2.ONE * 0.15
		hand.set_meta("visual_pointer", true)
		button.add_child(hand)
	if button.get_node_or_null("DayOneArrowGlow") == null:
		var glow := Panel.new()
		glow.name = "DayOneArrowGlow"
		glow.position = Vector2(-5.0, -5.0)
		glow.size = Vector2(122.0, 122.0)
		glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
		glow.show_behind_parent = true
		var halo := StyleBoxFlat.new()
		halo.bg_color = StorybookUI.CORAL
		halo.set_corner_radius_all(61)
		halo.shadow_color = StorybookUI.CORAL
		halo.shadow_size = 16
		glow.add_theme_stylebox_override("panel", halo)
		button.add_child(glow)
	reset_attention()
	sync_button()


func end_handoff() -> void:
	reset_attention()
	var button: Button = m.global_navigation_button
	if button == null or not is_instance_valid(button):
		return
	for child_name: String in ["DayOneRouteGhostHand", "DayOneArrowGlow"]:
		var child: Node = button.get_node_or_null(child_name)
		if child != null:
			button.remove_child(child)
			child.queue_free()


func observe_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		if event.pressed:
			m.navigation_held_touches[event.index] = true
		else:
			m.navigation_held_touches.erase(event.index)
	if event is InputEventScreenTouch or event is InputEventScreenDrag \
			or event is InputEventMouseButton or event is InputEventKey \
			or event is InputEventJoypadButton:
		reset_attention()
	elif event is InputEventMouseMotion and event.relative.length_squared() > 0.0:
		reset_attention()
	elif event is InputEventJoypadMotion and absf(event.axis_value) > 0.2:
		reset_attention()


func reset_attention() -> void:
	m.navigation_idle_seconds = 0.0
	var button: Button = m.global_navigation_button
	if button == null or not is_instance_valid(button):
		return
	button.self_modulate = Color.WHITE
	var glow: CanvasItem = button.get_node_or_null("DayOneArrowGlow") as CanvasItem
	if glow != null:
		glow.modulate.a = 0.0


func tick_attention(delta: float) -> void:
	var button: Button = m.global_navigation_button
	if button == null or not is_instance_valid(button):
		return
	var actionable: bool = handoff_actionable() and button.visible and not button.disabled
	var hand: CanvasItem = button.get_node_or_null("DayOneRouteGhostHand") as CanvasItem
	if hand != null:
		hand.visible = actionable
	if not actionable:
		reset_attention()
		return
	if not m.navigation_held_touches.is_empty() or Input.get_mouse_button_mask() != 0:
		reset_attention()
		return
	m.navigation_idle_seconds += maxf(delta, 0.0)
	if m.navigation_idle_seconds < IDLE_CUE_SECONDS:
		return
	# A soft two-second pulse preserves the pearl/violet silhouette and press state.
	var phase: float = (m.navigation_idle_seconds - IDLE_CUE_SECONDS) * TAU / PULSE_SECONDS
	var strength: float = 0.35 + 0.65 * (0.5 - 0.5 * cos(phase))
	button.self_modulate = Color.WHITE.lerp(StorybookUI.CORAL, strength * 0.65)
	var glow: CanvasItem = button.get_node_or_null("DayOneArrowGlow") as CanvasItem
	if glow != null:
		glow.modulate.a = strength
