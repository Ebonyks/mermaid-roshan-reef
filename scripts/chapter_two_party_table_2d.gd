class_name ChapterTwoPartyTable2D
extends Control

## Picture-only Main Hall summary of Chapter 2's party preparation.
##
## The thirteen approved Opera goal props become a persistent visual answer to
## "what have we made?". No button lives here: plot activation stays with the
## director-owned ChapterTwoRoomPlot surface.

const TABLE_TEXTURE := \
	"res://assets/flats/castle/dream_house/dining_table.png"
const BANNER_TEXTURE := \
	"res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png"
const PROP_ROOT := "res://assets/opera/worlds/props/"
const PROP_FILES := {
	0: "goal_chef.png",
	1: "goal_detective.png",
	2: "goal_ballerina.png",
	3: "goal_candymaker.png",
	5: "goal_doctor.png",
	6: "goal_farmer.png",
	7: "goal_boxer.png",
	8: "goal_magician.png",
	10: "goal_painter.png",
	11: "goal_astronaut.png",
	12: "goal_racer.png",
	13: "goal_popstar.png",
	15: "goal_nursery.png",
}
const SLOT_SIZE := Vector2(76.0, 76.0)
const SLOT_GAP := 10.0
const TOP_ROW_COUNT := 7
const ACT_CHEF := ChapterTwoGiantCake2D.ACT_CHEF
const CHAPTER2_LEGACY_SUMMARY_ACTS := [
	ChapterTwoDirector.ACT_CHEF,
	ChapterTwoDirector.ACT_DETECTIVE,
	ChapterTwoDirector.ACT_CANDY_MAKER,
	ChapterTwoDirector.ACT_FARMER,
]
const CHAPTER2_RETAINED_SUMMARY_POSITIONS := {
	ChapterTwoDirector.ACT_BALLERINA: Vector2(54.0, 410.0),
	ChapterTwoDirector.ACT_PAINTER: Vector2(54.0, 502.0),
	ChapterTwoDirector.ACT_POP_STAR: Vector2(1150.0, 410.0),
	ChapterTwoDirector.ACT_ASTRONAUT: Vector2(1150.0, 502.0),
}

var m: ReefMain
var prop_nodes: Dictionary = {}
var table_glow: Panel
var giant_cake: ChapterTwoGiantCake2D
var party_candle: ChapterTwoRainbowCandle2D
var lighting_rocket: TextureRect
var ember_scout_actor: Node2D
var ember_king_actor: Node2D
var ember_son_actor: Node2D
var ember_carried_candle: ChapterTwoRainbowCandle2D
var north_star_clue: Node2D
var scout_arriving := false
var king_take_in_motion := false
var king_departing := false
var scout_tween: Tween
var king_tween: Tween
var persistent_cake_state: Dictionary = {}


func setup(main: ReefMain) -> void:
	m = main
	name = "ChapterTwoPartyTable2D"
	position = Vector2.ZERO
	size = StorybookUI.CANVAS_SIZE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 1
	set_meta("true_2d_party_table", true)
	set_meta("picture_only_nonreader_progress", true)
	set_meta("chapter2_legacy_summary_art_suppressed", [
		"corn", "candy_bag", "crown", "tiara", "clue_chest"])
	set_meta("chapter2_single_cake_authority", "giant_cake")
	_build_banner()
	_build_table()
	_build_slots()
	_build_story_centerpieces()
	# Visitors now belong to the Sky Lagoon lawn; no identity placeholders here.
	refresh()


func refresh() -> void:
	if m == null:
		return
	var mask := m.chapter2_party_piece_mask & ChapterTwoPartyPlan.ALL_PARTY_MASK
	var earned_count := _party_mask_count(mask)
	for act_value: Variant in prop_nodes:
		var act_index := int(act_value)
		var earned := (mask & (1 << act_index)) != 0
		var prop := prop_nodes[act_value] as TextureRect
		if prop == null:
			continue
		prop.modulate = Color.WHITE if earned \
			else Color(0.28, 0.22, 0.38, 0.16)
		prop.scale = Vector2.ONE if earned else Vector2.ONE * 0.88
		prop.set_meta("party_piece_earned", earned)
		prop.set_meta("taken_by_ember_king", false)
	var ready := mask == ChapterTwoPartyPlan.ALL_PARTY_MASK
	if table_glow != null:
		table_glow.add_theme_stylebox_override("panel", StorybookUI.panel_style(
			Color(1.0, 0.83, 0.34, 0.26) if ready \
			else Color(0.45, 0.28, 0.58, 0.10),
			Color(1.0, 0.94, 0.62, 0.96) if ready \
			else Color(0.78, 0.68, 0.92, 0.72), 42, 5))
	var cake_state := _cake_state_from_main(mask)
	if not persistent_cake_state.is_empty():
		cake_state = _merge_cake_state(cake_state, persistent_cake_state)
	var chef_ready := (mask & (1 << ACT_CHEF)) != 0
	var candle_ready := (mask & (1 << ChapterTwoDirector.ACT_DETECTIVE)) != 0
	var rocket_ready := (mask & (1 << 11)) != 0
	var cake_final_ready := bool(cake_state.get("cake_placed_final", false))
	if giant_cake != null:
		giant_cake.set_state(cake_state)
		giant_cake.visible = giant_cake.has_visual_progress()
		giant_cake.set_festive(m.chapter2_party_started)
	if party_candle != null:
		party_candle.visible = candle_ready and not m.chapter2_candle_taken
		# Detective finds the candle only after the decorated cake is complete.
		# Keep the candle a separate sibling layer and mount it on the top tier
		# only when Candy Maker's placement milestone is physically present.
		party_candle.position = Vector2(
			591.0, 60.0 if cake_final_ready else 208.0)
		party_candle.set_lit(m.chapter2_candle_lit)
		party_candle.set_meta("taken_by_ember_king", m.chapter2_candle_taken)
		party_candle.set_meta("mounted_on_completed_cake", cake_final_ready)
	if lighting_rocket != null:
		lighting_rocket.visible = rocket_ready
		lighting_rocket.set_meta("rocket_ready", rocket_ready)
	if ember_scout_actor != null and not scout_arriving:
		ember_scout_actor.visible = m.chapter2_ember_scout_seen \
			and not m.chapter2_ember_king_crashed
	if ember_king_actor != null and not king_take_in_motion \
			and not king_departing:
		ember_king_actor.visible = false
	if north_star_clue != null:
		north_star_clue.visible = m.chapter2_ember_king_crashed
	if ember_son_actor != null:
		ember_son_actor.visible = m.chapter2_ember_son_seen
	set_meta("party_piece_mask", mask)
	set_meta("earned_party_piece_count", earned_count)
	set_meta("party_ready", ready)
	set_meta("gigantic_cake_ready", chef_ready)
	set_meta("cake_state", giant_cake.persistent_state() if giant_cake != null else cake_state)
	set_meta("cake_stage", giant_cake.stage_id() if giant_cake != null else "none")
	set_meta("cake_visual_phase", giant_cake.visual_phase_id()
		if giant_cake != null else "none")
	set_meta("strawberry_mask", int(cake_state.get("strawberry_mask", 0)))
	set_meta("cake_piece_mask", int(cake_state.get("cake_piece_mask", 0)))
	set_meta("cake_piece_required_mask",
		int(cake_state.get("cake_piece_required_mask", 0x7F)))
	set_meta("strawberries_ready", bool(cake_state.get(
		"strawberries_ready", false)))
	set_meta("cake_final_prerequisites_met", bool(cake_state.get(
		"cake_placed_final", false)))
	set_meta("cake_remains_after_candle_taken", true)
	set_meta("farmer_strawberries_visible", bool(cake_state.get(
		"farmer_strawberries_visible", false)))
	set_meta("candied_strawberries_glossy", bool(cake_state.get(
		"candied_strawberries_glossy", false)))
	set_meta("prepared_glossy_berries", bool(cake_state.get(
		"prepared_glossy_berries", false)))
	set_meta("cake_placed_final", bool(cake_state.get(
		"cake_placed_final", false)))
	set_meta("final_cake_ready", bool(cake_state.get(
		"cake_placed_final", false)))
	set_meta("candle_lighting_rocket_ready", rocket_ready)
	set_meta("rainbow_candle_lit", m.chapter2_candle_lit)
	set_meta("rainbow_candle_taken", m.chapter2_candle_taken)
	set_meta("ember_scout_visibly_staged",
		ember_scout_actor != null and ember_scout_actor.visible)
	set_meta("ember_king_visibly_staged",
		ember_king_actor != null and ember_king_actor.visible)
	set_meta("ember_visitors_use_identity_placeholder", true)
	set_meta("ember_son_runtime_art_approved", false)
	set_meta("ember_son_visually_depicted",
		ember_son_actor != null and ember_son_actor.visible)
	set_meta("ember_son_identity_acceptance_open", true)
	set_meta("next_arc_clue_visible",
		north_star_clue != null and north_star_clue.visible)
	set_meta("chapter2_single_strawberry_token_count", 5)
	set_meta("chapter2_no_legacy_corn_bag_crown", true)
	var cake_rect := Rect2()
	if giant_cake != null:
		cake_rect = Rect2(giant_cake.position, giant_cake.size)
	var summary_rects: Array[Rect2] = []
	var summary_icons_avoid_cake := true
	for prop_value: Variant in prop_nodes.values():
		var summary_prop := prop_value as TextureRect
		if summary_prop == null:
			continue
		var summary_rect := Rect2(summary_prop.position,
			summary_prop.size * summary_prop.scale)
		summary_rects.append(summary_rect)
		summary_icons_avoid_cake = summary_icons_avoid_cake \
			and not summary_rect.intersects(cake_rect)
	set_meta("chapter2_retained_summary_icon_rects", summary_rects)
	set_meta("chapter2_summary_icons_avoid_cake", summary_icons_avoid_cake)


func _party_mask_count(mask: int) -> int:
	var count := 0
	for bit_index in range(16):
		if (mask & (1 << bit_index)) != 0:
			count += 1
	return count


func play_scout_arrival() -> void:
	if ember_scout_actor == null:
		return
	if scout_tween != null and scout_tween.is_valid():
		scout_tween.kill()
	scout_arriving = true
	ember_scout_actor.visible = true
	ember_scout_actor.position = Vector2(1335.0, 244.0)
	ember_scout_actor.scale = Vector2.ONE * 0.72
	set_meta("party_visual_beat", "ember_scout_arriving")
	scout_tween = ember_scout_actor.create_tween()
	scout_tween.set_parallel(true)
	scout_tween.tween_property(ember_scout_actor, "position",
		Vector2(1080.0, 244.0), 0.78).set_trans(Tween.TRANS_BACK) \
		.set_ease(Tween.EASE_OUT)
	scout_tween.tween_property(ember_scout_actor, "scale",
		Vector2.ONE, 0.78).set_trans(Tween.TRANS_BACK) \
		.set_ease(Tween.EASE_OUT)
	scout_tween.chain().tween_callback(func() -> void:
		scout_arriving = false
		set_meta("party_visual_beat", "ember_scout_watching"))


func play_king_entrance() -> void:
	if ember_king_actor == null or party_candle == null \
			or not party_candle.visible or not m.chapter2_candle_lit:
		return
	if king_tween != null and king_tween.is_valid():
		king_tween.kill()
	king_take_in_motion = true
	ember_king_actor.visible = true
	ember_king_actor.position = Vector2(1390.0, 126.0)
	if ember_carried_candle != null:
		ember_carried_candle.visible = false
	set_meta("party_visual_beat", "ember_king_entering_for_lit_candle")
	set_meta("king_target_is_lit_candle_only", true)
	king_tween = ember_king_actor.create_tween()
	king_tween.tween_property(ember_king_actor, "position",
		Vector2(732.0, 126.0), 1.25).set_trans(Tween.TRANS_QUAD) \
		.set_ease(Tween.EASE_OUT)


func complete_king_take() -> void:
	if ember_king_actor == null:
		return
	if king_tween != null and king_tween.is_valid():
		king_tween.kill()
	king_take_in_motion = false
	king_departing = true
	ember_king_actor.visible = true
	if ember_carried_candle != null:
		ember_carried_candle.visible = true
		ember_carried_candle.set_lit(true)
	refresh()
	if ember_son_actor != null:
		ember_son_actor.visible = true
		ember_son_actor.position = Vector2(1265.0, 270.0)
		var son_arrival := ember_son_actor.create_tween()
		son_arrival.tween_property(ember_son_actor, "position",
			Vector2(1110.0, 270.0), 0.72).set_trans(Tween.TRANS_BACK) \
			.set_ease(Tween.EASE_OUT)
	set_meta("party_visual_beat", "ember_king_carrying_glowing_candle")
	set_meta("cake_remains_after_candle_taken", giant_cake != null \
		and giant_cake.visible)
	king_tween = ember_king_actor.create_tween()
	king_tween.set_parallel(true)
	king_tween.tween_property(ember_king_actor, "position",
		Vector2(1390.0, 88.0), 1.35).set_trans(Tween.TRANS_QUAD) \
		.set_ease(Tween.EASE_IN)
	king_tween.tween_property(ember_king_actor, "scale",
		Vector2.ONE * 0.82, 1.35)
	king_tween.chain().tween_callback(func() -> void:
		king_departing = false
		ember_king_actor.visible = false
		set_meta("party_visual_beat", "north_star_next_arc_clue"))


func prop_for_act(act_index: int) -> TextureRect:
	return prop_nodes.get(act_index) as TextureRect


## Director/probe seam for carrying the assembled cake between preparation and
## the later Main Hall party. The table remains the visual owner; no candle
## value is accepted here, so Ember King's crash can only affect the candle.
func set_persistent_cake_state(state: Dictionary) -> void:
	persistent_cake_state = state.duplicate(true)
	if giant_cake != null:
		giant_cake.set_state(persistent_cake_state)
		giant_cake.visible = giant_cake.has_visual_progress()
	set_meta("cake_state", persistent_cake_state.duplicate(true))
	set_meta("cake_state_injected", true)
	queue_redraw()


func set_cake_state(state: Dictionary) -> void:
	set_persistent_cake_state(state)


func apply_milestone_masks(new_strawberry_mask: int,
		new_cake_piece_mask: int) -> void:
	set_persistent_cake_state(ChapterTwoGiantCake2D.state_from_milestone_masks(
		new_strawberry_mask, new_cake_piece_mask))


func get_persistent_cake_state() -> Dictionary:
	if giant_cake != null:
		return giant_cake.persistent_state()
	return persistent_cake_state.duplicate(true)


func clear_persistent_cake_state_override() -> void:
	persistent_cake_state.clear()
	refresh()


func _merge_cake_state(derived: Dictionary, explicit: Dictionary) -> Dictionary:
	var merged := derived.duplicate(true)
	for key: Variant in explicit:
		merged[key] = explicit[key]
	return merged


func _cake_state_from_main(legacy_party_mask: int) -> Dictionary:
	# New milestone masks are authoritative whenever ReefMain exposes them.
	# Object.get keeps this visual compatible with an older scene owner while
	# avoiding a fallback to career bits when a present mask is legitimately 0.
	var raw_strawberry_mask: Variant = m.get("chapter2_strawberry_mask")
	var raw_cake_piece_mask: Variant = m.get("chapter2_cake_piece_mask")
	if raw_strawberry_mask != null or raw_cake_piece_mask != null:
		return ChapterTwoGiantCake2D.state_from_milestone_masks(
			int(raw_strawberry_mask) if raw_strawberry_mask != null else 0,
			int(raw_cake_piece_mask) if raw_cake_piece_mask != null else 0)
	return ChapterTwoGiantCake2D.state_from_party_piece_mask(legacy_party_mask)


func _build_banner() -> void:
	if not ResourceLoader.exists(BANNER_TEXTURE):
		return
	var banner := TextureRect.new()
	banner.name = "BirthdayRainbowBanner"
	banner.position = Vector2(442.0, 30.0)
	banner.size = Vector2(396.0, 118.0)
	banner.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	banner.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	banner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	banner.texture = load(BANNER_TEXTURE) as Texture2D
	banner.modulate = Color(1.0, 1.0, 1.0, 0.94)
	banner.set_meta("approved_banner_reuse", true)
	add_child(banner)


func _build_table() -> void:
	table_glow = Panel.new()
	table_glow.name = "PartyTableGlow"
	table_glow.position = Vector2(285.0, 352.0)
	table_glow.size = Vector2(710.0, 238.0)
	table_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(table_glow)
	if not ResourceLoader.exists(TABLE_TEXTURE):
		return
	var table := TextureRect.new()
	table.name = "ApprovedFamilyTable"
	table.position = Vector2(330.0, 388.0)
	table.size = Vector2(620.0, 206.0)
	table.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	table.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	table.mouse_filter = Control.MOUSE_FILTER_IGNORE
	table.texture = load(TABLE_TEXTURE) as Texture2D
	table.set_meta("approved_table_reuse", true)
	add_child(table)


func _build_slots() -> void:
	var act_indices := ChapterTwoPartyPlan.all_act_indices()
	var retained_act_indices: Array[int] = []
	for act_value: Variant in act_indices:
		var candidate_act := int(act_value)
		if not CHAPTER2_LEGACY_SUMMARY_ACTS.has(candidate_act):
			retained_act_indices.append(candidate_act)
	for slot_index in range(retained_act_indices.size()):
		var act_index: int = retained_act_indices[slot_index]
		var file_name := String(PROP_FILES.get(act_index, ""))
		var path := PROP_ROOT + file_name
		if file_name == "" or not ResourceLoader.exists(path):
			continue
		var prop := TextureRect.new()
		prop.name = "PartyPiece_%02d" % act_index
		prop.position = CHAPTER2_RETAINED_SUMMARY_POSITIONS.get(
			act_index, Vector2(54.0, 410.0)) as Vector2
		prop.size = SLOT_SIZE
		prop.pivot_offset = SLOT_SIZE * 0.5
		prop.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		prop.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		prop.mouse_filter = Control.MOUSE_FILTER_IGNORE
		prop.texture = load(path) as Texture2D
		prop.set_meta("act_index", act_index)
		prop.set_meta("party_piece_id", String(
			ChapterTwoPartyPlan.entry_for_act(act_index).get("piece", "")))
		add_child(prop)
		prop_nodes[act_index] = prop


func _build_story_centerpieces() -> void:
	giant_cake = ChapterTwoGiantCake2D.new()
	giant_cake.setup()
	giant_cake.position = Vector2(460.0, 168.0)
	giant_cake.z_index = 2
	add_child(giant_cake)

	party_candle = ChapterTwoRainbowCandle2D.new()
	party_candle.setup(false)
	party_candle.position = Vector2(591.0, 60.0)
	party_candle.scale = Vector2.ONE * 0.65
	party_candle.z_index = 3
	party_candle.set_meta("party_ignition_source", "astronaut_party_rocket")
	add_child(party_candle)

	var rocket_path := PROP_ROOT + String(PROP_FILES[11])
	if not ResourceLoader.exists(rocket_path):
		return
	lighting_rocket = TextureRect.new()
	lighting_rocket.name = "CandleLightingRocket"
	lighting_rocket.position = Vector2(815.0, 235.0)
	lighting_rocket.size = Vector2(112.0, 112.0)
	lighting_rocket.pivot_offset = lighting_rocket.size * 0.5
	lighting_rocket.rotation = -0.28
	lighting_rocket.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	lighting_rocket.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	lighting_rocket.mouse_filter = Control.MOUSE_FILTER_IGNORE
	lighting_rocket.texture = load(rocket_path) as Texture2D
	lighting_rocket.z_index = 3
	lighting_rocket.set_meta("plot_prop", "candle_lighting_rocket")
	lighting_rocket.set_meta("built_by", "astronaut_roshan")
	add_child(lighting_rocket)


func _build_ember_visitor_stage() -> void:
	# No approved transparent 2D Ember character cutouts exist yet. These
	# deliberately non-identifying silhouettes make the physical party action
	# readable without importing retired 3D renders or promoting concept art.
	ember_scout_actor = Node2D.new()
	ember_scout_actor.name = "EmberScoutIdentityPlaceholder"
	ember_scout_actor.z_index = 8
	ember_scout_actor.visible = false
	ember_scout_actor.set_meta("runtime_role", "ember_scout_silhouette")
	ember_scout_actor.set_meta("identity_art_approved", false)
	_add_polygon(ember_scout_actor, "ScoutOuterFlame", PackedVector2Array([
		Vector2(0.0, 76.0), Vector2(-42.0, 34.0), Vector2(-24.0, -14.0),
		Vector2(-6.0, 2.0), Vector2(4.0, -58.0), Vector2(25.0, -12.0),
		Vector2(46.0, 28.0),
	]), Color(1.0, 0.47, 0.12, 0.96))
	_add_polygon(ember_scout_actor, "ScoutSafeSilhouette", PackedVector2Array([
		Vector2(0.0, 63.0), Vector2(-29.0, 29.0), Vector2(-16.0, -1.0),
		Vector2(-2.0, 10.0), Vector2(5.0, -34.0), Vector2(19.0, 0.0),
		Vector2(32.0, 27.0),
	]), Color(0.22, 0.12, 0.30, 1.0))
	_add_eye(ember_scout_actor, Vector2(-12.0, 20.0))
	_add_eye(ember_scout_actor, Vector2(10.0, 20.0))
	add_child(ember_scout_actor)

	ember_king_actor = Node2D.new()
	ember_king_actor.name = "EmberKingIdentityPlaceholder"
	ember_king_actor.z_index = 9
	ember_king_actor.visible = false
	ember_king_actor.set_meta("runtime_role", "ember_king_silhouette")
	ember_king_actor.set_meta("identity_art_approved", false)
	_add_polygon(ember_king_actor, "KingCapeGlow", PackedVector2Array([
		Vector2(-76.0, 162.0), Vector2(-58.0, 28.0), Vector2(-33.0, 4.0),
		Vector2(35.0, 4.0), Vector2(66.0, 36.0), Vector2(88.0, 162.0),
	]), Color(1.0, 0.42, 0.10, 0.96))
	_add_polygon(ember_king_actor, "KingCapeSilhouette", PackedVector2Array([
		Vector2(-63.0, 151.0), Vector2(-48.0, 39.0), Vector2(-27.0, 17.0),
		Vector2(29.0, 17.0), Vector2(53.0, 45.0), Vector2(73.0, 151.0),
	]), Color(0.19, 0.08, 0.25, 1.0))
	_add_polygon(ember_king_actor, "KingHead", _circle_points(
		Vector2(0.0, 0.0), 36.0, 18), Color(0.24, 0.10, 0.30, 1.0))
	_add_polygon(ember_king_actor, "KingCrownGlow", PackedVector2Array([
		Vector2(-38.0, -23.0), Vector2(-31.0, -61.0), Vector2(-9.0, -39.0),
		Vector2(2.0, -70.0), Vector2(17.0, -39.0), Vector2(38.0, -61.0),
		Vector2(36.0, -20.0),
	]), Color(1.0, 0.66, 0.12, 1.0))
	var taking_arm := Line2D.new()
	taking_arm.name = "CandleTakingArm"
	taking_arm.points = PackedVector2Array([
		Vector2(-32.0, 49.0), Vector2(-73.0, 7.0), Vector2(-111.0, -30.0)])
	taking_arm.width = 18.0
	taking_arm.default_color = Color(0.22, 0.09, 0.28, 1.0)
	taking_arm.begin_cap_mode = Line2D.LINE_CAP_ROUND
	taking_arm.end_cap_mode = Line2D.LINE_CAP_ROUND
	ember_king_actor.add_child(taking_arm)
	ember_carried_candle = ChapterTwoRainbowCandle2D.new()
	ember_carried_candle.setup(true)
	ember_carried_candle.position = Vector2(-139.0, -93.0)
	ember_carried_candle.scale = Vector2.ONE * 0.52
	ember_carried_candle.visible = false
	ember_carried_candle.set_meta("carried_by", "ember_king_silhouette")
	ember_carried_candle.set_meta("same_party_candle", true)
	ember_king_actor.add_child(ember_carried_candle)
	add_child(ember_king_actor)

	ember_son_actor = Node2D.new()
	ember_son_actor.name = "EmberPrinceIdentityPlaceholder"
	ember_son_actor.z_index = 8
	ember_son_actor.visible = false
	ember_son_actor.set_meta("runtime_role", "ember_prince_child_silhouette")
	ember_son_actor.set_meta("relationship", "ember_king_son")
	ember_son_actor.set_meta("identity_art_approved", false)
	_add_polygon(ember_son_actor, "PrinceGlow", PackedVector2Array([
		Vector2(0.0, 92.0), Vector2(-47.0, 48.0), Vector2(-30.0, 2.0),
		Vector2(-10.0, 17.0), Vector2(1.0, -48.0), Vector2(23.0, 2.0),
		Vector2(49.0, 45.0),
	]), Color(1.0, 0.55, 0.14, 0.98))
	_add_polygon(ember_son_actor, "PrinceChildSilhouette", PackedVector2Array([
		Vector2(0.0, 78.0), Vector2(-33.0, 43.0), Vector2(-20.0, 12.0),
		Vector2(-6.0, 24.0), Vector2(2.0, -27.0), Vector2(16.0, 11.0),
		Vector2(34.0, 40.0),
	]), Color(0.31, 0.13, 0.39, 1.0))
	_add_polygon(ember_son_actor, "PrinceSmallCrown", PackedVector2Array([
		Vector2(-23.0, -13.0), Vector2(-18.0, -39.0), Vector2(-5.0, -25.0),
		Vector2(2.0, -46.0), Vector2(12.0, -24.0), Vector2(23.0, -37.0),
		Vector2(21.0, -10.0),
	]), Color(1.0, 0.87, 0.28, 1.0))
	_add_eye(ember_son_actor, Vector2(-9.0, 25.0))
	_add_eye(ember_son_actor, Vector2(9.0, 25.0))
	add_child(ember_son_actor)

	north_star_clue = Node2D.new()
	north_star_clue.name = "NorthStarNextArcClue"
	north_star_clue.position = Vector2(1080.0, 98.0)
	north_star_clue.z_index = 8
	north_star_clue.visible = false
	north_star_clue.set_meta("next_arc_direction", "north")
	north_star_clue.set_meta("son_identity_not_depicted", true)
	_add_polygon(north_star_clue, "NorthArrowGlow", PackedVector2Array([
		Vector2(-22.0, 72.0), Vector2(-22.0, -9.0), Vector2(-52.0, -9.0),
		Vector2(0.0, -70.0), Vector2(52.0, -9.0), Vector2(22.0, -9.0),
		Vector2(22.0, 72.0),
	]), Color(1.0, 0.90, 0.34, 0.94))
	_add_polygon(north_star_clue, "NorthArrowCore", PackedVector2Array([
		Vector2(-11.0, 60.0), Vector2(-11.0, -18.0), Vector2(-29.0, -18.0),
		Vector2(0.0, -52.0), Vector2(29.0, -18.0), Vector2(11.0, -18.0),
		Vector2(11.0, 60.0),
	]), Color(0.44, 0.24, 0.66, 1.0))
	add_child(north_star_clue)


func _add_polygon(parent: Node2D, node_name: String,
		points: PackedVector2Array, color: Color) -> void:
	var polygon := Polygon2D.new()
	polygon.name = node_name
	polygon.polygon = points
	polygon.color = color
	parent.add_child(polygon)


func _add_eye(parent: Node2D, eye_position: Vector2) -> void:
	_add_polygon(parent, "FriendlyEye", _circle_points(
		eye_position, 5.5, 12), Color(1.0, 0.96, 0.72, 1.0))


func _circle_points(center: Vector2, radius: float,
		point_count: int) -> PackedVector2Array:
	var points := PackedVector2Array()
	for point_index in range(point_count):
		var angle := TAU * float(point_index) / float(point_count)
		points.append(center + Vector2(cos(angle), sin(angle)) * radius)
	return points
