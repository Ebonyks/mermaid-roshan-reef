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
}

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

# ---------------------------------------------------------------- tier math

func evaluate(id: String, stats: Dictionary) -> int:
	# Pure: no side effects, probe-testable. Returns 0 for unranked ids (shop).
	if id == "fairy":
		# Precision shmup: gold = a perfect run (never lost the sparkle shield,
		# zapped every shadow bug); silver = at most one shield loss.
		if int(stats.get("fails", 0)) == 0 and int(stats.get("hits", 0)) >= 10:
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
	_celebrate(tier)
	var best: int = int(m.medals.get(id, 0))
	if tier > best:
		m.medals[id] = tier
		refresh_friend_glyphs()
		m._update_hud()
		m._write_save()
	return tier

func award_from_end_game(game_id: String, g2: Dictionary) -> void:
	# Central hook inside main._end_game(win=true): every 3D arena game's
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
	return "   🥇 %d  🥈 %d  🥉 %d" % [int(c[3]), int(c[2]), int(c[1])]

func refresh_friend_glyphs() -> void:
	# a floating medal under each won friend's star — the in-world scoreboard
	for f in m.friends:
		var tier: int = int(m.medals.get(String(f.get("game", "")), 0))
		if tier <= 0:
			continue
		var lab: Label3D = null
		if f.has("medal_lab") and is_instance_valid(f["medal_lab"]):
			lab = f["medal_lab"]
		else:
			lab = Label3D.new()
			lab.font_size = 150
			lab.outline_size = 16
			lab.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			lab.position = (f["node"] as Sprite3D).position + Vector3(0, 5.6, 0)
			m.add_child(lab)
			f["medal_lab"] = lab
		lab.text = String(GLYPH[tier])

func _celebrate(tier: int) -> void:
	# tier banner + tier-colored sparkles + a chime that rises with the medal.
	# Kept lighter than _celebrate_pose (which still owns first-time trophies).
	var cl := CanvasLayer.new()
	cl.layer = 23
	m.add_child(cl)
	var big := Label.new()
	big.text = String(GLYPH[tier])
	big.add_theme_font_size_override("font_size", 96)
	big.add_theme_constant_override("outline_size", 14)
	big.add_theme_color_override("font_outline_color", Color(0.2, 0.1, 0.3))
	big.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	big.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	big.offset_top = 180.0
	cl.add_child(big)
	var col: Color = TIER_COLOR[tier]
	if m.player != null:
		for si in range(2 + tier * 2):
			var sa: float = TAU * float(si) / float(2 + tier * 2)
			m._sparkle_burst(m.player.position + Vector3(cos(sa) * 2.0, 1.2, sin(sa) * 2.0), col)
	if m.chime != null:
		m.chime.pitch_scale = 1.0 + 0.15 * float(tier)
		m.chime.play()
	m.get_tree().create_timer(2.2).timeout.connect(cl.queue_free)
