extends SceneTree

## Focused state-only probe for the Day One art room and shared attack profile.
## No castle scene is opened: this keeps the progression/save contract cheap to
## exercise and proves malformed additive values fall back safely.

var failures: int = 0


func _init() -> void:
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
	for material: Dictionary in DayOneArtStudio.MATERIALS:
		var material_id: String = String(material["id"])
		studio.call("_on_material_pressed", material_id)
		_check("art tap %s never opens logo" % material_id,
			main.castle_logo_layer == null)
	for grime: Dictionary in DayOneArtStudio.GRIME:
		var grime_id: String = String(grime["id"])
		studio.call("_on_grime_pressed", grime_id)
		_check("art tap %s never opens logo" % grime_id,
			main.castle_logo_layer == null)
	_check("seven art taps finish cleanup without logo hijack",
		director.art_cleanup_complete() and director.art_desk_unlocked
		and main.castle_logo_layer == null)
	var customizer := AttackCustomizer.new()
	# Mount the picker the same way the live main scene does. A Control directly
	# under the SceneTree root has no CanvasLayer GUI routing in this state-only
	# probe, so Input.parse_input_event() cannot reach its dimmer. Viewport input
	# below is the real modal path and still tests the outside-card gesture.
	var customizer_layer := CanvasLayer.new()
	customizer_layer.layer = 18
	root.add_child(customizer_layer)
	customizer_layer.add_child(customizer)
	customizer.attach(main)
	var confirmations := 0
	customizer.open(func() -> void: confirmations += 1)
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
	dim_tap.pressed = true
	dim_tap.position = Vector2(40.0, 40.0)
	customizer.get_viewport().push_input(dim_tap, false)
	await process_frame
	_check("dim tap before a choice does not confirm", customizer.is_open)
	customizer._on_color_pressed(AttackCustomizer.COLORS[3] as Color)
	var chosen: Dictionary = customizer.audit_snapshot()
	_check("color choice is visible before confirmation",
		bool(chosen.get("choice_made", false))
		and customizer.attack_color.is_equal_approx(AttackCustomizer.COLORS[3] as Color))
	var confirm_tap := InputEventScreenTouch.new()
	confirm_tap.pressed = true
	confirm_tap.position = Vector2(40.0, 40.0)
	customizer.get_viewport().push_input(confirm_tap, false)
	await process_frame
	_check("dim tap after one choice confirms", not customizer.is_open
		and confirmations == 1)
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
	# SceneTree teardown owns the two root children. Queueing them during
	# SceneTree._init() trips Godot's root lock even though gameplay teardown is
	# safe after the first frame.
	main.free()
	print("DAY_ONE_ART_ATTACK_STATE|RESULT: ",
		"PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)


func _check(label: String, ok: bool) -> void:
	if not ok:
		failures += 1
	print("DAY_ONE_ART_ATTACK_STATE|", label, ": ", "OK" if ok else "FAIL")
