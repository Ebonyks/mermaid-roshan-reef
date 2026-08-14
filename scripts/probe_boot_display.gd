extends SceneTree

# Display-build boot gate.
#
# The first area the game shows is chosen inside ReefMain._ready(), behind
#   if START_AT_CASTLE_GATE and DisplayServer.get_name() != "headless":
# so the headless probe suite can NEVER execute it. Every existing check
# (probe_ocean_kingdoms, probe_l2) calls _enter_level2_now() by hand, several
# frames after boot, with a camera already in the tree — a different code path
# from the one the phone runs.
#
# Owner report 2026-07-29: the phone boots into the legacy 3D reef, with the
# reef sun already hidden and reef music playing. That combination is the
# signature of _enter_level2_now() starting (it hides sun_light and switches
# the track first) and then dying partway through the promenade build, which
# leaves the player standing in the reef that _ready() built underneath.
#
# This probe boots main.tscn under a REAL viewport (Xvfb in CI), verifies the
# untouched first frame, then dismisses the story and exercises the route the
# child sees. Headless probes cannot cover either display-only boot behavior.

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

	# The whole point: she must not be left in the open reef (game == "").
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

	# The route already exists while the story is open, but its prompt must wait
	# until the story is gone instead of expiring behind four full-screen pages.
	var route_target: Dictionary = {}
	for target_value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = target_value as Dictionary
		if String(target.get("id", "")) == "reef_route":
			route_target = target
			break
	_check(not route_target.is_empty(), "reef_route_is_visible_on_first_phone_frame")
	_check(float(route_target.get("radius_px", 0.0)) >= 128.0,
		"reef_route_has_child_touch_radius")
	_check(String(route_target.get("affordance_kind", "")) == "interaction",
		"reef_route_uses_blue_interaction_language")
	if main.first_session and main.intro_active:
		_check(bool(main.g.get("lagoon_reef_guidance_pending", false)),
			"reef_guidance_waits_behind_story")
	if main.intro_active:
		main._skip_intro()
	for _i in range(4):
		await process_frame
	_check(not bool(main.g.get("lagoon_reef_guidance_pending", true)),
		"reef_guidance_releases_after_story")
	_check(String(main.g.get("lagoon_promenade_focus", "")) == "reef_route",
		"reef_route_pulses_after_story")
	_check(main.msg_timer > 0.0 and main.hud_msg.text.contains("visit the Reef"),
		"reef_route_prompt_is_post_story_and_semantic")

	# One tap on the focused plane is enough: this is the normal visible return
	# route, not a hidden Pause-menu escape hatch.
	var route_node: CanvasItem = route_target.get("node") as CanvasItem
	var route_ready: bool = route_node != null and is_instance_valid(route_node)
	if route_ready:
		var route_screen: Vector2 = route_node.get_global_transform_with_canvas().origin
		promenade.handle_touch(route_screen)
		for _i in range(3):
			await process_frame
	_check(route_ready and main.game == "" and main.player.visible
		and main.we_node.environment == main.world_env,
		"one_tap_reef_route_restores_free_swim")

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
