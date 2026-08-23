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

	# The opening plane and its dirt landing are scenery, not a hidden route back
	# to the retired 3D Reef. They must already read on the first phone frame.
	var route_target: Dictionary = {}
	for target_value in (main.g.get("lagoon_promenade_targets", []) as Array):
		var target: Dictionary = target_value as Dictionary
		if String(target.get("id", "")) == "reef_route":
			route_target = target
			break
	var plane: Sprite2D = main.g.get("lagoon_plane_card") as Sprite2D
	var landing: Sprite2D = main.g.get("lagoon_dirt_landing_card") as Sprite2D
	_check(route_target.is_empty(), "retired_reef_route_is_absent")
	_check(plane != null and is_instance_valid(plane) and plane.texture != null,
		"grounded_plane_is_visible_on_first_phone_frame")
	_check(landing != null and is_instance_valid(landing) and landing.texture != null,
		"dirt_landing_is_visible_on_first_phone_frame")
	if main.intro_active:
		main._skip_intro()
	for _i in range(4):
		await process_frame
	var water_screen: Vector2 = promenade.screen_from_master(Vector2(180.0, 1320.0))
	promenade.handle_touch(water_screen)
	for _i in range(3):
		await process_frame
	_check(main.game == "level2" and String(main.g.get("phase", "")) == "promenade"
		and not main.player.visible, "water_tap_cannot_restore_retired_free_swim")

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
