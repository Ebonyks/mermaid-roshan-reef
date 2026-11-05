class_name BubbleDuelInventory
extends RefCounted
## Closed shop IDs. Pearl balances and owned equipment use the shared save transaction.

const SAVE_KEY := "bubble_duel"
const CAST_IDS: Array[String] = ["roshan", "rumi", "daddy_mermaid", "baby_eagle", "rainbow_dust_bunny", "marlo"]
const COLOR_PRICES: Array[int] = [0, 20, 20, 20, 30]
const ITEMS: Array[Dictionary] = [
	{"id": "classic", "name": "Original", "price": 0, "use": 0, "icon": -1, "outfit": "roshan_original", "help": "Your own familiar look"},
	{"id": "tidewing", "name": "Tidewing Ribbons", "price": 60, "use": 0, "icon": 0, "outfit": "roshan_ribbon_v1", "help": "Ribbons give a gentle lift"},
	{"id": "moonpearl", "name": "Moonpearl Guardian", "price": 120, "use": 2, "icon": 1, "outfit": "roshan_party_dress_v1", "help": "Float gently with your pearl"},
	{"id": "swiftconch", "name": "Swift Conch Courier", "price": 150, "use": 40, "icon": 2, "outfit": "roshan_garden_v1", "help": "Ride a quick current"},
	{"id": "rainbow", "name": "Rainbow Weaver", "price": 220, "use": 50, "icon": 3, "outfit": "star", "help": "Send a pearl to pop a bubble"},
	{"id": "kelp", "name": "Living Kelp Keeper", "price": 260, "use": 60, "icon": 4, "outfit": "blossom", "help": "Bring your friend closer"},
	{"id": "lullaby", "name": "Lullaby Shell", "price": 300, "use": 70, "icon": 5, "outfit": "winter", "help": "A gentle song calms the current"},
	{"id": "squid", "name": "Twilight Squid", "price": 340, "use": 80, "icon": 6, "outfit": "magician", "help": "A soft ink puff pauses your friend"},
]


static func item(id: String) -> Dictionary:
	for entry: Dictionary in ITEMS:
		if entry["id"] == id:
			return entry
	return ITEMS[0]


static func state(main: ReefMain) -> Dictionary:
	var raw: Variant = main.save_data.get(SAVE_KEY, {})
	var result: Dictionary = raw.duplicate(true) if raw is Dictionary else {}
	var pearls: Variant = result.get("pearls", 100)
	result["pearls"] = clampi(int(pearls), 0, 1000000) if pearls is int or pearls is float else 100
	var wins: Variant = result.get("wins", 0)
	result["wins"] = clampi(int(wins), 0, 1000000) if wins is int or wins is float else 0
	var owned: Variant = result.get("owned", ["classic"])
	result["owned"] = owned.duplicate() if owned is Array else ["classic"]
	if "classic" not in result["owned"]:
		result["owned"].append("classic")
	var colors: Variant = result.get("colors", [0])
	result["colors"] = colors.duplicate() if colors is Array else [0]
	# JSON decodes numeric array entries as floats; Array membership is typed.
	# Normalize only known color IDs and preserve future/unknown values.
	for index: int in range(result["colors"].size()):
		var saved: Variant = result["colors"][index]
		if saved is float and saved >= 0.0 and saved <= 4.0 and saved == floorf(saved):
			result["colors"][index] = int(saved)
	if 0 not in result["colors"]:
		result["colors"].append(0)
	var unlocked: Variant = result.get("cast_unlocked", CAST_IDS)
	result["cast_unlocked"] = unlocked.duplicate() if unlocked is Array else CAST_IDS.duplicate()
	if "roshan" not in result["cast_unlocked"]:
		result["cast_unlocked"].append("roshan")
	var players: Variant = result.get("players", {})
	result["players"] = players.duplicate(true) if players is Dictionary else {}
	return result


static func equipped(main: ReefMain, player: int = 0) -> String:
	var data := state(main)
	var profile := _raw_profile(data, player)
	var id := String(profile.get("gear", data.get("equipped", "classic") if player == 0 else "classic"))
	return id if id in data["owned"] and item(id)["id"] == id else "classic"


static func color(main: ReefMain, player: int = 0) -> int:
	var data := state(main)
	var raw: Variant = _raw_profile(data, player).get("color", data.get("color", 0) if player == 0 else 0)
	return int(raw) if (raw is int or raw is float) and int(raw) in data["colors"] and int(raw) in range(5) else 0


static func _store(main: ReefMain, data: Dictionary) -> bool:
	var present := main.save_data.has(SAVE_KEY)
	var previous: Variant = main.save_data.get(SAVE_KEY)
	main.save_data[SAVE_KEY] = data
	if main._write_save():
		return true
	if present:
		main.save_data[SAVE_KEY] = previous
	else:
		main.save_data.erase(SAVE_KEY)
	return false


static func choose_item(main: ReefMain, id: String, player: int = 0) -> bool:
	if player not in [0, 1]:
		return false
	var entry := item(id)
	if entry["id"] != id:
		return false
	var data := state(main)
	if id not in data["owned"]:
		var price: int = entry["price"]
		if int(data["pearls"]) < price:
			return false
		data["pearls"] = int(data["pearls"]) - price
		data["owned"].append(id)
	var profile := _raw_profile(data, player)
	profile["gear"] = id
	profile["look"] = "set:" + id
	_set_profile(data, player, profile)
	if player == 0:
		data["equipped"] = id
	return _store(main, data)


static func choose_color(main: ReefMain, index: int, player: int = 0) -> bool:
	if player not in [0, 1]:
		return false
	if index not in range(COLOR_PRICES.size()):
		return false
	var data := state(main)
	if index not in data["colors"]:
		if int(data["pearls"]) < COLOR_PRICES[index]:
			return false
		data["pearls"] = int(data["pearls"]) - COLOR_PRICES[index]
		data["colors"].append(index)
	var profile := _raw_profile(data, player)
	profile["color"] = index
	_set_profile(data, player, profile)
	if player == 0:
		data["color"] = index
	return _store(main, data)


static func reward(main: ReefMain, amount: int, won: bool = false) -> bool:
	var data := state(main)
	data["pearls"] = mini(1000000, int(data["pearls"]) + maxi(0, amount))
	if won:
		var wins: Variant = data.get("wins", 0)
		data["wins"] = int(wins) + 1 if wins is int or wins is float else 1
	# Earned progress stays in memory if the device cannot finish the write.
	main.save_data[SAVE_KEY] = data
	return main._write_save()



static func _raw_profile(data: Dictionary, player: int) -> Dictionary:
	var raw: Variant = (data.get("players", {}) as Dictionary).get(str(clampi(player, 0, 1)), {})
	return raw.duplicate(true) if raw is Dictionary else {}


static func _set_profile(data: Dictionary, player: int, profile: Dictionary) -> void:
	(data["players"] as Dictionary)[str(clampi(player, 0, 1))] = profile


static func profile(main: ReefMain, player: int = 0) -> Dictionary:
	var data := state(main)
	var result := _raw_profile(data, player)
	var person := String(result.get("character", "roshan" if player == 0 else "rumi"))
	if person not in CAST_IDS or person not in data["cast_unlocked"]:
		person = "roshan"
	result["character"] = person
	result["gear"] = equipped(main, player)
	result["color"] = color(main, player)
	var look := String(result.get("look", "set:" + String(result["gear"])))
	result["look"] = look if look_available(main, person, look) else "set:classic"
	return result


static func look_available(main: ReefMain, person: String, look: String) -> bool:
	if person not in CAST_IDS:
		return false
	if look.begins_with("set:"):
		var id := look.trim_prefix("set:")
		return item(id)["id"] == id and id in state(main)["owned"] and \
			(person in FashionParts.PEOPLE or id in (["classic"] if person == "marlo" else ["classic", "tidewing", "moonpearl", "swiftconch"]))
	var definition := FashionDesigner.outfit(look)
	return not definition.is_empty() and String(definition.get("character", "")) in [person, "*"] \
		and String(definition.get("slot", "body")) == "body" and FashionDesigner.owned(main, look)


static func looks(main: ReefMain, person: String) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for entry: Dictionary in ITEMS:
		if look_available(main, person, "set:" + String(entry["id"])):
			result.append({"id": "set:" + String(entry["id"]), "name": String(entry["name"]) + " set"})
	if person != "marlo":
		for entry: Dictionary in FashionDesigner.outfits(person):
			if String(entry["id"]) != person + "_original" and look_available(main, person, String(entry["id"])):
				result.append({"id": entry["id"], "name": entry.get("label", entry["id"])})
		if person in FashionParts.PEOPLE:
			for entry: Dictionary in FashionParts.items(person, "body"):
				if not String(entry["id"]).begins_with(person + "_") and look_available(main, person, String(entry["id"])):
					result.append({"id": entry["id"], "name": entry.get("label", entry["id"])})
	return result


static func choose_character(main: ReefMain, id: String, player: int = 0) -> bool:
	var data := state(main)
	if player not in [0, 1] or id not in CAST_IDS or id not in data["cast_unlocked"]:
		return false
	var chosen := _raw_profile(data, player)
	chosen["character"] = id
	if not look_available(main, id, String(chosen.get("look", "set:classic"))):
		chosen["look"] = "set:classic"
	_set_profile(data, player, chosen)
	return _store(main, data)


static func choose_look(main: ReefMain, look: String, player: int = 0) -> bool:
	if player not in [0, 1]:
		return false
	var chosen := profile(main, player)
	if not look_available(main, String(chosen["character"]), look):
		return false
	chosen["look"] = look
	var data := state(main)
	_set_profile(data, player, chosen)
	return _store(main, data)
