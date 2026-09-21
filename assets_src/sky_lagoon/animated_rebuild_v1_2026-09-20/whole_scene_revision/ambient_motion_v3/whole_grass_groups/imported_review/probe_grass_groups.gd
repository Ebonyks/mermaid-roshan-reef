extends SceneTree
const GRASS := preload("res://scripts/arena/sky_lagoon_grass_groups.gd")
var failures: int = 0
func check(label: String, condition: bool) -> void:
	print("GRASS|", label, "|", "PASS" if condition else "FAIL")
	if not condition:
		failures += 1
func _initialize() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var state: Dictionary = {}
	check("missing_all_or_none", not GRASS.build(state, holder, Color.WHITE, "res://missing_grass/") and holder.get_child_count() == 0)
	check("build", GRASS.build(state, holder, Color(0.48, 0.56, 0.82)))
	var cards: Array = state.get("lagoon_grass_groups", []) as Array
	check("eighteen", cards.size() == 18)
	var seen: Array[Dictionary] = []
	for i: int in range(cards.size()):
		seen.append({})
	for sample: int in range(60):
		GRASS.tick(state, 0.05, false)
		for i: int in range(cards.size()):
			var card: Sprite2D = cards[i] as Sprite2D
			seen[i][card.frame] = true
			check("root_%d_%d" % [i, sample], (card.position + GRASS.ROOT * card.scale).is_equal_approx(GRASS.GROUPS[i]["root"] as Vector2))
	for i: int in range(cards.size()):
		check("all_four_%d" % i, seen[i].size() == 4)
	var timer: float = state["lagoon_grass_group_t"]
	var frame: int = (cards[0] as Sprite2D).frame
	GRASS.tick(state, 0.1, true)
	check("pause_freezes", timer == float(state["lagoon_grass_group_t"]) and frame == (cards[0] as Sprite2D).frame)
	for toggle: String in ["lagoon_environment_motion_enabled", "lagoon_plants_motion_enabled"]:
		state[toggle] = false
		GRASS.tick(state, 0.1, false)
		var static_ok: bool = true
		for value: Variant in cards:
			static_ok = static_ok and (value as Sprite2D).frame == 0
		check("static_" + toggle, static_ok and timer == float(state["lagoon_grass_group_t"]))
		state[toggle] = true
	check("rebuild_without_duplicates", GRASS.build(state, holder, Color.WHITE) and holder.get_child_count() == 18)
	GRASS.clear(state)
	check("rollback_removes_all", holder.get_child_count() == 0 and not state.has("lagoon_grass_groups"))
	holder.free()
	quit(0 if failures == 0 else 1)
