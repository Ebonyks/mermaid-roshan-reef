class_name NavigationController
extends RefCounted

# One explicit navigation stack for the whole game. Mutable route state stays
# on ReefMain; this satellite only owns the routing rules.

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
		and top_id() == "" \
		and (m.pause_panel == null or not m.pause_panel.visible)


func press() -> void:
	if m._pause_ref()._navigation_locked():
		return
	if m.pause_panel != null and m.pause_panel.visible:
		m._pause_ref().toggle_pause()
		return
	_prune_invalid()
	if not m.navigation_routes.is_empty():
		var route: Dictionary = m.navigation_routes.pop_back() as Dictionary
		var close_action: Callable = route.get("close", Callable()) as Callable
		if close_action.is_valid():
			close_action.call()
		sync_button()
		return
	if m.navigation_root_id == "sky_lagoon":
		m._pause_ref().toggle_pause()
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
	button.position = Vector2(18.0, 18.0)


func _prune_invalid() -> void:
	for index: int in range(m.navigation_routes.size() - 1, -1, -1):
		var route: Dictionary = m.navigation_routes[index] as Dictionary
		var owner_ref: WeakRef = route.get("owner") as WeakRef
		if owner_ref != null and owner_ref.get_ref() == null:
			m.navigation_routes.remove_at(index)
