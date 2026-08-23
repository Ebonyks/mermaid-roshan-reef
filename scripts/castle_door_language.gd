class_name CastleDoorLanguage
extends RefCounted
# One non-reading navigation vocabulary for every Pearl Castle route.
# State comes only from existing saved progression; the language adds no save
# keys and therefore cannot strand an older save behind a new lock.

const BLOCKED := "blocked"
const OPEN := "open"
const BONUS := "bonus"
const PLOT := "plot"

const ROYAL_HALL_ID := "__royal_hall"
const FIRST_VISIT_OPEN_ROOMS: Array[String] = [
	"kitchen",
	"library",
	"playroom",
]
const CASTLE_DESTINATIONS: Array[String] = [
	"main_hall",
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


static func resolve(destination_id: String, crown_awarded: bool,
		playroom_bonus_available: bool, royal_plot_available: bool) -> String:
	# Unknown or retired destinations fail closed. This also prevents an old,
	# direct elevator tuple from becoming a route around Act One sequencing.
	if not CASTLE_DESTINATIONS.has(destination_id):
		return BLOCKED
	if destination_id == "main_hall":
		return OPEN
	if destination_id == ROYAL_HALL_ID:
		return PLOT if royal_plot_available else BLOCKED
	if not crown_awarded and not FIRST_VISIT_OPEN_ROOMS.has(destination_id):
		return BLOCKED
	if destination_id == "playroom" and playroom_bonus_available:
		return BONUS
	return OPEN


static func allows_travel(state: String) -> bool:
	return state == OPEN or state == BONUS or state == PLOT


static func normalize(state: String) -> String:
	if state == OPEN or state == BONUS or state == PLOT:
		return state
	return BLOCKED


static func child_meaning(state: String) -> String:
	match normalize(state):
		OPEN:
			return "You may visit. Nothing urgent is waiting."
		BONUS:
			return "You may visit. A bonus is still waiting."
		PLOT:
			return "Go here next to continue the story."
		_:
			return "This route is resting for now."
