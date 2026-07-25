extends SceneTree
# Emits audit/opera_art_manifest.json — the machine-readable contract between
# the GAME and codex's concept art.
#
# Why this exists: every art work order written by hand has gone stale within a
# day, because the acts keep being redesigned underneath it. A prop list that a
# human retypes is a snapshot; this is derived from OperaHouse.ACTS and the
# beat tables below, so when an act changes its beats the manifest changes with
# it and the diff tells codex exactly which objects need redesigning.
#
# Run:  $GODOT --headless -s scripts/probe_art_manifest.gd
# It is a GENERATOR, not a gate — it never prints FAIL.

const OUT_PATH := "res://audit/opera_art_manifest.json"

# The costume key in OperaHouse.ACTS is not always the asset folder name.
const DIR_ALIAS := {"chef": "pastry_chef"}

# Beats that are SPECIFIED in OPERA_ACT_REDESIGN_2026-07-25.md but not yet
# playable. Their art is still wanted — it is simply not the art that unblocks
# a beat a child can play today, so the manifest marks it and codex can sort
# by it. Delete a name from here in the same commit that ships its beat.
const PENDING_BEATS := {
	"detective": ["case_board"],
	"candymaker": ["syrup", "wrap", "parade"],
	"farmer": ["plant", "mud", "barn"],
	"painter": ["sketch", "fill"],
}

# Every beat a career actually plays, and the objects that beat needs on screen.
# "states" are the visual states the gesture drives — the rule that generates
# them: if the child's finger changes what a thing looks like, it needs states.
const BEATS := {
	"chef": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping", "gone"], "caged_farmer": ["trapped", "freed", "waving"], "carrot_gift": ["flying", "landed"]}},
		{"beat": "sift", "gesture": "scrub", "objects": {"sieve": ["still", "shaking"], "flour_snow": ["falling"], "bowl": ["empty", "dusted"]}},
		{"beat": "pour", "gesture": "hold", "objects": {"milk_jug": ["upright", "tipping", "pouring"], "fill_line": ["under", "reached", "over"]}},
		{"beat": "stir", "gesture": "circular drag", "objects": {"batter": ["loose", "ribboning", "thick", "peaked"], "whisk": ["still", "spinning"], "stir_swirl": ["turning"]}},
		{"beat": "bake", "gesture": "timed tap", "objects": {"oven": ["closed", "glowing", "open"], "cake_in_tin": ["flat", "rising", "risen", "golden"]}},
		{"beat": "pipe", "gesture": "trace", "objects": {"piping_bag": ["idle", "squeezing"], "guide_dot": ["waiting", "piped"], "frosting_bead": ["set"]}},
		{"beat": "decorate", "gesture": "drag-and-drop", "objects": {"cherry": ["loose", "placed"], "topping_spot": ["empty", "filled"]}},
	],
	"detective": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_stagehand": ["trapped", "freed"], "lantern_gift": ["flying", "landed"]}},
		{"beat": "search", "gesture": "drag lens + dwell", "objects": {"magnifier": ["held"], "clue_glint": ["hidden", "lit"], "dwell_ring": ["empty", "filling", "full"], "prop_box": ["closed", "wiggling", "open", "fish_surprise"]}},
		{"beat": "case_board", "gesture": "drag-and-drop", "objects": {"case_board": ["empty", "partial", "complete"], "clue_card": ["loose", "pinned"], "suspect_portrait": ["neutral", "accused", "cleared"]}},
	],
	"ballerina": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_dancer": ["trapped", "freed"], "ribbon_gift": ["flying", "landed"]}},
		{"beat": "barre", "gesture": "hold", "objects": {"barre": ["idle"], "pose_ribbon": ["empty", "winding", "full"]}},
		{"beat": "echo", "gesture": "watch + hold", "objects": {"dance_tile": ["dark", "demo", "pressed"], "mirror_ball": ["turning"]}},
		{"beat": "ribbon", "gesture": "trace", "objects": {"ribbon_arc": ["guide", "traced"], "ribbon_wand": ["held"]}},
		{"beat": "twirl", "gesture": "circular drag", "objects": {"tutu_flare": ["still", "spinning"], "petal_fall": ["falling"]}},
	],
	"candymaker": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_mouse": ["trapped", "freed"], "sugar_gift": ["flying", "landed"]}},
		{"beat": "syrup", "gesture": "hold", "objects": {"syrup_bottle": ["upright", "tipping"], "vat": ["empty", "filling", "full"]}},
		{"beat": "sort", "gesture": "drag-and-drop", "objects": {"conveyor": ["slow", "fast"], "candy_body": ["riding", "carried", "chuted", "rejected"], "collar_ring": ["pink", "blue", "gold"], "chute": ["idle", "hover", "accept", "reject"]}},
		{"beat": "wrap", "gesture": "rotational drag", "objects": {"wrapper": ["loose", "twisting", "sealed"]}},
		{"beat": "parade", "gesture": "drag-and-drop", "objects": {"parade_cart": ["empty", "loading", "full", "rolling"]}},
	],
	"doctor": [
		{"beat": "chase", "gesture": "tap", "objects": {"ward_imp": ["mischief", "popped"]}},
		{"beat": "find", "gesture": "search + tap", "objects": {"ward_animal": ["well", "hurt", "scooped"], "ouch_star": ["throbbing"]}},
		{"beat": "carry", "gesture": "walk", "objects": {"carried_patient": ["in_arms"]}},
		{"beat": "xray", "gesture": "read + tap", "objects": {"fluoroscope": ["dark", "lit"], "bone": ["sound", "cracked", "named"], "crack_pulse": ["pulsing"]}},
		{"beat": "cast", "gesture": "circular drag", "objects": {"padding_band": ["layer1", "layer2", "layer3"], "limb": ["bare", "padded"]}},
		{"beat": "coban", "gesture": "circular drag", "objects": {"coban_band": ["layer1", "layer2"], "limb": ["padded", "sealed"], "recovered_animal": ["hopping"]}},
	],
	"farmer": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_farmer": ["trapped", "freed"], "carrot_gift": ["flying", "landed"]}},
		{"beat": "plant", "gesture": "drag-and-drop", "objects": {"seed": ["loose", "dropped"], "furrow_hole": ["empty", "sprouting"]}},
		{"beat": "feed", "gesture": "charge-and-release", "objects": {"sling_pull": ["slack", "drawn"], "aim_dot": ["arc"], "veggie": ["in_flight", "landed", "bounced"], "piggy": ["trot", "hop", "munch", "fed"]}},
		{"beat": "mud", "gesture": "swipe up", "objects": {"mud_puddle": ["still", "splashed"], "piggy_leap": ["airborne", "landed"]}},
		{"beat": "barn", "gesture": "drag", "objects": {"barn_gate": ["shut", "open"], "sunset_sky": ["dusk"]}},
	],
	"boxer": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_crew": ["trapped", "freed"], "gloves_gift": ["flying", "landed"]}},
		{"beat": "warmup", "gesture": "tap", "objects": {"training_bag": ["hanging", "swinging"], "bag_strap": ["taut"]}},
		{"beat": "rounds", "gesture": "rhythm tap", "objects": {"ring_imp": ["down", "up", "bopped"], "beat_lamp": ["off", "pulse"], "round_light": ["dim", "won"]}},
		{"beat": "duck", "gesture": "swipe down", "objects": {"swinging_glove": ["incoming", "passed"]}},
		{"beat": "belt", "gesture": "walk", "objects": {"belt": ["descending", "taken"], "podium": ["dim", "gold"]}},
	],
	"magician": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_usher": ["trapped", "freed"], "scarf_gift": ["flying", "landed"]}},
		{"beat": "vanish", "gesture": "drag", "objects": {"magic_hat": ["idle", "lifted", "settled"], "bunny_fish": ["visible", "hidden"]}},
		{"beat": "shuffle", "gesture": "track + tap", "objects": {"swap_trail": ["swirling"], "magic_hat": ["dancing"], "reveal_pop": ["burst"]}},
		{"beat": "rope", "gesture": "pull-apart drag", "objects": {"knotted_rope": ["knotted", "loosening", "straight"]}},
		{"beat": "cabinet", "gesture": "rhythm tap", "objects": {"trick_cabinet": ["shut", "swinging", "open"], "star_wand": ["idle", "tapped"], "giant_bunny_fish": ["revealed"]}},
	],
	"painter": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_painter": ["trapped", "freed"], "paints_gift": ["flying", "landed"]}},
		{"beat": "sketch", "gesture": "trace", "objects": {"guide_outline": ["dotted", "drawn"], "charcoal_line": ["following"]}},
		{"beat": "fill", "gesture": "tap-to-flood", "objects": {"shape_region": ["blank", "flooded"], "shape_marker": ["circle", "star", "heart"]}},
		{"beat": "paint", "gesture": "drag-to-paint", "objects": {"brush_stamp": ["soft_round"], "primed_canvas": ["bare", "partial", "covered"], "loaded_brush": ["plum", "coral", "cream"]}},
		{"beat": "splatter", "gesture": "tap", "objects": {"splat": ["wet"]}},
		{"beat": "frame", "gesture": "drag-and-drop", "objects": {"gold_frame": ["loose", "fitted"], "gallery_wall": ["empty", "hung"]}},
	],
	"astronaut": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_engineer": ["trapped", "freed"], "pipes_gift": ["flying", "landed"]}},
		{"beat": "pipedream", "gesture": "drag-and-drop", "objects": {"grid_cell": ["empty", "waiting", "piped"], "pipe_piece": ["straight", "upright", "elbow_ne", "elbow_nw", "elbow_se", "elbow_sw"], "queue_slot": ["front", "waiting"], "bubble_flow": ["running", "leaking"], "fuse": ["lit", "burning"]}},
		{"beat": "valve", "gesture": "tap", "objects": {"valve_wheel": ["still", "spinning"], "pressure_lamp": ["off", "on"]}},
		{"beat": "launch", "gesture": "hold", "objects": {"thrust_bar": ["empty", "filling", "sagging", "full"], "rocket": ["idle", "straining", "launched"], "bubble_column": ["growing"]}},
	],
	"racer": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_pitcrew": ["trapped", "freed"], "wheels_gift": ["flying", "landed"]}},
		{"beat": "race", "gesture": "steering", "objects": {"opera_kart": ["livery"], "lap_pip": ["one", "two"], "zoom_strip": ["idle", "active"], "checkered_flag": ["waving"], "trophy_podium": ["dim", "gold"]}},
	],
	"popstar": [
		{"beat": "rescue", "gesture": "tap", "objects": {"bubble_cage": ["whole", "popping"], "caged_band": ["trapped", "freed"], "instruments_gift": ["flying", "landed"]}},
		{"beat": "concert", "gesture": "rhythm", "objects": {"pearl_microphone": ["idle", "singing"], "arrow_glyph": ["left", "right", "up", "down"], "hold_note_tail": ["held"], "encore_banner": ["hidden", "shown"]}},
	],
}

func _init() -> void:
	var acts := {}
	var total_objects := 0
	var total_states := 0
	var total_missing := 0
	var total_built := 0
	var total_pending := 0
	for cfg: Dictionary in OperaHouse.ACTS:
		var costume := String(cfg.get("costume", ""))
		if costume == "" or not BEATS.has(costume):
			continue
		var dir_name := String(DIR_ALIAS.get(costume, costume))
		var beats: Array = []
		var beat_list: Array = BEATS[costume]
		for b: Dictionary in beat_list:
			var objs := {}
			var spec: Dictionary = b["objects"]
			for key in spec.keys():
				var oname := String(key)
				var states: Array = spec[key]
				var rel := "assets/opera/jobs/%s/opera_%s_%s.glb" % [dir_name, dir_name, oname]
				var have := ResourceLoader.exists("res://" + rel)
				if not have:
					total_missing += 1
				objs[oname] = {
					"states": states,
					"path": rel,
					"exists": have,
				}
				total_objects += 1
				total_states += states.size()
			var bname := String(b["beat"])
			var pend: Array = PENDING_BEATS.get(costume, [])
			var is_built: bool = not pend.has(bname)
			if is_built:
				total_built += 1
			else:
				total_pending += 1
			beats.append({
				"beat": bname,
				"gesture": b["gesture"],
				"built": is_built,
				"objects": objs,
			})
		acts[costume] = {
			"career": String(cfg.get("career", "")),
			"name": String(cfg.get("name", "")),
			"engine": String(cfg.get("kind", "")),
			"rescues": String(cfg.get("rescue", "")),
			"gift": String(cfg.get("gift", "")),
			"uses_gift_for": String(cfg.get("uses", "")),
			"beats": beats,
		}
	var manifest := {
		"schema": 1,
		"generated_from": "scripts/probe_art_manifest.gd + OperaHouse.ACTS",
		"acts": acts,
		"totals": {
			"acts": acts.size(),
			"objects": total_objects,
			"states": total_states,
			"missing": total_missing,
			"beats_built": total_built,
			"beats_pending": total_pending,
		},
	}
	var text := JSON.stringify(manifest, "\t", false)
	# a stable digest so codex can tell at a glance whether anything moved
	manifest["fingerprint"] = text.sha256_text().substr(0, 16)
	text = JSON.stringify(manifest, "\t", false)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://audit"))
	var f := FileAccess.open(OUT_PATH, FileAccess.WRITE)
	if f != null:
		f.store_string(text + "\n")
		f.close()
	print("ARTMANIFEST|acts=%d beats=%d/%d built objects=%d states=%d missing=%d fingerprint=%s"
		% [acts.size(), total_built, total_built + total_pending, total_objects,
			total_states, total_missing, String(manifest["fingerprint"])])
	print("ARTMANIFEST|written %s" % OUT_PATH)
	print("ARTMANIFEST|done")
	quit()
