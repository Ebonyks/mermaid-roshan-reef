extends "res://export/flat_vector_r72/capture_fairy.gd"
const ReuseCandidate = preload("res://export/flat_vector_r72/skyway_reuse.gd")
var reuse_candidate: RefCounted
var comparisons: Array[Dictionary] = []

func _sprite_data(value: Variant, include_position: bool = true) -> Dictionary:
	var sprite: Sprite2D = value as Sprite2D
	if sprite == null:
		return {}
	var result: Dictionary = {"id": sprite.get_instance_id(), "texture": _tex(sprite.texture), "scale": _safe(sprite.scale), "z_index": sprite.z_index, "visible": sprite.visible, "modulate": _safe(sprite.modulate), "self_modulate": _safe(sprite.self_modulate)}
	if include_position:
		result["position"] = _safe(sprite.position)
	return result

func _preserved_signature() -> Dictionary:
	var handoff: RefCounted = m.fairy_conservatory_handoff
	if handoff == null:
		return {}
	var world: Node2D = handoff.get("_world") as Node2D
	var layer: CanvasLayer = handoff.get("_layer") as CanvasLayer
	var root_control: Control = handoff.get("_root") as Control
	return {"game": m.game, "controller": handoff.get_instance_id(), "source_script": (handoff.get_script() as Script).resource_path, "source_state": handoff.call("audit_snapshot"), "world_id": world.get_instance_id(), "world_position": _safe(world.position), "world_scale": _safe(world.scale), "layer_id": layer.get_instance_id(), "root_id": root_control.get_instance_id(), "root_size": _safe(root_control.size), "walkway": _sprite_data(handoff.get("_walkway")), "house": _sprite_data(handoff.get("_house")), "roshan": _sprite_data(handoff.get("_roshan")), "pointer": _sprite_data(handoff.get("_pointer")), "house_control": _control_state("ButterflyHouseHotspot"), "navigation": super._snapshot().get("navigation_bindings", [])}

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	result["visual_variant"] = OS.get_environment("R72_VISUAL")
	result["candidate_comparisons"] = comparisons.duplicate(true)
	result["reuse_candidate"] = reuse_candidate.call("audit_snapshot") if reuse_candidate != null else {}
	if is_instance_valid(m) and m.fairy_conservatory_handoff != null:
		var handoff: RefCounted = m.fairy_conservatory_handoff
		var world: Node2D = handoff.get("_world") as Node2D
		var backdrop: ColorRect = handoff.get("_backdrop") as ColorRect
		var tile_rows: Array[Dictionary] = []
		for value: Variant in handoff.get("_tiles"):
			tile_rows.append(_sprite_data(value))
		result["candidate_visual_nodes"] = {"backdrop_id": backdrop.get_instance_id(), "backdrop_z": backdrop.z_index, "backdrop_visible": backdrop.visible, "backdrop_color": _safe(backdrop.color), "tiles": tile_rows, "world_position": _safe(world.position), "world_scale": _safe(world.scale), "foreground_signature": _preserved_signature()}
	return result

func _enter_handoff(prefix: String) -> bool:
	if not await super(prefix):
		return false
	var before: Dictionary = _preserved_signature()
	var prior_candidate: RefCounted = reuse_candidate
	if prior_candidate != null:
		_check("prior source root disposed before fresh entry " + prefix, not bool((prior_candidate.call("audit_snapshot") as Dictionary)["root_alive"]))
	reuse_candidate = ReuseCandidate.new()
	var attached: bool = bool(reuse_candidate.call("attach", m.fairy_conservatory_handoff, OS.get_environment("R72_VISUAL")))
	_check("candidate attaches only to original loaded source nodes " + prefix, attached)
	if not attached:
		return false
	var after: Dictionary = _preserved_signature()
	comparisons.append({"entry": prefix, "before": before, "after": after, "equal": before == after, "declared_delta": "Existing backdropz -30; optional background tile positions/uniform scale and one resize observer. Source foreground/world/control/state/navigation unchanged."})
	_check("candidate preserves exact source state/input/foreground signature " + prefix, before == after)
	await _frames(3)
	await _capture(prefix + "_reuse_visible")
	return true

func _hall_camera_settled() -> bool:
	if m._castle_rooms_25d == null or m.castle_room_player_sprite == null:
		return false
	var foot: Vector2 = m.castle_room_player_sprite.get_meta("stage_foot", Vector2.ZERO) as Vector2
	var target: float = clampf(foot.x - CastleRooms25D.HALL_VIEW_SIZE.x * 0.5, 0.0, CastleRooms25D.HALL_LOGICAL_SIZE.x - CastleRooms25D.HALL_VIEW_SIZE.x)
	return absf(float(m._castle_rooms_25d.get("_hall_view_left_art")) - target) <= 0.001

func _exercise() -> void:
	if not await _boot():
		return
	await _capture("01_original_menu")
	if not await _castle_entry("02") or not await _frame_moonflower("03"):
		return
	if not await _wait(_hall_camera_settled, 20.0):
		errors.append("source hall camera did not naturally converge")
		return
	await _capture("03_hall_camera_settled")
	var hall_id: int = m.castle_room_layer.get_instance_id()
	var hall_view: float = float(m._castle_rooms_25d.get("_hall_view_left_art"))
	if not await _enter_handoff("04"):
		return
	await _tap(_button("GlobalNavigationButton"), _button("GlobalNavigationButton").size * 0.5)
	if not await _wait(func() -> bool: return m.game == "level2" and str(m.g.get("phase", "")) == "hall" and m.fairy_conservatory_handoff == null, 25.0):
		errors.append("original direct Skyway Back failed")
		return
	await _frames(30)
	_check("original direct Skyway Back resumes same cached hall", is_instance_valid(m.castle_room_layer) and m.castle_room_layer.get_instance_id() == hall_id and is_equal_approx(float(m._castle_rooms_25d.get("_hall_view_left_art")), hall_view))
	_check("original source teardown disposes candidate-bound root", not bool((reuse_candidate.call("audit_snapshot") as Dictionary)["root_alive"]))
	await _capture("05_direct_back_hall")
	if not await _enter_handoff("06_reentry"):
		return
	await _journey("07")
