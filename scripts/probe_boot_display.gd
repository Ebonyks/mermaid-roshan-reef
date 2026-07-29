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
# This probe boots main.tscn under a REAL viewport (Xvfb in CI) and takes no
# action at all: it just waits and asserts the promenade actually came up.

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

	_finish()


func _finish() -> void:
	if failures == 0:
		print("RESULT|PASS")
		quit(0)
	else:
		print("RESULT|FAIL|%d" % failures)
		quit(1)
