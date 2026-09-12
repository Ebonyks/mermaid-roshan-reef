extends SceneTree

## Focused state and real GUI-touch probe for the Day One art room and shared
## attack profile. No castle scene is opened; the actual Canvas controls still
## receive ordinary touch input, including the mouse-emulation path.

var failures: int = 0


func _init() -> void:
	# Window setup during SceneTree construction is overwritten by engine
	# initialization, making parsed input miss an otherwise visible control.
	call_deferred("_run")


func _run() -> void:
	var main: ReefMain = ReefMain.new()
	var director: DayOneDirector = main._day_one_ref()
	_check("child-friendly aqua attack default",
		main.attack_color.is_equal_approx(Color(
			0.2705882353, 0.8588235294, 0.9215686275, 1.0))
		and main.attack_effect == "bubbles")
	_check("art begins empty and gated",
		director.art_collected_materials.is_empty()
		and director.art_cleaned_grime.is_empty()
		and not director.art_desk_unlocked
		and not director.art_customization_completed
		and not director.complete_art_studio())
	_check("one pickup and one scrub cannot unlock the desk",
		director.record_art_cleanup("material", "brushes")
		and director.record_art_cleanup("grime", "left_counter")
		and not director.art_desk_unlocked)
	for material_id: String in DayOneDirector.ART_MATERIAL_IDS:
		director.record_art_cleanup("material", material_id)
	for grime_id: String in DayOneDirector.ART_GRIME_IDS:
		director.record_art_cleanup("grime", grime_id)
	_check("all seven cleanup actions unlock the desk",
		director.art_desk_unlocked and director.art_cleanup_complete())
	_check("customization is desk-gated",
		director.complete_art_customization()
		and director.art_customization_completed)
	# Move the route to the art room without touching the physical castle.
	# Mirror the persisted bathroom boundary required by the live director. The
	# art probe is state-only, so seed the already-completed rescue rather than
	# pretending a fresh bathroom can complete without its two gestures.
	director.bathroom_supply_hunt_step = 2
	director.bathroom_tools_authorized = true
	director.bathroom_cleanup_step = 2
	director.bathroom_toilet_cleaned = true
	director.complete_tutorial("bathroom")
	director.complete_activity("pool", "pool_activity")
	director.complete_activity("stuffie", "stuffie_activity")
	_check("art completion uses the existing room order",
		director.current_room_id == "art"
		and director.complete_art_studio()
		and director.is_room_completed("art"))
	var saved: Dictionary = director.serialize_state()
	_check("serialized art state is JSON-safe",
		(saved.get("day_one_art_collected_materials", {}) as Dictionary).size() == 4
		and (saved.get("day_one_art_cleaned_grime", {}) as Dictionary).size() == 3
		and bool(saved.get("day_one_art_desk_unlocked", false))
		and bool(saved.get("day_one_art_customization_completed", false)))
	var malformed: Dictionary = SaveState.new(main)._normalise_save({
		"attack_color": "not-a-colour",
		"attack_effect": "rainbow",
		"day_one_art_collected_materials": ["PAINTS"],
		"day_one_art_cleaned_grime": {"COUNTER": 1},
		"day_one_art_desk_unlocked": true,
		"day_one_art_customization_completed": true,
	})
	_check("malformed attack values use safe defaults",
		malformed.get("attack_effect", "") == "bubbles"
		and Color.from_string(String(malformed.get("attack_color", "")),
			Color.BLACK).is_equal_approx(Color(
				0.2705882353, 0.8588235294, 0.9215686275, 1.0)))
	_check("partial unknown art collections remain safely gated",
		malformed.get("day_one_art_collected_materials", {}) == {"paints": true}
		and malformed.get("day_one_art_cleaned_grime", {}) == {"counter": true}
		and not bool(malformed.get("day_one_art_desk_unlocked", false))
		and not bool(malformed.get("day_one_art_customization_completed", false)))
	var studio := DayOneArtStudio.new()
	# The focused probe omits the full castle scene, so provide the same Canvas
	# world owner that the real Craft Room mounts before the studio opens.
	main.castle_room_world_root = Node2D.new()
	root.add_child(main.castle_room_world_root)
	root.add_child(studio)
	studio.setup(main, false)
	var studio_audit: Dictionary = studio.audit_snapshot()
	_check("studio builds seven large Canvas cleanup targets at castle scale",
		int(studio_audit.get("material_count", 0)) == 4
		and int(studio_audit.get("grime_count", 0)) == 3
		and int(studio_audit.get("material_art_count", 0)) == 4
		and int(studio_audit.get("grime_art_count", 0)) == 3
		and bool(studio_audit.get("canvas_only", false))
		and studio.scale.is_equal_approx(Vector2.ONE * 1.25))
	# Exercise the actual seven touch handlers in their Day One room context.
	# The craft-room paint-table card is shared with the later logo studio, so
	# this is deliberately fail-closed: every cleanup tap must leave that layer
	# absent, including the two taps that animate the shared station.
	director.day_one_active = true
	director.current_room_id = "art"
	main.day_one_art_collected_materials = {}
	main.day_one_art_cleaned_grime = {}
	main.day_one_art_desk_unlocked = false
	main.day_one_art_customization_completed = false
	studio.refresh_from_state()
	root.size = Vector2i(1280, 720)
	await process_frame
	# Keep the required 160px targets generous while separating neighbours.
	# A blank gap must not silently choose either adjacent supply.
	for index: int in range(DayOneArtStudio.MATERIALS.size() - 1):
		var left_id: String = String(DayOneArtStudio.MATERIALS[index]["id"])
		var right_id: String = String(DayOneArtStudio.MATERIALS[index + 1]["id"])
		var left: Button = studio._material_buttons[left_id] as Button
		var right: Button = studio._material_buttons[right_id] as Button
		var left_rect: Rect2 = left.get_global_rect()
		var right_rect: Rect2 = right.get_global_rect()
		_check("art neighbours %s/%s have separate generous targets" % [left_id, right_id],
			not left_rect.intersects(right_rect)
			and left_rect.size.x >= 110.0 and right_rect.size.x >= 110.0
			and left_rect.size.y >= 110.0 and right_rect.size.y >= 110.0)
		var gap := Vector2((left_rect.end.x + right_rect.position.x) * 0.5,
			left_rect.get_center().y)
		await _art_gui_tap(gap)
		_check("gap between %s/%s does not collect a neighbour" % [left_id, right_id],
			main.day_one_art_collected_materials.is_empty())
	for material: Dictionary in DayOneArtStudio.MATERIALS:
		var material_id: String = String(material["id"])
		var card: Sprite2D = studio._material_art[material_id] as Sprite2D
		var button: Button = studio._material_buttons[material_id] as Button
		var visible_center: Vector2 = card.get_global_transform_with_canvas().origin
		var pointer_center: Vector2 = studio._pointer.get_global_transform_with_canvas() \
			* (studio._pointer.size * 0.5)
		_check("hand points above visible %s in its touch region" % material_id,
			absf(pointer_center.x - visible_center.x) < 1.0
			and pointer_center.y < visible_center.y
			and button.get_global_rect().has_point(visible_center))
		var before_count: int = main.day_one_art_collected_materials.size()
		await _art_gui_tap(visible_center)
		_check("one visible %s tap collects only that supply" % material_id,
			bool(main.day_one_art_collected_materials.get(material_id, false))
			and main.day_one_art_collected_materials.size() == before_count + 1)
		_check("art tap %s never opens logo" % material_id,
			main.castle_logo_layer == null)
	for grime: Dictionary in DayOneArtStudio.GRIME:
		var grime_id: String = String(grime["id"])
		var grime_card: Sprite2D = studio._grime_art[grime_id] as Sprite2D
		var grime_center: Vector2 = grime_card.get_global_transform_with_canvas().origin
		var hand_center: Vector2 = studio._pointer.get_global_transform_with_canvas() \
			* (studio._pointer.size * 0.5)
		_check("hand points above visible %s" % grime_id,
			absf(hand_center.x - grime_center.x) < 1.0 and hand_center.y < grime_center.y)
		await _art_gui_tap(grime_center)
		_check("visible %s touch cleans its own spot" % grime_id,
			bool(main.day_one_art_cleaned_grime.get(grime_id, false)))
		_check("art tap %s never opens logo" % grime_id,
			main.castle_logo_layer == null)
	_check("seven art taps finish cleanup without logo hijack",
		director.art_cleanup_complete() and director.art_desk_unlocked
		and main.castle_logo_layer == null)
	var customizer := AttackCustomizer.new()
	# Mount the picker under the SceneTree root, as the live CanvasLayer path does.
	# `main` is intentionally state-only and is not in the tree, so a CanvasLayer
	# parented to it has no viewport and cannot receive modal GUI input.
	var customizer_layer := CanvasLayer.new()
	customizer_layer.layer = 18
	root.add_child(customizer_layer)
	customizer_layer.add_child(customizer)
	# Wait for the layer's viewport-enter notification before pushing the
	# outside tap; the modal needs its actual viewport to receive GUI input.
	await process_frame
	customizer.attach(main)
	var confirmations := [0]
	customizer.open(func() -> void: confirmations[0] += 1)
	var customizer_audit: Dictionary = customizer.audit_snapshot()
	_check("customizer opens with child guidance and picture confirmation",
		int(customizer_audit.get("color_choices", 0)) == 5
		and int(customizer_audit.get("effect_choices", 0)) == 2
		and bool(customizer_audit.get("confirm_button", false))
		and bool(customizer_audit.get("painted_brush", false))
		and bool(customizer_audit.get("painted_effect_previews", false))
		and bool(customizer_audit.get("visual_pointer", false))
		and not bool(customizer_audit.get("choice_made", false))
		and bool(customizer_audit.get("canvas_only", false)))
	var dim_tap := InputEventScreenTouch.new()
	dim_tap.index = 0
	dim_tap.pressed = true
	dim_tap.position = Vector2(40.0, 40.0)
	var picker_viewport: Viewport = customizer.get_viewport()
	picker_viewport.size = Vector2i(1280, 720)
	picker_viewport.push_input(dim_tap, false)
	await process_frame
	_check("dim tap before a choice does not confirm", customizer.is_open)
	# Complete the physical touch before sending the next one. Two pressed
	# events with the same finger index are one held contact to the viewport,
	# not two child-sized taps, so the second dim tap would be ignored.
	var dim_release := InputEventScreenTouch.new()
	dim_release.index = 0
	dim_release.pressed = false
	dim_release.position = dim_tap.position
	picker_viewport.push_input(dim_release, false)
	await process_frame
	customizer._on_color_pressed(AttackCustomizer.COLORS[3] as Color)
	var chosen: Dictionary = customizer.audit_snapshot()
	_check("color choice is visible before confirmation",
		bool(chosen.get("choice_made", false))
		and customizer.attack_color.is_equal_approx(AttackCustomizer.COLORS[3] as Color))
	var confirm_tap := InputEventScreenTouch.new()
	confirm_tap.index = 0
	confirm_tap.pressed = true
	confirm_tap.position = Vector2(40.0, 40.0)
	picker_viewport.push_input(confirm_tap, false)
	await process_frame
	var confirm_release := InputEventScreenTouch.new()
	confirm_release.index = 0
	confirm_release.pressed = false
	confirm_release.position = confirm_tap.position
	picker_viewport.push_input(confirm_release, false)
	_check("dim tap after one choice confirms", not customizer.is_open
		and confirmations[0] == 1)
	# Grand Puff owns one HitEngine feedback instance for the whole encounter.
	# Its Canvas layer must consume the saved profile on every accepted tap and
	# be torn down with the encounter, without leaving a global overlay behind.
	main.attack_color = Color(1.0, 0.48, 0.55, 1.0)
	main.attack_effect = "splashes"
	var boss_game := DustBossGame.new(main)
	main.g = {}
	boss_game._ensure_attack_feedback()
	boss_game._on_tap_progress(1, 3)
	var feedback: HitEngine = boss_game.attack_feedback
	var fx_layer: CanvasLayer = feedback.attack_fx_layer
	var fx: Node = fx_layer.get_child(0) as Node \
		if fx_layer != null and fx_layer.get_child_count() > 0 else null
	var fx_sprite: Sprite2D = fx.get("sprite") as Sprite2D if fx != null else null
	_check("Grand Puff feedback uses saved color and splash effect",
		feedback != null and fx_layer != null and fx != null and fx_sprite != null
		and String(fx.get("effect")) == "splashes"
		and (fx.get("tint") as Color).is_equal_approx(main.attack_color)
		and fx_sprite.texture.resource_path.ends_with(
			"fx_water_splash_medium_atlas.png"))
	boss_game.stage_close()
	_check("Grand Puff feedback tears down with encounter",
		boss_game.attack_feedback == null)
	# SceneTree teardown owns the root children; the state-only main was never
	# attached to it and must be freed explicitly.
	main.free()
	print("DAY_ONE_ART_ATTACK_STATE|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _art_gui_tap(point: Vector2) -> void:
	var press := InputEventScreenTouch.new()
	press.index = 0
	press.pressed = true
	press.position = point
	Input.parse_input_event(press)
	await process_frame
	var release := InputEventScreenTouch.new()
	release.index = 0
	release.pressed = false
	release.position = point
	Input.parse_input_event(release)
	await process_frame


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_ART_ATTACK_STATE|", label, ": ", "OK" if ok else "FAIL")
