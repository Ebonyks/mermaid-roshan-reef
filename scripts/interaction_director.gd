class_name InteractionDirector
extends RefCounted
# Shared touch interaction language:
# ambient -> discoverable glow -> focused acknowledgement -> approach -> ready
# -> automatic activation on arrival. Proximity advertises; a deliberate point
# selects the destination and replaces the old stick-plus-confirm sequence.

const SCREEN_HIT_RADIUS := 104.0
const DISCOVERY_DEFAULT := 30.0
const REFRESH_INTERVAL := 0.45

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main
	_build_visuals()

func tick(delta: float, player_pos: Vector3) -> void:
	m.touch_registry_t -= delta
	if m.touch_registry_t <= 0.0:
		m.touch_registry_t = REFRESH_INTERVAL
		m._populate_touch_interactables()
	_validate_focus()
	var discoverable: Dictionary = _nearest_discoverable(player_pos)
	_place_ring(m.touch_discovery_ring, discoverable, false, delta)
	var focused: Dictionary = _find(m.touch_focus_id)
	_place_ring(m.touch_focus_ring, focused, true, delta)
	if not focused.is_empty():
		var distance: float = _distance_to(player_pos, _position(focused))
		var activation_radius: float = float(focused.get("activation_radius", 5.0))
		m.touch_focus_ready = distance <= activation_radius

func on_world_touch(screen_pos: Vector2) -> void:
	if not m.touch_uses_explicit_interactions() or m.player == null:
		return
	var picked: Dictionary = _pick(screen_pos)
	if picked.is_empty():
		clear_focus()
		if m._tap_move_ref().start_from_screen(screen_pos):
			m.show_msg("Roshan", "Swimming there!", "hint")
		return
	var picked_id: String = String(picked["id"])
	# An action edge belongs to the focus that existed when it was pressed.
	# Choosing a different target must never inherit a pre-focus button press,
	# even when both inputs land in the same rendered frame.
	if picked_id != m.touch_focus_id and m.touch_ui != null:
		m.touch_ui.clear_action_edge()
	m.touch_focus_id = picked_id
	m.touch_focus_ready = _distance_to(m.player.position, _position(picked)) <= float(picked.get("activation_radius", 5.0))
	m._sparkle_burst(_position(picked) + Vector3(0.0, 1.0, 0.0), Color(1.0, 0.92, 0.48))
	if m.touch_focus_ready:
		_activate(picked)
		return
	m._tap_move_ref().start(
		_position(picked),
		picked_id,
		float(picked.get("activation_radius", 5.0)))
	m.show_msg(String(picked.get("label", "Roshan")), "Coming closer!", "hint")

func mark_ready(interactable_id: String) -> void:
	if interactable_id != m.touch_focus_id:
		return
	var focused: Dictionary = _find(interactable_id)
	if focused.is_empty():
		return
	# Arrival and readiness share one metric, but the target may have drifted
	# while she swam. Never activate until the shared readiness metric agrees.
	if m.player != null and _distance_to(m.player.position, _position(focused)) > float(focused.get("activation_radius", 5.0)):
		m.show_msg(String(focused.get("label", "Roshan")), "Almost there!", "hint")
		return
	m.touch_focus_ready = true
	_activate(focused)

func clear_focus() -> void:
	m.touch_focus_id = ""
	m.touch_focus_ready = false
	if m.touch_focus_ring != null:
		m.touch_focus_ring.visible = false

func _activate(item: Dictionary) -> void:
	var item_id: String = String(item.get("id", ""))
	if item_id.is_empty():
		return
	m._tap_move_ref().cancel("activated")
	clear_focus()
	m._activate_touch_interactable(item_id, item.get("payload", null))

func _pick(screen_pos: Vector2) -> Dictionary:
	var camera: Camera3D = m.get_viewport().get_camera_3d()
	if camera == null:
		return {}
	var best: Dictionary = {}
	var best_score := INF
	for item_value: Variant in m.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if not bool(item.get("enabled", true)):
			continue
		var position: Vector3 = _position(item)
		if camera.is_position_behind(position):
			continue
		var projected: Vector2 = camera.unproject_position(position)
		var screen_distance: float = projected.distance_to(screen_pos)
		var radius: float = float(item.get("screen_radius", SCREEN_HIT_RADIUS))
		if screen_distance > radius:
			continue
		var depth: float = camera.global_position.distance_to(position)
		var score: float = screen_distance + depth * 0.015
		if score < best_score:
			best_score = score
			best = item
	return best

func _nearest_discoverable(player_pos: Vector3) -> Dictionary:
	var best: Dictionary = {}
	var best_distance := INF
	for item_value: Variant in m.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if not bool(item.get("enabled", true)):
			continue
		var distance: float = _distance_to(player_pos, _position(item))
		if distance > float(item.get("discover_radius", DISCOVERY_DEFAULT)):
			continue
		if distance < best_distance:
			best_distance = distance
			best = item
	return best

func _find(interactable_id: String) -> Dictionary:
	if interactable_id.is_empty():
		return {}
	for item_value: Variant in m.touch_interactables:
		var item: Dictionary = item_value as Dictionary
		if String(item.get("id", "")) == interactable_id and bool(item.get("enabled", true)):
			return item
	return {}

func _validate_focus() -> void:
	if m.touch_focus_id.is_empty():
		return
	if _find(m.touch_focus_id).is_empty():
		clear_focus()
		m._tap_move_ref().cancel("focus invalid")

func _position(item: Dictionary) -> Vector3:
	var node_value: Variant = item.get("node")
	if node_value != null and is_instance_valid(node_value):
		var node: Node3D = node_value as Node3D
		return node.global_position
	return item.get("pos", Vector3.ZERO) as Vector3

func _distance_to(a: Vector3, b: Vector3) -> float:
	# Shared with TapMoveDirector: arrival must satisfy this exact metric.
	var horizontal: float = Vector2(a.x - b.x, a.z - b.z).length()
	var vertical: float = absf(a.y - b.y) * TapMoveDirector.VERTICAL_WEIGHT
	return horizontal + vertical

func _build_visuals() -> void:
	m.touch_discovery_ring = _ring(Color(0.48, 1.0, 0.88, 0.50), 3.8)
	m.touch_discovery_ring.name = "TouchDiscoveryRing"
	m.add_child(m.touch_discovery_ring)
	m.touch_focus_ring = _ring(Color(1.0, 0.88, 0.36, 0.88), 4.8)
	m.touch_focus_ring.name = "TouchFocusRing"
	m.add_child(m.touch_focus_ring)

func _ring(color: Color, radius: float) -> MeshInstance3D:
	var ring := MeshInstance3D.new()
	var torus := TorusMesh.new()
	torus.inner_radius = radius - 0.45
	torus.outer_radius = radius
	torus.rings = 20
	torus.ring_segments = 10
	ring.mesh = torus
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.albedo_color = color
	material.emission_enabled = true
	material.emission = Color(color.r, color.g, color.b)
	material.emission_energy_multiplier = 0.75
	material.cull_mode = BaseMaterial3D.CULL_DISABLED
	ring.material_override = material
	ring.visible = false
	return ring

func _place_ring(ring: MeshInstance3D, item: Dictionary, focused: bool, delta: float) -> void:
	if ring == null:
		return
	if item.is_empty() or not m.touch_uses_explicit_interactions():
		ring.visible = false
		return
	var position: Vector3 = _position(item)
	ring.position = position + Vector3(0.0, float(item.get("ring_height", 0.35)), 0.0)
	ring.rotation.y += delta * (1.8 if focused else 0.8)
	var time_now: float = Time.get_ticks_msec() / 1000.0
	var pulse: float = 1.0 + sin(time_now * (4.0 if focused else 2.2)) * (0.10 if focused else 0.05)
	ring.scale = Vector3.ONE * pulse
	ring.visible = true
