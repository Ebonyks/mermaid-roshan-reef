extends SceneTree
## Windowed Mobile-render capture set for MA-OPERA-012:
## nine Castle-room career route sets and all thirteen direct Canvas careers.

const ROUTE_ROOMS: Array[String] = [
	"kitchen", "opera_hall", "library", "craft_room", "playroom",
	"bubble_bath", "mermaid_pool", "dining_room", "movie_lounge",
]

var main: ReefMain
var rooms: CastleRooms25D
var routes: CastleCareerRoutes
var out_dir := ""
var failed := 0


func _settle(frames: int) -> void:
	for _frame: int in range(frames):
		await process_frame


func _settle_for_stage(stage_id: String, canvas_layer: int, max_frames := 120) -> void:
	# Fade reveal time is elapsed-time based, not frame-count based. Wait for
	# the shipping main loop to select and paint the requested ambient stage so
	# a fast desktop render cannot capture the Castle stage under a new career.
	for _frame: int in range(max_frames):
		await process_frame
		if main.living_stage_id == stage_id and main.living_layer != null \
				and main.living_layer.visible \
				and main.living_layer.layer == canvas_layer:
			return


func _shot(name: String) -> void:
	await _settle(4)
	await RenderingServer.frame_post_draw
	var image: Image = get_root().get_viewport().get_texture().get_image()
	var error: Error = image.save_png(out_dir.path_join(name + ".png"))
	if error != OK:
		failed += 1
	print("OPERASHOT|", name, "|", "OK" if error == OK else "FAIL")


func _capture_room_routes() -> void:
	for room_id: String in ROUTE_ROOMS:
		rooms.show_room(room_id, false)
		await _settle_for_stage("castle.room.%s" % room_id, 15)
		routes.sync()
		var expected := CastleCareerRoutes.act_indices_for_room(room_id)
		var actual: Array[int] = []
		for button: Button in routes.buttons:
			actual.append(int(button.get_meta("act_index", -1)))
		var layer_contract := main.castle_room_layer != null \
				and main.castle_room_layer.visible \
				and main.castle_room_layer.layer == 14 \
				and main.living_layer != null and main.living_layer.visible \
				and main.living_layer.layer == 15 \
				and main.living_stage_id == "castle.room.%s" % room_id \
				and main.pause_layer != null and main.pause_layer.layer == 16
		if actual != expected or routes.root == null or not routes.root.visible \
				or not layer_contract:
			failed += 1
			print("OPERASHOT|castle_career_routes_%s|FAIL|expected=%s actual=%s layers=%s/%s/%s stage=%s" % [
				room_id, str(expected), str(actual),
				str(main.castle_room_layer.layer if main.castle_room_layer != null else -1),
				str(main.living_layer.layer if main.living_layer != null else -1),
				str(main.pause_layer.layer if main.pause_layer != null else -1),
				main.living_stage_id,
			])
			continue
		await _shot("castle_career_routes_%s" % room_id)


func _remove_current_act() -> void:
	var opera := main.opera_game as OperaHouse
	if opera == null:
		return
	opera._leave_early()
	await _settle(4)


func _capture_act_sets() -> void:
	for index: int in OperaHouse.LIVE_ACT_INDICES:
		await _remove_current_act()
		var room_id := CastleCareerRoutes.room_for_act(index)
		rooms.show_room(room_id, false)
		await _settle(4)
		routes.sync()
		var button := routes.button_for_act(index)
		var config: Dictionary = OperaHouse.ACTS[index]
		var slug := String(config.get("career", "career")).to_lower().replace(" ", "_")
		if button == null or not button.visible:
			failed += 1
			print("OPERASHOT|opera_act_%02d_%s|FAIL|missing %s route" % [
				index + 1, slug, room_id,
			])
			continue
		# Emit the shipping picture control rather than calling OperaHouse
		# privately. ReefMain records the exact return room before the direct act.
		button.pressed.emit()
		await _settle_for_stage("opera.act.%02d" % index, 11)
		var opera := main.opera_game as OperaHouse
		var current := opera.act as OperaAct if opera != null else null
		if opera == null or current == null or current.career_world_2d == null \
				or main.opera_return_room != room_id or opera.act_index != index:
			failed += 1
			print("OPERASHOT|opera_act_%02d_%s|FAIL|direct start from %s" % [
				index + 1, slug, room_id,
			])
			continue
		var layer_contract := current.career_world_2d.layer == 10 \
				and main.living_layer != null and main.living_layer.visible \
				and main.living_layer.layer == 11 \
				and main.living_stage_id == "opera.act.%02d" % index \
				and main.hud_layer != null and main.hud_layer.visible \
				and main.hud_layer.layer == 12 \
				and main.pause_layer != null and main.pause_layer.layer == 13
		if not layer_contract:
			failed += 1
			print("OPERASHOT|opera_act_%02d_%s|FAIL|layers=%s/%s/%s/%s stage=%s" % [
				index + 1, slug, str(current.career_world_2d.layer),
				str(main.living_layer.layer if main.living_layer != null else -1),
				str(main.hud_layer.layer if main.hud_layer != null else -1),
				str(main.pause_layer.layer if main.pause_layer != null else -1),
				main.living_stage_id,
			])
			continue
		current.set_process(false)
		current.career_world_2d.set_process(false)
		await _shot("opera_act_%02d_%s_from_%s" % [index + 1, slug, room_id])


func _init() -> void:
	if DisplayServer.get_name() == "headless":
		print("OPERASHOT|RESULT|HEADLESS SKIP")
		quit()
		return
	var requested: String = OS.get_environment("OPERA_SHOT_OUT")
	out_dir = requested if not requested.is_empty() \
		else ProjectSettings.globalize_path("res://tmp/opera_shots")
	DirAccess.make_dir_recursive_absolute(out_dir)
	seed(20260812)
	var scene := load("res://scenes/main.tscn") as PackedScene
	main = scene.instantiate() as ReefMain
	get_root().add_child(main)
	await _settle(2)
	if main.intro_active:
		main._skip_intro()
	await _settle(12)
	main.opera_progress = 0
	main.opera_stars = 0
	main.opera_done = false
	main.game = "level2"
	main._enter_castle_interior_now(false)
	await _settle(24)
	rooms = main._castle_rooms_ref()
	routes = main._castle_career_routes_ref()
	if not rooms.is_open() or main.castle_room_stage == null:
		print("OPERASHOT|RESULT|FAIL|Castle room stage did not start")
		quit(1)
		return
	if main.hud_layer != null:
		main.hud_layer.visible = false
	if main.player != null:
		main.player.visible = false
		main.player.set_process(false)
	await _capture_room_routes()
	await _capture_act_sets()
	await _remove_current_act()
	if rooms.is_open():
		rooms.close()
	main.queue_free()
	await _settle(4)
	print("OPERASHOT|RESULT|", "ALL OK" if failed == 0 else "%d FAILED" % failed)
	print("OPERASHOT|DONE|", out_dir)
	quit(0 if failed == 0 else 1)
