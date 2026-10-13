class_name MedalSystem
extends RefCounted
# Bronze / silver / gold performance ranking for every minigame. All mutable
# state stays on main (m.medals: game id -> best tier ever earned); this class
# owns only the logic, following the CollectionSystem satellite pattern.
#
# Design contract (see MEDALS.md):
# - Bronze is COMPLETION. Every finished game earns at least bronze — there is
#   still no fail state anywhere; a medal can only be added, never taken away.
# - Silver rewards solid play a preschooler lands sometimes.
# - Gold demands real skill and precision (zero misses, full collections,
#   fast times, 1st place) — calibrated for a 6-8 year old, so it stays a
#   long-term goal the game can grow into.
# - Medals persist upgrade-only in reef_save.json under "medals".
# - Awards fire ONLY from win paths. A zero-input session can never change
#   m.medals (probe_passive guards this).

const BRONZE := 1
const SILVER := 2
const GOLD := 3

const GLYPH := {1: "🥉", 2: "🥈", 3: "🥇"}
const TIER_COLOR := {
	1: Color(0.87, 0.56, 0.32),
	2: Color(0.88, 0.91, 0.98),
	3: Color(1.0, 0.85, 0.25),
}
const CELEBRATION_ELEMENTS := {BRONZE: 8, SILVER: 10, GOLD: 12}
const CELEBRATION_CENTER := Vector2(640.0, 255.0)
const CELEBRATION_SECONDS := 2.2
const CELEBRATION_LAYER_NAME := "MedalCelebrationLayer"

# Threshold table. kind "fewer": stat <= gold -> gold, <= silver -> silver
# (misses, seconds, race placement — lower is better). kind "more": stat >=
# gold -> gold, >= silver -> silver (collectibles, rooms — higher is better).
# Games with compound rules (fairy, penguin) are handled in evaluate().
# All numbers are tuning knobs — see MEDALS.md before changing.
const TIERS := {
	"fetch":       {"kind": "fewer", "key": "miss", "gold": 0, "silver": 2},
	"dolls":       {"kind": "fewer", "key": "missed", "gold": 0, "silver": 2},
	"seek":        {"kind": "fewer", "key": "slow_find", "gold": 12.0, "silver": 25.0},
	"melody":      {"kind": "fewer", "key": "time", "gold": 75.0, "silver": 150.0},
	"slide":       {"kind": "more", "key": "got", "gold": 5, "silver": 3},
	"race":        {"kind": "fewer", "key": "time", "gold": 80.0, "silver": 160.0},
	"treasure":    {"kind": "fewer", "key": "time", "gold": 100.0, "silver": 200.0},
	"snowman":     {"kind": "fewer", "key": "time", "gold": 80.0, "silver": 160.0},
	"garden":      {"kind": "fewer", "key": "time", "gold": 25.0, "silver": 60.0},
	"trampoline":  {"kind": "fewer", "key": "time", "gold": 10.0, "silver": 25.0},
	"xmas":        {"kind": "fewer", "key": "time", "gold": 35.0, "silver": 80.0},
	"kart":        {"kind": "fewer", "key": "place", "gold": 1, "silver": 3},
	"galaxy":      {"kind": "fewer", "key": "time", "gold": 360.0, "silver": 720.0},
	"combat_ice":  {"kind": "fewer", "key": "time", "gold": 60.0, "silver": 120.0},
	"combat_fire": {"kind": "fewer", "key": "time", "gold": 75.0, "silver": 150.0},
	"dungeon":     {"kind": "more", "key": "rooms", "gold": 10, "silver": 5},
	"bells":       {"kind": "fewer", "key": "oops", "gold": 0, "silver": 2},
	"dance":       {"kind": "more", "key": "combo", "gold": 10, "silver": 5},
	# Boss contact is harmless, so it is also the optional mastery axis: zero or
	# one bump earns gold, two earns silver, and three-plus still earns bronze.
	# Completion and story progress remain unconditional.
	"dustboss":    {"kind": "fewer", "key": "bumps", "gold": 1, "silver": 2},
}

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ---------------------------------------------------------------- tier math

func evaluate(id: String, stats: Dictionary) -> int:
	# Pure: no side effects, probe-testable. Returns 0 for unranked ids (shop).
	if id == "fairy":
		# Gentle flight: gold = a perfect run (never emptied fairy light and
		# sparkled all seven danger bugs); silver = at most one light refill.
		if int(stats.get("fails", 0)) == 0 and int(stats.get("hits", 0)) >= 7:
			return GOLD
		return SILVER if int(stats.get("fails", 0)) <= 1 else BRONZE
	if id == "penguin":
		# Chase slide: gold = actually caught him (plan beans + corner him);
		# silver = cornered him at least once so he had to panic-burst away.
		if bool(stats.get("caught", false)):
			return GOLD
		return SILVER if int(stats.get("panic", 0)) >= 1 else BRONZE
	if not TIERS.has(id):
		return 0
	var t: Dictionary = TIERS[id]
	var stat: float = float(stats.get(String(t["key"]), 1.0e9))
	if String(t["kind"]) == "more":
		stat = float(stats.get(String(t["key"]), -1.0e9))
		if stat >= float(t["gold"]):
			return GOLD
		return SILVER if stat >= float(t["silver"]) else BRONZE
	if stat <= float(t["gold"]):
		return GOLD
	return SILVER if stat <= float(t["silver"]) else BRONZE

# ---------------------------------------------------------------- award flow

func award_stats(id: String, stats: Dictionary) -> int:
	# The single entry point every win path calls. Celebrates the tier earned
	# THIS run; persists only upgrades so a slower replay never loses a medal.
	var tier: int = evaluate(id, stats)
	if tier <= 0:
		return 0
	_celebrate(tier, id, stats)
	var best: int = int(m.medals.get(id, 0))
	if tier > best:
		m.medals[id] = tier
		refresh_friend_glyphs()
		m._update_hud()
		m._write_save()
	return tier

func award_from_end_game(game_id: String, g2: Dictionary) -> void:
	# Central hook inside main._end_game(win=true): every arena game's
	# scratch dict already carries its performance signals — no per-game
	# call-site changes needed here.
	match game_id:
		"fetch":
			award_stats("fetch", {"miss": int(g2.get("miss", 0))})
		"dolls":
			award_stats("dolls", {"missed": int(g2.get("missed", 0))})
		"seek":
			award_stats("seek", {"slow_find": float(g2.get("slow_find", float(g2.get("t", 0.0))))})
		"melody":
			award_stats("melody", {"time": float(g2.get("t", 0.0))})
		"race":
			award_stats("race", {"time": float(g2.get("t", 0.0))})
		"treasure":
			award_stats("treasure", {"time": float(g2.get("t", 0.0))})
		"slide":
			if String(g2.get("mode", "fish")) == "chase":
				award_stats("penguin", {"caught": bool(g2.get("caught", false)), "panic": int(g2.get("panic_n", 0))})
			else:
				award_stats("slide", {"got": int(g2.get("got", 0))})
		"fairyshoot":
			award_stats("fairy", {"fails": m.fs_fails, "hits": int(g2.get("hits", 0))})
		"dustboss":
			award_stats("dustboss", {
				"bumps": int(g2.get("db_bumps", 0)),
				"perfect_bonus": bool(g2.get("db_perfect_bonus", false)),
			})

func award_from_mg2d(kind: String, mg2: Dictionary) -> void:
	# 2D picture games are tap toys — the skill axis is pace, so they rank on
	# completion time (mg["t"] runs from _mg2d_open to the win).
	if kind in ["snowman", "garden", "trampoline", "xmas"]:
		award_stats(kind, {"time": float(mg2.get("t", 0.0))})

# ---------------------------------------------------------------- display

func counts() -> Dictionary:
	var out: Dictionary = {1: 0, 2: 0, 3: 0}
	for tier_value: Variant in m.medals.values():
		var tier: int = clampi(int(tier_value), 0, 3)
		if tier > 0:
			out[tier] = int(out[tier]) + 1
	return out

func hud_suffix() -> String:
	# appended to the hud_stars line — pure glyphs, readable by a non-reader
	var c: Dictionary = counts()
	if int(c[1]) + int(c[2]) + int(c[3]) == 0:
		return ""
	# its OWN line: appended to the star/crown line it ran past the right edge
	# of the status tray and spilled the medal glyphs out over the world
	return "\n🥇 %d  🥈 %d  🥉 %d" % [int(c[3]), int(c[2]), int(c[1])]

func refresh_friend_glyphs() -> void:
	# Compatibility hook for callers and live sessions that predate the Canvas
	# medal display. Friend dictionaries never persist scene nodes, but a hot
	# session can still cache the retired in-world badge under `medal_lab`.
	# Detach it synchronously so refresh is idempotent from the active tree's
	# perspective; the non-reading tally above and centered award remain the
	# sole medal displays.
	for friend: Dictionary in m.friends:
		if not friend.has("medal_lab"):
			continue
		var legacy_value: Variant = friend.get("medal_lab")
		if legacy_value is Node and is_instance_valid(legacy_value):
			var legacy_node := legacy_value as Node
			if legacy_node.get_parent() != null:
				legacy_node.get_parent().remove_child(legacy_node)
			legacy_node.queue_free()
		friend.erase("medal_lab")

func _celebrate(tier: int, id: String = "", stats: Dictionary = {}) -> void:
	# The centered tier card owns one bounded Canvas celebration. A rapid replay
	# replaces it synchronously, so neither transparent elements nor tweens can
	# accumulate while the child keeps tapping through completion screens.
	_retire_celebration()
	var cl := CanvasLayer.new()
	cl.name = CELEBRATION_LAYER_NAME
	cl.layer = 23
	cl.set_meta("celebration_tier", tier)
	m.add_child(cl)
	var card := StorybookUI.add_hud_panel(cl, Rect2(490, 140, 300, 230), Color(TIER_COLOR[tier]), Color(1.0, 0.97, 0.90, 0.97), 48)
	card.name = "MedalCelebrationCard"
	var big := Label.new()
	big.name = "MedalCelebrationGlyph"
	big.text = String(GLYPH[tier])
	big.position = Vector2(0.0, 0.0)
	big.size = Vector2(300.0, 142.0)
	StorybookUI.style_hud_label(big, 82, StorybookUI.INK, 8)
	big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	big.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	card.add_child(big)
	var stars := Label.new()
	stars.name = "MedalCelebrationStars"
	stars.text = _star_row(tier)
	stars.position = Vector2(0.0, 132.0)
	stars.size = Vector2(300.0, 82.0)
	stars.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stars.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	StorybookUI.style_hud_label(stars, 46, TIER_COLOR[tier] as Color, 6)
	card.add_child(stars)
	var perfect_bonus: bool = id == "dustboss" \
		and bool(stats.get("perfect_bonus", false))
	cl.set_meta("perfect_bonus", perfect_bonus)
	if perfect_bonus:
		var gem := Label.new()
		gem.name = "PerfectBonusGem"
		gem.text = "💎"
		gem.position = Vector2(216.0, 4.0)
		gem.size = Vector2(76.0, 72.0)
		gem.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		gem.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		StorybookUI.style_hud_label(gem, 45, StorybookUI.PEARL_BLUE, 6)
		card.add_child(gem)
	var col: Color = TIER_COLOR[tier]
	var element_count: int = int(CELEBRATION_ELEMENTS[tier])
	var burst := Control.new()
	burst.name = "MedalCelebrationBurst"
	burst.position = CELEBRATION_CENTER
	burst.mouse_filter = Control.MOUSE_FILTER_IGNORE
	burst.set_meta("feedback_kind", "medal")
	burst.set_meta("visible_elements", element_count)
	cl.add_child(burst)
	var star_points := PackedVector2Array([
		Vector2(0, -14), Vector2(4, -4), Vector2(14, 0), Vector2(4, 4),
		Vector2(0, 14), Vector2(-4, 4), Vector2(-14, 0), Vector2(-4, -4)])
	for i in range(element_count):
		var angle: float = TAU * float(i) / float(element_count) \
			+ 0.09 * float(i % 2)
		var direction := Vector2(cos(angle), sin(angle))
		var sparkle := Polygon2D.new()
		sparkle.polygon = star_points
		sparkle.color = col.lerp(Color.WHITE, 0.12 * float(i % 3))
		sparkle.position = direction * 10.0
		sparkle.rotation = angle
		sparkle.scale = Vector2.ONE * (0.78 + 0.10 * float(i % 3))
		sparkle.set_meta("feedback_endpoint",
			direction * (112.0 + 12.0 * float(i % 3)))
		burst.add_child(sparkle)
	var feedback_tween := burst.create_tween()
	feedback_tween.set_parallel(true)
	for child_value in burst.get_children():
		var sparkle := child_value as Polygon2D
		if sparkle == null:
			continue
		var endpoint: Vector2 = sparkle.get_meta(
			"feedback_endpoint", Vector2.ZERO) as Vector2
		feedback_tween.tween_property(sparkle, "position", endpoint, 0.78) \
			.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		feedback_tween.tween_property(
			sparkle, "scale", Vector2(0.18, 0.18), 0.78)
		feedback_tween.tween_property(sparkle, "modulate:a", 0.0, 0.78)
	cl.set_meta("feedback_tween", feedback_tween)
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + 0.15 * float(tier)
		m.chime.play()
	var teardown_tween := cl.create_tween()
	teardown_tween.tween_interval(CELEBRATION_SECONDS)
	teardown_tween.tween_callback(cl.queue_free)
	cl.set_meta("teardown_tween", teardown_tween)

func _star_row(tier: int) -> String:
	var out := ""
	for i in range(GOLD):
		out += "★" if i < tier else "☆"
	return out

func _retire_celebration() -> void:
	var previous := m.get_node_or_null(CELEBRATION_LAYER_NAME) as CanvasLayer
	if previous == null or not is_instance_valid(previous):
		return
	previous.visible = false
	for meta_key: StringName in [&"feedback_tween", &"teardown_tween"]:
		var previous_tween: Tween = previous.get_meta(meta_key) as Tween
		if previous_tween != null and previous_tween.is_valid():
			previous_tween.kill()
	# Removing before queueing makes replacement synchronous from the active
	# tree's perspective; the old layer cannot overlap the new award for a frame.
	if previous.get_parent() != null:
		previous.get_parent().remove_child(previous)
	previous.queue_free()
