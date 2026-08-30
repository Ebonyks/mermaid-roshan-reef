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
	_check("all nine saved cleanup actions unlock the desk",
		director.art_desk_unlocked and director.art_cleanup_complete())
	_check("customization is desk-gated",
		director.complete_art_customization()
		and director.art_customization_completed)
	# Move the focused state probe to Art without invoking Bathroom's separate
	# live basket/scrub gates, which belong to its integration probe.
	director.completed_rooms = {
		"bathroom": true, "pool": true, "stuffie": true,
	}
	director.current_room_id = "art"
	_check("art completion uses the existing room order",
		director.current_room_id == "art"
		and director.complete_art_studio()
		and director.is_room_completed("art"))
	var saved: Dictionary = director.serialize_state()
	_check("serialized art state is JSON-safe",
		(saved.get("day_one_art_collected_materials", {}) as Dictionary).size() == 6
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
	_check("studio builds ten ordered Canvas cleanup targets at castle scale",
		int(studio_audit.get("material_count", 0)) == 6
		and int(studio_audit.get("grime_count", 0)) == 3
		and int(studio_audit.get("material_art_count", 0)) == 6
		and int(studio_audit.get("grime_art_count", 0)) == 3
		and int(studio_audit.get("ordered_interaction_count", 0)) == 11
		and bool(studio_audit.get("target_table_clearance_pass", false))
		and bool(studio_audit.get("canvas_only", false))
		and studio.scale.is_equal_approx(Vector2.ONE * 1.25))
	var customizer := AttackCustomizer.new()
	root.add_child(customizer)
	customizer.attach(main)
	customizer.open()
	var customizer_audit: Dictionary = customizer.audit_snapshot()
	_check("customizer builds five colors, two effects and picture confirmation",
		int(customizer_audit.get("color_choices", 0)) == 5
		and int(customizer_audit.get("effect_choices", 0)) == 2
		and bool(customizer_audit.get("confirm_button", false))
		and bool(customizer_audit.get("painted_brush", false))
		and bool(customizer_audit.get("painted_effect_previews", false))
		and bool(customizer_audit.get("canvas_only", false)))
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
