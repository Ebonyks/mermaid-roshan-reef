extends SceneTree
const Plants := preload("res://scripts/arena/sky_lagoon_plant_cels.gd")
var failures: int = 0
func check(label: String, okay: bool) -> void:
	print("SKYPLANTS|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var state: Dictionary = {}
	check("original_unchanged", not Plants.build(state, holder, "original", false) and holder.get_child_count() == 0)
	check("two_sparse_plants_build", Plants.build(state, holder, "animated_v1", false) and holder.get_child_count() == 2)
	var sampled: Dictionary = {}
	var anchors_ok: bool = true
	for index: int in range(2400):
		Plants.tick(state, 0.016, false)
		for child: Node in holder.get_children():
			var card: Sprite2D = child as Sprite2D
			sampled[card.frame] = true
			anchors_ok = anchors_ok and card.get_rect().size == Vector2(512, 512)
			anchors_ok = anchors_ok and (card.position + (Plants.ROOT - Plants.CELL * 0.5) * card.scale).is_equal_approx(card.get_meta("root_anchor") as Vector2)
	check("all_eight_cells_sampled", sampled.size() == 8)
	check("roots_fixed_for_2400_ticks", anchors_ok)
	var before: float = float(state["lagoon_plant_cel_t"])
	for index: int in range(600):
		Plants.tick(state, 10.0, true)
	check("pause_freezes_clock", float(state["lagoon_plant_cel_t"]) == before)
	state["lagoon_plants_motion_enabled"] = false
	Plants.tick(state, 1.0, false)
	var rest: bool = true
	for child: Node in holder.get_children():
		rest = rest and (child as Sprite2D).frame == 0
	check("static_rest", rest)
	var rebuild_ok: bool = true
	for index: int in range(40):
		Plants.build(state, holder, "animated_v1", index % 2 == 0)
		rebuild_ok = rebuild_ok and holder.get_child_count() == 2
		for child: Node in holder.get_children():
			var card: Sprite2D = child as Sprite2D
			rebuild_ok = rebuild_ok and (card.modulate != Color.WHITE if index % 2 == 0 else card.modulate == Color.WHITE)
	check("rebuild_and_night_tint", rebuild_ok)
	Plants.build(state, holder, "original", false)
	check("rollback_removes_plants", holder.get_child_count() == 0 and not state.has("lagoon_plant_cels"))
	Plants.build(state, holder, "animated_v1", false)
	holder.free()
	Plants.tick(state, 0.016, false)
	Plants.clear(state)
	check("freed_parent_cleanup", not state.has("lagoon_plant_cels"))
	print("SKYPLANTS|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
