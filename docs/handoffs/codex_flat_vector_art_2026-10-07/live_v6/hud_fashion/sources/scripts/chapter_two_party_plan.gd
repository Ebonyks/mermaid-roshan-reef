class_name ChapterTwoPartyPlan
extends RefCounted

## Pure-data contract for the eight live Opera careers that prepare the
## birthday party. The save bit is the existing Opera bit; this table never
## repurposes retired slots or legacy `opera_stars` state.

const LIVE_CAREERS: Array[Dictionary] = [
	{"act_index": 6, "career": "farmer", "room": "dining_room", "scene_id": "sky_lagoon_farmer", "location_label": "Sky Lagoon strawberry grove", "route_label": "Dining Room berry doorway", "function": "gather Sky Lagoon strawberries for the cake", "piece": "strawberries", "lawn_nodes": ["Cake"], "seed": "chapter3_garden_path"},
	{"act_index": 0, "career": "chef", "room": "kitchen", "function": "bake the gigantic strawberry birthday cake", "piece": "birthday_cake", "lawn_nodes": ["Cake"], "seed": "chapter3_warm_cake"},
	{"act_index": 3, "career": "candy_maker", "room": "kitchen", "function": "finish the cake with candied strawberries", "piece": "candied_strawberries", "lawn_nodes": ["Cake"], "seed": "chapter3_sweet_trail"},
	{"act_index": 10, "career": "painter", "room": "craft_room", "function": "paint the Main Hall birthday banner", "piece": "party_banner", "lawn_nodes": ["Banner"], "seed": "chapter3_sunrise_sign"},
	{"act_index": 2, "career": "ballerina", "room": "playroom", "function": "teach the stuffies to dance and play together", "piece": "stuffie_dance", "lawn_nodes": ["StuffieCat", "StuffieBunny", "MusicBox"], "seed": "chapter3_ribbon_step"},
	{"act_index": 13, "career": "popstar", "room": "opera_hall", "function": "sound-check the birthday song with Rumi", "piece": "party_song", "lawn_nodes": ["Rumi", "PartyMicrophone"], "seed": "chapter3_echo_song"},
	{"act_index": 11, "career": "astronaut", "room": "mermaid_pool", "function": "build the little rocket that lights the rainbow candle", "piece": "candle_lighting_rocket", "lawn_nodes": ["Rocket"], "seed": "chapter3_north_star"},
	{"act_index": 1, "career": "detective", "room": "library", "function": "find the last missing candle", "piece": "rainbow_candle", "lawn_nodes": ["Candle"], "seed": "chapter3_storybook_clue"},
]

const ALL_PARTY_MASK := 0x2C4F
const GUIDE_ORDER: Array[int] = [6, 0, 3, 10, 2, 13, 11, 1]

static func all_act_indices() -> Array[int]:
	var result: Array[int] = []
	for entry: Dictionary in LIVE_CAREERS:
		result.append(int(entry["act_index"]))
	return result

static func entry_for_act(act_index: int) -> Dictionary:
	for entry: Dictionary in LIVE_CAREERS:
		if int(entry["act_index"]) == act_index:
			return entry.duplicate(true)
	return {}

static func is_live_act(act_index: int) -> bool:
	return act_index >= 0 and act_index < 16 \
		and (ALL_PARTY_MASK & (1 << act_index)) != 0

static func next_incomplete_entry(piece_mask: int) -> Dictionary:
	for act_index: int in GUIDE_ORDER:
		if (piece_mask & (1 << act_index)) == 0:
			return entry_for_act(act_index)
	return {}
