extends SceneTree
# PROBE_RANK — the bronze/silver/gold ranking gate (see MEDALS.md).
# 1. Tier math: MedalSystem.evaluate() is pure — table-check every game's
#    bronze/silver/gold thresholds, including the compound fairy/penguin rules.
# 2. Floor rule: every completion earns at least bronze; shop is unranked.
# 3. Upgrade-only: a worse replay can never downgrade a saved medal.
# 4. Integration: really WIN the fetch game with live verbs (probe_audit's
#    input loop) and assert a medal lands on m.medals, the HUD, and the save.
# Prints RANK| lines; any FAIL fails CI.
var main: Node3D
var player: Node3D

func _init() -> void:
	seed(20260718)
	Engine.time_scale = 6.0
	var ms: PackedScene = load("res://scenes/main.tscn")
	main = ms.instantiate()
	get_root().add_child(main)
	await process_frame
	await process_frame
	if main.has_method("_skip_intro"):
		main._skip_intro()
	await process_frame
	player = main.player
	print("RANK|boot OK")
	var bad := 0

	# ---- fresh save starts with zero medals ----
	if (main.medals as Dictionary).is_empty():
		print("RANK|fresh state: OK no medals")
	else:
		print("RANK|fresh state: FAIL medals pre-populated ", main.medals)
		bad += 1

	# ---- tier math table (pure evaluate(), no side effects) ----
	var ranker = main._medal_ref()
	var cases := [
		["fetch", {"miss": 0}, 3], ["fetch", {"miss": 2}, 2], ["fetch", {"miss": 3}, 1],
		["dolls", {"missed": 0}, 3], ["dolls", {"missed": 2}, 2], ["dolls", {"missed": 4}, 1],
		["seek", {"slow_find": 8.0}, 3], ["seek", {"slow_find": 20.0}, 2], ["seek", {"slow_find": 40.0}, 1],
		["melody", {"time": 60.0}, 3], ["melody", {"time": 120.0}, 2], ["melody", {"time": 300.0}, 1],
		["slide", {"got": 5}, 3], ["slide", {"got": 3}, 2], ["slide", {"got": 1}, 1],
		["penguin", {"caught": true, "panic": 0}, 3], ["penguin", {"caught": false, "panic": 2}, 2], ["penguin", {"caught": false, "panic": 0}, 1],
		["fairy", {"fails": 0, "hits": 10}, 3], ["fairy", {"fails": 1, "hits": 10}, 2], ["fairy", {"fails": 3, "hits": 4}, 1],
		["race", {"time": 70.0}, 3], ["treasure", {"time": 300.0}, 1],
		["snowman", {"time": 70.0}, 3], ["garden", {"time": 40.0}, 2],
		["trampoline", {"time": 8.0}, 3], ["xmas", {"time": 200.0}, 1],
		["kart", {"place": 1}, 3], ["kart", {"place": 3}, 2], ["kart", {"place": 6}, 1],
		["galaxy", {"time": 300.0}, 3], ["combat_ice", {"time": 100.0}, 2], ["combat_fire", {"time": 400.0}, 1],
		["dungeon", {"rooms": 10}, 3], ["dungeon", {"rooms": 5}, 2], ["dungeon", {"rooms": 1}, 1],
		["bells", {"oops": 0}, 3], ["bells", {"oops": 2}, 2], ["bells", {"oops": 5}, 1],
		["dance", {"combo": 12, "hits": 20}, 3], ["dance", {"combo": 6, "hits": 9}, 2], ["dance", {"combo": 1, "hits": 1}, 1],
		["shop", {}, 0],
	]
	var tiers_bad := 0
	for c in cases:
		var got: int = ranker.evaluate(String(c[0]), c[1] as Dictionary)
		if got != int(c[2]):
			print("RANK|tier math: FAIL ", c[0], " ", c[1], " expected ", c[2], " got ", got)
			tiers_bad += 1
	if tiers_bad == 0:
		print("RANK|tier math: OK ", cases.size(), " threshold cases")
	bad += tiers_bad

	# evaluate() must be pure — the table sweep may not have created medals
	if (main.medals as Dictionary).is_empty():
		print("RANK|evaluate purity: OK")
	else:
		print("RANK|evaluate purity: FAIL evaluate() wrote state ", main.medals)
		bad += 1

	# ---- upgrade-only persistence rule ----
	ranker.award_stats("bells", {"oops": 5})
	var t1: int = int(main.medals.get("bells", 0))
	ranker.award_stats("bells", {"oops": 0})
	var t2: int = int(main.medals.get("bells", 0))
	ranker.award_stats("bells", {"oops": 5})
	var t3: int = int(main.medals.get("bells", 0))
	if t1 == 1 and t2 == 3 and t3 == 3:
		print("RANK|upgrade-only: OK bronze->gold sticks through a worse replay")
	else:
		print("RANK|upgrade-only: FAIL tiers ", [t1, t2, t3], " expected [1, 3, 3]")
		bad += 1

	# ---- integration: win fetch with real verbs, medal must follow ----
	var fetch_f: Dictionary = {}
	for f in main.friends:
		if String(f.get("game", "")) == "fetch":
			fetch_f = f
			break
	if fetch_f.is_empty():
		print("RANK|fetch friend: MISSING")
		bad += 1
	else:
		var node: Node3D = fetch_f["node"]
		player.position = node.position + Vector3(3, 0, 0)
		player.vel = Vector3.ZERO
		await _frames(10)
		var guard := 0
		while float(fetch_f["cool"]) > 0.0 and guard < 3000:
			guard += 1
			await process_frame
		for k in range(10):
			player.position = node.position + Vector3(3, 0, 0)
			player.vel = Vector3.ZERO
			await process_frame
		if main.game != "fetch":
			print("RANK|fetch: GAME DID NOT START")
			bad += 1
		else:
			var won: bool = await _drive_fetch(fetch_f)
			var medal: int = int(main.medals.get("fetch", 0))
			if won and medal >= 1:
				print("RANK|fetch win medal: OK tier ", medal)
			else:
				print("RANK|fetch win medal: FAIL won=", won, " tier=", medal)
				bad += 1
			if String(main.hud_stars.text).contains("🥉") or String(main.hud_stars.text).contains("🥈") or String(main.hud_stars.text).contains("🥇"):
				print("RANK|hud tally: OK")
			else:
				print("RANK|hud tally: FAIL '", main.hud_stars.text, "'")
				bad += 1

	# ---- medals survive the save file round trip ----
	await _frames(30)
	var persisted := false
	var fh := FileAccess.open("user://reef_save.json", FileAccess.READ)
	if fh != null:
		var parsed: Variant = JSON.parse_string(fh.get_as_text())
		fh.close()
		if parsed is Dictionary:
			var md: Variant = (parsed as Dictionary).get("medals", {})
			persisted = md is Dictionary and int((md as Dictionary).get("bells", 0)) == 3 \
				and int((md as Dictionary).get("fetch", 0)) == int(main.medals.get("fetch", 0)) \
				and (parsed as Dictionary).has("won")
	if persisted:
		print("RANK|save round trip: OK medals + won intact")
	else:
		print("RANK|save round trip: FAIL")
		bad += 1

	print("RANK|result: ", ("ALL OK" if bad == 0 else "%d check(s) FAILED" % bad))
	quit()

func _frames(n: int):
	for i in range(n):
		await process_frame

func _drive_fetch(f: Dictionary) -> bool:
	# same live-verb loop probe_audit uses: press the button while the arrow
	# aims at safe snow, release otherwise, until Chuck brings the ball home
	var deadline := 60.0 * 90.0
	var fcount := 0
	player.position = main.ARENA_POS + Vector3(0, 8, 18)
	player.vel = Vector3.ZERO
	while main.game != "" and fcount < deadline:
		fcount += 1
		var g: Dictionary = main.g
		if g.has("phase") and String(g["phase"]) == "aim":
			var ad: Vector3 = g.get("aim_dir", Vector3.ZERO)
			main.touch_ui.action_down = ad != Vector3.ZERO and ad.x < 0.1 and fcount % 12 < 6
		else:
			main.touch_ui.action_down = false
		await process_frame
	main.touch_ui.action_down = false
	return main.game == "" and bool(f["won"])
