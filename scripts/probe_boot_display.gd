extends SceneTree

# Display-build boot gate.
#
# The display build now waits at the start menu. The headless suite cannot
# exercise that viewport-only surface, so this probe verifies the real menu,
# activates its real Continue button, and then checks the resulting promenade.
# The XDG sandbox is intentionally fresh, so Continue begins disabled; the
# fixture marks the already-loaded session as resumable before pressing it.
#
# Owner report 2026-07-29: the phone boots into the legacy 3D reef, with the
# reef sun already hidden and reef music playing. That combination is the
# signature of _enter_level2_now() starting (it hides sun_light and switches
# the track first) and then dying partway through the promenade build, which
# leaves the player standing in the reef that _ready() built underneath.
#
# This probe boots main.tscn under a REAL viewport (Xvfb in CI), verifies the
# untouched menu, then exercises Continue and the visible route the child sees.
# Headless probes cannot cover either display-only boot behavior.

var failures: int = 0


func _initialize() -> void:
	call_deferred("_run")


func _check(condition: bool, label: String) -> void:
	if condition:
		print("BOOTDISPLAY|%s|OK" % label)
	else:
		failures += 1
		print("BOOTDISPLAY|%s|FAIL" % label)


func _run() -> void:
	# A headless run would skip the very branch this probe exists to cover and
	# then pass vacuously, so refuse to be green in that case.
	_check(DisplayServer.get_name() != "headless", "probe_runs_on_a_real_display")
	if DisplayServer.get_name() == "headless":
		_finish()
		return

	var packed: PackedScene = load("res://scenes/main.tscn") as PackedScene
	_check(packed != null, "main_scene_loads")
	if packed == null:
		_finish()
		return
	var main: ReefMain = packed.instantiate() as ReefMain
	_check(main != null, "main_is_reef_main")
	if main == null:
		_finish()
		return
	root.add_child(main)
	# the lens is created deferred; give the boot entry room to finish
	for i in range(20):
		await process_frame

	_check(main.start_menu_active, "boot_waits_at_start_menu")
	_check(main.game == "", "menu_does_not_enter_the_world_early")
	_check(main.water_node == null and main.sun_light == null \
		and main.caustics_plane == null and main.portal_node == null \
		and main.pearls.is_empty() and main.friends.is_empty() \
		and main.aquatic_movers.is_empty(),
		"retired_reef_nodes_are_never_constructed_in_display_build")
	var menu_layer: CanvasLayer = main.start_menu_layer
	_check(menu_layer != null and is_instance_valid(menu_layer),
		"start_menu_canvas_is_in_the_tree")
	if menu_layer == null or not is_instance_valid(menu_layer):
		_finish()
		return
	var continue_button := menu_layer.find_child(
		"StartMenuContinueButton", true, false) as Button
	var new_game_button := menu_layer.find_child(
		"StartMenuNewGameButton", true, false) as Button
	var options_button := menu_layer.find_child(
		"StartMenuOptionsTab", true, false) as Button
	_check(continue_button != null and continue_button.disabled,
		"fresh_boot_continue_is_disabled")
	_check(new_game_button != null and not new_game_button.disabled,
		"fresh_boot_new_game_is_available")
	_check(options_button != null and not options_button.disabled,
		"fresh_boot_options_is_available")
	if continue_button == null:
		_finish()
		return

	# Exercise the actual Continue signal after making this isolated in-memory
	# fixture represent an existing loaded save. Continue must never start Day 1.
	main.has_saved_game = true
	continue_button.disabled = false
	continue_button.pressed.emit()
	for i in range(20):
		await process_frame
	_check(not main.start_menu_active, "continue_closes_start_menu")
	_check(not main.day_one_is_active(), "continue_bypasses_day_one")

	# Continue must now land in gameplay rather than leave her in the reef shell.
	_check(main.game == "level2", "boot_leaves_the_reef")
	_check(String(main.g.get("phase", "")) == "promenade", "boot_lands_on_the_promenade")

	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	_check(promenade != null, "promenade_exists")
	if promenade == null:
		_finish()
		return
	var stage_root: CanvasLayer = promenade.root()
	var canvas_root: Control = promenade.canvas_root()
	var camera: Camera2D = promenade.camera_2d()
	_check(stage_root != null and is_instance_valid(stage_root)
		and stage_root.layer == main.SKY_LAGOON_STAGE_CANVAS_LAYER,
		"promenade_canvas_layer_is_in_the_tree")
	_check(canvas_root != null and is_instance_valid(canvas_root)
		and canvas_root.name == &"SkyLagoonViewport"
		and camera != null and is_instance_valid(camera) and camera.enabled,
		"promenade_owns_full_rect_canvas_and_camera2d")
	_check(not main.player.cam.current,
		"promenade_has_no_active_spatial_camera")

	# A single failed texture load used to abort build() silently, half-way
	# through, which is what put her back in the reef. Every painted tile of
	# the mural has to be present AND carry a texture.
	var painted := 0
	if stage_root != null:
		for row in range(2):
			for column in range(6):
				var tile := stage_root.find_child(
					"SkyLagoonBackdrop_r%d_c%d" % [row, column], true, false) as Sprite2D
				if tile != null and tile.texture != null:
					painted += 1
	_check(painted == 12, "mural_is_whole_%d_of_12" % painted)

	# The hidden generic player is not layout authority. The visible actor starts
	# on page one in native master pixels and the Camera2D follows that route.
	var spawn_x: float = promenade.master_route_x()
	_check(spawn_x >= 0.0 and spawn_x < 2048.0
		and is_equal_approx(spawn_x, float(main.g.get("lagoon_master_x", -1.0)))
		and not main.player.visible, "canvas_actor_spawns_on_screen_one")

	# The retired Reef route must not exist on the first phone frame. The arrival
	# plane may finish its story beat, but it is no longer an interaction target.
	var has_retired_route: bool = false
	for target_value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = target_value as Dictionary
		if String(target.get("id", "")) == "reef_route":
			has_retired_route = true
			break
	_check(not has_retired_route, "retired_reef_route_absent_on_first_phone_frame")
	var arrival_plane: Sprite2D = main.g.get("lagoon_plane_card") as Sprite2D
	_check(arrival_plane == null or not arrival_plane.has_meta("interaction_id"),
		"arrival_plane_is_story_dressing_only")
	if main.first_session and main.intro_active:
		_check(bool(main.g.get("lagoon_castle_guidance_pending", false)),
			"castle_guidance_waits_behind_story")
	if main.intro_active:
		main._skip_intro()
	for _i in range(4):
		await process_frame
	_check(not bool(main.g.get("lagoon_castle_guidance_pending", true)),
		"castle_guidance_releases_after_story")
	_check(main.msg_timer > 0.0 and main.hud_msg.text.contains("castle"),
		"castle_prompt_is_post_story_and_semantic")
	_check(main.game == "level2" and not main.player.visible,
		"boot_remains_in_live_canvas_game")

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
