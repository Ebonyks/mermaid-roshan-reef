extends SceneTree
# Focused headless contract for the new Stage 1 -> Stage 2 -> Stage 3 spine.

var failures := 0
var main: ReefMain

const PROMENADE_MASTER := "res://assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_3x1.png"
const PROMENADE_MASTER_SHA256 := "7952b4579c922025a3030b3ddd976247fde138f697f00468b5a08fd5b88d66e3"
const PROMENADE_TILE_PATHS: Array[String] = [
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_0.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_1.png",
	"res://assets/flats/sky_lagoon/main/flat_sky_lagoon_main_panorama_tile_2.png",
]
const PROMENADE_TILE_SHA256: Array[String] = [
	"78b1a33e5487d9dfbb75ab92fea5de84c20f4c1a7164eb5b1e8c8e9dba842703",
	"b32ac8aebab3cbdf5d82a00f7004104981039a487ea0df829a44061b5e110a78",
	"ee3477137069b0fe3a5e007d84ca79fbdd52e82c2fa796c8ebbd988dcd159e3a",
]
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
	_check("opening fallback does not stretch a background plate",
		main.intro_layer != null
		and String(main.intro_layer.get_meta("cinematic_fallback_art", "x")) == "")
	main._skip_intro()
	await process_frame
	_check("opening completion saved in memory", main.opening_seen)

	main.arrival_imp_seen = false
	main._enter_level2_now(false, false, true)
	await process_frame
	await process_frame
	_check("stage two is the 2D promenade", main.game == "level2"
		and String(main.g.get("phase", "")) == "promenade")
	var master_image: Image = Image.load_from_file(
		ProjectSettings.globalize_path(PROMENADE_MASTER))
	_check("preserved native panorama keeps exact 3 to 1 ratio",
		master_image != null and master_image.get_width() == 2172
		and master_image.get_height() == 724
		and FileAccess.get_sha256(PROMENADE_MASTER) == PROMENADE_MASTER_SHA256)
	var background_values: Array = main.g.get("promenade_background_cards", []) as Array
	var background_cards: Array[Sprite3D] = []
	var tiles_valid := background_values.size() == 3
	for index in range(background_values.size()):
		var card := background_values[index] as Sprite3D
		if card == null:
			tiles_valid = false
			continue
		background_cards.append(card)
		var texture: Texture2D = card.texture
		tiles_valid = (tiles_valid and not card.shaded and texture != null
			and texture.get_width() == 724 and texture.get_height() == 724
			and is_equal_approx(card.position.z, -18.0)
			and FileAccess.get_sha256(PROMENADE_TILE_PATHS[index]) == PROMENADE_TILE_SHA256[index]
			and card.get_meta("source_rect") == SkyLagoonPromenade.BACKDROP_TILE_RECTS[index])
	_check("three lossless background tiles are unshaded at coherent depth", tiles_valid)
	var reconstructed: Image = Image.create(2172, 724, false, master_image.get_format())
	for index in range(PROMENADE_TILE_PATHS.size()):
		var tile_image: Image = Image.load_from_file(PROMENADE_TILE_PATHS[index])
		reconstructed.blit_rect(tile_image, Rect2i(0, 0, 724, 724),
			Vector2i(index * 724, 0))
	_check("decoded tiles reconstruct every master pixel exactly",
		reconstructed.get_data() == master_image.get_data())
	var seam_geometry_ok := background_cards.size() == 3
	if seam_geometry_ok:
		for index in range(2):
			var left: Sprite3D = background_cards[index]
			var right: Sprite3D = background_cards[index + 1]
			var left_edge: float = left.position.x + float(left.texture.get_width()) * left.pixel_size * 0.5
			var right_edge: float = right.position.x - float(right.texture.get_width()) * right.pixel_size * 0.5
			seam_geometry_ok = seam_geometry_ok and absf(left_edge - right_edge) <= 0.0001
	_check("background cards reconstruct with zero world-space seam gap", seam_geometry_ok)
	var background_card: Sprite3D = background_cards[0] if not background_cards.is_empty() else null
	var imp_state: Dictionary = main.g.get("arrival_imp", {}) as Dictionary
	var imp_card: Sprite3D = imp_state.get("node") as Sprite3D
	_check("first arrival imp is an unshaded foreground Sprite3D card",
		imp_card != null and background_card != null and not imp_card.shaded
		and imp_card.position.z > background_card.position.z
		and FileAccess.get_sha256(SkyLagoonPromenade.IMP_TEX) == IMP_SHA256)
	var stage_root: Node3D = main.g.get("ss_root") as Node3D
	var stage_cards: Array[Node] = stage_root.find_children("*", "Sprite3D", true, false)
	var all_cards_unshaded := true
	for stage_node: Node in stage_cards:
		all_cards_unshaded = all_cards_unshaded and not (stage_node as Sprite3D).shaded
	_check("stage two world inventory is cards only at real depth",
		stage_cards.size() == 24 and all_cards_unshaded
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
	_check("stage three fallback rejects undersized or ratio-changed plates",
		main.intro_layer != null
		and String(main.intro_layer.get_meta("cinematic_fallback_art", "x")) == "")
	main._cinematic_ref().finish()
	await process_frame
	_check("reveal completion saved in memory", main.castle_reveal_seen)
	_check("dirty castle is a 2D gameplay phase", String(main.g.get("phase", "")) == "dirty_castle"
		and main.dirty_castle_layer != null)
	var dirty: DirtyCastleStage = main._dirty_castle_ref()
	_check("cleaning exception is a non-navigable full-screen Control minigame",
		String(main.dirty_castle_layer.get_meta("presentation_kind", "")) == "full_screen_control_minigame"
		and not bool(main.dirty_castle_layer.get_meta("navigable_world", true))
		and main.dirty_castle_layer.find_children("*", "Node3D", true, false).is_empty())
	_check("cleaning stage has no generated background plate",
		dirty.background is ColorRect
		and String(main.dirty_castle_layer.get_meta("runtime_background_kind", "")) == "code_native_control_color"
		and String(main.dirty_castle_layer.get_meta("runtime_plate", "x")) == "")
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
