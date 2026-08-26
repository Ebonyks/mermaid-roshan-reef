class_name CastleDoorLanguage
extends RefCounted
## Pure four-state vocabulary for Pearl Castle routes.
##
## Reachability and visuals are resolved together. During Act One, the existing
## DayOneDirector is the sequence owner; this class translates its one current
## destination into the one persistent highlight allowed in the castle.

const BLOCKED := "blocked"
const OPEN := "open"
const BONUS := "bonus"
const PLOT := "plot"

const MAIN_HALL_ID := "main_hall"
const ROYAL_HALL_ID := "__royal_hall"
const ACT_ONE_DESTINATIONS: Array[String] = [
	"bubble_bath",
	"mermaid_pool",
	"playroom",
	"craft_room",
]
const CASTLE_DESTINATIONS: Array[String] = [
	MAIN_HALL_ID,
	"family_gallery",
	"opera_hall",
	"kitchen",
	"library",
	"playroom",
	"craft_room",
	"mermaid_pool",
	"bubble_bath",
	"dining_room",
	"royal_bedroom",
	"sleepover_bedroom",
	"movie_lounge",
	ROYAL_HALL_ID,
]


static func resolve_act_one(destination_id: String,
		current_destination_id: String, completed_destination_ids: Array[String],
		boss_door_ready: bool, active_kind: String = PLOT) -> String:
	if not CASTLE_DESTINATIONS.has(destination_id):
		return BLOCKED
	if destination_id == MAIN_HALL_ID:
		return OPEN
	if destination_id == ROYAL_HALL_ID:
		return PLOT if boss_door_ready else BLOCKED
	if not ACT_ONE_DESTINATIONS.has(destination_id):
		return BLOCKED
	if completed_destination_ids.has(destination_id):
		return OPEN
	if destination_id == current_destination_id:
		return BONUS if active_kind == BONUS else PLOT
	return BLOCKED


static func resolve_free_play(destination_id: String,
		royal_plot_available: bool) -> String:
	if not CASTLE_DESTINATIONS.has(destination_id):
		return BLOCKED
	if destination_id == ROYAL_HALL_ID:
		return PLOT if royal_plot_available else BLOCKED
	return OPEN


static func active_highlight_id(current_destination_id: String,
		boss_door_ready: bool) -> String:
	if boss_door_ready:
		return ROYAL_HALL_ID
	if ACT_ONE_DESTINATIONS.has(current_destination_id):
		return current_destination_id
	return ""


static func allows_travel(state: String) -> bool:
	return state == OPEN or state == BONUS or state == PLOT


static func is_highlighted(state: String) -> bool:
	return state == BONUS or state == PLOT


static func normalize(state: String) -> String:
	if state == OPEN or state == BONUS or state == PLOT:
		return state
	return BLOCKED


static func child_meaning(state: String) -> String:
	match normalize(state):
		OPEN:
			return "You may visit. Nothing urgent is waiting."
		BONUS:
			return "You may visit. A bonus is waiting."
		PLOT:
			return "Go here next to continue the story."
		_:
			return "This route is resting for now."
