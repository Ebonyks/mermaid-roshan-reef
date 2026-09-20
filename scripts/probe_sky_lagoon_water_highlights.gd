extends SceneTree
const Highlights := preload("res://scripts/arena/sky_lagoon_water_highlights.gd")
var failures: int = 0
func check(label: String, okay: bool) -> void:
	print("SKYSHIMMER|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var state: Dictionary = {}
	check("original_unchanged", not Highlights.build(state, holder, "original", false) and holder.get_child_count() == 0)
	check("two_pools_build", Highlights.build(state, holder, "animated_v1", false) and holder.get_child_count() == 2)
	var sampled: Dictionary = {}
	var anchored: bool = true
	for index: int in range(2400):
		Highlights.tick(state, 0.016, false)
		for child: Node in holder.get_children():
			var card: Sprite2D = child as Sprite2D
			var rect: Rect2 = card.get_meta("master_rect") as Rect2
			sampled[card.frame] = true
			anchored = anchored and card.position == rect.get_center() and (card.get_rect().size * card.scale).is_equal_approx(rect.size)
	check("twelve_cels_no_padding", sampled.size() == 12 and not sampled.has(12))
	check("geography_fixed", anchored)
	var before: float = float(state["lagoon_water_highlight_t"])
	Highlights.tick(state, 99.0, true)
	check("pause_freezes", float(state["lagoon_water_highlight_t"]) == before)
	state["lagoon_water_motion_enabled"] = false
	Highlights.tick(state, 0.016, false)
	check("static_exact_plate", not (holder.get_child(0) as Sprite2D).visible and not (holder.get_child(1) as Sprite2D).visible)
	var rebuild_ok: bool = true
	for index: int in range(40):
		Highlights.build(state, holder, "animated_v1", index % 2 == 0)
		rebuild_ok = rebuild_ok and holder.get_child_count() == 2
		for child: Node in holder.get_children():
			var card: Sprite2D = child as Sprite2D
			rebuild_ok = rebuild_ok and (card.modulate != Color.WHITE if index % 2 == 0 else card.modulate == Color.WHITE)
	check("night_and_rebuild", rebuild_ok)
	Highlights.build(state, holder, "original", false)
	check("rollback", holder.get_child_count() == 0)
	Highlights.build(state, holder, "animated_v1", false)
	holder.free()
	Highlights.tick(state, 0.016, false)
	Highlights.clear(state)
	check("freed_parent", not state.has("lagoon_water_highlights"))
	print("SKYSHIMMER|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
