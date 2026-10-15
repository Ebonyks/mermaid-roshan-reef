extends "res://export/flat_vector_r67/capture_entry.gd"
const Candidate = preload("res://export/flat_vector_r67/painted_gate.gd")
var gate_weak: WeakRef

func _bind_private_before_ready(node: Node) -> void:
	super(node)
	if node is ReefMain and mode == "candidate":
		var main: ReefMain = node as ReefMain
		main._sky_lagoon_promenade = Candidate.new(main) as SkyLagoonPromenade

func _gate() -> Dictionary:
	if not is_instance_valid(m):
		return {}
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		var target: Dictionary = value as Dictionary
		if str(target.get("id", "")) != "castle_gate":
			continue
		var node: Node2D = target.get("node") as Node2D
		var glow: Sprite2D = target.get("highlight") as Sprite2D
		if node == null or glow == null:
			return {}
		return {"id": target["id"], "kind": target["kind"], "payload": target["payload"], "radius_px": target["radius_px"], "anchor_id": node.get_instance_id(), "anchor_class": node.get_class(), "anchor_position": str(node.position), "anchor_source_owned": node.get_meta("source_owned", false), "point": str(m._sky_lagoon_promenade.screen_from_master(node.position)), "glow_id": glow.get_instance_id(), "glow_path": str(glow.get_path()), "texture": glow.texture.resource_path if glow.texture != null else "", "scale": str(glow.scale), "modulate": str(glow.modulate), "rgb": [glow.modulate.r, glow.modulate.g, glow.modulate.b], "alpha": glow.modulate.a, "z_index": glow.z_index, "visible": glow.is_visible_in_tree(), "target_count": (m.g.get("lagoon_promenade_targets", []) as Array).size(), "source_helper_script": m._sky_lagoon_promenade.get_script().resource_path}
	return {}

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	result["gate"] = _gate()
	result["candidate_mode"] = mode
	return result

func _capture(id: String, role := "R67_SOURCE_BOUND_REUSE_TRIAL_NOT_QA11") -> void:
	await super(id, role)

func _gate_touch() -> void:
	var anchor: Node2D = m.g.get("lagoon_castle_door_focus") as Node2D
	if anchor == null:
		errors.append("original door anchor missing")
		return
	var point: Vector2 = m._sky_lagoon_promenade.screen_from_master(anchor.position)
	_check("original target point lies inside native viewport", Rect2(Vector2.ZERO, Vector2(root.size)).has_point(point))
	_screen_touch(point, true)
	await _frames(1)
	_screen_touch(point, false)
	await _frames(4)

func _exercise() -> void:
	if not await _boot():
		return
	var continue_button: Button = _button("StartMenuContinueButton") as Button
	_check("original Continue available for private active profile", continue_button != null and not continue_button.disabled)
	await _tap(continue_button, continue_button.size * 0.5)
	if not await _wait(func() -> bool: return not m.start_menu_active and m._day_one_story_clip == null and str(m.g.get("phase", "")) == "promenade", 70.0):
		errors.append("original Continue/unskipped opening did not reach promenade")
		return
	await _frames(60)
	await _capture("01_focused")
	var target: Dictionary = _gate()
	_check("original automatic focus selects castle", str(m.g.get("lagoon_promenade_focus", "")) == "castle_gate")
	_check("invisible source door anchor/radius retained", target.get("anchor_class") == "Node2D" and bool(target.get("anchor_source_owned", false)) and float(target.get("radius_px", 0)) == 128.0)
	var glow: Sprite2D = m.get_node_or_null(str(target.get("glow_path", ""))) as Sprite2D
	gate_weak = weakref(glow)
	_check("trial texture bound", str(target.get("texture", "")) == (Candidate.PAINTED_CUE if mode == "candidate" else "res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png"))
	if mode == "candidate":
		_check("candidate retains authored RGB", target.get("rgb") == [1.0, 1.0, 1.0])
	await _tap(_button("GlobalNavigationButton"), _button("GlobalNavigationButton").size * 0.5)
	await _capture("02_original_pause")
	_check("original pause clears focus", paused and str(m.g.get("lagoon_promenade_focus", "")) == "")
	await _tap(_button("PauseResumeButton"), _button("PauseResumeButton").size * 0.5)
	await _capture("03_idle_after_resume")
	_check("resume retains cleared focus", not paused and str(m.g.get("lagoon_promenade_focus", "")) == "")
	if not await _wait(func() -> bool: return m.msg_timer <= 0.0, 18.0):
		errors.append("original caption did not naturally finish")
		return
	await _gate_touch()
	await _capture("04_reselected")
	_check("original first target touch focuses gate", str(m.g.get("lagoon_promenade_focus", "")) == "castle_gate")
	await _gate_touch()
	if not await _wait(func() -> bool: return str(m.g.get("phase", "")) == "hall" and m._day_one_story_clip == null, 70.0):
		errors.append("original second target touch did not reach castle hall")
		return
	await _frames(30)
	await _capture("05_castle_after_activation")
	_check("source activation enters main hall", m.castle_room_id == "main_hall" and str(m.g.get("phase", "")) == "hall")
	_check("original teardown frees cue and removes targets", gate_weak.get_ref() == null and not m.g.has("lagoon_promenade_targets"))

func _run() -> void:
	mode = OS.get_environment("R67_MODE")
	out_dir = OS.get_environment("R67_OUT")
	normal_base = OS.get_environment("R67_NORMAL_BASE")
	var width: int = int(OS.get_environment("R67_WIDTH"))
	if mode not in ["control", "candidate"] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
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
	seed = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "day_one_active": true, "day_one_arrival_plane_media_seen": false, "day_one_dirty_castle_discovered": false, "flat_vector_private_unknown": {"token": "R67_PRIVATE_ONLY", "keep": [3, 7]}}
	var file: FileAccess = FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	node_added.connect(_bind_private_before_ready)
	source_main = load("res://scenes/main.tscn") as PackedScene
	if await _aspect(Vector2i(width, 720)):
		await _exercise()
	var final_snapshot: Dictionary = _snapshot()
	await _retire()
	_check("retirement removes owned Main", m == null)
	if _normal_hashes() != normal_before:
		errors.append("normal save/archive hashes changed")
	var report: Dictionary = {"schema": "reef.painted_gate_reuse/1", "mode": mode, "source_revision": OS.get_environment("R67_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "aspect": [width, 720], "states": states, "events": events, "checks": checks, "errors": errors, "bindings": bindings, "seed": seed, "normal_before": normal_before, "normal_after": _normal_hashes(), "final_snapshot": final_snapshot, "actual_child_data": false, "production_changes": [], "scope": "Bounded nonproduction reuse candidate, original configured Main route and source touch/pause/activation/teardown owners; no force2D/bootstrap/camera/clock changes. Private synthetic save. Dummy audio. Not freshOS, QA11, device, child, owner, all caller/fallback or creative acceptance."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("GATE67|RESULT|", "PASS" if errors.is_empty() else "FAIL", "|", errors)
	quit(0 if errors.is_empty() else 1)
