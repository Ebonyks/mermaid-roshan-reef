class_name CastleCleanup
extends RefCounted
# Day 1 "Cleaning Day" — the Sparkle Scrub layer.
#
# Runtime home of the Codex dirty-castle 2D pack
# (assets/castle/dirty_cleanup_2d/, 96 sprites). Every skin here is an
# unshaded Sprite3D overlay on an EXISTING castle fixture: no room geometry,
# no collider, no OmniLight and no gameplay node is created or moved. The
# object->GLB binding follows audit/dirty_castle_2d_2026-07-22/
# scene_resemblance_ledger.json, per DIRTY_CASTLE_2D_GODOT_HANDOFF_2026-07-23.
#
# Design constants (CLAUDE.md / STORY_DAYS.md §Day 1): non-reader, one finger,
# no timer, no fail state, no lost progress. A target is cleaned by rubbing:
# swim close, then tap OR wiggle the stick. Three rubs and it dissolves. The
# state saves the instant a target finishes, never only at room end. Nothing
# completes without the child's own input — helpers never finish a target.
#
# Phase 7 satellite: ALL state lives on main (m.g / m.save_data); this class
# owns logic only and receives `main` by reference.

const SKIN := "res://assets/castle/dirty_cleanup_2d/"
const RUBS_PER_TARGET := 3
# generous by design: the established castle touch zones are 3.5..8 world
# units and a 4-year-old aims with a whole hand, not a cursor
const REACH := 6.0
const RUB_COOL := 0.22          # min seconds between accepted rubs
const WIGGLE_MIN := 0.45        # stick deflection that counts as a rub stroke
const VIGNETTE_SECONDS := 3.2   # room intro card, then it dissolves

# ---------------------------------------------------------------------------
# Room table. Positions are LOCAL to the castle origin (m.CASTLE_POS), the
# same `o` convention every CastleHall builder uses. `mode`:
#   prop    - billboard skin standing on/next to a fixture
#   flat    - floor/counter mark, laid onto the receiving surface
#   fixture - non-billboard overlay facing the room's normal camera direction,
#             for skins that include the fixture itself (sink, stove, tub,
#             mirror, loo). Fades away to reveal the real 3D fixture beneath.
# `h` is the visible world height the sprite is fitted to.
# ---------------------------------------------------------------------------
const ROOMS: Array[Dictionary] = [
	{
		"id": "playroom",
		"who": "Princess Huluu",
		"intro": "The playroom got all jumbly! Let us put the toys away together!",
		"done": "Look at this tidy playroom! Every toy is home!",
		"vignette": "targets/room_vignettes/room_vignette_playroom.png",
		"vignette_pos": Vector3(44.0, 40.0, 2.0),
		"tool": "tools/tool_sorting_basket.png",
		"targets": [
			{"id": "playroom_puzzle_tiles", "tex": "rooms/playroom/playroom_puzzle_tiles.png",
				"pos": Vector3(44.0, 34.15, 4.5), "h": 3.6, "mode": "flat"},
			{"id": "playroom_wheeled_shell_toy", "tex": "rooms/playroom/playroom_wheeled_shell_toy.png",
				"pos": Vector3(41.0, 35.1, -11.0), "h": 3.4, "mode": "prop"},
			{"id": "playroom_stacking_rings", "tex": "rooms/playroom/playroom_stacking_rings.png",
				"pos": Vector3(40.0, 35.1, -1.5), "h": 3.2, "mode": "prop"},
			{"id": "playroom_shell_tea_set", "tex": "rooms/playroom/playroom_shell_tea_set.png",
				"pos": Vector3(47.2, 35.0, 5.0), "h": 3.0, "mode": "prop"},
			{"id": "playroom_dressup_pile", "tex": "rooms/playroom/playroom_dressup_pile.png",
				"pos": Vector3(46.8, 35.0, 9.8), "h": 3.2, "mode": "prop"},
			{"id": "playroom_balls_beanbag", "tex": "rooms/playroom/playroom_balls_beanbag.png",
				"pos": Vector3(41.2, 35.0, 11.8), "h": 3.2, "mode": "prop"},
		],
	},
	{
		"id": "library",
		"who": "Princess Huluu",
		"intro": "The story books tumbled down! Can you tuck them back in?",
		"done": "Every story is back on its shelf. Thank you!",
		"vignette": "targets/room_vignettes/room_vignette_library.png",
		"vignette_pos": Vector3(-44.0, 40.0, 2.0),
		"tool": "tools/tool_ribbon_duster.png",
		"targets": [
			{"id": "library_fallen_books", "tex": "rooms/library/library_fallen_books.png",
				"pos": Vector3(-45.8, 34.15, -1.5), "h": 3.4, "mode": "flat"},
			{"id": "library_picture_cards", "tex": "rooms/library/library_picture_cards.png",
				"pos": Vector3(-42.6, 34.15, 5.5), "h": 3.0, "mode": "flat"},
			{"id": "library_bookmark_ribbons", "tex": "rooms/library/library_bookmark_ribbons.png",
				"pos": Vector3(-49.6, 35.4, -16.0), "h": 3.0, "mode": "prop"},
			{"id": "library_story_scrolls", "tex": "rooms/library/library_story_scrolls.png",
				"pos": Vector3(-49.6, 35.4, -4.0), "h": 3.0, "mode": "prop"},
			{"id": "library_book_cart", "tex": "rooms/library/library_book_cart.png",
				"pos": Vector3(-44.0, 35.4, 2.0), "h": 3.4, "mode": "prop"},
			{"id": "library_reading_cushions", "tex": "rooms/library/library_reading_cushions.png",
				"pos": Vector3(-44.0, 35.0, 9.0), "h": 3.0, "mode": "prop"},
		],
	},
	{
		"id": "royal_kitchen",
		"who": "Princess Huluu",
		"intro": "The royal kitchen is floury and drippy! Shall we wipe it shiny?",
		"done": "The kitchen sparkles! The soup will taste even better now.",
		"vignette": "targets/room_vignettes/room_vignette_royal_kitchen.png",
		"vignette_pos": Vector3(17.0, -12.0, -2.0),
		"tool": "tools/tool_star_sponge.png",
		"targets": [
			# tc = o + (17, 0, -2); the counter run sits along the back wall
			{"id": "kitchen_sink_plates", "tex": "rooms/royal_kitchen/kitchen_sink_plates.png",
				"pos": Vector3(16.6, -13.7, -6.1), "h": 3.2, "mode": "fixture", "yaw": 0.0},
			{"id": "kitchen_counter_flour", "tex": "rooms/royal_kitchen/kitchen_counter_flour.png",
				"pos": Vector3(12.4, -14.05, -5.6), "h": 2.8, "mode": "flat"},
			{"id": "kitchen_stove_drips", "tex": "rooms/royal_kitchen/kitchen_stove_drips.png",
				"pos": Vector3(22.2, -14.2, -5.7), "h": 3.4, "mode": "fixture", "yaw": 0.0},
			{"id": "kitchen_crooked_pan", "tex": "rooms/royal_kitchen/kitchen_crooked_pan.png",
				"pos": Vector3(16.2, -13.4, -6.2), "h": 2.4, "mode": "prop"},
			{"id": "kitchen_cabinet_jars", "tex": "rooms/royal_kitchen/kitchen_cabinet_jars.png",
				"pos": Vector3(10.4, -13.6, -6.3), "h": 3.0, "mode": "prop"},
			{"id": "kitchen_tipped_cups", "tex": "rooms/royal_kitchen/kitchen_tipped_cups.png",
				"pos": Vector3(15.0, -15.9, 3.5), "h": 2.6, "mode": "prop"},
		],
	},
	{
		"id": "bubble_bath",
		"who": "Princess Huluu",
		"intro": "Bubble time made a splashy mess! Let us make it shine!",
		"done": "The bubble bath is sparkling clean. Splash splash!",
		"vignette": "targets/room_vignettes/room_vignette_bubble_bath.png",
		"vignette_pos": Vector3(-17.0, -12.0, -28.0),
		"tool": "tools/tool_shell_scrub_brush.png",
		"targets": [
			# bc = o + (-17, 0, -28); tub at the front wall, vanity at the back
			{"id": "bath_tub_soap_ring", "tex": "rooms/bubble_bath/bath_tub_soap_ring.png",
				"pos": Vector3(-19.0, -16.1, -23.9), "h": 3.6, "mode": "fixture", "yaw": 180.0},
			{"id": "bath_foggy_mirror", "tex": "rooms/bubble_bath/bath_foggy_mirror.png",
				"pos": Vector3(-12.0, -14.4, -33.5), "h": 3.0, "mode": "fixture", "yaw": 0.0},
			{"id": "bath_vanity_droplets", "tex": "rooms/bubble_bath/bath_vanity_droplets.png",
				"pos": Vector3(-12.0, -16.2, -33.0), "h": 2.6, "mode": "prop"},
			{"id": "bath_rumpled_towels", "tex": "rooms/bubble_bath/bath_rumpled_towels.png",
				"pos": Vector3(-11.5, -16.6, -22.8), "h": 3.0, "mode": "prop"},
			{"id": "bath_toy_basket", "tex": "rooms/bubble_bath/bath_toy_basket.png",
				"pos": Vector3(-23.2, -16.8, -27.0), "h": 3.0, "mode": "prop"},
			{"id": "bath_water_droplet_trail", "tex": "rooms/bubble_bath/bath_water_droplet_trail.png",
				"pos": Vector3(-17.0, -17.9, -28.5), "h": 4.0, "mode": "flat"},
		],
	},
	{
		"id": "royal_loo",
		"who": "Princess Huluu",
		"intro": "Even the little royal loo wants to sparkle!",
		"done": "The tiny royal loo is shiny. Nobody forgets the little room!",
		"vignette": "targets/room_vignettes/room_vignette_royal_loo.png",
		"vignette_pos": Vector3(-30.25, -12.0, -28.0),
		"tool": "tools/tool_shell_spray_bottle.png",
		"targets": [
			# lc = o + (-30.25, 0, -28); build_toilet() ground is lc + (-1.75, -18, 0)
			{"id": "loo_toilet_soap_ring", "tex": "rooms/basement/loo_toilet_soap_ring.png",
				"pos": Vector3(-32.0, -16.1, -28.0), "h": 3.0, "mode": "fixture", "yaw": 90.0},
			{"id": "loo_clean_water_splash", "tex": "rooms/basement/loo_clean_water_splash.png",
				"pos": Vector3(-29.6, -17.9, -26.4), "h": 2.6, "mode": "flat"},
			{"id": "loo_crooked_paper_rolls", "tex": "rooms/basement/loo_crooked_paper_rolls.png",
				"pos": Vector3(-33.6, -15.4, -30.6), "h": 2.4, "mode": "prop"},
			{"id": "loo_brush_holder", "tex": "rooms/basement/loo_brush_holder.png",
				"pos": Vector3(-33.6, -16.8, -25.6), "h": 2.4, "mode": "prop"},
		],
	},
	{
		"id": "undercroft",
		"who": "Princess Huluu",
		"intro": "The undercroft is dusty and cobwebby! Brave helper, follow me!",
		"done": "No more cobwebs down here. You are the bravest cleaner!",
		"vignette": "targets/room_vignettes/room_vignette_undercroft.png",
		"vignette_pos": Vector3(0.0, -12.0, 30.0),
		"tool": "tools/tool_shell_broom.png",
		"targets": [
			{"id": "undercroft_dusty_storage", "tex": "rooms/basement/undercroft_dusty_storage.png",
				"pos": Vector3(8.0, -16.6, 34.0), "h": 3.4, "mode": "prop"},
			{"id": "undercroft_stair_cobweb", "tex": "rooms/basement/undercroft_stair_cobweb.png",
				"pos": Vector3(-24.0, -13.0, 27.5), "h": 3.6, "mode": "prop"},
		],
	},
]

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

func build(o: Vector3) -> void:
	# additive only: every skin is a sprite laid over already-built geometry.
	# One room-scoped root owns every cleaning visual, so transient feedback
	# sprites never grow main's game_nodes list and the whole layer frees with
	# the arena in a single entry.
	var root := Node3D.new()
	root.name = "CastleCleanup"
	m.add_child(root)
	m.game_nodes.append(root)
	m.g["clean_root"] = root
	m.g["clean_targets"] = []
	m.g["clean_rooms"] = {}
	m.g["clean_active"] = ""
	m.g["clean_ring"] = null
	m.g["clean_tool"] = null
	m.g["clean_vignette"] = null
	m.g["clean_vignette_t"] = 0.0
	m.g["clean_room_seen"] = {}
	m.g["clean_praise_cool"] = 0.0
	var cleaned: Dictionary = _cleaned_dict()
	var ring: Sprite3D = _sprite(SKIN + "effects/fx_clean_ring.png", Vector3.ZERO, 5.0, "flat", 0.0)
	if ring != null:
		ring.visible = false
		m.g["clean_ring"] = ring
	var tool_card: Sprite3D = _sprite(SKIN + "effects/fx_wipe_swoosh.png", Vector3.ZERO, 2.6, "prop", 0.0)
	if tool_card != null:
		tool_card.visible = false
		m.g["clean_tool"] = tool_card
	for room_value: Variant in ROOMS:
		var room: Dictionary = room_value as Dictionary
		var room_id: String = String(room["id"])
		var room_targets: Array = []
		for target_value: Variant in (room["targets"] as Array):
			var target: Dictionary = target_value as Dictionary
			var target_id: String = String(target["id"])
			if bool(cleaned.get(target_id, false)):
				continue   # already finished on a previous day — never re-dirty
			var world_pos: Vector3 = o + (target["pos"] as Vector3)
			var mode: String = String(target.get("mode", "prop"))
			var skin: Sprite3D = _sprite(
				SKIN + String(target["tex"]), world_pos, float(target["h"]), mode, float(target.get("yaw", 0.0)))
			if skin == null:
				continue
			var entry: Dictionary = {
				"id": target_id,
				"room": room_id,
				"pos": world_pos,
				"node": skin,
				"rubs": 0,
				"cool": 0.0,
				"mode": mode,
			}
			(m.g["clean_targets"] as Array).append(entry)
			room_targets.append(target_id)
		(m.g["clean_rooms"] as Dictionary)[room_id] = {
			"left": room_targets.size(),
			"total": (room["targets"] as Array).size(),
			"centre": o + (room["vignette_pos"] as Vector3),
			"index": _room_index(room_id),
		}

func _room_index(room_id: String) -> int:
	for i in range(ROOMS.size()):
		if String((ROOMS[i] as Dictionary)["id"]) == room_id:
			return i
	return 0

func _cleaned_dict() -> Dictionary:
	if m.clean_done is Dictionary:
		return m.clean_done
	var stored: Variant = m.save_data.get("clean_done", {})
	return stored if stored is Dictionary else {}

# ---------------------------------------------------------------------------
# sprite construction (handoff "Rendering contract")
# ---------------------------------------------------------------------------

func _sprite(path: String, pos: Vector3, height: float, mode: String, yaw: float) -> Sprite3D:
	if not ResourceLoader.exists(path):
		return null
	var tex: Texture2D = load(path) as Texture2D
	if tex == null:
		return null
	var spr := Sprite3D.new()
	spr.texture = tex
	# the 512px canvas carries 32px of transparent padding on every side; the
	# visible silhouette is what gets fitted to `height`
	spr.pixel_size = height / float(maxi(tex.get_height(), 1))
	spr.position = pos
	spr.shaded = false                       # painted highlights, never relit
	spr.double_sided = true
	spr.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	# handoff render contract: linear filter, repeat disabled, mipmaps only
	# where a skin materially shrinks — these sit a few units from the camera
	spr.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR
	match mode:
		"flat":
			# floor/counter marks lie ON the receiving surface, depth-tested so
			# they never draw through furniture or walls
			spr.billboard = BaseMaterial3D.BILLBOARD_DISABLED
			spr.rotation_degrees = Vector3(-90.0, yaw, 0.0)
		"fixture":
			spr.billboard = BaseMaterial3D.BILLBOARD_DISABLED
			spr.rotation_degrees = Vector3(0.0, yaw, 0.0)
		_:
			spr.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	spr.visibility_range_end = 120.0 if m.quality == "speedy" else 0.0
	spr.visibility_range_end_margin = 10.0 if m.quality == "speedy" else 0.0
	spr.visibility_range_fade_mode = (
		GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
		if m.quality == "speedy"
		else GeometryInstance3D.VISIBILITY_RANGE_FADE_DISABLED
	)
	var root: Node3D = m.g.get("clean_root") as Node3D
	if is_instance_valid(root):
		root.add_child(spr)
	else:
		m.add_child(spr)
		m.game_nodes.append(spr)
	return spr

# ---------------------------------------------------------------------------
# tick
# ---------------------------------------------------------------------------

func tick(delta: float, ppos: Vector3) -> void:
	var targets: Array = m.g.get("clean_targets", [])
	if targets.is_empty():
		_hide_pointer()
		return
	m.g["clean_praise_cool"] = maxf(0.0, float(m.g.get("clean_praise_cool", 0.0)) - delta)
	_tick_vignette(delta)
	# nearest unfinished target inside reach becomes the one the ring points at
	var best: Dictionary = {}
	var best_d: float = REACH
	for value: Variant in targets:
		var entry: Dictionary = value as Dictionary
		entry["cool"] = maxf(0.0, float(entry["cool"]) - delta)
		var d: float = (entry["pos"] as Vector3).distance_to(ppos)
		if d < best_d:
			best_d = d
			best = entry
	if best.is_empty():
		m.g["clean_active"] = ""
		_hide_pointer()
		return
	_announce_room(String(best["room"]))
	m.g["clean_active"] = String(best["id"])
	_show_pointer(best)
	if float(best["cool"]) > 0.0:
		return
	if _rub_input():
		best["cool"] = RUB_COOL
		_rub(best)

func _rub_input() -> bool:
	# one finger, two equally valid gestures: a tap, or a rub (stick wiggle).
	# Both are real input — nothing here can fire on an idle frame, which is
	# what probe_passive.gd asserts.
	if m.touch_ui != null:
		if m.touch_ui.has_method("consume_action_just") and bool(m.touch_ui.consume_action_just()):
			return true
		if bool(m.touch_ui.action_down):
			return true
		var stick: Vector2 = m.touch_ui.stick_vec
		if stick.length() > WIGGLE_MIN:
			return true
	return false

# ---------------------------------------------------------------------------
# scrubbing
# ---------------------------------------------------------------------------

func _rub(entry: Dictionary) -> void:
	var rubs: int = int(entry["rubs"]) + 1
	entry["rubs"] = rubs
	var pos: Vector3 = entry["pos"]
	var skin: Sprite3D = entry["node"] as Sprite3D
	if is_instance_valid(skin):
		# every accepted input answers immediately — the grime visibly lifts
		skin.modulate.a = maxf(0.15, 1.0 - float(rubs) / float(RUBS_PER_TARGET) * 0.7)
		var tw: Tween = skin.create_tween()
		tw.tween_property(skin, "scale", Vector3.ONE * 1.06, 0.08)
		tw.tween_property(skin, "scale", Vector3.ONE, 0.12)
	_puff(pos, "effects/fx_soap_bubbles.png" if rubs % 2 == 1 else "effects/fx_dust_poof.png", 2.4)
	m._sparkle_burst(pos + Vector3(0, 1.2, 0), Color(0.72, 0.94, 1.0))
	if rubs == 1:
		_dust_bunny(pos)
	if rubs < RUBS_PER_TARGET:
		return
	_finish_target(entry)

func _finish_target(entry: Dictionary) -> void:
	var pos: Vector3 = entry["pos"]
	var skin: Sprite3D = entry["node"] as Sprite3D
	if is_instance_valid(skin):
		var tw: Tween = skin.create_tween()
		tw.tween_property(skin, "modulate:a", 0.0, 0.42)
		tw.parallel().tween_property(skin, "scale", Vector3.ONE * 1.25, 0.42)
		tw.tween_callback(skin.queue_free)
	_puff(pos, "effects/fx_gold_sparkle.png", 3.2)
	m._sparkle_burst(pos + Vector3(0, 1.6, 0), Color(1.0, 0.9, 0.55))
	var targets: Array = m.g.get("clean_targets", [])
	targets.erase(entry)
	# SAVE NOW: one finished object is progress a short session must never lose
	var cleaned: Dictionary = _cleaned_dict()
	cleaned[String(entry["id"])] = true
	m.clean_done = cleaned
	m.save_data["clean_done"] = cleaned
	m._write_save()
	var room_id: String = String(entry["room"])
	var rooms: Dictionary = m.g.get("clean_rooms", {})
	var room_state: Dictionary = rooms.get(room_id, {})
	if room_state.is_empty():
		return
	var left: int = maxi(int(room_state.get("left", 1)) - 1, 0)
	room_state["left"] = left
	var total: int = int(room_state.get("total", 1))
	_progress_card(pos, total - left, total)
	if left > 0:
		if float(m.g.get("clean_praise_cool", 0.0)) <= 0.0:
			m.g["clean_praise_cool"] = 3.0
			m._say("huluu", "clean", 4.0)
			m.show_msg("Princess Huluu", "Look how shiny! Keep going!", "talk")
		return
	_finish_room(room_id, pos)

func _finish_room(room_id: String, pos: Vector3) -> void:
	var room: Dictionary = ROOMS[_room_index(room_id)] as Dictionary
	_puff(pos + Vector3(0, 2.5, 0), "effects/fx_all_clean_badge.png", 4.0)
	m._sparkle_burst(pos + Vector3(0, 3.0, 0), Color(1.0, 0.86, 0.5))
	m._say("huluu", "cleanwin", 0.0)
	m.show_msg("Princess Huluu", String(room["done"]), "win")
	if m.g.get("clean_targets", []).is_empty():
		_finish_castle(pos)

func _finish_castle(pos: Vector3) -> void:
	# the whole castle sparkles. The Crown Light beat itself belongs to the
	# Week-of-Light wiring (STORY_DAYS W2) — this pass only celebrates.
	m._fanfare()
	m._sparkle_burst(pos + Vector3(0, 4.0, 0), Color(1.0, 0.95, 0.7))
	m.show_msg("Princess Huluu", "The whole castle is sparkling! It is ready for the Festival!", "win")

# ---------------------------------------------------------------------------
# feedback art (dust bunnies, puffs, progress shells, pointer, vignettes)
# ---------------------------------------------------------------------------

func _puff(pos: Vector3, rel: String, height: float) -> void:
	# Speedy tier caps the feedback layers the handoff allows at two
	var spr: Sprite3D = _sprite(SKIN + rel, pos + Vector3(0, 1.0, 0), height, "prop", 0.0)
	if spr == null:
		return
	var tw: Tween = spr.create_tween()
	tw.tween_property(spr, "position", spr.position + Vector3(0, 1.6, 0), 0.55)
	tw.parallel().tween_property(spr, "modulate:a", 0.0, 0.55)
	tw.tween_callback(spr.queue_free)

func _dust_bunny(pos: Vector3) -> void:
	if m.quality == "speedy":
		return
	var art: Array[String] = [
		"critters/dust_bunnies/dust_bunny_hop.png",
		"critters/dust_bunnies/dust_bunny_curl_ears.png",
		"critters/dust_bunnies/dust_bunny_siblings.png",
		"critters/dust_bunnies/dust_bunny_sleepy.png",
	]
	var spr: Sprite3D = _sprite(SKIN + art[randi() % art.size()], pos + Vector3(0, 0.6, 0), 2.2, "prop", 0.0)
	if spr == null:
		return
	# a friendly reaction, never a squash: the bunny hops aside and waves off
	var away := Vector3(randf_range(-2.4, 2.4), 0.0, randf_range(-2.4, 2.4))
	var tw: Tween = spr.create_tween()
	tw.tween_property(spr, "position", spr.position + away + Vector3(0, 1.1, 0), 0.34).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(spr, "position", spr.position + away, 0.26).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
	tw.tween_property(spr, "modulate:a", 0.0, 0.5)
	tw.tween_callback(spr.queue_free)

func _progress_card(pos: Vector3, done: int, total: int) -> void:
	# non-reading progress: one, two, then three pearls. Rooms with more than
	# three targets show the three-pearl card once they are finished.
	var step: int = clampi(int(round(float(done) / float(maxi(total, 1)) * 3.0)), 1, 3)
	var card: String = ["progress/progress_one_pearl.png",
		"progress/progress_two_pearls.png",
		"progress/progress_three_pearls.png"][step - 1]
	var spr: Sprite3D = _sprite(SKIN + card, pos + Vector3(0, 3.2, 0), 2.8, "prop", 0.0)
	if spr == null:
		return
	var tw: Tween = spr.create_tween()
	tw.tween_property(spr, "position", spr.position + Vector3(0, 1.0, 0), 1.1)
	tw.parallel().tween_property(spr, "modulate:a", 0.0, 1.1)
	tw.tween_callback(spr.queue_free)

func _show_pointer(entry: Dictionary) -> void:
	var ring: Sprite3D = m.g.get("clean_ring") as Sprite3D
	var pos: Vector3 = entry["pos"]
	if is_instance_valid(ring):
		ring.visible = true
		var lift: float = 0.06 if String(entry["mode"]) == "flat" else -1.4
		ring.position = pos + Vector3(0, lift, 0)
		var pulse: float = 1.0 + sin(float(m.g.get("t", 0.0)) * 4.0) * 0.09
		ring.scale = Vector3.ONE * pulse
	var tool_card: Sprite3D = m.g.get("clean_tool") as Sprite3D
	if is_instance_valid(tool_card):
		var room: Dictionary = ROOMS[_room_index(String(entry["room"]))] as Dictionary
		var tool_path: String = SKIN + String(room["tool"])
		if ResourceLoader.exists(tool_path) and tool_card.get_meta("tool_path", "") != tool_path:
			tool_card.texture = load(tool_path) as Texture2D
			tool_card.set_meta("tool_path", tool_path)
			var tool_tex: Texture2D = tool_card.texture
			if tool_tex != null:
				tool_card.pixel_size = 2.6 / float(maxi(tool_tex.get_height(), 1))
		tool_card.visible = true
		tool_card.position = pos + Vector3(0, 2.6 + sin(float(m.g.get("t", 0.0)) * 2.4) * 0.16, 0)

func _hide_pointer() -> void:
	var ring: Sprite3D = m.g.get("clean_ring") as Sprite3D
	if is_instance_valid(ring):
		ring.visible = false
	var tool_card: Sprite3D = m.g.get("clean_tool") as Sprite3D
	if is_instance_valid(tool_card):
		tool_card.visible = false

func _announce_room(room_id: String) -> void:
	var seen: Dictionary = m.g.get("clean_room_seen", {})
	if bool(seen.get(room_id, false)):
		return
	seen[room_id] = true
	var room: Dictionary = ROOMS[_room_index(room_id)] as Dictionary
	var rooms: Dictionary = m.g.get("clean_rooms", {})
	var room_state: Dictionary = rooms.get(room_id, {})
	var centre: Vector3 = room_state.get("centre", Vector3.ZERO)
	m._say("huluu", "cleanroom", 0.0)
	m.show_msg(String(room["who"]), String(room["intro"]), "talk")
	# the room vignette introduces the mess, then dissolves before the child
	# starts on the individual targets (never shown alongside all of them)
	var vignette: Sprite3D = _sprite(SKIN + String(room["vignette"]), centre, 9.0, "prop", 0.0)
	if vignette == null:
		return
	var previous: Sprite3D = m.g.get("clean_vignette") as Sprite3D
	if is_instance_valid(previous):
		previous.queue_free()
	m.g["clean_vignette"] = vignette
	m.g["clean_vignette_t"] = VIGNETTE_SECONDS

func _tick_vignette(delta: float) -> void:
	var left: float = float(m.g.get("clean_vignette_t", 0.0))
	if left <= 0.0:
		return
	left -= delta
	m.g["clean_vignette_t"] = left
	var vignette: Sprite3D = m.g.get("clean_vignette") as Sprite3D
	if not is_instance_valid(vignette):
		return
	if left <= 0.0:
		var tw: Tween = vignette.create_tween()
		tw.tween_property(vignette, "modulate:a", 0.0, 0.5)
		tw.tween_callback(vignette.queue_free)
		m.g["clean_vignette"] = null
		return
	vignette.modulate.a = clampf(left / 0.8, 0.0, 0.9)

# ---------------------------------------------------------------------------
# probe / debug surface
# ---------------------------------------------------------------------------

func targets_left() -> int:
	return (m.g.get("clean_targets", []) as Array).size()

func cleaned_count() -> int:
	return _cleaned_dict().size()
