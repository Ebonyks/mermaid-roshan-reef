extends Node
## Source-only native Mobile fixture. Never loads the game, saves or existing UI.

const ActorScript = preload("res://shared_actor.gd")
const FPS: int = 30
const DURATION: float = 7.6
const OUT_DIR: String = "res://raw_capture"

var avatar: ActorScript
var viewport: SubViewport
var camera: Camera2D
var caption: Label
var detail: Label
var running_fixture: bool = false
var automatic: bool = true
var live_time: float = 0.0
var checks: Array = []
var failures: Array = []
var swap_count: int = 0
var run_id: String = "interactive"


func _ready() -> void:
	var background: ColorRect = ColorRect.new()
	background.size = Vector2(1280, 720)
	background.color = Color(0.07, 0.13, 0.19)
	add_child(background)
	viewport = SubViewport.new()
	viewport.name = "NativeCharacterViewport"
	viewport.size = Vector2i(1280, 720)
	viewport.transparent_bg = true
	viewport.world_2d = World2D.new()
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	add_child(viewport)
	avatar = ActorScript.new()
	avatar.name = "Roshan"
	viewport.add_child(avatar)
	camera = Camera2D.new()
	camera.name = "ReviewCamera"
	camera.enabled = true
	camera.zoom = Vector2(0.90, 0.90)
	viewport.add_child(camera)
	_follow_camera()
	var picture: TextureRect = TextureRect.new()
	picture.texture = viewport.get_texture()
	picture.size = Vector2(1280, 720)
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(picture)
	caption = Label.new()
	caption.position = Vector2(22, 15)
	caption.add_theme_font_size_override("font_size", 25)
	caption.text = "Roshan — shared native rig / source prototype"
	add_child(caption)
	detail = Label.new()
	detail.position = Vector2(22, 650)
	detail.add_theme_font_size_override("font_size", 18)
	add_child(detail)
	for i in range(2):
		var button: Button = Button.new()
		var identity: String = "ballet" if i == 0 else "magician"
		button.text = identity.capitalize()
		button.position = Vector2(1000 + i * 130, 18)
		button.size = Vector2(122, 42)
		button.pressed.connect(func() -> void: avatar.apply_skin(identity))
		add_child(button)
	await get_tree().process_frame
	var args: PackedStringArray = OS.get_cmdline_user_args()
	for argument: String in args:
		if argument.begins_with("--run-id="):
			run_id = argument.trim_prefix("--run-id=")
	if args.has("--pose-preview"):
		running_fixture = true
		await _pose_preview()
	elif args.has("--verify-only"):
		running_fixture = true
		await _verify()
		get_tree().quit(0 if failures.is_empty() else 1)
	elif args.has("--capture"):
		running_fixture = true
		await _verify()
		if failures.is_empty():
			await _capture()
		get_tree().quit(0 if failures.is_empty() else 1)


func _process(delta: float) -> void:
	if running_fixture:
		return
	if automatic:
		live_time += minf(delta, 0.05)
		if live_time > DURATION + 1.0:
			live_time = 0.0
			avatar.reset_travel()
			avatar.pose_at(0.0)
		avatar.advance_motion(minf(delta, 0.05))
	_follow_camera()
	detail.text = "Costume: %s    Phase: %.3fs    Same actor: %s    Space: pause/resume" % [avatar.skin_id, avatar.player.current_animation_position, avatar.get_instance_id()]


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.is_pressed() and not event.is_echo():
		if event.keycode == KEY_SPACE:
			automatic = not automatic
		elif event.keycode == KEY_B:
			avatar.apply_skin("ballet")
		elif event.keycode == KEY_M:
			avatar.apply_skin("magician")


func _follow_camera() -> void:
	camera.position = avatar.position + Vector2(450, 335)


func _check(name_string: String, condition: bool, evidence: Variant = null) -> void:
	checks.append({"name": name_string, "pass": condition, "evidence": evidence})
	if not condition:
		failures.append(name_string)
	print("SHAREDSWIM|", name_string, "|", "OK" if condition else "FAIL")


func _save_json(path: String, value: Variant) -> void:
	if typeof(value) == TYPE_DICTIONARY:
		value["run_id"] = run_id
	var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
	assert(file != null, "Cannot write fixture evidence")
	file.store_string(JSON.stringify(value, "\t") + "\n")
	file.close()


func _same_snapshot(a: Dictionary, b: Dictionary) -> bool:
	return a == b


func _matrix(value: Transform2D) -> Array:
	return [value.x.x, value.x.y, value.y.x, value.y.y, value.origin.x, value.origin.y]


func _bone_state() -> Dictionary:
	var result: Dictionary = {}
	for name_string: String in avatar.bones:
		result[name_string] = _matrix(avatar.local_bone_transform(name_string))
	return result


func _verify() -> void:
	var version: Dictionary = Engine.get_version_info()
	_check("approved exact engine", int(version["major"]) == 4 and int(version["minor"]) == 7 and int(version["patch"]) == 2 and str(version["status"]) == "stable", version)
	avatar.pose_at(1.3)
	avatar.apply_skin("ballet")
	var initial: Dictionary = avatar.identity_snapshot()
	_check("one shared native skeleton", avatar.skeleton is Skeleton2D and avatar.bones.size() == 19, initial)
	var representative: Array = []
	var swaps_ok: bool = true
	var maximum_phase_change: float = 0.0
	var begin: int = Time.get_ticks_msec()
	for i in range(2048):
		var t: float = fmod(float(i) * 0.03717 + 0.137, 7.15)
		avatar.pose_at(t)
		avatar.position = Vector2(float(i % 13) * 3.0, float(i % 7) * -2.0)
		avatar.velocity = Vector2(31.25, -11.125)
		var before: Dictionary = avatar.identity_snapshot()
		var accepted: bool = avatar.apply_skin("magician" if i % 2 == 0 else "ballet")
		var after: Dictionary = avatar.identity_snapshot()
		maximum_phase_change = maxf(maximum_phase_change, absf(float(after["phase"]) - float(before["phase"])))
		if not accepted or not _same_snapshot(before, after):
			swaps_ok = false
			failures.append("swap invariant at " + str(i))
			break
		swap_count += 1
		if i % 256 == 0:
			representative.append({"index": i, "skin": avatar.skin_id, "before": before, "after": after})
		if i % 32 == 0:
			await get_tree().process_frame
	_check("2048 costume swaps preserve actor bones rest anatomy phase root and velocity", swaps_ok and swap_count == 2048, {"max_phase_delta": maximum_phase_change, "elapsed_ms": Time.get_ticks_msec() - begin, "samples": representative})
	avatar.pose_at(0.731)
	avatar.reset_travel()
	avatar.apply_skin("ballet")
	var restoration: Dictionary = avatar.identity_snapshot()
	var slot_textures: Array = []
	for slot: String in avatar.slot_nodes:
		slot_textures.append(avatar.slot_nodes[slot].texture.get_instance_id())
	avatar.apply_skin("magician")
	avatar.apply_skin("ballet")
	var restored_textures: Array = []
	for slot: String in avatar.slot_nodes:
		restored_textures.append(avatar.slot_nodes[slot].texture.get_instance_id())
	_check("original selected Ballet skin restores exact resident textures", restoration == avatar.identity_snapshot() and slot_textures == restored_textures)
	var doc: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://skins/magician.json"))
	for kind: String in ["foreign_rig", "unknown_view", "missing_slot", "code", "duplicate", "bad_hash", "escape", "anatomy"]:
		var invalid: Dictionary = doc.duplicate(true)
		match kind:
			"foreign_rig": invalid["rig"]["id"] = "another_character"
			"unknown_view": invalid["views"] = ["unpainted_profile"]
			"missing_slot": invalid["coverage"]["swim_right_quarter"].erase("body_front")
			"code": invalid["script"] = "costume_builder.gd"
			"duplicate": invalid["attachments"][1]["slot"] = invalid["attachments"][0]["slot"]
			"bad_hash": invalid["attachments"][0]["texture"]["sha256"] = "0000"
			"escape": invalid["attachments"][0]["texture"]["path"] = "../outside.png"
			"anatomy": invalid["attachments"][0]["texture"] = avatar.anatomy["parts"][0]["texture"].duplicate(true)
		var before: Dictionary = avatar.identity_snapshot()
		var old_skin: String = avatar.skin_id
		var accepted: bool = avatar.try_skin_document(invalid)
		_check("atomic rejection " + kind, not accepted and before == avatar.identity_snapshot() and old_skin == avatar.skin_id, avatar.last_error)
	avatar.paused = true
	var pause_time: float = avatar.player.current_animation_position
	avatar.apply_skin("magician")
	avatar.advance_motion(0.5)
	await get_tree().process_frame
	_check("paused costume swap keeps phase", avatar.player.current_animation_position == pause_time and avatar.paused)
	avatar.paused = false
	avatar.advance_motion(1.0 / 30.0)
	_check("animation advances from the preserved phase", absf(avatar.player.current_animation_position - pause_time - 1.0 / 30.0) < 0.000001)
	avatar.pose_at(0.0, "cycle")
	var cycle_start: Dictionary = _bone_state()
	avatar.pose_at(1.9, "cycle")
	var cycle_end: Dictionary = _bone_state()
	var loop_error: float = 0.0
	for name_string: String in cycle_start:
		for i in range(6):
			loop_error = maxf(loop_error, absf(float(cycle_start[name_string][i]) - float(cycle_end[name_string][i])))
	_check("cycle actor-local endpoint matrices", loop_error <= 0.00001, loop_error)
	var deterministic: bool = true
	for i in range(128):
		var t: float = fmod(float(i) * 0.293, 7.2)
		avatar.pose_at(t)
		var before: Dictionary = _bone_state()
		avatar.pose_at(fmod(t + 1.7, 7.3))
		avatar.pose_at(t)
		if before != _bone_state():
			deterministic = false
	_check("128 out-of-order seeks restore exact pose", deterministic)
	var ablations: Array = []
	for enabled: bool in [false, true]:
		avatar.tail_motion_enabled = enabled
		avatar.reset_travel()
		for i in range(913):
			var t: float = float(i) / 120.0
			avatar.pose_at(t)
			avatar.integrate_travel(1.0 / 120.0, t)
		ablations.append({"tail_enabled": enabled, "distance": avatar.position.length(), "end_speed": avatar.velocity.length(),
			"fin_turn": avatar.fin_turn, "fin_cup": avatar.fin_cup, "disabled_scope": "Hips, TailA-D, Fin bones and shared fin material view"})
	_check("tail-disabled rest has zero propulsion and stroke produces travel", float(ablations[0]["distance"]) < 0.000001 and float(ablations[1]["distance"]) > 5.0, ablations)
	_check("braking resolves to quiet travel endpoint", float(ablations[1]["end_speed"]) < 0.5, ablations[1])
	avatar.tail_motion_enabled = true
	avatar.pose_at(0.0)
	avatar.reset_travel()
	avatar.apply_skin("ballet")
	var final: Dictionary = avatar.identity_snapshot()
	_check("resident node texture and geometry counts stay bounded", initial["node_count"] == final["node_count"] and initial["texture_count"] == final["texture_count"] and initial["mesh_count"] == final["mesh_count"], {"initial": initial, "final": final})
	_save_json("res://evidence/native_swap_tests.json", {"pass": failures.is_empty(), "checks": checks,
		"swaps": swap_count, "failures": failures, "actor_instances_constructed": 1,
		"renderer": RenderingServer.get_current_rendering_method(), "version": version,
		"visual_acceptance": false, "actual_device_verified": false, "owner_accepted": false})
	print("SHAREDSWIM|SWAP_TESTS|", "PASS" if failures.is_empty() else "FAIL")


func _sample(t: float, index: int, file_path: String) -> Dictionary:
	return {"index": index, "time": t, "skin": avatar.skin_id,
		"actor_id": avatar.get_instance_id(), "animator_id": avatar.player.get_instance_id(),
		"phase": avatar.player.current_animation_position, "fin_state": avatar.fin_state,
		"fin_turn_degrees": avatar.fin_turn, "fin_cup_weight": avatar.fin_cup,
		"root": [avatar.position.x, avatar.position.y], "velocity": [avatar.velocity.x, avatar.velocity.y],
		"thrust_acceleration": avatar.thrust_acceleration, "bones": _bone_state(),
		"frame": file_path, "png_sha256": FileAccess.get_sha256(file_path) if file_path != "" else ""}


func _pose_preview() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://raw_pose"))
	var samples: Array = []
	for skin: String in ["ballet", "magician"]:
		avatar.apply_skin(skin)
		for index in range(4):
			var t: float = [0.0, 1.6, 3.2, 6.4][index]
			avatar.pose_at(t)
			_follow_camera()
			await RenderingServer.frame_post_draw
			var path: String = "res://raw_pose/%s_%d.png" % [skin, index]
			var image: Image = viewport.get_texture().get_image()
			image.save_png(ProjectSettings.globalize_path(path))
			samples.append(_sample(t, index, path))
	_save_json("res://evidence/pose_preview.json", {"samples": samples, "renderer": RenderingServer.get_current_rendering_method(), "version": Engine.get_version_info()})
	print("SHAREDSWIM|POSE_PREVIEW_COMPLETE|8")
	get_tree().quit()


func _capture() -> void:
	_check("actual Mobile rendering", RenderingServer.get_current_rendering_method() == "mobile")
	var jobs: Array = [{"id": "ballet", "skin": "ballet"}, {"id": "magician", "skin": "magician"}, {"id": "live_swaps", "skin": "ballet"}]
	var counts: Dictionary = {}
	var swap_evidence: Array = []
	for job: Dictionary in jobs:
		var directory: String = OUT_DIR + "/" + str(job["id"])
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(directory))
		avatar.apply_skin(str(job["skin"]))
		avatar.reset_travel()
		avatar.pose_at(0.0)
		var samples: Array = []
		var count: int = int(round(DURATION * FPS)) + 1
		for index in range(count):
			var t: float = float(index) / FPS
			if index > 0:
				avatar.advance_motion(1.0 / FPS)
			if job["id"] == "live_swaps" and index in [37, 76, 113, 154, 187]:
				var before: Dictionary = avatar.identity_snapshot()
				avatar.apply_skin("magician" if avatar.skin_id == "ballet" else "ballet")
				var after: Dictionary = avatar.identity_snapshot()
				_check("rendered live swap phase " + str(index), before == after)
				swap_evidence.append({"frame": index, "skin": avatar.skin_id, "before": before, "after": after})
			_follow_camera()
			await RenderingServer.frame_post_draw
			var path: String = directory + "/frame_%04d.png" % index
			var image: Image = viewport.get_texture().get_image()
			image.save_png(ProjectSettings.globalize_path(path))
			samples.append(_sample(t, index, path))
		_save_json("res://evidence/" + str(job["id"]) + "_samples.json", {"fps": FPS, "samples": samples, "camera_offset": [450, 335], "camera_zoom": 0.9})
		counts[str(job["id"])] = samples.size()
	_save_json("res://evidence/native_capture_complete.json", {"pass": failures.is_empty(), "counts": counts,
		"swaps": swap_evidence, "actor_instances_constructed": 1,
		"renderer": RenderingServer.get_current_rendering_method(), "version": Engine.get_version_info(),
		"source_only": true, "visual_device_owner_acceptance": false})
	print("SHAREDSWIM|NATIVE_CAPTURE_COMPLETE|", JSON.stringify(counts))
