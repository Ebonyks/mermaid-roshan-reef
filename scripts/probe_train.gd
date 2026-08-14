extends SceneTree
# The retired courtyard train is covered here by the Canvas promenade's real
# assisted route, synchronous teardown and exact rebuild contract.

const TARGET_IDS: Array[String] = [
	"castle_gate", "reef_route", "seesaw", "slide", "swing",
]


func _frames(count: int) -> void:
	for _index: int in range(count):
		await process_frame


func _ids(main: ReefMain) -> Array[String]:
	var result: Array[String] = []
	for value: Variant in main.g.get("lagoon_promenade_targets", []) as Array:
		result.append(String((value as Dictionary).get("id", "")))
	result.sort()
	return result


func _init() -> void:
	var scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	var main: ReefMain = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _frames(2)
	if main.intro_active:
		main._skip_intro()
	await _frames(2)
	main.pearl_count = main.PEARL_TOTAL
	for friend_value: Variant in main.friends:
		var friend: Dictionary = friend_value as Dictionary
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	main.save_data["lagoon_plane_departed"] = true
	main._enter_level2()
	await _frames(8)
	var promenade: SkyLagoonPromenade = main._lagoon_promenade_ref()
	var phase_ok: bool = String(main.g.get("phase", "")) == "promenade" \
		and promenade.root() is CanvasLayer and promenade.camera_2d() is Camera2D \
		and not main.player.visible
	print("TRAIN|Canvas promenade replaces courtyard train: ",
		"OK" if phase_ok else "FAIL")

	promenade.set_master_route_x(2048.0)
	var start_x: float = promenade.master_route_x()
	var destination := Vector2(4300.0, float(main.g.get("lagoon_master_y", 1450.0)))
	promenade._set_walk_goal(promenade.screen_from_master(destination))
	for _index: int in range(300):
		promenade.tick(1.0 / 60.0)
	var travelled: float = promenade.master_route_x() - start_x
	var travel_ok: bool = travelled > 120.0 \
		and main.g.get("lagoon_walk_goal_master") == null \
		and absf(promenade.master_route_x() - destination.x) \
			<= SkyLagoonPromenade.ARRIVE_RADIUS_MASTER \
		and is_equal_approx(float(main.g.get("lagoon_master_x", -1.0)),
			promenade.master_route_x())
	print("TRAIN|assisted Canvas route moved %.1f: %s" % [
		travelled, "OK" if travel_ok else "FAIL"])

	var old_root: CanvasLayer = promenade.root()
	main._enter_castle_interior()
	await _frames(8)
	var cleanup_ok: bool = not is_instance_valid(old_root) \
		and String(main.g.get("phase", "")) == "hall" \
		and not main.g.has("lagoon_walk_goal_master")
	print("TRAIN|Canvas promenade clears on castle entry: ",
		"OK" if cleanup_ok else "FAIL")

	main._enter_level2(true)
	await _frames(8)
	promenade = main._lagoon_promenade_ref()
	var rebuild_ok: bool = String(main.g.get("phase", "")) == "promenade" \
		and promenade.root() is CanvasLayer and promenade.camera_2d() is Camera2D \
		and _ids(main) == TARGET_IDS
	print("TRAIN|Canvas promenade rebuilds: ", "OK" if rebuild_ok else "FAIL")
	if not (phase_ok and travel_ok and cleanup_ok and rebuild_ok):
		print("FAIL|Sky Lagoon Canvas traversal regression")
		quit(1)
	else:
		print("=== TRAIN PROBE ALL OK ===")
		quit(0)
