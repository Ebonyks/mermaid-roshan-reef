extends SceneTree
const Cels := preload("res://scripts/arena/sky_lagoon_bough_cels.gd")
var failures: int = 0

func check(label: String, okay: bool) -> void:
	print("BOUGHCELS|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var tile := Sprite2D.new()
	tile.name = "SkyLagoonBackdrop_r0_c0"
	var original: Texture2D = load("res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_v5_tile_r0_c0.png") as Texture2D
	tile.texture = original
	holder.add_child(tile)
	var state: Dictionary = {"saved_progress": 7}
	check("original_unchanged", not Cels.build(state, holder, "original") and tile.texture == original and holder.get_child_count() == 1)
	check("build_replaces_painted_copy", Cels.build(state, holder, "animated_v1") and tile.texture != original)
	var card: Sprite2D = state.get("lagoon_bough_card") as Sprite2D
	var seen: Dictionary = {}
	var geometry_ok: bool = true
	for step: int in range(2400):
		Cels.tick(state, 0.016, false)
		seen[card.frame] = true
		geometry_ok = geometry_ok and card.position == Vector2(0, 448) and card.get_rect().size == Vector2(512, 256) and card.rotation == 0.0 and card.scale == Vector2.ONE
	check("three_cels_never_unused_fourth", seen.size() == 3 and not seen.has(3))
	check("2400_ticks_fixed_source_geometry", geometry_ok)
	var clock_before: float = float(state["lagoon_bough_t"])
	var frame_before: int = card.frame
	for step: int in range(600):
		Cels.tick(state, 50.0, true)
	check("pause_freezes_pose_and_clock", float(state["lagoon_bough_t"]) == clock_before and card.frame == frame_before)
	for control: String in ["lagoon_environment_motion_enabled", "lagoon_plants_motion_enabled"]:
		state[control] = false
		Cels.tick(state, 50.0, false)
		check("static_rest_" + control, card.frame == 0 and float(state["lagoon_bough_t"]) == clock_before)
		state[control] = true
	var rebuilds_ok: bool = true
	for cycle: int in range(40):
		tile.modulate = Color(0.48, 0.56, 0.82) if cycle % 2 == 0 else Color.WHITE
		Cels.build(state, holder, "animated_v1")
		card = state["lagoon_bough_card"] as Sprite2D
		rebuilds_ok = rebuilds_ok and holder.get_child_count() == 2 and card.modulate == tile.modulate and state["lagoon_bough_original"] == original
	check("40_rebuilds_preserve_rollback_and_night_tint", rebuilds_ok)
	Cels.build(state, holder, "original")
	check("rollback_restores_original_texture_and_removes_card", tile.texture == original and holder.get_child_count() == 1 and not state.has("lagoon_bough_card"))
	Cels.build(state, holder, "animated_v1")
	holder.free()
	Cels.tick(state, 1.0, false)
	Cels.clear(state)
	Cels.clear(state)
	check("freed_parent_idempotent_cleanup", not state.has("lagoon_bough_original") and not state.has("lagoon_bough_tile"))
	check("no_progress_mutation", state["saved_progress"] == 7)
	print("BOUGHCELS|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
