extends SceneTree
const BANKS := preload("res://scripts/arena/sky_lagoon_cloud_banks.gd")
var failed: int = 0
func check(label: String, good: bool) -> void:
	print("BANKS|", label, "|", "PASS" if good else "FAIL")
	if not good:
		failed += 1
func _initialize() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var state: Dictionary = {}
	check("missing_resource_adds_nothing", not BANKS.build(state, holder, Color.WHITE, "res://absent/") and holder.get_child_count() == 0)
	check("build", BANKS.build(state, holder, Color(0.48, 0.56, 0.82)))
	var cards: Array = state.get("lagoon_cloud_bank_cards", []) as Array
	check("eight_cards", cards.size() == 8)
	var seen: Array[Dictionary] = []
	for i: int in range(cards.size()):
		seen.append({})
	var shared: bool = true
	var homes_fixed: bool = true
	for sample: int in range(481):
		BANKS.tick(state, 0.05, false)
		var phases: Dictionary = {}
		for i: int in range(cards.size()):
			var card: Sprite2D = cards[i] as Sprite2D
			var row: Dictionary = BANKS.CARDS[i]
			var cycle: float = float(row["cycle"])
			var regions: Array = row["regions"] as Array
			var rect: Rect2 = card.region_rect
			var frame_index: int = -1
			for k: int in range(4):
				var expected: Array = regions[k] as Array
				if rect == Rect2(float(expected[0]), float(expected[1]), float(expected[2]), float(expected[3])):
					frame_index = k
			seen[i][frame_index] = true
			if phases.has(cycle):
				shared = shared and phases[cycle] == frame_index
			phases[cycle] = frame_index
			var position: Array = row["position"] as Array
			homes_fixed = homes_fixed and card.position == Vector2(float(position[0]), float(position[1]))
	check("shared_bank_clock_every_sample", shared)
	check("fixed_card_geometry_every_sample", homes_fixed)
	for i: int in range(cards.size()):
		check("four_valid_regions_%d" % i, seen[i].size() == 4 and not seen[i].has(-1))
	var timer: float = float(state["lagoon_cloud_bank_t"])
	var prior: Rect2 = (cards[0] as Sprite2D).region_rect
	BANKS.tick(state, 0.1, true)
	check("pause", float(state["lagoon_cloud_bank_t"]) == timer and (cards[0] as Sprite2D).region_rect == prior)
	state["lagoon_environment_motion_enabled"] = false
	BANKS.tick(state, 0.1, false)
	var hidden: bool = true
	for value: Variant in cards:
		hidden = hidden and not (value as Sprite2D).visible
	check("static_background_restored", hidden and float(state["lagoon_cloud_bank_t"]) == timer)
	state["lagoon_environment_motion_enabled"] = true
	BANKS.tick(state, 0.1, false)
	check("resume", (cards[0] as Sprite2D).visible)
	check("rebuild_without_duplicates", BANKS.build(state, holder, Color.WHITE) and holder.get_child_count() == 8)
	BANKS.clear(state)
	check("clear", holder.get_child_count() == 0 and not state.has("lagoon_cloud_bank_cards"))
	holder.free()
	quit(0 if failed == 0 else 1)
