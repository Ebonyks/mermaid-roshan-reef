class_name ShopGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# shop minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = 999.0
	m._build_shop_cabin(origin)
	m.player.position = origin + Vector3(0, 4, 9)
	m.player.vel = Vector3.ZERO
	m.player.yaw = PI
	m.show_msg("Pearl Shop", "Welcome aboard! Swim up to a treasure on the counter to buy it!")

func _tick_shop(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m.hud_game.text = "Pearls: %d - swim to a treasure to buy it!" % m.pearl_count
	m.shop_msg_cool = maxf(0.0, m.shop_msg_cool - delta)
	for it in m.g.get("items", []):
		var inode: Node3D = it["node"]
		if not inode.visible:
			continue
		inode.position.y = (it["base"] as Vector3).y + sin(float(m.g["t"]) * 2.0 + (it["base"] as Vector3).x) * 0.25
		inode.rotate_y(delta * 1.2)
		if m._near_ground(it["base"], ppos, 5.0, 14.0):
			var iid := String(it["id"])
			var price: int = int(it["price"])
			if iid == "beans":
				if m.beans_t >= 0.0:
					pass
				elif m.pearl_count >= price:
					_shop_buy(iid)
					m.show_msg("Pearl Shop", "Beans! Hold on to your tail!")
				elif m.shop_msg_cool <= 0.0:
					m.shop_msg_cool = 2.5
					m.show_msg("Pearl Shop", "Beans cost %d pearls - the reef is full of them!" % price)
			elif m.pearl_count >= price:
				_shop_buy(iid)
				inode.visible = false
				(it["tag"] as Label3D).text = String(it["tag"].text.split("\n")[0]) + "\n(yours!)"
				m.show_msg("Pearl Shop", "It looks WONDERFUL on you!")
			elif m.shop_msg_cool <= 0.0:
				m.shop_msg_cool = 2.5
				m.show_msg("Pearl Shop", "You need %d pearls for that - the reef is full of them!" % price)
	var door: MeshInstance3D = m.g["exit"]
	door.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 3.0) * 0.08)
	# leave the shop by simply swimming OUT of the room (open front / sides)
	var rel: Vector3 = ppos - m.ARENA_POS
	if float(m.g["t"]) > 1.5 and (rel.z > 20.0 or rel.z < -16.0 or absf(rel.x) > 19.0):
		m._end_game(true, fr, "Bye-bye! Come back soon!")

func _shop_buy(id: String) -> void:
	for it in m.SHOP_ITEMS:
		if String(it["id"]) != id or m.pearl_count < int(it["price"]):
			continue
		if id == "beans":
			if m.beans_t < 0.0:
				m.pearl_count -= int(it["price"])
				m.shop_owned["_beans_once"] = true   # counts toward Big Shopper
				m._update_hud()
				m._write_save()
				if m.buy_sound != null:
					m.buy_sound.play()
				m._beans_go()
				m._sparkle_burst(m.player.position + Vector3(0, 1, 0), Color(0.6, 1.0, 0.4))
				_check_shopper()
			return
		# permanent treasures (hard-generated assets only — the early procedural
		# cosmetics were retired; the catalog is beans-only until replacements land)
		if bool(m.shop_owned.get(id, false)):
			return
		m.pearl_count -= int(it["price"])
		m.shop_owned[id] = true
		m._update_hud()
		m._write_save()
		if m.buy_sound != null:
			m.buy_sound.play()
		m._sparkle_burst(m.player.position + Vector3(0, 2, 0), Color(1.0, 0.9, 1.0))
		_check_shopper()
		return

func _check_shopper() -> void:
	# Big Shopper = bought everything in the current catalog (beans once, plus
	# any permanent treasure it lists)
	if not bool(m.shop_owned.get("_beans_once", false)):
		return
	for it in m.SHOP_ITEMS:
		var id := String(it["id"])
		if id != "beans" and not bool(m.shop_owned.get(id, false)):
			return
	m.award_sticker("shopper")
