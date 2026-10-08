class_name FashionDesigner
extends RefCounted
## Shared clothing policy. Every durable field belongs to ReefMain.
const PARTY_DRESS := "roshan_party_dress_v1"
const CHARACTERS: Array[Dictionary] = [
	{"id": "roshan", "name": "Roshan", "source": "res://assets/characters/roshan_25d/roshan_base.png"},
	{"id": "rumi", "name": "Rumi", "source": "res://assets/characters/rumi/rumi_eight_pose_runtime.png"},
	{"id": "baby_eagle", "name": "Baby Eagle", "source": "res://assets/characters/companions/baby_eagle.png"},
	{"id": "daddy_mermaid", "name": "Daddy", "source": "res://assets/characters/friends/daddy.webp"},
	{"id": "rainbow_dust_bunny", "name": "Rainbow Friend", "source": "res://assets/sprites/dust_bunnies/rainbow_friend.png"},
]
const SOURCES := {
	"roshan": ["roshan_base", "roshan_directional", "roshan_swim_front",
		"roshan_swim_back", "roshan_gesture_a", "roshan_gesture_b",
		"roshan_gesture_c", "roshan_gesture_d", "roshan_play_a", "roshan_play_b"],
	"rumi": ["rumi_eight_pose_runtime", "rumi_pool_idle_swim_atlas"],
	"baby_eagle": ["baby_eagle"],
	"daddy_mermaid": ["daddy"],
	"rainbow_dust_bunny": ["rainbow_friend"],
}
const SAVE_DICTIONARIES: Array[String] = [
	"character_outfits", "character_clothing_parts", "outfits_unlocked",
	"fashion_disguise_progress", "fashion_rewards_claimed", "fashion_dressing_progress"]
const ORIGINAL_IDS := {
	"roshan": "roshan_original", "rumi": "rumi_original",
	"baby_eagle": "baby_eagle_original", "daddy_mermaid": "daddy_mermaid_original",
	"rainbow_dust_bunny": "rainbow_dust_bunny_original"}
const DISGUISE_MASK := 7

static func character(id: String) -> Dictionary:
	for entry: Dictionary in CHARACTERS:
		if String(entry["id"]) == id:
			return entry
	return {}

static func outfits(character_id: String) -> Array[Dictionary]:
	return FashionSkinEngine.outfits(character_id)

static func outfit(id: String) -> Dictionary:
	return FashionSkinEngine.outfit(id)

static func _flag(values: Dictionary, key: String) -> bool:
	var value: Variant = values.get(key, false)
	return typeof(value) == TYPE_BOOL and bool(value)

static func normalise_save_patch(raw: Dictionary) -> Dictionary:
	var result: Dictionary = {}
	for key: String in SAVE_DICTIONARIES:
		var value: Variant = raw.get(key, {})
		result[key] = (value as Dictionary).duplicate(true) if value is Dictionary else {}
	var done: Variant = raw.get("chapter2_party_dress_done", false)
	result["chapter2_party_dress_done"] = (typeof(done) == TYPE_BOOL and bool(done)) \
		or _flag(raw, "chapter2_party_started")
	return result

static func restore(main: ReefMain, raw: Dictionary) -> void:
	var patch: Dictionary = normalise_save_patch(raw)
	main.character_outfits = patch["character_outfits"]
	main.character_clothing_parts = patch["character_clothing_parts"]
	main.fashion_composed_textures.clear()
	main.outfits_unlocked = patch["outfits_unlocked"]
	main.fashion_disguise_progress = patch["fashion_disguise_progress"]
	main.fashion_dressing_progress = patch["fashion_dressing_progress"]
	main.fashion_rewards_claimed = patch["fashion_rewards_claimed"]
	main.chapter2_party_dress_done = bool(patch["chapter2_party_dress_done"])
	refresh_unlocks(main)

static func selected(main: ReefMain, character_id: String) -> String:
	if main == null or not ORIGINAL_IDS.has(character_id):
		return ""
	if character_id in FashionParts.PEOPLE:
		return FashionParts.selected(main, character_id, "body")
	var value: Variant = main.character_outfits.get(character_id, ORIGINAL_IDS[character_id])
	# Unknown future IDs stay in the save; presentation falls back without erasure.
	if value is String:
		var definition: Dictionary = outfit(String(value))
		if String(definition.get("character", "")) == character_id \
				and owned(main, String(value)):
			return String(value)
	return String(ORIGINAL_IDS[character_id])

static func owned(main: ReefMain, id: String) -> bool:
	var definition: Dictionary = outfit(id)
	if main == null or definition.is_empty():
		return false
	return bool(definition.get("starter", false)) or String(definition["kind"]) in ["original", "ribbon"] \
		or _flag(main.outfits_unlocked, id)

static func grant(main: ReefMain, id: String) -> bool:
	if outfit(id).is_empty() or owned(main, id):
		return false
	main.outfits_unlocked[id] = true
	return true

static func refresh_unlocks(main: ReefMain) -> void:
	var party_ready: bool = main._chapter_two_ref().party_is_ready() \
		or main.chapter2_party_started or main.chapter2_story_complete
	var garden_ready: bool = main.chapter2_farmer_strawberries_ready \
		or (main.opera_stars & (1 << ChapterTwoDirector.ACT_FARMER)) != 0
	var friends_party: bool = party_ready
	for person: Dictionary in CHARACTERS:
		var id: String = String(person["id"])
		if (party_ready if id == "roshan" else friends_party):
			grant(main, PARTY_DRESS if id == "roshan" else id + "_party_v1")
		if garden_ready:
			grant(main, id + "_garden_v1")
	FashionParts.refresh_unlocks(main)
	if next_disguise_phase(main) >= 3:
		grant(main, "roshan_garden_disguise_v1")

static func equip(main: ReefMain, character_id: String, id: String,
		intentional: bool = false) -> bool:
	var definition: Dictionary = outfit(id)
	if not intentional or not FashionParts.fits(definition, character_id) \
			or not owned(main, id):
		return false
	var slot: String = String(definition.get("slot", "body"))
	var changed: bool = FashionParts.selected(main, character_id, slot) != id if character_id in FashionParts.PEOPLE else main.character_outfits.get(character_id, "") != id
	if character_id in FashionParts.PEOPLE:
		var parts: Dictionary = FashionParts.raw_parts(main, character_id)
		parts[slot] = id
		main.character_clothing_parts[character_id] = parts
	if slot == "body":
		main.character_outfits[character_id] = id
	if character_id in ["roshan", "rumi", "daddy_mermaid"]:
		var raw: Variant = main.fashion_dressing_progress.get(character_id, {})
		var fitted: Dictionary = (raw as Dictionary).duplicate(true) if raw is Dictionary else {}
		fitted["dressed"] = true
		fitted["outfit_id"] = selected(main, character_id)
		var old_parts: Variant = fitted.get("parts", {})
		var journal: Dictionary = (old_parts as Dictionary).duplicate(true) if old_parts is Dictionary else {}
		journal.merge(FashionParts.selections(main, character_id), true)
		fitted["parts"] = journal
		main.fashion_dressing_progress[character_id] = fitted
	var legacy_skin: bool = main.skin_id != "classic"
	if character_id == "roshan":
		main.skin_id = "classic"
		if slot == "body" and id == PARTY_DRESS and main._chapter_two_ref().party_is_ready() \
				and not main.chapter2_party_started:
			main.chapter2_party_dress_done = true
	if character_id == "roshan" and legacy_skin:
		main._apply_skin()
	FashionSkinEngine.refresh(main, character_id)
	main._companion_ref().refresh_wardrobe()
	main._write_save()
	return changed

static func party_dressed(main: ReefMain) -> bool:
	return main.chapter2_party_dress_done and main.skin_id == "classic" \
		and selected(main, "roshan") == PARTY_DRESS

static func practice_available(main: ReefMain) -> bool:
	return main.chapter2_story_complete

static func _disguise_mask(raw: Variant) -> int:
	# JSON numbers restore as floats. Keep future high bits across each known beat.
	if typeof(raw) == TYPE_INT:
		return maxi(int(raw), 0)
	if typeof(raw) == TYPE_FLOAT:
		var number: float = float(raw)
		if is_finite(number) and number >= 0.0 and number < 9223372036854775808.0 and number == floor(number):
			return int(number)
	return 0

static func next_disguise_phase(main: ReefMain) -> int:
	var mask: int = _disguise_mask(main.fashion_disguise_progress.get("completed_mask", 0))
	for phase: int in range(3):
		if (mask & (1 << phase)) == 0:
			return phase
	return 3

static func complete_disguise_phase(main: ReefMain, phase: int, choice: String,
		intentional: bool = false) -> bool:
	if not intentional or not practice_available(main) \
			or phase != next_disguise_phase(main) or phase >= 3:
		return false
	var expected: String = ["roshan_garden_v1","tail_strawberry_v1","finish_bow"][phase]
	if choice != expected or not owned(main, "roshan_garden_v1") or (phase == 1 and not owned(main,"tail_strawberry_v1")):
		return false
	var old_mask: Variant = main.fashion_disguise_progress.get("completed_mask", 0)
	main.fashion_disguise_progress["completed_mask"] = _disguise_mask(old_mask) | ((1 << (phase + 1)) - 1)
	if phase < 2:
		equip(main, "roshan", expected, true)
	else:
		grant(main, "roshan_garden_disguise_v1")
		main.fashion_rewards_claimed["garden_disguise_v1"] = true
		equip(main, "roshan", "head_pearl_v1", true)
	return true

static func main_for(node: Node) -> ReefMain:
	var cursor: Node = node
	while cursor != null:
		if cursor is ReefMain:
			return cursor as ReefMain
		cursor = cursor.get_parent()
	return null
