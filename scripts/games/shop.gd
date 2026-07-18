class_name ShopGame
extends RefCounted
# Phase 7.4: mechanical extraction from main.gd — builder + tick for the
# shop minigame. All state stays on main (m.*); received by reference.

var m: ReefMain

func _init(main: ReefMain) -> void:
	m = main

func _build_shop_cabin(origin: Vector3) -> void:
	var f: float = m.ARENA_POS.y + 2.0
	# A single authored open-front diorama replaces the repeated all-surface wood
	# sheet. The broad floor/wall panels retain the cozy cabin role while giving
	# the shop a distinct shell emblem, canopy, palette, and readable counter.
	m._art35_prop("res://assets/art35/arena/shop_interior.glb", Vector3(origin.x, f - 0.5, origin.z), 1.0)
	# collision audit #4: the cabin walls were swim-through
	m._wall_solid(Vector3(origin.x, f + 9.0, origin.z - 13.0), Vector3(34, 19, 1.2), 0.5)
	m._wall_solid(Vector3(origin.x - 16.0, f + 9.0, origin.z + 2.0), Vector3(1.2, 19, 30), 0.5)
	m._wall_solid(Vector3(origin.x + 16.0, f + 9.0, origin.z + 2.0), Vector3(1.2, 19, 30), 0.5)
	# warm hanging lanterns
	for lx in [-7.0, 7.0]:
		var lamp := OmniLight3D.new()
		lamp.light_color = Color(1.0, 0.78, 0.45)
		lamp.light_energy = 2.4
		lamp.omni_range = 22.0
		lamp.position = Vector3(origin.x + lx, f + 12.0, origin.z - 2.0)
		m.add_child(lamp)
		m.game_nodes.append(lamp)
		var bulb := MeshInstance3D.new()
		var bm3 := SphereMesh.new()
		bm3.radius = 0.3
		bm3.height = 0.6
		bulb.mesh = bm3
		var bmat3 := StandardMaterial3D.new()
		bmat3.emission_enabled = true
		bmat3.emission = Color(1.0, 0.8, 0.45)
		bmat3.emission_energy_multiplier = 3.5
		bulb.material_override = bmat3
		bulb.position = lamp.position
		m.add_child(bulb)
		m.game_nodes.append(bulb)
		var cord := m._course_box(lamp.position + Vector3(0, 3.0, 0), Vector3(0.12, 6.0, 0.12), Color(0.25, 0.18, 0.1))
		cord.material_override.emission_enabled = false
	# hanging kelp bunches like dried herbs — spring pendulums (PHYSICS LAB)
	m.g["kelp"] = []
	for hk in range(5):
		var bunch := MeshInstance3D.new()
		bunch.mesh = m._cross_blade(0.5, 2.2)
		bunch.material_override = m._sway_grass_mat(Color(0.2, 0.25, 0.1), Color(0.45, 0.5, 0.2))
		bunch.position = Vector3(origin.x - 10.0 + float(hk) * 5.0, f + 15.5, origin.z - 9.0)
		bunch.rotation_degrees = Vector3(180, randf() * 360.0, 0)
		m.add_child(bunch)
		m.game_nodes.append(bunch)
		(m.g["kelp"] as Array).append({"node": bunch, "yaw": bunch.rotation.y, "ang": Vector2.ZERO, "vel": Vector2.ZERO})
	# Kareem is the living shopkeeper, a billboard sprite sitting beside his goods
	var kareem := Sprite3D.new()
	kareem.texture = load("res://assets/characters/friends/kareem.png")
	kareem.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	kareem.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	kareem.pixel_size = 0.02
	kareem.position = Vector3(origin.x + 9.5, f + 5.5, origin.z - 6.0)
	m.add_child(kareem)
	m.game_nodes.append(kareem)
	var kspot := OmniLight3D.new()
	kspot.light_color = Color(1.0, 0.92, 0.8)
	kspot.light_energy = 1.6
	kspot.omni_range = 16.0
	kspot.position = kareem.position + Vector3(0, 3, 3)
	m.add_child(kspot)
	m.game_nodes.append(kspot)
	var klbl := Label3D.new()
	klbl.text = "Kareem's Shop"
	klbl.font_size = 60
	klbl.pixel_size = 0.02
	klbl.outline_size = 12
	klbl.modulate = Color(1.0, 0.9, 0.6)
	klbl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	klbl.position = Vector3(origin.x, f + 14.0, origin.z - 9.0)
	m.add_child(klbl)
	m.game_nodes.append(klbl)
	# wares on the counter — spread evenly around the middle
	m.g["items"] = []
	for ii in range(m.SHOP_ITEMS.size()):
		var it: Dictionary = m.SHOP_ITEMS[ii]
		var iid := String(it["id"])
		var ipos := Vector3(origin.x + (float(ii) - float(m.SHOP_ITEMS.size() - 1) * 0.5) * 4.3, f + 2.2, origin.z - 4.6)
		# the legendary Can of Beans
		var can := MeshInstance3D.new()
		var cyl := CylinderMesh.new()
		cyl.top_radius = 0.45
		cyl.bottom_radius = 0.45
		cyl.height = 1.1
		can.mesh = cyl
		var tin := StandardMaterial3D.new()
		tin.albedo_color = Color(0.75, 0.78, 0.8)
		tin.metallic = 0.9
		tin.roughness = 0.3
		can.material_override = tin
		var lbl := MeshInstance3D.new()
		var lcyl := CylinderMesh.new()
		lcyl.top_radius = 0.47
		lcyl.bottom_radius = 0.47
		lcyl.height = 0.6
		lbl.mesh = lcyl
		var lm2 := StandardMaterial3D.new()
		lm2.albedo_color = Color(0.85, 0.3, 0.2)
		lm2.roughness = 0.8
		lbl.material_override = lm2
		can.add_child(lbl)
		var inode: Node3D = can
		inode.position = ipos
		m.add_child(inode)
		m.game_nodes.append(inode)
		var tag := Label3D.new()
		tag.text = "%s\n%d pearls" % [String(it["label"]), int(it["price"])]
		tag.font_size = 64
		tag.modulate = Color(1.0, 0.95, 0.8)
		tag.outline_size = 14
		tag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		tag.position = ipos + Vector3(0, 1.7, 0)
		m.add_child(tag)
		m.game_nodes.append(tag)
		(m.g["items"] as Array).append({"id": iid, "node": inode, "tag": tag, "price": int(it["price"]), "base": ipos})
	# ANIMAL TANKS: glass tanks mounted on the back wall, each holding a reef
	# friend Kareem will sell. Swim up with enough pearls and it goes FREE -
	# out of the tank and into the reef forever (ANIMAL_SHOP / _tank_buy).
	m.g["tanks"] = []
	var tank_slots := [-10.5, -3.5, 3.5, 10.5]
	for ti in range(m.ANIMAL_SHOP.size()):
		var ta: Dictionary = m.ANIMAL_SHOP[ti]
		var tid := String(ta["id"])
		var tpos := Vector3(origin.x + tank_slots[ti], f + 8.8, origin.z - 11.4)
		# wooden shelf, then the glass box on top
		var shelf := m._course_box(tpos + Vector3(0, -2.2, 0), Vector3(6.0, 0.5, 3.2), Color(0.45, 0.3, 0.18))
		shelf.material_override.roughness = 1.0
		var glass := MeshInstance3D.new()
		var gbox := BoxMesh.new()
		gbox.size = Vector3(5.6, 3.6, 2.8)
		glass.mesh = gbox
		var gmat := StandardMaterial3D.new()
		gmat.albedo_color = Color(0.55, 0.85, 1.0, 0.22)
		gmat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		gmat.metallic = 0.2
		gmat.roughness = 0.05
		gmat.cull_mode = BaseMaterial3D.CULL_DISABLED
		glass.material_override = gmat
		glass.position = tpos
		m.add_child(glass)
		m.game_nodes.append(glass)
		# a strip of sand so it reads "little home", not "specimen jar"
		var sand := m._course_box(tpos + Vector3(0, -1.6, 0), Vector3(5.2, 0.35, 2.4), Color(0.93, 0.85, 0.6))
		sand.material_override.roughness = 1.0
		# the friend swimming inside — each species gets its own close-up idle:
		# the turtle a full skeleton (fin strokes via _rig_turtle), the others
		# a boosted sway so wing/jet/tail motion reads through the glass
		var pet: Node3D = null
		var trig := {}
		if m.CREATURE_GEN2.has(String(ta["model"])):
			pet = m._gen2_creature(String(m.CREATURE_GEN2[String(ta["model"])]), tpos + Vector3(0, -0.3, 0), 2.2)
		if pet != null:
			m.game_nodes.append(pet)
			if tid == "turtle":
				trig = m._rig_turtle(pet, 2.4)
				m._set_sway(pet, 0.02)   # the skeleton owns the motion now
			elif tid == "stingray":
				m._set_sway(pet, 0.22)
			elif tid == "squid":
				m._set_sway(pet, 0.18)
			elif tid == "dolphin":
				m._set_sway(pet, 0.13)
		var ttag := Label3D.new()
		ttag.text = "%s\n%d pearls" % [String(ta["label"]), int(ta["price"])]
		ttag.font_size = 64
		ttag.modulate = Color(0.75, 1.0, 0.95)
		ttag.outline_size = 14
		ttag.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		ttag.position = tpos + Vector3(0, 2.6, 0.6)
		m.add_child(ttag)
		m.game_nodes.append(ttag)
		if bool(m.animals_owned.get(tid, false)):
			if pet != null:
				pet.visible = false
			ttag.text = "%s\n(set free!)" % String(ta["label"])
		(m.g["tanks"] as Array).append({"id": tid, "node": pet, "tag": ttag, "price": int(ta["price"]), "base": tpos, "ph": randf() * TAU, "rig": trig})
	# glowing exit door
	var door := MeshInstance3D.new()
	var dt := TorusMesh.new()
	dt.inner_radius = 2.4
	dt.outer_radius = 3.1
	door.mesh = dt
	door.rotation_degrees = Vector3(90, 0, 0)
	var dm := StandardMaterial3D.new()
	dm.albedo_color = Color(0.5, 0.9, 1.0)
	dm.emission_enabled = true
	dm.emission = Color(0.4, 0.85, 1.0)
	dm.emission_energy_multiplier = 1.8
	door.material_override = dm
	door.position = Vector3(origin.x - 12.0, f + 4.0, origin.z + 14.5)
	m.add_child(door)
	m.game_nodes.append(door)
	m.g["exit"] = door
	var dl := Label3D.new()
	dl.text = "\u2190 swim out to leave"
	dl.font_size = 56
	dl.outline_size = 12
	dl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	dl.position = door.position + Vector3(0, 3.6, 0)
	m.add_child(dl)
	m.game_nodes.append(dl)

func build(fr: Dictionary, origin: Vector3) -> void:
	m.g["timer"] = -1.0
	_build_shop_cabin(origin)
	# The old trail/tiara/skin wares no longer have visible, fitted rewards.
	# Keep their save keys for compatibility, but do not display or sell a
	# promise the game cannot currently keep. Center the one real counter item.
	for it in m.g.get("items", []):
		var iid := String(it["id"])
		var inode: Node3D = it["node"]
		var tag: Label3D = it["tag"]
		if iid != "beans":
			inode.visible = false
			tag.visible = false
			continue
		var base: Vector3 = it["base"]
		var center_shift := Vector3(origin.x - base.x, 0.0, 0.0)
		base += center_shift
		it["base"] = base
		inode.position += center_shift
		tag.position += center_shift
	m.g["shop_action_down"] = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_ENTER) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
	m.g["shop_wait_release"] = bool(m.g["shop_action_down"])
	m.player.position = origin + Vector3(0, 4, 9)
	m.player.vel = Vector3.ZERO
	m.player.yaw = PI
	m.show_msg("Pearl Shop", "Welcome aboard! Swim close, then tap to buy Beans or set a reef friend free!")

func _purchase_action_just() -> bool:
	# Proximity chooses an item; a separate tap/press confirms the purchase.
	# Latching keyboard/gamepad input prevents a held button buying twice.
	var down: bool = Input.is_physical_key_pressed(KEY_SPACE) or Input.is_physical_key_pressed(KEY_ENTER) or m.joy_pressed(JOY_BUTTON_A) or m.joy_pressed(JOY_BUTTON_B)
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
	m.hud_game.text = "Pearls: %d - swim close, then tap the pink button to buy" % m.pearl_count
	m.shop_msg_cool = maxf(0.0, m.shop_msg_cool - delta)
	var buy_pressed := _purchase_action_just()
	var choice_kind := ""
	var choice_id := ""
	var choice_price := 0
	var choice_dist := 1e20
	# PHYSICS LAB: hanging kelp = damped spring pendulums, swing when brushed
	if m.foliage_push_enabled:
		for kd in m.g.get("kelp", []):
			var bn: MeshInstance3D = kd["node"]
			if not is_instance_valid(bn):
				continue
			var ang0: Vector2 = kd["ang"]
			var tip: Vector3 = bn.position + Vector3(ang0.x, -1.0, ang0.y).normalized() * 2.0
			var dd: float = tip.distance_to(ppos)
			if dd < 2.4:
				var push := Vector2(tip.x - ppos.x, tip.z - ppos.z)
				if push.length() > 0.01:
					kd["vel"] = (kd["vel"] as Vector2) + push.normalized() * (2.4 - dd) * 12.0 * delta
			ReefPhysics.spring2(kd, 6.0, 1.5, delta)
			var ang: Vector2 = kd["ang"]
			bn.rotation = Vector3(PI - ang.y * 0.8, float(kd["yaw"]), ang.x * 0.8)
	for it in m.g.get("items", []):
		var inode: Node3D = it["node"]
		if not inode.visible:
			continue
		inode.position.y = (it["base"] as Vector3).y + sin(float(m.g["t"]) * 2.0 + (it["base"] as Vector3).x) * 0.25
		inode.rotate_y(delta * 1.2)
		if m._near_ground(it["base"], ppos, 5.0, 14.0):
			var iid := String(it["id"])
			var price: int = int(it["price"])
			var item_delta: Vector3 = (it["base"] as Vector3) - ppos
			var item_dist: float = Vector2(item_delta.x, item_delta.z).length_squared()
			if iid == "beans" and item_dist < choice_dist:
				choice_kind = "beans"
				choice_id = iid
				choice_price = price
				choice_dist = item_dist
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
			var tank_delta: Vector3 = (tk["base"] as Vector3) - ppos
			var tank_dist: float = Vector2(tank_delta.x, tank_delta.z).length_squared()
			if tank_dist < choice_dist:
				choice_kind = "friend"
				choice_id = tid
				choice_price = tprice
				choice_dist = tank_dist
	if choice_id != "":
		if choice_kind == "beans" and m.beans_t >= 0.0:
			m.hud_game.text = "Bean power is already bubbling!"
			if buy_pressed and m.shop_msg_cool <= 0.0:
				m.shop_msg_cool = 2.5
				m.show_msg("Pearl Shop", "You already have bean power — enjoy the ride!")
		elif m.pearl_count < choice_price:
			m.hud_game.text = "Pearls: %d / %d" % [m.pearl_count, choice_price]
			if buy_pressed and m.shop_msg_cool <= 0.0:
				m.shop_msg_cool = 2.5
				m.show_msg("Pearl Shop", "That costs %d pearls — the reef is full of them!" % choice_price)
		else:
			m.hud_game.text = "Pearls: %d - tap the pink button to choose!" % m.pearl_count
			if buy_pressed:
				if choice_kind == "beans":
					_shop_buy(choice_id)
					m.show_msg("Pearl Shop", "Beans! Hold on to your tail!")
				else:
					_tank_buy(choice_id)
	var door: MeshInstance3D = m.g["exit"]
	door.scale = Vector3.ONE * (1.0 + sin(float(m.g["t"]) * 3.0) * 0.08)
	# leave the shop by simply swimming OUT of the room (open front / sides)
	var rel: Vector3 = ppos - m.ARENA_POS
	if float(m.g["t"]) > 1.5 and (rel.z > 20.0 or rel.z < -16.0 or absf(rel.x) > 19.0):
		m._end_game(true, fr, "Bye-bye! Come back soon!")

func _shop_buy(id: String) -> void:
	# Retired cosmetic ids remain in saves and SHOP_ITEMS for compatibility,
	# but cannot be bought until they have a visible fitted reward again.
	if id != "beans":
		return
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
	# Beans are the only current counter item. The old cosmetic keys stay in
	# saves but no longer block the shopping sticker.
	if not bool(m.shop_owned.get("_beans_once", false)):
		return
	m.award_sticker("shopper")
