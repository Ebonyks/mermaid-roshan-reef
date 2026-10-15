extends "res://export/flat_vector_r68/capture_entry.gd"
const Candidate = preload("res://export/flat_vector_r68/painted_gate.gd")
const Missing = preload("res://export/flat_vector_r68/missing_gate.gd")
const Baseline = preload("res://export/flat_vector_r68/baseline_gate.gd")
var art_failures: Array[String] = []
var first_cue: WeakRef
var returned_cue: WeakRef

func _bind_private_before_ready(node: Node) -> void:
	super(node)
	if node is ReefMain:
		var main: ReefMain = node as ReefMain
		if mode == "baseline_missing":
			main._sky_lagoon_promenade = Baseline.new(main) as SkyLagoonPromenade
		elif mode == "missing":
			main._sky_lagoon_promenade = Missing.new(main) as SkyLagoonPromenade
		else:
			main._sky_lagoon_promenade = Candidate.new(main) as SkyLagoonPromenade

func _gate() -> Dictionary:
	if not is_instance_valid(m):
		return {}
	var target: Dictionary = {}
	for value: Variant in m.g.get("lagoon_promenade_targets", []) as Array:
		if str((value as Dictionary).get("id", "")) == "castle_gate":
			target = value as Dictionary
			break
	var node: Node2D = m.g.get("lagoon_castle_door_focus") as Node2D
	if node == null or not is_instance_valid(node):
		return {}
	var glow: Sprite2D = target.get("highlight") as Sprite2D
	return {"target_registered": not target.is_empty(), "id": target.get("id", ""), "kind": target.get("kind", ""), "payload": target.get("payload", ""), "radius_px": target.get("radius_px", 0), "anchor_id": node.get_instance_id(), "anchor_class": node.get_class(), "anchor_position": str(node.position), "anchor_source_owned": node.get_meta("source_owned", false), "point": str(m._sky_lagoon_promenade.screen_from_master(node.position)), "glow_present": glow != null and is_instance_valid(glow), "glow_id": glow.get_instance_id() if glow != null else 0, "glow_path": str(glow.get_path()) if glow != null else "", "texture": glow.texture.resource_path if glow != null and glow.texture != null else "", "rgb": [glow.modulate.r, glow.modulate.g, glow.modulate.b] if glow != null else [], "alpha": glow.modulate.a if glow != null else 0, "scale": str(glow.scale) if glow != null else "", "art_status": node.get_meta("gate_cue_art_status", "UNSET_REGISTRATION_MISSING"), "expected_texture": node.get_meta("gate_cue_expected_texture", ""), "target_count": (m.g.get("lagoon_promenade_targets", []) as Array).size(), "source_helper_script": m._sky_lagoon_promenade.get_script().resource_path}

func _snapshot() -> Dictionary:
	var result: Dictionary = super()
	result["gate"] = _gate()
	result["candidate_mode"] = mode
	result["source_motion"] = {"walk_goal": str(m.g.get("lagoon_walk_goal_master")), "master_x": m.g.get("lagoon_master_x", "absent"), "master_y": m.g.get("lagoon_master_y", "absent"), "castle_armed": m.g.get("lagoon_castle_armed", "absent")}
	return result

func _capture(id: String, role := "R68_GATE_FUNCTIONAL_TRIAL_NOT_QA11") -> void:
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
	_check("functional castle target registered independently of artwork", bool(target.get("target_registered", false)) and float(target.get("radius_px", 0)) == 128.0 and int(target.get("target_count", 0)) == 4)
	_check("source invisible anchor retained", target.get("anchor_class") == "Node2D" and bool(target.get("anchor_source_owned", false)))
	if mode == "normal":
		_check("painted cue retains its source pixels and RGB", str(target.get("texture", "")) == Candidate.PAINTED_CUE and target.get("rgb") == [1.0, 1.0, 1.0])
		first_cue = weakref(m.get_node(str(target["glow_path"])))
	else:
		art_failures.append("castle_gate expected painted cue unavailable; artwork acceptance blocked")
		_check("missing cue creates no substitute artwork", not bool(target.get("glow_present", false)) and str(target.get("texture", "")).is_empty())
	await _frames(30)
	_check("one-second passive observation does not enter castle", str(m.g.get("phase", "")) == "promenade")
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
	var reached: bool = await _wait(func() -> bool: return str(m.g.get("phase", "")) == "hall" and m._day_one_story_clip == null, 70.0)
	await _frames(30)
	await _capture("05_castle_after_activation" if reached else "05_failed_activation")
	_check("source castle route finishes original clip and reaches main hall", reached and m.castle_room_id == "main_hall")
	if not reached:
		return
	if mode == "baseline_missing":
		_check("source walking entry survives missing direct target", not bool(target.get("target_registered", false)))
		return
	_check("source teardown removes old target and cue", not m.g.has("lagoon_promenade_targets") and (first_cue == null or first_cue.get_ref() == null))
	var old_anchor: int = int(target["anchor_id"])
	await _tap(_button("GlobalNavigationButton"), _button("GlobalNavigationButton").size * 0.5)
	_check("original hall navigation opens pause", paused)
	var leave: Button = _button("PauseLeaveButton") as Button
	_check("original neutral exit is available", leave != null and leave.is_visible_in_tree() and not leave.disabled)
	await _tap(leave, leave.size * 0.5)
	var returned: bool = await _wait(func() -> bool: return str(m.g.get("phase", "")) == "promenade" and not paused and m._day_one_story_clip == null, 25.0)
	await _frames(30)
	await _capture("06_returned_courtyard")
	target = _gate()
	_check("original exit rebuilds a new functional target", returned and bool(target.get("target_registered", false)) and int(target.get("anchor_id", old_anchor)) != old_anchor and float(target.get("radius_px", 0)) == 128.0 and int(target.get("target_count", 0)) == 4)
	if not returned:
		return
	if mode == "normal":
		returned_cue = weakref(m.get_node(str(target["glow_path"])))
		_check("return rebuilds the painted cue", str(target.get("texture", "")) == Candidate.PAINTED_CUE and bool(target.get("glow_present", false)))
	else:
		_check("return preserves missing-art failure without drawing a fallback", not bool(target.get("glow_present", false)) and str(target.get("art_status", "")) == "MISSING_CUE_ARTWORK_FAILED")
	if not await _wait(func() -> bool: return m.msg_timer <= 0.0, 18.0):
		errors.append("original return caption did not naturally finish")
		return
	if str(m.g.get("lagoon_promenade_focus", "")) != "castle_gate":
		await _gate_touch()
	await _capture("07_return_gate_focused")
	_check("returned gate can be focused", str(m.g.get("lagoon_promenade_focus", "")) == "castle_gate")
	await _gate_touch()
	var reentered: bool = await _wait(func() -> bool: return str(m.g.get("phase", "")) == "hall" and m._day_one_story_clip == null, 35.0)
	await _frames(30)
	await _capture("08_reentered_castle")
	_check("original return target permits re-entry", reentered and m.castle_room_id == "main_hall")
	_check("second source teardown removes rebuilt cue and target", not m.g.has("lagoon_promenade_targets") and (returned_cue == null or returned_cue.get_ref() == null))

func _run() -> void:
	mode = OS.get_environment("R68_MODE")
	out_dir = OS.get_environment("R68_OUT")
	normal_base = OS.get_environment("R68_NORMAL_BASE")
	var width: int = int(OS.get_environment("R68_WIDTH"))
	if mode not in ["normal", "missing", "baseline_missing"] or out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
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
	seed = {"schema_version": 1, "save_generation": 7, "won": {}, "found": {}, "pearls": 23, "plays": 3, "skin": "classic", "quality": "speedy", "music": false, "mic": false, "day_one_active": true, "day_one_arrival_plane_media_seen": false, "day_one_dirty_castle_discovered": false, "flat_vector_private_unknown": {"token": "R68_PRIVATE_ONLY", "keep": [3, 7]}}
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
	var report: Dictionary = {"schema": "reef.gate_missing_art/1", "mode": mode, "source_revision": OS.get_environment("R68_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "aspect": [width, 720], "states": states, "events": events, "checks": checks, "errors": errors, "art_failures": art_failures, "functional_status": "PASS" if errors.is_empty() else "FAIL", "artwork_status": "CANDIDATE_UNREVIEWED" if art_failures.is_empty() else "FAIL_MISSING_CUE_ARTWORK", "bindings": bindings, "seed": seed, "normal_before": normal_before, "normal_after": _normal_hashes(), "final_snapshot": final_snapshot, "actual_child_data": false, "production_changes": [], "scope": "Bounded candidate repair and declared null-texture provider, not asset removal. Original source route/input/pause/activation/neutral exit/rebuild/re-entry/teardown owners. Private synthetic data. Baseline raw failures retained/excluded. Functional PASS with missing artwork never accepts art, QA11, freshOS, device, child, owner or whole-game completion."}
	var output: FileAccess = FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("GATE68|RESULT|", report["functional_status"], "|ART|", report["artwork_status"], "|", errors)
	quit(0 if errors.is_empty() else 1)
