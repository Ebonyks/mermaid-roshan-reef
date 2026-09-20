extends SceneTree
const Cels := preload("res://scripts/arena/sky_lagoon_environment_cels.gd")
var failures: int = 0
func check(label: String, okay: bool) -> void:
	print("SKYCELS|%s|%s" % [label, "OK" if okay else "FAIL"])
	if not okay:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var holder := Node2D.new()
	root.add_child(holder)
	var state: Dictionary = {"progress_sentinel": {"earned": 7}}
	check("original_has_no_candidate_nodes", not Cels.build(state, holder, "original") and holder.get_child_count() == 0)
	check("candidate_build", Cels.build(state, holder, "animated_v1"))
	check("three_stages_have_intentional_ground_cover", holder.get_child_count() == 12)
	var seen: Dictionary = {}
	var stable: bool = true
	for index: int in range(1200):
		Cels.tick(state, 0.016, false)
		for value: Variant in state["lagoon_environment_cels"] as Array:
			var card: Sprite2D = value as Sprite2D
			seen[card.frame] = true
			var actual: Vector2 = card.position + (Cels.ROOT_IN_CELL - Cels.CELL_SIZE * 0.5) * card.scale
			stable = stable and actual.is_equal_approx(card.get_meta("root_anchor") as Vector2)
			stable = stable and card.get_rect().size == Vector2(320, 320)
	check("all_four_atlas_cells_sampled", seen.size() == 4)
	check("all_roots_fixed_for_1200_ticks", stable)
	var before: float = float(state["lagoon_environment_cel_t"])
	for index: int in range(600):
		Cels.tick(state, 10.0, true)
	check("pause_does_not_accumulate_time", float(state["lagoon_environment_cel_t"]) == before)
	state["lagoon_environment_motion_enabled"] = false
	Cels.tick(state, 10.0, false)
	var rest: bool = true
	for value: Variant in state["lagoon_environment_cels"] as Array:
		rest = rest and (value as Sprite2D).frame == 0
	check("static_control_restores_rest_cels", rest)
	var rebuilds: bool = true
	for index: int in range(40):
		Cels.build(state, holder, "animated_v1", index % 2 == 0)
		rebuilds = rebuilds and holder.get_child_count() == 12
		for child: Node in holder.get_children():
			var sprite: Sprite2D = child as Sprite2D
			rebuilds = rebuilds and (sprite.modulate != Color.WHITE if index % 2 == 0 else sprite.modulate == Color.WHITE)
	check("rebuild_has_no_duplicate_nodes", rebuilds)
	check("ambient_does_not_change_progress", int((state["progress_sentinel"] as Dictionary)["earned"]) == 7)
	Cels.build(state, holder, "original")
	check("rollback_removes_all_candidate_nodes", holder.get_child_count() == 0 and not state.has("lagoon_environment_cels"))
	_check_bridge(holder, state)
	Cels.build(state, holder, "animated_v1")
	holder.free()
	Cels.tick(state, 0.016, false)
	Cels.clear(state)
	check("cleanup_handles_freed_parent", not state.has("lagoon_environment_cels"))
	print("SKYCELS|RESULT|%s" % ("ALL OK" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)

func _check_bridge(holder: Node2D, state: Dictionary) -> void:
	var castle := Sprite2D.new()
	castle.texture = load("res://assets/sprites/sky_lagoon/sky_lagoon_castle_four_tower_v4.png") as Texture2D
	holder.add_child(castle)
	var original: Texture2D = castle.texture
	check("bridge_original_unmodified", not Cels.build_bridge(state, castle, "original") and castle.texture == original)
	check("bridge_candidate_build", Cels.build_bridge(state, castle, "animated_v1"))
	var patch: Sprite2D = state.get("lagoon_bridge_patch") as Sprite2D
	var chains: Sprite2D = state.get("lagoon_bridge_chains") as Sprite2D
	check("bridge_chain_cell_geometry", chains != null and chains.get_rect().size == Vector2(224, 192) and chains.position == Vector2(8, -19))
	var chain_sync: bool = true
	check("bridge_atlas_cell_geometry", patch != null and patch.get_rect().size == Vector2(256, 192) and patch.hframes == 4 and patch.vframes == 3)
	state["lagoon_environment_motion_enabled"] = true
	state["lagoon_bridge_motion_enabled"] = true
	var on_deck := Vector2(240, 940) - Vector2(511, 512)
	var away := Vector2(10, 10) - Vector2(511, 512)
	for index: int in range(2400):
		Cels.tick_bridge(state, 0.016, on_deck, false, false)
	check("bridge_idle_never_triggers", int(state.get("lagoon_bridge_play_count", -1)) == 0)
	Cels.tick_bridge(state, 0.016, away, true, false)
	check("bridge_off_deck_motion_never_triggers", int(state.get("lagoon_bridge_play_count", -1)) == 0)
	state["lagoon_environment_motion_enabled"] = true
	Cels.tick_bridge(state, 0.016, on_deck, true, false)
	check("bridge_entry_triggers_once", int(state.get("lagoon_bridge_play_count", -1)) == 1)
	var before: float = float(state.get("lagoon_bridge_t", -1.0))
	for index: int in range(600):
		Cels.tick_bridge(state, 10.0, on_deck, true, true)
	check("bridge_pause_does_not_accumulate", float(state.get("lagoon_bridge_t", -1.0)) == before)
	var sampled: Dictionary = {}
	for index: int in range(180):
		Cels.tick_bridge(state, 0.008, on_deck, true, false)
		sampled[patch.frame] = true
		chain_sync = chain_sync and chains.frame == patch.frame
	check("bridge_samples_all_twelve_cels", sampled.size() == 12)
	check("bridge_chain_contact_sync", chain_sync)
	check("bridge_contact_does_not_queue", int(state.get("lagoon_bridge_play_count", -1)) == 1 and patch.frame == 0 and float(state.get("lagoon_bridge_t", 0.0)) < 0.0)
	Cels.tick_bridge(state, 0.016, away, true, false)
	Cels.tick_bridge(state, 0.016, on_deck, true, false)
	check("bridge_reentry_rearms", int(state.get("lagoon_bridge_play_count", -1)) == 2)
	state["lagoon_bridge_motion_enabled"] = false
	Cels.tick_bridge(state, 0.016, on_deck, true, false)
	check("bridge_static_rest", patch.frame == 0 and chains.frame == 0 and float(state.get("lagoon_bridge_t", 0.0)) < 0.0)
	Cels.clear_bridge(state)
	check("bridge_rollback_restores_original", castle.texture == original and castle.get_child_count() == 0 and not state.has("lagoon_bridge_patch"))
	castle.free()
