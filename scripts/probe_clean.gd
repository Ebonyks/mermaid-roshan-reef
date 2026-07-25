extends SceneTree

# Cleaning Day (Sparkle Scrub) probe.
#
# Covers the DIRTY_CASTLE_2D_GODOT_HANDOFF acceptance points that a headless
# bot can prove: every runtime skin resolves and is unshaded/uncoloured, the
# 2D layer adds no collider and no OmniLight, a tap target and a rub (swipe)
# target both clean, state saves per object, a reload restores the exact set,
# and — the agency rule — nothing completes while the child does nothing.

const SKIN := "res://assets/castle/dirty_cleanup_2d/"

var main: ReefMain
var checks_failed := 0


func _ck(label: String, ok: bool, detail: String = "") -> void:
	if not ok:
		checks_failed += 1
	print("CLEAN|", label, "|", "OK" if ok else "FAIL", "|", detail)


func _frames(count: int) -> void:
	for _index in range(count):
		await process_frame


func _audit_pack() -> void:
	# every path the room table names must exist and be a 512px RGBA sprite
	var missing: Array[String] = []
	var wrong_size: Array[String] = []
	var target_total := 0
	for room_value: Variant in CastleCleanup.ROOMS:
		var room: Dictionary = room_value as Dictionary
		var paths: Array[String] = [String(room["vignette"]), String(room["tool"])]
		for target_value: Variant in (room["targets"] as Array):
			var target: Dictionary = target_value as Dictionary
			paths.append(String(target["tex"]))
			target_total += 1
		for rel: String in paths:
			var path: String = SKIN + rel
			if not ResourceLoader.exists(path):
				missing.append(rel)
				continue
			var tex: Texture2D = load(path) as Texture2D
			if tex == null or tex.get_width() != 512 or tex.get_height() != 512:
				wrong_size.append(rel)
	_ck("pack_paths_resolve", missing.is_empty(), "missing=%s" % [missing])
	_ck("pack_render_contract", wrong_size.is_empty(), "non-512px=%s" % [wrong_size])
	_ck("pack_target_count", target_total == 30, "room-bound object skins=%d" % target_total)
	for fx: String in ["effects/fx_clean_ring.png", "effects/fx_dust_poof.png",
			"effects/fx_soap_bubbles.png", "effects/fx_gold_sparkle.png",
			"effects/fx_all_clean_badge.png", "progress/progress_one_pearl.png",
			"progress/progress_two_pearls.png", "progress/progress_three_pearls.png"]:
		_ck("fx_" + fx.get_file().get_basename(), ResourceLoader.exists(SKIN + fx), fx)


func _clean_root() -> Node3D:
	return main.g.get("clean_root") as Node3D


func _skins() -> Array:
	var root: Node3D = _clean_root()
	if not is_instance_valid(root):
		return []
	return root.find_children("*", "Sprite3D", true, false)


func _target_by_id(target_id: String) -> Dictionary:
	for value: Variant in (main.g.get("clean_targets", []) as Array):
		var entry: Dictionary = value as Dictionary
		if String(entry["id"]) == target_id:
			return entry
	return {}


func _stand_at(pos: Vector3) -> void:
	main.player.position = pos
	main.player.vel = Vector3.ZERO


func _idle_near(target: Dictionary, seconds: float) -> void:
	# zero input: the stick is centred and the action button is released
	main.touch_ui.stick_vec = Vector2.ZERO
	main.touch_ui.action_down = false
	var steps: int = int(seconds * 60.0)
	for _index in range(steps):
		_stand_at(target["pos"] as Vector3)
		await process_frame


func _await_cool(entry: Dictionary, budget_ms: int) -> void:
	# Headless Godot does NOT run at 60fps, so a frame count is not a clock
	# (the same trap JOLT_PHYSICS_AUDIT recorded). Wait on the real cooldown
	# state against a wall-clock budget, holding Roshan on the target so she
	# cannot drift away while the rub cooldown runs down.
	var deadline: int = Time.get_ticks_msec() + budget_ms
	while Time.get_ticks_msec() < deadline:
		if float(entry.get("cool", 0.0)) <= 0.0:
			return
		if int(entry.get("rubs", 0)) >= CastleCleanup.RUBS_PER_TARGET:
			return
		_stand_at(entry["pos"] as Vector3)
		await process_frame


func _tap_clean(target: Dictionary, taps: int) -> void:
	for _index in range(taps):
		_stand_at(target["pos"] as Vector3)
		main.touch_ui.action_down = true
		await process_frame
		await process_frame
		main.touch_ui.action_down = false
		await _await_cool(target, 4000)


func _rub_clean(target: Dictionary, strokes: int) -> void:
	for index in range(strokes):
		_stand_at(target["pos"] as Vector3)
		main.touch_ui.stick_vec = Vector2(0.9, 0.0) if index % 2 == 0 else Vector2(-0.9, 0.0)
		await process_frame
		await process_frame
		await _await_cool(target, 4000)
	main.touch_ui.stick_vec = Vector2.ZERO


func _run() -> void:
	_audit_pack()
	var main_scene: PackedScene = load("res://scenes/main.tscn") as PackedScene
	main = main_scene.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	main._skip_intro()
	main.pearl_count = main.PEARL_TOTAL
	for friend_value in main.friends:
		var friend: Dictionary = friend_value
		friend["found"] = true
		friend["won"] = true
	main.trophies = 5
	await _frames(8)
	main._enter_level2()
	await _frames(18)
	main._enter_castle_interior()
	await _frames(30)

	var skins: Array = _skins()
	_ck("layer_built", not skins.is_empty(), "sprites=%d" % skins.size())
	var shaded := 0
	var tinted := 0
	for value: Variant in skins:
		var spr: Sprite3D = value as Sprite3D
		if spr.shaded:
			shaded += 1
		if spr.modulate != Color(1, 1, 1, 1):
			tinted += 1
	_ck("skins_unshaded", shaded == 0, "shaded=%d" % shaded)
	_ck("skins_ungraded", tinted == 0, "tinted at build=%d" % tinted)
	var root_node: Node3D = _clean_root()
	var lights: int = 0
	var bodies: int = 0
	if is_instance_valid(root_node):
		lights = root_node.find_children("*", "Light3D", true, false).size()
		bodies = root_node.find_children("*", "CollisionObject3D", true, false).size()
	_ck("no_new_lights", lights == 0, "Light3D under the cleaning root=%d" % lights)
	_ck("no_new_bodies", bodies == 0, "physics bodies under the cleaning root=%d" % bodies)

	var live: int = int((main.g.get("clean_targets", []) as Array).size())
	_ck("targets_registered", live == 30, "live targets=%d" % live)

	# --- agency: standing still on a target must never clean it -------------
	var passive_target: Dictionary = _target_by_id("playroom_puzzle_tiles")
	_ck("passive_target_found", not passive_target.is_empty(), "playroom_puzzle_tiles")
	if not passive_target.is_empty():
		await _idle_near(passive_target, 3.0)
		_ck("zero_input_cleans_nothing", int(passive_target.get("rubs", 0)) == 0
			and main.clean_done.is_empty(),
			"rubs=%d done=%d" % [int(passive_target.get("rubs", 0)), main.clean_done.size()])
		_ck("pointer_shows_the_target", String(main.g.get("clean_active", "")) == "playroom_puzzle_tiles",
			"active=%s" % String(main.g.get("clean_active", "")))

	# --- tap leg ------------------------------------------------------------
	if not passive_target.is_empty():
		await _tap_clean(passive_target, CastleCleanup.RUBS_PER_TARGET)
		await _frames(4)
		_ck("tap_target_cleans", bool(main.clean_done.get("playroom_puzzle_tiles", false)),
			"done=%s" % [main.clean_done.keys()])
		_ck("tap_target_saved", bool((main.save_data.get("clean_done", {}) as Dictionary).get(
			"playroom_puzzle_tiles", false)), "saved after the first finished object")
		_ck("tap_target_retired", _target_by_id("playroom_puzzle_tiles").is_empty(),
			"cleaned target leaves the live list")

	# --- rub (swipe) leg ----------------------------------------------------
	var rub_target: Dictionary = _target_by_id("library_book_cart")
	_ck("rub_target_found", not rub_target.is_empty(), "library_book_cart")
	if not rub_target.is_empty():
		await _rub_clean(rub_target, CastleCleanup.RUBS_PER_TARGET)
		await _frames(4)
		_ck("rub_target_cleans", bool(main.clean_done.get("library_book_cart", false)),
			"a stick rub is accepted like a tap")

	# --- room completion ----------------------------------------------------
	var loo_ids: Array[String] = [
		"loo_toilet_soap_ring", "loo_clean_water_splash",
		"loo_crooked_paper_rolls", "loo_brush_holder",
	]
	for loo_id: String in loo_ids:
		var loo_target: Dictionary = _target_by_id(loo_id)
		if loo_target.is_empty():
			continue
		await _tap_clean(loo_target, CastleCleanup.RUBS_PER_TARGET)
		await _frames(3)
	var loo_state: Dictionary = (main.g.get("clean_rooms", {}) as Dictionary).get("royal_loo", {})
	_ck("room_completes", int(loo_state.get("left", 99)) == 0,
		"royal_loo left=%d" % int(loo_state.get("left", 99)))
	_ck("room_saved", main.clean_done.size() >= 6, "saved objects=%d" % main.clean_done.size())

	# --- reload restores the exact cleaned set ------------------------------
	var expected: Array = main.clean_done.keys()
	expected.sort()
	main._load_save()
	var restored: Array = main.clean_done.keys()
	restored.sort()
	_ck("reload_restores_set", restored == expected, "restored=%d expected=%d" % [
		restored.size(), expected.size()])
	# rebuilding the castle must not re-dirty anything already finished
	main._enter_castle_interior()
	await _frames(30)
	var rebuilt_ids: Array[String] = []
	for value: Variant in (main.g.get("clean_targets", []) as Array):
		var entry: Dictionary = value as Dictionary
		rebuilt_ids.append(String(entry["id"]))
	var re_dirty: Array[String] = []
	for done_id: Variant in main.clean_done.keys():
		if String(done_id) in rebuilt_ids:
			re_dirty.append(String(done_id))
	_ck("cleaned_stays_clean", re_dirty.is_empty(), "re-dirtied=%s" % [re_dirty])

	print("CLEAN|RESULT=", "FAIL" if checks_failed > 0 else "OK", " checks_failed=", checks_failed)
	quit(1 if checks_failed > 0 else 0)


func _init() -> void:
	call_deferred("_run")
