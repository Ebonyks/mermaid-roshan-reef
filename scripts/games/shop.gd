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
	m.show_msg("Pearl Shop", "Welcome aboard! Treasures on the counter - and new reef friends in the tanks!")

func _tick_shop(delta: float, fr: Dictionary, ppos: Vector3) -> void:
	m.hud_game.text = "Pearls: %d - swim to a treasure or a tank friend to buy it!" % m.pearl_count
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
	for tk in m.g.get("tanks", []):
		var tid := String(tk["id"])
		var pet: Node3D = tk["node"]
		if pet != null and is_instance_valid(pet) and pet.visible:
			# little laps inside the glass so the tank reads alive: x sweeps on a
			# sine, and the friend turns to face its swim direction (creatures
			# face -X at rotation.y 0 - same convention the reef movers steer).
			# On top of the lap, EACH species plays its own close-up idle -
			# this is what she watches while deciding to buy.
			var tt: float = float(m.g["t"])
			var base: Vector3 = tk["base"]
			var ph: float = float(tk["ph"])
			var rate: float = 0.9
			var sweep: float = 1.1
			if tid == "turtle":
				rate = 0.55        # turtles glide, they don't dart
			elif tid == "stingray":
				rate = 0.7
			elif tid == "squid":
				rate = 0.5
				sweep = 0.4        # squid mostly hovers and breathes
			var swim := sin(tt * rate + ph)
			pet.position.x = base.x + swim * sweep
			var going: float = cos(tt * rate + ph)
			pet.rotation.y = lerp_angle(pet.rotation.y, 0.0 if going < 0.0 else PI, delta * 4.0)
			if tid == "turtle":
				# the full skeleton: flipper power strokes, rudder paddles,
				# curious look-around (built by _rig_turtle's motion cage)
				pet.position.y = base.y - 0.3 + sin(tt * 0.8 + ph) * 0.08
				if not (tk["rig"] as Dictionary).is_empty():
					m._turtle_idle(tk["rig"], tt)
			elif tid == "dolphin":
				# porpoise arcs: two gentle rises per lap
				pet.position.y = base.y - 0.3 + sin(tt * rate * 2.0 + ph) * 0.22
			elif tid == "stingray":
				# wing-heavy glide (boosted sway) with a lazy banking roll
				pet.position.y = base.y - 0.3 + sin(tt * 0.6 + ph) * 0.12
				pet.rotation.z = sin(tt * 0.8 + ph) * 0.08
			elif tid == "squid":
				# jet breathing: squash-and-stretch synced to a drifting bob
				var pulse := sin(tt * 2.6 + ph)
				pet.scale = Vector3(1.0 - pulse * 0.03, 1.0 + pulse * 0.06, 1.0 - pulse * 0.03)
				pet.position.y = base.y - 0.3 + sin(tt * 2.6 + ph - 0.7) * 0.10
		if bool(m.animals_owned.get(tid, false)):
			continue
		if m._near_ground(tk["base"], ppos, 5.5, 7.0):
			var tprice: int = int(tk["price"])
			if m.pearl_count >= tprice:
				_tank_buy(tid)
			elif m.shop_msg_cool <= 0.0:
				m.shop_msg_cool = 2.5
				m.show_msg("Pearl Shop", "This friend costs %d pearls - the reef is full of them!" % tprice)
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

func _tank_buy(id: String) -> void:
	# release a tank friend into the reef: deduct pearls, persist, spawn its
	# patrols + babies right away so it is already swimming when she leaves.
	# Callable outside the shop scene too (probes) - the tank visuals are only
	# touched when the cabin is actually built.
	for it in m.ANIMAL_SHOP:
		if String(it["id"]) != id:
			continue
		if bool(m.animals_owned.get(id, false)) or m.pearl_count < int(it["price"]):
			return
		m.pearl_count -= int(it["price"])
		m.animals_owned[id] = true
		m._spawn_shop_animals()
		m._update_hud()
		m._write_save()
		if m.buy_sound != null:
			m.buy_sound.play()
		m._sparkle_burst(m.player.position + Vector3(0, 2, 0), Color(0.5, 1.0, 0.9))
		for tk in m.g.get("tanks", []):
			if String(tk["id"]) != id:
				continue
			var pet: Node3D = tk["node"]
			if pet != null and is_instance_valid(pet):
				pet.visible = false
			(tk["tag"] as Label3D).text = "%s\n(set free!)" % String(it["label"])
		m.show_msg("Pearl Shop", "The %s is FREE! It lives in YOUR reef now - go find it!" % String(it["label"]), "win")
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
