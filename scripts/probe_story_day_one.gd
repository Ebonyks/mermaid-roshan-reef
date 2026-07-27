extends SceneTree
# Focused headless contract for the new Stage 1 -> Stage 2 -> Stage 3 spine.

var failures := 0
var main: ReefMain

const PROMENADE_PLATE := "res://assets/flats/sky_lagoon/main/day_one_promenade_2048x1024.svg"
const PROMENADE_SHA256 := "b1e3346d79671f2616b00b53e6bb1b26cd7470adb777bf0ac48039a5f9f71e77"
const CASTLE_PLATE := "res://assets/flats/dirty_castle/day_one_dirty_castle_2048x1024.svg"
const CASTLE_SHA256 := "0e90e1e10fb9856a73f08fc9406556ad4a7a0597e049a635dd2520d1b11bf944"
const IMP_SHA256 := "ab1026350656ac43f6c4576d4fec6658b61b702fc0cd7801a9e5ea2cc14174d5"

func _check(label: String, ok: bool) -> void:
	print("DAYONE|", label, ": ", "OK" if ok else "FAIL")
	if not ok:
		failures += 1

func _init() -> void:
	var packed := load("res://scenes/main.tscn") as PackedScene
	main = packed.instantiate() as ReefMain
	root.add_child(main)
	await process_frame
	await process_frame
	_check("opening cinematic active", main.intro_active)
	_check("opening has one continue", main.intro_layer != null
		and main.intro_layer.find_child("IntroContinueButton", true, false) != null)
	main._skip_intro()
	await process_frame
	_check("opening completion saved in memory", main.opening_seen)

	main.arrival_imp_seen = false
	main._enter_level2_now(false, false, true)
	await process_frame
	await process_frame
	_check("stage two is the 2D promenade", main.game == "level2"
		and String(main.g.get("phase", "")) == "promenade")
	var background_card: Sprite3D = main.g.get("promenade_background_card") as Sprite3D
	var background_texture: Texture2D = background_card.texture if background_card != null else null
	_check("stage two background is an unshaded native 2K Sprite3D card",
		background_card != null and not background_card.shaded
		and background_texture != null and background_texture.get_width() == 2048
		and background_texture.get_height() == 1024
		and FileAccess.get_sha256(PROMENADE_PLATE) == PROMENADE_SHA256)
	var imp_state: Dictionary = main.g.get("arrival_imp", {}) as Dictionary
	var imp_card: Sprite3D = imp_state.get("node") as Sprite3D
	_check("first arrival imp is an unshaded foreground Sprite3D card",
		imp_card != null and not imp_card.shaded
		and imp_card.position.z > background_card.position.z
		and FileAccess.get_sha256(SkyLagoonPromenade.IMP_TEX) == IMP_SHA256)
	var stage_root: Node3D = main.g.get("ss_root") as Node3D
	var stage_cards: Array[Node] = stage_root.find_children("*", "Sprite3D", true, false)
	var all_cards_unshaded := true
	for stage_node: Node in stage_cards:
		all_cards_unshaded = all_cards_unshaded and not (stage_node as Sprite3D).shaded
	_check("stage two world inventory is cards only at real depth",
		stage_cards.size() == 22 and all_cards_unshaded
		and stage_root.find_children("*", "MeshInstance3D", true, false).is_empty()
		and stage_root.find_children("*", "CanvasItem", true, false).is_empty())
	var plane_target: Dictionary = (main.g.get("lagoon_promenade_targets", []) as Array)[0] as Dictionary
	var plane_node: Node3D = plane_target.get("node") as Node3D
	var plane_screen: Vector2 = main.player.cam.unproject_position(plane_node.global_position)
	_check("stage two touch uses camera-ray card intersection",
		String(main._lagoon_promenade_ref()._target_at(plane_screen).get("id", "")) == "plane")
	for index in range(55):
		main._lagoon_promenade_ref().tick(0.1)
	_check("imp escape completes once", main.arrival_imp_seen)
	main._enter_level2_now(false, false, true)
	_check("imp does not replay after completion",
		(main.g.get("arrival_imp", {}) as Dictionary).is_empty())

	main.castle_reveal_seen = false
	main._begin_dirty_castle_entry()
	_check("stage three reveal blocks gameplay", main.intro_active
		and main._cinematic_ref().is_active())
	main._cinematic_ref().finish()
	await process_frame
	_check("reveal completion saved in memory", main.castle_reveal_seen)
	_check("dirty castle is a 2D gameplay phase", String(main.g.get("phase", "")) == "dirty_castle"
		and main.dirty_castle_layer != null)
	var dirty: DirtyCastleStage = main._dirty_castle_ref()
	var castle_texture: Texture2D = dirty.background.texture if dirty.background != null else null
	_check("cleaning exception is a non-navigable full-screen Control minigame",
		String(main.dirty_castle_layer.get_meta("presentation_kind", "")) == "full_screen_control_minigame"
		and not bool(main.dirty_castle_layer.get_meta("navigable_world", true))
		and main.dirty_castle_layer.find_children("*", "Node3D", true, false).is_empty())
	_check("cleaning background is exact native 2K master",
		castle_texture != null and castle_texture.get_width() == 2048
		and castle_texture.get_height() == 1024
		and FileAccess.get_sha256(CASTLE_PLATE) == CASTLE_SHA256)
	var first_target := dirty.current_target_id()
	var before := dirty.targets_left()
	for index in range(30):
		dirty.tick(0.1)
	_check("zero input cleans nothing", dirty.targets_left() == before)
	dirty.rub_active()
	dirty.rub_active()
	dirty.rub_active()
	_check("three taps clean exactly one object", dirty.targets_left() == before - 1)
	_check("object completion saves immediately", bool(main.clean_done.get(first_target, false))
		and bool((main.save_data.get("clean_done", {}) as Dictionary).get(first_target, false)))
	var persisted: Dictionary = {}
	if FileAccess.file_exists(main.SAVE_PATH):
		var file := FileAccess.open(main.SAVE_PATH, FileAccess.READ)
		if file != null:
			var parsed: Variant = JSON.parse_string(file.get_as_text())
			if parsed is Dictionary:
				persisted = parsed as Dictionary
	_check("story and object progress reach disk",
		bool(persisted.get("opening_seen", false))
		and bool(persisted.get("arrival_imp_seen", false))
		and bool(persisted.get("castle_reveal_seen", false))
		and bool((persisted.get("clean_done", {}) as Dictionary).get(first_target, false)))
	_check("new stage adds no physics bodies or lights",
		main.dirty_castle_layer.find_children("*", "PhysicsBody3D", true, false).is_empty()
		and main.dirty_castle_layer.find_children("*", "Light3D", true, false).is_empty())

	print("DAYONE|RESULT: ", "ALL OK" if failures == 0 else "%d FAIL" % failures)
	quit(0 if failures == 0 else 1)
