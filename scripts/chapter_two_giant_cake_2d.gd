class_name ChapterTwoGiantCake2D
extends Control

## Persistent, code-native 2D cake for the Chapter 2 party table.
##
## Chef supplies the baked cake, tiers, and frosting; Farmer supplies the
## visible strawberries; Candy Maker turns those strawberries into glossy
## candied decorations. The state is plain data so the director and probes
## can carry the exact same details between rooms and after a load.

const ACT_CHEF := 0
const ACT_CANDY_MAKER := 3
const ACT_FARMER := 6
const STATE_VERSION := 1
const STRAWBERRY_REQUIRED_MASK := 0x1F
const CAKE_PIECE_REQUIRED_MASK := 0x7F
const CAKE_BOTTOM_BIT := 1 << 0
const CAKE_MIDDLE_BIT := 1 << 1
const CAKE_TOP_BIT := 1 << 2
const CAKE_STACKED_BIT := 1 << 3
const CAKE_FROSTED_BIT := 1 << 4
const CAKE_CANDIED_BERRIES_BIT := 1 << 5
const CAKE_PLACED_BIT := 1 << 6
const CAKE_CHEF_LEGACY_MASK := 0x1F
const RAINBOW_TIER_COLOURS: Array[Color] = [
	Color("#ef667d"), Color("#f39a52"), Color("#f5c95b"),
	Color("#62c995"), Color("#5bbbe1"), Color("#9d74dd"),
]
const RAINBOW_TIER_NAMES: Array[String] = [
	"red", "orange", "yellow", "green", "blue", "violet",
]
const FINAL_CAKE_TEXTURE := \
	"res://assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png"
const STRAWBERRY_CLUSTER_TEXTURE := \
	"res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png"

var festive: bool = false
var strawberry_mask: int = 0
var cake_piece_mask: int = 0
var cake_baked: bool = false
var bottom_built: bool = false
var middle_built: bool = false
var top_built: bool = false
var tiers_stacked: bool = false
var tiers_built: bool = false
var frosting_applied: bool = false
var farmer_strawberries_visible: bool = false
var prepared_glossy_berries: bool = false
var candied_strawberries_glossy: bool = false
var cake_placed_final: bool = false
var final_cake_sprite: Sprite2D = null
var ingredient_cluster_sprite: Sprite2D = null


func setup() -> void:
	name = "ChapterTwoGiantBirthdayCake"
	size = Vector2(360.0, 220.0)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_meta("plot_prop", "gigantic_birthday_cake")
	set_meta("made_by", "chef_roshan")
	set_meta("true_2d_code_native", true)
	set_meta("persistent_state_version", STATE_VERSION)
	set_meta("cake_remains_after_candle_taken", true)
	_build_approved_art_nodes()
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


## Apply the saved Opera contribution mask. This is the normal runtime seam
## for the director and is also convenient for headless probes.
func apply_party_piece_mask(piece_mask: int) -> void:
	set_state(state_from_party_piece_mask(piece_mask))


## Compatibility alias for callers that describe the same state as a party
## state rather than a piece mask.
func set_party_piece_mask(piece_mask: int) -> void:
	apply_party_piece_mask(piece_mask)


## Apply the ordered scene milestones. Strawberry pickups and cake pieces are
## separate save masks, so a quit between any two touches keeps the exact
## physical assembly visible on the next Main Hall visit.
func apply_cake_piece_mask(piece_mask: int,
		new_strawberry_mask: int = 0) -> void:
	set_state(state_from_milestone_masks(new_strawberry_mask, piece_mask))


func set_cake_piece_mask(piece_mask: int,
		new_strawberry_mask: int = 0) -> void:
	apply_cake_piece_mask(piece_mask, new_strawberry_mask)


func apply_milestone_masks(new_strawberry_mask: int,
		new_cake_piece_mask: int) -> void:
	set_state(state_from_milestone_masks(new_strawberry_mask,
		new_cake_piece_mask))


func set_milestone_masks(new_strawberry_mask: int,
		new_cake_piece_mask: int) -> void:
	apply_milestone_masks(new_strawberry_mask, new_cake_piece_mask)


## Build a render-ready state from the two persistent Chapter 2 milestone
## masks. Invalid skipped bits are trimmed to the contiguous physical prefix.
static func state_from_milestone_masks(new_strawberry_mask: int,
		new_cake_piece_mask: int) -> Dictionary:
	var safe_strawberry_mask := new_strawberry_mask & STRAWBERRY_REQUIRED_MASK
	var safe_piece_mask := _ordered_piece_prefix(new_cake_piece_mask)
	var strawberries_ready := safe_strawberry_mask == STRAWBERRY_REQUIRED_MASK
	var candied := (safe_piece_mask & CAKE_CANDIED_BERRIES_BIT) != 0 \
		and strawberries_ready
	var placed := (safe_piece_mask & CAKE_PLACED_BIT) != 0 \
		and safe_piece_mask == CAKE_PIECE_REQUIRED_MASK \
		and strawberries_ready
	return {
		"state_version": STATE_VERSION,
		"strawberry_mask": safe_strawberry_mask,
		"cake_piece_mask": safe_piece_mask,
		"strawberries_required_mask": STRAWBERRY_REQUIRED_MASK,
		"cake_piece_required_mask": CAKE_PIECE_REQUIRED_MASK,
		"strawberries_ready": strawberries_ready,
		"mix_batter": (safe_piece_mask & CAKE_BOTTOM_BIT) != 0,
		"stir_batter": (safe_piece_mask & CAKE_MIDDLE_BIT) != 0,
		"bake_six_rainbow_tiers": (safe_piece_mask & CAKE_TOP_BIT) != 0,
		"stack_six_rainbow_tiers": (safe_piece_mask & CAKE_STACKED_BIT) != 0,
		"frost_six_rainbow_tiers": (safe_piece_mask & CAKE_FROSTED_BIT) != 0,
		"cake_baked": (safe_piece_mask & CAKE_TOP_BIT) != 0,
		"bottom_built": (safe_piece_mask & CAKE_BOTTOM_BIT) != 0,
		"middle_built": (safe_piece_mask & CAKE_MIDDLE_BIT) != 0,
		"top_built": (safe_piece_mask & CAKE_TOP_BIT) != 0,
		"tiers_stacked": (safe_piece_mask & CAKE_STACKED_BIT) != 0,
		"tiers_built": (safe_piece_mask & CAKE_STACKED_BIT) != 0,
		"frosting_applied": (safe_piece_mask & CAKE_FROSTED_BIT) != 0,
		"farmer_strawberries_visible": safe_strawberry_mask != 0,
		"prepared_glossy_berries": candied,
		"candied_strawberries_glossy": candied,
		"cake_placed_final": placed,
		"chef_created": (safe_piece_mask & CAKE_FROSTED_BIT) != 0,
		"farmer_ingredient_state": safe_strawberry_mask != 0,
		"candy_maker_final_decorating": candied,
		"cake_remains_after_candle_taken": true,
	}


## Return a deterministic cake state for the persistent party bit mask.
static func state_from_party_piece_mask(piece_mask: int) -> Dictionary:
	var chef_done := (piece_mask & (1 << ACT_CHEF)) != 0
	var farmer_done := (piece_mask & (1 << ACT_FARMER)) != 0
	var candy_done := (piece_mask & (1 << ACT_CANDY_MAKER)) != 0
	var legacy_piece_mask := 0
	if chef_done:
		legacy_piece_mask = CAKE_BOTTOM_BIT | CAKE_MIDDLE_BIT | CAKE_TOP_BIT \
			| CAKE_STACKED_BIT | CAKE_FROSTED_BIT
	if candy_done:
		legacy_piece_mask = CAKE_PIECE_REQUIRED_MASK
	return state_from_milestone_masks(
		STRAWBERRY_REQUIRED_MASK if farmer_done else 0, legacy_piece_mask)


## Set the complete accumulated state supplied by the director or a probe.
func set_state(state: Dictionary) -> void:
	if state.has("cake_piece_mask") or state.has("strawberry_mask"):
		var milestone_state := state_from_milestone_masks(
			int(state.get("strawberry_mask", 0)),
			int(state.get("cake_piece_mask", 0)))
		_apply_milestone_state(milestone_state)
		_sync_metadata()
		_sync_approved_sprite_visibility()
		queue_redraw()
		return
	cake_baked = _state_bool(state, "cake_baked",
		_state_bool(state, "baked", _state_bool(state, "cake_ready", false)))
	tiers_built = _state_bool(state, "tiers_built",
		_state_bool(state, "tiers", _state_bool(state, "tiers_ready", false)))
	frosting_applied = _state_bool(state, "frosting_applied",
		_state_bool(state, "frosting", _state_bool(state, "frosting_ready", false)))
	bottom_built = cake_baked
	middle_built = tiers_built
	top_built = tiers_built
	tiers_stacked = tiers_built
	farmer_strawberries_visible = _state_bool(state,
		"farmer_strawberries_visible", _state_bool(state,
			"farmer_strawberries", _state_bool(state, "strawberry_ingredient_state", false)))
	candied_strawberries_glossy = _state_bool(state,
		"candied_strawberries_glossy", _state_bool(state,
			"candied_strawberries", _state_bool(state, "glossy_candied_strawberries", false)))
	prepared_glossy_berries = candied_strawberries_glossy
	strawberry_mask = STRAWBERRY_REQUIRED_MASK if farmer_strawberries_visible else 0
	cake_piece_mask = CAKE_PIECE_REQUIRED_MASK if candied_strawberries_glossy \
		else (CAKE_CHEF_LEGACY_MASK if cake_baked else 0)
	cake_placed_final = cake_piece_mask == CAKE_PIECE_REQUIRED_MASK \
		and strawberry_mask == STRAWBERRY_REQUIRED_MASK \
		and candied_strawberries_glossy
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func _apply_milestone_state(state: Dictionary) -> void:
	strawberry_mask = int(state.get("strawberry_mask", 0)) & STRAWBERRY_REQUIRED_MASK
	cake_piece_mask = _ordered_piece_prefix(
		int(state.get("cake_piece_mask", 0)))
	cake_baked = (cake_piece_mask & CAKE_TOP_BIT) != 0
	bottom_built = (cake_piece_mask & CAKE_BOTTOM_BIT) != 0
	middle_built = (cake_piece_mask & CAKE_MIDDLE_BIT) != 0
	top_built = (cake_piece_mask & CAKE_TOP_BIT) != 0
	tiers_stacked = (cake_piece_mask & CAKE_STACKED_BIT) != 0
	tiers_built = tiers_stacked
	frosting_applied = (cake_piece_mask & CAKE_FROSTED_BIT) != 0
	farmer_strawberries_visible = strawberry_mask != 0
	prepared_glossy_berries = (cake_piece_mask & CAKE_CANDIED_BERRIES_BIT) != 0 \
		and strawberry_mask == STRAWBERRY_REQUIRED_MASK
	candied_strawberries_glossy = prepared_glossy_berries
	cake_placed_final = (cake_piece_mask & CAKE_PLACED_BIT) != 0 \
		and cake_piece_mask == CAKE_PIECE_REQUIRED_MASK \
		and candied_strawberries_glossy


## Explicit API for each authored contribution. Calls are cumulative, which
## protects already-built details when a later beat only adds garnish.
func add_chef_cake_state() -> void:
	cake_piece_mask |= CAKE_CHEF_LEGACY_MASK
	cake_baked = true
	bottom_built = true
	middle_built = true
	top_built = true
	tiers_stacked = true
	tiers_built = true
	frosting_applied = true
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func add_chef_baked_base() -> void:
	cake_piece_mask |= CAKE_BOTTOM_BIT | CAKE_MIDDLE_BIT | CAKE_TOP_BIT
	cake_baked = true
	bottom_built = true
	middle_built = true
	top_built = true
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func add_chef_tier() -> void:
	cake_piece_mask |= CAKE_BOTTOM_BIT | CAKE_MIDDLE_BIT | CAKE_TOP_BIT \
		| CAKE_STACKED_BIT
	cake_baked = true
	bottom_built = true
	middle_built = true
	top_built = true
	tiers_stacked = true
	tiers_built = true
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func add_chef_frosting() -> void:
	cake_piece_mask |= CAKE_CHEF_LEGACY_MASK
	cake_baked = true
	bottom_built = true
	middle_built = true
	top_built = true
	tiers_stacked = true
	tiers_built = true
	frosting_applied = true
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func add_farmer_strawberries() -> void:
	strawberry_mask = STRAWBERRY_REQUIRED_MASK
	farmer_strawberries_visible = true
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func add_candy_maker_decoration() -> void:
	cake_piece_mask |= CAKE_CANDIED_BERRIES_BIT
	prepared_glossy_berries = true
	candied_strawberries_glossy = true
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


func set_chef_state() -> void:
	add_chef_cake_state()


func set_farmer_state() -> void:
	add_farmer_strawberries()


func set_candy_maker_state() -> void:
	add_candy_maker_decoration()


func place_final_cake() -> void:
	cake_piece_mask |= CAKE_PLACED_BIT
	cake_placed_final = cake_piece_mask == CAKE_PIECE_REQUIRED_MASK \
		and strawberry_mask == STRAWBERRY_REQUIRED_MASK
	_sync_metadata()
	_sync_approved_sprite_visibility()
	queue_redraw()


## Full state export used when moving the visual from preparation into the
## later Main Hall party. It intentionally has no candle fields: the candle
## belongs to the table and may disappear without changing this dictionary.
func persistent_state() -> Dictionary:
	return {
		"state_version": STATE_VERSION,
		"strawberry_mask": strawberry_mask,
		"cake_piece_mask": cake_piece_mask,
		"strawberries_required_mask": STRAWBERRY_REQUIRED_MASK,
		"cake_piece_required_mask": CAKE_PIECE_REQUIRED_MASK,
		"bottom_built": bottom_built,
		"middle_built": middle_built,
		"top_built": top_built,
		"tiers_stacked": tiers_stacked,
		"cake_baked": cake_baked,
		"cake_ready": cake_baked,
		"mix_batter": (cake_piece_mask & CAKE_BOTTOM_BIT) != 0,
		"stir_batter": (cake_piece_mask & CAKE_MIDDLE_BIT) != 0,
		"bake_six_rainbow_tiers": (cake_piece_mask & CAKE_TOP_BIT) != 0,
		"stack_six_rainbow_tiers": (cake_piece_mask & CAKE_STACKED_BIT) != 0,
		"frost_six_rainbow_tiers": (cake_piece_mask & CAKE_FROSTED_BIT) != 0,
		"tiers_built": tiers_built,
		"tiers_ready": tiers_built,
		"frosting_applied": frosting_applied,
		"frosting_ready": frosting_applied,
		"farmer_strawberries_visible": farmer_strawberries_visible,
		"strawberry_ingredient_state": farmer_strawberries_visible,
		"candied_strawberries_glossy": candied_strawberries_glossy,
		"prepared_glossy_berries": candied_strawberries_glossy,
		"cake_placed_final": cake_placed_final,
		"glossy_candied_strawberries": candied_strawberries_glossy,
		"chef_created": cake_baked,
		"farmer_ingredient_state": farmer_strawberries_visible,
		"candy_maker_final_decorating": candied_strawberries_glossy,
		"cake_remains_after_candle_taken": true,
	}


func get_persistent_state() -> Dictionary:
	return persistent_state()


func has_visual_progress() -> bool:
	return cake_piece_mask != 0 or strawberry_mask != 0


func stage_id() -> String:
	if cake_placed_final:
		return "placed_final"
	if prepared_glossy_berries:
		return "candied_strawberries_preplacement"
	if frosting_applied:
		return "chef_frosting"
	if tiers_stacked:
		return "tiers_stacked"
	if top_built:
		return "chef_top_tier"
	if middle_built:
		return "chef_middle_tier"
	if bottom_built:
		return "chef_bottom_tier"
	if strawberry_mask != 0:
		return "farmer_strawberry_ingredients"
	return "none"


func visual_phase_id() -> String:
	if cake_placed_final:
		return "placed_final"
	if prepared_glossy_berries:
		return "candied_strawberries_preplacement"
	if frosting_applied:
		return "frost_six_rainbow_tiers"
	if tiers_stacked:
		return "stack_six_rainbow_tiers"
	if top_built:
		return "bake_six_rainbow_tiers"
	if middle_built:
		return "stir_batter"
	if bottom_built:
		return "mix_batter"
	if strawberry_mask != 0:
		return "farmer_strawberry_ingredients"
	return "none"


func set_festive(is_festive: bool) -> void:
	festive = is_festive
	set_meta("party_started", festive)
	queue_redraw()


func _draw() -> void:
	var ink := Color("#402b58")
	if not has_visual_progress():
		return
	_draw_ellipse_shape(Vector2(180.0, 207.0), Vector2(166.0, 11.0),
		Color(0.14, 0.08, 0.24, 0.24))
	# The approved complete cake is a single Sprite2D only for the final
	# decorating state. It contains no candle or flame, which remains a sibling
	# table layer owned by ChapterTwoPartyTable2D.
	if cake_placed_final and final_cake_sprite != null:
		return

	# Chef's first two milestones are batter actions, before any cake tier
	# exists. Keeping this silhouette separate prevents a visual jump from a
	# differently-coloured placeholder cake into the six-tier final asset.
	if not cake_baked:
		if farmer_strawberries_visible:
			_draw_ingredient_tray(ink)
		_draw_batter_bowl(ink, middle_built)
		return
	if not top_built:
		_draw_batter_bowl(ink, middle_built)
		return

	if top_built and not tiers_stacked:
		_draw_loose_rainbow_tiers(ink)
	else:
		_draw_six_tier_stack(ink, frosting_applied)

	# Candy Maker's glossy berry prep stays visible on the six-tier cake before
	# the placement bit is earned. The final Sprite2D takes over only at 0x7F.
	if prepared_glossy_berries:
		for fruit_index in range(5):
			var fruit_x := 116.0 + float(fruit_index) * 32.0
			_draw_strawberry(Vector2(fruit_x, 27.0), true, ink)

	if festive:
		for sparkle: Vector2 in [
			Vector2(35.0, 105.0), Vector2(327.0, 108.0),
			Vector2(82.0, 47.0), Vector2(280.0, 40.0),
		]:
			draw_line(sparkle - Vector2(8.0, 0.0),
				sparkle + Vector2(8.0, 0.0), Color("#fff4a8"), 4.0)
			draw_line(sparkle - Vector2(0.0, 8.0),
				sparkle + Vector2(0.0, 8.0), Color("#fff4a8"), 4.0)


func _draw_batter_bowl(ink: Color, stirred: bool) -> void:
	_draw_rounded_layer(Rect2(76.0, 112.0, 208.0, 65.0), 24.0,
		Color("#f4ca72"), ink, 5.0)
	_draw_ellipse_shape(Vector2(180.0, 118.0), Vector2(92.0, 18.0),
		Color("#fff1cf"))
	_draw_ellipse_shape(Vector2(180.0, 121.0), Vector2(78.0, 13.0),
		Color("#e7a95d"))
	if stirred:
		draw_arc(Vector2(180.0, 121.0), 38.0, 0.3, 5.5, 24,
			Color("#fff4a8"), 5.0, true)
		draw_line(Vector2(218.0, 116.0), Vector2(256.0, 72.0), ink, 7.0)
		draw_circle(Vector2(257.0, 70.0), 9.0, Color("#f5c95b"))


func _draw_loose_rainbow_tiers(ink: Color) -> void:
	# Six prepared tiers are deliberately offset like a little baker's tray;
	# they already have the same red-to-violet palette as the final cake.
	for tier_index in range(6):
		var tier_width := 106.0 + float(tier_index) * 12.0
		var tier_x := (360.0 - tier_width) * 0.5 \
			+ float((tier_index % 2) * 7 - 3)
		var tier_y := 34.0 + float(tier_index) * 27.0
		_draw_rounded_layer(Rect2(tier_x, tier_y, tier_width, 22.0), 9.0,
			RAINBOW_TIER_COLOURS[tier_index], ink, 3.0)


func _draw_six_tier_stack(ink: Color, frosted: bool) -> void:
	# Top-to-bottom order is fixed and matches the accepted final artwork:
	# red, orange, yellow, green, blue, violet.
	for tier_index in range(6):
		var tier_width := 146.0 + float(tier_index) * 34.0
		var tier_x := (360.0 - tier_width) * 0.5
		var tier_y := 28.0 + float(tier_index) * 29.0
		var tier_rect := Rect2(tier_x, tier_y, tier_width, 28.0)
		_draw_rounded_layer(tier_rect, 10.0,
			RAINBOW_TIER_COLOURS[tier_index], ink, 4.0)
		if frosted:
			_draw_icing(Rect2(tier_x + 4.0, tier_y + 1.0,
				tier_width - 8.0, 11.0), ink)


func _draw_ingredient_tray(ink: Color) -> void:
	_draw_rounded_layer(Rect2(48.0, 144.0, 264.0, 48.0), 18.0,
		Color("#f8d783"), ink, 4.0)
	if farmer_strawberries_visible and ingredient_cluster_sprite == null:
		for fruit_index in range(4):
			_draw_strawberry(Vector2(116.0 + float(fruit_index) * 38.0,
				141.0), candied_strawberries_glossy, ink)
	if candied_strawberries_glossy:
		for sparkle_index in range(3):
			var sparkle := Vector2(139.0 + float(sparkle_index) * 42.0, 169.0)
			draw_circle(sparkle, 4.0, Color("#fff4a8"))


func _draw_icing(rect: Rect2, ink: Color) -> void:
	_draw_rounded_layer(rect, 10.0, Color("#fff1cf"), ink, 3.0)
	for drip: Vector2 in [
		Vector2(rect.position.x + 34.0, rect.position.y + rect.size.y - 2.0),
		Vector2(rect.position.x + rect.size.x * 0.32, rect.position.y + rect.size.y - 1.0),
		Vector2(rect.position.x + rect.size.x * 0.68, rect.position.y + rect.size.y),
		Vector2(rect.end.x - 36.0, rect.position.y + rect.size.y - 3.0),
	]:
		draw_circle(drip, 8.0, ink)
		draw_circle(drip, 5.0, Color("#fff1cf"))


func _draw_strawberry(center: Vector2, glossy: bool, ink: Color) -> void:
	var fruit := PackedVector2Array([
		center + Vector2(-12.0, -2.0), center + Vector2(12.0, -2.0),
		center + Vector2(0.0, 20.0),
	])
	draw_colored_polygon(fruit, ink)
	var inner := PackedVector2Array([
		center + Vector2(-8.0, 0.0), center + Vector2(8.0, 0.0),
		center + Vector2(0.0, 15.0),
	])
	draw_colored_polygon(inner, Color("#ef667d"))
	draw_colored_polygon(PackedVector2Array([
		center + Vector2(-10.0, -3.0), center + Vector2(0.0, 2.0),
		center + Vector2(10.0, -3.0), center + Vector2(4.0, -10.0),
		center + Vector2(-4.0, -10.0),
	]), Color("#62c995"))
	for seed_index in range(3):
		var seed_position := center + Vector2(-5.0 + float(seed_index) * 5.0,
			6.0 + float(seed_index % 2) * 5.0)
		draw_circle(seed_position, 1.7, Color("#fff1cf"))
	if glossy:
		draw_circle(center + Vector2(-4.0, 3.0), 3.0, Color("#fff9dc"))
		draw_circle(center + Vector2(3.0, 9.0), 2.0, Color("#ffcae0"))


func _sync_metadata() -> void:
	set_meta("cake_state", persistent_state())
	set_meta("cake_stage", stage_id())
	set_meta("cake_visual_phase", visual_phase_id())
	set_meta("rainbow_tier_order", RAINBOW_TIER_NAMES.duplicate())
	set_meta("strawberry_mask", strawberry_mask)
	set_meta("strawberry_required_mask", STRAWBERRY_REQUIRED_MASK)
	set_meta("strawberries_ready", strawberry_mask == STRAWBERRY_REQUIRED_MASK)
	set_meta("cake_piece_mask", cake_piece_mask)
	set_meta("cake_piece_required_mask", CAKE_PIECE_REQUIRED_MASK)
	set_meta("mix_batter", bottom_built and not cake_baked)
	set_meta("stir_batter", middle_built and not cake_baked)
	set_meta("bake_six_rainbow_tiers", top_built)
	set_meta("stack_six_rainbow_tiers", tiers_stacked)
	set_meta("frost_six_rainbow_tiers", frosting_applied)
	set_meta("cake_final_prerequisites_met",
		cake_piece_mask == CAKE_PIECE_REQUIRED_MASK
		and strawberry_mask == STRAWBERRY_REQUIRED_MASK)
	set_meta("cake_baked", cake_baked)
	set_meta("cake_ready", cake_baked)
	set_meta("tiers_built", tiers_built)
	set_meta("tiers_ready", tiers_built)
	set_meta("frosting_applied", frosting_applied)
	set_meta("frosting_ready", frosting_applied)
	set_meta("farmer_strawberries_visible", farmer_strawberries_visible)
	set_meta("strawberry_ingredient_state", farmer_strawberries_visible)
	set_meta("candied_strawberries_glossy", candied_strawberries_glossy)
	set_meta("prepared_glossy_berries", prepared_glossy_berries)
	set_meta("cake_placed_final", cake_placed_final)
	set_meta("final_cake_ready", cake_placed_final)
	set_meta("final_cake_sprite_visible",
		final_cake_sprite != null and final_cake_sprite.visible)
	set_meta("glossy_candied_strawberries", candied_strawberries_glossy)
	set_meta("chef_created", cake_baked)
	set_meta("farmer_ingredient_state", farmer_strawberries_visible)
	set_meta("candy_maker_final_decorating", candied_strawberries_glossy)
	set_meta("cake_remains_after_candle_taken", true)
	set_meta("true_2d_stateful_assembly", true)
	set_meta("approved_final_cake_texture", FINAL_CAKE_TEXTURE)
	set_meta("approved_strawberry_ingredient_texture", STRAWBERRY_CLUSTER_TEXTURE)
	set_meta("final_cake_is_sprite2d", final_cake_sprite != null)
	set_meta("ingredient_cluster_is_sprite2d", ingredient_cluster_sprite != null)


func _build_approved_art_nodes() -> void:
	if ResourceLoader.exists(FINAL_CAKE_TEXTURE):
		final_cake_sprite = Sprite2D.new()
		final_cake_sprite.name = "ApprovedGrandCandiedStrawberryCake"
		final_cake_sprite.texture = load(FINAL_CAKE_TEXTURE) as Texture2D
		final_cake_sprite.position = Vector2(180.0, 84.0)
		final_cake_sprite.scale = Vector2.ONE * 0.30
		final_cake_sprite.z_index = 4
		final_cake_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		final_cake_sprite.set_meta("approved_asset_reuse", true)
		final_cake_sprite.set_meta("cake_delivery_stage", "candy_maker_final_decorating")
		final_cake_sprite.set_meta("contains_candle", false)
		add_child(final_cake_sprite)
	if ResourceLoader.exists(STRAWBERRY_CLUSTER_TEXTURE):
		ingredient_cluster_sprite = Sprite2D.new()
		ingredient_cluster_sprite.name = "ApprovedFarmerStrawberryIngredients"
		ingredient_cluster_sprite.texture = load(STRAWBERRY_CLUSTER_TEXTURE) as Texture2D
		ingredient_cluster_sprite.position = Vector2(180.0, 137.0)
		ingredient_cluster_sprite.scale = Vector2.ONE * 0.115
		ingredient_cluster_sprite.z_index = 4
		ingredient_cluster_sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		ingredient_cluster_sprite.set_meta("approved_asset_reuse", true)
		ingredient_cluster_sprite.set_meta("ingredient_source", "farmer_roshan")
		add_child(ingredient_cluster_sprite)


func _sync_approved_sprite_visibility() -> void:
	if final_cake_sprite != null:
		final_cake_sprite.visible = cake_placed_final
	if ingredient_cluster_sprite != null:
		ingredient_cluster_sprite.visible = farmer_strawberries_visible \
		and not cake_baked


func _state_bool(state: Dictionary, key: String, fallback: bool) -> bool:
	var value: Variant = state.get(key, fallback)
	return bool(value)


static func _ordered_piece_prefix(raw_mask: int) -> int:
	var prefix := 0
	var safe_mask := raw_mask & CAKE_PIECE_REQUIRED_MASK
	for piece_index in range(7):
		var bit := 1 << piece_index
		if (safe_mask & bit) == 0:
			break
		prefix |= bit
	return prefix


func _draw_rounded_layer(rect: Rect2, radius: float, fill: Color,
		outline: Color, outline_width: float = 5.0) -> void:
	_fill_rounded_rect(rect, radius, outline)
	var inset := Rect2(rect.position + Vector2.ONE * outline_width,
		rect.size - Vector2.ONE * outline_width * 2.0)
	_fill_rounded_rect(inset, maxf(2.0, radius - outline_width), fill)


func _fill_rounded_rect(rect: Rect2, radius: float, colour: Color) -> void:
	var safe_radius := minf(radius, minf(rect.size.x, rect.size.y) * 0.5)
	draw_rect(Rect2(rect.position + Vector2(safe_radius, 0.0),
		Vector2(rect.size.x - safe_radius * 2.0, rect.size.y)), colour, true)
	draw_rect(Rect2(rect.position + Vector2(0.0, safe_radius),
		Vector2(rect.size.x, rect.size.y - safe_radius * 2.0)), colour, true)
	for centre: Vector2 in [
		rect.position + Vector2(safe_radius, safe_radius),
		rect.position + Vector2(rect.size.x - safe_radius, safe_radius),
		rect.position + Vector2(safe_radius, rect.size.y - safe_radius),
		rect.position + Vector2(
			rect.size.x - safe_radius, rect.size.y - safe_radius),
	]:
		draw_circle(centre, safe_radius, colour)


func _draw_ellipse_shape(centre: Vector2, radii: Vector2,
		colour: Color) -> void:
	var points := PackedVector2Array()
	for index in range(32):
		var angle := TAU * float(index) / 32.0
		points.append(centre + Vector2(
			cos(angle) * radii.x, sin(angle) * radii.y))
	draw_colored_polygon(points, colour)
