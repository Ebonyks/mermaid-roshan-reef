extends "res://export/flat_vector_r94/capture_fairy.gd"
# R94 nonruntime preview: original current Dev scene/controller, unchanged R93 PNG.
var r94_variant: String = ""
var r94_bound: bool = false
var r94_texture: ImageTexture
var r94_decode: Dictionary = {}
var r94_comparisons: Array[Dictionary] = []
var r94_cycles: Array[Dictionary] = []
const R94_TIP := Vector2(536.5, 1091.0)
const R94_SCALE := 49.0 / 665.0

func _r94_hash(bytes: PackedByteArray) -> String:
	var h := HashingContext.new()
	h.start(HashingContext.HASH_SHA256)
	h.update(bytes)
	return h.finish().hex_encode()

func _r94_sprite(value: Variant, pointer: bool = false) -> Dictionary:
	var s: Sprite2D = value as Sprite2D
	if s == null:
		return {}
	var result: Dictionary = {"id": s.get_instance_id(), "position": _safe(s.position), "rotation": s.rotation, "z": s.z_index, "visible": s.visible, "modulate": _safe(s.modulate), "self_modulate": _safe(s.self_modulate), "centered": s.centered, "flip_h": s.flip_h, "flip_v": s.flip_v, "region_enabled": s.region_enabled, "region_rect": _safe(s.region_rect)}
	if not pointer:
		result["texture"] = _tex(s.texture)
		result["scale"] = _safe(s.scale)
		result["offset"] = _safe(s.offset)
		result["filter"] = s.texture_filter
	return result

func _r94_signature() -> Dictionary:
	var handoff: RefCounted = m.fairy_conservatory_handoff
	if handoff == null:
		return {}
	var world: Node2D = handoff.get("_world") as Node2D
	var backdrop: ColorRect = handoff.get("_backdrop") as ColorRect
	var rows: Array[Dictionary] = []
	for value: Variant in handoff.get("_tiles"):
		rows.append(_r94_sprite(value))
	return {"game": m.game, "controller": handoff.get_instance_id(), "source_state": handoff.call("audit_snapshot"), "world_id": world.get_instance_id(), "world_transform": str(world.transform), "backdrop": {"id": backdrop.get_instance_id(), "z": backdrop.z_index, "visible": backdrop.visible, "color": _safe(backdrop.color)}, "tiles": rows, "walkway": _r94_sprite(handoff.get("_walkway")), "house": _r94_sprite(handoff.get("_house")), "hero": _r94_sprite(handoff.get("_roshan")), "pointer_except_declared_texture_scale_offset_filter": _r94_sprite(handoff.get("_pointer"), true), "house_button": _control_state("ButterflyHouseHotspot"), "navigation": super._snapshot().get("navigation_bindings", [])}

func _r94_apply() -> bool:
	var handoff: RefCounted = m.fairy_conservatory_handoff
	var p: Sprite2D = handoff.get("_pointer") as Sprite2D
	if p == null or p.texture == null or p.texture.get_size() != Vector2(512, 512) or p.scale != Vector2.ONE * 0.12 or not p.centered or p.region_enabled or p.flip_h or p.flip_v:
		return false
	var path: String = OS.get_environment("R94_CANDIDATE")
	if FileAccess.get_sha256(path) != "b10923462ca5947ee360db49b0fa8a33ca2fd660fb1fb85767a638c67853ecec":
		return false
	var image: Image = Image.load_from_file(path)
	if image == null or image.get_size() != Vector2i(1254, 1254):
		return false
	image.convert(Image.FORMAT_RGBA8)
	var base: PackedByteArray = image.get_data()
	if image.generate_mipmaps() != OK:
		return false
	r94_texture = ImageTexture.create_from_image(image)
	var decoded: Image = r94_texture.get_image()
	var gpu_base: PackedByteArray = decoded.get_data().slice(0, base.size())
	r94_decode = {"source_png_sha256": FileAccess.get_sha256(path), "source_base_rgba_sha256": _r94_hash(base), "gpu_base_rgba_sha256": _r94_hash(gpu_base), "base_rgba_exact": base == gpu_base, "native_size": [1254, 1254], "mipmaps_added_to_loaded_copy_only": image.has_mipmaps(), "source_png_modified": false, "pixel_crop_resize_alpha_repaint": false, "export_ready": false}
	if base != gpu_base:
		return false
	p.texture = r94_texture
	p.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	p.scale = Vector2.ONE * R94_SCALE
	var desired_delta := Vector2(-40.0, 0.0) - Vector2(-42.0, -82.0)
	p.offset = desired_delta / p.scale - (R94_TIP - Vector2(627.0, 627.0))
	r94_bound = true
	return true

func _r94_tip() -> Dictionary:
	var h: RefCounted = m.fairy_conservatory_handoff
	if h == null:
		return {}
	var p: Sprite2D = h.get("_pointer") as Sprite2D
	var world: Node2D = h.get("_world") as Node2D
	var snap: Dictionary = h.call("audit_snapshot") as Dictionary
	var source_tip: Vector2 = R94_TIP if r94_bound else Vector2(217, 447)
	var tip: Vector2 = p.get_global_transform_with_canvas() * (p.get_rect().position + source_tip)
	var rect: Rect2
	var target: Vector2
	if str(snap["state"]) == "butterfly_house":
		var b: Button = h.get("_house_button") as Button
		rect = b.get_global_rect()
		target = rect.get_center()
	else:
		var logical: Vector2 = h.call("_next_waypoint") as Vector2
		target = world.get_global_transform_with_canvas() * logical
		var half: Vector2 = FairyConservatoryHandoff2D.MIN_TOUCH * 0.5
		var lo: Vector2 = world.get_global_transform_with_canvas() * (logical - half)
		var hi: Vector2 = world.get_global_transform_with_canvas() * (logical + half)
		rect = Rect2(lo, hi - lo)
	return {"state": snap["state"], "index": snap["waypoint_index"], "phase": float(h.get("_pointer_phase")), "native_tip": _safe(tip), "native_target": _safe(target), "target_rect": [rect.position.x, rect.position.y, rect.size.x, rect.size.y], "inside": rect.has_point(tip), "pointer_position": _safe(p.position), "pointer_scale": _safe(p.scale), "pointer_offset": _safe(p.offset), "filter": p.texture_filter, "texture_size": _safe(p.texture.get_size()), "registered_candidate": r94_bound}

func _r94_cycle() -> bool:
	var first: Dictionary = _r94_tip()
	var rows: Array[Dictionary] = []
	for i: int in range(150):
		var row: Dictionary = _r94_tip()
		if row.is_empty():
			errors.append("original handoff disappeared during natural cue cycle")
			return false
		rows.append(row)
		if (float(row["phase"]) - float(first["phase"])) * 4.0 >= TAU + 0.05:
			break
		await process_frame
	var outside: int = 0
	for row: Dictionary in rows:
		if not bool(row["inside"]):
			outside += 1
	var span: float = (float(rows[-1]["phase"]) - float(first["phase"])) * 4.0
	r94_cycles.append({"state": first["state"], "index": first["index"], "natural_phase_radians": span, "samples": rows, "outside_count": outside, "candidate_bound": r94_bound})
	_check("natural complete bob cycle " + str(first["state"]) + str(first["index"]), span >= TAU)
	_check("passive bob never advances source progress", int(_r94_tip()["index"]) == int(first["index"]))
	if r94_bound:
		_check("candidate fingertip stays in original target for full cycle", outside == 0)
	return errors.is_empty()

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	result["r94_variant"] = r94_variant
	result["r94_candidate_bound"] = r94_bound
	result["r94_tip"] = _r94_tip() if is_instance_valid(m) and m.fairy_conservatory_handoff != null else {}
	result["r94_decode"] = r94_decode
	result["r94_comparisons"] = r94_comparisons
	return result

func _capture(id: String, role: String = "R94_BOUND_NAMED_HAND_PREVIEW_NOT_ACCEPTANCE") -> void:
	if not id.begins_with("r94_"):
		return
	await super(id, "R94_PAINTED_REGISTERED_NATIVE_PREVIEW" if r94_bound else "R94_UNCHANGED_FLAT_SOURCE_CONTROL")

func _r94_hall_settled() -> bool:
	var foot: Vector2 = m.castle_room_player_sprite.get_meta("stage_foot", Vector2.ZERO) as Vector2
	var target: float = clampf(foot.x - CastleRooms25D.HALL_VIEW_SIZE.x * 0.5, 0.0, CastleRooms25D.HALL_LOGICAL_SIZE.x - CastleRooms25D.HALL_VIEW_SIZE.x)
	return absf(float(m._castle_rooms_25d.get("_hall_view_left_art")) - target) <= 0.001

func _exercise() -> void:
	if not await _boot() or not await _castle_entry("pre_castle") or not await _frame_moonflower("pre_moon"):
		return
	if not await _wait(_r94_hall_settled, 20.0):
		errors.append("current source hall camera did not settle")
		return
	if not await _enter_handoff("r94_00_before"):
		return
	var before: Dictionary = _r94_signature()
	if r94_variant == "painted_registered":
		_check("exact unchanged PNG binds only to original hand Sprite2D", _r94_apply())
		if not r94_bound:
			return
	var after: Dictionary = _r94_signature()
	r94_comparisons.append({"before": before, "after": after, "preserved_except_declared_pointer_draw": before == after})
	_check("original state/input/targets/background/hero and other geometry preserved", before == after)
	await _frames(3)
	await _capture("r94_01_bound")
	var h: RefCounted = m.fairy_conservatory_handoff
	for i: int in range(3):
		if not await _r94_cycle():
			return
		var tip: Dictionary = _r94_tip()
		var p: Array = tip["native_tip"] if r94_bound else tip["native_target"]
		await _raw_tap(Vector2(float(p[0]), float(p[1])))
		if not await _wait(func() -> bool: return m.fairy_conservatory_handoff == h and int((h.call("audit_snapshot") as Dictionary)["waypoint_index"]) == i + 1, 5.0):
			errors.append("original waypoint input did not advance " + str(i))
			return
		await _capture("r94_0%d_outbound" % (i + 2))
	_check("original house control appears at earned endpoint", str((h.call("audit_snapshot") as Dictionary)["state"]) == "butterfly_house" and _button("ButterflyHouseHotspot").is_visible_in_tree())
	if not await _r94_cycle():
		return
	await _capture("r94_05_house_cycle")
	_check("original beforeReady private save dependency remains bound", m._save_state.save_path == profile)

func _run() -> void:
	mode = "opened"
	r94_variant = OS.get_environment("R94_VARIANT")
	out_dir = OS.get_environment("R94_OUT")
	normal_base = OS.get_environment("R94_NORMAL_BASE")
	var width: int = int(OS.get_environment("R94_WIDTH"))
	if r94_variant not in ["source", "painted_registered"] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	var engine: Dictionary = Engine.get_version_info()
	if str(engine.get("hash", "")) != "ed1daf0bf001b61586d9930840f2f1394092c079" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() != "Windows" or Engine.time_scale != 1.0:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "day_one_active": false, "opera_done": false, "chapter3_fairy_door_revealed": true, "chapter3_fairy_door_opened": true, "chapter3_fairy_mission_started": false, "custom_fish": [], "custom_friends": [], "companion": "", "flat_vector_private_unknown": {"token": "R94_PRIVATE_ONLY", "keep": [3, 7]}}
	var file: FileAccess = FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	node_added.connect(_bind_private_before_ready)
	source_main = load("res://scenes/main.tscn") as PackedScene
	if await _aspect(Vector2i(width, 720)):
		await _exercise()
	var final_snapshot: Dictionary = _snapshot()
	await _retire()
	_check("owned original Main retired", m == null)
	_check("normal eleven save/archive hashes unchanged", _normal_hashes() == normal_before)
	var report: Dictionary = {"schema": "reef.painted_hand_native_preview/1", "source_revision": OS.get_environment("R94_REV"), "variant": r94_variant, "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "quality": "speedy", "aspect": [width, 720], "time_scale": Engine.time_scale, "states": states, "checks": checks, "events": events, "errors": errors, "bindings": bindings, "normal_before": normal_before, "normal_after": _normal_hashes(), "source_seed": seed, "candidate_decode": r94_decode, "natural_hint_cycles": r94_cycles, "draw_delta_comparisons": r94_comparisons, "final_snapshot": final_snapshot, "generation_calls_this_preview": 0, "actual_child_data": false, "production_changes": [], "status": "PASS" if errors.is_empty() else "FAIL", "scope": "Original currentDevF Main/Continue/Castle/Moonflower/Skyway and three one-finger waypoint actions with natural bob; stop at house endpoint. RawR93PNG unchanged; pointer texture/scale/offset/filter only. Original backdrop/layout/foreground untouched; noR70visual patch, progress/clock/target/controller writes, production adoption, export/device/formalQA11/child/owner/allcaller or return closure."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("HAND94|RESULT|", report["status"], "|CHECKS|", checks.size(), "|", errors)
	quit(0 if errors.is_empty() else 1)
