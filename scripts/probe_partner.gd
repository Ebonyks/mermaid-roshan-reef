extends SceneTree
# PartnerAssist probe: the bubble exists only when a partner is present and
# never fires without a tap (agency); each partner's SUPER does its job —
# stuffie SPARKLE STAMPEDE pops nearest fodder, dizzies the rest and grants
# Big Taps; DADDY SPLASH clears ordinary castle dust but never the Baby
# Eagle rescue pins; the cooldown gates repeat use; and the child's own
# pops shave the partner's rest.

var main: ReefMain
var bad := 0

func _init() -> void:
	seed(20260801)
	Engine.time_scale = 6.0
	var scene: PackedScene = load("res://scenes/main.tscn")
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await process_frame
	await process_frame
	main._skip_intro()
	await process_frame
	await _no_partner_case()
	await _stuffie_case()
	await _daddy_case()
	print("PARTNER|result: ", "ALL OK" if bad == 0 else "%d check(s) FAILED" % bad)
	# tear the scene down before quitting (Windows exit-teardown crash guard)
	get_root().remove_child(main)
	main.free()
	await process_frame
	quit()

func _ck(label: String, ok: bool) -> void:
	print("PARTNER|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		bad += 1

func _no_partner_case() -> void:
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("no companion means no bubble", arena != null and arena.pa == null)
	arena.cancel(false)
	await process_frame

func _stuffie_case() -> void:
	main.companion_id = "eagle"
	main.game = "galaxy"
	main._start_combat("ice")
	await process_frame
	var arena: CombatArena = main.combat_game
	_ck("stuffie bubble attaches ready", arena.pa != null and arena.pa.ready())
	for _i in range(30):
		await process_frame
	var active := 0
	for enemy: Dictionary in arena.enemies:
		if String(enemy["state"]) == "active":
			active += 1
	_ck("idle frames never fire the super", active == 8 and arena.pa.ready())
	arena.pa.on_bubble_tap()
	await process_frame
	var popped_or_frozen := 0
	var stunned := 0
	for enemy: Dictionary in arena.enemies:
		if String(enemy["state"]) != "active":
			popped_or_frozen += 1
		elif float(enemy.get("stun_t", 0.0)) > 0.0:
			stunned += 1
	_ck("stampede pops the nearest fodder",
		popped_or_frozen == PartnerAssist.STAMPEDE_POPS)
	_ck("stampede dizzies the rest",
		stunned == 8 - PartnerAssist.STAMPEDE_POPS)
	_ck("stampede grants Big Taps", arena.he.big_taps == PartnerAssist.BIG_TAPS)
	_ck("super starts the cooldown", not arena.pa.ready())
	var cool_before: float = arena.pa.cool
	arena.pa.on_bubble_tap()
	_ck("resting bubble refuses a tap", absf(arena.pa.cool - cool_before) < 0.001)
	arena.pa.note_child_pop()
	_ck("her own pop shaves the rest",
		cool_before - arena.pa.cool >= PartnerAssist.POP_SHAVE - 0.001)
	arena.cancel(false)
	await process_frame

func _daddy_case() -> void:
	main.companion_id = ""
	main.game = "level2"
	main.g["t"] = 0.0   # the hall clock castle ticks read (probe_combat's pattern)
	var rooms: CastleRooms25D = main._castle_rooms_ref()
	rooms.open("main_hall")
	await process_frame
	await process_frame
	_ck("no pop yet means no daddy bubble", main.castle_partner == null)
	rooms._explode_dust_bunny("sleepy_bunny")
	await process_frame
	_ck("her first pop invites Daddy",
		main.castle_partner != null and main.castle_partner.ready())
	main.castle_partner.on_bubble_tap()
	await process_frame
	_ck("DADDY SPLASH clears the hall dust", _live_dust_count() == 0)
	_ck("the splash starts Daddy's rest", not main.castle_partner.ready())
	# the rescue pins are HER moment: a splash in the playroom spares them
	rooms.show_room("playroom", false)
	await process_frame
	var pins_before: int = _live_dust_count()
	_ck("playroom rescue pins spawn", pins_before == 2)
	main.castle_partner.cool = 0.0
	main.castle_partner.on_bubble_tap()
	await process_frame
	_ck("splash never pops the rescue pins", _live_dust_count() == pins_before)
	rooms.close()
	await process_frame
	_ck("closing the castle stows the bubble", main.castle_partner == null)

func _live_dust_count() -> int:
	var live := 0
	for item_id_value: Variant in main.castle_room_item_sprites:
		var record: Dictionary = main.castle_room_item_sprites[item_id_value] \
			as Dictionary
		var item_data: Dictionary = record.get("data", {}) as Dictionary
		if String(item_data.get("dust_bunny_role", "")) != "":
			live += 1
	return live
