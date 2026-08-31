class_name ChapterTwoCareerSceneAdapter
extends RefCounted
## Data-only Chapter 2 career scene seam.
##
## The Opera room owns one interaction pipeline. Chapter 2 supplies the
## story-specific verbs as validated data, so a director can stage a career
## without adding another career branch to the world or changing save bits.

const VALID_MODES := [
	"tap", "hold", "swipe", "circle", "pourt", "oven", "choice", "lens",
	"pipe", "echo", "timing", "bop", "catch", "candy_sort", "farm_lob",
	"garden_plant", "xray_scan", "paint_reveal", "talk", "clue_board",
	"crown_chest", "ballet_pose",
	"ballet_ribbon", "ballet_twirl", "boxing_guide", "boxing_jab",
	"boxing_guard", "boxing_imp", "boxing_belt", "dance_sequence",
]

const CAREER_ORDER := [
	"chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
	"boxer", "magician", "painter", "astronaut", "racer", "popstar", "nursery",
]

## These are the canonical Chapter 2 beats. `milestone` is a stable hook ID;
## `mode` deliberately names an existing Opera interaction surface.
const PHASE_SETS := {
	"chef": {
		"finale_start": 5,
		"scene_id": "chapter2_chef_cake",
		"phases": [
			{"name": "MIX", "milestone": "mix", "mode": "pourt", "goal": 5.0, "vo": "op_chef_pour", "voice": "Tip the sparkling batter into the bowl!"},
			{"name": "STIR", "milestone": "stir", "mode": "circle", "goal": 2.0, "vo": "op_chef_stir", "voice": "Draw big circles to stir the batter!"},
			{"name": "BAKE", "milestone": "bake", "mode": "oven", "goal": 6.0, "vo": "op_chef_bake", "voice": "Watch for golden, then take the cake out with the mitt!"},
			{"name": "STACK", "milestone": "stack", "mode": "tap", "goal": 3.0, "vo": "op_chef_stack", "voice": "Tap each cake tier to stack the rainbow cake!"},
			{"name": "FROST", "milestone": "frost", "mode": "swipe", "goal": 6.0, "vo": "op_chef_pipe", "voice": "Trace the frosting ribbon across the cake!"},
		],
	},
	"detective": {
		"finale_start": 2,
		"scene_id": "chapter2_detective_candle",
		"phases": [
			{"name": "LENS", "milestone": "lens", "mode": "lens", "goal": 3.0, "vo": "op_detective_lens", "voice": "Sweep the magnifying glass across the painted clues!"},
			{"name": "CASE BOARD", "milestone": "board", "mode": "clue_board", "goal": 3.0, "vo": "op_detective_match", "voice": "Match each glowing clue to the case board!"},
			{"name": "UNLIT CANDLE", "milestone": "unlit_candle_reveal", "reveal": "unlit_candle", "mode": "crown_chest", "visual_context": "crown_chest", "goal": 1.0, "vo": "op_detective_name", "voice": "Tap the unlit candle to reveal the final clue!"},
		],
	},
	"ballerina": {
		"finale_start": 2,
		"scene_id": "chapter2_ballet_party",
		"phases": [
			{"name": "PEARL MIRROR", "milestone": "pose", "mode": "ballet_pose", "goal": 3.0, "vo": "op_ballerina_watch", "voice": "Tap the matching pearl pose!"},
			{"name": "RIBBON TRAIL", "milestone": "ribbon", "mode": "ballet_ribbon", "goal": 6.0, "vo": "op_ballerina_ribbon", "voice": "Guide the pearl along the glowing ribbon current!"},
			{"name": "GRAND TWIRL", "milestone": "twirl", "mode": "ballet_twirl", "goal": 2.0, "vo": "op_ballerina_twirl", "voice": "Turn the pearl around the shell for the grand twirl!"},
		],
	},
	"candymaker": {
		"finale_start": 3,
		"scene_id": "chapter2_candy_workshop",
		"phases": [
			{"name": "COAT", "milestone": "coat", "mode": "pourt", "goal": 5.0, "vo": "op_candymaker_syrup", "voice": "Tip the shiny coat over every candy!"},
			{"name": "SORT", "milestone": "sort", "mode": "candy_sort", "goal": 6.0, "vo": "op_candymaker_sort", "voice": "Drag each candy into its matching shape box!"},
			{"name": "GLAZE", "milestone": "glaze", "mode": "circle", "goal": 2.0, "vo": "op_candymaker_wrap", "voice": "Twist the glossy glaze in circles!"},
			{"name": "PLACE CANDIED STRAWBERRIES", "milestone": "place_candied_strawberries", "mode": "tap", "goal": 5.0, "vo": "op_candymaker_share", "voice": "Place a candied strawberry on each sweet!"},
		],
	},
	"doctor": {
		"finale_start": 3,
		"scene_id": "chapter2_stuffie_surgeon",
		"phases": [
			{"name": "WASH", "milestone": "wash", "mode": "hold", "goal": 3.6, "vo": "op_doctor_wash", "voice": "Hold the bubbly basin to wash your hands!"},
			{"name": "FIND", "milestone": "find", "mode": "choice", "goal": 4.0, "vo": "op_doctor_find", "voice": "Choose the plushy with the glowing ouch!"},
			{"name": "X-RAY", "milestone": "xray", "mode": "xray_scan", "goal": 2.0, "vo": "op_doctor_x_ray", "voice": "Slide the scanner over the plushy!"},
			{"name": "CAST", "milestone": "cast", "mode": "circle", "goal": 2.0, "vo": "op_doctor_cast", "voice": "Draw gentle circles to wrap the soft cast!"},
		],
	},
	"farmer": {
		"finale_start": 3,
		"scene_id": "chapter2_farmer_strawberries",
		"phases": [
			{"name": "GATHER STRAWBERRIES", "milestone": "gather_strawberries", "mode": "tap", "goal": 6.0, "vo": "op_farmer_gather", "voice": "Tap the ripe strawberries to gather them gently!"},
			{"name": "WASH", "milestone": "wash_strawberries", "mode": "hold", "goal": 3.0, "vo": "op_farmer_wash", "voice": "Hold the bubbly stream to wash the strawberries!"},
			{"name": "FILL BASKET", "milestone": "fill_basket", "mode": "tap", "goal": 4.0, "vo": "op_farmer_fill", "voice": "Tap to place each strawberry in the picnic basket!"},
			{"name": "PICNIC", "milestone": "picnic", "mode": "tap", "goal": 3.0, "vo": "op_farmer_picnic", "voice": "Set one berry snack beside every piggy!"},
		],
	},
	"boxer": {
		"finale_start": 3, "scene_id": "chapter2_friendly_bout",
		"phases": [
			{"name": "GLOVE GUIDE", "milestone": "glove_guide", "mode": "boxing_guide", "goal": 2.0, "vo": "op_boxer_work", "voice": "Push each glove toward the glowing mitt!"},
			{"name": "JAB PRACTICE", "milestone": "jab", "mode": "boxing_jab", "goal": 4.0, "vo": "op_boxer_jab", "voice": "Punch each glowing training pad!"},
			{"name": "SOFT GUARD", "milestone": "guard", "mode": "boxing_guard", "goal": 3.0, "vo": "op_boxer_duck", "voice": "Bring a glove into the glowing guard bubble!"},
			{"name": "TITLE IMP", "milestone": "title_imp", "mode": "boxing_imp", "goal": 6.0, "vo": "op_boxer_bell_chase", "voice": "Punch when the bright star opens!"},
			{"name": "BELT", "milestone": "belt", "mode": "boxing_belt", "goal": 1.0, "vo": "op_boxer_belt", "voice": "Punch the glowing championship belt!"},
		],
	},
	"magician": {
		"finale_start": 3, "scene_id": "chapter2_illusion_duel",
		"phases": [
			{"name": "VANISH", "milestone": "vanish", "mode": "hold", "goal": 3.8, "vo": "op_magician_vanish", "voice": "Hold the wand to hide Lamba under a hat!"},
			{"name": "TRACK", "milestone": "track", "mode": "choice", "goal": 5.0, "vo": "op_magician_track", "voice": "Follow the glowing hat through the shuffle!"},
			{"name": "ROPE", "milestone": "rope", "mode": "swipe", "goal": 5.0, "vo": "op_magician_rope", "voice": "Swipe the knotted rope into one long ribbon!"},
			{"name": "CABINET", "milestone": "cabinet", "mode": "swipe", "goal": 1.0, "vo": "op_magician_cabinet", "voice": "Swipe down to open the magic cabinet!"},
			{"name": "PORTAL", "milestone": "portal", "mode": "circle", "goal": 2.0, "vo": "op_magician_portal", "voice": "Draw circles to open the star portal!"},
		],
	},
	"painter": {
		"finale_start": 2, "scene_id": "chapter2_sunrise_paint",
		"phases": [
			{"name": "PAINT", "milestone": "paint", "mode": "paint_reveal", "goal": 1.0, "vo": "op_painter_sketch", "voice": "Paint across the cloudy canvas to reveal the sunrise!"},
			{"name": "STAMPS", "milestone": "stamps", "mode": "tap", "goal": 5.0, "vo": "op_painter_splat", "voice": "Add five bright finishing stamps!"},
			{"name": "GALLERY", "milestone": "gallery", "mode": "choice", "goal": 1.0, "vo": "op_painter_reveal", "voice": "Choose the glowing frame and hang your sunrise!"},
		],
	},
	"astronaut": {
		"finale_start": 2,
		"scene_id": "chapter2_astronaut_rocket",
		"phases": [
			{"name": "BUILD ROCKET", "milestone": "build_rocket", "mode": "pipe", "goal": 3.0, "vo": "op_astronaut_pipes", "voice": "Connect the rocket parts from the tank to the nose!"},
			{"name": "PARK ROCKET", "milestone": "park_rocket", "mode": "swipe", "goal": 5.0, "vo": "op_astronaut_park", "voice": "Swipe the little rocket into its launch bay!"},
			{"name": "PATCH", "milestone": "patch", "mode": "tap", "goal": 5.0, "vo": "op_astronaut_patch", "voice": "Tap every sparkling leak to patch the rocket!"},
			{"name": "LAUNCH", "milestone": "launch", "mode": "hold", "goal": 4.5, "vo": "op_astronaut_launch", "voice": "Hold through the countdown and launch!"},
		],
	},
	"racer": {
		"finale_start": 2, "scene_id": "chapter2_grand_prix",
		"phases": [
			{"name": "TUNE", "milestone": "tune", "mode": "circle", "goal": 1.8, "vo": "op_racer_tune_up", "voice": "Turn the wrench to finish the pit stop!"},
			{"name": "TO THE LINE", "milestone": "to_line", "mode": "swipe", "goal": 5.0, "vo": "op_racer_to_the_line", "voice": "Push the kart to the pearl starting arch!"},
			{"name": "RACE", "milestone": "race", "mode": "circle", "goal": 0.9, "vo": "op_racer_lap_two", "voice": "Loop the loop! Draw big racing circles!"},
		],
	},
	"popstar": {
		"finale_start": 2,
		"scene_id": "chapter2_popstar_rumi",
		"phases": [
			{"name": "SOUND CHECK", "milestone": "sound_check", "mode": "hold", "goal": 3.8, "visual_context": "charge_popstar", "subject": "rumi", "vo": "op_popstar_sound_check", "voice": "Hold the microphone while Rumi checks the rainbow note!"},
			{"name": "STAGE RUMI", "milestone": "stage_rumi", "mode": "choice", "subject": "rumi", "vo": "op_popstar_dance", "voice": "Tap the glowing arrow to stage Rumi with the band!"},
			{"name": "RHYTHM", "milestone": "rhythm", "mode": "echo", "goal": 3.0, "vo": "op_popstar_rhythm", "voice": "Listen to the three stars, then sing their song back!"},
			{"name": "ENCORE", "milestone": "encore", "mode": "circle", "goal": 2.0, "vo": "op_popstar_encore", "voice": "Draw one big encore spin for the crowd!"},
		],
	},
	"nursery": {
		"finale_start": 4, "scene_id": "chapter2_moonbeam_nursery",
		"phases": [
			{"name": "WASH HANDS", "milestone": "wash", "mode": "hold", "goal": 3.4, "vo": "op_nursery_wash", "voice": "Hold the bubbly basin to wash your hands!"},
			{"name": "CATCH BABIES", "milestone": "catch", "mode": "catch", "goal": 5.0, "speaker": "Faron", "vo": "op_nursery_catch", "voice": "Slide the soft cradle under five babies!"},
			{"name": "FEED", "milestone": "feed", "mode": "hold", "goal": 4.0, "speaker": "Faron", "vo": "op_nursery_feed", "voice": "Hold the warm bottle while you feed each baby!"},
			{"name": "BURP", "milestone": "burp", "mode": "tap", "pace": 0.55, "goal": 4.0, "vo": "op_nursery_burp", "voice": "Pat the baby's back gently and slowly!"},
			{"name": "BEDTIME", "milestone": "bedtime", "mode": "swipe", "goal": 3.0, "speaker": "Faron", "vo": "op_nursery_bedtime", "voice": "Swipe each blanket down and tuck every baby in!"},
		],
	},
}

static func _fallback_phase_set(career: String) -> Dictionary:
	return {"finale_start": 0, "scene_id": "chapter2_%s" % career, "phases": []}


static func phase_set(career: String) -> Dictionary:
	var source: Dictionary = PHASE_SETS.get(career, _fallback_phase_set(career)) as Dictionary
	return source.duplicate(true)


static func phase_set_for(career: String) -> Dictionary:
	return phase_set(career)


static func _normalise_phase_set(career: String, phases: Array) -> Array:
	var result: Array = []
	for raw in phases:
		if not raw is Dictionary:
			return []
		var phase: Dictionary = (raw as Dictionary).duplicate(true)
		if not phase.has("milestone"):
			phase["milestone"] = String(phase.get("name", "phase")).to_lower().replace(" ", "_")
		result.append(phase)
	return result


static func validate_phase_overrides(career: String, phases: Array) -> bool:
	if career.is_empty() or phases.is_empty():
		return false
	var seen: Dictionary = {}
	for raw in phases:
		if not raw is Dictionary:
			return false
		var phase: Dictionary = raw as Dictionary
		var name := String(phase.get("name", ""))
		var mode := String(phase.get("mode", ""))
		if name.is_empty() or mode not in VALID_MODES or seen.has(name):
			return false
		if float(phase.get("goal", 0.0)) <= 0.0:
			return false
		seen[name] = true
	return true


static func validate_config_overrides(career: String, overrides: Dictionary) -> bool:
	if overrides.is_empty():
		return true
	if overrides.has("phase_overrides"):
		var phases_variant: Variant = overrides.get("phase_overrides")
		if not phases_variant is Array \
				or not validate_phase_overrides(career, phases_variant as Array):
			return false
	if overrides.has("finale_start"):
		var finale := int(overrides.get("finale_start", -1))
		if finale < 0:
			return false
	if overrides.has("scene_adapter") \
				and not (overrides.get("scene_adapter") is Dictionary):
		return false
	if overrides.get("scene_adapter", {}) is Dictionary:
		var adapter: Dictionary = overrides.get("scene_adapter", {}) as Dictionary
		var adapter_phases: Variant = adapter.get("phase_overrides", adapter.get("phases", null))
		if adapter_phases != null and (not adapter_phases is Array \
				or not validate_phase_overrides(career, adapter_phases as Array)):
			return false
	return true


static func resolve(career: String, overrides: Dictionary = {}) -> Dictionary:
	var source := phase_set(career)
	if overrides.has("phase_overrides"):
		var phases_variant: Variant = overrides.get("phase_overrides")
		if phases_variant is Array and validate_phase_overrides(career, phases_variant as Array):
			source["phases"] = _normalise_phase_set(career, phases_variant as Array)
	if overrides.has("finale_start"):
		source["finale_start"] = int(overrides.get("finale_start", source.get("finale_start", 0)))
	if overrides.has("scene_id"):
		source["scene_id"] = String(overrides.get("scene_id", source.get("scene_id", "")))
	return source


static func adapter_config(career: String, overrides: Dictionary = {}) -> Dictionary:
	var resolved := resolve(career, overrides)
	return {
		"id": String(resolved.get("scene_id", "chapter2_%s" % career)),
		"career": career,
		"finale_start": int(resolved.get("finale_start", 0)),
		"phase_count": (resolved.get("phases", []) as Array).size(),
	}
