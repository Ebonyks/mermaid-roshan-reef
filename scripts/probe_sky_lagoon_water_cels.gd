extends SceneTree
const Water := preload("res://scripts/arena/sky_lagoon_water_cels.gd")
var failures: int = 0
func check(label: String, okay: bool) -> void:
	print("SKYWATER|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var state: Dictionary = {}
	var blockers: Array[Sprite2D] = []
	check("original_unchanged", not Water.build(state, holder, "original", blockers) and holder.get_child_count() == 0)
	check("bounded_pool", Water.build(state, holder, "animated_v1", blockers) and holder.get_child_count() == 3)
	for index: int in range(2400):
		Water.tick(state, 0.016, false)
	check("no_input_no_effect", int(state["lagoon_water_emit_count"]) == 0)
	check("both_pools_accept", Water.is_water(state, Vector2(100, 1340)) and Water.is_water(state, Vector2(5600, 1400)))
	check("paths_and_rocks_reject", not Water.tap(state, Vector2(2000, 1650)) and not Water.tap(state, Vector2(5960, 1340)) and not Water.tap(state, Vector2(5830, 1520)))
	check("tap_consumed", Water.tap(state, Vector2(5600, 1400)))
	var slot: Dictionary = state["lagoon_water_slots"][0]
	var card: Sprite2D = slot["node"] as Sprite2D
	var sampled: Dictionary = {0: true}
	for index: int in range(95):
		Water.tick(state, 0.01, false)
		sampled[card.frame] = true
	check("all_eight_cels", sampled.size() == 8)
	check("fade_near_zero", card.modulate.a < 0.01)
	Water.tick(state, 0.02, false)
	check("complete_disappearance", not card.visible and card.modulate.a == 0.0 and float(slot["time"]) < 0.0)
	Water.tap(state, Vector2(5600, 1400))
	var before: float = float(slot["time"])
	for index: int in range(600):
		Water.tick(state, 1.0, true)
	check("pause_freezes", float(slot["time"]) == before)
	var count: int = int(state["lagoon_water_emit_count"])
	for index: int in range(100):
		Water.tap(state, Vector2(5600, 1400))
	check("burst_throttled", int(state["lagoon_water_emit_count"]) == count)
	for index: int in range(200):
		Water.tick(state, 0.1, false)
		Water.tap(state, Vector2(5600, 1400))
	check("pool_never_grows", holder.get_child_count() == 3)
	state["lagoon_water_motion_enabled"] = false
	Water.tick(state, 0.01, false)
	var hidden: bool = true
	for child: Node in holder.get_children():
		hidden = hidden and not (child as Sprite2D).visible
	check("static_hides_effects", hidden)
	var blocker := Sprite2D.new()
	var image := Image.create(64, 64, false, Image.FORMAT_RGBA8)
	image.fill(Color.WHITE)
	blocker.texture = ImageTexture.create_from_image(image)
	blocker.position = Vector2(5600, 1400)
	holder.add_child(blocker)
	blockers.append(blocker)
	Water.build(state, holder, "animated_v1", blockers)
	check("opaque_object_blocks_tap", not Water.tap(state, Vector2(5600, 1400)))
	blocker.free()
	check("freed_blocker_safe", Water.is_water(state, Vector2(5600, 1400)))
	Water.build(state, holder, "original", [])
	check("rollback_removes_pool", holder.get_child_count() == 0 and not state.has("lagoon_water_slots"))
	Water.build(state, holder, "animated_v1", [])
	holder.free()
	check("freed_parent_rejects_tap", not Water.tap(state, Vector2(5600, 1400)))
	Water.tick(state, 0.016, false)
	Water.clear(state)
	check("teardown_clears_state", not state.has("lagoon_water_slots"))
	print("SKYWATER|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
