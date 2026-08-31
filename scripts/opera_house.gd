class_name OperaHouse
extends Node
## Canvas-only Opera career lifecycle and stable save-bit authority.
##
## The roster deliberately remains a sixteen-slot table. The three retired
## floor finales are inert tombstones so every surviving career keeps the bit
## it has always owned in `opera_stars`.

const RETIRED_ACT_INDICES: Array[int] = [4, 9, 14]
const ChapterTwoAdapter := preload("res://scripts/chapter_two_career_scene_adapter.gd")
const LIVE_ACT_INDICES: Array[int] = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15]
const RETIRED_STAR_MASK := 0x4210
const ACTIVE_STAR_MASK := 0xBDEF
const ALL_STARS := ACTIVE_STAR_MASK
const ACTIVE_ACT_COUNT := 13

const ACTS := [
	{
		"save_bit": 0, "name": "The Castle Bake-Off", "career": "Pastry Chef",
		"costume": "chef", "emoji": "🍰", "story": 1, "type": "show",
		"kind": "order", "music": "opera_chef", "props": "cake", "order": [0, 2, 1, 0, 2], "finale": "stir", "decorate": 4, "imps": 6, "shell": true,
		"rescue": "farmers", "gift": "carrots", "uses": "carrots",
		"voice": "Chef hat on! You and the pastry imp each have a kitchen. Sift, pour, stir, bake, pipe and decorate the brightest celebration cake for the crowd!",
		"win_line": "Roshan's celebration cake wins the Castle Bake-Off!",
		"floor_col": Color(0.72, 0.5, 0.62), "trim": Color(1.0, 0.78, 0.86), "curtain": Color(0.85, 0.3, 0.4),
	},
	{
		"save_bit": 1, "name": "The Two-Detective Mystery", "career": "Detective",
		"costume": "detective", "emoji": "🔍", "story": 1, "type": "show",
		"kind": "sleuth", "music": "opera_detective", "props_n": 12, "clues": 5, "imps": 6, "shell": true,
		"rescue": "stagehands", "gift": "lanterns", "uses": "lanterns",
		"voice": "Detective Roshan and the detective imp are solving the SAME case! Find five clues before the timer; if the imp gets there first, watch the answer and race the remembered mystery again!",
		"win_line": "Case closed! Roshan solved the Two-Detective Mystery!",
		"floor_col": Color(0.42, 0.46, 0.62), "trim": Color(0.72, 0.85, 1.0), "curtain": Color(0.3, 0.35, 0.6),
	},
	{
		"save_bit": 2, "name": "The Mermaid Pearl Ballet Party", "career": "Ballerina",
		"costume": "ballerina", "emoji": "🩰", "story": 1, "type": "show",
		"kind": "echo", "music": "opera_ballerina", "pads": 3, "rounds": [2, 3, 3], "pitch": 0.6,
		"silence_entry_voice": true,
		"rescue": "dancers", "gift": "ribbons", "rescue_imps": 4,
		"voice": "Mermaid ballet party! Hold pearl poses, guide the glowing ribbon, and finish with one beautiful grand twirl!",
		"win_line": "Roshan's pearl-ribbon ballet ends with a beautiful grand twirl!",
		"floor_col": Color(0.62, 0.45, 0.72), "trim": Color(1.0, 0.72, 0.86), "curtain": Color(0.55, 0.3, 0.62),
	},
	{
		"save_bit": 3, "name": "The Candy Workshop Cup", "career": "Candy Maker",
		"costume": "candymaker", "emoji": "🍬", "story": 1, "type": "show",
		"kind": "press", "music": "opera_candymaker", "candies": 9,
		"rescue": "sweet-shop mice", "gift": "sugar", "rescue_imps": 4,
		"voice": "Candy Maker Roshan! Mix, sort, wrap and load your parade candies while the candy imp runs the rival workshop!",
		"win_line": "Roshan's smiling sweets win the Candy Workshop Cup!",
		"floor_col": Color(0.78, 0.5, 0.58), "trim": Color(1.0, 0.75, 0.82), "curtain": Color(0.82, 0.35, 0.5),
	},
	{"save_bit": 4, "retired": true},
	{
		"save_bit": 5, "name": "The Stuffie Surgeon Relay", "career": "Stuffie Surgeon",
		"costume": "doctor", "emoji": "🩺", "story": 2, "type": "show",
		"kind": "doctor", "music": "opera_doctor", "imps": 6, "shell": true, "patients": 4,
		"voice": "Stuffie Surgeon Roshan and the surgeon imp each have a plushy-care station. Find each ouch, check the X-ray and wrap every soft cast with care!",
		"win_line": "Every stuffie is wiggling again — Roshan wins the surgeon relay!",
		"floor_col": Color(0.75, 0.82, 0.9), "trim": Color(0.7, 0.95, 1.0), "curtain": Color(0.4, 0.55, 0.75),
	},
	{
		"save_bit": 6, "name": "The Piggy Picnic Challenge", "career": "Farmer",
		"costume": "farmer", "emoji": "🐷", "story": 2, "type": "show",
		"kind": "scroll", "music": "opera_farmer", "piggies": 12,
		"rescue": "farmers", "gift": "carrots", "rescue_imps": 5,
		"voice": "Farmer Roshan! Plant, feed and guide your piggies while the farmer imp tends the next meadow lane. Make the happiest herd!",
		"win_line": "Roshan's happy herd wins the Piggy Picnic Challenge!",
		"floor_col": Color(0.55, 0.75, 0.5), "trim": Color(0.95, 0.9, 0.55), "curtain": Color(0.4, 0.6, 0.35),
	},
	{
		"save_bit": 7, "name": "The Friendly Championship Bout", "career": "Boxer",
		"costume": "boxer", "emoji": "🥊", "story": 2, "type": "show",
		"kind": "box", "music": "opera_boxer", "rounds": [4, 5, 6], "warmup": 5,
		"rescue": "the ring crew", "gift": "gloves", "rescue_imps": 4,
		"voice": "Boxer Roshan, into the ring! Warm up, then fight one padded boxer imp for three friendly rounds. Punch on the beat and duck the counter-glove!",
		"win_line": "And the winner of the friendly championship is... ROSHAN!",
		"floor_col": Color(0.55, 0.32, 0.3), "trim": Color(1.0, 0.82, 0.45), "curtain": Color(0.72, 0.2, 0.24),
	},
	{
		"save_bit": 8, "name": "The Grand Illusion Duel", "career": "Magician",
		"costume": "magician", "emoji": "🎩", "story": 2, "type": "show",
		"kind": "shuffle", "music": "opera_magician", "rounds": 6, "imps": 5, "shell": true,
		"rescue": "usher crabs", "gift": "silk scarves", "uses": "silk scarves",
		"voice": "Abracadabra! Face the magician imp in a whole illusion duel: hide and track the bunny-fish, melt the rope, open the cabinet and charge the giant star portal!",
		"win_line": "Roshan's star portal wins the Grand Illusion Duel!",
		"floor_col": Color(0.36, 0.3, 0.55), "trim": Color(0.85, 0.7, 1.0), "curtain": Color(0.4, 0.22, 0.6),
	},
	{"save_bit": 9, "retired": true},
	{
		"save_bit": 10, "name": "The Sunrise Paint-Off", "career": "Painter",
		"costume": "painter", "emoji": "🎨", "story": 3, "type": "show",
		"kind": "paint", "music": "opera_painter", "props": "paint", "order": [2, 0, 1, 2, 0], "flow": "carry_paint", "decorate": 5, "decorate_theme": "splatter", "imps": 5, "shell": true,
		"rescue": "painter", "gift": "paints", "uses": "paints",
		"voice": "Painter Roshan! You and the painter imp have matching easels. Trace, fill and paint your sunrise before the gallery reveal!",
		"win_line": "Roshan's sunrise wins the paint-off and hangs in the gallery!",
		"floor_col": Color(0.65, 0.5, 0.42), "trim": Color(1.0, 0.82, 0.55), "curtain": Color(0.75, 0.42, 0.3),
	},
	{
		"save_bit": 11, "name": "The Rocket Repair Race", "career": "Astronaut Engineer",
		"costume": "astronaut", "emoji": "🚀", "story": 3, "type": "show",
		"kind": "fix", "music": "opera_astronaut", "imps": 6, "shell": true,
		"rescue": "bubble engineers", "gift": "spare pipes", "uses": "spare pipes",
		"voice": "Astronaut Engineer Roshan! Route your bubble pipes while the astronaut imp repairs the rival launch lane, then spin the valve and launch first!",
		"win_line": "Roshan routes the bubbles and wins the Rocket Repair Race!",
		"floor_col": Color(0.3, 0.34, 0.55), "trim": Color(0.7, 0.9, 1.0), "curtain": Color(0.22, 0.26, 0.5),
	},
	{
		"save_bit": 12, "name": "The Opera Grand Prix", "career": "Racecar Driver",
		"costume": "racer", "emoji": "🏎", "story": 3, "type": "show",
		"kind": "race", "music": "opera_racer", "laps": 2,
		"rescue": "pit crew", "gift": "spare wheels", "rescue_imps": 4,
		"voice": "Racecar Driver Roshan! TWO laps against the helmeted rival imp — steer, grab the zoom strips and tap TURBO to fly!",
		"win_line": "Roshan takes the Opera Grand Prix as the audience waves checkered flags!",
		"floor_col": Color(0.4, 0.4, 0.48), "trim": Color(1.0, 0.95, 0.95), "curtain": Color(0.85, 0.25, 0.3),
	},
	{
		"save_bit": 13, "name": "The Starlight Sound-Off", "career": "Pop Star",
		"costume": "popstar", "emoji": "🎤", "story": 3, "type": "show",
		"kind": "dance", "music": "opera_popstar", "rescue": "the band", "gift": "instruments", "rescue_imps": 4,
		"voice": "Pop Star Roshan! The pop-star imp has the other microphone. Dance the floating arrows and lift the crowd higher with every rainbow phrase!",
		"win_line": "Roshan wins the Starlight Sound-Off and the crowd sings along!",
		"floor_col": Color(0.5, 0.3, 0.6), "trim": Color(1.0, 0.7, 0.95), "curtain": Color(0.45, 0.2, 0.55),
	},
	{"save_bit": 14, "retired": true},
	{
		"save_bit": 15, "name": "The Moonbeam Nursery", "career": "Nursery Nurse",
		"costume": "nursery", "emoji": "🍼", "story": 3, "type": "show", "kind": "nursery",
		"music": "opera_nursery",
		"voice": "Nursery Nurse Roshan! Work with Nurse Faron to catch the babies, feed them, burp them and tuck every little one into bed!",
		"win_line": "Roshan and Faron tucked every cozy baby into the Moonbeam Nursery!",
		"floor_col": Color(0.45, 0.68, 0.66), "trim": Color(1.0, 0.82, 0.70), "curtain": Color(0.48, 0.38, 0.68),
	},
]

var m: ReefMain
var finish_cb: Callable
var state := "idle"
var act: OperaAct = null
var act_index := -1
var run_context: Dictionary = {}
var plot_context := ""
var story_mode := false
## Chapter 2's four opening lessons teach a single verb and grant a skill.
## This flag is deliberately independent from run_context: plot performances
## (such as the Stuffie Ballet) remain full scored Opera runs.
var tutorial_mode := false


static func is_live_act_index(index: int) -> bool:
	return index >= 0 and index < ACTS.size() \
		and LIVE_ACT_INDICES.has(index) \
		and not bool((ACTS[index] as Dictionary).get("retired", false))


static func live_star_count(star_mask: int) -> int:
	var total := 0
	for index: int in LIVE_ACT_INDICES:
		if (star_mask & (1 << index)) != 0:
			total += 1
	return total


static func has_all_live_stars(star_mask: int) -> bool:
	return (star_mask & ACTIVE_STAR_MASK) == ACTIVE_STAR_MASK


func start(main: ReefMain, index: int, done_cb: Callable,
		config_overrides: Dictionary = {}, run_context: Dictionary = {}) -> bool:
	if state != "idle" or not is_live_act_index(index):
		push_error("OperaHouse: retired or unknown Opera slot %d" % index)
		return false
	var next_config: Dictionary = (ACTS[index] as Dictionary).duplicate(true)
	if not ChapterTwoAdapter.validate_config_overrides(
		String(next_config.get("costume", "")), config_overrides):
		push_error("OperaHouse: invalid Chapter 2 config override at slot %d" % index)
		return false
	next_config.merge(config_overrides.duplicate(true), true)
	if not run_context.is_empty():
		next_config["run_context"] = run_context.duplicate(true)
	story_mode = String(next_config.get("reward_policy", "")) == "chapter2_story"
	if story_mode:
		# Story careers use the Chapter 2 phase catalog and completion authority;
		# they are not tutorial truncations and never mint Opera freeplay stars.
		next_config["chapter2_tutorial"] = false
		var scene_config := ChapterTwoAdapter.adapter_config(
			String(next_config.get("costume", "")), config_overrides)
		var scene_adapter_value: Variant = config_overrides.get(
			"scene_adapter", null)
		if scene_adapter_value is Dictionary:
			# Keep caller-supplied bindings/hooks while filling absent story fields
			# from the data catalog. Nested phase overrides are validated and
			# resolved by the adapter before the world receives this config.
			var scene_adapter_dictionary: Dictionary = scene_adapter_value
			scene_config.merge(
				scene_adapter_dictionary.duplicate(true),
				true)
		next_config["scene_adapter"] = scene_config
		next_config["chapter2_scene"] = String(scene_config.get("backdrop", ""))
		var story_run_context: Dictionary = {}
		var story_context_value: Variant = next_config.get("run_context", null)
		if story_context_value is Dictionary:
			var story_context_dictionary: Dictionary = story_context_value
			story_run_context = story_context_dictionary.duplicate(true)
		story_run_context["chapter"] = "chapter2"
		story_run_context["reward_policy"] = "chapter2_story"
		next_config["run_context"] = story_run_context
		if main.chapter2_is_active():
			next_config["chapter2_resume_phase_index"] = \
				main._chapter_two_ref().resume_phase_index_for_act(index)
	if not OperaAct.supports_config(next_config):
		push_error("OperaHouse: invalid Canvas career mapping at slot %d" % index)
		return false
	m = main
	finish_cb = done_cb
	act_index = index
	plot_context = String(next_config.get("chapter2_context", ""))
	self.run_context = {}
	var configured_context_value: Variant = next_config.get("run_context", null)
	if configured_context_value is Dictionary:
		var configured_context_dictionary: Dictionary = configured_context_value
		self.run_context = configured_context_dictionary.duplicate(true)
	if not run_context.is_empty():
		self.run_context.merge(run_context.duplicate(true), true)
	tutorial_mode = bool(next_config.get("chapter2_tutorial", false))
	state = "playing"
	next_config["act_tag"] = String(next_config.get("name", "")) + "  "
	act = OperaAct.new()
	add_child(act)
	if not act.start(m, next_config, Callable(self, "_act_won")):
		act.queue_free()
		act = null
		act_index = -1
		state = "idle"
		finish_cb = Callable()
		push_error("OperaHouse: slot %d failed to start its Canvas career" % index)
		return false
	return true


func _act_won() -> void:
	var finished := act_index
	act = null
	act_index = -1
	if not is_live_act_index(finished):
		push_error("OperaHouse: win callback had no live Opera slot")
		_finish(false)
		return
	if tutorial_mode or story_mode:
		# Opening Chapter 2 lessons are skill hooks, not Opera performances:
		# preserve every normal Opera reward and progress counter untouched.
		m.chapter2_on_opera_completed(finished, plot_context)
		m._write_save()
		_finish(true)
		return
	var bit := 1 << finished
	var first_time := (m.opera_stars & bit) == 0
	m.opera_stars |= bit
	m.pearl_count += 3 if first_time else 1
	m.opera_progress = live_star_count(m.opera_stars)
	m.chapter2_on_opera_completed(finished, plot_context)
	if has_all_live_stars(m.opera_stars) and not m.opera_done:
		m.opera_done = true
		m.pearl_count += 50
		m.award_sticker("showtime")
	m._write_save()
	m._update_hud()
	_finish(true)


func _leave_early() -> void:
	if state == "done" or state == "idle":
		return
	if act != null:
		var current_act := act
		current_act.cancel()
		# A won act completes synchronously from cancel(), so keep its stable
		# index available until _act_won() has committed the reward. A still-
		# playing act has no callback and is cleared here after cancellation.
		if state == "done":
			return
		if act == current_act:
			act = null
			act_index = -1
	_finish(false)


func _finish(completed: bool) -> void:
	if state == "done":
		return
	state = "done"
	var completed_cb := finish_cb
	finish_cb = Callable()
	if completed_cb.is_valid():
		completed_cb.call(completed)
	queue_free()


func action_label() -> String:
	return act.action_label() if act != null else "PLAY"
