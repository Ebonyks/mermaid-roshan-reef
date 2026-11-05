extends "res://scripts/probe_bubble_duel_stress.gd"
## Extends the isolated real-venue harness with local bouts and wearable checks.
const Cast := preload("res://scripts/bubble_duel_cast.gd")
var cast_cases: Array[Dictionary] = []
var pairs: Dictionary = {}


func _story() -> Array:
	var result := super._story()
	result.append_array([main.character_outfits.duplicate(true), main.character_clothing_parts.duplicate(true), main.outfits_unlocked.duplicate(true)])
	return result


func _tour(index: int, seen: Dictionary) -> bool:
	_tap(venue.bubble_duel_button)
	var d := venue.bubble_duel as BubbleDuelOverlay
	if d == null: return false
	d.set_process(false)
	if index == 0:
		main.save_data[Shop.SAVE_KEY] = {"pearls": 30000, "owned": ["classic"], "colors": [0], "equipped": "classic", "future_item": {"keep": true}, "players": {"future": {"keep": 7}}}
		_inventory()
		_geometry(d)
		_controls(d)
		_collision_edges(d)
		_solo_cast(d)
		_powers(d, seen)
		_touch_layout(d)
	var p0: String = Cast.PEOPLE[index % 6]
	var p1: String = Cast.PEOPLE[(index / 6) % 6]
	_check("P1 character selection saves", Shop.choose_character(main, p0, 0))
	_check("P2 character selection saves", Shop.choose_character(main, p1, 1))
	_check("P1 gear saves", Shop.choose_item(main, Shop.ITEMS[index % 8]["id"], 0))
	_check("P2 gear saves", Shop.choose_item(main, Shop.ITEMS[(index / 8 + 3) % 8]["id"], 1))
	_check("P1 color saves", Shop.choose_color(main, index % 5, 0))
	_check("P2 color saves", Shop.choose_color(main, (index + 2) % 5, 1))
	d._show_setup(true)
	var play := _button(d, "Play together")
	_check("pictured local Play exists", play != null)
	if play == null: return false
	_tap(play)
	_check("actual Play starts simultaneous game", d.mode == Duel.Mode.VERSUS)
	var coins := int(Shop.state(main)["pearls"])
	for frame: int in range(20): d._process(1.0 / 60.0)
	_check("idle cannot move or reward", d.mode == Duel.Mode.VERSUS and int(Shop.state(main)["pearls"]) == coins and d.fighters[0]["position"] == Vector2(350, 480))
	var won := _play(d, index % 2, index)
	_check("natural controls complete local bout", won)
	_check("one shared payout", int(Shop.state(main)["pearls"]) == coins + 10)
	for frame: int in range(12): d._process(1.0 / 30.0)
	_check("celebration cannot repeat payout", int(Shop.state(main)["pearls"]) == coins + 10)
	pairs[p0 + "/" + p1] = true
	cast_cases.append({"run": index, "completed": won, "p1": Shop.profile(main, 0), "p2": Shop.profile(main, 1), "winner": index % 2})
	var file := FileAccess.open(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT") + ".cast.json", FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks": checked, "failures": bad, "cases": cast_cases, "pairs": pairs.keys()}, "  "))
	file.close()
	if not won: return false
	var replay := _button(d, "Play together again")
	_check("local replay pictured", replay != null)
	if replay == null: return false
	_tap(replay)
	_check("replay retains independent profiles", d.mode == Duel.Mode.VERSUS and d.fighters[0]["profile"] == Shop.profile(main, 0) and d.fighters[1]["profile"] == Shop.profile(main, 1))
	d._notification(Control.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_back()
	_check("Back restores hub", d.mode == Duel.Mode.HUB)
	_back()
	return venue.bubble_duel == null and venue.accepting_input and main._navigation_ref().top_id() == "opera_venue"


func _inventory() -> void:
	_check("legacy inventory defaults to two known friends", Shop.equipped(main) == "classic" and Shop.profile(main, 1)["character"] == "rumi")
	_check("six existing characters available", Shop.state(main)["cast_unlocked"].size() == 6)
	_check("first purchase succeeds", Shop.choose_item(main, "moonpearl", 0))
	var coins := int(Shop.state(main)["pearls"])
	_check("other player equips owned item free", Shop.choose_item(main, "moonpearl", 1) and int(Shop.state(main)["pearls"]) == coins)
	_check("one player changing does not change other", Shop.choose_item(main, "classic", 0) and Shop.equipped(main, 1) == "moonpearl")
	_check("colors independent", Shop.choose_color(main, 1, 1) and Shop.color(main, 0) == 0 and Shop.color(main, 1) == 1)
	_check("unknown cast ID refused", not Shop.choose_character(main, "res://invalid", 0))
	_check("locked item-set refused", not Shop.choose_look(main, "set:squid", 0))
	_check("invalid slot cannot purchase", not Shop.choose_item(main, "squid", 2))
	var before := Shop.state(main)
	main._save_state.future_schema_read_only = true
	_check("failed disk save rejects purchase", not Shop.choose_item(main, "squid", 1))
	_check("failed save rolls back both profiles", Shop.state(main) == before)
	main._save_state.future_schema_read_only = false
	for entry: Dictionary in Shop.ITEMS:
		_check("actual item unlocked " + String(entry["id"]), Shop.choose_item(main, entry["id"], 0))
	for index: int in range(5): Shop.choose_color(main, index, 0)
	_check("unknown fields preserved", Shop.state(main)["future_item"] == {"keep": true} and Shop.state(main)["players"]["future"] == {"keep": 7})


func _geometry(d: BubbleDuelOverlay) -> void:
	for person: String in Cast.PEOPLE:
		for item: Dictionary in Shop.ITEMS:
			var profile := {"character": person, "gear": item["id"], "look": "set:" + String(item["id"]), "color": 0}
			for moving: bool in [false, true]:
				var frames := 16 if person == "roshan" and moving else (4 if person == "rumi" or (person == "marlo" and moving) else 1)
				for index: int in range(frames):
					var clock := float(index) / (15.0 if person == "roshan" else (5.0 if person == "marlo" else 6.0))
					var frame := d.appearance.frame(profile, moving, clock)
					var texture := d.appearance.texture(profile, moving)
					_check("authored frame kept " + person, texture != null and Rect2(Vector2.ZERO, texture.get_size()).encloses(frame["region"]))
					var point := d.appearance.contact(profile, moving, clock)
					_check("finite painted contact " + person, is_finite(point.x) and is_finite(point.y) and point.length() < 160.0)
					var wear := d.appearance.attachment(profile, moving, clock)
					if item["id"] != "classic":
						_check("wearable readable bounded size " + person, not wear.is_empty() and (wear["rect"] as Rect2).size.x >= 15.0 and (wear["rect"] as Rect2).size.y <= 90.0)
						_check("socket follows figure " + person, (wear["socket"] as Vector2).length() < 115.0)
						var opaque := 0
						var overlap := 0
						var exposed := 0
						var rect: Rect2 = wear["rect"]
						var body_image := d.appearance._source_image(String(frame["source"]))
						var icon_image: Image = d.appearance.icons[int(wear["icon"])].get_image()
						if icon_image.is_compressed(): icon_image.decompress()
						for y: int in range(ceili(rect.size.y)):
							for x: int in range(ceili(rect.size.x)):
								var uv := Vector2(float(x) / rect.size.x, float(y) / rect.size.y)
								if icon_image.get_pixel(mini(255, int(uv.x * 256)), mini(255, int(uv.y * 256))).a < 0.4: continue
								opaque += 1
								var pixel := (frame["anchor"] as Vector2) + (rect.position + Vector2(x, y)) / float(frame["factor"])
								var region: Rect2 = frame["region"]
								var on_body := Rect2(Vector2.ZERO, region.size).has_point(pixel) and body_image.get_pixel(int(region.position.x + pixel.x), int(region.position.y + pixel.y)).a > 0.4
								if on_body: overlap += 1
								else: exposed += 1
						_check("painted gear touches body " + person + "/" + String(item["id"]) + "/" + str(index), opaque > 20 and overlap > 0)
						if bool(wear["behind"]):
							_check("backpack remains visible " + person + "/" + str(index), exposed > 10)
	_check("texture cache bounded", d.appearance.textures.size() <= 16)
	_check("source image cache bounded", d.appearance.source_images.size() <= 8)


func _button(d: Control, tooltip: String) -> Control:
	for child: Node in d.menu.get_children():
		if child is Control and child.tooltip_text == tooltip: return child as Control
	return null


func _finger(d: Control, index: int, point: Vector2, down: bool, canceled: bool = false) -> void:
	var event := InputEventScreenTouch.new()
	event.index = index
	event.position = root.get_screen_transform() * (d.get_screen_transform() * point)
	event.pressed = down
	event.canceled = canceled
	root.push_input(event, false)


func _drag(d: Control, index: int, point: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = index
	event.position = root.get_screen_transform() * (d.get_screen_transform() * point)
	root.push_input(event, false)


func _key(code: Key, down: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = code
	event.pressed = down
	root.push_input(event, false)


func _controls(d: BubbleDuelOverlay) -> void:
	d._begin_versus()
	var pads := d.Duo.PADS
	_finger(d, 0, pads[0].get_center() + Vector2(70, 0), true)
	_finger(d, 1, pads[1].get_center() - Vector2(70, 0), true)
	for frame: int in range(12): d._process(1.0 / 60.0)
	_check("two routed fingers move two swimmers", d.duo_touch_owners.get(0, -1) == 0 and d.duo_touch_owners.get(1, -1) == 1 and (d.fighters[0]["position"] as Vector2).x > 350 and (d.fighters[1]["position"] as Vector2).x < 930)
	_finger(d, 2, pads[0].get_center(), true)
	_check("third finger cannot steal either player", not d.duo_touch_owners.has(2))
	_drag(d, 0, pads[1].get_center())
	_check("crossing sides preserves ownership", d.duo_touch_owners.get(0, -1) == 0 and d.duo_touch_owners.get(1, -1) == 1)
	_finger(d, 0, pads[1].get_center(), false, true)
	var other: Vector2 = d.fighters[1]["position"]
	d._process(1.0 / 60.0)
	_check("P1 cancel leaves P2 moving", not bool(d.fighters[0]["armed"]) and bool(d.fighters[1]["held"]) and d.fighters[1]["position"] != other)
	_finger(d, 1, pads[1].get_center(), false)
	_finger(d, 2, pads[0].get_center(), false)
	_key(KEY_W, true)
	_key(KEY_UP, true)
	d._process(1.0 / 60.0)
	_check("both keyboard players thrust", bool(d.fighters[0]["held"]) and bool(d.fighters[1]["held"]))
	_key(KEY_W, false)
	d._process(1.0 / 60.0)
	_check("one key release cannot stop other player", not bool(d.fighters[0]["held"]) and bool(d.fighters[1]["held"]))
	_key(KEY_UP, false)
	d._notification(Control.NOTIFICATION_APPLICATION_FOCUS_OUT)
	var first: Vector2 = d.fighters[0]["position"]
	other = d.fighters[1]["position"]
	var balance: int = int(Shop.state(main)["pearls"])
	for frame: int in range(60): d._process(1.0 / 60.0)
	_check("focus loss flushes both without later action", d.duo_keys.is_empty() and d.duo_touch_owners.is_empty() and d.fighters[0]["position"] == first and d.fighters[1]["position"] == other and Shop.state(main)["pearls"] == balance)
	d._show_setup(true)
	d._open_picker(0, "character")
	var choice: Control
	for child: Node in d.menu.get_children():
		if child is Control and child.get_meta("choice_id", "") == "daddy_mermaid": choice = child as Control
	_check("six-card cast picker exists", choice != null)
	if choice != null:
		_tap(choice)
		_check("actual character card saves", Shop.profile(main, 0)["character"] == "daddy_mermaid")


func _collision_edges(d: BubbleDuelOverlay) -> void:
	# Explicit collision fixtures complement full control-driven bouts.
	# Two pearls arrive on the last bubbles in the same integration step.
	for player: int in range(2): Shop.choose_item(main, "rainbow", player)
	d._begin_versus()
	var balance := int(Shop.state(main)["pearls"])
	for player: int in range(2):
		d.fighters[player]["bubbles"] = [1]
		(d.fighters[player]["shots"] as Array).append({"position": d.duo.bubble_at(1 - player, 1), "life": 1.0})
	d._process(1.0 / 30.0)
	_check("simultaneous last hits resolve a friendly tie", d.mode == Duel.Mode.CELEBRATE and (d.fighters[0]["bubbles"] as Array).is_empty() and (d.fighters[1]["bubbles"] as Array).is_empty())
	_check("tie credits one shared reward", int(Shop.state(main)["pearls"]) == balance + 10)
	d._begin_versus()
	d.fighters[1]["bubbles"] = [1]
	(d.fighters[0]["shots"] as Array).append({"position": d.duo.bubble_at(1, 0), "life": 1.0})
	d._process(1.0 / 60.0)
	_check("missing bubble side cannot be popped again", d.mode == Duel.Mode.VERSUS and d.fighters[1]["bubbles"] == [1])
	for player: int in range(2):
		d.fighters[player]["armed"] = true
		d.fighters[player]["position"] = Vector2(350 if player == 0 else 930, 700)
		d.fighters[player]["velocity"] = Vector2(0, 365)
	d._process(1.0 / 30.0)
	_check("both floor crossings recover without losing bubbles", (d.fighters[0]["position"] as Vector2).y == 480 and (d.fighters[1]["position"] as Vector2).y == 480 and float(d.fighters[0]["recover"]) > 0 and float(d.fighters[1]["recover"]) > 0 and d.fighters[0]["bubbles"] == [0, 1] and d.fighters[1]["bubbles"] == [1])
	d._notification(Control.NOTIFICATION_APPLICATION_FOCUS_OUT)
	_check("focus flushes every in-flight pearl", (d.fighters[0]["shots"] as Array).is_empty() and (d.fighters[1]["shots"] as Array).is_empty())


func _solo_cast(d: BubbleDuelOverlay) -> void:
	for person: String in Cast.PEOPLE:
		Shop.choose_character(main, person, 0)
		Shop.choose_item(main, "classic", 0)
		Shop.choose_character(main, "rumi" if person != "rumi" else "roshan", 1)
		d._begin(Duel.Mode.DUEL)
		_check("selected cast can finish solo " + person, _hit(d, 1, 1.0 / 60.0) and _hit(d, 2, 1.0 / 60.0) and d.mode == Duel.Mode.CELEBRATE)
	Shop.choose_character(main, "roshan", 0)
	var other := Shop.profile(main, 1)
	var wardrobe_choice := ""
	for look: Dictionary in Shop.looks(main, "roshan"):
		if not String(look["id"]).begins_with("set:"):
			wardrobe_choice = look["id"]
			break
	_check("shared unlocked wardrobe is selectable independently", not wardrobe_choice.is_empty() and Shop.choose_look(main, wardrobe_choice, 0) and Shop.profile(main, 0)["look"] == wardrobe_choice and Shop.profile(main, 1) == other)


func _touch_layout(d: BubbleDuelOverlay) -> void:
	for state: String in ["setup", "character", "look", "versus"]:
		d._show_setup(true)
		if state in ["character", "look"]: d._open_picker(0, state)
		elif state == "versus": d._begin_versus()
		for child: Node in d.menu.get_children():
			if child is Button:
				var control := child as Button
				_check("pictured touch target is generous and fully visible " + state + "/" + control.tooltip_text, control.size.x >= 110 and control.size.y >= 110 and Rect2(0, 0, 1280, 720).encloses(control.get_rect()))
	for pad: Rect2 in d.Duo.PADS:
		_check("raw pad hit region meets touch floor", pad.size.x >= 110 and pad.size.y >= 110 and Rect2(0, 0, 1280, 720).encloses(pad))


func _powers(d: BubbleDuelOverlay, seen: Dictionary) -> void:
	for player: int in range(2):
		for entry: Dictionary in Shop.ITEMS:
			var id := String(entry["id"])
			Shop.choose_item(main, id, player)
			d._begin_versus()
			var fighter: Dictionary = d.fighters[player]
			var other: Dictionary = d.fighters[1 - player]
			var before := float(fighter["glow"])
			if id in ["classic", "tidewing"]:
				_check("passive gear spends no glow", not d.duo.activate(player) and float(fighter["glow"]) == before)
				if id == "tidewing":
					fighter["armed"] = true
					fighter["position"] = Vector2(350 if player == 0 else 930, 480)
					fighter["velocity"] = Vector2(0, 240)
					d._process(1.0 / 60.0)
					_check("both ribbon wearers can lift", (fighter["velocity"] as Vector2).y < 0.0)
					seen[id] = true
				continue
			_tap(d.power_button if player == 0 else d.second_power_button)
			_check("either real power button spends exact cost", float(fighter["glow"]) == before - float(entry["use"]))
			seen[id] = true
			var origin: Vector2 = fighter["position"]
			var target: Vector2 = other["position"]
			if id == "rainbow":
				var tip := d.appearance.tool_tip(fighter["profile"], origin, float(fighter["facing"]), false, d.active_time)
				_check("pearl starts on worn wand", (fighter["shots"] as Array).size() == 1 and ((fighter["shots"] as Array)[0]["position"] as Vector2).is_equal_approx(tip))
			for frame: int in range(12): d._process(1.0 / 60.0)
			match id:
				"moonpearl": _check("either wearer hovers", absf((fighter["position"] as Vector2).y - origin.y) < 0.01)
				"swiftconch": _check("either conch drives its wearer", absf((fighter["position"] as Vector2).x - origin.x) > 100.0)
				"kelp": _check("either kelp harness pulls other", (other["position"] as Vector2).distance_to(origin) < target.distance_to(origin))
				"lullaby": _check("either shell dims and slows other", float(other["glow"]) < 1.0 and float(other["slow_time"]) > 1.0)
				"squid": _check("either squid satchel holds other", other["position"] == target and float(other["hold_time"]) > 0.0)
				"rainbow":
					for frame: int in range(150): d._process(1.0 / 60.0)
					_check("either worn wand pops a bubble", (other["bubbles"] as Array).size() == 1)


func _play(d: BubbleDuelOverlay, player: int, run: int) -> bool:
	var other := 1 - player
	var pad: Rect2 = d.Duo.PADS[player]
	var down := false
	if String((d.fighters[player]["profile"] as Dictionary)["gear"]) not in ["classic", "tidewing"]:
		_tap(d.power_button if player == 0 else d.second_power_button)
	var dt := 1.0 / (30.0 if run % 2 else 60.0)
	for frame: int in range(1200):
		if d.mode == Duel.Mode.CELEBRATE:
			if down: _finger(d, player, pad.get_center(), false)
			return (d.fighters[other]["bubbles"] as Array).is_empty()
		var fighter: Dictionary = d.fighters[player]
		var bubbles: Array = d.fighters[other]["bubbles"]
		if bubbles.is_empty(): continue
		var target := d.duo.bubble_at(other, int(bubbles[0]))
		var contact := d.appearance.contact(fighter["profile"], false, d.active_time)
		var position: Vector2 = fighter["position"]
		var goal := target.x - contact.x * float(fighter["facing"])
		var error := goal - position.x
		var point := pad.get_center() + Vector2(clampf(error / 65.0, -1.0, 1.0) * 105.0, 0)
		if down:
			if absf(error) < 9.0 and position.y + contact.y < target.y - 20.0 and float(d.fighters[other]["recover"]) <= 0.0:
				_finger(d, player, point, false)
				down = false
			else: _drag(d, player, point)
		elif not bool(fighter["armed"]) or position.y + contact.y > target.y + 38.0 or (absf(error) > 28.0 and (fighter["velocity"] as Vector2).y >= 0.0):
			_finger(d, player, point, true)
			down = true
		d._process(dt)
	if down: _finger(d, player, pad.get_center(), false, true)
	print("BUBBLECAST|bout incomplete|", run, "|", d.fighters)
	return false


func _verify_reload() -> void:
	var result: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(OS.get_environment("BUBBLE_DUEL_STRESS_OUTPUT") + ".cast.json"))
	var expected: Dictionary = (result["cases"] as Array).back()
	for player: int in range(2):
		var actual := Shop.profile(main, player)
		var profile: Dictionary = expected["p1" if player == 0 else "p2"]
		for key: String in ["character", "gear", "look"]:
			_check("new process restores P%d %s" % [player + 1, key], actual[key] == profile[key])
		_check("new process restores color", int(actual["color"]) == int(profile["color"]))
	var restored := Shop.state(main)
	_check("unknown inventory data survives reload", restored["future_item"] == {"keep": true} and (restored["players"]["future"] as Dictionary).get("keep") == 7)
	var file := FileAccess.open(OS.get_environment("BUBBLE_DUEL_RELOAD_OUTPUT"), FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks": checked, "failures": bad, "profiles": [Shop.profile(main, 0), Shop.profile(main, 1)], "inventory": restored}, "  "))
	file.close()
	print("BUBBLECASTRELOAD|", checked, " checks|", bad, " failures")
	main.queue_free()
	quit(0 if bad == 0 else 1)
