extends SceneTree
## R75 original-control or declared named visual-only registration preview. Original source input/state/clocks.
var m: ReefMain
var venue: OperaHouseVenue2D
var book: OperaTreeBookTest
var out_dir := ""
var profile := ""
var states: Array[Dictionary] = []
var events: Array[Dictionary] = []
var checks: Array[Dictionary] = []
var errors: Array[String] = []
var cycles: Array[Dictionary] = []
var source_contracts: Array[Dictionary] = []
var seed: Dictionary = {}
var normal_before: Dictionary = {}
var boot_count := 0
const RegistrationPreview := preload("res://export/flat_vector_r75/registration_preview.gd")
var pointer_preview: Node2D
var mode := ""
var comparisons: Array[Dictionary] = []
var teardown_checks: Array[Dictionary] = []

func _init() -> void:
	call_deferred("_run")

func _normal_hashes() -> Dictionary:
	var row: Dictionary = {}
	var base := ProjectSettings.globalize_path("user://reef_save.json")
	for suffix: String in ["", ".bak", ".tmp", ".tmp0", ".tmp1", ".old", ".bak.tmp", ".bak.old", ".before_new_game", ".before_new_game.tmp", ".before_new_game.old"]:
		var f := base + suffix
		row[suffix] = FileAccess.get_sha256(f) if FileAccess.file_exists(f) else "absent"
	return row

func _frames(count: int) -> void:
	for i: int in range(count):
		await process_frame

func _wait(predicate: Callable, seconds: float = 14.0) -> bool:
	var deadline := Time.get_ticks_msec() + int(seconds * 1000.0)
	while Time.get_ticks_msec() < deadline:
		if bool(predicate.call()):
			return true
		await process_frame
	return bool(predicate.call())

func _check(label: String, passed: bool) -> bool:
	checks.append({"label": label, "pass": passed})
	if not passed:
		errors.append(label)
	return passed

func _aspect(width: int) -> bool:
	root.mode = Window.MODE_WINDOWED
	for i: int in range(180):
		DisplayServer.window_set_position(Vector2i(-2400, 0))
		root.size = Vector2i(width, 720)
		DisplayServer.window_set_size(Vector2i(width, 720))
		await process_frame
		var image: Image = root.get_texture().get_image()
		if image != null and image.get_size() == Vector2i(width, 720):
			return true
	return false

func _tex(texture: Texture2D) -> Dictionary:
	if texture == null:
		return {}
	var row := {"path": texture.resource_path, "class": texture.get_class(), "size": [texture.get_width(), texture.get_height()]}
	if texture is AtlasTexture:
		var a := texture as AtlasTexture
		row["atlas"] = _tex(a.atlas)
		row["region"] = [a.region.position.x, a.region.position.y, a.region.size.x, a.region.size.y]
		row["margin"] = [a.margin.position.x, a.margin.position.y, a.margin.size.x, a.margin.size.y]
	return row

func _disk() -> Dictionary:
	if profile.is_empty() or not FileAccess.file_exists(profile):
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(profile))
	if not parsed is Dictionary:
		return {}
	return {"book": parsed.get(OperaTreeBookTest.SAVE_KEY, {}), "unknown": parsed.get("flat_vector_private_unknown"), "save_generation": parsed.get("save_generation"), "stars": parsed.get("opera_stars"), "pearls": parsed.get("pearls")}

func _native_rect(rect: Rect2) -> Array:
	var transform: Transform2D = book.get_global_transform_with_canvas()
	var a := transform * rect.position
	var b := transform * rect.end
	return [a.x, a.y, b.x - a.x, b.y - a.y]

func _tip_state() -> Dictionary:
	if mode == "registered" and is_instance_valid(pointer_preview):
		return pointer_preview.call("tip_state") as Dictionary
	if not is_instance_valid(book) or book.hand == null:
		return {}
	var target: Rect2
	var draw_box: Rect2
	if book.stage < 3:
		target = book.choice_rect(book.answer_slot())
		draw_box = Rect2(target.end - Vector2(68, 55 + sin(book.elapsed * 3.0) * 9.0), Vector2(80, 80))
	elif book.stage == 4:
		target = OperaTreeBookTest.LEAF_RECT
		draw_box = Rect2(target.position + Vector2(80, 78 + sin(book.elapsed * 3.0) * 10.0), Vector2(95, 95))
	else:
		return {}
	var source_size := book.hand.get_size()
	var scale_factor := minf(draw_box.size.x / source_size.x, draw_box.size.y / source_size.y)
	var actual_size := source_size * scale_factor
	var actual_origin := draw_box.get_center() - actual_size * 0.5
	var local_tip := actual_origin + Vector2(217, 447) * scale_factor
	var native_tip := book.get_global_transform_with_canvas() * local_tip
	return {"stage": book.stage, "help": book.help_level, "elapsed": book.elapsed, "bob_phase_radians": book.elapsed * 3.0, "texture": _tex(book.hand), "source_alpha64_tip": [217, 447], "draw_box": [draw_box.position.x, draw_box.position.y, draw_box.size.x, draw_box.size.y], "local_tip": [local_tip.x, local_tip.y], "native_tip": [native_tip.x, native_tip.y], "target": [target.position.x, target.position.y, target.size.x, target.size.y], "native_target": _native_rect(target), "inside": target.has_point(local_tip), "pointer_visible_by_source_branch": book.help_level == 2 if book.stage < 3 else book.help_level > 0}

func _source_signature() -> Dictionary:
	var d: Dictionary = {}
	for key: String in ["stage", "help_level", "idle_seconds", "elapsed", "treatment", "approach", "suspended", "closing", "pressed_choice", "pointer_id", "pointer_position", "wrong_slot", "wrong_time"]:
		d[key] = book.get(key)
	d["script"] = book.get_script().resource_path
	d["main"] = book.m.get_instance_id()
	d["caption"] = book.instruction.text
	d["checkpoint"] = book.progress_snapshot().duplicate(true)
	d["leaf_rect"] = OperaTreeBookTest.LEAF_RECT
	d["choices"] = [book.choice_rect(0),book.choice_rect(1),book.choice_rect(2),book.choice_rect(3)] if book.stage < 3 else []
	d["navigation"] = m._navigation_ref().top_id()
	d["private_profile"] = m._save_state.save_path
	return d

func _snapshot() -> Dictionary:
	var row := {"boot_count": boot_count, "time_scale": Engine.time_scale, "paused": paused, "disk": _disk(), "preview_mode": mode, "preview_alive": is_instance_valid(pointer_preview)}
	if is_instance_valid(m):
		row["main"] = {"id": m.get_instance_id(), "scene": m.scene_file_path, "game": m.game, "room": m.castle_room_id, "quality": m.quality, "private_save_path": m._save_state.save_path, "navigation_top": m._navigation_ref().top_id(), "menu": m.start_menu_active, "intro": m.intro_active, "caption_timer": m.msg_timer, "stars": m.opera_stars, "opera_progress": m.opera_progress, "pearls": m.pearl_count}
	if is_instance_valid(venue):
		row["venue"] = {"id": venue.get_instance_id(), "visible": venue.is_visible_in_tree(), "accepting_input": venue.accepting_input, "floor": venue.floor_index, "rect": str(venue.get_global_rect()), "practice_book": venue.practice_book != null, "practice_rect": str(venue.practice_book.get_global_rect()) if venue.practice_book != null else ""}
	if is_instance_valid(book):
		var textures: Dictionary = {}
		for key: String in book.textures:
			textures[key] = _tex(book.textures[key] as Texture2D)
		row["book"] = {"id": book.get_instance_id(), "parent": book.get_parent().get_instance_id(), "script": book.get_script().resource_path, "source_main_bound": book.m == m, "rect": str(book.get_global_rect()), "transform": str(book.get_global_transform_with_canvas()), "visible": book.is_visible_in_tree(), "stage": book.stage, "help": book.help_level, "idle_seconds": book.idle_seconds, "elapsed": book.elapsed, "treatment": book.treatment, "approach": book.approach, "suspended": book.suspended, "suspension_reasons": book.suspension_reasons.duplicate(), "closing": book.closing, "pressed_choice": book.pressed_choice, "pointer_id": book.pointer_id, "pointer_position": [book.pointer_position.x, book.pointer_position.y], "wrong_slot": book.wrong_slot, "wrong_time": book.wrong_time, "caption": book.instruction.text, "hand": _tex(book.hand), "textures": textures, "checkpoint": book.progress_snapshot(), "choice_rects": [_native_rect(book.choice_rect(0)), _native_rect(book.choice_rect(1)), _native_rect(book.choice_rect(2)), _native_rect(book.choice_rect(3))] if book.stage < 3 else [], "leaf_rect": _native_rect(OperaTreeBookTest.LEAF_RECT), "tip": _tip_state()}
	return row

func _capture(id: String, lane := "BOUNDED_CURRENT_CONTEXT") -> void:
	await RenderingServer.frame_post_draw
	var image: Image = root.get_texture().get_image()
	var path := out_dir.path_join(id + ".png")
	if image == null or image.get_size() != root.size or image.save_png(path) != OK:
		errors.append("bad framebuffer " + id)
		return
	states.append({"id": id, "path": id + ".png", "size": [image.get_width(), image.get_height()], "sha256": FileAccess.get_sha256(path), "classification": lane, "snapshot": _snapshot()})
	print("TREEBOOK75|CAPTURE|", id)

func _touch(c: Control, at: Vector2, down: bool, canceled := false) -> void:
	var e := InputEventScreenTouch.new()
	e.index = 75
	e.position = c.get_global_transform_with_canvas() * at
	e.pressed = down
	e.canceled = canceled
	events.append({"type": "touch", "down": down, "canceled": canceled, "local": [at.x, at.y], "native": [e.position.x, e.position.y], "target": str(c.get_path()), "stage_before": book.stage if is_instance_valid(book) else -1, "ticks": Time.get_ticks_msec()})
	c.get_viewport().push_input(e, true)

func _tap(c: Control, at: Vector2) -> void:
	_touch(c, at, true)
	await _frames(1)
	_touch(c, at, false)
	await _frames(2)

func _boot() -> bool:
	var scene := load("res://scenes/main.tscn") as PackedScene
	m = scene.instantiate() as ReefMain
	m._save_state = SaveState.new(m, profile)
	root.add_child(m)
	current_scene = m
	boot_count += 1
	await _frames(3)
	if not _check("private source SaveState dependency before ready", m._save_state.save_path == profile):
		return false
	if not await _wait(func() -> bool: return m.get_node_or_null("BootSplashHandoff") == null, 18.0):
		errors.append("splash did not settle")
		return false
	var button: Button = m.start_menu_layer.find_child("StartMenuContinueButton", true, false) as Button if m.start_menu_layer != null else null
	if not _check("original Continue available", button != null and button.is_visible_in_tree() and not button.disabled):
		return false
	await _tap(button, button.size * 0.5)
	if m.intro_active:
		m._skip_intro()
	if not await _wait(func() -> bool: return not m.start_menu_active and not m.intro_active and m.fade_rect.modulate.a <= 0.02, 18.0):
		errors.append("startup presentation did not settle")
		return false
	# Explicit private startup routing seam, before any observed book action. Not natural DayOne traversal.
	m.game = "level2"
	m.g["t"] = 0.0
	m._enter_castle_interior_now(false)
	await _frames(40)
	m._castle_rooms_ref().show_room("opera_hall", false)
	await _frames(12)
	return true

func _open_venue(prefix: String) -> bool:
	var routes: RefCounted = m._castle_career_routes_ref()
	routes.call("sync")
	await _frames(3)
	venue = routes.get("opera_venue") as OperaHouseVenue2D
	if not _check("original venue source constructed", is_instance_valid(venue)):
		return false
	await _capture(prefix + "_opera_room", "EXCLUDED_STARTUP_ROOM_DIAGNOSTIC")
	var record: Dictionary = m.castle_room_item_sprites.get("stage_star", {})
	var hotspot: Button = record.get("hotspot") as Button
	if not _check("original stage-star hotspot available", hotspot != null and hotspot.is_visible_in_tree() and not hotspot.disabled):
		return false
	await _tap(hotspot, hotspot.size * 0.5)
	if not await _wait(func() -> bool: return venue.is_open() and venue.accepting_input, 18.0):
		errors.append("source stage-star input did not open venue")
		return false
	await _capture(prefix + "_venue_open")
	return _check("source venue owns navigation", m._navigation_ref().top_id() == "opera_venue")

func _open_book(prefix: String) -> bool:
	var picture: TextureButton = venue.practice_book
	if not _check("original practice picture available", picture != null and picture.is_visible_in_tree() and not picture.disabled):
		return false
	await _tap(picture, picture.size * 0.5)
	if not await _wait(func() -> bool: return is_instance_valid(venue.tree_book_test) and venue.tree_book_test.is_node_ready(), 5.0):
		errors.append("original practice picture did not open book")
		return false
	book = venue.tree_book_test
	if mode == "registered":
		var before: Dictionary = _source_signature()
		pointer_preview = RegistrationPreview.new()
		var attached: bool = bool(pointer_preview.call("attach", book))
		var after: Dictionary = _source_signature()
		comparisons.append({"event": "attach_"+prefix, "source_signature_unchanged": before == after, "allowed_visual_changes": ["book.hand:null suppresses only original _fit(hand)", "fixture-owned child uses same texture/80or95square/source bob plus36or44px upward offset"]})
		if not _check("candidate attaches without source input state clock target changes " + prefix, attached and before == after):
			return false
	await _capture(prefix + "_book_open")
	return _check("source book owns navigation and main", book.m == m and m._navigation_ref().top_id() == "arborist_tree_book_test")

func _back(prefix: String) -> bool:
	var button: Button = m.global_navigation_button as Button
	if not _check("original global Back available", button != null and button.is_visible_in_tree() and not button.disabled):
		return false
	await _tap(button, button.size * 0.5)
	if not await _wait(func() -> bool: return venue.tree_book_test == null and venue.accepting_input, 5.0):
		errors.append("source Back did not restore venue")
		return false
	if mode == "registered":
		var disposed: bool = not is_instance_valid(pointer_preview)
		teardown_checks.append({"event": prefix, "source_teardown_disposed_preview": disposed})
		_check("source teardown disposes candidate " + prefix, disposed)
	pointer_preview = null
	book = null
	await _capture(prefix + "_venue_restored")
	return _check("Back restores source venue navigation", m._navigation_ref().top_id() == "opera_venue")

func _cycle_and_tip_input(prefix: String) -> bool:
	var rows: Array[Dictionary] = []
	var start := book.elapsed * 3.0
	var deadline := Time.get_ticks_msec() + 8000
	while book.elapsed * 3.0 - start < TAU and Time.get_ticks_msec() < deadline:
		await RenderingServer.frame_post_draw
		rows.append(_tip_state())
	if not _check("natural full hand cycle " + prefix, rows.size() > 15 and book.elapsed * 3.0 - start >= TAU):
		return false
	var outside := 0
	for row: Dictionary in rows:
		if not bool(row.get("inside", false)):
			outside += 1
	cycles.append({"id": prefix, "stage": book.stage, "start_phase": start, "end_phase": book.elapsed * 3.0, "samples": rows, "outside": outside, "total": rows.size()})
	var before_stage := book.stage
	var before_dose := book.treatment
	var tip := _tip_state()
	var point := Vector2(float(tip.local_tip[0]), float(tip.local_tip[1]))
	_touch(book, point, true)
	await _frames(8)
	await _capture(prefix + "_tip_pressed")
	_touch(book, point, false)
	await _frames(2)
	await _capture(prefix + "_tip_released")
	var advanced := book.stage != before_stage or book.treatment > before_dose + 0.001
	source_contracts.append({"id": prefix, "stage_before": before_stage, "tip": tip, "outside_samples": outside, "sample_count": rows.size(), "input_advanced": advanced, "stage_after": book.stage, "dose_before": before_dose, "dose_after": book.treatment, "status": "SOURCE_RENDERED_TIP_MISSES_ACTIONABLE_TARGET" if outside == rows.size() and not advanced else "CANDIDATE_RENDERED_TIP_ADVANCES_ORIGINAL_TARGET" if mode == "registered" and outside == 0 and advanced else "REVIEW_REQUIRED"})
	return _check("candidate point prediction advances " + prefix, outside == 0 and advanced) if mode == "registered" else _check("source point prediction matches miss " + prefix, outside == rows.size() and not advanced)

func _state_equal(left: Variant, right: Variant) -> bool:
	return JSON.parse_string(JSON.stringify(left)) == JSON.parse_string(JSON.stringify(right))

func _retire() -> void:
	if is_instance_valid(m):
		m.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		await _frames(2)
		m.queue_free()
		await _frames(5)
	m = null
	venue = null
	book = null

func _exercise() -> void:
	if not await _boot() or not await _open_venue("first") or not await _open_book("first"):
		return
	var original_stars := m.opera_stars
	var original_pearls := m.pearl_count
	for phase: int in range(3):
		if not _check("source sequential choice stage", book.stage == phase):
			return
		await _capture("choice%d_ready" % phase)
		if not await _wait(func() -> bool: return book.help_level >= 1, 8.0):
			errors.append("natural help1 did not arrive")
			return
		await _capture("choice%d_help1" % phase)
		if not await _wait(func() -> bool: return book.help_level == 2, 8.0):
			errors.append("natural help2 did not arrive")
			return
		await _capture("choice%d_help2" % phase)
		if not await _cycle_and_tip_input("choice%d" % phase):
			return
		if mode == "registered":
			if phase == 2:
				await _capture("carry_start")
			if not _check("registered tip advances original choice", book.stage == phase + 1):
				return
		else:
			var correct := book.choice_rect(book.answer_slot()).get_center()
			_touch(book, correct, true)
			await _frames(2)
			await _capture("choice%d_correct_pressed" % phase)
			_touch(book, correct, false)
			await _frames(1)
			if phase == 2:
				await _capture("carry_start")
			else:
				await _capture("choice%d_correct_released" % phase)
			if not _check("original centre input advances choice", book.stage == phase + 1):
				return
	if not await _wait(func() -> bool: return book.stage == 4, 5.0):
		errors.append("source carry did not reach treatment")
		return
	await _capture("treatment_ready")
	if not await _wait(func() -> bool: return book.help_level >= 1, 8.0):
		errors.append("natural treatment hand did not arrive")
		return
	await _capture("treatment_help")
	if not await _cycle_and_tip_input("treatment"):
		return
	var leaf := OperaTreeBookTest.LEAF_RECT.get_center()
	_touch(book, leaf, true)
	await _frames(8)
	await _capture("treatment_partial_pressed")
	_touch(book, leaf, false, true)
	await _frames(2)
	await _capture("treatment_partial_canceled")
	if not _check("source hold cancellation preserves partial dose", book.stage == 4 and book.treatment > 0.0 and book.treatment < 0.9 and book.pointer_id == -99):
		return
	var dose := book.treatment
	if not await _back("partial") or not await _open_book("partial_reopen"):
		return
	if not _check("original book reopens saved partial dose", book.stage == 4 and absf(book.treatment - dose) < 0.01):
		return
	await _back("before_main_reload")
	await _retire()
	if not await _boot() or not await _open_venue("reload") or not await _open_book("reload"):
		return
	if not _check("new original Main restores book checkpoint", boot_count == 2 and book.stage == 4 and absf(book.treatment - dose) < 0.01):
		return
	_touch(book, leaf, true)
	if not await _wait(func() -> bool: return book.stage == 5, 3.0):
		errors.append("source deliberate leaf hold did not complete")
		return
	_touch(book, leaf, false)
	await _frames(2)
	await _capture("healthy_complete")
	await _back("healthy")
	if not await _open_book("healthy_reopen"):
		return
	_check("completion persists on original reopen", book.stage == 5 and is_equal_approx(book.treatment, 1.0))
	await _tap(book, OperaTreeBookTest.REPLAY_RECT.get_center())
	await _capture("replay_started")
	_check("source replay returns to first decision", book.stage == 0 and is_zero_approx(book.treatment))
	_check("book does not award career or currency", m.opera_stars == original_stars and m.pearl_count == original_pearls)
	_check("private unknown sentinel retained", _state_equal(_disk().get("unknown"), seed.get("flat_vector_private_unknown")))
	if mode == "registered":
		var before: Dictionary = _source_signature()
		var restored: bool = bool(pointer_preview.call("restore"))
		var after: Dictionary = _source_signature()
		comparisons.append({"event": "detach_restore", "source_signature_unchanged": before == after, "restored_original_hand": book.hand != null and book.hand.resource_path == "res://assets/castle/training/ghost_hand.png"})
		_check("candidate restores exact original hand without source state changes", restored and before == after and book.hand != null)
		await _frames(2)
		await _capture("candidate_detached_restore", "CANDIDATE_RESTORE_DIAGNOSTIC")
	await _back("final")

func _run() -> void:
	var engine := Engine.get_version_info()
	if int(engine.get("major", 0)) != 4 or int(engine.get("minor", 0)) != 7 or int(engine.get("patch", 0)) != 2 or String(engine.get("status", "")) != "stable" or String(engine.get("build", "")) != "official" or RenderingServer.get_current_rendering_method() != "mobile" or DisplayServer.get_name() == "headless" or Engine.time_scale != 1.0:
		quit(1)
		return
	mode = OS.get_environment("R75_MODE")
	if mode not in ["control", "registered"]:
		quit(1)
		return
	out_dir = OS.get_environment("R75_OUT")
	var width := int(OS.get_environment("R75_WIDTH"))
	if out_dir.is_empty() or DirAccess.dir_exists_absolute(out_dir) or width not in [1280, 1600]:
		quit(1)
		return
	normal_before = _normal_hashes()
	DirAccess.make_dir_recursive_absolute(out_dir)
	profile = out_dir.path_join("private_profile/reef_save.json")
	DirAccess.make_dir_recursive_absolute(profile.get_base_dir())
	seed = {"schema_version": 1, "save_generation": 7, "day_one_active": false, "day_one_giant_dust_bunny_boss_defeated": true, "day_one_completed_rooms": DayOneDirector.ROOM_ORDER, "day_one_cleaned_rooms": DayOneDirector.ROOM_ORDER, "day_one_giant_dust_bunny_boss_triggered": true, "chapter2_active": true, "chapter2_unlocked_opera_mask": 0x0449, "chapter2_job_phase_masks": [0, 0, 0, 0, 0, 0, 0, 0], "skin": "classic", "music": false, "mic": false, "quality": "speedy", "pearls": 23, "pearls_ever": 23, "crafts": {}, "stickers": {}, "custom_fish": [], "custom_friends": [], "flat_vector_private_unknown": {"token": "R75_SYNTHETIC_ONLY", "keep": [4, 7]}}
	var file := FileAccess.open(profile, FileAccess.WRITE)
	file.store_string(JSON.stringify(seed, "\t", true) + "\n")
	file.close()
	if await _aspect(width):
		await _exercise()
	else:
		errors.append("native viewport did not settle")
	await _retire()
	_check("normal eleven save-name hashes unchanged", _normal_hashes() == normal_before)
	var report := {"schema": "reef.tree_book_registration/1", "mode": mode, "comparisons": comparisons, "teardown_checks": teardown_checks, "source_revision": OS.get_environment("R75_REV"), "engine": engine, "renderer": RenderingServer.get_current_rendering_method(), "display": DisplayServer.get_name(), "aspect": [width, 720], "time_scale": Engine.time_scale, "seed": seed, "private_profile": profile, "normal_before": normal_before, "normal_after": _normal_hashes(), "states": states, "events": events, "checks": checks, "errors": errors, "hint_cycles": cycles, "source_contracts": source_contracts, "observer_status": "PASS" if errors.is_empty() else "FAIL", "actual_child_data": false, "production_changes": [], "scope": "Current original Main/room/venue/book after declared private Castle room bootstrap; actual stage-star/practice/globalBack/choice/treatment/replay viewport inputs and natural clocks. Read-only bot geometry oracle, not child comprehension or QA11/device/owner acceptance. Source pointer failures are separate from observer health. No progress/help/camera/source file writes. Control has no visual writes. Registered mode substitutes only named hand visual resource and adds original-pixel child at fixed upward offset; actual target/input/state/clock unchanged, restoration/teardown checked. This preserves flat art and is not production, finalQA11 or creative acceptance."}
	var output := FileAccess.open(out_dir.path_join("capture_manifest.json"), FileAccess.WRITE)
	output.store_string(JSON.stringify(report, "\t", true) + "\n")
	output.close()
	print("TREEBOOK75|RESULT|", report.observer_status, "|", errors)
	quit(0 if errors.is_empty() else 1)
