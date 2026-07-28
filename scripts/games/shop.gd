class_name ShopGame
extends RefCounted
# Kareem's Pearl Shop. The four live offers and the single usable counter
# treasure are 2D standees over a custom shell-market plate.

const BACKGROUND := "res://assets/minigames/shop/background.png"
const BEANS_SPRITE := "res://assets/minigames/shop/beans.svg"
const PEARL_SPRITE := "res://assets/minigames/shop/pearl.svg"
const EXIT_SPRITE := "res://assets/minigames/shop/exit.svg"
const ROSHAN_SHOP := "res://assets/minigames/shared/roshan_catch.png"
const ANIMAL_SPRITES := {
	"stingray": "res://assets/minigames/shop/stingray.png",
	"turtle": "res://assets/minigames/shop/turtle.png",
	"squid": "res://assets/minigames/shop/squid.png",
	"dolphin": "res://assets/minigames/shop/dolphin.png",
}

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _sprite(path: String, height: float, pos: Vector3) -> Sprite3D:
	var sprite := Sprite3D.new()
	sprite.texture = load(path)
	sprite.pixel_size = height / maxf(1.0, float(sprite.texture.get_height()))
	sprite.position = pos
	sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	sprite.shaded = false
	sprite.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	m.add_child(sprite)
	m.game_nodes.append(sprite)
	return sprite

func _add_background(origin: Vector3) -> void:
	# One authored plate carries the architecture, shelves, glass and lighting.
	var background := Sprite3D.new()
	background.name = "PearlShopPlate"
	background.texture = load(BACKGROUND)
	background.pixel_size = 23.0 / maxf(1.0, float(background.texture.get_height()))
	background.position = origin + Vector3(0.0, 12.5, -14.0)
	background.billboard = BaseMaterial3D.BILLBOARD_DISABLED
	background.shaded = false
	background.alpha_cut = SpriteBase3D.ALPHA_CUT_DISABLED
	background.render_priority = -10
	m.add_child(background)
	m.game_nodes.append(background)

func _pearl_marker(pos: Vector3, count: int) -> Node3D:
	# Price bands are shown as one through four large pearl pictures. Exact
	# balances still live in the HUD, but choosing an offer never requires text.
	var marker := Node3D.new()
	marker.position = pos
	m.add_child(marker)
	m.game_nodes.append(marker)
	var span: float = float(count - 1) * 0.58
	for i in range(count):
		var pearl := Sprite3D.new()
		pearl.texture = load(PEARL_SPRITE)
		pearl.pixel_size = 0.75 / maxf(1.0, float(pearl.texture.get_height()))
		pearl.position.x = float(i) * 0.58 - span * 0.5
		pearl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		pearl.shaded = false
		pearl.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		marker.add_child(pearl)
	return marker

func _build_shop(origin: Vector3) -> void:
	_add_background(origin)
	m.g["kelp"] = []
	m.g["items"] = []
	m.g["tanks"] = []

	# Kareem's identity art is intentionally reused unchanged.
	var kareem := _sprite("res://assets/characters/friends/kareem.png", 7.8,
		origin + Vector3(10.8, 6.2, -8.5))
	kareem.name = "KareemShopkeeper"

	var beans_pos := origin + Vector3(0.0, 4.2, -3.8)
	var beans := _sprite(BEANS_SPRITE, 3.1, beans_pos)
	beans.name = "BeanTreasure"
	var beans_marker := _pearl_marker(beans_pos + Vector3(0.0, 2.2, 0.0), 1)
	(m.g["items"] as Array).append({
		"id": "beans",
		"node": beans,
		"tag": beans_marker,
		"price": 2,
		"base": beans_pos,
	})

	var tank_slots := [-10.5, -3.5, 3.5, 10.5]
	for ti in range(m.ANIMAL_SHOP.size()):
		var offer: Dictionary = m.ANIMAL_SHOP[ti]
		var animal_id := String(offer["id"])
		var base := origin + Vector3(tank_slots[ti], 10.5, -11.4)
		var pet := _sprite(String(ANIMAL_SPRITES[animal_id]), 4.4, base)
		pet.name = "ShopFriend_%s" % animal_id
		var marker := _pearl_marker(base + Vector3(0.0, 2.8, 0.2), ti + 1)
		var owned: bool = bool(m.animals_owned.get(animal_id, false))
		pet.visible = not owned
		marker.visible = not owned
		(m.g["tanks"] as Array).append({
			"id": animal_id,
			"node": pet,
			"tag": marker,
			"price": int(offer["price"]),
			"base": base,
			"ph": float(ti) * 1.7,
			"rig": {},
		})

	var exit := _sprite(EXIT_SPRITE, 4.5, origin + Vector3(-14.0, 4.2, 11.0))
	exit.name = "WordlessShopExit"
	m.g["exit"] = exit

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	m.player.set_skin("__minigame_2d", ROSHAN_SHOP)
	_build_shop(origin)
	m.g["shop_action_down"] = Input.is_physical_key_pressed(KEY_SPACE) \
		or Input.is_physical_key_pressed(KEY_ENTER) \
		or m.joy_pressed(JOY_BUTTON_A) \
		or m.joy_pressed(JOY_BUTTON_B)
	m.g["shop_wait_release"] = bool(m.g["shop_action_down"])
	m.player.position = origin + Vector3(0, 4, 9)
	m.player.vel = Vector3.ZERO
	m.player.yaw = PI
	m.show_msg(fr["fname"], "Swim close to Beans or a reef friend, then tap the pink button!")

func _purchase_action_just() -> bool:
	# Proximity chooses an offer; a separate fresh tap confirms it.
	var down: bool = Input.is_physical_key_pressed(KEY_SPACE) \
		or Input.is_physical_key_pressed(KEY_ENTER) \
		or m.joy_pressed(JOY_BUTTON_A) \
		or m.joy_pressed(JOY_BUTTON_B)
	var touch_just := false
	if m.touch_ui != null and m.touch_ui.has_method("consume_action_just"):
		touch_just = bool(m.touch_ui.consume_action_just())
	if bool(m.g.get("shop_wait_release", false)):
		m.g["shop_action_down"] = down
		if not down and not touch_just:
			m.g["shop_wait_release"] = false
		return false
	var just: bool = down and not bool(m.g.get("shop_action_down", false))
	m.g["shop_action_down"] = down
	if touch_just:
		just = true
	return just

func _tick_shop(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m.hud_game.text = "Pearls: %d  •  swim close, then tap the pink button" % m.pearl_count
	m.shop_msg_cool = maxf(0.0, m.shop_msg_cool - delta)
	var buy_pressed := _purchase_action_just()
	var choice_kind := ""
	var choice_id := ""
	var choice_price := 0
	var choice_dist := 1e20

	for raw_item in m.g.get("items", []):
		var item: Dictionary = raw_item
		var item_node: Sprite3D = item["node"]
		if not item_node.visible:
			continue
		var item_base: Vector3 = item["base"]
		item_node.position.y = item_base.y + sin(float(m.g["t"]) * 2.0) * 0.18
		item_node.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 3.0) * 0.05)
		if m._near_ground(item_base, ppos, 5.0, 14.0):
			var item_delta := item_base - ppos
			var item_dist := Vector2(item_delta.x, item_delta.z).length_squared()
			if item_dist < choice_dist:
				choice_kind = "beans"
				choice_id = String(item["id"])
				choice_price = int(item["price"])
				choice_dist = item_dist

	for raw_tank in m.g.get("tanks", []):
		var tank: Dictionary = raw_tank
		var animal_id := String(tank["id"])
		var pet: Sprite3D = tank["node"]
		if is_instance_valid(pet) and pet.visible:
			var time: float = float(m.g["t"])
			var base: Vector3 = tank["base"]
			var phase: float = float(tank["ph"])
			var rate := 0.7
			var sweep := 0.75
			if animal_id == "turtle":
				rate = 0.45
			elif animal_id == "squid":
				rate = 0.55
				sweep = 0.3
			var swim := sin(time * rate + phase)
			pet.position.x = base.x + swim * sweep
			pet.position.y = base.y + sin(time * rate * 1.7 + phase) * 0.15
			pet.flip_h = cos(time * rate + phase) > 0.0
			pet.rotation.z = sin(time * 0.8 + phase) * (0.06 if animal_id == "stingray" else 0.025)
			var pulse := sin(time * 2.4 + phase)
			pet.scale = Vector3.ONE * (1.0 + pulse * (0.035 if animal_id == "squid" else 0.02))
		if bool(m.animals_owned.get(animal_id, false)):
			continue
		var tank_base: Vector3 = tank["base"]
		if m._near_ground(tank_base, ppos, 5.5, 7.0):
			var tank_delta := tank_base - ppos
			var tank_dist := Vector2(tank_delta.x, tank_delta.z).length_squared()
			if tank_dist < choice_dist:
				choice_kind = "friend"
				choice_id = animal_id
				choice_price = int(tank["price"])
				choice_dist = tank_dist

	if choice_id != "":
		if choice_kind == "beans" and m.beans_t >= 0.0:
			m.hud_game.text = "Bean power is already bubbling!"
			if buy_pressed and m.shop_msg_cool <= 0.0:
				m.shop_msg_cool = 2.5
				m.show_msg("Pearl Shop", "You already have bean power—enjoy the ride!")
		elif m.pearl_count < choice_price:
			var meter_fill := clampi(int(floor(
				10.0 * float(m.pearl_count) / float(maxi(1, choice_price)))), 0, 9)
			m.hud_game.text = "Pearls  " + m._pips(meter_fill, 10, "⚪")
			if buy_pressed and m.shop_msg_cool <= 0.0:
				m.shop_msg_cool = 2.5
				m.show_msg("Pearl Shop", "Find a few more pearls, then come back!")
		else:
			m.hud_game.text = "Pearls  " + m._pips(10, 10, "⚪") + "  tap the pink button!"
			if buy_pressed:
				if choice_kind == "beans":
					_shop_buy(choice_id)
					m.show_msg("Pearl Shop", "Beans! Hold on to your tail!")
				else:
					_tank_buy(choice_id)

	var exit: Sprite3D = m.g["exit"]
	exit.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 3.0) * 0.08)
	var relative: Vector3 = ppos - m.ARENA_POS
	if float(m.g["t"]) > 1.5 and (relative.z > 20.0 or relative.z < -16.0 or absf(relative.x) > 19.0):
		m._end_game(true, fr, "Bye-bye! Come back soon!")

func _shop_buy(id: String) -> void:
	# Retired cosmetic ids remain in saves for compatibility, but only Beans
	# has a fitted offer and can be purchased.
	if id != "beans":
		return
	for raw_item in m.SHOP_ITEMS:
		var item: Dictionary = raw_item
		if String(item["id"]) != id or m.pearl_count < int(item["price"]):
			continue
		if m.beans_t < 0.0:
			m.pearl_count -= int(item["price"])
			m.shop_owned["_beans_once"] = true
			m._update_hud()
			m._write_save()
			if m.buy_sound != null:
				m.buy_sound.play()
			m._beans_go()
			m._sparkle_burst(m.player.position + Vector3(0, 1, 0), Color(0.6, 1.0, 0.4))
			_check_shopper()
		return

func _tank_buy(id: String) -> void:
	for raw_offer in m.ANIMAL_SHOP:
		var offer: Dictionary = raw_offer
		if String(offer["id"]) != id:
			continue
		if bool(m.animals_owned.get(id, false)) or m.pearl_count < int(offer["price"]):
			return
		m.pearl_count -= int(offer["price"])
		m.animals_owned[id] = true
		m._spawn_shop_animals()
		m._update_hud()
		m._write_save()
		if m.buy_sound != null:
			m.buy_sound.play()
		m._sparkle_burst(m.player.position + Vector3(0, 2, 0), Color(0.5, 1.0, 0.9))
		for raw_tank in m.g.get("tanks", []):
			var tank: Dictionary = raw_tank
			if String(tank["id"]) != id:
				continue
			var pet: Sprite3D = tank["node"]
			if is_instance_valid(pet):
				pet.visible = false
			var marker: Node3D = tank["tag"]
			marker.visible = false
		m.show_msg("Pearl Shop", "The %s is FREE! Go find your new reef friend!" % String(offer["label"]), "win")
		return

func _check_shopper() -> void:
	if bool(m.shop_owned.get("_beans_once", false)):
		m.award_sticker("shopper")
