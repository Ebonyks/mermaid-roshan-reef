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

const CELEBRATION_BOUNDS := Rect2(Vector2.ZERO, Vector2(1280.0, 720.0))
const CELEBRATION_MAX_SUBTREE_NODES := 16


func _celebration_layer() -> CanvasLayer:
	return main.get_node_or_null("MedalCelebrationLayer") as CanvasLayer


func _active_celebration_count() -> int:
	var total := 0
	for child_value in main.get_children():
		var child := child_value as Node
		if child != null and child.name == &"MedalCelebrationLayer":
			total += 1
	return total


func _direct_child_ids() -> Dictionary:
	var ids: Dictionary = {}
	for child_value in main.get_children():
		var child := child_value as Node
		if child != null:
			ids[child.get_instance_id()] = true
	return ids


func _only_celebration_added(
		baseline: Dictionary, layer: CanvasLayer) -> bool:
	if layer == null or not is_instance_valid(layer) \
			or baseline.has(layer.get_instance_id()):
		return false
	var current: Dictionary = _direct_child_ids()
	if current.size() != baseline.size() + 1 \
			or not current.has(layer.get_instance_id()):
		return false
	for instance_id: Variant in baseline:
		if not current.has(instance_id):
			return false
	return true


func _subtree_node_count(node: Node) -> int:
	var total := 1
	for child_value in node.get_children():
		var child := child_value as Node
		if child != null:
			total += _subtree_node_count(child)
	return total


func _tween_stopped(tween: Tween) -> bool:
	return tween == null or not tween.is_valid() or not tween.is_running()


func _celebration_contract(layer: CanvasLayer, tier: int) -> bool:
	if layer == null or not is_instance_valid(layer) or not layer.visible \
			or layer.layer != 23 or int(layer.get_meta("celebration_tier", 0)) != tier:
		return false
	var card := layer.get_node_or_null("MedalCelebrationCard") as Panel
	var glyph := layer.get_node_or_null(
		"MedalCelebrationCard/MedalCelebrationGlyph") as Label
	var burst := layer.get_node_or_null("MedalCelebrationBurst") as Control
	if card == null or glyph == null or burst == null \
			or card.position != Vector2(490.0, 140.0) \
			or card.size != Vector2(300.0, 230.0) \
			or glyph.text != String(MedalSystem.GLYPH[tier]) \
			or burst.position != Vector2(640.0, 255.0) \
			or not CELEBRATION_BOUNDS.has_point(burst.position):
		return false
	var expected_elements: int = int(MedalSystem.CELEBRATION_ELEMENTS[tier])
	if int(burst.get_meta("visible_elements", 0)) != expected_elements \
			or burst.get_child_count() != expected_elements \
			or _subtree_node_count(layer) > CELEBRATION_MAX_SUBTREE_NODES:
		return false
	var style := card.get_theme_stylebox("panel") as StyleBoxFlat
	var tier_color: Color = MedalSystem.TIER_COLOR[tier]
	if style == null or not style.border_color.is_equal_approx(
			tier_color.lerp(StorybookUI.PURPLE_DEEP, 0.62)):
		return false
	for element_value in burst.get_children():
		var element := element_value as Polygon2D
		if element == null or not element.visible or element.modulate.a <= 0.95 \
				or element.polygon.size() != 8 \
				or not CELEBRATION_BOUNDS.has_point(
					burst.position + element.position):
			return false
		var endpoint: Vector2 = element.get_meta(
			"feedback_endpoint", Vector2.ZERO) as Vector2
		if not CELEBRATION_BOUNDS.has_point(burst.position + endpoint):
			return false
	return true


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
		["fairy", {"fails": 0, "hits": 7}, 3], ["fairy", {"fails": 1, "hits": 7}, 2], ["fairy", {"fails": 3, "hits": 4}, 1],
		["race", {"time": 70.0}, 3], ["treasure", {"time": 300.0}, 1],
		["snowman", {"time": 70.0}, 3], ["garden", {"time": 40.0}, 2],
		["trampoline", {"time": 8.0}, 3], ["xmas", {"time": 200.0}, 1],
		["kart", {"place": 1}, 3], ["kart", {"place": 3}, 2], ["kart", {"place": 6}, 1],
		["galaxy", {"time": 300.0}, 3], ["combat_ice", {"time": 100.0}, 2], ["combat_fire", {"time": 400.0}, 1],
		["dungeon", {"rooms": 10}, 3], ["dungeon", {"rooms": 5}, 2], ["dungeon", {"rooms": 1}, 1],
		["bells", {"oops": 0}, 3], ["bells", {"oops": 2}, 2], ["bells", {"oops": 5}, 1],
		["dance", {"combo": 12, "hits": 20}, 3], ["dance", {"combo": 6, "hits": 9}, 2], ["dance", {"combo": 1, "hits": 1}, 1],
		["dustboss", {"wasted": 0}, 3], ["dustboss", {"wasted": 2}, 2], ["dustboss", {"wasted": 9}, 1],
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

	# ---- upgrade-only persistence + bounded award feedback ----
	var direct_child_baseline: Dictionary = _direct_child_ids()
	ranker.award_stats("bells", {"oops": 5})
	var t1: int = int(main.medals.get("bells", 0))
	var bronze_layer: CanvasLayer = _celebration_layer()
	var bronze_layer_ref: WeakRef = weakref(bronze_layer)
	var bronze_feedback_tween: Tween = bronze_layer.get_meta(
		"feedback_tween") as Tween if bronze_layer != null else null
	var bronze_teardown_tween: Tween = bronze_layer.get_meta(
		"teardown_tween") as Tween if bronze_layer != null else null
	var bronze_feedback_ok: bool = _active_celebration_count() == 1 \
		and _celebration_contract(bronze_layer, MedalSystem.BRONZE) \
		and _only_celebration_added(direct_child_baseline, bronze_layer) \
		and main.chime != null \
		and is_equal_approx(float(main.chime.pitch_scale), 1.15)
	ranker.award_stats("bells", {"oops": 0})
	var t2: int = int(main.medals.get("bells", 0))
	var gold_layer: CanvasLayer = _celebration_layer()
	var gold_layer_ref: WeakRef = weakref(gold_layer)
	var gold_feedback_tween: Tween = gold_layer.get_meta(
		"feedback_tween") as Tween if gold_layer != null else null
	var gold_teardown_tween: Tween = gold_layer.get_meta(
		"teardown_tween") as Tween if gold_layer != null else null
	var bronze_replaced: bool = bronze_layer != null and gold_layer != null \
		and bronze_layer != gold_layer and bronze_layer.get_parent() == null \
		and not bronze_layer.visible \
		and _tween_stopped(bronze_feedback_tween) \
		and _tween_stopped(bronze_teardown_tween)
	var gold_feedback_ok: bool = _active_celebration_count() == 1 \
		and _celebration_contract(gold_layer, MedalSystem.GOLD) \
		and _only_celebration_added(direct_child_baseline, gold_layer) \
		and main.chime != null \
		and is_equal_approx(float(main.chime.pitch_scale), 1.45)
	ranker.award_stats("bells", {"oops": 5})
	var t3: int = int(main.medals.get("bells", 0))
	var replay_layer: CanvasLayer = _celebration_layer()
	var replay_layer_ref: WeakRef = weakref(replay_layer)
	var replay_instance_id: int = replay_layer.get_instance_id() \
		if replay_layer != null else -1
	var replay_feedback_tween: Tween = replay_layer.get_meta(
		"feedback_tween") as Tween if replay_layer != null else null
	var replay_teardown_tween: Tween = replay_layer.get_meta(
		"teardown_tween") as Tween if replay_layer != null else null
	var gold_replaced: bool = gold_layer != null and replay_layer != null \
		and gold_layer != replay_layer and gold_layer.get_parent() == null \
		and not gold_layer.visible \
		and _tween_stopped(gold_feedback_tween) \
		and _tween_stopped(gold_teardown_tween)
	var replay_feedback_ok: bool = _active_celebration_count() == 1 \
		and _celebration_contract(replay_layer, MedalSystem.BRONZE) \
		and _only_celebration_added(direct_child_baseline, replay_layer) \
		and t3 == MedalSystem.GOLD \
		and main.chime != null \
		and is_equal_approx(float(main.chime.pitch_scale), 1.15)
	if t1 == 1 and t2 == 3 and t3 == 3:
		print("RANK|upgrade-only: OK bronze->gold sticks through a worse replay")
	else:
		print("RANK|upgrade-only: FAIL tiers ", [t1, t2, t3], " expected [1, 3, 3]")
		bad += 1
	await process_frame
	await process_frame
	var rapid_cleanup_ok: bool = bronze_layer_ref.get_ref() == null \
		and gold_layer_ref.get_ref() == null
	if bronze_feedback_ok and gold_feedback_ok and replay_feedback_ok \
			and bronze_replaced and gold_replaced and rapid_cleanup_ok:
		print("RANK|award feedback: OK bounded Canvas burst + rapid replacement")
	else:
		print("RANK|award feedback: FAIL bronze=", bronze_feedback_ok,
			" gold=", gold_feedback_ok, " replay=", replay_feedback_ok,
			" replace=", [bronze_replaced, gold_replaced],
			" old_freed=", rapid_cleanup_ok)
		bad += 1
	var teardown_guard := 0
	while replay_layer_ref.get_ref() != null and teardown_guard < 240:
		teardown_guard += 1
		await process_frame
	var teardown_ok: bool = replay_layer_ref.get_ref() == null \
		and _active_celebration_count() == 0 \
		and _tween_stopped(replay_feedback_tween) \
		and _tween_stopped(replay_teardown_tween)
	var fresh_child_baseline: Dictionary = _direct_child_ids()
	ranker.award_stats("bells", {"oops": 5})
	var fresh_layer: CanvasLayer = _celebration_layer()
	var fresh_layer_ref: WeakRef = weakref(fresh_layer)
	var fresh_feedback_tween: Tween = fresh_layer.get_meta(
		"feedback_tween") as Tween if fresh_layer != null else null
	var fresh_teardown_tween: Tween = fresh_layer.get_meta(
		"teardown_tween") as Tween if fresh_layer != null else null
	var fresh_ok: bool = teardown_ok and fresh_layer != null \
		and fresh_layer.get_instance_id() != replay_instance_id \
		and _active_celebration_count() == 1 \
		and _celebration_contract(fresh_layer, MedalSystem.BRONZE) \
		and _only_celebration_added(fresh_child_baseline, fresh_layer) \
		and int(main.medals.get("bells", 0)) == MedalSystem.GOLD \
		and main.chime != null \
		and is_equal_approx(float(main.chime.pitch_scale), 1.15)
	var fresh_guard := 0
	while fresh_layer_ref.get_ref() != null and fresh_guard < 240:
		fresh_guard += 1
		await process_frame
	var fresh_cleanup_ok: bool = fresh_layer_ref.get_ref() == null \
		and _active_celebration_count() == 0 \
		and _tween_stopped(fresh_feedback_tween) \
		and _tween_stopped(fresh_teardown_tween)
	if fresh_ok and fresh_cleanup_ok:
		print("RANK|award feedback lifecycle: OK teardown + clean re-entry")
	else:
		print("RANK|award feedback lifecycle: FAIL teardown=", teardown_ok,
			" fresh=", fresh_ok, " fresh_cleanup=", fresh_cleanup_ok,
			" guards=", [teardown_guard, fresh_guard])
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
		if main.game == "" and main.touch_uses_explicit_interactions():
			var fetch_index: int = main.friends.find(fetch_f)
			main._activate_touch_interactable("friend:%d" % fetch_index, fetch_index)
			await _frames(10)
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
