class_name NavigationController
extends RefCounted

# One explicit navigation stack for the whole game. Mutable route state stays
# on ReefMain; this satellite only owns the routing rules.

var m: ReefMain
var _handoff_pulse: Tween


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
	if m._pause_ref()._navigation_locked():
		return
	if is_instance_valid(m._day_one_story_clip):
		m._day_one_story_clip.skip()
		return
	if m.pause_panel != null and m.pause_panel.visible:
		m._pause_ref().toggle_pause()
		return
	_prune_invalid()
	if (m.game == "dustboss" and m.day_one_is_active()) \
			or (top_id() == "pearl_castle" and (m.day_one_is_active() or m.chapter2_is_active())):
		m._pause_ref().toggle_pause()
		return
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
	var story_playing: bool = is_instance_valid(m._day_one_story_clip)
	_sync_handoff_pulse(button, button.visible and not story_playing
		and (m.pause_panel == null or not m.pause_panel.visible)
		and top_id() == "pearl_castle_room" and m.day_one_is_active()
		and m._day_one_room_handoff_target != ""
		and m._day_one_room_handoff_source == m.castle_room_id)
	if not button.visible:
		return
	var menu_mode: bool = at_sky_lagoon_root() or (m.game == "dustboss" and m.day_one_is_active()) \
		or (top_id() == "pearl_castle" and (m.day_one_is_active() or m.chapter2_is_active()))
	var mode := "skip" if story_playing else ("menu" if menu_mode else "back")
	if String(button.get_meta("global_navigation_mode", "")) == mode:
		return
	button.set_meta("global_navigation_mode", mode)
	match mode:
		"skip": StorybookUI.style_navigation_button(button, "⏭", "Skip")
		"menu": StorybookUI.style_navigation_button(button, "☰", "Menu")
		_: StorybookUI.style_navigation_button(button, "↩", "Back")
	position_button(button)


func _sync_handoff_pulse(button: Button, cue_ready: bool) -> void:
	if cue_ready and (_handoff_pulse == null or not _handoff_pulse.is_valid()):
		button.pivot_offset = button.size * 0.5
		_handoff_pulse = button.create_tween().set_loops()
		_handoff_pulse.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
		_handoff_pulse.tween_property(button, "scale", Vector2.ONE * 1.12, 0.45)
		_handoff_pulse.parallel().tween_property(button, "self_modulate", Color(1.13, 1.04, 0.81), 0.45)
		_handoff_pulse.tween_property(button, "scale", Vector2.ONE, 0.55)
		_handoff_pulse.parallel().tween_property(button, "self_modulate", Color.WHITE, 0.55)
	elif not cue_ready and _handoff_pulse != null:
		_handoff_pulse.kill()
		_handoff_pulse = null
		button.scale = Vector2.ONE
		button.self_modulate = Color.WHITE


func _prune_invalid() -> void:
	for index: int in range(m.navigation_routes.size() - 1, -1, -1):
		var route: Dictionary = m.navigation_routes[index] as Dictionary
		var owner_ref: WeakRef = route.get("owner") as WeakRef
		if owner_ref != null and owner_ref.get_ref() == null:
			m.navigation_routes.remove_at(index)


func position_button(button: Button) -> void:
	button.set_anchors_preset(Control.PRESET_TOP_LEFT)
	button.offset_left = 18.0
	button.offset_right = 130.0
	button.offset_top = 18.0
	button.offset_bottom = 130.0
