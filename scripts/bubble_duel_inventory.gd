class_name BubbleDuelInventory
extends RefCounted
## Closed shop IDs. Pearl balances and owned equipment use the shared save transaction.

const SAVE_KEY := "bubble_duel"
const COLOR_PRICES: Array[int] = [0, 20, 20, 20, 30]
const ITEMS: Array[Dictionary] = [
	{"id": "classic", "name": "Roshan", "price": 0, "use": 0, "icon": -1, "outfit": "roshan_original", "help": "Your own lovely tail"},
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
	return result


static func equipped(main: ReefMain) -> String:
	var data := state(main)
	var id := String(data.get("equipped", "classic"))
	return id if id in data["owned"] and item(id)["id"] == id else "classic"


static func color(main: ReefMain) -> int:
	var data := state(main)
	var raw: Variant = data.get("color", 0)
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


static func choose_item(main: ReefMain, id: String) -> bool:
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
	data["equipped"] = id
	return _store(main, data)


static func choose_color(main: ReefMain, index: int) -> bool:
	if index not in range(COLOR_PRICES.size()):
		return false
	var data := state(main)
	if index not in data["colors"]:
		if int(data["pearls"]) < COLOR_PRICES[index]:
			return false
		data["pearls"] = int(data["pearls"]) - COLOR_PRICES[index]
		data["colors"].append(index)
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

