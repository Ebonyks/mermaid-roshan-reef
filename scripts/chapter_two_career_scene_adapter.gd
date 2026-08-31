class_name ChapterTwoCareerSceneAdapter
extends RefCounted
## Data-only Chapter 2 Opera scene seam. Each phase reuses a shipped
## interaction mode; the world remains the single input/score owner.

const VALID_MODES := [
	"tap", "hold", "swipe", "circle", "pourt", "oven", "choice", "lens",
	"pipe", "echo", "timing", "bop", "catch", "candy_sort", "farm_lob",
	"garden_plant", "xray_scan", "paint_reveal", "talk", "clue_board",
	"crown_chest", "ballet_pose", "ballet_ribbon", "ballet_twirl",
	"boxing_guide", "boxing_jab", "boxing_guard", "boxing_imp", "boxing_belt",
	]

const CAREER_ORDER := [
	"chef", "detective", "ballerina", "candymaker", "doctor", "farmer",
	"boxer", "magician", "painter", "astronaut", "racer", "popstar", "nursery",
]

const PHASE_SETS := {
	"chef": {"finale_start": 5, "scene_id": "chapter2_chef_cake", "backdrop": "chapter2_chef_cake", "cake_asset": "res://assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png", "strawberry_asset": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "prop": "res://assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png", "phases": [
		{"name": "MIX", "milestone": "mix", "mode": "pourt", "goal": 5.0, "vo": "op_chef_pour", "voice": "Tip the sparkling batter into the bowl!"},
		{"name": "STIR", "milestone": "stir", "mode": "circle", "goal": 2.0, "vo": "op_chef_stir", "voice": "Draw big circles to stir the batter!"},
		{"name": "BAKE", "milestone": "bake", "mode": "oven", "goal": 6.0, "vo": "op_chef_bake", "voice": "Watch for golden, then take the cake out with the mitt!"},
		{"name": "STACK", "milestone": "stack", "mode": "tap", "goal": 3.0, "vo": "", "voice": "Tap each cake tier to stack the rainbow cake!"},
		{"name": "FROST", "milestone": "frost", "mode": "swipe", "goal": 6.0, "vo": "op_chef_pipe", "voice": "Trace the frosting ribbon across the cake!"},
	]},
	"detective": {"finale_start": 2, "scene_id": "magic_storybook", "story_object": "magic_storybook", "backdrop": "magic_storybook", "prop": "res://assets/opera/worlds/props/goal_detective.png", "mechanic": "unlit_rainbow_candle", "legacy_mechanic": "crown_chest", "phases": [
		{"name": "LENS", "milestone": "storybook_lens", "mode": "lens", "goal": 3.0, "vo": "op_detective_lens", "voice": "Sweep the lens across the magic storybook clues!"},
		{"name": "STORYBOOK BOARD", "milestone": "storybook_board", "mode": "tap", "widget_context": "storybook_board", "goal": 3.0, "vo": "op_detective_match", "voice": "Tap each glowing storybook clue on the board!"},
		{"name": "UNLIT RAINBOW CANDLE", "milestone": "unlit_rainbow_candle_reveal", "reveal": "unlit_rainbow_candle", "mode": "tap", "widget_context": "unlit_rainbow_candle", "mechanic": "unlit_rainbow_candle", "goal": 1.0, "vo": "", "voice": "Tap the unlit rainbow candle to reveal the final clue!"},
	]},
	"ballerina": {"finale_start": 2, "scene_id": "stuffie_room", "backdrop": "stuffie_room", "prop": "res://assets/flats/castle/rooms/room_playroom_item_stuffie_nook.png", "phases": [
		{"name": "STUFFIES MIRROR", "milestone": "stuffies_mirror", "mode": "ballet_pose", "subject": "stuffies", "vo": "", "goal": 3.0, "voice": "Tap the matching pose as the stuffies mirror Roshan!"},
		{"name": "STUFFIES TWIRL", "milestone": "stuffies_twirling", "mode": "ballet_ribbon", "subject": "stuffies", "vo": "op_ballerina_ribbon", "goal": 6.0, "voice": "Guide the ribbon while the stuffies twirl along!"},
		{"name": "STUFFIES BOW", "milestone": "stuffies_bow", "mode": "ballet_twirl", "subject": "stuffies", "vo": "op_ballerina_twirl", "goal": 2.0, "voice": "Take one grand twirl, then bow with the stuffies!"},
	]},
	"candymaker": {"finale_start": 3, "scene_id": "strawberry_cake_workshop", "backdrop": "strawberry_cake_workshop", "strawberry_asset": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "cake_asset": "res://assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png", "prop": "res://assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png", "phases": [
		{"name": "COAT STRAWBERRIES", "milestone": "coat_strawberries", "mode": "pourt", "widget_context": "pour_candymaker", "ingredient_path": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "goal": 5.0, "vo": "", "voice": "Tip the shiny coat over the strawberries!"},
		{"name": "SORT STRAWBERRIES", "milestone": "sort_strawberries", "mode": "candy_sort", "widget_context": "lanes_candymaker", "ingredient_path": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "goal": 6.0, "vo": "", "voice": "Sort the same strawberries by their matching color!"},
		{"name": "GLAZE STRAWBERRIES", "milestone": "glaze_strawberries", "mode": "circle", "widget_context": "crank_candymaker", "ingredient_path": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "goal": 2.0, "vo": "", "voice": "Twist the glaze around each strawberry!"},
		{"name": "PLACE ON CAKE", "milestone": "place_candied_strawberries", "mode": "tap", "widget_context": "target_candymaker", "ingredient_path": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "prop": "res://assets/chapter2/birthday/chapter2_grand_candied_strawberry_cake.png", "goal": 5.0, "vo": "", "voice": "Place the candied strawberries on the actual cake!"},
	]},
	"doctor": {"finale_start": 3, "scene_id": "chapter2_stuffie_surgeon", "phases": [
		{"name": "WASH", "milestone": "wash", "mode": "hold", "goal": 3.6, "vo": "op_doctor_wash", "voice": "Hold the bubbly basin to wash your hands!"},
		{"name": "FIND", "milestone": "find", "mode": "choice", "goal": 4.0, "vo": "op_doctor_find", "voice": "Choose the plushy with the glowing ouch!"},
		{"name": "X-RAY", "milestone": "xray", "mode": "xray_scan", "goal": 2.0, "vo": "op_doctor_x_ray", "voice": "Slide the scanner over the plushy!"},
		{"name": "CAST", "milestone": "cast", "mode": "circle", "goal": 2.0, "vo": "op_doctor_cast", "voice": "Draw gentle circles to wrap the soft cast!"},
	]},
	"farmer": {"finale_start": 2, "scene_id": "chapter2_farmer_strawberries", "backdrop": "sky_lagoon_farmer", "strawberry_asset": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "delivery": "kitchen", "prop": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "phases": [
		{"name": "GATHER STRAWBERRIES", "milestone": "gather_strawberries", "mode": "tap", "widget": "", "widget_context": "", "piece_path": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "goal": 5.0, "vo": "", "voice": "Gather exactly five ripe Sky Lagoon strawberries!"},
		{"name": "FILL BASKET", "milestone": "fill_basket", "mode": "tap", "widget": "", "widget_context": "", "piece_path": "res://assets/chapter2/birthday/sky_lagoon_strawberry_cluster.png", "goal": 5.0, "vo": "", "voice": "Load all five strawberries into the basket!"},
		{"name": "DELIVER TO KITCHEN", "milestone": "deliver_to_kitchen", "mode": "swipe", "widget_context": "push_farmer", "goal": 6.0, "vo": "", "voice": "Swipe the full basket all the way to the kitchen!"},
	]},
	"boxer": {"finale_start": 3, "scene_id": "chapter2_friendly_bout", "phases": []},
	"magician": {"finale_start": 3, "scene_id": "chapter2_illusion_duel", "phases": []},
	"painter": {"finale_start": 3, "scene_id": "main_hall_birthday_banner", "backdrop": "main_hall_birthday_banner", "destination": "main_hall", "persistent_prop": true, "prop": "res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png", "phases": [
		{"name": "PAINT", "milestone": "paint_banner", "subject": "birthday_banner", "mode": "paint_reveal", "widget_context": "trace_painter", "prop": "res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png", "goal": 1.0, "vo": "", "voice": "Paint the birthday banner for Main Hall!"},
		{"name": "STAMP", "milestone": "stamp_banner", "subject": "birthday_banner", "mode": "tap", "widget_context": "target_painter", "prop": "res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png", "goal": 5.0, "vo": "", "voice": "Stamp bright birthday stars on the banner!"},
		{"name": "HANG", "milestone": "hang_banner", "subject": "birthday_banner", "mode": "choice", "widget_context": "lanes_painter", "prop": "res://assets/flats/castle/logo_studio_v2/castle_banner_rainbow.png", "goal": 1.0, "vo": "", "voice": "Choose the Main Hall spot and hang the birthday banner!"},
	]},
	"astronaut": {"finale_start": 4, "scene_id": "chapter2_astronaut_rocket", "backdrop": "chapter2_astronaut_rocket", "rocket_state": "parked_ready_unlaunched", "prop": "res://assets/opera/worlds/props/goal_astronaut.png", "phases": [
		{"name": "BUILD ROCKET", "milestone": "build_rocket", "mode": "pipe", "goal": 3.0, "vo": "", "voice": "Connect the rocket parts from the tank to the nose!"},
		{"name": "PATCH", "milestone": "patch", "mode": "tap", "goal": 5.0, "vo": "op_astronaut_patch", "voice": "Tap every sparkling leak to patch the rocket!"},
		{"name": "VALVE", "milestone": "valve", "mode": "circle", "goal": 1.8, "vo": "op_astronaut_valve", "voice": "Turn the launch valve, but keep the rocket parked!"},
		{"name": "READY PARK", "milestone": "ready_park", "mode": "swipe", "widget_context": "push_racer", "rocket_state": "parked_ready_unlaunched", "goal": 5.0, "vo": "", "voice": "Park the repaired rocket and leave it ready for later!"},
	]},
	"racer": {"finale_start": 2, "scene_id": "chapter2_grand_prix", "phases": []},
	"popstar": {"finale_start": 2, "scene_id": "chapter2_popstar_rumi", "backdrop": "chapter2_popstar_rumi", "phases": [
		{"name": "SOUND CHECK", "milestone": "sound_check", "mode": "hold", "goal": 3.8, "visual_context": "charge_popstar", "subject": "rumi", "vo": "op_popstar_sound_check", "voice": "Hold the microphone while Rumi checks the rainbow note!"},
		{"name": "STAGE RUMI", "milestone": "stage_rumi", "mode": "choice", "subject": "rumi", "vo": "op_popstar_dance", "goal": 3.0, "voice": "Tap the glowing arrow to stage Rumi with the band!"},
		{"name": "RHYTHM", "milestone": "rhythm", "mode": "echo", "goal": 3.0, "vo": "", "voice": "Listen to the three stars, then sing their song back!"},
		{"name": "ENCORE", "milestone": "encore", "mode": "circle", "goal": 2.0, "vo": "op_popstar_encore", "voice": "Draw one big encore spin for the crowd!"},
	]},
	"nursery": {"finale_start": 4, "scene_id": "chapter2_moonbeam_nursery", "phases": []},
}

static func phase_set(career: String) -> Dictionary:
	var fallback := {"finale_start": 0, "scene_id": "chapter2_%s" % career, "phases": []}
	return (PHASE_SETS.get(career, fallback) as Dictionary).duplicate(true)

static func phase_set_for(career: String) -> Dictionary:
	return phase_set(career)

static func validate_phase_overrides(career: String, phases: Array) -> bool:
	if career.is_empty() or phases.is_empty():
		return false
	var seen: Dictionary = {}
	for raw in phases:
		if not raw is Dictionary:
			return false
		var phase: Dictionary = raw as Dictionary
		var name := String(phase.get("name", ""))
		if name.is_empty() or seen.has(name) \
				or String(phase.get("mode", "")) not in VALID_MODES \
				or float(phase.get("goal", 0.0)) <= 0.0:
			return false
		seen[name] = true
	return true

static func validate_config_overrides(career: String, overrides: Dictionary) -> bool:
	if overrides.has("phase_overrides"):
		var phases: Variant = overrides.get("phase_overrides")
		if not phases is Array or not validate_phase_overrides(career, phases as Array):
			return false
	if overrides.has("scene_adapter") and overrides.get("scene_adapter") is Dictionary:
		var adapter := overrides.get("scene_adapter") as Dictionary
		var nested_phases: Variant = adapter.get(
				"phase_overrides", adapter.get("phases", null))
		if nested_phases != null and (not nested_phases is Array
				or not validate_phase_overrides(career, nested_phases as Array)):
			return false
	if overrides.has("finale_start") and int(overrides.get("finale_start", -1)) < 0:
		return false
	if overrides.has("scene_adapter") and not overrides.get("scene_adapter") is Dictionary:
		return false
	return true

static func resolve(career: String, overrides: Dictionary = {}) -> Dictionary:
	var resolved := phase_set(career)
	var phase_override: Variant = overrides.get("phase_overrides", null)
	var raw_adapter: Variant = overrides.get("scene_adapter", {})
	if phase_override == null and raw_adapter is Dictionary:
		var adapter := raw_adapter as Dictionary
		phase_override = adapter.get("phase_overrides", adapter.get("phases", null))
	if phase_override is Array and validate_phase_overrides(career, phase_override as Array):
		resolved["phases"] = (phase_override as Array).duplicate(true)
	if raw_adapter is Dictionary:
		var adapter := raw_adapter as Dictionary
		for key: String in ["scene_id", "id", "backdrop", "prop", "widget",
				"story_object", "mechanic", "strawberry_asset", "cake_asset",
				"delivery", "destination", "persistent_prop", "rocket_state"]:
			if adapter.has(key):
				resolved[key] = adapter.get(key)
	if overrides.has("finale_start"):
		resolved["finale_start"] = int(overrides.get("finale_start", 0))
	if overrides.has("scene_id"):
		resolved["scene_id"] = String(overrides.get("scene_id", resolved.get("scene_id", "")))
	return resolved

static func adapter_config(career: String, overrides: Dictionary = {}) -> Dictionary:
	var resolved := resolve(career, overrides)
	return {"id": String(resolved.get("scene_id", "chapter2_%s" % career)),
		"career": career, "backdrop": String(resolved.get("backdrop", career)),
		"prop": String(resolved.get("prop", "")),
		"widget": String(resolved.get("widget", "")),
		"story_object": String(resolved.get("story_object", "")),
		"mechanic": String(resolved.get("mechanic", "")),
		"strawberry_asset": String(resolved.get("strawberry_asset", "")),
		"cake_asset": String(resolved.get("cake_asset", "")),
		"delivery": String(resolved.get("delivery", "")),
		"destination": String(resolved.get("destination", "")),
		"persistent_prop": bool(resolved.get("persistent_prop", false)),
		"rocket_state": String(resolved.get("rocket_state", "")),
		"finale_start": int(resolved.get("finale_start", 0)),
		"phase_count": (resolved.get("phases", []) as Array).size()}
