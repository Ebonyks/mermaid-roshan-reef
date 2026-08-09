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

	var promenade := main._lagoon_promenade_ref()
	_check(promenade != null, "promenade_exists")
	if promenade == null:
		_finish()
		return
	var stage_root: Node3D = promenade.stage.root()
	_check(stage_root != null, "promenade_stage_is_in_the_tree")

	# A single failed texture load used to abort build() silently, half-way
	# through, which is what put her back in the reef. Every painted tile of
	# the mural has to be present AND carry a texture.
	var painted := 0
	if stage_root != null:
		for row in range(2):
			for column in range(6):
				var tile := stage_root.get_node_or_null(
					"SkyLagoonBackdrop_r%d_c%d" % [row, column]) as Sprite3D
				if tile != null and tile.texture != null:
					painted += 1
	_check(painted == 12, "mural_is_whole_%d_of_12" % painted)

	# and she is standing on the promenade, not at the reef origin
	var from_lagoon: float = main.player.position.distance_to(main.LEVEL2_POS)
	_check(from_lagoon < 120.0, "player_spawns_on_the_promenade")

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
	var route_node: Node3D = route_target.get("node") as Node3D
	var route_ready: bool = route_node != null and is_instance_valid(route_node)
	if route_ready:
		var route_screen: Vector2 = main.player.cam.unproject_position(
			route_node.global_position)
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
